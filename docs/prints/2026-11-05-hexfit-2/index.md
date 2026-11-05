---
run: 2026-11-05-hexfit-2
plate: "hexfit-2 — what stops the hexagon halves rocking"
plate_3mf: "hexfit-2.plate.3mf"
status: printed
outcome: no-reading
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, green #00AE42"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; tried by hand, answered in chat"
pins:
  bikar_ref: 21420bc3ba9d9dd99ff186427f8c95f41d80f4f9
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "fd36ae299a118a4f7822e5e046f055907f2fbb42c691b71b7a78b68e31185af4"
    piece: "Hex"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":7,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.01,"slide_slot_extra":1,"slide_height":0.8,"slide_hex":1,"slide_outer":1,"wedge":36,"dots_hex":1,"dots_bottom":1}
    count: 2
    iteration: "it-1f3fe90210db"
    verdict: keep
    notes:
      - "1 dot, HEX-CTRL: hexfit-1's best fit, 0.01 mm a side, rail 4 mm wide and 0.8 mm tall"
      - "Row 1: the only count Omar ticked as staying flat"
      - "Omar: \"they are all very identical, just go with 1 dot\""
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "fd36ae299a118a4f7822e5e046f055907f2fbb42c691b71b7a78b68e31185af4"
    piece: "Hex"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":7,"pins_kite":1,"pins_star":1,"slide":4,"slide_gap":0.01,"slide_slot_extra":0,"slide_height":1,"slide_hex":1,"slide_outer":1,"wedge":36,"dots_hex":2,"dots_bottom":1}
    count: 2
    iteration: "it-1fb8dda103f8"
    verdict: drop
    notes:
      - "2 dots, HEX-TALL: the rail 1.0 mm tall"
      - "Row 1: not ticked as staying flat"
      - "Not taken forward: Omar, \"just go with 1 dot\""
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "fd36ae299a118a4f7822e5e046f055907f2fbb42c691b71b7a78b68e31185af4"
    piece: "Hex"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":7,"pins_kite":1,"pins_star":1,"slide":6,"slide_gap":0.01,"slide_slot_extra":1,"slide_height":0.8,"slide_hex":1,"slide_outer":1,"wedge":36,"dots_hex":3,"dots_bottom":1}
    count: 2
    iteration: "it-988adf359d59"
    verdict: drop
    notes:
      - "3 dots, HEX-WIDE: the rail 6 mm wide"
      - "Row 1: not ticked as staying flat"
      - "Not taken forward: Omar, \"just go with 1 dot\""
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "fd36ae299a118a4f7822e5e046f055907f2fbb42c691b71b7a78b68e31185af4"
    piece: "Hex"
    params: {"size":112.5,"stud":1.2,"stud_gap":0.25,"stud_spacing":6,"stud_ring2":54.4,"stud_ring2_n":10,"stud_ring2_turn":18,"stud_ring3":13,"stud_ring3_n":10,"stud_ring3_turn":18,"stud_ring4":25.1,"stud_ring4_n":10,"stud_ring4_turn":0,"stud_ring5":33.5,"stud_ring5_n":10,"stud_ring5_turn":18,"stud_boss":1,"room":0.2,"gap":0.1,"stud_wall":0.7,"halves":1,"pin":1.2,"pin_gap":0.25,"pins_middle":7,"pins_kite":1,"pins_hex":3,"pins_star":1,"slide":4,"slide_gap":0.01,"slide_slot_extra":1,"slide_height":0.8,"slide_hex":0,"slide_outer":1,"wedge":36,"dots_hex":4,"dots_bottom":1}
    count: 2
    iteration: "it-7927279608c7"
    verdict: drop
    notes:
      - "4 dots, HEX-PINS: three pins in place of the rail"
      - "Row 1: not ticked as staying flat"
      - "Not taken forward: Omar, \"just go with 1 dot\""
readings: []
photos: []
feedback:
  lesson: "On the flange coaster's hexagon piece, the rail at hexfit-1's 0.01 mm a side, 4 mm wide and 0.8 mm tall, stayed flat; a taller rail, a wider rail and pins in its place did no better. hexfit-1's rocking pieces were the 0.15 mm ones, so the loose fit was the rock. 0.4 mm nozzle, 0.42 mm outer and 0.45 mm inner wall lines, 0.20 mm layers"
  decisions: []
  symptom: "Omar ticked only 1 dot as staying flat; on side play, \"they are all very identical, just go with 1 dot\""
  cause: "The up-and-down rock on hexfit-1 came with the 0.15 mm gap; at 0.01 mm a side it is gone without changing the rail"
  next: "The hexagon keeps the rail as it is, at bikar's default 0.01 mm a side (bikar #356). No rail-height, rail-width or pin change; the pin-beside-the-rail bikar change is not needed"
---

Omar tried these pieces by hand after the print of 2026-11-05 and answered both after-print
questions in chat the same evening.

The bed had sixteen hexagon halves from the flange coaster: two copies of each of four versions,
each copy in two halves, told apart by the dots on the lower half's bed face (1 to 4). All four
keep hexfit-1's 0.01 mm gap a side; versions 2 to 4 change the rail.

| Question | Answer | In Omar's words |
|---|---|---|
| 1. Which pieces stay flat when you press each end? | in my words | only 1 dot ticked (the control) |
| 2. Do the taller and wider rails still fit snug side to side? | in my words | "they are all very identical, just go with 1 dot" |

**Read, not said.** Row 1's tick says only the control stayed flat; row 2's words say the four
felt alike. Either way his call is the control, so the three changes are dropped, not judged
worse in every respect.

**The print.** Sent at 21:48 UTC on 2026-11-05 in green from AMS 0 slot 3, finished at 22:15 UTC,
all 17 layers (the [print log](../../design/plates/print-logs/hexfit-2.md)). Nothing was measured
with a tool, so there are no readings and no bet moves.
