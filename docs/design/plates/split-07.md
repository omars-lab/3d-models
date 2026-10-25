---
plate: split-07
recipe: split-07.yaml
iteration: 1
stage: proposed
times_printed: 0
runs: []
answers: "Does the whole flange coaster, with split-06's 40 pins where they stand and a 0.7 mm wall round each pin socket (split-06 had 0.9 mm), keep its hex and outer pieces snug, close flush all the way round and hold together, so it is a coaster to keep?"
kind: new
maturity: experiment
bets: []
unblocks:
  - "D-119: the flange coaster's socket wall is 0.7 mm (its reversal, if the whole coaster shakes or cracks)"
  - "the flange coaster as a production plate (D-098: one run kept as laid out)"
minutes: 116
grams: 31
bed_plates: 1
risk: watch
pictures:
  - split-07-media/pins.png
  - split-07-media/bed.png
  - split-07-media/ledges.png
---

# split-07 — the whole flange coaster with a 0.7 mm socket wall

![The whole lower half of the flange coaster from above, grey, with its 40 pins of 1.2 mm as white squares in four rings of ten: between the small kites, between the bigger kites, between the stars, and on the outer points](split-07-media/pins.png)

**In short.** On [split-08](split-08.md) you tried three walls round each pin's socket and said "the
middle one was the best one, 1c i think" and "left ond did (1a shook)". So the 0.9 mm wall that
[split-06](split-06.md) printed shook, and 0.7 mm was the best
([D-119](../../working-model/decisions-log.md#d-119--the-flange-coasters-socket-wall-is-07-mm)).
This plate is split-06 again, the whole coaster with no labels, with that one change. The plate is
[`split-07.yaml`](split-07.yaml).

## What it is

The whole flange coaster at 112.5 mm, as split-06: a lower half, an upper half, the middle piece,
and every kite, hex piece, star and outer piece.

| | split-06 | split-07 |
|---|---|---|
| Wall round each pin socket | 0.9 mm | **0.7 mm** |
| Disc round each pin (radius) | 1.625 mm | **1.425 mm** |
| Pins | 40, 1.2 mm, 0.25 mm play, in four rings | the same |
| Piece gap | 0.10 mm, kites 0.12 | the same |
| Labels | none | none |

- **The pins stand where split-06's stand**: rings at 14.3, 25.1, 33.5 and 54.4 mm, ten in each.
- **The disc still bites the hex pieces' ledges, but less.** On split-08's 0.7 mm set the hex
  piece's point kept 0.37 mm of its 0.80 mm ledge, where split-06 kept 0.17, and the outer pieces
  kept all of theirs. The recipe says the bite is by design, so the send's ledge check lets it
  through.
- Setting 8 on every piece, room 0.2, bosses on: all as split-06.

**The color is picked at the send**: say it with the yes.

**What I assumed, for you to change:**

- **"go" meant build this plate.** You said it after split-08's verdicts; if you meant something
  else, say so.
- **The pins stay where they are.** split-08 did not test moving them, and 0.7 did not shake.
- **0.7, not 0.45.** The 0.45 set did not shake either, but you picked 0.7, and nobody checked yet
  whether the one-line walls hold when pressed.
- **Sliced for the gold Textured PEI plate**, the one Bambu Studio is set to. It is sliced again
  at the send if another plate is on.

## How much the wall bites

Measured on the sliced plate by `.claude/skills/place-pins/scripts/ledge_check.py`: how far each
piece's hidden ledge reaches past its face at each corner, where a whole ledge reaches 0.80 mm.
Each piece's face is grey, its hidden ledge orange, and each corner whose ledge reaches less than
0.55 mm is ringed blue with how far it reaches.

| Pieces | What the check found |
|---|---|
| The 10 hex pieces | the point reaches 0.37 mm, the blunt end 0.45 mm, the sides the whole 0.80: split-08's 0.7 mm set exactly |
| The 10 outer pieces | 0.80 mm all round |
| The stars, the kites, the middle | 0.77 to 0.80 mm all round |

The picture shows the two groups the pins sit near: the hex pieces on top, the outer pieces below.

![Top row: the ten hex pieces, each ringed blue at its point (0.37) and its blunt end (0.45). Bottom row: the ten outer pieces with an even orange ledge all round and no rings](split-07-media/ledges.png)

## Why print it

split-08 showed the 0.7 mm wall on one slice. Only the whole coaster shows whether forty sockets
that thin, all at once, close flush, hold and keep every hex piece still. If it does, it can become
the production plate. If it shakes or a wall cracks, D-119 is reversed: 0.45 mm if its sockets
prove to hold, or the pins move off the points.

## After the print

What gets asked when it comes off the bed. One question first, in your own words; the rest only if
the answer does not cover them.

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| The whole coaster, put together | **Do:** Put every piece in the lower half, close the upper half on its pins and pinch it all the way round, then shake it. **Look for:** Is it a coaster you would keep as it is? If not, what is wrong? | Flush round the outside, no shake: split-08's 0.7 mm set did not shake. | Keep: it becomes the production plate. Not kept: what is wrong decides the next change. |
| The hex and outer pieces | **Do:** Push each hex piece and each outer piece side to side with a fingertip in the closed coaster. **Look for:** Snug, or do some wiggle? Which ones? | Snug: the 0.7 mm wall halves the bite at the hex point and leaves the outer pieces whole. | Snug: 0.7 mm stays. The hex pieces wiggle: try 0.45 mm, or move the pins off the points. |
| The bigger kites | **Do:** Lay two bigger kites side by side, and look at each against its neighbours in the closed coaster. **Look for:** Do they match? If one is lopsided, which side? | They match: as drawn the pieces are mirror-symmetric. | Match: nothing to change. Lopsided: a photo with the side marked, to find where the print differs from the drawing. |
| The sockets, pressed | **Do:** Press hard over each ring of pins, then pull the halves apart. **Look for:** Does each pin stay in its socket and the halves stay shut? | All hold, as on split-08's 0.7 mm set. | All hold: 0.7 mm stays. A socket lets go: the wall is too thin there. |
| Round each socket | **Do:** Look at the wall round each socket on the upper half, before and after pressing, against the light. **Look for:** Any split, crack or broken wall? | Whole: 0.7 mm is nearly two lines. | Whole: 0.7 mm stands. Cracked: back to 0.9 at those rings, or move the pins. |
| Closing it | **Do:** Close the upper half on the lower and press it down. **Look for:** Does it go on with an even press? | An even press: the pins and play are split-06's. | Even: nothing to do. Hard to close: loosen the play to 0.30. |
| The kites | **Do:** Push each kite side to side with a fingertip. **Look for:** Snug, tight or wiggling? | Snug. | Snug: 0.12 stays. Tight: 0.13. Wiggles: 0.11. |

## Pictures

Where the pins stand on the whole lower half, from above, at the top of this page. Drawn from the
coaster file at the plate's settings by `tools/print_review.py pins`.

The bed, from above, as the slice lays it out, each piece named. Drawn from the sliced plate by
`tools/print_review.py bed`.

![split-07 on the bed from above: the lower and upper halves of the whole coaster and every loose piece, each named](split-07-media/bed.png)

## Cost and risk

**About 116 minutes and 31 g of PLA** (the slicer's estimate, 6987 s and 31.45 g), one bed, no
prime tower, one color.

**Risk: watch.** As on split-06: each band sticks out 0.8 mm with nothing under it and may droop,
a look to judge. The kites and stars are small loose pieces that can lift or get knocked. The pins
are 1.2 mm and stand on the lower half's cut face, so a pin that prints badly breaks off as a look,
not a danger to the printer. New: forty sockets with a 0.7 mm wall, which only one slice has tried.

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
| 2026-10-25 | proposed: after split-08's print, on Omar's verdicts ("the middle one was the best one, 1c i think", "left ond did (1a shook)") and his "go"; split-06 with a 0.7 mm socket wall (D-119) | this page |
| 2026-10-25 | sliced — for the gold Textured PEI plate, 7 objects, no slicer warnings: 6987 s and 31.45 g | this page |
