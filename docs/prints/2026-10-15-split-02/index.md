---
run: 2026-10-15-split-02
plate: "split-02 — the split gBV coaster whose loose pieces carry a flange (option C), 112.5 mm, no studs"
status: printed
outcome: no-reading
plate_3mf: "split-02.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C"
  spool: "620317506F7D477AB7EB1CD14089FFDA"
  nozzle_mm: 0.4
  nozzle_type: "HS01"
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand, on the hub's judging page and in chat"
pins:
  bikar_ref: 11ea0fd008053ca53cc237cfe0becb104f2dc3d5
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "0cc6a7761859468b7e2f733a6ee1739d3f49403a4b2190a46d56a26efb4756dd"
    piece: "Lower"
    params: {"size":112.5,"id":2}
    count: 1
    iteration: "it-c3b6ab1683d9"
    verdict: adjust
    notes:
      - "The lower half, its id 2 cut 2 mm tall into its bottom face"
      - "Omar, asked whether the closed halves stay together with no glue: \"Come apart\"; and later: \"also the two hafs have a space inbetween them\""
      - "The page set \"Come apart\" to mean the flange needs glue (split design call 3), which counts against the flange in D-100"
      - "Omar, asked whether the 2 on its bottom reads: \"Not\". The page set that to mean the flange coaster's id goes somewhere else, decided before its next iteration"
      - "Omar, asked whether the pieces sit level on each face: \"Flush\""
      - "Verdict adjust: the halves do not hold and the id does not read; what replaces them is open"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "0cc6a7761859468b7e2f733a6ee1739d3f49403a4b2190a46d56a26efb4756dd"
    piece: "Upper"
    params: {"size":112.5,"id":2}
    count: 1
    iteration: "it-463f0a7348a5"
    verdict: adjust
    notes:
      - "The upper half, no id, printed face down"
      - "Omar: \"Come apart\"; \"also the two hafs have a space inbetween them\""
      - "Omar, on the faces with the pieces in: \"Flush\""
      - "Verdict adjust, as the lower half: the two halves do not stay together"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "0cc6a7761859468b7e2f733a6ee1739d3f49403a4b2190a46d56a26efb4756dd"
    piece: "Middle"
    params: {"size":112.5,"id":2}
    count: 1
    iteration: "it-27a81fdf840f"
    verdict: adjust
    notes:
      - "The twenty-sided middle piece, carved SP2 over 5 M"
      - "Omar, asked whether the band's underside is clean: \"Clean or a slight droop\". The page set that to mean the flange can be built as drawn"
      - "Omar, asked whether the pieces sit level with the straps: \"Flush\""
      - "Omar, asked whether the pieces wiggle or rattle once closed: \"Loose\", in his words \"they do; and when i shake it makes a shound ...; also there is a margin around stars, kite, etc\""
      - "The page set \"Loose\" to mean a smaller gap round the pieces (0.25 mm now), as a new iteration"
      - "Verdict adjust: the gap round the piece"
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "0cc6a7761859468b7e2f733a6ee1739d3f49403a4b2190a46d56a26efb4756dd"
    piece: "Kite"
    params: {"size":112.5,"id":2}
    count: 1
    iteration: "it-212bcd9fac9b"
    verdict: adjust
    notes:
      - "The ten small four-sided kites, no id"
      - "Omar: \"Clean or a slight droop\"; \"Flush\""
      - "Omar, on the wiggle: \"Loose\", and \"also there is a margin around stars, kite, etc\": the kites are named"
      - "Verdict adjust: a smaller gap round the piece"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "0cc6a7761859468b7e2f733a6ee1739d3f49403a4b2190a46d56a26efb4756dd"
    piece: "Hex"
    params: {"size":112.5,"id":2}
    count: 1
    iteration: "it-da269151485d"
    verdict: adjust
    notes:
      - "The inner ring of ten six-sided pieces, each carved 5H"
      - "Omar: \"Clean or a slight droop\"; \"Flush\"; on the wiggle: \"Loose\""
      - "Verdict adjust: a smaller gap round the piece"
  - entry: "c6"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "0cc6a7761859468b7e2f733a6ee1739d3f49403a4b2190a46d56a26efb4756dd"
    piece: "Star"
    params: {"size":112.5,"id":2}
    count: 1
    iteration: "it-1baf9ee124af"
    verdict: adjust
    notes:
      - "The ten ten-pointed stars, no id"
      - "Omar: \"Clean or a slight droop\"; \"Flush\""
      - "Omar, on the wiggle: \"Loose\", and \"also there is a margin around stars, kite, etc\": the stars are named"
      - "Verdict adjust: a smaller gap round the piece"
  - entry: "c7"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr"
    source_sha256: "0cc6a7761859468b7e2f733a6ee1739d3f49403a4b2190a46d56a26efb4756dd"
    piece: "Outer"
    params: {"size":112.5,"id":2}
    count: 1
    iteration: "it-c1039d62078d"
    verdict: adjust
    notes:
      - "The outer ring of ten six-sided pieces, each carved 5R"
      - "Omar: \"Clean or a slight droop\"; \"Flush\"; on the wiggle: \"Loose\""
      - "Verdict adjust: a smaller gap round the piece"
readings: []
photos: []
feedback:
  lesson: "The flange holds a loose piece flush on both faces, and its 0.8 mm band prints with at most a slight droop underneath; but at 0.25 mm all round the pieces are loose in their holes and rattle when the coaster is shaken, with a margin Omar could see round the stars and kites. With no studs and no glue the two halves come apart, with a space between them, and a 2 mm id under the undercut strip does not read (0.4 mm nozzle, 0.20 mm layers, sliced as a Smooth PEI / High Temp plate)"
  decisions: []
  symptom: "The bands' undersides: clean or a slight droop. The pieces: flush on both faces, but loose, rattling when shaken, a visible margin round the stars and kites. The halves: come apart on their own, a space between them. The lower half's 2: not readable"
  cause: "Not measured. The page expected a little play from the 0.25 mm gap and doubted friction alone would hold the halves; both came out worse than a little. Why there is a space between the halves (a piece standing taller than its pocket, or the cut faces not flat) is not known: Omar said the faces are flush, and nobody measured the gap"
  next: "Every piece adjust: a smaller gap round the pieces, as a new iteration, as the page set \"Loose\" to mean. Both halves adjust: the page set \"Come apart\" to mean the flange needs glue (split design call 3), which counts against the flange in D-100, Omar's call with split-01. The id moves off the lower half's bottom before the next iteration. What prints next is Omar's call"
---

Omar judged this plate on 2026-10-22, rows 1 to 4 on the hub's judging page and row 5 in chat,
one row of the page's [After the print](../../design/plates/split-02.md#after-the-print) table at a
time. His answers are on the page's [Judged](../../design/plates/split-02.md#judged) table, word
for word. Row 5, whether the pieces wiggle, was added after the print, at his word: "on split 02,
i wasnt asked if the peices wiggle".

- **Row 1, every piece, the band's underside:** "Clean or a slight droop". The page set this to
  mean the flange can be built as drawn.
- **Row 2, the pieces in the halves, the faces:** "Flush". The flange keeps today's look on both
  faces, its case in D-100.
- **Row 3, the closed halves, no glue:** "Come apart", and later "also the two hafs have a space
  inbetween them". The page set "Come apart" to mean the flange needs glue (split design call 3),
  which counts against it in D-100.
- **Row 4, the `2` on the lower half's bottom:** "Not". The id goes somewhere else, decided
  before the next iteration.
- **Row 5, the closed coaster held shut, do the pieces move:** "Loose". In his words: "they do;
  and when i shake it makes a shound ...; also there is a margin around stars, kite, etc". The
  page set "Loose" to mean a smaller gap round the pieces, as a new iteration.

| Part | In Omar's words | What the page set that answer to mean |
|---|---|---|
| The bands (every piece) | clean or a slight droop | the flange builds as drawn |
| The faces, pieces in | flush | today's look on both faces |
| The pieces in their holes | loose; rattles when shaken; a margin round the stars and kites | a smaller gap, new iteration |
| The two halves | come apart; a space between them | needs glue, against the flange in D-100 |
| The `2` on the bottom | not readable | the id moves |

**What stands.** The flange did the part it was for: the pieces sit flush on both faces and the
band prints. What failed is the fit round it: the pieces are loose, and the halves neither stay
together nor close up tight. D-100, lip or flange, is still Omar's call, beside
[split-01](../../design/plates/split-01.md), which has not printed yet.

**Not known.** Why there is a space between the halves. Omar said the faces are flush, so it is
not obvious that a piece holds them apart; nobody measured it. No photos were sent for this plate.

**The slice.** Sliced 2026-10-15 at 20:22 UTC for the glacier plate as Smooth PEI, with the X2D
preset and PLA Basic, 112 minutes and 31.8 g, no slicer warnings. The send went out two minutes
later, so the slice the printer got is the one this record's hashes come from.

**The print.** Sent at 20:24 UTC on 2026-10-15, in pink from AMS 0 slot 0. The watch lost the
printer at 22:03 UTC, at about half way, and found it finished, all 22 layers, at 23:49 UTC (the
[print log](../../design/plates/print-logs/split-02.md)), so when it finished between those times
is not known. The timelapse is on [the page](../../design/plates/split-02.md#the-print). Nothing
was measured with a tool, so there are no readings and no bet moves.
