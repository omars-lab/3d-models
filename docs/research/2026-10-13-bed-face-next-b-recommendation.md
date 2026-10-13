---
date: 2026-10-13
produced-by: Claude (research pass B of two, for what to try next on the bottom slits after bedface-4; independent of pass A). Built from the raw findings in docs/research/2026-10-13-bed-face-next-b.md. Nothing was printed or sliced for this file.
feeds:
  - docs/design/printing/bed-face-slicing-design.md
  - the next bedface plate (not yet written), after docs/design/plates/bedface-4.md
---

# Bottom slits after bedface-4: what to try next, ranked (pass B)

The question: bedface-4 found two settings that left fewer slits than stock, 55% overlap and 10%
more first-layer plastic, but every piece still slit. What else can we try? Highest expected value
first. Every claim links back to
[the raw findings](2026-10-13-bed-face-next-b.md). The plan this builds on is
[the checked plan from 2026-10-12](2026-10-12-first-layer-slits-consolidated.md).

How each item is tested, unless it says otherwise: a bed of coaster pieces like
[bedface-4](../design/plates/bedface-4.md), two pieces per setting, a stock pair beside them, each
piece with its carved id. Compare the same spot on each piece with
`python3 tools/print_review.py compare`, stock first, and Omar judges by hand.

## 1. Where the new evidence changes the 2026-10-12 plan

- **First-layer flow is proven per piece, in print.** The plan called it "not proven per piece".
  bedface-4 set it per piece, the G-code laid 1.052 times the plastic, and the print differed
  ([findings §2](2026-10-13-bed-face-next-b.md#2-bedface-4-as-recorded)).
- **A slower first layer (whole-plate step 2) should change little.** On stock `H`, the
  bottom-surface moves average 1.75 mm at an acceleration of 500 mm/s². At that length the nozzle
  peaks near 30 mm/s, so a 60 mm/s cap touches fewer than 35 of 729 moves
  ([findings §1.3](2026-10-13-bed-face-next-b.md#13-arithmetic-on-those-numbers-mine-not-measured)).
  This is my arithmetic, and it ignores how the firmware blends corners. One A1 user found 25 mm/s
  "seemed to make it worse" (forum 256070). One P-series user found slowing by half "mitigates"
  (forum 68800, layers above the first). Move it below every item here.
- **Elephant-foot compensation is back on the table, per piece.** Both 2026-10-12 passes said to
  leave it alone for the fits. One A1 mini user turned it off and wrote "That elephant foot
  compensation seemed to be the culprit" (forum 145182). It is per piece in the code. See item 4.
- **The travel extend default is 45 on the X2D, not 0.** A forum reply says 0% outside the H2
  series and P2S (forum 198663). Our X2D slice reads 45. The slice is the authority for our printer.

## 2. The ranked list

### 1. A lower first layer, −0.02 mm, under the whole bed

- **The setting:** the nozzle 0.02 mm closer on the first layer, on the glacier plate. Then
  −0.04 mm only if slits remain.
- **Per piece or plate:** whole plate.
- **Evidence (strongest here):** our gold-plate print (bedface-3) had fewer slits at 0.02 mm lower,
  though the plate's texture changed too. Two X2D users report −0.014 to −0.02 helping (2026-10-12
  plan). Three more threads point at height for first-layer gaps: "This is a issue with your first
  layer height." (Prusa forum, 2025); "the Z height is changing and you are getting different
  squish" (forum 216407, H2S); "probably his 0 is a little too high" (forum 250557, P2S). Hedges:
  none of those three reported a fix from height alone, and the 2026-10-12 plan notes one X2D user
  doubted −0.02 was the cause.
- **Transfer condition:** this carries over because the X2D's own start code already lowers the
  nozzle 0.02 mm for a Textured PEI plate, so −0.02 on the glacier is a height Bambu itself prints
  at. The forum results come from other Bambu printers and a Prusa; they carry only as far as the
  slit is a squash problem, which bedface-3 suggests and does not prove.
- **How it is applied:** not this file's call. Either slice the glacier as Textured PEI, which the
  send refuses today ([the issue](../issues/sliced-for-wrong-plate.md)), or set the printer's
  manual first-layer offset, which Omar sets and the plate page must record.
- **Risk:** no risk to the machine at −0.02 (Bambu's own textured height). −0.04 goes past any
  height Bambu's code uses; the risk is the nozzle marking the smooth plate, not damage. More squash
  may widen the bottom edge, so loose-piece fits are checked again.
- **How to test:** put the whole next bed on −0.02 (see §3). The stock pair on that bed is read
  against bedface-4's `H` and `J` photos. That is a photo-to-photo read across two prints, weaker
  than stock beside, and it is worth it because it also lets the per-piece items below ride on the
  same bed.

### 2. More overlap: 75% and 100%, on the stock `monotonic` bottom

- **The setting:** `infill_wall_overlap` 75% on one pair, 100% on another.
- **Per piece or plate:** per piece, proven (bedface-2 and bedface-4). The compose tool takes up to
  100% ([compose.ts](../../tools/bambu/src/commands/compose.ts)).
- **Mechanism:** the push is the percent times about 0.46 mm on the first layer (my arithmetic from
  [the code](2026-10-13-bed-face-next-b.md#3-bambu-studios-code)). So 55% moves the fill's edge
  about 0.25 mm outward, 75% about 0.34 mm, 100% about 0.46 mm, about one line, onto the inner
  wall's center line.
- **Evidence (medium):** in bedface-4, 55% beat 30%, and 30% split around stock: a trend, from two
  steps. OrcaSlicer uses a separate overlap on layer 1, 25% by default against Bambu's 15%, and its
  tooltip says "A value of 25-30% is a good starting point, minimizing the appearance of pinholes"
  (findings §4). At 75%, one Bambu user wrote "You can see the gap close in the preview" (forum
  86402), in the preview only. Against it: an H2S user still saw gaps at 50% (forum 216407), and a
  Prusa user saw "no improvement" at 100% before a loose belt turned out to be the cause.
- **Transfer condition:** OrcaSlicer's layer-1 push uses the same formula as Bambu's single key, so
  Bambu's overlap on layer 1 is the same lever as Orca's bottom overlap. It carries to the whole
  coaster because it acts at each spot where a fill line meets a wall, and the pieces have every
  kind of wall the coaster has.
- **Risk:** a ridge where the fill crowds the wall, on the bottom and on the top face too, because
  Bambu has one overlap for every layer. Check the top face of these pieces, not only the bottom.
  It may move a loose piece's fit. Not a machine risk.
- **How to test:** two pairs on the next bed, stock beside. Keep each alone. Do not stack 100% with
  more flow, or a ridge cannot be traced to one of them.

### 3. 55% overlap and first-layer flow 1.10 together

- **The setting:** `infill_wall_overlap` 55% and `initial_layer_flow_ratio` "1.1" on the same piece.
- **Per piece or plate:** per piece. Both keys proven in print one at a time.
- **Evidence (medium):** both left fewer slits than stock in bedface-4, on separate pieces. They
  were never on one piece. The record says so: "55% and the flow pieces were not set side by side".
  Hedge: three threads on other printers saw no fix from more flow alone (2026-10-12 plan).
- **Transfer condition:** carries to the whole coaster because both act on every first-layer line
  of the piece alike, and the piece's lines match the coaster's in width, speed and length.
- **Risk:** more plastic plus more push is the likeliest ridge maker on this list. Check both faces.
- **How to test:** one pair, beside a 55%-only pair, so the flow's share can be read.

### 4. Elephant-foot compensation off

- **The setting:** `elefant_foot_compensation` 0 (stock 0.15).
- **Per piece or plate:** per piece in the code (findings §3). Not yet tried per piece by us, and
  compose refuses the key today. Add it to compose only after a slice's read-back shows the piece
  carries 0 and stock carries 0.15.
- **Evidence (weak to medium):** one fetched "solved" for this symptom: "That elephant foot
  compensation seemed to be the culprit." (forum 145182). Hedges: that user had 0.2, not our 0.15;
  PETG, OrcaSlicer, a textured plate, an A1 mini; and slight gaps remained after. Bambu's code
  shrinks the layer-1 outline before walls and fill are made, so it gives no clear reason why the
  fill would stop short of the wall. A guess, not checked: the narrower band (about 1.6 mm against
  1.9) makes the diagonal lines shorter.
- **Transfer condition:** carries only if the slit comes from the shrunken first-layer outline, which
  nothing here shows. It is cheap to try, which is why it is on the bed.
- **Risk:** the first layer comes out about 0.15 mm wider on each side, the bump the setting exists
  to hide. Coaster pieces only. Loose pieces with fits stay at stock until a fit check.
- **How to test:** one pair on the next bed. Check the bottom edge for a lip as well as the slits.

### 5. Pressure advance: a lower K, or Flow Dynamics off with a hand-set K

- **The setting:** the 2026-10-12 plan's whole-plate step 3, unchanged in substance.
- **Per piece or plate:** whole plate.
- **Evidence (weak to medium):** a P-series user's K from 0.025 to 0.012 "eliminated almost all
  gaps" (forum 68800, layers above the first, OrcaSlicer). A P2S user lowered K with three other
  changes at once (forum 250557). Against it: in the same thread lkraus expected the fix to need a
  higher K, not lower.
- **Transfer condition:** K shapes the start and end of every line, and the slits sit at line ends.
  It carries to the X2D only if the X2D's Flow Dynamics value is off for this PLA, which no one has
  measured here.
- **Risk:** none to the machine. A wrong K shows as blobs or thin line ends.
- **How to test:** a bed of its own after item 1, the plan's way.

### 6. Walls that fill the strap: Arachne with four loops

- **The setting:** `wall_generator` arachne and `wall_loops` 4.
- **Per piece or plate:** per piece in the code (findings §3). Not tried per piece in print; compose
  refuses both keys today.
- **Evidence (weak):** "the Arachne wall generator helps somewhat" (forum 256070). Many walls with
  Arachne was suggested for first-layer holes (forum 146050), with no result reported. Our
  2026-10-10 slice put the coaster at 25.59 sq mm bare against stock's 35.98
  ([that file](2026-10-10-bed-face-slits.md)), but the plan has ranked wrong in print twice.
- **Mechanism:** with four loops a side, the walls cover most of a 3.75 mm strap, so few diagonal
  lines end at a wall. That is my reading.
- **Transfer condition:** carries only if the walls' meeting line down the strap middle closes in
  print. The rings did not close theirs (bedface-1 and 2), so this is a real doubt.
- **Risk:** the walls change every layer, so the top face looks different too. Limiting it to the
  first layer needs a height-range modifier, which compose cannot write.
- **How to test:** only after items 1 to 4, one pair, top face judged too.

### 7. Fill angle per piece

- **The setting:** `infill_direction`, for example 0 or 90 instead of 45.
- **Per piece or plate:** per piece in the code; the solid fill takes its angle from it (findings
  §3). Not tried per piece.
- **Evidence (weak):** in both overlap pairs of bedface-4 the turned piece did better (`2` over `T`,
  `P` over `L`). But the stock pair, turned and not, was not told apart, and the turned pieces also
  sat in other places on the bed.
- **Transfer condition:** the coaster has straps at many angles, so no single angle suits all of
  them. This picks the least-bad angle; it cannot remove the slits.
- **Risk:** the top face's lines turn too.
- **How to test:** only if the bed has room after items 2 to 4.

### 8. One wall on the first layer

- **The setting:** `only_one_wall_first_layer` on.
- **Per piece or plate:** per piece in the code (findings §3).
- **Evidence:** none of the 13 web pages fetched here supports it. A search summary credited it to a
  Prusa moderator, and the page it pointed to does not say it (findings §6).
- **Why it is low:** the fill still meets a wall, now the outer one. The number of line ends per
  millimeter of wall does not change. My reading.
- **Risk:** a thinner first-layer edge.

### 9. A little extra plastic after each stop

- **The setting:** `retract_restart_extra` above 0, for example 0.05 mm.
- **Per piece or plate:** whole plate.
- **Evidence:** none from outside. My own theory: `H` has 27 wipes inside its bottom, each pulls
  back and pushes the same amount back in, and a line may start thin after it.
- **Read against itself:** `H`'s notches are regular, along every strap edge. There are several
  hundred line ends and only 27 wipes. So this explains at most 27 slits, not the pattern.
- **How to test:** first, without printing, mark the 27 wipe spots on `H`'s G-code drawing and
  look at the same spots in `H`'s photo. Print only if they line up with notches.

### Looked at and dropped

- **Slower first layer:** see §1.
- **Ironing:** it works on top surfaces only.
- **Bottom density below 100%:** the code calls it a texture, "not to fix issues such as over-extrusion."
- **XY hole and contour compensation:** these move every layer and would move every fit.
- **Monotonic line with travel extend:** printed in bedface-4, about the same as stock.
- **Nozzle temperature:** last in the 2026-10-12 plan; nothing new here.

## 3. The next bed, as one proposal

Twelve pieces of the gBV coaster, the bedface-4 shape, all on −0.02 mm (item 1), on the glacier
plate:

| Pair | Setting | What it reads |
|---|---|---|
| 1 | stock | the −0.02 mm effect, against bedface-4's `H` and `J` photos |
| 2 | overlap 55% | the bedface-4 winner again, as the bridge between the two beds |
| 3 | overlap 75% | item 2 |
| 4 | overlap 100% | item 2 |
| 5 | overlap 55% and flow 1.1 | item 3, against pair 2 |
| 6 | elephant-foot 0 | item 4, needs compose to take the key first |

Turn one piece of each pair a quarter turn, as bedface-4 did, so item 7 gets a free look.

## 4. What this file assumes, not decides

- Putting the whole bed on −0.02 mm gives up a stock-beside read of the height. The alternative is
  to keep stock height and run the per-piece pairs alone. Omar's call.
- How the −0.02 mm reaches the printer (a Textured PEI slice or the printer's offset) is the send
  step's call.
- One pie slice of the coaster stands for the whole coaster, as in the 2026-10-12 plan.
- These were left unranked, since none of the pages fetched here backs them:
  - **Fill before walls** (`is_infill_first`, whole plate): the fill would land first and the walls
    after. No source, and it may move the outer edge.
  - **A thicker first layer**, 0.25 or 0.28 mm (whole plate): more plastic per line, but less squash
    at the same width, which bedface-3 suggests is the wrong way.
  - **The first-layer fan:** which fan the profile's first-layer value drives on the X2D was not
    checked.
- The arithmetic in item 2 and in §1 uses my estimate of the line spacing, not the slicer's
  printed numbers.
