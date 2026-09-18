# Minimal coasters — the pattern is the solid

*Status: designed here, being built in bikar (task #38, branch `feat/coaster-minimal`,
PR to follow NaqshCoffee/bikar#209). Decision D-070. This is the third coaster form
after the fitted slab of [`coaster-design.md`](coaster-design.md) and the interlocked
slab of [`coaster-interlock-design.md`](coaster-interlock-design.md); it lives in the
same `coaster` kernel and adds no new solid.*

## 1. The ask

Omar (2026-09-17): "i also want a version of the coasters where the pattern is not on
a solid under it — where it's the pattern, vertically extruded with round outer edges
along the perimeter of pattern" — "minimal coasters".

Read literally, and that is the reading this doc builds (the assumption is stated so
it can be corrected on the first render):

- **No slab.** The printed solid is the pattern's strap network — every drawn
  segment thickened to the strap width — and nothing else. The cells of the pattern
  that a slab coaster fills with flat ground are **through-holes**.
- **Vertically extruded.** Flat bottom on the plate, straight side walls up to
  `base`, no relief on top: the strap *is* the full height.
- **Round outer edges along the perimeter of the pattern.** A round-over on the
  top edge of the silhouette, following every strap edge and the rim of every hole.
  In plan view the silhouette is already rounded by construction — a centreline
  dilated by a disc has circular convex corners and semicircular strap ends — so the
  round-over is the Z half of the pebble edge, and both readings of "round" are
  honoured by one clause.
- **Bottom stays square.** A round-over on the bottom edge would be a downward
  overhang steeper than 45° on the first layers, and the coaster prints flat with no
  supports (§6 of [`coaster-design.md`](coaster-design.md)). Refused, not silently
  skipped (§4).

## 2. Options and the rubric

Rubric (0/1/2): **R1 says what it is** (does the source read as "the outline is the
pattern", with no nominal outline nobody sees?); **R2 one kernel** (a change to
classification and the edge distance, not a new solid or a boolean); **R3 checkable**
(the CV1–CV9 queries still have a defined answer, and the new failure modes get a
validator); **R4 prints flat** (no overhang, no support); **R5 costs the grammar
nothing** (no new reserved word, G2 snapshot unchanged).

| Option | R1 | R2 | R3 | R4 | R5 | Verdict |
|---|---|---|---|---|---|---|
| **(a) `outline pattern`** — a fourth outline alternative; the outline *is* the inscribed pattern's strap silhouette | 2 | 2 | 2 | 2 | 2 | **chosen** |
| (b) `minimal` flag on a fitted outline — keep `outline polygon …` and add a clause that drops the ground | 0 | 2 | 1 | 2 | 2 | the outline becomes a lie: it is fitted, sized and checked (CV7) against a slab that is never printed; one name with two meanings, which is the defect CLAUDE.md says to delete rather than hide |
| (c) `piece … extrude <pattern>` with a 2D offset — the slice-1 path of the plan, dilating the centrelines in 2D and extruding | 1 | 0 | 0 | 2 | 2 | no height field, so no round-over without a second bevel kernel; none of CV1–CV9 runs; the mesh gate is the only check |
| (d) Boolean the slab away — subtract the open cells from a fitted slab | 1 | 0 | 1 | 2 | 2 | bikar has no boolean union or difference (D-064); a new solid for one product |

(a) wins on R1 and R2 together: the pattern names the outline, and the kernel change
is one function (§5). (b) is the tempting cheap fix and is exactly a fork — two
meanings of `outline`, with CV7 measuring an outline that does not exist.

## 3. The solid

Let `w` be the strap width and `d(p)` the distance from a point `p` to the nearest
strap centreline (`distToStraps`, the same query the strap relief already uses).
The signed inset of the silhouette is

```
s(p) = w/2 − d(p)        > 0 inside a strap, 0 on the silhouette, < 0 in a hole
```

and the coaster is

```
solid(p)  = s(p) > 0
bottom    = 0
top(p)    = base − drop(s(p))          drop = the top-edge chamfer or quarter-round of
                                       coaster-design.md §4, measured from s instead
                                       of the outline's inset
```

There is no relief term: `relief` is not a statement of this form (§4). The kernel's
height field (D-I) stays the single shape — `top` over a `solid` mask with holes,
walls stitched down every boundary loop, per-cell flat bottom — and the mesh is
watertight by the same construction that already makes `trivet` holes watertight
(§5). The strap ends are semicircles of radius `w/2` and the convex corners where
two straps meet are arcs of the same radius, because the solid is the Minkowski sum
of the centrelines with a disc; the reflex corners are sharp, which is what a
dilation produces and what a printed rib would have anyway.

## 4. Grammar

One alternative added to `CoasterOutline` in bikar `docs/grammar.md` §10.3:

```ebnf
CoasterOutline = "outline" ( "round" ConstExpr
                           | "square" ConstExpr
                           | "polygon" UINT ConstExpr [ "rotate" ConstExpr ]
                           | "pattern" ) NL ;
```

`pattern` is already a reserved word (it heads pattern declarations), and the
coaster body dispatches on token text, so nothing is added to the keyword snapshot
(G2). The required set becomes outline-dependent, and the parser keeps naming every
missing statement in one error:

| outline | required | forbidden |
|---|---|---|
| `round` / `square` / `polygon` | `inscribe`, `base`, `relief` | — |
| `pattern` | `inscribe`, `base`, `strap width` | `relief` |

```bkr
coaster Coaster
  outline pattern
  inscribe GimTvN9hw4U
  base 4
  strap width $strap
  edge fillet $round top
```

Refusals, each an evaluation error naming the clause (the evaluator passes any
`coaster:`-prefixed error through, the mechanism `interlock` already uses):

- `relief` — there is no slab to carve; the pattern is the solid. A `relief straps`
  would double-count the strap and a `relief faces` has no face to raise.
- `rim` — a rim is measured inward from an outline. There is none.
- `trivet` — everything that is not strap is already cut through; the trivet's cut
  mask would be redundant where it agrees and would sever straps where it does not.
- `interlock` — no straight edge to carry a tab or a slot.
- `edge … bottom` — the bottom chamfer offsets the outer loop with `insetPolygon`,
  which refuses holes, and a bottom round-over is a first-layer overhang (§1).

`edge chamfer|fillet <run> top` is the round-over and is the one optional clause.
`gridPitchMm` and `minFeatureMm` keep their meanings.

## 5. Kernel change

In `bikar/packages/core/src/kernel3d/coaster.ts`:

1. **One inset function.** `signedInset(p)` is `signedDistToRing(p, outlineRing)` for
   the three ring outlines and `w/2 − distToStraps(p)` for `pattern`. Classification
   (`solid = inset > 0`), the rim contribution, the top-edge drop and CV7 all read
   it, so the round-over follows every strap edge and every hole with no second
   formula. `outlineInset` (convex-only, CV7's instrument) is untouched for rings.
2. **Extent from the art.** `sampleField` sizes the grid from the strap bounding box
   plus `w/2` plus two pitches of margin — derived from the art, not a new default.
   `outlineRing` for `pattern` returns that bounding square so `field.solidRing` and
   any ring consumer stay defined; no solid is classified against it.
3. **No relief cells.** `relief`, `deboss` and `cut` masks are all false; `topZ` is
   `base − drop`. `declaredMinFeatureMm` is the strap width, never a silent zero,
   which is what `--check` reads as the mesh gate's feature floor.
4. **Mesh path unchanged.** `assembleFlatBased` emits a per-cell top, a vertical wall
   down every loop `boundaryLoops` finds — outer silhouette and every hole alike —
   and a per-cell flat bottom. `assembleChamfered` and `assembleInterlock` are never
   reached (§4 refusals). This is why the form costs no new mesh code: the height
   field with holes was already the `trivet` case.

The only quantisation is the 0.4 mm sampling pitch the slab coaster already has
(`COASTER_GRID_PITCH_MM`); a strap edge is a staircase at that pitch, as every slab
edge is today. The interlock's exact-wall machinery is not used, because nothing
here mates with anything.

## 6. Validators

CV1–CV9 keep running on the same field. What changes:

- **CV1** (deboss floor) and **CV3** (relief aspect): no deboss and no relief; both
  report not-applicable and say so, as CV1 does on the emboss coaster today.
- **CV2** (strap width) applies, with a **new floor** — §6.1.
- **CV4 / CV5** (bottom bevel): not applicable, a bottom edge is refused.
- **CV6a** (neck between pockets): the only pockets are the through-holes, and the
  narrowest solid between two of them is a strap, so CV6a floors at the strap width
  by construction. It still runs; it should never be the one that fires.
- **CV6b** (one connected solid) is **the by-design failure of this form**: a pattern
  whose straps do not all touch prints as loose pieces. On a slab coaster the ground
  joins everything; here nothing does. The test fixture is two concentric,
  non-touching rings under `outline pattern`, which must report `bodies = 2`.
- **CV7** (art enclosed): the outline follows the pattern, so there is nothing to
  enclose and nothing to crop; passes with the message "outline follows the pattern —
  nothing to enclose". The grid is sized from the art (§5), which is the fact CV7
  exists to check on a ring outline.
- **CV8 / CV9**: interlock-only; `interlock` is refused.
- **CV10** is new — §6.2.

### 6.1 CV2 under `outline pattern` — the strap is the whole wall

The floor is a **new bet, CAL-CST-07** (free-standing strap floor), registered in
bikar's `CAL_BETS` with the implementation and carrying a provisional `Calibrated`
record of 1.6 mm — four 0.4 mm perimeters, two shells a side so the rib has an inner
and an outer perimeter with no gap-fill between them — settled on coupon CS-4. This
doc states no D3 default for it until the generated registry
([`../.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md)) carries
the bet, exactly as [`coaster-interlock-design.md`](coaster-interlock-design.md) §10
did for CAL-CST-06; the 1.6 mm below is the bet's provisional value, not a source.

CAL-CST-01 (0.8 mm, two perimeters) **does not transfer** to this form. It was bet for
a strap that sits *on* a slab: its first layer is the slab's, its bottom is bonded to
solid, and the strap carries no load but its own. A free-standing strap is the whole
wall of the piece — its first layer is a 1.6 mm ribbon on the plate, not a disc; it
takes the bending load of a coaster picked up by one edge; and a two-perimeter rib
with nothing under it is two walls touching along their length with no top or bottom
skin to tie them. The load case, the adhesion case and the shell topology all differ,
which is the K10 sentence the transfer would need and cannot have. So the free-standing
floor is a new bet, not a reuse, and it is twice the seated one on the same
first-principles reasoning (perimeter counts), which is a bet and not a measurement.

**Validator:** with `outline pattern`, `strap width` is at least the free-standing
strap floor (`CAL-CST-07` = 1.6 mm); ring outlines keep CAL-CST-01.
- PASS: `strap width 3` — the shipped knob default, 3.00 mm, nearly two floors.
- FAIL: `strap width 1.2` — passes CAL-CST-01 with room (1.20 ≥ 0.80) and would print
  as a rib on a slab; free-standing it is three perimeters — one shell with no partner — below
  1.60. The finding names CAL-CST-07, not CAL-CST-01, so the reader learns which bet
  is binding.

### 6.2 CV10 — the round-over fits the strap

A quarter-round of run `r` on both edges of a strap of width `w` leaves a flat top of
`w − 2r`. At `r = w/2` the top is a full half-round; past it the two round-overs
cross and the strap's top becomes a ridge *below* `base` — the coaster is thinner than
its `base` says, on every strap, with no finding from any other validator (the mesh
is watertight and CV2 measures width, not height).

**Validator:** with `outline pattern` and a top `edge`, `2 · run ≤ strap width`.
Ring outlines and pattern coasters with no top edge pass trivially with a message
saying so.
- PASS: `strap width 3`, `edge fillet 1 top` — `2.0 ≤ 3.0`, a 1 mm flat top on every
  strap.
- FAIL: `strap width 2`, `edge fillet 1.2 top` — `2.4 > 2.0`: the round-overs cross
  0.2 mm before the flat, and the strap crests 0.2 mm below `base`. CV2 passes this
  (2.0 ≥ 1.6); only CV10 sees it. The boundary case `strap 2, fillet 1` passes at
  equality and is a full half-round, which is a legitimate pebble edge.

## 7. Sizing: what the minimal form costs and saves

There is no `margin`: nothing lies outside the art. `size` stays the one print knob,
now the across-flats span of the **silhouette** in the fitted outline's own measure
(the same `K` the plain file measured at import, §5 of
[`coaster-design.md`](coaster-design.md)), and `unit` is derived so that the strap's
*outer* edge lands on `size`:

```
param size  = 90 range 40..120     # mm, silhouette across flats
param strap = 3 range 1.6..5       # mm, the rib width — CAL-CST-07 is the floor
param round = 1 range 0..1.5       # mm, top round-over run — CV10 caps it at strap/2
param unit  = ($size - $strap) / K
```

The `strap` and `round` values are choices, like `size` and `margin` on the slab
coaster (§9 of [`coaster-design.md`](coaster-design.md)): `strap = 3` is the seated
strap width of D-066 (2 mm) widened for a rib that is the whole wall, and `round = 1`
leaves a 1 mm flat top on it. Neither binds a real decision yet; when one does it
wants a bet. The `round` range top is `1.5` because at `strap = 3` that is the CV10
limit; the range is a knob's UI hint, CV10 is the check.

What the form saves is material and print time — the slab is most of a coaster's
volume — and what it costs is stiffness and a floor: a minimal coaster is a lattice,
not a plate, and a glass sits on straps, not on ground. Whether a 40 mm mini at 4 mm
base is stiff enough to pick up is CS-4's first question (§10).

## 8. Importer

`bikar import geogebra --coaster` gains `--minimal`, exclusive with `--interlock`.
Off, the emitted file is byte-identical to today's goldens. On, the trailer is the
§4 block with the three knobs of §7 and no `margin`. The two shipped presets are the
plain goldens with that trailer swapped in, so the construction body is identical
between a coaster and its minimal twin — one pattern, three products.

The catalog carries the minimal variant as its own entry (CS-4) beside CS-1…CS-3;
the gallery shows it from above and at a low angle, because a lattice reads as a
lattice only when the holes show.

## 9. Decisions

- **D-070**: the minimal coaster is `outline pattern` — the outline *is* the
  inscribed pattern's strap silhouette — with `relief`, `rim`, `trivet`, `interlock`
  and bottom edges refused, one inset function feeding classification and the top
  round-over, CV10 for the round-over and a new free-standing strap bet CAL-CST-07
  for CV2. See [`decisions-log.md`](decisions-log.md).
- D-064…D-069 as in [`coaster-design.md`](coaster-design.md) §8; unchanged. D-I (a
  coaster is a height field) is what makes this form free: a solid mask with holes
  was already a height field the kernel could wall.

## 10. Not yet

- **Nothing has been printed.** CAL-CST-07 is a perimeter-count bet like
  CAL-CST-01…06; CS-4 settles it (owner-gated, D-060). Until then `strap = 3` is a
  choice that happens to clear the bet by a wide margin.
- **Stiffness has no validator.** A lattice coaster's bending stiffness depends on
  the pattern's topology, not only on strap width; two patterns with the same `strap`
  and `base` can differ by an order of magnitude. No CV measures it. If a printed
  mini flexes, the first knob is `base`, and a stiffness bet would want a load, which
  is the rig CAL-STR-01 already lacks.
- **Sliver holes.** Two straps that pass close without touching leave a void narrower
  than a perimeter, which the slicer fills or bridges unpredictably. The 0.4 mm
  sampling pitch quantises such voids away below one cell, and nothing reports it.
  A minimum-void check is the natural CV11 if a real pattern shows the artefact.
- **Reflex corners are sharp.** The dilation rounds convex corners and strap ends
  and leaves the inside corner where two straps meet sharp. A fillet there is a
  second offset and is not asked for.
- **The pattern must be connected.** CV6b refuses a pattern whose straps do not all
  touch; there is no clause to add a ring or a bar that joins them. D-068's border
  band (#36) is the clause that would, and it is sequenced after this.
- **Colour regions (#37)** are unchanged in direction; a minimal coaster is one body
  and has no region to colour separately until #36 gives it a second.
