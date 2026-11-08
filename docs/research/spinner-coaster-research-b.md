---
date: 2026-11-08
produced-by: researcher B agent (Claude Opus 5.5), one of two independent passes; web pages opened with WebFetch, the rest seen only as WebSearch summaries, each marked below; repo, bikar and the installed Bambu Studio read from disk, nothing printed or sent
feeds:
  - docs/design/pieces/spinner-coaster-design.md
  - docs/design/pieces/spinner-coaster-design-b.md
---

# A spinner coaster with a bearing dropped in mid-print: raw findings (researcher B)

**The ask** (Omar, 2026-11-08): "creating a spinner version of our coaster that we've been making in
full where the print maybe stops halfway and then we put in a spinning bearing, and then we resume
the print ... design it ... and create design.md with potentially the technique to stop the print
midway and then resume it after it's been inserted."

How to read this file. Every web source says whether I **fetched** the page (read its text) or only
saw a **snippet** (a search engine's summary, which can be wrong or out of date). A snippet carries
no weight on its own. Every repo or machine fact names the file it came from. Quotes are verbatim
where marked with quote marks; everything else is my summary.

Nothing was printed, sliced or sent to the printer for this file.

## 1. On our own machine: what the pause is

| # | What | Where | What it says |
|---|---|---|---|
| L1 | The pause G-code Bambu Studio writes for an "Add Pause" | `/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/machine/fdm_bbl_3dp_002_common.json`, line 389, Bambu Studio 02.08.02.61 (read from the app's `Info.plist`) | `"machine_pause_gcode": "M400 U1"` |
| L2 | That the X2D inherits it | `Bambu Lab X2D 0.4 nozzle.json` in the same folder, line 4 | `"inherits": "fdm_bbl_3dp_002_common"`; the X2D files do not override `machine_pause_gcode` |
| L3 | That a real X2D slice of ours carries it | `tools/bambu/test/fixtures/minis-04/flattened-slice.project_settings.config` lines 1152 and 1388 | `"machine_pause_gcode": "M400 U1"` beside `"printer_model": "Bambu Lab X2D"` |
| L4 | Our slice settings in that fixture | same file | `layer_height` 0.2, `initial_layer_print_height` 0.2, `wall_loops` 2, `top_shell_layers` 5, `bottom_shell_layers` 3, `sparse_infill_density` 15%, `ironing_type` "no ironing" |
| L5 | The X2D nozzle | `Bambu Lab X2D 0.4 nozzle.json` line 432 onward | `"nozzle_type": ["hardened_steel", ...]` for every entry |
| L6 | The X2D's head clearance and height | same file, lines 37 to 39 and 151 | `extruder_clearance_height_to_rod` 32.8, `extruder_clearance_height_to_lid` 133, `printable_height` 261 |
| L7 | Our tooling can pause and resume a running print by hand | `tools/bambu/src/backends/mqtt.ts` lines 168 to 169 and 348 to 349; `tools/bambu/README.md` line 73 | `buildPrintControlCommand("pause" \| "resume" \| "stop")`; "`pause`/`resume` are reversible and immediate." Nothing in `tools/bambu/` writes a pause into a plate: a grep for `custom_gcode`, `M400` and `pause` in `tools/bambu/src` and `tools/bambu/presets` finds only the hand control and status words. |
| L8 | The printer reports a paused state we already log | `tools/bambu/src/timed-prints.ts` line 36 | `paused` and `resumed` are in the set of states that break a timed run |

What L1 to L3 do **not** tell us: what the X2D's firmware does when it reaches `M400 U1` (where the
head goes, which heaters stay on, for how long). That is inside the firmware, and I found no
official or X2D-specific page on it (section 2).

## 2. The web: pausing on Bambu printers

None of the sources in this section is official Bambu Lab documentation, and none names the X2D.
Searches for a Bambu wiki page on pausing, and for X2D pause behaviour, returned no such page
(three searches, listed in section 6).

| # | Source | Fetched? | What it says |
|---|---|---|---|
| W1 | [Bambu forum, "Setting pause in Bambu studio"](https://forum.bambulab.com/t/setting-pause-in-bambu-studio/154801) | Fetched | How: "(right click on right hand slider select add pause)" (Obecny75). When: "It pauses at the start of layer 107." (JonRaymond), and for a cavity whose last layer is 107, the pause goes at 108: "Correct." So a pause set on layer N fires **before** layer N prints. |
| W2 | [Bambu forum, "Pause at layer?"](https://forum.bambulab.com/t/pause-at-layer/7025) | Fetched | "Right click on the layer slider will give you the option to add a pause." (NoobPrinter). jules.wale embedded magnets this way: "this works well for the small parts I am making." weetartkneebiter lowered the bed from the screen and warned: "do not move the head manually as it could loose its location in the 3D space." the_Raz edited the machine pause G-code to drop the bed 100 mm and warned "you must not use this at a height of ~15 cm or more." No printer model named. |
| W3 | [Bambu forum, "Is a print 'Pause' effectively infinite?"](https://forum.bambulab.com/t/is-a-print-pause-effectively-infinite/28695) | Fetched | "Generally, the pause is as long as you want." (Wylaryzel). Against it: "I've definitely had a repeatable problem with longterm pauses actually restarting." (Level23). The asker planned to "leave the bed heated overnight". In the P-series category; no model named. Nothing on where the head parks. |
| W4 | [Bambu forum, "How to change the default pause settings?"](https://forum.bambulab.com/t/how-to-change-the-default-pause-settings/147603/6) | Fetched | "You can't change where the M400 U1 parks" (JonRaymond). His custom pause adds a move to the front and `G28 X Y ; Home the X and Y axes in case they were upset`. The thread notes the pause G-code applies only to pauses added when slicing, not to a pause pressed during a print. P-series category. |
| W5 | [Bambu forum, "Head collision during pause"](https://forum.bambulab.com/t/head-collision-during-pause/108306) | Fetched | P1S. During a pause TobakoLT moved the head by hand, it hit the frame, the belt slipped, and the print was scrapped: the head "could no longer align with the original print position". A cleaning routine tried later misaligned the second layer. |
| W6 | Search summary of [Bambu forum, "Bambu Studio adds a color change when pause added"](https://forum.bambulab.com/t/bambu-studio-adds-a-color-change-when-pause-added/12732) | Snippet | One user reports that adding a pause also changed the color for that layer and could not be turned off. Old thread; may be fixed. |
| W7 | Search summary of a MakerWorld model page (link in the search results, [makerworld 939048](https://makerworld.com/en/models/939048)) | Snippet | "if you print from Bambu Handy, you won't be able to program the pause". Not verified. |
| W8 | Search summary: one forum user, model not stated | Snippet | "on a pause, the nozzle heater shuts off but the bed stays on." |
| W9 | Search summary of a third-party tool page ([glama.ai kiln pause_print](https://glama.ai/mcp/servers/codeofaxel/kiln/tools/pause_print)) | Snippet | For the A1 and A1 mini, "the firmware drops the **hotend** target ~3-5 minutes into a pause regardless of slicer settings (bed target survives)". Not Bambu, not the X2D. |
| W10 | Search summary of a Bambu forum post | Snippet | `M400 U1` "parks toolhead at chute and pauses for user interaction". |

Read together, and with their hedges: on the Bambu printers these posters use, a slicer pause fires
before the chosen layer, parks the head somewhere the user cannot choose (one says the chute), can
last a long time (one poster saw long pauses restart on their own), and may turn the nozzle heater
off while keeping the bed warm (one forum report and one third-party page, neither for the X2D).
Moving the head by hand during a pause lost position in two fetched reports (W2, W5).

## 3. The web: embedding a part mid-print, in general

| # | Source | Fetched? | What it says |
|---|---|---|---|
| E1 | [Prusa help, "Insert pause or custom G-code at layer"](https://help.prusa3d.com/en/article/insert-pause-or-custom-g-code-at-layer_120490/) | Fetched | The pause is "inserted before the selected layer is printed". Its example message is about placing bearings in slots. Magnets must sit firmly or "they can get stuck to the print head as it passes over them"; use a tight slot or a drop of glue. For custom G-code: "Verify twice that you inserted the right G-codes", since some commands can move the nozzle into the bed. One commenter saw a layer-10 pause land in layer 11. |
| E2 | [Printago guide, magnet holes in Bambu Studio](https://printago.io/guides/bambu-studio-magnet-holes) | Fetched | Hole "diameter plus about 0.1 to 0.2 mm clearance, and height to the magnet thickness". Pause: "find the layer where the pocket gets capped and add a pause at that layer"; the pocket is sized so the magnet "sits just below a layer that will later cover it". "keep magnets away from the nozzle and any steel components while the head moves." |
| E3 | [Prusa forum, "Pausing print job to insert non 3D printed items"](https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-print-tips-archive/pausing-print-job-to-insert-non-3d-printed-items) | Fetched | A filament-change pause (`M600`) is "probably the best method" (PJR). Magnets "will want to stick to the print head and jam on the print" (david.b14); brass nozzles are not magnetic (Maxim). Pauses of "more than 12 hours" from an SD card reported (paraphrase of david.b14). |
| E4 | [Prusa forum, "Pause print (to insert hardware) results in catastrophic failure"](https://forum.prusa3d.com/forum/english-forum-original-prusa-i3-mk3-5s-hardware-firmware-and-software-help/pause-print-to-insert-hardware-results-in-catastrophic-failure) | Fetched | MK3.5S, nuts at layer 156. Resume was only possible through OctoPrint, the nozzle had cooled, "it started printing at 100c", and a 5-hour print was lost. A cold resume is a real failure. |
| E5 | Search summaries of Prusa and OctoPrint threads | Snippet | PETG oozes during a pause, which "can leave a weak first resumed layer"; one user had a blank screen and no extrusion after resuming over a nut. |
| E6 | Search summary of [hex-3d-gon lesson, captive nuts](https://hex-3d-gon.pages.dev/lessons/strength-007) | Snippet | Seat the hardware "below the next layer height" and watch for nozzle collision on resume. |
| E7 | Search summary of [Kingroon, embedding magnets](https://kingroon.com/blogs/3d-printing-guides/how-to-embed-magnets-into-3d-prints) | Snippet | Pause at the layer just above the top of the slot; 2 mm slot at 0.2 mm layers pauses at layer 11. |
| E8 | Search summary (no single page named) | Snippet | "adding an extra layer of about one layer height to the cavity ... to make up for sagging". |

Agreement across the fetched pages (E1, E2, W1): the pause goes on the **first layer that covers
the pocket**, because it fires before that layer prints, and the part's top must be **at or below**
the bottom of that layer. Nobody fetched gave a number for how far below. E8 (a snippet) is the only
source for an extra layer of depth.

## 4. The web: bearings

| # | Source | Fetched? | What it says |
|---|---|---|---|
| B1 | [bearingsdirect.com, 6704-2RS1](https://bearingsdirect.com/6704-2rs1-ball-bearing-20x27x4-sealed-61704-2rs1) | Fetched | 20 mm bore, 27 mm outside, 4 mm wide, "Rubber Seals on both sides", "Chrome Steel SAE-52100", "Now: $37.49" (an SKF-branded part; the high end). |
| B2 | [SKDIN, 6704](https://www.skdin.com/products/productid-6704) | Fetched | 20 × 27 × 4 mm; width tolerance "-0.120 mm to 0"; chrome steel rings and balls; open (no seals); $2.65 each. No shoulder diameters: drawings "will be launched soon". |
| B3 | [SKDIN, S6704](https://www.skdin.com/products/productid-S6704) | Fetched | Same sizes and tolerances in stainless steel, open; $2.65 each. |
| B4 | [SKDIN, S6705](https://www.skdin.com/products/productid-S6705) | Fetched | 25 × 32 × 4 mm, stainless rings, balls and cage; $3.43 each. |
| B5 | [TFL Bearing, F-6700 series (flanged)](https://tflbearing.com/?p=2953) | Fetched | F6704 20 × 27 × 4, F6705 25 × 32 × 4, F6706 30 × 37 × 4 (flanged parts; the plain 67xx share bore, outside and width). |
| B6 | [Simply Bearings, 6700ZZ](https://www.simplybearings.co.uk/products/6700-zz-eu) | Fetched on 2026-10-27 by the spinner-middle checker ([check §2](2026-10-27-spinner-middle-check.md#2-sources-re-opened)); not re-opened by me | 10 × 15 × 4 mm. |
| B7 | Search summaries of SKDIN 688ZZ, 625ZZ, Ezo, Zoro, NSK pages | Snippet | 688ZZ 8 × 16 × 5 mm (one SKDIN page says 8 × 16 × 4; most say 5); 625ZZ 5 × 16 × 5 mm. |
| B8 | Search summaries of Emerson, SKF (Rubix), Misumi pages | Snippet | 608 is 8 × 22 × 7 mm. One SKF datasheet mirror gives "D2 of 19.03 mm" for the 608, which would be the outer ring's inside shoulder: about 1.5 mm of flat steel ring face, less a 0.3 mm chamfer. |
| B9 | Search summaries of the "Vortex Fidget Spinner (Embedded Bearings)" listings ([MyMiniFactory](https://www.myminifactory.com/object/vortex-fidget-spinner-embedded-bearings-36890)) | Snippet; the page returned 403 to the fetcher | Four 608s dropped in while the print is paused "between 9.3mm-9.5mm Z height". A second spinner family pauses to press washers in: "they should be a tight fit". |
| B10 | Search summaries of 608 pocket fits (Printables 561588 comments, a Printables pillow block, Hackaday) | Snippet | "0.2 mm should work" against "0.2 clearance is for the 608 bearing clearly too loose", good at 0.12 mm; models ship Tight/Loose variants at ±0.05 mm; the fit is printer-dependent, so test a ladder. |
| B11 | [SCA Shinyei, AISI 440C](https://sca-shinyei.com/ballbearing/bearing_aisi440c) | Fetched 2026-10-27 by the checker ([check §2](2026-10-27-spinner-middle-check.md#2-sources-re-opened)); not re-opened by me | 440C stainless resists rust better than chrome steel but "may corrode". |
| B12 | Search summaries of spinning coasters on MakerWorld (a gyroscope beer coaster, a 608 spinner loaded from the bottom, a "hypnotic spinner") | Snippet | Turning coasters exist; none found pauses to embed a bearing in a coaster. That is "none of the few seen in one search", not "none exists". |

No source I opened gives the **shoulder diameters** of a 67xx bearing (how wide the flat face of
each ring is). They decide how much plastic can sit on the outer ring without touching the seal
or the inner ring. They have to be measured with calipers on the bearing we buy.

## 5. What we already have, in this repo and in bikar

| # | What | Where | What it means here |
|---|---|---|---|
| R1 | The full coaster is a height field: a flat bottom and one top surface | [coaster-design.md](../design/coaster/coaster-design.md), D-064 | A closed pocket (air with plastic above it) is two heights at one point, which the height field cannot say. A bearing pocket needs the split kernel or a separate tool. |
| R2 | Today's full coaster: a 4 mm slab, straps embossed 1.2 mm above it, 90 mm | `~/Workspace/git/bikar/patterns/Constructions/7apC5Q9QS-8-coaster.bkr` lines 7, 8 and 493 | `param size = 90 range 40..120`, `param height = 4 range 1.4..16`, `relief straps emboss 1.2`. So the coaster is about 5.2 mm thick at a strap, 4 mm between straps, and `height` may go to 16. |
| R3 | The split kernel already builds a closed pocket with a neck over it | `~/Workspace/git/bikar/packages/core/src/kernel3d/coaster-split.ts` around line 1222 (`pocket: 'neck over the pocket'`); bikar's `Split-Pocket-Coupon` (bikar #320) | The nearest thing to a bearing pocket we own. No bikar source file mentions a bearing, a pause or a magnet (grep of `packages/core/src` and `packages/cli/src`; the word "bearing" appears only as "load-bearing" and compass bearings). |
| R4 | Our own printed proof of air gaps on the X2D | [pkt-1](../design/plates/pkt-1.md), printed 2026-10-08 ([record](../prints/2026-10-09-pkt-1/index.md)) | "one layer of air fused in both pairs", "two layers loose with rims whole and bands level"; 0.4 mm necks survived; a 0.6 mm band printed over air stayed level. Two layers (0.4 mm) is the least air between two printed bodies that came apart. |
| R5 | A turning middle at 4.4 mm, ruled against a steel bearing | [spinner-middle-design.md](../design/coaster/spinner-middle-design.md#0-the-answer-in-one-screen) | "A steel bearing would spin, but not in this coaster ... a different, thicker product". Every bearing checked was 4 mm tall and needs a coaster about 5.2 to 6 mm. That doc is about the split flange coaster with loose pieces. This ask is that thicker product. |
| R6 | Steel in a wet coaster | [spinner-middle-design.md §4](../design/coaster/spinner-middle-design.md#4-living-with-a-mug) | Sealed and stainless is the cautious pick. |
| R7 | Bets already registered that fit this design | `.claude/skills/calibrate/bets.md` | CAL-HOL-01 (hole compensation), CAL-FIT-01 (fit ladder), CAL-CLR-01 (least gap printed in place), CAL-BRG-01 (bridge span), CAL-CST-03 (floor under a pocket), CAL-CST-05 (elephant's foot). No bet covers a pause or an insert. |
| R8 | Prior fidget work | [fidget-toys-from-patterns.md](../design/pieces/fidget-toys-from-patterns.md), [toys-1](../design/plates/toys-1.md) | Slide-out rings, nothing turns, no insert. Not a precedent for the bearing; a sibling toy. |
| R9 | Supports only outside, for orbs | [whole-orb-outside-supports-design.md](../design/orb/whole-orb-outside-supports-design.md) | About a closed hollow that must print over nothing. The only overlap here is the same rule of thumb: what prints over air must hold itself up. |
| R10 | The machine safety rule | memory "No measurement worth the machine" (2026-09-18) and guide-print gate 3 | A coupon that could damage the printer is never sent; a crash risk needs a guard or the option goes. |

## 6. Searches run (for the checker)

1. "Bambu Studio add pause at layer insert magnet nut wiki"
2. "embedding bearing mid-print pause fidget spinner captive 608 bearing print over"
3. "Bambu Lab X2D pause print nozzle park heatbed timeout paused how long"
4. "wiki.bambulab.com pause printing at specific layer Bambu Studio"
5. "Prusa knowledge base insert components magnets nuts pause print clearance"
6. "608 bearing dimensions 22 x 8 x 7 688 625 dimensions datasheet"
7. "\"M400 U1\" Bambu pause what does printer do head moves bed temperature"
8. "Bambu Lab wiki \"pause\" print resume nozzle temperature heatbed kept \"H2D\" OR \"X1\" OR \"X2D\" official"
9. "thin section bearing 6704 6705 6706 6804 dimensions ..."
10. "3D printed 608 bearing pocket hole diameter press fit 22.1 22.2 22.3 mm clearance PLA"
11. "embed hardware mid print pocket depth extra layer clearance over insert ..."
12. "Bambu Lab X2D specifications dual nozzle toolhead build volume heated chamber" (resellers only: 256 × 256 × 260 mm, heated chamber to 65 °C; consistent with L6)
13. "688ZZ bearing 8x16x5 625ZZ 5x16x5 6700ZZ 10x15x4 dimensions"
14. "spinning coaster 3D print bearing pause insert makerworld printables ..."

Pages that failed: MyMiniFactory (403), runsom.com bearing chart (timed out), Instructables
captive nuts (empty page to the fetcher).

## 7. What I could not find

- Anything official, or anything about the X2D, on what the printer does during `M400 U1`: where
  the head parks, whether the nozzle and bed stay hot, and whether there is a time limit.
- Whether a pause added in Bambu Studio survives our own send path (`bambu print send` builds and
  sends the plate's `.3mf`). Nothing in `tools/bambu/` handles a pause; untested.
- A measured spin time for a coaster-sized disc on a thin bearing.
- How PLA laid on a steel ring at about 220 °C behaves next to a rubber seal (does it touch,
  stick, or bind the seal). No source.
