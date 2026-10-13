---
date: 2026-10-13
produced-by: research pass A, Claude subagent (one of two independent passes; it did not read pass B)
feeds:
  - docs/design/printing/bed-face-slicing-design.md (the bed-face design)
  - the next bedface plate
---

# What else to try for the slits on the coaster bottoms: the raw findings (pass A)

This file collects what I found on one question. What else can we try to get rid of the short
dark slits along the strap edges on the coaster bottoms? The ranked answer built from it is in
[the pass A recommendation](2026-10-13-bed-face-next-a-recommendation.md).

It builds on [the merged research from 2026-10-12](2026-10-12-first-layer-slits-consolidated.md)
and on [the bedface-4 print](../prints/2026-10-13-bedface-4/index.md). It does not repeat what
those say, except where new evidence changes it (§4).

## 1. The setup and what is already known

- **Printer and slicer:** Bambu Lab X2D, 0.4 mm nozzle, Bambu PLA Basic, 0.20 mm layers, Bambu
  Studio. The profile is "0.20mm Standard @BBL X2D", sliced as a smooth plate (the "glacier"
  plate, bed at 55 °C).
- **The part:** the gBV coaster, a ten-fold rosette
  ([the constructions ledger](../constructions/ledger.md)), 4.4 mm tall, with straps about
  3.75 mm wide.
- **The slits:** on the first layer, the diagonal lines that fill each strap stop short of the
  wall loops. A "wall loop" is a line the slicer lays around the edge of each shape; the lines
  inside it are the "bottom surface infill" (the fill).
- **What bedface-4 showed** (12 pieces of the coaster, judged by hand on 2026-10-13):
  - Pushing the fill 55% into the wall left fewer slits than 30%, with no ridge. Piece `2` was the
    cleanest of the twelve photos.
  - 10% more plastic on the first layer helped a little, against what the research expected.
    Every flow piece still slit.
  - The `monotonicline` bottom pattern only moved the slits.
  - In both overlap pairs, the piece the bed arranger turned a quarter turn did better (`P` over
    `L`, `2` over `T`). Two pairs are too few to call it.
- **Dropped before this pass:** ring-shaped (concentric) bottoms, which left dashes where rings
  meet; the gold textured plate, for its grain; a narrower 0.42 mm first line, which made no
  difference in print.

Stock values that matter below, read from the project settings inside the sheets-04g-fit2 stock
slice (Bambu Studio 02.08.02.61):

| Setting | What it does | Stock value |
|---|---|---|
| `infill_direction` | the angle of the fill lines on the bed | 45° |
| `is_infill_first` | lay the fill before the walls | off |
| `wall_sequence` | which wall loop goes down first | inner, then outer |
| `wall_loops`, `wall_generator` | how many wall loops, and how they are drawn | 2, classic |
| `only_one_wall_first_layer` | one loop only on the first layer | off |
| `filter_out_gap_fill` | drop gap-fill lines shorter than this | 0 (keep all) |
| `gap_infill_speed` | speed for the thin "gap fill" lines | 250 mm/s |
| `elefant_foot_compensation` | shrink the first layer's outline to offset squash | 0.15 mm |
| `initial_layer_acceleration`, `initial_layer_jerk` | how fast the nozzle may speed up on layer 1 | 500 mm/s², 9 |
| first-layer speed, first-layer fill speed | | 50 mm/s, 105 mm/s |
| `monotonic_travel_into_wall` | see §3.4 | 45% |
| `initial_layer_line_width` | | 0.5 mm |

## 2. Which settings can be set per piece

A setting can differ from piece to piece on one plate only if Bambu Studio keeps it per object.
In the code, those are the two "per object" and "per region" groups in
[PrintConfig.hpp](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L946)
(from L946 and from L1062). The whole-plate groups start at L1219. All code links in this file are
at the tag v02.08.02.61, the version our slices were made with.

| Setting | Per piece in the code? | Line |
|---|---|---|
| `infill_wall_overlap`, `bottom_surface_pattern`, `infill_direction`, `wall_loops`, `wall_sequence`, `initial_layer_flow_ratio`, `monotonic_travel_into_wall` | yes (per region) | [L1062-L1170](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1062) |
| `wall_generator`, `only_one_wall_first_layer`, `elefant_foot_compensation` | yes (per object) | [L946-L1044](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L946) |
| `is_infill_first`, first-layer speeds, acceleration, jerk, line width, nozzle temperature | no, whole plate | [L1219 on](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1219) |

"Per piece in the code" is not the same as per piece in our tools. Our compose tool
([compose.ts](../../tools/bambu/src/commands/compose.ts)) accepts only three keys today:
`bottom_surface_pattern` (monotonic, monotonicline, concentric), `infill_wall_overlap` (up to
100%), and `initial_layer_flow_ratio`. Each was added after a slice showed Studio honored it. Any
other key needs the same proof first: the key shows on that piece's settings in the 3mf that is
sent, and not on the stock piece.

## 3. What the code says

These are my readings of the Bambu Studio source at the tag. They are not tested in a slice or a
print unless I say so.

### 3.1 "Lay the fill first" does nothing on the first layer

[GCode.cpp L5465-5467](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L5465):
"for first layer, we always print wall firstly to get better bed adhesive force". The branch that
lays the fill first runs only `if (is_infill_first && !first_layer)`. The second copy of that
branch, at [L5762](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L5762),
has the same test. So `is_infill_first` cannot change the first layer. It is ruled out.

### 3.2 Gap fill on the first layer is already slow

[GCode.cpp L7291](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7291)
sets gap-fill speed to `gap_infill_speed` (250 mm/s). But
[L7334-7338](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7334)
then overrides every first-layer line except the bottom fill with the first-layer speed (50 mm/s).
The bottom fill itself gets the first-layer fill speed (105 mm/s,
[L7283](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7283)).
So gap-fill speed is not a first-layer lead. `filter_out_gap_fill` is already 0, so no gap fill
is dropped either.

### 3.3 When two fill lines get joined along the wall

On a solid fill (density above 80%), the slicer joins the end of one fill line to the start of the
next by a short run along the wall, but only if that run is no longer than three line spacings:
[Fill.cpp L697-698](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/Fill.cpp#L697),
`link_max_length = 3. * f->spacing`. The fill code then marks longer runs "as too long"
([FillRectilinear.cpp L2903-2904](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/FillRectilinear.cpp#L2903),
measured at [L1253-1263](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/FillRectilinear.cpp#L1253)).

My inference, not tested: where the fill lines meet a wall at an angle θ, the run along the wall
between two line ends is about one spacing divided by sin θ. That is three spacings or less only
when θ is about 19.5° or more. So along a strap edge that runs within about 19.5° of the fill
direction, the line ends would not be joined. They stop and start on their own, and a line that
stops on its own is where a slit is most likely.

The fill angle comes from `infill_direction`
([Fill.cpp L252](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/Fill.cpp#L252)),
which is a per-piece setting.

Transfer condition: this rule acts per strap direction, not per piece. A ten-fold rosette's strap
edges usually run in ten directions 18° apart. I did not measure this coaster's. If they do, then
for any fill angle, two or three of the ten directions sit within 19.5° of the fill. Setting the
fill halfway between two strap directions gives two, the best case. Setting it along one gives
three. So the fill angle can at best move one strap direction out of ten past the limit on the
whole coaster. It cannot remove the effect. A test piece holds only some of the straps, so a piece
tested at one angle may not stand for the whole coaster on this one effect.

What bedface-4 shows about it: the plate page reads a quarter turn as mapping the straps onto
straps at the same angles ([bedface-4](../design/plates/bedface-4.md)). Ten directions 18° apart
do map onto themselves under a quarter turn (90° is five steps of 18°). The slice agreed for the
stock pair (`H` 356 slits planned, `J` 350). But it did not for the overlap pairs: `P` 273 against
`L` 306, and `2` 101 against `T` 159. So the turn did change the planned fill in those pieces,
perhaps through where the piece's cut edges and rim sit against the fill. I did not look into why.

One more pointer: in the photos, the slits on `T`, `W` and `Y` sit mostly "on the left" straps
([the print record](../prints/2026-10-13-bedface-4/index.md)). Slits that sit on straps of one
direction would fit the joining rule. Slits that sit on one side of the bed would fit a bed or
height cause instead, like the H2S case in §5.3. Nobody has sorted the photos by strap direction
yet.

### 3.4 The monotonic-line pattern and its "travel extend"

The merged research from 2026-10-12 already covers this, and bedface-4 dropped the pattern. One
addition: the profile that gives the X2D its 45% value is the dual-nozzle common profile
(`"monotonic_travel_into_wall": "45.0"`), while the base common profile sets 0. The setting is
hidden unless the slicer is in Develop mode
([PrintConfig.cpp L2109-2118](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.cpp#L2109),
`def->mode = comDevelop`). On an H2D, one user says the 45% "caused my H2D to print the top infill
over the edge of the print on round corners" ([forum 198663](https://forum.bambulab.com/t/please-add-percentage-setting-for-overlap-of-top-layer-walls/198663),
user_4199167829, 2026-04-28, fetched). That is a top surface, on an H2D.

### 3.5 How far the overlap reaches, in millimeters

The tooltip says the overlap is a percent "relative to line width of sparse infill"
([PrintConfig.cpp L3956](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.cpp#L3956)).
The code uses a different base:
[PerimeterGenerator.cpp L1400](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PerimeterGenerator.cpp#L1400)
takes the percent of half the wall spacing plus half the solid-fill spacing. The setting has no
upper limit in the code; our compose tool caps it at 100%. That code has no test for the layer, so
the overlap applies to every layer of the piece, the top face included, not only the first.

My estimate, not measured: with every first-layer line 0.5 mm wide and 0.2 mm tall, the spacing is
about 0.46 mm, and the base is about the same. So each step reaches about this far into the wall:

| Overlap | Reach into the wall (about) |
|---|---|
| 15% (stock) | 0.07 mm |
| 30% | 0.14 mm |
| 55% | 0.25 mm |
| 75% | 0.34 mm |
| 100% | 0.46 mm, one full line |

### 3.6 Elephant-foot compensation shrinks walls and fill together

[PrintObjectSlice.cpp L1228-1268](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintObjectSlice.cpp#L1228)
shrinks the first layer's outline (0.15 mm per side here) before any wall or fill is planned. My
inference: walls and fill both follow the smaller outline, so this should not open or close the
gap between them. Changing it moves the bottom edge, which puts the fits of loose pieces at risk.
Not a lead.

### 3.7 Two walls first, then fill, on narrow straps

The first-layer line is 0.5 mm wide. Two wall loops on each side of a 3.75 mm strap take about
1.8 mm, so about 1.9 mm is left for the fill: four or five diagonal lines, each with two ends on a
wall. My estimate. More walls leave fewer fill lines and fewer ends, which is the idea behind the
"more walls" leads in §5.

## 4. Where the new evidence changes the merged research from 2026-10-12

| The merged research said | What changed | Source |
|---|---|---|
| Overlap 30% is the top bet; 55% risks a ridge | bedface-4: 55% beat 30%, with no ridge. That opens 75% and 100%. Outside support for going past 50% exists but is weak (§5.1) | [bedface-4 print record](../prints/2026-10-13-bedface-4/index.md) |
| First-layer flow: "expect little" | It helped a little in print (1.10 fewer than 1.05, 1.05 a bit fewer than stock). Still not a fix alone | same |
| Slower first layer is the second whole-plate step | Two more users slowed down with no fix; one says it "made it worse" (§5.5) | forums 256070, 67327 |
| A lower first layer has the strongest support | One more user, on a Prusa: lowering Z had "some positive effect but did not fully close the gaps" and roughed the top of the first layer (§5.4) | Prusa forum |
| One piece stands for the whole coaster (its §4 assumption) | Holds for the stock pair. For the overlap pairs, the turned piece did better in print and in the slice. If the fill angle matters (§3.3), a piece tested at one angle may not stand for the coaster on that effect | §3.3 |
| Did not list "lay fill first" | Ruled out: the code always lays walls first on layer 1 | §3.1 |

## 5. What outside sources say, by lead

"Fetched" means I opened the page and read it. "Snippet only" means I saw it only in a search
result. None of the sources below is an X2D, unless I say so.

### 5.1 Push the fill further into the wall (overlap above 55%)

- **Prusa forum, "low density on first layer"** (fetched). MK3S+, PrusaSlicer, Prusament PLA, gaps
  between fill and walls on the first layer only. The poster's only workaround was overlap at
  "50%+", which he disliked because it changed other layers. He settled on 25% plus a lower Z plus
  a pattern change: "somewhat satisfying results. However, still not at the quality of my prints
  from last year" (MSt, 2023-07-09).
  <https://forum.prusa3d.com/forum/prusaslicer/low-density-on-first-layer/>
  Transfer: the gap is the same kind (fill stops short of the wall, first layer only). The slicer
  is PrusaSlicer, the family Bambu Studio comes from, but its overlap base may differ.
- **Bambu forum 86402** (fetched). Bambu Studio, Archimedean fill at 100%, gap between wall and
  fill. Raising "Infill/Wall Overlap" to 75% closed the outer gap "in the preview"
  (user_3794745147, 2025-05-09). No print reported.
  <https://forum.bambulab.com/t/filling-the-gap-between-outer-wall-and-archimedean-infill/86402>
  Transfer: same slicer; a preview only, and our own prints show the plan is not the print.
- **Bambu forum 146050** (fetched). A1, holes in the first layer. One reply suggested "100%
  infill/wall overlap" among other changes (Sigama_Crafts, 2025-02-16). No outcome reported.
  <https://forum.bambulab.com/t/holes-in-first-layer/146050>
- **Bambu forum 216407** (fetched). H2S, a 260 by 260 mm single-layer test: the fill "is not fully
  reaching the perimeter" along the front edge only. Overlap at 50%: "the issue is still there"
  (wirlybird, 2025-12-15). A reply read it as "the Z height is changing". No fix found.
  <https://forum.bambulab.com/t/h2s-issue-where-infill-meets-perimeter-at-front-of-print/216407>
  Transfer: weak. That gap depended on where it sat on the bed; ours runs along strap edges all
  over the piece.
- **Duet forum** (snippet only). After tuning pressure advance, raising overlap from 25% to 40%
  "changed nothing". <https://forum.duet3d.com/post/133242?page=3>
- **OrcaSlicer wiki, infill settings** (fetched). "Infill area is enlarged slightly to overlap with
  wall for better bonding", and it advises "~10-15% to minimize potential over extrusion".
  <https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_infill.html>
  That is general advice for all layers, not first-layer advice.

### 5.2 The fill angle against the straps

- None of the 11 pages I fetched ties first-layer slits to the angle between the fill and the
  wall. The case rests on the code (§3.3) and our own bedface-4 pairs.
- **Bambu forum 146050** (fetched): one reply's list of changes includes "90° infill" alongside
  six others, with no outcome.
- **MatterHackers, infill settings** (snippet only): the angle is relative to the X axis, 45° as
  the baseline. General, not about gaps.
  <https://matterhackers.com/mattercontrol/support/slice-settings/general/infill>

### 5.3 Bed adhesion: a clean plate and a fresh bed check

The idea: a fill line that does not stick at once gets dragged inward at a sharp turn, which
leaves a gap at the wall. I found no source that tests this for slits at the wall.

- **Bambu forum 67165** (snippet only). "99% of the time it's due to improper plate cleaning", and
  "IPA just doesn't cut it", with a dish soap wash recommended.
  <https://forum.bambulab.com/t/bed-adhesion-issues/67165> That thread is about parts not
  sticking, not slits.
- **Bambu forum 250557** (fetched). P2S. One reply: "Run an autocalibrate from the menu" and clean
  the plate (Bullocks, 2026-04-20). Not reported as tried.
  <https://forum.bambulab.com/t/fixing-first-layer/250557>
- The merged research from 2026-10-12 found one H2S user whose fix was bed leveling plus automatic
  calibration before each print (forum 248800).

### 5.4 A lower first layer (more squash)

- **Prusa forum, "low density on first layer"** (fetched). Lowering Z "as far as possible" gave
  "some positive effect but did not fully close the gaps", and made the first layer's top
  "unclean" (MSt, 2023-07-09). Another user: "With sufficient squish the first layer will fill in
  any gaps shown on a slice preview" (Neophyl, 2023-07-03).
- **Prusa forum, "Gap Between Solid Infill and Perimeters"** (fetched). "This is a issue with your
  first layer height. You need to get the nozzle closer to the bed" (Neophyl, 2025-04-02). No
  outcome reported.
  <https://forum.prusa3d.com/forum/prusaslicer/gap-between-solid-infill-and-perimeters/>
- **Bambu forum 250557** (fetched). P2S: the poster moved the nozzle closer, but changed pressure
  advance, flow and a gap setting at the same time, so the effect of each is not known.

### 5.5 A slower first layer

- **Bambu forum 256070** (fetched). A1 mini, Bambu Studio, gaps between walls and fill on the
  first layer of a round part. Slowing the first layer and fill to 25 mm/s "made it worse", per
  the poster (compl1cated, 2026-07-03). More flow: no effect. Every fill pattern still left "a
  small gap somewhere between the walls and infill".
  <https://forum.bambulab.com/t/need-help-please-small-gaps-on-first-layer/256070>
- **Bambu forum 67327** (fetched). X1C, gaps in the first layers after slowing to 25 and 50 mm/s
  and raising flow to 1.08. The reply: "Calibrate the filament and the default speeds will work
  well" (lkraus, 2024-03-28). No outcome.
  <https://forum.bambulab.com/t/small-gaps-in-first-layers/67327>

### 5.6 Pressure advance

"Pressure advance" (Bambu calls it Flow Dynamics, with a factor K) eases the plastic pressure
before a corner or a stop, so the nozzle does not ooze. Set too high, it starves the line just
before the turn.

- **Bambu forum 250557** (fetched). P2S, gaps between fill and walls: "The gaps are occurring
  where the nozzle changes direction" (lkraus, 2026-04-20). The poster then dropped K from 0.12 to
  0.02, reasoning it "was set too high, which caused gaps between the outer walls and the infill"
  (Harth, 2026-04-21). He changed four settings at once, and 0.12 is an unusual start.
- **Klipper documentation, pressure advance** (fetched). Above the right value: "rounded corners
  and poor extrusion leading up to the corner".
  <https://github.com/Klipper3d/klipper/blob/master/docs/Pressure_Advance.md>
  Transfer: Klipper firmware, not Bambu's, but the same idea of starving a line before a turn.
- **Voron forum** (snippet only). "If there are gaps your PA value is too high."
  <https://forum.vorondesign.com/threads/how-to-confirm-your-pressure-advance-value-is-correct.23>

Our slits sit where fill lines turn or stop at the wall, which is where this would act. The
merged research already plans a hand-set K as a later whole-plate step.

### 5.7 More walls, or Arachne walls

"Arachne" is a wall generator that varies line width to fill narrow shapes with walls.

- **Bambu forum 256070** (fetched). "You will not be able to eliminate all gaps, but the Arachne
  wall generator helps somewhat" (EnoTheThracian, 2026-07-02). Not tested by the poster.
- **Bambu forum 146050** (fetched). "Arachne with 999 walls" or a concentric first layer
  (EnoTheThracian, 2025-02-15). No outcome.
- Our own slice from 2026-10-10 ([the bed-face slits slice](2026-10-10-bed-face-slits.md)): four
  Arachne walls cut the planned bare area on the whole coaster from 36.0 to 25.6 sq mm, less than
  30% overlap did (19.8). On the 3.75 mm "middle" piece it was worse (0.69 against 0.41). It moved
  the outer walls by 0.017 to 0.028 mm. A strap made of walls is close to the ring pattern we
  dropped, so the same dashes where loops meet are likely.

### 5.8 Bottom patterns that turn at the wall more often

- **Cura forum** (snippet only). With "Connect Top/Bottom Polygons", Cura links the lines into one
  path; "where sharp angles appear in the outline, small gaps in the first layer are left".
  <https://community.ultimaker.com/topic/19608-cura-27-toolpath/>
- **Prusa forum, "low density on first layer"** (fetched). The poster "changed the pattern" and saw
  "some additional improvement", without saying which pattern.
- A search snippet credits a Bambu user with "monotonic infill pattern instead of rectilinear
  helped reduce gaps". I could not find which thread it came from, so I do not lean on it.

Bambu Studio's "zig-zag" bottom (the `rectilinear` key) joins lines along the wall in the same way
as the stock `monotonic`, but does not force the lines into one sweep across. My inference: it may
leave fewer lone line ends on narrow straps. Untested. Compose does not accept that value today.

### 5.9 Other slicers' tools

- **OrcaSlicer "Apply gap fill"** (fetched, wiki): "Enables gap fill for the selected solid
  surfaces", with choices Everywhere, Top and Bottom, or Nowhere. On forum 86402, a user found it
  "filled the outer gap well" in OrcaSlicer, in the preview (Berioldir, 2024-07-09).
- **OrcaSlicer "Anchor"** (fetched, wiki): "Connect an infill line to an internal perimeter with a
  short segment of an additional perimeter." That page lists it with sparse fill, not the bottom.

Moving to another slicer would change the whole print pipeline, not one setting.

### 5.10 A smaller nozzle

- **Bambu forum 256070** (fetched). "you're limited by the nozzle size", with a suggestion to try a
  0.2 mm nozzle in the slicer preview (RetroSharky, 2026-07-02). Not printed.

A hardware change, slower to print, and it changes every line on the coaster. Listed, not ranked.

## 6. Leads I looked at and set aside

| Lead | Why it is set aside |
|---|---|
| Lay the fill first | The code always lays walls first on the first layer (§3.1) |
| Faster or slower gap fill | Gap fill on layer 1 already runs at 50 mm/s, and none is dropped (§3.2) |
| Elephant-foot compensation | Shrinks walls and fill together; fit risk (§3.6) |
| `wall_sequence` (inner or outer loop first) | The fill still stops at the inner loop either way. No source ties it to these gaps |
| `only_one_wall_first_layer` | The fill then stops at the outer loop instead, with as many line ends. No source |
| Narrower first line | 0.42 mm was cleanest in the slice and made no difference in print |
| `monotonicline` and its travel extend | bedface-4: it only moved the slits. 200% smeared (merged research) |
| Acceleration and jerk on layer 1 | Already 500 mm/s² and 9; whole plate; no source ties them to these gaps |

## 7. Sources

Fetched and read (11 pages): Bambu forum 256070, 250557, 216407, 86402, 198663, 67327, 146050;
Prusa forum "low density on first layer" and "Gap Between Solid Infill and Perimeters"; the
OrcaSlicer infill wiki page; Klipper's pressure-advance page.

Snippet only (5): the Duet forum post, the Voron forum thread, the Cura forum thread, Bambu forum
67165, MatterHackers' infill page. The unattributed snippet in §5.8 is not counted, since I could
not find its page.

Code read at the tag v02.08.02.61 (8 files): PrintConfig.hpp, PrintConfig.cpp, Fill.cpp,
FillRectilinear.cpp, PerimeterGenerator.cpp, GCode.cpp, ExtrusionEntity.hpp,
PrintObjectSlice.cpp, plus the X2D process profiles.
