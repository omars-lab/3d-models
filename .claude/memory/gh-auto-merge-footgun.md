---
name: gh-auto-merge-footgun
description: "NaqshCoffee repos have auto-merge disabled, so `gh pr merge --auto` merges immediately instead of waiting for CI"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 416aa36c-c7af-4cf1-91db-d2cdc9668841
  modified: 2026-07-31T10:43:38.292Z
---

`NaqshCoffee/bikar` and `NaqshCoffee/qiyas` both have `allow_auto_merge=false`
(verified 2026-07-31 via `gh api repos/OWNER/REPO -q .allow_auto_merge`). On a repo
without auto-merge enabled, `gh pr merge --auto` does **not** error — it silently falls
back to an **immediate** merge. qiyas#5 and bikar#31 both landed while CI was still
running because of this.

**Why:** the flag reads as "merge when green" but degrades to "merge now", so the guard
you think you armed is simply absent. Neither PR turned out broken, which is exactly why
it went unnoticed twice.

**How to apply:** never pass `--auto` on these repos. Poll `gh pr checks <n>` to green
first, then `gh pr merge <n> --rebase --delete-branch`. Also never `--squash` on a branch
carrying the user's commits — a prior `--squash` collapsed three Lego Lab commits.
The user has admin on both repos and could enable auto-merge in settings; that is their
call, not a change to make unasked. Related: [[islamic-orb-project]].
