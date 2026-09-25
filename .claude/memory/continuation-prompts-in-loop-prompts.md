---
name: continuation-prompts-in-loop-prompts
description: "Continuation prompts for a new session are committed under .claude/loop-prompts/, loop-shaped, goal first, linking the plans"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-25T17:25:55.745Z
---

A continuation prompt for a new clean session is a committed file in `.claude/loop-prompts/<slug>.md`,
not text pasted into chat. It opens with a clear goal and says when the goal is met. It links the
plans in `.claude/plans/` that hold the detail. It is written as a `/loop` pass: look, pick by ROI,
ship, record, wait when blocked. It lists the open work in ROI order and names Omar's calls.

**Why:** Omar, 2026-09-25, asking for a continuation prompt: "should be commited to
.claude/loop-prompts/... and it should reference relevant plans", "see if prompt can be loop
focused", "working back in ROI priority order", "the goal should be clear".

**One loop, one job.** The product loop (`coaster-pipeline.md`, #307) never does PR, branch or
worktree consolidation. That is its own loop, `consolidation.md`. Omar, the same day: "pr
consolidation shouldnt be looped for in this ... separate loop prompt".

Later the same day Omar added three more loops: print infrastructure ("churn out prints in
robust, visualizable, easy to configure way"), catalog expansion ("find new patterns to
reconstruct") and video reconstruction ("deconstructing a video, iterating on it"). There are
five in all, listed in `.claude/loop-prompts/README.md`.

**Each loop has its own backlog and done list at `docs/tasks/<loop>/{backlog,done}.md`**
(decided 2026-09-25). They live under `docs/tasks/`, not under `.claude/` and not in a
`docs/loops/` folder; Omar: "there shouldnt be loops under docs", then "it should be
docs/tasks/<loop>/{backlog,done}.md". The prompt says how a pass runs and the backlog says what
comes next. A pass adds what it finds to the matching loop's backlog, and the PR that ships an
item moves it to the done list. Work no loop owns goes in `docs/tasks/parked/backlog.md`.
`docs/backlog.md` stays in place as the print-gated register, because the count gates read it.
`docs/tasks/done.md` is frozen at Snapshot 10 so old task ids still resolve. The video loop
keeps its lists in the youtube repo.

**How to apply:** when the state changes, update the matching file rather than writing a new
one. A new loop gets its own file only when it has a different goal. Related:
[[omar-working-preferences]], [[branch-state-across-repos]].
