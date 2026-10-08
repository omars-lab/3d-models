---
plate: swatch-10204
recipe: swatch-10204.yaml
iteration: 1
stage: waiting
times_printed: 0
runs: []
answers: "What does PLA Basic Hot Pink (10204) really look like printed: its top, its sheen and its bed face, on a chip and on our own straps?"
kind: taste
maturity: experiment
bets: []
unblocks: []
minutes: 18
grams: 5.44
bed_plates: 1
risk: ok
pictures:
  - swatch-media/chip.png
  - swatch-10204-media/bed.png
---

# swatch-10204 — a swatch of PLA Basic Hot Pink

**In short.** You picked our own swatch card over bought sample packs (D-105): "our swatch/samples
will be erived form bambu ... but we might buy other faimelnt too eventually". This is the swatch
for PLA Basic Hot Pink, code 10204, one color, #F5547C. On the printer now, so it can print as soon as you say yes. The plate is
[`swatch-10204.yaml`](swatch-10204.yaml). One bed, 18 minutes, about 5.44 g.

## What it is

- **CHIP:** a 50 x 30 mm card, 2 mm thick, with 10204 engraved in the top. The top shows the
  surface and the sheen; the bottom shows the bed face, the side a coaster sits on.
- **WINDOW:** a 30 mm window of the gBV coaster [sheets-04g](sheets-04g.md) printed, cut at its
  star, so the color is seen on our own straps and edges.

**The color is picked at the send:** `bambu print send … --color "#F5547C"`.

**What I assumed, for you to change:**

- **The code is the label.** It is the number on the spool, so a chip names the spool to buy again.
- **A window of the coaster, not a whole one,** to keep a swatch to a few grams.

## Why print it

A picture on a screen is not the color a coaster comes out in. The chip settles it for this spool,
and sits beside the others when picking a theme.

## After the print

What gets asked when it comes off the bed, one row at a time (the review-print skill asks them).

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| CHIP | Does the chip's top match the color catalog's hex for 10204, and how does its bed face differ? | Near the catalog's hex on top; the bed face flatter in sheen, since it printed against the plate. | Matches: the catalog's hex stands for PLA Basic Hot Pink. Off: the catalog entry for 10204 is corrected to the printed color, and the theme pictures that use it are drawn again. |
| WINDOW | Does PLA Basic Hot Pink read well on our own straps and edges, at coaster size? | As the chip reads; a very dark or very light color may lose the strap lines. | Reads well: the color stays a candidate for themes. Lines lost or too loud: the color-themes skill stops offering it for a coaster's straps. |

## Pictures

The chip, drawn from bikar's `Swatch-Chip.bkr` (every swatch's chip, with its own code).

![A swatch chip: a 50 by 30 mm card with a five-digit code engraved in the middle](swatch-media/chip.png)

The slice: the chip and the coaster window on the bed, in the slicer's green, since the recipe names no color and the send picks it.

![swatch-10204 on the bed: the chip and a 30 mm window of the gBV coaster](swatch-10204-media/bed.png)

## Cost and risk

One bed, 18 minutes, about 5.44 g (local slice, 2026-10-05, X2D preset and PLA Basic,
sliced for the Textured PEI plate Bambu Studio has saved, nothing sent). One color, so no swaps.

**Risk: ok.** Two flat pieces, no loose small parts.

## Your call

- [ ] **Approve as it stands**
- [ ] **Hold** — say why in the notes

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-05 | proposed — the swatch for 10204, by the color-themes skill's swatch.py (D-105) | this page |
| 2026-10-05 | sliced — local slice fits one bed, 18 minutes, 5.44 g | this page |
