<!--
  Research produced 2026-08-04 by Claude (Opus 5) under the 3d-models
  design-doc rules, as the second half of the text-emit investigation.
  The first half is text-emit-survey.md, which measured the single-stroke
  centreline route; this file measures the outline-font route it never
  considered, and refutes two of that file's sections.
  Sources: eight font files already present on this machine, read with
  fontTools; first-hand measurement of those files by the scripts in §7,
  run on this machine on 2026-08-04; and the web sources in §8, all of
  which are documentary and none of which supply a number used here.
  Feeds: docs/text-emit-design.md — specifically the route choice, the
  three bake-time checks, and the layout validator.
  NOTHING WAS PRINTED and no slicer was run. Every number below is
  measured from font data. The one number that is about the machine —
  the 0.4 mm nozzle — is a stated parameter, not a measurement, and §5
  says what happens when it is wrong.
-->

# The outline-font route: measured over eight faces, 296 glyphs

## 0. Why this file exists

[`text-emit-survey.md`](text-emit-survey.md) asked how to turn a **single-stroke
centreline** glyph into printable geometry, measured that it cannot be done
without a polygon offset, measured that the offset breaks, and laid out four
routes for getting an offset. Every one of those routes is a way to acquire
machinery this repo does not have.

None of them was necessary. A TrueType or CFF glyph is not a centreline; it is
already **a set of closed contours, with counters as holes**. There is nothing to
offset, so there is nothing to union. That is what OpenSCAD's `text()` +
`linear_extrude` is, and the survey's §4 talked itself out of it on a premise
about *font matching* that never applied to *outline extraction*.

This file measures the outline route the way the survey measured the centreline
one: on the actual glyph data, on the actual 37 characters a rung label needs,
and — the part that matters — **on the quantised bytes that would ship**, not on
the ideal curve, because quantisation can itself create a crossing.

| # | Question | Answered by | Kind of answer |
|---|---|---|---|
| 1 | Do outline glyphs really need no union? | §2 | **Measured — per font, and one font says no** |
| 2 | What does the payload cost against a single-stroke font? | §3 | **Measured** |
| 3 | Does the shipped, quantised data survive the checks an extruder needs? | §4 | **Measured — six pass, one finds a real modelling gap** |
| 4 | What is the thinnest thing a 0.4 mm nozzle has to lay down? | §5 | **Measured** |
| 5 | What actually binds — glyph geometry, or something else? | §6 | **Measured, and the answer is something else** |
| 6 | Which face can this project legally ship? | §2 | Documentary, from each font's own `name` table |

## 1. What was measured, and on what

Eight faces, all already on this machine; **nothing was downloaded for this
work**. Licence is read from each font's own `name` table (ID 13), not from a
web page.

| Face | File | Licence, per its `name` table |
|---|---|---|
| Arial Bold / Regular | `/System/Library/Fonts/Supplemental/` | proprietary (Monotype) — **measure-only** |
| Verdana Bold | `/System/Library/Fonts/Supplemental/` | proprietary (Microsoft) — **measure-only** |
| Tahoma Bold | `/System/Library/Fonts/Supplemental/` | proprietary (Microsoft) — **measure-only** |
| Source Code Pro Bold / Regular | a local checkout | SIL Open Font License 1.1 (Adobe) — **shippable** |
| DM Sans, wght 400 and 700 | a local variable font, instanced with `fontTools.varLib.instancer` | SIL Open Font License 1.1 (Colophon Foundry / Google) — **shippable** |

The four proprietary faces are in the table because a claim of the form *"outline
fonts do not need a union"* is a claim about a **set** (K2), and a set of two
shippable families is too small to say anything about. They are measured as
reference points and cannot be shipped. **The shipping candidates are Source Code
Pro and DM Sans, and nothing else here.**

Every face is compared **at the same cap height** — 5.0 mm, the scale set from
that face's own measured `H` bounding box, so a face with a large em square is not
penalised. Character set: `0`–`9`, `A`–`Z` and `-` — 37 glyphs, the alphabet a
rung label needs. Curves are flattened to 0.01 mm of chord for measurement and
0.05 mm for shipping (§3).

## 2. Do outline glyphs need a union? Six faces say no; DM Sans says yes

A closed contour needs no union **as long as no two of a glyph's contours cross
each other, and no contour crosses itself.** That is a property a font either has
or does not — TrueType permits overlap and renderers resolve it by the non-zero
winding rule, so a font is under no obligation to avoid it.

Over 296 glyphs:

| Face | Glyphs whose contours cross | Which |
|---|---|---|
| Arial Bold, Arial Regular | 0 | — |
| Verdana Bold, Tahoma Bold | 0 | — |
| Source Code Pro Bold, Regular | 0 | — |
| **DM Sans Bold (wght 700)** | **5 of 37** | `A` `B` `H` `Q` `R` |
| **DM Sans Regular (wght 400)** | **5 of 37** | `A` `B` `H` `Q` `R` |

Totals across all eight faces: 2 self-intersections and 28 cross-contour
intersections, all of them in DM Sans. Per glyph, as (self, cross), identical at
both weights: `A` (0, 4) · `B` (1, 0) · `H` (0, 4) · `Q` (0, 4) · `R` (0, 2).

### 2a. This table was measured twice, and the first measurement was wrong

The rows above are the **second** measurement. The first, taken by the script in
§7 when this file was written, said `6 of 37` — `A B H Q R Y` — and `4`
self-intersections. Re-derived on 2026-08-04 by an independent implementation
(`bikar:scripts/bake-glyphs.py`, written from this file's §3 and §4 without
reusing §7's crossing code), stable across chord tolerances 0.01 / 0.002 / 0.001
/ 0.0005 and 3 / 6 decimal places:

- **`Y` does not cross, at either weight.** It is a *single* contour of 9
  points, all straight lines — `DecomposingRecordingPen` yields
  `moveTo, lineTo ×9, closePath` and nothing else. Of its non-adjacent segment
  pairs, only two have even overlapping bounding boxes and neither meets
  transversally. A glyph with one convex-cornered simple contour has nothing to
  cross.
- **`B` self-intersects, and the first measurement never named it.** Ring 0
  (87 points, depth 0), segment 40 `(0.67121, 0.51382) → (0.65527, 0.51688)`
  properly crosses segment 46 `(0.66047, 0.51459) → (0.68922, 0.52411)` — a
  ~0.03-cap-height tangle at the waist where the two bowls meet, 0.15 mm at a
  5 mm cap. It is exactly the class of defect B1 exists to catch, and it is
  invisible at any rendering size.

The two counts that changed are both small; **the count that did not change is
the large one.** 28 cross-contour intersections is agreed by both
implementations, which is what makes the disagreement on the other two credible
rather than a wholesale methodology gap: had the crossing predicates differed in
kind, 28 would not have survived.

The lesson is narrower than "check your work". Both scripts share one
methodology and one author; what caught the error was a *reimplementation with a
different purpose* — the bake, which had to produce the failing fixture and so
had to name the failing glyphs one at a time. An aggregate ("6 glyphs cross")
carries no obligation to be right about any particular member, and that is the
same substitution CLAUDE.md's D2 note warns about: **an aggregate cannot
discharge a claim about every part.**

**DM Sans draws `H` as three overlapping rectangles** — two stems and a crossbar,
each a separate closed contour, with four proper crossings where the bar meets
the stems. A renderer fills that correctly. An extruder that treats each closed
contour as one ring of a solid does not: it produces three interpenetrating
prisms and two internal walls that should not exist.

So the honest claim is **not** "outline fonts need no union". It is:

> Of the eight faces measured here, six need no union for these 37 glyphs, and
> two do. Whether a given font needs one is a property of that font, and is
> checkable.

This is the K2 discipline applied to a conclusion I wanted to be general and is
not. It also settles where the check belongs: §3 puts the flattening in a
**build-time** script, so the rare union — if a face that needs one is ever
chosen — runs once in Python and never in bikar.

## 3. What it costs: bake at build time, ship coordinates

The survey's §4 compared "a TTF parser plus a font file" against "coordinates".
That comparison is avoidable. Flatten the 37 glyphs' contours **once, in the
build**, and what ships is coordinates in both cases.

Measured with `fontTools.subset` for the TTF column and by baking flattened
contours at cap height 1.0, rounded to 3 decimals, for the rest:

| Font | Subset TTF | Baked, 5 dp | **Baked, 3 dp** | gzipped | Rings | Points |
|---|---|---|---|---|---|---|
| Arial Bold | 25,532 | 17,390 | **13,710** | 4,139 | 51 | 986 |
| Source Code Pro Bold | 6,936 | 22,823 | **17,935** | 5,170 | 52 | 1,291 |

Reference: the whole `hersheytext.json` is **476,882** bytes; the survey's §5.1
measures its `futural` face, minified to the 95 glyphs it needs, at **7,503**
bytes.

So the outline route's payload is roughly **1.8×–2.4× a single-stroke face**, for
a route with no offset in it — against the survey's four routes, each of which
adds a polygon-offset or union implementation to the engine. At 3 decimal places
the quantum is 0.001 of a cap height, or **5 µm at a 5 mm cap** — two orders below
anything a 0.4 mm nozzle resolves.

Three consequences worth stating plainly, because each one is a cost the survey
assumed and this measurement removes:

1. **No runtime font parser.** Not `opentype.js` (~120 KB), not FreeType, not a
   WASM port. The parser is `fontTools`, it runs in the build, and it does not
   ship.
2. **bikar's zero-runtime-dependency position is untouched.** The 2026-05-07
   decision that produced `packages/core/src/kernel3d/earcut-vendored.ts` —
   vendor a small single-purpose thing rather than take a dependency — is
   *satisfied*, not strained, by a constant.
3. **The CLI and the browser get identical geometry**, because they get identical
   numbers. The survey's §4 worry about a `text` feature behaving differently in
   the Lab and the CLI was the right worry, and baking is the answer to it.

## 4. Does the shipped data survive? Six checks on the quantised bytes

Checks are run on the **flattened, rounded rings that would ship**, not on the
font's curves, because rounding can move a point across a neighbour.

| # | Check | Why an extruder needs it |
|---|---|---|
| Q1 | No ring self-intersects | a self-crossing ring has no well-defined inside |
| Q2 | No two rings of a glyph cross | §2's property, re-checked after quantisation |
| Q3 | Every non-outer ring lies strictly inside the outer one | the outline+holes model assumes it |
| Q4 | No zero-length edges | degenerate triangles downstream |
| Q5 | Ring-to-ring clearance > 0 | two rings that touch are one ring |
| Q6 | Holes wind opposite to the outer ring | earcut reads winding to tell hole from island |

| Face | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Min ring clearance | Shortest edge |
|---|---|---|---|---|---|---|---|---|
| Arial Bold | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 0.5622 mm | 0.1553 mm |
| Verdana Bold | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 0.6139 mm | 0.0200 mm |
| Tahoma Bold | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 0.6100 mm | 0.0200 mm |
| **Source Code Pro Bold** | ✓ | ✓ | ✓ | ✓ | ✓ | **fails on `0`** | 0.5680 mm | 0.0200 mm |

### 4.1 The one failure is not a font defect — it is a modelling gap

Source Code Pro Bold's `0` is a **dotted zero**: an outer shell, a counter inside
it, and *a dot inside the counter*. Three rings, nested **two** deep. The Q6
implementation assumed "the largest-area ring is the outer one and every other
ring is a hole", which is the `outline + holes` shape — and under that assumption
the dot is a hole, so its winding is wrong.

The dot is not a hole. It is ink at depth 2. The failure is in the model, not the
font, and it is worth having found here rather than in a mesh:

- **`solidifyExtrudedPiece` cannot represent it either — and cannot represent a
  glyph at all.** Its signature is
  `solidifyExtrudedPiece(outline, holes: PieceHoleSpec[], depth)` in
  `packages/core/src/kernel3d/solidify-piece.ts`, and `PieceHoleSpec` is
  `{name, x, y, bands: {d, from, to}[]}` — **holes are circles**, given as a
  centre and a stack of diameters. There is no polygonal hole in that API, so
  "reuse the piece extruder" is not an option for text, for any font, dotted zero
  or not.
- **The reusable part is one level down.** The same file's cap builder already
  lays a section out as *"outline vertices then each hole ring, reversed so earcut
  reads it as a hole"* with earcut's `holeIndices`, plus a deviation check and
  sliver absorption. That machinery takes arbitrary polygons. It is the *hole
  spec*, not the triangulator, that is specialised to circles.
- **Nesting depth is therefore a design input, not an edge case.** Either the
  emitter carries depth (even ring depths are ink, odd ones are holes — which is
  exactly the even-odd rule), or a face with a dotted zero is rejected at bake
  time with a message that says which glyph and why. Silence is the one option
  that is not available.

## 5. What the nozzle has to lay down: bold is not folklore, it is 1.7×

"Thinnest stroke" is not well defined on an outline glyph — a stroke has no
centreline to measure across. What *is* well defined is the thinnest sustained
stem, and it can be measured directly:

> Rasterise the glyph's ink under the non-zero winding rule. Take the Euclidean
> distance transform **of the ink mask**. Binary-search the erosion radius `r` at
> which the number of connected components of `{ink : dist ≥ r}` changes. `2r` is
> the thinnest sustained stem, and it is exactly the widest bead that can be laid
> along that stem without leaving the ink.

At a 5.0 mm cap height, over all 37 glyphs:

| Face | Thinnest stem | Where | Glyphs under a 0.4 mm nozzle |
|---|---|---|---|
| Tahoma Bold | 0.764 mm | `3` | none |
| Verdana Bold | 0.735 mm | `3` | none |
| DM Sans Bold | 0.645 mm | `5` | none |
| Arial Bold | 0.600 mm | `3` | none |
| Source Code Pro Bold | 0.573 mm | `W` | none |
| Arial Regular | 0.431 mm | `5` | none |
| DM Sans Regular | 0.412 mm | `8` | none |
| **Source Code Pro Regular** | **0.377 mm** | `6` | **`3` `5` `6` `9`** |

Bold faces sit at 0.57–0.76 mm; regular faces at 0.38–0.43 mm. That is a **1.7×
spread across the same cap height**, and it is the whole of the "use a bold face"
advice, stated as a number instead of a preference.

The failure mode is not thin ink; it is **ink that stops being connected**. Eroding
by half a nozzle width:

| Glyph | SCP **Bold** | SCP **Regular** |
|---|---|---|
| `3` | 0.699 mm, stays 1 island | 0.394 mm, **breaks into 6 islands** |
| `5` | 0.699 mm, stays 1 island | 0.394 mm, **breaks into 3 islands** |
| `6` | 0.577 mm, stays 1 island | 0.377 mm, **breaks into 2 islands** |
| `9` | 0.595 mm, stays 1 island | 0.377 mm, stays 1 island |

Six islands is what a `3` looks like when the printer has laid the parts of it
that fit and nothing joining them.

**This is measured at a stated 0.4 mm nozzle and a stated 5 mm cap, and both
scale.** The number that transfers is not "0.4 mm" but the ratio: a face whose
thinnest stem is under one nozzle width at the cap height in use will break up,
and both inputs are knobs. Nothing here was printed; what is measured is the
geometry the slicer is handed, and a real print is the thing that would outrank
it.

## 6. The constraint that actually binds is the space *between* letters

Every glyph in every bold face above clears the nozzle comfortably. Laid out as
real strings — kerned, at a 5 mm cap — they do not.

Minimum gap between two ink islands anywhere in the laid-out label:

| Label | Arial Bold | Source Code Pro Bold |
|---|---|---|
| `MC-2 R08` | 0.669 mm at `-2` | 0.878 mm at `R0` |
| **`MC-4 R12`** | **0.181 mm at `-4`** | 0.752 mm at `R1` |
| `LG-B2` | 0.563 mm at `-B` | 0.898 mm at `B2` |
| `W-F1` | 0.566 mm at `-F` | 1.342 mm at `-F` |
| `0000` | 0.638 mm at `00` | 0.859 mm at `00` |
| `AVA` | 1.217 mm at `AV` | 1.622 mm at `AV` |
| **`WWW`** | **0.031 mm at `WW`** | **0.061 mm at `WW`** |

Three things follow, and the third is the one that changes the design:

1. **A real label already fails.** `MC-4 R12` is a machine-card rung label this
   project wants, and in Arial Bold at a 5 mm cap the hyphen and the `4` are
   0.181 mm apart — under half a nozzle width. Two beads laid on either side
   merge, and the label reads `MC4`.
2. **The monospace face is the robust one.** Source Code Pro Bold clears 0.4 mm on
   every real label by a factor of ~1.9 or better; its only failure is the
   synthetic `WWW`, which no label contains. The best-behaved shippable face is a
   monospace, which is a slightly unglamorous answer and is what the measurement
   says.
3. **No per-glyph check can see this.** The gap is a property of *the string* —
   which glyphs are adjacent, and what the kern pair does. A font can pass every
   check in §2, §4 and §5 and still lay out an illegible label. That is why the
   validator in the design doc runs on the laid-out label and not on the font.

Tracking needed to open the tightest pairs to 0.4 mm, in Arial Bold: `MC-4 R12`
needs **+0.219 mm**, `WWW` needs **+0.369 mm**.

## 7. The scripts, so every number can be re-derived

Four scripts produced everything above; they live in this session's scratchpad
rather than in the repo, because they read font files this repo does not ship and
would fail on any other machine. Their method is recorded here so the numbers can
be reproduced from the description:

- **`glyphs.py`** — contour extraction and the per-glyph measurements of §2 and
  §5. Uses `fontTools.pens.recordingPen.DecomposingRecordingPen` so composite
  glyphs are resolved to real contours, handles TrueType `qCurveTo` (including
  implied on-curve midpoints and the all-off-curve closed case) and CFF
  `curveTo`, flattens to a chord tolerance, and drops rings of ≤ 3 points.
  Crossing detection is *proper* crossings only — interiors meeting transversally
  — so a shared endpoint is not a crossing. Rasterisation is a vectorised
  non-zero winding count on a 0.02 mm grid.
- **`bake.py`** — the §3 sizes. `fontTools.subset` with `desubroutinize`,
  dropping `GSUB`/`GPOS`/`GDEF`/`kern`, and deleting `SVG `/`COLR`/`CPAL` from
  the `TTFont` before subsetting (Arial Bold ships an `SVG ` table, and merely
  listing it in `drop_tables` still requires `lxml`).
- **`verify.py`** — Q1–Q6 of §4, run on the rounded rings.
- **`routeE.py`** — the figure data for the published comparison, including the
  erosion cores drawn in §5.

### 7.1 The measurement that was wrong before it was published

The first run of §5 reported **DM Sans Bold `H` at a 0.01 mm stem** — a number
that would have been published as "this face is unprintable" and would have been
false.

The distance transform was being taken **from the drawn segments** rather than
from the ink mask. Those agree only when no two contours overlap. DM Sans draws
`H` as three overlapping rectangles (§2), and the seams where they overlap are
segments but are *not* boundaries of the ink — so every point near a seam
measured as near-zero.

The fix is one line: `ndimage.distance_transform_edt(ink, sampling=step)`. The
cross-check that it is right is that the six non-overlapping faces barely moved
(Arial Bold 0.58 → 0.60 mm), which is what a correct fix to an overlap-only bug
looks like.

The generalisable part: **§2's finding and §5's method were coupled and I did not
notice.** Discovering that a font overlaps its own contours should have
immediately invalidated every measurement that assumed it did not. It did not,
until the number came out absurd. A finding about the input is also a finding
about every tool that reads the input.

## 8. Fetch record

Every number in this file is measured locally. These sources are documentary —
they establish that a claim is a known property of the ecosystem, and none of
them supplies a number used above.

| Source | URL | Fetched | Used for |
|---|---|---|---|
| opentype.js README | https://github.com/opentypejs/opentype.js/blob/master/README.md | 2026-08-04 | the runtime-parser option §3 rules out |
| fontTools `removeOverlaps` | https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/ttLib/removeOverlaps.py | 2026-08-04 | that overlapping contours are a known, tooled-for condition — **located, not read in full** |
| JSCAD text | https://github.com/jscad-community/jscad-text, https://github.com/jscad/OpenJSCAD.org/issues/72 | 2026-08-04 | that a comparable JS CAD ships Hershey-only text — **search results, not read in full** |
| OpenSCAD `text()` stack | https://github.com/openscad/openscad/issues/512 | 2026-08-04 (via `text-emit-survey.md` §4) | the FreeType/HarfBuzz/fontconfig split §0 relies on |
| Each font's `name` table | — | 2026-08-04 | §1 licences, read from the font files themselves |

## 9. What could not be determined

- **Whether any of this survives a print.** Nothing was printed and no slicer was
  run. §5's connectivity result is about the geometry handed to a slicer; the
  slicer's own thin-wall handling could rescue or worsen it, and only a coupon
  settles that.
- **Whether Source Code Pro or DM Sans is the right shipping face.** SCP Bold wins
  on every measurement here — no overlap, every real label clear by ~1.9× — and
  loses on being a monospace, which is an aesthetic judgement this file cannot
  make.
- **What tracking or a minimum-advance rule should be.** §6 measures how much is
  needed for two labels. Whether to solve it by tracking, by face choice, by cap
  height, or by refusing the label is a design decision, not a measurement.
- **Whether the six DM Sans glyphs can be fixed by a build-time union.** Almost
  certainly yes — the shapes are three overlapping rectangles, the easy case —
  but no union was run. §2's claim is that the condition is *detectable*, not
  that it is repaired.
- **Every face outside these eight.** 37 glyphs of 8 faces is a sample. The claims
  in §2 and §5 are written as "of the faces measured here", and that is not
  modesty; it is the whole of what was checked.
