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

- **Not 40 mm — too small.** minis-01 to minis-03 used 40, the Coaster Lab's size chip. Printed,
  minis-03 was "much too small" (Omar, 2026-09-26). The next sample plate goes up to **70 mm**.
  That is a guess, not a measured size: 70 is under the 90 mm full coaster and still fits
  several pieces on a plate. Correct it when that plate comes back. Re-run review-print at the
  new size, because the straps and holes change with it.
- **Straps at 1.6 mm for every style where the holes are the point** — minimal, minimal-frame,
  minimal-pegs, twist. At 40 mm the default 2 mm strap closes the holes up; 1.6 mm opens them and
  is still the freestanding floor (CAL-CST-07), so the gate passes. (Openwork previews,
  2026-09-25; minis-02 twist, same day.)
- **Twist minis**: height 6, twist 15 on CS-1. CV12 caps the wall lean at 45°, about 2.5° of twist
  per mm of height at a 40 mm hexagon; twist 20 at height 6 fails. CS-2's pattern is too dense at
  40 mm to show holes even at 1.6 mm, so the twist sample is CS-1's. (minis-02 header.)
- **Pegs frame**: leave `frame` at the file's default (`depth + clearance + 2.5`); narrower breaks
  CV8 on CS-2 at 90 mm and the kernel refuses anything under `depth + clearance + 1.6`.
- **Pegs: the join is two frames of solid.** With the defaults (depth 3, clearance 0.15), each
  frame is about 5.7 mm. Mated, the two patterns sit about 11 mm apart. At 40 mm that band is
  over a quarter of the piece, and it reads as "big spaces between the patterns" (minis-03,
  Omar, 2026-09-26). The frame width is fixed in mm, so a bigger size shrinks the band's share
  (about 16% at 70 mm). A shallower dovetail (`depth` 2) also allows a narrower frame. Whether
  depth 2 still passes CV8 and still holds is not yet checked: render it and review the pair
  before putting it on a plate.
- **Pegs fit: 0.15 mm clearance was a bit loose** on minis-03 (CS-1 pair, pink PLA, X2D; Omar,
  2026-09-26: "a bit loose"). That is one hand-feel reading, not a measurement. It points
  CAL-FIT-01 tighter but does not settle it. Next time, print a clearance ladder: one pair at
  0.10 and one pair at 0.05, the low end of the file's range.

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
