# Tower-Sleeve — captured product idea

Status: **IDEA — UNSPECCED. A bench proof-of-concept exists** (an MC-6 tower rod
seats in the MC-4 cone throat and closes from either end — §2), but nothing is yet
designed, dimensioned, or rendered as a product. No number in this file is measured
or chosen; every quantity below is an **open question**, deliberately, so that
nothing here trips the "invented number" line. This file *tracks* the idea with its
provenance until it earns a real spec — it is not that spec.

Provenance: Omar, 2026-09-18, looking at the printed Plate 1 machine card. The
**MC-6 bed-contact towers** are solid rods —
[`bikar/patterns/Coupons/Machine-Card.bkr`](../../bikar/patterns/Coupons/Machine-Card.bkr)
`piece MC6Tower03` is `rod d 3 height 40`, and ⌀5 / ⌀8 / ⌀12 likewise — printed
only to settle `CAL-BED-01` (which diameter survives on bare plate). Standing on
the bed, they read as a **product** rather than a coupon: bore one through and it
becomes a **sleeve / bushing** — insert an axle, cap either end. The calibration
height (40 mm, for the bed-contact aspect-ratio ladder) is incidental; a product
sleeve would pick a functional length ("could have been made shorter").

Companion: [`calibration-design.md`](calibration-design.md) (the machine card the
towers come from); bet registry
[`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md).

---

## 1. What the product is (one sentence, no dimensions)

A short vertical **sleeve** — a tube — sized so an **axle** slides into the bore
and **either end can be closed** (a plug, an integral lip, or a separate cap). The
solid MC-6 tower with a through-bore and a chosen length.

## 2. Physical proof of concept — 2026-09-18 (unmeasured)

Demonstrated at the bench by combining **two existing Plate 1 coupons**, before any
sleeve was designed: an **MC-6 tower rod** inserts into the **central throat of the
MC-4 overhang fan** (the fan is a `revolve` of a profile with an inner ring, so it
has a bored center) and is **held by friction**, and **either end can be closed**.
So the sleeve-plus-axle-plus-caps concept is not hypothetical — the geometry mates.

The insight worth keeping: Plate 1's headline finding was *this machine prints
tight*, which **refuted** the MC-1 fit ladder (nothing seated at the intended
clearances — a failure for parts meant to slide). For a **friction-fit** sleeve the
same tightness is a **feature** — the tower stays put because the fit is tight. The
product turns the calibration's bad news into its working principle.

Not measured: the tower ⌀ used, the fan throat ⌀, and therefore the actual
interference — all still caliper-pending (#61). This is a qualitative *it mates and
holds*, recorded as such, not a fit number.

## 3. Why it is worth tracking now, not later

It is the **first product this project's own calibration print suggested** — the
card was printed to settle the machine tuple, and looking at what came off the bed
produced a thing to make. That is a loop worth keeping (a print settles bets *and*
spawns products), so the idea is captured here rather than lost in the bench notes.

It also **consumes the exact bets Plate 1 is settling**, so it cannot be honestly
dimensioned ahead of them — the dependency is real, not bureaucratic (see §5).

## 4. Open design questions (all unanswered — none guessed)

- **Bore ⌀ and axle clearance.** The whole product is the bore-to-axle fit. This
  rides `CAL-FIT-01` (fit class) and `CAL-HOL-01` (`holeCompMm`, hole shrinkage) —
  both still direction-only / caliper-pending from Plate 1. Plate 1's headline was
  *this machine prints tight*: bores seated nothing, so a hand-inserted axle will
  need the bore **oversized**, by an amount only the caliper (#61) can set.
- **Is the axle printed or off-the-shelf?** If printed, axle+sleeve is itself an
  MC-1-style fit pair and inherits the same clearance unknown. If a bought rod
  (metal / dowel), the bore is sized to a real diameter and only clearance is ours.
- **Sleeve wall thickness / outer ⌀.** Bounded below by whatever `CAL-FEA-01` /
  MC-2 walls land on for a solid perimeter; unset until that number is real.
- **End closure.** Press-fit plug vs. integral lip vs. separate cap; whether both
  ends close the same way; whether a capped sleeve is a spacer, a bearing, or a
  capsule. Undecided.
- **Length.** Functional, not the 40 mm calibration height. What sets it —
  the axle, the use, or a family of lengths — is open.
- **One part or a family.** The towers were a ⌀ ladder; the product may want to be
  a parametric family (bore ⌀ × length) or a single canonical part. Open.

## 5. What blocks a real spec

The bore clearance **cannot be chosen honestly** until Plate 1's fit reads land as
numbers: `CAL-FIT-01` and `CAL-HOL-01` are the two this product spends, and today
both are recorded direction-only (fits run tight) with magnitude gated on the
caliper (task #61). So this stays an idea until those reads settle — at which point
it becomes the first *design coupon* that reuses a machine-card number instead of
re-measuring it.

## 6. Where it goes when it is real

An authored pattern lives in bikar as a `.bkr` under `patterns/Pieces/` (the home
for functional pieces), rendered and mesh-gated by `make` like every other pattern,
and — once it ships an actual experience — pinned into the actor/use-case map
(`.claude/skills/maintain-use-cases/use-cases.md`). Until then it is exactly what
this file is: an idea in a design doc, per that map's own rule that planned-but-
unshipped experiences live in design docs and the task list, not in the map.
