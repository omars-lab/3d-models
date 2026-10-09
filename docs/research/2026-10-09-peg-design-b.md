---
date: 2026-10-09
produced-by: research subagent B (Claude Opus 5.5), web search and page fetches, independent of researcher A
feeds: docs/design/pieces/peg-design-b.md
---

# Printed pegs and sockets: how to make two printed halves join well (research B)

**The question.** Our split coasters join two printed PLA halves with round studs in round
sockets on the cut plane. On spl-1 (gaps drawn from −0.10 to 0.15 mm across the diameter)
every pair needed a hammer. spl-2, sent to the printer on 2026-10-09 and not yet judged, runs
0.15 to 0.40 mm. What do other people
do to get a good press fit, a snap, or a LEGO-like clutch between printed parts, and which of
those ideas transfer to a 2 mm stud in a 2.2 mm half printed on a Bambu X2D with a 0.4 mm
nozzle at 0.20 mm layers?

**How to read this file.**

- Sources are numbered S1 to S30. Each says **FETCHED** (I read the page through the fetch
  tool, which hands back a model's reading of the page, not the raw HTML; S1 was also read as
  raw HTML) or **SNIPPET** (only a search-result line or summary was seen, or the site refused
  the fetch). A snippet can be out of context and is never load-bearing on its own.
- C1 to C9 are sources this repo already fetched and recorded in earlier research. They are
  carried, not fetched again, and each names the file that holds it.
- Quotes are verbatim and short. Where a quote contained the British spelling of "mold", it is
  paraphrased instead.
- Every number says whether it is **per side** or **diametral** (across the diameter), and the
  printer, nozzle, material and layer height behind it. "Not stated" means the source is
  silent.
- The design doc this feeds is [peg-design-b](../design/pieces/peg-design-b.md).

## 1. Why our fit is tight: holes print small, studs print large

**S1 — Bambu Lab wiki, "Auto circle contour-hole compensation".** FETCHED (raw HTML read
directly). Kind: vendor manual.
https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation

- Scope: "only for complete circles on the horizontal plane", with "a diameter size within
  50mm".
- It is calibrated at 200 mm/s with maximum cooling, and is "only compatible with some Bambu
  Official filaments".
- The effect is reduced at 100% infill or when shafts sit too close together.
- Moisture moves the fit: "dry filament results in a looser fit, and moist filament results in
  a tighter fit".
- The fine-tune value: "positive values make the assembly looser", in a "step value of 0.02mm".
  Per side or diametral: not stated.
- It uses a scarf seam on the circles.
- It is off by default (`enable_circle_compensation` is "0" in the page's example settings).
- Printer: Bambu machines in general; nozzle, material and layer: not stated beyond "some Bambu
  Official filaments".

**S2 — Bambu forum, "Square section is good but round section is small" (thread 168189).**
FETCHED. Kind: user forum thread, H2D.
https://forum.bambulab.com/t/square-section-is-good-but-round-section-is-small/168189

- "The round section of my part is consistently too small but the square portion is
  dimensionally correct".
- A hole drawn about 11.1 mm printed about 10.9 mm (diametral). Others in the thread report
  circles undersize by "up to 0.7mm" (diametral, by context) and say older Bambu machines were
  "within 0.1mm of CAD".
- Auto circle compensation (S1) made little difference for the poster; slowing down made it
  worse; enlarging the hole in CAD worked best. "Speed can be a contributing factor!" One reply:
  "Isn't this why polyholes were invented?"
- Printer: H2D. Materials: Polymaker ABS and Bambu PLA. Nozzle and layer: not stated.

**S3 — Bambu forum, "Hole size issues" (thread 100439).** FETCHED. Kind: user forum thread.
https://forum.bambulab.com/t/hole-size-issues/100439

- "10mm holes are a little large, around 4mm is perfect and as they get smaller they get
  tighter".
- Printer, nozzle, material and layer: not stated.

**S4 — Bambu forum, thread 195469.** FETCHED. Kind: user forum thread.
https://forum.bambulab.com/t/printing-precise-elements-which-settings-to-improve-accuracy/195469

- "I used .4mm nozzle, .08mm layer, .3mm line width"; "I had to increase hole's inner diameter
  by .2mm" (diametral, by the wording "inner diameter").
- Printer and material: not stated.

**S5 — Bambu forum, thread 258975.** FETCHED. Kind: user forum thread.
https://forum.bambulab.com/t/precision-of-fdm/258975

- A calibration cube printed "20.00 (x) x 20.00 (y) x 19.98 (z)". No hole data. It shows flat
  outer faces can print true while S2 says circles do not.

**C1 — Creative3DP, "Press-fit tolerances for 3D printing".** Carried from
[split-with-studs research §3](split-with-studs-research.md#3-fdm-pin-and-stud-tolerances)
(its S22). Kind: tool vendor blog.
https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/

- Holes print 0.1 to 0.3 mm undersize; shafts about 0.1 (0.1 to 0.2) oversize. Diametral by
  the table's framing.
- Its table, for 5 to 25 mm parts, diametral: press −0.10, snug +0.05, close running +0.15,
  free +0.35.
- "A PLA press fit under constant stress relaxes over months".
- Printer, nozzle and layer: not stated; material: PLA among others.

**C9 — repeatability against bias**, carried from
[lego-lab §3.5](../design/pieces/lego-lab-design.md#35-our-existing-fit-vocabulary-cannot-express-a-lego-clutch--but-not-for-the-reason-v1-gave):
Zaborniak (repeatability σ about 0.02 mm, a range of 0.06 over 12 parts), NIST Moylan
(+0.023 on pins against −0.115 on holes in one build, metal powder-bed, so the mechanism
transfers and the size does not), the ISO/ASTM 52902 test artifact (about 0.05 on flat faces
against about 0.15 on cylinders), Popescu (6 mm holes −0.124 best, −0.370 worst).

**What this adds up to.** The printer repeats itself well (σ about 0.02) but is biased: holes
come out small and studs come out large. Using C1's ranges, a hole 0.1 to 0.3 small plus a
stud 0.1 to 0.2 large is 0.2 to 0.5 mm of squeeze across the diameter. A gap drawn at 0.15
then nets about −0.35 to −0.05 (interference), which matches spl-1's 4F: it went in by hand
but needed a hammer to sit flush. A gap drawn at 0.40 nets about −0.10 to +0.20. **Transfer
(K10):** C1's ranges are for 5 to 25 mm parts on unnamed printers; our holes are 2 mm, and S3
says small holes get tighter, so the squeeze at 2 mm may sit at or past the top of C1's range.
The arithmetic is a reason to expect the hand fit near or above 0.40, not a prediction of it.

## 2. Polyholes: why a small round hole shrinks, and the fix

**S6 — nophead (HydraRaptor blog), "Polyholes", 5 Feb 2011.** FETCHED. Kind: maker blog by a
RepRap developer. https://hydraraptor.blogspot.com/2011/02/polyholes.html

- "When Reprap machines print holes they tend to come out undersized".
- Corner cutting (the nozzle path cutting the inside of each polygon corner) is "the dominant
  effect on my machines".
- The rule: sides n = max(round(2d), 3), and the drawn radius r = (d/2)/cos(180°/n).
- "10 vertices … 5% and 22 for 1%"; "the maximum number of vertices you can have before the
  hole shrinks is twice the hole size in mm".
- Holes tested 1 to 10.5 mm in 0.5 steps. HydraRaptor laid 0.375 mm filament from a 0.4 nozzle;
  the Mendel 0.6 mm through a 0.5. Material and layer: not stated in what I read.
- At d = 1 the rule gives a triangle; at our d = 2 it gives a square (n = 4).

**Transfer (K10).** The mechanism (a flowing line rounds the inside of a curve, so many small
facets print as a smaller circle) is about extrusion, so it carries to any FDM machine. The
size of the effect on a 2011 RepRap does not carry to an X2D, whose motion and slicer are very
different; S2 is the only Bambu evidence that circles still shrink, and it is one thread.

**S25 — softsolder (Ed Nisley).** SNIPPET. Kind: maker blog. Snippets say polyholes did poorly
for small holes for him, that he used a fixed "HoleWindage" adder of about 0.2 mm (per side or
diametral: not stated), and that he cut a glue gutter around pins. Printer, nozzle, material:
not stated in the snippets.

**S27 — a search summary, page not identified.** SNIPPET. "1.6 mm for the 2 mm hole, 2.67 mm
for the 3 mm hole, 3.7 mm for the 4 mm hole with the classic wall generator and no
compensation." If true, a 2 mm hole printed 0.4 small. I could not find the page, so this
stays out of every conclusion.

## 3. Slicer compensation

**S1** (above) is the Bambu-side fix: per-hole compensation tuned in 0.02 mm steps, for
complete horizontal circles under 50 mm, off by default, tuned for "some Bambu Official
filaments". Our sockets are complete horizontal circles under 50 mm, so they qualify on
shape. Whether our PLA is on the list: not checked.

**C2 — Bambu wiki, XY hole compensation.** Carried from
[split-with-studs research §3](split-with-studs-research.md#3-fdm-pin-and-stud-tolerances).
Default 0; holes under 1 mm are "challenging to tune".

**S2** is the counter-evidence: one H2D owner found auto circle compensation made little
difference and drawing the hole larger worked best. One thread, so it is a warning, not a
verdict.

## 4. Lead-ins: chamfers, elephant foot, seams

**S14 — Make, "Tips for 3D printing press-fit parts".** FETCHED. Kind: magazine how-to.
https://makezine.com/article/digital-fabrication/3d-printing-workshop/tips-3d-printing-press-fit-parts/

- Chamfer the pin's end and the mating part's edge.
- Give a pin a flat side so it can print lying down, the strong way.
- A center hole in a pin lets it flex.
- A hexagon or octagon pin in a round hole.
- The author drew zero clearance and needed six tries to get the fit. Printer, nozzle,
  material, layer: not stated.

**S16 — Makerforums, "Print design tips" (thread 89216).** FETCHED. Kind: user forum.
https://forum.makerforums.info/t/print-design-tips/89216

- A 2° taper "works really well" to hold parts "yet allow them to release".
- The poster "added .1mm to the radius" (per side) of holes, and leaves "2 mm of extra depth"
  at the bottom of a hole so the pin never bottoms out.
- Printer, nozzle, material, layer: not stated.

Elephant foot (the first layers squashed wider by the bed) is carried from
[split-with-studs research §6](split-with-studs-research.md#6-elephants-foot). Both our halves
print face down, so the stud's top and the socket's mouth are the last layers, and elephant foot
does not reach them. Where the seam lands on a small circle is a separate effect; S1 moves it
onto a scarf seam for compensated holes.

## 5. Crush ribs

**S17 — Hackaday, Donald Papp, 15 Oct 2020, "Adding crush ribs to 3D printed parts for a
better press fit".** FETCHED (read through the site's tag page, which carries the post in
full). Kind: tech news write-up.
https://hackaday.com/2020/10/15/adding-crush-ribs-to-3d-printed-parts-for-a-better-press-fit/

- Crush ribs are "a set of very small standoffs that deform" when a part is pressed in.
- They are "far easier (and more forgiving)" than tuning a round hole.
- No numbers.

**S18 — newscrewdriver, 31 Dec 2020, "Accommodate 3D printer variation with crush ribs".**
FETCHED. Kind: maker blog.
https://newscrewdriver.com/2020/12/31/accommodate-3d-printer-variation-with-crush-ribs/

- "it is easier for a bearing to crush small ribs than to reshape the entire cylinder".
- No numbers.

**S20 — Printables model 43636, a crush-rib test.** SNIPPET (the site returned 403). Kind:
model page. Snippets say the author found the walls flexing mattered more than the ribs
crushing; the test used a square hole; a 2° draft fit but was hard to remove and 1° came out
easier. A forum reply nearby suggests 0.2 to 0.3 mm of interference (per side or diametral:
not stated).

**S21 — molding crush-rib guidance, from a search summary (page not identified).** SNIPPET.
At least 3 ribs, about 0.25 mm (0.01 in) of interference. For injection-molded parts.

**Transfer (K10).** The idea (put the squeeze into a few thin features that can give, instead of
the whole wall) carries, because it is about where the interference goes, not about the
process. The 0.25 mm number does not carry: it comes from molded parts, and a printed rib on a
2.5 mm bore is one or two lines wide, so its true height is set by the printer, not the
drawing.

## 6. Other shapes: square and hex holes, split pins, dowels

**S6** above: at 2 mm, nophead's rule itself gives a square hole.

**S2** above: square sections print true while round ones shrink, on an H2D.

**S14** above: a hexagon or octagon pin in a round hole.

**S23 — Printables model 240168, a filament hole gauge.** SNIPPET. Kind: model page. Holes 1.7
to 2.8 mm in 0.1 steps for a 1.75 mm filament rod; "one size doesn't work for both
orientations" (vertical and horizontal holes print differently).

**S24 — printablescenery, a guide to filament pins.** SNIPPET. Kind: maker guide. Drill the
hole slightly larger; set with super glue; a remixer went to 2.1 mm for a 1.75 rod (0.35
diametral).

**S22 — MakerWorld model 2820462, a hole tolerance test.** SNIPPET (403). Holes from +0.10 to
+0.60 mm over nominal (per side or diametral: not stated).

## 7. Which way layers run, and how short a peg should be

**S13 — CNC Kitchen, "Stop printing flat: the 45° secret for stronger parts".** FETCHED. Kind:
maker lab blog with tensile tests.
https://cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts

- Flat "63 MPa", standing "31 MPa".
- "Layer adhesion is typically around 50% of the in-plane strength".
- Printer: Prusa CORE One; layer 0.2 mm; nozzle and material grade: not stated in what I read.

**S15 — UPenn mechanical engineering, "3-d printing tips".** FETCHED. Kind: university lab
guide. https://medesign.seas.upenn.edu/index.php/Guides.3-dPrintingTips

- Use "stubby pegs (aspect ratio no greater than 1, or they have a tendency to break off)".
- Draw pegs line-on-line (zero clearance). Printer, nozzle, material, layer: not stated.

Our stud is 2.0 wide and 1.4 tall, so it already meets S15's stubby rule (height under
width). It stands upright, the weak way for layers (S13), and spl-1 broke none.

## 8. A taper

**S16** (2° holds and releases) and **S20** (2° hard to remove, 1° easier) both point at a
small taper. Over our 1.4 mm stud, 2° is about 0.05 mm a side, about one fortieth of a line
width. **Transfer (K10):** a taper changes the fit only when it is larger than what the printer
resolves; at 1.4 mm tall it falls inside the hole-and-stud bias of §1, so on our stud it would
act as a lead-in, not as a fit setting.

## 9. Locating pins: one round, the rest slotted

**S12 — Carr Lane, "Locating pins".** FETCHED. Kind: fixture maker's engineering notes.
https://carrlane.com/engineering-resources/technical-information/manual-workholding/locating-devices/locating-pins

- Diamond (relieved) pins avoid "the redundant location that causes binding during loading".
- "the diamond pin acts as a radial locator" (it fixes rotation only, while one round pin fixes
  position).

**Transfer (K10).** This is geometry, not process: two round pins that are both a tight fit
over-constrain a part, and any spacing error between them becomes binding. That holds for
printed halves as for machined fixtures, and it gets worse as stud count grows.

## 10. The LEGO clutch

**C3 — the LEGO patent and LEGO's own explanation.** Carried from
[the LEGO brick survey §2](lego-brick-system-survey.md#2-the-clutch-is-tangency--and-it-is-patented-as-such)
and the [clutch survey §3](pattern-outline-body-clutch-survey.md#3-counter-evidence-the-case-that-the-wall-is-load-bearing).
US3005282 states the clutch as tangency: each stud touches the tube and the walls along lines.
LEGO describes studs "wedged in between the tubes and the sides". Walls carry 50 to 67% of the
contacts by the clutch survey's count.

**C4 — Brighton (via the LEGO brick survey).** Studs measure 4.88 to 4.89 mm, "deliberately
oversized" so the walls flex.

**C5 — LEGO sizes (via the LEGO brick survey and lego-lab).** Stud 4.8, tube outside 6.514,
tube wall 0.857 (per the survey's figures), pin 3.2, outer wall 1.5.

**Mold accuracy.** LEGO says, in a press release carried in
[the baseplate survey §1.2](lego-baseplate-seam-survey.md#12-patent-and-official-lego-tolerance-statements),
that its molds hold about 0.004 mm. Paraphrased; the quote uses the British spelling.

**C6 — MachineBlocks (via lego-lab).** About −0.1 mm per side, plus 0.1 mm clamp ribs.

**S19 — MachineBlocks, "Calibration".** FETCHED. Kind: printable-brick library docs.
https://machineblocks.com/docs/calibration

- Adjustment settings named studDiaAdj, wallThickAdj, tubeZDiaAdj, pinDiaAdj.
- "Start with the smallest setting in each row".
- "Do not force original LEGO® bricks onto the calibration tool".
- No step size or defaults stated on the page.

**C7 — lego-lab §7.6.** [The clutch rib](../design/pieces/lego-lab-design.md#76-the-clutch-rib--a-first-class-feature):
rib 0.10 mm, arc at least 0.8 mm. The LG coupons were never printed.

**C8 — Brickset and Brick Architect (via the LEGO brick survey §5).** Printed bricks clutch
weakly against real ones.

**S26 — thewave.engineer.** SNIPPET (403). lego-lab §3.5 quotes it as "roughly 0.1–0.2 mm" of
interference and 2 to 3 N of pull; nothing more was readable this pass.

**Why it works in molded ABS, and what transfers (K10).** The clutch is a stud touching a thin
wall (and a tube) along a line, with the wall bending a little to make room. A thin wall that
bends forgives an oversize stud; a thick wall does not. That idea transfers to printing because
it is about stiffness, not process. The interference number does not: LEGO's molds hold about
0.004 mm, while a printed 2 mm hole is off by tenths (§1). A fixed interference tuned in
molded ABS is smaller than our printer's bias, so the printed version has to be tuned on the
printer (S19's calibration ladder is exactly that).

## 11. Snap fits

**S7 — Bayer MaterialScience, "Snap-fit joints for plastics: a design guide".** FETCHED (PDF,
mirrored by SparkFun). Kind: material maker's design guide for molded parts.
https://cdn.sparkfun.com/assets/home_page_posts/1/4/1/0/Plastic_Snap_fit_design.pdf

- Table 2 allowable short-term strains: PC/ABS 2.5%, PC 4%, PC blends 3.5%, 10% glass-filled PC
  2.2%, 20% glass-filled PC 2.0%.
- For parts snapped apart and together often, use "about 60%" of those.
- "partially crystalline … almost to the yield point, amorphous … about 70%".
- A tapered arm gives "more than 60%" more deflection for the same strain.
- Annular snap undercut "Ypm = εpm·d"; with both parts equally flexible the strain on each is
  halved.
- Molding-only: PLA is not in the table.

**S8 — Fictiv, "How to design snap fit components".** FETCHED. Kind: manufacturing service
guide. https://www.fictiv.com/articles/how-to-design-snap-fit-components

- Allowable strain: PLA "4-8%", ABS "7%", nylon "4-15%". Process: not stated.
- For printed parts, "reducing the allowable stress/strain by 50% for Z-axis cantilevers",
  because "elongation at break is reduced by 50% and tensile strength by 20-30%".
- "a return angle of 90° can never be disassembled".
- Clearances 0.2 (tight), 0.3 (close-fit snap), 0.4 (slide); printed snaps "typically 0.1–0.3
  mm". Per side or diametral: not stated. Printer, nozzle, layer: not stated.
- A second Fictiv URL (designing-3d-printed-snap-fit-joints) returned only an index page.

**S9 — Xometry Pro, snap-fit design guide.** FETCHED. Kind: manufacturing service guide,
molded parts. https://xometry.pro/en/?p=156440

- Lead and return angles: "30 degrees is typical for a self-engaging latch", "80 degrees is
  typical for a serviceable latch", "At 90 degrees the joint becomes effectively permanent".
- Cantilever strain "ε = 3 × Y × h / (2 × L²)".
- Root fillet "Default R = 0.4 × h".
- Repeated use roughly halves the allowable strain.
- "at least 0.5 degrees of draft per side".

**S10 — UL Prospector, pointing at the BASF snap-fit manual.** FETCHED. Kind: materials
database article. https://ulprospector.ul.com/1248/snapfit-3/

- No strain values; it points to the BASF manual's page IV-4.
- The beam formula holds when length to thickness "is greater than 10:1".

**S11 — Hubs, "How to design snap-fit joints for 3D printing".** FETCHED. Kind: manufacturing
service guide. https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing

- Cantilever and annular types; root fillet at least 0.5 × thickness; arm width at least 5 mm.
- FDM clearance 0.5 mm (per side or diametral: not stated); FDM materials named ABS, nylon,
  TPU.
- "avoid snap-fit cantilevers built vertically in the Z direction".

**S28 — snap angle snippets.** SNIPPET. Lead-in 20 to 30°; one annular reference says 30°
separates easily, 45° is typical, 90° is permanent; a Bayer figure cited in a patent says 60
to 90° is effectively inseparable.

**Protolabs** was not fetched (see the search log).

**What this means at our size.** Two worked cases, with the arithmetic in the design doc's
[snap section](../design/pieces/peg-design-b.md#snap-fits):

- A ring snap on a 2 mm stud (bead 2.3, throat 2.1) needs about 10% strain to pass. S7's
  annular rule at 2 to 4% allows an undercut of only 0.04 to 0.17 mm on a 2 mm ring, and S8
  halves printed allowances again. The undercut a printer can form is a few tenths, so the ring
  either cracks or never clicks.
- A barbed split prong: from S9's formula, length L = sqrt(1.5·y·t/ε). With a 0.2 mm barb (y),
  0.8 mm prong (t, two lines) and 2 to 4% strain, L is 2.5 to 3.5 mm. That is longer than our
  1.6 mm socket and the whole 2.2 mm half, and S10's 10:1 length rule would want 8 mm.

**Transfer (K10).** S7, S9 and S10 are molding guides; their strain limits are for solid,
molded plastics. S8 is the only source here that gives a PLA strain, and it says to halve it
for parts loaded across layers, which is how an upright prong is loaded. S11 says to avoid
upright cantilevers. None of the snap sources here was written for features under 3 mm.

## 12. Fit coupons and calibration

**S19** (MachineBlocks) starts from the smallest setting in each row and steps up. **S23**
gauges 1.75 mm filament in 0.1 steps. **S22** steps holes from +0.10 to +0.60. **S29 — zbotic
press-fit classes.** SNIPPET. Interference light 0.1 to 0.2, medium 0.2 to 0.4, tight 0.4 to
0.6 mm (per side or diametral: not stated; printer: not stated).

**S30 — Bambu PLA Basic technical data sheet.** Not fetched. A snippet gives PLA Silk 3.5%
elongation at break; that is a different material and is not used as a stand-in.

## 13. Where the sources disagree

| Question | One side | Other side | Which this pass trusts |
|---|---|---|---|
| Does Bambu's auto circle compensation fix small holes? | S1: yes, per filament, 0.02 steps | S2: little difference on an H2D; draw larger instead | Neither alone; worth one free reslice (it costs nothing to try) |
| Is a 2° taper a good fit? | S16: holds and releases | S20: 2° fits but is hard to remove, 1° easier | Both agree a degree or two works; at 1.4 mm tall it is a lead-in only (§8) |
| Do small holes print small? | S3, S2, C1, S6, C9: yes | S5: a flat cube prints true | Both: flats print true, circles shrink |
| Polyholes for small holes | S6: the fix | S25 (snippet): poor for small holes | Unsettled; the hex socket test settles it for us |
| Snap clearance | S8: 0.1 to 0.3 | S11: 0.5 | Moot at our size: no snap fits (§11) |

## 14. Numbers table

| Number | Source | Per side or diametral | Printer | Nozzle | Material | Layer |
|---|---|---|---|---|---|---|
| Holes 0.1 to 0.3 small, shafts 0.1 to 0.2 large | C1 | diametral | not stated | not stated | PLA among others | not stated |
| Press −0.10, snug +0.05, running +0.15, free +0.35 | C1 | diametral | not stated | not stated | not stated | not stated |
| Circles up to 0.7 small | S2 | diametral (by context) | H2D | not stated | ABS, PLA | not stated |
| Hole enlarged 0.2 | S4 | diametral | not stated | 0.4 | not stated | 0.08 |
| Compensation step 0.02 | S1 | not stated | Bambu | not stated | some Bambu filaments | not stated |
| Sides n = max(round(2d), 3) | S6 | n/a | RepRap (HydraRaptor, Mendel) | 0.4, 0.5 | not stated | not stated |
| +0.1 on the radius, 2 mm extra depth | S16 | per side | not stated | not stated | not stated | not stated |
| Flat 63 MPa, standing 31 MPa | S13 | n/a | Prusa CORE One | not stated | not stated | 0.2 |
| Peg height no more than width | S15 | n/a | not stated | not stated | not stated | not stated |
| PLA strain 4 to 8%, halved across layers | S8 | n/a | not stated | not stated | PLA | not stated |
| PC/ABS 2.5%, PC 4% short-term strain | S7 | n/a | molded | n/a | PC, PC/ABS | n/a |
| Return 30° self-engaging, 80° serviceable, 90° permanent | S9 | n/a | molded | n/a | not stated | n/a |
| Snap clearance 0.1 to 0.3 | S8 | not stated | not stated | not stated | not stated | not stated |
| Snap clearance 0.5 | S11 | not stated | not stated | not stated | ABS, nylon, TPU | not stated |
| Crush rib interference about 0.25 | S21 | not stated | molded | n/a | not stated | n/a |
| LEGO stud 4.8 (measured 4.88 to 4.89) | C4, C5 | diameter | molded | n/a | ABS | n/a |
| MachineBlocks −0.1 plus 0.1 ribs | C6 | per side | not stated | not stated | not stated | not stated |
| Clutch rib 0.10, arc at least 0.8 | C7 | per side | X2D (planned, never printed) | 0.4 | PLA | 0.2 |
| Repeatability σ about 0.02 | C9 | not stated | see lego-lab §3.5 | not stated | not stated | not stated |

## 15. Search log

- Searched, among others: press-fit pin tolerance tests; the BASF snap-fit manual; crush ribs
  for printed press fits (three wordings); snap-fit cantilever strain for PLA (Hubs, Fictiv);
  nophead's polyholes; Bambu Studio auto circle compensation; diamond locating pins; annular
  snap undercut strain (Bayer, Covestro); filament as a dowel pin; layer adhesion by print
  orientation; split or slotted printed pegs; seam bumps in small holes; tapered pegs and
  draft; the 1.6/2.67/3.7 hole-size claim (S27); the Bambu PLA Basic data sheet.
- The Bayer guide (S7) and the Bambu wiki page (S1) were downloaded and read as files; the rest
  went through the fetch tool.
- Fetched: S1 to S19 (19 pages; S1 also as raw HTML).
- Snippet or refused: S20 to S30 (11; Printables, MakerWorld and thewave.engineer returned
  403).
- Not fetched: Protolabs' snap-fit guide (search found it, no fetch was made this pass); the
  Bambu PLA Basic data sheet (S30); Fictiv's printed-snap page returned only an index.
- Carried from earlier repo research, not fetched again: C1 to C9.
- None of the sources here measured a 2 mm stud on a Bambu X2D. Every number above is ported,
  and each says whether it transfers.
