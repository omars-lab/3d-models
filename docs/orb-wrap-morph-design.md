# Flat→sphere wrap morph for the breakdown page

**Status:** v0 — **designed, not built.** The owner chose "design doc first, then
build" ([D-049 §2](decisions-log.md)); this is the design. Nothing in bikar or in
this repo's gate has changed yet. Build order is section 6.
**Grounded by:** [`research/orb-wrap-morph-grounding.md`](research/orb-wrap-morph-grounding.md)
— every engine fact below is a row of its §A (cited as A1…A8), every count a row of
§B or §D, and every outside source a row of §C marked **fetched**. Sources that
could not be fetched are listed there and not cited here.
**Parent:** [`orb-construction-timelapse-design.md`](orb-construction-timelapse-design.md),
whose teach-construction rework deliberately left this morph out ("no machinery to
reuse"). This document is the reuse it did not find.

## 1. What this is, and the one fact that decided it

The breakdown page tells a newcomer that the flat drawing is *copied onto every face
of a solid and bent onto the sphere* (A8, the standfirst). The frames draw the
opposite order: every stage frame, from `element 1` on, is already on the sphere,
and the page's own footer admits it — "there is no frame that shows the flat drawing
bending onto the sphere" (A8). The teach-construction rework shipped the flat
drawing and the bare solid as endpoints and left the bend as future work because it
believed a morph was new geometry.

It is not. The fact that decided this design is A1: for every pattern vertex,
`projectFacePolygon` already computes **both** ends of the bend. `flat` is the
vertex lifted onto the face's chord plane; `dir` is `flat` normalised onto the
sphere; the orb's declared projection picks which one is drawn, and the front-cap
cull reads `dir` either way. The two points are collinear with the centre, so the
travel between them is a straight line along the radius, and a frame at any point
of the bend is

    world = R · ( (1 − t)·flat + t·dir ),   t ∈ [0, 1]

with `t = 0` the faceted drawing and `t = 1` the spherical one. The task that
opened this work called the travel a *slerp*. Slerp is bikar's tool for the camera
tilt and the scaffold arcs (A5), and between collinear endpoints it reduces to
ordinary linear interpolation (C1, the degenerate case). So "slerp" was not wrong,
it was empty: the honest name is a radial lerp, and it needs no new geometry.

**Transfer condition, stated.** The one outside precedent cited, Yang et al. (C3),
morphed between a globe and a flat map by linearly interpolating the 3D positions
of the same points in two renderings, with the user controlling the progress. That
*mechanism* transfers here because the situation is the same: one set of points,
two positions each, both already computed. Their paper makes no claim that the
morph helps comprehension — it names evaluation as future work — and this document
makes none either. The claim here is narrower and checkable: after the change, the
frames draw the order the copy promises.

### 1.1 What the picture will actually show

The camera is orthographic (§D of the research), so a radial move at angle θ off
the view axis shows in the picture as that move times sin θ: nothing on the face
under the camera, most near the limb. How far a face centre moves is `1 − r`, the
base solid's inradius over its circumradius, and it differs by base (§D table):

| base | lifted orbs | face-centre travel | in-picture shift at 60° off axis |
|---|---|---|---|
| tetrahedron | StarTetraOrb | 0.667·R | 0.577·R |
| cube, octahedron | RosetteCubeOrb, StarCubeOrb, StarOctaOrb | 0.423·R | 0.366·R |
| dodecahedron, icosahedron | the other seven | 0.205·R | 0.178·R |

So the morph is plainly visible on every lifted orb, dramatic on the tetrahedron,
and near-invisible on the one face the camera looks straight down at. That last
point is a property of the camera, not a defect of the morph: the stage view is
chosen down a vertex (`vertex-3/4/5`, §B), so no face is exactly under the camera
and every face shows some of the bend. The silhouette does not change at all — the
solid's vertices are on the sphere at both ends — which is the visual statement the
morph makes: *the corners were always on the ball; the bend is what happens in
between.*

### 1.2 Non-goals

- Changing the projection. bikar's `spherical` is normalisation, the gnomonic map,
  with the corner-bunching antitile describes (C2). The morph draws that map's two
  ends; a better map is a different document.
- A morph on the woven family's ribbons, or on any orb born on the sphere (§2).
- A comprehension claim. None is available (C3) and none is made.

## 2. Scope, stated rather than assumed

The eleven `flat.relation: 'lifted'` orbs are in (§B). Each declares `project
spherical` (A4) and each has a face lift, so each has both ends of the bend.

Out, with the reason, and each gets `morph: null` in the manifest so the page and
the gate can tell "no morph" from "manifest from an older build" (T1):

- The three `flat.relation: 'preview'` orbs (Maclado9, Maclado9Weave,
  Maclado9Overlap). The language reference says it for wheelfields: "the field is
  born on the sphere, there is no flat" (A4). There is no `flat` end to start from.
- Any orb that declares `project faceted`. Its shipped drawing *is* the `t = 0` end;
  a morph would carry it to a projection it did not declare (A3). None of the
  fourteen declares it today (A4), so this is a rule for the fifteenth, not a case.
- The strand stages of the four cell+strand orbs. Their ribbons come from the
  ribbon projector, not from the face lift, so they have no faceted end; and the
  cells `complete` frame precedes the first strand stage in every such sequence
  (§B), so the morph sits in the cell half and the strand half is unchanged. What the woven family shows, then, is: tile faceted,
  inflate, then thread on the sphere — which is the construction order.

## 3. The design

### 3.1 Stages are drawn faceted; the morph inflates them

Today every stage frame draws at the orb's declared projection (A3), so the bend
happens before frame 1. The change: stage frames (`base`, `element`, `repeat`) draw
at `t = 0`, the faceted end; a run of `morph` frames carries the finished tiling
from `t = 0` to `t = 1`; the `complete` frame is untouched, still the shipped view
repainted and not redrawn, so T3 holds exactly as written (A7).

The `base` frame is the polyhedron's own faces as cells, and those are already flat
polygons; drawing it at `t = 0` changes nothing but makes the invariant uniform. It
also tightens T7 for free: a cell on the chord plane lies *inside* the solid the
scaffold draws, where today's spherical cells lie on the sphere and pass only by the
containment slack (A7).

Sequences, per family:

| family | frames, in order |
|---|---|
| cells (8 lifted orbs) | base → element → repeat → **morph** → complete |
| cells + strands (3 lifted orbs) | base → element → repeat → **morph** → complete (cells) → strand → complete (ribbons) |
| preview and strand-only (3 orbs) | unchanged; `morph: null` |

### 3.2 The kernel parameter

`projectFacePolygon` gains one number, the blend `t`, in place of the two-way
`projection` switch it reads today: `'faceted'` is `t = 0`, `'spherical'` is
`t = 1`, and the call sites that pass `projection: orb.projection` (A3) keep
passing the word — the CLI maps the word to the number. The DSL is untouched; no
`.bkr` learns a new keyword. Two properties the kernel tests pin:

- At `t = 0` and `t = 1` the output is byte-identical to today's `faceted` and
  `spherical` drawings respectively. This is the test that protects qiyas, the
  gallery previews and the pinned composites: the instrument set never sees a
  fractional `t`.
- The cull reads `dir` (A1), which does not depend on `t`, so **the set of
  polygons drawn is the same at every `t`**. A morph frame has exactly the polygon
  count of the last `repeat` frame and of the cells `complete` frame — and those two
  already agree on all eleven lifted orbs (§D: 42, 21, 21, 84, 18, 36, 16, 55, 6, 18,
  40). Only vertex positions move.

### 3.3 Frames, files, style

- Files `<orb>.<view>.morph.NNN.svg`, kind `morph`, on the stage view and the stage
  viewBox (T2). Frame `NNN` draws at `t = NNN / (N − 1)`.
- `N` is the orb's transition frame count (§B: 3, 6 or 7), reused so tilt and bend
  run at the same tempo per orb. That is a reuse, not a default: the number is
  already the orb's, chosen by the camera arc, and the doc that chose it owns it. If
  a bend wants its own tempo that is section 7's first question.
- Style is `STAGE_STYLE` with the scaffold on, like every unfinished frame (A6,
  T6); no highlight fill, because nothing is being placed; the front-cap cull as
  today.
- Manifest: a top-level `morph: { frames: [{file, index, t, polygons}] } | null`,
  beside `transition` and shaped like it, so the page reads it with the same
  defensive `?? []` that lets old manifests still render.

### 3.4 Two junctions and one invariant, each a byte check

The morph is bracketed by frames that already exist, which is what makes it
checkable rather than merely plausible.

- **J1 — the morph starts where the tiling ended.** `morph[0]` is the last `repeat`
  frame with the highlight fill `#c9782e` replaced by the placed fill `#8a8a8a`
  (A6): same polygons, same `t = 0`, nothing placed. The check performs that one
  substitution on the `repeat` frame and demands byte equality — and demands that
  the substitution *changed something*, because a `repeat` frame with no highlight
  would pass the identity while proving nothing.
- **J2 — the morph ends on the finished orb.** `morph[N−1]` with the scaffold
  elements stripped is the cells `complete` frame, byte for byte: `t = 1` is the
  spherical drawing (§3.2), and `complete` differs from a stage only by the scaffold
  (A6). The check strips and demands equality — and demands the strip *removed
  something*, for the same reason.
- **N — the count never moves.** Every `morph` frame's polygon count equals the
  last `repeat` frame's. This is the cull invariance of §3.2 made into a rule, and
  it is the rule that would catch a `t` leaking into the cull.

### 3.5 The page

- The `morph` kind gets a caption in `breakdown-copy.ts` beside the others: for the
  cell family, "the copies bend onto the sphere"; the woven family adds "…before
  the ribbons are threaded over them". Derived from frame kind and `flat.relation`
  like every caption there, no orb names.
- The footer's "there is no frame that shows the flat drawing bending" (A8) stays
  **only** on pages whose manifest carries `morph: null`, and says why in the family's
  words (born on the sphere / threaded, not bent). On a lifted orb it is deleted,
  not softened.

### 3.6 The gate

[`../.claude/gates/timelapse_gate.py`](../.claude/gates/timelapse_gate.py) grows by
one kind and two rules; T1–T7 apply to `morph` frames unchanged.

- `STAGE_KINDS` and `CONTAINED_KINDS` gain `morph`; `STAGE_FILLS` is unchanged (a
  morph frame uses only the placed fill and the ground).
- **The junction rule** (provisionally **T8**; a containment rule proposed since
  the gate shipped — tie the drawn outline to the solid the manifest declares — is
  queued and may take that number first, in which case this is T9 and the next is
  T10; the gate assigns numbers at build time) is J1 + J2 of §3.4.
- **The count rule** (provisionally **T9**) is N of §3.4.
- `--self-test` gains the by-design failures for each: a morph run whose first
  frame is the `repeat` frame *with* the highlight (J1 fails on the identity), a
  `repeat` frame with no highlight at all (J1 fails on "changed nothing"), a last
  morph frame still wearing the scaffold (J2 fails), a `complete` frame handed in as
  `morph[N−1]` (J2 fails on "removed nothing"), and a morph frame with one polygon
  fewer (N fails).

**Validator:** the morph run is a bend and nothing else — J1, J2 and N together, on
every lifted orb, on every `make orbs`.
PASS: StarOrb — `morph.000` equals `repeat.010` after one `#c9782e`→`#8a8a8a`
substitution that touched at least one element; `morph.005` minus its scaffold
equals `complete.000`; all six morph frames report 55 polygons.
FAIL: a build where `t` reached the cull — `morph.003` reports 54 polygons because
one polygon near the cap edge culled differently at `t = 0.6`; N fires, names the
frame and the two counts. And the substitution case: a `repeat` frame written with
no highlight passes J1's byte identity and fails its "changed nothing" clause.

## 4. Options

Each says what it verifies; the cheapest is not the default, and "do nothing" is
not neutral.

### 4.1 Option 0 — do nothing

Keep the page as it is: copy says bend-after-copy, frames show copy-after-bend, and
the footer admits it.

**What it verifies:** nothing new. It keeps a sentence on every page that says the
page does not do what its standfirst says. Rejected — the D-049 decision was to
build this, design first.

### 4.2 Option A — morph in picture space (rejected)

Interpolate the 2D SVG paths of the flat drawing into the 2D paths of the shipped
view, the way SVG path-morphing libraries do (C7, description only).

**What it verifies:** that two pictures can be blended. It cannot verify anything
about the construction, because the flat drawing is one repeat unit in the picture
plane and the shipped view is twenty copies on a sphere — there is no point
correspondence, and a library would guess one (C7). The junction identities of
§3.4 are unavailable: a picture-space frame is not produced by the projector, so no
byte check ties it to a real frame. It would also draw a bend the geometry does not
perform (A2: the flat end is the pattern *on the face plane*, not in the picture
plane). Rejected.

### 4.3 Option B — radial inflation with faceted stages (recommended)

Section 3. The stages draw the faceted end, the morph inflates the finished tiling
to the sphere, `complete` is untouched.

**What it verifies:** that every morph frame is a projector output at a known `t`
(no hand-made frame), that the run starts on the last thing placed and ends on the
shipped drawing (two byte identities), and that the bend moves vertices only (the
count). It verifies the copy's order against the frames' order, which is the
defect. Cost: one kernel parameter, one CLI writer, one caption, two gate rules.
Its risk is that faceted stages look different from today's stages on every lifted
orb — they are meant to; that difference *is* the bend being shown — and the
build must re-render all fourteen breakdowns, which `make orbs` already does.

### 4.4 Option C — spherical stages as today, then deflate-and-inflate (rejected)

Keep every stage on the sphere and append a morph that snaps back to faceted and
inflates again.

**What it verifies:** the same identities as B at the inflating end. But its first
frame is a snap the construction never performs, drawn to undo the projection that
the stages already applied, and its J1 would have to compare against a *deflated*
`repeat` frame that exists nowhere else. It is B with a lie prepended. Rejected.

### 4.5 Option D — bend one face first, then the rest (deferred)

Morph the highlighted `element` stage's single face from `t = 0` to `t = 1` before
the repeats, so a newcomer sees one copy land before twenty do.

**What it verifies:** the same per-frame facts as B, on a subset. Deferred, not
rejected: it needs a per-face `t` rather than one `t` per frame, and the page would
then show the same face bending twice (once alone, once with the tiling) unless
the repeat stages draw at `t = 1` for placed faces and `t = 0` for the new one —
which is a second design. Recorded as section 7's second question.

### 4.6 Recommendation

Option B. It is the only one whose every frame is a projector output and whose
ends are byte-checked against frames the gate already trusts.

## 5. Validators

**Validator:** the endpoints are today's drawings. At `t = 0` the kernel's output is
byte-identical to the `faceted` projection and at `t = 1` to the `spherical` one,
for every lifted orb and every view — the instrument set is unchanged by the
parameter's existence.
PASS: `build/orb-views/StarOrb/vertex-5.svg` after the bikar PR has the md5 it had
before; qiyas's pinned composites read exactly the pinned values.
FAIL: a kernel that rounds `t` to a float and drifts `1.0` by one ulp writes
`vertex-5.svg` with a coordinate differing in the last digit; the snapshot test
names the file and the byte.

**Validator:** no polygon appears or vanishes during the bend. The count of every
`morph` frame equals the last `repeat` frame's and the cells `complete` frame's.
PASS: all eleven lifted orbs, counts as §D lists them, on every morph frame.
FAIL: a projector that culls on `lerp(flat, dir, t)` instead of `dir` drops a
cap-edge polygon at mid-bend; the rule reports the frame, the expected 55 and the
found 54.

**Validator:** the page's footer hedge is honest per orb. It appears when and only
when `manifest.morph` is `null`.
PASS: Maclado9Overlap's page carries the hedge in the strand-only family's words;
StarOrb's page has no such sentence.
FAIL: a page template that keeps the hedge unconditionally after the build — the
e2e fixture for the cell family asserts the sentence's absence and fails.

## 6. Build plan

Two pull requests, never stacked, in this order.

**bikar PR — the frames.**

1. Kernel: `t` in `projectFacePolygon`; tests for the two byte identities
   (`t = 0` ≡ faceted, `t = 1` ≡ spherical) and for polygon-set invariance across a
   sweep of `t`.
2. CLI: stage frames at `t = 0`; `writeMorph` after the last `repeat`, `N` from the
   transition count, `STAGE_STYLE` with scaffold; manifest key `morph`; tests for
   J1, J2 and N on the CLI's own output, including the "changed nothing" and
   "removed nothing" clauses.
3. Page: caption for `morph`; footer hedge conditional on `morph === null`; e2e
   fixtures for a lifted orb and a preview orb.
4. Merge gate: the full suite; the orb-composite pins must not move (§5, first
   validator).

**3d-models PR — the gate and the record.**

1. Bump `build/bikar-ref.txt`; `make orbs`; confirm by md5 that no file under
   `build/orb-views/` at the top level changed.
2. Gate: `morph` in `STAGE_KINDS` and `CONTAINED_KINDS`; the junction and count
   rules; the self-test failures of §3.6.
3. Docs: this document's status to **built** with the PR numbers; the parent
   document's status line; plan row; a shipped-record bullet.

## 7. Open questions

1. **Tempo.** The morph reuses the tilt's frame count. If the bend reads too fast
   on the tetrahedron (0.667·R of travel in three frames) the answer is a count
   derived from travel — `ceil(travel / step)` for a step the camera arc already
   implies — not a per-orb number.
2. **One face first** (Option D). Needs a per-face `t`.
3. **Sub-triangle faceting.** If a future orb's face lift subdivides the face
   (geodesic style), `flat` lies on several planes per face and the `t = 0` end is
   a finer polyhedron than `base` draws; T7's containment then needs the finer
   outline. No orb does this today (A2: one plane per face).
4. **Containment slack at the cap edge.** With faceted stages inside the solid, the
   slack T7 carries may be reducible; measure it on the built frames before
   touching it.
