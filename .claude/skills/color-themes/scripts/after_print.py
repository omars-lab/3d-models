#!/usr/bin/env python3
"""The `## After the print` table on a theme or swatch plate page: what gets asked when it comes off the bed.

Omar asked on 2026-10-08 for an "anticipated table of printing this and each one and why we are
printing it". The plates gate's rule P12 holds every experiment plate to it: a row per question,
`| Pieces | The question | What we expect, and why | What each answer changes |`, every cell written.
The review-print skill asks the rows one at a time when the print comes back.

theme_plates.py and swatch.py write the table into each new page. `insert` adds it to a page
those scripts wrote before the rule, without writing the page again, so its approvals, timeline
and slice numbers stay as they are. It reads what it needs from the page itself: the pieces from
the first "What it is" bullet, the color from the title, and the gap-0 warning from the flags.

Usage:
    after_print.py insert <page.md>...    add the table to theme-*.md and swatch-*.md pages lacking one
    after_print.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEAD = "| Pieces | The question | What we expect, and why | What each answer changes |"
TITLE = "## After the print"
INTRO = "What gets asked when it comes off the bed, one row at a time (the review-print skill asks them)."
GAP0 = "cut at `gap: 0`"


def section(rows: list[tuple[str, str, str, str]]) -> str:
    """The section, ending in a blank line so the next `##` follows as on every page."""
    body = "\n".join(f"| {' | '.join(r)} |" for r in rows)
    return f"{TITLE}\n\n{INTRO}\n\n{HEAD}\n|---|---|---|---|\n{body}\n\n"


def theme_rows(what: str, color: str, gap: float | None, frame_only: bool) -> list[tuple[str, str, str, str]]:
    """A theme plate's questions: the color, then the fit (or, for a frame alone, whether it lies flat)."""
    rows = [(
        what,
        f"Does {color} look the way the theme picture draws it, beside the theme's other colors in the frame?",
        "Close, not exact: the picture draws the color catalog's screen color, not a printed surface.",
        "Looks right: the color stays in the theme. Off: the color-themes skill swaps in the nearest "
        "color and draws the theme again, and this plate is cut again in it.",
    )]
    if frame_only:
        rows.append((
            what,
            "Does the frame lie flat, with no corner lifted, and do the other plates' pieces drop into it?",
            "Flat: it is the frame sheets-04g printed at this size, on the same bed.",
            "Flat: the frame is kept as it is. A lifted corner: the frame recipe gets a brim, as a new "
            "iteration, before the rest of the theme is printed.",
        ))
        return rows
    if gap == 0:
        expect = ("The kites too tight and the middle too loose: they are cut at gap 0, the fit "
                  "sheets-04g printed and found off.")
    else:
        expect = f"They drop in and stay: they are cut at the gap this recipe names{f' ({gap} mm)' if gap is not None else ''}."
    rows.append((
        f"{what}, in the frame",
        "Do the pieces drop into the frame and stay, without pressing?",
        expect,
        "Drop in and stay: the gap is kept for every theme plate. Tight or loose: every theme plate is "
        "cut again at the gaps sheets-04g-fit settles, each as a new iteration of its recipe.",
    ))
    return rows


def swatch_rows(code: str, color: str) -> list[tuple[str, str, str, str]]:
    """A swatch's questions: the chip against the catalog, then the color on our own coaster."""
    return [
        (
            "CHIP",
            f"Does the chip's top match the color catalog's hex for {code}, and how does its bed face differ?",
            "Near the catalog's hex on top; the bed face flatter in sheen, since it printed against the plate.",
            f"Matches: the catalog's hex stands for {color}. Off: the catalog entry for {code} is corrected "
            "to the printed color, and the theme pictures that use it are drawn again.",
        ),
        (
            "WINDOW",
            f"Does {color} read well on our own straps and edges, at coaster size?",
            "As the chip reads; a very dark or very light color may lose the strap lines.",
            "Reads well: the color stays a candidate for themes. Lines lost or too loud: the color-themes "
            "skill stops offering it for a coaster's straps.",
        ),
    ]


def insert(text: str, sec: str) -> str | None:
    """The page with the section before `## Pictures`, or None when it has one already."""
    if re.search(rf"^{re.escape(TITLE)}\b", text, re.MULTILINE):
        return None
    at = re.search(r"^## Pictures\b", text, re.MULTILINE)
    if not at:
        raise SystemExit("no '## Pictures' section to put the table before")
    return text[:at.start()] + sec + text[at.start():]


def rows_for(text: str, name: str) -> list[tuple[str, str, str, str]]:
    """The rows for a page the generators wrote, read from the page itself."""
    h1 = re.search(r"^# (\S+) — (.+)$", text, re.MULTILINE)
    if not h1:
        raise SystemExit(f"{name}: no '# <plate> — …' title")
    plate, rest = h1.group(1), h1.group(2)
    if plate.startswith("swatch-"):
        m = re.fullmatch(r"a swatch of (.+)", rest)
        if not m:
            raise SystemExit(f"{name}: the title does not say 'a swatch of …'")
        return swatch_rows(plate.split("-", 1)[1], m.group(1))
    if plate.startswith("theme-"):
        m = re.fullmatch(r"(.+) in (.+)", rest)
        what = re.search(r"^## What it is\s+- \*\*(.+?)\*\*", text, re.MULTILINE)
        if not m or not what:
            raise SystemExit(f"{name}: no '<theme> in <color>' title or no first 'What it is' bullet")
        pieces = [p.strip() for p in what.group(1).split(",")]
        frame_only = all(p.lower().startswith("frame") for p in pieces)
        return theme_rows(what.group(1), m.group(2), 0 if GAP0 in text else None, frame_only)
    raise SystemExit(f"{name}: not a theme or swatch page; write its table by hand")


def insert_pages(paths: list[Path]) -> int:
    for p in paths:
        text = p.read_text()
        out = insert(text, section(rows_for(text, p.name)))
        if out is None:
            print(f"{p.name}: has a table already, left as it is")
            continue
        p.write_text(out)
        print(f"{p.name}: table added")
    return 0


def self_test() -> int:
    fails = []
    theme = ("# theme-night-sky-11600 — Night sky in Marine Blue\n\n## What it is\n\n"
             "- **Kite ×10**, every one in PLA Matte Marine Blue (11600)\n\n**Before you say yes:**\n\n"
             "- **The pieces are cut at `gap: 0`, as sheets-04g printed them**\n\n## Why print it\n\nx\n\n"
             "## Pictures\n\ny\n")
    rows = rows_for(theme, "t")
    if len(rows) != 2 or "too tight" not in rows[1][2] or "Marine Blue" not in rows[0][1]:
        fails.append(f"a gap-0 theme page read wrong: {rows}")
    out = insert(theme, section(rows))
    if out is None or out.index(TITLE) > out.index("## Pictures") or out.index(TITLE) < out.index("## Why print it"):
        fails.append("the table is not between Why print it and Pictures")
    if out and insert(out, section(rows)) is not None:
        fails.append("a page with a table got a second one")
    frame = theme.replace("Kite ×10", "Frame ×1").replace(GAP0, "cut at")
    rows = rows_for(frame, "f")
    if "lie flat" not in rows[1][1]:
        fails.append(f"a frame-only page is asked about the fit: {rows}")
    mixed = theme.replace("Kite ×10", "Frame ×1, Kite ×10")
    if "lie flat" in rows_for(mixed, "m")[1][1]:
        fails.append("a frame-and-pieces page is asked only whether the frame lies flat")
    swatch = "# swatch-10204 — a swatch of PLA Basic Hot Pink\n\n## Pictures\n"
    rows = rows_for(swatch, "s")
    if [r[0] for r in rows] != ["CHIP", "WINDOW"] or "10204" not in rows[0][1]:
        fails.append(f"a swatch page read wrong: {rows}")
    for r in theme_rows("Kite ×10", "Marine Blue", 0.1, False) + swatch_rows("10204", "Hot Pink"):
        if len(r) != 4 or any(not c.strip() or c.strip() in ("—", "-") or "|" in c for c in r):
            fails.append(f"a row the plates gate would refuse: {r}")
    sec = section(theme_rows("Kite ×10", "Marine Blue", 0, False))
    if HEAD not in sec.splitlines():
        fails.append("the header is not the plates gate's")
    for bad in ("# split-01 — a split\n\n## Pictures\n", "# theme-x — no color here\n\n## Pictures\n"):
        try:
            rows_for(bad, "bad")
            fails.append(f"read rows from a page it should refuse: {bad.splitlines()[0]}")
        except SystemExit:
            pass
    try:
        insert("# theme-x — A in B\n", "s")
        fails.append("inserted into a page with no Pictures section")
    except SystemExit:
        pass
    for f in fails:
        print(f"FAIL: {f}")
    print(f"after_print self-test: {'ok' if not fails else f'{len(fails)} failed'}")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    i = sub.add_parser("insert")
    i.add_argument("pages", nargs="+", type=Path)
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd == "insert":
        return insert_pages(a.pages)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
