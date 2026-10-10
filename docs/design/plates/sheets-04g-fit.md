---
plate: sheets-04g-fit
print_log: '[[print-logs/sheets-04g-fit|print log]]'
recipe: sheets-04g-fit.yaml
iteration: 4
stage: printed
times_printed: 1
runs: [2026-10-10-sheets-04g-fit]
answers: "At what gap does a kite drop into the sheets-04g coaster by hand and stay, and at what gap does the middle piece, now cut along the strap's real edge, sit without rattling?"
kind: new
maturity: experiment
bets:
  - CAL-LSE-01
unblocks:
  - "the gap per group for the next sheets-04g iteration: kites and middle piece now, the hexes, stars and outer pieces once judged"
  - "CAL-LSE-01, the loose-piece gap per face by shape in a straps-only frame"
minutes: 78
grams: 21
bed_plates: 1
risk: watch
pictures:
  - sheets-04g-fit-media/bed.png
  - sheets-04g-fit-media/ids.png
  - sheets-04g-fit-media/ids-coaster.png
---

# sheets-04g-fit — the kites and the middle piece at a ladder of gaps

**In short.** On [sheets-04g](sheets-04g.md) you said "the small kits were too tight ti fit" and
"adn the middle piece was too lose". Every piece there was cut at gap 0. The write-up,
[sheets-04g: the kites too tight, the middle piece too loose](../../issues/sheets-04g-fit.md),
found two different causes. The middle piece had sharp inward corners where the strap's edge
is round, which left 0.45 mm of play at each of its ten notches. The kites had no play anywhere
and the least room for error of any piece. bikar now cuts every piece along the strap's real
edge (bikar #303), so the gap is the gap all the way round. This plate prints the two pieces you
named, at several gaps each, and a fresh coaster to press them into, beside the one you already
have. One bed, 78 minutes, about 21 g.

## What it is

Recipe: [sheets-04g-fit.yaml](sheets-04g-fit.yaml). The same size as sheets-04g (112.5 mm across,
3.75 mm straps, 4.4 mm tall), so the pieces fit that coaster's holes. The gap comes entirely off
the piece, so the coaster you have would do. You asked for a fresh one anyway (2026-10-06: "we
should re-print minimal consturciton with this to fit in again"), so the plate prints one too.

- **The coaster:** the gBV minimal coaster, as sheets-04g printed it.
- **Kites, ten at each of five gaps:** 0.05, 0.10, 0.15, 0.20 and 0.25 mm per face (50 kites).
- **The middle piece, one at each of four gaps:** 0, 0.05, 0.10 and 0.15 mm per face. Its gap 0
  is not the old gap 0: it is cut along the round strap edge now, so it should no longer rattle.
- **Dots on each middle piece**, as you asked ("3 dots for biggest, 1 dot for smallest"): four at
  gap 0, three at 0.05, two at 0.10, one at 0.15. Each dot is 1 mm across, cut into the top, with
  at least 0.8 mm of top left to the piece's edge (CAL-CST-01). The kites carry none. Since
  bikar #324 a dot row sits at the piece's widest spot, and a kite holds one dot at gaps 0.05
  to 0.15 but none at 0.20 or 0.25, so dots can split the rungs into two groups at most, not
  five. How to keep the kite rungs apart is call 6b
  on the [2026-10-06 calls page](../../working-model/feedback-requests/2026-10-06-open-calls.md).

## Why print it

- **The question:** which gap lets a kite drop in by hand and stay, and which middle piece sits
  without rattling?
- **The bet it moves:** CAL-LSE-01, the loose-piece gap per face by shape in a straps-only frame
  ([bets.md](../../../.claude/skills/calibrate/bets.md)). It is not borrowed from CAL-FIT-01's
  sliding fit (0.15). That was set across the diameter of round parts, which have no points.
- **What it lets us decide:** a gap per group for the next sheets-04g iteration.
- **What to read off it:** for each kite rung, does a kite go into its hole by hand, and does it
  stay in when the coaster is turned over; for each middle piece, does it go in, and does it
  rattle or turn.

## After the print

What gets asked when it comes off the bed, one row at a time (the review-print skill asks them).
Each row names the pieces by the id cut into their bottoms, as the [pictures](#pictures) show:
`4GF 4A` is the middle piece reading 4GF over 4 A, and the fresh coaster carries a small `Z`. The
kites have no id and no dots, so each row names them by the pile they came off the bed in.

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| The kites (no id): five piles of ten, one per gap, 0.05, 0.10, 0.15, 0.20 and 0.25 mm, kept apart as they came off the bed; the fresh coaster (`Z` on its bottom) | **Do:** Take one kite from each pile and push it by hand into a kite hole of the `Z` coaster, a different hole for each pile. Then hold the coaster upside down over the table. **Look for:** Which piles' kites go in by hand, and which will not go in? Of those that went in, which stay in upside down, and which drop out? Say each by its pile's gap. | A middle rung: gap 0 was too tight on sheets-04g, and a wide gap leaves nothing to grip in a floorless coaster. | That rung is the kites' gap on the next sheets-04g iteration and the theme plates (CAL-LSE-01). All too tight: the ladder moves looser. All fall out: kites need a press. |
| `4GF 4A` (gap 0, four dots on top), `4GF 4B` (0.05, three dots), `4GF 4C` (0.10, two), `4GF 4D` (0.15, one) | **Do:** Push each middle piece in turn into the middle hole of the `Z` coaster. With it in, shake the coaster gently next to your ear, then try to turn the piece with a fingertip. **Look for:** Which go in by hand? Of those, which sit silent and do not turn, and which rattle or turn? Say each by its id. | Gap 0: it is cut along the round strap edge now, which took out the 0.45 mm of play at its notches. | That gap is the middle piece's on the next iteration. Gap 0 still rattles: the corners were not the whole cause, and the sheets-04g fit issue is opened again. |
| The fresh coaster (`Z` on its bottom, on a strap left of the middle) and the sheets-04g coaster (no id) | **Do:** Take the kite pile and the middle piece that fit best in the `Z` coaster, and push them into the sheets-04g coaster the same way. **Look for:** Does each go in as easily, and sit as firmly, as in the `Z` coaster, or is it tighter or looser? | The same: the coaster has not changed, and the gap comes off the piece. | Same: one gap per piece shape is enough. Different: hole size moves from print to print, and the gaps need room for it. |

## Pictures

The slice from above (2026-10-07, with the coaster), front of the bed at the bottom, drawn only
over the part of the bed the pieces take. Each rung has its own color, and a label on it or with a
line to it. The kite rungs look alike off the bed, so take one rung off at a time and bag or mark
it.

Going round the coaster (the colors are the picture's, not the print's):

| Where | What | In the picture |
|---|---|---|
| the middle | COASTER | amber |
| back left, two interlaced rows of kites | KITE 0.20 (the back row), KITE 0.05 (the front row) | grey, blue |
| left, two middle pieces one above the other | MIDDLE 0.05 (back), MIDDLE 0.15 (front) | purple, teal |
| front left, a row of kites | KITE 0.15 | orange |
| front, below the coaster | MIDDLE 0.10 | yellow |
| front right | MIDDLE 0 | pink |
| right front, two interlaced rows of kites | KITE 0.10 (the back row), KITE 0.25 (the front row) | green, brown |

![sheets-04g-fit on the bed: the coaster in the middle, five rows of ten kites and four middle pieces round it, each labeled with its gap](sheets-04g-fit-media/bed.png)

The ids cut into the four middle pieces' bed faces, seen from below (D-109): A is the 0 gap, B
0.05, C 0.10 and D 0.15, so a middle piece tells its gap off the bed.

![The bottoms of the four middle pieces: ten-pointed pieces reading 4GF over 4 and A, B, C or D, turned on their sides](sheets-04g-fit-media/ids.png)

The coaster has room only for one letter, Z, on a strap left of the middle (D-114); it is small,
but it is the coaster's only mark. The kites have room for none; [the recipe](sheets-04g-fit.yaml)
says how they are told apart, and [the carved-id fit note](../../issues/carved-id-fit.md) says why.

![The bottom of the coaster: a ten-pointed star of straps with a small Z on a strap left of the middle](sheets-04g-fit-media/ids-coaster.png)

## Cost and risk

One bed, 78 minutes, about 21.4 g (local slice, 2026-10-07, X2D preset and PLA Basic, Textured
PEI plate, no slicer warnings, no brim, support or raft, nothing sent). One color, so no swaps.
Before the coaster was added it was 25 minutes and 5.3 g (2026-10-04).

**Risk: watch.** Fifty kites of about 0.05 cm³ each are small loose pieces, the kind that can
lift or get knocked by the nozzle. sheets-04g printed the same kites at this size without trouble.

## Your call

- [ ] **Approve as it stands**: the coaster, the five kite rungs and the four dotted middle
  pieces. Say the color with the yes.
- [ ] **Hold**: say why in the notes.

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|
| 2026-10-08 | approved | Omar, in chat, in pink | iteration 2 @ 9872c01d7d | reset 2026-10-08 |
| 2026-10-08 | approved | Omar, in chat, in pink | iteration 4 @ d99e8c88b1 in #F5547C | sent 2026-10-10 |

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-04 | proposed: the fit coupon for Omar's verdict on sheets-04g, kites at five gaps and the middle piece at four, cut along the strap's real edge (bikar #303) | [the write-up](../../issues/sheets-04g-fit.md) |
| 2026-10-04 | sliced: local slice fits one bed, 25 minutes, 5.3 g, no slicer warnings | this page |
| 2026-10-07 | changed (iteration 2): a fresh gBV minimal coaster added, and dots on each middle piece, four at gap 0 to one at 0.15, on Omar's comment on the 2026-10-06 calls page | [the calls page](../../working-model/feedback-requests/2026-10-06-open-calls.md) |
| 2026-10-07 | sliced: local slice fits one bed, 78 minutes, 21.4 g, no slicer warnings | this page |
| 2026-10-10 | sent — by `bambu print send`; spends the approval of 2026-10-08, iteration 4 @ d99e8c88b1 in #F5547C | this page |
| 2026-10-10 | printed — on the X2D, glacier plate, one bed, all 22 layers, 91 minutes against the slicer's 78; judged by hand: in the `Z` coaster the 0.05 mm kites fit and the 0.10 to 0.25 kites were too small, `4GF 4A` (gap 0) was too tight and `4GF 4B` (0.05) good but came out a little too easily, so Omar asked for a midway; `4GF 4C` and `4GF 4D` not judged; in the older sheets-04g coaster the same pieces sat about one rung looser | [the record](../../prints/2026-10-10-sheets-04g-fit/index.md) |
