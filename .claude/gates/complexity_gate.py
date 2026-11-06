#!/usr/bin/env python3
"""Complexity gate: no Python function in this repo may grow past a
complexity of 10, the limit bikar (eslint) and qiyas (ruff) already use.

Complexity here is ruff's C901 (McCabe): roughly one plus the number of
branches a function can take. Over 10, a function is hard to read and hard
to test every path of (D-129, docs/design/process/code-graph.md).

86 functions were already over 10 when this gate was added (2026-11-06).
They are listed in complexity-baseline.json with their score. The list is a
ratchet: it may shrink freely and grows only by editing it on purpose.

    FAIL: a function not on the list is over 10, or a listed one got worse.
    PASS: every function over 10 is listed at its score or lower.
    Note, not a failure: a listed function is now at 10 or below, or
    lower than listed. Run --update to shrink the list to match.

ruff is run through uvx at a pinned version, so every machine measures the
same way:

    complexity_gate.py              # check the tracked Python files
    complexity_gate.py --update     # rewrite the list (only shrinks unless --allow-grow)
    complexity_gate.py --self-test  # the compare logic on fixtures
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RUFF = "ruff@0.14.3"
MAX = 10
ROOT = Path(__file__).resolve().parents[2]
BASELINE = Path(__file__).with_name("complexity-baseline.json")
_MSG = re.compile(r"`(?P<name>[^`]+)` is too complex \((?P<score>\d+) > \d+\)")


def tracked_python() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "*.py"],
                         capture_output=True, text=True, check=True).stdout
    return [p for p in out.splitlines() if p and (ROOT / p).exists()]


def measure(files: list[str]) -> dict[str, list[int]]:
    """'path::function' -> scores over the limit, highest first."""
    cmd = ["uvx", RUFF, "check", "--isolated", "--select", "C901",
           "--config", f"lint.mccabe.max-complexity={MAX}",
           "--output-format", "json", "--exit-zero", *files]
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
    if res.returncode != 0:
        raise RuntimeError(f"ruff failed ({res.returncode}): {res.stderr.strip()[:500]}")
    found: dict[str, list[int]] = {}
    for row in json.loads(res.stdout or "[]"):
        m = _MSG.search(row.get("message", ""))
        if not m:
            continue
        path = Path(row["filename"]).resolve().relative_to(ROOT).as_posix()
        found.setdefault(f"{path}::{m['name']}", []).append(int(m["score"]))
    return {k: sorted(v, reverse=True) for k, v in found.items()}


def compare(now: dict[str, list[int]], listed: dict[str, list[int]]) -> tuple[list[str], list[str]]:
    """(failures, notes). Same-named functions in one file pair up highest first."""
    fails, notes = [], []
    for key, scores in sorted(now.items()):
        base = listed.get(key, [])
        for i, s in enumerate(scores):
            if i >= len(base):
                fails.append(f"{key} is {s}, over {MAX}, and not on the list")
            elif s > base[i]:
                fails.append(f"{key} went from {base[i]} to {s}")
            elif s < base[i]:
                notes.append(f"{key} dropped from {base[i]} to {s}")
    for key, base in sorted(listed.items()):
        extra = len(base) - len(now.get(key, []))
        if extra > 0:
            notes.append(f"{key} is now at {MAX} or below (or gone)")
    return fails, notes


def load_baseline() -> dict[str, list[int]]:
    if not BASELINE.exists():
        return {}
    data = json.loads(BASELINE.read_text(encoding="utf-8"))
    return {k: sorted(v, reverse=True) for k, v in data["functions"].items()}


def write_baseline(funcs: dict[str, list[int]]) -> None:
    data = {
        "_about": "Python functions over complexity 10 when the gate was added, with their "
                  "score. Shrinks freely; grows only on purpose. See complexity_gate.py.",
        "max": MAX,
        "ruff": RUFF,
        "functions": dict(sorted(funcs.items())),
    }
    BASELINE.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")


def run(update: bool, allow_grow: bool) -> int:
    if not shutil.which("uvx"):
        print("complexity: uvx not on PATH (brew install uv) — not checked", file=sys.stderr)
        return 1
    now = measure(tracked_python())
    listed = load_baseline()
    fails, notes = compare(now, listed)
    if update:
        if fails and not allow_grow:
            print("complexity: will not add to the list without --allow-grow:")
            for f in fails:
                print(f"  {f}")
            return 1
        write_baseline(now)
        print(f"complexity: list rewritten, {sum(len(v) for v in now.values())} function(s) over {MAX}")
        return 0
    for n in notes:
        print(f"  note: {n} — shrink the list with --update")
    total = sum(len(v) for v in now.values())
    if fails:
        print(f"complexity: {len(fails)} problem(s):")
        for f in fails:
            print(f"  FAIL {f}")
        print(f"  Split the function, or (on purpose) add it with --update --allow-grow.")
        return 1
    print(f"complexity: OK — {total} function(s) over {MAX}, all on the list at their score or lower")
    return 0


def self_test() -> int:
    listed = {"a.py::f": [15], "a.py::g": [12, 11], "b.py::h": [11]}
    cases = [
        ("same as list", {"a.py::f": [15], "a.py::g": [12, 11], "b.py::h": [11]}, 0, 0),
        ("new function over", {**listed, "c.py::k": [11]}, 1, 0),
        ("listed one worse", {**listed, "a.py::f": [16]}, 1, 0),
        ("second same-named one appears", {**listed, "b.py::h": [11, 11]}, 1, 0),
        ("one fixed", {"a.py::f": [15], "a.py::g": [12, 11]}, 0, 1),
        ("one better", {**listed, "a.py::f": [13]}, 0, 1),
    ]
    bad = 0
    for name, now, want_fail, want_note in cases:
        f, n = compare(now, listed)
        if (len(f), len(n)) != (want_fail, want_note):
            bad += 1
            print(f"FAIL {name}: {len(f)} failure(s), {len(n)} note(s); want {want_fail}, {want_note}")
    m = _MSG.search("`check_page` is too complex (33 > 10)")
    if not m or m["name"] != "check_page" or m["score"] != "33":
        bad += 1
        print("FAIL ruff message no longer parses")
    print(f"complexity self-test: {len(cases) + 1} cases, {'OK' if not bad else f'{bad} failed'}")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(run("--update" in sys.argv, "--allow-grow" in sys.argv))
