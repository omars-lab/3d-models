# The coaster outline is fitted to the art, not traced from it — and the "clipped" claim was wrong

*Issue slug: `coaster-outline-fit-pivot`. Written 2026-09-17 while landing coaster
shape v2 (bikar NaqshCoffee/bikar#208, decisions D-066…D-068). Measurements in
[`../research/coaster-shape-study.md`](../research/coaster-shape-study.md).*

## What was asked

Omar, on the disc coasters P2.7 produced: "instead of circle coasters, can we make
the pattern pop out more? can they be hexagonal, square, etc based on the pattern …
want to minimize the flat borders around the edges of the coaster", then "or even
trace the outer border / add a border bezel". Three changes of approach followed;
each is recorded here so the next session does not re-walk them.

## Pivot 1 — the retracted "clipped" claim

**What was said.** The first shape study (artifact *Coaster Shape Study*) stated that
both P2.7 coasters were **clipped**: that `K` in `param unit = ($size - 8) / K` "was
never measured" and that at `size=90` the art overran the 82 mm window the formula
leaves inside a 90 mm disc.

**What the evidence showed.** `K` *was* measured, at import, and recorded in
[`../research/coaster-measurements.md`](../research/coaster-measurements.md): 5.1962
units for GimTvN9hw4U and 5.6569 for 7apC5Q9QS-8, each the art's **enclosing
diameter** (twice the farthest drawn point from the bbox centre). The shape study's
hull probe reproduces both numbers exactly (`circumdiameter 5.1962` and `5.6569`).
So at `size=90` the art's enclosing diameter is `(90 − 8) = 82 mm`, wholly inside the
90 mm disc with the intended 4 mm margin. **Nothing was clipped.** The claim came from
a first hull probe that returned `NaN` (a `$size` substitution bug in the scratch
script) and from reading the top-view renders, where the hexagonal art's straight
flats sit visibly close to the round rim — close is not over. The claim is withdrawn
in the design doc, the decisions log and the republished artifact.

**What is true instead.** A round outline around a hexagonal or square art wastes
area — 21.21 units² of disc around 17.54 units² of hexagon, 25.13 around 16.00 of
square — and that waste, not clipping, is the flat border Omar wanted gone.

## Pivot 2 — "trace the outer border" became "fit the least-area regular outline"

**What was tried.** Tracing the art's convex hull as the coaster outline, as asked.

**What the evidence showed.** The hull is not a regular polygon. GimTvN9hw4U's hull
has **23 vertices** (the six-fold rosette's outer straps end at different radii);
7apC5Q9QS-8's has 8, with collinear runs. A traced outline is a per-pattern polygon
with no single across-flats measure, so `unit` cannot be derived from `size` by one
constant (D-065's whole point), the outline cannot be turned by a `rotate` knob, and
an interlocking edge (task #34) has no regular edge to sit on.

**What replaced it.** The importer fits the art's hull to **seven fixed candidates**
(round; square; `polygon 4 rotate 45`; `polygon 6 rotate 0` and `rotate 30`;
`polygon 8 rotate 0` and `rotate 22.5`), measuring `K` in each candidate's own
measure (diameter, side, across flats), and keeps the **least enclosed area** —
earlier candidate wins a tie. GimTvN9hw4U lands on the corner-up hexagon (17.54 vs
21.21 for round), 7apC5Q9QS-8 on the square (16.00 vs 25.13). The margin becomes a
named knob: `param margin = 2 range 1..10`, `unit = ($size - 2 * $margin) / K`.
Grammar gained `outline polygon N <mm> [rotate <deg>]` so the fitted orientation is
expressible; `rotate` was already reserved, so no keyword change.

## Pivot 3 — silent cropping became a validator

**What the evidence showed.** While building the fit, an outline deliberately too
small for its art rendered without any finding: the sampler drops cells outside the
outline, so a cropped pattern is a *valid* mesh (`--check` PASS) with part of the art
missing. The P2.7 design doc had already flagged this in its §9 ("enclosure is not
validated").

**What replaced it.** **CV7 `artEnclosure`** — every strap end must sit at least half
a strap width inside the outline, every face vertex inside it; the worst point is
named with its location; a failing CV7 throws like CV1–CV6b. The hard FAIL witness is
a strap whose centreline is inside but whose width spills (0.5 mm in, needs 1.0).
`outlineInset` (the exact signed inward distance for round, square and regular
polygon) was added to the kernel for it, and CV7's own transfer condition is that the
outline is convex — a concave outline would need a different inset.

## What was kept

D-064 (height field) and D-065 (importer emits the block, `size` drives, `unit`
derived) stand unchanged; the fit only chooses *which* outline and *which* measure
`K` is taken in. `size` stays the single print knob; the mini is still
`--param size=40` of the same file.
