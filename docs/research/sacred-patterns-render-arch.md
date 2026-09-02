<!--
provenance:
  date: 2026-09-02
  produced-by: Explore subagent (read-only architecture read), driven by Claude Code (Opus 4.8)
  method: source read of sacred-patterns@0d3ad1e (src/ts, canvas.ts, index.ts, polygons.ts,
    star.ts, circles.ts, theme.ts; package.json, webpack.config.js, Makefile, gate-parity.yaml,
    test/regression/*, CLAUDE.md), cross-referenced against bikar@5b9fb27's viz layer
    (packages/core/src/viz/face-constructs.ts, packages/web/src/viz-d3.ts) as the target shape.
  feeds: docs/vocabulary-convergence-design.md §5 (the C structural refactor), plan.md §2 row 2.4
  note: angle brackets un-escaped from the transcript's HTML entities (&lt;->< etc.); otherwise
    preserved. This grounds the current-state claims in the design doc's sacred-patterns section.
-->

# sacred-patterns rendering architecture (for the Q-VOCAB refactor)

## 1. Render entry path (one traced drawing — drawStarGrid, src/ts/index.ts:242-259)

1. Caller invokes `drawStarGrid(drawingId, radius, size, background_theme, lines_theme, mountSelector)`.
2. `appendSVGToDOM(...)` (`index.ts:77-95`) does `d3.select(mountSelector).append("svg")` (`index.ts:80`),
   sets width/height/viewBox/title/id, appends `<defs>` + two `appendLinearGradientDef` gradients, and
   returns a `d3SVG` (`d3.Selection<SVGSVGElement,...>`) — **the object holding the SVG root**; every
   subsequent append chains off it.
3. `applyBackground(svg, background_theme)` (`index.ts:106-110`).
4. Twelve **direct, synchronous d3 append calls** follow, no intermediate data structure: e.g.
   `appendPolygon(svg, star.lines, lines_theme)` (`index.ts:246`), repeated for rotations and
   `star.right()`/`star.above()`/`star.above().right()`.
5. Returns `svg`.

Each `appendPolygon` builds a `Point[]` fresh from `Star.points`/`Polygon.points` getters, converts to
`Line[]` via `Lines.fromPoints`, then emits **one `<polyline>`** with a computed `points` attribute.
**No intermediate geometry-only array survives past the single append call** — geometry is produced,
serialized to SVG attributes, and discarded. All 8 `draw*` functions in `index.ts` follow this shape:
`appendSVGToDOM` -> `applyBackground` -> N inline `append*` calls interleaved with geometry construction.

## 2. The SVG-append layer (src/ts/canvas.ts, 177 lines — sole owner of element creation)

| method | emits | file:line | uses d3? |
|---|---|---|---|
| `appendCircleWithMidpoint` | 2x `<circle>` | `canvas.ts:56-74` | yes — `onto.append('circle')` x2 |
| `appendCircle` | 1x `<circle>` | `canvas.ts:90-101` | yes — returns the selection |
| `appendLine` | 1x `<line>` | `canvas.ts:112-121` | yes |
| `appendPolygon` | 1x `<polyline>` (none on empty) | `canvas.ts:133-150` | yes — builds `points` by hand-joining coords (`_.join`), not `d3.line()` |
| `appendText` | 1x `<text>` | `canvas.ts:163-177` | yes |
| `appendSVGToDOM` (index.ts) | `<svg>`+`<defs>`+2 gradients | `index.ts:77-95` | yes — `d3.select(...).append("svg")` |
| `appendLinearGradientDef` (index.ts) | `<linearGradient>`+2 `<stop>` | `index.ts:39-58` | yes |
| `applyBackground` (index.ts) | styles existing `<svg>` | `index.ts:106-110` | yes |
| `rotateOuterCircles` (index.ts) | mutates `<circle>`s via `.transition()` | `index.ts:122-139` | yes — `d3.easeLinear`, `.transition().attr(...)` |

**d3 IS a dependency:** `package.json` `d3@^7.9.0`, `@types/d3@^7.4.3`; imported `import * as d3 from 'd3'`
at `index.ts:6`; `canvas.ts` uses `d3.*` as **ambient types only** (via `export as namespace d3`), the
selections passed in as params. Webpack marks d3/lodash as `externals` (`webpack.config.js:48-55`) —
loaded via `<script>` at runtime, not bundled. **All appends are one-shot `.append(...)` — never
`.selectAll(...).data(...).join(...)`. Grep for `.data(`/`.join(` across src/ts and tools: absent
(outside unrelated Array/lodash `.join()`).**

## 3. Primitive object model

- **Polygon** (`polygons.ts:21-53`): boundary is a **lazy `Point[]` getter** (`points`, `:38-41`) sampling
  `outerCircle.pointsOnCircumference(n, radial_shift)`; a `lines` getter (`:43-45`) wraps it via
  `Lines.fromPoints`. No path string, no cached array — every read re-derives from `center`/`size`/`radial_shift`.
- **Star** (`star.ts:19-106`): same shape — `points` getter (`:43-73`), `lines` getter (`:75-77`).
- No path-string representation anywhere (`d3.line()`/path-`d` absent; `appendPolygon` hand-builds
  `points="x,y ..."` for a `<polyline>`).

**Anything face-list-shaped today? Absent.** No array-of-closed-polygons-with-metadata survives past
a render call. Closest is transient `Polygon[]`/`Hexagon[]` arrays some `draw*` build before looping
(e.g. `nonagonsThatFormA6PointStarCenteredAt` -> `Polygon[]`, `index.ts:175-198`) — but they carry **no
index/id, no centroid, no class tag, no ring field**, immediately consumed by `_.forEach(..., p ->
appendPolygon(svg, p.lines, theme))`.

**Which bikar `FaceConstruct` fields (`index`,`polygon`,`centroid`,`colorHex`,`classes`,`ring`,`isCurved`
— `bikar/packages/core/src/viz/face-constructs.ts:16-39`) already exist:**

| FaceConstruct field | sacred-patterns analog | present? |
|---|---|---|
| `polygon` (ordered `Point[]`) | `Polygon.points`/`Star.points` getters | yes, but re-derived each read, not stored |
| `index` (stable per-face id) | none | absent |
| `centroid` | only `center`/`midpoint` (construction center, not a computed centroid) | absent |
| `classes` (category tags) | none — `CircleMetadata.stroke`/`fill` is styling only | absent |
| `ring` / level grouping | `Circle.metadata.level` (recursion-depth int, `circles.ts:15-20`) — **Circle only**, not Polygon/Star | partial |
| `colorHex`/style | `CircleMetadata.fill`/`.stroke` (Circle only); `LineTheme` applied uniformly per append call, not per-face | partial |
| `isCurved` | n/a — no curved primitives; every boundary is straight `Line` segments | not applicable |

## 4. d3 presence

Used exclusively as a thin DOM-creation shim (`.select().append().attr().style()`), never data-binding.
`d3.select` (`index.ts:80`), `d3.easeLinear` (`index.ts:131`). No `.data()`/`.join()`/`.enter()`/`.exit()`
anywhere in src/ts. No d3 scales — all coordinate math is hand-rolled trig in Circle/Polygon/Star. The
target pattern already exists in the bikar sibling: `joinFaces(g, constructs, opts)` at
`bikar/packages/web/src/viz-d3.ts:46-64` (`g.selectAll('path.face').data(constructs, key).join('path')...`,
keyed by `String(f.index)`), fed by `faceConstructs()` at `bikar/packages/core/src/viz/face-constructs.ts:53-73`.

## 5. Build/test/gate constraints

- No CI — every enforced check is a git hook; `gate-parity.yaml` maps each hook to its whole-tree form
  so `make local.ci` runs what the hooks partially cover. `pre-commit::typecheck-lint` -> `npm run lint &&
  npm run typecheck`, gated on staged `^src/ts/.*\.ts$`.
- **The binding constraint: `test/regression/check.js`** — a golden-file test. Loads the built UMD bundle
  into jsdom, calls `drawHexagonWithSurroundingNonagons('d6', 100, 6, {...},{...})` (`check.js:67`) and
  asserts against `test/regression/reference.svg`: **exact count** of `points="..."` values (`:98-104`),
  **exact match in sorted order** of every `<polyline>` points string (`:93-115` — tolerates emission-order
  changes but not coordinate/count/grouping changes: splitting one polyline into two paths fails it), and
  **exact element counts** for polyline/circle/linearGradient/stop/defs (`:120-130`). Keyed to
  `drawHexagonWithSurroundingNonagons`. **Moving `<polyline>`-per-shape to `<path>`-per-face breaks it
  outright** even if pixels are identical — must be regenerated via `capture-baseline.js`, not surprised.
- Playwright `test:visual`/`test:studio` target the weave-progress/studio pages, not the src/ts pipeline.
- **No keywords snapshot, no public-surface manifest** in sacred-patterns (searched; `public-surface.json`
  is a bikar-only deploy-host concept, not code API surface).

## 6. The refactor seam

**A shallow chokepoint.** Every drawing funnels through `appendSVGToDOM` (one place the d3SVG root is made)
and canvas.ts's five `append*` (one place geometry becomes a DOM node) — but **between** them, emission is
scattered: each of the 8 `draw*` functions interleaves construction with 1-12+ inline `append*` calls (47
call sites in index.ts), each in its own `_.forEach`/`_.flatMap` loop. There is no single "compile geometry,
then render" boundary today.

**Smallest slot-in set:**
- **New module `src/ts/faces.ts`** (mirroring bikar's `face-constructs.ts`): maps a `Polygon[]`/`Star[]`/
  `Circle[]` collection to a `FaceConstruct[]`-shaped array — sits alongside polygons.ts/star.ts/circles.ts.
- **New d3 data-join renderer** (mirroring `viz-d3.ts:joinFaces`): a `joinFaces(g, constructs, opts)`
  doing `.selectAll('path.face').data(constructs, key).join('path')...`, emitting `<path class="face">`
  per face — replacing per-shape `appendPolygon`.
- **All 8 `draw*` functions** change call sites from N inline `appendPolygon(...)` to: build shape array
  -> map to `FaceConstruct[]` -> one `joinFaces(svg, constructs)` call. Mechanical (geometry getters reused
  as-is), but touches all 8 since none produces an intermediate shape array uniformly.

**CLAUDE.md conventions the refactor must honor** (`sacred-patterns/CLAUDE.md`):
- **Relative-to-origin scaling** (`:158`): every coordinate/size a ratio of the originating circle's
  `(cx,cy)` and `R`; `FaceConstruct.polygon`/`.centroid` stay in those origin-relative terms — the
  face-list step is a pure mapping, never a place to introduce absolute/pixel coords.
- **No unexplained `R*0.52`-style constants** (`:157`).
- **Tenet 10 (functional/immutable)** (`:24`): the mapper is a pure function of its inputs.
- **Tenet 15 (typed variants, no bag `Record<string,unknown>`)** (`:31`): a real `FaceConstruct`-analog
  interface, not a metadata bag (theme.ts already migrated off `unknown` for this reason).
- **Golden-file discipline**: regenerate `test/regression/reference.svg` deliberately
  (`node test/regression/capture-baseline.js`), never let it silently start failing.

## Effort read

A **localized insert, not a geometry rewrite** — but it touches every `draw*` function's render call site.
The geometry layer (Point/Line/Circle/Polygon/Star and their `points`/`lines` getters) needs zero changes:
the `faceConstructs()`-style mapper is a thin pure adapter over existing getters, exactly as bikar's
`faceConstructs()` is a thin adapter over `EvaluationResult.faces`. Two genuinely new pieces: (1) the
geometry->`FaceConstruct[]` mapper, (2) the `joinFaces` data-join renderer. The cost is **breadth, not
depth**: 47 inline append call sites across 8 draw functions regroup into "build array -> map -> one
joinFaces". Two draw functions (`drawRotatingCircles`, `drawCirclesRecursively`) mix polygon + circle
rendering with `.transition()` animation (`rotateOuterCircles`, `index.ts:122-139`) that doesn't map onto
a static face-list join and needs the d3 `.join()` update-branch — a distinct code path, not a new
mechanism. The binding external constraint is `check.js`'s exact-DOM-shape assertion, regenerated as part
of the same change.
