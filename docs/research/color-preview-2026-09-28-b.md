---
date: 2026-09-28
feeds:
  - '[[color-preview-design-b]]'
---

# Colour previews for coasters — raw findings (researcher B)

- **Date:** 2026-09-28
- **Produced by:** researcher B (one of two independent researchers; the other researcher's
  files were not read)
- **Feeds:** [`docs/color-preview-design-b.md`](../design/coaster/color-preview-design-b.md)
- **Question (Omar):** "Do we have the ability to alternate colors / customize colors on the
  PNGs we are generating? If not, would we need to integrate an alternate CAD software?"
  Plus the scope addition: configure orbits, colours, flush vs lowered and a live preview in
  Coaster Lab, with the Lab preview and the printed parts coming from one code path.

Evidence form: 3d-models paths are relative to this repo at `5938f31`. bikar paths are written
`bikar:<path>:L<n>` and read in the `bikar-work` checkout on branch `feat/orbit-radial-fill`
at `f8796fc` (PR NaqshCoffee/bikar#270, not yet on bikar main `ccf93a6`), so line numbers can
differ on main.

---

## 1. In-repo findings

### 1.1 Where today's PNGs come from (two paths, both one colour)

| PNG | Made by | Colour today |
|---|---|---|
| Gallery / brick / coaster previews (`src/**/*.png`) | `build/brick_previews.py` runs OpenSCAD 2021.01 on a one-line `import()` of the single `--format stl` mesh, `--colorscheme=Cornfield` (`build/brick_previews.py:L116`), then `build/process_images.py` keys out the cream background `BG = (255, 255, 229)` (`build/process_images.py:L20`) | Cornfield gold, one colour |
| Catalog / Lab thumbnails (184×184, e.g. `docs/catalog/media/GimTvN9hw4U/`) | bikar `scripts/render-coaster-thumbnails.ts` opens `coaster.html?f=<id>` in headless Playwright and copies the viewer canvas (`bikar:scripts/render-coaster-thumbnails.ts:L90`) | Lab bronze `BRONZE_FRONT = [214,178,84]` (`bikar:packages/lab/src/viewer.ts:L40`) — presets carry no colours |
| Coaster make target | `Makefile:L803` calls `brick_previews.py --coasters --mate …` | as row 1 |
| Orb gallery previews | `build/orb_previews.py` recolours view SVGs to one gold at each fill's own luminance | one hue |

The bikar CLI makes a PNG only by rasterizing an SVG with `rsvg-convert` or `magick`
(`bikar:packages/cli/src/rasterize.ts`). For a coaster, `--format views` writes only
`<name>.top.svg` (`bikar:packages/cli/src/index.ts:L1022`).

### 1.2 The colour split already exists and already feeds the printer

- `buildCoasterParts` (`bikar:packages/core/src/kernel3d/coaster.ts:L3261`) splits a coaster
  into one body per region / palette colour. `--format parts` writes one STL per body plus
  `<name>.parts.json` (region, stl, triangles, paletteName, hex, pinch)
  (`bikar:packages/cli/src/index.ts:L1035`). The default pinch is `fillet`
  (`bikar:packages/cli/src/index.ts:L698`).
- `tools/bambu` turns that manifest into a multi-part 3MF: `filament_colour` from each part's
  hex (`tools/bambu/src/ams.ts:L137`), one extruder per part.

### 1.3 Coaster Lab already shows a live coloured preview from the same split

- `bikar:packages/lab/src/evaluate.ts:L385` calls `buildCoasterParts(built, { pinch: 'fillet' })`;
  `coasterTintMesh` (`bikar:packages/lab/src/evaluate.ts:L324`) joins the bodies and tags every
  triangle with its part's colour (`triRgb`); the viewer paints it
  (`bikar:packages/lab/src/viewer.ts`, `shadeTriangles`) and the page shows it with
  `viewer.setMesh(msg.coasterTint ?? msg.mesh)` (`bikar:packages/lab/src/coaster-main.ts:L691`).
- So Lab preview and printed parts already share one function. Two caveats: the Lab hardcodes
  pinch `fillet` (equal to the CLI default, but a CLI `--pinch merge` run would differ), and the
  tint is null when no region is coloured.
- The Lab's colour knobs cover only `base`, `straps`, `border`, via a pure source rewrite
  `setCoasterColor(source, region, name|null)` (`bikar:packages/lab/src/coaster-colors.ts:L91`,
  decision D-076). There is no per-fill or per-orbit control.
- Lab conventions seen: a `touched` set plus `overrideParams()` in `coaster-main.ts`; the URL
  writer keeps the print target out of share URLs; custom source loads from
  `?f=custom&code=<lz-string of "bkr1\n"+source>` (`bikar:packages/lab/src/url-state.ts`).
- Params are numbers only: `ParamSpec` has name/value/default/min/max/step
  (`bikar:packages/core/src/dsl/ast.ts:L966`). Colours are palette names, not params, which is
  why the Lab rewrites source text for them.

### 1.4 What the split refuses

- Minimal / openwork (`outline pattern`) coasters are refused:
  `"coaster: --format parts has no regions to split on a minimal (outline pattern) coaster"`
  (`bikar:packages/core/src/kernel3d/coaster.ts:L3298`). Commit `f8796fc` on the radial branch
  makes filled faces solid at strap height as **one body with the straps**, so the radial
  variants (e.g. `patterns/Constructions/GimTvN9hw4U-radial-coaster.bkr` in bikar) print in one
  colour. The Lab shows them bronze (no tint), because `parts` is null.
- Slab-reshaping clauses (interlock / rim / trivet / openwork / edges) and deboss are refused too
  (`hasSlabReshapingClause`, same file).

### 1.5 The existing flat colour picture in `bambu slice coaster`

- `writeColourPreview` (`tools/bambu/src/commands/coaster.ts:L404`) writes
  `<plate>.preview.png` from `renderCoasterTopSVG` (`bikar:packages/core/src/render/coaster-top-renderer.ts:L213`),
  which draws from the **spec**, not from the split bodies.
- Its check `missingRegionColours` (`tools/bambu/src/color-preview.ts:L20`) only asks whether
  each manifest hex appears somewhere in the SVG — an aggregate. A body that the split shrank or
  lost (for example straps winning an overlap) would still pass, since the SVG never saw the split.
- `composeColourPreview` (`tools/bambu/src/color-preview.ts:L45`) appends the images.

### 1.6 Bambu Studio cannot make the colour picture headless

`docs/issues/coaster-3mf-filament-shape-and-export-hang.md`: `--export-3mf` hangs (and that step
is where thumbnails are drawn); `--load-settings` overrides the embedded filament colours down to
one slot; an `Application=BambuStudio-<version>` tag crashes headless. The same file says the
colour check is a GUI step. A 3MF sliced in the GUI does carry Studio pictures: the machine-card
sliced 3MF holds `Metadata/plate_1.png` and `top_1.png` at 512×512, drawn in the filament colour
(seen: green).

### 1.7 Orbits

The `orbit` fill attribute (D-081) lives in `bikar:packages/core/src/theme/orbit.ts`;
`bikar bands` lists orbits (`bikar:packages/cli/src/orbits.ts`). The radial coaster's comments
list orbits 0–7 with radii and name alternative sets: `0/2/4/6`, inner rosette (`orbit <= 1`),
outer ring (`orbit >= 6`). Lowered fills (`relief both emboss 1.2 fills 0.6`) are proposed in
`docs/multicolor-design.md` §3 and not built.

---

## 2. Experiments (scratch only, no code changed; every PNG looked at by eye)

Scratch dir: the session scratchpad (`…/scratchpad/`), not checked in.

1. **7apC5Q9QS-8-fill coaster.** `bikar build … --format parts --check` → 4 bodies (base 204300,
   Slab 106772, Ruby 14972, straps 105132 triangles), all PASS. A 4-line `preview.scad`,
   one `color("<hex>") import("<part>.stl");` per manifest part, rendered by OpenSCAD 2021.01
   with the `brick_previews.py` camera in ~0.3–0.5 s. **Seen:** dark slab, gold straps, ruby
   stars, cream background. Correct.
2. **CS-1 slab coaster with alternating orbit colours.** The GimTvN9hw4U coaster source with its
   fills replaced by `fill void where orbit == 1|3|5|7 color Ruby`, `== 0|2|4|6 color Teal`,
   `>= 8 color Slab`, `relief both emboss 1.2`, `color base Slab`, `color straps Gold`.
   Parts: base 177308, Ruby 41968, Teal 52968, straps 76816, all PASS (no Slab body came out —
   no face matched `orbit >= 8`). **Seen:** the OpenSCAD picture shows the orbits alternating
   ruby and teal, clearly.
3. **Same source in Coaster Lab.** A Playwright + Vite probe (same method as
   `render-coaster-thumbnails.ts`, loading `?f=custom&code=…`) saved the viewer canvas.
   **Seen:** identical alternating colouring; the colours section was visible (`hidden=false`).
   So alternate per-orbit colours work end to end today on slab styles — Lab, parts, printer
   manifest — with no new CAD software.
4. **Radial minimal coaster.** `--format parts` refused with the §1.4 message; the Lab shows it
   bronze.
5. **Tools installed here:** `rsvg-convert`, `magick`, OpenSCAD 2021.01, BambuStudio.app.
   Not installed: Blender, F3D.

---

## 3. External sources

| Source | Fetched? | What it says (load-bearing part) |
|---|---|---|
| [OpenSCAD manual, Transformations — `color()`](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations) | fetched | `color()` "is only used for the F5 preview as CGAL and STL (F6) do not currently support color"; hex strings need 2019.05+ |
| [OpenSCAD issue #6522](https://github.com/openscad/openscad/issues/6522) | fetched | on 2026.01.06, CLI `-o file.3mf` does not keep colour; closed "Not a bug" |
| [three.js ThreeMFLoader docs](https://threejs.org/docs/#examples/en/loaders/3MFLoader) | fetched | base materials plus partial Materials extension (colour groups, textures, PBR) |
| [BambuStudio wiki, Command-Line-Usage](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage) | fetched | documents `--export-3mf`; no thumbnail / PNG option documented |
| [F3D supported formats](https://f3d.app/docs/supported_formats) | fetched | STL and 3MF (3MF via assimp); says nothing on colour |
| [printago.io, 3MF file format](https://www.printago.io/blog/3mf-file-format) | fetched | Bambu colour lives in `project_settings.config` `filament_colour` plus `extruder` metadata and `paint_color`, not in core 3MF materials |
| Blender manual, command-line rendering | fetch failed (403) | — |
| OpenSCAD 2025 3MF colour export bugs #5848, #5849, #5994 | snippet only | colour export to 3MF buggy in dev builds |
| pycolorscad / colorscad | snippet only | split an OpenSCAD model by `color()` into per-colour files |
| TheZingo/stl-render-tool, yuki-koyama/blender-cli-rendering | snippet only | headless Blender (`-b -P`) renders of STL |
| ModelRift blog on OpenSCAD colour | snippet only | — |

Nothing here was checked beyond what the table says; snippet-only rows are leads, not evidence.
