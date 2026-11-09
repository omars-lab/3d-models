---
run: 2026-11-08-fidget-star-1
plate: "fidget-star-1 — the 8-point fidget star on a plate of its own"
plate_3mf: "fidget-star-1.plate.3mf"
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
  instrument: "none; turned by hand, answered on the hub"
pins:
  bikar_ref: fe6b109e1bdb22fbfe6dbe2863b5dfa4e5b49a0a
  self_ref: ~
objects:
  - entry: "c1"
    source: "3d-models:.bambu/imports/8pt-fidget-star.stl"
    source_sha256: "4ac4e45a65a3336d6098bf1e02a83f63e8cc7b57c87cc8e02f8c971f87c21340"
    params: {}
    count: 1
    iteration: "it-e613b42a4157"
    verdict: keep
    notes:
      - "A downloaded print-in-place star (not ours), rings nested, no supports"
      - "Row 1, Omar: Free (the rings turn freely; no words added)"
      - "Not said: whether it moved more easily than toys-1's star, which printed with supports on"
photos: []
readings: []
feedback:
  lesson: "The 8-point fidget star's nested rings turned freely when printed with no supports; toys-1 printed it with supports on for the whole plate. 0.4 mm nozzle, 0.20 mm layers, Bambu PLA Basic"
  decisions: []
  symptom: "Omar: Free"
  cause: "With supports off, nothing is printed in the gaps between the rings, so they stay apart"
  next: "Print more stars like this, with no supports"
---

Omar turned the star after the print and answered its one question on the hub's judging page
on 2026-11-09.

The bed had one piece: the 8-point fidget star, a downloaded print-in-place mesh kept out of git
and pinned by its sha256. It has no carved id. It printed with no supports, so nothing sat in the
gaps between its rings.

| Question | Answer | In Omar's words |
|---|---|---|
| 1. Do the star's rings turn? | Free | — |

The question also asked to compare it with toys-1's star. The answer doesn't say, so the record
makes no claim about it.

**The print.** Sent at 15:57 UTC on 2026-11-08 in green from AMS 0 slot 3, 29.34 g by the slice.
Finished at 17:03 UTC, all 90 layers (the [print log](../../design/plates/print-logs/fidget-star-1.md)).
Nothing was measured with a tool, so there are no readings and no bet moves.
