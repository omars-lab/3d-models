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
3. **Waiting on Omar: bikar's pattern upload to Supabase fails.** The "Sync patterns to Supabase"
   run on bikar main last worked 2026-10-10. Every run since 2026-10-22, 13 of them, fails the
   same way: all 187 patterns compile, then the upload stops within a quarter second with
   `fetch failed`. Nothing in the sync script, the workflow or the packages changed between the
   last good run and the first bad one, so the cause is the Supabase project or the
   `SUPABASE_URL` secret. Twelve quiet days fits a free project paused for inactivity. The bikar
   studio's pattern list is read from that table, so nothing merged since 2026-10-10, the 0.01 mm
   dovetail gap included, reaches it. Unpausing the project or fixing the secret is Omar's;
   after that, re-run the latest failed run. Found 2026-10-29.
4. **Remove the merged hub worktree `3d-model-hub-owed`.** Its branch (waiting-on-you) merged as
   3d-model-hub #21; delete the worktree and the local branch. Found 2026-10-29.
5. **Check the public gallery is current.** Compare the gh-pages deploy date with the newest
   coaster cards (CS-16 and CS-17, added 2026-10-06), and run `make deploy` if the site is behind.
   Found 2026-10-29.
