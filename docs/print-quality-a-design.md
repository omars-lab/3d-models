# Print quality for thin openwork PLA coasters on the X2D (research A)

Status: proposal, 2026-09-26. Nothing here has been printed or measured yet. Sources and fetch
status: [`research/print-quality-a.md`](research/print-quality-a.md).

Omar on minis-04 (2026-09-26): "i see tiny holes on the print and the peg system border is too
big and pegs too tight". The plate is [`plates/minis-04.yaml`](plates/minis-04.yaml): 80 mm hex
coasters, 1.4 mm frame (seven 0.2 mm layers) with 1.2 mm straps standing on it, dovetail pegs at
clearance 0.10 mm, sliced with `0.20mm Standard @BBL X2D` and Bambu PLA Basic. The previous run,
[minis-03](prints/2026-09-26-minis-03/index.md), had pegs at 0.15 that were "a bit loose" on a
taller piece. Nothing on either run was measured with calipers.

What the shipped slicer profile actually does is in the research file §0. The three facts this
doc leans on most: walls use the **classic** generator with 2 loops, the top surface pattern is
**monotonic line**, and first-layer (elephant foot) compensation is **0.15 mm**; hole and contour
compensation are both 0.

## 1. Tiny holes

### 1.1 Causes, most likely first

1. **Pinholes where the top skin meets the walls.** A known, still-open Bambu Studio problem:
   [BambuStudio #9768](https://github.com/bambulab/BambuStudio/issues/9768) reports gaps and
   pinholes in top and first layers, filed on an H2C, and one user writes "I have a new X2D and
   immediately noticed gaps… more often like those described in this issue". Bambu staff there
   say "The temporary solution is to use monotonic lines and overlaps"; a user reports the
   infill/wall overlap setting "doesn't apply to the standard top infill pattern Monotonic Line",
   which is exactly the X2D profile's top pattern. Evidence is user reports plus a staff
   workaround, not a measurement, and one X2D report is thin — hence "most likely", not "the
   cause". The X2D profile already sets `monotonic_travel_into_wall` 45, which a Bambu
   contributor says "is designed to improve pinholes", so part of the fix may already be in.
2. **An unfilled strip down the middle of each 2 mm strap.** Two classic walls a side at
   0.42 mm (outer) and 0.45 mm (inner) nominal widths add up to about 1.74 mm, leaving a strip of
   very roughly 0.2–0.3 mm in the middle (the exact number depends on how the slicer spaces
   overlapping lines, which I did not compute). A strip that narrow is either filled by gap fill
   or left empty; the Bambu wiki says of classic walls "If the polygon is too small, the result
   of the shrinkage will be empty" ([wall generator](https://wiki.bambulab.com/en/software/bambu-studio/wall-generator)).
   This is a derivation, not an observation — the slicer preview settles it without printing
   (§4.1).
3. **Under-extrusion from flow ratio or pressure advance.** The PLA Basic preset uses flow
   0.98; the Bambu troubleshooting page calls 0.98 "normal for PLA filament with X1C" and says to
   raise it toward 1.00 for "even gaps in top layer". That number was written for the X1C and may
   not transfer to the X2D's hotend. A pressure-advance value that is too high gives "lines not
   connected"; one forum poster fixed wall/infill gaps by lowering K from 0.025 to 0.012.
4. **Seam gap at the corners of the openings.** Aligned seams prefer concave corners, and the
   seam leaves a small gap by default (15% of the nozzle) — [Seam](https://wiki.bambulab.com/en/software/bambu-studio/Seam).
   Openwork has hundreds of corners.
5. **First-layer gaps** — a dirty plate or too fast a first layer ("no air gaps" is the target,
   [first-layer guide](https://wiki.bambulab.com/en/knowledge-sharing/identify-and-fix-first-layer-issues-with-a-test-print)).
6. **Wet filament.** Lowest here: the Bambu PLA page says PLA has "low hygroscopicity" and does
   not list PLA Basic among the types that must be dried, though it says drying prevents
   "bubbles, holes".

### 1.2 How to tell them apart (look before changing anything)

| What you see | Points to |
|---|---|
| Holes on the **top** face, along the edge where the flat top meets a wall | cause 1 |
| Holes down the **centre line** of a strap, top or side | cause 2 |
| Holes at the **same corner** of every opening, stacked up the height | cause 4 |
| Even, regular gaps between top lines across the whole top | cause 3 (flow) |
| Gaps at the **start** of lines, lines not joined to walls | cause 3 (pressure advance) |
| Holes on the **bottom** face only | cause 5 |
| Craters or bubbles, popping or hissing while printing, stringing | cause 6 |

A phone photo under a raking light of top and bottom faces is enough to place most of these.

## 2. Pegs too tight

### 2.1 How the joint is built

From [coaster-interlock-design.md](coaster-interlock-design.md) §3: a dovetail tab at L/4 of
each edge and a matching slot at 3L/4, the slot offset by the clearance c **on every face**. The
slot opens to the outside, so to the slicer it is part of the piece's **outer contour**, not a
hole. The pieces drop together along Z, so friction acts over the 1.4 mm height.

### 2.2 Causes, most likely first

1. **0.10 mm per face is below every published starting point read here.** The `CAL-FIT-01`
   ladder was transcribed from [Creative3DP](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/),
   whose numbers are **diametral** (total across a round pin of 5–25 mm), and which says holes
   print 0.1–0.3 mm undersize and shafts about 0.1 mm oversize, with those errors to be
   compensated **separately** from the fit. bikar's coaster clearance is **per face**, and the
   profile applies no contour or hole compensation. So 0.10 per face is 0.20 total, between
   Creative3DP's "snug" and "close running" — but only after compensation we do not apply. My
   hypothesis (unmeasured): the tab prints a little wide and the slot a little narrow, eating
   most of the 0.10. The other fetched sources start higher still — Prusa "at least 0.3 mm" for
   movable parts, Hubs "0.5 mm" for FDM interlocking joints, neither saying per side or total.
   This also raises a transfer question about `CAL-FIT-01` itself (§6, Q3).
2. **Seam on a bearing face.** Aligned seams prefer concave corners, and the slot's inner
   corners are concave corners of the outer contour; the Bambu compensation page lists "Seam,
   this feature can affect hole precision" among the checks. A seam bump on a slot flank makes a
   high spot.
3. **Sharp corners.** Direction changes at the dovetail's corners are where material bunches;
   Prusa: "Using a chamfer on the edges of two parts that slot together can save you a lot of
   effort when assembling"; Hubs: "Adding a small radius to part edges assists joint assembly";
   Creative3DP recommends a 0.5 mm × 45° lead-in chamfer. On a 1.4 mm tall joint a 0.5 mm chamfer
   is a third of the height, so its size needs a print test.
4. **Elephant foot.** The first layer is 1 of 7 at 1.4 mm (it was about 1 of 26 on minis-03's
   taller piece), so a first-layer flare now spans a much larger share of the joint. The profile
   already compensates 0.15 mm; the Bambu wiki's worked example lands at 0.10 and says the right
   value varies by plate type, so 0.15 is uncalibrated in either direction
   ([elephant foot](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot)).
   Ranked lower because compensation is on: if anything it pulls the first layer in.
5. **Pieces not flat.** A thin 1.4 mm frame can curl; curled pieces bind even at a fair gap.
   Tell-tale below.

Shrinkage does **not** mismatch the pitch: both pieces are the same shape, and tab and slot sit
symmetric about each edge's midpoint, so both shrink together.

### 2.3 How to tell them apart

| Check | Points to |
|---|---|
| Measure tab width and slot width at mid-height with calipers; gap per face = (slot − tab) / 2 | cause 1 if the gap is well under 0.10 |
| Binding only at the bottom edge; a light file on the first layer frees it | cause 4 |
| One flank binds, and there is a visible bump at a slot corner | cause 2 |
| Freed by rounding the tab corners with a blade | cause 3 |
| A piece rocks on a flat table | cause 5 |

## 3. Peg border too big

This one is by design, not a print defect. The frame per piece is
`frame = depth + clearance + wall` (in bikar's minimal-pegs construction,
`GimTvN9hw4U-minimal-pegs-coaster.bkr`, not in this repo), so at
minis-04's values two frames meet in a solid band of about 11 mm. The alternatives are already
built as plates, with their band widths:

| Option | Joint band | Plate |
|---|---|---|
| Dovetail today (neck 3, depth 3, wall 2.5) | ~11.1 mm | [minis-04](plates/minis-04.yaml) |
| Slim dovetail (neck 2, depth 2, wall 2.1) | ~8.4 mm | [minis-06](plates/minis-06.yaml) |
| Plain frame, no join | ~6.0 mm | [minis-05](plates/minis-05.yaml) |
| Tab | ~5.8 mm | [minis-05](plates/minis-05.yaml) |
| Butterfly key | ~5.7 mm | [minis-05](plates/minis-05.yaml) |
| Butterfly key at frame 2 (approach A) | ~4 mm | [coaster-borderless-joins-design.md](coaster-borderless-joins-design.md) |

What each costs: the slim dovetail keeps the joint style but sits at the tab-neck floor
(`CAL-CST-06`, unsettled); the key needs a separate small part per join and its own clearance
ladder (KEY-1); the tab gives no pull-apart lock. Nothing in the sources read here settles which
looks best — that is Omar's call from the printed pieces.

## 4. Changes

Each change says what it fixes, what it risks and what it costs. None changes temperatures past
the filament preset's range, none slows ironing into heat-creep territory, and none touches the
machine profile — nothing here puts the printer at risk.

### 4.1 Check before printing: the slicer preview (free)

Slice minis-04 in Bambu Studio and look at a layer inside the straps with the line-type view.

**Validator:** in the layer preview at a strap-only layer (above 1.4 mm), each 2 mm strap shows
its walls plus either gap fill or nothing in the middle.
PASS: the middle of every strap is filled (walls or gap fill) along its whole length — then cause
1.1-2 is ruled out and the holes are elsewhere.
FAIL: a thin empty line runs down the middle of the straps, or gap fill is broken into dashes —
then cause 1.1-2 is live and change A below is the fix to test first.

### 4.2 Slicer changes — a per-plate process override

These are process settings, so they can live in a small process JSON next to the plate and be
passed through `bambu slice compose -s "<machine preset>;<override.json>"` (the flag accepts
preset names or JSON paths, per [`../tools/bambu/FLAGS.md`](../tools/bambu/FLAGS.md)). Open
question: whether the slicer resolves an `inherits` line in a user JSON passed this way, or needs
the full flattened preset — the bambu tool does not resolve inheritance itself (§6, Q6).

| # | Change | Fixes | Risks | Costs |
|---|---|---|---|---|
| A | `wall_generator` classic → **arachne** | strap centre strip (1.1-2) | Arachne "can make discontinuous walls" (wiki); changes every wall, so fits shift too | nothing; re-slice |
| B | `top_surface_pattern` monotonicline → **monotonic**, `infill_wall_overlap` 15% → higher | top pinholes (1.1-1) | more overlap can leave a ridge along the walls; the 55% value is one user's | nothing |
| C | `xy_contour_compensation` 0 → **negative** (e.g. −0.05) | tight pegs (2.2-1), tunes fit without re-rendering | plate-wide: also narrows the tab neck and the outer edge by the same amount; untested on this joint | nothing; re-slice |
| D | `seam_position` aligned → **back** or a painted seam away from the joint | seam on a slot flank (2.2-2) | moves the seam line onto the visible face | nothing |
| E | first layer slower (the Bambu guide's example: outer wall 30, infill 60 mm/s) | first-layer gaps (1.1-5), cleaner joint bottom | slower first layer | a few minutes per plate |
| F | filament flow 0.98 → 1.00, after a flow calibration | even top gaps (1.1-3) | over-extrusion tightens the pegs — do it **before** the clearance ladder, not after | a calibration print |

On C: a negative contour compensation of −x narrows the tab by x on each flank and, because the
slot is part of the same outer contour, widens the slot by x on each flank — so the gap on each
face grows by 2x when two such pieces mate. Hole compensation would **not** reach the slot: the
Bambu wiki says it "only applies to closed paths", and the slot is open to the outside. The
openings in the artwork are closed holes, so C leaves them alone. The Bambu page on this is
[X-Y compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation);
the "PLA 0.05" starting value seen for it came from a search snippet only.

Not recommended: **ironing**. The top of each strap is 2 mm wide, and the wiki warns ironing
rubs the part (a small piece can be knocked loose) and, run slow with PLA, risks heat creep and
clogs. It fixes a cosmetic top, not the holes above.

### 4.3 DSL knob changes (bikar parameters)

| Knob | Change | Fixes | Risks | Costs |
|---|---|---|---|---|
| `clearance` | 0.10 → back to 0.15, and ladder it (§5.2) | tight pegs | 0.15 was "a bit loose" on minis-03 — on a 4 mm piece, so it may be right at 1.4 mm | a ladder plate |
| `strap` | 2.0 → a width the walls fill exactly, e.g. 1.7 (four lines) or 2.5 (six) | centre strip, if §4.1 fails | changes the art's look; 1.7 is near the 1.6 floor (`CAL-CST-07`) | a render |
| `wall` | 2.5 → 2.1 (the CV8 floor) | border width, −0.8 mm on the band | less material behind the slot | a render |
| a tab-corner chamfer or radius | new knob — does not exist in bikar today | tight pegs (2.2-3) | shrinks bearing area on a 1.4 mm joint | a bikar change |
| `height` | 1.4 → 1.6 or 1.8 | elephant foot's share of the joint, floppiness | thicker coaster, more plastic | a render |

**Default:** keep the dovetail `clearance` at 0.15 mm per face for any production-style plate
until the ladder in §5.2 reports — that is the CAL-FIT-01 rung the
[interlock design](coaster-interlock-design.md) already names, and the only value with a print
behind it ([minis-03](prints/2026-09-26-minis-03/index.md), "a bit loose").

## 5. Test plates

Print on the same plate type, same filament spool, same profile, and record `nozzle_type`,
spool and room humidity in the print record (minis-03 left them null).

### 5.1 Pinhole coupon

Four 30 mm hex minis of the minis-04 art at height 1.4, sliced as four objects with per-object
overrides: (1) stock; (2) change A only; (3) change B only; (4) A + B. One plate, one variable
per piece, so a photo compares them.

**Validator:** count visible holes on the top face of each piece under a raking light, same
lighting for all four.
PASS: at least one of pieces 2–4 shows clearly fewer holes than piece 1 (as a rough bar, half or
fewer) — adopt that change in the override.
FAIL: all four look the same — the cause is not the wall generator or the top pattern; go to flow
(change F) and the §1.2 table.

### 5.2 Clearance ladder

Pairs of the minis-04 piece (two copies of each, per the mating rule in
[sample-rules.md](../.claude/skills/print-coaster-samples/sample-rules.md)) at `clearance` 0.10,
0.125, 0.15 and 0.20 mm per face, height 1.4, same art. Creative3DP's coupon steps by 0.05; the
0.125 rung is added because 0.10 was tight and 0.15 was loose on a taller piece. If change C is
tried, it gets its own row (0.10 with −0.05 contour compensation), never mixed into the others.

**Validator:** for each rung, push the pair together by hand along Z, then lift one piece by its
far edge.
PASS: a rung exists where the pieces go together by hand without a tool and the joined pair holds
when lifted by one piece — the smallest such rung becomes the new `CAL-FIT-01` point for 1.4 mm
coasters, and the calipered tab and slot widths go in the print record.
FAIL: every rung either needs force or falls apart when lifted — the joint shape, not the
clearance, is the problem (check corners, seam and flatness from §2.3 before adding rungs).

## 6. Open questions only a print can answer

1. Are the holes top-skin pinholes, a strap centre strip, or seam gaps? (§1.2 photo, §5.1)
2. Does Arachne fix the straps without making the walls discontinuous at 2 mm? (§5.1)
3. Was `CAL-FIT-01`'s rung transcribed as per face when the source is diametral and assumes
   separate compensation? If so, what does per face mean on this printer? (§5.2, calipers)
4. Is the X2D's elephant-foot compensation of 0.15 right for the plate type used? (the wiki's
   25 mm cube test)
5. Is 0.98 flow right for the X2D, given the Bambu figure was stated for the X1C?
6. Does `bambu slice compose -s` accept a partial process JSON with `inherits`? (a dry run —
   `--dry-run` does not talk to the printer)
7. Which join looks best at 80 mm: slim dovetail, key or tab? (minis-05/06, Omar's eye)

## 7. What to print next

1. **Nothing yet — look at minis-04 against §1.2 and slice it for §4.1.** Free, and it cuts the
   hole causes in half.
2. **Pinhole coupon (§5.1).** Small, one plate.
3. **Clearance ladder (§5.2)**, after any flow change, since flow moves the fit.
4. **minis-05 and minis-06**, already planned, to settle the border by eye.
5. **Elephant-foot cube** from the Bambu wiki, only if §2.3 points at the first layer.
