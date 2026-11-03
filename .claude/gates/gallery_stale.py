#!/usr/bin/env python3
"""Has the public gallery fallen behind master?

Nothing deploys the gallery on its own: `make deploy` publishes, so it stays a
hand step. But nothing said when it had not been run either. `status.html`
shows the last deploy, to someone who opens it, and between 2026-09-28 and
2026-11-03 five weeks of coaster work sat unpublished with nobody noticing.
This check says so, in `make validate`'s end summary, and fails nothing.

How it reads the state: the gh-pages tip's subject is written by `make deploy`
as "Deploy gallery from master (<sha>)". The commits on master after that sha
that touch a deployed path (the list `make deploy` copies, passed in as
arguments) are the unpublished changes; when the oldest of them is older than
`--days` (7), the gallery is stale: the gate prints a `gallery: WARN …` line
and exits WARN_RC. The Make target folds that exit to 0 (make would report any
other code as 2) and the parity runner repeats every `<check>: WARN` line in
its end summary, so the warning is read where the verdict is read, not
mid-stream.

A gh-pages ref that is not here prints a skip line (exit 0, like the timelapse
gate when nothing is rendered). A subject that does not carry a sha, or a sha
this checkout cannot resolve, is itself the warning: the gallery's state is
unknown, which is the thing this exists to prevent.

Usage:
    python3 .claude/gates/gallery_stale.py [--days 7] [--base origin/master] -- <deployed paths>
    python3 .claude/gates/gallery_stale.py --self-test
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

#: The exit code that means "ran, passed, but has something to say". The
#: parity runner (hook_parity.py) treats it as passed-and-warned; a plain
#: shell treats it as a failure, which is right for a script that is not
#: being read.
WARN_RC = 3

SUBJECT = re.compile(r"Deploy gallery from master \(([0-9a-f]{7,40})\)")
GALLERY_REFS = ("refs/remotes/origin/gh-pages", "refs/heads/gh-pages")


def _git(repo: Path, *args: str) -> str | None:
    """stdout of a git command, or None when it fails."""
    res = subprocess.run(  # noqa: S603
        ["git", "-C", str(repo), *args], capture_output=True, text=True
    )
    if res.returncode != 0:
        return None
    return res.stdout.strip()


def _first_ref(repo: Path, candidates: tuple[str, ...]) -> str | None:
    for ref in candidates:
        if _git(repo, "rev-parse", "--verify", "--quiet", ref) is not None:
            return ref
    return None


def check(repo: Path, paths: list[str], days: float, base: str | None, now: float | None = None) -> tuple[int, str]:
    """(exit code, message). 0 quiet, WARN_RC stale or unknown."""
    now = time.time() if now is None else now
    tip = _first_ref(repo, GALLERY_REFS)
    if tip is None:
        return 0, "gallery: no gh-pages ref in this checkout, skipping"
    subject = _git(repo, "log", "-1", "--format=%s", tip) or ""
    m = SUBJECT.search(subject)
    if not m:
        return WARN_RC, (
            f"gallery: WARN the gh-pages tip's subject is not a deploy line ({subject!r}); "
            "which master commit it shows is unknown"
        )
    source = m.group(1)
    if _git(repo, "rev-parse", "--verify", "--quiet", f"{source}^{{commit}}") is None:
        return WARN_RC, (
            f"gallery: WARN the gh-pages tip says it deployed {source}, which this checkout "
            "does not have; fetch origin, then run again"
        )
    base_ref = base or _first_ref(repo, ("refs/remotes/origin/master", "HEAD"))
    if base_ref is None:
        return WARN_RC, "gallery: WARN no origin/master and no HEAD to compare against"
    out = _git(repo, "log", "--format=%H %ct", f"{source}..{base_ref}", "--", *paths)
    if out is None:
        return WARN_RC, f"gallery: WARN could not list {source}..{base_ref} for the deployed paths"
    pending = [line.split() for line in out.splitlines() if line.strip()]
    if not pending:
        return 0, f"gallery: current, gh-pages shows {base_ref} as of {source}"
    oldest = min(int(ct) for _sha, ct in pending)
    age_days = (now - oldest) / 86400
    if age_days <= days:
        return 0, (
            f"gallery: {len(pending)} unpublished change(s) to deployed files, oldest "
            f"{age_days:.1f} day(s) old, within the {days:g}-day window"
        )
    return WARN_RC, (
        f"gallery: WARN {len(pending)} change(s) to deployed files on {base_ref} are "
        f"unpublished, the oldest {age_days:.0f} days old (gh-pages still shows {source}). "
        "Run `make deploy` when the gallery should show them."
    )


# --- self-test ---------------------------------------------------------------

def _run(repo: Path, *args: str, env: dict | None = None) -> None:
    full = dict(os.environ, **(env or {}))
    subprocess.run(  # noqa: S603
        ["git", "-C", str(repo), *args], check=True, capture_output=True, env=full
    )


def _commit(repo: Path, path: str, text: str, when: int, subject: str) -> None:
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    (repo / path).write_text(text)
    date = f"@{when} +0000"
    _run(repo, "add", path)
    _run(repo, "commit", "-q", "-m", subject,
         env={"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date})


def _self_test() -> int:
    """The by-design warning must fire, and the quiet cases must stay quiet."""
    ok = True
    now = 1_800_000_000
    day = 86400

    def expect(label: str, got: tuple[int, str], want_rc: int) -> None:
        nonlocal ok
        flag = "ok  " if got[0] == want_rc else "FAIL"
        if got[0] != want_rc:
            ok = False
        # Indented so a case's message can never read as the gate's own WARN line.
        print(f"  {flag}  {label} -> rc={got[0]} {got[1]}")

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "r"
        repo.mkdir()
        _run(repo, "init", "-q", "-b", "master")
        _run(repo, "config", "user.email", "t@example.com")
        _run(repo, "config", "user.name", "t")
        _run(repo, "config", "commit.gpgsign", "false")
        _commit(repo, "index.html", "v1", now - 30 * day, "first gallery")
        source = _git(repo, "rev-parse", "--short", "HEAD")
        _run(repo, "branch", "gh-pages")
        _run(repo, "checkout", "-q", "gh-pages")
        _commit(repo, "index.html", "v1 deployed", now - 30 * day, f"Deploy gallery from master ({source})")
        _run(repo, "checkout", "-q", "master")
        paths = ["index.html", "assets"]

        expect("fresh deploy, nothing changed: quiet",
               check(repo, paths, 7, "master", now), 0)

        _commit(repo, "docs/notes.md", "x", now - 10 * day, "a doc, not deployed")
        expect("only a non-deployed path changed 10 days ago: quiet",
               check(repo, paths, 7, "master", now), 0)

        _commit(repo, "assets/a.css", "x", now - 2 * day, "deployed file, 2 days ago")
        expect("deployed path changed 2 days ago: quiet",
               check(repo, paths, 7, "master", now), 0)

        _commit(repo, "index.html", "v2", now - 10 * day, "deployed file, 10 days ago")
        expect("deployed path changed 10 days ago: WARN",
               check(repo, paths, 7, "master", now), WARN_RC)

        _run(repo, "checkout", "-q", "gh-pages")
        _commit(repo, "index.html", "by hand", now - day, "hand edit on gh-pages")
        _run(repo, "checkout", "-q", "master")
        expect("gh-pages tip is not a deploy line: WARN",
               check(repo, paths, 7, "master", now), WARN_RC)

        _run(repo, "branch", "-D", "gh-pages")
        expect("no gh-pages ref: skip, quiet",
               check(repo, paths, 7, "master", now), 0)

    print("gallery --self-test: " + ("all cases behaved as designed" if ok else "a case FAILED"))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--days", type=float, default=7, help="warn past this many days (default 7)")
    ap.add_argument("--base", default=None, help="ref to compare against (default origin/master, else HEAD)")
    ap.add_argument("paths", nargs="*", help="the paths `make deploy` copies")
    args = ap.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.paths:
        print("gallery: no deployed paths given; pass $(DEPLOY_PATHS)", file=sys.stderr)
        return 1
    rc, msg = check(ROOT, args.paths, args.days, args.base)
    print(msg)
    return rc


if __name__ == "__main__":
    sys.exit(main())
