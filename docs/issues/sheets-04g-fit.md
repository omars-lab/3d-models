---
date: 2026-10-04
---

# sheets-04g: the kites too tight, the middle piece too loose

**2026-10-04.** Omar printed [sheets-04g](../design/plates/sheets-04g.md), the gBV minimal coaster
at 1.25 times its size with all 41 of its pieces on one bed, every piece at gap 0. His words: "in
our olast print, the small kits were too tight ti fit" and "adn the middle piece was too lose".
He said nothing yet about the hexes, the stars, the outer pieces or the coaster.
The record is [2026-10-04-sheets-04g](../prints/2026-10-04-sheets-04g/index.md).

One number for every piece gave two opposite results, so this write-up asks what is different
about the kites and about the middle piece, and answers by measuring.

## What was measured

Everything below is bikar's own geometry at the exact sheets-04g settings (bikar `6629f24`, size
112.5, strap 3.75, height 4.4, round 1.25, gap 0), rendered with each piece left where its hole
is (the pieces file without `pack zipper`), and the slice that printed. The tool is
[`tools/fit_gap.py`](../../tools/fit_gap.py). It cuts the coaster and the pieces flat at one
height and reads the gap round every piece. The cut is at 2.0 mm, inside the straight wall and
under the top round.

| Group | Pieces | Gap at its points | Gap at its inward corners | Sharpest point | Area | Outline per area |
|---|---|---|---|---|---|---|
| Middle | 1 | 0 | **+0.447 mm** at each of 10 | 72° | 208.9 mm² | 0.353 /mm |
| Kite | 10 | 0 | none (no inward corner) | **36°** | 11.8 mm² | **1.334 /mm** |
| Hex | 10 | 0 | none | 72° | 122.3 mm² | 0.353 /mm |
| Star | 10 | 0 | **+0.447 mm** at each notch | 36° | 26.4 mm² | 1.334 /mm |
| Outer | 10 | 0 | none | 72° | 122.3 mm² | 0.353 /mm |

The piece and its hole are the same size across: the widest span of every piece over its hole's
is 1.00000, so nothing was scaled wrong.

**The slicer.** The X2D preset has `xy_hole_compensation` and `xy_contour_compensation` at 0 and
`elefant_foot_compensation` at 0.15. Read off the slice's own wall paths
(`fit_gap.py walls`), at 2.0 mm every wall sits on the drawn line. On the first layer the gap
opens by about 0.3 mm per face for every group alike: Middle +0.357, Kite +0.259, Hex +0.300,
Star +0.266. At 3.8 mm the top round only opens the top of the hole; it does not shrink the hole's
points. So the slicer does not treat a piece differently from its hole, or one group differently
from another.

## Why the middle piece was loose

bikar cut a piece by moving its hole's outline in by half a strap plus the gap, with sharp corners
everywhere. The minimal coaster is straps only, and a strap's edge is round where the hole turns
inward: a circle of radius half a strap (1.875 mm) round the hole's corner. So the frame's own
wall was round at the middle piece's ten inward corners, and the piece's corner was sharp. A sharp
corner of half-angle φ/2 sits t/sin(φ/2) from the hole's corner, where the round wall sits at t:
1.875/sin 54° − 1.875 = **0.443 mm** of play at every notch, while the piece touched everywhere
else. Ten such notches let the middle piece turn and rattle. The stars have the same notches.

The kernel already knew. A comment in its coaster code said "the strap's own edge is rounded at a
reflex corner of the face", and a step there (`raiseLooseBands`) raised the sliver between the
two outlines in the old frame from the pieces file, so that frame matched its own sharp pieces.
The minimal coaster the pieces actually go into had no such step. Two outlines for one edge, in two
code paths: that was the defect.

## Why the kites were too tight

Nothing in the drawing makes a kite tighter than a hex: the gap is 0 all round both. What a kite
has is the least room for error. At gap 0 there is no play anywhere, so any width the printer
adds to a piece's outline, or takes from a hole's, binds the piece. The kite has 3.8 times as much
outline per area as the middle piece, so the same error along the outline weighs 3.8 times as
much against its size. And a point magnifies an error along the faces: moving both faces of a
point by Δ moves its tip by Δ/sin(α/2), 3.24 Δ at the kite's 36° against 1.70 Δ at 72°.

The stars fit the same reading without proving it. A star has the kite's 36° points and the same
outline per area, but it had the 0.447 mm of play at its notches that the kite never had, room
for the printer's error to go. Omar has not said how the stars fit, so this is a reason to watch
them on the fit plate's coaster, not evidence.

This is the likely reading, not a measured one: the printer's own widening per face was not
measured, and the nozzle also rounds a 36° tip off, by about 0.47 mm in principle, which helps a
point fit rather than hurting it. So the evidence points at the gap per face, not at the tip. A tip
relief stays the next knob to try only if a kite at a positive gap still catches at its point.

## What changes, and why

The old approach was one gap for every piece, and a piece cut with sharp corners. Both go.

1. **One edge, round where the strap is round.** bikar now cuts the hole and the piece along the
   strap's real edge, `strapEdgeInset` in `coaster-loose.ts`: sharp at an outward corner, an arc of
   radius half a strap round the hole's corner at an inward one. The gap is then the gap all round,
   notches included. A bikar test reads every piece of the pieces file against the minimal coaster
   at gap 0 and 0.1; it failed before the change (the middle piece 0.447 mm off its wall at gap
   0) and passes after (within 0.02 mm). `raiseLooseBands` had nothing left to cover and is gone.
2. **A gap per group, not one for all.** Each group already renders on its own (`--piece Kite`),
   so a plate can give each its own `gap`. No new knob was needed: `clearance` already takes any
   value above minus half a strap.
3. **The right gap per shape is an open bet, CAL-LSE-01.** No source settles a loose piece's gap
   in a straps-only frame, and CAL-FIT-01's sliding rung (0.15) was set across the diameter of
   round parts, so it does not carry over: a round peg has no points and the least outline for its
   size of any shape.
4. **The next print measures it.** [sheets-04g-fit](../design/plates/sheets-04g-fit.md) tries
   kites at five gaps and middle pieces at four, in the coaster Omar already printed.

## Why a fit plate and not a reprint

Two ways to try the fix were open: a new iteration of sheets-04g (`plate_approve.py --iterate`)
with new gaps, or a plate of only the two pieces Omar named, at a ladder of gaps.

| | Reprint sheets-04g | Fit plate, kites and middle pieces only |
|---|---|---|
| Time | about 97 minutes, a new coaster and 41 pieces | about 25 minutes and 5.3 g (local slice, 2026-10-04) |
| What it tells | one gap per group, so a miss means another full reprint | five kite gaps and four middle gaps side by side in one print |
| The coaster | printed again, unchanged | the one already printed; the fix changes only the pieces |
| Risk | a second coaster of the same design, waste if the gap is still wrong | none to the coaster; small pieces only |

The fit plate wins on return for the time: it answers the question the reprint would only guess
at, and it reuses the coaster, because the whole gap comes off the piece and the coaster's outline
did not change. The pick for each group then goes into a sheets-04g iteration.

## What the fit plate showed

**2026-10-10.** sheets-04g-fit printed, and Omar tried its pieces by hand, first in the fresh
coaster printed beside them (`Z` on its bottom), then in the older sheets-04g coaster. The record
is [2026-10-10-sheets-04g-fit](../prints/2026-10-10-sheets-04g-fit/index.md).

- **The kites fit at 0.05 mm.** "the biggest size fits well, rest too small/lost". The kites
  carry no mark, so which pile that was is worked out, not read off a piece: a smaller gap makes
  a bigger kite, so the biggest are the 0.05 pile. The 0.10 to 0.25 piles were too small for the
  `Z` coaster.
- **The middle piece wants a gap between 0 and 0.05.** `4GF 4A` (gap 0) went in "but to tight";
  `4GF 4B` (0.05) "is good but comes off a bit to easy". Omar asked: "is there a midway between a
  and b?" So gap 0 no longer rattles since the corner fix above; it is now too tight.
- **The same pieces sit about one rung looser in the older coaster.** There `4GF 4A` "fits but
  easliy removable", `4GF 4B` "is loose", and "all small kites are loose". So the older
  coaster's holes came out about one 0.05 mm step larger than the `Z` coaster's. The coaster's
  source gained two knobs between the two prints, both left at 0, which should not change the
  holes; the two meshes were not compared. This is one pair of coasters, a first reading and not
  a rule, but it agrees with [spl-2](../prints/2026-10-09-spl-2/index.md), where a stud's fit
  moved 0.05 to 0.10 mm from one print to the next.

**What it changes.** The fit plate's case for reusing the old coaster (the table above) assumed
the holes come out the same each time. They did not, by about as much as one step of the ladder.
So the halfway test, a middle piece at 0.025 mm between `4A` and `4B`, prints its own fresh coaster
on the same bed, and its pieces are judged in that coaster. A gap picked in one coaster may still
come out one step loose or tight in the next.
