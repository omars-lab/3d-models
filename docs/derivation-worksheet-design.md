# Derivation Worksheet — implementation design doc

Status: **DRAFT v1 — grounded in a derivation-visualization survey
([`research/derivation-visualization-survey.md`](research/derivation-visualization-survey.md),
sources in Appendix A) and in first-party experiments against the bikar tree
(measurements in §2 and §3; contested bets recorded in Appendix B).**
Scope: a *visual math worksheet* — a rendered artifact that shows how a bikar part is composed,
step by step, from its base construction to the finished shape, so a reader can follow the
geometry the way they would follow a worked equation.
Builds on: the existing `parse` → `evaluateFile` → `renderSVG` pipeline, the `wave:` / `layer:`
construction-pass tagging, and the `data-*` provenance already emitted by `svg-renderer.ts`.
Rides: nothing. This is additive and read-only with respect to the engine.

**Nothing in this doc is implemented. No code has been written. The measurements in §2–§3 come
from throwaway scripts run against the built `packages/core/dist`, not from anything checked in.**

---

## 1. Goals

1. **Show the derivation, not the result.** A worksheet page for a `.bkr` file shows a numbered
   sequence of intermediate states — the compass-and-straightedge construction, then the pattern
   emerging from it — with the operation that produced each state named in text.
2. **Name the engine's real operations.** The vocabulary drawn is bikar's vocabulary. No generic
   ∪ / ∩ / ∖ symbology is used to describe operations that are not set operations (§4.1).
3. **Reuse what exists.** No new evaluator instrumentation, no recorded trace format, no fork of
   `svg-renderer.ts`. The derivation is obtained through the already-public API surface (§4.2) and
   drawn by the existing renderer (§4.3).
4. **Stay readable at the sizes real files reach.** Measured: median 10 steps per file, p90 16,
   max 85 (§2.5). The worksheet must degrade gracefully at 85, not just at 10.
5. **Be honest where the derivation is not visible.** Some composition in bikar is invisible to
   the mechanism this doc proposes (tile blocks, `rotate`/`mirror` bodies — §2.6). The worksheet
   must *say so on the page*, not silently render a jump from nothing to everything.

**Non-goals for v1** (each should be an explicit "not in this version" note wherever a reader
would expect it):

- **No interactivity.** No scrubbing, no play button, no click-to-source. The v1 artifact is a
  static SVG sheet. GeoGebra's Navigation Bar and CascadeStudio's timeline (survey §8.4, §5.3)
  are the obvious next step, and are deferred, not rejected.
- **No 3D derivation.** The worksheet covers the 2D pattern pipeline only. `piece`/`wall`/`orb`
  solidification is out of scope for v1 — see §6.3 for why that is a harder problem, not just a
  bigger one.
- **No editing.** The worksheet is a read-only view, like FreeCAD's dependency graph
  ("The dependency graph is purely a visualization tool, therefore it cannot be edited" —
  survey §3.4).
- **No tree/DAG layout.** v1 is a linear small-multiples sheet. §4.6 records why, and Appendix B
  records the case against.
- **No new DSL syntax.** Nothing in this design adds a keyword to `.bkr`.

---

## 2. Engine ground truth

Facts verified against the bikar tree that shape the design. **Five of them contradict or
qualify assumptions in the brief that commissioned this work; those are marked ⚠.**

### 2.1 The op vocabulary as it actually exists

- **⚠ There is no general 2D polygon-clipping op.** `clip pattern to <boundary>` does not clip
  polygons against polygons; it partitions the half-edge graph and *annotates* the resulting
  faces, stamping `face.partial` and `face.clippedAtBoundary`
  (`bikar/packages/core/src/graph/half-edge.ts`, `Face` shape). Two other unrelated things are
  also spelled `clip`: `clip <Name>` is the CornerClip declaration
  (`bikar/packages/core/src/kernel3d/corner-clip.ts`), and `crop clip` is a wall mode.
- **`bikar-core` ships zero runtime dependencies.** `bikar/docs/decisions/2026-05-07-polygon-clipping-dep.md`
  records that `packages/core/package.json` has no `dependencies` block at all, and
  `grep -rn "polygon-clipping" packages/` returns nothing. There is no boolean library to
  visualize even if one wanted to.
- **⚠ `fill void where … color …` is a styling rule, not a combining op.** `evalFill` pushes to
  `env.fillRules` (`bikar/packages/core/src/dsl/evaluator.ts`). It selects faces for colour; it
  does not create or destroy geometry. Drawing it as a combining step would be a lie.
- **The real union op is exact directed-edge cancellation.** `unionPatternFaces` in
  `evaluator.ts` unions bounded faces by cancelling twin directed edges — an arrangement-walk
  union over an existing planar subdivision, not a clipping-library boolean.
- **The pipeline is a planar-graph arrangement, in 8 stages** (`bikar/docs/architecture.md`):
  planar graph → intersection graph → half-edge DCEL → face extraction. Faces are *found*, not
  *constructed*; there is no solid to subtract from.
- **⚠ `boundary X = union(...)` and `clip pattern to <boundary>` are undocumented** in
  `bikar/docs/language-reference.md`. Anyone reading the language reference to learn the
  vocabulary will not find them. (Recorded as a gap, not fixed here — this doc must not modify
  engine docs.)

### 2.2 Provenance the engine already carries

- `Face` (`graph/half-edge.ts`) has `sources?` (flattened tag set) and `edgeSources?` (per-edge
  tag multiset, parallel to `vertices`). The doc comment cites CGAL's
  `Arrangement_with_history_2` inducing-curve container as the model. **This is real
  per-primitive provenance and it already exists.**
- `evaluator.ts` `buildConnectSourceTag` emits per-invocation tags of the form
  `<base>:<mode>[:step]:#<counter>` via `env.connectInvocationCounter++`.
- `wave N` / `layer N` are construction-pass tags in the DSL and land on faces as `wave:N` /
  `layer:N` source tags.
- `svg-renderer.ts` already emits `data-face-index`, `data-sides`, `data-layer`, `data-ring`,
  plus `buildProvenanceAttrs(face)` → `data-symmetry-fold`, `data-wave`, `data-shape-id`,
  `data-authored-region`, `data-partial`, `data-clipped-boundary`. `data-wave` is the *minimum*
  `wave:N` across a face's source set.
- **The blueprint is already emitted as a hidden ghost layer**:
  `<g data-layer="-1" style="display:none">`. The scaffold is drawn, then suppressed.

### 2.3 What is *not* a derivation structure, despite the name

- **⚠ `bikar/packages/core/src/dsl/construction-tree.ts` is a name collision, not a feature.**
  It is 70 lines and tracks only circle nesting under `repeat`, to resolve `@1.3.2` address
  selectors. It is not a general derivation tree and must not be mistaken for one.
- **`piece3d` / `wall3d` / `assembly3d` provenance objects are result descriptors, not traces.**
  They describe what was produced, not the sequence that produced it. **Question (ii) of the
  brief — "check whether existing provenance is already sufficient" — resolves to: no, not for
  step sequencing.** It is sufficient for *labelling* (§4.4), which is a different job.

### 2.4 Two more stale/incorrect premises found

- **⚠ The "strict nesting interface contract" is stale.**
  `bikar/packages/core/src/kernel3d/solidify-slabs.ts` uses a **shared cell partition** and
  states in-source that "a nesting-only interface contract cannot express them." The phrasing in
  `bikar/docs/decisions/2026-07-29-w2-wall-connectors-mounts.md` (and repeated in the brief for
  this work) predates commit `31a82a3 W2 1/8: slab-stack solidifier over a shared cell
  partition`.
- **⚠ A vendored triangulator exists** (`kernel3d/earcut-vendored.ts`), which qualifies the
  founding decision's "no triangulation dependency" phrasing. The no-CSG commitment is intact;
  the no-dependency framing is looser than stated.

### 2.5 Prefix re-evaluation works today, measured

Experiment: parse a `.bkr`, cut the declaration list, re-run `evaluateFile`. Run over all 92
`.bkr` files in `bikar/patterns/`:

```
files=92  parseFail=0  steps=1139  fail=0  empty=353  warnings=67  totalMs=13410
steps per file: median=10  p90=16  max=85
```

- **Zero failures across 1139 prefixes**, once the cut semantics are right (§2.6).
- Worst file by step count: `Petal-Full.bkr` — 85 steps, 0 failures, 148 ms total.
- **Worst file by time: `Tiled Patterns/Moroccan-12-Tiled.bkr` — 10,086 ms for 11 steps
  (~917 ms/step).** Second: `Flower of Life/Flower-of-Life.bkr`, 785 ms / 17 steps. The cost is
  dominated by a handful of files, not spread evenly.
- **353 of 1139 prefixes (31%) return an empty result.** These are the blueprint phase:
  `evaluateFile` returns `lastResult`, which is undefined until a pattern runs, so the
  compass-and-straightedge steps — the most interesting part for a worksheet — render nothing by
  default.
- **18 spurious `[bikar] connect arc .petal: no face has an edge tagged '…:arc:#N'` warnings**
  appear during the `Petal-Full.bkr` prefix sweep and **0** on full evaluation. Intermediate
  states legitimately fail invariants that the finished state satisfies.

### 2.6 Three sharp edges in prefix re-evaluation, all measured

1. **Cut semantics are load-bearing.** A prefix must be: declarations `0..d-1` intact,
   declaration `d` truncated to `k` statements, and **every declaration after `d` dropped**. An
   earlier attempt truncated the blueprint while leaving downstream patterns in place and 11 of
   21 steps threw `Evaluation error: Circle C0 has not been divided` /
   `Circle L8_L0 has not been divided`.
2. **The blueprint phase needs a synthesized probe to render.** Validated workaround: parse a
   two-line stub file to obtain well-formed `render circles` / `render lines` statement nodes,
   then graft them onto a synthetic pattern pointing at the truncated blueprint. Measured output
   grows monotonically: `C=1 L=0 pts=1 bytes=401` → `C=1 L=10 pts=41 bytes=2107`. **No engine
   change required.**
3. **⚠ Not all composition is statement-shaped.** `tileBlock` is not in `pattern.statements`, so
   tile/surround composition is invisible to statement-prefix cutting: on `Rosette-10-Ring.bkr`
   it lands as one atomic jump from 0 to 202 faces. `rotate` / `mirror` bodies are likewise
   atomic. **This is the single largest honest limitation of the proposed mechanism** and is why
   Goal 5 exists.

### 2.7 The renderer is reusable unmodified

`renderSVG` already accepts and draws circles, construction lines, named points
(`emitNamedPoints`), segments, faces, face colours, layers and strapwork, and emits the full
`data-*` set. `orb-view-renderer.ts` / `--format views` is the in-tree precedent for a second
renderer composing over the same primitives. `compileDSL` in `packages/core/src/index.ts` is a
single-call-site adapter (`evaluate` → `renderSVG` with a fixed 20-field mapping) — a clean seam
to sit beside rather than modify.

### 2.8 Prior art inside this project (and the honest counter-argument)

The repo already contains four partial answers to this brief, which is both justification and a
reason for caution:

- `wave` / `layer` tagging plus CSS keyframe step-reveal — already animates construction order.
- `debug-views.ts` `facesByLayer()` / `facesBySource()` — already slices faces by provenance.
- The STRUCTURE→COLOR→WEAVE ladder in `decomposition-approach.md`.
- **31 of 92 `.bkr` files carry hand-written `# Construction:` comment blocks**, and
  `patterns/Petal Tutorial/` is a hand-maintained step series.

**The counter-argument is real: the hand-maintained tutorial series exists because a human chose
the steps, and a mechanical prefix walk will not reproduce that editorial judgment.** §4.5 and
Appendix B.4 address this; it is not fully solved.

---

## 3. What the survey established

The load-bearing facts, with the design consequence stated. Full citations in Appendix A;
detail in [`research/derivation-visualization-survey.md`](research/derivation-visualization-survey.md).

**3.1 A derivation cannot be recovered from a finished artifact — four independent literatures
agree.** Fayolle & Friedrich count `(1/(n+1))·C(2n,n)·2ⁿ·(2|P|)ⁿ⁺¹` distinct CSG trees per solid
(survey §1.6). Bonner, on his own illustrations: *"it is not always possible to know which
underlying polygonal tessellation was used to create such examples"* (§9.2). Kaplan: *"Most of the
original design techniques are lost to history"* (§9.4). OpenSCAD's own two dumps demonstrate the
loss mechanically — the `.csg` knows what was built but not what it was called, the AST dump knows
the names but has no geometry (§2.4). **Consequence: derive from authored source, never from
output geometry. This is the strongest single justification for the prefix-re-evaluation approach
and against any scheme that inspects the finished faces.**

**3.2 CSG-tree edges do not carry transforms, and no surveyed tool labels an edge at all.**
Requicha 1980 §2.5.1 verbatim: *"Nonterminal nodes represent operators, which may be either rigid
motions or regularized union, intersection, or difference; terminal nodes are either primitive
leaves … or transformation leaves which contain the defining arguments of rigid motions."* Every
implementation checked bakes the matrix into the leaf — OpenSCAD `new CSGLeaf(ps, state.matrix(),
…)`, Manifold `CsgLeafNode(pImpl_, mat3x4 transform_)`, JSCAD `{polygons, transforms}`. FreeCAD's
edges mean containment; OSGE's mean dataflow with semantics on the *destination node's port name*.
**Consequence: §4.4 depicts transformations as named steps, not as arrow labels. The brief's
"named arrows" option is available but would be an invention, and is recorded as such in
Appendix B.2.**

**3.3 Faint scaffold under bold result is a six-way convergence — and it is the Islamic
tradition's own convention.** OpenSCAD `%`/`#`/`!`/`*`; ManifoldCAD `show()` (transparent red) /
`only()` (grey ghost of the final result); OSGE's four subtree modifiers; CQ-editor `debug()` at
`color="red", alpha=0.2`; jupyter-cadquery's `#808080` result edges and bbox; replicad's
highlight API. Translucent red = "this operand"; translucent grey = "context." And Broug's
*Islamic Design Workbook* ships *"48 loose-leaf sheets, each lightly printed with the geometry of
the corresponding featured design"*, while the Topkapı Scroll preserves *"the underlying
geometries in the form of incised 'dead' drawings"* — the scaffold present but deliberately
invisible under the inked result. **bikar already does exactly this**
(`<g data-layer="-1" style="display:none">`, §2.2). **Consequence: §4.4's ghosting convention is
the most over-determined decision in this doc.**

**3.4 The principled answers to "too many steps" all come from outside CAD, and one of them maps
onto a tag system bikar already has.** MeshFlow generates 11 levels of detail by *"substituting
regular expressions defined on the operation tags"* — explicitly non-geometric clustering
(survey §7.1). GeoGebra's **Breakpoint** groups several objects into one navigable step (§8.4).
Chronicle caps fan-out at *"no more than 7"* (§7.2). Lamport supplies the rationale: *"The reader
can stop opening lower levels of the proof when satisfied that she understands why the statement
is true."* (§8.1). Meanwhile **no shipping CAD tool solved this**: ocp_vscode has a global
collapse enum, jupyter-cadquery *prunes* rather than folds, OSGE has no collapse at all.
**Consequence: §4.5 groups steps by bikar's existing `wave:` / `layer:` tags — the in-repo
analogue of MeshFlow's tag regexes — rather than by anything geometric.**

**3.5 Repetition and symmetry have a citable answer.** Agrawala et al. 2003, verbatim: *"A better
approach is to skip repetitive operations after they have been presented in detail a few times."*
And: *"maintaining visibility for all parts in a symmetric group is less important. If the user is
aware of the symmetry, it is usually enough that at least one part in the group is visible, since
the others will attach in a similar way."* Plus the visibility rule: *"all the new parts added in
each step of the assembly must be visible"* and *"the parts attached in earlier steps should also
be visible to provide context."* **Consequence: §4.6 — draw the instance once, annotate ×N,
never draw all 20 orb faces or all tiles in a wall grid.**

**3.6 Two secondary but decisive UX facts.** (a) **Sticky camera and sticky visibility across
steps** separate usable step-through from unusable: ocp_vscode's `debug.md` — *"The viewer
remembers camera position and which variables were unselected in the tree across steps"*;
jupyter-cadquery sets `reset_camera="keep"` after the first render. (b) **Node labelling is the
universal weak point**: CQ-editor labels a step with its *plane-origin coordinates*;
jupyter-cadquery with `func(args) => _v1`; OpenSCAD with `cube1` after module names are already
destroyed. Kurlander & Feiner said it in 1988 — print the operation name *"since this is not
always immediately obvious from the before and after view."* **Consequence: §4.3's fixed viewBox
across all panels, and §4.4's requirement that every panel carry a source-derived text label.**

**3.7 One negative worth stating.** **No mainstream history CAD ships per-step geometric
thumbnails.** SOLIDWORKS, Fusion, Onshape and FreeCAD all show icon + name and move a single
global cursor into one shared viewport. The per-node-geometry precedents are a 2000 Dassault
patent (US6636211B2), TouchDesigner's node viewers, Dynamo's Watch3D, and Sverchok's Stethoscope
(which renders *data*, not geometry); Blender explicitly declines — *"Complex data types such as
geometry or grids cannot be previewed this way."* **Consequence: this design's small-multiples
sheet is following Requicha's Figure 6, UCSG-Net's Figure 6, TouchDesigner and the printed
pedagogy tradition — not mainstream CAD. That is a deliberate departure and is recorded in
Appendix B.1.**

---

## 4. The design

### 4.1 Op-vocabulary honesty — option (b), with a hard rule

The brief offered three options: (a) render the true op vocabulary; (b) map onto set-theoretic
notation only where the mapping is exact; (c) show both, honest op primary, set-notation gloss
secondary.

**Decision: (b), which in practice means the true vocabulary everywhere and a set-notation gloss
almost nowhere.**

The rule: **a set-theoretic symbol may appear only where the operation is provably that set
operation on the objects being drawn.** Applying it to the ops that exist:

| DSL / engine operation | What it actually does | Worksheet label | Set gloss? |
|---|---|---|---|
| `circle` / `line` / `divide` | adds a construction primitive to the blueprint | *"draw circle C0, r=10"* | no |
| `connect` | walks tagged edges, adds segments | *"connect .petal (arc)"* | no |
| `unionPatternFaces` | exact directed-edge cancellation over bounded faces | *"merge faces (edge cancellation)"* | **yes — ∪, this is a union of point sets** |
| `boundary X = union(...)` | arrangement-walk polygon union | *"boundary X = union(…)"* | **yes — ∪** |
| `clip pattern to <B>` | partitions the arrangement, stamps `partial` / `clippedAtBoundary` | *"clip to B — N faces marked partial"* | **no.** It is a partition + annotation, not a difference. Nothing is removed. |
| `fill void where …` | pushes a styling rule to `env.fillRules` | *"fill rule: void → colour"* | **no.** It is a style, not geometry. |
| `wave N` / `layer N` | tags the construction pass | grouping header, not a step | n/a |
| `rotate` / `mirror` body | replays statements under a transform | *"rotate 60° ×6"* | no |
| z-band `hole` (3D, out of v1 scope) | in-plane difference within a band | — | **yes — ∖, the brief's example is correct** |

**The brief's own example holds up**: a z-band `hole` genuinely *is* an in-plane difference, and
would earn a `∖`. **But it is 3D, and 3D is out of scope for v1** (§1 non-goals), so **v1 ships
with exactly two operations carrying a set-notation gloss, both of them unions.** That is a
deliberately thin result and it is the honest one.

**The failure this rule prevents:** labelling `clip` with `∖` or `∩`. `clip` removes nothing —
it partitions and marks. A reader shown `∖` would conclude bikar has a boolean difference. It
does not.

Rendering: the honest name is the panel's primary label; the gloss, where it exists, is set
smaller in parentheses after it, e.g. `merge faces — edge cancellation (∪)`.

### 4.2 Where the derivation comes from — prefix re-evaluation, no new trace

**Decision: reconstruct by prefix re-evaluation of the parsed AST through the existing public
`parse` → mutate `declarations` → `evaluateFile` seam. No recorded trace. No evaluator
instrumentation. No engine change.**

Justification, in the order it should be weighed:

1. **It works today, measured**: 1139 prefixes across 92 files, 0 failures (§2.5).
2. **It reads authored source, which §3.1 establishes is the only sound place to read a
   derivation from.**
3. **"Prefer reusing what exists"** — the brief's own instruction. `parse`, `evaluateFile` and
   `evaluateAST` are already exported.
4. Existing provenance (`piece3d` / `wall3d` / `assembly3d`) is a **result descriptor, not a
   trace** (§2.3) — it cannot supply step order. Adding a trace would mean instrumenting the
   evaluator, which is the most invasive option in the survey's ranking (§12.8: monkey-patching
   the shape class is what jupyter-cadquery's own source warns against leaving on).

**The mechanism, precisely:**

```
steps(ast) = for each declaration index d, for each statement index k in decl d:
               prefix = declarations[0..d-1]  ++  [ declarations[d] with body truncated to k ]
               (declarations after d are DROPPED — §2.6.1)
               result = evaluateFile({ ...ast, declarations: prefix })
```

with `bodyOf(decl)` returning `statements` or `body`, whichever the node kind uses, and a
declaration with neither treated as one atomic step.

**Blueprint probe.** When `result` is empty and the truncated declaration is a blueprint,
re-evaluate with a synthesized trailing pattern carrying `render circles` / `render lines`,
obtained by parsing a fixed two-line stub (§2.6.2). This closes the measured 31% empty-result
gap and is the difference between a worksheet that shows the compass work and one that starts at
the finished pattern.

**Diagnostics.** Intermediate states legitimately violate invariants the final state satisfies
(§2.5: 18 warnings during a prefix sweep, 0 on full evaluation). The worksheet builder **must**
capture and suppress `[bikar]` diagnostics during prefix evaluation, and surface them only in a
`--verbose` mode. Silently letting them print would make every worksheet run look broken.

**Cost.** Median file: 10 steps, milliseconds. Worst measured: 10,086 ms for 11 steps
(`Moroccan-12-Tiled.bkr`). **Mitigation (borrowed from CascadeStudio, survey §5.3): build the
step list as metadata first, render geometry per step on demand / in a second pass, and cache.
Not implemented in v1 — v1 accepts the 10 s worst case for a batch-generated static artifact and
records it as a known cost.**

### 4.3 Rendering surface — a thin new emitter over the unmodified `svg-renderer.ts`

**Decision: a new `worksheet-renderer.ts` that composes N calls to the existing `renderSVG` into
one SVG sheet of small multiples. `svg-renderer.ts` is not modified.**

- **Precedent in-tree**: `orb-view-renderer.ts` / `--format views` already does exactly this
  shape of thing — a second renderer that arranges output from the shared primitives.
- **The renderer is already sufficient** (§2.7): circles, construction lines, named points,
  segments, faces, colours, layers, plus the full `data-*` provenance set.
- **Surface**: a new `--format worksheet` alongside `--format views`. Output is a single SVG.
- **Not the Lab.** `packages/lab` (vendored into `3d-models/lab.html` + `assets/`) is the natural
  home for the *interactive* version and is where a scrub bar would live. v1 is static (§1
  non-goals) so the Lab is deferred, not rejected.
- **Not a hand-made doc figure.** The whole point is that it regenerates when the `.bkr` changes.

**Layout**: a grid of panels, reading order left-to-right then top-to-bottom, each panel a
fixed-size cell.

**Fixed viewBox across every panel — non-negotiable.** Survey §3.6a: the intermediate states must
not rescale the view, or the reader loses the ability to compare panels. Compute the union bbox
of the *final* state and apply it to all panels. This is jupyter-cadquery's `reset_camera="keep"`
and its persistent grey reference, transposed to print.

**Provenance attributes.** Panels carry `data-worksheet-step`, `data-worksheet-decl`,
`data-worksheet-stmt`, and `data-worksheet-op`. **These are new `data-*` attributes and therefore
enter `bikar/docs/dsl-metadata-contract.md` as PROPOSED**, per that document's governance. They
are not ACCEPTED by this design doc and this doc does not modify that file. (Cautionary
precedent: `data-shape-id` is producer-side ACCEPTED but its F2-oracle use case was FALSIFIED
2026-05-29 — mAP 0.296 against 0.607 for `face_class` and 0.892 for `geom_label`. A `data-*`
attribute existing is not evidence it is useful.)

### 4.4 How a step is depicted

Each panel contains, in this order:

1. **Step number** — `07 / 23`. GeoGebra's Navigation Bar shows position as a fraction (`2 / 7`);
   copy it.
2. **The state after the step, drawn boldly** — the current prefix's rendered output.
3. **The final state, ghosted underneath at low opacity in grey** — the persistent reference.
   jupyter-cadquery's `#808080` result edges; ManifoldCAD `only()`'s grey ghost; Agrawala's *"the
   parts attached in earlier steps should also be visible to provide context."*
4. **What this step added, in translucent red / accent** — the six-way convention of §3.3.
   Computed as a set difference on rendered primitives between prefix *k* and prefix *k−1*
   (circles, lines, named points, faces by index), **not** by geometry inspection.
5. **A text label naming the operation**, derived from the source statement node kind plus its
   salient arguments — `divide C0 into 12`, `connect .petal (arc)`, `clip to B`. Kurlander &
   Feiner 1988: the name is printed *"since this is not always immediately obvious from the
   before and after view."* §3.6b shows every tool that skipped this ended up labelling steps
   with coordinates or synthetic names.

**Transformations specifically.** A transform is **a step of its own**, with the pre-transform
state ghosted and the post-transform state bold — a before/after pair inside one panel, which is
Kurlander & Feiner's prologue/epilogue. **It is not an arrow label**, because §3.2 establishes
that no surveyed system labels an edge and Requicha's formalism puts motions in nodes. Where a
directional cue helps (e.g. `rotate 60°`), draw a small arc arrow *inside the panel* as
decoration on the geometry — not as a graph edge.

**Explosion directions, if ever needed for the 3D case**: Li et al. 2008 — restrict to canonical
axes, *"Restricting the number of explosion directions makes it easier for the viewer to
interpret how each part in the exploded view has moved from its original position."* Out of v1
scope; recorded so it is not re-derived later.

### 4.5 Elision — group by the tags the DSL already has

**Decision: steps are grouped into sections by their `wave:` / `layer:` tags, and a section may
collapse to a single representative panel.**

This is MeshFlow's mechanism (*"substituting regular expressions defined on the operation tags"*
— non-geometric, tag-driven) applied to tags bikar already emits, and GeoGebra's Breakpoint
(several objects grouped into one navigable step) applied to a grouping the author already wrote
in the `.bkr` file.

Concretely:

- **`--worksheet-detail=full`** — one panel per prefix. Median 10, max 85 (§2.5).
- **`--worksheet-detail=waves`** (default) — one panel per `wave` / `layer` boundary, plus the
  final state. Targets the measured median of ~10 rather than the measured max of 85.
- **`--worksheet-detail=phases`** — blueprint / pattern / style, three panels plus final.

**Fan-out cap**: no more than **7** panels in a row before wrapping, from Chronicle's *"no more
than 7, which prevents the need for scrolling."* This is a layout constant, not a limit on total
steps.

**Honest limits of this scheme**, stated because they will bite:

- `wave` / `layer` are **optional** in the DSL. A file that uses neither gets `waves` mode
  degenerating to `full`. The worksheet must detect this and say so on the page rather than
  silently emitting 85 panels.
- The grouping reflects the *author's* construction passes, which is a feature (it is editorial
  judgment, per §2.8) and a liability (it is only as good as the author's tagging).
- **This does not solve §2.6.3.** Tile blocks and `rotate`/`mirror` bodies are atomic regardless
  of detail level. Those panels must be annotated on the page — e.g. *"tile block: 202 faces in
  one step (not decomposable — see §2.6.3)"* — per Goal 5.

### 4.6 The many-instance case — draw once, annotate ×N

**Decision: repeated and symmetric instances are drawn once at full detail, with the remainder
indicated by a count annotation and, where cheap, a faint outline of the full set.**

Directly from Agrawala et al. 2003 (§3.5): *"A better approach is to skip repetitive operations
after they have been presented in detail a few times"*, and *"If the user is aware of the
symmetry, it is usually enough that at least one part in the group is visible."*

Measured instance counts in-tree: `Clip-Wall.bkr` wall `instances = 4`; `Dodeca-Orb.bkr` base
polyhedron 12 faces / 20 vertices; `Rosette-Orb.bkr` 22 faces / 45 segments, projection
`spherical`, family `lattice`.

Rendering rule:

- A `repeat` / `rotate ×N` / tile grid produces **one detailed panel** showing instance 1, bold,
  with instances 2..N drawn as faint outlines in the same panel, plus the label `×N`.
- **Panel N+1 shows the assembled result**, so the reader sees the whole. This is Agrawala's
  *"presented in detail a few times"* reduced to "once, then the aggregate."
- **Symmetry folds already have a provenance attribute** — `data-symmetry-fold` (§2.2) — so the
  fold count is available without new computation.

**v1 does not do this for the 3D orb case**, because 3D is out of scope. The 20-face orb is
listed in the brief as a motivating example and **v1 does not address it.** §6.3.

### 4.7 Scope-outs, stated explicitly

Beyond the §1 non-goals:

- **No `.bkr` file is modified.** The worksheet is derived, not authored.
- **No engine file is modified.** Not `svg-renderer.ts`, not `evaluator.ts`, not
  `dsl-metadata-contract.md`. The new `data-*` attributes are PROPOSED, and proposing them is a
  separate change under that document's governance.
- **No claim that this replaces `patterns/Petal Tutorial/`.** The hand-maintained series encodes
  editorial choices a mechanical walk does not reproduce (§2.8).
- **No colour-as-referent scheme.** Byrne's 1847 substitution of coloured glyphs for alphabetic
  labels (survey §8.2) is the most interesting unexplored idea in the survey and is deliberately
  deferred; bikar's colour channel is already carrying `fill` rules and would collide.
- **No two-level scoring.** Euclidea's simultaneous L (tool moves) / E (elementary moves) scoring
  maps suggestively onto `.bkr` statements vs. underlying construction primitives, and is
  deferred.

---

## 5. Validators and failure modes

There is no manifold gate here — nothing is fabricated — but the worksheet can be wrong in
specific, checkable ways.

| # | Failure | Detection | Response |
|---|---|---|---|
| V1 | A prefix throws | catch per step | Emit the panel with an error stamp and the message; **do not abort the sheet.** Measured baseline is 0/1139, so any failure is a signal. |
| V2 | A prefix renders empty | `!result \|\| !result.faces` | Try the blueprint probe (§4.2). If still empty, emit an explicit "no visible output at this step" panel — **never a blank panel**, which reads as a bug. |
| V3 | Non-monotonic output | primitive counts decrease between step *k* and *k+1* | Legitimate in principle (`clip` reduces nothing, but a re-render might), suspicious in practice. Warn in verbose mode; do not fail. |
| V4 | Step count explodes | steps > 40 in `full` mode | Auto-fall back to `waves` and print a note on the sheet. |
| V5 | Slow file | total build > 30 s | Warn with the per-step timing; measured worst is 10 s. |
| V6 | `[bikar]` diagnostics during prefix eval | intercept `console.warn`/`console.error` | Suppress by default (§4.2). **Count them and report the count**, so a real regression is not hidden by the suppression. |
| V7 | Atomic-jump panel | a single step's face delta exceeds a threshold (e.g. > 50% of final) | Annotate the panel as an atomic composition (§2.6.3). This is the Goal 5 requirement made mechanical. |
| V8 | viewBox drift | any panel's content exceeds the shared viewBox | Should be impossible if the final state bounds everything; if it happens, the fixed-viewBox assumption is wrong for that file. Fail loudly. |

**The failure mode with no validator**: the worksheet can be *complete and correct and still not
be the derivation the author had in mind*, because §3.1 says the derivation is a choice. Prefix
re-evaluation recovers *a* faithful sequence — the one the source file literally specifies — not
necessarily a pedagogically good one. No validator can catch that.

### 5.1 Enforcement — what is a gate, what is a warning, what cannot be enforced

§5's table says what the builder *does* on each failure. It does not say which of those are
**gates**. Without that distinction V1–V8 quietly become documentation instead of checks, so this
section fixes it.

**First, the largest category: enforced by construction, needing no gate at all.**

The worksheet cannot drift from the code, because it holds no independent representation of the
code. Every panel is `evaluateFile` run on a truncated copy of the real AST, rendered through the
unmodified `renderSVG` (§4.2, §4.3). There is no second geometry path to keep in sync, which is
precisely why the recorded-trace alternative was rejected — *that* design would have created one.
Edit the `.bkr` and panel *k* changes because the compiler genuinely produces something different
at step *k*. **No hook is needed to enforce agreement between the worksheet and the engine; the
architecture makes disagreement unrepresentable.**

What remains enforceable is narrower, and worth naming exactly.

#### The three mechanical gates

**E1 — the prefix sweep must stay at `fail=0`.** Phase 1 already specifies the 92-file sweep as a
test fixture; this promotes it from a one-off measurement to a standing assertion. The measured
baseline is 1139 prefixes, 0 failures (§2.5), which is what makes V1 meaningful: *any* throw is a
signal precisely because the floor is zero. A vitest case, so it rides the existing
`npm test` → pre-commit → CI chain. **No new hook.**

**E2 — the set-gloss rule becomes a closed vocabulary in code.** §4.1's rule ("a set-theoretic
symbol may appear only where the operation is provably that set operation") is currently prose,
and prose rules about notation are exactly the kind that erode. Make the §4.1 table a literal
table in the emitter — op kind → `{ label, gloss? }` — where `gloss` is populated for an
**allowlist of two** (`unionPatternFaces`, `boundary … = union(…)`). A test asserts no gloss
outside that allowlist.

This converts the rule into a lint, and gives the property that matters: **adding a gloss is a
reviewable diff.** When 3D lands and z-band `hole` earns its `∖` (§4.1), that is a deliberate
one-line change someone signs off on — not a label that appeared because it looked plausible. The
failure this prevents is concrete and already identified: labelling `clip` with `∖`, which would
tell a reader bikar has boolean difference. It does not.

**E3 — suppressed diagnostics are counted against a baseline.** §4.2 requires `[bikar]`
diagnostics to be suppressed during prefix evaluation, because intermediate states legitimately
violate invariants the final state satisfies (18 warnings during a sweep, 0 on full evaluation).
Suppression that is not counted is indistinguishable from a regression being swallowed. V6 already
says "count them and report the count" — E3 asserts the count against the recorded baseline, so a
new warning class surfaces as a diff rather than vanishing into the suppressor.

#### V1–V8, triaged

| | Failure | Enforcement class |
|---|---|---|
| V1 | prefix throws | **gate (E1)** — `fail=0` asserted in test |
| V2 | prefix renders empty | runtime behaviour — explicit panel, never blank; counted |
| V3 | non-monotonic output | warning, verbose only — legitimate in principle |
| V4 | step count explodes | runtime behaviour — auto-fall back to `waves`, note on sheet |
| V5 | slow file | warning with per-step timing |
| V6 | `[bikar]` diagnostics | **gate (E3)** — count vs baseline |
| V7 | atomic-jump panel | annotation, deliberately not a gate — it is a *finding*, not a fault |
| V8 | viewBox drift | **gate** — should be impossible; fail loudly, do not degrade |

Three gates, five non-gates. That ratio is intended: a worksheet that refuses to build is worse
than one that builds with an honest error stamp on one panel, so V1 aside, failures render rather
than abort.

#### If a hook is wanted, extend the one that exists

The repo already runs `.claude/hooks/check-bkr-mesh.py` as a Stop hook: on changed `.bkr` files it
runs `bikar render … --format stl --check` per declared part, against an allowlist. The natural
move is to **extend that hook** — when a `.bkr` changes, also build its worksheet and assert E1 —
rather than to add a second hook with its own conventions. The cost of that gate is already paid
and understood.

Two properties of that hook are worth copying rather than reinventing:

- **It reports stale exemptions.** An allowlisted part that starts *passing* is surfaced, so an
  exemption does not quietly outlive its cause. E2's gloss allowlist should behave the same way:
  a gloss entry for an op that no longer exists is reported, not ignored.
- **Its allowlist demands a stated physical reason.** The schema note says that if you cannot
  write the reason, the part does not belong there. E2's allowlist should carry the same burden —
  each gloss entry names *why* the operation is provably that set operation on the objects drawn.

#### What cannot be enforced, restated

The gap above §5.1 is not closed by any of this, and no amount of hook design will close it: a
worksheet can pass E1, E2 and E3, be complete and correct, and still not be the derivation the
author meant, because §3.1 establishes that the derivation is a *choice*. E1–E3 enforce
**faithfulness to the source**. Pedagogical quality is reviewed by a human or not at all, and
this document should not pretend otherwise.

A second, smaller honesty note: **E1's floor is only as good as its corpus.** `fail=0` across 92
files means the mechanism holds for the constructions those files use. A genuinely new
declaration kind could break prefix cutting (§2.6.1) without any existing fixture noticing. When
a new declaration kind lands, the sweep corpus must grow with it — that obligation belongs to
whoever adds the kind, and is not something the gate can self-detect.

---

## 6. Phasing

Commit-sized steps. Nothing below is implemented.

**Phase 1 — step extraction, no rendering.** `worksheet-steps.ts`: `parse` → enumerate prefixes
with the §4.2 cut semantics → return `{ declIndex, stmtIndex, kind, label, result }[]`. Includes
diagnostic suppression (V6) and the blueprint probe. Test: the 92-file sweep as a fixture,
asserting `fail=0`.

**Phase 2 — single-panel rendering.** Render one step through the unmodified `renderSVG` with a
supplied fixed viewBox. Proves §2.7's claim that no renderer change is needed.

**Phase 3 — the sheet.** `worksheet-renderer.ts`: grid layout, 7-per-row wrap, step numbering,
shared viewBox, per-panel labels. `--format worksheet` in the CLI.

**Phase 4 — ghosting and deltas.** Final-state grey underlay; per-step added-primitive
highlighting in accent colour (§4.4 items 3–4).

**Phase 5 — grouping.** `--worksheet-detail` with `full` / `waves` / `phases`; the
no-tags-present degradation notice; V4 auto-fallback.

**Phase 6 — instances.** ×N annotation and faint outlines for `repeat` / `rotate` / tile grids
(§4.6); V7 atomic-jump annotation.

**Phase 7 — contract.** Propose `data-worksheet-*` in `bikar/docs/dsl-metadata-contract.md` as
PROPOSED, with the use case stated so it can be falsified later the way `data-shape-id`'s was.

**Deferred beyond v1**: laziness/caching for the 10 s file; the Lab panel with a scrub bar;
click-to-source; 3D.

> **Correction (2026-07-29).** The parenthetical this list originally carried — *"CascadeStudio
> recovers the line from the stack, Zoo keeps source ranges — both cheap, survey §12.7"* — was
> wrong in both halves, and `docs/click-to-source-design.md` records the measurements.
> **CascadeStudio does not implement click-to-source at all**: the stack trick is real but drives a
> timeline scrubber, its viewport carries only a `mousemove` listener, and its `Face Index: N`
> tooltip is never joined to a line number. The survey's §12.7 was accurate about *step*→source;
> this list compressed it into *shape*→source. **Zoo's source ranges are not the hard part either**
> — its own README says a wall face has no direct bit of KCL to refer to, so it traverses an
> artifact graph and highlights *both* the segment and the extrude node. The blocker for bikar is
> not spans (see the §8.5 correction); it is that provenance is genuinely many-to-many.

---

## 7. Open questions

Numbered, each with how it gets resolved.

**Q1. Does prefix re-evaluation stay at 0 failures outside `bikar/patterns/`?**
The sweep covered the 92 in-repo files. Real user files, and the 3d-models catalog's own `.bkr`
sources, are unmeasured. *Resolved by:* running the Phase 1 sweep over every `.bkr` reachable in
both repos before Phase 3 lands.

**Q2. Is `waves` grouping actually available on the files that need it most?**
`wave` / `layer` are optional. If the 85-step `Petal-Full.bkr` has no wave tags, the default
detail mode does nothing for the worst case. *Resolved by:* counting `wave` / `layer` usage
across the corpus — a one-line grep — before committing to `waves` as the default.

**Q3. Is the 10 s worst case a property of the file or of prefix re-evaluation?**
`Moroccan-12-Tiled.bkr` costs ~917 ms/step. Unknown whether full evaluation of that file is
already slow (making the worksheet ~11× a slow baseline) or whether prefix cutting defeats a
cache. *Resolved by:* timing one full `evaluateFile` on that file and comparing.

**Q4. What is the right answer for tile blocks and `rotate`/`mirror` bodies?**
§2.6.3 is the largest limitation. Options: (a) annotate and accept, which is v1's answer; (b)
extend prefix cutting into `tileBlock` and body arrays, which is more evaluator surface than this
design wants to touch; (c) add a DSL-level opt-in. *Resolved by:* shipping (a), then measuring how
often V7 fires across the corpus. If it fires on most files, (a) is not enough.

**Q5. Is the fixed shared viewBox right, or should the compass phase have its own?**
The blueprint's construction circles may extend well beyond the final pattern's bounds, or be
much smaller. A single viewBox may make the early panels unreadably tiny. *Resolved by:*
computing both bboxes on a sample of files and comparing the ratio; if it commonly exceeds ~3×, a
two-viewBox scheme (one for the blueprint section, one for the pattern section) is needed —
which weakens §3.6a's sticky-view principle and must be traded off explicitly.

**Q6. Does the added-primitive delta (§4.4 item 4) survive re-indexing?**
The delta is computed by comparing rendered primitive lists between consecutive prefixes. If face
indices are not stable across prefixes — plausible, since faces are *extracted* from an
arrangement that changes — index-based diffing is wrong and the highlight will be noise.
*Resolved by:* checking whether `Face.sources` / `edgeSources` give a stable identity to diff on
instead of the index. **This is the most likely thing in this doc to be wrong.**

**Q7. Is `--format worksheet` the right surface, or should this be a separate package?**
`compileDSL`'s fixed 20-field mapping is a narrow seam. Adding a format may pressure it.
*Resolved by:* attempting Phase 3 against the existing CLI; if it requires changing `compileDSL`,
that is a signal to make it a sibling entry point instead.

**Q8. Should the two set-notation glosses (§4.1) exist at all in v1?**
With 3D out of scope, only two operations earn a symbol, both unions. Two symbols on a sheet may
be more confusing than zero. *Resolved by:* rendering a sample sheet both ways and picking. This
is a judgment call that should not be made in the abstract.

**Q9. Does anything here duplicate `debug-views.ts` badly enough to merge?**
`facesByLayer()` / `facesBySource()` already slice by provenance (§2.8). *Resolved by:* reading
`debug-views.ts` in full during Phase 1 and either reusing its selectors or recording why not.

**Q10. How does the worksheet interact with the `maintain-use-cases` pre-commit hook?**
This repo's hook blocks pointer-file commits without a use-case map update. A new doc plus a new
output format probably needs a UC entry. *Resolved by:* reading
`.claude/skills/maintain-use-cases` before the first commit that touches the map. **Not resolved
here, because this doc is not being committed.**

---

## 8. Should the AST be a schema-validated JSON IR?

This question arrived through the worksheet — §4.2 consumes the parsed AST by prefix
re-evaluation — but it is broader than the worksheet, and the honest answer turns out not to
depend on the worksheet at all. **Measurements in this section come from throwaway scripts run
against the built `packages/core/dist`, same convention as §2–§3. Nothing here is implemented.**

Tool versions used, so the numbers are reproducible: Node 22.22.3, TypeScript 7.0.2,
`ts-json-schema-generator` 2.9.0, `ajv` 8.20.0.

### 8.1 Premise check

**The premise:** `parse(source)` returns a `FileNode` (`bikar/packages/core/src/dsl/ast.ts:372`)
built entirely from interfaces and discriminated unions — no classes, Maps, Sets or functions —
so the AST is already a JSON document in all but name, and a 20-file spot check round-trips it
through `JSON.stringify`/`JSON.parse` losslessly.

**It survives, and the corpus is much larger than 20 — but the word "losslessly" needs one
qualification that had not been measured.**

Every `.bkr` file reachable in the four repos that touch this pipeline was swept: **327 files**
(bikar 93 — the 92 in `patterns/` from §2.5 plus one in `packages/core/tests/fixtures`;
3d-models 11; sacred-patterns 112; qiyas 111). One pre-existing parse failure,
`sacred-patterns/sessions/bikar-medallion-10/girih-network/girih-star4.bkr`
(`Parse error at 17:37: Unexpected token: Identifier ('star')`) — unrelated to serialization, and
noted rather than fixed.

```
files=327  parseFail=1  AST object nodes scanned=55,701  distinct node kinds observed=61
round-trip, VALUE identity (deepStrictEqual, undefined-valued keys stripped):  326/326
round-trip, KEY   identity (deepStrictEqual, raw AST vs revived):                0/326
JSON.stringify is a fixpoint after one pass:                                   326/326
JSON size: 2,199,036 bytes total, mean 6,746 bytes/file
```

A structural audit of all 55,701 object nodes found **zero** classes, Maps, Sets, Dates, RegExps,
functions, symbols, BigInts, reference cycles, or non-finite numbers. On that axis the premise is
not merely true, it is unqualifiedly true.

**The qualification: key identity is 0/326, not 326/326.** The parser writes properties with an
explicit `undefined` value rather than omitting them — **11,057 occurrences across all 326 files**,
led by `offsetDeg` (7,099), `className` (2,067), `opacity` (381) and `tileBlock` (326).
`JSON.stringify` drops those keys. So `Object.keys(node)` differs before and after the round trip,
and `assert.deepStrictEqual(ast, JSON.parse(JSON.stringify(ast)))` **fails on every file in the
corpus**.

This is semantically nil under TypeScript's default optional-property model — `{ offsetDeg:
undefined }` and `{}` both inhabit `{ offsetDeg?: number }` — and it is invisible to a JSON Schema,
because absence and `undefined` are the same thing on the wire. But it is a live trap in exactly
two places, and both are places this design would walk into:

- **`deepStrictEqual` in a test.** A round-trip fixture written the obvious way fails on all 326
  files. It must compare `JSON.parse(JSON.stringify(x))` against `JSON.parse(JSON.stringify(y))`,
  never the raw parse output.
- **`exactOptionalPropertyTypes`.** If bikar ever enables it, `undefined`-valued optional keys stop
  type-checking and 11,057 of them surface at once.

The saving grace is the third measurement: **serialization is a fixpoint after one pass.** Once a
`FileNode` has been through JSON, it is stable forever. So the IR, if it existed, would be
well-defined; it is the *first* hop that is not identity.

**Two of the brief's other premises also verified, unchanged:**

- **`gt.json` is a post-evaluation result descriptor, not a trace.** `GT_SCHEMA_VERSION = '1.24'`
  at `bikar/packages/core/src/render/gt-emitter.ts:341`; the file header states it "exports the
  face graph from `EvaluationResult`". It takes the *output* of `evaluateFile` as input. It cannot
  supply step order, exactly as §2.3 already concluded for the `piece3d`/`wall3d` provenance
  objects. **Confirmed.**
- **`GT_SCHEMA_VERSION = '1.24'` and qiyas `SCHEMA_VERSION = '1.22'` are independent version
  lines, not drift.** `qiyas/src/qiyas/schema.py:17` names "bikar GT schema 1.24" inside the
  changelog comment for its own 1.22. **Confirmed; not reported as a problem anywhere below.**

### 8.2 What the IR is for — a consumer census, and it comes up empty

A schema is worth its maintenance only if something across a boundary reads it. Every candidate
consumer was checked against the tree rather than assumed.

| Candidate consumer | Does it need a serialized, schema-validated AST today? | Evidence |
|---|---|---|
| **The derivation worksheet** (this doc) | **No.** It calls `parse` and mutates `declarations` **in-process**, then hands the object straight to `evaluateFile` (§4.2). The AST never crosses a process boundary, never becomes a string, and is already statically typed as `FileNode` by `tsc`. | §4.2 mechanism; `parse` / `evaluateFile` / `evaluateAST` all confirmed exported at runtime from `packages/core/dist/index.js` |
| **qiyas** | **No.** qiyas consumes rasterized SVG and `gt.json` — the *geometry* seam, not the *source* seam. A grep for `.bkr` across `qiyas/src/qiyas/*.py` returns **one hit, inside a docstring** (`validate_dsl_contract.py:181`). qiyas has never parsed a `.bkr`. | grep over `qiyas/src/qiyas/` |
| **The Lab / studio** | **No.** `packages/lab/src/evaluate.ts:230` calls `parse(req.source).params` — it ships **source text** over the wire and parses at the far end, reading only the `params` knob specs. The AST is created and discarded locally. | `packages/lab/src/evaluate.ts:230` |
| **The CLI** | **Already emits one — but for a human, not a program.** The `parse` subcommand does `console.log(JSON.stringify(ast, null, 2))` (`packages/cli/src/index.ts:571`), so an AST-as-JSON surface **does** exist today. It is a debug dump to stdout: unversioned, undocumented, with no declared consumer and nothing reading it back. `--format ast` is separately absent — `packages/cli/src/index.ts:405` rejects any format outside `svg, stl, views, parts`. | `packages/cli/src/index.ts:571`, `:405` |
| **Click-to-source** | **Impossible**, not merely absent — see §8.5. | `ast.ts`, `lexer.ts:85` |
| **External / third-party tooling** | Speculative. No such consumer exists or has been requested. | — |

**Decision: the IR has zero actual consumers, and every enumerated candidate is either speculative
or has been checked and does not want it.** This is the finding that decides the section. The
worksheet — the work that raised the question — is the *least* motivated consumer of all, because
it is a single-process caller that already gets a compile-time-checked `FileNode` for free.

A schema whose only consumer is hypothetical is a solution looking for a problem, and this doc's
own track record (`data-shape-id`: producer-side ACCEPTED, use-case FALSIFIED 2026-05-29, mAP 0.296
against 0.892 — §4.3) is the local precedent for what happens when an artifact ships ahead of a
verified consumer.

### 8.3 The discriminated-union problem — tested, and it is not the problem

The brief's stated worry: a generator that flattens a discriminated union into an unconstrained
`oneOf` produces a schema that validates almost nothing. `ast.ts` is built on such unions —
`ASTNode` (`ast.ts:11`), `Declaration` (`:56`), `PieceConstructorNode` (`:128`),
`PortContractNode` (`:167`), `StyleSelector` (`:387`), `NumericExpr` (`:590`).

**This was tested against the real file, not a toy.** `ts-json-schema-generator` 2.9.0 was pointed
at `packages/core/src/dsl/ast.ts` with `--type FileNode` and the real `packages/core/tsconfig.json`.

**It succeeded on the first attempt, with no errors, no annotations, and no changes to `ast.ts`.**

```
draft: draft-07     definitions: 80     union definitions: 9     bytes: 88,424
unions whose branches are all $ref-or-const-tagged:  9 / 9
branch counts: ASTNode=38  Declaration=10  NumericExpr=6  PortContractNode=5  PieceConstructorNode=4
```

What it actually emitted for `StyleSelector` (`ast.ts:387`) — abridged, but structurally verbatim:

```json
{ "anyOf": [
    { "type": "object", "additionalProperties": false,
      "properties": { "type": { "const": "class", "type": "string" },
                      "className": { "type": "string" } },
      "required": ["type", "className"] },
    { "type": "object", "additionalProperties": false,
      "properties": { "type": { "const": "and", "type": "string" },
                      "left":  { "$ref": "#/definitions/StyleSelector" },
                      "right": { "$ref": "#/definitions/StyleSelector" } },
      "required": ["type", "left", "right"] },
    …3 more ] }
```

That is the correct shape: one branch per variant, `const` on the tag, `additionalProperties:
false`, accurate `required` lists, optional properties simply omitted from `required`, and
`$ref` self-reference for the recursive `and` arm. `Declaration` came out as an `anyOf` of ten
`$ref`s to named per-kind definitions. **The feared flattening did not occur anywhere: 9 of 9
unions are correctly tagged.**

Validating the corpus against the generated schema:

```
files=327  parseFail=1  schemaPass=326  schemaFail=0
ajv compile (once): 122 ms      validate 326 ASTs: 142 ms total (0.44 ms/file)
```

**So the generation problem is solved, cheaply, and the premise's worry is falsified.** What is
*not* solved is error quality, and that is worth recording because it is the real cost:

| Concern | Measured |
|---|---|
| Corrupting one `declarations[0].kind` to an unknown value, `allErrors: true` | **58 errors** — every branch of `Declaration` reports its own failure |
| Same, `allErrors: false` | **11 errors**, and the first one is misleading: `/declarations/0 must have required property 'body'` — ajv picked a branch the author never intended |
| Wrong scalar type, unknown property, null-for-object, tag/payload mismatch | all correctly **rejected** |

The fix is known but is not free. `anyOf` + `const` is the canonical JSON Schema idiom;
**OpenAPI's `discriminator` keyword is not part of JSON Schema** — it appears in none of the
2020-12 applicator or validation vocabularies. ajv supports it as an opt-in extension
(`discriminator: true`, off by default) and it collapses the 58-error cascade to one precise
error, but its documented requirements are strict: `oneOf` must be present, the tag must be
`required`, each branch must carry the tag as `const` or `enum` with values unique across the
union, and branches must be inline or bare `$ref`. `ts-json-schema-generator` can emit exactly
that shape via `discriminatorType: 'open-api'` — but that config is **not exposed on the 2.9.0
CLI** (verified: `--discriminator-type` is rejected as an unknown option; the field exists only in
the programmatic `Config`, defaulting to `'json-schema'`), **and it activates only per-type via a
`@discriminator` JSDoc tag on the union declaration.**

That last clause is the sting: getting good errors means **adding nine JSDoc annotations to
`ast.ts`**, which is an engine-file edit, which §4.7 already scopes out. The good schema is not
obtainable without touching the engine.

### 8.4 Shape is not meaning — stated hard, because this is where a schema oversells

**A JSON Schema validates that a declaration carries the fields its `kind` requires. It does not
and cannot validate that the file means anything.** That stays the evaluator's job, permanently.

This was not left as an assertion. Nine mutations were applied to the parsed AST of
`patterns/Flower of Life/Flower-of-Life.bkr`, each touching **only existing fields with
type-correct values**, then run through both the generated schema and `evaluateFile`:

| Mutation | Schema | Evaluator |
|---|---|---|
| `divide.circleId` → a circle that was never declared | **VALID** | throws `Undefined circle: C_NEVER_DECLARED` |
| `pattern.blueprintRef` → a blueprint that does not exist | **VALID** | throws `Blueprint 'NOPE' not defined` |
| `declarations.reverse()` — pattern now precedes its blueprint | **VALID** | throws `Blueprint 'flower_of_life' not defined` |
| delete the `blueprintDeclaration`, keep the pattern using it | **VALID** | throws `Blueprint 'flower_of_life' not defined` |
| `divide.count` → `0` | **VALID** | throws `Point index 0 out of range for circle C0` |
| `divide.count` → `-3` | **VALID** | throws `Point index 0 out of range` |
| `divide.count` → `2.5` (non-integer) | **VALID** | throws `Point index 3 out of range` |
| circle radius literal → `-5` (negative radius) | **VALID** | **evaluates, produces output** |
| circle radius literal → `0` | **VALID** | **evaluates, produces output** |

**9 of 9 semantic corruptions pass the schema.** Seven crash the evaluator; **two — a
zero-radius and a negative-radius circle — pass the schema *and* the evaluator and silently
produce a render.** A tenth mutation, `divide.count` → `1,000,000`, is schema-valid and drove Node
to a fatal out-of-memory at a 4 GB heap.

The rule this establishes, and which any future IR document must repeat: **`connect` referencing
an existing tag, `blueprintRef` resolving, a port contract being satisfiable, declaration order
being sound, and a radius being positive are all invariants over the *environment* the evaluator
builds, not over the *shape* of a node.** No JSON Schema expresses them. A gate that validates
the AST against a schema and reports green has verified that `tsc` did its job — nothing more.

There is a sharper version of this. `parse()`'s output is already constrained by `ast.ts` at
compile time. Runtime-validating it against a schema *generated from `ast.ts`* is a tautology: it
can only fail if TypeScript's type system was violated. **A schema earns its cost only where AST
JSON arrives from outside the type system** — hand-written fixtures, a second producer, a network
boundary. §8.2 established that no such source exists.

### 8.5 Source spans and round-trip fidelity — the AST is not a CST and cannot cheaply become one

**bikar's AST retains no source positions at all.** A grep for any node field named
`line`/`column`/`loc`/`span`/`pos`/`range`/`start`/`end`/`offset`/`comments`/`trivia` across all
1,190 lines of `ast.ts` returns **nothing**. Position information exists — every `Token` carries
`line` and `column`, and `ParseError` (`packages/core/src/dsl/parser.ts:90–96`) surfaces them so
the CLI can pretty-print `<file>:<line>:<column>` — but it is **consumed and discarded at node
construction**.

Two further findings compound it:

- **Comments are destroyed in the lexer.** `packages/core/src/dsl/lexer.ts:85` —
  *"`#` to end-of-line; whole comment discarded"*. §2.8 records that **31 of 92 `.bkr` files carry
  hand-written `# Construction:` comment blocks**. Those blocks are the single most
  editorially valuable content in the corpus, and the AST cannot see them.
- **There is no AST → `.bkr` printer.** A grep for `unparse` / `printAST` / `toSource` /
  `astToSource` / `formatBkr` across `packages/*/src` returns one false positive (the word
  "unparseable" in a comment at `render/svg-utils.ts:202`) and nothing real.

**Consequences, stated plainly:**

1. **Click-to-source is not "deferred", it is blocked.** §6's deferred list cites CascadeStudio
   recovering the line from a stack and Zoo keeping source ranges, both "cheap". For bikar they are
   **not** cheap: they require threading token positions into every AST node — an `ast.ts` change,
   a `parser.ts` change, and a corresponding schema change. Shipping an IR first would lock in a
   version that cannot do the thing the IR's most attractive use case needs. **Q-new below records
   this.**

   > **Correction (2026-07-29) — the cost claim above is wrong, but the conclusion survives for a
   > different reason.** `docs/click-to-source-design.md` measured it. "Threading token positions
   > into every AST node" is the cost of *expression*-level spans (101 tagged construction sites,
   > 76 distinct tags, 166 object literals). Click-to-source needs only *statement* granularity,
   > and `parseStatement` (`bikar/packages/core/src/dsl/parser.ts:2167`) and `parseDeclaration`
   > (`:604`) are each a **single handler-table dispatch chokepoint** — verified. A **+9/−2-line
   > patch at two sites** gives **1,400 / 1,405 (99.6 %)** statement and declaration nodes a
   > correct `loc`, none pointing at a blank or comment line, with all 92 pattern files still
   > evaluating. Comment retention is ~4 lines in `lexer.ts` plus a side list on `FileNode`.
   >
   > What actually blocks the feature is **§8.5's third consequence, not its first**: provenance is
   > many-to-many. Measured over 5,394 faces in 92 files, only **38.9 %** of faces trace to exactly
   > one source line (50.5 % trace to two, 8.1 % to three, 2.4 % to none). Backwards is worse — one
   > statement produces a **median of 17 faces, p90 129, max 417**, and **exactly 1 of 186**
   > statement-sources produces exactly one face. So the honest answer to "which line made this
   > shape?" is usually a *set*, and the AST change is not what stands in the way of giving it.
   >
   > This means **§4.7 / §8.9's "no engine file modified" scope-out is now a deliberate, documented
   > exception**, not a constraint: every workaround costs more than the 12 lines it avoids, and
   > the `WeakMap` side table specifically dies on this doc's own `{...ast, declarations: prefix}`
   > prefix-spread (§2.5). Two hazards found while measuring, both pre-existing and worth knowing
   > before anyone acts on the above: riding `Segment.tags` with a `src:<line>` marker **silently
   > corrupts the ACCEPTED `data-shape-id` contract** (734 → 1,788 faces, +143.6 %, and it emits a
   > literal `data-shape-id="src:15"`) because `isNamedShapeTag` is an exclusion list mirrored in
   > three places — `svg-renderer.ts:309`, `gt-emitter.ts:1219`, `gt-emitter.ts:816`; and
   > `preprocessSource`'s length-changing `#RRGGBB` rewrite **shifts every reported column by +5
   > per preceding hex literal** (283 lines across 75 files). Lines are unaffected, so statement
   > spans are safe; `ParseError` columns are already wrong today.
   >
   > **Built 2026-07-29.** Both landed in bikar, in that order —
   > `docs/decisions/2026-07-29-lexer-hex-colors-token-context.md` (the column shift; the
   > preprocessor is gone, positions now address the file as written) and
   > `docs/decisions/2026-07-29-parser-statement-spans-comment-retention.md` (the spans). The
   > estimate above was pessimistic in one respect: `parseStatement` and `parseDeclaration` are
   > table dispatches, so the stamp is one helper at two call sites, not a field on 64 node
   > interfaces — **98.2 % of 23,800 corpus nodes carry a span, 0 of them landing on a blank or
   > comment line**. The 421 without one are sub-blocks no chokepoint dispatches. The
   > `data-shape-id` hazard was avoided rather than fixed: nothing rides `Segment.tags`.
2. **Source→AST→source round-trip is impossible.** The IR is lossy with respect to the file: it
   drops comments, whitespace, and formatting. It is an **AST, not a CST**, in the sense
   Prettier's design turns on. Anyone reading "lossless round trip" in §8.1 must read it as
   *AST-object → JSON → AST-object*, never *file → JSON → file*.

   > **Correction (2026-07-29).** "Drops comments" is no longer true. `FileNode.comments` retains
   > every one — `{ text, line, column }` in source order, **24,971 across the four-repo corpus, of
   > which 0 are trailing** — so attachment collapses to "the run of comments directly above
   > `node.loc.line`". This does not make the IR a CST: whitespace and formatting are still gone,
   > and the `for`-unroll many-to-one span means the tree still cannot reproduce the file. But the
   > specific loss that mattered to *this* doc — the 239 lines of `# Construction:` prose across 32
   > of the 92 pattern files, which is the derivation narrative the worksheet is trying to
   > render — is recoverable now.
3. **This strengthens §3.1, not weakens it.** The derivation must come from authored source. The
   AST is the *evaluator's* view of authored source, and it has already thrown away the author's
   own prose account of the construction.

### 8.6 Versioning and publishing — and why the `qiyas-schema` pipeline is the wrong mirror

`packages/qiyas-schema/` is real, works, and is the obvious template. It is also **pointed the
other way**, and that asymmetry is the whole answer.

| | `packages/qiyas-schema` (exists) | A hypothetical `bikar-ast-schema` |
|---|---|---|
| Source of truth | **Python** — qiyas Pydantic models | **TypeScript** — `ast.ts` |
| Direction | schema → types | types → schema |
| Tool | `json-schema-to-typescript` (`scripts/codegen.mjs`, `compileFromFile`) | `ts-json-schema-generator` (the inverse tool) |
| Why a schema is needed | the producer is in **another language, in another repo** | the producer and every consumer are **the same TypeScript program** |
| Ships | real `schemas/*.json` + generated `src/*.ts`, exported as `"./schemas/*.json"` | — |
| Publishing | `@naqshcoffee/` scope, GitHub Packages, `access: restricted`, gated by `scripts/check-publish-config.js:17–23` | same, if it existed |

The pipeline exists because **a Python program and a TypeScript program must agree about a JSON
file on disk**. There is no cross-language, cross-process seam for the AST. The IR would be
generating a schema so that TypeScript could check TypeScript.

**The stronger in-repo precedent is the opposite mechanism.** `packages/core/src/contract-conformance.ts`
enforces the *existing* cross-repo contract at **compile time**, with no schema and no runtime
validator: it is a type-only module, never bundled, typechecked by `tsc`, and its own header states
the design intent — *"a divergence is a build failure, not a runtime surprise"*
(`contract-conformance.ts:13–14`). **bikar's established answer to "how do we stop two
representations desyncing" is a typecheck, not a schema.** For an artifact that never leaves the
TypeScript program, that answer already applies and is strictly cheaper.

**Decision: do not reuse the `qiyas-schema` pipeline, and do not publish an AST schema package.**
Rejected alternatives and why they lost:

- **Publish `@naqshcoffee/bikar-ast-schema` mirroring `qiyas-schema`** — rejected: no
  cross-language consumer (§8.2), and publishing creates a compatibility promise to nobody.
- **Fold the AST schema into `gt.json`'s version line** — rejected: `GT_SCHEMA_VERSION` versions a
  *post-evaluation result descriptor* (§8.1), a different artifact with a different lifecycle.
  Coupling them would force a GT bump on every `ast.ts` field addition and mislead qiyas, whose
  `schema.py:17` tracks GT 1.24 specifically.
- **Invert authorship — TypeBox or Zod v4, write schemas and derive TS types** — rejected: it
  makes a schema library a runtime production dependency of `bikar-core`, whose zero-runtime-dependency
  property is a recorded decision (`bikar/docs/decisions/2026-05-07-polygon-clipping-dep.md`, cited
  in §2.1). Buying a runtime dependency to serve zero consumers is not a trade.
- **`typia`** — rejected: it requires replacing `tsc` with the `ttsc`/`ttsx` toolchain repo-wide.
  Disproportionate for schema emission alone.

**If an IR is ever built, the versioning rule is:** its own line, `AST_SCHEMA_VERSION`, independent
of `GT_SCHEMA_VERSION` — the same independence §8.1 confirmed between bikar 1.24 and qiyas 1.22.
Additive field changes bump the minor; removing a field, renaming a `kind`, or narrowing a union
bumps the major. Note that **adding a new `Declaration` kind is a breaking change for consumers
even though it is additive for producers**, because a closed `anyOf` rejects it — the same
asymmetry §5.1's closing note already identified for E1's corpus floor.

### 8.7 Prior art: essentially nobody schemas an AST

Because §8.2's answer is "no consumers", the correct next question is whether the wider field
knows something that would change the calculus. It does, and it points the same way.

| Project | What it actually ships for its AST | Format | Purpose |
|---|---|---|---|
| **ESTree** | 11 Markdown files, no JSON, no conformance suite | prose + pseudo-IDL | docs |
| **`@types/estree`** | hand-written `index.d.ts` — explicitly *not* generated | TypeScript | compile-time types |
| **Babel** | `spec.md` + `defineType` validators in `.ts` source | imperative JS functions | runtime validation |
| **SWC** | nothing for the AST; its published JSON Schema covers `.swcrc` config only | — | — |
| **tree-sitter** | `node-types.json` | **bespoke JSON array**, no `$schema` | **codegen** |
| **Roslyn** | `Syntax.xml`, validated by `Syntax.xsd` | bespoke XML | **codegen** |
| **CPython** | `Parser/Python.asdl` | **ASDL**, a bespoke DSL | **codegen** |
| **Rust `syn`** | `syn.json` | bespoke JSON, no `$schema` | **codegen** of visitors |
| **LSP** | `metaModel.json`, described by `metaModel.schema.json` | bespoke meta-model | **codegen** of clients |
| **Clang** | `-ast-dump=json`, explicitly unstable, no schema | — | debug |

Three things fall out, and all three matter here:

1. **Not one of them ships a JSON Schema for AST instances.** Shipping a machine-readable AST
   *description* is common and well-trodden; shipping a JSON Schema that validates *trees* is
   done by nobody surveyed.
2. **Where JSON Schema or XSD does appear, it validates the definition file, not the trees.**
   Roslyn's `Syntax.xsd` validates `Syntax.xml`; LSP's `metaModel.schema.json` validates
   `metaModel.json`. The schema sits one level up, guarding the codegen input.
3. **The universal purpose is code generation** — tree-sitter's docs state it outright: the
   node-types data exists so *"you can use this data to generate type declarations in
   statically-typed programming languages."* bikar does not need that: `ast.ts` **is** the
   statically-typed declaration, hand-written and already canonical.

Babel is the sole runtime validator, and it validates with imperative functions rather than a data
schema — a considered choice by a project with far more incentive than bikar has. Clang goes
further and refuses to promise stability at all.

**This is counter-evidence to the proposal and it is recorded as such**, in the spirit of
Appendix B. If a schema-validated AST IR were the obvious right answer, ESTree — the most
consumed AST on earth, with dozens of independent implementations and a genuine cross-tool
interop problem — would have one. After a decade it ships Markdown.

### 8.8 Enforcement — reconciling with §5.1

§5.1 defines three mechanical gates (E1 prefix-sweep `fail=0`, E2 closed gloss vocabulary, E3
diagnostic-count baseline) and one governing principle: *extend the existing Stop hook, don't add
a second one.*

**Decision: the IR adds no gate. It would duplicate E1 while covering strictly less.**

The reasoning is §8.4's, made specific to §5.1:

- **A schema gate is strictly weaker than E1 on semantics.** E1 runs 1,139 real `evaluateFile`
  calls (§2.5). Of the nine semantic mutations in §8.4, the evaluator caught seven and the schema
  caught zero. Anything a schema gate would catch on `parse()` output is a violation of `ast.ts`'s
  own types, which `tsc` already rejects at build time.
- **It would not strengthen E1; it would sit upstream of it and pass unconditionally.** E1's
  measured floor is `fail=0` across 1,139 prefixes. Adding "…and each prefix AST validates against
  the schema" appends a check that is green by construction — a green light nobody can turn red is
  documentation wearing a gate's costume, which is precisely the failure §5.1 was written to
  prevent.
- **It violates the one-hook principle.** A schema gate needs the generated schema kept current,
  so it drags in a `codegen` step, a committed 88 KB artifact, and a staleness check —
  a *second* enforcement surface with its own conventions, for zero consumers.

**What is worth adopting from this section into §5.1's Phase 1 is much smaller, and is not a
schema.** §4.2's mechanism silently depends on the AST being a plain, cloneable data structure —
if a future `ast.ts` change introduced a class instance or a Map, prefix cutting via object spread
(`{ ...ast, declarations: prefix }`) could start sharing mutable state across steps and the
worksheet would go subtly wrong rather than loudly failing. That property is currently
**unasserted anywhere**. So:

> **E4 (proposed, cheap) — the AST stays plain data.** A vitest that parses the corpus and asserts,
> per file: no classes, Maps, Sets, Dates, RegExps, functions or cycles anywhere in the node graph;
> and `JSON.stringify` is a fixpoint after one pass. Measured baseline: **326/326 on both, across
> 55,701 nodes.** No schema, no generated artifact, no published package, no new hook — it rides
> the existing `npm test` → pre-commit → CI chain exactly as E1 does.

E4 buys the property §4.2 actually relies on, at roughly thirty lines. **The schema buys the
property nothing relies on, at the cost of a generator, an 88 KB committed artifact, nine engine-file
JSDoc annotations for tolerable errors, and a version line.**

Note also that E4's assertion must be written the §8.1 way — comparing two serialized forms, never
`deepStrictEqual` against the raw parse output, which fails on all 326 files.

### 8.9 Decision, scope-outs, and phasing

**Decision: do not build a schema-validated JSON IR for the bikar AST. Not for v1, and not for the
worksheet at all.**

The case against, ranked by weight:

1. **Zero consumers.** Worksheet, qiyas, Lab and CLI were each checked in the tree and each turned
   out not to want it (§8.2).
2. **It would be a tautology.** Validating `parse()` output against a schema generated from
   `ast.ts` can only fail if `tsc` failed (§8.4).
3. **It validates shape, never meaning** — 9/9 semantic corruptions pass, 2 of them silently
   through the evaluator too (§8.4).
4. **Essentially nobody in the field does this**, and the ones with the strongest incentive
   (ESTree, Babel, Clang) declined explicitly (§8.7).
5. **bikar's own answer to this class of problem is a typecheck**, already shipping in
   `contract-conformance.ts` (§8.6).

**What the research does *not* support:** it does not say the AST is unsuitable as an IR. §8.1 and
§8.3 say the opposite — it is unusually clean data, and a correct 80-definition schema generates
from the real `ast.ts` on the first attempt with no engine changes and validates 326/326. **The
proposal fails on demand, not on feasibility.** That distinction matters, because it means the
answer flips the moment a consumer appears, and nothing needs to be re-derived when it does.

**Scope-outs, explicit:**

- **No `ast.ts` modification.** Not source spans, not `@discriminator` JSDoc tags, not
  `exactOptionalPropertyTypes`. §4.7's no-engine-file rule extends here.
- **No committed generated schema**, and no `schemas/*.json` in any package.
- **No new npm package, and no publishing.** `scripts/check-publish-config.js` is not extended.
- **No `AST_SCHEMA_VERSION` constant.** Naming a version line for an artifact that does not exist
  invites something to depend on it.
- **No `--format ast` CLI surface.** That is the cheapest possible way to mint an external
  consumer by accident and thereby manufacture the demand this section found absent.
- **No promotion of the existing `bikar parse` dump.** It already prints AST-as-JSON
  (`packages/cli/src/index.ts:571`), and it stays exactly what it is: an unversioned debug aid
  whose consumer is a human reading stdout. It is deliberately **not** documented as an
  interchange format, given no version constant, and not schema-checked. Note the asymmetry this
  creates: it is the one surface where a schema *would* attach if demand ever appeared, so if
  something starts parsing that output, the Phase-1 trigger below has fired.
- **No claim about the parse failure.** `girih-star4.bkr` is a pre-existing sacred-patterns issue,
  reported here and not investigated.

**Phasing — trigger-gated, not scheduled.** Nothing below is on a timeline; each phase is unlocked
by a named event, and if the event never occurs the phase never happens.

| Phase | Do it when | What it is |
|---|---|---|
| **0 — now** | unconditional, ~30 lines | **E4** (§8.8): assert plain-data + stringify-fixpoint over the corpus. No schema. |
| **1** | a **second process** needs an AST it did not parse itself — a worker, a cache, a `--format ast` request from a real caller | Generate the schema at build time from `ast.ts`, validate the corpus in CI. **Do not commit the schema; do not publish it.** Proven feasible: 122 ms compile, 0.44 ms/file. |
| **2** | a **non-TypeScript** consumer appears (a Python AST reader, a second producer) | Commit the schema, add `AST_SCHEMA_VERSION`, add the `@discriminator` tags for usable errors, mirror the `qiyas-schema` publishing shape (§8.6). Only at this point does the pipeline analogy hold. |
| **never unless separately justified** | — | Runtime schema validation of in-process `parse()` output. It is `tsc` with extra steps. |

**Q11 (new, belongs with §7). Does click-to-source require source spans in the AST, and does that
change the IR calculus?** §8.5 establishes that `ast.ts` carries no positions and the lexer
discards comments, so the §6 deferred item "click-to-source (both cheap)" is **wrong for bikar** —
it is an `ast.ts` + `parser.ts` change, not a recovery trick. If spans are ever added, the AST
grows a field on nearly every node, and *that* is the change that would most plausibly justify a
versioned IR, because spans are the first AST content a second process would want. *Resolved by:*
costing the span-threading change before promising click-to-source anywhere.

> **Q11 — RESOLVED 2026-07-29** by `docs/click-to-source-design.md`, and it resolved against the
> question's own framing. **Yes, spans are required; no, they do not change the IR calculus.**
> Spans land on ~1,405 statement and declaration nodes, not "nearly every node", via a +9/−2-line
> patch at two dispatch chokepoints — so the AST growth this question worried about does not
> happen, and the strongest remaining argument for a versioned IR is unaffected. §8's verdict
> (build E4, not the IR) stands unchanged.
>
> The question also assumed spans were the blocker. They are not: **38.9 %** of faces trace to
> exactly one line, and **1 of 186** statement-sources produces exactly one face, so the feature's
> real obstacle is that the honest answer is plural and there is nowhere to display it — the Lab's
> editor is a plain `<textarea>` by stated constraint (`bikar/packages/lab/src/editor.ts:3`), which
> cannot show more than one highlighted range. Recommendation carried forward: **add the spans and
> comment retention, do not build the feature.** Comment retention in particular is the
> highest-value-per-line change that investigation found, and it belongs to *this* doc, not that
> one — it answers §3.6b's "node labelling is the universal weak point" by recovering the 269 lines
> of hand-written `# Construction:` prose across 31 of 92 files that `lexer.ts:88` currently throws
> away. All 812 comment lines in the corpus are own-line with zero trailing comments, so Prettier's
> three-class attachment problem collapses to one class here.

---

## Appendix A — sources

Full detail, quotations, and access failures in
[`research/derivation-visualization-survey.md`](research/derivation-visualization-survey.md).

**CSG as a visual formalism**
- Requicha, "Representations for Rigid Solids," *ACM Computing Surveys* 12(4), 1980 — https://dl.acm.org/doi/10.1145/356827.356833 · PDF https://lvelho.impa.br/i3d14/modtec/p437-requicha.pdf
- Kirsch & Döllner, "OpenCSG: A Library for Image-Based CSG Rendering," 2005 — https://www.opencsg.org/data/csg_freenix2005_paper.pdf
- Rossignac, "Blist: A Boolean list formulation of CSG trees" — https://www.13thmonkey.org/documentation/CAD/rossignac98blist.pdf
- Fayolle & Friedrich, "A survey of methods for converting unstructured data to CSG models," arXiv:2305.01220 — https://arxiv.org/abs/2305.01220

**Implementations**
- OpenSCAD — https://github.com/openscad/openscad · architecture diagram https://github.com/openscad/openscad/blob/master/doc/OpenSCAD-csg.pdf · modifiers https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Modifier_Characters
- Manifold `src/csg_tree.h` — https://github.com/elalish/manifold/blob/master/src/csg_tree.h · debug API https://github.com/elalish/manifold/blob/master/bindings/wasm/lib/debug.ts · https://manifoldcad.org/docs/jsuser/
- JSCAD — https://github.com/jscad/OpenJSCAD.org
- FreeCAD `importCSG.py` — https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/OpenSCAD/importCSG.py

**Feature trees and timelines**
- SOLIDWORKS FeatureManager / rollback bar — https://help.solidworks.com/2024/english/SolidWorks/sldworks/c_featuremanager_design_tree.htm · https://help.solidworks.com/2016/English/solidworks/sldworks/c_rollback_bar.htm *(403 to direct fetch; indexed content only)*
- Fusion Timeline — https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-USE-TIMELINE *(503; indexed content only)*
- Onshape — https://cad.onshape.com/help/Content/PartStudio/features_and_parts_lists.htm
- FreeCAD Tree view / Dependency graph — https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Tree_view.md · https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Std_DependencyGraph.md
- Dassault, "CAD/CAM feature tree with manipulatable 3D miniatures," US6636211B2 — https://patents.google.com/patent/US6636211B2/en

**Node graphs**
- Houdini flags — https://www.sidefx.com/docs/houdini/network/flags.html
- Blender Geometry Nodes — https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/
- Sverchok Stethoscope / shortcuts — https://sverchok.readthedocs.io/en/latest/nodes/text/stethoscope.html · https://nortikin.github.io/sverchok/docs/user_interface/shortcuts.html
- TouchDesigner node viewers — https://docs.derivative.ca/Viewer
- OpenSCAD Graph Editor — https://github.com/derkork/openscad-graph-editor/blob/master/manual/manual.md

**Code-CAD provenance viewers**
- CQ-editor — https://github.com/CadQuery/CQ-editor
- jupyter-cadquery `replay.py` — https://github.com/bernhard-42/jupyter-cadquery/blob/master/jupyter_cadquery/replay.py
- CascadeStudio — https://github.com/zalo/CascadeStudio · https://zalo.github.io/CascadeStudio/
- Zoo Design Studio Feature Tree — https://zoo.dev/docs/zoo-design-studio/features/workspace/feature-tree
- ocp_vscode — https://github.com/bernhard-42/vscode-ocp-cad-viewer
- replicad — https://replicad.xyz/docs/intro
- Curv — https://github.com/curv3d/curv

**Instructions, exploded views, history visualization**
- Agrawala et al., "Designing Effective Step-By-Step Assembly Instructions," SIGGRAPH 2003 — https://graphics.stanford.edu/papers/assembly_instructions/assembly.pdf
- Li et al., "Automated Generation of Interactive 3D Exploded View Diagrams," SIGGRAPH 2008, DOI 10.1145/1360612.1360700 — https://www.wilmotli.com/pubs/li08exview3D.pdf
- Denning, Kerr & Pellacini, "MeshFlow," SIGGRAPH 2011 — https://gfx.cse.taylor.edu/projects/meshflow/meshflow_acm.pdf
- Grossman, Matejka & Fitzmaurice, "Chronicle," UIST 2010 — https://www.tovigrossman.com/papers/uist2010_chronicle.pdf
- Kurlander & Feiner, "Editable Graphical Histories," VL 1988 — https://kurlander.net/DJ/Pubs/VL88.pdf
- Heer et al., "Graphical Histories for Visualization," InfoVis 2008 — https://idl.cs.washington.edu/papers/graphical-histories/

**Proof and construction pedagogy**
- Lamport, "How to Write a 21st Century Proof," 2011/2012
- Byrne's Euclid (1847), Rougeux recreation — https://www.c82.net/euclid/ · https://www.c82.net/euclid/about/
- Euclidea — https://www.euclidea.xyz/
- GeoGebra Construction Protocol / Navigation Bar — https://geogebra.github.io/docs/manual/en/Construction_Protocol/ · https://geogebra.github.io/docs/manual/en/Navigation_Bar/

**Islamic geometric construction**
- Bonner, *Islamic Geometric Patterns*, Springer 2017, DOI 10.1007/978-1-4419-0217-7 — https://link.springer.com/book/10.1007/978-1-4419-0217-7 *(303 to auth; quotations from first-party PDF front-matter extraction)*
- Broug, *Islamic Design Workbook*, Thames & Hudson 2016 — https://thamesandhudson.com/islamic-design-workbook-9780500292426 · *Islamic Geometric Patterns* rev. ed. 2019 — https://thamesandhudson.com/islamic-geometric-patterns-9780500294680 *(broug.com 403 at every variant)*
- Necipoğlu, *The Topkapı Scroll*, Getty 1995/96 — https://www.getty.edu/publications/virtuallibrary/9780892363353.html *(301)*
- Kaplan, "Islamic Star Patterns from Polygons in Contact," GI 2005
- Bodner, "Hankin's 'Polygons in Contact' Grid Method…," Bridges 2008
- Met, "Islamic Art and Geometric Design" — https://www.metmuseum.org/learn/educators/curriculum-resources/islamic-art-and-geometric-design *(429; PDF undecodable)*

**HCI on CAD comprehension**
- Cheng, Olechowski & Zhou, "It's a Complete Haystack," CSCW 2025 — https://arxiv.org/abs/2508.05940 · DOI 10.1145/3757617
- Gonzalez et al., "Understanding the Challenges of OpenSCAD Users for 3D Printing" — https://arxiv.org/abs/2408.01796

**Layout**
- Reingold & Tilford 1981 — https://doi.org/10.1109/TSE.1981.234519 *(403)*
- Buchheim, Jünger & Leipert, GD 2002 — https://doi.org/10.1007/3-540-36151-0_32 *(303)*
- van der Ploeg, "Drawing non-layered tidy trees in linear time" — https://doi.org/10.1002/spe.2213 *(402 Payment Required)*
- Gansner et al., "A Technique for Drawing Directed Graphs" — https://www.graphviz.org/documentation/TSE93.pdf
- d3-hierarchy — https://d3js.org/d3-hierarchy/tree · ELK — https://eclipse.dev/elk/ · dagre — https://github.com/dagrejs/dagre

**Explorable explanations**
- Victor, "Explorable Explanations," 2011 — http://worrydream.com/ExplorableExplanations/
- *(Small multiples: `https://www.edwardtufte.com/notebook/small-multiples/` returned **HTTP 404**. All small-multiples material is secondary and no Tufte quotation is used anywhere in this design.)*

**ASTs as machine-readable artifacts — prior art (§8.7)**
- ESTree spec — https://github.com/estree/estree *(11 Markdown files; no JSON, no conformance suite)*
- `@types/estree` — https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/estree *(hand-written `.d.ts`, explicitly not generated)*
- Babel AST spec — https://github.com/babel/babel/blob/main/packages/babel-parser/ast/spec.md · `defineType` validators https://raw.githubusercontent.com/babel/babel/main/packages/babel-types/src/definitions/utils.ts
- SWC — AST-to-JSON-Schema request unimplemented, https://github.com/swc-project/swc/discussions/7728 *(the official `swc.rs/schema.json` covers `.swcrc` config only)*
- tree-sitter static node types — https://tree-sitter.github.io/tree-sitter/using-parsers/6-static-node-types.html · real file https://raw.githubusercontent.com/tree-sitter/tree-sitter-javascript/master/src/node-types.json *("You can use this data to generate type declarations in statically-typed programming languages.")*
- Roslyn `Syntax.xml` (codegen input, guarded by `Syntax.xsd`) — https://github.com/dotnet/roslyn/blob/main/src/Compilers/CSharp/Portable/Syntax/Syntax.xml
- CPython ASDL — https://raw.githubusercontent.com/python/cpython/main/Parser/Python.asdl
- Rust `syn` — https://raw.githubusercontent.com/dtolnay/syn/master/syn.json · https://docs.rs/syn-codegen *("every Syn release comes with a machine-readable description of that version of the syntax tree as a JSON file syn.json")*
- LSP meta-model — https://raw.githubusercontent.com/microsoft/vscode-languageserver-node/main/protocol/metaModel.json · its guarding schema https://raw.githubusercontent.com/microsoft/vscode-languageserver-node/main/protocol/metaModel.schema.json
- Clang AST JSON instability — https://github.com/dtolnay/clang-ast *("the specific fields associated with each node kind are expected to change over time in non-additive ways")*

**TypeScript → JSON Schema tooling and validators (§8.3, §8.6)**
- `ts-json-schema-generator` — https://github.com/vega/ts-json-schema-generator *(v2.9.0 run first-party against `bikar/packages/core/src/dsl/ast.ts`; `discriminatorType` is programmatic-`Config`-only and gated on a `@discriminator` JSDoc tag)*
- `typescript-json-schema` — https://github.com/YousefED/typescript-json-schema · https://www.npmjs.com/package/typescript-json-schema *(still maintained; no discriminator support; `--required` / `--noExtraProps` default to off)*
- typia — https://typia.io/docs/json/schema/ · https://github.com/samchon/typia *("You **must** use `ttsc` and `ttsx`. The stock `tsc`, `ts-node`, and `tsx` cannot apply the `typia` transform")*
- TypeBox — https://github.com/sinclairzx81/typebox · Zod JSON Schema — https://zod.dev/json-schema *(both invert authorship: schema first, TS type derived)*
- ajv JSON Schema support and drafts — https://ajv.js.org/json-schema.html · https://ajv.js.org/guide/schema-language.html · https://ajv.js.org/options.html *("draft-07 has better performance"; "BREAKING draft-2020-12 is not backwards compatible"; `discriminator` "is not enabled by default")*
- OpenAPI Discriminator Object — https://spec.openapis.org/oas/v3.1.0.html#discriminator-object *(not a JSON Schema keyword; "MAY act as a 'hint' to shortcut validation")*
- Python `jsonschema` — https://python-jsonschema.readthedocs.io/en/stable/ *(full Draft 2020-12/2019-09/7/6/4/3 support; ignores `discriminator` as an unknown keyword)*
- Pydantic JSON Schema — https://pydantic.dev/docs/validation/latest/concepts/json_schema/ *(emit-only: model → schema; no API builds a model from a schema)*
- `datamodel-code-generator` — https://raw.githubusercontent.com/koxudaxi/datamodel-code-generator/main/README.md *(the JSON Schema → Pydantic v2 build-time codegen path)*

**In-repo sources**
- `bikar/docs/decisions/2026-07-23-orb-kernel3d-ring-solidify-no-csg.md`, `.../2026-07-28-c2-ports-connect-assembly.md`, `.../2026-07-29-w2-wall-connectors-mounts.md`, `.../2026-05-07-polygon-clipping-dep.md`
- `bikar/docs/architecture.md`, `bikar/docs/language-reference.md`, `bikar/docs/dsl-metadata-contract.md`
- `bikar/packages/core/src/{dsl/evaluator.ts, dsl/construction-tree.ts, dsl/ast.ts, dsl/parser.ts, dsl/lexer.ts, graph/half-edge.ts, render/svg-renderer.ts, render/orb-view-renderer.ts, render/gt-emitter.ts, kernel3d/solidify-slabs.ts, contract-conformance.ts, index.ts}`
- `bikar/packages/qiyas-schema/{package.json, tsup.config.ts, scripts/codegen.mjs}`, `bikar/scripts/check-publish-config.js`, `bikar/packages/cli/src/index.ts`, `bikar/packages/lab/src/evaluate.ts`
- `qiyas/src/qiyas/schema.py`
- `3d-models/docs/decomposition-approach.md`, `3d-models/docs/w2-connector-design.md`, `3d-models/docs/c2-assembly-design.md`

---

## Appendix B — contested bets and why they stand

**B.1 Drawing geometry per step departs from every mainstream CAD tool.**
*Counter-evidence:* SOLIDWORKS, Fusion, Onshape and FreeCAD all show icon + name and move one
cursor into one shared viewport. Blender states the position explicitly: *"Complex data types
such as geometry or grids cannot be previewed this way."* The only per-node-geometry precedents
are a 2000 patent, TouchDesigner (a realtime engine that re-evaluates everything anyway), and
Dynamo's opt-in Watch3D.
*Why the bet stands:* those are **interactive editors**, where a shared viewport plus a cursor is
cheaper and the user can scrub. This is a **printed worksheet** — there is no cursor to move, and
the entire premise is side-by-side comparison. The correct precedents are Requicha's Figure 6
(*"A CSG tree and the solids represented by its subtrees"*), UCSG-Net's Figure 6, and Broug's
printed step diagrams. **But the bet is real and the survey's negative should not be softened:
if this ever becomes an interactive Lab panel, the mainstream-CAD design is probably right and
this one should be revisited.**

**B.2 Transforms as steps rather than as labelled arrows.**
*Counter-evidence:* the brief explicitly offered "named arrows" as an option, and it is
intuitive. *Why the bet stands:* Requicha 1980 puts rigid motions in **nonterminal nodes with
transformation leaves**, not on edges; every implementation checked bakes the matrix into the
leaf; and **no surveyed tool labels an edge with anything.** Choosing arrows would be inventing a
convention. §4.4 nonetheless allows an in-panel arc arrow as *decoration on the geometry*, which
is not the same thing as a labelled graph edge.

**B.3 Prefix re-evaluation rather than a recorded trace.**
*Counter-evidence:* it is O(n) evaluations rather than one, it produced a measured 10 s worst
case, and it cannot see inside tile blocks or `rotate` bodies (§2.6.3) — a recorded trace
could. *Why the bet stands:* it needs **zero engine changes**, works through the existing public
API, was measured at **0 failures across 1139 prefixes**, and the survey's own ranking puts
evaluator instrumentation at the invasive end (jupyter-cadquery's source warns against leaving
its `__getattribute__` hook enabled). The cost is bounded and cacheable; the invasiveness of the
alternative is not. **If Q4 shows V7 firing on most files, this bet weakens substantially.**

**B.4 A mechanical walk is presented alongside hand-authored tutorials it does not replace.**
*Counter-evidence:* `patterns/Petal Tutorial/` exists, 31 of 92 files carry hand-written
`# Construction:` blocks, and §3.1 establishes that the derivation is an editorial choice. A
mechanical prefix walk recovers the sequence the file *literally specifies*, which is not
necessarily the sequence a teacher would choose. *Why the bet stands:* the mechanical version
regenerates when the file changes and the hand-authored one does not, and §4.5's grouping
delegates the editorial judgment back to the author via `wave` / `layer` tags. **But this is
genuinely unresolved: a worksheet that is faithful and pedagogically worse than the hand-made one
is a real possible outcome, and no validator in §5 catches it.**

**B.5 Linear small multiples rather than a tree or DAG layout.**
*Counter-evidence:* §10 of the survey assembles the full layout literature, FreeCAD needed a
second DAG view specifically for *"locating forks in a tree,"* and Requicha's own footnote 7
concedes *"the representations are graphs rather than trees."* *Why the bet stands:* prefix
re-evaluation produces a **sequence**, not a tree — there is no fork to draw. A tree layout would
be depicting structure the mechanism does not recover. Also: Sugiyama-family layouts are
non-deterministic across small input changes, so the sheet would rearrange on every edit, which
is bad for an artifact meant to be re-read. **If Q4 is resolved by extending into tile blocks and
bodies, nesting appears and this decision must be revisited.**

**B.6 Only two set-notation glosses survive the honesty rule.**
*Counter-evidence:* a "visual math worksheet" that contains almost no math symbols may read as
under-delivering on the brief's framing. *Why the bet stands:* the alternative is labelling
`clip` with `∖`, which would tell the reader bikar has boolean difference. It does not — `clip`
partitions and annotates, removing nothing. Q8 leaves open whether two symbols are better than
zero, but never whether a wrong symbol is acceptable.

**B.7 Declining the AST JSON IR, when it demonstrably works.**
*Counter-evidence:* this is the bet with the strongest counter-case in the doc, because the
proposal was **tested and it passed**. A correct 80-definition, 9-of-9-tagged schema generated from
the real `ast.ts` on the first attempt, with no engine change; 326/326 corpus files validate at
0.44 ms each; the AST contains zero non-JSON-safe values across 55,701 nodes (§8.1, §8.3). "It
would work and it is cheap" is a genuine argument, and the Phase 1 trigger in §8.9 could plausibly
fire — the moment anyone wants a worker, a cache, or a Python-side AST reader.
*Why the bet stands:* feasibility is not demand. Every candidate consumer was checked in the tree
and none wants it (§8.2); validating `parse()` output against a schema derived from `ast.ts` can
only fail if `tsc` failed (§8.4); 9 of 9 semantic corruptions pass the schema, two of them silently
through the evaluator as well; and the field's most incentivized projects — ESTree, Babel, Clang —
looked at this and declined (§8.7). **But the falsifier is cheap and named: if a second process
ever needs an AST it did not parse itself, §8.9 Phase 1 unlocks and this bet is simply over.**
The section is written so nothing has to be re-derived when that happens.
