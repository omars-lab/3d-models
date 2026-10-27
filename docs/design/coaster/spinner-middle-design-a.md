---
status: draft
date: 2026-10-27
produced-by: researcher A subagent (Claude Opus 5.5), one of two independent passes; web research and two renders of the flange coaster, recorded in docs/research/2026-10-27-spinner-middle-research-a.md
---

# A middle piece that turns: options (researcher A)

> Status: researcher A's pass, one of two independent ones; a checker compares both and writes the
> doc to act on. Nothing here is built or printed. Every source and measurement is in
> [the research file](../../research/2026-10-27-spinner-middle-research-a.md), cited below as S1,
> M1 and so on. No pictures yet: the side and top views this needs are listed in §8 for the
> consolidated doc.

**The ask.** Could the middle piece of the split flange coaster, the 10-pointed star, be printed so
it turns in place, like a fidget spinner set into the coaster?

## 0. The answer in one screen

**Yes, as a dial that turns; not, at this size and thickness, as a free spinner.** Three things
decide it.

1. **The opening has to become round.** A star cannot turn in a star-shaped hole. The frame's
   opening must be a circle at least as big as the star's tips, about 19 mm across (M1). That
   removes the bits of frame that reach in between the star's ten points, a ring from 7.35 to
   9.48 mm out. They move onto the turning disc, so the disc shows the star *and* those ten
   wedges of line. How the disc shows them is a picture call for Omar (§2).
2. **Our coaster already holds pieces the way a turntable holds its platter.** Each loose piece has
   a flange trapped under the frame's lip between the two halves. Make the middle piece's flange
   and the frame's undercut round, and the piece turns on that flange. Nothing new to buy, and the
   height stays 4.4 mm. PLA sliding on PLA is draggy (S26, no figure found), so expect a smooth turn
   that stops when you let go, not seconds of spin.
3. **A real spin needs a steel bearing, and none fits here without changing the coaster.** Every
   thin bearing found is 4 mm tall (S9, S10, S11). Hidden under a 0.6 mm face on each side it needs
   a 5.2 mm coaster, not 4.4. And the small kites' holes sit only 10.7 to 11.65 mm from the centre
   (M2), so a bearing 23 or 27 mm across would cut into them. A printed 608 is 7 mm tall (S12).

| Option | What turns, on what | Pros | Cons | Implications | What it verifies |
|---|---|---|---|---|---|
| **A. Round flange, PLA on PLA** (recommended first) | a round disc on its own flange, under the frame's lip | height and halves unchanged; nothing to buy; built from the loose-piece code we have; the test print is one slice | turns, does not coast (S20 says fully printed spinners lack spin time; a designer's claim, not a measurement); the kites' undercuts must be trimmed near the middle (M2); the disc's face must sit a layer below both faces or it drags on the table | the art call (§2) comes next; a 36° click to bring the pattern back in line is a later add | whether a round piece turns by a fingertip with no rattle, at which gap, on our printer |
| B. Steel balls in a printed groove | the disc on 2 to 2.5 mm steel balls (S13), dropped in when the halves close | smoother than A, likely; the balls go in at assembly, so no pause in a print (S17) | the groove crosses the 2.2 mm cut, so the halves' line-up becomes a bearing part; printed grooves are rough (S8) and balls can work out (S16); groove reaches the kites' undercuts (M2); chrome steel in a wet coaster, rust not covered by any source found | a new groove shape in bikar for four parts; buying and counting balls per coaster | whether printed grooves at our 0.2 mm layers give a better spin than A, and whether balls stay put |
| C. Commercial thin bearing (6704, 20×27×4 mm) | the disc pressed into the bearing's 20 mm hole, the bearing in the frame | a real spin (S18, S19); cheap, about £1 at ten (S10) | needs the coaster 5.2 mm or taller (§3.3); the 27 mm bearing cuts into the ten small kites (M2), so the pattern round the middle changes; metal in a wet coaster | a different-looking, thicker product; a pattern change near the middle; a part to stock | nothing about our geometry until the pattern is redrawn; it is a product change, not a test |

**Recommendation.** Print option A first as one slice of the coaster with three gaps and a stock
slice beside it (§7). It answers the question that decides everything else, whether a round piece
in our flange turns well enough to be worth it, with the parts and printer we have; B is the next
step only if A turns but feels too draggy, and C only if Omar wants a real spinner enough to
change the coaster's thickness and the pattern round the middle.

Not offered: a centre pin (axle). The middle hole goes through both faces, so a pin needs a floor
or a bar across one face, which hides the star on that face. It is set aside here, not ruled out.

## 1. What we have today

- **The coaster.** 112.5 mm across, 4.4 mm tall, cut at 2.2 mm into two halves printed face down.
  Each loose piece is a 0.6 mm face block, a 3.0 mm band that steps out 0.8 mm under the frame's lip,
  and a 0.6 mm face block. Pieces are dropped in when the halves close, so nothing is printed in
  place. split-06 used a piece gap of 0.10 mm per face (small kite 0.12) and `room` 0.2, each piece
  0.2 mm shorter than the coaster ([split-06](../plates/split-06.md),
  [cut-pieces-joins §1](cut-pieces-joins-design.md#1-what-exists)).
- **The middle piece.** Its tips reach 9.48 mm from the centre at the faces and 10.84 mm at the
  band; its notches come in to 7.35 mm (M1). It has room for three 1.2 mm pins joining its two
  halves ([cut-pieces-joins §2.1](cut-pieces-joins-design.md#21-a-pin-in-a-half)).
- **What is round it.** At the faces, about 2 mm of frame before the small kites' holes; at the
  band, the kites' own undercuts reach in to 10.70 mm at the notch angles (M2).
- **The pegs.** split-06's ring of pegs in the star's inner corners (9.6 mm out) was taken out in
  its fourth round; the nearest ring left stands at 14.3 mm with a filled disc round each peg
  ([split-06](../plates/split-06.md)). Neither reaches a round undercut at about 10.4 mm.

## 2. The round opening, and what it does to the picture

To turn, the disc must be round where it meets the frame, at both faces and at the flange. The
frame's opening becomes a circle of about 9.6 mm radius (the tips, 9.48, plus the gap). The frame
inside that circle, ten small wedges between the star's points, goes onto the disc. Seen from
above, the change is a thin round line through the roots of the ten lines that run out from the
star's tips, plus whatever the disc shows in place of the wedges.

Two ways the disc can show it, a picture call for Omar once A turns:

- **Two colors on the disc.** The star in its color, the ten wedges in the frame's color, so at rest
  it looks like today's coaster with one round hairline; turned, the lines break and come back every
  36°. Each disc half then prints two colors on its face, and every swap costs time and waste
  (memory note, Omar 2026-10-04: about 1.6 min a swap, one color a plate; R6 in the research file).
- **One color, the star drawn by a groove.** The disc in the star's color, the star's outline cut
  as a shallow line. One color per part, as today, but the middle reads as a round disc, not a star.

A third, keeping today's star loose inside a round ring of frame color that turns, does not fit:
the ring would need its own flange outside 9.6 mm, and the kites' undercuts start at 10.7 (M2).

## 3. The options in detail

### 3.1 A. Round flange, PLA on PLA

**Shape.** The disc's faces are circles of about 9.45 mm radius (the frame's 9.6 less the gap); its
band a circle stepped out under the lip. The frame's undercut round the middle becomes a matching
round groove. Two things differ from a loose piece today:

- **The kites' undercuts must give way near the middle.** With today's 0.8 mm flange the round
  undercut reaches about 10.4 mm and leaves 0.3 mm of wall before the kites' undercuts at 10.70 mm
  (M2), less than the one 0.4 mm line bikar takes as its least wall. Either the kites' undercuts are
  filled where they come near the middle, and the kites' flanges notched to match, as `stud_boss`
  already does round a peg; or the disc's flange is narrower, about 0.3 to 0.4 mm, which holds it by
  less. The first keeps the disc held as well as every other piece and is the one proposed.
- **Both faces sit a layer in.** A piece today rests on its flange with its bottom face level with
  the coaster's bottom (0.6 mm face block through a 0.6 mm lip). A disc like that would rub the table
  and the mug. Make each face block one 0.2 mm layer thinner, so the disc stands 0.2 mm in from both
  faces and only the frame touches the table and the mug.

**The gaps.** Two, and they do different jobs. The *side* gap, between the disc's edge and the
frame, decides whether it turns or binds. The *up-and-down* gap, the disc's height against the
undercut's (`room`), decides whether it rattles and tips. Omar did not take a pin that "shakes a
bit" (split-05, R5), so rattle is a failure, not a trade.

**Default:** side gap 0.15 mm per face, the sliding step of CAL-FIT-01. The bounds come from two
sides. Our own piece gap of 0.10 mm drops in but was never asked to turn
([split-06](../plates/split-06.md)). The print-in-place tests on our nearest setup moved at 0.15
(X1 Carbon, PLA, 0.4 mm, 0.2 mm layers, S1) and turned freely at 0.20 to 0.25 (A1, PLA, S2); those
parts were printed touching and had to break apart, ours are not, so for us they are an upper
bound, not a target. This transfers because the nozzle, layers and material match; it does not
transfer as is because a dropped-in disc has two printed walls each with its own error, and a
circle prints differently from a polygon's straight sides (CAL-HOL-01, the printer shrinking a
hole, is the open bet that covers that). The test in §7 reads it.

**Default:** up-and-down gap 0.2 mm, today's `room`, kept as is; the same `room` already closes the
halves on each other and not on a piece ([cut-pieces-joins §1](cut-pieces-joins-design.md#1-what-exists)),
and the CAL-FIT-01 bet covers it until the test reads rattle at it. A whole 0.2 mm layer is the
smallest step the slicer can make, so the next rung down is 0, which would jam.

**What it will feel like.** No source found gives how long a PLA disc turning on PLA keeps going
(S26). The only spin-time statement found, a designer's, says even a printed spinner with a steel
608 bearing gives "several seconds" (S20). Expect a dial: it turns as far as you push it and stops.
Turning a flat disc that sits 0.2 mm in may need a fingertip grip; a few shallow dimples on its face
would give one, and are a later add.

### 3.2 B. Steel balls in a printed groove

A ring of 2 to 2.5 mm steel balls (S13) between the disc's band and the frame, each in a groove
half in the disc and half in the frame. In the 3.0 mm band a 2 mm ball, centred on the 2.2 mm cut,
spans 1.2 to 3.2 mm up and leaves 0.6 mm of band above and below. The groove crosses the cut, so
each of the four parts (two frame halves, two disc halves) carries a quarter-round groove, and how
well the frame halves line up (their pegs, at a 0.25 mm gap in split-06) becomes how round the
race is. The balls go in by hand when the halves close, as the pieces do, so no pause in a print is
needed (S17, which is for a part a single print must enclose).

What stands against it: print-in-place bearing makers ran about 0.2 mm between ball and groove and
say printed grooves will not match steel for friction (S7, S8, both at layers or printers not
matching ours, S7 at 0.12 mm layers); a 6 mm-ball printed race came out too loose and the balls
worked out (S16). Radially the groove, centred about 10 mm out, reaches 11 mm or more, past where
the kites' undercuts start (M2). And a coaster gets wet: none of the sources found say whether
chrome steel balls rust in it.

### 3.3 C. A commercial thin bearing

The thin bearings found are all 4 mm tall: 6700 is 10 × 15 × 4 mm (S9), 6704 is 20 × 27 × 4 mm
(S10), and the listings put 6701 to 6705 in between (S11, marketplace figures). The arithmetic:

- **Height.** Hidden behind a 0.6 mm face on each side, a 4 mm bearing needs 0.6 + 4.0 + 0.6 =
  5.2 mm. The coaster is 4.4. bikar's `height` goes to 6 (R4), so a 5.2 mm coaster can be built,
  but every piece and the whole coaster grow 0.8 mm thicker. At 4.4 the bearing shows on a face.
- **Which one.** The middle hole goes through both faces, so the bearing's inner ring must turn
  with the disc and its outer ring sit in the frame. The 6704's 20 mm hole just takes a disc 19 mm
  across at its tips (M1). The 6700 to 6702 are too small for that, their outer ring would sit inside
  the star. The 6703's 17 mm hole is smaller than the disc.
- **Room.** The 6704's 27 mm outside means a pocket out to about 13.6 mm from the centre. The
  small kites' holes start at 11.65 mm and their undercuts at 10.70 (M2). The ten kites round the
  middle would be cut, so the pattern changes there.

That makes C a different product, thicker and with a redrawn middle, not a change to this one.
What it would give: the "decent spin" of a steel bearing (S19) and a real fidget feel. What it
costs in money is small, under £2 a bearing (S10).

## 4. Living with a mug

- **Sits flat, no wobble.** The disc stands 0.2 mm in from both faces (§3.1), so the coaster rests on
  its frame only and the mug never stands on the disc. A disc that pokes out by a layer would rock.
- **Wet.** Water will get into a round hairline the way it gets into every piece's gap today. For A
  that is PLA in water, as now. For B and C it is steel in water; none of the sources found speak to
  rust, so a stainless ball or a sealed bearing (a 6700-2RS was listed sealed both sides, S11) is
  the cautious pick if either is tried.
- **Heat.** PLA softens from about 60 °C by hobby sources (S24), and holds a steady load poorly over
  time (S25). A flat disc held round its edge carries no mug's weight in A, so this is no worse than
  today's pieces; it does mean no dishwasher, as for the whole coaster.
- **Cleaning.** A rinse and a shake. The disc cannot be taken out without opening the halves, as
  with every piece now.
- **Spin against rattle.** One gap sets each: the side gap for a free turn, `room` for rattle. The
  test in §7 reads both at once, by turning and by shaking.

## 5. What bikar would need

For A, in the flange coaster's split code and the `.bkr`:

1. **A round piece for one ring of pieces.** A word on the `loose` line, say `spin`, that replaces
   that ring's piece and opening by circles: the opening at the faces as the circle round the piece's
   tips plus the gap; the undercut as that circle plus the flange. Refused for any ring whose pieces
   are not centred on the coaster's centre, which leaves only the middle (orbit 0) here.
2. **Fill the neighbours' undercuts that come too close.** Where another ring's undercut comes
   within the wall (`stud_wall`) of the round undercut, fill it and notch that ring's flange to
   match, as `stud_boss` does round a peg. Refuse, by name and with the room it found, when the
   faces themselves come too close.
3. **Faces set in.** A knob for how far the turning piece's faces stand in from the coaster's faces,
   in whole layers, default 0.2 mm when `spin` is on.
4. **Pegs kept out of the round groove.** Refuse a peg, or its filled disc, that cuts into the round
   undercut.
5. **The disc's own halves.** The disc is cut and pinned like any piece, three 1.2 mm pins
   (cut-pieces-joins §2.1); the pins must stay inside the disc's face circle.
6. **The test slice.** `wedge_center 1` must keep the round middle and its round opening in a wedge
   (R4); check it on the render.
7. **Art (after §2's call).** Two colors on the disc need the disc's face drawn as two regions; one
   color with a groove needs an engraved line on a piece face, which the loose-piece code does not do
   today.

For B, add a groove shape cut into four parts and a ball count; for C, a bearing pocket and a press
fit hub, and a redrawn middle. Neither is worth building before A's test reads.

## 6. Checks

**Validator (the turn, by hand, per gap):** close each slice with its disc in, set it flat on a
table, and turn the disc with one fingertip; then shake the closed slice beside an ear.
PASS: the disc makes a whole turn under one fingertip without the slice moving on the table, and
shaking it gives no click or rattle you can hear.
FAIL: the disc binds anywhere in the turn (the elephant's-foot flare or the seam on a circle is the
likely spot, so turn it a full turn, not a quarter), or the slice slides along with it, or it
rattles when shaken, or a face of the disc stands proud of the frame's face. The hard case is the
tightest gap that passes: a gap wide enough to turn that also rattles is a FAIL, not a pass with a
note.

**Validator (no drag on the table):** lay the closed slice disc-side down and turn it.
PASS: the disc turns as freely as face up.
FAIL: it turns more stiffly face down, which means the disc's face touches the table.

## 7. The smallest test print

**One repeat, several settings, a stock control beside it.** bikar's
`wedge 36 wedge_from 9 wedge_center 1` prints a 36° slice of both frame halves with the middle piece and its opening (R4).
On one bed:

| Slice | Middle | Side gap per face | What it shows |
|---|---|---|---|
| 1 | round disc (option A) | 0.10 | today's piece gap, asked to turn |
| 2 | round disc | 0.15 | the default bet |
| 3 | round disc | 0.20 | the print-in-place figure (S2), the loose end |
| 4 | today's star (stock) | 0.10 | the same slice as split-06 would print it, so the round slices are judged against a known one |

All four at `room` 0.2, the disc's faces 0.2 mm in, its halves pinned with three 1.2 mm pins at
0.25 mm, one color. Each disc carries its carved id. Whether four slices with their halves and
discs fit one bed is for the plate page to check; if not, drop slice 1. The stock slice also shows
whether trimming the kites' undercuts near the middle (§5 step 2) changed how the kites sit, by
comparison.

What it reads: the side gap at which a round piece turns cleanly on this printer; whether `room` 0.2
rattles a turning piece; whether a face-set-in disc drags. It does not read spin time with a flick,
since none is expected; count turns per flick anyway as the baseline B would have to beat.

## 8. Open, and for the consolidated doc

- Pictures this doc should open on: a top view of the middle as today and with the round opening
  (both §2 art choices), and a side view of the disc in its round undercut with the faces set in
  (`draw-side-view`).
- M1 and M2 are one render of a 2026-10-06 checkout; re-measure on bikar main when step 1 is built.
- No PLA-on-PLA friction figure and no spin time for a printed plain bearing were found (S26); the
  test is the measurement.
- The turning coasters found (S21 to S23) were seen only as search summaries; none is a split
  coaster with loose pieces. That is "none of the three found", not "none exists".
