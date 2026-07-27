# Print Validation Gate — design doc (pre-implementation)

Status: **DRAFT v1 — no implementation yet.**
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

## 2. Failure taxonomy

| # | Failure | Layer signature | Severity |
|---|---------|-----------------|----------|
| F1 | Disconnected final part | mesh has >1 connected component | error |
| F2 | Island, never merges | region with no material below, no later merge | error (modeling bug) |
| F3 | Island, later merges | region with no material below that later joins the body | warn: supports required (report z, XY) |
| F4 | Overhang beyond threshold | region extends past dilated previous layer | warn, with worst angle |
| F5 | Sub-extrusion neck | layer region erodes to nothing at r < extrusion half-width | error (layer-resolved strut floor) |
| F6 | Long bridge | unsupported straight span between anchored ends | warn above span threshold |
| F7 | Bad bed contact | first-layer area / footprint below floor | warn (brim/raft/flatten advice) |

F1 is a 3D check on the final mesh (union-find over shared vertices post-weld — near-free).
F2–F7 come from the slice simulation.

## 3. Algorithm

1. **Slice**: intersect the welded mesh with planes z = k·h (layer height `h`, default
   0.2 mm). Each triangle-plane intersection yields segments; chain them into closed loops;
   classify outer boundaries vs holes by signed area → a **region set** per layer (polygons
   with holes). StarOrb is 5,040 tris × ~600 layers — trivial cost; even the 45k-tri
   subdivide-3 mesh stays well under a second.
2. **Support map**: for layer *i*, compute `unsupported_i = region_i − dilate(region_{i−1},
   h·tan θ_max)` with 2D boolean + offset ops (θ_max default 45°). Empty → fully printable;
   otherwise each connected patch of `unsupported_i` is an F4 candidate, and a patch that is
   an *entire* region (no overlap at all with layer i−1) is an island → F2/F3.
3. **Island lifetime**: track islands forward with region overlap between consecutive
   layers; an island that eventually overlaps the main body is F3 (record birth z and merge
   z); one that never does is F2. (The main body is the component containing the largest
   bed-contact region.)
4. **Neck scan**: per layer, erode regions by extrusion half-width (default 0.21 mm for a
   0.4 mm nozzle); any region that vanishes flags F5 with its XY centroid and z. This is the
   mesh-gate strut floor made layer-accurate.
5. **Bridges**: within `unsupported_i` patches that *touch* supported material at both ends,
   measure max span; over `bridge_max` (default 10 mm) → F6.
6. **Bed contact**: layer-0 region area and its share of the part's XY footprint → F7 below
   thresholds; the report suggests brim/raft or a flattened pole (orbs).

All 2D ops (boolean difference, dilate/erode offsets, overlap tracking) are exactly what
the composition work needs for holes/crops — one robust 2D clipping dependency (Clipper2
class; final pick in the composition doc) serves both.

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
- **The `/prototype` catalog is the calibration arm.** The gate's thresholds (45° overhang,
  10 mm bridge, 0.21 mm erode, bed-contact floor) are industry folklore until P1/P2 prints
  confirm or move them; the catalog's "Feeds" lines gain "print-gate thresholds" as a
  propagation target. The gate automates the *geometry* half of catalog questions (P2 Q5
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

Unlike the sibling docs, this one has no dedicated research report behind it. The default
thresholds (45° overhang, 10 mm bridge, 0.21 mm erode for a 0.4 mm nozzle, bed-contact
floor) are slicer-community defaults, deliberately uncited: §5 makes the `/prototype`
catalog their calibration authority, and P1/P2 print evidence — not literature — is what
moves them. Two borrowed pieces do have sources on file:

- The **2D boolean/offset engine** this gate shares with composition (scaled-integer
  coordinates, post-simplify, sliver culling) is sourced in
  [`research/code-cad-composition-survey.md`](research/code-cad-composition-survey.md) §5
  (Clipper2 and its WASM ports).
- The FDM **dimensional-tolerance and clearance context** (±0.1–0.2 mm printed accuracy)
  that motivates layer-resolved neck checks is sourced in
  [`research/tile-craft-field-survey.md`](research/tile-craft-field-survey.md) §7.
