---
name: subagent-loop-signal
description: A background agent that re-reads the same file dozens of times with zero Write/Edit calls is looping, not working — stop it and re-scope; the P1.5 printer agent did 1,348 calls in 9.5 h (parser.ts read 129×) and wrote nothing because its gate required inverting the whole parser.
metadata:
  type: feedback
  originSessionId: 82a84811-d601-4caf-aeb6-288a0d47b1e9
---

2026-09-17: the Opus agent for P1.5 (naqsh printer, round-trip over every G1 corpus file) ran 9.5 h, 1,348 tool calls, read `packages/core/src/dsl/parser.ts` 129 times by Read plus ~40 `sed -n` ranges, and never called Write/Edit. Its text turns repeated "I have the complete AST, let me verify …" — context compaction erased what it had read, so it re-read. Omar asked "is it going in circles?"; the measure that answered in one command: tool-call histogram + Write/Edit count + `git status` in the worktree (empty).

**Why:** a task whose acceptance gate is "invert a 6k-line parser for every declaration kind" has no partial deliverable, so a compacting agent restarts reconnaissance forever. The cheap check (`jq` over the task output: tool names, most-repeated targets, Write/Edit count) should run whenever an agent has been up for more than an hour with no notification.

**How to apply:** (1) give agents a task with a first partial deliverable (a printer for the subset the importer emits, round-trip on the constructions corpus) and grow the gate after; (2) check long-running agents with the histogram before assuming progress; (3) the session-reflect design (task #23) proposes this as an automatic loop detector — see [[parallel-opus-subagents-in-worktrees]], [[bikar-build-and-test-traps]].
