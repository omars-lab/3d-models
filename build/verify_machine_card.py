#!/usr/bin/env python3
"""Render the machine card and check every rung against its own design doc.

`docs/calibration-design.md` §7 ships a full expectation table — euler,
watertight, degenerate count, minFeature, `--check` verdict, triangles,
volume — for all 23 rungs. This script renders the card per §6 and diffs the
actual gate output against that table. The doc is the spec; nothing here
restates a number the doc already states.

Two things make this a gate rather than a smoke test:

  1. **Four rungs are expected to FAIL.** MC2Wall04/06/08/10 sit under the
     1.2 mm feature floor on purpose (§3.1) — that is what the wall ladder is
     *for*. A verifier that demanded "everything PASSes" would either be wrong
     about those four or would have to skip them, and CLAUDE.md is explicit
     that a gate which cries wolf gets switched off. So each of those four is
     rendered twice: once without `--check` to write the STL that §6 asks for,
     and once *with* `--check` to assert the failure the doc predicts, with
     the minFeature the doc predicts. A silent PASS there is a defect.

  2. **The piece set is cross-checked three ways.** §6's shell block, §7's
     table, and this script must name the same rungs. That is the K7 read-the-
     doc-against-itself check, mechanised: editing one and not the others
     fails here instead of shipping.

Usage:  python3 build/verify_machine_card.py [--bikar-dir DIR] [--out DIR]
        python3 build/verify_machine_card.py --self-test
Exit 0 if every rung matches the table, 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "calibration-design.md"
CARD = "patterns/Coupons/Machine-Card.bkr"

MESH_RE = re.compile(
    r"mesh gate: watertight=(?P<wt>\S+) euler=(?P<euler>-?\d+) "
    r"degenerate=(?P<degen>\d+) minFeature=(?P<minf>[\d.eE+-]+)mm "
    r"\(floor [\d.]+mm\) — (?P<verdict>PASS|FAIL)"
)
STL_RE = re.compile(
    r"STL written to \S+ \((?P<tris>\d+) triangles, [\d.]+ \w+, "
    r"volume (?P<vol>[\d.]+) cm³\)"
)
PRINT_RE = re.compile(r"print gate: .*? warn=(?P<warn>\d+) — (?P<verdict>PASS|FAIL)")

# The three verdicts §7's `--check` column is allowed to hold, and what each
# one means operationally. Anything else in that column is a doc error.
PASS = "PASS"
PASS_WARN = "PASS (+F7 warn)"
FAIL_BY_DESIGN = "FAIL — by design"


def parse_doc(text: str) -> tuple[list[dict], set[str], int, float]:
    """Pull §7's expectation table, §6's piece set, and the stated totals."""
    rows = []
    for m in re.finditer(
        r"^\| `(MC\w+)` \| (−?-?\d+) \| (\w+) \| (\d+) \| ([\d.]+) \| (.+?) \| "
        r"(\d+) \| ([\d.]+) \|$",
        text,
        re.M,
    ):
        piece, euler, wt, degen, minf, check, tris, vol = m.groups()
        rows.append(
            {
                "piece": piece,
                # the doc uses U+2212 MINUS SIGN, which int() will not take
                "euler": int(euler.replace("−", "-")),
                "watertight": wt,
                "degenerate": int(degen),
                "minfeature": minf,  # kept as text: its precision is the tolerance
                "check": check.replace("**", "").strip(),
                "tris": int(tris),
                "vol": vol,
            }
        )

    # §6's shell block — every `--piece X` and every `for P in ...` list.
    # Comments are stripped first: §6 names MC1FitGaugePress/Sliding/Free in a
    # comment precisely to say they are *not* rendered, and reading that as a
    # command line makes the cross-check fire on a doc that is correct.
    block = re.search(r"## 6\. Render commands.*?```sh\n(.*?)```", text, re.S)
    if not block:
        sys.exit("could not find §6's shell block in the doc")
    code_only = "\n".join(
        line for line in block.group(1).splitlines() if not line.lstrip().startswith("#")
    )
    in_six = set(re.findall(r"\bMC\d\w+", code_only))

    total = re.search(
        r"\*\*Total solid volume across all (\d+) pieces: ([\d.]+) cm³\*\*", text
    )
    if not total:
        sys.exit("could not find §7's stated total volume")
    return rows, in_six, int(total.group(1)), float(total.group(2))


def run(bikar_dir: Path, args: list[str]) -> tuple[int, str]:
    cli = bikar_dir / "packages" / "cli" / "dist" / "index.js"
    p = subprocess.run(
        ["node", str(cli), "render", CARD, "--format", "stl", *args],
        cwd=bikar_dir,
        capture_output=True,
        text=True,
    )
    return p.returncode, p.stdout + p.stderr


def check_mode(piece: str, expected_check: str) -> list[str]:
    """§6's rule for which gate a rung runs under, in one place."""
    if piece.startswith("MC6"):
        return ["--check", "print"]  # bed contact exercises F7 — the bet under test
    if expected_check == FAIL_BY_DESIGN:
        return []  # §6 renders these bare; the FAIL is asserted separately
    return ["--check"]


def num_eq(expected: str, actual: str) -> bool:
    """Compare at the precision the doc chose to state — '5.000' vs 4.99999997."""
    places = len(expected.split(".")[1]) if "." in expected else 0
    try:
        return f"{float(actual):.{places}f}" == f"{float(expected):.{places}f}"
    except ValueError:
        return False


def verify(row: dict, bikar_dir: Path, out: Path, tmp: Path) -> list[str]:
    piece, want = row["piece"], row["check"]
    bad: list[str] = []
    dest = out / f"{piece}.stl"
    code, log = run(
        bikar_dir, [*check_mode(piece, want), "--piece", piece, "-o", str(dest)]
    )

    stl = STL_RE.search(log)
    if not stl:
        return [f"{piece}: no STL written (exit {code})\n{log.strip()}"]
    if int(stl["tris"]) != row["tris"]:
        bad.append(f"{piece}: tris {stl['tris']} ≠ doc {row['tris']}")
    if stl["vol"] != row["vol"]:
        bad.append(f"{piece}: volume {stl['vol']} ≠ doc {row['vol']} cm³")

    if want == FAIL_BY_DESIGN:
        # The whole point of the wall ladder: prove the floor actually rejects
        # these, at the minFeature the doc names. A PASS here is the defect.
        code, log = run(
            bikar_dir,
            ["--check", "--piece", piece, "-o", str(tmp / f"{piece}.stl")],
        )
        if code == 0:
            bad.append(f"{piece}: --check succeeded; doc says it must FAIL by design")

    mesh = MESH_RE.search(log)
    if not mesh:
        return bad + [f"{piece}: no mesh-gate line\n{log.strip()}"]

    verdict = FAIL_BY_DESIGN if mesh["verdict"] == "FAIL" else PASS
    if want == PASS_WARN:
        pg = PRINT_RE.search(log)
        if not pg:
            bad.append(f"{piece}: doc expects a print gate, none ran")
        elif pg["verdict"] != "PASS" or int(pg["warn"]) < 1:
            bad.append(
                f"{piece}: print gate {pg['verdict']} warn={pg['warn']}; "
                f"doc says PASS with an F7 warning"
            )
        elif "F7:" not in log:
            bad.append(f"{piece}: warn raised but it is not F7; doc names F7")
        verdict = PASS_WARN if mesh["verdict"] == "PASS" else FAIL_BY_DESIGN
    elif piece.startswith("MC6"):
        pg = PRINT_RE.search(log)
        if pg and int(pg["warn"]) != 0:
            bad.append(f"{piece}: print gate warn={pg['warn']}; doc says a clean PASS")

    if verdict != want:
        bad.append(f"{piece}: --check {verdict} ≠ doc {want}")
    if mesh["wt"] != ("true" if row["watertight"] == "yes" else "false"):
        bad.append(f"{piece}: watertight={mesh['wt']} ≠ doc {row['watertight']}")
    if int(mesh["euler"]) != row["euler"]:
        bad.append(f"{piece}: euler {mesh['euler']} ≠ doc {row['euler']}")
    if int(mesh["degen"]) != row["degenerate"]:
        bad.append(f"{piece}: degenerate {mesh['degen']} ≠ doc {row['degenerate']}")
    if not num_eq(row["minfeature"], mesh["minf"]):
        bad.append(f"{piece}: minFeature {mesh['minf']} ≠ doc {row['minfeature']}")

    row["actual_vol"] = float(stl["vol"])
    return bad


def run_verification(
    doc: Path, bikar_dir: Path, out: Path, only: set[str] | None, quiet: bool = False
) -> int:
    rows, in_six, doc_count, doc_total = parse_doc(doc.read_text(encoding="utf-8"))
    in_seven = {r["piece"] for r in rows}

    problems: list[str] = []
    if in_six != in_seven:
        problems.append(
            f"§6 and §7 disagree on the piece set: "
            f"only in §6 {sorted(in_six - in_seven)}, only in §7 {sorted(in_seven - in_six)}"
        )
    if len(rows) != doc_count:
        problems.append(f"§7 has {len(rows)} rows but claims {doc_count} pieces")

    if only:
        rows = [r for r in rows if r["piece"] in only]
    out.mkdir(parents=True, exist_ok=True)
    if not quiet:
        print(f"machine card → {out}  ({len(rows)} rungs, bikar {bikar_dir})")

    with tempfile.TemporaryDirectory() as td:
        for row in rows:
            bad = verify(row, bikar_dir, out, Path(td))
            if not quiet:
                mark = "ok  " if not bad else "FAIL"
                note = "" if row["check"] == PASS else f"   [{row['check']}]"
                print(f"  {mark} {row['piece']:<15} {row['check']:<16}{note}")
            problems.extend(bad)

    got = round(sum(r.get("actual_vol", 0.0) for r in rows), 1)
    # A subset cannot discharge a claim about the whole card, so the total is
    # only checked on a full run.
    if not only and abs(got - doc_total) > 0.05:
        problems.append(f"total volume {got} cm³ ≠ §7's stated {doc_total} cm³")

    if problems:
        if not quiet:
            print(f"\n{len(problems)} mismatch(es) against {doc.name} §7:")
            for p in problems:
                print(f"  - {p}")
        return 1
    if not quiet:
        tail = "" if only else f"; total volume {got} cm³ as stated"
        print(f"\nall {len(rows)} rungs match §7{tail}")
    return 0


# Each case names one way the doc and the geometry can drift apart, and the
# rung that is cheapest to prove it on. `None` means the case fires during
# parsing and needs a rung only to have something to render.
SELF_TEST_CASES = [
    (
        "triangle count drifts",
        ("| `MC1Pin03` | 2 | yes | 0 | 3 | PASS | 256 | 0.1 |",
         "| `MC1Pin03` | 2 | yes | 0 | 3 | PASS | 257 | 0.1 |"),
        "MC1Pin03",
    ),
    (
        "euler drifts",
        ("| `MC1Pin04` | 2 | yes | 0 | 4 | PASS | 256 | 0.2 |",
         "| `MC1Pin04` | 4 | yes | 0 | 4 | PASS | 256 | 0.2 |"),
        "MC1Pin04",
    ),
    (
        "minFeature drifts",
        ("| `MC1Pin05` | 2 | yes | 0 | 5 | PASS | 256 | 0.3 |",
         "| `MC1Pin05` | 2 | yes | 0 | 5.5 | PASS | 256 | 0.3 |"),
        "MC1Pin05",
    ),
    (
        # The hard case. If someone 'tidies' the by-design FAIL into a PASS,
        # the wall ladder silently stops testing the feature floor.
        "a by-design FAIL is relabelled PASS",
        ("| `MC2Wall04` | 0 | yes | 0 | 0.40 | **FAIL — by design** | 768 | 0.2 |",
         "| `MC2Wall04` | 0 | yes | 0 | 0.40 | PASS | 768 | 0.2 |"),
        "MC2Wall04",
    ),
    (
        # ...and the reverse: a rung that really does pass must not be able to
        # hide behind the by-design label.
        "a passing rung is labelled FAIL by design",
        ("| `MC2Wall20` | 0 | yes | 0 | 2.00 | PASS | 768 | 1.3 |",
         "| `MC2Wall20` | 0 | yes | 0 | 2.00 | **FAIL — by design** | 768 | 1.3 |"),
        "MC2Wall20",
    ),
    (
        "§6 renders a rung §7 does not tabulate",
        ("for P in MC2Wall12 MC2Wall16 MC2Wall20; do",
         "for P in MC2Wall12 MC2Wall16 MC2Wall20 MC2Wall99; do"),
        "MC1Pin06",
    ),
    (
        "the F7 warning MC-6 is built to raise stops being expected",
        ("| `MC6Tower03` | 2 | yes | 0 | 3 | PASS (+F7 warn) | 256 | 0.3 |",
         "| `MC6Tower03` | 2 | yes | 0 | 3 | PASS | 256 | 0.3 |"),
        "MC6Tower03",
    ),
]


def self_test(bikar_dir: Path) -> int:
    """Prove the gate fires. A gate nobody has watched fail is not a gate."""
    src = DOC.read_text(encoding="utf-8")
    failures = []
    with tempfile.TemporaryDirectory() as td:
        out, tmpdoc = Path(td) / "stls", Path(td) / "calibration-design.md"

        tmpdoc.write_text(src, encoding="utf-8")
        code = run_verification(tmpdoc, bikar_dir, out, {"MC1Pin03"}, quiet=True)
        print(f"  {'ok  ' if code == 0 else 'FAIL'} unmutated doc passes")
        if code != 0:
            failures.append("unmutated doc does not pass")

        for name, (old, new), piece in SELF_TEST_CASES:
            if old not in src:
                failures.append(f"{name}: fixture text no longer in the doc")
                print(f"  FAIL {name} (fixture is stale)")
                continue
            tmpdoc.write_text(src.replace(old, new, 1), encoding="utf-8")
            code = run_verification(tmpdoc, bikar_dir, out, {piece}, quiet=True)
            print(f"  {'ok  ' if code == 1 else 'FAIL'} fires when {name}")
            if code != 1:
                failures.append(f"gate did not fire when {name}")

    if failures:
        print(f"\nself-test: {len(failures)} case(s) the gate would miss:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"\nself-test: all {len(SELF_TEST_CASES) + 1} cases behave as documented")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bikar-dir", default=os.environ.get("BIKAR_DIR", ""))
    ap.add_argument("--out", default=str(ROOT / "build/stls/coupons/machine-card"))
    ap.add_argument("--doc", default=str(DOC))
    ap.add_argument("--only", action="append", metavar="PIECE")
    ap.add_argument(
        "--self-test", action="store_true", help="mutate the doc and check the gate fires"
    )
    args = ap.parse_args()

    bikar_dir = Path(args.bikar_dir or Path.home() / "Workspace/git/bikar").resolve()
    cli = bikar_dir / "packages/cli/dist/index.js"
    if not cli.exists():
        print(f"bikar CLI not built — run 'npm run build' in {bikar_dir}")
        return 1

    if args.self_test:
        return self_test(bikar_dir)
    return run_verification(
        Path(args.doc), bikar_dir, Path(args.out), set(args.only) if args.only else None
    )


if __name__ == "__main__":
    sys.exit(main())
