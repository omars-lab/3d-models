# Coaster interlock — edges that plug into each other

*Status: built — NaqshCoffee/bikar#209 (task #34), catalogued as CS-3 in 3d-models. Decision D-069. Measurements in
[`research/coaster-interlock-study.md`](research/coaster-interlock-study.md). The
bikar implementation follows shape v2 (NaqshCoffee/bikar#208) and landed in the same
`coaster` kernel this doc extends:
[`coaster-design.md`](coaster-design.md).*

## 1. The ask

Omar, on the *Coaster Shape Study* artifact (2026-09-17): "how can we make the edges
plug into other coasters? so they can be interconnected? like legos?" Two things are
being asked for: coasters that **join edge to edge** into a larger mat, and a join
that behaves like a toy brick — any piece onto any other, no instructions. The second
half is the harder constraint and is what drives the choice in §2.

The joint has to live inside the coaster of D-064…D-066: a height field over a
fitted regular outline, printed flat, no supports, no boolean union in the kernel.

## 2. Options and the rubric

Two independent choices: the **shape** of the joint and the **pairing** rule that says
which edge meets which. Rubric (0/1/2): **R1 any-to-any** (does any edge of tile A
mate with any edge of tile B, in any orientation?); **R2 prints flat** (full-height
feature on the outline, no overhang, no support); **R3 holds in the plane** (resists
the pull that separates two coasters on a table); **R4 fits the kernel** (a change to
the outline ring and the field clip, not a new solid); **R5 checkable** (a validator
can state PASS/FAIL from the field).

| Shape | R1 | R2 | R3 | R4 | R5 | Verdict |
|---|---|---|---|---|---|---|
| **Dovetail** — trapezoidal tab, head wider than neck | — | 2 | 2 | 2 | 2 | **chosen shape**: a plane-locking joint that is still a 2D outline change |
| S-profile — a wavy edge, the neighbour's wave the inverse | — | 2 | 1 | 2 | 1 | holds only by friction along the wave; no head to lock |
| Side studs — cylindrical pins on one edge, holes on the other | — | 0 | 2 | 0 | 1 | pins printed sideways off a flat coaster are overhangs; holes through a side wall are a new solid the height field cannot express |

| Pairing | R1 | R2 | R3 | R4 | R5 | Verdict |
|---|---|---|---|---|---|---|
| Alternating edges — tab, slot, tab, slot around the polygon | 1 | 2 | 2 | 2 | 2 | tiles by translation on the hexagon only; the square, diamond and octagon need every other tile turned one edge (study §3) |
| **Self-mating half-edge** — tab on the first half of every edge, slot on the second | 2 | 2 | 2 | 2 | 2 | **chosen**: any edge to any edge on every polygonal candidate, no rule to remember |

Alternating edges score full marks on everything but the one thing Omar asked for.
R1 is why the self-mating profile wins even though it puts twice as many features on
the outline. Studs lose on R2 alone; the coaster prints flat and nothing on its side
may overhang.

## 3. The joint

Every straight edge of the outline, traversed counter-clockwise from its start
vertex, carries:

```
 start vertex                 midpoint                    end vertex
 v ──────┐   ┌────────────────┼──────────┐         ┌──────── v'
         │   │  tab (out)     │          │  slot   │
         └───┘                │          └─────────┘  (in, the tab's 180° image)
         ← L/4 →              ← 3L/4 →
```

- A **tab** centred at `L/4`, protruding outward: neck `n` at the edge line, head
  `h = n + d` at depth `d`. Head = neck + depth is a construction choice that fixes
  the flare at about 26.6° a side; it is stated, not sourced, and §10 owns it.
- A **slot** centred at `3L/4`, cut inward: the tab rotated 180° about the edge
  midpoint, then offset outward by the clearance `c` on every face (the probe in the
  study approximates that as neck and head widened by `2c` and depth by `c`).
- Full slab height — the joint is part of the outline, so the bottom is flat, the
  tab's top is at `base` height and carries no relief (the relief field is clipped
  to the **nominal** outline, so tabs are plain and slots are empty).
- A neighbour traverses the shared edge the other way, so its tab lands in our slot
  and ours in its slot. Any edge mates any edge of the same length (study §3).

The **tile pitch** is unchanged: two mated coasters sit at across-flats spacing, the
tab wholly inside the neighbour's slot. A coaster alone spans `size + d` across a
tab. The art is inset by `margin` from the nominal outline as before, and the slots
eat into that margin — §6 CV8 is the check and §7 the cost.

## 4. Grammar

One clause, added to `CoasterStmt` in bikar `docs/grammar.md` §10.3, optional and at
most once:

```ebnf
CoasterInterlock = "interlock" "dovetail" ConstExpr ConstExpr [ "clearance" ConstExpr ] NL ;
```

The two numbers are the neck `n` and the depth `d` in millimetres; `clearance` is
`c` and defaults per §6. `dovetail` is the only profile word today, so a second
profile is a new alternative in the same production rather than a new statement.
`interlock` is a contextual identifier inside the `coaster` body like `outline`
and `strap`; no new reserved word (the G2 keyword snapshot is unchanged).

```bkr
coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  base 4
  relief straps emboss 1.2
  strap width 2
  interlock dovetail $neck $depth clearance $clearance
```

Refusals, each an evaluation error naming the clause:

- `interlock` with `outline round` — a round outline has no edge to mate (study §2).
- `interlock` with `edge … bottom` — the bottom chamfer offsets the outer loop with
  `insetPolygon`, exercised on convex loops only; a dovetailed ring has a reflex
  vertex at every slot mouth and neck, and the offset's behaviour there is
  unverified. Refused rather than trusted (K10: the chamfer's rule was established
  on convex outlines and its transfer to a slotted ring has not been shown).
- `interlock` with `trivet` — a cut-through region next to a slot can leave the slot
  wall as the only material between two voids; the neck check (CV6a) does not see
  the outside as a pocket, so the combination is refused until it does.

## 5. Kernel change

In `bikar/packages/core/src/kernel3d/coaster.ts`:

1. **Slotted ring.** A new function builds the interlocked ring from
   `outlineRing(outline, pitch)` and the `(n, d, c)` triple: per edge, start vertex,
   the four tab points, the four slot points. It is a simple, non-convex, CCW ring.
2. **Field clip.** `sampleField` keeps clipping the relief cells to the nominal
   outline, and additionally masks cells whose centre falls outside the slotted
   ring with `signedDistToRing` (exact, any simple ring — `grid-gate.ts`). Tab cells
   are added at `base` height.
3. **Exact outer wall.** The side wall and the bottom are emitted from the slotted
   ring itself, not from the grid-cell staircase `boundaryLoops` produces. The top
   surface between the outermost sampled cells and the exact ring is a flat collar at
   `base` height. This is the load-bearing change: a wall quantised to 0.4 mm cells
   carries up to ±0.2 mm of stair per face, more than the 0.15 mm clearance the joint
   is asked to hold (study §6). A plain coaster keeps its staircase wall; nothing
   changes for a coaster without `interlock`.
4. **No chamfer.** `bottomRingFor` is never reached with a slotted ring (§4 refusal).

`outlineInset` (convex-only) is untouched and stays CV7's instrument. `--check` runs
the mesh gate on every render as before; the exact-wall stitching is the part most
likely to produce a non-manifold edge, so the bikar PR's fixtures render both goldens
with `interlock` at both sizes through `--check`.

## 6. Validators

Two validators join CV1–CV7 of [`coaster-design.md`](coaster-design.md) §7, both
queries on the same field, both throwing during evaluation when they fail.

The clearance has a default; the tab neck does not yet (§10).

**Default:** interlock clearance = 0.15 mm — CAL-FIT-01, the `sliding` rung of the
fit ladder (press −0.1 · snug 0.05 · sliding 0.15 · free 0.35). This transfers
because the ladder is an XY-plane clearance between two separately printed parts on
the same nozzle, mated in the plane, which is exactly a coaster tab in a coaster
slot; it is a bet, not a measurement (study §7), and coupon MC-1 settles both uses at
once. `sliding` rather than `snug` because a coaster mat is assembled and taken apart
by hand on a table, not pressed once.

### CV8 — the art is enclosed by the slotted ring

**Validator:** every point CV7 checks (strap endpoints needing half a strap width,
face vertices needing any positive inset) lies inside the **slotted** ring by at
least its limit, measured as the exact signed distance to that ring
(`signedDistToRing`). CV7 keeps measuring the nominal outline; CV8 is the extra check
an interlocked coaster needs, because a slot cuts `d + c` into the margin CV7 was
satisfied with. The worst point is named.
- PASS: the goldens with `margin 5.15`, `n = d = 3`, `c = 0.15`: the worst strap end
  sits 2.00 mm inside the slotted ring (limit 1.00) at both sizes, e.g. `(30.99,
  −28.12)` for GimTvN9hw4U at size 90.
- FAIL: the same goldens with `margin 4` — CV7 passes at 4.00 mm, four times its
  limit, and CV8 reports `0.85 mm inside the slotted ring (needs ≥ 1.00 mm)` at
  `(−5.33, −15.40)` for GimTvN9hw4U at size 40. With the shipped `margin 2` the
  slot bottom is 1.15 mm *inside* the art. Neither is visible to CV7.

### CV9 — the tab has room on its edge

**Validator:** on every edge, the land between the slot's head and the nearest of
the edge's vertex and midpoint, `L/4 − h/2 − c`, is at least the strap floor
(CAL-CST-01, 0.8 mm). The land is a full-height rib of solid between a void and the
outside, the same physical thing CAL-CST-01 floors, so the floor transfers as a
*necessary* condition; it is not sufficient, because this rib takes the tab's pull
load and a decorative strap takes none (§10, the neck bet). A land that goes
negative means the slot has broken through the vertex.
- PASS: every polygonal candidate at both sizes with `n = d = 3`, `c = 0.15`: the
  smallest land is the octagon at size 40, 0.99 mm (limit 0.80); the hexagon at 40
  has 2.62 mm, the square 6.85 mm.
- FAIL: the octagon at size 40 with `n = d = 4`: `land −0.01 mm on edge 0 (needs ≥
  0.80 mm)` — the slot reaches the vertex. With `n = d = 5` it is −1.01 mm. Both
  pass CV8 comfortably; only the edge itself is too short.

## 7. Sizing: what the interlock costs

From the study (§4, §5), `n = d = 3`, `c = 0.15`:

| Outline, size | edge mm | land mm | least margin for CV8 (`d + c + w/2`) | art span at that margin |
|---|---|---|---|---|
| hexagon 40 | 23.09 | 2.62 | 4.15 mm (5.15 used, 1 mm to spare) | 29.7 mm |
| square 40 | 40.00 | 6.85 | 4.15 mm | 29.7 mm |
| octagon 40 | 16.57 | 0.99 | 4.15 mm | 29.7 mm |
| hexagon 90 | 51.96 | 9.84 | 4.15 mm | 79.7 mm |
| square 90 | 90.00 | 19.35 | 4.15 mm | 79.7 mm |
| octagon 90 | 37.28 | 6.17 | 4.15 mm | 79.7 mm |

The interlock trades the minimal flat border of D-066 for a border of `margin ≥ d +
c + w/2` — with the worked numbers 5.15 mm instead of 2 mm. On a mini that is a
picture 29.7 mm wide instead of 36 mm. That trade is the reason the importer emits
the clause only when asked (§8): a lone coaster and a mat tile are different
products, and the plain one keeps its tight border.

## 8. Importer

`bikar import geogebra --coaster` gains `--interlock`. Off, the emitted file is
byte-identical to today's goldens. On, it adds three knobs and one clause:

```bkr
param neck = 3 range 2..5              # mm, dovetail neck at the edge line
param depth = 3 range 2..5             # mm, how far the tab protrudes / the slot cuts in
param clearance = 0.15 range 0.05..0.35   # mm, CAL-FIT-01 ladder: snug .. free
param margin = 2 + $depth + $clearance # mm, the plain 2 mm border plus what the slot eats
```

and `interlock dovetail $neck $depth clearance $clearance` as the last clause of the
block. `margin` is derived, so `unit` (D-065) shrinks with it and CV8 passes by
construction at the default; a user who narrows `margin` by hand gets the CV8
finding, not a cropped mat. The `clearance` range is the fit ladder's endpoints, so
the Coaster Lab (#35) can offer snug…free as a slider without inventing numbers.
The neck and depth defaults are choices, not defaults in the D3 sense (§10).

The catalog carries the interlocked variant as its own entry (CS-3) beside
CS-1/CS-2; the gallery shows two mated tiles, because a single tile with
tabs does not explain itself.

## 9. Decisions

- **D-069**: the interlock is a self-mating half-edge dovetail on every straight
  edge — tab on the first half, slot on the second — so any edge mates any edge with
  no orientation rule; the joint is part of the outline ring, walls are emitted
  exact, and the bottom chamfer, `trivet` and `round` are refused with it. See
  [`decisions-log.md`](decisions-log.md).
- D-064…D-068 as in [`coaster-design.md`](coaster-design.md) §8; this doc changes
  none of them. D-068's border band (#36) is sequenced after this, because the tab
  geometry decides what a band's outer edge is: the band follows the nominal
  outline, and tabs and slots are outside it.

## 10. Not yet

- **The tab neck has no floor.** A neck of `n` mm is the narrowest loaded feature
  on the coaster: it takes the pull that separates two tiles. CAL-CST-01 floors an
  unloaded strap and is cited in CV9 as necessary only. The loaded floor is a new
  bet, **CAL-CST-06** (tab neck floor: the narrowest dovetail neck that survives a
  hand pull apart at full slab height), registered in bikar's `CAL_BETS` and
  `bets.md` with the implementation (NaqshCoffee/bikar#209, no `Calibrated` record
  yet), settled on coupon CS-1 alongside CAL-CST-01…05.
  Until it exists this doc states no default for the neck; `neck = 3` in §8 is a
  choice, like `size` and `margin` in [`coaster-design.md`](coaster-design.md) §9.
- **Head = neck + depth** (a 26.6° flare) is a construction choice with no source.
  Wood dovetails use shallower angles; printed puzzle joints steeper. If the joint
  proves loose or won't seat, the flare is the first knob to add, and it wants a bet.
- **Nothing has been printed.** The clearance default inherits CAL-FIT-01's
  provisional status; whether a 0.15 mm gap on a 3 mm tab slides or binds on the X2D
  is what MC-1 measures (owner-gated, D-060).
- **Only same-outline, same-size tiles mate.** A hexagon cannot join a square and a
  40 mm tile cannot join a 90 mm one (study §2). A mixed mat is not a goal.
- **Octagons do not tile the plane alone**; an octagon mat needs square fillers of
  the octagon's edge length, which is a different outline and cannot mate (previous
  bullet). The octagon candidate keeps the interlock for pairs and strips only.
- **The border band (#36) and colour regions (#37)** are unchanged in direction
  (D-068) and now have a stated edge to stop at: the nominal outline.
