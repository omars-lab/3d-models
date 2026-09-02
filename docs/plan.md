# Working plan — what we are working against

Last updated: 2026-09-01. This is the **index of record** for active work across the
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
| 2.1 | **d3 Phase 2 — the full orb-view instrument.** One bikar orb `.bkr` compiled in the browser → one orb-view SVG (the same one the core renderer emits, faces carrying their index) → qiyas encodes that exact SVG as *ref* and a deliberately degraded copy as *recon* → `/diff` → a status mark per shape overlaid on the bikar-rendered SVG, joined by id. Chosen 2026-08-31 over the fixture-only and 2D-only slices. | 🔵 | none — join measured (qiyas D-API-4), Phase 1 layer shipped | d3 doc §4 Phase 2, §5 Q-DATA |
| 2.1.a | Orb-view SVG from an orb source inside the studio. **Mapped 2026-09-01:** the chain is four public core exports — compile to geometry, `symmetryViewAxes`, `projectOrbViewScene`, `renderOrbViewSVG` — already driven by the editor one view at a time; sixteen orbs are bundled, Star-Orb is the smallest (three views: `vertex-5`, `face-3`, `edge-2`); every face carries `data-face-index`, unique **per view** (restarts at 0 per view), so the join key is (view id, face index) | 🔵 | — | `bikar:packages/core/src/render/orb-view-renderer.ts`, `bikar:packages/web/src/main.ts` |
| 2.1.b | Getting a browser-rendered SVG *into* qiyas. **Mapped 2026-09-01:** only `POST /deconstruct` takes inline bytes (multipart `file`, `.svg` allowed) and returns an Encoding; `/encoding` and `/diff` take server-side *paths*, so nothing today diffs two browser-held renders. The studio's same-origin proxy already streams any method and body. Decision to make: add a `POST /diff` that takes two Encodings inline (mirrors the CLI's `diff` of two encoding files, and is the second consumer D-API-4 said would justify a route) vs write both SVGs to a server workspace path. Tests use a checked-in Encoding + Diff pair either way | 🔵 | — | qiyas `qiyas:src/qiyas/review/server.py`; studio proxy `bikar:packages/web/functions/api/qiyas/[[path]].js` |
| 2.1.c | The join: `/encoding(ref)` + `/encoding(recon)` + `/diff` → `{id, x, y, status}` honouring the **two id namespaces** (ref-side buckets join on the ref encoding, `extra_in_recon` on the recon encoding) | ⚪ | 2.1.b | d3 doc §5 Q-DATA |
| 2.1.d | The page: `/orb-instrument` cloned from the rosette explorer's shape — plain shell, d3 owns the SVG interior, one status-mark join in the separable `viz-d3` module keyed by qiyas id; core stays d3-agnostic | ⚪ | 2.1.a–c | bikar decision 2026-08-31 d3 viz adapter |
| 2.1.e | Registration — five real touch points (html file, page marker meta, `PAGE_ROUTES`, rollup input, routing test; there is no site nav and the public-surface file lists hosts and env keys, not pages) + tests that fail without the join, DOM-free like the package's other tests + a checked-in Encoding/Diff fixture pair so the suite needs no server | ⚪ | 2.1.d | `bikar:packages/web/vite.config.ts`, `bikar:packages/web/tests/routing.test.ts` |
| 2.1.f | Record it: d3 doc §4 Phase 2 → shipped, backlog §6.4 row, §3 here, memory shipped-record bullet | ⚪ | 2.1.e | this file |
| 2.2 | Explorer open ledger — widen the roster (6.6.1), ground the explorer doc (6.6.2), plates as data (6.6.3), interior-tube cap (6.6.4) | ⚪ | none | explorer doc §6.6 |
| 2.3 | Memory decomposition — `islamic-orb-project.md` is one 140 KB file; split by topic into one-fact files | ⚪ | none; do before the next append | §4.2 below |
| 2.4 | d3 Phase 3 — unify the vocabulary across the explorers and sacred-patterns (Q-VOCAB) | ⚪ | after 2.1 shows what is shared | d3 doc §4 Phase 3 |
| 2.5 | Publish the contract + JSON schema | 🟡 | user: venue and versioning | qiyas `contract/schemas/`, sacred-patterns canonical v1.5 |
| 2.6 | coffee-house-sites issue 1 | 🟡 | user | that repo |
| 2.7 | First physical print — machine card, LEGO ladder, W-series, orb ladder; prints-tab rungs S2–S7 | 🔴 | a Bambu-class printer | backlog §2–§3, prints-tab doc |
| 2.8 | Explorer printer-held rows (3.3, 3.4, 4.3) | 🔴 | printer | explorer doc §6.5 item 5 |

## 3. Shipped — this stream, newest first

| Date | What | Where |
|---|---|---|
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
| 4.2 | The memory index line had become the shipped-record log itself (13.7k chars, growing per ship) | Log moved verbatim into the memory file; index line is a hook | Index lines never carry content; memory edits are PR'd — PR-flow memory. Residue: the 140 KB file (§2.3) |
| 4.3 | Durable text cited session-scoped task ids that no longer existed | Replaced by the durable owner (prints-tab rungs) | Stable ids only — rule at the top of this file and on the memory hook line |
| 4.4 | `backlog.md` presented itself as the durable non-printer sequence but had no d3 entry; the live stream existed only in the task list | backlog §6.4 pointer; this file | Every live stream has a durable home that the task list mirrors, not replaces |
| 4.5 | A memory claim ("origin authoritative") rested on a subject match; the branch survey had already shown subject matches lie | Content-sentinel verified, then reconciled with local edits kept | A memory line that says X is authoritative names the check that showed it |
| 4.6 | The live item's task still carried its *measurement* title after the measurement shipped | Retitled to the build; sub-steps 2.1.a–f filed | A task's title is its current deliverable |

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

- §2.1's state (live) agrees with backlog §6.4 (live, nothing built) and d3 doc §4
  (Phase 2 not shipped). When 2.1.f runs, all three move together.
- §2.2 lists exactly the four unblocked rows of explorer doc §6.6; §2.8 is its item 5.
- §3's newest row is this file's own PR only after it merges — the sha is filled in
  by that PR, never predicted.
