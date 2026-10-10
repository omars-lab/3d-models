---
run: 2026-10-10-sheets-04g-fit
plate: "sheets-04g-fit — the kites and the middle piece at a ladder of gaps, with a fresh coaster to press them into"
status: printed
outcome: no-reading
plate_3mf: "sheets-04g-fit.plate.3mf"
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
    verdict: keep
    notes:
      - "The pile of ten kites cut at 0.05 mm (no id, no dots; one render gives the ring of ten). Fits well in the Z coaster"
      - "Omar, in chat: \"smill kite wise, the biggest size fits well, rest too small/lost\""
      - "Worked out, not read off the piece: the kites carry no mark, and the biggest kites are the 0.05 pile, since a smaller gap makes a bigger kite"
      - "In the older sheets-04g coaster (no id) it is loose. Omar, in chat: \"all small kites are loose\""
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Kite"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.1}
    count: 10
    iteration: "it-8638e25816b4"
    verdict: drop
    notes:
      - "The pile of ten kites cut at 0.10 mm (no id). Too small in the Z coaster"
      - "Omar, in chat: \"the biggest size fits well, rest too small/lost\""
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Kite"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.15}
    count: 10
    iteration: "it-b072451f28db"
    verdict: drop
    notes:
      - "The pile of ten kites cut at 0.15 mm (no id). Too small in the Z coaster"
      - "Omar, in chat: \"rest too small/lost\""
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Kite"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.2}
    count: 10
    iteration: "it-7a086919f2e3"
    verdict: drop
    notes:
      - "The pile of ten kites cut at 0.20 mm (no id). Too small in the Z coaster"
      - "Omar, in chat: \"rest too small/lost\""
  - entry: "c6"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Kite"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.25}
    count: 10
    iteration: "it-7d4cd455024f"
    verdict: drop
    notes:
      - "The pile of ten kites cut at 0.25 mm (no id). Too small in the Z coaster"
      - "Omar, in chat: \"rest too small/lost\""
  - entry: "c7"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0,"middle_dots":4}
    count: 1
    iteration: "it-6a2fa863e4a0"
    verdict: adjust
    notes:
      - "Carved id 4GF 4A (gap 0, four dots). Fits the Z coaster but too tight"
      - "Omar, in chat: \"middle peice wise, a fits but to tight\""
      - "In the older sheets-04g coaster it fits but comes out easily. Omar, in chat: \"4a fits but easliy removable\""
  - entry: "c8"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.05,"middle_dots":3}
    count: 1
    iteration: "it-07fff622d637"
    verdict: adjust
    notes:
      - "Carved id 4GF 4B (gap 0.05, three dots). Good in the Z coaster, but comes out a little too easily"
      - "Omar, in chat: \"B is good but comes off a bit to easy? is there a midway between a and b?\""
      - "In the older sheets-04g coaster it is loose. Omar, in chat: \"4b on that oen is loose\""
  - entry: "c9"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.1,"middle_dots":2}
    count: 1
    iteration: "it-aa02388fda8e"
    verdict: not-judged
    notes:
      - "Carved id 4GF 4C (gap 0.10, two dots). Omar did not say how it fit"
  - entry: "c10"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "983068570a0a5cbcb98b926782e43a70e999e3396e82b694b74b0bc8281b3594"
    piece: "Middle"
    params: {"size":112.5,"strap":3.75,"height":4.4,"gap":0.15,"middle_dots":1}
    count: 1
    iteration: "it-4aa9717704e9"
    verdict: not-judged
    notes:
      - "Carved id 4GF 4D (gap 0.15, one dot). Omar did not say how it fit"
readings: []
photos: []
feedback:
  lesson: "In the fresh Z coaster, printed on the same bed, the kites fit at 0.05 mm and every looser rung was too small, and the middle piece sits between 4A (gap 0, too tight) and 4B (0.05, good but comes out a little too easily). In the older sheets-04g coaster the same pieces sat about one 0.05 mm rung looser: 4A fit but came out easily, 4B and every kite were loose. So the coaster's holes came out about one rung larger on that print than on this one. One pair of coasters: a first reading, not a rule"
  decisions: []
  symptom: "Z coaster: the 0.05 kites fit well, the 0.10 to 0.25 kites were too small; 4GF 4A fit but too tight, 4GF 4B good but came out a little too easily; 4GF 4C and 4D not judged. Older sheets-04g coaster: 4A fit but came out easily, 4B loose, all kites loose"
  cause: "Not measured on the pieces (no calipers reading). The older coaster printed on 2026-10-04 in green from another spool; the coaster's source gained two knobs since (hole-point round and weld), both left at 0, which should leave the holes as they were, though the two meshes were not compared. Why its holes come out larger is not known. spl-2 found the stud fit moving 0.05 to 0.10 mm from print to print too"
  next: "Kites stay at 0.05 mm. Omar asked for a midway between 4A and 4B: a middle piece at 0.025 mm. Because the holes move about one rung between prints, that plate prints its own fresh coaster beside the middle pieces, and the pieces are judged in it"
---

Omar judged this plate by hand on 2026-10-10, the day it printed. It has no photos. Each row of
the page's [After the print](../../design/plates/sheets-04g-fit.md#after-the-print) table was
asked in turn: the kites and the middle pieces in the fresh `Z` coaster, then the best of them in
the older sheets-04g coaster.

- **Kites: 0.05 mm fits, the rest are too small.** Omar, in chat: "smill kite wise, the biggest
  size fits well, rest too small/lost". The kites carry no mark, so "the biggest" is my reading:
  a smaller gap makes a bigger kite, so the biggest are the 0.05 pile. The 0.10, 0.15, 0.20 and
  0.25 piles were too small for the `Z` coaster.
- **Middle piece: between 4A and 4B.** "a fits but to tight. B is good but comes off a bit to
  easy? is there a midway between a and b?" `4GF 4A` is gap 0 and `4GF 4B` is 0.05 mm. `4GF 4C`
  and `4GF 4D` were not mentioned, so they stay not judged.
- **The older coaster is about one rung looser.** "4b on that oen is loose. 4a fits but easliy
  removable'. all small kites are loose". So in the sheets-04g coaster, `4A` behaves about the
  way `4B` does in `Z`, and the 0.05 kites that fit `Z` are loose.

**The lesson for the next plate.** The pieces come out of one print and the holes out of
another, and the holes moved by about one 0.05 mm rung between the two coasters. That is one
pair of coasters, so it is a first reading, not a rule. It agrees with
[spl-2](../2026-10-09-spl-2/index.md), where the stud fit moved 0.05 to 0.10 mm from print to
print. So the halfway test Omar asked for, a middle piece at 0.025 mm, prints its own fresh
coaster on the same bed, and the pieces are judged in that one.

**How it went.** It was sent at 12:50 UTC on 2026-10-10, in pink from AMS 0 slot 0, on the smooth
glacier plate. The printer said FINISH at 14:21 with all 22 layers done (the
[print log](../../design/plates/print-logs/sheets-04g-fit.md)). That is 91 minutes against the
slicer's 78, with nothing lifting in the chamber pictures.

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built, at bikar `c0e6563a`; neither source changed up to the bikar commit the send ran on. Nothing
was measured with a tool, so there are no readings and no bet moves.
