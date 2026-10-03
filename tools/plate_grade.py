#!/usr/bin/env python3
"""Grade a plate's maturity from what its prints showed, and measure how full its bed is.

    python3 tools/plate_grade.py                      grade every plate page
    python3 tools/plate_grade.py --plate sheets-04    grade one (repeat --plate for more)
    python3 tools/plate_grade.py --json               the same, as data
    python3 tools/plate_grade.py --fill <plate.3mf>   how much of the first bed the pieces cover
    python3 tools/plate_grade.py --self-test

The levels and what each must show are in docs/design/printing/plate-maturity-design.md; the
numbers they use (how many kept prints make a piece repeatable, how full a production bed must
be) are in the grade-plate skill's rubric.md, read at run time. The evidence half is the plates
gate's own `maturity_evidence`, so the grade this prints and the check hook 39 runs cannot
disagree.

The grade reads three things:

  history   every print record's verdict on every piece this plate's recipe holds, oldest first.
            A piece is the same piece on any plate: same model file, same piece, same params.
  fill      the share of the first bed the pieces cover, from a sliced plate: each object's
            outline from above (the convex hull of its mesh, as `--arrange` placed it), summed,
            over the bed's 256 x 256 mm. A hull counts the space inside a ring as used, which
            is right for packing: nothing else can go there.
  value     what the plate's own prints taught: bet readings that landed (any verdict but
            no-reading), and piece verdicts given, kept or not.

`--fill` needs a slice (`bambu slice compose`), which lives in the gitignored build/plates/, so
the grade looks for one there and says when there is none; the skill copies the number onto the
page as `bed_fill`, the way it copies minutes and grams.
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "gates"))
sys.path.insert(0, str(ROOT / "tools"))

import plates_gate as pg  # noqa: E402

BED_MM = 256.0  # the X2D bed (D-053), as print_review.py and compose use


def hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Convex hull, counter-clockwise (Andrew's monotone chain)."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area(poly: list[tuple[float, float]]) -> float:
    return abs(sum(poly[i][0] * poly[i - 1][1] - poly[i - 1][0] * poly[i][1]
                   for i in range(len(poly)))) / 2


def bed_fill(plate: Path) -> dict:
    """{fill, objects, off_bed}: hull area of the objects on the first bed over the bed's area.
    An object whose centre is off the 256 mm square went to another bed and is counted apart."""
    from print_review import plate_objects  # needs Pillow; only --fill and the grade load it

    with zipfile.ZipFile(plate) as zf:
        objs = plate_objects(zf)
    used, on, off = 0.0, 0, 0
    for _, tris in objs:
        pts = [p for t in tris for p in t]
        if not pts:
            continue
        cx = sum(x for x, _ in pts) / len(pts)
        cy = sum(y for _, y in pts) / len(pts)
        if not (0 <= cx <= BED_MM and 0 <= cy <= BED_MM):
            off += 1
            continue
        used += area(hull(pts))
        on += 1
    return {"fill": round(used / (BED_MM * BED_MM), 3), "objects": on, "off_bed": off}


def slice_of(name: str) -> Path | None:
    """The newest local slice of this plate, in this checkout or the vault's main checkout."""
    for base in (ROOT, ROOT.parent.parent.parent if ROOT.parent.name == "worktrees" else ROOT):
        p = base / "build" / "plates" / f"{name}.plate.3mf"
        if p.is_file():
            return p
    return None


def grade(names: list[str] | None = None) -> list[dict]:
    rubric = pg.read_rubric(pg.RUBRIC)
    history = pg.piece_history(pg.PRINTS)
    runs = pg.plate_runs(pg.PRINTS)
    out = []
    for path, data, body, err in pg.read_pages(pg.PLATES):
        if names and path.stem not in names:
            continue
        if err or not data:
            out.append({"plate": path.stem, "error": err or "no frontmatter"})
            continue
        ev = pg.maturity_evidence(path, data, history, runs, rubric)
        own = runs.get(path.stem, [])
        sliced = slice_of(path.stem)
        fill = None
        if sliced:
            try:
                fill = bed_fill(sliced)
            except (OSError, KeyError, ValueError, zipfile.BadZipFile) as e:
                fill = {"error": str(e)}
        out.append({
            "plate": path.stem,
            "declared": data.get("maturity"),
            "evidence": ev["level"],
            "why": ev["why"],
            "pieces": ev["pieces"],
            "runs": [r["run"] for r in own],
            "clean_runs": [r["run"] for r in own if r["clean"]],
            "readings_landed": sum(r["landed"] for r in own),
            "readings": sum(r["readings"] for r in own),
            "verdicts": {v: sum(r["verdicts"].get(v, 0) for r in own) for v in ("keep", "adjust", "drop")},
            "bed_fill_page": data.get("bed_fill"),
            "bed_fill_slice": fill,
            "slice": str(sliced) if sliced else None,
        })
    return out


def show(rows: list[dict], rubric: dict) -> None:
    for r in rows:
        if "error" in r:
            print(f"{r['plate']}: cannot grade — {r['error']}")
            continue
        flag = "" if r["declared"] == r["evidence"] else "   <-- page and evidence differ"
        print(f"{r['plate']}: page says {r['declared']}, prints show {r['evidence']}{flag}")
        for line in r["why"]:
            print(f"    {line}")
        v = r["verdicts"]
        print(f"    its own prints: {len(r['runs'])} run(s), {len(r['clean_runs'])} with every piece kept; "
              f"pieces judged keep {v['keep']}, adjust {v['adjust']}, drop {v['drop']}; "
              f"bet readings that landed {r['readings_landed']} of {r['readings']}")
        f = r["bed_fill_slice"]
        if f is None:
            print("    bed: no local slice to measure")
        elif "error" in f:
            print(f"    bed: the slice did not read — {f['error']}")
        else:
            need = rubric["production_fill"]
            print(f"    bed: {f['fill']:.0%} of the first bed covered by {f['objects']} object(s)"
                  + (f", {f['off_bed']} on another bed" if f["off_bed"] else "")
                  + f" (production asks {need:.0%})")


def self_test() -> int:
    fails = 0

    def check(ok: bool, label: str) -> None:
        nonlocal fails
        fails += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}")

    sq = [(0, 0), (10, 0), (10, 10), (0, 10), (5, 5)]
    check(abs(area(hull(sq)) - 100) < 1e-9, "a square's hull is the square; an inside point adds nothing")
    ring = [(x, y) for x, y in sq[:4]] + [(4, 4), (6, 4), (6, 6), (4, 6)]
    check(abs(area(hull(ring)) - 100) < 1e-9, "a ring counts the space inside it as used")
    check(area(hull([(0, 0), (1, 1)])) == 0, "a degenerate object covers nothing")
    print("self-test: " + ("PASS" if not fails else f"FAIL ({fails})"))
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plate", action="append", help="grade only this plate (repeatable)")
    ap.add_argument("--json", action="store_true", help="print the grade as JSON")
    ap.add_argument("--fill", metavar="PLATE_3MF", help="measure one sliced plate's bed fill")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.fill:
        print(json.dumps(bed_fill(Path(a.fill))))
        return 0
    rows = grade(a.plate)
    if a.json:
        print(json.dumps(rows, indent=2, default=str))
    else:
        show(rows, pg.read_rubric(pg.RUBRIC))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
