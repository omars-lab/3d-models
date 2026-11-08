---
id: Lego/Pin-Rail
aliases:
  - Pin-Rail
title: Pin-Rail
family: lego
status: built
bikar files:
  - patterns/Lego/Pin-Rail.bkr
tags:
  - library
  - lego
---

# Pin-Rail

From bikar's pattern library: `bikar:patterns/Lego/Pin-Rail.bkr`, in the lego family.

No picture: bikar draws no flat picture of this file at its default knobs. Some orbs, lego pieces and coupons exist only as solids.

## What the file says

```text
Pin-Rail — a 1 × 8 strip, the footprint class that gets *pins* instead of
tubes.

§3.3's census is a rule about shape, not size: a footprint needs two studs
in both axes to have an interior vertex a tube can sit on, so anything
`1 × n` takes solid pins between the studs of the host row and a `1 × 1`
takes nothing at all. `anchors auto` picks; this preset exists so the
picker's other branch is one click away in the Lab and shows up in the
lattice overlay as pins on the row line rather than tubes on the grid
crossings.

A rail is also the piece where rotation lock is thinnest. Seven pins in a
straight line resist twisting only through their own spacing, and the
clutch is doing that work alone — there is no second row to triangulate
against. Print it before assuming a long thin piece behaves like a brick.

`studs full` keeps it stackable and, at 1 × 8, useful as an edge or a
spacer. `rows` stops at 2 rather than 1: a 1 × 1 gets no anchor at all, so
it fails §5.3's hard gate outright and V7 warns that a single stud cannot
lock rotation — the degenerate end of the same fact, and not something to
put a slider stop on top of.

Render:
  bikar render patterns/Lego/Pin-Rail.bkr --format stl --check -o PinRail.stl

Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
coupon LG-F1). Print the coupon before trusting the fit.
```

## Knobs

| Knob | Default | Range |
|---|---|---|
| `rows` | 8 | 2..12 |
| `plates` | 3 | 1..9 |
| `engage` | 3.2 | 1.6..4.0 |

<!-- written by hand below this line; the sync tool stops here -->

## Notes

Nothing written by hand yet.
