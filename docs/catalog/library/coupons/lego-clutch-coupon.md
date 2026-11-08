---
id: Coupons/Lego-Clutch-Coupon
aliases:
  - Lego-Clutch-Coupon
title: Lego-Clutch-Coupon
family: coupons
status: built
bikar files:
  - patterns/Coupons/Lego-Clutch-Coupon.bkr
tags:
  - library
  - coupons
---

# Lego-Clutch-Coupon

From bikar's pattern library: `bikar:patterns/Coupons/Lego-Clutch-Coupon.bkr`, in the coupons family.

No picture: bikar draws no flat picture of this file at its default knobs. Some orbs, lego pieces and coupons exist only as solids.

## What the file says

```text
Lego-Clutch-Coupon — the LG-series ladders: three coupons that settle what
no source publishes, which is what a *printed* LEGO-compatible joint does.

Catalogue: `3d-models/.claude/skills/prototype/catalog.md` LG-F1, LG-F2,
LG-R1. Design doc: `3d-models/docs/design/pieces/lego-lab-design.md` §3.3, §3.8, §7.6,
§11 Q1 and Q2. Bet: CAL-RIB-01.

**The ladders are not `param`s, and that is the whole shape of this file.**
A `param` is a knob the source declares and a `brick` statement reads —
footprint, height, engage. Rib thickness, stud ⌀ and pin ⌀ are read by no
brick statement at all: they are `brickFit` offsets, facts about a printer
and a spool rather than about a design, applied at emit time on top of the
tangency datum. So the rungs are swept with `--brick-fit`, and the geometry
below does not change between them. Both halves of that sentence matter —
a ladder whose *design* moved with its rung would measure two things.

Diameters are diametral deltas onto the datum: `studDiaMm = -0.15` means a
4.65 mm stud, not a 0.15 mm one. The shipped default is −0.2 on every mating
surface, which is the convention the surveyed generators ship and not a
measurement of ours — every value here is `'manual'` provenance until a
printed coupon promotes it.

─── LG-F1 — CouponAnchorPlate — rib ladder ────────────────────────────────
  A 2 × 4 tile-style piece: no studs, three anti-stud tubes, fixed bore.
  Rung 0 is the no-rib control and doubles as the bore test — if it clutches,
  §3.8's compliant-rib architecture is unnecessary and that is a real
  finding, not a failed print.

  rungs   --brick-fit ribMm=0 | 0.05 | 0.10 | 0.15 | 0.20
  crossed --param engage=1.6 | 3.2 | 8.0

    bikar render patterns/Coupons/Lego-Clutch-Coupon.bkr --format stl \
      --piece CouponAnchorPlate --brick-fit ribMm=0.10 --param engage=3.2 \
      -o LG-F1-rib010-eng32.stl

─── LG-F2 — CouponStudPlate — stud ⌀ ladder ───────────────────────────────
  A 2 × 4 plate, studs up, engaged into a real LEGO brick's underside. Five
  rungs centred on the 4.8 mm datum at ±0.15:

    4.65      4.73      4.80      4.88      4.95   mm realised ⌀
    -0.15     -0.07     0         +0.08     +0.15  --brick-fit studDiaMm=

    bikar render patterns/Coupons/Lego-Clutch-Coupon.bkr --format stl \
      --piece CouponStudPlate --brick-fit studDiaMm=0 -o LG-F2-stud480.stl

  §11 Q1 is what this decides: whether `studs full` is viable on a 0.4 mm
  nozzle at all. Print one full ladder at 0.4 and, if the machine has one,
  a second at 0.2–0.3 — with a published counterexample worth knowing first,
  since Brickset's 0.2 mm-nozzle brick clutched *worse* than its 0.4.

─── LG-R1 — CouponPinStrip — pin ⌀ ladder ─────────────────────────────────
  A 1 × 4: the footprint class with no interior lattice vertex, so §3.3's
  picker gives it three solid ⌀3.2 pins between the host row's studs instead
  of tubes. Same ±0.15 spread, on `pinDiaMm`:

    3.05      3.13      3.20      3.28      3.35   mm realised ⌀
    -0.15     -0.07     0         +0.08     +0.15  --brick-fit pinDiaMm=

    bikar render patterns/Coupons/Lego-Clutch-Coupon.bkr --format stl \
      --piece CouponPinStrip --brick-fit pinDiaMm=0 -o LG-R1-pin320.stl

  §11 Q2 is what this decides: a pin contacts two studs where a tube
  contacts four, and it is a small solid column loaded laterally — the shape
  FDM layer anisotropy is worst at. If it shears, 1 × N stops being a
  supported footprint and starts being an error with a pointer.

─── Mating parts ──────────────────────────────────────────────────────────
  Real LEGO, every time. Compatibility with our own output proves nothing —
  two printed parts apply the fit profile's offset twice, once per side,
  and that is a different coupon (LG-S1, `patterns/Assemblies/Brick-Stack.bkr`).

─── Recording ─────────────────────────────────────────────────────────────
  Machine, material, nozzle, layer height, XY compensation — and the spool
  plus its dryness. Bambu's own documentation says fit moves with moisture,
  so a LEGO profile is valid for a spool and not for a printer, and LG-F1
  is where that is either confirmed or dismissed.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `engage` | 3.2 | 1.6..8.0 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
