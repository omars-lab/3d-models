> **Continuation (2026-09-17):** the coaster work and every open task now live in
> [`coaster-border-continuation.md`](coaster-border-continuation.md), which is self-contained.
> This file stays as the architecture, decisions (D-A…D-I) and phase map of record; Phases 0–3
> are shipped, Phase 4–5 items are restated there with current file anchors.

# Plan: GeoGebra constructions → naqsh (bikar) → STL coasters, repeatably

## Context

`~/Workspace/git/youtube` reconstructs Islamic-geometry tutorials as GeoGebra constructions
(`reconstructions/<id>/construction.ggb-commands`, rendered and scored into the iCloud data dir
`…/CloudDesktop/data/youtube/<id>/reconstruction/`). Nine exist today, the corpus ladder keeps
adding them, and nothing downstream consumes the geometry. The user wants every construction to
become a physical object — a coaster first — via **naqsh**, the name we use for bikar's `.bkr`
language (decision: bikar keeps its name, naqsh is a synonym; "make a naqsh file" produces a
`.bkr`), showcased in this repo's catalog and printed many at a time on the X2D, starting with
mini versions and iterating fast, with the process repeatable for every new construction.

Grounded facts that shape the design (file pointers in §9):

- The `.ggb` files are **recipes, not coordinates**: `ggb_build.py` writes `geogebra.xml` with a
  `<command>` block per dependent object and `<coords>` only for free points. A coordinate-level
  import is a dead end; a **construction-level** transpile is the only faithful path. A `.ggb`
  saved by GeoGebra itself has the same `<command>` blocks (plus cached coords), so a front-end
  that reads `geogebra.xml` works for **any GeoGebra file**, not only ours.
- `ggb_build.parse()` already **fails closed** (`die()` on any unrecognised line) and already
  holds the full parsed construction (views, statements, hides, styles, exports) after
  `expand()`. A JSON AST is a projection of that structure, not a new parser.
- Corpus census (9 reconstructions + 9 technique snippets): Reflect 152, Intersect 84, Rotate 82,
  Polygon 42, Line 41, PerpendicularBisector 20, Circle 20, Sequence 18, Midpoint 13,
  PerpendicularLine 12, Segment 7, AngleBisector 6, CircularArc 3, Vector/Translate 2, Parabola 2,
  ClosestPoint 2, Center 2, Hyperbola 1, Centroid 1. Free-point literals are only `A=(0,0)`,
  `B=(1,0)`, `D=(0,1)` plus the lattice snippet's `C=(0.5,0.5)`/`uE=(2,0)`.
- naqsh is **already a relative construction language** with a normative EBNF
  (`bikar/docs/grammar.md`) held to the parser by gates G1 (corpus sweep), G2 (keyword snapshot,
  130 words), G3 (every ```bkr block parses, §12 coverage table). It has no first-class named
  points (`PointRef = IDENT "." PointId`), no single-object `Rotate/Reflect/Translate` (only the
  N-fold replication blocks `rotate N around` / `mirror around`), no angle bisector (`bisector`
  is the perpendicular bisector), no parallel/perpendicular line, no midpoint/centroid points.
- naqsh extrudes 2D art to STL today (`piece … extrude <pattern> depth`); `tile` is square-only
  and its `inscribe` is 2D art; `brick`/`mural` own the relief kernel; orbs own struts.
- Highlighting already drifts: `packages/web/src/main.ts` keeps its own `KEYWORDS` set apart
  from `tokens.ts`; the lab editor is a bare textarea by rule (no CodeMirror/Monaco).
- `lark`, `pydantic`, `jsonschema` are not in the `youtube` conda env (deps are `PIP_PKGS` in
  its Makefile). OpenSCAD imports SVG only as closed polygons and verifies nothing: it stays
  with the cookie cutters, out of this pipeline.
- Printing is owner-gated (21 CAL bets, 0 measured). **Mini coasters ride Plate 1 or the plate
  right after**; nothing here dispatches a print. X2D bed 256 × 256 mm (D-053). Bambu Studio CLI
  accepts multiple inputs, `--arrange 1`, `--scale`, `--export-3mf`; `tools/bambu slice plate`
  wraps one model today.
- The shared checkout keeps switching branches under another session. **All implementation
  happens in a dedicated worktree per repo**, one PR per slice, never on the shared checkout.

## Decisions made in this session (→ `docs/decisions-log.md` D-055…, next free id at merge)

| # | Decision | Why |
|---|---|---|
| D-A | naqsh is a synonym for the bikar DSL; extension stays `.bkr`; "new naqsh file" ⇒ `.bkr`; docs say "naqsh (the language) — bikar (the engine)". No package renames. | Omar, 2026-09-16. Zero cascade across 357 files. |
| D-B | Import is construction-level and **one parser per language**: any `geogebra.xml` is lowered to `.ggb-commands` text, the existing `ggb_build.parse()` projects a JSON AST, `bikar import geogebra` lowers that to naqsh next to the evaluator that defines the target forms. | Coordinates are not in the files; a frozen import verifies nothing; a second parser of either grammar cannot be a source of truth. |
| D-C | Unsupported input fails **loud and enumerated**: unknown command, free point off the root frame, ambiguous intersect. Coverage is a printed table, never a silent drop. | "Any GeoGebra code" is a claim about a set (K2); the tool must print the set. |
| D-D | Dynamic STLs are re-rendered from `--param`, never mesh-scaled; mesh `--scale` exists only as a flagged escape hatch. | Scaling a mesh scales walls and relief below the FDM floor. |
| D-E | Minis ride Plate 1 or the next plate; no coaster dispatch before one honest measurement. | Omar, 2026-09-16. |
| D-F | Grammar is the source of truth for both languages: EBNF checked in and gated G1/G2/G3-style; highlighters and cookbook are generated from / tested against the same fixtures. | A grammar that can drift from its parser is worse than none. |
| D-G | GeoGebra free points are **root-circle aliases** (`A` = centre, `B`/`D` = 0°/90° division points); a free point off that frame is a transpile error ("rewrite relative to A, B"). Free numbers become `param`s. | Preserves the relative-construction tenet with **no new literal-carrying syntax**. Covers 9/9 reconstructions. A `frame` block for arbitrary free points is deferred to a `dsl-design` decision in slice 3, only if a real file needs it. |
| D-H | "GeoGebra ≡ naqsh" is **three claims with three oracles**: per-label geometry (GgbAPI coordinate dump vs naqsh evaluation), what is drawn (edge-SSIM vs the hero export), what is solid (GeoGebra coords → OpenSCAD extrusion → STL, compared to the naqsh STL by footprint IoU + Hausdorff). None implies the others; the mesh oracle runs at the flat extruded-pattern stage, before rim/bevel/relief exist. | An aggregate score cannot discharge a per-object claim; a reference STL that shares bikar's kernel proves nothing, so the reference extruder is OpenSCAD (independent, already installed). |
| D-I | A coaster is a **height field over an outline**: flat bottom, top `z = base + relief(x,y) + rim(r)`, stitched side wall. Straps, face emboss/deboss and the rim chamfer/fillet are all height contributions. Cut-through is a trivet mode, not a coaster. | Manifold by construction with no boolean union (bikar has none); bevel and relief become one kernel; every printability check is a query on the same field. |

## Architecture

```
youtube repo                                         bikar repo                              3d-models repo
──────────────                                       ──────────────                          ──────────────
any geogebra.xml/.ggb ─ggb_from_xml.py─▶ .ggb-commands
construction.ggb-commands ──────────────▶ ggb_build.py --ast-json ─▶ construction.json (Pydantic schema, mirrored byte-identical)
                                                                            │
                                                     bikar import geogebra ─┴─▶ lower.ts → printer.ts → patterns/Constructions/<id>.bkr
                                                     (header + provenance, mangling table, coverage report; fails closed)
                                                            │
                                                     bikar render --format views ⇄ edge-SSIM vs export.png (oracle 1, ggb_score.py)
                                                     bikar render … --check       ⇄ named points vs cached <coords> (oracle 2, per label)
                                                            │
                                                     piece Coaster extrude … (slice 1)   coaster <Name> disc relief (slice 2)
                                                            └──────────────▶ STL ──▶ make coasters ──▶ src/Coasters/, catalog, gallery
                                                                                                          │
                                                                                 tools/bambu slice compose plate.yaml ──▶ X2D .3mf
                                                                                 (re-render per --param, arrange on 256×256)
```

## Equivalence: three oracles (D-H)

| Oracle | Claim it discharges | Reference side | naqsh side | Compare | Runs |
|---|---|---|---|---|---|
| O1 geometry | every named object has the same geometry | `ggb_coords.py`: Playwright + GeoGebra Apps API (`setBase64`, `getAllObjectNames`, `getXcoord/getYcoord`, `getValue`, `getCommandString`) → `coords.json` for **any** `.ggb` | `bikar render --format parts`/evaluator dump of named points, lines, circles | per label after fitting the frame (scale `$unit`, origin `A`), tolerance in GeoGebra units; a missing or extra label is a FAIL | per commit (fast, numeric) |
| O2 drawing | the same objects are visible in the final state | hero `export.png` (already produced by the reconstruct loop) | `bikar render --format views` | edge-SSIM via `ggb_score.py --align --mask-ref` at the loop's own accept threshold (read from the script in P0.1) | per construction |
| O3 solid | the same region is solid in the printed piece | `coords.json` exported polygons → generated `.scad` (`polygon(points)` + `linear_extrude`) → OpenSCAD → `reference.stl`; **no bikar code** | `piece Coaster extrude … depth` → STL | `qiyas mesh compare`: footprint IoU at mid-height, symmetric Hausdorff, volume ratio; `--check` on both | per coaster, before the catalog entry |

O3 compares the **flat extruded pattern**; the finished coaster (rim, bevel, relief) has no
GeoGebra reference, so its added features are validated by the mesh gate, the structural
validators in P1.6 and the `CAL-CST-*` bets. GeoGebra's 3D view has a "download as STL"; whether
the Apps API exposes it headlessly is **unverified** (P0.1 checks), and the plan does not depend
on it. An aggregate score never discharges a per-object claim, so O1 is per label and O3 reports
the worst local deviation, not only the IoU.

## Options and the grading rubric

Rubric questions (0/1/2 each; recorded verbatim in the design doc so the reasoning is inherited):

- **R1 Generality:** any GeoGebra file, or only our `.ggb-commands`?
- **R2 One parser per language:** is any grammar known in two places?
- **R3 Fidelity:** does the output stay a relative, re-renderable construction, or freeze?
- **R4 What it verifies:** render-diff, coordinate oracle, mesh gate — or nothing?
- **R5 Failure honesty:** are unsupported inputs enumerated loudly?
- **R6 Cost:** to the first coaster / to the Nth construction.
- **R7 Gate fit:** rides G1–G3, catalog, docs, use-cases, counts?
- **R8 Readability:** would a person author the resulting file?

| Import path | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| A. GeoGebra `--export=svg` → OpenSCAD `import()` → STL | 2 | 2 | 0 | 0 | 0 | 2/1 | 0 | 0 | Rejected: frozen, closed polygons only, verifies nothing. |
| B. XML → `.ggb-commands` → JSON AST → `bikar import geogebra` | 2 | 2 | 2 | 2 | 2 | 1/2 | 2 | 2 | **Chosen.** |
| C. Python emits `.bkr` text in youtube | 1 | 0 | 2 | 1 | 1 | 2/1 | 1 | 1 | Rejected: naqsh syntax encoded in the repo that does not own the grammar; no evaluator to check semantics. |
| D. TypeScript re-parser of `.ggb-commands` in bikar | 0 | 0 | 2 | 2 | 1 | 1/1 | 1 | 2 | Rejected: second parser of one grammar. |
| E. Headless GgbAPI coordinate dump → `polygon` literals | 2 | 2 | 0 | 1 | 1 | 1/1 | 0 | 0 | Rejected as the path; **kept as oracle 2's fallback** for files without cached coords. |

Parser tooling for `.ggb-commands`: **keep the hand-rolled parser + an EBNF doc with a G3-style
conformance test** (bikar's own option (b)). Lark rejected: not in the env, the grammar is
line-regular except one nested form the parser already special-cases, and a Lark grammar beside
the parser is a second source of truth while replacing the parser is the big-bang rewrite
3d-models already rejected for naqsh. Ohm/Peggy/Chevrotain surveyed for bikar and rejected for
the same reason.

| Plate composer | Verdict |
|---|---|
| P1. Manifest → bikar re-render per variant → Bambu Studio CLI multi-input `--arrange 1 --export-3mf` | **Chosen.** Reuses the wrapped CLI; the manifest is the reviewable artifact. |
| P2. Own 2D packer writing a 3MF | Deferred; only if P1's arrange proves unreliable (`docs/issues/` note if so). |
| P3. Manual GUI arrangement | Rejected: verifies nothing, not repeatable. |

## Phases and tasks (with dependencies)

Ids are `P<phase>.<n>`; `deps:` = merged first. Each task is a PR in the named repo, in a
worktree. Every task that adds a number ships the test or doc marker that fails before and passes
after (graduation rule). Tier-0 witnesses (`patterns/witness/*.bkr`) precede any composite golden.

### Phase 0 — Ground and decide (docs only) — 1 session

- **P0.1** `3d-models/docs/research/geogebra-construction-import-survey.md` — research preserved
  verbatim under the provenance header (produced / produced-by / feeds / scope): GeoGebra XML
  format and command recompute, `--export` formats, GgbAPI route, Bambu Studio CLI, X2D bed,
  parser toolkits and why hand-rolled + conformance wins, OpenSCAD SVG-import limits, the corpus
  census above, the youtube loop's edge-SSIM accept threshold (read from `ggb_score.py`, not
  assumed). Links in §9. deps: none.
- **P0.2** `3d-models/docs/geogebra-construction-import-design.md` — umbrella design: the
  architecture, rubric and option tables, AST contract summary, ledger, skill. Markers: every
  `**Default:**` cites P0.1 or a `CAL-*` id; every `**Validator:**` has `PASS:`/`FAIL:`. deps: P0.1.
- **P0.3** `docs/decisions-log.md` D-A…D-G (renumber at merge; `decision-id-collision`). deps: P0.2.
- **P0.4 bikar** `docs/decisions/2026-09-<dd>-naqsh-language-name.md`; `grammar.md` /
  `language-reference.md` / README titles "naqsh (the language) — bikar (the engine)";
  `bikar-dsl` skill line. Memory `naqsh-is-bikar-dsl-synonym` (feedback). deps: none.
- **P0.5** Worktrees: `git worktree add ../3d-models-constructions feat/constructions-import`,
  `../bikar-constructions`, `../youtube-constructions` (youtube commits on `main` per its
  CLAUDE.md; commit only when asked). deps: none.

### Phase 1 — Languages made robust (grammar as source of truth)

- **P1.1 youtube: EBNF for `.ggb-commands`.** `youtube/docs/grammar.md` in bikar's notation: §1
  notation, §2 lexical (`LABEL`, `NUM` with `°`, comment rule incl. the `=#rrggbb` carve-out),
  §3 file, §4 statements (`PointLit`, `NumberDecl`, `Command`, `MultiOut`), §5 one production per
  directive, §6 slider-expression subset, §7 the nested `Sequence` form, §8 coverage table
  generated from `_CMD_TYPE ∪ _POLYMORPHIC` + directives. Gates: `scripts/test_ggb_grammar.py`
  (G3 twin: every ```ggb fence in grammar/README/CLAUDE/cookbook parses via `expand()+parse()`,
  every ```ggb invalid fence dies; §8 == dispatch keys both ways); G2 twin
  `scripts/fixtures/ggb-vocabulary.txt` written by `ggb_build.py --dump-vocabulary`. The existing
  identity test is the G1 twin. No parser rewrite. deps: P0.5.
- **P1.2 youtube: `scripts/ggb_from_xml.py`** — any `.ggb`/`geogebra.xml` → `.ggb-commands`
  text: `<element type=point><coords>` (free) → `A = (x, y)`; `<expression label exp>` →
  `G = 0.3333`; `<command name><input><output>` → `out = Cmd(a0, a1, …)` (multi-output →
  `{E, F} = …`); `<show object="false">` → `@hide`; `<command name="Sequence">` kept nested.
  Anything else (conics, text, scripting, `<expression>` with functions) is **listed** in a
  `--coverage` report and aborts unless `--lenient` drops it explicitly. Fixtures: our 9 renders
  (round-trip must re-parse to the same AST as the hand-written file) + 3–5 public geogebra.org
  materials with provenance recorded. deps: P1.1.
- **P1.2b youtube: `scripts/ggb_coords.py` (oracle O1 + O3 reference)** — Playwright drives
  the GeoGebra web app offline-cached (or the desktop Classic 5 via the same API if reachable),
  loads any `.ggb` with `setBase64`, dumps every object's type, coords/equation, visibility and
  `getCommandString` into `coords.json`; `--scad` also writes `reference.scad` (one
  `polygon(points)` + `linear_extrude(depth)` per exported polygon, unioned) and runs
  `openscad -o reference.stl`. Test: on our 9 renders the free points equal the file's
  `<coords>` and every command string round-trips through `parse()`. Playwright/browsers
  added to `PIP_PKGS` if absent (checked at P0.5). deps: P0.5.
- **P1.3 youtube: `ggb_build.py --ast-json PATH`** (exclusive with `--out`) serialising the
  expanded + parsed construction; each statement carries `src`, `line`, `t` (the `# t=` tag),
  `hidden_at_end`, `exported`, cached coords when the source XML had them. Pydantic models in
  `scripts/ggb_ast.py` (`pydantic` added to `PIP_PKGS`), `schemas/ggb-construction.schema.json`
  checked in with a regenerate-and-byte-compare test; mirrored byte-identical into bikar
  `packages/qiyas-schema/schemas/` with the hook-41 pattern and `codegen.mjs` types. Test: every
  construction and snippet → valid JSON. deps: P1.1.
- **P1.4 bikar: naqsh construction statements** (spec in §8; one PR per family, each with a
  Tier-0 witness, grammar.md production + §12 row, G3 ```bkr/```bkr invalid fences, a
  language-reference section, evaluator tests, `engine-extension` checklist):
  (a) bare-name `PointRef` + `point <id> = …` (alias, `midpoint`, `centroid`, `center`,
  `closest … to`, `intersect … [pick]`) with a **defined** intersect ordering in `evalIntersect`;
  (b) `Transform` (`= rotate … by … around`, `= reflect … across`, `= translate … by P Q`) on
  point/line/segment/polygon/circle; (c) `circle … through`, `line … through … parallel|
  perpendicular`, `line … = bisect angle …`, `polygon … = regular N from A to B`;
  (d) `rotate` admitted inside `mirror` bodies if not already. G2 regen after each; G1 tells
  which shipped `.bkr` used a new word (`point`, `regular`, …) as an identifier. deps: P0.4.
- **P1.5 bikar: `printer.ts`** — naqsh AST → `.bkr` text (bikar has no printer; `knobs` rewrites
  text). Gate: `parse(print(parse(src)))` deep-equals for every G1 corpus file. deps: P1.4(a).
- **P1.6 bikar: `coaster` declaration** (slice 2 of the object; slice 1 uses `piece … extrude`).
  Grammar: `coaster <Name>` / `outline round <⌀mm> | square <mm> | polygon <N> <across-mm>` /
  `inscribe <pattern>` / `base <mm>` / `relief straps|faces|both emboss|deboss <mm>` /
  `strap width <mm>` / `rim <mm>` / `edge chamfer|fillet <mm> [top|bottom]` / `trivet` (opt-in
  cut-through). **Kernel (D-I):** `packages/core/src/kernel3d/coaster.ts`, a height field over
  the outline: bottom flat, top `z = base + relief(x,y) + rim(r)`, side wall stitched; relief from
  the pattern's edge distance (straps: `|d| < w/2`) and face membership (`voids detect` /
  exported polygons); grid pitch a `param` (default cites the nozzle width in P0.1). It starts
  with a survey of `brick-top-face.ts` to reuse its relief union where it already conforms to
  polygon edges. **Structural validators (D2, each with `PASS:`/`FAIL:`, all queries on the
  field):** floor under the deepest deboss ≥ `CAL-CST-03`; strap width ≥ `CAL-CST-01`; relief
  height / strap width ≤ `CAL-CST-04` (tall thin ribs snap); bottom bevel angle ≤ 45° from
  horizontal (an overhang — say which convention, K10) while the top edge may be any curve;
  bottom chamfer ≥ elephant's-foot allowance `CAL-CST-05`; **weak points:** the solid region
  above the floor is one connected component and every neck (narrowest bridge between raised
  areas, measured by distance-transform erosion) ≥ `CAL-CST-01`, and no strap island is
  attached by less than that; `trivet` additionally requires the remaining region to be one
  component. FAIL cases are the hard ones: a deboss that leaves 0.2 mm floor, a 0.6 mm neck
  between two debossed faces, a 45.1° bottom chamfer. Print orientation fixed flat, top up,
  no supports; the mesh gate (`--check`) runs on every render. Bets `CAL-CST-01…05` registered
  in `.claude/skills/calibrate/bets.md`; no bare numbers (D3). deps: P1.4(a).
- **P1.7 Syntax highlighting, generated from one source.**
  - bikar: `scripts/gen-highlight.ts` reads `keywords.snapshot.txt` (G2) + `MATH_FUNCTIONS` +
    `grammarSurface()` (statement heads vs connectives) → `editors/naqsh.tmLanguage.json`,
    `editors/naqsh-keywords.json`, `editors/vscode-naqsh/` (contributes `.bkr`). Test: keyword
    alternation == fixture set, MathFn alternation == `MATH_FUNCTIONS`.
    `packages/core/src/dsl/highlight.ts` `tokenizeLine()` built on the lexer's own `tokenize()`
    with an error-tolerant fallback; `packages/web/src/main.ts` deletes its private `KEYWORDS`
    and `TOKEN_MATCHERS`; `packages/lab/src/editor.ts` gets a `<pre class="hl">` overlay behind
    the transparent textarea (same metrics, scroll-synced, ~60 lines, no dependency).
  - youtube: `scripts/gen_highlight.py` reads `ggb-vocabulary.txt` → `hub/src/prism-ggb.js`
    (replaces the inline grammar in `hub/src/App.jsx`) + `editors/ggb-commands.tmLanguage.json`;
    `hub/src/naqsh-keywords.json` mirrors bikar's byte-identically → `prism-naqsh.js`. Tests:
    alternation sets == fixtures.
  deps: P1.1 (youtube half), P1.4 (bikar half).

### Phase 2 — Transpiler, first construction, cookbook

- **P2.1 bikar: `bikar import geogebra <ast.json> -o <file.bkr>`** —
  `packages/core/src/import/geogebra/lower.ts`, a pure function AST → naqsh `ASTNode[]`: root
  frame check (D-G), identifier mangling (`'` → `_p`, keyword collision → trailing `_`,
  `rosette` is already reserved; table emitted in the header), free numbers → `param`, radians →
  degrees symbolically, `Sequence` eligibility proof (`step == 2π/N` and `hi−lo+1 == N` → one
  `rotate N around` block, else `for`), hide/export → layer assignment (all geometry in
  `blueprint <id>_scaffold`; pattern layer only `edges from` in `@export` order), single
  `intersect` with ≠1 hit → error. Unsupported command → typed error naming the cookbook gap;
  `--coverage` prints the histogram. Runs `validate` on its own output before writing; idempotence
  test (`parse(output)` equals the lowered AST). deps: P1.3, P1.4, P1.5.
- **P2.2 First slice: `GimTvN9hw4U`** (26 statements, six-fold rosette; exercises root frame,
  `point = rotate`, perpendicular bisector, single + paired intersect, `circle through`,
  `midpoint`, `line through … parallel`, `reflect` of line/point/list, `polygon [..]`, `Sequence`
  → `rotate 6`, nested `mirror`, `@hide except`, `@export`). Golden
  `bikar/patterns/Constructions/GimTvN9hw4U.bkr` (dir added to the G1 sweep roots) with fixture
  `packages/core/tests/fixtures/geogebra/GimTvN9hw4U.json`; test: lower + print == golden byte
  for byte, golden evaluates. youtube `make naqsh ID=…` and `make naqsh-score ID=…` (bikar PNG vs
  hero `export.png` through `ggb_score.py --align --mask-ref`, oracle O2); `make naqsh-coords
  ID=…` (oracle O1: `ggb_coords.py` dump vs `bikar render --format parts` label table, per
  label, frame-fitted); **expectation stated before viewing**: a six-petal rosette with its
  reflected ring, no scaffold lines. Nothing generated is committed in youtube. deps: P2.1, P1.2b.
- **P2.3 Slice-1 coaster (fast path):** `piece Coaster` / `extrude GimTvN9hw4U depth $depth`
  appended to the golden with `param unit = 20 range 15..45` (mm per GeoGebra unit; mini ≈ 40 mm
  across at 20, standard ≈ 90 mm at 45); `bikar render --format stl --check` for both; screenshots
  recorded. deps: P2.2.
- **P2.3b qiyas: `qiyas mesh compare <a.stl> <b.stl>` (oracle O3)** — footprint IoU at
  mid-height, symmetric Hausdorff, volume ratio, worst local deviation; JSON score + PASS/FAIL
  against thresholds whose defaults cite P0.1 (qiyas is the score authority; FastAPI/CLI
  conventions of that repo). Run on `reference.stl` (P1.2b, OpenSCAD) vs the P2.3 STL for
  `GimTvN9hw4U`; the by-design FAIL case is the same construction with one `edges from` dropped.
  deps: P1.2b, P2.3.
- **P2.4 Readability rules + header convention** in `language-reference.md` "Constructions"
  and the `dsl-design` skill (rules in §8); `bikar validate --style constructions` enforces the
  header. deps: P2.1.
- **P2.5 Cookbook `bikar/docs/cookbook/geogebra-to-naqsh.md`** — one `## Cmd` per census command
  by frequency; template: ```ggb fence → ```bkr fence → **Why** → **Seen in** (id + `t=`) →
  **Pitfalls**. Kept true by: G3's fence glob extended to `docs/cookbook/**`;
  `cookbook-conformance.test.ts` (every recipe has a fixture whose lowered+printed output equals
  its `bkr` fence; every vocabulary command has a recipe or a row in `## Not yet supported`, both
  directions); youtube's grammar test parses the mirrored `ggb` fences. `<!--count:cookbook-recipes-->`.
  deps: P2.1.
- **P2.6 Second slice: `7apC5Q9QS-8`** (144 statements: `AngleBisector`, indexed `Intersect` →
  `pick`, `Polygon(O2,O1,8)` → `regular`, heavy unrolled Rotate chains). Golden + score. deps: P2.2.
- **P2.7 Disc coaster** from the golden via P1.6 (`coaster GimRosette outline round $size
  inscribe GimTvN9hw4U relief emboss …`), mini `size=40` and standard `size=90`, `--check` both.
  deps: P1.6, P2.2.

### Phase 3 — Repeatable process: skill, ledger, hook, catalog, gallery

- **P3.1 Skill `3d-models/.claude/skills/import-construction/`** — `SKILL.md` with a sharp
  dispatch `description` ("import/migrate a GeoGebra construction to naqsh and a coaster") and a
  `rubric.md` read at run time (readability rules + fidelity checks). Steps: pick id from the
  ledger → `ggb_build.py --ast-json` (or `ggb_from_xml.py` first) → `bikar import geogebra` →
  readability review → `naqsh-score` + coord oracle → coaster block → catalog entry → ledger row
  → PRs. deps: P2.5, P2.7.
- **P3.2 Ledger + gate + hook.** `docs/constructions/ledger.md`: one row per youtube
  reconstruction id — title, youtube state (attempted = `reconstructions/<id>/` exists; done =
  listed in `docs/tasks/done.md`, read at a **pinned youtube git ref**, the pointer-gate
  convention), naqsh file, score, coord oracle, coaster STL, catalog id, printed. Gate
  `.claude/gates/constructions_ledger.py` (`make validate-constructions`, Makefile tail): **fails**
  on a row whose `.bkr`/STL path is missing; **reports** (non-blocking, the `20-use-cases`
  reminder shape) every youtube id without a row; hook `.githooks/pre-commit.d/38-constructions`;
  a SessionStart hook line "N constructions not yet migrated: …". Counts
  `<!--count:constructions-migrated-->` / `<!--count:constructions-total-->`. Worktree self-test
  (`gate-verdict-checkout-independent`). `M60LJNNslHU` (mechanism, no final piece) is a row
  marked "no piece by design" — the by-design failure the gate must not skip. deps: P2.2.
- **P3.3 Catalog + gallery.** Catalog entries `CS-1…` in `.claude/skills/prototype/catalog.md`
  (`--param unit`/`size`, `--piece Coaster` harvested by hook 36 from the `.bkr`); `make coasters`
  (Makefile tail: bikar render STL + views for `patterns/Constructions/*.bkr`, vendor into
  `src/Coasters/`, previews in `build/`); "The Coasters" section + JS array in `index.html`;
  `DEPLOY_PATHS`, `docs/site-graph.json` node; use-case map row with anchored pointers
  (`validate.py --refresh`, stage `use-cases.md` in the same commit). deps: P2.7.

### Phase 4 — Many on one plate (dynamic STLs, mix-and-match CLI)

- **P4.1 `tools/bambu slice compose <plate.yaml>`** — manifest items `{bkr, piece, params,
  count}`; render each variant via bikar (cache keyed by bkr hash + params), collect STLs, call
  Bambu Studio CLI with all inputs `--arrange 1 --export-3mf`; `--dry-run` prints argv; `--bed
  x2d` = 256 × 256 with an area/count pre-check that fails before the slicer; per-object
  provenance pins `bikar:<path>@<ref>` in the plate record; mesh `--scale` passthrough prints the
  D-D warning. `docs/plate-composer-design.md` (Defaults cite P0.1; Validator PASS/FAIL for the
  bed check). deps: P3.3.
- **P4.2 Mini plate manifest `docs/plates/minis-01.yaml`**: every migrated construction at mini
  size, count 2, one relief variant each — the plate after Plate 1. `bambu validate plate`
  accepts a composed 3MF. deps: P4.1, P3.2.
- **P4.3 Print record** when Omar dispatches: `docs/prints/<date>-minis-01/` through the
  compare-verdict loop (gate R5), settling `CAL-CST-01/02`. Owner-gated. deps: P4.2, Plate 1.

### Phase 5 — Scale the corpus

- **P5.1** Remaining done rungs in ladder order (`rDuxHF3xMOc`, `tA8eSdVx_EQ`, `sDO9fpu76v8`,
  `lEfWSogWscs`, `nmEjCTzMbDg`), each adding recipes for new commands and a ledger row. Conics
  (`Parabola`, `Hyperbola`, `CircularArc` beyond the `arc` family) are engine tasks filed, not
  faked. deps: P3.1.
- **P5.2** Standard-size plate once `CAL-CST-*` are measured. deps: P4.3.
- **P5.3** `frame` block decision for arbitrary free points, only if a public GeoGebra fixture
  needs it (D-G). deps: P1.2 fixtures.

## Dependency summary

```
P0.1 → P0.2 → P0.3
P0.5 → P1.1 ─┬→ P1.2 ──────────────┐
             ├→ P1.3 ──────────────┼→ P2.1 → P2.2 ─┬→ P2.3 (fast coaster) ─┬→ P2.3b (O3) → P3.3 → P4.1 → P4.2 → P4.3 → P5.2
             └→ P1.7(youtube half) │      ▲        ├→ P2.6 → P5.1          │
P0.5 → P1.2b (O1 dump + O3 ref) ───┼──────┘        ├→ P3.2 ────────────────┘
P0.4 → P1.4 ─┬→ P1.5 ──────────────┘               └→ P2.4, P2.5 → P3.1
             ├→ P1.6 → P2.7 → P3.1 → P5.1
             └→ P1.7(bikar half)
```

Critical path to the first mini STL: P0.5 → P1.1 → P1.3 → P2.1 → P2.2 → P2.3, with P1.4 +
P1.5 in parallel and P1.2b alongside (O1 gates P2.2's acceptance, O3 gates the catalog entry).
P1.2, P1.6, P1.7 are off the critical path.

## Design docs to write (each with research, links, options, rubric)

| Doc | Repo | Feeds from | Gate markers |
|---|---|---|---|
| `docs/geogebra-construction-import-design.md` | 3d-models | `docs/research/geogebra-construction-import-survey.md` | Default/Validator/count, pointer gate |
| `docs/coaster-design.md` (height-field kernel, relief modes, rim profiles, the structural validators and their hard FAIL cases, print orientation, mini/standard sizing) | 3d-models | survey + `CAL-CST-01…05` | Default → CAL ids, Validator PASS/FAIL |
| `docs/construction-equivalence.md` (the three oracles, what each cannot see, thresholds) | 3d-models | survey + `ggb_score.py` threshold | Validator PASS/FAIL per oracle |
| `docs/mesh-compare.md` | qiyas | O3 metrics, threshold provenance | that repo's gates |
| `docs/plate-composer-design.md` | 3d-models | survey (Bambu CLI, X2D bed) | Validator for bed check |
| `docs/design/<NN>-construction-statements.md` + `docs/decisions/…naqsh-language-name.md` | bikar | §8 + `dsl-design` | G1–G3 on grammar.md |
| `docs/cookbook/geogebra-to-naqsh.md` | bikar | P2.5 | G3 fences, conformance test, count |
| `docs/grammar.md` (new) + `docs/design/construction-ast-export.md` | youtube | P1.1–P1.3 | conformance test, schema mirror |

## Verification (end to end)

1. youtube `make test`: grammar conformance, vocabulary fixture, `--ast-json` for all 18 files,
   `ggb_from_xml.py` round-trip on the 9 renders + public fixtures with an enumerated coverage.
2. bikar `npm test`: G1 (now sweeping `patterns/Constructions/`), G2 (new count), G3 (new
   productions + cookbook fences), printer round-trip, Tier-0 witnesses, golden byte-equality,
   cookbook conformance, highlighter == fixture.
3. Oracles on `GimTvN9hw4U`: O1 `make naqsh-coords` reports every label within tolerance and
   no missing/extra label; O2 `make naqsh-score` ≥ the loop's threshold; O3 `qiyas mesh compare
   reference.stl coaster.stl` passes, and the dropped-edge variant fails.
4. `bikar render … --format stl --check` for mini and standard, both coaster forms; every
   structural validator's PASS and hard FAIL fixture exercised (thin floor, thin neck, 45.1°
   bottom chamfer, strap island); `make coasters`; `make validate` green (docs, pointers,
   catalog, counts, constructions ledger, use-cases).
5. `bambu slice compose docs/plates/minis-01.yaml --dry-run` prints a valid multi-input argv;
   the real run produces a `.3mf` that `bambu validate plate` accepts. No print is sent.
6. Gallery: local `index.html` opened in a real browser; the Coasters section renders previews.
7. Ledger hook in a fresh worktree: every youtube id has a row or a reminder; the SessionStart
   nudge lists the unmigrated ids.

## Assumptions stated (correct on review)

- Sources of record live in **bikar** `patterns/Constructions/` (capitalised like `Pieces/`,
  `Orbs/`); 3d-models vendors into `src/Coasters/`; youtube commits nothing generated and gains
  only the grammar doc, the XML front-end, `--ast-json`, the schema and the highlighter generator.
- The ledger, skill and gates live in **3d-models** (owner of the catalog and gate infrastructure).
- The AST schema's canonical copy sits with its producer (youtube), vendored into bikar's
  `packages/qiyas-schema` (renamed `schema-mirror` only if the name bothers).
- Mini ≈ 40 mm across, standard ≈ 90 mm, both via `param`, never two files.
- The first construction is `GimTvN9hw4U`, the second `7apC5Q9QS-8`, then ladder order.

## §8 Language design (reconciled from the design report)

**Principle:** derived objects take one new shape, `<kind> <Name> = <op> …` ("define this named
object as that operation" — exactly what a GeoGebra line means); existing forms stay. Angles are
degrees, CCW. `rotate N around` / `mirror around` **blocks replicate statements**; `= rotate` /
`= reflect` **derive one named object**; documented side by side in §7.10, never conflated.

Gap table (GeoGebra → naqsh):

| GeoGebra | naqsh |
|---|---|
| `A=(0,0)`, `B=(1,0)`, `D=(0,1)` | `circle unit center(0,0) radius $unit` · `divide unit into 4` · `point A = unit.mpt` · `point B = unit.cpt0` · `point D = unit.cpt1` (other free points: error, D-G) |
| free number `G = 0.3333`, `@slider n` | `param G = 0.33333 range 0.1..1`, `param n = 6 range 3..12 step 1` |
| `Circle(A, r)` / `Circle(B, H)` | `circle c center(A) radius $r` / `circle c center(B) through H` |
| `Line(A,B)` / `Segment(A,B)` | `line l from A to B` / `segment s from A to B` |
| `Line(I, l)` / `PerpendicularLine(J, s)` | `line n through I parallel l` / `line p through J perpendicular s` |
| `PerpendicularBisector(A,B)` | `bisector m from A to B` (unchanged) |
| `AngleBisector(A,B,H)` / `{a,b} = AngleBisector(r, n)` | `line rb = bisect angle A B H` / `… = bisect angle r n [other]` |
| `Rotate(A, -120°, B)` / `Rotate(l, 45°, O)` | `point C = rotate A by -120 around B` / `line l2 = rotate l by 45 around O` (also segment/polygon/circle) |
| `Reflect(X, m)` | `point X_p = reflect X across m` (also line/polygon) |
| `Translate(pet, Vector(P,Q))` | `polygon petE = translate pet by P Q` (`Vector(P)` → `by A P`) |
| `Intersect(m,n)` / `{E,F}=Intersect(c,d)` / `Intersect(c,p,2)` | `point H = intersect m n` (error if ≠1) / `intersect EF c d` + `point E = EF.cpt0` / `point K = intersect c p pick 2` (prefer `pick nearest P`) |
| `Midpoint(A,B)` / `Centroid(q)` / `Center(c)` / `ClosestPoint(c,P)` | `point I = midpoint A B` / `centroid q` / `center c` / `closest c to P` |
| `Polygon(A,B,6)` / `Polygon(H,J,I,K)` | `polygon q = regular 6 from A to B` (vertices `q.p0..p5`) / `polygon q [H J I K]` |
| `Sequence(Rotate({q1,q2}, 2*pi*i/8, H), i, 0, 7)` | pattern layer: `rotate 8 around H` ⏎ `edges from q1` ⏎ `edges from q2` (partial orbit → `for`) |
| `Reflect(ring, de)` then `Sequence(Rotate(…))` | nested `rotate 6 around G` ⏎ `mirror around D E` ⏎ … |
| `@hide`, `@hide except`, `@export` | not statements: geometry → `blueprint <id>_scaffold`; the pattern draws only the export whitelist |
| `@view`, `@style`, `@labels` | dropped (`@style stroke` → optional `edges color`) |
| `# t=mm:ss` | preserved above each emitted statement |

Grammar productions to add to `bikar/docs/grammar.md`:

```
PointRef      = IDENT "." PointId | IDENT ;
CircleCenter  = VARIABLE | NUMBER "," NUMBER | REPEATADDR "." PointId | PointRef ;
CircleStmt    = "circle" IDENT "center" "(" CircleCenter ")" ( "radius" Expr | "through" PointRef ) NL ;
PointStmt     = "point" IDENT "=" PointExpr NL ;
PointExpr     = PointRef | "intersect" EntityId EntityId [ Pick ] | "midpoint" PointRef PointRef
              | "centroid" IDENT | "center" EntityId | "closest" EntityId "to" PointRef | Transform ;
Pick          = "pick" ( NUMBER | "nearest" PointRef | "farthest" PointRef ) ;
IntersectStmt = "intersect" IDENT EntityId EntityId [ Pick ] NL ;
LineStmt      = "line" IDENT ( "from" PointRef "to" PointRef
              | "through" PointRef ( "parallel" | "perpendicular" ) EntityId
              | "=" ( Transform | "bisect" "angle" PointRef PointRef PointRef [ "other" ]
                                | "bisect" "angle" EntityId EntityId [ "other" ] ) ) NL ;
SegmentStmt   = "segment" IDENT ( "from" PointRef "to" PointRef | "=" Transform ) NL ;
PolygonStmt   = "polygon" IDENT ( "[" PointRef { PointRef } "]"
              | "=" ( "regular" NUMBER "from" PointRef "to" PointRef | Transform ) ) NL ;
CircleDerived = "circle" IDENT "=" Transform NL ;
Transform     = "rotate" EntityId "by" Expr "around" PointRef
              | "reflect" EntityId "across" EntityId
              | "translate" EntityId "by" PointRef PointRef ;
```

New reserved words (G2 delta, each a §12 row): `point through parallel perpendicular reflect
translate across midpoint centroid closest pick nearest farthest regular bisect other`
(`center` to be checked: keyword or contextual today). Semantics to record in the decision:
intersect ordering becomes **defined** (circle-first pairs by angle around the first centre,
otherwise by parameter along the line) so a `pick N` swap is caught by the render-diff;
`Name = IDENT | KEYWORD` positions must not admit the new words as class names.

Readability rules (transpiled and hand-written constructions alike):

1. Names are the presenter's; only mandatory mangling (`'`→`_p`, keyword→trailing `_`), table
   in the header.
2. One statement per GeoGebra line, source order, provenance comment above it
   (`# t=03:10  H = Intersect(m, n)`).
3. Section banners follow the `# t=` tags.
4. Root frame first, always the same three lines.
5. All geometry in `blueprint <id>_scaffold`; the pattern layer only draws.
6. One generator per ring; nested orbits nest blocks; partial orbits use `for`; never unrolled.
7. Numbers appear only as `param`s or angles in degrees.
8. The pattern's `edges from` order is the `@export` order (else the `@hide except` survivors).

Header convention:

```
# naqsh construction — GimTvN9hw4U
# title:  <video title>
# url:    https://www.youtube.com/watch?v=GimTvN9hw4U
# steps:  26 statements, 20 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:<…>
# renamed: rosette -> rosette_ (reserved word)
param unit = 20 range 15..45          # mm per GeoGebra unit
```

## §9 Sources and pointers

Repo facts: `youtube/scripts/ggb_build.py` (`parse()`/`expand()`/`die()`, `_CMD_TYPE`,
`_POLYMORPHIC`, emitter ~L1106-1163), `youtube/Makefile:39` (`PIP_PKGS`), `youtube/hub/src/App.jsx:14-23`
(inline Prism grammar), `youtube/docs/design/youtube-reconstruct.md:130-172` (build options, GgbAPI
fallback), `bikar/docs/grammar.md` (§2.4 keyword count, §5.1 `PointRef`, §7.2 intersect, §7.10
blocks, §10 3D decls, §12 coverage; G1–G3 table), `bikar/packages/core/src/dsl/{parser,evaluator,
tokens}.ts`, `bikar/packages/core/tests/fixtures/keywords.snapshot.txt`, `bikar/packages/web/src/
main.ts` (~L984 private `KEYWORDS`), `bikar/packages/lab/src/editor.ts`, `bikar/packages/qiyas-schema/`
(mirror + `codegen.mjs`), `bikar/patterns/Pieces/Nail-Tile.bkr` (extrude template),
`bikar/.claude/skills/dsl-design/SKILL.md`, `3d-models/.claude/gates/catalog_models.py:114-120`,
`3d-models/tools/bambu/src/commands/slice.ts:22-44,132-149`, `3d-models/Makefile:259,283,591`.

Web (preserved verbatim in P0.1):
- GeoGebra XML format: https://wiki.geogebra.org/en/Reference:File_Format ,
  https://geogebra.github.io/docs/reference/en/Common_XML_tags_and_types/
- GeoGebra CLI and export: https://geogebra.github.io/docs/reference/en/Command_Line_Arguments/ ,
  https://geogebra.github.io/docs/manual/en/commands/ExportImage/
- Headless GgbAPI route: https://github.com/TioSavich/geogebra-mcp
- GeoGebra source: https://github.com/geogebra/geogebra
- OpenSCAD SVG import limits: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/SVG_Import
- Bambu Studio CLI: https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage
- X2D specs: https://bambulab.com/en/x2d/specs
- Parser toolkits surveyed: https://lark-parser.readthedocs.io/ , https://ohmjs.org/ ,
  https://github.com/peggyjs/coverage , https://chevrotain.io/
