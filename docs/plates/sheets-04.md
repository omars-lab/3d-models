---
plate: sheets-04
recipe:
stage: planned
approved: false
approved_on:
times_printed: 0
runs: []
answers: "Which gap per face lets a loose gBV piece drop into its pocket and stay, and do the small five-point stars catch at 0.15?"
kind: new
bets:
  - CAL-FIT-01
  - CAL-HOL-01
unblocks:
  - "loose-pieces call 4: the gap a loose piece gets per face"
  - "the F3 openwork frame (D-090), which follows F1 and reuses the gap this plate settles"
minutes:
grams:
bed_plates:
risk: watch
pictures:
  - sheets-04-media/gbv-frame-and-pieces.png
  - ../design/coaster/loose-pieces-media/frames.png
needs:
  - "the sheet's file in bikar: the gBV frame plus one ring of pieces at each of the four gaps and the small stars at 0.15, as a coupon (not a catalog coaster, so it needs no style name)"
  - "the sheet plate in the bambu tool: the frame and each gap set as separate items"
  - "your yes on failure detection on and the first layer watched (loose-pieces §3.7)"
---

# sheets-04 — the gBV fit

**In short.** The gBV coaster as a backed frame (a solid slab with pockets, F1), printed once, and
loose pieces for one ring of it at four gaps per face: 0.05, 0.10, 0.15 and 0.20 mm. The small
five-point stars come at 0.15 only, to see whether their tips catch. It answers
[loose-pieces call 4](../design/coaster/loose-pieces-design.md#7-open-calls-for-omar) with the gaps that page proposes. The frame and
the pieces can be made now (bikar #292, 2026-10-01); the sheet itself is not put together yet.

## What it is

The [sampler sheets design](../design/coaster/sampler-sheets-design.md#3-the-sheets), sheet 4. Unlike sheets 1 to 3 there is no card:
the frame is the whole coaster, and the pieces sit loose in it.

| Code | What it is |
|---|---|
| GAP 05, GAP 10, GAP 15, GAP 20 | one ring of pieces at that gap per face; which ring is read off `bikar bands` when built |
| STAR 15 | the small five-point stars at 0.15 |

Each gap set is its own plate item and goes in its own bag straight off the plate, labelled with
its code, because the sets look alike.

## Why print it

- **The question:** at which gap does a piece drop in by hand and stay when the coaster is turned
  over, and do the star tips catch at the default?
- **The bets it moves:** CAL-FIT-01 (the gap ladder) and CAL-HOL-01 (how much a printed hole
  shrinks) ([bets.md](../../.claude/skills/calibrate/bets.md)).
- **What it lets us decide:** loose-pieces call 4, and the gap the F3 openwork frame reuses
  ([D-090](../working-model/decisions-log.md#d-090--lines-and-loose-pieces-in-two-colors-true-edges-first)).
- **What to read off it:** for each bag, drops in / pressed in / will not go; stays / falls out
  upside down; tips catch or not.

## Pictures

gBV as bikar now makes it, at 80 mm with all five rings loose at 0.15 mm: the frame alone on the
left, and the 41 pieces lifted above their pockets on the right. A quick render of the checked
STLs. The odd sliver in it is the drawing, not the mesh: both files pass the mesh check, closed
and with no zero-area triangles. The smallest piece is 2.4 mm across at its narrowest, and still
2.3 mm at the loosest gap, 0.20.

![gBV frame and its loose pieces, from bikar #292](sheets-04-media/gbv-frame-and-pieces.png)

The frame kinds in cross-section, from the loose-pieces design; this plate is F1, the first one.

![The three frames, and flush, proud and recessed pieces in the first](../design/coaster/loose-pieces-media/frames.png)

## Cost and risk

No slice yet.

**Risk: watch.** The pieces are the smallest things we would have printed, and a small piece that
comes loose can be dragged across the bed. It prints only with failure detection on and the first
layer watched; if that is a no, the pieces stay off the plate (loose-pieces §3.7).

## What it waits on

- The sheet's file: the gBV frame, one ring of pieces at each gap, and the small stars at 0.15.
  The loose-piece output it is made from shipped 2026-10-01 (bikar #292): the pocket walls follow
  the outline exactly, so the gap measured on every CS-1 piece is 0.150 mm all round (the old
  staircase wall touched the piece on all 24).
- The sheet plate in the bambu tool.
- Your yes on the printer question in loose-pieces call 4.

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