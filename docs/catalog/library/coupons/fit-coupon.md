---
id: Coupons/Fit-Coupon
aliases:
  - Fit-Coupon
title: Fit-Coupon
family: coupons
status: built
bikar files:
  - patterns/Coupons/Fit-Coupon.bkr
tags:
  - library
  - coupons
---

# Fit-Coupon

From bikar's pattern library: `bikar:patterns/Coupons/Fit-Coupon.bkr`, in the coupons family.

![Fit-Coupon](../../media/library/coupons/Fit-Coupon.webp)

The file drawn at its default knobs.

## What the file says

```text
Fit-Coupon — printer fit calibration in one small print: a 60 x 20 mm
plate with a five-bore ladder plus a gauge pin. Print the plate and one
gauge, then push the gauge into each bore. The tightest bore that takes
the gauge with firm thumb pressure is your press fit; the loosest it
turns in without wobble is your sliding fit.

The ladder is `pin_d + FIT_GAP_MM[class]` verbatim from
kernel3d/fit-profile.ts — press -0.10 | snug +0.05 | sliding +0.15 |
free +0.35 — plus a line-to-line `zero` rung so the ladder has an
origin. Hole names are the class names, not the resulting diameters:
the diameters move with `pin_d`, the classes do not.

WHY THE FitCoupon ASSEMBLY BELOW HAS FOUR CONNECTS. Every rung that is
not `connect`ed to a port of its own fit class can drift away from
FIT_GAP_MM in silence, and three of them did: this file shipped a
+0.10/+0.20/+0.30 ladder against a shipped +0.05/+0.15/+0.35 for long
enough that the catalog pointed at it as the connector fit coupon. One
connect per class is what makes that a hard evaluation error. `zero`
stays unasserted because line-to-line is not a fit class — it is the
origin the other four are measured from.

THE FOUR GAUGES ARE ONE PHYSICAL PART. FitGaugePress / Snug / Sliding
/ Free are identical rods of diameter pin_d; only their port's `fit`
differs, and `fit` is an assertion, not geometry. Print one and use it
in all five bores.

If the press bore is unusably tight, render deliverables with
--fit-profile pla_calibrated (+0.20 mm) or petg_calibrated (+0.25 mm).
Render:
  bikar render patterns/Coupons/Fit-Coupon.bkr --format parts --check -o parts/
  bikar render patterns/Coupons/Fit-Coupon.bkr --format parts --check -o parts-cal/ --fit-profile pla_calibrated

This coupon is the *bore and pin* fit — a peg in a hole. The clip-in-
notch fit that the W-series CornerClip needs is a different joint with
a different failure mode, and it lives in Clipseat-Fit-Coupon.bkr
(catalog W-F1). On the machine card, MC-1's MC1FitLadder is the same
ladder as this one at a 70 mm plate with a six-diameter sweep beside
it; print that one instead if you are calibrating the printer rather
than checking this file.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `pin_d` | 3 | 2..6 |
| `depth` | 6 | 4..10 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
