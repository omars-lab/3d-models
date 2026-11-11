---
date: 2026-11-11
produced-by: research pass A (Claude subagent)
feeds: docs/design/pieces/cable-spiral-design.md (PR #1023)
---

# Research A: a thin, stackable "top-open cable spiral"

**The question.** Omar wants our own cable spiral: a part you wrap a cable around, or press it into,
so the cable stays put. It must be thin and stackable. It prints on the Bambu Lab X2D with a 0.4 mm
nozzle, in PLA, at 0.20 mm layers, with no supports. This file is the raw findings. The design
proposal is in the companion file, 2026-11-11-cable-spiral-a-recommendation.md, in this folder.

**How to read the sources.** Every source is marked **fetched** (I read the page itself) or
**snippet** (I saw only a search-engine summary of it). A snippet can be wrong about the page, so a
number that rests on one is flagged. Printables, 3dgo.app and the MakerWorld search page sat behind
a bot check for this pass, so every Printables model below is a snippet. MakerWorld model pages
opened in a browser three times out of six.

**What was surveyed.** 10 pages fetched, 2 downloaded meshes measured by us, and 20 sources (22
links) seen only as snippets. Every claim of "none" below is about that set, not about the whole web.

## 1. What shapes match "top-open cable spiral"

### What the survey turned up

| Shape | Examples | How the cable is held | Thin? | Stacks? |
|---|---|---|---|---|
| **A. Flat disc, open-topped spiral groove.** The cable is laid or pressed down into a groove cut into the top face, spiralling in from the rim, like a record groove. | None of the surveyed pages whose shape I could see. fokerman's organizer (row C) was not seen and may be one. | (Not seen.) | Yes: about one cable diameter plus a floor. | Like coasters. |
| **B. Flat spool or winder.** The cable winds around a core between two flanges, and the end tucks into a slot. | Stackable Cable Winder, MakerWorld 2426343 (**fetched**). Cable winder Pro, MakerWorld 2079227 (**fetched**). Next Gen USB winder, Printables 1037051 (**snippet**). Advanced Stackable winder, Printables 629654 (**snippet**). Easy cable winder, MakerWorld 1509676 (**snippet**). Cable Roll, Thangs 1089730 (**snippet**). | Wound turns press on each other, and a slot or twist lid holds the end. | No: 20 to 80 mm tall. | Yes, several by design. |
| **C. Spiral cable organizer.** A small spiral body that a few cables are fed into. | fokerman's "Spiral cable organizer", Printables 302991 and 1430486 (**snippet** only). | The snippet says it holds "at least 2 cables", and three if loaded "thickest first". | Unknown. | Unknown. |
| **D. Spiral wrap or sleeve.** A helix wrapped along a cable run, to bundle or protect it. | Spiral cable wrap, 2 to 20 mm, Printables 1075969 (**snippet**). Parametric spiral wrap, Printables 1499648 (**snippet**). Spiral sleeve tool, MakerWorld 806568 (**snippet**). | Wraps around the cable. | Yes. | No: this is a different job, not a holder. |
| **E. Press-in clip.** A C-shaped clip or slot the cable is pushed past a narrow mouth into. | The two parts already on `cables-1`, measured below. Parametric One-Piece Snap Cable Clip, MakerWorld 3436380 (**fetched**). | A narrow mouth the cable snaps past. | Yes. | Not a spiral. |

**What I did not find.** None of the 10 fetched pages, and none of the snippets whose shape I could
make out, shows shape A: a flat disc with a spiral channel open on top that the cable is pressed
into. One exception is unknown: fokerman's "Spiral cable organizer" is the closest name match in the
survey, and I never saw its shape, so it may be shape A. Searches for
"top open" cable spiral, spiral cable clip, and spiral groove disc returned nothing that matched.
This could mean the shape is uncommon, or only that my searches missed it. Printables was unreadable
in this pass, and its search was never tried directly.

### Which reading fits "wrap around, stays in place, thin, stackable" best

- **"Top-open"** names an open top face. Shape A has one; a spool (B) has its opening around the rim.
- **"Stays in place"** is something A can do for every turn by pressing the cable past a narrow
  mouth, as shape E does. A spool holds only the end, and the turns stay because they are wound
  tight.
- **"Thin"** rules out every spool whose height I saw: the shortest is about 20 mm (the Next Gen 80 x 20
  version, **snippet**) and Cable winder Pro is 82 mm tall (**fetched**). A disc with a groove
  is about one cable diameter plus a floor.
- **"Wrap a cable around"** fits B better than A, because in A you lay the cable in rather than
  wrap it.

So A, the flat disc with an open spiral groove that grips the cable, fits three of the four words,
and the shape E clips show how the grip works. B fits "wrap around" and fails "thin".

**The one-sentence question for Omar, if it is truly ambiguous:** "Do you picture pressing the cable
down into a spiral groove on the top face of a flat disc, like a record groove, or winding it around
the edge of a thin disc, like a yo-yo?"

## 2. How the cable is held

### Measured by us: the two press-in parts on `cables-1`

I cut both meshes from the gitignored imports folder (`.bambu/imports/`) with a plane and drew the
cross-section. These are **measured by us from the maker's mesh**, read off a 1 mm grid, so each is
good to about ±0.1 mm.

- **Cable clips** (MakerWorld 1733675, `cable-clips-all.stl`). Each clip is a round bore **4.0 mm**
  across, with a mouth **2.5 mm** wide at the top. The mouth is 0.62 of the bore. The bore wraps
  about 285° around the cable. Above the mouth the tips flare outward into a lead-in, a sloped entry
  that steers the cable in. The thinnest part of the C beside the bore is about 1.3 mm. Inside the
  arms the section shows short cut lines that may be relief slits or may be a meshing artifact; I did
  not check which. I also did not check which way the clip lies on the bed: the plate page says the
  maker's project turns the bare STL a quarter turn.
- **Universal Cable Holder** (MakerWorld 1003508, `universal-cable-holder-3-slots.stl`). This one
  works differently. Each slot is a bottle shape whose two sides are thin S-curved springs, about
  **0.75 mm** thick and roughly 11 mm long. The cable passes a neck about **0.8 mm** wide by
  spreading the springs, then sits loose in a bulb about **7.2 mm** across. The mesh's bounds match
  the plate page's 34 x 16.75 x 15 mm block on its base. If its height axis is the printer's, the
  springs are drawn in the bed plane, so they bend along the layer lines, which is the strong way
  (see below).

These two are the only source I have for the mouth-to-cable ratio. The clip squeezes the jacket
past a mouth well under the cable's width, with a short, stiff arm. The holder uses long, soft
springs and a very narrow neck.

### Other snap-fit and grip numbers

| What | Number | Source | Its hedge |
|---|---|---|---|
| Undercut, the depth of the hook the part snaps past | 0.5 to 1.2 mm | Sovol, **fetched** | "starting baselines to test" |
| Lead-in angle, the slope the part slides up | 25° to 35° | Sovol, **fetched** | same |
| Clearance between mating parts | 0.20 to 0.40 mm per side; 0.30 to 0.40 if too tight | Sovol, **fetched** | same |
| Length of a PLA flex arm against its thickness | 8:1 to 10:1 (a 2.0 mm arm about 16 to 20 mm long) | Sovol, **fetched** | for "stiffer materials like PLA" |
| Root fillet, the rounded corner where the arm meets the body | r ≥ half the arm's thickness, at least 0.8 to 1.0 mm for a 0.4 mm nozzle | Sovol, **fetched** | |
| Extra room per cable channel in a lidded clip | 0.6 mm (range 0 to 2) | Parametric One-Piece Snap Cable Clip, MakerWorld 3436380, **fetched** | a lidded clip, not a press-in |
| Hook undercut angle in that clip | 20°, "keep it above ~12° or the lid can pry the latch open" | same | |
| Latch arm thickness | 1.4 mm (range 1 to 2.6) | same | |
| A thin cable holder broke on first use (PETG) | — | Cable winder Pro reviews, MakerWorld 2079227, **fetched** | the designer blamed fast cooling of a very thin part and said he would thicken it |
| Silicone press-in clips: slots "a tad too big" let standard cables pop out; thick, stiff cables are "harder to press into" | — | marketplace reviews (desertcart), **snippet** | buyer reviews |

### How far a thin PLA wall can bend before it cracks

| What | Number | Source | Its hedge |
|---|---|---|---|
| Strain at break, along the layers (X-Y) | 12.2 ± 0.4% | Bambu PLA Basic data sheet V2.0, **fetched** | 100% infill specimens, annealed and dried at 55 °C for 8 h. The sheet says the values are "for design reference and comparison only". |
| Strain at break, across the layers (Z) | 7.5 ± 0.3% | same | same |
| Bending modulus, X-Y and Z | 2750 and 2370 MPa | same | same |
| "Acceptable strain" for printed PLA | 4 to 8% | Fictiv, **fetched** | No test standard or source is given. |
| Derate for an arm bent across its layers | halve the allowed strain | Fictiv, **fetched** | Fictiv's own recommendation, not tied to a material or printer. |
| PLA creeps under load, a slow bend that does not spring back; switch to PETG or ASA if a clip loosens | — | Sovol, **fetched** | |
| Cycle a test joint 20 to 30 times and look for cracks or a bend that stays | — | Sovol, **fetched** | |

**The figures above are break values, not working values.** 12.2% and 7.5% are where an annealed,
solid test bar snapped. A thin printed wall with two lines and seams will do worse. Fictiv's 4 to
8%, halved to 2 to 4% across the layers, is the only working figure I found, and it has no cited
source.

**Which way does the wall bend?** On a disc printed flat, a groove wall stands up from the bed. When
a cable pushes past the top of the wall, the wall bends like a diving board stood on end, and the
stretch at its root runs up and down, across the layer lines. That is the weak direction, so the 7.5%
and the halving apply. The cable holder above avoids this by drawing its springs in the bed plane.
A flat disc cannot, because its cable lies flat.

**Worked example.** I used the standard formula for a straight cantilever, a beam fixed at one end,
with a constant cross-section: strain at the root ε = 1.5 · t · y / L². Here t is the wall's
thickness, y is how far its tip moves, and L is its height. Fictiv's page prints the same formula,
but its rendering was garbled in the fetch.

- With a wall 0.8 mm thick (two lines), 4 mm tall, whose top moves 0.3 mm: ε = 1.5 × 0.8 × 0.3 / 16
  = **2.25%**.
- That sits at the bottom of the 2 to 4% band (Fictiv, halved) and well under the 7.5% break value.
- At 0.5 mm of movement it is 3.75%, the top of the band.
- With the recommendation's own wall, 0.9 mm thick and 4.1 mm tall, a 0.3 mm movement gives
  1.5 × 0.9 × 0.3 / 16.8 = **2.4%**, still in the lower half of the band. The strain climbs fast
  as the wall gets shorter: at 3.5 mm tall it would be 3.3%.

**Two reasons the formula may be wrong for a spiral.**

1. **The wall is not a free arm.** A spiral wall is joined to itself all the way along, so it bends
   much less than a lone arm does. The cable can still go in, because the jacket squashes as well.
   How much of the grip comes from the wall bending, and how much from the jacket squashing, is
   **a guess to test**.
2. **Neighbouring turns share their walls.** The wall between two turns is shared. If the next turn
   already holds a cable, the wall cannot bend toward it. This is my own reading of the geometry,
   not something a source says.

## 3. Typical cable diameters

| Cable | Outer diameter | Source | Its hedge |
|---|---|---|---|
| Apple USB-C, 1 m (came with an iPad Pro 12.9) | ~3.0 mm | Apple Community thread 253788184, one user's measurement, **fetched** | "different suppliers may use cables that vary"; another user said "I don't believe the diameter of the cable is a published specification" |
| Apple USB-C, 2 m (optional) | ~3.5 mm | same | same |
| Anker 515 USB-C to USB-C (A8487) | 4.7 mm | Anker FAQ, **fetched** | |
| Apple 240 W USB-C, the laptop-charging cable | ~4.6 mm | ChargerLAB teardown, **fetched** | method not stated |
| Braided USB-C, 1 m | Ø5 mm | a Next Gen winder derivative's notes, **snippet** | |
| USB-C to Lightning (C2G, several models) | 3.2, 3.8, 4.2 mm | C2G spec sheet, **snippet** (the page redirected away) | |
| Lindy Lightning | 3.5 mm jacket | Lindy listing, **snippet** (page blocked) | |
| Wired earbuds | **no source found** | Two searches found only plug and driver sizes. | Measure it. |
| Laptop charger, the barrel-plug side of the brick | **no source found** | The 7.3 to 7.6 mm figures I found are for the mains cord on the wall side (StarTech C5/C7 cords, **snippet**), not the cord from the brick to the laptop. | Measure it. |

The range I can source for phone and laptop cables runs from about **3.0 to 5 mm**, which is wide
for a press-in grip. A groove sized for one end of that range will be loose at the other, or will
not take the cable at all. Omar's own cables should be measured with calipers before any groove
width is fixed.

## 4. How stacking is done

| Method | Example | Source | Thickness given? |
|---|---|---|---|
| A separate connector ring joining two winders, a snap fit "depending on your tolerance settings"; "print connector ring with same material as cable winder, to make sure tolerances are correct" | Stackable Cable Winder, MakerWorld 2426343 | **fetched** | No. One unit holds up to 2 m of cable up to 4.5 mm across. |
| "All sizes can be stacked due to identical core diameter and handle size" | Advanced Stackable winder, Printables 629654 | **snippet** | Large size Ø70 x 48 mm |
| Stackable units added to expand capacity | Cable Roll, Thangs 1089730 | **snippet** | No |
| Print-in-place, stackable | Next Gen USB winder, Printables 1037051 | **snippet** | 80 x 20, 80 x 24 and 80 x 28 mm versions (in derivatives) |

Pegs, a lip with a matching recess, and magnets are common ways to stack printed parts, but **none of
the surveyed cable pages uses or describes them**. The per-layer thickness for our part has no
source. It is our own sum of the floor, the cable and the lip, and is worked out in the
recommendation as a guess to test.

## 5. Print traps

| Trap | What the source says | Source |
|---|---|---|
| Overhang, a part of a layer that hangs out past the layer below | Max overhang angle 55° for PLA Basic. The sheet does not say whether the angle is measured from upright or from flat. Read as from upright, a 45° slope is safe. Read as from flat, only slopes within 35° of upright are, and a 45° slope is not | Bambu PLA Basic data sheet, **fetched** |
| | The 45° rule is the usual safe start; PLA with strong cooling often reaches 55 to 60° | blogs and vendor guides (3dprinterly, jlc3dp), **snippet**, which they themselves call estimates |
| Bridging, a line printed across open air between two supports | Max bridging length 30 mm for PLA Basic | Bambu PLA Basic data sheet, **fetched** |
| | Other guides give anything from 10 to 50 mm | blogs, **snippet** |
| Walls thinner than two lines | In PrusaSlicer's Arachne wall generator, which varies line width to fit a thin wall, "Features thinner than this value will not be printed"; anything above that is widened to a minimum line width | Prusa help, Arachne perimeter generator, **fetched**; no default value was on the page |
| | Walls thinner than one line are likely skipped; a 0.4 mm wall still gets a line under Arachne | Prusa forum posts, **snippet**, community answers |
| | Thin arms (1.5 to 2.5 mm) want 4 wall loops and solid infill | Sovol, **fetched** |
| Flex arm printed upright | It "can separate layers at the root when it flexes"; print the arm flat so it bends along the layer lines | Sovol, **fetched**; Fictiv agrees ("Print snap arms parallel to the build plane whenever possible"), **fetched** |
| Supports under a flexing part | Support scars on the stretched face can start cracks | Sovol, **fetched** |
| First layer of a thin flat part | Elephant foot compensation shrinks the first layer to offset its squash. Bambu's wiki says to set it to 0 and add a brim when a part warps | Bambu wiki, elephant foot and "use disc to avoid warping", **snippet** (the page refused the fetch) |
| | Bed 35 to 45 °C and PVP glue on the plate | Bambu PLA Basic data sheet, **fetched** |

I bring the Bambu data sheet's 55° and 30 mm across from Bambu's own test conditions to our X2D
with PLA Basic. That holds because the sheet is for the same filament and Bambu printers. It may not
hold for another brand of PLA.

## Sources

Fetched:

- Fictiv, How to design snap-fit components: https://www.fictiv.com/articles/how-to-design-snap-fit-components
- Sovol, 3D printed snap-fit joints: https://www.sovol3d.com/blogs/news/3d-printed-snap-fit-joints-how-to-design-clips-that-work
- Bambu PLA Basic technical data sheet V2.0: https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PLA_Basic_Technical_Data_Sheet.pdf
- Stackable Cable Winder (KL Worx), MakerWorld 2426343: https://makerworld.com/en/models/2426343-stackable-cable-winder
- Cable winder Pro (Mechaverse3d), MakerWorld 2079227: https://makerworld.com/en/models/2079227-cable-winder-pro
- Parametric One-Piece Snap Cable Clip (AlexB), MakerWorld 3436380: https://makerworld.com/en/models/3436380
- ChargerLAB teardown of the Apple 240 W cable: https://chargerlab.com/teardown-of-apple-240w-usb-c-charge-cable-a2794
- Apple Community thread on USB-C cable diameter: https://discussions.apple.com/thread/253788184
- Anker 515 USB-C cable FAQ: https://service.anker.com/article-description/Anker-515-USB-C-to-USB-C-cable-FAQ
- Prusa help, Arachne perimeter generator: https://help.prusa3d.com/article/arachne-perimeter-generator_352769

Measured by us from the maker's mesh (files gitignored, not in this repo):

- Cable clips, MakerWorld 1733675 (`cable-clips-all.stl`)
- Universal Cable Holder 3-slot, MakerWorld 1003508 (`universal-cable-holder-3-slots.stl`)

Snippet only:

- Spiral cable organizer (fokerman): https://www.printables.com/model/302991-spiral-cable-organizer and https://www.printables.com/model/1430486-spiral-cable-organizer
- Next Gen USB cable winder: https://www.printables.com/model/1037051-next-gen-usb-and-more-cable-winder-organizer-print
- Advanced Stackable USB cable winder: https://www.printables.com/model/629654-advanced-stackable-print-in-place-usb-cable-winder
- Next Gen USB (80x28): https://www.printables.com/model/1429880-next-gen-usb-80x28
- Stackable Cable Winder, Printables: https://www.printables.com/model/1456960-stackable-cable-winder-smart-desk-cable-organizer
- Easy cable winder, MakerWorld 1509676: https://makerworld.com/en/models/1509676-easy-cable-winder
- Cable Organiser, Cable Roll (Thangs): https://thangs.com/m/1089730
- Spiral cable wrap 2 to 20 mm: https://printables.com/model/1075969-spiral-cable-wrap-2mm-to-20mm-inner-diameter
- Spiral wrap, parametric: https://www.printables.com/model/1499648-spiral-wrap-for-cables-parametrizablecustomizable
- Spiral sleeve tool, MakerWorld 806568: https://makerworld.com/models/806568
- Earbud spool with cable fixing feature: https://www.stlfinder.com/model/earbud-spool-with-cable-fixing-feature-cGd8EuG7/2439353
- Portable Cable Organizer / Winder: https://www.printables.com/model/564262-portable-cable-organizer-winder
- C2G USB-C to Lightning spec sheet: https://Www.Cablestogo.com/p/print/CG-C2G54556.pdf
- Lindy Lightning cables: https://comms-express.com/categories/lindy-usb-to-lightning-cables/
- StarTech laptop power cords: https://cdw.com/product/startech.com-10-ft-standard-laptop-power-cord-nema-1-15p-to-c7/2569800
- Silicone cable clip reviews: https://www.desertcart.co.za/products/156583665-soulwit-cable-holder-clips-3-pack-cable-management-cord-organizer
- Bambu wiki, elephant foot: https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot
- Bambu wiki, use disc to avoid warping: https://wiki.bambulab.com/en/software/bambu-studio/use-disc-to-avoid-warping
- Overhang guides: https://3dprinterly.com/the-45-degree-rule-in-3d-printing-optimal-orientations/ and https://jlc3dp.com/blog/how-to-get-better-overhangs-3d-printing
- Prusa forum, thin walls: https://forum.prusa3d.com/forum/prusaslicer/help-with-wall-thickness
