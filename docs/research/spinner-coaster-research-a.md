---
date: 2026-11-08
produced-by: researcher A agent (Claude Opus 5.5), one of two independent passes — WebSearch, WebFetch, Bambu Studio's source read at commit 4c2c19a4bf698edf153555dfe28fd4f81d6550be (master on 2026-11-07), a read of this repo at origin/master 3566906e and a grep of bikar at origin/main fe6b109e
feeds:
  - docs/design/pieces/spinner-coaster-design.md (the consolidated doc, not yet written; this pass's own draft is docs/design/pieces/spinner-coaster-design-a.md)
---

# Research A: a coaster that spins on a bearing dropped in mid-print

**The question.** Omar wants a spinner version of our coasters: the coaster prints as usual, the
printer pauses partway up, he drops a ball bearing into a pocket, and the print resumes and closes
over it, so the coaster's centre (or its rim) turns. How do we design and print that robustly on our
printer, without any risk to the printer?

**Our setup, for every "does this transfer" line below.** Bambu Lab X2D, 0.4 mm nozzle, PLA,
0.2 mm layers, first layer 0.2 mm (R4). Coasters are 90 mm (`7apC5Q9QS-8`) to 112.5 mm
(split-pocket) across and 4 to 4.4 mm tall (R1, R2).

**How to read this file.** Outside sources are S1, S2 and so on, grouped by topic. Each is marked
**FETCHED** (I read the page in this run) or **SNIPPET** (I saw only a search-result summary, or the
fetch failed, with the reason). Quotes are from the fetched text as the fetch tool returned it.
"Who said it" matters: most pause facts are forum users, not Bambu staff, and I say so each time.
Repo facts are R1 onward at the end. Prices are left out: this repo is public.

**Counts.** 37 outside sources: 26 FETCHED (four of them, S2 to S5, Bambu Studio source files
downloaded whole and searched; S27 came back empty), 11 SNIPPET.

**Not found anywhere I looked.** Nothing about how the **X2D** behaves during a pause: where its head
parks, what its heaters do, how it moves Z on pause and resume. Every behaviour report below is from
another Bambu model, or names no model. Bambu's own wiki page on the slicing preview returned 402 to
the fetcher, so no official Bambu page on pauses was read in this run.

## 1. How Bambu Studio adds a pause, and what it writes

**S1. Bambu Studio source, `CustomGCode.hpp`.** FETCHED (raw file on GitHub, master).
<https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/CustomGCode.hpp>
The per-layer item types, in order: `ColorChange, PausePrint, ToolChange, Template, Custom, Unknown`
(no explicit numbers, so PausePrint is 1). Each item has `print_z`, `type`, `extruder`, `color`,
`extra`.

**S2. Bambu Studio source, `GCode.cpp`, at commit 4c2c19a4.** FETCHED (downloaded whole; the fetch
tool could read only its first fifth).
<https://github.com/bambulab/BambuStudio/blob/4c2c19a4bf698edf153555dfe28fd4f81d6550be/src/libslic3r/GCode.cpp>
- Function `emit_custom_gcode_per_print_z`: for a PausePrint item it writes the line
  `;PAUSE_PRINTING` (a tag for Bambu's own G-code reader) and then the printer's
  `machine_pause_gcode`, followed by a newline.
- Function `process_layer`: the order inside one layer is `change_layer(print_z)` (the move up to
  the new layer), then the printer's layer-change G-code, then, under the comment
  `// Normal (non-sequential) print.`, the call to `emit_custom_gcode_per_print_z`, then the skirt
  and the layer's extrusions. **So the pause runs after the head has moved to the new layer's
  height and before anything of that layer is printed.** This agrees with S9 and S10 (Prusa).
- The call sits inside `if (single_object_instance_idx == size_t(-1))`, the non-sequential case.
  **In "print by object" mode the pause is not written.** S8 (snippet) agrees from the user side:
  the menu item is greyed out in that mode.

**S3. Bambu Studio source, `GCodeProcessor.cpp`, at master.** FETCHED (downloaded).
<https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/GCode/GCodeProcessor.cpp>
The reserved tag string is `" PAUSE_PRINTING"`; when the reader meets it, it records a pause point
in the preview. So a sliced file holding a pause has the literal text `; PAUSE_PRINTING` (with
whatever spacing the writer uses; S2 writes `";" + tag`, which gives `; PAUSE_PRINTING`).

**S4. Bambu Studio source, `bbs_3mf.cpp`, at master.** FETCHED (downloaded).
<https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/Format/bbs_3mf.cpp>
- Pauses are saved in the project 3MF as `Metadata/custom_gcode_per_layer.xml`
  (`CUSTOM_GCODE_PER_PRINT_Z_FILE`). The writer emits, per plate, `<plate_info id=…/>` and one
  `<layer top_z=… type=… extruder=… color=… extra=… gcode=…/>` per item, then `<mode value=…/>`.
- The loader reads that file only under `!dont_load_config`, the same switch that decides whether
  the project's settings are loaded. **Whether our CLI slicing path loads it is not settled by the
  source alone** (see R7, R8).

**S5. Bambu Studio source, `PrintConfig.cpp` and `BambuStudio.cpp`, at commit 4c2c19a4.** FETCHED
(downloaded).
<https://github.com/bambulab/BambuStudio/blob/4c2c19a4bf698edf153555dfe28fd4f81d6550be/src/libslic3r/PrintConfig.cpp>
and <https://github.com/bambulab/BambuStudio/blob/4c2c19a4bf698edf153555dfe28fd4f81d6550be/src/BambuStudio.cpp>
- The CLI has an option `load_custom_gcodes` ("Load custom gcode from json", example parameter
  `custom_gcode_toolchange.json`).
- The CLI reads that JSON with `CustomGCode::Info::from_json` and stores it for the plate being
  sliced (`plate_to_slice`, or plate 0).
- So the CLI has a second way to get a pause into a slice, separate from the 3MF file. I did not see
  the JSON's field names (`from_json` is in a file I did not read), and I did not run it. S8's
  snippet points at a Printago page documenting it.

**S6. Bambu forum, "Is a print pause effectively infinite?"** FETCHED.
<https://forum.bambulab.com/t/is-a-print-pause-effectively-infinite/28695>
All users, no staff. "Generally, the pause is as long as you want" (Wylaryzel). Level23: "I've
definitely had a repeatable problem with longterm pauses actually restarting" (overnight). The fan
keeps running. No firmware timeout reported. P-series category, no model named.

**S7. Bambu forum, "Pause at layer?"** FETCHED.
<https://forum.bambulab.com/t/pause-at-layer/7025>
"Right click on the layer slider will give you the option to add a pause." One user edits the
"Machine Pause G-code" to drop the bed 100 mm around `M400 U1`; he warns tall prints cannot drop the
full 100 mm and the bed then rises 100 mm into the nozzle. Another: "do not move the head manually
as it could loose its location in the 3D space." No model named in this excerpt.

**S8. Search summaries on adding and storing pauses.** SNIPPET.
Queries "custom_gcode_per_layer.xml Bambu Studio 3mf pause type" and "wiki.bambulab.com pause layer
slider". Points seen only in summaries: pause and custom G-code are "grayed out in Print by Object
mode" (forum, <https://forum.bambulab.com/t/pause-at-layer-when-print-sequence-by-object/110033>);
Printago documents a CLI custom-gcode JSON with the same type names
(<https://printago.io/slicer-cli/load-custom-gcodes>); one user says Studio places pauses "at the
beginning of the layer". The Bambu wiki page
(<https://wiki.bambulab.com/en/software/bambu-studio/view-slicing-information>) returned 402 when
fetched.

**S9. Prusa help, "Insert pause or custom G-code at layer".** FETCHED.
<https://help.prusa3d.com/article/insert-pause-or-custom-g-code-at-layer_120490>
The pause is inserted "**before** the selected layer is printed". Magnets "need to be firmly in
their slots" or they can stick to the print head; use a tight slot or a drop of super glue. A search
summary of the same page adds that pauses do not work with sequential printing.
*Transfer:* PrusaSlicer, not Bambu Studio; it agrees with S2's reading of Bambu's source, which is
the evidence we rest on.

**S10. Prusa blog, "Practical uses of color change in PrusaSlicer".** FETCHED.
<https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/>
- "the starting point of the color change is at the beginning of the selected layer"; "Users often
  tend to set the change one layer above or below the desired point."
- "The most suitable spacing is 0,15mm in all directions" (MK3S profiles, 0.4 mm nozzle, 0.15 mm
  layers). Too little can fail the print, too much rattles.
- Cover a cosmetic insert with "only a few layers of filament (2-3 should work just fine)".
- "embedding large metal parts requires spreading a thin layer of glue stick on them"; magnets can
  "jump out and stick to metal parts of the printer", so superglue them.

**S11. Printago, "Bambu Studio magnet holes".** FETCHED.
<https://printago.io/guides/bambu-studio-magnet-holes>
Size the pocket so "the magnet sits just below a layer that will later cover it"; "find the layer
where the pocket gets capped and add a pause at that layer". Pocket "diameter plus about 0.1 to
0.2 mm clearance" (on the diameter). Pauses need someone present. Keep magnets away from the nozzle
and steel parts.

**S12. Bambu forum, "How to change the default pause settings".** FETCHED.
<https://forum.bambulab.com/t/how-to-change-the-default-pause-settings/147603>
P1S owner. The head "always goes to the back of the case" when paused. JonRaymond (user): "You
can't change where the M400 U1 parks"; "It's baked into the firmware". The pause G-code field "is
only for manually inserted pauses". Heaters not covered.

**S13. Search summaries on M400 U1 and on heaters during a pause.** SNIPPET.
Users describe `M400 U1` as "Stops print till user presses 'Resume'" and as behaving "just like when
printer is paused from touch screen" (<https://forum.bambulab.com/t/how-to-change-the-default-pause-settings/147603/6>).
One user: "on a pause, the nozzle heater shuts off but the bed stays on"
(<https://forum.bambulab.com/t/is-a-print-pause-effectively-infinite/28695/5>). A third-party tool
page (<https://glama.ai/mcp/servers/codeofaxel/kiln/tools/pause_print>) says A1 models drop the
hotend target a few minutes into a pause while X1/P1 hold both targets; not checked against Bambu,
not about the X2D.

## 2. What goes wrong with pauses (reported)

**S14. Bambu forum, "Printer do not pause at the selected layer height".** FETCHED.
<https://forum.bambulab.com/t/printer-do-not-pause-at-the-selected-layer-height/71680>
A1 mini: "paused at layer 5 instead of layer 2". A reply points to a Bambu Studio 1.9.1.67 GitHub
issue, "Layer Pause Bug Gcode on the wrong layer with Scarf Seam enabled", reportedly fixed in
1.9.2. Not confirmed in the thread.

**S15. Bambu forum, "Pauses are no longer saved in project file".** FETCHED.
<https://forum.bambulab.com/t/pauses-are-no-longer-saved-in-project-file/221477>
"Closing and reopening a project now removes the pause". No version named, no official reply, no
fix. One user's color-change pauses do save.

**S16. Bambu forum, "Print not resuming after pause at layer".** FETCHED.
<https://forum.bambulab.com/t/print-not-resuming-after-pause-at-layer/77882>
"the hotend would stay in position on the print then not resume printing", leaving a blob. Not an
AMS printer, model not named. Worked around with custom G-code "Pause" instead of the built-in pause.

**S17. Bambu forum, "Filament leaking on pause resume".** FETCHED.
<https://forum.bambulab.com/t/filament-leaking-on-pause-resume/259189>
"Every time on resuming print after a Pause … the nozzle is not cleared properly". Suggested: change
the wiping roller; oozing "can be a strong indicator that your filament is wet". Model not named
(the link given is for the X1 wiper).

**S18. Bambu forum, "Bambu Studio adds a color change when pause added".** FETCHED.
<https://forum.bambulab.com/t/bambu-studio-adds-a-color-change-when-pause-added/12732>
X1 Carbon with AMS: a pause showed as a color change in the preview; the user later thought it was
"just an indicator" and a test print did not change color. No fix.

**S19. Prusa forum, "Pause print to insert hardware results in catastrophic failure".** FETCHED.
<https://forum.prusa3d.com/forum/english-forum-original-prusa-i3-mk3-5s-hardware-firmware-and-software-help/pause-print-to-insert-hardware-results-in-catastrophic-failure>
MK3 via OctoPrint: after a pause the print resumed cold ("started printing at 100c") and failed.
Cause was OctoPrint's setup. *Transfer:* we do not print through OctoPrint, so the cause does not
carry; the lesson that a resume can come back cold does.

**S20. Bambu forum, "Stop printing at layer height".** FETCHED.
<https://forum.bambulab.com/t/stop-printing-at-layer-height/18774>
Does not say whether the pause is before or after the layer. Confirms "The printer will stop the
print at the layer".

**S21. Bambu forum, topic 63822 (automatic pause at a height).** FETCHED.
<https://forum.bambulab.com/t/topic/63822>
"Move to the layer you want to stop at, right click the "+" slider, and click "Add Pause"". "You
will need to slice your model again after adding the pause".

**S22. Bambu forum, "Heat print nozzle during print job pause".** FETCHED.
<https://forum.bambulab.com/t/heat-print-nozzle-during-print-job-pause/109676>
A1 feature request; says nothing about what a pause does. Listed so the next reader does not
re-fetch it.

**S23. Search summaries on resume problems.** SNIPPET.
Prusa-forum users report a magnet jumping to "something magnetic" in the printhead, a resume that
went straight back into a pause, and a pause nobody noticed for minutes; a Qidi user saw a visible
line at the pause layer (query "OrcaSlicer pause at layer … magnet"; results included
<https://forum.prusa3d.com/forum/how-do-i-print-this-printing-help/pause-and-resume-without-visible-lines>
and <https://community.octoprint.org/t/can-i-pause-a-print-to-insert-magnets/14465>). Not Bambu.

## 3. Embedding a part: depth, clearance, covering

**S24. Bambu forum, "How to embed a nut within a print".** FETCHED.
<https://forum.bambulab.com/t/how-to-embed-a-nut-within-a-print/226107>
RocketSled: "set the nut a little deeper in the pocket", so the nozzle bridges over without touching
it. Avarax: "the printer was printing into empty space between the nut and its layer"; fixed with a
bridge method (0.6 nozzle, 0.3 layers). Untested ideas: print infill first; glue stick on the nut.

**S25. hex-3d-gon, "strength-007" lesson.** FETCHED.
<https://hex-3d-gon.pages.dev/lessons/strength-007>
At the pause "ensure it sits below the next layer height (no proud edges)"; check "for nozzle
collision, shifting hardware, or poor bridging over the pocket". Slide-in pockets "+0.2 to +0.4 mm on
FDM" (not said whether per side). For bearings, support the outer race with a shoulder. A site of
unknown authority.

**S26. Hackaday, "Use a gap-cap to embed hardware in your next 3D print", 2026-03-27.** FETCHED.
<https://hackaday.com/2026/03/27/use-a-gap-cap-to-embed-hardware-in-your-next-3d-print/>
A pre-printed lid placed over the part at the pause gives the next layers "a smooth and flat
surface". No dimensions.

**S27. Instructables, "Captive nuts and more in 3D printing".** FETCHED, but the page body came back
empty (title only). <https://www.instructables.com/CAPTIVE-NUTS-AND-MORE-IN-3D-PRINTING> Nothing used.

**S28. Search summaries on bearings in prints.** SNIPPET.
Query "embed 608 bearing pause print fidget spinner pocket clearance". Fidget spinners press 608s in
**after** printing; one designer says printed-in-place bearings need "at least 0.2mm clearance";
another found a bearing hole too loose and suggests a light press fit. Query "embed bearing mid
print pause pocket depth": a Reddit idea, a bigger pocket with a 60° chamfer just above the part.
No source found that drops a ball bearing in mid-print and prints over it. That is "none of the
pages these two queries returned", not "no one does it".

## 4. Bearings

**S29. NSK 688ZZ via Quality Bearings Online.** FETCHED.
<https://www.qualitybearingsonline.ca/688zz-nsk-miniature-deep-groove-8x16x5mm/>
Bore 8, outside 16, width 5 mm; "Two Metal Shields"; steel cage; ring material not given.

**S30. Henderson Bearings, 61704 / 6704 thin section, 20×27×4 mm.** FETCHED.
<https://www.hendersonbearings.co.uk/61704-6704-thin-section-ball-bearing-20x27x4mm.html>
Bore 20, outside 27, width 4 mm; steel. Shield type not stated on the page.

**S31. Simply Bearings, 6700ZZ.** SNIPPET this run (fetch returned 429); FETCHED by the 2026-10-27
pass, R6: 10×15×4 mm. <https://www.simplybearings.co.uk/products/6700-zz-eu>

**S32. 608ZZ, retailers.** SNIPPET. Kramp, Grobotronics, Onlinemetals and others give 8×22×7 mm,
shielded both sides (<https://kramp.com/shop-ro/en/p/deep-groove-ball-bearing-8x22x7mm-ina-fag--608ZZ>).
The SKF page came back empty and the NSK page 404.

**S33. MR128ZZ.** SNIPPET. Albeco lists 8×12×3.5 mm, also in stainless (SMR128)
(<https://www.albeco.com.pl/en/product/IUN/single-row-deep-groove-ball-bearing-miniature-mr128zz-ezo.html>);
Wych Bearings says its stock is chrome steel SAE 52100.

**S34. 6800ZZ.** SNIPPET. 10×19×5 mm, double shielded (NTN, Motion, an RS datasheet,
<https://docs.rs-online.com/2c8a/A700000015247544.pdf>).

**S35. 625ZZ.** SNIPPET. 5×16×5 mm (<https://olimex.com/Products/Robot-CNC-Parts/Bearings/625ZZ>).

**S36. 67xx series all 4 mm wide.** SNIPPET, from R6 (eBay):
6700 10×15, 6701 12×18, 6702 15×21, 6703 17×23, 6704 20×27, 6705 25×32. Only 6700 and 6704 are
backed by a fetched page.

**S37. Search on the X2D's pause behaviour.** SNIPPET. Query "Bambu Lab X2D pause print behavior
nozzle parked chamber heated": retailer and review pages only (for example
<https://all3dp.com/4/bambu-lab-x2d/>); one review says torque sensing lets the X2D pause on an
anomaly "in theory". Nothing on where it parks or what it heats during a user pause.

**Not covered by any source here:** how wide each race's flat face (the "land" plastic can press on)
is for any of these bearings; whether chrome steel rusts in a coaster that gets wet; whether the X2D
toolhead holds a magnet strong enough to pull a bearing.

## 5. Findings from our repo and bikar

**R1. The split-pocket coaster.** `src/Coasters/gBV_JTt3Kxk-split-pocket-coaster.bkr`: size 112.5
(range 80 to 125), height 4.4 (range 3.6 to 6), split at half height, neck 0.8, lip 0.4, air 0.4,
gap 0.25 (CAL-LSE-01), stud 2. Its halves print as separate pieces (`--piece Lower`, `--piece Upper`).

**R2. The 8-fold coaster.** `src/Coasters/7apC5Q9QS-8-coaster.bkr`: size 90 (range 40 to 120),
height 4 (range 1.4 to 16). `make coasters` (`Makefile`, target `coasters`) builds a 40 mm mini and a
90 mm standard from bikar's construction coasters.

**R3. pkt-1, the pocket coupon.** `docs/design/plates/pkt-1.md`: a piece printed in place inside its
pocket. One layer of air (0.2 mm) fused; two layers (0.4 mm) came out loose. That gap was horizontal
(air between stacked layers).

**R4. Our printer settings.** `tools/bambu/test/fixtures/minis-04/flattened-slice.project_settings.config`:
`"machine_pause_gcode": "M400 U1"`, printer model "Bambu Lab X2D", layer height 0.2, first layer
0.2, printable height 261. This is a fixture captured from a real slice, not a live read of the
printer.

**R5. The fidget-toy design.** `docs/design/pieces/fidget-toys-from-patterns.md`: 0.4 mm is the
least gap that prints apart, a bet on CAL-CLR-01 (`.claude/skills/calibrate/bets.md`: two surfaces
printed in place, 0.4 mm, provisional, coupon MC-8 not printed). The doc says pkt-1's horizontal
result "transfers only as a hint" to a vertical gap, because the two fill in differently. A
coaster-thick toy was ruled out there.

**R6. The earlier spinner study.** `docs/design/coaster/spinner-middle-design.md` with
`docs/research/2026-10-27-spinner-middle-research-a.md`, `…-research-b.md` and `…-check.md`. It asked
whether the split flange coaster's middle piece could turn. It found: bearings need a coaster about
5.2 to 6 mm tall; a 6704 cuts into the kites of that pattern; the halves are separate prints, so a
bearing can go in when the coaster is closed by hand, with no pause. Its gap bets were 0.10, 0.15
and 0.20 mm per face (CAL-FIT-01, CAL-LSE-01). CAL-HOL-01 notes a round hole prints smaller than
drawn, unmeasured.

**R7. How our tools call the slicer.** `tools/bambu/src/commands/slice.ts` builds the CLI call with
`--load-settings`, `--load-filaments`, `--arrange 1`, `--slice <plate>` and `--export-3mf`.
`tools/bambu/src/commands/coaster.ts` calls it with
`--debug 2 --load-settings … --slice 0 <3mf> --outputdir …`. Neither passes `load_custom_gcodes`.

**R8. How our tools build the 3MF.** `tools/bambu/src/threemf-assemble.ts` writes the input 3MF for
colored plates. It writes no `custom_gcode_per_layer.xml`. So today no tool path of ours can put a
pause in a slice; it would have to be added in the GUI, or taught to the tools (S4 or S5).

**R9. The printer tools already know the paused state.** `tools/bambu/src/backends/mqtt.ts` builds
pause, resume and stop commands; `tools/bambu/src/commands/print.ts` keeps them owner-gated;
`tools/bambu/src/send-gate.ts` and `tools/bambu/src/actuals.ts` treat `PAUSE` as a print state;
`tools/bambu/src/plate-type.ts` notes the X2D pauses itself with HMS 0500-8051 on a plate mismatch.
So the monitor-print watcher can see a pause; no new state is needed.

**R10. bikar.** A grep of bikar's `packages/core/src` at origin/main fe6b109e for "bearing" finds the
word only as an angle (a direction) in `coaster.ts` and as "load-bearing" in `coaster-split.ts`;
"pause" finds animation code only. bikar has no bearing pocket, no print-in-place hub, and no notion
of a pause layer. It does have closed pockets, loose pieces, necks and lips (R1, R3), which are the
nearest parts to build on.

## 6. What this pass takes as settled, and what stays open

Settled by source: the pause runs before the chosen layer prints (S2, matching S9, S10); a pause is
lost in print-by-object mode (S2, S8); the pause is stored in the 3MF as
`Metadata/custom_gcode_per_layer.xml` or passed to the CLI as JSON (S4, S5); on our printer it is
`M400 U1` (R4); the firmware decides where the head parks (S12, a user, P1S).

Open, each needing our own print or a read of our own sliced file: what the X2D does while paused
(park spot, heaters, Z moves); whether a bearing seated 0.2 mm below the next layer stays clear of
the nozzle; whether a first layer over a recessed steel race holds; the race land widths; whether the
pause survives our own slicing path; whether chrome steel rusts in use.
