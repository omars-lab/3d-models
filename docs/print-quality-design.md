# Print quality for thin openwork coasters on the X2D

**Status:** consolidated design, 2026-09-26. Nothing in it has been printed or measured.
It merges two independent write-ups and a check of both:

- researcher A: [`print-quality-a-design.md`](print-quality-a-design.md), sources in
  [`research/print-quality-a.md`](research/print-quality-a.md);
- researcher B: [`print-quality-b-design.md`](print-quality-b-design.md), sources in
  [`research/print-quality-b.md`](research/print-quality-b.md);
- the checker's log of what was re-opened and what it says:
  [`research/print-quality-verification.md`](research/print-quality-verification.md)
  (cited below as "verification §n").

No decision id is taken here.

**The question.** Omar on minis-04 ([`plates/minis-04.yaml`](plates/minis-04.yaml)),
2026-09-26: "i see tiny holes on the print and the peg system border is too big and
pegs too tight". What caused each, and what do we change?

## 1. The short answer

1. **minis-04 was not sliced with the preset it names.** Our slicer passes Studio's
   command line only the leaf preset file, and the command line does not follow its
   parents. Every setting the parents hold fell back to Studio's built-in value: 54
   process keys and 50 filament keys differ from the chain in both the minis-03 and
   minis-04 slices (verification §1.2). A Bambu maintainer says the command line
   expects a full JSON (BambuStudio #6836). B found this; the check confirms it and
   finds more fallbacks than B listed, including a zig-zag top, cooling fans turned
   down and the aux fan off.
2. **Holes:** most likely the slicer's own gaps in 2 mm straps and sharp star points
   under Arachne walls, on settings that were not the X2D preset. Ranked in §2.
3. **Tight pegs:** most likely the dovetail's real clearance being about half of `c`
   at its tightest point, because the kernel's slot is not a true offset of the tab
   (0.047 mm at c = 0.10, derived, verification §1.4), with elephant-foot compensation
   off on a 7-layer piece on top of it. Ranked in §3.
4. **Border too big:** not a defect. The dovetail's band is about 11 mm by design, and
   minis-05 and minis-06 already carry narrower joins. §4.

Everything that printed on minis-01 to minis-06 printed on the fallback settings, if
our slice is what ran. Whether the desktop app re-sliced at send time is still open
(§6, Q1).

## 2. Tiny holes

Omar has not said where on the pieces the holes are. That one observation splits most
of the causes.

What the slice actually did (verification §1.2, §1.3): Arachne walls, no gap-fill lines
at all (Arachne widens lines instead, 0.37 to 0.67 mm on the pegs pieces), a zig-zag top
at 4 layers / 0.6 mm, travel-into-wall 0, flow 0.98, seam aligned with a 15% gap, the
aux fan at 0 and the minimum fan at 20%. Strap tops are mostly wall lines, not top
infill. The pegs pieces have no sparse infill; the minimal-frame pieces do.

| Rank | Cause | Why it fits minis-04 | How to tell it apart | Who |
|---|---|---|---|---|
| 1 | **Slicer gaps in narrow straps and sharp points**, under Arachne and the fallback settings. | Arachne's wall paths are "discontinuous" and "can affect the print surface quality" (Bambu wall-generator page; it says surface quality, not holes, so the step to holes is an inference). Forum 5489: "very pointy corners ... leaves gaps", "Long, narrow pointy areas are the worst case". The art is 2 mm straps and star points. | In Studio's slice preview at the same spots; repeats on identical pieces; at strap crossings and star tips, not on open flat areas. | B (A ranked a classic-wall strip, which did not print) |
| 2 | **Top-skin / wall pinholes** (BambuStudio #9768). | A known open Studio problem, with one X2D owner reporting it. But minis-04 printed a zig-zag top with travel-into-wall 0, not the monotonic-line top A describes, and only the exposed base top and the frames have top infill. It can act there, not on the straps. It becomes the live cause after the preset fix, when the top turns monotonic-line. | On the top face, along the line where a flat top meets a wall; not down the straps. | A |
| 3 | **Too few top layers over sparse infill.** | 4 / 0.6 mm printed instead of 5 / 1.0. Only the minimal-frame pieces have sparse infill; the pegs pieces do not. | Top holes on wide areas with the infill pattern showing through; none on the pegs pieces. | B |
| 4 | **Slight under-extrusion.** | Flow 0.98, never calibrated. Bambu's troubleshooting page calls 0.98 "normal for PLA filament with X1C" and says to raise it toward 1.00. Written for the X1C; it transfers to the X2D only if the X2D hotend behaves the same, which no one here has checked. A K-factor too high gives "lines not connected to walls". | Evenly spaced gaps across whole top areas (flow); gaps at line starts (pressure advance). | Both |
| 5 | **Weak cooling on small features.** | The fallback ran the aux fan at 0 and the minimum fan at 20% where the chain says 70 and 100. The troubleshooting page says PLA "benefits the most" from the aux fan, "mostly on small objects". Neither researcher raised this, and no source read here ties low cooling to holes rather than to sagging and rough tops, so it is a candidate only. | Droopy or rough strap tops and star tips alongside the holes. | Checker |
| 6 | **Seam gaps.** | Aligned seam, 15% gap; seams prefer concave corners, and openwork has hundreds. | Holes stacked vertically at one corner of each opening. | Both |
| 7 | **Thin first layer.** | 0.4 mm first-layer line instead of 0.5, and a 45 °C bed instead of 55. | Holes on the underside only. | Both |
| 8 | **A slicer glitch** (BambuStudio #8784). | Seen on an H2S with an older Studio, cleared by re-slicing. Different printer and version, so weak (K10). | Preview holes that go away when the same file is re-sliced unchanged. | B |
| 9 | **Wet filament.** | Not checked. The Bambu PLA page calls PLA's hygroscopicity low. The specific symptoms (craters, popping) rest on snippets only. | Random craters, popping or hissing, stringing. | Both |

Ruled out from the slice file: ironing was off (forum 256619 traced holes to ironing)
and the tiny-gap filter was off. A's "unfilled strip down a strap" needs classic walls,
and the slice used Arachne, so it did not happen on this print; it may come back after
the preset fix brings classic walls in (§5, change 4).

**First, at no cost:** a photo of the holes under a raking light, and the minis-04 slice
open in Studio's preview with the line-type view on. Holes in the preview mean causes 1,
2, 3 or 8; holes not in the preview mean 4, 5, 6, 7 or 9.

## 3. Pegs too tight

**How the joint is built** (verification §1.4). bikar's `slottedRing` makes a tab
with neck `n`, head `n + d` and depth `d`, flanks at 26.57°, and straight edges beside
it that butt with zero designed gap. The slot is made by moving the tab's corners
sideways by `c`, and the head down by `c`. That is not an outward offset of the tab: the
slot's flank is steeper than the tab's, so the gap between them shrinks from `c` at the
neck to about 0.46c (measured square to the flank) at the tab's head corner. The
interlock doc says the slot is offset "on every face" and calls the probe's version an
approximation; the kernel builds the approximation. That is a disagreement between the
doc and the code (a K7-type finding), and it is the checker's derivation, not a source.

With `e` the per-face overgrowth of every printed outline, the play for pulling two
pieces apart is roughly `1.07c − 6.6e` at d = 3 (B wrote `2c − 6.5e`; the overgrowth
factor agrees, the clearance factor does not, verification §3.4). Play reaches zero at
e ≈ 0.016 mm for c = 0.10 and e ≈ 0.025 mm for c = 0.15. Neither `e` has been measured.
If those numbers are near right, a few hundredths of a millimetre of growth separates
"loose" from "jammed", which fits minis-03 at 0.15 being "a bit loose" and minis-04 at
0.10 being tight. It fits; it does not prove it.

| Rank | Cause | Why it fits | How to tell it apart | Who |
|---|---|---|---|---|
| 1 | **Small real clearance, multiplied by any overgrowth.** | Tightest gap 0.047 mm at c = 0.10 (derived above); any outline growth above about 0.016 mm per face closes it. | Calipers across the tab head above the first layer against the design 6.0 mm: overgrowth ≈ (measured − 6.0) / 2. The joint catches near the tab's head corners, not along the whole flank. | Both (B's multiplier; the half-clearance at the head is the checker's) |
| 2 | **Elephant's foot left uncorrected.** | Compensation printed as 0; the X2D preset says 0.15. At 1.4 mm the first layer is 1 of 7 layers of the joint; on minis-03 it was 1 of 20. Bambu: on "assemblies, snaps, rails ... the flared base directly affects fit". | A lip at the bottom edge of tab and slot. Scrape it off one joint; if the pair now fits, this was it. | B (A ranked it low, believing 0.15 was on) |
| 3 | **Seam bumps on the fit faces.** | Seams prefer concave corners. The concave corners here are the bottom of the slot and the root of the tab, both on the fit (verification §3.5). | A vertical line of blobs at one corner of each joint; the joint catches at a point. | Both |
| 4 | **Thin, large pieces curl.** | 80 mm by 1.4 mm; the plate's own notes say "may be floppy". | Lay each piece on glass: does it rock or lift? | Both |
| 5 | **Sharp corners.** | Material bunches at direction changes; Prusa and Hubs both recommend a chamfer or radius on mating edges. A 0.5 mm chamfer is a third of 1.4 mm, so its size needs a test. | Freed by rounding the tab corners with a blade. | A |
| 6 | **Three things changed at once.** | Clearance, height and size all changed from minis-03 to minis-04. | Only a ladder at fixed height and size separates them (T1). | B |

Not causes: flow 0.98 makes parts slightly smaller, not tighter; shrinkage is the same
on both mating pieces and cancels. Both researchers agree.

**The clearance ladder's unit.** CAL-FIT-01's numbers (press −0.1, snug 0.05, sliding
0.15, free 0.35) are Creative3DP's **diametral** ladder, which assumes the printer's
hole and shaft errors are compensated separately. bikar applies `c` per face and we
apply no compensation. Per face is the looser reading, so the unit alone does not
explain a tight fit; but the ladder was never measured in the unit bikar uses, and the
coaster doc's transfer sentence does not say so. A's reading that 0.10 per face sits
"between snug and close running" is off: 0.20 across sits between close running (0.15)
and free (0.35) (verification §3.3).

## 4. Border too big

By design. The band where two dovetailed pieces meet is
`2 × (depth + clearance + wall)`, about 11 mm on minis-04's knobs. Both researchers list the same alternatives,
already on plates:

| Join | Band | Plate |
|---|---|---|
| dovetail, minis-04 knobs (neck 3, depth 3, wall 2.5) | ~11.1 mm | [`plates/minis-04.yaml`](plates/minis-04.yaml) |
| slim dovetail (neck 2, depth 2, wall 2.1) | ~8.4 mm | [`plates/minis-06.yaml`](plates/minis-06.yaml) |
| no join (plain pair) | ~6.0 mm | [`plates/minis-05.yaml`](plates/minis-05.yaml) |
| tab into the neighbour's opening | ~5.8 mm | [`plates/minis-05.yaml`](plates/minis-05.yaml) |
| butterfly key | ~5.7 mm | [`plates/minis-05.yaml`](plates/minis-05.yaml) |

The ranked options are in [`coaster-borderless-joins-design.md`](coaster-borderless-joins-design.md).
The slim dovetail sits at the kernel's frame floor; the key needs a separate part and its
own ladder; the tab gives no pull-apart lock. B adds one idea on neither plate: thicken
the frame only behind each slot (a bikar kernel change). Which looks and holds best is
Omar's call from printed pieces, and those pieces should be sliced after change 1.

## 5. Changes, in order

Ordered by value per unit of effort and risk. None needs a print until change 5.

| # | Change | Fixes | Risks | Cost |
|---|---|---|---|---|
| 1 | **Flatten the preset chain** in tools/bambu before `--load-settings`: walk `inherits`, merge child over parent (lists replaced whole, the maintainer's own merge in #6836), drop `inherits`, write one process and one filament file. | Every fallback in verification §1.2: walls, elephant foot, top layers and pattern, line widths, cooling, bed temperature. | The merge must match the desktop app's (the maintainer's script is the only statement of it we have); the CLI also clamps machine limits, which flattening does not touch; plates sliced after it are not comparable with minis-01 to 06. | Code and a test. No print. |
| 2 | **Re-slice minis-04 and compare previews**, before and after change 1, with the line-type view. | Tells which hole causes are slicer-side, and whether classic walls now leave a strip in the 2 mm straps (A's cause 2). | None. | No print. |
| 3 | **Make the dovetail slot a true outward offset of the tab** in bikar's `slottedRing`, or at least state the real gap at the head in the interlock doc and the knob's range. | Makes `c` mean what the doc says; the head-corner gap goes from ~0.46c to c. | A kernel change moves every dovetail piece's geometry; old plates stop matching. The fix is a bikar PR, not this repo. | Code and a geometry test. No print. |
| 4 | **A per-plate process override** in the plate file, merged last into the one process file, that refuses any key the flattened chain does not have. | Lets a coupon vary one setting (walls, seam, compensation, top pattern) without a new preset. | Studio does not check values, so a misspelt key is silently ignored unless we refuse it. | Code and tests. No print. |
| 5 | **T1: dovetail ladder at 1.4 mm**, after changes 1 and 3. | Finds the clearance window at the real thickness, and whether elephant-foot 0.15 is enough. | Uses Omar's time and filament; printing is his call. | One small plate. |
| 6 | **T2: pinhole coupon**, previews first. Arachne vs Classic; top 4 / 0.6 vs 5 / 1.0; Standard vs High Quality; flow as-is vs calibrated. Print only variants whose previews differ. | Holes causes 1 to 4. | High Quality prints slower. Classic can drop features narrower than a line. | Free to slice; up to four coupons. |
| 7 | **Keep seams off the joints** (paint them onto straight outer edges, or another seam position). | Pegs cause 3; holes cause 6. | Seam painting is per object in the app; our command line cannot do it today. | One print to compare. |
| 8 | **Strap width as a whole number of lines** (DSL `strap`), checked in the preview. | The sliver between walls, if classic walls come back. | The right width depends on the slicer's line spacing, not just 0.42 × n; wider straps change the look. | Free: slice 1.6 / 1.8 / 2.0 / 2.2 and look. |
| 9 | **Calibrate flow and pressure advance, and dry the filament** from the app or the printer's screen. | Holes causes 4 and 9. | None to the machine: these are Bambu's own calibration prints. | Omar's time. |
| 10 | **X-Y contour compensation**, only if T1 shows a steady overgrowth. | Overgrowth at every joint without touching the art (openwork windows are holes, not contour). | Two knobs, the DSL's clearance and the slicer's compensation, would then set one fit: the "one name, two meanings" trap. | One ladder print. |
| 11 | **Base height** (DSL `height`), 1.4 against 2.0. | Smaller first-layer share of the joint; stiffer piece. | Omar chose thin pieces; thicker is a different look. | Part of T1. |

**Validator (change 1):** slice minis-04 with the fix and read every key that any file
in the preset chain sets back from the 3MF's project settings.
PASS: every key equals the flattened chain's value, for example wall_generator classic,
elefant_foot_compensation 0.15, top_shell_layers 5, top_surface_pattern monotonicline,
additional_cooling_fan_speed 70 and hot_plate_temp 55.
FAIL: any one key holds Studio's built-in value where the chain sets another, such as
top_surface_pattern zig-zag. A check on a handful of keys cannot pass this; one key left
behind is the defect.

Change 1 shipped in [#349](https://github.com/omars-lab/3d-models/pull/349): `bambu slice` now flattens each chain and runs this check after every plate and compose slice. The minis-04 re-slice passes, and the old minis-04 settings fail on 128 keys.

**Validator (change 3):** for the tab and slot at n = 3, d = 3, c = 0.10, compute the
shortest distance from every tab edge to the slot outline at the mated position.
PASS: the flank and head distances are each at least c less 0.001 mm, along the whole
flank including the head corner.
FAIL: any point closer than that, as today's kernel gives at the tab's head corner
(about 0.047 mm). The straight edges beside the joint are excluded: they butt by design.

Change 3 shipped in [bikar #262](https://github.com/NaqshCoffee/bikar/pull/262): the slot is now the tab offset outward by c, corners mitred. At c = 0.10 the head-corner gap went from 0.0465 mm to 0.1000 mm, and a test fails the old kernel in all 27 cases (c 0.05, 0.10, 0.15 × three neck/depth pairs). Only the first c/√5 of each flank, at the slot mouth, opens to at most 1.118c. Side effect: pull-apart play is now about 2.24c, where it was about 1.07c. The key and tab clearance defaults were set against the old reasoning; the key's moved from 0.075 to the dovetail's 0.15 per face and the tab's stays at 0.15 ([bikar #264](https://github.com/NaqshCoffee/bikar/pull/264)). Pieces printed before it, minis-03 and minis-04 included, have the old slot.

**Default:** after change 1, a plate uses Bambu's X2D 0.20 mm Standard chain unchanged,
including elephant-foot compensation 0.15 and 5 top layers, as
[`fdm_process_dual_0.20_nozzle_0.4.json`](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json)
sets them. This transfers because it is the vendor's preset for this printer, nozzle and
layer height; it was tuned for general parts, not 1.4 mm openwork, which is what change 4
is for.

**Default:** dovetail clearance stays at 0.15 per face for any plate meant to be kept,
the sliding step of CAL-FIT-01, until T1 settles it. This carries over only as a
starting point: the ladder is diametral and assumes compensation is applied separately,
neither of which holds here, and at today's kernel 0.15 gives about 0.07 mm at the head.

## 6. Open questions only a photo, the app or a print can answer

- **Q1. Which slice ran?** Omar opens the job's project in the desktop app and reads
  Process → Quality → Wall generator and Elephant foot compensation. Arachne and 0 means
  our fallback slice printed. No printer contact needed.
- **Q2. Where are the holes?** Top, underside or side; straps or frame; in the preview or
  not.
- **Q3. How much does this X2D grow an outline, and does 0.15 elephant-foot compensation
  cancel the bulge at 1.4 mm?** (T1)
- **Q4. Which clearance window fits at 1.4 mm**, and does it hold at 80 mm? (T1, then one
  full-size pair.)
- **Q5. Do Classic walls or High Quality remove the holes** without losing strap detail?
  (T2)
- **Q6. Do the key and tab joins hold** well enough to replace the 11 mm dovetail band?
  (minis-05 and minis-06, re-sliced after change 1.)

**Validator (T1):** each pair is tried by hand, on its own.
PASS: the pair slides together by hand with no tool, the straight edges touch along
their length with no visible gap, and the pair stays joined when lifted by one piece.
FAIL: a pair needs a tool or force, or shows a gap at the straight edges, or falls apart
when lifted by one piece. Report the window per pair; "most pairs passed" discharges
nothing.

## 7. What to print next

1. **No print.** Omar answers Q1 and Q2: which slice ran, and a photo of where the holes
   are.
2. **No print.** Land change 1 (flatten) with its validator, then change 4 (override).
   Re-slice minis-04 and compare previews (change 2).
3. **No print.** Change 3 in bikar, or at least document the real head gap.
4. **T2 previews**, then print only the variants whose previews differ.
5. **T1**, the dovetail ladder at 1.4 mm with changes 1 and 3 in place: clearance 0.075,
   0.10, 0.125, 0.15, 0.175, 0.20 per face, plus one pair at 0.10 with elephant-foot
   compensation forced to 0 through change 4, to isolate that cause.
6. **minis-05 and minis-06 re-sliced** after change 1, so the border choice is made on
   pieces printed with the right preset.

## 8. Claim table

Agreed: both researchers say it and the check holds. Disputed: they differ, or the check
contradicts one. Only-A / only-B: one said it, and the check says whether it held.
Snippet-only: rests on a search snippet no one fetched.

| Claim | Status | Check |
|---|---|---|
| The CLI does not resolve `inherits`; parent keys fell back to built-ins | only-B | Verified: 54 process and 50 filament keys differ in both slices; maintainer comment in #6836 |
| The slice used classic walls, monotonic-line top, EFC 0.15 | only-A | False for the printed slice: Arachne, zig-zag, EFC 0. True of the preset chain |
| Fallback also changed top pattern, travel-into-wall, fans, infill, arc fitting, skirt | checker | Verified in the 3MF |
| Holes cause: slicer gaps in narrow/pointy areas | only-B (A ranks it 2nd as a classic-wall strip) | Forum 5489 verified; wall-generator page says "surface quality", holes is inference |
| Holes cause: #9768 top-skin/wall pinholes | only-A (B does not list it) | Issue verified; does not match the printed top pattern; applies after change 1 and only where top infill exists |
| Holes: A's classic-wall centre strip | only-A | Did not print (Arachne, no gap fill); may return after change 1 |
| Holes: too few top layers over infill | only-B | Only the minimal-frame pieces have sparse infill |
| Flow 0.98 "normal for PLA with X1C" | agreed | Verified; X1C-to-X2D transfer unchecked |
| K-factor 0.025 → 0.012 fixed gaps | only-A | Verified (forum 68800), one poster |
| Seam prefers concave corners; seam gap 15% | agreed | Verified |
| Seam bumps at "slot mouth and neck corners" | disputed | Mouth corners are convex; the concave ones are the slot bottom and tab root (checker's reading) |
| Ironing caused holes in forum 256619; ironing off here | only-B | Verified |
| Outer wall "not last" reduced gaps (forum 15122) | only-B | **Inverted**: the poster printed outer lines *last*, and "never was able to fix it" |
| Elephant foot affects fit on assemblies | agreed | Verified |
| EFC was on at 0.15, so EF ranks low | only-A | False for the printed slice |
| First layer is 1/7 now, 1/20 on minis-03 | disputed | B right (1/20); A's "1 of 26" used total height |
| Slot is open to the edge, so it is contour not hole for compensation | agreed | Verified on the X-Y compensation page |
| CAL-FIT-01 is diametral; bikar is per face | agreed | Verified in bets.md, c2-assembly §5 and B.3 |
| 0.10 per face sits between snug and close running | only-A | Wrong: 0.20 across is between close running and free |
| 0.10 per face is below every published starting point read | only-A | Wrong against Creative3DP snug/close running and Hydra 0.1 per side; right only against Prusa 0.3 and Hubs 0.5 |
| The interlock doc's port of CAL-FIT-01 lacks a transfer condition | only-A | Verified |
| Play ≈ 2c − 6.5e | only-B | Clearance factor overstated: the kernel slot is not a true offset; ≈ 1.07c − 6.6e at d = 3 (derived) |
| Kernel slot is narrower than a true offset; head gap ≈ 0.46c | checker | Derived from the kernel source, hand-checked; not printed |
| Straight edges butt at zero gap; flanks at 26.57° | only-B | Verified in `slottedRing` |
| Shrinkage cancels; flow cannot tighten | agreed | Reasoning, not measured |
| Dovetail band ≈ 11 mm; alternatives on minis-05/06 | agreed | Matches the plate files |
| Prusa "at least 0.3 mm" for movable parts | agreed | Verified; per side or total not stated |
| Hubs / Formlabs FDM 0.5 mm | agreed | Verified; Formlabs' 0.2 / 0.4 are for SLA/SLS |
| Forum 87473 dovetails "about 0.04mm gap" | only-B | Verified; one P1S user, unit not stated |
| #8784 preview pinholes on H2S | only-B | Verified |
| Aux fan at 0 as a hole cause | checker | Candidate only; no source read here ties it to holes |
| Which slice the printer ran | open | Unchecked; Q1 |
| Bambu forum 123711: "0.1 and 0.15 is more than enough" | only-A (as a snippet) | Now fetched and verified; unit unclear, X1C/P1S users |
| PLA X-Y compensation about 0.05 | snippet-only | Not on the fetched Bambu page |
| BambuStudio #3817: unequal hole and contour values leave a ring | snippet-only | Not fetched |
| Per-side ladders: Sovol / utility guides, industrialmonitordirect, artopia | snippet-only | Not fetched |
| Prusa forum tolerance threads; Prusa KB "at least 0.3 mm" article | snippet-only | Not fetched (the Prusa modeling page's 0.3 mm is verified) |
| MakerWorld tolerance tests (132619, 640436); Printables 32321 | snippet-only | Not fetched by anyone |
| Bambu forum jigsaw-connector "0.30 mm" start | snippet-only | Not fetched |
| Gridfinity clip clearances | snippet-only | Not fetched |
| Wet-filament signs (craters, popping); Sovol, Siraya pages | snippet-only | Not fetched |
| Pinhole cause lists (3dprofilefix, fashion3d); seam-gap and gap-filter snippets | snippet-only | Not fetched |
| Ironing flow 15–30% | snippet-only | Not fetched; ironing is off anyway |
