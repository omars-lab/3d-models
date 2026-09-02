---
name: composition-and-wall-facts
description: Piece/tile/wall/assembly/mural facts that are decisions rather than code — clips never route through connect, clip exempt from the FDM floor, mural STL fails --check by design, seams by construction, crop stretch unshipped
metadata:
  type: project
---

- **Clip placement is layout-derived, never routed through C2 `connect`**: a clipped 2×2 grid is a closure cycle the tree solver would flag on every wall. Clipseats/keyholes still mint ports so C2 can reference them (decision `2026-07-29-w2-wall-connectors-mounts`).
- **The clip is exempt from the 1.2 mm FDM mesh floor, the tile is not**: `--piece StarClip --check` FAILs at 0.6 mm by design; the tile's rebate is a step, not a strut. `clipseat corners rebate|proud` keeps the variant word mandatory because Q1 is empirical and unresolved.
- A mural's fused STL fails `--check` by design (single-mesh path holds the 1.2 mm orb floor, each piece is entitled to the 0.7 mm brick floor); `make pattern-sets` gates per piece via `--format parts --check` and writes the composite ungated; `make bricks` skips `mural`. Seam continuity is by construction (cut lines injected into one planar-graph extraction), never tolerance; the 0.2 mm gap stays physical (D-013).
- Wall layout always scores all four half-pitch candidates (deliberate divergence from the design's sliver-only retry); only an exact 2·pitch boundary yields legal 50.0 halves. `crop stretch` was designed but never shipped (parser rejects with a pointer). W2's commit series is numbered by title, not number.
- Tile connectors are opt-in (`connect none` default); the connect graph must be a tree; fit ladder press −0.10 / snug +0.05 / sliding +0.15 / free +0.35 diametral, profiles compensate printed bores only.
- `tile` is a reserved keyword (cannot name a boundary `tile`); `unionPatternFaces` is the exact directed-edge union that makes star-over-tile relief work.
- LG-P1's seam coupon carries two bars at ±5.5 mm, not one: a single mid-line bar deletes a 2×2's only anchor candidate.

**Why:** each was a design-vs-implementation divergence resolved deliberately and recorded; re-litigating them is the K7 trap.

**How to apply:** cite the decision doc when a doc restates one of these. Coupons stay `planned` until printing resumes ([[owner-gated-and-on-hold]]).
