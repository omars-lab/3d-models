---
date: 2026-09-17
produced-by: bikar `feat/disc-coaster` (PR NaqshCoffee/bikar#207) — `bikar render … --coaster … --check` and a direct `evaluate()` of the two coaster goldens
feeds: docs/coaster-design.md
---

# Coaster render + validator measurements (P2.7)

> **Superseded 2026-09-17 (shape v2, D-066, bikar #208 / 3d-models #239).**
> The vendored meshes are no longer the round discs measured below: the presets
> now emit `outline polygon 6 $size rotate 30` (GimTvN9hw4U) and `outline square
> $size` (7apC5Q9QS-8) with `relief straps emboss 1.2` and a `margin` param. The
> current render table is in
> [`coaster-shape-study.md`](coaster-shape-study.md); this file is kept verbatim
> as the record of what P2.7 produced.

Verbatim measurements from rendering the two construction coasters at mini
(`--param size=40`) and standard (`--param size=90`), captured while landing the
`--coaster` importer flag. The design doc cites these numbers; this file is the
record that they were actually produced, not estimated.

## Enclosing-diameter constant K (measured off the lowered pattern)

`K` is the inscribed art's enclosing diameter in GeoGebra units — `2·maxRadial /
unitDefault`, `maxRadial` = farthest drawn point from the pattern's bbox centre.
The importer measures it at import and writes `param unit = ($size - 8) / K`.

| Construction | K (units) | pattern bbox @ unit=20 | maxRadial |
|---|---|---|---|
| GimTvN9hw4U | 5.1962 | 90.00 × 103.92 mm | 51.962 mm |
| 7apC5Q9QS-8 | 5.6569 | 80.00 × 80.00 mm | 56.569 mm |

Note: the planning estimates (~4.4 / ~5.4) were the rosette **width**; the true
enclosing circle over the recentred bbox is larger, which is why K is measured,
not guessed.

## Render `--check` results

Command shape:
`node packages/cli/dist/index.js render patterns/Constructions/<c>-coaster.bkr --piece Coaster --format stl --check --param size=<size> -o out.stl`

| Construction | Size | bbox (mm) | z-range | triangles | STL | volume | mesh gate | linkage gate |
|---|---|---|---|---|---|---|---|---|
| GimTvN9hw4U | standard (90) | 90.00 × 90.00 × 4.00 | 0..4 | 160860 | 7855 KiB | 23.8 cm³ | PASS | PASS |
| GimTvN9hw4U | mini (40) | 40.00 × 40.00 × 4.00 | 0..4 | 32240 | 1574 KiB | 4.5 cm³ | PASS | PASS |
| 7apC5Q9QS-8 | standard (90) | 90.00 × 90.00 × 4.00 | 0..4 | 160860 | 7855 KiB | 23.7 cm³ | PASS | PASS |
| 7apC5Q9QS-8 | mini (40) | 40.00 × 40.00 × 4.00 | 0..4 | 32240 | 1574 KiB | 4.6 cm³ | PASS | PASS |

Mesh gate line at every render: `watertight=true euler=2 degenerate=0
minFeature=0.8mm (floor 0.8mm) — PASS`. Linkage gate: `bodies=1 pointContacts=0
errors=0 warn=0 — PASS`. The disc diameter equals the `size` knob (`outline round
$size`); the 4 mm z-height is the `base`.

## Structural validator (CV1–CV6b) findings — identical at both sizes

Because `base`, deboss depth and `strap width` are absolute millimetres (only the
disc diameter and the inscribed-art scale track `size`), the z-dependent findings
are identical for mini and standard. Captured from `evaluate(golden, {params:{size}})`
`.coaster3d.findings` for both constructions, both sizes:

- CV1 PASS — thinnest floor under a deboss pocket is 3.20 mm (floor 0.6 mm)
- CV2 PASS — declared strap width 2 mm (floor 0.8 mm)
- CV3 PASS — relief aspect height/width = 0.40 (ceiling 2)
- CV4 PASS — no bottom bevel (limit 45°)
- CV5 PASS — no bottom chamfer; elephant-foot allowance not applicable (limit 0.4 mm)
- CV6a PASS — fewer than two separate relief pockets; no neck to measure (floor 0.8 mm)
- CV6b PASS — the printed solid is one connected body (1, expected 1)

No validator was weakened; both sizes pass as emitted, so no fall-back to a larger
mini was needed. A failing structural validator throws during evaluation, so a
clean render is itself the CV1–CV6b pass.
