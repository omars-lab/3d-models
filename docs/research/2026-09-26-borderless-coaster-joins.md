---
date: 2026-09-26
produced-by: a Claude research subagent (WebSearch + WebFetch), plus two local renders of bikar's committed minimal-frame coasters at size 80 (`bikar render … --format views --param size=80`, bikar-main at 383c0a1), read by eye
feeds: docs/coaster-borderless-joins-design.md
---

# Borderless coaster joins — sources and what they show

Omar, 2026-09-26: "can we brainstorm different pegging techniques / approaches where we
don't need to even add a border for peg, can re-use frames own border. have a sub agent
research this, consolidate links and create a design.md with approaches".

This file holds the links behind [`../coaster-borderless-joins-design.md`](../coaster-borderless-joins-design.md),
what each one shows, and whether it was actually fetched. Many maker sites (Printables,
MakerWorld, Thingiverse, Instructables) blocked the fetch tool or returned an empty page
shell. For those, all we have is the search-result snippet, and anything taken from them
is marked **search-only**. This is not a full survey of joinery. It covers the sources
listed here and nothing more.

## 1. Fetch status at a glance

| # | Source | Fetched? |
|---|---|---|
| S1 | BOSL2 `joiners.scad` wiki | yes |
| S2 | openGrid board guide (opengrid.world) | yes, but the summary looks unreliable (§3) |
| S3 | Hands On Katie openGrid page | yes, no joint detail on the page |
| S4 | MultiBuild core-parts docs | yes, no tile-to-tile joint detail |
| S5 | 3D Prints Fast "Multiboard parts explained" | yes, no tile-to-tile joint detail |
| S6 | Gridfinity baseplate generator docs (extrabold.tools) | yes |
| S7 | Gridfinity clip-together baseplates (Printables 633086) | **no**, 403 |
| S8 | Protolabs/Hubs interlocking-joints guide | yes |
| S9 | Industrial Monitor Direct dowel-and-slot guide | yes (community grade) |
| S10 | Wikipedia, Butterfly joint | yes |
| S11 | Popular Woodworking, "Butterfly Keys Made Easy" | yes |
| S12 | Wikipedia, Lap joint | yes |
| S13 | Wikipedia, Girih tiles | yes |
| S14 | Lu & Steinhardt 2007, *Science* | **search-only** (abstract snippet) |
| S15 | Rothman-Shore, "The secret of how Magna-Tiles work" | yes |
| S16 | Magnetic tile patents US9636600B2, US12377362B2 | **search-only** |
| S17 | Magnet embedding guides (Kingroon, printpal, Prusa forum, DPHacks) | **search-only** |
| S18 | printpal jigsaw-puzzle guide | **search-only** |
| S19 | Interlocking coaster models (Zesch, Connecting Puzzle Coasters, Instructables) | **no**: 404, 403, and an empty page |
| S20 | Bowtie connector model (Printables 1434242) | **search-only** |
| S21 | BOSL2 dovetail demo (Thingiverse 7301488) | **no**, empty page shell |
| S22 | Tongue-and-groove / overhang notes (Markforged, VoxelMatters) | **search-only**; Markforged 403 |

## 2. Code-CAD joiners

**S1 — BOSL2 `joiners.scad`** — <https://github.com/BelfrySCAD/BOSL2/wiki/joiners.scad> (fetched).
BOSL2 ships half joiners, full joiners, `dovetail()`, `snap_pin()`/`snap_pin_socket()`,
`rabbit_clip()` and `hirth()`. Numbers the page gives:
- `dovetail()`: "`$slop` increases the width of socket by double this amount and depth by
  this amount". So the socket grows by `2·slop` across its width and by `slop` in depth.
  That is the same widening our interlock uses (`coaster-interlock-design.md` §3). The
  default slope is 6, and a taper is an option.
- `snap_pin()`: default clearance 0.2 and preload 0.2. Sizes run from "standard" (L 10.8,
  D 7) down to "tiny" (L 4, D 2.5). Its default orientation is the flat-printable one.
- `rabbit_clip()`: default clearance 0.1, compression 0.1. For the socket depth the page
  says "try 0.4 mm", which is itself a hedge.
- Every joiner here is a separate part or a feature on a full 3D solid. None is
  a height field, and none targets a part only 1.4–2.6 mm thick.

## 3. Grid ecosystems (openGrid, Multiboard, Gridfinity)

**S2 — openGrid board guide** — <https://www.opengrid.world/guides/board/> (fetched).
According to the fetch summary, boards "connect using small plastic pegs that insert into
holes along the edges". Full boards are 6.8 mm thick and Lite boards 4 mm, on a 28×28 mm
grid. It also says connectors use "existing holes" rather than adding a border. **Treat the
connector wording as unverified.** The summary may have paraphrased loosely, and S3 (the
designer's own page) gave no joint geometry to check it against. What the design doc can
use is only the principle, stated as the source states it: the joint lives in features the
board already has.

**S3 — Hands On Katie, openGrid** — <https://www.handsonkatie.com/opengrid> (fetched). The
page says boards "Connect & Screw" and points to connectors on MakerWorld. It gives no
geometry.

**S4 / S5 — Multiboard** — <https://docs.multibuild.io/beginner-section/core-parts-documentation>,
<https://3dprintsfast.com/blog/multiboard-parts-explained> (both fetched). Neither page
describes how tiles join each other. S4: snaps "'snap' into the Large Holes of the MultiBoard
Tiles". S5: tiles mount to the wall with "two-part snaps". The search snippet for S4 lists
Double/Quad Snaps "for connecting two tiles", which would mean one snap straddling holes on
both tiles, but the fetched text did not confirm it (**search-only**). The 12.5 mm / 25 mm
grid numbers also come from the snippet.

**S6 — Gridfinity baseplate generator** — <https://www.extrabold.tools/docs/gridfinity-baseplate>
(fetched). "When Split to Build Plates is on, clip holes along internal seams lock printed
pieces together". A separate clip is packaged with the download. The page gives no
clip dimensions or clearances.

**S7 — Gridfinity clip-together baseplates** — <https://www.printables.com/model/633086-gridfinity-clip-together-baseplates>
(403). The search snippet says the clips are separate parts pushed on "from the bottom",
adding "only 3.4mm" of height, and that to take the grid apart "the clips will in most cases
not be usable again". **Search-only.** Related, all search-only:
<https://makerworld.com/en/models/1034973-gridfinity-base-snapclip-system> (U-shaped clips into
holes at plate edges), <https://www.printables.com/model/430144-gridfinity-base-with-snap-connectors>,
<https://www.printables.com/model/711904-gridfinity-connecting-baseplate-with-press-fit-mag>.

## 4. FDM joint guidance

**S8 — Protolabs/Hubs** — <https://www.hubs.com/knowledge-base/how-design-interlocking-joints-fastening-3d-printed-parts/>
(fetched). It covers finger, dovetail and puzzle joints, and gives FDM a tolerance of
0.5 mm for interlocking parts. It says FDM suits cases "when accuracy and durability are not
critical" and prefers ABS over PLA "due to higher ductility". It is a generic,
process-level figure with no stated printer or joint size.

**S9 — Industrial Monitor Direct, dowel-and-slot** — <https://industrialmonitordirect.com/blogs/knowledgebase/designing-interlocking-joints-for-multi-part-3d-prints-dowel-and-slot-connections>
(fetched; community/vendor grade). It gives a Bambu P1S PLA table: a 6 mm dowel is +0.15
press-fit, +0.25 loose, +0.4 glue-only. It also says horizontal slots "fail catastrophically
in PLA due to 90° overhangs" and to avoid "any geometry where a surface spans >2mm
unsupported at 45° or shallower". These are one author's numbers on one printer.

**S18 — printpal jigsaw guide** — <https://blog.printpal.io/how-to-turn-any-3d-model-into-a-3d-printed-jigsaw-puzzle/>
(**search-only**). The snippet says to start PLA at 0.30 mm clearance and go to 0.40 if too
tight. It describes the knob as "wider at the bulge than at the neck". Our own printed
evidence points the other way: 0.15 mm on the X2D felt "a bit loose" (sample-rules,
minis-03). Generic PLA clearances don't carry over to our printer without a coupon.

**S22 — overhangs** — <https://markforged.com/resources/blog/joinery-onyx> (403), and
<https://www.voxelmatters.com/wave-based-toolpaths-enable-support-free-horizontal-overhangs-in-extrusion-3d-printing/>
(**search-only**). The snippet says a classic tongue-and-groove is "hard for most printers
to make because of the overhang it creates". It cites the usual 45° rule, and research
toolpaths that print 90° overhangs "on unmodified desktop hardware", which is not a slicer
feature we have.

## 5. Woodworking joints

**S10 — Butterfly joint** — <https://en.wikipedia.org/wiki/Butterfly_joint> (fetched). Also
called "bow tie, dovetail key, Dutchman joint, or Nakashima joint": "two dovetails connected
at their narrow ends", inlaid into a cavity, often in a contrasting wood. The article hedges
on its purpose: "mainly used for aesthetics, but they can also be used to reinforce cracks".

**S11 — Popular Woodworking** — <https://www.popularwoodworking.com/techniques/butterfly-keys-made-easy/>
(fetched). Wing angles "anything between 8 and 10° looks and works great". Side bevel about
1°, eased to 0.5° in maple and 2° in fir or pine. Keys "at least 1/4″ thick". Pocket depth
"roughly 1/16″ less than the thickness of the key". Keys should be "designed to suit the job
at hand". All of this is about hand-fitted wood, glued in.

**S12 — Lap joint** — <https://en.wikipedia.org/wiki/Lap_joint> (fetched). In a half lap,
"material is removed from both of the members so that the resulting joint is the thickness
of the thickest member". Its strength comes from glue: "two long-grain wood faces are joined
with glue". The page also lists a dovetail lap "that resists withdrawal".

## 6. Tiling where the art crosses the seam

**S13 — Girih tiles** — <https://en.wikipedia.org/wiki/Girih_tiles> (fetched). The set has
five equal-edged tiles: decagon, elongated hexagon, bow tie, rhombus and pentagon. Their
strap lines "cross the boundaries of the tiles at the center of an edge at 54°", so the
pattern flows unbroken from tile to tile. The article hedges on what craftsmen knew: "there
is no indication of how much more the architects may have known about the mathematics
involved".

**S14 — Lu & Steinhardt 2007** — <https://www.science.org/doi/10.1126/science.1135491>; PDF
<https://paulsteinhardt.org/wp-content/uploads/2023/01/LuSteinhardt2007.pdf> (**search-only**).
The paper argues that by 1200 C.E. girih patterns were "reconceived as tessellations of
equilateral polygons … decorated with lines". A published comment disputes parts of it:
<https://www.science.org/doi/abs/10.1126/science.1146262>.

## 7. Magnets

**S15 — Magna-Tiles** — <https://rothmanshore.com/2013/03/03/the-secret-of-how-magna-tiles-work/>
(fetched). Each edge holds two magnets with their poles pointing up and down: "if the one on
the left has North pointing up, the one on the right has North pointing down. This continues
around all four edges". So "there is no way to place two Magna-Tiles next to each other such
that the magnets are facing the opposite direction", and any edge joins any edge. This is
the magnet version of our self-mating half-edge rule (D-069).

**S16 — patents** — <https://patents.google.com/patent/US9636600B2/en>,
<https://patents.google.com/patent/US12377362> (**search-only**). The snippets describe fixed
alternating magnets, and cylinder magnets "given enough clearance to rotate" in a cavity so
they turn to attract.

**S17 — embedding magnets in prints** (**search-only**):
<https://kingroon.com/blogs/3d-printing-guides/how-to-embed-magnets-into-3d-prints>,
<https://printpal.io/resources/how-to-easily-add-magnets-to-your-3d-prints>,
<https://forum.prusa3d.com/forum/how-do-i-print-this-printing-help/how-to-safely-insert-magnets-into-a-print/>,
<https://dphacks.com/2025/11/02/how-to-add-hidden-magnets-to-3d-prints/>. Two methods: pause at
a layer to bury the magnet, or press it into an open pocket. For a 10 mm magnet, one snippet
says a 10.1–10.2 mm hole is "large enough to push magnets easily in, while still ensuring
enough of a press-fit", and warns that "Clearance for PETG might not fit the same as PLA".
None of these sources gives the side-by-side pull between two small disc magnets 1–2 mm
apart, which is the number a coaster join would need.

## 8. Interlocking coasters and bowtie connectors

All **not fetched** (404/403/empty):
<https://www.thingiverse.com/thing:145345> (Zesch interlocking coasters, "interlock in a
hexagonal grid", per the snippet),
<https://www.printables.com/model/966057-connecting-puzzle-coasters>,
<https://www.instructables.com/Interlocking-Coaster-Pattern-a-Fun-and-Functional-/>,
<https://www.printables.com/model/1434242-bowtie-connector> (the snippet calls it "a small part
to connect 2 parts together", which "can be … used as a negative modifier"). From the
snippets, the coaster sets join with jigsaw-style knobs. We could not check whether any of
them joins through the coaster's own openings.

## 9. Repo-internal sources

- [`../coaster-interlock-design.md`](../coaster-interlock-design.md): the shipped dovetail
  (D-069). It covers the half-edge pairing (§2), the exact outer wall and why a grid
  staircase wall carries up to ±0.2 mm of stair per face (§5.3), CV8/CV9 (§6), and the
  neck bet CAL-CST-06 (§10).
- [`coaster-interlock-study.md`](coaster-interlock-study.md) §3: alternating tab/slot edges
  tile by translation on the hexagon only.
- [`../tile-wall-design.md`](../tile-wall-design.md) §4: a separate `CornerClip` that drops
  into a `clipseat` recess across the joint. This is the repo's own precedent for a separate
  connector.
- bikar `docs/design/coaster-openwork.md` §3: `frame ≥ depth + clearance + 1.6`, the
  pegs files' `+ 2.5`, and the refusal of a bottom `edge` under openwork (§4).
- [`../../.claude/skills/print-coaster-samples/sample-rules.md`](../../.claude/skills/print-coaster-samples/sample-rules.md):
  minis-03 feedback ("big spaces between the patterns", "a bit loose" at 0.15) and the
  ~11 mm mated band.

## 10. Local renders (this session)

The top views of `GimTvN9hw4U-minimal-frame-coaster.bkr` and
`7apC5Q9QS-8-minimal-frame-coaster.bkr` at `size=80` show the pattern over the outline. The
frame is not drawn. All readings below are **by eye** off a 900 px raster, roughly ±1 mm:

- **GimTvN9hw4U (hexagon, six-fold).** On every flat, the outer rosette hexagons touch the
  frame near the quarter points of the edge, and the art pulls away at the **edge
  midpoint**. That leaves an opening roughly 8–12 mm wide along the frame's inner edge and a
  few mm deep. The 6-fold mirror line through each edge midpoint means the neighbour's
  opening is the mirror image of ours across the seam.
- **7apC5Q9QS-8 (square, eight-fold).** The art carries its own straps parallel to each
  edge, 1–2 strap widths inside it. At each edge midpoint there is only a small opening, very
  roughly 7 mm wide and about 2 mm deep. That is much less room than the hexagon has.

Nothing was measured with a tool and nothing was printed.
