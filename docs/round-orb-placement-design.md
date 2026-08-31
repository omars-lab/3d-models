# Placing a round pattern on a sphere — design doc

Status: **v1 — Phase 0 + Phase 1 built and green in bikar (`packages/core`), witnesses
shipped as `bikar:patterns/Orbs/Donut-Hex-Orb.bkr` (one disc, watertight) and
`bikar:patterns/Orbs/Donut-Hex-Weld.bkr` (two adjacent discs, welded), both riding the
studio's generic solid-mesh preview and a Playwright browser proof
(`bikar:packages/e2e/tests/round-orb.spec.ts`).** The engine change is a new DSL statement
family — `base sphere` + `place rule` — and the plug for a socket the maclado work left
declared but never read.

Direction (AskUserQuestion, 2026-08-31): **prove the mechanism first**. v1 places ONE
hand-authored round `.bkr` on a sphere (watertight) and welds TWO adjacent copies so they
share a real welded vertex. The general rule-table (all sites per axis class), reproducing
the 20-wheel maclado field through this path, a second placement rule, and fillers between
discs are an explicit **follow-on**, not v1.

Surface (AskUserQuestion, 2026-08-31): **a new `base sphere` / `place rule` spelling**,
read as its own statement family — *not* a variant of `base wheelfield`. The maclado
`wheelfield` path and its dead `placeRule` socket are left byte-untouched; the new
`place rule` on `base sphere` is what finally gets read.

Scope: give the DSL a way to say "take *this* round `.bkr` disc — a rosette, a wheel, a
donut hexagon — and place it at chosen sites on a sphere, letting adjacent copies touch and
weld." Today the engine wraps a *polygon* pattern across every face of a Platonic solid
(`inscribe`, 23 patterns) or runs the kernel's own circular maclado wheel
(`base wheelfield`, 3 patterns). Neither lets a user place their own round pattern. This
adds that path for the two-rung mechanism proof; it does not add a filler solver or a rule
library.

Grounding. Every engine claim below was verified first-hand against the bikar working tree
this session — the placer's frame-based reuse, the coincidence weld, the per-cap watertight
gate, and the studio's dispatch on `orbMesh` without `orb3d`. Where a fact is a follow-on
gap rather than a shipped guarantee, this doc says so in place (§6 names the CLI mesh-gate
gap explicitly rather than implying `--check mesh` covers the sphere-orb path — it does not).

---

## 1. Goals and non-goals

**Goals.**

1. **Place one hand-authored round pattern on a sphere and close it watertight** — the disc
   arrives through the new `base sphere` DSL, its rim wall closes into a cap, and the cap
   passes the manifold gate. (Phase 0, `Donut-Hex-Orb.bkr`.)
2. **Weld two adjacent copies at a real shared vertex** — `sites 2` asks the rule for its
   adjacent pair, one shared `VertexPool` fuses their facing contacts, and a frozen vitest
   asserts the two contact points resolve to a *single* vertex index. (Phase 1,
   `Donut-Hex-Weld.bkr`.)
3. **Make the weld visible where a user reads it** — the studio solid-view overlay reports
   `N sites · N welds` alongside its existing `N tris · N cm³ · watertight`, and a Playwright
   spec asserts the pair paints and the overlay reads `2 sites · 1 weld`.
4. **Read the socket the maclado work left.** `place rule` is declared, typed, and stored
   today, and its only read in the whole repo was a round-trip test. This builds the plug —
   `decl.placeRule` is actually consumed in `evaluateSphereOrbDecl`.

**Non-goals (v1).**

- **A rule table.** The one `dodecahedral` rule returns a 1-site slice (Phase 0) or a
  2-adjacent-site slice (Phase 1) of the dodecahedron vertex set. Site sets per axis class,
  a second (icosahedral 5-fold) rule, and reproducing the full 20-wheel maclado field through
  this general path are the follow-on.
- **Fillers between discs.** Phase 1 proves the *weld* — a shared vertex — not a closed
  two-body manifold. The welded union of two caps is a deliberate non-manifold pinch at the
  shared tip; a closed shell with fillers is the follow-on (§5.3).
- **Unifying `MacladoWheel`.** The general contact-ring path runs *beside* the maclado
  wheel, not through it; the maclado tests and `Maclado-9*` outputs stay byte-identical.
- **The browser configurator.** The witnesses ride the studio's existing solid-mesh preview
  (the same one the Lego bricks use); no Orb Lab knob path is added for the round family.

---

## 2. The law any placement obeys — the divisor trick, restated for a user disc

A pattern with `Cₙ` rotational symmetry may be centred on a `k`-fold axis **iff `k | n`**.
This is the same theorem the maclado field rests on (`maclado-orb-design.md` §2): the
polyhedral rotation-axis orders are only {2, 3, 4, 5}, so a disc's *full* `Cₙ` is never
global, but a disc placed at a site of order `k` stays legal whenever its motif is invariant
under the site's rotations — it needs `C_k ⊂ Cₙ`, i.e. **`k` divides `n`**.

Dodecahedron vertices are **3-fold** axes (`k = 3`). A valid round disc for this rule needs
`n` divisible by 3. The v1 witness — a **donut hexagon**, a central hexagonal void ringed by
six trapezoids out to the boundary — has six outer contacts, so `Cₙ = C₆`, and `3 | 6` ✓. A
square disc (`C₄`) is refused at evaluation time, **naming both numbers**: `4 % 3 ≠ 0`. A
Fibonacci phyllotaxis disc has rotational order 1 and is explicitly not a candidate.

Where does `n` come from? **Derived from the contact ring's point count** — the disc declares
its outer contacts by class (§3, Q1), the placer counts them (`n` contacts ⇒ `Cₙ`), then
validates against the rule's `k` with `k | n`, erroring with both numbers named rather than
misplacing silently. Declared, never guessed (Tenet 23).

---

## 3. What the engine reuses, and the one thing it plugs in

Three of the four hard parts were already general and shipped before this work — verified by
grep and read this session, not assumed:

1. **The placer is already frame-based.** `placeWheelInFrame(wheel, frame, radius, unitMm)`
   (`bikar:packages/core/src/kernel3d/maclado-field.ts`) takes the wheel *as data* and an
   explicit orthonormal frame; its own docstring records that it was exported so a
   *search*-based caller could reuse it. Placement was decoupled from the dodecahedron once
   already.
2. **The weld is coincidence-based, not topology-based.** `VertexPool.intern`
   (`bikar:packages/core/src/kernel3d/weld.ts`) returns an existing index for any point within
   tolerance, searching the 27 neighbour cells. *Any construction that makes points coincide
   welds.* Placing two discs through one shared pool is the whole weld mechanism — nothing new.
3. **The 2D preview and the solidify tail come free.** The pattern's own bounded faces lift
   onto the spherical cap through the frame; the pierce/shell/manifold machinery in
   `solidify-lattice.ts` is the same path the `inscribe` orb already uses. The studio needs
   **zero new rendering code** — see §4.

**The one thing genuinely missing, and now built:** the `place rule` word was *declared,
typed, stored, and never read* — its only prior read in the whole repo was a round-trip test.
This work adds:

- **`SphereOrbNode`** (`bikar:packages/core/src/dsl/ast.ts`) — a separate AST node from the
  classic orb and the wheelfield orb, carrying `base sphere`, `radius`, `struts`, `inscribe`,
  `contact <class>`, `place rule <R>`, and `sites <n>`.
- **The parser path** (`bikar:packages/core/src/dsl/parser.ts`) — a `base sphere` branch, a
  `PLACEMENT_RULES` set validated the way `ORB_SOLIDS` already is (the allowed list read off
  the set so an error can't name the wrong one), and `parseOrbSites` refusing `sites > 2` at
  parse time (`orb sites is 1 or 2 in v1 … placing the full site set of a rule is follow-on`).
- **`kernel3d/placement-rule.ts`** (new) — a total `PLACEMENT_RULES` record shaped like
  `ORB_SOLID_BUILDERS`, so adding a rule forces a compile error until it has a builder. The
  one `dodecahedral` builder returns `siteCount` frames (a 1- or 2-site slice) built from the
  dodecahedron vertices, reusing the field's framing math.
- **`evaluateSphereOrbDecl`** (`bikar:packages/core/src/dsl/evaluator.ts`) — extracts the
  `contact`-classed boundary ring, runs the `k | n` check, calls the rule (**`decl.placeRule`
  is read here** — the whole point), places every frame through one shared `VertexPool`, and
  gates on watertightness. Returns `orbMesh` with **no** `orb3d`.

---

## 4. Why the studio needs no new rendering code

A `base sphere` orb returns `orbMesh` **without** an `orb3d` descriptor. That single fact
routes it, through `pickRenderPath` (`bikar:packages/web/src/solid-view.ts`), to the generic
`'solid-mesh'` path — the raw watertight-mesh preview the Lego bricks use — *not* the per-axis
orb-views tabs. It gets the `.orb-3d-canvas` and the solid-view bar (2D toggle) with zero new
UI code.

The only new UI is two measurements in the overlay. The `solidDetail` string
(`bikar:packages/web/src/solid-view.ts`) already read `<name> · 3D · N tris · X cm³ ·
watertight`; it now also reports `N site(s) · N weld(s)`, sourced from `orbMesh.stats`
(`siteCount`, `weldCount`, `capsWatertight` — all set by the placer). Singular/plural is
handled ("1 site" / "2 sites", "0 welds" / "1 weld"). The discipline is the one the
`solid-preview` spec pins: **measurements, never a verdict** — the overlay never prints
PASS / FAIL / "will hold", and the Playwright spec asserts it doesn't.

---

## 5. Watertightness — per cap, not aggregate

This is the one genuinely subtle result of the v1 build, and it is load-bearing.

### 5.1 A lone cap closes; the pair's union does not, on purpose

A single placed disc's rim wall closes it into a watertight cap — `watertight === true`,
reported plainly. Two welded discs are different. They share their fused contact's vertical
rim-wall edge: the directed edge `out0 → inn0` appears in **both** caps' rim walls (the
"doubled wall"). The aggregate `meshStats` edge-twin check therefore sees that directed edge
twice and reports `watertight === false`. **But each cap individually still closes.**

### 5.2 `capsWatertight` is the correct gate

So the placer computes `capsWatertight` (`bikar:packages/core/src/kernel3d/solidify-lattice.ts`)
— every cap's triangle-slice individually watertight, via a per-cap
`meshStats(vertices, triangles.slice(s, e)).watertight`. For a lone cap this equals aggregate
`watertight`; for a multi-site placement it is the right gate, because the aggregate's "false"
is an artifact of the deliberate shared-wall pinch, not a hole. The evaluator gates on
`capsWatertight ?? watertight`, and the studio overlay prints `watertight` from the same flag.
Verified empirically this session: the pair reports `watertight = false, capsWatertight = true`,
and both STLs emit real meshes (single 192 tris / 0.1 cm³, pair 384 tris / 0.3 cm³).

### 5.3 The union is a follow-on, not a v1 claim

The welded pair is a **non-manifold pinch** at the shared tip — the two rim walls meet at one
edge with no filler between them. A closed two-body shell (fillers between the discs) is the
explicit follow-on. v1 proves the *weld* (a shared vertex index — the frozen vitest in
`bikar:packages/core/tests/kernel3d/place-cap.test.ts` asserts `weldCount === 1`,
`capsWatertight === true`, aggregate `watertight === false`), not a printable union.

---

## 6. What v1 does not gate — the CLI mesh-gate gap, stated in the open

The evaluator's `capsWatertight` gate throws at *compile time*, so a sphere orb that fails to
close cannot be evaluated at all — the guarantee is real. But the **CLI** `--check mesh` gate
(`bikar:packages/cli/src/index.ts`) keys on `if (checkMode() !== 'none' && (result.orb3d ||
result.piece3d))`. A sphere orb has `orbMesh` but **no** `orb3d`/`piece3d`, so `--check mesh`
silently *skips* the sphere-orb path. This is an honest follow-on gap, not a Phase-1 blocker:
the watertight guarantee is enforced three ways over (the evaluator throw, the frozen vitest,
the Playwright overlay), but the CLI's dedicated mesh gate does not yet cover this path.
Closing it is a one-line predicate widen (`|| result.orbMesh`) plus the aggregate-vs-caps
decision about which watertight flag the CLI should report — filed as the follow-on's first
task, and worth a `bikar:docs/engine-issues.md` entry.

---

## 7. The witnesses

Two `.bkr` patterns, shipped as studio patterns (not fixtures) so the new path is debuggable
through the pick menu, the `?b=1` overlay, and `#slug:fN` highlight — none of which work on a
vitest fixture. Both share one blueprint and pattern (the donut hexagon); they differ only in
the orb block.

- **`Donut-Hex-Orb.bkr`** — Phase 0. One disc at one dodecahedron 3-fold vertex. Overlay reads
  `… · watertight · 1 site · 0 welds`.
- **`Donut-Hex-Weld.bkr`** — Phase 1. `sites 2` adds the adjacent pair. Overlay reads
  `watertight · 2 sites · 1 weld`.

Each owes, in the same commit, a `bikar:packages/web/public-surface.json`
`patternSources.count` bump (120 → 122) with a `why` paragraph — enforced by pre-commit —
stating the two sources publish only geometry (no secret) and that the weld witness is a
mechanism proof, not a printable part; and the manifest bijection
(`bikar:patterns/index.json`, `pattern-manifest.test.ts`).

The flat-disc ship-gate (Tenets 24/25) was cleared: expectation written first (a clean
hexagonal donut, no slivers), the disc rendered and the PNG Read, matched exactly.

---

## 8. Verification — what is green

- Full bikar suite green (4272 passed, 3 expected-fail); `make build` (core + web) green;
  manifest + surface tests green (23/23); both witnesses compile via the CLI and emit STLs.
- The load-bearing regression is the shared-vertex vitest
  (`bikar:packages/core/tests/kernel3d/place-cap.test.ts`, Tenet 18) — `weldCount === 1`,
  `capsWatertight === true`, aggregate `watertight === false`.
- The browser proof is `bikar:packages/e2e/tests/round-orb.spec.ts` (`make test-e2e`, Docker,
  per the standing directive — not Chrome DevTools MCP): Phase 0 asserts the disc paints
  (`.orb-3d-canvas` visible, `distinctPixels > 1`) and the overlay reads
  `… · watertight · 1 site · 0 welds`; Phase 1 asserts `watertight · 2 sites · 1 weld`. Both
  `not.toHaveText(/PASS|FAIL|will hold/i)`. **Both pass** (2 passed, 1.8s).
- DSL-level tests in `bikar:packages/core/tests/kernel3d/sphere-orb.test.ts` pin the parse and
  evaluate path: siteCount/weldCount, the `C₄` rejection naming `4 contacts … 3-fold … k | n`,
  the unknown-rule error, the missing-contact-class error, the `sites 20` refusal, and the
  route to `solid-mesh`.

---

## 9. Explicitly deferred to the follow-on (not v1)

Each is a named milestone gated behind v1 shipping:

1. **The full rule table** — site sets per axis class, so `sites` can ask for the whole set,
   not just 1 or 2.
2. **Reproduce the 20-wheel maclado field through this general path** — the strongest
   correctness test, because it has a fixture (`maclado-field.test.ts`); the general
   contact-ring path should reconstruct byte-identical geometry.
3. **A second placement rule** — the icosahedral 5-fold axes (`k = 5`), hosting `C₅`/`C₁₀`
   discs.
4. **Fillers** — a closed two-body (then N-body) shell between welded discs, turning the §5.3
   pinch into a printable union. The generic instruments for it (`decomposeWheelGap`,
   `checkFillerClosure`, currently unexported) are noted, not touched.
5. **The CLI mesh-gate widen** (§6) — cover the `orbMesh` path in `--check mesh`, decide the
   aggregate-vs-caps report, and add the engine-issue entry.
6. **Unify `MacladoWheel`** into the general contact-ring model (v1 runs parallel).
