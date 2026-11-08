---
date: 2026-11-08
repo: 3d-models
session: plates-and-feedback
branch: plates/ball-1
folded: no
---

## Snags
- `tools/print_review.py` G-code reader: a push of filament with no move (a G1 with only E) was
  counted as a support line at the last position, which made 46 false hits inside the ball. Fixed
  with a self-test; any new G-code reader here should skip moves whose X and Y do not change.
- Studio's sliced 3MF re-centres each part, so a component's transform is no longer the identity
  after a slice. A reader that takes mesh points from `3D/Objects/*.model` without applying the
  component transform puts the piece in the wrong place on the bed (my first centre was off by the
  whole bed offset).
- "On build plate only" (`support_on_build_plate_only`) does not keep support out of a hollow
  lattice: columns from the bed rise through the windows. Tree supports also bend round a support
  blocker (621 runs inside). Plain supports plus a blocker is what worked.

## Worth copying
- Proving a slicer setting by reading the G-code, not the preview picture: the preview showed
  nothing wrong while the G-code had supports in the hollow.
- Not tuning the check's radius to make it pass: the three nubs that remain are written on the page
  with a close-up, and the question after the print asks about them.
