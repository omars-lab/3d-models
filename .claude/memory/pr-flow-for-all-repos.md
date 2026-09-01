---
name: pr-flow-for-all-repos
description: "All changes to every repo — docs and memory included — go through a PR, never direct-to-master; every merge ends with the closing checklist (worktree, local branch, remote branch gone)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 27e89d38-2159-4b95-9416-70151c40cbd0
  modified: 2026-08-06T15:44:07.432Z
---

Route **every** change through a branch → PR → merge, in all repos, **including docs-only commits to 3d-models**. Do not push directly to `master`/`main`.

**Why:** the standing directive is "merge everything back to main via prs" so work-tree changes are not lost and there is a review surface. On 2026-08-06 the #104 docs half was pushed straight to 3d-models master (`03facc4`) while the bikar half correctly went through PR #79; asked how to handle it, the user chose "Leave it, PR next time" — i.e. accept that one, but PR going forward, docs included.

**How to apply:** for any repo change, create a branch, open a PR, let CI/gates go green, then merge. Never `git push origin master` with local commits that never saw a PR. Docs-only is NOT an exemption. See [[islamic-orb-project]] for the #104 context and [[gh-auto-merge-footgun]] for the merge-timing trap (poll to green, don't `--auto` blindly).

**Closing checklist (added 2026-09-01, after the re-audit found it recurring):** a merge is not
done until `git worktree remove <wt>` (if any), `git branch -D <local>` and
`git push origin --delete <remote>` have all run — or `gh pr merge --squash --delete-branch`
plus the local delete. The per-task worktree flow removed the worktree and the remote every
time but left the local branch **every** time, and twice left the remote too; by 2026-09-01
that was 8 stale locals in 3d-models, 9 in bikar, 3 stale worktrees and 6 stale remotes across
both — the 2026-08-30 "remote = main only" state had silently regressed. Verify "merged" by
`gh pr list --state merged --head <branch>` (a squash makes `ahead` meaningless), never by
subject match, and never touch a branch with no PR: it is someone's unmerged work.

**Memory edits are changes too:** they go through the same branch → PR → merge. Leaving
`MEMORY.md` dirty in the working tree "for later" is how 2026-08-31's index-line edit sat
uncommitted across sessions. See [[islamic-orb-project]] for the 2026-09-01 audit record.
