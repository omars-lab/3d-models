# import-construction — run-time rubric

Read by [`SKILL.md`](SKILL.md) at the steps it names. Two halves: the **readability
rules** (would a person author this file?) and the **fidelity checks** (is it the
same construction?). The readability rules apply to every construction `.bkr`,
transpiled or hand-written; the fidelity checks are the three oracles' pass
conditions, grounded in
[`../../../docs/construction-equivalence.md`](../../../docs/construction-equivalence.md).

## Readability rules — the checklist

`bikar validate --style constructions` gates the mechanically-checkable subset (the
header order + sha256, the two root-frame lines, the scaffold split). The rest is a
read-through; each rule says what to look at.

1. **Names are the presenter's.** Only mandatory mangling is allowed (`'` → `_p`, a
   keyword collision → a trailing `_`). Look at: every identifier against the
   `# renamed:` header lines — a renamed name must appear there and nowhere else
   unexplained; a name that is not the GeoGebra label and not in the table is wrong.
2. **One statement per GeoGebra line, source order, with a provenance comment above
   it** (`# t=03:10  H = Intersect(m, n)`). Look at: each emitted statement has the
   comment carrying the original GeoGebra line and its `# t=` tag; the order matches
   the construction.
3. **Section banners follow the `# t=` tags.** Look at: banner comments group the
   statements by the tagged steps, not by an invented structure.
4. **Root frame first, always the same three lines.** Look at: the file opens with
   the unit circle, its division, and the A/B/D aliases — identical every time
   (`circle unit …` · `divide unit into 4` · `point A = unit.mpt` etc.). This is the
   part `--style constructions` also checks.
5. **All geometry in `blueprint <id>_scaffold`; the pattern layer only draws.** Look
   at: construction lines/points/circles live in the scaffold blueprint; the pattern
   layer contains only `edges from …` in export order — no scaffold geometry leaks
   into what prints.
6. **One generator per ring; nested orbits nest blocks; partial orbits use `for`;
   never unrolled.** Look at: a full N-fold ring is one `rotate N around` block (or a
   nested `rotate … / mirror around …`), not N copied statements; only a partial
   orbit uses `for`.
7. **Numbers appear only as `param`s or as angles in degrees.** Look at: no bare
   millimetre literal in a statement body; free numbers are `param … range …`,
   rotations are integer/decimal **degrees**, CCW.
8. **The pattern's `edges from` order is the `@export` order** (else the `@hide
   except` survivors). Look at: the draw order in the pattern layer matches the
   construction's export whitelist, so the ink layering is the presenter's.

### Header convention (rule 2/4 in the header)

The file opens with this block; `--style constructions` gates its order and the
64-hex sha256:

```
# naqsh construction — <id>
# title:  <video title>
# url:    https://www.youtube.com/watch?v=<id>
# steps:  <N> statements, <M> tagged steps
# source: reconstructions/<id>/construction.ggb-commands sha256:<64 hex>
# renamed: <old> -> <new> (<reason>)   # one line per mangled name, or omitted
param unit = 20 range 15..45          # mm per GeoGebra unit (slice-1 piece)
```

For a `--coaster` file the print knob is `param size` (mm) with `unit` derived from
it, so the disc auto-scales to the inscribed art (render mini/standard via
`--param size=`).

## Fidelity checks — the three oracles

An aggregate never discharges a per-object claim, so O1 is **per label** and O3
reports **where** the worst deviation is, not only how much agrees. All three are
run before a construction earns a catalog entry. Full spec, blind spots and
provenance: [`../../../docs/construction-equivalence.md`](../../../docs/construction-equivalence.md).

### O1 — per-label geometry (`make naqsh-coords`)

GeoGebra's own numbers (Apps-API dump) vs `bikar points`, the frame divided out
(A at origin, B one unit along +x), not fitted.

- **Per label:** points by `x, y`; circles by centre + radius; lines by both naqsh
  endpoints lying on the reference line; segments by length; polygons by vertex ring
  (cyclic, either orientation) or by area; free numbers against the naqsh `param` of
  that name.
- **No missing / no extra labels:** a label present on only one side is its own FAIL
  **unless** the lowering accounts for it (a GeoGebra-generated polygon edge, a
  `Sequence` orbit that became the pattern layer, or a conjugate the lowering
  introduced). Check every skip/extra has a stated reason.
- **Threshold:** `1e-6` GeoGebra units per coordinate — a hundred times looser than
  GeoGebra's own `STANDARD_PRECISION` (`1e-8`), ten times tighter than its
  `MIN_PRECISION` (`1e-5`); the largest residual measured was `9.9e-13`.
- **PASS:** every compared label within tolerance and no unaccounted label.
- **FAIL:** one label out of tolerance; the hard case is a `pick` swap onto a
  mirror-image intersection, which O2 cannot see (the drawing is symmetric).

### O2 — drawing (`make naqsh-score`)

Naqsh render placed on the hero export's own pixel grid (computed, never fitted),
compared by centreline recall/precision plus the loop's edge-SSIM.

- **Threshold (quoted from the script, not assumed):** youtube's O2 scorer
  `naqsh_score.py` (at scripts/naqsh_score.py on branch feat/ggb-coords) sets
  `COVERAGE_MIN_DEFAULT = 0.98` (edge recall **and** precision) and
  `SSIM_MIN_DEFAULT = 0.70` (the reconstruct loop's own `--ssim-min`). Recall ≥ 0.98
  and precision ≥ 0.98 is bet `CAL-EQV-01`; edge-SSIM ≥ 0.70 is reported and gated
  but not relied on. Do not hard-code these — pass them through / let the script
  default, and if a construction forces a change, move the bet, not the number.
- **Stale-hero trap:** an old `export.png` can be a stale square scoring recall
  ~0.01. Before trusting an O2 FAIL, rebuild the hero with the reconstruct loop's own
  export and re-run (youtube issue note naqsh-score-stale-hero, feat/ggb-coords).
- **PASS:** recall ≥ 0.98 **and** precision ≥ 0.98 **and** edge-SSIM ≥ 0.70, on a
  confirmed-fresh hero.
- **FAIL:** any of the three below its floor, named. The smallest single-statement
  drop (one rosette of seven) scored recall 0.858 — the margin the corpus ladder,
  not a print, settles.

### O3 — solid (`make reference` → `qiyas mesh compare`)

Two STLs of the flat extrusion: OpenSCAD's `linear_extrude` of the O1 polygons (no
bikar code) vs the `piece … extrude`/coaster STL, same frame, nothing aligned.

- **Directional metrics (gated):** **coverage** — the fraction of the reference's
  mid-height footprint the print covers, on a 0.2 mm grid; **local missing** — the
  largest inscribed disc of reference region the print leaves unfilled (locates a
  dropped petal even when coverage stays high).
- **Threshold:** coverage ≥ 0.99 and local missing ≤ 1.0 mm, bet `CAL-EQV-02`.
- **Reported, never gated:** IoU, 2D/3D Hausdorff, volume ratio, extra fill mm², the
  symmetric disc — bikar's `extrude` solidifies every bounded face, so the naqsh
  solid is a strict superset of the reference and the symmetric metrics cannot gate.
- **PASS:** coverage ≥ 0.99 and local missing ≤ 1.0 mm.
- **FAIL:** a dropped nested ring block → coverage 0.143, local missing 10 mm; a
  0.5 mm translation → coverage 0.975 fails while local missing 0.40 mm passes (the
  floor, not the disc, catches a shifted mesh). A dropped **central** rosette is
  *not* an O3 FAIL — its edges lie inside a bounded face and change no solid; that is
  O2's claim, asserted as O3's blind spot, not a bug.

### What each oracle cannot see (so all three run)

- **O1** is blind to what is drawn or hidden and to `Sequence` orbits — O2/O3 cover it.
- **O2** is blind to a label swap between two objects that draw the same ink, and to
  ink outside the export's view — O1 covers it.
- **O3 (flat)** is blind to interior edges that change no bounded face and to solid
  added beyond the reference (interstitial fill); and it says nothing about the
  finished coaster's rim/bevel/relief — the coaster validators and `CAL-CST-*` do.
