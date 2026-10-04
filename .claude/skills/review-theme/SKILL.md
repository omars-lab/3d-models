---
name: review-theme
description: Score a coaster's color themes through six made-up coffee-drinker personas (espresso purist, latte-and-pastry café regular, cold-brew minimalist, third-wave specialty fan, gift buyer, café owner buying sets) — a 1 to 5 score with a one-line reason from each, and an overall line — after looking at each theme's picture (gradients, silk, sparkle, translucent and two-color spools included), and store the scores beside the themes in `docs/design/coaster/themes/<id>/reviews.yaml`. Use for "review the themes", "rate these color combinations", "what would customers think of these colors", "score the palettes as personas", or after the color-themes skill adds or recolors a theme (its gate fails until the review is redone). Simulated opinions, never customer research. Not for judging a print off the bed (review-print) or a pattern choice (prioritize-design).
---

# review-theme — six coffee drinkers look at a color theme

Omar asked for this on 2026-10-04, beside [color-themes](../color-themes/SKILL.md): "have another
skill to review the combination (as different coffee drinker persona) and rate it". The scores
feed the order of each construction's gallery page.

**These are simulated opinions.** Each score is Claude imagining how one persona might react to a
flat picture. Nobody was asked. A score is good for ranking ideas against each other and for
spotting who a theme is for. It is not evidence of what sells, and nothing here may be quoted as
customer feedback. Every gallery page and every reviews file says so.

## Every run

1. **Read [`personas.md`](personas.md)** — the six personas, what each cares about and is put off
   by, and the 1 to 5 rubric. It is read on every run, so it can sharpen without this file changing.
   `reviews.py check` reads the persona ids from its table.
2. **Look at every picture you score.** Render the PNGs with
   `themes.py render <id> --png <scratch dir>` and open each one. Score what the picture shows, not
   the color names: a group can vanish under the straps, two named colors can blur together, and
   one color can swamp the rest. Silk sheen, sparkle flecks and see-through translucent are drawn
   roughly, and a two-color spool as stripes whose place on each piece is luck; rubric point 5 in
   `personas.md` says how to score them.
3. **Read `themes.py check <id>`** for each theme's heads-up lines, plate count and cost. The café
   owner weighs plates and colors to buy; the others mostly do not.
4. **Write the review.** `reviews.py stub <id> [<theme>]` prints the block with the theme's
   coloring hash and every persona filled in at 0. Give each persona a whole score from 1 to 5 and
   one line of reason in their own terms that names what in the picture drove it. Then write one
   overall sentence: who the theme is for, and what holds it back. Keep the personas apart. A
   spread of 1 to 5 across one theme is the useful result, so do not pull everyone toward 3.
5. **Check, then rebuild the gallery.** `reviews.py check <id>`, then `themes.py gallery <id>`.

When a theme's colors change, its hash changes and `reviews.py check` fails until it is
reviewed again from the new picture. A review is for one coloring, not for a theme's name.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/reviews.py stub` | Prints the block to paste into `reviews.yaml`, with the coloring hash and every persona | Starting a review, of one theme or of all of them | `python3 .claude/skills/review-theme/scripts/reviews.py stub gbv pink-heart` |
| `scripts/reviews.py check` | Every theme reviewed for its current colors; every persona scored once, 1 to 5, with a one-line reason; an overall line | After writing reviews; `--all` is what the gate runs | `python3 .claude/skills/review-theme/scripts/reviews.py check gbv` |
| `scripts/reviews.py --self-test` | The check against a fixture with each kind of mistake (stale hash, missing or unknown persona, score out of range or not whole, two-line reason, a theme reviewed twice or not at all) | Before changing the script; the gate runs it | `python3 .claude/skills/review-theme/scripts/reviews.py --self-test` |

`reviews.py` reuses `themes.py` from the color-themes skill for the coloring hash and the folder
layout, so the two cannot disagree on which coloring a review saw.

## Why this is a skill

Omar asked for it, and like color-themes it is a repeated creative step, not a defect class (the
reasoning against skills for defect classes is in
[issue-register-evaluation.md](../../../docs/design/process/issue-register-evaluation.md)).
The parts that can be checked (coverage, score range, freshness) are gated by
`make validate-color-themes`; the judgment is not, and cannot be.
