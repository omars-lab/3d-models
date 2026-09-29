#!/usr/bin/env python3
"""List every worktree, branch, stash and open PR across our repos, and say which can go.

A cleanup only loses work when something is deleted that main does not hold. This prints, per
repo, what would be lost if each thing went away, so the delete list is read off the output
instead of worked out by hand (the fifth cross-repo cleanup, 2026-09-29, is why it exists).

  python3 tools/branch_inventory.py ../bikar-main ../qiyas [...]
  python3 tools/branch_inventory.py            # the repos in DEFAULT_REPOS

For each branch, "merged" means one of: it is an ancestor of the default branch, or every file it
changed since its fork point has the same content on the default branch (a squash merge). Anything
else is "UNIQUE" and must not be deleted without a look. A worktree with uncommitted or untracked
files is "DIRTY"; its files are not in any commit and are listed.

Read-only: it runs `git fetch` (so the default branch is current) and nothing that writes.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

GIT = Path.home() / "Workspace/git"
DEFAULT_REPOS = ["3d-models", "bikar-main", "qiyas", "sacred-patterns", "3d-model-hub", "youtube", "hifth", "review-md"]


def run(repo, *args, check=False):
    r = subprocess.run(args, cwd=repo, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def git(repo, *args):
    return run(repo, "git", *args)


def default_ref(repo):
    head = git(repo, "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD")
    if head:
        return head
    for name in ("origin/main", "origin/master", "main", "master"):
        if git(repo, "rev-parse", "-q", "--verify", name):
            return name
    return "HEAD"


def branch_state(repo, ref, base):
    """(verdict, ahead) for one branch against the default branch."""
    ahead = int(git(repo, "rev-list", "--count", f"{base}..{ref}") or 0)
    if ahead == 0:
        return "merged (ancestor)", 0
    fork = git(repo, "merge-base", base, ref)
    files = git(repo, "diff", "--name-only", fork, ref).splitlines()
    if not files:
        return "merged (no changes)", ahead
    if not git(repo, "diff", "--name-only", ref, base, "--", *files):
        return "merged (content on default)", ahead
    return "UNIQUE", ahead


def worktrees(repo):
    out, cur = [], {}
    for line in git(repo, "worktree", "list", "--porcelain").splitlines() + [""]:
        if not line:
            if cur:
                out.append(cur)
            cur = {}
            continue
        key, _, val = line.partition(" ")
        cur[key] = val or True
    return out


def report(name, repo, prs):
    git(repo, "fetch", "-q", "--prune", "origin")
    base = default_ref(repo)
    print(f"\n## {name}  (default {base}, remote {git(repo, 'remote', 'get-url', 'origin') or 'none'})")
    checked_out = set()
    print("worktrees:")
    for wt in worktrees(repo):
        if wt.get("bare"):
            print(f"  {wt['worktree']}  bare")
            continue
        path = wt["worktree"]
        br = wt.get("branch", "").removeprefix("refs/heads/")
        checked_out.add(br)
        status = git(path, "status", "--porcelain").splitlines()
        where = br or f"detached {wt.get('HEAD', '')[:7]}"
        extra = ""
        if not br:
            v, ahead = branch_state(repo, wt["HEAD"], base)
            extra = f"  head {v}" + (f" +{ahead}" if ahead else "")
        print(f"  {path}  [{where}]{extra}  {'DIRTY ' + str(len(status)) if status else 'clean'}")
        for s in status[:12]:
            print(f"      {s}")
        if len(status) > 12:
            print(f"      … {len(status) - 12} more")
    print("local branches:")
    for br in git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines():
        v, ahead = branch_state(repo, br, base)
        up = git(repo, "rev-parse", "-q", "--verify", f"origin/{br}")
        mark = " (checked out)" if br in checked_out else ""
        print(f"  {br:45} {v}{f' +{ahead}' if ahead else ''}{'' if up else '  no remote'}{mark}")
    print("remote branches:")
    for br in git(repo, "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").splitlines():
        if br in ("origin/HEAD", "origin", base):
            continue
        v, ahead = branch_state(repo, br, base)
        print(f"  {br:45} {v}{f' +{ahead}' if ahead else ''}")
    stashes = git(repo, "stash", "list").splitlines()
    print(f"stashes: {len(stashes)}")
    for s in stashes:
        print(f"  {s}")
    if prs:
        slug = run(repo, "gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
        if slug:
            open_prs = json.loads(run(repo, "gh", "pr", "list", "-R", slug, "--state", "open",
                                      "--json", "number,headRefName,title") or "[]")
            print(f"open PRs: {len(open_prs)}")
            for p in open_prs:
                print(f"  #{p['number']} {p['headRefName']}: {p['title']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("repos", nargs="*", help="repo paths (default: our repos under ~/Workspace/git)")
    ap.add_argument("--no-prs", action="store_true", help="skip the GitHub open-PR lookup")
    a = ap.parse_args()
    paths = [Path(p) for p in a.repos] or [GIT / r for r in DEFAULT_REPOS]
    for p in paths:
        if not (p / ".git").exists() and not (p / "HEAD").exists():
            print(f"\n## {p.name}: not a git repo, skipped", file=sys.stderr)
            continue
        report(p.name, p.resolve(), not a.no_prs)


if __name__ == "__main__":
    main()
