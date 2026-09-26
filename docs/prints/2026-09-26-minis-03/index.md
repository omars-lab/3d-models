---
run: 2026-09-26-minis-03
plate: "minis-03 — openwork minis at 40 mm"
status: printed
outcome: no-reading
plate_3mf: "minis-03.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA (pink in the photos; the .3mf carries the Bambu PLA Basic preset)"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  layer_mm: 0.2
  slicer_profile: "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D"
  ambient_c: ~
  instrument: "none; judged by eye and hand from Omar's photos"
pins:
  bikar_ref: 383c0a14a62ca39f5903da6b257d0518b3a97405
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/GimTvN9hw4U-minimal-frame-coaster.bkr"
    source_sha256: "b6e587693459580a31bd4286218b9ecdc4bd7c4ea39e7054f285217ae9ae0a2a"
    piece: "Coaster"
    params: {"size": 40, "strap": 1.6}
    count: 1
    iteration: "it-f69105def119"
    verdict: adjust
    notes:
      - "good start: the pattern reads"
      - "much too small at 40 mm"
  - entry: "c2"
    source: "bikar:patterns/Constructions/GimTvN9hw4U-minimal-pegs-coaster.bkr"
    source_sha256: "78460be4e2899f0850049896cff19d172e858fbd2edddb96f686c30db0d5a70f"
    piece: "Coaster"
    params: {"size": 40, "strap": 1.6}
    count: 2
    iteration: "it-e2c3a07302be"
    verdict: adjust
    notes:
      - "much too small at 40 mm"
      - "mated, big spaces between the patterns: two 5.7 mm frames leave about 11 mm of solid at the join"
      - "a bit loose at the file's default clearance 0.15 mm (hand feel, not measured)"
  - entry: "c3"
    source: "bikar:patterns/Constructions/7apC5Q9QS-8-minimal-frame-coaster.bkr"
    source_sha256: "c9f5beddd4294e41f307b451c1de2798a257d717d34530302c1bc9470ff92ada"
    piece: "Coaster"
    params: {"size": 40, "strap": 1.6}
    count: 1
    iteration: "it-3195d0da18ab"
    verdict: adjust
    notes:
      - "good start: the pattern reads"
      - "much too small at 40 mm"
  - entry: "c4"
    source: "bikar:patterns/Constructions/rDuxHF3xMOc-minimal-frame-coaster.bkr"
    source_sha256: "ff4baf23c74f3c0132acca25822172aae18082a944145eb92e71e779c6b6d7b1"
    piece: "Coaster"
    params: {"size": 40, "strap": 1.6}
    count: 1
    iteration: "it-c4434e7b7e15"
    verdict: adjust
    notes:
      - "good start: the pattern reads"
      - "much too small at 40 mm"
readings: []
photos:
  - file: photos/plate-overview.jpg
    sha256: 0e602c262e2dfb2d9b98d3c81c6529d473801394a6d9d4a1a7419ef1aaf48be9
    of: "all five pieces, the pegs pair pushed together at the top"
    why: "shows the size and the solid band at the pegs join"
  - file: photos/pegs-pair-and-cs1.jpg
    sha256: eb442a03f67a7ec01bca5c6f9dd1ad5db871974deffc0ffdcc7e0c57cce025c4
    of: "the CS-1 minimal-frame close up, the mated pegs pair behind it"
    why: "shows how the openwork reads at 40 mm"
feedback:
  symptom: "minis too small; the mated pegs pair has a wide solid band at the join and fits a bit loose"
  cause: "size 40 is too small to show the pattern; the pegs frame is a fixed 5.7 mm per side, so the band is over a quarter of a 40 mm piece; clearance 0.15 mm is loose on this machine by feel"
  next: "next sample plate at 70 mm; pegs pairs at clearance 0.10 and 0.05; try a shallower dovetail (depth 2) for a narrower frame"
---

Omar printed this plate on the X2D on 2026-09-26, sent from Bambu Studio, and judged it from
the pieces in hand (typos fixed; "at .4" read as 40 mm): "Good start but the minis at 40 were
much too small. Also the interlocking
ones, once interlocked, have big spaces between the patterns and are a bit loose."

Nothing was measured with a tool, so there are no readings and no bet moves. The clearance
note is a hand-feel reading for CAL-FIT-01, not a settled number. The 11 mm band is worked out
from the file's frame rule (`depth + clearance + 2.5`, twice), not measured on the part.

The plate was sliced green in the `.3mf`. The filament actually loaded (pink) was mapped in
Bambu Studio at send time, and the spool was not recorded.

The plate was composed from a bikar branch commit (`db68768a`) that the squash merge of bikar
#251 replaced. `pins.bikar_ref` names that merge on bikar main instead. The four pattern files
hash the same at both commits, so the pieces are the ones printed.

The lessons went into the print-coaster-samples skill's `sample-rules.md` and the review-print
rubric (3d-models #326).
