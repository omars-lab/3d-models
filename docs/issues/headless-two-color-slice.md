---
date: 2026-10-03
---

# A two-color plate slices headlessly after all, once each mesh is given its slot

*Issue slug: `headless-two-color-slice`. Written 2026-10-03, building sheets-04d: the gBV minimal
coaster 1.25 times as wide, with two sets of its loose pieces in two colors. Rewritten 2026-10-04,
when the retry worked and phones-01 became the first two-color plate.*

## What we tried first (2026-10-03)

Omar asked for "fill pieces 2x of differrnt colors" beside the larger coaster. The first plan was one
plate with every piece on it, each set assigned its own filament, sliced by `bambu slice compose`
through Bambu Studio's command line (02.08.02.61, X2D presets). Two attempts, both failed:

- **Assigning filaments with `--load-filament-ids 1,2`**: Studio crashed (exit 139, a segfault)
  before writing anything.
- **Loading two filament presets without the ids**: Studio flooded the log with `group_nozzle_info`
  errors. That is the X2D's two-nozzle filament grouping (see
  [the grouping note](x2d-filament-grouping-mode.md), which found the mode settable but only tried
  one material).

So the plan became one color per plate: sheets-04d for the coaster, sheets-04e and sheets-04f for
the two piece sets. For the send to feed the right tray, each slice has to carry its color: the stock
"Bambu PLA Basic" preset says green (#00AE42), and the send matches trays by color. So a plate recipe
took `profile.color: "#RRGGBB"`, written into the filament preset before slicing and checked in the
slice afterwards (`setFilamentColor` in `tools/bambu/src/commands/slice.ts`).

## What the retry showed (2026-10-04)

Omar asked "can we not consolidate onto a single sheet?", so the same Studio build was tried again,
this time reading its refusals closely.

- **The ids want one entry per input file, not per filament.** `--load-filament-ids` takes the
  1-based slot of each mesh in the order the meshes are passed. With 13 meshes and two filaments it
  takes 13 ids, such as `1,1,2,…`. A wrong list is refused cleanly, exit 254, with a message that
  says what is wrong: `loaded_filament_ids size 2 should be the same with input files size 3`, or
  `invalid filament_id 2 at index 2, max 1` when only one filament is loaded.
- **The crash did not come back.** No variant tried on 2026-10-04 crashed. What made the 2026-10-03
  run crash is not known; it was not kept.
- **Error lines in the log are not a failed slice.** Lines naming filament `T65279` or `T65535`
  appear in slices that come out right, one and two colors alike. The slice is judged by its
  output: the objects, their slots and the colors in the 3MF.
- **Studio picks the nozzles itself.** The X2D has two nozzles. Asking for the hand-set grouping
  (`Manual`) is not honored: the G-code still says `Auto For Flush`, the filament-saving default.
  It puts each color on its own nozzle (`filament_map = 2,1`), which is what we want anyway, so
  nothing is set.

Measured on the combined 13-object plate (the 04d coaster, phone and bear, and both piece sets):

| Plate | Time | Filament |
|---|---|---|
| One plate, prime tower on (Studio's default) | about 164 minutes | 42.3 g |
| One plate, prime tower off | 159 minutes | 40.8 g |
| sheets-04d, 04e and 04f as three plates | 137 minutes | 41 g |

The prime tower is the block the printer wipes the nozzle on between colors. It stays on, as Studio
sets it. One plate costs about half an hour more than three because of the color changes, but it is
one send and one bed to clear instead of three.

## What replaced it

A plate recipe can now name two filaments, a color for each, and a slot for every item:

- `profile.filament` lists two presets, `profile.color` lists one color per preset, and each item
  says `filament: 1` or `filament: 2`. With two filaments, an item without a slot is refused,
  since it would quietly print in slot 1.
- The same preset twice (pink PLA Basic and black PLA Basic) is written to two files, so each
  keeps its own color.
- `bambu slice compose` passes one id per mesh. A mesh in slot 2 is staged as
  `<iteration>-f2.stl`, so the bed map can still tell a pink piece from the same piece in black.
- The checks after the slice already handled two filaments: the preset check looks at each slot,
  and `filament-sync` matches each slot to a tray by color.

[phones-01](../design/plates/phones-01.md) is the first plate made this way: four phones, two
colors, each on the slot its recipe names. The combined 04d/e/f plate is set aside, since Omar
asked for the phones plate instead.

## What would reopen it

A Studio release that refuses or crashes on ids that work today, or a two-color print whose colors
land on the wrong objects. Then each color goes back to its own plate until the cause is found.
