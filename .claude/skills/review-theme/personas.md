# Personas and rubric for review-theme

Read this file on every run, before looking at any picture. It is kept apart from SKILL.md so the
personas can get sharper without the skill changing. `reviews.py check` reads the persona ids
from the table below, so a persona added here is one every review must then cover.

**These are made-up people.** A score is Claude imagining how such a person might react to a
flat picture. It is not customer research, nobody was asked, and a high score is a hunch about
taste, not a forecast of sales. Say so wherever the scores are shown.

## The six personas

| Id | Name | Cares about | Put off by |
|---|---|---|---|
| `espresso-purist` | Espresso purist | Restraint and dark, roasted tones; one or two colors that let the pattern carry the piece; a coaster that sits quietly under a small cup | Bright, toy-like colors; more than three colors; anything that looks like a novelty |
| `latte-regular` | Latte-and-pastry café regular | Warm, soft, friendly colors (milk, caramel, pink, cream); something cheerful that looks nice in a photo next to a cake | Harsh black-and-neon contrast; cold or stark looks; a pattern so busy it reads as noise |
| `cold-brew-minimalist` | Cold-brew minimalist | Few colors, clean contrast, cool or neutral tones; a shape that reads clearly from across the table | Many colors; warm busy palettes; low contrast that turns the pattern to mush |
| `third-wave-fan` | Third-wave specialty fan | Something with a story: the colors of an origin, a craft, or a place; a palette that feels chosen, not default | The printer's stock colors used just because they were loaded; looks that feel generic or mass-made |
| `gift-buyer` | Gift buyer | Reads as a finished, giftable object at first glance; a "safe but special" palette that suits someone else's kitchen | Anything that looks like a test print; colors a recipient might dislike; a look that needs explaining |
| `cafe-owner` | Café owner buying sets | Looks good as a set of six or twelve, survives daily use, fits a range of café interiors, and is cheap to make again (few plates, few colors to stock) | Many plates per coaster; colors to buy that are used nowhere else; pale colors that show coffee stains |

## The rubric

Each persona gives every theme a whole number from 1 to 5, with a one-line reason in their own
terms. The reason names what in the picture drove the score, not a general opinion.

| Score | Means |
|---|---|
| 5 | They would pick this one out of the set and want it |
| 4 | They like it; small things they would change |
| 3 | Fine, nothing they would reach for |
| 2 | It misses what they care about |
| 1 | It hits what puts them off |

How to score:

1. Look at the picture itself (the PNG, or the SVG in the gallery), not only the color names. Two
   colors with good names can still blur together on the coaster, and a tiny group (the gBV
   kites are almost hidden by the straps) counts for less than its row in the table suggests.
2. Read the theme's heads-up lines and its plates and cost from `themes.py check`. The café owner
   weighs the plate count and the colors to buy; the other personas mostly ignore cost.
3. Keep the personas apart. A theme can be a 5 for one and a 1 for another; that spread is the
   useful part, so do not round everyone toward 3.
4. The overall line is one sentence: who it is for, and the main thing holding it back. It is
   not an average, and the gallery shows the mean of the six scores beside it.
5. A color that is to buy is judged by its hex, the maker's label for it. The finish (matte or
   basic) and how close the screen is to the spool are unknown, and a reason may say so.
