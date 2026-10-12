---
date: 2026-10-12
produced-by: Claude (research pass B of two, for the bed-face slits; independent of pass A)
feeds:
  - docs/issues/bed-face-preset-failed-in-print.md
---

# First-layer slits: what to test next (pass B's recommendation)

This is the short version of [the pass B research](2026-10-12-first-layer-slits-b.md). It says
what to print to find out which first-layer settings close the slits on the coaster's bed side.
Items marked **(unsure)** rest on code I read or on one user's report, not on a print.

## The one thing to try first

Switch the first-layer pattern from `monotonic` to `monotonicline`.

- The stock X2D profile already holds a setting that pushes each first-layer line further into
  the wall before it turns. It is set to 45%.
- The stock pattern switches it off. The slicer only uses it with `monotonicline`.
- The edge slits are lines that turn short of the wall. That is the problem this setting is for.
- Our plate tool already accepts `monotonicline` per piece. So this needs no new code.
- **(unsure)** No print has tried it. One H2 user said it did not help them. A user on Bambu's
  bug tracker suspects the slicer mis-counts the area beside these turns.
- It will not touch the rings' meeting dashes. Those belong to the rings pattern.

## Plate 1: settings that can change piece by piece

Each piece is one tenth of the coaster. All go on one bed, in one color, on the glacier plate.
Each piece carries its own settings.

| Piece | Setting changed from stock | Why |
|---|---|---|
| S | none (stock) | the baseline |
| A | pattern `monotonicline` | turns on the 45% push into the wall |
| B | pattern `monotonicline`, push into wall 100% | a stronger push **(unsure: the highest value the slicer takes is not checked)** |
| C | pattern `monotonicline`, overlap 30% | Bambu's own suggested workaround on the H2 bug |
| D | first-layer flow 1.05 | a little more plastic on layer one only |
| E | first-layer flow 1.10 | more again |
| F | rings, overlap 30%, first-layer flow 1.10 | do the meeting dashes close with more plastic? |

Before printing, two steps are needed.

1. **Teach the plate tool the new keys.** It allows a per-piece key only after a slice shows
   Studio kept it. The push into the wall and the first-layer flow are not on its list yet.
2. **Slice once and check.** Look in the sliced file that each piece kept its own values. For the
   flow pieces, check that the plastic fed per millimetre on layer one really differs from S.
   **(unsure)** I read in the code that first-layer flow can be set per piece. I did not slice it.
   It is a developer-mode setting.

Leave elephant-foot compensation alone on this plate (see Risks).

## Plates 2 and on: settings that need their own print

These settings apply to the whole plate or the whole filament. Each needs its own print. Put one
stock-shaped piece on each, and compare it with S from Plate 1. Keep the color, plate and model
the same.

Listed with the strongest outside evidence first.

1. **Start the nozzle a little lower.** Try 0.02 mm lower than now. That is the same trim the
   textured plate gets.
   - Gaps between first-layer lines most often mean the nozzle is too high. Three sources here
     say so. Only one was read in full; the other two were seen only in search summaries.
   - Two X2D users lowered it by 0.014 mm and 0.02 mm, with good and partial results.
   - Our gold textured plate, which starts 0.02 mm lower, gave fewer slits.
   - How: a copy of the start G-code with the textured value used for the glacier plate, or the
     printer's own first-layer offset. **(unsure)** I did not confirm that offset menu from
     Bambu's own pages.
   - Using the textured trim on a smooth plate goes against what Bambu intended. Bambu lowers it
     only because the texture's peaks touch the nozzle when homing.
2. **Turn Flow Dynamics to On at the send.** This makes the printer measure its pressure setting
   before this print.
   - It costs only a little time at the start.
   - It mostly bears on gaps where the nozzle changes direction, not on gaps along a wall.
   - Bambu says its results vary by about 10%.
3. **Slower first-layer infill.** Try 50 mm/s, down from 105 mm/s.
   - One general guide says fill printed too fast cannot bond to the wall.
   - Bambu support reportedly told an H2 user to go slower still. The user said it was still
     not good.
4. **Filament flow 1.00, up from 0.98.** This changes every layer, not just the first. Better to
   run Bambu's flow calibration once than to guess.
5. **First-layer nozzle 225 °C, up from 220 °C.** **(unsure)** This is the weakest lead. No source
   here tested heat for gaps between lines on the bed.

Not worth a print yet:

- A narrower first line. Our 0.42 mm line did nothing.
- A thicker first layer.
- Bed temperature. No source ties it to these gaps.

## Risks

- **Loose pieces fit tighter.** More plastic on layer one makes the bottom edge fatter.
  - bedface-1 already came out one 0.025 mm fit step tighter with more overlap and the narrow
    line.
  - Any winner here needs a fit check on the loose pieces before it becomes the house setting.
- **Elephant-foot compensation is the biggest fit risk.** Stock shrinks the first layer by
  0.15 mm. Setting it to 0 could let each edge sit up to 0.15 mm further out, which is far more
  than one fit step. That is my reading of its description, not a measurement. Test it only
  together with a fit check.
- **Too much overlap bulges.** Bambu's wiki warns the surface can bulge.
- **Too low a nozzle smears.** Lines turn smooth or wavy, especially on a smooth plate.
- **The H2 bug may or may not apply.** Bambu's bug report names the H2 printers. The X2D shares
  their profiles and calibration, but no source shows the bug on an X2D.
- **The slicer's plan does not rank prints.** Judge each piece from the print itself, as before.
