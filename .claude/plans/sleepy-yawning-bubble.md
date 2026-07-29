# Lego Lab — plan

## Context

Orb Lab took one thing the engine could already do (`orb`) and gave it a public, knob-driven,
trust-instrumented surface: a vendored static page, sliders auto-generated from the `.bkr`
`param` block, a mesh gate that says out loud whether the thing will print, and a phase ladder
(M5 → P0 → P1 → P2) with an implementation-status log. That machinery is now the house pattern.

**Lego Lab applies it to a different question:** take a bikar pattern, break it into pieces, and
turn each piece into a **3D-printable LEGO-compatible part** — a body carrying the pattern relief,
with studs and/or anti-stud tubes on the LEGO 8 mm lattice so it clutches into real LEGO.

The interesting problem is not meshing — `solidifySlabStack`
(`bikar/packages/core/src/kernel3d/solidify-slabs.ts`) already builds watertight z-varying solids
from a shared 2D cell partition with zero booleans, which is exactly the shape a brick wants
(hollow walls low, solid ceiling, studs on top). The interesting problem is **commensurability**:
LEGO's lattice is square and offers 90° and 45°; Islamic patterns divide circles into 5, 8, 10, 12.
Eight-fold lands on the lattice, twelve-fold nearly does, five-fold never will at any scale.

The resolution — and the decision this plan is built on — is that a *printed* piece's outline does
not have to obey the grid. Only its **interface** does. So compatibility splits in two, and both
become measurable:

| | Question | Nature |
|---|---|---|
| **Anchorability** | Does this piece have enough body to host ≥2 legal clutch features with adequate wall? | Hard gate. Pass/fail. Satisfiable by every pattern family. |
| **Grid fit** | Is the pattern's repeat unit an integer stud count, so pieces butt together seamlessly? | Score 0..1. Tunable via scale / rotation offset / division count. Unreachable for 5-fold. |

That pairing is the direct analogue of the existing mesh gate + qiyas trust badge, and it is what
makes the `✅ verified / 🔬 needs sweep / ✖ rejected` compatibility matrix fillable.

### Decisions locked (Omar, 2026-07-29)

1. **Output is 3D-printed LEGO-compatible parts** — STL, not a BrickLink shopping list. Stock-part
   mosaic generation is explicitly out of scope.
2. **Both gates**: anchorability is hard pass/fail; grid fit is a score with tuning knobs and a
   scale sweep.
3. **Interface is a per-piece DSL option** — one declaration emits tile-style (smooth/relief top,
   tubes below), full-brick (studs + tubes), or edge-stud variants.
4. **True LEGO scale** — 8 mm pitch, real interoperability with LEGO the user already owns. The
   printer's actual floor is settled by a clutch-fit coupon before any part is designed.
5. **Full `/ground-design-doc` ceremony** — survey + adversarial audit + Appendix A/B, same bar as
   w2/c2.

---

## Deliverable 0 — Research and design doc (do this first)

This phase produces no code. It is the gate on everything below, and several load-bearing numbers
below are *provisional* until it runs.

**`docs/research/lego-brick-system-survey.md`** — the field survey. Must establish, each with a
primary source read in full:

- The dimensional standard: pitch, stud ⌀ and height, plate/brick height, wall and ceiling
  thickness, the `studs × 8 − 0.2 mm` footprint rule, **and the interior tube geometry** (outer ⌀,
  inner ⌀, and the wall between tube and outer shell).
- **The 1×N exception.** One-stud-wide bricks physically cannot host a tube; LEGO uses inner-wall
  ribs/rails instead. If true, the anchor solver must branch on footprint width, and this is the
  single most likely source of a wrong first design.
- FDM reality at 0.4 mm nozzle: what stud and tube diameters actually clutch, what XY compensation
  is needed, orientation, layer height. Counter-evidence to seek: sources arguing true scale is
  *not* achievable at 0.4 mm and requires 0.2 mm.
- Clutch power as a physical mechanism — interference fit, contact area, material creep, and how
  PLA vs PETG behave over repeated cycles. (Note the existing house rule that aged PLA embrittles
  on flex — `docs/w2-connector-design.md`.)
- LDraw as an interchange/preview format: LDU ↔ mm, type-1 part lines, `ldconfig.ldr` colors.
- Prior art on pattern→grid legalization worth borrowing or explicitly avoiding: *Legolization*
  (SIGGRAPH Asia 2015) for the stability metric and refinement loop; brickmos/brickr for the
  quantize-and-merge shape; the LEGO advanced-technique literature (half-stud offset via jumper
  plates, cheese slopes, Pythagorean-triple angle escapes) for what "escaping the grid" costs.

**`docs/lego-lab-design.md`** — house structure, §1–§12 + Appendix A/B, mirroring
`docs/w2-connector-design.md`:

```
## 1. Goals (+ explicit Non-goals v1)
## 2. Engine ground truth        — what bikar can do today, cited file:line at a pinned commit,
                                   ⚠ on anything that contradicts this plan
## 3. What the survey established (the load-bearing facts)
## 4. Language design            — the `brick` declaration (§ below)
## 5. Grid registration and the anchor solver
## 6. Validators (compile-time; house error style)
## 7. Kernel: the brick cell partition over solidifySlabStack
## 8. Coupons and the prototype catalog (the LG ladder)
## 9. Lego Lab — the page
## 10. Phasing (+ Implementation status log)
## 11. Open questions
## Appendix A — survey sources
## Appendix B — counter-evidence and divergences
```

Then run `/ground-design-doc docs/lego-lab-design.md`, preserving the audit verbatim at
`docs/research/lego-lab-grounding-audit.md` and driving v1 → v2.

**Load-bearing claims the audit must attack.** Every dimensional number in this plan is
provisional: pitch 8.0, stud ⌀4.8 × 1.6 h, plate 3.2, brick 9.6, wall/ceiling 1.6,
footprint `8n − 0.2`, tube ⌀6.51/4.8, 1 LDU = 0.4 mm. Sources already disagree on stud diameter
(4.8 vs 5.0) and the tube figure is the least verified of the set. Also contested: whether true
scale prints on a 0.4 mm nozzle at all, and whether the 1×N rail exception is real.

---

## The engine work (in `bikar`)

### The `brick` declaration

A new solid declaration, sibling to `tile` / `clip`, because footprint-in-studs is a semantic
`tile … outline square 100` cannot express. Grammar lands in
`bikar/docs/language-reference.md` beside the tile/wall grammar (~L540-697):

```
brick StarTile
  inscribe star_pattern            # existing pattern reference, same as tile
  footprint 4 x 4                  # in studs; `auto` fits the pattern's bbox
  height 1 plate | 1 brick | $n plates
  studs none | full | edge         # decision 3 — the per-piece interface option
  tubes auto | none                # `auto` = solver picks tubes or rails per footprint
  relief depth $d                  # pattern relief into the top face
  origin centered | at (col,row)   # lattice registration
```

`studs none` + `tubes auto` is the tile-style default. `studs full` + `tubes auto` is a stackable
brick. Validators in the house error style reject: footprint smaller than the pattern needs,
`studs full` combined with a relief depth that would bury the studs, heights that are not integer
plate multiples, and `tubes none` on a piece the anchor gate then fails.

### `kernel3d/brick.ts` — the cell partition

Builds the `Slab[]` stack for `solidifySlabStack`. The z-layering is naturally three slabs and maps
onto the existing contract cleanly:

| Slab | z range | Cells solid |
|---|---|---|
| body | `0 → h − ceiling` | outer wall ring, tube annuli (or inner rails on 1×N) |
| ceiling | `h − ceiling → h` | full footprint, minus the relief pockets |
| studs | `h → h + 1.6` | one disc cell per stud position |

Two invariants from `solidify-slabs.ts:26-31` are the hard part and must be honoured explicitly:
**cell identity is by object reference** across slabs, and **shared boundaries between neighbouring
cells must reuse the same discretized polyline** — so the design needs a ring cache for every
circle it discretizes (stud discs, tube annuli, relief arcs), the same pattern C1 established.
Get this wrong and the mesh is silently non-watertight.

Reuse rather than re-derive: `circlePoints`, `normalizeRing`, `pointInPolygon`, `minDistToRing`,
`WELD_TOLERANCE` are already exported from `kernel3d/solidify-piece.ts`. Pattern outlines come from
`unionPatternFaces` (`dsl/evaluator.ts:956`), which already turns a pattern's bounded faces into one
simply-connected extrudable ring by exact directed-edge cancellation.

### `kernel3d/grid-gate.ts` — the two gates

```ts
gridGate(brick: BrickSolid, opts) → GridGateReport {
  passed: boolean
  anchors: { count, kinds: ('tube'|'rail'|'stud')[], positions: GridCell[] }
  minTubeWallMm: number
  rotationLocked: boolean          // ≥2 non-coincident anchors
  gridFit: number                  // 0..1
  snapResidualMaxMm: number
  repeatUnitStuds: number | null   // null when incommensurable
  findings: GridFinding[]
}
```

Modelled directly on `meshGate` (`kernel3d/mesh-gate.ts`, 99 lines) and `printGate`
(`print-gate.ts`, with its `PrintFinding` code vocabulary). Anchorability is the `passed` boolean;
everything else is readout. A companion `sweepGridFit(source, param, range)` returns fit-vs-value
so the Lab can surface sweet spots — this is the mechanism that fills the compatibility matrix,
exactly as the Orb Lab calibration sweeps flipped 🔬 cells to ✅.

### `kernel3d/fit-profile.ts` — extend, don't fork

Add LEGO clutch entries beside the existing `press/snug/sliding/free` ladder and the
`pla_calibrated` / `petg_calibrated` printer profiles. Authored dimensions stay the contract; the
profile widens bores at emit time. The coupon ladder produces the numbers.

### Protocol gap to close

`packages/lab/src/evaluate.ts:202` (`previewResponse`) returns `null` for a bare `piece`/`tile`/
`clip` — "This script declares no orb or wall" — and `LabResponse.family` is
`'lattice' | 'weave' | 'wall'`. Lego Lab needs `'brick'`. Extend the union in
`packages/lab/src/protocol.ts` rather than forking the protocol, since Lego Lab's worker is a copy
of the same shape.

---

## The Lab (`bikar/packages/lego-lab`)

A copy of `packages/lab`'s structure — it is a template, not a framework: hand-written HTML, plain
DOM, module-scope state, one `style.css`, zero UI dependencies. Same 12-file layout
(`main.ts` / `worker.ts` / `evaluate.ts` / `worker-host.ts` / `protocol.ts` / `viewer.ts` /
`editor.ts` / `scripts.ts` / `url-state.ts` / `custom-state.ts`).

**Reuse verbatim from `@naqshcoffee/bikar-knobs`** — `renderKnobPanel`, `syncKnobPanel`,
`applyConstraints`, `clampToSpecs`, `MACHINES`/`loadPrintTarget`, `encodeBkr`/`decodeBkr`. Any new
cross-param rules (e.g. relief depth vs ceiling thickness) go in `knobs/src/constraints.ts` beside
the two orb rules, per the ADR that put the knob layer in its own workspace package.

**Reuse `viewer.ts`** — the Canvas-2D painter takes a mesh; a brick is a mesh. No three.js. One
addition: a **lattice overlay** in the top-down view drawing the 8 mm grid under the piece with
anchor positions marked, so the anchor solve is visible rather than asserted.

**New surface unique to this Lab:**
- A **grid-gate panel** beside the mesh-gate panel: PASS/FAIL, anchor count and kinds, min tube
  wall, rotation-lock ✓, then grid-fit score, snap residual, repeat unit.
- A **scale-sweep strip** — fit plotted against the swept param, sweet spots clickable to set the
  knob. This is the concrete answer to "can we play with settings to make a pattern compatible?"
- **Multi-part export** when a pattern decomposes into several pieces — the CLI already has
  `--format parts`; the page needs the equivalent zip/sequential download.

URL schema, debounce timings, stale-while-revalidate, worker watchdog, size guard, and the
preset↔custom byte-comparison all carry over unchanged from `packages/lab`.

---

## Physical validation — the LG coupon ladder

Added to `.claude/skills/prototype/catalog.md` in the skill's entry schema (Status / Model with the
exact reproducing CLI command / Print target / What we want to learn / What we learned / Iteration
log / Feeds). Ordered cheapest-decisive-learning-first, per the ladder rule. **LG-F1 must print
before any brick geometry is finalized** — it is the exact analogue of W-F1 blocking W-C1.

- **LG-F1 — clutch coupon (tube side).** One 2×4 tile with a five-rung tube-⌀ ladder, mated against
  a real LEGO plate. Answers: does it clutch, does it hold, what offset does this printer need.
  Feeds → `fit-profile.ts` LEGO entries.
- **LG-F2 — clutch coupon (stud side).** A plate with a stud-⌀ ladder, tested against a real LEGO
  brick's underside. Answers whether `studs full` is viable at 0.4 mm at all, or whether it needs a
  0.2 mm nozzle — which would make tile-style the only shippable interface on this machine.
- **LG-R1 — 1×N rail coupon.** Settles the survey's rail-vs-tube exception in plastic.
- **LG-B1 — first patterned brick.** A 4×4 eight-fold tile at defaults. The first thing that is
  both a real LEGO part and a real Islamic pattern.
- **LG-B2 — off-grid anchor.** A five-fold rosette piece anchored by two tubes. Tests that
  rotation lock holds when the outline is incommensurable with the lattice — the load-bearing bet
  of the whole anchor-only approach.

Catalog rules apply: every entry needs ≥1 question answerable by measuring the object; nothing is
marked answered from a slicer preview; a failed print is a logged result.

---

## Publishing (in `3d-models`)

Mirrors `make lab` exactly (`Makefile:82-106`):

- `make lego-lab` — `cd $(BIKAR_DIR)/packages/lego-lab && npx vite build`, copy `dist/lego-lab.html`
  → `./lego-lab.html`, `dist/assets` → merged into `./assets`.
- `make lego-lab-smoke` — the vendoring integrity check: page exists, every `assets/` reference
  resolves, the worker chunk referenced by the main JS chunk exists.
- Add outputs to `DEPLOY_PATHS` (`Makefile:32`), to `clean` (`Makefile:135`), wire into `deploy`
  (`Makefile:160`) and `experiences` (`Makefile:124`).
- `index.html`: a `§ 03 The Bricks` section and a `BRICKS` data array beside `MODELS` (L322) and
  `ORBS` (L360), each entry carrying `lab:"lego-lab.html?v=1&f=<id>"`. Bump `ASSET_VER` (L320).
- **`.claude/skills/maintain-use-cases/use-cases.md`** — a new UC node in the Mermaid diagram *and*
  a matching table row, in the same commit that ships the capability, then
  `validate.py --refresh`. The pre-commit hook (`.githooks/pre-commit.d/20-use-cases`) will block
  the commit otherwise, since this work touches `index.html`, `Makefile`, and `src/`.
- **`bikar/docs/decisions/2026-XX-XX-lego-brick-declaration.md`** — ADR in the two-layer frontmatter
  format with `## 0. Premise check (MANDATORY)` and its empirical table; add the tag to
  `docs/decisions/tags.yaml`; `npm run ledger`.

---

## Phasing

| Phase | Where | Contents |
|---|---|---|
| **R0** | 3d-models | Survey → design doc v1 → `/ground-design-doc` → v2. **Blocks everything.** |
| **LG-F1/F2** | physical | Clutch coupons. Print before finalizing brick geometry. Blocks M6's dimensions. |
| **M6** | bikar | `brick` declaration (parser, AST, evaluator, `brick3d` provenance), `kernel3d/brick.ts` cell partition, LEGO fit-profile entries, language-reference + ADR. |
| **M7** | bikar | Anchor solver (tubes vs rails, rotation lock), `grid-gate.ts`, `sweepGridFit`, `LabResponse.family` gains `'brick'`. |
| **P0** | both | Lego Lab core: page, preset chips, knobs, viewer + lattice overlay, both gate panels, STL download, `make lego-lab` vendoring, gallery section. First shippable. |
| **P1** | both | Breadth: pattern-family × grid compatibility matrix filled by scale sweeps, the sweep strip UI, multi-piece decomposition + `--format parts` export, more curated `brick` scripts. |
| **P2** | both | Custom mode: code drawer, lz-string `code=` share links, Open in Studio, localStorage draft. |
| **P3** | both | Polish: per-family print notes, adjusted-parameter toasts, LDraw `.ldr` placement export for previewing an assembled set. |

Each phase ends with the standard verification bar (below) and an entry in the design doc's
`### Implementation status` subsection carrying commit hashes in **both** repos, deliberate
deviations from the spec called out, and additions beyond it noted.

---

## Critical files

**New (bikar):** `packages/core/src/kernel3d/brick.ts`, `grid-gate.ts`;
`packages/lego-lab/**` (12 source files + `vite.config.ts` + tests);
`patterns/Bricks/*.bkr` (the curated preset corpus);
`patterns/Coupons/Lego-Clutch-Coupon.bkr`.

**Modified (bikar):** `packages/core/src/dsl/{ast,parser,evaluator}.ts` (the `brick` declaration and
its registry entry in `evaluateFile`, `dsl/evaluator.ts:630-683`);
`packages/core/src/kernel3d/{index.ts,fit-profile.ts}`;
`packages/knobs/src/constraints.ts`; `packages/lab/src/protocol.ts`;
root `package.json` (workspaces, `typecheck`, `import-graph`);
`packages/e2e/playwright.config.ts` (a third `webServer` on a fresh strict port);
`docs/language-reference.md`; `docs/decisions/`.

**New (3d-models):** `docs/lego-lab-design.md`,
`docs/research/lego-brick-system-survey.md`, `docs/research/lego-lab-grounding-audit.md`.

**Modified (3d-models):** `Makefile` (targets, `DEPLOY_PATHS`, `clean`, `deploy`, `experiences`),
`index.html` (§03 + `BRICKS` array + `ASSET_VER`),
`.claude/skills/prototype/catalog.md` (LG ladder),
`.claude/skills/maintain-use-cases/use-cases.md` (UC node + row).

---

## Verification

**Per engine phase (bikar):**
- `npm test` (vitest) — new unit tests under `packages/core/tests/kernel3d/` mirroring the existing
  split: `brick-parse` + `brick-e2e`, plus `grid-gate.test.ts` as a gate unit test in the style of
  `mesh-gate.test.ts` / `print-gate.test.ts`.
- Watertightness is not asserted by eye: every generated brick must pass `meshGate` with
  `watertight: true` and `euler` consistent — the cell-partition invariants fail silently otherwise,
  so this is the real regression test for `brick.ts`.
- `npm run ci` (lint, format:check, build, test, spelling, madge --circular).
- `npm run check:decisions` for the ADR.
- Golden STLs for every committed `patterns/Bricks/*.bkr` at declared defaults, byte-checked so
  later phases cannot silently move geometry — the same discipline M5 used for the orbs.

**Per Lab phase:**
- Playwright specs under `packages/e2e/tests/lego-lab.spec.ts`, using the existing test hooks
  (`data-` attributes on the gate panel, `?budgetMs=` for the watchdog).
- `make lego-lab && make lego-lab-smoke` — the vendoring check must pass before deploy.
- `make site` (port 8613) and drive the page by hand: preset load, knob drag, gate flip, scale
  sweep, STL download, URL round-trip, unknown-`f` fallback. **The module worker will not load over
  `file://`** — `make open` is not sufficient.
- `make validate-use-cases` green with `as_of` at HEAD.

**Physical (the only verification that counts for fit):**
- Print LG-F1, measure, and record in the catalog's iteration log. A coupon question is never
  closed from a slicer preview. The clutch numbers that come out of it are what
  `fit-profile.ts` ships — not the survey's.
