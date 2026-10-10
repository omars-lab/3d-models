---
plate: sheets-04g-fit3
recipe: sheets-04g-fit3.yaml
iteration: 1
stage: proposed
times_printed: 0
runs: []
answers: "Does the 0.025 mm middle piece win again beside its two controls in a fresh coaster, and does a 0.075 mm kite go in easier than the 0.05 one and still stay in?"
kind: new
maturity: experiment
bets:
  - CAL-LSE-01
unblocks:
  - "the middle piece's gap on the next sheets-04g iteration"
  - "the kites' gap on the next sheets-04g iteration"
  - "CAL-LSE-01, the loose-piece gap per face by shape in a straps-only frame"
minutes: 70
grams: 19
bed_plates: 1
risk: watch
pictures:
  - sheets-04g-fit3-media/bed.png
  - sheets-04g-fit3-media/ids.png
  - sheets-04g-fit3-media/kites.png
---

# sheets-04g-fit3 — the 0.025 middle piece again, and a looser kite

**In short.** On [sheets-04g-fit2](sheets-04g-fit2.md) you picked the middle piece at 0.025 mm
("4gh ic is winner") and said the 0.05 kites "could be a bit smaller, tought to insert". But the
pieces that printed on both fit plates did not feel the same on both, though the files, the
settings and the spot on the bed were the same ([the issue](../../issues/sheets-04g-fit.md#the-same-file-a-different-fit)).
So one win is a good sign, not a settled gap. This plate prints the 0.025 piece again beside its
two controls, the kites at 0.05 and at a looser 0.075, and a fresh coaster to try them in.

## What it is

Recipe: [sheets-04g-fit3.yaml](sheets-04g-fit3.yaml). The same size as sheets-04g-fit2 (112.5 mm
across, 3.75 mm straps, 4.4 mm tall).

- **The coaster:** the gBV minimal coaster, as sheets-04g-fit2 printed it, with `Z` on its bottom.
- **The middle piece at the same three gaps as fit2:** 0, 0.025 and 0.05 mm per face, with the
  same dots (three, two, one) and the same letters (A, C, E). The code `4GJ` tells them from
  fit2's `4GH` pieces.
- **Ten kites at 0.05, one dot each:** the control. On fit2 they were tough to push in.
- **Ten kites at 0.075, no dot.** This is an assumption, not a decision: halfway between 0.05
  ("tought to insert") and sheets-04g-fit's 0.10 ("too small/lost"). A kite has no room for a
  carved id, so the dot is how the two piles are told apart. The dot is in the top, so it does
  not change the fit.

## Why print it

- **The question:** does `4GJ 1C` (0.025) sit firmer than `4GJ 1E` and go in easier than
  `4GJ 1A` again? And does a 0.075 kite go in easier than a 0.05 one and still stay in upside down?
- **The bet it moves:** CAL-LSE-01, the loose-piece gap per face by shape in a straps-only frame
  ([bets.md](../../../.claude/skills/calibrate/bets.md)).
- **What it lets us decide:** the middle piece's gap and the kites' gap on the next sheets-04g
  iteration.
- **What to read off it:** for each piece, does it go in by hand, does it stay with the coaster
  upside down, and does it come out too easily.

## After the print

What gets asked when the plate comes off the bed, one row at a time (the review-print skill asks
them). Each middle piece is named by the id cut into its bottom: `4GJ 1A` reads 4GJ over 1 A. The
fresh coaster carries a small `Z`. The kites have no id: the 0.05 ones have one dot in the top, the
0.075 ones none. Keep this plate's pieces apart from fit2's; the codes differ (4GJ here, 4GH there),
but the kites look the same.

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| `4GJ 1A` (gap 0, three dots on top), `4GJ 1E` (0.05, one dot), the fresh coaster (`Z` on its bottom) | **Do:** Push `4GJ 1A` by hand into the middle hole of the `Z` coaster, then take it out. Do the same with `4GJ 1E`. **Look for:** Is `4GJ 1A` very tight, as `4GH 1A` was? Is `4GJ 1E` loose, as `4GH 1E` was? Say each by its id. | The same as on fit2: 1A very tight, 1E loose. | Same: this coaster's holes match fit2's, and the next row is read as it is. Different: the holes moved again, so the next row is read against these two, not against fit2. |
| `4GJ 1C` (0.025, two dots), the `Z` coaster | **Do:** Push `4GJ 1C` by hand into the middle hole of the `Z` coaster. Hold the coaster upside down over the table, then pull the piece out with a fingertip. **Look for:** Does it go in without forcing? Does it stay in upside down? Is it firmer than `4GJ 1E` and easier than `4GJ 1A`? | The winner again: in by hand, stays upside down, between the two. | Yes: 0.025 is the middle piece's gap, now on two prints. No: the step is inside how much the fit moves from print to print, and the gap is picked from the controls you like best over both plates. |
| The kites with one dot (0.05), the kites with no dot (0.075), the `Z` coaster | **Do:** Push three dotted kites by hand into three kite holes of the `Z` coaster, and three plain kites into three others. Then hold the coaster upside down over the table. **Look for:** Which go in easier? Do both kinds stay in upside down? | The plain 0.075 kites go in easier than the dotted 0.05 ones, and both stay in. | Plain easier and staying: 0.075 is the kites' gap. Plain falling out: the gap sits between 0.05 and 0.075, and 0.05 stays for now. Both the same: the 0.025 step is lost in the print, as above. |

## Pictures

The slice from above (2026-10-10), front of the bed at the bottom, drawn only over the part of the
bed the pieces take. Each piece has its own color and a label. The two kite rows sit at opposite
corners of the bed, so each comes off as its own pile.

| Where | What | In the picture |
|---|---|---|
| the middle | COASTER | amber |
| back left, one diagonal row of kites | KITE 0.05 (one dot each) | blue |
| front right, one diagonal row of kites | KITE 0.075 (no dot) | green |
| left | MIDDLE 0.025 (`4GJ 1C`) | purple |
| front, the left one of two | MIDDLE 0.05 (`4GJ 1E`) | yellow |
| front, the right one of two | MIDDLE 0 (`4GJ 1A`) | pink |

![sheets-04g-fit3 on the bed: the coaster in the middle, two rows of ten kites and three middle pieces round it, each labeled with its gap](sheets-04g-fit3-media/bed.png)

The ids cut into the three middle pieces' bed faces, seen from below (D-109): A is the 0 gap, C
0.025 and E 0.05, the same letters as on fit2 under a new code.

![The bottoms of the three middle pieces: ten-pointed pieces reading 4GJ over 1 and A, C or E](sheets-04g-fit3-media/ids.png)

The coaster carries a small `Z` on a strap left of the middle, in the same place as on
sheets-04g-fit ([its picture](sheets-04g-fit-media/ids-coaster.png)).

The two kite rungs from above (`tools/print_review.py art`, the tops only): one dot in each 0.05
kite, none in the 0.075. The dot is 1 mm across.

![Two rows of ten kites from above: the 0.05 ones each with one dot, the 0.075 ones plain](sheets-04g-fit3-media/kites.png)

## Cost and risk

One bed, 70 minutes, about 19.4 g (local slice, 2026-10-10, X2D preset and PLA Basic, the glacier
plate sliced as the High Temp Plate, no slicer warnings, no brim, support or raft, nothing sent).
One color, so no swaps. fit2's slice said 67 minutes and the print took 75.

**Risk: watch.** Twenty kites of about 0.05 cm³ each are small loose pieces, the kind that can lift
or get knocked by the nozzle. sheets-04g, sheets-04g-fit and fit2 printed the same kites at this
size without trouble.

## Your call

- [ ] **Approve as it stands**: the coaster, the three middle pieces and the two kite rungs.
  Say the color with the yes.
- [ ] **Hold**: say why in the notes.

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-10 | proposed: the middle piece at 0, 0.025 and 0.05 mm again, the kites at 0.05 and 0.075, and a fresh coaster, after fit2 picked 0.025 and found the 0.05 kites tough to push in, and the same files fit differently on two prints | [sheets-04g-fit2](sheets-04g-fit2.md), [the issue](../../issues/sheets-04g-fit.md#the-same-file-a-different-fit) |
| 2026-10-10 | sliced: local slice fits one bed, 70 minutes, 19.4 g, no slicer warnings; the carved ids read `4GJ 1A`, `1C` and `1E` from below, and the 0.05 kites carry their dot | this page |
