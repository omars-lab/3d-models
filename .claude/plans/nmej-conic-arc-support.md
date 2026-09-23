# nmEjCTzMbDg — conic + arc-edge engine support (build plan)

Owner decision 2026-09-20: **build conic + arc support now** (chose over defer / scope-first /
drop). Large multi-PR bikar-first effort. This plan is the durable decomposition.

## What nmEj actually needs (from reading construction.ggb-commands)

The only drawn art is `@export ring*` (line 124) = `Sequence(Rotate({e_1, f_1, g_1, d_1, a},
2πi/n, H), i, 0, n-1)`. So the petal unit that gets orbited is:

| member | kind | role | status |
|--------|------|------|--------|
| `e_1`,`f_1`,`g_1` | **CircularArc(centre, start, end)** | the three scallops (DRAWN) | net-new curved edge |
| `d_1` | **Circle** (rim circle) DRAWN | net-new: full circle as a drawn element |
| `a` | Segment | the spoke | supported |

Scaffolding (all `@hide`-den, never drawn — lines 103–104, 116):
- `d = Parabola(J, m)`, `q = Parabola(N, m)` — parabola = locus equidistant from a point & a line.
  Used ONLY via `L = Intersect(d, p, 2)`, `O = Intersect(q, p, 2)` → arc centres.
- `t = Hyperbola(H, Q, K)` — used ONLY via `R = Intersect(t, m, 2)` → rim-circle centre.
- `c' = Reflect(c, s)` where s is a **circle** → **circle inversion**; `d_1 = Reflect(c_1, s)` too.
- `Q = Center(c')`, `D = Center(d_1)` — circle centre accessor.
- `K = Reflect(J, B)`, `N = Reflect(J, L)`, `T = Reflect(S, D)` — **reflect a point across a POINT**
  (half-turn).
- `ClosestPoint(m, L)` (M, P) — tangency points (may already be supported; verify).

**Key scope narrowing:** the conics are never drawn, so they need only enough evaluator support to
compute `Intersect(conic, line, index)` with a STABLE index (the video fixes index=2 = the H side;
topology stable for all n). No conic meshing/emit. The genuinely net-new *drawing* surface is
**circular-arc pattern edges + full-circle elements** (e_1/f_1/g_1/d_1).

## Reflect has three unsupported forms here
1. point across point (half-turn) — easy.
2. circle across circle (inversion) — non-trivial inversive geometry, produces a circle.
3. (point across line already supported: `I' = Reflect(I, p)`.)

## PR decomposition (bikar-first, ROI order: smallest reusable win first)
- **PR-1 Reflect-across-a-point** — importer cookbook + evaluator half-turn. Tiny, independent.
- **PR-2 Center + Reflect-across-a-circle (inversion) + ClosestPoint (if missing)** — construction
  ops that yield points/circles. Foundation for the hyperbola focus (Q) & rim circle (d_1).
- **PR-3 Parabola + Hyperbola loci + Intersect(conic, line, index)** — evaluator conic support with
  stable index; no drawing. The scaffolding math.
- **PR-4 Circular-arc pattern edges + circle-as-edge in kernel** — AST arc-edge node, evaluator
  arc geometry, emitter, kernel3d arc→strap solid, mesh gate, O2/O3 coverage. The big surface.
  **Reshaped + split in the build session** (see State): the coaster relief is an SDF, not a
  lofted solid, so a curved strap needs ZERO kernel geometry — tessellating each `ArcEdge` at the
  evaluator boundary is indistinguishable from the true arc at the field's 0.4 mm sampling pitch
  (K10: valid *because sampled, not lofted*). PR-4 splits into:
  - **PR-4a** (steps 1–2): the DSL arc-**drawing** surface — arc straps raise as relief in
    `resolveCoasterArt`/`resolveBorderCell`, and the printer emits `connect arc` for round-trip.
    Mergeable and valuable on its own (arcs already exist in `env.arcEdges` via `connect arc`).
  - **PR-4b** (steps 4–5): the arc-**importer** surface — CircularArc lowering (`connect arc`
    node, computing `major` from the CCW sweep), an `arc` leaf in the orbit expression so
    `Rotate({…arcs})` lowers arcs inside `rotate N around` blocks, and the full-circle drawn element
    (`d_1`, as two CCW half-arcs sharing a synthesised host circle). This is what PR-5 consumes.
  - **Measured pivot (2026-09-20):** step 3 = **major-arc support**, folded into PR-4a not PR-4b.
    `arcFromPoints` normalized to the minor arc, but nmEj's scallops are all MAJOR (g_1 CCW sweep
    231° at n=7 → 198° at n=20, every one > π; GeoGebra `CircularArc` draws CCW start→end, which
    fixes which of the two arcs). Minor-only import would silently draw the wrong inward arc (K1/K10
    trap). Major-arc is engine work, so it belongs on the drawing surface. See
    `bikar-rdux:docs/issues/2026-09-20-connect-arc-major-sweep.md`.
- **PR-5 Migrate nmEj** end-to-end (fixture, base, coaster, goldens; O1/O2/O3), then 3d-models
  vendoring. Only after 1–4 land on bikar main.

Each PR: bikar-first, own branch off bikar main, verified (validate + oracle + mesh gate +
goldens), owner-merged. Ground each in how the existing importer/kernel work (K10: state transfer
conditions). Document the arc-edge model in 3d-models docs/ (design-doc home) as PR-4 lands.

## State
- **✅ COMPLETE (2026-09-22): CS-9 vendoring shipped as 3d-models PR #291** (`feat/vendor-nmEjCTzMbDg`,
  commit `0ef7650`), awaiting owner merge. Rendered from bikar main's `nmEjCTzMbDg-coaster.bkr` with a
  fresh CLI build at `origin/main` (87ea3b4, #243): standard 160,860 tri / 31.7 cm³, mini 32,240 tri /
  6.4 cm³ — **mesh gate PASS** (watertight, euler 2, 0 degenerate, minFeature 1.2 mm) + **linkage PASS**
  (1 body). 7-file shape (CS-9 catalog entry; ledger row + migrated 5→6; backlog catalog-entries 40→41;
  pointer-baseline mini grandfather; UC28 anchor L72→L75; fixed stale "CS-1…CS-6 and CS-8"→"CS-1…CS-9").
  All 17 pre-commit hooks green. **This is the last unlanded construction migration** — all 6 migratable
  reconstructions now vendor a printable coaster; bikar PR-5 #243 is merged. Nothing left on this plan.
- **ALL MERGED (2026-09-21, explicit owner auth):** bikar arc/conic chain #230→#231→#232→#233 and
  constructions #228 (sDO9) / #229 (n3I) are on bikar main (`0191780`); 3d-models coaster vendorings
  #287 (rDux, CS-8) / #284 (lEf, CS-7) are on master (`4d7f072`). #229, #284 and the arc chain each
  needed hand conflict resolution (golden test-slot collisions; ledger/backlog/catalog/pointer count
  drift — ledger now reads **5 migrated**, catalog **40 entries**). PR-4b is now unblocked.
- Shipped earlier: sDO9 (bikar #228), n3I (bikar #229) — MERGED; 3d-models vendoring MERGED (#287/#284).
- **PR-1 SHIPPED — bikar #230** (`feat/reflect-across-point`): Reflect-across-a-point lowers to
  `rotate 180 around C` (one code path; no new AST/parser/evaluator/emitter — the treatment
  transforms §3 already prescribed). 125 import tests, all pre-commit gates green. Awaits owner
  merge. NOTE: the bikar pre-commit `gen-calibration-registry` + calibration-records hooks read
  the SHARED 3d-models checkout — stale on `feat/x2d-slice-preflight`; commit with
  `THREED_MODELS_DIR=/Users/omareid/Workspace/git/3d-models-master-ro` (at origin/master).
- **PR-2 SHIPPED — bikar #231** (`feat/circle-inversion`): a fourth transform arm `invert P in s`
  / `invert c in s` — the first non-isometric transform. Kernel `invertPoint`/`invertCircle`
  (image-circle centre is NOT the inverse of the source centre — uses the power
  `s = k²/(|C−O|²−ρ²)`); evaluator special-cases deriveCircle, refuses invert on line/polygon
  (kind-changing); `reflectBuilder` lowers a circle axis to `invert`. Center AND ClosestPoint were
  already supported (lower.ts:542-560), so PR-2 was JUST the inversion arm. 128 tests, all
  pre-commit gates green. Awaits owner merge. Branched off origin/main, NOT stacked on #230; the
  reflectBuilder edit is a clean both-kept merge with PR-1's point arm.
- **PR-3 SHIPPED — bikar #232** (`feat/conic-loci`): Parabola + Hyperbola loci +
  `Intersect(conic, line, index)` with a stable index. New `kernel/conic.ts` represents every conic
  as an implicit quadratic `a·x²+b·xy+c·y²+d·x+e·y+f=0` (focus+directrix / foci+through), one
  `lineConicIntersection`/`segmentConicIntersection` serves both, crossings returned in increasing
  line-parameter order (the `pick N` contract). Grammar `parabola <id> focus <pt> directrix <line>`
  / `hyperbola <id> foci <pt> <pt> through <pt>` — only the two heads reserved, modifier words stay
  contextual. Conics live in `env.conics`, are never drawn/meshed/filled, feed `intersect` via the
  existing pick machinery; conic×conic / conic×circle refused. Importer lowers Parabola/Hyperbola/
  Intersect-conic (numeric-semi-axis Hyperbola is a distinct cookbook gap). Printer round-trips both.
  docs/grammar.md §7.12 + §12 rows; regenerated keyword snapshot + highlight artifacts. New tests:
  kernel/conic.test.ts (17), dsl/conic.test.ts (8), lower.test.ts conic shapes. Full core suite
  green (234 files, 4087 tests). Branched off origin/main, NOT stacked on #230/#231. Awaits owner
  merge.
- Terrain map (importer cookbook + edge model) is IN HAND — see the session's exploration report;
  arc edges already exist in the 2D graph (`env.arcEdges`, `connect arc`, conjugation), so PR-4's
  net-new work is the coaster-strap arc branch (resolveCoasterArt drops arcs at evaluator.ts:3474)
  + CircularArc importer lowering, not the whole 2D arc substrate.
- **PR-4a SHIPPED — bikar #233** (`feat/arc-strap-edges`): the DSL arc-drawing surface, two commits.
  - *Step 1 (8089bbd):* `resolveCoasterArt`/`resolveBorderCell` inscribe `env.arcEdges` alongside
    straight segments via new `arcEdgeToSegments(arc, ARC_STRAP_SAGITTA_MM)` in `kernel/arc-ops.ts`
    (delegates to the existing `arcToSegments` loop; chord count derived from the sagitta so every
    chord stays within tolerance regardless of radius/sweep). Tolerance
    `ARC_STRAP_SAGITTA_MM = COASTER_GRID_PITCH_MM / 4 = 0.1 mm`, coupled to the pitch constant so it
    tracks (CAL-FEA-01). No `EvaluationResult` change — `mergeInto` already pushes child arcEdges up.
  - *Step 2 (76a0a72):* printer `connect arc` case (`printer.ts` `connect()` method) — single-pair,
    bracketed multi-pair, and bare arcs round-trip; non-arc connect modes still throw `PrinterError`
    ("lowered subset only" honesty).
  - *Step 3 (b3acdb2) — MAJOR-ARC support (the measured pivot):* `arcFromPoints(circle, from, to,
    { major })` — reflex branch subtracts a full turn in the sweep direction after minor
    normalization. `ConnectArcNode.major?`, contextual `major` parse (identifier match, not a
    reserved token — zero `major` uses across 239 .bkr; after `on <circle>`, before `.class`),
    printer emits `major` only when set, evaluator threads `node.major`. `arcEdgeToSegments` needs
    NO change — it derives segment count from the arc's own angles, so a major arc tessellates from
    correct angles. docs/issues pivot record + 7 new tests (5 arcFromPoints, 2 printer round-trip).
  - Tests: arc-ops (sagitta invariant at tol 1/0.1/0.01, endpoints, single-chord collapse; +
    arcFromPoints minor/major/complementary/endpoints/far-side), coaster-eval (arc-only pattern
    builds watertight relief + raises the field at the bulge — throws pre-fix), printer-connect-arc
    (single/bracketed/bare + major round-trip + minor omits). 66 tests across the three suites;
    tsc/eslint/prettier/calibration/doc-pointers/page-frame/gitleaks green. Branched off origin/main
    at #227 (list-literal importer fix), NOT stacked on #230/#231/#232. Awaits owner merge.
- **PR-4b SHIPPED — bikar #234** (`feat/arc-importer-lowering`, off origin/main 0191780, NOT
  stacked): CircularArc/full-Circle/Segment lowering in `lower.ts`. `CircularArc(centre,start,end)`
  → `connect arc … on <synthesised host>`, `major` from the endpoints' CCW sweep read from
  `cached_coords` (refuses when the XML carried no coords — never guess the arc, K1/K10). Full
  `Circle` → `divide … into 2` + two complementary CCW half-arcs. Drawn `Segment` → `connect
  points`. New `arc` `Kind` + a `draw` `OrbitExpr` leaf so arc/circle/segment members ride
  `Sequence(Rotate({…}))` replication (importer glue — `evalRotate` already replicates arcEdges/
  segments); `conjugate` refuses a transform of a list holding a curve. `exportOutput` split into
  `drawnPatternNodes` to keep complexity ≤ 10. **Scope expanded beyond the literal plan:** the
  Segment leaf is included too, so **PR-5 needs zero further _bikar_ changes** (see the probe below
  for the one remaining _non-bikar_ input).
  +9 `lower.test.ts` cases incl. a K7 evaluator round-trip. All pre-commit gates green. Awaits owner
  merge.
- **PR-5 READINESS PROBE — 2026-09-21 (this session).** Ran the real importer on nmEj against the
  #234 worktree (`bikar-rdux`@`feat/arc-importer-lowering` b1a8ae1): `make ast IN=…/nmEjCTzMbDg/
  construction.ggb-commands` (youtube) → `node packages/cli/dist/index.js import geogebra <json>
  --coverage`. **Rebuild core+cli first** — the checked-in `cli/dist` was stale and masked the
  CircularArc dispatch entry behind the generic "unsupported command" refusal; after
  `npm run build --workspace @naqshcoffee/bikar-core --workspace @naqshcoffee/bikar-cli` the true
  refusal appeared. **Verdict: the engine is COMPLETE.** Import refuses ONLY the three
  `CircularArc(...)` lines (100–102) + the one dependent (117), and ONLY with the by-design
  `CircularArc/no-coords` message — `arcIsMajor()` reads the CCW sweep from `cached_coords` and
  refuses rather than guesses when absent (K1/K10). Reflect-across-point (#230), Parabola/Hyperbola
  loci (#232), `invert` (#231) and `Sequence(Rotate({…}))` (#227) all lowered silently — **no other
  gap.** Our `make ast` emitted `cached_coords: {}`, which is why the arcs refused.
> Superseded — see State above (producer built in bikar #236, nmEj shipped via #243).
- **⚠ PR-5's one remaining input is `cached_coords`, and its PRODUCER IS UNBUILT.** The plumbing
  exists (`ggb_build.py --ast-json --cached-coords <{label:[x,y]}.json>`, youtube), but the coords
  source is deferred: `youtube:docs/design/construction-ast-export.md` §cached_coords points at
  "P1.2b's GgbAPI dump" and `youtube:docs/design/geogebra-applescript-automation.md` is still
  **Status: design**. So PR-5 waits on TWO things: (a) bikar **#234 merging** (owner), and (b) a
  cached_coords producer for the 9 arc endpoints (O,P,P',L,M,M',B,I,I') — build P1.2b (GgbAPI/
  headless dump) in youtube, or compute the 9 coords another deterministic way. **Do NOT** hand-edit
  the `.bkr` or add a coords-free arc-direction guess to the importer; the refuse-don't-guess design
  is correct.
- **MAIN-RED CLEANUP SHIPPED — bikar #235** (`fix/main-red-bookkeeping`, off origin/main, NOT
  stacked): repaired the five pre-existing red test files so the effort's CI can read green.
  `keyword-snapshot`/`highlight-generated` = `invert` (#231) added without regenerating the
  snapshot + tmLanguage (regenerated both; `grammar.md` §2.4 count 138→139). `point-parse` =
  the "point expression after `=`" refusal now lists `invert` (updated the expected message).
  `grammar-conformance` §12 = the coverage-row regex required exactly one space before the second
  pipe, so Prettier's column alignment left it matching only the widest keyword per table
  (`phyllotaxis`, `blueprint`) — widened the gap to `+` (robust fix). `pattern-manifest`/
  `public-surface` = the five construction migrations (#227–#229) landed `.bkr` files on disk but
  not in `patterns/index.json`/the coaster roster/the published count — added 10 manifest entries,
  5 coaster roster entries (each passes every CV + watertight at default/40/90), +10 to the count.
  Full suite green: 299 passed, 1 skipped, 3 expected-fail. PR CI is billing-blocked (`steps:0`),
  so local green is the authority. Awaits owner merge. **NOT invert-only as first assumed** — the
  §12 regex drift predated #231 (broke whenever Prettier aligned the table); the summary's
  "invert fallout" label was imprecise.
- ~~**PR-4b NEXT**~~ (steps 4–5): CircularArc importer lowering in `lower.ts` (emit a `connect arc`
  node, computing `major` from the CCW sweep of `CircularArc(centre, start, end)`; extend the `Kind`
  union with `'arc'`; extend `OrbitExpr` with an arc leaf so `Rotate({…})` lowers arcs inside
  `rotate N around` — `evalRotate` already replicates arcs via `replicateArcsRadially`, so this is
  importer glue not engine work), plus the full-circle drawn element (`d_1`, as two CCW half-arcs),
  plus `lower.test.ts` coverage. Serves PR-5. Branch off origin/main (NOT stacked on #233).
