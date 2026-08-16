<!--
  Research produced 2026-08-15 by Claude Fable 5, under the 3d-models
  design-doc rules, to discharge milestone Q4 of
  docs/qiyas-wheelfield-validation-design.md — "measure before gating".
  Sources: MEASUREMENT RUNS against two local checkouts —
  `~/Workspace/git/qiyas` at `17552cc` (branch `fix/orb-view-scoreable-split`,
  the PR #11 head) and `~/Workspace/git/bikar-lego-lab` at `cc66cd3` (branch
  `feat/orb-ribbon-views`, the PR #96 head). No web sources; no external
  documentation was consulted.
  Feeds: docs/qiyas-wheelfield-validation-design.md §7.
  WHAT WAS RUN: three scratch programs, described in §1 below and reproduced
  there in full. (a) a TypeScript program that compiled the four orb sources
  through bikar's own `compileToGeometry`, projected every symmetry-axis view
  in both representations, emitted ground truth in memory, and measured
  nearest-neighbour centroid spacing; (b) a Python program that fed each
  emitted ground truth back through qiyas's real
  `score_encoding_against_gt` with one element displaced, and recorded the
  composite; (c) a Python program that re-implements that function's matching
  arithmetic exactly, in order to read the per-pair statistics the `Scores`
  object does not carry. Fifteen view sets were rendered to the session
  scratchpad to produce the ground-truth files; nothing was written into either
  repo, no rasterizer was invoked, no encoder was run on a raster image, no
  mesh was generated, and no print was made.
  LIMITATION, stated here because every number below inherits it: the
  "encoding" in (b) and (c) is bikar's own ground truth relabelled, so a clean
  run scores exactly 1.0000 and a clean per-pair drift is exactly 0.0000 by
  construction. This isolates the displacement — it is the only variable — but
  it does NOT measure what qiyas's encoder actually recovers from a rendered
  PNG. The real encoder's drift floor is unmeasured and is the reason §3's
  decision defers one number rather than inventing it.
-->

# The scorer's acceptance radius on wheelfield views — measured

*Measurement date: 2026-08-15. Question: does
`CENTER_MATCH_MAX_DIAG_FRAC = 0.02` — the radius inside which
`qiyas orb-validate` will pair a detected shape to a ground-truth shape —
transfer from classic per-face orbs to the wheelfield family's cell and ribbon
views, and can any composite threshold be recorded on top of it?*

The constant is declared at `qiyas:src/qiyas/orb_validate.py:71` and justified
in place by classic-orb face spacing: faces sit "~0.05 diagonals apart", so a
0.02-diagonal radius is "far below inter-face spacing". That is a K10 transfer
claim about one family of pictures being made on behalf of another, and
[`docs/qiyas-wheelfield-validation-design.md`](../qiyas-wheelfield-validation-design.md)
§7 made checking it a precondition for recording any threshold.

**The short answer: it does not transfer, the design doc's own PASS margin was
never met even by the classic orb it was attributed to, and no composite
threshold is recordable for these views at any value.**

---

## 1. Method

All four shipped orb sources were compiled and projected at width 900 px
(diagonal 1272.79 px), the width `make orbs` uses:

- `bikar:patterns/Orbs/Weave-Orb.bkr` — the classic per-face orb, the family
  the 0.02 constant was set against. Cells only.
- `bikar:patterns/Orbs/Maclado-9.bkr` — wheelfield, cells only.
- `bikar:patterns/Orbs/Maclado-9-Weave.bkr` — wheelfield, both representations.
- `bikar:patterns/Orbs/Maclado-9-Overlap.bkr` — wheelfield, ribbons only (it
  has no cell decomposition; that refusal is the subject of PR #96).

Each was projected along all three of its symmetry axes, and ground truth was
emitted through `bikar:packages/core/src/render/gt-emitter.ts` — the same
emitter the CLI writes to disk — giving fifteen view/representation
combinations.

**(a) Spacing.** For every ground-truth shape, the distance to the nearest
other shape centroid, divided by the image diagonal, so the numbers are in the
same units as the constant. Reported as min / p05 / median / p95 and the count
below 0.02.

**(b) Composite.** Each ground truth was turned into a valid `Encoding` —
every shape relabelled `square` with the positional fields the scorer reads
(centre, area, bbox, polar, quadrant), symmetry copied across — and scored by
the real `score_encoding_against_gt`. Then one element at a time (a sample of
about 25 spread across the view) was displaced along +x by 0.9×, 2× and 5× the
acceptance radius, and re-scored. Because the encoding's symmetry is copied
from the ground truth, the symmetry term is 1.0 in every run and the whole
composite movement comes from the structural and geometric terms
(`W_STRUCTURAL = 0.4`, `W_GEOMETRIC = 0.35`, `W_SYMMETRY = 0.25`, at
`qiyas:src/qiyas/diff/scorer.py:94-96`).

**(c) Per-pair statistics.** `Scores` carries four numbers, and three of them
are means or ratios over the whole view; there is no way to ask it about the
worst single pair. So (c) re-implements the matching arithmetic exactly — same
unit square, same `max_dist = 0.02·√2`, same `linear_sum_assignment` over
plain centre distance, same `0.5·(dist/max_dist) + 0.5·relative-area-diff`
drift blend — and reports `max_drift`, the count of gt shapes whose assigned
partner fell outside the radius (`drop`), and `mispair`, the number of pairs
the assignment did *not* return to their own index.

In (c) the displacement is aimed at each element's **nearest neighbour**
rather than along +x, because that is the direction in which the radius can
swap the pair — the hazard the spacing statistic predicts. `mispair` is
readable only because reference and reconstruction share an index order here;
it is a property of the probe, not a statistic production could compute.

Each row of (b) and (c) aggregates its sample to the **friendliest** outcome a
defect could get away with: the lowest structural, the lowest geometric, the
highest `max_drift`.

---

## 2. Results

### 2.1 Nearest-neighbour centroid spacing, in image diagonals

The acceptance radius is 0.0200 in these units. The design doc's §7 PASS
condition asked for a minimum separation of at least 2.5× that, i.e. 0.0500.

| orb | axis | repr | n | min | p05 | median | p95 | under 0.02 |
|---|---|---|---|---|---|---|---|---|
| Weave-Orb | vertex-5 | cells | 40 | 0.0370 | 0.0370 | 0.0586 | 0.0612 | 0 (0%) |
| Weave-Orb | face-3 | cells | 40 | 0.0521 | 0.0521 | 0.0575 | 0.0737 | 0 (0%) |
| Weave-Orb | edge-2 | cells | 44 | 0.0483 | 0.0483 | 0.0512 | 0.0689 | 0 (0%) |
| Maclado-9 | vertex-3 | cells | 127 | 0.0141 | 0.0141 | 0.0197 | 0.0275 | 66 (52%) |
| Maclado-9 | face-5 | cells | 101 | 0.0191 | 0.0191 | 0.0236 | 0.0488 | 20 (20%) |
| Maclado-9 | edge-2 | cells | 130 | 0.0121 | 0.0121 | 0.0222 | 0.0277 | 44 (34%) |
| Maclado-9-Weave | vertex-3 | cells | 127 | 0.0141 | 0.0141 | 0.0197 | 0.0275 | 66 (52%) |
| Maclado-9-Weave | face-5 | cells | 101 | 0.0191 | 0.0191 | 0.0236 | 0.0488 | 20 (20%) |
| Maclado-9-Weave | edge-2 | cells | 130 | 0.0121 | 0.0121 | 0.0222 | 0.0277 | 44 (34%) |
| Maclado-9-Weave | vertex-3 | ribbons | 456 | 0.0006 | 0.0042 | 0.0089 | 0.0224 | 429 (94%) |
| Maclado-9-Weave | face-5 | ribbons | 370 | 0.0023 | 0.0024 | 0.0103 | 0.0250 | 335 (91%) |
| Maclado-9-Weave | edge-2 | ribbons | 447 | 0.0003 | 0.0032 | 0.0096 | 0.0194 | 425 (95%) |
| Maclado-9-Overlap | vertex-3 | ribbons | 516 | 0.0002 | 0.0043 | 0.0096 | 0.0240 | 474 (92%) |
| Maclado-9-Overlap | face-5 | ribbons | 435 | 0.0025 | 0.0037 | 0.0105 | 0.0253 | 375 (86%) |
| Maclado-9-Overlap | edge-2 | ribbons | 478 | 0.0011 | 0.0034 | 0.0098 | 0.0261 | 430 (90%) |

Three readings:

1. **The Maclado-9 and Maclado-9-Weave cell rows are identical to four
   decimals across all three axes.** They should be: the weave adds ribbons
   over the same field and does not move a cell. It is a free cross-check that
   the projection is deterministic and that `weave` is not perturbing the cell
   decomposition.
2. **Ribbon views put 86–95% of their bands closer to a neighbour than the
   radius**, with minima two orders of magnitude below it (0.0002–0.0025).
   Wheelfield *cells* are milder but still fail: 20–52% under the radius.
3. **The classic orb does not meet the doc's margin either.** Weave-Orb's
   three minima are 0.0370, 0.0521 and 0.0483 — that is 1.85×, 2.61× and 2.42×
   the radius, and §7 asserted 2.5× as "the same margin the classic-orb
   geometry had". Two of its three views are under it. The 0.05 figure came
   from qiyas's source comment about inter-**face** spacing on the sphere, and
   §7 ported it to nearest-neighbour **cell centroid** spacing in a projected
   view — a different quantity, on a picture where projection foreshortens the
   rim. That is a K10 transfer inside the doc that set the K10 test, and §7 has
   been corrected.

### 2.2 Composite under one displaced element (real scorer)

Clean is 1.0000 in every row by construction (see the header's limitation).

| view | n | 0.9r worst | 2r worst | 5r worst | 5r cost |
|---|---|---|---|---|---|
| WeaveOrb.vertex-5 | 40 | 0.9961 | 0.9879 | 0.9800 | 0.0200 |
| WeaveOrb.face-3 | 40 | 0.9961 | 0.9900 | 0.9900 | 0.0100 |
| WeaveOrb.edge-2 | 44 | 0.9964 | 0.9909 | 0.9909 | 0.0091 |
| Maclado9.vertex-3 | 127 | 0.9988 | 0.9969 | 0.9969 | 0.0031 |
| Maclado9.face-5 | 101 | 0.9984 | 0.9955 | 0.9942 | 0.0058 |
| Maclado9.edge-2 | 130 | 0.9988 | 0.9969 | 0.9969 | 0.0031 |
| Maclado9Weave.vertex-3 (ribbons) | 456 | 0.9997 | 0.9991 | 0.9991 | 0.0009 |
| Maclado9Weave.face-5 (ribbons) | 370 | 0.9996 | 0.9989 | 0.9989 | 0.0011 |
| Maclado9Weave.edge-2 (ribbons) | 447 | 0.9996 | 0.9991 | 0.9991 | 0.0009 |
| Maclado9Overlap.vertex-3 (ribbons) | 516 | 0.9997 | 0.9992 | 0.9992 | 0.0008 |
| Maclado9Overlap.face-5 (ribbons) | 435 | 0.9996 | 0.9991 | 0.9991 | 0.0009 |
| Maclado9Overlap.edge-2 (ribbons) | 478 | 0.9997 | 0.9992 | 0.9992 | 0.0008 |

**The composite dilutes as 1/n.** One element displaced five times the
acceptance radius — a defect nobody would argue about if they looked at the
picture — costs 0.0200 on a 40-cell classic view, 0.0031–0.0058 on a
101–130-cell wheelfield view, and **0.0008–0.0011 on a 370–516-band ribbon
view**. At the four decimal places `Scores` records, that last is the
difference between 0.9992 and 1.0000.

The 2r and 5r columns are equal on ten of the twelve rows: past the radius the
element is simply unmatched, and pushing it further changes nothing. The score
saturates at "one element missing" and is thereafter blind to *how* wrong the
picture is.

### 2.3 Per-pair statistics, displacement aimed at the nearest neighbour

`drop` and `mispair` are counts; `struct` and `geom` are the scorer's own two
non-symmetry terms; `maxdrift` is the worst single pair's drift.

| view | n | push | struct | geom | maxdrift | drop | mispair |
|---|---|---|---|---|---|---|---|
| WeaveOrb.vertex-5 | 40 | 0.5r | 1.0000 | 0.9938 | 0.2500 | 0 | 0 |
| | | 0.9r | 1.0000 | 0.9888 | 0.4500 | 0 | 0 |
| | | 2r | 0.9750 | 0.9939 | 0.2394 | 1 | 2 |
| WeaveOrb.face-3 | 40 | 0.5r | 1.0000 | 0.9938 | 0.2500 | 0 | 0 |
| | | 0.9r | 1.0000 | 0.9888 | 0.4500 | 0 | 0 |
| | | 2r | 0.9750 | **1.0000** | 0.0000 | 1 | 0 |
| WeaveOrb.edge-2 | 44 | 0.5r | 1.0000 | 0.9943 | 0.2500 | 0 | 0 |
| | | 0.9r | 1.0000 | 0.9898 | 0.4500 | 0 | 0 |
| | | 2r | 0.9773 | **1.0000** | 0.0000 | 1 | 0 |
| Maclado9.vertex-3 | 127 | 0.5r | 1.0000 | 0.9980 | 0.2500 | 0 | 0 |
| | | 0.9r | 1.0000 | 0.9898 | 0.8264 | 0 | **2** |
| | | 2r | 0.9921 | 0.9930 | 0.8803 | 1 | 2 |
| Maclado9.face-5 | 101 | 0.5r | 1.0000 | 0.9975 | 0.2500 | 0 | 0 |
| | | 0.9r | 1.0000 | 0.9955 | 0.4500 | 0 | 0 |
| | | 2r | 0.9901 | 0.9914 | 0.8649 | 1 | 2 |
| Maclado9.edge-2 | 130 | 0.5r | 1.0000 | 0.9981 | 0.2500 | 0 | 0 |
| | | 0.9r | 1.0000 | 0.9908 | 0.6927 | 0 | **2** |
| | | 2r | 0.9923 | 0.9930 | 0.9071 | 1 | 2 |
| Maclado9Weave.vertex-3 (ribbons) | 456 | 0.5r | 1.0000 | 0.9976 | 0.5881 | 0 | **2** |
| | | 0.9r | 1.0000 | 0.9972 | 0.7080 | 0 | 2 |
| | | 2r | 0.9978 | 0.9983 | 0.7534 | 1 | 2 |
| Maclado9Weave.face-5 (ribbons) | 370 | 0.5r | 1.0000 | 0.9971 | 0.6521 | 0 | **2** |
| | | 0.9r | 1.0000 | 0.9965 | 0.7402 | 0 | 2 |
| | | 2r | 0.9973 | 0.9979 | 0.7580 | 1 | 2 |
| Maclado9Weave.edge-2 (ribbons) | 447 | 0.5r | 1.0000 | 0.9976 | 0.6229 | 0 | **2** |
| | | 0.9r | 1.0000 | 0.9971 | 0.6733 | 0 | 2 |
| | | 2r | 0.9978 | 0.9983 | 0.7612 | 1 | 2 |
| Maclado9Overlap.vertex-3 (ribbons) | 516 | 0.5r | 1.0000 | 0.9979 | 0.5697 | 0 | **2** |
| | | 0.9r | 1.0000 | 0.9976 | 0.7408 | 0 | 2 |
| | | 2r | 0.9981 | 0.9988 | 0.6211 | 1 | 2 |
| Maclado9Overlap.face-5 (ribbons) | 435 | 0.5r | 1.0000 | 0.9976 | 0.5811 | 0 | **2** |
| | | 0.9r | 1.0000 | 0.9971 | 0.7641 | 0 | 2 |
| | | 2r | 0.9977 | 0.9987 | 0.5618 | 1 | 2 |
| Maclado9Overlap.edge-2 (ribbons) | 478 | 0.5r | 1.0000 | 0.9979 | 0.5762 | 0 | **2** |
| | | 0.9r | 1.0000 | 0.9977 | 0.6806 | 0 | 2 |
| | | 2r | 0.9979 | 0.9984 | 0.7824 | 1 | 2 |

Three results, each independent of the others.

**R1 — the mis-pairing threshold falls with field density, exactly as the
spacing statistic predicts.** The classic orb never swaps a pair inside the
radius: at 0.9r all three of its views still return every element to itself,
and the one swap that appears (vertex-5 at 2r) comes with the element already
dropped. Wheelfield cells swap at 0.9r on the two densest axes (vertex-3 and
edge-2, minima 0.0141 and 0.0121) and not on the sparsest (face-5, 0.0191).
**Every ribbon view swaps at 0.5r** — half the acceptance radius is enough to
make the assignment hand a band to its neighbour. The prediction and the
behaviour agree on all fifteen rows, which is the evidence that the spacing
statistic is measuring the right thing.

**R2 — the worst pair is n-independent where the mean is not.** On
Maclado9Overlap.vertex-3 at 0.9r the geometric mean has moved 0.0024 from
perfect while the worst pair's drift is 0.7408 — a factor of about 310. Across
the six ribbon views at 0.9r the mean moves 0.0023–0.0035 and `maxdrift` sits
at 0.67–0.76, a factor of 200–330. `maxdrift` does not shrink as bands are
added; the mean does, in direct proportion. Any statistic that is going to see
one broken band on a 516-band view has to be a per-pair extreme, not an
average.

**R3 — the geometric score is not monotone in the defect.** On
WeaveOrb.face-3 and WeaveOrb.edge-2, pushing an element to 2r raises the
geometric score to a **perfect 1.0000**, up from 0.9888 and 0.9898 at 0.9r.
The mechanism is plain once seen: past the radius the pair is discarded, and
the mean is then taken over the pairs that remain, all of which are exact. So
making the defect worse improves one of the three numbers the report prints.
The composite still falls, because the structural term catches the drop — but
`geometric` on its own, read from a report, points the wrong way. This is not
specific to wheelfields; it is a property of the scorer and it is visible on
the classic orb.

---

## 3. What this settles, and the one number it does not

§7 of the design doc set a two-armed validator and made recording any
wheelfield threshold conditional on passing it. Both arms fail:

- The spacing arm fails on every wheelfield view (§2.1) — and, on the
  corrected reading of the margin, on two of the three classic views the
  margin was attributed to.
- The perturbation arm — "displacing an element leaves the composite
  unchanged" — fails on the ribbon views (§2.2), where five times the radius
  costs 0.0008.

So:

1. **No composite threshold is recordable for wheelfield views, at any
   value.** 0.95 would be a rubber stamp; so would 0.99. Every defect measured
   here scores above 0.9942, most above 0.998. `--min-view-threshold` (qiyas
   D-f) keeps its report-only default, and the reason is now a measurement
   rather than a deferral.
2. **The gate that *is* recordable is a count, not a tolerance.** The number
   of ground-truth elements with no partner inside the radius (`drop`) is an
   integer, does not dilute with n, and moves from 0 to 1 the moment an
   element leaves the radius on any of the fifteen views. It requires no
   threshold to be invented.
3. **`max_drift` is the statistic that sees a defect inside the radius**, and
   qiyas does not expose it. Adding it to `Scores` alongside the three means
   is a prerequisite for gating on it — filed as Q4a.
4. **The acceptance radius should scale with the representation.** A single
   0.02 constant is 5–8× the ribbon field's own p05 spacing. What the right
   scaling is, this measurement does not settle.

**The number that is deliberately not recorded here is the bound on
`max_drift`.** Everything above compares ground truth against a perturbed copy
of itself, so the clean baseline is exactly 0.0000 — which is not the number a
real gate has to clear. qiyas's encoder recovering bands from a rendered PNG
will drift for reasons that have nothing to do with a defect, and that floor
has not been measured (the local `qiyas encode` CLI cannot run: cairo is
missing). Naming a bound now would be a bare number wearing a measurement's
clothes, which is the K4 failure this whole milestone exists to avoid. It is
measured in Q5, from the first CI run that encodes a real render, and recorded
then.

---

## Appendix — the three programs

Reproduced so the numbers can be re-derived. They were run from the session
scratchpad and are not checked in as executables; this appendix is the record.

### (a) spacing — TypeScript, run under `npx tsx` from the bikar worktree

```ts
const ROOT = '<bikar-worktree>/patterns/';
const WIDTH = 900;
const DIAG = Math.hypot(WIDTH, WIDTH);
const RADIUS = 0.02;

for (const bkr of ['Orbs/Maclado-9.bkr', 'Orbs/Maclado-9-Weave.bkr',
                   'Orbs/Maclado-9-Overlap.bkr', 'Orbs/Weave-Orb.bkr']) {
  const result = compileToGeometry(readFileSync(ROOT + bkr, 'utf-8'));
  const orb = result.orb3d!;
  for (const view of symmetryViewAxes(orb.base)) {
    const p = { radiusMm: orb.radiusMm, projection: orb.projection, view };
    // cells: projectOrbViewScene(result, p) -> emitOrbViewGroundTruth(...)
    //   (wrapped in try/catch: the overlap preset refuses, and the refusal is
    //    reported rather than swallowed)
    // ribbons, when result.orbWeave is set:
    //   projectOrbRibbonScene(result, p) -> emitRibbonViewGroundTruth(...)
    // then, per shape, min distance to any other shape's `center`, / DIAG
  }
}
```

### (b) composite — Python, run under `uv run python` from the qiyas checkout

```python
from qiyas.orb_validate import CENTER_MATCH_MAX_DIAG_FRAC, score_encoding_against_gt
from qiyas import arrangement_variants as _av  # noqa: F401  (side effect: model_rebuild)
from qiyas import shape_variants as _sv        # noqa: F401  (side effect: model_rebuild)
from qiyas.schema import Encoding

# Encoding built from gt: every shape type "square" with sides/side_length/
# rotation_deg, centre/area/bbox/polar/quadrant copied, primitives=None,
# symmetry and stats copied. One shape's centre pushed by
#   frac * CENTER_MATCH_MAX_DIAG_FRAC * hypot(width, height)
# along +x. Scored with the real score_encoding_against_gt.
```

Note for anyone re-running it: `Encoding.model_validate` raises "`Encoding` is
not fully defined" unless `qiyas.shape_variants` has been imported first — the
`model_rebuild` call is a side effect of that module, at
`qiyas:src/qiyas/shape_variants.py:587`, and `qiyas.contract` imports it for
that reason.

### (c) per-pair statistics — Python, same environment

```python
max_dist = 0.02 * math.sqrt(2.0)
cost = [[math.hypot(rx - ex, ry - ey) for (ex, ey, _) in rec] for (rx, ry, _) in ref]
rows, cols = linear_sum_assignment(cost)
for i, j in zip(rows, cols, strict=True):
    if i != j:
        mispaired += 1          # only meaningful because ref and rec share an order
    d = cost[i][j]
    if d > max_dist:
        dropped += 1
        continue
    area = abs(ref[i][2] - rec[j][2]) / max(ref[i][2], rec[j][2])
    drifts.append(0.5 * (d / max_dist) + 0.5 * area)
# structural = len(drifts) / max(len(ref), len(rec))
# geometric  = 1 - mean(drifts);  max_drift = max(drifts)
```

The displacement here is aimed at `ref[nearest(i)]` rather than +x.
