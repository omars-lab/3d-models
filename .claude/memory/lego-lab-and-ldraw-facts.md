---
name: lego-lab-and-ldraw-facts
description: Lego Lab decisions and the LDraw export/render facts by decision id — grounded colour names, stud colour in the inline block, thumbnail gates split at the GPU, visibleColours is baked not derived
metadata:
  type: project
---

Lego Lab = bikar pattern → LEGO-compatible printed parts at true 8 mm pitch, printed parts not a stock-part mosaic, both gates (anchorability hard pass/fail + grid-fit 0..1 with scale/rotation sweep), interface as a per-piece DSL option (`docs/lego-lab-design.md`). `footprint outline` is the third footprint arm (requires `inscribe`, changes the shape never the lattice; V18 refuses cusps sharper than ≈23.1°).

- **D-026** (bikar #79 `2d60b00`): `place <Piece> color <c>` takes a bare LDraw code or a grounded name — every name is the LDConfig name lower-cased, fetched 2026-08-06, no synonyms; resolution deferred to eval so a bad name fails every format.
- **D-027** (bikar #80 `0f497df`): `studs <c>` paints stud triangles inside the inline block (one inherit slot on a type-1 line); a stud is exactly a triangle with a vertex above body height H; emitter refuses `studs` on an empty stud set.
- **D-028** (bikar #82 `1113052`): thumbnail CLI renders a `.mpd` to a set of angles via Playwright **full Chromium** (headless shell has no WebGL here); counts are the HARD gate, golden pixels SOFT and valid only for the backend that baked them (K10). A render without edge lines is evidence of shape, not structure.
- **D-029** (bikar #83 `6dba045`, #84 `e8b07d5`): colour-set gate classifies pixels to the model's own palette; `visibleColours` is the VISIBLE set, deliberately ⊊ resolved (occlusion), baked by `--update-goldens`, never auto-derived. The only hook is the GPU-free catalog test (every `.mpd` has `expected.json` + `.notes.md`, every colour named). The whole split is one axis: does a GPU sit in the path?
- A multi-colour brick gives three's LDrawLoader a material ARRAY; single-material read-back reported an empty palette.

**Why:** each fixed a silent all-grey or wrong-count regression and set the gate boundary.

**How to apply:** new LDraw features keep colours grounded and the GPU out of hooks; the pin explorer that reads the anchor solver is [[rosette-explorer-findings]].
