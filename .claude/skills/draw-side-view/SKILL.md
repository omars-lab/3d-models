---
name: draw-side-view
description: Draw a labeled cut-through side view of a coaster or a piece from a short YAML description: the lower and upper halves, the pieces, pockets, air gaps, studs, sockets, dovetails, lips and flanges, with the first layer (solid blue) and the last layer (orange dashed) marked, labels with leader lines, dimensions, a print bed, and notes, written as an SVG and a PNG beside the description. Use for "draw a side view", "a cut-through picture", "a cross-section", "show how the halves fit", "show the dovetail", "how does the piece sit in the lip", "draw the join", "how do the two halves print", or any picture of a join, lip, stud, pocket or dovetail for a design doc or a calls page. It is the schematic kind of picture; a side cut taken from a real mesh is `tools/print_review.py side`.
---

# draw-side-view — labeled cut-through pictures from a short description

Omar asked for this on 2026-10-08 (review thread dunuoe, on the 2026-10-05 calls page): "do we
have a good skill to draw these kinds of svgs? I enjoy them". The look is the one in
[way-a-cut-pieces.png](../../../docs/working-model/feedback-requests/2026-10-05-open-calls-media/way-a-cut-pieces.png):
dark gray for the lower half, light gray for the upper half, gold and teal for the pieces, white for
air, solid blue for the faces printed on the bed and orange dashes for the faces printed last. The
first picture drawn with it is
[way-a-dovetail.png](../../../docs/working-model/feedback-requests/2026-10-05-open-calls-media/way-a-dovetail.png),
way a with a dovetail across the cut.

## The flow

1. **Write the description** next to the page's pictures, named `<name>.side.yaml` (copy
   [way-a-dovetail.side.yaml](../../../docs/working-model/feedback-requests/2026-10-05-open-calls-media/way-a-dovetail.side.yaml)).
   It has a `title`, optional `columns` (default 2) and a list of `panels`. Each panel has a
   `title`, a `width` in mm when anything is mirrored, an optional `scale` [px per mm across, px per
   mm up], its `parts`, and `notes` and `warn` lines under it. Sizes are in mm, `x` across and `z`
   up from the bed.
2. **Draw it.** The SVG and the PNG land beside the description, `<name>.svg` and `<name>.png`.
3. **Look at the PNG** before using it: labels that crowd, a leader that crosses another piece, a
   panel far wider than the rest. Fix with `label_at`, `label_side: left` or a smaller `scale`,
   then draw again.
4. **Put the PNG in the page** with a relative link, and a line saying what it shows.

The default scale is 18 px per mm across and 36 up, so thin layers can be seen; the legend then
says "Not to scale." Give a panel a square `scale`, such as [32, 32], to draw it to scale.

## The parts

`kinds` prints every part with its keys. In short:

| Part | What it draws | Needs |
|---|---|---|
| `half` | the lower (dark gray) or upper (light gray) half of the coaster | `side`, `box` |
| `lip` | the ledge on a half that holds a piece | `side`, `box` |
| `piece` | a loose piece, gold by default | `box` |
| `flange` | a piece's rim that sits on a lip | `box` |
| `pocket`, `air` | a hole or an air gap, white | `box` |
| `stud`, `socket` | a peg (by `side` or `color`, its free end `toward` up or down) and the hole it goes into | `box` |
| `dovetail` | a stepped rail and its slot: `width` at the root, `height`, `flare` a side at the top, `gap` a side, slot `depth`, layer `steps`, `toward` up or down, `show` both, rail or slot | `at`, `width`, `height`, `flare` |
| `seam` | a dashed line where two parts meet | `line` |
| `bed` | the print bed, with its words | `line` |
| `arrow`, `dim` | an arrow (words optional), a dimension | `from`, `to`; a dim also `text` |

Every part also takes `both: true` (mirrored about the panel's middle), `first` and `last` (the
faces printed first and last, `top` and/or `bottom`), `label`, `label_at` (where the leader
points) and `label_side` (`left` or `right`, default right). A box is `[x, z, width, height]`.

It refuses what it cannot draw honestly, with the reason: a dovetail whose `flare` is not bigger
than its `gap` (the rail would lift straight out, so it would not be a dovetail), a slot shallower
than its rail, layer steps that do not divide the rail into whole layers, an unknown part or key, a
color that is not one of its piece colors, and a part outside its panel.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| [`side_view.py draw`](scripts/side_view.py) | Draws one description into an SVG and a PNG beside it | Every new or edited side view | `python3 .claude/skills/draw-side-view/scripts/side_view.py draw <name>.side.yaml` (`--no-png` for the SVG alone, `--zoom 2` sets the PNG size) |
| [`side_view.py check`](scripts/side_view.py) | Fails when a description under `docs/` has no SVG, an SVG older than its description, or no PNG | Before a commit; hook `52-side-views` and `make validate-side-views` run it | `python3 .claude/skills/draw-side-view/scripts/side_view.py check` |
| [`side_view.py kinds`](scripts/side_view.py) | Prints every part kind with its keys | Writing a description | `python3 .claude/skills/draw-side-view/scripts/side_view.py kinds` |
| [`side_view.py --self-test`](scripts/side_view.py) | Draws a fixture with every part kind, checks the marks, labels, legend, the stepped rail and every refusal, and that `check` catches a stale picture | After changing the script | `python3 .claude/skills/draw-side-view/scripts/side_view.py --self-test` |

The PNG is made by `rsvg-convert` (`brew install librsvg`).
