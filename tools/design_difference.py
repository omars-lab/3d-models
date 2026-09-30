#!/usr/bin/env python3
"""How different a coaster candidate is from the coasters already made, and the
weighted total the prioritize-design skill ranks by.

    python3 tools/design_difference.py table [--candidate ID ...]
    python3 tools/design_difference.py rank --scores <scores.md>
    python3 tools/design_difference.py check
    python3 tools/design_difference.py --self-test

Four facts per design, read from the table in .claude/skills/prioritize-design/scoring.md:
fold family, layout, outline, lines. Two designs are as similar as the share of the four
facts they have in common (0, 0.25, 0.5, 0.75 or 1). A candidate's **difference** is 1 minus
its average similarity to every made coaster: Hekkert's measure of how typical a thing is,
with the made coasters as the category. The made set is read from the constructions ledger
(docs/constructions/ledger.md): every row with a vendored coaster. That is why the score
must be recomputed after every pick; the next coaster made changes every other candidate's
difference.

`table` prints, per candidate: the four facts, the difference, the nearest made coaster
with its similarity, and the "same source as" note from the facts table (what the four
facts cannot see, e.g. two patterns from the same monument).

`rank` reads a markdown table of judged scores (columns `id`, `appeal` 0–8, `unusual` 0–2,
and optionally `ready` yes/no and `rebuild` 0–1) and prints the total each candidate gets:
appeal + 5 × difference + unusual ÷ 2 (D-085), highest first, ties broken on `ready` then
`rebuild`. The weights are a guess and live at the top of this file, so a round that moves
them changes one line.

`check` is what the pre-commit hook runs: every made coaster in the ledger has a facts row,
every fact value is one the scoring file allows, and no id appears twice. It fails naming
each missing id (D-086: the facts live in the scoring file, not the ledger, so the tool
must catch the drift itself). `table` and `rank` run it first.

Validator (prioritize-design design, section 4.3): a coaster already in the made set,
scored as a candidate, shows itself as nearest at 1.00 and has a lower difference than any
candidate. The self-test holds that, plus the failing shape: a tool that drops the
candidate's own row shows its nearest below 1.00. Only the standard library is needed.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTS_FILE = ROOT / ".claude" / "skills" / "prioritize-design" / "scoring.md"
LEDGER_FILE = ROOT / "docs" / "constructions" / "ledger.md"

# The four facts and the values each may take. A value outside these is a typo, and a typo
# would silently score as "different from everything".
FACTS = ("fold family", "layout", "outline", "lines")
ALLOWED = {
    "fold family": {"4/8", "3/6/12", "5/10", "7", "9/18"},
    "layout": {"centre", "tile", "field cut"},
    "outline": {"round", "hexagon", "square", "octagon", "heptagon", "rhombus", "rectangle"},
    "lines": {"straight", "arcs", "woven"},
}

# D-085: appeal + 5 × difference + unusual ÷ 2. Both weights are a guess (the design says so);
# a round that moves them changes these two numbers and says why in the round log.
DIFFERENCE_WEIGHT = 5.0
UNUSUAL_WEIGHT = 0.5

_ID = re.compile(r"`([^`]+)`(?:\s+(\S.*))?")


def _rows(text, required):
    """Every row of the first markdown table whose header holds all `required` columns,
    as dicts keyed by the header's lower-cased cell text."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        header = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if not all(col in header for col in required):
            continue
        rows = []
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if len(cells) != len(header):
                raise SystemExit(f"table row has {len(cells)} cells, header {len(header)}: {row}")
            rows.append(dict(zip(header, cells)))
        return rows
    raise SystemExit(f"no table with columns {required}")


def load_facts(path=FACTS_FILE):
    """The facts table: {key: {fact: value, 'id': base id, 'variant': str, 'catalog': ..,
    'sell': .., 'source': ..}}. The key is the id, plus the variant word when the row is a
    variant of a made pattern (`` `NtnlGMTElBk` woven ``)."""
    facts = {}
    problems = []
    for row in _rows(path.read_text(encoding="utf-8"), ("id", *FACTS)):
        m = _ID.fullmatch(row["id"])
        if not m:
            problems.append(f"id cell is not `id` [variant]: {row['id']}")
            continue
        base, variant = m.group(1), (m.group(2) or "").strip()
        key = f"{base} {variant}".strip()
        if key in facts:
            problems.append(f"{key}: listed twice")
        for fact in FACTS:
            if row[fact] not in ALLOWED[fact]:
                problems.append(
                    f"{key}: {fact} {row[fact]!r} is not one of {sorted(ALLOWED[fact])}"
                )
        facts[key] = {
            "id": base,
            "variant": variant,
            "catalog": row.get("catalog", ""),
            "sell": row.get("sell", ""),
            "source": row.get("same source as", ""),
            **{fact: row[fact] for fact in FACTS},
        }
    return facts, problems


def load_made(path=LEDGER_FILE):
    """Ids of every ledger row with a vendored coaster, and the ids done in youtube with no
    coaster yet (the pool a candidate is usually drawn from)."""
    made, pool = [], []
    for row in _rows(path.read_text(encoding="utf-8"), ("id", "coaster", "youtube")):
        m = _ID.fullmatch(row["id"])
        if not m:
            continue
        if "src/Coasters/" in row["coaster"]:
            made.append(m.group(1))
        elif row["youtube"] == "done" and "by design" not in row["coaster"]:
            pool.append(m.group(1))
    return made, pool


def similarity(a, b):
    return sum(a[f] == b[f] for f in FACTS) / len(FACTS)


def score(candidate, made_rows):
    """(difference, nearest key, nearest similarity) of one facts row against the made rows.
    The candidate's own row, when it is made, stays in: that is the Validator."""
    if not made_rows:
        raise SystemExit("no made coasters to compare with")
    sims = {key: similarity(candidate, row) for key, row in made_rows.items()}
    nearest = max(sims, key=lambda k: (sims[k], k == candidate.get("_key"), k))
    return 1 - sum(sims.values()) / len(sims), nearest, sims[nearest]


def check(facts, problems, made, wanted=()):
    """Fail naming every made coaster and every wanted candidate without a facts row."""
    missing = [i for i in made if i not in facts]
    if missing:
        problems.append(
            "made coasters with no row in the four-facts table: " + ", ".join(missing)
        )
    absent = [w for w in wanted if w not in facts]
    if absent:
        problems.append("candidates to rank with no row in the four-facts table: " + ", ".join(absent))
    if problems:
        raise SystemExit("design_difference: " + "\n  ".join(["", *problems]))


def split(facts, made):
    """Made rows are the made ids without a variant; everything else is a candidate."""
    made_rows = {k: r for k, r in facts.items() if r["id"] in made and not r["variant"]}
    candidates = {k: r for k, r in facts.items() if k not in made_rows}
    return made_rows, candidates


def difference_table(facts, made, keys=None):
    made_rows, candidates = split(facts, made)
    keys = keys or sorted(candidates)
    out = []
    for key in keys:
        row = dict(facts[key], _key=key)
        diff, nearest, sim = score(row, made_rows)
        out.append((key, row, diff, nearest, sim))
    out.sort(key=lambda t: (-t[2], t[0]))
    return out, made_rows


def fmt_table(rows, made_rows):
    lines = [
        "| id | catalog | fold | layout | outline | lines | difference | nearest made | same source as | sell |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for key, row, diff, nearest, sim in rows:
        near = made_rows[nearest]["catalog"] or nearest
        lines.append(
            f"| {key} | {row['catalog']} | {row['fold family']} | {row['layout']} | "
            f"{row['outline']} | {row['lines']} | {diff:.2f} | {near}, {sim:.2f} | "
            f"{row['source']} | {row['sell']} |"
        )
    return "\n".join(lines)


def load_scores(path):
    rows = _rows(Path(path).read_text(encoding="utf-8"), ("id", "appeal", "unusual"))
    scores = {}
    for row in rows:
        m = _ID.fullmatch(row["id"]) or re.fullmatch(r"(\S+)(?:\s+(\S.*))?", row["id"])
        key = f"{m.group(1)} {(m.group(2) or '').strip()}".strip()
        scores[key] = {
            "appeal": float(row["appeal"]),
            "unusual": float(row["unusual"]),
            "ready": row.get("ready", "").strip().lower() == "yes",
            "rebuild": float(row["rebuild"]) if row.get("rebuild", "").strip() else 0.0,
        }
    return scores


def total(appeal, difference, unusual):
    """From the difference as printed (two places), so the total on the page can be checked
    by hand from the numbers beside it: 7 + 5 × 0.61 + 2 ÷ 2 = 11.05, not 11.06."""
    return appeal + DIFFERENCE_WEIGHT * round(difference, 2) + UNUSUAL_WEIGHT * unusual


def rank(facts, made, scores):
    rows, made_rows = difference_table(facts, made, list(scores))
    ranked = []
    for key, row, diff, nearest, sim in rows:
        s = scores[key]
        ranked.append((total(s["appeal"], diff, s["unusual"]), s, key, row, diff, nearest, sim))
    ranked.sort(key=lambda t: (-t[0], not t[1]["ready"], -t[1]["rebuild"], t[2]))
    lines = [
        "| rank | id | appeal | unusual | difference | nearest made | total | ready | rebuild | sell |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for n, (tot, s, key, row, diff, nearest, sim) in enumerate(ranked, 1):
        near = made_rows[nearest]["catalog"] or nearest
        lines.append(
            f"| {n} | {key} | {s['appeal']:g} | {s['unusual']:g} | {diff:.2f} | {near}, {sim:.2f} | "
            f"**{tot:.2f}** | {'yes' if s['ready'] else 'no'} | {s['rebuild']:.3f} | {row['sell']} |"
        )
    lines.append("")
    lines.append(
        f"total = appeal + {DIFFERENCE_WEIGHT:g} × difference + {UNUSUAL_WEIGHT:g} × unusual "
        f"(D-085); ties: ready, then rebuild. Made set: {len(made_rows)} coasters."
    )
    return "\n".join(lines)


# --- self-test -------------------------------------------------------------------------

_NINE = """
| id | catalog | fold family | layout | outline | lines |
|---|---|---|---|---|---|
| `GimTvN9hw4U` | CS-1 | 3/6/12 | centre | hexagon | straight |
| `7apC5Q9QS-8` | CS-2 | 4/8 | centre | square | straight |
| `tA8eSdVx_EQ` | CS-6 | 7 | centre | heptagon | straight |
| `lEfWSogWscs` | CS-7 | 4/8 | centre | octagon | straight |
| `rDuxHF3xMOc` | CS-8 | 4/8 | tile | square | straight |
| `nmEjCTzMbDg` | CS-9 | 9/18 | centre | round | arcs |
| `n3IidKfXE1I` | CS-10 | 3/6/12 | centre | round | straight |
| `sDO9fpu76v8` | CS-11 | 3/6/12 | tile | hexagon | straight |
| `bknVRSMcLj0` | CS-12 | 3/6/12 | tile | round | straight |
| `n_ICgwOr6qs` | | 5/10 | centre | round | arcs |
| `Y6kS1MvnKoc` | | 5/10 | field cut | round | straight |
| `_U6G8QSfWnk` | | 5/10 | tile | rectangle | straight |
| `gBV_JTt3Kxk` | | 5/10 | centre | rhombus | straight |
| `jlTmt_279M4` | | 7 | tile | square | straight |
| `fhGHzop7ULw` | | 3/6/12 | tile | rectangle | straight |
| `NtnlGMTElBk` | | 5/10 | centre | round | straight |
| `A9fefFurD_s` | | 5/10 | centre | round | straight |
"""
_NINE_MADE = ["GimTvN9hw4U", "7apC5Q9QS-8", "tA8eSdVx_EQ", "lEfWSogWscs", "rDuxHF3xMOc",
              "nmEjCTzMbDg", "n3IidKfXE1I", "sDO9fpu76v8", "bknVRSMcLj0"]
# The design's own worked numbers (prioritize-design, section 4.3 and researcher B's table):
# the tool must reproduce the doc it implements.
_EXPECTED = {"n_ICgwOr6qs": (0.72, "nmEjCTzMbDg", 0.75), "Y6kS1MvnKoc": (0.69, "n3IidKfXE1I", 0.50),
             "_U6G8QSfWnk": (0.69, "rDuxHF3xMOc", 0.50), "gBV_JTt3Kxk": (0.61, "rDuxHF3xMOc", 0.50),
             "jlTmt_279M4": (0.61, "rDuxHF3xMOc", 0.75), "fhGHzop7ULw": (0.58, "sDO9fpu76v8", 0.75),
             "NtnlGMTElBk": (0.53, "n3IidKfXE1I", 0.75), "A9fefFurD_s": (0.53, "n3IidKfXE1I", 0.75)}


def self_test():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "facts.md"
        p.write_text(_NINE, encoding="utf-8")
        facts, problems = load_facts(p)
        assert not problems, problems
        made_rows, candidates = split(facts, _NINE_MADE)
        assert len(made_rows) == 9 and len(candidates) == 8

        # PASS: CS-2 scored as a candidate against the nine, its own row kept in.
        cs2 = dict(facts["7apC5Q9QS-8"], _key="7apC5Q9QS-8")
        diff, nearest, sim = score(cs2, made_rows)
        assert nearest == "7apC5Q9QS-8" and sim == 1.0, (nearest, sim)
        rows, _ = difference_table(facts, _NINE_MADE)
        assert all(diff < d for _, _, d, _, _ in rows), "CS-2 must differ less than any candidate"

        # The doc's worked example, to two places.
        for key, row, d, near, s in rows:
            e_diff, e_near, e_sim = _EXPECTED[key]
            assert round(d, 2) == e_diff, (key, d, e_diff)
            assert s == e_sim, (key, s, e_sim)
            # B's nearest is one of the ties; ours must be at least as similar.
            assert similarity(row, facts[e_near]) <= s, (key, near, e_near)

        # FAIL: the tool that leaves the candidate's own row out shows nearest below 1.00.
        without = {k: r for k, r in made_rows.items() if k != "7apC5Q9QS-8"}
        _, nearest, sim = score(cs2, without)
        assert sim < 1.0, "own row omitted must not read as 1.00"
        # ... and with only three facts that same wrong tool would read CS-7 as identical,
        # which is why all four are compared.
        assert len(FACTS) == 4
        three = [f for f in FACTS if f != "outline"]
        assert sum(cs2[f] == facts["lEfWSogWscs"][f] for f in three) == 3

        # check: a made coaster without a row fails naming it.
        try:
            check(facts, [], _NINE_MADE + ["missing-id"])
        except SystemExit as e:
            assert "missing-id" in str(e), e
        else:
            raise AssertionError("check must fail on a made coaster with no row")

        # check: a value outside the allowed set fails naming the row.
        p.write_text(_NINE.replace("| `A9fefFurD_s` | | 5/10 |", "| `A9fefFurD_s` | | 10 |"),
                     encoding="utf-8")
        _, problems = load_facts(p)
        assert problems and "A9fefFurD_s" in problems[0], problems

        # rank: the weighted total and its tie-break on readiness.
        p.write_text(_NINE, encoding="utf-8")
        facts, _ = load_facts(p)
        s = Path(tmp) / "scores.md"
        s.write_text(
            "| id | appeal | unusual | ready | rebuild |\n|---|---|---|---|---|\n"
            "| `jlTmt_279M4` | 7 | 2 | yes | 0.941 |\n| `gBV_JTt3Kxk` | 7 | 2 | no | 0.906 |\n"
            "| `NtnlGMTElBk` | 6 | 2 | yes | 0.930 |\n",
            encoding="utf-8",
        )
        out = rank(facts, _NINE_MADE, load_scores(s))
        assert "| 1 | jlTmt_279M4 |" in out and "| 2 | gBV_JTt3Kxk |" in out, out
        assert "**11.05**" in out and "**9.65**" in out, out
    print("design_difference: self-test ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--facts", type=Path, default=FACTS_FILE)
    ap.add_argument("--ledger", type=Path, default=LEDGER_FILE)
    sub = ap.add_subparsers(dest="cmd")
    t = sub.add_parser("table", help="difference and nearest made coaster per candidate")
    t.add_argument("--candidate", action="append", default=[], help="rank only these (repeatable)")
    r = sub.add_parser("rank", help="the D-085 total per candidate from a judged-scores table")
    r.add_argument("--scores", required=True, help="markdown table: id | appeal | unusual [| ready | rebuild]")
    sub.add_parser("check", help="every made coaster has a facts row; every value is allowed")
    args = ap.parse_args(argv)

    if args.self_test:
        self_test()
        return 0
    if not args.cmd:
        ap.print_help()
        return 2

    facts, problems = load_facts(args.facts)
    made, pool = load_made(args.ledger)
    wanted = getattr(args, "candidate", [])
    scores = load_scores(args.scores) if args.cmd == "rank" else {}
    check(facts, problems, made, list(wanted) + list(scores))

    if args.cmd == "check":
        unscored = [i for i in pool if i not in facts]
        print(f"design_difference: {len(made)} made coasters, all with facts; "
              f"{len(facts) - len(made)} candidate rows")
        if unscored:
            print("  ledger rows done in youtube with no facts row yet (add one before ranking): "
                  + ", ".join(unscored))
        return 0
    if args.cmd == "table":
        rows, made_rows = difference_table(facts, made, wanted or None)
        print(fmt_table(rows, made_rows))
        print(f"\nMade set from the ledger: {len(made_rows)} coasters.")
        return 0
    print(rank(facts, made, scores))
    return 0


if __name__ == "__main__":
    sys.exit(main())
