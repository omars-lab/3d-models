# Backlog — PRs, branches and worktrees

Loop: [`consolidation.md`](../../../.claude/loop-prompts/consolidation.md). Done list:
[`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

This loop's work comes from a fresh stock-take each pass, so most of it never needs writing
down. Write an item here only when a pass has to leave it: a PR waiting on Omar, a branch
another session is still using, a trap that needs a fix in its own PR.

## Open

Last full pass 2026-10-27; state in the
[`branch-state-across-repos`](../../../.claude/memory/branch-state-across-repos.md) memory.
Left by that pass:

1. **The snapshot step should refuse to push a removed picture.** `branch_inventory.py snapshot`
   pushes by default, and on hifth that would put back the two held-text pictures its 2026-10-08
   history rewrite removed. Today only a line in `rules.md` stops it. The fix: before pushing,
   refuse any tip whose history holds a file `origin/<default>` no longer has, and add a
   self-test case for it. Found by the 2026-10-27 pass.
2. **Waiting on Omar: purge hifth's GitHub.** About 130 old-history branches, about 60
   `refs/snapshots/2026-10-04/*` and `2026-10-08/*` refs, and `refs/pull/*` (needs GitHub
   Support) still hold the removed pictures. Found by the 2026-10-27 pass.
