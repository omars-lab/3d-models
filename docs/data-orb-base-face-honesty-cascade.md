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
   - `make orbs` re-record against the merged bikar (`bikar-stamp` rewrites the
     gitignored `build/bikar-ref.txt` from the built checkout's HEAD); verify each
     wheelfield breakdown scaffold now carries `data-orb-unit` and no
     `data-orb-base-face`, while inscribed orbs keep `data-orb-base-face`.
   - Land the T9 check in `.claude/gates/timelapse_gate.py`, **branched on orb family**
     — the manifest's own `base` block is the discriminator (`base.faces == 0` ⟺ a
     faceless wheelfield). A lifted orb (`base.faces > 0`) keeps the base-face
     presence/range/subset check against `data-orb-base-face`; a wheelfield asks the
     same three questions of `data-orb-unit`, and treats **any** `data-orb-base-face`
     as a finding — a claim about a facet the orb does not have. (The earlier plan to
     make the check *universal* on `data-orb-base-face` was dropped once the scaffold
     itself was made honest: a wheelfield scaffold now stamps `data-orb-unit`, so the
     gate must read the unit label, not treat its absence as trivially satisfied — see
     [`docs/issues/base-face-honesty-scaffold-pivot.md`](issues/base-face-honesty-scaffold-pivot.md).)
   - Close #49.

## 4. Prepared work (do not lose; rebase onto latest at cascade time)

- **bikar SVG half** — **landed as [#170](https://github.com/NaqshCoffee/bikar/pull/170)**
  (merged to bikar `c2fa085`). The renderer conditional split (`data-orb-unit` vs
  `data-orb-base-face` keyed on `OrbViewScene.baseIndexKind`) turned out to need **two
  layers**, not one: the main polygon loop already read `baseIndexKind`, but the
  breakdown base solid renders as the *scaffold underlay* (`scaffoldElements`), which
  stamped `data-orb-base-face` unconditionally, and the `baseSolidScene` that feeds it
  hardcoded `'face'`. Both had to become family-driven (`OrbViewPlan.baseIndexKind`,
  derived per family in the CLI) or the drawn views said `unit` while the scaffold
  under them still said `base-face`. See the issue doc for the diagnosis.
- **3d-models T9 check** — lands in step 4 as a **family-branched** gate (not the
  earlier universal-on-`data-orb-base-face` form, superseded by the honest scaffold).
  `--self-test` grows a wheelfield fixture (`_make_wheelfield`) and three by-design
  mutators — a claimed face, blanked units, an orphaned unit — that must each fire.

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
- 3d-models: after `make orbs`, every wheelfield breakdown scaffold carries
  `data-orb-unit` and no `data-orb-base-face` (spot-checked DonutHexOrb: 0 base-face
  across all frames), inscribed orbs keep `data-orb-base-face` (StarOrb base frame: 10).
  The family-branched T9 gate passes on the re-recorded build (16 breakdowns, OK) and
  its `--self-test` still fires every by-design case — inscribed (a filler index
  `>= base.faces`, a label the scaffold never draws) and wheelfield (a claimed face,
  blanked units, an orphaned unit). (`build/` is gitignored — the renders ship via
  `make deploy`, so the verification is the gate on the fresh build, not a git diff.)
