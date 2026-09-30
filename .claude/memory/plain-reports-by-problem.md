---
name: plain-reports-by-problem
description: "Omar's shape for status reports — one section per problem, the problem as the header, plain words, no internal ids or house terms"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-30T18:39:11.780Z
---

Status reports to Omar are split into sections, one per problem, with the problem itself as the
header ("The coaster fill had to be typed by hand"). Each section has two paragraphs: first a
short summary paragraph (what was wrong and where it stands now), then a detail paragraph (what
changed, how it was checked, what is left for them). No internal names in the prose: no review
thread ids, branch names, hook numbers, backlog item numbers, "ROI item", "fast-forward",
"classifier", "chip". A PR number or a name they have to type goes at the end of its section, not
in the sentence that explains.

**Why:** Omar, 2026-09-30, after a report listing merges by PR and thread id: "lots of jargon in
the repro", "how do we split into sections with problesm as headers", "simple to read", "exec
summary paragrpah", "then detial pragraph". The
global rule to kill the jargon (see the wiki rule in the global CLAUDE.md) applies to chat
reports too, not only to vault pages.

**How to apply:** before sending a recap, give each problem its own header written as the
problem, keep each section to two or three short sentences, and move ids and names they must act
on into a short "yours to do" section at the end ([[omar-working-preferences]]). The same layout is written into the youtube repo's retro skill, in the retro-doc.md file next to its SKILL.md, so retro docs read this way too.
