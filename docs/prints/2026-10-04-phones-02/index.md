---
run: 2026-10-04-phones-02
plate: "phones-02 — phones-01 in pink only, with the small phones 1.25 times wider and longer and twice as thick"
status: printed
outcome: no-reading
plate_3mf: "phones-02.plate.3mf"
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
  bikar_ref: 6629f2455492b0f3cd96392d540f1b4cd3474c0f
  self_ref: ~
objects:
  - entry: "c1"
    source: "3d-models:.bambu/imports/iphone-16-pro-phone.stl"
    source_sha256: "6c0155fcb3d2639796d493b903b4ac6dfbc7aea8467558c1644dd2e63a9dd09b"
    params: {}
    count: 2
    iteration: "it-200048b79232"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"print good\" (said of the whole plate)"
  - entry: "c2"
    source: "3d-models:.bambu/imports/iphone-16-pro-phone.stl"
    source_sha256: "6c0155fcb3d2639796d493b903b4ac6dfbc7aea8467558c1644dd2e63a9dd09b"
    params: {"scale_x": 0.3125, "scale_y": 0.3125, "scale_z": 0.5}
    count: 2
    iteration: "it-9c7f0745141c"
    verdict: keep
    notes:
      - "Omar, in chat after it finished: \"print good\" (said of the whole plate)"
readings: []
photos: []
feedback:
  lesson: "One color per plate: the same phones took about 13 minutes in one color against phones-01's 62 in two, and the plate became the first production plate."
  decisions: [D-098]
  symptom: ~
  cause: ~
  next: "Omar asked to save it as production ready; the plate is promoted, and a reprint goes out on its standing approval"
---

Omar printed this plate on the X2D on 2026-10-04 and judged it by hand, without photos: "print
good, lets save it as prod ready". He said it of the whole plate, so both phone sizes carry the
verdict `keep` and his words.

**How long it took.** The watch started at 14:40 UTC with the print already running, and the
printer said FINISH at 14:53, all 22 layers done (the [print log](../../design/plates/print-logs/phones-02.md)).
That is about 13 to 14 minutes against the slicer's 12. phones-01, the same phones in two colors,
sliced at 22 minutes and took about 62. So nearly all of phones-01's extra time went to the color
swaps.

The source hash and iteration ids are the ones `bambu slice compose` recorded when the plate was
built. The phone file itself is not in git (the repo is public); it sits in the gitignored imports
folder and is held to that hash. Nothing was measured with a tool, so there are no readings and no
bet moves.
