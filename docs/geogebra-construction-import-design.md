# GeoGebra constructions → naqsh → coasters — umbrella design doc

Status: **v1 — grounded in
[`research/geogebra-construction-import-survey.md`](research/geogebra-construction-import-survey.md)
(every number below cites a survey section or a `CAL-*` bet); decisions
recorded as D-055…D-063 in [`decisions-log.md`](decisions-log.md).**
Scope: how any GeoGebra construction — the nine youtube reconstructions first,
any `.ggb` eventually — becomes a naqsh (`.bkr`) file that bikar renders, how
that file is proven equivalent to its source, how the flat art becomes a
printable coaster, and how many coasters share one X2D plate. This doc owns the
architecture, the grading rubric and the option tables. Three child docs own
their own numbers: construction equivalence (the three oracles), the coaster
kernel and its structural validators, and the plate composer. They are written
in phases P2, P1.6 and P4 of §11 and are **not linked here until they exist**
(K9: a link to an unwritten file is a defect, not a promise).

Naming: **naqsh is the language, bikar is the engine.** A "naqsh file" is a
`.bkr` file. No package, directory or extension is renamed (D-055).

---

## 1. Goals

1. **Construction-level import.** A GeoGebra file is a recipe (survey §2.3):
   `<command>` blocks, not coordinates. The import lowers the recipe to naqsh
   statements that GeoGebra's semantics and naqsh's evaluator agree on, so the
   result stays a relative construction that re-renders at any `param`.
2. **Any GeoGebra file, honestly.** "Any" is a claim about a set (K2). The
   tool prints the set: every command it lowers, every command it refuses, and
   it aborts on the second kind unless told which to drop.
3. **One parser per language.** The `.ggb-commands` grammar is parsed only by
   the youtube repo's `ggb_build.py`; naqsh is parsed only by bikar's
   `parser.ts`. The bridge is a JSON AST whose schema is owned by the producer
   and mirrored byte-identically into the consumer.
4. **Equivalence is three claims, three oracles.** Per-label geometry, what is
   drawn, and what is solid. No oracle implies another (§6).
5. **A coaster is a height field** (D-063): manifold by construction, one
   kernel for rim, bevel and relief, every printability check a query on the
   same field.
6. **Many on a plate, none by hand.** A manifest re-renders each variant from
   `param`s and hands the STLs to the Bambu Studio CLI to arrange (§9).
7. **Repeatable for the Nth construction.** A ledger with a gate, a hook that
   names the unmigrated ids, and a skill that walks the steps.

Non-goals: dispatching a print (owner-gated; minis ride Plate 1 or the plate
after it, D-059); importing GeoGebra scripting, text or sliders as animation;
a new literal-carrying syntax for arbitrary free points (D-061 defers it).

## 2. Ground truth (from the survey)

| Fact | Where |
|---|---|
| Nine reconstructions, 20 command kinds, Reflect/Intersect/Rotate dominate | survey §1 |
| `parse()` dies on any unknown line; `_CMD_TYPE` 40 keys + `_POLYMORPHIC` 7 | survey §2.1 |
| The youtube loop accepts at edge-SSIM ≥ 0.70 | survey §2.2 |
| GeoGebra recomputes dependents from `<command>` blocks on load | survey §2.3 |
| `pydantic`, `playwright`, `jsonschema`, `lark` absent from the env | survey §2.4 |
| `.ggb` = zip of `geogebra.xml`; a GeoGebra-saved file has the same blocks plus cached coords | survey §3 |
| Desktop `--export` writes SVG/PNG/PDF/EMF/EPS; Apps API has coords, command strings, no STL | survey §4, §5 |
| OpenSCAD imports SVG as closed polygons only; 2021.01 installed | survey §7 |
| Bambu Studio CLI 02.08.02.61 takes many inputs, `--arrange`, `--export-3mf` | survey §8 |
| X2D single-nozzle footprint 256 × 256 mm | survey §9 |
| naqsh: normative EBNF + gates G1/G2/G3, 130 reserved words, no printer | survey §10, §11 |

Engine facts that shape the language work (bikar tree at the survey's ref):
naqsh has `PointRef = IDENT "." PointId` and no bare named points; its
`rotate N around` and `mirror around` are replication **blocks**, not
single-object transforms; `bisector` is the perpendicular bisector; there is no
angle bisector, parallel/perpendicular line, midpoint, centroid or
`circle … through`. See
[`dsl-grammar-formalization.md`](dsl-grammar-formalization.md) for the gate
numbering this doc reuses.

## 3. The rubric

Each option is scored 0/1/2 per question. The questions are recorded verbatim
so the reasoning is inherited, not re-derived.

- **R1 Generality:** any GeoGebra file, or only our `.ggb-commands`?
- **R2 One parser per language:** is any grammar known in two places?
- **R3 Fidelity:** does the output stay a relative, re-renderable construction, or freeze?
- **R4 What it verifies:** render-diff, coordinate oracle, mesh gate — or nothing?
- **R5 Failure honesty:** are unsupported inputs enumerated loudly?
- **R6 Cost:** to the first coaster / to the Nth construction.
- **R7 Gate fit:** rides G1–G3, catalog, docs, use-cases, counts?
- **R8 Readability:** would a person author the resulting file?

Per the repo tenet, the cheapest option is not the default and every option
states what it verifies (R4); one that verifies nothing is named as such.

## 4. Options

### 4.1 Import path

| Path | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| A. GeoGebra `--export=svg` → OpenSCAD `import()` → STL | 2 | 2 | 0 | 0 | 0 | 2/1 | 0 | 0 | Rejected: frozen, closed polygons only (survey §7), verifies nothing. |
| B. XML → `.ggb-commands` → JSON AST → `bikar import geogebra` | 2 | 2 | 2 | 2 | 2 | 1/2 | 2 | 2 | **Chosen** (D-056). |
| C. Python emits `.bkr` text in youtube | 1 | 0 | 2 | 1 | 1 | 2/1 | 1 | 1 | Rejected: naqsh syntax encoded in the repo that does not own the grammar; no evaluator to check semantics. |
| D. TypeScript re-parser of `.ggb-commands` in bikar | 0 | 0 | 2 | 2 | 1 | 1/1 | 1 | 2 | Rejected: a second parser of one grammar. |
| E. Headless Apps-API coordinate dump → `polygon` literals | 2 | 2 | 0 | 1 | 1 | 1/1 | 0 | 0 | Rejected as the path; **kept as oracle O1's reference side** (§6). |

### 4.2 Parser tooling for `.ggb-commands`

Keep the hand-rolled parser and add a normative EBNF with a G3-style
conformance test (bikar's own choice, survey §10). Lark is rejected: not in the
env (survey §2.4); the grammar is line-regular except one nested `Sequence`
form the parser already special-cases; a Lark grammar beside the parser is a
second source of truth, and replacing the parser is the big-bang rewrite this
repo already rejected for naqsh. Ohm, Peggy and Chevrotain are rejected for
bikar on the same grounds (D-060).

### 4.3 Plate composer

| Option | Verifies | Verdict |
|---|---|---|
| P1. Manifest → bikar re-render per variant → Bambu Studio CLI multi-input `--arrange 1 --export-3mf` | bed-area pre-check, mesh `--check` per STL, the slicer's own placement | **Chosen.** The manifest is the reviewable artifact; the CLI is already wrapped. |
| P2. Own 2D packer writing a 3MF | the same, plus packing we would have to test ourselves | Deferred; only if P1's arrange proves unreliable, recorded in `docs/issues/` when it does. |
| P3. Manual GUI arrangement | nothing | Rejected: not repeatable. |

## 5. Architecture

```
youtube repo                                         bikar repo                              3d-models repo
──────────────                                       ──────────────                          ──────────────
any geogebra.xml/.ggb ─ggb_from_xml.py─▶ .ggb-commands
construction.ggb-commands ──────────────▶ ggb_build.py --ast-json ─▶ construction.json (Pydantic schema, mirrored byte-identical)
                                                                            │
                                                     bikar import geogebra ─┴─▶ lower.ts → printer.ts → patterns/Constructions/<id>.bkr
                                                     (header + provenance, mangling table, coverage report; fails closed)
                                                            │
                                                     bikar render --format views ⇄ edge-SSIM vs export.png       (O2, ggb_score.py)
                                                     bikar render --format parts ⇄ Apps-API coords.json per label (O1, ggb_coords.py)
                                                            │
                                                     piece Coaster extrude … (slice 1)   coaster <Name> … (slice 2)
                                                            └──────────────▶ STL ⇄ OpenSCAD reference.stl (O3, qiyas mesh compare)
                                                                              └──▶ make coasters ──▶ src/Coasters/, catalog, gallery
                                                                                                          │
                                                                                 tools/bambu slice compose plate.yaml ──▶ X2D .3mf
                                                                                 (re-render per --param, arrange on 256×256)
```

Ownership: sources of record are bikar `patterns/Constructions/*.bkr`
(capitalised like `Pieces/` and `Orbs/`); this repo vendors STLs into
`src/Coasters/` and owns the ledger, catalog, gates and skill; youtube commits
only the grammar doc, the XML front end, the AST export, the schema and the
highlighter generator, never generated output.

### 5.1 The AST contract (summary; the schema is the contract)

One JSON document per construction, produced by `ggb_build.py --ast-json` after
`expand()` and `parse()` (shipped 2026-09-17; youtube's
`docs/design/construction-ast-export.md` is the producer's own account):

- `schema_version`: `1`.
- `construction`: `{ id, source_path, source_sha256, title?, url? }` — `title`
  and `url` only for a `construction.ggb-commands`, never for a technique
  snippet, whose header quotes *other* videos.
- `statements[]`, in source order, one per authored line, each
  `{ line, src, t?, kind, outputs[] }` where `line` is the authored line (slider
  expansion keeps lines 1:1) and
  `kind ∈ { point_literal, number_decl, command, multi_out, sequence }`;
  a `point_literal` adds `coords`, a `number_decl` adds `{ value, is_angle }`,
  a `command` / `multi_out` adds `{ cmd, args[] }` with args typed
  `label | number | list`, a `sequence` keeps its nested form
  `{ body: { cmd, target, angle, centre }, var, lo, hi, angles_rad[] }` — the
  angle verbatim and evaluated, one output per `Sequence`.
- `outputs[]` per statement, each `{ label, type?, hidden_at_end, exported }`:
  `type` is `infer_type`'s best effort (`null` for a command outside its table,
  e.g. `UnitVector`); `hidden_at_end` is the presenter's hide as the final XML
  shows it (a free number is always hidden by the emitter, so there it is not
  the presenter's choice); `exported` is `@export` membership. There is no
  separate labels list: the outputs are the label table.
- `directives`: `{ views[], hides[], exports[], styles[] }` — `@hide except`
  is a `hides[]` entry with `keep_only: true`.
- `cached_coords{}`: label → `[x, y]` when the source XML carried them (empty
  for files written by `ggb_build.py`; `--cached-coords` supplies them).

Pydantic models are the source; `schemas/ggb-construction.schema.json` is
checked in with a regenerate-and-byte-compare test (`make schema-sync`); bikar
vendors it byte-identically as `packages/qiyas-schema/schemas/ggb_construction.json`
and generates `GgbConstruction` from it. Byte identity is this repo's
schema-mirror gate's job (hook 41, `.claude/gates/schema_mirror.py`): bikar's
vendored tree is split by stem, `ggb_construction` is held to youtube at a
`youtube` pin in the use-case map's `as_of` block — a local commit, since
youtube has no remote — and the rest to qiyas. The pin is owed the moment
bikar's pin vendors the stem: that state is a finding, not a skip.

### 5.2 Root frame and free values (D-061)

GeoGebra free points are root-circle aliases: `A` is the centre, `B` and `D`
are the 0° and 90° division points of the unit circle. A free point off that
frame is a transpile error whose message says "rewrite relative to A, B". Free
numbers become `param`s. This covers all nine reconstructions (survey §1) with
no new literal-carrying syntax. A `frame` block for arbitrary free points is
deferred to a bikar `dsl-design` decision, opened only when a public fixture
needs it.

### 5.3 What lowering must refuse (D-057)

Unknown command; free point off the root frame; a single-output `Intersect`
that yields ≠ 1 hit; a `Sequence` whose step and range do not prove a full
orbit and that cannot be expressed as `for`; an identifier that collides with a
reserved word after mangling. Each is a typed error naming the cookbook gap.
`--coverage` prints the histogram of lowered and refused commands.

**Validator:** `bikar import geogebra` exits non-zero and prints every refused
statement, with line and reason, before writing anything.
- PASS: an AST containing one `Parabola(…)` statement produces no `.bkr`, exit
  code 1, and a report listing `Parabola` under "unsupported" with the source
  line — and the same AST with `--lenient Parabola` writes the file and lists
  the dropped statement in the file header.
- FAIL: an AST whose `Intersect(c, d)` has two solutions but a single output
  label, where the tool silently picks the first; the hard case is two circles
  that meet twice, which is every `{E,F} = Intersect` in the corpus written
  with one label.

## 6. Equivalence: three oracles (D-062)

| Oracle | Claim | Reference side | naqsh side | Compare |
|---|---|---|---|---|
| O1 geometry | every named object has the same geometry | `coords.json` from the Apps API via Playwright (survey §5) | `bikar render --format parts` label table | per label after fitting the frame; missing or extra label is a FAIL |
| O2 drawing | the same objects are visible at the end | hero `export.png` from the reconstruct loop | `bikar render --format views` | edge-SSIM via `ggb_score.py --align --mask-ref` |
| O3 solid | the same region is solid | `coords.json` polygons → generated `.scad` → OpenSCAD 2021.01 `reference.stl`, no bikar code | `piece Coaster extrude …` STL | `qiyas mesh compare`: footprint IoU at mid-height, symmetric Hausdorff, volume ratio, worst local deviation |

**Default:** the O2 accept threshold is edge-SSIM ≥ 0.70, the youtube loop's
own `--ssim-min` default, read from `ggb_score.py` in
[survey §2.2](research/geogebra-construction-import-survey.md). The metric is scikit-image's
[`structural_similarity`](https://scikit-image.org/docs/stable/api/skimage.metrics.html) over Canny edges; the number has no
published source — it is the loop's own bar, inherited rather than bet because O2 is a
regression check against that loop, not a print quantity. The naqsh
render must clear the same bar the reconstruction cleared.

O1 tolerance, O3 thresholds and the frame-fitting procedure are specified in
the equivalence doc (P2), which registers its own bets; nothing here states
them. O3 compares the **flat extruded pattern** only: rim, bevel and relief
have no GeoGebra reference and are validated by the mesh gate, the coaster
validators and the `CAL-CST-*` bets. An aggregate score never discharges a
per-object claim, so O1 is per label and O3 reports the worst local deviation,
not only the IoU.

**Validator:** O1 fails on any label whose fitted position differs from the
reference by more than the tolerance, and on any label present on one side only.
- PASS: `GimTvN9hw4U` lowered and evaluated reports every one of its labels
  within tolerance and no label missing on either side.
- FAIL: the same file with `pick 2` swapped for `pick 1` on one intersection
  reports that label out of tolerance and every dependent label after it; the
  hard case is a swap that lands on the mirror image, which O2's SSIM cannot
  see because the drawing is symmetric.

## 7. Language additions (summary; specified in bikar)

Derived objects take one new shape, `<kind> <Name> = <op> …`. The gap table,
the grammar productions, the reserved-word delta and the defined intersect
ordering live in the bikar design doc and decision that P1.4 ships; the
readability rules and header convention live in bikar's language reference.
What this repo pins:

- `rotate N around` / `mirror around` **replicate**; `= rotate` / `= reflect`
  **derive one named object**. Documented side by side, never conflated.
- Angles are degrees, CCW; radians in the source become degrees symbolically.
- Intersect ordering becomes **defined** so that a `pick N` swap is caught by
  O1, not hidden by O2.
- New reserved words are a G2 delta, each with a §12 row in bikar's grammar
  doc; G1 reports which shipped `.bkr` used one as an identifier.

## 8. The coaster (summary; specified in the coaster doc)

A coaster is a height field over an outline (D-063): flat bottom, top
`z = base + relief(x, y) + rim(r)`, side wall stitched. Straps, face
emboss/deboss and the edge chamfer or fillet are all height contributions.
Cut-through is a `trivet` mode, not a coaster. bikar has no boolean union, so
this is the only shape that is manifold by construction with one kernel.

Two slices: slice 1 is `piece Coaster` / `extrude <pattern> depth $depth` on
the existing machinery, with `param unit` setting millimetres per GeoGebra unit
(mini and standard are two values of one param, never two files, D-058).
Slice 2 is a `coaster` declaration with `outline`, `inscribe`, `base`,
`relief`, `strap width`, `rim`, `edge` and `trivet`.

Structural validators, each a query on the field, each with a hard FAIL fixture
in the coaster doc: floor under the deepest deboss, strap width, relief height
to strap width ratio, bottom bevel angle (stated with its convention, K10),
bottom chamfer vs elephant's foot, one connected solid above the floor with
every neck wider than the strap floor, and `trivet` connectivity. Their
defaults are bets `CAL-CST-01…05`, registered in bikar's calibration registry
before the coaster doc states a single number
([`calibration-design.md`](calibration-design.md)). Print orientation is fixed
flat, top up, no supports; `--check` runs on every render
([`print-validation-design.md`](print-validation-design.md)).

## 9. The plate composer (summary; specified in the plate doc)

`tools/bambu slice compose <plate.yaml>`: manifest items
`{ bkr, piece, params, count }`; each variant is re-rendered by bikar (cache
keyed by file hash + params), the STLs are handed to the Bambu Studio CLI as
multiple inputs with `--arrange 1 --export-3mf` (survey §8). Dynamic size is
always a `--param` re-render; mesh `--scale` exists only as a flagged escape
hatch that prints a warning, because scaling a mesh scales walls and relief
below the printable floor (D-058).

**Default:** the `--bed x2d` footprint is 256 × 256 mm, the X2D single-nozzle
build area ([survey §9](research/geogebra-construction-import-survey.md), a
secondary source because [bambulab.com/en/x2d/specs](https://bambulab.com/en/x2d/specs)
returned 403 to the fetcher), the
same value this repo's confirmed slice profile records.

**Validator:** the composer refuses a manifest whose items cannot fit the bed
before invoking the slicer.
- PASS: a manifest of 9 minis at 40 mm plus 2 standards at 90 mm passes the
  area pre-check and the resulting `.3mf` is accepted by `bambu validate plate`.
- FAIL: a manifest of 4 standards at 130 mm — 4 × 130 = 520 mm of edge in one
  row, which exceeds 256 mm per row twice over while the summed area
  (4 × 130² = 67,600 mm²) is barely above the bed's 65,536 mm² — fails, and the
  hard case is a manifest whose area fits but whose pieces do not tile, which
  the area check alone would pass and only the slicer's arrange result catches.

## 10. Repeatability: ledger, gate, hook, skill

- **Ledger** `docs/constructions/ledger.md`: one row per youtube reconstruction
  id — title, youtube state (attempted / done, read at a pinned youtube git
  ref, the pointer-gate convention), naqsh file, O1/O2/O3 results, coaster STL,
  catalog id, printed. `M60LJNNslHU` (a mechanism with no final piece) is a
  row marked "no piece by design": the by-design failure the gate must not
  skip.
- **Gate** `.claude/gates/constructions_ledger.py` (`make validate-constructions`):
  **fails** on a row whose `.bkr` or STL path is missing; **reports**, without
  blocking, every youtube id without a row (the `20-use-cases` reminder shape).
  Counts `<!--count:constructions-migrated-->` and
  `<!--count:constructions-total-->` pin the two numbers to the tool that prints
  them. A worktree self-test keeps the verdict checkout-independent.
- **Hook** `.githooks/pre-commit.d/38-constructions`, plus a SessionStart line
  "N constructions not yet migrated: …".
- **Skill** `.claude/skills/import-construction/` with a sharp dispatch line
  and a `rubric.md` read at run time (readability rules + fidelity checks):
  pick id → AST → `bikar import geogebra` → readability review → O1 + O2 →
  coaster block → O3 → catalog entry → ledger row → PRs.

**Validator:** the ledger gate fails on a missing artifact and only reports on
a missing row.
- PASS: a ledger whose every `.bkr` and STL path resolves, with two youtube ids
  absent from it, exits 0 and prints the two ids as unmigrated.
- FAIL: a ledger row naming `patterns/Constructions/<id>.bkr` for an id whose
  file was deleted exits 1 naming the row; the hard case is the
  "no piece by design" row, which must pass with no STL because its STL column
  says so explicitly, not because the gate skips empty cells.

## 11. Phases and dependencies

Ids are `P<phase>.<n>`; each is one PR in the named repo, in a worktree; each
task that adds a number ships the test or doc marker that fails before and
passes after. Tier-0 witnesses precede any composite golden.

| Phase | Tasks | Blocks on |
|---|---|---|
| 0 Ground and decide | P0.1 survey · P0.2 this doc · P0.3 decisions D-055…D-063 · P0.4 bikar naqsh-name decision + titles · P0.5 worktrees | — |
| 1 Languages made robust | P1.1 youtube EBNF + conformance + vocabulary fixture · P1.2 `ggb_from_xml.py` · P1.2b `ggb_coords.py` (O1 dump + O3 reference) · P1.3 `--ast-json` + Pydantic schema + bikar mirror · P1.4 naqsh construction statements (a)–(d) · P1.5 bikar printer + round-trip gate · P1.6 `coaster` declaration + height-field kernel + validators + `CAL-CST-*` · P1.7 highlighting generated from the fixtures (bikar + youtube) | P0.4, P0.5 |
| 2 Transpiler, first construction, cookbook | P2.1 `bikar import geogebra` · P2.2 `GimTvN9hw4U` golden + O1/O2 · P2.3 slice-1 coaster · P2.3b `qiyas mesh compare` (O3) · P2.4 readability rules + header · P2.5 cookbook with conformance test · P2.6 `7apC5Q9QS-8` · P2.7 disc coaster | P1.3, P1.4, P1.5, P1.2b |
| 3 Repeatable process | P3.1 skill · P3.2 ledger + gate + hook · P3.3 catalog `CS-*`, `make coasters`, gallery section | P2.5, P2.7, P2.2 |
| 4 Many on one plate | P4.1 `bambu slice compose` + plate doc · P4.2 `docs/plates/minis-01.yaml` · P4.3 print record (owner-gated) | P3.3, P3.2, Plate 1 |
| 5 Scale the corpus | P5.1 remaining rungs in ladder order · P5.2 standard-size plate · P5.3 `frame` decision if a public fixture needs it | P3.1, P4.3, P1.2 |

Critical path to the first mini STL: P0.5 → P1.1 → P1.3 → P2.1 → P2.2 → P2.3,
with P1.4 + P1.5 in parallel and P1.2b alongside (O1 gates P2.2's acceptance,
O3 gates the catalog entry). P1.2, P1.6 and P1.7 are off the critical path.

## 12. Verification, end to end

1. youtube `make test`: grammar conformance, vocabulary fixture, `--ast-json`
   for every construction and snippet, XML round-trip on the nine renders plus
   public fixtures with an enumerated coverage report.
2. bikar `npm test`: G1 sweeping `patterns/Constructions/`, G2 at the new
   count, G3 over the new productions and cookbook fences, printer round-trip,
   Tier-0 witnesses, golden byte-equality, cookbook conformance, highlighter
   alternation equal to the fixture set.
3. Oracles on `GimTvN9hw4U`: O1 every label in tolerance, O2 ≥ the §6 default,
   O3 passes and the dropped-edge variant fails.
4. `bikar render … --format stl --check` for mini and standard, both coaster
   forms; every structural validator's PASS and hard FAIL fixture exercised;
   `make coasters`; `make validate` green.
5. `bambu slice compose docs/plates/minis-01.yaml --dry-run` prints a valid
   multi-input argv; the real run produces a `.3mf` that `bambu validate plate`
   accepts. No print is sent.
6. The gallery's Coasters section renders in a real browser.
7. The ledger hook in a fresh worktree lists every unmigrated id.

## 13. Open and unverified

- Headless STL from GeoGebra (survey §14): not needed; not claimed.
- Whether Bambu Studio's `--arrange 1` places every manifest reliably; the
  first plate answers it and P2 of §4.3 is the fallback.
- The `frame` block (D-061): deferred until a fixture needs it.
- Decision ids: D-055…D-063 assume PRs #182 (D-053) and #183 (D-054) merge
  first; the first-merged PR owns an id and the open one renumbers
  (survey §12).

## Appendix A — sources

All web and tree sources, with fetch dates and what was unreachable, are in
[`research/geogebra-construction-import-survey.md`](research/geogebra-construction-import-survey.md)
§15. Defect kinds referenced by K-number are defined in
[`grounding-defect-taxonomy.md`](grounding-defect-taxonomy.md).
