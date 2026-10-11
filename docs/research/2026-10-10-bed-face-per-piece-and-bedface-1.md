---
date: 2026-10-10
produced-by: Claude Opus 5.5, building the bedface-1 test plate on Omar's "send the plate" (2026-10-10) and his pick of one plate on the new preset only, in pink. Every number below came from slicing with the installed Bambu Studio CLI and drawing the sliced G-code with `tools/print_review.py paths`. No piece was printed for this file, and no web source was read.
feeds:
  - docs/design/printing/bed-face-slicing-design.md
  - docs/design/plates/bedface-1.md
---

# Bed face: what can be set per piece, and bedface-1 against fit2

Kept verbatim as the record the design doc's §5.2 and the bedface-1 page come from. The slices
and drawings are not checked in: the per-piece test lived in the session's scratch folder, and
the two plate slices are in the gitignored `build/plates/`.

## 1. Which of the three settings Bambu takes per piece

The design's first plan for the test was one plate in two halves: stock settings on one half,
the house settings on the other. That works only if each of the three house settings can be set
on one piece and not the next.

**Method.** A scratch recipe of one kite row (gap 0.05) and one middle piece (gap 0.025), both
at size 112.5, strap 3.75, height 4.4, on the stock `0.20mm Standard @BBL X2D` process, was
composed to a `.3mf` (`base.3mf`). Its `Metadata/model_settings.config` was unpacked, three keys
added under each `<object>` as `<metadata key=… value=…/>`:

```xml
<metadata key="bottom_surface_pattern" value="concentric"/>
<metadata key="infill_wall_overlap" value="30%"/>
<metadata key="initial_layer_line_width" value="0.42"/>
```

and packed back (`mixed2-in.3mf`), then sliced with the Bambu Studio CLI on the same stock
process. The exact slicing command line was not kept. Both slices were drawn with
`print_review.py paths … --below` and measured the same way.

**Result.**

| Piece | Stock, bare share / largest spot (sq mm) | With the per-piece keys | First line width in the G-code |
|---|---|---|---|
| Middle piece (no carved id) | 0.29% / 0.072 | 0.09% / 0.011 | 0.5 on both |
| Kite row | 4.44% / 0.584 | 4.44% / 0.584 | 0.5 on both |

The middle piece took the rings and the overlap: its bottom turned from diagonal lines to rings
and its bare area dropped by two thirds. The kite row did not move at all, since what fills a
kite's core is the narrower first line, and the G-code kept the plate-wide 0.5 width on both
pieces. **So the rings and the overlap can be set per piece; the first line's width cannot.** It
is plate-wide, set by the process.

What this rules out: a two-halves plate can test the rings and the overlap, but not the whole
preset, and not the kites at all. That is why the test became one whole plate on the house
preset (§2).

## 2. bedface-1 against sheets-04g-fit2

bedface-1 is sheets-04g-fit2 piece for piece, in the same places, with the settings line changed
from the X2D's `0.20mm Standard` to `tools/bambu/presets/bed-face-0.20.json`. fit2's slice
(`build/plates/sheets-04g-fit2.plate.3mf`, stock) and bedface-1's
(`build/plates/bedface-1.plate.3mf`, house, sliced 2026-10-10 with
`bambu slice compose docs/design/plates/bedface-1.yaml --plate-type hot_plate`) were each drawn
and measured with:

```
python3 tools/print_review.py paths <out.png> <plate.3mf> 0.2 <x>,<y>,<side> --below --check
```

at 30 px a millimeter, with the same window per piece on both, since both put each piece in the
same place (the windows are the piece centers from `bedface-1.plate.bedmap.json`). The check fails
at 0.6% bare or a largest bare spot of 0.2 sq mm.

| Piece | Window (x, y, side mm) | fit2, stock | bedface-1, house | Check on bedface-1 |
|---|---|---|---|---|
| Coaster | 148.3, 134.4, 118 | 1.10% / 0.677 | 0.26% / 0.160 | PASS |
| Kites | 102.5, 174.6, 46 | 2.25% / 0.619 | 0.33% / 0.089 | PASS |
| Middle 0, id `A` | 192.7, 85.3, 22 | 1.99% / 0.483 | 0.70% / 0.160 | FAIL, share |
| Middle 0.025, id `C` | 175.1, 75.0, 22 | 1.89% / 0.598 | 0.50% / 0.202 | FAIL, spot |
| Middle 0.05, id `E` | 83.7, 140.7, 22 | 1.89% / 0.636 | 0.41% / 0.192 | PASS |

Notes on reading it:

- The coaster's window takes in the edge of a middle piece and a few kites, on both plates alike,
  so its numbers are a little worse than the coaster's own.
- The middle pieces here carry carved ids; the design's sweep measured a middle piece with none
  (0.21% bare on stock, 0.03% on house). The letters are holes the first layer has to turn round,
  and they raise the bare share about tenfold. The house preset still cuts it by about two thirds
  or more, but `A` and `C` stay just over the bars, which were fitted to pieces with no letters.
- The slice, on the house preset: one bed, 67 minutes, about 19 g, no slicer warnings, the three
  house keys read back from the `.3mf`. fit2's stock slice: 67 minutes, 18.9 g.

This is the slicer's plan, not the print. Whether the print matches it is what bedface-1 is for.
