---
date: 2026-09-17
produced-by: this session — bikar `feat/coaster-shape-v2` (PR NaqshCoffee/bikar#208) dist: `shape_study.mjs` (convex hull of the drawn art, the seven-candidate fit, `evaluate().coaster3d.findings`), `bikar render … --check` at size 40 and 90, `stl_bbox.mjs` over the written STLs, `cell_radius.py` over the study's OpenSCAD top views
feeds: docs/coaster-design.md, docs/issues/coaster-outline-fit-pivot.md, docs/decisions-log.md D-066
---

# Coaster shape study (shape v2)

Verbatim measurements behind coaster shape v2: which outline the importer fits to
each construction's art and why, what the fitted coasters measure at both sizes, and
the numbers that retract the earlier "clipped" claim
([`../issues/coaster-outline-fit-pivot.md`](../issues/coaster-outline-fit-pivot.md)).
The P2.7 record ([`coaster-measurements.md`](coaster-measurements.md)) stays as the
round-disc baseline these supersede.

## 1. The art's convex hull, in GeoGebra units

The drawn pattern is evaluated at `size=90`, its segment endpoints recentred on the
bounding-box centre and divided by `unit`, and the convex hull taken (monotone
chain). Vertices as printed:

**GimTvN9hw4U — 23 vertices:** (-2.2500, 0.7217) (-2.2500, -1.0104) (-2.2500, -1.2990)
(-2.0000, -1.4434) (-0.5000, -2.3094) (-0.2500, -2.4537) (0.0000, -2.5981)
(0.2500, -2.4537) (2.0000, -1.4434) (2.2500, -1.2990) (2.2500, -1.0104)
(2.2500, -0.7217) (2.2500, 1.0104) (2.2500, 1.2990) (2.0000, 1.4434) (0.5000, 2.3094)
(0.2500, 2.4537) (-0.0000, 2.5981) (-0.2500, 2.4537) (-1.7500, 1.5877)
(-2.0000, 1.4434) (-2.2500, 1.2990) (-2.2500, 1.0104).
x-span 4.5000 · y-span 5.1962 · circumdiameter 5.1962.

**7apC5Q9QS-8 — 8 vertices:** (-2.0000, -2.0000) (-1.6384, -2.0000) (-0.3616, -2.0000)
(2.0000, -2.0000) (2.0000, 2.0000) (-0.3616, 2.0000) (-1.6384, 2.0000)
(-2.0000, 2.0000). x-span 4.0000 · y-span 4.0000 · circumdiameter 5.6569.

Neither hull is a regular polygon (23 vertices; 8 with collinear runs), which is why
the outline is *fitted* to a fixed candidate rather than *traced* from the hull.

## 2. The seven-candidate fit

For each candidate the importer measures `K` — the art's span in that outline's own
measure (diameter, side, across flats), rounded **up** to 4 decimals so the art never
exceeds the outline by float noise — and the area the outline encloses at that `K`.
The least area wins; an earlier row wins a tie.

**GimTvN9hw4U**

| candidate | measure | K (units) | area (units²) | |
|---|---|---|---|---|
| round | diameter | 5.1962 | 21.21 | |
| square | side | 5.1962 | 27.00 | |
| polygon 4 rotate 45 | across flats | 5.0191 | 25.19 | |
| polygon 6 rotate 0 | across flats | 5.1962 | 23.38 | |
| polygon 6 rotate 30 | across flats | 4.5000 | 17.54 | **least** |
| polygon 8 rotate 0 | across flats | 5.1962 | 22.37 | |
| polygon 8 rotate 22.5 | across flats | 5.1517 | 21.99 | |

The emitted golden carries `4.5001`: the importer's own measurement lands a float
hair above 4.5 and the ceil keeps it, so the CLI note reads
`coaster outline fitted to the art: polygon 6 rotate 30, 4.5001 GeoGebra units span
across flats (least area of 7 candidates)`.

**7apC5Q9QS-8**

| candidate | measure | K (units) | area (units²) | |
|---|---|---|---|---|
| round | diameter | 5.6569 | 25.13 | |
| square | side | 4.0000 | 16.00 | **least** |
| polygon 4 rotate 45 | across flats | 5.6569 | 32.00 | |
| polygon 6 rotate 0 | across flats | 5.4642 | 25.86 | |
| polygon 6 rotate 30 | across flats | 5.4642 | 25.86 | |
| polygon 8 rotate 0 | across flats | 5.6569 | 26.51 | |
| polygon 8 rotate 22.5 | across flats | 5.2263 | 22.63 | |

The `round` rows reproduce P2.7's `K` exactly (5.1962 and 5.6569 in
[`coaster-measurements.md`](coaster-measurements.md)). Under the P2.7 formula
`unit = ($size - 8) / K` the art's enclosing diameter at `size=90` is therefore
82 mm inside a 90 mm disc — the basis for withdrawing the "clipped" claim.

## 3. Render `--check` at both sizes (shape-v2 goldens)

Command shape: `bikar render patterns/Constructions/<c>-coaster.bkr --format stl
--check --param size=<size> -o out.stl`. Bounding boxes read back off the written
STL.

| Construction | outline | size | bbox x × y × z (mm) | triangles | STL | volume | mesh gate | linkage gate |
|---|---|---|---|---|---|---|---|---|
| GimTvN9hw4U | polygon 6 rotate 30 | 40 | 40.00 × 46.00 × 5.20 | 35508 | 1734 KiB | 6.6 cm³ | PASS | PASS |
| GimTvN9hw4U | polygon 6 rotate 30 | 90 | 90.00 × 104.00 × 5.20 | 177308 | 8658 KiB | 31.1 cm³ | PASS | PASS |
| 7apC5Q9QS-8 | square | 40 | 40.00 × 40.00 × 5.20 | 40800 | 1992 KiB | 7.8 cm³ | PASS | PASS |
| 7apC5Q9QS-8 | square | 90 | 90.00 × 90.00 × 5.20 | 204300 | 9976 KiB | 36.6 cm³ | PASS | PASS |

Mesh gate line at every render: `watertight=true euler=2 degenerate=0
minFeature=1.2mm (floor 0.8mm) — PASS` (the 1.2 mm is the emboss height); linkage
gate `bodies=1 pointContacts=0 errors=0 warn=0 — PASS`. `size` is the across-flats
measure, so the corner-up hexagon stands `size / cos 30°` tall (103.92 mm, sampled to
104.00 at the grid pitch); z is `base 4` + `emboss 1.2`.

## 4. Structural validator findings CV1–CV7 — identical at both sizes

From `evaluate(golden, { params: { size } }).coaster3d.findings`, both constructions:

- CV1 PASS — no deboss region to floor (not applicable: the relief is an emboss)
- CV2 PASS — declared strap width 2 mm (floor 0.8 mm)
- CV3 PASS — relief aspect height/width = 0.60 (ceiling 2)
- CV4 PASS — no bottom bevel
- CV5 PASS — no bottom chamfer; elephant-foot allowance not applicable
- CV6a PASS — fewer than two separate relief pockets; no neck to measure
- CV6b PASS — the printed solid is one connected body (1, expected 1)
- CV7 PASS — the inscribed art clears the outline by 1.00 mm at its closest strap end
  (measured 2.00 mm inside, limit 1.00): GimTvN9hw4U at (-18.00, 10.39) for size 40 and
  (-43.00, 19.31) for size 90; 7apC5Q9QS-8 at (-18.00, 9.00) and (-43.00, 21.50)

CV7's 2.00 mm is the `margin` knob at its default; the 1.00 mm limit is half the
2 mm strap width.

## 5. Cup contact on the study renders

Measured with `cell_radius.py` (largest empty circle between drawn straps, distance
transform at 6.4 px/mm) on the study's size-90 top views of the same two outlines:

| Construction | largest open cell radius | face within 5 mm of a strap |
|---|---|---|
| GimTvN9hw4U (corner-up hexagon) | 7.4 mm | 75 % |
| 7apC5Q9QS-8 (square) | 8.2 mm | 67 % |

Strap tops are one plane by construction (a single height field), so a cup base wider
than about 20 mm rests on a coplanar lattice, not on three points; printed flatness of
that plane is CAL-CST-05's territory, unmeasured.
