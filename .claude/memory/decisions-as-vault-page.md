---
name: decisions-as-vault-page
description: "Omar wants open decisions gathered as a docs/ vault page with pictures and tick boxes, opened in Obsidian — not a round of AskUserQuestion; the request-feedback skill does it"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-29T19:50:02.376Z
---

When several calls wait on Omar, or a call needs pictures, write a page in
`docs/working-model/feedback-requests/<date>-<slug>.md` and open it in Obsidian. Use the
`request-feedback` skill (3d-models #420). The first page was 2026-09-29-open-calls.

**Why:** on 2026-09-29 he turned down an AskUserQuestion round and asked instead for "a md in
our docs dir … with all context / screenshots for me to make decision". He then asked for this
to become "the typical way we document and gather feedback on decisions".

**How to apply:**
- Each option gets pros, cons and what it leads to, plus a pick and tick boxes.
- When he says he has answered, read the ticks back into the decisions log.
- The vault is the shared main checkout. Fast-forward it with `git merge --ff-only --autostash origin/master`, but only after checking that its uncommitted memory edits change different lines from upstream. See [[omar-working-preferences]].
