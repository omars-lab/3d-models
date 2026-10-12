---
date: 2026-10-12
produced-by: Claude (research pass A of two, for the bed-face slits; independent of pass B)
feeds:
  - docs/issues/bed-face-preset-failed-in-print.md
---

# First-layer slits on the coaster bottom: what the sources say (pass A)

This file collects what outside sources say about closing thin slits in the first layer.
It feeds [the issue where the bed-face preset failed in print](../issues/bed-face-preset-failed-in-print.md).
The short recommendation built from it is in [the pass A recommendation](2026-10-12-first-layer-slits-a-recommendation.md).

## The setup and the problem

The printer is a Bambu Lab X2D with a 0.4 mm hardened nozzle.
The filament is Bambu PLA Basic, sliced with "0.20mm Standard @BBL X2D".
The coaster bottom shows thin slits in two places:

- along strap edges, where the diagonal first-layer lines stop short of the wall;
- with ring-shaped (concentric) first-layer lines, as short dashes where two sets of rings meet down the middle of 3.75 mm straps.

Stock first-layer values, read from the project settings inside the sheets-04g-fit2 plate file (Bambu Studio 02.08.02.61):

| Setting | Stock value |
|---|---|
| nozzle_temperature_initial_layer | 220 °C |
| filament_flow_ratio | 0.98 |
| initial_layer_flow_ratio, print_flow_ratio | 1, 1 |
| enable_pressure_advance, pressure_advance | 0, 0.02 |
| initial_layer_speed, initial_layer_infill_speed | 50, 105 mm/s |
| hot_plate_temp_initial_layer | 55 °C |
| initial_layer_print_height, initial_layer_line_width | 0.2 mm, 0.5 mm |
| bottom_surface_pattern | monotonic |
| infill_wall_overlap | 15% |
| monotonic_travel_into_wall | 45% |
| elefant_foot_compensation | 0.15 mm |
| close_fan_the_first_x_layers | 1 |
| ensure_vertical_shell_thickness | enabled |

What our own prints already showed, and this file does not re-research:

- Rings plus 30% overlap closed the strap-edge slits but left dashes where the rings meet.
- A 0.42 mm first line instead of 0.5 mm made no difference.
- The gold textured plate starts 0.02 mm lower and gave fewer slits. So more squash helps, but it is not the whole answer.
- The slicer's planned "bare share" did not rank the prints correctly.

How to read the marks below:

- **Fetched** means the page itself was downloaded and read.
- **Snippet** means only a search-result summary was seen. Treat those claims as leads, not facts.
- **Source code** means the Bambu Studio source on GitHub was read at the tag that matches the installed app (v02.08.02.61), unless it says master.

25 sources are in the table at the end: 15 fetched pages, the Bambu Studio source (counted once), and 9 seen only as snippets.
This is not a full survey; it says nothing about sources it did not find.

---

## 1. Pressure advance and the printer's own flow calibration (strongest match to our symptom)

### What the sources say

**Bambu wiki, "Troubleshooting printing issues" (fetched).**
It has a section titled "Lines not connected to walls".
Its first cause is "K-factor set too high".
It says: "The most common problem which causes such print quality issues, where the printed lines are not touching with each other is caused by a K-factor which is incorrectly set to a very high value."
It gives a normal range: "Most common results for regular filaments give a K-factor value between 0.02 and 0.04 as long as the hotend is free from any partial clog, and the extruder is clean."
Above 0.04–0.05 it advises cleaning the extruder and hotend and calibrating again.
This is the only source found here that names our exact defect (lines that stop short of the wall).
It does not name a printer model for this section.

**Bambu wiki, "Flow Dynamics Calibration" (fetched).**
The K-factor is the pressure-advance value.
A section is titled "H2D/H2S/P2S/X2D Printer", so it covers our printer.
These printers purge at the wiper and read extrusion force with an eddy-current sensor in the toolhead.
There are three modes before a print:

- Automatic: calibrates again only if the filament, nozzle or hotend changed.
- On: calibrates before each print (the page calls it "open").
- Off: "The system will use the K value (PA profile) you set manually. If there is no profile for the filament in this slot, the system default value (default) will be used."

The page says the automatic K can run high on purpose:

- "To prevent corner stacking effects, the Factor K during H2D automatic flow calibration will be set higher than in pattern mode of manual calibration."
- "The automatic calibration value (K value) of the algorithm may sometimes be significantly higher than the manual calibration value, which is normal. This design is intended to avoid filament pile-up problems at the corners of the model by slightly increasing the K value, thereby better ensuring the assembly accuracy between models."
- "If a saved PA profile is selected, the K value will still be displayed, but will only be effective in the 'Off' position."

Hedge: these quotes name the H2D. The section header lists the X2D, but the body text does not say the X2D behaves the same in every detail.

**Bambu Studio source (source code).**
The process option enable_pressure_advance has the tooltip "Enable pressure advance, auto calibration result will be overwritten once enabled. Useless for Bambu Printer".
The pressure_advance tooltip also ends "Useless for Bambu Printer".
So the profile's 0.02 is very likely not what the X2D prints with.
The printer's own K (calibrated, or set on the printer) decides it.

**Bambu forum, "Community Tech Talk: deep dive into auto flow dynamics calibration" (fetched).**
It says the calibration sets pressure-advance parameters during print preparation.
It does not mention the flow ratio.

**Bambu wiki, "Flow rate calibration" (fetched).**
It says "Only X1 series support Auto calibration" for the flow ratio.
That page may be out of date for newer printers. It still means the X2D's automatic step should be read as a K calibration, not a flow-ratio calibration.

**Bambu Studio GitHub issue #9768, "Gaps in prints" (fetched, open, on an H2C).**
One user (ingoingo) suspects pressure advance for gaps between monotonic lines and walls.
That is a user guess, not a finding.

**X2D retailer and press pages (snippets).**
They describe "Dynamic Flow Calibration" before each print on the X2D.
One review says it covers only the direct-drive (left) nozzle. This is not confirmed here.

### What this means for us (inference, not tested)

A line that ends early at a wall is what too much pressure advance would do.
Pressure advance eases off the push before a line ends, so a high K can stop the bead short.
That link from "higher K" to "our slits" is my inference.
The wiki ties high K to lines not touching, and ties the H2D-family auto K to running high; it does not tie it to first layers on the X2D.

Transfer conditions: the wiki troubleshooting page is general across Bambu printers.
It transfers because the X2D uses the same Flow Dynamics system, named in the X2D section header.
It would not transfer if the X2D's firmware applies K differently on the first layer; no source here says either way.

### Where it is set

Pressure advance cannot vary per piece.
It is per filament slot on the printer, and the mode (Auto, On, Off) is chosen when the print is sent.
In the slicer, enable_pressure_advance and pressure_advance are filament settings (GCodeConfig class in [PrintConfig.hpp at L1220–L1231](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1220)).

---

## 2. Flow: filament flow ratio and first-layer flow

### What the sources say

**Bambu wiki, "Troubleshooting printing issues" (fetched).**
Under "Even gaps in the top layer (Under extrusion)":
"the value is set to 0.98 which is considered normal for PLA filament with X1C. To solve this issue, increasing the flow rate to 1.00 should solve the problem and give you better results."
It also says: "It is very rare for the filament to require more than a 1.00 flow rate value in the Filament profile."
It tells you to rule out a partly clogged nozzle or a dirty extruder first.

**Bambu wiki, "Flow rate calibration" (fetched).**
"Not all defects… are the result of inaccurate flow rates."
Manual coarse calibration covers 80–120% in 5% steps; the fine pass covers 91–100% in 1% steps.
The sample is judged on its top surface. The worked example lands on 0.9975.
Hedge: this calibrates the top surface, not the first layer against the bed.

**Bambu wiki, "Identify and fix first-layer issues with a test print" (fetched).**
A good first layer has "no gaps between the lines".
"Cracks on the first layer" are "often caused by a dirty nozzle or the flow rate not set correctly."
For uneven texture it says to run bed leveling "before trying any other adjustments", then check flow.

**Bambu wiki, "PLA" filament page (fetched).**
For clear PLA prints (a different goal), it says "Moderately increasing the flow ratio helps to completely fill the tiny gaps between print lines."

**Bambu forum, H2S thread "First layer is not squished enough, visible gaps" (fetched).**
One user says raising the flow (extrusion multiplier) "does not really fix it unless I push it to the point of obvious over-extrusion".
Changing nozzle, filament and temperatures did not help that user.
This is one user on an H2S, not a test.

**Bambu forum, X2D thread "PLA print flow rate isn't fine or some other issue" (fetched).**
Users report gaps on the X2D. One calls the dynamic flow calibration result "partial". No Bambu staff reply.

**Bambu Studio source (source code).** Three flow numbers multiply together on the first layer:

1. filament_flow_ratio (filament, 0.98) is folded into every extrusion ([Extruder.cpp L18](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Extruder.cpp#L18)).
2. print_flow_ratio (per object, 1.0) multiplies each path ([GCode.cpp L7192](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7192)).
3. initial_layer_flow_ratio (per object, 1.0) multiplies again on the first layer only, except top-solid lines ([GCode.cpp L7194–L7196](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7194)).

The tooltips, from [PrintConfig.cpp on master](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp):

- filament_flow_ratio: "Recommended value range is between 0.95 and 1.05. Maybe you can tune this value to get nice flat surface when there has slight overflow or underflow."
- initial_layer_flow_ratio: "This factor affects the amount of material for the initial layer". Range 0–2. It is a Develop-mode option (hidden in normal mode).
- print_flow_ratio: "The flow ratio set by object, the meaning is the same as flow ratio." Also Develop-mode.

Bambu's own flow-calibration plate sets print_flow_ratio per object on one bed ([CalibUtils.cpp on master](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/Utils/CalibUtils.cpp)).
That is evidence the per-object flow route works in the slicer.

### What this means for us

Our 0.98 has never been calibrated on the X2D.
Bambu's own text calls 0.98 normal "for PLA filament with X1C" and says 1.00 fixes even gaps.
Transfer conditions: the X2D PLA Basic preset carries the same 0.98, and the claim is about the filament.
It transfers if the X2D hotend and extruder deliver the same flow as the X1C at 0.98.
They are different machines, so that is unverified.

A first-layer-only flow boost (initial_layer_flow_ratio) leaves layers 2 and up alone.
That makes it a cleaner test than changing the filament flow.

---

## 3. Squash: first-layer height, Z offset and bed leveling

### What the sources say

**Our own print (not a source, already known).** The textured plate starts 0.02 mm lower and gave fewer slits.

**Bambu wiki, "Troubleshooting printing issues" (fetched).**
"The Textured PEI Plate also has a different Z offset which impacts how close the nozzle is to the print surface for the first layer to be printed."
It recommends a bed leveling calibration for first-layer problems, and "to keep the Bed Leveling Calibration option turned on when starting a print".

**Bambu wiki, "Identify and fix first-layer issues" (fetched).**
"If it's barely sticking or appears thin and wavy, the nozzle is too high. If it's squished to the point where it's creating raised edges or dragging the nozzle, it's too low."

**Bambu forum, X2D thread 251550 (fetched).**
One user lowered Z by 0.014 mm and says the next print was fine.
Another set the first-layer offset to −0.02 mm and says it "helped some".
No Bambu staff reply. Two users, no controls.

**Bambu forum, "X2D print quality issues" thread, post 97 (fetched).**
A user set Z to −0.02 mm but doubts that was the cause. The same user prints PLA Basic at flow 0.98.

**Bambu forum, H2S thread 248800 (fetched).**
A high-temperature bed leveling plus recalibrating before every print helped one user and not another.

**Ellis' print tuning guide, "First layer squish" (fetched).**
Gaps between first-layer lines mean too little squish.
It suggests a first layer of at least 0.25 mm and a first-layer line width of at least 120%, adjusted in 0.01 mm steps.
Transfer conditions: written for Klipper and Marlin printers with a hand-set Z offset.
The idea (gaps mean the nozzle is too high) carries to any printer. The numbers do not: the X2D sets its own Z by probing.

**Prusa forum threads on first-layer gaps (snippets).**
Gaps usually mean "Live Z" is set too high.
In one thread, more infill overlap fixed gaps at the perimeter where lowering Z did not.

**X2D Z offset in the printer menu (snippet, link not kept).**
A search summary says the X2D has a manual first-layer calibration with a Z offset of up to ±0.05 mm.
Its source page was not recorded, so it is not in the table. Treat it as unconfirmed until someone looks at the printer's menu. The start G-code route (the Textured PEI −0.02 mm line) is confirmed in our own plate's start code.

### Where it is set

Z offset is per plate at best: the start G-code, or the printer menu.
initial_layer_print_height is plate-wide (PrintConfig, [PrintConfig.hpp L1475](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1475)).

---

## 4. Infill-to-wall overlap and the monotonic travel setting

### What the sources say

**Bambu Studio source (source code).**
infill_wall_overlap: "Infill area is enlarged slightly to overlap with wall for better bonding. The percentage value is relative to line width of sparse infill." Default 15%.

monotonic_travel_into_wall is labelled "Monotonic line travel extend".
Its tooltip: "Enable this option to extend the travel distance between lines, improving the adhesion between the monotonic line infill and the walls. (percent to line width)".
It is a Develop-mode option, range 0–200%, default 0.
The X2D's parent process profile (fdm_process_dual_common) sets it to 45%; the H2S and P2S profiles on master do too.

In Fill.cpp on master, the setting is passed on only when the pattern is `ipMonotonicLine` or `ipGlobalMonotonicLine` (the "monotonic line" patterns).
Our stock bottom pattern is "monotonic", a different pattern.
So, read from source and not tested: **the X2D profile ships Bambu's fix for this exact gap at 45%, but it does nothing on our stock bottom pattern.**

**Bambu Studio GitHub issue #9768 (fetched, open).**
Users on the H2C report gaps between monotonic first and top lines and the wall.
A Bambu contributor (Diatom-Bambu, 2026-02-27): "We are indeed aware of the issue… We will include some mitigation measures in the next Bambustudio release to improve the integration of monotronic lines with the wall."
The same contributor (2026-04-27) calls the feature a "non-extrude travel… intended for applying material".
User reports in the thread:

- ingoingo: overlap does not apply to the monotonic-line pattern; 55% overlap with plain monotonic "almost" removes the holes. I did not check the first claim in source. If true, overlap and travel-into-wall do not stack.
- bulbabam: a first-layer line width of 0.35 mm helped. This conflicts with our own 0.42 mm result, which made no difference.
- krwc: travel-into-wall at 200% smears the line rather than filling the gap.

**Simplify3D, "Gaps between infill and outline" (fetched).**
Raise the outline overlap, for example from 20% to 30%. Slow the print speed by 50%.
Transfer conditions: the overlap idea is the same in any slicer (push the infill edge into the wall). The 20% → 30% numbers are Simplify3D's scale, not Bambu's.

**Bambu forum, "Filling the gap between outer wall and archimedean infill" (snippet).**
Gap fill closed a wall-to-infill gap for one user but left a bump in the middle.

**Bambu forum, "First/top layer gaps on H2 series: confirmed bug, still unresolved" (snippet, title only).**
The title suggests the same gap is a known slicer problem on newer Bambu printers. Not read.

### What this means for us

Our own print showed 30% overlap closes the strap-edge slits when used with rings.
With the stock diagonal pattern, raising overlap to 30–55% is untested here; one user says 55% "almost" works.
Switching the bottom to the monotonic-line pattern would switch on the 45% travel that is already in the profile.

### Where it is set

Both are per-object settings (PrintRegionConfig, [PrintConfig.hpp L1075 and L1110](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1075)).
Our earlier print measured infill_wall_overlap and bottom_surface_pattern taking effect per piece ([bedface-1 research](2026-10-10-bed-face-per-piece-and-bedface-1.md)).

---

## 5. First-layer speed

### What the sources say

**Bambu wiki, "Identify and fix first-layer issues" (fetched).**
"Reduce the printing speed for the first layer… you can set the outer wall speed to 30 mm/s and the infill speed to 60 mm/s."
"Slower speeds also give the material more time to bond properly."

**Bambu Studio profiles (source code).**
The common dual-nozzle process sets 30 and 60 mm/s.
The X2D 0.20 mm Standard profile overrides them to 50 and 105 mm/s.
So the X2D ships a first layer almost twice as fast as Bambu's own wiki advice.
Hedge: Bambu may have tuned 50/105 for the X2D on purpose; no source says why.

**Simplify3D (fetched).** Slow by 50% for infill-to-outline gaps.

**Bambu forum, "Filling the gap between outer wall and archimedean infill" thread (snippet).** For first-layer-only gaps, "slow it down and see what happens".

### Where it is set

Plate-wide only (PrintConfig, [PrintConfig.hpp L1476–L1478](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1476)).

---

## 6. First-layer nozzle temperature

### What the sources say

**Bambu wiki, "Troubleshooting printing issues" (fetched).**
"the PLA filament temperature configured in Bambu Studio is 220C which should work best for the default print speed settings in the profile."
For Silent mode at 50% speed, 210 °C, because slower printing "doesn't require as much heat for efficient extrusion".
The reverse is implied, not stated: faster needs hotter.

**Bambu wiki, "PLA" (fetched).** For clear prints, raise the temperature along with the flow.

**Bambu PLA Basic data sheet (snippet).** Nozzle range 190–230 °C. So 225–230 °C stays inside Bambu's range.

**Flashforge PLA guide (snippet).** The first layer is often run about 5 °C hotter than later layers, with the fan off or low. This is general advice about sticking to the bed, not about gaps at walls.

**Bambu forum, H2S thread 248800 (fetched).** Changing temperatures did not fix one user's gaps.

### What this means for us

This is the weakest evidence of the six.
No source here ties a hotter first layer to closing gaps at walls.

### Where it is set

Plate-wide (PrintConfig, [PrintConfig.hpp L1479](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1479)), and in practice per filament.
Two filament slots with different first-layer temperatures might give two temperatures on one bed.
But the X2D's two nozzles differ (left is direct drive, right is Bowden, per snippets), so that would test two things at once.

---

## 7. Bed temperature

**Bambu wiki, "PLA" (fetched).** The default bed is 55 °C; it can be lowered 5–10 °C in hot seasons.
**Bambu PLA Basic data sheet (snippet).** Bed 35–45 °C, named for the Cool Plate, High Temperature Plate or Textured PEI Plate.
No source here ties bed temperature to gaps between lines. Plate-wide (PrintConfig, [PrintConfig.hpp L1431](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1431)).

---

## 8. Other settings sources name

**Elephant-foot compensation (Bambu wiki, fetched).**
It shrinks the first-layer outline to offset the flare from bed heat and the weight of later layers.
"The elephant foot compensation value can vary between different types of build plates."
It moves the walls and the infill edge inward together, so it should not change the gap between them (inference).
It matters here as a risk, not a fix: more first-layer squash or flow makes the flare bigger and tightens loose-piece fits.
Per object (PrintObjectConfig, [PrintConfig.hpp L947](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L947)).

**First-layer line width.** Plate-wide in 02.08.02.61 (PrintConfig, [L1474](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1474)). Our print measured the same. Master has a new initial_layer_infill_line_width that this version lacks.

**First-layer cooling.** close_fan_the_first_x_layers is 1, so the fan is already off for the first layer. Plate-wide. No source here suggests changing it.

**Ensure vertical shell thickness.** Already on. Per object. No source here ties it to first-layer gaps.

**Bed leveling and plate flatness.** Bambu's wiki says to run bed leveling first (section 3). This is a printer action before the print, not a slicer setting.

---

## 9. Which settings can vary per piece

The answer comes from which class each setting lives in, in [PrintConfig.hpp at v02.08.02.61](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp).
Object and region classes can be set per object, part or modifier. Print and G-code classes cannot.
The same reading correctly predicted our measured result for first-layer line width (plate-wide) and for overlap and pattern (per piece).
The Bambu wiki ("How to set slicing parameters", fetched) agrees in general: "the value from the smallest level will be used"; filament presets hold "print temperature, hotbed temperature, and flow ratio".

| Setting | Per piece? | Class |
|---|---|---|
| initial_layer_flow_ratio | yes (inferred, Develop-mode) | region |
| print_flow_ratio | yes (inferred, Develop-mode) | region |
| infill_wall_overlap | yes (measured in our print) | region |
| bottom_surface_pattern | yes (measured in our print) | region |
| monotonic_travel_into_wall | yes (inferred, Develop-mode) | region |
| ensure_vertical_shell_thickness | yes (inferred) | region |
| elefant_foot_compensation | yes (inferred) | object |
| wall and infill line widths | yes (inferred) | region |
| initial_layer_line_width | no (measured in our print) | print |
| initial_layer_print_height | no | print |
| initial_layer_speed, initial_layer_infill_speed | no | print |
| nozzle_temperature_initial_layer | no (per filament) | print |
| hot_plate_temp_initial_layer | no | print |
| close_fan_the_first_x_layers | no | print |
| filament_flow_ratio | no (per filament) | G-code |
| pressure advance and K | no (per filament slot on the printer) | G-code / printer |
| Z offset | no (start G-code or printer menu) | machine |

One open point for the first test slice: the three Develop-mode keys.
GCode.cpp applies each region's settings before printing its paths ([L6470](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L6470)).
But whether a Develop-mode key written into model_settings.config is honoured when the app is in normal mode is untested here.
The first slice should check that the extrusion (E) values differ between pieces.

---

## Sources

| Link | What it supports | Fetched or snippet |
|---|---|---|
| [Bambu wiki: Troubleshooting printing issues](https://wiki.bambulab.com/en/knowledge-sharing/troubleshooting-printing-issues) | High K causes lines not touching walls; 0.98 normal on X1C, 1.00 fixes gaps; 220 °C for default speed; textured plate Z offset; bed leveling | fetched |
| [Bambu wiki: Flow Dynamics Calibration](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa) | X2D-family eddy-sensor calibration; Auto/On/Off; auto K higher than manual on purpose; manual K used only when Off | fetched |
| [Bambu wiki: Flow rate calibration](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate) | Not every defect is flow; manual flow steps; judged on the top surface | fetched |
| [Bambu wiki: First-layer test print](https://wiki.bambulab.com/en/knowledge-sharing/identify-and-fix-first-layer-issues-with-a-test-print) | First layer 30/60 mm/s; good layer has no gaps; level the bed first | fetched |
| [Bambu wiki: Elephant foot](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot) | Shrinks the first-layer outline; varies by plate | fetched |
| [Bambu wiki: PLA](https://wiki.bambulab.com/en/filament/pla) | More flow fills tiny gaps (for clear prints); bed 55 °C default | fetched |
| [Bambu wiki: How to set slicing parameters](https://wiki.bambulab.com/en/software/bambu-studio/how-to-set-slicing-parameters) | Global, object, part, modifier levels; filament holds temperatures and flow | fetched |
| [Bambu wiki: Parameter table](https://wiki.bambulab.com/en/software/bambu-studio/parameter-table) | Per-object editing beyond the table columns | fetched |
| [Bambu Studio PrintConfig.hpp at v02.08.02.61](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp) | Which class (per piece or plate-wide) each setting is in | source code |
| [Bambu Studio GCode.cpp at v02.08.02.61, L7192](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7192) | How the per-object and first-layer flow factors multiply | source code |
| [Bambu Studio Extruder.cpp at v02.08.02.61, L18](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Extruder.cpp#L18) | Filament flow ratio applies to every extrusion | source code |
| [Bambu Studio PrintConfig.cpp on master](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp) | Tooltips: PA "Useless for Bambu Printer"; flow ranges; travel-into-wall wording | source code |
| [Bambu Studio Fill.cpp on master](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/Fill/Fill.cpp) | Travel-into-wall applies only to the monotonic-line patterns | source code |
| [Bambu Studio CalibUtils.cpp on master](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/Utils/CalibUtils.cpp) | Bambu's flow calibration plate varies print_flow_ratio per object | source code |
| [Bambu Studio X2D process profile at v02.08.02.61](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process) | X2D first layer 50/105 mm/s; parent sets travel-into-wall 45%, EFC 0.15 | source code |
| [Bambu Studio issue #9768: Gaps in prints](https://github.com/bambulab/BambuStudio/issues/9768) | Bambu aware of monotonic-to-wall gaps; user reports on overlap 55%, line width 0.35, travel 200% | fetched |
| [Bambu forum: Auto flow dynamics deep dive](https://forum.bambulab.com/t/community-tech-talk-deep-dive-into-auto-flow-dynamics-calibration/225453) | Auto calibration sets PA, not flow ratio | fetched |
| [Bambu forum: X2D PLA flow rate thread](https://forum.bambulab.com/t/x2d-pla-print-flow-rate-isnt-isnt-fine-or-some-other-issue/251550) | X2D users: Z −0.014 and −0.02 helped some; calibration "partial" | fetched |
| [Bambu forum: X2D print quality issues, post 97](https://forum.bambulab.com/t/x2d-print-quality-issues/253016/97) | X2D user at Z −0.02 and flow 0.98, unsure of cause | fetched |
| [Bambu forum: H2S first layer not squished enough](https://forum.bambulab.com/t/first-layer-is-not-squished-enough-visible-gaps-h2s/248800) | Flow helps only at obvious over-extrusion; temperature did not help; leveling mixed | fetched |
| [Ellis: First layer squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html) | Gaps mean too little squish (Klipper/Marlin numbers) | fetched |
| [Simplify3D: Gaps between infill and outline](https://www.simplify3d.com/resources/print-quality-troubleshooting/gaps-between-infill-and-outline/) | Raise outline overlap; slow down 50% | fetched |
| [Bambu forum: H2 series first/top layer gaps bug](https://forum.bambulab.com/t/first-top-layer-gaps-on-h2-series-confirmed-bug-still-unresolved/256312) | Title only: a known gap problem on newer printers | snippet |
| [Bambu forum: gap between wall and archimedean infill](https://forum.bambulab.com/t/filling-the-gap-between-outer-wall-and-archimedean-infill/86402) | Gap fill closes a wall gap but adds a bump; slow down for first-layer gaps | snippet |
| [Prusa forum: gaps in first layer](https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-assembly-and-first-prints-troubleshooting/gaps-in-first-layer) | Gaps mean Live Z too high | snippet |
| [Prusa forum: dot gaps in first layer at walls](https://forum.prusa3d.com/forum/how-do-i-print-this-printing-help/dot-gaps-in-first-layer-at-walls) | Overlap fixed perimeter gaps where Z did not | snippet |
| [All3DP: Bambu Lab X2D](https://all3dp.com/4/bambu-lab-x2d/) | X2D dual nozzle, dynamic flow calibration before each print | snippet |
| [3D Printing Industry: X2D launch](https://3dprintingindustry.com/news/bambu-lab-launches-x2d-dual-nozzle-3d-printer-targeting-reduced-post-processing-and-material-waste-251005/) | X2D left direct drive, right Bowden | snippet |
| [3DJake: Bambu Lab X2D](https://www.3djake.com/bambu-lab/x2d) | Calibration may cover only the direct-drive nozzle | snippet |
| [Additive-X: Bambu PLA Basic data sheet](https://www.additive-x.com/shop/mpattachments/file/viewonline/id/494/product_id/2236) | Nozzle 190–230 °C; bed 35–45 °C | snippet |
| [Flashforge: PLA melting point](https://www.flashforge.com/blogs/news/pla-melting-point) | First layer often about 5 °C hotter | snippet |

Repo context, not outside sources: [bed-face slits research](2026-10-10-bed-face-slits.md), [bedface-1 per-piece research](2026-10-10-bed-face-per-piece-and-bedface-1.md), [print quality design](../design/printing/print-quality-design.md) (which first quoted the 0.98-on-X1C line).
