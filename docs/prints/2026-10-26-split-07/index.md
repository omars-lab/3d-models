---
run: 2026-10-26-split-07
plate: "split-07 — the whole flange coaster, every loose piece cut in two and joined"
status: printed
outcome: no-reading
plate_3mf: "split-07.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, green #00AE42"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: "HS01 (standard flow, hardened steel)"
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; closed unjudged, nothing looked at for this record"
pins:
  bikar_ref: 112d257569a8501109f7fe6a3821d52cbe4d2e7b
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "2941dd671aed15bdc883d36240cb3b3dd9559bea1c7b3cedfcdf2500093ea847"
    piece: "Lower"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13.0,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":3,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.15,"slide_height":0.8,"slide_hex":1,"slide_outer":1}
    count: 1
    verdict: keep
    notes:
      - "The lower half of the frame, with its 40 pins and 0.7 mm socket walls"
      - "Verdict keep: Omar in chat on 2026-10-27 said the frame \"came out well\""
      - "Whether the closed coaster is one to keep as it is (question 1) was taken over by split-10, which retried each loose piece he named"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "2941dd671aed15bdc883d36240cb3b3dd9559bea1c7b3cedfcdf2500093ea847"
    piece: "Upper"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13.0,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":3,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.15,"slide_height":0.8,"slide_hex":1,"slide_outer":1}
    count: 1
    verdict: keep
    notes:
      - "The upper half of the frame"
      - "Verdict keep: Omar in chat on 2026-10-27 said the frame \"came out well\""
      - "Whether it closes snug and flush (question 5) was taken over by split-10 and hexfit-1"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "2941dd671aed15bdc883d36240cb3b3dd9559bea1c7b3cedfcdf2500093ea847"
    piece: "Middle"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13.0,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":3,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.15,"slide_height":0.8,"slide_hex":1,"slide_outer":1}
    count: 1
    verdict: adjust
    notes:
      - "The middle piece, cut in two and joined by three pins"
      - "Verdict adjust: Omar in chat on 2026-10-27 said it has a \"webbed duck feel\", and \"the middle peice had 3 asymetric pins ... should have been 1 in middel and 4 or 6 radially around the middle near the edges with enough room\""
      - "Taken over by split-10: its question 2 (the webbed feel, answered by Omar's \"this was best\" on its MIDDLE-SUPPORT) and its question 3 (the pin count, closed by closeout-1)"
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "2941dd671aed15bdc883d36240cb3b3dd9559bea1c7b3cedfcdf2500093ea847"
    piece: "Kite"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13.0,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.12,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":3,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.15,"slide_height":0.8,"slide_hex":1,"slide_outer":1}
    count: 1
    verdict: not-judged
    notes:
      - "The small kites, cut in two and joined by one pin, gap 0.12"
      - "Omar: \"the dovetail kites are really loose\". Not a verdict on this piece: it is not clear whether he meant the small kites or the dovetail pieces (hexagons and outers)"
      - "The kites at 0.12 mm (question 8) were taken over by split-10's question 4, which closeout-1 closes"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "2941dd671aed15bdc883d36240cb3b3dd9559bea1c7b3cedfcdf2500093ea847"
    piece: "Hex"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13.0,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":3,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.15,"slide_height":0.8,"slide_hex":1,"slide_outer":1}
    count: 1
    verdict: not-judged
    notes:
      - "The hexagon pieces, cut in two and joined by a slide"
      - "Omar: \"the dovetail kites are really loose\". Not a verdict on this piece: it is not clear whether he meant the small kites or the dovetail pieces (hexagons and outers)"
      - "The slide question (4) was taken over by hexfit-1, which settled the dovetail gap at 0.01 mm a side, now bikar's default; hexfit-2 kept the rail at that gap"
      - "The lopsided bigger kites (question 6) close with no photo, by Omar's choice on 2026-11-06; they come back only if the next whole coaster shows them"
  - entry: "c6"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "2941dd671aed15bdc883d36240cb3b3dd9559bea1c7b3cedfcdf2500093ea847"
    piece: "Star"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13.0,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":3,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.15,"slide_height":0.8,"slide_hex":1,"slide_outer":1}
    count: 1
    verdict: adjust
    notes:
      - "The stars, cut in two and joined by one pin"
      - "Verdict adjust: Omar in chat on 2026-10-27 said \"stars faces are just bad\", and that they \"are not a star extruded, they have a curve\""
      - "The faces (question 2) were taken over by split-10's question 1, and the pins (questions 3 and 7) by split-10's question 3 and star-3's question 1; closeout-1 closes all three"
  - entry: "c7"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "2941dd671aed15bdc883d36240cb3b3dd9559bea1c7b3cedfcdf2500093ea847"
    piece: "Outer"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13.0,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":3,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.15,"slide_height":0.8,"slide_hex":1,"slide_outer":1}
    count: 1
    verdict: not-judged
    notes:
      - "The outer pieces, cut in two and joined by a slide"
      - "Omar: \"the dovetail kites are really loose\". Not a verdict on this piece: it is not clear whether he meant the small kites or the dovetail pieces (hexagons and outers)"
      - "The slide question (4) was taken over by hexfit-1, which settled the dovetail gap at 0.01 mm a side, now bikar's default; hexfit-2 kept the rail at that gap"
      - "The lopsided bigger kites (question 6) close with no photo, by Omar's choice on 2026-11-06; they come back only if the next whole coaster shows them"
readings: []
photos: []
feedback:
  lesson: "split-07 was closed without its eight questions asked. Omar said in chat what he saw: the frame came out well, the stars' faces curve, the middle feels webbed and its three pins sit wrong, and some joined pieces are loose. The pieces were replaced by split-10, star-3, hexfit-1, hexfit-2 and closeout-1. Closed unjudged on Omar's say-so on 2026-11-06 (\"Close all four\")"
  decisions: []
  cause: "Omar's chat comments on 2026-10-27 led straight to split-10, which tried each fault on its own pieces, so the page's own questions were never put to him"
  next: "Nothing more from these pieces. The faces, pins and kite gap close on closeout-1, the dovetail on hexfit-1 and hexfit-2, the middle's feel on split-10's MIDDLE-SUPPORT. The lopsided bigger kites come back only if the next whole coaster shows them"
---

The bed held one whole flange coaster in green: the lower and upper halves of the frame and every
loose piece, each loose piece cut in two at its middle and joined (pins on the middle, kite and
star; a slide on the hexagons and outer pieces), with a 0.7 mm wall round each pin socket.

**Why it was not judged.** Omar looked at the pieces and said in chat on 2026-10-27 what was wrong
with them: the frame "came out well", but the "stars faces are just bad", the middle has a "webbed
duck feel" and its three pins sit wrong, "the dovetail kites are really loose", and "i want to run
experiments on these infill pieces". split-10 was built from those words, so the page's eight
questions were never asked. On 2026-11-06 he closed the plate ("Close all four").

| Question | Taken over by |
|---|---|
| 1, keep the coaster as it is | split-10 |
| 2, both faces smooth | split-10 question 1, closed by closeout-1 |
| 3, pinned halves hold | split-10 question 3 and star-3 question 1, closed by closeout-1 |
| 4, hexagons and outers slide on | hexfit-1 (0.01 mm a side, bikar's default), then hexfit-2 |
| 5, joined pieces snug | split-10 and hexfit-1 |
| 6, the lopsided bigger kites | closed with no photo, Omar 2026-11-06 |
| 7, sockets hold when pressed | split-10 question 3 and star-3 question 1 |
| 8, kites at 0.12 mm | split-10 question 4, closed by closeout-1 |

**Read, not said.** The frame is read as the lower and upper halves, so "came out well" is their
keep. "The dovetail kites" could mean the small kites or the dovetail pieces, so neither gets a
verdict from it.

**Not asked.** All eight questions on the page. The params are the recipe's iteration 3, the one
sent; the draft the slicer left was from iteration 2 and was not used.

**The print.** Sent at 18:03 UTC on 2026-10-26 in green from AMS 0 slot 3, finished at 20:41 UTC,
all 18 layers, 36.49 g by the slice (the [print log](../../design/plates/print-logs/split-07.md)).
Nothing was measured with a tool, so there are no readings and no bet moves.
