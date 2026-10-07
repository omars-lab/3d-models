---
status: draft
date: 2026-10-05
produced-by: Claude (Opus 5.5), from a read of this repo at origin/master b74d88f and of the research already checked in (split-with-studs-research.md, w2-connector-coupon-survey.md, hemisphere-split-survey.md); no new web research
---

# Joining the two halves of a piece: slide, clip or screw

> Status: draft 2026-10-05. It informs calls 10 and 11 on the
> [2026-10-05 open calls page](../../working-model/feedback-requests/2026-10-05-open-calls.md#10-split-the-pieces-too-start-with-way-a-or-go-straight-to-way-c)
> and decides neither. Asked by Omar on 2026-10-05, of the cut pieces in the
> [finish techniques brainstorm](../printing/finish-techniques-brainstorm.md#11-five-ways):
> "Only one of the faces will be glossay here, and I want the coaster to be flat ... leaning
> towards c", then "can two pieces sldie into each other / clip or be screwed onto each other?"
> Before that, of way c: "how do connect the infill pieces ao they feel like one post print"
> ([§1.4](../printing/finish-techniques-brainstorm.md#14-way-c-making-the-two-piece-halves-feel-like-one)).

**In short.** A slide works: a small dovetail across the cut faces joins two loose piece halves
into one piece before it goes into the coaster. That suits ways a, b and d, where the halves are
loose. It does not suit way c, because there each half is held in its own pocket and the two
halves can only meet straight down. A clip does not fit on a piece half: at 1.6 mm, the stud
would be under a millimetre tall, too short to bend and click back. It could go on the coaster
halves' own studs, so it is tried there. A screw does not work for the pieces at all. A thread
closes by turning, and a kite, a hexagon or a star cannot turn in a hole of its own shape.

For way c, Omar's lean, the useful finding is that joining the two piece halves would not stop
what can be felt. The pair can still shift as one by the pocket's air gap. So in way c nothing
joins the piece halves. The pockets hold each pair, and the coaster halves join once, at their
own studs. That is one join a coaster instead of 31.

![Four drawings. 1: two loose piece halves, a dovetail rail on one and a slot in the other, sliding together sideways. 2: a stud with a bulge pushed into a socket; on a 1.6 mm piece half it is under a millimetre tall. 3: from above, a kite in its kite-shaped hole, with a curved arrow and a red cross: it cannot turn. 4: a strip of coaster cut through, a pocketed pair of piece halves in the middle and the coaster's studs in the straps on both sides.](join-halves-media/joins.png)

Drawn from [joins.html](join-halves-media/joins.html), rendered headless, not to scale.

## 1. Two places a join can go

A split coaster has two kinds of halves:

- **The coaster halves.** Each is 2.2 mm thick on gBV at 1.25× (112.5 mm across, 4.4 mm tall,
  3.75 mm straps). The split design already joins them with 2.0 mm studs, 1.4 mm tall, in sockets
  1.6 mm deep, at the 56 spots where straps cross
  ([split §4.1](split-with-studs-design.md#41-the-stud-and-socket)).
- **The piece halves.** gBV's pieces are 3.2 mm tall, so a cut piece leaves two 1.6 mm halves,
  eight 0.2 mm layers each. There are 31 pieces, so 62 halves.

How a piece half is held depends on the way picked in the brainstorm's
[table of ways](../printing/finish-techniques-brainstorm.md#11-five-ways):

| Way | Are the piece halves loose? | What would a join between them do? |
|---|---|---|
| a. Lip + cut piece | Yes, placed by hand | Halve the parts to place (31, not 62). The lips already trap both halves once the coaster closes. |
| b. Flange + cut piece | Yes, placed by hand | The same as a. |
| c. Flange, printed in place | No: each half prints inside its coaster half, in a pocket | Very little (§5). |
| d. Pegged halves | Yes, in a one-piece coaster | The join is the only thing holding the halves together. |

## 2. Slide: a dovetail across the cut

**How it works.** One half grows a rail on its cut face, wider at its top than at its root. The
other half has a slot of the same shape. Push the rail into the slot from one side, and the two
halves can no longer pull apart, only slide back out the way they went in. Both halves still print
with their outside face on the bed, so both faces are first layers.

**Sizes.** A half is 1.6 mm. The rail is 0.8 mm tall, four layers, and 4 mm wide at its root.
The slot is one layer deeper than the rail, 1.0 mm, so the rail's top never touches its floor and
the two cut faces close flat. That leaves 0.6 mm of floor under the slot, three layers, the floor
the kernel already keeps under a debossed pocket (CAL-CST-03). The floor rule transfers because it
is the same kind of thing printed the same way: a thin slab, face down, under a cut that opens at
the top. These are starting sizes for a coupon, not measured ones.

**Slope.** BOSL2's `dovetail()` uses woodworking slopes of 4, 6 or 8, default 6, and says "Adding a
chamfer helps printed parts fit together without problems at the corners"
([research S38](../../research/split-with-studs-research.md#q11-alternatives-dovetails-rails-jigsaws-snap-pins)).
That default does not transfer to a rail this short. A dovetail holds only if the rail's top is
wider than the slot's mouth. Built in 0.2 mm layers, a rail of height h at slope s is wider at its
top than at its root by (h − 0.2) / s a side. At slope 6 and 0.8 mm that is 0.1 mm, which is no
more than any clearance SLD-1 tries, so the rail would lift straight out. At slope 2 it is 0.3 mm,
which beats the widest gap, 0.20, by 0.1 mm a side. The coupon uses slope 2, so each layer is
0.1 mm a side wider than the one under it; the kernel refuses a dovetail that does not lock.

**The fit.** The only dovetail clearance with a print behind it here is bikar's 0.15 mm per face.
minis-03 printed it, and it came out "a bit loose"
([print quality A §4.3](../printing/print-quality-a-design.md#43-dsl-knob-changes-bikar-parameters), CAL-FIT-01).
That value does not transfer as it is. It was set for a dovetail cut across the coaster's outline,
where the slanted sides are walls the nozzle traces. Here the dovetail stands on the cut face, so
its slanted sides are built as steps, one 0.2 mm layer at a time, and the rail's top hangs out a
little past its root, with the slot's mouth doing the same. A stepped side fits differently from a
traced one, which is why the coupon tries three clearances, not one.

**Where it suits.** Ways a, b and d. In a and b it turns two loose halves into one piece before
it goes in, so placing the pieces is the same job as today. In d it is the whole join. It does not
suit c (§5).

**What it costs.** One rail and one slot per piece, sized per shape. A kite is narrow near its
tips, so its rail would be short or would run along its long axis only. The rail must run along a
line that both halves of the shape share when the upper half is turned over, not mirrored
([brainstorm §1.2](../printing/finish-techniques-brainstorm.md#12-true-of-every-way)).

**The coupon, SLD-1.** Three pairs of 1.6 mm hexagon halves, printed face down, with a
0.8 mm rail and a 1.0 mm slot at 0.10, 0.15 and 0.20 mm per face, and the clearance debossed on the
cut face. Add one kite pair at the clearance that reads best, to see if a short rail holds at all.
Omar picked the dovetail to try first (D-107). The coupon is bikar's
`patterns/Coupons/Dovetail-Coupon.bkr`; its plate is [sld-1](../plates/sld-1.md). The hexagon is
regular, about the area of gBV's hexagon at 1.25×; it stands in for gBV's elongated hexagon by
area, not by shape.

**Printed 2026-10-07.** Omar: "alos 10, 15, and 20 all worked ..." ([the record](../../prints/2026-10-07-sld-1/index.md)).
He did not say which one felt best, or whether each held when shaken,
so the kite pair still waits on that.

**Validator:** for each pair, slide it together by hand, hold it cut face down by one half and
shake it.
PASS: it slides together without a tool, the other half stays on when shaken, and both faces
sit level when the pair lies on a table.
FAIL: it needs a tool or a hard push, the rail breaks off, or the halves part when shaken. A pair
that holds but leaves one face standing proud also fails: the coaster has to sit flat.

## 3. Clip: a stud with a bulge

**How it works.** A stud with a small bulge near its tip is pushed into a socket. The bulge
squeezes in, then springs back past a lip, and the two parts hold without glue. The slicer cut
tools ship this as their Snap connector. In PrusaSlicer and Orca the bulge is 0.15 and the room
around it 0.3 of the connector's size, read from their source code as ratios
([research S1](../../research/split-with-studs-research.md#q1-prusaslicer-cut-tool-connectors)),
so a 2 mm stud gets a 0.3 mm bulge
([split §4.2](split-with-studs-design.md#42-the-other-joints-considered)). Nothing here has printed
one.

**Not on a piece half.** A 1.6 mm half leaves room for a stud under 1 mm tall. A snap works by
bending, and a stud that short has no length to bend; the split design already found the same for
a 1.4 mm stud ([split §4.2](split-with-studs-design.md#42-the-other-joints-considered)).

**On the coaster halves: worth one coupon row.** Their 2.0 mm studs could take a bulge. What a
snap would buy is a hold that does not loosen: a PLA press fit "relaxes over months" under steady
stress (Creative3DP,
[research §3](../../research/split-with-studs-research.md#q6-pin-and-dowel-clearance-press-slip-loose)),
while a snap sits unstressed once it has clicked. The fit classes the research gathered agree on
needing more room for a snap: Sovol gives press 0.05–0.15, sliding 0.2–0.3 and snap 0.3 mm or
more; Prusa says "at least 0.3 mm" for parts that "lock/snap together"
([research §3](../../research/split-with-studs-research.md#q6-pin-and-dowel-clearance-press-slip-loose)).

Two warnings, both from sources and neither tested here. A snap arm should never bend across the
layer lines, and PLA is a poor snap material next to PETG (Hubs and Formlabs, both vendors,
[W2 survey §1](../../research/w2-connector-coupon-survey.md#1-cantilever-snap-fit-engineering-numbers)).
A stud standing up from the cut face bends across its layers, which is why BOSL2 prints its
`snap_pin()` lying down
([research S38](../../research/split-with-studs-research.md#q11-alternatives-dovetails-rails-jigsaws-snap-pins)).
So a snap stud on the coaster halves may break rather than click. The coupon row is how to find
out. It is not a recommendation.

**The coupon: two rows added to SPL-1.** Next to the press-fit pairs in
[split §9](split-with-studs-design.md#9-the-coupon-spl-1): three pairs of 2.0 mm studs with a
0.3 mm bulge, at 0.3, 0.4 and 0.5 mm of room, and one pair at 3.0 mm with a 0.45 mm bulge, in case
the 2 mm ones break.

**Validator:** press each pair together, pull it apart, and do that five times.
PASS: it clicks in by hand, does not come apart when shaken, and comes apart by hand without
breaking, all five times.
FAIL: the stud breaks or cracks, it never clicks (no hold beyond friction), or it needs a tool to
part.

## 4. Screw: the piece has to turn

**A printed thread on a piece.** A thread closes by turning one part a full turn or more in the
other. A kite, a hexagon or a star cannot turn in a hole of its own shape, so its two halves cannot
be screwed together inside the coaster. Outside the coaster, they could only be screwed together
if the joining part were round and hidden inside the piece, a round plug on one half in a round
threaded hole in the other. At 1.6 mm a half, that thread would be one or two turns long at most.
No source on printed threads this small is in this repo's research, so pitch and clearance would
be guesses.

**A bought screw through the coaster.** The smallest screw surveyed here, a #6 pan head, has a
head 6.86 mm across and 2.08 mm tall and a thread 3.51 mm across
([W2 survey §3](../../research/w2-connector-coupon-survey.md#3-keyhole-slot-dimensions-and-face-down-printing),
ASME B18.6.3 via Engineers Edge and AFT). The head is wider than a 3.75 mm strap and would sit on a
face meant to be a first layer. Smaller screws were not surveyed, so this rules out #6, not every
screw.

**The coupon, if one is wanted: SCR-1.** A round 10 mm test piece cut in two, a plug with a thread
on one half and a threaded hole in the other, at two pitches. My advice is not to print it. Even if
it held, no piece shape could use it except a round one hidden inside a piece, and gBV has no
round pieces.

## 5. What this means for way c

In way c each piece half prints inside its own coaster half, in a pocket: a narrow neck at the face
and another at the cut, with the piece's band in a closed room between them and one layer of air
(0.2 mm) above and below it
([brainstorm §1.4](../printing/finish-techniques-brainstorm.md#14-way-c-making-the-two-piece-halves-feel-like-one)).
Closing the coaster brings each half straight down onto its partner. Nothing can slide sideways,
so a dovetail cannot engage, and a peg or a clip would have to press home along the same line the
coaster closes on, at all 31 pieces at once.

More to the point, a join between the two piece halves does not stop the movement Omar would feel.
Closed, the two halves of a piece press face to face at the cut. Lifted, the pair can move as one by
the air gap, about 0.2 mm, toward one face. A join keeps the two halves together; it does not stop
the pair moving. Only glue to the coaster, or pieces tall enough to press hard on their necks,
stops that, and both have costs the brainstorm already lists. Unjoined, each half could also drift
outward by up to its own gap. This comes from reading the drawing, not a print, and the pocket
coupon in §1.4 is what would show whether either movement can be felt.

So for way c: **the pockets hold the 31 pairs, and the coaster halves join once, at their own
studs**, by press fit, a snap (§3) or glue. Which one is the split design's call 3, call 7 on the
open calls page. That is one join a coaster, not 31.

## 6. Side by side

| Join | Pros | Cons | What it leads to |
|---|---|---|---|
| **Nothing between the piece halves in way c; the coaster halves join at their studs** (my pick, if c) | No extra part, no glue on the pieces, every piece comes apart again; one join per coaster | The pair can still move by the air gap, as with any join between the halves | The pocket coupon of §1.4 decides if the movement matters; call 7 decides how the coaster halves hold |
| **Slide (SLD-1)**, if a, b or d | Two halves become one part before placing, so 31 parts to place, not 62; no glue; comes apart again | A rail and slot sized per shape; the kite's rail is short; the fit has no print behind it at this size | A per-shape knob in bikar, and a three-clearance coupon first |
| **Snap rows on SPL-1**, for the coaster halves | A hold that does not loosen over months, with no glue | A stud that stands up bends across its layers, and sources call PLA a poor snap material: it may break | Two extra rows on a coupon already planned; if they break, press fit or glue (call 7) |
| **Screw (SCR-1)** | Strong and can come apart | No piece shape can turn in its hole; a #6 head is wider than a strap and shows on a face | Nothing, unless a round hidden plug is wanted; not recommended |

**My pick.** If way c: no join between the piece halves, as §1.4 already picked, and the snap rows
added to SPL-1 so call 7 has a third option with a print behind it. If way a or b: SLD-1, because
halving the parts to place is the cost the brainstorm named against way a. The screw is out.

## 7. How this feeds calls 10 and 11

- **Call 10 (a first, or straight to c).** It removes one of way a's costs, twice the parts to place,
  if SLD-1 holds. It adds no cost to c.
- **Call 11 (if c, how the halves become one).** It supports the pocket with nothing extra. The
  peg-and-socket row on that call is the same kind of join as the clip here, and it meets the same
  limit: a piece half too thin for it to bend, and nothing it would add that the pocket does not.

Neither call is decided here.

## Yours to do

- Calls 10 and 11 on the [open calls page](../../working-model/feedback-requests/2026-10-05-open-calls.md#11-if-way-c-how-the-two-piece-halves-become-one), when you are ready; this note is the
  joining answer they waited on.
- Nothing here prints without your yes. I have assumed the snap rows go onto SPL-1 when it is
  built, since they cost two rows on a coupon already planned; say if you would rather leave them
  off.
