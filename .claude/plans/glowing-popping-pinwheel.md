# Breakdown-pages kickoff (#81) — reconcile to current state and close out

## Context

You asked me to "go on `.claude/plans/breakdown-pages-kickoff.md` … and ensure we
complete remaining open items." Investigating the ground truth against
`origin/master` (which is **6 commits ahead** of this stale local checkout — local
`69d18f6`/#166 vs remote `6f8a9ef`/#172) shows the premise has moved:

**The breakdown-pages arc is already shipped and merged.** Every technical piece the
kickoff hands off exists on origin/master and in bikar's `origin/main`:

- bikar producer: `meanDot`, `baseSolidCells`, `OrbViewStyle` + highlight, `writeTransition`,
  ribbon turntable, the `flat`/`transition`/`base`/`weave`/`turntableRepresentation`
  manifest keys, the five-section `breakdown-main.ts` — all present (verified against the
  live bikar tree). Wrap morph landed too (bikar #149, gate rule T8).
- 3d-models: `orb_previews.py` structural restyle + `display/`+`ribbons/` fallback, the
  `make orbs` timelapse pipeline, the 16-orb breakdown index, and the **T9 base-face gate
  (#49 / D-052) merged today as #170 (`19e885d`)**. bikar's producer half is #170
  (`c2fa085`, "wheelfield scaffold stamps `data-orb-unit`, not base-face"), #171, #172.
- `breakdown.html` + the transition/complete frames are live on `gh-pages`.

The `origin/master` §2 priority queue is 🟢 through 2.14; no live/queued breakdown row
remains. So the kickoff (committed as the most-recent #172) and its "source of truth"
`sunny-booping-crescent.md` are **stale docs that frame already-shipped work as
to-be-built** — a K7-style contradiction between a doc and the repo it ships in. The
kickoff's "task #81" is a fresh-snapshot id, unrelated to `done.md`'s #81 (hifth
worktrees); done.md already archives the whole "Per-orb breakdown + timelapse arc (S2)"
(#37–#48) as complete.

**There are no remaining *feature* items.** What is genuinely open is (1) proving the
shipped page meets its *goal* — the original complaint was "a newcomer still cannot see
the flat drawing become an orb," which no merge checkmark settles and which I have not
yet looked at — and (2) tidying the stale planning artifacts + local-checkout hygiene so
the next session doesn't re-attempt done work.

**Decision (2026-09-10, confirmed by Omar):** do both — verify the render *and* reconcile
the docs. Not "docs only" (a merge checkmark can't prove the page teaches) and not moving
on to 2.15 Spaced Rosette (separate feature work, out of scope here). Browser check runs
via the `claude-in-chrome` tools — the `chrome-devtools` MCP failed to connect this
session, so that path is unavailable and I'll load `claude-in-chrome` via ToolSearch.

## Local-checkout hazards (report only — I will NOT touch these)

The shared checkout is churning (a second session is on `master`), and it carries work
that is not mine:

- **An orphaned, stale, uncommitted `timelapse_gate.py` draft** (+134 lines) — an *earlier*
  non-family-branching T9 that is superseded by what merged as #170. Left by a now-idle
  session. It produces 55 findings on the pre-#170 local `build/`. It should be discarded,
  but per the shared-tree rules I will not `git restore` another session's file.
- Other uncommitted files (`.claude/memory/*`, `.claude/plans/lego-tooling.md`,
  `docs/research/ldraw-cli-viewers.md`) belong to other sessions — untouched.
- Local `master` is 6 commits behind `origin/master`.

I will do all edits in a **fresh worktree off `origin/master`**, never in the shared
checkout, and open a PR (this repo is branch→PR→merge for everything).

## Plan

### 1. Verify the goal on the actual render (the real close-out)
Look at the deployed/built breakdown, per `sunny-booping-crescent.md`'s own final
verification step, across all three families:
- **StarOrb** (cell), **WeaveOrb** (cell+strand), **Maclado9Overlap** (strand-only),
  and one **round/wheelfield** orb (DonutHexOrb) — the family the T9 honesty fix targeted.
- For each, confirm the five beats read: flat drawing → named base solid → tiling copies
  (newly-placed unit tinted) → camera-continuous spin with depth cues → live viewer; and
  that the spin reads as a *turning sphere*, not a wobbling mandala.
- Serve the built page locally (or open the `gh-pages` deploy) and capture screenshots.
- **If it teaches well** → the kickoff is obsolete; proceed to step 2 as pure tidy-up.
- **If a real teaching gap remains** → that is the one genuine open item; I scope it as a
  fresh, small, family-parameterised follow-on (not a rebuild) and bring options back.

### 2. Reconcile the stale planning docs (branch → PR)
- Mark `.claude/plans/breakdown-pages-kickoff.md` and `.claude/plans/sunny-booping-crescent.md`
  **SHIPPED** at the top (one line each, pointing at the merges: bikar #110/#149/#153–4/#170,
  3d-models #84/#148/#158/#159/#170), so no future session treats them as live. Keep the
  bodies as the historical spec/audit.
- Add a `docs/plan.md` §3 shipped line: "#81 breakdown-teaching arc — shipped; the page
  tells the five beats across all three families (T9 base-face honesty, #170)."
- Spot-check the breakdown memory `breakdown-page-instrument.md` D-052 note against the
  pivot doc — it is accurate (bikar #170 `c2fa085` = `data-orb-unit`/`baseIndexKind`), no
  change needed.

### 3. Hand back the hygiene items
Report the three local-checkout hazards above and recommend: let the shared checkout sync
to `origin/master` and discard the orphaned T9 draft (owner's call, since it is another
session's file).

## Verification
- Step 1: screenshots of the four orbs' breakdown pages, beat-by-beat, stated plainly
  (teaches / gap-here). This is the check the arc never had — the page has no continuity
  or coverage gate.
- Step 2: the doc-reconciliation PR runs `make validate` green (docs gate D1 pointers,
  pointer gate, counts) from its worktree; no `build/` regeneration needed (docs only).
- No bikar change and no `make orbs` regen: the producer and pipeline are already merged.
