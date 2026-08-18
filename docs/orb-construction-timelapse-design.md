# Orb construction timelapse

**Status:** DRAFT — nothing implemented. Design only.
**Grounded by:** [`research/orb-stage-decomposition-measurement.md`](research/orb-stage-decomposition-measurement.md)
— every number in this document is from that file, measured 2026-08-18 against
bikar `e0a81cc` and 3d-models `50bac8d`. Where that file marks a figure
NOT VERIFIED, this document marks it too.

## 1. What this is, and the one fact that decided it

Today an orb is one finished picture on a card in [`../index.html`](../index.html):
a render, a sentence, three chips, three links to Source, STL and the Lab.
There is no page per orb and no view of how the thing is *made*.

This document designs a per-orb construction timelapse — a dense sequence of
images under a fixed camera, ordered from the simplest piece outward, arriving
at the shipped orb on the last frame, with prose derived from the source rather
than typed.

One investigation was supposed to decide the whole design: **is the
construction staged internally, or does it arrive as one expression?** The
answer is *one expression*, and it is not close. In `packages/core/src/dsl/evaluator.ts`,
`evaluateOrbDecl` reaches solidification in a single call — `solidifyLattice(base, voids, {...})` —
with the woven and wheelfield paths doing the same through `weaveLattice(...)`
and `solidifyMacladoField(...)`. No stage boundary is exposed and no partial
result is retained.

That fact would have killed the feature if the pipeline ended there. It does
not, and the reason is the finding this design rests on: **the view pipeline is
already tagged per element.** `projectOrbView` in `packages/core/src/kernel3d/orb-views.ts`
stamps every polygon it emits with `baseFaceIndex` and `patternFaceIndex`; the
ribbon path stamps `strandId`. So a construction stage is a pure filter over an
array that already exists:

```js
const subset = { ...scene, polygons: scene.polygons.filter(p => p.baseFaceIndex === firstBase) };
renderOrbViewSVG({ scene: subset, faceColors: r.faceColors, faceClasses: r.faceClasses });
```

That is the whole mechanism, and it requires **no change to the geometry
engine**. The engine does not need to be staged, because the *drawing* is
already indexed along the axes a stage would cut.

A second tag turned up unlooked-for and matters more for the prose than the
frame counts do: every polygon carries a `source` set naming the DSL constructs
that produced it — `'tri'` for a `polygon tri [...]` declaration, `'C1:every:2:#0'`
for a `connect every 2 on C1` statement, `'layer:0'` for the layer. A caption
can name the construction element without a human typing it.

### 1.1 Relation to the derivation worksheet

[`derivation-worksheet-design.md`](derivation-worksheet-design.md) already
designs a static SVG derivation sheet for the **2D** pattern pipeline. This
document is its 3D sibling and deliberately does not duplicate it: that one
explains how a flat pattern is derived, this one how an orb is assembled from a
pattern already derived. Two of its scope-outs are load-bearing here and are
answered rather than inherited — see section 7.2 for the scrubber it deferred,
and section 4.2 for the 3D-solidification argument it promised and never wrote.

### 1.2 Non-goals

- **No 3D mesh timelapse in v1.** The last two stages the brief imagined —
  fusion across edges, then the final solid — cannot be drawn by this
  machinery at all. Section 4.2 says why.
- **No new DSL surface.** Section 6 gives the verdict and the evidence.
- **Not a replacement for the gallery card.** The card stays; the timelapse is
  what its "how it is made" link opens.

## 2. Scope, stated rather than assumed

Designed for: **the 14 `.bkr` files in bikar's `patterns/Orbs/` as of `e0a81cc`.**
All 14 were enumerated by running the proposed filter over each; none was
extrapolated from a neighbour. Where this document says "all 14" it means those
14 and makes no wider claim.

Not designed for, and what would change:

- **qiyas's flat showcase fixtures** are PNGs with hand-authored sidecar JSON,
  not compiled geometry. There is no scene array to filter, so none of section 3
  transfers and a showcase timelapse would be a different design with a
  different mechanism.
- **The Lego bricks** compile through the LDraw path to meshes rather than to an
  orb view scene, so they land in section 4.2's mesh problem rather than here.

Widening scope to either does not extend this design; it starts a second one.

## 3. Stage decomposition, per family, all 14 enumerated

The 14 orbs split by two independent properties read from the compiled result
rather than inferred from filenames: **surface** (`inscribed`, 11 orbs;
`wheelfield`, 3) and **family** (`lattice`, 9; `weave`, 5).

### 3.1 Inscribed orbs — a two-axis grid

For the 11 inscribed orbs, `(baseFaceIndex, patternFaceIndex)` is a genuine
grid: pattern element *p* on base face *b*. Both orderings the brief cared about
are free filters over it.

- **The simplicity axis** — hold `baseFaceIndex` at the first visible base face
  and admit `patternFaceIndex` values one at a time. Frame 1 is one strut, one
  hexagram arm, or one petal. This is *not* the engine's loop order; the
  engine's inner loop produces all of them at once. It is a re-sort of an
  array, and it costs nothing.
- **The repetition axis** — admit whole base faces one at a time, each carrying
  its complete pattern. This *is* the engine's outer loop order.

Both orderings are available for all 11, so the "simplicity versus pipeline
order" tension the brief anticipated **does not arise** here.

### 3.2 Wheelfield orbs — where the semantic ordering costs something

The three Maclado orbs are the family the brief warned about, and they are
different — but less different than an earlier draft of this document claimed,
and the correction is worth stating because it simplifies the build.

`projectSphericalCells` flattens `patternFaceIndex` to a running cell index, so
the grid of section 3.1 is not there in the same form. But **grouping is still
free**: `unit === baseFaceIndex` on every visible cell, with 0 mismatches
measured across Maclado-9. Wheel-by-wheel frames need nothing but the projected
scene.

What is *not* free is the semantic ordering *within* a wheel. That needs a
second array — `r.orbCells[patternFaceIndex]` yields `{unit, kind, index}` —
and gives the simplicity ordering a different shape: **spike, then wheel, then
field**, ordered by `kind` and then `index`. Maclado-9's 392 cells are
`{core: 20, triangle: 180, petal: 180, filler: 12}`, and within one wheel the
order runs `core:0, triangle:0, petal:0, triangle:1, petal:1, …` out to
`triangle:8, petal:8` — nine spikes, which is what the name says, and 19 cells
per wheel, which is exactly the `elements` count the generic filter reports.

**So the two decompositions agree.** The generic filter and the semantic wheel
structure produce the same 19, and the extra code buys naming and ordering, not
grouping. Budget for one generator plus a naming pass, not two generators.

The 12 `filler` cells are the honest wrinkle. They belong to no wheel — they are
what the field needs to close, and they are why 392 is not a multiple of 19.
They are excluded from the wheel-by-wheel frames and admitted only at the final
frame.

### 3.3 Measured frame counts, all 14

One hero symmetry view each. Two counts, because they differ and the difference
is load-bearing: **emitted** is `elements + repeats + strands`, the frames the
filter actually produces; **notional** adds the base-polyhedron frame section
3.4 cannot build yet.

| Orb | surface | elements | repeats | strands | emitted | notional |
|---|---|---|---|---|---|---|
| Star-Tetra-Orb | inscribed | 2 | 3 | — | 5 | 6 |
| Star-Octa-Orb | inscribed | 4 | 4 | — | 8 | 9 |
| Rosette-Cube-Orb | inscribed | 7 | 3 | — | 10 | 11 |
| Hankin-Orb | inscribed | 6 | 6 | — | 12 | 13 |
| Star-Cube-Orb | inscribed | 12 | 3 | — | 15 | 16 |
| Dodeca-Orb | inscribed | 11 | 6 | — | 17 | 18 |
| Rosette-Weave-Orb | inscribed | 6 | 3 | 9 | 18 | 19 |
| Weave-Dodeca-Orb | inscribed | 6 | 3 | 9 | 18 | 19 |
| Star-Orb | inscribed | 10 | 10 | — | 20 | 21 |
| Rosette-Orb | inscribed | 21 | 6 | — | 27 | 28 |
| Maclado-9 | wheelfield | 19 | 13 | — | 32 | 33 |
| Weave-Orb | inscribed | 7 | 10 | 15 | 32 | 33 |
| Maclado-9-Overlap | wheelfield | — | — | 30 | 30 | 30 |
| Maclado-9-Weave | wheelfield | 19 | 13 | 26 | 58 | 59 |

**302 frames emitted across all 14; 315 notional.** Every number is a count
taken from the compiled scene. Nobody chose them.

> **Correction (2026-08-18).** This section shipped one day earlier with a
> single `frames` column totalling **329**, under the rule
> `1 base + elements + repeats + 1 final (+ strands)`. Writing the frames out to
> disk rather than hashing them produced 302, and the 27-frame gap resolves
> exactly: 13 base frames section 3.4 cannot build, and **14 `final` frames that
> were a double count.** Section 4.1's own validator asserts the last cumulative
> frame is byte-identical to the full render; re-measured today it is —
> 13 IDENTICAL, 1 orb with no cell scene, 0 differing — so the `+ 1 final` term
> counted a frame this document had already proved was the frame before it. The
> table contradicted a section two doors down, and it survived because nobody
> wrote the frames out.
> ([research](research/orb-stage-decomposition-measurement.md) section 6a,
> CORRECTION 6.)

`elements` is counted on the first visible base face only, so it is a per-unit
count for one representative unit — not a minimum, not a mean. Faces nearer the
cap rim are clipped and carry fewer polygons.

### 3.4 The base-polyhedron frame is not free

Frame 0 is the bare base solid, and an earlier draft called it free. It is not,
and this is the one place the design needs a change outside itself.
`projectSphericalCells` is exported from `packages/core/src/kernel3d/index.ts`,
but `packages/core/package.json` declares exactly one export path and `dist/`
carries only the bundle, so the function is reachable from code **inside** core
and not from an external consumer.

Two ways out, both cheap: widen the export, or place the stage generator inside
core. Section 7 takes the second, because the generator wants the scene types
anyway. Either way it is a build-plan line item rather than a filter.

### 3.5 Ribbon stages, and the front-cap hedge

Woven orbs get a second sequence keyed on `strandId` — one loop threaded at a
time. Maclado-9-Overlap has *only* this sequence: it draws no cells at all, by
design, and the engine says so in an error message rather than returning
something plausible.

**A single symmetry view shows only the front cap.** Maclado-9-Overlap yields
30 visible strands on its hero view and 32 on `edge-2`; its own `.bkr` header
speaks of 60 loops. None of these is "the" strand count — the first two are
picture counts and the third is a solid count. Any caption that quotes a total
beside a picture is describing something the reader cannot see, which is why
section 8's criterion 8 makes the hedge mandatory rather than optional.

## 4. Camera, materials, and what cannot be drawn

### 4.1 Invariance is free, under a condition worth writing down

`renderOrbViewSVG` in `packages/core/src/render/orb-view-renderer.ts` carries
its own docstring on the point: the viewBox is the fixed sphere disc plus
padding, identical across the three views of one orb. It is computed from
`radiusMm` and never reads content bounds, so removing 90% of the polygons
cannot move it.

There is no lighting to hold still either. The pipeline is flat-shaded SVG, not
a lit 3D render: two colour literals, recoloured on the way to the gallery by
[`../build/orb_previews.py`](../build/orb_previews.py).

This document sets **no default of its own** — no padding value, no scale, no
frame-count constant. Every such value is inherited unchanged from a renderer
this design does not modify, and marking an inherited constant `**Default:**`
would claim a decision that was not made here. There is house precedent for
declining the marker on exactly these grounds at
[`lego-lab-design.md`](lego-lab-design.md), where a copy limit is left unmarked
"because no measurement settles it and pretending otherwise would put a number
in Appendix B that no coupon can close." The same reasoning applies in the
other direction: a number someone else already settled is not this document's
to declare.

**The transfer condition, stated because the invariance is not unconditional:**
it holds *only while every frame is the same orb at the same declared radius*.
The viewBox is a function of `radiusMm`. A stage sequence that swept `radius`
would break camera invariance in the one way that matters — silently, with
every frame still looking plausible. That risk lives in section 5's Option D,
and it is why Option D is scoped to non-radius parameters.

**Validator:** every frame in a sequence carries a byte-identical `viewBox`
attribute, and the last cumulative frame is byte-identical to the orb's shipped
view SVG.

PASS: all 14 orbs, 302 cumulative frames, one hero view each — exactly one
distinct `viewBox` string per orb, and every terminal frame byte-identical to
the unfiltered render. Star-Orb's pair is `c575552949e9` against
`c575552949e9`; the other thirteen shas are in the research file.

FAIL: Maclado-9-Overlap's shipped artifacts, and this is the hard case because
it is already true. `build/orb-views/Maclado9Overlap/` holds three cell SVGs,
three PNGs and three ground-truth files dated 2026-08-15, and the engine at
`e0a81cc` refuses to produce cell views for that orb at all — `projectOrbViewScene`
throws with a message explaining that its rims cross so the field cells are not
its surface. No ribbon directory exists anywhere under `build/`. So terminal
identity is **already false today** for this orb, before any timelapse exists,
and nothing in either repo detects it. This is the case an aggregate would
hide: 13 orbs passing and one silently comparing against an artifact from a
different engine version averages to "fine". The validator must be per-orb, and
it must fail here on its first run.

### 4.2 What SVG cannot show — the debt this repays

`struts width … depth …`, `project spherical` and `pierce voids` have **no
effect on the view representation**. Star-Orb declares no `pierce voids` and
Star-Octa-Orb does; both render identical-in-kind cell views. The view path
draws the pattern's cells and ribbons, not the solid built from them.

Therefore the brief's fourth and fifth stages — fusion across edges, then the
final solid — **cannot be drawn by this machinery**, and no amount of filtering
will make them appear. The honest sequence ends at "the pattern, complete, on
the sphere", and the jump from there to the shipped STL is exactly the jump the
timelapse does not show.

This is the argument [`derivation-worksheet-design.md`](derivation-worksheet-design.md)
promised twice at a `§6.3` it never wrote — the reference dangles, its section 6
has no subsections, and it is not a typo for the `§2.6.3` that file cites
elsewhere, since that one is about tile blocks while both `§6.3` citations sit
in explicit 3D-solidification context. Stated plainly here instead: **2D
derivation is filterable because the drawing is the artifact; 3D solidification
is not, because the drawing and the artifact are different objects and only the
drawing is indexed.** Option C is the only route to those two stages, and it
buys them by giving up byte-identity.

## 5. Options

Per [`../CLAUDE.md`](../CLAUDE.md)'s robustness-over-ease rule, the cheapest
option is not the default and "do nothing" is not neutral. Each says what it
verifies.

### 5.1 Option 0 — do nothing

**What it verifies:** nothing, and that is the cost rather than the saving. The
Maclado-9-Overlap staleness in section 4.1 is currently undetected by anything
in either repo, and was found only because this investigation ran the current
engine against the shipped output. Declining the feature also declines the
detector, and the divergence stays invisible until someone opens the orb and
wonders why it looks wrong.

### 5.2 Option A — hand-authored frame lists (cheapest, rejected)

A JSON sidecar per orb naming its stages and captions.

**What it verifies:** that a human read the orb. Nothing else. It cannot verify
that frame 3 corresponds to anything the `.bkr` declares, and cannot notice when
the geometry changes underneath it. It reproduces exactly the failure the brief
named — a hand-written paragraph per orb per stage.

The qiyas showcase is genuinely the precedent here, and the precedent is the
warning: its runner derives structure, scores and pages from data, while
`demonstrates`, `title` and `category` come from a hand-authored sidecar. The
half of qiyas that generates transfers; the half that describes does not.
Rejected for the 14 orbs. Named honestly as the *only* option if scope widens to
qiyas's flat fixtures, which have no compiled scene to filter.

### 5.3 Option B — derived filter timelapse (recommended)

Generate every frame as a filter over the compiled scene, ordered by section 3's
axes, rendered through the existing SVG renderer. No engine change. The frame
list is a consequence of the geometry, not an input.

**What it verifies:** that the sequence and the geometry cannot disagree,
because the sequence *is* the geometry — a frame asserting a stage the `.bkr`
does not declare is not merely wrong, it is unconstructible. It verifies the
final frame against the shipped render byte-for-byte, which catches section
4.1's staleness class, and verifies camera invariance structurally rather than
by inspection.

### 5.4 Option C — mesh render timelapse (deferred, not rejected)

Render each stage as a lit 3D mesh through the LDraw thumbnail path.

**What it verifies:** the actual solid — struts, piercing, fusion, the things
section 4.2 says SVG cannot show. It is the only option that can draw the last
two stages the brief imagined.

**What it costs:** the byte-identity guarantee, permanently. That path already
concedes this, pairing a hard counts gate with a soft, tolerant, GPU-dependent
pixel gate. A mesh timelapse can never assert "the final frame equals the
shipped render"; only "within tolerance on this machine". Worth revisiting when
someone wants to *see* a strut, not before.

### 5.5 Option D — parameter-sweep timelapse (opt-in second axis)

Where an orb has a parameter whose sweep *is* its narrative, recompile across
the declared range and use the sweep as a stage axis.

**What it verifies:** that the declared range is real. This is the option that
found something. Sweeping Maclado-9-Overlap's `overlap` outside its declared
`1.15..1.25` shows the feasible set is **two disjoint bands** — `[1.08, 1.26]`
and `[1.38, 1.60]` — separated by a dead band at `[1.28, 1.36]` where 30 of 30
adjacent pairs refuse to weld. The second band is a *different weave regime*:
750 ribbon polygons against band one's 516, 270 `over` passes against 192.
Feasibility is not an interval because weld-node spacing is not monotonic in
the ratio — the kernel reports nodes 0.76 mm apart at 1.05 and 0.39 mm apart at
1.30, both closer than the 1.2 mm strut width. The `.bkr` header's "past ~1.25"
reads as a single ceiling; the geometry has two floors and two ceilings.

Two limits, both stated in the research file and repeated here because they
bound the claim: this is a **compile-time** result — no STL, no qiyas score, so
nothing says the second band is a legitimate solid rather than one that survives
the welder — and the sweep steps 0.02, so each band edge is located only to
within 0.02.

**Scoped deliberately:** never sweep `radius`, for section 4.1's reason. And the
sweep cannot tell the orb's own origin story — at `overlap = 1` the parser
refuses with a dedicated message saying that at 1 the field is tangent, rims
touch tip-to-tip and nothing crosses. Tangency is declared unreachable, so the
frame the narrative wants first is the one frame that cannot exist. That belongs
in the prose as a stated absence, not papered over.

### 5.6 Recommendation

**B as the mechanism, D as an opt-in second axis where a parameter declares one,
C deferred behind section 4.2.**

## 6. Does the DSL need enriching? No

Blunt, because the question was asked that way.

1. **Staged output is already expressible with zero new surface** — not "with a
   flag", with nothing. The renderer's per-element tagging carries the
   information a stage needs, and this was verified by running the filter across
   all 14 orbs: 302 frames, one distinct viewBox per sequence, every terminal
   frame byte-identical to the unfiltered render.
2. **The cost argument does not save a proposal.** Orb body words are contextual
   identifiers rather than reserved keywords, so a new orb statement would cost
   nothing in the keyword surface. This makes the case *against* new syntax
   stronger, not weaker: the argument cannot be won on expense, so it would have
   to be won on necessity, and necessity is absent.
3. **The one thing new surface would buy is not a stage declaration.** It is a
   *declared narrative axis* — a way for an orb to say "my story is the
   `overlap` sweep" rather than having a generator guess. That is real, and a
   manifest field or a comment convention buys it without touching the grammar.
   Revisit if many orbs need it and the convention keeps drifting — with a count.
4. **New syntax would not fix the actual limitation.** Section 4.2's gap is
   between the view path and the mesh path. No grammar closes it, and anyone
   arguing for DSL enrichment on the strength of "we cannot show the final
   solid" has misdiagnosed which layer is missing.

The one-line answer: **the engine's ignorance of stages turned out not to
matter, because the renderer's per-element tagging already carries the
information a stage needs.**

## 7. Cost, output format, and where it ships

### 7.1 Cost

Measured, one hero view, all 14 orbs. Compiling all 14 costs 94 ms; generating
all 302 emitted frames as SVG, compile included, costs **126 ms** (median of
148 / 124 / 126) and 5.76 MB; writing them to disk adds ~57 ms. The Maclado
Overlap — flagged in the brief as the cost risk for its dense weave — is a 12 ms
compile.

All figures are on one machine with a warm module cache and should be read as
orders of magnitude. No CI measurement was taken, and no baseline for the
existing `orbs:` target was taken either, so this cost is stated as an absolute
addition and never as a percentage.

**Rasterisation, now measured.** An earlier draft claimed SVG-only is roughly
thirty times cheaper and could not re-derive it; the multiplier shipped marked
NOT VERIFIED. Re-run against a writable path, `rsvg-convert 2.62.1` at
1024x1024, one process per frame: **9.394 s and 9.556 s for the 302 frames —
31.1 and 31.6 ms each**, against 126 ms for the whole vector pass. The ratio is
**about 75x, not 30x**, so the correction runs in the direction that strengthens
the conclusion rather than weakening it.

The number that changes a decision, though, is not the ratio. **Rasterisation
cost is a fixed floor, not a function of scene complexity.** The corpus's
smallest frame — 510 bytes — costs 26.0 ms; its largest, 334x bigger at 170 KB,
costs 49.5 ms, a 1.9x rise. Process spawn is only 1.1 ms of that (302
`/usr/bin/true` iterations run in 0.333 s), so the rest is librsvg and cairo
painting 1,048,576 pixels regardless of what is on them. A timelapse's early
frames are its simplest, and **rasterising them is no cheaper than rasterising
the finished orb.** If Option C is ever taken, the lever is one process for many
frames.

The mitigation is therefore unchanged and better supported: **ship SVG,
rasterise nothing.** The frames are already vector at the point of generation, a
scrubbable sequence does not need a bitmap the way a gallery card does, and the
PNGs are 21 MB against the SVGs' 5.76 MB.

### 7.2 Output format

Ship an inline SVG frame sequence with a scrubber, and the frame strip as the
no-JavaScript fallback.

- **A strip of stills** verifies that each increment is legible in isolation and
  survives with JavaScript off. It does not verify that the sequence reads as
  accumulation.
- **A scrubber** verifies accumulation directly — dragging backwards subtracts
  exactly what dragging forwards added — and is the only form in which "differs
  by one comprehensible increment" is checkable by a human in seconds.
- **An animated format** verifies nothing the scrubber does not, costs a
  rasterisation pass, and takes pacing away from the reader.

The scrubber is not a new idea in this repo and the transfer condition is
already written: [`derivation-worksheet-design.md`](derivation-worksheet-design.md)
scopes out interactivity for its v1 while recording that a navigation bar and a
timeline are "the obvious next step, and are deferred, not rejected." This is
that next step, in the sibling context — and it transfers because both artifacts
are ordered SVG sequences over one fixed frame, which is the property a scrubber
needs and the only one it needs.

### 7.3 Where it ships

**bikar generates, 3d-models publishes.**

Generation belongs in bikar because that is where the scene, the tags and the
renderer live, and a generator elsewhere would import all three across a repo
boundary. Publication belongs in 3d-models because that is where the gallery and
the deploy are.

Concretely: a new `render --format timelapse` writing under bikar's build
directory alongside the existing views output, consumed by a new page per orb in
3d-models. The `orbs:` target in [`../Makefile`](../Makefile) already loops all
14 doing an STL check and then views; this is a third line in that loop.

Two pinned things must move together. `DEPLOY_PATHS` does **not** currently
include `docs/`, so the timelapse pages must not live under `docs/` unless that
list changes — and [`../.claude/gates/site_graph.py`](../.claude/gates/site_graph.py)
pins both `DEPLOY_PATHS` and `LAB_PAGES` by content, so changing either is a
deliberate, gated act rather than an edit. Put the pages where `DEPLOY_PATHS`
already reaches. Separately, bikar's studio catalogue is pinned by its own test,
so adding entries there fails that test until the test is updated in the same
commit, which is the intended behaviour.

## 8. Audit criteria for a timelapse post

This list is the durable artifact. It is what a gate checks and what a skill
would follow, and it stands whichever of section 9's answers is taken.

1. **Frame count is derived from the compiled scene, not declared.** A post
   whose frame count is a literal in a config file fails.
2. **Ordering is by the declared axis** (`element`, `repeat`, `strand`, `spike`,
   `wheel`, `param`) and is stable across regenerations of the same geometry.
3. **Camera invariance** — every frame's `viewBox` attribute is byte-identical
   to every other frame's in the same sequence.
4. **Material invariance** — fill and stroke constants identical across frames;
   no per-frame styling.
5. **One increment per frame** — consecutive frames differ by exactly one
   element on the declared axis, and the polygon count is non-decreasing through
   a cumulative sequence.
6. **Terminal identity** — the last cumulative frame is byte-identical to the
   orb's shipped view SVG for that axis, or the sequence declares a reason it
   cannot be.
7. **No undeclared stage** — every stage name maps to a construct actually
   present in the orb's `.bkr`. A frame captioned "pierced" for an orb that
   declares no piercing fails.
8. **Prose matches geometry** — every numeric claim in a caption is a count
   taken from the scene, and any count that differs between the solid and the
   visible front cap carries the hedge.
9. **Provenance** — the post records the `.bkr` content hash and the engine
   version it was generated from, so section 4.1's staleness is detectable
   rather than discovered.

## 9. Skill, or gate?

[`../CLAUDE.md`](../CLAUDE.md)'s Precedent section governs this and points at
two documents that both answered "no skill". Read against their standard —
**measured recurrence**, not plausibility — the answer here is not close.

[`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md)
rejected its skill on a finding it stated bluntly: the documentation was wrong
in ways nothing could detect, so the fix is a detector rather than more
documentation. Its gate then failed open on the first draft, and closing the
predicate took the violation count from 5 to 31.
[`issue-register-evaluation.md`](issue-register-evaluation.md) measures 48
defect fixes across 426 commits with 12 registered, and kills its own proposal
on the observation that a good register entry existed and the same defect class
shipped six more times anyway.

**Verdict: no skill. A gate.** The reason is arithmetic. Zero timelapse posts
exist. Recurrence over a population of zero is not a low number, it is an
undefined one, and a skill justified on an undefined recurrence is justified on
how useful it sounds — the exact move both precedent documents were written to
prevent.

**Splitting making from auditing, since they need not have the same answer.**
For *making*, the generator argument is total: under Option B the post is a
function of the compiled scene, so there is nothing for a skill to advise — it
would be telling an author to do by hand what the generator does by
construction. For *auditing*, the criteria in section 8 are all mechanically
checkable against artifacts on disk. Nine criteria, nine predicates, no
judgement calls. A skill is the right shape for prescriptions that need a human
to apply taste; section 8 needs none.

**The gate.** A `timelapse_gate.py` beside the existing gates, hung off a
numbered hook in the pre-commit directory and wired into `make validate`. It
must sort after the catalog and counts hooks and before the site-graph one,
since it reads generated artifacts and belongs with the artifact gates. It
checks criteria 1, 3, 4, 5, 6, 7 and 9 mechanically; criteria 2 and 8 are
checked as far as counts allow — numeric claims in captions must appear in the
scene's count table — and no further.

**Its by-design failure case**, because a gate that asserts everything passes is
a gate that has not been tested: **Maclado-9-Overlap must fail criterion 6 on
the first run.** Not as a bug, as the fixture. Its shipped cell views are ones
the current engine refuses to produce, so terminal identity has a genuine
mismatch to find, and a gate reporting 14 green on day one is a gate whose
predicate is wrong. Verify it adversarially in both directions, the way the
DSL-extension evaluation verified its own: inject a caption asserting piercing
on an orb that declares none and confirm criterion 7 fires; remove a live
sequence and confirm the gate notices the absence rather than passing vacuously.

**When to revisit the skill.** After 14 posts exist and have been regenerated at
least twice under geometry changes. If the gate is by then catching the same
class of authored-prose defect repeatedly *and* the fix needs judgement the
predicate cannot encode, the premise becomes measurable and this section should
be rewritten against real counts. The shape to copy on that day is
[`../.claude/skills/prototype/SKILL.md`](../.claude/skills/prototype/SKILL.md),
whose prescriptions live in a [`catalog.md`](../.claude/skills/prototype/catalog.md)
policed by its own gate — because a skill's prescriptions are themselves claims
and must be falsifiable.

## 10. Build plan

**First shippable slice: a timelapse format emitting SVG frames for one orb,
Star-Orb.** Smallest independently useful thing — the frames are inspectable
immediately — exercising the inscribed two-axis path that covers 11 of 14 orbs,
at 22 frames.

1. **bikar** — a stage-sequence function inside `packages/core`, returning an
   ordered array of polygon-index subsets plus stage metadata. Inscribed path
   only. A pure function over the existing scene; no engine change. Placing it
   inside core rather than widening the package export is what answers section
   3.4.
2. **bikar** — the CLI format, writing numbered SVGs per axis plus a manifest
   carrying counts, `.bkr` hash and engine version. Ship here; this is the slice.
3. **bikar** — extend to the wheelfield path via the cell metadata and to the
   ribbon path via `strandId`. Now all 14.
4. **bikar** — tests: terminal identity per orb, viewBox invariance per
   sequence, monotonic polygon counts. This is where section 4.1's FAIL case
   first turns red.
5. **3d-models** — the gate, its hook, `make validate` wiring, and the
   adversarial fixtures. Gate before page, deliberately: the gate is what makes
   the page's claims worth publishing.
6. **3d-models** — the per-orb page generator and the strip and scrubber, under
   a path `DEPLOY_PATHS` already reaches; link it from the card in `index.html`.
7. **bikar** — the parameter-sweep axis as an opt-in, non-radius parameters
   only. Last, because it is the only step that recompiles.

Steps 1 and 2 are the slice; 3 to 5 the completion; 6 and 7 the feature.

## 11. Open questions

1. Does the second `overlap` band at `[1.38, 1.60]` produce a *valid* orb, or
   one that merely compiles? Nothing has measured its printability or run qiyas
   against it.
2. Should the wheelfield `filler` cells get their own named stage rather than
   arriving with the final frame?
3. What does the page do for the orbs where cells and ribbons both exist — two
   sequences side by side, or one interleaved?
4. Does derived prose read as prose, or as telemetry? Section 8's criterion 8 is
   the correctness check; readability is untested and is the single largest risk
   to the "blog post for free" premise.
