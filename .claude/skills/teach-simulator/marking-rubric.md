# Marking the slits in a bed-face photo

teach-simulator reads this at step 2, every time, so the rubric can sharpen without the skill
changing. The marks go into
[`marked-slits.yaml`](../simulate-first-layer/marked-slits.yaml), one entry per judged piece, and
`scripts/marks.py` checks them.

## What a mark is

A slit is a place where the first layer left the bed showing through the bottom face: a dark dot, a
dash, a thin line or a small triangle you can see into. A mark is how many of them sit in one
**place** on the piece, as a level:

| Level | Means |
|---|---|
| 0 | none seen |
| 1 | a few, scattered |
| 2 | some: a row of them somewhere, or several in more than one strap |
| 3 | many: rows along most of the straps |
| null | the place is not on this piece (no rings, no id), or the photo cannot show it; say which in `why` |

## The four places

- **wall**: along a wall, where the fill meets the wall loops. On stock pieces these are the dots
  at the ends of the zigzag, where it turns.
- **middle**: in the middle of a strap, away from the walls: a seam, a crossing of fill lines, the
  short dashes between many short lines (monotonicline).
- **ring_seam**: where a ring closes, or where the rings from two sides of a strap meet (ring
  layouts only, null on the rest).
- **id**: at the carved id.

The place matters more than the total. The Fitted reading is checked by whether its bare bed lands in
the same places as the marks, not only by its count.

## How to read a photo

1. Open the photo at full size. Read only the part that is sharp and lit. If glare or a steep angle
   hides part of the piece, read the rest and say which part in `photo_quality`.
2. Look at one place at a time across the whole readable face, then give it its level. Do not count
   the same slit twice under two places: a dot at a wall is a wall mark even if a seam ends there.
3. Write `seen` as one plain sentence of what is there and where ("rows of dots along the outer and
   inner walls of the left straps").
4. Write `photo_quality`: how the photo was taken and how much of it could be read.
5. Leave a mark null, with a `why`, rather than guess. A textured plate presses its grain into the
   whole face and hides the slits; those pieces are null, and say so.
6. A photo of the second layer from above is not a bed-face photo. List it under `not_marked`.

## Honesty

- **The marks are Claude's reading, not Omar's.** `read_by` says so, and nothing here changes his
  verdicts in `judged-pairs.yaml`.
- **Say whether the marking was blind.** Marked knowing the verdicts, a mark can lean toward the
  verdict it sits beside; the file's header says so. A blind re-mark shuffles the pieces, hides the
  ids and the verdicts, and marks again; agreement between the two is the check.
- **A photo limits the marks.** A phone shot at an angle, under room light, at about 1000 px across
  a 50 mm piece, shows dots and dashes but not hairlines. Flat, straight-down photos with light from
  one low side (so every slit casts a shadow), or a flatbed scan of the bed face, would show more.
  Those are Omar's to take.
