---
name: git-and-gh-mechanics
description: git/gh traps met across the orb repos — silent whole-add abort on a bad pathspec, denied amend+force-push, local --delete-branch failing while the remote merge succeeded, fresh branches off origin/main after squash, no-CI merges
metadata:
  type: feedback
---

- `git add a b c` with one nonexistent pathspec aborts the ENTIRE add silently; check the commit's "N files changed" before pushing (a PR once shipped without its docs).
- Amend + force-push on a pushed branch is permission-denied here; push a plain follow-up commit.
- `gh pr merge --delete-branch` fails locally when `main` is checked out in another worktree, but the REMOTE merge already succeeded — verify with `gh pr view --json state,mergedAt`, don't retry. `gh pr merge --admin` is blocked by the auto-mode classifier; wait for mergeability to recompute after a force-push and re-merge plainly.
- Squash merges break ancestry: branch every milestone fresh off `origin/main` (`git fetch origin` first — a stale local ref pins the use-case map to a commit lacking the new file).
- 3d-models has no CI, so a MERGEABLE/CLEAN PR merges immediately; a "red" check that ran 0 steps in ~2 s is the billing block, not a failure.
- A rerun of a failed workflow reuses the definition at the original SHA; workflow fixes need a fresh run (`workflow_dispatch`).
- Verify "merged" by sentinel content in the target branch, not by subject match, before deleting a branch or resetting a diverged local main.

**Why:** each produced a wrong "done" or a lost change once.

**How to apply:** count files in the commit, verify merges remotely, never stack ([[stacked-pr-stranding]]), never `--auto` ([[gh-auto-merge-footgun]]), always PR ([[pr-flow-for-all-repos]]), read main's CI first ([[check-main-ci-not-just-the-pr]]).
