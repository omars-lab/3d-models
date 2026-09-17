---
name: import-construction
description: Migrate a GeoGebra construction into a naqsh (`.bkr`) file bikar renders to a printable coaster, end to end. Use for "import/migrate this GeoGebra construction to naqsh", "make a naqsh file from this .ggb", "make a coaster from this construction", "do the next construction in the ledger", "add construction <video-id>". Drives the three fidelity oracles (O1/O2/O3) and the readability review, refuses unsupported input loudly, and stops at one bikar PR + one 3d-models PR — it never dispatches a print.
---

# import-construction — a GeoGebra construction → naqsh → coaster

This skill runs the repeatable pipeline the umbrella design owns
([`../../../docs/geogebra-construction-import-design.md`](../../../docs/geogebra-construction-import-design.md)):
a youtube reconstruction's GeoGebra construction becomes a `.bkr` of record in
bikar, is proven equivalent by three oracles, becomes a coaster, and lands in
this repo's ledger and catalog. It advises and verifies; it **never** dispatches
a print (printing is owner-gated, D-060).

The run-time rubric — the eight readability rules, the header convention, and the
per-oracle fidelity checks — lives in [`rubric.md`](rubric.md) next to this file
and is read at each step it names, so it can sharpen without editing this body.

## The boundary — own the process, consume the verbs

Three repos, one job. Do not reimplement across the seam:

- **youtube** owns the GeoGebra front-end and the oracle references: `ggb_from_xml.py`
  (any `.ggb`/`geogebra.xml` → `.ggb-commands`), `ggb_build.py --ast-json` (the
  construction AST), `ggb_coords.py` (the GeoGebra-engine coordinate + polygon dump),
  and the `make naqsh-coords` / `make naqsh-score` / `make reference` verdict targets.
- **bikar** owns the language and engine: `bikar import geogebra` (AST → `.bkr`,
  fails closed), `bikar validate --style constructions`, `bikar render`, `bikar points`,
  the `coaster` kernel, and the source-of-record goldens under `patterns/Constructions/`.
- **this repo (3d-models)** owns the ledger, the catalog, the gallery and the gates.

Work each repo in its **own worktree**, never the shared checkout, one PR per repo.

## When it fires

Any request to bring a GeoGebra construction into naqsh or into a coaster, or to
advance the corpus: "migrate `<id>`", "next construction in the ledger", "make a
coaster from this `.ggb`". If the input is a raw `.ggb`/`geogebra.xml` from anywhere
(not only our reconstructions), start at step 1 — the front-end reads any GeoGebra
file, not just ours.

## The steps

Each step says **what it verifies** and its **PASS/FAIL** shape. The by-design
failures (an unknown command, a free point off the root frame, an ambiguous
intersect) are cases this pipeline **expects** to hit; they are enumerated
refusals, never worked around — see "Failures this skill expects" below.

### 0. Pick the id — from the ledger, unmigrated first, ladder order

Open [`../../../docs/constructions/ledger.md`](../../../docs/constructions/ledger.md).
Take the first row whose **naqsh** cell is `—` (not yet migrated), in the ladder
order the plan fixes (`GimTvN9hw4U`, `7apC5Q9QS-8`, then `rDuxHF3xMOc`,
`tA8eSdVx_EQ`, `sDO9fpu76v8`, `lEfWSogWscs`, `nmEjCTzMbDg`, …). A row marked **no
piece by design** (`M60LJNNslHU`, a mechanism video with no final art) is skipped,
not migrated — it is a complete row that asserts no `.bkr`.
- Verifies: you are building the construction the corpus actually needs next.
- PASS: an id with an unmigrated row (or an explicit `.ggb` the user handed you).
- FAIL: no such row, or the id is the `no piece by design` sentinel — stop and say so.

### 1. Get the AST — front-end first if the input is a GeoGebra file

If the input is a `.ggb` or `geogebra.xml`, lower it to `.ggb-commands` text with
`ggb_from_xml.py` (it fails closed on unknown XML and enumerates the gap under
`--coverage`). Then project the AST with `ggb_build.py --ast-json <out.json>`
(youtube target `make ast IN=… OUT=…`). For our reconstructions the
`construction.ggb-commands` already exists, so start at `--ast-json`.
- Verifies: the construction is captured as the one AST both later stages read
  (a projection of the fail-closed `parse()`, not a second parser).
- PASS: a `construction.json` that validates against the mirrored schema.
- FAIL: `ggb_from_xml.py` aborts on an unhandled XML element (conic, text,
  scripting) — that element is a coverage row, not a silent drop.

### 2. Lower to naqsh — `bikar import geogebra` with `--coverage`

```
bikar import geogebra <construction.json> -o <id>.bkr --coverage
```
`--coverage` prints the per-command histogram to stderr; **read it**. Every command
the importer understands is lowered; every one it does not is a **typed refusal
naming the cookbook gap**, never dropped. A gap is closed by adding a `## Not yet
supported` row to bikar's cookbook (`geogebra-to-naqsh.md`) **and** filing a bikar
engine task — never by `--lenient` (the explicit-drop escape hatch is for a
deliberately out-of-scope decoration, and even then it is enumerated, D-C).
- Verifies: "any GeoGebra file" is honest — the supported set is printed, not claimed (K2).
- PASS: a `.bkr` written; the importer re-parsed its own output before writing.
- FAIL (by design): an unknown command / a free point off the root frame / a single
  `intersect` with ≠1 hit → the importer refuses and names the gap.

### 3. Readability review — `rubric.md` + `bikar validate --style constructions`

Read the emitted `.bkr` against the eight readability rules and the header
convention in [`rubric.md`](rubric.md), then gate the mechanical half:
```
bikar validate <id>.bkr --style constructions
```
which checks the provenance-header order and 64-hex sha256, the two root-frame
lines, and the `<pattern>_scaffold` split.
- Verifies: a person would author this file — names are the presenter's, one
  statement per GeoGebra line, geometry in the scaffold blueprint, numbers only as
  params/degrees.
- PASS: `validate` exits 0 and every rubric rule holds on a read-through.
- FAIL: `validate` names a violating line (exit 1), or a rubric rule fails — fix
  the lowering (or the importer), not the file by hand for a repeatable id.

### 4. Fidelity oracles — O1, then O2, then O3 when a reference exists

Run in the youtube worktree, `BIKAR_DIR` pointing at the bikar worktree whose CLI
has `points`. Details and thresholds: [`rubric.md`](rubric.md) "Fidelity checks"
and [`../../../docs/construction-equivalence.md`](../../../docs/construction-equivalence.md).

- **O1 geometry** — `make naqsh-coords ID=<id> NAQSH=<id>.bkr`. Per authored label,
  GeoGebra's own numbers (dumped through the Apps API) vs `bikar points`, the frame
  divided out, not fitted.
  - PASS: every compared label within tolerance, no label missing or unaccounted for.
  - FAIL: one label out of tolerance (the hard case is a `pick` swap onto a
    mirror-image intersection — only O1 can see it; the drawing is symmetric).
- **O2 drawing** — `make naqsh-score ID=<id> NAQSH=<id>.bkr`. Centreline recall and
  precision of the naqsh render against the hero export, plus the loop's edge-SSIM.
  - **Stale-hero trap:** an old `export.png` can be a stale square that scores recall
    ~0.01. Before trusting an O2 FAIL, rebuild the hero with the loop's own export
    (the reconstruct loop's two commands) and re-run — the youtube issue note
    naqsh-score-stale-hero on `feat/ggb-coords` has the evidence.
  - PASS: recall ≥ 0.98 and precision ≥ 0.98 and edge-SSIM ≥ 0.70.
  - FAIL: any of the three below its floor, named — after the hero is confirmed fresh.
- **O3 solid** — only once a coaster/piece STL and a `.ggb` export exist:
  `make reference IN=<export.ggb> OUT=<dir>` (OpenSCAD, no bikar code), then
  `qiyas mesh compare <dir>/reference.stl <print.stl>`.
  - PASS: coverage ≥ 0.99 and local missing ≤ 1.0 mm (reference-relative, directional).
  - FAIL: a dropped solid region drops coverage / raises local missing; the by-design
    FAIL fixture is the same construction with one `edges from` dropped.

Record only the verdict the validator printed, into the ledger's oracle cells —
never a re-typed summary (an aggregate cannot discharge a per-label claim).

### 5. Coaster + `--check` at both sizes

The importer appends the coaster trailer with `--coaster <Name>` (a height-field
disc, `param size` in mm — mini and standard are two values of one param, never two
files, D-059/D-065). `--piece <Name>` is the flat slice-1 alternative; the two are
mutually exclusive. Render and gate the mesh at both print sizes:
```
bikar render <id>.bkr --format stl --check --param size=40   # mini ≈ 40 mm
bikar render <id>.bkr --format stl --check --param size=90   # standard ≈ 90 mm
```
Dynamic STLs are **re-rendered per `--param`, never mesh-scaled** (D-D: scaling a
mesh scales walls and relief below the FDM floor).
- Verifies: the coaster is watertight and every feature clears the floor at the
  size it will actually print.
- PASS: `--check` exits 0 at size 40 and size 90.
- FAIL: the mesh gate names the thin feature — that is a coaster-validator finding
  (`CAL-CST-*`), addressed in the kernel/params, not by scaling.

### 6. Catalog entry — `CS-<n>` + `make coasters`

Add a catalog entry `CS-<n>` in `.claude/skills/prototype/catalog.md` (the harvested
`--param size` / `--piece <Name>` must name something the `.bkr` declares — hook 36
checks it). `make coasters` renders STL + views for `patterns/Constructions/*.bkr`
and vendors into `src/Coasters/<id>.stl`.
- Verifies: the coaster is reproducible from a checked-in command and vendored for
  the gallery.
- PASS: `make coasters` produces `src/Coasters/<id>.stl`; hook 36 passes.
- FAIL: a catalog knob names nothing in the `.bkr` (hook 36) — fix the entry.

### 7. Ledger row — `docs/constructions/ledger.md`

Fill the row's cells: **naqsh** = `bikar/patterns/Constructions/<id>.bkr`, the three
oracle verdicts (verbatim), **coaster** = `src/Coasters/<id>.stl`, **catalog** =
`CS-<n>`. Then `make validate-constructions` (gate `.claude/gates/constructions_ledger.py`,
hook 38): it FAILS a row whose `.bkr`/`.stl` path does not resolve and REPORTS any
youtube id without a row.
- Verifies: the record matches disk and every migrated construction is accounted for.
- PASS: `make validate-constructions` exits 0; the migrated count moved by one.
- FAIL: a named path does not resolve — the cell is ahead of the merge; land the
  bikar PR first (step 8).

### 8. PRs — bikar first, then 3d-models, pointer gate

Two PRs, in order, because the 3d-models pointer gate resolves backticked
`bikar/patterns/Constructions/<id>.bkr` at bikar's ref:
1. **bikar** PR: the golden `.bkr` (dir in the G1 sweep), its AST fixture, the
   lower+print byte-equality test, any new cookbook recipe.
2. **3d-models** PR: the ledger row, the catalog entry, the vendored STL, the gallery.
Run `make validate` green in the 3d-models worktree before opening. Never merge here;
merges are the owner's.

## Failures this skill expects to hit (D-C)

These are not bugs — they are the enumerated refusals the pipeline exists to make
loud. When one fires, the fix is the named one, never a hack:

| Refusal | Cause | The fix (never a hack) |
|---|---|---|
| unknown command | a GeoGebra command with no lowering | a `## Not yet supported` cookbook row + a bikar engine task |
| free point off the root frame | a free point that is not A (centre) / B (0°) / D (90°) | rewrite the construction relative to A, B (D-G); a `frame` block is a deferred dsl-design decision, only if a real file needs it |
| ambiguous `intersect` | a single `intersect` with ≠1 hit | add `pick <n>` / `pick nearest <P>`; the render-diff (O1) catches a wrong pick |

`--coverage` prints the full supported/unsupported set every run, so the boundary is
always visible rather than assumed.
