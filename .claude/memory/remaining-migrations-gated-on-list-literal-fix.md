---
name: remaining-migrations-gated-on-list-literal-fix
description: "P5.1 construction-migration status (2026-09-21, updated): list-literal fix (#227), reflect-across-point (#230), invert (#231), parabola/hyperbola loci (#232), CircularArc/Segment importer lowering (PR-4b #234), and the cached_coords producer (#236, B′ self-bootstrap D-080) are ALL MERGED to bikar main. rDuxHF3xMOc/sDO9fpu76v8/n3IidKfXE1I/lEfWSogWscs/tA8eSdVx_EQ migrated + rostered (#235). nmEjCTzMbDg engine path is now COMPLETE end-to-end: with real cached_coords injected the 3 CircularArc scallops lower, and the ONE remaining engine gap — the printer crashing on the lowered `connect points` (drawn Segment) — is fixed in bikar #238 (OPEN, owner-gated merge). With #238 the full nmEj import is 0 refused / 0 dropped and renders. nmEj migration to bikar (fixture/golden) + the 3d-models vendoring PR both wait on #238 merging."
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-21T21:10:55.083Z
---

The P5.1 migrations each used a **transform of a brace-group list literal** —
`Reflect({a,b,…}, ax)` or `Sequence(Rotate({a,b}, …))` — the case bikar PR #227
(`feat/rdux-construction`) fixed in `lowerTransform`. **#227 MERGED 2026-09-21**, so
that linchpin is gone and branches base off bikar main normally (never stack on an
open branch — [[stacked-pr-stranding]]).

**Status 2026-09-21:**
- **rDuxHF3xMOc, sDO9fpu76v8, n3IidKfXE1I, lEfWSogWscs, tA8eSdVx_EQ — ALL migrated
  and on bikar main.** Their base `.bkr` + coaster `.bkr` are on disk; **bikar #235**
  (main-red cleanup) rostered all five coasters into `patterns/index.json`, the
  Coaster Lab roster (`coaster-scripts.ts`) and the published-source count. Each
  coaster passes every CV and stays watertight at default/40/90 (the `coaster-presets`
  gate proves it). 3d-models vendoring PRs land per [[pr-flow-for-all-repos]] once each
  `.bkr` is on bikar main (pointer/ledger gate resolves it at bikar's git ref — never
  `CONSTRUCTIONS_OK=1`).
- **nmEjCTzMbDg (#34) — the SOLE remaining P5.1 construction.** Its base import needs
  surfaces main didn't have — and **every one is now in the engine**: `Parabola`/`Hyperbola`
  loci (**merged #232**), `Reflect(J, B)` = reflect across a **point** → `rotate 180 around B`
  (**PR-1, bikar #230, MERGED** — re-confirmed composing by the probe below), circle inversion
  `invert` (**#231**), and `CircularArc` (×3) + drawn `Segment` importer lowering (**= PR-4b,
  bikar #234, OPEN, awaiting owner merge**). The scallops `e_1/f_1/g_1` are the CircularArcs
  and the tangent-circle centres come off the Parabola/Hyperbola loci — load-bearing, not
  droppable.

  **Empirical probe (2026-09-21, on the #234 worktree `bikar-rdux`@`feat/arc-importer-lowering`
  b1a8ae1):** produced the AST JSON with `make ast IN=reconstructions/nmEjCTzMbDg/construction.ggb-commands`
  (youtube repo) and ran `node packages/cli/dist/index.js import geogebra <json> --coverage`
  (**rebuild core+cli first — the checked-in cli/dist was stale and hid the CircularArc dispatch
  entry behind the generic "unsupported command" refusal**). Result: import refuses ONLY the
  three `CircularArc(...)` lines (100–102) + the one line depending on them (117); the refusal is
  the **by-design** `CircularArc/no-coords` — `arcIsMajor()` reads the CCW sweep from
  `cached_coords` to fix major-vs-minor and **refuses rather than guesses** when coords are absent
  (K1/K10; `bikar:docs/issues/2026-09-20-connect-arc-major-sweep.md`). Our `make ast` emitted
  `cached_coords: {}`, so the arcs cannot resolve. Reflect-across-point, parabola/hyperbola loci,
  invert, `Sequence(Rotate(...))` all lowered silently — **no other gap**.

- **The cached_coords producer is now BUILT and MERGED** (was "unbuilt" above): bikar **#236**
  ships `evaluatedCoords()` / `import geogebra --emit-coords` — the **B′ self-bootstrap** (D-080,
  [[option-evaluation-axes]]): `evaluatedCoords(ast, {lenient:['CircularArc']})` drops the arcs,
  evaluates the construction with bikar's **own kernel**, and reads back `{label:[x,y]}`. No
  GeoGebra dump, no new engine. Applied to nmEj it produced all 20 point coords incl. the 9 arc
  endpoints (O,P,P',L,M,M',B,I,I'), which `ggb_build.py --cached-coords` (youtube) injects into the
  AST. **Never hand-edit the `.bkr` and never add a coords-free arc-direction guess** — but writing
  REAL evaluated cached_coords IS the sanctioned mechanism.

- **NEW engine gap found + fixed (2026-09-21): printer crashed on `connect points`.** Once the
  arcs lower (coords present), the nmEj import reaches its drawn `Segment` `H -> T` and dies with
  `PrinterError('connect points')`: `Printer.connect` covered only `mode:'arc'`, but `lower()` has
  ALWAYS lowered a drawn Segment to `connect points` (`segmentDrawNodes`) — the "arc-only lowered
  subset" was documented/tested yet never true, just never exercised until a segment met lowerable
  arcs. **Fixed in bikar #238** (`fix/printer-connect-points`, OPEN): printer emits `connect A -> B`
  / `connect [ … ] .class` (inverse of the parser), stride/cycle still refuse (lower never emits
  them). Verified: 11 printer tests, 1360 dsl+import tests, and `import geogebra nmej-ast-coords.json
  --coverage` = **0 refused / 0 dropped** (3/3 CircularArc, 1/1 Segment), lowered `.bkr` renders.
  `bikar:docs/issues/2026-09-21-printer-connect-points-crash.md`.

**How to apply:** the nmEj ENGINE is complete; the migration now waits on ONE thing — bikar **#238
merging** (owner-gated, phantom billing block: MERGEABLE + BLOCKED, `steps:0`). Do NOT stack the
nmEj fixture/golden PR on #238's branch ([[stacked-pr-stranding]]). When #238 is on main: branch
off *current* bikar main (fetch first), regenerate the AST with `--cached-coords`, confirm ZERO
unlowered via `--coverage`, then the standard fixture → base → coaster → goldens → O1/O2/O3 flow,
then the 3d-models vendoring PR. The scratchpad already holds `nmej-coords.json` (20 coords) and
`nmej-ast-coords.json` (AST with coords injected). Related: [[islamic-orb-project]],
[[orb-repo-roles]], [[3d-models-use-case-hook]], [[decision-id-collision-recurred]].
