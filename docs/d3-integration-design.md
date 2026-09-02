# A proper d3 integration for the bikar / qiyas surfaces (scoping)

**Status:** SCOPING / backlog capture (not yet gate-audited, not built). Produced 2026-08-31
to answer one question the project keeps re-encountering: *when a bikar or qiyas surface
needs interactive 2D SVG — a rosette explorer, an orb breakdown, a score overlay — what is
the proper way to reach for d3, given a fourth repo (sacred-patterns) already has a mature
d3 vocabulary and a stalled React-on-d3 experiment?* This file is the backlog item. It does
**not** commit an implementation — it scopes one, records the audit that informs it, and
carried the load-bearing choices to the user as decisions ([§5](#5-decisions-to-make)), **all
four of which were settled 2026-08-31** and are now recorded there as the direction a build
follows.

This is a *prepare-the-approach* item, in the sense [`backlog.md`](backlog.md) reserves for
work that is queued but not yet a build. It is the visualization-layer sibling of the
[rosette → LEGO-pin explorer](rosette-pin-explorer-design.md), which is the first concrete
consumer that will need this decision settled.

---

## 1. The three repos and where d3 actually sits today

The system is deliberately split (see [`../CLAUDE.md`](../CLAUDE.md)): **bikar** is the DSL
+ geometry engine and producer of record, **qiyas** validates renders, and this repo
consumes bikar. A fourth repo, **sacred-patterns**, predates all of them and is the original
d3 project. Grounded against each repo's working tree, 2026-08-31:

| repo | language | d3 today | React today | role for a viz layer |
|---|---|---|---|---|
| **sacred-patterns** | TypeScript | **yes** — `master` runs d3 v7 vanilla-TS; its own package description is *"Sacred geometric patterns as SVG using D3.js"* | no (shipped); an unmerged branch tried it — [§2](#2-audit-the-wipreact-d3-2024-branch) | owns a reusable geometry + draw vocabulary |
| **bikar** | TypeScript | some, ad-hoc — the studio's `decomp` page and dist bundles reference d3; the web packages do **not** declare d3 or React as dependencies. 3D views use three.js (`OrbViewer`) | no | producer of the SVG geometry (rosette, orb cell/ribbon views) a viz consumes |
| **qiyas** | **Python** | no — it emits validation JSON (per-view scores, `drop`, `max_drift`, diffs); it does not and should not run d3 | n/a | producer of the *scoring* data a viz overlays |

Two facts fall out of this table and shape everything below:

- **"qiyas integrates with d3" cannot mean qiyas runs d3.** qiyas is a Python validator. Its
  integration is a **data contract**: it emits JSON a d3 layer reads. The DSL-metadata
  contract that already governs bikar↔qiyas (contract v1.5, mirrored across the repos) is the
  precedent — a viz overlay is a third consumer of the same scored output, not new qiyas code.
- **bikar is not a d3 project and sacred-patterns is.** So the interesting question is not
  "add d3 to bikar" but **"where does the d3 layer live, and does sacred-patterns' vocabulary
  get shared or stay separate?"** — a cross-repo boundary question, which is exactly the kind
  [`../CLAUDE.md`](../CLAUDE.md) says to price before writing code.

---

## 2. Audit: the `wip/react-d3-2024` branch

The branch was surveyed during the 2026-08-30 branch cleanup and **deliberately kept** as
genuinely-unmerged work; this section is the audit the user asked for. It is
`sacred-patterns` `wip/react-d3-2024`, tip `4ce6e32` ([permalink](https://github.com/omars-lab/sacred-patterns/blob/4ce6e32b37a363266180b009715a0f397ba2a468/src/ts/index.tsx)),
three commits, the newest a 2026-08-03 checkpoint of a working tree last actually worked on
in **June 2024**.

### 2.1 What it attempted

Two separable things, and telling them apart is the whole value of the audit:

1. **A dependency modernization.** d3 5 → 7, TypeScript 3 → 5, webpack 4 → 5, eslint 6 → 8,
   plus `npm-check-updates` wiring.
2. **A UI-shell introduction.** React 18 + `react-bootstrap` + `bootstrap`. A new
   an `index.tsx` renders a `<NavigationBar>` → `<ArtworkDropdown>` that selects among
   nine artworks by `eventKey`, and a `D3Artwork` component bridges React to d3 with the
   canonical hooks pattern: React owns a `<svg ref>`, `useEffect` runs `d3.select(ref)` +
   imperative draws on `[activeArtworkIndex]` change. A new `draw.ts` holds the
   artwork functions (`drawChainedStars`, `drawStarGrid`, `drawLotfallahDome`, …) over the
   repo's existing geometry classes (`Circle`, `Hexagon`, `Nonagon`, `Star`, `Polygon`).

### 2.2 What is dead, and what is live

- **The dependency half is dead.** `master` has since done the same upgrades independently —
  it is already on d3 v7, TypeScript 5.7, webpack 5. Resurrecting the branch for its deps
  would be a merge conflict with no payload. This is why the branch never needed to land.
- **The live idea is the React-on-d3 bridge and the artwork registry** — a shell that lists
  named drawings and swaps one into an SVG the framework owns. That pattern is sound and is
  precisely what an *explorer* surface (rosette, orb) wants: a control strip driving a redraw.
- **The genuinely reusable asset is the vocabulary, not the plumbing** —
  [`draw.ts`](https://github.com/omars-lab/sacred-patterns/blob/4ce6e32b37a363266180b009715a0f397ba2a468/src/ts/draw.ts)
  plus the geometry classes and the `append*` canvas helpers. That is a real Islamic-geometry
  d3 toolkit; it is the thing worth sharing across surfaces.

### 2.3 The smells to *not* carry forward

The branch is a 2024 checkpoint, and it shows. A proper integration must not inherit:

- **Full teardown per change** — `svg.selectAll("*").remove()` then redraw on every dropdown
  change, rather than a d3 data-join that enters/updates/exits. Fine for nine static
  artworks; wrong as a template for an interactive explorer that changes a dial 60×/second.
- **Config through the DOM** — reading `JSON.parse(document.getElementById("config").innerText)`
  for theme, instead of passing props. A React shell exists specifically to make that a prop.
- **`setInterval` animation** (`drawRotatingCircles`) rather than d3 transitions or rAF.
- **Two mount paths** — a React `ref` path and a `d3.select("body").append("svg")` path
  coexist; one of them has to go.
- **No tests.** The weave-progress work in the same repo shows the current bar (Playwright
  visual specs, a pixel-diff route); a new d3 layer should meet it, not the 2024 bar.

**Net:** keep the *registry + React-bridge shape* and the *geometry/draw vocabulary*; discard
the deps, the teardown-redraw idiom, the DOM-config, and the dual mount.

---

## 3. What "a proper integration" has to decide

The audit gives a pattern; it does not answer *where the layer lives* or *who owns it*. Those
are the real content of this backlog item, and they are cross-repo, so they were carried to
the user as decisions ([§5](#5-decisions-to-make)) rather than settled in code. The four
questions, as framed for that decision (their answers are in [§5](#5-decisions-to-make)):

- **Q-HOME — where does the shared d3 layer live?** Candidates: (a) a new package inside
  bikar's web workspace, imported by every bikar surface; (b) a standalone package extracted
  from sacred-patterns; (c) no shared package — each surface vendors what it needs. (a) keeps
  the producer of record as the single source; (c) is cheapest now and forks the vocabulary
  later — the trade [`../CLAUDE.md`](../CLAUDE.md) names ("robust and simplifying outrank
  cheap in a refactor").
- **Q-SHELL — React, or not?** The branch chose React 18. bikar's surfaces are currently
  non-React (three.js + vanilla/Vite). Adopting React is a real commitment across those
  surfaces; the alternative is the same bridge in vanilla/Lit. This choice is independent of
  d3 and should be made on the surfaces' terms, not the branch's.
- **Q-VOCAB — port sacred-patterns' vocabulary, or keep it a separate gallery?** Sharing it
  makes the Islamic-geometry drawings available to the bikar explorers; keeping it separate
  avoids a cross-repo dependency into a fourth repo the core system does not otherwise touch.
- **Q-DATA — the qiyas overlay contract.** A score/diff overlay reads qiyas JSON. Decide
  whether that reuses the existing contract output as-is or needs a viz-shaped projection of
  it (positions per view, not just scalars). qiyas stays Python either way.

---

## 4. A sketch of the plan (not a commitment)

Phased so each phase answers a question before the next spends effort. Nothing here is
scheduled; the ordering is the dependency order, not a promise.

- **Phase 0 — this doc.** Scope, audit, decisions. **Done** — the four [§5](#5-decisions-to-make)
  decisions are settled, and the bikar-studio public-surface keystone resolved 2026-08-31
  (internal, org-GitHub-gated, internet-reachable).
- **Phase 1 — one reference surface, end to end. SHIPPED 2026-08-31.** The
  [rosette → LEGO-pin explorer](rosette-pin-explorer-design.md) was the natural first consumer:
  it is already an SVG instrument, and its own roadmap was *blocked on the same bikar-studio
  public-surface decision*. Built as the studio's `/rosette-explorer` page in a **plain vanilla
  shell** (Q-SHELL — d3 owns the `<svg>` inside a plain container), consuming real bikar rosette
  geometry through the **d3-agnostic constructs + opt-in converter** (Q-HOME). Three bikar PRs,
  no stacking: the core `faceConstructs` adapter + `ribbedRingPoints`/`solveAnchorsOnGlobalGrid`
  exports (**#123** `42b22b3`), the dropped-anchor positions on the solve (`7674683`), and the
  page + separable `viz-d3.ts` converter (**#125** `ac26658`). The converter lives web-side (a
  standalone module, no page state) until a second consumer earns its extraction to
  `@naqshcoffee/bikar-d3`. The one deliberate divergence — one global baseplate under all pieces,
  not `solveAnchors`' piece-local centered lattice — is kept **in the kernel** as
  `solveAnchorsOnGlobalGrid`, so the page runs the engine's rule rather than re-porting it; this
  deletes the private artifact's hand-ported anchor copy. Follow-on **Track 2 (schema-driven
  dials) shipped 2026-08-31** (bikar **#126** `cff3cf1`): the pattern dials are generated from the
  compiled `.bkr`'s own `param` declarations (`compileToGeometry(src).params`, already on the
  wire as `ParamSpec`), not hand-coded per pattern. The **pattern picker (1.3) shipped the same
  day** (bikar **#127** `821dfe7`): a roster of flat, origin-centred `.bkr` figures (Rosette-N +
  Star-N) with a `<select>` to swap them, each pattern's dials generated from its own schema — so
  every non-printer piece of Phase 1 (Tracks 1–2) is shipped.
- **Phase 2 — the qiyas overlay. SHIPPED 2026-09-01** as the studio's `/orb-instrument`
  page, the whole chain in the browser: an orb `.bkr` compiled and rendered to one
  symmetry-axis view (bikar **#129** `d524766`, the `orbViewSvgs` helper over the same four
  core exports the editor drives) → qiyas `POST /deconstruct` encodes that exact SVG as the
  reference → the page drops every Nth shape as the reconstruction → `POST /diff` with both
  encodings inline (qiyas **#26** `95dd893`, D-API-5 — the second consumer D-API-4 said would
  earn a route) → each diff bucket carried onto the face it was measured from (bikar **#132**
  `7824e12`). It is a *data* integration: no Python touches d3, and the stage is the core
  renderer's own SVG with one `data-status` attribute joined onto each `<path data-face-index>`.
  The Q-DATA join was re-measured on orb faces before it was built: a shape's **centre is not a
  key** (orb faces are concave; two shapes' centres fell inside the same neighbouring face),
  its **ring is** — qiyas keeps bikar-tagged contours vertex-exact, so `evidence.outline`
  mapped through the viewBox→px affine equals exactly one face ring, 55/55 bijective at 0.0
  deviation on Star-Orb's hero view. The by-design failures are the load-bearing cases: a ref
  id in no diff bucket is shown *unknown*, never defaulted to matched; a face no shape claims is
  drawn *unclaimed*; an id in two buckets throws. A checked-in fixture (the hero SVG, its
  encoding, the degraded copy, the diff) is pinned to the live render byte for byte and to the
  encoding's sha256, so a renderer or encoder change turns it red rather than stale, and the
  page falls back to it — labelled — when no qiyas answers. Found on the way: bikar's
  generated qiyas schema types lagged qiyas's `scores` (no `drop`/`surplus`/`max_drift`), so the
  first page derived them from the buckets. Fixed since (bikar #145 `cdc0331`): the mirror is
  re-vendored, the page reads the scores, and a 3d-models gate (`.claude/gates/schema_mirror.py`)
  holds bikar's copy to qiyas's export at the use-case map's pins — [`plan.md`](plan.md) §2 row 2.9.
- **Phase 3 — unify the vocabulary.** Per Q-VOCAB, converge the explorers and sacred-patterns
  on one **common naming convention**, refactoring either side as needed. With one or two
  surfaces built, how much vocabulary actually gets shared is cheap to see.

**What unblocks what:** Phase 1's blockers were all cleared — the bikar-studio keystone
resolved and Q-HOME/Q-SHELL settled — and Phases 1 and 2 are both **built** (the
`/rosette-explorer` and `/orb-instrument` pages). Phase 2 did end up needing one qiyas change
after all — `POST /diff` with inline encodings (D-API-5) — because nothing before it diffed two
browser-held renders. Phase 3 is now unblocked: two surfaces exist to read the shared vocabulary off.

---

## 5. Decisions, resolved 2026-08-31

The four questions were carried to the user and settled in one sitting. These are the
directions a build follows; the reasoning the user gave is recorded with each.

1. **Q-HOME → an opt-in converter, on top of a d3-agnostic engine.** Not "bake d3 into
   bikar." The rule the user set: **bikar's core stays d3-agnostic and emits generic,
   d3-friendly, generally-consumable constructs** — anything can read them, not just d3 — and
   a **separable, optional converter** maps those constructs to d3 for the surfaces that want
   it. A bikar user who only needs geometry is never forced to pull in the d3 layer. This is
   the robust reading of the [`../CLAUDE.md`](../CLAUDE.md) trade: the coupling that would rot
   (engine tied to one viz library) is designed out; the shared code is the thin adapter.
   *(Was: bikar-package vs extracted vs per-surface — resolved as a decoupled adapter, home
   secondary to the decoupling.)*
2. **Q-SHELL → plain / lightweight, not React.** The shell (controls, layout — the frame
   around the drawing) is **vanilla or Lit**, matching bikar's existing viewer (plain +
   three.js). d3 owns the `<svg>` inside a plain container. The react-d3-2024 branch's React
   shell is therefore **not** adopted — only its geometry/draw vocabulary and the general
   "framework owns the container, d3 owns its interior" bridge idea carry forward.
3. **Q-VOCAB → converge on a common naming convention; refactor either side to get there.**
   Not "import one side's names as-is." The explorers and sacred-patterns should share **one
   vocabulary under a common naming convention**, and refactoring *either* sacred-patterns or
   bikar to align the names is explicitly authorized. Effectively share-but-unify.
4. **Q-DATA → a viz projection that is a JOIN, not new qiyas fields (MEASURED 2026-08-31).** The
   overlay wants **per-shape** `{id, x, y, status}` per view so it can point at the exact failing
   shape, not just badge a view with a number. A direct measurement (encode a fixture, diff it
   against another through the qiyas runner) settles how to get it: **`{id, x, y}` is already
   universal** — `center` (`[x,y]`) and `id` are keys on *every* shape in qiyas's `ShapeUnion` — and
   **`status` is just the diff bucket the id lands in** (`matched` / `missing_in_recon` /
   `ambiguous` partitioned all of a fixture's shapes, 0 unknown, 0 uncovered). So Q-DATA is a
   documented join of `/encoding` + `/diff`, **no new qiyas fields**; qiyas stays Python. One catch
   the overlay must honor: statuses live in **two id namespaces** — ref-side ids join on
   `/encoding(ref)`, while `extra_in_recon` (surplus) is recon-side and joins on `/encoding(recon)`.
   Recorded qiyas-side as D-API-4; the `response_model=` typing that surfaces these schemas in
   Swagger shipped as qiyas PR #24. Default: the join lives in the d3 overlay, not a new endpoint.

**Keystone RESOLVED 2026-08-31 (was open under Q-HOME/Phase 1):** the bikar-studio surface *is*
public in the sense that its only entry — bikar.naqshcoffee.com — is internet-reachable, but it is
**gated behind an org GitHub sign-in**, so the audience is internal (org members only). "Internal,
over the internet." The converter/adapter and the rosette explorer are therefore served from this
same org-gated surface — reachable over the internet, not open to the world. This unblocks the
Phase 1 call [§4](#4-a-sketch-of-the-plan-not-a-commitment) was waiting on.

---

## 6. Related tasks, closed in favor of this item

Before this doc, the two `wip/*` branches kept after the 2026-08-30 cleanup were the open
thread. They are now resolved:

- **`sacred-patterns/wip/react-d3-2024`** — its "what do we do with this?" question is
  **answered by this doc**, not by merging the branch. The dep half is dead (master did it);
  the live ideas (React-bridge shape, artwork registry, geometry/draw vocabulary) are captured
  in [§2](#2-audit-the-wipreact-d3-2024-branch) and feed Phases 1 and 3. The branch stays
  **kept** as the auditable prior art this doc cites — deleting it would orphan the citations —
  but it is no longer an undecided item.
- **`sacred-patterns/wip/weave-progress-page`** — the other kept branch, and unrelated to d3
  integration; it holds a shipped-quality weave-progress page. It is **merged into
  sacred-patterns `master`** rather than folded here (see the branch-cleanup memory note),
  because it is finished work, not a scoping question.

---

## Provenance

Repos read at their working-tree checkouts 2026-08-31: sacred-patterns (`master` and
`wip/react-d3-2024` at `4ce6e32`), bikar (`main` at `8709471`), qiyas (`main`, Python — no d3
dependency, but a versioned pydantic JSON contract and a FastAPI/Swagger surface, see
[§5](#5-decisions-to-make) Q-DATA). Sibling files are cited by GitHub permalink at a pinned
commit, not by local path. The four [§5](#5-decisions-to-make) decisions are settled
2026-08-31; the bikar-studio public-surface keystone is the one call still open. This remains
a *scoping* item — if it graduates to a committed design doc that ships code, it must be run
through the `ground-design-doc` process: the cross-repo claims pinned to git refs, any
external d3/React source moved into [`research/`](research) under a provenance header, and the
whole run through the doc gates (D1–D4) and an adversarial grounding audit.
