---
date: 2026-09-17
produced-by: this session — bikar `feat/coaster-shape-v2` (PR NaqshCoffee/bikar#208) dist: `interlock_probe.mjs` (the two goldens evaluated at size 40 and 90 with `margin` overridden, the fitted outline's ring, a self-mating dovetail ring built on it, and the signed distance of every drawn segment endpoint to both rings), `edge_lengths.mjs` (side length and edge parity of the seven outline candidates), and a read of `coaster.ts`, `coaster-validate.ts` and `grid-gate.ts` at bikar 30db06a
feeds: docs/coaster-interlock-design.md, docs/coaster-design.md §9, docs/decisions-log.md D-069
---

# Coaster interlock study

Verbatim measurements behind the interlocking-edge design
([`../coaster-interlock-design.md`](../coaster-interlock-design.md)): what the seven
fitted outlines offer as an edge, which tab pairings tile on which of them, what a
slot costs the art enclosure, and what the coaster kernel can and cannot do with a
non-convex ring today. Nothing here has been printed; every number is geometry.

## 1. The ask

Omar, on the *Coaster Shape Study* artifact (thread `5bb38d7f`, 2026-09-17):

> how can we make the edges plug into other coasters? so they can be interconnected?
> like legos?

Three shapes were offered in reply — dovetail tabs, a self-mating S-profile, side
studs — with a lean to the dovetail and the note that the enclosure check must keep
measuring the nominal hexagon. This study is the measurement behind that lean.

## 2. What each fitted outline offers as an edge

Shape v2 fits one of seven regular candidates (D-066). Six are polygons and one is
round. Side length is `size · tan(π/N)` for across-flats `size` (the square's side
*is* its size). `edge_lengths.mjs`, 2026-09-17:

| Candidate | N | size 40: edge mm | L/4 | size 90: edge mm | L/4 |
|---|---|---|---|---|---|
| square | 4 | 40.00 | 10.00 | 90.00 | 22.50 |
| polygon 4 rotate 45 (diamond) | 4 | 40.00 | 10.00 | 90.00 | 22.50 |
| polygon 6 (rotate 0 or 30) | 6 | 23.09 | 5.77 | 51.96 | 12.99 |
| polygon 8 (rotate 0 or 22.5) | 8 | 16.57 | 4.14 | 37.28 | 9.32 |
| round | — | no edge | — | no edge | — |

`L/4` is the room a half-edge tab has on each side of its centre (§4). A round
outline has no straight edge to mate and cannot tile the plane; it is out.

## 3. Edge parity: which pairing tiles

**Alternating edges** (tab, slot, tab, slot … around the polygon) only tile when a
tile's edge `k` faces a neighbour's edge of the *other* kind under pure translation.
The neighbour across edge `k` presents its edge `k + N/2`; the two have the same
parity when `N/2` is even and opposite parity when `N/2` is odd:

| N | N/2 | opposite edge's parity | alternating tab/slot tiles by translation? |
|---|---|---|---|
| 4 (square, diamond) | 2 | same | no — every other tile must be turned one edge (a checkerboard rule) |
| 6 (hexagon) | 3 | opposite | yes |
| 8 (octagon) | 4 | same | no — same checkerboard rule; octagons alone do not tile the plane anyway |

So an alternating dovetail works on the hexagon only. On the square, the diamond and
the octagon it needs a rotation rule the user has to know, and two identical tiles
placed the obvious way collide tab-on-tab.

**Self-mating half-edge profile.** Put the tab on the first half of every edge
(centred at `L/4` from the edge's start vertex, protruding) and the slot on the
second half (centred at `3L/4`, cut in), the slot the 180°-rotated image of the tab
about the edge midpoint. A neighbour traverses the shared edge in the opposite
direction, so its first half is our second half: its tab meets our slot and our tab
meets its slot, **on every edge, in every orientation, on every N**. No parity, no
rule to remember. Two coasters of the same outline and size mate on any edge pair;
different outlines or sizes cannot mate (their edge lengths differ, §2).

## 4. Room on the edge: the land beside a tab

For a dovetail with neck `n`, depth `d`, head `h = n + d` (the design's construction
choice, §4 of the design doc) and clearance `c`, the solid land between the slot's
head and the vertex — and equally between the slot's head and the edge midpoint — is
`L/4 − h/2 − c`. With `n = d = 3`, `c = 0.15` (so `h = 6`):

| Candidate, size | L/4 | land mm | ≥ 0.8 (CAL-CST-01 strap floor)? |
|---|---|---|---|
| square / diamond 40 | 10.00 | 6.85 | yes |
| hexagon 40 | 5.77 | 2.62 | yes |
| octagon 40 | 4.14 | **0.99** | yes, barely |
| square / diamond 90 | 22.50 | 19.35 | yes |
| hexagon 90 | 12.99 | 9.84 | yes |
| octagon 90 | 9.32 | 6.17 | yes |

Octagon at size 40, growing the tab: `n = d = 4` → land −0.01 mm (the slot reaches
the vertex); `n = d = 5` → −1.01 mm. The mini octagon is the binding case for a tab
room check.

## 5. What a slot costs the enclosure

The goldens ship `margin 2` (D-066: the art's farthest point sits 2.00 mm inside the
nominal outline — CV7's PASS value). A slot cut `d + c` into that margin puts the
slot bottom **inside** the art wherever a slot lands over it. `interlock_probe.mjs`,
segment endpoints standing in for CV7's point set, `n = d = 3`, `c = 0.15`:

| Golden, size | margin | CV7 (nominal inset) | CV8 (inset from the slotted ring) |
|---|---|---|---|
| GimTvN9hw4U (hexagon rotate 30), 40 | 2 (as shipped) | 2.00 PASS | **−1.15 FAIL** at (−4.00, −18.47) |
| GimTvN9hw4U, 90 | 2 | 2.00 PASS | −1.15 FAIL at (33.44, −30.34) |
| 7apC5Q9QS-8 (square), 40 | 2 | 2.00 PASS | −1.15 FAIL at (18.00, 9.00) |
| 7apC5Q9QS-8, 90 | 2 | 2.00 PASS | −1.15 FAIL at (43.00, 21.50) |
| both goldens, both sizes | 4 | 4.00 PASS | **0.85 FAIL** (needs ≥ 1.00) |
| both goldens, both sizes | 5.15 | 5.15 PASS | 2.00 PASS |

The arithmetic is exact: the worst art point is `margin` inside the nominal outline
and `margin − d − c` inside the slotted ring, so the interlock needs
`margin ≥ d + c + w/2` (w = strap width). At `margin 4` the art clears the nominal
outline by four times CV7's limit and still fails CV8 by 0.15 mm — the case CV7
cannot see. With `d = 6`: −2.36 mm at size 40 on the hexagon (`margin 2`).

The cost in art: at size 40 with `margin 5.15` the art spans 29.7 mm instead of
36 mm. An interlocked mini is a smaller picture on the same tile.

## 6. What the kernel can do with a non-convex ring (bikar 30db06a)

- `outlineRing(outline, pitch)` returns the nominal convex ring; `regularPolygon`
  puts the first flat on −y at rotation 0. A slotted ring is a new function on top
  of it, not a change to it.
- `outlineInset(outline, p)` is **convex-only** by construction (support planes; its
  own docblock says so) and is what CV7 reads. It stays as CV7's instrument.
- `signedDistToRing(p, ring)` in `grid-gate.ts` is exact for any simple ring,
  positive inside, and is what CV8 reads against the slotted ring. The probe's
  numbers in §5 come from a copy of it.
- `sampleField(spec)` masks cells on the 0.4 mm grid (`COASTER_GRID_PITCH_MM =
  PERIMETER_WIDTH_MM`), and the mesh's side wall is built from `boundaryLoops(field)`
  — the **grid-cell staircase**, not the exact ring. That is invisible on a plain
  coaster (a 0.4 mm stair on a 90 mm edge) and fatal on a joint: a tab and a slot
  whose walls are quantised to 0.4 mm cells carry up to ±0.2 mm of staircase per
  wall, more than the 0.15 mm sliding clearance they are meant to hold. The
  interlocked wall has to be emitted from the exact ring.
- The bottom chamfer offsets the outer loop with `insetPolygon(loop, run)` and
  throws when the inset collapses; it has been exercised on convex loops only. A
  dovetailed ring has reflex vertices at every slot mouth and neck, where a naive
  offset self-intersects. Unverified, so refused together (K10) rather than trusted.
- `CV7` builds its point set from strap endpoints (half a strap width of inset
  needed) and face vertices (any inset); the same point set serves CV8.

## 7. Fit clearance: what CAL-FIT-01 records

`.claude/skills/calibrate/bets.md`, `FIT_GAP_MM_CAL` (bikar `fit-profile.ts`),
2026-09-17:

> press −0.1 · snug 0.05 · sliding 0.15 · free 0.35 (mm). Literature-shaped FDM
> clearance ladder, spaced on an even 0.10 mm step for legibility rather than fitted
> to any machine; no pin and socket have been printed and mated. Coupon MC-1 (bore &
> fit plate) settles it.

The ladder is an XY-plane clearance between two separately printed parts on the same
nozzle, which is exactly what a coaster tab in a coaster slot is; the transfer
sentence lives in the design doc. The same record notes that this is a bet, not a
measurement, so an interlock clearance drawn from it inherits its status.
