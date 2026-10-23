---
run: 2026-10-23-split-04
plate: "split-04 — three slices of the flange coaster, every piece kind in a border held by four 1.7 mm pins, at piece gaps 0.25, 0.15 and 0.10 mm"
status: printed
outcome: no-reading
plate_3mf: "split-04.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, green #00AE42"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: "HS01"
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand, in chat"
pins:
  bikar_ref: 03f7119599cf408a2d2ceb95c54a98b72bc46c15
  self_ref: ~
objects:
  # set 7, gap 0.25 (split-02's gap, the control)
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Lower"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.25,"id":7}
    count: 1
    iteration: "it-66825298027d"
    verdict: adjust
    notes:
      - "Set 7's lower half, its 7 on the bottom, four 1.7 mm pins on its outer part"
      - "Omar: \"the border sides with pins are flush, without are not\"; \"we need more pints all the way around border\""
      - "Omar, asked whether the halves show a space with and without the pieces in: \"Space only where no pin\". The space comes from the unpinned sides lifting, not from the pieces standing tall"
      - "Verdict adjust: pins on every side of the border"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Upper"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.25,"id":7}
    count: 1
    iteration: "it-d4f23f1dbe4c"
    verdict: adjust
    notes:
      - "Set 7's upper half, a hole for each pin"
      - "Omar: \"the border sides with pins are flush, without are not\"; \"Space only where no pin\""
      - "Verdict adjust, as the lower half: pins on every side"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Middle"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.25,"id":7}
    count: 1
    iteration: "it-78d646e4a9d2"
    verdict: drop
    notes:
      - "The middle piece at gap 0.25, carved A"
      - "Omar: \"set 7 is very loose\""
      - "Verdict drop at this gap: 0.25 rattles, as on split-02. The piece goes on at 0.10 (set 9)"
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Kite"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.25,"id":7}
    count: 1
    iteration: "it-262064ed735e"
    verdict: drop
    notes:
      - "The kites at gap 0.25, no id, kept with set 7 from the bed map"
      - "Omar: \"set 7 is very loose\""
      - "Verdict drop at this gap"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Hex"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.25,"id":7}
    count: 1
    iteration: "it-1f4f12c5dfc1"
    verdict: drop
    notes:
      - "The inner hex at gap 0.25, carved E"
      - "Omar: \"set 7 is very loose\""
      - "Verdict drop at this gap"
  - entry: "c6"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Star"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.25,"id":7}
    count: 1
    iteration: "it-5855de0a77fd"
    verdict: drop
    notes:
      - "The star at gap 0.25, no id, kept with set 7 from the bed map"
      - "Omar: \"set 7 is very loose\""
      - "Verdict drop at this gap"
  - entry: "c7"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Outer"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.25,"id":7}
    count: 1
    iteration: "it-1fcbfa99f4fc"
    verdict: drop
    notes:
      - "The outer piece at gap 0.25, carved F"
      - "Omar: \"set 7 is very loose\""
      - "Verdict drop at this gap"
  # set 8, gap 0.15
  - entry: "c8"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Lower"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.15,"id":8}
    count: 1
    iteration: "it-0362b716a20d"
    verdict: adjust
    notes:
      - "Set 8's lower half, its 8 on the bottom"
      - "Omar: \"the border sides with pins are flush, without are not\"; \"Space only where no pin\""
      - "Verdict adjust: pins on every side of the border"
  - entry: "c9"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Upper"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.15,"id":8}
    count: 1
    iteration: "it-ac9be7b6f1c9"
    verdict: adjust
    notes:
      - "Set 8's upper half"
      - "Omar: \"the border sides with pins are flush, without are not\""
      - "Verdict adjust: pins on every side"
  - entry: "c10"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Middle"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.15,"id":8}
    count: 1
    iteration: "it-c94077d5519e"
    verdict: drop
    notes:
      - "The middle piece at gap 0.15, carved C"
      - "Omar, on set 8: \"better but stil a little wiggle\""
      - "Verdict drop at this gap: set 9 at 0.10 went in by hand and does not wiggle, so 0.15 is not needed"
  - entry: "c11"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Kite"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.15,"id":8}
    count: 1
    iteration: "it-cecbff2a0b15"
    verdict: adjust
    notes:
      - "The kites at gap 0.15, no id"
      - "Omar, on set 8: \"better but stil a little wiggle\"; on set 9 at 0.10: \"some peices were tight (small kite)\""
      - "Verdict adjust: the kite's gap lies between 0.10 (tight) and 0.15 (a little wiggle), so the kite may want its own gap; not measured"
  - entry: "c12"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Hex"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.15,"id":8}
    count: 1
    iteration: "it-a4369227fa5e"
    verdict: drop
    notes:
      - "The inner hex at gap 0.15, carved J"
      - "Omar, on set 8: \"better but stil a little wiggle\""
      - "Verdict drop at this gap: 0.10 is snug"
  - entry: "c13"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Star"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.15,"id":8}
    count: 1
    iteration: "it-39298db505c7"
    verdict: drop
    notes:
      - "The star at gap 0.15, no id"
      - "Omar, on set 8: \"better but stil a little wiggle\""
      - "Verdict drop at this gap: 0.10 is snug"
  - entry: "c14"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Outer"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.15,"id":8}
    count: 1
    iteration: "it-e4e6fbcbc0dd"
    verdict: drop
    notes:
      - "The outer piece at gap 0.15, carved K"
      - "Omar, on set 8: \"better but stil a little wiggle\""
      - "Verdict drop at this gap: 0.10 is snug"
  # set 9, gap 0.10
  - entry: "c15"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Lower"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":9}
    count: 1
    iteration: "it-3750657fa853"
    verdict: adjust
    notes:
      - "Set 9's lower half, its 9 on the bottom"
      - "Omar: \"the border sides with pins are flush, without are not\"; \"Space only where no pin\"; \"we need more pints all the way around border\""
      - "Verdict adjust: pins on every side of the border"
  - entry: "c16"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Upper"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":9}
    count: 1
    iteration: "it-764e4cf85ab1"
    verdict: adjust
    notes:
      - "Set 9's upper half"
      - "Omar: \"the border sides with pins are flush, without are not\""
      - "Verdict adjust: pins on every side"
  - entry: "c17"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Middle"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":9}
    count: 1
    iteration: "it-a67be021fcf4"
    verdict: keep
    notes:
      - "The middle piece at gap 0.10, carved L"
      - "Omar, on set 9: \"in by hand, all snug\"; \"no shaking on last one\""
      - "Verdict keep: 0.10 is the middle's gap"
  - entry: "c18"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Kite"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":9}
    count: 1
    iteration: "it-8baf923efcc9"
    verdict: adjust
    notes:
      - "The kites at gap 0.10, no id"
      - "Omar, on set 9: \"in by hand, all snug, but some peices were tight (small kite)\""
      - "Verdict adjust: it goes in, but tight; a little more gap for the small kite only. How much is not measured: somewhere under 0.15, where set 8 wiggled"
  - entry: "c19"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Hex"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":9}
    count: 1
    iteration: "it-91e33f2c4492"
    verdict: keep
    notes:
      - "The inner hex at gap 0.10, carved T"
      - "Omar, on set 9: \"in by hand, all snug\"; \"no shaking on last one\""
      - "Verdict keep: 0.10 is the hex's gap"
  - entry: "c20"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Star"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":9}
    count: 1
    iteration: "it-a054f144d2f5"
    verdict: keep
    notes:
      - "The star at gap 0.10, no id"
      - "Omar, on set 9: \"in by hand, all snug\" (he named only the small kite as tight); \"no shaking on last one\""
      - "Verdict keep: 0.10 is the star's gap"
  - entry: "c21"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "8993f777966c014a510e2071f9bfcfb8b5174dd849b79d489c831eb359ab0007"
    piece: "Outer"
    params: {"size":112.5,"stud":1.7,"stud_gap":0.25,"stud_spacing":10,"room":0.2,"wedge":72,"wedge_from":9,"wedge_center":1,"gap":0.1,"id":9}
    count: 1
    iteration: "it-0056e3a87c17"
    verdict: keep
    notes:
      - "The outer piece at gap 0.10, carved U"
      - "Omar, on set 9: \"in by hand, all snug\"; \"no shaking on last one\""
      - "Verdict keep: 0.10 is the outer piece's gap"
readings: []
photos: []
feedback:
  lesson: "In a pinned border, a 0.10 mm gap per face gives the middle, hex, star and outer pieces a snug fit that goes in by hand and does not rattle; the small kite is tight at 0.10. At 0.15 the pieces still wiggle a little, and at 0.25 they are very loose. The halves close flush only on the sides that have a pin: with four 1.7 mm pins on the slice's outer part, the unpinned sides lift and leave a space (0.4 mm nozzle, 0.20 mm layers, setting 8, sliced as Smooth PEI for the glacier plate)"
  decisions: []
  symptom: "Set 7 (0.25): very loose. Set 8 (0.15): a little wiggle. Set 9 (0.10): in by hand, snug, no rattle when shaken, the small kite tight. The halves: flush where a pin is, a space where none is, with or without the pieces in. The bands: clean, as on split-02"
  cause: "Not measured. The space follows the pins, not the pieces: it is there with no pieces in, only on the unpinned sides, so the 0.2 mm the pieces were shortened did its job and the halves need holding all round. Why the kite alone is tight at 0.10 is not known; its sharp tips leave least room, as the page expected"
  next: "Every piece kind except the kite keeps 0.10 mm. The kite adjusts: a little more gap than 0.10, under 0.15. The halves adjust: pins on every side of the border, Omar's words \"we need more pints all the way around border\". The pins fit in the middle's border is still open: no 1.7 mm pin fits there, so pins all round likely means a smaller pin. Setting 8 stays for split coasters, pieces included. What prints next is Omar's call"
---

Omar judged this plate on 2026-10-23 in chat, from the pieces in hand. His answers are on the
page's [Judged](../../design/plates/split-04.md#judged) table, word for word.

The bed had three sets, each in its own block: set 7 on the left at a 0.25 mm gap per face, set
8 in the middle at 0.15 mm, set 9 on the right at 0.10 mm.

| Part | In Omar's words | What it means |
|---|---|---|
| Set 7's pieces (0.25) | "set 7 is very loose" | 0.25 is out, as split-02 already showed |
| Set 8's pieces (0.15) | "better but stil a little wiggle" | 0.15 is out |
| Set 9's pieces (0.10) | "in by hand, all snug, but some peices were tight (small kite)"; "no shaking on last one" | 0.10 is the gap for the middle, hex, star and outer pieces; the kite needs a little more |
| The halves | "Space only where no pin" | the space follows the pins, not the pieces |
| The pins | "the border sides with pins are flush, without are not"; "we need more pints all the way around border" | pins on every side of the border |
| The bands | "Clean, same as split-02" | setting 8 stays for split coasters |

**Not asked.** Row 1, whether any stars or kites got mixed up between sets: Omar judged set by
set, so the sets were kept apart, but nobody asked. Row 5's other parts were not asked either:
whether a closed set stays shut when turned over, and whether the border round the middle flexes.

**The slice.** Sliced 2026-10-23 at 03:39 UTC for the glacier plate as Smooth PEI, with the X2D
preset and PLA Basic, each set laid out in a block of its own, no slicer warnings. The record's
pieces, hashes and iterations come from the earlier slice that night, from the same recipe and
the same bikar commit (#342, still bikar main's tip when the plate was sent). The send's own
draft named an older bikar commit, the shared checkout's, which did not build this plate.

**The print.** Sent at 03:41 UTC on 2026-10-23 in green from AMS 0 slot 3, finished at 05:31 UTC,
all 21 layers (the [print log](../../design/plates/print-logs/split-04.md)). Every chamber picture
looked clean. Nothing was measured with a tool, so there are no readings and no bet moves.
