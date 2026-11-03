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
   `-pm` and `-master-ro` (dropping them is Omar's, item 6 below). Fast-forward a clean detached
   one that lags master with `git checkout --detach origin/master`. A subagent worktree whose
   session has closed, whose branch is an ancestor of master and which is clean holds nothing, but
   the rules say leave it, so it is listed for Omar rather than removed.
4. **When a branch does hold unmerged work:** snapshot the branch and master both, start a fresh
   branch off `origin/master`, merge the work in, open each conflicted file and keep both sides
   (never `-X ours`/`theirs`, never `checkout --ours`/`--theirs`), prove nothing was lost with
   `branch_inventory.py survives`, run `make validate`, then a PR. Unmerged work that belongs to
   another session is shown to Omar first.
5. **Record the pass** in [done.md](done.md) with the counts and the snapshot date, and update the
   [`branch-state-across-repos`](../../../.claude/memory/branch-state-across-repos.md) memory.
6. **Then the other repos**, bikar, qiyas, youtube, sacred-patterns, 3d-model-hub and the store
   repos, with the same inventory command and no path argument. They are a later pass.

Left by the 2026-10-27 pass:

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
