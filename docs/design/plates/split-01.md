---
plate: split-01
recipe: split-01.yaml
iteration: 2
stage: approved
times_printed: 0
runs: []
answers: "Does a split gBV coaster close over its loose pieces and hold them by a lip on each face, with the pieces dropped in at a loose gap and the halves lined up by studs?"
kind: new
maturity: experiment
bets: []
unblocks:
  - "D-100: lip or flange, which way a split coaster holds its loose pieces (with split-02)"
  - "split design plan item 4: whether a whole gBV split closes flat and holds"
minutes: 89
grams: 30
bed_plates: 1
risk: watch
pictures:
  - split-01-media/opened.png
  - split-01-media/how-it-holds.png
  - split-01-media/bed.png
---

# split-01 — the split gBV coaster that holds its pieces under a lip (option A)

**In short.** You asked, for the split coaster's call 6, "i want a olate hat tries a and c ...
these shoukd be different options in coaster lab". This is A, the lip. The gBV coaster at the size
sheets-04g printed is cut flat through the middle into two halves. Each half's holes are a little
narrower at its outer face, so a piece dropped into the lower half cannot fall through, and the
upper half closes over it. C, the flange, is [split-02](split-02.md). The plate is
[`split-01.yaml`](split-01.yaml). One bed, 89 minutes, about 30 g, in the color you pick
when you say yes.

## What it is

- **The two halves.** The gBV minimal coaster (gBV_JTt3Kxk), 112.5 mm across, 3.75 mm straps,
  4.4 mm tall when closed, cut at half its height. Both halves print face down, so both faces of
  the closed coaster are bed faces.
  - LOWER: the lower half, with its studs standing up on the cut face (1)
  - UPPER: the upper half, with the sockets for the studs (1)
- **The lip.** Every hole is 0.8 mm narrower all round for the first 0.6 mm in from each face. The
  lip is the first three layers of each half, laid on the bed.
- **Its 31 pieces**, plain blocks 3.2 mm tall, 0.25 mm smaller than their holes on every side, so
  they drop in. They sit 0.6 mm in from each face, under the lips.
  - MIDDLE: the twenty-sided piece in the middle (1)
  - KITE: the small four-sided kites (10)
  - HEX: the inner ring of six-sided pieces (10)
  - OUTER: the outer ring of six-sided pieces (10)
- **The stars stay open holes**, as in the minimal coaster. A star's hole made 0.8 mm narrower all
  round closes up its arms, so there would be no star to see; bikar refuses a lip that does that.
  The flange version holds the stars too.
- **Studs** 2 mm across, at least 25 mm apart, on the lower half, so the halves line up.
- **Its id, 1** (iteration 2, on your comment of 2026-10-06: "every proptoty should have an id"),
  so it can be told from split-02 and every later prototype. The cut faces are mostly pocket, so
  the id is cut 2.5 mm tall into the lower half's bottom face, the face the coaster stands on,
  mirrored so it reads the right way round when you turn the coaster over. At 112.5 mm the lip
  coaster has room for any id from 1 to 9.

**The color is picked at the send**, as on sheets-04g: say it with the yes ("yes, in pink").

**What I assumed, for you to change:**

- **Two plates, not one.** You asked for "a plate". Each coaster's halves are about 113 mm across,
  and four of them fill the 256 mm bed with no room for pieces, so A and C are a plate each.
- **The bikar defaults:** lip 0.8 mm wide and 0.6 mm thick, gap 0.25 mm, no extra room above the
  pieces. They come from the [split design §11.2](../pieces/split-with-studs-design.md#112-how-it-is-built),
  and the print is what tests them.
- **No glue.** Whether the halves are glued is call 3 of the split design, still open. Pressed
  together, the studs hold them.

## Why print it

It is the first print of a split coaster. It answers whether the pieces drop in, whether the upper
half closes over them, whether the studs line the halves up, and how the lip looks: the straps read
0.8 mm wider from each face, and the pieces sit in a little.

## Pictures

Opened up: the lower half with its studs, the pieces lifted over their holes, and the upper half
above them. Drawn by bikar and OpenSCAD from the coaster file, with the pieces' packing taken out
so each sits over its own hole (`tools/cookbook_render.py --file`).

![The split lip coaster opened up: the lower half with studs at the bottom, colored pieces floating above their holes, the upper half above them](split-01-media/opened.png)

How the lip holds, on the cookbook's small star: the piece is narrower than the hole at each face.

![A small star coaster split, lower half, pieces and upper half, the lip version](split-01-media/how-it-holds.png)

The slice: both halves on the right, the HEX and OUTER rows at the left with the kites beside them, the middle piece between.

![split-01 on the bed](split-01-media/bed.png)

## Cost and risk

One bed, 89 minutes, about 30 g (local slice, 2026-10-05, X2D preset and PLA Basic, sliced
for the Textured PEI plate Bambu Studio has saved, no slicer warnings, nothing sent). One color, so no swaps.

**Risk: watch.** The kites are small loose pieces, the kind that can lift or get knocked by the
nozzle. The lips are three layers thick; a piece pushed in hard could snap one, which is a
cosmetic loss, not one for the printer.

## Your call

- [ ] **Approve as it stands** — say the color with the yes
- [ ] **Hold** — say why in the notes

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|
| 2026-10-07 | approved | Omar, tick on the 2026-10-06 calls page: "Yes, after spl-1, in pink" | iteration 1 @ d0e7506f93 | reset 2026-10-07 |
| 2026-10-08 | approved | Omar, in chat, in pink | iteration 2 @ fcdbac0237 | |

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| 2026-10-05 | proposed — at Omar's ask, option A of the split design's call 6, beside split-02 (C) | this page |
| 2026-10-05 | sliced — local slice against bikar #305, fits one bed, 89 minutes, 30 g, no slicer warnings | this page |
| 2026-10-07 | changed (iteration 2): its id, 1, cut into the lower half's bottom face, on Omar's comment on the 2026-10-06 calls page (bikar #323); the yes in pink given before it is reset | [the calls page](../../working-model/feedback-requests/2026-10-06-open-calls.md) |
| 2026-10-07 | sliced — local slice from bikar main after bikar #323, fits one bed, 89 minutes, 30 g, no slicer warnings; the id did not change the time | this page |
