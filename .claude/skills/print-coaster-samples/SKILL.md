---
name: print-coaster-samples
description: Build a plate of coaster samples (minis) to print — one mini of each coaster style for one or more patterns, with TWO of every style that mates (interlock, minimal-pegs) so the pair can be pushed together to test the fit. Use for "print a mini of each style", "make a samples plate", "minis plate for the new styles", "test the pegs fit", "add <style> to the minis". Writes or updates a `minis-NN.yaml` in `docs/plates/`, checks every item, dry-runs the compose, and stops at the owner gate. NOT general print planning (print-model) and NOT the send itself (bambu `print send` is Omar's).
---

# print-coaster-samples — a plate of coaster minis that tests what it should

A samples plate is how a new coaster style gets judged in the hand before anyone prints it at
full size. It only earns its filament if each sample can actually answer its question — a pegs
coaster printed alone cannot say whether the pegs fit. The rules for what goes on the plate live
in [`sample-rules.md`](sample-rules.md); read that file every run, it sharpens as prints come back.

Style names come from
[`coaster-styles.md`](../import-construction/coaster-styles.md) — use them exactly in plate
comments and replies.

## How one run goes

1. **Pick the patterns and styles.** The user names them, or default to every style that has a
   `-<style>-coaster.bkr` file in bikar for each pattern asked about
   (`ls ../bikar-main/patterns/Constructions/<id>-*coaster.bkr`, read at origin/main).
2. **Apply the rules** in [`sample-rules.md`](sample-rules.md): how many copies of each, which
   mini params, which styles go on a separate plate and why.
3. **Check each item before it goes on the plate** — the mesh gate at the exact params the plate
   will use:
   `node packages/cli/dist/index.js render patterns/Constructions/<file> --format stl --check --param size=40 [--param …] -o <scratch>.stl`
   run from the bikar checkout. A FAIL means change the params or leave that sample off, with the
   reason in the plate header.
4. **Write the plate** as a `minis-NN.yaml` in `docs/plates/` (next free number; update the latest
   unprinted one instead if the user is adding to it). The header says what the plate is for,
   one line per style using the style names, and what was left off and why — the minis-02 header
   is the model.
5. **Dry-run it**: `bambu slice compose docs/plates/minis-NN.yaml --dry-run`. It must place every
   item on the bed; if not, split into two plates rather than dropping a sample silently.
6. **Stop at the owner gate.** Hand over the plate file and the dry-run result. Slicing and the
   plan are the [print-model](../print-model/SKILL.md) skill's job; the physical send is Omar's
   (`bambu print send`, never with `--yes`). Filament choice is Omar's too.
7. **Ship the plate file** branch → PR → merge like any other doc, and add the print as waiting on
   Omar in the coaster-pipeline backlog (`docs/tasks/coaster-pipeline/backlog.md`).

## When prints come back

What the samples show goes into `sample-rules.md` as a new or corrected rule, with the date and
the plate it came from — e.g. a clearance that was too tight on the pegs pair, or a strap that
broke at 40 mm. That is how the next samples plate gets better without this file changing.
