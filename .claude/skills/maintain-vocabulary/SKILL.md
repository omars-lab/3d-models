---
name: maintain-vocabulary
description: Keep the print vocabulary (docs/vocabulary/, the hub's Vocabulary page) growing, one term a card with a real picture, a plain definition, where it shows up on our coasters, a code snippet and the plates that used it. Use when a print or design word comes up that the page does not explain (skirt, brim, raft, supports, pin, stud, slide, dovetail, flange, lip, slope, wedge, halves, dots, carved id, gap, first layer, bed face, printed in place), when Omar asks "what is a …" or mixes two look-alikes up, when a plate brings in a new generic technique or a new param or object setting, or when hook `54-vocabulary` says a plate knob is named by no term. Not for naqsh language keywords with a one-knob picture; that is maintain-cookbook.
---

# maintain-vocabulary — the words we print with, each with a picture

Omar, 2026-11-05: "i also want a vocabulary in out hub with visual - skirt va brim vs pin va
dovetail wtc ... as we add more generic techiques we expand the vocabulary/tehcniqur oage ... make
sure we have skill for this ... tehc iqur page may even have code snippets etc". He had asked
whether a plate had "stars with skirts"; the star he meant stood on grid supports, and nothing here
said what either word meant.

- **Source:** [`docs/vocabulary/vocabulary.yaml`](../../../docs/vocabulary/vocabulary.yaml). The
  field list is at its top.
- **Vault page:** [`docs/vocabulary/README.md`](../../../docs/vocabulary/README.md), written from
  the YAML by `render`. Never edit it by hand.
- **Hub page:** `/vocabulary.html` on the hub reads `vocabulary.py json`, so it shows whatever the
  hub's checkout of this repo holds.

## Why a skill, and why beside the cookbook

Both precedent evaluations here
([DSL extension](../../../docs/design/process/dsl-extension-skill-evaluation.md),
[issue register](../../../docs/design/process/issue-register-evaluation.md)) came out "no skill, a
gate instead". This is both. The mechanical half is a gate: hook `54-vocabulary` fails when the
page is behind the YAML, a picture or plate is missing, or a plate uses a knob no term names. The
other half no gate can do: choosing the picture, writing the plain definition, and saying what we
found. Omar asked for the skill by name.

The [cookbook](../../../docs/cookbook/README.md) is one naqsh keyword a recipe, drawn three times
with one knob changed, and gated against bikar's grammar. Half these words have no keyword (skirt,
brim, raft, supports, first layer, bed face are slicer settings), so they cannot live there. Where
a term has a recipe (pins, slide, split, ids, dots), the card links to it instead of copying it.

## Adding a term

1. **Find where it was used.** Search the plate pages and recipes for the word and its knobs:
   `grep -liE '<word>' docs/design/plates/*.md`. Put the plates that asked about it in `plates`,
   not every plate that happens to pass the param.
2. **Pick a real picture.** In order: a picture a plate already has (`docs/design/plates/*-media/`),
   a cookbook picture, a slice or render made for this page, and last a drawing
   ([draw-side-view](../draw-side-view/SKILL.md)) marked `drawn: true`. Open it and look before
   naming it: the `alt` says what is in it, not what it should show.
3. **Write it plain.** `what` is for someone who has never printed. `ours` says where it sits on
   our coasters and what a plate found. Put a look-alike in `also` and link both ways in `related`.
4. **Add the knobs and a snippet.** `knobs` names the bkr params and `setting:<key>` object
   settings that switch it on. A glob like `pins_*` is fine. The snippet is the few lines from a
   plate recipe or the bkr that turn it on.
5. `render`, then `check`, then look at the hub page (below).

When the check names a knob no term covers: if it is a technique, give it a term or add it to the
nearest term's `knobs`. If it is a size or a pattern shape (the cookbook's job), list it under
`not_techniques` with a reason.

## Making a picture for the page

`pictures` remakes the pictures drawn for this page. They are the skirt, raft and tree-support
crops, from the first layer of a demo slice
([`media/bases-demo.yaml`](../../../docs/vocabulary/media/bases-demo.yaml), never sent), and the
slope side cuts, from the flange coaster rendered at slope 0 and 0.2. Notes:

- The slicer names raft lines "Support" in its G-code, so the raft shows grey like supports. The
  raft card's alt and banner say which grey it is.
- Our stock process prints no skirt. The demo turns one on through a process file
  ([`media/bases-demo-process.json`](../../../docs/vocabulary/media/bases-demo-process.json)),
  since `skirt_loops` is a whole-plate setting, not an object setting.

A new made picture goes in `media/` and gets a step in `cmd_pictures`, so it can be remade.

## Looking at it

After a change, look at the hub's page in a browser, desktop and phone width, before telling Omar.
Run the hub from its own worktree against this checkout:

```sh
PORT=4718 THREED_MODELS_DIR=<this checkout> npm start
```

Then open `http://127.0.0.1:4718/vocabulary.html`. The live hub on 4717 shows it once the change is
merged and its checkout has moved.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| [`vocabulary.py render`](scripts/vocabulary.py) | Writes `docs/vocabulary/README.md` from the YAML | After every edit to the YAML | `python3 .claude/skills/maintain-vocabulary/scripts/vocabulary.py render` |
| [`vocabulary.py check`](scripts/vocabulary.py) | Fails when the page is behind the YAML, a picture, plate, cookbook link or related id is missing, a picture is outside docs/, or a plate knob is named by no term | Before a commit; hook `54-vocabulary` and `make validate-vocabulary` run it | `python3 .claude/skills/maintain-vocabulary/scripts/vocabulary.py check` |
| [`vocabulary.py scan`](scripts/vocabulary.py) | Lists the plate knobs no term names; `--all` also shows which term names each one | Looking for techniques the page is missing | `python3 .claude/skills/maintain-vocabulary/scripts/vocabulary.py scan --all` |
| [`vocabulary.py json`](scripts/vocabulary.py) | Prints the terms for the hub, each picture as a path inside docs/ | The hub calls it; run it to see what the hub gets | `python3 .claude/skills/maintain-vocabulary/scripts/vocabulary.py json` |
| [`vocabulary.py pictures`](scripts/vocabulary.py) | Slices the demo plate and renders the star, then draws the skirt, raft, tree-support and slope pictures in `docs/vocabulary/media/` | After changing the demo plate or the slicer profile; needs the bambu tool and bikar's CLI (`BIKAR_DIR`) | `python3 .claude/skills/maintain-vocabulary/scripts/vocabulary.py pictures` |
| [`vocabulary.py --self-test`](scripts/vocabulary.py) | Checks every refusal on a fixture, the page render, and that a technique no term names is the only miss | After changing the script | `python3 .claude/skills/maintain-vocabulary/scripts/vocabulary.py --self-test` |
