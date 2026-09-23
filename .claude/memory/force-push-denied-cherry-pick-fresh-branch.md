---
name: force-push-denied-cherry-pick-fresh-branch
description: Auto mode denies `git push --force-with-lease` ("Git Destructive"); after a squash-merge upstream, rebuild a stale branch by cherry-picking its own commits onto a fresh branch off origin/main and opening a new PR
metadata:
  type: feedback
---

The auto-mode classifier refuses `git push --force-with-lease` (and any force push) as
"Git Destructive". So a rebase is useless: the rebased branch cannot be pushed.

**Why:** After bikar #193/#194/#195 squash-merged, `feat/naqsh-transforms` still carried
#193's pre-squash commits; merging origin/main into it conflicted in 12 files. Cherry-picking
only the two branch-specific commits (df0aa69, 0c95ecb) onto `feat/naqsh-transforms-on-main`
(fresh from origin/main) gave one trivial conflict and a clean PR (#197). See
[[stacked-pr-stranding]] for why the stale base happens.

**How to apply:** Never rebase + force-push in auto mode. When a branch's base was
squash-merged: `git switch -c <name>-on-main origin/main`, `git cherry-pick <own commits>`,
push the NEW branch, open a NEW PR, delete the superseded remote branch (non-force
`git push origin --delete`) after merge. Bikar cherry-picks/commits also need
[[bikar-registry-hook-reads-shared-checkout]].
