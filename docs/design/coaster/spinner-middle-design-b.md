---
status: draft
date: 2026-10-27
produced-by: researcher B subagent (Claude Opus 5.5), from web research recorded in docs/research/2026-10-27-spinner-middle-research-b.md and a read of this repo and bikar origin/main; written independently of researcher A, for a checker to compare
---

# A middle piece that spins (design B)

> Draft, 2026-10-27. One of two independent designs for the same question; a checker compares
> them and writes the consolidated spinner-middle design, the one to act on. Raw findings and sources:
> [2026-10-27-spinner-middle-research-b](../../research/2026-10-27-spinner-middle-research-b.md).

**In short.** A ten-pointed star cannot turn inside a star-shaped hole, so a spinning middle means
the boundary between the turning part and the frame has to be a circle at every height, faces
included. That costs the pattern something wherever the circle runs: either the middle becomes a
round disc, or a thin round seam crosses the straps round the star. The 4.4 mm height rules out
every bought bearing checked here, so the turning surface is printed PLA on printed PLA, the same
flange-under-a-lip the pieces are held by today, made round. Steel balls are a possible later
step, and they need no paused print: they drop in when the halves go together. Expect the middle
to **turn** when pushed, not to spin on its own for seconds like a hand spinner. It is small and
light, and nothing found here says otherwise. The smallest test is a palm-sized round coupon at
three gaps, beside a stock middle piece.

## 1. What decides it: the height and the star

- **Height.** The closed coaster is 4.4 mm, cut into two 2.2 mm halves. The lip over each piece's
  flange is about 0.6 mm thick and the undercut about 3.2 mm tall
  ([research §1, R3](../../research/2026-10-27-spinner-middle-research-b.md#1-our-own-facts-repo-reads)).
- **The star's size.** At the face, the middle piece is 18.0 × 19.0 mm across; the largest circle
  inside it has a radius of 7.27 mm; its points reach roughly 9.5 mm from the centre. At the
  flange it is 20.6 × 21.7 mm
  ([cut-pieces-joins §2](cut-pieces-joins-design.md#2-the-room-in-each-piece)). These come
  from that doc's measurement of 2026-10-24, not a fresh render: the local bikar build was too old
  to read today's coaster file.
- **The straps round it** reach out to about 13 mm, where split-10 puts a ring of ten pegs
  ([split-10.yaml](../plates/split-10.yaml)).

So any turning part is at least a circle of about 9.5 mm radius at the face (just clearing the
star's points), and the frame must give up the ten V-shaped bits of strap between the points, or
carry them on the turning part.

## 2. The options

Three ways to make it turn, and one that does not fit. Each says what it changes in the look, and
what a print of it would and would not prove.

| | A. Round disc | B. Turning ring round today's star | C. B (or A) plus steel balls |
|---|---|---|---|
| **What turns** | One round disc, about 19 mm across, with the star drawn on it as a shallow groove | A round frame-colored ring carrying the ten V-straps, with today's star piece captive inside it as now | As B, rolling on 2 mm stainless balls in a groove, as many as the groove holds |
| **Pros** | Fewest parts; the simplest new geometry; the disc's flange is a plain round ring | Looks exactly like today when lined up; the star keeps its own color; ten small clicks can bring it back into line every 36° | Longest spin of the three; the balls go in at assembly, no paused print (research §5) |
| **Cons** | The star is no longer its own colored piece: one color, the star only a line, unless printed in two colors (a color swap per plate costs time and filament) | Four more halves to print and join; the ring is narrow at the star's points (about 1.3 mm at the face if the seam sits at 10.8 mm); a thin round seam shows across the straps | Needs a groove about 2.4 mm wide, three times today's 0.8 mm undercut, which eats into the straps and maybe the kite holes; balls are bought parts; water reaches them, and 440C stainless "may corrode" (research S17) |
| **Implications** | Commits the middle of every spinner coaster to a disc; the pattern's centre reads differently; no new pieces | Needs a measured render first: if no circle stays inside the straps all the way round, the seam crosses the kite holes and the kites must be cut too, which makes B much bigger | A bought-parts line for every coaster; a ball count and size to stock; only worth it if A or B turns too briefly to enjoy |
| **What a print verifies** | The turning fit and rattle of a round flange; says nothing about how B looks | The fit and the look, and whether the narrow ring survives being pushed | Whether rolling beats sliding at this size, and by how much |

**Not an option at 4.4 mm: a bought bearing.** The thinnest checked are 4 mm (a 6700ZZ, 10 × 15 ×
4, and a needle thrust cage with two washers, 10 × 24 × 4). Either leaves 0.2 mm, one layer, for
both faces together, and the thrust bearing is wider than the middle piece
([research §4](../../research/2026-10-27-spinner-middle-research-b.md#4-bought-bearings-and-balls-and-whether-they-fit-in-44-mm)).
That is true of the four bearings checked, not of every bearing made. A 6700ZZ would fit a coaster
about 5.5 to 6 mm tall (the `height` setting goes to 6), which changes the feel of every coaster
we have printed.

## 3. The fit that lets it turn

The number that matters is the gap between the round flange and its round undercut, per face. No
source found measures it for our case: two PLA parts **printed apart** and put together, on a
Bambu, turning.

- **What the web gives is print-in-place**, where the two parts print already together and the
  risk is that they fuse. The nearest to us is a Bambu X1 Carbon, 0.4 mm nozzle, 0.2 mm layers,
  PLA, where joints "were moveable at 0,15" mm, not saying per side or across
  ([Fab Academy Ísafjörður](https://fabacademy.org/2025/labs/isafjordur/group_assignments/group_week05/)).
  A 2026 guide recommends 0.25 to 0.3 mm for PLA at a 0.4 mm nozzle, minimum 0.15, also not
  saying per side ([uavmodel guide](https://blog.uavmodel.com/?p=4008)).
- **This transfers only as an upper bound.** A gap that keeps two printed-in-place parts from
  fusing is wider than one two separate parts need to turn, because separate parts cannot fuse.
  What a separate part fights instead is the first-layer flare on its bottom edge, the layer
  ridges of two upright walls rubbing, and the round hole printing smaller than drawn (the
  hole-shrink bet CAL-HOL-01, unmeasured). The X1 Carbon is not the X2D; the condition for that
  number to carry over is the same nozzle, layer and filament with similar flow, which holds,
  and the same process, which does not.
- **Our own fit** for a loose piece that is dropped in and left still is 0.10 to 0.12 mm per face
  (split-07, split-10). Whether that holds for a part that turns is what the test measures; the
  loose-piece bet CAL-LSE-01 is still open
  ([loose-pieces §3.4](loose-pieces-design.md#34-which-fit-numbers-transfer-and-on-what-condition)).

**Default:** the turning gap starts at 0.15 mm per face, with 0.10 and 0.20 beside it. This is a
starting ladder, not a result: 0.15 is where a Bambu with PLA moved in print-in-place joints
([Fab Academy Ísafjörður](https://fabacademy.org/2025/labs/isafjordur/group_assignments/group_week05/)),
0.10 is our stationary fit, and 0.20 is inside the print-in-place range
([uavmodel guide](https://blog.uavmodel.com/?p=4008)). The coupon in §6 settles it.

**Rattle is the other side of the same gap.** Today each piece is 0.2 mm shorter than the space
between the halves (`room 0.2`), which is up-and-down play. A turning part with that play will
click against the lips when the coaster moves. The coupon tests two heights of play.

## 4. Living as a coaster

- **A wet mug.** Water will wick into a round gap. Plain PLA on PLA has nothing to rust and can be
  rinsed. Steel balls (option C) bring rust: chrome steel rusts; 440C stainless resists but the
  maker says it "may corrode depending on the environments and conditions"
  ([SCA Shinyei](https://sca-shinyei.com/ballbearing/bearing_aisi440c)).
- **Sits flat, mug does not wobble.** A flush turning middle carries part of the mug and could
  turn the mug. Setting it one 0.2 mm layer lower keeps the mug on the frame; bikar already sets a
  loose piece's height ([loose-pieces §3.2](loose-pieces-design.md#32-the-fit-and-whether-the-piece-sits-flush-proud-or-recessed)).
  The cost is a slightly sunken centre.
- **Cleaning.** A captive part with a 0.1 to 0.2 mm gap holds grime that only comes out by
  separating the halves, which the pegs make hard on purpose.
- **Spin.** No friction number for PLA on PLA was found, so spin time is not estimated. Without
  one: a flat disc's resistance to slowing down grows with the fourth power of its radius, so a
  middle about 21 mm across has very little, and hand spinners get theirs from steel weights far
  out (research §6, §7). Expect a push-and-turn, not a flick-and-watch. A bigger turning part
  (more of the rosette) would spin far longer, and is a much larger change to the pattern.
- **The flange already prints poorly on the middle.** split-07's middle had a "webbed" feel at its
  flange step, which split-10 is testing supports and a slope for
  ([split-10 page](../plates/split-10.md)). A round flange has the same step over air, so
  whatever split-10 finds applies here.

## 5. What bikar would need

None of this exists today; each item is new geometry in the split kernel, which owns the hole, the
undercut and the halves.

1. **A round hole and undercut for one orbit.** A setting on `loose` (a working name: `turn`)
   that, for the chosen ring of pieces, replaces the hole at both faces and the undercut with
   circles: the face circle at the piece's farthest point plus a wall, the undercut circle that
   plus the flange. It must refuse by name when the circle crosses another hole, rather than cut
   through a kite silently.
2. **The turning part.** For option A, the piece's outline becomes the circle, with the star cut
   as a shallow groove on both faces. For option B, a new ring body: the circle less today's star
   hole, cut into halves and pinned like any loose piece, with today's star piece loose inside it.
   The ring's narrowest point at a star tip must meet the printable-wall floor or be refused.
3. **Clicks (option B).** Ten small bumps on the ring's flange and ten dimples in the undercut
   floor, one per 36°, so it stops lined up. Snippet sources only (a 36-click rotary fidget, and
   notes that PLA springs deform under sustained load); untested here.
4. **The pegs round the middle.** split-10's ring of ten pegs at 13.0 mm leaves, on paper, about
   11.7 mm before a peg's wall begins; a round undercut out to about 11.6 mm just clears it. That
   margin is arithmetic from the stated sizes, not a render, and is the first thing the render in
   item 1 should check.
5. **A ball groove (option C).** A round channel in the lower half's undercut floor and the ring's
   flange, sized to a stocked ball, with the count as a setting.

## 6. The smallest test

One repeat of the shape, several settings on one bed, a stock control beside it. The test asks
the bearing question only (does a round flange turn without rattling, at which gap); the look
question waits for the render in §5 item 1.

- **The coupons.** A round frame coupon about 32 mm across and 4.4 mm tall, cut into two halves,
  with a round hole of about 9.7 mm radius and lips and an undercut matching the coaster's (about
  0.6 mm lips by the coaster file's own comment, to be read off a render before the coupon is drawn);
  and a round turning disc in two halves, pinned as today's middle is. bikar cannot draw this yet,
  so it is a short OpenSCAD file in this repo, which keeps the test from waiting on §5.
- **The ladder.** Gaps 0.10, 0.15 and 0.20 mm per face, two of each so one bad piece does not
  decide it: six coupons. At 0.15, one more pair with no up-and-down play (`room` 0) beside the
  stock 0.2, to separate rattle from turning: eight coupons in all.
- **The control.** The stock middle piece in its stock opening, printed the same day: the coaster
  file at `wedge 36` with `wedge_center 1` gives exactly that, as split-04 did. It cannot turn; it
  is there so the same-day fit and rattle of today's piece sit beside the new ones.
- **Then.** Rinse each under the tap, dry, and turn again.

**Validator:** each coupon is judged by hand, closed, the frame held flat on the table.
PASS: a finger push turns the disc a full turn without catching, it does not click when the
coupon is shaken gently, and it still turns after a rinse and dry.
FAIL: the disc binds at any point of the turn, or needs two hands, or rattles audibly when
shaken, or sticks after the rinse. The hard case is the 0.10 gap after the rinse: it may turn dry
and bind wet, and a test that only turns it dry would pass a coaster that sticks in use.

The coupon does not test the look of option B, the clicks, the narrow ring at the star's points,
or steel balls; each is a later round if this one passes.

## 7. Recommendation

Start with the plain printed fit, no bought parts: print the eight-coupon ladder of §6 beside a
stock middle. If one gap turns cleanly, wet and dry, without rattle, build option B (today's star
in a turning ring) only after a render shows a seam circle that stays inside the straps; if no
such circle exists, decide between A's disc and a bigger turning part. Steel balls (C) are worth
a round only if the plain fit turns too briefly to enjoy; a bought bearing needs a taller coaster.

## Yours to do

- Say whether "spins" means a fidget you flick and watch, or a centre you can turn and that clicks
  back into line; the second is in reach at this size, the first likely is not without a bigger
  turning part or steel.
- Approve the eight-coupon plate when its page is written.
