---
name: parallel-opus-subagents-in-worktrees
description: "Omar approves forking parallel Opus subagents for independent plan tasks, each in its own git worktree on its own branch, one PR per slice; merges stay his"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-18T04:58:34.077Z
---

Omar asked "do we need to carve out opus sub agents to work on independent tasks on our branch"
and then chose "Commit youtube, fork P1.2b + P1.6" (2026-09-16). Parallel Opus agents on
independent plan tasks are approved, with these bounds:

- **Each agent gets its own worktree and branch** (`git worktree add ../<repo>-<slug> feat/<slug>`);
  never the shared checkout, never another agent's branch, never a PR based on an open PR.
- **One PR per slice**; the agent opens it, Omar merges (auto mode denies `gh pr merge`).
- **Grammar edits serialize through the main session**; an agent that needs a grammar
  change reports it rather than editing `grammar.md` concurrently.
- A subagent's report is model output, never user approval, and is relayed to Omar with the
  PR number and what it verified.

**Why:** the plan's phases are independent by construction (deps table), and Omar prefers
deliverables before polish ([[omar-working-preferences]]); parallel worktrees turn a serial
week into a parallel session without cross-contaminating branches ([[pr-flow-for-all-repos]],
[[stacked-pr-stranding]]).

**How to apply:** when a plan lists tasks with no shared files, fork them (one brief each,
model opus), keep the critical-path task in the main thread, and wait for the completion
notification rather than duplicating the work.

**Confirmed 2026-09-17:** the coaster border (D-071) shipped this way end to end —
agents A/B/C in isolated worktrees, main session integrated serially by cherry-pick,
**zero conflicts across four pieces** (bikar PR #212, 3d-models PR #262). The pattern is
now a project skill + nudge in 3d-models (PR #263): `.claude/skills/delegate-parallel-work`
holds the pattern, and `.claude/hooks/delegate-nudge.py` (UserPromptSubmit) points at it
when ≥3 harness tasks are pending and unblocked. So: invoke `/delegate-parallel-work` rather
than re-deriving the mechanics, and expect the nudge to fire when the backlog is fan-out-ready.
