---
date: 2026-09-29
produced-by: researcher B subagent (Claude Opus 5.5), one of two independent smooth-lines researchers; web search and fetch, a read-only read of bikar at `~/Workspace/git/bikar-main` (branch main, 2026-09-29), and our own renders and measurements of the CS-1 minimal coaster
feeds:
  - '[[smooth-lines-design-b]]'
---

# Smooth lines, research B: how to make the coaster straps smoother

The raw findings behind [`../design/coaster/smooth-lines-design-b.md`](../design/coaster/smooth-lines-design-b.md).

The question (Omar, 2026-09-29): *"when it comes to our lines... put together options for making
them smoother. Web search and prepare a design.md with options and screenshots we can review in
Obsidian. One of the options should be lines influenced by the SKIMS font design."*

Every web source below says whether I **fetched** the page (read its text) or saw only a
**search snippet** (a line or two shown by the search engine, which can be out of context).
Nothing load-bearing in the design doc rests on a snippet alone; where a claim does, it is
flagged there. Quotes are short. Everything else is paraphrase.

**Nothing was printed and no slicer was run.** Every claim about what a print looks like is either
quoted guidance (hedged as the source hedges it) or a geometric measurement of a file, labelled as
such.

## 1. Our own measurements (the part that matters most)

### 1.1 What the kernel does today

Read in `bikar/packages/core/src/kernel3d/coaster.ts` (bikar main, 2026-09-29):

- The coaster is sampled on a square grid whose pitch is `COASTER_GRID_PITCH_MM`, set equal to the
  perimeter width, 0.4 mm (line 200, tied to the bet `CAL-FEA-01`). A spec field `gridPitchMm`
  (line 372) can override it, but no naqsh clause sets it.
- `classifyCell` (line 977) decides each cell solid or empty from its centre. For a minimal coaster
  a cell is solid when its centre is closer than half the strap width to the nearest centreline.
- The side walls follow cell edges. So **every strap wall**, not only the coaster's outer rim, is
  an axis-aligned staircase with 0.4 mm steps wherever the strap runs at a slant to the grid.
- The one place the kernel does not do this is the interlock coaster's outer ring:
  `emitExactWall` (line 2155) and `assembleInterlock` (line 2180) write the slotted ring as an
  exact vertical wall, because the dovetails need a smooth face
  ([coaster-interlock-design.md §5](../design/coaster/coaster-interlock-design.md#5-kernel-change)).
- The top round-over (`edge fillet $round top`) is sampled on the same grid, so it softens the top
  but cannot move the wall off the staircase.
- bikar has a 2D union, `bikar/packages/core/src/graph/polygon-union.ts`, built on its half-edge
  graph. Its header says it walks the **outer perimeter**; the strap network also needs its inner
  loops (the open cells), so reusing it for an exact strap outline would need that added.

### 1.2 How far the stepped wall strays

Rendered from bikar main, read-only, into a scratch folder:

```
node packages/cli/dist/index.js render patterns/Constructions/GimTvN9hw4U-minimal-coaster.bkr \
  --format stl --check --param size=90 --param round=<0|1|1.5> -o <out>.stl
```

The CS-1 minimal coaster: size 90 mm, height 4 mm, strap 3 mm. I rebuilt the exact centrelines
from `bikar points` (252 unique segments), drew the exact strap outline (each centreline widened by
1.5 mm each side, with round ends), and compared it with the STL's bottom-face outline.

| Measurement | Value | How |
|---|---|---|
| Worst stray of the STL wall from the true edge, straight runs only | 0.273 mm | 4,044 wall corners more than 2.5 mm from any segment end |
| Worst stray, whole coaster | 0.277 mm | every bottom-outline corner |
| Mean stray, whole coaster | 0.126 mm | same |
| Triangles in today's STL (round 1) | 103,524 (5 MB) | STL header |
| Mesh-gate volume, round 0 / 1 / 1.5 | 14.6 / 14.0 / 13.4 cm³ | `--check` output; all three pass |

The 0.273 mm agrees with `tools/edge_stairs.py`'s 0.27 mm for a slab coaster's slanted sides:
the same grid produces the same step.

### 1.3 Simulated options, checked against the real file first

The option pictures are drawn by a scratch script (not committed) that samples the exact outline
the way the kernel does. **Check before use:** at 0.4 mm the simulated shape and the real STL
differ by 0.003 mm² of area inside the 14 mm crop (one grid cell is 0.16 mm²), and the simulated
worst stray is 0.273 mm, the same as the STL's. So the simulation reproduces the kernel for this
crop.

| Option, same 14 mm crop | Worst stray | Mean stray | Note |
|---|---|---|---|
| 0.4 mm grid (today) | 0.273 mm | 0.097 mm | matches the STL |
| 0.2 mm grid | 0.136 mm | 0.045 mm | triangles about ×4: an estimate, about 0.41 M |
| 0.1 mm grid | 0.069 mm | 0.022 mm | triangles about ×16: an estimate, about 1.66 M |
| 0.4 mm samples, edge interpolated between them | 0.150 mm | 0.005 mm | the worst is only at the sharp inside corners, where the tip is cut off |
| Slicer-style simplify, 0.0125 mm | 0.273 mm | 0.096 mm | 229 → 146 outline points; every step kept |
| Slicer-style simplify, 0.25 mm | 0.273 mm | 0.101 mm | 102 points; cuts across the steps unevenly, left and right differently |

The triangle counts for the finer grids are scaling estimates (count grows with the square of
1/pitch), not renders.

For an exact outline, a round strap end of radius 1.5 mm needs 28 straight pieces per half-circle
to stay within 0.01 mm of the true arc, and 13 to stay within 0.05 mm (chord arithmetic,
`n = π / acos(1 − tol/r)`).

### 1.4 Our slicer settings

From [`print-quality-verification.md`](print-quality-verification.md) (our own read of the minis-04
3MF): the Bambu preset chain says `resolution` 0.012 and arc fitting on; the minis-04 slice used
`resolution` 0.01 and arc fitting off. A resolution of 0.01 mm is far below the 0.4 mm step, so on
that evidence the slicer keeps every step of today's wall.

## 2. Smoothing at the geometry layer

- **Marching squares.** The edge is placed between samples by linear interpolation along each cell
  edge; ambiguous "saddle" cells need a rule ([Wikipedia: Marching squares](https://en.wikipedia.org/wiki/Marching_squares), fetched).
  Jamie Wong's metaballs article shows the same grid drawn blocky without interpolation and smooth
  with it ([jamie-wong.com](https://jamie-wong.com/2014/08/19/metaballs-and-marching-squares/), fetched).
- **Exact offsets.** Clipper2's offsetter approximates round joins and ends with straight pieces,
  and its `ArcTolerance` sets how far they may stray; the default is the offset radius / 500
  ([Clipper2 ArcTolerance](https://www.angusj.com/clipper2/Docs/Units/Clipper.Offset/Classes/ClipperOffset/Properties/ArcTolerance.htm), fetched).
- **OpenSCAD `offset`.** `offset(r=…)` rounds, `offset(delta=…)` keeps sharp corners. The manual
  gives the two-step recipes: shrink by `delta` then grow by `r` rounds outside corners; grow then
  shrink rounds inside corners. `$fn`, `$fa`, `$fs` set the facet count
  ([OpenSCAD User Manual: Transformations](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations), fetched).

## 3. Smoothing at the corners

- **Inside fillets by a second offset.** Same OpenSCAD recipe as §2 (fetched). Our own
  [coaster-minimal-design.md](../design/coaster/coaster-minimal-design.md#10-not-yet) lists a
  fillet at the inside corner as "a second offset" that "is not asked for".
- **Curvature-continuous (G2) rounding.** BOSL2's `round_corners` has a "smooth" method: "continuous
  curvature rounding using 4th order Bezier curves", with a parameter `k` for the shape
  ([BOSL2 rounding.scad](https://github.com/BelfrySCAD/BOSL2/wiki/rounding.scad), fetched).
- **Round-Anything** (OpenSCAD library): its README says "internal radii in particular can be a real
  pain" in OpenSCAD ([Irev-Dev/Round-Anything](https://github.com/Irev-Dev/Round-Anything), fetched).
- **Smooth minimum.** Íñigo Quilez's polynomial smooth-min blends two distance fields so the join
  melts, with a blend width `k`; it adds material at the join
  ([iquilezles.org: smooth minimum](https://iquilezles.org/articles/smin/), fetched).
- **Fusion 360 sketch fillets.** The Autodesk help page returned 404 when fetched. What I have is
  from tutorial snippets (desktopmakes, productdesignonline) only: **snippet**.

## 4. Smoothing in the mesh

- Hubs' STL export guide: set chord height (deviation) to about 1/20 of the layer height; too
  coarse and "visible triangles" show on the print
  ([Hubs: STL files step by step](https://www.hubs.com/knowledge-base/3d-printing-stl-files-step-step-guide/), fetched).
  At our 0.2 mm layers that is 0.01 mm. **Transfer note:** Hubs writes about exporting curved CAD
  surfaces; it applies to our exact-outline option (arcs cut into straight pieces), not to the grid
  staircase, which is not an approximation of a curve at all.
- Fusion's default export tolerance (0.1 mm deviation, 1° normal): **snippet** only.

## 5. Smoothing in the slicer

- **Arc fitting.** OrcaSlicer: arc fitting "mainly changes how the toolpath is encoded", and arcs
  "introduce approximation"
  ([OrcaSlicer wiki: precision](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_precision), fetched).
  Bambu forum: "Arc fitting is just done for gcode compression, and is effectively lossy"
  ([X2D curve planning slower](https://forum.bambulab.com/t/x2d-curve-planning-much-slower-compared-to-arc-fitting/252200), fetched; a forum user, not Bambu staff).
- **Arc fitting only on outer walls?** A user reports it applies to external perimeters only; no
  staff reply ([forum thread 34179](https://forum.bambulab.com/t/arc-fitting-not-working-on-internal-perimeters/34179), fetched). One user's report.
- **X2D curve planning.** The X2D's first firmware (01.01.00.00) notes say curve planning gives
  "better surface quality in certain scenarios, especially on rounded features"
  ([X2D OTA 01.01.00.00](https://forum.bambulab.com/t/first-update-for-x2d-is-out-ota-01-01-00-00/250867), fetched).
  Users report that turning it on silently turns arc fitting off in Bambu Studio
  ([forum thread 253630](https://forum.bambulab.com/t/curve-planning-silently-turns-off-arc-fitting-in-bambu-studio/253630), fetched;
  [BambuStudio issue 11739](https://github.com/bambulab/BambuStudio/issues/11739), fetched, no staff explanation).
  That curve planning "uses splines": **snippet** only.
- **Resolution.** OrcaSlicer: resolution simplifies contours before slicing
  ([precision page](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_precision), fetched).
  Bambu's recommended 0.012 and Prusa's slice-resolution default of 0: **snippet** only.
- **Arachne walls.** Varies extrusion width, with a minimum feature size and minimum wall width set as
  a percentage of the nozzle ([OrcaSlicer wiki: wall generator](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_wall_generator), fetched).
  Prusa: "Features thinner than this value will not be printed"
  ([Prusa: Arachne](https://help.prusa3d.com/article/arachne-perimeter-generator_352769), fetched).

**What this means for us (my reading, not a source's):** arc fitting and curve planning change how
the nozzle moves along the outline the slicer gives them. They have no curve to find in a 0.4 mm
staircase of straight axis-aligned steps. A slicer setting cannot recover the true edge; it can only
keep the steps (fine resolution) or cut across them (coarse resolution), and §1.3 shows the coarse
cut is uneven and breaks the left–right symmetry.

## 6. The SKIMS wordmark

### 6.1 What it looks like (seen myself)

I downloaded the logo SVG from SKIMS's own Shopify CDN
([SVG](https://cdn.shopify.com/s/files/1/0259/5448/4284/files/Skims-Logo-Shopify_afa1385f-2e6f-46f3-940e-923f2385bc9b.svg), fetched)
into scratch to look at it. It is **not** copied into the repo. What I saw:

- heavy all-caps letters, "bubble" style, with a forward slant;
- no straight lines: every contour is a continuous curve;
- big convex bulges, with tight rounded pinches in the concave notches;
- the S ends swell into bulbs thicker than the stroke's waist;
- letters nearly touching, so the counters (the holes inside letters) are narrow slits.

### 6.2 What sources say

| Source | Fetched? | What it says |
|---|---|---|
| [mojomox](https://fonts.mojomox.com/blogs/brand-fonts/what-font-does-skims-use) | fetched | custom lettering; strokes "thick and even, with no real thick-to-thin variation"; "terminals are fully rounded"; "very tight spacing" |
| [1000logos](https://1000logos.net/skims-logo/) | fetched | a "stylized bubble font", "soft rounded contours"; names lookalike fonts (TPG DontBlurry, Spilled Ink, Outahere) |
| [logos-world](https://logos-world.net/skims-logo/) | fetched | a "bubble font"; letters like a "silicone mass, slightly spread"; credits Kanye West with the emblem |
| [Wikipedia: Skims](https://en.wikipedia.org/wiki/Skims) | fetched | founded June 2019; West credited as "Ghost Creative Director" and with creating the logo |
| [logotyp.us](https://logotyp.us/logo/skims/) | fetched | "custom sans-serif typeface", colour taupe #62554a; also says "lowercase treatment", which contradicts the all-caps mark, so I treat this page as low quality |
| rabbitlogo | snippet (403 when fetched) | a title saying the two S letters do not match |
| designrush / studiobennu | snippet | a design studio worked with the brand owner "since Skims"; not enough to credit the logo to them |

**Who designed it:** two fetched pages (Wikipedia, logos-world) credit Kanye West. No fetched page
names a type designer. Treat the credit as reported, not established.

**A disagreement to carry:** mojomox says the strokes have "no real thick-to-thin variation"; what
I saw in the SVG is S terminals that swell past the waist. Both can hold: the main strokes are even,
and the ends and joins bulge. The design doc uses the bulge only at joins and ends.

### 6.3 What transfers from a 2D logo to a 3D strap (K10)

A trait transfers only where the reason it works in the logo also holds on a printed strap.

| Trait | Transfers? | Why |
|---|---|---|
| No sharp corners; joins melt together | yes | It is a plan-view shape rule; a printed strap has plan-view joins too, and a rounded inside corner is easier for a 0.4 mm nozzle to trace than a sharp one. |
| Ends and joins swell | yes, at joins | Our straps have few free ends (the minimal coaster's are round caps at the rim), but every crossing is a join, and a swell there is a shape rule that repeats at every crossing, so the symmetry holds. |
| Pillowy, domed top | yes | The wordmark's 3D versions read as inflated; bikar already has a top round-over, and `round = strap/2` gives a full dome today. The repo's own [bubble-lettering research](coaster-bubble-lettering.md) reached the same "soft dome on top" reading. |
| Tight spacing, slit counters | **no** | On a coaster the counters are the open cells. Closing them makes a near-solid piece, which Omar has rejected before. |
| Forward slant | **no** | A slant breaks the mirror symmetry that Islamic geometric patterns are built on. |
| Custom letter shapes | **no** | We take traits, not letters; copying the mark is off the table. |

## 7. What other makers do

Surveyed: 8 pages. Fetched: mathgrrl's girih tiles post
([mathgrrl.com](https://mathgrrl.com/hacktastic/2016/03/girih-tiles-for-interactive-islamic-designs/)),
a Thingiverse Cordoba pattern ([thing 2218796](https://www.thingiverse.com/thing:2218796), title
only), the Wikipedia article on Islamic geometric patterns
([Wikipedia](https://en.wikipedia.org/wiki/Islamic_geometric_patterns): straps "weave over and
under each other"; nothing on constant width). Blocked (403): a Printables girih-tiles model
([Stefan Huber](https://www.printables.com/model/780631-girih-tiles-for-islamic-geometric-patterns))
and an Etsy Cordoba coaster listing ([Etsy 758443317](https://www.etsy.com/listing/758443317)).
Snippet only: Etsy, Printables and Cults tag pages for Islamic geometric coasters.

**Result:** none of the pages surveyed here says how the maker smooths their lines. This is a gap
in the survey, not evidence that nobody does.

Adjacent, snippet only: Inkscape's stroke-to-path with round joins and a miter limit (the common way
to turn line art into a solid outline), and Eric Broug's three ways to turn a line drawing into a
composition (widen and interlace, widen without interlace, colour).

## 8. Sources

| # | Source | URL | Fetched / snippet |
|---|---|---|---|
| 1 | logotyp.us SKIMS | https://logotyp.us/logo/skims/ | fetched |
| 2 | mojomox SKIMS font | https://fonts.mojomox.com/blogs/brand-fonts/what-font-does-skims-use | fetched |
| 3 | Wikipedia Skims | https://en.wikipedia.org/wiki/Skims | fetched |
| 4 | 1000logos SKIMS | https://1000logos.net/skims-logo/ | fetched |
| 5 | logos-world SKIMS | https://logos-world.net/skims-logo/ | fetched |
| 6 | rabbitlogo SKIMS | https://rabbitlogo.com/blog/skims-logo/ | snippet (403) |
| 7 | designrush / studiobennu | search results | snippet |
| 8 | SKIMS logo SVG | https://cdn.shopify.com/s/files/1/0259/5448/4284/files/Skims-Logo-Shopify_afa1385f-2e6f-46f3-940e-923f2385bc9b.svg | fetched, viewed, not copied |
| 9 | OrcaSlicer precision | https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_precision | fetched |
| 10 | OrcaSlicer wall generator | https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_wall_generator | fetched |
| 11 | Prusa Arachne | https://help.prusa3d.com/article/arachne-perimeter-generator_352769 | fetched |
| 12 | OpenSCAD manual, transformations | https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations | fetched |
| 13 | BOSL2 rounding | https://github.com/BelfrySCAD/BOSL2/wiki/rounding.scad | fetched |
| 14 | Round-Anything | https://github.com/Irev-Dev/Round-Anything | fetched |
| 15 | Quilez smooth minimum | https://iquilezles.org/articles/smin/ | fetched |
| 16 | Clipper2 ArcTolerance | https://www.angusj.com/clipper2/Docs/Units/Clipper.Offset/Classes/ClipperOffset/Properties/ArcTolerance.htm | fetched |
| 17 | Wikipedia marching squares | https://en.wikipedia.org/wiki/Marching_squares | fetched |
| 18 | Jamie Wong, metaballs | https://jamie-wong.com/2014/08/19/metaballs-and-marching-squares/ | fetched |
| 19 | Hubs STL guide | https://www.hubs.com/knowledge-base/3d-printing-stl-files-step-step-guide/ | fetched |
| 20 | Bambu forum 253630 | https://forum.bambulab.com/t/curve-planning-silently-turns-off-arc-fitting-in-bambu-studio/253630 | fetched |
| 21 | Bambu forum 252200 | https://forum.bambulab.com/t/x2d-curve-planning-much-slower-compared-to-arc-fitting/252200 | fetched |
| 22 | Bambu forum 34179 | https://forum.bambulab.com/t/arc-fitting-not-working-on-internal-perimeters/34179 | fetched |
| 23 | Bambu forum 250867 | https://forum.bambulab.com/t/first-update-for-x2d-is-out-ota-01-01-00-00/250867 | fetched |
| 24 | BambuStudio issue 11739 | https://github.com/bambulab/BambuStudio/issues/11739 | fetched |
| 25 | Bambu resolution 0.012 recommendation | search results | snippet |
| 26 | "curve planning uses splines" | search results | snippet |
| 27 | Prusa slice resolution default 0 | search results | snippet |
| 28 | Fusion export tolerance 0.1 mm / 1° | search results | snippet |
| 29 | Fusion help, sketch fillets | https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-ADD-FILLETS | fetch returned 404; facts from snippets |
| 30 | mathgrrl girih tiles | https://mathgrrl.com/hacktastic/2016/03/girih-tiles-for-interactive-islamic-designs/ | fetched |
| 31 | Thingiverse Cordoba | https://www.thingiverse.com/thing:2218796 | fetched (title only) |
| 32 | Printables girih tiles | https://www.printables.com/model/780631-girih-tiles-for-islamic-geometric-patterns | 403 |
| 33 | Etsy Cordoba coasters | https://www.etsy.com/listing/758443317 | 403 |
| 34 | Etsy / Printables / Cults tag pages | search results | snippet |
| 35 | Inkscape stroke to path, round joins | search results | snippet |
| 36 | Broug, line drawing to composition | search results | snippet |
| 37 | Wikipedia Islamic geometric patterns | https://en.wikipedia.org/wiki/Islamic_geometric_patterns | fetched |
