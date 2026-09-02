# Working plan — what we are working against

Last updated: 2026-09-02 (2.13 studio status page shipped). This is the **index of record** for active work across the
three repos: objectives, the priority queue, what shipped, what the audits found, and
where everything lives. It is a pointer document — a number or a design detail lives
in the doc that owns it and is linked from here, never re-typed. The live task list
mirrors §2; when the two disagree, fix whichever is stale in the same PR.

Rules this file follows:

- **Stable ids only.** Rung ids, `CAL-*` bets, D-numbers, PR number + sha. Task
  numbers are session-scoped and never appear here.
- **Every ship updates this file** in the PR that ships it (§2 row state, §3 row).
  A PR that moves a §2 row and does not touch this file is not done.
- **Pointer, not copy.** Owning sections: [`d3-integration-design.md`](d3-integration-design.md)
  §4 (phases) and §5 (decisions); [`rosette-pin-explorer-design.md`](rosette-pin-explorer-design.md)
  §6 (tracks), §6.5 (priority order), §6.6 (open ledger); [`backlog.md`](backlog.md)
  (print-gated sequence, §6.4 the d3 pointer); [`decisions-log.md`](decisions-log.md).
- The older `.claude/plans/*.md` files are plan-mode transcripts of shipped work
  (mural, calibration, lab) and are historical, not this file's competitors.

---

## 1. Objectives, ranked

1. **The d3 stream** — bikar-studio instruments that run the *real* kernel and, next,
   show qiyas's verdict on top of bikar's own render. The reason it ranks first: it is
   the only stream that needs nothing but work, and each phase answers a question the
   next one spends effort on (d3 doc §4).
2. **Publish the bikar/qiyas contract + JSON schema** — pending the user's call on
   where and how (memory: contract v1.5 accepted, mirrors cascaded).
3. **The first physical print** — printer-gated. Sequence and what each plate unblocks:
   [`backlog.md`](backlog.md) §2; record format: [`prints-tab-design.md`](prints-tab-design.md).
4. **Keep the house honest** — gates green, memory an index, branches clean, this file
   current. Not a project, a standing obligation (§4 records what happens when it lapses).

## 2. The priority queue

State marks: 🟢 shipped · 🔵 live (being built) · ⚪ unblocked, queued · 🟡 pending user ·
🔴 gated (printer or external).

| # | Item | State | Gate | Owner section |
|---|---|---|---|---|
| 2.1 | **d3 Phase 2 — the full orb-view instrument.** One bikar orb `.bkr` compiled in the browser → one orb-view SVG (the same one the core renderer emits, faces carrying their index) → qiyas encodes that exact SVG as *ref* and a deliberately degraded copy as *recon* → `/diff` → a status mark per shape overlaid on the bikar-rendered SVG, joined by id. Chosen 2026-08-31 over the fixture-only and 2D-only slices. **Shipped 2026-09-01** as `/orb-instrument` — bikar #129 `d524766`, qiyas #26 `95dd893`, bikar #132 `7824e12`. | 🟢 | — | d3 doc §4 Phase 2, §5 Q-DATA |
| 2.1.a | Orb-view SVG from an orb source inside the studio. **Mapped 2026-09-01:** the chain is four public core exports — compile to geometry, `symmetryViewAxes`, `projectOrbViewScene`, `renderOrbViewSVG` — already driven by the editor one view at a time; sixteen orbs are bundled, Star-Orb is the smallest (three views: `vertex-5`, `face-3`, `edge-2`); every face carries `data-face-index`, unique **per view** (restarts at 0 per view), so the join key is (view id, face index). Shipped as `orbViewSvgs` (bikar #129 `d524766`) | 🟢 | — | `bikar:packages/core/src/render/orb-view-renderer.ts`, `bikar:packages/web/src/main.ts` |
| 2.1.b | Getting a browser-rendered SVG *into* qiyas. **Mapped 2026-09-01:** only `POST /deconstruct` takes inline bytes (multipart `file`, `.svg` allowed) and returns an Encoding; `/encoding` and `/diff` take server-side *paths*, so nothing today diffs two browser-held renders. The studio's same-origin proxy already streams any method and body. Decision to make: add a `POST /diff` that takes two Encodings inline (mirrors the CLI's `diff` of two encoding files, and is the second consumer D-API-4 said would justify a route) vs write both SVGs to a server workspace path. Tests use a checked-in Encoding + Diff pair either way. **Decided and shipped:** `POST /diff` with two inline Encodings, D-API-5 (qiyas #26 `95dd893`) | 🟢 | — | qiyas `qiyas:src/qiyas/review/server.py`; studio proxy `bikar:packages/web/functions/api/qiyas/[[path]].js` |
| 2.1.c | The join: `/encoding(ref)` + `/encoding(recon)` + `/diff` → `{id, x, y, status}` honouring the **two id namespaces** (ref-side buckets join on the ref encoding, `extra_in_recon` on the recon encoding). **Re-measured on orb faces before building:** centre-in-face is not bijective (concave faces); the ring's vertex set is, 55/55 at 0.0 deviation — that is the key `qiyas-join.ts` uses (bikar #132) | 🟢 | — | d3 doc §4 Phase 2 |
| 2.1.d | The page: `/orb-instrument` cloned from the rosette explorer's shape — plain shell, d3 owns the SVG interior, one status-mark join in the separable `viz-d3` module keyed by qiyas id; core stays d3-agnostic. Shipped (bikar #132 `7824e12`); verified live in Chrome against a local qiyas on three views and a second orb | 🟢 | — | bikar decision 2026-08-31 d3 viz adapter |
| 2.1.e | Registration — five real touch points (html file, page marker meta, `PAGE_ROUTES`, rollup input, routing test; there is no site nav and the public-surface file lists hosts and env keys, not pages) + tests that fail without the join, DOM-free like the package's other tests + a checked-in Encoding/Diff fixture pair so the suite needs no server. Shipped in the same PR, plus a catalogue entry the public-surface test demanded | 🟢 | — | `bikar:packages/web/vite.config.ts`, `bikar:packages/web/tests/routing.test.ts` |
| 2.1.f | Record it: d3 doc §4 Phase 2 → shipped, backlog §6.4 row, §3 here, memory shipped-record bullet | 🟢 | — | this file (3d-models #129) |
| 2.2 | Explorer open ledger — widen the roster (6.6.1 🟢 2026-09-01, bikar #134 `85269ac`), ground the explorer doc (6.6.2 🟢 2026-09-01, 3d-models #136), plates as data (6.6.3 🟢 2026-09-02, bikar #141 `571cba2`), interior-tube cap (6.6.4 🟢 2026-09-02, bikar #143 `a4318c9`). **All four unblocked rows shipped**; what remains in §6.6 is gated on a download, a decision, or a printer | 🟢 | — | explorer doc §6.6 |
| 2.3 | Memory decomposition — `islamic-orb-project.md` was one 152 KB file; split by topic into one-fact files, the dated ship log archived verbatim. **Shipped 2026-09-02** (3d-models #145): 25 topic memories + a hub overview, each ≤2.5 KB with `name:` = filename and every `[[link]]` resolving; the log is `docs/research/shipped-record.md` (under `research/` for the pointer-gate and D4 exemptions, not root `docs/`) | 🟢 | — | §4.2 below |
| 2.4 | d3 Phase 3 — unify the vocabulary across the explorers and sacred-patterns (Q-VOCAB). **Shipped 2026-09-02**: A↔B renamed and joined on a shared `faceKey` (bikar #151 `1083046`); sacred-patterns grown a face-list + `<path class="face">` data-join in place of imperative `<polyline>`, pixel-identical (sacred-patterns #45 `76e3c17`). All three surfaces now read `index`/`polygon`/`ring`/`faceKey`/`joinFaces` (D-050) | 🟢 | — | d3 doc §4 Phase 3 |
| 2.5 | Publish the contract + JSON schema | 🟡 | user: venue and versioning | qiyas `contract/schemas/`, sacred-patterns canonical v1.5 |
| 2.6 | coffee-house-sites issue 1 | 🟡 | user | that repo |
| 2.7 | First physical print — machine card, LEGO ladder, W-series, orb ladder; prints-tab rungs S2 and S4 (S3, S5–S7 shipped) | 🔴 | a Bambu-class printer | backlog §2–§3, prints-tab doc |
| 2.8 | Explorer printer-held rows (3.3, 3.4, 4.3) | 🔴 | printer | explorer doc §6.5 item 5 |
| 2.9 | bikar's generated qiyas schema types lag qiyas: `Scores` lacks `drop`/`surplus`/`max_drift` that `POST /diff` returns. Regenerate from qiyas at `95dd893`, and gate the generator so the drift cannot recur (found building 2.1.d). **Shipped:** re-vendored byte-identical, `Scores` and `Contour` both (bikar #145 `cdc0331`, package 0.3.0 unpublished — the `schema-v0.3.0` tag is the owner's); the orb instrument reads the scores instead of deriving them; the schema-mirror gate here (hook 41, `make validate-schema-mirror`) diffs bikar's copy against qiyas's export at the map's pins | 🟢 | none | bikar `packages/qiyas-schema`; `.claude/gates/schema_mirror.py` |
| 2.10 | **Fourth orb on the M4c quantized lattice walk**, built as the measurement for the process: every stop an earlier orb also needed is logged and labelled *detector* (becomes a gate or test in the same PR) or *instruction*; an orb skill is written only if the instruction list is non-empty when the orb ships. **Shipped** as the 18-wheel **open shell** (owner's chosen shape) via `place rule latticewalk`: kernel (bikar#153), DSL seam + sweep predicate (bikar#154), 3d-models record + `make orbs` skip (this PR). **Eight detectors, zero instructions → no orb-creation skill** ([D-051](decisions-log.md)) | 🟢 | none | D-049 §5, maclado doc, skill-evaluation precedent |
| 2.11 | **Flat→sphere wrap morph** for the breakdown page — design doc **shipped** ([`orb-wrap-morph-design.md`](orb-wrap-morph-design.md): the bend is a radial lerp `projectFacePolygon` already holds both ends of, stages draw faceted, `morph` frames inflate to the untouched `complete`, two byte junctions + a count rule for the gate); next one bikar PR (kernel `t`, `writeMorph`, caption) then one 3d-models PR (gate rules, `make orbs`) — **both shipped** (bikar#149, 3d-models#148; gate rule T8) | 🟢 | none | D-049 §2, timelapse doc |
| 2.12 | **Decision hub** — the cross-repo ledger script (sacred-patterns' cross-repo generator, *not* bikar's within-repo one) indexes this repo's `## D-0xx` headings as links, nothing copied; the cross-repo citation check blocks on a D-number that resolves in neither this file's headings nor bikar's decisions tree. **Shipped** (sacred-patterns #44 `a89f45a`): index section + citation gate + 20 test assertions; the block fires in sacred-patterns' own pre-commit and `make local.ci`, and bikar's pre-commit runs it as a non-blocking NOTE | 🟢 | — | D-049 §3, D-004 |
| 2.13 | **Studio status page** — three facts read from files, none typed: bikar commit the gallery was built from, use-cases `as_of` pins, last deploy; rendered like the studio index, with a test holding it to the filesystem. **Shipped 2026-09-02** (3d-models #156): `status.html` at the gallery root (a 3d-models page, **not** a bikar lab page — all three facts are this repo's provenance and would be meaningless on bikar's own studio deploy), reading `status-manifest.json` that `build/status_manifest.py` writes from `build/bikar-ref.txt` + the map's `as_of` + the `gh-pages` tip; each absent source is a named null, and the generator's `--self-test` builds a real fixture repo and asserts every fact — and every zero-state — against disk. `make validate-status` runs it as a `hook_parity` EXTRA (no staged trigger, so no hook); UC27 + G.status added | 🟢 | none | D-049 §4 |
| 2.14 | **Rosette-N sweep record** — the three parked value-triples plus the working tree as a table beside the pattern in bikar (`patterns/Rosettes/Rosette-N.sweep.md`, bikar #142 `6bcf5c5`, corrected #144 `56ab23b`); stashes dropped and the working tree reverted 2026-09-02 after re-reading each against the table | 🟢 | none | D-049 §6 |

## 3. Shipped — this stream, newest first

| Date | What | Where |
|---|---|---|
| 2026-09-02 | **The gallery now shows what it was built from, and cannot say what the files do not** (2.13). `status.html` renders three provenance facts read from files and typed by nobody: the bikar commit the gallery was built from (`build/bikar-ref.txt`), the `as_of` pins the use-case map was last checked against, and the last deploy (the `gh-pages` tip's own subject line — so the page is one deploy behind by construction and says so). `build/status_manifest.py` reads those three sources and writes `status-manifest.json`, dependency-free so a git hook's `python3` can run it; its `--self-test` builds a real fixture repo (master + gh-pages commits) and asserts every fact, and every *absent-source* null zero-state, against disk. A 3d-models page, not a bikar lab page — the D-049 §4 owner call — because all three facts are this repo's provenance; `make validate-status` runs the self-test as a `hook_parity` EXTRA (its three inputs are files other gates own, so a commit here has no staged trigger to hang a hook on). Wired end to end: UC27 + G.status/edge, and the S7 index-link shift (Status added below Prints) re-paid across `site-graph.json` and the map's index.html anchors | 3d-models #156; [D-049](decisions-log.md) §4 |
| 2026-09-02 | **The fourth Family-3 orb shipped as an open shell, and the build measured its own process** (2.10). The 18-wheel lattice walk (owner's chosen shape) reaches the DSL as `place rule latticewalk length <n> start <k>` — a one-word keyword forced by the lexer, an open-mouth pierced bowl hemmed at the rim. It is the only orb that declares `orb3d` yet has neither cell nor ribbon views, so `render --format views` exits 1 on it: skipped in bikar's sweep by the finer `drawsOrbViews` predicate (graduated from `declaresOrbViews`) and reconciled by the `orb-composites` SWEPT/MESH_ONLY partition, and skipped in this repo's `make orbs` publish loop by a sibling branch that keeps the fail-closed `else`. Every build stop was logged: **eight detectors, zero instructions**, so by D-049 §5 **no orb-creation skill is written** — the outcome the two skill-evaluation precedents predict. Printing stays HELD | bikar #153, #154 `1b2098e`; 3d-models #155; [D-051](decisions-log.md) |
| 2026-09-02 | **The flat drawing now visibly bends onto the sphere, and a gate proves it** (2.11). `projectFacePolygon` already held both ends of the bend (`flat` on the chord plane, `dir` on the sphere, collinear through the centre), so the morph is a radial lerp needing no new geometry; the CLI writes a run of `morph` frames between the faceted tiling and the untouched `complete`. The gate rule **T8** checks the run is a bend and nothing else — J1 (starts on the last tiling frame, highlight neutralised), J2 (ends on the cells `complete` frame the wrap lands on, never `frames[-1]` — the weave family's `frames[-1]` is the ribbon terminal), N (polygon count never moves), plus even blend spacing and `data-blend` only on interior frames. The design's §3.6/§6 prescription to add `morph` to `CONTAINED_KINDS` was corrected in place: at `t = 1` the cells are spherical and burst the faceted base outline by the very overhang T7 catches, so morph stays in `STAGE_KINDS` only. `make orbs` also made robust to STL-only round-pattern orbs (#79). Self-test green on all 16 T8 cases incl. the weave family; gate green on all 14 real breakdowns | bikar #149; 3d-models #148 `00f8bdf` |
| 2026-09-02 | **The 152 KB memory file became 26 one-fact files** (2.3). `islamic-orb-project.md` was a single growing file mixing durable tenets with a dated ship narrative. Split into a hub overview + 25 topic memories (each ≤2.5 KB, `name:` = filename, every `[[link]]` resolving), and the dated log archived verbatim to `docs/research/shipped-record.md` — `research/` so the pointer gate and D4 leave the historical sibling refs and superseded numbers alone; one character is non-verbatim (a `**Validator**:` colon moved out of the bold so D2's whole-tree marker scan skips the archived line), noted in the file's own header | 3d-models #145 |
| 2026-09-02 | **Decision hub joined — the cross-repo ledger indexes this repo's decisions and gates citations** (2.12). sacred-patterns' cross-repo generator now reads this file's `## D-0xx —` headings at its origin ref and renders a links-only index; a `D-0xx` cited in any of the four repos that resolves to neither a heading here nor a file in bikar's decisions tree blocks the generator (write refuses, `--check` blocks). The hub is sacred-patterns', not bikar's within-repo generator; bikar's pre-commit calls it as a non-blocking NOTE. 20 test assertions incl. two regression witnesses: test-file fixtures excluded from the citation scan, and the suite is hermetic under a git hook | sacred-patterns #44 `a89f45a`; D-049 §3 |
| 2026-09-01 | **The vendored schema is a claim too — bikar's qiyas contract mirror re-vendored and gated** (2.9). bikar's copy of qiyas's exported JSON schemas lagged by two stems (`Scores` without `drop`/`surplus`/`max_drift`, `Contour` without its ribbon fields) with every check in both repos green, because nothing compared copy to source. Re-vendored byte-identical from qiyas `95dd893`, types regenerated, the orb instrument's score table now reads the seven fields off the diff; and a 3d-models gate reads both schema directories at the use-case map's pinned commits and names the def and fields that differ — its live first run found the second stem. Self-test: fixed fixtures plus a tempdir primary + worktree + siblings agreeing on a *failing* verdict | bikar #145 `cdc0331`; 3d-models `.claude/gates/schema_mirror.py`, hook `41-schema-mirror` |
| 2026-09-02 | **Branch protection applied on both repos** (D-048's setting, on the owner's go-ahead) and **six owner decisions recorded in plain words** — protection, the wrap morph, the decision hub, the status page, the fourth orb and its skill question, the Rosette-N stashes; each with the options as offered and the rule it runs under | D-049; §2 rows 2.10–2.14 |
| 2026-09-02 | **Explorer tube cap — a dial that cannot cross the kernel's floor** (6.6.4) — *Pin count* caps anchors per piece, verdict re-run on the capped set, census counts clutch lobes and capped rings under the kernel's own caveat; retention is thickest-wall-first so a cap can only raise a piece's thinnest wall (test: never fails a kernel pass; at 16 studs at least one thin-anchor fail passes capped). Closes the explorer ledger's unblocked rows | bikar #143 `a4318c9`; 3d-models #141 |
| 2026-09-02 | **Explorer plates are data, gated at load** (6.6.3) — `PLATES` → `data/plates.json` `{id, studs, mm, brand}`; `loadPlates` refuses a duplicate id, non-integer studs, a nominal plate whose mm ≠ 8 × studs, or a default naming no plate; select populated from the roster; verified in Chrome | bikar #141 `571cba2`; 3d-models #138 |
| 2026-09-02 | **CLI mesh gate covers sphere orbs, and reads the right flag** — the widen (peer) fired on `base sphere` orbs; measured against the welded pair it failed the by-design case and broke `make orbs`; the gate now reads per-cap closure like the evaluator and prints both flags. Design doc §6.1, D-047 resolution note | bikar `adb4e8c`, `8a01836` |
| 2026-09-02 | **Direct commits on main/master refused by hook** in both repos; branch protection measured absent (404) and left to the owner with the command written down (D-048). Also: the hook-env parity test masked the ahead/behind count that a concurrent session was moving | bikar #136 `4ac089b`; 3d-models #131 `04f2137` |
| 2026-09-02 | **d3 Phase 3 shipped (Q-VOCAB)** — one face-list vocabulary across all three d3 surfaces: A↔B renamed (`faceIndex`→`index`, boundary-holding `ring`→`polygon`) and joined on a shared `faceKey`; sacred-patterns grown a `faceConstructs()` mapper + a `joinFaces()` `<path class="face">` renderer, pixel-identical (259 faces, 2479 coordinate pairs, frozen golden). The K7 the build caught: convergence at the join is the shared `faceKey`, not routing B's status join through A's path-creating `joinFaces()` (D-050) | bikar #151 `1083046`; sacred-patterns #45 `76e3c17`; 3d-models #150 |
| 2026-09-02 | **Prints tab S7** — `prints.html` vendored into the gallery from bikar's lab page; `prints_manifest.py` writes the register from `docs/prints/*/index.md` through the gate's own parser (an honest zero today); UC24; bikar's `ci` fixed first (rasterizer missing on ubuntu-latest, red on main for four runs) | bikar #130 `e5ccb4f`, #131 `eef7587`, #133 `26c3d6f`; 3d-models #130 `e3f8e11` |
| 2026-09-01 | **Explorer doc grounded** (6.6.2) — audit checked in, Appendix A/B, every empirical residue clustered under an existing `CAL-*` bet. Killed a K1 hardening ("measured 0.00 mm" for an unprinted coupon), a misread pitch-drift figure, a phantom 4.8-vs-5.0 source split, a K2 novelty claim and two wrong PR shas | 3d-models #136 |
| 2026-09-01 | **Gates give one verdict from any checkout** — self as_of pinned at the published base so a squash merge cannot orphan it; doc_pointers, docs_gate D1 and the use-case validator retry beside the primary clone from a linked worktree; skipped ≠ resolved in the stale-baseline check. Found while landing 6.6.1 from a worktree: FAIL(4) there, OK from the primary | 3d-models #132 `44fba5c`, #133 `b7a8908` |
| 2026-09-01 | **Explorer roster widened to six** (6.6.1) — girih, hex-field and square-tiling figures join Rosette-N/Star-N, one per Lego Lab §5.3 lattice row; off-origin tilings recentred in the page, stage framed from the declared span | bikar #134 `85269ac`; 3d-models #134 |
| 2026-09-01 | **d3 Phase 2 shipped** — `/orb-instrument`: orb view rendered in the studio, encoded and diffed by qiyas, every verdict joined onto the face it was measured from; `POST /diff` with inline encodings (D-API-5); the ring, not the centre, is the join key | bikar #129 `d524766`, #132 `7824e12`; qiyas #26 `95dd893`; 3d-models #129 |
| 2026-09-01 | This working plan created as the index of record | 3d-models #126 `43886f2` |
| 2026-09-01 | Re-audit follow-through: memory index is an index again, backlog §6.4 points at the d3 stream, dead task ids removed; merge closing-checklist tenet | 3d-models #122 `d9b3c5d`, #123 `4cecb60` |
| 2026-08-31 | Track 1 follow-on 1.3 — pattern picker over an exported roster; Tracks 1–2 fully shipped | bikar #127 `821dfe7`; 3d-models #121 `4f7ab28` |
| 2026-08-31 | Track 2 — dials generated from each pattern's compiled param schema | bikar #126; 3d-models #120 |
| 2026-08-31 | Q-DATA measured: `{id,x,y,status}` is a join of `/encoding` + `/diff`, not new fields (D-API-4); two id namespaces | qiyas #25 `65b0edb`; 3d-models #117 `5df91eb` |
| 2026-08-31 | d3 Phase 1 — `/rosette-explorer` on the real kernel; d3-agnostic `faceConstructs` core adapter; separable `viz-d3` converter | bikar #123 `42b22b3`, #125 `ac26658`; 3d-models #118 |
| 2026-08-31 | qiyas data endpoints typed so the contract reaches OpenAPI | qiyas #24 `62124f4` |
| 2026-08-31 | bikar-studio public-surface keystone resolved: org-gated, internet-reachable | 3d-models #115 `3b80985` |
| 2026-08-31 | d3 decisions Q-HOME / Q-SHELL / Q-VOCAB / Q-DATA settled; qiyas HTTP API scoped | 3d-models #113 `75cf71d`; qiyas #23 `0c8f813` |
| 2026-08-30 | d3 integration scoping doc; branch survey and cleanup across four repos | 3d-models #111 `65f3fb3` |

Older shipments (orbs M0–M5, maclado, mural, LEGO lab, Q-series, D-039–D-046, prints-tab S1)
are the dated bullets in the memory's shipped record and the rows of
[`decisions-log.md`](decisions-log.md).

## 4. Findings — the 2026-09-01 re-audit

Systematic, not one-off: each recurred across sessions or repos. Resolution and the
tenet each left behind.

| # | Finding | Resolution | Tenet, and where it lives |
|---|---|---|---|
| 4.1 | Every per-task merge left the local branch behind, and twice the remote; stale worktrees accumulated (8 + 9 locals, 3 worktrees, 6 remotes across two repos) | All verified-merged branches deleted, worktrees removed; three no-PR bikar branches and one third-party branch deliberately kept | A merge is not done until worktree, local and remote are gone; verify "merged" by PR lookup, never subject match; never touch a no-PR branch — PR-flow memory |
| 4.2 | The memory index line had become the shipped-record log itself (13.7k chars, growing per ship) | Log moved verbatim into the memory file; index line is a hook | Index lines never carry content; memory edits are PR'd — PR-flow memory. Residue cleared 2026-09-02: the 152 KB file split into 26 one-fact memories + a `docs/research/` archive (§2.3 shipped, 3d-models #145) |
| 4.3 | Durable text cited session-scoped task ids that no longer existed | Replaced by the durable owner (prints-tab rungs) | Stable ids only — rule at the top of this file and on the memory hook line |
| 4.4 | `backlog.md` presented itself as the durable non-printer sequence but had no d3 entry; the live stream existed only in the task list | backlog §6.4 pointer; this file | Every live stream has a durable home that the task list mirrors, not replaces |
| 4.5 | A memory claim ("origin authoritative") rested on a subject match; the branch survey had already shown subject matches lie | Content-sentinel verified, then reconciled with local edits kept | A memory line that says X is authoritative names the check that showed it |
| 4.6 | The live item's task still carried its *measurement* title after the measurement shipped | Retitled to the build; sub-steps 2.1.a–f filed | A task's title is its current deliverable |
| 4.7 | Three gates and the map's self pin gave a different verdict depending on which checkout ran them: a linked worktree sits one level below the siblings, and a self pin taken at branch HEAD does not survive a squash merge — so a worktree commit failed on 14 false "resolves now" while the primary passed, and master carried an orphaned pin | Sibling fallback via the git common dir in all three gates; self pin at merge-base with origin; self-tests build a primary + worktree + sibling layout and assert both verdicts agree (#132 `44fba5c`, #133 `b7a8908`) | **A gate's verdict must not depend on which checkout runs it** — every gate that touches a path outside the repo gets a worktree self-test; a pin the repo takes on itself is taken at the published base, never at HEAD — memory `gate-verdict-checkout-independent` |

Related precedent on why this is a plan and not a register:
[`issue-register-evaluation.md`](issue-register-evaluation.md) — registers nobody re-reads
decay; this file is re-read because §2 is the queue we pull from.

## 5. Links

**Repos.** bikar `NaqshCoffee/bikar` (DSL + engine, producer of record); qiyas
`NaqshCoffee/qiyas` (validator, Python/FastAPI); 3d-models `omars-lab/3d-models` (this
repo: docs, gallery, gh-pages); sacred-patterns (canonical contract, d3 prior art on
`wip/react-d3-2024`).

**Live surfaces.** bikar-studio at `bikar.naqshcoffee.com` (org-GitHub-gated;
`/rosette-explorer` is Phase 1). The studio reaches qiyas through its same-origin
`/api/qiyas/*` proxy to a configured upstream behind a service token; locally qiyas runs via
`uv run qiyas` (`review` for the portal with wildcard CORS, `serve` headless on port 8731,
no CORS when hosted).

**Design docs here.** [`d3-integration-design.md`](d3-integration-design.md) ·
[`rosette-pin-explorer-design.md`](rosette-pin-explorer-design.md) ·
[`lego-lab-design.md`](lego-lab-design.md) · [`prints-tab-design.md`](prints-tab-design.md) ·
[`backlog.md`](backlog.md) · [`decisions-log.md`](decisions-log.md) ·
[`grounding-defect-taxonomy.md`](grounding-defect-taxonomy.md).

**Sibling docs.** bikar decision `bikar:docs/decisions/2026-08-31-d3-viz-adapter.md`
(core d3-agnostic, one converter module, page registration pattern); qiyas scoping
`qiyas:docs/design/data-model-http-api.md` (existing FastAPI app, no second framework).

**Memory.** [`../.claude/memory/MEMORY.md`](../.claude/memory/MEMORY.md) is the index;
[`../.claude/memory/islamic-orb-project.md`](../.claude/memory/islamic-orb-project.md)
holds the dated shipped record; [`../.claude/memory/pr-flow-for-all-repos.md`](../.claude/memory/pr-flow-for-all-repos.md)
holds the merge closing checklist.

## 6. Reading this file against itself

- §2.1's state (shipped) agrees with backlog §6.4 (shipped 2026-09-01) and d3 doc §4
  (Phase 2 SHIPPED); the three moved together in the PR that ran 2.1.f.
- §2.2 lists exactly the four unblocked rows of explorer doc §6.6; §2.8 is its item 5.
- §3's newest row is this file's own PR only after it merges — the sha is filled in
  by that PR, never predicted.
