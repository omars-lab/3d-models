#!/usr/bin/env python3
"""Check the slit marks read from the judged pieces' bed-face photos, and say whether they separate
Omar's verdicts: where the slits sit by layout, and whether the marks alone order the judged pairs as
he did. This is the stop rule's first half (SKILL.md step 2): if every place shows on every layout in
like numbers, the marks cannot teach a model what goes where, and the fit should not ship.

  marks.py [--marks FILE] [--pairs FILE]   check the file, then the table by layout and the pairs
  marks.py --self-test
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "tools/print_review.py").exists())
SIM = ROOT / ".claude/skills/simulate-first-layer"
sys.path.insert(0, str(SIM / "scripts"))
import yaml  # noqa: E402

PLACES = ("wall", "middle", "ring_seam", "id")
SPREAD_MIN = 1.0     # a place separates layouts when their mean levels differ by at least one step


def problems(marks, pairs, root=ROOT):
    """Every way the marks file is wrong: a judged piece with no entry, a level outside 0-3, a
    piece left unmarked with no reason, a photo that is not on disk, no photo-quality line, or a
    reader other than Claude named (the marks are never Omar's)."""
    out = []
    if "Claude" not in str(marks.get("read_by", "")):
        out.append("read_by must say the marks are Claude's reading, not Omar's")
    pieces = marks.get("pieces") or {}
    for key in pairs["pieces"]:
        if str(key) not in {str(k) for k in pieces}:
            out.append(f"{key}: judged but not in the marks file")
    for key, e in pieces.items():
        m = e.get("marks") or {}
        for place in PLACES:
            v = m.get(place, "missing")
            if v is not None and v not in (0, 1, 2, 3):
                out.append(f"{key}: {place} is {v!r}; a level is 0-3, or null when the place is not there")
        if (not e.get("photo") or all(m.get(p) is None for p in PLACES)) and not e.get("why"):
            out.append(f"{key}: no photo or no mark, and no `why`")
        if e.get("photo") and not (root / e["photo"]).exists():
            out.append(f"{key}: photo {e['photo']} is not on disk")
        if not e.get("photo_quality"):
            out.append(f"{key}: no photo_quality line")
    return out


def by_layout(marks):
    """{layout: {place: mean level, or None}} over the marked pieces."""
    acc = {}
    for e in marks["pieces"].values():
        for place in PLACES:
            v = (e.get("marks") or {}).get(place)
            if v is not None:
                acc.setdefault(e["layout"], {}).setdefault(place, []).append(v)
    return {lay: {p: (sum(v) / len(v) if (v := d.get(p)) else None) for p in PLACES} for lay, d in acc.items()}


def separating(table):
    """The places whose mean level differs across layouts by at least SPREAD_MIN."""
    out = []
    for place in PLACES:
        vals = [d[place] for d in table.values() if d[place] is not None]
        if len(vals) > 1 and max(vals) - min(vals) >= SPREAD_MIN:
            out.append(place)
    return out


def total(e):
    m = e.get("marks") or {}
    vals = [m.get(p) for p in ("wall", "middle", "ring_seam")]
    return None if all(v is None for v in vals) else sum(v or 0 for v in vals)


def pair_order(marks, pairs):
    """[(pair, what the mark totals say, agrees?)] for the judged pairs whose two pieces are marked.
    Fewer marks is better; equal totals say same."""
    pieces = {str(k): e for k, e in marks["pieces"].items()}
    out = []
    for p in pairs["pairs"]:
        a, b = total(pieces.get(str(p["a"]), {})), total(pieces.get(str(p["b"]), {}))
        if a is None or b is None:
            continue
        says = "same" if a == b else ("better" if a < b else "worse")
        ok = says == p["omar"] or (p["omar"] == "not_better" and says != "better")
        out.append((p, says, ok))
    return out


def report(marks, pairs):
    table = by_layout(marks)
    print("Mean slit level by layout (0 none, 3 many), from the photos, Claude's reading:")
    print()
    print("| Layout | Pieces | " + " | ".join(PLACES) + " |")
    print("|---|---|" + "---|" * len(PLACES))
    count = {}
    for e in marks["pieces"].values():
        if total(e) is not None:
            count[e["layout"]] = count.get(e["layout"], 0) + 1
    for lay, d in table.items():
        print(f"| {lay} | {count.get(lay, 0)} | " + " | ".join("-" if d[p] is None else f"{d[p]:.1f}"
                                                         for p in PLACES) + " |")
    sep = separating(table)
    rows = pair_order(marks, pairs)
    nt = [r for r in rows if r[0]["omar"] not in ("same",)]
    ok_nt = sum(r[2] for r in nt)
    print()
    print("| A | B | Omar | Marks say | Agrees |")
    print("|---|---|---|---|---|")
    for p, says, ok in rows:
        print(f"| {p['a']} | {p['b']} | {p['omar']} | {says} | {'yes' if ok else 'no'} |")
    print()
    print(f"Places that differ by layout (mean levels {SPREAD_MIN:g} step or more apart): "
          + (", ".join(sep) or "none"))
    print(f"Mark totals order {ok_nt} of {len(nt)} marked pairs that are not ties as Omar did, "
          f"{sum(r[2] for r in rows)} of {len(rows)} in all.")
    stop = not sep or ok_nt * 2 <= len(nt)
    print("Stop rule: " + ("the marks do NOT separate the verdicts; ship the marks with that finding, "
                           "not a model." if stop else
                           "the marks separate the verdicts (slits sit in different places by layout, "
                           "and the totals order most pairs as Omar did); fitting may go on."))
    return stop


def self_test():
    pairs = {"pieces": {"A": {}, "B": {}, "C": {}}, "pairs": [
        {"a": "A", "b": "B", "omar": "better"}, {"a": "B", "b": "C", "omar": "same"}]}
    good = {"read_by": "Claude", "pieces": {
        "A": {"photo": None, "why": "none", "layout": "x", "photo_quality": "none",
              "marks": {"wall": 0, "middle": 0, "ring_seam": None, "id": 0}},
        "B": {"photo": None, "why": "none", "layout": "y", "photo_quality": "none",
              "marks": {"wall": 0, "middle": 3, "ring_seam": None, "id": 0}},
        "C": {"photo": None, "why": "none", "layout": "y", "photo_quality": "none",
              "marks": {"wall": 0, "middle": 3, "ring_seam": None, "id": 0}}}}
    bad = {"read_by": "Omar", "pieces": {"A": {"photo": "no/such.jpg", "layout": "x",
                                               "marks": {"wall": 5, "middle": None, "ring_seam": None, "id": None}}}}
    errs = problems(bad, pairs)
    table = by_layout(good)
    rows = pair_order(good, pairs)
    flat = {"pieces": {k: {**e, "layout": "x"} for k, e in good["pieces"].items()}}
    return [
        ("marks: a good file has no problems", problems(good, pairs) == []),
        ("marks: Omar named as the reader is refused", any("read_by" in e for e in errs)),
        ("marks: a level outside 0-3 is refused", any("wall is 5" in e for e in errs)),
        ("marks: a judged piece with no entry is named", any(e.startswith("B:") for e in errs)),
        ("marks: a photo not on disk is named", any("not on disk" in e for e in errs)),
        ("marks: no photo quality line is named", any("photo_quality" in e for e in errs)),
        ("marks: a place that differs by layout separates", separating(table) == ["middle"]),
        ("marks: one layout separates nothing", separating(by_layout(flat)) == []),
        ("marks: fewer marks reads better, equal reads same",
         [s for _, s, _ in rows] == ["better", "same"] and all(ok for *_, ok in rows)),
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--marks", default=str(SIM / "marked-slits.yaml"))
    ap.add_argument("--pairs", default=str(SIM / "judged-pairs.yaml"))
    args = ap.parse_args()
    if args.self_test:
        checks = self_test()
        for name, ok in checks:
            print("PASS" if ok else "FAIL", name)
        sys.exit(0 if all(ok for _, ok in checks) else 1)
    marks = yaml.safe_load(Path(args.marks).read_text())
    pairs = yaml.safe_load(Path(args.pairs).read_text())
    errs = problems(marks, pairs)
    for e in errs:
        print("marks:", e)
    if errs:
        sys.exit(1)
    report(marks, pairs)


if __name__ == "__main__":
    main()
