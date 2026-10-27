---
date: 2026-10-27
produced-by: researcher A subagent (Claude Opus 5.5), one of two independent passes — WebSearch, WebFetch, a read of this repo at origin/master 2566564b, a read of bikar's split flange coaster at origin/main, and one render of the middle piece with bikar-main at 951995a measured for its radii
feeds:
  - docs/design/coaster/spinner-middle-design.md
---

# Research A: what it would take to make the coaster's middle piece spin

**The question.** Could the middle piece of the split flange coaster (the 10-pointed star, orbit 0)
be printed so it turns in place, like a fidget spinner set into the coaster? What joint, what gap,
what bearing, and what would bikar have to build?

**Our setup, for every "does this transfer" line below.** Bambu Lab X2D, 0.4 mm nozzle, PLA,
0.2 mm layers. The coaster is 112.5 mm across and 4.4 mm tall, cut flat at 2.2 mm into a lower and
an upper half. Each loose piece is a 0.6 mm face block, a 3.0 mm band that steps out 0.8 mm under
the frame's lip (the flange), and a 0.6 mm face block. Pieces are **dropped in at assembly**, not
printed in place: the frame halves and the pieces are separate prints. split-06 ran a piece gap of
0.10 mm per face (the small kite 0.12) and `room` 0.2 (each piece 0.2 mm shorter than the coaster).

**How to read this file.** Sources are S1, S2 and so on. Each is marked **FETCHED** (I read the page
in this run) or **SNIPPET** (I saw only a search-result summary, or the fetch failed, with the
reason). Every MakerWorld, Printables, MyMiniFactory and 3dgo page returned 403 to the fetcher, so
every maker-site claim below is a SNIPPET. For each clearance I say per side or not stated, and the
printer, material and layer height, or "not stated". Repo facts are R1 to R6 at the end.

**Counts.** 26 sources: 6 FETCHED, 20 SNIPPET.

## 1. Our own geometry (measured, not researched)

**M1. The middle star's radii.** Rendered `--piece Middle` from bikar-main at 951995a (2026-10-06,
the checkout the Makefile defaults to; its flange coaster has no `room` or `halves` knobs, which do
not change the outline seen from above) at `gap 0.10`, and read the vertex radii from the piece's
centre at each height:

| Height | Tips (largest radius) | Notches (smallest radius) |
|---|---|---|
| Faces (0–0.6 mm and 3.8–4.4 mm) | 9.48 mm | 7.35 mm |
| Band (0.6–3.8 mm) | 10.84 mm | 7.35 mm |

So the star's tips sweep a circle about 19.0 mm across at the faces and 21.7 mm across at the band.
This agrees with the cut-pieces table (R1: face 18.0 × 19.0 mm, band 20.6 × 21.7 mm). The ring
between 7.35 and 9.48 mm is where the frame's lines reach in between the star's points; for
anything to turn, that frame material has to go (design doc §2).

**M2. How much frame there is round the middle opening.** Rendered `--piece Lower` from the same
checkout at `gap 0.10`, cut it flat at two heights, and walked out from the coaster's centre along a
ray every 3°, noting where the frame is solid. The star's tips point at 18° (and every 36° on);
its notches at 0°.

| Height | At a notch (0°) | 6° | At a tip (18°) |
|---|---|---|---|
| 0.3 mm, in the face block | solid 7.50 to 11.65 mm, then the small kite's hole | solid 7.70 to 12.70 | solid 9.65 to 16.05 (the strap running out from the tip) |
| 1.5 mm, in the undercut band | solid 8.30 to 10.70 mm, then the kite's undercut | solid 8.75 to 11.60 | solid 11.05 to 14.70 |

What this means: at the face, a round opening as big as the tips' circle (radius about 9.6 mm
with a gap) still leaves about 2 mm of frame before the small kites' holes. But one layer up, in the
undercut, the small kites' own undercuts come in to 10.70 mm at the notch angles. A round undercut
for a spinner flange of today's 0.8 mm would reach about 10.4 mm, leaving about 0.3 mm of wall,
under the 0.4 mm single line bikar takes as its least wall (`stud_wall`, R4) and well under the
0.9 mm two-line wall split-06 printed. Anything bigger, a bearing pocket of 23 or 27 mm across,
runs into the kites' undercuts and, past 11.65 mm, into the kites' holes. These are one render of
a 2026-10-06 checkout; bikar main has since added knobs (pins, slides, peg rings), which
are not expected to move these outlines but were not re-measured on main.

## 2. Clearances for parts that turn

**S1. Fab Academy 2025, Ísafjörður lab, group assignment week 5.** FETCHED.
<https://fabacademy.org/2025/labs/isafjordur/group_assignments/group_week05/>
Two print-in-place test files, rotating joints on a horizontal and a vertical axis, at 0.1/0.15/0.2
and 0.1/0.2/0.3 mm. Bambu Lab X1 Carbon, PLA, 0.4 mm nozzle, 0.2 mm layers: "Both the horizontal and
vertical joints were moveable at 0,15." Prusa MK4S table: PLA horizontal 0.15, vertical 0.2; PETG
the same. Per side or across is not stated. "Moveable" is not defined; it does not say free-spinning.
*Transfers to us as an upper bound*: same nozzle, layer height, material and printer family (Bambu
core-XY); but these surfaces were printed in contact and had to break apart, and ours are not.

**S2. Fab Academy 2026, Kochi lab, Mishael Sharaf, week 5.** FETCHED.
<https://fabacademy.org/2026/labs/kochi/students/mishael-sharaf/assignments/week05.html>
Bambu Lab A1, generic PLA, 0.4 mm nozzle, layer height not stated for the gauge: "0.05–0.10 mm:
fused or immovable; 0.15 mm: moved with friction; 0.20–0.25 mm: moved freely and smoothly; 0.30 mm:
loose fit." A print-in-place coin at 0.2 mm layers: "0.25 mm clearance around the inner edge was
sufficient" once a thin bridge across the gap snapped. Per side not stated. Same transfer
condition as S1: print-in-place, so an upper bound for a dropped-in part.

**S3. Sovol, "Print-in-Place 3D Printing: How to Design Hinges, Joints, and Moving Parts".**
SNIPPET (HTTP 429). <https://www.sovol3d.com/blogs/news/print-in-place-3d-printing-how-to-design-hinges-joints-and-moving-parts-that-actually-work>
Summary said: 0.25 mm per side (0.50 across) as a PLA hinge baseline, "baseline starting points, not
universal constants". Printer not stated in the summary.

**S4. uavmodel blog, "Print-In-Place Designs: Clearance Tolerances…" (2026).** SNIPPET.
<https://blog.uavmodel.com/?p=4008>
Summary said: 0.2 mm for faces that turn once and lock, 0.3 mm for faces that slide; a Prusa MK4
with 0.4 mm nozzle separates 0.2 mm gaps in PLA, an Ender 3 needs 0.3. Per side not stated.

**S5. MakerWorld, "Gimbal Fidget – Print-in-Place, Customizable" (model 3240371).** SNIPPET (403).
<https://makerworld.com/models/3240371>
Summary said: 0.35 mm everywhere by default; 0.40 if the joints bind, 0.30 if they rattle; PETG
needs 0.05–0.10 mm more than PLA. The bind/rattle pair is the useful part: the designer names both
failure ends of one ladder.

**S6. Print-in-place spinner rings.** SNIPPET (403 on each).
Lunar Prototypes "Ring Fidget Toy" (Thangs 1209639, <https://thangs.com/m/1209639>): 0.2 mm
between the rings by default. Printables "FidgetRing print in place" (1101574,
<https://www.printables.com/model/1101574-fidgetring-print-in-place>) and "Print-in-place fidget
ring" (133578): summaries mention stiffness at first from "tiny burrs" left by the printer, eased
by turning it, and "a well tuned / calibrated printer with 0.4mm nozzle", 0.2 mm layers.
These are the closest shape to ours: a thin band captive inside another band, turning about the
axis of the layers. Thickness and per-side figures not seen.

**S7. MakerWorld, "Print-in-Place 6000 Ball Bearing" (model 2902210).** SNIPPET (403).
<https://www.makerworld.com/en/models/2902210>
Summary said: tested 0.15 to 0.25 mm, 0.20 gave "the best balance of smooth rotation and minimal
play"; Bambu Lab P2S, PLA, **0.12 mm layers**, no supports. *Does not transfer as is*: our layers
are 0.2 mm, so a vertical gap is a whole layer, not 0.12.

**S8. MakerWorld, PAX Designs parametric print-in-place bearing (model 1904412).** SNIPPET (403).
<https://makerworld.com/models/1904412>
Summary said: ball-to-race clearance 0.2 mm, at least 0.25 mm between balls, a total-height
parameter and a vertical ball clearance; printed balls "will not match the low friction or wear
resistance of precision steel bearings".

## 3. Bearings that could fit in 4.4 mm

**S9. Simply Bearings, 6700ZZ thin-section ball bearing.** FETCHED.
<https://www.simplybearings.co.uk/products/6700-zz-eu>
"Inside diameter 10 mm, outside diameter 15 mm, width 4 mm"; £3.40 ex VAT each, £3.03 at 10+.

**S10. Henderson Bearings, 61704 / 6704 thin-section ball bearing 20x27x4 mm.** FETCHED.
<https://www.hendersonbearings.co.uk/61704-6704-thin-section-ball-bearing-20x27x4mm.html>
Bore 20 mm, outside 27 mm, width 4 mm; £1.91 + VAT each, £0.96 at 10, £0.86 at 50.

**S11. The 67xx series, all 4 mm wide.** SNIPPET (eBay listings, not a maker's catalog).
<https://www.ebay.de/itm/127001265740>
Summary listed 6700 10×15×4, 6701 12×18×4, 6702 15×21×4, 6703 17×23×4, 6704 20×27×4,
6705 25×32×4 mm. A Walmart listing in the same search sold a 6700-2RS "sealed on both sides".
The widths of 6700 and 6704 agree with S9 and S10 (fetched); the rest are marketplace figures.

**S12. MakerWorld, printed 608 bearing taking 4.5 mm steel BBs (model 1373851).** SNIPPET (403).
<https://makerworld.com/models/1373851>
Summary said: keeps the 608's outside size, "8mm inner diameter, 22mm outer diameter, and 7mm
thickness"; uses "4.5mm steel BBs, specifically 4.40mm". So a 608, printed or steel, is 7 mm tall.

**S13. Small steel balls.** SNIPPET.
Minibearings Australia, 2 mm chrome steel balls, grade 25, 500 a pack
(<https://minibearings.com.au/products/2mm-balls-bl00200chg25>); an eBay listing of 2.5 mm grade 25
chrome steel, 100 for US$22.99 (<https://www.ebay.com/itm/175079805986>). Chrome steel (52100) is
named in both; whether it rusts in a wet coaster is not covered by these pages.

**S14. MakerWorld, a print with pauses for magnets and 4 mm steel balls.** SNIPPET; seen only in a
search summary, the model id was not resolved.
Summary said: "add in a PAUSE at Layer 19 (3.8mm) and a PAUSE at Layer 44 (8.8mm)", and "If your
printer is not accurate eneough or your extrusion settings are too high, it can happen that the
parts fuse together."

**S15. MakerWorld, "Fully parametric customizable ball bearing, default to 608ZZ" (2108208).**
SNIPPET (403). <https://makerworld.com/en/models/2108208-fully-parametric-customizable-ball-bearing-default>
Summary said: inner and outer races and a cage for "off-the-shelf steel balls, glass beads, or
BBs"; default five 4 mm balls.

**S16. Austin Wells (NC State), "3D Printed Bearings", 2021.** SNIPPET (the fetch failed on its
certificate). <https://austinwells.wordpress.ncsu.edu/2021/01/18/3d-printed-bearings>
Summary quoted: "In the end, the races were too loose and the balls had a tendency to work their way
out from between the races when the semicircular cut-outs I used to insert them were aligned." 6 mm
BBs. Printer and material not seen.

**S17. Bambu Studio pause at a layer.** SNIPPET. Bambu forum "Pause at layer?"
(<https://forum.bambulab.com/t/pause-at-layer/7025>) and Printago's magnet guide
(<https://printago.io/guides/bambu-studio-magnet-holes>): right-click the layer slider, Add Pause;
a pause "needs a human standing by"; one user found pauses dropped after saving a project.
*Why this matters less to us*: our halves are separate prints, so anything loose (balls, a bearing)
goes in when the coaster is closed by hand, as the pieces do now. A pause is needed only if one
print must enclose the part.

## 4. Spinners and turning coasters as precedent

**S18. Adafruit, "3D Printed Fidget Spinner".** FETCHED.
<https://learn.adafruit.com/3d-printed-fidget-spinner/overview>
Most designs "use a standard 608ZZ ball bearing to spin freely"; "The purpose of a ball bearing is
to reduce rotational friction." No clearance or spin-time figures.

**S19. Gears n Gizmos, "short stack pocket spinner" (Tindie).** FETCHED.
<https://www.tindie.com/products/gearsngizmos/short-stack-pocket-spinner/>
"Steel ball bearings give the toy a nice heft and a decent spin"; body and caps PLA, "Steel Ball
Bearing" listed as a material. No spin time.

**S20. MakerWorld, "Vortex Spinner – 608 Bearing" (3009262).** SNIPPET (403).
<https://www.makerworld.com/en/models/3009262>
Summary said: fully printed spinners are satisfying but lack the weight and spin time of an
old-school one; with a 608 bearing, "several seconds" of spin rather than 10 seconds or more; a
ceramic bearing recommended for longer spin. This is the only spin-time statement found, and it is
a designer's claim, not a measurement.

**S21. MakerWorld, "Kinetic Coaster – Flower of Life" (516120), Eternity Labs.** SNIPPET (403; the
3dgo.app mirror also 403). <https://makerworld.com/models/516120>
Summary said: print-in-place coaster with three rings that "spin independently"; "pop the three
rings out on the first use and push them back in until you hear a satisfying 'Click'"; "the
tolerances for this model are meticulously tight"; the largest ring spins less smoothly than the
inner two; about 1.5 h on an X1 Carbon. Thickness and gap not seen. The closest precedent found: a
drinks coaster whose rings turn, held by a snap rather than a bearing.

**S22. MakerWorld, "Kinetic Moiré pattern coaster / fidget" (2428076).** SNIPPET (403).
<https://www.makerworld.com/en/models/2428076>
Summary said: OpenSCAD, a solid base and a rotating top layer whose turn makes a moiré pattern;
licence limits sharing to MakerWorld. How the top is held not seen.

**S23. Printables, "Gear/Cog Drinks Coaster V1" (1030857).** SNIPPET (403).
<https://www.printables.com/model/1030857-gearcog-drinks-coaster-v1>
Summary said: the gears and outer wheel "can be spun", and two placed together drive each other;
imported from Thingiverse.

These are the turning coasters this search found (S21–S23), none of them a split coaster with
loose pieces. That is "none of the three found", not "none exists".

## 5. Living with a mug

**S24. PLA's softening temperature.** SNIPPET. Plastic Ranger
(<https://plasticranger.com/pla-glass-transition-temperature/>): "60-65 °C"; 3D Printerly
(<https://3dprinterly.com/?p=3516>): PLA is not dishwasher safe, household hot water 55–75 °C;
other summaries ranged 57 to 80 °C. Hobby sources, not a filament data sheet.

**S25. PLA creep under a steady load.** SNIPPET. Outdoors Codidact
(<https://outdoors.codidact.com/q/278429>): "a constant force on a piece of PLA will cause it to
flow, permanently changing the shape of the part."

**S26. PLA friction.** SNIPPET. Search summaries of tribology papers (Zivic et al. 2021,
<https://scidar.kg.ac.rs/handle/123456789/13222>; Pawlak and Wieleba, PLA against steel,
<https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-8fe00cc3-68fd-45bf-be4c-e0712e79c308/c/PAWLAKWIELEBA.pdf>):
printed PLA's friction depends on print direction and infill; "PLA exhibits relatively high friction
compared to other 3D printing materials like nylon or PTFE" (a 2026 review, per the summary). **No
PLA-on-PLA friction figure was found.** How long a printed plain bearing spins is therefore
unmeasured here.

## 6. From this repo

- **R1.** [cut-pieces-joins-design.md §2](../design/coaster/cut-pieces-joins-design.md#2-the-room-in-each-piece):
  middle face 18.0 × 19.0 mm, band 20.6 × 21.7 mm, room for three 1.2 mm pins; a half is 2.1 mm
  (0.6 face block, 1.5 band); pins keep a 0.6 mm floor (CAL-CST-03).
- **R2.** [loose-pieces-design.md §3.4](../design/coaster/loose-pieces-design.md#34-which-fit-numbers-transfer-and-on-what-condition):
  CAL-FIT-01's ladder (press −0.1, snug 0.05, sliding 0.15, free 0.35) and why the print-in-place
  gap CAL-CLR-01 (0.4 mm) does not transfer to a dropped-in piece.
- **R3.** [split-06](../design/plates/split-06.md): piece gap 0.10 (small kite 0.12), `room` 0.2,
  1.2 mm pins at 0.25 mm; its pin ring 1 at 9.6 mm (in the middle star's inner corners) was removed
  in iteration 4; ring 3 stands at 14.3 mm with `stud_boss 1`, which fills the undercut in a disc
  round each pin.
- **R4.** bikar `patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr` at origin/main: the
  `wedge`, `wedge_from` and `wedge_center` knobs print a slice with the middle piece and its
  opening; `height` ranges 3.2 to 6; `room` 0 to 0.6; `stud_boss` notches each piece's flange.
- **R5.** split-05: 1.0 mm pins "shakes a bit", which Omar did not take (record linked from R1 §1).
- **R6.** Memory, Omar 2026-10-04: a color swap costs about 1.6 min and prime-tower waste; one color
  per plate, picked at the send.
