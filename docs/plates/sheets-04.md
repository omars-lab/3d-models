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
minutes: 55
grams: 15
bed_plates: 1
risk: watch
pictures:
  - sheets-04-media/bed-map.png
  - sheets-04-media/fit-in-coaster.png
  - sheets-04-media/gbv-frame-and-pieces.png
---

# sheets-04 — the gBV fit

**In short.** The gBV minimal coaster itself (the straps only, 4 mm tall, no base), printed once,
and loose pieces for one ring of it at four gaps per face: 0.05, 0.10, 0.15 and 0.20 mm. The small
five-point stars come at 0.15 only, to see whether their tips catch. It answers
[loose-pieces call 4](../design/coaster/loose-pieces-design.md#7-open-calls-for-omar) with the gaps that page proposes, read in
the real coaster rather than a test frame. The pieces come from bikar's `Loose-Fit-Coupon.bkr`
(bikar #296) and the plate is [`sheets-04.yaml`](sheets-04.yaml). One bed, about 55 minutes and 15 g.

**Measured before printing:** the coaster's holes are smaller than the pockets the pieces were cut
for, so today only the 0.20 set clears and the star tips catch. See [the fit](#the-fit-in-todays-coaster).

## What it is

The [sampler sheets design](../design/coaster/sampler-sheets-design.md#3-the-sheets), sheet 4. Unlike sheets 1 to 3 there is no card:
the coaster is the whole test, and the pieces sit loose in its holes.

| Code | What it is |
|---|---|
| COASTER | the gBV minimal coaster, once: 90 mm, 3 mm straps, 4 mm tall, no base |
| GAP 05, GAP 10, GAP 15, GAP 20 | the middle ring (orbit 2): ten six-sided pieces at radius 19.9 mm, at that gap per face |
| STAR 15 | the next ring out (orbit 3): ten small five-point stars at radius 28.3 mm, at 0.15 |

The pieces are 1.2 mm thick, so in the 4 mm coaster they sit below the top and the fit is read on
the walls. The rings were read off `bikar bands`. The gap is taken off the piece, so one coaster
takes every set. Each set is its own plate item and goes in its own bag straight off the plate,
labelled with its code, because the sets look alike. The bed map below says which set is where.

Changed 2026-10-02 at Omar's ask: the first version printed the coupon's frame, a 2 mm round slab
with the straps on it and a pocket in every cell. From above it reads as a plain disk; the real
coaster is the better test, and it costs less (55 minutes and 15 g, against 56 and 22).

## Why print it

- **The question:** at which gap does a piece drop in by hand and stay put, and do the star tips
  catch at the default?
- **The bets it moves:** CAL-FIT-01 (the gap ladder) and CAL-HOL-01 (how much a printed hole
  shrinks) ([bets.md](../../.claude/skills/calibrate/bets.md)).
- **What it lets us decide:** loose-pieces call 4, and the gap the F3 openwork frame reuses
  ([D-090](../working-model/decisions-log.md#d-090--lines-and-loose-pieces-in-two-colors-true-edges-first)).
- **What to read off it:** for each bag, drops in / pressed in / will not go; tips catch or not.

## The fit in today's coaster

The coaster's holes are not cut on the exact outline the pieces were made for. The coupon's own
frame leaves every piece its full gap all round. The minimal coaster's hole comes 0.15 to 0.25 mm
further in at a hexagon's points, and its star holes have blunted tips. So a printed piece meets
the wall at its corners before the gap it was given.

Measured on the two meshes at mid height, 2026-10-02. Room is the distance from a piece corner to
the nearest coaster wall; below zero means the corner is inside the wall.

| Set | Least room | Corners inside the wall |
|---|---|---|
| GAP 05 | −0.20 mm | 48 of 120 |
| GAP 10 | −0.12 mm | 22 of 120 |
| GAP 15 | −0.03 mm | 6 of 120 |
| GAP 20 | +0.05 mm | none |
| STAR 15 | −0.13 mm | 34 of 200, all at the tips |

![A hexagon at 0.15 and a star at 0.15 in the coaster's holes, corners marked by room](sheets-04-media/fit-in-coaster.png)

Printed as it is, the sheet would mostly measure this mismatch, not the gap. The fix is in bikar:
cut the coaster's holes on the same outline as the pockets, so a piece fits the real coaster by
construction. After it, the plate gets re-sliced and re-measured, and every corner should keep its
full gap. That fix is the next piece of work, before this prints.

## Pictures

The bed as it will print, front edge at the bottom, each set named where it landed. The four hexagon
rings look the same in the hand, so bag them by this map. It is drawn from the sliced plate by
`print_review.py bed`, from the bed map compose writes beside the plate.

![The sheets-04 bed: the coaster, four hexagon rings at four gaps and the star ring, each labelled](sheets-04-media/bed-map.png)

The coupon's frame and its 41 loose pieces at 80 mm, all five rings at 0.15 mm, from the first
version of this plate: the frame alone on the left, the pieces lifted above their pockets on the
right. The pieces on this plate are the same; the frame is no longer on it. The odd sliver is the
drawing, not the mesh. The smallest piece is 2.4 mm across at its narrowest, and still 2.3 mm at
the loosest gap, 0.20.

![The coupon frame and its loose pieces, from bikar #292](sheets-04-media/gbv-frame-and-pieces.png)

## Cost and risk

One bed, 55 minutes, about 15 g (local slice of the plate, 2026-10-02, X2D preset and PLA Basic, no
slicer warnings, nothing sent).

**Risk: watch.** The pieces are the smallest things we would have printed, and a small piece that
comes loose can be dragged across the bed. It prints only with failure detection on and the first
layer watched; if that is a no, the pieces stay off the plate (loose-pieces §3.7).

## How it was built

- The coaster: bikar's `gBV_JTt3Kxk-minimal-coaster.bkr` (CS-13), unchanged. It passes the mesh
  check: one closed body, 10.8 cm³.
- The pieces: bikar's `Loose-Fit-Coupon.bkr` (bikar #296) copies the gBV construction unchanged and
  keeps its size and strap, so the gap is read on the pieces the gBV coaster will have. It stands
  on the loose-piece output of bikar #292, whose pocket walls follow the outline exactly: the gap
  measured on every CS-1 piece is 0.150 mm all round.
- Every piece passes the mesh check: each hexagon set is ten bodies, 8.97 mm across at its
  narrowest at 0.05 and 8.67 mm at 0.20; the stars are ten bodies, 2.10 mm.
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
| 2026-10-02 | sliced — reworked at Omar's ask, the minimal coaster in place of the frame; 55 minutes, 15 g; the holes measured smaller than the pockets, only GAP 20 clears | this page |