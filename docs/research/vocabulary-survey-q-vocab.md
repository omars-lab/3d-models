<!--
provenance:
  date: 2026-09-02
  produced-by: Explore subagent (read-only vocabulary survey), driven by Claude Code (Opus 4.8)
  method: source read across bikar@5b9fb27 (packages/web, packages/core/src/viz,
    packages/core/src/kernel3d, packages/qiyas-schema) and sacred-patterns@0d3ad1e
    (src/ts, templates, docs, tools); every term cited file:line. No web sources —
    this is a code-vocabulary measurement, not a literature survey.
  feeds: docs/vocabulary-convergence-design.md (Phase 3 / Q-VOCAB), plan.md §2 row 2.4
  note: preserved verbatim from the survey. This is the grounding measurement for the
    convergence design doc; the "thin rename vs deep refactor" verdict below is what the
    Q-VOCAB decision (d3-integration-design.md §5.3) was designed to make cheap to see.
-->

# Vocabulary survey: d3 Phase 3 (Q-VOCAB)

Three surfaces: **A** the rosette explorer (bikar), **B** the orb instrument (bikar),
**C** sacred-patterns. The question: how much naming vocabulary is actually SHARED vs
DIVERGENT, so a convergence refactor can be scoped.

## Surface A — rosette explorer

| concept | term used | code identifier | file:line |
|---|---|---|---|
| the page itself | "Rosette explorer" | route `/rosette-explorer`, module comment | `bikar/packages/web/src/rosette-explorer.ts:1-2` |
| pattern roster item | "pattern" (picker label) | `PatternEntry.name` / `.label` | `bikar/packages/web/src/rosette-explorer.ts:124-141` |
| roster: rosette figure | "Rosette" | `Rosette-N.bkr` | `bikar/packages/web/src/rosette-explorer.ts:131` |
| roster: star figure | "Star {n/k}" | `Star-N.bkr` | `bikar/packages/web/src/rosette-explorer.ts:132` |
| roster: girih figure | "Girih {10/3}" / "Girih decagon" | `Girih-10.bkr`, `Girih-Decagon.bkr` | `bikar/packages/web/src/rosette-explorer.ts:134-136` |
| roster: tiling figure | "Hex field (6-fold tiling)" / "Star-8 field (square tiling)" | `Hex-Tiled.bkr`, `Star-8-Tiled.bkr` | `bikar/packages/web/src/rosette-explorer.ts:138-140` |
| a figure's declared width | "spanPU" | `PatternEntry.spanPU` (pattern units) | `bikar/packages/web/src/rosette-explorer.ts:127` |
| a knob | "dial" | `DialModel`, CSS `.dial` | `bikar/packages/web/src/rosette-explorer.ts:49-57`; `bikar/packages/web/rosette-explorer.html:454-497` |
| dial param key | raw `.bkr` param name, e.g. `petal_reach` | `ParamSpec.name` | `bikar/packages/web/src/rosette-explorer.ts:59-63,80-92` |
| dial label text | humanized (`_`->space) param name | `humanizeParamName()` | `bikar/packages/web/src/rosette-explorer.ts:61-63` |
| overlay-only knob: plate offset in studs | "span" | `dSpan` / `state.span` | `bikar/packages/web/rosette-explorer.html:478-480`; `rosette-explorer.ts:211` |
| overlay-only knob: inset between outline and anchors | "grout" | `dGap` / `state.gapMm` | `bikar/packages/web/rosette-explorer.html:483-485`; `rosette-explorer.ts:212` |
| overlay-only knob: baseplate offset | "nudge X" / "nudge Y" | `dNudgeX`, `dNudgeY` / `state.nudgeX/Y` | `bikar/packages/web/rosette-explorer.html:492-497`; `rosette-explorer.ts:213-214` |
| baseplate size roster | "plate" | `PLATES[].id/w/h/label` | `bikar/packages/web/src/rosette-explorer.ts:195-201` |
| geometry construct: one piece of a compiled figure | "face" / "piece" | `FaceConstruct` | `bikar/packages/core/src/viz/face-constructs.ts:16-39` |
| face boundary | "polygon" (a closed ring) | `FaceConstruct.polygon` | `bikar/packages/core/src/viz/face-constructs.ts:24` |
| face center point | "centroid" | `FaceConstruct.centroid` | `bikar/packages/core/src/viz/face-constructs.ts:26` |
| face tag/category | "class" (e.g. `star`, `petal`) | `FaceConstruct.classes` | `bikar/packages/core/src/viz/face-constructs.ts:33`; used at `rosette-explorer.ts:314-315` |
| concentric grouping | "ring" | `FaceConstruct.ring` | `bikar/packages/core/src/viz/face-constructs.ts:36` |
| LEGO anchor point | "anchor" (tube / pin) | `PieceSolve.anchors`, `sol.kind` | `bikar/packages/web/src/rosette-explorer.ts:246-256,299-327` |
| a stud that a piece covers | "stud" / "engaged stud" | `engagedPU`, `drawStuds()` | `bikar/packages/web/src/rosette-explorer.ts:250,399-410` |
| a failed-fit candidate | "dropped candidate" | `droppedPU`, `drawGhosts()` | `bikar/packages/web/src/rosette-explorer.ts:252,446-465` |
| the d3 face->path binding | "join" (enter/update/exit) | `joinFaces()` | `bikar/packages/web/src/viz-d3.ts:46-65` |
| the data file: bundled pattern text | "starter pattern" | `StarterPattern{name, content, dirty, folder}` | `bikar/packages/web/src/starter-patterns.ts:29-36` |

## Surface B — orb instrument

| concept | term used | code identifier | file:line |
|---|---|---|---|
| the page itself | "Orb instrument" | route `/orb-instrument`, module comment | `bikar/packages/web/src/orb-instrument.ts:1-2` |
| symmetry-axis view id | "view" (`vertex-N`, `face-N`, `edge-2`) | `OrbViewAxis.id`, `dView` | `bikar/packages/core/src/kernel3d/orb-views.ts:16-29,44-53`; `bikar/packages/web/orb-instrument.html:528-531` |
| view kind | "vertex" / "face" / "edge" | `OrbViewKind` | `bikar/packages/core/src/kernel3d/orb-views.ts:14` |
| view's rotational order | "fold" | `OrbViewAxis.fold` | `bikar/packages/core/src/kernel3d/orb-views.ts:26` |
| a rendered face's shape count | "faces" (picker readout `N faces`) | `OrbViewRender.faceCount` | `bikar/packages/web/src/orb-view-svg.ts:37-39`; `orb-instrument.ts:106` |
| join key between rendered SVG and qiyas encoding | "the join key is each face's own ring" (page copy) | `data-face-index`, `SvgFace.ring`, `ringKey()` | `bikar/packages/web/orb-instrument.html:507-509`; `qiyas-join.ts:34-38,113-123,137-139` |
| a rendered face's verdict | "status" (`matched`/`missing`/`ambiguous`/`unknown`/`unclaimed`) | `RefStatus`, `FaceStatus.status` | `bikar/packages/web/src/qiyas-join.ts:41,66-71` |
| a face/shape's identity | "id" | `refId` / `reconId` (qiyas `ref_id`/`recon_id`) | `qiyas-join.ts:44-56`; schema `bikar/packages/qiyas-schema/src/diff.ts:85-88` |
| positional accuracy | "drift" / "position_drift_px" | `driftPx`, `position_drift_px` | `qiyas-join.ts:48,161`; `packages/qiyas-schema/src/diff.ts:85` |
| overlay scores panel | "composite / structural / geometric / symmetry" | `DiffLike.scores.{composite,structural,geometric,symmetry}` | `bikar/packages/web/src/orb-instrument.ts:289-301`; schema `packages/qiyas-schema/src/diff.ts:93-97` |
| shapes not reconstructed | "drop" | `diff.missing_in_recon` | `orb-instrument.ts:286-298` |
| shapes reconstructed with no reference | "surplus" | `diff.extra_in_recon` | `orb-instrument.ts:297-298` |
| worst positional error | "max drift" | computed `maxDrift` | `orb-instrument.ts:291,299` |
| census counters | "matched / missing / ambiguous / unknown / extra in recon / unclaimed faces / unjoined shapes" | `JoinResult.counts`, `showCensus()` | `qiyas-join.ts:62,167-173`; `orb-instrument.ts:303-334` |
| dial: degrade rate | "drop every" | `dEvery` / `degrade(enc, every)` | `bikar/packages/web/orb-instrument.html:533-536`; `orb-instrument.ts:117-120` |
| dial: pattern picker | "pattern" | `dPattern` | `orb-instrument.html:522-526` |
| dial: view picker | "view" | `dView` | `orb-instrument.html:528-531` |
| toggle: live vs fixture | "Live" | `tLive` | `orb-instrument.ts:61,72-75,374` |
| toggle: flagged-face markers | "Marks" | `tMarks` | `orb-instrument.ts:62,232-256` |
| toggle: status tint | "Tint" | `tTint` | `orb-instrument.ts:63,220` |

## Surface C — sacred-patterns

| concept | term used | code identifier | file:line |
|---|---|---|---|
| repo/product framing | "Sacred Patterns... generates sacred geometric patterns as SVG" | — | `sacred-patterns/CLAUDE.md:7` |
| geometric primitive: point | "Point" | `Point` class | `sacred-patterns/src/ts/points.ts` (per `CLAUDE.md:127`) |
| geometric primitive: line | "Line" | `Line`, `Lines` | `sacred-patterns/src/ts/lines.ts` (per `CLAUDE.md:128`) |
| geometric primitive: circle | "Circle" | `Circle` (carries `level`, `fill`, `stroke`) | `sacred-patterns/src/ts/circles.ts` (per `CLAUDE.md:129`) |
| geometric primitive: N-gon | "Polygon" base + named subclasses | `Polygon`, `Triangle`..`Decagon`, `PolygonWithSides` | `sacred-patterns/src/ts/polygons.ts:21-33,83-232` |
| geometric primitive: star | "Star" | `Star`, `FivePointStar`, `ElongatedFivePointStar` | `sacred-patterns/src/ts/star.ts:19-143` |
| star roster in doc comments | "N-pointed star" | `Star.numberOfPoints` | `sacred-patterns/src/ts/star.ts:7-21` |
| a drawing/pattern (top-level unit) | "drawing" / `draw*` functions | `drawCirclesRecursively`, `drawChainedStars`, `drawStarGrid`, `drawHexagonWithSurroundingNonagons`, `drawRotatedStar`, `drawDifferentStars`, `drawRotatingCircles`, `drawDifferentPolygons` | `sacred-patterns/src/ts/index.ts:216-469` |
| pattern parameterization convention | "Geometric construction from central origin" / "Relative-to-origin scaling" | `CLAUDE.md` Key Conventions | `sacred-patterns/CLAUDE.md:154-155` |
| positioning param names | `center`, `size`, `radial_shift` (constructor args) | `Polygon`, `Star` constructors | `sacred-patterns/src/ts/polygons.ts:22`; `sacred-patterns/src/ts/star.ts:21` |
| render styling bags | "theme" (`BackgroundTheme`, `LineTheme`) | `applyBackground()` | `sacred-patterns/src/ts/theme.ts`; used `sacred-patterns/src/ts/index.ts:106-110,216-469` |
| catalog naming convention (documented) | "Symmetry: D{n} (n-fold) / Star notation: {n/k} / Tiling method: radial rosette / periodic / girih / hybrid" | patterns-catalog.md template | `sacred-patterns/.claude/skills/generate-drawing/learnings/patterns-catalog.md:1-20` |
| geometry primitive doc index | "Geometry Primitive Layer" | CLAUDE.md Architecture | `sacred-patterns/CLAUDE.md:125-131` |
| "dial"/control terminology (weave-studio tool only) | "dials", `URL_KEYS` param map, snake_case keys (`field_angle`, `field_wave_lo`, `step`, `shadow`) | `URL_KEYS`, `syncControlsFromState()` | `sacred-patterns/tools/wave-plan-server.py:582-621` |
| naming-convention/glossary document | none dedicated (CLAUDE.md sections + patterns-catalog.md template are closest; REFERENCES.md is domain terms) | — | `sacred-patterns/REFERENCES.md:1-16` |

## Cross-surface concept map

| concept | A's term | B's term | C's term | AGREE / DIVERGE / ABSENT |
|---|---|---|---|---|
| one drawable pattern/figure unit | "pattern" (`PatternEntry`, `.bkr`) | "pattern" / "orb" (`.bkr`) | "drawing" (`draw*` function) | DIVERGE — A/B share "pattern"; C calls it a "drawing" |
| pattern name display convention | `Star {n/k}` | `Star-Orb` (bare `.bkr` filename) | "Star notation: {n/k}" (catalog doc) | AGREE (concept) — `{n/k}` in A and C's convention; B doesn't surface `{n/k}` (view ids are `vertex-N`/`face-N`/`edge-2`) |
| a knob/control | "dial" (`DialModel`, CSS `.dial`) | "dial" (CSS `.dial`) | "dial" only in *weave-studio* tool, not core lib | AGREE A/B (word + markup); PARTIAL in C (peripheral tool only) |
| dial parameter key casing | snake_case `.bkr` names (`petal_reach`) humanized | N/A (B has no pattern dials) | snake_case (`field_angle`, `radial_shift`) | AGREE — A and C both snake_case |
| a piece of compiled geometry | "face" (`FaceConstruct`, `.index`) | "face" (`FaceStatus`, `.faceIndex`) | no equivalent — composes primitives directly | DIVERGE (A vs B: `index` vs `faceIndex`) / ABSENT (C) |
| "ring" | concentric group id (`FaceConstruct.ring`) | face boundary polygon (`SvgFace.ring`) | not a geometry term; closest is `Circle.level` | DIVERGE — same word, two unrelated things A vs B; C uses "level" |
| construction/positioning origin | `.bkr` coords, `recentred()` | mm viewBox, `SvgFrame.viewBox` | "central origin", ratio of `R`,`(cx,cy)` (doc convention) | ABSENT cross-mapping — A/B compiled frames; C a documented rule, no data structure |
| N-fold symmetry vocabulary | prose in roster labels | "fold" (`OrbViewAxis.fold`) | "D{n} (n-fold)" (catalog template) | AGREE (loose) — no shared field name |
| status/verdict of a piece | `pass`/`failures` (anchorability) | `status` enum | `Confidence: X.XX` (catalog, human-entered) | DIVERGE — three verdict shapes for one idea |
| id/key for a tracked shape | face `index` | qiyas `refId`/`reconId` | no per-shape id | DIVERGE (A vs B) / ABSENT (C) |
| drift/deviation metric | none | `driftPx`/`position_drift_px`, `max_drift` | none in code ("Confidence" closest) | ABSENT in A and C |
| d3 join mechanics | `joinFaces()` reusable, keyed by `f.index` | inlined `.data().join()` in `paint()`, keyed by `faceIndex` | no data-join; `canvas.ts` `append*` imperative | DIVERGE (A vs B) / ABSENT (C — imperative append) |
| geometric primitive class names | none (works from compiled DSL) | none | full OO hierarchy `Point`..`Star` | ABSENT in A/B — structural, not naming |

## Divergence summary

**Real name conflicts (same thing, different word — a thin rename fixes these):**
- "face" identity field: `index` (A `FaceConstruct.index`) vs `faceIndex` (B `FaceStatus.faceIndex`) — same ordinal into `result.faces`, different key, both consuming the same `FaceConstruct`/`data-face-index` origin.
- "ring": A = concentric-band classification (`FaceConstruct.ring`); B = a face's boundary polygon (`SvgFace.ring`). A genuine collision — the same identifier means two different geometric ideas in sibling modules of one page family. Rename B's to `boundary`/`outline` to free "ring" for A's concentric sense.
- "dial" vs constructor-argument: A/B expose a schema-driven `DialModel` (label+key+bounds); C's core lib has no dial concept — parameters are plain constructor args with no declared range/step/label. C's only dial vocabulary lives in a peripheral tool (`wave-plan-server.py`), snake_case URL keys already resembling `.bkr` naming.

**Concepts one surface simply lacks (absence, not conflict):**
- B has no pattern/parameter dials (only `pattern`, `view`, `drop every` — orchestration knobs).
- C has no compiled/faceted intermediate (`FaceConstruct`/`SvgFace`) — composes primitives (`Circle`, `Polygon`, `Star`) directly into SVG via imperative `append*`, never through a d3 `.data().join()`. Structural gap: no C-side "face" to rename.
- C has no qiyas-style verdict/score vocabulary in code — closest is a hand-filled `Confidence: X.XX` in a markdown template.
- A has no first-class "fold" field — roster labels bake fold into prose.

**Estimate — thin rename vs deep refactor:**
**A<->B is a thin rename** (bikar's own two surfaces): they already share `FaceConstruct`,
`viz-d3.ts:joinFaces()`, and the `.bkr` coordinate model — the only real conflicts are two
field names (`index`/`faceIndex`, the `ring` collision) plus B not routing its d3 join through
`joinFaces()`. A handful of renames plus one refactor converge A and B.

**Bringing C into the convention is a deeper, structural undertaking, not a rename:** C's
`src/ts` library has no compiled-pattern intermediate (no `FaceConstruct`/face-index, no
schema-driven dial, no d3 enter/update/exit idiom — it appends SVG imperatively from OO
primitive instances). Converging C's *vocabulary* requires first converging C's *architecture*
(introducing a compiled-geometry -> face-list step and a data-join rendering step). The one
genuinely reusable alignment already in place is star/pattern notation (`{n/k}`, N-fold) and
snake_case parameter-key casing, both of which C's documentation/tooling already use in a form
compatible with A's `.bkr` convention.
