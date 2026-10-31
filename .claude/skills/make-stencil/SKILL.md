---
name: make-stencil
description: Make a thin, bendable tracing stencil for kids or a class to draw a shape on ordinary paper (a flag's emblem, an animal, a letter, a logo), sized so the finished drawing fills a sheet of Letter or A4: the outline from a public-domain SVG, a 0.6 mm card as tall as the paper with the shape cut out and grown for crayons, notches that line it up on a folded sheet, then a plate page with pictures and one after-print question. Use for "make a stencil", "a stencil to trace", "a tracing card", "something the kids can trace around", "a cut-out to draw around on printer paper", or another card like cedar-stencil-1.
---

# make-stencil — a tracing card for drawing a shape on paper

Omar asked for this on 2026-10-30, after the cedar card printed: "i like the thickness of the
print, we should have a skill to make similar stencils like this with the technique/approach we
took". The worked example is [cedar-stencil-1](../../../docs/design/plates/cedar-stencil-1.md):
the Lebanon flag's cedar, for a pre-K class drawing the flag on a sideways Letter sheet. Its source
[`LebanonCedar.scad`](../../../src/Stencils/LebanonCedar.scad) is the file to copy for a new one.

## What a stencil here is

One flat card that prints in about 30 minutes:

- **0.6 mm thick, three 0.2 mm layers.** It bends like a plastic sheet and springs back. Omar
  picked "thin, maybe a few layers, not too thick, still bendable", and liked the result in hand.
  Go to 0.8 mm only when a print shows the card creasing or tearing.
- **As tall as the paper,** so its top and bottom edges sit flush with the sheet's and it can only
  go at the right height. The width is the opening plus a 16 mm border each side.
- **V-notches, 6 mm,** at the middle of the top and bottom edges, to line up with a fold down the
  sheet's middle, and on the sides wherever the grown-up needs a pencil mark (the cedar's mark the
  stripe lines). Corners rounded at 6 mm.
- **The opening grown 1.5 mm all round.** A crayon is 8 to 11 mm across and can't get into 2 to
  3 mm tips of the exact outline. The scale is set so the grown opening, the line a child
  traces, spans exactly the space it should fill on the page.
- **The card only, not the loose cut-out,** unless Omar asks for it (cedar: "i want the bigger
  piece, not the smaller one").
- **No carved id.** It is a classroom tool and an id would show up in the traced line; the recipe
  gives a `no_id` reason.

## Steps

1. **Pin down the drawing.** What gets traced, on which paper (Letter unless told), which way up,
   and who traces it (crayons for small children). Then decide what the finished page looks like
   and **fill the sheet** unless told otherwise. The first cedar card drew an official 2:3 flag
   inside the sheet, and Omar's first question was whether it fit an 8.5 × 11 in flag. Size from
   the paper, never from the shape's own official proportions, and say on the page if they differ.
2. **Get the outline.** Find a public-domain SVG (Wikimedia Commons is the usual source), keep it
   in `src/Stencils/` and name its source in the `.scad` header. Write the outline with
   `svg_outline.py` (table below). Never `import()` the SVG into OpenSCAD: Bambu Studio refused
   to slice the card with the cedar imported that way. Inner subpaths (details inside the shape)
   are left out so the opening is one hole.
3. **Write the `.scad`** by copying `LebanonCedar.scad`. Keep its contract: a `part` variable with
   `"sheet"` (the card that prints) and `"paper"` (the finished drawing on the sheet, with the
   card's outline where it sits). Keep the knobs at the top too: `paper`, `thick`, `grow`,
   `sheet_w`, `notch`, `corner`. Set the scale `k` from the span on the page the opening must fill.
4. **Render** the STL and the page's two pictures with `render_stencil.py`. Open both. In
   `on-paper.png` the drawing should fill the sheet and the opening should touch what it must
   touch. In `pieces.png` look for slivers of card under 3 mm between parts of the shape: those
   are the weak spots, named on the page.
5. **The plate.** Copy [`cedar-stencil-1.yaml`](../../../docs/design/plates/cedar-stencil-1.yaml)
   (one item with the STL's sha256, a label, `no_id`, an `id_code`), then
   `tools/bambu/bin/bambu slice compose docs/design/plates/<plate>.yaml`. It must fit one bed. The
   card is at most 216 mm tall on Letter, but a second piece beside it spills: the X2D's usable
   width is about 235 mm. Copy `build/plates/<plate>.plate.preview.png` to the media folder as
   `bed.png`.
6. **The page.** Copy cedar-stencil-1's page. Keep its sections: in short, the drawing on the page,
   the card, the assumptions made, on the bed, after the print, approvals, timeline. The
   after-print row is one question, Do and Look for. It has at most four answers written as
   `Label: what it changes.` sentences, or the hub shows no buttons
   (`after_print.py measure` and the judging page show it). Run `python3 .claude/gates/plates_gate.py --write` and ship
   it (branch, PR, merge). Printing it is [send-plate](../send-plate/SKILL.md), on Omar's yes.

## Scripts — when to use each

| Script | What it does | When to use it | Command |
|---|---|---|---|
| `scripts/svg_outline.py` | Flattens one SVG path's outer edge into an OpenSCAD polygon (SVG px, y up, the SVG's middle at the origin), cleaned into one valid shape | Step 2, once per new shape, or when its SVG changes | `uv run --with svgelements --with shapely python .claude/skills/make-stencil/scripts/svg_outline.py <svg> --fill "<color>" --var <name>_outline --out src/Stencils/<name>-outline.scad` (`--id` picks a path by id, `--subpath` another edge, `--origin X,Y` another middle) |
| `scripts/render_stencil.py` | Renders the card's STL (`part="sheet"`), prints its sha256 for the recipe, and draws `on-paper.png` and `pieces.png` | Step 4, and after any knob change | `python3 .claude/skills/make-stencil/scripts/render_stencil.py src/Stencils/<Name>.scad --stl src/Stencils/<name>-sheet-letter.stl --media docs/design/plates/<plate>-media [-D 'paper="a4"']` |

Both rebuild cedar-stencil-1 exactly: the outline's 367 points and the card's sha256
`d8c9158d…` match what printed.

## Rules

- A change to the card after it is approved is a recipe change: new STL, new sha256 in the recipe,
  `plate_approve.py --iterate`, and a new yes (manage-approvals).
- Lead the page with the picture of the finished drawing on the sheet. That picture answers "will
  it fit" before Omar has to ask.
