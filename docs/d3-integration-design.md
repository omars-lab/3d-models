# A proper d3 integration for the bikar / qiyas surfaces (scoping)

**Status:** SCOPING / backlog capture (not yet gate-audited, not built). Produced 2026-08-31
to answer one question the project keeps re-encountering: *when a bikar or qiyas surface
needs interactive 2D SVG — a rosette explorer, an orb breakdown, a score overlay — what is
the proper way to reach for d3, given a fourth repo (sacred-patterns) already has a mature
d3 vocabulary and a stalled React-on-d3 experiment?* This file is the backlog item. It does
**not** commit an implementation — it scopes one, records the audit that informs it, and
hands the load-bearing choices back to the user as decisions ([§5](#5-decisions-to-make)).

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
are the real content of this backlog item, and they are cross-repo, so they are decisions
([§5](#5-decisions-to-make)) rather than code. Framed as questions:

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

- **Phase 0 — this doc.** Scope, audit, decisions surfaced. Done when the user settles
  [§5](#5-decisions-to-make)'s Q-HOME and Q-SHELL — the two that gate everything downstream.
- **Phase 1 — one reference surface, end to end.** The
  [rosette → LEGO-pin explorer](rosette-pin-explorer-design.md) is the natural first consumer:
  it is already an SVG instrument, and its own roadmap is *blocked on the same bikar-studio
  public-surface decision* a shared-package home would settle. Build the d3 layer once, there,
  in whatever shell Q-SHELL picks, consuming real bikar rosette geometry.
- **Phase 2 — the qiyas overlay.** Render per-view score/diff data (from qiyas JSON) as a d3
  layer on top of a bikar SVG orb view — the "why did this view score 0.67" instrument. This
  is the qiyas↔d3 integration proper, and it is a *data* integration: no Python touches d3.
- **Phase 3 — decide sacred-patterns' fate.** With one or two surfaces built, the Q-VOCAB
  answer is cheap to see: either extract the vocabulary into the Q-HOME package, or leave
  sacred-patterns as an independent gallery and let the explorers keep their own primitives.

**What unblocks what:** Phase 1 needs Q-HOME + Q-SHELL. Phase 2 needs Phase 1's layer + Q-DATA.
Phase 3 needs Phases 1–2 to have revealed how much vocabulary actually gets shared.

---

## 5. Decisions to make

These are the user's calls, not tasks. Each blocks the phase that names it.

1. **Q-HOME** — shared d3 package in bikar's web workspace, a standalone extracted package,
   or per-surface vendoring? *(Blocks Phase 1.)* Recommendation to weigh: a shared package in
   bikar keeps the producer of record single-source, at the cost of standing up a new
   workspace package now.
2. **Q-SHELL** — React across the bikar surfaces, or a vanilla/Lit bridge? *(Blocks Phase 1.)*
   The branch's React choice should not decide this by inertia; bikar's surfaces are
   non-React today.
3. **Q-VOCAB** — port sacred-patterns' geometry/draw vocabulary into the shared layer, or keep
   it a separate gallery? *(Blocks Phase 3, informs Phase 1.)*
4. **Q-DATA** — does the qiyas overlay reuse the current contract output, or need a
   viz-shaped projection? *(Blocks Phase 2.)*
5. **The bikar-studio public-surface question**, already flagged by the rosette explorer's
   roadmap, is the keystone under Q-HOME/Phase 1 — the same decision, surfaced from two docs.

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
`wip/react-d3-2024` at `4ce6e32`), bikar (`main` at `8709471`), qiyas (`main`, Python —
confirmed no d3 dependency). Sibling files are cited by GitHub permalink at a pinned commit,
not by local path. If this scoping item graduates to a committed design doc that ships code,
it must be run through the `ground-design-doc` process — the cross-repo claims pinned to git
refs, any external d3/React source moved into [`research/`](research) under a provenance
header, and the whole run through the doc gates (D1–D4) and an adversarial grounding audit.
Until then this is a plan, and every decision in [§5](#5-decisions-to-make) is open.
