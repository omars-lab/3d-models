# Experiments: print a piece of the shape, not the whole shape

Read at run time by four skills: [print-model](SKILL.md) when it plans an experiment,
[prioritize-prints](../prioritize-prints/SKILL.md) when it writes an experiment plate's page,
[calibrate](../calibrate/SKILL.md) when it designs a coupon, and
[review-print](../review-print/SKILL.md) when the plate comes back. It is kept apart so it can
sharpen without the four skills changing.

## Why

The slits on the coasters' bottoms took four whole-coaster plates to narrow down
([bedface-1 to 3](../../../docs/issues/bed-face-preset-failed-in-print.md)). Each plate held one or
two coasters, each coaster one setting, and each took over an hour and a half. The coaster repeats
ten times round, so nine tenths of every coaster said again what the first tenth said. Omar,
2026-10-12: "is there a way to make a cropped version of different experiments to compare … doesn't
have to be whole coaster", and then "I don't want bare minimum kind of tiny experiments but … just
being generally more efficient".

## The rule

**When a print asks a question, print the smallest piece of the real shape that still holds what is
being tested, at its real size, and put several of them on one bed.**

1. **The piece holds the thing under test, with its neighbors.** For the bottom slits that is one
   area of the real coaster holding its straps, a star hole and part of the rim: bedface-4 cuts a
   50 mm square out of it with bikar's `window: <side>@<x>,<y>`, at the coaster's own size. It is
   not a small chip of flat bottom, which has no straps and no walls for the slits to form against. For a fit
   it is the frame round one hole with its piece, not a lone peg. Size and the params stay the
   plate's own; never scale a piece down to save time.
2. **Write why the piece answers for the whole.** One sentence on the plate page:
   *"this carries over because …"*, naming what is the same: line width, speed, the plate, the lines
   on either side. If it cannot be written, print the whole shape and say why. Things that change
   with the size of the piece do not carry over: warping and lifting, how the top looks, and
   anything set by layer time, since a small piece finishes each layer sooner and cools
   differently. The first layer carries over best, because each line is laid the same way whatever
   is round it.
3. **Several settings on one bed, a stock piece beside them.** A setting Studio takes per piece goes
   on its own piece of the same bed, through `object_settings:` in the plate recipe. Today those
   are `bottom_surface_pattern` and `infill_wall_overlap`
   ([the per-piece test](../../../docs/research/2026-10-10-bed-face-per-piece-and-bedface-1.md#1-which-of-the-three-settings-bambu-takes-per-piece)),
   and `initial_layer_flow_ratio`: on bedface-4's slice the 1.05 and 1.1 pieces laid 1.05 and 1.10
   times stock's plastic per mm on the first layer and the same as stock on the second
   (`scripts/layer_extrusion.py`). Write it as text with no trailing zero (`"1.1"`, not `"1.10"`),
   since Studio writes it back that way and the read-back compares text. Check any other key the
   same way before planning on it. Studio's arranger may turn some pieces a quarter turn; when it
   does, put stock pieces in both turns, so the turn can be read off the stock pair. Every bed carries one piece on stock, so
   each change is read against a piece printed the same day, on the same plate and spool.
4. **A setting for the whole bed gets a bed of its own, still in pieces.** The first line's width,
   the nozzle's start height, the plate, and the filament's temperature and flow apply to everything
   on the bed. Testing one takes its own print. Make that print a few pieces too. Its stock is a
   print of the same pieces on stock settings, the same day where that can be done; where it
   cannot, it is the stock piece from the last print on the same kind of plate, and the page says
   so.
5. **Not too small.** A piece that answers half the question costs a second print. Give each
   setting two pieces when the thing being judged varies from spot to spot (slits do). Keep the
   ids readable: every piece carries its carved id
   ([the sample rules](../print-coaster-samples/sample-rules.md#checks-every-plate-passes-before-the-owner-gate)).
6. **Judge the same spot on every piece.** When it comes back, cut the same spot from each piece's
   photo and lay them side by side: `python3 tools/print_review.py compare <out.png>
   "LABEL=photo@x,y,w,h" …` ([review-print](../review-print/SKILL.md), step 4). Stock goes first.

## When the whole shape is the right print

- The question is about the whole object: does it look right, does it sit flat, does it warp.
- The pieces of the answer interact across the shape: a fit that depends on every hole at once,
  or a coaster that is printed as two halves.
- A piece has already answered, and the whole is the check that it carries over before it goes on a
  plate that matters. Say on the page that it is that check.

## How a plate page shows it

The page's **Why print it** says which piece is printed and gives the sentence from rule 2. Its
**After the print** table names the pieces by their carved ids, the stock piece first.

## Round log

| Date | What changed | Why |
|---|---|---|
| 2026-10-12 | The rule, first version | The bed-face slits took four whole-coaster plates; Omar asked for pieces |
| 2026-10-12 | Rule 1: a square window of the coaster, not a pie slice; rule 3: first-layer flow per piece, and the arranger's turns | Building bedface-4: bikar's `window` cuts the square, the flow setting was proven in the G-code, and Studio turned eight of twelve pieces |
