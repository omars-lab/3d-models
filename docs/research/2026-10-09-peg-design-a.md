---
date: 2026-10-09
produced-by: research subagent A (Claude Opus 5.5), web search and page fetches, independent of researcher B
feeds: docs/design/pieces/peg-design-a.md
---

# Research A: how printed pegs and sockets join two printed halves

**The question.** How should a printed stud and its socket be shaped so two printed halves of a
coaster close by hand, flush, and stay closed? On spl-1 every pair from −0.10 to 0.15 mm needed a
hammer. spl-2 is printing 0.15 to 0.40 mm now, and its result is not known as this is written.

**Our setup, for every "does this transfer" line below.** Bambu X2D, 0.4 mm hardened-steel nozzle,
PLA, 0.20 mm layers, outer wall line about 0.42 mm, inner wall 0.45 mm, first layer 0.5 mm. Two
wall loops. Seam aligned. Bambu Studio's circle compensation, XY hole compensation and XY contour
compensation are all off; elephant-foot compensation is 0.15 mm. Our stud is round, 2.0 mm across,
1.4 mm tall, with a one-layer 45° chamfer on its top only. The socket is 1.6 mm deep on a 0.6 mm
floor, with a 0.9 mm wall around it and no chamfer at its mouth. Both halves print outer face down,
so the stud stands up off the lower half's cut face (built along Z) and the socket opens upward in
the upper half. The gap is **diametral**: socket diameter less stud diameter.

**How to read this file.** Sources are S1, S2 and so on. Each says FETCHED (I read the page in this
run) or SNIPPET (I saw only a search-result excerpt, or the fetch failed), and what kind of source it
is. Quotes are verbatim and short, in the source's own spelling. For every number I say whether it
is per side or diametral and what printer, nozzle, material and layer it came from, or "not
stated". The repo's earlier research is cited, not repeated: R1 to R6 at the end.

**Counts.** 36 sources: 17 FETCHED, 19 SNIPPET (two of the SNIPPETs, S19 and S20, are quoted
through this repo's own earlier survey, which fetched them; I could not reach them in this run).

---

## 1. Fit types, and which one a coaster half wants

The sources use five words for how tight a joint is. Their numbers do not agree, and most do not
say whether a gap is per side or across the diameter. rigcad (S5) puts the warning plainly: "a
clearance applied to a radius is half the clearance applied to a diameter."

| Fit | What it feels like | Diametral gap, as each source gives it |
|---|---|---|
| Free / running | turns with play | rigcad 0.5–0.8 (S5) |
| Sliding / slip | moves smoothly, little slop | rigcad 0.3–0.5 (S5); val.town "slide" 0.30 (S4); AON3D "1–2× your extrusion width", per side or diametral not stated (S6) |
| Close / locating | "Assembles by hand, no movement in use" | rigcad 0.2–0.3, typical use "Alignment pins" (S5); val.town "loose" 0.20, "tight" 0.10 (S4) |
| Transition | sometimes a little play, sometimes a little force | AON3D: "the tightest dimensional tolerance achievable with FDM" (S6), no number |
| Press / interference | needs force | rigcad 0.0 to −0.1 (S5); val.town 0.00 "Hammer/clamp to seat" (S4); R1's Creative3DP ladder −0.10 |
| Snap | goes in with a click, held by an undercut | §5 below |

**What a coaster half wants.** The studs only line the halves up and hold them lightly; the lips
(R4) and the pieces carry the rest. That is rigcad's "close / locating" row: in by hand, no movement
in use. It is not a press fit (it needs a hammer, which is what spl-1 got) and not a slip fit (the
halves would fall apart when turned over). A light snap is the one other fit that would also do the
job, if it can be printed at this size (§5 says probably not at 2 mm).

**Does rigcad's 0.2–0.3 transfer to our 2 mm stud?** Only partly. rigcad says its table suits
"features in the 3 to 20 mm range" at a 0.4 mm nozzle, and that "Small holes suffer far more than
large ones". Our 2 mm stud is below that range, so the gap we need is likely at or above the top of
its 0.2–0.3 band, not inside it. This matches spl-1, where 0.15 still needed a hammer.

## 2. Why round holes print small and pegs print big

Four causes recur. Each source names its own subset; none of the sources here names all four.

1. **The straight segments of a polygon cut inside the circle.** Nop Head (S1): a hole drawn as an
   n-sided polygon shrinks "by cos(π / n)". At our 48 sides that is a 0.2% loss, about 0.004 mm on
   2 mm, so it is not our problem; it matters only for coarse polygons.
2. **Plastic piles up on the inside of a tight curve, and the nozzle cuts corners.** Nop Head (S1):
   "too much plastic on the inside of the curve", and the head "likes to take a short-cut". rigcad
   (S5): "Corners overshoot … Small holes suffer far more than large ones — proportionally, a 3 mm
   hole loses much more of its diameter than a 30 mm one." This is the cause that grows as the hole
   shrinks, and our 2 mm socket is small.
3. **The first layer spreads.** rigcad (S5): "A peg is widest at its base, a hole is tightest there,
   and if the mating surface is near the plate that is the dimension that governs." Bambu (S3) lists
   "Elephant's foot" among the causes. *Transfer:* neither our stud root nor our socket mouth is on
   the bed (both are on cut faces printed last), so elephant foot does not reach the joint
   directly. It can still keep a half from sitting flat if the half's bottom edge flares.
4. **The seam.** Bambu (S3) lists "Seam, this feature can affect hole precision". AON3D (S6):
   "Z-seams can be hidden within a corner of the shaft" on a hexagon. Our preset puts the seam
   "aligned", so on a 2 mm stud every layer's start-and-stop bump sits on one line up its side.

**The two errors add.** rigcad (S5): "Printed holes come out undersized and printed pegs come out
oversized, and those two errors add rather than cancel." Bambu's own worked example (S3) measured
an M6 test hole at 5.66 mm, "0.24 mm undersized", on its own printer and filament (printer, nozzle
and layer not stated). R5 (the sheets-04g fit check) found our sliced walls sit on the drawn line at
mid-height, so on our setup the shrink comes from the printed plastic, not from the slicer's path.

**What the slicer can do about it.**

- **XY hole compensation** (S3): "The hole diameter will increase by twice the compensation value"
  (the setting is per side). It "only applies to closed paths". Off in our preset.
- **Auto circle holes-contour compensation** (S2): Bambu's newer setting, "only for complete circles
  on the horizontal plane", diameters "within 50mm". It slows circles and sets maximum cooling, uses
  a scarf seam on them, and carries built-in values for some official filaments. Its user offset
  moves in "a step value of 0.02mm", where "positive values make the assembly looser". It warns that
  "dry filament results in a looser fit, and moist filament results in a tighter fit". Off in our
  preset. *Transfer:* this is Bambu's own feature for Bambu printers, and the X2D runs Bambu Studio,
  so the mechanism transfers. Whether its built-in value suits a 2 mm circle is not stated; S2 gives
  no lower size limit, and S3 warns "holes below 1 mm can be challenging to tune".
- **Polyholes** (S1): draw the hole with few sides and a larger radius,
  `n = max(round(2*d),3); r=(d/2)/cos(180/n)`. Measured by Nop Head on a 0.5 mm nozzle (Mendel), PLA
  and layer not stated. *Transfer:* the polygon-correction half transfers to any printer. The
  side-count rule was tuned to a 2011 printer, so it does not transfer as a number. A 2 mm polyhole
  would have 4 sides by that rule, which is a square, not a hole we would draw.

## 3. Lead-ins: chamfers on the stud and in the socket mouth

- rigcad (S5): "A 45 degree chamfer on the mouth of a hole and the end of a pin turns an
  interference into a guided entry. This single change rescues more marginal fits than any
  clearance adjustment." No number for size. This is a rule of thumb, not a measurement.
- Bambu (S3) lists "Lack of chamfers or lead-in features on holes" as a cause of fits that need
  force.
- **Ours.** The stud has a one-layer (0.2 mm) 45° chamfer on its top. The socket mouth has none:
  the split design (R4, §4.1) rejected it because "a chamfer there would open a gap visible from the
  side". *Reading that against the geometry:* the mouth is on the cut face, inside the closed pair.
  A 0.2–0.3 mm mouth chamfer cuts into a 0.9 mm socket wall and stops 0.6 mm or more short of the
  side, so it would show from the side only where a socket sits within the chamfer's width of an
  edge. The objection holds for a socket that close to an edge; it does not hold for a socket in the
  middle of a strap. On the spl-2 tile the socket is in the middle of a 15 mm tile.
- **The stud's root.** No source here measured a fillet or relief at the root of a small printed
  stud for fit. Hubs (via R1) and S12 recommend a fillet at a pin's or arm's base for strength. A
  small groove at the root, the opposite of a fillet, is the machinist's trick for letting a pin
  seat flush past a burr. I found no FDM source testing it, so it would be our own experiment.

## 4. Shapes that give way: hexagon holes, crush ribs, slots, D-flats

**Hexagon and square holes.** AON3D (S6): "circular holes can only expand by stretching along their
circumference, which often leads to material cracking or delamination"; "square or hexagonal
geometries reduce the amount of stretching needed". A round stud in a hexagon socket touches at six
lines, each on a flat that can bend, and the gaps in the six corners take the seam and any excess
plastic. No number for the hexagon's size is given. *Transfer:* the idea is geometry and does not
depend on the printer. The flat-to-flat size has to be found on our printer.

**Crush ribs.** Small ridges, on the peg or in the bore, that deform on assembly.

- Hackaday on Dan Royer (S7): ribs are "very small standoffs that deform as a part is press-fit",
  and "a 0.1 mm difference can have a noticeable effect"; it calls them "a bit of a hack since their
  original purpose in injection molding is somewhat different". Printer, nozzle and material not
  stated.
- New Screwdriver (S8): "easier for a bearing to crush small ribs than to reshape the entire
  cylinder". The costs: "load is transmitted only through these small contact patches", and the
  part's "center … will end up in an unpredictable location".
- AON3D (S6): transition-fit ribs, "Slope the inner or outer diameter by ~2° … and add 0.2 mm
  vertical crush ribs"; press-fit ribs (no slope) "should only be used for one-time assembly".
  Whether 0.2 mm is the rib's height or width is not stated, nor printer or material.
- Printables test prints by one maker (S9, SNIPPET, the pages refused my fetcher): four 0.3 mm ribs
  on a 15 mm cylinder at a 2°, 1° and ½° taper, 1° described as a "good firm fit"; undrafted ribs
  much tighter; the mechanism described as the "walls bending inward". Printer and material not
  seen.
- Lemmy thread (S23, SNIPPET, anecdote): 0.2–0.3 mm of rib interference.
- This repo's Lego Lab (R3, §7.6) already designs ribs: a lobe of `ribMm` (0.10 mm) over an arc of
  `ribArcMm` (0.8 mm), with the rule that a rib narrower than "2 × nozzle" is "absorbed into the
  perimeter path and does not exist in the printed part".

*Transfer.* The rib idea transfers: the rib is the only part that has to give, so the force comes
from a small known volume of plastic. The sizes do not transfer as numbers: S7 to S9 are on larger
pegs (8 to 15 mm) and other printers. On a 2 mm stud a rib 0.8 mm wide (R3's floor) takes up more
than an eighth of the circumference, so at most three or four fit. A rib 0.05 mm tall is under a
quarter of a line width and may print as nothing; R3's floor is about width, and a height floor is
not stated in any source here.

**Slots and split pegs.** AON3D (S6): "add thin radial cuts or split sections … so the walls can flex
during assembly", for "a secure hold with moderate force while allowing reassembly without permanent
deformation". It also describes "grip fins" that "maintain clamping force over multiple assembly
cycles". No sizes given. *Transfer:* a slot in a 2 mm stud leaves two half-studs about 0.8 mm thick
each after a 0.4 mm slot; that is two lines wide and stands 1.4 mm tall, built along Z. It will
bend, and it is in the weak direction (§7), so the open question is whether it breaks before it
bends.

**D-flats.** BOSL2's snap pin (S13) has "flat sides so they can be printed", printed "flat side
down". That is a flat for printing a pin lying down, not a fit trick. None of the sources here
tests a D-flat as a way to loosen a round stud in a round socket.

**Teardrop holes.** For holes that run sideways (horizontal), not ours: BOSL2's `teardrop()` (R1
S36). Our sockets are vertical, so it does not apply.

## 5. Snap fits

**The two kinds.** Hubs (S12): cantilever (a bending arm with a hook) and annular ("hoop strain to
retain a press-fit part", like a pen cap). Ball-and-socket is an annular snap on a sphere.

**How much a printed PLA arm may bend.** The sources disagree, by a factor of four.

| Source | PLA strain allowed | Conditions |
|---|---|---|
| Fictiv (S10) | "4-8%" | For snap arms, printed; printer not stated. For an arm built along Z: "elongation at break is reduced by 50%", and it recommends "reducing the allowable stress/strain by 50% for Z-axis cantilevers" |
| Covestro (S11) | no PLA value; for a one-time snap "partially crystalline materials may be stressed almost to the yield point, amorphous ones up to about 70% of the yield strain"; for repeated use "about 60% of these values" | Molded parts. Table 2 gives PC 4%, PC/ABS 2.5% |
| Bambu PLA Basic data sheet (S14) | elongation at break XY 12.2 ± 1.8%, Z 7.5 ± 1.3%; no yield strain | Bambu's own printed test bars, annealed; "for design reference and comparison only" |
| Seas3D PLA data sheet (S33, SNIPPET) | yield 2%, break 4% | A generic PLA, ASTM D638 Type V |
| Machine Design (S32, SNIPPET) | annular snap at 50% of strain at break | Molded parts |

Hubs (S12) adds: "brittle grades like PLA and standard SLA resins are less suitable", and for FDM
snap fits "0.5mm" of clearance (per side or diametral not stated), a root fillet "at least 0.5
times the cantilever base thickness", a width of at least 5 mm, and "avoid snap-fit cantilevers
built vertically in the Z direction".

**Formulas.** Fictiv (S10) and Covestro (S11) give the same beam formula for a straight cantilever,
strain = 1.5 · thickness · deflection / length². Covestro: tapering the arm to half its thickness at
the tip "increases the permissible deflection by more than 60%". Fictiv gives the push-in force
W = P(μ + tan α)/(1 − μ tan α); "a return angle of 90° can never be disassembled". Covestro's worked
example uses a 30° lead angle.

**Annular snaps.** Covestro (S11): the undercut a ring can take is about strain × diameter, and
"With components of equal flexibility, the strain is halved, i.e., the undercut can be twice as
large."

*Transfer to a 2 mm printed stud, worked through.* At 4% strain (the low end of Fictiv, and Seas3D's
break), the undercut on a 2 mm ring is 0.04 × 2 = 0.08 mm; at 8% it is 0.16 mm. Halved again for
a Z-built part, 0.04–0.08 mm. Every one of those is under half a 0.42 mm line, and a 0.20 mm layer
cannot place a bead that small reliably. **So a printed annular snap on a 2 mm stud is not
something our printer can make reliably, at any strain in the table.** A cantilever needs length:
at Covestro's formula, a 0.4 mm thick arm 1.4 mm long bending 0.1 mm takes 1.5 × 0.4 × 0.1 / 1.96
≈ 3% strain, which is at the edge of the table's range before the Z-axis halving. Our studs are
1.4 mm tall, so an arm is that short.

**BOSL2's snap pin (S13), the one printed snap with numbers.** Based on Emmett's Thingiverse pin
(thing:213310). It prints lying flat, so its arms bend in the strong direction. Its smallest preset,
"tiny", is 4 mm long and 2.5 mm across, with a 0.25 mm snap, 0.8 mm walls, 0.10 preload; the
default clearance is 0.2 ("how far to shrink the pin away from the socket walls", so per side by its
wording). "To make pins tighter increase preload and/or decrease clearance". Its rabbit clip
examples "work printed in PLA on a Prusa MK3, with default clearance of 0.1 and a depth of 5"
(nozzle and layer not stated). *Transfer:* the tiny pin is a separate part printed lying down, 4 mm
long, so it needs a socket 2 mm or more deep in each half. Our halves have a 1.6 mm socket, so it
does not fit our present tile without deeper sockets.

## 6. How LEGO gets its fit (clutch)

R2 (the LEGO survey) and R3 (Lego Lab) already hold the numbers; this section says only what they
mean for us.

**Where the contact is.** On a LEGO brick a stud touches a tube and the outer wall, not a round
socket. The tube sits where four studs meet, so each stud touches the tube along one line and the
wall along one or two lines. The tube's outside is 6.514 mm by tangency to four 4.8 mm studs on an
8 mm pitch (R2 §2, derived, not measured). The tube wall is 0.857 mm by that geometry; the outer wall
is 1.5 mm in the usual reading (R2 §4).

**How much interference.** thewave.engineer (S19, quoted by R2, which fetched it; refused to my
fetcher in this run) puts stud-to-tube interference at "roughly 0.1–0.2 mm", a 10 µm mold tolerance
and ±0.01 mm on the stud. The Brighton Toy Museum micrometer survey (S20, quoted by R2 via the
Wayback Machine; rate-limited in this run) measured studs at 4.88–4.89 mm, "deliberately oversized
… to force the mating brick's walls to flex". LEGO's own designers call it "an interference fit"
(BrickNerd, via R2). Molded parts carry about 0.5° of draft (hardwareishard, via R2), so a
"tangent" fit holds at one height only. R2's own audit retracted its earlier "0.02 mm clutch band"
as unsourced and dropped one site's (Pixenib's) tube number as not a LEGO dimension.

**Why it works in molded ABS.** The contact is a line, not a full circle, and the thing that gives
way is a thin wall that bends, not a ring that has to stretch. MachineBlocks (S16): "Original LEGO®
bricks are cast from relatively soft ABS plastic to an accuracy of a tenth of a millimeter. 3D
printed bricks, on the other hand, are generally harder". (Note that MachineBlocks says a tenth of a
millimeter where S19 says 10 µm; they disagree by ten times.)

**What happens with printed bricks.**

- Brickset (S17) printed the same 2×4 brick on a 0.2 mm nozzle at 0.1 mm layers and a 0.4 mm nozzle
  at 0.2 mm layers: clutch "is nowhere near as good as that of real bricks … slightly better on the
  red bricks", the 0.4 mm ones. A commenter put the red bricks' grip down to "a lot of first layer
  elephant foot" (anecdote).
- Brick Architect (S18), on an Elegoo Neptune 3 Pro in PLA, nozzle not stated: "even when on the best
  settings the 3D printed parts fail to reach the clutch power of LEGO bricks"; a real brick sat on
  the printed one, but not the reverse, "as the walls were to thick and the tubes were not perfectly
  aligned".
- MachineBlocks (S16) tunes four separate knobs: `studDiaAdj`, `wallThickAdj`, `tubeZDiaAdj`,
  `pinDiaAdj`, each an "Amount in mm added to the diameter" (or to the wall's thickness). Its
  method is a printed ladder: "Start with the smallest setting in each row … until the brick fits
  snugly", and "Do not force original LEGO® bricks onto the calibration tool".

**What transfers to a coaster stud (K10).** The idea transfers: touch at a few lines, and put the
give in a thin wall or a rib that can bend, not in a full ring that must stretch. That holds in any
material that bends before it cracks, which PLA does at small strain (§5). The interference number
does not transfer. LEGO's 0.1–0.2 mm is set by a mold that holds 0.01 mm in soft ABS; our printer
puts more error than that into every printed circle (§2), and PLA is stiffer than ABS (S16). Our
0.9 mm socket wall is solid plastic around a 2 mm hole in a 15 mm tile, so it cannot bend the way a
LEGO wall spanning 8 mm does. A LEGO-style joint for us means making something thin on purpose:
ribs on the stud (R3 §7.6), or a socket made of a few thin fingers.

## 7. Integral studs against separate dowels, and print direction

- Hubs (S15): "Tensile strength in the XY plane is typically 4 to 5 times higher than in the Z
  direction", and "For parts like pins or bolts, a horizontal orientation ensures the shear force has
  to cut across thousands of solid plastic strands". The Bambu PLA data sheet (S14) gives a much
  smaller gap for its own PLA: tensile strength XY 35 ± 4 MPa against Z 31 ± 3 MPa, but elongation
  at break 12.2% against 7.5%. *These disagree.* S14 is Bambu's annealed test bars; S15 is a
  general rule across FDM. The safe reading is that a Z-built stud breaks at a lower bend.
- CNC Kitchen (S29, SNIPPET): 63 MPa flat against 31 MPa upright in its own test, which was not a
  pin test.
- Our studs are built along Z on the lower half's cut face (R4 §4.1). A separate dowel printed lying
  down puts its layers along its length, so a sideways push crosses every line. It costs a part to
  print, count and seat, and both halves then need a socket. R4 §4.2 kept loose dowels "for the
  general case".
- UT Austin course wiki (S25, SNIPPET): a 5.2 mm hole for a 5 mm dowel, diametral 0.2, printer not
  seen.

## 8. Stud height against diameter

None of the sources here gives a height-to-diameter rule for a printed locating peg. What they do
say: val.town (S4): "Taller plugs create more friction" (A1 Mini, PLA, 70 mm rings), and walls under
about 1 mm flex. Hubs (via R1) says pins under 5 mm across are weak. Our stud is 1.4 mm tall on a
2 mm diameter, so the engaged length is 0.7 diameters; that is short, which keeps friction low but
gives little lead before the faces meet.

## 9. How many studs, and where

- Machine design practice (S27, S28, SNIPPET): one round pin "locates … X and Y", a diamond pin "stops
  rotation but has relief", and a second full round pin "would fight for constraint". This is from
  machined fixtures, steel on steel. *Transfer:* the geometry argument (more round pins than needed
  over-constrain the part, so any spacing error has to be forced out) holds in any material. The
  steel tolerances do not.
- R4 plans many studs per coaster at 25 mm spacing. With every stud a tight round fit, any spacing
  error between the two halves (from shrink or bow) has to be forced out at every stud at once. A
  single-stud tile like spl-2 cannot show this.
- Printpal's splitter (S26, SNIPPET): tapered pegs of 2–5° "self-center and tolerate slight
  first-layer squish", clearance 0.15–0.3 (per side or diametral not seen).

## 10. Tapered pegs

S26 (SNIPPET) above, and S9's drafted ribs (SNIPPET). AON3D (S6) slopes a rib-carrying bore by "~2°".
A taper means the stud is loose for most of its travel and only touches near the end. *Transfer:* a
2° taper on a 1.4 mm stud changes its radius by 1.4 × tan 2° ≈ 0.05 mm, a quarter of one layer's
height and an eighth of a line width. The slicer would print that as a step or two at most; whether
the printer resolves it at all is unknown, so a taper here would need to be steeper (5° ≈ 0.12 mm
per side) to be a real shape.

## 11. Test coupons

- rigcad (S5): holes "stepping the clearance from 0.1 mm to 0.8 mm in 0.1 mm increments. Label each
  one in the model", and "Print it in the orientation and profile the real part will use".
- MakerWorld 2820462 (S21, SNIPPET): press 0.00, removable 0.10–0.20, sliding 0.20 and up; "smaller
  features shrink proportionally more".
- MachineBlocks (S16): a ladder per knob, tried from the smallest up.
- Bambu (S3): print a hole ladder, test with a screw, set half the measured shortfall as hole
  compensation.
- spl-1 and spl-2 are already this kind of coupon (R6).

## 12. Where the sources disagree

1. **Close-fit gap.** rigcad 0.2–0.3 (S5, diametral, 3–20 mm features), val.town 0.10–0.20 for tight
   to loose (S4, diametral, 70 mm rings), Creative3DP 0.05–0.15 (R1, diametral), Fictiv 0.2–0.4 for
   snap joints (S10, not stated), Hubs 0.5 for snaps (S12, not stated). The spread follows size: the
   bigger the part tested, the smaller the gap. Our 2 mm stud is smaller than all of them.
2. **PLA snap strain.** 2% to 8% (§5 table).
3. **Z-direction penalty.** Hubs 4–5× (S15), Bambu data sheet about 1.1× in strength but 1.6× in
   elongation (S14), CNC Kitchen about 2× (S29).
4. **LEGO mold accuracy.** 10 µm (S19 via R2) against "a tenth of a millimeter" (S16).

## 13. What I looked for and did not find

- Fusion and Onshape: I found no published fit tables of their own in this run; I did not fetch any
  page from either. Formlabs and Xometry snap-fit pages turned up in search; I did not read them.
- Prusa: covered in R1 (S24, S25, S33 there); not re-fetched.
- None of the 36 sources here measures a printed locating stud as small as 2 mm. The smallest
  measured parts are BOSL2's 2.5 mm snap pin (S13, a pin printed lying down) and Nop Head's small
  holes (S1).
- None of them tests a socket-mouth chamfer, a stud-root groove or a hexagon socket at our size with
  numbers. These are the gaps a coupon fills.

---

## Sources

### S1. Nop Head, "Polyholes" (HydraRaptor blog, 2011)
https://hydraraptor.blogspot.com/2011/02/polyholes.html. FETCHED. Kind: maker's blog, measured.
- "shrinking it by cos(π / n)"; "too much plastic on the inside of the curve"; "likes to take a
  short-cut".
- Formula `n = max(round(2*d),3); r=(d/2)/cos(180/n)`: d is the hole diameter. Mendel, 0.5 mm
  nozzle; layer and material not stated.

### S2. Bambu Lab Wiki, "Auto Circle Holes-contour Compensation"
https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation.
FETCHED. Kind: vendor manual.
- "only for complete circles on the horizontal plane"; "diameter size within 50mm".
- "dry filament results in a looser fit, and moist filament results in a tighter fit".
- "positive values make the assembly looser", "a step value of 0.02mm". Whether the offset is per
  side or diametral is not stated.

### S3. Bambu Lab Wiki, "XY Hole / Contour compensation"
https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation. FETCHED. Kind:
vendor manual.
- Causes: "Elephant's foot", "Moist filament", "holes below 1 mm can be challenging to tune", "Lack
  of chamfers or lead-in features on holes", "Seam, this feature can affect hole precision".
- "0.24 mm undersized" (M6 hole measured 5.66, diametral). "The hole diameter will increase by
  twice the compensation value" (setting per side). "only applies to closed paths". Printer, nozzle
  and layer of the example not stated.

### S4. val.town, "PRESS-FIT-NOTES"
https://www.val.town/embed/x/dcm31/stl-creator/PRESS-FIT-NOTES.md. FETCHED. Kind: one maker's
notes, measured.
- Diametral: slide 0.30, loose 0.20, tight 0.10, semipermanent 0.00 "Hammer/clamp to seat".
- "Taller plugs create more friction". Bambu A1 Mini, PLA, fuzzy skin, 70 mm rings; nozzle and
  layer not stated.

### S5. rigcad, "Clearances for 3D-Printed Parts That Have to Move"
https://rigcad.com/articles/p12/clearances-for-3d-printed-moving-parts. FETCHED. Kind: engineering
blog, a guide, not a measurement.
- "those two errors add rather than cancel"; "Small holes suffer far more than large ones"; "A peg is
  widest at its base, a hole is tightest there".
- Diametral table "for FDM at a 0.4 mm nozzle": free 0.5–0.8, sliding 0.3–0.5, close/locating
  0.2–0.3 ("Alignment pins"), press 0.0 to −0.1. "features in the 3 to 20 mm range". Material and
  layer not stated; "Material changes the answer".
- "Chamfer every lead-in."

### S6. AON3D, "Engineering Fits: How to Design for 3D Printed Assemblies"
https://www.aon3d.com/applications/engineering-fits-how-to-design-for-3d-printed-assemblies/.
FETCHED. Kind: printer-maker's application note.
- "a clearance of 1–2× your extrusion width" (per side or diametral not stated; its example is a
  0.6 mm nozzle, 0.75 mm width).
- "the tightest dimensional tolerance achievable with FDM"; "circular holes can only expand by
  stretching along their circumference"; "square or hexagonal geometries reduce the amount of
  stretching needed"; "Z-seams can be hidden within a corner".
- Ribs: "~2°" slope plus "0.2 mm vertical crush ribs"; press ribs "only … for one-time assembly".
  Relief cuts: "reassembly without permanent deformation". Grip fins: "multiple assembly cycles".

### S7. Hackaday, "Adding Crush Ribs To 3D Printed Parts For A Better Press Fit" (2020-10-15)
https://hackaday.com/2020/10/15/adding-crush-ribs-to-3d-printed-parts-for-a-better-press-fit/.
FETCHED (read through https://hackaday.com/tag/press-fit). Kind: news write-up of Dan Royer's video.
- "very small standoffs that deform as a part is press-fit"; "a 0.1 mm difference can have a
  noticeable effect" (what the 0.1 is measured on is not stated); "a bit of a hack".

### S8. New Screwdriver (Roger Cheng), "Accommodate 3D Printer Variation With Crush Ribs"
https://newscrewdriver.com/2020/12/31/accommodate-3d-printer-variation-with-crush-ribs/. FETCHED.
Kind: maker's blog.
- "easier for a bearing to crush small ribs than to reshape the entire cylinder"; "load is
  transmitted only through these small contact patches".

### S9. Printables, crush-rib test prints, versions 01 to 04
https://www.printables.com/model/43586-test-print-crush-ribs-version-01,
https://www.printables.com/model/43599-test-print-crush-ribs-version02,
https://www.printables.com/model/43628?lang=en,
https://www.printables.com/model/43636-test-print-crush-ribs-version04. SNIPPET (403 to my
fetcher). Kind: user test models.
- Four 0.3 mm ribs on a 15 mm cylinder; 2°, 1° ("good firm fit"), ½° drafts; "walls bending
  inward". Rib height or width and printer not seen.

### S10. Fictiv, "How to Design Snap Fit Components"
https://www.fictiv.com/articles/how-to-design-snap-fit-components. FETCHED. Kind: manufacturing
service's guide.
- PLA "4-8%" strain; "elongation at break is reduced by 50%" along Z; "reducing the allowable
  stress/strain by 50% for Z-axis cantilevers"; "Print snap arms parallel to the build plane".
- "a return angle of 90° can never be disassembled".
- "0.3 mm for close-fit snap joints, 0.2 mm for tight fits, 0.4 mm for slide fits" (per side or
  diametral not stated; printer not stated).

### S11. Covestro (formerly Bayer), "Snap-Fit Joints for Plastics – A Design Guide"
https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1556891135.pdf.
FETCHED (PDF). Kind: resin maker's design guide, for molded parts.
- "partially crystalline materials may be stressed almost to the yield point, amorphous ones up to
  about 70% of the yield strain"; "for frequent separation and rejoining, use about 60% of these
  values"; a tapered arm "increases the permissible deflection by more than 60%"; annular "the
  strain is halved, i.e., the undercut can be twice as large". Table 2: PC 4%, PC/ABS 2.5%.

### S12. Hubs (Protolabs Network), "How to design snap-fit joints for 3D printing"
https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/. FETCHED. Kind:
manufacturing service's guide.
- FDM clearance "0.5mm" (per side or diametral not stated); fillet "at least 0.5 times the
  cantilever base thickness"; "a minimum width of 5 mm"; "avoid snap-fit cantilevers built vertically
  in the Z direction"; "brittle grades like PLA … are less suitable".

### S13. BOSL2, `joiners.scad` wiki
https://github.com/BelfrySCAD/BOSL2/wiki/joiners.scad. FETCHED. Kind: open-source CAD library docs.
- snap_pin: "flat sides so they can be printed"; "flat side down on the xy plane"; "To make pins
  tighter increase preload and/or decrease clearance"; clearance "Default: 0.2", preload "Default:
  0.2". Presets (length / diameter / snap / nub depth / wall / preload): tiny 4 / 2.5 / 0.25 / 0.9 /
  0.8 / 0.10; small 6 / 3.2 / 0.40 / 1.2 / 1.0 / 0.16. From Thingiverse thing:213310.
- rabbit_clip: "work printed in PLA on a Prusa MK3, with default clearance of 0.1 and a depth of 5".

### S14. Bambu Lab, "Bambu PLA Basic Technical Data Sheet" V3.0
https://wiki.bambulab.com/filament-acc/abs-asa-pc/bambu_pla_basic_technical_data_sheet.pdf. FETCHED
(PDF). Kind: vendor data sheet.
- Young's modulus XY 2580 ± 220, Z 2060 ± 170 MPa; tensile strength XY 35 ± 4, Z 31 ± 3 MPa;
  elongation at break XY 12.2 ± 1.8%, Z 7.5 ± 1.3%. Annealed printed bars. "for design reference and
  comparison only". No yield strain.

### S15. Hubs (Protolabs Network), "How does part orientation affect a 3D print?"
https://www.hubs.com/knowledge-base/how-does-part-orientation-affect-3d-print/. FETCHED. Kind:
manufacturing service's guide.
- "Tensile strength in the XY plane is typically 4 to 5 times higher than in the Z direction"; "a
  horizontal orientation ensures the shear force has to cut across thousands of solid plastic
  strands".

### S16. MachineBlocks, "Calibration"
https://machineblocks.com/docs/calibration. FETCHED. Kind: open-source LEGO-compatible generator's
docs.
- "cast from relatively soft ABS plastic to an accuracy of a tenth of a millimeter"; "3D printed
  bricks, on the other hand, are generally harder"; four knobs, "Amount in mm added to the
  diameter"; "Start with the smallest setting in each row"; "Do not force original LEGO® bricks onto
  the calibration tool".

### S17. Brickset, "Can you make compatible bricks with consumer 3D printers?"
https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers.
FETCHED. Kind: hobby site's test, one person.
- 0.2 mm nozzle / 0.1 mm layers against 0.4 mm / 0.2 mm; clutch "nowhere near as good as that of real
  bricks … slightly better on the red bricks". A commenter: "a lot of first layer elephant foot".

### S18. Brick Architect, "Enhancing your LEGO hobby with 3D printing" (2023)
https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/. FETCHED. Kind:
hobby site's test, one person.
- "precision of 10 micrometers or better" for molded bricks; "fail to reach the clutch power";
  "tubes … are a lot deeper"; "bars are the most suitable pieces for 3D printing". Elegoo Neptune 3
  Pro, PLA; nozzle and layer not stated.

### S19. thewave.engineer, "LEGO tolerances"
https://thewave.engineer/lego-tolerances/. SNIPPET in this run (403 to both my fetchers); FETCHED
and quoted by R2. Kind: engineering blog.
- Interference "roughly 0.1–0.2 mm"; 10 µm mold tolerance; ±0.01 mm on the stud (all via R2).

### S20. Brighton Toy Museum, LEGO dimensions (micrometer survey)
http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions.
SNIPPET in this run (the Wayback Machine rate-limited me); FETCHED and quoted by R2. Kind: museum's
measurements.
- Studs 4.88–4.89 mm, "deliberately oversized … to force the mating brick's walls to flex" (via R2).

### S21. MakerWorld 2820462, "Tolerance Fit Test"
https://makerworld.com/en/models/2820462-tolerance-fit-test. SNIPPET. Kind: user test model.
- Press 0.00, removable 0.10–0.20, sliding 0.20 and up; "smaller features shrink proportionally
  more". Per side or diametral not seen.

### S22. Reddit thread on round holes printing small (Bambu H2C), via a mirror
https://reddit.sentinel-team.org/posts/1r93j6r/snapshots/2026-02-20T03%3A14%3A12.63357Z. SNIPPET.
Kind: forum anecdote.
- Round holes 0.3–0.4 mm undersize, polyholes about 0.1. Diametral by context; not measured by me.

### S23. Lemmy thread on crush ribs
https://lemmy.nekusoul.de/post/1629502/4632822. SNIPPET. Kind: forum anecdote.
- 0.2–0.3 mm interference on ribs.

### S24. zbotic, "3D Printing Tolerances: Designing Gaps for Press-Fits, Threads and Snap-Fits"
https://zbotic.in/3d-printing-tolerances-designing-gaps-for-press-fits-threads-and-snap-fits/.
SNIPPET. Kind: shop blog.
- 0.1–0.2 by hand, 0.2–0.4 with a mallet. Per side or diametral not seen.

### S25. UT Austin course wiki, "Manufacturing and Assembly"
https://cloud.wikis.utexas.edu/wiki/spaces/RMD/pages/51057176/IV.+Manufacturing+and+Assembly.
SNIPPET. Kind: university course notes.
- A 5.2 mm hole for a 5 mm dowel.

### S26. Printpal, 3D model splitter
https://printpal.io/tools/3d-model-splitter. SNIPPET. Kind: tool vendor page.
- Tapered pegs 2–5°, "self-center and tolerate slight first-layer squish"; clearance 0.15–0.3.

### S27. Mechanical Design Handbook, "Dowel pins and locating pins"
https://mechanical-design-handbook.blogspot.com/2009/08/dowel-pins-and-locating-pins.html, with
https://metrol-sensor.com/blog/2024/01/01/89881/. SNIPPET. Kind: machine-design blogs.
- "Round pin locates … X and Y"; "Diamond pin … stops rotation but has relief".

### S28. Eng-Tips, "Can anyone explain how diamond locating pins work"
https://www.eng-tips.com/threads/can-anyone-explain-how-diamond-locating-pins-work-like-a-pin-and-slot.489173/.
SNIPPET. Kind: engineers' forum.
- A second round pin "would fight for constraint".

### S29. CNC Kitchen, "Stop printing flat: the 45° secret for stronger parts"
https://www.cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts. SNIPPET. Kind:
maker's measured tests.
- 63 MPa flat, 31 MPa upright (its own test pieces, not pins).

### S30. PartForm, "Splitting oversized parts"
https://partform.eu/guides/splitting-oversized-parts. SNIPPET. Kind: service guide.
- 0.15–0.30 mm for alignment pins; per side or diametral not seen.

### S31. OpenFlexure issue 236
https://gitlab.com/openflexure/openflexure-microscope/-/issues/236. SNIPPET. Kind: project issue.
- Elephant foot spoiling alignment between printed parts.

### S32. Machine Design, "Fundamentals of annular snap-fit joints"
https://www.machinedesign.com/fastening-joining/article/21834620/fundamentals-of-annular-snap-fit-joints.
SNIPPET. Kind: trade magazine.
- Annular snap at 50% of strain at break.

### S33. Seas3D, PLA data sheet
https://www.seas3d.com/MaterialTDS-PLA.pdf. SNIPPET. Kind: filament data sheet.
- Elongation at yield 2%, at break 4% (ASTM D638 Type V).

### S34. Meshy, "Best Tolerances for 3D Printing LEGO-Compatible Bricks"
https://www.meshy.ai/blog/lego-compatible-3d-print-tolerances. SNIPPET here (R1 S19 has it). Kind:
vendor blog.
- Molding ±0.01 against FDM ±0.1–0.2; stud target 4.75–4.85.

### S35. Bambu Lab Wiki, "Seam", and OrcaSlicer wiki, seam settings
https://wiki.bambulab.com/en/software/bambu-studio/Seam,
https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_seam. SNIPPET. Kind: vendor and
open-source manuals.
- A scarf seam can apply to "Contour and hole"; a forum thread reports under-extrusion on small holes
  with it (https://forum.bambulab.com/t/help-scarf-joint-seam-under-extrusion/112311, SNIPPET).

### S36. Snap-fit blog posts: Sovol, Zdcpu, Amuse3d, Unionfab
https://www.sovol3d.com/blogs/news/3d-printed-snap-fit-joints-how-to-design-clips-that-work,
https://www.zdcpu.com/knowledge-hub/how-do-you-design-3d-print-snap-fit/,
https://www.amuse3d.in/blogs/3d-print-snap-fit-joints,
https://www.unionfab.com/blog/2025/06/3d-print-snap-fit. SNIPPET. Kind: shop blogs.
- Arm length to thickness 8:1 or more, root fillet at least half the thickness, gap 0.3–0.5.

### This repo's own earlier work, cited not repeated

- **R1.** [split-with-studs-research.md](split-with-studs-research.md): slicer cut tools, LEGO
  dimensions, the Creative3DP and BOSL2 fit ladders, Bambu hole compensation, elephant foot.
- **R2.** [lego-brick-system-survey.md](lego-brick-system-survey.md): LEGO geometry, the clutch, its
  audit's corrections, FDM reality at 0.4 mm. Also
  [lego-baseplate-seam-survey.md](lego-baseplate-seam-survey.md) and
  [pattern-outline-body-clutch-survey.md](pattern-outline-body-clutch-survey.md).
- **R3.** [lego-lab-design.md](../design/pieces/lego-lab-design.md): the clutch rib (§7.6) and the
  LG-F1 rib ladder (§8).
- **R4.** [split-with-studs-design.md](../design/pieces/split-with-studs-design.md): our stud and
  socket (§4.1), the joints already considered (§4.2).
- **R5.** [sheets-04g-fit.md](../issues/sheets-04g-fit.md): the sliced walls sit on the drawn line.
- **R6.** [spl-1](../design/plates/spl-1.md) and [spl-2](../design/plates/spl-2.md): the two split
  coupons.
