# The orb pipeline, source to badge

**Status:** Living map · **Date:** 2026-08-17 · **Repos:** bikar (construct + emit),
qiyas (validate), 3d-models (publish)

One `.bkr` file becomes a printable STL, a set of per-axis SVG views, a ground-truth
JSON, a score, and a badge in the Lab. That path crosses three repositories, and no
single repo's docs own it: [`orb-lab-design.md`](orb-lab-design.md) describes the
product end, bikar's `docs/architecture.md` the engine end, and
[`qiyas-wheelfield-validation-design.md`](qiyas-wheelfield-validation-design.md) the
scoring end. This file is the seam between them — the picture a reader needs before
any of the three make sense.

## What this document claims, and how the claims are checked

A diagram full of code pointers is a document full of things that can quietly stop
being true. This repo has already measured that failure: on 2026-08-02, 23 of 44
use-case pointers had drifted while every run reported *"all valid"*
([D-020](decisions-log.md)). So the split here is deliberate:

- **The diagram is for orientation.** Its nodes name stages and functions. It carries
  no line numbers and no `click` URLs, because nothing in this repo can check either.
- **The table under each lane is the truth.** Every path in it is a backticked,
  repo-qualified pointer of the form `bikar:packages/core/src/kernel3d/weld.ts`, which
  is exactly the form `.claude/gates/doc_pointers.py` resolves against the sibling
  checkouts on every commit and on `make validate-pointers`. A file that moves or is
  deleted fails the gate here.

**No third pointer form was invented for this document.** Line-level anchors of the
form the use-case map uses are checkable too, but they pin a *literal* at a line, and
a diagram that names a stage does not have a literal to pin — the honest unit here is
the file.

What the diagram therefore does **not** assert: that the stages shown are the only
stages, or that a named function is the only entry point into its module. It shows the
path an orb actually takes, at the granularity where the names are stable.

## The map

```mermaid
flowchart TB
  SRC["Star-Orb.bkr<br/>one pattern decl<br/>plus one orb decl"]

  subgraph BC["bikar — construct"]
    direction TB
    B1["lexer, parser, AST"]
    B2["evaluate the pattern decl<br/>the existing 2D engine,<br/>reused unchanged"]
    B3["buildOrbBase<br/>Platonic solid<br/>plus geodesic subdivision"]
    B4{"which family?"}
    B5["Family 2 — pierced lattice<br/>solidifyLattice"]
    B6["Family 1 — woven ribbons<br/>weaveLattice"]
    B7["Family 3 — maclado field<br/>buildWovenOverlapGraph"]
    B8["inside each: lift into the<br/>face-local frame, weld shared<br/>vertices, project to the sphere"]
    B9["manifold gate<br/>watertight, euler, volume"]
    B1 --> B2 --> B4
    B1 --> B3 --> B4
    B4 -->|"no weave"| B5
    B4 -->|"weave"| B6
    B4 -->|"base wheelfield"| B7
    B5 --> B8
    B6 --> B8
    B7 --> B8
    B8 --> B9
  end

  subgraph BE["bikar — emit"]
    direction TB
    E1["mesh-emitter<br/>binary STL"]
    E2["orb-view-renderer<br/>one SVG per symmetry axis"]
    E3["gt-emitter<br/>one gt.json per view"]
    E4["mesh-gate<br/>runs on --check"]
  end

  subgraph QV["qiyas — validate"]
    direction TB
    Q1["discover_views<br/>pair each SVG with its gt"]
    Q2["rasterize, then the<br/>encode stages"]
    Q3["reconcile<br/>bucket candidate shapes"]
    Q4["Hungarian match<br/>against the gt"]
    Q5["structural, geometric,<br/>symmetry, drop, max_drift"]
    Q6["per-view composite,<br/>then the mean"]
    Q1 --> Q2 --> Q3 --> Q4 --> Q5 --> Q6
  end

  subgraph HN["holding the number"]
    direction TB
    H1["sweep-orb-validate<br/>the measuring half"]
    H2["orb-composites.test.ts<br/>the comparing half<br/>RECORDED_DROP, MAX_DRIFT_CEILING"]
    H3["scripts.ts qiyasComposite<br/>the recorded number"]
    H4["the Lab trust badge"]
    H5["3d-models gallery<br/>make orbs, make deploy"]
    H1 --> H2
    H3 --> H2
    H2 --> H4 --> H5
  end

  SRC --> B1
  B9 --> E1
  B9 --> E2
  B9 --> E3
  E1 --> E4
  E1 --> H5
  E2 --> Q1
  E3 --> Q1
  Q6 --> H1
  H2 -.->|"a widened drop or drift<br/>fails the build"| SRC
```

### Reading the two edges that surprise people

**`gt-emitter` is on the bikar side.** The ground truth qiyas scores against is a
*product of the engine*, not an input qiyas brings. bikar states what it drew; qiyas
independently encodes the picture and the two are compared. Read the other way round —
as though qiyas held the answer key — the whole arrangement looks circular, and it is
the single fact readers get wrong most often.

**The dashed edge back to the source is what makes this a system.** `sweep-orb-validate.ts`
measures, `orb-composites.test.ts` compares that measurement against the number recorded
in `scripts.ts`, and a divergence fails the build. Without that edge this is a pipeline
that produces a number nobody is accountable to; with it, a geometry change that quietly
degrades a score cannot merge. Its own docstring calls the re-run *"a tripwire"*.

## Lane 1 — bikar, construct

| stage | pointer |
|---|---|
| declaration dispatch | `bikar:packages/core/src/dsl/evaluator.ts` |
| base solid, subdivision, duals | `bikar:packages/core/src/kernel3d/polyhedra.ts` |
| face-local 2D ↔ 3D frame | `bikar:packages/core/src/kernel3d/face-frame.ts` |
| vertex weld | `bikar:packages/core/src/kernel3d/weld.ts` |
| Family 2 — pierced lattice | `bikar:packages/core/src/kernel3d/solidify-lattice.ts` |
| Family 1 — over/under solve and ribbons | `bikar:packages/core/src/kernel3d/weave.ts` |
| Family 3 — maclado field | `bikar:packages/core/src/kernel3d/maclado-field.ts` |
| Family 3 — welded woven overlap | `bikar:packages/core/src/kernel3d/maclado-woven.ts` |
| 2D over/under precedent the 3D solve reuses | `bikar:packages/core/src/kernel/strapwork.ts` |
| void polygons the lattice pierces | `bikar:packages/core/src/graph/face-extractor.ts` |

The branch at `B4` is a real fork in `evaluator.ts`, not a diagram convenience: a
`weave` statement routes to the ribbon path, a `base wheelfield` declaration routes to
a separate evaluator that never touches `inscribe` at all, and the absence of both
falls through to the pierced lattice.

`B8` is drawn as one node because all three solidifiers do the same three things —
each imports `makeFaceLift` from `face-frame.ts` and constructs a `VertexPool` from
`weld.ts`. It is a stage *inside* each solidifier, not a stage between them, and the
diagram compresses that.

## Lane 2 — bikar, emit

| stage | pointer |
|---|---|
| binary STL | `bikar:packages/core/src/render/mesh-emitter.ts` |
| per-axis orthographic SVG | `bikar:packages/core/src/render/orb-view-renderer.ts` |
| symmetry axes and front-cap projection | `bikar:packages/core/src/kernel3d/orb-views.ts` |
| ribbon projection into a view | `bikar:packages/core/src/kernel3d/orb-ribbons.ts` |
| ground truth per view | `bikar:packages/core/src/render/gt-emitter.ts` |
| mesh gate behind `--check` | `bikar:packages/core/src/kernel3d/mesh-gate.ts` |
| the CLI that fans these out | `bikar:packages/cli/src/index.ts` |

The CLI's `--format` switch is where the fan-out is visible from a shell:
`--format stl` writes the mesh, `--format views` writes the SVG set. `--check` is what
turns the mesh gate on; without it an STL is emitted unexamined beyond the evaluator's
own watertight assertion.

## Lane 3 — qiyas, validate

| stage | pointer |
|---|---|
| view discovery, scoring, the gate | `qiyas:src/qiyas/orb_validate.py` |
| shape reconciliation and bucketing | `qiyas:src/qiyas/stages/detectors/reconcile.py` |
| SVG-side primitives | `qiyas:src/qiyas/stages/svg_primitives.py` |
| symmetry stage | `qiyas:src/qiyas/stages/symmetry.py` |
| the envelope both sides type against | `qiyas:src/qiyas/schema.py` |
| running CI locally when Actions cannot | `qiyas:docs/local-ci-runbook.md` |

`reconcile` earns its own node rather than folding into the encode stages, because it
is where the last validator defect lived: three bucketing gates that all read bounding
boxes and scalars could not tell *one region found twice* from *two regions either
side of a shared edge*, and two rosette orbs carried a shortfall for three weeks that
was qiyas's, not bikar's ([D-035](decisions-log.md)).

Note what `Q5` implies about reading a single number. `geometric` is not monotone in
the input — an element moving further away can raise it — which is why `drop` sits
beside it and why the per-view gate counts rather than tolerances. The composite alone
also cannot see shape *type*, so a run can score 1.000 with most bands encoded as the
wrong primitive. Both facts are recorded at the definitions above; the diagram cannot
carry them, which is the honest limit of a diagram.

## Lane 4 — holding the number

| stage | pointer |
|---|---|
| the sweep that measures | `bikar:scripts/sweep-orb-validate.ts` |
| the test that compares | `bikar:packages/lab/tests/orb-composites.test.ts` |
| the recorded composites | `bikar:packages/lab/src/scripts.ts` |
| the build target that publishes | `3d-models:Makefile` |
| the gallery design | [`orb-lab-design.md`](orb-lab-design.md) |

`sweep-orb-validate.ts` will not guess where qiyas comes from: it requires either a
pinned container image or an explicit sibling checkout, because *"a sweep against a
pinned qiyas and a sweep against working-tree qiyas are different claims."* That
refusal is the reason the recorded numbers mean something.

## What this map deliberately does not draw

- **Any number.** Composites, drops and drift ceilings live in the files above and in
  [`decisions-log.md`](decisions-log.md), where a change to one is a reviewed edit. A
  number copied into a diagram is a number with no owner — the failure this repo
  withdrew a printer-accuracy figure over.
- **The 2D pattern engine's internals.** `B2` is a single node standing for the whole
  girih/hankin/star/rosette evaluation, which the orb work reuses unchanged. It is
  bikar's `docs/language-reference.md` and `docs/architecture.md` that decompose it.
- **Open defects.** As of this date, two views in the sweep are surplus to the gt and
  the composites carry a recorded shortfall rather than a clean 1.000 across the set.
  That is a state, not a stage; it belongs in the tracker and the decisions log, and
  drawing it here would make the map wrong the moment it is fixed.
- **The CI wiring.** Which workflow runs which half is the subject of
  `qiyas:docs/local-ci-runbook.md`, which covers all three repos and changes on a
  different clock than the geometry does.
