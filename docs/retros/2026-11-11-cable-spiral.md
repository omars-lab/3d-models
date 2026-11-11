---
date: 2026-11-11
repo: 3d-models
session: monitor-print-watcher
branch: cable-spiral, PR #1023
folded: no
---

## Snags
- `src/CableSpiral/cable-spiral.scad` (OpenSCAD 2021.01): slopes built from stacked 0.1 mm slabs split
  into separate solids, because `4.0 + n*0.1` leaves hair-thin gaps. Overlapping each slab by 0.01 mm
  fixed it (one bar went from 5 volumes to 1). Any stacked-slab model here needs the same overlap.
- `.claude/skills/draw-side-view`: it draws boxes only, so a lip's 45° underside has to be drawn square
  with a note. A `slope` part kind would have saved a second picture.
- The worktree budget hook (9) blocked a temporary worktree for a one-line fix on another branch;
  switching my own worktree after committing is the way.

- `src/CableSpiral/cable-spiral.scad` `bar()`: the id tab was joined full height to one wall, so on a
  quarter of each bar that wall could not bend, which is the very thing the bar tests. An id tab on
  a test part should touch only what the test does not measure (here, the floor).

## Worth copying
- Two researchers, then a checker, then the doc: the checker's note caught that the research's disc
  size (92 mm) left out half a channel width; the model printed 96.7 mm.
- `-D 'only="X"'` on the test piece to render one part alone traced a render error to one bar in
  seconds.

## Didn't work
- Reasoning about the grip with the cable drawn square in `cut-and-stack.side.yaml`: the doc claimed
  the lip presses on any cable over d, but a round cable clears the 45° underside up to about 1.3 d.
  The second readability review caught it by doing the round-cable sum; check fits against the round
  shape, never the drawing's box.
- Naming the grip ranges ("snug", "loose") before computing the room each leaves: the third review
  found them the wrong way round. The model's `grip` part now prints side room and lift per cable,
  so the names come from numbers.
- `.claude/skills/review-design` loop on a part design: eleven rounds to pass, and four of the fails
  were C8 (a concept explained in words with no picture) or a claim about where a wall bends. Draw a
  picture per mechanism and a zones view of the shape before the first review, not after.
