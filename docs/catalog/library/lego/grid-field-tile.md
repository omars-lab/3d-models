---
id: Lego/Grid-Field-Tile
aliases:
  - Grid-Field-Tile
title: Grid-Field-Tile
family: lego
status: built
bikar files:
  - patterns/Lego/Grid-Field-Tile.bkr
tags:
  - library
  - lego
---

# Grid-Field-Tile

From bikar's pattern library: `bikar:patterns/Lego/Grid-Field-Tile.bkr`, in the lego family.

![Grid-Field-Tile](../../media/library/lego/Grid-Field-Tile.webp)

The file drawn at its default knobs.

## What the file says

```text
Grid-Field-Tile — the preset that makes the *scored* gate say a number.

Every other preset here inscribes a one-off motif, and a one-off motif has
no repeat vectors, so §5.3's grid fit honestly reports `n/a` rather than a
score of zero. This one tiles a motif on a square lattice of pitch `pitch`,
which gives the gate two vectors to measure and the Lab a knob that moves
the score: at `pitch 8.0` the art repeats exactly on the stud lattice and
the fit is 1.0; drag it to 8.5 and the pattern walks off the studs a little
more with every repeat.

That is the whole point of scoring rather than passing/failing. A piece
whose art does not register on the 8 mm grid is still printable and still
clutches — the anchor gate is the one that can fail — but it cannot be
extended by adding another one beside it without the pattern breaking at
the seam. V8 warns below 0.8 and names the nearest sweet spot.

Two circles, one drawn and one not: `M` carries the diamond that becomes
the relief pocket, `G` exists only so the tiler has a pair of points a
whole `pitch` apart to step by. `M` is deliberately smaller than half the
pitch, so neighbouring pockets stay separated instead of meeting at a
corner — a vertex-touching pocket pair is a T-junction the cell partition
has to resolve, and there is no reason to hand it one on purpose.

Render:
  bikar render patterns/Lego/Grid-Field-Tile.bkr --format stl --check -o GridFieldTile.stl
  bikar render patterns/Lego/Grid-Field-Tile.bkr --format svg -o GridFieldTile.svg

Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
coupon LG-F1). Print the coupon before trusting the fit.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `pitch` | 8.0 | 6.0..12.0 |
| `plates` | 3 | 2..9 |
| `engage` | 3.2 | 1.6..4.0 |
| `relief` | 0.8 | 0.8..2.0 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
