---
run: 2026-10-23-split-05
plate: "split-05 — two slices of the flange coaster at a 0.10 mm piece gap, one held by 1.2 mm pins, one by 1.0 mm pins, the kite at 0.12 and 0.13 mm"
status: printed
outcome: no-reading
plate_3mf: "split-05.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, green #00AE42"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: "HS01"
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand, in chat"
pins:
  bikar_ref: 03f7119599cf408a2d2ceb95c54a98b72bc46c15
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Lower"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":3}
    count: 1
    iteration: "it-48c98605116a"
    verdict: keep
    notes:
      - "The lower half of set 3, 1.2 mm pins, its 3 on the bottom"
      - "Omar: \"both are good\"; \"2a one probably better\""
      - "Verdict keep: the 1.2 mm pins are the better of the two"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Upper"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":3}
    count: 1
    iteration: "it-dbcf8ff08c5a"
    verdict: keep
    notes:
      - "The upper half of set 3, 1.2 mm pins, no id, kept with its set from the bed map"
      - "Omar: \"both are good\"; \"2a one probably better\""
      - "Verdict keep: the 1.2 mm pins are the better of the two"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Middle"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":3}
    count: 1
    iteration: "it-dda56955e4c2"
    verdict: keep
    notes:
      - "The middle piece of set 3, 1.2 mm pins, carved 2A"
      - "Omar: \"both are good\"; \"2a one probably better\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9"
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Kite"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.12,"id":3}
    count: 1
    iteration: "it-180e2dd093b5"
    verdict: keep
    notes:
      - "The kite of set 3, 1.2 mm pins, no id, kept with its set from the bed map, gap 0.12"
      - "Omar: \"both are good\"; \"2a one probably better\""
      - "Verdict keep under \"both are good\". Omar did not compare the two kites (0.12 mm here) apart from their sets, so which kite gap is better is not known"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Hex"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":3}
    count: 1
    iteration: "it-6836dfeddde0"
    verdict: keep
    notes:
      - "The inner hex of set 3, 1.2 mm pins, carved 2E"
      - "Omar: \"both are good\"; \"2a one probably better\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9"
  - entry: "c6"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Star"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":3}
    count: 1
    iteration: "it-d8f8be445813"
    verdict: keep
    notes:
      - "The star of set 3, 1.2 mm pins, no id, kept with its set from the bed map"
      - "Omar: \"both are good\"; \"2a one probably better\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9"
  - entry: "c7"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Outer"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":3}
    count: 1
    iteration: "it-bea12257d025"
    verdict: keep
    notes:
      - "The outer piece of set 3, 1.2 mm pins, carved 2F"
      - "Omar: \"both are good\"; \"2a one probably better\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9"
  - entry: "c8"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Lower"
    params: {"size":112.5,"stud":1,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":5}
    count: 1
    iteration: "it-6ae96346666e"
    verdict: adjust
    notes:
      - "The lower half of set 5, 1.0 mm pins, its 5 on the bottom"
      - "Omar: \"both are good\"; \"2c one shakes a bit\""
      - "Verdict adjust: the set with 1.0 mm pins shakes a bit when closed, so the 1.2 mm pins win"
  - entry: "c9"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Upper"
    params: {"size":112.5,"stud":1,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":5}
    count: 1
    iteration: "it-f7585e0d0535"
    verdict: adjust
    notes:
      - "The upper half of set 5, 1.0 mm pins, no id, kept with its set from the bed map"
      - "Omar: \"both are good\"; \"2c one shakes a bit\""
      - "Verdict adjust: the set with 1.0 mm pins shakes a bit when closed, so the 1.2 mm pins win"
  - entry: "c10"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Middle"
    params: {"size":112.5,"stud":1,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":5}
    count: 1
    iteration: "it-f60fab5180da"
    verdict: keep
    notes:
      - "The middle piece of set 5, 1.0 mm pins, carved 2C"
      - "Omar: \"both are good\"; \"2c one shakes a bit\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9. The shake in set 5 is read as the halves on their smaller pins, not this piece; Omar did not say which"
  - entry: "c11"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Kite"
    params: {"size":112.5,"stud":1,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.13,"id":5}
    count: 1
    iteration: "it-d9f1cbe2e30d"
    verdict: keep
    notes:
      - "The kite of set 5, 1.0 mm pins, no id, kept with its set from the bed map, gap 0.13"
      - "Omar: \"both are good\"; \"2c one shakes a bit\""
      - "Verdict keep under \"both are good\". Omar did not compare the two kites (0.13 mm here) apart from their sets, so which kite gap is better is not known. The shake in set 5 is read as the halves on their smaller pins, not this piece; Omar did not say which"
  - entry: "c12"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Hex"
    params: {"size":112.5,"stud":1,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":5}
    count: 1
    iteration: "it-a0bae26d54da"
    verdict: keep
    notes:
      - "The inner hex of set 5, 1.0 mm pins, carved 2J"
      - "Omar: \"both are good\"; \"2c one shakes a bit\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9. The shake in set 5 is read as the halves on their smaller pins, not this piece; Omar did not say which"
  - entry: "c13"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Star"
    params: {"size":112.5,"stud":1,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":5}
    count: 1
    iteration: "it-6377508c79d9"
    verdict: keep
    notes:
      - "The star of set 5, 1.0 mm pins, no id, kept with its set from the bed map"
      - "Omar: \"both are good\"; \"2c one shakes a bit\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9. The shake in set 5 is read as the halves on their smaller pins, not this piece; Omar did not say which"
  - entry: "c14"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Outer"
    params: {"size":112.5,"stud":1,"stud_gap":0.25,"stud_spacing":6,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":5}
    count: 1
    iteration: "it-d277bf1aaa91"
    verdict: keep
    notes:
      - "The outer piece of set 5, 1.0 mm pins, carved 2K"
      - "Omar: \"both are good\"; \"2c one shakes a bit\""
      - "Verdict keep: 0.10 mm stays the gap, as on split-04's set 9. The shake in set 5 is read as the halves on their smaller pins, not this piece; Omar did not say which"
readings: []
photos: []
feedback:
  lesson: "On the flange coaster's pinned slice at a 0.10 mm piece gap, 1.2 mm pins placed at least 6 mm apart round every outer edge and point (6 in a slice, 31 on a whole coaster) hold the halves better than 1.0 mm pins (11 in a slice, 54 on a whole coaster): both came out good, and the 1.0 mm set shakes a bit. 0.4 mm nozzle, 0.20 mm layers, setting 8, sliced as Textured PEI for the gold plate"
  decisions: []
  symptom: "Omar: both sets good; set 3 (1.2 mm pins, middle carved 2A) probably better; set 5 (1.0 mm pins, middle carved 2C) shakes a bit"
  cause: "Not measured. A thinner pin with the same 0.25 mm of play round it has more room to move for its size, which may be the shake; not checked"
  next: "1.2 mm pins, 6 mm apart, are the pin for the flange coaster. The pieces keep 0.10 mm; the kite keeps 0.12 mm, set 3's, since its kite was in the set Omar picked, though the two kites were not compared on their own. Still open: whether the ring round the middle piece, where no pin fits, closes flush. Omar asked next for a whole coaster at set 3's settings with no ids, as a production piece"
---

Omar judged this plate on 2026-10-23 in chat, from the pieces in hand, in three lines. He turned
down the page's six questions one by one ("too many questions") and gave his verdict instead.

The bed had two sets, each in its own block: set 3 on the left with 1.2 mm pins, set 5 on the right
with 1.0 mm pins. Both at a 0.10 mm piece gap. The kites at 0.12 mm (set 3) and 0.13 mm (set 5).

| Part | In Omar's words | What it means |
|---|---|---|
| Both sets | "both are good" | the pins printed and the pieces fit in both |
| Set 3, 1.2 mm pins (its middle carved 2A) | "2a one probably better" | 1.2 mm is the pin |
| Set 5, 1.0 mm pins (its middle carved 2C) | "2c one shakes a bit" | 1.0 mm is out |

**Read, not said.** Omar named each set by its middle piece. The shake in set 5 is read here as
the halves on their thinner pins, not as one loose piece; he did not say which. "Both are good" is
read as the pins printing whole and the pieces fitting, since he raised no fault.

**Not asked.** The page's rows on sorting, the space round the middle piece where no pin fits,
whether a closed set stays shut when turned over, and the two kites compared on their own.

**The ids.** The page named the pieces 1A, 1E, 1F and 1C, 1J, 1K. The print carved 2A, 2E, 2F
and 2C, 2J, 2K: the digit is the recipe's iteration, and the plate went to iteration 2 before
it was sent. The page is corrected in the same change.

**The slice.** Sliced again at the send for the gold Textured PEI plate 
(`--plate-type textured_plate`), with the X2D preset and PLA Basic, from bikar #342, each set in a block of its
own, no slicer warnings. The record's pieces and iterations are that slice's.

**The print.** Sent at 17:44 UTC on 2026-10-23 in green from AMS 0 slot 3, finished at 19:00 UTC,
all 21 layers (the [print log](../../design/plates/print-logs/split-05.md)). Every chamber picture
looked clean, and the pins stood upright on both lower halves near the end. Nothing was measured
with a tool, so there are no readings and no bet moves.
