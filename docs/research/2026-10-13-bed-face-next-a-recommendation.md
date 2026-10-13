---
date: 2026-10-13
produced-by: research pass A, Claude subagent (one of two independent passes; it did not read pass B)
feeds:
  - docs/design/printing/bed-face-slicing-design.md (the bed-face design)
  - the next bedface plate
---

# What to try next for the slits on the coaster bottoms (pass A's ranking)

The short answer: push the fill further into the wall, with a little more plastic, on the next
test bed. Before that print, spend an hour on two free checks: clean the plate properly, and find
out whether the slits follow the strap direction. Then move to the whole-plate steps, starting
with a lower first layer.

The evidence for every item is in [the pass A raw findings](2026-10-13-bed-face-next-a.md). This
file builds on [the merged research from 2026-10-12](2026-10-12-first-layer-slits-consolidated.md)
and [the bedface-4 print](../prints/2026-10-13-bedface-4/index.md).

## How to test each item

Use the bedface-4 layout: pieces of the gBV coaster on the glacier plate, every test setting on
its own piece, and a stock piece beside them. "Stock" means the slicer's own settings, with no
change.

Two changes to how bedface-4 was laid out:

- **Pair every setting, one piece turned and one not.** Bambu Studio's arranger turned some pieces
  a quarter turn, and in both overlap pairs the turned one did better. Our compose tool cannot stop
  the arranger. So record each piece's turn on the plate page, and judge a setting by both of its
  pieces, not by the better one.
- **Keep two stock pieces, one turned and one not**, for the same reason.

Judge by hand, by the carved id on each piece, as bedface-4 was judged. Count slits per piece, and
note which straps they sit on.

## The ranked list

### 1. Push the fill further into the wall, with 10% more plastic

- **Settings:** `infill_wall_overlap` at 75% and at 100%, each with `initial_layer_flow_ratio` at
  1.1. Repeat 55% with 1.1 as the anchor that ties this plate to bedface-4. So three settings, each
  on a turned and an unturned piece, plus the two stock pieces: eight pieces.
- **Per piece or per plate:** per piece. Our compose tool accepts both keys today, so no tool
  change is needed.
- **What it does:** the overlap moves the fill's edge into the wall loop. By my estimate (not
  measured), 75% reaches about 0.34 mm into it and 100% about 0.46 mm, a full first-layer line.
  More plastic makes each line wider.
- **Evidence:** medium, mostly our own.
  - bedface-4 showed 55% beat 30% with no ridge, and 1.10 flow beat 1.05.
  - On a Prusa, overlap "50%+" was the only workaround one user found (fetched).
  - In Bambu Studio, 75% closed a gap in one user's preview only (fetched).
  - On an H2S, 50% did not fix a gap tied to one side of the bed (fetched).
  - Nobody I found printed 75% or 100% on a first layer and reported the result.
- **Transfer condition:** bedface-4's result transfers because it is this printer, slicer,
  filament, plate and part. The outside cases transfer only in kind: the same gap between fill and
  wall on a first layer. Their slicers and parts differ.
- **Risk:** too much plastic at the fill's edge can raise a ridge on the bottom, or push the outer
  wall out and tighten the fits of loose pieces. bedface-4 showed no ridge at 55% with flow 1.0;
  1.1 with 100% has never been tried. Check the bottom face for a ridge, and test-fit a 100% piece
  against its neighbor before using it on a whole coaster.

### 2. Clean the plate and check the bed before each test plate

- **Settings:** none. Wash the glacier plate with dish soap and water, rinse and dry it, and run
  the printer's bed leveling before the plate.
- **Per piece or per plate:** per plate. It belongs on every plate from now on, not as a test of
  its own.
- **What it does:** a fill line that sticks at once is less likely to be dragged away from the wall
  at a turn. This is my reasoning; no source tests it for gaps at the wall.
- **Evidence:** weak. A Bambu forum post says "99% of the time" adhesion trouble is plate cleaning
  (snippet only, about parts not sticking, not about slits). One P2S reply suggests calibrating and
  cleaning (fetched, not reported tried). The merged research found one H2S user whose fix was
  leveling plus calibration before each print.
- **Transfer condition:** it transfers if our slits come in part from lines not sticking. If they
  come only from where the slicer stops the lines, it will not help.
- **Risk:** none to the printer. It does make the next plate's stock pieces not quite comparable
  with bedface-4's, so compare within the plate.

### 3. Check, for free, whether the slits follow the strap direction

- **Settings:** none yet. Two checks, no print:
  1. Sort the twelve bedface-4 photos by strap direction. If the slits sit mostly on straps that
     run near the fill direction (45° on the bed), the joining rule below is likely acting. If they
     sit on one side of the bed, a bed or height cause is more likely.
  2. Slice one piece with `infill_direction` at 0°, 45° and 90°, and draw each first layer with
     `tools/print_review.py paths`. Count the line ends that do not join along the wall.
- **What it would show:** the slicer joins two fill lines by a short run along the wall only when
  that run is three line spacings or less. My reading of the code is that this fails where a strap
  edge runs within about 19.5° of the fill direction. Those line ends stop on their own, which is
  where a slit is most likely.
- **Per piece or per plate:** the setting is per piece in the slicer, but our compose tool does not
  accept it yet. If the checks point this way, compose needs the key added, with proof that the
  key shows on that piece in the sent file and not on the stock piece.
- **Evidence:** the code only, plus the turned-piece pattern on bedface-4. None of the 11 pages I
  fetched ties first-layer slits to the fill angle.
- **Transfer condition:** this acts per strap direction. If the ten-fold coaster's strap edges run
  in ten directions 18° apart (I did not measure this), then at any fill angle two or three
  directions sit inside the 19.5° limit. The best angle moves one direction out of ten. So it can
  move slits, and perhaps cut them a little; it cannot remove them on the whole coaster.
- **Risk:** none for the checks. A changed fill angle also changes how the bottom looks under
  light, which is a taste call for Omar.

### 4. A lower first layer

- **Settings:** the plate's Z offset at −0.02 mm, then −0.04 mm, as the merged research planned.
- **Per piece or per plate:** per plate. Test it on a plate of only stock settings, laid out like
  bedface-4, and compare its pieces with bedface-4's stock pieces.
- **Evidence:** the strongest outside support of any lead, and still not a fix on its own. The
  merged research gathered it. One more user, on a Prusa, found lowering Z gave "some positive
  effect but did not fully close the gaps" and made the first layer's top rough (fetched). Another
  Prusa reply says closer is the fix, with no outcome (fetched).
- **Transfer condition:** it transfers if our first layer is under-squashed. The X2D levels its own
  bed, so the offset adds to what it measures; whether 0.02 mm is a real step on this printer is
  not known.
- **Risk:** too low a first layer roughs the bottom and can leave a raised lip at the edge, which
  hurts fits. Small steps only. Anything that drives the nozzle into the plate is out.

### 5. Pressure advance set by hand

- **Settings:** run Bambu's flow dynamics calibration (it measures the factor K) for this PLA on
  this nozzle, then send a plate with that K set by hand instead of the automatic one.
- **Per piece or per plate:** per plate (per filament).
- **What it does:** pressure advance eases the pressure before a turn or a stop. Set too high, it
  starves the line just before the turn. Our slits sit where fill lines turn or stop at the wall.
- **Evidence:** weak. One P2S user dropped K from 0.12 to 0.02 and saw fewer gaps, but changed
  three other settings at the same time (fetched). Klipper's guide says too high a value gives
  "poor extrusion leading up to the corner" (fetched, different firmware). A Voron forum post
  says gaps mean the value is too high (snippet only).
- **Transfer condition:** it transfers only if our K is too high now. We do not know what K the
  printer uses on the first layer, so the calibration comes first.
- **Risk:** none to the printer. A K too low leaves blobs at corners.

### 6. The zig-zag bottom pattern

- **Settings:** `bottom_surface_pattern` set to `rectilinear` ("zig-zag" in the slicer) on one
  pair.
- **Per piece or per plate:** per piece in the slicer. Compose does not accept this value yet, so
  slice it first and look at the first layer with `tools/print_review.py paths` before changing
  any tool.
- **What it does:** like the stock pattern, it joins lines along the wall, but it does not force
  every line to run the same way. My guess is that it may leave fewer lone line ends on narrow
  straps. Untested.
- **Evidence:** weak and mixed. A Prusa user "changed the pattern" and saw "some additional
  improvement", without naming it (fetched). A Cura post says linked lines leave small gaps at
  sharp corners (snippet only).
- **Transfer condition:** it transfers only if the slice shows fewer unjoined line ends than stock
  on the coaster's straps.
- **Risk:** the bottom's sheen will look less even than the stock one, a taste call.

### 7. A slower first layer, then 225 °C

- **Settings:** first layer 30 mm/s and first-layer fill 60 mm/s, as the merged research planned;
  then the nozzle at 225 °C on the first layer.
- **Per piece or per plate:** per plate.
- **Evidence:** weaker than when the merged research ranked it. Two more users slowed down with no
  fix; on an A1 mini, slowing to 25 mm/s "made it worse" (fetched). An X1C reply says the default
  speeds work once the filament is calibrated (fetched).
- **Transfer condition:** it transfers if our lines are too fast to stick at the turns. Those two
  users suggest that is not the usual cause.
- **Risk:** none to the printer. Slower plates take longer.

## Set aside, with the reason

| Lead | Why not now |
|---|---|
| Lay the fill first (`is_infill_first`) | Bambu Studio always lays the walls first on the first layer |
| Gap-fill speed | Gap fill on the first layer already runs at the first-layer speed |
| The monotonic-line pattern and its travel extend | bedface-4: it only moved the slits |
| Arachne or more walls | It cut planned gaps less than overlap did, was worse on the middle piece, and is close to the ring bottoms we dropped |
| A narrower first line | No difference in print |
| Elephant-foot compensation | Shrinks the walls and the fill together, and puts fits at risk |
| `wall_sequence`, `only_one_wall_first_layer` | No source, and the fill still stops at a wall loop either way |
| A 0.2 mm nozzle | A hardware change, slower, and it changes every line. Omar's call |
| OrcaSlicer's gap fill on the bottom | A different slicer, so a different print pipeline |

## What this file assumes, not decides

- **That the coaster keeps its bottom face down.** Printing it flipped, or adding a first layer
  that is sanded or covered, would change the question. That is a design call, not a slicer one.
- **That a few slits may still be acceptable.** No source here, and no print so far, removes them
  all. Where the line sits between "good enough to sell" and "not" is Omar's call.
- **That the gBV strap edges run in ten directions 18° apart.** Item 3 rests on it, and I did not
  measure it.
- **That a test piece stands for the whole coaster.** It holds for the overlap and flow settings.
  For the fill angle, it may not (item 3).
- **That the arranger's turns are random enough to pair.** If compose gains a way to fix each
  piece's turn, use it and drop the pairing.
- **That my millimeter estimates for the overlap are close.** They come from reading the code,
  with every first-layer line 0.5 mm wide. A slice measurement would settle them.
- **The order of the whole-plate steps.** I kept the merged research's order and moved the slower
  first layer down. It does not decide whether the next plate is a per-piece plate (item 1) or a
  whole-plate one (item 4); I recommend item 1 first because compose can already build it.
