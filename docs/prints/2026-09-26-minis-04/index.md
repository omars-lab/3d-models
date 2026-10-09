---
run: 2026-09-26-minis-04
plate: "minis-04 — minis-03 at 80 mm and half the height, plus the twist"
status: printed
outcome: no-reading
plate_3mf: "minis-04.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: ~
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle (named only: the slice ran about 54 process and 50 filament settings at Studio's built-in defaults, see below)"
  ambient_c: ~
  instrument: "none; judged by eye and hand"
pins:
  bikar_ref: 6356bb3a7f3db2988860a86e7110e30e658a980f
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/GimTvN9hw4U-minimal-frame-coaster.bkr"
    source_sha256: "2ba7481587cb04c22b560ada2e2aff54528b243e7bbb7b6d48e1b342771d42ae"
    piece: "Coaster"
    params: {"size": 80, "height": 1.4}
    count: 1
    iteration: "it-42079dfbceef"
    verdict: adjust
    notes:
      - "tiny holes (said of the print as a whole, not of this piece)"
      - "the change is the slice, not the params: re-slice once the preset chain is flattened"
  - entry: "c2"
    source: "bikar:patterns/Constructions/GimTvN9hw4U-minimal-pegs-coaster.bkr"
    source_sha256: "0568809287585a117d5623f604f9b79177ed1cdc3d18738c4a92392ec3baf501"
    piece: "Coaster"
    params: {"size": 80, "height": 1.4, "clearance": 0.1}
    count: 2
    iteration: "it-0176c7946044"
    verdict: adjust
    notes:
      - "the peg system border is too big"
      - "the pegs are too tight at clearance 0.10 (hand feel, not measured)"
      - "border about 11 mm at these knobs, worked out from the file's frame rule, not measured"
      - "tight has three suspects besides clearance: elephant-foot compensation printed as 0, the slot is not a true offset of the tab (tightest gap about c/2), and height and size changed at the same time"
  - entry: "c3"
    source: "bikar:patterns/Constructions/7apC5Q9QS-8-minimal-frame-coaster.bkr"
    source_sha256: "5e5e8b603c1d0881f67c06403c3103a642530ef0cfb0cdb26d7dd0df9be69d8e"
    piece: "Coaster"
    params: {"size": 80, "height": 1.4}
    count: 1
    iteration: "it-447e3a70a4d2"
    verdict: adjust
    notes:
      - "tiny holes (said of the print as a whole, not of this piece)"
      - "the change is the slice, not the params: re-slice once the preset chain is flattened"
  - entry: "c4"
    source: "bikar:patterns/Constructions/rDuxHF3xMOc-minimal-frame-coaster.bkr"
    source_sha256: "309de6d655cdaeab2eb324da5e5e9d9ff24881bad6c8471461a9251236245699"
    piece: "Coaster"
    params: {"size": 80, "height": 1.4}
    count: 1
    iteration: "it-d5ed5eac9d4a"
    verdict: adjust
    notes:
      - "tiny holes (said of the print as a whole, not of this piece)"
      - "the change is the slice, not the params: re-slice once the preset chain is flattened"
  - entry: "c5"
    source: "bikar:patterns/Constructions/GimTvN9hw4U-twist-coaster.bkr"
    source_sha256: "bfc6befbb6f8f146b1ff46f8063542b0f705ae31c87f9358fbe96af487f2a728"
    piece: "Coaster"
    params: {"size": 80, "strap": 1.6, "height": 4, "twist": 4}
    count: 1
    iteration: "it-5d90d82d2dd4"
    verdict: adjust
    notes:
      - "tiny holes (said of the print as a whole, not of this piece)"
      - "the change is the slice, not the params: re-slice once the preset chain is flattened"
readings: []
photos: []
feedback:
  lesson: "A slice must carry the whole X2D preset: Studio's command line ignores `inherits`, and its built-in settings fit the tiny holes and the tight pegs."
  symptom: "tiny holes in the print; the pegs pair's border is too big and the pegs fit too tight"
  cause: "the slice ran on Studio's built-in defaults, not the X2D preset: our slicer passed only the top preset file and Studio's command line does not follow `inherits`, so elephant-foot compensation was 0 (preset 0.15), the top was 4 layers / 0.6 mm (preset 5 / 1.0), walls were Arachne and the top zig-zag. The holes fit those settings; the tight pegs fit compensation 0 plus the slot shape; the border is the dovetail frame rule by design. Causes ranked in docs/design/printing/print-quality-design.md; none measured."
  next: "flatten the preset chain and re-slice minis-04 to compare previews; fix the slot offset in bikar; then a clearance ladder at 1.4 mm (T1) before CAL-FIT-01 moves; the narrower joins are on minis-05 and minis-06"
---

Omar printed this plate on the X2D and judged it by hand, without photos (typos fixed): "i see
tiny holes on the print and the peg system border is too big and pegs too tight".

He named the holes for the print as a whole, not per piece. So every piece carries that note as
his plate-wide remark, and every verdict is `adjust`: the right idea, but the next print needs a
different slice. Only the pegs pair also needs a change to the piece itself.

**The slice did not use the preset it names.** `tools/bambu` gave Bambu Studio's command line
only the top preset file, and the command line ignores `inherits` (BambuStudio #6836). About 54
process and 50 filament settings fell back to Studio's built-in values. So this plate, like
minis-03, says nothing reliable about clearance or strap width on the real X2D preset. The
diagnosis and the fix order are in [`print-quality-design.md`](../../design/printing/print-quality-design.md).

One thing is unknown: whether Omar's send from Bambu Studio re-sliced the file. If it did, the
desktop app would have followed `inherits`, and the settings above would not describe the print.

The source hashes and iteration ids come from re-composing the plate from its file at bikar
`6356bb3`. Every mesh in that `.3mf` matches the printed `.bambu/plates/minis-04.plate.3mf`
vertex for vertex, so they describe the pieces that were printed. No draft was scaffolded at
the time. The filament loaded and the spool were not recorded.

Nothing was measured with a tool, so there are no readings and no bet moves.
