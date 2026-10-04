---
name: color-themes
description: Make color themes for a loose-piece coaster — which filament color goes on the frame and on each ring of pieces — draw each theme as a picture (silk sheen, sparkle flecks, translucent and two-color spools drawn roughly), check it (pieces that melt into the frame, colors too close to tell apart, colors we would have to buy), say how many one-color plates it takes and roughly how long and how much plastic, and write the construction's inspiration gallery page in `docs/design/coaster/themes/`. Its colors come from a catalog of every Bambu filament color (`catalog.py`: built from Bambu Studio's own list, drawn as swatch sheets, `refresh` reports what Bambu added on GitHub), and `suggest --helper gradient` steps from one color in the middle to another at the rim through the nearest real colors. Use for "color themes", "color combinations", "what colors should the pieces be", "mix and match colors", "a palette for this coaster", "an inspiration gallery", "theme ideas for gBV", "a gradient from light blue to dark blue", "silk or sparkle colors", "all the Bambu colors", "pull the latest Bambu colors", or adding a theme or a construction to the gallery. Scoring the themes is the review-theme skill; choosing a theme to print is prioritize-prints and send-plate.
---

# color-themes — color ideas for a coaster, drawn, checked and costed

Omar asked for this on 2026-10-04: "a skill for us to color coordinate different combinations of
infill colors, etc and create themes", with a second skill to rate them as coffee-drinker personas
([review-theme](../review-theme/SKILL.md)) and "an inspiration gallery per construction on how to
mix and match it". The gallery is one generated page per construction, for example
[gbv-themes.md](../../../docs/design/coaster/themes/gbv-themes.md).

## What it assumes, and what it leaves open

It builds on the [piece colors design](../../../docs/design/coaster/infill-color-ux-design.md)
(#538) and does **not** settle that design's four open calls. It takes two working assumptions,
both that design's own picks, so the gallery can be drawn today:

1. **A color per group.** A group is one ring of pieces (one orbit), and the frame is one more
   group. Every piece in a group takes the same color. One odd piece is not offered (call 2).
2. **One plate per color.** Each color prints as its own one-color plate, and the frame rides on
   the plate of its color (call 1). Plates, minutes and grams in the gallery are counted that way.

If Omar picks differently on either call, the plate counts and costs change and the gallery says
the wrong thing; redo both here. Calls 3 (does the color go in the recipe) and 4 (how the Lab
learns the trays) are not touched: a theme writes no plate recipe and reads no printer.

## Real filament only

Every color a theme names comes from [`palette.yaml`](palette.yaml). Nothing else counts:

- **Owned** are the trays the printer reported, with the date they were read. When a spool changes,
  re-read the trays (`bambu filament --json`, which needs the dotenvx key) and edit the list.
- **Buy** are Bambu colors not loaded, each copied from the color catalog,
  [`catalog.yaml`](../../../docs/design/coaster/themes/catalog/catalog.yaml): every color Bambu
  Studio ships (314 in 02.08.02.61), with its code, line, name, hexes and finish, written by
  `catalog.py build` from the app's own list ([where it comes from](../../../docs/research/2026-10-04-bambu-filament-color-catalog.md)).
  `themes.py --self-test` fails when a buy color's code is not in the catalog, its name, line or
  hex differs, or its line is not in the catalog's `coaster_lines` (the PLA lines and four PETG
  lines). To add a color, find it on [the catalog page](../../../docs/design/coaster/themes/bambu-color-catalog.md)
  and copy its row into `palette.yaml`; `suggest --helper gradient` prints the rows for the colors it picks.
- **New colors from Bambu.** `catalog.py refresh` fetches the same list from Bambu's GitHub repo
  and reports colors added, removed or changed since the installed app. It writes nothing: the
  catalog follows the slicer on this machine, so rebuild with `build` after the app updates.
- A theme never writes a hex. A hex is the maker's label, not a measured print. The pictures draw
  finishes roughly (a light band for silk, dots for sparkle, half see-through for translucent), and
  a two-color or gradient spool as its colors in stripes: where along the spool the color changes
  cannot be predicted per piece, and `check` says so.

## The workflow

1. **New construction only.** Make `docs/design/coaster/themes/<id>/themes.yaml` (copy
   [gbv's](../../../docs/design/coaster/themes/gbv/themes.yaml)): the frame and pieces sources in
   bikar, the print sizes, the plate whose slice prices it, and the groups by orbit. Then
   `themes.py base <id>` and `themes.py measure <id>`. Both run bikar (set `BIKAR_DIR` to a bikar
   checkout at main). The frame file must not have a palette of its own; the script adds a marker
   palette to a copy so each group's faces come out in a color it can find.
2. **Write themes.** Six to ten per construction, each with an id, a name, a one-line mood and a
   color for every group, frame included. The helpers give a starting point to edit:
   `suggest --helper match-trays` (the trays only, darkest on the frame),
   `--helper alternate --colors a,b[,frame]` (rings take turns),
   `--helper one-color --colors a`,
   `--helper gradient --from <id|code> --to <id|code> [--reverse]` (the middle at one color, the
   rim at the other, each ring the nearest catalog color on the way, no ring going back; the frame
   is the neutral furthest from the outer ring). Paste what it prints and give it a real mood line.
3. **Render and look.** `themes.py render <id> --png <scratch dir>` writes every picture, plus PNGs
   to look at. Open every one (the Read tool shows a PNG). A theme that looks wrong is wrong
   whatever its numbers say: small groups hide under thick straps (gBV's kites), and two colors
   that pass the check can still look muddy.
4. **Read the check.** `themes.py check <id>` prints each theme's colors, its heads-up lines and its
   plates with minutes and grams. A heads-up is not an error; a theme can keep one on purpose (the
   all-green baseline melts into its frame), but say so in its mood.
5. **Review.** Run [review-theme](../review-theme/SKILL.md) on every new or recolored theme.
6. **Gallery.** `themes.py gallery <id>` writes `docs/design/coaster/themes/<id>-themes.md`, themes
   ordered by score. Never edit that page by hand; edit the data and run this again.
7. **Gate.** `make validate-color-themes` (also run by `make validate` and the pre-commit hook
   `50-color-themes`) fails when a picture, a review or a gallery page is out of date with the data.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/themes.py base` | bikar draws the coaster flat, each group's faces in its marker color, to `base.svg` | A new construction, or its source or sizes changed | `python3 .claude/skills/color-themes/scripts/themes.py base gbv` |
| `scripts/themes.py measure` | bikar makes each group's STL; their volumes go to `volumes.yaml` for the cost split | Same as `base` | `python3 .claude/skills/color-themes/scripts/themes.py measure gbv` |
| `scripts/catalog.py build` | Reads Bambu Studio's color list and writes `catalog.yaml` | After Bambu Studio updates | `python3 .claude/skills/color-themes/scripts/catalog.py build` |
| `scripts/catalog.py refresh` | Fetches the list from Bambu's GitHub and reports added, removed and changed colors; writes nothing | "Are there new Bambu colors?" | `python3 .claude/skills/color-themes/scripts/catalog.py refresh` |
| `scripts/catalog.py sheets` | Draws a swatch sheet per coaster line (owned and buy marked) and the catalog page; `--png` also writes PNGs | After `build` or a `palette.yaml` edit | `python3 .claude/skills/color-themes/scripts/catalog.py sheets --png <scratch>/png` |
| `scripts/catalog.py check` | Fails when the catalog, its sheets or its page are out of date | `--quiet` is what the gate runs | `python3 .claude/skills/color-themes/scripts/catalog.py check` |
| `scripts/catalog.py --self-test` | Finish labels, the multi-hex reading and the refresh diff on fixtures | Before changing the script; the gate runs it | `python3 .claude/skills/color-themes/scripts/catalog.py --self-test` |
| `scripts/themes.py suggest` | Prints a starting theme from a helper | Starting a theme from the trays, alternating rings, or one color | `python3 .claude/skills/color-themes/scripts/themes.py suggest gbv --helper alternate --colors pink,green,black` |
| `scripts/themes.py suggest --helper gradient` | Steps from one color in the middle to another at the rim through the nearest catalog colors, and prints the palette rows to add | A light-to-dark or one-hue-to-another theme | `python3 .claude/skills/color-themes/scripts/themes.py suggest gbv --helper gradient --from ice-blue --to dark-blue` (`--reverse`, `--lines "PLA Matte,PLA Basic"`) |
| `scripts/themes.py render` | Draws every theme's picture (SVG, and PNGs with `--png`) | After any edit to `themes.yaml` or `palette.yaml` | `python3 .claude/skills/color-themes/scripts/themes.py render gbv --png <scratch>/png` |
| `scripts/themes.py check` | Colors, heads-ups, plates and cost per theme; fails on stale pictures or gallery | After rendering; `--all --quiet` is what the gate runs | `python3 .claude/skills/color-themes/scripts/themes.py check gbv` |
| `scripts/themes.py gallery` | Writes the construction's gallery page | After the reviews are in | `python3 .claude/skills/color-themes/scripts/themes.py gallery gbv` |
| `scripts/themes.py --self-test` | Buy colors against the catalog, the color math, the gradient helper, the finish drawing, and the checks on a three-piece fixture | Before changing the script; the gate runs it | `python3 .claude/skills/color-themes/scripts/themes.py --self-test` |

## How the numbers are made, and where they are weak

- **Neighbors** are groups whose faces share an edge in bikar's flat drawing; the frame touches
  every group. A strap runs between any two pieces, so two pieces in one color are fine. A piece in
  the frame's own color melts into it, and the check says so.
- **Too close** is a CIE76 color difference under 20, between neighbors. The 20 was picked by
  eye on the gBV renders; nothing measured says what a person can tell apart across a strap on a
  printed coaster. Tune it on the first two-color prints.
- **Minutes and grams** split the construction's one-bed slice (gBV: sheets-04g, 86 min, 27 g) by
  each group's share of the plastic. Minutes do not follow volume exactly, and each extra plate
  adds a start-up that has not been measured, so a plate of a few minutes' plastic takes longer
  than its share says. They are for comparing themes, not for planning a print day.

## Why this is a skill and not a gate

The two process evaluations in [dsl-extension-skill-evaluation.md](../../../docs/design/process/dsl-extension-skill-evaluation.md)
and [issue-register-evaluation.md](../../../docs/design/process/issue-register-evaluation.md) both
turned down a proposed skill: one overlapped two skills that already covered it, and the other
was a defect class that a gate catches better than prose. Neither applies here. Omar asked for
this by name. It is a creative workflow that will be repeated for each construction and each new
spool, not a kind of defect. No other skill covers it: [prioritize-design](../prioritize-design/SKILL.md)
picks patterns, not colors, and the piece colors design is a screen that has not been built. The
parts that can be checked are a gate (`make validate-color-themes`), as those evaluations ask.
