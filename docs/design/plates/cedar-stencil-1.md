---
plate: cedar-stencil-1
recipe: cedar-stencil-1.yaml
iteration: 1
stage: waiting
times_printed: 0
runs: []
answers: "Can a pre-K class trace a correctly sized Lebanon flag cedar on a sideways sheet of Letter paper with this card?"
kind: new
maturity: experiment
bets: []
unblocks: []
minutes: 101
grams: 72
bed_plates: 1
risk: ok
pictures:
  - cedar-stencil-1-media/on-paper.png
  - cedar-stencil-1-media/pieces.png
  - cedar-stencil-1-media/bed.png
---

# cedar-stencil-1 — the Lebanon flag's cedar, as a stencil for pre-K

**In short.** You asked for a stencil of the cedar (the arz) to trace when making a landscape
Lebanon flag on ordinary printer paper, with the right proportions, for a pre-K class. This plate
prints two things: a card as tall as the paper with the cedar cut out, and the cedar on its own
to trace around. The recipe is [`cedar-stencil-1.yaml`](cedar-stencil-1.yaml) and the source is
[`LebanonCedar.scad`](../../../src/Stencils/LebanonCedar.scad). It needs one bed, about 1 h 41 m
and 72 g of PLA.

## The flag on the page

![The finished flag on a sideways Letter sheet, with the card's outline where it sits](cedar-stencil-1-media/on-paper.png)

The flag is 2:3 and spans the full width of a sideways US Letter sheet: 279.4 × 186.3 mm. That
leaves a 14.8 mm strip above and below to trim off. Each red stripe is a quarter of the flag's
height and the white band is half. The cedar is a third of the flag's width (93 mm), and its tip
and base touch the red stripes, as on the real flag. The outline comes from Wikimedia's flag
drawing (public domain), [kept in the repo](../../../src/Stencils/Flag_of_Lebanon.svg).

## The two pieces

![The card with the cedar cut out, and the loose cedar](cedar-stencil-1-media/pieces.png)

- **The card** (140 × 215.9 mm, 3 mm thick). Its top and bottom edges line up with the paper's,
  so it can only sit at the right height. To center it, fold the paper in half side to side and
  line up the two notches with the fold. A child traces inside the cedar opening.
  The slits are for the grown-up's pencil. The outer pair marks where to trim the flag. The
  inner pair marks the stripe lines; they stop short of the cedar so a crayon in the opening
  doesn't run into them. Join the marks with a ruler.
- **The loose cedar**, to trace around, for children who find that easier.

The cedar is drawn 1.5 mm fatter all round than the flag's outline. The exact outline has frond
tips 2–3 mm wide; a crayon (8–11 mm across) can't get into them, and on the loose piece they
would snap off. Set `grow = 0` in the source for the exact outline.

## Assumptions made

- **US Letter paper.** For A4, set `paper = "a4"` in the source and re-render the STLs; the flag is
  then 297 × 198 mm.
- **One of each piece.** The card takes most of the bed, so a second card means printing the plate
  again. Loose cedars are small: a plate of only those could hold several (`count` in the recipe).
- **No carved id.** It's a classroom tool, and an id cut into the face would show up in the traced
  line.

## On the bed

![The slicer's picture of the plate](cedar-stencil-1-media/bed.png)

The slicer turns the card to fit and finds nothing to warn about. Any one color works.

## After the print

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| The card | **Do:** Turn a sheet of Letter paper sideways, fold it in half side to side and open it. Lay the card on it, its top and bottom edges flush with the paper's and its notches on the fold. Trace the cedar opening with a crayon, then mark the four slits with a pencil. Lift the card and measure the flag from the top trim mark to the bottom one. **Look for:** Does the crayon follow the whole outline, and does the flag measure 186 mm tall? | The crayon follows it and the flag is 186 mm, since the card is sized from the paper and the cedar is grown 1.5 mm for crayons. | Crayon catches in the fronds: grow the cedar more (`grow` 2.5). Height off: check the print for shrink before changing the source. Works: print more cards for the class. |
| The loose cedar | **Do:** Hand it to a child (or try it yourself) and trace around it with a crayon. **Look for:** Does it stay put while tracing, and do any frond tips bend or snap? | It holds and nothing snaps at 3 mm thick with the grown outline. | Slips: add a small knob to hold it by. Snaps: thicken it or grow it more. |

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-30 | proposed: on Omar's ask for a cedar stencil to trace a landscape Lebanon flag on printer paper, for pre-K; a card and a loose cedar, sliced clean | this page |
