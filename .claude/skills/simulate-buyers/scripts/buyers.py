#!/usr/bin/env python3
"""Simulated buyers at a range of prices: the block to fill in, the check that holds it honest, and
the numbers the price page draws from it.

SIMULATED, NOT CUSTOMER RESEARCH. Every verdict and thought is Claude imagining a made-up buyer.

Sweeps live beside the themes they show, in `docs/design/coaster/themes/<id>/buyers.yaml`:

    sweeps:
      - theme: ice-to-navy          # a theme id in themes.yaml
        coloring: d98115ed1b        # themes.py's hash of the theme's colors when it was shown
        shown: "one 112.5 mm coaster: ..."   # what the buyers saw besides the picture
        prices: [4, 6, 8]           # US dollars a coaster, rising
        buyers:
          bargain-hunter:
            4: { verdict: buy, thought: "one line, first person" }
            ...                     # every price, every buyer in ../buyers.md, no others
        overall: "One sentence: where the buyers split, and who holds on longest."

A construction with no buyers.yaml has no sweeps, which is fine: a sweep is made when a theme is
being priced, not for every theme.

Usage:
    buyers.py stub  <id> <theme> [--prices 4,6,8]   print the block to paste into buyers.yaml
    buyers.py check <id> | --all                    every sweep whole, current and in order
    buyers.py curve <id> <theme> [--json]           the buy share at each price, and each buyer's turn
    buyers.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ROOT = SKILL.parent.parent.parent
BUYERS = SKILL / "buyers.md"
# The themes, their hash and the folder layout belong to the color-themes skill; reuse them
# rather than keep a second copy that could drift.
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "color-themes" / "scripts"))
import themes as th  # noqa: E402

DEFAULT_PRICES = [4, 6, 8, 10, 12, 15, 20, 25, 35]
MAX_THOUGHT = 240  # longer than this is a paragraph, not a thought
# How warm each verdict is, for the order rule; too-cheap sits outside it. WEIGHT is what each
# counts for in the buy share: the 0.5 for a maybe is made up (buyers.md says so).
WARMTH = {"buy": 2, "maybe": 1, "walk": 0}
WEIGHT = {"buy": 1.0, "maybe": 0.5, "walk": 0.0, "too-cheap": 0.0}
VERDICTS = list(WEIGHT)


def buyer_ids(path: Path = BUYERS) -> list[str]:
    """The ids in the buyers table, under `## The six buyers` only (the verdict table is backticked too)."""
    ids, inside = [], False
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## The six buyers"
            continue
        m = re.match(r"\|\s*`([a-z0-9-]+)`\s*\|", line) if inside else None
        if m:
            ids.append(m.group(1))
    return ids


def one_line(text) -> bool:
    return isinstance(text, str) and text.strip() != "" and "\n" not in text.strip()


def price_key(cells: dict, p) -> object:
    """A price as the YAML wrote it: 4 and 4.0 and "4" are the same price."""
    for k in cells:
        try:
            if float(k) == float(p):
                return k
        except (TypeError, ValueError):
            continue
    return None


def order_problems(who: str, verdicts: list[tuple[float, str]]) -> list[str]:
    """buyers.md rule 5: one window. A maybe may turn into a buy as the price rises (it felt a bit
    cheap), but once warmth falls it never comes back, a walk is never followed by anything warmer,
    and too-cheap only comes below the buyer's first buy or maybe."""
    out = []
    warm = [(p, v) for p, v in verdicts if v in WARMTH]
    fallen = False
    for (p1, v1), (p2, v2) in zip(warm, warm[1:]):
        if WARMTH[v2] > WARMTH[v1] and (fallen or v1 == "walk"):
            why = ("a walk is never followed by anything warmer; if the lower price felt too cheap, say too-cheap"
                   if v1 == "walk" else "once a buyer cools as the price rises, they do not warm up again")
            out.append(f"{who}: {v1} at ${p1:g} but {v2} at ${p2:g}; {why}")
        if WARMTH[v2] < WARMTH[v1]:
            fallen = True
    first_warm = next((p for p, v in verdicts if v in ("buy", "maybe")), None)
    for p, v in verdicts:
        if v == "too-cheap" and (first_warm is None or p > first_warm):
            out.append(f"{who}: too-cheap at ${p:g} with no buy or maybe above it; too cheap means "
                       f"a higher price would win them")
    return out


def sweep_problems(sweep: dict, theme: dict | None, buyers: list[str]) -> list[str]:
    tid = sweep.get("theme")
    out = []
    if theme is None:
        return [f"a sweep names theme {tid!r}, which themes.yaml does not have"]
    if sweep.get("coloring") != th.theme_hash(theme):
        out.append(f"{tid}: the sweep is for an earlier coloring; show the buyers the new picture and "
                   f"sweep again (coloring is now {th.theme_hash(theme)})")
    if not one_line(sweep.get("shown")):
        out.append(f"{tid}: `shown` must say in one line what the buyers saw")
    prices = sweep.get("prices") or []
    if not prices or not all(isinstance(p, (int, float)) and not isinstance(p, bool) and p > 0 for p in prices):
        out.append(f"{tid}: prices must be a list of positive numbers")
        return out
    if sorted(set(prices)) != list(prices):
        out.append(f"{tid}: prices must rise, each once")
    cells_by = sweep.get("buyers") or {}
    for bid in buyers:
        if bid not in cells_by:
            out.append(f"{tid}: no reactions from {bid}")
    for bid, cells in cells_by.items():
        if bid not in buyers:
            out.append(f"{tid}: {bid} is not a buyer in buyers.md")
            continue
        cells = cells or {}
        verdicts = []
        for p in prices:
            k = price_key(cells, p)
            if k is None:
                out.append(f"{tid}: {bid} has no reaction at ${p:g}")
                continue
            c = cells[k] or {}
            v = c.get("verdict")
            if v not in VERDICTS:
                out.append(f"{tid}: {bid} at ${p:g}: verdict {v!r} is not one of {', '.join(VERDICTS)}")
                continue
            t = c.get("thought")
            if not one_line(t):
                out.append(f"{tid}: {bid} at ${p:g}: the thought must be one line of text")
            elif len(t.strip()) > MAX_THOUGHT:
                out.append(f"{tid}: {bid} at ${p:g}: the thought is {len(t.strip())} characters; keep it "
                           f"to one line of at most {MAX_THOUGHT}")
            verdicts.append((float(p), v))
        extra = [k for k in cells if all(price_key({k: 0}, p) is None for p in prices)]
        for k in extra:
            out.append(f"{tid}: {bid} reacts at {k!r}, which is not in prices")
        out += [f"{tid}: {e}" for e in order_problems(bid, verdicts)]
    if not one_line(sweep.get("overall")):
        out.append(f"{tid}: the overall line must be one line of text")
    return out


def problems(con: dict, data: dict | None, buyers: list[str]) -> list[str]:
    """Everything wrong with one construction's sweeps, as plain sentences."""
    themes = {t["id"]: t for t in con["themes"]}
    out, seen = [], set()
    for s in (data or {}).get("sweeps") or []:
        tid = s.get("theme")
        if tid in seen:
            out.append(f"{tid}: swept twice; keep one sweep per theme")
        seen.add(tid)
        out += sweep_problems(s, themes.get(tid), buyers)
    return out


def load(cid: str, root: Path = th.THEMES_DIR) -> tuple[dict, dict | None]:
    con = th.construction(cid, root)
    path = con["_folder"] / "buyers.yaml"
    return con, (th.load_yaml(path) if path.exists() else None)


def check(cid: str) -> int:
    con, data = load(cid)
    errs = problems(con, data, buyer_ids())
    for e in errs:
        print(f"{cid}: {e}")
    return 1 if errs else 0


def curve(sweep: dict) -> dict:
    """The numbers the page draws: per price, the verdict counts and the buy share; per buyer, the
    highest price they would still buy (or maybe) at, and the price they first walk at."""
    prices = list(sweep["prices"])
    cells_by = sweep["buyers"]
    n = len(cells_by)
    rows = []
    for p in prices:
        counts = {v: 0 for v in VERDICTS}
        for cells in cells_by.values():
            counts[cells[price_key(cells, p)]["verdict"]] += 1
        share = sum(WEIGHT[v] * c for v, c in counts.items()) / n if n else 0.0
        rows.append({"price_each": p, "counts": counts, "share": round(share, 4)})
    turns = {}
    for bid, cells in cells_by.items():
        vs = [(p, cells[price_key(cells, p)]["verdict"]) for p in prices]
        warm = [p for p, v in vs if v in ("buy", "maybe")]
        last_buy = max((p for p, v in vs if v == "buy"), default=None)
        walks = [p for p, v in vs if v == "walk" and warm and p > min(warm)]
        turns[bid] = {"buys_up_to": last_buy, "warm_up_to": max(warm) if warm else None,
                      "walks_from": min(walks) if walks else None,
                      "too_cheap_below": min(warm) if warm and any(v == "too-cheap" for _, v in vs) else None}
    return {"theme": sweep["theme"], "buyers": n, "maybe_weight": WEIGHT["maybe"], "by_price": rows, "turns": turns}


def find_sweep(cid: str, tid: str) -> dict:
    con, data = load(cid)
    errs = problems(con, data, buyer_ids())
    if errs:
        raise SystemExit(f"{cid}: fix the sweeps first (`buyers.py check {cid}`): {errs[0]}")
    for s in (data or {}).get("sweeps") or []:
        if s.get("theme") == tid:
            return s
    raise SystemExit(f"{cid}: no sweep for {tid}; `buyers.py stub {cid} {tid}`")


def stub(cid: str, tid: str, prices: list[float]) -> None:
    con = th.construction(cid)
    theme = next((t for t in con["themes"] if t["id"] == tid), None)
    if theme is None:
        raise SystemExit(f"{cid} has no theme {tid}")
    ps = ", ".join(f"{p:g}" for p in prices)
    lines = [f"  - theme: {tid}", f"    coloring: {th.theme_hash(theme)}", '    shown: ""',
             f"    prices: [{ps}]", "    buyers:"]
    for bid in buyer_ids():
        lines.append(f"      {bid}:")
        for p in prices:
            lines.append(f'        {p:g}: {{ verdict: "", thought: "" }}')
    lines.append('    overall: ""')
    print("\n".join(lines))


def self_test() -> int:
    fails = []

    def expect(cond, what):
        if not cond:
            fails.append(what)

    buyers = buyer_ids()
    expect(len(buyers) == 6, f"buyers.md: expected 6 buyers, read {len(buyers)}")

    theme = {"id": "a", "colors": {"x": "pink", "frame": "black"}}
    con = {"_folder": Path("fx"), "themes": [theme]}
    bs = ["b1", "b2"]

    def good():
        return {"theme": "a", "coloring": th.theme_hash(theme), "shown": "one coaster", "prices": [5, 10, 20],
                "overall": "b2 holds on longest.",
                "buyers": {"b1": {5: {"verdict": "buy", "thought": "cheap enough"},
                                  10: {"verdict": "maybe", "thought": "hmm"},
                                  20: {"verdict": "walk", "thought": "no"}},
                           "b2": {5: {"verdict": "too-cheap", "thought": "is it junk?"},
                                  10: {"verdict": "buy", "thought": "right"},
                                  20: {"verdict": "buy", "thought": "still fine"}}}}

    expect(problems(con, {"sweeps": [good()]}, bs) == [], f"a clean sweep failed: {problems(con, {'sweeps': [good()]}, bs)}")
    expect(problems(con, None, bs) == [], "a construction with no sweeps failed")

    def fails_with(edit, needle, what):
        s = good()
        edit(s)
        errs = problems(con, {"sweeps": [s]}, bs)
        expect(any(needle in e for e in errs), f"{what} was not caught: {errs}")

    fails_with(lambda s: s.update(coloring="0000000000"), "earlier coloring", "a stale coloring")
    fails_with(lambda s: s["buyers"].pop("b2"), "no reactions from b2", "a missing buyer")
    fails_with(lambda s: s["buyers"].update(b3=s["buyers"]["b1"]), "not a buyer", "an unknown buyer")
    fails_with(lambda s: s["buyers"]["b1"].pop(10), "no reaction at $10", "a missing price")
    fails_with(lambda s: s["buyers"]["b1"].update({15: {"verdict": "walk", "thought": "x"}}), "not in prices", "a price not swept")
    fails_with(lambda s: s["buyers"]["b1"][5].update(verdict="love"), "is not one of", "an unknown verdict")
    fails_with(lambda s: s["buyers"]["b1"][5].update(thought="a\nb"), "one line", "a two-line thought")
    fails_with(lambda s: s["buyers"]["b1"][5].update(thought="x" * (MAX_THOUGHT + 1)), "characters", "an over-long thought")
    fails_with(lambda s: s.update(prices=[10, 5, 20]), "must rise", "falling prices")
    fails_with(lambda s: s.update(shown=""), "shown", "an empty shown line")
    fails_with(lambda s: s.update(overall=""), "overall line", "an empty overall line")
    fails_with(lambda s: s.update(theme="zzz"), "does not have", "a sweep of a theme that does not exist")
    # The by-design failures: a buyer who walks at $10 and buys at $20, one who cools and warms
    # again, and one too cheap above a buy. A maybe turning into a buy is allowed (one window).
    fails_with(lambda s: s["buyers"]["b1"].update({10: {"verdict": "walk", "thought": "x"}, 20: {"verdict": "buy", "thought": "y"}}),
               "a walk is never followed", "a buyer warming up after a walk")
    fails_with(lambda s: s["buyers"]["b1"].update({20: {"verdict": "buy", "thought": "y"}}),
               "do not warm up again", "a buyer cooling, then warming again")
    s = good()
    s["buyers"]["b1"] = {5: {"verdict": "maybe", "thought": "a bit cheap"}, 10: {"verdict": "buy", "thought": "right"},
                         20: {"verdict": "walk", "thought": "too much"}}
    expect(problems(con, {"sweeps": [s]}, bs) == [], "a maybe turning into a buy (one window) was refused")
    fails_with(lambda s: s["buyers"]["b2"].update({20: {"verdict": "too-cheap", "thought": "x"}}),
               "too-cheap at $20", "too-cheap above a buy")
    fails_with(lambda s: s["buyers"]["b1"].update({5: {"verdict": "too-cheap", "thought": "x"}, 10: {"verdict": "walk", "thought": "y"}}),
               "no buy or maybe above it", "too-cheap with nothing warm above it")
    s = good()
    errs = problems(con, {"sweeps": [s, good()]}, bs)
    expect(any("swept twice" in e for e in errs), "a theme swept twice was not caught")

    c = curve(good())
    shares = [r["share"] for r in c["by_price"]]
    expect(shares == [0.5, 0.75, 0.5], f"buy share: expected [0.5, 0.75, 0.5], got {shares}")
    expect(c["turns"]["b1"] == {"buys_up_to": 5, "warm_up_to": 10, "walks_from": 20, "too_cheap_below": None},
           f"b1's turn: {c['turns']['b1']}")
    expect(c["turns"]["b2"]["too_cheap_below"] == 10 and c["turns"]["b2"]["walks_from"] is None,
           f"b2's turn: {c['turns']['b2']}")

    for f in fails:
        print(f"self-test FAIL: {f}")
    print("self-test: ok" if not fails else f"self-test: {len(fails)} failed")
    return 1 if fails else 0


def parse_prices(text: str) -> list[float]:
    out = []
    for part in text.split(","):
        p = float(part)
        if not p > 0:
            raise SystemExit(f"--prices: {part!r} is not a positive price")
        out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("stub"); s.add_argument("id"); s.add_argument("theme"); s.add_argument("--prices")
    c = sub.add_parser("check"); c.add_argument("id", nargs="?"); c.add_argument("--all", action="store_true")
    v = sub.add_parser("curve"); v.add_argument("id"); v.add_argument("theme"); v.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd == "stub":
        stub(a.id, a.theme, parse_prices(a.prices) if a.prices else DEFAULT_PRICES)
        return 0
    if a.cmd == "check":
        ids = th.all_constructions() if a.all else [a.id]
        if not ids or ids == [None]:
            raise SystemExit("check: name a construction or pass --all")
        return max(check(i) for i in ids)
    if a.cmd == "curve":
        cv = curve(find_sweep(a.id, a.theme))
        if a.json:
            print(json.dumps(cv, indent=2))
            return 0
        print(f"{a.id} {a.theme}: SIMULATED buyers, not customer research ({cv['buyers']} buyers; a maybe counts {cv['maybe_weight']:g})")
        for r in cv["by_price"]:
            k = r["counts"]
            print(f"  ${r['price_each']:<6g} share {r['share']:.2f}   buy {k['buy']}  maybe {k['maybe']}  walk {k['walk']}  too-cheap {k['too-cheap']}")
        for bid, t in cv["turns"].items():
            print(f"  {bid}: buys up to {t['buys_up_to']}, warm up to {t['warm_up_to']}, walks from {t['walks_from']}, too cheap below {t['too_cheap_below']}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
