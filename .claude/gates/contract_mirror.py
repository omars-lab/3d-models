#!/usr/bin/env python3
"""Contract-mirror gate: the prose contract mirrors must not drift behind canonical.

WHAT IT HOLDS. sacred-patterns owns the DSL metadata contract; bikar and qiyas
each vendor a **prose** copy of `dsl-metadata-contract.md` for readers on their
side. Unlike the JSON schemas (which are byte-identical and guarded by
`schema_mirror.py`), the prose copies are hand-maintained — each carries a
`Mirrored canonical version: vN.N` header naming the canonical version it was
last vendored from. Nothing compares that header to canonical, so a mirror can
sit at v1.5 long after canonical accepts v1.6, and every check stays green.

It has: the mirror prose lagged canonical by a full amendment across
v1.4 → v1.5 → v1.6, each caught only by a human remembering to re-vendor. This
gate makes the lag visible, from the one repo (3d-models) that already reads
both siblings — the same shape and home as `schema_mirror.py`.

WHAT THE INVARIANT IS. For each mirror: the version in its `Mirrored canonical
version:` header must equal canonical's current `**Version:**` headline. A
mirror at an *older* version is behind and must re-vendor; a mirror naming a
version canonical does not document at all is a stale or mistyped reference.
This is not a "did you update canonical?" reminder — those fire on every schema
bump, most of which change no contract meaning, and a gate that cries wolf gets
switched off. This fires only when a published mirror genuinely disagrees with
published canonical, which is a real defect every time.

WHERE IT READS. Every doc is read **at the sibling's default branch**, resolved
from that repo's `origin/HEAD` symref — the branch GitHub serves as default,
which `git clone` and `git remote set-head` point the symref at. Reading the one
canonical ref (not the first of a guessed `main`/`master` list to carry the file)
is what makes the verdict correct when a repo has both branches at different
versions. It is read via `git show` in the sibling checkout — never the working
tree, which is whatever another session has checked out (docs/decisions-log.md
D-001; same rule as `doc_pointers.py` and `schema_mirror.py`). So the verdict is
checkout-independent and offline — but it reflects the **last-fetched** origin
state (and last-known symref): a stale clone can read a mirror as behind when the
re-vendor merged but was never fetched. Every finding says so and names the
`git fetch` that clears a false one. A repo with no origin (the self-test
fixtures) falls back to `HEAD`.

SKIPS. A sibling not checked out at all is a warning and a skip, in the same
words the other sibling-reading gates use ("not checked out locally"). If
canonical (sacred-patterns) is not checked out, there is nothing to compare
against and the whole check is skipped. A mirror file absent at the origin ref
of a checked-out sibling is a finding, not a skip: the copy is supposed to be
there.

    contract_mirror.py               compare, exit 1 on any finding
    contract_mirror.py --self-test   fixed fixtures, then a tempdir layout with a
                                     primary clone, a linked worktree and the
                                     siblings, asserting the same verdict from each
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doc_pointers import _git_env, _sibling_root  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

#: Canonical owner and where it keeps the contract, relative to that repo's root.
CANONICAL_REPO = "sacred-patterns"
CANONICAL_REL = "docs/dsl-metadata-contract.md"

#: Each mirror repo and where it vendors its prose copy.
MIRRORS = {
    "bikar": "docs/dsl-metadata-contract.md",
    "qiyas": "src/qiyas/docs/dsl-metadata-contract.md",
}

_VERSION = r"v\d+(?:\.\d+)*"
CANON_VERSION = re.compile(r"^\*\*Version:\*\*\s+(" + _VERSION + r")", re.MULTILINE)
CANON_SECTION = re.compile(r"^##\s+Attributes\s+—\s+(" + _VERSION + r")\b", re.MULTILINE)
MIRROR_VERSION = re.compile(r"Mirrored canonical version:\s*(" + _VERSION + r")")

REPAIR = (
    "repair: re-vendor the mirror's dsl-metadata-contract.md from canonical "
    "(sacred-patterns) — flip its `Mirrored canonical version:` header and any "
    "changed rows to the accepted version, then merge. If a sibling's origin ref "
    "is stale, `git -C <repo> fetch origin` and re-run — this reads last-fetched "
    "origin. Override once: CONTRACT_MIRROR_OK=1 git commit"
)


# ------------------------------------------------------------------- sibling reads


def _git(repo: Path, *args: str) -> str | None:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=True,
            env=_git_env(),
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def _default_ref(repo: Path) -> str:
    """The repo's canonical ref to read from: its origin default branch, else `HEAD`.

    `origin/HEAD` is a symref that `git clone` / `git remote set-head` aim at the
    remote's default branch — so this reads the branch GitHub serves as canonical,
    not whichever of `origin/main` / `origin/master` happens to exist and carry the
    file. A repo with no origin (the self-test fixtures) has no such symref and
    falls back to `HEAD`.
    """
    out = _git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if out and out.strip():
        return out.strip()
    return "HEAD"


def read_doc(repo: Path, rel: str) -> str | None:
    """The text of `rel` at `repo`'s default branch; None if that ref lacks it."""
    ref = _default_ref(repo)
    out = _git(repo, "show", f"{ref}:{rel}")
    if out is not None:
        return out
    # An origin default that lacks the file, or an unusable symref: last-resort
    # read the checked-out HEAD so a lone-branch fixture still resolves.
    return _git(repo, "show", f"HEAD:{rel}")


# ------------------------------------------------------------------------ parse


def _tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version[1:].split("."))


def canonical_versions(text: str) -> tuple[str | None, set[str]]:
    """(headline version, every version canonical documents). Headline is None if absent."""
    m = CANON_VERSION.search(text)
    headline = m.group(1) if m else None
    known = set(CANON_SECTION.findall(text))
    if headline:
        known.add(headline)
    return headline, known


def mirror_version(text: str) -> str | None:
    m = MIRROR_VERSION.search(text)
    return m.group(1) if m else None


# ---------------------------------------------------------------------- compare


def check_mirrors(canonical_text: str, mirrors: dict[str, str]) -> list[str]:
    """Findings between canonical and each mirror's declared version. Empty means in step."""
    headline, known = canonical_versions(canonical_text)
    if headline is None:
        return [
            f"{CANONICAL_REPO}:{CANONICAL_REL}: no `**Version:**` headline found — "
            f"cannot tell what version to hold the mirrors to"
        ]
    findings: list[str] = []
    for name, text in sorted(mirrors.items()):
        declared = mirror_version(text)
        if declared is None:
            findings.append(
                f"{name} mirror: no `Mirrored canonical version:` header — "
                f"cannot tell what it is vendored from"
            )
        elif declared == headline:
            continue
        elif _tuple(declared) < _tuple(headline):
            findings.append(
                f"{name} mirror is behind canonical: declares {declared}, canonical is "
                f"{headline} — re-vendor its dsl-metadata-contract.md to {headline}"
            )
        elif declared not in known:
            findings.append(
                f"{name} mirror declares {declared}, which canonical does not document "
                f"(canonical is at {headline}) — a stale or mistyped reference"
            )
        else:
            findings.append(
                f"{name} mirror declares {declared}, ahead of canonical's {headline} — "
                f"canonical has not accepted that version"
            )
    return findings


# -------------------------------------------------------------------------- run


def run(root: Path) -> tuple[list[str], list[str]]:
    """(findings, warnings) for the repo at `root`, reading siblings at their origin refs."""
    warnings: list[str] = []
    canon_repo = _sibling_root(CANONICAL_REPO, root)
    if canon_repo is None:
        warnings.append(
            f"repo '{CANONICAL_REPO}' not checked out locally — skipped the contract-mirror check"
        )
        return [], warnings
    canon_text = read_doc(canon_repo, CANONICAL_REL)
    if canon_text is None:
        return (
            [f"{CANONICAL_REPO}: {CANONICAL_REL} not found at origin — `git -C {canon_repo} fetch origin`"],
            warnings,
        )
    findings: list[str] = []
    mirrors: dict[str, str] = {}
    for name, rel in sorted(MIRRORS.items()):
        repo = _sibling_root(name, root)
        if repo is None:
            warnings.append(f"repo '{name}' not checked out locally — skipped its mirror")
            continue
        text = read_doc(repo, rel)
        if text is None:
            findings.append(f"{name}: {rel} not found at origin — `git -C {repo} fetch origin`")
            continue
        mirrors[name] = text
    findings.extend(check_mirrors(canon_text, mirrors))
    return findings, warnings


def report(findings: list[str], warnings: list[str]) -> int:
    for w in warnings:
        print(f"contract-mirror: warning — {w}")
    if warnings and not findings:
        return 0
    if not findings:
        print("contract-mirror: every prose mirror is vendored from canonical's current version")
        return 0
    print(f"contract-mirror: {len(findings)} finding(s)")
    for f in findings:
        print(f"  - {f}")
    print(f"  {REPAIR}")
    return 1


# --------------------------------------------------------------------- self-test


def _mirror_doc(version: str, header: bool = True) -> str:
    line = f"**Mirrored canonical version: {version}** (sacred-patterns#NN)\n" if header else "no header here\n"
    return f"# DSL Metadata Contract (mirror)\n{line}\nrows follow.\n"


CANON_FIXTURE = (
    "# DSL Metadata Contract\n"
    "**Version:** v1.6 (v1 ACCEPTED + ribbon-view provenance ACCEPTED 2026-08-16 "
    "+ base-face honesty ACCEPTED 2026-09-09)\n"
    "**Owner:** sacred-patterns\n\n"
    "## Attributes — v1 ACCEPTED (currently emitted)\n\n"
    "## Attributes — v1.5 ACCEPTED (ribbon-view provenance)\n\n"
    "## Attributes — v1.6 ACCEPTED (base-face honesty, D-052)\n"
)

#: name → (mirrors dict, wanted finding count, substring every wanted finding carries)
FIXTURE_CASES: list[tuple[str, dict[str, str], int, str]] = [
    ("in-step", {"bikar": _mirror_doc("v1.6"), "qiyas": _mirror_doc("v1.6")}, 0, ""),
    ("behind", {"bikar": _mirror_doc("v1.5")}, 1, "behind canonical: declares v1.5, canonical is v1.6"),
    ("dangling", {"bikar": _mirror_doc("v1.9")}, 1, "which canonical does not document"),
    ("no-header", {"qiyas": _mirror_doc("v0", header=False)}, 1, "no `Mirrored canonical version:` header"),
]


def _fixture_cases() -> bool:
    ok = True
    for label, mirrors, want, needle in FIXTURE_CASES:
        got = check_mirrors(CANON_FIXTURE, mirrors)
        hit = len(got) == want and all(needle in f for f in got)
        ok &= hit
        print(f"self-test {'ok  ' if hit else 'FAIL'}: {label} → {got or 'no findings'}")
    # A canonical with no headline cannot hold the mirrors to anything.
    no_headline = check_mirrors("# no version line here\n", {"bikar": _mirror_doc("v1.6")})
    hit = len(no_headline) == 1 and "no `**Version:**` headline" in no_headline[0]
    ok &= hit
    print(f"self-test {'ok  ' if hit else 'FAIL'}: no-canonical-headline → {no_headline}")
    return ok


def _init_repo(path: Path, files: dict[str, str]) -> None:
    """A git repo at `path` with `files` committed on the default branch."""
    path.mkdir(parents=True)
    for rel, data in files.items():
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        (path / rel).write_text(data, encoding="utf-8")
    env = {**_git_env(), "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    cmds = [
        ["init", "-q"],
        ["add", "-A"],
        ["-c", "user.email=t@e.invalid", "-c", "user.name=t", "commit", "-q", "--no-verify", "-m", "fixture"],
    ]
    for c in cmds:
        subprocess.run(["git", "-C", str(path), *c], check=True, env=env, capture_output=True)


def _layout_case(tmp: Path) -> bool:
    """A primary clone, a linked worktree one level down, and the siblings beside the primary.

    The worktree must reach the same verdict as the primary — the checkout-independence
    rule every sibling-reading gate here is held to. The siblings deliberately carry a
    lagging bikar mirror so the agreed verdict is a *failing* one: two "nothing to
    check" runs would agree too.
    """
    _init_repo(tmp / CANONICAL_REPO, {CANONICAL_REL: CANON_FIXTURE})
    _init_repo(tmp / "bikar", {MIRRORS["bikar"]: _mirror_doc("v1.5")})
    _init_repo(tmp / "qiyas", {MIRRORS["qiyas"]: _mirror_doc("v1.6")})
    primary = tmp / "3d-models"
    _init_repo(primary, {"README.md": "primary\n"})
    wt = tmp / "3d-models.worktrees" / "gate"
    subprocess.run(
        ["git", "-C", str(primary), "worktree", "add", "-q", "--detach", str(wt)],
        check=True,
        env=_git_env(),
        capture_output=True,
    )
    saved = os.environ.pop("BIKAR_DIR", None)
    try:
        verdicts = {name: run(root) for name, root in (("primary", primary), ("worktree", wt))}
    finally:
        if saved is not None:
            os.environ["BIKAR_DIR"] = saved
    ok = True
    for name, (findings, warnings) in verdicts.items():
        hit = len(findings) == 1 and "bikar mirror is behind canonical" in findings[0] and not warnings
        ok &= hit
        print(f"self-test {'ok  ' if hit else 'FAIL'}: layout/{name} → {findings or warnings or 'nothing'}")
    if verdicts["primary"] != verdicts["worktree"]:
        print("self-test FAIL: primary and worktree disagree")
        ok = False
    return ok


def self_test() -> int:
    ok = _fixture_cases()
    with tempfile.TemporaryDirectory() as d:
        ok &= _layout_case(Path(d))
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="the prose contract mirrors (bikar, qiyas) vs canonical's version, at origin refs"
    )
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    findings, warnings = run(ROOT)
    return report(findings, warnings)


if __name__ == "__main__":
    sys.exit(main())
