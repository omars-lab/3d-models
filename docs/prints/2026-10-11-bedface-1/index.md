---
run: 2026-10-11-bedface-1
plate: "bedface-1 — sheets-04g-fit2's pieces again, on the house bed-face preset (rings on the first layer, 30% overlap, a 0.42 mm first line)"
status: printed
outcome: no-reading
plate_3mf: "bedface-1.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C"
  spool: "620317506F7D477AB7EB1CD14089FFDA"
  nozzle_mm: 0.4
  nozzle_type: "HS01"
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "Naqsh bed face 0.20mm @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand and one photo"
pins:
  bikar_ref: c0e6563afc856be8f881b5059766f689821fd932
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    count: 1
    iteration: "it-b2cb0c66967d"
    verdict: adjust
    notes:
      - "The coaster carved F on its bottom, the same design as fit2's Z coaster, printed on the house preset. Its bottom is no cleaner than Z's: the rings close the slits along the strap edges but leave short dark dashes and small triangles down the middle of the straps and where straps meet, where the rings from the two sides come together (the photo)"
      - "Omar, asked whether F has fewer slits than Z: \"About the same\""
      - "Omar, beside the kites: \"F as a coaster has more slits\""
      - "Omar, with the photo: \"F has a lot of slits ..\""
      - "The design is not at fault here: the verdict is on the first-layer settings it printed with, which go back to stock until a new fix is printed"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Kite"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.05}
    count: 10
    iteration: "it-8f8e45d963aa"
    verdict: adjust
    notes:
      - "The pile of ten kites cut at 0.05 mm (no id; one render gives the ring of ten). No dent in the middle of the bottom: the 0.42 mm first line filled the core, as the plan said"
      - "Omar, in chat: \"f's kites don't have dents\""
      - "Too tight in the F coaster; fit2's same 0.05 kites were already tough to push into the Z coaster"
      - "Omar, in chat: \"kites too tight\""
      - "Whether they stay in upside down was not said"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0,"middle_dots":3}
    count: 1
    iteration: "it-af5de7a345d4"
    verdict: not-judged
    notes:
      - "Carved id FC1 1A (gap 0, three dots). Omar named FC1 1E the winner and said nothing of 1A by itself"
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.025,"middle_dots":2}
    count: 1
    iteration: "it-df319f05a87f"
    verdict: not-judged
    notes:
      - "Carved id FC1 1C (gap 0.025, two dots), fit2's winner as 4GH 1C. Omar named FC1 1E the winner and said nothing of 1C by itself"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.05,"middle_dots":1}
    count: 1
    iteration: "it-24b27d8e290c"
    verdict: keep
    notes:
      - "Carved id FC1 1E (gap 0.05, one dot). The best fit of the three in the F coaster, where its fit2 twin 4GH 1E was loose in the Z coaster"
      - "Omar, in chat: \"fc1 1e winner\""
readings: []
photos:
  - file: photos/f-coaster-bed-face.jpg
    sha256: 91d67bd115b116dc217a150fef33ed3a161da005949356ccdc04f082feca1033
    of: "the F coaster's bottom, held up in the hand: rings along every strap, with dark dashes and small triangles down the strap middles and at the junctions"
    why: "shows where the house preset's first layer leaves bed bare in print: where two sets of rings meet, not at the strap edges"
feedback:
  lesson: "The house bed-face preset did not clean the coaster's bottom in print: the rings closed the slits at the strap edges but left dashes and small triangles down the middle of each strap and at the junctions, and Omar found as many slits as on the stock coaster, or more, though the slicer's plan had the bare share falling from 1.10% to 0.26%. The 0.42 mm first line did fill the small kites' core. And every fit came out about one 0.025 mm rung tighter than fit2's (0.4 mm nozzle, 0.42 mm first line and 0.42 mm outer and 0.45 mm inner wall lines, 0.20 mm layers, glacier plate sliced as Smooth PEI)"
  decisions: []
  symptom: "F coaster: slits about the same as fit2's Z coaster, or more (the photo: dashes and triangles down the strap middles and at the junctions). Kites: no dent in the middle, but too tight in the F coaster. Middle piece: FC1 1E (0.05) the winner, where fit2's winner was 4GH 1C (0.025) and its 0.05 piece was loose"
  cause: "Not separated by this plate; three suspects. The rings: where the rings from two sides of a strap meet, the slicer leaves specks, which the design's §3.3 drew and counted as small; in print they show as dashes. The narrower first line: 0.42 mm squashes less than 0.5, so the specks the plan leaves are not closed by squash (design §7). The glacier plate: sliced as Smooth PEI, it gets no extra 0.02 mm push on the first layer (design §3.4). The tighter fit: the plan kept the outer edge in place, so a wider first layer in print would have to come from the overlap or the narrower line, not measured; and coasters already move by about one rung from print to print (fit2's record), so one plate cannot say how much of the shift is the preset"
  next: "The house preset does not roll out; every plate stays on the X2D 0.20 mm Standard. The slit fix is reworked, and the slicer's plan is no longer taken as proof of a clean bottom (docs/issues/bed-face-preset-failed-in-print.md). The fit shift is read again with fit3 before any gap changes"
---

Omar judged this plate by hand on 2026-10-11, the day it printed, beside
[sheets-04g-fit2](../2026-10-10-sheets-04g-fit2/index.md)'s pieces printed on the stock settings.
The rows of the page's [After the print](../../design/plates/bedface-1.md#after-the-print) table were
asked in turn, and he sent one photo of the `F` coaster's bottom.

- **The `F` coaster: no cleaner.** Asked whether `F` has fewer slits than fit2's `Z`: "About the
  same". Then, "F as a coaster has more slits", and with the photo, "F has a lot of slits ..". The
  photo shows where: the rings follow each strap's edges, so the edges are closed, but down the
  middle of the straps, and where three straps meet, the rings from the two sides come together
  and leave short dark dashes and small triangles of bare bed. That is the place the
  [bed-face design](../../design/printing/bed-face-slicing-design.md#33-what-rings-bring-with-them)
  drew as "a thin row of specks" and judged far smaller than the slits.
- **Kites: no dent, but too tight.** "f's kites don't have dents": the 0.42 mm first line filled
  the core, the one thing the plan got right in print. But "kites too tight" in the `F` coaster,
  where fit2's same 0.05 kites were already tough to push in.
- **Middle piece: `FC1 1E` wins.** "fc1 1e winner". On fit2 the winner was `4GH 1C` (0.025) and
  `4GH 1E` (0.05) was loose, so the fit moved about one 0.025 mm rung tighter. `FC1 1A` and
  `FC1 1C` are left not judged: he named the winner, not how the other two felt.
- **Round the carved letters:** not judged yet. The photo is of the coaster, not the FC1 pieces.

![The F coaster's bottom: rings along the straps, with dashes and triangles where they meet](photos/f-coaster-bed-face.jpg)

The photo was re-saved at 1200 by 1600 with no metadata, so it carries no location.

**The lesson for the next plate.** The slicer's plan said this preset cut the bare bed on the
coaster's first layer by three quarters, and the print came out no better than stock. So a plan
that draws the bed covered is not proof the print is: the plan counts the meeting lines of the
rings as covered, or nearly, and in print they show. The design said this in its own words
("a PASS means the slicer is not planning slits, never the underside will be clean"); this plate is
the first time it mattered. The fit moved too, by about one rung, which is the size coasters
already move from print to print, so the next plate reads it again before any gap changes.

**How it went.** It was sent at 03:34 UTC on 2026-10-11, in pink, on the smooth glacier plate,
sliced as Smooth PEI. The printer said FINISH at 04:48 with all 22 layers done (the
[print log](../../design/plates/print-logs/bedface-1.md)): 74 minutes against the slicer's 67. The
timelapse is on [the page](../../design/plates/bedface-1.md#the-print).

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built, at bikar `c0e6563a`. The send ran from an older bikar checkout (`951995ab`), which does not
change what printed: the printer got the sliced file made at `c0e6563a`. Nothing was measured
with a tool, so there are no readings and no bet moves.
