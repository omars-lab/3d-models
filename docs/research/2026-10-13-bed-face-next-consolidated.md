---
date: 2026-10-13
produced-by: checker, Claude subagent (Claude Opus 5.5), consolidating research passes A and B on what to try next for the bottom slits after bedface-4. All four pass files were read in full. Every load-bearing claim was checked by re-opening its source. That meant Bambu Studio's code at tag v02.08.02.61, OrcaSlicer's code at 0dd4b98, eleven forum threads, the bedface-4 slice (its settings and G-code), the compose tool, and the bedface-4 print record. Nothing was printed for this file, and no new slice was made.
feeds:
  - docs/design/printing/bed-face-slicing-design.md
  - the next bedface plate (not yet written), after docs/design/plates/bedface-4.md
---

# Bottom slits after bedface-4: the two research passes, checked and merged

The question: on the X2D (0.4 mm nozzle, PLA Basic, 0.20 mm layers, Bambu Studio), the coaster
bottoms show short dark slits along the strap edges. These are spots where the first-layer fill
lines stop short of the wall loops. bedface-4 found two settings that left fewer slits than stock:
55% overlap and 10% more first-layer plastic. Every piece still slit. What else can we try?

This file is built from four files, all on master:

- Pass A: [the raw findings](2026-10-13-bed-face-next-a.md) and
  [its ranking](2026-10-13-bed-face-next-a-recommendation.md).
- Pass B: [the raw findings](2026-10-13-bed-face-next-b.md) and
  [its ranking](2026-10-13-bed-face-next-b-recommendation.md).

It builds on [the checked plan from 2026-10-12](2026-10-12-first-layer-slits-consolidated.md), the
[bedface-4 plate page](../design/plates/bedface-4.md) and
[the bedface-4 print record](../prints/2026-10-13-bedface-4/index.md). This file is the one to act
on. The four pass files stay as the record it was built from.

Two slicer words come up throughout:

- **Overlap** (`infill_wall_overlap`) is how far the slicer pushes the edge of the fill into the
  wall loops, given as a percent.
- **Turned** means Bambu Studio's arranger rotated a piece a quarter turn to fit it on the bed.

## 1. What I re-opened, and what it said

Each row is a claim that changes what gets printed. "Confirmed" means I opened the source and it
says this. "Contradicted as worded" means the source says something narrower or different from
how the pass put it. "Second-hand" means the claim rests on someone else's report that I could
not check further. "Not re-opened" means I could not open it, or there was nothing to open.

| Claim | Who made it | Source I re-opened | Verdict |
|---|---|---|---|
| "Lay the fill first" (`is_infill_first`) cannot change the first layer | A (B left it unranked) | [GCode.cpp L5465-5467](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L5465): "for first layer, we always print wall firstly", and the test `is_infill_first && !first_layer`. The second copy at [L5762](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L5762) has the same test | Confirmed. B's "may move the outer edge" is moot on layer 1 |
| First-layer gap fill already runs at the first-layer speed, and the bottom fill at the first-layer fill speed (105 mm/s) | A | [GCode.cpp L7283](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7283) (bottom surface) and [L7334-7338](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7334) (every other first-layer role gets `initial_layer_speed`) | Confirmed. A's link to L7291 is one line off. The gap-fill line is L7292 |
| On a solid fill, two line ends are joined by a run along the wall only if that run is at most three line spacings | A | [Fill.cpp L697-698](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/Fill.cpp#L697) (`link_max_length = 3. * f->spacing` above 80% density). [FillRectilinear.cpp L1253-1263](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/FillRectilinear.cpp#L1253) marks longer runs too long | Confirmed in the code. A's step to "fails within about 19.5° of the fill direction" is correct arithmetic (the sine of 19.5° is one third). It has not been tested in a slice |
| The gBV strap edges run in ten directions 18° apart, so a quarter turn maps them onto themselves | A, flagged by A as not measured | Nothing to open. The arithmetic holds: 90° is five steps of 18° | Not re-opened. The slice doubts it for three pairs (§2, "found only by this check") |
| The overlap moves the fill's edge by the percent times about 0.46 mm: 55% about 0.25 mm, 75% about 0.34 mm, 100% about 0.46 mm | A and B | [PerimeterGenerator.cpp L1389-1401](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PerimeterGenerator.cpp#L1389): `infill_peri_overlap` is the percent times half a wall spacing plus half a fill spacing. [PrintConfig.cpp L3953-3960](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.cpp#L3953): default 15%, no upper limit | The formula is confirmed. The millimeters are both passes' estimate from a 0.5 mm line, not read from a slice |
| The overlap acts on every layer, so the top face gets it too | A and B | Same code: no test for the layer | Confirmed |
| Which keys are per piece and which are whole plate | A and B | [PrintConfig.hpp](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L946): the per-object group starts at L946 and the per-region group at L1062, both per piece. The whole-plate groups start at L1219 and L1402 | Confirmed. B read master (47a13ee), not the tag. The substance is the same at the tag |
| Elephant-foot compensation shrinks the first-layer outline before walls and fill are made, per piece, and only with no raft | A and B | [PrintObjectSlice.cpp L1232-1268](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintObjectSlice.cpp#L1232) | Confirmed. Walls and fill shrink together, which is A's reason to set it aside |
| The fill angle comes from `infill_direction`, a per-piece setting | A and B | [Fill.cpp L252](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/Fill.cpp#L252) | Confirmed |
| The compose tool takes only three per-piece keys: bottom pattern, overlap (0 to 100%) and first-layer flow (0.8 to 1.2) | A and B | [compose.ts](../../tools/bambu/src/commands/compose.ts), `OBJECT_SETTINGS` near L307 | Confirmed. Elephant foot, fill angle, wall generator and wall count each need a new key first |
| First-layer flow is proven per piece, in print | B | The plate page: `U`, `W` laid 1.05 times stock on layer 1, `X`, `Y` 1.10 times, and every piece the same on layer 2. The print record: in Omar's words, `X` and `Y` had fewer slits than `J` | Confirmed. This changes the 2026-10-12 plan, which called it "not proven per piece" |
| The stock values in the bedface-4 slice (first line 0.5 mm, elephant foot 0.15, overlap 15%, fill angle 45, travel extend 45%, first-layer acceleration 500, first-layer speeds 50 and 105, pressure advance left to Flow Dynamics) | B | The bedface-4 slice's project settings | Confirmed. One more: the stock top pattern is already `monotonicline` (§2) |
| `H`'s first-layer bottom has 729 moves, 1.75 mm long on average, with 27 wipes inside it | B | The bedface-4 slice G-code, object `H`, layer 1 | Confirmed: 730 moves by my count, a mean of 1.75 mm, and 27 wipes |
| At 500 mm/s², a 60 mm/s cap on the first layer touches fewer than 35 of those moves | B (its own arithmetic) | Same G-code. A move must be at least 7.2 mm long to reach 60 mm/s at that acceleration | Confirmed: 19 of 730 moves are that long. As B says, this ignores how the firmware blends corners, and it says nothing about walls |
| OrcaSlicer has its own overlap for the first layer, 25% by default, and its tooltip calls "25-30%" a "good starting point" | B | [Orca PrintConfig.cpp L4944](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PrintConfig.cpp#L4944) and [PerimeterGenerator.cpp L2028-2033](https://github.com/SoftFever/OrcaSlicer/blob/0dd4b98604ab4774d93b33b0a758523ee979f431/src/libslic3r/PerimeterGenerator.cpp#L2028-L2033) | Confirmed in the code. But the tooltip's advice is about the top solid fill and pinholes. It does not carry to the bottom face without saying why |
| At 75% overlap, "You can see the gap close in the preview" | A and B | [Forum 86402](https://forum.bambulab.com/t/filling-the-gap-between-outer-wall-and-archimedean-infill/86402) | Confirmed. Preview only, never printed, and the thread does not say which face |
| An H2S user still saw the gap at 50% overlap | A and B | [Forum 216407](https://forum.bambulab.com/t/h2s-issue-where-infill-meets-perimeter-at-front-of-print/216407): "I have tried at 50% and the issue is still there" | Confirmed. The gap sat on one side of the bed, a reply blamed "the Z height is changing", and no fix was reported |
| On a Prusa, "50%+" overlap was the one workaround, and a lower first layer helped only partly | A | [Prusa forum, "low density on first layer"](https://forum.prusa3d.com/forum/prusaslicer/low-density-on-first-layer/): "some positive effect but did not fully close the gaps" | Confirmed |
| On a Prusa, 100% overlap gave "no improvement", and a loose Y belt turned out to be the cause | B | [Prusa forum, "gap between infill and perimeters"](https://forum.prusa3d.com/forum/prusaslicer/gap-between-infill-and-perimeters/) | Confirmed, on "the first few layers". This makes A's "Nobody I found printed 75% or 100% on a first layer and reported the result" contradicted as worded |
| Slowing to 25 mm/s "seemed to make it worse", and "the Arachne wall generator helps somewhat" | A and B | [Forum 256070](https://forum.bambulab.com/t/need-help-please-small-gaps-on-first-layer/256070) | Both quotes confirmed. The Arachne line is one replier's view. The poster said "i will try again with arachne" and never reported back |
| Two more users slowed down with no fix | A | [Forum 67327](https://forum.bambulab.com/t/small-gaps-in-first-layers/67327) | Contradicted as worded. The X1C poster tried 25 and 50 mm/s and flow 1.08, but reported no result either way |
| Pressure advance (K) from 0.025 to 0.012 "eliminated almost all gaps" | B | [Forum 68800](https://forum.bambulab.com/t/gap-between-infill-and-inner-wall/68800) | Confirmed, but it is weaker than B says. The source says the first layer "consistently adheres well", and top and bottom were "always perfect, even with the wrong K-Factor". So the source rules out our face. Flow 1.1 and overlap 25% did nothing there |
| A P2S user made four changes at once and got a better first layer | A and B | [Forum 250557](https://forum.bambulab.com/t/fixing-first-layer/250557): K 0.12 to 0.02, Z offset −0.02 to 0.03 "so the nozzle is closer to the plate", first-layer flow 1.05, Arachne, gap-closing radius 0 | Confirmed. A replier (lkraus) expected the fix to need "higher K values", the other way |
| "That elephant foot compensation seemed to be the culprit" | B | [Forum 145182](https://forum.bambulab.com/t/first-layer-walls-separating-from-infill/145182) | Confirmed as worded, with its "seemed". Not in B's hedges: the same poster also changed flow, K, one wall on the first layer and the top line width. It was PETG on an A1 mini in OrcaSlicer, and slight gaps remained |
| The travel extend defaults to 45% only on the H2 series and the P2S, 0% elsewhere | B | [Forum 198663](https://forum.bambulab.com/t/please-add-percentage-setting-for-overlap-of-top-layer-walls/198663) | Confirmed. The post names no X2D. Our slice reads 45%, and the slice is the authority for our printer |
| More walls with Arachne, or more first-layer flow, was suggested for first-layer holes | B | [Forum 146050](https://forum.bambulab.com/t/holes-in-first-layer/146050) | Confirmed. No result was reported for any suggestion |
| "This is a issue with your first layer height." (Prusa forum, 2025) | B | The ["help with gaps" thread](https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-how-do-i-print-this-printing-help/help-with-gaps): the page I got showed only the question, with no replies | Not re-opened. Flagged: it may sit on a page I could not load |
| Arachne with four walls cut the planned gaps less than 30% overlap did, and was worse on the middle piece | A | [The 2026-10-10 slice](2026-10-10-bed-face-slits.md): the coaster at 25.59 sq mm bare (stock 35.98, 30% overlap 19.79), the middle piece 0.69 (stock 0.41) | Confirmed |
| "99% of the time" first-layer trouble is plate cleaning | A | Forum 67165, snippet only in A | Not re-opened. And it was about parts not sticking, not slits, as A says |
| Pressure-advance and pattern advice from Klipper, Voron, Cura, Duet and MatterHackers | A | Snippets, or a different firmware | Not re-opened |
| In both overlap pairs the turned piece did better (`P` over `L`, `2` over `T`) | A and B | The print record: "P has fewer, l has more" and "2 is better than T" are Omar's words. That the turn is the cause is Claude's reading, and the record says so | Confirmed as Omar's ranking. The cause is a reading. The turned pieces also sat in other places on the bed |
| The slits on `T`, `W` and `Y` sit mostly "on the left" straps | A | The print record: these are Claude's photo captions, not Omar's words | Contradicted as worded. A cites it as the record's finding. It is Claude's reading of a photo, and "left" is the photo's left, not the bed's |
| 1.10 flow beat 1.05 | A | The print record: Omar set each flow piece against `J` ("W is almost identical to J. U is a bit better"; "Y has less than J and X has less than Y"), never 1.10 against 1.05 | Second-hand: a fair inference from two answers about `J`, not a direct comparison |

Of 33 rows: 26 confirmed (several with a narrower reading, noted in the row), 2 contradicted as
worded, 1 second-hand, and 4 not re-opened. The Prusa 100% row also contradicts a third claim as
worded, A's "Nobody I found printed 75% or 100%".

## 2. Where the passes agree, disagree, or stand alone

### They agree

- Push the overlap past 55%, to 75% and 100%, per piece. Compose takes both today.
- Put 55% and flow 1.1 on one piece. They were never on one piece in bedface-4.
- A lower first layer (−0.02 mm, then −0.04 mm) stays the strongest whole-plate step. Its support is
  the 2026-10-12 plan's X2D users and the bedface-3 hint.
- A slower first layer moves down the list.
- Arachne, the fill angle and pressure advance are all weak leads.
- Check the top face of every overlap piece, because the overlap acts on every layer.
- Keep the house method: pieces of the real coaster on one bed, two per setting, stock beside.
- Nothing either pass proposes risks the printer.

### They disagree

| Point | A | B | Which side the sources support |
|---|---|---|---|
| What the next bed is | Per-piece overlap and flow at stock height; the lower first layer is a later plate | The whole bed at −0.02 mm, with the per-piece pairs riding on it | Neither, from sources. It is a trade. B's way reads the height only against bedface-4's photos, across two prints. A's way keeps the stock-beside read for everything on the bed. The owner decides; §3 lays out both |
| Stacking more flow on 75% and 100% | Stack 1.1 on each | Keep 75% and 100% alone, so a ridge can be traced to one change | No outside source. Both passes stack 55% and 1.1, so the disagreement is only how much to stack. B's reads cleaner. The proposal in §3 takes B's rule for 100% and stacks only 75%, beside 75% alone |
| How pieces are laid | One turned and one not in every pair | Both pieces of a pair unturned | Neither can be ordered today. The plate page says "compose has no way to stop" the arranger. See "found only by this check" on `--no-arrange` |
| Elephant-foot compensation | Set aside: it shrinks walls and fill together, and risks fits | Rank 4, a cheap try per piece | The code supports A: the shrink happens before walls and fill are made. B's forum case changed four other things at once. It stays low, and it needs a compose key |
| Arachne with four walls | Set aside | Rank 6 | The 2026-10-10 slice supports A: worse than 30% overlap on the coaster, and worse than stock on the middle piece |
| Plate cleaning | Rank 2, before every plate | Not listed | Only a snippet supports it, about parts not sticking. It costs nothing and risks nothing, but washing makes the next stock pair less comparable to bedface-4's |
| Fill angle | Rank 3, as a free check: sort the photos and slice three angles | Rank 7, as a later pair in print | Not a real conflict. A's is a check without a print. B's is a print after that |
| Pressure advance | Rank 5 | Rank 5 | Same rank. But the strongest source behind it, forum 68800, says the bottom was perfect with the wrong K. That weakens it below where either pass put it |
| A's claim that nobody printed 75% or 100% on a first layer | Nobody did | Cites the Prusa user who printed 100% with "no improvement" | B. A's claim is a K2: it speaks for a space A did not fully search. The Prusa case was a loose belt, so it does not show 100% fails when the slicer is the cause |

### Only pass A found

- `is_infill_first` cannot act on the first layer (code, confirmed). B left it unranked.
- The rule that joins line ends along the wall, and the 19.5° limit it implies. It is untested, and
  it rests on the strap angles, which nobody has measured.
- The zig-zag (`rectilinear`) bottom pattern as a per-piece lead. Compose does not take that value
  yet.
- The free checks: sort the bedface-4 photos by strap direction, and slice one piece at fill angles
  0, 45 and 90.

### Only pass B found

- Its own G-code reading of `H`: 730 moves, 1.75 mm average, 27 wipes (confirmed). From it, the
  slower first layer touches only 19 of the bottom moves.
- OrcaSlicer's separate first-layer overlap (confirmed, but its advice is about the top face).
- The Prusa 100% case and the elephant-foot case (both confirmed, both with confounds).
- `retract_restart_extra`, a little extra plastic after each stop. B itself shows it can explain at
  most 27 slits, not the pattern, and says to check the wipe spots against `H`'s photo before
  printing.

### Found only by this check

- **Nobody asked Omar whether `H` and `J` differ.** Row 1's question set them against bedface-2's
  `S` coaster as a pair. So the stock turn check is still open, and every "the turned piece did
  better" reading leans on it.
- **The slice misranked a piece against stock a third time.** In Omar's words, `L` (30%, not
  turned) had more slits than stock. The slice planned it with fewer (306 against `H`'s 356).
- **The slice predicted a turn effect the print did not show.** The monotonicline pair differs in
  the slice (`4` turned 246, `7` not turned 323), but Omar called them "About the same". The slice
  also split `P` (273) from `L` (306) and `2` (101) from `T` (159). So either the ten-direction
  premise is wrong for these windows, or the cut edges and rim change the fill. Neither pass looked
  into why.
- **The stock top face already uses `monotonicline`**, with the 45% travel extend. So the top face
  has the travel-extend look before any overlap change. When the overlap pieces' top faces are
  checked, compare them with the stock pieces' top faces, not with an idea of a plain top.
- **Compose has a `--no-arrange` flag** that "keeps authored positions"
  ([compose.ts](../../tools/bambu/src/commands/compose.ts), its options near L1447). The plate page
  says compose cannot stop the arranger turning pieces. Whether `--no-arrange` gives a twelve-piece
  bed laid out and unturned is untested. Until it is, both passes' turn layouts are wishes, and
  each piece's turn must be read off the slice and written on the plate page.

## 3. The plan, ranked by expected value for the next test print

Every item uses the house method unless it says otherwise: pieces cut from the real gBV coaster,
the bedface-4 shape, on the glacier plate. Each setting gets two pieces, with a stock pair on the
same bed. Each piece carries its carved id, and Omar judges by hand.

1. **Overlap 75% and 100%, each alone.** Per piece; compose takes it today. It extends the one
   trend we have (30% split, 55% better), and the mechanism is plain in the code.
   *This carries over to the whole coaster because the overlap acts at every spot where a fill
   line meets a wall, and each piece holds the coaster's straps, star hole and rim.* Risk: a
   ridge, on the bottom and on the top face. Not a machine risk.
2. **55% with flow 1.1, and 75% with flow 1.1.** Per piece; both keys are in compose. Each
   stacked pair sits beside the same overlap alone, so the flow's share and any ridge can be
   traced. *This carries over because both act on every first-layer line of the piece alike, and
   the piece's lines match the coaster's in width, speed and length.*
3. **A lower first layer, −0.02 mm.** Whole plate only. It is still the first whole-plate step, as
   in the 2026-10-12 plan. Then −0.04 mm only if slits remain. −0.02 mm is the trim Bambu's own
   start code applies on a textured plate, and −0.04 mm is inside the printer menu's ±0.05 mm
   range, so neither risks the machine. *This carries over because it lowers every first-layer
   line on the bed the same way, if the slit is a squash problem, which bedface-3 suggests and
   does not prove.* How it reaches the printer (a Textured PEI slice, or the menu offset) is the
   send step's call. See [the wrong-plate issue](../issues/sliced-for-wrong-plate.md).
4. **The free checks, before or beside the print.** Sort bedface-4's twelve photos by strap
   direction. Slice one piece at fill angles 0, 45 and 90, and draw each first layer with
   `tools/print_review.py`. Also ask Omar whether `H` and `J` differ. None of this needs a print.
   If the slits follow strap direction, the fill angle earns a compose key and a pair.
5. **Wash the plate with dish soap, and run bed leveling, before every plate from now on.** Whole
   plate. Weak support, no risk, and no cost but time. Compare within the plate, since the wash
   makes the stock pair less like bedface-4's.
6. **Pressure advance set by hand, after a Flow Dynamics calibration.** Whole plate. Weaker than
   the 2026-10-12 plan thought, since its best source says the bottom was fine with the wrong K.
7. **Elephant-foot compensation 0.** Per piece in the code, but compose needs the key first, with a
   read-back that shows 0 on the piece and 0.15 on stock. The code gives no reason it would help.
   Coaster pieces only; loose pieces with fits stay at stock.
8. **The zig-zag (`rectilinear`) bottom pattern.** Per piece, but compose does not take the value
   yet. Slice it and draw it before any print.
9. **Arachne with four walls.** Per piece in the code, but compose takes neither key. The
   2026-10-10 slice ranked it below 30% overlap.
10. **A slower first layer, then 225 °C.** Whole plate. Last, as both passes say.

Dropped: lay the fill first (the code ignores it on layer 1), gap-fill speed (already the
first-layer speed), monotonicline (Omar: "About the same"), 30% overlap (55% did better), one wall
on the first layer (no source), and `retract_restart_extra` until the wipe spots line up with
notches in `H`'s photo.

### A proposed next bed

This is a proposal. What prints next is the owner's call.

Twelve pieces, the bedface-4 shape, on the glacier plate, at stock height, with the plate washed
first:

| Pair | Setting | Per piece or plate | What it reads |
|---|---|---|---|
| 1 | stock | — | the control on this bed |
| 2 | overlap 55% | per piece | bedface-4's best, again; the bridge to bedface-4 |
| 3 | overlap 75% | per piece | item 1 |
| 4 | overlap 100% | per piece | item 1; the likeliest ridge |
| 5 | overlap 55% and flow 1.1 | per piece | item 2, against pair 2 |
| 6 | overlap 75% and flow 1.1 | per piece | item 2, against pair 3 |

Lay one piece of each pair turned and one not. If `--no-arrange` can hold the pieces still, use
it. If not, read each piece's turn off the slice and write it on the plate page. Judge both
faces: the bottom for slits and a ridge, and the top beside the stock pair's top.

The alternative, B's: the same bed with everything at −0.02 mm, and pair 6 as elephant foot 0
(which needs a compose key first). It reads the height in the same print. It gives up a
stock-beside read of the height, since the stock pair is then lowered too. Under this proposal the
height gets its own stock-only plate after this one.

### Where this changes the 2026-10-12 plan

- Plate 1 of that plan is done (bedface-4). First-layer flow is now proven per piece, and in
  Omar's words it helped a little, where the plan expected nothing.
- Monotonicline and 30% overlap leave the list. 55% is the new base, and 75% and 100% are next.
- The lower first layer stays the first whole-plate step, unchanged.
- The slower first layer was the second whole-plate step. It drops to last: only 19 of `H`'s 730
  bottom moves are long enough to reach 60 mm/s.
- So pressure advance moves up to the second whole-plate step, but with weaker support than the
  plan gave it (forum 68800).
- Elephant foot moves from "leave alone" to a low per-piece try, and only after compose has the
  key.
- New: the turn of each piece must be recorded, and Omar should be asked whether `H` and `J`
  differ.

## 4. What this file assumes, not decides

- That a piece of the coaster stands for the whole coaster for overlap and flow. For the fill
  angle it may not, because a piece holds only some strap directions.
- That the overlap millimeters are close. They are both passes' estimate, not read from a slice.
- That a few slits may be acceptable. No source and no print so far removes them all. Where "good
  enough to sell" sits is Omar's call.
- Whether the next bed is at stock height or −0.02 mm, and how a lower first layer reaches the
  printer. Owner's call and the send step's call.
- Whether to give compose new keys (elephant foot, fill angle, the zig-zag value). Each would need
  the same read-back proof the flow key got.
- That the 100% overlap and 75% plus flow 1.1 pieces will not mark the plate or the nozzle. The
  extra plastic is small (at most about 0.46 mm of push and 10% more flow on one layer), so I see
  no machine risk. But neither has been printed here.
