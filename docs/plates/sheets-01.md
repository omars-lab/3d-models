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
  - ../design/coaster/sampler-sheets-media/sheet-1-card.png
  - ../design/coaster/sampler-sheets-media/sheet-1-samples.png
  - ../design/coaster/sampler-sheets-media/sheet-1-mockup.png
needs:
  - "row A TODAY: the old staircase edge cut to a window (bikar main draws only the true edge, and the commit before it has no window)"
---

# sheets-01 — edge and top

**In short.** One card, three 30 mm windows cut from real 90 mm coasters (a CS-1 crossing, a CS-2
star, a gBV star), each in four versions: today's edge, the true edge, the true edge with the full
dome, and a finer grid if the language can set it by then. It answers whether the steps on today's
edges show at all, and which top to keep. It is the first sampler sheet worth printing. Rows B and C
build today: the window cut (bikar #293), the labeled card (`Sampler-Cards.bkr`, piece Sheet1Card)
and the plate ([`sheets-01.yaml`](sheets-01.yaml), assembled by `bambu slice sheet`). Row A does not
yet, so the sheet is not for printing.

## What it is

The layout is in the [sampler sheets design](../design/coaster/sampler-sheets-design.md#3-the-sheets), sheet 1. Rows:

| Code | What it is | Value |
|---|---|---|
| A TODAY | today's edge in 0.4 mm squares, round 1 (the control) | not built yet |
| B TRUE | the edge drawn between grid points, round 1 (the file's default) | `round` 1 |
| C DOME | the same edge, round 1.5 | `round` 1.5 |

Columns: CS-1 crossing (window `30@9.7,1`), CS-2 star (`30@18.5,18.5`), GBV star (`30@0,0`), each
cut from the coaster's own minimal file at 90 mm. The card is 138 × 122 × 1.4 mm with the codes
engraved 0.6 mm deep, one per plate. D FINE, a 0.2 mm grid, is left off the card: no option sets
the grid size, and a labeled empty row would read as a sample that failed. When one lands the card
grows a row.

## Why print it

- **The question:** can you see or feel the difference between A and B? If not, the edge work
  closes.
- **What it lets us decide:** the [smooth-lines calls](../design/coaster/smooth-lines-design.md#6-open-calls-for-omar) 1 and 4.
- **What to read off it:** A against B for the steps; B against C for the top.

## Pictures

What the plate builds today, drawn from the assembled mesh (`bambu slice sheet … --stl`, then
`tools/print_review.py`). On the left are the card's top faces, with its engraved codes. On the
right are the samples' top faces where they stand on the card: row B on top, row C below it with the
narrower flat tops the dome leaves, and the top band empty for row A.

![sheets-01 card: title, column heads CS-1, CS-2, GBV and row codes A TODAY, B TRUE, C DOME engraved](../design/coaster/sampler-sheets-media/sheet-1-card.png)
![sheets-01 samples: six 30 mm windows in rows B and C, row A's band empty](../design/coaster/sampler-sheets-media/sheet-1-samples.png)

The layout mockup the design started from:

![sheets-01 layout mockup](../design/coaster/sampler-sheets-media/sheet-1-mockup.png)

## Cost and risk

No time or filament yet: the plate is assembled and slices clean headless, but the print plan
waits for row A. The card is the safety: every window stands on the card's footprint, not on its
own thin feet.

**Risk: ok.** Flat card, samples fused to it, nothing loose.

## What it waits on

- The staircase for the today's-edge row. The true edges shipped 2026-10-01 (bikar #291), so
  bikar main no longer draws the staircase, and the window cut
  ([sampler sheets §2](../design/coaster/sampler-sheets-design.md#2-cutting-a-window-out-of-a-coaster))
  shipped the same day after it (bikar #293), so the commit that still draws the staircase cannot
  cut a window. Row A needs one of the two brought to the other: the old edge as an option on
  main, or the coaster STLs vendored here before the re-vendor cut to the same 30 mm squares.
- Everything else is built: rows B and C, the card and the plate
  ([§5](../design/coaster/sampler-sheets-design.md#5-from-the-design-to-the-plate)). Built and
  checked 2026-10-01: every window passes the mesh check, the layout check passes (each sample on
  the card, none touching another), and the assembled plate slices clean headless.

## Your call

Nothing to tick yet: without row A the sheet cannot answer its first question. When row A lands
this page moves to `waiting` with the slice, its time and filament, and the boxes below are the ones
you will answer.

- [ ] **Approve as it stands**
- [ ] **Hold** — say why in the notes

Notes:

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-01 | proposed — designed as a sampler sheet; waits on the build listed above | the [sampler sheets design](../design/coaster/sampler-sheets-design.md) |