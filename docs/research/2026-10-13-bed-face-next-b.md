---
date: 2026-10-13
produced-by: Claude (research pass B of two, for what to try next on the bottom slits after bedface-4; independent of pass A). Read the bedface-4 slice's own G-code and settings, the installed Bambu Studio 02.08.02.61 X2D profiles, Bambu Studio's code (master at commit 47a13ee, not the installed tag), OrcaSlicer's code (main at commit 0dd4b98), and the web pages listed below. Nothing was printed or sliced for this file.
feeds:
  - docs/design/printing/bed-face-slicing-design.md
  - the next bedface plate (not yet written), after docs/design/plates/bedface-4.md
---

# Bottom slits after bedface-4: raw findings, pass B

Kept as found. The ranking and what to print are in
[the recommendation](2026-10-13-bed-face-next-b-recommendation.md). This file builds on
[the checked plan from 2026-10-12](2026-10-12-first-layer-slits-consolidated.md) and
[the bedface-4 record](../prints/2026-10-13-bedface-4/index.md). It does not redo them.

Words used below:

- **Bottom surface:** the solid fill on the first layer, inside the walls. On the X2D stock profile
  it is diagonal lines (the `monotonic` pattern).
- **Wall loops:** the lines that trace the outline. Stock is two per side.
- **Overlap** (`infill_wall_overlap`): how far the fill area is pushed out into the walls.
- **Elephant-foot compensation** (`elefant_foot_compensation`, spelled that way in the slicer): the
  first layer is drawn a little smaller, so its squashed edge does not stick out.
- **Wipe:** at a stop, the nozzle moves back along the line it just laid while pulling plastic back.
- **Per piece:** the slicer keeps the setting for one object, so two pieces on one bed can differ.
  **Whole plate:** one value for every piece on the bed.

## 1. Our own slice: what stock does on the first layer

Source: the bedface-4 slice file (build/plates/bedface-4.plate.3mf in the main checkout; build
output, not tracked). Its G-code, its settings file and its per-object settings were unzipped and
read. Piece `H` (stock, the control) is object 2 on the bed.

### 1.1 Stock values for the keys this pass looked at

Read from the slice's project settings:

| Key | Stock value |
|---|---|
| `initial_layer_line_width` | 0.5 |
| `inner_wall_line_width` | 0.45 |
| `initial_layer_print_height` | 0.2 |
| `wall_loops` | 2 |
| `wall_generator` | classic |
| `wall_sequence` | inner wall/outer wall |
| `is_infill_first` | 0 (walls first) |
| `only_one_wall_first_layer` | 0 |
| `elefant_foot_compensation` | 0.15 |
| `infill_wall_overlap` | 15% |
| `infill_direction` | 45 |
| `bottom_surface_pattern` | monotonic |
| `bottom_surface_density` | 100% |
| `monotonic_travel_into_wall` | 45 |
| `initial_layer_speed` | 50 |
| `initial_layer_infill_speed` | 105 |
| `initial_layer_acceleration` | 500 |
| `filament_flow_ratio` | 0.98 |
| `retraction_minimum_travel` | 1 |
| `reduce_infill_retraction_mode` | Auto |
| `z_hop` | 0.4 |

The profile's `enable_pressure_advance` is 0, so the printer's own Flow Dynamics sets the
pressure advance (K).

### 1.2 The order and shape of `H`'s first layer

- Order on the first layer: outer and inner walls, then gap fill (thin lines of varying width,
  about 0.1 to 0.55 mm), then the bottom surface.
- The stock `monotonic` bottom is one zig-zag: diagonal lines joined by short connectors, about
  0.65 mm long, that run along the inner wall.
- `H`'s bottom-surface section has 729 extrusion moves. 300 are shorter than 0.8 mm, 230 are 0.8 to
  2 mm, 164 are 2 to 5 mm, and 35 are 5 mm or longer. The mean is 1.75 mm.
- The bottom surface is sent at F6300 (105 mm/s), with the acceleration set to 500 mm/s².
- There are 27 wipes inside `H`'s bottom surface. Each one moves back about 1 mm while pulling back
  0.38 mm of filament, pulls back 0.02 mm more, lifts to 0.6 mm in a spiral, and then pushes 0.4 mm
  back in before the next line.

### 1.3 Arithmetic on those numbers (mine, not measured)

- At 500 mm/s², reaching 105 mm/s and stopping again takes about 22 mm of line. A 1.75 mm move
  tops out near 30 mm/s. Only moves longer than about 7 mm can pass 60 mm/s, and fewer than 35 of
  729 are that long. This ignores how the firmware blends corners, which was not modeled.
- 27 wipes against several hundred line ends along the walls (most of the 729 moves end at a
  wall or a connector).
- The stock first layer of a 3.75 mm strap is drawn about 0.3 mm narrower, from elephant-foot
  compensation at 0.15 per side. Two wall loops take roughly 0.9 mm on each side. That leaves a
  band about 1.6 mm wide for the diagonal fill: three or four lines across. With compensation at 0
  the band would be about 1.9 mm. The line spacing here is my estimate from the line width and
  height, not read from the slicer.

### 1.4 What `H`'s photo shows (looked at, not measured)

[`H`'s bottom](../prints/2026-10-13-bedface-4/photos/piece-h-bed-face.jpg): short dark notches on
the inner side of the wall loops, along the strap edges, at a fairly regular spacing.

## 2. bedface-4, as recorded

From [the bedface-4 record](../prints/2026-10-13-bedface-4/index.md), Omar's words, judged by
hand:

- 55% overlap left fewer slits than 30%, with no ridge. `2` (turned) did better than `T`.
- First-layer flow 1.10: `X` fewer than `Y`, `Y` fewer than stock. Still slits.
- First-layer flow 1.05: `U` a bit fewer, `W` the same as stock.
- 30% overlap split: `P` (turned) fewer, `L` more.
- The `monotonicline` pieces (`4`, `7`): about as many as stock, in other places.
- Stock `H` and `J` (turned): "a little less" than bedface-2's whole stock coaster.
- Every piece still slit.
- The slicer's plan had `L` below stock (306 slits against 356). The print did not follow.

Per-piece flow (`initial_layer_flow_ratio`) was set in the slice's per-object settings at 1.05 and
1.1, and the record shows a difference in print.
[compose.ts](../../tools/bambu/src/commands/compose.ts) notes the 1.05 piece laid 1.052 times the
stock piece's plastic per mm on layer 1.

## 3. Bambu Studio's code

Read at master, commit
[47a13ee](https://github.com/bambulab/BambuStudio/tree/47a13eeb1d9af65ef2371e361c856e21d4f6ca72).
The installed slicer is 02.08.02.61, so line numbers differ from the 2026-10-12 files, which read
the tag. Marked `fetched` (the files were read whole from a clone).

| What | Where | What it says |
|---|---|---|
| Per-piece keys | [PrintConfig.hpp L975-1227](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.hpp#L975-L1227) | The object and region groups hold `elefant_foot_compensation` (L982), `wall_generator` (L1064), `only_one_wall_first_layer` (L1073), `infill_direction` (L1111), `infill_wall_overlap` (L1147), `wall_loops` (L1167), `initial_layer_flow_ratio` (L1208) |
| Whole-plate keys | [PrintConfig.hpp L1466-1652](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.hpp#L1466-L1652) | The plate group holds `initial_layer_line_width`, `initial_layer_print_height`, the first-layer speeds and acceleration, `retraction_minimum_travel`, `is_infill_first` (L1621) |
| No bottom-only flow or overlap | the same file | No `bottom_solid_infill_flow_ratio` and no separate bottom overlap key. One `infill_wall_overlap` serves every layer |
| How far the overlap pushes | [PerimeterGenerator.cpp L1386](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PerimeterGenerator.cpp#L1386) | The push is the percent times half the wall spacing plus half the solid fill spacing (classic walls). Arachne walls use it at [L1451](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PerimeterGenerator.cpp#L1451) |
| Overlap range | [PrintConfig.cpp L4114](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.cpp#L4114) | No upper limit is set in the definition |
| Fill angle | [Fill.cpp L287](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/Fill/Fill.cpp#L287) | The solid fill's angle is taken from the piece's `infill_direction` |
| One wall on layer 1 | [PerimeterGenerator.cpp L919](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PerimeterGenerator.cpp#L919) | Wall loops drop to one when `only_one_wall_first_layer` is on and the layer is 0. Tooltip at [PrintConfig.cpp L1618](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.cpp#L1618): "Use only one wall on the first layer of model" |
| Infill first | [PrintConfig.cpp L2294](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.cpp#L2294) | "Order of wall/infill. false means print wall first." |
| Bottom density | [PrintConfig.cpp L2203](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.cpp#L2203) | 10 to 100%, "Intended for aesthetic or functional purposes, not to fix issues such as over-extrusion." |
| Elephant-foot compensation | [PrintObjectSlice.cpp L1289-1330](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintObjectSlice.cpp#L1289-L1330) | Applied to the layer-0 outline before walls and fill are made, so walls and fill shrink together. Only when there is no raft |

## 4. OrcaSlicer's code

Read at main, commit
[0dd4b98](https://github.com/SoftFever/OrcaSlicer/tree/0dd4b98604ab4774d93b33b0a758523ee979f431),
fetched 2026-10-13. Marked `fetched` (both files downloaded whole).

| What | Where | What it says |
|---|---|---|
| A separate overlap for top and bottom | [PrintConfig.cpp L4944](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PrintConfig.cpp#L4944) | `top_bottom_infill_wall_overlap`, 25% by default. Tooltip: "A value of 25-30% is a good starting point, minimizing the appearance of pinholes." |
| The plain overlap | [PrintConfig.cpp L4934](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PrintConfig.cpp#L4934) | `infill_wall_overlap`, 15% by default. "Set this value to ~10-15% to minimize potential over extrusion" |
| Layer 1 uses the top/bottom overlap | [PerimeterGenerator.cpp L2028-2033](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PerimeterGenerator.cpp#L2028-L2033) | When `layer_id == 0`, the push uses `top_bottom_infill_wall_overlap`, with the same formula Bambu uses for its single key. Arachne walls: [L2979-2983](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PerimeterGenerator.cpp#L2979-L2983) |
| A bottom-surface flow | [PrintConfig.cpp L1692](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PrintConfig.cpp#L1692) | `bottom_solid_infill_flow_ratio`, "affects the amount of material for bottom solid infill." Bambu has no such key (§3) |
| A first-layer flow | [PrintConfig.cpp L1709](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PrintConfig.cpp#L1709) | `first_layer_flow_ratio`, multiplied into each path role on the first layer |
| Gap fill on top and bottom | [PrintConfig.cpp L1492](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PrintConfig.cpp#L1492) | `gap_fill_target`: "making sure the top and bottom surfaces have no pinhole gaps" |

## 5. Web sources, fetched

Each was opened in full. The quotes are as the fetch returned them.

### 5.1 Bambu forum 256070, "Need help please. Small gaps on first layer"

- URL: <https://forum.bambulab.com/t/need-help-please-small-gaps-on-first-layer/256070>
- Posted 2026-07-02 to 07-03. A1 or A1 mini, Bambu Studio. `fetched`.
- Slowing the first layer to 25 mm/s "seemed to make it worse".
- EnoTheThracian: "You will not be able to eliminate all gaps, but the Arachne wall generator helps somewhat."
- EnoTheThracian: "Arachne allows printing of local line widths down to ~60% of the nozzle diameter."
- Monotonic line was said to close the triangle void that `monotonic` leaves at a slanted wall.
- No fix confirmed in the thread.

### 5.2 Bambu forum 68800, "Gap between infill and inner wall"

- URL: <https://forum.bambulab.com/t/gap-between-infill-and-inner-wall/68800>
- Posted 2024-04-05. P series, OrcaSlicer. The gaps were on layers above the first. `fetched`.
- Flow up to 1.1 and overlap up to 25% did not fix it.
- Slowing by 50% "mitigates".
- K lowered from 0.025 to 0.012 "eliminated almost all gaps".
- Gavrik: "Very similar to incorrect PA".

### 5.3 Bambu forum 216407, "H2S issue where infill meets perimeter at front of print"

- URL: <https://forum.bambulab.com/t/h2s-issue-where-infill-meets-perimeter-at-front-of-print/216407>
- Posted 2025-12-14 to 12-15. H2S, first layer, a large print, front left only. `fetched`.
- mugglesmuggle: "That looks more like the Z height is changing and you are getting different squish".
- hotellonely: "just infill/perimeter overlap rate set too low".
- The poster still saw it at 50% overlap. Unresolved.

### 5.4 Bambu forum 86402, "Filling the gap between outer wall and archimedean infill"

- URL: <https://forum.bambulab.com/t/filling-the-gap-between-outer-wall-and-archimedean-infill/86402>
- Posted 2024-07-08 to 07-09, and 2025-05-09. Bambu Studio and OrcaSlicer 2.1.1. Archimedean fill
  at 100%. `fetched`.
- At 75% overlap: "You can see the gap close in the preview". Preview only, not a print.
- OrcaSlicer's gap fill filled it but left a bump.
- "Filter out tiny gaps" "didn't change any of the slicing result".
- JonRaymond: it may show less in print than in the preview.

### 5.5 Bambu forum 198663, "Please add percentage setting for overlap of top layer/walls"

- URL: <https://forum.bambulab.com/t/please-add-percentage-setting-for-overlap-of-top-layer-walls/198663>
- Request posted 2025-09-30; reply 2026-04-28 (H2D). `fetched`.
- On the 15% overlap: "but that is not for the top layer."
- The reply points to `monotonic_travel_into_wall` in Develop mode, and says it is 45% on the H2
  series and P2S and 0% on other Bambu printers.
- The reply: the 45% "caused my H2D to print the top infill over the edge of the print on round corners."
- Our X2D slice reads 45 (§1.1), not 0.

### 5.6 Bambu forum 146050, "Holes in first layer"

- URL: <https://forum.bambulab.com/t/holes-in-first-layer/146050>
- Posted 2025-02-15 to 02-17. A1, smooth plate, matte PLA. `fetched`.
- EnoTheThracian: concentric bottom, or many walls with Arachne, and a little more first-layer flow,
  "max 5%".
- Sigama_Crafts: raise the overlap, change the bottom pattern; later 100% overlap with other changes.
- No result reported for those settings on the original model.

### 5.7 Bambu forum 250557, "Fixing first layer"

- URL: <https://forum.bambulab.com/t/fixing-first-layer/250557>
- Posted 2026-04-20 to 04-21. P2S, Bambu Studio, textured plate. `fetched`.
- lkraus: gaps where the nozzle changes direction "nearly always indicates incorrect pressure advance".
- Jacques_Premium on Z: "probably his 0 is a little too high".
- The poster then changed K from 0.12 to 0.02, the Z offset, first-layer flow to 1.05, and the
  slice gap closing radius, all at once. Result: better, goal not met.

### 5.8 Prusa forum, "Gap between infill and perimeters"

- URL: <https://forum.prusa3d.com/forum/prusaslicer/gap-between-infill-and-perimeters/>
- Posted 2021-10-18. MK3S+ with MMU2S, PrusaSlicer. First few layers. `fetched`.
- Overlap at 100%: "no improvement".
- Neophyl: "not a slicing issue, you need to be looking for something physical on the printer".
- Fixed by tightening the Y belt: "That was it! Now it's printing like a champ again!"

### 5.9 Prusa forum, "Gap Between Solid Infill and Perimeters"

- URL: <https://forum.prusa3d.com/forum/prusaslicer/gap-between-solid-infill-and-perimeters/>
- Posted 2025-02-04 (shown as 04/02/2025, day first). Printer and version not given. `fetched`.
- The gap: "consistently a small gap on first layers and surfaces above supports."
- Neophyl, on the first-layer part: "This is a issue with your first layer height."
- No result reported.

### 5.10 Bambu forum 145182, "First layer walls separating from infill"

- URL: <https://forum.bambulab.com/t/first-layer-walls-separating-from-infill/145182>
- Posted 2025-02-12 to 02-26. A1 mini, OrcaSlicer, PETG, textured PEI. `fetched`.
- Flow and K changes first; little change.
- A reply noted the usual compensation is about 0.05, not the 0.2 the poster had.
- The poster turned elephant-foot compensation off: "That elephant foot compensation seemed to be the culprit."
- Very slight first-layer gaps remained afterward.

### 5.11 OrcaSlicer wiki, strength settings, infill

- URL: <https://github.com/SoftFever/OrcaSlicer/wiki/strength_settings_infill>
- Last edited 2026-10-08. `fetched`.
- Overlap: "Infill area is enlarged slightly to overlap with wall for better bonding."
- Gap fill target "Top and Bottom surfaces": "Applies gap fill to top and bottom surfaces only, balancing print speed".
- The page has no section on a top/bottom overlap (the code has one, §4).

### 5.12 LulzBot forum 4844, "Gaps between perimeter and fill"

- URL: <https://forum.lulzbot.com/t/gaps-between-perimeter-and-fill/4844>
- Posted 2017-04-28 to 05-15. LulzBot, Slic3r, ABS, the top surface. `fetched`.
- More top layers filled the top: "The top is now filled."
- The page does not mention outline overlap. A search summary had pointed here for the
  40%-to-60% claim in §6; the claim is not on this page.

### 5.13 Prusa forum, "help with gaps"

- URL: <https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-how-do-i-print-this-printing-help/help-with-gaps>
- Posted 2025-06-19. Only the first post, no replies. `fetched`.
- "gaps between the perimeter and the solid infill of the first few layers"
- The page does not mention one wall on the first layer or a height-range modifier. A search
  summary had attributed that advice to a Prusa thread; it is not on this page.

## 6. Web sources, snippet only

Seen in search results, not opened, or opened without the claim on the page. None is used for a
ranking step without saying so.

| Source | URL | What the snippet said |
|---|---|---|
| A search summary, page not found | none confirmed | "start with 40%" outline overlap, and 60% removed the gaps ("Outline Overlap" is Simplify3D's name for the setting) |
| A Prusa moderator, page not found | none confirmed | one perimeter on the first layer, through a height-range modifier from 0 to 0.2 mm |
| Obico, "gaps in print surfaces" | <https://www.obico.io/blog/gaps-in-print-surfaces/> | the nozzle may be too far from the bed for first-layer gaps; too much retraction leaves gaps where retractions happen |
| STLFlix help, gaps and holes | <https://help.stlflix.com/en/articles/7178444-gaps-holes> | raise infill outline overlap; too much shows the pattern through walls |
| Simplify3D forum | <https://forum.simplify3d.com/viewtopic.php?p=34124> | listed under "gaps between infill and perimeter"; not opened |
| An OrcaSlicer mirror commit | <https://git.trueserve.org/PublicCodeMirror/OrcaSlicer-bambulab/commit/07cd25d0ecd3d4a2fce834b7f735a44c151aa254> | an overlap added "for better bonding"; "backlash might cause gaps" |
| Bambu forum 237388 | <https://forum.bambulab.com/t/237388> | 50% overlap closed edge holes but may warp the outer wall |
| r/FixMyPrint, "gaps in first layer" | not recorded | general first-layer gap advice |
