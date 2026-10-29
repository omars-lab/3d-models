# Plan: merge and clean up branches and worktrees across all 17 repos

## Context

You asked for one focused pass on merging and cleanup: bring every branch's and worktree's work
back to main, lose nothing in either direction, and resolve every conflict by hand. You chose to
cover all 17 repos, which means the skill's 8 plus the 9 NaqshCoffee store repos.

The read-only inventory has already run (2026-10-28). The table below lists what it found.

| Repo | Proven merged, can delete | Unmerged, needs a decision | Other |
|---|---|---|---|
| 3d-models | 0 | 0 | local master is 2 behind, in another session's checkout |
| bikar | 0 | 6 `salvage/*` branches (Apr–Sep) | **skipped by the skill**: its list still says `bikar-main`, which no longer exists |
| qiyas, review-md | 0 | 0 | qiyas: 2 untracked skill folders in the main checkout |
| sacred-patterns | 0 | 6 dependabot PRs (open) | `wip/react-d3-2024` is on the keep list |
| 3d-model-hub | 2 local | 0 | 5 untracked comment threads |
| youtube | 0 | 0 | 6 modified `rung.yaml` files in the main checkout |
| hifth | ~352 (old history) | 2 diverged, both in kept worktrees | snapshots must **not** be pushed; remote deletes cost 5 min each |
| coffee-house-storefront | 15 | `feat/cup-bare-picture` (kept for the record, Oct 14) | 2 worktrees: one live, one holding only `.venv` |
| coffee-house-sites / -mcps / -internal-agent / coffee-house | 6 / 2 / 2 / 3 | 0 | 5 local copies of main are behind |

## The rules every step follows

These come from `.claude/skills/consolidate-branches/rules.md`:

- Snapshot every tip before deleting it.
- Re-run `verify` right before each delete.
- Run one delete per command.
- Never use `-X ours`/`-X theirs`, `-s ours` or `--ours`/`--theirs`.
- Never force-push.
- Never `git add -A`.
- Never touch a dirty checkout, a live one, or a subagent's.
- Unmerged work, or work belonging to another session, is your call. I show it to you before merging it.

## How no meaningful work is lost, in each direction

**Branch to main: nothing gets deleted until its work is proven to be on main.**
- A branch is deleted only when `verify` proves its content is already on main. That means one of these holds:
  - it is an ancestor of main;
  - its files match main;
  - its files match its merged PR;
  - each line it added is on main and each line it removed is gone.
- Matching commit names and `git cherry` don't count as proof.
- Before any delete, the branch's last commit is saved on GitHub as `refs/snapshots/2026-10-28/<branch>`. hifth's are saved locally only (see step 2). Either way, a wrong delete can be undone with one checkout.
- A branch that isn't proven merged is never deleted in this pass. "Drop" is not an option this time: the choices are merge it by hand or keep it with a written reason.

**Main to each local copy: nothing local gets overwritten.**
- Local copies of main only ever fast-forward (`--ff-only`). That can't throw away a local commit: if the local copy has its own commits, git refuses, and I report it as a `look` row instead.
- A checkout with uncommitted files is never reset, restored or fast-forwarded by me. Before any change, I compare each file against main. Files that already match are listed for you; files that differ are offered as a save PR.
- Ignored files a worktree removal would wipe (local settings, private assets) keep that worktree in place. The inventory already flags them, as it does for hifth-native.

## How every conflict is worked by hand

For each unmerged branch you choose to merge:

1. **Back up both sides first.** Snapshot the branch, and snapshot main as `main-before-<branch>`. Both sides are then on GitHub exactly as they were, whatever the merge does.
2. **Merge into a fresh branch off main,** in a reused clean worktree. Never the shared checkout, and never on top of another open PR.
3. **Open each conflicted file and read both sides.** For each conflict block, write down in one line what main meant and what the branch meant. Then write a version that keeps both meanings:
   - If both sides edited the same line, combine them into one line that does both.
   - If one side deleted something the other side changed, keep the change if the code it belongs to still exists on main. If that code is gone, the change goes to you as a question.
   - If the conflict is in a generated block (use-case pins, a code map, a count), run that block's sync command so it is rebuilt from both sides. I don't hand-edit those.
   - If the two sides truly contradict each other (for example, two different values for the same setting), I don't pick. I stop and ask you, with both versions side by side.
4. **Prove both sides survived.** Run `branch_inventory.py survives` on every conflicted file. It checks that every line either side added is in the merged result. Any line it reports missing has to be one I removed on purpose, and each one is named in the PR with the reason.
5. **Run the repo's checks**, then open the PR. The PR body lists each conflict: what each side wanted and how both were kept. Then merge it.
6. **Only then** prove the old branch is dead with `verify`, and delete it as in step 2.

The forbidden shortcuts (`-X ours`/`-X theirs`, `-s ours`, `--ours`/`--theirs`) are already blocked by a hook. I'll also never regenerate a conflicted file to get past a conflict, and never close and reopen a PR to dodge one.

## Steps, in order

### 1. Fix the tool first (3d-models PR)

- Change `DEFAULT_REPOS` in `.claude/skills/consolidate-branches/scripts/branch_inventory.py`:
  - `bikar-main` becomes `bikar`.
  - Add a second root for `~/Workspace/git-naqshcoffee/coffee-house*`, so the store repos are part of every pass.
- Add to `rules.md`:
  - Known trap: the worktree limit (budget 9) refuses `git worktree add`. Reuse a clean `-work` tree, then switch it back afterwards.
  - Regenerable: `.venv` is already there; confirm the storefront's `r18-parts` worktree is the case it covers.
  - Leave-alone: `*/.claude/worktrees/side`, if the store uses it as a standing tree. Check its CLAUDE.md first.
- Run `branch_inventory.py --self-test`, then open the PR and merge it.

### 2. Clear what is proven merged (no merging needed)

For each repo, run the `snapshot` line the inventory prints, then for each branch run `verify`, then delete it.

- **Store repos:**
  - storefront: 14 local branches and 1 remote.
  - sites: 4 local and 2 remote.
  - mcps: 2 remote.
  - coffee-house: 3 remote.
  - internal-agent: 2 local.
- **3d-model-hub:** 2 local.
- **hifth:**
  - Snapshot with `--no-push` only. Pushing these old-history tips would put the removed pictures back on GitHub.
  - Delete the local branches.
  - List the ~352 remote deletes for you to run. Each one triggers hifth's full 5-minute pre-push check, and the rules say that's yours to run or unblock.
- **Local copies of main that are behind:**
  - Fast-forward only where the checkout is clean: coffee-house-clis, -design-kit, and shopify-app-cli (`fetch origin main:main`).
  - Leave the dirty ones alone: 3d-models, coffee-house and internal-agent.
- **The storefront's `r18-parts` worktree:**
  - It's detached at a merged commit and holds only `.venv`, so it can be removed.
  - Check first that no session holds it: no lock file, nothing touched in the last 6 hours.

### 3. Unmerged work: one look per branch, then your call

For each branch I read the diff against main and say in one line what it holds and whether main already has a newer version of the same work. Then one question per repo, with two options:

- **Merge it by hand,** following "How every conflict is worked by hand" above.
- **Keep it on purpose,** with the reason added to the keep list.

There's no delete option for unmerged work.

- **bikar `salvage/*` (6 branches):**
  - `core-license-middleware`, Apr
  - `dsl-contract-ci-gate`, Jun
  - `medallion-weave-parked`, Jun, 36 commits
  - `design-html-notes`, Jul
  - `review-reader-origin-at-runtime`, Aug
  - `minimal-frame-coasters-five-more`, Sep
  - Most fork 100–870 commits back, so merging any of them means real conflicts. Before each merge, snapshot both sides (`main-before-<branch>`).
- **storefront `feat/cup-bare-picture`:** its subject line says "kept for the record". I'd propose adding it to the keep list rather than merging it.
- **sacred-patterns dependabot PRs (6):** these are dependency bumps from a bot, not session work. I'd propose a separate pass to check and merge them. They are not part of this cleanup.
- **hifth `native-shell` and `worktree-agent-a8fa…`:** these live in kept worktrees. The first holds private assets and Xcode files; the second belongs to a subagent. I'll describe what is unmerged in each and leave both to you.

### 4. Uncommitted work in main checkouts: look, don't touch

- The dirty checkouts:
  - qiyas: 2 skill folders
  - 3d-model-hub: 5 comment threads
  - youtube: 6 `rung.yaml` files
  - hifth: memory notes
  - storefront: comment threads and local settings
  - coffee-house: 2 SKILL.md files
  - internal-agent: 3 CLI folders
  - shopify-app-cli: memory
  - bikar: 1 plan
- For each one, check whether another session is active there (recent file times, a running `claude` process).
- If none is, show you the files and suggest saving them in a PR, as I did for 3d-models in #815.
- I won't commit another session's files without your yes.

### 5. Report, per repo

What was kept and why, what was merged (PR numbers), the backup names, what was deleted, and what's left for you. That last part covers: the hifth remote deletes, the dirty checkouts, the 3d-models master fast-forward (its 13 untracked files have to be removed or staged first), and the subagent worktrees.

## Verification

- `branch_inventory.py --self-test` passes after step 1.
- After steps 2 and 3, re-run `inventory --commands`. Every repo should show `planned_deletes 0`, and every remaining `look` row should have a recorded decision.
- Every deleted tip has a `refs/snapshots/2026-10-28/…` ref on origin, or a local-only one for hifth.
- For each merge: `survives` passes on every file that conflicted, the repo's gates pass, and the PR is merged.
