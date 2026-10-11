---
date: 2026-10-10
produced-by: Claude Opus 5.5, in the session that answered Omar's photo of a pink coaster's bed face ("why do i get gaps like this in the plate touching side"). Every number below came from slicing with the installed Bambu Studio CLI (through `bambu slice compose`) and drawing the sliced G-code with `tools/print_review.py paths`. No piece was printed for this file, and no web source was read.
feeds:
  - docs/design/printing/bed-face-slicing-design.md
---

# Bed-face slits: what the slicer plans on the first layer

Kept verbatim as the record the design doc's numbers come from. The pictures and slices were made
in the session scratchpad and are not kept; the commands below make them again.

## What was sliced

Four scratch recipes and the gBV coaster, each with `no_id: "scratch slice, not printed"`, all on
`bed: x2d`, filament `Bambu PLA Basic @BBL X2D 0.4 nozzle`, sliced `--plate-type hot_plate` (the
glacier plate's slice):

| Name | Construction | Piece | Params |
|---|---|---|---|
| star | `7apC5Q9QS-8-minimal-coaster` | the coaster | size 90, strap 3, height 4, round 1 |
| radial | `GimTvN9hw4U-radial-coaster` | the coaster | size 90, strap 3, height 4, round 1 |
| coaster | `gBV_JTt3Kxk` coaster | the coaster | size 112.5, strap 3.75, height 4.4, round 1.25 |
| kite | `gBV_JTt3Kxk-minimal-pieces` | Kite (a row of small kites) | size 112.5, strap 3.75, height 4.4, gap 0.05 |
| middle | `gBV_JTt3Kxk-minimal-pieces` | Middle | size 112.5, strap 3.75, height 4.4, gap 0.025 |

## The variants

Each is a process file with `"type": "process"`, `"from": "User"` and
`"inherits": "0.20mm Standard @BBL X2D"`, plus:

| Variant | Keys set |
|---|---|
| base | none (the recipe's stock preset, no `-s`) |
| overlap30 | `infill_wall_overlap` 30% |
| concentric | `bottom_surface_pattern` concentric |
| arachne4 | `wall_generator` arachne, `wall_loops` "4" |
| combo | concentric and 30% |
| walls3 | combo and `wall_loops` "3" |
| narrow | combo and `initial_layer_line_width` "0.42" |

Every slice exited 0, and each variant's keys were read back from the slice's
`Metadata/project_settings.config`.

The stock values, read from the base slice: `bottom_surface_pattern` monotonic,
`infill_wall_overlap` 15%, `initial_layer_line_width` 0.5, `line_width` 0.42,
`outer_wall_line_width` 0.42, `inner_wall_line_width` 0.45, `wall_generator` classic, `wall_loops`
2, `bottom_shell_layers` 3, `initial_layer_print_height` 0.2, `detect_thin_wall` 0,
`filter_out_gap_fill` 0, `elefant_foot_compensation` 0.15.

## Commands

Slice: `bambu slice compose <recipe.yaml> -s "Bambu Lab X2D 0.4 nozzle;<variant.json>" -d <dir> -o <name>-<variant>.3mf --no-record --plate-type hot_plate`
(the base slice leaves out `-s`).

Draw and measure: `python3 tools/print_review.py paths <out.png> <slice.3mf> 0.2 <cx>,<cy>,<side> --below --px <n>`,
at 30 px a millimeter for whole pieces (star and radial 95 mm at 2850 px, coaster 115 mm at 3450,
kite 30 mm at 900, middle 40 mm at 1200), all centered on 138.25,128. Close-ups: the star's center,
14 mm at 138.25,128; one small kite, 7 mm at 140.4,128.3.

## Bare area on the first layer, whole piece (sq mm)

Bare means black left inside the print in the drawing: bed no planned line covers. The slit count
`paths` also prints is not used here, since a whole piece at 30 px a millimeter counts single-pixel
specks as slits.

| Piece | base | overlap30 | concentric | arachne4 | combo | walls3 | narrow |
|---|---|---|---|---|---|---|---|
| star | 39.97 | 19.04 | 14.30 | 26.29 | 15.50 | 13.61 | 17.50 |
| radial | 24.24 | 12.17 | 5.54 | 13.26 | 5.16 | 5.82 | 5.01 |
| coaster | 35.98 | 19.79 | 10.71 | 25.59 | 16.90 | 10.64 | 8.57 |
| kite | 3.43 | 3.43 | 3.43 | 0.94 | 3.43 | 3.43 | 0.36 |
| middle | 0.41 | 0.15 | 0.17 | 0.69 | 0.12 | 0.08 | 0.05 |

## Close-ups (sq mm bare)

| Close-up | base | concentric | overlap30 | arachne4 | combo | walls3 | narrow |
|---|---|---|---|---|---|---|---|
| star center, 14 mm | 0.762 | 0.065 | 0.277 | 0.384 | 0.027 | 0.057 | 0.035 |
| one kite, 7 mm | 0.610 | 0.610 | 0.610 | 0.156 | 0.610 | 0.610 | 0.060 |

The base kite at z 0.4 (its second layer) drew 0.24 sq mm bare in the same 7 mm square: the core
the first layer leaves bare gets internal solid infill there, with small gaps left in it.

## What the pictures showed (looked at, not measured)

- star, base: dark dashes along every strap edge, where the diagonal bottom lines turn at the inner
  wall.
- star, concentric: the edge dashes gone; small specks left where loops close at strap crossings,
  and a thin seam down the middle of some straps. Close-up: four-pointed pinholes at the crossings.
- star, narrow: the cleanest of the set; the specks at crossings remain.
- kite, base: two wall loops 0.5 mm wide and a gap-fill line, with a bare core in the middle of the
  kite. At z 0.4 the core gets internal solid infill.
- kite, arachne4: the core mostly filled by walls. kite, narrow: the core filled by bottom surface,
  one tiny speck left.

## Do the outer walls move? (the fit carries over or not)

For each variant, the distance from each point of its outer wall to the nearest point of the base
slice's outer wall, per layer:

| Variant | Result |
|---|---|
| concentric, combo | the same walls: median and 99th percentile 0.000 mm at z 0.2, 0.4 and 2.0. One largest value of 0.8 to 1.9 mm per layer, not looked into (a seam or a start point is the likely reason; not checked). |
| narrow | first layer only: median 0.04 mm, 99th percentile up to 0.083 (kite) and 0.042 (coaster). The wall's center line moves in by half the width change, so the planned outer edge stays where it was. Layers above are the same as base. |
| arachne4 | 99th percentile 0.017 to 0.028 mm at every layer, the size of the 0.025 mm fit step. |
| walls3, overlap30 | not checked. |

## A checked-in preset by path (after the above)

`tools/bambu/presets/bed-face-0.20.json` (combo plus the 0.42 first-layer line, the narrow variant)
sliced the middle piece through a recipe whose `profile.settings` names it by repo path, once the
CLI read repo paths from its own checkout: `preset check: PASS`, no slicer warnings, and the slice's
config reads `bottom_surface_pattern` concentric, `infill_wall_overlap` 30%,
`initial_layer_line_width` 0.42, `print_settings_id` "Naqsh bed face 0.20mm @BBL X2D".

## Bare share and largest pocket (added later the same day)

`paths` was extended to print, beside the bare area, the area the drawing shows printed, the bare
share (bare over bare plus printed) and the largest single bare pocket. The same slices, the same
commands, base against narrow (narrow is the checked-in preset; the middle piece's narrow row is
the slice made through it by path):

| Piece | Variant | Bare (sq mm) | Printed (sq mm) | Bare share | Largest pocket (sq mm) |
|---|---|---|---|---|---|
| star | base | 39.967 | 4516.6 | 0.88% | 0.684 |
| star | narrow | 17.501 | 4570.6 | 0.38% | 0.108 |
| radial | base | 24.240 | 4504.8 | 0.54% | 0.390 |
| radial | narrow | 5.007 | 4535.7 | 0.11% | 0.164 |
| coaster | base | 35.978 | 4055.5 | 0.88% | 0.429 |
| coaster | narrow | 8.567 | 4100.5 | 0.21% | 0.081 |
| kite | base | 3.429 | 65.5 | 4.98% | 0.587 |
| kite | narrow | 0.358 | 69.4 | 0.51% | 0.049 |
| middle | base | 0.413 | 200.7 | 0.21% | 0.050 |
| middle | narrow (by path) | 0.053 | 200.9 | 0.03% | 0.004 |

Looked at, not measured: the radial narrow slice's largest pocket is one round dot about 0.45 mm
across, in the wide flat band above the center star, where the concentric loops of that band run
out. It is the concentric close point, the same defect as the specks at strap crossings, larger
here because the band is wide.
