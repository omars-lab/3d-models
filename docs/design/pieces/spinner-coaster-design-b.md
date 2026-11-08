# A spinner coaster: pause the print, drop in a bearing, print over it (design, researcher B)

Status: draft from one of two independent research passes, 2026-11-08. A checker will merge it with
the other pass into `spinner-coaster-design.md`. Nothing here has been printed. Raw sources:
[spinner-coaster-research-b.md](../../research/spinner-coaster-research-b.md) (cited below as W1,
E2, B3 and so on).

**The ask** (Omar, 2026-11-08): a spinner version of the coaster "we've been making in full",
where the print stops partway, he puts in a spinning bearing, and the print resumes and closes over
it.

## 0. The answer in one screen

- **Which coaster.** "In full" is read here as the one-piece coaster (the straps coaster, D-064),
  not the split coaster with loose pieces. That coaster is 4 mm thick with straps 1.2 mm on top
  (R2). A bearing is 4 mm tall at the thinnest (B2), so the spinner version is a thicker coaster,
  about 7 mm at a strap. This is the "different, thicker product" the earlier spinner-middle work
  set aside ([spinner-middle §0](../coaster/spinner-middle-design.md#0-the-answer-in-one-screen)).
  What changed: Omar now asks for the bearing and the pause by name.
- **The bearing.** A 6704 thin bearing: 20 mm hole, 27 mm across, 4 mm tall, stainless and sealed
  (§1).
- **What gets buried.** Only the **outer ring** of the bearing. The print lays a thin ring of plastic
  over the outer ring's top face and stops there. The seal and the inner ring stay open (§4).
- **What spins.** A separate printed **medallion** (a disc with one of our patterns on it) whose
  stub is pressed into the bearing's hole after the print is off the bed. The coaster body stays
  still; the medallion turns (§5).
- **The pause.** One pause in Bambu Studio, on the first layer above the bearing's top. On the X2D
  that writes `M400 U1` into the file (L1 to L3). The file is checked for it before sending (§3).
- **First print.** A small pocket coupon, not a coaster: three pocket sizes, one pause, and a
  no-pocket control beside them (§7).
- **The biggest open risk.** The cap's inner edge has to reach over the bearing's outer ring, a
  flat steel band about 1 mm wide between the pocket wall and the seal. With the default pocket it
  is laid one layer (0.2 mm) above the steel and sags onto it. Nobody publishes that band's width
  for the 6704 (section 4 of the research). It has to be measured with calipers, and the coupon
  tests whether plastic laid there holds.

## 1. Which bearing, and why

| Bearing | Hole × across × tall (mm) | Fits a coaster? | Source |
|---|---|---|---|
| 608 (skateboard) | 8 × 22 × 7 | Too tall: 7 mm of bearing plus a floor and a cap is a 9 mm coaster before the straps | B8, snippet |
| 688 | 8 × 16 × 5 | Small hole, 5 mm tall | B7, snippet |
| 6700 | 10 × 15 × 4 | 4 mm, but a 10 mm hole is a thin stub to press a medallion onto | B6 |
| **6704** | **20 × 27 × 4** | **4 mm, and the 20 mm hole takes a strong printed stub** | B1 to B3, fetched |
| 6705 | 25 × 32 × 4 | Same height, bigger middle | B4, fetched |
| 6706 | 30 × 37 × 4 | Same height, bigger still | B5, fetched |

**Default:** 6704, 20 × 27 × 4 mm, from the fetched [SKDIN S6704 page](https://www.skdin.com/products/productid-S6704).
Its width tolerance is "-0.120 mm to 0", so a bearing is never taller than 4.0 mm, which makes the
pocket depth safe to set (§2). The 6705 and 6706 are the same height and only change the diameters;
pick one of them if Omar wants a bigger turning middle (open question Q2).

Stainless and sealed is the pick for something that sits under wet mugs. The checker's source says
440C stainless resists rust better than chrome steel but "may corrode" (B11), so stainless is
better, not proof. The sealed stainless 6704 price was not fetched; the open stainless one is $2.65
(B3) and an SKF-branded sealed chrome one is $37.49 (B1). Nothing has been bought.

## 2. The pocket and its clearances

The coaster body is printed with a round pocket in the middle, open at the top until the pause.

| Measure | Value | Why |
|---|---|---|
| Pocket diameter | 27.2 mm to start, laddered on the coupon | below |
| Pocket depth | 4.2 mm | below |
| Floor under the bearing | 1.0 mm | below |
| Floor under the inner ring | 0.4 mm lower than under the outer ring | the inner ring must not rub |
| Cap ring over the outer ring | 0.6 mm (3 layers) | below |

**Default:** pocket diameter 27.2 mm, the bearing's 27 mm plus 0.2 mm, the top of the "0.1 to 0.2
mm clearance" range in the fetched [Printago guide](https://printago.io/guides/bambu-studio-magnet-holes)
(E2). Printed holes come out small (CAL-HOL-01), and the snippets on 608 pockets disagree on
whether 0.2 mm is right or too loose (B10). So the coupon prints three sizes: 27.1, 27.2 and 27.3
mm. The wanted fit is a **drop fit**: the bearing falls in under its own weight and does not rattle.
A press fit is ruled out during the pause, because pushing down hard on a print stuck to the bed
can shift it or the bed (§6, risk 7).

**Default:** pocket depth 4.2 mm, which is the bearing's 4.0 mm plus one 0.2 mm layer. The fetched
guides size the pocket to the part's height so it sits "just below a layer that will later cover
it" (E2), and one snippet adds about a layer for sag (E8). One extra layer means a bearing that sits
a little high, on a crumb or a bulge, still stays below the nozzle (§6, risk 2). The nearest
registered bet is CAL-FIT-01, though it is a ladder across diameters, not depths, so it does not
settle this. The cost of the extra layer: the bearing can lift up to 0.2 mm under the cap. The
coupon prints a 4.2 mm pocket and a 4.0 mm one side by side to measure whether that play matters.

**Default:** floor 1.0 mm (5 layers), under CAL-CST-03, the bet on the thinnest floor that stays
flat and closed under a pocket. Under the inner ring the floor steps down another 0.4 mm, two layers
of air, because our pkt-1 print showed one layer of air fuses and two come apart
([pkt-1](../plates/pkt-1.md)). The bearing's own steel does not fuse, but the inner ring must turn
without rubbing on a rough printed floor. The step goes from 20 mm to about 23 mm across; the exact
edge waits on the caliper reading (§4).

Elephant's foot (the first layers squashing outward, CAL-CST-05) does not touch the pocket, because
the pocket starts 1.0 mm up.

### The stack, bottom to top (90 mm coaster, 0.2 mm layers)

There is no side-view picture yet (follow-up F1). In words:

| Height (mm) | What prints there | Layer numbers |
|---|---|---|
| 0.0 to 0.6 | solid floor everywhere | 1 to 3 |
| 0.6 to 1.0 | solid floor, except a 23 mm round dip under where the inner ring will sit | 4 to 5 |
| 1.0 to 5.2 | the body, with the 27.2 mm pocket open through it | 6 to 26 |
| **pause** | the printer stops before layer 27; the bearing goes in | |
| 5.2 to 5.8 | cap ring: covers the body and laps over the outer ring's face, open in the middle | 27 to 29 |
| 5.8 to 7.0 | the straps, raised 1.2 mm, as on today's coaster; a round recess in the middle for the medallion | 30 to 35 |

Total: 5.8 mm between straps, 7.0 mm at a strap, against today's 4.0 and 5.2. The coaster's
`height` knob already goes to 16 mm (R2), so the slab can be this thick; what bikar cannot draw is
the closed pocket inside a height field (§9).

## 3. The pause, and how to set it in Bambu Studio

The pause fires **before** the layer it is put on (W1: "It pauses at the start of layer 107"; E1:
"inserted before the selected layer is printed"). So the pause goes on the **first layer above the
pocket**, layer 27 in the stack above, the one that prints from 5.2 to 5.4 mm.

Steps:

1. Slice the plate. Open the Preview tab.
2. Drag the layer slider on the right until it reads layer 27, height 5.40 (the slider shows a
   layer's top). Check the picture: layer 26 still shows the open pocket, and layer 27 shows the cap
   ring for the first time.
3. Right-click the slider handle and pick **Add Pause** (W1, W2).
4. Look for a color-change mark on that layer as well; one old thread says adding a pause also
   added one (W6, snippet). Remove it if it is there.
5. Slice again and export the plate.

On the X2D the pause is the command `M400 U1` (L1 to L3). Forum posts on other Bambu printers say
it parks the head where the firmware wants, and the user cannot change where (W4, W10). No official
or X2D page says what the X2D does during it (research §7).

**Validator:** the sliced file pauses exactly once, at the right height. Unzip the exported `.3mf`,
open its plate G-code, and find each `M400 U1` and the last layer height printed before it.
PASS: one `M400 U1`, after the layer ending at 5.2 mm and before the first move of the layer
ending at 5.4 mm.
FAIL: no `M400 U1` (the pause was lost; the printer would print the cap straight onto an empty
pocket), or one placed after layer 27 has started (a layer late, as a Prusa commenter saw, E1),
or two of them.

This check runs on the exact file that will be sent. Whether our own send path, `bambu print send`,
keeps a pause added in Studio is untested (research §7), so the check has to read what is sent, not
only what Studio saved. The send itself stays Omar's, per plate, as always.

## 4. How the print closes over the bearing

When the print resumes, layer 27 prints the whole top of the body at 5.2 to 5.4 mm, plus a ring
that reaches inward over the bearing's outer ring. The outer ring of a 6704 is the band from 27 mm
across in to where its seal starts. The bearing is about 3.5 mm wide from hole to rim, shared by the
outer ring, the seal and the inner ring, so the outer ring's flat face is likely about 1 mm wide. No
source gives the number: SKDIN says its drawings "will be launched soon" (B2), and the only shoulder
figure found is for a 608, by snippet (B8). **Measure it** (Q1).

The cap ring then reaches from the pocket wall inward by that measured width less 0.2 mm, so it
never touches the seal. Each layer of the ring is mostly anchored on the plastic body around the
pocket, with only its inner edge, about one line, reaching over the steel. With the default 4.2 mm
pocket that edge is laid one layer above the steel face, over 0.2 mm of air, and sags onto it; only
in a 4.0 mm pocket (coupon block P3) does it lie straight on the steel. Either way that is on
purpose: hot plastic barely sticks to cold steel, so the plastic body carries the ring and the
steel only stops the bearing lifting.

The cap ring starts at 0.6 mm, three layers. This is a starting value for the coupon, not a
settled default: no source and no registered bet covers plastic laid over a steel ring after a
pause, and this pass did not add a bet (a new one would go to `calibrate`). What it rests on: our
pkt-1 print had 0.6 mm bands printed over air come out level and 0.4 mm necks over air come out
whole ([pkt-1](../plates/pkt-1.md)), so three layers is one more than the thinnest that held. Lying
on steel instead of air is new; the coupon tests it.

What holds the bearing in: the snug pocket stops it sliding sideways, and the cap ring stops it
lifting out, with up to 0.2 mm of lift in the default pocket. The bearing is not glued and not
pressed in. If the cap ring fails, the bearing can
lift out under a pull from the medallion; the coupon's pull test (§7) checks for that.

## 5. What spins and what stays still

| Part | Still or turning | What it is |
|---|---|---|
| Coaster body, floor, straps | still | printed in one go, with the pause |
| Bearing outer ring | still | held by the pocket and the cap ring |
| Bearing inner ring | turning | free above the 0.4 mm dip in the floor |
| Medallion | turning | printed on its own; a 20 mm stub pressed into the bearing's hole |

The medallion is a disc about 40 mm across, sitting in a round recess in the coaster's top. Its stub
goes down through the open middle of the cap ring into the bearing's hole. Under the disc, above the
cap ring and the body, sits a gap.

**Default:** 0.4 mm of air between the medallion and the coaster body everywhere (under it and round
its edge), the two layers of air that came apart on [pkt-1](../plates/pkt-1.md) and the bet
CAL-CLR-01. Here the parts are printed apart, so it is a comfortable gap, not a tight one.

The medallion's top sits 0.2 mm below the coaster's top, as the spinner-middle work proposed
([spinner-middle §4](../coaster/spinner-middle-design.md#4-living-with-a-mug)). A mug then rests on
the still coaster and the medallion turns only when a finger flicks it. If Omar wants the mug itself
to turn on the medallion, the medallion sits proud instead and has to be big enough to carry a mug
(Q3).

A gap in this stack, stated rather than hidden: with the recess floor on the cap's top (5.8 mm),
0.4 mm of air under the disc and its top 0.2 mm below the straps (7.0 mm), the disc is only 0.6 mm
thick, a wafer. Two ways out, not chosen here: let the coaster grow by about 0.6 mm more, or keep
the cap ring only as wide as it must be over the pocket rim and drop the recess floor elsewhere
under the disc to 5.2 mm, which gives a disc about 1.2 mm thick (Q6).

The stub's press fit into the 20 mm hole is the CAL-FIT-01 press rung, tested on a second, pause-free
coupon (§7). It is done on the bench after printing, so it carries no risk to the printer.

## 6. What can go wrong at the pause or the resume, and the guard for each

The rule: no measurement is worth the machine (R10). Risks 1 to 3 can hurt the printer and each has a
hard guard. The rest only waste a print.

| # | What goes wrong | Harm | Guard |
|---|---|---|---|
| 1 | **The pause is missing or a layer late.** The printer prints the cap over an empty pocket, or the nozzle reaches an already-placed bearing late. | A wasted print; a layer late with the bearing in is risk 2. | The validator in §3, on the exact file sent. |
| 2 | **The bearing sits high.** A crumb, a stringy blob in the pocket, or a bearing tilted on its edge, so steel stands above 5.2 mm. The hardened-steel nozzle (L5) then drives into a steel ring. | Can damage the nozzle and knock the gantry, not only the print. | Pocket one layer deeper than the bearing (§2). Before resuming, lay a stiff card across the pocket on the body's rim and slide it: it must pass the bearing without catching. Then press the bearing flat with a fingertip. If the card catches, do not resume: stop the print. |
| 3 | **The head is moved by hand during the pause.** | Lost position or belt slip in two fetched reports (W2, W5); one hit the frame. | Never move the head or the bed by hand, and never change the machine's pause G-code (it is shared profile state, and one custom version re-homes and was reported to shift a layer, W4, W5). Drop the bearing in where the print is. |
| 4 | **The nozzle has cooled at the resume.** The first cap layer comes out thin or missing. | A weak cap, or the bearing lifts later. | Keep the pause short: have the bearing out of its bag, the card and tweezers ready, before the pause comes. One report says the nozzle heater goes off in a pause while the bed stays on (W8, snippet); a third-party page says A1 printers drop the nozzle 3 to 5 minutes in (W9, snippet). Neither is the X2D: the coupon reads what the X2D's screen shows at minute 1 and minute 5. A Prusa resume at 100 °C lost a print (E4). |
| 5 | **The bed cools in a long pause.** The print lifts from the bed and the cap lands out of place. | A wasted print. | The same short pause. Reports say the bed stays on (W3, W8); the coupon reads the bed on the screen during the pause. |
| 6 | **The print resumes by itself.** One poster saw long pauses restart on their own (W3). | If the bearing is not in, a cap over an empty pocket; if a hand is in the chamber, a moving head. | Be at the printer when the pause comes; do not walk away from a paused print with the door open. |
| 7 | **The bearing is pushed in hard.** | Can unstick the print, or load the bed. | Drop fit only (§2). If the bearing will not drop in, stop the print; that pocket size is the coupon's answer. |
| 8 | **Steel and magnets.** | Magnets in a pause cling to the hot end (E1, E3). | A bearing is steel, not a magnet, and is held by the pocket. No magnets in this design. |
| 9 | **A hot chamber.** The X2D is closed and its chamber heats (search 12). | A burn reaching in near a hot head. | PLA does not need the chamber heated. Reach in with tweezers, away from the parked head. |
| 10 | **Hot plastic on the seal.** If the cap ring is too wide it lays PLA on the rubber seal. | A bearing that drags or stops. | The cap stops 0.2 mm short of the measured seal edge (§4). Nothing found on PLA against a seal (research §7). |

## 7. What to print first: a pocket coupon, not a coaster

Omar's standing rule is to test a print question on one repeat of the shape, several settings to a
bed, with a stock control beside it (Omar, 2026-10-12). So the first print is a coupon plate, not a
coaster.

**Coupon 1: pockets and the pause.** Three small round blocks, each about 35 mm across and 5.8 mm tall,
each with one 6704 pocket and a cap ring, all paused once together:

| Block | Pocket diameter | Pocket depth | Reads |
|---|---|---|---|
| P1 | 27.1 mm | 4.2 mm | the tightest drop fit |
| P2 | 27.2 mm | 4.2 mm | the default |
| P3 | 27.3 mm | 4.0 mm | a loose fit, and whether an exact-depth pocket lets the bearing rattle |
| S | none | none | the stock control: the same block printed solid, beside the others, to show what the resume did to the surface |

One pause covers all three because they share a height. What to read off it:

1. Did each bearing drop in, and does it rattle once capped?
2. Did the cap's first layer print fully, at full width, over the steel and the plastic?
3. The nozzle and bed temperatures on the X2D's screen at the start of the pause, at minute 1 and at
   minute 5 (keep one pause deliberately about 5 minutes long, with the bearings already in).
4. Does the inner ring turn freely, by a fingertip, on each?
5. Pull test: hook a finger in the bearing's hole and lift. Does the bearing stay in?
6. Did the stock block's top come out the same as the others' (no seam or step at 5.2 mm)?

This uses about 25 g and three bearings, which can be cut out and reused. The bearings must be
measured first (Q1), to set the cap width.

**Coupon 2: the medallion stub, no pause.** Three short 20 mm stubs at three press sizes from the
CAL-FIT-01 ladder, printed flat. Press each into a bare bearing on the bench. This carries no pause
and no risk and can share a plate with anything.

Only after both read well: one full spinner coaster.

## 8. Other ways to the same toy

| Way | What it buys | What it costs | What it commits to |
|---|---|---|---|
| **A. Pause and cap (this doc)** | One printed body; the bearing is hidden and cannot fall out | A pause Omar has to be present for; risk 2 to guard; a 7 mm coaster | A pause on every print of it, so no unattended batch printing |
| **B. Split halves, bearing at assembly** | No pause; uses our split kernel and its pocket-with-neck holds (R3); the bearing is placed with the print off the bed, so no printer risk at all | A seam round the coaster; two pieces to print and join; the join has to hold | The split coaster family, its joins and its tests |
| **C. Through hole, pressed in after** | No pause; the classic fidget-spinner way; simplest to print | The bearing shows from underneath; held only by the press fit; the coaster's floor has a hole | A press fit that has to hold under wet mugs |
| **D. A whole-top turntable** | The whole top turns, like a lazy susan | A big thin bearing, larger than any checked here; a top piece to print | Sourcing a large thin bearing; not researched here |

A is the default because it is what Omar asked for, and its printer risks have hard guards. B is
the strong fallback: it needs no pause and keeps every hand out of the printer, and we already own
the pocket kernel. If the coupon shows the cap does not hold on the steel, B is next.

## 9. What bikar would need

The coaster is a height field (one top surface over a flat bottom, D-064). A closed pocket with a cap
over it is not a height field (R1). The split kernel builds closed pockets with a neck over them
(R3), which is the nearest thing we own. For the coupon, the blocks are simple enough to make by hand
in OpenSCAD with no bikar change. For a pattern coaster, bikar needs a "bearing pocket" hold on the
one-piece coaster, or the coaster is cut into the two pieces of way B. Neither is designed here.

## 10. Open questions for Omar

- **Q1.** Measure, with calipers, the flat face of the bearing's outer ring (from its outside rim to
  where the seal starts) on the bearing you buy. The cap width and the safety of the first resumed
  layer hang on it.
- **Q2.** The 6704's middle is 20 mm. Is a bigger turning middle wanted (6705, 25 mm; 6706, 30 mm),
  at the same 4 mm height?
- **Q3.** Should a mug turn on it (the medallion sits proud and carries the mug), or is it a toy you
  flick while the mug sits on the still coaster (the default)?
- **Q4.** Is a coaster about 7 mm thick acceptable, against today's 5.2 mm?
- **Q5.** Is the pause-and-cap way (A) the one, or would the split way (B), with no pause, be
  preferred once you have seen both?
- **Q6.** The turning disc comes out 0.6 mm thick in the stack as drawn (§5). Should the coaster
  grow a little more, or should the recess under the disc go deeper outside the cap ring?

## Follow-ups

- **F1.** A side-view picture of §2's stack, with `draw-side-view`, once the stack is agreed.
- **F2.** The coupon's OpenSCAD file and its plate page, after Q1's measurement.
- **F3.** A check in `tools/bambu/` that a plate meant to pause still carries its `M400 U1` in the
  file it sends (§3's validator as a tool).
