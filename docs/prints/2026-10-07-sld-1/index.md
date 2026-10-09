---
run: 2026-10-07-sld-1
plate: "sld-1 — the dovetail coupon: three rail and slot pairs at 0.10, 0.15 and 0.20 mm a side"
status: printed
outcome: no-reading
plate_3mf: "sld-1.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C"
  spool: "620317506F7D477AB7EB1CD14089FFDA"
  nozzle_mm: 0.4
  nozzle_type: ~
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand"
pins:
  bikar_ref: 951995abe58505b23bb2d80952f4edeb57519b3c
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Coupons/Dovetail-Coupon.bkr"
    source_sha256: "4933520550e5c8021b317785f029f4fae22a623d691328e13b5b7b36a303d4ec"
    piece: "Rail"
    params: {"gap":10}
    count: 1
    iteration: "it-b8fee8931afd"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"alos 10, 15, and 20 all worked ...\" (said of all three gaps)"
  - entry: "c2"
    source: "bikar:patterns/Coupons/Dovetail-Coupon.bkr"
    source_sha256: "4933520550e5c8021b317785f029f4fae22a623d691328e13b5b7b36a303d4ec"
    piece: "Slot"
    params: {"gap":10}
    count: 1
    iteration: "it-6b142f3f8880"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"alos 10, 15, and 20 all worked ...\" (said of all three gaps)"
  - entry: "c3"
    source: "bikar:patterns/Coupons/Dovetail-Coupon.bkr"
    source_sha256: "4933520550e5c8021b317785f029f4fae22a623d691328e13b5b7b36a303d4ec"
    piece: "Rail"
    params: {"gap":15}
    count: 1
    iteration: "it-e4531128a147"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"alos 10, 15, and 20 all worked ...\" (said of all three gaps)"
  - entry: "c4"
    source: "bikar:patterns/Coupons/Dovetail-Coupon.bkr"
    source_sha256: "4933520550e5c8021b317785f029f4fae22a623d691328e13b5b7b36a303d4ec"
    piece: "Slot"
    params: {"gap":15}
    count: 1
    iteration: "it-fc85a8c5c85b"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"alos 10, 15, and 20 all worked ...\" (said of all three gaps)"
  - entry: "c5"
    source: "bikar:patterns/Coupons/Dovetail-Coupon.bkr"
    source_sha256: "4933520550e5c8021b317785f029f4fae22a623d691328e13b5b7b36a303d4ec"
    piece: "Rail"
    params: {"gap":20}
    count: 1
    iteration: "it-5672822dfbaf"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"alos 10, 15, and 20 all worked ...\" (said of all three gaps)"
  - entry: "c6"
    source: "bikar:patterns/Coupons/Dovetail-Coupon.bkr"
    source_sha256: "4933520550e5c8021b317785f029f4fae22a623d691328e13b5b7b36a303d4ec"
    piece: "Slot"
    params: {"gap":20}
    count: 1
    iteration: "it-d04afc8c77fe"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"alos 10, 15, and 20 all worked ...\" (said of all three gaps)"
readings: []
photos: []
feedback:
  lesson: "All three dovetail gaps, 0.10, 0.15 and 0.20 mm a side, worked; which felt best is not said yet. On the glacier plate the printer stopped twice before the first layer, and ran on the gold plate."
  symptom: ~
  cause: ~
  next: "Which of the three gaps felt best is still Omar's to say; the kite pair the joining note adds waits on that gap"
---

Omar printed this plate on the X2D on 2026-10-07 and judged it by hand, without photos: "alos 10,
15, and 20 all worked ...". He said it of all three gaps, so all six halves carry the verdict
`keep` and his words. He did not say which gap felt best, or whether each pair stays together
when shaken, so this record claims only that each pair worked.

**How it went.** It was sent at 18:31 UTC on the smooth light-blue glacier plate. The printer
stopped before the first layer twice: "foreign objects detected on heatbed" (0500-806E) on an
empty plate, then "the print plate marker was not detected" (0500-8062). Omar put the gold
Textured PEI plate in, the print ran from 18:50, and the printer said FINISH at 19:03 with all 12
layers done (the [print log](../../design/plates/print-logs/sld-1.md)). That is about 13 minutes
of printing against the slicer's 12.

The source hash and iteration ids are the ones `bambu slice compose` recorded when the plate was
built. Nothing was measured with a tool, so there are no readings and no bet moves.
