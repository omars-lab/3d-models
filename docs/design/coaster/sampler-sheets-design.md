---
status: draft
---

# Sampler sheets: decide the smooth-lines calls in the hand

> "before making the decsisions ... how can we add a design to print a sheet of different subsets
> of shapes and approaches / tehcniques for us to make the decision (or multiple sheets) ... where
> each pattern / shape subset is clearly lableled?"
> — Omar, comment on the [smooth-lines design](smooth-lines-design.md), 2026-10-01

**Status:** draft, 2026-10-01. The window cut (§2), the labeled cards for sheets 1 and 5 (§4) and
the sheet plate (§5, `bambu slice sheet`) are built (bikar #293 and #294). Sheet 1 is built in
full, row A included, and waits on Omar's tick: one bed, about 1 h 48 m and 46 g. It is the first one worth printing (§3). Printing stays Omar's call and stays last. Sheets 4 and 5
and the three guided-page pictures were added the same day, after Omar asked on the
[loose-pieces design](loose-pieces-design.md) how its calls could be made "without a sheet of poc
prints for us to inspect". Each sheet has a plate page in [`docs/design/plates/`](../plates/README.md)
that waits on the build it needs.

## 0. The answer in one screen

A sampler sheet is one flat card with small samples standing on it in a grid.

- **Rows** are the values of one technique: today's edge against the new edge, round 1 against
  round 1.5, and so on.
- **Columns** are shape subsets: a strap crossing, an eight-point star, a ten-point star. Each is
  a 30 mm window cut from a real 90 mm coaster at its real size.
- **Labels** are engraved into the card only: a title, a code over each column, a code beside each
  row. Nothing is engraved on a sample, so a label can never change the thing being judged. The
  values behind each code sit on the plate's review page.

Five sheets cover the [smooth-lines open calls](smooth-lines-design.md#6-open-calls-for-omar)
and the [loose-pieces calls](loose-pieces-design.md#7-open-calls-for-omar) 3 and 4:

| Sheet | Answers | Can it be made today? | Plate page |
|---|---|---|---|
| 1. Edge and top | smooth-lines call 1 (do the steps show?) and call 4 (the top) | yes: rows B and C from bikar main (#291, #293, #294), row A from the old edge kept in this repo ([how](../../../src/Samplers/sheets-01-row-a/README.md)) | [sheets-01](../plates/sheets-01.md) |
| 2. Star points | smooth-lines call 2 (sharp or softened) | yes: hole-point rounding (`holes round`, bikar #325), fed by a `tip` knob on every minimal coaster, and its card, Sheet2Card (bikar #328) | [sheets-02](../plates/sheets-02.md) |
| 3. Soft weld | smooth-lines call 3 (how much SKIMS) | no: needs the soft weld and its card piece | [sheets-03](../plates/sheets-03.md) |
| 4. Fit | loose-pieces call 4 (the gaps, and printing it) | yes: bikar's `Loose-Fit-Coupon.bkr` (#296), on the loose pieces of #292 | [sheets-04](../plates/sheets-04.md) |
| 5. Fill height | loose-pieces call 3 (raised fills everywhere, or only as loose pieces) | two rows of three: lowered and flush exist; raised is refused | [sheets-05](../plates/sheets-05.md) |

Loose-pieces call 2, where the guided page lives, is not something to hold in the hand. It gets
three pictures instead ([§3](#where-the-guided-page-lives-three-pictures-not-a-sheet)).

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

**What was built (bikar #293, 2026-10-01).** A window option on the coaster:
`--window <side>[@<x>,<y>]` on the command line, a square of `side` mm centred on a point of the 90 mm
coaster. The sample is the coaster's own file plus that one option, so it cannot drift from the
coaster the next time the coaster changes (the reason behind
[D-041](../../working-model/decisions-log.md)); copying each coaster into a sample file with
`clip pattern to` added was the route not taken. The cut is made on the finished coaster, after
its size is set, so the window keeps the coaster's grid, its mm per unit and its place, and a
window holding the whole coaster gives the same mesh vertex for vertex. A strap the square
detaches from the rest is dropped and named. The option refuses what it cannot cut honestly:
joins, twist, a bottom edge, loose pieces, and a square edge running along a strap that would
leave a fin thinner than the floor.

**Tried on 2026-10-01**, each with the mesh check passing: a CS-1 crossing, a CS-2 star and a gBV
star on their minimal coasters; gBV at `round` 1.5 (sheet 1, row C); and the CS-2 fill coaster,
a square slab with the pattern inscribed (sheet 5), where it also splits into color parts.

**Picking the windows.** Once per coaster, by eye from its render: the busiest crossing for CS-1,
one star with its ring of straps for CS-2 and for the ten-fold gBV coaster. The centres go in the
sheet's plate file, so a sheet can be reprinted exactly.

## 3. The sheets

Each sheet is one card, three columns by three or four rows of 34 mm cells. As built, sheet 1's
card measures 138 × 122 × 1.4 mm with three rows; each further row adds 34 mm. It fits the X2D's
256 × 256 mm bed with room to spare; two cards side by side would need 276 mm, so it is one sheet
per plate. (The first sketch, Figure 1, drew four rows on 128 × 156 mm; the built card added a
32 mm row-code column on the left so the codes clear the samples, and left row D off.)

![Sheet 1 as built: the nine samples standing on their cells, rows A and B alike from above, row C's
domed straps narrower below them](sampler-sheets-media/sheet-1-samples.png)

*Figure 2. Sheet 1 as the plate assembles it, drawn from the mesh (`bambu slice sheet --stl`, then
`tools/print_review.py art`): the samples' top faces where they stand. Rows A and B differ at the
wall, not the top, so the [sheets-01 page](../plates/sheets-01.md#pictures) adds a close-up of
the bottom faces (`print_review.py edge`), and the card's own picture.*

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
0.3, 0.75 and 1.5 mm. The 1.5 row is there on purpose: it is where stars turn into flowers, and
seeing it is the point.

As built on 2026-10-07:
- **The rounding** is `holes round <mm>` (bikar #325, option 5). Every minimal coaster feeds it
  from a `tip` knob (bikar #328). At 0, the knob's default, each coaster's mesh is the same as
  before.
- **The card** is Sheet2Card, 138 × 156 mm, with rows A SHARP, B LIGHT, C MEDIUM and D STRONG.
- **The columns** follow sheet 1's order (CS-1, CS-2, gBV), so the two sheets read across.
- **CS-1's window** moved to 12,2. At 1.5 mm, sheet 1's 9.7,1 leaves a 0.07 mm sliver along the
  window's edge, and the cut refuses it.
- **The plate** is [`sheets-02.yaml`](../plates/sheets-02.yaml). It slices to one bed, 2 h 8 m
  and 58 g.

**Sheet 3 — soft weld.** Columns: CS-1 crossing, CS-2 star with its octagons, gBV star. Rows: none,
light, strong. The two smooth-lines researchers chose different amounts (one used 0.6 and 1.2 mm on
CS-2, the other 1.2 and 2.4 mm on CS-1), so if those stay unsettled the sheet carries both lights.
Waits on the soft weld (option 8), which is not built.

**Sheet 4 — fit.** This sheet is the answer to
[loose-pieces call 4](loose-pieces-design.md#7-open-calls-for-omar), and it keeps the gaps that
page proposes. Different on purpose: the card is the loose-pieces backed frame (a solid slab with
pockets, F1) for the gBV coaster, and the pieces sit loose in it. The frame prints once; only the
pieces change.

| Code | What it is |
|---|---|
| GAP 05, GAP 10, GAP 15, GAP 20 | one ring of pieces at 0.05, 0.10, 0.15 and 0.20 mm per face, the same shape at each gap |
| STAR 15 | gBV's small five-point stars at 0.15 only, to see whether the tips catch at the default |

The loose-pieces page put the four gaps on CS-1's ring 1 and the tip check on ring 5. D-090 moved
the fit sample to gBV, whose small stars it names as the hardest case, so the stars take the tip
check; which gBV ring carries the four gaps is read off `bikar bands` when the sheet is built. The
codes go on the plate page and on the bags, not on the pieces or the frame: each gap set is its own plate item and goes in its own bag straight
off the plate, because the sets look alike. Here the bed side and the snug of a piece in a pocket
are what is judged, so the pieces cannot stand on a card.

Before it can print, it needs: true edges in bikar
([D-090](../../working-model/decisions-log.md#d-090--lines-and-loose-pieces-in-two-colors-true-edges-first):
the staircase is bigger than the gap under test), then the loose-piece output (loose-pieces §6
items 2 and 3, catalog item 6). Both shipped 2026-10-01 (bikar #291, #292); what is left is the
sheet's own file and its plate. The window cut is not needed; the frame is the whole coaster.
The pieces are the smallest things we would have printed. Call 4's printer question (failure
detection on and the first layer watched) is settled: the X2D does its own failure detection, so
it is not asked per plate
([D-092](../../working-model/decisions-log.md#d-092--failure-detection-is-the-printers-job-not-a-per-plate-yes),
loose-pieces §3.7).

**Sheet 5 — fill height.** The answer to
[loose-pieces call 3](loose-pieces-design.md#7-open-calls-for-omar): lowered, flush and raised fills
side by side on the same 30 mm windows. Only the CS-2 fill coaster has a fill height today
(`7apC5Q9QS-8-fill-coaster.bkr`, `relief both emboss 1.2 fills $fill`), so all three columns are
windows of it: the centre star, a petal, an octagon. The samples print in the coaster's own colors
(gold straps, ruby and slab fills), so each sample is several color parts, not one.

| Code | What it is | Can it be made today? |
|---|---|---|
| A LOW | fills 0.6 mm, below the 1.2 mm straps (the multicolor design's lowered look) | yes: inside the preset's `range 0.2..1.2` |
| B FLUSH | fills 1.2 mm, level with the straps | yes: the preset's default |
| C HIGH | fills 1.8 mm, 0.6 mm above the straps | no: bikar's parser refuses it ("fills may be at most the relief height (equal is flush)"). Needs loose-pieces §6 item 1: lift the refusal, strap wins on height, the ramp into the fill, the feature floor counting raised fills, a wider preset range |
| D PIECE | a loose piece 1.8 mm tall standing in a 1.2 mm pocket | the piece can be made: `loose … height 1.8` (bikar #313, 2026-10-06) stands it 0.6 mm proud of a 1.2 mm pocket. The sample still waits on the sheet plate's color parts, like the rest of the sheet |

C against D is call 3 itself: if a raised fill and a tall loose piece look the same in the hand,
raised fills can come only through loose pieces and the kernel work is not needed. Row C can be
printed from a bikar branch, so the look is judged before anyone decides to merge the kernel
change. A against B is also the multicolor design's open taste call,
[flush or lowered](multicolor-design.md#3-the-look-flush-or-lowered-fills), which wanted the same
two values side by side. The window cut (§2) and the card (piece Sheet5Card, labeled STAR, PETAL,
OCTAGON and A LOW, B FLUSH, C HIGH) are built. The sheet plate (§5) is built for one color, which is
not enough here: each cell needs its color parts, which the bambu tool does for a whole colored
coaster but not yet per sample. The window cut works on this square slab too (tried 2026-10-01:
one body, mesh check passing, and `--format parts` gives a body per color).

**Not on any sheet.** The slicer wall settings (option 10) are a per-plate setting, not a shape,
so they ride along on whichever plate prints next. The mitred joins, varying width and the pillow
top come later, as looks.

### Where the guided page lives: three pictures, not a sheet

[Loose-pieces call 2](loose-pieces-design.md#7-open-calls-for-omar) is about software, so it is
decided on pictures. Each is HTML in the Coaster Lab's own colors, screenshotted headless; the
coaster in them is a stand-in drawing. Source:
`docs/design/coaster/sampler-sheets-media/guided-page-options.html`.

![Option 1: the Coaster Lab with a step bar under its header, step 2 "Loose rings" lit, only the
Orbits panel showing, and a Guided / All knobs switch](sampler-sheets-media/guided-lab.png)

*Option 1, a guided mode in the Coaster Lab.* The same page and the same share link, with a step
bar and one panel at a time; "All knobs" puts every panel back. Nothing is wired twice.

![Option 2: a separate "Assemble a coaster" page with a large preview and a numbered list of
seven steps on the right](sampler-sheets-media/guided-page.png)

*Option 2, a separate page next to the Lab.* Cleaner, with no knobs, and easier to open to people
outside later. The same panels are wired a second time unless both pages import the same modules.

![Option 3: a light document page in this repo with eight cards, one per step, each a picture of
a Lab panel](sampler-sheets-media/guided-howto.png)

*Option 3, a written how-to.* No code. You find each panel in the Lab yourself, and the pictures go
stale when a panel changes, with nothing to catch it.

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
3. Put the card in a bikar coupons file, with its engraved labels. *Built:*
   `patterns/Coupons/Sampler-Cards.bkr`, pieces Sheet1Card and Sheet5Card (bikar #294).
4. Teach the bambu tool a sheet plate: one object, card plus samples at their cells. *Built:*
   `bambu slice sheet <sheet>.yaml`. It cuts each window, stands it on its cell with the window's
   centre (not its art's) on the cell's point and its base on the card's top, checks that every
   sample is on the card and none overlaps another, writes one object with the card and each sample
   as parts, and slices it headless to check the geometry. `--dry-run` stops before assembling, and
   `--stl <file>` writes the whole sheet as one mesh to look at.
5. Write the sheet's plate file (a `.yaml` named for the sheet) beside its review page, which
   already waits at `planned`, and add the row and column legend with every value to the page.
   *Done for sheet 1:* [`sheets-01.yaml`](../plates/sheets-01.yaml), all three rows. Row A is
   three STLs kept in this repo with their hashes, since bikar main no longer draws the old edge.
6. Run `bambu slice sheet` with `--dry-run`, then the usual look (review-print) and queue (prioritize-prints).
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
- Read in bikar's `origin/main` on 2026-10-01: the coaster block's statements (no text, no window; the window
  option came later that day, bikar #293),
  `clip pattern to` in the pattern block, `text … engrave` on flat-topped pieces and its 37-glyph
  font and O/0 check; for sheet 5, the parser's refusal of fills above the relief height
  (`packages/core/src/dsl/parser.ts`) and the fill preset
  (`patterns/Constructions/7apC5Q9QS-8-fill-coaster.bkr`, `param fill = 1.2 range 0.2..1.2`).
- Sheets 4 and 5 and the guided-page pictures: the [loose-pieces design](loose-pieces-design.md)
  §2, §3.6, §3.7, §4, §5 B and §7, and the [multicolor design](multicolor-design.md) §3.
- Read in this repo: the bambu tool's packing and its one-object-many-parts builder for colored
  coasters, and the X2D bed size.
- The mockup is HTML screenshotted headless; re-render it with the command in its header.
