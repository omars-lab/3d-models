# consolidate-branches — the rules

`scripts/branch_inventory.py` reads this file every time it runs. Add a line here when a pass finds
a new case, and the next pass will follow it. The script only reads bullets under the four headings
below that have backticked fields. Everything else in the file is for the person running the pass.

## Keep: never delete

Format: `` - `<repo or *>` `<branch>` — why ``. The repo is the folder name, as in the inventory
header. `*` matches every repo.

- `*` `gh-pages` — the deployed site, with its own history on purpose.
  It is never merged into the default branch and never deleted.
- `sacred-patterns` `wip/react-d3-2024` — prior art the d3 work cites.
  It was kept on purpose.
- `bikar` `feat/strapwork-outer-edge-closure` — the June medallion weave work (36 commits), parked
  with a handoff plan on the branch. Omar chose to keep it parked (2026-10-28); picking it up means
  a large hand merge.
- `bikar` `archive/core-license-middleware` — the April license client for bikar-core 0.2.0,
  archived on purpose.
- `bikar` `archive/minimal-frame-coasters-rejected` — six minimal-frame coasters Omar turned down
  (Sept 25); main kept rDux's only.
- `coffee-house-storefront` `feat/cup-bare-picture` — an early cup picture kept for the record;
  main has the fuller version.

## Never merge

The same format. The inventory marks these branches `never-merge`, so nobody folds them back in by
mistake.

- `bikar` `fix/weave-amplitude-guard-by-depth-suffix` — it improves a rule main withdrew (D-042).
  If it shows up again, it must not merge.

## Leave alone: worktrees

Format: `` - `<path glob>` — why ``. The glob is matched against the worktree's full path.

- `*/3d-models-pm` — a standing read-only checkout another loop reads.
- `*/3d-models-master-ro` — a standing read-only checkout another loop reads.
- `*/3d-models-hub-ro` — a standing read-only checkout another loop reads.
- `*/3d-models-hub-rw` — the checkout the hub's judging page writes Omar's answers into
  (`HUB_RW_CHECKOUT` in 3d-model-hub's Makefile). It is clean and detached at an old master
  most of the time, so the plan called it dead on 2026-10-23; removing it would break the page.
- `*/.claude/worktrees/agent-*` — a subagent's worktree, owned by its session.
- `*/bikar` — bikar's own checkout on `main`, the default `BIKAR_DIR` the gates read. Since
  2026-10-29 it is an ordinary checkout, no longer a bare repo with `bikar-main` beside it.
- `*-work` — a loop's standing working tree, reused for each next PR.
  The global rule is one working worktree per repo per session, reused, so a clean detached
  `-work` tree is waiting for its loop's next branch, not abandoned.

A local branch named `worktree-agent-<id>` belongs to the worktree `.claude/worktrees/agent-<id>`
and is kept while that worktree is kept. A remote branch whose local twin is checked out in a
kept worktree is kept too: that session may push to it again.

## Regenerable: ignored paths a worktree remove may delete

Format: `` - `<glob>` — why ``. The glob is matched against each part of an ignored path.
`git worktree remove` deletes ignored files along with the folder, and it doesn't warn. So a clean
worktree that holds any ignored path that doesn't match a glob here is kept, and the inventory
names those paths. Examples are a local settings file, private assets, and screenshots. Move or
copy them out first, or add the glob here once you know a build brings them back.

- `node_modules` — `npm install` brings it back.
- `dist` — the build writes it.
- `dist-*` — the build writes it.
- `build` — the build writes it.
- `test-results` — the test run writes it.
- `playwright-report` — the test run writes it.
- `*.xcresult` — the Xcode test run writes it.
- `.DS_Store` — Finder writes it.
- `__pycache__` — Python writes it.
- `.venv` — the setup step creates it.

## Live window

Live window: 6 hours

If a clean worktree's index or HEAD changed within this window, it counts as live. Its session may
still be using it, so the plan leaves it and its branch alone. A dirty worktree is always left
alone, whatever its age.

## What counts as proof

A branch is **dead**, meaning safe to delete after a snapshot, only when one of these holds:

1. It is an ancestor of the origin default branch.
2. It changed no files since it forked from the default.
3. Every file it touched has the same content on the origin default.
4. Every file it touched has the same content in the merge commit of its merged PR.
5. In every file it touched, each line it added since the fork is on the origin default, and
   each line it removed is not. This is the case where main took the change and then kept
   editing those files, so neither 3 nor 4 can match: review-md's two fix branches came back as
   looks in two passes running, and were proven by hand each time (2026-10-04).

For checks 3, 4 and 5, the British and American spellings of "color" count as the same word. The color rename
(D-083, 2026-09-28) changed those files on main after many branches had already forked.

Never use `git cherry` or a matching commit subject as proof. Squash merges rewrite every commit,
so neither one tells you whether the work landed.

**Not proof:** "every line the branch adds is on the default" while a line it removed is still
there. The inventory reports this as `lines-on-default` and plans a look, not a delete. Main may
have kept the old line on purpose, or the line may only repeat elsewhere in the file (a closing
brace), so someone has to read it.

## Before anything destructive

- Snapshot the tip first with `branch_inventory.py snapshot`, which writes
  `refs/snapshots/<date>/<branch>` and pushes it to origin. Do this for every tip you are about to
  delete, not only for the complicated ones.
- In bikar, a snapshot push runs the full pre-push suite (about 5 minutes). Only a push that
  deletes refs and nothing else skips it. Run that push in the background.
- In hifth, every push runs the full pre-push checks (about 5 minutes), deletions included, so
  each `push origin --delete` costs one full run. A deletion skip like bikar's was refused by the
  permission check as a CI bypass (2026-10-04), so hifth's remote deletes are Omar's to run or to
  unblock. If the checks fail on typecheck with `Cannot find module 'preact'`, the main
  checkout's `node_modules` is stale: `pnpm install --frozen-lockfile` there, not `--no-verify`.
  If only the "pitch build's Study Quran commentary" tests fail (34 on 2026-10-29), the private
  pitch data is older than main's pitch tools: it is gitignored, so a pull never rebuilds it.
  Copy `apps/web/public/assets/private/study-quran` aside, then rebuild it with
  `node packages/etl/tools/pitch/extract.mjs` and re-run `make pitch-e2e`. Never print its
  output: it is held text.
- Run the delete commands one at a time: `git branch -D <b>`, then `git push origin --delete <b>`
  as a separate command, and `git worktree remove <path>`. If you chain them, or delete several
  branches in one push, the auto-mode permission check refuses the command.
- If the permission check refuses a delete, list it for Omar. Do not retry it another way.
- In bikar, push and delete from a work tree: `~/Workspace/git/bikar` itself since it stopped being
  a bare repo (2026-10-29), or a worktree of it. The pre-push hook needs a work tree. `snapshot` does this itself: given a bare repo, it pushes from
  the repo's first worktree (it used to push from the bare repo and fail with "this operation must
  be run in a work tree", 2026-10-05).

## Bringing unmerged work back

- Before a `diverged` branch is merged, snapshot the default too, as
  `<default>-before-<branch>=origin/<default>`, so both sides as they stood are on origin (Omar,
  2026-10-04: "backup main and branch for hard to merge branches").
- Start a fresh branch off `origin/<default>`, open a PR, and merge it. Never force-push. Never
  base a PR on another open PR's branch.
- Resolve every conflict by hand and keep both sides. Never use `-X ours`, `-X theirs`,
  `-s ours`, or `checkout --ours`/`--theirs`.
- If the conflict sits inside a managed block, such as a code map, a run catalog, or use-case
  pins, run that block's sync target. It rewrites the block from both sides.
- Prove that nothing was lost by running `branch_inventory.py survives <repo> <merged-file>
  <merge-base> <ours> <theirs>`, which checks every non-blank line each side added is in the
  merged file. The only misses allowed are lines you resolved by hand on purpose (a list line
  that moved, a regenerated count); name each one in the PR. Then re-run the repo's gates.
- Unmerged work that belongs to another session, or that has no PR yet, is Omar's call. Show him
  the classification and wait for his answer.

## Known traps

- In zsh, `$files` does not split on newlines. A dead-branch loop then passes all the files as one
  pathspec, and it reports every branch as merged. The script avoids this by passing argument
  lists, never strings.
- Read `origin/<default>`, not the local default ref. Local `master` in 3d-models is checked out in
  `-pm` and lags behind origin.
- youtube's remote is the Mac Studio bare repo, `studio:git/youtube.git`, so it has no GitHub PRs.
  Its branches have to be proven dead by content.
- A local branch and its `origin/` twin at the same tip map to one snapshot name. Pushing both
  refspecs fails with "receives from more than one src", so `snapshot` writes and pushes the name
  once (review-md, 2026-10-04).
- A generated line can keep a merged branch at `diverged`. In 3d-models, the "Waiting on a build"
  queue line in `docs/design/plates/README.md` is rebuilt by every plate PR. So a plate branch's
  copy of that line matches neither master nor its PR's merge commit, even when every other file
  it touched landed. Prove the rest by hand: compare each file with the PR's merge commit, and
  check that master's current queue line still names the plate. Then snapshot the branch. `pkt-2`
  (PR #657) was proven this way on 2026-10-24. It stays checked out in `3d-models-work`, so it is
  kept and not deleted.
- A rewritten history makes every older branch look `diverged`. hifth's main was rewritten on
  2026-10-08 (`git filter-repo --strip-blobs-with-ids`) to remove two pictures of held text, so a
  branch left on the old history shows about +500–900 / −1432 and still carries those pictures.
  Prove such a branch dead by hand: compare its tree with the rewritten twin of the same merge on
  `origin/<default>` (find it by commit subject). The only differences should be the removed
  files. Then snapshot it with `--no-push` only. **Never run the printed `snapshot` line on these
  tips:** pushing them puts the removed pictures back on GitHub. The old-history branches and the
  `refs/snapshots/2026-10-04/*` and `2026-10-08/*` refs already on hifth's GitHub carry them too,
  and purging those is Omar's (2026-10-27 pass).
- A plain `git status` rewrites a worktree's index when a file's stat is stale, which made every
  worktree the inventory read look live for the next 6 hours (2026-10-28: the store's `r18-parts`,
  last used Oct 15, came back "live"). The inventory now reads the age first and runs status with
  `--no-optional-locks`; do the same in any hand check of a worktree's age.
- A hook refuses `git worktree add` past 9 worktrees. Reuse a clean `-work` tree for the merge
  branch (`git switch -c <branch> origin/<default>`) instead of adding one (2026-10-28).
- The store repos live under `~/Workspace/git-naqshcoffee/`, not `~/Workspace/git/`; the inventory
  reads every `coffee-house*` folder there as well (2026-10-28).
- The storefront's pre-push check runs `make check-repo`, which needs Docker running. With Docker
  down, a snapshot push fails; `open -a Docker`, wait for `docker info`, and push again
  (2026-10-28).
- A merged branch can be the only place an older branch's commits live. When a session merges a
  `salvage/*` branch in (rather than squashing it) and then deletes the salvage branch, the old
  commits survive only inside the merge branch, because the PR squash put none of them on main.
  Snapshot the merge branch before deleting it; that snapshot keeps the whole history. Find which
  ref holds a commit with `git for-each-ref --contains <sha>` (bikar's `dsl-contract-gate` and
  `review-reader-runtime-origin`, 2026-10-29).
- Untracked files in a main checkout are not always work to save. Before opening a save PR,
  check whether each one is already committed somewhere else. internal-agent's `places-cli`,
  `quip-cli` and `supabase-cli` matched `coffee-house-clis`'s committed copies byte for byte
  (`diff -rq`). qiyas's two skill folders were symlinks into sacred-patterns' committed skills.
  Committing a second copy creates a fork nothing keeps in sync, so leave them and list them for
  Omar (2026-10-29).
- To save another session's uncommitted files in a shared main checkout without moving them:
  `git switch -c <save-branch>` in the checkout, stage the files by name, commit, push, PR, merge.
  Then `git fetch origin <default>:<default>`, then `git switch <default>`. The files match the
  merge, so nothing changes on disk (youtube, the hub, the storefront, hifth, coffee-house,
  shopify-app-cli, 2026-10-29).
- A snapshot push can fail on a flaky push-check test after the local ref is already written.
  Re-run the failed check on its own; if it passes on the same commit, push only the ref
  (`git push origin refs/snapshots/<date>/<branch>`). Don't re-run `snapshot`, which refuses to
  move an existing ref (the storefront's `StoreMark.test.tsx`, 2026-10-29).
