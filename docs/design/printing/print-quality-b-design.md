---
status: superseded
---

# Print quality for thin openwork coasters (researcher B)

**Status:** research draft, 2026-09-26. Nothing in it has been printed or measured. It is
one of two independent write-ups on the same question. The sources are in
[`../../research/print-quality-b.md`](../../research/print-quality-b.md), each marked as a fetched
page or a search snippet. No decision id is taken here.

**The question.** How do we make small, thin, openwork PLA coasters print better on the
Bambu X2D? And what caused what Omar saw on the minis-04 plate
([`../../plates/minis-04.yaml`](../../plates/minis-04.yaml)) on 2026-09-26: "i see tiny holes on the
print and the peg system border is too big and pegs too tight"?

## 1. The short answer

1. **The plate was not sliced with the X2D preset it named.** Our slicer hands Studio's
   command line only the top preset file. The command line does not follow that file's
   parent presets, so every setting the parents hold fell back to Studio's built-in
   values. The sliced minis-04 file shows:
   - Arachne walls, not Classic;
   - elephant-foot compensation 0, not 0.15;
   - 4 top layers / 0.6 mm, not 5 / 1.0 mm;
   - 0.4 mm lines, not 0.42 / 0.45 mm;
   - a 0.4 mm first-layer line, not 0.5 mm;
   - a 45 °C bed, not 55 °C.

   Research §1–§2 has the evidence, including a Bambu maintainer's comment on
   BambuStudio issue #6836. This one fault feeds both the holes and the tight pegs. It is
   the first thing to fix, and fixing it costs no print.
2. **Tiny holes.** Most likely gaps left by the slicer in the narrow straps and pointy
   corners. Arachne's broken wall paths and round line ends cannot fill a sharp tip.
   Behind that come too few top layers on the wider frame and slight under-extrusion
   (flow 0.98, never calibrated). Wet filament and seam gaps are possible but have
   different tells (§3). The first check is free: open the sliced plate in Studio's
   preview and see whether the holes are already there.
3. **Pegs too tight.** Most likely the bottom-layer bulge (elephant's foot), left
   uncorrected on a piece that is only 7 layers thick. On top of that, any overgrowth of
   the outer outline is multiplied about 3× by the dovetail's shape: its straight edges
   butt with zero designed gap, and its flanks lean at 26.6°. Clearance also dropped from
   0.15 to 0.10 between minis-03 and minis-04, while the pieces went from 4 mm to 1.4 mm
   thick and from 40 mm to 80 mm across. That is three changes in one step.
4. **Border too big.** Not a print defect but geometry. The dovetail's frame is
   `depth + clearance + wall`, and the seam band between two pieces is twice that: about 11 mm on
   the default knobs. The minis-05 and minis-06 plates already carry the narrower
   options (§5). Which to keep is a question of hold against looks, and only a print
   answers it.

## 2. The fault under both defects: presets not flattened

**What we found.** `resolvePresetList` in
[`../../../tools/bambu/src/commands/slice.ts`](../../../tools/bambu/src/commands/slice.ts) turns a
preset name into the bundled leaf file and passes it to `--load-settings` as it is. The
leaf `0.20mm Standard @BBL X2D` sets only a few keys, such as wall and gap-fill speeds.
The rest come from its parents: `fdm_process_dual_0.20_nozzle_0.4`, then
`fdm_process_dual_common`, then `fdm_process_common`. In the sliced minis-04 file:
- the leaf's keys were applied (outer wall 200 mm/s, gap fill 250 mm/s);
- the parents' keys were not.

The minis-03 slice shows the same. Research §1 has the full table.

**Why.** A Bambu maintainer on BambuStudio issue #6836 wrote: "CLI has limited logic to
process the jsons, we suppose the full json has been generated before when passed to
CLI". That is an issue comment, not documentation, and a later Studio may change it
(K1).

**Open: which slice did the printer run?** If Omar sent minis-04 from the Studio desktop
app, the app may have re-sliced it with the full preset. Then the holes and tight pegs
happened under the *right* settings, and the ranking in §3 and §4 changes. He can check
in the app without touching the printer. Open the job's project and look at Process →
Quality → Wall generator and Elephant foot compensation. If they read Arachne and 0, it
printed our slice.

**The fix: flatten before slicing.** Walk the `inherits` chain in the bundled profiles.
Merge each file over its parent, child keys winning, into one process file and one
filament file. Hand those to `--load-settings`. The comment in `slice.ts` already says
extra keys must go into the one process file, because a second process file errors with
"duplicate process config file".

- **Fixes:** every plate gets Bambu's own tuned values for the X2D, not the command
  line's fallbacks.
- **Risks:**
  - The merge order has to match the desktop app's, and arrays (per-extruder values)
    have to merge as whole values.
  - Plates sliced after the fix are not comparable with minis-01 to minis-06. Anything
    learned from those plates was learned under the fallback settings.
- **Cost:** code and a test in tools/bambu. No print, no spend.

**Validator:** slice minis-04 with the fix. For **every** key that any file in the
preset chain sets, read that key back from the 3MF's project settings. Compare it with
the merged chain's value.
PASS: each key matches the merged chain. For example wall_generator is classic,
elefant_foot_compensation is 0.15, top_shell_layers is 5, initial_layer_line_width is
0.5 and hot_plate_temp is 55.
FAIL: even one key holds Studio's built-in value where the chain sets another, such as
wall_generator arachne while fdm_process_common says classic. A check on a handful of
keys, or on the total filament use, cannot pass this: one key left behind is the defect.

**Default:** after flattening, a plate uses Bambu's X2D 0.20 mm Standard chain
unchanged, including elephant-foot compensation 0.15 and 5 top layers, as
[`fdm_process_dual_0.20_nozzle_0.4.json`](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json)
sets them. This transfers because it is the vendor's preset for this exact printer,
nozzle and layer height. It was tuned for general parts, not for 1.4 mm openwork, so
the per-plate overrides below exist for when a print shows it falls short.

## 3. Tiny holes: ranked causes and how to tell them apart

Omar has not yet said *where* the holes are. That is the first thing to find out, because
it splits the causes almost by itself.

| Rank | Cause | Why it fits minis-04 | How to tell it from the others |
|---|---|---|---|
| 1 | **The slicer leaves gaps in narrow and pointy shapes.** Arachne breaks wall paths where the line count changes. Round line ends cannot fill sharp tips. | Straps are 2 mm wide. Two walls a side at 0.4 mm lines leave a sliver the slicer fills with gap-fill or wedge-shaped transition lines. The art is full of acute star points. Bambu's wall-generator page says Arachne "will generate discontinuous wall paths" that "can affect the print surface quality". Forum thread 5489 puts the gaps in "very pointy corners" and "long, narrow pointy areas". | The holes show in Studio's **slice preview** at the same spots. They repeat in the same place on identical pieces. They sit at strap crossings and star points, not on open flat areas. |
| 2 | **Too few solid top layers over infill.** | The fallback gave 4 top layers / 0.6 mm, not 5 / 1.0. Where the frame is wide enough for sparse infill, 0.6 mm of top can sag between infill lines. | Holes only on the **top** of the **wider** parts (frame, relief tops), with the infill pattern showing through. None on the narrow straps. |
| 3 | **Slight under-extrusion.** | Flow ratio 0.98, never calibrated. Bambu's troubleshooting page names 0.98 as the common case for "even gaps in the top layer". | **Evenly spaced** gaps between parallel top lines, over whole top areas, not just at corners. |
| 4 | **Seam gaps.** | Seam aligned, seam gap 15% (Bambu's default). Aligned stacks the seam at one corner. | Holes **line up vertically** on the side walls at one corner of each loop. |
| 5 | **Thin or gappy first layer.** | The first-layer line was 0.4 mm, not 0.5 mm, on a 45 °C Cool Plate setting. | Holes on the **underside** only. |
| 6 | **Wet filament.** | Not checked. | Random craters with no pattern, popping or hissing while printing, stringing. The specific signs rest on snippets only (research §7). |
| 7 | **A slicer glitch.** | BambuStudio issue #8784: pinholes in the preview on an H2S with an older Studio, cleared by re-slicing. | Holes in the preview that go away after re-slicing the same file unchanged. Different printer and version, so a weak candidate (K10). |

**Ruled out from the slice file:** ironing was off (forum thread 256619 traced holes to
ironing), and the tiny-gap filter was off (filter_out_gap_fill 0).

**First, at no cost:**
1. Open the minis-04 3MF in Studio's preview. Turn on the line-type view (gap fill, inner
   and outer wall) and compare it with a photo of the holes.
2. If the holes are in the preview, the cause is 1, 2 or 7 and it is a slicer setting.
3. If they are not, it is 3, 5 or 6 and it happened on the printer.

## 4. Pegs too tight: ranked causes and how to tell them apart

**How the dovetail meets.** From bikar's `slottedRing` in
packages/core/src/kernel3d/coaster.ts, origin/main: the tab is a trapezoid with neck `n`,
head `h = n + d` and depth `d`. The slot is the same shape grown by `c` on each face.
Two things follow.
- The **straight edges** on each side of the joint have **zero** designed gap. They are
  meant to butt.
- Each **flank** leans at atan(0.5) = 26.6° from the edge's normal, whatever `n` and `d`
  are.

**My own derivation (not from a source).** Let e be how far the printed outer outline
grows past the design on each face. Growing the outline pushes the butted edges apart
by 2e and closes each flank gap. The play left for pulling the pieces apart is then about

  play ≈ 2c − 6.5e

- At c = 0.10 the play reaches zero at e ≈ 0.03 mm. At c = 0.15 it reaches zero at
  e ≈ 0.05 mm.
- So a few hundredths of a millimetre of overgrowth is the difference between loose and
  jammed.
- Each 0.05 mm step in c moves the play by 0.10 mm, while overgrowth counts about 3×.

That fits minis-03 at 0.15 being "a bit loose" and minis-04 at 0.10 being too tight. It
does not prove it: e has never been measured.

| Rank | Cause | Why it fits | How to tell |
|---|---|---|---|
| 1 | **Elephant's foot left uncorrected.** | Compensation was 0; Bambu's X2D preset says 0.15. The pieces slide together **downward**, so a bulged first layer on the tab and a narrowed first layer in the slot rub along the whole joint. On a 1.4 mm frame the first layer is 1/7 of the joint's height; on minis-03's 4 mm it was 1/20. Bambu's page says the flare "directly affects fit" on "assemblies, snaps, rails". | A lip at the bottom edge of the tab and slot. Scrape that lip off one joint with a craft knife or deburring tool: if it now fits, this was it. |
| 2 | **The outer outline prints oversize, and the shape multiplies it.** | Any e > 0.03 mm jams c = 0.10 (derivation above). Nothing was measured. | Calipers across the tab's head, measured **above** the first layer, against the design head h = n + d (6.0 mm on defaults). Overgrowth per face is e ≈ (measured − 6.0) / 2. |
| 3 | **Seam bumps on the fit faces.** | The seam logic ranks concave corners first (Bambu seam page). The slot mouth and neck corners are concave. Aligned stacks a bump there on every layer. | A vertical line of small blobs at the same corner of each slot. The joint catches at one point, not along the whole face. |
| 4 | **Thin, large pieces curl.** | minis-04 pieces are 80 mm and 1.4 mm; the plate's own risk list says they "may be floppy". A tab that is not flat enters a flat slot at an angle and binds. | Lay each piece on glass: does it rock, or do the corners lift? |
| 5 | **Three things changed at once.** | c, height and size all changed from minis-03 to minis-04. Nothing isolates c. | Only a ladder at fixed height and size separates them (§6, test T1). |

**Not causes:**
- **Flow 0.98** under-extrudes a little, which makes parts slightly *smaller*. It cannot
  make them tighter.
- **Shrinkage** is the same on both mating pieces, so it cancels.

**A unit mix-up to fix in the record.** CAL-FIT-01's four numbers (press −0.10, snug
0.05, sliding 0.15, free 0.35) are the same numbers the creative3dp calculator gives as
**diametral** clearance, the total gap across a pin. bikar applies `c` **per face**. This
does not explain the tight fit, since per-face use is the looser reading. It does mean
the ladder was never measured in the unit bikar uses. It should be re-stated when MC-1
or T1 below settles it.

## 5. Border too big

The seam band between two dovetailed pieces is `2 × (depth + clearance + wall)`. On the
knobs of GimTvN9hw4U-minimal-pegs-coaster.bkr in bikar (depth 3, clearance 0.1, wall
2.5) that is about 11.2 mm. The plate files record these bands:

| Join | Band | Plate |
|---|---|---|
| dovetail, default knobs | 11.1 mm | [`../../plates/minis-06.yaml`](../../plates/minis-06.yaml) |
| slim dovetail (neck 2, depth 2, wall 2.1, c 0.1) | 8.4 mm | [`../../plates/minis-06.yaml`](../../plates/minis-06.yaml) |
| tab into the neighbour's opening (c 0.1) | 5.8 mm | [`../../plates/minis-05.yaml`](../../plates/minis-05.yaml) |
| butterfly key | 5.7 mm | [`../../plates/minis-05.yaml`](../../plates/minis-05.yaml) |
| no join (plain pair) | 6.0 mm | [`../../plates/minis-05.yaml`](../../plates/minis-05.yaml) |

The floors on the dovetail:
- `wall` is at least 2.1, because the art sits 1 mm into the frame and the enclosure
  check needs at least 1 mm.
- The kernel refuses a frame under `depth + c + 1.6`
  ([`sample-rules.md`](../../../.claude/skills/print-coaster-samples/sample-rules.md)).

So the dovetail cannot get much narrower than the slim version without a kernel change.
The ranked alternatives are in
[`../coaster/coaster-borderless-joins-design.md`](../coaster/coaster-borderless-joins-design.md).

One idea not on minis-05 or minis-06: **thicken the frame only behind each slot** and
keep the plain margin elsewhere. The band would drop to about the plain 6 mm except at
the joints. This needs a bikar kernel change, and it keeps a local bump the eye may
still read as a border.

The key and tab joins give a narrower band, but they hold differently. Only a print
shows whether they hold well enough.

## 6. Changes: what each fixes, risks and costs

| # | Change | Fixes | Risks | Cost |
|---|---|---|---|---|
| S1 | **Flatten the preset chain** in tools/bambu (§2). | Most of both defects, if they came from the fallbacks: elephant's foot, top layers, line widths, walls. | Merge-order bugs; breaks comparison with minis-01 to minis-06. | Code and tests. No print. |
| S2 | **A per-plate process override** in the plate file (say `profile.process_overrides: {key: value}`), merged last into the single process file. | Lets a coupon plate vary one setting (walls, seam, compensation) without a new preset. | Studio does not check setting values; a misspelt one is silently ignored. So refuse any key the flattened chain does not already have, and any value outside that key's known options. | Code and tests. No print. |
| S3 | **Try the 0.20mm High Quality @BBL X2D preset** for coaster plates. Against Standard: outer walls 60 vs 200 mm/s, gap fill 50 vs 250 mm/s, acceleration 4000 vs 10000. | Slower gap fill and outer walls may fill thin straps and pointy corners better. | Longer prints. Untested on our pieces. | One slice, then one plate. |
| S4 | **Classic walls against Arachne** on the pinhole coupon (T2). | Classic gives unbroken loops and "only one seam per layer" (Bambu wall-generator page). | Classic can drop features narrower than a line, and thin straps may lose detail. | One coupon. |
| S5 | **Keep seams off the joints.** Paint them onto the straight outer edges away from the dovetails, or try another seam position. | Seam bumps on the fit faces (cause 3). | Painting is per object in the app, which our command line cannot do today. Random scatters bumps everywhere. | A print to compare. |
| S6 | **X-Y contour compensation** as a slicer-side fit knob, a negative value to shrink the outer outline. | Overgrowth e at every joint, without touching the art. Openwork windows are holes, not outline, so they stay put (Bambu X-Y compensation page). | Two knobs, the DSL's clearance and the slicer's compensation, would then set one fit. That is the "one name, two meanings" trap. Keep compensation at 0 until T1 shows a steady overgrowth, then decide where it lives. | One ladder print. |
| S7 | **Strap width as a whole number of lines** (DSL `strap`). | Removes the sliver gap-fill has to fill (cause 1). | The right width depends on the slicer's line spacing; it is not simply 0.42 × n. Wider straps change the look. | Free to check: slice strap 1.6 / 1.8 / 2.0 / 2.2 and count gap-fill lines in the preview. |
| S8 | **Base height** (DSL `height`), e.g. 1.4 against 2.0. | More layers means the first-layer bulge is a smaller share of the joint, and the piece is stiffer (causes 1 and 4 in §4). | Omar chose thin pieces. A thicker piece is a different look. | Part of T1. |
| S9 | **Calibrate flow and flow dynamics, and dry the filament.** Omar runs these from the app or the printer's screen. | Holes cause 3 and 6. | None to the machine: these are Bambu's own calibration prints. | Omar's time. A short print. |

**Default:** clearance stays at 0.15 per face, CAL-FIT-01's sliding step, for any
dovetail printed before test T1 reports. minis-03 at 0.15 was the only pegs pair
reported "a bit loose" rather than tight. That value came from a 4 mm piece, and it may
not carry to 1.4 mm (K10). T1 is what settles it.

## 7. Test plates

Printing is Omar's call. None of these is something that could hurt the printer: they
are small flat PLA pieces on Bambu's own preset.

**T1: dovetail ladder at the real thickness.**
- Pairs of short joint strips, about 30 mm, at the real base height 1.4 mm with S1 in
  place.
- Clearance 0.075, 0.10, 0.125, 0.15, 0.175, 0.20 per face. That puts finer steps around
  the two values we have seen.
- One extra pair at 0.10 with elephant-foot compensation forced to 0 through S2. This
  isolates cause 1.

**Validator:** each pair is tried by hand, on its own.
PASS: a pair slides together by hand with no tool. The straight edges touch along their
full length with no visible gap. The pair stays joined when lifted by one piece.
FAIL: a pair needs a tool or force, or leaves a visible gap at the straight edges (too
tight). Or it falls apart when lifted by one piece (too loose).
Report the pass window per pair. "Most pairs passed" discharges nothing. The answer is
the narrowest clearance that passes and the widest that still holds.

**T2: pinhole coupon.**
- One 40 mm piece of the busiest art: thin straps and sharp star points.
- Printed four ways, varying one thing each time: walls Arachne vs Classic; top shell
  4 / 0.6 vs 5 / 1.0; Standard vs High Quality; flow as-is vs calibrated.
- Before printing, slice all four and compare their previews. Any hole already in a
  preview is a slicer finding and needs no print.

**Validator:** photograph each coupon's top and bottom under raking light.
PASS: a variant shows no hole you can see through, on every strap and star point.
FAIL: any see-through hole on any strap or point. The count per variant is the result.

## 8. Open questions only a print can answer

- **Where are the holes?** Top, underside or side walls; straps or frame. Are they in the
  slice preview? (A photo and the preview, no print.)
- **Which slice did the printer run?** Ours, or a desktop re-slice (§2)?
- **How much does this X2D grow an outline?** Does 0.15 elephant-foot compensation
  cancel the bulge at 1.4 mm? (T1)
- **Which clearance window fits** at 1.4 mm, and does it hold at 80 mm? (T1, then one
  full-size pair.)
- **Does Classic or High Quality remove the holes** without losing strap detail? (T2)
- **Do the key and tab joins hold well enough** to replace the dovetail and its 11 mm
  band? (minis-05 and minis-06)

## 9. What to print next

1. **No print.** Land S1 (flatten presets) and S2 (per-plate override). Re-slice minis-04
   and check the validator in §2.
2. **No print.** Omar checks the photo and the preview (§3), and which slice ran (§2).
3. **T2 previews only.** Slice the four variants; print only those whose previews
   differ.
4. **T1, the dovetail ladder,** with S1 in place, at 1.4 mm.
5. **The minis-05 and minis-06 joins,** re-sliced after S1, so the band choice is made on
   pieces printed with the right preset.
