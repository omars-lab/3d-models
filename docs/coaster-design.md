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
— so the outline must be large enough to enclose the inscribed art, a condition
§5 resolves.

## 2. The two slices

A construction becomes a coaster through `bikar import geogebra`, which appends one
of two trailers. The flags are **mutually exclusive**: a construction imports as
one kind of part or the other, never both in one file.

- **Slice 1 — `--piece Name`** (P2.3): a flat extrude of the pattern's *own*
  outline — `piece Name` / `extrude <pattern> depth $depth`, on the existing piece
  machinery. `param unit` sets millimetres per GeoGebra unit; mini and standard are
  two values of one param, never two files (D-059).
- **Slice 2 — `--coaster Name`** (P2.7): a height-field disc that inscribes the
  pattern — `coaster Name` / `outline round $size` / `inscribe <pattern>` / `base`
  / `relief straps deboss` / `strap width`. This is the slice this doc is about;
  the importer emits the whole block (`bikar/packages/core/src/import/geogebra/emit.ts`),
  so the golden stays fully generated and re-renders from `--param`, never from a
  mesh transform (D-065).

The two generated coaster goldens — `GimTvN9hw4U-coaster.bkr` and
`7apC5Q9QS-8-coaster.bkr` — ship in bikar under `patterns/Constructions/` (added
by NaqshCoffee/bikar#207).

## 3. Relief modes

The coaster grammar carries three relief kinds, all height contributions on the
same field: **strap** relief (the pattern's strapwork raised or carved), **face**
relief (whole bounded faces raised or carved), and the `trivet` **cut-through**
mode (§7, CV6b). Each is either an `emboss` (raised above the base) or a `deboss`
(carved into it).

The **importer emits exactly one**: `relief straps deboss` — the pattern's
strapwork debossed into the top. Face relief, emboss and trivet are reachable by
hand-editing the emitted `.bkr` but the import path never writes them, so the
worked examples below and the validator evidence in
[`research/coaster-measurements.md`](research/coaster-measurements.md) cover the
strap-deboss coaster only. This is a statement about the two constructions
imported here and the importer's one emitted mode, not a claim about every coaster
the grammar can express.

## 4. Rim and edge profiles

`rim(r)` and the bottom `edge` (a chamfer or fillet) are further height
contributions, governed by CV4 and CV5 (§7). The **importer emits neither**: the
disc it writes has a square side wall meeting the plate at 90°, and no rim
profile. So on every coaster this pipeline produces today CV4 and CV5 report "not
applicable" (§7) — they exist for hand-authored or future coasters that declare a
bottom edge, and they are stated here rather than dropped so the "not applicable"
is a recorded fact, not a silent skip.

## 5. Sizing: mini and standard from one file

The disc auto-scales to the inscribed art. `size` (the finished disc diameter, mm)
is the one print knob; `unit` (mm per GeoGebra unit) is **derived** from it, so the
art clears the rim by a constant margin at every size. The importer writes
`param unit = ($size - 8) / K`, where `K` is the pattern's enclosing diameter in
GeoGebra units — measured off the lowered pattern at import — and `8` is twice the
4 mm rim margin. The parser inlines the `size` literal when it reads the file, so a
round-tripped `.bkr` carries a plain number, not the expression.

One file is therefore both sizes: `--param size=90` is the standard, `--param
size=40` the mini. Because `base`, deboss depth and `strap width` stay in absolute
millimetres, only the disc diameter and the art's scale change between them — never
the mesh, and never a wall driven below the printable floor (D-059).

Measured spans (both from `--check` renders, full record in
[`research/coaster-measurements.md`](research/coaster-measurements.md)):

| Construction | K (units) | mini (size=40) | standard (size=90) |
|---|---|---|---|
| GimTvN9hw4U | 5.1962 | 40.0 × 40.0 × 4.0 mm, 32240 tris, 4.5 cm³ | 90.0 × 90.0 × 4.0 mm, 160860 tris, 23.8 cm³ |
| 7apC5Q9QS-8 | 5.6569 | 40.0 × 40.0 × 4.0 mm, 32240 tris, 4.6 cm³ | 90.0 × 90.0 × 4.0 mm, 160860 tris, 23.7 cm³ |

The `size` default (90 mm) and the 4 mm rim margin are product/framing choices, not
calibrated numbers — see §9.

## 6. Print orientation

Fixed: **flat, top face up, no supports**. The height field has a flat bottom by
construction, so the whole footprint is the first layer and the relief prints as
unsupported top detail (D-064). `--check` runs the mesh gate on every render, and
the coaster's own structural validators run inside evaluation
([`print-validation-design.md`](print-validation-design.md)).

## 7. Structural validators

The seven structural validators CV1–CV6b are each a query on the height field
(`bikar/packages/core/src/kernel3d/coaster-validate.ts`); a failing one throws
during evaluation, so a coaster that renders has passed all seven. Each FAIL below
is the hard case — the dimensionally-valid geometry that is nonetheless
unprintable — not a trivially malformed one. The worked strap-deboss coaster
(`base 4`, `relief straps deboss 0.8`, `strap width 2`) satisfies every one, which
is why it renders (§5).

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
- PASS: `base 4` over a `0.8` deboss leaves a 3.20 mm floor — the worked coaster,
  measured 3.20 mm at both sizes.
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
- PASS: `0.8 / 2` = 0.40 — the worked coaster.
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

## 8. Decisions

- **D-064** (logged): a coaster is a height field over an outline; cut-through is a
  trivet mode. The premise this doc builds on.
- **D-065** (this work): the `--coaster` importer emits the whole coaster block,
  and drives the file from a `size` knob with `unit` derived from it. See
  [`decisions-log.md`](decisions-log.md).

## 9. Not yet

Honest gaps, so the next session inherits them rather than rediscovering them:

- **Every CAL-CST bet is provisional and unprinted.** CAL-CST-01…05 are bets from
  first principles (perimeter widths, layer counts), not measurements; CS-1 has not
  run the calibration ladder, and no physical coaster has been printed (owner-gated,
  D-060). The validators are only as right as the bets.
- **`size` default (90 mm) and rim margin (4 mm) are ungrounded.** They are
  product/framing choices with no bet and no source. If either ever binds a real
  decision it wants a `CAL-*` bet, not a bare number; until then they are named here
  as choices, not defaults.
- **The importer emits one relief mode.** Only `relief straps deboss` with a square
  wall and no rim ships from the import path; face relief, emboss, rim profiles,
  bottom edges and `trivet` are grammar features this pipeline does not exercise, so
  CV4 and CV5 have no worked coaster and report not-applicable on everything
  produced here.
- **Enclosure is not validated.** The derived-`unit` formula keeps the art inside
  the rim by construction, but no validator asserts the inscribed art actually fits
  the outline; a hand-edited `unit` or `size` could push art past the rim silently.
