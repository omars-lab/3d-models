#!/usr/bin/env python3
"""Validate the use-case map in use-cases.md.

Modes:
  validate.py            full validation of the working copy
  validate.py --staged   pre-commit mode (called by .githooks/pre-commit.d/20-use-cases)
  validate.py --refresh  rewrite frontmatter as_of hashes to each repo's HEAD, then validate

Checks (full mode):
  - frontmatter parses and every as_of hash resolves in its repo
  - every pointer `repo:path:Lstart[-Lend]` names a file that exists at the
    pinned as_of commit and has at least Lend lines
  - the mermaid diagram and the pointer table declare the same UC ids
  - warns when a repo's as_of lags its local HEAD (missing cross-repo
    checkouts are warn-and-skip, never a failure)

Pre-commit mode adds the freshness contract:
  - use-cases.md staged  -> staged content must fully validate AND its
    3d-models as_of must equal HEAD (the commit being built upon)
  - use-cases.md not staged but a staged file is referenced by a 3d-models
    pointer -> BLOCK (override once with USE_CASES_OK=1 git commit ...)
  - staged files touch experience surfaces (index.html, Makefile, docs/,
    src/) -> non-blocking reminder
  - 3d-models as_of more than STALE_LIMIT commits behind HEAD -> reminder
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

DOC_RELPATH = ".claude/skills/maintain-use-cases/use-cases.md"
SELF_REPO = "3d-models"
STALE_LIMIT = 20
SURFACE_PATTERNS = (
    re.compile(r"^index\.html$"),
    re.compile(r"^Makefile$"),
    re.compile(r"^docs/.*\.md$"),
    re.compile(r"^src/"),
)
POINTER_RE = re.compile(r"`(?P<repo>[\w.-]+):(?P<path>[^`\s:]+):L(?P<start>\d+)(?:-L(?P<end>\d+))?`")
UC_RE = re.compile(r"\bUC\d+\b")


def run_git(repo_dir: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", repo_dir, *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def try_git(repo_dir: str, *args: str) -> str | None:
    try:
        return run_git(repo_dir, *args)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


class Doc:
    def __init__(self, text: str):
        self.as_of: dict[str, str] = {}
        self.repos: dict[str, str] = {}
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            raise ValueError(f"{DOC_RELPATH}: missing frontmatter block")
        section = None
        for line in m.group(1).splitlines():
            if re.match(r"^as_of:\s*$", line):
                section = self.as_of
            elif re.match(r"^repos:\s*$", line):
                section = self.repos
            elif re.match(r"^\S", line):
                section = None
            elif section is not None:
                kv = re.match(r"^\s+([\w.-]+):\s*(\S+)\s*$", line)
                if kv:
                    section[kv.group(1)] = kv.group(2)
        if SELF_REPO not in self.as_of:
            raise ValueError(f"{DOC_RELPATH}: frontmatter as_of is missing '{SELF_REPO}'")
        body = text[m.end() :]
        mermaid = re.search(r"```mermaid\n(.*?)```", body, re.DOTALL)
        if not mermaid:
            raise ValueError(f"{DOC_RELPATH}: no mermaid diagram found")
        self.diagram_ucs = set(UC_RE.findall(mermaid.group(1)))
        self.table_ucs: set[str] = set()
        self.pointers: list[tuple[str, str, int, int]] = []
        for line in body.splitlines():
            if not line.startswith("| UC"):
                continue
            uc = UC_RE.match(line[2:])
            if uc:
                self.table_ucs.add(uc.group(0))
            for p in POINTER_RE.finditer(line):
                start = int(p.group("start"))
                end = int(p.group("end") or start)
                self.pointers.append((p.group("repo"), p.group("path"), start, end))

    def repo_dir(self, repo: str, root: str) -> str | None:
        if repo == SELF_REPO:
            return root
        rel = self.repos.get(repo)
        if rel is None:
            return None
        d = os.path.normpath(os.path.join(root, rel))
        return d if os.path.isdir(os.path.join(d, ".git")) else None


def validate_full(doc: Doc, root: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if doc.diagram_ucs != doc.table_ucs:
        only_d = ", ".join(sorted(doc.diagram_ucs - doc.table_ucs)) or "-"
        only_t = ", ".join(sorted(doc.table_ucs - doc.diagram_ucs)) or "-"
        errors.append(f"diagram/table mismatch: diagram-only [{only_d}], table-only [{only_t}]")
    pointer_repos = {p[0] for p in doc.pointers}
    for repo in sorted(pointer_repos - set(doc.as_of)):
        errors.append(f"pointers reference repo '{repo}' but frontmatter as_of has no hash for it")
    for repo, pin in doc.as_of.items():
        rdir = doc.repo_dir(repo, root)
        if rdir is None:
            warnings.append(f"repo '{repo}' not checked out locally — skipped its pointer checks")
            continue
        if try_git(rdir, "cat-file", "-e", f"{pin}^{{commit}}") is None:
            errors.append(f"as_of hash for '{repo}' ({pin[:12]}) does not resolve in {rdir}")
            continue
        head = try_git(rdir, "rev-parse", "HEAD")
        if head and head != pin:
            behind = try_git(rdir, "rev-list", "--count", f"{pin}..{head}")
            # The self pin is always >= 1 behind once the map-commit lands
            # (as_of records that commit's parent) — only nag past the limit.
            if repo != SELF_REPO or behind is None or int(behind) > STALE_LIMIT:
                warnings.append(f"'{repo}' as_of is {behind or '?'} commit(s) behind its local HEAD")
        for prepo, path, start, end in doc.pointers:
            if prepo != repo:
                continue
            blob = try_git(rdir, "cat-file", "-p", f"{pin}:{path}")
            if blob is None:
                errors.append(f"{prepo}:{path} does not exist at as_of {pin[:12]}")
                continue
            nlines = blob.count("\n") + 1
            if end > nlines:
                errors.append(f"{prepo}:{path}:L{start}-L{end} exceeds file length {nlines} at as_of {pin[:12]}")
    return errors, warnings


def report(errors: list[str], warnings: list[str], context: str) -> int:
    for w in warnings:
        print(f"use-cases [{context}] warning: {w}", file=sys.stderr)
    for e in errors:
        print(f"use-cases [{context}] ERROR: {e}", file=sys.stderr)
    return 1 if errors else 0


def mode_full(root: str) -> int:
    with open(os.path.join(root, DOC_RELPATH), encoding="utf-8") as f:
        doc = Doc(f.read())
    rc = report(*validate_full(doc, root), context="full")
    if rc == 0:
        print(f"use-cases: {len(doc.table_ucs)} use cases, {len(doc.pointers)} pointers — all valid at pinned commits")
    return rc


def mode_refresh(root: str) -> int:
    path = os.path.join(root, DOC_RELPATH)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    doc = Doc(text)
    for repo, pin in doc.as_of.items():
        rdir = doc.repo_dir(repo, root)
        head = try_git(rdir, "rev-parse", "HEAD") if rdir else None
        if head is None:
            print(f"use-cases refresh: '{repo}' not available — pin kept at {pin[:12]}", file=sys.stderr)
        elif head != pin:
            text = text.replace(f"{repo}: {pin}", f"{repo}: {head}")
            print(f"use-cases refresh: {repo} {pin[:12]} -> {head[:12]}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return mode_full(root)


def mode_staged(root: str) -> int:
    staged = [f for f in run_git(root, "diff", "--cached", "--name-only").splitlines() if f]
    head = try_git(root, "rev-parse", "HEAD")
    if DOC_RELPATH in staged:
        doc = Doc(run_git(root, "show", f":{DOC_RELPATH}"))
        errors, warnings = validate_full(doc, root)
        if head and doc.as_of.get(SELF_REPO) != head:
            errors.append(
                f"staged {SELF_REPO} as_of {doc.as_of.get(SELF_REPO, '?')[:12]} != HEAD {head[:12]} — "
                f"run .claude/skills/maintain-use-cases/validate.py --refresh and restage"
            )
        return report(errors, warnings, context="pre-commit")
    try:
        doc = Doc(run_git(root, "show", f"HEAD:{DOC_RELPATH}"))
    except subprocess.CalledProcessError:
        return 0  # map not committed yet — nothing to guard
    referenced = {path for repo, path, _, _ in doc.pointers if repo == SELF_REPO}
    hits = sorted(referenced & set(staged))
    if hits:
        if os.environ.get("USE_CASES_OK") == "1":
            print(f"use-cases: override accepted for pointer-referenced files: {', '.join(hits)}", file=sys.stderr)
        else:
            print(
                "use-cases BLOCK: staged files are referenced by the use-case map "
                f"({', '.join(hits)}) but {DOC_RELPATH} is not staged.\n"
                "  Update the map + run validate.py --refresh, stage it, and retry —\n"
                "  or override once with: USE_CASES_OK=1 git commit ...",
                file=sys.stderr,
            )
            return 1
    elif any(p.match(f) for f in staged for p in SURFACE_PATTERNS):
        print(
            "use-cases reminder: this commit touches experience surfaces — if it adds or "
            f"changes a user-facing capability, update {DOC_RELPATH} (skill: maintain-use-cases).",
            file=sys.stderr,
        )
    pin = doc.as_of.get(SELF_REPO)
    if head and pin:
        behind = try_git(root, "rev-list", "--count", f"{pin}..{head}")
        if behind is None or int(behind) > STALE_LIMIT:
            print(
                f"use-cases reminder: the map's as_of is {behind or 'unknown-count'} commits behind HEAD — "
                "consider validate.py --refresh in a follow-up commit.",
            file=sys.stderr,
            )
    return 0


def main() -> int:
    root = run_git(os.path.dirname(os.path.abspath(__file__)), "rev-parse", "--show-toplevel")
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--staged":
        return mode_staged(root)
    if mode == "--refresh":
        return mode_refresh(root)
    return mode_full(root)


if __name__ == "__main__":
    sys.exit(main())
