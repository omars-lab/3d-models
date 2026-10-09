---
run: 2026-10-09-pkt-1
plate: "pkt-1 — the pocket coupon: does a piece printed in its pocket come out loose"
status: printed
outcome: no-reading
plate_3mf: "pkt-1.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand"
pins:
  bikar_ref: a03d104023723b55dc3573dd33ce21bf42fa92a4
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Lower"
    params: {"air":0.2,"thick":0.6,"pair":15}
    count: 1
    iteration: "it-4a4a24310294"
    verdict: drop
    notes:
      - "Carved id 4S (pair O). Its hexagon printed fused to the square: one layer of air (0.2 mm) is not enough"
      - "Omar, in chat: \"Fused in both pairs\", then \"s and p are fused\""
  - entry: "c2"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Upper"
    params: {"air":0.2,"thick":0.6,"pair":15}
    count: 1
    iteration: "it-c73b1e1e6e58"
    verdict: drop
    notes:
      - "Upper OT (pair O, no bed-face id). Fused, as 4S"
      - "Omar, in chat, asked by id: none of 4S, OT, 4P, PT moves (\"None move: all four fused\")"
  - entry: "c3"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Lower"
    params: {"air":0.2,"thick":0.6,"pair":16}
    count: 1
    iteration: "it-7299e718c1b2"
    verdict: drop
    notes:
      - "Carved id 4P (pair P). Fused, as 4S: the second pair at one layer of air fused too, so it was not one bad layer"
      - "Omar, in chat: \"s and p are fused\""
  - entry: "c4"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Upper"
    params: {"air":0.2,"thick":0.6,"pair":16}
    count: 1
    iteration: "it-895f440ccd9d"
    verdict: drop
    notes:
      - "Upper PT (pair P, no bed-face id). Fused, as 4P"
  - entry: "c5"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Lower"
    params: {"air":0.4,"thick":0.4,"pair":17}
    count: 1
    iteration: "it-18310649100e"
    verdict: keep
    notes:
      - "Carved id 4Q (pair Q). The hexagon moves at two layers of air (0.4 mm); the 0.4 mm rim round it is whole; the band is level"
      - "Omar, in chat: \"i mean , q and r have slight movement\"; rims: \"All four rims whole\"; band: \"Level in all four\""
  - entry: "c6"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Upper"
    params: {"air":0.4,"thick":0.4,"pair":17}
    count: 1
    iteration: "it-3f48be5c84b3"
    verdict: keep
    notes:
      - "Upper QT (pair Q). Moves slightly, rim whole, band level. Closed onto 4Q it sits flat with no gap at the cut and makes no sound when tipped"
      - "Omar, in chat, of 4Q onto QT and 4R onto RT: \"Flat and silent, both\""
  - entry: "c7"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Lower"
    params: {"air":0.4,"thick":0.4,"pair":18}
    count: 1
    iteration: "it-a07aface014e"
    verdict: keep
    notes:
      - "Carved id 4R (pair R). Moves slightly, rim whole, band level"
      - "Omar, in chat: \"r might have been the best fit\". Pair R has the same settings as pair Q, so the difference is between two prints of one design, not between two designs"
  - entry: "c8"
    source: "bikar:patterns/Coupons/Split-Pocket-Coupon.bkr"
    source_sha256: "a0433d5a226a35d726edd6cdf307626ce53e959f4ddcb6362d8c76a9ae2c6fb0"
    piece: "Upper"
    params: {"air":0.4,"thick":0.4,"pair":18}
    count: 1
    iteration: "it-1c6fcf7449c1"
    verdict: keep
    notes:
      - "Upper RT (pair R). Moves slightly, rim whole, band level. Closed onto 4R it sits flat and silent"
      - "Omar, in chat: \"r might have been the best fit\""
readings: []
photos: []
feedback:
  lesson: "A piece printed in its pocket comes out loose with two layers of air (0.4 mm); with one layer (0.2 mm) both pairs fused (0.4 mm nozzle, 0.42 mm outer and 0.45 mm inner wall lines, 0.20 mm layers)."
  symptom: "At one layer of air (0.2 mm) the hexagon printed fused to its square in both pairs (4S/OT, 4P/PT)"
  cause: "One 0.2 mm layer of air is too little for the band to print free; both pairs fused, so it was not one bad layer"
  next: "Way c works at two layers of air (0.4 mm) with 0.4 mm necks and the 0.6 mm band: loose, rims whole, band level, and closed pairs flat and silent. pkt-2 builds there"
---

Omar judged this plate by hand on 2026-10-08, the evening it printed. It has no photos, and every
answer was asked by the id cut into the tile, one question at a time.

- **One layer of air (0.2 mm), pairs O and P: fused.** None of `4S`, `OT`, `4P` or `PT` moves.
  Both pairs fused, so it was not one bad layer: one layer of air is out. Those four halves carry
  `drop`.
- **Two layers of air (0.4 mm), pairs Q and R: loose.** The hexagons in `4Q`, `QT`, `4R` and `RT`
  move slightly. The 0.4 mm rim round each hexagon is whole, and the band inside is level in all
  four. Closed, `4Q` onto `QT` and `4R` onto `RT` both sit flat with no gap at the cut, and make no
  sound when tipped. Those four halves carry `keep`. Omar added "r might have been the best fit".
  Q and R share the same settings, so that difference is between two prints, not two designs.

The page expected a click once the halves were closed, and there was none. That is the lesson to
carry forward: at two layers of air the closed pocket holds its piece without glue.

**How it went.** It was sent at 00:38 UTC on 2026-10-09 (19:38 local on the 8th), in pink, on the
smooth light-blue glacier plate. The printer said FINISH at 01:19 with all 18 layers done (the
[print log](../../design/plates/print-logs/pkt-1.md)). That is about 42 minutes against the
slicer's 35, with no error and nothing lifting in the chamber pictures.

The source hash and iteration ids are the ones `bambu slice compose` recorded when the plate was
built. Nothing was measured with a tool, so there are no readings and no bet moves. The spool's id
was not logged at the send.
