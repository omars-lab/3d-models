# The coaster (product design)

The umbrella
([`geogebra-construction-import-design.md`](geogebra-construction-import-design.md)
§8) owns the pipeline from a GeoGebra construction to a printable coaster; this
doc owns the coaster itself — what it is, the two ways a construction becomes one,
its structural validators and the numbers that back them. The geometry engine is
bikar (`bikar/packages/core/src/kernel3d/coaster.ts`), which produces the mesh;
this repo consumes it and does not reimplement it.

Nothing here is printed. Every coaster is a bet-backed model until CS-1 runs the
calibration ladder, and no physical print is dispatched from this work (D-060).

## 1. What a coaster is

A coaster is a **height field over an outline** (D-064): a flat bottom, a top
surface `z = base + relief(x, y) + rim(r)`, and a side wall stitched between them.
Straps, face emboss/deboss and the edge chamfer or fillet are all height
contributions to the same field, and every structural validator is a query on
that one field. bikar has no boolean union, so the height field is the single
shape that is manifold by construction with one kernel — bevel and relief become
the same operation rather than two code paths that could disagree
(`bikar/packages/core/src/kernel3d/coaster.ts`). Cut-through is a separate
`trivet` mode, not a coaster.

The `outline` bounds the disc; the pattern is **inscribed** into it as relief. The
pattern is recentred on its bounding-box centre but **not** scaled to the outline
— so the outline must be large enough to enclose the inscribed art. §5 arranges that
by construction and CV7 (§7) checks it, because the sampler drops cells outside the
outline silently.

## 2. The two slices

A construction becomes a coaster through `bikar import geogebra`, which appends one
of two trailers. The flags are **mutually exclusive**: a construction imports as
one kind of part or the other, never both in one file.

- **Slice 1 — `--piece Name`** (P2.3): a flat extrude of the pattern's *own*
  outline — `piece Name` / `extrude <pattern> depth $depth`, on the existing piece
  machinery. `param unit` sets millimetres per GeoGebra unit; mini and standard are
  two values of one param, never two files (D-059).
- **Slice 2 — `--coaster Name`** (P2.7, reshaped by shape v2): a height-field slab
  that inscribes the pattern — `coaster Name` / `outline <fitted> $size` /
  `inscribe <pattern>` / `base` / `relief straps emboss` / `strap width`. This is
  the slice this doc is about; the importer emits the whole block
  (`bikar/packages/core/src/import/geogebra/emit.ts`), so the golden stays fully
  generated and re-renders from `--param`, never from a mesh transform (D-065), and
  it **fits the outline to the art** — a corner-up hexagon for GimTvN9hw4U, a square
  for 7apC5Q9QS-8 (D-066, §5).

The two generated coaster goldens — `GimTvN9hw4U-coaster.bkr` and
`7apC5Q9QS-8-coaster.bkr` — ship in bikar under `patterns/Constructions/` (added
by NaqshCoffee/bikar#207, reshaped by NaqshCoffee/bikar#208).

## 3. Relief modes

The coaster grammar carries three relief kinds, all height contributions on the
same field: **strap** relief (the pattern's strapwork raised or carved), **face**
relief (whole bounded faces raised or carved), and the `trivet` **cut-through**
mode (§7, CV6b). Each is either an `emboss` (raised above the base) or a `deboss`
(carved into it).

The **importer emits exactly one**: `relief straps emboss 1.2` — the pattern's
strapwork standing 1.2 mm proud of the slab, so the pattern reads as the object and
the slab as its ground (shape v2, D-066; P2.7 emitted `relief straps deboss 0.8`,
whose record is [`research/coaster-measurements.md`](research/coaster-measurements.md)).
Face relief, deboss and trivet are reachable by hand-editing the emitted `.bkr` but
the import path never writes them, so the worked examples below and the validator
evidence in [`research/coaster-shape-study.md`](research/coaster-shape-study.md)
cover the strap-emboss coaster only. This is a statement about the two constructions
imported here and the importer's one emitted mode, not a claim about every coaster
the grammar can express.

## 4. Rim, margin and edge profiles

`rim(r)` and the bottom `edge` (a chamfer or fillet) are further height
contributions, governed by CV4 and CV5 (§7). The **importer emits neither**: the
slab it writes has a square side wall meeting the plate at 90°, and no rim profile.
What it does control is the flat ground between the art and the outline — the
`margin` knob of §5, 2 mm by default, the smallest flat border Omar asked for
("minimize the flat borders around the edges"). A raised bezel around that margin is
the `rim` clause, hand-added per model, not emitted. So on every coaster this pipeline produces today CV4 and CV5 report "not
applicable" (§7) — they exist for hand-authored or future coasters that declare a
bottom edge, and they are stated here rather than dropped so the "not applicable"
is a recorded fact, not a silent skip.

## 5. Sizing: the outline fitted to the art, mini and standard from one file

The slab is **fitted** to the inscribed art (D-066). At import, bikar takes the
convex hull of the drawn pattern and measures it against **seven fixed outline
candidates** — `round`, `square`, `polygon 4 rotate 45` (a diamond), `polygon 6
rotate 0` (flat-up hexagon), `polygon 6 rotate 30` (corner-up), `polygon 8 rotate 0`
and `polygon 8 rotate 22.5` — computing for each the span `K` in that outline's own
measure (diameter, side, or across flats; rounded up to 4 decimals) and the area it
encloses. The least area wins, an earlier candidate winning a tie. The CLI prints the
verdict as a `note:` so the choice is visible, never silent. This is a claim about
those seven candidates, not about every outline the grammar can express; a pattern
whose hull fits none of them well still gets the least-bad of the seven.

`size` (the finished slab's across-flats measure, mm) stays the one print knob;
`margin` (the flat ground between the art and the outline, mm) is the second,
exposed because it is the border Omar wants minimal; `unit` (mm per GeoGebra unit)
is **derived** from both:

```
param size = 90 range 40..120
param margin = 2 range 1..10
param unit = ($size - 2 * $margin) / K
```

The parser inlines the literals when it reads the file, so a round-tripped `.bkr`
carries a plain number, not the expression. Because `K` is measured in the fitted
outline's own measure, the art's extreme points sit exactly `margin` inside the
outline's flats — and CV7 (§7) checks that they do.

One file is therefore both sizes: `--param size=90` is the standard, `--param
size=40` the mini. `base`, emboss height and `strap width` stay in absolute
millimetres, so only the outline and the art's scale change between them — never the
mesh, and never a wall driven below the printable floor (D-059).

Fitted outlines and measured spans (full record in
[`research/coaster-shape-study.md`](research/coaster-shape-study.md)):

| Construction | fitted outline | K (units) | least area vs round (units²) | mini (size=40) | standard (size=90) |
|---|---|---|---|---|---|
| GimTvN9hw4U | `polygon 6 $size rotate 30` | 4.5001 across flats | 17.54 vs 21.21 | 40.0 × 46.0 × 5.2 mm, 35508 tris, 6.6 cm³ | 90.0 × 104.0 × 5.2 mm, 177308 tris, 31.1 cm³ |
| 7apC5Q9QS-8 | `square $size` | 4 side | 16.00 vs 25.13 | 40.0 × 40.0 × 5.2 mm, 40800 tris, 7.8 cm³ | 90.0 × 90.0 × 5.2 mm, 204300 tris, 36.6 cm³ |

A corner-up hexagon is `size` across its flats and `size / cos 30°` corner to corner,
so the 90 mm GimTvN9hw4U coaster is 104 mm tall; `size` names the flats because that
is the measure the art is fitted in. The `size` default (90 mm), the `margin` default
(2 mm) and the emboss height (1.2 mm) are product/framing choices, not calibrated
numbers — see §9.

The earlier claim that the P2.7 round discs clipped their art is **withdrawn**: `K`
was measured at import (5.1962 and 5.6569 units, the enclosing diameters), and at
`size=90` the art spanned 82 mm inside the 90 mm disc. What the round disc wasted was
area, not art — 21.21 units² around a 17.54 hexagon — and that is what the fit
removes ([`issues/coaster-outline-fit-pivot.md`](issues/coaster-outline-fit-pivot.md)).

## 6. Print orientation

Fixed: **flat, top face up, no supports**. The height field has a flat bottom by
construction, so the whole footprint is the first layer and the relief prints as
unsupported top detail (D-064). `--check` runs the mesh gate on every render, and
the coaster's own structural validators run inside evaluation
([`print-validation-design.md`](print-validation-design.md)).

## 7. Structural validators

The eight structural validators CV1–CV7 are each a query on the height field
(`bikar/packages/core/src/kernel3d/coaster-validate.ts`); a failing one throws
during evaluation, so a coaster that renders has passed all eight. Each FAIL below
is the hard case — the dimensionally-valid geometry that is nonetheless
unprintable, or the pattern that is silently wrong — not a trivially malformed one.
The worked strap-emboss coaster (`base 4`, `relief straps emboss 1.2`, `strap width
2`, `margin 2`) satisfies every one, which is why it renders (§5).

The calibrated floors and ceilings these validators read are stated as defaults,
each discharged by its registered bet:

**Default:** strap / neck floor = 0.8 mm — CAL-CST-01, two 0.4 mm perimeter widths.
**Default:** mini-feature floor = 1.0 mm — CAL-CST-02, legibility at ~40 mm scale.
**Default:** deboss floor = 0.6 mm — CAL-CST-03, three 0.2 mm layers.
**Default:** relief-aspect ceiling = 2.0 — CAL-CST-04, height ÷ width before a rib delaminates.
**Default:** bottom-chamfer floor = 0.4 mm — CAL-CST-05, one perimeter width of first-layer squish.

All five are **provisional** bets, not settled numbers (§9).

### CV1 — floor under the deepest deboss

**Validator:** the solid slab left under the deepest deboss pocket is at least the
deboss floor (`CAL-CST-03` = 0.6 mm), so it does not print translucent and cup.
- PASS: the P2.7 coaster's `base 4` over a `0.8` deboss left a 3.20 mm floor,
  measured at both sizes. The worked emboss coaster has no deboss at all and reports
  "no deboss region to floor" — not applicable, carried as such (K1), not a pass on
  a floor it never measured.
- FAIL: a `deboss 3.8` into the same 4 mm base leaves a 0.2 mm floor — two layers,
  below the 0.6 mm floor. The disc is still watertight and dimensionally valid;
  only the field query catches it.

### CV2 — strap width

**Validator:** every declared strap is at least the strap floor (`CAL-CST-01` =
0.8 mm), so it prints as a solid rib rather than two touching walls.
- PASS: `strap width 2` — the worked coaster, 2.00 mm.
- FAIL: `strap width 0.6` — below the 0.8 mm floor, a strap with no solid core.

### CV3 — relief aspect

**Validator:** relief height ÷ strap width is at most the aspect ceiling
(`CAL-CST-04` = 2.0), so a raised rib does not delaminate along the layer lines.
- PASS: `1.2 / 2` = 0.60 — the worked emboss coaster (the P2.7 deboss was 0.40).
- FAIL: a `2.0` mm emboss on a `0.8` mm strap = 2.5, a rib two and a half times
  taller than it is wide.

### CV4 — bottom bevel angle

**Validator:** the bottom bevel is no steeper than 45° **measured from the plate
(horizontal)** — `rise/run`, so a bevel that rises as fast as it runs is exactly
45° and passes. The convention is load-bearing: bikar measures from horizontal, and
a rule stated from *vertical* would invert the test (the same porting hazard
`print-validation-design.md` records for slice height). This transfers to the
coaster because the underside prints as an overhang, and >45° from horizontal is
exactly the self-support limit an FDM underside can bridge without support.
- PASS: a bottom edge of `run 1, rise 1` — 45.0° exactly.
- FAIL: `run 1, rise 2` — 63.4° from horizontal. Worse, a bevel steeper than
  vertical is an **undercut the surface `z = f(x, y)` cannot express at all**: the
  height field has no second z for one `(x, y)`, so the geometry that would fail
  CV4 hardest is unrepresentable in the syntax, and the validator guards the
  boundary right up to it.

### CV5 — bottom chamfer vs elephant's foot

**Validator:** a declared bottom chamfer runs at least the elephant-foot allowance
(`CAL-CST-05` = 0.4 mm), so the first-layer squish insets rather than eating the
chamfer. A coaster with **no** chamfer is not failed — the wall meets the plate
square and the squish spreads outside the footprint — it is reported not-applicable
(carry the qualifier, K1).
- PASS: `chamfer run 0.4` — one perimeter width; or no chamfer at all (not applicable).
- FAIL: `chamfer run 0.2` — half a perimeter width, which the elephant foot closes.

### CV6a — neck between two relief pockets

**Validator:** the thinnest proud wall between two separate relief pockets clears
the strap/neck floor (`CAL-CST-01` = 0.8 mm). Walls between a pocket and the
outline are out of scope — the coaster's own side wall backs them full height — so
the scan is blocked at the outline (K10: the floor transfers only to free-standing
necks, not to walls with a full-height backing).
- PASS: two debossed faces separated by a 2 mm proud strap.
- FAIL: two debossed faces separated by a **0.6 mm** neck — below the 0.8 mm floor,
  a wall that prints as two touching perimeters with no core.

### CV6b — one connected solid

**Validator:** the printed solid above the floor is a single connected body, so
nothing prints as a loose piece.
- PASS: the worked coaster — `bodies = 1`, measured at both sizes.
- FAIL: a `trivet` cut-through that severs the frame into two rings, or a relief
  that detaches an island — 2 disconnected bodies, one of them loose.

A note on what CV6b does *not* discharge: it counts bodies over the whole field,
one aggregate number. It cannot stand in for CV6a's per-neck check — a coaster can
be one connected body while a single 0.6 mm neck inside it is too thin, so both
validators are needed and neither subsumes the other.

### CV7 — the inscribed art is enclosed

**Validator:** every strap end sits at least half a strap width inside the outline
and every face vertex sits inside it, measured as the exact signed inward distance
to the outline (`outlineInset` in `bikar/packages/core/src/kernel3d/coaster.ts`: the
nearest flat, edge or arc). The sampler drops cells beyond the outline without a
finding, so without CV7 a too-small outline prints a *cropped* pattern that passes
`--check` — the mesh is valid, the art is wrong. The worst point is named with its
location so the fix is a number, not a search. This transfers only to **convex**
outlines — round, square and the regular polygons the grammar has — because the
inset is computed against the nearest boundary feature; a concave outline would need
a different distance.
- PASS: the worked coasters — the closest strap end is 2.00 mm inside (the `margin`),
  limit 1.00 mm (half the 2 mm strap), so the art clears the outline by 1.00 mm; the
  message names the point, e.g. `(-43.00, 19.31)` for GimTvN9hw4U at size 90.
- FAIL: a strap whose **centreline** is inside but whose width spills — its end
  0.5 mm inside a 2 mm strap: `only 0.50 mm inside the outline (needs ≥ 1.00 mm
  inside)`. A strap 5 mm past the outline reports `5.00 mm outside`. A relief with no
  art passes and says so ("no art to enclose"), not silently.

## 8. Decisions

- **D-064** (logged): a coaster is a height field over an outline; cut-through is a
  trivet mode. The premise this doc builds on.
- **D-065** (P2.7): the `--coaster` importer emits the whole coaster block,
  and drives the file from a `size` knob with `unit` derived from it.
- **D-066** (shape v2): the outline is the least-area fit of seven fixed candidates,
  `margin` is a knob, the relief is an emboss, `rotate` orients a polygon outline,
  and CV7 checks enclosure.
- **D-067**: a coaster design UI is a Coaster Lab in bikar's lab, not a page in the
  hub; it starts once this knob set is stable.
- **D-068**: a border with its own pattern and per-region colour are coaster-level
  clauses composing patterns, sequenced after the interlock (#34) and the lab (#35);
  nothing of them ships yet. See [`decisions-log.md`](decisions-log.md).

## 9. Not yet

Honest gaps, so the next session inherits them rather than rediscovering them:

- **Every CAL-CST bet is provisional and unprinted.** CAL-CST-01…05 are bets from
  first principles (perimeter widths, layer counts), not measurements; CS-1 has not
  run the calibration ladder, and no physical coaster has been printed (owner-gated,
  D-060). The validators are only as right as the bets.
- **`size` default (90 mm), `margin` default (2 mm) and the 1.2 mm emboss are
  ungrounded.** They are product/framing choices with no bet and no source. If any
  ever binds a real decision it wants a `CAL-*` bet, not a bare number; until then
  they are named here as choices, not defaults. (The 1.2 mm emboss on a 2 mm strap
  is an aspect of 0.60 against CAL-CST-04's 2.0 ceiling, which is a check, not a
  source.)
- **The importer emits one relief mode.** Only `relief straps emboss` with a square
  wall and no rim ships from the import path; face relief, deboss, rim profiles,
  bottom edges and `trivet` are grammar features this pipeline does not exercise, so
  CV1, CV4 and CV5 have no worked coaster and report not-applicable on everything
  produced here.
- **Seven candidates, no traced outline.** A pattern whose hull fits none of the
  seven gets the least-bad of them; a traced (non-regular) outline was rejected
  because it has no single `K` measure and no regular edge for an interlock
  ([`issues/coaster-outline-fit-pivot.md`](issues/coaster-outline-fit-pivot.md)). A
  star or lobed coaster would need an `outline trace` mode with its own sizing rule.
- **Interlocking edges (#34)** — dovetail tabs on alternating polygon edges, full
  thickness, clearance a `CAL-*` bet; round outlines cannot tile. Not in the grammar.
- **Border band (#36) and colour regions (#37)** — the language today has neither:
  bikar's `border` declaration is a *tile edge profile*, not a pattern band, and
  `color` is a 2D render attribute that no STL carries. The direction (D-068) is a
  coaster-level `border <pattern> width <mm>` clause and named regions exported as
  separate bodies (`--format parts`) for a filament map in the 3MF; the X2D's AMS
  assignment happens in the slicer, not in bikar.
- **Coaster Lab (#35)** — after this knob set is stable (D-067).
