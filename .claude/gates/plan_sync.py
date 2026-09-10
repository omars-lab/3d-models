#!/usr/bin/env python3
"""Plan-sync gate for 3d-models: §2 and §3 of docs/plan.md move together.

docs/plan.md is the index of record. §2 is the priority queue — one numbered
row (`2.N`) per work item, carrying a State mark. §3 is the shipped log —
newest first, each row citing the queue item it discharges as `(2.N)`. The
standing rule this gate replaces read: *"every PR that moves a §2 row updates
§2/§3 in the same PR."* It lived as a remembered task (#50) that every future
PR had to honour by hand — precisely the "defensible argument that management
is occurring" that docs/issue-register-evaluation.md rejects. A remembered rule
is not a checked one.

The naive gate is a wolf-crier, and it was measured before this one was written
(the method issue-register-evaluation.md §5.1 and counts_gate.py both use).
The obvious invariant — "every §2 row marked 🟢 shipped appears in §3" — was run
against the live, well-maintained file on 2026-09-10:

    §2 rows marked 🟢:                 16
    of those, cited nowhere in §3:     10   (~63% false-alarm rate)

Every one of the ten is *correct*, for three legitimate reasons:

  * an aggregate row (2.2, the explorer ledger) is discharged in §3 by its four
    §6.6 sub-rows, not by a `(2.2)` tag;
  * a decomposed row (2.1 with sub-rows 2.1.a–f) is discharged by one "d3 Phase
    2 shipped" §3 row, not seven;
  * a descriptive §3 row ("d3 Phase 3 shipped (Q-VOCAB)" for 2.4) records the
    ship in prose without the `(2.N)` back-reference.

A resting-state gate that fired on those would be switched off inside a week —
"a gate that cries wolf gets switched off, which is worse than having no gate"
(CLAUDE.md). So the sync rule is **not** a claim about the file at rest. It is a
claim about a *transition*: the task says "the PR that **moves** a row." A move
is a diff, so the check is a diff. Firing only when a row crosses **into** 🟢
in this very commit, the ten resting rows are invisible and the false-alarm rate
on the live file is zero.

Rules:

  PS1  Forward referential integrity (resting). Every `(2.N)` cited in §3
       resolves to a row `| 2.N |` present in §2. Catches a §3 row left
       pointing at a queue item that a renumber moved or removed — the exact
       shape of the decision-id renumber that D-052 had to sweep corpus-wide.

  PS2  Legal state marks (resting). Every §2 data row (`| 2.N | …`) carries
       exactly one of the five legal marks in its State column. Catches an
       empty or fat-fingered State cell that would make PS3 and §6's
       read-against-itself checks silently blind to the row.

  PS3  Ship-in-the-same-commit (diff, pre-commit only). If the staged plan.md
       moves one or more §2 rows **into** 🟢 relative to HEAD, the staged §3
       shipped table must have gained at least one data row over HEAD. One new
       §3 row discharges any number of rows flipped together (the 2.1.a–f
       aggregate is why this is ≥1, not one-per-flip). This is the whole of the
       old task #50, now enforced rather than remembered.

The load-bearing failure — CLAUDE.md's "the by-design failure is the
load-bearing case" — is a commit that flips a row to 🟢 and adds no §3 row.
--self-test builds a clean two-revision fixture, requires it to pass, then
mutates it once per rule and requires each mutation to fire, including that PS3
failure and its passing twin (same flip + a new §3 row).

Modes:

  plan_sync.py                 resting invariants (PS1, PS2) over the working
                               tree. The wholesale form `make validate-plan-sync`
                               runs this; there is no diff over the whole tree,
                               so PS3 is a no-op there by construction.
  plan_sync.py --pre-commit    invoked by the hook. If docs/plan.md is not
                               staged the commit does not touch it and the gate
                               exits 0. Otherwise PS1/PS2 run over the *staged*
                               content and PS3 runs over HEAD→staged.
  plan_sync.py --self-test     fixtures; every by-design failure must fire.

Override once, for a deliberate exception (a renumber that reshuffles states, a
ship whose §3 record is landing in a follow-up): PLAN_SYNC_OK=1 git commit.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PLAN = "docs/plan.md"

GREEN = "🟢"
STATES = ("🟢", "🔵", "⚪", "🟡", "🔴")
_STATE_ALT = "|".join(re.escape(s) for s in STATES)

# A §2 data row: `| 2.N | Item… | STATE | …`. The lazy `.*?` spans the Item
# column up to the State column (the third field). Sub-rows like 2.1.a match.
_ROW = re.compile(rf"^\|\s*(2\.[0-9a-z.]+)\s*\|.*?\|\s*({_STATE_ALT})\s*\|")
# A §2 row present but with an unparseable/illegal State cell (for PS2).
_ROW_ANY = re.compile(r"^\|\s*(2\.[0-9a-z.]+)\s*\|")
# A §3 back-reference to a queue item.
_CITE = re.compile(r"\((2\.[0-9a-z.]+)\)")


def _section(lines: list[str], n: int) -> tuple[int, int]:
    """Return (start, end) line indices for `## n.` up to the next `## `."""
    start = None
    for i, ln in enumerate(lines):
        if re.match(rf"^##\s+{n}\.", ln):
            start = i
            break
    if start is None:
        return (-1, -1)
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s+\d+\.", lines[j]):
            return (start, j)
    return (start, len(lines))


def _s2(lines: list[str]) -> list[str]:
    a, b = _section(lines, 2)
    return lines[a:b] if a >= 0 else []


def _s3(lines: list[str]) -> list[str]:
    a, b = _section(lines, 3)
    return lines[a:b] if a >= 0 else []


def s2_rows(text: str) -> list[tuple[int, str, str]]:
    """(lineno, number, state) for every parseable §2 data row."""
    lines = text.splitlines()
    out = []
    a, _ = _section(lines, 2)
    for k, ln in enumerate(_s2(lines)):
        m = _ROW.match(ln)
        if m:
            out.append((a + k + 1, m.group(1), m.group(2)))
    return out


def s2_rows_missing_state(text: str) -> list[tuple[int, str]]:
    """(lineno, number) for §2 rows present but without a legal State mark."""
    lines = text.splitlines()
    a, _ = _section(lines, 2)
    out = []
    for k, ln in enumerate(_s2(lines)):
        if _ROW_ANY.match(ln) and not _ROW.match(ln):
            out.append((a + k + 1, _ROW_ANY.match(ln).group(1)))
    return out


def s3_citations(text: str) -> set[str]:
    return {m.group(1) for ln in _s3(text.splitlines()) for m in _CITE.finditer(ln)}


def s3_data_rows(text: str) -> int:
    """Count data rows in §3's table (pipe-lines after the `|---|` separator)."""
    seen_sep = False
    n = 0
    for ln in _s3(text.splitlines()):
        s = ln.strip()
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[\s:|-]+\|?\s*$", s):  # the `|---|---|` separator
            seen_sep = True
            continue
        if seen_sep:
            n += 1
    return n


def green_set(text: str) -> set[str]:
    return {num for _, num, st in s2_rows(text) if st == GREEN}


def check_resting(text: str, label: str) -> list[str]:
    """PS1 + PS2 over one file's content."""
    fails: list[str] = []
    nums = {num for _, num, _ in s2_rows(text)}
    for cite in sorted(s3_citations(text)):
        if cite not in nums:
            fails.append(
                f"PS1 [{label}]: §3 cites ({cite}) but §2 has no row {cite} "
                f"(renumbered or removed?)"
            )
    for lineno, num in s2_rows_missing_state(text):
        fails.append(
            f"PS2 [{label}]: §2 row {num} (line {lineno}) has no legal state "
            f"mark ({' '.join(STATES)})"
        )
    return fails


def check_transition(head_text: str, staged_text: str) -> list[str]:
    """PS3: rows moved into 🟢 this commit require a new §3 row."""
    newly_green = green_set(staged_text) - green_set(head_text)
    if not newly_green:
        return []
    if s3_data_rows(staged_text) > s3_data_rows(head_text):
        return []
    rows = ", ".join(sorted(newly_green))
    return [
        f"PS3: §2 row(s) {rows} moved to shipped (🟢) but §3 gained no row in "
        f"this commit. Record the ship in §3 (the two move together), or "
        f"PLAN_SYNC_OK=1 for a deliberate exception."
    ]


def _git_show(rev_path: str) -> str | None:
    """`git show <rev>:<path>` → text, or None if the object is absent.

    Run in the inherited cwd, which for a pre-commit hook is the worktree root
    of the repo being committed — so this reads *that* repo's index/HEAD, not a
    hardwired path. Paths are repo-root-relative, resolving from any subdir.
    """
    r = subprocess.run(
        ["git", "show", rev_path],
        capture_output=True,
        text=True,
    )
    return r.stdout if r.returncode == 0 else None


def _is_staged(path: str) -> bool:
    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
    )
    return path in r.stdout.split()


def run_precommit() -> int:
    if not _is_staged(PLAN):
        return 0  # commit does not touch the plan
    staged = _git_show(f":{PLAN}")
    if staged is None:
        return 0
    head = _git_show(f"HEAD:{PLAN}")
    if head is None:
        head = ""  # first commit of the file
    fails = check_resting(staged, "staged") + check_transition(head, staged)
    if fails:
        print("plan-sync FAILED:\n", file=sys.stderr)
        for f in fails:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("plan-sync: OK — §2/§3 consistent, no unshipped move.")
    return 0


def run_tree() -> int:
    text = (ROOT / PLAN).read_text(encoding="utf-8")
    fails = check_resting(text, "tree")
    if fails:
        print("plan-sync FAILED:\n", file=sys.stderr)
        for f in fails:
            print(f"  - {f}", file=sys.stderr)
        return 1
    rows = len(s2_rows(text))
    print(
        f"plan-sync: OK — {rows} §2 rows, every §3 citation resolves, "
        f"every state mark legal."
    )
    return 0


# ── self-test ────────────────────────────────────────────────────────────────

_HEAD_FIXTURE = """\
# Working plan

## 2. The priority queue

| # | Item | State | Gate | Owner |
|---|---|---|---|---|
| 2.1 | First thing | 🟢 | — | x |
| 2.2 | Second thing | 🔵 | — | y |
| 2.3 | Third thing | ⚪ | — | z |

## 3. Shipped — newest first

| Date | What | Where |
|---|---|---|
| 2026-01-01 | First thing shipped (2.1) | #1 |

## 4. Findings
nothing
"""


def _mutate(text: str, old: str, new: str) -> str:
    assert old in text, f"fixture missing {old!r}"
    return text.replace(old, new, 1)


def self_test() -> int:
    failures = []

    def expect(name: str, got: bool, want: bool) -> None:
        if got != want:
            failures.append(f"{name}: expected {'FAIL' if want else 'pass'}")

    # Clean baseline: HEAD passes resting; HEAD→HEAD has no transition.
    expect("clean-resting", bool(check_resting(_HEAD_FIXTURE, "t")), False)
    expect("clean-transition", bool(check_transition(_HEAD_FIXTURE, _HEAD_FIXTURE)), False)

    # PS3 fail: flip 2.2 to 🟢, add no §3 row.
    flipped = _mutate(_HEAD_FIXTURE, "| 2.2 | Second thing | 🔵 |", "| 2.2 | Second thing | 🟢 |")
    expect("PS3-no-new-row", bool(check_transition(_HEAD_FIXTURE, flipped)), True)

    # PS3 pass: same flip WITH a new §3 row.
    flipped_ok = _mutate(
        flipped,
        "| 2026-01-01 | First thing shipped (2.1) | #1 |",
        "| 2026-01-01 | First thing shipped (2.1) | #1 |\n| 2026-02-02 | Second thing shipped (2.2) | #2 |",
    )
    expect("PS3-with-new-row", bool(check_transition(_HEAD_FIXTURE, flipped_ok)), False)

    # PS3 aggregate: flip TWO rows, add ONE §3 row → passes (≥1).
    two = _mutate(flipped, "| 2.3 | Third thing | ⚪ |", "| 2.3 | Third thing | 🟢 |")
    two_ok = _mutate(
        two,
        "| 2026-01-01 | First thing shipped (2.1) | #1 |",
        "| 2026-01-01 | First thing shipped (2.1) | #1 |\n| 2026-02-02 | 2.2 and 2.3 shipped together | #2 |",
    )
    expect("PS3-aggregate-one-row", bool(check_transition(_HEAD_FIXTURE, two_ok)), False)

    # PS1 fail: §3 cites a row §2 does not have.
    dangling = _mutate(_HEAD_FIXTURE, "First thing shipped (2.1)", "Ghost shipped (2.9)")
    expect("PS1-dangling", any("PS1" in f for f in check_resting(dangling, "t")), True)

    # PS2 fail: a §2 row with no legal state mark.
    nostate = _mutate(_HEAD_FIXTURE, "| 2.2 | Second thing | 🔵 |", "| 2.2 | Second thing | ?? |")
    expect("PS2-bad-state", any("PS2" in f for f in check_resting(nostate, "t")), True)

    # Guard against parser drift: the live plan.md must pass resting today.
    live = ROOT / PLAN
    if live.exists():
        expect("live-resting-clean", bool(check_resting(live.read_text(encoding="utf-8"), "live")), False)

    if failures:
        print("plan-sync --self-test FAILED:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("plan-sync --self-test: OK — clean fixture passes, every by-design failure fires.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pre-commit", action="store_true", help="diff-aware, staged content")
    ap.add_argument("--self-test", action="store_true", help="run fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.pre_commit:
        return run_precommit()
    return run_tree()


if __name__ == "__main__":
    sys.exit(main())
