---
date: 2026-09-26
produced-by: research agent A (Claude Opus 5.5) — WebSearch, WebFetch, a browser-UA fetch for wiki.bambulab.com (WebFetch got HTTP 402 there), `gh issue view` for the BambuStudio GitHub issue, and a read of the Bambu Studio system profiles shipped inside the app on this machine
feeds: docs/print-quality-a-design.md
---

# Print quality for thin openwork PLA coasters on the X2D — sources

The question: how to raise the general quality of small, thin, openwork PLA coaster prints on
a Bambu Lab X2D, and how to fix the three defects Omar saw on minis-04 (2026-09-26): "i see
tiny holes on the print and the peg system border is too big and pegs too tight".

This file holds the sources behind [`../print-quality-a-design.md`](../print-quality-a-design.md).
Each entry says whether the page was **fetched** (the text was read) or is **snippet** (only a
search-result summary was seen — treat anything taken from it as a lead, not a fact). It is
not a survey of print tuning; it covers the pages listed here and nothing else.

## 0. The slicer profile the plate actually uses (read on disk)

Read from `/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/` — Bambu Studio app
02.08.02.61, BBL profile bundle 02.08.00.05. Caveat: the copies Bambu Studio keeps under the
user's `~/Library` can be newer than the app bundle and were not read, so these are the values
as shipped, not necessarily as sliced.

The process preset chain is `0.20mm Standard @BBL X2D` → `fdm_process_dual_0.20_nozzle_0.4`
→ `fdm_process_dual_common` → `fdm_process_common`. The effective values that matter here:

| Setting | Value | Set in |
|---|---|---|
| `wall_loops` | 2 | common |
| `wall_generator` | classic | common |
| `detect_thin_wall` | 0 (off) | common |
| `only_one_wall_top` | 1 | common |
| `wall_infill_order` | inner wall / outer wall / infill | common |
| `top_shell_layers` / `top_shell_thickness` | 5 / 1.0 mm | dual_0.20 |
| `bottom_shell_layers` / `bottom_shell_thickness` | 3 / 0 | common |
| `sparse_infill_density` | 15% | common |
| `infill_wall_overlap` | 15% | common |
| `elefant_foot_compensation` | 0.15 mm | dual_0.20 (common has 0) |
| `xy_hole_compensation` / `xy_contour_compensation` | 0 / 0 | common |
| `enable_circle_compensation` | 0 | common |
| `seam_position` / `seam_slope_type` | aligned / none | common |
| `top_surface_pattern` / `bottom_surface_pattern` | monotonicline / monotonic | common |
| `ironing_type` | no ironing | common |
| `monotonic_travel_into_wall` | 45.0 | dual_common (common has 0.0) |
| line widths: default, outer wall, top surface | 0.42 mm | dual_0.20 |
| line widths: inner wall, sparse infill | 0.45 mm | dual_0.20 |
| line width: first layer | 0.5 mm | dual_0.20 |
| outer wall / inner wall / top surface speed | 200 / 300 / 200 mm/s | X2D preset, "Direct Drive Standard" variant |
| first-layer speed / first-layer infill speed | 50 / 105 mm/s | X2D preset |
| top surface / outer wall acceleration | 2000 / 5000 mm/s² | X2D preset |
| gap infill speed | 250 mm/s | X2D preset |

The X2D preset carries six extruder variants (Direct Drive Standard, Direct Drive High Flow,
Direct Drive E3D High Flow, and three Bowden variants for extruder 2). The values above are the
Direct Drive Standard column. The minis-03 print record leaves `nozzle_type` null, so which
column was sliced is not recorded.

Filament preset `Bambu PLA Basic @BBL X2D 0.4 nozzle`: flow ratio 0.98, nozzle 220 °C, max
volumetric speed 21 mm³/s, `slow_down_min_speed` 20 mm/s.

## 1. Tiny holes (pinholes, gaps)

**Bambu wiki — Wall generator** — https://wiki.bambulab.com/en/software/bambu-studio/wall-generator — **fetched**.
Classic walls have a fixed width and one seam per layer; for a thin region "If the polygon is
too small, the result of the shrinkage will be empty", i.e. a narrow strip can be left without
a wall. "Detect thin wall" can overlap walls. Arachne varies the line width so walls do not
overlap, but can produce discontinuous walls. The page does **not** say which generator is the
default; a search summary claimed Arachne is, but the shipped X2D profile (§0) says classic.

**Bambu wiki — Seam** — https://wiki.bambulab.com/en/software/bambu-studio/Seam — **fetched**.
The seam gap default is 15% of the nozzle diameter. Aligned and Nearest seams prefer concave
corners, then convex ones, avoiding overhangs. Random seams cause zits across the surface.

**Bambu wiki — Ironing** — https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing — **fetched**.
Off by default; "only effective when the top surface is flat". Warns that slow, low-flow ironing
with PLA risks heat creep and clogs, and that the nozzle rubs the part, which can knock a small
part loose.

**Bambu wiki — Flow rate calibration** — https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate — **fetched**.
Too low a flow shows as "gaps in the printed lines". The page says "Only X1 series support Auto
calibration" of flow — written before the X2D; whether it applies to the X2D is not stated.
Manual calibration: coarse 5% steps, then fine 1% steps.

**Bambu wiki — Flow dynamics (pressure advance) calibration** — https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa — **fetched**.
Pressure lag shows as underextrusion — "gaps or thin lines" — at line starts and speed changes.
Results can jitter by about 10%, and damp filament makes them unreliable.

**Bambu wiki — Troubleshooting printing issues** — https://wiki.bambulab.com/en/knowledge-sharing/troubleshooting-printing-issues — **fetched**.
"Even gaps in top layer": flow ratio "0.98 which is considered normal for PLA filament with
X1C"; raise it toward 1.00, rarely above. "Inconsistent gaps" come from the wrong nozzle
selected in the slicer. "Lines not connected" come from a pressure-advance K that is too high;
K is typically 0.02–0.04. Dots or blobs come from random seams or moisture — "recommended to dry
all filaments". Small objects need a minimum layer time so each layer cools.

**Bambu wiki — PLA** — https://wiki.bambulab.com/en/filament/pla — **fetched**.
PLA has "low hygroscopicity" and can be stored at 50–60% RH. The must-dry list names Silk, Wood,
Aero, carbon-fibre and Translucent PLA; PLA Basic is not on it. Drying prevents "bubbles, holes".

**Bambu wiki — Identify and fix first-layer issues with a test print** — https://wiki.bambulab.com/en/knowledge-sharing/identify-and-fix-first-layer-issues-with-a-test-print — **fetched (partly)**.
A good first layer has "no air gaps". Fixes: wash the plate, dry the filament, slow the first
layer (the page's example: outer wall 30 mm/s, infill 60 mm/s), and a 0.2 mm single-layer test.

**BambuStudio GitHub issue #9768 "Gaps in prints"** — https://github.com/bambulab/BambuStudio/issues/9768 — **fetched** (`gh issue view`).
Open since 2026-02-14, filed on an H2C. A Bambu staff member (Mujin-code): "The temporary
solution is to use monotonic lines and overlaps". A contributor (Diatom-Bambu, 2026-02-27) said
they are "aware of the issue… will include some mitigation measures in the next Bambustudio
release", and later that the new `monotonic_travel_into_wall` option "is designed to improve
pinholes". User ingoingo: the infill/wall overlap setting "doesn't apply to the standard top
infill pattern Monotonic Line"; switching to Monotonic with overlap 55% made the holes almost
disappear. User interpretor (2026-04-22): "I have a new X2D and immediately noticed gaps… more
often like those described in this issue". User bulbabam: a 0.35 mm first-layer or top line
width helped. These are one user's reports each, not measurements.

**Bambu forum — First/top layer gaps on H2 series, confirmed bug** — https://forum.bambulab.com/t/first-top-layer-gaps-on-h2-series-confirmed-bug-still-unresolved/256312 — **fetched**.
Users on H2C/H2D/H2S report pinholes and gaps in first and top layers and call it a slicer bug.
No X2D mention.

**Bambu forum — Top surface has tiny holes and gaps** — https://forum.bambulab.com/t/top-surface-has-tiny-holes-and-gaps/5489 — **fetched** (users, not staff).
Explanation offered: "turns and ends of those lines are round", leaving gaps in "long, narrow
pointy areas". Fixes users tried: flow 1.05, top line width 0.25, 240 °C, a slower top surface,
monotonic, ironing, Arachne. Mixed results; no controlled test.

**Bambu forum — Gap between infill and inner wall** — https://forum.bambulab.com/t/gap-between-infill-and-inner-wall/68800 — **fetched**.
One poster fixed the gap by lowering pressure-advance K from 0.025 to 0.012 and confirmed it.

**Snippets only** (not fetched): a Bambu forum thread on bad top layers; a 3dprofilefix
top-surface guide suggesting 6–7 top layers, +5% infill and checking for wet filament; a
snippet giving an ironing flow of 15–30%.

## 2. Fits and tolerances

**Bambu wiki — Elephant foot compensation** — https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot — **fetched**.
The first layer flares outward; "On tolerance-critical parts such as assemblies… the flared base
directly affects fit". Calibrate with a 25×25×10 mm cube or gauge block, compensation 0, no
brim; measure the top and the bottom at mid-side with calipers to 0.01 mm; compensation =
(X deviation + Y deviation) / 2. The worked example lands at 0.10 mm. The right value varies by
build plate type.

**Bambu wiki — X-Y hole and contour compensation** — https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation — **fetched**.
Hole compensation moves closed holes; contour compensation moves the outer contour. Check first:
shrinkage, elephant foot, moist filament, flow dynamics, holes near nozzle size, lack of
chamfers, and "Seam, this feature can affect hole precision". A hole's diameter changes by twice
the value (the example: 0.24 mm undersize → compensate by half). Contour: (55 − measured) / 2 on
the test part, or iterate in 0.1 steps without calipers. Limitation: hole compensation "only
applies to closed paths"; on unclosed paths it can cause layer separation.

**Creative3DP — Press-fit tolerances** — https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/ — **fetched** (dated 2026-07-10).
A **diametral** ladder for round pins of 5–25 mm in PLA/PETG/ABS: press −0.10, snug +0.05, close
running +0.15, free +0.35. Holes print 0.1–0.3 mm undersize and shafts about 0.1 mm oversize;
keep fit allowance and printer compensation separate. Boxes: sliding +0.15 per mating pair. A
0.5 mm × 45° lead-in chamfer helps. Its test coupon changes one dimension by 0.05 at a time. It
cites Prusa "at least 0.3mm", Hubs 0.5 mm, Markforged 0.05 interference, and MDPI IT11–IT13.
This is the page `CAL-FIT-01`'s ladder was transcribed from (see
[`../c2-assembly-design.md`](../c2-assembly-design.md) §B.3).

**Prusa — Modeling with 3D printing in mind** — https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135 — **fetched**.
"An initial good measurement for movable parts is at least 0.3 mm" — the page does not say
whether that is per side or total. Elephant-foot compensation helps fits. "Using a chamfer on
the edges of two parts that slot together can save you a lot of effort when assembling." A wall
table of 0.45 / 0.9 / 1.35 / 1.8 mm for 1–4 perimeters at 0.45 mm width, labelled
"approximations"; "Walls thinner than one nozzle perimeter are not printable."

**Hubs (Protolabs Network) — Interlocking joints** — https://www.hubs.com/knowledge-base/how-design-interlocking-joints-fastening-3d-printed-parts/ — **fetched**.
Covers finger, dovetail and puzzle joints under friction, tension and shear. FDM interlocking
tolerance "0.5 mm" (SLA/SLS 0.2, material jetting 0.1) — not stated as per side or total. "ABS
is preferred over PLA due to higher ductility"; "Adding a small radius to part edges assists
joint assembly".

**Snippets only** (not fetched — leads, not facts):
- Bambu wiki search summary for XY compensation: PLA 0.05, ABS/PETG 0.1, nylon 0.15 as starting
  values. Not on the fetched page.
- BambuStudio GitHub issue #3817: different hole and contour values offset an inner surface into
  a visible ring.
- Sovol / utility guides: press 0.1, sliding 0.2–0.3, loose 0.4–0.5 mm per side.
- industrialmonitordirect.com: 0.2–0.5 mm per side for dovetails; PLA on a P1S shrinks
  0.2–0.4%. A puzzle-joint note: one user's 0.2 mm offset all round ("0.4mm total") was tight in
  PLA and freed up after a few cycles.
- artopia: 0.2–0.3 snug, 0.4 free; test 0.05 / 0.1 / 0.15 / 0.2 on one print.
- Prusa forum tolerance threads: 0.05 fused and 0.10 fine for one user; 0.15–0.20 for another.
- Bambu forum "How do you use tolerance value in your design with BL?"
  (https://forum.bambulab.com/t/how-do-you-use-tolerance-value-in-your-design-with-bl/123711):
  0.1–0.15 "more than enough" for typical joints on X1C/P1S; a 0.05 gap is below what a 0.4 mm
  nozzle resolves; out of the box with auto flow one user got 0.15–0.20.
- MakerWorld "Bambulab Tolerance Test" (https://makerworld.com/en/models/640436): a 0.05–0.30 mm
  per-side gauge with round, square and polygon pegs — "When a circular column can be inserted at
  0.1mm… the gap… on one side is 0.1mm".
- Printables tolerance test 32321.

## 3. What was not found

No source read here measures a fit on a dovetail only 1.4 mm tall, or pinholes on a 2 mm
freestanding strap. Every number in §2 was measured (where it was measured at all) on round pins,
boxes or gauges several millimetres tall. How each transfers is argued in the design doc.
