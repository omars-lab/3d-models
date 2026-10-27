---
plate: split-10
recipe: split-10.yaml
iteration: 1
stage: waiting
times_printed: 0
runs: []
answers: "Which change fixes each loose piece split-07 got wrong: the stars' curved faces, the middle's webbed feel, the loose kites and the dovetail fit?"
kind: new
maturity: experiment
bets: []
unblocks:
  - "the flange coaster's loose pieces, settled before a whole coaster is printed again"
minutes: 28
grams: 6
bed_plates: 1
risk: ok
pictures:
  - split-10-media/bed.png
---

# split-10 — the flange coaster's loose pieces, one per setting, stock beside each

![split-10 on the bed from above: twelve loose pieces, each printed as its two halves side by side and named — two ten-point middle pieces, three five-point stars, three kites, two hexagon pieces and two outer pieces](split-10-media/bed.png)

**In short.** split-07's frame came out well, but you found four things wrong with its loose
pieces: the stars' faces curve at the edges, the middle piece has a "webbed duck feel", the
"dovetail kites are really loose", and you want to experiment on them. This bed is those pieces
only, no frame, about 28 minutes. Each kind has a stock piece, exactly as split-07 printed it,
beside one or two changed ones. You try them in the split-07 frame you already have. The plate
is [`split-10.yaml`](split-10.yaml).

## What it tries

| Piece | Stock (as split-07) | Changed | What the change tests |
|---|---|---|---|
| Five-point star | STAR-STOCK | **STAR-WHOLE**: printed in one piece, not cut in two | Whether cutting the star caused the curve |
| | | **STAR-SUPPORT**: cut, with supports under the step | Whether the curve is the step drooping over air |
| Ten-point middle | MIDDLE-STOCK | **MIDDLE-SUPPORT**: supports under the same step | Whether the webbed feel is the same droop |
| Kite | KITE-STOCK (0.12 mm gap a face, pin hole 0.25 mm wider than the pin) | **KITE-G11**: gap 0.11 mm | A snugger kite in its hole |
| | | **KITE-PIN20**: pin hole 0.20 mm wider | Two halves that hold tighter to each other |
| Hexagon piece | HEX-STOCK (dovetail 0.15 mm a side) | **HEX-SLIDE10**: dovetail 0.10 mm a side | A tighter dovetail |
| Outer piece | OUTER-STOCK (dovetail 0.15 mm a side) | **OUTER-SLIDE10**: dovetail 0.10 mm a side | The same, on the other piece that has one |

**Why the stars curve, we think.** Each cut half prints face down. Its first 0.6 mm is the face;
above that, the band that sits under the frame's lip steps out 0.8 mm with nothing under it. At
the star's sharp points that overhang sags, and the face edge flares with it. The supports put
something under that step for two layers. The lasting fix is a slope under the step in the model
itself; that is a change to bikar, written on the coaster backlog, not tried here.

**"Dovetail kites".** The kites are joined by a pin, and the hexagon and outer pieces by the
dovetail. Both are on this bed, so the answers below settle which you meant.

**Telling the pieces apart.** No piece carries a label: both faces of a cut piece show in use,
and an id may only go on a face that hides (D-114). Take them off the bed one pair at a time,
using the picture above, and keep each pair in its own pile or bag with its name.

Every piece is split-07's in everything that touches the frame: size, pin rings, the 0.2 mm room,
setting 8 (infill and wall overlap 55%). Only the one setting named above changes.

## After the print

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| STAR-STOCK, STAR-WHOLE, STAR-SUPPORT | **Do:** Close each cut star's two halves, then lay the three stars face up side by side and look at each from the side, along a point. **Look for:** Which star's face is flat out to its points, with no curve at the edges? | STAR-SUPPORT flattest: it has something under the step that sagged. STAR-WHOLE shows whether the cut itself made the curve. | Support best: stars print with supports until the slope under the step is in bikar. Whole best: the cut caused it, and stars print whole. All three curve: the cause is something else, and the slope in bikar is next. All the same as split-07: tell us what you see, in the notes. |
| MIDDLE-STOCK, MIDDLE-SUPPORT | **Do:** Close each middle piece's halves and run a finger round its edge, then set each in the split-07 frame's middle hole. **Look for:** Does MIDDLE-SUPPORT lose the webbed feel MIDDLE-STOCK has? Say in the notes what "webbed duck feel" means. | MIDDLE-SUPPORT smoother at the edge, if the webbed feel is the same sag as the stars'. | Support fixes it: the middle prints with supports. Same: the feel is something else, and your note says what to change. Support worse: no supports on the middle. |
| KITE-STOCK, KITE-G11, KITE-PIN20 | **Do:** Put each kite in a kite hole of the split-07 frame, close the frame and shake it gently; then pull each kite's two halves apart. **Look for:** Which kite does not rattle in its hole, and which kite's halves hold together best? | KITE-G11 rattles least in the hole. KITE-PIN20's halves hold together best. | Gap 0.11 best: kites go to gap 0.11. Pin hole 0.20 best: kites go to a 0.20 pin hole. Both help: both changes on the next coaster. Neither: the kites need another way to hold. |
| HEX-STOCK, HEX-SLIDE10, OUTER-STOCK, OUTER-SLIDE10 | **Do:** Slide each piece's two halves together on their dovetail, then try to wiggle them apart. **Look for:** Do the 0.10 mm ones slide on and hold tighter than stock, and do any jam? | The 0.10 mm ones hold tighter and still slide on: sld-1's rails slid and held at 0.10, 0.15 and 0.20. | 0.10 better: dovetails go to 0.10 a side. The same: they stay at 0.15. 0.10 jams: they stay at 0.15. These were the loose ones: the dovetail was what you meant, and 0.10 is the fix if it holds. |

## Pictures

The bed, from above, as the slice lays it out, each piece named. Drawn from the sliced plate by
`tools/print_review.py bed --zoom`, at the top of this page.

## Cost and risk

**About 28 minutes and 6 g of PLA** (the slicer's estimate), one bed, no prime tower, one color.

**Risk: ok.** Small flat pieces. The two support pieces carry two thin layers of support to pick
off. The slice check read the supports back on those two pieces only, and the G-code has support
lines under them and nowhere else.

## Your call

- [ ] **Approve as it stands**: say the color with the yes
- [ ] **Hold**: say why in the notes

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-27 | proposed: on Omar's split-07 notes ("stars faces are just bad", "webbed duck feel", "dovetail kites are really loose", "i want to run experiments on these infill pieces"); one piece per setting, stock beside each | this page |
