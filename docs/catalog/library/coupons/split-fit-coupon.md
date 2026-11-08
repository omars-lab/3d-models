---
id: Coupons/Split-Fit-Coupon
aliases:
  - Split-Fit-Coupon
title: Split-Fit-Coupon
family: coupons
status: printed
bikar files:
  - patterns/Coupons/Split-Fit-Coupon.bkr
tags:
  - library
  - coupons
---

# Split-Fit-Coupon

From bikar's pattern library: `bikar:patterns/Coupons/Split-Fit-Coupon.bkr`, in the coupons family.

![Split-Fit-Coupon](../../media/library/coupons/Split-Fit-Coupon.webp)

The file drawn at its default knobs.

## What the file says

```text
Split-Fit-Coupon — SPL-1: how tight should a split coaster's studs be?

A split coaster is printed as two halves and glued; studs on the lower
half's cut face drop into sockets in the upper half and line the two up
(3d-models docs/design/pieces/split-with-studs-design.md §4, §9). This
coupon is one small square coaster cut in two at mid-height with a single
stud, so a plate of them ladders the three things the design leaves to a
print:

  gap    socket diameter less stud diameter. Six pairs at -0.10, -0.05, 0,
         +0.05, +0.10, +0.15 (a negative gap is a press fit). The pair that
         drops in by hand and does not rattle is the answer. SPL-1 found
         none: every pair needed a hammer, 0.15 the least (3d-models
         docs/prints/2026-10-09-spl-1), though the slice kept each drawn gap.
         SPL-2 ladders on from 0.15 to 0.40, so the range runs to 0.5.
  stud   the stud's diameter: a row at 1.5 and a row at 3.0, at gap 0 and
         +0.05, beside the 2.0 ladder.
  floor  what the socket leaves under it in the upper half: 0.6, 0.8 and
         1.0, in the lightest filament, to see whether a socket shows
         through the top face. A thicker floor makes a shorter stud.

  bikar render patterns/Coupons/Split-Fit-Coupon.bkr --piece Lower \
    --format stl --check --param gap=0.05 -o out/spl1-lower-05.stl
  bikar render patterns/Coupons/Split-Fit-Coupon.bkr --piece Upper \
    --format stl --check --param gap=0.05 -o out/spl1-upper-05.stl

  pair   which pair this is: its letter is cut into both cut faces, the
         lower half reading <letter>B and the upper <letter>T, so the halves
         of one pair find each other off the bed (3d-models feedback page
         2026-10-06: "minimal letters printed on each AT AB"). The plate's
         bed map says which gap each letter is.

LAYOUT (mm, centred on the origin): a square of side 13 (a circle of radius
9.1924 cut into four, turned 45°), plus a 2 mm strap round it, so 15 × 15.
4.4 tall, cut at 2.2, as the gBV split coaster is. The stud stands where the
stud rule puts it: the roomiest point, but room is measured only a few
millimetres out, so on this square many points tie and the first by position
wins, about 1.5 mm off the centre on each axis. `spacing 100` keeps it to one.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `gap` | 0.05 | -0.1..0.5 |
| `stud` | 2 | 1.5..3 |
| `floor` | 0.6 | 0.6..1 |
| `pair` | 1 | 1..26 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
