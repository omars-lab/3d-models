---
run: 2026-10-03-sheets-04b
plate: "sheets-04b — the gBV fit again, pieces only: hexagons and stars 4 mm tall, the gap from 0.05 mm down through zero into a press fit"
status: printed
outcome: no-reading
plate_3mf: "sheets-04b.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C"
  spool: "620317506F7D477AB7EB1CD14089FFDA"
  nozzle_mm: 0.4
  nozzle_type: ~
  nozzle_side: ~
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; nothing was judged piece by piece"
pins:
  bikar_ref: 4e06255df394f0167012b305d0983eab0b3cddd1
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "f721e943a4a2a066f4c6d458104a8fd9b00fd77c66d9f82d11fd4dc0050bb633"
    piece: "Hex"
    params: {"height":4,"gap":0.05}
    count: 1
    iteration: "it-802f83fe6550"
    verdict: not-judged
    notes:
      - "HEX +05: ten hexagons 0.05 mm smaller than the hole, in the middle row of the bed"
      - "Not asked whether it stays in the coaster"
  - entry: "c2"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "f721e943a4a2a066f4c6d458104a8fd9b00fd77c66d9f82d11fd4dc0050bb633"
    piece: "Hex"
    params: {"height":4,"gap":0}
    count: 1
    iteration: "it-67d6ed539337"
    verdict: not-judged
    notes:
      - "HEX 00: ten hexagons the size of the hole, alone in the front row of the bed"
      - "Omar, some time after the print: \"in the experiment the bottom row fir bitter in minimal construction\". Which pieces he meant by the bottom row is not written down; the front row of the bed map is this set. sheets-04g took no gap from it"
      - "Not a verdict: he compared the fit, he did not say keep, change or drop"
  - entry: "c3"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "f721e943a4a2a066f4c6d458104a8fd9b00fd77c66d9f82d11fd4dc0050bb633"
    piece: "Hex"
    params: {"height":4,"gap":-0.05}
    count: 1
    iteration: "it-6462f59c068e"
    verdict: not-judged
    notes:
      - "HEX -05: ten hexagons 0.05 mm larger than the hole, in the back row of the bed"
      - "Not asked whether it goes in and stays"
  - entry: "c4"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "f721e943a4a2a066f4c6d458104a8fd9b00fd77c66d9f82d11fd4dc0050bb633"
    piece: "Hex"
    params: {"height":4,"gap":-0.1}
    count: 1
    iteration: "it-e34611d6aa4e"
    verdict: not-judged
    notes:
      - "HEX -10: ten hexagons 0.10 mm larger than the hole, in the back row of the bed"
      - "Not asked whether it goes in and stays"
  - entry: "c5"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "f721e943a4a2a066f4c6d458104a8fd9b00fd77c66d9f82d11fd4dc0050bb633"
    piece: "Star"
    params: {"height":4,"star_gap":0}
    count: 1
    iteration: "it-1690a8c84d2b"
    verdict: not-judged
    notes:
      - "STAR 00: ten small stars the size of the hole, in the middle row of the bed"
      - "Not asked whether they press in or a tip breaks"
  - entry: "c6"
    source: "bikar:patterns/Coupons/Loose-Fit-Coupon.bkr"
    source_sha256: "f721e943a4a2a066f4c6d458104a8fd9b00fd77c66d9f82d11fd4dc0050bb633"
    piece: "Star"
    params: {"height":4,"star_gap":-0.05}
    count: 1
    iteration: "it-947d5ebd4720"
    verdict: not-judged
    notes:
      - "STAR -05: ten small stars 0.05 mm larger than the hole, in the back row of the bed"
      - "Not asked whether they press in or a tip breaks"
readings: []
photos: []
feedback:
  lesson: "The second send printed all 20 layers. The fit questions were never asked one by one; Omar's one recorded word on it is that the bottom row fit better in the minimal coaster"
  decisions: []
  symptom: "The first send stopped at layer 0: the slice was made for a Cool Plate and a Textured PEI Plate was on the bed (0500-8051), and the print was cancelled (0300-400C). Re-sliced for Textured PEI, the second send finished"
  cause: "The first send's slice named the wrong plate type; written up in docs/issues/sliced-for-wrong-plate.md"
  next: "D-109 prints sheets-04b again with carved ids, as a new iteration, and judges it then. sheets-04g already took no gap from Omar's word"
---

Written on 2026-10-22, nineteen days after the print, from the page, the print log and Omar's
words in the repo. Nobody asked the page's three
[After the print](../../design/plates/sheets-04b.md#after-the-print) questions at the time, so
every set stays `not-judged`.

**Two sends, one print.**

- **The first send** went out on 2026-10-03 and stopped at layer 0. The printer said the plate on
  the bed was not the one the file was sliced for (0500-8051), and the print was cancelled at
  20:12 UTC (0300-400C). Nothing printed. The plate was sliced again for the Textured PEI plate
  and got a new yes ([the issue](../../issues/sliced-for-wrong-plate.md)).
- **The second send** printed. The watch picked it up at 22:34 UTC at layer 5 of 20, and the
  printer said FINISH at 23:05 UTC, all 20 layers (the
  [print log](../../design/plates/print-logs/sheets-04b.md)).

This record is the second send. The first printed nothing, so it has no record of its own.

**What Omar said.** One line, quoted on [sheets-04g](../../design/plates/sheets-04g.md#what-it-is):
"in the experiment the bottom row fir bitter in minimal construction". sheets-04g read it as no
gap between a piece and its hole. That fits the bed map, where HEX 00 is alone in the front row.
But he did not say which pieces he meant, and he compared the fit rather than judging a set. So it
is a note on HEX 00, not a verdict.

**Not known.**

- Which set falls out, which stays and which will not go in.
- Whether a star tip broke.
- When Omar said the line above, and where he first said it. Only the sheets-04g quote is in the repo.

**What comes next.** D-109 prints sheets-04b again with carved ids, as a new iteration, and judges
that print instead. Nothing was measured with a tool, so there are no readings and no bet moves:
CAL-FIT-01 and CAL-HOL-01 stay where they were.
