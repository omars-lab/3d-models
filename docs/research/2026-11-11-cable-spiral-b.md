---
date: 2026-11-11
produced-by: "research pass B (Claude subagent)"
feeds: "docs/design/products/cable-spiral-design.md (not yet written)"
---

# Cable spiral: raw findings, research pass B

This file holds what research pass B found about a "top-open cable spiral": our own part that a
cable is wrapped around or pressed into so it stays put, thin and stackable, printed in PLA on the
X2D (0.4 mm nozzle, 0.20 mm layers, no supports). The design proposal built on it is in
[2026-11-11-cable-spiral-b-recommendation.md](2026-11-11-cable-spiral-b-recommendation.md). The
downloaded holder and clips already queued are on the plate page
[cables-1](../design/plates/cables-1.md); that plate has not been printed, so we have no grip data
of our own yet.

## How the sources were read, and what was not searched

Each source is marked:

- **fetched**: I read the page itself.
- **fetched (API text)**: I read the model's description text through Printables' public data
  service (`api.printables.com/graphql`), because the web page sat behind a bot check. I saw the
  maker's words but **none of the pictures**, so any shape not stated in the words is unknown.
- **snippet**: seen only as a search-result summary. The page itself did not load: MakerWorld,
  3dgo.app and Printables web pages all returned a bot check or 403 on 2026-11-11. One MakerWorld
  page did load in a browser (3436380, below).

Not searched: Thingiverse directly (only through search results), YouTube or other videos,
Amazon listings directly, and any patent. So every "none of" below is about the sources listed
here and nothing wider.

## 1. Shapes that exist

### What was found

| Source | What it is, in the maker's words | Status |
|---|---|---|
| Printables 302991 "Spiral cable organizer" <https://www.printables.com/model/302991-spiral-cable-organizer> | "allow at least 2 cable. A power cord and network ... put in those in the correct order. First the most thick and then the others." Printed **with supports**, 100% infill. The text never says what the shape is. | fetched (API text) |
| Printables 1430486 "Spiral cable organizer" <https://www.printables.com/model/1430486> | Same summary text as 302991, likely a re-upload. | fetched (API search summary only) |
| Printables 1702919 "USB Cable Spiral Ring Cord Organizer with Cutouts" <https://www.printables.com/model/1702919> | Summary: "An approximately 80mm diameter ring to accommodate a rolled up, wrapped, spiraled cord". Description empty. | fetched (API text) |
| Printables 533022 "Spiral Cable Guide" <https://www.printables.com/model/533022> | Summary: "Cable holder with spiral slit - supportless print". No further words. | fetched (API text) |
| Printables 320902 "Spiral Cable Holder" <https://www.printables.com/model/320902> | "Cables can slip right in and out. Base is designed to be the width of a Command Strip ... printed with PLA with no supports." | fetched (API text) |
| Printables 122384 "Cable clip - spiral" <https://www.printables.com/model/122384> | "Simple spiral cable clips ... use 4 perimeters to make it flex and strong ... several sizes (starting radius 6mm/8mm/10mm)." A spiral-shaped clip that bundles cables, not a winder. | fetched (API text) |
| Printables 1503885 "Cable clamp spiral" <https://www.printables.com/model/1503885> | Summary: "a spiral to hold a few cables together". | fetched (API search summary only) |
| MakerWorld 3056379 "Data Cable Spool Storage Box" <https://makerworld.com/en/models/3056379-data-cable-spool-storage-box> | Search summaries: "a disc-shaped winding structure with a built-in S-shaped hollow threading slot and reserved outlets at both ends"; "entire disc and internal S-shaped wire slot are formed in a single print, with no supports"; "one spool can accommodate two charging cables". "Hollow" may mean the slot is closed on top. | snippet |
| Printables 1037051 "Next Gen USB Cable Winder" <https://www.printables.com/model/1037051> | Two concentric rings "encapsulating the cable in its natural winding"; sizes Ø60, Ø80, Ø100 mm; "1 m of cable takes exactly 4 turns in the Ø80 mm versions"; "80×20 ... holds well a braided 1 m USB-C cable with Ø5 mm"; "80×24 catches up to 3 m of Ø4 mm cable". Plug cut-outs "USB-C 7×10.5 mm²", "USB-A 8×14 mm²". Separate stacking rings and base plates. | fetched (API text) |
| Printables 601730 "Parametric stackable cable organizer / winder" <https://www.printables.com/model/601730> | Print-in-place winder in a closed round box with snap clips; default cable 4 mm thick, 1.5 m; stacking by a ridge and groove (numbers in section 4). | fetched (API text) |
| Printables 1456960 "Stackable Cable Winder" <https://www.printables.com/model/1456960> | Print-in-place, no supports, 0.2 mm layers; "Standard ... up to approximately 1.5 m, ... Large ... up to approximately 2.0 m". No stacking method in the words. | fetched (API text) |
| Printables 436822 "Stackable Cable/Cord Winder Organizer" <https://www.printables.com/model/436822> | Threaded three-part winder; "the flat side of the base faces the cap while the indentation faces away so that the organizers can stack". 0.20 mm layers, 0.4 mm nozzle, no supports. | fetched (API text) |
| Printables 1827019 "Thin Stackable Cable Winder" <https://www.printables.com/model/1827019> | "A slim card ... connect to the wire's midpoint and turn to shorten." The cable is fixed at its middle and both ends leave at the edge. | fetched (API text) |
| Printables 56609 "USB Cable Winder Stackable (+Knurled) Print in Place" <https://www.printables.com/model/56609> | Print-in-place, "PETG recommended", no supports. Its color-change heights put the whole piece at about 38 mm tall. | fetched (API text) |
| Printables 246573 "Earbud Credit Card Style Wrap" <https://www.printables.com/model/246573> | A flat card cut-out to wrap earbud wires around; "STILL A WORK IN PROGRESS". | fetched (API text) |
| The Loop (product), review at <https://the-gadgeteer.com/2014/08/09/the-loop-review> | Search summary: "a 2.5-inch disc where you wind the cord, then secure the earbud ends in one of the front notches", polycarbonate. | snippet |
| All3DP, "USB cable organizer with a twist" <https://all3dp.com/4/tidy-up-and-3d-print-a-usb-cable-organizer-with-a-twist/> | Search summary: stacking rings that print together as one piece. | snippet |

### What this says about the readings

- **A flat disc with an open-topped spiral channel the cable is pressed into.** None of the 17
  sources above shows this in words I could read. The nearest is MakerWorld 3056379 (a disc with an
  S-shaped slot, two cables, both ends out at the rim), and that is a snippet whose "hollow" slot
  may be closed on top. The Printables "spiral cable organizer" (302991) could be this shape, but
  its text does not say, and it needs supports, which an open-topped groove would not.
- **A flat spool or ring the cable is wound around, with a lip.** Common: the Earbud Credit Card
  wrap, The Loop disc (snippet), the 80 mm ring 1702919, and every winder in the table (where the
  cable winds inside a closed box).
- **A spiral clip.** Exists (122384, 1503885, 533022): a small spiral that bundles or guides a few
  cables. It is not a holder you wind one cable onto, so it does not match "wrap a cable around".
- **Cable fixed at its middle, both ends out at the edge.** A recurring idea: 1827019 ("connect to
  the wire's midpoint"), 3056379 ("reserved outlets at both ends", snippet), and the Next Gen
  winder's plug cut-outs. It keeps the plugs out of the middle, which matters for thinness because a
  plug body is taller than the cable (section 3).

## 2. How the cable is held

### Numbers from cable clips (these flex in the plane of the layers, see the warning below)

| Figure | Source | Status |
|---|---|---|
| Opening "factor" 0.70 to 0.85 of the cable size; "a lower value grips the cable more firmly but takes more force to push it in" | MakerWorld 2887515, parametric cable clip, <https://makerworld.com/models/2887515> | snippet (page blocked by a bot check on retry) |
| Opening of 80% of the cable diameter, "small enough so that the cable doesn't come loose and large enough so that it's easy to insert" | search summary, no URL attributed | snippet, unattributed |
| Bore 0.5 to 1.0 mm larger than the cable; a 5 mm bore for a 4.2 mm cable, 3.8 mm for 3.2 mm | search summary, no URL attributed | snippet, unattributed |
| `cable_clearance` 0.6 mm default (range 0 to 2) "so the cable drops in easily"; `fin_height_ratio` 0.85 of cable diameter for the separators between cables; `fin_thickness` 1.6 mm; `barb` 1.4 mm; latch hook undercut 20°, "Keep it above ~12° or the lid can pry the latch open"; PETG recommended, "PLA works"; printed on its side "so the S-spring and the latch arm bend along their layers, not across them" | MakerWorld 3436380, "Parametric One-Piece Snap Cable Clip" <https://makerworld.com/en/models/3436380-parametric-one-piece-snap-cable-clip> | fetched |
| "Even heavier cables won't force the clip open even with a wall width of only 1.6 mm"; "PETG ... ABS/ASA or even PLA will work as well but may break if open/close cycled too often" | Printables 359285 KLAMMA <https://www.printables.com/model/359285> | fetched (API text) |
| "To maintain a secure clip, I recommend using materials that are CREEP RESISTANT. I always use ASA but PETG, PC, and fibre-filled materials should also work." Printed sideways, no supports, for 4 mm and 5 mm cables. "orient the clip so that any loading of the cable will pull it into the clip and away from the opening" | Printables 1410373 <https://www.printables.com/model/1410373> | fetched (API text) |
| Snap clamp "Printed in PETG for a good balance of strength and flexibility, essential for the 'snap-on' feature", 5 perimeters to start | Printables 1514154 <https://www.printables.com/model/1514154> | fetched (API text) |
| Snap clip bulge 0.7 mm wide; clip 2 mm thick; 0.2 mm gap so the clip can bend; groove wall 0.61 mm so every slicer prints one line; "The force required to open / close the winder depends on A LOT of parameters that are not imputable to the model design, such as: number of walls, infill density, infill pattern, material" | Printables 601730 | fetched (API text) |
| A notch-style cord clip "works okay but it would be better if it went a little deeper or if there was a stronger gate" (user review) | desertcart listing of the Side Winder product, via search | snippet |

**Hedge carried:** every clip number above is a maker's choice for their own part, not a tested
rule. None of them is for PLA walls standing up out of a disc.

### How far PLA can bend

| Figure | Source | Status |
|---|---|---|
| Bambu PLA Basic: breaking elongation **12.2 ± 0.4 % along the layers (X-Y)** and **7.5 ± 0.3 % across the layers (Z)**; Young's modulus 2680 MPa (X-Y), 2160 MPa (Z); tensile strength 39 MPa (X-Y), 35 MPa (Z). Test pieces were 100% infill, "annealed and dried at 55 °C for 8 hours before testing". "The values are for design reference and comparison only. Actual 3D printing model performance is related to many other factors." | Bambu Lab, PLA Basic Technical Data Sheet V2.0 <https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PLA_Basic_Technical_Data_Sheet.pdf> | fetched |
| Acceptable strain for a snap: **PLA 4 to 8 %** (ABS 7 %, nylon 4 to 15 %), offered as a starting point | Fictiv, "How to Design Snap Fit Components" <https://www.fictiv.com/articles/how-to-design-snap-fit-components> | fetched |
| Cantilever strain ε = 1.5 · t · Y / (L² · Q) (t beam thickness, Y deflection, L beam length, Q a magnification factor, 1 for a simple case). The formula came through garbled in the fetch; the form here is the standard one. | Fictiv, same page | fetched (formula layout uncertain) |
| "Print snap arms parallel to the build plane whenever possible"; for an arm built along Z, elongation at break "may drop by about 50%" and tensile strength 20 to 30 %, so reduce the allowable strain by 50 % | Fictiv, same page; same advice in Core77 <https://www.core77.com/posts/65318/how-to-design-snap-fit-components> | Fictiv fetched; Core77 snippet |
| Return angle equal to the lead-in angle means "the same force is used during assembly and disassembly"; a 90° return angle cannot be taken apart | Fictiv, same page | fetched |

**Hedges carried:** elongation at break is where a test bar snaps, not a safe working figure for
something bent over and over. Bambu's numbers come from annealed, solid test bars, which an
ordinary print is not. Fictiv's 4 to 8 % is a starting range, not a tested limit.

## 3. Cable sizes

| Cable | Outer diameter | Source | Status |
|---|---|---|---|
| USB-C to USB-C, 240 W, 0.9 m, TPE jacket | **4.0 mm** ("O.D.: 0.16in (4.0mm)"); its plug body is 12.2 mm wide and 6.4 mm tall | StarTech USB2EPR3F datasheet <https://media.startech.com/cms/pdfs/usb2epr3f_datasheet.pdf> | fetched |
| Apple USB-C to USB-C, 1 m (iPad Pro) | about 3.0 mm; Apple's optional 2 m cable about 3.5 mm. A forum user's own measurement; another user says Apple does not publish it | Apple Community thread 253788184 <https://discussions.apple.com/thread/253788184> | fetched |
| Other 240 W USB-C cables | 3.8 mm (braided), 4.7 mm (silicone and braid), 4.8 mm | search summaries of WYE, StarTech, Dynamix, ASUS listings | snippet |
| USB-C to Lightning | 3.2, 3.8 and 4.2 mm (one C2G line), 3.3 mm (Delock), 3.4 mm (Tripp Lite), 4.0 mm (Eaton) | search summaries of C2G, Delock, Tripp Lite, Eaton datasheets | snippet |
| Earbud cable | 2.0 mm main wire, 1.5 mm branch (DIY earphone wire listings, TPE); "slim 2.0 mm" Shure replacement cable. No figure found for Apple EarPods. | search summaries of Newegg and worldofstereo listings | snippet |
| Laptop charger, DC cord (barrel plug) | **not found** | none | — |
| Laptop charger, AC mains cord (wall side, for reference only) | 6.3 mm and 7.62 mm for 18 AWG cords | search summaries of C2G and StarTech listings | snippet |
| Laptop charger, USB-C 240 W | see the USB-C rows: 3.8 to 4.8 mm | as above | fetched (4.0) / snippet |
| USB-C plug cut-out a maker used | 7 × 10.5 mm; USB-A 8 × 14 mm | Printables 1037051 | fetched (API text) |

## 4. How stacking is done

| Method | Source and numbers | Status |
|---|---|---|
| Ridge on the top, groove underneath. The maker puts the ridge on the **top** face of the inner piece because a ridge on a face printed flat side down "would have necessitate a ton of supports"; ridge radius 2.5 mm, 0.1 mm margin in the groove; top and bottom faces 1.5 mm thick; wall 2.0 mm; the stackable version is optional because the ridge is "quite aggressive on your textile" in a pocket. A small chamfer was added "so that even an elephant foot would not fuse the two pieces". | Printables 601730 | fetched (API text) |
| Separate stacking rings and base plates, any winder of the same diameter class stacks | Printables 1037051 | fetched (API text) |
| Flat side up, indentation down, so they stack | Printables 436822 | fetched (API text) |
| "Stackable design" with no method given | Printables 1456960, 1827019, 56609 | fetched (API text) |
| Under 10 g per unit, "multiple organizers can be connected together" | MakerWorld 2851359 <https://makerworld.com/pt/models/2851359-modular-cable-organizer-stackable-cable-holder> | snippet |
| Magnets | none of the sources here uses magnets | — |

Thickness per piece: the only stated heights are the 601730 default (14 mm inside height plus two
1.5 mm faces) and the Next Gen 80×20 and 80×24 versions (20 and 24 mm). Every surveyed winder is a
closed box, so all are far thicker than a single layer of cable.

## 5. Print traps

| Trap | Figure | Source | Status |
|---|---|---|---|
| Overhangs | "between 45 and 60 degrees, depending on your nozzle diameter and settings" | Prusa, "Modeling with 3D printing in mind" <https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135> | fetched |
| Overhangs | "up to 45° without compromising quality", "depending on the material" | Hubs, "How to design parts for FDM 3D printing" <https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/> | fetched |
| Overhangs | Max overhang angle 55° for PLA Basic | Bambu PLA Basic data sheet | fetched |
| Bridges | Sag and support marks unless the bridge is "less than 5mm" | Hubs, same page | fetched |
| Bridges | Max bridging length 30 mm for PLA Basic | Bambu PLA Basic data sheet | fetched |
| Thin walls | A wall thinner than one perimeter cannot print; one perimeter from a 0.4 mm nozzle is about 0.45 mm; "Detect thin walls" helps but cannot fix walls under one perimeter | Prusa, same page | fetched |
| Thin walls | Groove wall set to 0.61 mm "so that every engine would print a (1 line thick) wall", even with a 0.6 mm nozzle | Printables 601730 | fetched (API text) |
| Thin walls | "It is tempting to print with more perimeters, but experience shows then prints to fail"; 0.35 mm gap between print-in-place rings, "0.3 mm or even 0.25 mm ... will only work on very well-tuned printers" | Printables 1037051 | fetched (API text) |
| First layer and the bottom edge | "Add a 45° chamfer or radius to edges touching the build plate" | Hubs, same page | fetched |
| First layer and the bottom edge | Rounded edges facing the bed make steep overhangs, so "use chamfer instead"; elephant foot compensation "can improve the tolerances of some areas" | Prusa, same page | fetched |
| Gaps between parts | Accurate to "at least 0.2 mm"; moving parts start at "at least 0.3 mm"; no one value fits all | Prusa, same page | fetched |
| Layer direction | Snap arms printed along Z lose about half their stretch | Fictiv (section 2) | fetched |
| Small tall prints | Print two at once so each layer cools | Printables 1410373 | fetched (API text) |

The Bambu wiki page on wall and surface settings returned HTTP 402 and was not read.

## Also seen, not used above

Kept so the record is whole. All are **snippets** unless marked.

- MakerWorld 3063346, a cable clip: keep the clip's gap angle at 150° or less.
  <https://makerworld.com/en/models/3063346>
- Nite Ize CordWrap / Curvyman product reviews: flat cords do not fit its clasps.
- Silicone cable wraps, product reviews: "not hard enough" to hold their shape.
- MakerWorld 806568, a spiral cable sleeve tool. <https://makerworld.com/en/models/806568>
- MakerWorld 1195362 and 1977251, cable winders. <https://makerworld.com/en/models/1195362>,
  <https://makerworld.com/en/models/1977251>
- Printables 1251652, a remix of a spiral cable holder; 1583187, a 20 mm clamp with a slim spiral
  for 6 to 8 mm cable. <https://www.printables.com/model/1251652>,
  <https://www.printables.com/model/1583187> (fetched, API search summary only)
- Printables 55627, a print-in-place cable puck. <https://www.printables.com/model/55627>
  (fetched, API search summary only)
