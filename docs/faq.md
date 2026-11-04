# FAQ — the questions sessions keep re-deriving

Every entry here answers a question that the transcripts show sessions working
out from scratch, again and again. An entry is added only when that repetition
has been measured; nobody adds one on a hunch. Each answer is then held to a
test: once it ships, do later sessions stop re-deriving the fact? The design,
and why this is a measured FAQ and not a hand-kept register, is in
[design/process/session-reflection-design.md](design/process/session-reflection-design.md).

Questions tracked: 5 <!--count:faq-questions-->

## How an entry gets here

1. `python3 tools/session_reflect.py update-faq` reads the transcripts and
   writes a proposal next to this file: candidate questions, each with how many
   sessions worked it out and a ready evidence line. It never edits this file.
2. A person reads the proposal and merges, splits or throws away candidates.
   For each one kept, they write the answer themselves.
3. The accepted entry goes below, and its evidence line goes in the sidecar,
   `docs/faq-evidence.jsonl`, with `answered` set to the day the answer ships.
4. `python3 tools/session_reflect.py show --audit` (also `make validate-reflect`)
   re-measures every answered entry. If sessions after the answer still work the
   fact out as often as before, the entry is flagged "answer not taking" and
   reopened.

## Entry shape

Each entry is a level-two heading of the form "Q-NNN — the question", with a
stable three-digit id so links to it survive edits. Under it:

- **Answer.** Written by a person, never by the tool. It names where the fact
  lives with an anchored pointer (repo, path, line and literal), so an answer
  that drifts from the code is caught by the use-case validator.
- **metrics:** the line the proposal supplies: distinct sessions, occurrences
  (authored and total), and the first and last date seen.
- **evidence:** the entry's id in the sidecar, which keeps the full list of
  session and line pointers behind the metrics.


## Q-001 — Where is SCHEMA_VERSION, and which one is the contract?

**Answer.** The version of the qiyas encoding contract is the `SCHEMA_VERSION` constant in qiyas, at `qiyas:src/qiyas/schema.py:L70 "SCHEMA_VERSION ="`, and `qiyas:tests/test_schema.py:L231 "assert SCHEMA_VERSION =="` holds the number so a bump cannot go unnoticed. qiyas has several other constants with the same name (hier_diff, zone_audit, raster_diff, mesh_compare, baseline, svg_audit); each versions that tool's own report file, not the contract. bikar defines no `SCHEMA_VERSION`. Its separate number is `GT_SCHEMA_VERSION` at `bikar:packages/core/src/render/gt-emitter.ts:L514 "export const GT_SCHEMA_VERSION"`, which versions `gt.json` and moves on its own; the two are independent. 3d-models only cites both. The qiyas pointer is checked at the qiyas commit the use-case map pins.

- **metrics:** re-derived in 5 sessions (after a failure 0, by searching 8, already knew it 0) · used in 5 · occ 8 (authored 8) · first 2026-07-29 · last 2026-09-10
- **evidence:** `Q-001` in `docs/faq-evidence.jsonl`

## Q-002 — Where is BIKAR_DIR set, and what is its default?

**Answer.** `3d-models:Makefile:L35 "BIKAR_DIR ?="` sets it with `?=`, so the environment can point it elsewhere without putting it on every command line; the default is `~/Workspace/git/bikar`. The Makefile builds the `BIKAR` command (the built CLI inside that checkout) from it and passes it to every gate that reads bikar: `.claude/gates/doc_pointers.py`, `.claude/gates/catalog_models.py`, `.claude/gates/prints_gate.py`. The bambu tool reads the same variable with the same default at `3d-models:tools/bambu/src/backends/bikar.ts:L21 "process.env.BIKAR_DIR"`, and `tools/cookbook_render.py` does too. bikar itself never reads `BIKAR_DIR`; the variable that points the other way, from bikar back here, is `THREED_MODELS_DIR`.

- **metrics:** re-derived in 4 sessions (after a failure 0, by searching 5, already knew it 0) · used in 4 · occ 5 (authored 5) · first 2026-08-01 · last 2026-09-17
- **evidence:** `Q-002` in `docs/faq-evidence.jsonl`

## Q-003 — Where is patternSources, the published pattern count?

**Answer.** In bikar's public-surface manifest, at `bikar:packages/web/public-surface.json:L122 "patternSources"`: a `count`, a `countedFrom` naming `bikar:patterns/index.json:L1`, and a `why` paragraph for each bump, all under `publishedOnPublicHosts`. The count is held by `bikar:packages/web/tests/public-surface.test.ts:L106 "patternSources.count"`, which recomputes it from the manifest and fails on a stale number, and bikar's pre-commit hook wants the bump in the same commit as the new `.bkr`. Nothing in 3d-models defines it; the design docs here only cite a bump.

- **metrics:** re-derived in 4 sessions (after a failure 0, by searching 6, already knew it 0) · used in 4 · occ 6 (authored 6) · first 2026-08-02 · last 2026-09-17
- **evidence:** `Q-003` in `docs/faq-evidence.jsonl`

## Q-004 — Where is tagSegments defined?

**Answer.** It is a method on the evaluator's environment, at `bikar:packages/core/src/dsl/environment.ts:L549 "tagSegments("`. Every command that produces segments pushes them through it with a source id and class name, so provenance tags come from one place. The one exception is `connect arc`, which bypasses it, stated in the source at `bikar:packages/core/src/dsl/evaluator.ts:L7856 "bypasses tagSegments"`. Nothing in 3d-models defines it; the click-to-source design doc here only cites it.

- **metrics:** re-derived in 4 sessions (after a failure 0, by searching 6, already knew it 0) · used in 4 · occ 6 (authored 6) · first 2026-07-29 · last 2026-08-31
- **evidence:** `Q-004` in `docs/faq-evidence.jsonl`

## Q-005 — Where is FILL_ATTRIBUTES, the set of fill selector words?

**Answer.** A private static set on bikar's parser, at `bikar:packages/core/src/dsl/parser.ts:L6466 "FILL_ATTRIBUTES = new Set(["`. The error message for an unknown attribute is derived from the set, so the list it prints cannot drift. Adding a selector word touches more than one site: `IDENTIFIER_RHS_ATTRIBUTES` in the same file, at `bikar:packages/core/src/dsl/parser.ts:L6506 "IDENTIFIER_RHS_ATTRIBUTES"`, when the right-hand side is a name rather than a number, and the resolver table at `bikar:packages/core/src/theme/fill-resolver.ts:L250 "const ATTRIBUTE_RESOLVERS"`. Nothing in 3d-models defines it; the multicolor-constructions design doc here only cites it.

- **metrics:** re-derived in 3 sessions (after a failure 0, by searching 4, already knew it 0) · used in 3 · occ 4 (authored 4) · first 2026-07-29 · last 2026-08-14
- **evidence:** `Q-005` in `docs/faq-evidence.jsonl`
