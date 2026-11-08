# A spinner coaster: a ball bearing dropped in mid-print (draft A)

**Status:** draft from researcher A, one of two independent passes, 2026-11-08. A checker compares
this with draft B and writes the doc to act on. Nothing here has been printed. The research behind
it, with every source and whether it was read or only seen in a search summary, is
[spinner-coaster-research-a.md](../../research/spinner-coaster-research-a.md) (S1 to S37 are its
sources, R1 to R10 its repo findings).

## In short

1. **The centre spins, the coaster stays still.** The coaster body holds the bearing's outer ring.
   A small round printed hub holds its inner ring. Hub and body print in the same job as two
   separate parts, with the bearing between them. A bearing shut inside one printed part cannot
   turn, so the two parts are the whole trick.
2. **The bearing is a 6704: 20 mm hole, 27 mm across, 4 mm thick, steel.** It is the thinnest common
   size with a hole wide enough for a hub you can flick with a finger.
3. **The coaster grows to 5.6 mm thick**, from today's 4 to 4.4 mm. A 4 mm bearing plus a floor and
   a cap cannot fit in less.
4. **It prints face down. The printer pauses before layer 25 (5.00 mm)**, Omar drops the bearing
   onto the hub's post, checks it sits below the rim, and presses resume. The next layers close over
   both rings of the bearing.
5. **The bearing sits one layer (0.2 mm) below the rim.** So the nozzle passes 0.4 mm above the steel,
   never at it, and the first layer after the pause is anchored on plastic.
6. **First print: a pocket coupon with no steel in it at all.** It tests the pause itself (where the
   X2D parks, whether it comes back clean) and the pocket sizes. Real bearings go in only on the
   second coupon.
7. **The biggest unknown is the X2D itself.** No source found says what the X2D does while paused:
   where the head goes, what stays hot, how it moves up and down. The first coupon finds out with
   nothing at stake but plastic.

## The setup this is written for

Bambu Lab X2D, 0.4 mm nozzle, PLA, 0.2 mm layers, first layer 0.2 mm, pause G-code `M400 U1` (R4).
So layer *n* tops out at 0.2 × *n* mm. Any number below that depends on the layer height says so;
at another layer height the layer numbers change.

## What spins and what stays still

Two parts print together, in one job:

- **The body** is the coaster. Around the bearing it has a **lower lip** under the outer ring, the
  **pocket wall** round the outside of the bearing, and an **upper lip** printed over the outer ring
  after the pause.
- **The hub** is a small spool in the middle. It has a **bottom disc** under the inner ring, a
  **post** up through the bearing's hole, and a **cap** printed over the inner ring and the top of the
  post after the pause.

The bearing is clamped by the body on its outer ring and by the hub on its inner ring, so turning
the hub turns only the inner ring. Between the hub and the body there is an open ring about 1.9 mm
wide on each face, over the part of the bearing between its two rings (its shields). Nothing of the
hub touches the body anywhere.

**Why the centre and not the rim.** A spinning rim round a still centre would stand on the centre
alone: a 21 mm disc under a 90 mm coaster, which tips when a mug sits off-centre, and the rim then
drags on the table. With the hub spinning, the whole body sits flat on the table and the hub is the
part that lifts clear (see the next section). Omar may still want the rim to spin; that is open
question 1.

**Which face is down.** The hub must not rub the table, so its table-side face has to sit one layer
below the body's. Only the last-printed face can be set down like that, because the first layer
lies flat on the bed for both parts. So the table face prints last and **the mug face prints on the
bed**, as the split-pocket coaster's halves already do ("face down", R1). Both mug-side faces are
flush; a mug sits across body and hub alike.

## Which bearing

| Bearing | Hole × across × thick (mm) | Source | Coaster thickness it needs | Hub you can flick |
|---|---|---|---|---|
| MR128 | 8 × 12 × 3.5 | S33, search summary only | 5.1 | about 10 mm across: too small |
| 6700 | 10 × 15 × 4 | S31 (read by the 2026-10-27 pass) | 5.6 | about 12 mm: small |
| **6704** | **20 × 27 × 4** | **S30, read** | **5.6** | **about 21.6 mm** |
| 6705 | 25 × 32 × 4 | S36, search summary only | 5.6 | about 26.6 mm |
| 688 | 8 × 16 × 5 | S29, read | 6.6 | about 10 mm |
| 608 | 8 × 22 × 7 | S32, search summary only | 8.6 | about 10 mm |

The thickness column is floor 0.6 + bearing + one layer of recess 0.2 + cap 0.8 (the next sections).
The hub column is the bearing's hole plus 0.8 mm of cap over the inner ring on each side.

**Default:** a 6704 (20 × 27 × 4 mm, steel), from the one fetched spec,
[Henderson Bearings](https://www.hendersonbearings.co.uk/61704-6704-thin-section-ball-bearing-20x27x4mm.html).
It is the thinnest kind (4 mm) whose hub is big enough to spin with a fingertip. The 6705 would give
a bigger hub at the same thickness, but its size rests on a marketplace listing only (S36), so it
waits until a maker's page confirms it. A 608, the fidget-spinner standard, would make the coaster
8.6 mm thick.

**What we do not know about the 6704.** How wide each ring's flat face is (the "land" plastic can
press on without touching the shields); the hub's cap must stay inside it. No source here gives it,
so the drawing uses 0.8 mm until a bearing in hand is measured with calipers. Whether the shields
are metal or rubber on the one we buy: Henderson's page does not say. Whether chrome steel rusts in
a coaster that gets wet: no source here covers it (open question 5).

## The pocket and its clearances

All sizes for the 6704; radii from the centre.

| Part | Size | Why |
|---|---|---|
| Hub post | 9.85 mm radius (19.7 across) | bearing hole 10 less the clearance |
| Pocket wall | 13.65 mm radius (27.3 across) | bearing 13.5 plus the clearance |
| Hub disc and hub cap | out to 10.8 mm radius | 0.8 mm over the inner ring, inside its land |
| Body lips | in to 12.7 mm radius | 0.8 mm over the outer ring, inside its land |
| Open ring between hub and body | 10.8 to 12.7 mm, 1.9 mm wide | over the shields; plastic never touches them |
| Wall round the pocket | at least 1.2 mm | CAL-FEA-01, the least wall we print |

**Default:** 0.15 mm clearance per side between the bearing and both the post and the pocket wall,
the spacing [Prusa's blog](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/)
gives for parts dropped in at a pause ("0,15mm in all directions"). *Does it transfer?* Prusa's
figure was for an MK3S with a 0.4 mm nozzle and 0.15 mm layers. Our nozzle is the same, so the wall
line width that decides how far a printed wall strays is the same; our layer is thicker, which
matters for heights, not for these side clearances. It transfers as a starting point, not as a
measured value: a round hole prints smaller than drawn (CAL-HOL-01, unmeasured) and a post larger,
so both errors eat the clearance. That is why the first coupon prints 0.10, 0.15 and 0.20 mm and
Omar test-fits a bearing in each. Our own sliding rung, CAL-FIT-01's 0.15, is across the diameter
(about 0.075 per side), so it is tighter than this and not the same number.

**Default:** the gap between hub and body is 1.9 mm, well over the 0.4 mm least gap that prints as
two parts (CAL-CLR-01). The gap is set by the bearing's shields, not by the print, so there is no
fusing risk to tune here. pkt-1's 0.4 mm result (R3) was measured on a gap of a different
direction from this one (R5), so it would transfer only as a hint; with 1.9 mm it does not need to.

## The layers, bottom to top

Printed face down, so z = 0 is the mug face.

| Height (mm) | Layers | Body | Hub |
|---|---|---|---|
| 0 to 0.6 | 1 to 3 | floor, with the lower lip under the outer ring | bottom disc under the inner ring |
| 0.6 to 4.8 | 4 to 24 | pocket wall and the rest of the coaster | post through the bearing's hole |
| — | pause before 25 | Omar drops the bearing in; it rests at 0.6 to 4.6 | |
| 4.8 to 5.6 | 25 to 28 | upper lip over the outer ring, the rest of the coaster | cap over the inner ring, 25 to 27 only (to 5.4) |

**Default:** a floor of 0.6 mm, three layers, under the bearing, from CAL-CST-03 (the least floor
that does not print see-through or cup).

**Default:** the bearing sits 0.2 mm, one layer, below the rim at the pause, as forum advice for
nuts gives it ("set the nut a little deeper in the pocket" so the nozzle "bridges" without touching
it, [Bambu forum](https://forum.bambulab.com/t/how-to-embed-a-nut-within-a-print/226107)) and as
[Printago](https://printago.io/guides/bambu-studio-magnet-holes) puts it for magnets ("just below a
layer that will later cover it"). *Why recessed and not flush with the last layer:* the bearing's
thickness and the printed floor's height each vary by a few hundredths, and the nozzle must never
meet steel. With the recess, the nozzle prints layer 25 with its tip at 5.0 mm while the steel's top
is at 4.6: 0.4 mm apart. The first lines of layer 25 then reach out over 0.2 mm of air from the wall
and the post, about 0.95 mm each way, and sag onto the rings. That is the overhang a lip already
prints over air in pkt-1; it is not a long bridge.

**The cap.** The body's upper lip is 0.8 mm (four layers: the 0.6 mm floor rule, CAL-CST-03, plus
the one layer the hub sits below it). The hub's cap is 0.6 mm (three layers) and stops one layer
short of the body's top. That one layer is what keeps the hub off the table. It is a design choice
no source backs; the coupon shows whether 0.2 mm is enough to stop it rubbing, and 0.4 mm is the next
try.

**What holds what.** On the table, the mug's weight goes into the body and the hub's disc, through
the bearing, into the body's upper lip, and onto the table. Every load is plastic pressing on steel;
nothing hangs on a thin layer.

## Setting the pause in Bambu Studio

From Bambu Studio's own source (S2): a pause is written after the head moves up to the chosen layer
and before anything of that layer prints. So "pause at layer 25" means layers 1 to 24 are done and
layer 25 is not started. Prusa says the same of its slicer (S9, S10), and warns that people often
put it one layer off.

1. Slice the plate as usual, with **print sequence "by layer"**. In "by object" mode Bambu Studio
   does not write the pause at all (S2) and greys out the menu item (S8).
2. Turn **scarf seam off**. Bambu Studio 1.9.1.67 put pauses on the wrong layer with it on,
   reportedly fixed in 1.9.2, not confirmed (S14).
3. Open **Preview**, drag the layer slider to **layer 25, 5.00 mm**, right-click the "+" on the
   slider and choose **Add Pause** (S7, S21). Slice again (S21).
4. Check the slider marks one pause at 25 and nowhere else. On printers with an AMS the pause can show
   as a color change in the preview; one user found it was only a marker (S18).
5. Export and run the slice check (Validator V1) on the exported file before any send.
6. Do not rely on the project file keeping the pause: one user found pauses vanished when a project
   was closed and reopened (S15, no version named). Re-check it every time the project is opened.

**Our own tools cannot add a pause yet.** They slice through the Bambu Studio command line and write
no pause into the input file (R7, R8). Bambu Studio has two ways in: the pause stored in the 3MF as
`Metadata/custom_gcode_per_layer.xml`, which the command line reads only when it loads the project's
settings (S4), and a `load_custom_gcodes` option that takes a JSON file (S5). Neither has been tried
here. So the first coupon is set up in the GUI, and teaching our tools is follow-up work that V1
checks either way.

### V1. The pause is in the sliced file, once, at the right layer

**Validator:** open the sliced G-code in the exported 3MF and count the lines reading
`; PAUSE_PRINTING` (the tag Bambu Studio writes before the pause, S2, S3). There must be exactly one,
followed by `M400 U1`, and the last layer-height marker above it must be 5.0 mm (the marker's exact
wording to be copied from the first real file).

PASS: one `; PAUSE_PRINTING`, then `M400 U1`, sitting after the move to 5.0 mm and before layer 25's
first extrusion.

FAIL: one `; PAUSE_PRINTING` above the 4.8 mm layer instead. One tag is present and the count alone
would pass, but the pause would come a layer early, with the walls lower than the bearing, so the
nozzle would cross proud steel. This is why V1 checks the height, not just the count. Zero tags (by
object mode, or a project that lost its pause) and two tags also fail.

## Risks, and the guard for each

"No measurement is worth the machine": every risk that could touch the printer has a guard that
stops the print before the nozzle gets near steel.

| What goes wrong | What it would do | Guard | How it is caught |
|---|---|---|---|
| **The pause is missing** (by-object mode, a lost pause, our command line) | the print runs on and caps an empty pocket: a wasted print, no harm to the printer | slice by layer; re-check after opening the project | V1 before the send |
| **The pause is a layer early** (scarf seam bug, off by one) | the walls end below the bearing's top: the nozzle would cross steel | scarf seam off; V1 checks the height | V1; and V2 at the printer: the rim check fails, so the print is stopped, not resumed |
| **The pause is late** | the cap has started over the empty pocket; the bearing cannot go in | as above | Omar sees it at the pause and stops the print; plastic only |
| **The bearing sits proud** (tilted, not pushed down, a blob or string in the pocket, a thick bearing) | the nozzle strikes it | 0.2 mm recess; the post and wall hold it level; Omar pushes it down; each bearing measured first | V0 before, V2 at the pause; if either fails, stop, never resume |
| **The bearing is pulled up by the toolhead** | a steel ring lifted into the nozzle path | the post keeps it centred; it is not a magnet itself | unknown whether the X2D head has a magnet (Prusa users report one in theirs, S23, search summary); coupon 2's first pass is watched, and the print stopped if the ring moves |
| **A layer shift on resume** | a stepped coaster, cap off centre | do not touch or move the head; only push the bearing straight down (S7: moving the head "could loose its location") | seen in the next layers; stop if shifted |
| **The bed cools and a part lifts** (the hub disc is a small island) | the hub tilts, the cap prints crooked | keep the pause short: bearing out of its bag and at hand before the pause; users report the bed stays on during a pause (S13, other Bambu models; not known for the X2D) | coupon 1 times a pause and checks the hub is still flat |
| **A blob or gap at the resume layer** (S16, S17; a visible line, S23) | a mark on layer 25 | it lands on the table face, which no one sees; dry filament; a clean wiper (S17) | judged on coupon 1 |
| **The print does not resume**, the head sits on the part (S16) | a blob on the part, a dirty nozzle | Omar is at the printer; stop the print | seen at once |
| **Nobody notices the pause** | the bed cools for hours; a long pause may not restart well (S6) | Omar sets the pause up only when he will be there; the print watcher sees the paused state (R9) | the watcher's alert |
| **Plastic touches the shields** (cap reaching too far) | the hub turns stiffly | caps stay inside the measured ring faces | V3 |
| **The bearing rusts** | a stiff, stained hub | open question 5 | after use, not at print |

## The test pieces, in order

Each piece carries a carved id and is judged on its own. "The plate spun fine" is not an answer:
one stuck hub among good ones is the case that matters.

**Coupon 1 — the pause with no steel.** One small plate, about 20 minutes, no bearings needed:

- three **open pocket tiles**, each a 32 mm square at 4.8 mm tall with a pocket and post at
  clearance 0.10, 0.15 and 0.20 mm per side, and no cap. They stop at the rim, so the pause does
  nothing to them. Once bearings are in hand, Omar tries one in each and says which drops in, which
  sticks, which rattles.
- one **closed tile** at 0.15 mm, the full 5.6 mm with its cap. The printer pauses before layer 25,
  Omar drops in nothing, checks the empty pocket with a straightedge, and resumes.

It answers, with nothing to damage: where the X2D parks during a pause; whether the nozzle and the
bed stay hot (read from the printer's own reports, R9); how the head moves up and down on pause and
resume; whether layer 25 starts clean or with a blob; whether the caps print over air at 0.95 mm.

**Coupon 2 — real bearings.** Two closed tiles at the clearance coupon 1 picked, each with a 6704
dropped in at the pause. It answers: does the hub turn, does the first layer over steel hold, does
the hub clear the table. Only after both pass does a whole coaster get a pocket.

### V0. The bearing is no thicker than drawn

**Validator:** each bearing is measured across its thickness with calipers at four points round the
ring, before the print.

PASS: all four readings on every bearing are 4.00 mm or less.

FAIL: one bearing reads 3.99, 4.00, 4.00 and 4.06. Its average is fine, but at that one point its top
sits 0.14 mm under the rim instead of 0.2, and if the ring also tilts it is proud. That bearing is not
used.

### V2. At the pause: the bearing is below the rim

**Validator:** with the bearing pushed down onto the post, lay a steel ruler across the pocket's rim
in two directions, at right angles.

PASS: both times the ruler rests on the rim, does not touch the bearing, and light shows under it all
the way across.

FAIL: the ruler rests on the rim but touches the bearing's edge on one side only. The bearing is
tilted, with a blob or a string under one side, so one edge stands higher than the rest. Stop the
print; do not resume. The same goes when the ruler cannot sit on the rim at all because the bearing
stands higher than the walls (the pause came early).

### V3. After the print: the hub turns, all the way round

**Validator:** hold the body, turn the hub slowly through two full turns, then flick it.

PASS: it turns evenly through both full turns and spins on after a flick.

FAIL: it turns freely most of the way and catches at one spot each turn. One sagged line of the cap
touches a shield. A quick flick can hide it, so the slow turn comes first. A hub that will not turn
at all also fails; then the first suspect is plastic on the shields, the second a clearance too
tight.

## Other ways, side by side

| | A. Pause and drop in (this doc) | B. A split coaster closed by hand round the bearing | C. Press the bearing in after printing |
|---|---|---|---|
| What it gives | one solid coaster, no seam | no pause and no steel in the printer at all; our split coasters already close by hand (R1, R6) | the simplest print |
| What it costs | a person at the printer for each coaster; the pause risks above | a seam round the edge; the halves need pegs and a hold that lasts (the split work in progress) | nothing holds the bearing but friction or glue; glue near a bearing stops it |
| Printer risk | small, guarded by V0 to V2 | none | none |
| What it commits us to | the 5.6 mm coaster; teaching our tools to add a pause | the split coaster line, at 5.6 mm or more | a fit we cannot see once it is in |

A is the recommendation because it is what Omar asked for and it makes a solid coaster. B is the
fallback if coupon 1 shows the X2D's pause is not clean. The earlier spinner study (R6) leaned on B
for the split flange coaster's middle piece.

## What bikar and our tools would need

Nothing here exists yet (R10).

- **bikar:** a bearing pocket that makes two pieces in one file, the body with its lips and wall and
  the hub with its disc, post and cap, from the bearing's three sizes and the clearances. The build
  should also print the pause height (here, layer 25 at 5.00 mm) so the plate page can state it.
- **Our tools:** a way to put a pause in a slice from the command line (S4 or S5), and V1 as a check
  after every slice that is meant to hold one.

## Numbers no source backs yet

| Number | Where | What settles it |
|---|---|---|
| 0.8 mm of cap over each ring | hub cap, body lips | the bearing in hand, measured |
| hub set one layer (0.2 mm) below the body | table face | coupon 2: does the hub rub |
| 0.95 mm reach of the first layer over air | caps at layer 25 | coupon 1 |
| a 32 mm square tile | coupons | none needed: wall over CAL-FEA-01's 1.2 mm on every side |

## Open questions for Omar

1. **What should spin: the centre (recommended) or the rim?** The centre keeps the coaster flat on the
   table; a spinning rim stands on a 21 mm centre and tips under an off-centre mug.
2. **Is a 5.6 mm coaster all right?** Today's are 4 to 4.4 mm. The 4 mm bearing cannot fit in less.
3. **Which coaster?** The pocket needs a plain round middle about 30 mm across (the bearing's 27 mm
   plus the wall). Patterns with a star or kites in the middle would lose them there, as the earlier
   study found for the 6704 (R6).
4. **Bearings to buy:** a few 6704s for coupon 2, and, if a maker's page confirms its size, a 6705
   for a bigger hub. Nothing is bought until Omar says.
5. **Rust and the look.** The bearing shows as a steel ring, 1.9 mm wide, on both faces. Chrome
   steel may rust in a wet coaster; no source here says. Is a stainless bearing worth looking for?
6. **Pause or split (A or B above)?** A is one solid print with a person at the printer each time; B
   needs no pause but has a seam.
