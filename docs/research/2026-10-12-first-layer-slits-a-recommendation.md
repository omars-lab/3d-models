---
date: 2026-10-12
produced-by: Claude (research pass A of two, for the bed-face slits; independent of pass B)
feeds:
  - docs/issues/bed-face-preset-failed-in-print.md
---

# First-layer slits: what to test next (pass A recommendation)

This is the short plan built from [the pass A research](2026-10-12-first-layer-slits-a.md).
It feeds [the issue where the bed-face preset failed in print](../issues/bed-face-preset-failed-in-print.md).
Every value below is a starting guess to test in print, not a known fix.

## The short version

Run one test plate of coaster slices on the smooth plate.
Each slice is one tenth of the coaster, so several fit on one bed.
One slice is stock, as the baseline.
The others each change one setting that can vary per piece.

Then run a short series of whole-plate prints, one setting at a time, for the settings that cannot vary per piece.
Start with the printer's pressure-advance calibration, because it is the only cause a source names for our exact defect.

## Why pressure advance comes first

Bambu's troubleshooting page has a section called "Lines not connected to walls".
Its first cause is a K-factor (pressure advance) set too high.
Bambu's calibration page says the X2D family's automatic K "may sometimes be significantly higher than the manual calibration value", on purpose, to stop blobs at corners.
Putting those two together is my inference: the printer may be easing off the push too early, so each line stops short of the wall.
No source tests this on an X2D first layer. It is a lead, not a finding.

## Plate 1: per-piece tests on one bed

All of these can be set per piece in model_settings.config through the compose step's `object_settings:` block.

| Slice | Change | Values to try | Why |
|---|---|---|---|
| A | none (stock) | — | baseline |
| B | initial_layer_flow_ratio | 1.05 | more plastic on the first layer only; layers above unchanged |
| C | initial_layer_flow_ratio | 1.10 | same, stronger |
| D | infill_wall_overlap | 30% | pushes the diagonal lines into the wall; 30% already closed the edge slits with rings |
| E | infill_wall_overlap | 50% | one H2C user says 55% "almost" removed the holes |
| F | bottom_surface_pattern | monotonicline | switches on the 45% "travel into wall" the X2D profile already ships but our stock pattern ignores |

Notes on this plate:

- **First check the slice, before printing.** initial_layer_flow_ratio is a hidden (Develop-mode) setting. Open the G-code and check the extrusion (E) amounts on the first layer differ between slices A, B and C. If they do not, the setting is being ignored, and print_flow_ratio is the fallback (Bambu's own flow test uses that one per object, but it changes every layer, not just the first).
- **Slice F is the least certain.** That the travel only works on the monotonic-line pattern is read from the source code, not tested. Leave the travel at its 45%; one user found 200% smears the line instead of filling the gap.
- **Do not stack D or E with F.** One user says overlap does not apply to the monotonic-line pattern. This is unchecked; keep them on separate slices so each result is clear.
- **Leave elephant-foot compensation alone.** It moves the wall and the infill edge in together, so it should not change the gap between them.

## Prints 2 onward: whole-plate tests, one per print

These cannot vary per piece. Each needs its own print of the stock slice (or the best slice from plate 1).
They are listed in order of how strong the evidence is.

1. **Pressure advance: Dynamic Flow Calibration Off, with a manual K.** When sending, set the calibration mode to Off. Select a saved K profile for the filament slot, since the page says a saved K "will only be effective in the 'Off' position". Try the profile's 0.02 first, which is at the low end of Bambu's normal 0.02–0.04. If time allows, run Bambu's manual flow-dynamics calibration and use its K. Compare with a print where the mode is Auto.
2. **More squash: Z offset −0.02 mm on the smooth plate.** This copies what the textured plate already does, which gave fewer slits. Do it through the start G-code (the same line the textured plate uses), or the printer's menu if it has that setting (unconfirmed). Two X2D users say −0.014 and −0.02 helped "some".
3. **Slower first layer: 30 mm/s outer wall, 60 mm/s infill.** This is Bambu's own wiki advice. The X2D profile runs 50 and 105. No source explains why the X2D runs faster.
4. **Filament flow 1.00.** Bambu calls 0.98 normal "for PLA filament with X1C" and says 1.00 fixes even gaps. Unverified on the X2D. Skip this if plate 1 already shows a first-layer flow boost works, since that test is narrower.
5. **Hotter first layer: 225 °C, then 230 °C.** Last, because no source here ties temperature to gaps at walls. Both stay inside the 190–230 °C range on the filament data sheet (snippet).

Run a bed leveling before each of these, as Bambu's wiki advises for first-layer problems. That keeps leveling out of the comparison.

## Risks

- **Loose pieces may fit tighter.** More flow, more overlap or more squash all make the bottom edge fatter. The first layer already flares outward (elephant foot). Measure a loose-piece fit on any slice that looks better before adopting it.
- **Ridges.** Too much first-layer flow can leave ridges the nozzle drags over. One H2S user says flow only helped "at the point of obvious over-extrusion".
- **Do not use the second nozzle to test temperature.** The X2D's two nozzles are built differently (direct drive and Bowden, per press snippets). A temperature test across nozzles would test two things at once.
- **The automatic calibration may treat the two nozzles differently.** One review says it covers only the direct-drive nozzle (snippet). Print the pressure-advance test on the same nozzle as the baseline.
- **The slicer's plan is not the print.** Judge every test from photos of the printed bottoms, not from the slicer's bare-share number, which ranked prints wrongly before.

## What this does not settle

- Whether the X2D firmware applies K differently on the first layer. No source says.
- Whether a Develop-mode setting in model_settings.config is honoured in normal mode. The first slice will show it.
- Whether the dashes where rings meet (concentric pattern) respond to any of these. This plan tests the stock diagonal pattern, since rings were dropped.
