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
- **Model**: `bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr` — a 2×4
  tile-style piece (`studs none`, three anti-stud tubes) at a fixed bore
  (6.514 mm authored, −0.1 mm/side global clearance applied) printed across a
  five-rung **rib-thickness** ladder, `ribMm` = **0 / 0.05 / 0.10 / 0.15 /
  0.20 mm**, crossed with `engage` = **1.6 / 3.2 / 8.0 mm**. Rung 0 is the
  no-rib control and doubles as the bore test — if it clutches, the §3.8
  architecture is unnecessary and that is a real finding. Render at defaults:
  `cd bikar && node packages/cli/dist/index.js render
  patterns/Coupons/Lego-Clutch-Coupon.bkr --format stl -o
  ../3d-models/build/stls/coupons/LG-F1-ClutchCoupon.stl` — **without
  `--check`** (sub-floor tube wall and rib, see the series note); sweep
  `--param rib_mm=... --param engage_mm=...`. Cheapest decisive coupon in the
  series: it fixes the numbers every later LG coupon and every shipped brick
  inherits.
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
  - [ ] 5. Does the 0.857 mm tube wall actually print — **measure it with
    calipers** — validating the §7.4 exemption, or does it come out as two merged
    perimeters? Brick Architect reports printed walls coming out *too thick*, so
    measure rather than assume the error's direction.
  - [ ] 6. Does the 0.8 mm-wide rib survive slicing, or does the perimeter path
    swallow it? Inspect the sliced preview *and* the printed part.
- **What we learned**: — pending.
- **Iteration log**:
  | # | date | change | question | result | decision |
  |---|------|--------|----------|--------|----------|
- **Feeds**: the rib and `wall` entries of the LEGO fit profile in `bikar`
  `kernel3d/fit-profile.ts`; the `engage` default in design doc §4 and §3.6; the
  §7.4 `minFeatureMm` override if Q5 disproves the thin wall; design doc
  Appendix B.8 — **the largest unverified bet in the document**; **M6's geometry
  constants — this coupon gates that phase.**

## LG-F2 — Clutch coupon, stud side (stud ⌀ ladder)

- **Status**: planned (printing on hold; blocks M6's `studs` interfaces)
- **Model**: `bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr` `--piece
  CouponStudPlate` — a 2×4 plate with a five-rung stud-⌀ ladder centred on
  4.8 mm at ±0.15 mm (**4.65 / 4.73 / 4.80 / 4.88 / 4.95 mm**), tested against a
  real LEGO brick's **underside**. Render without `--check` as above; sweep
  `--param stud_d=...`.
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

## LG-R1 — 1×N solid-pin coupon

- **Status**: planned (printing on hold; blocks 1×N footprint support)
- **Model**: `bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr` `--piece
  CouponPinStrip` — a 1×4 tile-style piece carrying the **three ⌀3.2 mm solid
  pins** design doc §3.3 predicts for a 1×4 footprint (LDraw `p/stud3.dat`),
  swept ±0.15 mm. This is the coupon that settles the survey's "1×N exception"
  in plastic rather than on paper.
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
- **Model**: `bikar/patterns/Bricks/Star-Brick.bkr` — a 4×4 eight-fold piece at
  declared defaults (`studs none`, `anchors auto` → nine tubes, relief at the
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

- **Status**: planned (printing on hold; blocked on LG-B1)
- **Model**: `bikar/patterns/Bricks/Rosette-Brick.bkr` — a five-fold rosette
  piece whose outline is genuinely incommensurable with the square lattice,
  anchored by two tubes. **The load-bearing bet of the entire anchor-only
  approach** (design doc §1, §5.3, Appendix B.2): that a printed piece's outline
  need not obey the grid so long as its interface does.
- **Print target**: TBD.
- **What we want to learn**:
  - [ ] 1. Does rotation lock actually hold when the outline is incommensurable
    — or does the piece rock/twist on two anchors in a way a rectangular piece
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
