# Coaster styles — the names we use

Read this whenever you name, describe or add a coaster style: a new `-<style>-coaster.bkr`
file, a gallery card, a Coaster Lab preset, a plate comment, or a reply to Omar. One
pattern (a construction such as CS-1 `GimTvN9hw4U`) can be made in several styles; the
style is the product, the pattern is the art on it.

## The styles

The **file suffix is the name of record** — the gallery, the Lab and the plates all key off it.

| Style | File | naqsh clause that makes it | What it is | Decided in |
|---|---|---|---|---|
| **plain** (no suffix) | `<id>-coaster.bkr` | `relief straps emboss 1.2` on `base 4` | the pattern's straps raised on a full slab | D-064, D-066 — [coaster design](../../../docs/coaster-design.md) |
| **interlock** | `<id>-interlock-coaster.bkr` | `interlock dovetail …` | plain, plus a self-mating dovetail tab and slot on every straight edge, so tiles plug together | D-069 — [interlock design](../../../docs/coaster-interlock-design.md) |
| **minimal** | `<id>-minimal-coaster.bkr` | `outline pattern` | the straps alone: no slab, every empty space in the pattern is a hole, top edges rounded over | D-070 — [minimal design](../../../docs/coaster-minimal-design.md) |
| **border** | `<id>-border-coaster.bkr` | `border <pattern> width <mm>` | plain, with a second pattern in a band round the edge; needs a colour plate, not compose | D-071 — [border design](../../../docs/coaster-border-design.md) |
| **twist** | `<id>-twist-coaster.bkr` | `outline pattern` + `twist <deg>` | minimal, twisted up its height; the twist is capped so the wall leans no more than 45° (CV12) | bikar's coaster twist-extrude design doc; CS-1 file from bikar #247 |
| **minimal-frame** | `<id>-minimal-frame-coaster.bkr` | `openwork frame <mm>` beside `relief straps …` | a solid frame round the edge, the straps standing inside it, every empty space cut through | bikar's coaster-openwork design doc; Omar chose the name 2026-09-25, keeping "minimal" for the family |
| **minimal-pegs** | `<id>-minimal-pegs-coaster.bkr` | `openwork frame <mm>` + `interlock dovetail …` | minimal-frame with the dovetails cut into the frame; the frame is at least slot depth + clearance + 1.6 mm, so no slot breaks into a hole | same doc; print its samples as a pair (print-coaster-samples skill) |

## Where the names show up

The card or preset title is `<Pattern> · <style>` everywhere, with the style exactly as
the file suffix spells it, and the bare pattern name for plain:

- **Coaster Lab** (bikar `packages/lab`): "Six-Fold Rosette · minimal".
- **Gallery** (`index.html` `COASTERS`): the same titles, one card per coaster file.
  `make coasters` fails when it builds a coaster the gallery has no card for
  (`build/brick_previews.py`), so a new style cannot ship without its card.
- **Plates** (`docs/plates/*.yaml`): the header lists each sample by its style name.
- **"solid"** is not an official name. The plain style has no suffix. Say "plain" or the
  bare pattern name, and use "solid" only as a description ("the slab is solid").

## The parts of a coaster

- **pattern / construction**: the line art, inscribed into the outline (`inscribe <id>`).
- **strap**: one band of the pattern's line work, `strap width <mm>`.
- **field**: the area inside the outline that the pattern fills. The **border band** is the
  ring round it.
- **outline**: the coaster's edge shape, fitted to the pattern (D-066). `outline pattern`
  means the pattern's own strap silhouette is the edge (minimal and twist).
- **base / slab**: the solid disc under the art, `base <mm>`.
- **relief**: height added (`emboss`) or carved (`deboss`) on the slab, over the straps
  (`relief straps …`) or over whole faces (`relief faces …`).
- **trivet**: cut the relief region right through. On CS-1 and CS-2 the face region covers
  the straps too, so trivet cuts everything. That is why minimal-frame uses its own cut,
  `openwork frame <mm>`, which keeps the straps and a frame and cuts only what lies between.
- **mini / standard**: size 40 and size 90 of the same file (`param size`), never two files.
