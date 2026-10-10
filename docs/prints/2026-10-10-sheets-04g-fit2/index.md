---
run: 2026-10-10-sheets-04g-fit2
plate: "sheets-04g-fit2 — the middle piece at 0.025 mm, halfway between sheets-04g-fit's A and B, with both as controls, the kites at 0.05 and a fresh coaster"
status: printed
outcome: no-reading
plate_3mf: "sheets-04g-fit2.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C"
  spool: "620317506F7D477AB7EB1CD14089FFDA"
  nozzle_mm: 0.4
  nozzle_type: "HS01"
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand"
pins:
  bikar_ref: c0e6563afc856be8f881b5059766f689821fd932
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    count: 1
    iteration: "it-f472bd0548e1"
    verdict: not-judged
    notes:
      - "The fresh coaster, carved Z on its bottom. Every piece on this plate was tried in it; Omar said how the pieces fit, not how the coaster itself came out"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Kite"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.05}
    count: 10
    iteration: "it-f357c32a4f5a"
    verdict: adjust
    notes:
      - "The pile of ten kites cut at 0.05 mm (no id; one render gives the ring of ten). Tough to push into the Z coaster, and once in, all three tried stay in upside down"
      - "Omar, in chat: \"samll kites could be a bit smaller, tought to insert\""
      - "Omar, asked whether three kites stay in the Z coaster upside down: \"All stay in\""
      - "On sheets-04g-fit the same 0.05 kites fit that plate's Z coaster well, so this coaster's kite holes came out tighter"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0,"middle_dots":3}
    count: 1
    iteration: "it-056b551b1821"
    verdict: drop
    notes:
      - "Carved id 4GH 1A (gap 0, three dots), the tight control. Super tight in the Z coaster"
      - "Omar, in chat: \"1a sauper tight\""
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.025,"middle_dots":2}
    count: 1
    iteration: "it-b4b931030b9a"
    verdict: keep
    notes:
      - "Carved id 4GH 1C (gap 0.025, two dots), the halfway piece. The best fit of the three in the Z coaster"
      - "Omar, in chat: \"4gh ic is winner\" (read as 4GH 1C: the id has no I)"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.05,"middle_dots":1}
    count: 1
    iteration: "it-49f88af36057"
    verdict: drop
    notes:
      - "Carved id 4GH 1E (gap 0.05, one dot), the easy control. Loose in the Z coaster"
      - "Omar, in chat: \"1e loose\""
readings: []
photos: []
feedback:
  lesson: "Halfway worked: printed beside its own coaster, the middle piece at 0.025 mm sat between gap 0 (super tight) and 0.05 (loose) and was the one Omar picked, so the slicer does keep a 0.025 mm step apart in feel. The kites at 0.05 went the other way from sheets-04g-fit: they fit that plate's coaster well and were tough to push into this one, though they hold once in. A coaster's holes move from print to print by about a 0.05 mm rung, now seen on three coasters, so a gap is judged in a coaster from the same bed"
  decisions: []
  symptom: "Z coaster: 4GH 1A super tight, 4GH 1C the winner, 4GH 1E loose; the 0.05 kites tough to push in but all stay in upside down"
  cause: "Not measured on the pieces (no calipers reading). The kites tighter and 4GH 1A tighter than on sheets-04g-fit, but 4GH 1E looser than that plate's 0.05 piece: not one shift of the whole coaster, and not explained. Nothing on this plate separates the coaster's holes from the pieces"
  next: "The middle piece's gap is 0.025 mm on the next sheets-04g iteration. The kites want a little more gap than 0.05; sheets-04g-fit found 0.10 too small, so the next kite step sits between the two. How big a step is Omar's call"
---

Omar judged this plate by hand on 2026-10-10, the day it printed. It has no photos. The rows of
the page's [After the print](../../design/plates/sheets-04g-fit2.md#after-the-print) table were
asked in turn, all in the fresh `Z` coaster printed on the same bed.

- **Middle piece: `4GH 1C` wins.** Omar, in chat: "4gh ic is winner". The ids carry no I, so
  "ic" is `1C`, the piece cut at 0.025 mm. The two controls bracket it: "1a sauper tight, 1e
  loose". `4GH 1A` is gap 0 and `4GH 1E` is 0.05 mm.
- **Kites: a bit smaller.** "samll kites could be a bit smaller, tought to insert". Asked whether
  three kites stay in the `Z` coaster held upside down, he answered "All stay in". So they hold,
  but pushing them in is too hard.

**The lesson for the next plate.** Halfway worked: the slicer keeps a 0.025 mm step apart in the
hand, and that step is the middle piece's gap. The kites moved the other way from
[sheets-04g-fit](../2026-10-10-sheets-04g-fit/index.md), where the same 0.05 kites fit that
plate's coaster well. The controls do not agree with one shift of the whole coaster either: `1A`
felt tighter than last time's gap-0 piece, `1E` looser than last time's 0.05 piece. Nothing was
measured, so that stays a reading by hand. What holds across three coasters now is that the holes
move by about one 0.05 mm rung from print to print, which is why every gap here was judged in a
coaster from the same bed.

**How it went.** It was sent at 15:13 UTC on 2026-10-10, in pink, on the smooth glacier plate.
The printer said FINISH at 16:28 with all 22 layers done (the
[print log](../../design/plates/print-logs/sheets-04g-fit2.md)). That is 75 minutes against the
slicer's 67. A background watcher looked at all 17 chamber pictures and saw nothing lift or
string; the timelapse is on [the page](../../design/plates/sheets-04g-fit2.md#the-print), with
the last picture left out because it shows a hand lifting the plate.

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built, at bikar `c0e6563a`. The send ran from an older bikar checkout (`951995ab`), which does not
change what printed: the printer got the sliced file made at `c0e6563a`. Nothing was measured
with a tool, so there are no readings and no bet moves.
