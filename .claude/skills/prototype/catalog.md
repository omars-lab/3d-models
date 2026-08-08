# Orb prototype catalog

Physical-print backlog for the Islamic geometric orbs, ordered by the
learning ladder: each entry exists to answer questions the entries below it
depend on. Schema and workflow: see `SKILL.md` next to this file.

All STLs regenerate via `make orbs` in this repo (→ `build/stls/<Name>.stl`)
or `bikar render patterns/Orbs/<name>.bkr --format stl --check -o <out>`.
Every committed orb passes the mesh gate (watertight, min strut ≥ 1.2 mm FDM
floor) — these prints test *reality*, not the mesh.

## P1 — Strut coupon ladder

- **Status**: planned
- **Model**: three small Star-Orbs at `radius` 40 with `strut_width`
  1.5 / 2 / 3 (`strut_depth` at default 2.4), plated together in the slicer
  (80 mm spheres — two runs if a small bed won't take all three). Rendered
  via CLI param override (no baked `.bkr` needed; values are validated
  against the declared ranges):
  `cd bikar && for w in 1.5 2 3; do node packages/cli/dist/index.js render
  patterns/Orbs/Star-Orb.bkr --format stl --check --param radius=40 --param
  strut_width=$w -o ../3d-models/build/stls/coupons/P1-StrutCoupon-W$w.stl;
  done` — all three pass the mesh gate (watertight; minFeature 1.5 / 2 /
  2.4 mm — at width 3 the 2.4 mm *depth* is the smallest feature);
  15.8 / 20.3 / 28.2 cm³, ≈80 g PLA for the trio. Cheapest honest coupon —
  the struts meet the sphere at the same angles as a real print, which a
  flat test plate would not exercise.
- **Print target**: TBD — record machine/material/nozzle/layer on first print.
- **What we want to learn**:
  - [ ] 1. Smallest `strut_width` that prints cleanly with a 0.4 mm nozzle —
    does the param floor (1.5) and the mesh-gate FDM floor (1.2) survive
    contact with reality, or should the floor rise?
  - [ ] 2. Do thin struts on the *underside* (overhanging lattice) print as
    well as topside ones, or does the floor need to be orientation-aware?
  - [ ] 3. At R=40, do star-tip acute voids (inset-limit corners) resolve or
    fuse shut?
  - [ ] 4. Support strategy for a small sphere: tree supports' scar severity
    on strut undersides.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `strut_width`/`strut_depth` param mins in every
  `patterns/Orbs/*.bkr`; bikar mesh-gate FDM floor; Lab machine-table
  process notes.

## P2 — Star-Orb at defaults (first full orb) — harness task: "print a physical orb prototype"

- **Status**: planned (blocked on P1's answer to Q1 only if P1 fails at 3 mm)
- **Model**: `patterns/Orbs/Star-Orb.bkr` at declared defaults (R=60,
  struts 3×2.4) — `build/stls/StarOrb.stl`, 5,040 tris, 45.7 cm³.
- **Print target**: TBD.
- **What we want to learn**:
  - [ ] 1. Whole-sphere printability: does a 120 mm pierced sphere with tree
    supports come out presentable, and how bad are support scars on the
    lower hemisphere lattice?
  - [ ] 2. Print time and filament mass at defaults (feeds a "what does an
    orb cost" note for the gallery).
  - [ ] 3. Dimensional accuracy: printed diameter versus 120 mm; strut width
    versus 3 mm (calibrates whether declared mm are trustworthy).
  - [ ] 4. Handling strength: does the lattice survive support removal and
    normal handling?
  - [ ] 5. Bed contact: a sphere touches at a point — does the slicer's
    default brim/raft suffice or does the model want a flattened pole?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: harness print-prototype task; gallery print notes;
  `docs/orb-lab-design.md` §5.

## P3 — Hemisphere-split Star-Orb — harness task: "decide FDM-friendly hemisphere-split STL export"

- **Status**: planned (after P2 — needs P2's support-scar baseline to
  compare against)
- **Model**: same StarOrb.stl, cut **in the slicer** (no engine work) — both
  halves printed flat-face-down, supports off or minimal. **Cut on the
  `vertex` symmetry axis, not at the model's equator.** The authored +z axis
  is an `edge-2` axis, so "cut at z = 0" gets a 491 mm² / 16-piece
  cross-section; the `vertex` plane gives one continuous 898 mm² annulus and
  the `face` plane gives 175 mm² in 12 pieces
  ([`hemisphere-split-design.md`](../../../docs/hemisphere-split-design.md) §3.5).
- **Print target**: TBD (same machine as P2 for a fair comparison).
- **What we want to learn**:
  - [ ] 1. Does flat-down/no-support halves beat the whole-sphere print on
    surface quality enough to justify engine work? Compare against **simply
    reorienting the whole orb onto its face axis**, which clears the print
    gate's bed-contact warning for free (design doc §9.1 Option A0) — that,
    not the whole-sphere print in its authored orientation, is the bar.
  - [ ] 2. Seam: how visible is the glued seam, and what does the **annular**
    `vertex`-plane cross-section actually achieve per mm²? (Predicted ~2.2 kN
    in tension on 898 mm² at the coupon literature's 2.46 MPa, against a 57 g
    orb — so the open question is whether a hand-glued lattice seam gets
    anywhere near the coupon figure, not whether the area is sufficient.)
  - [ ] 3. Alignment: how hard is registering two lattice halves by hand —
    would an engine split need registration pins/keys to be usable? (Note a
    `vertex` annular rim should be largely self-jigging; note also that a pin
    *in a strut* is ruled out by geometry — 0.6 mm socket ceiling against a
    2 mm minimum printable hole.)
  - [ ] 4. Where should the cut land: **`vertex` vs `face`** — the former
    maximises seam strength and bed contact, the latter minimises seam
    visibility, and they are opposed. Print both if budget allows; this is the
    one question a print answers better than analysis. (Constrains the engine
    design if we build it.)
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: the harness split-export decision task — its verdict
  (build / don't-build / build-with-pins) comes from here.

## P4 — Rosette-Orb (fine-feature fidelity)

- **Status**: planned (after P2)
- **Model**: `patterns/Orbs/Rosette-Orb.bkr` at defaults (dodeca 10-petal,
  R=60, inner 38, shoulder 60) — `build/stls/RosetteOrb.stl`, 47.0 cm³.
- **Print target**: TBD.
- **What we want to learn**:
  - [ ] 1. Do the petal-zigzag sliver voids near the inner ring resolve, or
    fuse into a solid core disc?
  - [ ] 2. Reality-check the knob envelope: defaults print — but does
    `inner` at its 16 mm floor produce printable geometry, or should the
    range floor rise? (One extra small print if defaults pass.)
  - [ ] 3. Is the rosette family visually worth being the Lab's default
    preset in the flesh, or does the simpler Star lattice print prettier?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `inner`/`shoulder` ranges in Rosette-*.bkr; Lab default-preset
  choice.

## P5 — Weave family (chainmail clearance) — validates the Lab's FDM weave notice

- **Status**: planned (after P1 — needs the real min-strut answer first)
- **Model**: `patterns/Orbs/Rosette-Weave-Orb.bkr` (10 interlocked ribbons,
  amplitude 1.6, depth 2.4 → 0.8 mm ribbon gap, 27.9 cm³); Weave-Orb
  (26 strands) as the harder follow-up.
- **Print target**: TBD — expected to *fail or disappoint on FDM*; an
  SLS/MJF service order (the Lab's service presets) is part of this entry.
- **What we want to learn**:
  - [ ] 1. Does FDM at 0.8 mm gap print interlaced free-moving ribbons, fuse
    them, or fill the gap with support that can't be removed?
  - [ ] 2. Is the Lab's tier-3 "weave on a filament machine" warning correctly
    calibrated — should it soften (it prints fine), harden (block STL), or
    stay advisory?
  - [ ] 3. SLS/MJF service result at the same gap: quality, cost, lead time —
    the number the Lab's service-preset note should quote.
  - [ ] 4. Do free ribbons make the orb feel like chainmail (a feature) or
    like a rattle (a defect)? Sets the `amplitude` default philosophy —
    fused-solid versus free-moving.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: Lab weave/FDM notice copy; `amplitude` defaults in Weave-*.bkr;
  ribbon-gap ✓/fused threshold (currently 0.4 mm) in the Lab gate rows.

## P6 — Size extremes (R=40 and R=110)

- **Status**: planned (after P2)
- **Model**: Star-Orb with `radius` baked to 40, then 110 (Lab bake →
  Download `.bkr`).
- **Print target**: TBD — R=110 (220 mm sphere) needs a machine whose
  build volume clears the Lab ceiling rule `2R ≤ min(XYZ) − 10`.
- **What we want to learn**:
  - [ ] 1. R=40: do features shrink gracefully, or does the radius floor
    need to rise from 40?
  - [ ] 2. R=110: warp/adhesion/time at full plate — is the ceiling rule's
    10 mm margin enough in practice?
  - [ ] 3. Does strut *width* need to scale with radius for visual balance
    (struts constant-mm look chunkier on small orbs)? If yes, param
    defaults may want a radius-linked note.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `radius` range in every orb script; Lab ceiling-margin rule.

## P7 — Material and finish pass

- **Status**: planned (last — pure aesthetics, needs a proven geometry)
- **Model**: whichever orb P2–P4 crowned as the best printer.
- **Print target**: TBD — candidates: silk-gold PLA (matches the gallery's
  gold renders), PETG (sunlight/ornament durability), resin (if any fine
  detail failed FDM).
- **What we want to learn**:
  - [ ] 1. Which material/finish best matches the gallery's gold-render
    aesthetic in person?
  - [ ] 2. Does the choice change print settings enough to warrant per-
    material notes in the Lab's machine table?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: gallery photography of real prints; Lab machine-table notes.

## P8 — Maclado orbs (Family 3: the 9-spike wheel field)

- **Status**: planned (after P1 for the real min-strut answer; the weave
  preset also wants P5's ribbon-gap answer first)
- **Model**: `patterns/Orbs/Maclado-9.bkr` (genus-379 pierced shell, 20
  nine-wheels on the dodecahedron vertices, struts 2 × 2.4, 86.8 cm³ at
  R=60 → `build/stls/Maclado9.stl`, 9,312 tris) and
  `patterns/Orbs/Maclado-9-Weave.bkr` (46 free ribbon loops over 390
  alternating crossings, ribbon 1.2 × 1.2, amplitude 0.8, 8.6 cm³ →
  `build/stls/Maclado9Weave.stl`, 7,200 tris). Design:
  `docs/maclado-orb-design.md` §7.
- **Print target**: TBD — **assumes a ~0.4 mm-class nozzle**. That is §7's
  K10 condition, not a preference: the 2.0 mm unsupported-thin-wall default
  is nozzle-relative, so a 0.2 or 0.8 mm nozzle shifts the floor and this
  sheet must be re-derived before printing on one. Record machine/material/
  nozzle/layer on first print. `--check print` findings to plan around:
  the solid passes with the sphere-tangency F7 warning only (3.8 mm²
  first-layer contact — brim or raft); the weave adds F3 mid-air ribbon
  spans near the top pole (supports required) on top of the same F7.
- **What we want to learn**:
  - [ ] 1. Do the 2 mm struts survive as *unsupported* thin walls across the
    wheel spans? §7's 2.0 mm default is a starting geometry, not a
    measurement — this print is what graduates it into a calibrated bet,
    or kills it.
  - [ ] 2. The weave ribbon (1.2 mm) sits exactly on the mesh gate's FDM
    floor: does it print at all, and do 390 crossings at amplitude 0.8 stay
    free or fuse (the script's fusion bound: amplitude ≥
    (ribbon_depth + 0.4) / 2)?
  - [ ] 3. Do the twelve 30-gon filler windows print clean rims, or does the
    wheel/filler boundary need a raised strut floor?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `strut_width`/`ribbon_width`/`ribbon_depth`/`amplitude`
  defaults in both Maclado `.bkr` scripts; §7's **Default** (graduation to
  a `CAL-*` bet per the calibrate ceremony); the Lab weave/FDM notice if
  maclado's numbers disagree with P5's.

---

# Machine characterization card (MC-series)

The MC-series measures the **printer**, not a design. Fit gap, hole compensation,
minimum feature, bridge span, overhang angle, warp and bed contact are properties
of *(machine, material, nozzle, slicer profile)* — a value measured on one tuple
is an anecdote on another, and measuring them inside a clip coupon, a brick coupon
and an orb coupon separately is measuring the same printer three times. One card
settles the shared substrate; every design coupon then tests only what is
genuinely design-specific.

**This series sits ahead of every other entry in the learning ladder** — ahead of
W-F1 and LG-F1 below, which consume its numbers, and ahead of P1 above, whose Q1
is MC-2's question asked in strut form. Each entry names the `CAL-…` bets it
settles; the registry is `.claude/skills/calibrate/bets.md` and the ceremony that
closes a bet is the `calibrate` skill (bikar Tenet 30 — a physical constant is not
earned until it records its provenance).

- **Model**: all six live in `bikar/patterns/Coupons/Machine-Card.bkr`, one piece
  per rung so that rung identity survives into the filename — bikar cannot emit
  text, so a coupon cannot label itself and monotone size ordering plus `--piece`
  is the substitute. MC-1 **extends** `patterns/Coupons/Fit-Coupon.bkr` rather
  than replacing it: that file's ⌀3 ladder is correct as far as it goes, and the
  card adds the ⌀ sweep `holeCompMm` actually needs.
- **Authored blind.** No machine exists yet, so every rung range below is a
  bracket around an unknown, not a prediction. A ladder that turns out to need
  re-centring is a **result** — log it and re-cut, per the `calibrate` rules.
- **Print target** for the whole series: record the full profile header from
  `.claude/skills/calibrate/protocol.md` (machine, material *and colour*, spool,
  nozzle ⌀ and type, layer height, profile verbatim, ambient, date, caliper)
  before anything is measured. That header **is** the deliverable; the numbers
  are meaningless without it.
- Print the whole card in one job where the bed allows, so all six readings share
  one profile header. Two jobs means two headers.

## MC-1 — Bore and fit plate (⌀ sweep + fit-class ladder)

- **Status**: planned (no machine yet)
- **Model**: `bikar/patterns/Coupons/Machine-Card.bkr` — **two** plates, because
  they ask two questions. `MC1BoreSweep` sweeps **⌀3 / 4 / 5 / 6 / 8 / 10 mm** to
  see whether bore drift depends on diameter (which a single scalar `holeCompMm`
  assumes it does not); `MC1FitLadder` holds one reference ⌀ and walks the four
  clearance classes — press / snug / sliding / free — at the gaps
  `kernel3d/fit-profile.ts` declares, plus a line-to-line zero for an origin.
  `MC1FitGauge` and `MC1Pin03/04/05/06/08/10` are the mating pins. Full render
  commands: `docs/calibration-design.md` §6 — **always pass `--piece`**, since
  without it the CLI renders the `MC1Fit` assembly as one mesh (a plate and a
  loose pin fused into a single useless STL).
- **Print target**: TBD — profile header per the series note.
- **Settles**: `CAL-FIT-01` (the `FIT_GAP_MM` press/snug/sliding/free ladder) and
  `CAL-HOL-01` (`holeCompMm` 0.20/0.25).
- **What we want to learn**:
  - [ ] 1. Realised vs authored bore at each ⌀ — **two orthogonal diameters per
    bore** (FDM bores are not round, and the X/Y difference is the anisotropy the
    fit classes live or die by). This is `holeCompMm`, and whether one number
    covers the whole ⌀ range or it varies with diameter.
  - [ ] 2. Which gap seats as *press*, *snug*, *sliding*, *free* by hand, judged
    on `protocol.md`'s four definitions and recorded with **who judged it** — a
    hand calibration is worthless without the hand.
  - [ ] 3. Does the literature ladder (−0.10 / +0.05 / +0.15 / +0.35) land on this
    machine at all, or do the credible looser sources (2–10× wider) win here?
    Both design docs that carry this bet expect the coupon, not the literature,
    to be the arbiter.
  - [ ] 4. Is the compensation separable from the intent, as the architecture
    assumes — i.e. does one compensation number plus the ladder reproduce the
    measured fits, or do they interact?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `FIT_GAP_MM` and `holeCompMm` in `bikar` `kernel3d/fit-profile.ts`
  (value **and** provenance record); `docs/c2-assembly-design.md` Appendix B.3 and
  B.6; `docs/piece-composition-design.md` Appendix B.2 — the same bet as c2 B.3,
  which is why one plate closes both; W-F1's blade-clearance conversion.

## MC-2 — Wall ladder (minimum printable feature)

- **Status**: planned (no machine yet)
- **Model**: seven `tube` rungs, wall **0.4 / 0.6 / 0.8 / 1.0 / 1.2 / 1.6 /
  2.0 mm** (wall = (outer − inner)/2), one piece per rung —
  `MC2Wall04 / 06 / 08 / 10 / 12 / 16 / 20`. The rung is in the piece name, not a
  parameter: the wall is what is being measured, so it is authored literally.
  Full render commands: `docs/calibration-design.md` §6.
- **Print target**: TBD — profile header per the series note.
- **Settles**: `CAL-FEA-01` (`DEFAULT_MIN_FEATURE_MM`, currently 1.2).
- **Sub-floor note**: the 0.4–1.0 mm rungs sit **below** the 1.2 mm mesh-gate
  floor, so `--check` reports FAIL on them **by design** — that is the coupon's
  whole point, and it is the same posture as the W-series clip blade and the
  LG-series tube wall. Render those rungs without `--check`; record the FAIL as
  expected, not as a defect. No `--min-feature` override flag exists and none is
  added.
- **What we want to learn**:
  - [ ] 1. The thinnest wall that prints as a continuous, handleable feature —
    the number that either confirms the 1.2 mm floor or moves it.
  - [ ] 2. **In which direction the error runs.** Brick Architect reports printed
    walls coming out *too thick*; measure realised vs authored at every rung
    rather than assuming thin-and-missing is the only failure.
  - [ ] 3. Where the slicer stops emitting a distinct feature and starts merging
    perimeters — inspect the sliced preview *and* the part, because the two
    disagree and only the part counts.
  - [ ] 4. Does the answer move with wall *height* (a short wall is stiffer than a
    tall one), or is a single floor honest?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `DEFAULT_MIN_FEATURE_MM` in `bikar` `kernel3d/mesh-gate.ts` (value
  **and** provenance record); `docs/lego-lab-design.md` Appendix B.5 and the §7.4
  `minFeatureMm: 0.8` override; P1 Q1 and LG-F1 Q5, both of which ask this
  question in design-specific form.

## MC-3 — Bridge plate (unsupported span)

- **Status**: planned (no machine yet)
- **Model**: one plate, `MC3BridgePlate` — 160 × 34 × 6 mm with eight **blind**
  bores that open on the *bottom* face and stop 2 mm short of the top, so the
  remaining ceiling must bridge the bore ⌀ and **span is the diameter**. Spans
  **4 / 6 / 8 / 10 / 12 / 16 / 20 / 25 mm**. `--check` PASS expected — but see
  below. The ladder runs past the shipped 10 mm rule on purpose: `w2` B.3 has
  already collected the counter-evidence (Multiboard demands 30 mm, community
  guidance 20–25, UltiMaker 25 in Tough PLA), so a ladder stopping at 12 could not
  fail and would cost a print to learn "higher than 12". 10 mm sits fourth from
  the bottom, bracketed on both sides. Full render command:
  `docs/calibration-design.md` §6.
- **Print target**: TBD — profile header per the series note. **Orientation is
  the measurement**: plate flat, +z up, **bore mouths on the bed**. Flipped, every
  bore is an ordinary pocket opening upward with nothing to bridge, and the coupon
  answers a question nobody asked.
- **What `--check` cannot see**: it reports `minFeature = 4.5 mm`, the margin
  beside the ⌀25 bore. The 2 mm bridged ceiling is not in the min-feature
  computation at all, so the gate is silent about the one dimension this coupon
  is built around. Do not read its PASS as an opinion on the ceiling.
- **Settles**: `CAL-BRG-01` (the ≤10 mm bridge rule).
- **What we want to learn**:
  - [ ] 1. The first rung that **sags** — not the first that fails. The usable
    limit is the last clean one; a drooping-but-present ceiling is still a defect
    in a cosmetic seat.
  - [ ] 2. Does the conservative 10 mm rule survive, or is it 2–3× tighter than
    this machine needs (Multiboard's shipped snaps demand 30 mm, community
    guidance says 20–25 mm)?
  - [ ] 3. Does the droop consume the clearance under the ceiling — the failure
    mode that matters for a cavity roof, as opposed to cosmetic sag.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: the bridge-span constant in `bikar` `kernel3d/print-gate.ts` (value
  **and** provenance record); `docs/w2-connector-design.md` Appendix B.3 and §4
  Q4; `docs/lego-lab-design.md` §3.6 (`engage`, whose 3.2 mm default rests on the
  cavity ceiling bridging cleanly) and §11 Q4.

## MC-4 — Overhang fan

- **Status**: planned (no machine yet)
- **Model**: one `revolve`d shell, `MC4OverhangFan`, that flares outward as it
  rises so its **underside** is the test surface — six conical bands of 4 mm rise
  at **20 / 30 / 40 / 45 / 50 / 60°** from vertical, separated by 1 mm vertical
  risers. 29 mm tall, top ⌀65.6 mm. (A true cone is rejected by the C1 ring-solid
  rule; the banded form is the legal one and its risers double as rung identity in
  the hand.) `--check` PASS expected. Full render command:
  `docs/calibration-design.md` §6.
- **Print target**: TBD — profile header per the series note. **Supports off**,
  and say so on the sheet: an overhang number measured with supports is not an
  overhang number.
- **Settles**: `CAL-OVH-01` (the F5 overhang threshold).
- **What we want to learn**:
  - [ ] 1. The first angle showing curl or droop — surface quality per angle,
    photographed, not just pass/fail.
  - [ ] 2. Does the shipped-slicer *auto* rule (overhang = half extrusion width
    per layer, so the effective angle follows layer height) beat a fixed angle
    here? Print the fan at two layer heights if the plate allows — that
    comparison is what decides whether the gate's default should be auto or
    fixed.
  - [ ] 3. Record the convention **explicitly** with the reading (from vertical
    vs from horizontal). At 45° the two coincide, which is exactly how convention
    bugs hide.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: the overhang threshold in `bikar` `kernel3d/print-gate.ts` (value
  **and** provenance record); `docs/print-validation-design.md` Appendix B.2 and
  the F5 tier split in §3.

## MC-5 — Warp plate

- **Status**: planned (no machine yet)
- **Model**: one thin `extrude`, `MC5WarpPlate` — 120 × 80 × 1.6 mm (eight layers
  at 0.2), using Fit-Coupon's guide-circle-quartered rectangle idiom (the
  blueprint has no rectangle primitive). `--check` PASS expected. One part, four
  corners measured — there is no ladder here. **No features**: no ribs, no
  lightening holes, nothing that locally changes stiffness, because that would
  turn the measurement into a property of the feature. The one exception is a ⌀3
  **fiducial** near one corner, so "corner A" means the same corner on the next
  print and the next machine — A is nearest the fiducial, then B, C, D clockwise
  from above. Full render command: `docs/calibration-design.md` §6.
- **Print target**: TBD — profile header per the series note, **plus** brim/raft
  and part-fan settings verbatim, since those are precisely what the conflicting
  sources disagree about.
- **Settles**: `CAL-WRP-01` (`warpMm`, currently `undefined`).
- **What we want to learn**:
  - [ ] 1. Gap at **each of four corners** on a flat reference (granite plate or
    float glass) by feeler gauge. Record all four, not the worst — the *pattern*
    distinguishes warp from a bed-levelling artifact, and only one of those is
    the number being sought.
  - [ ] 2. Does it differ by material? PLA vs PETG on the same plate is one extra
    print and settles a claim the sources flatly contradict each other on (Prusa's
    guide says PETG "does not shrink or warp"; WhyItFailed quotes 0.5–0.7%
    contraction).
  - [ ] 3. Does the bow relax over days, or is the as-printed number the number?
  - [ ] 4. Does a brim change it enough to be worth mandating in the print notes?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `warpMm` in `bikar` `kernel3d/fit-profile.ts` — today literally
  `undefined` pending this measurement (value **and** provenance record);
  `docs/w2-connector-design.md` Appendix B.5; W-F1 Q2, which is re-pointed here
  rather than re-measuring the printer.

## MC-6 — Bed-contact towers

- **Status**: planned (no machine yet)
- **Model**: four `rod` towers, ⌀ **3 / 5 / 8 / 12 mm** × 40 mm tall — one line
  each, one piece each: `MC6Tower03 / 05 / 08 / 12`. Constant height is what makes
  this a **contact-area** ladder rather than an aspect-ratio one. Render with
  `--check print` rather than bare `--check`: the slice simulation is what
  exercises F7, the trigger under test. It already confirms the bracket lands
  where intended — 7.1 and 19.6 mm² warn F7, 50.2 and 112.9 mm² are clean, so the
  25 mm² threshold falls between rungs 2 and 3. Full render command:
  `docs/calibration-design.md` §6.
- **Print target**: TBD — profile header per the series note, **plus** whether a
  brim/raft was used. **Bare plate, no brim, no raft**: a brim is precisely the
  mitigation F7 exists to recommend, so printing with one measures the brim
  instead of the threshold.
- **Settles**: `CAL-BED-01` (`MIN_BED_CONTACT_MM2` 25 mm² / footprint ratio 0.01)
  — but only half of it directly. `MIN_BED_CONTACT_RATIO = 0.01` is **untestable
  on a straight rod**: a rod's first layer *is* its widest layer, so the ratio is
  100% on all four towers. It rides the same bet and gets settled by inference
  from the absolute figure, not measured. Recorded as a weakness of this coupon in
  `docs/calibration-design.md` §8, not papered over.
- **What we want to learn**:
  - [ ] 1. Which towers survived to full height and which detached — and, if
    observed, at what point in the print. A tower that let go at 30 mm is a
    different result from one that never stuck.
  - [ ] 2. The smallest footprint that holds a 40 mm column, which is the number
    `MIN_BED_CONTACT_MM2` currently guesses at.
  - [ ] 3. Elephant's foot at the base of each tower, measured deliberately here
    so it does not contaminate every other coupon's readings.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `MIN_BED_CONTACT_MM2` and the footprint-ratio rule in `bikar`
  `kernel3d/print-gate.ts` (value **and** provenance record); P2 Q5, the
  point-contact sphere question, which inherits the threshold from here.

## MC-7 — Rung labels (engrave vs emboss)

- **Status**: model to author — needs the `text` statement, which does not exist
  yet (`docs/text-emit-design.md` §8 milestone T2). Listed here now because
  `CAL-TXT-01` and `CAL-TXT-02` name this coupon as what settles them, and a bet
  whose coupon is not written down anywhere is the W-F1 defect over again.
- **Model**: `bikar/patterns/Coupons/Text-Coupon.bkr` — one plate carrying the
  same six labels twice, engraved on one half and embossed on the other, at three
  relief depths. The labels are the real ones, not lorem: `MC-4 R12` is the string
  that fails the §5 gap validator in Arial Bold at a 5 mm cap (0.181 mm between
  the `-` and the `4`), so the plate must carry the shipping face's rendering of
  it and not the failing one.
- **Print target**: TBD — profile header per the series note. Print **flat on the
  plate, no supports**: an engraved label's floor and an embossed label's first
  layer are both first-layer features, and tilting the part measures the tilt.
- **Settles**: `CAL-TXT-01` (relief direction) and `CAL-TXT-02` (cap height 5.0 mm
  / relief depth 0.6 mm). Both are provisional and neither carries a `Calibrated`
  record in bikar yet — they govern 3d-models design-doc defaults, which is the
  same shape as `CAL-OVH-01`.
- **What we want to learn**:
  - [ ] 1. Engraved or embossed — which is actually readable at arm's length on a
    matte PLA surface. `docs/text-emit-design.md` §6 bets engraved and says
    plainly that it is a coin flip; §1.2 records that the sources disagree.
  - [ ] 2. The smallest cap height that still reads. 5.0 mm is the height the §5
    measurements were taken at and the smallest at which a bold face's thinnest
    stem clears one nozzle width with margin — it is **not** a legibility
    measurement, because none was made.
  - [ ] 3. Whether 0.6 mm of relief is enough, too much, or irrelevant. Three
    depths on one plate is what makes this answerable in one print.
  - [ ] 4. What the slicer does to a counter — the enclosed void in `0`, `4`, `A`
    — at these sizes. §7 Q3 records that nothing was printed and no slicer was
    run, and calls this the single largest gap in the investigation.
  - [ ] 5. Whether an engraved label near a measurand contaminates it. §7 Q5:
    MC-2's measurand *is* a minimum feature size, so a label cut into it is not
    obviously harmless, and this plate is where that gets decided before the
    labels go onto the other 23 rungs.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `docs/text-emit-design.md` §6's three defaults (value **and**
  provenance record, once the constants exist), and `docs/calibration-design.md`
  §8's "rung identity does not survive onto the part" — the weakness this whole
  line of work exists to close.

---

# Tile-wall connector ladder (W-series)

The W-series validates the **modular tile-wall** work (design docs
`docs/tile-wall-design.md`, `docs/w2-connector-design.md`), not the orbs.
These coupons decide the connector grammar — clipseat fit and the printed
CornerClip — in plastic before any full wall is committed. Same learning-ladder
rule: the fit coupon (W-F1) settles the blade clearance the clip coupon (W-C1)
then builds on. Printing is **on hold** (design doc §8), so both land `planned`.

Sub-floor note for this whole series: a printed `clip`'s bayonet blade is
~0.6 mm, below the 1.2 mm FDM mesh-gate floor — so `--check` on a **clip part**
reports FAIL *by design*, and that thin flexing blade is exactly what these
coupons validate in plastic (design doc §10 Q1). The **tiles** pass the gate
cleanly (the clipseat rebate is a supported step the gate excludes, not a
free-standing strut). Only the clip is exempt, and only where noted.

## W-F1 — Clipseat fit coupon (blade clearance ladder)

- **Status**: planned (printing on hold, design doc §8)
- **Model**: `bikar/patterns/Coupons/Clipseat-Fit-Coupon.bkr` — one 40 mm
  clipseat dummy tile plus five `CornerClip`s across a blade-clearance ladder,
  to find the clearance that seats firmly without forcing.
  **This is not `Fit-Coupon.bkr`.** Until 2026-08-02 this entry pointed there,
  which is a bore-and-pin ladder: a peg going straight into a hole, one axis,
  full contact, no rotation. The clip joint is a blade dropping down the gap
  channel between four tiles and *then* sweeping sideways under load — it can
  pass the drop and still bind on the twist, so a number measured on a bore
  does not transfer here. That is the whole reason the new file exists; see
  `docs/decisions-log.md` **D-008**.
  Print **four** of the tile — they serve W-C1 afterwards, being the same dummy
  `Clip-Coupon.bkr` uses — and one of each clip:
  `cd bikar && node packages/cli/dist/index.js render
  patterns/Coupons/Clipseat-Fit-Coupon.bkr --format stl --piece FitClipTile
  --check -o ../3d-models/build/stls/coupons/W-F1-FitClipTile.stl`, then the
  same per clip with `--piece FitClipC40` … `FitClipC00` and **without**
  `--check` (a bayonet blade is sub-floor by design — see the series note
  above). Cheapest connector coupon: it fixes the clearance number that every
  later clip coupon and the full Clip-Wall inherit via `--fit-profile`.
  The tiles are laid at **one** physical channel (`wall_gap`, default 1.2); the
  ladder is on the clip, and the difference between declared and actual gap is
  the clearance under test. Rung names are that clearance in hundredths of a
  mm — `C40` 0.40 / `C30` 0.30 / `C20` 0.20 (the shipped guess) / `C10` 0.10 /
  `C00` 0.00 — and stay correct if `wall_gap` moves.
- **Print target**: TBD — record machine/material/nozzle/layer on first print.
  Clips in PETG (the intended clip material); print the tile in the wall's tile
  material (PLA or PETG) so its shrinkage matches the channel you will have.
- **What we want to learn**:
  - [ ] 1. Which rung drops through and twists home firmly without forcing on a
    0.4 mm nozzle — i.e. the diametral blade clearance that becomes
    `CLIP_CLEARANCE_MM.insert` and the `gap` to declare
    (`profile.gapMm` / `--fit-profile petg_calibrated`)?
    **The ladder is built to be able to fail at both ends.** If `C00` — whose
    blade exactly fills the channel — drops through, the answer is not
    "0.00 works": it is that this machine undersizes the blade or oversizes the
    channel, and the reading measures *that* error. If `C40` drops freely but
    shears on the twist, the blade has stopped being a structural member.
  - [ ] 2. **Re-pointed to `CAL-WRP-01` / MC-5.** `profile.warpMm` is a property
    of *(machine, material, nozzle, profile)*, not of a clipseat tile — measuring
    it here would measure the printer a second time. The warp plate supplies the
    baseline. What stays W-F1's is the design-specific remainder: does a tile
    carrying a clipseat rebate bow **more** than the MC-5 plate at the same
    profile, i.e. does the rebate itself add bow, and does a corner jaw still
    bear evenly on the result? Compare against MC-5; only the difference is a
    finding here.
  - [ ] 3. Does the clearance need to differ by tile material (PLA vs
    PETG shrinkage), or is one `gap` good for both?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Settles**: the clip-joint half of `CAL-FIT-01` only. The four fit classes
  and the ⌀ sweep come from MC-1; W-F1 converts them into a blade clearance for
  *this* joint. Warp (Q2) belongs to `CAL-WRP-01` / MC-5.
- **Does not settle**: the Z stack — riser height, anti-rattle preload,
  back-flush setback — which is `CAL-CLP-01`, and the detent feel, which is
  `CAL-DET-01`; both are W-C1's. Nor rebate-vs-proud, W-C1's headline decision:
  this coupon uses `rebate` because the blade clearance is set by the gap
  channel alone and the variant only changes the jaw pad's thickness, so the
  ladder reads the same either way.
- **Confound, stated**: the declared gap sets the blade width *and*
  `rPadOutMm = rJaw − gap/√2`, the pad's reach over the border band. The two
  move together and the coupon reports the pair, which is fine — the
  deliverable is one number to declare, not a decomposition. A failed rung
  still says which effect bit: a blade that will not enter is the blade; a clip
  that enters, twists, then rocks or pulls off is the reach.
- **Feeds**: `--fit-profile` clearance profile consumed by
  `patterns/Coupons/Clip-Coupon.bkr` and `patterns/Walls/Clip-Wall.bkr`;
  `CLIP_CLEARANCE_MM` in `bikar` `kernel3d/corner-clip.ts`; clipseat constants
  in `bikar` `kernel3d/clipseat.ts` if the seat floor moves.

## W-C1 — CornerClip coupon (rebate-vs-proud joint decision)

- **Status**: planned (printing on hold, design doc §8; blocked on W-F1's
  blade-clearance number)
- **Model**: `bikar/patterns/Coupons/Clip-Coupon.bkr` — two 40 mm dummy tiles
  (one `clipseat rebate 0.6`, one `clipseat proud`) plus the `CornerClip` that
  mates them. There is no `assembly` (a bayonet clip has no connectable port),
  so render each part by name:
  `cd bikar && node packages/cli/dist/index.js render
  patterns/Coupons/Clip-Coupon.bkr --format stl --piece CouponTileRebate
  --check -o ../3d-models/build/stls/coupons/W-C1-TileRebate.stl` (and
  `--piece CouponTileProud --check`, then `--piece CouponClip` **without**
  `--check` — its blade is intentionally sub-floor). Print four of each dummy
  and a handful of clips, build two real four-corner joints (one rebate, one
  proud), and decide the clipseat default in plastic. Add
  `--fit-profile petg_calibrated` once W-F1 has set the profile.
- **Print target**: TBD — clips in PETG (`material petg`), dummy tiles in the
  wall's tile material. Record machine/material/nozzle/layer on first print.
- **What we want to learn**:
  - [ ] 1. **§10 Q1 — the clipseat default**: rebate vs proud in raking
    light on a real four-corner joint — which reads cleaner and hides the
    clip better? (This coupon's headline decision.)
  - [ ] 2. Does the CornerClip's bayonet detent have a positive past-center
    "click" feel, or does it seat mushy / not hold?
  - [ ] 3. Does the ~0.6 mm PETG jaw blade survive repeated seat/unseat
    cycles, or fatigue/snap — i.e. is the sub-floor blade printable-and-durable
    in practice, validating the mesh-gate exemption?
  - [ ] 4. Front-face lippage across the joint — do adjacent tiles sit flush,
    or does the clip pull a step between them?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Settles**: `CAL-DET-01` (the 0.3–0.5 mm detent band, `docs/w2-connector-design.md`
  Appendix B.6) — design-specific, deliberately **not** on the machine card, since
  a detent depth is a property of this clip's bayonet, not of the printer.
- **Feeds**: the clipseat grammar default (rebate vs proud) in
  `docs/w2-connector-design.md` §10 and every `clipseat` in
  `patterns/Walls/*.bkr`; the mesh-gate sub-floor exemption for bayonet clips
  (`bikar` `kernel3d/corner-clip.ts` minFeature) if Q3 disproves durability;
  `patterns/Walls/Clip-Wall.bkr` as the first full wall once the joint is
  proven.

## W-P1 — Frame band ladder (how wide reads as a margin)

- **Status**: planned (printing on hold, design doc §8). **Not blocked on
  W-F1 or W-C1** — the frame is a proportion, not a joint, so it needs no
  clearance number and can be printed the day the queue opens.
- **Model**: `bikar/patterns/Coupons/Frame-Band-Coupon.bkr` — one 60 mm
  octagram `FrameTile` and a `FrameWall` whose 2×2 field is held fixed at
  121.2 mm while the boundary grows with `$band`. Rungs are the band in mm:
  **B06 / B12** (the shipped guess) **/ B20 / B30**. Render one 1:1 SVG per
  rung and **one** printable module:
  `cd bikar && node packages/cli/dist/index.js render
  patterns/Coupons/Frame-Band-Coupon.bkr --format svg --param band=6
  -o ../3d-models/build/svg/coupons/W-P1-B06.svg` (and `band=12`, `band=20`,
  `band=30`), then
  `node packages/cli/dist/index.js render
  patterns/Coupons/Frame-Band-Coupon.bkr --format stl --piece FrameTile
  --check -o ../3d-models/build/stls/coupons/W-P1-FrameTile.stl`.
  Print **four** `FrameTile`s — the same four serve every rung.
- **The band is not a printed part, and that is stated on purpose.** W3
  renders the frame as the ring between the boundary rect and the field
  rect; there is no frame geometry to slice, so a coupon that claimed a
  printed band would be prescribing a part that does not exist. The reading
  is taken on the four printed tiles laid out at the wall's 1.2 mm field
  spacing on top of each rung's SVG at 1:1 — the plastic supplies the
  tile's real depth and sheen, the paper supplies the margin under test.
- **Print target**: TBD — record machine/material/nozzle/layer on first
  print. Any wall tile material; the finding is proportion, not fit.
- **What we want to learn**:
  - [ ] 1. Which rung first reads as a deliberate margin rather than as a
    wall that ran out of tiles, in raking light at ~2 m? That band is
    `CAL-FRM-01` / `FRAME_BAND_MM`.
    **The ladder is built to be able to fail at both ends.** If **B06**
    already reads as intentional, the shipped 12 mm is over-wide and the
    wall is giving up a tile's worth of field for nothing. If **B30** still
    reads thin, the default is under-scaled to the module and the number
    should track module size rather than be a constant at all — which is a
    change to the *shape* of the constant, not to its value.
  - [ ] 2. Does the answer move with viewing distance? A band judged at arm's
    length and a band judged across a room are different findings, and the
    wall is hung, so the room distance is the one that governs.
  - [ ] 3. Does `frame absorb`'s solved band (often much wider than 12 mm —
    40.6 mm on the doc's 486 × 323.6 worked example) still read as a frame,
    or as an empty border? If it reads empty, `absorb` is a fit tool and not
    a finish tool, and the language reference should say so.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Settles**: `CAL-FRM-01` — the wall perimeter trim band, the only bet
  this coupon carries.
- **Does not settle**: anything about the joint. The frame changes no
  clearance, no gap and no clipseat, so W-F1's and W-C1's numbers are
  untouched by whatever this reads.
- **Feeds**: `FRAME_BAND_MM_CAL` in `bikar`
  `packages/core/src/kernel/wall-frame.ts`, which is what a bare `frame`
  resolves to; the **Perimeter frame (W3)** section of `bikar`
  `docs/language-reference.md`; and `docs/tile-wall-design.md` §10 Q2.

# LEGO-compatible brick ladder (LG-series)

The LG-series validates the **Lego Lab** work (design doc
`docs/lego-lab-design.md`, survey `docs/research/lego-brick-system-survey.md`) —
turning a bikar pattern into a 3D-printed part that clutches into real LEGO at
true 8 mm scale.

**Why this series blocks its engine phase harder than any other.** LEGO's clutch
is authored from a tangency condition (US 3,005,282) but *realised* as an elastic
interference — measured studs run 4.88–4.89 mm against a 4.8 nominal, and LEGO's
own designers call the joint "an interference fit". No source publishes a
metrologically-obtained anti-stud tube diameter, and no source anywhere publishes
caliper measurements on a *printed* stud or a clutch durability cycle count.
Meanwhile FDM part-to-part repeatability on a 5 mm feature is σ ≈ 0.02 mm and a
fit clearance is a difference of two such features, so no single authored
dimension lands reliably. **No usable clutch dimension can be derived on paper.**
LG-F1 and LG-F2 therefore block M6's geometry outright (design doc §8, §10), the
way W-F1 blocks W-C1 — and LG-F2/LG-D1 would be the first public data of their
kind.

**Every coupon in this series mates a printed part to a real LEGO part; LG-S1 is
the one that does not.** Two printed bricks stacked on each other apply the fit
profile's diametral offset twice — once per side — where a moulded mating part
applies it once, and on the shipped defaults that cancels the interference
entirely. The series therefore splits along the *joint*, not along the feature:
LG-F1/LG-F2/LG-R1 settle printed-to-moulded, LG-S1 settles printed-to-printed,
and neither result may be quoted for the other without a sentence saying why it
transfers.

**The architecture these coupons test (post-audit, design doc §3.8/§7.6).**
Geometry is authored *loose* — every mating surface takes −0.1 mm/side of global
clearance — and grip comes back as a **discrete compliant rib**: four lobes on
each tube's outer ring facing the studs it clamps, plus wall lobes at each
stud-facing position. Same architecture as the W2 detent rib, and the same as
MachineBlocks' shipped clamp bands. So the parameter the ladder sweeps is **rib
thickness, not bore diameter** — the bore is deliberately not the fit surface.

Sub-floor note for this whole series: the anti-stud tube wall is
(6.514 − 4.8)/2 = **0.857 mm**, below the 1.2 mm FDM mesh-gate floor, and the
clutch rib protrudes only 0.1 mm — so `--check` on any `brick` part reports a
min-feature FAIL *by design*, and `kernel3d/brick.ts` passes an explicit
`minFeatureMm: 0.8` override that the Lab panel surfaces rather than hides
(design doc §7.4). The rib is additive and needs no numeric floor; what it needs
is **tangential width ≥ 2 × nozzle (0.8 mm)**, or the slicer absorbs it into the
perimeter and it does not exist in the printed part. Watertightness and Euler
consistency are **not** relaxed. Same posture as the W-series clip blade: the
floor is a default for pattern art, not a law about connectors.

The bore values below straddle the tangency 6.514 mm and LDraw's convention
6.4 mm (design doc Appendix B.1). The spread is 0.11 mm — smaller than the global
clearance the fit profile applies on top, and much smaller than the rib's effect —
which is exactly why the ladder sweeps the rib and holds the bore fixed.

## LG-F1 — Clutch coupon, anchor side (rib-thickness ladder)

- **Status**: planned (printing on hold; blocks M6)
- **Model**: `bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr` `--piece
  CouponAnchorPlate` — a 2×4 tile-style piece (`studs none`, three anti-stud
  tubes) at a fixed bore (6.514 mm authored, −0.1 mm/side global clearance
  applied) printed across a five-rung **rib-thickness** ladder, `ribMm` =
  **0 / 0.05 / 0.10 / 0.15 / 0.20 mm**, crossed with `engage` = **1.6 / 3.2 /
  8.0 mm**. Rung 0 is the no-rib control and doubles as the bore test — if it
  clutches, the §3.8 architecture is unnecessary and that is a real finding
  (bikar's `lego-coupons.test.ts` holds that rung to being *genuinely* ribless:
  fewer triangles than the ribbed solid, not a lobe of zero thickness). Render
  one rung:
  ```
  cd bikar && node packages/cli/dist/index.js render \
    patterns/Coupons/Lego-Clutch-Coupon.bkr --format stl \
    --piece CouponAnchorPlate --brick-fit ribMm=0.10 --param engage=3.2 \
    -o ../3d-models/build/stls/coupons/LG-F1-rib010-eng32.stl
  ```
  — **without `--check`** (sub-floor tube wall and rib, see the series note).
  The rib is **not** a `--param` and cannot be: a `param` is read by a `brick`
  statement and no brick statement reads a rib thickness. It is a `brickFit`
  offset, which is what `--brick-fit` reaches (bikar PR
  [#45](https://github.com/NaqshCoffee/bikar/pull/45)); an earlier version of
  this entry prescribed `--param rib_mm=…`, a knob that never existed. Cheapest
  decisive coupon in the series: it fixes the numbers every later LG coupon and
  every shipped brick inherits.
- **Print target**: TBD — record machine/material/nozzle/layer/XY-compensation
  **and filament spool + dryness** on first print. Bambu's own docs say fit moves
  with moisture ("dry filament results in a looser fit"), so a LEGO profile is
  valid for a spool, not for a printer, and this coupon is where that is either
  confirmed or dismissed. PLA and PETG both worth a pass; ABS is what real bricks
  are.
- **Mating part**: a **real LEGO plate** the user owns — not a printed one.
  Compatibility with our own output proves nothing.
- **What we want to learn**:
  - [ ] 1. Which `ribMm` clutches a real LEGO stud firmly without forcing — the
    number that becomes the LEGO profile's rib entry?
  - [ ] 2. **Does rung 0 clutch at all?** If a loose bore with no rib already
    holds, §3.8's whole architecture is over-engineering and the doc must say so.
  - [ ] 3. Does it *hold* — survive being picked up by the printed piece with a
    brick attached, and repeated seat/unseat without loosening? (Depth of that
    question is LG-D1's.)
  - [ ] 4. **`engage`: does 1.6 mm fail the way §3.6 predicts?** The prediction is
    specific — the bridged ceiling sags into the zone the host studs occupy. Look
    at the underside of the 1.6 rung before testing fit, and record whether the
    sag is what blocks it.
  - [ ] 5. **Re-pointed to `CAL-FEA-01` / MC-2.** Whether a sub-1.2 mm wall
    prints at all — and in which direction the realised thickness errs — is a
    property of the printer, and MC-2's seven-rung wall ladder answers it once
    for every design in this repo. Brick Architect's "walls came out too thick"
    is MC-2's Q2, not a LEGO question. What stays LG-F1's is narrower and still
    worth a caliper: does the tube wall at 0.857 mm on a **short, curved** tube
    behave like MC-2's flat rung of the same thickness, or does the curvature and
    the tube's stub height change it? Measure both and compare; a divergence is
    the finding, not the absolute number.
  - [ ] 6. Does the 0.8 mm-wide rib survive slicing, or does the perimeter path
    swallow it? Inspect the sliced preview *and* the printed part.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Settles**: `CAL-RIB-01` (clutch rib `ribMm`, design doc Appendix B.8) —
  design-specific and deliberately **not** on the machine card. The minimum
  printable wall (Q5) belongs to `CAL-FEA-01` / MC-2.
- **Feeds**: the rib and `wall` entries of the LEGO fit profile in `bikar`
  `kernel3d/fit-profile.ts`; the `engage` default in design doc §4 and §3.6; the
  §7.4 `minFeatureMm` override if Q5 disproves the thin wall; design doc
  Appendix B.8 — **the largest unverified bet in the document**; **M6's geometry
  constants — this coupon gates that phase.**

## LG-F2 — Clutch coupon, stud side (stud ⌀ ladder)

- **Status**: planned (printing on hold; blocks M6's `studs` interfaces)
- **Model**: `bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr` `--piece
  CouponStudPlate` — a 2×4 **three-plate brick** with a five-rung stud-⌀ ladder
  centred on 4.8 mm at ±0.15 mm (**4.65 / 4.73 / 4.80 / 4.88 / 4.95 mm**),
  tested against a real LEGO brick's **underside**. Render without `--check` as
  above; sweep `--brick-fit studDiaMm=` **−0.15 / −0.07 / 0 / +0.08 / +0.15**
  (the offsets are diametral deltas onto the 4.8 mm datum, so `0` *is* the
  moulded nominal and the shipped −0.2 sits one rung below the ladder).
  ```
  cd bikar && node packages/cli/dist/index.js render \
    patterns/Coupons/Lego-Clutch-Coupon.bkr --format stl \
    --piece CouponStudPlate --brick-fit studDiaMm=0 \
    -o ../3d-models/build/stls/coupons/LG-F2-stud480.stl
  ```
  **Three plates, not the one this entry first specified**, and the reason is a
  warning the engine emits rather than a preference: a plate is 3.2 mm tall, so
  it can engage at most 1.6 mm and keep any ceiling at all, and 1.6 mm is
  exactly the engagement V5b flags — the sag Q4 of LG-F1 is *about*. A 1-plate
  coupon would carry that confound into a measurement of stud ⌀. Body height is
  not what this ladder sweeps, so three plates costs a few grams and nothing
  else.
- **Print target**: TBD. **Print one full ladder at 0.4 mm nozzle and, if
  available, one at 0.2–0.3 mm** — that comparison is the entire point of Q1, and
  it has a published counterexample worth knowing before you run it: Brickset
  printed the same brick both ways and the **0.2 mm-nozzle part clutched
  *worse***. "Just use a finer nozzle" is not an established escape hatch.
- **Mating part**: a real LEGO brick (2×4), engaged from above.
- **What we want to learn**:
  - [ ] 1. **Is `studs full` viable at 0.4 mm at all?** Design doc §11 Q1: if a
    ⌀4.8 stud will not resolve cleanly on a 0.4 mm nozzle, `studs full` and
    `studs edge` ship disabled with a documented nozzle requirement and
    `studs none` carries the whole feature. This coupon decides it.
  - [ ] 2. Which stud ⌀ a real brick's anti-stud accepts → the `studDia` offset.
  - [ ] 3. Do printed studs survive repeated engagement, or do the layer lines
    shear off the stud tops?
  - [ ] 4. Is stud height 1.6 mm enough engagement when printed, or does the
    first-layer elephant's-foot eat it? Note Brickset's result runs the other
    way: the only clutch observed on their printed bricks was attributed by a
    commenter to elephant's foot. Record whether it helps or hurts here.
  - [ ] 5. **Measure every rung's realised stud ⌀ with calipers before testing
    fit**, and record authored-vs-realised. The grounding audit found **no public
    source that reports caliper measurements on a printed LEGO-compatible stud** —
    this table would be the first, and it is what turns §3.5's process-variance
    argument from literature into a local number.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: the `studDia` LEGO profile entry; **design doc §11 Q1 — whether the
  `studs full`/`studs edge` interfaces ship in M6 or at all**; the nozzle
  requirement in the Lab's print notes (P3).

## LG-S1 — Printed-onto-printed stack coupon (stud-⌀ offset ladder)

- **Status**: planned (printing on hold; blocks nothing, but the number it
  settles is currently a warning nobody can silence honestly)
- **Why this one is not LG-F1 or LG-F2 over again**: both of those mate a printed
  part to a **real LEGO** part, where exactly one side of the joint carries the
  printer's shrinkage and the fit profile's −0.2 mm diametral offset is applied
  once. This coupon mates **two printed parts**, so the offset lands on both
  sides and subtracts twice. On the shipped defaults that leaves total radial
  interference at **0.00 mm** — a stack that seats face-to-face with no clutch at
  all. bikar reports it as a warning on every `Brick-Stack` render
  (`brick-ports.ts`, PR [#36](https://github.com/NaqshCoffee/bikar/pull/36)); the
  warning is honest and the *ceiling* it is measured against is not yet.
  A textbook **K10** — a constant transferred across processes without stating
  the transfer condition — which is why it gets its own coupon rather than a
  footnote on LG-F2's.
- **Model**: `bikar/patterns/Assemblies/Brick-Stack.bkr` — two 3-plate 2×4 bricks
  joined `Base.stud_c0r1` → `Cap.anti_c0r1`, exported as two piece-local STLs:
  ```
  cd bikar && node packages/cli/dist/index.js render \
    patterns/Assemblies/Brick-Stack.bkr --format parts \
    -o ../3d-models/build/stls/coupons/LG-S1/
  ```
  Sweep the **stud-⌀ offset**, which is what the fit profile actually holds:
  rungs at `studDiaMm` = **−0.20 (shipped default, the no-clutch control) /
  −0.15 / −0.10 / −0.05 / 0.00 (moulded nominal, offset applied once)** —
  `--brick-fit studDiaMm=−0.10` and so on, the same flag LG-F1 and LG-F2 use
  (bikar PR [#45](https://github.com/NaqshCoffee/bikar/pull/45); before it, this
  ladder needed a script reaching past the CLI into the API). Note that in the
  catalogue's terms and the doc's, `studDiaMm` is an **offset onto 4.8 mm**,
  not a diameter.
- **Print target**: TBD — same recording discipline as LG-F1 (machine, material,
  nozzle, layer, XY compensation, spool + dryness). Both halves must come off the
  **same spool in the same session**: the whole question is what two parts with
  the *same* shrinkage do to each other, and mixing spools measures something
  else.
- **Mating part**: **none that is real LEGO.** That is the definition of this
  coupon. Print a real-LEGO control alongside — the winning LG-F2 rung on a real
  brick — so the printed-onto-printed grip can be read as a *ratio* against a
  joint whose behaviour is already characterised, not as a bare adjective.
- **What we want to learn**:
  - [ ] 1. **Where does entry actually stop?** `STUD_ENTRY_MAX_MM = 0.15 mm` is
    a guess at how much total radial interference two printed parts will swallow
    before the joint cannot be pushed together. Push each rung until it refuses
    and record which one does. This is the number `CAL-STK-01` exists for.
  - [ ] 2. **Does the shipped default really not clutch?** The arithmetic says
    0.00 mm interference. Print the −0.20 rung and try to lift the stack by the
    upper brick. If it holds anyway — surface friction, layer texture, the rib
    doing something the model does not account for — the warning is wrong and
    the doc must say so.
  - [ ] 3. Which rung is the one to ship as the printed-pair default, and is it
    the same number in PLA and PETG? A per-material entry is the likely answer
    and would mean the fit profile needs a printed-pair variant, not a constant.
  - [ ] 4. Does the joint survive repeated seat/unseat, or does the first
    insertion shave the interference away? (LG-D1's question, asked of a pair
    where *both* sides are printed and both can wear.)
  - [ ] 5. Does the anti-stud tube splay instead of gripping — i.e. is the
    receptacle's measured `clearRadiusMm` a rigid boundary or a compliant one?
    An edge cell is wall-bound and an interior cell tube-bound; compare the two
    on the same part before concluding anything about the number.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Settles**: `CAL-STK-01` (printed-onto-printed stud entry: max total radial
  interference).
- **Feeds**: `STUD_ENTRY_MAX_MM` in `bikar` `kernel3d/lego.ts` — the threshold
  the stud/anti-stud port contract errors on; whether the fit profile grows a
  printed-pair `studDiaMm` entry distinct from the printed-to-LEGO one; the
  warning text in `kernel3d/brick-ports.ts` and the K10 paragraph in bikar's
  `docs/language-reference.md`, both of which currently name this coupon as the
  thing that has not happened yet.

## LG-R1 — 1×N solid-pin coupon

- **Status**: planned (printing on hold; blocks 1×N footprint support)
- **Model**: `bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr` `--piece
  CouponPinStrip` — a 1×4 **three-plate** strip carrying the **three ⌀3.2 mm
  solid pins** design doc §3.3 predicts for a 1×4 footprint (LDraw
  `p/stud3.dat`), swept `--brick-fit pinDiaMm=` **−0.15 / −0.07 / 0 / +0.08 /
  +0.15** (realised **3.05 / 3.13 / 3.20 / 3.28 / 3.35 mm**). This is the coupon
  that settles the survey's "1×N exception" in plastic rather than on paper.
  ```
  cd bikar && node packages/cli/dist/index.js render \
    patterns/Coupons/Lego-Clutch-Coupon.bkr --format stl \
    --piece CouponPinStrip --brick-fit pinDiaMm=0 \
    -o ../3d-models/build/stls/coupons/LG-R1-pin320.stl
  ```
  Three plates for LG-F2's reason and one of its own: `engage` is the pin
  *length*, so a 1-plate strip would sweep pin ⌀ on 1.6 mm stubs and answer Q2's
  anisotropy question about a column half the height of the one that ships.
- **Print target**: TBD.
- **Mating part**: a real LEGO 1×4 plate/brick.
- **What we want to learn**:
  - [ ] 1. Does a printed ⌀3.2 solid pin clutch at all, or is a pin (contacting
    two studs) fundamentally weaker than a tube (contacting four)?
  - [ ] 2. **Design doc §11 Q2** — does FDM layer anisotropy shear the pin where
    a moulded one holds? Pins are small solid columns loaded laterally.
  - [ ] 3. Is 1×N worth supporting in M6, or should the first release require
    both footprint dimensions ≥ 2 and error on 1×N with a pointer?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: the `pinDia` LEGO profile entry; the anchor solver's 1×N branch in
  `bikar` `kernel3d/grid-gate.ts`; design doc §5.2 and §11 Q2.

## LG-D1 — Clutch durability (100 cycles)

- **Status**: planned (printing on hold; blocked on LG-F1 producing a passing
  rung)
- **Model**: two copies of the winning LG-F1 rung — same file, same profile, same
  spool — so one can be sacrificed and one kept as an unused reference.
- **Print target**: whatever LG-F1 settled on; record it and change nothing.
- **Mating part**: one **real LEGO plate**, the same physical plate for all 100
  cycles, so wear on the reference part is not confounded with wear on ours.
- **Why this coupon exists at all**: the grounding audit searched hard and found
  **zero public sources reporting a clutch durability cycle count for a printed
  LEGO-compatible part** — the question is simply unanswered in either direction,
  and it is the one that decides whether these are toys or display pieces. It is
  cheap to answer here.
- **What we want to learn**:
  - [ ] 1. Does clutch survive 100 seat/unseat cycles, or creep away? Judge at
    1 / 10 / 50 / 100 on a fixed scale (falls off under own weight / holds but
    slips / holds firm), recorded each time, not just at the end.
  - [ ] 2. Where does it fail — the rib flattening, the tube wall splaying, layer
    delamination at the tube root, or the mating LEGO part wearing?
  - [ ] 3. Does the *reference* (uncycled) copy still clutch the same after the
    same elapsed time? Separates mechanical wear from PLA ageing — this repo
    already records that aged PLA embrittles on flex (`w2-connector-design.md`).
  - [ ] 4. PETG vs PLA on the same rung, if both were printed: which retains grip?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: design doc Appendix B.8 (whether a 0.1 mm rib is a durable clutch or
  a one-shot one); the material recommendation in the Lab's print notes (P3); the
  answer to §11 Q6 — whether a geometry-only gate can be honest about clutch.

## LG-B1 — First patterned brick (8-fold, 4×4)

- **Status**: planned (printing on hold; blocked on LG-F1's clutch number)
- **Model**: `bikar/patterns/Lego/Star-Brick.bkr` (`brick StarBrick`) — an
  eight-fold piece at declared defaults (`inscribe star_relief`, `footprint
  auto` → 4×4, `studs none`, `anchors auto` → nine tubes, `relief depth` at the
  §4 default). The first object that is **both a real LEGO part and a real
  Islamic pattern**. Render with `--fit-profile` set from LG-F1.
- **Print target**: TBD.
- **What we want to learn**:
  - [ ] 1. Do relief and clutch coexist — does a piece thin enough to show the
    pattern still hold onto a baseplate?
  - [ ] 2. Is the relief legible at 8 mm pitch, or is a 4×4 (31.8 mm) piece too
    small to read an eight-fold star?
  - [ ] 3. **Design doc §11 Q4** — does the cavity ceiling bridge cleanly across
    a 4×4 (≈28 mm) span, or does it sag into the relief above it?
  - [ ] 4. Does the piece butt seamlessly against a neighbouring copy — the
    physical check on the grid-fit score reading 1.0.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: the `relief depth` and `engage` defaults in design doc §4; the P1
  compatibility matrix's first ✅ row; §11 Q4's bridging answer.

## LG-B2 — Off-grid anchor (5-fold rosette)

- **Status**: model authored (bikar `bf6c602`, 2026-08-02, riding the
  `footprint outline` mode that shipped in the same commit); printing on hold,
  blocked on LG-B1.
- **Model**: `bikar/patterns/Lego/Rosette-Brick.bkr` — a ten-fold rosette (the
  five-fold girih family) whose scalloped outline is genuinely incommensurable
  with the square lattice. At the default radius 20 it compiles to a 6×5 grid
  with **six tube anchors** in the eight fully-covered lattice cells — the
  earlier sketch here said "two tubes"; the build is the authority. **The
  load-bearing bet of the entire anchor-only approach** (design doc §1, §5.3,
  Appendix B.2): that a printed piece's outline need not obey the grid so long
  as its interface does.
- **Print target**: TBD.
- **What we want to learn**:
  - [ ] 1. Does rotation lock actually hold when the outline is incommensurable
    — or does the piece rock/twist on its anchors in a way a rectangular piece
    does not? (Appendix B.2 is reasoned, not measured.)
  - [ ] 2. Does a piece whose body only partly covers its footprint have enough
    material around each anchor, i.e. is §5.2's 0.4 mm body-clearance test
    generous enough?
  - [ ] 3. Does it *look* right sitting on a LEGO baseplate — the question no
    gate can answer, and the reason the whole feature exists.
  - [ ] 4. Grid-fit reads low for this piece by construction. Does the physical
    result vindicate shipping it anyway (validator V8 as WARN, not ERROR)?
  - [ ] 5. **How much clutch does giving up the tangent side wall cost?** The
    patent clamps a stud "between one secondary projection **and the inner face
    of an end or side wall**", and the contact census (design doc §3.3) says the
    wall supplies 50–67 % of contacts on footprints this size. A rosette outline
    has no continuous wall. Print a rectangular 2×4 control at the same profile
    and compare grip side by side — the number this coupon exists for is the
    *ratio*, not a pass/fail.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: design doc Appendix B.2 (the rotation-lock criterion) and V8's
  WARN-not-ERROR call in §6; the P1 compatibility matrix's 5-fold row.

## LG-P1 — Mural seam registration (two pieces, one motif)

- **Status**: model authored (bikar `73514f1`, 2026-08-02); printing on hold,
  blocked on LG-F1 producing a passing rung — a piece that does not seat has
  no seam to measure. Star-Mural's pieces would also share a seam but carry a
  whole star field; this is the cheapest two pieces that share one.
- **Model**: `bikar/patterns/Lego/Seam-Coupon.bkr` — a `mural` cut
  `pieces 2 x 1 of 2 x 2`: two 2×2-stud pieces, **two** straight relief bars
  crossing the single seam perpendicular to it, symmetric at ±5.5 mm about the
  panel mid-line. This entry originally prescribed *one* line, and authoring
  it proved one line self-defeating: the mural recentres art by its bbox, so a
  lone bar lands on the mid-line — exactly where a 2×2 piece keeps its only
  anti-stud tube candidate — and `solveAnchors` drops any anchor within reach
  of a pocket, leaving both pieces with zero clutch (V-M6). A coupon that
  rests unclutched cannot measure stud registration. Two offset bars keep the
  tube, and double the jog samples per seating. Still the smallest object that
  can answer **CAL-REG-01**: the mural machinery guarantees both sides of the
  seam share exact vertex coordinates (`bikar` `mural-split.test.ts` asserts
  it), but whether the *printed, seated* pieces keep those lines straight is
  decided by stud registration on a real plate, not by the graph.
- **Print target**: whatever LG-F1 settled on; render with that `--fit-profile`.
- **Mating part**: one real LEGO baseplate — the same plate class the set is
  sold against.
- **What we want to learn**:
  - [ ] 1. **CAL-REG-01** — how far does each relief bar jog laterally where it
    crosses the seam? The prediction is ≤ the 0.2 mm physical gap (design doc
    §3: the cut is nominal, the gap is physical, nothing re-registers art to
    gap); measure both jogs, don't eyeball them.
  - [ ] 2. Does the 0.2 mm gap read as a groove in the art, or does the eye
    continue the lines across it at arm's length (design doc §3's seam-visibility
    question, empirical by construction)?
  - [ ] 3. Do stud clearance and elephant's foot leave the two top edges level,
    or does a height step at the seam do more visual damage than the gap?
  - [ ] 4. Seat/unseat/reseat both pieces five times: is the jog repeatable
    (stud registration) or does it wander (clutch slop)?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `CAL-REG-01` (open, this is its coupon); design doc §3's
  registration-vs-gap distinction — a measured jog beyond 0.2 mm is the only
  thing that earns an art-side correction (decisions-log D-013's reversal
  condition); the gallery's "seam 0.2 mm" spec chip.

## LG-P2 — Clone-baseplate clutch differential

- **Status**: planned (printing on hold; blocked on LG-F1 producing a passing
  rung, and on buying the plates).
- **Model**: two copies of the winning LG-F1 rung — the same file and profile
  LG-D1 uses, so this coupon prices *plates*, not geometry.
- **Print target**: whatever LG-F1 settled on; record it and change nothing.
- **Mating parts**: one LEGO-brand baseplate and at least one clone plate of
  the kind actually stocked at Target/Amazon (Mega or generic). Record brand,
  SKU and purchase date per plate — "clone" is not one population.
- **What we want to learn**:
  - [ ] 1. **CAL-CLB-01** — does the LG-F1 rib that clutches a LEGO-brand plate
    also clutch a clone plate, on the same fixed scale LG-D1 uses (falls off /
    holds but slips / holds firm)?
  - [ ] 2. Pitch accumulation: seat two pieces eight studs apart on each plate —
    does the clone's pitch error, accumulated across the span, change how a
    multi-piece set seats (the research survey flags clone pitch deltas as
    hedged secondary data, not measurement)?
  - [ ] 3. Stud ⌀ delta: does the clone need a different `--brick-fit`
    `studDiaMm` compensation, i.e. is "baseplate-compatible" one profile or
    one per plate population?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `CAL-CLB-01` (open, this is its coupon); the design doc's K2
  discipline that compatibility claims say "LEGO-brand verified; clone
  unmeasured" until this coupon reports; whether the Lab's fit-profile page
  needs a per-plate-brand preset.

---

# Deliverables

The entries above are **coupons** — objects whose only purpose is to yield a
number. The four below are the **deliverables** the design docs actually
promise: the finished objects each rung of the C and W ladders exists to make
possible. They sit last because nothing else in this catalog depends on them,
and each stays `planned` until the coupons feeding it report.

They were absent from this file until 2026-08-03 even though four design docs
demanded them, which is what [`docs/backlog.md`](../../../docs/backlog.md) §3.5
was tracking. Every figure quoted below is from a render of the shipped model at
bikar `d9b3c84`, not an estimate.

## C1 — Nail-Tile deliverable (the girih tile you can hang)

- **Status**: planned. Not blocked on any coupon — it prints at the FDM floor
  with no fits, no clips and no mating part. Blocked only on a printer.
- **Model**: `patterns/Pieces/Nail-Tile.bkr` at declared defaults (`depth` 6,
  `shaft_d` 3.5, `sink_d` 7, `sink_depth` 2) — an {8/2} octagram inscribed in a
  100 mm square slab with a countersunk nail hole at the centroid.
  `bikar render patterns/Pieces/Nail-Tile.bkr --format stl --check -o NailTile.stl`
  → 528 triangles, **59.9 cm³** of solid, `watertight=true euler=0 degenerate=0
  minFeature=1.75mm — PASS`. Print flat, art side up, bore vertical.
- **Print target**: TBD — record machine/material/nozzle/layer on first print.
- **What we want to learn**:
  - [ ] 1. Does the countersink seat a real nail head flush, or does the
    ⌀7 × 2 mm seat need to grow once elephant's foot has had its say? The
    printed mouth is the dimension to caliper, not the modelled one.
  - [ ] 2. Does a 100 mm × 6 mm slab with a large void fraction stay flat on the
    bed, or does it cup at the corners? This is the same question **MC-5**
    answers for a solid plate — compare against MC-5's number rather than
    deriving a second one, and if they disagree the void fraction is why.
  - [ ] 3. Do the octagram's acute interior corners resolve at 0.4 mm, or does
    the slicer round them into blobs? `minFeature=1.75 mm` is the mesh's answer;
    the extruder's answer is what this measures.
  - [ ] 4. Hung on one nail, does the tile sit level and stay put, or does it
    rotate about the single fixing?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: [`docs/piece-composition-design.md`](../../../docs/piece-composition-design.md)'s
  countersink geometry; the gallery's first "functional piece" entry; Q2's
  answer feeds back into whether tile `depth` 6 is enough.

## C2 — Pinned-Tiles deliverable (do the authored fit windows survive plastic?)

- **Status**: planned. Print after **MC-1**: the whole point is the fit windows,
  and MC-1's ladder is what sets `holeCompMm` for the profile these render under.
  Printing before it measures the compiler's guess, not the design.
- **Model**: `patterns/Assemblies/Pinned-Tiles.bkr` at declared defaults
  (`pin_d` 3, `depth` 6) — two 60 mm slab tiles and two ⌀3 × 12 mm pins.
  `bikar render patterns/Assemblies/Pinned-Tiles.bkr --format parts --check -o parts/`
  → four gated parts: TileA and TileB at 532 triangles each
  (`euler=-2 minFeature=6mm — PASS`), PinA and PinB at 256 each
  (`euler=2 minFeature=3mm — PASS`). Add `--fit-profile pla_calibrated` once
  MC-1 has set one; the authored fits stay the contract either way. Pins print
  upright on the ⌀ face — a pin printed lying down is elliptical (the MC-1 rule,
  and it transfers because it is a property of the same extrusion, not of the
  coupon).
- **Print target**: TBD — record the `--fit-profile` used, or `authored` if none.
- **What we want to learn**:
  - [ ] 1. Does the press side (bore ⌀2.90 against a ⌀3.00 pin) actually press —
    seat once, stay seated, no glue — or does it split the 5 mm border?
  - [ ] 2. Does the sliding side (⌀3.15) slide *and* hold, or does it rattle?
    The two answers together are what the ±0.05 window claims; one alone is not.
  - [ ] 3. With both pins in, do the tiles meet flush, or does the 15 mm pin
    spacing plus bore tilt leave a visible step? Measure the step, don't eyeball it.
  - [ ] 4. Seat and unseat TileB five times: does the sliding fit stay a sliding
    fit, or does it wear open?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: [`docs/c2-assembly-design.md`](../../../docs/c2-assembly-design.md) §8's
  fit-window claim — Q1 and Q2 together are the only thing that earns it; the
  `press`/`sliding` offsets in bikar's fit table; whether `--fit-profile` needs a
  per-material variant beyond PLA and PETG.

## W1 — Nail-Wall 2×2 pilot (what a real tile actually costs)

- **Status**: planned. Print after **C1** — this is four of that tile, and a
  problem found on one is cheaper than a problem found on four.
- **Model**: `patterns/Walls/Nail-Wall.bkr` at declared defaults.
  `bikar render patterns/Walls/Nail-Wall.bkr --format stl --check -o NailTile.stl`
  emits the **module**, not the wall: 528 triangles, 59.9 cm³, `minFeature=1.75mm
  — PASS`, with the layout report on stderr reading `4 full, 0 fragment(s),
  0 dropped — offcut 0.0 cm², uncovered 4.8 cm²` for a 201.2 mm square boundary at
  `gap 1.2`. Print the module four times. Also render
  `--format svg -o NailWall.svg` and look at it before committing filament — the
  pattern-continuity check across the 1.2 mm gaps costs nothing.
- **Print target**: TBD — this coupon's *purpose* is to record it, so record
  everything: profile name, infill percentage and pattern, wall count, and
  wall-clock time per tile.
- **What we want to learn**:
  - [ ] 1. **Mass and time for one real tile.**
    [`docs/tile-wall-design.md`](../../../docs/tile-wall-design.md) §7.1 labels its
    whole production table *estimates* — "~40–60 g, ~2–4 h at 0.2 mm on a modern
    small printer" — and makes computing them for real a W3 deliverable. Weigh the
    tile and read the slicer's actual time. The mesh's 59.9 cm³ is **solid**
    volume; printed mass is whatever the infill leaves, which is exactly why the
    estimate needs a print and not arithmetic.
  - [ ] 2. Does the estimate hold, and in which direction? Every downstream figure
    in §7.1 — ~36 tiles / ~5 days / ~2 kg for a 0.6 × 0.6 m panel, ~200 tiles /
    ~4 weeks / ~10 kg for a 1.2 × 1.8 m wall — is this one number multiplied.
  - [ ] 3. Butted up on a flat surface, do four tiles read as one continuous
    pattern across the 1.2 mm gaps, or does the gap break the motif? This is the
    SVG's claim, tested in plastic.
  - [ ] 4. Does tile-to-tile dimensional variation accumulate across the 2×2, so
    that the outer corners no longer land on the 201.2 mm boundary?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: [`docs/tile-wall-design.md`](../../../docs/tile-wall-design.md) §7.1's
  estimate table — Q1 replaces every hedged figure in it with a measured one, and
  is the input W3's `layout report` production metrics need; the gallery's "what
  does a wall cost" note.

## W2 — Clip-Wall first full wall (does the joint scale?)

- **Status**: planned. Blocked on **W-F1** (blade clearance — a clip that does
  not engage has no joint to scale) and then **W-C1** (which jaw variant, and
  whether capture holds at MC-5's warp). Printing is on hold with the rest of
  the W series.
- **Model**: `patterns/Walls/Clip-Wall.bkr` at declared defaults (`depth` 10,
  `gap` 1.2). Two renders, because the tile and the clip are gated differently:
  `bikar render patterns/Walls/Clip-Wall.bkr --format stl --check -o ClipTile.stl`
  → 2,372 triangles, **98.2 cm³**, `watertight=true euler=2 degenerate=0
  minFeature=2.4mm — PASS`, with `connectors: 1 × CornerClip (StarClip, petg) —
  1 interior corner, 0 perimeter corners unclipped; screws: 4 × no8 keyhole` on
  the layout report. Then
  `bikar render patterns/Walls/Clip-Wall.bkr --format stl --piece StarClip -o StarClip.stl`
  → 718 triangles, 0.3 cm³, **no `--check`**: the bayonet blade is ~0.6 mm and
  deliberately sub-floor, so gating it would fail by design (the model's own
  header says so). Print four tiles and one clip; tiles in the wall's material,
  clip in PETG, per W-C1's cross-shrinkage rule.
- **Print target**: whatever W-F1 and W-C1 settled on; render with that
  `--fit-profile` and change nothing else.
- **Mating parts**: four #8 pan-head screws — one per tile. Not one: `mount
  keyhole` is declared on the *tile*, so each placement mints its own keyhole
  (this catalog entry is why
  [`docs/w2-connector-design.md`](../../../docs/w2-connector-design.md) §8's
  "hanging on one screw" was corrected on 2026-08-03; see its §11 Q6).
- **What we want to learn**:
  - [ ] 1. Does one interior CornerClip actually hold four 100 mm tiles in
    register, or does the outer perimeter — `0 perimeter corners unclipped` on
    the BOM only because this wall has no cropped edges — splay?
  - [ ] 2. Do the four keyholes line up with four screws set from a paper
    template, or does tile-to-tile variation exceed the keyhole slot? The slot
    length is the tolerance budget; measure what it actually absorbed.
  - [ ] 3. Front-face lippage: with the clip engaged from behind, do adjacent
    tile faces sit level in raking light, or does the joint pull one proud?
    W-C1 asks this of two tiles; this asks it of a closed 2×2 where four
    interfaces must agree at once.
  - [ ] 4. Hang it, then take it down and rehang it. Does the clip survive
    disassembly, and do the tiles return to the same register?
  - [ ] 5. Does the engaged joint carry any shear — i.e. could a wall-level
    mount replace four tile-level ones (**§11 Q6**)? This entry does not decide
    it, but it is the first object that can show whether the question is worth
    pursuing.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: [`docs/w2-connector-design.md`](../../../docs/w2-connector-design.md)
  §8's deliverable claim and §11 Q6 (Q5 is its only evidence); the connector BOM's
  all-four-full clip rule, which Q1 tests at its easiest case before W3 relaxes it
  to fragments; the gallery's clipped-wall entry.
