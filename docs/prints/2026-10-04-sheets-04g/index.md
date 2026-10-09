---
run: 2026-10-04-sheets-04g
plate: "sheets-04g — the gBV minimal coaster at 1.25 times wide and every one of its 41 pieces, one bed, one color"
status: printed
outcome: no-reading
plate_3mf: "sheets-04g.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "Bambu PLA Basic, Bambu Green (#00AE42)"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  layer_mm: 0.2
  slicer_profile: "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D"
  ambient_c: ~
  instrument: "none; judged by hand"
pins:
  bikar_ref: 6629f2455492b0f3cd96392d540f1b4cd3474c0f
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "dc3b7a8dde35113a80faf924a194bc1d7b1822d44b2514a5ee7631c784e95ec9"
    params: {"size": 112.5, "strap": 3.75, "height": 4.4, "round": 1.25}
    count: 1
    iteration: "it-cc3bad1e83d1"
    verdict: not-judged
    notes:
      - "no remark on the coaster itself yet"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "df89bf7cbb6d88f5abdfa437d3deda74012637c339899baf9f711b408c177228"
    piece: "Middle"
    params: {"size": 112.5, "strap": 3.75, "height": 4.4, "gap": 0}
    count: 1
    iteration: "it-ed01da2eed5b"
    verdict: adjust
    notes:
      - "adn the middle piece was too lose"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "df89bf7cbb6d88f5abdfa437d3deda74012637c339899baf9f711b408c177228"
    piece: "Kite"
    params: {"size": 112.5, "strap": 3.75, "height": 4.4, "gap": 0}
    count: 10
    iteration: "it-224e295566b5"
    verdict: adjust
    notes:
      - "the small kits were too tight ti fit"
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "df89bf7cbb6d88f5abdfa437d3deda74012637c339899baf9f711b408c177228"
    piece: "Hex"
    params: {"size": 112.5, "strap": 3.75, "height": 4.4, "gap": 0}
    count: 10
    iteration: "it-4d1db932eb53"
    verdict: not-judged
    notes:
      - "no remark yet"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "df89bf7cbb6d88f5abdfa437d3deda74012637c339899baf9f711b408c177228"
    piece: "Star"
    params: {"size": 112.5, "strap": 3.75, "height": 4.4, "gap": 0}
    count: 10
    iteration: "it-13e25f7b7efd"
    verdict: not-judged
    notes:
      - "no remark yet"
  - entry: "c6"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"
    source_sha256: "df89bf7cbb6d88f5abdfa437d3deda74012637c339899baf9f711b408c177228"
    piece: "Outer"
    params: {"size": 112.5, "strap": 3.75, "height": 4.4, "gap": 0}
    count: 10
    iteration: "it-4b194bef17f6"
    verdict: not-judged
    notes:
      - "no remark yet"
readings: []
photos: []
feedback:
  lesson: "A piece cut with sharp inward corners rattles where the strap rounds its hole, and the thinnest, sharpest pieces (the kites) bind first."
  symptom: "the ten kites were too tight to go into their holes, and the middle piece was loose in its hole; nothing said yet about the hexes, the stars, the outer pieces or the coaster"
  cause: "two causes, one per symptom. The middle piece was cut with sharp inward corners, but the coaster's strap rounds those corners off, so at each of its ten inward corners the piece stood 0.45 mm short of the wall: play the piece could rattle in. The kites had no play anywhere, and a kite is the thinnest piece on the plate, with 3.8 times as much edge for its size as the middle piece and a 36 degree point, so any width the printer adds to a piece, or takes from a hole, binds it first. Measured on bikar's own geometry and the slice; the printer's own widening was not measured."
  next: "bikar now cuts every piece along the strap's real, rounded edge (no more corner play), and a fit plate, sheets-04g-fit, tries kites at five gaps and middle pieces at four in this same coaster"
---

Omar printed this plate on the X2D on 2026-10-04 and judged two of its pieces by hand, without
photos. His words: "in our olast print, the small kits were too tight ti fit" and "adn the middle
piece was too lose".

The ten kites (`c3`) and the middle piece (`c2`) carry his words and the verdict `adjust`: the
idea stands, and the next print changes the fit. He said nothing yet about the hexes, the stars,
the outer pieces or the coaster, so those are `not-judged`, a verdict that waits for his word
rather than one written for him.

**Why.** The two complaints have different causes, and
[the issue write-up](../../issues/sheets-04g-fit.md) has the measurements. In short: the middle
piece had sharp corners where its hole is round, which left 0.45 mm of play at each of ten
corners. The kites had no play at all, and they have the most edge for their size and the
sharpest points, so they are the first to bind.

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate
was built at bikar `6629f24`. Nothing was measured on the print with a tool, so there are no
readings and no bet moves. The print log, with the times, is
[sheets-04g's log](../../design/plates/print-logs/sheets-04g.md).
