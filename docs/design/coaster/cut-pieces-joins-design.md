---
status: decided
date: 2026-10-24
produced-by: Claude (Opus 5.5), from a read of this repo at origin/master 90f2c48 and of bikar's split and dovetail code in the shared checkout, with piece outlines measured from STLs rendered at split-06's settings; no new web research
---

# Cut pieces with pins and slides: both faces printed on the bed

> Status: decided 2026-10-25, option B, one plate with the cut and the joins
> ([D-120](../../working-model/decisions-log.md#d-120--cut-pieces-the-cut-and-the-joins-on-one-plate)).
> Drafted 2026-10-24. Asked by Omar on 2026-10-24, after split-06: "why
> arent we doing split infil pieces with pins for the tiny kits and sliding for bigger ... so that
> it feels like both faces were pronted on plate", then "do we need a sub agent to design more
> experiments with this in mind".

**In short.** The idea is the brainstorm's
[way b](../printing/finish-techniques-brainstorm.md#11-five-ways): cut each loose piece of the
flange coaster through its thickness, print both halves face down, and both faces of the coaster
come off the bed. The measurements below change Omar's split in one place. The small kite has room
for one 1.2 mm pin, as he guessed. Of the bigger pieces, only the two hexagons (inner and outer)
can take a slide: the star and the middle piece turn inward, and bikar's slide refuses any outline
that does. They get pins instead. And the cut halves need no join to stay in the coaster: the
strap over each half's band catches it, as it catches a whole piece today. A join only makes the
pair one part to place and keeps it lined up.

The draft proposed two plates in order: cut pieces with no join (§4.1), then the joins: pins on the
kite, star and middle, and a slide beside pins on the hexagon (§4.2). Omar picked one plate with
both (§4.3, D-120), so all of §5 comes before the print. bikar cannot build it yet (§3).

![Three side views. 1: today's whole piece in the split-06 coaster; its bottom face is a first layer and its top face the last layer. 2: the same piece cut at its middle into two 2.1 mm halves, the cut inside the band under the straps. 3: both halves printed face down, the band stepping out over air as it does today.](cut-pieces-joins-media/cut-piece.png)

Drawn from [cut-piece.side.yaml](cut-pieces-joins-media/cut-piece.side.yaml) with the
draw-side-view skill, not to scale.

## 1. What exists

- **The coaster.** split-06 is the flange coaster at size 112.5: 4.4 mm tall, cut at 2.2 mm, a
  0.8 mm band, room 0.2, a piece gap of 0.10 mm (the small kite 0.12), 1.2 mm pins at a 0.25 mm gap
  ([split-06](../plates/split-06.md)). It printed on 2026-10-24 in 2 h 14 min, so Omar has a whole
  one in hand.
- **How a flange piece prints today.** A 0.6 mm face block, a 3.0 mm band, a 0.6 mm face block:
  4.2 mm in all, printed standing up. The band steps 0.8 mm out over air at 0.6 mm off the bed,
  and its underside came out "Clean or a slight droop" on split-02
  ([record](../../prints/2026-10-15-split-02/index.md)) and "Clean, same as split-02" on split-04
  ([record](../../prints/2026-10-23-split-04/index.md)).
- **Way b.** The brainstorm listed this cut as way b and worried about the band's overhang
  ([§1.1](../printing/finish-techniques-brainstorm.md#11-five-ways)). A half printed face down
  steps out at the same 0.6 mm off the bed by the same 0.8 mm as today's piece, so the two prints
  above answer that worry for the band. They do not answer it for a slot cut into the band (§2.3).
- **What is true of any cut piece**
  ([§1.2](../printing/finish-techniques-brainstorm.md#12-true-of-every-way)): the upper half is
  turned over, never mirrored; both faces now get the first layer's flare (elephant's foot);
  first layers are slow, and nothing here has measured how much time a second one adds.
- **The joins already tried.** The [joining note](../pieces/join-halves-design.md) found a slide
  works on loose halves, a clip is too short on a half this thin, and a screw cannot turn a kite.
  SLD-1 printed 1.6 mm regular hexagon halves with a 0.8 mm rail in a 1.0 mm slot at 0.10, 0.15
  and 0.20 mm a side, and Omar said "alos 10, 15, and 20 all worked ..."
  ([§2](../pieces/join-halves-design.md#2-slide-a-dovetail-across-the-cut)). He did not pick one,
  and the kite rail pair that note left waiting was never printed. D-107 made the slide the first
  join to try ([decisions log](../../working-model/decisions-log.md)).
- **The pins already tried.** split-05 picked 1.2 mm pins at a 0.25 mm gap over 1.0 mm pins, which
  "shakes a bit" ([record](../../prints/2026-10-23-split-05/index.md)). SPL-1 found every gap up to
  0.15 mm too tight to close by hand ([record](../../prints/2026-10-09-spl-1/index.md)).

## 2. The room in each piece

Measured 2026-10-24 from each piece rendered at split-06's settings, at the cut (the band's
outline) and at the face. "Room" is the distance from a point to the nearest edge. "Turns inward"
is the outline's area over the area of its convex hull: 1.0 means it never turns inward.

| Piece | Face: across, area, most room | Band: across, area, most room | Band area over hull |
|---|---|---|---|
| Small kite | 3.2 × 6.2 mm, 10 mm², 1.37 | 5.1 × 9.7 mm, 25 mm², 2.16 | 1.0 |
| Inner hexagon | 11.1 × 15.3 mm, 118 mm², 5.48 | 12.7 × 16.2 mm, 152 mm², 5.93 | 0.994 |
| Outer piece | as the inner hexagon | 12.7 × 17.3 mm, 154 mm², 6.11 | 0.999 |
| Star | 8.6 × 8.2 mm, 25 mm², 2.17 | 13.5 × 12.9 mm, 58 mm², 2.91 | 0.48 |
| Middle (one a coaster) | 18.0 × 19.0 mm, 205 mm², 7.27 | 20.6 × 21.7 mm, 265 mm², 8.0 | 0.77 |

### 2.1 A pin in a half

A half is 2.1 mm: the 0.6 mm face block and 1.5 mm of band. A 1.2 mm pin goes into a 1.45 mm hole
that keeps 0.6 mm of floor under it, the floor the coaster keeps under its own pin holes
(CAL-CST-03). Where the hole sits wholly over the face block it is 1.5 mm deep (2.1 less 0.6).
Where it hangs past the face block there is nothing under the band but air, so it can only be
0.9 mm deep (the band's 1.5 less 0.6). The pin is 0.2 mm shorter than its hole, so the cut faces
close flat and a little sag at the hole's floor does not hold them apart.

*Corrected 2026-10-25, when bikar built it:* this section first said a 1.0 mm pin in a 1.2 mm hole
over a 0.9 mm floor. That floor was a slip: the rule is 0.6 mm, and the hole goes as deep as the
rule allows. On the flange coaster every hole sits over the face block (§5 step 2), so every
pin is 1.3 mm tall.

split-06's notes give a 1.2 mm pin 1.625 mm of room
([split-06.yaml](../plates/split-06.yaml)). Carrying that, and the 0.25 mm gap, to a piece half
transfers because it is the same pin, nozzle, layer height and filament, and the pin again stands
up from a part printed face down into a hole in a part printed face down. What differs: the part
is a few millimetres across, not a 112 mm coaster half, so it may shift or flex when the pin is
pushed home. That is one reason §4.2 tries two gaps.

- **Small kite: one pin, not two.** Along its long axis the band has 1.625 mm of room only from
  about 1.8 mm on one side of the middle to 0.6 mm on the other, and the face block reaches 0.725
  mm (half the hole) only from 1.5 mm on one side to 1.35 mm on the other. One pin 0.6 mm off the middle has 2.0 mm of band
  room and 1.33 mm of face room. Two holes need 2.35 mm between centres (the pin, its gap and a wall), which leaves the
  outer one at the rule's edge and hanging past the face block, so two pins are not proposed.
- **Star: one pin, at its middle.** 2.05 mm of face room, 2.94 of band room. Along its longest
  line the room for a second pin runs out before the 2.35 mm spacing (1.44 mm of band room
  1.5 mm out on one side), so one pin.
- **Middle: three pins.** The face has room for a pin from 8 mm on one side to 8 mm on the other.
- **Hexagons: two pins** about 4 mm either side of the middle, with room to spare, as the
  comparison for the slide.

![Two side views of the small kite to scale. 1: the two halves closed, a 1.2 mm pin 1.3 mm tall from the lower half in a 1.5 mm deep hole in the upper half, a 0.6 mm floor over the face block. 2: both halves printed face down, the pin standing up on one, the hole open on the other; a red note says two pins only just fit.](cut-pieces-joins-media/kite-pin.png)

### 2.2 A slide in a half

bikar's slide checks that the outline never turns inward and refuses one that does, with no
allowance. That rules out the star (0.48) and the middle (0.77). The hexagons' bands measured 0.994
and 0.999, not 1.0, while their faces measured 1.0. The cause is the notches split-06 cuts in
each band round the coaster's pins (§2.4). So the slide refuses the hexagons as split-06 cuts them
too, unless the outline the rail runs on is the face (which never turns inward), the check allows
the notches, or the coaster's pins move off the pieces (§2.4). The kite's band is 4 mm wide at most, and SLD-1's
rail is 4 mm at its root and 0.3 mm a side wider at its top, so the kite takes no slide.

### 2.3 Where the slot runs thin

![Four side views of the hexagon. 1: SLD-1's rail: along the slot, the slot half printed face down, a 1.0 mm slot leaving 0.5 mm of band over air at both ends. 2: a 0.6 mm rail, 0.8 mm slot, leaving 0.7 mm. 3 and 4: both rails closed, across the rail, to scale.](cut-pieces-joins-media/hex-slide.png)

A slot runs from edge to edge so the rail can slide in. At each end it crosses the band's 0.8 mm
step, where the band is printed over air. With SLD-1's 1.0 mm slot only 0.5 mm of band is left
there. The coaster's 0.6 mm floor rule does not carry over: it was set for a floor on solid layers,
and this one is printed over air. A lower rail, 0.6 mm in a 0.8 mm slot, leaves 0.7 mm, but locks
by 0.2 mm a side instead of 0.3, so it holds at 0.10 and 0.15 mm a side and not at 0.20. SLD-1's
clearances carry over only so far: same rail, layer height and printer, but its halves were 1.6 mm
regular hexagons with no band, so the thin end is new.

### 2.4 Risk: pins that bite a piece's point

Two kinds of pin are in play, and neither may sit where it bites a piece's point.

**The coaster's own pins already do.** split-06 fills a 1 mm disc round each coaster pin
(stud_boss 1), and cuts a matching notch in the band of each loose piece beside it. Measured from
split-06's plate file (by the session that sent split-06, 2026-10-24): the inner hexagon and the
outer piece have the same face, a six-cornered kite with a sharp 72° tip. At the band, the outer
piece keeps its 72° tip and only its blunt end is notched. The inner hexagon has its tip bitten flat,
about 1.5 mm across with two 126° corners, and both shoulders notched. split-02 (no pins) and
split-05 (pins, no discs) have clean, matching bands on both. The bite is under the strap, so the
face does not show it, but a cut inner hexagon would carry it in both halves, and it is what turns
the hexagons' band outlines inward (§2.2). Before plate one, the coaster's pin rings should move so
no disc reaches a piece's point (the place-pins skill places them), or plate one should say it is
testing bitten pieces.

**The piece's own pins are placed away from its points.** Each pin in §2.1 sits where the band
has the full 1.625 mm of room round it, which by itself keeps it off a point:

| Piece | Where its pins sit |
|---|---|
| Small kite | one, on the long axis 0.6 mm from the middle toward the blunt end, about 6 mm from the sharp tip |
| Star | one, at the middle; each arm's point is 4 mm or more away |
| Middle | three, at the middle and about 5 mm either side along its longest line; each where the band has the full room, which an arm's narrowing point does not have |
| Hexagons | two, on the long axis about 4 mm either side of the middle, each at least 2 mm from the band's end |

bikar's step 2 (§5) should refuse a piece pin closer than its room rule to the outline, which
covers the points, and the plate page should draw where each pin sits from above.

## 3. What bikar can and cannot do today

- **Can:** build split-06 and its whole pieces; a slide on an extruded convex piece of its own
  (the SLD-1 coupon); pins on the coaster's cut face, with notches in the pieces' bands round them.
- **Cannot:** cut a loose piece in two; put a pin or a hole on a piece half's cut face; put a slide
  on a piece half. The piece builder in bikar's coaster-split code makes a whole piece only, the pin
  site picker runs only on the coaster's own cut face, and the slide hangs only off a standalone
  extruded piece with a `dovetail` line.

So neither plate can be built today, and this note writes no plate file or page.

## 4. The experiments

Both print pieces, not coasters: one of each piece kind, several settings on one bed, in the
green split-06 printed in, so a difference reads as finish, not color. The control is split-06's
own whole pieces: same printer, filament and settings, already printed. Each cut pair is tried in
the split-06 coaster in place of one whole piece of its kind.

### 4.1 Plate one: cut pieces, no join

| Row | Pieces | What changes |
|---|---|---|
| 1 | small kite, inner hexagon, outer piece, star, middle, cut in two | split-06's gaps (0.10, the kite 0.12) |
| 2 | the same five, cut in two | 0.02 mm looser |

Why the looser row: the upper half's face used to be a last layer and is now a first layer, with
its flare, so a cut piece may go into its hole tighter than a whole one. How much is not known;
0.02 mm is a guess, the step between split-05's two kite gaps.

It answers: do both faces read as bed-printed; is the seam seen at the edge; do the two halves sit
level; does the coaster still close round them; does a cut piece fit as a whole one did.

**Validator:** put one cut pair of each kind into the split-06 coaster in place of a whole piece,
close it, and look at both faces in raking light beside the whole pieces still in it.
PASS: both faces of each cut pair look like the whole pieces' bottom faces, no seam can be seen
from either face or at the edge of the hole, the coaster closes as before, and the pair does not
rattle more than the whole piece did.
FAIL: a seam or a step shows at either face or round the hole, one half stands proud of the other,
the coaster does not close, or a pair goes in tighter or looser than its whole piece in both rows.
A pair whose upper face looks like a last layer also fails: that would mean the half was not
turned over.

### 4.2 Plate two: the joins

| Piece | Joins tried |
|---|---|
| Small kite | one pin at 0.25 mm; one pin at 0.30 mm |
| Inner hexagon | SLD-1's rail at 0.10, 0.15 and 0.20; the 0.6 mm rail at 0.10 and 0.15; two pins at 0.25 |
| Outer piece | SLD-1's rail at the clearance that reads best on the inner hexagon, if any |
| Star | one pin at 0.25 mm; one pin at 0.30 mm |
| Middle | three pins at 0.25 mm |

The 0.30 mm rows are there because SPL-1 found the printer runs tight on pins, and a small half
has little to push against.

**Validator:** for each pair, join it by hand, hold it by one half and shake it, then put it in
the split-06 coaster and close it.
PASS: it joins without a tool, the other half stays on when shaken, both faces lie flat on a table,
the slot's thin end has no hole or droop that catches the rail, and the coaster closes round it.
FAIL: it needs a tool or a hard push, a pin or a rail breaks off, the halves part when shaken, a
face stands proud, or the slot's end has sagged so the rail sticks. A slot that holds but shows
through the face also fails.

### 4.3 Options

| Option | Pros | Cons | What it commits us to |
|---|---|---|---|
| **A. Plate one, then plate two** (my pick) | Plate one needs only the cut in bikar (§5 step 1) and answers Omar's question first: does a cut piece look bed-printed on both faces. If loose halves are fine in hand, the joins may be needed only for placing. | Two rounds before a coaster with joins. | bikar step 1 now; steps 2 and 3 only if plate one passes. |
| **B. One plate with both** | One print, the no-join and the joined pairs side by side. | Waits on all three bikar steps; more to judge at once; a fit problem in the cut itself muddies every join. | All bikar work before any print. |
| **C. As first asked: pins on the kite, a slide on every bigger piece** | Matches the first idea exactly. | The slide refuses the star and middle (§2.2); a new slide that clips a rail to an inward-turning outline is new geometry with no print behind it. | A new slide in bikar before anything prints. |

My pick was A, because plate one tests the thing Omar wants (faces) with the least new code, and
its answer decides whether plate two is needed at all.

**Decided 2026-10-25:** B, one plate with both → [D-120](../../working-model/decisions-log.md#d-120--cut-pieces-the-cut-and-the-joins-on-one-plate).
So §4.1's rows and §4.2's rows go on one bed, and bikar takes all three steps of §5 first. The
pairs are tried in a flange coaster Omar has in hand: split-06's, or split-07's once printed (its
0.7 mm socket wall bites the hexagon's point less, §2.4).

## 5. What bikar needs

1. **Cut the loose pieces.** A knob on `hold flange` that cuts each loose piece at its middle into
   two halves, a face block and half the band each, turns the upper half over (never mirrors it)
   and packs the pair side by side, both halves reachable through `--piece`. One call inside it: the 0.2 mm
   of room splits evenly, so each half is 2.1 mm.
   **How it is spelled and named (built 2026-10-25, [bikar #346](https://github.com/NaqshCoffee/bikar/pull/346)):** `hold flange … room 0.2 halves 1`. Both
   halves stay in their color's output, so `--piece Kite` gives every Kite half, upper and lower
   alike; there is no separate name per half. The knob is refused on a lip hold (its piece is not
   the same both ways up) and on a `loose` clause with no `pack`, since an unpacked half would
   land on top of its twin. The closed coaster in the Lab is unchanged; only the bed changes.
2. **Pins on a piece half.** A per-piece-kind count and gap for pins on the cut face, reusing the
   coaster's pin site picker against the band's outline, with the hole kept at 0.6 mm of floor:
   deep over the face block, shallower where it hangs past. Refuse a pin with no room, with the
   room it found. Refuse too any pin or disc, the piece's own or the coaster's, that cuts into a
   piece's point (§2.4), naming the piece and the point.
   **How it is spelled (built 2026-10-25, [bikar 347](https://github.com/NaqshCoffee/bikar/pull/347)):**
   the pin size goes on the hold, `hold flange … halves 1 pin 1.2 gap 0.25 wall 0.9 spacing 0`,
   and each piece kind asks for its count, `loose … pins 2`. `gap` and `wall` default to
   split-05's 0.25 mm and the coaster's 0.9 mm socket wall; `spacing 0` means the least that
   fits, the pin, its gap and a wall, 2.35 mm. The flange coaster pattern carries all of it as
   params (`pin`, `pin_gap`, `pin_wall`, `pin_spacing`, and `pins_middle`, `pins_kite`,
   `pins_hex`, `pins_star`, `pins_outer`), each off at 0. Pins stand on the lower half; the
   upper half takes the holes. On split-04's slice with one pin on the kite and star and two on
   the others, every hole sits over the face block, so every hole is 1.5 mm and every pin 1.3 mm;
   a hanging hole does not come up on this coaster, so the 0.9 mm case is built but not yet seen.
   `halves` is the switch: with it off, `pin` and `pins` build nothing, so each knob on its own
   still builds (bikar builds every param at its range ends, one at a time). bikar always refuses
   pins on a coaster that is not split. With halves on it refuses pins with no pin size, a wall
   thinner than one line, a spacing under the least, and more pins than a piece has room for (a
   second kite pin: "has room for 1 of its 2 pins … widest room on it is 1.95 mm"), and a coaster
   stud whose bite reaches a piece's point.
   bikar calls a convex corner sharper than 90° a point. That is a line drawn through this
   coaster's own corners, not a printed reading: every tip on it is 36° or 72° and every shoulder
   108° or more, so any line between 72° and 108° sorts them the same
   ([§2.4](#24-risk-pins-that-bite-a-pieces-point)). A coaster with a corner between 72° and
   108° has not been seen, and on one the line would need looking at again. split-07 as it printed still builds whole but is refused with halves on, because one
   of its studs bites a point. So cut pieces that fit split-07 as printed cannot be built: the
   plate needs a coaster whose studs sit off the points (the place-pins skill), which also means
   printing that coaster. Done on paper 2026-10-25: split-07's iteration 2 moved its inner ring
   from 14.3 to 13.0 mm, off the points, and its iteration 3 builds every piece cut, with the
   joins of §4.2's first column ([split-07](../plates/split-07.md)).
3. **A slide on a piece half.** Reuse the dovetail kernel's layer widths on a half's cut face.
   Either run the rail on the face's outline, or allow the hexagons' notches; keep the refusal for
   an outline that turns inward and say which piece it refused. Refuse a slot that leaves under
   0.5 mm of band over the step, so the thin end is a printed setting and not an accident.
   **How it is spelled (built 2026-10-25, [bikar #348](https://github.com/NaqshCoffee/bikar/pull/348)):**
   the rail's size goes on the hold, `hold flange … halves 1 slide 4 gap 0.15 height 0.8`, and
   each piece kind asks for it, `loose … slide 1`. `4` is SLD-1's rail width at its root;
   `height` is in whole 0.2 mm layers, at slope 2 as SLD-1 printed it. The rail stands on the
   lower half and the slot is sunk into the upper half, one layer deeper so the cut faces close
   flat, and the slot runs out through the band at both ends so the rail slides in from the side.
   The rail runs on the face's outline, through its middle along its long way, so a hexagon whose
   band a stud notches is still one clean run. The flange coaster pattern carries it all as params
   (`slide`, `slide_gap`, `slide_height`, and `slide_middle`, `slide_kite`, `slide_hex`,
   `slide_star`, `slide_outer`), each off at 0, and `halves` is the switch, as for pins.
   **Default:** a 0.15 mm gap a side. sld-1 printed 0.10, 0.15 and 0.20, and Omar said all
   three worked without naming one as best ([sld-1's record](../../prints/2026-10-07-sld-1/index.md),
   [pinned](https://github.com/omars-lab/3d-models/blob/18a3d5aeb34e6983711eb9e9d8e2af18b1abf40e/docs/prints/2026-10-07-sld-1/index.md),
   [D-120](../../working-model/decisions-log.md#d-120--cut-pieces-the-cut-and-the-joins-on-one-plate)).
   0.15 is the middle of what worked, and it still holds on the lower 0.6 mm rail (§2.3), where
   0.20 would lift out. That is a pick between three settings that all printed, not a reading
   that 0.15 is best.
   On split-04's slice it builds on the two hexagons and the two outer pieces. It refuses, by name:
   the star and the middle ("can't take a slide: its face turns inward at (x, y)"), the kite ("too
   narrow for the slide: its face reaches 1.47 mm from the rail's middle line, and the slot needs
   3.00 mm a side, 2.60 mm at its widest and one 0.40 mm line of wall"), a 1.0 mm rail, whose
   1.2 mm slot leaves 0.30 mm of band at its ends, under 0.5, pins and a slide on one piece, and a
   slide with no size on the hold. Without the piece's name it refuses a gap the rail does not
   lock past (0.6 mm rail at 0.20) and a height that is not whole layers.

After all three steps, one plate file and page per the print-coaster-samples and prioritize-prints
skills, with the pieces drawn from the real mesh.

## Yours to do

- Picked: B (D-120). Nothing to do until the plate's page is up; then a yes and a color.
- Optional: the slide gap is 0.15 mm a side, picked by Claude, not by you: sld-1's three gaps
  all worked, so bikar takes the middle one (§5 item 3). Say if one of the other two felt better.
- Optional: hold one split-06 whole piece of each kind back, so plate one has its control in hand.
