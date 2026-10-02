---
plate: sheets-04
recipe: sheets-04.yaml
stage: waiting
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
minutes: 56
grams: 22
bed_plates: 1
risk: watch
pictures:
  - sheets-04-media/bed-map.png
  - sheets-04-media/gbv-frame-and-pieces.png
  - ../design/coaster/loose-pieces-media/frames.png
---

# sheets-04 — the gBV fit

**In short.** The gBV coaster as a backed frame (a solid slab with pockets, F1), printed once, and
loose pieces for one ring of it at four gaps per face: 0.05, 0.10, 0.15 and 0.20 mm. The small
five-point stars come at 0.15 only, to see whether their tips catch. It answers
[loose-pieces call 4](../design/coaster/loose-pieces-design.md#7-open-calls-for-omar) with the gaps that page proposes. All of it
builds: the file is bikar's `Loose-Fit-Coupon.bkr` (bikar #296) and the plate is
[`sheets-04.yaml`](sheets-04.yaml). One bed, about 56 minutes and 22 g.

## What it is

The [sampler sheets design](../design/coaster/sampler-sheets-design.md#3-the-sheets), sheet 4. Unlike sheets 1 to 3 there is no card:
the frame is the whole coaster, and the pieces sit loose in it.

| Code | What it is |
|---|---|
| FRAME | the frame, once: the gBV coaster at its real size (90 mm, 3 mm straps) on a 2 mm slab, a pocket in every cell |
| GAP 05, GAP 10, GAP 15, GAP 20 | the middle ring (orbit 2): ten six-sided pieces at radius 19.9 mm, at that gap per face |
| STAR 15 | the next ring out (orbit 3): ten small five-point stars at radius 28.3 mm, at 0.15 |

The rings were read off `bikar bands`. The gap is taken off the piece, so one frame fits every set.
Each set is its own plate item and goes in its own bag straight off the plate, labelled with its
code, because the sets look alike. The bed map below says which set is where.

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

The bed as it will print, front edge at the bottom, each set named where it landed. The four hexagon
rings look the same in the hand, so bag them by this map. It is drawn from the sliced plate by
`print_review.py bed`, from the bed map compose writes beside the plate.

![The sheets-04 bed: the frame, four hexagon rings at four gaps and the star ring, each labelled](sheets-04-media/bed-map.png)

gBV as bikar now makes it, at 80 mm with all five rings loose at 0.15 mm: the frame alone on the
left, and the 41 pieces lifted above their pockets on the right. A quick render of the checked
STLs. The odd sliver in it is the drawing, not the mesh: both files pass the mesh check, closed
and with no zero-area triangles. The smallest piece is 2.4 mm across at its narrowest, and still
2.3 mm at the loosest gap, 0.20.

![gBV frame and its loose pieces, from bikar #292](sheets-04-media/gbv-frame-and-pieces.png)

The frame kinds in cross-section, from the loose-pieces design; this plate is F1, the first one.

![The three frames, and flush, proud and recessed pieces in the first](../design/coaster/loose-pieces-media/frames.png)

## Cost and risk

One bed, 56 minutes, about 22 g (local slice of the plate, 2026-10-01, X2D preset and PLA Basic, no
slicer warnings, nothing sent).

**Risk: watch.** The pieces are the smallest things we would have printed, and a small piece that
comes loose can be dragged across the bed. It prints only with failure detection on and the first
layer watched; if that is a no, the pieces stay off the plate (loose-pieces §3.7).

## How it was built

- The file: bikar's `Loose-Fit-Coupon.bkr` (bikar #296) copies the gBV construction unchanged and
  keeps its size and strap, so the gap is read on the pieces the gBV coaster will have. It stands
  on the loose-piece output of bikar #292, whose pocket walls follow the outline exactly: the gap
  measured on every CS-1 piece is 0.150 mm all round.
- Every piece passes the mesh check: the frame is one closed body; each hexagon set is ten bodies,
  8.97 mm across at its narrowest at 0.05 and 8.67 mm at 0.20; the stars are ten bodies, 2.10 mm.
- The plate gives each set a `label:`, and `bambu slice compose` writes the bed map from it.

## Your call

Two things, kept apart: whether to print it, and the printer question that comes with it.

- [ ] **Approve as it stands**
- [ ] **Hold** — say why in the notes

Separately, loose-pieces call 4 asks one yes or no of you before this prints:

- [ ] **Yes: failure detection on and the first layer watched** for this plate (loose-pieces §3.7).
  A no keeps the pieces off the plate.

Notes:

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-01 | proposed — designed as a sampler sheet; waits on the build listed above | the [sampler sheets design](../design/coaster/sampler-sheets-design.md) |
| 2026-10-01 | sliced — the file landed (bikar #296); local slice fits one bed, 56 minutes, 22 g, with a bed map | this page |