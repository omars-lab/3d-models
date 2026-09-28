# Coloured previews and the Coaster Lab colour controls — design (researcher A)

Omar, 2026-09-28: "Do we have the ability to alternate colors / customize colors on the PNGs we
are generating? If not, would we need to integrate an alternate CAD software?" — and then: "we
should have options to configure all of these in a robust easy to use fashion in coaster lab".

*Status: researcher A's design, one of two independent passes; a checker will consolidate. Nothing
here is built. It builds on [multicolor-design.md](multicolor-design.md) (how shapes are grouped
into colours, flush vs lowered, how colours reach the printer) and does not redo it. Raw findings,
file:line evidence and sources: [research/colour-preview-2026-09-28-a.md](research/colour-preview-2026-09-28-a.md).*

## 0. The answer in one screen

| Question | Answer |
|---|---|
| Can we colour the PNGs today? | **Partly.** The Coaster Lab already paints each printed body in its palette colour, and its picker thumbnails are screenshots of that. The **gallery** PNGs (the yellow three-quarter pictures) are one colour, because they are drawn from the single STL by OpenSCAD's default gold scheme |
| Why is the CS-1 radial variant yellow? | Not the renderer: that coaster is openwork, and its filled orbits are **one body with the straps**. `--format parts` refuses it, so the printer would get one colour too. Colouring it needs a kernel change first (§3) |
| Do we need other CAD software? | **No.** Both routes tried in a scratch run coloured the real printed bodies correctly with tools already installed: OpenSCAD 2021.01 `color()` over the part STLs, and a 60-line painter renderer using the Lab's own shading rule plus `rsvg-convert` (research §3) |
| Recommendation | Make one bikar function turn the parts `--format parts` writes into a coloured picture. The Lab viewer uses it live; a new `bikar render --format preview` uses it for the gallery PNG. One code path, from the same bodies the printer gets (§4) |
| Lab controls | An **Orbits** panel: one row per orbit with a fill tick and a colour from the palette, rule-based presets (none / inner / outer / alternate / all), a fill-height slider once the `fills` clause exists. Every control rewrites `.bkr` lines, like today's colour knob (§5) |

## 1. What exists today

Ten PNG paths were found (research §1). Only three matter for coasters:

1. **Gallery picture** — `build/brick_previews.py` imports the single STL into OpenSCAD with the
   Cornfield scheme and a fixed three-quarter camera; `build/process_images.py` then turns every
   cream pixel transparent. One colour. It draws the printed mesh, but the *combined* mesh, not the
   parts.
2. **Coaster Lab viewer and its thumbnails** — splits the coaster with `buildCoasterParts` using
   the export's own pinch default and paints each body by its palette colour
   ([D-076](decisions-log.md)). This is already a coloured preview from the printed bodies, but it
   lives only in a browser canvas; the PNGs of it are Playwright screenshots.
3. **Colour plate picture** from `bambu slice coaster` (#342) — a top-down 2D drawing made from the
   coaster's description, not from the split bodies. Its check only asks that each palette colour
   appears *somewhere* in the drawing.

So the colour data and a renderer that honours it both exist. What is missing is a PNG, outside a
browser, drawn from the parts — and the controls to choose the fills without typing `.bkr` lines.

## 2. The options

"Verifies" means: does the picture come from the same bodies, in the same colours, that the
printer gets?

| Option | What it verifies | Pros | Cons | Implications |
|---|---|---|---|---|
| **A. OpenSCAD `color()` over the part STLs** (gallery script reads the parts sidecar) | Same bodies (reads the STLs `--format parts` wrote) and the sidecar's hex per body | Tried: correct colours in 0.35 s on the installed 2021.01; about 30 lines in `build/brick_previews.py`; keeps the gallery camera | A **second renderer** beside the Lab's, so Lab and gallery can disagree on look; colour shows only in OpenSCAD's preview mode (fetched manual); the cream colour key in `process_images.py` would punch holes in a cream or white filament | Cheapest; ties the gallery to OpenSCAD for good; nothing reaches the Lab |
| **B. bikar's own renderer, shared by Lab and CLI** (recommended) | Same bodies **by construction**: one function takes the map `buildCoasterParts` returns plus the colour map the sidecar is written from | One code path for Lab, CLI and gallery; no new tool (`rsvg-convert` is already what bikar's `rasterize.ts` uses); tried in scratch: 1024 px in about 2 s; transparent background removes the cream-key problem | A bikar change (move the Lab viewer's projection, shading and body-colour code into core, add `--format preview`); depth sort by triangle centre is approximate — fine on a flat coaster, untested on tall walls | Gallery coasters move off OpenSCAD; the Lab viewer and the gallery then cannot drift |
| C. Render the parts **3MF** with a 3MF viewer (3MF Consortium viewer, or F3D) | The actual file the slicer opens, including the palette-to-slot bake | Checks one link further down the chain than A or B | New dependency plus a headless browser; per-object colour support is **snippet-only** for the 3MF viewer, and the fetched F3D options page does not mention 3MF | A second renderer again; worth it only if the 3MF bake itself goes wrong, which the slicer check (D-077) already watches |
| D. **Blender** headless | Whatever it is fed (the part STLs) | Photo-real material, lighting, shadows | Not installed; a large dependency for a flat coaster; its manual returned 403, so nothing about it is grounded here | A third toolchain to keep working; a product-photo job, not a preview job |
| E. Bambu Studio thumbnails | The sliced plate | The printer's own view | Headless 3MF export hangs ([coaster-3mf issue](issues/coaster-3mf-filament-shape-and-export-hang.md)); colour is a window check by D-077 | Not available headless today |
| F. Keep the top-down 2D drawing | Nothing about the bodies: drawn from the description | Exists | A merged pinch tip or a lost strap would still draw correctly | Fine as a plate legend; not a preview of the print |

Why B over A: A is quicker, but it creates two renderers that can disagree, which this repo treats
as the defect itself ("two code paths that disagree … are the defect", CLAUDE.md). B deletes that
by making the Lab and the gallery call one function. A stays a valid stop-gap if the gallery needs
colour before B lands; it verifies the same bodies, only not the same look.

## 3. The openwork prerequisite (why CS-1 radial is still one colour)

The radial coaster is `outline pattern`: a free-standing strap network with no slab. Its filled
orbits are closed solid at strap height as part of the strap body, and `buildCoasterParts` refuses
the whole openwork style. So neither the Lab nor any renderer can show them in a second colour,
and neither could the printer.

To colour it, the split has to learn openwork: one body for the straps, one per fill colour. That
is a kernel change, and it has a printing consequence the plain coaster does not: with no slab,
**every body stands on the bed**, so the first layer has several colours (on the plain coaster the
slab is one colour and colour starts above it, [multicolor-design.md §5](multicolor-design.md#5-printability)).
Whether that prints cleanly on the X2D is unmeasured; it may be fine, or it may need the fills to
start one layer up. This is a calibration question for a coupon, not something this doc settles.
Until then, the preview work (§4) is useful on the plain and border styles, which split today.

## 4. Recommended design: one preview function

1. **Core, one module** (for example `coaster-preview`): moved, not rewritten, from the Lab —
   `coasterTintMesh` (body → colour, today in the Lab's `evaluate.ts`) and the projection and
   head-light shading (today in the Lab's `viewer.ts`). Input: the parts map from
   `buildCoasterParts`, the body colours, a camera. Output: a list of shaded, depth-sorted polygons.
2. **Lab viewer** draws that list on its canvas, as it does now. Behaviour unchanged.
3. **CLI** `bikar render <coaster> --format preview -o <file>.png [--pinch …]`: evaluates, splits
   with the same pinch option `--format parts` takes, writes the polygon list as SVG with no
   background rectangle, and rasterises with the existing `rasterize.ts`. It refuses exactly where
   `--format parts` refuses, so a preview never promises a split the printer cannot get.
4. **Gallery**: `make coasters` calls `--format preview` for splittable coasters with colours and
   keeps `brick_previews.py` for the rest; the PNG already has a transparent background, so
   `process_images.py` has nothing to key.

The preview reuses the gallery's camera and size rather than choosing new ones: the three-quarter
view `0,0,0,60,0,25,0` (OpenSCAD's rotation-only camera form, read with `--viewall --autocenter`)
and 1024 px square, both as [`build/brick_previews.py`](../build/brick_previews.py) sets them. These
are house choices, not measured values — one shared angle, so a coloured and an uncoloured coaster
sit side by side in the gallery at the same angle.

The body colour map must be the one `--format parts` writes into the sidecar, taken from the same
function (today `pieceColour` in the CLI), so the preview and the sidecar cannot give one body two
colours.

## 5. Coaster Lab controls

Lab rules kept: a knob is a `.bkr` edit (numeric knobs are `param`s; colour, which has no param,
is a line rewrite like today's `color <region>` knob); touched knobs are tracked; a preset turns
into "custom" when edited; the print target never enters a share link. A custom coaster's source
already travels in the share link, so fills and colours travel with it with no extra work.

```
┌ Colours ───────────────────────────────────────────────┐
│ Straps [Gold ▾]   Base [Slab ▾]   Border [— ▾]          │
├ Fills (orbits about the centre) ───────────────────────┤
│ Presets: [None] [Inner] [Outer] [Alternate] [All]      │
│                                                         │
│  #  shape      count  radius   fill  colour             │
│  0  hexagon      1    0.0 mm   [x]   [Ruby  ▾]  ●       │
│  1  kite         6    9.4 mm   [ ]   [—     ▾]          │
│  2  star-6       6   18.1 mm   [x]   [Gold  ▾]  ●       │
│  …                                                      │
│ Palette: ● Slab #333333  ● Gold #d4af37  ● Ruby #9b1b30 │
│          [+ add colour]                                 │
├ Fill height ───────────────────────────────────────────┤
│ Lowered  0.4 ──────●────── 1.2 mm  Flush                │
│ (shown once the `fills` clause exists; flush until then)│
└────────────────────────────────────────────────────────┘
 Live preview: the viewer, painted by the §4 function.
 Hover a row → that orbit's faces highlight in the preview.
```

- **Orbit rows** come from `computeOrbits` in core (what `bikar bands` prints), added to the Lab's
  evaluate reply. Each ticked row is one `fill void where orbit == N color <Name>` line; unticking
  removes it. A new pure rewriter beside `coaster-colors.ts` does this, unit-tested the same way.
  Writing one explicit line per orbit keeps the `.bkr` the whole truth: no hidden Lab state.
- **Presets** are rules over the orbit list, not stored id lists, so they carry to any pattern:
  *inner* (the orbits below the median radius), *outer*, *alternate* (every other orbit by radius),
  *all*, *none*. A preset only ticks rows; the result is ordinary `fill` lines. A per-pattern named
  set ("snowflake" = the CS-1 radial's orbits 1, 3, 5, 7) is a committed preset `.bkr`, as the
  radial file already is; whether "alternate by radius" reproduces 1, 3, 5, 7 depends on how orbit
  ids are numbered, which was not checked.
- **Palette** edits the `palette` block (another line rewriter); a colour cannot be used before it
  is named, so the `.bkr` stays valid after every click.
- **Fill height** is a normal numeric knob once the `fills` clause from
  [multicolor-design.md §3](multicolor-design.md#3-the-look-flush-or-lowered-fills) exists and
  accepts a param: `param fill = 1.2 range 0.4..1.2` and `relief both emboss 1.2 fills $fill`.
  Flush is fill = strap height, so it is one slider, not a mode switch.
- **Refusals show, not hide**: on a style `--format parts` refuses (today: openwork, interlock,
  minimal), the Fills panel shows the refusal message, since a fill there cannot become its own
  body (§3).

**Default:** fill height flush (equal to the 1.2 mm strap height), the build-order default in
[multicolor-design.md §3](multicolor-design.md#3-the-look-flush-or-lowered-fills): the one version
built and passing the mesh gate, bikar [PR #261](https://github.com/NaqshCoffee/bikar/pull/261);
the 1.2 mm rise stays inside the relief bet CAL-CST-04. A build order, not a verdict on the look.

### What the `.bkr` needs to expose

| Control | Needs a grammar change? | What |
|---|---|---|
| Fill tick, per-orbit colour | No | `fill void where orbit == N color X` exists (D-081); the Lab rewrites lines |
| Palette colours | No | `palette` block exists; the Lab rewrites lines |
| Presets | No | Rules computed in the Lab over the orbit list |
| Fill height | **Yes** | The `fills <mm>` clause, taking a `$param` (multicolor-design §3, step 6 of its §10) |
| Colour on openwork | **Kernel**, not grammar | The split must accept `outline pattern` (§3) |
| Orbit list in the Lab | No grammar | The evaluate reply carries `computeOrbits` output |

## 6. Validators

**Validator:** the preview is drawn from the same bodies the export writes, checked body by body:
for each body key, the triangle count and a hash of the vertex data in the preview's input equal
those of the STL `--format parts` writes for the same source, params and pinch option.
PASS: `7apC5Q9QS-8-fill-coaster.bkr` at defaults gives four bodies whose counts match the export
row for row — base 204,300, Slab 106,772, Ruby 14,972, straps 105,132 (research §3.1) — and the
hashes match.
FAIL: a preview that splits with `pinch: 'merge'` while the export uses the default `fillet`, on a
saddled pattern: the base and straps rows differ even though the set of colours on screen is the
same. A check on the colour set alone (what the colour plate picture does today) passes this case,
which is why the check is per body.

**Validator:** each body is painted in the colour the sidecar records for it: for each body key,
the unshaded colour the preview assigns equals the sidecar's `hex` for that key.
PASS: the Ruby body is `#9b1b30`, straps `#d4af37`, base and Slab `#333333`, matching
`Coaster.parts.json`.
FAIL: a preview that colours only the three regions (the Lab's dropdown set) and leaves the colour
bodies that orbit or ring fills create in the default: the Ruby row reads bronze while the base and
straps rows match.

**Validator:** the gallery PNG has no hole inside the coaster: every pixel inside the coaster's
outline, projected at the preview camera, is fully opaque.
PASS: the recommended preview writes no background, so no colour key runs, and a cream fill stays
opaque.
FAIL: option A's PNG through `process_images.py` with a body coloured `#fffde8` (cream filament):
its lit faces fall within the 14-step key of `#FFFFE5` and turn transparent.

**Validator:** the Lab and the CLI draw the same thing: for one `.bkr` source, the polygon list the
Lab viewer receives equals the one `--format preview` rasterises (same count, same colours, same
order).
PASS: after §4 both call one core function with the same inputs.
FAIL: today's state — the Lab paints bodies on a canvas and the gallery draws the combined STL in
Cornfield gold; the lists differ in count and colour for every coloured coaster.

## 7. Next steps, smallest first

1. Core `coaster-preview` module (move from the Lab), Lab viewer switched to it; first and fourth
   validators as tests.
2. `bikar render --format preview`; second validator as a test; `make coasters` uses it for
   coloured splittable coasters.
3. Orbit list in the evaluate reply; Fills panel with ticks, colours and presets; the line
   rewriter with unit tests.
4. `fills <mm>` clause (multicolor-design §10 step 6), then the fill-height slider.
5. Openwork split (§3), after a coupon settles whether a multi-colour first layer prints on the X2D.

Stop-gap if Omar wants coloured gallery PNGs before step 2: option A in `brick_previews.py`, reading
the sidecar, with the cream key skipped for those files.

## 8. Still unverified

- Nothing here was sliced or printed; the pictures were checked by eye only (research §3).
- The painter's sort was only seen on one flat coaster; tall walls or deep openwork may show
  ordering errors.
- Per-object colour in the 3MF Consortium viewer is snippet-only; F3D's 3MF support was not found
  on the fetched page; Blender's manual returned 403.
- How orbit ids are numbered (for the *alternate* preset reproducing CS-1's 1, 3, 5, 7).
- Whether a multi-colour first layer on an openwork coaster prints cleanly on the X2D.
- The survey of PNG paths is a grep over the folders named in research §1, not every file in both
  repos.

## 9. Read against itself (K7) and transfer conditions (K10)

- §0 says "partly": the Lab colours bodies today (§1), the gallery does not; §2 and §4 build on
  exactly that. §0's CS-1 answer and §3 agree that the blocker is the split, and §5 shows the
  refusal in the panel rather than a colour it cannot print.
- The first validator's PASS numbers are the ones measured in research §3.1 on the machinery §4
  recommends reusing (`buildCoasterParts`); its FAIL uses the pinch option, not the renderer, to
  show a colour-set check is too weak.
- The fourth validator's FAIL is today's state, which is the reason for §4.
- **K10, OpenSCAD colour:** `color()` shows in the PNG because command-line PNG export uses preview
  mode (fetched manual); it transfers to any OpenSCAD version as long as the PNG stays in preview
  mode — adding `--render` would drop the colour.
- **K10, the Lab's shading on the gallery:** the Lab rule (`0.4 + 0.6·max(0, n·l)`, fixed light)
  was chosen for a live bronze viewer; it transfers to a gallery PNG because the picture is the
  same mesh under the same kind of flat-lit orthographic view. It is a look, not a colour claim:
  the colour check is the second validator on unshaded colours, not on pixels.
- **K10, the gallery camera:** `0,0,0,60,0,25,0` was set for OpenSCAD's `--viewall --autocenter`
  framing; in bikar's renderer it transfers as the two rotations (60° and 25°) with the framing
  recomputed from the mesh bounds. The scratch probe framed from the mesh bounds but used a near,
  not identical, angle (25° turn, 55° tilt), so matching OpenSCAD's view exactly is still to do.
