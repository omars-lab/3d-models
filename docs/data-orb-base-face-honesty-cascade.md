# Cascade: `data-orb-base-face` names one thing, a true base face (#49 follow-through)

**Status:** PLANNED 2026-09-02. Decision recorded in
[D-052](decisions-log.md). This doc is the actionable checklist for the four-repo
change; it does **not** re-argue the decision. Deferred deliberately so it runs on
clean, current masters (see §5) rather than across the seven in-flight bikar worktrees
that vendor the contract today.

## 1. The defect, in one line

`data-orb-base-face` (SVG) and gt.json `orb_base_face` carry **two meanings under one
name**: a true base-polyhedron face for inscribed orbs (the index a projected element
was lifted through), and a *generative unit* (wheel `0..19` / filler `20..31`) for
wheelfield orbs. bikar's contract row documents the overload honestly-by-doc but
dishonestly-by-name — "read it as which unit, never as which base face." T9 (#49)
uncovered it: a wheelfield breakdown labels `base face(s) 15, 16, 20, 25, 31 on a
12-face solid` — indices past the face count, because they are units, not faces.

## 2. The fix (the robust one, per the CLAUDE.md tenet)

One name, one meaning, everywhere:

- `data-orb-base-face` / `orb_base_face` = **a true base-polyhedron face only.**
  Present on inscribed cell views and the bare base solid; **absent** on wheelfield
  cell views and (already) ribbon views.
- The wheelfield generative unit is preserved under its own honest name
  `data-orb-unit` (SVG). gt.json **omits** `orb_base_face` for wheelfield shapes
  exactly as it already omits it for ribbon strands (contract v1.5, "the omission is
  the claim").

Why preserve rather than omit on the SVG side: a ribbon crosses many wheels, so no
single index is true and omission is honest; a wheelfield cell has **one** real
generative unit, so dropping it discards a real capability — the cheap trade the tenet
forbids. So it is renamed, not dropped.

## 3. The cascade — four repos, non-stacked PRs, each merged green before the next

The order is forced by the vendored contract (`sacred-patterns` canonical → `bikar`
and `qiyas` copies, byte-identical, checked by bikar hook 41 / `3d-models`
`schema_mirror.py`) and by `build/bikar-ref.txt`.

1. **sacred-patterns** — canonical `docs/dsl-metadata-contract.md`:
   - Rewrite the `data-orb-base-face` row: true base face only; absent on wheelfield
     **and** ribbon cell views.
   - Add a `data-orb-unit` row: producer-side provenance (wheel/filler index).
     Consumer = 3d-models' T9 / future grouping; **qiyas n/a** — qiyas has no use for
     the unit, so it is not a qiyas-round-tripped attribute (like `data-authored-region`).

2. **bikar** — the SVG half is already built on branch `feat/base-face-honest-attr`
   (see §4). Remaining:
   - `gt-emitter.ts` `buildOrbViewShape`: thread the scene's kind through and emit
     `orb_base_face` only for the face kind; omit it for wheelfield (mirror
     `buildRibbonShape`, which already omits it).
   - Bump `GT_SCHEMA_VERSION` (1.28 → 1.29) for the semantic change.
   - Update gt-emitter tests + the gt side of the instrument-stability snapshots +
     the metadata-contract test. Revisit the "metadata-only" SHA note in
     `orb-view-instrument-stability.test.ts` — under this step gt.json changes too,
     so the wheelfield PNG stays byte-identical but its `gt.json` does not.
   - Re-vendor the canonical contract byte-identical.

3. **qiyas** — no round-trip logic change (the round-trip stays quiet when neither
   SVG nor gt declares a base face):
   - Re-vendor the canonical contract.
   - Exempt wheelfield cell views from the strict `data-orb-base-face` presence
     requirement in `validate_dsl_contract.py`, via the same `allow_absent` mechanism
     that already exempts ribbon views.
   - Re-record the score-neutral gt set; confirm composites do not move
     (`orb_base_face` feeds only the round-trip warning + `Contour`/facts, never the
     composite score).

4. **3d-models** — the T9 gate + build re-record land **together** (the gate is
   whole-tree and would block every commit until the build passes it):
   - Bump `build/bikar-ref.txt` to the merged bikar commit.
   - `make orbs` re-record; verify each wheelfield SVG carries `data-orb-unit` and no
     `data-orb-base-face`, and every instrument PNG stays byte-identical by md5.
   - Land the T9 base-face check in `.claude/gates/timelapse_gate.py` (prepared, see
     §4), now **simplified**: `data-orb-base-face` is always a true face, so the
     presence/range/subset check is universal with no surface-branching — wheelfield
     cells carry none, so the subset check is trivially satisfied.
   - Close #49.

## 4. Prepared work (do not lose; rebase onto latest at cascade time)

- **bikar SVG half** — branch `feat/base-face-honest-attr` (bikar worktree
  `bikar-t9scaffold`): renderer conditional split (`data-orb-unit` vs
  `data-orb-base-face` keyed on a new `OrbViewScene.baseIndexKind`), kernel + ribbon
  scene fields, CLI base-solid caller passes `'face'`, and the emitter tests. The full
  bikar suite was green in the SVG-only state (gt untouched). At cascade time, rebase
  onto current bikar master before adding step 3.2's gt-emitter change.
- **3d-models T9 base-face check** — the strict `timelapse_gate.py` (137-line diff vs
  its shipped form) is preserved as `data-orb-base-face-t9-gate.patch` beside this doc.
  It is intentionally **not** committed to `timelapse_gate.py`: committed alone it
  would block every 3d-models commit until `make orbs` re-records. It lands in step 4.

## 5. "On latest and greatest" — preconditions before starting

- Every repo on a **current master**; the prepared branches rebased onto it.
- The seven in-flight bikar worktrees are the reason for the deferral: a canonical
  contract rewrite + `GT_SCHEMA_VERSION` bump forces each to re-vendor and rebuild.
  Start the cascade when that churn is cheapest (branches landed or few in flight).
- Re-read this doc against bikar's actual `gt-emitter.ts` and qiyas's
  `validate_dsl_contract.py` at that time — the anchors here are directional, not pinned.

## 6. Verification (at cascade time)

- bikar: full suite green; orb-composite pins unmoved; wheelfield SVG has
  `data-orb-unit`, no `data-orb-base-face`; wheelfield gt omits `orb_base_face`.
- qiyas: composites read exactly the pinned values (the instrument PNG never changed);
  the base-face round-trip stays quiet on wheelfield.
- 3d-models: `make orbs` diff is only the intended attribute rename; every instrument
  PNG byte-identical by md5; the simplified T9 gate passes on the re-recorded build and
  still fails its recorded by-design case (a filler index `>= base.faces`).
