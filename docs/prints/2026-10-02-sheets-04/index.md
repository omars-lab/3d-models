---
run: 2026-10-02-sheets-04
plate: "sheets-04 — the gBV fit: loose pieces at four gaps, set into the baseless minimal coaster"
status: printed
outcome: no-reading
plate_3mf: "sheets-04.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: ~
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand"
pins:
  bikar_ref: 093d4af2e0eec0bc49a800a3277faff349c334bd
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "dc3b7a8dde35113a80faf924a194bc1d7b1822d44b2514a5ee7631c784e95ec9"
    params: {}
    count: 1
    iteration: "it-705defc2be8c"
    verdict: keep
    notes:
      - "no remark on the coaster itself; it is kept as the frame the next pieces plate is set into"
  - entry: "c2"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "b63c517c93ed4e1ad83e0f2e5ab05a074de162ed69b36d74c34c57c5af9ebbf3"
    piece: "Hex"
    params: {"gap": 0.05}
    count: 1
    iteration: "it-9d9715818523"
    verdict: adjust
    notes:
      - "fell right through the coaster's holes (said of all the small pieces)"
  - entry: "c3"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "b63c517c93ed4e1ad83e0f2e5ab05a074de162ed69b36d74c34c57c5af9ebbf3"
    piece: "Hex"
    params: {"gap": 0.1}
    count: 1
    iteration: "it-b1797b7110f5"
    verdict: adjust
    notes:
      - "fell right through the coaster's holes (said of all the small pieces)"
  - entry: "c4"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "b63c517c93ed4e1ad83e0f2e5ab05a074de162ed69b36d74c34c57c5af9ebbf3"
    piece: "Hex"
    params: {"gap": 0.15}
    count: 1
    iteration: "it-91bc136fbd83"
    verdict: adjust
    notes:
      - "fell right through the coaster's holes (said of all the small pieces)"
  - entry: "c5"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "b63c517c93ed4e1ad83e0f2e5ab05a074de162ed69b36d74c34c57c5af9ebbf3"
    piece: "Hex"
    params: {"gap": 0.2}
    count: 1
    iteration: "it-c04b3517cc49"
    verdict: adjust
    notes:
      - "fell right through the coaster's holes (said of all the small pieces)"
  - entry: "c6"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "b63c517c93ed4e1ad83e0f2e5ab05a074de162ed69b36d74c34c57c5af9ebbf3"
    piece: "Star"
    params: {"star_gap": 0.15}
    count: 1
    iteration: "it-02a51ace557a"
    verdict: adjust
    notes:
      - "fell right through the coaster's holes (said of all the small pieces)"
  - entry: "c7"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "b63c517c93ed4e1ad83e0f2e5ab05a074de162ed69b36d74c34c57c5af9ebbf3"
    piece: "Hex"
    params: {"gap": 0.15, "peak": 2}
    count: 1
    iteration: "it-6a6add3ff032"
    verdict: adjust
    notes:
      - "fell right through the coaster's holes (said of all the small pieces)"
      - "Omar wants the next pieces flat, so the peak is not on the next plate"
readings: []
photos: []
feedback:
  lesson: "A coaster with no floor holds a loose piece only by friction, so every piece smaller than its hole fell through, at every gap from 0.05 to 0.20 mm."
  symptom: "all the small pieces fell right through the coaster's holes, at every gap from 0.05 to 0.20 mm"
  cause: "the minimal coaster has no floor (frame F3 in the loose-pieces design), so only friction holds a piece, and every gap on the plate was positive: each piece was smaller than its hole. The loose-pieces design said as much for F3 (pieces drop unless the fit is tight). The pieces were also 1.2 mm thin, so most of each wall was first layers, where elephant-foot compensation (0.15 on this preset) narrows the piece further. Not measured."
  next: "a pieces-only plate (sheets-05) with flat pieces 4 mm tall, flush with the coaster, at gaps from 0.05 down through 0 into a press fit, set into this same coaster"
---

Omar printed this plate on the X2D and judged it by hand, without photos: "all the small pieces
fell right through". He then asked for the next pieces to be "as tall as the minmal construction
piece and flat", and for "a new plate of just small pieces", since he already has the coaster.

He named the fall-through for every small piece, so every piece set carries that note and the
verdict `adjust`: the idea stands, the next print changes the gap and the height. He made no
remark on the coaster itself; it is `keep` because it is the frame the next plate is set into.

**Why they fell.** The baseless minimal coaster is the floorless frame of the loose-pieces
design, so nothing under a piece stops it. With every gap above zero, every piece was smaller
than its hole. The next plate crosses zero into a press fit, where the piece is larger than its
hole and friction holds it.

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate
was built at bikar `093d4af`. Nothing was measured with a tool, so there are no readings and no
bet moves. The filament loaded and the spool were not recorded.
