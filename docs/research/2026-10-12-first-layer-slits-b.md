---
date: 2026-10-12
produced-by: Claude (research pass B of two, for the bed-face slits; independent of pass A)
feeds:
  - docs/issues/bed-face-preset-failed-in-print.md
---

# First-layer slits on the X2D: what the sources say, setting by setting

This is research pass B. It was written without reading pass A.

The question comes from [the bed-face issue](../issues/bed-face-preset-failed-in-print.md). Two
kinds of slit show on the bed side of an openwork coaster printed on the X2D:

- **Edge slits (stock first layer).** Thin slits run along the strap edges. They sit where the
  diagonal first-layer lines turn back short of the wall.
- **Meeting dashes (rings first layer).** Short dashes run down the middle of the 3.75 mm straps.
  They sit where the rings from the two edges meet.

The setup is a 0.4 mm hardened nozzle, Bambu PLA Basic and the "0.20mm Standard @BBL X2D"
process. What our own prints already showed is not re-researched here (see the issue).

## How to read the marks

Each claim carries one of three marks.

- **Fetched.** I downloaded the page and read the passage myself.
- **Snippet.** I only saw the claim in a search-result summary. It is not confirmed.
- **Source read.** I read the Bambu Studio code on GitHub at commit
  [47a13eeb](https://github.com/bambulab/BambuStudio/tree/47a13eeb1d9af65ef2371e361c856e21d4f6ca72)
  (master, 2026-10-08), or the profiles installed with Bambu Studio 02.08.02.61 on this Mac. I did
  not slice anything to test what I read. The installed app is older than that commit, so a code
  path could differ between them. The X2D start G-code is the same in both.

Forum posts are one person's report. A post that says "this fixed it" is one print on one
printer, not a test.

## The headline: the stock profile's "travel into wall" is switched off by its own pattern

This is the main new finding. It comes from reading the code, not from a print.

- The X2D process inherits a setting called "Monotonic line travel extend"
  (`monotonic_travel_into_wall`), set to 45% (source read, the dual-nozzle common process
  profile).
- The stock first-layer pattern is `monotonic` (source read, the common process profile). Our own
  slice of the stock preset read the same value back (see
  [the 2026-10-10 slice notes](2026-10-10-bed-face-slits.md#the-variants)).
- The slicer only passes the travel-into-wall value on when the pattern is `monotonicline` or the
  global monotonic line pattern (source read,
  [Fill.cpp L262-276](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/Fill/Fill.cpp#L262-L276)).
  With plain `monotonic`, the 45% does nothing.
- Bambu's wiki says the same thing in plain words (fetched,
  [Strength advanced settings](https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings)).
  The setting "only works if your Top surface pattern or Bottom surface pattern is set to
  Monotonic Line". When it works, "the nozzle keeps moving straight for a tiny bit longer (into
  the inner wall) before making its turn. This can help create a cleaner, smoother surface
  finish." The wiki gives the value as a share of the inner wall's thickness. It says the setting
  is shown only in Developer Mode.

What the code does with it (source read,
[Fill.cpp L687-689](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/Fill/Fill.cpp#L687-L689)
and
[ExtrusionEntity.hpp L671-710](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/ExtrusionEntity.hpp#L671-L710)):

- In the monotonic line pattern, the hop from one line to the next is a move with no
  extrusion.
- That hop is only made when the next line starts within three line widths.
- With the setting above zero, the hop first carries on along the last line's direction, by the
  line width times the setting, before it turns. So the line's end is pushed toward the wall.

Why this matters here:

- The edge slits are exactly lines that turn short of the wall. This setting is the one
  Bambu ships for that.
- It is already in the profile, but the profile's own pattern switches it off.
- Switching the pattern to `monotonicline` turns it on with no other change.
- Our plate tool already accepts `monotonicline` as a per-piece setting (`tools/bambu/src/commands/compose.ts`).
  So it costs nothing new to test.

Hedges that must travel with this:

- **It did not help one H2 user.** The poster of the H2 first-layer gaps thread said "Monotonic
  line travel extend" did not help them (fetched,
  [forum 256312](https://forum.bambulab.com/t/first-top-layer-gaps-on-h2-series-confirmed-bug-still-unresolved/256312)).
  That is one user on a different machine.
- **A suspected bug sits in this exact move.** A September 29 comment on
  [GitHub issue 9768](https://github.com/bambulab/BambuStudio/issues/9768) (fetched) proposes that
  the no-extrusion hops are counted as covered area. If so, the gap filler skips the voids beside
  them. This is a user's reading of the code. Bambu has not confirmed it.
- **It addresses the edge slits only.** It does nothing for the rings' meeting dashes. Those
  come from the rings pattern itself, which has no wall-ward line ends to extend.
- **Developer Mode is untested for files.** The wiki says the setting is shown only in Developer
  Mode. I did not check whether a value written into the project file is honored without it.
  The pattern switch alone does not need it, since the 45% is already in the profile.
- **Plain `monotonic` joins lines in a way I did not read.** I did not trace how plain
  `monotonic` links its lines at the wall. The claim that it "turns short" comes from our
  pictures, not from the code.

## The X2D-specific evidence

Two kinds of report bear on this printer family. They should be kept apart.

**Direct X2D report.** The X2D PLA flow thread (fetched,
[forum 251550](https://forum.bambulab.com/t/x2d-pla-print-flow-rate-isnt-isnt-fine-or-some-other-issue/251550))
reports "Small holes on bottom surfaces where the nozzle changes direction". The poster says flow
calibration helps but does not fully fix it. Dynamic flow calibration helps "to some degree".
Replies:

- vladap: "it seems Z axis is to high, I lower it by 0,014 and first print is fine".
- shadow_dio: first-layer calibration at "-.02 helped some".
- lkraus: gaps at direction changes are "incorrect pressure advance".

These are three users with three different causes. None is confirmed.

**H2-series bug.** [GitHub issue 9768](https://github.com/bambulab/BambuStudio/issues/9768)
(fetched) covers gaps on first and top layers and between infill and walls. It was opened
February 14, 2026, and names the H2C, H2D and H2S.

- February 24, Mujin-code wrote "we are currently working on resolving this issue", speaking as
  Bambu. They suggested monotonic lines with more overlap as a workaround.
- February 27, Diatom-Bambu wrote that they were "aware of the issue" and its "complexity". They
  promised mitigations in the next release.
- September 23, user abarylak said the textured plate's −0.02 mm may be too high, and −0.04 to
  −0.05 mm worked better for them.
- The last activity was October 10, 2026. No root cause or fixed version is stated.

The matching forum thread (fetched,
[forum 256312](https://forum.bambulab.com/t/first-top-layer-gaps-on-h2-series-confirmed-bug-still-unresolved/256312))
says a developer confirmed the bug. Bambu support reportedly suggested 20 mm/s for the first
layer and 30 mm/s for first-layer infill. The poster said the result was still worse than an A1.

*Does the H2 bug transfer to the X2D?* Maybe, maybe not. The issue names H2 printers only. The
X2D shares the H2's dual-nozzle common profiles and the same Flow Dynamics method (wiki, fetched,
below). So the same slicer path and printer-side calibration are plausible. But no source here
shows the bug on an X2D. It transfers only if the cause is in the shared slicer code or the
shared calibration, not in H2 hardware.

## Setting by setting

### 1. First-layer nozzle temperature (now 220 °C)

- Stock value: 220 °C on the first layer and after (source read, the X2D PLA Basic filament
  profile).
- **Thinly sourced.** I found no test that raises only the first-layer temperature to close gaps
  between lines.
- A layer-separation guide says a too-cool nozzle makes new plastic "sit on top" rather than fuse,
  and suggests raising it 5 to 10 °C (snippet,
  [siddament](https://siddament.com.au/blogs/filament-guide-au/fix-layer-separation)). That is
  about bonding between layers, not between side-by-side lines on the bed. It transfers only if
  side-by-side lines fail for the same reason, too little heat to flow together. No source here
  shows that.
- A temperature-tower page says too much heat shows as shine, blobs or "zits" (snippet,
  [MakerWorld 2089881](https://makerworld.com/models/2089881)).
- Where to set it: a filament setting (source read, PrintConfig.cpp). It is not per piece.

### 2. Flow ratio (0.98, never calibrated here) and pressure advance

**Flow ratio.**

- Stock: 0.98 in the X2D PLA Basic filament profile and its base (source read).
- Studio's own tooltip: "Recommended value range is between 0.95 and 1.05. Maybe you can tune
  this value to get nice flat surface when there has slight overflow or underflow" (source read,
  PrintConfig.cpp).
- Bambu's flow rate wiki (fetched,
  [calibration_flow_rate](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate)):
  - "Only X1 series support Auto calibration" of flow rate. So the X2D does not calibrate flow
    ratio by itself.
  - The manual test runs 80 to 120% in 5% steps, then 91 to 100% in 1% steps.
  - "Avoid selecting the sample which shows slight signs of under-extrusion. For larger prints,
    this slight under-extrusion can increase, leading to potential gaps between the printed
    lines."
  - It lists "gaps in the print" among signs of under-extrusion. It says to check the nozzle and
    extruder first.
- A Bambu wiki page reportedly calls 0.98 "normal for PLA filament with X1C" and says raising it
  to 1.00 "should solve" top-layer gaps (snippet only,
  [top-layer-inconsistencies](https://wiki.bambulab.com/en/knowledge-sharing/top-layer-inconsistencies);
  the page returned 404 and 402 when fetched). It is about top layers on an X1C. It transfers
  only if the X2D's extruder delivers the same amount per commanded millimetre as the X1C's. No
  source here says so.
- More flow did not close first-layer gaps for one X1C user (fetched,
  [forum 35462](https://forum.bambulab.com/t/optimize-a-almost-perfect-first-layer/35462)):
  - They raised it up to 1.25. "The gaps happen even with some significant overextrusion".
  - "For line width >0.4mm the gaps start to become larger". 0.3 mm lines gave smaller gaps but
    not none.
  - Their best was a Hilbert curve bottom at flow 1.2: "There are still some gaps".
  - They suspected surface tension or the nozzle's shape.
  - It transfers to the X2D only if the cause is the plastic and nozzle, not that printer's Z.
- H2 users report mixed results at 1.0 to 1.05; 1.1 did not help (fetched, forum 256312).
- An H2S user found raising flow did not fix it short of plain over-extrusion (fetched,
  [forum 248800](https://forum.bambulab.com/t/first-layer-is-not-squished-enough-visible-gaps-h2s/248800)).

**First-layer flow and per-piece flow.**

- There is a first-layer-only flow setting, `initial_layer_flow_ratio`, range 0 to 2, default 1.
  Its tooltip: "This factor affects the amount of material for the initial layer" (source read,
  [PrintConfig.hpp L1208](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.hpp#L1208)).
- There is also a per-object flow, `print_flow_ratio`, "Object flow ratio": "The flow ratio set by
  object, the meaning is the same as flow ratio." Default 1 (source read, L1212).
- Both sit in the per-region settings, which can be set per piece. Both are marked
  developer-mode only.
- The G-code writer multiplies each line's flow by `print_flow_ratio`, then by
  `initial_layer_flow_ratio` on the first layer, except top surfaces (source read,
  [GCode.cpp L7225-7229](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/GCode.cpp#L7225-L7229)).
  The region's settings are applied before its lines are written, so a per-piece value should
  apply to that piece.
- **This was read in the code where region settings are applied per region; it was not tested by
  slicing.** Our plate tool does not allow these keys yet. It adds a key only once a slice shows
  Studio honored it.

**Pressure advance and Flow Dynamics.**

- The slicer's own fields are stock `enable_pressure_advance` 0 and `pressure_advance` 0.02. Both
  tooltips say "Useless for Bambu Printer" (source read, PrintConfig.cpp).
- The X2D does run its own calibration, called Flow Dynamics. It sets the pressure advance value,
  called K. It does not set the flow ratio. Bambu's wiki (fetched,
  [calibration_pa](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa)) says:
  - The H2D, H2S, P2S and X2D spit plastic onto the purge wiper and measure it with a sensor.
  - "Auto" re-calibrates only when the filament, nozzle or hotend changed. "On" calibrates
    before every print. "Off" uses the saved or default K.
  - "During acceleration, this lag can cause underextrusion, resulting in gaps or thin lines."
  - "The calibration results have about 10% jitter in our test."
  - "To prevent corner stacking effects, the Factor K during H2D automatic flow calibration will
    be set higher than in pattern mode of manual calibration."
- The X2D start G-code runs this calibration (`M983.3`) when the send dialog's switch asks for it
  (source read, the installed X2D start G-code template).
- Bambu staff say it "calibrates... to establish precise parameters for Pressure Advance" during
  print preparation (fetched,
  [forum 225453](https://forum.bambulab.com/t/community-tech-talk-deep-dive-into-auto-flow-dynamics-calibration/225453)).
- An H2S user said high-temperature bed levelling plus re-calibrating before each print "solved
  the issue" for them (fetched, forum 248800). Others in that thread had a bent wiper plate or no
  fix.
- K can explain gaps where the nozzle changes direction (lkraus in forum 251550, above). It
  should not explain a straight gap along a wall. That second point is my inference, not a
  source's.

### 3. First-layer speed (50 mm/s walls, 105 mm/s first-layer infill)

- Stock: `initial_layer_speed` 50, `initial_layer_infill_speed` 105, first-layer acceleration
  500 (source read, the X2D process profile). The second is the "Speed of solid infill part of
  initial layer" (source read, PrintConfig.cpp). That is the diagonal fill that leaves the edge
  slits.
- Simplify3D (fetched,
  [gaps between infill and outline](https://www.simplify3d.com/resources/print-quality-troubleshooting/gaps-between-infill-and-outline/)):
  "If the infill is printed too fast, it will not have enough time to bond to the outline
  perimeters". It suggests trying 50% slower. This is general advice for any printer. It
  transfers if the gap is from speed, which a slower test shows directly.
- Bambu support reportedly told an H2 user 20 mm/s first layer and 30 mm/s first-layer infill
  (fetched, forum 256312). The user said it was still worse than an A1. That is second-hand,
  through the poster.
- Where to set it: plate-wide (source read, PrintConfig.hpp, the plate-wide class). Not per
  piece.

### 4. Bed temperature, first-layer height and how high the nozzle starts

**Bed temperature.**

- Stock: 55 °C on the first layer for the smooth (hot) plate, the textured plate and the
  engineering plate with this filament (source read, fdm_filament_pla and the X2D PLA Basic
  profile). I did not check the cool plate or other plate types. The glacier plate is sliced as
  the smooth plate here.
- The glacier plate's maker reportedly gives PLA 45 to 55 °C (snippet,
  [BIQU Panda build plate](https://biqu.equipment/collections/all-accessories/products/panda-build-plate)).
- **No source here ties bed temperature to gaps between first-layer lines.** Note that 55 °C
  keeps the X2D on the cooler branch of its start G-code (≤ 70 °C, below). Above 70 °C the trim
  changes.
- Where to set it: filament and plate. Not per piece.

**How high the nozzle starts (the Z trim).** The X2D start G-code sets a small extra offset by
plate type (source read, installed 2.08.02.61 and GitHub master, identical):

| Bed at first layer | Textured PEI plate | Any other plate |
|---|---|---|
| 70 °C or below | +0.002 mm | +0.022 mm |
| above 70 °C | −0.003 mm | +0.017 mm |

The code's comment: "for Textured PEI Plate, lower the nozzle as the nozzle was touching topmost
of the texture when homing". So the textured plate starts 0.020 mm lower *relative to* the other
plates. It is not lowered below the measured surface.

- Our gold textured plate gave fewer slits, which fits this (the issue, our own print).
- Ellis's tuning guide (fetched,
  [first layer squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html)):
  - "If you see gaps between the lines, you need more squish."
  - Step 0.01 mm at a time. It is "generally better to lean on the side of a bit too much squish".
  - Too much squish shows as smooth or wavy lines, "especially on smooth PEI".
  - It transfers because squish is plain geometry on any printer. But on the X2D the lever is
    different. Height comes from the start G-code trim and the printer's own first-layer
    calibration, not a live knob in the slicer.
- The Prusa community view is that gaps between first-layer lines mostly mean the nozzle is too
  high, and raising flow to hide it is a workaround (snippet, from search over Prusa forum threads
  and the [Live adjust Z](https://help.prusa3d.com/article/ZhBlGFD9Ah-live-adjust-z) article).
- A shop blog reportedly says most first-layer gaps come from the nozzle being a little too high
  (snippet,
  [goodprints3d](https://www.goodprints3d.com/blogs/3d/why-do-first-layers-have-gaps-in-3d-printing-and-what-should-you-change-first)).
- X2D users lowered Z by 0.014 mm and 0.02 mm with good or partial results (fetched, forum
  251550). An H2 user found −0.04 to −0.05 mm better on the textured plate (fetched, issue 9768).
- An X2D user mentions a manual first-layer offset on the printer in ±0.05 mm steps (fetched,
  [forum 257448](https://forum.bambulab.com/t/underextrusion-on-the-top-layer-bambu-lab-x2d-warranty/257448);
  second-hand inside that thread). One X2D unit there was replaced under warranty for
  under-extrusion. I did not confirm that menu from Bambu's own pages.
- Where to set it: the slicer's own Z offset is switched off in this build (source read,
  commented out in PrintConfig.hpp). The levers are the plate type, a custom start G-code, or the
  printer's own offset. All of these are per print, not per piece.

**First-layer height.**

- Stock 0.2 mm (source read). Ellis prefers 0.25 mm or more "in my opinion".
- Where to set it: plate-wide (source read). Not per piece. The per-object menu in the code has it
  commented out (source read,
  [GUI_Factories.cpp L78-160](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/slic3r/GUI/GUI_Factories.cpp#L78-L160)).

### 5. Other settings the sources name

**Infill and wall overlap.**

- Stock 15% (source read). The wiki (fetched, Strength advanced settings) says:
  - It enlarges the fill "slightly to overlap with the wall for better bonding", and this covers
    the bottom surface.
  - The share is "relative to the line width of sparse infill". The code measures it against the
    inner wall's width instead (source read, PrintConfig.cpp). Both are 0.45 mm here, so it does
    not matter now.
  - "If the overlap rate is too high, the model's surface will bulge, affecting appearance."
- Simplify3D (fetched) suggests going from 20% to 30%. Its percentage is of its own outline
  width. It transfers in direction, not in number, since the base width differs.
- On the H2 issue, users say more overlap helps the bond. Mujin-code, speaking as Bambu,
  suggested monotonic lines with more overlap (fetched, issue 9768).
- Where to set it: per piece (source read, per-region class). Our plate tool already allows it.

**First-layer line width.**

- Stock 0.5 mm. A 0.42 mm line made no difference for us (the issue).
- The X1C user found wider than 0.4 mm made gaps larger (fetched, forum 35462). Ellis suggests
  120% or more (fetched). They disagree. Ellis is about adhesion; the X1C user measured gaps.
- Where to set it: plate-wide (source read, PrintConfig.hpp L1538). This matches our own slice
  test ([2026-10-10, §1](2026-10-10-bed-face-per-piece-and-bedface-1.md#1-which-of-the-three-settings-bambu-takes-per-piece)).

**Elephant-foot compensation.**

- Stock 0.15 mm (source read, the 0.4 mm dual-nozzle process). Tooltip: "Shrink the initial layer
  on build plate" (source read).
- No source here ties it to slits. It matters for fit. With it at 0, the first layer of each edge
  would sit up to 0.15 mm further out. That is my reading of the tooltip, not a measurement.
- Where to set it: per object (source read, PrintConfig.hpp L982, the per-object class; it is
  also in the per-object menu).

**First-layer cooling.**

- On the first layer the part fan is off (`close_fan_the_first_x_layers` 1). The extra fan runs
  at 40% (`first_x_layer_fan_speed`) (source read, the filament profiles and GCodeEditor.cpp
  L400-460).
- No source here ties first-layer cooling to gaps between lines. It is a filament setting, so not
  per piece.

**Bed levelling.** An H2S user credits high-temperature levelling plus per-print calibration
(fetched, forum 248800). It is a send-dialog choice. It is not per piece.

**Bottom pattern.** See the headline. The rings' meeting dashes are a known cost of rings. The
X1C user found a Hilbert curve best, but still with gaps (fetched, forum 35462).

## Which settings can be set per piece

From the code's config classes (source read,
[PrintConfig.hpp](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.hpp)).
Only the two marked "proven" have been checked by a slice.

| Setting | Where it lives | Per piece? |
|---|---|---|
| `bottom_surface_pattern` | per region | yes, proven by our slice |
| `infill_wall_overlap` | per region | yes, proven by our slice |
| `monotonic_travel_into_wall` | per region | yes in code, not sliced |
| `initial_layer_flow_ratio` | per region, developer mode | yes in code, not sliced |
| `print_flow_ratio` | per region, developer mode | yes in code, not sliced |
| `elefant_foot_compensation` | per object | yes in code, not sliced |
| `initial_layer_line_width` | plate | no, our slice showed it |
| `initial_layer_print_height` | plate | no |
| `initial_layer_speed`, `initial_layer_infill_speed` | plate | no |
| first-layer nozzle temperature | filament | no |
| bed temperature | filament and plate | no |
| `filament_flow_ratio` | filament | no |
| Flow Dynamics, bed levelling | send dialog | no |
| Z trim | start G-code or printer | no |

## Sources

| Link | What it supports | Fetched or snippet |
|---|---|---|
| [Bambu wiki: Strength advanced settings](https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings) | Overlap meaning, bulge risk; travel-into-wall needs Monotonic Line and Developer Mode | Fetched |
| [Bambu wiki: Flow Dynamics calibration](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa) | X2D measures K at the wiper; Auto/On/Off; about 10% jitter; K set higher than manual | Fetched |
| [Bambu wiki: Flow rate calibration](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate) | Only X1 auto-calibrates flow; manual steps; slight under-extrusion leads to gaps | Fetched |
| [Bambu wiki: top layer inconsistencies](https://wiki.bambulab.com/en/knowledge-sharing/top-layer-inconsistencies) | 0.98 normal on X1C, 1.00 "should solve" | Snippet (404/402 on fetch) |
| [GitHub issue 9768](https://github.com/bambulab/BambuStudio/issues/9768) | H2 first-layer gaps bug, workaround, −0.04 to −0.05 mm, hop-area theory | Fetched |
| [Forum 256312](https://forum.bambulab.com/t/first-top-layer-gaps-on-h2-series-confirmed-bug-still-unresolved/256312) | H2 bug confirmed by a developer per the poster; support's slow speeds; travel extend did not help | Fetched |
| [Forum 251550](https://forum.bambulab.com/t/x2d-pla-print-flow-rate-isnt-isnt-fine-or-some-other-issue/251550) | X2D holes at direction changes; Z −0.014 and −0.02 mm; pressure advance theory | Fetched |
| [Forum 248800](https://forum.bambulab.com/t/first-layer-is-not-squished-enough-visible-gaps-h2s/248800) | H2S: hot levelling plus per-print calibration solved it for one user; flow did not | Fetched |
| [Forum 257448](https://forum.bambulab.com/t/underextrusion-on-the-top-layer-bambu-lab-x2d-warranty/257448) | X2D under-extrusion warranty case; manual first-layer offset mentioned | Fetched |
| [Forum 225453](https://forum.bambulab.com/t/community-tech-talk-deep-dive-into-auto-flow-dynamics-calibration/225453) | Flow Dynamics sets pressure advance during print preparation | Fetched |
| [Forum 35462](https://forum.bambulab.com/t/optimize-a-almost-perfect-first-layer/35462) | X1C: gaps survive flow 1.25; wider lines widen gaps; Hilbert best | Fetched |
| [Simplify3D: gaps between infill and outline](https://www.simplify3d.com/resources/print-quality-troubleshooting/gaps-between-infill-and-outline/) | More outline overlap; slower infill | Fetched |
| [Ellis: first layer squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html) | Gaps mean more squish; 0.01 steps; wider first line, taller first layer | Fetched |
| [Prusa: Live adjust Z](https://help.prusa3d.com/article/ZhBlGFD9Ah-live-adjust-z) | Nozzle too high is the usual cause of line gaps (forum view) | Snippet |
| [goodprints3d blog](https://www.goodprints3d.com/blogs/3d/why-do-first-layers-have-gaps-in-3d-printing-and-what-should-you-change-first) | Most first-layer gaps from nozzle slightly too high | Snippet |
| [siddament: layer separation](https://siddament.com.au/blogs/filament-guide-au/fix-layer-separation) | Raise nozzle 5 to 10 °C for bonding between layers | Snippet |
| [MakerWorld 2089881](https://makerworld.com/models/2089881) | Too hot shows as shine, blobs, zits | Snippet |
| [BIQU Panda build plate](https://biqu.equipment/collections/all-accessories/products/panda-build-plate) | Glacier plate PLA bed 45 to 55 °C | Snippet |
| [Fill.cpp at 47a13eeb](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/Fill/Fill.cpp#L262-L276) | Travel into wall only for monotonic line patterns | Source read |
| [ExtrusionEntity.hpp at 47a13eeb](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/ExtrusionEntity.hpp#L671-L710) | The hop between lines and how it is extended | Source read |
| [GCode.cpp at 47a13eeb](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/GCode.cpp#L7225-L7229) | Per-object and first-layer flow multipliers | Source read |
| [PrintConfig.hpp at 47a13eeb](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/libslic3r/PrintConfig.hpp) | Which settings are per object, per region, plate or filament | Source read |
| [GUI_Factories.cpp at 47a13eeb](https://github.com/bambulab/BambuStudio/blob/47a13eeb1d9af65ef2371e361c856e21d4f6ca72/src/slic3r/GUI/GUI_Factories.cpp#L78-L160) | Per-object menu; first-layer height left out | Source read |
| Installed Bambu Studio 02.08.02.61 profiles (X2D process, PLA Basic filament, X2D start G-code) | Stock values; the Z trim table | Source read (local files) |
