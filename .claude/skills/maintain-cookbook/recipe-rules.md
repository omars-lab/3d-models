# Recipe rules

Read every run. Add a rule when a recipe comes back wrong, and say which recipe taught it.

## The picture

- **Vary one thing.** Every tile shows the same snippet with one piece of text changed. Two
  changes at once and the reader can't tell which did what.
- **The picture must show the claim.** If the text says "a wider band fits fewer chevrons",
  the tiles must show fewer chevrons. Look at the PNG before writing the sentence, not after.
  If what you see disagrees with what you expected, the render wins; `hankin-angle` taught
  this (a small angle barely dents the polygon, against the reference's wording).
- **Keep the drawing the same size across tiles.** Each tile is rescaled to fit, so a
  variant that makes the drawing bigger looks the same size as one that doesn't, and a
  "bigger" effect disappears. Vary a shape, not the overall size; if the size is the point,
  say in the text that the tiles are scaled.
- **Big enough to see.** At 360 pixels a tile loses anything under a millimeter or so on a
  90 mm coaster. Pick values far enough apart (`width 2 | 4 | 7`, not `2 | 2.5 | 3`).
- **A single picture is the exception.** Only when nothing sensible varies (a whole
  construction, a styled result, two coasters mated).

## The snippet

- **Smallest that works.** Cut a real pattern down rather than inventing geometry.
- **Reserved words can't be names.** `hex`, `rosette` and the other statement words fail
  as identifiers ("Expected Identifier, got hex"). Use `corners`, `rosette_`.
- **A coaster's art is used at its drawn size in mm.** A star of radius 30 on a 90 mm
  outline leaves room; a radius near 45 must reach the frame on purpose (openwork) or it
  is refused.
- **Colors come from the inscribed pattern's palette.** A coaster can only name colors in
  the palette of the pattern it inscribes.

## The words

- **Plain words, American spelling.** "color", "center", "gray", "neighbor". Identifiers
  and file names keep their own spelling (`coaster-color-design.md`).
- **"Watch out" is the mistake people actually make**, with the check name bikar reports
  (CV2, CV7) when there is one, so a reader can match the error they got.
- **Reference by GitHub URL**
  (`https://github.com/NaqshCoffee/bikar/blob/main/docs/language-reference.md#...`), never
  by a relative path into a sibling checkout.
- **Mark only what is harvested.** `covers:` takes a word from
  `python3 .claude/gates/cookbook_coverage.py --list`. Prose-only clauses (`weave`) can be
  explained but not marked.
- **Related links both ways.** When a recipe links to another, check the other links back
  if it's the natural next read.
