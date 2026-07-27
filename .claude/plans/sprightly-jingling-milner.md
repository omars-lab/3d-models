# Islamic Geometric Orb — bikar/qiyas/3d-models Plan

## Context

Goal (from `~/Downloads/islamic-geometric-orb-handoff.md` + research catalog): a generator that
produces a **sphere covered in an interlaced Islamic star-pattern lattice** and exports a
printable mesh (STL). Two visual families, **both in v1 scope** (user decision):

- **Family 2 — pierced polyhedral lattice**: star patterns built per-face on a subdivided
  polyhedron, background cells pierced, thin rigid struts. (Primary path — simplest manifold.)
- **Family 1 — woven strapwork**: ribbons weave over/under on the sphere. Bikar already solves
  2D over/under ordering (`packages/core/src/kernel/strapwork.ts`, `crossing alternating`), so
  the sweep design must carry crossing parity from day one.

Construction approach (handoff §2): **polyhedral/jitterbug (Bonner)** — base solid, generative
tessellation per face, star inscription (Hankin contact angles), project to sphere, solidify.
Kaplan & Salesin absolute-geometry is noted as future work, not v1.

Decisions made:
1. **Engine lives in bikar (TypeScript)** — new `orb` DSL declaration + `kernel3d/` + mesh emitter.
   Bikar stays producer-of-record.
2. **Both families in v1** — strut/ribbon sweep designed for radial over/under offsets from the start.
3. **qiyas extends to 3D validation via orthographic renders** — per-symmetry-axis views diffed
   against bikar ground truth; DSL-metadata-contract bump on both sides.

Key enabling insight: **no 3D booleans needed.** Bikar's DCEL face extraction
(`packages/core/src/graph/face-extractor.ts`) already yields every void polygon. Struts = inset
void polygons in face-local 2D, triangulate the remaining band (earcut), extrude radially
(inner/outer shell along sphere normals), stitch walls → watertight mesh directly.

## Repo roles

| Repo | Role |
|---|---|
| `~/Workspace/git/bikar` | DSL + geometry engine + mesh/SVG/gt emitters (all new 3D work) |
| `~/Workspace/git/qiyas` | Validation: per-view 2D encode/diff + new orb view-set command |
| `~/Workspace/git/3d-models` | Product end: Makefile `orbs` target, gallery entry, print know-how, gh-pages deploy |

## DSL extension (sketch)

```bkr
orb StarBall
  base icosahedron subdivide 1        # also: dodecahedron | goldberg M N | icosidodecahedron
  radius 60                           # mm
  inscribe Star-5 on faces where sides == 5
  inscribe Rosette-6 on faces where sides == 6
  hankin angle ideal_angle(5)         # cross-face contact-angle consistency
  project spherical                   # or: faceted
  struts width 3 depth 2.4 profile round
  weave crossing alternating amplitude 1.2   # Family 1; omit → Family 2 pierced lattice
  pierce voids
```

`inscribe` references existing `pattern` declarations — each polyhedron face is evaluated by the
existing 2D engine in a face-local frame, so all of girih/hankin/star/rosette machinery is reused
unchanged.

## Milestones

### M0 — Spike (no DSL changes)
Scratch TS script in bikar (`packages/core/scratch/` or a test): hardcoded icosahedron,
one star pattern per face via `compileToGeometry` (`packages/core/src/index.ts:43`), weld shared
edges, normalize to sphere, Family-2 solidify, binary STL out. **Success: STL is watertight and
slices in a slicer.** Proves inset→triangulate→extrude before grammar work.

### M1 — DSL + Family 2 (pierced lattice)
- Grammar: `orb` declaration + statements. Files: `packages/core/src/dsl/tokens.ts`, `lexer.ts`,
  `parser.ts`, `ast.ts`, `evaluator.ts` (orchestration only — per-face eval delegates to existing
  blueprint/pattern evaluation).
- New `packages/core/src/math/vec3.ts` (mirror `vec2.ts` style) and
  `packages/core/src/kernel3d/`: `polyhedra.ts` (Platonic + geodesic subdivision + Goldberg dual),
  `face-frame.ts` (face-local 2D ↔ 3D), `weld.ts` (3D spatial-hash vertex merge, modeled on
  `kernel/point-index.ts`; hard `EvalError` on cross-face edge mismatch — "surface, don't hide"),
  `project.ts` (spherical normalization), `solidify-lattice.ts` (inset voids → earcut band →
  radial extrude → stitch).
- `packages/core/src/render/mesh-emitter.ts` — binary STL (3MF stretch goal).
- New npm dep in `@naqshcoffee/bikar-core`: `earcut` (band triangulation). No other new runtime deps —
  no CSG library needed.
- CLI: `bikar render orb.bkr --format stl|svg|gt` (`packages/cli/src/index.ts`).
- Examples: `patterns/Orbs/Star-Orb.bkr` (+ a goldberg variant).
- Tests (vitest, match existing suites): kernel3d unit tests; snapshot mesh stats
  (vertex/tri counts, volume, watertight assertion); parser/evaluator cases; property test for
  weld idempotence.
- Docs: `docs/language-reference.md`, `docs/architecture.md` (stage list), decision-ledger entry.

### M2 — Family 1 (woven strapwork)
- Trace strands on the **welded spherical graph** (not per-face — strands cross face boundaries),
  reusing strand/crossing logic from `kernel/strapwork.ts`.
- `kernel3d/ribbon-sweep.ts`: sweep round/rect profile along strand polylines with ±`amplitude`
  radial offset from the existing alternating-crossing parity; closed strands ring the sphere.
- `weave` statement wiring + examples (`patterns/Orbs/Weave-Orb.bkr`) + snapshot tests.
- Risk gate: if global crossing parity is inconsistent on some polyhedra (odd cycles), surface as
  an evaluator error with the offending strand, don't silently flip.

### M3 — qiyas 3D validation
- Bikar side: orthographic **front-hemisphere** SVG previews along the base solid's symmetry axes
  (2/3/5-fold for icosahedral), emitted with existing per-face `data-*` attrs plus new
  `data-orb-view` / `data-projection`; extend `render/gt-emitter.ts` with per-view gt
  (`GT_SCHEMA_VERSION` bump). Front-hemisphere-only rendering keeps qiyas's 2D assumptions valid
  (no see-through occlusion).
- Contract: add rows to `dsl-metadata-contract.md` (canonical copy in sacred-patterns; mirrors in
  `bikar/docs/` and `qiyas/src/qiyas/docs/`), each with a witness test per
  `qiyas/tests/test_dsl_metadata_contract.py` convention.
- qiyas side: `SCHEMA_VERSION` bump in `src/qiyas/schema.py` (new contour fields), consume new
  attrs in `stages/svg_primitives.py`, new CLI command (e.g. `qiyas orb-validate`) that encodes
  the view set and aggregates per-view diffs into one composite; canonical orb fixtures in
  `fixtures-canonicals/`; `validate-dsl-contract` coverage for the new attrs.
- Regenerate `@naqshcoffee/qiyas-schema` types; `packages/core/src/contract-conformance.ts` keeps
  the envelope type-locked.
- Mesh gate (bikar test util + CLI flag): watertight, Euler characteristic, min strut width ≥
  printable threshold (default 1.2 mm FDM), degenerate-triangle scan.

### M4 — Publish via 3d-models
- `Makefile`: `orbs` target invoking bikar CLI → STL into `build/stls/`, preview PNG into
  `build/images/` (run through existing `build/process_images.py`); include in `make deploy`.
- `index.html`: new gallery section for orbs alongside cookie cutters.
- Print a physical prototype; feed measured strut results back into default `struts` params.

## Reused code (do not rewrite)

- 2D pattern evaluation end-to-end: `dsl/evaluator.ts`, `kernel/{girih-tiles,star-polygon,intersections}.ts`
- Planar graph/faces: `graph/{planar-graph-builder,face-extractor,polygon-union}.ts`
- Over/under solver: `kernel/strapwork.ts`
- Spatial hashing pattern: `kernel/point-index.ts`
- SVG + gt emission: `render/{svg-renderer,gt-emitter}.ts`
- qiyas pipeline stages unchanged; only new attrs + view-set orchestration added.

## Risks / watch-items

- **Cross-face edge compatibility**: enforce Hankin contact-angle consistency; weld errors are hard failures.
- **Polygon inset at star tips** (very acute angles): clamp/collapse degenerate offsets; fall back to a
  Clipper2 JS port if hand-rolled offsetting struggles.
- **Spherical distortion** of flat per-face patterns: accepted for v1 (matches prior-art orbs);
  absolute-geometry backend is future work.
- **Family 1 parity cycles** on some solids may be globally inconsistent — detect and report.

## Verification

1. `cd bikar && npm test` (vitest incl. new kernel3d/mesh snapshots) + `npm run ci` (madge, eslint, codespell).
2. `bikar render patterns/Orbs/Star-Orb.bkr --format stl` → mesh gate passes; open in slicer.
3. `cd qiyas && make local.ci`; `qiyas orb-validate <renders> --gt orb.gt.json` self-validation composite ≥ 0.95.
4. `qiyas validate-dsl-contract` green on an orb preview SVG.
5. `cd 3d-models && make orbs && make start` — gallery shows the orb with working STL link.
