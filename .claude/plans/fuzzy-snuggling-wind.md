# Pattern → Pinned Tile Set (`mural`): one pattern, c×r LEGO-compatible pieces, one baseplate

## Context

The user wants a new family of lego-based models: one holistic 2D pattern (Islamic
geometry) decomposed along the standard 8.0 mm LEGO stud grid into a c×r array of
rectangular pieces. Each piece carries its clipped pattern fragment as relief on the
top face and a LEGO-baseplate-compatible underside (existing anchor solver: tubes for
≥2×2, pins for 1×N), so pieces placed adjacently on a store-bought baseplate
reconstitute the pattern in top view. Decisions made with the user:

- **Decomposition**: rectangular grid tiles on the stock LEGO 8 mm stud grid.
- **Mount**: LEGO-baseplate compatible (no custom pinboard).
- **Scope**: full house process — design doc + bikar implementation.
- **Seam look: SEAMLESS FIRST.** The current kernel refuses relief pockets that cross
  the ~1.5 mm cavity wall (`requirePocketsInsideCavity`, `bikar
  packages/core/src/kernel3d/brick.ts:434`), which would leave ≈3.4 mm blank "grout"
  stripes between pieces. The user chose to do the kernel rebuild up front so art runs
  flush to every piece edge — only the 0.2 mm physical seam interrupts the pattern.

Three milestones, in order: **A** (bikar kernel: edge-to-edge relief), **B** (bikar
DSL: `mural` declaration), **C** (3d-models: docs, bets, gallery, use-case map).
The design doc + research (C1–C3) come first per house process; they document A and B
before the code lands.

Nothing is reimplemented in 3d-models; all geometry lives in bikar. Prefix every
node/git/npm command with `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`.

---

## Milestone C1–C3 — research + design doc (3d-models, do first)

**C1. Research survey** → `docs/research/lego-baseplate-seam-survey.md`, provenance
header per convention (date, produced-by, method, `Feeds: docs/lego-pattern-set-design.md
(Appendix A) + LG-P coupons`), body verbatim. Scope:
1. Store-bought baseplate dimensional variance — LEGO-brand stud pitch/⌀/height from
   LDraw part files (primary, same method as `docs/research/lego-brick-system-survey.md`),
   cross-checked; clone plates (Mega, generic Target/Amazon stock) pitch/⌀ deltas and
   accumulated pitch error across a 32-stud span. Carry hedges (K1): the existing
   survey already flags a ⌀4.8-vs-5.0 secondary-source split.
2. Prior art on one pattern split across multiple bricks (extends brick survey §8:
   LEGO Art/World Map mosaic UX, dlvoy/base-plate-outliner rectangle decomposition,
   MachineBlocks, printed multi-plate mosaics on Printables/Thingiverse).
3. Seam visibility at ~0.2 mm: FDM top-edge quality, elephant's foot, visual acuity
   for relief-line discontinuities.

**C2. Design doc** → `docs/lego-pattern-set-design.md`. Mirror
`docs/lego-lab-design.md`'s shape. Required content:
- §1 Goals/non-goals — defuse the apparent conflict with `lego-lab-design.md:78`
  ("stock-part mosaic generation" is a non-goal): this is a **printed-part** mosaic,
  cite L78 explicitly (K7). Non-goals: irregular piece outlines, multi-baseplate
  spans, colour.
- §2 Engine ground truth at a named bikar commit (brick kernel, grid-gate
  `SNAP_THRESHOLD_MM 0.05`, `lego.ts` `PART_RELIEF_MM 0.2` / `footprintMm 8n−0.2`,
  anchor solver, `--format parts` / D-006).
- §3 Seam arithmetic + the K10 sentences: (1) `PART_RELIEF_MM` 0.2 transfers as a
  physical-gap prediction (same constant, same use) but **not** as a
  pattern-registration tolerance — the repo's named K10 defect; (2) tile-wall gap
  formula does **not** port (operator-positioned vs stud-registered placement);
  (3) `SNAP_THRESHOLD_MM` is a lattice-snap threshold, not a visual-alignment
  tolerance — seam visibility is empirical → LG-P1.
- §4–5 Language surface + the cut rule: art is cut at **nominal 8 mm grid lines**;
  the physical body (`8f−0.2`) clips each fragment 0.1 mm per side at the edge, so
  exactly 0.2 mm of art is interrupted per seam. K2 discipline everywhere: baseplate
  compatibility claims enumerate the plates surveyed ("LEGO-brand verified;
  clone = CAL-CLB-01, unmeasured"), never "any store-bought baseplate".
- §6 Validators V14+ (continuing lego-lab's V1–V13), each with the D2 marker
  (`**Validator:** …` + `PASS:` + `FAIL:` with a hand-constructed counterexample):
  per-piece anchor solvability (FAIL: 1×1 piece), full-coverage area accounting,
  seam continuity, layout-report consistency.
- §7 Kernel: the edge-to-edge relief change (Milestone A summary) — amends
  lego-lab §7.2's "genuine constraint, not a shortcut" paragraph to historical.
- All `**Default:**` (D3) markers carry a citation or CAL-* id in the same paragraph;
  clutch claims stay qualified "provisional, LG-F1 unprinted" (K1 — bets.md is
  16 provisional / 0 measured).
- Appendix A sources → the research file; Appendix B contested bets; status line
  must agree with Appendix B (K7).

**C3. Register new bets in bikar** (`packages/core/src/kernel3d/calibration.ts`
`CAL_BETS`) so the doc's ids are real before the doc cites them:
- `CAL-REG-01` — seam art registration across the 0.2 mm gap on a real baseplate;
  coupon **LG-P1**.
- `CAL-CLB-01` — clone-baseplate clutch delta vs LEGO-brand; coupon **LG-P2**.
Then `npm run registry:calibration` regenerates `.claude/skills/calibrate/bets.md`
(generated file — never hand-edit).

**C4. Audit**: run `ground-design-doc` on the new doc →
`docs/research/lego-pattern-set-grounding-audit.md`; fix findings.

---

## Milestone A — bikar kernel: edge-to-edge relief (enables seamless)

Route chosen: **scoped planar-graph arrangement** (extends decision
`bikar/docs/decisions/2026-05-07-polygon-clipping-dep.md`; no vendored clipper — a
boolean wouldn't give the shared-coordinate discipline `solidifySlabStack` twin
cancellation requires; the arrangement gives it by construction).

- New `packages/core/src/kernel3d/brick-top-face.ts` (~400 lines):
  `partitionTopFace({bodyOutline, cavityRing, pockets, anchors})` → `TopFaceCells`.
  Only interacting rings enter the arrangement (cavity ring, crossing pockets, body
  outline only when a pocket reaches it); anchors/studs/bores stay out and hole-nest
  as today. Segments only (already-discretized RingCache polylines) — no arc
  consistency problem. Face classification by earcut-interior sample point; band
  annulus synthesized as outline+hole cell when the body ring isn't inserted;
  `presplitFlushEdges` handles the collinear-overlap gap in
  `segmentSegmentIntersection` (T-junction mutual splitting) for pocket edges lying
  exactly on the body outline — the mural cut-edge case.
- `brick.ts`: delete `requirePocketsInsideCavity`; dispatch — legacy zero-arrangement
  path when all pockets strictly inside the cavity (all seven shipped
  `patterns/Lego/*.bkr` presets ⇒ **meshes byte-identical**), arrangement path
  otherwise. Reshape `stackBrickSlabs` to take explicit per-slab cell lists. Guard:
  throw if a stud circle meets a pocket on the arrangement path. Pockets past the
  body outline are clipped with a note (mural relies on this: art cut at nominal,
  body clips the 0.1/side).
- Anchors covered by a wall-crossing pocket nest as holes (tube proud in the recess,
  today's semantics). `solidify-slabs.ts`, `grid-gate.ts`, validators, mesh/print
  gates: unchanged.
- Tests: `tests/kernel3d/brick-top-face.test.ts` + additions to `brick.test.ts` —
  invert the "crosses the cavity wall is refused" test (:180–193); edge-flush pocket
  sharing exact body-outline coordinates stays watertight with no top cap over the
  pocket; anchor-under-crossing-pocket; engage-slab area invariance vs legacy;
  near-tangent ε cases (1e-4, 1e-7); all seven presets hash-unchanged.
- Decision doc `bikar/docs/decisions/2026-08-XX-edge-to-edge-relief-top-face-arrangement.md`.
- Start with a 0.5–1 d spike: `buildIntersectionGraph` on polyline rings (collinear
  overlap, tangency, ε-merge, cost at ~1k segments). ~3.5–4.5 d total.

---

## Milestone B — bikar DSL: the `mural` declaration

**Name**: `mural` (one new reserved word; `mosaic` tainted by lego-lab L78, `panel`
collides with Lab vocabulary). Gate first with
`npx tsx scripts/corpus-sweep.ts` (328 .bkr, four repos); fallback `panelwork`.

**Grammar** (`docs/grammar.md` new section + §12 surface table; `x`/`of` are bare
identifiers per the footprint precedent):

```
mural StarMural
  inscribe Star
  pieces 4 x 4 of 4 x 4      # c x r pieces of f x g studs
  height 3 plates
  relief depth 0.6
  # blanks emit|skip (default emit) · slivers drop|keep|error (default drop)
```

`studs none` default, `anchors auto`, `clutch auto`; `relief depth` required > 0;
no `footprint`/`origin` (derived). Pattern recentred, never scaled (real-scale rule);
hard error if bbox exceeds the nominal (8·c·f)×(8·r·g) panel.

**Decomposition — graph injection, not polygon clipping** (reuse the
`clip pattern to boundary` route, evaluator.ts:3153/:3363/:3397):
1. Pattern registry keeps the AST node (`evaluator.ts:819`); `evaluatePattern` gains
   `extraCutEdges` appended into the existing `extractPlanarGraph` call (:3867).
2. `evaluateMuralDecl` injects the c−1 + r−1 **nominal** cut lines (pure multiples of
   8.0 — the 0.1/side body inset stays physical, never an art offset: K10).
3. Faces sourced only from `grid:` tags are dropped (mirror of `applyClipFilter`'s
   pure-boundary drop); surviving faces bucket by centroid into cells (cannot
   straddle — split at the lines).
4. Per cell: `faceComponents` + `unionPatternFaces` via a helper refactored out of
   `brickReliefPockets` (evaluator.ts:2193), recentred to piece-local frame. With
   Milestone A landed, fragments run to the nominal edge; the kernel clips at the
   physical body outline. Seam continuity is free: one planar graph ⇒ bit-identical
   vertices on both sides of every cut line.
5. Policies: slivers (< `BRICK_MIN_FEATURE_MM` 0.7) drop/keep/error with area ledger;
   enclosed-island error message names the cell; empty cells → blank brick
   (`blanks emit`) or omitted with report note (`skip`).

**Per-piece build + result shape**: factor `evaluateBrickDecl`'s tail into
`buildBrickResult(spec, fit)`; mint `BrickSpec` per cell named `P_c<i>r<j>`;
`solveAnchors`/`partitionBrick` untouched (f×g≥2×2 tubes, 1×N pins, 1×1 none →
warning). Result is **assembly-shaped** (`assembly3d` with `exportParts: true`, one
translated `PlacedPart` per piece) plus a new `mural3d` provenance for the layout
report. CLI: `--format parts` (→ `<Mural>-P_c0r0.stl`…), `--check`, and LDraw MPD
work unchanged (geometry-keyed interning dedupes identical blanks); add
`printMuralReport` (placement table, blanks, sliver/coverage ledger, gridFit score).

**Validators**: per-piece V1/V3/V4/V5b/V6/V7/V10/V13 via `validateBrick` with
`P_c<i>r<j>:` prefixes; new panel-level V-M1 (required stmts), V-M2 (bbox fits,
names smallest `pieces` that would), V-M3 (area conservation: fragments + dropped
slivers ≈ pattern bounded area, rel 1e-6), V-M5 (pocket vertices within cell ±
`SNAP_THRESHOLD_MM`), V-M6 (zero-anchor pieces listed), V8-panel (gridFit < 0.8
warning — warning not gate: quasiperiodic rosettes are the primary use case and
seams match by construction). Cap total pieces at 64 with a named error (perf, R2).

**Tests**: `tests/dsl/mural-parse.test.ts`, `tests/kernel3d/mural-split.test.ts`
(area conservation, exact seam coordinates, bucketing, sliver detection),
`tests/kernel3d/mural-brick.test.ts` (parts count, watertight per piece, anchor
kinds by piece size, island error names cell), `tests/dsl/mural-eval.test.ts`
(assembly shape, xforms on 8f pitch, policies), CLI export test (parts naming,
LDraw FILE blocks, `--check`). Grammar-conformance picks up new fences; update
`keywords.snapshot.txt`.

**Decision doc**: `bikar/docs/decisions/2026-08-XX-mural-panelization.md` (name,
graph-injection over clipping, gridFit-as-warning, nominal-line cut rule).

**Preset**: `patterns/Lego/Star-Mural.bkr` (or `patterns/Sets/` — see C6). Tenet 32:
`patterns/` is a public surface — call out in review. Lab: entry in
`packages/lab/src/lego-scripts.ts` registry; `viewer.ts` `WallInstance {x,y}`
already previews placed grids.

---

## Milestone C5–C9 — 3d-models integration (after B ships)

- **C5. Decisions log**: `D-008` in `docs/decisions-log.md` (D-007 template): the
  nominal-line cut rule + the printed-part/stock-part L78 ruling; reversal condition
  = LG-P1's physical measurement.
- **C6. Makefile**: `make bricks` renders one STL per .bkr — a mural needs
  `--format parts`. Add a `pattern-sets` branch/target invoking
  `--format parts -o build/stls/<name>/` plus a composed preview (all pieces placed
  at layout-report coordinates — the honest gallery image; extend
  `build/brick_previews.py`). Not automatic — real Makefile work.
- **C7. Gallery**: `index.html` `BRICKS` entry (shape at L449): `tag:"Set"`,
  specs like `["4 × 4 pieces","4 × 4 studs each","seam 0.2 mm"]`, lab deep link;
  clutch claims hedged per the array's own header discipline.
- **C8. Coupons + backlog**: append to `.claude/skills/prototype/catalog.md` after
  LG-B2 (~L899): **LG-P1** two-piece seam-registration coupon (two 2×2 pieces, one
  motif crossing the seam, on a real LEGO plate; blocked on LG-F1 — needs a measured
  rib to seat) and **LG-P2** clone-plate clutch differential. Register both in
  `docs/backlog.md` §3.2 (print-gated register). Print work stays **HELD** pending a
  printer (Bambu A1/P1S/X1C class, per memory).
- **C9. Use-case map**: add `UC19` row + mermaid node in
  `.claude/skills/maintain-use-cases/use-cases.md` with pointers to the new bikar
  files, the design doc, Makefile target, gallery line, LG-P1 entry; then
  `python3 .claude/skills/maintain-use-cases/validate.py --refresh`.

**Gate commands before each 3d-models commit** (hooks re-run them):
1. `make validate-docs` (D1/D2/D3), 2. `make validate-pointers` (new K9 pointer
gate — backticked sibling paths must resolve at a git ref; files still-to-be-authored
belong in `.claude/gates/doc-pointer-baseline.json`, a deliberate-grow ratchet),
3. `make validate-use-cases` / `--refresh`, 4. in bikar: full `npm run ci`
(grammar conformance, keywords snapshot, calibration ratchet, pointers, decisions).

## Sequencing summary

1. C1 research survey → C2 design doc → C3 register bets + regen bets.md → C4 audit.
2. A: kernel spike → `brick-top-face.ts` → integration → tests → decision doc.
3. B: corpus-sweep name gate → grammar/parser/AST → decomposition → per-piece build →
   validators → CLI/report → tests → decision doc → preset + Lab entry.
4. C5–C9: D-008, Makefile target, gallery, coupons/backlog, UC19 + refresh.
5. Print-gated (HELD until printer): LG-F1 ladder → LG-P1/LG-P2 → bets flip
   provisional→measured → doc qualifiers may firm up.

## Verification

- bikar: `npm run ci` green; all seven shipped Lego presets produce hash-identical
  meshes (legacy dispatch); new mural preset renders via
  `bikar render patterns/Lego/Star-Mural.bkr --format parts --check` → c·r watertight
  STLs; `--format ldraw` MPD has one FILE block per distinct piece; layout report's
  area ledger closes (V-M3).
- Seamless proof: mural-split test asserts both sides of every interior cut line
  share exact vertex coordinates; brick-top-face test asserts no top-face cap over an
  edge-flush pocket (art reaches the physical edge).
- 3d-models: `make validate-docs validate-pointers validate-use-cases` green;
  `make bricks` + new set target produce gallery previews showing the reconstituted
  pattern; commit passes all pre-commit hooks.
- Physical verification (LG-P1/P2) is registered but held pending a printer.

## Key risks

- **R2 perf**: arrangement cost on dense patterns at 8×8 pieces unmeasured — spike
  measures; 64-piece cap in v1.
- **R3**: rib-lobe arc interaction with edge-reaching pockets — re-check
  `clampRibArc` geometry during A integration.
- Collinear-overlap presplit vs `PointIndex` ε-merge: spike item; fallback is
  exact-coordinate reuse enforced at the mural-clipper contract.
