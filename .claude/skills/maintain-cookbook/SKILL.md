---
name: maintain-cookbook
description: Write or update a recipe in the naqsh cookbook (docs/cookbook/) — a short bkr snippet, a picture of it drawn three times varying ONE thing, a "Watch out" line and links. Use when a naqsh mechanism, keyword, knob or coaster style ships or gets explained ("add a cookbook entry for X", "show what reach does", "a new keyword/mechanism landed in bikar", "cookbook coverage failed on `kw`"), and whenever `make cookbook` or `make validate` names a keyword with no recipe. Also for shrinking the "Not in the cookbook yet" list. NOT the GeoGebra import walkthrough (bikar's docs/cookbook/geogebra-to-naqsh.md owns that; link it) and NOT the language reference (bikar's docs/language-reference.md; link it).
---

# maintain-cookbook — one idea, one picture, one warning

The cookbook is the wiki's show-me page for naqsh: someone reads a recipe, sees what one
knob does, and copies the snippet. It is author work: plain words, interlinked, like a
notebook. Read [`recipe-rules.md`](recipe-rules.md) every run; it is the rubric and it
sharpens as recipes come back wrong.

Work in a worktree on a branch off `origin/master`. Pictures render against a built bikar:
`BIKAR_DIR=<bikar checkout>` (defaults to `~/Workspace/git/bikar-main`).

## How one run goes

1. **Pick.** The keyword or mechanism to show. If `make cookbook` named one, that one. If
   several are waiting on the not-yet list in `docs/cookbook/README.md`, take the one a
   reader is most likely to reach for first. Find the page it belongs on (the README lists
   them); a new page only when no family fits.
2. **Smallest snippet.** The fewest lines that show the mechanism working. Borrow from a real
   pattern in `src/` or bikar's `examples/` and cut it down; don't invent geometry when a
   catalog pattern already does it. Check the syntax in bikar's `docs/language-reference.md`.
3. **Vary one thing.** Choose the one piece of text that changes, and two or three values
   that make the change obvious. Write the marker above the fence:
   - `<!-- recipe: NAME; swap: a | b | c -->`: each value replaces whichever one is written
     in the fence;
   - `param: NAME = 1 | 2 | 3` for a `param`;
   - `mate: MM` draws two copies pushed together (a joining coaster);
   - no `swap` gives a single picture. Use it only when there is nothing sensible to vary.
4. **Render.** `python3 tools/cookbook_render.py --recipe NAME`. A snippet bikar refuses
   fails the run with bikar's message: fix the snippet, don't skip it.
5. **Look.** Open the recipe's picture in `docs/cookbook/img/` and read it. Does each tile differ in exactly
   the way the text will say? If the change is too small to see, pick bigger values or a
   different knob. If the picture contradicts what you expected, the picture wins: rewrite
   the text (and say so in the report if it also contradicts bikar's reference).
6. **Write.** Heading, one `covers:` comment per harvested keyword the recipe shows (hidden
   HTML comment, e.g. `<!--covers:rosette-->`), a plain explanation, the marker and fence,
   the picture with alt text naming the values, `**Watch out:**`, `Related:`.
7. **Link.** Related recipes on this and other pages; the reference by GitHub URL. If the
   keyword was on the not-yet list, take it off. Add the page to the README if it is new.

Then `make cookbook` (every recipe renders, no orphan pictures, every keyword accounted
for) and `make validate`. Stage the page, its pictures and the README by name.

## When a keyword is not worth a recipe yet

Put it on the not-yet list with a one-line reason a reader would accept ("a change of a
millimeter at the rim, too small to see"). The list grows only with
`COOKBOOK_NOT_YET_MAY_GROW=1`, on purpose. Leave the reason honest: "not written yet" is
fine, and it is better than an invented obstacle.

## What the coverage check can't see

The keyword list is harvested from bikar's `docs/grammar.md`. Clauses written there as prose
(the bodies of `orb`, `piece`, `tile`, `wall`, `assembly`, such as `weave` or `band`) are not
harvested. Mention them in the text if they matter, but never mark them `covers:`; the
check will reject a word it doesn't know.
