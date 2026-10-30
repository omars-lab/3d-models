---
plate: cedar-stencil-1
recipe: cedar-stencil-1.yaml
iteration: 4
stage: waiting
times_printed: 0
runs: []
answers: "Can a pre-K class trace the Lebanon flag's cedar, sized to a flag that fills a sideways sheet of Letter paper, with this card?"
kind: new
maturity: experiment
bets: []
unblocks: []
minutes: 94
grams: 71
bed_plates: 1
risk: ok
pictures:
  - cedar-stencil-1-media/on-paper.png
  - cedar-stencil-1-media/pieces.png
  - cedar-stencil-1-media/bed.png
---

# cedar-stencil-1 — the Lebanon flag's cedar, as a stencil for pre-K

**In short.** You asked for a stencil of the cedar (the arz) to trace when making a landscape
Lebanon flag on ordinary printer paper, for a pre-K class. The flag fills the whole sheet turned
sideways, 11 in wide by 8.5 in tall. The plate prints a card as tall as the paper with the cedar cut
out, and the loose cedar to trace around, lying in the card's opening. The recipe is
[`cedar-stencil-1.yaml`](cedar-stencil-1.yaml) and the source is
[`LebanonCedar.scad`](../../../src/Stencils/LebanonCedar.scad). It needs one bed, about 1 h 34 m
and 71 g of PLA.

## The flag on the page

![The finished flag filling a sideways Letter sheet, with the card's outline where it sits](cedar-stencil-1-media/on-paper.png)

The flag is the whole sheet: 279.4 × 215.9 mm (11 × 8.5 in). Each red stripe is a quarter of the
height, 54 mm (2⅛ in), and the white band is half, 108 mm (4¼ in). The cedar opening's tip and
base touch the red stripes, as on the real flag, so it is 108 mm tall and, keeping the cedar's own
shape, 108 mm wide. The outline comes from Wikimedia's flag drawing (public domain),
[kept in the repo](../../../src/Stencils/Flag_of_Lebanon.svg).

This is not the official flag shape. The official flag is 2:3; a sheet is about 1.29:1. On the
official flag the cedar is a third of the flag's width, and here it is a bit more than that (39%),
because it is sized to the taller white band. The first version of this plate drew an official 2:3
flag across the sheet, 186 mm tall, with strips to trim above and below. It was changed after you
asked for a flag that fills the sheet. Setting `flag = "official"` in the source brings it back.

## The two pieces

![The card with the cedar cut out, and the loose cedar beside it (on the bed it lies in the opening)](cedar-stencil-1-media/pieces.png)

- **The card** (140 × 215.9 mm, 3 mm thick). Its top and bottom edges line up with the paper's,
  so it can only sit at the right height. To center it, fold the paper in half side to side and
  line up the two middle notches with the fold. A child traces inside the cedar opening.
  The notches on the card's sides are for the grown-up's pencil. They mark where the stripes
  start, and a ruler joins the marks across the sheet.
- **The loose cedar**, to trace around, for children who find that easier. It prints inside the
  card's opening with a 1 mm gap all round; lift it out after the print. Side by side, the two
  pieces do not fit on one bed.

Neither outline is the exact flag drawing. The exact outline has frond tips 2–3 mm wide; a crayon
(8–11 mm across) can't get into them, and on the loose piece they would snap off. So the loose
cedar is 1.5 mm fatter all round, and the opening is 2.5 mm fatter. The cedar is scaled so that the
opening, the line a child actually traces, spans the white band exactly. A tracing around the
loose cedar comes out 1 mm smaller on each side, so its tip and base fall about 1 mm short of the
stripes.

## Assumptions made

- **The flag fills the sheet**, as you asked, rather than the official 2:3. See above to switch.
- **US Letter paper.** For A4, set `paper = "a4"` in the source and re-render the STL.
- **One card and one loose cedar.** A class needs more cards; each one means printing the plate
  again.
- **No carved id.** It's a classroom tool, and an id cut into the face would show up in the traced
  line.

## On the bed

![The slicer's picture of the plate: the card, with the loose cedar in its opening](cedar-stencil-1-media/bed.png)

The slicer finds nothing to warn about and adds no brim, so nothing joins the loose cedar to the
card. Any one color works.

## After the print

| Pieces | The question | What we expect, and why | What each answer changes |
|---|---|---|---|
| The card | **Do:** Lift the loose cedar out of the opening. Turn a sheet of Letter paper sideways, fold it in half side to side and open it. Lay the card on it, its top and bottom edges flush with the paper's and its middle notches on the fold. Trace the cedar opening with a crayon, then mark the four side notches with a pencil. Lift the card and measure from the cedar's tip to the top stripe mark, and from its base to the bottom one. **Look for:** Does the crayon follow the whole outline, and do the tip and base touch the stripe marks? | The crayon follows it and both touch, since the card is sized from the paper and the opening spans the white band. | Crayon catches in the fronds: grow the opening more. Gap at the stripes: check the print for shrink before changing the source. Works: print more cards for the class. |
| The loose cedar | **Do:** Did it lift out of the opening without force? Hand it to a child (or try it yourself) and trace around it with a crayon. **Look for:** Does it stay put while tracing, and do any frond tips bend or snap? | It lifts out freely, since there is a 1 mm gap, and nothing snaps at 3 mm thick with the grown outline. | Stuck to the card: widen the gap. Slips: add a small knob to hold it by. Snaps: thicken it or grow it more. |

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-30 | proposed: on Omar's ask for a cedar stencil to trace a landscape Lebanon flag on printer paper, for pre-K; a card and a loose cedar, sliced clean | this page |
| 2026-10-30 | changed: the flag now fills the sheet (11 × 8.5 in), on Omar's question; the cedar is sized to the 108 mm white band, and the loose cedar prints in the card's opening so both fit one bed | this page, the recipe |
