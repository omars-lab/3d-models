---
name: two-sessions-split-by-kind-of-work
description: "Omar 2026-11-03 split the 3d-models sessions by kind of work; plates-and-feedback keeps prints, hub judging, comments and records, the other session takes the rest; the rule lives in the loop README"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e778ebdd-03d8-4cb5-9096-0e141345d0f5
  modified: 2026-11-03T18:29:41.489Z
---

On 2026-11-03 Omar said the plates-and-feedback session should "focus on printing, the hub,
getting comments, iterating on plates" and that all other work moves to another session and
off its list. The rule is written on master in `.claude/loop-prompts/README.md` under
"Which session runs which loop", with the tie-break "does this move a print, a judging page or
a comment?" Yes stays with plates; no goes to the other session.

**Why:** the printing session was carrying 28 open items, 16 of them decisions, catalog and
repo housekeeping, and Omar wanted it undistracted.

**How to apply:** when a task shows up in either session, route it by the README rule, not by
which backlog file it sits in. Pull work from a session by reading its task files at
`~/.claude/tasks/<session-id>/` (the last list it printed can be days stale), recreate the
items on the taking session's list, then message the giving session the ids to delete; an idle
session only reads the message at its next turn. Never edit another session's task files on
disk. See [[omar-working-preferences]] and [[branch-state-across-repos]].
