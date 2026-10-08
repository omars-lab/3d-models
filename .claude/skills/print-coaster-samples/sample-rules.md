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

- **80 mm, half height.** minis-01 to minis-03 used 40 mm, the Coaster Lab's size chip, and
  minis-03 printed "much too small". Omar set the next one on 2026-09-26: "half the hight and 2x l
  and w". So samples are **size 80, height 1.4**: 1.4 mm of frame or slab, and the straps stand
  1.2 mm above it, for 2.6 mm total instead of 5.2 mm. `height` is the Coaster Lab's knob on
  every flat coaster (bikar feat/coaster-height-knob). Re-run review-print at the new size,
  because the straps and holes change with it. (minis-04.)
- **Straps: default 2 mm at 80.** At 40 mm the default 2 mm strap closed the holes up, so
  minis-01 to minis-03 used 1.6 mm, the freestanding floor (CAL-CST-07). At 80 mm the holes
  are open at 2 mm (review-print sheet, 2026-09-26), so keep the default. (Openwork previews,
  2026-09-25; minis-04.)
- **Every sample plate carries a twist.** minis-03 left it off and Omar asked where it was
  (2026-09-26). It is CS-1's, because CS-2's pattern is too dense to show holes as a mini.
- **Twist doesn't halve.** CV12 caps the wall lean at 45°, so the twist allowed is about
  (height ÷ rim radius) radians. At 40 mm that is about 2.5° per mm of height (minis-02: height
  6, twist 15; twist 20 fails). At 80 mm it is about 1.2° per mm: twist 4 at height 4 passes and
  twist 5 is refused at 45.1°. The file's height floor is 4. At the cap the rim leans as far at
  any size; only the total turn shrinks. The 45° cap is a provisional bet (CAL-CST-08). (minis-04.)
- **Pegs frame**: leave `frame` at the file's default (`depth + clearance + 2.5`); narrower breaks
  CV8 on CS-2 at 90 mm and the kernel refuses anything under `depth + clearance + 1.6`.
- **Pegs: the join is two frames of solid.** With the defaults (depth 3, clearance 0.15), each
  frame is about 5.7 mm. Mated, the two patterns sit about 11 mm apart. At 40 mm that band is
  over a quarter of the piece, and it reads as "big spaces between the patterns" (minis-03,
  Omar, 2026-09-26). The frame width is fixed in mm, so a bigger size shrinks the band's share
  (about 14% at 80 mm). A shallower dovetail (`depth` 2) also allows a narrower frame. Whether
  depth 2 still passes CV8 and still holds is not yet checked: render it and review the pair
  before putting it on a plate.
- **Pegs fit: no reading so far counts.** minis-03 at 0.15 mm was "a bit loose" and minis-04
  at 0.10 came back "too tight" (Omar, 2026-09-26). Both are hand feel, and both plates were
  sliced on Studio's built-in defaults, not the X2D preset (elephant-foot compensation 0, not
  0.15; see [`print-quality-design.md`](../../../docs/design/printing/print-quality-design.md)). minis-04 also
  changed size and height along with clearance, and bikar's slot was not yet a true offset of
  the tab (fixed in bikar #262, after both printed). So **do not move CAL-FIT-01 on these two**, and do not read "0.10 is too tight" as a
  rule. The next clearance test is the design's T1 ladder: several pairs at 1.4 mm, one size,
  only clearance varying, sliced after the preset fix. (minis-03, minis-04.)
- **The pegs border is too big even at 80 mm.** Omar, 2026-09-26, on minis-04: "the peg
  system border is too big". The dovetail band there is about 11 mm, as the frame rule gives.
  The narrower joins are on minis-05 (key, tab, plain) and minis-06 (slim dovetail, band
  8.4 mm). Pick from what those show rather than another dovetail pair at the default knobs.

## What goes on a different plate

- **Border** carries a `color border …` line, so it needs a color plate (`bambu slice coaster`).
  Compose drops the color, so leave border off a compose plate and say so in the header.
  (minis-01.)

## Checks every plate passes before the owner gate

- Every item passes the mesh gate (`--check`) at the exact params on the plate.
- Every item passed the [review-print](../review-print/SKILL.md) look: it reads as its pattern
  at its print size and its art fills the shape. minis-03 dropped five minimal-frames on sight
  (2026-09-25). Two were near-solid discs (sDO9, nmEj); three had half-empty or wedge-gapped
  art (n3Ii, lEfW, tA8e). **Omar would rather have fewer patterns than a bad sample.**
- **Every prototype carries its id.** Omar, 2026-10-06, on split-01 and split-02: "mnake sure we
  are adding a label to atleast one main peice so we can distinguish. this proptoty ... every
  proptoty should have an id .. this should be aprt of our skills". Off the bed, two coupons or
  two coasters that differ by a tenth of a millimetre look the same, and the plate's labels stay
  in the slicer. So the plate sets the mark its `.bkr` declares, because the file's own default is
  0, no mark:
  - a split coaster: `id` (1 to 9), on the lower half's bottom face, mirrored to read from below
    (the gBV lip and flange coasters: their cut faces are mostly pocket or undercut);
  - a split coupon: `pair` (1 to 26, a letter), the lower half reading `AB`, the upper `AT`;
  - loose pieces at a ladder of gaps: `<ring>_dots`, the most dots on the biggest piece (the
    tightest gap), one dot on the smallest.
  Ids and letters run on from the last plate's, so no two prototypes on the shelf share one
  (spl-1 is A to N, pkt-1 O to R, split-01 1, split-02 2). A piece too small to take a mark, or
  to take enough dots to count its rungs, says so in the plate header, with how its rungs are
  kept apart instead. The row sits at the piece's widest spot (bikar #324), and a gBV kite at
  size 112.5 still holds only one dot, at gaps 0.05 to 0.15, and none at 0.20 or 0.25.
- `bambu slice compose <plate> --dry-run` places every item.
- **The slice carries the whole preset chain.** minis-03 and minis-04 printed on Studio's
  built-in values for about 54 process and 50 filament settings, because Studio's command line
  does not follow a preset's `inherits`. Their tiny holes and tight pegs fit those values.
  Until `tools/bambu` flattens the chain before slicing, a sample plate says nothing reliable
  about fit or strap width. After that, check that the slice's settings match the preset's.
  (minis-04, 2026-09-26.)
- The header names each style by its name in `coaster-styles.md` and lists what was left off and
  why. A sample dropped with no reason written down is a gap the next session cannot see.
- Nothing is sent. The send, the filament and whether to print at all are Omar's.
