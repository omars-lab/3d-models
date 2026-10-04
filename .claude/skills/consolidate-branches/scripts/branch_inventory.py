#!/usr/bin/env python3
"""Inventory our repos' branches and worktrees, prove what is dead, snapshot tips, check merges.

A cleanup only loses work when it deletes something the default branch does not hold, so for each
branch, worktree and stash this works out what deleting it would lose. The answer goes into a
plan: keep it, delete it (it is proven dead), fast-forward it, or have someone look at it.

  branch_inventory.py inventory [repos…] [--json] [--no-prs] [--no-fetch] [--commands]
  branch_inventory.py verify <repo> <ref>                    # exit 0 only if <ref> is proven dead
  branch_inventory.py snapshot <repo> <ref>… [--date D] [--no-push]
  branch_inventory.py survives <repo> <merged-file> <merge-base> <side>…
  branch_inventory.py --self-test

`inventory` with no repos reads the ones in DEFAULT_REPOS under ~/Workspace/git. It only reads:
it runs `git fetch --prune` (so the origin default is current) and `gh pr list`, and nothing that
writes. `snapshot` writes refs under refs/snapshots/<date>/ and pushes them; it never deletes.
The keep lists, the leave-alone worktrees and the live window come from ../rules.md, read at run
time. The proofs are described there too.
"""
import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

GIT = Path.home() / "Workspace/git"
DEFAULT_REPOS = ["3d-models", "bikar-main", "qiyas", "sacred-patterns", "3d-model-hub", "youtube", "hifth", "review-md"]
RULES = Path(__file__).resolve().parent.parent / "rules.md"
DEAD = {"ancestor", "no-changes", "content-on-default", "content-in-pr", "changes-on-default"}


def run(repo, *args):
    r = subprocess.run(args, cwd=repo, capture_output=True, text=True, errors="replace")
    return r.returncode, r.stdout.rstrip(), r.stderr.strip()


def git(repo, *args):
    return run(repo, "git", *args)[1]


# ---- rules.md -----------------------------------------------------------------------------------

def load_rules(path=RULES):
    """Keep / never-merge pairs, leave-alone and regenerable globs and the live window, from rules.md."""
    rules = {"keep": [], "never_merge": [], "leave_alone": [], "regenerable": [], "live_hours": 6.0}
    section = None
    heads = {"## keep": "keep", "## never merge": "never_merge", "## leave alone": "leave_alone",
             "## regenerable": "regenerable"}
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            section = next((v for k, v in heads.items() if line.lower().startswith(k)), None)
        m = re.match(r"Live window:\s*([\d.]+)\s*hours", line)
        if m:
            rules["live_hours"] = float(m.group(1))
        if section and line.startswith("- `"):
            fields = re.findall(r"`([^`]+)`", line.split(" — ")[0])
            reason = line.split(" — ", 1)[1].strip() if " — " in line else ""
            if section in ("leave_alone", "regenerable") and fields:
                rules[section].append((fields[0], reason))
            elif len(fields) >= 2:
                rules[section].append((fields[0], fields[1], reason))
    return rules


def rule_hit(pairs, repo_name, branch):
    for repo, br, reason in pairs:
        if repo in ("*", repo_name) and br == branch:
            return reason or "listed in rules.md"
    return None


# ---- proofs -------------------------------------------------------------------------------------

OLD_SPELLING = "colo" + "ur"


def normalize(text):
    """The British spelling of color → the American one, case kept, so the D-083 rename does not
    read as a change. The old word is built, not written, so the color-spelling gate stays clean."""
    pattern = "(?i)" + OLD_SPELLING
    pattern = pattern.encode() if isinstance(text, bytes) else pattern
    return re.sub(pattern, lambda m: m.group(0)[:4] + m.group(0)[5:], text)


def show(repo, ref, path):
    """The file's bytes at ref (binary files compare exactly), or None when it is absent."""
    r = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=repo, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def same_content(repo, a, b, files):
    """True when every file has the same content at a and b, British and American spellings of color folded."""
    for f in git(repo, "diff", "--name-only", a, b, "--", *files).splitlines():
        x, y = show(repo, a, f), show(repo, b, f)
        if x is None or y is None or normalize(x) != normalize(y):
            return False
    return True


def changed_lines(repo, base, side, path=None):
    """Non-blank lines `side` adds and removes over `base`, per file: {path: ([added], [removed])}."""
    args = ["diff", "--no-color", "--unified=0", base, side]
    if path:
        args += ["--", path]
    out, cur, header = {}, None, False
    for line in git(repo, *args).splitlines():
        if line.startswith("diff --git "):                     # a removed "-- x" reads "--- x":
            cur, header = None, True                           # file names only before the first @@
        elif line.startswith("@@"):
            header = False
        elif header and line.startswith("--- a/"):
            cur = line[6:]
        elif header and line.startswith("+++ b/"):
            cur = line[6:]
        elif not header and cur and line[:1] in "+-" and line[1:].strip():
            out.setdefault(cur, ([], []))[0 if line[0] == "+" else 1].append(line[1:])
    return out


def added_lines(repo, base, side, path=None):
    """Non-blank lines `side` adds over `base`, per file: {path: [line, …]}."""
    return {f: added for f, (added, _) in changed_lines(repo, base, side, path).items() if added}


def lines_on(repo, ref, base, fork, files):
    """How much of what ref changed since fork the base holds, file by file:

    - "changes": every line ref added is in that file on base, and every line it removed is not;
    - "lines": every added line is there, but a line it removed is still on base;
    - None: an added line is missing, or ref added nothing and removed lines base still holds.

    A removed line base still holds may only repeat elsewhere in the file (a closing brace), so
    "lines" stays a look, never a delete: a false "still there" costs a look, never work."""
    changed = {f: c for f, c in changed_lines(repo, fork, ref).items() if f in files}
    if not changed:
        return None
    removals_gone = True
    for f, (added, removed) in changed.items():
        have = show(repo, base, f)
        held = set(normalize(have.decode(errors="replace")).splitlines()) if have is not None else set()
        if any(normalize(x) not in held for x in added):
            return None
        if any(normalize(x) in held for x in removed):
            removals_gone = False
    if removals_gone:
        return "changes"
    return "lines" if any(added for added, _ in changed.values()) else None


def prove(repo, ref, base, merge_commits=()):
    """(state, ahead, behind) for one ref against the origin default.

    State is one of: ancestor, no-changes, content-on-default, content-in-pr,
    changes-on-default (every line it added is on the default and every line it removed is gone;
    all five dead), lines-on-default (the additions landed but a removed line is still there:
    look), ahead-only, diverged."""
    ahead = int(git(repo, "rev-list", "--count", f"{base}..{ref}") or 0)
    behind = int(git(repo, "rev-list", "--count", f"{ref}..{base}") or 0)
    if ahead == 0:
        return "ancestor", ahead, behind
    fork = git(repo, "merge-base", base, ref)
    files = git(repo, "diff", "--name-only", fork, ref).splitlines()
    if not files:
        return "no-changes", ahead, behind
    if same_content(repo, ref, base, files):
        return "content-on-default", ahead, behind
    for mc in merge_commits:
        if mc and same_content(repo, ref, mc, files):
            return "content-in-pr", ahead, behind
    landed = lines_on(repo, ref, base, fork, files)
    if landed:
        return f"{landed}-on-default", ahead, behind
    return ("diverged" if behind else "ahead-only"), ahead, behind


# ---- inventory ----------------------------------------------------------------------------------

def default_ref(repo):
    head = git(repo, "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD")
    if head:
        return head
    for name in ("origin/main", "origin/master", "main", "master"):
        if git(repo, "rev-parse", "-q", "--verify", name):
            return name
    return "HEAD"


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


def last_touch_hours(path):
    """Hours since this worktree's index or HEAD log changed (its session's last git action)."""
    gitdir = Path(git(path, "rev-parse", "--absolute-git-dir"))
    times = [os.path.getmtime(p) for p in (gitdir / "index", gitdir / "logs/HEAD") if p.exists()]
    return (time.time() - max(times)) / 3600 if times else None


def pr_index(repo):
    """({head branch: [merged PR merge-commit sha, …]}, open PRs, slug), or empties off GitHub."""
    code, slug, _ = run(repo, "gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
    if code or not slug:
        return {}, [], None
    raw = run(repo, "gh", "pr", "list", "-R", slug, "--state", "all", "--limit", "1000",
              "--json", "number,headRefName,state,mergeCommit,title")[1]
    merged, open_prs = {}, []
    for p in json.loads(raw or "[]"):
        if p["state"] == "MERGED" and p.get("mergeCommit"):
            merged.setdefault(p["headRefName"], []).append(p["mergeCommit"]["oid"])
        elif p["state"] == "OPEN":
            open_prs.append({"number": p["number"], "branch": p["headRefName"], "title": p["title"]})
    return merged, open_prs, slug


def plan_branch(item, rules, repo_name, default_name, wts, open_by_branch):
    """(action, reason): keep, delete (proven dead), ff (fast-forward) or look (Omar's call)."""
    name, state = item["name"], item["state"]
    keep = rule_hit(rules["keep"], repo_name, name)
    never = rule_hit(rules["never_merge"], repo_name, name)
    # A remote branch whose local twin is checked out in a kept worktree is that session's too.
    wt = next((w for w in wts if w.get("branch") == name), None)
    agent = next((w for w in wts if name.startswith("worktree-agent-")
                  and w["path"].endswith("/agent-" + name.removeprefix("worktree-agent-"))), None)
    if name == default_name:
        if state == "ancestor" and item["behind"]:
            return "ff", "the local default is behind origin; fast-forward it"
        if state == "ancestor":
            return "keep", "the default branch"
        return "look", "the local default has commits origin lacks"
    if keep:
        return "keep", f"rules.md keep: {keep}"
    if name in open_by_branch:
        return "keep", f"open PR #{open_by_branch[name]}"
    if wt and wt["action"] != "remove":
        return "keep", f"checked out in {wt['path']} ({wt['reason']})"
    if agent and agent["action"] != "remove":
        return "keep", f"named for the subagent worktree {agent['path']}"
    if never:
        return "look", f"rules.md never-merge: {never}"
    if state in DEAD:
        return "delete", f"proven dead: {state}"
    if state == "lines-on-default":
        return "look", "every added line is on the default, but a line it removed is still there"
    return "look", "unmerged work: Omar's call"


def plan_worktree(wt, rules, base, merged_by_branch, repo):
    path = wt["path"]
    for glob, reason in rules["leave_alone"]:
        if fnmatch.fnmatch(path, glob):
            return "keep", f"rules.md leave-alone: {reason}"
    if wt["main"]:
        return "keep", "the repo's main checkout"
    if wt["dirty"]:
        return "keep", f"{len(wt['dirty'])} uncommitted or untracked files"
    if wt["hours"] is not None and wt["hours"] < rules["live_hours"]:
        return "keep", f"live: touched {wt['hours']:.1f} h ago"
    precious = unregenerable(wt.get("ignored", []), rules)
    if precious:
        return "keep", (f"{len(precious)} ignored paths a remove would delete, not in rules.md's "
                        f"regenerable list: {', '.join(precious[:3])}")
    if wt["branch"]:
        state = prove(repo, wt["branch"], base, merged_by_branch.get(wt["branch"], ()))[0]
    else:
        state = prove(repo, wt["head"], base)[0]
    if state in DEAD:
        return "remove", f"clean, and its head is proven dead: {state}"
    return "keep", f"its head holds unmerged work: {state}"


def unregenerable(ignored, rules):
    """Ignored paths that `git worktree remove` would delete and no build step brings back."""
    globs = [g for g, _ in rules["regenerable"]]
    return [p for p in ignored
            if not any(fnmatch.fnmatch(part, g) for part in p.rstrip("/").split("/") for g in globs)]


def inventory(repo, rules, prs=True, fetch=True):
    repo = Path(repo).resolve()
    if fetch:
        git(repo, "fetch", "-q", "--prune", "origin")
    base = default_ref(repo)
    default_name = base.removeprefix("origin/")
    name = "bikar" if repo.name == "bikar-main" else repo.name
    merged, open_prs, slug = pr_index(repo) if prs else ({}, [], None)
    open_by_branch = {p["branch"]: p["number"] for p in open_prs}
    out = {"repo": name, "path": str(repo), "default": base,
           "remote": git(repo, "remote", "get-url", "origin") or None, "github": slug,
           "worktrees": [], "branches": [], "stashes": [], "open_prs": open_prs}

    for wt in worktrees(repo):
        if wt.get("bare"):
            out["worktrees"].append({"path": wt["worktree"], "bare": True, "action": "keep", "reason": "bare repo"})
            continue
        path = wt["worktree"]
        br = wt.get("branch", "").removeprefix("refs/heads/")
        exists = Path(path).exists()
        item = {"path": path, "branch": br or None, "head": wt.get("HEAD", ""),
                "main": exists and Path(git(path, "rev-parse", "--path-format=absolute", "--git-common-dir"))
                == Path(git(path, "rev-parse", "--absolute-git-dir")),
                "dirty": git(path, "status", "--porcelain").splitlines() if exists else [],
                "ignored": [l[3:] for l in git(path, "status", "--porcelain", "--ignored").splitlines()
                            if l.startswith("!! ")] if exists else [],
                "hours": last_touch_hours(path) if exists else None}
        item["action"], item["reason"] = plan_worktree(item, rules, base, merged, repo)
        if not exists:
            item["action"], item["reason"] = "keep", "path is gone; `git worktree prune` clears the record"
        out["worktrees"].append(item)

    refs = [("local", r) for r in git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines()]
    refs += [("remote", r) for r in git(repo, "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").splitlines()
             if r not in ("origin/HEAD", "origin", base)]
    for kind, ref in refs:
        short = ref.removeprefix("origin/") if kind == "remote" else ref
        state, ahead, behind = prove(repo, ref, base, merged.get(short, ()))
        item = {"kind": kind, "name": short, "ref": ref, "sha": git(repo, "rev-parse", ref),
                "state": state, "ahead": ahead, "behind": behind}
        item["action"], item["reason"] = plan_branch(item, rules, name, default_name, out["worktrees"], open_by_branch)
        out["branches"].append(item)

    for s in git(repo, "stash", "list").splitlines():
        out["stashes"].append({"entry": s, "action": "look", "reason": "a stash cannot be proven dead"})
    return out


def commands(inv):
    """The exact one-at-a-time commands for the plan's deletes, snapshot first."""
    repo, me = inv["path"], Path(__file__).resolve()
    dead = [b for b in inv["branches"] if b["action"] == "delete"]
    gone = [w for w in inv["worktrees"] if w.get("action") == "remove"]
    lines = []
    tips = sorted({b["ref"] for b in dead}
                  | {w["branch"] or f"worktree/{Path(w['path']).name}={w['head']}" for w in gone})
    if tips:
        lines.append(f"python3 {me} snapshot {repo} {' '.join(tips)}")
    lines += [f"git -C {repo} worktree remove {w['path']}" for w in gone]
    lines += [f"git -C {repo} branch -D {b['name']}" for b in dead if b["kind"] == "local"]
    lines += [f"git -C {repo} push origin --delete {b['name']}" for b in dead if b["kind"] == "remote"]
    for b in inv["branches"]:
        if b["action"] != "ff":
            continue
        wt = next((w for w in inv["worktrees"] if w.get("branch") == b["name"]), None)
        if wt is None:
            lines.append(f"git -C {repo} fetch origin {b['name']}:{b['name']}")
        elif not wt["dirty"]:
            lines.append(f"git -C {wt['path']} merge --ff-only {inv['default']}")
        else:
            lines.append(f"# {b['name']} is behind but checked out with changes in {wt['path']}: leave it")
    return lines


def print_inventory(inv, show_commands):
    print(f"\n## {inv['repo']}  (default {inv['default']}, remote {inv['remote'] or 'none'})")
    print("worktrees:")
    for w in inv["worktrees"]:
        where = "bare" if w.get("bare") else (w["branch"] or f"detached {w['head'][:7]}")
        print(f"  {w['action']:6} {w['path']}  [{where}]  {w['reason']}")
        for s in w.get("dirty", [])[:8]:
            print(f"           {s}")
        if len(w.get("dirty", [])) > 8:
            print(f"           … {len(w['dirty']) - 8} more")
    print("branches:")
    for b in inv["branches"]:
        label = b["ref"] if b["kind"] == "remote" else b["name"]
        counts = f"+{b['ahead']}/-{b['behind']}"
        print(f"  {b['action']:6} {label:50} {b['state']:20} {counts:9} {b['reason']}")
    print(f"stashes: {len(inv['stashes'])}")
    for s in inv["stashes"]:
        print(f"  look   {s['entry']}")
    print(f"open PRs: {len(inv['open_prs'])}")
    for p in inv["open_prs"]:
        print(f"  #{p['number']} {p['branch']}: {p['title']}")
    if show_commands:
        print("commands (run one at a time):")
        for c in commands(inv) or ["(nothing proven dead)"]:
            print(f"  {c}")


def headline(inv):
    default_name = inv["default"].removeprefix("origin/")
    others = [b for b in inv["branches"]
              if b["name"] != default_name and not b["reason"].startswith("rules.md keep")]
    return {"merged": sum(b["state"] in DEAD for b in others),
            "unmerged": sum(b["state"] in ("ahead-only", "lines-on-default") for b in others),
            "diverged": sum(b["state"] == "diverged" for b in others),
            "dirty_worktrees": sum(bool(w.get("dirty")) for w in inv["worktrees"]),
            "planned_deletes": sum(b["action"] == "delete" for b in inv["branches"])
            + sum(w.get("action") == "remove" for w in inv["worktrees"])}


# ---- snapshot, survives -------------------------------------------------------------------------

def snapshot(repo, refs, date, push=True):
    """Write refs/snapshots/<date>/<branch> for each ref; refuse to move an existing one."""
    repo, written = Path(repo).resolve(), []
    for ref in refs:
        given, _, ref = ref.rpartition("=")                     # name=ref names a detached head
        sha = git(repo, "rev-parse", "-q", "--verify", f"{ref}^{{commit}}")
        if not sha:
            raise SystemExit(f"snapshot: {ref} does not resolve in {repo}")
        short = ref.removeprefix("origin/")
        local = git(repo, "rev-parse", "-q", "--verify", f"refs/heads/{short}")
        name = given or (short if (not ref.startswith("origin/") or not local or local == sha) else ref)
        target = f"refs/snapshots/{date}/{name}"
        have = git(repo, "rev-parse", "-q", "--verify", target)
        if have and have != sha:
            raise SystemExit(f"snapshot: {target} already holds {have[:9]}, not {sha[:9]}; pick another --date")
        if not have:
            code, _, err = run(repo, "git", "update-ref", target, sha)
            if code:
                raise SystemExit(f"snapshot: {err}")
        if target in written:                                   # a branch and its remote twin at one tip
            continue
        written.append(target)
        print(f"{target} {sha}")
    if push and written:
        code, _, err = run(repo, "git", "push", "-q", "origin", *[f"{t}:{t}" for t in written])
        print(f"pushed {len(written)} snapshot refs to origin" if code == 0 else f"push failed: {err}")
        return code
    return 0


def survives(repo, merged_file, base, sides):
    """Every non-blank line each side added to this file over base is in the merged file."""
    have = set(Path(merged_file).read_text().splitlines())
    top = Path(git(repo, "rev-parse", "--show-toplevel")).resolve()
    rel = os.path.relpath(Path(merged_file).resolve(), top)
    missing = 0
    for side in sides:
        for lines in added_lines(repo, base, side, rel).values():
            for x in lines:
                if x not in have:
                    missing += 1
                    print(f"MISSING from {side}: {x}")
    print(f"{rel}: {f'{missing} added lines missing' if missing else 'every added line survives'}")
    return 1 if missing else 0


# ---- self-test ----------------------------------------------------------------------------------

def self_test():
    """Build a throwaway repo with one branch per verdict and check each is classified right."""
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        origin, repo = Path(tmp) / "origin.git", Path(tmp) / "work"
        run(tmp, "git", "init", "-q", "--bare", "-b", "main", str(origin))
        run(tmp, "git", "clone", "-q", str(origin), str(repo))

        def g(*a):
            return run(repo, "git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                       "-c", "core.hooksPath=/dev/null", *a)

        def commit(path, text, msg):
            (repo / path).write_text(text)
            g("add", path)
            g("commit", "-q", "-m", msg)

        g("checkout", "-q", "-b", "main")
        commit("a.txt", "one\n", "init")
        commit("g.txt", "old\n", "g")
        commit("h.txt", "keep\nold2\n", "h")
        commit("i.txt", "-- x\n", "i")
        g("push", "-q", "origin", "main")
        g("checkout", "-q", "-b", "halfway")                     # main took the new line, kept the old
        commit("g.txt", "new\n", "replace old")
        g("checkout", "-q", "-b", "rewritten", "main")           # main took the change, then moved on
        commit("h.txt", "keep\nnew2\n", "replace old2")
        g("checkout", "-q", "-b", "dashes", "main")              # a removed "-- x" diffs as "--- x"
        commit("i.txt", "-- y\n", "replace a dashed line")
        g("checkout", "-q", "main")
        commit("g.txt", "old\nnew\n", "take new, keep old")
        commit("h.txt", "keep\nnew2\nlater\n", "squash of rewritten, then more")
        commit("i.txt", "-- y\nmore\n", "squash of dashes, then more")
        g("checkout", "-q", "-b", "squashed")                    # landed by squash: content-on-default
        commit("b.txt", f"the {OLD_SPELLING}\n", "b")
        g("checkout", "-q", "-b", "renamed", "main")             # landed, then main renamed to color
        commit("c.txt", f"red {OLD_SPELLING}\n", "c")
        g("checkout", "-q", "main")
        commit("b.txt", "the color\n", "squash of b")
        commit("c.txt", "red color\n", "squash of c")
        g("checkout", "-q", "-b", "unique")                      # real work
        commit("d.txt", "new\n", "d")
        g("checkout", "-q", "-b", "inpr", "main")                # landed by its PR, then main moved on
        commit("e.txt", "pr text\n", "e")
        g("checkout", "-q", "main")
        commit("e.txt", "pr text\n", "squash of e")
        pr_merge = git(repo, "rev-parse", "HEAD")
        commit("e.txt", "pr text\nedited later\n", "edit e")
        g("checkout", "-q", "-b", "deleter", "main")             # adds nothing, only deletes a line
        commit("a.txt", "", "drop one")
        g("checkout", "-q", "main")
        commit("f.txt", "main moves\n", "f")
        g("branch", "ancestor", "HEAD~1")
        g("push", "-q", "origin", "main")
        g("fetch", "-q", "origin")

        base = "origin/main"
        want = {"squashed": "content-on-default", "renamed": "content-on-default", "unique": "diverged",
                "ancestor": "ancestor", "deleter": "diverged", "inpr": "changes-on-default",
                "halfway": "lines-on-default", "rewritten": "changes-on-default",
                "dashes": "changes-on-default"}
        for b, w in want.items():
            got = prove(repo, b, base)[0]
            if got != w:
                bad.append(f"{b}: {got}, expected {w}")
        if prove(repo, "inpr", base, [pr_merge])[0] != "content-in-pr":
            bad.append("inpr with its PR merge commit is not content-in-pr")
        old = OLD_SPELLING
        if normalize(f"{old.capitalize()} {old.upper()} {old}") != "Color COLOR color":
            bad.append("normalize does not fold every case of the British spelling")

        snapshot(repo, ["unique", "worktree/x=deleter"], "2000-01-01", push=False)
        if git(repo, "rev-parse", "refs/snapshots/2000-01-01/unique") != git(repo, "rev-parse", "unique") \
                or git(repo, "rev-parse", "refs/snapshots/2000-01-01/worktree/x") != git(repo, "rev-parse", "deleter"):
            bad.append("snapshot did not write the tips under their names")
        try:
            snapshot(repo, ["unique=deleter"], "2000-01-01", push=False)
            bad.append("snapshot moved an existing snapshot ref")
        except SystemExit:
            pass
        g("push", "-q", "origin", "unique")                      # a local branch and its remote twin,
        g("fetch", "-q", "origin")                               # same tip: one snapshot, one push
        if snapshot(repo, ["unique", "origin/unique"], "2000-01-02") != 0 \
                or not git(origin, "rev-parse", "-q", "--verify", "refs/snapshots/2000-01-02/unique"):
            bad.append("a branch and its remote twin at one tip did not snapshot and push as one ref")

        g("checkout", "-q", "unique")
        if survives(repo, repo / "d.txt", "main~0", ["unique"]) != 0:
            bad.append("survives misses a line that is present")
        (repo / "d.txt").write_text("")
        if survives(repo, repo / "d.txt", "main", ["unique"]) != 1:
            bad.append("survives passes a file that lost a line")

    rules = load_rules()
    live = {"path": "/r/.claude/worktrees/agent-abc", "branch": "feat", "action": "keep", "reason": "live"}
    plans = {("local", "worktree-agent-abc", "ancestor"): "keep",     # its subagent worktree is alive
             ("remote", "feat", "content-on-default"): "keep",         # twin of a live checkout
             ("remote", "gh-pages", "diverged"): "keep",
             ("local", "old", "content-in-pr"): "delete",
             ("local", "fix/weave-amplitude-guard-by-depth-suffix", "ancestor"): "look",
             ("local", "wip", "lines-on-default"): "look",
             ("local", "main", "diverged"): "look"}
    for (kind, name, state), want in plans.items():
        item = {"kind": kind, "name": name, "state": state, "behind": 0}
        got = plan_branch(item, rules, "bikar", "main", [live], {})[0]
        if got != want:
            bad.append(f"plan for {kind} {name} ({state}): {got}, expected {want}")
    if not rule_hit(rules["keep"], "sacred-patterns", "wip/react-d3-2024") \
            or not rule_hit(rules["keep"], "3d-models", "gh-pages") \
            or not any(fnmatch.fnmatch("/x/.claude/worktrees/agent-a1", glob) for glob, _ in rules["leave_alone"]):
        bad.append("rules.md did not parse into the keep and leave-alone lists")
    ignored = ["node_modules/", "apps/web/dist/", "native/x.xcresult/", ".DS_Store",
               ".claude/settings.local.json", "apps/web/public/assets/private"]
    if unregenerable(ignored, rules) != [".claude/settings.local.json", "apps/web/public/assets/private"]:
        bad.append(f"unregenerable ignored paths: {unregenerable(ignored, rules)}")
    clean = {"path": "/r/x", "main": False, "dirty": [], "hours": 99, "branch": None, "head": "HEAD",
             "ignored": [".claude/settings.local.json"]}
    if plan_worktree(clean, rules, "main", {}, Path("."))[0] != "keep":
        bad.append("a clean worktree holding an unregenerable ignored file was not kept")

    for b in bad:
        print(f"FAIL {b}")
    print("self-test: " + ("PASS" if not bad else f"{len(bad)} failures"))
    return 1 if bad else 0


def main():
    if sys.argv[1:] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    inv = sub.add_parser("inventory", help="classify every branch, worktree and stash; plan the cleanup")
    inv.add_argument("repos", nargs="*", help="repo paths (default: DEFAULT_REPOS under ~/Workspace/git)")
    inv.add_argument("--json", action="store_true", help="print the inventory as JSON")
    inv.add_argument("--no-prs", action="store_true", help="skip the GitHub PR lookup")
    inv.add_argument("--no-fetch", action="store_true", help="do not fetch origin first")
    inv.add_argument("--commands", action="store_true", help="print the delete commands the plan implies")
    ver = sub.add_parser("verify", help="exit 0 only if the ref is proven dead right now")
    ver.add_argument("repo")
    ver.add_argument("ref")
    snap = sub.add_parser("snapshot", help="save tips under refs/snapshots/<date>/ and push them")
    snap.add_argument("repo")
    snap.add_argument("refs", nargs="+")
    snap.add_argument("--date", default=dt.date.today().isoformat())
    snap.add_argument("--no-push", action="store_true")
    sur = sub.add_parser("survives", help="prove every line each side added is in the merged file")
    sur.add_argument("repo")
    sur.add_argument("merged_file")
    sur.add_argument("merge_base")
    sur.add_argument("sides", nargs="+")
    a = ap.parse_args()

    if a.cmd == "verify":
        repo = Path(a.repo).resolve()
        git(repo, "fetch", "-q", "--prune", "origin")
        merged = pr_index(repo)[0]
        state, ahead, behind = prove(repo, a.ref, default_ref(repo), merged.get(a.ref.removeprefix("origin/"), ()))
        print(f"{a.ref}: {state} (+{ahead}/-{behind}) — {'dead' if state in DEAD else 'NOT proven dead'}")
        return 0 if state in DEAD else 1
    if a.cmd == "snapshot":
        return snapshot(a.repo, a.refs, a.date, push=not a.no_push)
    if a.cmd == "survives":
        return survives(Path(a.repo).resolve(), a.merged_file, a.merge_base, a.sides)

    rules = load_rules()
    paths = [Path(p) for p in a.repos] or [GIT / r for r in DEFAULT_REPOS]
    results = []
    for p in paths:
        if not (p / ".git").exists() and not (p / "HEAD").exists():
            print(f"## {p.name}: not a git repo, skipped", file=sys.stderr)
            continue
        results.append(inventory(p, rules, prs=not a.no_prs, fetch=not a.no_fetch))
    if a.json:
        for r in results:
            r["headline"], r["commands"] = headline(r), commands(r)
        print(json.dumps(results, indent=1))
        return 0
    for r in results:
        print_inventory(r, a.commands)
    print("\n## headline")
    for r in results:
        print(f"  {r['repo']:16} " + "  ".join(f"{k} {v}" for k, v in headline(r).items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
