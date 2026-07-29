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
- **Model**: same StarOrb.stl, cut at the equator **in the slicer** (no
  engine work) — both halves printed flat-face-down, supports off or minimal.
- **Print target**: TBD (same machine as P2 for a fair comparison).
- **What we want to learn**:
  - [ ] 1. Does flat-down/no-support halves beat the whole-sphere print on
    surface quality enough to justify engine work?
  - [ ] 2. Seam: how visible is the glued equator, and does the lattice give
    enough glue area?
  - [ ] 3. Alignment: how hard is registering two lattice halves by hand —
    would an engine split need registration pins/keys to be usable?
  - [ ] 4. Where should the cut land — through struts or through voids —
    for the least-visible seam? (Constrains the engine design if we build it.)
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

---

# Tile-wall connector ladder (W-series)

The W-series validates the **modular tile-wall** work (design docs
`docs/w1-tile-wall-design.md`, `docs/w2-connector-design.md`), not the orbs.
These coupons decide the connector grammar — clipseat fit and the printed
CornerClip — in plastic before any full wall is committed. Same learning-ladder
rule: the fit coupon (W-F1) settles the seat clearance the clip coupon (W-C1)
then builds on. Printing is **on hold** (design doc §8), so both land `planned`.

Sub-floor note for this whole series: a printed `clip`'s bayonet blade is
~0.6 mm, below the 1.2 mm FDM mesh-gate floor — so `--check` on a **clip part**
reports FAIL *by design*, and that thin flexing blade is exactly what these
coupons validate in plastic (design doc §10 Q1). The **tiles** pass the gate
cleanly (the clipseat rebate is a supported step the gate excludes, not a
free-standing strut). Only the clip is exempt, and only where noted.

## W-F1 — Clipseat fit coupon (seat clearance ladder)

- **Status**: planned (printing on hold, design doc §8)
- **Model**: `bikar/patterns/Coupons/Fit-Coupon.bkr` — small clipseat dummy
  tiles printed across a gap ladder to find the seat clearance that seats
  firmly without forcing. Render at defaults:
  `cd bikar && node packages/cli/dist/index.js render
  patterns/Coupons/Fit-Coupon.bkr --format stl --check -o
  ../3d-models/build/stls/coupons/W-F1-FitCoupon.stl` — the dummy tiles pass
  the mesh gate; sweep the `gap` param (`--param gap=...`) to print the ladder.
  Cheapest connector coupon — it fixes the seat clearance number that every
  later clip coupon and the full Clip-Wall inherit via `--fit-profile`.
- **Print target**: TBD — record machine/material/nozzle/layer on first print.
  PETG is the intended clip material; the seat is on the tile, so print the
  coupon tiles in the wall's tile material (PLA or PETG) to match shrinkage.
- **What we want to learn**:
  - [ ] 1. Which `gap` value seats the clip firmly without forcing on a
    0.4 mm nozzle — i.e. the number that becomes `profile.gapMm` /
    `--fit-profile petg_calibrated`?
  - [ ] 2. Measured tile warp across the coupon → `profile.warpMm` (does a
    flat clipseat tile stay flat enough for a corner jaw to bear evenly?).
  - [ ] 3. Does the seat clearance need to differ by tile material (PLA vs
    PETG shrinkage), or is one `gap` good for both?
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: `--fit-profile` seat-clearance profile consumed by
  `patterns/Coupons/Clip-Coupon.bkr` and `patterns/Walls/Clip-Wall.bkr`;
  clipseat constants in `bikar` `kernel3d/clipseat.ts` if the seat floor moves.

## W-C1 — CornerClip coupon (rebate-vs-proud joint decision)

- **Status**: planned (printing on hold, design doc §8; blocked on W-F1's
  seat-clearance number)
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
- **Feeds**: the clipseat grammar default (rebate vs proud) in
  `docs/w2-connector-design.md` §10 and every `clipseat` in
  `patterns/Walls/*.bkr`; the mesh-gate sub-floor exemption for bayonet clips
  (`bikar` `kernel3d/corner-clip.ts` minFeature) if Q3 disproves durability;
  `patterns/Walls/Clip-Wall.bkr` as the first full wall once the joint is
  proven.
