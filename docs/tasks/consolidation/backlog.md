# Backlog — PRs, branches and worktrees

Loop: [`consolidation.md`](../../../.claude/loop-prompts/consolidation.md). Done list:
[`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

This loop's work comes from a fresh stock-take each pass, so most of it never needs writing
down. Write an item here only when a pass has to leave it: a PR waiting on Omar, a branch
another session is still using, a trap that needs a fix in its own PR.

## Open

Last full pass 2026-10-27; state in the
[`branch-state-across-repos`](../../../.claude/memory/branch-state-across-repos.md) memory.

### The plan for 3d-models, written 2026-11-03

Omar asked for a plan that brings the branches and worktrees back to master without losing any
real work, with every conflict worked by hand. The read-only inventory
(`python3 .claude/skills/consolidate-branches/scripts/branch_inventory.py inventory --commands <repo>`)
is the first step of every pass and decides the rest. What it found on 2026-11-03: 16 branches
proven dead by content (12 local, 4 on GitHub), 0 branches with unmerged work, 0 diverged, 0 open
PRs, 0 stashes. So there is no conflict to work by hand in this repo today; when one appears, step
4 is how it is handled.

1. **Save every tip before anything is deleted.** The `snapshot` line the inventory prints writes
   `refs/snapshots/<date>/<branch>` for each tip and pushes them to GitHub, so a delete can always
   be undone.
2. **Re-prove each branch dead right before deleting it** with the script's `verify` command
   (exit 0 means dead), then delete it with one command per branch: `git branch -D` for a local
   one, `git push origin --delete` for a remote one. Never two in one command.
3. **Worktrees.** Keep the standing ones: the main checkout, `-tasks` and `-work` (the
   plates-and-feedback session's), `-hub-ro` and `-hub-rw` (the hub reads and writes there),
   and `-else` (this session's, one reused worktree for every PR it opens). Fast-forward a clean
   detached one that lags master with `git checkout --detach origin/master`. A subagent worktree
   whose session has closed, whose branch is an ancestor of master and which is clean holds
   nothing: snapshot its tip, remove it, delete its branch (Omar, 2026-11-03: "do all the things
   to do", which covered the three leftover copies).
4. **When a branch does hold unmerged work:** snapshot the branch and master both, start a fresh
   branch off `origin/master`, merge the work in, open each conflicted file and keep both sides
   (never `-X ours`/`theirs`, never `checkout --ours`/`--theirs`), prove nothing was lost with
   `branch_inventory.py survives`, run `make validate`, then a PR. Unmerged work that belongs to
   another session is shown to Omar first.
5. **Record the pass** in [done.md](done.md) with the counts and the snapshot date, and update the
   [`branch-state-across-repos`](../../../.claude/memory/branch-state-across-repos.md) memory.
6. **Then the other repos**, bikar, qiyas, youtube, sacred-patterns, 3d-model-hub and the store
   repos, with the same inventory command and no path argument. They are a later pass.

Waiting on a merge that is Omar's:

1. **Delete bikar's three `feat/cup-band-*` branches on GitHub once PR #366 merges.** The
   2026-11-03 inventory found them to be ancestors of #366's branch (`feat/cup-bands-three`), so
   they hold nothing of their own once it lands. Then, from a bikar checkout: snapshot each tip
   under `refs/snapshots/<date>/`, re-prove it dead with the script's `verify`, and delete one
   per command. Waiting on bikar #366, which is Omar's to merge. From the session task board,
   2026-11-03.
