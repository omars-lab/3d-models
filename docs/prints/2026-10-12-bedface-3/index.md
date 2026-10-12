---
run: 2026-10-12-bedface-3
plate: "bedface-3 — bedface-2's two gBV coasters again, stock beside rings and a 30% overlap, on the gold Textured PEI plate"
status: printed
outcome: no-reading
plate_3mf: "bedface-3.plate.3mf"
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
  instrument: "none; judged by hand and two photos of the bottoms"
pins:
  bikar_ref: c0e6563afc856be8f881b5059766f689821fd932
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    count: 1
    iteration: "it-fd63b94a0d96"
    verdict: adjust
    notes:
      - "The coaster carved G, on the stock settings, sliced for and printed on the gold Textured PEI plate, which starts the first layer 0.02 mm closer to the bed than bedface-2's glacier plate. Its bottom is grainy all over, the gold plate's texture, with short dark slits along the inside of the outer edge in one star point (the photo)"
      - "Omar, with the photo: \"this is g, its better, but one corner had skits\""
      - "Omar, asked whether G has fewer slits than bedface-2's S: \"Fewer\""
      - "Omar, asked whether the gold plate's grain is fine on a coaster: \"Not fine\""
      - "The page's rows read these as: the plate was part of the cause (row 1, fewer), but the gold plate is out even though it closes slits (row 3, not fine). So the design prints on, and what changes is how the first layer meets the smooth plate; how to change it is Omar's call. That is why the verdict is adjust, on the setup, not on the design"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    count: 1
    iteration: "it-3a0db11abc35"
    verdict: drop
    notes:
      - "The coaster carved K: the same design, with rings on the first layer and the fill pushed 30% into the wall, on this coaster alone, on the gold plate. Its bottom is grainy, with short dark dashes down the middle of the straps and where straps meet, where the rings from the two sides come together (the photo), the same places bedface-2's R showed them"
      - "Omar, with the photo: \"this is k, it had a good amount of slit\""
      - "Omar, asked whether K has fewer specks than bedface-2's R: \"Fewer\""
      - "The page's row 2 reads \"fewer\" as: rings might come back, on the gold plate only. Row 3 put the gold plate out, so rings stay dropped. The drop is on the first-layer settings, not on the design, which prints on as G and S"
readings: []
photos:
  - file: photos/g-coaster-bed-face.jpg
    sha256: 9d4828dcf259145a8e5407a4c5f09cc279af989ed7ee19cec364139232672aef
    of: "one star point of the G coaster's bottom, close up: the gold plate's grain over the whole face, and short dark slits along the inside of the outer edge"
    why: "shows the one corner Omar named, and the grain row 3 found not fine on a coaster"
  - file: photos/k-coaster-bed-face.jpg
    sha256: 577324a0a61eb25d702477a1d64315534c2d1778e3a151d39b6932b0fd68646d
    of: "the K coaster's bottom, most of it, the carved K left of center: grain all over, with short dark dashes down the strap middles and where straps meet"
    why: "shows the rings' meeting lines still open on the gold plate, fewer than on R but, in Omar's words, a good amount"
  - file: photos/g-layer2-on-the-bed.jpg
    sha256: 1ecf4c5f9023b25105bac8126325133170c44488c2cb07d161d9fa371b44ac63
    of: "the G coaster on the gold plate during the print, from above, after the first layers: the walls and the diagonal fill inside each strap, the carved G near the top"
    why: "Omar's own look during the print; the top of the early layers, not the bottom the rows ask about"
  - file: photos/k-layer2-on-the-bed.jpg
    sha256: 7b42eed9797ccaeeb2ea6369d100d4ba8c2494d8be94feda215d477a7a4b314d
    of: "the K coaster on the gold plate during the print, from above, after the first layers: the walls and fill inside each strap, the carved K near the top"
    why: "Omar's own look during the print; the top of the early layers, not the bottom the rows ask about"
feedback:
  lesson: "Starting the first layer on the gold plate, 0.02 mm closer to the bed than on the glacier plate, left fewer slits on both coasters: Omar found G better than bedface-2's S, with one corner still slit, and K better than R, though still with a good amount. But the gold plate's grain is not fine on a coaster, so the gold plate is out. What carries forward is the squish, not the plate (0.4 mm nozzle, 0.5 mm first line, 0.20 mm layers, sliced as the Textured PEI plate, which lowers the nozzle 0.02 mm for the first layer)"
  decisions: []
  symptom: "G: slits along the inside of the outer edge in one star point, fewer than S. K: dashes down the strap middles and where straps meet, fewer than R. Both bottoms grainy from the plate"
  cause: "The plate was the only change from bedface-2, and both coasters had fewer slits, so the glacier plate's missing 0.02 mm push (the issue's third suspect) is part of the cause. Not the whole: G still has a slit corner and K a good amount. Changing the plate also changed the surface the first layer lands on, so the 0.02 mm and the texture are not told apart by this print"
  next: "The gold plate is out (row 3) and rings stay dropped (row 2 depends on the gold plate). Whether to get the same closer first layer on the smooth glacier plate, and how, is Omar's call from the issue (docs/issues/bed-face-preset-failed-in-print.md)"
---

Omar judged this plate by hand on 2026-10-12 and sent one photo of each coaster's bottom. The rows
of the page's [After the print](../../design/plates/bedface-3.md#after-the-print) table were asked
one at a time.

- **`G` against bedface-2's `S`: fewer.** With the photo: "this is g, its better, but one corner
  had skits". The photo is that corner: short dark slits along the inside of the outer edge, in
  one star point. The rest of the bottom is the gold plate's grain.
- **`K` against bedface-2's `R`: fewer.** With the photo: "this is k, it had a good amount of
  slit". The dashes sit where `R`'s did: down the middle of the straps and where straps meet,
  where the rings from the two sides come together.
- **`G`'s grain: not fine.** The gold plate is out, even though it closes slits.

![One star point of the G coaster's bottom: the gold plate's grain, and short slits along the inside of the outer edge](photos/g-coaster-bed-face.jpg)

![The K coaster's bottom, the carved K left of center: dashes down the strap middles and where straps meet](photos/k-coaster-bed-face.jpg)

Omar also sent two photos during the print, of each coaster's top after the first layers:

![The G coaster on the gold plate during the print, from above](photos/g-layer2-on-the-bed.jpg)

![The K coaster on the gold plate during the print, from above](photos/k-layer2-on-the-bed.jpg)

All four photos were re-saved with no metadata, so they carry no location. The `G` bottom photo
was cut down to the one star point, which leaves out the hand holding the coaster. The `K` photo
was cut off just below the coaster.

**What the answers mean, as the page set them out before the print.**

- Row 1, "Fewer": "the plate was part of the cause, and coasters print on the gold plate."
- Row 2, "Fewer": "rings might come back, on the gold plate only."
- Row 3, "Not fine": "the gold plate is out even if it closes the slits."

Row 3 overrules the second half of row 1 and all of row 2. So the plate is out and rings stay
dropped. What stands is the first half of row 1: the 0.02 mm the glacier plate misses is part of
the cause. It is not all of it, since `G` still has a slit corner. Changing the plate also changed
the surface the first layer lands on, so this print does not tell the closer nozzle apart from the
texture. What to try next, and whether to, is Omar's call, set out in
[the issue](../../issues/bed-face-preset-failed-in-print.md#2026-10-12-bedface-3-fewer-slits-on-the-gold-plate-but-the-plate-is-out).

**The print.** Sent at 15:41 UTC, FINISH at 17:42: 120 minutes against the slicer's 107, all 22
layers, no pause or error (the [print log](../../design/plates/print-logs/bedface-3.md)). The
timelapse is on [the page](../../design/plates/bedface-3.md#the-print).

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built, at bikar `c0e6563a`. The send ran from an older bikar checkout (`951995ab`), which does not
change what printed: the printer got the sliced file made at `c0e6563a`. Nothing was measured with
a tool, so there are no readings and no bet moves.
