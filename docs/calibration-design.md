# Machine Card — coupon design doc

Status: **AUTHORED, UNPRINTED.** The `.bkr` exists, every rung renders, and every
rung's mesh has been checked. **No rung has been printed and no calibration bet is
settled.** Rendering a coupon proves the geometry; only a caliper proves the number
(`.claude/skills/calibrate/SKILL.md`, Rules).

Card: [`bikar/patterns/Coupons/Machine-Card.bkr`](../../bikar/patterns/Coupons/Machine-Card.bkr)
Protocol: [`.claude/skills/calibrate/protocol.md`](../.claude/skills/calibrate/protocol.md)
Bet registry: `bikar/packages/core/src/kernel3d/calibration.ts` (generated view in
`.claude/skills/calibrate/bets.md`)

---

## 1. What the card is for

Seven design docs have been through `ground-design-doc`, and the residue is the same
verdict every time: *no literature can decide this — measure it.* Four separate
coupons (W-F1, W-C1, LG-F1, P1) each independently planned to measure some of warp,
wall floor, and bore fit. But warp is not a property of a clip, a wall floor is not a
property of a brick, and bore shrinkage is not a property of an orb. They are
properties of a **(printer, material, nozzle, slicer profile)** tuple.

The machine card measures that tuple once. Every design coupon afterwards tests only
what is genuinely design-specific — the clutch rib, the bayonet detent, the clipseat
choice — and inherits the substrate numbers rather than re-measuring them badly.

Six coupons, seven bets:

| Coupon | Geometry | Rungs | Settles |
|---|---|---|---|
| **MC-1** bore & fit plate | 2 × `extrude` + 7 × `rod` | bore ⌀ 3/4/5/6/8/10; fit −0.10/0/+0.05/+0.15/+0.35 | `CAL-HOL-01`, `CAL-FIT-01` |
| **MC-2** wall ladder | 7 × `tube` | wall 0.4/0.6/0.8/1.0/1.2/1.6/2.0 mm | `CAL-FEA-01` |
| **MC-3** bridge plate | `extrude` + 8 blind bores | span ⌀ 4/6/8/10/12/16/20/25 mm | `CAL-BRG-01` |
| **MC-4** overhang fan | 1 × `revolve` | 20/30/40/45/50/60° from vertical | `CAL-OVH-01` |
| **MC-5** warp plate | thin `extrude`, 120 × 80 | one part, four corners | `CAL-WRP-01` |
| **MC-6** bed-contact towers | 4 × `rod` | ⌀ 3/5/8/12 × 40 mm | `CAL-BED-01` |

`CAL-RIB-01` (clutch rib) and `CAL-DET-01` (detent band) stay off the card: they are
design-specific and belong to LG-F1 and W-C1. `CAL-STR-01` (Z-layer strength ratio)
has no coupon at all — it needs a load rig, and it is registered OPEN so the gap stays
visible rather than invisible.

## 2. Authored blind — read this before trusting a rung

There is no machine. Nothing on this card has been printed, by anyone, ever.

Every rung *range* below is a **bracket around an unknown, not a prediction**. The
ladders were cut around the constants the repo currently ships — 1.2 mm feature floor,
10 mm bridge, 25 mm² bed contact, 0.20/0.25 mm hole compensation — and those constants
are themselves the placeholders being tested. Cutting a ladder around a placeholder is
circular reasoning if you read the ladder as a prediction, and perfectly sound if you
read it as a bracket: the point is that the answer be *inside* the range, not near the
middle of it.

So the first print has three possible outcomes, and only one of them is boring:

1. The ladder brackets, and a rung in the middle is the answer. Log it, propagate it.
2. **Every rung passes.** The ladder is centred too conservatively. That is a result:
   the machine is better than the shipped constant, and the ladder gets re-cut lower.
3. **Every rung fails.** Same thing in the other direction.

Cases 2 and 3 are not defects in the card and must not be logged as "the coupon didn't
work". They are the coupon working — it told you which way to move. `protocol.md`
states this as a rule; this doc states it because the geometry is where the mistake
would be blamed.

One partial exception, flagged so the rest of the blindness stays credible: **MC-3's
top rungs are not blind.** `w2-connector-design.md` §B.3 already surveyed the bridging
literature and found the shipped 10 mm rule to be conservative by a factor of two or
more, so MC-3's ladder is cut where that survey says the wall is, not where the
constant sits (§5.3). It is still unmeasured — a survey is not a caliper — but it is
argued rather than guessed.

## 3. Two consequences, stated rather than hidden

### 3.1 MC-2 deliberately fails `--check`

Rungs 0.4, 0.6, 0.8 and 1.0 mm sit below `DEFAULT_MIN_FEATURE_MM = 1.2`
(`bikar/packages/core/src/kernel3d/mesh-gate.ts`), so `meshGate` reports **FAIL** on
all four — and refuses to write the STL. That is correct behaviour and it is the whole
point: the gate's floor is the quantity MC-2 exists to measure, so a wall ladder that
cleared the gate would be a ladder that could not see below it.

Those four rungs are rendered **without** `--check`. Their meshes are still watertight
(`euler = 0`, torus topology, verified — §7), which is the property that actually
matters for a file that is about to be sliced.

No `--min-feature` override flag is added, and adding one is explicitly out of scope.
A flag that silences the gate for a coupon is a flag that silences it for a shipped
part six months later. The precedent already exists in the repo and is the same shape:
the **W-series sub-floor rule** in `.claude/skills/prototype/catalog.md`, where
W-C1's ~0.6 mm bayonet blade renders bare and the catalog says so in the entry.

### 3.2 Rung identity: engraved on the plates, positional within them

bikar now emits engraved text on flat plate tops — the `text` statement, wired to the
mesh gate with a gap-and-counter validator ([`text-emit-design.md`](text-emit-design.md),
shipped T2). So the four flat-plate coupons carry the printed label the wild uses
(BOSL2's tolerance ladders; Bambu's own fit test): `MC1BoreSweep` says `MC-1 BORE`,
`MC1FitLadder` `MC-1 FIT`, `MC3BridgePlate` `MC-3`, `MC5WarpPlate` `MC-5`. The card no
longer has to be kept in order by hand for those four.

The capability is **extrude-only**, and that is the boundary of what T3 labelled. A rod
top, a tube rim and a revolved cone flank have no flat face to engrave, so the 14 rods
(MC-1 pins and gauges, MC-6 towers), the 7 MC-2 tubes and the MC-4 fan cannot carry a
label — and are not made to. They keep the two mitigations that always applied, neither
as good as a printed number but both real:

- **One piece per rung, rendered via `--piece`.** Identity lives in the STL filename
  (`MC2Wall08.stl`), which survives into the slicer's plate and into the sliced file
  name. It does not survive onto the part.
- **Monotone size ordering inside every ladder.** MC-1's bores ascend left to right;
  MC-2's walls ascend; MC-3's spans ascend; MC-4's angles increase bottom to top;
  MC-6's towers ascend. The ordering is self-evident in the hand even when the parts
  have been knocked off the plate — you can re-sort MC-2 by eye and be right.

For the round coupons the operational consequence still belongs in the print
instructions, not in the geometry: **bag each rung as it comes off the plate.** An
unbagged, unsorted MC-2 tube is an unidentifiable tube, and a mis-assigned rung is worse
than a missing one because it produces a confident wrong number.

Within a labelled plate the rungs themselves stay positional — the bores are one
ascending size ladder — because a per-bore label would collide with the bores it names.
And two plate labels are placed against, not on, their measurand: `MC-5` is 0.4 mm deep
(not the 0.6 default) and centred on the bottom edge, far from the four corners and the
fiducial whose warp it reads, so the recess perturbs opposite corners equally; `MC-3`'s
label sits at the top edge, clear of the bore line, so it never thins a bridging ceiling
(the machine card's `.bkr` states both rationales at the label sites). This is §7 Q5 —
"whether text belongs on the coupon or beside it" — answered per coupon rather than in
general.

MC-4 escapes the no-label limit a different way, and it is why the fan has risers: see
§5.4.

## 4. What the DSL could and could not do

The card is authored entirely in the shipped `.bkr` grammar — no engine work. Four
constraints shaped the geometry, and they are recorded here because the next coupon
author will hit all four.

**No rectangle primitive.** A `w × h` plate is two guide circles of radius
`(h/2)·√2`, each quartered at `offset 45` and inset `h/2` from one end; four of the
eight division points land exactly on the corners. This is Fit-Coupon's idiom, reused
verbatim for MC-1 (two plates), MC-3 and MC-5.

**`polygon` vertices must be division points.** `evalPolygon` resolves each vertex
through `env.getPoints(...)` and has no midpoint branch, so `C.mpt` — which resolves
perfectly well in `connect`, `line` and `intersect` — is rejected inside a `polygon`
with *"Circle C has not been divided"*. That asymmetry is what forced MC-4's idiom:

```
circle O04 center(0,9) radius 13.76528     # a profile vertex at (r=13.76528, z=9)
divide O04 into 1
```

A circle centred **on the revolution axis** at height `z` with radius `r`, divided into
one, puts its single division point at exactly `(r, z)`. It reads better than the
workaround it is: for a revolve profile, each guide circle *is* the circle of
revolution at that height, so MC-4's vertex table can be read straight off the
blueprint. (The asymmetry is still worth filing against the evaluator; it is not worked
around here beyond this idiom.)

**`center()` takes a bare `$param` but not an expression** (`center($w - 10, 0)` is a
parse error at the `-`; `radius $w - 5` is fine). The rectangle idiom needs
`center(w/2 − h/2, 0)`, which is exactly the form `center()` refuses — so every plate
outline is literal, and the params on this card drive thicknesses and bore diameters
only, never footprints. Re-sizing a plate means editing four numbers, not one.

**No polygon offset.** MC-4 wants a constant-thickness shell, which needs a normal
offset. bikar has none, so the fan's inner wall is the outer wall shifted 4 mm
*horizontally*. See §5.4 for what that costs.

**`line` is a reserved word.** MC-1's line-to-line rung is named `zero`, not `line`.

## 5. Coupon by coupon

### 5.1 MC-1 — bore & fit plate (`CAL-HOL-01`, `CAL-FIT-01`)

Two plates, because there are two questions, and one plate answering both would let
them contaminate each other.

**`MC1BoreSweep`** — 90 × 24 × 6 mm, six through bores at nominal ⌀ 3/4/5/6/8/10,
ascending left to right on 14 mm centres. It asks: *how far does a printed bore drift
from its commanded diameter, and does the drift depend on the diameter?* A single
scalar `holeCompMm` (0.20 PLA / 0.25 PETG in `PRINTER_PROFILES`) assumes the answer to
the second half is "no". That assumption has never been checked, and six bores across a
3×range is the cheapest way to check it. Fit-Coupon's single ⌀3 ladder structurally
cannot see it — which is why this card **extends** `Fit-Coupon.bkr` rather than
replacing it, and its ⌀3 ladder is correct as far as it goes.

> **Corrected 2026-08-02.** This paragraph used to add "that file stays exactly as
> it is; it is still catalog entry W-F1's coupon." Neither half survived. The file
> was shipping a `+0.10 / +0.20 / +0.30` ladder against a `FIT_GAP_MM` of
> `−0.10 / +0.05 / +0.15 / +0.35` — drifted from the constant it calibrates, which
> is the exact failure the `MC1Fit` assertion below exists to prevent, so
> `Fit-Coupon.bkr` was re-cut to the shipped values and given the same four
> `connect`s. And W-F1 is now `Clipseat-Fit-Coupon.bkr`, a different joint; see
> `docs/decisions-log.md` **D-008**. The drift is why the assertion is now written
> once per fit class in both files rather than once per file: a rung with no
> `connect` has nothing holding it to the constant.

**`MC1FitLadder`** — 70 × 20 × 6 mm, five bores at `ref_d` (default 6 mm) offset by the
shipped ladder verbatim: press −0.10, line-to-line 0, snug +0.05, sliding +0.15,
free +0.35, taken from `FIT_GAP_MM` in `kernel3d/fit-profile.ts`. It asks the other
question: *at one diameter, does each named clearance class behave like its name in
plastic?* Judgement is by hand, not by caliper (`protocol.md` §"Per-coupon judgement"),
and the hand that made it is recorded, because it is a human calibration.

**`MC1Pin03…MC1Pin10`** — six gauge rods at the sweep's nominal diameters, 15 mm tall.
They exist so the two error terms can be separated: a printed **pin** carries the
machine's XY dimensional error alone; a printed **bore** carries XY error *plus* hole
shrinkage. Only the difference is `holeCompMm`. Caliper both. `MC1FitGauge` is the
ladder's mating pin at `$ref_d`; at the default `ref_d = 6` it is geometrically
identical to `MC1Pin06`, so print one of the two.

`MC1FitGaugePress`, `MC1FitGaugeSliding` and `MC1FitGaugeFree` are the same rod at
the same diameter, declaring a different `fit` class each. They are one physical
part — print `MC1FitGauge` once and try it in all five bores. They exist as four
pieces because a `connect` places a piece, and one piece cannot be placed in four
bores at once; four pieces is what buys the four assertions below.

**The ladder asserts itself against the constant.** The `MC1Fit` assembly connects
`MC1FitGauge.grip` (declared `fit snug`) to `MC1FitLadder.snug`, which runs the shipped
fit-window check. If `FIT_GAP_MM['snug']` is ever edited without re-cutting this
ladder, the file stops evaluating. Verified by mutation: changing the snug rung to
+0.30 produces

```
assembly MC1Fit: connect MC1FitGauge.grip to MC1FitLadder.snug — pin ⌀6.00 with snug
fit needs socket ⌀6.05 ± 0.05, but 'MC1FitLadder.snug' is ⌀6.30 (gap +0.30 is free
territory)
```

A calibration coupon that has silently drifted from the constant it calibrates is worse
than no coupon, because it produces a number that looks earned and is measuring
something else.

### 5.2 MC-2 — wall ladder (`CAL-FEA-01`)

Seven tubes, inner ⌀ 12 mm and 15 mm tall throughout, outer ⌀ stepped so the wall is
0.4 / 0.6 / 0.8 / 1.0 / 1.2 / 1.6 / 2.0 mm. Wall = (outer − inner)/2, and that is also
exactly the number the CLI reports as the declared min feature — so the figure in the
piece name is the figure the gate prints back, with no arithmetic in between.

**A tube, not a flat fin.** A closed loop is what a slicer's perimeter generator
actually has to solve: it is where a wall thinner than one extrusion width either gets
Arachne'd into a single variable-width bead or gets dropped silently. A flat fin also
needs a brim to stand up, and a brim changes the first few layers of the thing being
measured.

1.2 mm — the shipped floor, "three perimeters at a 0.4 mm nozzle" from general practice
— is the fifth rung, deliberately not the first or last. Four rungs below it and two
above bracket it on both sides.

### 5.3 MC-3 — bridge plate (`CAL-BRG-01`)

160 × 34 × 6 mm, eight **blind** bores at ⌀ 4/6/8/10/12/16/20/25 that open on the
*bottom* face and stop 2 mm short of the top. The remaining 2 mm ceiling must bridge the
bore diameter, so **span is the diameter**.

**Why the ladder runs to ⌀25 and not to ⌀12.** The obvious ladder brackets the shipped
10 mm rule tightly. That ladder would almost certainly come back all-clean, because
`w2-connector-design.md` §B.3 has *already* collected the counter-evidence and states
the 10 mm rule is "deliberately conservative, not a capability claim": Multiboard's
official snaps require printers to bridge up to 30 mm, community guidance puts clean
unsupported bridges at 20–25 mm on well-tuned machines, and UltiMaker documents 25 mm
in Tough PLA. A ladder that cannot fail costs a whole print to learn "higher than 12".
So the top rungs are placed where the literature says the wall actually is, and the
10 mm rule sits fourth from the bottom — bracketed on both sides, which is the point.
This is the one rung range on the card that is *not* purely blind: §B.3's survey
constrains it even though no machine here has been measured.

**Orientation is the measurement.** Printed as authored: plate flat, +z up, bore mouths
on the bed. Flipped, every bore becomes an ordinary blind pocket opening upward with
nothing to bridge, and the coupon answers a question nobody asked. This is why
`calibrate`'s coupon-design step requires the orientation to be stated: a bridge number
without an orientation is not a number.

**Why round bores rather than rectangular slots.** A circular bore presents the slicer
with a bridge of continuously varying length, from the full diameter at the centre down
to nothing at the tangents. So the failure appears as an *arc* where sag begins rather
than a single pass/fail per rung, and one bore yields a reading finer than its own
nominal span: read the chord at which sag starts. The protocol asks for the first rung
that **sags**, not the first that fails — the usable limit is the last clean one.

**What the gate cannot see here.** `--check` reports `minFeature = 4.5 mm`, which is
the margin beside the ⌀25 bore. The 2 mm bridged ceiling is not part of the declared
min-feature computation at all. That is not a bug in this coupon, but it does mean the
mesh gate is silent about the one dimension MC-3 is built around — do not read its PASS
as an opinion on the ceiling.

At 160 mm this is the longest part on the card and, at 27.5 cm³, the heaviest. Both are
consequences of an honest span ladder: a ⌀25 bore needs a plate to sit in.

### 5.4 MC-4 — overhang fan (`CAL-OVH-01`)

One revolved shell that flares outward as it rises, so its **underside** is the test
surface. Six conical bands, 4 mm of rise each, at 20 / 30 / 40 / 45 / 50 / 60° from
vertical, separated by 1 mm vertical risers. Overall: 29 mm tall, top ⌀ 65.6 mm, bed
contact a 6–10 mm annulus (201 mm²).

**Why a revolve and not a cone.** A true cone touches the revolution axis, and C1
rejects axis-touching profiles — `solidifyRevolvedPiece` throws *"revolve profile
touches or crosses the revolution axis … C1 revolves ring profiles only (all r > 0)"*.
A truncated ring whose outer edge is a staircase of slopes is legal. It is also the
better coupon: a ring presents every angle at every compass bearing simultaneously, so
a machine whose part cooling is directional shows that as azimuthal variation within a
single part, instead of hiding it in a fan that faces one way.

**Why the risers.** A 45° → 50° slope change is nearly invisible on a printed surface.
A 1 mm vertical band is unmistakable. The risers are what make the rungs countable from
the bottom up, and they are this coupon's substitute for the label §3.2 cannot print.
They are vertical, so they contribute no overhang of their own.

**The cost of having no polygon offset.** The inner wall is the outer wall shifted 4 mm
horizontally, so the *perpendicular* wall thickness varies with band angle:

| Band | 20° | 30° | 40° | 45° | 50° | 60° |
|---|---|---|---|---|---|---|
| Perpendicular wall (mm) | 3.76 | 3.46 | 3.06 | 2.83 | 2.57 | 2.00 |

The thinnest rung is 2.00 mm, comfortably above the 1.2 mm floor, so wall thickness
never confounds the overhang reading — but the variation is real, it correlates with
the variable under test, and it is stated rather than hidden. If a future version of
bikar gains a polygon offset, this is the coupon to re-cut first.

**What the gate cannot see here either.** For a `revolve`, the CLI reports the profile
bounding-box extents as the declared min feature — 26.8 mm for this fan. It says
nothing whatever about the 2.00 mm wall. PASS on MC-4 means "watertight, non-degenerate
mesh", not "printable wall".

### 5.5 MC-5 — warp plate (`CAL-WRP-01`)

120 × 80 × 1.6 mm — eight layers at 0.2 mm. Thin and wide is the entire design: warp is
a differential-cooling moment, so it grows with footprint and falls off with section
stiffness. Large enough to lift on a machine that warps at all; small enough to fit any
bed this card is likely to meet, which matters because the card is authored without
knowing the machine.

`PrinterProfile.warpMm` is currently `undefined` and every shipped profile omits it —
deliberately, per `PROFILE_WARP_MM_CAL`, because absence is meaningful and consumers
must fall back explicitly to `capture = max(1.0, 2 × warp)`. MC-5 is what replaces the
absence with a number.

**No features.** No ribs, no infill pattern, no lightening holes. Anything that locally
changes stiffness turns the measurement into a property of that feature.

**One exception: the ⌀3 fiducial.** Near one corner, so that "corner A" means the same
corner on the next print and on the next machine — A is the corner nearest the
fiducial, then B, C, D clockwise viewed from above. Four readings, all four recorded:
the *pattern* across the corners is what distinguishes warp from a bed-levelling
artifact, which is why the protocol forbids reporting only the worst one. A ⌀3 hole
6.5 mm from the plate edge in a 9,600 mm² plate is a stiffness perturbation small
enough to accept for a permanent orientation reference.

### 5.6 MC-6 — bed-contact towers (`CAL-BED-01`)

Four rods, ⌀ 3/5/8/12, all 40 mm tall. First-layer contact areas bracket
`MIN_BED_CONTACT_MM2 = 25` from both sides — and the print gate confirms the bracket
lands where intended:

| Tower | Contact (mm²) | `--check print` |
|---|---|---|
| `MC6Tower03` | 7.1 | warn F7 |
| `MC6Tower05` | 19.6 | warn F7 |
| `MC6Tower08` | 50.2 | clean |
| `MC6Tower12` | 112.9 | clean |

Two below the threshold, two above, with the transition between rungs 2 and 3. The
`MIN_BED_CONTACT_RATIO = 0.01` companion trigger is untestable on a straight rod (a
rod's first layer *is* its widest layer, so the ratio is 100% for all four) — it rides
the same bet and is settled by inference from the absolute figure, not measured
directly. That is a weakness in this coupon and is recorded as one in §8.

**Constant height is what makes this a contact-area ladder** rather than an
aspect-ratio ladder. The aspect ratio does fall out of it anyway (13.3:1 down to
3.3:1), and the two failure modes are physically different: a tower that never sticks
is an adhesion result; a tower that sticks and then snaps off mid-print is a
stiffness/vibration result. Record which happened, and the height if it was observed.

**Bare plate — no brim, no raft.** A brim is precisely the mitigation F7 exists to
recommend, so printing with one measures the brim instead of the threshold.

## 6. Render commands

`make coupons` in this repo runs all of it and then checks the result against §7's
table; the block below is what it runs, and is worth reading before trusting either.
Everything is one command per rung — that is what puts the rung's identity in the
filename. `bikar` below is `packages/cli/dist/index.js` after a build, or
`npx tsx packages/cli/src/index.ts` from source.

```sh
cd bikar
CARD=patterns/Coupons/Machine-Card.bkr
OUT=../3d-models/build/stls/coupons/machine-card

# MC-1 — bore & fit plate. MC1FitGaugePress/Sliding/Free are the same rod as
# MC1FitGauge and are deliberately absent: they exist to carry assertions, not meshes.
for P in MC1BoreSweep MC1FitLadder MC1FitGauge \
         MC1Pin03 MC1Pin04 MC1Pin05 MC1Pin06 MC1Pin08 MC1Pin10; do
  bikar render $CARD --format stl --check --piece $P -o $OUT/$P.stl
done

# MC-2 — wall ladder. The first four rungs are sub-floor: NO --check.
for P in MC2Wall04 MC2Wall06 MC2Wall08 MC2Wall10; do
  bikar render $CARD --format stl --piece $P -o $OUT/$P.stl
done
for P in MC2Wall12 MC2Wall16 MC2Wall20; do
  bikar render $CARD --format stl --check --piece $P -o $OUT/$P.stl
done

# MC-3 / MC-4 / MC-5
bikar render $CARD --format stl --check --piece MC3BridgePlate -o $OUT/MC3BridgePlate.stl
bikar render $CARD --format stl --check --piece MC4OverhangFan -o $OUT/MC4OverhangFan.stl
bikar render $CARD --format stl --check --piece MC5WarpPlate   -o $OUT/MC5WarpPlate.stl

# MC-6 — bed contact. 'print' also exercises F7, which is the bet under test.
for P in MC6Tower03 MC6Tower05 MC6Tower08 MC6Tower12; do
  bikar render $CARD --format stl --check print --piece $P -o $OUT/$P.stl
done
```

**Always pass `--piece`.** Without it the CLI renders the file's last solid, which on
this card is the `MC1Fit` assembly combined into one mesh — a plate and a loose pin in
a single STL. That is a valid render and a useless coupon.

Re-cutting a ladder needs no edit: `--param ref_d=8` moves MC-1's fit ladder to ⌀8,
`--param bridge_z=9 --param ceiling_t=3` thickens MC-3's ceiling, `--param tower_h=60`
lengthens MC-6. Footprints are literal and are not parameterised (§4).

## 7. Verification record

Rendered from source at authoring time (`npx tsx packages/cli/src/index.ts`, Node
22.22.3). **Watertightness is the real regression test here** — a bad coupon fails
*silently* in the mesh, and a coupon that quietly self-intersects produces a print that
looks fine and measures nothing.

Expected Euler characteristics, so that a future change to the card can be checked
rather than eyeballed: an extruded plate with *n* through bores is `2 − 2n`; blind
pockets do not change genus, so MC-3 is `2`; a tube or a revolved ring is a torus, `0`;
a rod is `2`; MC-5's single fiducial through-hole makes it `0`.

| Piece | euler | watertight | degenerate | minFeature (mm) | `--check` | tris | vol (cm³) |
|---|---|---|---|---|---|---|---|
| `MC1BoreSweep` | −10 | yes | 0 | 5.000 | PASS | 2440 | 11.8 |
| `MC1FitLadder` | −8 | yes | 0 | 3.825 | PASS | 1776 | 7.5 |
| `MC1Pin03` | 2 | yes | 0 | 3 | PASS | 256 | 0.1 |
| `MC1Pin04` | 2 | yes | 0 | 4 | PASS | 256 | 0.2 |
| `MC1Pin05` | 2 | yes | 0 | 5 | PASS | 256 | 0.3 |
| `MC1Pin06` | 2 | yes | 0 | 6 | PASS | 256 | 0.4 |
| `MC1Pin08` | 2 | yes | 0 | 8 | PASS | 256 | 0.8 |
| `MC1Pin10` | 2 | yes | 0 | 10 | PASS | 256 | 1.2 |
| `MC1FitGauge` | 2 | yes | 0 | 6 | PASS | 256 | 0.4 |
| `MC2Wall04` | 0 | yes | 0 | 0.40 | **FAIL — by design** | 768 | 0.2 |
| `MC2Wall06` | 0 | yes | 0 | 0.60 | **FAIL — by design** | 768 | 0.4 |
| `MC2Wall08` | 0 | yes | 0 | 0.80 | **FAIL — by design** | 768 | 0.5 |
| `MC2Wall10` | 0 | yes | 0 | 1.00 | **FAIL — by design** | 768 | 0.6 |
| `MC2Wall12` | 0 | yes | 0 | 1.20 | PASS | 768 | 0.7 |
| `MC2Wall16` | 0 | yes | 0 | 1.60 | PASS | 768 | 1.0 |
| `MC2Wall20` | 0 | yes | 0 | 2.00 | PASS | 768 | 1.3 |
| `MC3BridgePlate` | 2 | yes | 0 | 4.500 | PASS | 2596 | 27.5 |
| `MC4OverhangFan` | 0 | yes | 0 | 26.817 | PASS | 4608 | 11.9 |
| `MC5WarpPlate` | 0 | yes | 0 | 1.6 | PASS | 720 | 15.3 |
| `MC6Tower03` | 2 | yes | 0 | 3 | PASS (+F7 warn) | 256 | 0.3 |
| `MC6Tower05` | 2 | yes | 0 | 5 | PASS (+F7 warn) | 256 | 0.8 |
| `MC6Tower08` | 2 | yes | 0 | 8 | PASS | 256 | 2.0 |
| `MC6Tower12` | 2 | yes | 0 | 12 | PASS | 256 | 4.5 |

The four `FAIL` rows are the expected outcome described in §3.1, not defects. All four
are watertight; the gate refuses to write their STLs only because of the feature floor,
and they render on the `--check`-less command line in §6.

The four flat plates carry more triangles than a bare plate would because each now has
an engraved coupon id (§3.2): `MC-1 BORE`, `MC-1 FIT`, `MC-3`, `MC-5`. The engraving is
a blind pocket, so it leaves `euler`, `degenerate`, `watertight` and — because it is
kept out of the feature-floor measurement — `minFeature` unchanged, and removes too
little material to move any plate's volume at 0.1 cm³. It changes only the triangle
count, and every label clears §5's gap-and-counter gate in the shipping face (the same
`--check` that wrote these rows runs that gate; a merging label would fail the build).

**This table is executable.** `make coupons` renders every rung per §6 and diffs the
mesh gate's actual output against the row above — including running `--check` on the
four sub-floor rungs specifically to assert they *fail*, at the minFeature named here.
So the by-design failures are tested rather than exempted, and relabelling one of them
`PASS` is caught. It also cross-checks that §6's shell block and this table name the
same rungs, and that they sum to the total stated below.

**Validator:** `build/verify_machine_card.py` compares each rung's `euler`,
`watertight`, `degenerate`, `minFeature`, `--check` verdict, triangle count and volume
against its row, at the decimal precision the row states.
PASS: `MC1BoreSweep` renders `euler=-10 degenerate=0 minFeature=4.999999965721486mm —
PASS`, 2440 triangles, 11.8 cm³ — matching row 1 once minFeature is read at the three
decimals the row writes.
FAIL: `MC2Wall04` renders `— PASS` under `--check`, or renders at `minFeature=0.45mm`
against a row that says `0.40`, or `MC6Tower03` raises no F7 warning. Each is a
mutation `make validate-coupons` applies to a scratch copy of this doc, to confirm the
verifier reports it; a gate nobody has watched fail is not a gate.

**Independent geometry checks**, because a mesh gate PASS is not the same as "the
geometry is what was designed":

- MC-4's outer silhouette radius was read back out of the rendered STL at every z and
  matched the design table exactly at all twelve vertices (10.0000 / 11.4559 / 11.4559
  / 13.7653 / 13.7653 / 17.1217 / 17.1217 / 21.1217 / 21.1217 / 25.8887 / 25.8887 /
  32.8169), and the inner silhouette matched `outer − 4` at all twelve. Its volume was
  computed independently by Pappus (profile area 116 mm² × 2π × centroid radius
  16.3586) as 11.92 cm³, against 11.9 reported.
- MC-3's STL has z levels at exactly 0, 4 and 6 — pockets 0→4, ceiling 4→6 = 2 mm.
- Plate footprints read back from the STLs as 90 × 24 (MC-1 sweep), 120 × 80 (MC-5),
  160 × 34 (MC-3).
- Every plate's volume matches its closed-form `l·w·d − Σ(π/4)d²·depth` to the reported
  0.1 cm³.

**Total solid volume across all 23 pieces: 89.7 cm³** — roughly 111 g of PLA at 100%
infill, less in practice since MC-1's and MC-3's plates are the only pieces with a
meaningful interior. MC-3 alone is 27.5 cm³ and MC-5 is 15.3 cm³.

**What this record does not establish.** Not one number on this card. `--check` PASS
means the mesh is sound; the print gate's F7 warnings on MC-6 mean the *current
provisional threshold* would flag those towers, not that those towers will detach. No
CAL bet moves from `provisional` to `measured` on the strength of anything in this
section, and `calibrate`'s rules forbid it.

## 8. Known weaknesses, recorded rather than fixed

- **`MIN_BED_CONTACT_RATIO` is not directly measured.** A straight rod's first layer is
  its widest layer, so the ratio is 100% for every MC-6 rung and the relative trigger is
  never exercised. It rides `CAL-BED-01` and would be settled by inference from the
  absolute figure. A coupon that tested it properly needs a tall part that is narrow at
  the bed and wide above — a mushroom — which is a second geometry and a second variable,
  so it is not on this card.
- **MC-4's wall thickness co-varies with the angle under test** (§5.4). Mitigated by
  keeping the thinnest rung at 2.00 mm, well clear of any plausible floor, but not
  eliminated. It cannot be eliminated without a polygon offset primitive.
- **The mesh gate is silent on both of the dimensions MC-3 and MC-4 are built around**
  — the 2 mm bridged ceiling and the 2 mm fan wall. Both PASS results are about mesh
  soundness only (§5.3, §5.4).
- **No raster render was eyeballed.** Geometry was verified numerically against the
  design tables instead (§7), which is a stronger check for a coupon whose failure mode
  is a silently wrong dimension, but it is not the same as looking at it. Look at the
  fan in a slicer before committing filament.
- **Rung identity survives onto the four flat plates but not the round coupons** (§3.2).
  Text emit (T2) fixed this for the plates outright; the emitter is extrude-only, so the
  14 rods, 7 tubes and the fan still rely on filename plus size-ordering plus bagging.
  Extending the emitter to rod tops / tube rims / cone flanks is a genuine second feature,
  not a placement tweak, and is deferred rather than in this card.
- **Every rung range is unvalidated** (§2) — MC-3's is argued from `w2` §B.3's survey
  rather than guessed, but a survey is not a caliper either. This is not a weakness to
  be fixed before printing; it is the reason for printing.

## 9. Measuring

The protocol is not optional and it is not in this document — it is
[`.claude/skills/calibrate/protocol.md`](../.claude/skills/calibrate/protocol.md),
which carries the profile header (machine, material *and colour*, spool, nozzle type,
layer height, verbatim profile name, ambient, date, instrument), the technique rules
(three readings, median, two orthogonal bore diameters, light jaw pressure, 30 minutes
of cooling), the per-coupon judgement scales, and the blank data sheet. A reading
without a profile header is anecdote, not calibration (bikar Tenet 30).

Print orientation, per coupon, since the geometry does not carry it:

| Coupon | Orientation | Why it matters |
|---|---|---|
| MC-1 plates | flat, bores vertical | bores print as vertical holes, which is how designs use them |
| MC-1 pins | upright, on the ⌀ face | matches the bore's axis; a pin printed lying down is elliptical |
| MC-2 tubes | upright | the wall is a vertical perimeter loop, which is the case under test |
| MC-3 plate | flat, **bore mouths on the bed** | flipped, there is nothing to bridge (§5.3) |
| MC-4 fan | upright, base on the bed | the flare is the overhang; any other orientation is a different test |
| MC-5 plate | flat | warp is a first-layer phenomenon |
| MC-6 towers | upright, bare plate, **no brim/raft** | the brim is the mitigation, not the measurement |

Print the whole card in **one material, one profile, one session** where the bed allows
it. A card printed across two sessions has two profile headers and is two half-cards.

When a reading lands, `calibrate`'s **Propagate** workflow is what closes it: the
constant's value *and* its `Calibrated<T>` provenance flip together, the design doc's
Appendix B entry closes with the measured value, the catalog entry flips, `bets.md` is
regenerated, and commit hashes are cited in both repos. Until every one of those has
happened the bet is open, whatever the bench notebook says.
