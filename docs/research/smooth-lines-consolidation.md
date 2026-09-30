---
date: 2026-09-29
produced-by: smooth-lines checker (Claude Opus 5.5), the third agent of a two-researchers-then-a-checker pass
feeds:
  - '[[smooth-lines-design]]'
checks: researcher A (PR #433, smooth-lines-design-a.md + smooth-lines-research-a.md) and researcher B (PR #432, smooth-lines-design-b.md + smooth-lines-research-b.md)
---

# Smoother coaster lines: what the checker re-opened, and what it says

Omar, 2026-09-29: *"our coaster lines are rough; put together options for making them smoother,
with web research and pictures we can review in Obsidian. One option should be lines influenced by
the SKIMS font design."*

Two researchers answered on their own, without reading each other:

- **Researcher A**, [PR #433](https://github.com/omars-lab/3d-models/pull/433): measured the CS-2
  coaster (`7apC5Q9QS-8-minimal-coaster.bkr`) in a 12 mm crop around one star hole.
- **Researcher B**, [PR #432](https://github.com/omars-lab/3d-models/pull/432): measured the CS-1
  coaster (`GimTvN9hw4U-minimal-coaster.bkr`, 90 mm, 3 mm strap), the whole coaster and a 14 mm crop.

Both PRs are open and are the record this file was built from; their files are not on master, so
they are linked by PR. This file says where they agree, where they disagree and which side the code
or the source backs, what only one of them found, and which claims nobody re-opened.

**What the checker did.** Read both design docs and both research files and looked at every figure.
Re-read the bikar coaster kernel at `bikar-main` e2b65c4 (2026-09-29, "coaster: split an
outline-pattern coaster by fill color (#284)"), read-only. Re-fetched the web sources behind the
claims that decide the order of work, and the SKIMS facts (§5). Nothing was printed, nothing was
sliced, and no new render was made by the checker.

## 1. Where both agree

Agreement between two independent passes is the strongest evidence here. Each row was found by
both, on different coasters.

| Finding | A (CS-2) | B (CS-1) | Checker |
|---|---|---|---|
| The roughness is the 0.4 mm grid: each cell is solid or not, judged from its centre, so every slanted wall is a staircase | worst 0.42 mm, typical 0.137 mm | worst 0.277 mm whole coaster, typical 0.126; crop 0.273 / 0.097 | Code confirms: `classifyCell` judges the centre, `emitWall` puts a flat panel on every cell edge, pitch set at `COASTER_GRID_PITCH_MM = PERIMETER_WIDTH_MM` (0.4 mm) |
| Slicer settings cannot fix it: the steps are in the model the slicer is given; a fine resolution keeps every step and a coarse simplify cuts across them unevenly | simplify at 0.3 mm: 0.34 / 0.106 | simplify at 0.25 mm: 0.273 / 0.101, lopsided left to right | Sources re-fetched (§5.3) agree arc fitting only changes how moves are written |
| A finer grid helps only as a dial and the file grows fast | 0.2 mm: 0.13 / 0.052; 0.1 mm: 0.07 / 0.030 | 0.2 mm: 0.136 / 0.045; 0.1 mm: 0.069 / 0.022; triangles about ×4 / ×16 (estimates, not renders) | `gridPitchMm` already exists on the field options, but no naqsh clause sets it |
| Drawing the edge *between* the grid points (marching squares) makes the typical edge almost exact but cuts off sharp points narrower than a step | 0.19 / 0.006 | 0.150 / 0.005 | Matches the method: Wikipedia confirms edge points come from "linear interpolation between the original field data values" (§5.3); the tip clipping is the researchers' measurement, not a source's claim |
| An exact outline gives zero stray but is the most code | 0 (in shapely) | 0 (in shapely) | Both measured it in Python's shapely, not in bikar; see §2 for what bikar has |
| The interlock coaster's exact outer wall is the in-house precedent | yes | yes | Code: `emitExactWall`, `emitCollar`, `assembleInterlock` |
| Rounding the sharp hole points (A) or inside corners (B) — the same corners — at 0.75 mm keeps the pattern; at 1.5 mm it changes the pattern | stars become flowers at 1.5 | fillets at 0.75 and 1.5 | Figures 06 and 07 in the design doc show it |
| The round top already exists: `edge fillet $round top`, `param round = 1 range 0..1.5`; `round=1.5` is a full dome on a 3 mm strap and needs no code | yes | yes | Both `.bkr` files carry `param round = 1 range 0..1.5 # … CV10 needs 2*round <= strap` |
| SKIMS: melted joins transfer; a swell where strokes meet transfers; the lean and the tight spacing do not (lean breaks mirror symmetry, tight spacing closes the open cells) | yes, plus hand-made irregularity does not transfer | yes | Re-fetched (§5.1) |
| The smooth blend that melts joins must not depend on the order the straps are blended | sorted two-nearest blend, measured 100% turned and mirrored | proposes a sum over nearby straps | Quilez confirms the common blend is "not associative" (§5.2) |
| The grid pitch's stated reason does not carry over to where an edge sits (K10): "the finest lateral feature the nozzle can place" is about which features exist, not where an edge lies | yes | yes | Agreed; the slicer places edges far finer than 0.4 mm (resolution 0.012 in the preset chain, 0.01 in the minis-04 slice) |
| Nothing was printed; whether the steps can be seen or felt on a real print is not known | yes | yes | Backlog item 7 in `docs/tasks/catalog-expansion/backlog.md` already says it "waits on a look at a printed edge" |

## 2. Where they disagree

### 2.1 Which edge fix to build first: exact outline (A) or marching squares (B)

**A** recommends the exact outline first (A3), following the interlock's exact wall, with the
SKIMS look (D-light) and hole-point rounding (B1) added on top. **B** recommends marching squares
first (its C), then inside rounding (E), then the SKIMS soft weld light (G-light), and advises
against the exact outline before marching squares.

**The code backs B on the order.**

1. **bikar's polygon union walks only the outer edge.** `packages/core/src/graph/polygon-union.ts`
   says so in its header and draws 6 arcs per half circle (about 3% area). A strap network is
   mostly holes. For a 1.5 mm round end, 6 arcs per half circle leave a gap of about
   1.5 × (1 − cos 15°) ≈ 0.05 mm — the checker's arithmetic, not a measurement — so even this
   code, as it stands, would not give A's "0".
2. **bikar chose not to take a polygon-clipping library.**
   `docs/decisions/2026-05-07-polygon-clipping-dep.md` in bikar picked Option C, reusing its own
   half-edge graph, over `polygon-clipping` and `martinez`. No clipper, martinez or polybool
   package appears in bikar's package files. An exact outline with holes means either reopening
   that decision or writing hole-tracing into the half-edge walk.
3. **The interlock precedent handles one loop, flat.** `emitCollar` throws unless it gets exactly
   one inside loop, and its outer ring sits at the flat base height. It has two issue write-ups
   behind it (the collar loft and the collar fold). A strap coaster needs dozens of loops, each
   carrying the round top.
4. **The shape options are field changes.** The SKIMS blend and the width changes alter the
   distance-from-strap number that each grid point already has (`signedInset`). Marching squares
   traces that same number, so every shape option works on it with no extra code. An exact outline
   would need each shape option redone as polygon offsets. **A's own figures agree:** its
   `make_figures.py` draws the SKIMS options by tracing the field (`contourf` / `contour` of `F`),
   which is marching-squares style, not by polygon offsets. So A's claim that D rides on A3 does
   not match how A drew D (a K7 inside A's doc).
5. **Marching squares fits the kernel's shape.** Each cell's piece of wall is decided from its four
   corners, and two neighbouring cells compute their shared edge point from the same two numbers,
   so the mesh closes by construction. The kernel already names the one hard case: `desaddle`'s
   comment calls diagonal pinches "marching-squares saddles".

**Where A's point stands.** Marching squares cuts sharp star points: 0.19 mm on CS-2, 0.15 mm on
CS-1. If sharp points must stay sharp, only the exact outline gets them. The fix both researchers
offer — rounding those corners a little — also removes the cut, because a rounded point is wider
than a grid step. So the order depends on one taste call: must star points stay needle-sharp?
That is an open call for Omar in the design doc.

**Who the evidence backs:** B on the build order. A on the validator (§3) and on getting a printed
look before building (backlog item 7 says the same).

### 2.2 Why A's worst stray (0.42 mm) is bigger than B's (0.277 mm)

When each cell is judged from its centre, the edge can be off by at most half a cell diagonal:
0.4 × √2 / 2 ≈ 0.283 mm. B's 0.277 fits that. A's 0.42 does not.

**Checker's reading — inferred, not confirmed by a re-render.** `desaddle` (coaster.ts) looks for
two solid cells touching only at a corner and fills one of the two empty cells beside them,
always the same one by position (`br` or `bl`). At a star point that fill can land on the cell
closest to the tip, which pushes the wall a whole cell past where it should be. A's figure 02 (the
design doc's `02-today-staircase.png`) is consistent with this: the upper-left star point shows a
lone empty cell cut off from the hole by a filled cell. It would also explain why A's simulation
differed from the STL by one cell (0.16 mm², noted in A's research). The same fill is a small
lopsided choice, which adds to B's finding that the square grid already breaks six-fold symmetry.
A lone empty 0.4 mm cell inside a strap is also a pinhole the slicer may or may not keep —
not checked.

### 2.3 Names

| Thing | A calls it | B calls it | The design doc says |
|---|---|---|---|
| `round=1.5` top | full pillow | full dome | **full dome** |
| a flat-topped strap with soft shoulders | (not drawn) | pillow top (a new shape) | **pillow top** |
| the sharp corners around a hole | hole points | inside corners | **hole points** (the sharp corner of the opening) |
| drawing the edge between grid points | A2 marching squares | C interpolated contour | **marching squares** (once), then "edge between grid points" |

## 3. What only one found

Kept and flagged, not dropped and not trusted as agreed.

**Only A:**

- The traditional reading of strap patterns uses **mitred joins**: Kaplan & Salesin 2004,
  "Where two thickened line segments meet, we must perform a mitered join" — **re-opened and
  confirmed** (§5.4). Kaplan 2017 (Bridges) on a "bulging" operation that rounds bands on 3D-printed
  pieces — not re-opened.
- A smoother-than-round blend (curvature-continuous, peak about 2.1/mm against 1/mm); A says it is
  likely not visible at this scale. Not re-checked.
- The **pen held at one angle** breaks symmetry (84% turned, 89% mirrored); a pen turned with the
  pattern keeps it (100% / 100%). Measured by A's script; not re-run.
- **D-strong** (octagons become circles), both SKIMS strengths measured 100% symmetric.
- A survey of 12 Printables Islamic-coaster listings: none of the 12 mentions smoothing a stepped
  edge. Not re-opened; it is a claim about those 12 only.
- The Bambu preset's resolution is 0.012 mm (read from the app's profiles on disk). **Confirmed
  locally:** `docs/research/print-quality-verification.md` §1.2 lists 0.012 for the preset chain.
- **The round top also saw-tooths:** `topEdgeDrop` is evaluated at grid points, so the round-over
  follows the staircase too. Confirmed in code (coaster.ts `topEdgeDrop` uses `signedInset` at
  each sampled vertex).
- **A per-loop edge check** (largest gap on each wall loop ≤ 0.05 mm), not one average. Adopted in
  the design doc as the validator. The 0.05 mm limit is A's choice, not a measured print threshold.
- **Print an edge coupon first.** Adopted as an open call, since whether to print is Omar's.

**Only B:**

- **The square grid breaks six-fold symmetry** on a six-fold pattern. Consistent with the code
  (a square grid has only four-fold turns). Not re-measured.
- The coarse simplify is **lopsided** left to right (figure 05).
- The **pillow top** as a new shape (flat top, soft shoulders); relates to the pillow height-field
  idea in `docs/research/coaster-bubble-lettering.md`.
- **Arc counts** for a 1.5 mm round end: 28 pieces per half circle for 0.01 mm, 13 for 0.05 mm, using
  Clipper2's rule. Clipper2's default arc tolerance is "offset_radius / 500" — **re-opened and
  confirmed** (§5.3).
- `polygon-union.ts` is outer-edge only — **confirmed in code** (§2.1).
- The minis-04 slice ran at resolution 0.01 with arc fitting off — **confirmed locally** in
  `print-quality-verification.md` §1.2 (the "Slice" column: `enable_arc_fitting` 0, `resolution`
  0.01).
- The first X2D firmware notes: curve planning "results in better surface quality in certain
  scenarios, especially on rounded features" — **re-opened and confirmed** (§5.3). It helps curves
  that are in the model; it cannot add curves that are not.
- A forum user calling arc fitting "effectively lossy" — **re-opened and confirmed** as one user's
  words, not Bambu's.
- Measured mesh-gate volumes at round 0 / 1 / 1.5: 14.6 / 14.0 / 13.4 cm³, all passing. Not re-run.

**Only the checker:** the `desaddle` reading in §2.2 (inferred), the 6-arcs arithmetic in §2.1, and
that `emitCollar` accepts exactly one loop.

## 4. Claims resting on a snippet, or not re-opened

These are not wrong; they are not confirmed by this pass. The design doc keeps each one's hedge.

| Claim | From | Status |
|---|---|---|
| mojomox: "a bit of irregularity" in the SKIMS mark | A | **Not found.** Re-fetched both mojomox pages (A's `mojomox.com/skims-font` and B's `fonts.mojomox.com/…/what-font-does-skims-use`); neither has "irregular" or "irregularity". A's first page says only that it is "a custom logotype". Treat "hand-made irregularity" as A's reading, not a quote. |
| The SKIMS mark was drawn in Ye's own handwriting | A (snippet) | Complex reports this as rapper Consequence's claim on X and calls it unverified. Only "he drew the logo" is on record. |
| designyourway: "geometric with subtle humanist touches" | A | Re-fetched, confirmed. It pulls against mojomox's soft, "not engineered" reading; the two sources disagree on the feel. |
| dafont forum: "most probably not a font" | A | Not re-opened. |
| logos-world: letters like a "silicone mass, slightly spread" | B | Re-fetched: the page says the lettering gives the impression of silicone "slightly spreading" and credits Kanye West ("It is believed…"). The exact phrase "silicone mass" came back paraphrased by the fetch tool; treat as close, not verbatim. |
| rabbitlogo SKIMS page | B | 403 for B; not re-opened. |
| logotyp.us | A, B | Both called it unreliable; not used. |
| Bambu curve planning uses splines; Prusa's resolution default is 0; Fusion's 0.1 mm / 1° export; Inkscape; Broug | B | Snippet only in B; not re-opened. None decides an option. |
| FDM corner guidance: tchncs, 3DVerkstan, Hydra, UltiMaker, littleboxes, Hubs, RapidDirect | A | tchncs re-fetched: "a radius on corners that is roughly equal to half the extrusion width" confirmed; the page does **not** say inside corners stay sharp (A's table says it does). The rest not re-opened. |
| OrcaSlicer wall generator, Prusa Arachne, BOSL2 `round_corners`, Round-Anything, Jamie Wong metaballs, BambuStudio issue 11739, forum thread 34179 | B | Not re-opened. None decides the order. |
| Alias G0–G3 continuity page | A | Not re-opened; A noted the fetch may have paraphrased it. |
| Kaplan 2017 "bulging" | A | Not re-opened. |
| 12 Printables listings, 8 maker pages | A, B | Not re-opened; each is a claim about the listed set only. |
| Finer-grid triangle counts (0.41 M, 1.66 M) | B | Estimates by scaling, not renders — both say so. |

## 5. Sources re-opened by the checker (2026-09-29)

### 5.1 SKIMS

| Source | Re-fetched | What it says |
|---|---|---|
| [mojomox, what font does SKIMS use](https://fonts.mojomox.com/blogs/brand-fonts/what-font-does-skims-use) | yes | "The strokes are thick and even, with no real thick-to-thin variation. The terminals are fully rounded, so the letters read as soft rather than engineered." "very tight spacing"; counters "squeezed small"; "appears to be custom rather than a licensed retail typeface". Lookalikes named: Skay, Nuido, Goji. No designer named. |
| [mojomox, SKIMS font](https://mojomox.com/skims-font) | yes | "The Skims font is a custom logotype designed for the Skims brand"; the rest is about the Skay lookalike. |
| [1000logos](https://1000logos.net/skims-logo/) | yes | "introduced at the end of 2019"; "a slanted designer typeface with massive uppercase characters and soft rounded contours"; closest fonts "TPG DontBlurry, Spilled Ink, or Outahere with some significant modifications". No designer named. |
| [Wikipedia, Skims](https://en.wikipedia.org/wiki/Skims) | yes | Kanye West "was credited as being her 'Ghost Creative Director' and for creating the company's logo"; co-founded June 2019. |
| [Complex, 2025-04-10](https://www.complex.com/style/a/tracewilliamcowen/kanye-west-skims-logo-explainer) | yes | Kim Kardashian at the 2019 DealBook conference: "For SKIMS, he drew the logo." The handwriting claim is Consequence's, unverified. In March 2025 Ye credited Vanessa Beecroft as "really where SKIMS came from". |
| [logos-world](https://logos-world.net/skims-logo/) | yes | "bubble font … popular due to its softness and volume"; creation "believed" to be Kanye West's. |
| [designyourway](https://www.designyourway.net/blog/skims-logo/) | yes | "The letterforms are geometric with subtle humanist touches"; uniform stroke widths. |

**What this settles.** Custom lettering, not a font you can buy (mojomox; A's dafont reply agrees, not re-opened). Credited
to Kanye West by Wikipedia and by Kim Kardashian's own words ("he drew the logo"); how it was drawn
is not on record. The traits the options use — even thick strokes, fully rounded ends, very tight
spacing, a slant — are each in a re-fetched source. "Melted joins" is the researchers' reading of
the look (mojomox's "soft rather than engineered", logos-world's spreading silicone), not a
source's words.

### 5.2 The blend

[Quilez, smooth minimum](https://iquilezles.org/articles/smin/), re-fetched: the quadratic smooth
minimum is `k *= 4.0; h = max(k-abs(a-b),0.0)/k; return min(a,b) - h*h*k*(1.0/4.0);` and this
family is "not associative": "the order in which you blend objects matters". So blending straps one
after another in file order would give a shape that depends on file order. A's sorted two-nearest
form avoids that (and measured 100% symmetric); B's sum over nearby straps is another order-free
form. Either works; the doc does not need to pick yet.

### 5.3 Edge tracing and the slicer

| Source | What it says |
|---|---|
| [Wikipedia, Marching squares](https://en.wikipedia.org/wiki/Marching_squares) | edge points by "linear interpolation between the original field data values"; saddles resolved with "the average data value for the center of the cell". Says nothing about sharp corners. |
| [Bambu forum 253630](https://forum.bambulab.com/t/253630), "Curve Planning Silently Turns off Arc Fitting In Bambu Studio" | "On a first slicing it will turn off Arc Fitting because curve planning suport [sic] was detected." Arc fitting "converts countless tiny line segments into real arc commands and mainly reduces G code size." A's quote ("automatically disabled arc fitting") is not this thread's wording; the fact matches. |
| [Bambu forum 252200](https://forum.bambulab.com/t/252200) | a user: "Arc fitting is just done for gcode compression, and is effectively lossy." |
| [Bambu forum 250867](https://forum.bambulab.com/t/250867), X2D OTA 01.01.00.00 | Curve Planning Enhancement "results in better surface quality in certain scenarios, especially on rounded features." |
| [OrcaSlicer precision wiki](https://github.com/SoftFever/OrcaSlicer/wiki/quality_settings_precision) | resolution: the path "is generated after simplifying the contour of models"; no default stated on the page. Arc fitting replaces short moves with G2/G3 arcs. |
| [Clipper2 ArcTolerance](https://www.angusj.com/clipper2/Docs/Units/Clipper.Offset/Classes/ClipperOffset/Properties/ArcTolerance.htm) | "The default ArcTolerance is: offset_radius / 500." |

### 5.4 The traditional reading

[Kaplan & Salesin 2004](https://grail.cs.washington.edu/wp-content/uploads/2015/08/kaplan-2004-isp.pdf),
re-fetched and read as text: "Where two thickened line segments meet, we must perform a mitered
join." That is how the classic strap drawing treats a bend; today's bikar strap has a round outside
bend (round ends on each segment), so today's look is already a small departure from it.

### 5.5 The vertical wall

Added 2026-09-29 for design-doc option 10 (layer lines up the wall), after Omar asked whether the
sides and the optional Bambu settings were covered. Bambu's own wiki could not be fetched: all five
pages tried (`/en/software/bambu-studio/seam`, `/precise-wall`, `/precise-z-height`,
`/adaptive-layer-height`, `/parameter/speed`) returned HTTP 402, so the setting descriptions come
from the OrcaSlicer wiki and from Bambu forum and GitHub threads.

| Source | Fetched | What it says |
|---|---|---|
| [OrcaSlicer wiki, layer height](https://github.com/SoftFever/OrcaSlicer/wiki/quality_settings_layer_height) | yes | smaller layer heights: "Less noticeable layer lines", "Smoother surface finishes"; on variable layer height only "You can use a variable layer height with the Variable Layer Height feature" |
| [OrcaSlicer wiki, variable layer height](https://github.com/OrcaSlicer/OrcaSlicer/wiki/prepare_variable_layer_height) | yes | "dynamic adjustment of layer heights throughout the print"; three modes, adaptive (a quality/speed slider), smooth (Gaussian filtering), manual. Says nothing about where it excels and nothing about vertical walls — the design doc's "nothing to adapt to on a straight wall" is the checker's reasoning |
| [OrcaSlicer wiki, seam](https://github.com/SoftFever/OrcaSlicer/wiki/quality_settings_seam) | yes | aligned "Will attempt to align the seam to a hidden internal facet of the model"; back "places the seam on the back side (Min Y point in that layer)"; random "places the seam randomly across the object"; nearest picks "the point that is closest to where the nozzle already is". Scarf joint "Adjusts the extrusion flow rate at seam points to create a smooth overlap between the start and end of each loop"; "Reduces visible z-seams"; "Improves cosmetic quality of curved surfaces"; "Less effective on sharp corners and overhangs"; "Requires tuning of parameters like length, speed, and flow"; scarf speed "less than 100 mm/s" recommended |
| [OrcaSlicer wiki, precision](https://github.com/SoftFever/OrcaSlicer/wiki/quality_settings_precision) | yes | Precise wall: "improving the dimensional accuracy of prints and minimizing layer inconsistencies by slightly increasing the spacing between the outer wall and the inner wall when printing in Inner Outer wall order"; only with inner-outer order. Precise Z height: "ensures the accurate Z height of the model after slicing, even if the model height is not a multiple of the layer height", adjusting the last five layers |
| [OrcaSlicer wiki, other layers speed](https://github.com/SoftFever/OrcaSlicer/wiki/speed_settings_other_layers_speed) | yes | outer wall speed: "Speed of outer wall which is outermost and visible. It's used to be slower than inner wall speed to get better quality and good layer adhesion." |
| [Bambu forum 29435, "Seam position?"](https://forum.bambulab.com/t/seam-position/29435) | yes | a forum user, not Bambu: aligned "puts the seam on the sharpest corner, and works best for most models"; back "still seeks out angles on the back side, so there's not just an obvious vertical seam"; nearest "also appears random (or nearly so)"; no setting makes a straight vertical seam; the seam painting brush places it by hand |
| [BambuStudio issue #10050](https://github.com/bambulab/BambuStudio/issues/10050) | yes | "'Smart scarf seam application' causes scarfs to not be used at all if the 'Seam Position' is Random or Nearest"; Studio 2.5.0.66; works with aligned or with smart scarf off; open, no maintainer reply visible |
| [BambuStudio issue #8030](https://github.com/bambulab/BambuStudio/issues/8030) | yes | "Precise Wall moves outer wall inward, incorrectly shrinks printed model"; Studio 2.2.1.60; reporter says "all walls move inward" and that OrcaSlicer keeps the outer wall in place; labelled bug, assigned, no reply or fix visible. Whether our 02.08.02.61 behaves the same: not known |
| [3djake, scarf seam guide](https://www.3djake.com/info/guide/get-rid-of-z-seams-how-to-get-smooth-surfaces-with-scarf-seam) | yes | "a gradual blend" instead of "a hard transition"; can make "the Z seam almost disappear" on uniform surfaces; "does not fix fundamental printing problems". Names no version, printer or material |
| Precise Z height "leaves the several topmost layers bulging out slightly" | snippet | a search snippet from a forum post; not opened |
| Precise wall "keeps outer walls at exactly one nozzle width" | snippet | a search snippet (stacksheriff); not opened, and it does not match the OrcaSlicer wiki's description, so not used |
| Bambu wiki: seam, precise wall, precise Z height, adaptive layer height, speed | **no** (402) | not read |

Local facts behind the option-10 table, all in this repo: `tools/bambu/test/fixtures/minis-04/process.flat.json`
(`layer_height 0.2`, `seam_position aligned`, `seam_slope_type none`, `seam_slope_min_length 10`,
`adaptive_layer_height 0`, `outer_wall_speed` first entry `200`, `small_perimeter_speed 50%`,
`enable_arc_fitting 1`, `wall_loops 2`); `tools/bambu/test/fixtures/minis-04/flattened-slice.project_settings.config`
(`precise_outer_wall 0`, `precise_z_height 0`); every `src/Coasters/*.bkr` sets
`param height = 4 range 1.4..16`; `docs/prints/2026-09-26-minis-04/index.md` has `layer_mm: 0.2`
and prints at height 1.4 (twist at 4). The six-entry `outer_wall_speed` list was not decoded beyond
its first entry.

## 6. Code facts the design doc leans on

All at bikar-main e2b65c4, `packages/core/src/kernel3d/coaster.ts` unless named.

- `COASTER_GRID_PITCH_MM = PERIMETER_WIDTH_MM` (0.4 mm), with a `**Default:**` comment citing CAL-FEA-01.
- `gridPitchMm?` exists on the field options; no naqsh clause sets it.
- `signedInset`: for a pattern, `strapWidth/2 − distToStraps`, a continuous distance, so marching
  squares has the number it needs. Only the solid/empty result is stored per cell today
  (`sampleField` keeps per-cell masks); the values would be computed again or kept.
- `topEdgeDrop`: quarter-round `rise·(1 − √(1 − (1−u)²))`, from `signedInset` at each grid point.
- `classifyCell` judges the centre; `emitTopCells` makes one flat top per cell; `boundaryLoops`
  cancels shared edges and does not merge straight runs; `emitWall` makes a vertical panel per
  cell edge; `assembleFlatBased` runs `desaddle` → top → walls → flat bottom.
- `desaddle` fills an empty cell at each diagonal pinch, always `br` (or `bl`), to a fixpoint; it
  works on a copy, and the validators read the field's own cells, untouched.
- `emitCollar` throws unless given exactly one inside loop; its outer ring is at the base height.
- `packages/core/src/graph/polygon-union.ts`: outer edge only, `ARCS_PER_HALF_CIRCLE = 6`.
- Both `.bkr` files: `param round = 1 range 0..1.5 # mm, top-edge quarter-round run — CV10 needs 2*round <= strap` and `edge fillet $round top`.
