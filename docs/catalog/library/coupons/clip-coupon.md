---
id: Coupons/Clip-Coupon
aliases:
  - Clip-Coupon
title: Clip-Coupon
family: coupons
status: built
bikar files:
  - patterns/Coupons/Clip-Coupon.bkr
tags:
  - library
  - coupons
---

# Clip-Coupon

From bikar's pattern library: `bikar:patterns/Coupons/Clip-Coupon.bkr`, in the coupons family.

No picture: bikar draws no flat picture of this file at its default knobs. Some orbs, lego pieces and coupons exist only as solids.

## What the file says

```text
Clip-Coupon — the W2 connector fit coupon: two 40 mm dummy tiles (one
per clipseat variant) plus the CornerClip that mates them. Print four of
each dummy and a handful of clips, then build two real four-corner joints
— one rebate, one proud — to decide the grammar's clipseat default in
plastic (design doc §8, §10 Q1). Every dimension a param so the coupon
re-prints at your gap and depth.

Sub-floor by design: the CornerClip's bayonet blade is ~0.6 mm, below the
1.2 mm FDM floor, so `--check` on the CLIP part reports FAIL — expected.
That thin flexing blade is the whole point of the coupon: it is validated
in plastic, not by the compiler (§10 Q1). The two dummy TILES pass the
floor cleanly (the rebate lip is a supported step the gate excludes, not a
free-standing wall) — so only the clip is exempt, and only on the coupon.

There is no `assembly` here: a bayonet CornerClip has no connectable port,
so it cannot join an assembly's connect graph. Render each part by name:
  bikar render patterns/Coupons/Clip-Coupon.bkr --format stl --piece CouponTileRebate --check -o CouponTileRebate.stl
  bikar render patterns/Coupons/Clip-Coupon.bkr --format stl --piece CouponTileProud  --check -o CouponTileProud.stl
  bikar render patterns/Coupons/Clip-Coupon.bkr --format stl --piece CouponClip              -o CouponClip.stl
    (drop --check on the clip — its blade is intentionally sub-floor)
Add --fit-profile petg_calibrated to widen the seat wells for your printer
once the Fit-Coupon has set the profile; the authored dims stay the contract.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `gap` | 1.2 | 0.8..2.0 |
| `depth` | 10 | 8..14 |
| `dummy` (advanced) | 40 | 30..60 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
