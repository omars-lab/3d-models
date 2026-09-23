---
name: option-evaluation-axes
description: "When presenting/evaluating options, always add three axes beyond pros/cons/implications — the dominating-variant search, short-term challenges, and long-term build-vs-reuse ownership (Omar, 2026-09-21)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-21T16:38:57.018Z
---

When presenting or evaluating options, the existing tenet (every option carries
pros, cons, and downstream implications, rendered as a comparison with a one-line
recommendation) is not enough. Omar, 2026-09-21: "these kinds of questions should be
questions we generally ask when presenting and evaluating options." The three axes to
add, on **every** options review:

1. **Dominating-variant search** — before accepting an option at its worst framing,
   look for a version that keeps its benefit and drops its biggest cost. An option is
   only truly rejected once its dominating variant was searched for and not found.
2. **Short-term challenges** — what breaks or blocks *this quarter*, including spike
   risk on anything "unverified"; name the fragile fallback the spike might land on.
3. **Long-term ownership (build vs. reuse)** — does it move us toward owning the
   capability or toward depending on someone else's, and is that the right direction?
   A strategic axis, not a cost one.

**Why:** cost is the only axis visible at the moment of choosing; robustness, lock-in,
and what-it-verifies are invisible then and decisive later, so the trade is
systematically mis-priced unless these are written down. This is the same reasoning as
CLAUDE.md "robustness over ease". The dominating-variant search is what turned "rebuild
GeoGebra's geometry engine" (huge, rejected) into "self-bootstrap the bikar kernel we
already have" (small, chosen) — [D-080](../../docs/decisions-log.md), the
[cached-coords producer design doc](../../docs/cached-coords-producer-design.md).

**Confirmation (Omar, 2026-09-21):** "b prime sounds good if its a good long term
investment, continue" — the **long-term-ownership axis was the deciding factor**, not
cost. This validates C13: the ownership axis changed a real call (A → B′). When an
option wins on ownership, say so explicitly and get that axis confirmed before building.

**How to apply:** these three axes now live in the 3d-models `design-craft.md` rubric
as criterion **C13** (checked by `review-design`, authored by `write-design`), so any
design doc's alternatives section is scored on them. For quick in-chat AskUserQuestion
option sets, ask the dominating-variant question *before* offering the options, and let
each option's row carry its short-term-challenge and ownership consequence, not just a
cost. The master option-presentation tenet lives in `~/.claude/CLAUDE.md` — these
augment it. Related: [[omar-working-preferences]].
