# Construction equivalence — three oracles for "GeoGebra ≡ naqsh"

**Status:** O1, O2 and O3 shipped and measured on `GimTvN9hw4U` (2026-09-17);
O3's comparator is [qiyas PR #32](https://github.com/NaqshCoffee/qiyas/pull/32),
open.
Feeds from
[`docs/research/construction-equivalence-measurements.md`](research/construction-equivalence-measurements.md);
decided as D-062 in [`docs/decisions-log.md`](decisions-log.md); summarised in
[§6 of the umbrella design](geogebra-construction-import-design.md#6-equivalence-three-oracles-d-062).

## 1. Why three

When a GeoGebra construction is imported as a naqsh file, "it is the same" is
three different claims, and no single score discharges all three:

| Oracle | Claim | Reference side (never bikar) | naqsh side | Verdict |
|---|---|---|---|---|
| O1 geometry | every named object has the same geometry | the GeoGebra engine's own numbers, dumped through the Apps API | `bikar points` | one row per authored label |
| O2 drawing | the same ink is drawn in the final state | the reconstruct loop's hero export and the view it was exported with | `bikar render` SVG, placed on the export's grid | recall and precision of centrelines |
| O3 solid | the reference's solid region is solid in the flat extrusion | OpenSCAD's extrusion of the O1 polygons | `piece … extrude` STL | coverage of the reference footprint and the largest unfilled reference disc |

An aggregate never discharges a per-object claim, so O1 is per label and O3
must report where the worst deviation is, not only how much area agrees. Each
oracle has a documented blind spot (§5), which is why all three run before a
construction earns a catalog entry.

## 2. O1 — per-label geometry

The reference is what the real GeoGebra engine computes: the youtube oracle
loads the export's own `.ggb` into the GeoGebra web app under Playwright and
dumps every object's type, coordinates or equation, value and command string.
Cached `<coords>` in the XML are never trusted over that recompute. The naqsh
side is `bikar points`, which prints every named point, circle, line and
polygon in millimetres.

**The frame is divided out, never fitted.** The lowering puts A at the origin
and B one unit along +x (D-061), so the naqsh side divided by its `unit` param
is already in GeoGebra units; no translation, rotation or scale is estimated.
Then, label by label: points by `x, y`; circles by centre and radius from the
equation; lines by both naqsh endpoints lying on the reference line; segments
by length; polygons by vertex ring (cyclic, either orientation) or by area when
the dump carries no ring; free numbers against the naqsh `param` of that name.
A label present on one side only is its own FAIL row unless the lowering
accounts for it (a GeoGebra-generated polygon edge, a `Sequence` orbit that is
the naqsh pattern layer, or a conjugate the lowering introduced).

**Default:** tolerance `1e-6` GeoGebra units per coordinate. GeoGebra's own
equality precision is `STANDARD_PRECISION = 1E-8` and its loosest is
`MIN_PRECISION = 1E-5`, both constants in ([Kernel.java at c281ae2, lines 271–286](https://github.com/geogebra/geogebra/blob/c281ae22b34ea2bf7f281767751d033e2fbfedf3/source/shared/common/src/main/java/org/geogebra/common/kernel/Kernel.java#L271-L286),
fetched 2026-09-17, quoted in
[research §4](research/construction-equivalence-measurements.md#4-geogebras-own-numeric-precision-fetched-2026-09-17));
`1e-6` sits between the two, a hundred times looser than the engine's standard
so a legitimately different evaluation order cannot fail it, and ten times
tighter than the loosest bar the engine itself accepts. The largest residual
measured on the 23 compared labels is `9.9e-13`
([research §1](research/construction-equivalence-measurements.md#1-oracle-o1--per-label-geometry-run-2026-09-17)),
seven orders inside it.

**Validator:** O1 passes iff every compared label is within tolerance and no
label is missing or unaccounted for on either side; exit 1 otherwise.
- PASS: `GimTvN9hw4U`, hand-transcribed lowering — `23 compared, 0 failed,
  17 skipped/extra`, every skip and extra with its reason on its own row.
- FAIL: the same file with `rotate A by 120 around B` for `by -120` — C and
  every label derived from it leave tolerance on the first row that uses them;
  the hard case is a `pick` swap that lands on a mirror-image intersection,
  which O2 cannot see because the drawing is symmetric and only this row can.

Run: `make naqsh-coords ID=<video-id> NAQSH=<file.bkr>` in the youtube repo,
with `BIKAR_DIR` pointing at a bikar checkout whose CLI has `points`.

## 3. O2 — drawing

O1 cannot say which objects are drawn. O2 renders the naqsh file to SVG, places
it on the hero export's own pixel grid, and asks whether the same ink is there.

**Placement is computed, never fitted.** The export's `.ggb` carries the view
it was exported with (`<size>` and `<coordSystem xZero yZero scale>`). Export
width over view width gives the export's pixel factor; `scale` times that
factor is pixels per GeoGebra unit; divided by `unit` it is pixels per naqsh
millimetre; the SVG viewBox origin lands at a computed pixel. There is no
alignment step: both sides come from the same numbers, so an offset is a
defect, not camera shake. Two things are normalised on the SVG before
rasterising because they are not drawing differences: every stroke width is
set to the export's mean line width, and the root width/height are set to the
viewBox's exact size (bikar rounds them to whole millimetres and the rasteriser
scales to the rounded value — a 0.6 % skew that failed every centreline at one
unit size and none at another).

**What is compared.** One crop, the union of both ink boxes plus 2 %, so an
invented shape costs precision instead of being cropped away. Inside it:

- **Centreline coverage**, the load-bearing metric: each side's ink (darker
  than mid-grey, so GeoGebra's pale face tints are not ink) is thinned to a
  one-pixel skeleton; *recall* is the fraction of the export's skeleton within
  2 px of the naqsh skeleton, *precision* the reverse. A dropped element costs
  recall, an invented one precision, a wrong orbit or a moved point both.
- **Edge-SSIM**, the reconstruct loop's own score on the same crop, gated at
  the loop's own bar because O2 is a regression check against that loop. It
  is reported, not relied on: it stays above 0.82 for every by-design failure.

**Default:** recall ≥ 0.98 and precision ≥ 0.98, bet CAL-EQV-01. The
correct file scores 1.000 at four unit sizes and the smallest single-statement
drop (one rosette of seven) 0.858
([research §2](research/construction-equivalence-measurements.md#2-oracle-o2--drawing-run-2026-09-17));
the bet is settled by the corpus ladder, not a print — the second construction
(`7apC5Q9QS-8`, 144 statements with curves) is the first test of the margin,
and a false FAIL there is loud where a looser floor would fail silently.

**Default:** edge-SSIM ≥ 0.70, inherited from the reconstruct loop's own
`--ssim-min` as recorded in the
[import survey §2.2](research/geogebra-construction-import-survey.md); the
metric is scikit-image's
[`structural_similarity`](https://scikit-image.org/docs/stable/api/skimage.metrics.html)
over Canny edges.

**Validator:** `O2 PASS` iff recall ≥ 0.98, precision ≥ 0.98 and edge-SSIM ≥ 0.70;
exit 1 otherwise, naming which failed.
- PASS: the `GimTvN9hw4U` lowering at unit 15, 20, 40 and 45 — 1.000 / 1.000
  each; `unit` is a change of millimetre units and the placement divides it
  back out.
- FAIL: the same file with the central rosette's `edges from pet` removed —
  the least ink any single statement in the file controls — recall 0.858,
  precision 1.000. The outer ring dropped, a five-fold orbit for six, a wrong
  midpoint and a flipped rotation sign all score lower (research §2).

The first wiring — full canvas, aligned, edge-SSIM only — passed every one of
those failures; the pivot is recorded in the youtube repo's issue note naqsh-score-blank-canvas under
docs/issues (branch feat/ggb-coords).

Run: `make naqsh-score ID=<video-id> NAQSH=<file.bkr>` in the youtube repo
(needs `BIKAR_DIR`, `rsvg-convert`, and the export's `.ggb` beside its PNG).

## 4. O3 — solid

O2 cannot say what is solid. O3 compares two STLs of the flat extrusion: the
reference is OpenSCAD's `linear_extrude` of the polygons in the O1 dump
(`make reference` in the youtube repo — 42 polygons for `GimTvN9hw4U`, no
bikar code), the naqsh side is `bikar render --piece Coaster --format stl
--check` of the same file with `piece Coaster` / `extrude <pattern> depth`.
Both are in the same frame (millimetres, A at the origin, z from 0 to depth),
so, as with O2, nothing is aligned and a translated mesh is a FAIL by design.

**O3 is directional, and the measurement forced it.** bikar's `extrude`
solidifies a pattern's *bounded faces* — every face, including the star-shaped
gaps between the 42 petals — so the naqsh solid is a strict superset of the
reference: the reference's 3637 mm² footprint lies entirely inside the
extrusion's 5889 mm² (reference minus print: 0.00 mm²). The symmetric metrics
the plan named cannot gate on that: a faithful print scores footprint IoU
0.618, the symmetric-difference disc is 11.6 mm for the faithful print and for
the dropped ring alike, and the volume ratio is non-monotonic (a print that
dropped exactly the fill would score 1.0). The pivot is recorded in the qiyas
repo's issue note 2026-09-17-o3-interstitial-fill
([qiyas PR #32](https://github.com/NaqshCoffee/qiyas/pull/32)).
`qiyas mesh compare reference.stl print.stl` therefore gates on two
reference-relative numbers and reports the symmetric ones as context:

- **coverage** — the fraction of the reference's mid-height footprint the
  print covers, on a 0.2 mm grid;
- **local missing** — the largest inscribed disc of reference region the print
  leaves unfilled, with its centre: the per-region number, so a dropped petal
  is located even when coverage stays high.

Reported, never gated: IoU, 2D and 3D Hausdorff, volume ratio, extra fill in
mm², and the symmetric disc.

**Default:** coverage ≥ 0.99 and local missing ≤ 1.0 mm, bet CAL-EQV-02.
Measured 2026-09-17
([research §3.1](research/construction-equivalence-measurements.md#31-measured-by-qiyas-mesh-compare-2026-09-17)):
the faithful extrusion 1.000 / 0.00 mm, the dropped ring 0.143 / 10.00 mm, a
synthetic 0.5 mm translation 0.975 / 0.40 mm. The floor leaves 1 % for raster
and float noise and still catches the translation; the disc sits above the
0.2 mm grid and above the translation's 0.4 mm sliver. One construction plus
synthetics chose them, so they are a bet settled by the corpus ladder.

**What the flat stage can and cannot see** (measured 2026-09-17,
[research §3](research/construction-equivalence-measurements.md#3-oracle-o3--solid-preliminary-2026-09-17-the-comparator-is-p23b)):
dropping the central rosette produced an STL byte-identical to the correct
one (380 triangles, 17.7 cm³ both, sha256 equal), because those edges lie
inside the ring's faces and change no face union; dropping the ring produced
92 triangles and 2.1 cm³. Solid the extrusion adds beyond the reference — the
interstitial fill, or an invented region — is expected and reported as extra
fill, never a FAIL. So interior ink and invented ink are O2's claims; a missing
solid region is O3's. The finished coaster (rim, bevel, relief) has no GeoGebra
reference at all; its added features are validated by the mesh gate, the
coaster validators and the `CAL-CST-*` bets, never by O3.

**Validator:** `O3 PASS` iff coverage ≥ 0.99 and local missing ≤ 1.0 mm;
exit 1 otherwise, naming which gate fired. The fixtures were fixed before the
comparator existed and the thresholds chosen against them, not the reverse:
- PASS: the `GimTvN9hw4U` extrusion against the OpenSCAD reference — coverage
  1.000, local missing 0.00 mm.
- FAIL: the same file with the outer ring's nested block dropped — coverage
  0.143, local missing 10.00 mm, both gates. The hard case is the synthetic
  0.5 mm translation: coverage 0.975 fails while local missing 0.40 mm passes,
  so the floor, not the disc, is what catches a shifted mesh. The
  central-rosette drop is *not* a FAIL fixture — it is the identical-file
  limitation above, asserted as such and tested in qiyas.

Run: `make reference IN=<export.ggb> OUT=<dir>` in the youtube repo, then
`qiyas mesh compare <dir>/reference.stl <print.stl>` (JSON score,
`schema_version` 1, exit 1 on FAIL).

## 5. What each oracle cannot see

| Oracle | Blind to | Covered by |
|---|---|---|
| O1 | anything not named: a `Sequence` orbit, which objects are hidden, what the pattern layer draws | O2, O3 |
| O2 | ink outside the export's view (clipped on both sides alike); colour and fill; a label swap between two objects that draw the same ink | O1 |
| O3 (flat) | interior edges that change no bounded face; solid added beyond the reference (the interstitial fill, an invented region); everything the coaster adds after extrusion | O2 and its precision; the coaster validators and `CAL-CST-*` |

## 6. Where each runs

| Oracle | Repo | Entry point | Runs |
|---|---|---|---|
| O1 | youtube | `make naqsh-coords ID=… NAQSH=…` | per commit of a `.bkr` (fast, numeric) |
| O2 | youtube | `make naqsh-score ID=… NAQSH=…` | per construction |
| O3 | qiyas + youtube | `make reference IN=… OUT=…` then `qiyas mesh compare` (qiyas PR #32) | per coaster, before the catalog entry |

All three take the golden `patterns/Constructions/<id>.bkr` from bikar once
`bikar import geogebra` produces it (P2.2); until then they were run on a
hand-transcribed lowering of the same construction, which is what every number
above measures.
