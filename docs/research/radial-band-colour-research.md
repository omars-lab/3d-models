<!--
provenance:
  date: 2026-09-19
  produced-by: subagent (Claude Opus 4.8) for Omar, read-only recon in worktree 3d-models-bands
  feeds: docs/radial-band-colour-design.md (the radial-band colour route, task #25, D-078)
  method: in-repo reads at the bikar sibling checkout present on this machine
          (~/Workspace/git/bikar-emit, a worktree off bikar main) and the 3d-models checkout
          (~/Workspace/git/3d-models). All anchors are file:line at those checkouts on the date
          above; a line number is a claim about a moving file and is preserved here verbatim as
          it read, not re-pinned, per the research/ exemption (docs-gate-quirks).
-->

# Research — radial-band colour (the ring a polygon sits in, carried into the 3D print)

This file records what the design doc's load-bearing claims trace to. Every claim is an in-repo
read at the bikar checkout `~/Workspace/git/bikar-emit` (a worktree off `main`) or the 3d-models
checkout, on 2026-09-19. Line numbers are as they read that day.

## Headline

The mechanism Omar described — group a construction's polygons by centroid distance from the
centre into concentric bands, then colour each band — **already exists** in bikar's 2D pattern
grammar as the `ring` fill selector. It is a separate, older subsystem than the coaster
`color <region>` work (D-073/D-076). Two parallel colour worlds:

- **2D pattern faces:** per-polygon, has `ring` / `angle-index` binning off a centre — this is the
  ask, already built for SVG styling.
- **3D coaster regions** (bikar PR #213/#216/#275): a fixed three-name enum `base|straps|border`
  for AMS body splitting; not per-polygon, not radial.

The feature is wiring the existing 2D `ring` binning into the 3D region-split path.

## Q1 — Existing colour grammar (`palette` + `color <region>`)

- `palette <name>` block: parser `packages/core/src/dsl/parser.ts:5351` `parsePalette()`; AST
  `packages/core/src/dsl/ast.ts:1554` `PaletteNode { kind:'palette'; name; colors[] }`.
- `color <region> <PaletteName>`: a **coaster-block** statement, parser `parser.ts:3418-3446`;
  region validated inline at `parser.ts:3428` to one of `base|straps|border`; AST type
  `ast.ts:571` `CoasterRegion = 'base' | 'straps' | 'border'` (a fixed union, hard-coded also at
  `kernel3d/coaster.ts:1685`). Evaluator `dsl/evaluator.ts:3658` `resolveCoasterColors()` validates
  against the inscribed pattern's palette.
- Conclusion: region is a **fixed three-value enum** validated in ≥3 places; `color` is a
  coaster-block statement, not a pattern statement.

## Q2 — Polygon representation & centroid (all present, retained post-eval)

- Face type: `packages/core/src/graph/half-edge.ts:40` `Face` — carries `vertices`, `area`, and
  `centroid` (`half-edge.ts:53` `readonly centroid: Point`).
- Centroid computed at extraction: `packages/core/src/graph/face-extractor.ts:211`
  `centroid: computeCentroid(faceVertices)` (vertex-average, not area-weighted).
- Retained post-eval: `EvaluationResult` exposes `faces`, `faceColors` (`evaluator.ts:408`),
  `faceRings` (`evaluator.ts:436`), `faceAngleIndices` (`evaluator.ts:437`); wired through
  `packages/core/src/index.ts:83-84`.
- Construction centre: `evaluator.ts:9760` `findCenter(env)` = centre of the first circle defined,
  else `{0,0}`; used at `evaluator.ts:6294`.

## Q2.5 — The radial-band primitive already exists (2D)

- `packages/core/src/theme/fill-resolver.ts:413` `computeRingBins(faces, center): Map<faceIdx,
  ringIdx>` — "Bucket faces into concentric rings by centroid distance… Bin 0 is innermost";
  1-D clustering of `sqrt(dx²+dy²)` with `TOLERANCE = 1e-2` opening a new ring
  (`fill-resolver.ts:428-439`). This is exactly the ask's grouping.
- Called in eval: `evaluator.ts:6304` `computeRingBins(planarGraph.faces, center)`.
- Author grammar: `ring` is a fill selector attribute (`parser.ts:5235` `FILL_ATTRIBUTES` includes
  `Ring`); `fill where ring == N color <name>` colours a band. `fill` is a pattern-block statement
  (`parser.ts:5206` `parseFill`).
- Rendered as `data-ring="N"` per face: `packages/core/src/render/svg-renderer.ts:665-666`; drives
  per-ring animation (`render/animation-compiler.ts:396-402`).
- Missing: (a) no verb to enumerate bands as a selectable thing; (b) ring colour does not reach the
  3D per-region STL split (which only knows base/straps/border).

## Q3 — Region → body split (`--format parts`, bikar PR #275)

- Kernel: `kernel3d/coaster.ts:2236` `buildCoasterParts(built, {pinch})` → `Map<CoasterPartRegion,
  OrbMesh>`; `CoasterPartRegion = 'base'|'straps'|'border'` (`coaster.ts:1685`).
- Assignment is geometric by height field on a grid, NOT by polygon identity:
  `coaster.ts:1700` `cellRaised()`, `coaster.ts:1722` `reliefRegionCells(field, spec, band)` splits
  raised cells into `straps` vs `border` by cell-centre inset (`coaster.ts:1729-1733`); `base` =
  whole slab flattened (`coaster.ts:1694`).
- CLI: `packages/cli/src/index.ts:2985` dispatches `format === 'parts'`; body writer
  `cli/src/index.ts:913` `writeCoasterPartBodies` — one STL per region + a `<coaster>.parts.json`
  manifest, entry schema at `cli/src/index.ts:884-902` (`region; stl; triangles; paletteName; hex`).
- Awkwardness: the split is over a rasterized height field keyed by the fixed 3-value enum + an
  inset test; it does NOT consult the retained 2D `faces`/`faceRings`. A band feature must map each
  raised grid cell → owning face → ring bin. The enum is hard-coded at parser.ts:3428, ast.ts:571,
  coaster.ts:1685.

## Q4 — AMS / filament slot constraints

- Colour→slot mapping is deferred to the downstream plate composer, not bikar; bikar emits only
  `paletteName`/`hex` in the parts manifest (Q3).
- Live X2D AMS schema (3d-models memory `bambu-x2d-bringup`, 2026-09-17): `print.ams.ams[]` (array
  of units, each with `tray[]`) plus one external spool via `print.vir_slot`; surfacing code
  `tools/bambu/src/commands/filament.ts`.
- **No explicit slot-count constant** was found in either repo. Standard Bambu AMS = 4 trays/unit
  and X2D is dual-nozzle (`nozzle_diameter = 0.4,0.4`), but this is general knowledge, NOT grounded
  in-repo. Treat the band cap (~4, more with multiple units + external spool) as UNVERIFIED and
  confirm against live `bambu filament` output before committing to a number. This is the design
  doc's §7 flag.

## Q5 — Where band-selection tooling would live

- The bikar CLI is a hand-rolled verb switch (`packages/cli/src/index.ts:256` `args[0]`,
  `:2955` `switch (command)`), NOT commander. Existing verbs: `import`, `render`, `parse`
  (`:3269`), `points` (`:3284`), `validate` (`:3329`).
- No existing `list`/`inspect`/`bands` verb. Closest precedent: the `points` verb (`:3284`)
  enumerates named points — the natural sibling for a band enumerator.
- Enumeration data already available: `compileToGeometry(...)` returns `faceRings`/`faceColors`/
  `faces` (`index.ts:83-84`), so a `bands` verb is a formatter over the ring bins + distinct-index
  count — no new kernel work for enumeration.

## Flags carried into the design doc

1. Two disjoint colour systems (2D `fill where ring` vs 3D `color <region>`); the feature straddles
   them — the design decision is whether to unify (design doc §6 chooses: ring colour overrides the
   region key on the faces it covers).
2. Region is a fixed 3-value enum, hard-coded in ≥3 places.
3. The 3D split is grid/height-field based, not face based; bridging needs grid-cell → face → ring.
4. Ring binning is geometric-average centroid + fixed 1e-2 tolerance; band boundaries follow the
   geometry's radial gaps, not author-chosen radii.
5. No in-repo slot-count constant; the band cap is inferred, not grounded (§7).
6. Positives: centroid, `findCenter`, retained faces, ring binning, angle indexing, and `data-ring`
   rendering all exist and survive evaluation — the 2D groundwork is essentially done.
