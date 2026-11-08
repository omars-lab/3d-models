---
id: Lego/Classic-Brick
aliases:
  - Classic-Brick
title: Classic-Brick
family: lego
status: built
bikar files:
  - patterns/Lego/Classic-Brick.bkr
tags:
  - library
  - lego
---

# Classic-Brick

From bikar's pattern library: `bikar:patterns/Lego/Classic-Brick.bkr`, in the lego family.

No picture: bikar draws no flat picture of this file at its default knobs. Some orbs, lego pieces and coupons exist only as solids.

## What the file says

```text
Classic-Brick — the reference part: a plain 2 × 4 with studs on top and
anti-studs underneath, i.e. LDraw `3001.dat` printed instead of moulded.

It carries no art on purpose. Every other preset here changes one thing
about this piece, so this is the one to print first and the one to measure
a clutch against: if a real brick will not stack onto this, no amount of
pattern work downstream is going to fit either. That is also why it is the
preset whose knobs are the *interface* dimensions rather than the art —
`plates`, `engage`, and the footprint itself.

`studs full` is what makes it stackable, and it is the mode V4 refuses to
combine with relief: a stud sits 1.6 mm proud of exactly the surface art
would be cut into. A patterned piece gives up stacking; this one gives up
the pattern. There is no setting that gets both on one face.

The 2 × 4 footprint is where §3.3's contact census is least forgiving: the
tangent side wall supplies 50 % of the clamping contacts on this shape (67 %
on a 2 × 2), so the three tube anchors are only half the grip and the shell
wall is the other half. `clutch auto` emits the §7.6 rib set into both.

Render:
  bikar render patterns/Lego/Classic-Brick.bkr --format stl --check -o ClassicBrick.stl
    (STL = the printable brick; stderr = the anchor gate and §6 warnings)

Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
coupon LG-F1). Print the coupon before trusting the fit.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `cols` | 2 | 2..8 |
| `rows` | 4 | 2..8 |
| `plates` | 3 | 1..9 |
| `engage` | 3.2 | 1.6..4.0 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
