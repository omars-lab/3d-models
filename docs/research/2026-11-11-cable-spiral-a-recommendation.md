---
date: 2026-11-11
produced-by: research pass A (Claude subagent)
feeds: docs/design/products/cable-spiral-design.md (not yet written)
---

# Recommendation A: a flat disc with a spiral groove you press the cable into

This proposal is built on the raw findings in 2026-11-11-cable-spiral-a.md, in this folder. Each
number below either names its source there or is marked **a guess to test**. "Suggested:" means a
starting value for the first test print, not a settled one.

## The reading I chose

**A flat disc with an open spiral groove on its top face.** You press the cable down into the
groove, starting at the rim and working inward, like the groove on a record. A narrow mouth along
the groove holds each turn in.

Why this reading:

- **"Top-open"** names an open top face. A spool's opening runs around its rim instead.
- **"Thin"** rules out every spool whose height I saw. The shortest was about 20 mm tall; a grooved
  disc is about one cable diameter plus a floor.
- **"Stays in place"** is what a press-in mouth does, and the two press-in parts already on the
  `cables-1` plate show how one works.
- **"Stackable"** comes easily: flat discs stack like coasters.

The other reading is **a thin flat spool**: the cable winds around a core between two flanges, like
a yo-yo. It fits "wrap around" better and fails "thin". None of the surveyed pages whose shape I
could see shows the grooved disc. One I could not see, fokerman's "Spiral cable organizer" on
Printables, may be one and is worth opening before any design work. Until then I have no maker to
copy, and the first prints are the evidence.

**If Omar's picture is the other one, ask him this:** "Do you picture pressing the cable down into a
spiral groove on the top face of a flat disc, like a record groove, or winding it around the edge of
a thin disc, like a yo-yo?"

## A sketch of the geometry

A cut through the disc, across three turns of the groove. The jacket is the cable's outer plastic
skin. The lip is a small ledge at the top of each wall that narrows the groove's mouth.

```
      lead-in       lead-in
       \  /          \  /
   ___ |  | ________ |  | ___      <- top of disc
  |   ||  ||        ||  ||   |
  |   |(  )|  wall  |(  )|   |     <- cable, held under the lip
  |___|____|________|____|___|
  |__________________________|     <- floor, 0.6 mm
```

| Part | Suggested | Where it comes from |
|---|---|---|
| Disc diameter | 80 mm | **A guess to test**: about a coaster, and the Next Gen winder's family is 80 mm across (**snippet**). |
| Groove width at the bottom | the cable's diameter, d | **A guess to test.** The lidded clip in MakerWorld 3436380 adds 0.6 mm of room, but a lid holds it closed and ours has none. |
| Groove depth | d + 0.6 mm: 4.1 mm for a 3.5 mm cable | **A guess to test.** The extra 0.6 mm is room for the lip above the cable, so the cable sits just under the disc top. |
| Mouth (the gap between the two lips) | d − 0.6 mm: 2.9 mm for a 3.5 mm cable, a ratio of about 0.83 | **A guess to test.** The press-in clip on `cables-1` measures 2.5 mm over a 4.0 mm bore, a ratio of 0.62 (our measurement of its mesh). I chose gentler because our walls bend across the layers (the weak way) and are shared between turns. |
| Lip | 0.3 mm a side | **A guess to test.** It is below Sovol's 0.5 to 1.2 mm undercut range, which is for a free snap arm. I chose smaller for the reasons in the row above. The test piece below tries lips of 0.1, 0.2 and 0.3 mm. |
| Underside of the lip | a chamfer, a sloped face instead of a flat ledge, at 30° from upright (about 0.5 mm tall for a 0.3 mm lip) | So it prints without supports. Bambu's data sheet gives 55° as PLA Basic's max overhang but does not say whether it measures from upright or from flat. 30° from upright is inside the limit either way; a 45° chamfer would pass only the from-upright reading. |
| Top of the lip | a lead-in sloped at about 30° | Sovol's 25° to 35° lead-in. |
| Wall between turns | 0.9 mm | **A guess to test**: thick enough for the slicer to lay two lines with the 0.4 mm nozzle. The line width the X2D profile uses was not checked. |
| Floor | 0.6 mm (three 0.20 mm layers) | **A guess to test.** |
| Spiral | the groove's centre line runs from radius 14 mm to 36 mm, one turn every 4.4 mm (d + wall) | Our own sum. The groove's inner edge is then at 12.25 mm and its outer edge at 37.75 mm, which leaves a 2.25 mm rim on an 80 mm disc. |
| Cable it holds | about 0.8 m for a 3.5 mm cable | Length of a spiral ≈ π(R² − r²) / pitch = π(36² − 14²) / 4.4 ≈ 785 mm. |
| Disc thickness | about 4.7 mm for a 3.5 mm cable | floor 0.6 + groove depth 4.1. |

**Will a 0.9 mm wall bend enough without cracking?** The standard beam formula is strain at the foot
= 1.5 × thickness × movement / height². For the wall in the table, 0.9 mm thick and 4.1 mm tall,
whose top moves 0.3 mm to let the cable past one lip, that is 1.5 × 0.9 × 0.3 / 16.8 = **2.4%**.

- Fictiv allows 4 to 8% for printed PLA, and says to halve that when the bend runs across the
  layers, as it does here. That leaves 2 to 4%, and 2.4% sits in its lower half.
- Bambu's 7.5% across the layers is where its solid, annealed test bars **broke**. It is not a
  working value.
- The strain rises fast as the wall gets shorter. A 3.5 mm wall would reach 3.3%.

Two cautions:

- The formula is for a lone arm. A spiral wall is joined to itself along its whole length, so it
  bends less, and the cable's jacket probably does much of the squashing. That share is unknown.
- A wall between two turns that both hold cable has nowhere to bend.

So the grip may be tighter, or looser, than the sum says. Only a test print settles it.

**Test a piece, not the whole disc.** Print a quarter of the disc with three short straight groove
runs. Make their mouths d − 0.2, d − 0.4 and d − 0.6 mm, and press in the cable Omar uses most. Push
it in and pull it out 20 to 30 times (Sovol's cycle test), then look for cracks and a wall that stays
bent. Then press a second cable into the next groove and check whether the first one still holds.

**PLA creeps.** It slowly bends under a steady load and stays bent, so a grip that holds on the first
day can loosen (Sovol). Changing to PETG is Sovol's fix if that happens.

## How the discs stack

**Suggested: a solid round boss (a short raised stub) in the middle of the top face, and a matching
round pocket in the middle of the underside.** The boss of one disc sits in the pocket of the disc
above.

- **Room in the middle.** The groove's inner edge is at radius 12.25 mm, and the wall inside it
  takes another 0.9 mm. That leaves a solid centre about 22 mm across, at the full 4.7 mm thickness.
- **The boss.** 10 mm across and 1.5 mm tall: **a guess to test**.
- **The pocket.** 10.4 mm across, so 0.2 mm of room per side (Sovol's 0.20 to 0.40 mm clearance;
  use 0.3 if it binds), and 1.7 mm deep, so the boss never bottoms out. That leaves 3.0 mm of solid
  plastic above the pocket.
- **Printing the pocket.** The disc prints top face up, so the pocket's ceiling is a flat 10.4 mm
  span over open air: a bridge. That is well inside the 30 mm max bridge in Bambu's PLA Basic data
  sheet. Whether the ceiling sags enough to matter is **a guess to test**.
- **The stack.** Each disc sits flat on the walls of the one below, so it adds its own 4.7 mm and
  nothing more.
- **The precedent.** The one stackable cable winder I could read, MakerWorld 2426343, joins units
  with a separate snap-fit ring. Its maker warns that the fit depends "on your tolerance settings".
  A boss printed as part of each disc avoids a second part, but it is untested.

Pegs, a lip with a matching recess, and magnets would all work too, but no surveyed cable page used
them, so I have no numbers for them.

## Questions for Omar

1. **Which picture:** the grooved disc, or a thin spool you wind around? (The question above.)
2. **Which cables?** Please measure the ones you want to store with calipers. The sourced USB-C
   cables run from about 3.0 to 4.7 mm across, and I found no figures for earbud cables or the cable
   from a laptop charger brick. One groove width will not grip all of them.
3. **Where do the plugs go?** A USB-C plug head is likely thicker than a 4.7 mm disc. The plug
   would need a pocket at the rim or at the middle, or it sits off the edge.
4. **How much cable per disc?** An 80 mm disc holds about 0.8 m of 3.5 mm cable. That takes most
   of a 1 m cable, with the ends hanging off, but not a 2 m one. A 90 mm disc would hold about 1 m.
5. **PLA or PETG?** PLA can loosen its grip over months. PETG is the usual fix, at the cost of a
   filament change.
