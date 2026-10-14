#!/usr/bin/env python3
"""Teach simulate-first-layer how one printer setup lays its first layer: fit the Fitted reading's
few numbers to the pairs of printed pieces Omar judged, hold out one plate at a time to score it,
write the setup's profile, and write a dated prediction for the next plate before it prints.

This is the teach-simulator skill's tool. It scores with simulate-first-layer's own code
(`simulate.py`: the plan's drawing, the spread model, the Fitted line ends); nothing is
re-implemented, and nothing is ever sent to the printer.

The Fitted reading has four numbers, the fewest the photos support (marking-rubric.md says why):

  spread    every bead `spread x flow x h/(h - lower)` times its planned width (the spread model)
  pull_mm   the first this-many mm of every stroke laid thin (the line end pulling back)
  thin      how thin: 1 = not laid at all, 0.5 = half its width
  at_turns  whether a turn sharper than 60 degrees starts the thin stretch again (the head slows)

pull_mm 0 is the spread model alone (one number). Every number is Fitted to Omar's verdicts, not
Measured on a bead.

  fit.py fit --setup <name> [--write] [--pictures DIR]   grid, hold out one plate at a time, profile
  fit.py predict <plate name | plate.3mf> --setup <name> [--write]   the dated Fitted ranking
  fit.py show-setup <plate name | plate.3mf>             a slice's printer, nozzle, plate, filament
  fit.py --self-test
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "tools/print_review.py").exists())
sys.path.insert(0, str(ROOT / ".claude/skills/simulate-first-layer/scripts"))
import simulate as sim  # noqa: E402

bfs, yaml = sim.bfs, sim.yaml
SPREAD = (1.0, 1.05, 1.1)
PULL = (0.0, 0.25, 0.5, 1.0)
THIN = (0.5, 1.0)
TURNS = (False, True)
OUT = ROOT / "build/simulate/teach"


# ---- the grid ---------------------------------------------------------------------------------

def grid(spread=SPREAD, pull=PULL, thin=THIN, turns=TURNS):
    """Every model the fit tries. pull 0 lays no line end, so thin and turns mean nothing there and
    it is tried once per spread."""
    out = []
    for s in spread:
        for L in pull:
            for t in (thin if L else (1.0,)):
                for at in (turns if L else (False,)):
                    out.append({"spread": s, "pull_mm": L, "thin": t, "at_turns": at})
    return out


def free_numbers(m):
    """How many numbers a model sets: the spread alone when no line end is laid; else spread, pull
    and thin, and one more when turns count."""
    return 1 if not m["pull_mm"] else 3 + bool(m["at_turns"])


def simpler(m):
    """The order that breaks a tie between models that agree as often: fewer free numbers, then the
    shorter line end, then the spread nearest 1, then the thinner (1 = not laid) line end."""
    return (free_numbers(m), m["pull_mm"], abs(m["spread"] - 1), -m["thin"], m["spread"])


# ---- scoring ----------------------------------------------------------------------------------

def _score(job):
    moves, model, flow, lower, h = job
    if model is None:
        nums, _, _ = bfs.score(moves)
    else:
        nums, _, _ = bfs.score(sim.fitted(moves, model, flow, lower, h))
    return nums["share_pct"], nums["slits"]


def load_pieces(spec, keys, plates_dir=None):
    """{key: (moves, flow, lower, h, cache stem, plate path)} for the pieces named."""
    plates, out = {}, {}
    for key in keys:
        piece = spec["pieces"][key]
        if piece["plate"] not in plates:
            p = sim.find_plate(piece["plate"], plates_dir)
            objs, text = sim.plate_objects(p)
            plates[piece["plate"]] = (p, {lab: lid for lab, _, lid in objs}, text)
        p, ids, text = plates[piece["plate"]]
        if piece["label"] not in ids:
            raise SystemExit(f"fit: {piece['plate']} has no piece labeled {piece['label']}")
        h, moves = sim.first_moves(text, ids[piece["label"]])
        stem = f"{piece['plate']}|{p.stat().st_size}-{p.stat().st_mtime_ns}|{piece['label']}"
        out[key] = (moves, float(piece.get("flow", 1)), float(piece.get("lower_mm", 0)), h, stem, p)
    return out


def score_all(pieces, models, cache_p, jobs):
    """{(key, model key or 'plan'): share} for every piece at the plain plan and every model,
    cached by plate, label and model so a second fit scores only what is new."""
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    todo = []
    for key, (moves, flow, lower, h, stem, _) in pieces.items():
        for m in [None, *models]:
            ck = f"{stem}|{'plan' if m is None else sim.model_key(m)}"
            if ck not in cache:
                todo.append((ck, (moves, m, flow, lower, h)))
    bfs.log("fit_score_start", todo=len(todo), cached=len(cache), jobs=jobs)
    if todo:
        with cf.ProcessPoolExecutor(max_workers=jobs) as ex:
            futs = {ex.submit(_score, job): ck for ck, job in todo}
            for i, fut in enumerate(cf.as_completed(futs), 1):
                cache[futs[fut]] = fut.result()
                if i % 25 == 0 or i == len(todo):
                    bfs.log("fit_score_progress", done=i, of=len(todo))
                    cache_p.write_text(json.dumps(cache, indent=0) + "\n")
    bfs.log("fit_score_end", scored=len(todo))
    out = {}
    for key, (*_, stem, _) in pieces.items():
        for m in [None, *models]:
            mk = "plan" if m is None else sim.model_key(m)
            out[(key, mk)] = cache[f"{stem}|{mk}"][0]
    return out


# ---- agreement --------------------------------------------------------------------------------

def verdicts(pairs, shares, mk, band):
    """[agrees?] per pair: the reading's word for a against b, against Omar's."""
    return [sim.agrees(p["omar"], sim.relation(shares[(str(p["a"]), mk)], shares[(str(p["b"]), mk)], band))
            for p in pairs]


def tally(pairs, oks):
    """(all, not ties, ties) as [agreed, of]."""
    t = {"all": [0, 0], "not_ties": [0, 0], "ties": [0, 0]}
    for p, ok in zip(pairs, oks):
        for g in ("all", "ties" if sim.is_tie(p) else "not_ties"):
            t[g][0] += ok
            t[g][1] += 1
    return t


def choose(models, pairs, shares, band):
    """The model that ranks the most of these pairs as Omar did; a tie goes to the simpler one."""
    return max(models, key=lambda m: (sum(verdicts(pairs, shares, sim.model_key(m), band)),
                                      tuple(-x for x in simpler(m))))


def folds(pairs, spec):
    """Groups of pairs to hold out together: one plate at a time, with the plates its pairs were
    judged against (bedface-1's coaster was judged against sheets-04g-fit2's, so those two go out
    together). Built by joining plates that share a pair."""
    parent = {}

    def root(x):
        while parent.setdefault(x, x) != x:
            x = parent[x]
        return x
    for p in pairs:
        a, b = (spec["pieces"][p["a"]]["plate"], spec["pieces"][p["b"]]["plate"])
        parent[root(a)] = root(b)
    groups = {}
    for i, p in enumerate(pairs):
        groups.setdefault(root(spec["pieces"][p["a"]]["plate"]), []).append(i)
    return sorted(groups.values(), key=lambda g: (-len(g), g))


def held_out(models, pairs, shares, band, groups):
    """Each fold's pairs scored by the model chosen on every other fold's: (agrees per pair, the
    model each fold chose)."""
    oks, chosen = [None] * len(pairs), []
    for g in groups:
        train = [p for i, p in enumerate(pairs) if i not in g]
        m = choose(models, train, shares, band)
        chosen.append(m)
        test = [pairs[i] for i in g]
        for i, ok in zip(g, verdicts(test, shares, sim.model_key(m), band)):
            oks[i] = ok
    return oks, chosen


def bar_met(t):
    """iterate-first-layer's bar on held-out pairs: more than half of the pairs that are not ties,
    and at least half of the ties."""
    nt, ti = t["not_ties"], t["ties"]
    return nt[0] * 2 > nt[1] and (ti[1] == 0 or ti[0] * 2 >= ti[1])


def frac(t):
    return f"{t[0]} of {t[1]}"


# ---- fit --------------------------------------------------------------------------------------

def setup_pairs(spec, setup):
    """The pairs whose two pieces both printed on this setup, and the pairs across setups that touch
    it (named, never pooled)."""
    tag = lambda k: spec["pieces"][k].get("setup")
    inside = [p for p in spec["pairs"] if tag(p["a"]) == setup and tag(p["b"]) == setup]
    across = [p for p in spec["pairs"] if (tag(p["a"]) == setup) != (tag(p["b"]) == setup)]
    return inside, across


def check_tags(pieces, prof, setup):
    """Every piece tagged with this setup must have been sliced for the setup's printer, nozzle,
    plate type and filament: a wrong tag would pool two setups (K10)."""
    want = {k: str(x) for k, x in prof["match"].items()}
    for key, (*_, p) in pieces.items():
        got = sim.setup_of(p)
        if got != want:
            raise SystemExit(f"fit: piece {key} is tagged {setup} but its slice {p.name} is "
                             f"{', '.join(got.values())}")


def fit(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    bfs.LOG = out / "teach.log"
    spec = yaml.safe_load(Path(args.pairs).read_text())
    band = float(spec["band_pp"])
    prof_p = Path(args.setups) / f"{args.setup}.yaml"
    if not prof_p.exists():
        raise SystemExit(f"fit: no profile {prof_p}; start one from the template in SKILL.md")
    prof = yaml.safe_load(prof_p.read_text())
    pairs, across = setup_pairs(spec, args.setup)
    if not pairs:
        raise SystemExit(f"fit: no judged pair has both pieces on {args.setup}")
    keys = sorted({str(p[k]) for p in pairs for k in ("a", "b")})
    pieces = load_pieces(spec, keys, args.plates)
    check_tags(pieces, prof, args.setup)
    models = grid()
    shares = score_all(pieces, models, out / f"{args.setup}-cache.json", args.jobs)
    groups = folds(pairs, spec)
    best = choose(models, pairs, shares, band)
    bk = sim.model_key(best)
    spread_only = [m for m in models if not m["pull_mm"]]
    best_s = choose(spread_only, pairs, shares, band)
    fit_t = tally(pairs, verdicts(pairs, shares, bk, band))
    plan_t = tally(pairs, verdicts(pairs, shares, "plan", band))
    s_t = tally(pairs, verdicts(pairs, shares, sim.model_key(best_s), band))
    ho, chosen = held_out(models, pairs, shares, band, groups)
    ho_t = tally(pairs, ho)
    ho_s, _ = held_out(spread_only, pairs, shares, band, groups)
    ho_s_t = tally(pairs, ho_s)
    one = [[i] for i in range(len(pairs))]
    ho1, _ = held_out(models, pairs, shares, band, one)
    ho1_t = tally(pairs, ho1)
    ties_n = sum(sim.is_tie(p) for p in pairs)
    near = sorted(models, key=lambda m: (-sum(verdicts(pairs, shares, sim.model_key(m), band)), simpler(m)))
    top = sum(verdicts(pairs, shares, bk, band))
    level = [m for m in models if sum(verdicts(pairs, shares, sim.model_key(m), band)) == top]
    line = (f"held out one plate at a time, Fitted ranks {frac(ho_t['all'])} judged pairs as Omar did "
            f"({frac(ho_t['not_ties'])} not ties, {frac(ho_t['ties'])} ties"
            f"{'; meets' if bar_met(ho_t) else '; does not meet'} the iterate bar); taught on all of them "
            f"it ranks {frac(fit_t['all'])}, the plain plan {frac(plan_t['all'])}. Tie band {band} points, "
            f"carried over from the plan unmeasured.")
    print(f"Setup {args.setup}: {len(pairs)} judged pairs ({ties_n} ties), {len(keys)} pieces, "
          f"{len(models)} models tried; left out across setups: "
          + (", ".join(f"{p['a']}/{p['b']}" for p in across) or "none"))
    print("Folds held out: " + "; ".join(
        "+".join(sorted({spec['pieces'][pairs[i]['a']]['plate'] for i in g}
                        | {spec['pieces'][pairs[i]['b']]['plate'] for i in g})) + f" ({len(g)} pairs)"
        for g in groups))
    print()
    print("| Reading | All pairs | Not ties | Ties | Held out, all | Held out, not ties | Held out, ties |")
    print("|---|---|---|---|---|---|---|")
    for name, t, h in (("the plain plan (Plan)", plan_t, plan_t),
                       (f"spread only, {best_s['spread']} (Theory)", s_t, ho_s_t),
                       (f"Fitted, {bk}", fit_t, ho_t)):
        print(f"| {name} | {frac(t['all'])} | {frac(t['not_ties'])} | {frac(t['ties'])} | "
              f"{frac(h['all'])} | {frac(h['not_ties'])} | {frac(h['ties'])} |")
    print()
    print("The plain plan fits nothing, so its held-out score is its score. One pair held out at a time "
          f"(secondary): Fitted {frac(ho1_t['all'])} ({frac(ho1_t['not_ties'])} not ties, "
          f"{frac(ho1_t['ties'])} ties).")
    print("Each fold's choice: " + "; ".join(sim.model_key(m) for m in chosen))
    print(f"Models level with the pick on all pairs: {len(level)} of {len(models)}")
    print()
    print("| A | B | Omar | Plan A | Plan B | Fitted A | Fitted B | Fitted says | Agrees | Held out agrees |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for i, p in enumerate(pairs):
        a, b = str(p["a"]), str(p["b"])
        fa, fb = shares[(a, bk)], shares[(b, bk)]
        says = sim.relation(fa, fb, band)
        print(f"| {a} | {b} | {p['omar']} | {shares[(a, 'plan')]:.2f}% | {shares[(b, 'plan')]:.2f}% | "
              f"{fa:.2f}% | {fb:.2f}% | {says} | {'yes' if sim.agrees(p['omar'], says) else 'no'} | "
              f"{'yes' if ho[i] else 'no'} |")
    print()
    print("Top models on all pairs: " + "; ".join(
        f"{sim.model_key(m)} {sum(verdicts(pairs, shares, sim.model_key(m), band))}" for m in near[:6]))
    print(line)
    if args.pictures:
        pictures(pieces, best, Path(args.pictures))
    if args.write:
        today = datetime.date.today().isoformat()
        prof.update({
            "can_fit": True,
            "model": {**best, "turn_deg": sim.TURN_DEG},
            "fit": {"date": today, "pairs": [f"{p['a']}/{p['b']}" for p in pairs], "ties": ties_n,
                    "pieces": keys, "plates": sorted({spec['pieces'][k]['plate'] for k in keys}),
                    "left_out_across_setups": [f"{p['a']}/{p['b']}" for p in across],
                    "models_tried": len(models), "models_level_with_pick": len(level),
                    "grid": {"spread": list(SPREAD), "pull_mm": list(PULL), "thin": list(THIN),
                             "at_turns": list(TURNS)},
                    "band_pp": band},
            "agreement": {
                "held_out_by_plate": ho_t, "meets_iterate_bar": bar_met(ho_t),
                "held_out_folds": [sorted({spec['pieces'][pairs[i][k]]['plate'] for i in g for k in ("a", "b")})
                                   for g in groups],
                "fold_choices": [sim.model_key(m) for m in chosen],
                "taught_on_all": fit_t, "held_out_one_pair": ho1_t,
                "plain_plan": plan_t, "spread_only": {"spread": best_s["spread"], "all": s_t, "held_out": ho_s_t}},
            "line": line,
        })
        prof.pop("why", None)  # the reason there was no fit; a fit replaces it
        prof.setdefault("predictions", [])
        prof_p.write_text(profile_text(prof_p.read_text(), prof))
        print(f"wrote {prof_p}")


def profile_text(old, prof):
    """The profile rewritten, its leading comment kept: the comment says what the setup is and why
    it matches as it does, which the fit cannot know."""
    head = []
    for ln in old.splitlines():
        if ln.startswith("#") or not ln.strip():
            head.append(ln)
        else:
            break
    body = yaml.safe_dump(prof, sort_keys=False, allow_unicode=True, width=100)
    return "\n".join(head).rstrip() + "\n\n" + body


def pictures(pieces, model, dest):
    """Each piece drawn by the plain plan and by Fitted, side by side, for looking at where Fitted
    puts the bare bed against where the photos have it."""
    dest.mkdir(parents=True, exist_ok=True)
    for key, (moves, flow, lower, h, _, _) in pieces.items():
        _, a, _ = bfs.score(moves)
        _, b, _ = bfs.score(sim.fitted(moves, model, flow, lower, h))
        sim.pr.join_pictures([sim.captioned(a, f"{key} plan"), sim.captioned(b, f"{key} Fitted")]).save(
            dest / f"{key}.png")
    print(f"pictures: {dest}")


# ---- predict ----------------------------------------------------------------------------------

def carved_ids(name):
    """{label: the id cut into the piece} from the plate's recipe, so a prediction names pieces as
    Omar will see them; empty when the plate has no recipe here."""
    recipe = ROOT / "docs/design/plates" / f"{name}.yaml"
    if not recipe.exists():
        return {}
    return {it["label"]: it["id"] for it in yaml.safe_load(recipe.read_text()).get("items", [])
            if "label" in it and "id" in it}


def plate_path(target, plates_dir):
    p = Path(target)
    return p if p.suffix == ".3mf" else sim.find_plate(target, plates_dir)


def predict(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    bfs.LOG = out / "teach.log"
    prof_p = Path(args.setups) / f"{args.setup}.yaml"
    prof = yaml.safe_load(prof_p.read_text())
    if not (prof.get("can_fit") and prof.get("model")):
        raise SystemExit(f"fit: {args.setup} carries no fit, so it predicts nothing")
    p = plate_path(args.target, args.plates)
    got, want = sim.setup_of(p), {k: str(x) for k, x in prof["match"].items()}
    if got != want:
        raise SystemExit(f"fit: {p.name} is sliced for {', '.join(got.values())}, not {args.setup}")
    model = prof["model"]
    name = p.name.split(".plate")[0]
    ids = carved_ids(name)
    objs, text = sim.plate_objects(p)
    rows = []
    for label, o, lid in objs:
        h, moves = sim.first_moves(text, lid)
        flow = sim.flow_of(o["settings"], p)
        plan, _ = sim.score_at(moves, 1.0, label)
        fit_n, _ = sim.score_at(moves, 1.0, label, sim.fitted(moves, model, flow, 0.0, h))
        rows.append({"label": label, "id": str(ids.get(label, label)), "turned": bool(o.get("turn_deg")),
                     "plan_pct": plan["share_pct"], "fitted_pct": fit_n["share_pct"]})
    rows.sort(key=lambda r: r["fitted_pct"])
    today = datetime.date.today().isoformat()
    print(f"Prediction for {name}, {today}, Fitted with {args.setup} ({sim.model_key(model)}): "
          f"fewest bare first. {prof['line']}")
    print()
    band = float(prof["fit"]["band_pp"])
    print(f"| Rank | Piece | Label | Turned | Fitted bare | Plan bare | Within {band} points of the one above |")
    print("|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        near = i > 1 and r["fitted_pct"] - rows[i - 2]["fitted_pct"] < band
        print(f"| {i} | {r['id']} | {r['label']} | {'yes' if r['turned'] else 'no'} | {r['fitted_pct']:.2f}% | "
              f"{r['plan_pct']:.2f}% | {'yes' if near else ''} |")
    if args.write:
        preds = prof.setdefault("predictions", [])
        if any(x["plate"] == name for x in preds):
            raise SystemExit(f"fit: {args.setup} already holds a prediction for {name}; a prediction is "
                             "written once, before the print, and never rewritten")
        preds.append({"plate": name, "date": today, "model": sim.model_key(model),
                      "order_fewest_bare_first": [r["id"] for r in rows],
                      "fitted_pct": {r["id"]: r["fitted_pct"] for r in rows}})
        prof_p.write_text(profile_text(prof_p.read_text(), prof))
        print(f"wrote the prediction into {prof_p}")


def show_setup(args):
    p = plate_path(args.target, args.plates)
    got = sim.setup_of(p)
    print("match:")
    for k, x in got.items():
        print(f"  {k}: {json.dumps(x)}")
    n, _ = sim.profile_for(got, where=args.setups)
    print(f"# profile matching it now: {n or 'none'}")


# ---- self-test --------------------------------------------------------------------------------

def self_test():
    # A stroke 4 mm along x then a sharp turn up 2 mm, and a separate 1 mm stroke after a travel.
    moves = [("Bottom surface", 0.5, [(0, 0), (4, 0)]), ("Bottom surface", 0.5, [(4, 0), (4, 2)]),
             ("Bottom surface", 0.5, [(10, 0), (11, 0)])]
    plain = sim.line_starts(moves, 0.0, 1.0, False)
    cut = sim.line_starts(moves, 0.5, 1.0, False)
    half = sim.line_starts(moves, 0.5, 0.5, False)
    turns = sim.line_starts(moves, 0.5, 1.0, True)
    length = lambda ms: sum(sim.dist(a, b) for _, _, r in ms for a, b in zip(r, r[1:]))
    widths = sorted({w for _, w, _ in half})
    spec = {"band_pp": 0.13, "pieces": {
        "A": {"plate": "p1", "setup": "s1"}, "B": {"plate": "p1", "setup": "s1"},
        "C": {"plate": "p2", "setup": "s1"}, "D": {"plate": "p3", "setup": "s1"},
        "E": {"plate": "p4", "setup": "s2"}}, "pairs": [
        {"a": "A", "b": "B", "omar": "better"}, {"a": "C", "b": "D", "omar": "same"},
        {"a": "E", "b": "A", "omar": "better"}]}
    inside, across = setup_pairs(spec, "s1")
    groups = folds(inside, spec)
    ms = grid()
    m0 = {"spread": 1.0, "pull_mm": 0.0, "thin": 1.0, "at_turns": False}
    m1 = {"spread": 1.0, "pull_mm": 0.5, "thin": 1.0, "at_turns": False}
    k0, k1 = sim.model_key(m0), sim.model_key(m1)
    # Both models rank A/B as Omar did; only m1 calls C/D the same.
    shares = {("A", k0): 0.5, ("B", k0): 0.9, ("C", k0): 0.5, ("D", k0): 0.9,
              ("A", k1): 0.5, ("B", k1): 0.9, ("C", k1): 0.6, ("D", k1): 0.65}
    tie_pick = choose([m1, m0], inside[:1], shares, 0.13)
    fit_pick = choose([m0, m1], inside, shares, 0.13)
    ho, chosen = held_out([m0, m1], inside, shares, 0.13, groups)
    with tempfile.TemporaryDirectory() as tmp:
        old = "# a setup\n# two lines\n\nsetup: s1\nmatch: {printer_model: X}\n"
        new = profile_text(old, {"setup": "s1", "match": {"printer_model": "X"}, "line": "l"})
        Path(tmp, "s1.yaml").write_text(new)
        back = yaml.safe_load(Path(tmp, "s1.yaml").read_text())
        hit = sim.profile_for({"printer_model": "X"}, where=tmp)
        miss = sim.profile_for({"printer_model": "Y"}, where=tmp)
    note = sim.fitted_note({k: "x" for k in sim.MATCH_KEYS}, None, None)
    return [
        ("fit: no line end leaves every stroke as drawn", plain == moves),
        ("fit: a line end not laid takes pull_mm off the start of each stroke, once per stroke",
         abs(length(cut) - (length(moves) - 2 * 0.5)) < 1e-9),
        ("fit: a stroke runs on across a move that starts where the last ended",
         len(sim.strokes(moves)) == 2),
        ("fit: a half-thin line end keeps its length at half the width", widths == [0.25, 0.5]
         and abs(length(half) - length(moves)) < 1e-9),
        ("fit: a sharp turn starts the line end again when turns count",
         abs(length(turns) - (length(moves) - 3 * 0.5)) < 1e-9),
        ("fit: pull 0 is tried once per spread, the rest at every thin and turn",
         len(ms) == len(SPREAD) * (1 + (len(PULL) - 1) * len(THIN) * len(TURNS))),
        ("fit: fewer free numbers win a tie", tie_pick == m0 and free_numbers(m1) == 3),
        ("fit: the pick is the model that agrees most", fit_pick == m1),
        ("fit: a pair across setups is named, never fit", len(inside) == 2 and len(across) == 1),
        ("fit: plates judged against each other are held out together, others apart",
         len(groups) == 2 and sorted(map(len, groups)) == [1, 1]),
        ("fit: a held-out pair is scored by a model fit without it", len(chosen) == 2 and ho[0] is True),
        ("fit: the bar wants more than half of the pairs that are not ties and half the ties",
         bar_met({"not_ties": [5, 9], "ties": [2, 4]}) and not bar_met({"not_ties": [4, 9], "ties": [4, 4]})
         and not bar_met({"not_ties": [9, 9], "ties": [1, 4]})),
        ("fit: a rewritten profile keeps its leading comment", new.startswith("# a setup\n# two lines")
         and back["line"] == "l"),
        ("fit: a profile is found by its match, and a slice with no match gets none",
         hit[0] == "s1" and miss == (None, None)),
        ("fit: with no profile the plain plan stands, labeled so", "plain plan stands" in note
         and "Plan" in note),
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("fit", "predict", "show-setup"))
    ap.add_argument("target", nargs="?", help="predict, show-setup: a plate name or a sliced .plate.3mf")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--setup", help="the setup profile's name (setups/<name>.yaml)")
    ap.add_argument("--write", action="store_true", help="fit: write the profile; predict: add the prediction")
    ap.add_argument("--pictures", help="fit: draw each piece, plan beside Fitted, into this folder")
    ap.add_argument("--pairs", default=str(sim.PAIRS))
    ap.add_argument("--setups", default=str(sim.SETUPS))
    ap.add_argument("--plates", default=None, help="where the judged plates' slices are")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    args = ap.parse_args()
    if args.self_test:
        checks = self_test()
        for name, ok in checks:
            print("PASS" if ok else "FAIL", name)
        sys.exit(0 if all(ok for _, ok in checks) else 1)
    if args.cmd in ("fit", "predict") and not args.setup:
        ap.error(f"{args.cmd} needs --setup")
    if args.cmd in ("predict", "show-setup") and not args.target:
        ap.error(f"{args.cmd} needs a plate")
    {"fit": fit, "predict": predict, "show-setup": show_setup}.get(args.cmd, lambda _: ap.print_help())(args)


if __name__ == "__main__":
    main()
