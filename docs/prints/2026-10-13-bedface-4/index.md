---
run: 2026-10-13-bedface-4
plate: "bedface-4 — twelve 50 mm pieces of the gBV coaster on the glacier plate: stock beside five first-layer settings, two pieces each"
status: printed
outcome: no-reading
plate_3mf: "bedface-4.plate.3mf"
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
  instrument: "none; judged by hand, bottoms side by side, and one photo of each piece's bottom"
pins:
  bikar_ref: 11ea0fd008053ca53cc237cfe0becb104f2dc3d5
  self_ref: ~
objects:
  - entry: "c1"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-cc7e1f23a152"
    verdict: adjust
    notes:
      - "The piece carved H: stock settings, not turned on the bed, the control. Its bottom has short dark notches along the strap edges (the photo)"
      - "Omar, asked whether H and J slit about as much as bedface-2's whole S coaster: \"they have less than s, but they both have slits\"; asked how much less: \"A little less\""
      - "The page reads \"a little less\" as: the pieces stand in for the whole coaster, so the rows below can rank the settings. Whether H and J look alike was not said; to me (Claude) the two photos look alike"
      - "Verdict adjust, on the setup, not the design, as for bedface-3's G: stock still slits, and the setup is what changes"
  - entry: "c2"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-287100ba79d3"
    verdict: adjust
    notes:
      - "The piece carved J: stock settings, turned a quarter turn on the bed, the control for the turned pieces. Its bottom has short dark notches along the strap edges (the photo)"
      - "Omar: \"they have less than s, but they both have slits\"; how much less: \"A little less\""
      - "Verdict adjust, on the setup, as for H"
  - entry: "c3"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-961f864f8707"
    verdict: drop
    notes:
      - "The piece carved L: the fill pushed 30% into the wall (infill_wall_overlap 30%), not turned. Its bottom has dark notches all along the strap edges, many (the photo)"
      - "Omar, asked whether L and P have fewer slits than H and J: \"P has fewer, l has more\""
      - "The slice had L below stock (306 slits against H's 356). The print did not follow it, the same lesson as bedface-1: the plan is not the print"
      - "Verdict drop: more than stock, in Omar's words"
  - entry: "c4"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-68f0821bf336"
    verdict: adjust
    notes:
      - "The piece carved P: the fill pushed 30% into the wall, turned a quarter turn. Its bottom looks smoother along the strap edges than L's, with few notches (the photo)"
      - "Omar: \"P has fewer, l has more\""
      - "Verdict adjust: fewer than stock, but the 55% pieces did better (row 3), so the overlap goes up, not back on as 30%. The pair split, so 30% on its own has no verdict"
  - entry: "c5"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-87ef36da7091"
    verdict: keep
    notes:
      - "The piece carved 2: the fill pushed 55% into the wall (infill_wall_overlap 55%), turned a quarter turn. Its bottom is smooth along the strap edges, with very few notches (the photo)"
      - "Omar, asked whether 2 and T have fewer slits than L and P, and a ridge where the fill meets the wall: picked \"Fewer, no ridge\"; then, in chat: \"2 is better than T\""
      - "The best piece on the plate, in Omar's words. The slice ranked it best too (101 slits against H's 356)"
      - "Verdict keep: fewer slits than 30% and no ridge, which the page read as \"55% beats 30%\""
  - entry: "c6"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-bb173e2337d3"
    verdict: keep
    notes:
      - "The piece carved T: the fill pushed 55% into the wall, not turned. Its bottom has more notches and texture along the strap edges than 2's, most on the left side (the photo)"
      - "Omar: picked \"Fewer, no ridge\" for 2 and T; then \"2 is better than T\""
      - "Verdict keep: fewer than 30% and no ridge, though not as clean as 2"
  - entry: "c7"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-da873c5f663e"
    verdict: adjust
    notes:
      - "The piece carved U: 5% more plastic on the first layer (initial_layer_flow_ratio 1.05), turned. Its bottom edges look smoother than J's (the photo)"
      - "Omar, asked whether the flow pieces have fewer slits than J: \"W is almost identical to J. U is a bit better\""
      - "Verdict adjust: a bit better than stock, but the 10% pieces did better still, so the flow goes up"
  - entry: "c8"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-c70769839274"
    verdict: drop
    notes:
      - "The piece carved W: 5% more plastic on the first layer, turned. Its bottom has notches along the left straps, like J's (the photo)"
      - "Omar: \"W is almost identical to J. U is a bit better\""
      - "Verdict drop: the same as stock, in Omar's words"
  - entry: "c9"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-90d60dceeec1"
    verdict: keep
    notes:
      - "The piece carved X: 10% more plastic on the first layer (initial_layer_flow_ratio 1.1), turned. Its bottom edges look fairly smooth (the photo)"
      - "Omar, asked about X and Y beside J: \"thye still have slits but Y has less than J and X has less than Y\""
      - "The fewest slits of the four flow pieces. The page expected flow to do nothing (research §1); it helped a little, in order: X fewer than Y, Y fewer than J, U a bit fewer than J, W the same"
      - "Verdict keep: fewer than stock. Still slits, so not a fix on its own"
  - entry: "c10"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-92a133f7370e"
    verdict: keep
    notes:
      - "The piece carved Y: 10% more plastic on the first layer, turned. Its bottom has a few notches on the left straps (the photo)"
      - "Omar: \"thye still have slits but Y has less than J and X has less than Y\""
      - "Verdict keep: fewer than stock, as X"
  - entry: "c11"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-266d61af8ffa"
    verdict: drop
    notes:
      - "The piece carved 4: the monotonicline bottom pattern, turned. Its bottom has short dark dashes along the lower-right straps and the bottom strap (the photo)"
      - "Omar, asked about the slits at the strap ends of 4 and 7 beside H and J: \"both have slits but in different places\"; asked to count them against stock: \"About the same\""
      - "Verdict drop: about the same as stock, which the page read as \"the pattern is dropped\""
  - entry: "c12"
    source: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
    source_sha256: "950b9d4bf0616318b4e9a8810acc0beb242b509905c44e3414e3d46e8ce4aa47"
    params: {"size":112.5,"strap":3.75,"height":4.4,"round":1.25}
    window: "50@13,30"
    count: 1
    iteration: "it-2fe99e2580e3"
    verdict: drop
    notes:
      - "The piece carved 7: the monotonicline bottom pattern, not turned. Its bottom has rows of short dark dashes along the top-right strap and the right-hand straps, and a small pink smear near the top-left corner, likely left on the plate by the last pink print (the photo)"
      - "Omar: \"both have slits but in different places\"; against stock: \"About the same\""
      - "Verdict drop, as 4"
readings: []
photos:
  - file: photos/piece-h-bed-face.jpg
    sha256: 725bfa1da2fc855cb585368a84109380e39efdf449ca941fd1be55e3421c6d92
    of: "the bottom of the piece carved H (stock), whole: short dark notches along the strap edges"
    why: "the control every other piece is read against"
  - file: photos/piece-j-bed-face.jpg
    sha256: b0a431aa6563d3b3ecc9393f606c6e8c8718fbb40c264a862853443303a38e07
    of: "the bottom of the piece carved J (stock, turned), whole: short dark notches along the strap edges, like H's"
    why: "the control for the turned pieces"
  - file: photos/piece-l-bed-face.jpg
    sha256: 578a64e5a411d51366de8531ba0e1d4665b94e1f2e47c6cbc1a1d6e7c9019986
    of: "the bottom of the piece carved L (overlap 30%), whole: dark notches all along the strap edges"
    why: "the 30% piece Omar found worse than stock"
  - file: photos/piece-p-bed-face.jpg
    sha256: fbe535488da9b4493db0ac32dbcf144908dbe8927a098d0767029bd991115785
    of: "the bottom of the piece carved P (overlap 30%, turned), whole: smoother strap edges, few notches"
    why: "the 30% piece Omar found better than stock; the pair split"
  - file: photos/piece-2-bed-face.jpg
    sha256: 5497d34a2b60a86cce5aad78ffab168d7cde554f3da8b179e6b7a3bd0e034a86
    of: "the bottom of the piece carved 2 (overlap 55%, turned), whole: smooth strap edges, very few notches"
    why: "the best piece on the plate, in Omar's words"
  - file: photos/piece-t-bed-face.jpg
    sha256: 28bd70ff5a3e3c841de7c517f91aefd280a9b58767aaed8c65c8f98fded681a0
    of: "the bottom of the piece carved T (overlap 55%), whole: more notches than 2, most on the left side"
    why: "the other 55% piece, fewer slits than 30% but not as clean as 2"
  - file: photos/piece-u-bed-face.jpg
    sha256: 216ba0e0f56650526f1bf4e28fb7b301696e160e103f94afbd101ddd0fbe62b8
    of: "the bottom of the piece carved U (flow 1.05, turned), whole: strap edges smoother than J's"
    why: "the 1.05 piece Omar found a bit better than stock"
  - file: photos/piece-w-bed-face.jpg
    sha256: 6dc494f222a9f826409de32f34917656e752b6e9b0f451e7584b6138b9613bc0
    of: "the bottom of a flow 1.05 piece, whole, its carved id hard to read; W by elimination, since Omar sent it with U's photo: notches along the left straps, like J's"
    why: "the 1.05 piece Omar found almost identical to stock"
  - file: photos/piece-x-bed-face.jpg
    sha256: 165001cc43b026cf462e672b4a4839b6cf44f2b6a1db0e596c17eb1e5dd5c576
    of: "the bottom of the piece carved X (flow 1.10, turned), whole: fairly smooth strap edges; the id reads X to me (Claude), not certain"
    why: "the flow piece with the fewest slits"
  - file: photos/piece-y-bed-face.jpg
    sha256: 02971908d8ff81363dcde460725e94f5b81c52eb7e91eeb9696a8b401264953b
    of: "the bottom of the piece carved Y (flow 1.10, turned), whole: a few notches on the left straps"
    why: "the other 1.10 piece, fewer slits than stock, more than X"
  - file: photos/piece-4-bed-face.jpg
    sha256: 685ef84ef2beb2777c34c0ae8c42ac4a3cebf5820bdec2710625cf430bb6bbdf
    of: "the bottom of the piece carved 4 (monotonicline, turned), whole: dashes along the lower-right straps and the bottom strap; the id reads 4 to me (Claude), not certain"
    why: "the monotonicline pieces, with the slits in different places from stock but about as many"
  - file: photos/piece-7-bed-face.jpg
    sha256: 429d6255f0a64a70e755ad2bac5ea7b1727476bf5283e233c5e9585398f08e71
    of: "the bottom of the piece carved 7 (monotonicline), whole: dashes along the top-right and right-hand straps, and a small pink smear near the top-left corner"
    why: "the other monotonicline piece"
feedback:
  lesson: "On pieces of the gBV coaster on the smooth glacier plate, pushing the fill 55% into the wall closed the most slits along the strap edges, with no ridge: the piece carved 2 was the best on the plate. 10% more plastic on the first layer helped a little, against what the research expected (X fewer than Y, Y fewer than J), but every flow piece still slit. 30% overlap split (P fewer, L more). The monotonicline bottom only moved the slits. The stock pieces slit a little less than bedface-2's whole stock coaster, so the pieces stand in for the coaster (0.4 mm nozzle, 0.5 mm first line, 0.20 mm layers, sliced as a Smooth PEI plate)"
  decisions: []
  symptom: "Stock H and J: short notches along the strap edges, a little fewer than the whole S coaster. 55%: very few on 2, more on T. 1.10 flow: fewer than stock, still some. 1.05: U a bit fewer, W the same. 30%: P fewer, L more. Monotonicline: about as many, in other places"
  cause: "Lines that stop short of the strap wall on the first layer, as the slice drawings show. Pushing the fill into the wall closes them; more plastic widens the lines a little. The turn may matter for the overlap pieces: in both pairs the turned piece did better (P over L, 2 over T), as the slice ranked them, but two pairs are too few to say. My (Claude's) reading, not Omar's"
  next: "Verdicts by one rule: keep where a setting left fewer slits than stock and nothing on the plate beat it (2, T, X, Y); adjust where it left fewer but a stronger version of it did better (P, U), and for the stock pair, whose setup is what changes; drop where it left the same or more (L, W, 4, 7). What prints next with 55% overlap, 10% flow or both, and on a whole coaster or more pieces, is Omar's call"
---

Omar judged this plate by hand on 2026-10-13, turning the pieces over side by side, and sent a
photo of each piece's bottom. The rows of the page's
[After the print](../../design/plates/bedface-4.md#after-the-print) table were asked one at a
time, with one follow-up round for rows 1 and 5.

- **Row 1, `H` and `J` (stock) against bedface-2's `S`:** "they have less than s, but they both
  have slits". Asked how much less: "A little less". So the pieces stand in for the whole
  coaster, and the rows below can rank the settings.
- **Row 2, `L` and `P` (30% overlap):** "P has fewer, l has more". The pair split.
- **Row 3, `2` and `T` (55% overlap):** "Fewer, no ridge", then "2 is better than T". `2` is the
  best piece on the plate.
- **Row 4, the flow pieces:** "W is almost identical to J. U is a bit better", and "thye still
  have slits but Y has less than J and X has less than Y". The page expected flow to do nothing;
  10% more plastic helped a little.
- **Row 5, `4` and `7` (monotonicline):** "both have slits but in different places". Asked to
  count them against stock: "About the same". The pattern is dropped.

| Setting | Pieces | In Omar's words | What the page set that answer to mean |
|---|---|---|---|
| stock | `H`, `J` | a little less than `S`, still slits | the pieces stand for the coaster |
| overlap 30% | `L`, `P` | `P` fewer, `L` more | split, no verdict on 30% alone |
| overlap 55% | `2`, `T` | fewer than 30%, no ridge; `2` better than `T` | 55% beats 30% |
| flow 1.05 | `U`, `W` | `U` a bit better than `J`, `W` the same | weak |
| flow 1.10 | `X`, `Y` | both fewer than `J`, `X` fewest; still slits | fewer: flow goes with the overlap on one plate |
| monotonicline | `4`, `7` | about the same, in different places | dropped |

The photos, each piece's bottom, carved id up:

![H, stock: notches along the strap edges](photos/piece-h-bed-face.jpg)

![J, stock, turned: notches along the strap edges](photos/piece-j-bed-face.jpg)

![L, overlap 30%: notches all along the strap edges](photos/piece-l-bed-face.jpg)

![P, overlap 30%, turned: smoother strap edges](photos/piece-p-bed-face.jpg)

![2, overlap 55%, turned: smooth strap edges, the best on the plate](photos/piece-2-bed-face.jpg)

![T, overlap 55%: more notches than 2, most on the left](photos/piece-t-bed-face.jpg)

![U, flow 1.05, turned: a bit smoother than J](photos/piece-u-bed-face.jpg)

![W, flow 1.05, turned: much like J](photos/piece-w-bed-face.jpg)

![X, flow 1.10, turned: fairly smooth](photos/piece-x-bed-face.jpg)

![Y, flow 1.10, turned: a few notches on the left straps](photos/piece-y-bed-face.jpg)

![4, monotonicline, turned: dashes along the lower-right straps](photos/piece-4-bed-face.jpg)

![7, monotonicline: dashes along the top-right and right-hand straps](photos/piece-7-bed-face.jpg)

All twelve photos were re-saved with no metadata; none carried a location. Each was cut down to
the piece, which leaves out the lap at the bottom edge of several. The carved ids on `W`, `X`
and `4` are hard to read in the photos. `W` is named by elimination: Omar sent it with `U`'s
photo, while the flow 1.05 row was being asked.

**What the answers mean, as the page set them out before the print.**

- Row 1, "a little less": the pieces slit like the coaster, so every row below can be trusted.
- Row 3, "Fewer and no ridge": "55% beats 30%".
- Row 4, fewer on 1.10: "the first-layer flow goes on the next coaster, and the overlap and flow
  get one plate together".
- Row 5, "About the same": "the pattern is dropped".

Row 2 split, so 30% on its own has no answer; row 3 supersedes it anyway. What stands: 55%
overlap is the strongest setting here, and 10% more first-layer plastic helps a little. Neither
alone left a piece with no slits. What prints next, and how, is Omar's call. The open history is
in [the issue](../../issues/bed-face-preset-failed-in-print.md).

One thing I (Claude) noticed, not Omar: in both overlap pairs the turned piece did better (`P`
over `L`, `2` over `T`), and the slice ranked them the same way. Two pairs are too few to call it.

**The print.** Sent at 23:12 UTC on 2026-10-12, finished at 02:26 UTC on 2026-10-13: 194 minutes
against the slicer's 173, all 22 layers, no pause or error (the
[print log](../../design/plates/print-logs/bedface-4.md)). Green PLA Basic from AMS slot 3. The
timelapse is on [the page](../../design/plates/bedface-4.md#the-print).

The source hashes and iteration ids are the ones `bambu slice compose` recorded when the plate was
built, at bikar `11ea0fd0`. Nothing was measured with a tool, so there are no readings and no bet
moves.
