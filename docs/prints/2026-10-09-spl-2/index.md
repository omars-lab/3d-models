---
run: 2026-10-09-spl-2
plate: "spl-2 — the split coupon again, looser: at what gap does a stud go in by hand"
status: printed
outcome: no-reading
plate_3mf: "spl-2.plate.3mf"
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
  instrument: "none; judged by hand"
pins:
  bikar_ref: 36c814c62213f34129d6a065dbd4284674f94492
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.15,"pair":1}
    count: 1
    iteration: "it-cfe3b5f085ee"
    verdict: keep
    notes:
      - "Carved id SL2 1A (2 mm stud, gap 0.15). Closed by hand onto 1M, held when shaken, and came apart by hand without breaking. The same gap needed a hammer on spl-1 (SL1 4F)"
      - "Omar, in chat: \"they all closed by hand, 1f and up very loose, 1d might have had a lcikc\"; \"1A to 1E hold, 1F on don't\"; \"None broke\""
  - entry: "c2"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.15,"pair":1}
    count: 1
    iteration: "it-85a29b81c72c"
    verdict: keep
    notes:
      - "Upper 1M. Closed by hand onto SL2 1A and held. Its id on the top face reads"
      - "Omar, in chat, of the uppers' ids: \"All read, mark is fine\""
  - entry: "c3"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.15,"pair":2}
    count: 1
    iteration: "it-99bb6802c15b"
    verdict: keep
    notes:
      - "Carved id SL2 1B (2 mm stud, gap 0.15). Closed by hand onto 1N, held when shaken, did not break when pulled"
      - "Omar found 1B and 1D hard to tell apart: \"but node b and d are confusing\""
  - entry: "c4"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.15,"pair":2}
    count: 1
    iteration: "it-82c3012918bc"
    verdict: keep
    notes:
      - "Upper 1N. Closed by hand onto SL2 1B and held. Its id reads, though M and N look alike: \"m and n oto\""
  - entry: "c5"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.2,"pair":3}
    count: 1
    iteration: "it-94bff1013e8d"
    verdict: keep
    notes:
      - "Carved id SL2 1C (2 mm stud, gap 0.20). Closed by hand onto 1P, held when shaken, did not break when pulled"
  - entry: "c6"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.2,"pair":3}
    count: 1
    iteration: "it-88acc20f3de2"
    verdict: keep
    notes:
      - "Upper 1P. Closed by hand onto SL2 1C and held. Its id reads"
  - entry: "c7"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.2,"pair":4}
    count: 1
    iteration: "it-a29df7e174d7"
    verdict: keep
    notes:
      - "Carved id SL2 1D (2 mm stud, gap 0.20). Closed by hand onto 1Q, maybe with a click, held when shaken, did not break when pulled"
      - "Omar, in chat: \"1d might have had a lcikc\""
  - entry: "c8"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.2,"pair":4}
    count: 1
    iteration: "it-3676ca8049ad"
    verdict: keep
    notes:
      - "Upper 1Q. Closed by hand onto SL2 1D and held. Its id reads"
  - entry: "c9"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.25,"pair":5}
    count: 1
    iteration: "it-02ac2ee5952e"
    verdict: keep
    notes:
      - "Carved id SL2 1E (2 mm stud, gap 0.25). Closed by hand onto 1R, held when shaken, did not break when pulled. The loosest pair that held"
      - "Omar, in chat, on the stud gap: \"it should be 1e\" — 0.25 mm for split-01, stud-1 and pkt-2 (D-116)"
  - entry: "c10"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.25,"pair":5}
    count: 1
    iteration: "it-6e5e52cf9a42"
    verdict: keep
    notes:
      - "Upper 1R. Closed by hand onto SL2 1E and held. Its id reads"
  - entry: "c11"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.25,"pair":6}
    count: 1
    iteration: "it-b96270d54f41"
    verdict: drop
    notes:
      - "Carved id SL2 1F (2 mm stud, gap 0.25, the same gap as 1E). Closed by hand onto 1S but very loose, and does not stay together when shaken"
      - "Omar, in chat: \"1F and up very loose / not stuck together\""
  - entry: "c12"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.25,"pair":6}
    count: 1
    iteration: "it-8d6a271e70bd"
    verdict: drop
    notes:
      - "Upper 1S. Very loose on SL2 1F; the pair falls apart when shaken. Its id reads"
  - entry: "c13"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.3,"pair":7}
    count: 1
    iteration: "it-c6673f6ef995"
    verdict: drop
    notes:
      - "Carved id SL2 1G (2 mm stud, gap 0.30). Very loose on 1T; does not stay together when shaken"
  - entry: "c14"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.3,"pair":7}
    count: 1
    iteration: "it-916d6af5b5e1"
    verdict: drop
    notes:
      - "Upper 1T. Very loose on SL2 1G. Its id reads"
  - entry: "c15"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.3,"pair":8}
    count: 1
    iteration: "it-775be24bd8c5"
    verdict: drop
    notes:
      - "Carved id SL2 1H (2 mm stud, gap 0.30). Very loose on 1U; does not stay together when shaken"
  - entry: "c16"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.3,"pair":8}
    count: 1
    iteration: "it-8ff615aa63cc"
    verdict: drop
    notes:
      - "Upper 1U. Very loose on SL2 1H. Its id reads"
  - entry: "c17"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.35,"pair":9}
    count: 1
    iteration: "it-0a0eb35b205f"
    verdict: drop
    notes:
      - "Carved id SL2 1I (2 mm stud, gap 0.35). Very loose on 1V; does not stay together when shaken"
  - entry: "c18"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.35,"pair":9}
    count: 1
    iteration: "it-85faca6a923e"
    verdict: drop
    notes:
      - "Upper 1V. Very loose on SL2 1I. Its id reads"
  - entry: "c19"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.35,"pair":10}
    count: 1
    iteration: "it-d9de9f0ab01d"
    verdict: drop
    notes:
      - "Carved id SL2 1J (2 mm stud, gap 0.35). Very loose on 1W; does not stay together when shaken"
  - entry: "c20"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.35,"pair":10}
    count: 1
    iteration: "it-e8ba25ac757a"
    verdict: drop
    notes:
      - "Upper 1W. Very loose on SL2 1J. Its id reads"
  - entry: "c21"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.4,"pair":11}
    count: 1
    iteration: "it-6f3828e4d504"
    verdict: drop
    notes:
      - "Carved id SL2 1K (2 mm stud, gap 0.40). Very loose on 1X; does not stay together when shaken"
  - entry: "c22"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.4,"pair":11}
    count: 1
    iteration: "it-68c669d502c5"
    verdict: drop
    notes:
      - "Upper 1X. Very loose on SL2 1K. Its id reads"
  - entry: "c23"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Lower"
    params: {"gap":0.4,"pair":12}
    count: 1
    iteration: "it-81841b077a14"
    verdict: drop
    notes:
      - "Carved id SL2 1L (2 mm stud, gap 0.40). Very loose on 1Y; does not stay together when shaken"
  - entry: "c24"
    source: "bikar:patterns/Coupons/Split-Fit-Coupon.bkr"
    source_sha256: "de7ad80ea34b72ef1eabc88e3237422c10105c45226b6b07e21c57968aa98090"
    piece: "Upper"
    params: {"gap":0.4,"pair":12}
    count: 1
    iteration: "it-f00be28a08e5"
    verdict: drop
    notes:
      - "Upper 1Y. Very loose on SL2 1L. Its id reads"
readings: []
photos: []
feedback:
  lesson: "A 2 mm stud went in by hand at every gap from 0.15 to 0.40 mm and held from 0.15 to 0.25, though spl-1 needed a hammer at 0.15; and at 0.25 one pair held (1E) while its twin fell apart (1F). So the fit moves about 0.05 to 0.10 mm from print to print (0.4 mm nozzle, 0.42 mm outer and 0.45 mm inner wall lines, 0.20 mm layers). And carved B and D, M and N, look alike at this size."
  decisions: [D-116]
  symptom: "Every pair closed by hand. SL2 1A to 1E (0.15 to 0.25 mm) held when shaken; SL2 1F to 1L (0.25 to 0.40 mm) were very loose and fell apart. None broke when pulled. 1D may have clicked in. All the uppers' ids on their top faces read"
  cause: "Not measured on the pieces (no calipers reading). The same 0.15 mm gap needed a hammer on spl-1, printed earlier the same day with the same nozzle, preset and spool, so the printer varies from print to print by about as much as one or two rungs of the ladder. Why it varies (chamber warmth, the plate, the spool's moisture) is not known"
  next: "The stud gap on split-01, stud-1 and pkt-2 is 0.25 mm, Omar's pick (D-116), the loosest gap that held here; 1F at the same gap fell apart, so a whole coaster at 0.25 may come out loose. split-01 and stud-1 set it in their recipes; pkt-2's pocket coaster has no stud-gap knob yet, so it waits on a bikar change. Coupon uppers keep their id on top (D-115 stands). Piece letters skip B, D, M, N and O"
---

Omar judged this plate by hand on 2026-10-09, the same day it printed. It has no photos. Each row
of the page's [After the print](../../design/plates/spl-2.md#after-the-print) table was asked by
the ids cut into the tiles.

- **Fit: every pair closes by hand.** From `SL2 1A` (0.15 mm) to `SL2 1L` (0.40 mm), every pair
  went in by thumb pressure. Omar, in chat: "they all closed by hand, 1f and up very loose, 1d
  might have had a lcikc". So the ladder went loose enough this time, and the fit lies at its
  tight end.
- **Shake and pull: 1A to 1E hold, 1F and up do not.** `SL2 1A` to `SL2 1E` (0.15, 0.20 and the
  first 0.25 pair) stay closed when shaken. `SL2 1F` on (the second 0.25 pair and everything
  looser) are "very loose / not stuck together". None broke when pulled apart.
- **The ids: all read.** The uppers' short ids on their top faces (`1M` to `1Y`) all read, and
  "mark is fine". So coupon uppers keep the id on top, and [D-115](../../working-model/decisions-log.md)
  stands. But B and D look alike once cut this small, and so do M and N: "but node b and d are
  confusing", "m and n oto". The print-coaster-samples rules now skip those letters.

**The stud gap: 0.25 mm.** Omar: "it should be 1e". That is 0.25 mm for split-01, stud-1 and
pkt-2 ([D-116](../../working-model/decisions-log.md)). The page's own rule would have picked 0.15,
the tightest gap whose two pairs both closed by hand and held; Omar chose two rungs looser. My
reading, not his stated reason: 0.15 needed a hammer on spl-1, so a gap that tight is not safe
from one print to the next. At 0.25 the two pairs disagree: `1E` held and `1F` fell apart.

**The lesson for the next plate.** On spl-1, printed earlier the same day with the same nozzle, preset
and spool, 0.15 mm needed a hammer. Here 0.15 went in by hand. So the fit moves by about 0.05 to
0.10 mm from print to print, as much as one or two rungs of the ladder, with a 0.4 mm nozzle,
0.42 mm outer and 0.45 mm inner wall lines and 0.20 mm layers. A coaster with several studs
cut at 0.25 may come out loose on one print and snug on another.

**How it went.** It was sent at 17:39 UTC on 2026-10-09, in pink from AMS 0 slot 0, on the smooth
light-blue glacier plate. The printer said FINISH at 18:30 with all 18 layers done (the
[print log](../../design/plates/print-logs/spl-2.md)). That is about 50 minutes against the
slicer's 45, with nothing lifting in the chamber pictures.

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built. Nothing was measured with a tool, so there are no readings and no bet moves.
