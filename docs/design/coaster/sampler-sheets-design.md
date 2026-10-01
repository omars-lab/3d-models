---
status: draft
---

# Sampler sheets: decide the smooth-lines calls in the hand

> "before making the decsisions ... how can we add a design to print a sheet of different subsets
> of shapes and approaches / tehcniques for us to make the decision (or multiple sheets) ... where
> each pattern / shape subset is clearly lableled?"
> — Omar, comment on the [smooth-lines design](smooth-lines-design.md), 2026-10-01

**Status:** draft, 2026-10-01. Nothing here is built. Sheet 1 is the first one worth printing, and
it waits on two pieces of bikar work (§3). Printing stays Omar's call and stays last.

## 0. The answer in one screen

A sampler sheet is one flat card with small samples standing on it in a grid.

- **Rows** are the values of one technique: today's edge against the new edge, round 1 against
  round 1.5, and so on.
- **Columns** are shape subsets: a strap crossing, an eight-point star, a ten-point star. Each is
  a 30 mm window cut from a real 90 mm coaster at its real size.
- **Labels** are engraved into the card only: a title, a code over each column, a code beside each
  row. Nothing is engraved on a sample, so a label can never change the thing being judged. The
  values behind each code sit on the plate's review page.

Four sheets cover the [smooth-lines open calls](smooth-lines-design.md#6-open-calls-for-omar)
and the loose-pieces fit:

| Sheet | Answers | Can it be made today? |
|---|---|---|
| 1. Edge and top | call 1 (do the steps show?) and call 4 (the top) | no: needs the new edge and the window cut |
| 2. Star points | call 2 (sharp or softened) | no: needs hole-point rounding |
| 3. Soft weld | call 3 (how much SKIMS) | no: needs the soft weld |
| 4. Fit | the loose-pieces gaps (D-090) | no: needs the loose-piece output |

![Sheet 1 mockup: a 128 × 156 mm card, three columns (CS-1, CS-2, GBV) by four rows (A TODAY,
B TRUE, C DOME, D FINE), labels engraved on the card](sampler-sheets-media/sheet-1-mockup.png)

*Figure 1. A layout mockup of sheet 1, not a render: the samples are drawn as stand-ins for the
real windows. Source: `docs/design/coaster/sampler-sheets-media/sheet-1-mockup.html`.*

## 1. Why the samples must be true size

Every technique in the smooth-lines design is set in millimetres: the 0.4 mm grid, round 1 or
1.5, a 0.3–0.75 mm tip round, a 0.6–2.4 mm weld. The look of each depends on how it compares to
the strap, which is 3 mm on the 90 mm coaster.

So the existing minis do not answer these calls. A mini is the whole coaster shrunk to 80 mm with
a 2 mm strap ([sample rules](../../../.claude/skills/print-coaster-samples/sample-rules.md)); a
round of 1.5 on a 2 mm strap is a different shape from a round of 1.5 on a 3 mm strap. A sample
answers for the real coaster only when it is a piece of the real coaster: same mm per pattern unit,
3 mm strap, 4 mm tall, same grid. That is why each column is a **window** (a cut-out), not a small
whole coaster. A judgement made on a window transfers to the full coaster because nothing that the
technique depends on has changed; it does not transfer to the coaster's outer rim, which no window
shows.

One thing a sample standing on a card cannot show is the bed side: first-layer squish and the
underside. For the edge and top calls that does not matter. For the fit sheet it does, which is why
sheet 4 is laid out differently (§3).

## 2. Cutting a window out of a coaster

**What exists.** bikar can already cut a pattern down to a region: inside a pattern,
`clip pattern to <boundary>` keeps the faces inside a named boundary and drops the rest, with tests
behind it. A coaster with `outline pattern` uses the pattern's straps as the solid, so a clipped
pattern should give a clipped coaster.

**What is untried.** Nobody has run a clipped pattern through the coaster builder. The clip may
leave loose ends where a strap is cut, and the coaster's size is set from the art's span, which a
window changes. The window has to keep the 90 mm coaster's mm per unit rather than re-fit the
window to 90 mm; holding the derived `unit` param at its 90 mm value looks like the way, but that
too is untried.

**What I would build.** A small window option on the coaster (a centre and a size), so a sample is
the coaster's own file plus a few params. The other route, copying each coaster into a sample file
with a clip added, gives a second copy that drifts from the first the next time the coaster
changes (the reason behind [D-041](../../working-model/decisions-log.md)). This is bikar work and
goes through bikar's own review.

**Picking the windows.** Once per coaster, by eye from its render: the busiest crossing for CS-1,
one star with its ring of straps for CS-2 and for the ten-fold gBV coaster. The centres go in the
sheet's plate file, so a sheet can be reprinted exactly.

## 3. The sheets

Each sheet is one card, three columns by three or four rows. Sheet 1 measures 128 × 156 mm, which
fits the X2D's 256 × 256 mm bed with room to spare; two sheets side by side would need exactly
256 mm and leave no margin, so it is one sheet per plate.

**Sheet 1 — edge and top.** Columns: CS-1 crossing, CS-2 star, gBV star. Rows:

| Code | What it is | Made with |
|---|---|---|
| A TODAY | today's edge in 0.4 mm squares, round 1 | today's bikar; this is the control |
| B TRUE | edge drawn between grid points (smooth-lines option 3), round 1 | option 3, in progress in bikar |
| C DOME | the same edge, round 1.5 (the full dome) | option 3 plus a value that exists today |
| D FINE | a 0.2 mm grid, round 1 | only if the coaster language can set the grid size by then; otherwise the row is left off |

A against B answers call 1: if Omar cannot see or feel the difference, the edge work closes, as
the smooth-lines design already says. B against C answers call 4.

**Sheet 2 — star points.** Columns: CS-2 star, gBV star, CS-1 inside corners. Rows: tip round 0,
0.3, 0.75 and 1.5 mm. Waits on hole-point rounding (option 5), which is not built. The 1.5 row is
there on purpose: it is where stars turn into flowers, and seeing it is the point.

**Sheet 3 — soft weld.** Columns: CS-1 crossing, CS-2 star with its octagons, gBV star. Rows: none,
light, strong. The two smooth-lines researchers chose different amounts (one used 0.6 and 1.2 mm on
CS-2, the other 1.2 and 2.4 mm on CS-1), so if those stay unsettled the sheet carries both lights.
Waits on the soft weld (option 8), which is not built.

**Sheet 4 — fit.** Different on purpose. The card is the loose-pieces solid slab with gBV pockets
cut into it, and the pieces sit loose in them; rows are the four test gaps from the
[loose-pieces design](loose-pieces-design.md) (0.05 to 0.20 mm). Here the bed side and the snug
of a piece in a pocket are the thing being judged, so the samples cannot stand on the card. Waits
on the loose-piece output (catalog item 6).

**Not on any sheet.** The slicer wall settings (option 10) are a per-plate setting, not a shape,
so they ride along on whichever plate prints next. The mitred joins, varying width and the pillow
top come later, as looks.

## 4. Labels

The card carries three kinds of label, all engraved: the title ("EDGE AND TOP"), a column code
("CS-1", "CS-2", "GBV") and a row code ("A TODAY"). Engraved text already works on flat-topped
pieces in bikar; the Machine-Card coupons carry their names the same way.

Two limits of today's font shape the codes. It has capitals, digits, the dash and the space, and
no full stop, so "1.5" cannot be written; the row code says what the row is and the review page
says the number. And bikar refuses a label that mixes the letter O with the slashed zero, so a code
like "ROUND 0" is out; pick words that avoid the clash.

Nothing is engraved into a sample. A label cut into a sample changes its geometry right next to the
thing being judged, the same reason the text design keeps labels off coupon faces.

## 5. From the design to the plate

The card and its samples are **one printed object**: the card is one part, each sample is another
part placed at its cell. The bambu tool already builds one object out of several parts sharing one
frame for colored coasters; a sheet needs the same with a position per part. This matters because
the tool's normal packing moves loose pieces wherever they fit, which would scatter samples away
from their labels.

The card also does a safety job. A 30 mm window is a small cut-up piece with thin feet; standing on
a card it has the card's whole footprint on the bed. A small part that comes loose and gets dragged
is the kind of risk the [no-measurement-worth-the-machine rule](../../../.claude/skills/guide-print/SKILL.md) is
there to stop. Whether a sample fuses well to the card is expected but unchecked until the slice
preview shows it.

The path, in order:

1. Render each sample through bikar with the mesh check on.
2. Check the full coaster at the same settings with the smooth-lines checks: the worst gap per
   loop, `tools/edge_stairs.py` and the symmetry number. The window inherits these; it is not a
   substitute for them.
3. Put the card in a bikar coupons file, with its engraved labels.
4. Teach the bambu tool a sheet plate: one object, card plus samples at their cells.
5. Write the sheet's plate file (a new sheets-01 in docs/plates) and its review page, with the row and column legend and every
   value.
6. Compose with `--dry-run`, then the usual look (review-print) and queue (prioritize-prints).
7. Stop at the owner gate. Sending, filament and timing are Omar's.

**Validator:** the sample is true size. Compare the sample's strap width and the span of its art
against the same region of the 90 mm coaster.

PASS: a window cut with the 90 mm coaster's unit; its strap measures 3 mm and its star matches the
coaster's star.

FAIL: a sample made by shrinking the whole coaster to 30 mm (`--param size=30`); its strap and star
are a third of the size and the round no longer compares.

## 6. Open calls for Omar

Tick one box per call. My pick is first, with its reason.

**Call 1 — how are samples held and labeled?**

| | Buys | Costs | Leads to |
|---|---|---|---|
| **One piece: samples standing on a labeled card** | labels can never be mixed up; small parts are safe on the bed; nothing engraved on a sample | the underside of a sample cannot be seen; sample-to-card fusing unproven until the slice preview | a sheet plate kind in the bambu tool |
| Pockets in a card, samples loose | samples can be picked up and turned over | the packing tool scatters them; a dropped sample loses its label | a pick-and-place step by hand after printing |
| A tag on each sample | each sample carries its own name | needs text on coasters in bikar, and the tag sits next to what is judged | new bikar text work first |

- [ ] **One piece on a card.** The label can never leave the sample, and the card is what keeps a
      small piece safe on the bed.
- [ ] Pockets, loose samples.
- [ ] A tag per sample.
- Notes:

**Call 2 — what goes on sheet 1?**

| | Buys | Costs | Leads to |
|---|---|---|---|
| **Edge and top together, four rows** | two calls answered by one print | waits on option 3 and the window; row D may drop | calls 1 and 4 settle together |
| Edge only, three rows (today, true edge, fine grid) | the narrowest test of call 1 | the top needs its own print | a second small sheet later |
| Wait and print all four sheets once options 5 and 8 land | one printing session | the edge question waits on unrelated work | call 1 stays open longest |

- [ ] **Edge and top together.** A against B and B against C share columns, so one card answers
      both.
- [ ] Edge only.
- [ ] Wait for all sheets.
- Notes:

**Call 3 — how big is a sample?**

| | Buys | Costs | Leads to |
|---|---|---|---|
| **30 mm window** | a whole star with its ring of straps; 12 samples fit a 128 × 156 card | a crossing shows its neighbours only in part | sheet 1 as drawn in Figure 1 |
| 20 mm | smaller card, faster print | a ten-point star barely fits; less to hold | four columns per sheet possible |
| 45 mm | more context, closer to holding the coaster | about 175 mm wide for three columns; fewer rows per bed | sheets split across plates |

- [ ] **30 mm.** The smallest size that still shows a whole star.
- [ ] 20 mm.
- [ ] 45 mm.
- Notes:

## 7. Where this came from

- The calls being decided: [smooth-lines design](smooth-lines-design.md), §2 (options), §5 (the
  order) and §6 (the open calls).
- The fit sheet: [loose-pieces design](loose-pieces-design.md) and D-090 in the
  [decisions log](../../working-model/decisions-log.md).
- Read in bikar's `origin/main` on 2026-10-01: the coaster block's statements (no text, no window),
  `clip pattern to` in the pattern block, `text … engrave` on flat-topped pieces and its 37-glyph
  font and O/0 check.
- Read in this repo: the bambu tool's packing and its one-object-many-parts builder for colored
  coasters, and the X2D bed size.
- The mockup is HTML screenshotted headless; re-render it with the command in its header.
