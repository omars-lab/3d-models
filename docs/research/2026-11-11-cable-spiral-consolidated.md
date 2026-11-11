---
date: 2026-11-11
produced-by: "checker pass (Claude subagent), consolidating #1020 and #1021"
feeds: docs/design/pieces/cable-spiral-design.md (PR #1023)
---

# Cable spiral: the checked, consolidated research

**What this is.** Omar wants our own "top-open cable spiral": a thin, stackable part that a cable is
pressed into so it stays put, printed in PLA on the X2D (0.4 mm nozzle, 0.20 mm layers, no
supports). Two research passes answered the question on their own, without reading each other:

- Pass A, PR #1020: docs/research/2026-11-11-cable-spiral-a.md and
  docs/research/2026-11-11-cable-spiral-a-recommendation.md, on branch research/cable-spiral-a.
- Pass B, PR #1021: docs/research/2026-11-11-cable-spiral-b.md and
  docs/research/2026-11-11-cable-spiral-b-recommendation.md, on branch research/cable-spiral-b.

Those four files live on their own PRs and are not copied or changed here. This note re-opens the
sources behind the claims that decide the design, marks where the passes agree and disagree, and
settles the numbers the design doc will start from. The downloaded holder and clips already queued
are on the [cables-1](../design/plates/cables-1.md) plate, which has not been printed, so nobody
has grip data of our own yet.

**How sources are marked.** *Re-opened* means I downloaded the page on 2026-11-11 and read the
quoted line myself. *Closed* means the page answered with a bot check (HTTP 403) and I did not try
to get round it. *Snippet* means I saw only a search-engine summary. Every "Suggested:" number is a
starting point for the first test print, not a settled value.

## In short

- **The shape.** Both passes picked the same shape: a flat disc with an open spiral groove on top.
  The cable is pressed down past a narrow mouth into the groove. This note keeps that shape.
- **The cable path.** B's path wins: the cable is folded at its middle into an S-bend at the
  centre, then runs out along two side-by-side spirals, so both plugs leave at the rim. A plug head
  is 6.3 to 6.4 mm thick (re-opened), which is about as thick as the whole disc, so a plug cannot
  sit in the middle of a stack.
- **The stack.** B's stack wins: each disc's flat underside closes the grooves of the disc below it,
  and a low ring at the rim keeps the discs lined up. A's centre stub and pocket sits exactly where
  the S-bend has to go, and its pocket roof is a 10.4 mm bridge.
- **The thickness.** Both passes' thicknesses are off. A's 4.7 mm leaves no height for its own
  lead-in. B's 6.8 mm carries extra floor and headroom. Suggested: **1.3 × d + 1.0 mm** (6.2 mm for
  a 4 mm cable), where d is the cable's diameter. A thinner variant at **d + 1.0 mm** (5.0 mm) goes
  on the same test piece, because thinner means a shorter wall that bends harder.
- **One disc per cable size.** A groove grips cables in a band from about 0.94 to 1.1 times the
  size it was drawn for. Three sizes cover 3.0 to 5.0 mm cables.
- **Prior art.** All three pages stayed closed. The search text for MakerWorld 3056379 describes a
  disc with an S-shaped slot and plugs left outside, which is B's layout. No page shows whether
  its slot is open on top.

## 1. The load-bearing claims, re-opened

### 1.1 Cable diameters

| Claim | Who made it | What the source says, quoted | Verdict |
|---|---|---|---|
| Apple's 1 m USB-C cable is about 3.0 mm, and the 2 m one about 3.5 mm | Both agree | Apple Community thread 253788184 (re-opened): "the standard USB-C to USB-C 1m cable, supplied with a recently obtained iPad Pro 12.9, is ~3.0mm. The optional 2m USB-C cable is slightly larger at ~3.5mm diameter." The accepted answer hedges: "different suppliers may use cables that vary, slightly, in physical dimensions." Another user: "I don't believe the diameter of the cable is a published specification." | Holds, as one user's measurement. |
| StarTech 240 W USB-C is 4.0 mm, and its plug is 12.2 × 6.4 mm | Only B. Flagged. | StarTech USB2EPR3F datasheet (re-opened): "O.D.: 0.16in (4.0mm)" and "Cable OD 0.2 in [4 mm]". The 12.2 and 6.4 mm come from "Product Width 0.5 in [12.2 mm]" and "Product Height 0.3 in [6.4 mm]". | The diameter holds. The datasheet calls the 12.2 × 6.4 mm the product's width and height, not the plug's. Reading it as the plug is a fair inference, and Anker's figure below backs it. |
| Anker 515 (A8487) is 4.7 mm | Only A. Flagged. | Anker FAQ (re-opened): "The outside diameter is (OD) 4.7 mm. The USB-C head cover is 6.3 mm thick, and the width is 12.15 mm." | Holds. Neither pass used the plug size on this page, but it decides where the plugs go (section 3.6). |
| Apple 240 W USB-C is about 4.6 mm | Only A. Flagged. | ChargerLAB teardown (re-opened): "the diameter is about 4.6mm (0.18 inches), which is pretty thick." | Holds. The method is not stated. |
| Earbud wire is 2.0 mm | Only B, and snippet only. Flagged. | Not re-opened. | Snippet evidence. Earbud wire is far below the other cables, so it would need its own size. |
| Laptop barrel-plug cord | Both found no figure | None | Still unknown. Omar's own cables need measuring with calipers. |

**What this gives us.** The sourced phone and laptop USB-C cables run from **3.0 to 4.7 mm**
(re-opened). Snippets reach 4.8 to 5 mm for braided 240 W cables. A plug head is **6.3 to 6.4 mm
thick and about 12.2 mm wide** (Anker re-opened, StarTech inferred).

### 1.2 How far PLA stretches

| Claim | Who made it | What the source says, quoted | Verdict |
|---|---|---|---|
| Bambu PLA Basic breaks at 12.2% along the layers and 7.5% across them | Both agree | [Bambu PLA Basic data sheet V2.0](https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PLA_Basic_Technical_Data_Sheet.pdf) (re-opened): "Breaking Elongation Rate (X-Y) … 12.2 ± 0.4%" and "Breaking Elongation Rate (Z) … 7.5 ± 0.3%". Its conditions: "Infill Density 100%" and "*All the specimens were annealed and dried at 55 °C for 8 hours before testing." Its disclaimer: "the values are for design reference and comparison only." | Holds. These are break values from solid, annealed test bars, not working values, and both passes say so. |
| Bambu's stiffness: bending modulus 2750 / 2370 MPa (A); Young's modulus 2680 / 2160 MPa and tensile strength 39 / 35 MPa (B) | Each pass quoted different rows | Same sheet: "Bending Modulus (X-Y) … 2750 ± 60 MPa", "Bending Modulus (Z) … 2370 ± 50 MPa", "Young's Modulus (X-Y) … 2680 ± 130 MPa", "Young's Modulus (Z) … 2160 ± 90 MPa", "Tensile Strength (X-Y) … 39 ± 2 MPa", "Tensile Strength (Z) … 35 ± 3 MPa". | All hold. |
| Fictiv: PLA's acceptable strain is 4 to 8% | Both agree | Fictiv's own page was closed (403). The same article is republished on [Core77](https://www.core77.com/posts/65318/how-to-design-snap-fit-components) (re-opened), where the strain table is a picture. I read the picture: "PLA 4-8%", next to "ABS 7%" and "Nylon 4-15%". No test standard or source is given for it. | Holds, with no stated basis. |
| Fictiv: halve the strain for an arm built up the Z axis | Both agree. B words it as "may drop by about 50%" | Core77 copy (re-opened): "If your cantilever can only be created in the Z axis, be aware elongation at break is reduced by 50% and tensile strength by 20-30%. We recommend reducing the allowable stress/strain by 50% for Z axis cantilevers." | Holds. The source says "is reduced", not "may drop". B softened it, which does not change the number. |
| The beam formula, strain = 1.5 × t × Y / (L² × Q) | Both agree. Both saw it garbled | Core77 copy, formula picture (re-opened): "MAXIMUM STRAIN (@ BASE) ∈ = 1.5 tY / L²Q", with t the beam thickness, Y the deflection, L the beam length and Q a "Deflection Magnification Factor". The text says "for a simple casing, leave Q as 1." | Holds. It also follows from textbook beam theory: a beam fixed at one end and pushed sideways by Y at a height L has a root strain of 1.5·t·Y/L². |

**The working range both passes use.** Fictiv's 4 to 8%, halved for a wall bent across its layers,
gives **2 to 4%**. Both numbers are now re-opened, but the 4 to 8% has no stated basis, so the band
is a starting range and not a tested limit. The one hard ceiling is Bambu's 7.5% break value.

### 1.3 Overhangs and bridges

| Claim | Who made it | What the source says, quoted | Verdict |
|---|---|---|---|
| Bambu's limits: overhang 55°, bridge 30 mm | Both agree | Bambu data sheet (re-opened): "Max Overhang Angle 55°" and "Max Bridging Length 30 mm". It does not say what the angle is measured from. | Holds. A's caution stands: the sheet gives no convention. The word "Max" reads most naturally as measured from upright, where bigger is harder, but that is my reading, not the sheet's. |
| A 45° lip underside is "inside what all three sources allow" | B. Flagged as partly wrong | [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) (re-opened): "Depending on the material, an overhang can usually be printed up to 45° without compromising quality. At 45°, the newly printed layer is supported by 50% of the previous layer." [Prusa](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) (re-opened): "A 3D printer can cleanly print overhanging structures with an angle between 45 and 60 degrees, depending on your nozzle diameter and settings." | 45° is backed by Hubs and Prusa. It is not backed by Bambu's sheet, which gives no convention. 45° from upright and 45° from flat are the same slope, so it is safe under any reading that allows 45° at all. |
| Bridges sag unless shorter than 5 mm | Only B. Flagged. | Hubs (re-opened): "sagging or marks from support material are to some extent always present unless the bridge is less than 5mm." | Holds. Hubs (5 mm, no sag or marks) and Bambu (30 mm, the most it will span) answer different questions. A's 10.4 mm pocket roof passes Bambu's limit but not Hubs'. |
| Put a chamfer, not a round, on edges touching the bed | Only B. Flagged. | Hubs (re-opened): "Include a 45° degree chamfer or radius on all edges of an FDM part touching the build plate." Prusa (re-opened): fillets facing the bed make "a very steep overhang … use chamfer instead". | Holds. |
| Thinnest wall: one line, about 0.45 mm | Only B. A cites Prusa's Arachne page for the same point. | Prusa (re-opened): "0.4 mm, which in PrusaSlicer has an extrusion width of 0.45 mm". | Holds for PrusaSlicer. I did not check the X2D profile's line width. |
| Accuracy and fit gaps | Only B. Flagged. | Prusa (re-opened): "An Original Prusa will be accurate to at least 0.2 mm" and "An initial good measurement for movable parts is at least 0.3 mm." | Holds for a Prusa. It carries to the X2D only as a starting guess. |
| Snap-fit starting values: undercut 0.5 to 1.2 mm, lead-in 25° to 35°, gap 0.20 to 0.40 mm a side, 20 to 30 press cycles, PLA creeps | Only A. Flagged. | [Sovol](https://www.sovol3d.com/blogs/news/3d-printed-snap-fit-joints-how-to-design-clips-that-work) (re-opened): "an initial starting undercut depth of 0.5 mm to 1.2 mm", "a starting lead-in angle of 25° to 35°", "an initial clearance tolerance offset of 0.20 mm to 0.40 mm per side", "Disengage and re-engage the clip 20 to 30 consecutive times", and PLA is "susceptible to creep under load". | Holds, as "starting test" values for a free snap arm, not an upright groove wall. |

### 1.4 The mouth width as a share of the cable

| Claim | Who made it | Source | Verdict |
|---|---|---|---|
| A clip opening of 0.70 to 0.85 of the cable, "a lower value grips the cable more firmly but takes more force" | Only B. Flagged. | MakerWorld 2887515 was closed to me (403). A fresh search summary repeats it: an "opening factor that determines how wide the top of the clip is open (value between 0.70 and 0.85)", and a smaller value "requires more force to push in". | Snippet only, from two separate searches. It also comes from a clip that flexes along its layers, which our upright wall cannot do, so it carries over only as the band to test. |
| The press-in clip on cables-1 has a 2.5 mm mouth over a 4.0 mm bore, 0.62 | Only A. Flagged. | Measured by A from the maker's mesh. I did not re-measure it. | Not re-checked. It is mouth over bore, not mouth over cable, so it does not line up with A's own 0.83 or B's 0.80. If the bore fits the cable closely, the two are about the same. |
| A clip adds 0.6 mm of room around the cable, with a 20° hook | Both agree | MakerWorld 3436380 was closed to me (403). Both passes read the page. | Two passes agree on it, but it is not re-opened. It comes from a lidded clip. |

**Where this leaves the mouth.** A wrote the mouth as **d − 0.6 mm** (0.83 of a 3.5 mm cable). B
wrote it as **0.80 × d**. For a 3.5 mm cable they nearly agree. A's fixed 0.6 mm drifts from 0.80
of a 3 mm cable to 0.87 of a 4.7 mm one, so the grip would change with cable size. B's share of the
cable keeps it even, and it matches the only source band we have. **Settled: mouth = 0.80 × d**,
and the test piece tries 0.75, 0.80 and 0.85.

### 1.5 The bending arithmetic, redone

The wall between two grooves stands up from the floor. The cable pushes its top sideways by
Y = (d − mouth) / 2. The stretch at the wall's foot is 1.5 × t × Y / L², where t is the wall's
thickness and L is the height where the cable pushes. The stretch at the foot runs up and down,
across the layer lines, so the halved band and the 7.5% break value apply. Both passes say so.

| Case | t | Y | L | Stretch | Pass's figure |
|---|---|---|---|---|---|
| A's wall, 3.5 mm cable | 0.9 | 0.3 | 4.1 | 2.41% | A: 2.4%. Correct. |
| A's first example | 0.8 | 0.3 | 4.0 | 2.25% | A: 2.25%. Correct. |
| A's shorter wall | 0.9 | 0.3 | 3.5 | 3.31% | A: 3.3%. Correct. |
| B's wall, 4 mm cable, push at the middle of the lip | 0.8 | 0.4 | 5.0 | 1.92% | B: 1.9%. Correct. |
| B's range, push at the lip's underside or top | 0.8 | 0.4 | 4.4 or 5.6 | 2.48% or 1.53% | B: 2.5% or 1.5%. Correct. |
| B's wall, push at the lip tip, where the push is largest | 0.8 | 0.4 | 5.1 | 1.85% | Not given. |

Both passes' sums are right. Two cautions apply to all of them:

- **The formula treats the wall as a lone strip, and it is not one.** The cable pushes one short
  stretch of a long, continuous wall, and the next turn may hold a cable on the far side. The push Y
  is set by the shapes, so a stiffer wall does not bend less. It pushes back harder, and the
  cable's jacket squashes more. Whether the strip figure is high or low for the real wall is
  unknown. Treat it as a way to rank options, not as a safety margin.
- **Breaking stretch is not a working value.** Only the print can show whether a lip survives being
  pressed every day.

## 2. The prior-art pages

All three pages answered an ordinary download with HTTP 403, a bot check, on 2026-11-11. I did
not try to get round it. What is known about them is snippet-only.

| Page | What a search summary says | What it means for us |
|---|---|---|
| [Printables 302991, "Spiral cable organizer"](https://www.printables.com/model/302991-spiral-cable-organizer) | "a spiral organizer meant to hold at least two cables, such as a power cord and a network cable. It could hold three cables, but they need to go in the correct order, with the thickest one first." | Its shape is unknown. Pass B also read the maker's words through Printables' data service, which I did not repeat. In B's reading it is printed "with supports" at 100% infill, which an open-top groove would not need. That is B-only and not re-opened. |
| [Printables 1430486, "Spiral cable organizer"](https://www.printables.com/model/1430486-spiral-cable-organizer) | The same description as 302991, from the same maker. | Likely a re-upload of 302991. |
| [MakerWorld 3056379, "Data Cable Spool Storage Box"](https://makerworld.com/en/models/3056379-data-cable-spool-storage-box) | "a disc-shaped winding structure with a built-in S-shaped hollow threading slot and reserved outlets at both ends"; the disc and slot are "formed in a single print", with no supports; it holds "two charging cables" with "the plugs exposed after storage". | The closest prior art either pass found. It backs B's S-bend with both plugs outside the disc. "Hollow" may mean the slot is closed on top, so it may not be top-open. |

None of the sources either pass read shows, in words or pictures they could see, an open-topped
groove disc that a cable is pressed into and that stacks. That is a claim about the roughly 40
sources in the two passes, not about the web. The shape is our own until one of these pages opens.

## 3. The settled design numbers

All sizes are in mm, and **d** is the cable's diameter, measured on Omar's own cable. Worked values
are for a 4.0 mm cable (StarTech, re-opened).

### 3.1 The groove, in terms of d

| Part | Formula | 4 mm cable | Sourced or guess |
|---|---|---|---|
| Groove width, w | d + 0.4 | 4.4 | **Guess to test.** It sits between A's zero gap and B's 0.6 mm, and it gives Sovol's 0.2 mm a side (re-opened, "per side between all non-locking mating faces"). A's zero gap is a mistake. A printed slot comes out a little narrow, so the cable would press on the walls all the time, and Sovol warns that PLA creeps under steady load. |
| Mouth, m | 0.80 × d | 3.2 | The 0.70 to 0.85 band is snippet-only (MakerWorld 2887515). 0.80 is the middle of it. **Test 0.75, 0.80 and 0.85.** |
| Push on each wall, Y | (d − m)/2 = 0.1 × d | 0.4 | Arithmetic. |
| Lip, how far it reaches in | (w − m)/2 = 0.1 × d + 0.2 | 0.6 | Arithmetic. |
| Lip underside | 45° from upright, so its height equals its reach | 0.6 tall | Hubs and Prusa, re-opened (section 1.3). |
| Lip tip height above the floor | d + (0.1 × d + 0.2) = 1.1 × d + 0.2 | 4.6 | Arithmetic. The underside starts at the wall at height d, so a cable resting on the floor never touches it. |
| Lead-in above the tip | 0.2 × d tall, sloped to open the mouth back toward the cable's width | 0.8 | Its height is geometry: a cable lifted until it meets the lip tips has its top 0.2 × d above them (at a 0.80 mouth, the top sits d/2 × (1 − √(1 − 0.8²)) = 0.2 × d above the tips). So a lead-in this tall keeps a lifted cable inside the disc's top face, and the disc above can close it. The slope angle is a **guess to test**. Sovol's 25° to 35° (re-opened) is a starting value. |
| Floor | 0.8 (four layers) | 0.8 | **Guess to test.** It sits between A's 0.6 and B's 1.2. |
| Wall between turns, t | 0.8 (two lines) | 0.8 | **Guess to test.** One line, about 0.45, is the least that prints (Prusa, re-opened). |
| Total thickness, T | floor + tip height + lead-in = **1.3 × d + 1.0** | **6.2** | Arithmetic on the rows above. |
| Stretch at the wall's foot | 1.5 × t × 0.1d / (1.1d + 0.2)² | 2.27% | Arithmetic. It sits inside Fictiv's halved 2 to 4% band (re-opened) and under Bambu's 7.5% break value (re-opened). |

**A's and B's sections run through the same check.**

- **A's 4.7 mm section has no room for its lead-in.** Its 0.3 mm lip with a 30°-from-upright
  underside is 0.52 mm tall. Its groove is 4.1 deep for a 3.5 mm cable, so the lip tip sits at 4.02
  and leaves 0.08 mm, less than half a layer, for the 30° lead-in its own table lists. Its zero gap
  also loads the walls all the time.
- **B's 6.8 mm section works, but carries extra height.** It has a 1.2 floor, 0.4 of headroom over
  the cable, and a 1.2 lip. Its lead-in, 0.5 tall, is just under the 0.2 × d = 0.8 a lifted 4 mm
  cable needs. So a lifted cable's top could stand 0.3 mm above the disc. The disc stacked on top
  would push it back down, so this matters only for the top disc.

### 3.2 How thin it can go

A thinner disc means a shorter wall, and a shorter wall stretches more for the same push. The
other way to thin it is to put the lip tip lower, at about 0.8 × d + 0.2. That is the lowest a tip
can sit and still clear a cable resting on the floor, with 0.2 mm to spare. The disc is then
**d + 1.0** thick.

| Cable d | Suggested (tip high): thickness | stretch, 0.8 wall | Thin variant (tip low): thickness | stretch, 0.8 wall | stretch, 0.45 wall |
|---|---|---|---|---|---|
| 3.0 | 4.9 | 2.9% | 4.0 | 5.3% | 3.0% |
| 3.5 | 5.6 | 2.6% | 4.5 | 4.7% | 2.6% |
| 4.0 | 6.2 | 2.3% | 5.0 | 4.2% | 2.3% |
| 4.7 | 7.1 | 2.0% | 5.7 | 3.6% | 2.0% |

All stretch figures come from the strip formula, with its cautions (section 1.5).

**The thinnest disc that holds the thickest cable.** The thickest re-opened cable is 4.7 mm
(Anker). Suggested: **7.1 mm**, with two-line walls and the stretch inside the 2 to 4% band. A
**5.7 mm** disc is possible with a single-line wall (0.45 mm), at the same 2.0% stretch. That wall
is far softer, about a sixth as stiff as a 0.8 mm one, so whether it still grips is untested. The
thin variant with a two-line wall reaches 3.6 to 5.3%, over the band for small cables. The test
piece settles which of the two wins.

### 3.3 One disc per cable size

A groove drawn for a cable of size d₀ grips a cable d when the mouth (0.80 × d₀) is 0.70 to 0.85 of
d, and the cable still fits the groove (d ≤ d₀ + 0.4). That gives a band from about **0.94 × d₀ to
d₀ + 0.4**:

| Drawn for | Grips cables of about | Disc thickness (suggested) |
|---|---|---|
| 3.2 | 3.0 to 3.6 | 5.2 |
| 3.9 | 3.7 to 4.3 | 6.1 |
| 4.6 | 4.3 to 5.0 | 7.0 |

So **yes, one disc per cable size**, and three sizes cover the 3.0 to 5.0 mm USB-C range. Earbud
wire, about 2 mm (snippet), would need a fourth size. The band rests on the snippet-only 0.70 to
0.85, so it is a guess until the test piece shows how far a groove's grip really reaches. The
design should take d as its one setting, so a size is printed for each measured cable.

### 3.4 The wall between turns

Suggested: **0.8 mm, two lines**, a guess to test. Both passes landed here: A on 0.9, B on 0.8. A
thicker wall grips harder and stretches more. The test piece tries 0.45, 0.8 and 1.2.

### 3.5 Disc diameter and how much cable it holds

The cable is folded at its middle. The fold sits in an S-bend at the centre, which is two
half-loops of radius ρ. Two spirals then run outward side by side, and each turn of groove takes
w + t = **d + 1.2** of radius.

- **The centre.** The S-bend needs a clear centre of radius 2ρ. Suggested: ρ = 2.5 × d (10 mm for a
  4 mm cable). This is a **guess to test**: no source gives a USB-C cable's tightest bend.
- **Cable held.** The S holds 2πρ. The spirals hold π(R² − (2ρ)²)/(d + 1.2), where R is the radius
  to the outermost groove.
- **The rim.** 2.0 mm, from B's reading of Printables 601730's wall. That source is B-only and not
  re-opened, so treat 2.0 mm as a guess.

| Cable d | Disc across for 1 m | Disc across for 2 m | Cable on an 80 mm disc |
|---|---|---|---|
| 3.0 | 81 mm | 111 mm | 0.96 m |
| 3.5 | 87 mm | 117 mm | 0.82 m |
| 4.0 | 92 mm | 124 mm | 0.69 m |
| 4.7 | 100 mm | 133 mm | 0.55 m |

**B's disc size was too small.** B's table used a 12 mm centre radius, but its own S-bend
half-loops, "about 10 to 12 mm in radius", need a centre radius of 20 to 24 mm. Redone with B's own
pitch of 5.4 mm and the same sum as the table above (counting the cable in the S-bend), 1 m of 4 mm
cable needs a disc about 94 to 97 mm across, not B's 90 mm. With the S-bend left out, as B's sum
does, it is 96 to 100 mm. A's 0.8 m on an 80 mm disc is right for its own layout,
a single spiral from a 14 mm centre. That layout leaves the inner plug in the middle.

**Suggested: one size for 1 m cables, about 90 to 100 mm across**, which is about the size of a
coaster. A 2 m cable needs a disc 110 to 135 mm across.

### 3.6 Where the plugs go

**Both plugs go out at the rim**, through two notches cut down through the rim, each as wide as the
groove (w). The plug heads hang outside the disc. This is B's layout, backed by the snippet for
MakerWorld 3056379 ("the plugs exposed after storage").

- A plug head is 6.3 mm thick and 12.15 mm wide (Anker, re-opened). That is as thick as the 6.2 mm
  disc for a 4 mm cable, so it cannot sit in the middle of a stack. This settles A's open question
  against a centre exit.
- B said a plug pocket "would need a disc about twice as thick" as its 6.8 mm disc. That does not
  follow for B's disc. A pocket needs the plug plus a floor, about 7.2 mm, only a little thicker. For
  a thin disc made for a 3 mm cable (4.0 to 4.9 mm), the same pocket is 1.5 to 1.8 times the
  thickness. Either way it is not worth it, because the plugs at the rim stay outside the stack.
- **Stagger the notches in a stack.** For cables under about 4 mm the disc is thinner than the
  6.3 mm plug, so plugs hanging from two neighbouring discs would hit each other if their notches
  lined up. The rim ring is round, so each disc can be turned. Turn each one so its notches miss the
  ones on the disc below.

### 3.7 How discs stack and stay lined up

**Suggested: B's stack.** Each disc's flat underside rests on the wall tops of the disc below and
closes its grooves, so a stacked cable cannot lift out at all.

- **Lining up.** A ring 0.4 mm tall around the outer edge of the top face, with a 45° inner face. It
  sits inside a 0.6 mm 45° chamfer on the bottom edge of the disc above. The ring is 0.2 mm shorter
  than the chamfer, so it never holds the disc above off the walls. 0.2 mm is Prusa's stated
  accuracy (re-opened, "accurate to at least 0.2 mm"). Both sizes are **guesses to test**.
- **The bottom chamfer.** It is sourced: Hubs and Prusa, re-opened, both say to chamfer the edges
  touching the bed.
- **No bridges at all.** The underside is flat.
- **Thickness per disc.** The disc's own thickness. The ring tucks into the chamfer above it.

**Why not A's stack.** A puts a 10 mm stub on top and a pocket underneath. The stub sits where the
S-bend must go, so it cannot be combined with rim exits for both plugs. Its pocket roof is a
10.4 mm bridge, which is over Hubs' 5 mm for a clean, sag-free roof (re-opened), though inside
Bambu's 30 mm. A also leaves the grooves open on every disc, while B closes all but the top one.

## 4. The first test piece

Not a whole disc. Following the repo's habit of testing pieces rather than whole shapes:

**Suggested:** one flat strip of straight groove runs, each about 40 mm long, with a carved id on
each. All are for one cable Omar measures first, or d = 4.0 mm until he does.

1. Mouth 0.75, 0.80 and 0.85 × d, tip high, 0.8 wall. This tests the grip band.
2. A plain groove with no lip, as the control.
3. The thin variant, tip low, with a 0.8 wall and with a 0.45 wall, at the 0.80 mouth. This tests
   how thin it can go.
4. Tip high with a 1.2 wall, at the 0.80 mouth, with a full groove beside it. This tests a shared
   wall with a neighbour holding a cable.
5. One curved run at the S-bend radius, ρ = 2.5 × d, at the 0.80 mouth. A curved wall is stiffer,
   and the S-bend is the tightest curve.
6. Two short stacking coupons with the rim ring and bottom chamfer. These test whether one sits
   flat on the other and stays lined up.

**The question after the print.** Press the cable into each run, then pull it up. Which take it
with a thumb press and hold it until pulled? Repeat 20 to 30 times (Sovol's cycle test). Look for a
cracked or bent wall at the foot.

The [cables-1](../design/plates/cables-1.md) plate is still unprinted. Its holder and clips could
share the bed, so one print answers both: how the bought designs grip the same cable, beside ours.

## 5. Where the passes stood

**Both agree.**

- The reading: a flat disc with an open spiral groove that the cable is pressed into.
- A press-in mouth narrower than the cable.
- The wall bends across its layers, so Fictiv's halving applies.
- The Bambu figures, Fictiv's 4 to 8%, and Apple's 3.0 and 3.5 mm.
- MakerWorld 3436380's 0.6 mm gap.
- PLA creeps, with PETG as the usual fix.
- Test a piece first, not a whole disc.

**They disagree. The verdict and its source:**

| Point | A | B | Which side the source supports |
|---|---|---|---|
| Thickness | 4.7 mm for a 3.5 mm cable | 6.8 mm for a 4 mm cable | Neither as written. A's lead-in does not fit. B carries extra floor and headroom. Suggested: 1.3 × d + 1.0 (section 3.1). |
| Stacking | Centre stub and pocket | Flat underside closes the grooves, with a rim ring | B: no bridge (Hubs, 5 mm), and it leaves the centre free for the S-bend. |
| Mouth | d − 0.6 | 0.80 × d | B: a share of the cable keeps the grip even across sizes and matches the only band found (snippet). |
| Gap beside the cable | 0 | 0.6 | Neither. 0.4 gives Sovol's 0.2 mm a side and avoids a steady load on the walls. |
| Lip underside | 30° from upright | 45° | B's 45° is backed by Hubs and Prusa. A was right that Bambu's sheet alone does not settle it. |
| Floor | 0.6 | 1.2 | No source for either. 0.8 is a guess to test. |
| Stretch estimate | 2.4% | 1.9% | Both sums are right for their own walls. |
| Plugs | Left open | Out at the rim through an S-bend | B: plug heads are 6.3 to 6.4 mm thick (re-opened). |

**Found by only one pass. Flagged, not dropped:**

- **Only A:** the measured cables-1 clip (0.62 mouth over bore) and holder springs (0.75 mm, drawn
  flat). Anker 4.7 mm and ChargerLAB 4.6 mm. Sovol's starting values. The doubt over Bambu's
  overhang convention. A's bending-modulus row.
- **Only B:** the S-bend and two spirals. StarTech's 4.0 mm and its product size. The 0.70 to 0.85
  mouth band (snippet). Earbud wire at 2 mm (snippet). Hubs' 5 mm bridge and bed-edge chamfer.
  Prusa's 0.45 mm line and 0.2 mm accuracy. Printables 601730's ridge-and-groove stack and 2 mm
  wall. The curved-wall test run. The Printables texts read through its data service, none of which
  I re-opened.

## 6. Claims found wrong or unsupported

1. **A's 4.7 mm thickness does not fit its own lip.** Only 0.08 mm of height is left above the lip
   tip for the 30° lead-in it lists.
2. **A's zero gap between the cable and the groove walls.** It contradicts Sovol's 0.2 to 0.4 mm a
   side (re-opened) and keeps a creeping PLA wall under load all the time.
3. **A's centre stub.** It cannot sit where the S-bend goes, and its 10.4 mm pocket roof is over
   Hubs' 5 mm for a clean roof.
4. **A's mouth ratio comparison.** The cables-1 clip's 0.62 is mouth over bore, not mouth over
   cable, so it is not like for like with A's own 0.83.
5. **B's disc size.** Its capacity sum used a 12 mm centre that its own S-bend cannot fit in. 1 m of
   4 mm cable needs about 94 to 97 mm, not 90.
6. **B's plug pocket "about twice as thick".** Against B's own 6.8 mm disc, a pocket needs only
   about 7.2 mm. It is 1.5 to 1.8 times as thick only for the thinnest discs.
7. **B's "45° is inside what all three sources allow".** It is inside Hubs and Prusa. Bambu's sheet
   gives no convention, so it does not confirm 45°.
8. **B's lead-in.** At 0.5 mm it is just short of the 0.8 mm a lifted 4 mm cable needs, so on the top
   disc a lifted cable can stand slightly proud.
9. **B's "may drop by about 50%".** Fictiv says it "is reduced by 50%". The number is unchanged.
10. **B's plug size.** The 12.2 × 6.4 mm is StarTech's "Product" width and height. Reading it as the
    plug is a fair inference, and Anker's explicit "head cover is 6.3 mm thick" confirms it.

## Sources re-opened by this pass

- Bambu PLA Basic technical data sheet V2.0:
  https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PLA_Basic_Technical_Data_Sheet.pdf
- Fictiv's snap-fit article, as republished on Core77, including its strain-table and formula
  pictures: https://www.core77.com/posts/65318/how-to-design-snap-fit-components (Fictiv's own page,
  https://www.fictiv.com/articles/how-to-design-snap-fit-components, answered 403)
- Sovol, snap-fit joints:
  https://www.sovol3d.com/blogs/news/3d-printed-snap-fit-joints-how-to-design-clips-that-work
- Prusa, modeling with 3D printing in mind:
  https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
- Hubs, designing parts for FDM:
  https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
- StarTech USB2EPR3F datasheet: https://media.startech.com/cms/pdfs/usb2epr3f_datasheet.pdf
- Apple Community thread 253788184: https://discussions.apple.com/thread/253788184
- Anker 515 FAQ: https://service.anker.com/article-description/Anker-515-USB-C-to-USB-C-cable-FAQ
- ChargerLAB, Apple 240 W cable teardown:
  https://chargerlab.com/teardown-of-apple-240w-usb-c-charge-cable-a2794

Closed (403), and seen as snippets only: Printables 302991 and 1430486, MakerWorld 3056379,
2887515 and 3436380.
