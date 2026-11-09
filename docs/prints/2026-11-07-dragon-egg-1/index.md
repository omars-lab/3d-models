---
run: 2026-11-07-dragon-egg-1
plate: "dragon-egg-1 — one small dragon egg, in silk blue"
plate_3mf: "dragon-egg-1.plate.3mf"
status: printed
outcome: no-reading
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Silk, blue #0047BB"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Silk @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; looked at by hand, answered on the hub"
pins:
  bikar_ref: fe6b109e1bdb22fbfe6dbe2863b5dfa4e5b49a0a
  self_ref: ~
objects:
  - entry: "c1"
    source: "3d-models:.bambu/imports/mini-twisted-dragon-egg.stl"
    source_sha256: "661d14f093b960560e4399648eb4cd4f5584b0a1490dcdac9a7f49533a1fde73"
    params: {}
    count: 1
    iteration: "it-c32f8973ea83"
    verdict: keep
    notes:
      - "A downloaded egg mesh (not ours), standing up, no supports"
      - "Row 1, Omar: Clean (the scale tips came out clean; no words added)"
photos: []
readings: []
feedback:
  lesson: "The Mini Twisted Dragon Egg printed clean standing up with no supports, though the slicer warned about scale tips starting in the air. 0.4 mm nozzle, 0.20 mm layers, Bambu PLA Silk"
  decisions: []
  symptom: "Omar: Clean"
  cause: "The scale tips overhang little enough to bridge from the layer below; the slicer's warning counts any tip that starts in the air"
  next: "Print more eggs as they are: the same file, standing up, no supports"
---

Omar looked at the egg after the print and answered its one question on the hub's judging page
on 2026-11-09.

The bed had one piece: the Mini Twisted Dragon Egg, a downloaded mesh kept out of git and
pinned by its sha256. It has no carved id. It printed standing up with no supports, as its maker
prints it.

| Question | Answer | In Omar's words |
|---|---|---|
| 1. Do the scales come out clean, or do some tips droop or string? | Clean | — |

**The print.** Sent at 02:58 UTC on 2026-11-07 in silk blue from AMS 0 slot 1, 15.6 g by the
slice. Finished at 04:21 UTC, all 178 layers (the [print log](../../design/plates/print-logs/dragon-egg-1.md)).
Nothing was measured with a tool, so there are no readings and no bet moves.
