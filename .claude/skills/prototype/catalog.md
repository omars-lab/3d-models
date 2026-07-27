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
  1.5 / 2 / 3 (Lab → set knobs → "Write values into code" → Download `.bkr`;
  `strut_depth` at default 2.4), plated together in the slicer. Cheapest
  honest coupon — the struts meet the sphere at the same angles as a real
  print, which a flat test plate would not exercise.
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
