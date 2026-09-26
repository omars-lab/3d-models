# Coaster samples — the rules for what goes on the plate

Read by the [print-coaster-samples](SKILL.md) skill every run. Each rule says where it came from.
When a print teaches something new, add or correct a rule here, with the date and the plate.

## How many of each

- **Styles that mate get two copies: interlock and minimal-pegs.** Their dovetail tab and slot
  are self-mating (every straight edge carries both), so two identical minis plug into each
  other. One copy alone cannot show whether the fit is right, too tight or too loose — which is
  the whole question a pegs sample asks. (Omar, 2026-09-25: "we need to create two for pegs
  since they need to fit together.")
- **Every other style gets one copy**: plain, minimal, minimal-frame, twist, border.

## Mini params

- **Size 40** — the mini size the Coaster Lab's size chip and the minis plates use.
- **Straps at 1.6 mm for every style where the holes are the point** — minimal, minimal-frame,
  minimal-pegs, twist. At 40 mm the default 2 mm strap closes the holes up; 1.6 mm opens them and
  is still the freestanding floor (CAL-CST-07), so the gate passes. (Openwork previews,
  2026-09-25; minis-02 twist, same day.)
- **Twist minis**: height 6, twist 15 on CS-1. CV12 caps the wall lean at 45°, about 2.5° of twist
  per mm of height at a 40 mm hexagon; twist 20 at height 6 fails. CS-2's pattern is too dense at
  40 mm to show holes even at 1.6 mm, so the twist sample is CS-1's. (minis-02 header.)
- **Pegs frame**: leave `frame` at the file's default (`depth + clearance + 2.5`); narrower breaks
  CV8 on CS-2 at 90 mm and the kernel refuses anything under `depth + clearance + 1.6`.

## What goes on a different plate

- **Border** carries a `color border …` line, so it needs a colour plate (`bambu slice coaster`).
  Compose drops the colour, so leave border off a compose plate and say so in the header.
  (minis-01.)

## Checks every plate passes before the owner gate

- Every item passes the mesh gate (`--check`) at the exact params on the plate.
- Every item passed the [review-print](../review-print/SKILL.md) look: it reads as its pattern
  at 40 mm and its art fills the shape. minis-03 dropped five minimal-frames on sight
  (2026-09-25). Two were near-solid discs (sDO9, nmEj); three had half-empty or wedge-gapped
  art (n3Ii, lEfW, tA8e). **Omar would rather have fewer patterns than a bad sample.**
- `bambu slice compose <plate> --dry-run` places every item.
- The header names each style by its name in `coaster-styles.md` and lists what was left off and
  why. A sample dropped with no reason written down is a gap the next session cannot see.
- Nothing is sent. The send, the filament and whether to print at all are Omar's.
