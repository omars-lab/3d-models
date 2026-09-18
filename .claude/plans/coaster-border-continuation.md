# Plan: finish the coaster border (task #36), then the open tail

*Written 2026-09-17 after context thrashing on the border implementation. This file is the
continuation of [`iterative-dazzling-finch.md`](iterative-dazzling-finch.md) (the umbrella
GeoGebra → naqsh → coaster plan, still authoritative for architecture, decisions D-A…D-I and the
phase map). Read this file first; open the umbrella only when a phase-level question comes up.*

## 0. Where things stand (verified on disk, not from memory)

| Repo / worktree | Branch | State |
|---|---|---|
| `~/Workspace/git/bikar-border` | `feat/coaster-border` off `origin/main` 5152cfd (#211 minimal coaster) | one commit `f5d1781` (checkpoint, not pushed): `ast.ts`, `parser.ts`, `evaluator.ts`, `coaster.ts` edits + new `coaster-border.ts` and its test (Fable subagent, 12/12). `npx vitest run coaster`: 7 files, 158 tests passing. |
| `~/Workspace/git/bikar-placeborder` | detached at 5152cfd | subagent scratch worktree; its two files are already copied into `bikar-border`. Remove it (`git worktree remove`) after the border PR merges. |
| `~/Workspace/git/3d-models-constructions` | (check with `git branch --show-current`) at 32ca662 | design doc `docs/coaster-border-design.md` merged as 3d-models #257 (D-071). The catalog/gallery slice (CS-5) is not started. |
| `~/Workspace/git/3d-models` (shared checkout) | `feat/x2d-slice-preflight` | **another session's branch — never commit here.** |

Merged inputs the border builds on: bikar #209 interlock (D-069), #210 Coaster Lab (D-067),
#211 minimal (D-070); 3d-models #255 CS-4, #257 border design.

Design of record: `3d-models-constructions/docs/coaster-border-design.md` §3 (solid + worked
table), §4 (grammar + refusals), §5 (kernel), §6 (CV7 re-aim, CV11), §7 (sizing), §8 (importer).
Everything below implements that doc; where the code deviates, the doc changes in the CS-5 PR.

## 1. What is already implemented in `bikar-border` (do not redo)

- **AST** `packages/core/src/dsl/ast.ts`: `CoasterDeclarationNode.border?: { pattern; widthMm }`.
- **Parser** `packages/core/src/dsl/parser.ts`: `border IDENT width <positive>` in the coaster
  dispatch map (contextual identifier `border`, `TokenType.Width`), `taken` guard refuses a
  second `border`. No G2 keyword delta.
- **Evaluator** `packages/core/src/dsl/evaluator.ts`: `resolveBorderCell(decl, patternRegistry)`
  (recentred on bbox like `resolveCoasterArt`; errors "border pattern 'X' is not declared" /
  "has no segments to place"); `coasterSpecFromDecl(..., borderCell)` spreads
  `border: { cell, widthMm }` into the spec.
- **Kernel** `packages/core/src/kernel3d/coaster.ts`: `CoasterSpec.border?: { cell, widthMm,
  placed?, runs? }`; `reliefAppliesAt` region-split on `outlineInset(p) < W` (band art) else field
  art; `refuseBorderConflicts` (border+`outline pattern`, border+`rim`, `h = W−w−t ≤ 0` printing
  all three); `placeBorderOnSpec` calls `placeBorder(outline, cell, W, w, t, pitch)` and returns
  the spec with `placed`/`runs`; `buildCoaster` returns `{ mesh, field, spec: placedSpec }` so
  validators read `built.field.spec.border`.
- **Placement** `packages/core/src/kernel3d/coaster-border.ts` (+ `tests/kernel3d/coaster-border.test.ts`):
  `placeBorder` per the §3 contract. Subagent deviations to carry into the doc: flats use
  `N = max(0, floor(U/ℓ + 1e-9))`; throws `coaster:` on a `pattern` outline **and** on a
  degenerate cell (L or H ≤ 0); round faces are chord-subdivided like straps; mini-hex ground is
  0.2376 (doc said 0.235, a loose rounding — fix the doc's table).

Empirical fact for the stock motif: a `pattern` block with `connect bl.mpt -> ap.mpt` /
`connect ap.mpt -> br.mpt` compiles to 2 drawn segments; `segment` statements compile to 0;
`edges from` needs a polygon. So the importer's chevron is drawn with `connect`.

## 2. Remaining steps for the bikar PR (one PR, `feat/coaster-border`; parallel split in §2b)

Every Bash call: `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"` in the same
command; `cd /Users/omareid/Workspace/git/bikar-border` inside the call (cwd resets); commits
need `THREED_MODELS_DIR=/Users/omareid/Workspace/git/3d-models-constructions`; `git branch
--show-current` before each commit; stage by name.

1. **Validators** `packages/core/src/kernel3d/coaster-validate.ts`
   - CV7 re-aim (design §6.1): `W = spec.border?.widthMm ?? 0`; strap ends need `ι(end) − W ≥ w/2`,
     face vertices `ι ≥ W`. Message unchanged in shape; mention the band inner edge when W > 0.
   - New CV11 `bandPlacement` (design §6.2): add `'CV11'` to `CoasterFindingCode` (line ~33-44)
     and to the `validateCoaster` list (line ~690, after CV10). Without a border: pass, "no border
     band". Checks: (i) every run in `spec.border.runs` has `N ≥ 1`; (ii) every placed band strap
     end has `w/2 + t ≤ ι ≤ W − w/2` and every placed face vertex `t ≤ ι ≤ W`, tolerance one
     grid pitch. Message carries `N` per run and the arc stretch.
   - Order test `packages/core/tests/kernel3d/coaster-validate.test.ts:425` — append `'CV11'`.
   - Tests in `tests/kernel3d/coaster-validate.test.ts`: CV11 pass on the §3 standard hex; CV11(ii)
     FAIL on a hand-built spec whose `placed` straps are forced past the band line; CV7 FAIL for
     the `margin 0.5` case in §6.1.
2. **Eval tests** `packages/core/tests/dsl/coaster-eval.test.ts`: border PASS (hex 90, W 8, chevron
   via `connect`); refusals (border + `outline pattern`, border + `rim`, `W − w − t ≤ 0`,
   undeclared border pattern); CV11(i) FAIL: mini hex 40 with W 8 and an `L = 3H` motif → `N = 0`
   → throws `/CV11/`. Parse tests in `tests/dsl/parser*.test.ts`: accept, reject missing `width`,
   reject duplicate `border`.
3. **Importer `--border`** `packages/core/src/import/geogebra/emit.ts`
   - `CoasterEmitSpec.border?: boolean`; `assertCompatibleTargets`: `--border` + `--minimal`
     exclusive (compatible with `--interlock`).
   - `withCoasterParams` gains a `border` knob (default 8, range 3..15) placed before `margin`, and
     `unit = ($size - 2 * ($border + $margin)) / K`; `paramTrailer` comment for `border`.
   - Emit the stock chevron `<id>_border` (blueprint with three circles at bl/br/apex, pattern with
     two `connect`s) after the construction's pattern and before the coaster block; add
     `  border <id>_border width $border\n` after the `inscribe` line.
   - CLI `packages/cli/src/index.ts` (~L1436 area in dist): parse `--border`, usage lines, the two
     exclusivity errors. Rebuild dist (`npm run build`) before rendering.
   - Goldens `patterns/Constructions/{GimTvN9hw4U,7apC5Q9QS-8}-border-coaster.bkr` generated by
     the CLI; `tests/import/emit.test.ts` new `describe('emit — coaster border (--border, D-071)')`
     mirroring the minimal block at L304 (byte-equal golden, off-path byte-identical, exclusivity).
   - Lab roster `packages/lab/src/coaster-scripts.ts`: two entries `six-fold-rosette-border` /
     `eight-fold-rosette-border` (the presets test pins the roster to `*-coaster.bkr` on disk and
     sweeps sizes 40 **and** 90 at the file's defaults — so the golden's default `border = 8` must
     hold ≥ 1 chevron on the 40 mm hex: U = 23.09 − 2·8·cot60° = 13.85, ℓ = h = 6 → N = 2, fine;
     and on the 40 mm square, U = 40 − 16 = 24 → N = 4).
4. **Docs** (same PR): `docs/grammar.md` §10.3 production (`CoasterBorder = "border" IDENT
   "width" ConstExpr NL`), prose, a `bkr` fence and a `bkr invalid` fence, §12 fence counts;
   `docs/language-reference.md` "Coaster Declarations (3D)" (L1195) + "Constructions" (L1604)
   importer flag; `docs/design/coaster-height-field.md` "Validators" (L146): CV7 re-aim, CV11 with
   `PASS:`/`FAIL:`; `docs/design/coaster-lab.md` roster note. G3 runs on every fence.
5. **Verify**: `npx vitest run` from repo root (full suite); `bikar render <golden> --coaster
   Coaster --param size=40 --param border=4 --format stl --check` and `--param size=90`, both
   goldens; `npm run lint`. Then push, `gh pr create -R NaqshCoffee/bikar`, gitleaks clean, poll to
   green (no `--auto`). If CI is billing-blocked, run the full local suite and report; `--admin`
   only under a fresh explicit authorization from Omar.
6. **Reply to the subagent** is not needed; it is done. Remove `bikar-placeborder` after merge.

Commit trailer: `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` +
`Claude-Session: https://claude.ai/code/session_01KX2J17nHSsa6F9cpuhg3Cv`. PR body ends with
`🤖 Generated with [Claude Code](https://claude.com/claude-code)`, blank line, the session URL.

## 2b. Parallel split: Opus subagents, same branch, their own commits

**Why not literally the same worktree.** Two agents committing in one working tree share one
index and one HEAD; a `git add` from one lands in the other's commit and a checkout mid-edit
loses work. Git also refuses to check the same branch out in two worktrees. So "same branch,
own commits" is done as: each agent commits on a **short-lived branch off the integration
tip** in **its own worktree**, and the main session lands those commits onto
`feat/coaster-border` one at a time with `git cherry-pick <sha>` (single commits, never a
range `A..B`). Author, message and trailer survive; the branch history reads as each agent's
commits in landing order. This differs from the standing rule "one worktree + branch + PR per
task" (`parallel-opus-subagents-in-worktrees`) only in that the pieces land in **one PR**:
goldens, validators and docs must be reviewed together because G3 fences, the presets sweep
and CV11 only make sense as a set.

**Step 0 (main session, before any spawn): checkpoint — DONE 2026-09-17.** The current
state is committed on `feat/coaster-border` as **`BASE = f5d1781`** (`wip(coaster): border band
— grammar, evaluator, kernel region split, placeBorder (D-071)`; all pre-commit gates green,
gitleaks clean, 158/158 coaster tests passing). Every agent branches from `BASE`, so all of
them see the parser, the spec shape and `placeBorder`. Not pushed yet.

**The pieces (file ownership is disjoint; an agent must not touch a file outside its list):**

| Piece | Agent / model | Worktree · branch | Owns | Must not touch |
|---|---|---|---|---|
| **A — validators + tests** (§2 steps 1–2) | Opus | `~/Workspace/git/bikar-border-a` · `feat/coaster-border-a` | `packages/core/src/kernel3d/coaster-validate.ts`, `tests/kernel3d/coaster-validate.test.ts`, `tests/dsl/coaster-eval.test.ts`, the parser test file that holds coaster parse cases | `coaster.ts`, `coaster-border.ts`, `emit.ts`, docs |
| **B — importer `--border`** (§2 step 3) | Opus | `~/Workspace/git/bikar-border-b` · `feat/coaster-border-b` | `packages/core/src/import/geogebra/emit.ts`, `packages/cli/src/index.ts`, `patterns/Constructions/*-border-coaster.bkr` (new), `tests/import/emit.test.ts`, `packages/lab/src/coaster-scripts.ts` | validators, kernel, docs |
| **C — docs + fences** (§2 step 4) | Opus | `~/Workspace/git/bikar-border-c` · `feat/coaster-border-c` | `docs/grammar.md`, `docs/language-reference.md`, `docs/design/coaster-height-field.md`, `docs/design/coaster-lab.md` | any `.ts` |
| **D — 3d-models CS-5** (§3) | Opus, **after B lands** | `~/Workspace/git/3d-models-constructions` · `feat/coaster-border-catalog` off `origin/master` | catalog, Makefile `coasters` target, `index.html`, `DEPLOY_PATHS`, `site-graph.json`, design-doc status, use-case map | anything in bikar |

Independence check: A, B and C share no file. B's goldens must pass every CV at sizes 40 and
90 (the presets test), including A's CV11 once both land — the §2 step-3 arithmetic says they
do (N = 2 on the 40 mm hex, 4 on the square). C's `bkr` fences must parse at `BASE`, which they
do because the parser is in the checkpoint. D reads bikar's goldens through hook 36
(`catalog_models.py`); point it at the `bikar-border` worktree until the bikar PR merges.

**Brief for each agent (the whole context it gets):** this plan file's §0–§2 and its own row;
`BASE`; its worktree path and branch; the exact file list above; the command rules of §2
(PATH prefix in the same call, `cd` inside the call, `THREED_MODELS_DIR` on commit,
`git branch --show-current` first, stage by name); the commit trailer; "run the tests you own
plus `npx vitest run` from the repo root before the last commit"; "do not push, merge, rebase
or touch the integration branch; do not read `.env`; report the commit SHAs, the test output
and any deviation from the design". A subagent that re-reads the same file dozens of times
with no edit is looping (`subagent-loop-signal`): stop it and take a partial deliverable.

**Integration (main session, serial):** for each agent in the order A, B, C: `git
cherry-pick <sha>` per commit onto `feat/coaster-border` in `bikar-border`; on a conflict,
open the file, keep both intents, `git add` it by name, `git cherry-pick --continue` (never
`-X ours`/`theirs`). After all three: `npm run build`, full `npx vitest run`, `npm run lint`,
the two `render --check` commands of §2 step 5, one fix-up commit if anything crosses (e.g. a
CV11 message the docs quote), push, PR. Then spawn D. Delete the three `-a/-b/-c` worktrees and
branches after the PR merges; they are never pushed.

**Worktree commands** (main session, one per agent, from `bikar-border`):
`git worktree add ../bikar-border-a -b feat/coaster-border-a BASE` — then in the new worktree
`npm ci` and `npm run build` (fresh bikar worktrees need both:
`bikar-registry-hook-reads-shared-checkout`).

## 3. Then the 3d-models slice (CS-5), branch off `origin/master` in `3d-models-constructions`

- Catalog `.claude/skills/prototype/catalog.md`: `## CS-5 — Bordered coasters (D-071)` after CS-4
  (L1424); knobs `--param size`, `--param border` (mini: `size=40 border=4`) — hook 36 checks each
  against the golden's `param` block.
- `make coasters` (Makefile L756) already globs `*-coaster.bkr`, so the border goldens vendor
  automatically; the mini render needs `--param border=4` only for the mini id — add a per-stem
  override (a `COASTER_MINI_EXTRA_<stem>` variable or a `case` on `$id`), not a second target.
- Gallery `index.html` Coasters section + JS array; `DEPLOY_PATHS`; `docs/site-graph.json`.
- Design doc status line → "built"; fix the §3 mini-hex ground to 0.2376; note the subagent's
  degenerate-cell refusal in §4. `docs/decisions-log.md` D-071 already exists — re-read the last
  id on `origin/master` before adding any new one (`decision-id-collision-recurred`).
- Use-case map row; `validate.py --refresh`; `make validate` green; PR on `omars-lab/3d-models`.

## 4. Open tail after #36 — every open task, with enough context to start cold

Task ids are the session TaskList ids. Each entry says what is done, what remains, where the
files are, and who gates it. Nothing here depends on the umbrella plan being open.

### #37 — Coaster colour regions → per-body export → filament map (X2D AMS), Coaster Lab knob

Omar's ask (2026-09-17): "will this be part of our coaster lab? color selection?" and "do we have
a 'border' component we compose with a pattern component and can assign colour individually that
translates to different filaments on X2D?" Status: **not today** — bikar colour exists only in 2D
(`edges color`, `palette`, language-reference §7.5); STL carries no colour; a coaster STL is one
body. The border kernel (#36) records the first region split (band vs field in `reliefAppliesAt`),
which is the hook this builds on. Route, in order:

1. **Design doc first** in 3d-models `docs/coaster-colour-design.md` (rubric, options, D-072+;
   re-read the last D-id on `origin/master` before minting). Region vocabulary: `base | straps |
   border`, symbolic names never filament ids — the DSL says what is distinct, the print manifest
   says which spool.
2. **DSL**: `coaster` gains `color <region> <PaletteName>`; grammar §10.3 production + G3 fences;
   parser dispatch (contextual identifier like `border`); evaluator resolves the palette name.
3. **Kernel/CLI**: `bikar render --format parts` for a coaster splits the height field by region
   into watertight bodies sharing coincident faces (slab to z = base; emboss straps as prisms on
   it; the band likewise). Requires **emboss** — deboss leaves nothing to colour (Option A of #33
   already chose emboss). Each body passes `--check` on its own.
4. **Plate composer** (P4.1 below): manifest maps palette name → AMS slot and writes per-object
   `extruder` into the project 3MF. Bambu Studio CLI `--load-filaments` loads profiles; whether
   per-object assignment must already be in the input 3MF is **unverified** — check it in the
   P4.1 research file before building.
5. **Coaster Lab** (`bikar/packages/lab`, Orb Lab pattern, D-067): colour per region is a knob
   that edits the `color` statements (Lego Lab `visibleColours` precedent), preview tinted per
   region.

Depends on #36 merged. The composer part depends on P4.1.

### #12 — Later phases of the umbrella plan (P4.x plate composer, P5.x corpus)

P3.1 (skill, #32) and P3.3 (catalog/gallery/`make coasters`, #31) are **done**; the task's
description is stale on that. What remains:

- **P4.1 `tools/bambu slice compose <plate.yaml>`** (3d-models, `tools/bambu/src/commands/`):
  manifest items `{bkr, piece, params, count}`; render each variant via bikar (cache keyed by bkr
  hash + params); collect STLs; call Bambu Studio CLI with all inputs `--arrange 1 --export-3mf`;
  `--dry-run` prints argv; `--bed x2d` = 256 × 256 mm (D-053) with an area/count pre-check that
  fails before the slicer; per-object provenance `bikar:<path>@<ref>` in the plate record; mesh
  `--scale` passthrough prints the D-D warning (dynamic STLs come from `--param`, never mesh
  scale). Design doc `docs/plate-composer-design.md` (`**Default:**` cites the research file;
  `**Validator:**` PASS/FAIL for the bed check). Existing wrapper: `tools/bambu slice plate`
  handles one model (`slice.ts:22-44,132-149`). Bambu CLI reference:
  https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage . Own 2D packer (P2) only if
  `--arrange` proves unreliable, recorded in `docs/issues/`.
- **P4.2 Mini plate manifest** `docs/plates/minis-01.yaml`: every migrated construction at mini
  size (`size=40`, bordered ones `border=4`), count 2, one relief variant each — the plate after
  Plate 1. `bambu validate plate` must accept the composed 3MF. deps P4.1, and the ledger (#20,
  done).
- **P4.3 Print record** when Omar dispatches: `docs/prints/<date>-minis-01/` through the
  compare-verdict loop (gate R5), settling `CAL-CST-01/02`. **Owner-gated** — nothing dispatches
  a print; the X2D dispatch (#9) is itself CAL-gated.
- **P5.1 Remaining constructions** in ladder order: `rDuxHF3xMOc`, `tA8eSdVx_EQ`, `sDO9fpu76v8`,
  `lEfWSogWscs`, `nmEjCTzMbDg` — each via the `import-construction` skill
  (`3d-models/.claude/skills/import-construction/`), adding cookbook recipes for new commands
  (`bikar/docs/cookbook/geogebra-to-naqsh.md`, conformance test) and a ledger row
  (`docs/constructions/ledger.md`, gate `constructions_ledger.py`). Conics (`Parabola`,
  `Hyperbola`, `CircularArc` beyond the `arc` family) are engine tasks filed, not faked.
- **P5.2 Standard-size plate** once `CAL-CST-*` are measured (after P4.3).
- **P5.3 `frame` block** for arbitrary free points, only if a public GeoGebra fixture needs it
  (D-G: free points are root-circle aliases `A`/`B`/`D`; anything else is a transpile error).

### #17 — O1 + O2 verdict scripts on youtube `feat/ggb-coords` (not on main)

youtube `feat/ggb-coords` (bf5e1de; earlier b969f4b, 3f03b7f) ships `make naqsh-coords` (O1,
per-label geometry via the GgbAPI dump), `make naqsh-score` (O2, edge-SSIM vs the hero
`export.png`), `make coords`, `make reference` (O3 reference STL via OpenSCAD). Verified
2026-09-17 against the bikar PR #200 golden with `BIKAR_DIR=bikar-import`: O1 PASS 23 compared /
0 failed / 17 skipped-or-extra (auto segments, Sequence lists, two lowering conjugates); O2 PASS
edge-SSIM 0.9831 (min 0.70), recall 1.0, precision 1.0 (min 0.98). **youtube commits to `main`
only when Omar says so**; branches awaiting that word: `feat/ggb-coords`, `feat/ggb-from-xml`
(6354329, P1.2 XML front-end), `feat/ggb-highlight` (ed04bbe, P1.7 youtube half). When asked:
rebase each on `main`, run `make test`, merge, delete the branch.

### #21 — Push bikar CI secrets (`make setup-secrets`) — owner-gated

Script `scripts/setup-secrets.sh` and the Makefile target are shipped in bikar; they pipe
`dotenvx get <NAME> -f .env` into `gh secret set` so values are never displayed. The Cloudflare
deploy check on bikar `main` stays red until the secrets land (only `ci`/`e2e`/`gitleaks` are
required checks, so merges are not blocked by it). **Do not run it until Omar writes "push".**
Never read `.env` in chat; shape checks return booleans only.

### #24 — `session-reflect` skill (after Omar reviews 3d-models design PR #218)

Build per `docs/session-reflection-design.md` §4–§9: `tools/session_reflect.py` with verbs
`census` / `update-faq` / `show` (`--audit`), walking the main transcript **and**
`<session>/subagents/agent-*.jsonl` (subagent transcripts are separate files; bikar's
`transcript.py` misses them); `docs/faq.md` (`## Q-NNN`, answer with an anchored
`repo:path:L<n> "literal"` pointer, a metrics line sessions·occ(authored)·first·last, an evidence
key) + `docs/faq-evidence.jsonl`; `faq-*` count authority registered in
`.claude/gates/counts_gate.py`; two fixture transcripts + `census --self-test` (PASS: a planted
re-derivation surfaces; FAIL: an answered entry with continuing recurrence is flagged "answer not
taking"); `validate-reflect` target at the **end** of the Makefile; `.claude/skills/session-reflect/
SKILL.md` with a sharp dispatch `description`. First real `update-faq` run has Omar writing or
accepting the answers for the top clusters (Node PATH, gates/CI, gh-pages, use-cases hook,
secrets, D-id collisions, worktrees, npm ci, THREED_MODELS_DIR). Open questions from §12: mint
`CAL-LOOP-01`; port the subagents-subtree fix to bikar's `transcript.py`. **Start only after
Omar reviews #218.**

### Housekeeping after the border merges

- `git worktree remove ~/Workspace/git/bikar-placeborder` (subagent scratch, nothing uncommitted
  worth keeping once the two files are in the PR).
- Update TaskList: #36 → completed with the PR numbers; #12 description → drop P3.1/P3.3.
- Memory: a `feedback` note that the hybrid worked (Fable subagent for the isolated geometry in
  its own worktree, main session integrates and commits) if Omar confirms it.

## 5. Standing constraints (the ones that bit this session)

- Prefer Bash (`cat`/`sed`/`grep`/python heredoc) for reads and edits; AskUserQuestion only for a
  one-way door. Delegate hard, separable pieces to a **Fable** subagent in its own worktree; the
  main session integrates and commits serially (`parallel-opus-subagents-in-worktrees`).
- Never `--force-with-lease`, `--no-verify`, `--auto`, range cherry-pick, `git merge
  origin/master`, headless `claude -p`. Work conflicts by hand. Never base a PR on an open PR's
  branch.
- macOS: no `timeout`; foreground `sleep` chained with `&&` is blocked; quote zsh globs; BSD sed
  has no `,+Np`; vitest from the bikar repo root.
- Secrets: never read `.env`, never print a value; shape checks return booleans only.
- Printing stays owner-gated (no CAL bet settled); the border adds no bet (design §7).
