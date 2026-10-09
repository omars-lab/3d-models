---
run: 2026-10-09-spl-1
plate: "spl-1 — the split coupon: how tight a stud, how thick a floor, does a lip hold a piece"
status: printed
outcome: no-reading
plate_3mf: "spl-1.plate.3mf"
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, pink #F5547C"
  spool: "620317506F7D477AB7EB1CD14089FFDA"
  nozzle_mm: 0.4
  nozzle_type: ~
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "0.20mm Standard @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; judged by hand"
pins:
  bikar_ref: 7bc3ba54b3c838dcee41007ca4db755641622aed
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"gap":-0.1,"pair":1}
    count: 1
    iteration: "it-eba23c424b32"
    verdict: drop
    notes:
      - "Carved id SL1 4A (2 mm stud, gap -0.10). Needed a hammer to close onto AT; nothing snapped"
      - "Omar, in chat: \"nothing binds or snaps, everything needed a hammer until 4f\""
  - entry: "c2"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"gap":-0.1,"pair":1}
    count: 1
    iteration: "it-5799e205c04e"
    verdict: drop
    notes:
      - "Upper AT. Needed a hammer to close onto SL1 4A"
  - entry: "c3"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"gap":-0.05,"pair":2}
    count: 1
    iteration: "it-4f3e0c83228d"
    verdict: drop
    notes:
      - "Carved id SL1 4B (2 mm stud, gap -0.05). Needed a hammer to close onto BT"
  - entry: "c4"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"gap":-0.05,"pair":2}
    count: 1
    iteration: "it-fecadd047473"
    verdict: drop
    notes:
      - "Upper BT. Needed a hammer to close onto SL1 4B"
  - entry: "c5"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"gap":0,"pair":3}
    count: 1
    iteration: "it-4d412e2c49eb"
    verdict: drop
    notes:
      - "Carved id SL1 4C (2 mm stud, gap 0). Needed a hammer to close onto CT"
  - entry: "c6"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"gap":0,"pair":3}
    count: 1
    iteration: "it-594855d8bf7d"
    verdict: drop
    notes:
      - "Upper CT. Needed a hammer to close onto SL1 4C"
  - entry: "c7"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"gap":0.05,"pair":4}
    count: 1
    iteration: "it-dcf60d4a3948"
    verdict: adjust
    notes:
      - "Carved id SL1 4D (2 mm stud, gap 0.05, floor 0.6: the split coaster's defaults). Needed a hammer to close onto DT, so the default gap moves looser"
      - "Closed, its top face showed no dent or spot over the stud under skimming light: the 0.6 mm floor stays"
  - entry: "c8"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"gap":0.05,"pair":4}
    count: 1
    iteration: "it-92275438178d"
    verdict: adjust
    notes:
      - "Upper DT (floor 0.6). Its socket does not show through its top face; its gap is too tight"
      - "Omar, in chat, of the closed pairs SL1 4K, 4L and 4D: \"None show\""
  - entry: "c9"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"gap":0.1,"pair":5}
    count: 1
    iteration: "it-7cfda84377c5"
    verdict: drop
    notes:
      - "Carved id SL1 4E (2 mm stud, gap 0.10). Needed a hammer to close onto ET"
  - entry: "c10"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"gap":0.1,"pair":5}
    count: 1
    iteration: "it-e5e5ff6c4ea9"
    verdict: drop
    notes:
      - "Upper ET. Needed a hammer to close onto SL1 4E"
  - entry: "c11"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"gap":0.15,"pair":6}
    count: 1
    iteration: "it-3352b1ff4d72"
    verdict: adjust
    notes:
      - "Carved id SL1 4F (2 mm stud, gap 0.15, the loosest on the ladder). The only pair that went in by hand, but it needed a hammer to sit flush. The next ladder starts above 0.15"
      - "Omar, in chat: \"4f only one that fit without hammer, hammer to make it flush\""
  - entry: "c12"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"gap":0.15,"pair":6}
    count: 1
    iteration: "it-50a38e4cc042"
    verdict: adjust
    notes:
      - "Upper FT. Went onto SL1 4F by hand, flush only with a hammer"
  - entry: "c13"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"stud":1.5,"gap":0,"pair":7}
    count: 1
    iteration: "it-752f67ef5833"
    verdict: adjust
    notes:
      - "Carved id SL1 4G (1.5 mm stud, gap 0). Needed a hammer and still did not sit flush. Whether the socket and stud printed clean was not asked apart from the fit"
      - "Omar, in chat: \"g needed a hemmer, not flush\""
  - entry: "c14"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"stud":1.5,"gap":0,"pair":7}
    count: 1
    iteration: "it-6e8ec71f7908"
    verdict: adjust
    notes:
      - "Upper GT. Hammered onto SL1 4G, not flush"
  - entry: "c15"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"stud":1.5,"gap":0.05,"pair":8}
    count: 1
    iteration: "it-3f4056f18da6"
    verdict: adjust
    notes:
      - "Carved id SL1 4H (1.5 mm stud, gap 0.05). Needed a hammer"
      - "Omar, in chat: \"also h and k needed hammers\""
  - entry: "c16"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"stud":1.5,"gap":0.05,"pair":8}
    count: 1
    iteration: "it-053b1d0ff4f4"
    verdict: adjust
    notes:
      - "Upper HT. Hammered onto SL1 4H"
  - entry: "c17"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"stud":3,"gap":0,"pair":9}
    count: 1
    iteration: "it-35d73e3ed1f8"
    verdict: adjust
    notes:
      - "Carved id SL1 4I (3 mm stud, gap 0). Needed a hammer and did not sit flush"
      - "Omar, in chat: \"i too i not flush\""
  - entry: "c18"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"stud":3,"gap":0,"pair":9}
    count: 1
    iteration: "it-0dc78c47d1ca"
    verdict: adjust
    notes:
      - "Upper IT. Hammered onto SL1 4I, not flush"
  - entry: "c19"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"stud":3,"gap":0.05,"pair":10}
    count: 1
    iteration: "it-65c152d8d772"
    verdict: adjust
    notes:
      - "Carved id SL1 4J (3 mm stud, gap 0.05). Went most of the way in by hand, a hammer to sit flush: closer than the 2 mm stud at the same gap (SL1 4D)"
      - "Omar, in chat: \"J fit most but also needed hammer for flush\""
  - entry: "c20"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"stud":3,"gap":0.05,"pair":10}
    count: 1
    iteration: "it-2ffe649afb9a"
    verdict: adjust
    notes:
      - "Upper JT. Most of the way onto SL1 4J by hand, flush with a hammer"
  - entry: "c21"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"floor":0.8,"pair":11}
    count: 1
    iteration: "it-9eb19fdce7b2"
    verdict: drop
    notes:
      - "Carved id SL1 4K (floor 0.8, gap 0.05). Needed a hammer. Closed, no dent or spot over the stud; nor at 0.6 (SL1 4D), so the thicker floor is not needed"
      - "Omar, in chat: \"also h and k needed hammers\"; of the floors: \"None show\""
  - entry: "c22"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"floor":0.8,"pair":11}
    count: 1
    iteration: "it-cd0ed8305d9f"
    verdict: drop
    notes:
      - "Upper KT (floor 0.8). The socket does not show through; 0.6 is enough"
  - entry: "c23"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Lower"
    params: {"floor":1,"pair":12}
    count: 1
    iteration: "it-e4e359f57004"
    verdict: drop
    notes:
      - "Carved id SL1 4L (floor 1.0, gap 0.05). Started in by hand, then needed a hammer. No dent or spot over the stud; 0.6 is enough"
      - "Omar, in chat: \"l also hammer but kinda initially fit\""
  - entry: "c24"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "3d0cada67c04802bfffa5573bd596d6607b9bb8343c1b0f01482a3ea09b9183f"
    piece: "Upper"
    params: {"floor":1,"pair":12}
    count: 1
    iteration: "it-fe869ba21e5f"
    verdict: drop
    notes:
      - "Upper LT (floor 1.0). The socket does not show through; 0.6 is enough"
  - entry: "c25"
    source: "bikar:patterns/Coupons/Split-Trap-Coupon.bkr"
    source_sha256: "1ccdb852962fbe8e5d9bb67604b8c2def5dbd3dbfb9ba89cc89439c322292271"
    piece: "Lower"
    params: {"room":0,"pair":13}
    count: 1
    iteration: "it-85caac462600"
    verdict: adjust
    notes:
      - "Carved id 4M (trap, room 0). The hexagon 4T dropped in by its own weight, and the lip held it under a hard thumb push from each face. Closing onto MT needed a hammer, as the 2 mm studs at their default gap do; it closed better than 4N"
      - "Omar, in chat: \"Both drop in\"; \"both needed hammer, 4m better than 4n\"; \"Both hold\""
  - entry: "c26"
    source: "bikar:patterns/Coupons/Split-Trap-Coupon.bkr"
    source_sha256: "1ccdb852962fbe8e5d9bb67604b8c2def5dbd3dbfb9ba89cc89439c322292271"
    piece: "Upper"
    params: {"room":0,"pair":13}
    count: 1
    iteration: "it-b7cbdd6e5c28"
    verdict: adjust
    notes:
      - "Upper MT. Its lip held the hexagon; it needed a hammer to close onto 4M"
  - entry: "c27"
    source: "bikar:patterns/Coupons/Split-Trap-Coupon.bkr"
    source_sha256: "1ccdb852962fbe8e5d9bb67604b8c2def5dbd3dbfb9ba89cc89439c322292271"
    piece: "Piece"
    params: {"room":0,"pair":13}
    count: 1
    iteration: "it-d2e8718d5702"
    verdict: keep
    notes:
      - "Hexagon 4T (room 0). Dropped in, does not wiggle or rattle once closed, and stayed in under a thumb push"
      - "Omar, in chat: \"4u wigles inside, 4t doesnt\"; \"Only 4N rattles\""
  - entry: "c28"
    source: "bikar:patterns/Coupons/Split-Trap-Coupon.bkr"
    source_sha256: "1ccdb852962fbe8e5d9bb67604b8c2def5dbd3dbfb9ba89cc89439c322292271"
    piece: "Lower"
    params: {"room":0.2,"pair":14}
    count: 1
    iteration: "it-d05d71f1fc7c"
    verdict: adjust
    notes:
      - "Carved id 4N (trap, room 0.2). The hexagon 4U dropped in and the lip held it under a thumb push. Closing onto NT needed a hammer, less cleanly than 4M"
  - entry: "c29"
    source: "bikar:patterns/Coupons/Split-Trap-Coupon.bkr"
    source_sha256: "1ccdb852962fbe8e5d9bb67604b8c2def5dbd3dbfb9ba89cc89439c322292271"
    piece: "Upper"
    params: {"room":0.2,"pair":14}
    count: 1
    iteration: "it-8fee02446525"
    verdict: adjust
    notes:
      - "Upper NT. Its lip held the hexagon; it needed a hammer to close onto 4N"
  - entry: "c30"
    source: "bikar:patterns/Coupons/Split-Trap-Coupon.bkr"
    source_sha256: "1ccdb852962fbe8e5d9bb67604b8c2def5dbd3dbfb9ba89cc89439c322292271"
    piece: "Piece"
    params: {"room":0.2,"pair":14}
    count: 1
    iteration: "it-014ffc02050a"
    verdict: drop
    notes:
      - "Hexagon 4U (room 0.2). Wiggles inside the closed pair and rattles when shaken: 0.2 mm is too much room"
      - "Omar, in chat: \"4u wigles inside\"; \"Only 4N rattles\""
readings: []
photos: []
feedback:
  lesson: "Every stud gap from -0.10 to 0.15 mm needed a hammer while the slice kept each gap as drawn, so the printer runs tight (0.4 mm nozzle, 0.42 mm outer and 0.45 mm inner wall lines, 0.20 mm layers); and an id on the upper's cut face is hidden once the pair closes."
  decisions: [D-115]
  symptom: "Every stud pair needed a hammer to close, from gap -0.10 to 0.15 mm and at 1.5, 2 and 3 mm; only SL1 4F (2 mm, 0.15) went in by hand, and it needed a hammer to sit flush. Nothing snapped"
  cause: "Not the slice. tools/fit_gap.py studs read the sliced wall paths: every pair's gap came out as drawn, to within 0.005 mm (4A -0.098 for -0.10, 4F +0.155 for 0.15), and the upper prints with its socket opening upward, so first-layer squish cannot narrow the mouth. What is left is the printer: printed holes running smaller than drawn, studs larger, or both. Not measured on the pieces themselves (no calipers reading), and the ladder never went loose enough to find the fit"
  next: "A looser stud ladder, above 0.15 mm, before any studded coaster (split-01, stud-1, pkt-2, all cut at 0.05) is sent. The 0.6 mm floor stays. Lips hold a loose piece, and room 0 is the room. The upper's letter goes on its outer face, not its cut face, so it can still be read once the pair is closed"
---

Omar judged this plate by hand on 2026-10-09, the morning after it printed. It has no photos. Each
row of the page's [After the print](../../design/plates/spl-1.md#after-the-print) table was asked
by the ids cut into the tiles. Rows 4 and 5 were asked as short step-by-step procedures, the
format the review-print skill now holds.

- **Stud fit: every pair is too tight.** From `SL1 4A` to `SL1 4E` (2 mm stud, gaps −0.10 to
  0.10 mm), each needed a hammer to close. `SL1 4F` (0.15 mm), the loosest on the ladder, was the
  only one that went in by hand, and it still needed a hammer to sit flush. Nothing snapped. The
  1.5 mm studs (`SL1 4G`, `SL1 4H`) and the 3 mm studs (`SL1 4I`, `SL1 4J`) were the same: all
  hammered. `4G` and `4I` (gap 0) never sat flush, and `4J` (3 mm at 0.05) went most of the way
  by hand. So no gap on this plate is the fit, and the next ladder starts above 0.15 mm. Whether
  the closed pairs hold when shaken, and come apart without breaking, was not asked once they
  needed a hammer.
- **The floor: 0.6 mm is enough.** With the pairs closed, none of `SL1 4D` (0.6), `SL1 4K` (0.8)
  or `SL1 4L` (1.0) shows a dent or spot over the stud under skimming light. The floor stays
  0.6 mm, and the stud keeps its full height.
- **The lip holds.** Both hexagons, `4T` and `4U`, dropped into their lowers by their own weight,
  and the lip held each under a hard thumb push from both faces. At room 0.2 `4U` wiggles and
  rattles; at room 0 `4T` does neither. So the split coaster holds its loose pieces by a lip, as
  split-01 does, at room 0. Closing both trap pairs needed a hammer, because their 2 mm studs sit
  at the same too-tight default gap.

**The lesson for the next coupon.** The upper's letter (`AT` to `NT`) is cut into its cut face,
so once a pair closes, the letter is hidden inside it. Omar, in chat: "when we add embeded labesl
.. the female side gets hidden after ... label should have been on other side". On the next split
coupon the upper's letter goes on its outer face.

**What waits on this.** split-01, the stud-layout plate stud-1 and pkt-2 all cut their 2 mm studs
at the 0.05 mm default gap, which needed a hammer here. They wait for the looser ladder's answer
before they are sent.

**How it went.** It was sent at 02:23 UTC on 2026-10-09, in pink, on the smooth light-blue
glacier plate. The printer said FINISH at 03:26 with all 18 layers done (the
[print log](../../design/plates/print-logs/spl-1.md)). That is about 63 minutes against the
slicer's 49, with nothing lifting in the chamber pictures.

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built. Nothing was measured with a tool, so there are no readings and no bet moves.
