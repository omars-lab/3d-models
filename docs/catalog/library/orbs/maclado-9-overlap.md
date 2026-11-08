---
id: Orbs/Maclado-9-Overlap
aliases:
  - Maclado-9-Overlap
title: Maclado-9-Overlap
family: orbs
status: built
bikar files:
  - patterns/Orbs/Maclado-9-Overlap.bkr
tags:
  - library
  - orbs
---

# Maclado-9-Overlap

From bikar's pattern library: `bikar:patterns/Orbs/Maclado-9-Overlap.bkr`, in the orbs family.

No picture: bikar draws no flat picture of this file at its default knobs. Some orbs, lego pieces and coupons exist only as solids.

## What the file says

```text
Maclado-9-Overlap — the welded woven-overlap orb (M4e, the D-032
follow-on): the 9-spike field grown past tangency so adjacent rims
CROSS, with ribbons woven over/under through the crossings — the
maker's-reference interpenetrating regime, not the tangent join. The
strand network has 420 degree-4 crossings (360 interior lattice + the
60 rim-crossing weld nodes) and 180 free tips; it decomposes into 60
linked ribbon loops with globally consistent alternation. The kernel
judges the overlap ratio against the D-032 instrument and refuses one
whose crossings cannot weld (tangent touch at 1.0 is refused by the
parser; weld nodes fuse below 1.08 and again across a dead band). See
3d-models docs/design/orb/maclado-orb-design.md §5.2 and decisions D-032, D-040.
Render with: bikar render Maclado-9-Overlap.bkr --format stl -o out.stl
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `radius` | 60 | 40..110 |
| `overlap` | 1.2 | 1.15..1.22 |
| `amplitude` | 1.4 | 1.4..1.6 |
| `ribbon_width` (advanced) | 1.2 | 0.8..2 |
| `ribbon_depth` (advanced) | 1.2 | 0.8..2 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
