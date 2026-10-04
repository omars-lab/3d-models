---
date: 2026-10-04
produced-by: a web-research subagent (Claude Opus 5.5), web pages plus GitHub source reads, for the split-with-studs design; regrouped under these headings by the design's author, quotes unchanged
feeds: docs/design/pieces/split-with-studs-design.md
---

# Research: cutting a print in half and joining it back with studs

**How to read this.** Every source is marked **FETCHED** (the page or file was downloaded and the
quoted part read) or **SNIPPET** (only a search-result snippet was seen; treat it as unverified).
Of 38 numbered sources, 36 were fetched and 2 are snippets only (S9, S21). Two side claims are also
snippet only: the Cut_Tool.pdf version note under S7 and the 2.6 connector list under S4.

**The gap that matters most.** No measured, controlled study (a test matrix with more than one
sample and a stated method) turned up for any printed-fit number below. Every fit number is a
vendor rule of thumb, a hobby library's tuned constant or a forum anecdote, and none was measured on
a Bambu X2D. So any default the design picks is a `CAL-*` bet to print, not a cited fact.

The research agent's notes follow, grouped by topic. Text in quotation marks is verbatim from the
source.

## 1. Slicer cut tools

### Q1. PrusaSlicer cut tool connectors

#### S1. "Cut tool | Prusa Knowledge Base"

- URL: https://help.prusa3d.com/article/cut-tool_1779
- Status: FETCHED (curl, HTML stripped). No date shown; page tagged PrusaSlicer 2.9 / Legacy.
- Kind: vendor docs.
- Quotes:
  - "The standard connector is a circular prism plug, but you can choose between three different types of connectors"
  - "Plug: adds a plug to the side of the cut and subtracts the space for it from the other side"
  - "Dowel: subtracts the pin from both sides and generates an extra object to print as the connector"
  - "Snap: Adds a snap-fit connector on one side and subtracts the space to fit it on the other side"
  - "You can also choose the plugs' style, shape, depth size, and rotation. If you wish to change the side of the cut for the plug and snap connectors, click on Flip cut plane."
  - "The Dovetail mode creates a pin and a tail in a trapezoidal shape on the cut plane."
  - "it is possible to choose what happens to each new object: keep the current orientation, place the part where the cut was made down on the print surface, or flip the part upside down from the current orientation."
- Comment on the KB page by Prusa staff (Jan Kratochvíl), answering a user who asked what the Tolerance field next to Width and Depth does: "Yes, the tolerances are for better fit of the pins or dovetails."
- The KB gives **no default numbers**. The defaults below come from source code.

#### S2. PrusaSlicer source, tag version_2.9.2

- Files:
  - `src/slic3r/GUI/Gizmos/GLGizmoCut.hpp` and `.cpp`, at https://raw.githubusercontent.com/prusa3d/PrusaSlicer/version_2.9.2/src/slic3r/GUI/Gizmos/GLGizmoCut.hpp
  - `src/libslic3r/CutUtils.cpp`
- Status: FETCHED.
- Kind: vendor source code.
- Defaults in `GLGizmoCut.hpp`:
  - `m_connector_depth_ratio{ 3.f }`
  - `m_connector_size{ 2.5f }`
  - `m_connector_depth_ratio_tolerance{ 0.1f }`
  - `m_connector_size_tolerance{ 0.f }`
  - `m_snap_bulge_proportion{0.15f}`, `m_snap_space_proportion{0.3f}`
- The UI shows the values with the format `"%.2f mm"`, so depth 3 mm, size 2.5 mm, depth tolerance 0.1 mm, size tolerance 0 mm.
- Choices offered:
  - Styles: `{"Prism","Frustum"}`
  - Shapes: `{"Triangle","Square","Hexagon","Circle"}`
  - Part orientation labels: "Keep orientation" / "Place on cut" / "Flip upside down"
- Size is a diameter and the tolerance is split across the radius:
  - `connectors[idx].radius = 0.5f * m_connector_size`
  - `radius_tolerance = 0.5f * m_connector_size_tolerance`
  - So a size tolerance of T widens the hole's diameter by T.
- The tolerance slider maximum is 0.5 × mean_size.
- `CutUtils.cpp apply_tolerance()` applies the tolerance to the hole side:
  - `// make a "hole" wider: sf[X] += radius_tolerance`
  - `// make a "hole" dipper: sf[Z] += height_tolerance`
- Plug versus dowel:
  - For a **plug**, the upper part gets the negative volume with the tolerance applied, and the lower part's connector becomes a MODEL_PART (the plug itself). So by default the plug sits on the lower half and the hole on the upper half; "Flip cut plane" swaps them.
  - For a **dowel**, both halves get holes and a separate dowel object is created.

#### S3. PrusaSlicer source, current master

- File: `src/slic3r-shared/include/Slic3r/App/Plater/CutDialog.hpp` (plus `CutDialog.cpp`)
- Status: FETCHED.
- Kind: vendor source code.
- Same defaults as 2.9.2:
  - `connector_depth{3.}`, `connector_depth_tolerance{0.1}`
  - `connector_size{2.5}`, `connector_size_tolerance{0.}`
  - Type Plug, Style Prism, Shape Circle by default
- Groove (dovetail) tolerance maximum in `CutDialog.cpp`: `min(0.3 × groove.depth, 1.5)`.

#### S4. "PrusaSlicer 2.6 is here: organic supports, text embossing, new cut tool and more"

- URL: https://blog.prusa3d.com/prusaslicer-2-6-is-here-organic-supports-text-embossing-new-cut-tool-and-more_79322/
- Date: June 19, 2023.
- Status: FETCHED.
- Kind: vendor blog.
- Quote: "you can define various types of connectors. You can control the depth, size, and tolerances of each connector and the negative hole."
- SNIPPET only (unverified): connectors arrived in 2.6 with Plug and Dowel; Snap and Dovetail came later.

### Q2. Bambu Studio cut tool

#### S5. "Cut Tool | Bambu Lab Wiki"

- URL: https://wiki.bambulab.com/en/software/bambu-studio/cut-tool
- Status: FETCHED (urllib/curl; WebFetch gets HTTP 402). No date shown.
- Kind: vendor docs.
- Quotes on connectors and output:
  - "At present, the connectors that can be added are Plug, Dowel and Snap"
  - "Bambu studio supports cutting the model into multiple objects (default) or a multi-part object"
  - "You can also choose the orientation of the model after cutting by selecting Keep orientation, Place on cut and Flip"
- Quotes on dovetail mode:
  - Depth: "Controls how deep the dovetail joint extends into the model from the cutting surface. Increasing the value increases the depth of the joint, thereby enhancing grip and alignment strength."
  - Width: "Sets the width of the dovetail's base at the cutting plane. Wider joints may offer more surface area for contact, improving stability."
  - Flap angle: "It determines the outward angle of the dovetail's sides. Increasing the angle creates a more pronounced interlock, making the parts fit tightly. A smaller angle on the other results in a looser fit."
  - Groove angle: "This sets the inward angle of the matching groove that receives the dovetail. It affects how snugly the flap fits into the groove."
  - "After dovetail cutting, a pop-up window may appear to indicate that non-mainfold edges remain after cutting." (sic)

#### S6. Bambu Studio source, bambulab/BambuStudio master

- Files:
  - `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp` / `.cpp`
  - `src/libslic3r/CutUtils.hpp`
- Status: FETCHED.
- Kind: vendor source code.
- Defaults:
  - `CutUtils.hpp`: `const float CUT_TOLERANCE = 0.1f;`
  - `m_connector_depth_ratio{3.f}`, `m_connector_depth_ratio_tolerance{CUT_TOLERANCE}`
  - `m_connector_size{2.5f}`, `m_connector_size_tolerance{CUT_TOLERANCE}`
  - So the size tolerance defaults to **0.1 here, against 0 in Prusa and Orca**.
- UI label is "Depth ratio". Styles `{"Prizm","Frustum"}` (sic). Shapes `{"Triangle","Square","Hexagon","Circle"}`.
- `connectors[idx].radius = 0.5f * m_connector_size; connectors[idx].radius_tolerance = m_connector_size_tolerance;`
  - The tolerance is **not halved** here, unlike Prusa and Orca.
  - My inference, not verified by a print: if the same apply-to-radius logic runs downstream, the default 0.1 widens the hole's *diameter* by about 0.2 mm.
- Groove (dovetail) struct in `CutUtils.hpp`: `depth_tolerance{CUT_TOLERANCE}`, `width_tolerance{CUT_TOLERANCE}`.
- Groove defaults in `GLGizmoAdvancedCut.cpp` L2469–2472:
  - `depth_init = std::max(1.f, 0.5f * float(get_grabber_mean_size(m_bounding_box)))`, so it scales with the model's bounding box
  - `width_init = 4.0f * depth`
  - `flaps_angle_init = PI/3` (60°)
  - `angle_init = 0`
- Orientation checkboxes: "Keep orientation", "Place on cut", "Flip", plus a "Middle of geometry" option.

#### S7. "Bambu Studio 1.8.0 Public Beta"

- URL: https://forum.bambulab.com/t/bambu-studio-1-8-0-public-beta/35626
- Post by michaelrbrown, Nov 14 2023.
- Status: FETCHED.
- Kind: forum post quoting release notes.
- Quote: "Add connector function (snap and dovetail cutting, and improvements to flat cutting"
- SNIPPET only: a Bambu Shopify-hosted Cut_Tool.pdf says V1.7.7.89 already had Dowel connectors. Not verified, so the exact version that first added connectors is unconfirmed; the fetched evidence only shows Snap and Dovetail landing in 1.8.0.

#### S8. GitHub issue #11148, "Dowel generated by the cut feature don't have tolerances in the depth direction"

- URL: https://github.com/bambulab/BambuStudio/issues/11148
- Date: June 14 2026. Bambu Studio 2.7.1.57.
- Status: FETCHED.
- Kind: user bug report; labeled "not-bug".
- Reporter's settings: depth ratio 5.0 mm, tolerance 0.10 mm.
- Reporter's result: the connector came out 10.0 mm long, not the 9.8 they expected, and the hole 5.0 deep, not 5.1.
- Meaning: on a dowel the depth tolerance does not shorten the dowel.

#### S9. MakerWorld 2422160, "Plug, Dowel, Snap - Bambu Studio Cut Connectors"

- Status: SNIPPET only.
- Kind: community model page.
- Claims: Snap is for repeated assembly, Plug for a strong friction fit, Dowel for alignment before gluing. Unverified.

#### S10. "A Guide to Splitting and Printing Large Files in Bambu Studio" (Bambu Lab Wiki)

- URL: https://wiki.bambulab.com/en/bambu-studio/manual/3d-print-large-files
- Status: FETCHED. No date shown.
- Kind: vendor docs (tutorial written around an A1).
- Quotes:
  - "When enabled, Bambu Studio generates a set of male-female connectors, which are usually cylindrical pegs on one side and corresponding holes on the other. There are three options: Plug, Dowel, and Snap. Plug is the default option."
  - "Pegs or sockets can be too tight or too loose, due to clearance or inconsistent extrusion. To fix it, ensure you adjust the cut tolerance to **0.15–0.3 mm**. Also, recalibrate the flow rate on your A1. Sand tight pegs, or reprint with corrected tolerances."
  - "Pegs can sometimes snap or sockets crack while pushing the parts together due to their thin nature. To fix, print them with extra wall thickness."
  - "Lightly sand the pegs or holes using a file or sandpaper (start with 220 grit). Avoid forcing parts together. It may cause cracking or stress marks."
  - "For PLA, super glue is an ideal choice. For PETG or ABS, use a two-part epoxy for stronger adhesion."
  - "press the parts together firmly and hold them in place for 30–60 seconds"
  - "Supports form directly on connector areas or mating surfaces, ruining fit due to automatic support generation over flat cut faces."
- Note: the wiki recommends 0.15–0.3 mm while the shipped default is 0.1. The two disagree, and the wiki does not say whether its figure is per side or on diameter.

### Q3. Orca Slicer cut tool

#### S11. SoftFever/OrcaSlicer main

- Files: `src/slic3r/GUI/Gizmos/GLGizmoCut.hpp` / `.cpp`
- Status: FETCHED.
- Kind: vendor source code.
- Same as PrusaSlicer:
  - depth ratio 3, size 2.5, depth tolerance 0.1, size tolerance 0
  - `radius_tolerance = 0.5 × size tolerance`
  - Types Plug/Dowel/Snap; styles Prism/Frustum; shapes Triangle/Square/Hexagon/Circle
  - "Keep orientation" / "Place on cut" / "Flip upside down"
- It is a fork of the PrusaSlicer gizmo. I fetched no separate Orca wiki page, so I make no claim about Orca docs.

#### Orientation for a horizontal cut

This is my inference from the option definitions in S1, S5 and S11; nothing was printed.

- Upper part with "Place on cut": the cut face goes down on the bed.
- Lower part with "Keep orientation": the original bottom stays down and the cut face points up.
- "Flip upside down" rotates the part 180°.
- So each half can be laid either outer-face-down or cut-face-down, chosen per part.
- For studs on the cut face: whichever half carries the plug must have its cut face up (the plug is a vertical prism, so it prints with no support). The half with the holes can lie cut-face-down; the holes then open on the first layer, where elephant foot narrows them (see Q9).

## 2. LEGO stud dimensions

### Q4. LEGO dimensions

#### S12. Christoph Bartneck, "LEGO Brick Dimensions & Measurements" (drawing of the 2x4 brick, part 3001)

- URL: https://www.bartneck.de/wp-content/uploads/2019/04/lego-2x4-brick-dimensions-measurements-3001.pdf
- Drawing dated 27/03/2019.
- Status: FETCHED (PDF read).
- Kind: independent measured drawing. Not LEGO-official.
- Values (mm):

| Feature | Value |
|---|---|
| Stud diameter | Ø4.8 |
| Stud height | 1.7 in the section view, but 1.8 in the side view; both appear on the same drawing |
| Pitch | 8 |
| 2x4 outer size | 31.8 × 15.8 (0.1 per side gap) |
| Edge to first stud centre | 3.9 |
| Wall | 1.2 |
| Brick height | 9.6 |
| Top thickness | 1 |
| Inner cavity | 6.3 |
| Rib | .8 |
| Tube | Ø6.51 outer / Ø4.8 inner |
| Small detail | Ø2.6 |
| Detail dimensions | .2 and .6 |

#### S13. Zoe Blade, "Lego brick dimensions"

- URL: https://notebook.zoeblade.com/Lego_brick_dimensions.html
- Status: FETCHED. No date; cites 2021/2022 sources.
- Kind: independent notes.
- Built on a 1.6 mm unit: wall 1.6, ceiling 1.6, stud height 1.6, stud diameter 4.8, module 8 mm, plate 3.2 mm, brick 9.6 mm.
- Quote: "0.1 mm of wriggle room on each side".
- Note: the wall here (1.6) disagrees with S12 (1.2).

#### S14. Orionrobots, "Lego Specifications"

- URL: https://orionrobots.co.uk/Lego+Specifications
- Status: FETCHED.
- Kind: independent wiki, citing Steve Baker / Lugnet.
- Values: stud diameter **5**, stud height 1.7, spacing 8, plate 3.2, brick 9.6, wall 1.5, cylinder outer 6.31, cylinder wall 0.657. It also gives a pitch of 7.985 and a plate of 3.194.
- **Disagrees** with S12 and S13 on the stud diameter (5 against 4.8) and the tube outer diameter (6.31 against 6.51).

#### S15. cfinke, LEGO.scad

- URL: https://github.com/cfinke/LEGO.scad
- Status: FETCHED.
- Kind: hobby library.
- Values: `stud_diameter` 4.8, `stud_height` 1.8, `stud_spacing` 8, `wall_thickness_with_splines` 1.2, `wall_play` 0.1, `stud_play` 0.03.

#### Agreement across sources

- Stud pitch 8 and stud diameter 4.8: S12, S13 and S15 agree; S14 gives 5.
- Stud height: 1.6, 1.7 and 1.8 all appear, and S12 alone shows both 1.7 and 1.8.
- No LEGO-official dimension source was found. All four sources are independent measurements or compilations.

## 3. FDM pin and stud tolerances

### Carried from earlier research in this repo (not re-fetched in this pass)

Hydra Research's design rules, https://www.hydraresearch3d.com/design-rules, as recorded by two
earlier research files here:

- [hemisphere-split-survey.md](hemisphere-split-survey.md): "minimum printable hole Ø > 2 mm;
  minimum structural wall 0.9 mm (2× extrusion line width)"; "~0.2 mm for loose fit, ~0.1 mm for
  tight fit".
- [c2-assembly-grounding-audit.md](c2-assembly-grounding-audit.md) (fetched there, quoted
  verbatim): pin diameter "> ø1.8 mm (4 times extrusion line width)"; the 0.1 / 0.2 mm clearances
  are per side; a "~0.3 mm" chamfer on edges touching the print surface.

### Q5. Fit tolerances for FDM-printed LEGO-style studs

None of these is a controlled study. They are hobby libraries and blogs, each tuned on its author's printer.

#### S16. anandamous/OpenSCADLEGO README

- URL: https://github.com/anandamous/OpenSCADLEGO
- Status: FETCHED.
- Kind: hobby library with an author test log; one printer.
- Quotes:
  - "Stud Diameter 4.85 mm Slightly increased from the official 4.8 mm to improve PLA fit"
  - "Fit Tolerance 0.1 mm Subtracted from final dimensions..."
  - "Testing - Printing on the QIDI Q1 Pro with PLA"
  - "A final tolerance of 0.1 mm balanced ease of assembly with secure fit, lower values or none led to too tight connections, higher values produced loose connections."
  - "stud_rescale trials from 1.00 to 1.1; 1.05 delivered reliable results."
- Conditions: QIDI Q1 Pro, PLA. Nozzle and layer height not stated in what I read.

#### S17. cfinke LEGO.scad, source comments

- Status: FETCHED.
- Kind: hobby library; per-printer anecdotes left as comments.
- Quote: "If your printer prints the blocks correctly except for the stud diameter, use this variable to resize just the studs... A value of 1.05 will print the studs 105% wider"
- Example values from the comments:

| Setting | Printer and material |
|---|---|
| `stud_rescale = 1.03` | Creality Ender 3 Pro, PLA |
| `stud_rescale = 1.0475` | Orion Delta, T-Glase |
| `stud_rescale = 1.022` | Orion Delta, ABS |
| `wall_splines_rescale = 0.3` | Bambu Lab A1 Mini, PETG |

- Nozzle and layer height are not given.

#### S18. PELA-blocks `material.scad` (Paul Houghton)

- URL: https://github.com/paulirotta/PELA-blocks/blob/master/material.scad
- Status: FETCHED.
- Kind: hobby library.
- Quote: "These reference numbers are tested on Taz 6, Ultimaker 2+, Ultimaker 3 and Mass Portal ED printers"
- Per-material adjustments (top knob, bottom socket), in mm:

| Material | Top knob (stud) | Bottom socket |
|---|---|---|
| PLA | −0.08 | +0.04 (from `pla_m = ["PLA", false, -0.08, 0.04, 0.07]`) |
| ABS | −0.18 | +0.16 |
| PET | +0.04 | +0.10 |

- Quote: "Turn down the bed heater on low temperature materials like PLA. This helps avoid 'elephant foot' expansion of the bottom edges of sockets."

#### S19. Meshy blog, "Best Tolerances for 3D Printing LEGO-Compatible Bricks"

- URL: https://www.meshy.ai/blog/lego-compatible-3d-print-tolerances
- Author Zoey, June 29 2026.
- Status: FETCHED.
- Kind: vendor blog; no test method or data cited.
- Quotes:
  - "Stud outer diameter: 4.80 (nominal), 4.75–4.85 (FDM target range)"
  - "Anti-stud inner diameter: 4.80 (nominal), 4.90–5.00"
  - "A stud at 4.95 mm won't connect; one at 4.65 mm falls out under its own weight."
  - "Bambu Lab X1C / P1S: −0.10 to −0.15 mm"; "Bambu Lab A1: −0.10 to −0.12 mm" (XY contour compensation)
  - Hole compensation +0.05 to +0.10
  - "Layer height at 0.16 mm..."

#### S20. Printables models (read through the API)

- Status: FETCHED.
- Kind: community, no numbers.
- 433337 "LEGO Stud Tolerance Gauge" (2023-03-25): no numbers given.
- 113640 Duplo (Prusa i3 MK2S, Das Filament PLA, 200 µm): "Fits now perfectly printed with PLA with my printer". No numbers.
- 116754: "Using a raft is by far the easiest to get accurate dimensions, especially height."

#### S21. Thingiverse 1621890 (xmbrst)

- Status: SNIPPET only.
- Claim: "stud tolerances of -0.2 reported as giving good results on some printers". A Cura horizontal expansion of −0.04 worked for one user. Unverified.

#### The sources disagree on which way to adjust the stud

| Direction | Sources |
|---|---|
| Make the stud **bigger** | S15/S17 cfinke: ×1.022–1.05. S16 OpenSCADLEGO: 4.85 mm, ×1.05 |
| Make the stud **smaller** | S18 PELA PLA/ABS: −0.08 / −0.18. S19 Meshy: −0.10 to −0.15 contour compensation. S21 Thingiverse snippet: −0.2 |

Both camps say it depends on the printer, and the sign appears to depend on whether the printer over- or under-sizes outer contours. No source I fetched measured a Bambu X2D. The 0.1 mm per-side play in S13 and S15 is LEGO's own molded clearance, a design value; it is not evidence about how printed studs fit.

### Q6. Pin and dowel clearance (press, slip, loose)

#### S22. Creative3DP, "Press-Fit Tolerances for 3D Printing: Numbers That Survive Contact With Reality"

- URL: https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/
- Date: July 10 2026.
- Status: FETCHED (curl).
- Kind: vendor/independent blog; cites Markforged, Prusa and AON3D, plus "community measurements".
- Diametral table, scoped "for rigid filaments (PLA, PETG, ABS) in the 5–25mm range":

| Fit | Diametral allowance |
|---|---|
| Press | −0.10 |
| Snug | +0.05 |
| Close running | +0.15 |
| Free | +0.35 |

- Quotes:
  - "printed hole comes out 0.1–0.3mm undersize"
  - "~0.24mm undersize for a 5mm hole in PLA on a 0.4mm nozzle"
  - "printed shaft comes out ~0.1mm oversize (community measurements run 0.1–0.2mm)"
  - "Markforged's printed unit tests found ~0.05mm of interference 'just right'... community engineering guides land at −0.1 to −0.2mm interference for desktop FDM; Prusa's design guidelines call for 'at least 0.3mm' of modeled clearance on anything that must move"
  - Crush ribs "~0.2mm proud" (citing AON3D)
  - "A PLA press fit under constant stress relaxes over months... add a mechanical backup — a shoulder, a groove and snap ring, a drop of CA"
  - "Put the precision on the shaft."
- Note: the table is scoped to 5–25 mm. Small studs (about 2.5–5 mm) fall at or below its lower bound. The scope does not carry to small studs without saying so (K10).

#### S23. Sovol blog, "FDM 3D Printing Tolerances & Clearances: How to Design Parts That Fit"

- URL: https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit
- Author Cathy Lim, Aug 26 2026.
- Status: FETCHED.
- Kind: vendor blog; rules of thumb, **per side**.
- Values:
  - Press 0.05–0.15, sliding 0.2–0.3, snap 0.3+, print-in-place about 0.3–0.4 total.
  - Per side by material: PLA 0.15–0.25, PETG 0.2–0.3, ASA 0.25–0.35.
  - Desktop FDM accuracy: "roughly ±0.2 to ±0.5 mm in practice".

#### S24. Prusa forum, "General tolerances for part design"

- URL: https://forum.prusa3d.com/forum/original-prusa-i3-mk2-s-others-archive/general-tolerances-for-part-design/
- Date: 05/10/2016.
- Status: FETCHED.
- Kind: forum anecdotes, MK2-era.
- PJR (moderator): "I generally use a 0.2mm difference to get a reasonable fit; I guess 0.15 would be tight and 0.3mm loose."
- gz1: "for D above 3mm, I usually add 0.2mm for a 'normal' fit."

#### S25. Prusa KB, "Modeling with 3D printing in mind"

- URL: https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
- Status: FETCHED. No date shown.
- Kind: vendor docs.
- Quotes:
  - "You will probably not be able to slot together two parts with zero-tolerance dimensions. You may have to tweak the tolerances until you reach an optimal result. There's no single 'universal' value"
  - "An Original Prusa will be accurate to at least 0.2 mm, but you also need to remember that different materials can warp or shrink during printing."
  - "Consider if two parts should move, like a hinge, or lock/snap together with a friction fit. An initial good measurement for movable parts is at least 0.3 mm."
  - "Using a chamfer on the edges of two parts that slot together can save you a lot of effort when assembling."
  - On splitting and gluing, see Q7.

#### S26. BOSL2 `$slop` (constants.scad wiki)

- URL: https://github.com/BelfrySCAD/BOSL2/wiki/constants.scad (fetched as raw markdown)
- Status: FETCHED.
- Kind: hobby library documentation.
- Quotes:
  - "`$slop` ... `0.0` by default."
  - "Your own part libraries should add a single `$slop` to every mating surface. For holes, increase the hole radius by get_slop() or diameter by 2*get_slop()."
  - "For smaller 3d-printed holes, `$slop` becomes inaccurate and varies based on printing orientation." (cites BOSL2 issue #1679)
  - "the ideal value for a large square peg and socket may not be the same as a small cylinder and hole"
  - Calibration example: "`$slop = 0.15;`". The calibration part steps in 0.05 increments.

#### S27. Bambu wiki, "XY Hole / Contour compensation"

- URL: https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation
- Status: FETCHED.
- Kind: vendor docs.
- Quotes:
  - "XY Hole Compensation: Adjusts the size of holes (closed, hollow areas) in each layer. It only affects holes and does not change the outer size of the model."
  - "The hole diameter will increase by twice the compensation value"
  - Worked example: "In this case, + 0.15"
  - "Hole diameters close to the Nozzle size, holes below 1 mm can be challenging to tune."
  - "X-Y Hole Compensation only applies to closed paths."
- The shipped defaults are 0, from `resources/profiles/BBL/process/fdm_process_common.json` (FETCHED): `"xy_hole_compensation": "0"`, `"xy_contour_compensation": "0"`. Neither the X2D 0.20 mm process profile nor its parent overrides them.

### Q10. Small pins, filament pins, steel dowels, horizontal holes

#### S34 again (Hubs), FETCHED

- "Smaller diameter pins (less than 5mm diameter) can be made up of only perimeter prints with no infill. This creates a discontinuity... weak connection susceptible to breaking."
- "For critical pins smaller than 5mm in diameter, an off-the-shelf pin inserted into a printed hole may be the optimal solution."
- "If your design contains pins smaller than 5mm in diameter, add a small fillet at the base of the pin."
- "FDM often prints undersized vertical-axis holes"
- The guide also suggests "Splitting a model, reorienting holes..."

#### S27 again (Bambu XY compensation), FETCHED

- "Hole diameters close to the Nozzle size, holes below 1 mm can be challenging to tune."

#### S10 again, FETCHED

- "Pegs can sometimes snap ... due to their thin nature. To fix, print them with extra wall thickness."

#### S35. Prusament home page

- URL: https://prusament.com/
- Status: FETCHED.
- Kind: vendor marketing.
- Quotes:
  - "We believe the industry standard of 0.05 mm isn't sufficient. We guarantee ±0.02mm precision for the vast majority of materials"
- Relevance: if 1.75 mm filament is used as a pin, its diameter is held to about ±0.02 mm (Prusament) to ±0.05 mm (the "industry standard" Prusa claims). That is much tighter than a printed pin.
- **Gap:** I found no fetched source that uses or tests filament as an alignment pin. That idea remains unsourced.

#### S36. BOSL2 `teardrop()` (shapes3d.scad wiki)

- URL: https://github.com/BelfrySCAD/BOSL2/wiki/shapes3d.scad (fetched as raw markdown)
- Status: FETCHED.
- Kind: hobby library documentation.
- Quotes:
  - "Makes a teardrop extrusion along the Y axis, which is useful for 3D printable holes."
  - "`ang` — Angle of hat walls from the Z axis. Default: 45 degrees"
  - "`cap_h` — If given, height above center where the shape will be truncated."
- Relevance: horizontal holes (axis parallel to the bed) need a teardrop or a flat-capped top to print without support. Vertical holes, which is what a horizontal cut produces for studs, do not.

#### Steel dowels

- No fetched source gives a hole size for a press-fit steel dowel in an FDM print.
- S34 says only "an off-the-shelf pin inserted into a printed hole may be the optimal solution."
- S22's press-fit −0.10 mm diametral row would apply, but only within its stated 5–25 mm scope.

## 4. Glue or press fit

### Q7. Glue versus press fit, and pins for alignment versus strength

#### S10 again (Bambu large-file guide), FETCHED

- "For PLA, super glue is an ideal choice. For PETG or ABS, use a two-part epoxy for stronger adhesion."
- "Before applying any adhesive, try to fit all the pieces using the connectors added during the splitting process."
- This guide treats connectors as alignment and a dry fit before gluing, not as the thing that holds the parts together.

#### S28. Bambu wiki, "Work After Printing Finished (removing, cleaning, bonding the prints...)"

- URL: https://wiki.bambulab.com/en/filament-acc/acc/print-finish-adv
- Status: FETCHED.
- Kind: vendor docs.
- Quotes:
  - "Standard filaments (such as PLA and PETG), when the bond strength requirement is not high: You can use common 'super glue' ('502', a kind of acrylic glue). However, this glue has poor cold and durability resistance; it will crack and lose bond strength in cold environments or after long-term use."
  - "When the bond strength requirement is high: For most filaments, you can try AB glue (a kind of epoxy glue) or TPU-type shoe repair glue."

#### S25 again (Prusa KB "Modeling with 3D printing in mind"), FETCHED

- "When you glue the parts of your object together, make sure that the surfaces to be glued are smooth and free of grease or dirt, to achieve an invisible seam. The ironing feature in PrusaSlicer can also assist in this. Also, it can be helpful to lightly sand the surface to increase adhesion."
- "Superglue can be very viscous, so it may not be ideal for rough surfaces. It can also leave traces of itself."
- "When you find the right glue for your model and material, the seam should be stronger than the rest of the material, but you might want to model in some pegs for alignment and strength."

#### S22 again (Creative3DP), FETCHED

- A PLA press fit relaxes over months under constant stress, so "add a mechanical backup ... a drop of CA".

#### Not found

- No measured CA-on-PLA lap-shear number from a fetched source.
- No measured comparison of how strong a pinned joint is against a glued one.
- The vendor docs line up as: connectors align, glue holds; CA is fine when low strength is needed (with Bambu's warning about cold and age); epoxy for strength.

## 5. Build plates and the face they leave

### Q8. Build plate surfaces and the X2D

#### S29. Bambu wiki, "Introduction to Bambu Lab Build Plates"

- URL: https://wiki.bambulab.com/en/filament-acc/acc/plates
- Status: FETCHED.
- Kind: vendor docs.
- Textured PEI:
  - "It is the standard plate included with Bambu lab printers."
  - "Special textured surface: Adds a unique textured finish to the bottom surface of printed parts."
  - 256*256 mm size lists "X2D / P2S / P1 Series / X1 Series / A1".
- Smooth PEI:
  - "The Smooth PEI Plate provides a flat surface for printed objects and is suitable for scenarios that require a level bottom surface."
  - "Smooth and Matte Surface Finish ... impart a smooth and matte texture to the bottom surface"
  - "High Z-axis Precision Printing ... an excellent choice for printing parts that demand a high level of fit accuracy, where precise alignment and tight tolerances are crucial."
  - "Only PLA filament does not require glue, while printing with other filaments requires the use of gluing to prevent the PEI sheet from tearing."
- Dual-Texture PEI: "allowing the model's bottom surface to have either a matte or smooth finish".
- Engineering Plate: "providing printed parts with a smoother, nearly glossy bottom finish". Also: "Before printing with any filament, apply glue on the Engineering Plate."
- Cool Plate SuperTack:
  - "a finely textured surface that approaches a smooth, glossy finish"
  - "This plate is designed only for printing PLA and PETG"
  - "Even at a low bed temperature of just 40 °C, PLA prints adhere firmly to the plate"
  - Lower bed temperature "helps effectively reduce warping and surface defects such as 'elephant foot'"
- Plate generations:
  - "Second-generation plates are compatible with the P2S/X2D printer. The main difference lies in the updated QR code identification."
  - "P2S/X2D printers can physically use first-generation build plates, but the plate type will not be automatically recognized."

#### S30. Bambu wiki, X2D "Accessories in the box"

- URL: https://wiki.bambulab.com/en/x2d/manual/acc-in-the-box
- Status: FETCHED.
- Kind: vendor docs.
- Quotes:
  - "Build plate (pre-installed on the heatbed)"
  - "Bambu Textured PEI Plate — Comes pre-installed on the heatbed for printing, with both sides available for use."
- So the X2D ships with Textured PEI only. Smooth PEI, SuperTack and Engineering are separate purchases (my reading of S29 plus S30).

#### What this means for a mating face

My inference, not measured: a half printed with its cut face down on the stock Textured PEI gets a textured mating face. That roughness adds to the seam gap and to how visible the seam is. A cut face printed facing up gets a top-surface finish instead (ironing is possible, S25). No source measured the seam gap that a textured face adds.

## 6. Elephant's foot

### Q9. Elephant's foot

#### S31. Bambu wiki, "Elephant foot compensation"

- URL: https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot
- Status: FETCHED.
- Kind: vendor docs.
- Quotes:
  - "On tolerance-critical parts such as assemblies, snaps, rails, and shaft holes, the flared base directly affects fit. When the first-layer elephant foot is large, assembly becomes less smooth and may fail completely."
  - "the slicer intentionally shrinks the first-layer contour"
  - Setting path: "Process → Quality → Precision → Elephant foot compensation"
  - The comparison image is labelled "0.2 mm".
  - Worked measurement example: "X-axis elephant foot deviation: 25.07 − 24.98 = 0.09; Y-axis elephant foot deviation: 25.11 − 25.00 = 0.11 ... (0.09 + 0.11) / 2 = 0.10". This is one illustrative example, not a survey.
  - "The elephant foot compensation value can vary between different types of build plates, so values are not interchangeable. After changing the build plate, measure and calculate the compensation value again."

#### S32. BambuStudio profiles (master)

- Status: FETCHED.
- Kind: vendor source and config.
- `resources/profiles/BBL/process/0.20mm Standard @BBL X2D.json` inherits `fdm_process_dual_0.20_nozzle_0.4`, which sets `"elefant_foot_compensation": "0.15"`. The X2D 0.4 mm standard profile therefore ships with **0.15 mm**.
- Other values found by `gh search code`:
  - `fdm_process_common`: 0
  - `fdm_process_single_0.xx` (X1/P1 family): 0.15
  - A1 profiles: 0.075
  - A1 mini: 0
- `ConfigManipulation.cpp` resets values above 1 to 0.

#### S33. Prusa KB, "Elephant foot compensation"

- URL: https://help.prusa3d.com/article/elephant-foot-compensation_114487
- Status: FETCHED.
- Kind: vendor docs.
- Quotes:
  - "the first layer is squished... usually a bit wider than it should be"
  - "will scale/shrink the first layer"
  - "Values around 0.2 mm usually work well for the default 0.4 mm nozzle"
  - "Official Prusa profiles have this setting turned on by default"

#### S34. Hubs (Protolabs Network), "How to design parts for FDM 3D printing"

- URL: https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
- Status: FETCHED. No date.
- Kind: vendor docs.
- Quotes:
  - Elephant's foot: "Protruding outside the specified dimensions, this flare can impact the ability to assemble FDM parts."
  - "Include a 45° degree chamfer or radius on all edges of an FDM part touching the build plate."

#### S18 again (PELA), FETCHED

- Turning the bed down for PLA "helps avoid 'elephant foot' expansion of the bottom edges of sockets".

#### What this means for a mating face

Inference from S31–S34:

- A socket half printed cut-face-down has its holes start on layer 1, where the flare narrows them.
- Compensation shrinks the outer contour of the first layer. I have not verified whether it also opens holes on the first layer; the wiki does not say.
- A chamfer at the mouth of each hole (S34, S25) is the documented geometric fix.

## 7. Other joints

### Q11. Alternatives: dovetails, rails, jigsaws, snap pins

#### S37. BOSL2 `partitions.scad` (wiki)

- URL: https://github.com/BelfrySCAD/BOSL2/wiki/partitions.scad
- Status: FETCHED.
- Kind: hobby library documentation.
- Quotes:
  - `partition()`: "Partitions an object into two parts, spread apart a small distance, with matched joining edges."
  - `cutpath`: "Standard named paths are 'flat', 'sawtooth', 'sinewave', 'comb', 'finger', 'dovetail', 'hammerhead', and 'jigsaw'." Default "jigsaw".
  - `cutsize` default 10.
  - `$slop`: "Extra gap to leave to correct for printer-specific fitting."
- Relevance: this is a cut that joins *in the plane of the cut* (a jigsaw edge), an alternative to studs that stick out of the cut face.

#### S38. BOSL2 `joiners.scad` (wiki)

- URL: https://github.com/BelfrySCAD/BOSL2/wiki/joiners.scad
- Status: FETCHED.
- Kind: hobby library documentation.
- `dovetail()`:
  - "To adjust the fit, use the $slop variable, which increases the depth and width of the female part of the joint to allow a clearance gap of $slop on each of the three sides."
  - "`slope` — Standard woodworking slopes are 4, 6, or 8. Default: 6."
  - "Adding a chamfer helps printed parts fit together without problems at the corners."
- `snap_pin()`:
  - "`clearance` — how far to shrink the pin away from the socket walls. Default: 0.2"
  - "`preload` ... Default: 0.2"
  - "The default orientation (FRONT) and anchor (FRONT) places the pin in a printable configuration, flat side down on the xy plane." So snap pins are printed lying down, for strength.
- `rabbit_clip()`:
  - "`compression` ... Default: 0.1"
  - "`clearance` — extra space in the socket for easier insertion. Default: 0.1"
  - "Here are several sizes that work printed in PLA on a Prusa MK3, with default clearance of 0.1 and a depth of 5". This is the author's own test, one printer.
  - "make the socket with a larger depth than the clip (try 0.4 mm)"
- `half_joiner` / `joiner`: overhang angle default 30.
- `hirth()` face spline: tooth angle default 60.

#### S5 and S6 again (Bambu dovetail mode), FETCHED

- Depth, width, flap angle and groove angle, with the defaults from source in S6.

#### S1 and S3 again (Prusa dovetail mode), FETCHED

- Trapezoidal pin and tail. Groove tolerance capped at min(0.3 × depth, 1.5).

## 8. Where the sources disagree

1. **Default size tolerance differs.**
   - PrusaSlicer and Orca: size tolerance 0, and the hole's diameter grows by the tolerance (it is halved onto the radius).
   - Bambu: 0.1 added to the radius unhalved, which by my inference is about 0.2 on the diameter.
   - The Bambu wiki guide recommends 0.15–0.3 without saying per side or diametral.
2. **Which way to adjust the stud.** cfinke and OpenSCADLEGO make studs bigger (×1.02–1.05, 4.85 mm). PELA (PLA, ABS) and Meshy make them smaller (−0.08 to −0.15). See Q5.
3. **Per side or diametral.** Sovol is per side, Creative3DP is diametral, the Prusa forum is ambiguous ("0.2 mm difference"), BOSL2 `$slop` is per surface. Every number has to be labelled with which one it is before it can be compared.
4. **Scope of the numbers.** Creative3DP's table is scoped to 5–25 mm. Hubs warns that pins under 5 mm are weak. The slicer default connector is 2.5 mm, so it sits outside both.
5. **LEGO stud height** is given as 1.6, 1.7 or 1.8 depending on the source; the stud diameter is 4.8 everywhere except Orionrobots (5).
6. **No measured study** for any FDM fit number; no X2D-specific fit data; no CA-on-PLA strength number; no fetched source for a filament pin.

## 9. The load-bearing numbers

| # | Number | What it means | Source | Fetched? | Conditions / qualifiers |
|---|---|---|---|---|---|
| 1 | 2.5 mm | Default connector size (a diameter) | S2/S3 PrusaSlicer, S6 Bambu, S11 Orca source | FETCHED | All three slicers |
| 2 | 3 mm | Default connector depth (Bambu labels it "depth ratio") | S2/S3, S6, S11 source | FETCHED | All three slicers |
| 3 | 0.1 mm | Default depth tolerance | S2/S3, S6, S11 source | FETCHED | Hole made deeper; S8 says a dowel is not shortened |
| 4 | 0 mm | Default size tolerance | S2/S3 Prusa, S11 Orca source | FETCHED | Halved onto the radius, so the hole's diameter grows by T |
| 5 | 0.1 mm (CUT_TOLERANCE) | Default size tolerance | S6 Bambu source | FETCHED | Applied to the radius unhalved; about 0.2 on the diameter is my inference |
| 6 | 0.15–0.3 mm | Recommended cut tolerance if pegs are too tight or loose | S10 Bambu wiki large-file guide | FETCHED | Vendor tutorial (A1); per side or diametral not stated |
| 7 | 60°, width 4 × depth, depth ≥ 1 | Bambu dovetail defaults (flap angle, width, depth) | S6 source | FETCHED | Depth scales with the model's bounding box |
| 8 | min(0.3 × depth, 1.5) | Maximum groove tolerance in Prusa | S3 source | FETCHED | Prusa master |
| 9 | 1.8.0 (Nov 2023) | Bambu version that added Snap and Dovetail | S7 forum release post | FETCHED | Dowel in 1.7.7.89 is SNIPPET only |
| 10 | 4.8 mm | LEGO stud diameter | S12, S13, S15 | FETCHED | Independent sources; S14 says 5 |
| 11 | 8 mm | LEGO stud pitch | S12–S15 | FETCHED | S14 also gives 7.985 |
| 12 | 1.7 / 1.8 / 1.6 mm | LEGO stud height | S12 (1.7 and 1.8), S15 (1.8), S13 (1.6) | FETCHED | Sources disagree |
| 13 | 6.51 / 4.8 mm | LEGO tube outer / inner diameter | S12 | FETCHED | S14 gives 6.31 outer |
| 14 | 0.1 mm per side | LEGO molded play | S13, S15 (`wall_play`), S12 (31.8 vs 32) | FETCHED | Molded, not printed |
| 15 | 4.85 mm, 0.1 tolerance, ×1.05 | Printed-stud tuning | S16 OpenSCADLEGO | FETCHED | QIDI Q1 Pro, PLA; one author's test |
| 16 | ×1.022–1.0475 | Stud rescale per printer | S17 cfinke comments | FETCHED | Ender 3 Pro PLA 1.03; Orion Delta ABS 1.022, T-Glase 1.0475; anecdotes |
| 17 | −0.08 stud / +0.04 socket | PLA adjustment | S18 PELA | FETCHED | Taz 6, UM2+, UM3, Mass Portal; library constant |
| 18 | 4.75–4.85 stud, 4.90–5.00 socket | FDM target ranges | S19 Meshy blog | FETCHED | No test data cited |
| 19 | −0.2 | Stud tolerance that "works on some printers" | S21 Thingiverse | SNIPPET | Unverified |
| 20 | −0.10 / +0.05 / +0.15 / +0.35 diametral | Press / snug / close running / free | S22 Creative3DP | FETCHED | Rigid filaments, 5–25 mm only; blog |
| 21 | 0.1–0.3 mm (≈0.24 at 5 mm) | Printed holes come out undersize | S22 | FETCHED | PLA, 0.4 nozzle; "community measurements" |
| 22 | ~0.1 (0.1–0.2) mm | Printed shafts come out oversize | S22 | FETCHED | "community measurements" |
| 23 | 0.05–0.15 press, 0.2–0.3 slide per side | Fit classes | S23 Sovol | FETCHED | Per side; rules of thumb |
| 24 | 0.15–0.25 per side | PLA clearance | S23 Sovol | FETCHED | Rule of thumb |
| 25 | 0.2 normal, 0.15 tight, 0.3 loose | Fit by difference | S24 Prusa forum (PJR) | FETCHED | Forum anecdote, MK2 era, 2016 |
| 26 | ≥ 0.3 mm | Starting clearance for parts that move | S25 Prusa KB | FETCHED | Vendor docs; "at least" |
| 27 | 0.2 mm | Original Prusa accuracy ("at least") | S25 Prusa KB | FETCHED | Vendor claim |
| 28 | 0.2 / 0.1 / 0.1 mm | BOSL2 snap_pin clearance / rabbit_clip clearance / compression | S38 | FETCHED | rabbit_clip: "work printed in PLA on a Prusa MK3" |
| 29 | 0.15 mm | Example `$slop` | S26 BOSL2 | FETCHED | Calibration example; default is 0 |
| 30 | < 5 mm | Pins below this are perimeter-only and weak; use a bought pin | S34 Hubs | FETCHED | Vendor design guide |
| 31 | < 1 mm | Holes "challenging to tune" | S27 Bambu wiki | FETCHED | Vendor docs |
| 32 | 0 | Default XY hole and contour compensation | S27 / S32 profiles | FETCHED | BBL `fdm_process_common` |
| 33 | 0.15 mm | Default elephant-foot compensation on the X2D 0.4 nozzle, 0.20 mm profile | S32 profile | FETCHED | Via `fdm_process_dual_0.20_nozzle_0.4` |
| 34 | 0.075 / 0 | Elephant-foot default for A1 / A1 mini | S32 profiles | FETCHED | Shown for contrast |
| 35 | ~0.2 mm | Prusa elephant-foot value that "usually work[s] well" | S33 Prusa KB | FETCHED | 0.4 nozzle; "usually" |
| 36 | 0.09–0.11 (avg 0.10) | Example measured flare on a 25 mm cube | S31 Bambu wiki | FETCHED | One illustrative example; value is plate-dependent |
| 37 | 45° | Chamfer on edges that touch the bed | S34 Hubs | FETCHED | Vendor guide |
| 38 | 45° | Teardrop hat angle for horizontal holes | S36 BOSL2 | FETCHED | Library default |
| 39 | Textured PEI | Plate shipped with the X2D (both sides) | S30, S29 | FETCHED | Smooth PEI and others are extra |
| 40 | ±0.02 mm (vs 0.05 "industry standard") | Filament diameter tolerance | S35 Prusament | FETCHED | Vendor claim; "vast majority of materials" |
| 41 | 30–60 s | Hold time for super glue | S10 Bambu wiki | FETCHED | Vendor tutorial |
| 42 | — | CA "poor cold and durability resistance" | S28 Bambu wiki | FETCHED | Qualitative; no number |

Source count: 38 numbered sources (S1–S38). 36 FETCHED. 2 SNIPPET only: S9 and S21. Two side claims are also SNIPPET only: the Cut_Tool.pdf version note under S7, and the 2.6 connector list under S4.

## 10. How the search was run

WebSearch (the budget ran out at 200/200 partway through):

1. Bambu Studio cut tool connectors plug dowel snap dovetail wiki
2. LEGO dimensions stud diameter 4.8 mm pitch 8 mm stud height 1.7 tube outer diameter 6.51
3. Bambu Studio release notes cut tool connectors added version 1.7 dowel plug
4. PrusaSlicer 2.6 release notes cut tool connectors plug dowel snap dovetail 2.7
5. Bambu Studio 1.8 release note cut tool snap connector dovetail new
6. LEGO brick tube outer diameter 6.51 mm inner 4.8 wall thickness 1.2 mm dimensions
7. 3D printed lego compatible brick tolerance stud diameter 4.8 printed PLA fit clutch test
8. printables lego compatible tolerance test stud 4.8 4.85 4.9 bambu lab
9. OpenSCAD LEGO.scad stud_diameter tolerance 3D printing "stud" "4.85"
10. reddit 3D printed lego studs too tight 4.8mm what diameter worked PLA 0.4 nozzle
11. forum.bambulab.com lego compatible bricks tolerance studs fit X1C
12. cfinke LEGO.scad 3D printing stud tolerance "stud_diameter" README fit tighter
13. FDM design guide clearance press fit 0.1 mm sliding fit 0.2 mm loose fit hubs protolabs tolerances connecting parts
14. Prusa blog tolerances 3D printing press fit clearance 0.2 mm holes pins how to design
15. (Formlabs/Xometry tolerance query: blocked by the exhausted search budget)

Other lookups (no WebSearch):

- Bambu wiki GraphQL search for "build plate", which found the wiki page paths fetched below.
- `gh search code` on bambulab/BambuStudio, prusa3d/PrusaSlicer and SoftFever/OrcaSlicer for the cut-gizmo files and for `elefant_foot_compensation`.
- The Printables GraphQL API (`print(id){...}`) for model pages 433337, 113640 and 116754.
- Direct curl of known URLs: BOSL2 wiki (raw markdown), Prusa KB, Prusament, the Bambu wiki (through a urllib helper, because WebFetch gets HTTP 402 there).

Dead ends:

| URL or site | What happened |
|---|---|
| brightontoymuseum LEGO page | HTTP 403 |
| Printables HTML and Thingiverse | 403 or empty; Thingiverse not resolved |
| formlabs.com/blog/3d-printing-tolerances/ | 404 |
| PrusaSlicer old gizmo path on master | 404; refactored to `src/slic3r-shared/...` |
| Bambu wiki `filament-acc/filament/pla-basic` | 404 |
