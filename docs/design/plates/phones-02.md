---
plate: phones-02
recipe: phones-02.yaml
iteration: 1
stage: waiting
times_printed: 0
runs: []
answers: "How much time and filament does one color save over phones-01, and do the small phones keep their lens bumps at twice the thickness?"
kind: taste
maturity: experiment
derived_from: phones-01
bets: []
unblocks: []
minutes: 12
grams: 3
bed_plates: 1
risk: ok
pictures:
  - phones-02-media/bed.png
---

# phones-02 — phones-01 in pink only, with bigger small phones

**In short.** You asked "i also want to make a pink only version of our print ... and I want to
make the itiny phone a bit bigger - 1.25x their lenght and width and 2x their thickness". This is
[phones-01](phones-01.md) with every phone in pink, and the two tiny phones made 1.25 times wider
and longer and twice as thick. The plate is [`phones-02.yaml`](phones-02.yaml). One bed, 12
minutes, about 3.5 g, one color.

## What it is

- **The two big phones.** The same iPhone 16 Pro as on phones-01 and
  [sheets-04d](sheets-04d.md), cut out of its case by
  [`sheets-04d-phone.scad`](sheets-04d-phone.scad), at its own size: about 16.6 x 40 x 4.6 mm.
- **The two small phones.** phones-01's quarter phones were 0.25 of the big one on every side,
  about 4.2 x 10 x 1.2 mm. These are 1.25 times that across and twice that up: 0.3125 across and
  0.5 up, about 5.2 x 12.5 x 2.3 mm. That is about 11 layers instead of six, so the lens bumps
  should come out instead of blurring. In the plate picture they are there.
- **One color.** Pink only, so the printer never swaps nozzles and prints no prime tower.

To scale a phone differently up and across, a plate recipe's `scale:` now also takes one number
per side, `[x, y, z]`, besides the single number it took before. A single number gives the same
plate id it always did.

The phone file is not in git, as on phones-01: this repo is public and the model's license likely
forbids sharing it. It sits in the gitignored imports folder and the recipe holds it to its hash.

**What I assumed, for you to change:**

- Pink is the same pink as phones-01 (#F5547C).
- Still two big and two small phones, as on phones-01.
- "Thickness" is the height off the bed, and "length and width" the two sides lying on it.

## Why print it

It is phones-01 without the color swaps, so it shows what one color saves. phones-01 swapped color
on every one of its 22 layers and took about 62 minutes against the slicer's 22: about 1.6 minutes
lost per swap. This plate's slice is 12 minutes; if it prints in about that, the swaps were the
whole difference. It also shows whether the thicker small phones keep their detail.

## Pictures

The slice: two big pink phones side by side, and the two small phones to their left.

![phones-02 on the bed: two big pink phones and two small pink phones](phones-02-media/bed.png)

| Phone | Size (mm) | Where on the bed (mm from front left) |
|---|---|---|
| PINK PHONE | about 16.6 x 40 x 4.6 | 151.1, 128 |
| PINK PHONE | about 16.6 x 40 x 4.6 | 132.5, 128 |
| PINK SMALL | about 5.2 x 12.5 x 2.3 | 119.7, 140.9 |
| PINK SMALL | about 5.2 x 12.5 x 2.3 | 119.7, 127.2 |

## Cost and risk

One bed, 12 minutes, 3.46 g of pink (local slice, 2026-10-04, X2D preset and PLA Basic, sliced for
the Textured PEI plate Bambu Studio has saved, no slicer warnings, no brim, support or raft,
nothing sent).

Against phones-01: that plate sliced at 22 minutes and 4.85 g and printed in about 62 minutes. This
one carries slightly more plastic in its small phones and still weighs about 1.4 g less, so about
1.5 g of phones-01, roughly a third, went to the color swaps and their prime tower.

**Risk: ok.** Four phones lying flat, one color. A small phone could come loose from the bed;
that costs a phone, not the printer. The X2D needs pink loaded before the send.

## Your call

- [ ] **Approve as it stands** — two big and two small phones, all pink
- [ ] **Hold** — say why in the notes

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-04 | proposed — at Omar's ask: phones-01 in pink only, the small phones 1.25 times wider and longer and twice as thick | this page |
| 2026-10-04 | sliced — local one-color slice fits one bed, 12 minutes, 3.46 g, no slicer warnings | this page |
