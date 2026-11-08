---
id: Coupons/Machine-Card
aliases:
  - Machine-Card
title: Machine-Card
family: coupons
status: built
bikar files:
  - patterns/Coupons/Machine-Card.bkr
tags:
  - library
  - coupons
---

# Machine-Card

From bikar's pattern library: `bikar:patterns/Coupons/Machine-Card.bkr`, in the coupons family.

![Machine-Card](../../media/library/coupons/Machine-Card.webp)

The file drawn at its default knobs.

## What the file says

```text
Machine-Card — the shared-substrate characterization card.

Six coupons that settle properties of a *(printer, material, nozzle,
slicer profile)* rather than of any one design: bore/fit (MC-1), wall
floor (MC-2), bridge span (MC-3), overhang angle (MC-4), plate warp
(MC-5), bed contact (MC-6). Print the card once per machine/material
pair; every design coupon after it (W-F1, W-C1, LG-F1, P1) then tests
only what is genuinely design-specific.

Geometry rationale, per-rung CLI lines and the measurement protocol:
  3d-models/docs/design/printing/calibration-design.md
  3d-models/.claude/skills/calibrate/protocol.md
Bets settled: CAL-FIT-01, CAL-HOL-01 (MC-1), CAL-FEA-01 (MC-2),
              CAL-BRG-01 (MC-3), CAL-OVH-01 (MC-4), CAL-WRP-01 (MC-5),
              CAL-BED-01 (MC-6) — see kernel3d/calibration.ts.

AUTHORED BLIND. No machine has printed this. Every rung *range* below
is a bracket around an unknown, not a prediction. If a ladder turns
out to be centred wrong — every rung clean, or every rung failed —
that is a result to log and re-cut, not a defect in the card.

RUNG IDENTITY. bikar now emits engraved text on flat plate tops (the
`text` statement, extrude bodies only — 3d-models/docs/design/language/text-emit-design.md),
so the four plate coupons below carry their own coupon id: MC1BoreSweep
and MC1FitLadder say `MC-1 BORE` / `MC-1 FIT`, MC3BridgePlate `MC-3`,
MC5WarpPlate `MC-5`. Within a plate the rungs stay POSITIONAL — the
bores are one ascending size ladder, self-evident in the hand — because
a per-bore label would collide with the bores it names.

The round coupons cannot carry text and are not made to: the emitter is
extrude-only, and a rod top / tube rim / cone flank has no flat face to
engrave. They keep the two mitigations that always applied: (a) one
piece per rung, rendered with `--piece`, so identity lives in the STL
filename; (b) monotone size ordering within every ladder. Keep them in
labelled bags off the plate — an unbagged MC-2 tube is still an
unidentifiable tube.

Two plate labels sit shallower or off the measurand on purpose, because
an engraving is a stiffness/thickness change and those two coupons
measure stiffness and thickness. MC-5 is a warp coupon: its label is
0.4 mm deep (not the 0.6 default) and centred on the bottom edge, far
from all four measured corners and the fiducial, so the recess perturbs
corners C and D equally and cannot bias the corner-to-corner warp it
exists to read. MC-3 bridges on its TOP face over bores that open on the
bed; its label sits at the top edge, clear of the bore line, so it never
thins a bridging ceiling.

MC-2 DELIBERATELY FAILS `--check`. Rungs 0.4/0.6/0.8/1.0 mm sit below
DEFAULT_MIN_FEATURE_MM = 1.2 (kernel3d/mesh-gate.ts), so the mesh gate
reports FAIL *by design* — that gate's own floor is the thing MC-2 is
measuring. Render those four rungs **without** `--check`; the mesh is
still watertight, which is what matters. No `--min-feature` override
flag exists and none is being added (the W-series sub-floor rule,
3d-models/.claude/skills/prototype/catalog.md).

Render (23 pieces; every rung is its own STL):
  bikar render patterns/Coupons/Machine-Card.bkr --format stl --check \
    --piece MC1BoreSweep -o out/MC1-BoreSweep.stl
  ...one line per piece; the full list is in calibration-design.md §6.

BLUEPRINT IDIOM — two constructions recur below, both forced by the
blueprint language and both worth naming once:
  * rectangle: there is no rectangle primitive, so a w x h plate is
    two guide circles of radius (h/2)*sqrt(2) quartered at offset 45,
    inset h/2 from each end; their division points land on the four
    corners. (Fit-Coupon.bkr's idiom, reused verbatim.)
  * profile point: `polygon` vertices must be division points, so an
    arbitrary (r, z) vertex is stamped by a circle centred ON the
    revolution axis at height z with radius r, divided into 1 — its
    single division point sits at exactly (r, z). Each guide circle is
    literally the circle of revolution at that height, which is why
    MC-4's vertex table reads straight off the geometry.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `ref_d` | 6 | 3..10 |
| `plate_depth` | 6 | 4..12 |
| `bridge_z` | 4 | 3..12 |
| `ceiling_t` | 2 | 1..4 |
| `warp_t` | 1.6 | 1.4..3 |
| `tower_h` | 40 | 10..60 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
