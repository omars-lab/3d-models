---
plate: sheets-04g-fit
recipe: sheets-04g-fit.yaml
iteration: 1
stage: waiting
times_printed: 0
runs: []
answers: "At what gap does a kite drop into the sheets-04g coaster by hand and stay, and at what gap does the middle piece, now cut along the strap's real edge, sit without rattling?"
kind: new
maturity: experiment
bets:
  - CAL-LSE-01
unblocks:
  - "the gap per group for the next sheets-04g iteration: kites and middle piece now, the hexes, stars and outer pieces once judged"
  - "CAL-LSE-01, the loose-piece gap per face by shape in a straps-only frame"
minutes: 25
grams: 5
bed_plates: 1
risk: watch
pictures:
  - sheets-04g-fit-media/bed.png
---

# sheets-04g-fit — the kites and the middle piece at a ladder of gaps

**In short.** On [sheets-04g](sheets-04g.md) you said "the small kits were too tight ti fit" and
"adn the middle piece was too lose". Every piece there was cut at gap 0. The write-up,
[sheets-04g: the kites too tight, the middle piece too loose](../../issues/sheets-04g-fit.md),
found two different causes. The middle piece had sharp inward corners where the strap's edge
is round, which left 0.45 mm of play at each of its ten notches. The kites had no play anywhere
and the least room for error of any piece. bikar now cuts every piece along the strap's real
edge (bikar #303), so the gap is the gap all the way round. This plate prints only the two pieces you
named, at several gaps each, to press into the coaster you already have. One bed, 25 minutes,
about 5 g.

## What it is

Recipe: [sheets-04g-fit.yaml](sheets-04g-fit.yaml). The same size as sheets-04g (112.5 mm across,
3.75 mm straps, 4.4 mm tall), so the pieces fit that coaster's holes. The gap comes entirely off
the piece, so no new coaster is needed.

- **Kites, ten at each of five gaps:** 0.05, 0.10, 0.15, 0.20 and 0.25 mm per face (50 kites).
- **The middle piece, one at each of four gaps:** 0, 0.05, 0.10 and 0.15 mm per face. Its gap 0
  is not the old gap 0: it is cut along the round strap edge now, so it should no longer rattle.

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

## Pictures

The slice from above, front of the bed at the bottom. Each rung has its own color, and a label
with a line to it. The kite rungs look alike off the bed, so take one rung off at a time and bag
or mark it.

From the back of the bed to the front (the colors are the picture's, not the print's):

| Where | What | In the picture |
|---|---|---|
| the two middle pieces on the left, side by side | MIDDLE 0.15 (left), MIDDLE 0.10 (right) | orange, purple |
| the back row of kites, to their right | KITE 0.05 | amber |
| the kite row just in front of it | KITE 0.10 | blue |
| the middle piece on the right, behind the diagonal | MIDDLE 0 | green |
| the diagonal line of kites | KITE 0.25 | grey |
| the middle piece on the right, in front of the diagonal | MIDDLE 0.05 | pink |
| the second kite row from the front | KITE 0.15 | yellow |
| the front row of kites | KITE 0.20 | teal |

![sheets-04g-fit on the bed: five rows of ten kites and four middle pieces, each labeled with its gap](sheets-04g-fit-media/bed.png)

## Cost and risk

One bed, 25 minutes, about 5.3 g (local slice, 2026-10-04, X2D preset and PLA Basic, Textured PEI
plate, no slicer warnings, no brim, support or raft, nothing sent). One color, so no swaps.

**Risk: watch.** Fifty kites of about 0.05 cm³ each are small loose pieces, the kind that can
lift or get knocked by the nozzle. sheets-04g printed the same kites at this size without trouble.

## Your call

- [ ] **Approve as it stands**: the five kite rungs and four middle pieces. Say the color with
  the yes.
- [ ] **Hold**: say why in the notes.

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-04 | proposed: the fit coupon for Omar's verdict on sheets-04g, kites at five gaps and the middle piece at four, cut along the strap's real edge (bikar #303) | [the write-up](../../issues/sheets-04g-fit.md) |
| 2026-10-04 | sliced: local slice fits one bed, 25 minutes, 5.3 g, no slicer warnings | this page |
