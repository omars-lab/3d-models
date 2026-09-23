---
name: subagent-transcripts-are-separate-files
description: Subagent transcripts live in ~/.claude/projects/<slug>/<session-uuid>/subagents/agent-*.jsonl, not inline as isSidechain lines; bikar's scripts/transcript.py and any reader that only globs *.jsonl silently drops them (176 of 193 files for 3d-models on 2026-09-17).
metadata:
  type: reference
  originSessionId: 82a84811-d601-4caf-aeb6-288a0d47b1e9
---

Measured by the session-reflection census (3d-models PR #218, `docs/research/session-reflection-census.md`): for this project 17 main session files plus 176 subagent files under `<session-uuid>/subagents/`, 241,226 lines. The `isSidechain: true` inline layout that bikar's `transcript-archaeology` skill and `scripts/transcript.py` assume is no longer how Claude Code writes them, so those tools see none of the delegated work — which is where the one real loop (parser.ts read 129×) lived.

**How to apply:** any transcript miner walks both `*.jsonl` and `*/subagents/agent-*.jsonl`; porting that to bikar's reader is open question §12.3 of the design. See [[subagent-loop-signal]].
