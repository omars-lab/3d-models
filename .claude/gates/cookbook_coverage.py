#!/usr/bin/env python3
"""Every naqsh statement keyword has a cookbook recipe, or a line saying why not.

The cookbook (`docs/cookbook/`) is only useful while it keeps up with the
language. Omar, 2026-09-28: "as we add new mechanisms to our language, we
should be extending the cookbook". A reminder in a skill does not make that
happen; this check does. It fails when bikar gains a keyword that the cookbook
neither covers nor lists as not covered yet, and it names the keyword.

WHERE THE KEYWORDS COME FROM. Harvested from bikar's `docs/grammar.md`, not
listed here — the same read `catalog_models.py` makes, for the same reason: its
first run carried a hand-written list, the list missed `clip`, and it reported
two correct entries as wrong. bikar's own G3 conformance test holds grammar.md
to what the parser actually accepts, so reading the grammar stays true.

What counts as a statement keyword: the first word of each alternative of
every production named `...Stmt` or `...Decl` (a statement inside a block, or a
top-level declaration), following a production that is only a list of other
productions — `CoasterStmt = CoasterOutline | CoasterBase | ...` — one level
into each, so the coaster's `outline`, `strap`, `interlock` ... count. Plus
`Transform`, whose four words (`rotate`, `reflect`, `translate`, `invert`) are
the core moves of a construction even though they sit on the right of an `=`.
If the grammar cannot be read, or yields implausibly few keywords, the check
fails loud rather than passing on an empty set.

What it does NOT see: grammar.md writes the bodies of `orb`, `piece`, `tile`,
`wall` and `assembly` as prose, not productions, so their clauses (`weave`,
`band`, `hole` ...) are not harvested and cannot be marked `covers:`. When
bikar writes those as productions they show up here on their own.

WHERE THE COVERAGE COMES FROM.
  * `<!--covers:kw-->` anywhere in `docs/cookbook/*.md` (the same marker
    bikar's GeoGebra cookbook uses), and
  * the "Not in the cookbook yet" section of `docs/cookbook/README.md`: bullets
    that name keywords in backticks, then a dash and the reason.

The not-yet list may shrink freely — that is a recipe landing — but it grows
only on purpose, like the doc-pointer baseline: a keyword added to it that was
not there at HEAD needs `COOKBOOK_NOT_YET_MAY_GROW=1`. Otherwise "add it to the
not-yet list" becomes the easy answer every time.

Usage:
    python3 .claude/gates/cookbook_coverage.py            # check; non-zero on a gap
    python3 .claude/gates/cookbook_coverage.py --list     # every keyword and where it stands
    python3 .claude/gates/cookbook_coverage.py --self-test

Env:
    BIKAR_DIR                      where bikar is checked out (the Makefile passes it)
    COOKBOOK_NOT_YET_MAY_GROW=1    allow new entries on the not-yet list
    COOKBOOK_OK=1                  skip entirely (the hook honors it)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from catalog_models import read_from_bikar  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
COOKBOOK_REL = "docs/cookbook"
README_REL = f"{COOKBOOK_REL}/README.md"
GRAMMAR_MD_REL = "docs/grammar.md"
NOT_YET_HEADING = "## Not in the cookbook yet"

#: A production's head: `CircleStmt   = ...` at the start of a line.
PRODUCTION = re.compile(r"^([A-Za-z]+)\s*=(?!=)", re.M)
EBNF_FENCE = re.compile(r"```ebnf\n(.*?)```", re.S)
COVERS = re.compile(r"<!--\s*covers:\s*([a-z_]+)\s*-->")
BACKTICK_WORD = re.compile(r"`([a-z_]+)`")
#: Fewer than this and the grammar has changed shape under us.
MIN_KEYWORDS = 40


def productions(grammar: str) -> dict[str, str]:
    """`{name: body}` for every production in the grammar's ebnf fences.

    A body runs from after the `=` to the `;` that ends it. A `;` inside a
    quoted literal or an `(* ... *)` comment does not end it.
    """
    out: dict[str, str] = {}
    for fence in EBNF_FENCE.findall(grammar):
        text = re.sub(r"\(\*.*?\*\)", " ", fence, flags=re.S)
        heads = list(PRODUCTION.finditer(text))
        for i, m in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            body = text[m.end() : end]
            body = _cut_at_terminator(body)
            out.setdefault(m.group(1), body)
    return out


def _cut_at_terminator(body: str) -> str:
    in_quote = False
    for i, ch in enumerate(body):
        if ch == '"':
            in_quote = not in_quote
        elif ch == ";" and not in_quote:
            return body[:i]
    return body


def alternatives(body: str) -> list[str]:
    """Split a body on the `|` signs that are not inside brackets or quotes."""
    parts, depth, in_quote, cur = [], 0, False, []
    for ch in body:
        if ch == '"':
            in_quote = not in_quote
        elif not in_quote and ch in "([{":
            depth += 1
        elif not in_quote and ch in ")]}":
            depth -= 1
        elif not in_quote and depth == 0 and ch == "|":
            parts.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


FIRST = re.compile(r'^(?:"([a-z_]+)"|([A-Z][A-Za-z]*))')


def first_words(name: str, prods: dict[str, str], depth: int = 0) -> set[str]:
    """The keywords that can open production `name`, following one bare reference."""
    words: set[str] = set()
    for alt in alternatives(prods.get(name, "")):
        m = FIRST.match(alt)
        if not m:
            continue
        if m.group(1):
            words.add(m.group(1))
        elif depth == 0 and m.group(2) in prods and alt == m.group(2):
            words |= first_words(m.group(2), prods, depth + 1)
    return words


def harvest(grammar: str) -> set[str]:
    prods = productions(grammar)
    keywords: set[str] = set()
    for name in prods:
        if name.endswith(("Stmt", "Decl")) or name == "Transform":
            keywords |= first_words(name, prods)
    return keywords


def statement_keywords(root: Path = ROOT) -> tuple[set[str], str | None]:
    src = read_from_bikar(GRAMMAR_MD_REL, root)
    if src is None:
        return set(), f"bikar's {GRAMMAR_MD_REL} could not be read"
    kws = harvest(src)
    if len(kws) < MIN_KEYWORDS:
        return set(), (
            f"{GRAMMAR_MD_REL} yielded only {len(kws)} statement keyword(s) — "
            "its `...Stmt = \"kw\"` productions have changed shape"
        )
    return kws, None


def covered(root: Path = ROOT) -> dict[str, str]:
    """`{keyword: page}` for every `<!--covers:kw-->` in the cookbook."""
    out: dict[str, str] = {}
    for page in sorted((root / COOKBOOK_REL).glob("*.md")):
        for kw in COVERS.findall(page.read_text(encoding="utf-8")):
            out.setdefault(kw, page.name)
    return out


def not_yet(readme: str) -> set[str]:
    """Keywords named in the README's "Not in the cookbook yet" bullets.

    Only the backticked words before the reason's dash count, so a reason may
    mention another keyword without listing it.
    """
    out: set[str] = set()
    lines = readme.split("\n")
    inside = False
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == NOT_YET_HEADING
            continue
        if inside and line.startswith("- "):
            head = re.split(r"\s[—–-]\s", line[2:], maxsplit=1)[0]
            out |= set(BACKTICK_WORD.findall(head))
    return out


def not_yet_at_head(root: Path) -> set[str] | None:
    try:
        text = subprocess.run(
            ["git", "show", f"HEAD:{README_REL}"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return not_yet(text)


def check(
    keywords: set[str], cover: dict[str, str], later: set[str], previous: set[str] | None
) -> list[str]:
    problems: list[str] = []
    missing = sorted(keywords - set(cover) - later)
    if missing:
        problems.append(
            "naqsh keyword(s) with no cookbook recipe and no not-yet line: "
            + ", ".join(f"`{k}`" for k in missing)
            + "\n    Run the maintain-cookbook skill: write the recipe (mark it"
            " `<!--covers:kw-->`),\n    or add the keyword to the not-yet list in"
            f" {README_REL} with the reason."
        )
    both = sorted(set(cover) & later)
    if both:
        problems.append(
            "covered by a recipe AND still on the not-yet list — take them off the list: "
            + ", ".join(f"`{k}`" for k in both)
        )
    unknown = sorted((set(cover) | later) - keywords)
    if unknown:
        problems.append(
            "named in the cookbook but not a naqsh statement keyword (renamed or removed "
            "in bikar?): " + ", ".join(f"`{k}`" for k in unknown)
        )
    if previous is not None and os.environ.get("COOKBOOK_NOT_YET_MAY_GROW") != "1":
        grew = sorted(later - previous)
        if grew:
            problems.append(
                "the not-yet list GREW: "
                + ", ".join(f"`{k}`" for k in grew)
                + "\n    It may shrink freely and grows only on purpose. Write the recipe,"
                " or state the addition:\n      COOKBOOK_NOT_YET_MAY_GROW=1 make validate-cookbook"
            )
    return problems


def _self_test() -> int:
    grammar = (
        "```ebnf\n"
        'CircleStmt = "circle" IDENT "center" Expr\n'
        '           | "circle" IDENT "=" Transform ;\n'
        'Transform  = "rotate" Operand | "reflect" Operand (* ; not the end *) ;\n'
        "BoxStmt    = BoxSize | BoxLid ;\n"
        'BoxSize    = "size" NUMBER ;\n'
        'BoxLid     = "lid" ( "on" | "off" ) ;\n'
        'Pick       = "pick" NUMBER ;\n'
        "```\n"
    )
    readme = (
        "# Cookbook\n\n## Not in the cookbook yet\n\n"
        "- `lid` — rare; see `size` for the pattern\n\n## Next\n\n- `pick` — not a list entry\n"
    )
    cases = [
        ("harvest reads alternatives, Transform and one level of reference",
         harvest(grammar) == {"circle", "rotate", "reflect", "size", "lid"}),
        ("a keyword in the reason is not listed", not_yet(readme) == {"lid"}),
    ]
    kws = harvest(grammar)
    cover = {"circle": "a.md", "rotate": "a.md", "reflect": "a.md"}
    cases += [
        # FAIL: bikar gains `size` — named, and the skill is named.
        ("an uncovered keyword fails and names the skill",
         any("`size`" in p and "maintain-cookbook" in p for p in check(kws, cover, {"lid"}, {"lid"}))),
        # PASS: every keyword covered or listed.
        ("covered + listed passes", check(kws, {**cover, "size": "b.md"}, {"lid"}, {"lid"}) == []),
        ("growing the list fails", any("GREW" in p for p in check(kws, cover, {"lid", "size"}, {"lid"}))),
        ("shrinking the list passes", check(kws, {**cover, "size": "b.md", "lid": "b.md"}, set(), {"lid"}) == []),
        ("a stale keyword fails", any("`gone`" in p for p in check(kws, {**cover, "gone": "a.md"}, {"lid", "size"}, None))),
    ]
    ok = True
    for name, passed in cases:
        print(f"self-test {'ok  ' if passed else 'FAIL'}: {name}")
        ok &= passed
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if os.environ.get("COOKBOOK_OK") == "1":
        return 0
    keywords, why = statement_keywords()
    if why:
        print(f"cookbook coverage: CANNOT CHECK — {why}", file=sys.stderr)
        return 1
    cover = covered()
    readme = ROOT / README_REL
    later = not_yet(readme.read_text(encoding="utf-8")) if readme.is_file() else set()
    if args.list:
        for kw in sorted(keywords):
            where = cover.get(kw) or ("not yet" if kw in later else "MISSING")
            print(f"{kw:14} {where}")
    problems = check(keywords, cover, later, not_yet_at_head(ROOT))
    for p in problems:
        print(f"cookbook coverage: {p}", file=sys.stderr)
    print(
        f"cookbook coverage: {len(keywords)} naqsh statement keywords; "
        f"{len(set(cover) & keywords)} have a recipe, {len(later & keywords)} not yet"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
