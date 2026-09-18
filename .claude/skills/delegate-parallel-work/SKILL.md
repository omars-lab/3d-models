---
name: delegate-parallel-work
description: Fan several independent, unblocked tasks out to parallel Opus subagents, each in its own git worktree, then integrate serially by cherry-pick. Use when the backlog holds three or more pending tasks whose files are disjoint — a multi-piece feature, a batch of docs, a set of validators — and the pieces can be built at once without stepping on each other. Not for a single task, for tasks that all edit the same file, or for anything the owner must gate.
---

# Delegate parallel work

The pattern that shipped the coaster border (D-071) end to end with zero
cherry-pick conflicts across four pieces: one isolated worktree and one Opus
subagent per piece, the main session integrating them one at a time. It trades a
little setup for real isolation — subagents never share a checkout, so their
edits cannot collide, and the main session stays the single point that touches
the shared tree, opens the PR, and resolves anything by hand.

Reach for it when the signal is real: several tasks are `pending`, none is
blocked by another, and their file sets are disjoint. The `delegate-nudge` hook
(`.claude/hooks/delegate-nudge.py`) watches the task list and points here when
that is true; it is advisory, not a command. One reviewable piece done directly
is always a fine answer.

## When it does not apply

- **One task, or a chain.** No parallelism to win. Do it directly.
- **Shared files.** Two tasks that edit the same file will conflict no matter how
  they are isolated. Either serialize them or re-split the work along file lines
  first. Grammar or schema edits that every piece imports serialize through the
  main session.
- **Owner-gated steps.** Anything that spends money, publishes, touches shared
  state, or needs Omar's call is not delegated — the subagent stops at the gate
  and hands the decision back.

## The split

Write the ownership table before spawning anything. Each piece names the files it
owns, and no file appears twice. A plan section is the right home for it — see
`.claude/plans/coaster-border-continuation.md` for the worked example (§2b: agents
A/B/C/D with a file-ownership table). If two pieces want the same file, the split
is wrong; fix it before delegating, not after.

Give each subagent:

- its own worktree and branch, off the current `origin/master`;
- the exact files it owns and an explicit "touch nothing else";
- the gates it must leave green (`make validate`, the sibling build, tests);
- the constraints from the global and project rules that apply — stage by name,
  never `git add -A`, work conflicts by hand, no `--auto` / `--force` /
  `--no-verify`.

## Isolated worktrees

One worktree per subagent keeps each on its own copy of the tree:

    git worktree add ../3d-models-<piece> -b feat/<piece> origin/master

Never point two subagents at the same checkout, and never let a subagent work in
the shared primary checkout — another session may be on that branch. Fresh
worktrees in a Node repo need their own install and build before the gates run.

## Integrate serially by cherry-pick

The main session pulls the pieces in one at a time, in dependency order, each as a
single reviewable step:

    git cherry-pick <piece-commit>

Cherry-pick one commit at a time — never a range (`A..B`). Run the gates after
each pick, not once at the end, so a break is localized to the piece that caused
it. If a pick conflicts, open the file, keep both intents, re-run the gates, then
`git add` that file by name and continue — never `-X ours` / `-X theirs` or
`checkout --ours` / `--theirs`, which the guardrail hook denies anyway.

When every piece is integrated and green, commit on the integration branch and
open one PR. The subagents' branches were scaffolding; the PR is the deliverable.

## After it ships

Clean up the worktrees (`git worktree remove`). If the run taught something about
the pattern itself — a split that should have been finer, a gate that caught a
subagent, a conflict that a better ownership table would have avoided — record it
so the next fan-out starts from it, in a plan or a memory as fits.
