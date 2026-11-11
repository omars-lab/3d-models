---
name: open-hub-at-owed-questions
description: "Omar 2026-10-29 — \"open the hub / the pieces I need to answer about\" runs judge-page's open_questions.py; a by-hand flow he repeats belongs in a skill"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-29T16:54:58.133Z
---

When Omar asks to open the hub's judging page with comments, or which questions he still owes,
run `python3 .claude/skills/judge-page/scripts/open_questions.py` (lists plates with open rows,
starts the comments server if down, opens the first open row). `--list` only lists; `--link`
prints the link and opens nothing.

**Why:** 2026-10-29 he asked for it ("open the hub plate page with comments on pieces i need to
answer questions abouit"), and while I did it by hand he said "this shoudl be part of our skills"
(#829). A flow he asks for twice belongs in a skill script, not repeated by hand.

**How to apply:** use the script, never rebuild the address by hand; if it misses a case, fix the
script. Related: [[print-feedback-on-hub-page]].

**Every judging link to Omar is the comments one** (`http://127.0.0.1:8768/judge.html#<plate>/<row>`; take it from `open_questions.py <plate> --link`), never :4717. :4717 is the bare hub with no comments. The comments server runs the same live hub and adds comments. On 2026-11-09 Omar asked "why is comment mode not enabled?" after I gave him the :4717 link. The port moved from 8766 to 8768 (the hub's `.page-comments/config.json` is the source; 8766 belongs to social-presence-hub), and the script now reads it from there (2026-11-11).
