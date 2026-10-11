---
status: draft
---

# The bed face: slits, a bare core, and the slicer settings that close them

**Status:** proposed, 2026-10-10. Nothing in it has been printed. Every number comes from slicing
five pieces with the installed Bambu Studio and drawing the sliced G-code; the record, with the
commands, is [`../../research/2026-10-10-bed-face-slits.md`](../../research/2026-10-10-bed-face-slits.md)
(cited below as "the research"). No decision id is taken here.

**The question.** Omar, 2026-10-10, with a photo of a pink coaster's underside: "why do i get gaps
like this in the plate touching side". The photo shows short dark slits along the straps, a
five-pointed star-shaped hole, and scalloped edges where the fill lines turn. Then: "create a
deaign.md on our approach to fix this rohbustly across all coaster and pieces".

## 1. The short answer

1. **The slits are where the fill lines turn around at the wall.** The first layer is drawn as two
   wall loops round each shape and diagonal lines filling the inside. Each diagonal line stops at
   the inner wall, turns, and comes back. The turn is round, so a thin sliver of bed between the
   turn and the wall gets no plastic. On the underside that sliver is a dark slit. A strap is
   narrow, so it has many turns and many slits.
2. **Small pieces have a second cause: a bare core.** In a small kite, the two wall loops (each
   0.5 mm wide on the first layer) leave a middle too thin for the slicer to fill at all. That
   middle is bare on the first layer and filled one layer up, so it shows as a dimple.
3. **The fix is three slicer settings**, kept in one checked-in preset,
   [`tools/bambu/presets/bed-face-0.20.json`](../../../tools/bambu/presets/bed-face-0.20.json):
   fill the first layer with rings that follow the walls instead of diagonal lines
   (`bottom_surface_pattern` concentric), push the fill further into the wall (`infill_wall_overlap`
   30%, from 15%), and draw the first layer 0.42 mm wide instead of 0.5 (`initial_layer_line_width`),
   which is what fills the kite's core. In the slicer's plan this cuts the bare bed on the first
   layer by 56% to 90% across the five pieces sliced (§4).
4. **It is a plan, not a print.** The pictures show what the slicer asks for at the line width it
   asks for. A narrower first line squashes less, which an older write-up lists as a cause of
   holes on the underside (§7). So the preset is printed on a small coupon, stock beside it,
   before any plate uses it (§5).

## 2. What the first layer is made of

The slicer plans each layer as moves of a nozzle, each a line of plastic of a set width.
`tools/print_review.py paths` draws every move on one layer at that width, colored by what it is:
pink for the outer wall, dark pink for the inner wall, orange for the bottom surface, blue for gap
fill. Black inside the piece is bed that no line covers. With `--below` the drawing is mirrored, so
it reads like the underside held up in the hand.

The stock settings, read from a slice of the X2D 0.20 mm Standard preset
([`fdm_process_dual_0.20_nozzle_0.4.json`](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json)):
two wall loops with classic walls, the first layer 0.5 mm wide, the bottom surface in straight
diagonal lines (monotonic), and the fill reaching 15% of a line width into the wall.

## 3. The causes

### 3.1 Slits where the lines turn at the wall

A diagonal fill line meets the inner wall at an angle, turns in a half-circle, and runs back. The
gap between the round turn and the straight wall is the slit. Overlap pushes the turn into the wall
and narrows the slit; rings that run along the wall have no turns there at all.

![A gBV coaster's first layer, from below: today (left) and the house preset (right)](bed-face-slicing-media/coaster-whole.png)

![A 24 mm crop of the same coaster's straps: today (left), house preset (right)](bed-face-slicing-media/coaster-strap.png)

In the crop, today's straps are edged with dark dashes on both sides. With the house preset the
edges are closed; what is left is a thin row of specks down the middle of some straps, where two
rings meet (§3.3).

### 3.2 A bare core in thin pieces

The small kite is narrow. Two wall loops on each side, each 0.5 mm wide on the first layer, take up
most of its width, and the middle left is too thin for a line. The slicer leaves it bare on the first layer and fills it with
internal solid infill on the second (0.24 sq mm still bare there in a 7 mm square, the research).
Rings and overlap do nothing here, because there is no room for a line to begin with. What helps
is room: a narrower first-layer line (0.42) leaves a middle wide enough for one, and Arachne walls
(which vary their width) fill it with wall instead.

![One small kite: today's first layer, today's second layer, Arachne with 4 walls, the house preset](bed-face-slicing-media/kite-core.png)

### 3.3 What rings bring with them

Rings are not free. Where a ring closes on itself, or where the rings of two straps meet at a
crossing, the slicer leaves a speck, and at the star's center a few four-pointed pinholes. In a
wide flat band the rings shrink to a point and leave a round dot: the largest bare pocket in the
house radial coaster is one such dot, about 0.45 mm across (0.164 sq mm), above the center star.
These are far smaller and fewer than the slits they replace, but they are there, and the coupon
must show whether they show in the print.

![The star coaster's center, 14 mm: today, rings only, the house preset](bed-face-slicing-media/star-center.png)

### 3.4 The glacier plate (a hedge)

The pink coaster in the photo was most likely printed on the glacier plate, which is sliced as a
Smooth PEI plate (the [plate research](../../research/2026-10-07-third-party-plates.md)). The X2D
lowers the nozzle a further 0.02 mm on the first layer for the Textured PEI plate only, so on the
glacier the first layer is squashed less, and a slit the slicer plans is less likely to be closed by
squash. This is likely, not shown: no print here compared the two plates.

## 4. Before and after, piece by piece

Five pieces were sliced, each with the stock preset and with the house preset, on the glacier's
slice (`--plate-type hot_plate`), and drawn at 30 px a millimeter (the research, §"Bare share and
largest pocket"). "Bare share" is the share of the first layer left bare; "largest pocket" is the
biggest single bare spot.

| Piece | Bare share today | House preset | Largest pocket today (sq mm) | House preset |
|---|---|---|---|---|
| Star coaster, 90 mm | 0.88% | 0.38% | 0.684 | 0.108 |
| Radial coaster, 90 mm | 0.54% | 0.11% | 0.390 | 0.164 |
| gBV coaster, 112.5 mm | 0.88% | 0.21% | 0.429 | 0.081 |
| Small kites (a row) | 4.98% | 0.51% | 0.587 | 0.049 |
| Middle piece | 0.21% | 0.03% | 0.050 | 0.004 |

![The star coaster, from below: today (left), the house preset (right)](bed-face-slicing-media/star-whole.png)

![The radial coaster, from below: today (left), the house preset (right)](bed-face-slicing-media/radial-whole.png)

![The small kites today and with the house preset, then the middle piece today and with the house preset](bed-face-slicing-media/pieces-whole.png)

The middle piece is not broken today: its share and largest pocket are both small, and it passes
the check in §6 with the stock settings. Of the five, the small kites gain the most, because only
the narrower line reaches their core.

**The fit carries over** for the rings and the overlap: the outer walls are the same lines as
today, at every layer checked. The narrower first line moves the first layer's outer wall center in
by about 0.04 mm (half the width change), so its planned outer edge stays where it was, and the
layers above are unchanged. Whether a narrower first line also changes the elephant foot in print
is not known; the coupon's fit pieces measure it. Arachne moves the outer walls by 0.017 to 0.028 mm
at every layer, the size of one 0.025 mm fit step, so every fit we have measured would have to be
measured again (the research, "Do the outer walls move?").

## 5. What we change

### 5.1 The options

Bare first-layer area, whole piece, in sq mm (the research): star / radial / gBV coaster / kites /
middle.

| Option | Bare area | Pros | Cons | Implications | What it verifies |
|---|---|---|---|---|---|
| **Stock** (do nothing) | 40.0 / 24.2 / 36.0 / 3.4 / 0.4 | No change, no reprint of any fit. | Slits on every strap; the kites' core stays bare. | Every plate keeps the faces Omar asked about. | Nothing. |
| **Rings only** | 14.3 / 5.5 / 10.7 / 3.4 / 0.2 | The edge slits go; walls unchanged. | Kites unchanged; specks at crossings. | Fixes coasters, not small pieces. | The drawing; the kites' bare area alone (share about 5%) fails `--check`. |
| **Overlap 30% only** | 19.0 / 12.2 / 19.8 / 3.4 / 0.2 | Smallest change; walls unchanged. | Halves the slits, does not remove them; kites unchanged. | A half-step that leaves both defects visible. | The drawing; fails `--check` on the kites. |
| **Rings and overlap** | 15.5 / 5.2 / 16.9 / 3.4 / 0.1 | Cleanest at the star's center (0.027 sq mm bare in a 14 mm close-up, against 0.762 today). | Kites unchanged; more bare than rings alone on the gBV coaster (16.9 against 10.7), not looked into. | As rings only. | The drawing; fails `--check` on the kites. |
| **House preset: rings, overlap, 0.42 first line** (recommended, coupon first) | 17.5 / 5.0 / 8.6 / 0.4 / 0.1 | The only option that fills the kites' core and closes the edges; outer walls planned in the same place. | A narrower first line squashes less, which may cost grip on the bed and may open holes of its own (§7); ring specks stay. | Every experiment recipe changes its settings line, which resets each yes (D-097); fits are kept unless the coupon shows the elephant foot moved. | The drawing and `--check` on all five pieces; the bed face and fit only by the coupon. |
| **Arachne, 4 walls** | 26.3 / 13.3 / 25.6 / 0.9 / 0.7 | Fills most of the kites' core with wall. | Leaves more bare on coasters than the rings; moves every outer wall by about one fit step. | A one-way door: every fit gap we have printed and judged would have to be measured again. | The drawing; the kites' share (over 1%) still fails `--check`; nothing about fit until reprinted. |
| **Rings, overlap, 3 walls** | 13.6 / 5.8 / 10.6 / 3.4 / 0.1 | Lowest bare area on two coasters. | Kites unchanged; more wall on thin straps. | Wall position not checked. | The drawing; fails `--check` on the kites. |

**Recommended: the house preset, printed on a coupon first**, because it is the only option that
fixes both causes and keeps the outer walls where the fits were measured. It is not chosen here:
the coupon is Omar's to approve and judge.

### 5.2 The coupon

One small plate in two halves, on the glacier plate, sliced as Smooth PEI: the stock preset on one
half and the house preset on the other. Each half holds a row of small kites, a middle piece in its
frame and a star coaster. Omar turns them over and compares the undersides, and tries each middle
piece in its frame. The question for him: which half's underside is cleaner, and does either half's
middle piece fit differently?

### 5.3 How it is rolled out, once the coupon says yes

**Default:** until the coupon has printed and been judged, every plate keeps the X2D 0.20 mm
Standard chain unchanged, as
[`fdm_process_dual_0.20_nozzle_0.4.json`](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json)
sets it. This holds because it is the vendor's preset for this printer, nozzle and layer height,
and the house preset has only been checked in the slicer's plan.

If the coupon favors the house preset:

- **Recipes.** An experiment plate's recipe names the preset after the machine:
  `settings: "Bambu Lab X2D 0.4 nozzle;tools/bambu/presets/bed-face-0.20.json"`. The CLI reads that
  path from its own checkout, so a worktree's slice reads the worktree's preset, never the vault's.
  Each changed recipe resets that plate's yes (D-097). Today that costs almost nothing: fit3 is
  waiting on a yes anyway, and split-01, stud-1 and split-02 need a new one before they go.
- **Production plates are left alone.** phones-02 is frozen (D-095); a change to it is a new
  experiment.
- **The tools that write recipes change too**, or the next plate goes back to the stock preset:
  `tools/bambu/src/commands/coaster.ts`, `tools/bambu/src/by-color.ts`, and the skill scripts that
  name the stock preset (`.claude/skills/color-themes/scripts/swatch.py` and the print-model
  scripts). A grep for `0.20mm Standard @BBL X2D` lists them.

[D-095 and D-097](../../working-model/decisions-log.md) are in the decisions log.

## 6. The check

**Validator:** `python3 tools/print_review.py paths <out.png> <plate.3mf> 0.2 <x>,<y>,<side> --below --check`
over each whole piece. It draws the first layer at 30 px a millimeter and fails when the bare share
is 0.6% or more, or the largest bare pocket is 0.2 sq mm or more. Both bars are fitted to the ten
slices in §4, so they are a bet on five pieces, not a rule for every shape; the simulator (§8) is
what widens the set.
PASS: the house preset on all five pieces, including the two closest to a bar: the radial coaster's
ring dot (largest pocket 0.164) and the small kites (share 0.51%). The stock middle piece passes too.
FAIL: the stock radial coaster, which fails on its largest pocket alone (0.390) while its share
(0.54%) is under the bar, and the stock star, gBV coaster and small kites, which fail on both.

What this check can and cannot say: the drawing is the slicer's plan at the width it asks for.
Bed left bare in the plan is very likely bare in the print, since nothing is laid there. Bed
covered in the plan is not proof the print is covered: flow, squash and the plate decide that. So a
PASS means "the slicer is not planning slits", never "the underside will be clean".

## 7. What this does not settle

- **The narrower first line against the older holes table.** The
  [print-quality design](print-quality-design.md#2-tiny-holes) lists "Thin first layer — 0.4 mm
  first-layer line instead of 0.5, and a 45 °C bed instead of 55" as a cause of holes on the
  underside, from minis-04, which printed on Studio's fallback settings. The house preset asks for
  0.42 at the stock 55 °C bed, so the two are not the same case, but the worry carries: a thinner
  line is squashed less and may grip less. Only the coupon settles which wins.
- **Ring specks in print.** Whether the specks and the 0.45 mm dot close up under squash is not
  known.
- **Other nozzles, other sizes, other plates.** Everything here is one nozzle (0.4), one filament
  (Bambu PLA Basic), one layer height (0.2), one plate type (Smooth PEI) and five pieces.
- **Walls 3 and overlap alone** were not checked for wall movement.

## 8. What comes next

1. The coupon (§5.2), as a plate page for Omar's yes.
2. If the coupon favors it: the recipes and the recipe-writing tools switch to the house preset
   (§5.3).
3. A simulator, which Omar asked for on 2026-10-10 ("can we also build a simulator ehere we can
   play with nozzle size and shape size to dind ideal settings"): the same slice-and-draw run over
   nozzle sizes, strap widths and piece sizes, each scored by the check in §6, so the settings can
   be chosen per piece size rather than from five examples.
