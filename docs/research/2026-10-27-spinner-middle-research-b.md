---
date: 2026-10-27
produced-by: researcher B subagent (Claude Opus 5.5), web search and page fetches, independent of researcher A; repo facts read from this repo at origin/master and from bikar origin/main
feeds: docs/design/coaster/spinner-middle-design.md (through docs/design/coaster/spinner-middle-design-b.md)
---

# A middle piece that spins: raw findings (research B)

**The question.** What would it take to 3D print the middle piece of the split flange coaster so
it spins, like a fidget spinner set into the coaster? The coaster is 112.5 mm across and 4.4 mm
tall, printed on a Bambu Lab X2D with a 0.4 mm nozzle, PLA, 0.2 mm layers. The middle piece is a
ten-pointed star, cut into two halves joined by 1.2 mm pins, held in the frame by a flange under
the frame's lip.

**How to read this file.**

- Sources are numbered S1 to S22. Each is marked **FETCHED** (I read the page through the fetch
  tool, which returns a model's reading of the page, not raw HTML) or **SNIPPET** (I saw only a
  search result summary, or the site refused the fetch with 403, 429 or 402). A snippet is never
  load-bearing on its own.
- R1 to R5 are facts from this repo or from bikar, read from files, not the web.
- Every clearance says whether the source gave it **per side** or **across the diameter**, or
  "not stated", and on what printer, nozzle and material.
- Quotes are short and verbatim where marked with quotation marks.

## 1. Our own facts (repo reads)

- **R1. The middle piece's size.** The cut-pieces design measured it on 2026-10-24 from a render at
  split-06's settings: at the face 18.0 × 19.0 mm across, 205 mm², and the largest circle that
  fits inside it has a radius of 7.27 mm; at the band (the flange level) 20.6 × 21.7 mm, 265 mm²,
  room 8.0 mm; its area over the area of its convex hull is 0.77, so it turns inward deeply
  ([cut-pieces-joins §2](../design/coaster/cut-pieces-joins-design.md#2-the-room-in-each-piece)).
  So the star's points reach roughly 9.5 mm from the centre at the face, and about 10.8 mm at the
  band. I tried to re-render the middle piece with the bikar CLI on 2026-10-27; the shared bikar
  checkout's built CLI is older than bikar origin/main and refused the file ("Statement 'pins' is
  not allowed in a coaster block"), so no fresh measurement was taken.
- **R2. The frame round the middle.** The plates that printed split-09 and split-10 put a ring of
  ten 1.2 mm pegs at 13.0 mm radius round the middle star (stud ring 3), on the strap junctions
  there ([split-10.yaml](../design/plates/split-10.yaml)). So the straps round the star's points
  reach out to about 13 mm.
- **R3. Height.** The closed coaster is 4.4 mm; each half is 2.2 mm. The bkr file's own comment
  says the undercut starts 0.6 mm up from each face, so the lip over a piece's flange is 0.6 mm
  thick and the undercut is about 3.2 mm tall. The flange reaches 0.8 mm into the strap (bkr
  `flange` default 0.8). Read from the bkr file in bikar origin/main
  (patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr).
- **R4. Fits we have printed.** Loose pieces fit their holes at 0.10 to 0.12 mm per face in
  split-07 and split-10's stock pieces; these are pieces dropped in and left still, not turned.
  The bet that governs this, CAL-LSE-01, is still open, and the loose-pieces design says plainly
  that neither CAL-FIT-01 nor the print-in-place gap CAL-CLR-01 transfers to a loose piece in a
  closed pocket ([loose-pieces §3.4](../design/coaster/loose-pieces-design.md#34-which-fit-numbers-transfer-and-on-what-condition)).
- **R5. The middle's flange already prints poorly.** split-07's middle piece had what Omar called
  a "webbed duck feel"; split-10 tests whether supports or a 45° slope under the flange's step fix
  it ([split-10 page](../design/plates/split-10.md)). Any round flange inherits the same step over
  air.

## 2. Clearances for rotating printed parts

- **S1. Fab Academy Ísafjörður, group week 5 (2025).** FETCHED.
  <https://fabacademy.org/2025/labs/isafjordur/group_assignments/group_week05/>
  Print-in-place rotational joints, horizontal and vertical, at 0.1, 0.15, 0.2 (and 0.3) mm.
  **Bambu Lab X1 Carbon, 0.4 mm nozzle, 0.2 mm layers, PLA, 50% infill:** "Both the horizontal and
  vertical joints were moveable at 0,15." Prusa MK4S, 0.4 mm, 0.2 mm layers, PETG: "the vertical
  joint broke loose at 0,2 mm clearance and the horizontal joint at 0,15 mm." Per side or across
  the diameter: **not stated**. The nearest machine to ours in this file (a Bambu, same nozzle,
  same layer, PLA), but a print-in-place test: the failure it measures is the two parts fusing.
- **S2. "Print-In-Place Designs: Clearance Tolerances…" (blog.uavmodel.com, 2026 guide).**
  FETCHED. <https://blog.uavmodel.com/?p=4008>
  Table: PLA, 0.4 mm nozzle, minimum 0.15 mm, recommended 0.25 to 0.3 mm; PETG 0.4 mm, minimum
  0.25, recommended 0.35. Sliding faces 0.3 mm, faces that "rotate once and lock" 0.2 mm. A
  ball joint "fuses if the radial clearance is tighter than 0.15mm". Per side or across: **not
  stated** in the table. Printers named: Prusa MK4 separates 0.2 mm PLA gaps, Ender 3 needs 0.3.
  Advice: print a gauge of narrowing gaps and pick the smallest that separates.
- **S3. Sovol, "Print-in-Place 3D Printing: How to Design Hinges, Joints, and Moving Parts".**
  SNIPPET (429 on fetch).
  <https://www.sovol3d.com/blogs/news/print-in-place-3d-printing-how-to-design-hinges-joints-and-moving-parts-that-actually-work>
  Search summary: 0.20 to 0.30 mm per side for smooth rotation, 0.25 per side as a test point.
- **S4. Gimbal Fidget, print-in-place (MakerWorld 3240371).** SNIPPET (403).
  <https://makerworld.com/models/3240371> Search summary: 0.35 mm everywhere, tested on a Bambu Lab
  P1S; PETG needs 0.05 to 0.10 more; 0.40 if a joint stays locked.
- **S5. Fidget Spinner Keychain, parametric, print in place (Printables 1424794).** SNIPPET (403).
  <https://www.printables.com/model/1424794-fidget-spinner-keychain-parametric-print-in-place>
  Search summary: "clearance remains the same - 0,3mm"; large seams can fuse the bearing to the
  body; lower flow a few percent if it fuses.
- **S6. SPINNER, print-in-place hand spinner (Thangs, CharlesRegaud).** SNIPPET (403).
  <https://thangs.com/designer/CharlesRegaud/3d-model/SPINNER%2520%257C%2520Print-in-place%2520fidget%2520hand%2520spinner-995119>
  Search summary: three files at 0.2, 0.25, 0.3 mm; "The 0.2 mm version works, but you'll have to
  wiggle the bearings a little to get them unstuck."
- **S7. QIDI, "How to 3D Print Interlocking Parts and Assemblies".** SNIPPET (429).
  <https://qidi3d.com/en-br/blogs/news/how-to-3d-print-interlocking-parts-and-assemblies>

**What transfers.** Every number in S1 to S6 is for parts **printed in place**, where the risk is
the two parts fusing into one. Our middle piece and frame are printed apart and put together, so
fusing cannot happen; the risks are instead the first-layer flare (elephant foot) on the bottom
edge, the layer ridges of two vertical walls rubbing, and the closed round hole printing smaller
than drawn (the hole-shrink bet CAL-HOL-01, unmeasured). So these numbers are **upper bounds on
the gap we need, not the gap**: a gap that keeps printed-in-place parts apart is wider than one
that lets two separate parts turn. The one Bambu-with-PLA reading (S1, 0.15) was measured on an
X1 Carbon, not an X2D, and the source does not say per side. Our own stationary fit (R4) is 0.10
to 0.12 per face. That brackets a starting ladder of 0.10 to 0.25 per face; no source found here
measures a turning fit between two separately printed PLA parts on any Bambu printer.

## 3. Printed bearings and rollers

- **S8. Bambu Lab forum, "Bearings: Balls or No Balls (i.e. rollers, nothing, etc)".** FETCHED.
  <https://forum.bambulab.com/t/bearings-balls-or-no-balls-i-e-rollers-nothing-etc/94119>
  Printed ball bearings: "Half the balls still needed 'massaging' before they rolled freely, but
  they did work." Printed 608-style bearings work in PLA, PETG or PC but "they are just too rough
  to make for decent bearings." A plain bushing in low-friction filament (Igus iglidur) is
  mentioned, not tried. No printer named.
- **S9. Hackaday on Matvey Kukuy's "Ultimate 608 Bearing with Calibration Kit".** FETCHED.
  <https://hackaday.com/tag/608-bearings/> Print-in-place 608 bearings; 64 calibration variants
  searched like a binary search; "two key tolerances" found by testing, not CAD; PLA at 0.16 mm
  layers gave the best results; print one bearing at a time, since a full bed shifted results;
  a PTFE grease such as Super Lube suggested.
- **S10. Print-in-place roller cages, a soft-robot patent (USPTO 9802314).** SNIPPET.
  Search summary: printed roller cages worked best at about 0.2 mm; above about 0.3 rollers escape
  or jam; under 0.1 they fuse. Different machine and process, not stated.
- **S11. Parametric bearing with steel balls (MakerWorld 2108208).** SNIPPET (not fetched).
  <https://makerworld.com/en/models/2108208-fully-parametric-customizable-ball-bearing-default>
  Printed races sized for bought steel balls, glass beads or BBs, with a Gothic-arch race and a
  printed cage; says steel balls in printed races beat all-plastic bearings.

**Reading.** Printed rolling bearings exist and turn, but the two fetched reports (S8, S9) agree
they are rough unless tuned hard and run in, and S9's tuning took a 64-variant calibration. No
source found here prints a rolling bearing in a part as thin as 4.4 mm.

## 4. Bought bearings and balls, and whether they fit in 4.4 mm

- **S12. 6700ZZ (Simply Bearings).** FETCHED. <https://www.simplybearings.co.uk/products/6700-zz-eu>
  Bore 10 mm, outside 15 mm, width 4 mm. The thinnest deep-groove ball bearing found in this
  search near our size.
- **S13. 61800 thin-section bearing.** SNIPPET. <https://www.simplybearings.co.uk/products/61800>
  10 × 19 × 5 mm.
- **S14. AXK 1024 needle roller thrust cage (SKF, Klium).** FETCHED.
  <https://www.klium.be/en/skf-axk-1024-needle-roller-bearing-10-x-24-mm-46430> Bore 10, outside
  24, thickness 2 mm; a "Needle roller and cage assembly", washers sold apart.
- **S15. AXK1024 with two AS1024 washers (Simply Bearings, NTN).** SNIPPET (429 twice).
  <https://www.simplybearings.co.uk/products/axk1024-ntn-as1024-ntn> Search summary: cage with two
  1 mm washers is 10 × 24 × 4 mm; roller diameter 2 mm.
- **S16. 3.175 mm G25 chrome steel balls (Miniature Bearings Australia).** SNIPPET.
  <https://miniaturebearings.com.au/products/3-175mm-balls-bl00318chg25/data?view=data>
  ±0.00254 mm on diameter, SAE 52100 chrome steel.
- **S17. AISI 440C stainless ball bearings (SCA Shinyei).** FETCHED.
  <https://sca-shinyei.com/ballbearing/bearing_aisi440c> "Higher resistance to rust and corrosion
  than 52100 chrome bearing steel", but "AISI 440C stainless steel may corrode depending on the
  environments and conditions"; points to 304 or 630 where more resistance is needed.
- **S18. Stainless vs chrome steel balls, other suppliers (Bearing King, McMaster-Carr).**
  SNIPPET. 440C is passivated; 316 resists more but wears more; about 1.984 mm (0.0781 in) is a
  common stock size near 2 mm.

**Height arithmetic (mine, from the numbers above and R3).** The coaster is 4.4 mm.

| Part | Height | What is left of 4.4 mm | Fits? |
|---|---|---|---|
| 6700ZZ (S12) | 4 mm | 0.2 mm for both faces' skins | No: one 0.2 mm layer per face would not cover it, and its 15 mm outside is near the star's 14.5 mm smallest across at the face (R1) |
| 61800 (S13) | 5 mm | none | No |
| AXK1024 cage + two washers (S14, S15) | 4 mm, 24 mm across | 0.2 mm per face | No: wider than the middle piece's band (20.6 × 21.7 mm, R1) and as tall as the 6700 |
| AXK1024 cage alone, rollers on printed faces | 2 mm | 2.4 mm, 1.2 per face | Fits in height; needles rolling on PLA rather than on hardened washers is outside what the listings rate, and 24 mm is still wider than the band |
| 2 mm steel balls in a groove | 2 mm, plus 0.2 mm groove depth each side | about 0.6 mm skin above and below at the coaster's middle | Fits in height on paper; the ring of balls needs a groove about 2.4 mm wide, three times today's 0.8 mm undercut |

None of the bought bearings checked here fits the 4.4 mm coaster with both faces covered. The
coaster's `height` param runs to 6 mm (R3), so at about 5.5 to 6 mm the 6700ZZ would fit with
0.75 to 1 mm over each face; that changes how every coaster we have printed feels in the hand.

## 5. Putting steel balls in: pause the print, or drop them in at assembly

- **S19. Printago, "Bambu Studio magnet holes" guide.** FETCHED.
  <https://printago.io/guides/bambu-studio-magnet-holes> Pause at the layer where the pocket gets
  capped; size a pocket at "diameter plus about 0.1 to 0.2 mm clearance"; "keep magnets away from
  the nozzle and any steel components while the head moves."
- **S20. Pause at layer, MakerWorld model pages and a Bambu forum thread.** SNIPPET. Right-click
  the layer slider in Bambu Studio, "Add Pause", re-slice; a pause set from Bambu Handy does not
  work; one guide uses a cavity 0.3 mm wider than the magnet with 0.4 mm over it.

**Reading.** Our coaster is already put together by hand from two frame halves and loose pieces.
So balls can be dropped into the lower half's groove at assembly and trapped when the upper half
goes on, the same way the pieces are trapped today. A pause at a layer is not needed for this
design, and the X2D's steel nozzle-and-magnet caution (S19) does not arise unless magnets are
used.

## 6. Spinning things set into flat objects (precedent)

- **S21. Kaleidoscope Coaster (Printables 769752).** SNIPPET (403).
  <https://www.printables.com/model/769752-kaleidoscope-coaster> Rotating honeycomb discs pick a
  motif; a later update closed the bottom "so the coaster works as a coaster".
- **S22. Gear/Cog Drinks Coaster V1 (Printables 1030857).** SNIPPET.
  <https://www.printables.com/model/1030857-gearcog-drinks-coaster-v1> Gears and an outer wheel;
  two side by side turn each other; glued at the corners.
- Also seen only as snippets: a "rose window" rotary clicker on MakerWorld with "36 tactile clicks
  per revolution" from a flexible arm in the base riding a 36-step rim; a ratchet fidget whose
  maker reports PLA works and PLA+ gives a stronger click; a note that PLA flexures deform under
  sustained load and PETG is safer for a spring that flexes often. Fidget hand-spinner listings
  (MyMiniFactory, Tindie, Instructables) pair a 608 bearing with steel weights, and one says
  printed-only spinners "simply don't have the weight or spin time of a metal-bearing spinner".

**Reading.** I found two coasters with turning parts (S21, S22), both snippets, neither a spinner;
none of the listings seen states a spin time or a clearance for a coaster. "No coaster spinner
exists" would be a claim over a space this search did not cover; what it found is none among the
pages above.

## 7. Friction and spin time

- No PLA-on-PLA friction coefficient was found. The search returned PLA sliding on steel at about
  0.49 to 0.54 (two tribology papers, SNIPPET), and a 2021 study of printed PLA under a ball that
  found friction lower along the print lines than across them and higher at 20% infill than at
  100% (SNIPPET, no number in the abstract). So spin time cannot be estimated from a source here.
- **What can be said without a friction number.** How long a part spins after a flick depends on
  how much it resists being slowed (its moment of inertia) against the drag in its bearing. For a
  flat disc of fixed thickness the mass grows with the radius squared and the inertia with mass
  times radius squared, so the inertia grows with the **fourth power** of the radius. A middle
  piece about 21 mm across is small and light; a disc twice as wide holds sixteen times the spin.
  Hand spinners get their spin from steel weights far out and a steel ball bearing (section 6),
  neither of which the middle piece has room for. My expectation, unmeasured: the middle piece will
  **turn** when pushed and stop within a turn or two, rather than spin on its own for seconds.

## 8. Coaster-specific constraints (from the sources and repo)

- **Wet mug.** A coaster takes condensation and spills. Water will wick into any round gap and
  into a ball groove. Chrome steel balls (52100) rust; 440C resists but "may corrode" (S17). A
  plain PLA-on-PLA turning fit has nothing to rust and can be rinsed.
- **Flat, no wobble.** A spinning middle that sits flush carries part of the mug's weight on the
  turning part; one that sits one layer lower (bikar's `loose … height` already sets a piece's
  height, loose-pieces §3.2) leaves the mug on the frame. Vertical play is what rattles: today's
  `room 0.2` makes each piece 0.2 mm shorter than the gap between the halves.
- **Cleaning.** A captive turning part with a 0.1 to 0.25 mm gap can trap grime; the coaster
  comes apart only by separating the halves, which split-02 showed can come apart in the hand
  without pegs (bkr comment) and split-09/10 hold with pegs.
