---
date: 2026-09-30
---

# CS-6 scored 0.73 on symmetry because the turn was about the wrong point

Was catalog-expansion backlog item 8, now in its [done list](../tasks/catalog-expansion/done.md).
Fixed by bikar #290 and 3d-models #PR.

## What was suspected

`print_review.py sheet` scored CS-6 (`tA8eSdVx_EQ`, the 5-minute seven-fold star rosette) 0.73
at order 7, where every other coaster scored 1.00. The art sheet seemed to show seven petals of
uneven size. The item guessed at two causes: the video's quick seven-fold was only
approximate, or our rebuild had drifted from it.

## What the evidence showed

Neither. The construction is exactly seven-fold. It builds one regular heptagon
(`polygon poly1 = regular 7 from A to B`), finds its centre `H` from two perpendicular
bisectors, and makes every repeat with `rotate 7 around H`. Nothing in it is measured by eye.
The rendered 80 mm mesh agrees. Its top-face art turned about its own centre of mass scores
0.9998 at order 7. Turned about its bbox centre, it scores 0.72.

Two real defects sat behind the one number.

- **The tool turned about the bbox centre.** For art with a half-turn symmetry, which covers
  every even-order rosette, the bbox centre is the middle. A seven-point star with a point up
  reaches farther up than down, so its bbox centre sits above its middle. At 80 mm the gap is
  about 2 mm, or 10 px on the 400 px tile. That is twice the 5 px slack, which is enough to lose
  a quarter of the match. The petals were always equal. The art sheet's marked centre, which
  was the bbox centre, is what made them look unequal.
- **bikar placed the art off-centre in its frame, for the same reason.** The coaster block
  centred the inscribed art on its bbox centre. The heptagon outline is centred on its own
  middle, so the star sat 1.94 mm below the frame's centre. That left a 5.6 mm margin at the
  top point and 1.2 mm at the bottom flat. This was a real print defect, not only a scoring
  one. It may be part of why the 40 mm minimal-frame piece looked off on minis-03 ("weird empty
  space"). That link has not been checked against the printed piece.

## What changed

- **bikar:** `artCenter` (`packages/core/src/kernel/art-center.ts`) returns the art's rotation
  centre when it has one, and its bbox centre otherwise. The coaster block and the GeoGebra
  importer both use it, so the span the importer measures is the span that gets built. All 34
  coaster files were rendered before and after. 33 came out byte-identical. Only CS-6 changed:
  its art now sits on the frame's centre, and its `unit` divisor went from 2.7886 to 2.6433. At
  the same `size`, the art is therefore 5.5% larger, with the margin now even all round. With
  the art centred, the least-area fitter would now pick a circle rather than an octagon if
  CS-6 had no pin. The pinned heptagon (D-079) is kept, and it is now the tightest frame of all.
- **3d-models:** `print_review.py` turns about the art's centre of mass. Any turn that maps the
  art onto itself leaves that point in place. A new self-test check, a filled seven-point star
  band with a point up, fails with the bbox centre (0.68) and passes with the centre of mass
  (1.00). Across every vendored standard coaster, only CS-6's score moved, from 0.73 to 1.00.

## Not changed

Two other places still centre on a bbox. The pieces mode (`brickReliefPockets`,
`brickBodyOutline`) takes `art.center`, and the border motif (`resolveBorderCell`) takes a
bbox centre. No odd-order art uses either one today. They are left for when one does.
