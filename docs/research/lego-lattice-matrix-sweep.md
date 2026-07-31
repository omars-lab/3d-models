<!--
  Measurement run 2026-07-31 by bikar `scripts/sweep-lattice-matrix.ts`
  (bikar PR #37), executed against bikar `origin/main` at c60faf2.
  Feeds: docs/lego-lab-design.md §5.3 (the Expected column -> Measured),
  and phase P1's line item "compatibility matrix filled by sweeps" (§10).
  Tool output preserved verbatim; the commentary is marked as commentary.
-->

# Lattice-compatibility matrix: the measured run

## What was run, and against what

`npx tsx scripts/sweep-lattice-matrix.ts` in bikar, at `origin/main` = `c60faf2`,
on 2026-07-31. The script sweeps five translation bases across a **single shared
scale interval** and reports what `packages/core/src/kernel3d/grid-gate.ts`
returns for each. Every family gets the same interval and the same step, because
the comparison of interest is *between* families and a per-family range would be
choosing the answer.

- Interval: **2 mm to 20 mm**, 3601 samples → **0.005 mm** step. That is an order
  of magnitude finer than the 0.05 mm snap threshold §5.3 sets, so a scale that
  snaps cannot fall between samples.
- Stud pitch: **8 mm** (`STUD_PITCH_MM`).
- Rotation: `gridFit` maximizes over θ internally; the reported θ\* is the one
  that achieves the reported fit.

**What this run does and does not measure.** It measures `gridFit` against a
lattice, not a pattern against `gridFit`. The bases are written down in the
script rather than compiled from a `.bkr`. That is the right unit for §5.3,
whose claims are claims about lattices — *"what decides the score is the aspect
ratio of the pattern's translation lattice"* — and the `hexagonal` and
`rectangular` rows use the exact shapes the evaluator's `repeatVectors` emits
for a `tile` block. A pattern that declares one of these bases inherits its row.
A pattern that declares something else is **not covered by this run**.

## Table 1 — the sweep (verbatim tool output)

```
Swept scale 2..20 mm over 3601 samples (0.005 mm step), stud pitch 8 mm.

| Lattice | Ratio | max fit | at scale (mm) | θ* (°) | residual (mm) | axis residuals (mm) | scales scoring ≥ 0.999 | repeat unit |
|---|---|---|---|---|---|---|---|---|
| `square` | 1.0000 | 1.0000 | 8.000 | 0.00 | 0.0000 | 0.000 / 0.000 | 4 | 1 × 1 |
| `hexagonal` | 1.7321 | 0.8037 | 17.570 | 60.00 | 0.7850 | 0.785 / 0.785 | 0 | withheld |
| `rhombic72` | 1.3764 | 0.7264 | 6.995 | 9.00 | 1.0943 | 1.094 / 1.094 | 0 | withheld |
| `rectangular32` | 1.5000 | 1.0000 | 16.000 | 0.00 | 0.0000 | 0.000 / 0.000 | 1 | 3 × 2 |
| `quasiperiodic` | — | **undefined** | — | — | — | — | 0 | withheld |
```

## Table 2 — the fixed-scale probe (verbatim tool output)

```
At scale = 8 mm and θ = 0 — the first basis vector is exactly one pitch:

| Lattice | fit at θ=0 | axis-1 residual (mm) | axis-2 residual (mm) |
|---|---|---|---|
| `square` | 1.0000 | 0.000 | 0.000 |
| `hexagonal` | 0.4824 | 0.000 | 4.000 |
| `rhombic72` | 0.6871 | 0.000 | 2.472 |
| `rectangular32` | 0.4142 | 0.000 | 4.000 |
| `quasiperiodic` | **undefined** | — | — |
```

## Why there are two tables

*(Commentary.)* Table 1 alone cannot test §5.3's hexagonal row. That row predicts
**"one axis snaps, the other plateaus"** — a statement about the two axes
*separately*. `gridFit` scores the **worst** axis, so its argmax is necessarily
wherever the two residuals balance against each other. At the winning scale the
hexagonal axis residuals are 0.785 and 0.785: identical, by construction, and
the asymmetry is invisible at exactly the point Table 1 looks.

Table 2 probes the scale that makes the first basis vector exactly one pitch
long and reads each axis. There the prediction holds precisely: **0.000 mm on
axis 1 — a clean snap — against 4.000 mm on axis 2, which is a half pitch and
therefore the worst offset that exists.** The vector is `(s/2, s√3/2)`; at
s = 8 the x-component is 4 mm, half of the pitch, and no rotation of the whole
basis can fix one axis without moving the other.

This is the same trap the doc's own §5.3 warns about in a different register:
a single worst-case scalar cannot express a per-axis claim. The measurement had
to be shaped to the claim, not the claim read off the nearest available number.

## Row-by-row, against what §5.3 predicted

| Row | §5.3 predicted | Measured | Verdict |
|---|---|---|---|
| `square` | **1.0** at the right scale | 1.0000 at 8.000 mm, θ = 0, repeat unit 1 × 1; **four** scales in range score ≥ 0.999 | **Confirmed** — and "the right scale" is plural: 2, 4, 8 and 16 mm all divide the pitch |
| `hexagonal` | one axis snaps, the other plateaus | invisible at the argmax (0.785 / 0.785); exact at scale 8, θ = 0 (**0.000 / 4.000**). Never scores ≥ 0.999 anywhere in range | **Confirmed, but only by Table 2** — see above |
| `rhombic72` | never reaches 1 at any scale | max **0.7264**, at 6.995 mm, θ = 9°. Zero scales ≥ 0.999 | **Confirmed over 2–20 mm only** — see the qualifier note below |
| `rectangular, rational p/q` | **1.0** reachable | `rectangular32` (p/q = 3/2) hits 1.0000 at 16.000 mm, θ = 0, repeat unit **3 × 2** | **Confirmed** — and the repeat unit comes out in studs, which is the number a user sizing a footprint needs |
| `quasiperiodic` | `gridFit` **undefined** | `undefined`, both tables | **Confirmed** — not 0, which would read as "measured and bad" |

## The qualifier that must survive into the doc

*(Commentary.)* §5.3's rhombic row says **"never reaches 1 at any scale"**. This
run searched **2 mm to 20 mm**. It did not search every scale, and cot 36° being
irrational is an argument for the claim, not this run's evidence for it. The
honest transcription into the doc is *max 0.7264 over the swept interval*, with
the unbounded version left standing on the irrationality argument that already
carries it — attributed to that argument, not to this table.

Stating it the other way would be a K2: an exhaustiveness claim over a space
that was not searched, attributed to a measurement that could not have searched
it.

## Two things the run establishes beyond the table

*(Commentary.)*

1. **`square` snaps at four scales, not one.** §5.3's "at the right scale"
   reads as though there is one. Every divisor of the pitch in range works
   (2, 4, 8, 16 mm), which matters for the Lab's sweep strip: the sweet spots
   are periodic, so a sweep window that happens to straddle none of them
   reports a flat curve on a lattice that registers perfectly.

2. **The repeat unit is withheld, not zero, when the basis is sheared.**
   `hexagonal` scores 0.8037 — a decent score — and still reports no repeat unit
   in studs. That is correct and worth stating in the doc: the *score* is about
   registration and the *repeat unit* is about axis alignment, and a sheared
   basis can do well at the first while having no answer to the second.

## Reproducing

```
cd ~/Workspace/git/bikar
npx tsx scripts/sweep-lattice-matrix.ts          # both tables, as markdown
npx tsx scripts/sweep-lattice-matrix.ts --json   # the same numbers, raw
```

The numbers are pinned by `packages/core/tests/kernel3d/lattice-matrix.test.ts`
(7 tests), which imports the script rather than re-deriving the bases — a test
that rebuilt them would pass while the published table and the script disagreed,
which is the drift it exists to catch.
