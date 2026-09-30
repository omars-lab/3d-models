---
date: 2026-09-29
produced-by: researcher A subagent (Claude Opus 5.5), one of two independent passes — WebSearch, WebFetch, the Printables GraphQL API for maker listings, `pdftotext` on the two Kaplan papers, a read of the Bambu Studio process profiles shipped in the app on this machine, and local renders of bikar-main at e2b65c4 (read-only) measured with `docs/design/coaster/smooth-lines-media-a/make_figures.py`
feeds:
  - docs/design/coaster/smooth-lines-design-a.md
---

# Smoother coaster lines — sources and measurements (researcher A)

Omar, 2026-09-29: "when it comes to our lines... put together options for making them smoother.
Web search and prepare a design.md with options and screenshots we can review in Obsidian. One of
the options should be lines influenced by the SKIMS font design."

This file holds the raw findings behind
[`../design/coaster/smooth-lines-design-a.md`](../design/coaster/smooth-lines-design-a.md).
Each web source says whether the page was **fetched** (its text was read through WebFetch, which
returns a summary of the page, so a quote below is as the fetch returned it) or **snippet** (only a
search-result summary was seen — a lead, not a fact). Quotes are kept under 15 words. It covers the
pages listed here and nothing else; it is not a survey of everything written on the subject.

## 1. Our own measurements (read, not searched)

Coaster: CS-2, `bikar/patterns/Constructions/7apC5Q9QS-8-minimal-coaster.bkr`, size 90,
rendered to STL, SVG and previews (round 0, 1, 1.5) with the bikar CLI into a scratch folder.
The crop every comparison uses is centred at (−8.3, −19.5) mm, 12 mm across, holding one star hole
with acute points.

| What | Number | How it was measured |
|---|---|---|
| Grid the kernel samples on | 0.4 mm, origin at 0.2 mod 0.4 | kernel constant `COASTER_GRID_PITCH_MM` (bikar coaster.ts L200); origin recovered from the STL's bottom-face vertices |
| Simulated grid vs the real STL | differ by 0.16 mm² (one cell) in the crop | cells whose centre lies inside the exact shape, compared with the union of STL bottom triangles |
| Today's edge vs the exact outline | largest 0.42 mm, typical 0.137 mm | points every 0.05 mm along the STL outline, distance to the exact offset of the straps |
| The 0.42 mm | a lone diagonal cell left hanging off a star-hole point | read in the picture (fig01) |
| 0.2 mm grid | largest 0.13, typical 0.052 | same simulation, finer pitch |
| 0.1 mm grid | largest 0.07, typical 0.030 | same |
| Marching squares at 0.4 mm | largest 0.19, typical 0.006 | contour of the signed field at the same 0.4 mm samples |
| Exact offset | 0 | by construction |
| Slicer-style simplify of today's steps, 0.2 mm tolerance | largest 0.42, typical 0.102 | shapely Douglas–Peucker on the STL outline |
| Same, 0.3 mm tolerance | largest 0.34, typical 0.106 | same |
| Facet gap on a 1.5 mm radius | 0.114 / 0.029 / 0.007 / 0.002 mm at 2 / 4 / 8 / 16 flats per quarter turn | r·(1 − cos(π/4n)) |
| Symmetry, today (whole coaster, symmetric sample grid) | 100% turned 90°, 100% mirrored | overlap of the solid mask with itself turned and mirrored |
| Pen held at one angle (30°, widths 1.8–3.4 mm) | 84% turned, 89% mirrored | same measure |
| Pen turned with the pattern | 100% / 100% | same |
| SKIMS-influenced light (joins blended 0.6 mm, 2.7 mm waist) | 100% / 100% | same |
| SKIMS-influenced strong (1.2 mm, 2.4 mm waist) | 100% / 100% | same |
| Curvature, circular fillet r 1 on a 90° corner | steps 0 → 1/mm → 0 | analytic |
| Curvature, quartic curvature-continuous blend over the same corner | ramps 0 → about 2.1/mm → 0 | sampled along the curve (fig04) |

Read in the renders (fig07b): at round 1 and 1.5 the top round-over also follows the grid — its
top edge shows the same saw-tooth as the wall, because the kernel's round-over (`topEdgeDrop`) is
evaluated at cell centres.

Read in the code (bikar-main at e2b65c4, `bikar/packages/core/src/kernel3d/coaster.ts`):

- L191–199: the pitch's reason — "the finest lateral feature the nozzle can place, so sampling at
  the perimeter width resolves every strap the machine can actually lay down."
- L1598 `assembleFlatBased`: the plain coaster is cell tops (`emitTopCells`), one vertical wall per
  cell-staircase loop (`boundaryLoops`, `emitWall`), and a flat bottom.
- L2180 `assembleInterlock`: the interlock coaster already builds one exact wall (`emitExactWall`)
  and joins it to the cell tops with a collar (`emitCollar`) — the in-house precedent for an exact
  edge.
- L864 `topEdgeDrop`: the round-over is a function of distance to the strap edge (`signedInset`),
  sampled per cell.

Read on disk: Bambu Studio app bundle, profiles/BBL/process/fdm_process_common.json,
line 102 has `"resolution": "0.012"`, the slicer's contour-simplify tolerance that the X2D process
presets inherit.

## 2. SKIMS wordmark — traits and who drew it

| Source | Status | What it says |
|---|---|---|
| [mojomox — SKIMS font](https://mojomox.com/skims-font) | fetched | "thick and even with no real thick-to-thin variation"; "the terminals are fully rounded"; "very tight spacing"; "a bit of irregularity"; custom, not a retail font |
| [1000logos — SKIMS logo](https://1000logos.net/skims-logo/) | fetched | introduced end of 2019; a stylized bubble-style font, slanted; names TPG DontBlurry, Spilled Ink and Outahere as similar faces |
| [dafont forum 423073](https://www.dafont.com/forum/read/423073/skims) | fetched | the one real reply: "This is most probably not a font" |
| [designyourway — SKIMS logo](https://www.designyourway.net/blog/skims-logo/) | fetched | calls it custom, "geometric with subtle humanist touches" — conflicts with mojomox's hand-made reading |
| [Wikipedia — Skims](https://en.wikipedia.org/wiki/Skims) | fetched | Kanye West credited as "Ghost Creative Director" and for creating the logo |
| [Complex — Kanye West SKIMS logo explainer](https://www.complex.com/style/a/tracewilliamcowen/kanye-west-skims-logo-explainer) | fetched | dated 2025-04-10; quotes Kim Kardashian, "For SKIMS, he drew the logo"; Ye later credited Vanessa Beecroft for where SKIMS "came from" |
| [logotyp.us — SKIMS](https://logotyp.us/logo/skims/) | fetched | conflicts with the other sources on attribution; treated as unreliable |
| [Wikipedia — Yorgo Tloupas](https://en.wikipedia.org/wiki/Yorgo_Tloupas) | fetched | checked because a snippet linked him; the page does not mention SKIMS |
| [King & Partners — SKIMS](https://www.kingandpartners.com/work/skims/) | fetched | brand framework and website work; does not say who drew the wordmark |
| search results for "Kanye drew SKIMS logo by hand" and "Kimono bubble font" | snippet | that he drew it by hand, and that he designed the earlier Kimono bubble lettering — not confirmed by a fetched page |

What the sources agree on: heavy strokes of even weight, fully rounded ends, tight spacing, a soft
bubble feel, a slight slant and hand-made irregularity. Who drew it: Kim Kardashian's 2019
statement credits Ye (fetched, via Complex and Wikipedia); the hand-drawn detail is snippet only.

No SKIMS image was copied into the repo. The trait sheet in fig06 is drawn from scratch.

## 3. Slicer and printer

| Source | Status | What it says |
|---|---|---|
| [OrcaSlicer wiki — quality settings, precision](https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_precision) | fetched | the G-code path is made after simplifying the model's contour; smaller resolution = more points, slower slicing |
| OrcaSlicer resolution default | snippet | 0.012 mm per a search summary; the Bambu Studio value is confirmed on disk, §1 |
| [Bambu forum — curve planning silently turns off arc fitting](https://forum.bambulab.com/t/curve-planning-silently-turns-off-arc-fitting-in-bambu-studio/253630) | fetched | Bambu Studio "silently turns off Arc Fitting" when curve planning is present; one user reports about 20% shorter prints with arc fitting back on |
| [Bambu forum — warning message issue](https://forum.bambulab.com/t/warning-message-issue/251897) | fetched | X2D users see "The software has automatically disabled arc fitting." |
| [Bambu forum — arc fitting on H2S](https://forum.bambulab.com/t/arc-fitting-on-h2s-on-or-off-studio-warns-to-disable-but-its-on-by-default/252893) | fetched | `enable_arc_fitting` is "1" in the default profiles; only some profiles turn it off |
| [BambuStudio issue #11739](https://github.com/bambulab/BambuStudio/issues/11739) | fetched | question about arc fitting vs curve planning; no developer answer at fetch time |

Consequence for us: arc fitting turns short straight moves into arcs; it cannot turn a 0.4 mm
staircase into a slope, because the staircase is in the model, and on the X2D it is switched off
anyway. The resolution setting simplifies contours; our Douglas–Peucker trial (§1) shows a loose
tolerance leaves a jagged, still-wrong edge rather than a smooth one. Bambu's own simplifier was not
read, so this rests on the assumption that it behaves like Douglas–Peucker.

## 4. How FDM prints corners and small features

| Source | Status | What it says |
|---|---|---|
| [tchncs discussion](https://discuss.tchncs.de/post/9917920) | fetched | outside corners print with a radius "roughly equal to half the extrusion width"; inside corners can be sharp |
| [3DVerkstan — designing for 3D printing](https://support.3dverkstan.se/article/38-designing-for-3d-printing) | fetched | "impossible to create a perfectly sharp outer corner" with a round nozzle |
| [Hydra Research design rules](https://www.hydraresearch3d.com/design-rules) | fetched | minimum feature ">1.8 mm or 4 times extrusion line width"; thin walls >0.9 mm |
| [UltiMaker — design for FFF](https://ultimaker.com/learn/design-for-fff-3d-printing-maximize-your-success/) | fetched | minimum wall about 0.5 mm |
| [littleboxes — rounded vs sharp corners](https://littleboxes.ai/blog/rounded-corners-vs-sharp-corners-3d-printing) | fetched | top-rim radii kept to about 1 mm or less |
| [Hubs — STL files step by step](https://www.hubs.com/knowledge-base/3d-printing-stl-files-step-step-guide/) | fetched | smaller chord height = smoother surface; suggests chord height near 1/20 of layer height and a 15° angle tolerance |
| [RapidDirect — sharp corners in CNC](https://www.rapiddirect.com/blog/sharp-corners-in-cnc-machining/) | fetched | a milled inside corner is rounded by the tool radius — the laser/CNC analogue of our hole points |

Transfer note (K10): "outside corners round to half the bead width" transfers to our strap bends
because it is about the nozzle, which is the same 0.4 mm nozzle on the X2D. "Inside corners can be
sharp" transfers to our hole points with a hedge: it holds when the slicer's perimeter path reaches
into the point, which a 3 mm strap around a narrow star point does, but it was not seen on a print.

## 5. Geometry methods

| Source | Status | What it says |
|---|---|---|
| [OpenSCAD manual — offset](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations) | fetched | `offset(r=…)` rounds corners, `offset(delta=…, chamfer=…)` keeps or cuts them |
| [Clipper2 — InflatePaths](https://www.angusj.com/clipper2/Docs/Units/Clipper/Functions/InflatePaths.htm) | fetched (thin page) | polygon offset with round, square and mitre joins, and a mitre limit |
| [Wikipedia — Marching squares](https://en.wikipedia.org/wiki/Marching_squares) | fetched | contour from grid samples, with the edge placed by interpolation along each cell side; saddle cells are ambiguous |
| [Inigo Quilez — smooth minimum](https://iquilezles.org/articles/smin/) | fetched | blends two distance fields; the polynomial family "is not associative" — the order of blending matters |
| [Autodesk Alias — G0 G1 G2 G3 continuity](https://help.autodesk.com/cloudhelp/2026/ENU/Alias-Video-Tutorials/files/essential-concepts/continuity-g0-g1-g2-g3.html) | fetched (may be paraphrased by the fetch) | G1 = matching direction, G2 = matching curvature too, which reads as a smoother highlight |

The non-associativity matters for us: blending strap fields one at a time would give a different
result depending on the order the straps come in, which would break symmetry. The prototype blends
only the two nearest straps at each point (sorted), which is order-free; the whole-coaster symmetry
check in §1 confirms it on CS-2.

## 6. Islamic strapwork — the traditional reading

| Source | Status | What it says |
|---|---|---|
| [Kaplan & Salesin 2004, Islamic star patterns in absolute geometry](https://grail.cs.washington.edu/wp-content/uploads/2015/08/kaplan-2004-isp.pdf) | fetched (PDF, read with pdftotext) | "Where two thickened line segments meet, we must perform a mitered join"; interlaced strands pass "alternately over and under" |
| [Kaplan 2017, Interwoven Islamic geometric patterns (Bridges)](https://cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2017.pdf) | fetched (PDF) | 3D-printed interwoven pattern sculptures; a geometric "bulging" operation that turns the flat bands into rounded, undulating forms |

Reading: the textbook strap is a band of constant width with mitred (sharp) joins. Rounded and
bulged forms are a documented, deliberate departure (Kaplan 2017), not a corruption of the reading.

## 7. What other makers do

Printables listings read through its public GraphQL API (fetched, description and print settings):

| Listing | What it says about line smoothness |
|---|---|
| [231256](https://www.printables.com/model/231256) | nothing on edges |
| [231263](https://www.printables.com/model/231263) | nothing on edges |
| [1692055](https://www.printables.com/model/1692055) | nothing on edges |
| [1183439](https://www.printables.com/model/1183439) | nothing on edges |
| [304764](https://www.printables.com/model/304764) | nothing on edges |
| [780631](https://www.printables.com/model/780631) | nothing on edges |
| [13025](https://www.printables.com/model/13025) | nothing on edges |
| [805376](https://www.printables.com/model/805376) | nothing on edges |
| [1230673](https://www.printables.com/model/1230673) (Arabesque/Girih coasters) | offered in "square and round corners" versions — the outline, not the straps |
| [1231426](https://www.printables.com/model/1231426) | nothing on edges |
| [1235334](https://www.printables.com/model/1235334) | nothing on edges |
| [858209](https://www.printables.com/model/858209) | 0.12 mm layers "for sharp detail" |

None of the 12 Printables listings surveyed here describes smoothing a stepped edge, fillets on
hole points, or arc fitting. Their models come from CAD or vector tools, so most likely have exact
edges to begin with — an inference, not something the listings say.

Snippet only (pages returned 403 to WebFetch): [Thingiverse 2218796](https://www.thingiverse.com/thing:2218796)
and [Thingiverse 2772588](https://www.thingiverse.com/thing:2772588/files) appear to be OpenSCAD
pattern generators with a line-width knob; [Etsy 758443317](https://www.etsy.com/listing/758443317/islamic-geometric-pattern-coasters-1)
is a laser-cut Islamic coaster set. No maker images were copied into the repo.
