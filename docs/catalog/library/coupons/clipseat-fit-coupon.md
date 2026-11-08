---
id: Coupons/Clipseat-Fit-Coupon
aliases:
  - Clipseat-Fit-Coupon
title: Clipseat-Fit-Coupon
family: coupons
status: built
bikar files:
  - patterns/Coupons/Clipseat-Fit-Coupon.bkr
tags:
  - library
  - coupons
---

# Clipseat-Fit-Coupon

From bikar's pattern library: `bikar:patterns/Coupons/Clipseat-Fit-Coupon.bkr`, in the coupons family.

No picture: bikar draws no flat picture of this file at its default knobs. Some orbs, lego pieces and coupons exist only as solids.

## What the file says

```text
Clipseat-Fit-Coupon — the W-F1 clip-in-notch fit ladder. Catalog entry
W-F1; the coupon W-C1 is blocked on.

THE JOINT UNDER TEST. Four clipseat tiles meet at a corner. The gap
between them is a cross-shaped channel, and a CornerClip drops its four
jaw blades down that channel from behind before twisting ~30° to land
them on the front border band. The blade has to pass a channel it did
not print in the same pass — different part, different perimeter, all
of one machine's XY error between them. The clearance that makes that
pass is `CLIP_CLEARANCE_MM.insert` in kernel3d/corner-clip.ts, today a
provisional 0.2 mm diametral read off other people's twist-lock seats
on other people's machines. Nothing has been printed and nothing has
been twisted. This coupon prints it.

THIS IS NOT THE BORE-AND-PIN LADDER. Fit-Coupon.bkr and the machine
card's MC-1 measure a peg going straight into a hole: one axis, full
contact, no rotation. A blade sliding down a slot and then sweeping
sideways under load is a different failure mode — it can pass the drop
and still bind on the twist — so a number measured there does not
transfer here, which is the whole reason this file exists. The catalog
pointed W-F1 at Fit-Coupon.bkr until 2026-08-02; it was pointing at the
wrong joint.

HOW THE LADDER WORKS. The four tiles are laid at the nominal `wall_gap`
— one physical channel, printed once. The ladder is on the *clip*: each
rung declares a gap the wall does not have, and the difference is the
clearance under test. A clip declared for gap g gets a blade of width
g − CLIP_INSERT_CLEARANCE_MM, so in a channel of width `wall_gap` its
diametral clearance is `wall_gap − g + 0.2`. Rung names are that
clearance in hundredths of a mm, which is the quantity being
calibrated and does not move when `wall_gap` does:

  FitClipC40  gap wall_gap-0.20   0.40 mm clearance   (loosest)
  FitClipC30  gap wall_gap-0.10   0.30 mm
  FitClipC20  gap wall_gap        0.20 mm   <- the shipped guess
  FitClipC10  gap wall_gap+0.10   0.10 mm
  FitClipC00  gap wall_gap+0.20   0.00 mm   (must not pass — see below)

THE LADDER IS BUILT TO BE ABLE TO FAIL AT BOTH ENDS. C00's blade is
exactly as wide as the channel, so if it drops through, the answer is
not "0.00 works" — it is that this machine is undersizing the blade or
oversizing the channel, and the reading is a measurement of that error.
C40 is close to the two-perimeter floor the resolver enforces
(2 × PERIMETER_WIDTH_MM = 0.8 mm blade at wall_gap 1.2), so a C40 that
drops through freely but shears on the twist is the other bound: the
blade got thin enough to stop being a structural member.

THE CONFOUND, STATED. Declared gap does not only set the blade. It also
sets `rPadOutMm = rJaw − gap/√2`, so a wider declared gap gives a
shorter pad reach over the border band. The two move together and the
coupon reports the pair, not either alone — which is fine, because the
deliverable is one number (`profile.gapMm`, the value to declare) and
not a decomposition. A failed rung still tells you which effect bit,
by inspection: a blade that will not enter the channel is the blade; a
clip that enters, twists, and then rocks or pulls off is the reach.

WHAT IT DOES NOT MEASURE. Not the Z stack — riser height, anti-rattle
preload and back-flush setback are CAL-CLP-01 and belong to W-C1. Not
the detent feel — CAL-DET-01, also W-C1. Not rebate-vs-proud, which is
W-C1's headline decision; this file uses `rebate` because the blade
clearance is set by the gap channel alone and the variant only changes
the jaw pad's thickness, so the ladder reads the same either way.

PRINTING. The tile is deliberately the same 40 mm dummy as
Clip-Coupon.bkr's CouponTileRebate — print four and they serve W-C1
afterwards. Clips print in PETG (the intended clip material); the
tiles print in whatever the wall's tiles will be, so their shrinkage
matches the channel you will actually have.

  bikar render patterns/Coupons/Clipseat-Fit-Coupon.bkr --format stl --piece FitClipTile --check -o FitClipTile.stl
  bikar render patterns/Coupons/Clipseat-Fit-Coupon.bkr --format stl --piece FitClipC40 -o FitClipC40.stl
  ... and the same for C30, C20, C10, C00.

Render the clips WITHOUT `--check`: a bayonet blade is ~0.6 mm, below
the 1.2 mm mesh-gate floor, so a clip part reports FAIL by design
(w2-connector-design.md §10 Q1). The tile passes cleanly.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `wall_gap` | 1.2 | 1.0..2.0 |
| `dummy` (advanced) | 40 | 30..60 |
| `depth` (advanced) | 10 | 8..14 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
