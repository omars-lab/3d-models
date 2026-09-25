#!/usr/bin/env python3
"""next_id — hand out the next free decision / FAQ id, and refuse a clash.

Two sessions have twice taken the same next decision id (D-051 on 2026-09-02,
D-055 on 2026-09-17). Each read "the last id + 1" from its own checkout, and
the clash only surfaced later as a merge conflict and a renumbering across
the docs. The session did not lack the rule; it had a stale view of the
number. So the number comes from a command, and a hook catches the clash.

  next D|Q    print the next free id. It looks at origin/master (fetched
              first unless --no-fetch), every local and origin branch, and
              this working tree, and names the branch holding any id above
              master's, since that branch has already claimed it.
  check       exit 1 when (a) one id heads two entries in the same file, or
              (b) an id this branch added is already on origin/master under a
              different title. First merged owns the id, so the branch that
              is still open renumbers. An added id that another branch holds
              under a different title is reported, not blocked: neither has
              merged yet. `--staged` reads the index (the hook); the default
              reads the working tree (`make validate-ids`).
  --self-test builds a throwaway repo with each case and checks the verdicts.

"Added by this branch" means absent from the file at the merge base of HEAD
and origin/master. The check does not fetch: it judges against origin/master
as of the last fetch, which `next` refreshes.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KINDS = {
    "D": ("docs/decisions-log.md", re.compile(r"^## (D-\d{3}) — (.+?)\s*$", re.M)),
    "Q": ("docs/faq.md", re.compile(r"^## (Q-\d{3}) — (.+?)\s*$", re.M)),
}
MASTER = "origin/master"


def git(root: Path, *args: str) -> str | None:
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def heads(text: str | None, pat: re.Pattern) -> list[tuple[str, str]]:
    return pat.findall(text or "")


def at(root: Path, ref: str, path: str) -> str | None:
    """The file at a ref ('' ref = the index), or None when absent there."""
    return git(root, "show", f"{ref}:{path}")


def branches(root: Path) -> list[str]:
    out = git(root, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes") or ""
    return [r for r in out.split() if r not in ("origin/HEAD", "origin", MASTER)
            and "gh-pages" not in r]


def num(i: str) -> int:
    return int(i.split("-")[1])


def next_id(root: Path, kind: str) -> tuple[str, list[str]]:
    path, pat = KINDS[kind]
    master = {i for i, _ in heads(at(root, MASTER, path), pat)}
    top = max(map(num, master), default=0)
    notes, seen = [], set(master)
    wt = root / path
    sources = [(b, at(root, b, path)) for b in branches(root)]
    sources.append(("working tree", wt.read_text() if wt.exists() else None))
    for name, text in sources:
        mine = {i for i, _ in heads(text, pat)} - master
        if mine:
            seen |= mine
            notes.append(f"{name} holds {', '.join(sorted(mine, key=num))} (not on {MASTER})")
    top = max(map(num, seen), default=0)
    return f"{kind}-{top + 1:03d}", notes


def check(root: Path, staged: bool) -> list[tuple[str, str]]:
    """(level, message) findings; level is BLOCK or NOTE."""
    out = []
    base = (git(root, "merge-base", "HEAD", MASTER) or "").strip()
    here = (git(root, "rev-parse", "--abbrev-ref", "HEAD") or "").strip()
    for kind, (path, pat) in KINDS.items():
        text = at(root, "", path) if staged else (
            (root / path).read_text() if (root / path).exists() else None)
        if text is None:
            continue
        mine = heads(text, pat)
        ids = [i for i, _ in mine]
        for i in sorted({i for i in ids if ids.count(i) > 1}, key=num):
            out.append(("BLOCK", f"{path}: {i} heads {ids.count(i)} entries"))
        before = {i for i, _ in heads(at(root, base, path), pat)} if base else set()
        master = dict(heads(at(root, MASTER, path), pat))
        others = [(b, dict(heads(at(root, b, path), pat))) for b in branches(root) if b != here]
        for i, title in mine:
            if i in before:
                continue
            if i in master and master[i] != title:
                out.append(("BLOCK", f"{path}: {i} is already on {MASTER} as "
                                     f"“{master[i]}”; this branch added it as “{title}”. "
                                     f"First merged owns the id: renumber this one "
                                     f"(`python3 tools/next_id.py next {kind}`) and "
                                     f"`git grep -n {i}` for every reference"))
            for b, theirs in others:
                if i in theirs and theirs[i] != title and i not in master:
                    out.append(("NOTE", f"{path}: {i} is also claimed on {b} as "
                                        f"“{theirs[i]}”; whichever merges second renumbers"))
    return out


# ------------------------------------------------------------------ self-test


def _repo(tmp: Path) -> Path:
    """A repo whose origin/master has D-001 and D-002; HEAD branched at D-001."""
    r = tmp / "r"
    r.mkdir()
    g = lambda *a: subprocess.run(["git", "-C", str(r), *a], check=True, capture_output=True)
    g("init", "-q", "-b", "work")
    g("config", "user.email", "t@t")
    g("config", "user.name", "t")
    log = r / KINDS["D"][0]
    log.parent.mkdir(parents=True)
    log.write_text("# Log\n\n## D-001 — first\n")
    g("add", ".")
    g("commit", "-qm", "base")
    g("branch", "other")
    g("checkout", "-q", "-b", "m")
    log.write_text("# Log\n\n## D-001 — first\n\n## D-002 — master took it\n")
    g("commit", "-qam", "master")
    g("update-ref", f"refs/remotes/{MASTER}", "HEAD")
    g("checkout", "-q", "other")
    log.write_text("# Log\n\n## D-001 — first\n\n## D-003 — other branch reserved\n")
    g("commit", "-qam", "other")
    g("checkout", "-q", "work")
    g("branch", "-D", "m")
    return r


def self_test() -> int:
    ok = True

    def expect(label, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"self-test {'ok  ' if good else 'FAIL'}: {label} → {got!r}"
              + ("" if good else f" (wanted {want!r})"))

    with tempfile.TemporaryDirectory() as t:
        r = _repo(Path(t))
        log = r / KINDS["D"][0]
        nid, notes = next_id(r, "D")
        expect("next skips master's D-002 and the other branch's D-003", nid, "D-004")
        expect("next names the branch that holds an id above master", len(notes), 1)

        log.write_text("# Log\n\n## D-001 — first\n\n## D-002 — mine, written from a stale view\n")
        levels = [lv for lv, _ in check(r, staged=False)]
        expect("an added id master already has, under another title, blocks", levels, ["BLOCK"])

        log.write_text("# Log\n\n## D-001 — first\n\n## D-002 — master took it\n")
        expect("the same id and title as master (a rebased branch) passes",
               check(r, staged=False), [])

        log.write_text("# Log\n\n## D-001 — first\n\n## D-003 — mine\n")
        expect("an id only another open branch claims is a note, not a block",
               [lv for lv, _ in check(r, staged=False)], ["NOTE"])

        log.write_text("# Log\n\n## D-001 — first\n\n## D-001 — first again\n")
        expect("one id heading two entries blocks",
               [lv for lv, _ in check(r, staged=False)], ["BLOCK"])

        log.write_text("# Log\n\n## D-001 — first, retitled\n")
        expect("retitling an id the branch did not add is not a clash",
               check(r, staged=False), [])

        log.write_text("# Log\n\n## D-001 — first\n\n## D-004 — mine\n")
        subprocess.run(["git", "-C", str(r), "add", "."], check=True)
        log.write_text("# Log\n\n## D-001 — first\n\n## D-002 — unstaged edit\n")
        expect("--staged judges the index, not the working tree",
               check(r, staged=True), [])

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb")
    n = sub.add_parser("next")
    n.add_argument("kind", choices=sorted(KINDS))
    n.add_argument("--no-fetch", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--staged", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.verb == "next":
        if not a.no_fetch and git(REPO, "fetch", "--quiet", "origin") is None:
            print(f"warning: fetch failed; using {MASTER} as last fetched", file=sys.stderr)
        nid, notes = next_id(REPO, a.kind)
        print(nid)
        for x in notes:
            print(f"  {x}", file=sys.stderr)
        return 0
    if a.verb == "check":
        found = check(REPO, a.staged)
        for lv, msg in found:
            print(f"{lv}: {msg}", file=sys.stderr)
        if any(lv == "BLOCK" for lv, _ in found):
            return 1
        print("ids: no clash")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
