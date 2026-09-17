<!-- Produced 2026-09-16 by Claude (WebFetch/WebSearch + local reads of the youtube, bikar and 3d-models trees, and `--help` of the installed tools); checked in verbatim. Feeds: docs/geogebra-construction-import-design.md, docs/construction-equivalence.md, docs/coaster-design.md, docs/plate-composer-design.md. -->

# GeoGebra construction import — research survey

Scope: everything the umbrella design doc needs to cite. Each section names its
source, the date it was read, and whether the fact was **fetched** (web),
**read** (a file in one of the three repos, at the commit named in §0), or
**run** (a tool invoked locally). Nothing here is a decision; decisions live in
`docs/geogebra-construction-import-design.md` and `docs/decisions-log.md`.

## 0. Trees read

| Repo | Path | Ref read |
|---|---|---|
| youtube | `~/Workspace/git/youtube` | `main`, working tree clean on 2026-09-16 |
| bikar | `~/Workspace/git/bikar-constructions` (worktree) | `origin/main` @ `5473221` |
| 3d-models | `~/Workspace/git/3d-models-constructions` (worktree) | `origin/master` @ `955192c` |

## 1. The corpus (read, youtube)

`reconstructions/` holds nine video reconstructions plus `_techniques/`:

```
_techniques  7apC5Q9QS-8  GimTvN9hw4U  lEfWSogWscs  M60LJNNslHU
n3IidKfXE1I  nmEjCTzMbDg  rDuxHF3xMOc  sDO9fpu76v8  tA8eSdVx_EQ
```

`docs/tasks/done.md` records these rungs as done, with their final score
(`ggb_score.py` output, `objects matched / total` and edge-SSIM):

| id | objects | edge-SSIM |
|---|---|---|
| `n3IidKfXE1I` | 37/37 | 0.8719 |
| `tA8eSdVx_EQ` | 30/30 | 0.8844 |
| `rDuxHF3xMOc` | 47/47 | 0.9135 |
| `M60LJNNslHU` | 9/9 | 0.9608 |
| `sDO9fpu76v8` | 77/77 | 0.8661 |

Command census, `grep -o` over every `construction.ggb-commands` and every
`_techniques/*.ggb-commands` on 2026-09-16 (counts are call sites, including
the technique snippets):

| Command | Count | Command | Count |
|---|---|---|---|
| Reflect | 152 | Segment | 7 |
| Intersect | 84 | AngleBisector | 6 |
| Rotate | 82 | CircularArc | 3 |
| Polygon | 42 | Vector | 2 |
| Line | 41 | Translate | 2 |
| PerpendicularBisector | 20 | Parabola | 2 |
| Circle | 20 | ClosestPoint | 2 |
| Sequence | 18 | Center | 2 |
| Midpoint | 13 | Hyperbola | 1 |
| PerpendicularLine | 12 | Centroid | 1 |

Free-point literals in the corpus: `A=(0,0)`, `B=(1,0)`, `D=(0,1)` in every
reconstruction; the lattice technique snippet also has `C=(0.5,0.5)` and
`uE=(2,0)`. No reconstruction places a free point off the unit frame.

`GimTvN9hw4U/construction.ggb-commands` has 26 statements and 20 `# t=` tags;
`7apC5Q9QS-8` has 144 statements.

## 2. The youtube toolchain (read + run)

### 2.1 `scripts/ggb_build.py`

`parse()` calls `die()` on any line it does not recognise, so the parser fails
closed. `expand()` runs before `parse()` and unrolls `Sequence` forms and
sliders. The command-to-type dispatch, read verbatim at L308–330:

```python
_CMD_TYPE = {
    # points
    "point": "point", "intersect": "point", "midpoint": "point", "center": "point",
    "centroid": "point", "root": "point", "vertex": "point", "closestpoint": "point",
    # lines / rays
    "line": "line", "perpendicularline": "line", "perpendicularbisector": "line",
    "anglebisector": "line", "ray": "line", "tangent": "line", "polarline": "line",
    "parallelline": "line", "asymptote": "line",
    "segment": "segment", "vector": "vector",
    # conics
    "circle": "conic", "ellipse": "conic", "hyperbola": "conic", "parabola": "conic",
    "conic": "conic", "semicircle": "conic",
    "arc": "conicpart", "circulararc": "conicpart", "sector": "conicpart",
    "circumcirculararc": "conicpart", "circumcircularsector": "conicpart",
    # polygons
    "polygon": "polygon", "regularpolygon": "polygon",
    # scalars / angles
    "angle": "angle", "distance": "numeric", "length": "numeric", "area": "numeric",
    "radius": "numeric", "slope": "numeric",
}
_POLYMORPHIC = {"rotate", "reflect", "translate", "dilate", "shear",
                "applymatrix", "mirror"}
OUTLYING_PATH_TYPES = {"segment", "conicpart", "polygon"}
```

`_CMD_TYPE` has 40 keys; `_POLYMORPHIC` has 7. Every command in the §1 census
is in one of the two sets. The emitter writes `geogebra.xml` with a `<command>`
block per dependent object and `<coords>` only for free points (emitter
≈ L1106–1163).

### 2.2 `scripts/ggb_score.py`

- L40 (docstring): `Verdict: pass = edge-SSIM >= --ssim-min`.
- L256: `ap.add_argument("--ssim-min", type=float, default=0.70, ...)`.
- `--dilate` default 2; Canny thresholds 50/150; `--align` and `--mask-ref` are
  the options the reconstruct loop uses.
- `scripts/yt_reconstruct.py` L58 passes `--ssim-min` through with the same
  default, 0.70. **The loop's accept threshold is therefore 0.70 edge-SSIM**;
  the five done rungs above all cleared it by ≥ 0.16.

### 2.3 `docs/design/youtube-reconstruct.md` L130–172

Build options section. The load-bearing sentence: GeoGebra recomputes all
dependent geometry from `<command>` blocks on load, so dependents need no baked
coordinates and no `<element>` type. The supporting issue note is
`docs/issues/ggb-xml-command-blocks-recompute.md`. The section also names the
GgbAPI (Apps API) as the fallback route for coordinates.

### 2.4 Environment (run, `conda run -n youtube`)

| module | present |
|---|---|
| `PIL` | yes |
| `skimage` | yes |
| `cv2` | yes |
| `pydantic` | **no** |
| `playwright` | **no** |
| `jsonschema` | **no** |
| `lark` | **no** |

Dependencies are the `PIP_PKGS` variable in `youtube/Makefile` (≈ L39); the
`env` target installs them and `deps-check` verifies pillow, imagehash,
scikit-image and opencv. Bare `python`/`pip` are blocked by a hook in that repo;
use the `scripts/` wrappers, make targets or `conda run -n youtube`.

## 3. GeoGebra file format (fetched 2026-09-16)

Source: <https://geogebra.github.io/docs/reference/en/File_Format/> and
<https://geogebra.github.io/docs/reference/en/Common_XML_tags_and_types/>.
(`wiki.geogebra.org` did not resolve, ENOTFOUND; the GitHub-hosted reference is
the same content.)

- A `.ggb` is a zip archive containing `geogebra.xml` (the construction),
  `geogebra_thumbnail.png`, `geogebra.js` (scripts) and an `images/` folder.
- `geogebra.xml` is `<geogebra>` → `<construction>` containing, per object,
  either an `<element type="…" label="…">` block (free objects, with
  `<coords x y z>`, `<show object label>`, style tags) or a
  `<command name="…"><input a0 a1 …/><output a0 a1 …/></command>` block for a
  dependent object, **followed by** an `<element>` block per output carrying
  the cached state and style.
- Free numbers and formulas are `<expression label="…" exp="…"/>`.
- Visibility is `<show object="true|false" label="true|false"/>` inside the
  element.
- Multi-output commands (`Intersect` of two circles, `AngleBisector` of two
  lines) list every output in `<output a0="E" a1="F"/>`.

Consequence recorded for the design doc: a file written by GeoGebra itself has
the same `<command>` blocks as one written by `ggb_build.py`, plus cached
`<coords>` for the dependents. A front end that reads `<command>` blocks reads
both.

## 4. GeoGebra command-line export (fetched 2026-09-16)

Source: <https://geogebra.github.io/docs/reference/en/Command_Line_Arguments/>.

Arguments recorded from the page:

- `--export=<File>` exports the loaded construction to the named file; the
  format is taken from the extension: SVG, PNG, PDF, EMF, EPS.
- `--dpi=<n>` for raster export.
- `--exportAnimation=<File>`.
- `--showAxes=<bool>`, `--showGrid=<bool>`.
- `--settingsFile=<File>`.

Local (run): `/Applications/GeoGebra.app/Contents/MacOS/GeoGebra` and
`/Applications/GeoGebra Geometry.app` are installed; the youtube loop already
drives the desktop `--export` to render `export.png`.

## 5. GeoGebra Apps API and the headless route (fetched 2026-09-16)

Source: <https://geogebra.github.io/docs/reference/en/GeoGebra_Apps_API/>.

Methods relevant to an oracle, as listed on the page:

- `setBase64(base64, callback)` loads a `.ggb` from its base64 encoding;
  `getBase64()` returns the current file.
- `getAllObjectNames([type])`, `getObjectType(name)`.
- `getXcoord(name)`, `getYcoord(name)`, `getZcoord(name)`, `getValue(name)`.
- `getVisible(name)`, `getLayer(name)`, `getColor(name)`.
- `getCommandString(name[, localized])` returns the defining command;
  `getValueString(name)` the value as text; `getDefinitionString(name)`.
- `evalCommand(str)` executes a command line.
- `exportSVG(callback)`, `exportPDF(scale, filename, sliderLabel)`,
  `getPNGBase64(exportScale, transparent, dpi)`.

**STL:** the API page lists no STL method. The manual's export page
(<https://geogebra.github.io/docs/manual/en/Export_Menu/>) describes STL only as
the GUI action "Download as → 3D print (.stl)" from the 3D Graphics view, which
exports visible objects. Whether STL can be produced headlessly is therefore
**unverified** on 2026-09-16; no design here depends on it.

geogebra-mcp (<https://github.com/TioSavich/geogebra-mcp>, README fetched):
drives the official Apps API in headless Chromium through Playwright, pins a
GeoGebra web-app version, and exposes an environment override
`GEOGEBRA_CODEBASE` to point at a local copy. This is the precedent for
`ggb_coords.py`: Playwright + the web app, offline once cached.

GeoGebra source: <https://github.com/geogebra/geogebra> (GPL/CC; the XML
reader is in `common/src/main/java/org/geogebra/common/io/`).

## 6. ExportImage command (fetched 2026-09-16)

Source: <https://geogebra.github.io/docs/manual/en/commands/ExportImage/>.
`ExportImage[…]` takes key/value pairs such as `"type"`, `"scale"`, `"dpi"`,
`"transparent"`, `"filename"`, `"view"`, `"clipboard"`, and runs inside the app
(so it is also reachable via `evalCommand`). It produces PNG/SVG/PDF; no STL.

## 7. OpenSCAD SVG import (fetched) and the local binary (run)

Source: <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/SVG_Import>.

- `import("file.svg")` reads only **closed** paths as polygons; an open path
  is imported as a shape of its stroke width, not as a line.
- Fill and stroke attributes are ignored on closed shapes.
- Text, clipping paths and gradients are not supported; text must be
  converted to paths first.
- Units are px at 96 dpi unless the SVG carries a `viewBox` with physical
  units.

Local: OpenSCAD 2021.01 is installed at
`/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD`. The zsh alias
`openscad` points at the missing `/Applications/OpenSCAD.app/...` and fails;
call the binary by its full path. `polygon(points)` + `linear_extrude` +
`-o file.stl` are the only features the O3 reference extruder needs.

## 8. Bambu Studio command line (fetched + run)

Source: <https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage>, and
`/Applications/BambuStudio.app/Contents/MacOS/BambuStudio --help` (version
02.08.02.61, run 2026-09-16). Options recorded from the help text:

- Inputs: one or more `.3mf` / `.stl` files as positional arguments.
- `--arrange 0|1|auto` — arrange objects on the bed; `--orient` — auto-orient.
- `--assemble` — assemble all inputs into one object.
- `--scale <f>`, `--rotate <deg>`, `--rotate-x`, `--rotate-y`.
- `--repetitions <n>`, `--clone-objects <n>`.
- `--ensure-on-bed`.
- `--export-3mf <file>`, `--export-stl <file>`, `--export-stls <dir>`.
- `--export-png <file>` (thumbnail), `--export-slicedata <dir>`.
- `--slice 0|<i>` — slice all plates or plate *i*.
- `--load-settings "machine.json;process.json"`, `--load-filaments "f.json"`.
- `--outputdir <dir>`, `--debug 0-5`, `--min-save`, `--info`, `--no-check`.
- Priority when the same key is set twice: CLI > loaded settings > 3mf.

`3d-models/tools/bambu/src/commands/slice.ts` L22–44 and L132–149 wrap a single
model today (`bambu slice plate`), with `--load-settings` and `--export-3mf`.

## 9. X2D bed (fetched 2026-09-16, secondary source)

<https://bambulab.com/en/x2d/specs> returned HTTP 403 to the fetcher. Values
below come from a retailer spec page (goodprints3d, X2D product article) and
search-result snippets, and are marked **secondary**:

| mode | build volume (W × D × H) |
|---|---|
| single nozzle | 256 × 256 × 260 mm |
| dual nozzle | 235.5 × 256 × 256 mm |

Also from the same secondary sources: nozzle up to 300 °C, chamber up to 65 °C.
The only value any design here uses is the 256 × 256 mm footprint, which
`docs/prints/` in this repo already records from the confirmed X2D slice
profile (commit `ed41d33`, "record the confirmed X2D slice profile").

## 10. Parser toolkits surveyed (fetched 2026-09-16)

| Toolkit | Lang | Kind | Notes from its docs |
|---|---|---|---|
| Lark <https://lark-parser.readthedocs.io/> | Python | EBNF grammar → Earley / LALR(1) / CYK parsers; builds a parse tree automatically | Not in the youtube env (§2.4). A grammar file beside the existing parser is a second source of truth unless it replaces the parser. |
| Ohm <https://ohmjs.org/> | JS/TS | PEG; grammar text separate from semantic actions; editor tooling | Would replace bikar's hand-rolled parser wholesale. |
| Chevrotain <https://chevrotain.io/> | JS/TS | Parser-combinator style internal DSL, no code generation, generates syntax diagrams | The grammar *is* the code, so no separate EBNF to gate against. |
| Peggy <https://peggyjs.org/> | JS | PEG generator → a `parse()` function | Same second-source problem as Lark. |

bikar's own grammar decision (`docs/decisions/2026-07-29-dsl-grammar-spec-and-gates.md`,
read) chose a hand-written normative EBNF in `docs/grammar.md` held to the
parser by three gates rather than a generator: G1 sweeps the pattern corpus, G2
snapshots the reserved words, G3 parses every ```bkr fence in the docs and
requires every ```bkr invalid fence to fail. That is the shape this survey
recommends copying for `.ggb-commands`.

## 11. bikar facts (read)

- `docs/grammar.md` is titled `# BIKAR DSL Grammar`; `docs/language-reference.md`
  is `# BIKAR DSL Language Reference`. bikar has no root `README.md`.
- `packages/core/tests/fixtures/keywords.snapshot.txt` has **130** lines (G2).
- `patterns/` top level: `Assemblies`, `Coupons`, `Flower of Life`, `Lego`,
  `Orbs`, `Petal Tutorial`, `Pieces`, `Rosettes`, `Showcase`, `Spirals`,
  `Stars`, `Tiled Patterns`, `Walls`, `Weave`, plus loose `.bkr` files and
  `index.json`. `tests/canonical/corpus-sweep.test.ts` and
  `starter-compile.test.ts` compile the files under `patterns/` (92 at the ref
  read).
- No AST-to-text printer exists; `packages/knobs` rewrites source text.
- `packages/web/src/main.ts` keeps a private `KEYWORDS` set (≈ L984) separate
  from `packages/core/src/dsl/tokens.ts`.
- Decision docs follow `docs/decision-schema.md`: frontmatter with `status`,
  `discovered`, `decided`, `owner`, `status_token`, `picked_option`, `tag`
  (member of `docs/decisions/tags.yaml`), `supersedes`, `superseded_by`,
  `related`; body starts `## 0. Premise check (MANDATORY)`. `make ledger`
  regenerates `docs/decisions/README.md` and `LEDGER.md`; `make local.coherence`
  and `make local.ledger-check` gate it. Latest doc at the ref read:
  `2026-09-02-tainted-innerhtml-gate.md`.
- The `bikar-dsl` skill description: "Authoring guardrails for .bkr scripts —
  param declarations …, and the edit-time validation loop (compile + mesh
  gate). Use when writing or editing any .bkr file, especially param headers
  and orb scripts."

## 12. 3d-models facts (read)

- `docs/decisions-log.md` ends at **D-052** on `origin/master`. Open PRs #182 and #183
  (`gh pr list --repo omars-lab/3d-models`, 2026-09-16) claim **D-053** and **D-054**,
  so the next free id is **D-056**; re-check the open-PR list before merging
  (`decision-id-collision`: first merged owns the id, the open PR renumbers).
- `.claude/gates/docs_gate.py` rules D1–D5; `docs/research/` is exempt from D4
  (the `"research" in path.parts` test at L345).
- 38 files in `docs/research/`; the provenance-header convention is the first
  line of this file.
- `Makefile` targets are appended at the end (use-case map convention).

## 13. Numbers this survey licenses

A design doc may cite these with `**Default:**` … `[survey §N]`; anything not
in this table needs a `CAL-*` bet.

| Number | Value | Source |
|---|---|---|
| edge-SSIM accept threshold | 0.70 | §2.2, `ggb_score.py:256` |
| edge-SSIM dilation | 2 px | §2.2 |
| X2D single-nozzle footprint | 256 × 256 mm | §9 (secondary) + `docs/prints/` |
| reserved words in naqsh | 130 | §11 |
| `_CMD_TYPE` keys / `_POLYMORPHIC` | 40 / 7 | §2.1 |
| reconstructions in corpus | 9 (+ `_techniques`) | §1 |
| latest decision id / next free | D-052 / D-056 | §12 |

## 14. Unverified and open

- Headless STL export from GeoGebra (§5).
- The X2D spec page itself (§9); the footprint is confirmed by this repo's own
  slice profile, the other figures are not used.
- Whether the GeoGebra web app can be fully cached for offline Playwright use;
  geogebra-mcp's `GEOGEBRA_CODEBASE` suggests yes, not yet run here.

## 15. Links

- GeoGebra XML: <https://geogebra.github.io/docs/reference/en/File_Format/>,
  <https://geogebra.github.io/docs/reference/en/Common_XML_tags_and_types/>
- GeoGebra CLI: <https://geogebra.github.io/docs/reference/en/Command_Line_Arguments/>
- GeoGebra Apps API: <https://geogebra.github.io/docs/reference/en/GeoGebra_Apps_API/>
- ExportImage: <https://geogebra.github.io/docs/manual/en/commands/ExportImage/>
- geogebra-mcp: <https://github.com/TioSavich/geogebra-mcp>
- GeoGebra source: <https://github.com/geogebra/geogebra>
- OpenSCAD SVG import: <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/SVG_Import>
- Bambu Studio CLI: <https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage>
- X2D specs (403 on fetch): <https://bambulab.com/en/x2d/specs>
- Lark: <https://lark-parser.readthedocs.io/> · Ohm: <https://ohmjs.org/> ·
  Chevrotain: <https://chevrotain.io/> · Peggy: <https://peggyjs.org/>
