#!/usr/bin/env python3
"""Grade a plate's maturity from what its prints showed, and measure how full its bed is.

    python3 tools/plate_grade.py                      grade every plate page
    python3 tools/plate_grade.py --plate sheets-04    grade one (repeat --plate for more)
    python3 tools/plate_grade.py --json               the same, as data
    python3 tools/plate_grade.py --fill <plate.3mf>   how much of the first bed the pieces cover
    python3 tools/plate_grade.py --recipe-hash <plate>
                                     the hash a production page pins as `recipe_hash`
    python3 tools/plate_grade.py --derive <prod-plate> <new> --answers "<question>"
                                     a new experiment plate for a change to a production recipe
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

Each grade also says whether the plate has a standing approval (D-095): a production page whose
prints still show production, on the recipe it was promoted on, with the `standing` row that
promotion writes in its Approvals table (`tools/plate_approve.py <name> --standing`, D-096).
`bambu print send` asks `plate_approve.py --status`, which reads the same check, so a production
plate goes out with no new yes and a plate that slipped, or whose recipe was edited in place,
does not.

A production recipe does not change in place. `--derive` copies it to a new plate, an experiment
whose page names its parent in `derived_from`; the change is made and printed there, and the new
plate earns production on its own prints (grade-plate skill, "Changing a production plate").

`--fill` needs a slice (`bambu slice compose`), which lives in the gitignored build/plates/, so
the grade looks for one there and says when there is none; the skill copies the number onto the
page as `bed_fill`, the way it copies minutes and grams.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "gates"))
sys.path.insert(0, str(ROOT / "tools"))

import plates_gate as pg  # noqa: E402
import plate_approve  # noqa: E402

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
        standing, standing_why = pg.standing_approval(path, data, ev, body)
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
            "standing": standing,
            "standing_why": standing_why,
            "derived_from": data.get("derived_from"),
            "recipe_hash_page": data.get("recipe_hash"),
            "recipe_hash_now": pg.recipe_hash(path),
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
        if r["declared"] == "production":
            print(f"    standing approval: {'yes' if r['standing'] else 'no'} — {r['standing_why']}")
        if r["derived_from"]:
            print(f"    derived from {r['derived_from']}")
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


def derive(parent: str, new: str, answers: str, plates: Path = pg.PLATES,
           today: str | None = None) -> str:
    """Write <new>.yaml and <new>.md: an experiment plate for a change to production plate
    `parent`. Returns the new page's path; raises ValueError when it must not be made."""
    src = plates / f"{parent}.md"
    if not src.is_file():
        raise ValueError(f"no plate page {src}")
    data, err = pg.parse_frontmatter(src.read_text(encoding="utf-8"))
    if err or not data:
        raise ValueError(f"{parent}: the page does not parse — {err}")
    if data.get("maturity") != "production":
        raise ValueError(f"{parent} is {data.get('maturity')!r}, not production: an experiment's "
                         f"recipe is edited in place, so there is nothing to derive from")
    if not new or "/" in new or new == parent:
        raise ValueError(f"{new!r} is not a new plate name")
    page, recipe = plates / f"{new}.md", plates / f"{new}.yaml"
    for p in (page, recipe):
        if p.exists():
            raise ValueError(f"{p} exists already")
    today = today or datetime.date.today().isoformat()
    recipe.write_text(f"# Derived from {parent} ({parent}.yaml) on {today}: a change to a "
                      f"production plate, as an experiment.\n"
                      f"# Make the change below and say what it is on {new}.md.\n"
                      + (plates / f"{parent}.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    cost = {k: data.get(k) for k in ("minutes", "grams", "bed_plates")}
    # The parent's cost stands in until the new recipe is sliced. With none to copy the plate
    # cannot be ranked yet, so it starts planned, waiting on its slice.
    costed = all(pg._pos(v) for v in cost.values())
    fm = {"plate": new, "recipe": f"{new}.yaml", "stage": "proposed" if costed else "planned",
          "times_printed": 0, "runs": [],
          "answers": answers, "kind": "new", "maturity": "experiment", "derived_from": parent,
          "bets": data.get("bets") or [], "unblocks": data.get("unblocks") or [], **cost,
          "risk": data.get("risk"), "pictures": [],
          **({} if costed else {"needs": [f"a slice of {new}.yaml"]})}
    page.write_text(
        "---\n" + pg.yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
        + "---\n" + plate_approve.with_table("\n"
        f"# {new} — a change to [{parent}]({parent}.md)\n\n"
        f"**In short.** {parent} is a production plate, so its recipe does not change in place "
        f"(D-095). This plate is its recipe with one change, printed as an experiment. If the "
        f"change holds up, this plate earns production on its own prints and {parent} is "
        f"retired.\n\n"
        f"## What changes from [{parent}]({parent}.md)\n\n"
        f"Say the change, and why. "
        + (f"The cost is {parent}'s until this plate is sliced." if costed else
           "It has no cost until it is sliced, so it waits as planned.") + "\n\n"
        "## Your call\n\n"
        "- [ ] **Approve as it stands**\n"
        "- [ ] **Hold** — say why in the notes\n\n"
        "Notes:\n\n"
        "## Timeline\n\n"
        "| Date | What happened | Where it is written |\n|---|---|---|\n"
        f"| {today} | proposed — derived from [{parent}]({parent}.md), a production plate, by "
        "`plate_grade.py --derive` | this page |\n"),
        encoding="utf-8")
    return str(page)


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

    import tempfile
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        plates, prints, scoring, bets = pg._build(tmp)
        rubric = pg._rubric(plates)
        try:
            derive("minis-09", "minis-10", "q", plates, "2026-10-03")
            check(False, "an experiment is not derived from")
        except ValueError as e:
            check("not production" in str(e), "an experiment is not derived from")
        pg._mature("production", pg._KEPT, own=pg._CLEAN_OWN)(plates)
        derive("minis-09", "minis-11", "does the change hold", plates, "2026-10-03")
        pg._edit("minis-09", "minutes: null\ngrams: null\nbed_plates: null",
                 "minutes: 50\ngrams: 9\nbed_plates: 1")(plates)
        derive("minis-09", "minis-10", "does the change hold", plates, "2026-10-03")
        pg.rewrite(plates, prints, scoring, bets, quiet=True, rubric=rubric)
        findings, _, _, _ = pg.check_tree(plates, prints, scoring, bets, rubric)
        check(findings == [], "derived plates pass the plates gate as written"
              + (f" — {findings}" if findings else ""))
        stage = {n: pg.parse_frontmatter((plates / f"{n}.md").read_text(encoding="utf-8"))[0]
                 ["stage"] for n in ("minis-10", "minis-11")}
        check(stage == {"minis-10": "proposed", "minis-11": "planned"},
              "it takes the parent's cost to rank, and waits on a slice when there is none")
        data, _ = pg.parse_frontmatter((plates / "minis-10.md").read_text(encoding="utf-8"))
        check(data["derived_from"] == "minis-09" and data["maturity"] == "experiment"
              and "approved" not in data and pg.approvals(plate_approve.split(
                  (plates / "minis-10.md").read_text(encoding="utf-8"))[1])
              == ([], None), "it is an experiment naming its parent, with an empty Approvals table")
        check(pg.recipe_hash(plates / "minis-10.md") == pg.recipe_hash(plates / "minis-09.md"),
              "its recipe starts as the parent's (the header comment is not a change)")
        try:
            derive("minis-09", "minis-10", "q", plates, "2026-10-03")
            check(False, "a name already taken is refused")
        except ValueError as e:
            check("exists already" in str(e), "a name already taken is refused")
    print("self-test: " + ("PASS" if not fails else f"FAIL ({fails})"))
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plate", action="append", help="grade only this plate (repeatable)")
    ap.add_argument("--json", action="store_true", help="print the grade as JSON")
    ap.add_argument("--fill", metavar="PLATE_3MF", help="measure one sliced plate's bed fill")
    ap.add_argument("--recipe-hash", metavar="PLATE", help="print the hash of a plate's recipe")
    ap.add_argument("--derive", nargs=2, metavar=("PARENT", "NEW"),
                    help="a new experiment plate for a change to production plate PARENT")
    ap.add_argument("--answers", help="with --derive: the question the new plate answers")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.fill:
        print(json.dumps(bed_fill(Path(a.fill))))
        return 0
    if a.recipe_hash:
        h = pg.recipe_hash(pg.PLATES / f"{a.recipe_hash}.md")
        if h is None:
            print(f"{a.recipe_hash}: no readable recipe docs/design/plates/{a.recipe_hash}.yaml",
                  file=sys.stderr)
            return 1
        print(h)
        return 0
    if a.derive:
        if not a.answers:
            print("--derive needs --answers: the question the new plate answers", file=sys.stderr)
            return 2
        try:
            page = derive(a.derive[0], a.derive[1], a.answers)
        except ValueError as e:
            print(f"plate_grade: {e}", file=sys.stderr)
            return 1
        print(f"wrote {page} and its recipe. Make the change in the recipe, say it on the page, "
              "then `python3 .claude/gates/plates_gate.py --write`.")
        return 0
    rows = grade(a.plate)
    if a.json:
        print(json.dumps(rows, indent=2, default=str))
    else:
        show(rows, pg.read_rubric(pg.RUBRIC))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
