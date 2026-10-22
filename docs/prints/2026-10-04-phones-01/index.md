---
run: 2026-10-04-phones-01
plate: "phones-01 — four mini iPhones, two at the sheets-04d size and two at a quarter of it, pink and black"
status: printed
outcome: no-reading
plate_3mf: "phones-01.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C and black #000000"
  spool: "620317506F7D477AB7EB1CD14089FFDA (pink); the black spool was not recorded"
  nozzle_mm: 0.4
  nozzle_type: ~
  nozzle_side: ~
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; nothing was judged piece by piece"
pins:
  bikar_ref: 6629f2455492b0f3cd96392d540f1b4cd3474c0f
  self_ref: ~
objects:
  - entry: "c1"
    source: "3d-models:.bambu/imports/iphone-16-pro-phone.stl"
    source_sha256: "6c0155fcb3d2639796d493b903b4ac6dfbc7aea8467558c1644dd2e63a9dd09b"
    piece: "PINK PHONE"
    params: {}
    count: 1
    iteration: "it-200048b79232"
    verdict: not-judged
    notes:
      - "The full-size phone in pink, slot 1"
      - "Omar said nothing about how it came out; his next plate, phones-02, printed it again unchanged, in pink only"
  - entry: "c2"
    source: "3d-models:.bambu/imports/iphone-16-pro-phone.stl"
    source_sha256: "6c0155fcb3d2639796d493b903b4ac6dfbc7aea8467558c1644dd2e63a9dd09b"
    piece: "BLACK PHONE"
    params: {}
    count: 1
    iteration: "it-200048b79232"
    verdict: not-judged
    notes:
      - "The full-size phone in black, slot 2"
      - "Omar said nothing about how it came out"
  - entry: "c3"
    source: "3d-models:.bambu/imports/iphone-16-pro-phone.stl"
    source_sha256: "6c0155fcb3d2639796d493b903b4ac6dfbc7aea8467558c1644dd2e63a9dd09b"
    piece: "PINK QUARTER"
    params: {"scale":0.25}
    count: 1
    iteration: "it-bc286ef2c2a9"
    verdict: adjust
    notes:
      - "The quarter-size phone in pink, slot 1, about 4.2 x 10 x 1.2 mm"
      - "Omar, after phones-01 printed: \"I want to make the itiny phone a bit bigger - 1.25x their lenght and width and 2x their thickness\""
      - "Verdict adjust: the same phone at bigger params, which phones-02 printed"
  - entry: "c4"
    source: "3d-models:.bambu/imports/iphone-16-pro-phone.stl"
    source_sha256: "6c0155fcb3d2639796d493b903b4ac6dfbc7aea8467558c1644dd2e63a9dd09b"
    piece: "BLACK QUARTER"
    params: {"scale":0.25}
    count: 1
    iteration: "it-bc286ef2c2a9"
    verdict: adjust
    notes:
      - "The quarter-size phone in black, slot 2"
      - "Omar, after phones-01 printed: \"I want to make the itiny phone a bit bigger - 1.25x their lenght and width and 2x their thickness\""
      - "Verdict adjust, as the pink quarter phone"
readings: []
photos: []
feedback:
  lesson: "A two-color plate on the X2D took about 62 minutes against the slicer's 22: one color swap on each of its 22 layers, about 1.6 minutes a swap, which the slicer does not count. Omar dropped plates that switch colors after it"
  decisions: []
  symptom: "It printed to the end, all 22 layers, about three times the sliced time"
  cause: "The color swaps: a nozzle change, a reheat and a prime tower pass on every layer"
  next: "phones-02 printed the same phones in pink only, with the quarter phones 1.25 times wider and longer and twice as thick, at Omar's ask"
---

Written on 2026-10-22, eighteen days after the print, from the page, the print log and Omar's
words in the repo. Nobody asked the page's two
[After the print](../../design/plates/phones-01.md#after-the-print) questions at the time, so
they have no answer here.

**The print.** Sent by `bambu print send` on 2026-10-04 and watched from 12:53 UTC. The printer
said FINISH at 13:55 UTC, all 22 layers (the
[print log](../../design/plates/print-logs/phones-01.md)). That is about 62 minutes against the
slicer's 22.

**What Omar said.** Two things, both right after it finished:

- On the color swaps: "i want the color swtichign to be saved as a memory - it results in alot
  more waste and slower prints". He then dropped plates that switch colors.
- On the quarter phones: "I want to make the itiny phone a bit bigger - 1.25x their lenght and
  width and 2x their thickness". That is the source of the two `adjust` verdicts.

He said nothing about the full-size phones, so they stay `not-judged`. phones-02 printed them
again unchanged, in pink only, and became the first production plate
([its record](../2026-10-04-phones-02/index.md)).

**Not known.**

- Whether each phone came out in its own color, the page's first question. Nobody asked it.
- Which black spool fed slot 2, and which nozzle went with which color.

**The source.** The source hash and iteration ids are the ones `bambu slice compose` recorded
when the plate was built. The phone file is not in git, because the repo is public. It sits in
the gitignored imports folder, held to that hash. Nothing was measured with a tool, so there are
no readings and no bet moves.
