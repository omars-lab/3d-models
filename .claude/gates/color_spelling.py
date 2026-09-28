#!/usr/bin/env python3
"""Does the British spelling of "color" creep back into 3d-models?

On 2026-09-28 Omar chose American spelling everywhere ("American everywhere",
review thread e7b42d), and every use of the old spelling in this repo's docs,
skills, tools and file names became "color" in one change (D-083), paired with
bikar #277, which did the same to bikar. A rename like that grows back one word
at a time unless something says no, so this says no: it fails when the old
spelling appears, in any case and as part of any word, in a tracked file or a
tracked file's name, unless the line holds one of ALLOWED_TOKENS or the file
matches one of ALLOWED_PATHS. Every entry carries its reason, printed with
`--list`, so the allow list can be read and argued with rather than trusted.

It mirrors bikar's `scripts/check-color-spelling.mjs`: an allowed token is cut
out of the line before the test, so a line that holds an allowed token AND a new
`fooColour` still fails, and a new `colour-thing.md` fails on its name alone.

Usage:
    python3 .claude/gates/color_spelling.py             # every tracked file
    python3 .claude/gates/color_spelling.py --staged    # the index only (pre-commit)
    python3 .claude/gates/color_spelling.py --list      # print the allow list
    python3 .claude/gates/color_spelling.py --self-test
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

WORD = re.compile("colo" + "ur", re.IGNORECASE)

#: Literal substrings that may hold the old spelling, each with its reason.
ALLOWED_TOKENS: list[tuple[str, str]] = [
    ("filament_colour", "Bambu Studio's config key in a 3MF's project_settings.config "
     "(also default_filament_colour); the slicer spells it this way"),
    ("extruder_colour", "Bambu Studio's config key, same as above"),
    ("!COLOUR", "LDraw meta-command name (LDConfig.ldr syntax); the format spells it this way"),
    ("1 <colour>", "the LDraw spec's own syntax for a type-1 line"),
    ("do-the-engines-rings-match-omars-colour-classes",
     "link anchor into a heading of a verbatim research doc (docs/research/multicolor-constructions.md)"),
    ("The colour palette — grounded",
     "heading literal in verbatim research (docs/research/lego-ldraw-export.md), "
     "cited by a use-case map anchor"),
    ("bikar-coaster-colour", "the name a past worktree had; a record names it as it was"),
    ("feat/coaster-colour-regions", "the name a past branch had; a record names it as it was"),
    ("reduce colour changes", "quoted from Sovol's guide (docs/design/coaster/multicolor-design.md)"),
    ('"up to 25 colours"', "quoted from Bambu's store page snippet (docs/design/coaster/multicolor-design.md)"),
    ('British "colour"', "the decision record (D-083) naming the old spelling once"),
]

#: Whole files (fnmatch patterns on the repo path) that may hold the old spelling.
ALLOWED_PATHS: list[tuple[str, str]] = [
    ("docs/research/*", "verbatim: research is checked in as it was written (CLAUDE.md "
     "'Research is checked in'); only link targets to renamed files were changed"),
    ("*/.*.comments.md", "review-md sidecar: written only through Obsidian and holds the "
     "reviewers' own words; never hand-edited"),
    (".claude/gates/color_spelling.py", "this check; its allow list names the old word"),
]


def path_allowed(path: str) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat, _ in ALLOWED_PATHS)


def offends(line: str) -> bool:
    """Cut every allowed token out of the line, then ask whether the old spelling is left."""
    rest = line
    for token, _ in ALLOWED_TOKENS:
        rest = rest.replace(token, "")
    return bool(WORD.search(rest))


def scan_file(path: str, data: bytes) -> list[tuple[str, int, str]]:
    """Findings for one file: its name (line 0), then each offending line."""
    if path_allowed(path):
        return []
    findings: list[tuple[str, int, str]] = []
    if offends(path):
        findings.append((path, 0, "(file name)"))
    if b"\0" in data:
        return findings  # binary: only its name is checked
    text = data.decode("utf-8", errors="replace")
    for i, line in enumerate(text.split("\n"), 1):
        if offends(line):
            findings.append((path, i, line.strip()))
    return findings


def _git(root: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True).stdout


def list_files(root: Path, staged: bool) -> list[str]:
    args = ["diff", "--cached", "--name-only", "--diff-filter=ACMR"] if staged else ["ls-files"]
    return [p for p in _git(root, *args).decode().splitlines() if p]


def read_file(root: Path, path: str, staged: bool) -> bytes:
    try:
        if staged:
            return _git(root, "show", f":{path}")
        full = root / path
        return b"" if full.is_dir() else full.read_bytes()
    except (OSError, subprocess.CalledProcessError):
        return b""  # a file deleted but not staged


def run(root: Path, staged: bool) -> int:
    findings = [f for p in list_files(root, staged) for f in scan_file(p, read_file(root, p, staged))]
    if not findings:
        print("color-spelling: ok (no British spelling outside the allow list)")
        return 0
    for path, line, text in findings:
        print(f"{path}:{line}: {text[:160]}", file=sys.stderr)
    print(f"\ncolor-spelling: {len(findings)} use(s) of the British spelling outside the allow list.\n"
          "3d-models spells it \"color\" (D-083 in docs/decisions-log.md). If the old spelling is\n"
          "genuinely required (a file format's name, a quoted source), add an entry with its reason\n"
          "to ALLOWED_TOKENS or ALLOWED_PATHS in .claude/gates/color_spelling.py.", file=sys.stderr)
    return 1


def print_allow_list() -> None:
    print("Allowed tokens:")
    for token, reason in ALLOWED_TOKENS:
        print(f"  {token} — {reason}")
    print("Allowed paths:")
    for pat, reason in ALLOWED_PATHS:
        print(f"  {pat} — {reason}")


def _self_test() -> int:
    failures = 0

    def expect(label: str, got: object, want: object) -> None:
        nonlocal failures
        ok = got == want
        failures += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" (got {got!r}, want {want!r})"))

    old = "colo" + "ur"
    Old = "Colo" + "ur"
    # FAIL: a new identifier in a doc.
    expect("a new fooColour in a doc is a finding",
           [f[1] for f in scan_file("docs/x.md", f"const foo{Old} = 1\n".encode())], [1])
    # PASS: an allowed external name.
    expect("an allowed !COLOUR line passes",
           scan_file("docs/x.md", f"0 !{old.upper()} Black CODE 0\n".encode()), [])
    expect("a token hides only itself",
           len(scan_file("docs/x.md", f"0 !{old.upper()} x; foo{Old}\n".encode())), 1)
    expect("every case is caught", len(scan_file("a.ts", f"{old.upper()}\n{Old}s\nmulti{old}\n".encode())), 3)
    expect("a file name is checked", scan_file(f"docs/{old}-thing.md", b"fine\n")[0][1:], (0, "(file name)"))
    expect("a binary file is checked by name only", scan_file("a.png", f"\0{old}".encode()), [])
    expect("research is verbatim", scan_file("docs/research/r.md", f"{old}\n".encode()), [])
    expect("a review sidecar is exempt", scan_file("docs/.n.comments.md", f"{old}\n".encode()), [])
    expect("American spelling passes", scan_file("docs/x.md", b"color colors colored\n"), [])

    # The whole run, on a throwaway repo: exit 1 on the FAIL case, 0 on the PASS case.
    # A hook runs with GIT_DIR / GIT_INDEX_FILE set, and they outrank `git -C`;
    # drop them here so the throwaway repo is the one read.
    saved = {k: os.environ.pop(k) for k in list(os.environ) if k.startswith("GIT_")}
    try:
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            _git(repo, "init", "-q")
            (repo / "ok.md").write_text(f"0 !{old.upper()} Black CODE 0\n")
            _git(repo, "add", "ok.md")
            expect("a tree with only allowed uses exits 0", run(repo, staged=False), 0)
            (repo / "bad.md").write_text(f"let foo{Old} = 1\n")
            _git(repo, "add", "bad.md")
            expect("a staged new fooColour exits 1", run(repo, staged=True), 1)
    finally:
        os.environ.update(saved)
    print(f"self-test: {'PASS' if failures == 0 else f'{failures} FAILED'}")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--staged", action="store_true", help="check the index only")
    ap.add_argument("--list", action="store_true", help="print the allow list")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()
    if a.list:
        print_allow_list()
        return 0
    return run(ROOT, a.staged)


if __name__ == "__main__":
    sys.exit(main())
