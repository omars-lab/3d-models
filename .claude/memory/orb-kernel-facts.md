---
name: orb-kernel-facts
description: Load-bearing facts about bikar's orb kernel — no boolean union, ring-solidify without CSG, genus arithmetic, earcut for reflex fillers, aggregate checks cannot discharge per-part claims, meshGate is combinatorial
metadata:
  type: project
---

- bikar has **no boolean union**; bands are per-void inset-ring quad strips (decision `2026-07-23-orb-kernel3d-ring-solidify-no-csg`), and weaving is the only construction that resolves a crossing without one. That coupling is a kernel fact, not grammar: `overlap` without `weave` fails the manifold gate at every declared ratio (D-044, bikar #120).
- Pattern convention: regular n-gon circumradius 100, corners at 90°+k·360/n CCW; a star-tip void degenerates if the inset exceeds ~5 pattern units. Hole-wall winding `(vi_i_out, vi_j_out, vi_j_inn, vi_i_inn)`; the flipped order produced 1680 bad edges.
- A closed shell with H tunnels has genus H−1 (χ = 4−2H); a capped disc reads genus = holes.
- Fillers with reflex vertices must be earcut via a gnomonic chart, never centroid-fanned.
- `meshGate` is combinatorial (manifold + feature floor) and cannot see interpenetration; `linkageGate` asks bodies/clearance/linkage, and pairwise linking number is not a complete obstruction (Borromean) — see [[woven-orb-clearance]].
- The CLI mesh gate reads `capsWatertight ?? watertight` like the evaluator (bikar `8a01836`); a welded `base sphere` orb is the by-design case where the two flags diverge (D-047).
- Aggregate checks cannot discharge per-part claims: area sum + count passed while per-tile congruence failed (maclado M3); centre distance passed while zero rim points coincided (M2).
- Face-boundary edges make degree-6 nodes that cannot weave; weave needs every node degree 2 or 4.

**Why:** these decide what a new feature can and cannot be built on.

**How to apply:** before proposing a construction, check it against the no-union rule and the node-degree rule; write the by-design FAIL as the first test. Family 3 specifics: [[maclado-family-facts]].
