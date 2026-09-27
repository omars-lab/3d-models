---
name: only-touch-our-repos
description: Never edit or commit the global ~/.claude/CLAUDE.md or the workspace repo it lives in; sessions here touch only the project repos
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-27T17:11:39.912Z
---

Do not touch the global `~/.claude/CLAUDE.md` (a symlink into `~/Workspace/git/workspace`), and do not commit anything in the workspace repo. Only work in our project repos: 3d-models, bikar, qiyas, 3d-model-hub, hifth and sacred-patterns.

**Why:** On 2026-09-27, Omar said "i dont want to touch ~/Claude.md .. we ahould only toucb our repos" and "remeber thos". I was about to commit the researchers-plus-checker tenet onto the workspace repo's feature branch. I unstaged it, and the task was dropped.

**How to apply:** When a user request says to put a rule "in CLAUDE.md", use the project's own `CLAUDE.md`, a skill or a memory file. Never use the global file. Tenets written into the global file by earlier sessions stay as they are. Don't commit them, and don't revert them unless Omar asks. Related: [[omar-working-preferences]].
