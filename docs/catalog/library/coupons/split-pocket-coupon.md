---
id: Coupons/Split-Pocket-Coupon
aliases:
  - Split-Pocket-Coupon
title: Split-Pocket-Coupon
family: coupons
status: printed
bikar files:
  - patterns/Coupons/Split-Pocket-Coupon.bkr
tags:
  - library
  - coupons
---

# Split-Pocket-Coupon

From bikar's pattern library: `bikar:patterns/Coupons/Split-Pocket-Coupon.bkr`, in the coupons family.

![Split-Pocket-Coupon](../../media/library/coupons/Split-Pocket-Coupon.webp)

The file drawn at its default knobs.

## What the file says

```text
Split-Pocket-Coupon — way c: does a piece printed in place in its pocket come out loose?

The other way to trap a loose piece in a split coaster (3d-models
docs/design/coaster/finish-techniques-brainstorm.md §1.4, way c): cut the
piece at the split too, and print each piece half inside its own half, in a
closed pocket. The pocket necks down to the lip outline at the face and
again at the cut; between the necks is a room at the full opening. The
piece half is a spool: a plug through each neck and a band in the room,
with air above and below the band. Nothing is placed by hand: closing the
coaster presses each piece half onto its partner at the cut, with nothing
extra between them.

A pair asks three things of the hand: does the band come free of the necks
when the half is flexed, or did the air close up and fuse it; does the
closed piece move or click in its pocket when the coaster is lifted; and
does the band's underside, printed over air on the plug, come out flat.

Two parts, each printed flat; the piece halves are part of them:
  Lower  the bottom half, studs standing on its cut face, its piece half inside.
  Upper  the top half, sockets in its cut face, its piece half inside.

The plate prints two pairs, at one layer of air (thick 0.6, air 0.2) and two
(thick 0.4, air 0.4); either way each half's band is 2.2 - 2 × thick -
2 × air = 0.6 mm:

  bikar render patterns/Coupons/Split-Pocket-Coupon.bkr --piece Lower \
    --format stl --check --param air=0.2 --param thick=0.6 -o out/pkt-lower-02.stl
  bikar render patterns/Coupons/Split-Pocket-Coupon.bkr --piece Upper \
    --format stl --check --param air=0.2 --param thick=0.6 -o out/pkt-upper-02.stl

`pair` is the pair's letter, cut into both cut faces, the lower half reading
<letter>B and the upper <letter>T, so the halves of one pair find each other
off the bed (3d-models feedback page 2026-10-06, Omar: "every prototype should
have an id"). The plate's bed map says which air each letter is.

LAYOUT: the Split-Trap-Coupon's tile, 25 × 25 × 4.4 cut at 2.2, with the
same hexagon (circumradius 7) and the same two studs on opposite corners.
The neck is 0.8 wide (the strap floor, CAL-CST-01). The gap round the plug
and round the band is 0.25 mm per side (CAL-LSE-01), so the band overlaps
each neck by 0.55. A 0.4 mm neck is under the 0.6 mm deboss floor
(CAL-CST-03); it is printed to see whether the band clears two layers of
air, and a neck that tears is part of that answer.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `air` | 0.2 | 0.2..0.4 |
| `thick` | 0.6 | 0.4..0.6 |
| `gap` | 0.25 | 0..0.5 |
| `pair` | 1 | 1..26 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
