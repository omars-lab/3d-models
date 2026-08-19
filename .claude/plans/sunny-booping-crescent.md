# Make the orb breakdown pages teach construction — audit + plan

## Context

The breakdown page shipped (bikar #110, 3d-models #84) with build stages, a 36-frame
turntable, and a live-viewer handoff. The user reports it still fails its core job:
**a newcomer cannot see how the flat overhead drawing becomes an orb.** This plan
starts from a measured audit of what a viewer actually sees, then fixes the pipeline
so every published breakdown is a valid, newcomer-friendly education in how the orb
is constructed.

## Audit findings (measured — frames rendered to PNG and inspected, code read to file:line)

**A1 — Every frame is a flat gray blob.** All faces carry the same `fill="#8a8a8a"`
(`DEFAULT_ORB_VIEW_FILL`, bikar `orb-view-renderer.ts:12`). The star pattern is
*invisible as a pattern*; the turntable is the same blob tilted. A rotating
uniform-gray projection reads as a wobbling flat mandala, not a turning sphere.

**A2 — Zero depth cues.** No silhouette circle, no shading, no back hemisphere
(front-cap cull at `orb-views.ts:171`). Nothing ever disappears around a limb —
the one cue that proves "sphere".

**A3 — The flat pattern is never shown, and the flat→sphere map runs before
frame 1.** The map exists only as a single non-parameterised jump (`makeFaceLift`
`face-frame.ts:93`, then `normalize3/scale3` `orb-views.ts:166–169`). Every stage
frame — including `element 1` — is already on the sphere. No flat 2D pattern
image ships in any breakdown directory; `source.bkr` is fetched only as compiler
input, never displayed. No interpolation machinery exists anywhere in core.

**A4 — No placement story.** The repeat stages *are* partial tilings, but with no
tint distinguishing the newly placed unit (faceColors is keyed by
`patternFaceIndex`, shared by all 20 copies — `orb-view-renderer.ts:79`), a viewer
sees strokes accreting in a fixed overhead view. The designed "frame 0 = bare
base solid" (design doc §3.4) was never built. `data-orb-base-face` is emitted
per polygon but nothing consumes it.

**A5 — The two cameras never meet.** Stages are on `vertex-5` (elevation ≈58.3°);
all 36 turntable frames are pinned at elevation 18° (`cli/src/index.ts:1055`).
Byte-verified: no turntable frame equals the terminal stage frame. The page
compounds it by showing the spin *first*, then jumping back to a different camera
showing one hexagon.

**A6 — The copy is jargon, and its one explanatory sentence is wrong.** No
sentence on the page mentions a flat pattern, a base polyhedron, lifting, or
wrapping (grep-verified). Shown untranslated: `element then repeat`,
`vertex-5`, `unit 3`, `new: C1:every:2:#0 · layer:0 · tri`, `front cap`, `18° up`.
The §2 sentence (`breakdown-main.ts:432`) says element stages "lay down one repeat
unit face by face" — it describes the wrong axis (element stages hold one base
face and add pattern elements). Frames 10→11 show an unchanged picture while the
caption flips `element 10` → `unit 1`, unexplained.

**A7 — The design doc never specified the transition.** §1.1 delegates the flat
side to `derivation-worksheet-design.md`; §4.2 defines "the gap" as pattern→STL;
§11.4 caps per-frame prose at an ordinal. The turntable does not appear in the
design doc at all — it was added ad hoc. The §9 timelapse gate is NOT BUILT
(task #17). The doc header still says "the page of section 7.3 is not built."

**Existing hooks (found, to reuse — not new):**
- `renderOrbViewSVG` accepts `faceColors`/`faceClasses`; per-polygon
  `baseFaceIndex` is in the scene and the SVG.
- `orbCellStages`/`sceneAtStage` (partial tiling) + `projectOrbViewScene` with a
  free `view.axis` (arbitrary camera) exist and are used — just never together.
- The 2D pattern renderer exists (the DSL is 2D-first); the flat drawing is
  renderable today.
- Terminal identity: last stage frame is byte-identical to
  `build/orb-views/<orb>/<view>.svg` — an invariant that must evolve deliberately,
  and a qiyas constraint: the gray default exists so qiyas can encode the views;
  restyling `build/orb-views` invalidates recorded composites.

## The story the page must tell (the fix, page half)

A newcomer needs five beats, in order — each currently missing or broken:

1. **"This is the flat drawing."** Show the actual 2D pattern (one repeat unit,
   the real flat SVG) first. New manifest content; the 2D renderer already exists.
2. **"It gets copied onto every face of this solid."** The §3.4 bare base solid,
   then one face carrying the unit, highlighted. Names the polyhedron in plain
   words ("an icosahedron — 20 triangular faces").
3. **"Copies tile the sphere until it closes."** The existing repeat stages,
   restyled: newly placed unit tinted, prior units neutral (baseFaceIndex-keyed
   colors), with captions like "copy 7 of 20".
4. **"And it really is a sphere — watch it turn."** The turntable, with depth
   cues (shading + silhouette), entered by camera-continuous transition frames
   from the stage axis — no jump.
5. **"Now turn it yourself."** The existing live-viewer handoff (works today).

Page reorders to stages-then-spin (construction before proof), copy rewritten in
newcomer vocabulary with the wrong sentence fixed, jargon either translated
(`vertex-5` → "looking down a 5-point star vertex") or moved to the table.

## Scope decisions (user-chosen, govern everything below)

1. **Style every human surface; keep the gray instrument for qiyas.** (Revised
   from "everything, re-record qiyas" after design-time evidence: qiyas's
   detector classifies `fill="none"` elements as stroke outlines and would read
   a ghosted back hemisphere as foreign contours — `svg_primitives.py:584`;
   bikar pins per-orb composites at tolerance 5e-4 plus a drop table pinned at
   0 in `packages/lab/src/scripts.ts`; and `build/orb_previews.py:40-42`
   recolors gallery views by *literal string replacement* of `fill="#8a8a8a"`,
   silently mangling any varied fill. A full re-record is a three-repo cascade
   repeated on every future style tweak.) So: every surface a human looks at —
   gallery hero previews, breakdown transition + turntable frames — gets the
   depth-cued style; the qiyas-scored SVG/PNG/gt.json instrument set stays
   **byte-stable**, protected by a snapshot test. Not the D-014 23-row table
   either way — that records coupon mesh metrics, untouched by any SVG change.
2. **Generality is a hard requirement.** Every mechanism (depth cues, highlight,
   transitions, endpoint frames, captions) is parameterised by what the
   manifest/scene declares — orb family (cell / strand / wheelfield), stage
   axes, view kinds — never by orb-name special cases. Acceptance shape:
   `make orbs` regenerates all 14 breakdowns and each tells a coherent story
   with zero per-orb code. Where a family can't support a beat, the fallback is
   a designed family-level variant, not an empty hole. The family parameter is
   *measured, not assumed* — derivable from each manifest's frame-kind set:
   cell-only `{element,repeat}` (9 orbs), cell+strand `{element,repeat,strand}`
   (4 orbs), strand-only `{strand}` (Maclado9Overlap alone, and alone at
   turntable=0). Stage views vary too (vertex-3 ×11, vertex-4 ×1, vertex-5 ×2),
   so camera-transition math reads the stage axis from the manifest.
3. **Maclado9Overlap is first-class, in scope now.** The user's words: "we over
   promised but under delivered." Its page reaches parity: real story beats for
   the woven construction (60 loops over 420 crossings, parity solve) and a
   working ribbon turntable with depth cues (absorbs task #35). Its stale
   shipped cell views (task #14) get resolved in the same stroke — regenerated
   as ribbon views or removed, with the gallery/qiyas implications stated.

## Renderer / geometry / gates half (designed; all anchors verified by agent)

### A. Depth cues — opt-in `OrbViewStyle` on the existing renderer

- `OrbViewPolygon` gains one additive field `meanDot` (mean of per-vertex
  `dot(v̂, view.axis)`), computed where `minDot` already is: `projectFacePolygon`
  (`orb-views.ts:154`), `projectSphericalCells` (:252), and the band builder in
  `orb-ribbons.ts` (bands already compute a center dot for `depthMm`).
  `RibbonViewPolygon extends OrbViewPolygon` → ribbons covered by inheritance.
  `meanDot`, not `minDot`: min is rim-biased and bands at the cap boundary.
- `render/orb-view-renderer.ts`: `OrbViewSVGInput`/`OrbRibbonViewSVGInput` gain
  `style?: OrbViewStyle` — `{ shading?: {mode:'lambert', strength?}, silhouette?:
  boolean }`. Lambert = luminance-only multiply of the resolved fill,
  `L = 0.35 + 0.65·clamp01(meanDot)` blended by strength; strokes untouched.
  Silhouette = one `<circle r={radiusMm} fill="none" stroke="#333333"
  data-orb-silhouette="true"/>` after the background rect. Shaded elements carry
  `data-orb-style="shaded"` so the gate distinguishes frame classes.
  **`style` absent ⇒ bytes character-identical to today — pinned by a snapshot
  test; this is the test that protects qiyas, `orb_previews.py`, and the pinned
  composites forever.**

### B. Per-unit highlighting (stage frames)

- `baseFaceColors?: ReadonlyMap<number,string>` keyed by `baseFaceIndex`
  (already on every polygon, emitted as `data-orb-base-face`);
  `strandColors?: ReadonlyMap<number,string>` keyed by strand id for ribbon
  input. Precedence: `baseFaceColors` > `faceColors` (patternFaceIndex) >
  `DEFAULT_ORB_VIEW_FILL`. One exported constant `DEFAULT_ORB_HIGHLIGHT_FILL`;
  highlighted elements carry `data-orb-highlight="true"`.
- CLI drives it from the stage's own key domain — `element` → patternFaceIndex
  override, `repeat` → `baseFaceColors: {stage.key: highlight}`, `strand` →
  `strandColors` — zero per-orb code.
- **Terminal identity preserved by construction:** stage frames stay *unshaded*
  (no style), and the sequence gains one final `kind:'complete'` frame with no
  highlight → byte-identical to the shipped instrument view (`ribbons/<view>.svg`
  for the strand-only family). §4.1's invariant survives unrelaxed, moved to
  the complete frame.

### C. Camera continuity — slerp transition frames

- New `writeTransition` in `cli/src/index.ts`: slerp from the stage view's axis
  (read from the manifest — vertex-3/-4/-5 vary) to the *nearest* turntable
  orbit point (`entersAtIndex = round(az/(360/n)) % n`); frame count =
  `ceil(arc/(360/n))` so tilt and orbit share angular speed (~4 frames for
  StarOrb). Style ramps with `t`: `strength = t`, silhouette on for `t > 0` —
  so **transition[0] is byte-identical to the complete stage frame and
  transition[last] to turntable[0]**: both junctions pin as byte checks.
- Turntable frames render at full style. Manifest gains a separate top-level
  `transition: {frames: [...], entersAtIndex} | null` — `frames`/`turntable`
  untouched (same separation argument as `cli/src/index.ts:1187-1190`); page
  plays stages → transition → spin entering at `entersAtIndex`.

### D. The two missing endpoints

- **Flat pattern**: `renderTimelapse` already holds the `EvaluationResult`; one
  call to the existing 2D path (`renderSVG(renderOptionsFromResult(result))`,
  `svg-renderer.ts:121`) writes `<orb>.flat.svg`. New manifest key — *not*
  frame 0 (its viewBox is the pattern's, would break per-frame viewBox
  identity): `flat: {file, relation: 'lifted'|'preview'} | null`, `'lifted'`
  for inscribed orbs (this drawing is what `makeFaceLift` lifts), `'preview'`
  for wheelfield/overlap (lifting the field preview renders a different solid,
  `orb-views.ts:326-341`). The page captions from `relation` — honesty carried
  in data.
- **Bare base solid** (design doc §3.4): new `baseSolidCells(base)` in core —
  base faces as `SphericalCell[]`, reusing `projectSphericalCells`; no new
  projector. Ships as `frames[0]` with `kind:'base'`, unstyled like all stage
  frames, same viewBox. Works for all 14 (every orb has `orb3d.base`); caption
  is family-driven ("copied onto each face" vs "wheels anchor at its vertices").
- Deliberately *not* built: a `t`-parameterized flat→sphere wrap morph — new
  geometry, no machinery to reuse; endpoints + tilt-in ship, morph recorded as
  future work.

### E. Gallery restyle (the "human surfaces" half of scope decision 1)

- `--format views` additionally writes styled display variants under
  `build/orb-views/<orb>/display/<view>.svg` — a *subdirectory*, so qiyas's
  top-level view discovery and gt pairing never see them (pattern proven by
  `ribbons/`). Instrument set at the top level: byte-identical, asserted.
- `build/orb_previews.py` `restyle()` rewritten structural, not literal: map
  any grayscale fill scaled by its luminance ratio into the gallery gold
  (preserving the Lambert modeling), map the stroke, keep the silhouette;
  `hero()` prefers `display/`, falls back to `ribbons/` when the top level has
  no views — which closes the Maclado9Overlap gallery hole in the same stroke.

### F. Maclado9Overlap first-class + family parameterization

- `writeTurntable` refactor: `projectSweepScene(...)` returns
  `{representation: 'cells'|'ribbons', scene}` — cell projection if the orb has
  one, else ribbon projection via `projectOrbRibbonScene` (same free
  `view.axis`), rendered by the matching renderer with full style. Used by both
  turntable and transition. Manifest gains `turntableRepresentation:
  'cells'|'ribbons'|null`. The "no projected cell view to sweep" message +
  its test flip **by design** to assert ribbon frames (`turntable-flag.test.ts`
  woven case); the null branch stays, exercised via fixture.
- **Task #14 resolved by deletion, not regeneration** — the engine *refuses* to
  produce those cell views by design (`orb-views.ts:334-341`); regeneration is
  impossible and their existence is the defect. `make orbs` deletes
  `build/orb-views/Maclado9Overlap/*.{svg,png,gt.json}` at top level; `ribbons/`
  is the complete view set (already what the CLI declares). bikar's sweep
  already scores it `cells: null, ribbons: score` — pins unaffected.
- Optional manifest key `weave: {strands, crossings} | null` read off
  `result.orbWeave`'s topology **only if honestly derivable** — else null and
  the page keeps the picture-count hedge. Feeds the "60 loops over 420
  crossings" beat.
- Family matrix (all derived, no orb names): projector pair from
  cell-projection-throws⇒ribbon; highlight key domain from `OrbStage.kind`;
  copy from frame-kind set + `flat.relation` + representation — "tile then
  repeat" / "tile, repeat, then thread" / "thread one loop at a time".

### G. Gates

- **`timelapse_gate.py`** (new, `.claude/gates/`, wired into `make validate` +
  pre-commit chain; design doc §9, task #17). Per orb dir: (1) manifest keys
  present; (2) one viewBox across `frames`+`transition`+`turntable` (`flat`
  exempt by schema); (3) terminal identity — `frames[last].kind=='complete'` and
  bytes equal the shipped instrument view (ribbons path for strand-only); (4)
  stage frames carry no `data-orb-style`/`data-orb-silhouette`; fills only from
  {defaults, highlight}; (5) junction identities transition[0]/transition[last];
  (6) every named file exists, no orphan SVGs, `sourceSha256` round-trips.
  `--self-test` mutates a fixture N ways and asserts each fires.
  **By-design failures, named:** (a) first run against the pre-#14 tree must
  FAIL check 3 on Maclado9Overlap — gate ships with that failure recorded, the
  deletion is the visible remediation commit; (b) a manifest from a stale
  pre-upgrade CLI dist must fail check 1 naming the missing keys.
- **`orb-breakdown-index`** (Makefile:269): required-key tuple grows to 10 —
  `+ flat, transition, turntableRepresentation` — same check, same failure
  message style.

## Execution order (branch→PR→merge each; never stacked)

**bikar PR 1** (~3–4 days): kernel `meanDot` + `baseSolidCells` (+tests) →
renderer `OrbViewStyle`/highlight (+**byte-stability snapshot test first**) →
CLI: complete/base/flat frames, highlight, `writeTransition`,
`projectSweepScene` ribbon turntable, display variants, manifest keys →
`turntable-flag.test.ts` flip + transition tests → `breakdown-main.ts` page:
prelude (flat→base), transition playback, family copy, defensive reads
(`?? []` — old manifests still render) → e2e fixtures (cell family + strand-only
variant). Gate for merge: full bikar suite; orb-composites pins must not move.

**3d-models PR 2** (~2 days, after PR 1 merges; bump `build/bikar-ref.txt`):
`orb_previews.py` structural restyle + display/ribbons fallback → Makefile
key-tuple + stale-view deletion in `orbs` → `make orbs` regeneration →
`timelapse_gate.py` + wiring + self-test → doc amendments
(`orb-construction-timelapse-design.md` §3.4 built, §4.1 restated on the
complete frame, §9 built with the measured first-run failure; decisions-log
entry; close tasks #14, #17, #35).

## Verification

1. bikar: snapshot test proves styleless output byte-identical to today (the
   qiyas shield); junction byte-identities asserted in CLI tests; e2e proves
   the page renders both family fixtures and old manifests.
2. 3d-models: after `make orbs`, `git status` on `build/orb-views` shows ONLY
   the intended changes (new `display/` subdirs; Maclado9Overlap top-level
   deletion) — every instrument file byte-identical, checked by md5 before
   commit.
3. `make validate` green with the new gate; gate `--self-test` passes; the two
   by-design failures demonstrated in the PR description (Overlap terminal-
   identity failure pre-deletion; stale-manifest key failure via fixture).
4. Optional belt-and-braces (docker precondition, else NOT VERIFIED, stated):
   run the qiyas sweep — composites must read exactly the pinned values, since
   the instrument never changed.
5. Eyes on the result: open `breakdown.html?orb=` for StarOrb (cell), WeaveOrb
   (cell+strand), Maclado9Overlap (strand-only) — each tells the five beats;
   the spin reads as a turning sphere.

## Deliberately NOT in v1

Ghosted back hemisphere (future `OrbViewStyle` member); flat→sphere wrap morph;
per-strand highlight on strand *stages*; qiyas detector changes or composite
re-records; shading non-hex author fills (left unshaded, documented); mesh-
render timelapse (§5.4 stays deferred-not-rejected); per-orb special cases
anywhere.
