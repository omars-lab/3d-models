---
date: 2026-11-11
produced-by: "research pass B (Claude subagent)"
feeds: "docs/design/pieces/cable-spiral-design.md (PR #1023)"
---

# Cable spiral: design proposal, research pass B

This proposal rests on the findings in
[2026-11-11-cable-spiral-b.md](2026-11-11-cable-spiral-b.md). Each number below says where it came
from, or is marked **guess, test in print**. Nothing here has been printed. The downloaded holder
and clips on the [cables-1](../design/plates/cables-1.md) plate are not printed either, so we have
no grip measurement of our own.

## 1. The reading I picked

**A flat round disc with an open-topped spiral groove. You press the cable down into the groove
and a small lip on each side holds it.** The next disc stacks on top, and its flat underside
closes the grooves below.

The cable goes in folded at its middle. The fold sits in an S-shaped bend at the center of the
disc, and the two halves run out along two side-by-side spirals (a "two-start" spiral: two grooves
wound together, like two threads on one screw). Both plugs leave at the rim. This keeps the plugs
out of the middle, which matters because a USB-C plug body is 6.4 mm tall (StarTech datasheet,
fetched), taller than the groove is deep.

Why this reading:

- "Top-open" and "press a cable into it" both point at a groove open on top, not a closed winder.
- "Thin and stackable" rules out the winders surveyed, which are all closed boxes 14 to 24 mm
  inside or more (Printables 601730 and 1037051, fetched as API text).
- The nearest shape found is the MakerWorld "Data Cable Spool Storage Box" (3056379): a disc with
  an S-shaped slot and outlets at both ends. It is a **snippet** only, and its slot may be closed
  on top.

**This shape is my own put-together.** None of the 17 shape sources in the findings file shows,
in words I could read, an open-topped groove disc that is pressed into and stacks. I saw almost
none of their pictures, so one of them may well be this shape.

The other reading is a spool: a flat disc with a center post and two rims, wound around like a
yo-yo, with a notch to catch the end (The Loop, the Earbud Credit Card wrap). It is simpler to
print but the cable is wound, not pressed in, and the stack is not closed.

**Question for Omar (one sentence):** Do you want to press the cable down into a spiral groove in a
flat disc, with the next disc closing it, or wind it around a center post between two rims like a
yo-yo, and do you have a link or picture of the one you have in mind?

## 2. Geometry, for a 4 mm cable

All sizes are for one cable of 4.0 mm across (the StarTech 240 W USB-C cable, fetched). Apple's own
1 m USB-C cable measures about 3.0 mm (a user's measurement, fetched). Each groove size should be
a setting of the cable size, so a 3 mm version is the same file.

Cut-through of one groove (not to scale):

```
        mouth 3.2
       |<------>|
   ____/        \____      <- lead-in chamfer on top of each lip
  |    \        /    |     <- lip, 0.7 mm per side, 45 deg underside
  |     \      /     |
  |   (  cable 4.0  )|     <- groove width 4.6, room height 4.4
  |__________________|
  |   floor 1.2      |
```

| Part | Suggested | Where it comes from |
|---|---|---|
| Groove width | Suggested: 4.6 mm (cable + 0.6) | The 0.6 mm `cable_clearance` "so the cable drops in easily" of MakerWorld 3436380 (fetched). That is a clip, not a groove; it carries over because both let a round cable sit loose below a narrower opening. |
| Mouth (opening at the top) | Suggested: 3.2 mm (0.80 × cable) | The 0.70 to 0.85 "opening factor" of MakerWorld 2887515 (**snippet**). Test 0.75, 0.80 and 0.85. |
| Lip per side | 0.7 mm, from width and mouth | arithmetic: (4.6 − 3.2) / 2 |
| Lip underside | Suggested: 45° | Prints without support: 45° Hubs, 45 to 60° Prusa, 55° Bambu PLA Basic (all fetched). |
| Lip top | Suggested: a lead-in chamfer that guides the cable down into the mouth; its angle is a **guess, test in print** | Fictiv (fetched): a return angle equal to the lead-in angle gives the same force in and out, so making the two differ is how pressing in is made easier than pulling out. |
| Room under the lip | Suggested: 4.4 mm (cable + 0.4) | **guess, test in print** |
| Floor | Suggested: 1.2 mm (six 0.20 mm layers) | **guess, test in print**. 601730 uses 1.5 mm faces (fetched). |
| Wall between grooves | Suggested: 0.8 mm (two lines) | **guess, test in print**. Prusa (fetched): a wall under one line, about 0.45 mm, cannot print. 601730 uses a 0.61 mm one-line wall (fetched). |
| Outer rim wall | Suggested: 2.0 mm | 601730's wall width (fetched) |
| Lip height | Suggested: 1.2 mm (six layers) | arithmetic: the 0.7 mm overhang at 45° takes 0.7 mm of height, which leaves 0.5 mm for the lead-in chamfer on top |
| Disc height | about 6.8 mm (1.2 floor + 4.4 room + 1.2 lip) | arithmetic; about 5.8 mm for a 3 mm cable (3.4 mm room) |
| Bottom edge | Suggested: 45° chamfer, 0.6 mm | Hubs and Prusa (fetched): chamfer, not a round, on edges touching the bed; it also keeps elephant foot (the squashed, wider first layer) from showing. |
| Center S-bend | Suggested: each half-loop about 10 to 12 mm in radius | **guess, test in print**: a cable folded tighter than that may not lie flat. |
| Plug exits | Two notches in the rim, 4.6 mm wide | same as the groove width |

### Will the wall bend far enough without cracking?

A 4.0 mm cable through a 3.2 mm mouth pushes each lip out 0.4 mm. The wall is a small upright
beam 0.8 mm thick, fixed at the floor. The cable pushes on the lip, between 4.4 mm (the lip's
underside) and 5.6 mm (its top) above the floor, so take the beam as about 5 mm tall. With
Fictiv's beam formula (strain = 1.5 × thickness × push / height², fetched, though the formula came
through garbled), that is about **1.9 % stretch** (1.5 % if the push lands at the lip's top, 2.5 %
at its underside). This is a rough estimate.

The wall stands up out of the disc, so it bends across the layers, and the across-layers figures
apply. Bambu PLA Basic breaks at 7.5 % across layers (fetched, from annealed solid test bars).
Fictiv says PLA snaps start at 4 to 8 % and to halve that for parts bent across layers, which
gives 2 to 4 %. So 1.9 % sits just under that range: **probably safe for one press, still
marginal for daily use, and the test piece has to settle it.** Breaking stretch is also not a safe figure for a part bent over and over.

The clip figures above all come from C-shaped clips that bend along their layers (3436380 is
printed on its side for that very reason). They carry over to our wall only as a starting point,
because our wall bends the weaker way. The soft cable jacket also squashes, which the estimate
leaves out, and it helps.

A neighboring groove that already holds a cable may keep the shared wall from bending. Pressing in
from the center outward would put that cable on the side the wall bends toward. The test piece
should try a full neighbor.

A curved wall is stiffer than a straight one, and the tightest curves are near the center. So the
straight test grooves below carry over to the outer turns, where the curve is gentle, but not to
the inner ones. The test piece adds one curved groove at the smallest radius for that.

### Size of the disc

Cable length on a disc is about π × (outer radius² − center radius²) ÷ (groove width + wall),
arithmetic, ignoring the S-bend. With 4.6 + 0.8 = 5.4 mm per turn and a 12 mm center:

| Cable | Disc across (with a 2 mm rim) |
|---|---|
| 1 m of 4 mm cable | about 90 mm |
| 2 m of 4 mm cable | about 124 mm |
| 1 m of 3 mm cable (4.4 mm per turn) | about 82 mm |

A cross-check: the Next Gen winder says "1 m of cable takes exactly 4 turns" in its Ø80 mm size
(fetched), but it stacks turns on top of each other, so it is not the same shape.

## 3. Stacking

- **Flat underside closes the grooves below.** The bottom of each disc is flat, so it sits on the
  lips of the one under it. No groove on the underside means no bridge and no support on the bed
  face.
- **Lining them up.** Suggested: a low raised ring on the outer edge of the rim, 0.4 mm tall with
  a 45° inside face. The 0.6 mm 45° chamfer on each disc's bottom edge sits over it. The ring is
  smaller than the chamfer so it can never hold the disc above off the lips: Prusa puts print
  accuracy at "at least 0.2 mm" (fetched), and 0.2 mm is the margin left. **guess, test in
  print.** The 45° faces print without support (sources above). The ring stops the stack sliding.
- **Thickness per disc** is the disc height, about 6.8 mm for 4 mm cable and 5.8 mm for 3 mm
  cable, because the ring tucks inside the chamfer above.
- **A choice not taken:** 601730's ridge and groove (ridge 2.5 mm, 0.1 mm margin, fetched). It
  needs a groove in the underside, and its maker warns the ridge is "quite aggressive on your
  textile". Magnets: none of the sources here uses them.
- **Plugs stay outside.** A plug body (12.2 × 6.4 mm, StarTech, fetched) is nearly as tall as the
  whole 6.8 mm disc, so the two plugs hang out of the rim notches. A plug pocket would need a disc about twice
  as thick.

## 4. Print traps for this shape

- Print flat, open side up. Every lip underside is a 45° overhang, inside what all three sources
  allow.
- No bridges at all in this shape. Hubs says keep bridges under 5 mm; Bambu says 30 mm for PLA
  Basic. The two disagree, and this shape needs neither.
- Walls at 0.8 mm are two lines. A wall under about 0.45 mm will not print (Prusa).
- The first layer of a wide, thin disc can lift at the edge. The 45° bottom chamfer is the
  sources' fix for edges touching the bed. The X2D watches for failures itself.
- PLA creeps under steady load (1410373 warns to use creep-resistant materials, fetched), and
  KLAMMA says PLA "may break if open/close cycled too often" (fetched). Both are risks for a lip
  pressed every day.

## 5. What to print first

Not a whole disc. Suggested: one small test piece of straight groove segments, each about 40 mm
long and cut to this cross-section, with a carved id on each:

- mouth 0.75, 0.80 and 0.85 × the cable
- one plain groove with no lip, as the control
- one 0.8 mm and one 1.2 mm wall at the 0.80 mouth, with a full groove beside it
- one curved groove at the 12 mm center radius, at the 0.80 mouth

The question after the print: press a 4 mm USB-C cable into each, then pull it up. Which ones take
it with a press and hold it until you pull, and did any wall crack? The cables-1 plate, once
printed, gives a second answer to compare: how the downloaded holder grips the same cable.

## 6. Open questions

1. The reading (section 1): groove disc or yo-yo spool.
2. One cable per disc, folded at its middle? Or several short cables per disc?
3. Which cables matter most: 3 mm Apple USB-C, 4 to 5 mm 240 W USB-C, or 2 mm earbud wire? One
   groove size will not grip all three. No laptop barrel-plug cord size was found.
4. Should the stack carry the plugs (a thicker disc), or should they hang out?
5. If PLA lips crack or loosen over time, is PETG acceptable? Most clip makers here pick it.
