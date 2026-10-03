---
date: 2026-09-26
produced-by: research agent B (Claude Opus 5.5), one of two independent print-quality researchers; web search and fetch, `gh api` for GitHub issues, and a read of the Bambu Studio 02.08.02.61 preset files and the minis-04 sliced 3MF on this machine
feeds:
  - '[[print-quality-b-design]]'
---

# Print quality research B: small openwork PLA coasters on the X2D

The raw findings behind [`../design/printing/print-quality-b-design.md`](../design/printing/print-quality-b-design.md).
The question: how to lift the print quality of small, thin, openwork PLA coasters on a
Bambu X2D, and what caused the three things Omar saw on the minis-04 plate on
2026-09-26: "i see tiny holes on the print and the peg system border is too big and
pegs too tight".

Every web source says whether I **fetched** the page (read the whole text) or saw only a
**search snippet**. A snippet is a line or two the search engine showed. It can be out of
context, so nothing load-bearing in the design doc rests on a snippet alone. Quotes are
kept short. Everything else is paraphrase.

## 1. Local evidence: what minis-04 was actually sliced with

This is the finding that matters most, and it comes from our own files, not the web.

**Where I looked.** The sliced plate that `bambu slice compose` wrote for minis-04 lives
at .bambu/plates/minis-04.plate.3mf. That folder is gitignored, so this is a local path,
not a repo link. I read two places inside it: `Metadata/project_settings.config` and the
settings block at the end of the G-code. The slice warnings file was empty. Studio
version: 02.08.02.61.

**What the plate asked for** ([`../design/plates/minis-04.yaml`](../design/plates/minis-04.yaml)):
process "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D", filament "Bambu PLA Basic
@BBL X2D 0.4 nozzle".

**What the preset chain on disk says.** I read these files in the Studio app bundle,
under Contents/Resources/profiles/BBL/process and BBL/filament:

- `0.20mm Standard @BBL X2D.json` inherits `fdm_process_dual_0.20_nozzle_0.4`. That
  inherits `fdm_process_dual_common`, which inherits `fdm_process_common`.
- `fdm_process_dual_0.20_nozzle_0.4` sets elefant_foot_compensation 0.15,
  top_shell_layers 5, top_shell_thickness 1.0.
- `fdm_process_common` sets wall_generator classic, wall_loops 2, bottom_shell_layers 3,
  line_width 0.42, inner_wall_line_width 0.45, initial_layer_line_width 0.5,
  seam_position aligned, xy_hole_compensation 0, xy_contour_compensation 0, ironing
  none, sparse infill 15%.
- The PLA base `fdm_filament_pla` sets hot_plate_temp 55, textured_plate_temp 55,
  slow_down_layer_time 4, nozzle 220.

**What the sliced file actually used:**

| Setting | In the sliced 3MF | What the preset chain says |
|---|---|---|
| wall_generator | arachne | classic |
| elefant_foot_compensation | 0 | 0.15 |
| top_shell_layers / top_shell_thickness | 4 / 0.6 | 5 / 1.0 |
| outer / inner wall line width | 0.4 / 0.4 | 0.42 / 0.45 |
| initial_layer_line_width | 0.4 | 0.5 |
| sparse infill | 20% cubic | 15% grid |
| hot_plate_temp / textured_plate_temp | 45 / 45 | 55 / 55 |
| slow_down_layer_time | 5 | 4 |

Other values in the sliced file: curr_bed_type Cool Plate, filament_flow_ratio 0.98,
seam_position aligned, seam_gap 15%, filter_out_gap_fill 0, both X-Y compensations 0,
ironing none, wall_sequence inner/outer. outer_wall_speed 200 and gap_infill_speed 250
match the **leaf** preset, so the leaf's own keys were applied.
`different_settings_to_system` was empty, so Studio did not think anything had been
changed.

The minis-03 slice (build/plates/minis-03.plate.3mf, also local) shows the same pattern.

**Reading.** Keys written in the leaf preset file were applied. Keys the leaf only
inherits from its parents fell back to values that look like Studio's built-in defaults.
The preset files never set arachne, 0.4 mm lines, 4 top layers or a 45 °C bed, so those
values came from somewhere other than the named preset.

**Why this happens.** Our slicer wrapper passes the leaf preset file to the Studio command
line as-is (`resolvePresetList` in
[`../../tools/bambu/src/commands/slice.ts`](../../tools/bambu/src/commands/slice.ts)).
BambuStudio issue #6836 (below) says the command line does not resolve inheritance.

**Open.** If Omar re-sent the plate from the Studio desktop app, the app may have
re-sliced it with the full preset. The file on disk is what our tool made. Whether the
printed plate matches it can be checked in the app without touching the printer.

## 2. Bambu Studio command line and presets

**github.com/bambulab/BambuStudio/issues/6836**, fetched with `gh api`. The issue is
about command-line slicing with system presets. Bambu maintainer lanewei120 replied:
"CLI has limited logic to process the jsons, we suppose the full json has been generated
before when passed to CLI". Read: the command line expects a fully flattened preset, and
a preset that only says `inherits` is not expanded. A commenter adds that the command
line also clamps machine limits. The hedge: this is a maintainer's comment on an issue,
not documentation, and it may change in a later Studio version.

Local confirmation: §1 above.

**The same presets on GitHub** (fetched with `gh api`, BambuStudio `master`, 2026-09-26):
- `resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json`
  (https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json)
  sets elefant_foot_compensation "0.15", top_shell_layers "5" and top_shell_thickness
  "1.0".
- `resources/profiles/BBL/process/fdm_process_common.json`
  (https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/process/fdm_process_common.json)
  sets these:
  - wall_generator "classic", wall_loops "2", detect_thin_wall "0";
  - line_width "0.42", inner_wall_line_width "0.45", initial_layer_line_width "0.5";
  - seam_position "aligned";
  - both X-Y compensations "0", and elefant_foot_compensation "0", which its child
    overrides to 0.15;
  - ironing "no ironing";
  - wall_infill_order "inner wall/outer wall/infill".

These match the files in the installed 02.08.02.61 app bundle for the keys listed. The
K10 hedge: `master` can move ahead of the installed version, so the bundle on this
machine is the authority for what our slicer would have used.

## 3. Bambu wiki pages (fetched)

wiki.bambulab.com answers the normal web fetcher with HTTP 402. I fetched these pages
with a browser user agent and read their text. Each was re-read on 2026-09-26 before I
wrote this file.

**wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation** (fetched).
- There are two separate settings. **Hole** compensation "Adjusts the size of holes
  (closed, hollow areas)" and "does not change the outer size of the model". **Contour**
  compensation "Adjusts the outer contour of the model" and leaves hole sizes alone.
- The hole diameter grows by twice the compensation value, so the value is per side.
- The page lists causes to check and correct *before* you touch compensation: material
  shrinkage, elephant's foot, moist filament, flow dynamics not tuned, holes near nozzle
  size, missing chamfers, and the seam, which "can affect hole precision".
- Its method is to print a test model with the same process and filament, find the
  fitting hole, and enter that value. It says the calibration "is specific to each
  filament". In its worked example a hole measured 0.24 mm undersize.
- My note, not from the page: a dovetail slot is open to the part's edge, so it belongs
  to the outer contour, not to a closed hole. Only contour compensation moves its faces.
  Hole compensation would instead move the openwork windows between the straps.

**wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot** (fetched).
- Elephant's foot is the first layer, "and sometimes the first few layers", coming out
  wider than the layers above. Two things cause it: heat from the bed, and the weight of
  the layers above pressing on a base that is still soft.
- On parts where tolerance matters, such as "assemblies, snaps, rails", the flare
  "directly affects fit" and can make assembly "fail completely".
- The compensation shrinks the first-layer outline. For ordinary models "the system
  default is fine". For tight-tolerance parts the page gives a measure-and-calculate
  procedure: clean the plate, level the bed, calibrate flow dynamics, print a test
  model, then measure.

**wiki.bambulab.com/en/software/bambu-studio/wall-generator** (fetched).
- **Classic** walls have one width, and each wall is a closed loop. That gives "only one
  seam per layer" and better surface quality. The cost: features narrower than the line
  width can vanish from the slice.
- **Detect thin wall** fixes that in some cases but can make walls overlap or leave
  broken, fragile single lines.
- **Arachne** varies the line width. It keeps small details and does not overlap walls.
  But it "will generate discontinuous wall paths" in some cases, and these "can affect
  the print surface quality".
- Arachne blends between different line counts with wedge-shaped "wall transition"
  paths. Its parameters are a transition angle, a filter margin and a transition length.
  The page warns that more wedges "may cause over-extrusion".

**wiki.bambulab.com/en/software/bambu-studio/Seam** (fetched).
- The seam is the gap where a loop starts and ends, and it is "unavoidable in FDM".
- Nearest ranks candidate spots "concave non-overhang vertex > convex non-overhang
  vertex > …". Aligned uses the same candidates, then picks the one nearest the previous
  layer's seam.
- Seam gap: "the extrusion is stopped in advance … leaving a gap at the seam position".
  It is a percent of nozzle diameter, and the default is 15%.
- You can paint the seam by hand. Scarf seams, added in Studio 1.9, overlap the loop
  ends to hide the seam better.
- My note: the corners at the dovetail's mouth and slot are concave vertices, the spots
  the seam logic ranks first. A seam bump or gap there lands on a fit face.

**wiki.bambulab.com/en/knowledge-sharing/troubleshooting-printing-issues** (fetched).
- The page is general, "can be used for most Bambu Lab 3D printers".
- **Even gaps in the top layer** mean under-extrusion. The most common cause is a flow
  ratio set "a bit too low". Its example is 0.98, "considered normal for PLA filament
  with X1C", where raising it to 1.00 "should solve the problem". The best fix is the
  flow calibration in Studio.
- **Overheating on small objects.** Minimum layer time (about 4 s in its example) slows
  small layers down so they can cool. The page says this "is commonly a problem when
  printing very small objects".

## 4. Bambu forum threads (fetched)

These are user reports, not tests.

**forum.bambulab.com/t/top-surface-has-tiny-holes-and-gaps/5489** (fetched).
- **Cause named:** line geometry. The printer fills a shape with lines of a set width and
  "the turns and ends of those lines are round", so gaps are left in "very pointy
  corners" and "long, narrow pointy areas". A bigger nozzle leaves bigger gaps.
- **Fixes suggested:**
  - calibrate flow and pressure advance;
  - monotonic top pattern;
  - Arachne ("variable line thickness should help");
  - a narrower top-surface line (0.25 mm);
  - a hotter nozzle (PLA at 240 °C);
  - slower top surfaces;
  - ironing.
- **What held up:** the original poster got "best (not perfect) results" by combining
  several of these. Flow calibration "helps the problem on bigger surfaces". Ironing
  "does not always work with small and narrow surfaces". One later user found ironing
  "the only thing that seems to help".

**forum.bambulab.com/t/micro-gaps-in-outer-skin/15122** (fetched).
- **Causes suggested:** gaps in the outer wall came from binding in the filament path,
  dirty extruder gears, a failing extruder motor, too much volumetric flow, retraction or
  wipe, wall order, and hotend variance.
- **What the original poster confirmed:** printing the outer wall *not last*
  "dramatically reduced the occurrence". Turning retraction off also helped but caused
  stringing.
- **A second poster** fixed silk filament by raising the flow ratio from 0.98 to about
  0.99–1.0.
- The thread does not discuss Arachne.

**forum.bambulab.com/t/holes-when-printing-seam-patterns/256619** (fetched).
- **The case:** holes on the top layer of a multi-colour keychain with a very dense mesh
  (330,000 detail elements), on a 0.4 mm nozzle.
- **Confirmed cause:** ironing. "Turn it on and the holes appear; turn it off and
  they're gone." A 0.2 mm nozzle also gave fewer holes.
- **Consensus:** it was mostly a modelling problem, "the details are much too small for
  a 0.4 nozzle".

**forum.bambulab.com/t/how-to-join-large-flat-parts-at-the-edge/87473** (fetched).
- **The case:** joining flat printed parts edge to edge, on a P1S.
- **Joins suggested:** a zipper joint, dovetails, and the Studio cut tool's connectors.
- **One dovetail result:** a poster makes dovetails "quite tight (about 0.04mm gap)"
  with "rounded corners". The parts go together with "a light tap with a small hammer",
  and "layer lines hold the parts together". No material is stated.
- **K10:** one person's result on a P1S, for a join meant to replace glue. A coaster the
  user pulls apart by hand is a different fit. It also does not say whether 0.04 mm is
  per face or total.

## 5. BambuStudio GitHub issues (fetched)

**github.com/bambulab/BambuStudio/issues/8784** (fetched with `gh api`, still open).
- **The report:** "Top surface under extrusion and pin holes", on Studio 02.03.01.51 with
  an H2S. The reporter says the pinholes show **in the slice preview**, together with a
  slightly lower filament total.
- **Their workaround:** re-slice with 0 walls, then re-slice with the original wall
  count. The holes go and filament use rises a little.
- **K10:** this is a different printer and an older Studio than our 02.08.02.61. It shows
  that a slicer state alone can cause pinholes, visible in the preview before printing.
  It does not show that ours does.

## 6. Fit and clearance sources

**hubs.com, "how to design interlocking joints"** (fetched).
- Gives FDM a tolerance of about "0.5 mm", and says tight interlocking joints are harder
  in FDM than in SLA or SLS.
- Generic FDM advice across machines, not tuned to one printer.

**formlabs.com/blog/how-to-3d-print-interlocking-joints** (fetched).
- SLA: 0.4 mm recommended. Under 20 mm² features 0.2 mm, over 20 mm² 0.4 mm.
- SLS: 0.3 / 0.6 mm.
- FDM needs larger clearances than SLA or SLS, and is less suitable for tight joints.
- Smaller, thinner parts: about "0.2 mm tolerance gap". Larger, chunkier ones: about
  "0.4 mm".
- K10: the numbers are for resin and powder printers first. The FDM text is qualitative.

**tools.creative3dp.com press-fit calculator** (fetched).
- A fit ladder: press −0.10, snug +0.05, sliding +0.15, free +0.35 mm.
- Given as **diametral** clearance, the total gap across the part.
- Holes tend to print 0.1 to 0.3 mm small, and shafts about 0.1 mm large.
- Note: CAL-FIT-01's ladder in `.claude/skills/calibrate/bets.md` uses these same four
  numbers.

**makerworld.com dovetail tolerance test, model 132619** (search snippet only; the site
returned 403). A printable dovetail test with several clearances. I could not read which
clearances or what users reported.

**Prusa knowledge base, clearance for printed-in-place and mating parts** (search
snippet only). The snippet recommends clearance of "at least 0.3 mm" between parts. I
did not see the context.

## 7. Wet filament, flow and general quality (search snippets only)

These pages were not fetched. Nothing in the design doc rests on them alone. Moist
filament is also named by the fetched X-Y compensation page (§3), but only as a cause of
uneven extrusion; the specific "holes and craters" symptom below is snippet-only.

- **Sovol and Siraya pages on wet filament** (snippets): PLA picks up moisture. Signs are
  popping or hissing, steam, bubbles, stringing, and small craters or holes on the
  surface. Drying is the fix.
- **3dprofilefix and fashion3d pages on pinholes** (snippets): they list under-extrusion,
  too few top layers, wet filament and too-fast printing as pinhole causes.
- **Seam gap snippets**: a large seam gap leaves a hole where a loop closes. Reducing
  seam gap is the fix.
- **"Filter out tiny gaps" snippets from Studio issues**: when this filter is on, gap-fill
  lines under a length are dropped, and that can leave small holes. In our slice it was 0
  (off), so it is not our cause.

## 8. Joins: narrower edges (search snippets only)

- **Jigsaw-connector forum snippet** (forum.bambulab.com): a poster started at "0.30 mm"
  clearance and considered raising it to "0.40". The full thread was not read.
- **Gridfinity snippets**: clip variants differing by 0.2 mm; socket clearance around
  0.25 mm. Other parts, other geometry, context unread.

## 9. What I did not find

Among the sources above, none gives a measured clearance for a dovetail between two thin
(under 3 mm) PLA plates on an X2D. None gives a measured pinhole rate for Arachne against
Classic on 2 mm straps. Both need a print.
