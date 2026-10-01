---
plate: sheets-01
recipe:
stage: planned
approved: false
approved_on:
times_printed: 0
runs: []
answers: "Do the 0.4 mm steps on today's coaster edges show in the hand, and which top (round 1 or the full dome) looks right?"
kind: new
bets: []
unblocks:
  - "smooth-lines call 1: whether the true-edge work is worth finishing"
  - "smooth-lines call 4: the top, round 1 or the full dome"
minutes:
grams:
bed_plates:
risk: ok
pictures:
  - ../design/coaster/sampler-sheets-media/sheet-1-mockup.png
needs:
  - "row A TODAY: the old staircase edge cut to a window (bikar main draws only the true edge, and the commit before it has no window)"
  - "the card with engraved labels, in a coupons file"
  - "the sheet plate in the bambu tool: one object, card plus samples at their cells"
---

# sheets-01 — edge and top

**In short.** One card, three 30 mm windows cut from real 90 mm coasters (a CS-1 crossing, a CS-2
star, a gBV star), each in four versions: today's edge, the true edge, the true edge with the full
dome, and a finer grid if the language can set it by then. It answers whether the steps on today's
edges show at all, and which top to keep. It is the first sampler sheet worth printing. The window
cut is built (bikar #293); the card, its labels and the plate are not.

## What it is

The layout is in the [sampler sheets design](../design/coaster/sampler-sheets-design.md#3-the-sheets), sheet 1. Rows:

| Code | What it is |
|---|---|
| A TODAY | today's edge in 0.4 mm squares, round 1 (the control) |
| B TRUE | the edge drawn between grid points, round 1 |
| C DOME | the same edge, round 1.5 |
| D FINE | a 0.2 mm grid, round 1, only if the grid size can be set by then |

Columns: CS-1, CS-2, GBV. Card about 128 × 156 mm, one per plate.

## Why print it

- **The question:** can you see or feel the difference between A and B? If not, the edge work
  closes.
- **What it lets us decide:** the [smooth-lines calls](../design/coaster/smooth-lines-design.md#6-open-calls-for-omar) 1 and 4.
- **What to read off it:** A against B for the steps; B against C for the top.

## Pictures

A layout mockup, not a render: the samples are stand-ins.

![sheets-01 layout mockup](../design/coaster/sampler-sheets-media/sheet-1-mockup.png)

## Cost and risk

No slice yet, so no time or filament. The card is the safety: every window stands on the card's
footprint, not on its own thin feet.

**Risk: ok.** Flat card, samples fused to it, nothing loose.

## What it waits on

- The staircase for the today's-edge row. The true edges shipped 2026-10-01 (bikar #291), so
  bikar main no longer draws the staircase, and the window cut
  ([sampler sheets §2](../design/coaster/sampler-sheets-design.md#2-cutting-a-window-out-of-a-coaster))
  shipped the same day after it (bikar #293), so the commit that still draws the staircase cannot
  cut a window. Row A needs one of the two brought to the other: the old edge as an option on
  main, or the coaster STLs vendored here before the re-vendor cut to the same 30 mm squares.
- Rows B and C can be cut today: `--window 30@<x>,<y>` on each coaster's own file, at its 90 mm
  scale, with the mesh check passing.
- The card with its engraved labels, and the sheet plate in the bambu tool
  ([§5](../design/coaster/sampler-sheets-design.md#5-from-the-design-to-the-plate)).

## Your call

Nothing to tick yet: the sheet cannot be built, so there is no slice, no time and no picture of
the real thing. When its recipe lands this page moves to `proposed`, then to `waiting` with the
review sheet and the slice, and the boxes below are the ones you will answer.

- [ ] **Approve as it stands**
- [ ] **Hold** — say why in the notes

Notes:

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-01 | proposed — designed as a sampler sheet; waits on the build listed above | the [sampler sheets design](../design/coaster/sampler-sheets-design.md) |
