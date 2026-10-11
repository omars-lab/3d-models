#!/usr/bin/env python3
"""Bed-face sweep: slice a few pieces at every X2D nozzle, stock preset against the house preset,
and score each first layer with the bed-face check (docs/design/printing/bed-face-slicing-design.md
§6). It is the slicer's plan that is scored, not a print.

    tools/bed_face_sweep.py run  [--out build/bed-face-sweep] [--nozzles 0.2,0.4,0.6,0.8]
                                 [--shapes star-2,...] [--presets stock,house] [--force | --rescore]
    tools/bed_face_sweep.py page  [--out build/bed-face-sweep]
    tools/bed_face_sweep.py table [--out build/bed-face-sweep]
    tools/bed_face_sweep.py --self-test

`run` writes one scratch recipe per piece (each `no_id`, never printed), slices it through
`bambu slice compose` with the nozzle's stock machine, process and filament presets, and for the
house preset adds the per-nozzle process from `house_preset` (the checked-in
tools/bambu/presets/bed-face-0.20.json at 0.4). It draws the lowest layer with print_review's
`paths` drawing, marks the slits white, and keeps the numbers in results.json; a job already in
results.json is skipped unless --force (slice again) or --rescore (score the kept slices again).
Every step logs an `ev=` line to sweep.log. `page` writes index.html beside the pictures: pick the
nozzle, piece and preset, see the drawing and the numbers. `table` prints the results as Markdown.
"""
import argparse
import datetime
import html
import json
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import print_review as pr  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BAMBU = ROOT / "tools/bambu/bin/bambu"
HOUSE_04 = ROOT / "tools/bambu/presets/bed-face-0.20.json"
PROFILES = Path("/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/process")
SLICE_TIMEOUT = 900   # s, one slice
MARGIN = 2.0          # mm around the first layer's moves
CLOSE_SIDE = 6.0      # mm, the close-up's side
CLOSE_PX = 600        # px, the close-up's side (100 px a millimeter)
WHOLE_PX = 900        # px, the long side of the whole-piece picture on the page
ISLAND_MM2 = 1.0      # sq mm, the least printed patch counted as a piece of its own (not a speck)
SLIT_MARK = (255, 255, 255)
WIDE_MARK = (60, 230, 90)

# the X2D's own presets per nozzle: machine, process, filament (PLA Basic)
NOZZLES = {
    "0.2": ("Bambu Lab X2D 0.2 nozzle", "0.10mm Standard @BBL X2D 0.2 nozzle",
            "Bambu PLA Basic @BBL X2D 0.2 nozzle"),
    "0.4": ("Bambu Lab X2D 0.4 nozzle", "0.20mm Standard @BBL X2D",
            "Bambu PLA Basic @BBL X2D 0.4 nozzle"),
    "0.6": ("Bambu Lab X2D 0.6 nozzle", "0.30mm Standard @BBL X2D 0.6 nozzle",
            "Bambu PLA Basic @BBL X2D 0.6 nozzle"),
    "0.8": ("Bambu Lab X2D 0.8 nozzle", "0.40mm Standard @BBL X2D 0.8 nozzle",
            "Bambu PLA Basic @BBL X2D 0.8 nozzle"),
}
STAR = "bikar:patterns/Constructions/7apC5Q9QS-8-minimal-coaster.bkr"
RADIAL = "bikar:patterns/Constructions/GimTvN9hw4U-radial-coaster.bkr"
GBV = "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
# the pieces: the star at three strap widths, the radial, and a row of gBV small kites at three
# coaster sizes (the kite grows with the coaster; the strap follows the size, capped at 4)
SHAPES = {
    "star-2": dict(bkr=STAR, label="STAR", params=dict(size=90, strap=2, height=4, round=1),
                   title="Star coaster, 90 mm, strap 2"),
    "star-3": dict(bkr=STAR, label="STAR", params=dict(size=90, strap=3, height=4, round=1),
                   title="Star coaster, 90 mm, strap 3"),
    "star-4": dict(bkr=STAR, label="STAR", params=dict(size=90, strap=4, height=4, round=1),
                   title="Star coaster, 90 mm, strap 4"),
    "radial-3": dict(bkr=RADIAL, label="RADIAL", params=dict(size=90, strap=3, height=4, round=1),
                     title="Radial coaster, 90 mm, strap 3"),
    "kite-90": dict(bkr=GBV, piece="Kite", label="KITE",
                    params=dict(size=90, strap=3, height=4.4, gap=0.05),
                    title="gBV small kites, 90 mm coaster, strap 3"),
    "kite-112": dict(bkr=GBV, piece="Kite", label="KITE",
                     params=dict(size=112.5, strap=3.75, height=4.4, gap=0.05),
                     title="gBV small kites, 112.5 mm coaster, strap 3.75"),
    "kite-125": dict(bkr=GBV, piece="Kite", label="KITE",
                     params=dict(size=125, strap=4, height=4.4, gap=0.05),
                     title="gBV small kites, 125 mm coaster, strap 4"),
}
PRESETS = ("stock", "house")
CONFIG_KEYS = ("print_settings_id", "layer_height", "initial_layer_print_height", "line_width",
               "initial_layer_line_width", "bottom_surface_pattern", "infill_wall_overlap",
               "nozzle_diameter")

LOG = None


def log(ev, msg=None, **kv):
    """One greppable line: UTC time, pid, ev=<event>, key=value, an optional quoted msg."""
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    parts = [now, f"pid={os.getpid()}", f"ev={ev}"]
    parts += [f"{k}={str(v).replace(' ', '_')}" for k, v in kv.items()]
    if msg:
        parts.append(f'msg="{msg}"')
    line = " ".join(parts)
    print(line, flush=True)
    if LOG:
        with open(LOG, "a") as f:
            f.write(line + "\n")


# ---- presets ----------------------------------------------------------------------------------

def stock_value(process, key, profiles=PROFILES):
    """A process preset's value for key, following its `inherits` chain through Studio's files."""
    name = process
    while name:
        data = json.loads((profiles / f"{name}.json").read_text())
        if key in data:
            v = data[key]
            return v[0] if isinstance(v, list) else v
        name = data.get("inherits")
    raise KeyError(f"{key} not set anywhere up the chain from {process}")


def house_preset(nozzle, profiles=PROFILES):
    """The house bed-face preset for a nozzle: concentric first layer, 30% overlap, and the first
    line as wide as the preset's ordinary line, on top of the nozzle's stock process."""
    machine, process, _ = NOZZLES[nozzle]
    return {"type": "process", "name": f"Naqsh bed face sweep {nozzle} nozzle", "from": "User",
            "inherits": process, "bottom_surface_pattern": "concentric",
            "infill_wall_overlap": "30%",
            "initial_layer_line_width": stock_value(process, "line_width", profiles)}


def preset_path(out, nozzle):
    """The house preset file for a nozzle: the checked-in one at 0.4, a written one otherwise."""
    if nozzle == "0.4":
        return HOUSE_04
    p = out / "presets" / f"bed-face-{nozzle}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(house_preset(nozzle), indent=2) + "\n")
    return p


# ---- slicing ----------------------------------------------------------------------------------

def recipe_text(shape, nozzle):
    s, (machine, process, filament) = SHAPES[shape], NOZZLES[nozzle]
    params = ", ".join(f"{k}: {v}" for k, v in s["params"].items())
    lines = [f"# scratch: bed-face sweep, {shape} at the {nozzle} nozzle", "bed: x2d", "profile:",
             f'  settings: "{machine};{process}"', f'  filament: "{filament}"', "", "items:",
             f"  - bkr:    {s['bkr']}"]
    if "piece" in s:
        lines.append(f"    piece:  {s['piece']}")
    lines += [f"    params: {{ {params} }}", f"    label:  {s['label']}",
              '    no_id:  "scratch slice, not printed"', ""]
    return "\n".join(lines)


def slice_one(out, shape, nozzle, preset):
    """Slice one job; the 3mf path, or None when the slicer failed or timed out."""
    job = f"{shape}-n{nozzle}-{preset}"
    recipe = out / "recipes" / f"{shape}-n{nozzle}.yaml"
    recipe.parent.mkdir(parents=True, exist_ok=True)
    recipe.write_text(recipe_text(shape, nozzle))
    cmd = [str(BAMBU), "slice", "compose", str(recipe), "-d", str(out / "slices"), "-o",
           f"{job}.3mf", "--no-record", "--plate-type", "hot_plate"]
    if preset == "house":
        cmd[4:4] = ["-s", f"{NOZZLES[nozzle][0]};{preset_path(out, nozzle)}"]
    (out / "logs").mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    log("slice_start", job=job)
    try:
        with open(out / "logs" / f"{job}.log", "w") as f:
            rc = subprocess.run(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT,
                                timeout=SLICE_TIMEOUT).returncode
    except subprocess.TimeoutExpired:
        log("slice_timeout", job=job, secs=SLICE_TIMEOUT)
        return None
    log("slice_end", job=job, rc=rc, secs=round(time.time() - t0))
    p = out / "slices" / f"{job}.3mf"
    return p if rc == 0 and p.exists() else None


# ---- scoring ----------------------------------------------------------------------------------

def read_slice(plate):
    """The G-code, the config keys and the slicer's time and weight from a sliced 3mf."""
    with zipfile.ZipFile(plate) as zf:
        name = next(n for n in zf.namelist() if n.endswith(".gcode"))
        text = zf.read(name).decode("utf-8", "replace")
        conf = json.loads(zf.read("Metadata/project_settings.config"))
        info = zf.read("Metadata/slice_info.config").decode()
    keys = {k: (conf[k][0] if isinstance(conf.get(k), list) else conf.get(k)) for k in CONFIG_KEYS}
    meta = lambda k: info.split(f'key="{k}" value="', 1)[1].split('"', 1)[0] if k in info else None
    return text, keys, {"seconds": int(meta("prediction") or 0), "grams": float(meta("weight") or 0)}


def first_layer(text):
    """The lowest layer's height and moves."""
    heights = [float(ln.split(":")[1]) for ln in text.splitlines() if ln.startswith("; Z_HEIGHT:")]
    if not heights:
        raise SystemExit("bed_face_sweep: the G-code has no '; Z_HEIGHT:' lines")
    return pr.gcode_layer(text, min(heights))


def region_of(moves):
    xs = [x for _, _, run in moves for x, _ in run]
    ys = [y for _, _, run in moves for _, y in run]
    side = max(max(xs) - min(xs), max(ys) - min(ys)) + 2 * MARGIN
    return ((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, side)


def mark_slits(img, k):
    """Paint every slit white and every wide closed-in pocket green; both as (pixels, first
    pixel). A wide pocket is a hole the design cuts or a core no line reached: the check's slit
    rule does not count it, so the sweep weighs it against the 0.4 stock slice of the same piece,
    where the design's holes are the same."""
    bare, slits, wide = pr.slit_pockets(img, k)
    w = img.size[0]
    for found, color in ((slits, SLIT_MARK), (wide, WIDE_MARK)):
        for _, start in found:
            ImageDraw.floodfill(img, (start % w, start // w), color)
    return slits, wide, bare


def islands(bare, w, h, k):
    """How many printed patches of at least ISLAND_MM2 the picture holds: one per piece on the
    bed, whatever its line width, so a piece the slicer drops shows as one fewer."""
    return sum(n / k / k >= ISLAND_MM2 for n, *_ in pr.pockets([not b for b in bare], w, h))


def score(moves, px_per_mm=pr.CHECK_PX_PER_MM):
    """The check's numbers for a first layer, the marked whole-piece picture, and where the
    largest slit is (mm), drawn from below as `paths --below` does."""
    region = region_of(moves)
    cx, cy, side = region
    px = round(side * px_per_mm)
    img, (n, area, largest, printed) = pr.paths_picture(moves, region, below=True, px=px)
    k = px / side
    found, wide, bare = mark_slits(img, k)
    at = None
    if found:
        size, start = max(found)
        at = (round(cx + side / 2 - (start % px) / k, 2), round(cy + side / 2 - (start // px) / k, 2))
    share = 100 * area / (area + printed) if area + printed else 0
    nums = {"slits": n, "bare_mm2": round(area, 3), "printed_mm2": round(printed, 1),
            "share_pct": round(share, 3), "largest_mm2": round(largest, 3),
            "pass": pr.bed_face_ok(area, largest, printed), "largest_at": at,
            "wide_mm2": round(sum(n for n, _ in wide) / k / k, 3), "wide_n": len(wide),
            "islands": islands(bare, px, px, k)}
    return nums, img, region


def close_up(moves, at):
    region = (at[0], at[1], CLOSE_SIDE)
    img, _ = pr.paths_picture(moves, region, below=True, px=CLOSE_PX)
    mark_slits(img, CLOSE_PX / CLOSE_SIDE)
    return img


def score_job(out, job, plate):
    t0 = time.time()
    log("score_start", job=job)
    text, keys, info = read_slice(plate)
    z, moves = first_layer(text)
    nums, img, region = score(moves)
    img_dir = out / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = img.getbbox()   # the piece, without the square's empty bed
    pad = round(MARGIN * pr.CHECK_PX_PER_MM / 2)
    img = img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.size[0], x1 + pad),
                    min(img.size[1], y1 + pad)))
    scale = WHOLE_PX / max(img.size)
    img.resize((round(img.size[0] * scale), round(img.size[1] * scale)), Image.LANCZOS).save(
        img_dir / f"{job}.png")
    if nums["largest_at"]:
        close_up(moves, nums["largest_at"]).save(img_dir / f"{job}-close.png")
    log("score_end", job=job, share=nums["share_pct"], largest=nums["largest_mm2"],
        check="PASS" if nums["pass"] else "FAIL", secs=round(time.time() - t0))
    return {**nums, "z": z, "region": [round(v, 2) for v in region], "config": keys, **info,
            "whole": f"img/{job}.png", "close": f"img/{job}-close.png" if nums["largest_at"] else None}


# ---- the sweep --------------------------------------------------------------------------------

def load_results(out):
    p = out / "results.json"
    return json.loads(p.read_text()) if p.exists() else {"jobs": {}}


def save_results(out, results):
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")


def annotate(results):
    """Each job against the 0.4 stock slice of the same piece, where the design's holes are the
    same: its count of printed islands (one fewer is a piece the slicer dropped) and of wide
    closed-in pockets (one more is a core no line reached, or a slit grown past slit width).
    Counts, not areas: the printed and wide areas follow the first line's width, since every edge
    moves with it, so they change on every nozzle whether or not anything went missing; they are
    kept as context. Then the best job per piece and nozzle and per piece: passing, nothing lost
    or new, the least share; on a tie (the house changes leaving the slice as it was), stock."""
    jobs = results["jobs"]
    for job, r in jobs.items():
        ref = jobs.get(f"{r['shape']}-n0.4-stock")
        # a record scored by an older version lacks the newer fields until it is scored again
        both = lambda k: ref is not None and k in r and k in ref
        r["printed_vs_04_stock"] = round(r["printed_mm2"] / ref["printed_mm2"], 3) if ref else None
        r["wide_vs_04_stock"] = round(r["wide_mm2"] - ref["wide_mm2"], 3) if both("wide_mm2") else None
        r["wide_new"] = r["wide_n"] - ref["wide_n"] if both("wide_n") else None
        r["islands_lost"] = ref["islands"] - r["islands"] if both("islands") else None
        r["lost"] = bool(r["islands_lost"] and r["islands_lost"] > 0)
        r["core"] = bool(r["wide_new"] and r["wide_new"] > 0)
    rank = lambda r: (not r["pass"], r["lost"] or r["core"], r["share_pct"], r["largest_mm2"],
                      PRESETS.index(r["preset"]) if r.get("preset") in PRESETS else 0)
    best = {}
    for job, r in jobs.items():
        for key in (r["shape"], f"{r['shape']}-n{r['nozzle']}"):
            if key not in best or rank(r) < rank(jobs[best[key]]):
                best[key] = job
    results["best"] = best
    return results


def run(args):
    global LOG
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    LOG = out / "sweep.log"
    results = load_results(out)
    todo = [(s, n, p) for s in args.shapes for n in args.nozzles for p in args.presets]
    log("sweep_start", jobs=len(todo), out=out)
    t0 = time.time()
    for i, (shape, nozzle, preset) in enumerate(todo, 1):
        job = f"{shape}-n{nozzle}-{preset}"
        if job in results["jobs"] and not (args.force or args.rescore):
            log("job_skip", job=job, n=i)
            continue
        log("job_start", job=job, n=i, of=len(todo))
        plate = out / "slices" / f"{job}.3mf"
        if not (args.rescore and plate.exists()):
            plate = slice_one(out, shape, nozzle, preset)
        if plate is None:
            log("job_fail", job=job, msg=f"see logs/{job}.log")
            continue
        r = score_job(out, job, plate)
        results["jobs"][job] = {"shape": shape, "nozzle": nozzle, "preset": preset,
                                "params": SHAPES[shape]["params"], **r}
        save_results(out, annotate(results))
        log("job_end", job=job, n=i, elapsed_min=round((time.time() - t0) / 60, 1))
    save_results(out, annotate(results))
    log("sweep_end", jobs=len(results["jobs"]), minutes=round((time.time() - t0) / 60, 1))
    for key, job in sorted(results["best"].items()):
        r = results["jobs"][job]
        print(f"best {key:16} {job:28} share {r['share_pct']:.2f}%  largest {r['largest_mm2']:.3f}"
              f"  {'PASS' if r['pass'] else 'FAIL'}{'  LOST' if r['lost'] else ''}"
              f"{'  CORE' if r['core'] else ''}")


# ---- self-test --------------------------------------------------------------------------------

def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        prof = Path(tmp)
        (prof / "base.json").write_text(json.dumps({"line_width": "0.42"}))
        (prof / "0.20mm Standard @BBL X2D.json").write_text(json.dumps({"inherits": "base"}))
        (prof / "0.40mm Standard @BBL X2D 0.8 nozzle.json").write_text(
            json.dumps({"line_width": ["0.82"], "inherits": "base"}))
        h04, h08 = house_preset("0.4", prof), house_preset("0.8", prof)
        kept = json.loads(HOUSE_04.read_text())
        same = all(h04[k] == kept[k] for k in ("inherits", "bottom_surface_pattern",
                                               "infill_wall_overlap", "initial_layer_line_width"))
        # a full fill and a fill stopped short of the wall, on two layers; the lowest is scored
        def layer(z, end):
            g = [f"; Z_HEIGHT: {z}", "; FEATURE: Outer wall", "; LINE_WIDTH: 0.4", "G1 X0 Y0",
                 "G1 X10 Y0 E1", "G1 X10 Y10 E1", "G1 X0 Y10 E1", "G1 X0 Y0 E1",
                 "; FEATURE: Bottom surface", "; LINE_WIDTH: 0.42"]
            for i in range(1, 25):
                g += [f"G1 X{0.2 + end} Y{i * 0.4}", f"G1 X{9.8 - end} Y{i * 0.4} E1"]
            return g
        good = "\n".join(layer(0.3, 0.0) + layer(0.6, 0.4))
        bad = "\n".join(layer(0.3, 0.4) + layer(0.6, 0.0))
        zg, mg = first_layer(good)
        zb, mb = first_layer(bad)
        ng, _, rg = score(mg)
        nb, imgb, _ = score(mb)
        white = imgb.convert("L").histogram()[255]
        nw, imgw, _ = score([m for m in mg if m[0] == "Outer wall"])   # a wall with nothing in it
        green = imgw.getpixel((imgw.size[0] // 2, imgw.size[1] // 2)) == WIDE_MARK
        recipe = recipe_text("kite-112", "0.6")
        two = score([m for m in mg if m[0] == "Outer wall"]
                    + [("Outer wall", w, [(x + 20, y) for x, y in run])
                       for f, w, run in mg if f == "Outer wall"])[0]
        jobs = {"jobs": {j: dict(shape="a", nozzle=j[3:6], preset=j[7:]) for j in (
            "a-n0.4-stock", "a-n0.6-stock", "a-n0.6-house", "a-n0.8-stock", "a-n0.8-house",
            "a-n0.2-stock", "a-n0.2-house")}}
        # (pass, share, printed, wide area, wide pockets, islands): 0.6 stock prints less, as a
        # narrower line does, but every piece; 0.6 house drops one. 0.2 stock has more wide area,
        # as a narrower line gives every hole, but no new pocket; 0.2 house has one pocket more.
        # 0.8 house is 0.8 stock again.
        for (job, r), (ok, share, printed, wide, n, isl) in zip(jobs["jobs"].items(), (
                (False, 0.1, 100, 50, 5, 5), (True, 0.4, 80, 50, 5, 5), (True, 0.05, 99, 50, 5, 4),
                (False, 0.01, 100, 50, 5, 5), (False, 0.01, 100, 50, 5, 5),
                (True, 0.3, 100, 90, 5, 5), (True, 0.02, 100, 51, 6, 5))):
            r.update({"pass": ok, "share_pct": share, "printed_mm2": printed, "largest_mm2": 0.1,
                      "wide_mm2": wide, "wide_n": n, "islands": isl})
        best = annotate(jobs)["best"]
        return [
            ("sweep: the 0.4 house preset made here matches the checked-in one", same),
            ("sweep: a nozzle's house first line is its stock line width, read up the chain",
             h08["initial_layer_line_width"] == "0.82" and h08["inherits"].endswith("0.8 nozzle")),
            ("sweep: the lowest layer is the one scored", zg == 0.3 and zb == 0.3),
            ("sweep: a fill that reaches the wall passes", ng["pass"] and ng["slits"] == 0
             and ng["largest_at"] is None),
            ("sweep: a fill stopped short of the wall fails, with its slits painted white",
             not nb["pass"] and nb["slits"] >= 2 and white > 0),
            ("sweep: a wide bare middle is no slit, but is counted wide and painted green",
             nw["pass"] and nw["slits"] == 0 and abs(nw["wide_mm2"] - 9.6 ** 2) < 3 and green),
            ("sweep: the largest slit is placed inside the square",
             nb["largest_at"] is not None and all(-0.5 < v < 10.5 for v in nb["largest_at"])),
            ("sweep: the drawn region is the moves' center lines plus the margin",
             abs(rg[2] - (10 + 2 * MARGIN)) < 1e-6 and rg[:2] == (5, 5)),
            ("sweep: a scratch recipe names its piece and nozzle and is never printed",
             "piece:  Kite" in recipe and "X2D 0.6 nozzle;0.30mm" in recipe and "no_id:" in recipe),
            ("sweep: the best is a passing job with nothing lost, not a failing one with less bare",
             best["a"] in ("a-n0.6-stock", "a-n0.2-stock") and best["a-n0.8"] == "a-n0.8-stock"),
            ("sweep: a wide pocket the 0.4 stock slice lacks is a core and not the best; more wide "
             "area alone is not",
             jobs["jobs"]["a-n0.2-house"]["core"] and not jobs["jobs"]["a-n0.2-stock"]["core"]
             and best["a-n0.2"] == "a-n0.2-stock"),
            ("sweep: one printed island is counted per piece, a wall with a bare middle included",
             ng["islands"] == 1 and nw["islands"] == 1 and two["islands"] == 2),
            ("sweep: a job with an island fewer than 0.4 stock is lost; less printed area alone is not",
             jobs["jobs"]["a-n0.6-house"]["lost"] and not jobs["jobs"]["a-n0.6-stock"]["lost"]),
            ("sweep: when house leaves the slice as stock had it, stock is named the best",
             best["a-n0.8"] == "a-n0.8-stock"),
        ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("run", "page", "table"))
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "build/bed-face-sweep"))
    ap.add_argument("--nozzles", default=",".join(NOZZLES))
    ap.add_argument("--shapes", default=",".join(SHAPES))
    ap.add_argument("--presets", default=",".join(PRESETS))
    ap.add_argument("--force", action="store_true", help="slice and score again")
    ap.add_argument("--rescore", action="store_true", help="score again, slicing only what is missing")
    args = ap.parse_args()
    if args.self_test:
        checks = self_test()
        for name, ok in checks:
            print("PASS" if ok else "FAIL", name)
        sys.exit(0 if all(ok for _, ok in checks) else 1)
    args.nozzles, args.shapes = args.nozzles.split(","), args.shapes.split(",")
    args.presets = args.presets.split(",")
    for v, known in ((args.nozzles, NOZZLES), (args.shapes, SHAPES), (args.presets, PRESETS)):
        bad = [x for x in v if x not in known]
        if bad:
            raise SystemExit(f"unknown {bad}; known: {', '.join(known)}")
    if args.cmd == "run":
        run(args)
    elif args.cmd == "page":
        page(Path(args.out).resolve())
    elif args.cmd == "table":
        print(table(annotate(load_results(Path(args.out).resolve()))))
    else:
        ap.print_help()


def page(out):
    """index.html beside results.json and img/: pick a piece, nozzle and preset, see the first
    layer drawn from below with its numbers; the best per piece is marked. The page reads the
    results it embeds and the pictures next to it, nothing else."""
    results = annotate(load_results(out))
    data = {"jobs": results["jobs"], "best": results["best"],
            "shapes": {k: {"title": v["title"], "params": v["params"]} for k, v in SHAPES.items()},
            "nozzles": {n: NOZZLES[n][1] for n in NOZZLES},
            "bars": {"share": pr.CHECK_MAX_SHARE, "pocket": pr.CHECK_MAX_POCKET,
                     "island": ISLAND_MM2, "slit": pr.SLIT_WIDE},
            "made": datetime.date.today().isoformat()}
    blob = json.dumps(data, sort_keys=True).replace("</", "<\\/")
    text = (Path(__file__).resolve().parent / "bed_face_sweep_page.html").read_text()
    (out / "index.html").write_text(text.replace("/*DATA*/null", blob))
    files = sorted(p.relative_to(out).as_posix() for p in (out / "img").glob("*.png"))
    (out / "files.json").write_text(json.dumps([{"path": f} for f in files]) + "\n")
    log("page", jobs=len(results["jobs"]), pictures=len(files), out=out / "index.html")


def table(results):
    """The results as Markdown, for the research file: every job in sweep order, then the best per
    piece and per piece and nozzle. Printed vs 0.4 stock and new bare are against the same piece's
    0.4 stock slice."""
    jobs = results["jobs"]
    order = {k: i for i, k in enumerate(SHAPES)}
    key = lambda j: (order.get(jobs[j]["shape"], 99), float(jobs[j]["nozzle"]),
                     PRESETS.index(jobs[j]["preset"]))
    rows = ["| Job | First line | Bare share % | Largest pocket mm² | Slits | Pieces | Printed vs 0.4 stock "
            "| Wide bare spots (new) | Check | Slicer time min | Grams |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for j in sorted(jobs, key=key):
        r = jobs[j]
        flag = "PASS" if r["pass"] else "FAIL"
        flag += " lost" if r["lost"] else ""
        flag += " core" if r["core"] else ""
        rows.append(f"| {j} | {r['config'].get('initial_layer_line_width')} | {r['share_pct']:.3f} "
                    f"| {r['largest_mm2']:.3f} | {r['slits']} | {r.get('islands')} | {r['printed_vs_04_stock']} "
                    f"| {r.get('wide_n')} ({r.get('wide_new')}) | {flag} | {round(r['seconds'] / 60)} | {r['grams']} |")
    rows += ["", "| Best for | Job |", "|---|---|"]
    rows += [f"| {k} | {v} |" for k, v in sorted(results["best"].items(), key=lambda kv: (
        order.get(jobs[kv[1]]["shape"], 99), kv[0]))]
    return "\n".join(rows)


if __name__ == "__main__":
    main()
