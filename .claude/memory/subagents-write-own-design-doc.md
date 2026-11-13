---
name: subagents-write-own-design-doc
description: "Omar 2026-11-13 — every subagent that builds or proposes something writes its design in its own design .md, shipped in its PR"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fe5f7eab-501b-48b0-ac7f-872e4bdaa414
  modified: 2026-11-13T15:02:52.940Z
---

Every subagent that builds or proposes something writes up its own design in a design .md of its own, in the repo the work lands in, in the same PR. In bikar that is `docs/features/<name>.md`. In 3d-models it is `docs/design/<area>/<name>-design.md`, written to `design-craft.md`. A research-only agent writes the proposed design as its own file, apart from its research notes. Put this in the agent's brief from the start, not as a message sent afterwards.

**Why:** Omar, 2026-11-13: "ensure sub agents are documenting their designs in their own design.mds". He asked after three background agents were briefed with no design doc: the print-pages fallback, the local link check and the sidebar research. Each agent's design was going to live only in its PR body and its report.

**How to apply:** each Agent prompt names the doc's path and its shape (premise and problem first, what it verifies, what it misses). Related: [[parallel-opus-subagents-in-worktrees]].
