---
run: 2026-10-12-bedface-2
plate: "bedface-2 — two gBV coasters on one bed, stock beside rings and a 30% overlap, both at the stock 0.5 mm first line"
status: printed
outcome: no-reading
plate_3mf: "bedface-2.plate.3mf"
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
  instrument: "none; judged by hand and two photos"
pins:
  bikar_ref: c0e6563afc856be8f881b5059766f689821fd932
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    count: 1
    iteration: "it-09ad7b8d8d11"
    verdict: keep
    notes:
      - "The coaster carved S, on the stock settings: diagonal lines on the first layer, as on fit2's Z. Its bottom has short dark slits running along the straps, a line or two in from each edge, where the diagonal fill turns short of the wall (the photo)"
      - "Omar, with the photo: \"these are the slits fot s\""
      - "Omar, asked whether R has fewer slits than S: \"About the same\", then \"both have slits, byt in different places\""
      - "The page's row 1 reads \"the same\" as: the coaster stays on stock. So S is what keeps printing, slits and all; the slits Omar asked about on 2026-10-10 are not fixed by this plate"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    count: 1
    iteration: "it-62ce032b2a1e"
    verdict: drop
    notes:
      - "The coaster carved R: the same design, with rings on the first layer and the fill pushed 30% into the wall, on this coaster alone, at the stock 0.5 mm first line. The strap edges are closed, but small dark specks and triangles run down the middle of the straps and sit where straps meet, where the rings from the two sides come together (the photo), the same places bedface-1's F showed them"
      - "Omar, with the photo: \"this for r\""
      - "Omar, beside S: \"About the same\", then \"both have slits, byt in different places\""
      - "The page's row 1 reads \"the same\" as: the rings' meeting lines open in print at either line width, so rings are dropped for good. The drop is on the first-layer settings, not on the design, which prints on as S"
      - "Row 2 (are the dashes on F only, on both, or on neither?) and row 3 (does FC1 1E feel the same in S's middle hole as in R's?) were not judged yet"
readings: []
photos:
  - file: photos/s-coaster-bed-face.jpg
    sha256: af0f5584ac9671666c6d5ca44f1dc6fcd5a9670185cd8f09a80098816861b558
    of: "the S coaster's bottom, close up: short dark slits along each strap, a line or two in from the edges, where the diagonal fill meets the wall loops"
    why: "shows where the stock first layer leaves bed bare in print: along the strap edges, as the slicer's plan drew it"
  - file: photos/r-coaster-bed-face.jpg
    sha256: 87a7f0efe2526f499b69f1a208a44c4c113c40b4597c331275f96eb049b1b69c
    of: "the R coaster's bottom, close up, the carved R near the bottom: rings along every strap, with small dark specks and triangles down the strap middles and where straps meet"
    why: "shows that at the stock line width the rings still leave bed bare where they meet, so the slits move from the edges to the middles rather than go away"
feedback:
  lesson: "Rings did not clean the coaster's bottom at the stock 0.5 mm first line either: Omar found the ring coaster and the stock coaster about the same, \"both have slits, but in different places\". On stock the slits run along the strap edges; with rings they move to the strap middles and to where straps meet, where the rings from the two sides come together. So bedface-1's dashes were not the narrow line's doing, and rings are dropped (0.4 mm nozzle, 0.5 mm first line, 0.42 mm outer and 0.45 mm inner wall lines, 0.20 mm layers, glacier plate sliced as Smooth PEI)"
  decisions: []
  symptom: "S: slits along the strap edges. R: specks and small triangles down the strap middles and at the junctions. About the same amount on each, in different places"
  cause: "Rings leave a meeting line down the middle of each strap and at each junction, and it opens in print at the 0.5 mm line as it did at 0.42, so the narrower line (the issue's second suspect) is cleared of bedface-1's dashes and where rings meet (the first) is what stands. The slicer's plan had R at 0.41% bare against S's 0.93%, so for the second plate running the plan ranked the ring bottom cleaner than the print. The glacier plate's missing 0.02 mm push (the third suspect) was the same for both coasters, so it is still untested"
  next: "Rings and the 30% overlap are not used; every plate stays on the X2D 0.20 mm Standard, as the page's row 1 said for this answer. Whether to keep chasing the stock slits, and how, is Omar's call from the issue's remaining options (docs/issues/bed-face-preset-failed-in-print.md)"
---

Omar judged this plate by hand on 2026-10-12 and sent one photo of each coaster's bottom. The rows
of the page's [After the print](../../design/plates/bedface-2.md#after-the-print) table were asked
in turn.

- **`R` against `S`: about the same, in different places.** Asked whether `R` has fewer slits than
  `S`: "About the same", and then "both have slits, byt in different places". The photos show
  where. On `S` the slits run along each strap, a line or two in from the edge, where the diagonal
  fill turns short of the wall. On `R` the edges are closed, and the specks and small triangles sit
  down the middle of the straps and where straps meet, where the rings from the two sides come
  together: the same places bedface-1's `F` showed them, now at the stock line width.
- **`R` against bedface-1's `F`:** not judged yet.
- **`FC1 1E` in `S` and in `R`:** not judged yet.

![The S coaster's bottom: slits along the strap edges](photos/s-coaster-bed-face.jpg)

![The R coaster's bottom: specks and triangles down the strap middles and where straps meet, the carved R near the bottom](photos/r-coaster-bed-face.jpg)

Both photos were re-saved with no metadata, so they carry no location, and the `R` photo was cut
off just below the coaster's carved letter to leave out the hand holding it.

**What the answer means, as the page set it out before the print.** "The same or more: the rings'
meeting lines open in print at either width. Rings are dropped for good and the coaster stays on
stock." So the narrower first line was not what made bedface-1's dashes; where the rings meet is.
And the slicer's plan ranked the ring bottom cleaner than stock for the second plate running (0.41%
bare against 0.93%), where the print found them about even. What is left open, and Omar's to pick,
is in [the issue](../../issues/bed-face-preset-failed-in-print.md#2026-10-12-bedface-2-rings-move-the-slits-they-do-not-close-them).

**Two prints, one record.** The plate printed twice, from the same slice, in the same pink, on the
same glacier plate: first sent at 21:33 UTC on 2026-10-11 and FINISH at 23:33, then, on Omar's
"reprint", sent at 02:59 on 2026-10-12 and FINISH at 04:59. Each took 120 minutes against the
slicer's 107, with all 22 layers done (the [print log](../../design/plates/print-logs/bedface-2.md)),
and each has its own timelapse on [the page](../../design/plates/bedface-2.md#the-print). Why he
asked for the reprint was not said in chat, and which print's pair the photos show was not said
either, so this one record holds the pair he judged. The other pair is not judged.

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built, at bikar `c0e6563a`. The sends ran from an older bikar checkout (`951995ab`), which does not
change what printed: the printer got the sliced file made at `c0e6563a`. Nothing was measured
with a tool, so there are no readings and no bet moves.
