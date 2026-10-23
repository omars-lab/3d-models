---
plate: split-06
recipe: split-06.yaml
iteration: 1
stage: proposed
times_printed: 0
runs: []
answers: "Does the whole flange coaster, with split-05's set 3 settings (1.2 mm pins, 0.10 mm piece gap, the kite at 0.12) and no labels, close flush all the way round, hold together and keep its pieces snug, so it is a coaster to keep?"
kind: new
maturity: experiment
bets: []
unblocks:
  - "D-100: lip or flange, which way a split coaster holds its loose pieces (with split-01)"
  - "the flange coaster as a production plate (D-098: one run kept as laid out)"
minutes: 112
grams: 31
bed_plates: 1
risk: watch
pictures:
  - split-06-media/pins.png
  - split-06-media/bed.png
---

# split-06 — the whole flange coaster, set 3's settings, no labels

![The whole lower half of the flange coaster from above, grey, with its 31 pins of 1.2 mm as white squares round every outer edge and point, and none on the ring round the middle piece](split-06-media/pins.png)

**In short.** On [split-05](split-05.md) you said "both are good", "2a one probably better", "2c
one shakes a bit", then: "lets send a 2a print with the whole patterh, no labels, a production
piece". This plate is that: the whole coaster at set 3's settings, with nothing carved into any
piece. The plate is [`split-06.yaml`](split-06.yaml).

## What it is

The whole flange coaster at 112.5 mm across: a lower half, an upper half, and every loose piece,
the middle, the kites, the hexes, the stars and the outer pieces.

- **1.2 mm pins, at least 6 mm apart**: 31 of them, round every outer edge and point, as set 3.
  The play round each pin stays 0.25 mm.
- **The ring round the middle piece still has no pin.** No spot there has room for one. This is the
  first print where that ring is closed all the way round, so it is the first that shows whether it
  stays flush.
- **Piece gap 0.10 mm** for the middle, hexes, stars and outer pieces; **0.12 mm for the kites**,
  set 3's kite.
- **No labels**: no carved ids, and no number on the lower half's bottom.
- **Setting 8** on every piece, as every split plate since split-03.
- **No glue.**

**The color is picked at the send**: say it with the yes ("yes, in green").

**What I assumed, for you to change:**

- **The kites at 0.12 mm.** Set 3's kite, but the two kites on split-05 were never compared on
  their own.
- **One coaster, on one bed.** If you would rather print two and keep the better, say so.
- **Sliced for the gold Textured PEI plate**, which was on the bed after split-05. It is sliced again
  at the send if another plate is on.

## Why print it

The slices settled the pin (1.2 mm) and the piece gap (0.10 mm). What is left only a whole coaster
can show: whether the ring round the middle closes flush with no pin on it, whether the halves stay
flat across the full 112.5 mm, and how it goes together with every piece in. If you keep it as it
comes off the bed, it is the first production plate of this coaster (D-098), and it can be printed
again with no new yes (D-095).

## After the print

What gets asked when it comes off the bed. One question first, in your own words; the rest only if
the answer does not cover them.

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| The whole coaster, put together | **Do:** Put every piece in the lower half, close the upper half on its pins and pinch it all the way round. Look at the edge and round the middle piece, and shake it. **Look for:** Is it a coaster you would keep as it is? If not, what is wrong? | Flush round the outside, as set 3. Round the middle, maybe a space. No shake. | Keep: it becomes the production plate. Not kept: what is wrong decides the next change. |
| The ring round the middle piece | **Do:** Pinch the closed coaster round the middle piece. **Look for:** Flush, or a space? | Maybe a space: there is no pin there. | Flush: nothing to do. A space: the middle needs its own hold (a wider strap for a pin, or glue). |
| The halves, laid flat | **Do:** Put the closed coaster on a table and press each side. **Look for:** Does it rock? | Flat. | Flat: nothing to do. Rocks: the halves bow over the full width; look at the bed face and the cooling. |
| The kites | **Do:** Push each kite side to side with a fingertip. **Look for:** Snug, tight or wiggling? | Snug. | Snug: 0.12 stays. Tight: 0.13. Wiggles: 0.11. |

## Pictures

Where the pins stand on the whole lower half, from above, at the top of this page: the half in grey,
each 1.2 mm pin a white square. Drawn from the coaster file at the plate's settings by
`tools/print_review.py pins`.

The bed, from above, as the slice lays it out, each piece named. Drawn from the sliced plate by
`tools/print_review.py bed`.

![split-06 on the bed from above: the lower and upper halves of the whole coaster and every loose piece, each named](split-06-media/bed.png)

## Cost and risk

One bed, 112 minutes, about 31 g (local slice, 2026-10-23, X2D preset and PLA Basic, from bikar #342), sliced for the gold Textured PEI plate (`--plate-type textured_plate`). The slicer gave no warnings, and all 7 items carry setting 8. One color, so no swaps.

**Risk: watch.** As on split-05: each band sticks out 0.8 mm with nothing under it and may droop,
a look to judge. The kites and stars are small loose pieces that can lift or get knocked. The pins
are 1.2 mm and stand on the lower half's cut face, so a pin that prints badly breaks off as a look,
not a danger to the printer.

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
| 2026-10-23 | proposed: after split-05's print, on Omar's words "lets send a 2a print with the whole patterh, no labels, a production piece"; set 3's 1.2 mm pins, the 0.10 mm piece gap, the kite at 0.12 | this page |
