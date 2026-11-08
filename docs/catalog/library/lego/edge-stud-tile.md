---
id: Lego/Edge-Stud-Tile
aliases:
  - Edge-Stud-Tile
title: Edge-Stud-Tile
family: lego
status: built
bikar files:
  - patterns/Lego/Edge-Stud-Tile.bkr
tags:
  - library
  - lego
---

# Edge-Stud-Tile

From bikar's pattern library: `bikar:patterns/Lego/Edge-Stud-Tile.bkr`, in the lego family.

![Edge-Stud-Tile](../../media/library/lego/Edge-Stud-Tile.webp)

The file drawn at its default knobs.

## What the file says

```text
Edge-Stud-Tile — the third interface: studs on the perimeter cells only,
with the art cut into the interior they enclose.

`studs none` gives up stacking to carry a pattern and `studs full` gives up
the pattern to stack (V4 will not let one face do both). `studs edge` is the
partial answer available on a footprint big enough to have an interior: the
ring of perimeter studs still takes a piece on top around the border, and
the interior stays flat for relief. It is not free — anything laid across
the middle bridges the art rather than clutching to it — but on a 6 × 6 the
ring is 20 studs and the interior is a 4 × 4 field, which is 32 mm, which
is where a radius-12 rosette fits with room to spare.

Like `Star-Brick`, the art here is a single centred motif, so the scored
grid gate reports `n/a` rather than a number: a one-off rosette has no
repeat vectors to measure against the 8 mm lattice, and §5.3 says
`undefined` for unmeasurable instead of scoring it zero. `Grid-Field-Tile`
is the preset that gives that gate something to chew on.

Render:
  bikar render patterns/Lego/Edge-Stud-Tile.bkr --format stl --check -o EdgeStudTile.stl
  bikar render patterns/Lego/Edge-Stud-Tile.bkr --format svg -o EdgeStudTile.svg

Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
coupon LG-F1). Print the coupon before trusting the fit.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `plates` | 3 | 2..9 |
| `engage` | 3.2 | 1.6..4.0 |
| `relief` | 0.8 | 0.8..2.0 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
