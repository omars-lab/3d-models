---
name: place-pins
description: Choose where the pins go on a split coaster, ring by ring round its centre, and write the choice into the plate. Draws the cut face with every ring that has room for a pin, each in its own color with a letter, its radius and its pin count, so Omar can mark which rings to keep, drop or add; then puts the kept rings into the plate's params and checks the pins picture. Use for "radial pin placement", "pins round the centre", "more pins round the middle star", "too many pins on the border", "fewer pins on the outside", "where do the pins go", "a ring of pins", "remove the red, add the blue" on a pins picture, or any change to how many pins a split coaster has or where they stand.
---

# place-pins — pins in rings, chosen from a picture

A split coaster is held shut by pins standing on the lower half's cut face, each going into a hole
in the upper half. Until split-06 the kernel picked the spots itself: every spot with room, at
least `stud_spacing` apart. That put 31 pins round the border and none round the middle star,
which is the opposite of what Omar wanted ("i want more pins around central star", "too many pins
around border", then a picture marked "remove redC add blue", 2026-10-23).

A rosette repeats round its middle, so a spot that has room in one repeat has room in all of them.
That makes a **ring** the natural unit: one radius, one turn, one pin per repeat (or two). Omar
picks rings, not spots, and the coaster file takes the rings he picked.

## Two things that decide the room

- **The pin size.** A pin needs half its width plus half the play (`stud_gap`) plus a 0.9 mm wall
  round its hole: 1.625 mm of room from its centre for a 1.2 mm pin at 0.25 mm play.
- **The hidden groove.** Each loose piece's rim (its flange) sits in a groove cut 0.8 mm into the
  strap on each side, at the halves' cut. That leaves only the middle of the strap for a pin. On
  the flange coaster at 112.5 mm the ring round the middle star has room for a 0.71 mm pin at
  most. **Pin bosses** fill the groove in a small disc round each pin, in both halves, and notch
  the piece's rim to match, so the pin gets the whole strap width. Omar picked this on 2026-10-23
  ("Fill the hidden groove at each pin").

So measure at the height that matches the coaster: just under the cut (2.05 mm on a 4.4 mm
coaster) without bosses, low in the lower half (0.5 mm) with them.

## The flow

1. **Render the lower half** at the plate's params (the plate's `.yaml` items), with bikar's CLI:
   `node <bikar>/packages/cli/dist/index.js render <file.bkr> --format stl --piece Lower --param …  -o <scratch>/lower.stl`.
2. **Draw the ring map**: `ring_map.py` (below). Read the picture yourself. Each ring is one color
   and a letter; the legend gives its radius, its pin count and the turn of its first pin. Rings
   with an odd count, or a count that is not a multiple of the rosette's repeats, are a greedy
   pick's leftovers: name them as such, do not offer them as a ring.
3. **Ask Omar from the picture.** Send it (SendUserFile) with one free-text question: which rings
   to keep, drop or add. He may mark the picture instead; read his marks against the letters.
   When he marks a few pins, take it as their whole ring in every repeat and say so.
4. **Write the rings into the plate.** Each kept ring is three params on every item of the plate:
   `stud_ringN` (radius, mm), `stud_ringN_n` (pins) and `stud_ringN_turn` (degrees from +x of the
   first pin), N = 1 to 5; add `stud_boss: 1` when a ring stands where the groove was. Any ring
   turns the automatic pick off, so a pin the old layout had and you want kept must be in a ring
   too. A pin stands exactly where its ring puts it when that spot has room, so every repeat
   matches; only a pin without room there moves, to the roomiest point within 1.5 mm, and a pin
   with no room in reach is refused, naming the ring and the angle: draw the map again, do not
   loosen the wall. When Omar asks for a ring on a circle that has no room (split-06's stars, at
   35.3 mm), use the nearest radius on the same line that has room, and say how far in it moved. `--check` on the
   render lists every pin's radius and angle, so read the old layout's rings off it. split-06 was
   the first ([the plate](../../../docs/design/plates/split-06.md); bikar's pin rings and bosses).
5. **Check it.** Render the lower half again and draw the plate's pins picture
   (`python3 tools/print_review.py pins <png> <lower.stl>`). The pins must stand where Omar's
   marks are, and only there. Then slice the plate and check that no pin disc bites a piece's
   hidden ledge: `ledge_check.py build/plates/<name>.plate.3mf` (below). With `stud_boss: 1` a
   disc round each pin notches every ledge it reaches. On split-06 the discs flattened the pink
   hex pieces' points and clipped their shoulders, so the ledge there reached 0.17 mm past the
   face instead of 0.8 mm, and those pieces wiggled while the green ones, with the same face,
   held (Omar, 2026-10-24: "the blunt pieces wiggle more than the pointy kites"). A bitten piece
   means the ring moves, not the check: draw the map again and pick a radius whose discs miss
   the points. Then update the plate's page: pin count, where they stand, and the questions
   after the print (is it flush round each kept ring; do the notched pieces still sit).
   The send runs the same ledge check on every plate with a split-flange piece and refuses a
   bitten one (`.claude/skills/send-plate/plate-checks.yaml`), so this step finds it early.
6. **A recipe change resets the yes**: `plate_approve.py <page> --iterate` (manage-approvals).

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/ring_map.py` | Finds every spot on the cut face with room for a pin, groups them into rings by radius, and draws the face with each ring lettered and colored, with a legend (radius, pins, first turn); prints the same as lines | Step 2, and again whenever the pin size, the strap width or the bosses change | `python3 .claude/skills/place-pins/scripts/ring_map.py <lower.stl> --z 0.5 --stud 1.2 --gap 0.25 --out <map.png>` |
| `tools/split_sites.py --rings 1` | The widest room in each 1 mm ring out from the centre, and the biggest pin it takes | To answer "how big a pin fits round the middle" without a picture | `python3 tools/split_sites.py <lower.stl> --z 2.05 --stud 1.2 --gap 0.25 --rings 1` |
| `scripts/ledge_check.py` | Reads a sliced plate and, for every loose piece, checks that its ledge reaches past its face by the ledge's own width along every side and round every corner; names each bitten corner by its angle and how far the ledge reaches, and each object by its bed-map label; exit 1 when any piece is bitten. With `--recipe`, a recipe that says `ledge_bitten_by_design: "<why>"` (a plate testing the bite, split-08) turns it round: exit 0 only when a piece is bitten. `--draw DIR` writes one picture per set (the recipe's `group:`): face grey, ledge orange, each bitten corner ringed blue with its reach. A piece with its id carved in its face is checked like any other: only an object whose holes take over a quarter of its outline is a half and skipped (the first run on split-08 skipped every piece with an id). PASS: split-02 and split-05 (no discs). FAIL: split-06 as printed (pink hex point 0.17 mm, blunt ends 0.25 and 0.46 mm, against 0.8 mm along the sides) | Step 5, after every slice of a plate with pins, and `--draw` for the page's ledge pictures; the send runs it with `--recipe` (plate-checks.yaml); `make validate-print-review` runs its self-test (a clean kite passes, the bitten one fails, the by-design recipe turns both round, `--draw` writes one picture) | `python3 .claude/skills/place-pins/scripts/ledge_check.py build/plates/<name>.plate.3mf [--recipe docs/design/plates/<name>.yaml] [--draw docs/design/plates/<name>-media] [--tol 0.25]` |
| `tools/print_review.py pins` | The plate's pins picture: the lower half from above, each pin a white square | Step 5, and for the plate page | `python3 tools/print_review.py pins <png> <lower.stl>…` |

`ring_map.py` imports `tools/split_sites.py` by walking up to the repo root, so the room is
measured one way in both.

## Rules

- **Rings, not spots.** A pin that is not part of a ring breaks the rosette's symmetry and holds one
  repeat tighter than the rest.
- **Keep the wall.** 0.9 mm round the hole is bikar's socket wall by default; a pin that fits only
  with less is a pin that does not fit. The wall is a setting since bikar #345 (`studs … wall
  <mm>`, `stud_wall`, at least one 0.4 mm line), and [split-08](../../../docs/design/plates/split-08.md)
  tests 0.7 and 0.45 mm beside 0.9; until it is judged, keep 0.9 (D-118).
- **Quality first.** Fewer pins where they hold beat many where they show: a boss changes the
  piece's rim, so the page asks whether the notched pieces still sit flush.
