# naqsh cookbook

Short recipes for the naqsh language (the language bikar reads, in `.bkr` files). Each
recipe is one idea:
- a few lines of code;
- a picture of that code drawn three times, with **one** thing changed each time, so you
  can see what that one thing does;
- a "Watch out" line for the mistake people actually make with it;
- links to the recipes it builds on.

In the flat pictures, the finished lines are black. The helper circles and lines they were
built from are drawn thin, gray and dashed. bikar normally hides them, but they are how
you read a construction. The coaster pictures are 3D previews.

The full rules for every statement are in bikar's
[language reference](https://github.com/NaqshCoffee/bikar/blob/main/docs/language-reference.md).
To turn a GeoGebra construction into naqsh, use bikar's
[GeoGebra to naqsh cookbook](https://github.com/NaqshCoffee/bikar/blob/main/docs/cookbook/geogebra-to-naqsh.md).

## The pages

Roughly in the order you'd build a pattern:

1. [Circles, divisions and points](scaffold.md): divide a circle, join its points, name
   points and build a shape from them.
2. [Lines, bisectors and crossing points](lines.md): find new points where circles and
   lines cross, the way a compass-and-ruler construction does.
3. [Copies: rotate and mirror](copies.md): draw one piece and let the language repeat it.
4. [Stars and colored faces](stars-and-fills.md): Hankin stars, rosettes, and coloring the
   shapes between the lines.
5. [Weave](weave.md): lines drawn as bands that pass over and under.
6. [Coaster knobs](coaster-knobs.md): turn a pattern into a printable coaster, one knob at a
   time.

## How the pictures are made

Every recipe's code is the real input. `make cookbook` hands each snippet to bikar, draws
the variants, and fails if any snippet doesn't render. So a recipe can't drift out of step
with the language without someone noticing. The pictures live in [img/](img/).

Adding or changing a recipe: use the `maintain-cookbook` skill
(`.claude/skills/maintain-cookbook/`). Its [recipe rules](../../.claude/skills/maintain-cookbook/recipe-rules.md)
say what makes a good one.

## Keeping up with the language

Every statement word in naqsh is either shown by a recipe here or listed below with the
reason it isn't yet. `make cookbook` and `make validate` fail when bikar gains a word that
is in neither place, and name the word. So a new mechanism in the language shows up here as
a job to do, not as something quietly missing.

A recipe marks the words it shows with a hidden `covers:` comment under its heading.
The list below may get shorter at any time; making it longer takes a deliberate override,
so "add it to the list" isn't the easy way out.

## Not in the cookbook yet

- `brick` `mural` `footprint` `height` `studs` `anchors` `engage` `clutch` `origin` `pieces` `blanks` `slivers` — the LEGO-compatible brick and mural blocks; they have their own lab and page in bikar, and a picture needs the LDraw viewer, not the flat render
- `orb` `piece` `tile` `wall` `assembly` `clip` — the 3D bodies beyond the coaster; each has its own gallery pipeline, and a side-by-side needs the orb or piece renderer
- `loose` — loose pieces in a frame (bikar #292); the frame looks the same as the plain coaster whichever ring is loose (the walls only move onto the exact outline), and the pieces are a separate `--piece <color>` output the recipe renderer does not draw yet; next up once it can draw a named piece
- `rim` `edge` `trivet` — coaster knobs whose change is a millimeter at the rim, too small to see in a 360-pixel picture; next up once the coaster picture can zoom to the edge
- `girih` `phyllotaxis` `spiral` `parabola` `hyperbola` — pattern families and curves that draw well flat; not written yet
- `tangent` `offset` `fillet` `face` `segment` `boundary` `extend` `nest` — construction helpers that show well flat; not written yet
- `translate` `invert` `symmetry` — transforms; not written yet (`rotate`, `mirror` and `reflect` are)
- `param` `for` `repeat` — naming a number, loops and recursion; the picture is the same as the plain pattern, so the recipe needs a different kind of illustration
- `animate` `render` `scale` `layer` `wave` `lines` `circles` — drawing and animation settings, not geometry; they change how a render looks, not what the pattern is
