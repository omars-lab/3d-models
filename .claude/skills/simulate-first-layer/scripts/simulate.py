#!/usr/bin/env python3
"""What a first layer will look like before it prints: the slicer's plan, drawn and measured.

This is the simulate-first-layer skill's tool. It simulates the slicer's PLAN, not the print: it
slices locally with Bambu Studio, reads the first layer's moves out of the G-code and draws every
line as a bead of its planned width (tools/print_review.py), then counts the bare bed the lines
leave (tools/bed_face_sweep.py's score). Nothing here re-implements either; nothing is ever sent to
the printer.

The plan cannot see squash and spread, pressure lag at line ends, or bed height. `--spread` takes
`plan`, which draws every bead exactly as the slicer planned it (Plan), and numbers, which stand in
for the first and the last and are Theory, not Measured: every bead is drawn
`spread x flow x h/(h - lower)` times its planned width (h the first layer's height, flow the
first-layer flow ratio, lower how much closer the nozzle starts to the bed). So spread 1.0 already
counts a piece's extra flow; `plan` counts nothing the drawing cannot see. The model keeps the
plastic's volume and lets the bead widen; nothing has measured how a real bead spreads.

  simulate.py run <variant.yaml> [--spread plan,1.0,1.1,1.2] one variant beside stock, sliced alike
  simulate.py plate <recipe.yaml | plate.3mf> [--spread plan] every piece on a plate, one row each
  simulate.py calibrate [--spread plan,1.0,1.1,1.2]           the plan against Omar's verdicts
  simulate.py --self-test

A variant file (every key optional; the default is the bedface-4/5 piece, sliced stock):

  name: overlap-75-flow-110                    # names the output folder
  bkr: bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr
  params: { strap: 3.75 }                      # merged over the piece's default params
  window: 50@13,30
  object_settings: { infill_wall_overlap: "75%", initial_layer_flow_ratio: "1.1" }   # per piece
  plate_settings: { wall_generator: arachne, wall_loops: "5" }   # whole plate, a process file via -s
  lower_mm: 0.0                                # Theory only: a nozzle this much closer to the bed

Every result carries calibrate's agreement line (from the last calibrate run, cached), so a number
is never read without how far the plan has tracked the prints.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "tools/print_review.py").exists())
sys.path.insert(0, str(ROOT / "tools"))
import bed_face_sweep as bfs  # noqa: E402
import print_review as pr  # noqa: E402
import yaml  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

SKILL = Path(__file__).resolve().parents[1]
PAIRS = SKILL / "judged-pairs.yaml"
OUT = ROOT / "build/simulate"
MACHINE, PROCESS, FILAMENT = bfs.NOZZLES["0.4"]
PIECE = {"bkr": "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr",
         "params": {"size": 112.5, "strap": 3.75, "height": 4.4, "round": 1.25},
         "window": "50@13,30"}
SPREADS = "plan,1.0,1.1,1.2"
EXTRUDING = ("G0 ", "G1 ", "G2 ", "G3 ")
START = "; start printing object, unique label id:"
STOP = "; stop printing object, unique label id:"
CAPTION_PX = 60


# ---- slicing ----------------------------------------------------------------------------------

def recipe_text(v, label):
    """A one-piece scratch recipe for a variant: never printed, no id carved."""
    params = {**PIECE["params"], **(v.get("params") or {})}
    lines = ["# scratch: simulate-first-layer, never printed", "bed: x2d", "profile:",
             f'  settings: "{MACHINE};{PROCESS}"', f'  filament: "{FILAMENT}"', "", "items:",
             f"  - bkr:    {v.get('bkr', PIECE['bkr'])}",
             "    params: { " + ", ".join(f"{k}: {x}" for k, x in params.items()) + " }"]
    if v.get("window", PIECE["window"]):
        lines.append(f"    window: {v.get('window', PIECE['window'])}")
    lines += [f"    label:  {label}", '    no_id:  "scratch slice, not printed"']
    if v.get("object_settings"):
        lines.append("    object_settings: { " + ", ".join(
            f'{k}: "{x}"' for k, x in v["object_settings"].items()) + " }")
    return "\n".join(lines) + "\n"


def process_text(plate_settings):
    """A scratch process file for whole-plate keys, on top of the stock process."""
    return json.dumps({"type": "process", "name": "simulate-first-layer scratch", "from": "User",
                       "inherits": PROCESS, **{k: str(x) for k, x in plate_settings.items()}},
                      indent=2) + "\n"


def compose(recipe, out, name, preset=None, plate_type="hot_plate"):
    """Slice a recipe with `bambu slice compose`, locally; the 3mf, or None on a failure."""
    (out / "logs").mkdir(parents=True, exist_ok=True)
    cmd = [str(bfs.BAMBU), "slice", "compose", str(recipe), "-d", str(out), "-o", f"{name}.3mf",
           "--no-record", "--plate-type", plate_type]
    if preset:
        cmd[4:4] = ["-s", f"{MACHINE};{preset}"]
    t0 = time.time()
    bfs.log("slice_start", job=name)
    try:
        with open(out / "logs" / f"{name}.log", "w") as f:
            rc = subprocess.run(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT,
                                timeout=bfs.SLICE_TIMEOUT).returncode
    except subprocess.TimeoutExpired:
        bfs.log("slice_timeout", job=name, secs=bfs.SLICE_TIMEOUT)
        return None
    bfs.log("slice_end", job=name, rc=rc, secs=round(time.time() - t0))
    p = out / f"{name}.3mf"
    return p if rc == 0 and p.exists() else None


def slice_variant(v, out):
    """Slice one variant alone on the bed, cached by what it asks for: the same request is the same
    slice, so the stock piece is sliced once for every round."""
    recipe = recipe_text(v, "SIM")
    preset = process_text(v["plate_settings"]) if v.get("plate_settings") else None
    key = hashlib.sha1((recipe + (preset or "")).encode()).hexdigest()[:12]
    plate = out / "slices" / f"{key}.3mf"
    if plate.exists():
        bfs.log("slice_cached", key=key)
        return plate
    (out / "slices").mkdir(parents=True, exist_ok=True)
    (out / "slices" / f"{key}.yaml").write_text(recipe)
    pfile = None
    if preset:
        pfile = out / "slices" / f"{key}.process.json"
        pfile.write_text(preset)
    got = compose(out / "slices" / f"{key}.yaml", out / "slices", key, pfile)
    if not got:
        raise SystemExit(f"simulate: the slice failed; see {out / 'slices/logs' / (key + '.log')}")
    missing = plate_settings_missing(got, v.get("plate_settings") or {})
    if missing:
        got.unlink()
        raise SystemExit("simulate: the slice does not hold the plate settings asked for: "
                         + "; ".join(missing))
    return got


def plate_settings_missing(plate, want):
    """Every whole-plate key read back from the slice: a key Studio drops would make the variant
    stock and report no effect, so a mismatch stops the run."""
    if not want:
        return []
    with zipfile.ZipFile(plate) as zf:
        conf = json.loads(zf.read("Metadata/project_settings.config"))
    got = {k: (conf[k][0] if isinstance(conf.get(k), list) else conf.get(k)) for k in want}
    return [f"{k} is {got[k]!r}, asked {str(x)!r}" for k, x in want.items() if str(got[k]) != str(x)]


# ---- one piece's first layer out of a plate ----------------------------------------------------

def only_object(text, label_id):
    """The G-code with every other object's extrusion turned into travel. Comments, layer marks and
    travels stay, so the reader's height, feature, width and position are right when the wanted
    object's moves begin; the skirt, purge line and other pieces print nothing."""
    keep, cur = [], None
    for line in text.splitlines():
        if line.startswith(START):
            cur = line[len(START):].strip()
        elif line.startswith(STOP):
            cur = None
        elif line[:3] in EXTRUDING and cur != label_id:
            code, sep, note = line.partition(";")
            line = re.sub(r"\sE-?[0-9.]+", "", code) + sep + note
        keep.append(line)
    return "\n".join(keep)


def plate_objects(plate):
    """[(label, entry dict, label id)] for every object on a composed plate, from its bed map and
    the slice's own object list. Two objects of one iteration are told apart by where they sit."""
    bedmap = json.loads(Path(str(plate)[:-4] + ".bedmap.json").read_text())
    with zipfile.ZipFile(plate) as zf:
        info = zf.read("Metadata/slice_info.config").decode()
        text = zf.read(next(n for n in zf.namelist() if n.endswith(".gcode"))).decode("utf-8", "replace")
        settings = object_settings(zf.read("Metadata/model_settings.config").decode())
    ids = {}
    for oid, name in re.findall(r'<object identify_id="(\d+)" name="([^"]+)"', info):
        ids.setdefault(name.rsplit(".", 1)[0], []).append(oid)
    out, taken = [], set()
    for o in bedmap["objects"]:
        cands = [i for i in ids.get(o["iteration"], []) if i not in taken]
        if not cands:
            raise SystemExit(f"simulate: {o['label']} ({o['iteration']}) is not in the slice")
        if len(cands) > 1:
            cands.sort(key=lambda i: dist(center(only_object(text, i)), (o["x"], o["y"])))
        taken.add(cands[0])
        out.append((o["label"], {**o, "settings": settings.get(o["iteration"], {})}, cands[0]))
    return out, text


def object_settings(model_settings):
    """{iteration: {key: value}} for the object-level keys of a 3mf's model settings."""
    out = {}
    for body in re.findall(r"<object id=\"\d+\">(.*?)</object>", model_settings, re.S):
        head = body.split("<part", 1)[0]
        kv = dict(re.findall(r'<metadata key="([^"]+)" value="([^"]*)"/>', head))
        if "name" in kv:
            name = kv.pop("name").rsplit(".", 1)[0]
            out[name] = {k: x for k, x in kv.items() if k != "extruder"}
    return out


def center(text):
    _, moves = bfs.first_layer(text)
    cx, cy, _ = bfs.region_of(moves) if moves else (0, 0, 0)
    return cx, cy


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# ---- scoring ----------------------------------------------------------------------------------

def widen(moves, factor):
    """Every bead `factor` times its planned width: the spread model (Theory)."""
    return [(f, w * factor, run) for f, w, run in moves]


def factor_for(spread, flow, lower, h):
    """How many times its planned width each bead is drawn: 1 for `plan`, the spread model else."""
    return 1.0 if spread == "plan" else spread * flow * h / (h - lower)


def spreads_of(text):
    """`plan,1.0,1.1` -> ["plan", 1.0, 1.1]."""
    return [s if s == "plan" else float(s) for s in text.split(",")]


def first_moves(text, label_id=None):
    """The first layer's height and moves, of one object when a label id is given."""
    h, moves = bfs.first_layer(only_object(text, label_id) if label_id else text)
    if not moves:
        raise SystemExit(f"simulate: object {label_id} lays nothing on the first layer")
    return h, moves


def score_at(moves, factor, tag="-"):
    """The check's numbers, and the marked picture, with every bead `factor` times as wide."""
    t0 = time.time()
    bfs.log("score_start", obj=tag, factor=round(factor, 4))
    nums, img, _ = bfs.score(widen(moves, factor))
    bfs.log("score_end", obj=tag, factor=round(factor, 4), slits=nums["slits"],
            share=nums["share_pct"], secs=round(time.time() - t0, 1))
    return nums, img


def score_text(text, label_id, spreads, flow=1.0, lower=0.0, pictures=None):
    """{spread: numbers} for one object's first layer, and its marked pictures by spread when asked."""
    h, moves = first_moves(text, label_id)
    out = {}
    for s in spreads:
        f = factor_for(s, flow, lower, h)
        nums, img = score_at(moves, f, label_id or "-")
        nums.update(spread=s, flow=flow, lower_mm=lower, height=h, factor=round(f, 4))
        out[s] = nums
        if pictures is not None:
            pictures[s] = img
    return out


def flow_of(settings, plate):
    """The first-layer flow ratio a piece prints with: its own, else the plate's, else 1."""
    if "initial_layer_flow_ratio" in settings:
        return float(settings["initial_layer_flow_ratio"])
    with zipfile.ZipFile(plate) as zf:
        conf = json.loads(zf.read("Metadata/project_settings.config"))
    v = conf.get("initial_layer_flow_ratio")
    return float((v[0] if isinstance(v, list) else v) or 1)


def kind(spread, flow, lower):
    """Plan when the beads are drawn as the slicer planned them; Theory once the model widens them."""
    plain = spread == "plan" or (spread == 1 and flow == 1 and lower == 0)
    return "Plan" if plain else "Plan widened by the spread model (Theory)"


def captioned(img, text):
    font = ImageFont.load_default(size=max(18, CAPTION_PX * 2 // 3))
    out = Image.new("RGB", (img.width, img.height + CAPTION_PX), (30, 30, 30))
    out.paste(img, (0, CAPTION_PX))
    ImageDraw.Draw(out).text((12, 8), text, fill=(255, 255, 255), font=font)
    return out


def line(name, n):
    return (f"{name:<22} {n['slits']:>5} slits  {n['share_pct']:>6.3f}% bare  largest "
            f"{n['largest_mm2']:.3f} sq mm  {'passes' if n['pass'] else 'fails'} the 0.6% bar")


def agreement_line(out):
    p = out / "calibrate.json"
    if not p.exists():
        return "Calibration: not run yet here; run `simulate.py calibrate` before trusting a number."
    return json.loads(p.read_text())["line"]


# ---- run --------------------------------------------------------------------------------------

def run(args):
    v = yaml.safe_load(Path(args.variant).read_text()) or {}
    name = v.get("name") or Path(args.variant).stem
    out = Path(args.out)
    dest = out / "runs" / name
    dest.mkdir(parents=True, exist_ok=True)
    bfs.LOG = out / "simulate.log"
    bfs.log("run_start", name=name)
    stock = {k: v[k] for k in ("bkr", "params", "window") if k in v}
    spreads = spreads_of(args.spread)
    lower = float(v.get("lower_mm", 0))
    vflow = float((v.get("object_settings") or {}).get("initial_layer_flow_ratio")
                  or (v.get("plate_settings") or {}).get("initial_layer_flow_ratio") or 1)
    pics_s, pics_v = {}, {}
    sp = slice_variant(stock, out)
    vp = slice_variant(v, out)
    s_nums = score_text(bfs.read_slice(sp)[0], None, spreads, pictures=pics_s)
    v_nums = score_text(bfs.read_slice(vp)[0], None, spreads, vflow, lower, pics_v)
    agree = agreement_line(out)
    result = {"name": name, "spec": v, "calibration": agree,
              "kind": {str(s): kind(s, vflow, lower) for s in spreads},
              "stock_slice": str(sp), "variant_slice": str(vp),
              "stock": {str(s): n for s, n in s_nums.items()},
              "variant": {str(s): n for s, n in v_nums.items()}}
    for s in spreads:
        pic = pr.join_pictures([captioned(pics_s[s], f"stock, spread {s}"),
                                captioned(pics_v[s], f"{name}, spread {s}")])
        pic.save(dest / f"spread-{s}.png")
        result.setdefault("pictures", []).append(str(dest / f"spread-{s}.png"))
    (dest / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(agree)
    for s in spreads:
        print(f"spread {s} ({kind(s, vflow, lower)}):")
        print("  " + line("stock", s_nums[s]))
        print("  " + line(name, v_nums[s]))
        print(f"  difference: {v_nums[s]['share_pct'] - s_nums[s]['share_pct']:+.3f} points of bare "
              f"share, {v_nums[s]['slits'] - s_nums[s]['slits']:+d} slits")
    print("pictures:", ", ".join(result["pictures"]))
    print("result:", dest / "result.json")
    bfs.log("run_end", name=name)


# ---- plate ------------------------------------------------------------------------------------

def plate(args):
    """Every piece on a plate, one row each: a recipe is sliced first; a sliced plate is read as is
    (its `<name>.bedmap.json` beside it names the pieces)."""
    out = Path(args.out)
    bfs.LOG = out / "simulate.log"
    src = Path(args.target).resolve()
    spreads = spreads_of(args.spread)
    if src.suffix == ".3mf":
        p = src
    else:
        p = compose(src, out / "plates", src.stem + ".plate", None, args.plate_type)
        if not p:
            raise SystemExit(f"simulate: the plate did not slice; see {out / 'plates/logs'}")
    objs, text = plate_objects(p)
    rows = []
    for label, o, lid in objs:
        flow = flow_of(o["settings"], p)
        for s, n in score_text(text, lid, spreads, flow, args.lower_mm).items():
            rows.append({"label": label, "turn_deg": o.get("turn_deg", 0), "settings": o["settings"],
                         "kind": kind(s, flow, args.lower_mm), **n})
    (out / "plates").mkdir(parents=True, exist_ok=True)
    dest = out / "plates" / (p.name[:-4] + ".json")
    dest.write_text(json.dumps({"plate": str(p), "rows": rows}, indent=2) + "\n")
    print(agreement_line(out))
    print(f"| Piece | Settings | Turned on the bed | Spread | Slits | Bare share | Largest pocket (sq mm) |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        sets = ", ".join(f"{k} {x}" for k, x in r["settings"].items()) or "stock"
        print(f"| {r['label']} | {sets} | {'yes' if r['turn_deg'] else 'no'} | {r['spread']} | "
              f"{r['slits']} | {r['share_pct']:.2f}% | {r['largest_mm2']:.2f} |")
    print("result:", dest)


# ---- calibrate --------------------------------------------------------------------------------

def main_checkout():
    common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--git-common-dir"],
                            capture_output=True, text=True, timeout=30).stdout.strip()
    return (ROOT / common).resolve().parent if common else ROOT


def find_plate(name, given):
    """A sliced plate by name: in --plates, else this checkout's build/plates, else the main
    checkout's (build/ is gitignored, so a fresh worktree has none)."""
    for base in ([Path(given)] if given else [ROOT / "build/plates", main_checkout() / "build/plates"]):
        p = base / f"{name}.plate.3mf"
        if p.exists():
            return p
    raise SystemExit(f"simulate: no sliced {name}.plate.3mf; slice it (`make plates`) or pass --plates")


def relation(a, b, band):
    """The plan's word for a against b: fewer bare (better), more (worse), or within the band (same)."""
    d = a - b
    return "better" if d < -band else "worse" if d > band else "same"


def agrees(omar, plan):
    return plan != "better" if omar == "not_better" else plan == omar


def shape_digest(moves):
    """The first layer's lines, placed relative to their own middle: two pieces with the same
    digest are drawn the same by the plain plan, wherever they sat on the bed."""
    cx, cy, _ = bfs.region_of(moves)
    flat = [(f, w, tuple((round(x - cx, 2), round(y - cy, 2)) for x, y in run)) for f, w, run in moves]
    return hashlib.sha1(repr(sorted(flat)).encode()).hexdigest()[:12]


def calibrate(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    bfs.LOG = out / "simulate.log"
    spec = yaml.safe_load(Path(args.pairs).read_text())
    band, spreads = float(spec["band_pp"]), spreads_of(args.spread)
    cache_p = out / "calibrate-cache.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    bfs.log("calibrate_start", pairs=len(spec["pairs"]), spreads=args.spread)
    plates, scores, digests = {}, {}, {}
    for key, piece in spec["pieces"].items():
        key = str(key)
        if piece["plate"] not in plates:
            p = find_plate(piece["plate"], args.plates)
            objs, text = plate_objects(p)
            stamp = f"{p.stat().st_size}-{p.stat().st_mtime_ns}"
            plates[piece["plate"]] = ({lab: lid for lab, _, lid in objs}, text, stamp)
        ids, text, stamp = plates[piece["plate"]]
        if piece["label"] not in ids:
            raise SystemExit(f"simulate: {piece['plate']} has no piece labeled {piece['label']}")
        h, moves = first_moves(text, ids[piece["label"]])
        digests[key] = shape_digest(moves)
        flow, lower = float(piece.get("flow", 1)), float(piece.get("lower_mm", 0))
        for s in spreads:
            f = factor_for(s, flow, lower, h)
            ck = f"{piece['plate']}|{stamp}|{piece['label']}|{f:.5f}"
            if ck not in cache:
                cache[ck] = score_at(moves, f, key)[0]
                cache_p.write_text(json.dumps(cache, indent=1) + "\n")
            scores[(key, s)] = cache[ck]
    by_spread, rows = {}, []
    for s in spreads:
        tally = {"plan": [0, 0], "model": [0, 0]}
        for pair in spec["pairs"]:
            a, b = str(pair["a"]), str(pair["b"])
            group = "model" if digests[a] == digests[b] else "plan"
            sa, sb = scores[(a, s)], scores[(b, s)]
            plan = relation(sa["share_pct"], sb["share_pct"], band)
            ok = agrees(pair["omar"], plan)
            tally[group][0] += ok
            tally[group][1] += 1
            rows.append({"spread": s, "a": a, "b": b, "omar": pair["omar"], "words": pair["words"],
                         "plan": plan, "agrees": ok, "seen_by": group,
                         "a_share": sa["share_pct"], "b_share": sb["share_pct"],
                         "a_slits": sa["slits"], "b_slits": sb["slits"]})
        by_spread[s] = tally
    total = {s: t["plan"][0] + t["model"][0] for s, t in by_spread.items()}
    best = max(total.values())
    best_s = [s for s in spreads if total[s] == best]
    m = len(spec["pairs"])
    t1 = by_spread[spreads[0]]
    bar = {k: scores[(str(k), spreads[0])]["pass"] for k in spec["pieces"]}
    first = "the plain plan" if spreads[0] == "plan" else f"spread {spreads[0]} (Theory)"
    line = (f"Calibration ({time.strftime('%Y-%m-%d')}, {m} judged pairs, tie band {band} points of "
            f"bare share): {first} ranks {total[spreads[0]]} of {m} as Omar "
            f"did ({t1['plan'][0]} of {t1['plan'][1]} it can tell apart, {t1['model'][0]} of "
            f"{t1['model'][1]} it draws alike); best spread {', '.join(map(str, best_s))} at {best} of "
            f"{m} (Theory).")
    result = {"line": line, "band_pp": band, "spreads": spreads,
              "by_spread": {str(s): t for s, t in by_spread.items()}, "pairs": rows,
              "passes_bar_plain": bar, "digests": digests}
    (out / "calibrate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(line)
    print()
    print("| Spread | Pairs the plan tells apart | Pairs drawn alike (model only) | All |")
    print("|---|---|---|---|")
    for s, t in by_spread.items():
        print(f"| {s} | {t['plan'][0]} of {t['plan'][1]} | {t['model'][0]} of {t['model'][1]} | "
              f"{total[s]} of {m} |")
    for s in spreads:
        print()
        print(f"Spread {s}:")
        print("| A | B | Omar | His words | Plan | A bare | B bare | A slits | B slits | Agrees | Drawn |")
        print("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in (r for r in rows if r["spread"] == s):
            print(f"| {r['a']} | {r['b']} | {r['omar']} | {r['words']} | {r['plan']} | "
                  f"{r['a_share']:.2f}% | {r['b_share']:.2f}% | {r['a_slits']} | {r['b_slits']} | "
                  f"{'yes' if r['agrees'] else 'no'} | {'apart' if r['seen_by'] == 'plan' else 'alike'} |")
    passing = [k for k, ok in bar.items() if ok]
    print()
    print(f"The 0.6% bar, {first}: {len(passing)} of {len(bar)} judged pieces pass it "
          f"({', '.join(map(str, passing)) or 'none'}); every one of them still slit in print.")
    bfs.log("calibrate_end", best=best, of=m)


# ---- self-test --------------------------------------------------------------------------------

def self_test():
    # Two objects on one layer: object 1 a square of walls with fill lines 0.6 mm apart at 0.5 mm
    # wide (a 0.1 mm gap between each two, closed in at both ends by the walls); object 2 the same
    # moved 20 mm right. A travel inside object 2's block sets where its first line starts.
    def square(x0):
        g = ["; FEATURE: Outer wall", "; LINE_WIDTH: 0.5", f"G1 X{x0} Y0 F6000",
             f"G1 X{x0 + 6} Y0 E1", f"G1 X{x0 + 6} Y6 E1", f"G1 X{x0} Y6 E1", f"G1 X{x0} Y0 E1",
             "; FEATURE: Bottom surface", "; LINE_WIDTH: 0.5"]
        for i in range(1, 10):
            g += [f"G1 X{x0 + 0.25} Y{0.0 + i * 0.6:.2f}", f"G1 X{x0 + 5.75} Y{i * 0.6:.2f} E1"]
        return g
    text = "\n".join(["; Z_HEIGHT: 0.2", "G1 X-5 Y-5 E2", f"{START} 7", *square(0), f"{STOP} 7",
                      f"{START} 9", *square(20), f"{STOP} 9", "; Z_HEIGHT: 0.4", f"{START} 7",
                      *square(0), f"{STOP} 7"])
    h, one = first_moves(text, "7")
    _, two = first_moves(text, "9")
    _, both = first_moves(text)
    xs = [x for _, _, run in one for x, _ in run]
    n10, _ = score_at(one, 1.0)
    n12, _ = score_at(one, factor_for(1.2, 1.0, 0.0, h))
    n_flow, _ = score_at(one, factor_for(1.0, 1.1, 0.0, h))
    n_low, _ = score_at(one, factor_for(1.0, 1.0, 0.02, h))
    v = {"object_settings": {"infill_wall_overlap": "55%"}, "params": {"strap": 3.7}}
    r = recipe_text(v, "SIM")
    with tempfile.TemporaryDirectory() as tmp:
        ms = ('<config><object id="2"><metadata key="name" value="it-aaa.stl"/>'
              '<metadata key="extruder" value="1"/><metadata key="initial_layer_flow_ratio" value="1.1"/>'
              '<part id="1"><metadata key="name" value="it-aaa.stl"/></part></object>'
              '<object id="4"><metadata key="name" value="it-bbb.stl"/><part id="3"/></object></config>')
        sets = object_settings(ms)
        fake = Path(tmp) / "x.plate.3mf"
        info = ('<object identify_id="7" name="it-aaa.stl" skipped="false" />'
                '<object identify_id="9" name="it-aaa.stl" skipped="false" />')
        with zipfile.ZipFile(fake, "w") as zf:
            zf.writestr("Metadata/slice_info.config", info)
            zf.writestr("Metadata/plate_1.gcode", text)
            zf.writestr("Metadata/model_settings.config", ms)
        bedmap = {"objects": [{"label": "RIGHT", "iteration": "it-aaa", "x": 23, "y": 3},
                              {"label": "LEFT", "iteration": "it-aaa", "x": 3, "y": 3}]}
        (Path(tmp) / "x.plate.bedmap.json").write_text(json.dumps(bedmap))
        objs, _ = plate_objects(fake)
    placed = {lab: lid for lab, _, lid in objs}
    return [
        ("simulate: one object's moves are kept and the other's dropped, the skirt too",
         all(-0.5 < x < 6.5 for x in xs) and len(one) == 10 and len(two) == 10 and len(both) == 21),
        ("simulate: the kept object's first line starts where its own travel left the head",
         min(x for _, _, run in two for x, _ in run) >= 20),
        ("simulate: the lowest layer is the one read", h == 0.2),
        ("simulate: fill 0.1 mm apart leaves slits in the plan", n10["slits"] >= 8 and not n10["pass"]),
        ("simulate: drawn 1.2 times as wide the same fill closes", n12["slits"] == 0),
        ("simulate: more first-layer flow and a lower nozzle each widen the beads",
         n_flow["slits"] < n10["slits"] and n_low["slits"] < n10["slits"]),
        ("simulate: the spread factor keeps volume: 1.1 flow is 1.1, 0.02 mm lower at 0.2 is 1.111",
         abs(factor_for(1, 1.1, 0, 0.2) - 1.1) < 1e-9 and abs(factor_for(1, 1, 0.02, 0.2) - 0.2 / 0.18) < 1e-9),
        ("simulate: a variant's recipe is a scratch slice with its settings and params",
         'no_id:  "scratch slice, not printed"' in r and 'infill_wall_overlap: "55%"' in r
         and "strap: 3.7" in r and "size: 112.5" in r),
        ("simulate: a piece's own settings are read from the 3mf, the extruder left out",
         sets == {"it-aaa": {"initial_layer_flow_ratio": "1.1"}, "it-bbb": {}}),
        ("simulate: two pieces of one iteration are told apart by where they sit",
         placed == {"RIGHT": "9", "LEFT": "7"}),
        ("simulate: the tie band makes a small difference the same, a large one better or worse",
         relation(0.70, 0.75, 0.13) == "same" and relation(0.33, 0.71, 0.13) == "better"
         and relation(0.71, 0.33, 0.13) == "worse"),
        ("simulate: 'not better' agrees with same or worse, never with better",
         agrees("not_better", "same") and agrees("not_better", "worse")
         and not agrees("not_better", "better") and agrees("same", "same")),
        ("simulate: the same lines placed elsewhere are drawn alike",
         shape_digest(one) == shape_digest(two)),
        ("simulate: Plan only when nothing widens the beads",
         kind(1.0, 1, 0) == "Plan" and "Theory" in kind(1.1, 1, 0) and "Theory" in kind(1.0, 1.05, 0)
         and kind("plan", 1.1, 0.02) == "Plan" and factor_for("plan", 1.1, 0.02, 0.2) == 1.0
         and spreads_of("plan,1.1") == ["plan", 1.1]),
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("run", "plate", "calibrate"))
    ap.add_argument("target", nargs="?", help="run: a variant file; plate: a recipe or a sliced plate")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--spread", default=None, help=f"plan (as planned) and bead width factors, Theory "
                    f"(default {SPREADS}; plate: plan)")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--pairs", default=str(PAIRS))
    ap.add_argument("--plates", default=None, help="where the judged plates' slices are")
    ap.add_argument("--plate-type", default="hot_plate")
    ap.add_argument("--lower-mm", type=float, default=0.0, help="plate: a nozzle this much closer (Theory)")
    args = ap.parse_args()
    if args.self_test:
        checks = self_test()
        for name, ok in checks:
            print("PASS" if ok else "FAIL", name)
        sys.exit(0 if all(ok for _, ok in checks) else 1)
    args.spread = args.spread or ("plan" if args.cmd == "plate" else SPREADS)
    if args.cmd in ("run", "plate") and not args.target:
        ap.error(f"{args.cmd} needs a file")
    if args.cmd == "run":
        args.variant = args.target
        run(args)
    elif args.cmd == "plate":
        plate(args)
    elif args.cmd == "calibrate":
        calibrate(args)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
