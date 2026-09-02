# Lego tooling — the plan we are working against

**Status: live. Opened 2026-09-01.** This file is the one place that says what the Lego
stream is for, what is built, what is left, what gates each remaining item, and where the
evidence lives. It is a *plan*, not a record: the design docs own every number, and this file
points at them rather than re-typing them. If this file and a design doc disagree, the doc wins
and this file is wrong.

## 1. Objective

Turn a bikar pattern into a **LEGO-compatible printed part that clutches into real LEGO** —
and make "is this pattern LEGO-compatible?" a measurable question rather than a guess. The
five concrete goals are `docs/lego-lab-design.md` §1; their state on 2026-09-01:

| # | Goal | State | Where the evidence is |
|---|---|---|---|
| 1 | A `brick` declaration compiling to a watertight printable solid with pattern relief | **built** (M6) | lego-lab-design §4, §7, §10 |
| 2 | Anchorability as a hard pass/fail gate | **built** (M7) | §5.2, §5.3; `grid-gate.ts` |
| 3 | Grid fit as a 0..1 score with a tuning path | **built** (M7 + P1 sweep strip) | §5.3, `research/lego-lattice-matrix-sweep.md` |
| 4 | True-scale interoperability **verified in plastic** | **open — the only open goal** | `docs/backlog.md` §3.2; printer on hold |
| 5 | The Lego Lab page | **built** (P0–P3) | §9, §14 |

Beyond the five: multi-piece export (D-006), `mural` (UC20), `footprint outline` (UC21), LDraw
export + read-back + two-tone colour (§14.3–14.6), the thumbnail CLI and colour gate (§15–16),
and the rosette → LEGO-pin explorer running the real kernel in bikar-studio (Tracks 1–2). All
shipped; each has its section in the doc named above.

## 2. What is left, by what gates it

The authoritative list is `docs/rosette-pin-explorer-design.md` **§6.6** (the open ledger).
`docs/backlog.md` §6.4 points at it. Summary, with the task that tracks each:

| Gate | Item | Task |
|---|---|---|
| none | Widen the explorer roster past Rosette-N / Star-N — 🟢 bikar #134 `85269ac` | #65 done |
| none | Ground the explorer doc — it is the roadmap of record and reads "draft" — 🟢 3d-models #136 | #66 done |
| none | Track 3.2 — `PLATES` const → data file, no fabricated links — 🟢 bikar #141 `571cba2` | #67 done |
| none | Track 4.2 — interior-tube cap dial, kernel floor un-overridable — 🟢 bikar #143 `a4318c9` | #68 done |
| download (user) | Open the MPD in LeoCAD and BrickLink Studio | #69 |
| decision (user) | §11 Q6 — ship a clutch compliance proxy as a `CAL-*` bet, or not | #71 |
| printer (held) | Every LG-* coupon: F1, F2, R1, S1, D1, B1, B2, P1, P2 | none — `backlog.md` §3.2 owns them, per its §3.8 |

Closed doors, so they are not reopened: §15.4's hook graduation (waits on measured recurrence),
Q8's general two-vector basis (D-007, resolved as a label), Track 2.3's authoring skill (not
needed at runtime).

**Order of attack for the unblocked four** (all shipped 2026-09-01/02, in this order): #65 first
(it is the goal's own objective — *any* pattern — and costs one line per figure), then #66 (the
roadmap of record should not be the one un-audited doc), then #67 and #68. Task metadata carries
the same ordering as `priority` 1–4 and, for the gated rows, `priority` 5–7 with the gate named.
**Nothing unblocked is left**: every open row below needs the user (a download, a decision) or a
printer, so the next code-shaped move is whichever of those the user unblocks first.

## 3. Adjacent, not Lego — tracked so they are not confused with it

| Task | What | Gate |
|---|---|---|
| #63 | `bikar-studio.pages.dev` exposure-equivalent to the custom domain | user: Cloudflare dashboard + service token + 2 GH secrets |
| #64 | Repoint `index.html:277` off the Access-gated host | blocked by #63 |
| #52 | Folder round-trip against the live studio | user: a signed-in session behind CF Access |

## 4. Findings from the 2026-09-01 survey worth keeping

- **The use-case map's line numbers were never checked.** 23 of 44 pointed at unrelated lines
  while every run said "all valid". Fixed with opt-in anchors (`repo:path:L137 "orbs:"`),
  proven red-then-green through the real hook. PRs #13, #14; the tenet is in `CLAUDE.md`
  (PR #15).
- **`make deploy` was the one publish path with no gate in front of it** — the hooks fire in the
  `gh-pages` worktree but every `.claude`-dependent gate skips there by design. `deploy` now
  depends on `validate-site-graph`.
- **Every code-shaped Lego goal is built.** What remains is gated on things code cannot supply:
  a printer, a downloaded app, or a decision. The ledger in §6.6 exists so that stays visible
  instead of being re-discovered.
- **A cap on anchors can *lift* a kernel failure, not only preserve a pass** (found building #68).
  The first draft kept the outermost anchors — exactly the thin-walled ones — and the two-way
  assertion "verdict unchanged under cap" failed on face #11 at 16 studs because dropping the thin
  anchor turned a wall FAIL into a PASS. The honest invariant is one-directional, and the retention
  rule that makes it true by construction is the kernel's own criterion (thickest wall first). A
  spatial spread would have been a clutch guess, which §11 Q6 says the gate may not make.
- **An uncommitted `patterns/Rosettes/Rosette-N.bkr` default change in the primary bikar checkout**
  (points 5, crossover 37, reach 0.44, alongside a `.folders.json` edit) fails 3 of the 17 explorer
  roster tests (dial defaults, `spanPU`, recentring) — verified green on a clean `origin/main`
  worktree. It is another session's working tree, not committed; if it lands as-is the roster
  tests go red. This is the Rosette-N sweep record `docs/plan.md` row 2.14 is about.
- **A scratch worktree of bikar needs its own `dist`s.** Symlinking the primary checkout's
  `node_modules` makes `@naqshcoffee/*` resolve to the *primary's* packages, so `tsc` in the
  worktree typechecks `cli` against whatever core the other checkout has built — five phantom
  `MeshGateReport` errors here. Fix: a real `node_modules` dir of per-entry symlinks with
  `@naqshcoffee/*` pointing back into the worktree, then build core / knobs / qiyas-schema.

## 5. Links

- Design docs: `docs/lego-lab-design.md` (§10 implementation status, §11 open questions),
  `docs/rosette-pin-explorer-design.md` (§6 roadmap, §6.6 ledger),
  `docs/lego-pattern-set-design.md` (mural), `docs/pattern-outline-brick-design.md`,
  `docs/d3-integration-design.md` §4 (the explorer is d3 Phase 1).
- Backlog: `docs/backlog.md` §3.2 (LEGO ladder), §6.1 (LDraw viewers), §6.4 (d3 stream pointer).
- Research: `docs/research/ldraw-cli-viewers.md` §10 (what was actually run),
  `docs/research/lego-lattice-matrix-sweep.md`.
- The explorer artifact (the original diagnostic; the studio page superseded it):
  https://claude.ai/code/artifact/df5788b3-8785-492b-a5f0-92533fbad4e5
- The kernel-backed page: `/rosette-explorer` in bikar-studio;
  source `bikar:packages/web/src/rosette-explorer.ts`.
- This session's PRs (3d-models): #13, #14, #15 (anchors + tenet), #124 (the ledger), #141 (this
  row). bikar: #143 (the tube cap).

## 6. How this file stays honest

A task number here is a *pointer into the session task system*, which is the one place that may
carry them (memory rule: durable docs cite stable ids, never task numbers — this file is a plan,
not a durable doc, which is why it is allowed to). When a task closes, update §2 and the doc's
§6.6 in the same change. When a printer arrives, §2's last row moves to `backlog.md` §4's
"before the first print" sequence and this file records the date.
