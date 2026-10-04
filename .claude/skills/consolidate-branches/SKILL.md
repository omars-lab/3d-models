---
name: consolidate-branches
description: Bring every branch, worktree and stash across our repos back to main without losing work in either direction — inventory, prove what is merged by content (squash merges hide it from git cherry), snapshot tips to refs/snapshots/<date>/ before anything destructive, land unmerged work through a fresh branch and PR with conflicts worked by hand, then delete what is proven dead. Use for "consolidate branches", "clean up worktrees", "bring everything back to main", "what's not merged", "delete merged branches", "back up branch refs", or before and after a burst of parallel sessions or subagents. Covers 3d-models, bikar (bare repo + worktrees), qiyas, youtube, sacred-patterns, 3d-model-hub, hifth and review-md. Not for opening a single PR (just do it) or resolving one in-flight conflict on your own branch.
---

# consolidate-branches — everything back to main, nothing lost

Many sessions and subagents leave branches, worktrees and stashes across eight repos. Most of
it has landed through squash merges, so git's ancestry no longer shows it as merged. Some of it has
not landed. And sometimes a local default branch holds commits its remote lacks, which is the other
direction work can be lost in. This skill sorts all of it, keeps what is unmerged, and deletes only
what is **proven** dead.

The rules that sharpen over time live in [`rules.md`](rules.md). They are the keep lists, the
worktrees to leave alone, the live window, what counts as proof, and the known traps. The script
reads that file every time it runs. Read it before a pass, and add a line to it when a pass teaches
you something.

## The flow

0. **Commit your own work first.** A dirty worktree is always `keep`, so whatever this session
   has not committed sits out of the pass, and a branch that only exists locally is one deleted
   folder from gone. On your own branch, run the gates, commit the files you changed by name, and
   push it. It then shows up as a branch with a state, like everyone else's. Another session's
   uncommitted files are not yours to commit: list them in the report.
1. **Inventory (read-only, always run it).**
   `python3 .claude/skills/consolidate-branches/scripts/branch_inventory.py inventory --commands`
   It covers the repos in `DEFAULT_REPOS`, or the paths you pass. You get one table per repo:
   worktrees (dirty, live, kept by rules), local and remote branches with their ahead and behind
   counts, stashes and open PRs. The last lines are a headline per repo. `--json` gives the same
   thing to a program.
2. **Classify.** Each branch gets a state and an action:

   | State | Means | Action |
   |---|---|---|
   | `ancestor`, `no-changes` | Its commits are all on origin's default, or it changed nothing | `delete` |
   | `content-on-default` | Every file it touched matches origin's default (British and American spellings of color folded) | `delete` |
   | `content-in-pr` | Every file it touched matches its merged PR's merge commit | `delete` |
   | `changes-on-default` | Every line it added is on the default, and every line it removed is gone from it (main took the change, then moved on) | `delete` |
   | `lines-on-default` | Every line it added is on the default, but a line it removed is still there | `look` |
   | `ahead-only` | Unmerged commits; the default has not moved past its fork | `look` |
   | `diverged` | Unmerged commits, and the default has moved on | `look`, snapshot first |
   | local default `ancestor` and behind | The local default lags origin | `ff` |
   | local default ahead | Commits origin lacks: work that was never pushed | `look` |

   `keep` overrides all of these. It applies to anything in rules.md's keep list, a branch with an
   open PR, and a branch checked out in a worktree that is dirty, live, main, or protected. A
   worktree is `remove` only when it is clean, past the live window, not protected, its head is
   proven dead, and it holds no ignored files outside rules.md's regenerable list. That last check
   is there because `git worktree remove` deletes ignored files without a word, and a local
   settings file or a folder of private assets is ignored too.
3. **Show the plan and act on the safe part.** Paste the headline and every `look` row into the
   report. You don't need to ask before taking snapshots or running the read-only inventory. Ask
   Omar before you merge unmerged work or anything that belongs to another session. Present it as
   options with their pros, cons and implications.
4. **Snapshot, then delete what is proven dead.**
   - Run the `snapshot` line that `--commands` printed. It writes `refs/snapshots/<date>/<branch>`
     for every tip it is about to delete and pushes those refs to origin.
   - Re-check a branch just before you delete it with `branch_inventory.py verify <repo> <ref>`.
     It exits 0 only if the branch is dead right now.
   - Run each `worktree remove`, `branch -D` and `push origin --delete` on its own. Never chain
     them, and never put two branches in one push. The permission check refuses both.
   - If a delete is refused, list it for Omar. Don't retry it another way.
5. **Bring unmerged work back (only after Omar's yes).**
   - Snapshot both sides before a hard merge: the branch, and the default it is going into, under
     a name that says which merge it guards:
     `branch_inventory.py snapshot <repo> <branch> <default>-before-<branch>=origin/<default>`.
     Either side can then be read back exactly as it was, whatever the merge did.
   - Start a fresh branch off `origin/<default>`, merge or cherry-pick the work in by name, and
     resolve every conflict by hand, keeping both sides.
   - Prove nothing was lost: `branch_inventory.py survives <repo> <file> <merge-base> <ours> <theirs>`
     on each file that conflicted.
   - Run the repo's gates, then open the PR and merge it. Only then delete the old branch, as in
     step 4.
6. **Report per repo:** what was kept and why, what was merged (PR numbers), what was snapshotted
   (the ref names), what was deleted, and what is left for Omar.

## Never

These are the guardrails, and each one has cost work before:

- No `git cherry` or subject match as proof of merge.
- No force-push.
- No `-X ours`/`-X theirs`, `-s ours` or `checkout --ours`/`--theirs`.
- No `git add -A` and no `git restore .`.
- No range cherry-pick (`A..B`).
- Don't touch another session's worktree or the files in it. That includes a dirty main checkout,
  even when its branch is behind, and a subagent's `.claude/worktrees/agent-*`.
- Don't stack a PR on another open PR's branch.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/branch_inventory.py inventory` | Read-only: fetches, classifies every branch, worktree and stash, plans keep, delete, ff or look, and prints the commands the plan implies | Every pass starts here; also "what's not merged" | `python3 .claude/skills/consolidate-branches/scripts/branch_inventory.py inventory --commands` |
| `scripts/branch_inventory.py verify` | Re-proves one ref dead against origin's default and its PR's merge commit; exit 0 means dead | Right before deleting a branch | `python3 .claude/skills/consolidate-branches/scripts/branch_inventory.py verify <repo> <ref>` |
| `scripts/branch_inventory.py snapshot` | Writes `refs/snapshots/<date>/<branch>` (or `<name>=<ref>` for a detached head), refuses to move an existing one, pushes them | Before any delete, and before merging a diverged branch | `python3 .claude/skills/consolidate-branches/scripts/branch_inventory.py snapshot <repo> <ref>…` |
| `scripts/branch_inventory.py survives` | Checks that every non-blank line each side added over the merge base is in the merged file | After a hand-resolved conflict, before committing the merge | `python3 .claude/skills/consolidate-branches/scripts/branch_inventory.py survives <repo> <file> <merge-base> <ours> <theirs>` |
| `scripts/branch_inventory.py --self-test` | Builds a throwaway repo with one branch per state and checks each verdict, the plan rules, the snapshot and the survives check | After any edit to the script or to rules.md | `python3 .claude/skills/consolidate-branches/scripts/branch_inventory.py --self-test` |

The script used to live at `tools/` and was moved here on 2026-10-04. The proofs were extended
then: PR merge commits, folding the British spelling of color, behind counts and the plan column were added.
