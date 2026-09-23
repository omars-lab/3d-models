---
name: remaining-migrations-gated-on-list-literal-fix
description: "P5.1 construction migration is COMPLETE (2026-09-22): all five list-literal constructions (rDuxHF3xMOc, sDO9fpu76v8, n3IidKfXE1I, lEfWSogWscs, tA8eSdVx_EQ) on bikar main + rostered (#235); nmEjCTzMbDg shipped via bikar PR-5 #243 after #238 (printer `connect points`) merged 2026-09-21; 3d-models master vendors CS-1/2/6/7/8/9/10/11 (CS-10/CS-11 via #294); ledger = 8 migrated, 1 no-piece-by-design, 0 remaining. File keeps the migration techniques: list-literal transform fix, rebuild before probing, refuse-don't-guess arcs, real evaluated cached_coords via --emit-coords (B′, D-080), printer must emit everything lower() produces."
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-23T04:33:07.000Z
---

**Status 2026-09-22: P5.1 is done.** The five brace-group list-literal constructions
(rDuxHF3xMOc, sDO9fpu76v8, n3IidKfXE1I, lEfWSogWscs, tA8eSdVx_EQ) are on bikar main and
rostered into `patterns/index.json`, the Coaster Lab roster and the published-source count
(bikar #235). bikar #238 (printer emits `connect points`) MERGED 2026-09-21T21:19Z, which
unblocked nmEjCTzMbDg: migrated via bikar PR-5 #243 and vendored as CS-9. 3d-models master now
vendors CS-1/2/6/7/8/9/10/11 — CS-10 (n3Ii) + CS-11 (sDO9) landed via PR #294 (350d134).
`docs/constructions/ledger.md` reads **8 migrated, 1 no-piece-by-design (M60LJNNslHU), 0
remaining**. Nothing is left on this plan; do not re-open it.

**Techniques worth keeping (each earned by a gap the last migration left):**

- A transform of a brace-group list literal — `Reflect({a,b,…}, ax)`, `Sequence(Rotate({a,b}, …))`
  — needed bikar #227's `lowerTransform` fix; every P5.1 construction hit it.
- Rebuild core+cli before probing an import: the checked-in `cli/dist` was stale and hid the
  `CircularArc` dispatch entry behind the generic "unsupported command" refusal.
- The `CircularArc/no-coords` refusal is by design — `arcIsMajor()` reads the CCW sweep from
  `cached_coords` to settle major-vs-minor and refuses rather than guesses (K1/K10).
- Real evaluated `cached_coords` via `import geogebra --emit-coords` (B′ self-bootstrap, D-080,
  [[option-evaluation-axes]]) is the sanctioned producer: bikar's own kernel evaluates the
  construction with the arcs dropped and reads back `{label:[x,y]}`. Never hand-edit the `.bkr`
  and never add a coords-free arc-direction guess.
- The printer must emit every construct `lower()` produces: `Printer.connect` covered only
  `mode:'arc'` while `lower()` had always emitted `connect points` for a drawn Segment, and the
  "arc-only subset" was documented and tested yet never true — it just was never exercised
  until a segment met lowerable arcs (#238, `bikar:docs/issues/2026-09-21-printer-connect-points-crash.md`).

**How to apply:** for any future construction import, branch off *current* bikar main (fetch
first, never stack — [[stacked-pr-stranding]]), regenerate the AST with `--cached-coords`,
confirm zero unlowered via `--coverage`, then fixture → base → coaster → goldens → O1/O2/O3 →
the 3d-models vendoring PR per [[pr-flow-for-all-repos]] (the pointer/ledger gate resolves the
`.bkr` at bikar's git ref — never `CONSTRUCTIONS_OK=1`). Related: [[islamic-orb-project]],
[[orb-repo-roles]], [[3d-models-use-case-hook]], [[decision-id-collision-recurred]].
