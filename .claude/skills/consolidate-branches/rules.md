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
  It was kept on purpose and is the only unmerged work we hold on to.

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
- `*/.claude/worktrees/agent-*` — a subagent's worktree, owned by its session.
- `*/bikar-main` — bikar's push-and-delete worktree; the bare repo has no work tree of its own.
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

For checks 3 and 4, the British and American spellings of "color" count as the same word. The color rename
(D-083, 2026-09-28) changed those files on main after many branches had already forked.

Never use `git cherry` or a matching commit subject as proof. Squash merges rewrite every commit,
so neither one tells you whether the work landed.

**Not proof:** "every line the branch adds is on the default". The inventory reports this as
`lines-on-default` and plans a look, not a delete. It shows that the additions landed, but it says
nothing about lines the branch deleted.

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
- Run the delete commands one at a time: `git branch -D <b>`, then `git push origin --delete <b>`
  as a separate command, and `git worktree remove <path>`. If you chain them, or delete several
  branches in one push, the auto-mode permission check refuses the command.
- If the permission check refuses a delete, list it for Omar. Do not retry it another way.
- In bikar, push and delete from a worktree such as `bikar-main`. The bare repo has no work tree,
  and the pre-push hook needs one.

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
