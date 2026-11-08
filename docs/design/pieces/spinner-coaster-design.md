# A spinner coaster: pause the print, drop in a bearing, print over it

**Status:** design, 2026-11-08, consolidated by a checker from two independent research passes.
Nothing here has been printed, sliced or bought. The stack, the clearances and the pause layer are
starting values for two small test pieces, not settled numbers.

**Where this came from.** Two researchers answered the same question without reading each other:
researcher A ([raw findings](../../research/spinner-coaster-research-a.md),
[draft](spinner-coaster-design-a.md)) and researcher B
([raw findings](../../research/spinner-coaster-research-b.md), [draft](spinner-coaster-design-b.md)).
A checker re-opened the sources behind the claims the design rests on, checked the repo claims
against this repo and bikar, and wrote this doc. Where the two drafts disagreed, the
[agreement table](#agreement-between-the-two-passes) says which side the source supports. The two
drafts stay as the record this was built from; this is the one to act on.

**The ask** (Omar, 2026-11-08): "creating a spinner version of our coaster that we've been making in
full where the print maybe stops halfway and then we put in a spinning bearing, and then we resume
the print ... design it ... and create design.md with potentially the technique to stop the print
midway and then resume it after it's been inserted."

## In short

1. **The coaster stays still and a small round button in its middle spins.** The coaster body
   holds the bearing's outer ring. A printed button, about 25 mm across, is pressed into the
   bearing's hole after the print comes off the bed, so it turns with the inner ring.
2. **The bearing is a 6704:** 20 mm hole, 27 mm across, 4 mm thick. It is the thinnest common size
   with a hole wide enough for a button you can flick.
3. **The coaster is the straps coaster we print today, made thicker and printed face up as now:**
   5.8 mm between the straps and 7.0 mm at a strap, against today's 4.0 and 5.2.
4. **The printer pauses before layer 27 (5.2 to 5.4 mm).** Omar drops the bearing into its pocket,
   checks it sits below the rim, and presses resume. The next three layers close over the bearing's
   outer ring and leave its middle open.
5. **The bearing sits one layer (0.2 mm) below the rim,** so when printing resumes the nozzle passes
   at least 0.4 mm above the steel.
6. **Our own tools cannot carry a pause yet, and that has to be fixed before the first send.** Our
   slicing command adds no pause, and our send command refuses a file it did not slice. Bambu
   Studio's command line has an option that can add one; it has not been tried here.
7. **First print: a coupon with no steel in it,** using a printed plastic stand-in for the bearing.
   It shows what the X2D does during a pause, which no source we found says. Real bearings go in
   only on the second coupon.

## The setup this is written for

Bambu Lab X2D, 0.4 mm nozzle, PLA, 0.2 mm layers, first layer 0.2 mm. So layer *n* ends at 0.2 × *n*
mm. Our captured X2D slice settings say all of this, and that the X2D's pause command is `M400 U1`
(`tools/bambu/test/fixtures/minis-04/flattened-slice.project_settings.config`). The checker also read
the installed Bambu Studio 02.08.02.61: its shared Bambu machine profile sets
`"machine_pause_gcode": "M400 U1"`, and the X2D 0.4 nozzle profile inherits it without changing it.
At another layer height every layer number below changes.

## What spins and what stays still

| Part | Still or turning | What it is |
|---|---|---|
| Coaster body, floor, straps | still | one print, with one pause |
| Bearing outer ring | still | held sideways by the pocket wall and from above by the cap |
| Bearing inner ring | turning | touches nothing printed: there is air under it and round it |
| Button | turning | printed on its own; a stub pressed into the bearing's 20 mm hole |

The mug sits on the straps, which stand 0.2 mm above the button's top. So the button turns when a
finger flicks it, not under the mug.

**Why this split, and not the two drafts' other ideas.** The two drafts disagreed here, and the
coaster decides it.

- **Draft A spun a hub printed in the same job,** caught between two printed caps, with the coaster
  printed face down so the hub could sit one layer short of the table. That needs a coaster whose
  pattern face can lie on the bed. The straps coaster we make today cannot: its straps stand 1.2 mm
  proud of a 4 mm slab (`src/Coasters/7apC5Q9QS-8-coaster.bkr`, `height = 4`,
  `relief straps emboss 1.2`; bikar's copy of the same file says the same). Face down, the straps would touch the bed and
  the slab between them would print over air. A's hub also stands alone on the bed through the
  pause, a 21 mm island a dropped bearing could knock loose, and it needs both of the bearing's
  ring faces measured before it can be drawn. A's idea stays as a choice for a flat-faced coaster
  (open question 1).
- **Draft B spun a printed disc pressed in afterwards,** which works face up on the coaster we
  already make. But B's own stack left that disc 0.6 mm thick, and B said so. This doc keeps B's
  body and shrinks the turning part to A's hub size: a button that sits inside the cap's opening,
  beside the cap rather than above it. That gives a 1.6 mm button with no change to B's thickness.
  The button is a raised disc: it stands 1.0 mm above the coaster's top between the straps, and
  0.2 mm below the strap tops.
  Neither draft drew this; it is the checker's join of the two.
- **A spinning rim round a still middle** was ruled out by A: the coaster would stand on a 21 mm
  middle and tip under a mug set off-centre. B did not consider it. Not carried.

Counting what still has to be measured: this design needs the width of the outer ring's flat face
(for the cap) and the inner ring's (for the button's collar). The collar is on a bench part that
can be reprinted in minutes. A's hub needs both faces right inside the print that holds the steel.

## The bearing and why

| Bearing | Hole × across × thick (mm) | Coaster it needs | Turning middle | Size source |
|---|---|---|---|---|
| 608 (skateboard) | 8 × 22 × 7 | about 9 mm before straps | 8 mm hole: too small | search summaries only (both passes) |
| 688 | 8 × 16 × 5 | about 6.8 mm before straps | too small | A fetched one maker's page; B saw summaries |
| 6700 | 10 × 15 × 4 | 5.8 mm before straps | small | read by the 2026-10-27 spinner pass, not re-opened |
| **6704** | **20 × 27 × 4** | **5.8 mm before straps** | **about 25 mm button** | **re-opened by the checker** |
| 6705 | 25 × 32 × 4 | 5.8 mm before straps | about 30 mm | B fetched one shop page; A saw a summary only; not re-opened |

**Default:** a 6704, 20 × 27 × 4 mm. The checker re-opened three shop pages that agree on the size:
[SKDIN S6704](https://www.skdin.com/products/productid-S6704) (stainless, **open**, width tolerance
"-0.120mm to 0"), [Henderson Bearings](https://www.hendersonbearings.co.uk/61704-6704-thin-section-ball-bearing-20x27x4mm.html)
(steel, shield type not stated) and [Bearings Direct 6704-2RS1](https://bearingsdirect.com/6704-2rs1-ball-bearing-20x27x4-sealed-61704-2rs1)
("Rubber Seals on both sides", "Chrome Steel SAE-52100"). The width tolerance means an SKDIN 6704 is
never thicker than 4.00 mm. That is one maker's figure, so every bearing is measured anyway (V0).

**Sealed or shielded, not open.** The cap's first layer sags onto the bearing (see "Closing over the
bearing"). On an open bearing, plastic that reaches past the outer ring lands on the turning balls
and cage. A seal or shield covers that gap. This is the checker's reasoning; no source tested it.
A sealed 6704 page was read (chrome steel). A sealed **stainless** 6704 was not found by either pass:
B's draft called its pick "stainless and sealed" but linked an open stainless part. Stainless would
suit a wet coaster better, though the 2026-10-27 pass's source says 440C stainless still "may
corrode" ([spinner-middle §4](../coaster/spinner-middle-design.md#4-living-with-a-mug)). Which to
buy is open question 3.

**Not known from any source:** how wide each ring's flat face is (no page read gives the shoulder
diameters; SKDIN says its drawings "will be launched soon", per B). Both are measured with calipers
on the bearing bought, before the coupon is drawn.

## The coaster and its thickness

Printed face up, as today. z = 0 is the table face, on the bed. 6704, 0.2 mm layers:

| Height (mm) | Layers | What prints |
|---|---|---|
| 0.0 to 0.6 | 1 to 3 | solid floor everywhere |
| 0.6 to 1.0 | 4 to 5 | floor, except a round dip 23 mm across in the middle, under the inner ring and the hole |
| 1.0 to 5.2 | 6 to 26 | the body, with the 27.3 mm pocket open through it |
| **pause** | before 27 | the bearing goes in; it rests on the floor at 1.0 and its top is at 5.0 or lower |
| 5.2 to 5.8 | 27 to 29 | the cap: the body's top, reaching 0.8 mm in over the outer ring, open in the middle (25.4 mm across) |
| 5.8 to 7.0 | 30 to 35 | the straps, raised 1.2 mm as today, stopping at the opening's edge |

Total: 5.8 mm between straps and 7.0 mm at a strap, against today's 4.0 and 5.2. The coaster's
`height` knob already allows up to 16 mm. The pattern loses its middle 26 mm or so to the opening,
as the 2026-10-27 spinner pass found for any 6704 ([spinner-middle](../coaster/spinner-middle-design.md)).
Draft A's 5.6 mm was a flat slab; it compared against "4 to 4.4 mm" coasters and left out the
straps. Draft B's 5.8 and 7.0 are the ones the repo supports.

**Default:** a floor of 0.6 mm (three layers) under the middle, the least floor the coaster kernel
allows under a pocket (CAL-CST-03), and 1.0 mm under the outer ring, as draft B drew it.

**Default:** 0.4 mm of air (two layers) under the inner ring, the dip in layers 4 and 5. Two layers
of air came apart and one fused on our own [pkt-1](../plates/pkt-1.md) print (bet CAL-CLR-01). Here
the inner ring is steel and cannot fuse; the air is there so the turning ring never rubs a rough
printed floor. The number is borrowed only as the smallest gap we have seen stay open on this
printer; the reason for it here is clearance, not fusing. The dip's 23 mm edge must fall outside the inner ring and inside the outer ring's
flat face, so it is redrawn once those are measured.

### What bikar can model today

The coaster is a height field, one top surface over a flat bottom
([coaster-design](../coaster/coaster-design.md), D-064), so a closed pocket with a cap over it cannot
be said in it. A grep of bikar's core and command-line source by both passes finds no bearing, no
pause and no magnet; "bearing" appears only as a compass direction and in "load-bearing". The split
kernel already builds a closed pocket with a neck over it (bikar #320, the split-pocket coupon), the
nearest thing we own. For the coupons, the blocks are simple enough for OpenSCAD by hand. A full
pattern coaster needs a bearing pocket added to bikar, which is not designed here.

## The pocket and its clearances

| Part | Size | Why |
|---|---|---|
| Pocket wall | 27.3 mm across (13.65 radius) | the bearing's 27 plus 0.15 a side |
| Pocket depth | 4.2 mm, from the floor at 1.0 to the rim at 5.2 | the bearing's 4.0 plus one layer |
| Cap opening | 25.4 mm across (12.7 radius) | 0.8 mm over the outer ring, to be checked against its measured face |
| Wall round the pocket | at least 1.2 mm | CAL-FEA-01, the least wall we print |

**Default:** 0.15 mm a side between the bearing and the pocket wall (27.3 mm across), from
[Prusa's blog](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/), "The
most suitable spacing is 0,15mm in all directions", for parts dropped in at a pause. *It transfers
as a starting point because* Prusa's figure was for a 0.4 mm nozzle, like ours, and side clearance
depends on how far a printed wall strays, which the nozzle and line width set more than the layer
height (Prusa's was 0.15 mm, ours 0.2). It is not a measured value for our printer: a round hole
prints smaller than drawn (CAL-HOL-01, unmeasured), which eats the clearance. So coupon 1 prints
27.2, 27.3 and 27.4 mm and Omar tries a bearing in each.

The other source sits at the tight end. [Printago](https://printago.io/guides/bambu-studio-magnet-holes)
says "diameter plus about 0.1 to 0.2 mm clearance" and does not say whether that is on the diameter
or a side. Draft B read it as on the diameter (27.2 mm) and A used Prusa's (27.3); the ladder covers
both. Our sliding rung on CAL-FIT-01 is a different number again, set across the diameter of printed
parts, so it is not used here.

**The fit wanted is a drop fit:** the bearing falls in under its own weight and does not rattle. A
press fit is ruled out during a pause, because pushing hard on a part stuck to the bed can unstick it
or shift it (both drafts agree).

**Default:** the pocket is one layer (0.2 mm) deeper than the bearing, so the bearing sits just below
the layer that will cover it. Fetched sources say the same in words:
[Printago](https://printago.io/guides/bambu-studio-magnet-holes) ("sits just below a layer that will
later cover it") and a [Bambu forum thread on nuts](https://forum.bambulab.com/t/how-to-embed-a-nut-within-a-print/226107)
("set the nut a little deeper in the pocket", from draft A). No source gave a number; one layer is
the least recess a 0.2 mm layer can make. It is what keeps the nozzle off the steel if the bearing
sits a little high on a crumb.

**Dropped from draft B's first coupon:** a block with a pocket exactly as deep as the bearing (4.0
mm). With no recess, the nozzle lays the first layer straight onto steel, 0.2 mm above it, and a
single crumb puts steel in its path. A card slid across the rim would pass a flush bearing, so the
check B gave cannot catch it. No measurement is worth the machine, so that block is gone. The
question it asked (does the bearing rattle under a 0.2 mm lift) is answered by V3 on the recessed
blocks.

## The pause

### Where it goes

Bambu Studio writes a pause **after moving up to the chosen layer and before printing anything of
it**. The checker read this in Bambu Studio's own source
([GCode.cpp on master, 2026-11-08](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/GCode.cpp)):
the layer marker `; Z_HEIGHT:` (the top of the layer about to print) is written first, then, under
the comment "Normal (non-sequential) print.", the pause, then the layer's skirt and lines. The pause
itself is the line `; PAUSE_PRINTING` followed by the printer's pause command, `M400 U1` here. A Bambu
forum answer says the same from the user side: "It pauses at the start of layer 107", so to pause
after 107 is done "pause at 108"; "Correct."
([forum](https://forum.bambulab.com/t/setting-pause-in-bambu-studio/154801)). Both drafts agree.

**Default:** the pause goes on layer 27, the layer that prints from 5.2 to 5.4 mm and first covers
the pocket, from [Bambu Studio's source](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/GCode.cpp)
as read above. Layers 1 to 26 are done when it stops; the bearing's top is at 5.0 mm or lower; the
nozzle resumes printing at 5.4 mm, at least 0.4 mm above the steel.

The same source puts the pause inside the "non-sequential" branch only. **In "print by object" mode
no pause is written.** Draft A found this in the source and in a forum summary; the checker saw the
branch.

### How to set it in Bambu Studio

1. Set print sequence to **by layer**, not by object.
2. Turn **scarf seam off**. One forum thread, from draft A, says Bambu Studio 1.9.1.67 put pauses on
   the wrong layer with it on, reportedly fixed in 1.9.2; not confirmed.
3. Slice, open **Preview**, drag the layer slider on the right to **layer 27**. The slider shows a
   layer's top, so it reads 5.40. Layer 26 should still show the open pocket and layer 27 the cap
   for the first time.
4. Right-click the slider and choose **Add Pause** (both drafts' forum sources). Slice again.
5. Check the slider shows one pause, at 27, and nothing else. One old thread says adding a pause
   also showed a color change (search summary in B; fetched by A, where the user later thought it
   was only a marker). Remove a color change if there is one.
6. Do not trust a saved project to keep the pause: one user found pauses gone after closing and
   reopening (draft A, fetched forum thread, no version named). V1 runs on the file actually sent.

### Getting the pause through our own tools

This is a finding of the checker's, built on what both drafts saw. Draft A found our slicing adds
no pause; B found nothing in our tools writes one.

- Our slicing command builds the Bambu Studio command line with settings, plate and output folder
  only, and adds no pause (`tools/bambu/src/commands/slice.ts`). The checker's grep of
  `tools/bambu/src` for "custom_gcode", "load_custom_gcodes" and "M400" finds nothing.
- Our send command refuses a plate without a fresh slicer-warnings file written by our own slicing
  (`tools/bambu/src/commands/print.ts`, `warningsGateAllows`: "no sidecar → BLOCK"). So a file
  sliced with its pause in the Bambu Studio window will be refused by our send, and re-slicing it
  with our command drops the pause.
- The way through: Bambu Studio's command line has an option to load custom G-code from a JSON
  file. Draft A found it in the source; the checker found the string `load_custom_gcodes` in the
  installed 02.08.02.61 program. A third-party page,
  [Printago](https://printago.io/slicer-cli/load-custom-gcodes), documents the file: a `"gcodes"` list,
  each item with `type` (`"PausePrint"`), `print_z`, `extruder` and `color`. Nobody has run it here.
- The send's escape hatch, `--allow-unverified`, is a bypass of a gate and is not the plan.

So before coupon 1 can go through our send, our slicing has to learn to pass that option, and V1
becomes a check our slicing runs. Open question 4 lays out the choice.

### V1. The pause is in the sliced file, once, on the right layer

**Validator:** open the plate's G-code inside the exported .3mf. Count the lines `; PAUSE_PRINTING`.
Read the last `; Z_HEIGHT:` line above the pause, and check what follows it.

PASS: exactly one `; PAUSE_PRINTING`, followed by `M400 U1`; the last `; Z_HEIGHT:` above it reads
5.4; no extrusion of that layer sits between the marker and the pause.

FAIL: exactly one `; PAUSE_PRINTING`, followed by `M400 U1`, but the `; Z_HEIGHT:` above it reads 5.2.
The count passes, yet the pause comes a layer early: the pocket wall stops at 5.0, level with the
bearing's top, so the recess is gone and the nozzle would lay layer 26 straight onto steel. This is
why V1 reads the height and not only the count (from draft A's check). No pause line, two of them, or
a marker reading 5.6 also fail.

The `; Z_HEIGHT:` wording is from Bambu Studio's source, read by the checker. No sliced G-code file
is checked into this repo, so the first real file confirms it before V1 is trusted.

## What the X2D does while paused

**No source either pass found says what the X2D does during a pause:** where its head parks, whether
the nozzle and bed stay hot, or whether it times out. Every report below is from another Bambu model
or names none, and none is from Bambu staff. The checker's own search for an official page found
none either.

- **Where the head goes.** On a P1S the head "always goes to the back of the case", and "You can't
  change where the M400 U1 parks" ([forum](https://forum.bambulab.com/t/how-to-change-the-default-pause-settings/147603),
  re-opened by the checker; users, not staff). One search summary says it parks "at chute" (B, not
  fetched).
- **Heat.** One user says the nozzle heater goes off and the bed stays on (both drafts: search
  summary only). A third-party tool page says A1 printers drop the nozzle after 3 to 5 minutes (both:
  summary only). Not the X2D. A cold resume lost a Prusa print, through OctoPrint (both drafts,
  fetched).
- **How long.** "Generally, the pause is as long as you want", but one user had "a repeatable
  problem with longterm pauses actually restarting", that is, failing to resume properly after an
  overnight pause ([forum](https://forum.bambulab.com/t/is-a-print-pause-effectively-infinite/28695),
  re-opened by the checker; P-series, no model). Draft B read this as a pause that "resumes by
  itself"; the thread does not say that.
- **Moving the head by hand.** Two fetched reports, both drafts: "do not move the head manually as
  it could loose its location", and a P1S whose head hit the frame and slipped a belt.

Coupon 1 finds out on our printer with nothing at stake but plastic: where the head goes, and the
nozzle and bed temperatures on the screen at the start of the pause, at 1 minute and at 5 minutes.
The print watcher already sees a paused state (`tools/bambu/src/backends/mqtt.ts`,
`tools/bambu/src/timed-prints.ts`).

## Closing over the bearing

When the print resumes, layer 27 prints the whole top of the body and a ring reaching in over the
bearing's outer ring. From the pocket wall at 13.65 mm radius to the cap's edge at 12.7 mm, about
0.95 mm of each line hangs past the plastic: over the 0.15 mm side gap, then over steel with 0.2 mm
of air under it, so it sags onto the ring. That is about one line's reach, anchored on the body; it
is not a long bridge. Hot PLA barely sticks to cold steel, so the plastic body carries the cap and
the steel only stops the bearing lifting (B's reasoning; no source tested it).

The cap is three layers (0.6 mm), the 0.6 mm floor rule turned upside down. Our pkt-1 print had
0.6 mm bands over air come out level, so three layers is one more than the thinnest that held; laid
on steel instead of air is new. This is a starting value with no source or bet behind it, so it is
not a default; coupon 1 tests it.

The reach of 0.8 mm over the outer ring must stay inside that ring's flat face, short of the seal by
0.2 mm, once the face is measured. If the face is narrower, the opening grows to match.

**The button.** Printed on its own, top face down on the bed: a disc 24.6 mm across and 1.6 mm thick
(from 5.2 to 6.8 mm once fitted), a collar 0.2 mm tall under it that rests on the inner ring's face
out to 10.6 mm radius, and a stub 3 mm long into the 20 mm hole. Its edge has 0.4 mm of air to the
cap's opening (CAL-CLR-01, here between parts printed apart, so a comfortable gap rather than a
tight one). Its underside sits 0.2 mm above the bearing's top, so only the collar touches steel. The
stub's press fit is the press rung of CAL-FIT-01, tested on the bench with no printer involved.

**What holds what.** The pocket wall stops the bearing sliding; the cap stops it lifting, with up to
0.2 mm of play. The button's stub holds the button. Lifting the button pulls on the inner ring, the
balls and the outer ring, and the cap holds them.

## What a failed pause or resume risks, and the guard for each

The rule: no measurement is worth the machine. Every way steel or a loose part could end up in the
nozzle's path has a guard that stops the print before resume, or the option is dropped.

| What goes wrong | What it would do | Guard | Caught by |
|---|---|---|---|
| **The pause is missing** (by-object mode, a project that lost it, our slicing dropping it) | the cap prints over an empty pocket; plastic wasted, no harm | slice by layer; the pause carried by our slicing; never trust a saved project | V1, on the file sent |
| **The pause is a layer early** (scarf seam bug, off by one) | the recess is gone; the first layer is laid straight onto steel | scarf seam off; V1 reads the height | V1; and at the printer V2 fails, so the print is stopped, not resumed |
| **The pause is late** | the cap has started over the empty pocket; the bearing cannot go in | as above | Omar sees it at the pause and stops; plastic only |
| **The bearing sits high** (tilted, a crumb or string in the pocket, a thick bearing) | the hardened-steel nozzle strikes a steel ring | one-layer recess; every bearing measured (V0); the pocket checked clean before the drop; bearing pressed flat with a fingertip | V0 before, V2 at the pause; if either fails, stop, never resume |
| **The bearing is pulled up by the head** | a steel ring lifted into the nozzle's path | the pocket keeps it level; unknown whether the X2D head carries a magnet (Prusa users report magnets clinging to theirs, search summary in A; B's "a bearing is not a magnet" does not settle it, since a magnet pulls steel). **Before any steel goes in a print:** with the printer off and cold, hold a measured 6704 against the underside of the toolhead round the nozzle. If it is pulled, pause-and-cap is dropped for the split halves; if not, this unknown is settled | the bench test first; then the first pass after resume is still watched on coupon 2, and the print stopped if the ring moves |
| **The head or bed is moved by hand**, or the pause G-code is edited to move it | lost position, a shifted layer; one P1S head hit the frame | never move the head or bed; never change the machine's pause G-code (one user's bed-drop version rises back into the nozzle on tall prints, A and B) | Omar's routine; seen in the next layers, stop if shifted |
| **A hard push on the bearing** | unsticks the print or loads the bed | drop fit only; if it will not drop in, stop the print | that pocket size is the coupon's answer |
| **The nozzle cools during the pause** | a thin or missing first cap layer; a blob on resume | keep the pause short: bearing measured, out of its bag, with tweezers and the ruler at hand before the pause | coupon 1 holds its pause 5 minutes on purpose, with only a plastic stand-in in the pocket, to read the temperatures this guard relies on at 0, 1 and 5 minutes |
| **The bed cools in a long pause** | the print lifts; the cap lands out of place | the same short pause | coupon 1 reads the bed temperature |
| **The print does not resume cleanly** (head stops on the part, a blob; a long pause not restarting well) | a blob, a dirty nozzle | Omar is at the printer when the pause comes and stays; stop the print | seen at once; the print watcher sees the paused state |
| **Nobody notices the pause** | hours paused, the case above | set the pause only on a print Omar will stand by | the watcher's alert |
| **A hand near a hot head** | a burn | reach in with tweezers, away from the parked head | Omar's routine |
| **Plastic reaches past the outer ring** | an open bearing's balls and cage drag; a seal is pressed | sealed or shielded bearing; the cap stops 0.2 mm short of the measured seal edge | V3 |
| **A blob or line at the resume layer** | a mark at 5.2 mm on the edge | dry filament, a clean wiper (A's source) | judged on coupon 1 against the solid control |
| **Getting round our send's refusal with `--allow-unverified`** | a plate sent without its warnings check | teach our slicing the pause instead (open question 4) | not used |

### V0. Every bearing is no thicker than drawn

**Validator:** before the print, measure each bearing's thickness with calipers at four points round
the ring.

PASS: all four readings on every bearing are 4.00 mm or less.

FAIL: one bearing reads 3.99, 4.00, 4.00 and 4.06. Its average is fine, but at that one point its top
sits 0.14 mm under the rim instead of 0.2, and tilted on a crumb it would stand proud. That bearing
is not used. (For the stand-in ring on coupon 1, "4.00" reads "3.80", its drawn thickness.)

### V2. At the pause: the bearing is below the rim

**Validator:** with the bearing dropped in and pressed flat with a fingertip, lay a steel ruler across
the pocket's rim twice, at right angles.

PASS: both times the ruler rests on the rim, does not touch the bearing, and light shows under it all
the way across.

FAIL: the ruler rests on the rim and touches the bearing's edge on one side only. The bearing is
tilted on a crumb or a string, so one edge stands high. Stop the print; do not resume. The same if the
ruler touches the bearing all round, or rocks on it: the bearing is level with or above the rim, so
the pause came early.

### V3. After the print: the ring turns, all the way round

**Validator:** hold the body, turn the bearing's inner ring (or the fitted button) slowly through two
full turns, then flick it.

PASS: it turns evenly through both full turns and spins on after a flick, and the bearing does not
lift when the inner ring is pulled up with a finger in its hole.

FAIL: it turns freely most of the way and catches at one spot each turn: one sagged line of the cap
touches the seal or the inner ring. A quick flick hides it, so the slow turn comes first. A ring that
will not turn at all also fails; first suspect plastic past the outer ring, then a pocket too tight.

## The test pieces, in order

Each piece carries a carved id and is judged on its own. "The plate spun fine" is not an answer: one
stuck ring among good ones is the case that matters.

**Before anything: buy and measure.** A few sealed 6704s (open question 3). Measure each one's
thickness (V0) and both rings' flat faces. Draw the cap opening, the dip and the button collar from
those readings. With the printer off and cold, hold one bearing against the underside of the
toolhead round the nozzle: if the head pulls it, pause-and-cap is dropped for the split halves.
Nothing is bought until Omar says.

**Coupon 1, no steel.** One small plate, all pieces judged by id:

- **A stand-in ring,** printed beforehand: PLA, 27 × 20 mm, drawn 3.8 mm thick so it is safely
  thinner than a bearing. Measured like a bearing (V0). It is what goes in at the pause, so the whole
  routine is rehearsed with no steel on the bed. The cap will likely weld onto it, so it tests the
  drop-in, the pause and the first layer over an insert, not spinning (draft A's idea).
- **One closed block** about 35 mm across and 5.8 mm tall with the 27.3 mm pocket, the dip and the
  cap; the stand-in goes in at the pause before layer 27, V2 is run on it, then resume.
- **One solid block** the same size with no pocket, beside it: the control that shows what the pause
  itself did to the surface (draft B's idea, and Omar's standing rule of a stock control beside).
- **Three open pocket blocks** at 27.2, 27.3 and 27.4 mm, 5.2 mm tall, with the dip and no cap. They
  end at layer 26, so the pause does nothing to them. Once bearings are in hand Omar drops one in each
  and says which falls in, which sticks and which rattles.
- **Three button stubs** at three press sizes from the CAL-FIT-01 ladder, no pause involved, tried on
  a bare bearing on the bench.

It answers, with nothing to damage: where the X2D's head goes during a pause; the nozzle and bed
temperatures on the screen at 0, 1 and 5 minutes (keep this pause about 5 minutes on purpose); how
the head comes back on resume; how long the drop-in and the ruler check really take; whether layer
27 starts clean; whether the cap reaches its 0.95 mm over the gap and lies down. And which pocket size
and stub size to use.

**Coupon 2, real bearings.** Two closed blocks at the pocket size coupon 1 picked, each with a
measured 6704 dropped in at the pause, V2 run on each, the first pass after resume watched. It answers:
does the cap hold on steel, does the inner ring turn (V3), does the bearing stay in under a pull, does
the chosen button fit. Only after both coupons pass does a whole coaster get a pocket.

## The fallback: split halves, no pause

If coupon 1 shows the X2D's pause is not clean, or coupon 2 shows the cap does not hold on steel, the
same toy can be made with no pause and no steel in the printer at all. Both drafts name this as the
fallback.

| | Pause and cap (this doc) | Split halves, bearing placed by hand | Through hole, pressed in after |
|---|---|---|---|
| What it buys | one printed body, no seam; the bearing cannot fall out | no pause, no hand in the printer, no printer risk; uses the split kernel's pocket and pegs, which our split coasters already have | the simplest print |
| What it costs | Omar at the printer for every coaster; the guarded risks above | a seam round the edge; two pieces and a join that has to hold | the bearing shows from below; only friction holds it, under wet mugs |
| What it commits to | teaching our slicing to carry a pause; no unattended batches of this coaster | the split coaster family, its joins and tests | a press fit we cannot inspect once it is in |

The 2026-10-27 spinner pass leaned on split halves for the split flange coaster's middle piece
([spinner-middle](../coaster/spinner-middle-design.md)).

## Open questions for Omar

Recommended option first in each.

**1. What spins, and in which coaster?**

| Choice | What it buys | What it costs | What it commits to |
|---|---|---|---|
| **A button pressed into the bearing, in the straps coaster printed face up (recommended)** | the coaster we already make; a 1.6 mm button; the inner ring touches nothing printed | a second small part to print and press in; the button is about 25 mm across | a bikar bearing pocket on the one-piece coaster |
| A hub printed in the same job, in a flat-faced coaster printed face down (draft A) | one print, no pressing; mug face flat across hub and body | only a coaster whose pattern face can lie on the bed; the hub stands alone through the pause; both ring faces must be exact inside the print | a flat-faced coaster we do not make today |

**2. Is a coaster 7.0 mm thick at the straps (5.8 between) all right, against today's 5.2 (4.0)?**

| Choice | What it buys | What it costs | What it commits to |
|---|---|---|---|
| **7.0 mm, the button sits inside the cap (recommended)** | the thinnest stack that holds a 4 mm bearing | a 25 mm button | the stack above |
| About 7.6 mm, a 40 mm disc over the cap (draft B's first way out) | a bigger turning disc that can carry its own pattern | 0.6 mm thicker again; the disc rides over the cap with 0.4 mm of air | a thicker product |

**3. Which bearing to buy?**

| Choice | What it buys | What it costs | What it commits to |
|---|---|---|---|
| **Sealed chrome steel 6704 (recommended for the coupons)** | a page read gives the size and seals; seals keep sagged plastic off the balls | chrome steel may rust under wet mugs | a stainless search before a coaster is sold |
| Sealed stainless 6704 | better against rust ("may corrode" still) | no page found by either pass | finding a source first |
| Open stainless 6704 | page read, size and tolerance known | sagged plastic can reach the balls and cage | a narrower cap and more risk at V3 |
| A 6705 (25 × 32 × 4) instead | a bigger button at the same thickness | size read by B only, not re-opened; the pattern loses more middle | redrawn coupons |

**4. How does the pause get into the file we send?**

| Choice | What it buys | What it costs | What it commits to |
|---|---|---|---|
| **Teach our slicing to pass the pause to Bambu Studio's command line (recommended)** | our send's checks stay whole; V1 runs as part of every slice | a small tool change, untried: the option exists, nobody has run it | a code change and its test before coupon 1 |
| Slice and send from the Bambu Studio window | no code | outside our approvals, warnings check and print log | a hand path for every spinner print |

(Sending a window-sliced file through `--allow-unverified` is not offered: it bypasses a gate.)

**5. Pause and cap, or split halves?**

| Choice | What it buys | What it costs | What it commits to |
|---|---|---|---|
| **Pause and cap first, through the two coupons (recommended)** | what you asked for; one solid coaster | you at the printer for every one | the tool change in question 4 |
| Split halves now | no pause, no printer risk | a seam, a join to hold | the split coaster family |

## Agreement between the two passes

"Checker" means the checker re-opened the source on 2026-11-08 or read the repo, bikar or the
installed Bambu Studio. A claim resting on one pass only, or on a search summary, is flagged.

| Claim | A | B | Source check | Verdict |
|---|---|---|---|---|
| Bearing: 6704, 20 × 27 × 4 | yes | yes | SKDIN S6704, Henderson, Bearings Direct re-opened: all 20 × 27 × 4 | agree, confirmed |
| 6704 width never over 4.00 | not found | SKDIN "-0.120mm to 0" | re-opened: stated, for SKDIN's part | B only, confirmed for one maker; V0 still measures |
| The default bearing is sealed | open question | "stainless and sealed", linking an open part | SKDIN S6704 is "Open"; the sealed page read is chrome steel | B's pick unsourced as written; sealed chrome is the sourced pick |
| Ring face widths | unknown | unknown, about 1 mm guessed | no page gives them | agree: measure |
| 6705 is 25 × 32 × 4 | search summary | SKDIN page fetched | not re-opened | B fetched; flagged, not re-checked |
| Pause fires before the chosen layer | yes, from Bambu Studio source | yes, from the forum and Prusa | source read: layer marker, then pause, then the layer's lines; forum "pauses at the start of layer 107" re-opened | agree, confirmed |
| No pause in by-object mode | yes, source | not found | source read: pause only in the non-sequential branch | A only, confirmed |
| X2D pause command is `M400 U1` | fixture | installed profile and fixture | checker read both | agree, confirmed |
| Where the X2D parks; heat; time limit | not found for the X2D | not found for the X2D | checker's search found no official or X2D page; P1S thread re-opened: "back of the case", firmware-fixed | agree it is unknown; coupon 1 reads it |
| Nozzle off, bed on during a pause | search summary | search summary | not fetchable as a page | flagged: snippet only, other models |
| A long pause may restart badly | "may not restart well" | "resumes by itself" | thread re-opened: "problem with longterm pauses actually restarting", i.e. failing to | A's reading is right; B's misreads it |
| Don't move the head by hand | yes | yes, plus a P1S frame strike | fetched by both | agree |
| Pocket clearance | 0.15 a side (Prusa) | 0.2 on the diameter (Printago) | Prusa re-opened: "0,15mm in all directions", MK3S, 0.15 layers; Printago re-opened: "0.1 to 0.2 mm", side or diameter not said | both read their source right; ladder 27.2/27.3/27.4 covers both; default 27.3 |
| Recess one layer below the cap | yes | yes | Printago "just below a layer that will later cover it"; no source gives a number | agree; the number is ours |
| Nozzle over steel at resume | 0.4 mm | 0.4 mm | both stacks add up | agree |
| Coaster thickness today | 4 to 4.4, flat | 4.0 slab, 5.2 at straps | repo: `height = 4`, straps emboss 1.2 | B right; A left out the straps |
| Coaster face down | yes, for its hub | face up | straps coaster cannot print face down (raised straps on the bed) | B for this coaster; A's hub kept as a choice for a flat coaster |
| What turns | hub printed in the job | disc pressed in after | design choice | B's way, shrunk to A's hub size by the checker |
| B's disc 0.6 mm thick | n/a | flagged by B itself | stack adds up to 0.6 | fixed here by seating the button inside the cap's opening |
| Flush-depth pocket on the first coupon | not proposed | block P3 at 4.0 mm | nozzle 0.2 mm over steel, card check cannot catch a crumb | dropped: machine risk |
| First coupon with no steel | yes, PLA stand-in | real bearings from the start | brief asks for no steel first | A's order kept, B's solid control added |
| A bearing cannot be pulled by the head | unknown whether the head has a magnet | "a bearing is steel, not a magnet" | a magnet pulls steel; no source on the X2D head | A's hedge kept; watched on coupon 2 |
| Our slicing cannot add a pause | yes | yes | checker's grep of `tools/bambu/src`: no custom G-code, no `M400` | agree, confirmed |
| Bambu Studio's command line can load a pause | yes, source | not found | installed program contains `load_custom_gcodes`; Printago page re-opened gives the file shape | A only, confirmed to exist; untried |
| Our send refuses a window-sliced file | not found | "untested" | checker read `print.ts`: no fresh warnings file → blocked | checker's finding |
| bikar has no bearing, pause or magnet | yes | yes | both grepped; split kernel's closed pocket is the nearest | agree |
| pkt-1: one layer of air fused, two came apart | yes | yes | [pkt-1](../plates/pkt-1.md) print record line read | agree, confirmed |
| No one embeds a bearing in a coaster mid-print | "none of these queries' pages" | "none of the few seen in one search" | not searched further | agree, hedged as a search, not a fact |
