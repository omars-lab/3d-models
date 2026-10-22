---
run: 2026-10-04-sheets-04c
plate: "sheets-04c — the gBV minimal coaster alone, 90 mm, a second one of the coaster sheets-04 printed"
status: printed
outcome: no-reading
plate_3mf: "sheets-04c.plate.3mf"
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
  instrument: "none; nothing was judged"
pins:
  bikar_ref: 8936c8bd550f4a0dadf05c3926cc6f5c0f0918fd
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "dc3b7a8dde35113a80faf924a194bc1d7b1822d44b2514a5ee7631c784e95ec9"
    params: {}
    count: 1
    iteration: "it-0d140d733625"
    verdict: not-judged
    notes:
      - "The gBV minimal coaster at the file's own settings: 90 mm across, 3 mm straps, 4 mm tall, no floor"
      - "Not asked whether the sheets-04b pieces fit it the same as the first one. The 2026-10-06 open calls 8a and 8b would have asked; they were replaced on 2026-10-08 by a reprint with carved ids, judged then"
readings: []
photos: []
feedback:
  lesson: "It printed to the end, all 20 layers, as sheets-04 did. Nothing was judged, so it says nothing yet about whether hole size moves from print to print"
  decisions: []
  symptom: ~
  cause: ~
  next: "D-109 prints sheets-04c again with carved ids, as a new iteration, and judges it then. sheets-04g has since printed the same coaster at 112.5 mm"
---

Written on 2026-10-22, eighteen days after the print, from the page, the print log and the open
calls. Nobody asked the page's one
[After the print](../../design/plates/sheets-04c.md#after-the-print) question, whether the
sheets-04b pieces fit this coaster the same as the first one. So the coaster stays `not-judged`.

**The print.** Sent by `bambu print send` on 2026-10-03, in pink. The watch started at 00:32 UTC
on 2026-10-04, and the printer said FINISH at 01:20 UTC, all 20 layers (the
[print log](../../design/plates/print-logs/sheets-04c.md)). That is about 48 minutes against the
slicer's 42.

**Why it was not judged.** The 2026-10-06 open calls had two questions on it, 8a and 8b. They were
never asked. On 2026-10-08 they were replaced by a reprint of sheets-04c with carved ids, to be
judged then (D-109).

**Not known.** How the coaster came out, and whether the sheets-04b pieces fit it. Nothing was
measured with a tool, so there are no readings and no bet moves.
