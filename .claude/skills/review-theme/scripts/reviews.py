#!/usr/bin/env python3
"""Persona reviews of color themes: the block to fill in, and the check that holds them honest.

Reviews live beside the themes they score, in `docs/design/coaster/themes/<id>/reviews.yaml`:

    reviews:
      - theme: pink-heart          # a theme id in themes.yaml
        coloring: 1a2b3c4d5e       # themes.py's hash of the theme's colors when it was reviewed
        scores:
          espresso-purist: { score: 2, why: "one line, in the persona's terms" }
          ...                      # every persona in ../personas.md, no others
        overall: "One sentence: who it is for, and what holds it back."

The personas are read from `.claude/skills/review-theme/personas.md` on every run, so adding one
there makes every review short of it until it is scored.

Usage:
    reviews.py stub  <id> [<theme>]   print the block to paste into reviews.yaml (every theme if none named)
    reviews.py check <id> | --all     every theme reviewed for its current colors, every persona scored
    reviews.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

SKILL = Path(__file__).resolve().parent.parent
ROOT = SKILL.parent.parent.parent
PERSONAS = SKILL / "personas.md"
# The themes, their hash and the folder layout belong to the color-themes skill; reuse them
# rather than keep a second copy that could drift.
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "color-themes" / "scripts"))
import themes as th  # noqa: E402

MAX_WHY = 200  # a "why" longer than this is a paragraph, not a one-line reason


def persona_ids(path: Path = PERSONAS) -> list[str]:
    ids = []
    for line in path.read_text().splitlines():
        m = re.match(r"\|\s*`([a-z0-9-]+)`\s*\|", line)
        if m:
            ids.append(m.group(1))
    return ids


def one_line(text) -> bool:
    return isinstance(text, str) and text.strip() != "" and "\n" not in text.strip()


def problems(con: dict, data: dict | None, personas: list[str]) -> list[str]:
    """Everything wrong with one construction's reviews, as plain sentences."""
    out = []
    themes = {t["id"]: t for t in con["themes"]}
    reviews = (data or {}).get("reviews") or []
    seen = set()
    for r in reviews:
        tid = r.get("theme")
        if tid not in themes:
            out.append(f"a review names theme {tid!r}, which themes.yaml does not have")
            continue
        if tid in seen:
            out.append(f"{tid}: reviewed twice")
        seen.add(tid)
        if r.get("coloring") != th.theme_hash(themes[tid]):
            out.append(f"{tid}: the review is for an earlier coloring; look at the new picture and "
                       f"review it again (coloring is now {th.theme_hash(themes[tid])})")
        scores = r.get("scores") or {}
        for pid in personas:
            if pid not in scores:
                out.append(f"{tid}: no score from {pid}")
        for pid, sc in scores.items():
            if pid not in personas:
                out.append(f"{tid}: {pid} is not a persona in personas.md")
                continue
            s = (sc or {}).get("score")
            if not isinstance(s, int) or isinstance(s, bool) or not 1 <= s <= 5:
                out.append(f"{tid}: {pid}'s score {s!r} is not a whole number from 1 to 5")
            why = (sc or {}).get("why")
            if not one_line(why):
                out.append(f"{tid}: {pid}'s reason must be one line of text")
            elif len(why.strip()) > MAX_WHY:
                out.append(f"{tid}: {pid}'s reason is {len(why.strip())} characters; keep it to one line "
                           f"of at most {MAX_WHY}")
        if not one_line(r.get("overall")):
            out.append(f"{tid}: the overall line must be one line of text")
    for tid in themes:
        if tid not in seen:
            out.append(f"{tid}: not reviewed; `reviews.py stub {con['_folder'].name} {tid}`")
    return out


def check(cid: str, root: Path = th.THEMES_DIR, personas: list[str] | None = None) -> int:
    con = th.construction(cid, root)
    path = con["_folder"] / "reviews.yaml"
    data = th.load_yaml(path) if path.exists() else None
    errs = problems(con, data, personas or persona_ids())
    for e in errs:
        print(f"{cid}: {e}")
    return 1 if errs else 0


def stub(cid: str, tid: str | None) -> None:
    con = th.construction(cid)
    picked = [t for t in con["themes"] if tid is None or t["id"] == tid]
    if not picked:
        raise SystemExit(f"{cid} has no theme {tid}")
    lines = ["reviews:"] if tid is None else []
    for theme in picked:
        lines += [f"  - theme: {theme['id']}", f"    coloring: {th.theme_hash(theme)}", "    scores:"]
        for pid in persona_ids():
            lines.append(f'      {pid}: {{ score: 0, why: "" }}')
        lines.append('    overall: ""')
    print("\n".join(lines))


def self_test() -> int:
    fails = []

    def expect(cond, what):
        if not cond:
            fails.append(what)

    personas = persona_ids()
    expect(len(personas) == 6, f"personas.md: expected 6 personas, read {len(personas)}")

    con = {"_folder": Path("fx"), "themes": [
        {"id": "a", "colors": {"x": "pink", "frame": "black"}},
        {"id": "b", "colors": {"x": "green", "frame": "black"}},
    ]}
    ps = ["p1", "p2"]

    def good(tid):
        t = next(t for t in con["themes"] if t["id"] == tid)
        return {"theme": tid, "coloring": th.theme_hash(t), "overall": "Fine for p1.",
                "scores": {"p1": {"score": 4, "why": "likes it"}, "p2": {"score": 2, "why": "too loud"}}}

    expect(problems(con, {"reviews": [good("a"), good("b")]}, ps) == [], "a clean pair of reviews failed")

    def fails_with(review_b, needle, what):
        errs = problems(con, {"reviews": [good("a"), review_b]}, ps)
        expect(any(needle in e for e in errs), f"{what} was not caught: {errs}")

    r = good("b"); r["coloring"] = "0000000000"
    fails_with(r, "earlier coloring", "a stale coloring")
    r = good("b"); del r["scores"]["p2"]
    fails_with(r, "no score from p2", "a missing persona")
    r = good("b"); r["scores"]["p3"] = {"score": 3, "why": "x"}
    fails_with(r, "not a persona", "an unknown persona")
    for bad in (0, 6, 3.5, "4", True):
        r = good("b"); r["scores"]["p1"]["score"] = bad
        fails_with(r, "whole number", f"score {bad!r}")
    r = good("b"); r["scores"]["p1"]["why"] = "line one\nline two"
    fails_with(r, "one line", "a two-line reason")
    r = good("b"); r["scores"]["p1"]["why"] = "x" * (MAX_WHY + 1)
    fails_with(r, "characters", "an over-long reason")
    r = good("b"); r["overall"] = ""
    fails_with(r, "overall line", "an empty overall line")
    r = good("b"); r["theme"] = "zzz"
    fails_with(r, "does not have", "a review of a theme that does not exist")
    errs = problems(con, {"reviews": [good("a")]}, ps)
    expect(any("b: not reviewed" in e for e in errs), "an unreviewed theme was not caught")
    errs = problems(con, {"reviews": [good("a"), good("a"), good("b")]}, ps)
    expect(any("reviewed twice" in e for e in errs), "a theme reviewed twice was not caught")

    for f in fails:
        print(f"self-test FAIL: {f}")
    print("self-test: ok" if not fails else f"self-test: {len(fails)} failed")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("stub"); s.add_argument("id"); s.add_argument("theme", nargs="?")
    c = sub.add_parser("check"); c.add_argument("id", nargs="?"); c.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd == "stub":
        stub(a.id, a.theme)
        return 0
    if a.cmd == "check":
        ids = th.all_constructions() if a.all else [a.id]
        if not ids or ids == [None]:
            raise SystemExit("check: name a construction or pass --all")
        return max(check(i) for i in ids)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
