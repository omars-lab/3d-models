---
name: print-pieces-not-whole-shapes
description: "Omar 2026-10-12 — test a print question on a piece of the shape (one repeat of the coaster, several settings per bed), not a whole coaster per round; but not bare-minimum tiny coupons either"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-12T19:09:18.067Z
---

When a print experiment asks one question (slits on the bottom, a fit, a join), print the smallest
part of the shape that still holds the thing being tested at real size: e.g. one tenth of a
ten-fold coaster with its straps and rim, several settings side by side on one bed, a stock control
beside them. Not a whole coaster per round, and not a tiny square coupon that lacks the feature.

**Why:** the bed-face slits took four whole-coaster rounds (bedface-1 to 3) at one or two settings
each. Omar: "is there a way to make a cropped version of different experiments to compare … doesn't
have to be whole coaster", then "I don't want bare minimum kind of tiny experiments but … just being
generally more efficient".

**How to apply:** before planning an experiment plate, say why a piece answers the question as well
as the whole (the transfer sentence: same line width, speed, plate, neighbors), batch per-piece
settings on one bed, give whole-bed settings (nozzle height, temperature, flow, plate) one print
each, and compare the same spot with `tools/print_review.py compare`. Related: [[look-before-you-print]],
[[slicer-plan-is-not-the-print]], [[try-joins-in-print]].
