---
date: 2026-10-14
produced-by: Claude Opus 5.5, a subagent writing the no-slits design. Five scratch slices of the bedface-4 piece (one 50 mm window of the gBV coaster), made with the installed Bambu Studio CLI through `bambu slice compose`, and drawn with `tools/print_review.py paths`. Nothing was printed for this file, and no web source was read.
feeds:
  - docs/design/printing/no-slits-design.md
---

# Wall-only straps: what the slicer plans on the first layer

Kept as the record the no-slits design's slice numbers come from. The slices and full-size
pictures were made in the session scratchpad and are not kept. The commands below make them again.
The two shrunk pictures the design shows are in `docs/design/printing/no-slits-media/`.

## What was sliced

One scratch recipe, the same piece as bedface-4 and bedface-5: `bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr`, params `{ size: 112.5, strap: 3.75, height: 4.4, round: 1.25 }`, `window: 50@13,30`, `no_id: "scratch slice, not printed"`, on `bed: x2d`, profile `Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D`, filament `Bambu PLA Basic @BBL X2D 0.4 nozzle`. A second recipe was the same with `strap: 3.70`.

Every variant is a process file with `"type": "process"`, `"from": "User"` and `"inherits": "0.20mm Standard @BBL X2D"`, passed with `-s`. That sets the keys for the whole plate, not per piece: compose takes none of these keys per piece today.

| Variant | Keys set | Strap |
|---|---|---|
| A, stock | none (no `-s`) | 3.75 |
| B, 4 classic walls | `wall_loops` "4" | 3.75 |
| B′, 4 classic walls, narrower strap | `wall_loops` "4" | 3.70 |
| C, 4 classic walls, no elephant-foot shrink | `wall_loops` "4", `elefant_foot_compensation` "0" | 3.75 |
| D, 5 Arachne walls | `wall_generator` "arachne", `wall_loops` "5" | 3.75 |

Every slice printed `preset check: PASS` and `slicer warnings: none`. `wall_loops` and `wall_generator` were read back from each slice's `Metadata/project_settings.config`.

## Commands

Slice: `bambu slice compose <recipe.yaml> -s "Bambu Lab X2D 0.4 nozzle;<variant.json>" -d <dir> -o <name>.3mf --no-record --plate-type hot_plate` (stock leaves out `-s`).

Draw and measure: `python3 tools/print_review.py paths <out.png> <slice.3mf> 0.2 138.2,128,52 --below --check --px 1560`, 30 px a millimeter. The center is the middle of the first layer's printed moves, read from the G-code (x 113.5 to 162.9, y 103.4 to 152.6).

## First layer, the whole piece

| Variant | Slits | Bare (sq mm) | Printed (sq mm) | Bare share | Largest pocket (sq mm) |
|---|---|---|---|---|---|
| A, stock | 355 | 9.511 | 1077.9 | 0.87% | 0.453 |
| B, 4 classic walls | 182 | 10.173 | 1077.2 | 0.94% | 0.684 |
| B′, 4 classic walls, strap 3.70 | 184 | 9.091 | 1067.1 | 0.84% | 0.669 |
| C, 4 classic walls, foot 0 | 463 | 10.110 | 1155.6 | 0.87% | 0.556 |
| D, 5 Arachne walls | 178 | 7.033 | 1080.3 | 0.65% | 0.340 |

Every row fails the bed-face check's bar (under 0.6% bare and no pocket of 0.2 sq mm or more). Stock's 355 sits inside the 350 to 374 the bedface-5 page reports for its stock pieces, a sign the window and the drawing match that page's.

## The first layer's line widths, read from the stock G-code

The first layer's outer wall is laid at `LINE_WIDTH: 0.5`, and no other width is written before the inner walls, so every wall on that layer is 0.5 mm. Gap fill is laid at 0.33 to 0.49 mm.

## What the pictures showed (looked at, not measured)

- A, stock: two wall loops round each strap, then short diagonal fill lines across the rest, turning at the inner wall. Dark notches along every strap edge where they turn.
- B, 4 classic walls: three loops fit on each side of a strap, not four, and one gap-fill line runs down the middle, broken into dashes. Fill is left only in triangles at the strap crossings. Bare shows between the gap-fill dashes and round the triangles.
- B′, strap 3.70: looks the same as B, with the gap-fill line down the middle.
- C, foot 0: four loops fit on each side, and the gap-fill line is gone. A hairline seam is left down the middle of most straps, where the two innermost loops meet. The slit count rose because the seam is counted in pieces. Fill triangles remain at the crossings.
- D, 5 Arachne walls: each strap is filled by walls of varying width, with no seam to be seen along the straps at this scale. Small fill dashes and thin dark slivers are left at the crossings, where wall loops from different straps meet.
