# Print Validation Gate — design doc (pre-implementation)

Status: **DRAFT v2 — no implementation yet.** Revised after an adversarial grounding
audit ([research/print-validation-grounding-audit.md](research/print-validation-grounding-audit.md);
counter-evidence and divergences in Appendix B). v1→v2: the overhang default moved from
a fixed 45° to the slicer-standard auto rule (half extrusion width) with the angle
convention stated, F5 split into error/warn tiers (Arachne prints far below one
extrusion width), the 10 mm bridge default is now credited to Bambu Studio and measured
along the best bridging direction, the "no slicer" bet gained an explicit divergence
justification plus a PrusaSlicer-CLI CI oracle, and the 2D-dependency framing was
corrected (manifold-3d already bundles Clipper2-backed 2D ops and `Manifold.slice`).
Scope: a geometry-level *printability* gate for every mesh bikar emits (orbs today;
`piece`/`tile` solids once composition lands): global connectivity, then a layer-by-layer
slice simulation that detects mid-air islands, excessive overhangs, sub-extrusion necks,
long bridges, and bad bed contact — before a slicer or a printer ever sees the STL.

Sibling docs (planned): `piece-composition-design.md` (piece/port/connect/assembly),
`tile-wall-design.md` (tiles, connectors, wall layouts). This gate is designed to ride the
same new 2D-boolean dependency those need, so the three land as one dependency decision.

---

## 1. Motivation

The existing mesh gate answers "is this a sound *mesh*": watertight, Euler characteristic,
min strut width ≥ 1.2 mm FDM floor, degenerate-triangle scan. It says nothing about whether
the part is printable **as a stack of layers**:

- A cropped tile whose cut removed the only bridge between two regions produces two bodies
  in one STL — a perfectly watertight mesh that falls apart in your hand.
- An orb lattice has struts whose lower ends begin in mid-air at some z; whether that's
  "supports required" or "will fail" is invisible until slicing.
- A sphere touches the bed at a point (prototype catalog P2, question 5) — first-layer
  contact area is a number we can compute, not a surprise on the plate.
- The 1.2 mm strut floor is checked in 3D, but a feature can be wide in 3D yet present a
  sub-extrusion-width cross-section *on some layer* (e.g., a strut crossing a layer plane
  near-tangentially).

None of this needs a slicer: slicing a triangle mesh into planar regions and comparing
consecutive layers is computational geometry we can own, with errors phrased in bikar's
vocabulary ("strut from void 12 starts unsupported at z=41.2 mm") instead of a slicer's.

**Why not just run a slicer?** (Divergence — full counter-evidence in Appendix B.1.)
PrusaSlicer slices headless (`prusa-slicer --export-gcode`,
[CLI wiki](https://github.com/prusa3d/PrusaSlicer/wiki/Command-Line-Interface)) and
Kiri:Moto ([grid.space/kiri](https://grid.space/kiri/)) proves full slicing runs in
browser workers; the geometry here is commodity (trimesh ships `section_multiplane`). We
still own the gate for three reasons: (a) the only CuraEngine-in-WASM port
([cura-wasm](https://github.com/Cloud-CNC/cura-wasm)) is archived since 2021, and
embedding Kiri:Moto means adopting a whole slicer app to extract warnings it doesn't
emit; (b) slicers *silently drop* features below `min_feature_size` — PrusaSlicer's own
tooltip says thin features "will not be printed" — so a dry-run reports nothing for
exactly the defects F2/F5 must catch; (c) our errors must speak bikar's vocabulary.
**Mitigation:** CI additionally runs a PrusaSlicer CLI dry-run on gallery presets as an
oracle, so gate false-negatives/positives surface as disagreement diffs.

## 2. Failure taxonomy

| # | Failure | Layer signature | Severity |
|---|---------|-----------------|----------|
| F1 | Disconnected final part | mesh has >1 connected component | error |
| F2 | Island, never merges | region with no material below, no later merge | error (modeling bug) |
| F3 | Island, later merges | region with no material below that later joins the body | warn: supports required (report z, XY) |
| F4 | Overhang beyond threshold | region extends past dilated previous layer | warn, with worst angle |
| F5 | Sub-min-feature / sub-extrusion neck | region erodes to nothing at min-feature floor / at extrusion half-width | error / warn (two tiers — see §3 step 4) |
| F6 | Long bridge | unsupported straight span between anchored ends | warn above span threshold |
| F7 | Bad bed contact | first-layer area / footprint below floor | warn (brim/raft/flatten advice) |

F1 is a 3D check on the final mesh (union-find over shared vertices post-weld — near-free).
Nuance: two components sharing a single welded vertex pass union-find but are not
structurally joined; the neck scan (F5) is the backstop — a point contact erodes to
nothing on its shared layer. F2–F7 come from the slice simulation.

## 3. Algorithm

1. **Slice**: intersect the welded mesh with planes z = k·h (layer height `h`, default
   0.2 mm). Each triangle-plane intersection yields segments; chain them into closed loops;
   classify outer boundaries vs holes by signed area → a **region set** per layer (polygons
   with holes). StarOrb is 5,040 tris × ~600 layers ≈ 3 M triangle–plane pairs — trivial
   cost (even *naive* slicing processes 200–250 M pairs/s; Minetto et al. 2017, CAD 92);
   the 45k-tri subdivide-3 mesh stays well under a second. The actual cost center to
   benchmark in the V1 spike is not slicing but the ~600 per-layer Clipper passes
   (dilate + diff + erode) in steps 2–4.
2. **Support map**: for layer *i*, compute `unsupported_i = region_i − dilate(region_{i−1},
   d)` with 2D boolean + offset ops. This is CuraEngine's own overhang formulation
   ([Generating-Areas](https://github.com/Ultimaker/CuraEngine/wiki/Generating-Areas)).
   The per-layer dilation `d` defaults to **auto = half the extrusion width** — the
   detection PrusaSlicer ships and recommends (`support_material_threshold = 0` →
   "Overhang defined by half the extrusion width",
   [SupportMaterial.cpp](https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/Support/SupportMaterial.cpp)) —
   which correctly makes the effective angle a function of layer height (≈48° at
   0.2 mm/0.45 mm, ≈66° at 0.1 mm). `--overhang <deg>` pins an explicit angle instead:
   θ is measured **from vertical** (Cura convention), `d = h·tan θ`; note PrusaSlicer
   measures from horizontal and uses `h/tan θ` — state the convention or port a bug.
   (Why not a fixed 45°: every flagship slicer defaults less conservative — Cura 50°
   from vertical, Bambu 30° from horizontal = tolerates 60° — see Appendix B.2.)
   Empty → fully printable; otherwise each connected patch of `unsupported_i` is an F4
   candidate, and a patch that is an *entire* region (no overlap at all with layer i−1)
   is an island → F2/F3.
3. **Island lifetime**: track islands forward with region overlap between consecutive
   layers; an island that eventually overlaps the main body is F3 (record birth z and merge
   z); one that never does is F2. (The main body is the component containing the largest
   bed-contact region.)
4. **Neck scan (two tiers)**: per layer, erode regions at two radii. Erode by
   `min_feature_floor` (default 0.05 mm ≈ half of Arachne's `min_feature_size`, 25% of
   nozzle — features below this are *silently not printed* by PrusaSlicer/Cura): vanish →
   **F5 error**. Erode by extrusion half-width (0.20–0.225 mm depending on the assumed
   line width — 0.40 mm Cura default vs 0.45 mm Prusa default; derived from `--nozzle`,
   the assumed width is stated in the report): vanish → **F5 warn** "single-bead
   feature — printable via Arachne variable-width beads but far below the 1.2 mm strut
   floor". Rationale: since PrusaSlicer 2.5 / Cura 5.0, Arachne prints features from
   0.1 mm up by thinning beads to `min_bead_width` (85% of nozzle), so
   sub-extrusion-width is degraded, not unprintable
   ([Arachne KB](https://help.prusa3d.com/article/arachne-perimeter-generator_352769));
   v1's single error tier would have rejected geometry shipping slicers print. Each hit
   reports its XY centroid and z. This is the mesh-gate strut floor made layer-accurate.
5. **Bridges**: within `unsupported_i` patches that *touch* supported material at both
   ends, measure the span along the *best* bridging direction (shortest anchored lines),
   not the patch's max chord — bridge feasibility is direction-dependent, per
   PrusaSlicer's [BridgeDetector](https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/BridgeDetector.hpp),
   which brute-force searches the bridging angle. Over `bridge_max` (default 10 mm —
   Bambu Studio's shipped `max_bridge_length` default; deliberately conservative vs
   community capability of 20–80 mm on tuned printers, acceptable because F6 is
   warn-only) → F6.
6. **Bed contact**: layer-0 region area and its share of the part's XY footprint → F7 below
   thresholds; the report suggests brim/raft or a flattened pole (orbs).

All 2D ops (boolean difference, dilate/erode offsets, overlap tracking) are exactly what
the composition work needs for holes/crops — one robust 2D clipping dependency (Clipper2
class; final pick in the composition doc) serves both. Note: **manifold-3d already
bundles Clipper2-backed 2D ops** (`CrossSection`: booleans, `offset`, simplify) plus
`Manifold.slice(height)` and `project()`
([docs](https://manifoldcad.org/docs/html/classmanifold_1_1_cross_section.html)). If
composition C1 adopts manifold-3d, this gate's 2D engine and even the slicing core may be
zero *new* dependencies; the hand-rolled slicer (Open Question 1) should be spiked
against `Manifold.slice` per layer before we commit to owning segment chaining.

## 4. Where it runs

- **CLI**: `bikar render foo.bkr --format stl --check print` — runs the mesh gate, then
  this gate; `--check` alone keeps meaning the mesh gate (back-compat). Exit non-zero on
  errors (F1/F2/F5), zero-with-report on warnings. `--layer-height`, `--overhang`,
  `--nozzle` flags override defaults; a future `print` DSL block can pin per-model defaults
  (e.g., a piece's print orientation — checks run in *print* orientation, which for a
  hemisphere-split half is face-down, not model-space).
- **Lab**: new gate-panel rows alongside the tri-count/mesh rows — "supports: none needed"
  / "supports required from z=41 mm" / "⚠ 0.3 mm neck at layer 118". The slice sim runs in
  the existing worker (post-solidify, same generation-guard rules); budget guard applies.
- **CI**: the orb snapshot suite asserts every committed preset is F1/F2/F5-clean and
  records the F3/F4 warning fingerprint, so a param change that suddenly makes a preset
  support-hungry shows up as a snapshot diff.

## 5. Relationship to qiyas and the prototype catalog

- **qiyas** stays the *pattern-fidelity* validator (2D encode/diff of orthographic views).
  The print gate is bikar-side computational geometry — no schema/contract change. (A
  possible later artifact: emit the worst-layer region set as SVG for eyeballing; explicitly
  out of scope here.)
- **The `/prototype` catalog is the calibration arm.** The gate's default thresholds are
  now sourced from shipped slicer defaults rather than folklore (auto-overhang =
  PrusaSlicer's half-width rule, 10 mm bridge = Bambu's `max_bridge_length`, 0.1 mm
  min-feature = Arachne's floor — Appendix A), but they remain *this printer's* numbers
  only after P1/P2 prints confirm or move them; the catalog's "Feeds" lines gain
  "print-gate thresholds" as a propagation target. The gate automates the *geometry* half of catalog questions (P2 Q5
  bed contact, P1 Q3 void resolution); scars, stringing, and strength remain physical.

## 6. What it deliberately does not catch

Slicer-level behavior (actual toolpaths, seam placement, support generation quality),
material behavior (warp, adhesion, PLA creep), and machine calibration. The gate's claim is
narrow: *this geometry, sliced ideally, has no unprintable structure*. The slicer preview
and the prototype catalog own the rest.

## 7. Phasing

- **V1 (with composition C1, shared dependency)**: F1 components; slicing core; F2/F3
  islands; F7 bed contact; CLI `--check print`; snapshot assertions.
- **V2**: F4 overhang margins, F5 neck scan, F6 bridges; Lab gate rows.
- **V3 (with composition C2/C3)**: per-piece print orientation, assembly-aware runs (each
  part checked in its own orientation), threshold updates from P1/P2 print evidence.

## 8. Open questions

1. Slice representation: exact segment chaining vs a small BSP per layer — decide during
   V1 spike with the degenerate cases (tangent triangles, vertices on the plane).
2. Island tracking granularity: per-region overlap is O(layers × regions²) worst case —
   fine for orbs; revisit if girih-field tiles explode region counts.
3. Should F3 (supports required) ever be an *error* for presets shipped in the gallery?
   Leaning yes-for-gallery, warn-for-Lab-custom.

## Appendix A — provenance

v1 called its thresholds "slicer-community defaults, deliberately uncited." The grounding
audit ([`research/print-validation-grounding-audit.md`](research/print-validation-grounding-audit.md))
showed they are citable from primary sources — and that two of them disagreed with
shipped slicer defaults (see Appendix B). Sources now on file:

- **CuraEngine support-area algorithm** (grounds §3 step 2 — the formula is theirs):
  [Generating-Areas wiki](https://github.com/Ultimaker/CuraEngine/wiki/Generating-Areas),
  [support.cpp](https://github.com/Ultimaker/CuraEngine/blob/main/src/support.cpp)
- **PrusaSlicer defaults, auto-overhang, Arachne floors** (grounds the auto rule and the
  F5 tiers):
  [PrintConfig.cpp](https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/PrintConfig.cpp),
  [SupportMaterial.cpp](https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/Support/SupportMaterial.cpp),
  [Arachne KB](https://help.prusa3d.com/article/arachne-perimeter-generator_352769),
  [BridgeDetector.hpp](https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/BridgeDetector.hpp)
- **Bambu Studio defaults** (grounds F6's 10 mm; contests a fixed 45°):
  [PrintConfig.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)
- **Cura defaults**:
  [fdmprinter.def.json](https://github.com/Ultimaker/Cura/blob/main/resources/definitions/fdmprinter.def.json)
- **Slicing performance** (grounds §3 step 1's "trivial cost"): Minetto et al., "An
  optimal algorithm for 3D triangle mesh slicing", Computer-Aided Design 92 (2017) —
  [PDF](https://www.inf.ufpr.br/murilo/public/CAD-slicing.pdf)
- **Orientation/bed-contact prior art** (grounds F7):
  [Tweaker-3](https://github.com/ChristophSchranz/Tweaker-3),
  [Tweaker paper](https://zenodo.org/records/5569145)
- **Overhang threshold is parameter-dependent** (contests any fixed angle):
  [Jiang et al. 2018, IJCIM 31(10)](https://www.tandfonline.com/doi/full/10.1080/0951192X.2018.1466398);
  [PADT self-supporting guidelines](https://www.padtinc.com/2017/07/12/towards-self-supporting-design-for-additive-manufacturing-part-1-standard-guidelines/)
- The **2D boolean/offset engine** this gate shares with composition (scaled-integer
  coordinates, post-simplify, sliver culling) is sourced in
  [`research/code-cad-composition-survey.md`](research/code-cad-composition-survey.md) §5
  (Clipper2 and its WASM ports) — whose pitfall (2), "inset by more than half the local
  feature width deletes geometry silently," is exactly the mechanism F5 exploits.
- The FDM **dimensional-tolerance context** that motivates layer-resolved neck checks is
  sourced in [`research/tile-craft-field-survey.md`](research/tile-craft-field-survey.md)
  §7: holes print 0.1–0.3 mm undersize and external dimensions ~0.1 mm oversize — the
  asymmetry matters for necks bounded by holes.

The `/prototype` catalog (§5) remains the calibration authority: literature sets the
defaults, print evidence moves them.

## Appendix B — counter-evidence and divergences

Each entry records the strongest counter-position found by the grounding audit
([`research/print-validation-grounding-audit.md`](research/print-validation-grounding-audit.md)),
with either our justification for diverging or the design change it forced.

Entries tagged `[CAL-…]` are **empirical** bets that no source can close — only a
measurement can. The id is the bet's entry in the registry
([`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md)), which
names the coupon that settles it; the ceremony is the `calibrate` skill (bikar
Tenet 30 — a physical constant is not earned until it records its provenance).

### B.1 "No slicer needed" — divergence justified, with a CI oracle

The counter-evidence: PrusaSlicer slices fully headless via CLI; Kiri:Moto is an
actively maintained pure-JS slicer running in browser workers, refuting any claim that
in-browser slicing is infeasible; and multiplane mesh slicing is a commodity primitive
(trimesh `section_multiplane`). We diverge anyway — cura-wasm (the only
CuraEngine-in-WASM port) has been archived since 2021; embedding Kiri:Moto means
adopting a whole slicer app that still doesn't emit the reports we need; and the
decisive asymmetry is that slicers **silently drop** sub-threshold features
(PrusaSlicer's `min_feature_size` tooltip: thin features "will not be printed" — no
warning), so a slicer dry-run cannot surface F5-class defects without G-code diffing.
The concession the counter-evidence won: CI runs a PrusaSlicer CLI dry-run on gallery
presets as an oracle against our gate (§1).

### B.2 The fixed 45° overhang default — the counter-evidence won [CAL-OVH-01 — coupon MC-4]

v1 defaulted θ_max to 45°. Every flagship slicer ships less conservative: PrusaSlicer's
recommended default is *auto* (overhang = half extrusion width per layer, making the
effective angle a function of layer height); Cura defaults to 50° from vertical; Bambu
Studio to 30° from horizontal (tolerating 60°). The literature (Jiang et al. 2018) adds
that the printable threshold moves with cooling, speed, and temperature — it is not a
fixed geometric constant. v2 adopts the auto rule as default with `--overhang <deg>` as
explicit override, and states the angle convention (from vertical, `d = h·tan θ`;
PrusaSlicer measures from horizontal with `h/tan θ` — at 45° the two coincide, which
hides convention bugs).

### B.3 F5 as a single error tier — the counter-evidence won

v1 made erode-by-half-width-vanishes an ERROR. Since PrusaSlicer 2.5 / Cura 5.0, the
Arachne engine is the default and prints features from ~0.1 mm (25% of nozzle) up by
thinning beads to `min_bead_width` (85% of nozzle) — so v1's floor was 4× the modern
printable floor and would have rejected geometry shipping slicers print. v2 splits F5:
vanish at the min-feature floor (~0.05 mm erode) = error ("silently not printed");
vanish at half-width = warn (single-bead, degraded, far below bikar's 1.2 mm strut
floor — which the mesh gate still enforces separately).

### B.4 Bridge span measurement — simplified formulation corrected [CAL-BRG-01 — the same bet as w2-connector B.3; one coupon (MC-3) closes both]

The 10 mm default survives (it is Bambu's shipped `max_bridge_length`, now credited),
but "max span between anchored ends" was naive: bridge feasibility is
direction-dependent, and PrusaSlicer's BridgeDetector brute-force searches the bridging
angle for the direction minimizing spanned length. v2 measures span along the best
bridging direction; community capability (20–80 mm on tuned printers) says the default
is conservative, acceptable because F6 is warn-only.
