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
4. **Waiting on Omar: deploy the public gallery.** Checked 2026-11-02: gh-pages was last deployed
   2026-09-30 (from master 42ef7de), so the split coaster cards CS-16 and CS-17 (#583, #591, added
   2026-10-06) and everything since are not live. `make deploy` changes the public site, so it
   runs on Omar's yes. Found 2026-10-29.
5. **Warn when the gallery falls behind master.** Nothing keeps the gallery current: no hook or
   Make target deploys it, and nothing says it is stale. `status.html` shows the last deploy, but
   only to someone who opens it, and five weeks went by unseen. Add a check to `make validate`
   that compares the gh-pages tip's source commit with master and prints a warning (not a
   failure) when files the gallery ships have changed for more than a week. Deploying itself
   stays a manual step, because it publishes. Found 2026-11-02.
6. **Waiting on Omar: which leftover backup copies to drop.** The duplicate `-pm` and
   `-master-ro` worktrees here, hifth's merged remote branches and review-md's two branches hold
   nothing their main lacks, but each removal is his call. The list is in the
   [`branch-state-across-repos`](../../../.claude/memory/branch-state-across-repos.md) memory.
   Found by the 2026-10-08 pass, still open 2026-11-02.
7. **Waiting on Omar: bikar's pre-push hook runs the full test suite even for a tag on a commit
   main already passed.** An edit to skip it was refused as a way round a check, so whether to
   skip it is his call. Found 2026-09-21, still open 2026-11-02.
