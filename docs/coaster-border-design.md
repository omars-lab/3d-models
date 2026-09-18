# Coaster border band — a second pattern around the field

*Status: designed, not built (task #36, decision D-071). The direction is D-068 (a):
`border <pattern> width <mm>` as a clause of the `coaster` block, the field art inset
by the band. This is the fourth coaster form after the fitted slab of
[`coaster-design.md`](coaster-design.md), the interlocked slab of
[`coaster-interlock-design.md`](coaster-interlock-design.md) and the minimal lattice
of [`coaster-minimal-design.md`](coaster-minimal-design.md); it lives in the same
`coaster` kernel, adds no new solid, and is the first form with two named regions,
which is what colour (#37) needs.*

## 1. The ask

Omar (D-068 context, 2026-09-17): can the border carry a different pattern from the
field; does the language have a "border" component that composes with a pattern
component and takes its own colour. D-068 chose coaster-level composition and
sequenced it after the interlock (#34, D-069) and the lab (#35, D-067), both of which
have shipped. What is left to decide here is not *whether* but *how a second pattern
is laid into a band that follows an outline the importer chooses per construction*
— round, square, diamond, hexagon or octagon (`OUTLINE_CANDIDATES` in
[`coaster-design.md`](coaster-design.md) §5). Read as a careful colleague would:

- **A band, not a bezel.** The `rim` clause already raises a plain annulus; the band
  is the same annulus carrying its own art, relieved exactly as the field's art is.
- **The band follows the outline.** On a hexagon the border turns at six corners;
  on a disc it is a ring. A ring pattern clipped by a hexagon is not a border, it is
  a mistake with a name.
- **The field moves in.** The band replaces the outer part of what `margin` used to
  be; the field's art is inset by the band width plus `margin`, and CV7 measures
  enclosure against the band's inner edge, not the outline.
- **Colour is a region, not a geometry.** The kernel records which cells are band and
  which are field; the per-region export is #37 and is not designed here.

## 2. Options and the rubric

Rubric (0/1/2): **R1 follows the outline** (does the band turn with every outline the
importer can pick, with no clipped corner?); **R2 one kernel** (a second relief
channel through the existing height field, no new solid, no boolean); **R3
checkable** (CV1–CV10 keep a defined answer over both regions and the new failure
modes get a validator with a constructible FAIL); **R4 costs the grammar nothing**
(no new reserved word; the G2 snapshot is unchanged); **R5 costs the author one
cell** (the border pattern is written once, as a motif, in the same language as the
field, and the kernel repeats it).

| Option | R1 | R2 | R3 | R4 | R5 | Verdict |
|---|---|---|---|---|---|---|
| (a) **Plane-clipped** — the border pattern is drawn in the coaster's plane, scaled to the outline, and its relief masked to the annulus `0 < inset < W` | 0 | 2 | 2 | 2 | 1 | a ring motif is cut by every flat of a polygon and a square motif by every arc of a disc; the author must draw the band's shape as well as its art |
| **(b) Strip-mapped per run** — the border pattern is a motif cell; the kernel lays copies of it along each flat of a polygon outline (affine, corners plain) and around a round outline (polar, the ring closed by rounding the count) | 2 | 2 | 2 | 2 | 2 | **chosen** |
| (c) Corner motifs — (b) plus a `corner <pattern>` cell mitred into each vertex | 2 | 1 | 1 | 1 | 0 | a second cell, a mitre mapping and a second enclosure check for one visual gain; the plain corner of (b) is what a picture frame does |
| (d) A stock band style — `border chevron width 8`, art generated from the outline by the kernel | 2 | 2 | 2 | 0 | 2 | one reserved word per style and the art lives in the kernel, which is the composition D-068 rejected: the language composes patterns, it does not ship them |
| (e) 2D composition in the pattern layer — `nest`/`scale`/`repeat` the border into the field pattern and `inscribe` one pattern | 1 | 2 | 0 | 2 | 0 | CV7 cannot tell band from field, no region exists for #37, and the author writes the placement by hand for every outline the importer might pick (D-068's reasoning against a second `coaster`) |

(b) wins because the outline is the importer's choice, made per construction by
area fit, and the author of a border motif cannot know it. The one thing the kernel
knows and the pattern does not is the outline; so the kernel does the placement.
The cost (b) accepts is a **plain corner** on polygon outlines — a `W × W` patch of
ground at each vertex — and a **stretch of at most half a cell** spread around a
round outline so the ring closes. Both are stated in §3 and reported by CV11 (§6.2),
never silent.

## 3. The solid

Let `ι(p)` be the exact inset of `p` from the **nominal** outline (`outlineInset`,
the convex support-plane distance CV7 already reads; with `interlock` the nominal
outline is the one the tabs sit outside of and the slots bite into, D-069). Let `W`
be the band width, `w` the strap width and `t` the run of the top `edge` if there is
one (0 otherwise). The **band** is

```
B = { p : 0 < ι(p) < W }
```

and the **field** is `ι(p) ≥ W`. The band's art may not reach the band's edges: a
strap of width `w` centred on the band's outer line would hang `w/2` past the
outline, and one centred `t` from the edge would sit on the round-over's slope. So
the art is laid into the **strap-safe band**

```
ι ∈ [ w/2 + t ,  W − w/2 ]        height  h = W − w − t   (must be > 0, §4)
```

**The motif cell.** The border pattern's straps and bounded faces are recentred on
their bounding box exactly as `resolveCoasterArt` recentres the field's; the box is
the cell, `L` wide and `H` tall in pattern units. The cell's `+y` is **outward**:
its top edge lands on the outer line of the strap-safe band, its bottom edge on the
inner line. The scale is `s = h / H`, so one motif is `ℓ = s · L` mm long, and the
strap width stays `w` mm — a feature in mm is a feature in mm, which is why the band
width does not scale with `size` (§7).

**Polygon and square outlines — one run per flat.** A flat of length `F` meets its
neighbours at the interior angle `θ` (`120°` on a hexagon, `90°` on a square, `135°`
on an octagon). The band's inner corner sits `W · cot(θ/2)` along the flat from the
outer corner, so the straight run available to the motif is

```
U = F − 2 · W · cot(θ/2)          N = ⌊ U / ℓ ⌋   copies, centred, (U − N·ℓ)/2 of ground at each end
```

The mapping on flat `k` is affine: cell `x` runs along the flat's tangent, cell `y`
along its inward normal, offset to the strap-safe band. Straight stays straight;
the corners are ground.

**Round outlines — one polar run.** The ring must close, so the count is rounded,
not floored, and each copy is stretched tangentially to fit:

```
R_m = R − w/2 − t − h/2      (mid-radius of the strap-safe band)
C   = 2π · R_m               N = round( C / ℓ ),  N ≥ 1      cell length on the ring  C / N
```

Cell `x` becomes the angle `2π · (k + (x − x₀)/L) / N`, cell `y` the radius
`R − w/2 − t − (y₁ − y) · s`. A straight segment of the cell becomes an arc of a
spiral; it is emitted as chords, subdivided until each chord's sagitta is under a
quarter of the grid pitch, so the sampled field cannot tell the chord from the arc.
The stretch is `|C/N − ℓ| / ℓ ≤ 1/(2N)`; CV11 reports `N` and the stretch.

**Worked numbers** (chevron motif, `L = H`, so `ℓ = h`; `w = 2`, no top edge):

| coaster | outline | `W` | `h = ℓ` | run | `N` | ground per end / stretch |
|---|---|---|---|---|---|---|
| standard | hexagon 90 across flats (`F = 51.96`) | 8 | 6 | `U = 51.96 − 9.24 = 42.72` | 7 | 0.36 mm |
| mini | hexagon 40 across flats (`F = 23.09`) | 4 | 2 | `U = 23.09 − 4.62 = 18.47` | 9 | 0.24 mm |
| standard | round ⌀90 | 8 | 6 | `R_m = 41`, `C = 257.6` | 43 | −0.2 % |
| mini | round ⌀40 | 4 | 2 | `R_m = 18`, `C = 113.1` | 57 | −0.8 % |

**Height.** Nothing changes in the height formula of D-064: `top = base + relief +
rim − drop`. What changes is *which straps and faces* `reliefAppliesAt` consults at
`p`: the field's where `ι(p) ≥ W`, the placed band's where `0 < ι(p) < W`. One
`relief` statement (target, direction, height) and one `strap width` govern both;
a band that wanted its own relief height would be a second knob set, and §10 says
why it is not asked for. With `interlock`, the existing `reliefClip` (the nominal
ring) still holds every relief inside the nominal outline, so tabs stay plain and a
slot takes a bite out of the band exactly as it takes one out of the field today
(D-069's "stated edge to stop at").

**Regions.** The field gains a per-cell `band` mask beside `relief`/`deboss`/`cut`
— `band = inside ∧ 0 < ι < W` — so a cell is *ground*, *field* or *band* by two
bits, and #37 has something to export without re-deriving the geometry.

## 4. Grammar

One statement added to `CoasterStmt` in bikar `docs/grammar.md` §10.3:

```ebnf
CoasterStmt   = CoasterOutline | CoasterInscribe | CoasterBase | CoasterRelief
              | CoasterStrap   | CoasterRim      | CoasterEdge | CoasterTrivet
              | CoasterInterlock | CoasterBorder ;
CoasterBorder = "border" IDENT "width" ConstExpr NL ;
```

`border` already heads the tile edge-profile declaration and `width` is a reserved
word (`strap width` uses it), and the coaster body dispatches on token text, so the
keyword snapshot (G2) is unchanged. `border` is optional and may appear once. The
named pattern must be declared before the coaster, like `inscribe`'s, and must have
at least one segment; it may be the same pattern as the field's.

```bkr
coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  border GimTvN9hw4U_border width $border
  base 4
  relief straps emboss 1.2
  strap width 2
```

Refusals, each an evaluation error naming the clause (the `coaster:`-prefixed
mechanism `interlock` and `outline pattern` already use):

- `border` with `outline pattern` — the band is relief on ground and a minimal
  coaster has none. Lifting this is a classification change (band straps become
  solid, and must then join the field's straps), not a new mapping; §10.
- `border` with `rim` — both claim the annulus at the outline. A lip under a
  patterned band would raise the band's art by the lip height with no validator
  measuring the step; one clause owns the annulus.
- `border … width W` with `W − w − t ≤ 0` — the band is narrower than its own strap
  and round-over need; the message prints all three numbers.
- a run that holds no whole motif — §6.2 CV11's FAIL, an error like every CV FAIL.

`trivet` is allowed: it cuts the band's straps through like the field's, and CV6b
decides whether what is left is one body. `interlock` is allowed and composes as
§3 says.

## 5. Kernel change

In `bikar/packages/core/src/kernel3d/coaster.ts` and one new module beside it for
the placement:

1. **A second art channel.** `CoasterSpec.border?: { pattern: CoasterPattern,
   widthMm }` carries the *unplaced* motif cell; `buildCoaster` places it once
   (`placeBorder(outline, cell, widthMm, strapWidthMm, topRunMm) → CoasterPattern`
   in mm) before sampling, and the placed straps and faces are what the predicates
   read. Placement is a pure function of the outline and the cell, so it is unit
   tested on its own against the §3 table.
2. **`reliefAppliesAt` reads by region.** `ι(p) < W` selects the placed band art,
   otherwise the field art; the strap and face tests are unchanged. `classifyCell`
   stores the `band` bit.
3. **Extent unchanged.** The band lies inside the outline, so `sampleField`'s grid is
   the same; nothing outside the outline is touched.
4. **Mesh path unchanged.** Relief is relief; the assemblers see more relief cells
   and nothing new. `assembleInterlock` composes because the nominal ring already
   clips relief.

The only quantisation is the 0.4 mm sampling pitch every coaster already has, plus
the chord rule of §3 for arcs, chosen so it is invisible at that pitch.

## 6. Validators

CV1–CV10 keep running on the same field; the band's cells are relief cells and are
seen by every check that reads relief. What changes:

- **CV1, CV3, CV4, CV5, CV6a, CV6b**: unchanged and now cover the band too — a deboss
  band leaves the same floor question as a deboss field, a neck between a band
  pocket and a field pocket is a neck.
- **CV2** (strap width): unchanged; the band's straps are `w` wide by construction.
- **CV7** (art enclosed): **re-aimed** — §6.1.
- **CV8 / CV9** (interlock): unchanged; the slot margin CV8 measures is between the
  slot and the nearest relief, which may now be band relief. That is the intended
  reading: the band must not reach a slot wall either.
- **CV10** (minimal round-over): not applicable; `outline pattern` is refused.
- **CV11** is new — §6.2.

### 6.1 CV7 measures against the band's inner edge

**Validator:** with `border … width W`, every field strap ends at least `w/2` inside
`ι = W` (that is, `ι(end) − W ≥ w/2`) and every field face vertex has `ι ≥ W`; without
`border`, `W = 0` and the check is exactly today's. The band's own art is not
CV7's business — it is placed inside the strap-safe band by construction and CV11
checks the placement.
- PASS: the hex standard of §3 with `border 8` and `margin 2`: `unit` is derived so
  the field's outermost strap end sits at `ι = 10`, and `10 − 8 = 2 ≥ 1`.
- FAIL: the same file with `border 8` but `margin 0.5`: the outermost end sits at
  `ι = 8.5`, and `0.5 < 1` — the strap's outer half crosses into the band and would
  merge with the band's art with no finding from any other validator (CV2 measures
  each strap's width, not their union). Today's CV7 passes this file with room
  (`8.5 ≥ 1`), which is why the check has to move.

### 6.2 CV11 — the band holds whole motifs, and the placement is checked

An aggregate cannot discharge a per-part claim, so CV11 checks every run and every
placed strap, not a total.

**Validator:** (i) every run (each flat of a polygon or square outline; the one ring
of a round outline) holds at least one whole motif, `N ≥ 1`; (ii) every placed band
strap end has `w/2 + t ≤ ι ≤ W − w/2` and every placed face vertex `t ≤ ι ≤ W`,
within one grid pitch. The finding's message carries `N` per run and, on a round
outline, the closure stretch, so a stretched or sparse band is read, not guessed.
- PASS: the four rows of §3's table — the standard hex holds 7 chevrons per flat,
  the mini 9; the standard disc closes at 43 with 0.2 % stretch.
- FAIL: the standard's `border 8` kept on the mini (40 across flats, hexagon) with a
  motif three times as long as tall (a running key, `L = 3H`): `h = 6`, `ℓ = 18`,
  `U = 23.09 − 9.24 = 13.85 < 18`, so `N = 0` on every flat. Nothing else sees this
  — CV7 passes (the field is merely small), CV2 has no straps to measure in the
  band, and the mesh is a valid slab with a plain 8 mm border that the file *says*
  carries a pattern. This is the by-design failure of a band width in mm on a
  coaster that scales: §7.
- FAIL (ii) is not expressible in the grammar — a placement that leaves the band is
  a kernel defect — and is exercised the way CV4's steep bevel is, by building the
  spec directly with a cell whose placement is forced past the line.

## 7. Sizing: the band is in mm, the field gives way

`size` stays the one print knob. The band width is a second mm knob, like `strap`
and `round` on the minimal coaster, and `margin` keeps its meaning — clear ground
between the field's art and whatever bounds it, which is now the band:

```
param size   = 90 range 40..120     # mm, across flats of the outline
param border = 8  range 3..15       # mm, band width — CV11 refuses a band no motif fits
param margin = 2  range 1..10       # mm, ground between the field's art and the band
param unit   = ($size - 2 * ($border + $margin)) / K
```

`border = 8` is a choice, like `strap = 3` on the minimal coaster: on a 90 mm
standard it leaves a 70 mm field, which still reads as the construction, and holds
7 chevrons a flat. It binds no real decision and wants no bet: the band's straps are
seated straps on a slab, which is CAL-CST-01's case exactly (same load, same
adhesion, same shells — the K10 sentence the minimal doc could not write, written),
so no new floor is introduced. What *is* new is that the band **does not scale
with `size`**: an 8 mm band on a 40 mm mini leaves a 20 mm field and, with a long
motif, no motif at all (§6.2). So the mini sets its own: `--param size=40 --param
border=4`, the second knob the catalog entry carries. A fraction-of-size band was
considered and rejected — every other knob is in mm, and a strap in a 4 mm band is
the same 2 mm strap as in an 8 mm one.

## 8. Importer

`bikar import geogebra --coaster` gains `--border`, compatible with `--interlock`
and exclusive with `--minimal` (§4). Off, the emitted file is byte-identical to
today's goldens. On, the importer emits, after the construction's pattern and before
the coaster block, a **stock motif pattern** `<id>_border` — a chevron: three circles
at the cell's corners and apex and two segments between their centres, written in
the same statements a person would use — and the §4 block with the `border` clause
and the two knobs of §7. The stock motif is a starting point the author replaces by
editing one identifier; a border imported from a second construction (`--border-from
<ast.json>`) is the real prize and is §10.

The catalog carries the bordered variant as CS-5 beside CS-1…CS-4; the gallery
shows it from above, where a band reads as a band.

## 9. Decisions

- **D-071**: the border band is `border <pattern> width <mm>`, the motif cell
  strip-mapped by the kernel along each flat (affine, plain corners) or around a
  round outline (polar, count rounded to close), laid into the strap-safe band
  `[w/2 + t, W − w/2]`, relieved by the coaster's one `relief` statement; CV7 measures
  the field against the band's inner edge; CV11 checks every run holds a whole motif
  and every placed strap stays in the band; `rim` and `outline pattern` refused;
  the field records a `band` bit for #37. See
  [`decisions-log.md`](decisions-log.md).
- **D-068** is the direction this builds; **D-064…D-070** as in the three sibling
  docs, unchanged. D-I (a coaster is a height field) is again what makes the form
  cheap: a second art channel is a second set of straps for one predicate to read.

## 10. Not yet

- **Nothing has been printed**, and the band adds no new bet: its straps are
  CAL-CST-01's case (§7). CS-5's first question is whether a 2 mm chevron at 1.2 mm
  emboss reads as a border at arm's length or as noise.
- **Corners are plain.** A `W × W` patch of ground at each vertex of a polygon
  outline. A `corner <pattern>` cell (option (c)) is the extension if a print says
  the gap shows.
- **One relief for both regions.** A band embossed while the field is debossed, or
  a band at a different height, is a second relief statement scoped to a region.
  Not asked for; if it is, the region bit of §3 is where the scope attaches.
- **A minimal coaster has no band.** `outline pattern` is refused (§4).
  [`coaster-minimal-design.md`](coaster-minimal-design.md) §10 said this clause is
  what would join a disconnected lattice; it will, once band straps can be *solid*
  rather than relief — a classification change on the same placement, sequenced
  after CS-5 prints.
- **A border from a second construction.** `--border-from <ast.json>` lowers a
  second GeoGebra file as the motif. The placement does not care where the cell came
  from; the importer's header and mangling table would need a second source.
- **Colour regions (#37)** now have their region: the `band` bit. The per-body
  export (`--format parts`) and the filament map are #37's, unchanged in direction
  (D-068).
