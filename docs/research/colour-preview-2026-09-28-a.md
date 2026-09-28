# Colour previews — raw findings (researcher A)

- **Date:** 2026-09-28
- **Produced by:** researcher A (one of two independent researchers; a checker consolidates later)
- **Feeds:** [colour-preview-design-a.md](../colour-preview-design-a.md)
- **Question (Omar):** "Do we have the ability to alternate colors / customize colors on the PNGs we
  are generating? If not, would we need to integrate an alternate CAD software?" — plus, later, the
  Coaster Lab controls to drive it.
- **bikar state read:** `/Users/omareid/Workspace/git/bikar-work` on `feat/orbit-radial-fill` at
  `f8796fc` (open PR NaqshCoffee/bikar#270). Line numbers below are at that commit.

## 1. Every PNG path today, and whether it can carry per-body colour

| # | Where | How the PNG is made | Colour today | Drawn from the printed bodies? |
|---|---|---|---|---|
| 1 | 3d-models gallery, coasters/bricks/sets | `build/brick_previews.py` writes a one-line `.scad` that `import()`s the single STL, runs OpenSCAD with `--colorscheme=Cornfield` and the camera `0,0,0,60,0,25,0` (`build/brick_previews.py:99-123`, `CAMERA` at `:61`) | **One colour: Cornfield gold on cream.** This is the "yellow isometric" picture | Yes, but the *single* STL, not the parts |
| 2 | 3d-models gallery post-process | `build/process_images.py` keys every pixel within 14 of `#FFFFE5` to transparent (`:20-30`) — a whole-image colour key, not a flood fill | n/a | n/a — but a light filament colour (cream, ivory, white under the head-light) would be punched out too |
| 3 | 3d-models gallery, orbs | `make orbs` → `bikar render --format views` SVGs → `build/orb_previews.py` restyles → `rsvg-convert` (`Makefile:286-312`) | Per-face colour already: `renderOrbViewSVG` fills each face from the pattern's `faceColors`, else `#8a8a8a` (bikar `packages/core/src/render/orb-view-renderer.ts:12,306-322`) | Orbs, not coasters |
| 4 | bikar CLI `render --image` | `packages/cli/src/rasterize.ts` shells to `rsvg-convert` or `magick` and reads the PNG header back | Whatever the SVG says | 2D drawing |
| 5 | bikar CLI coaster `--format views` | `renderCoasterTopSVG` (bikar `packages/core/src/render/coaster-top-renderer.ts:213`), called at `packages/cli/src/index.ts:1018-1033`; input is the coaster **spec** plus region colours and palette (`index.ts:1000-1015`) | Region + palette colours, top-down 2D | **No** — drawn from the spec, not from `buildCoasterParts` |
| 6 | 3d-models `bambu slice coaster` colour plate picture (#342) | `tools/bambu/src/colour-preview.ts`: `bikar render --format svg` per coaster → `rsvg-convert` → `magick +append` | Region colours, top-down | No — 2D drawing. Its only check, `missingRegionColours` (`:19-27`), asks that every sidecar hex *appears somewhere* in the SVG — an aggregate, it cannot say the right region is in the right colour |
| 7 | Coaster Lab live viewer | Canvas-2D painter's-algorithm renderer, no WebGL (bikar `packages/lab/src/viewer.ts:1-7`); per-triangle `triRgb` tint, shade `0.4 + 0.6·max(0, n·l)` (`viewer.ts:54-110`, bronze `[214,178,84]` at `:40`) | **Per-body palette colour already** | **Yes** — `evaluate.ts:385` calls `buildCoasterParts(built, { pinch: 'fillet' })`, the export's own default, and `coasterTintMesh` (`evaluate.ts:324-354`) colours each body by its key; `coaster-main.ts:691` shows `coasterTint ?? mesh` |
| 8 | Coaster Lab picker thumbnails | `scripts/render-coaster-thumbnails.ts` (bikar root): Playwright opens `coaster.html?f=<id>`, waits for `data-tris`, copies the viewer canvas | Same as #7 | Yes (same as #7). **Looked:** `coaster-thumbs/eight-fold-rosette-fill.png` shows gold straps, dark slab, ruby stars; `six-fold-rosette-radial.png` is all bronze |
| 9 | 3d-models `tools/print_review.py sheet` | Top-down silhouette of each STL for the look-before-you-print review | Black/white mask | Single STL |
| 10 | 3d-models `%.png: %.scad` (`Makefile:251-253`) | OpenSCAD on the cookie-cutter `.scad` sources | Cornfield | n/a (cookie cutters) |

Other PNGs found by grep (e2e screenshots, LDraw thumbnails via `render-ldraw-thumbnails.ts`, the
qiyas pixel-diff path) are test or Lego surfaces, not coaster previews; not examined further. This
is a grep over bikar `packages/*` and 3d-models `tools/`, `build/`, `Makefile`, `.claude/skills`
for `png|rasteriz|openscad|playwright`; paths outside those were not searched.

## 2. Why the CS-1 radial variant is one colour — it is the geometry, not the renderer

- `GimTvN9hw4U-radial-coaster.bkr` is `outline pattern` (openwork/minimal); its palette has one
  name, `Gold`, and the fills are `fill void where orbit == 1|3|5|7 color Gold` (bikar
  `patterns/Constructions/GimTvN9hw4U-radial-coaster.bkr:111-133`). Its own comment: "A filled face
  is closed solid at strap height, **one body with the straps**" (`:110`).
- Ran: `bikar render GimTvN9hw4U-radial-coaster.bkr --coaster Coaster --format parts -o …` →
  exit 1, `Error: coaster: --format parts has no regions to split on a minimal (outline pattern)
  coaster — it is already one strap network. Render it with --format stl.` The refusal is
  `assertSplittable` (bikar `packages/core/src/kernel3d/coaster.ts:3244-3246,3298`).
- So no renderer can show the radial fill in a second colour today: the printer would get one body.
  The Lab thumbnail agrees (all bronze). Colouring an openwork coaster first needs the split to
  make each filled orbit its own body — `multicolor-design.md` §3 lists this as B's option D,
  "needs the openwork split refusal lifted".

## 3. Experiments (scratch only, nothing committed to bikar)

All outputs in the session scratchpad; commands run with Node 22.22.3 and the built bikar CLI.

**3.1 Parts of a splittable coaster.** `bikar render 7apC5Q9QS-8-fill-coaster.bkr --coaster
Coaster --format parts --check -o fill/` → four bodies, every mesh gate PASS: `base` (Slab
#333333, 204,300 tris), `Slab` (#333333, 106,772), `Ruby` (#9b1b30, 14,972), `straps` (Gold
#d4af37, 105,132). The sidecar `Coaster.parts.json` carries `region`, `stl`, `paletteName`, `hex`
per body.

**3.2 OpenSCAD `color()` over the part STLs.** A four-line `.scad`, `color("<hex>")
import("<body>.stl");` per body (hex copied from the sidecar), run with the gallery's own flags
(`--imgsize=1024,1024 --camera=0,0,0,60,0,25,0 --viewall --autocenter --colorscheme=Cornfield`) on
the installed **OpenSCAD 2021.01**. Rendered in 0.35 s ("Normalized CSG tree has 4 elements").
**Looked at the PNG:** dark slab, gold straps, ruby stars in the right places; cream background.
Works because PNG export uses preview (OpenCSG) mode, where `color()` is honoured.

**3.3 bikar-style painter renderer over the part STLs.** A 60-line scratch Node script: read the
sidecar, read each binary STL, colour every triangle by its body's hex, rotate to a three-quarter
view, drop back faces, sort by depth, shade with the Lab viewer's own rule
(`0.4 + 0.6·max(0, n·l)`, light `(-0.35, 0.55, 0.76)` normalised), write an SVG of filled
triangles; then `rsvg-convert -w 1024`. 214,711 front triangles; SVG in 0.45 s, PNG in 1.6 s.
**Looked at the PNG:** same colours in the same places as 3.2; white background, no hairline gaps
visible at 1024 px (each path stroked 0.05 mm in its own colour to close seams). No new dependency:
`rsvg-convert` is the rasteriser bikar's `rasterize.ts` already probes. Painter's sort by centroid
depth is approximate; no ordering glitch was visible on this flat coaster, and none was tested on
tall walls.

## 4. External sources

| Source | Fetched? | What it says (load-bearing part) |
|---|---|---|
| [OpenSCAD manual — command line](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_OpenSCAD_in_a_command_line_environment) | **Fetched** | "By default, cmdline .png output uses Preview mode (f5) with OpenCSG. For some situations it may be desirable to output the full render, with CGAL." Lists `--camera`, `--viewall`, `--autocenter`, `--colorscheme` |
| [OpenSCAD manual — Transformations (`color`)](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations) | **Fetched** | color "is only used for the F5 preview as CGAL and STL (F6) do not currently support color" |
| [openscad/openscad#5849](https://github.com/openscad/openscad/issues/5849) | **Fetched** | 3MF colour export on 2025.04.21 comes out all grey in OrcaSlicer/CrealityPrint; closed as not planned |
| [openscad/openscad#5848](https://github.com/openscad/openscad/issues/5848), [#5994](https://github.com/openscad/openscad/issues/5994), [pycolorscad](https://github.com/thatdecade/pycolorscad) | Snippet only | Same colour-3MF-export trouble in nightlies; a third-party tool to work around it |
| [F3D options](https://f3d.app/docs/user/OPTIONS) | **Fetched** | `--output` "render directly into a png file"; `--no-background` for transparent PNG; `--camera-direction`, azimuth/elevation; `--multi-file-mode`. The fetched page did **not** mention 3MF or per-file colour |
| [3MFConsortium/3mfViewer](https://github.com/3MFConsortium/3mfViewer) | Snippet only | three.js + lib3mf WebAssembly viewer; per-object base colours; "capture PNG images" through a promise API |
| [Blender manual — command-line render](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html) | **Tried, HTTP 403** | Nothing taken from it; Blender headless rendering (`-b`, `-P`) is common knowledge, not grounded here |
| [three.js docs — SVGRenderer](https://threejs.org/docs/#api/en/renderers/SVGRenderer) | Fetched, but the page body did not come through (index only) | Nothing taken from it |

Not installed on this machine (checked `which` and `/Applications`): Blender, F3D, MeshLab.
Installed: OpenSCAD 2021.01, BambuStudio, `rsvg-convert`, `magick`.

## 5. What the Coaster Lab already does, and what it lacks for Omar's scope addition

- Knobs are numeric `param`s (`packages/knobs`); a colour has no `param`, so the colour knob edits
  `color <region> <name>` lines with a pure source rewriter (bikar
  `packages/lab/src/coaster-colors.ts:1-11`), and the edit flips a preset to custom
  (`coaster-main.ts:277-282`). Touched knobs are a `Set` (`coaster-main.ts:141`); the print target
  is kept in `localStorage` and "deliberately absent from the URL" (`coaster-main.ts:79,210`).
- The colour dropdowns cover the three regions only (`evaluate.ts:302-314`: `base`, `straps`,
  `border`). There is no control for **which orbits are filled** or **each orbit's colour**; those
  exist only as `fill void where orbit == N color X` lines a person types.
- `computeOrbits` is exported from core (`packages/core/src/theme/orbit.ts:379`) and `bikar bands`
  lists orbit id, members, sides, area, radius and colour (`packages/cli/src/orbits.ts:11-18`), so
  the data a per-orbit control needs exists in core; the Lab's evaluate reply does not carry it.
- Flush vs lowered: `multicolor-design.md` §3 proposes `relief both emboss 1.2 fills 0.6`; not
  built (parser refuses a second relief clause, kernel has one relief height).
