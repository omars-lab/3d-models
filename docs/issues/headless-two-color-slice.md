---
date: 2026-10-03
---

# A two-color plate will not slice headlessly, so each color gets its own plate

*Issue slug: `headless-two-color-slice`. Written 2026-10-03, building sheets-04d: the gBV minimal
coaster 1.25 times as wide, with two sets of its loose pieces in two colors.*

## What we tried

Omar asked for "fill pieces 2x of differrnt colors" beside the larger coaster. The first plan was one
plate with every piece on it, each set assigned its own filament, sliced by `bambu slice compose`
through Bambu Studio's command line (02.08.02.61, X2D presets). Two attempts, both failed:

- **Assigning filaments with `--load-filament-ids 1,2`**: Studio crashed (exit 139, a segfault)
  before writing anything.
- **Loading two filament presets without the ids**: Studio flooded the log with `group_nozzle_info`
  errors. That is the X2D's two-nozzle filament grouping, which the command line cannot settle for
  more than one filament (see [the grouping note](x2d-filament-grouping-mode.md), which found the
  mode settable but only tried one material).

## Why the approach changed

Neither failure is in our code, and a two-filament slice made in the Studio window could not pass
through the checks we run on every send (the slice must carry the presets we asked for, sliced for
the plate on the bed). So a two-color plate is not something we can make and check today.

## What replaced it

One color per plate. sheets-04d prints the coaster, and each piece set is its own plate in its own
color. For the send to feed the right tray, the slice has to carry that color: the stock "Bambu PLA
Basic" preset says green (#00AE42), and the send matches trays by color. So a plate recipe now takes
`profile.color: "#RRGGBB"`, written into the one filament preset before slicing and checked in the
slice afterwards (`setFilamentColor` in `tools/bambu/src/commands/slice.ts`).

Both piece sets stay PLA Basic, the material the gap was measured on (sheets-04, sheets-04c). Silk or
another material may print a different width, so a change of material is a new fit question, not a
color swap.

## What would reopen it

A Studio release whose command line slices two filaments on the X2D without crashing. Then the two
piece sets could share a plate again, and the color per item would move from the plate recipe to
the item.
