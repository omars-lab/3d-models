# Design: producing `cached_coords` for arc-bearing construction imports

> Status: decided 2026-09-21 (D-080). Consumer: bikar `import geogebra`. Producer:
> undecided until this doc — it replaces the deferral in the youtube design doc
> construction-ast-export.md §cached_coords ("P1.2b's GgbAPI dump"), which named a
> producer but never chose or built one.
>
> Grounded on a live probe run this session against the bikar arc-importer branch
> (PR #234): the AST for construction nmEjCTzMbDg was produced with the youtube
> `make ast` target and fed to `bikar import geogebra … --coverage`. Cross-repo
> and not-yet-merged code is cited by PR number, not by line pointer, because the
> anchor cannot resolve until the PR lands.

## 1. The problem, and why it is a real one

A GeoGebra `CircularArc(centre, start, end)` sweeps counter-clockwise from `start`
to `end`. Depending on where the two endpoints sit on the circle, that CCW sweep is
either the **minor** arc (< 180°) or the **major/reflex** arc (> 180°). The bikar
importer decides which by measuring the actual sweep from the endpoints'
coordinates, and **refuses rather than guesses** when no coordinates are present —
the "never guess the arc" rule (bikar PR #234; the K1/K10 discipline this repo's
CLAUDE.md enforces). This is correct: nmEjCTzMbDg's three scallops are all major
arcs, and a guess would silently draw the wrong inward-bulging arc.

So an arc-bearing construction cannot be imported without a `cached_coords` map —
`{ label: [x, y] }` for at least the arc endpoints. The plumbing to *feed* that map
already exists (youtube `ggb_build.py --ast-json --cached-coords`). What has never
existed is anything that *produces* it. The five constructions migrated so far
(rDuxHF3xMOc, sDO9fpu76v8, n3IidKfXE1I, lEfWSogWscs, tA8eSdVx_EQ) use no arcs, so
their fixtures carry `cached_coords: {}` and never needed a producer. nmEjCTzMbDg is
the first arc-bearing migration and the first to need one.

**Probe result (this session):** on the PR #234 branch, nmEjCTzMbDg imports cleanly
for every statement *except* its three `CircularArc` lines, which fail only with the
by-design "needs coordinates" refusal because the AST was produced with an empty
`cached_coords`. Reflect-across-a-point (bikar PR #230), the parabola/hyperbola loci
(#232), circle inversion (#231) and `Sequence(Rotate({…}))` (#227) all lower
silently. **The bikar engine is complete; the only missing input is coordinates.**

## 2. How each option is evaluated

Options are not scored on cost alone. Each is put through the same questions — the
ones a careful review of alternatives should always ask:

1. **Is there a dominating variant?** Before accepting an option's worst framing,
   look for a version that keeps its benefit and drops its biggest cost. (This is
   what turned "rebuild a geometry engine" into the far cheaper self-bootstrap.)
2. **Pros / cons / downstream implications** — what it buys, what it costs, and
   what it commits us to or rules out next.
3. **Short-term challenges** — what breaks or blocks *this quarter*, including
   spike risk on anything marked "unverified".
4. **Long-term ownership** — does it make sense to *own* this capability rather
   than depend on someone else's, and does the option move us toward or away from
   that? Build-vs-reuse is a strategic axis, not only a cost one.
5. **What it verifies** — an option that checks nothing against ground truth is
   named as such.

## 3. The options

### Option A — reuse GeoGebra: headless GgbApplet / GUI coords dump

Drive GeoGebra itself to compute the construction, then read coordinates back
through its scripting API (`getXcoord`/`getYcoord`). This is the producer the
youtube doc named ("GgbAPI dump").

- **Dominating variant?** No cheaper faithful variant found — reading GeoGebra's own
  numbers requires running GeoGebra.
- **Pros:** GeoGebra stays the single source of truth for coordinates; its numbers
  are faithful to the source by definition. Reusable for every future construction.
- **Cons:** couples the coords pipeline to a GeoGebra runtime forever; two engines
  in the loop (GeoGebra computes, bikar renders) can disagree numerically.
- **Short-term challenges:** the headless GgbApplet path is *unverified* (GeoGebra
  Classic 5 is a Java Swing app with no documented headless mode; youtube's
  geogebra-applescript-automation.md is still "Status: design"). If it will not run
  without a display, the fallback is macOS GUI automation — a logged-in Mac only, no
  CI, no SSH, and menu-clicking that breaks on a GeoGebra version bump. A spike could
  burn time only to land on the fragile fallback.
- **Long-term ownership:** moves *away* from owning the capability — it entrenches a
  third-party desktop dependency at the centre of the pipeline.
- **Verifies:** faithful to GeoGebra, but *not* necessarily to what bikar renders.

### Option B — build a standalone geometry engine

Write a new evaluator that replays the ggb-commands (points, conics, intersects,
reflections, inversions) and computes coordinates from scratch, no GeoGebra.

- **Pros:** portable, headless, CI-able; no GeoGebra dependency.
- **Cons:** a second geometry engine to build and keep faithful to GeoGebra's exact
  conventions — intersect-index ordering, conic branch, CCW sense. Divergence on one
  index yields a plausible-but-wrong point and the wrong arc, silently (a textbook
  K10 porting hazard).
- **Short-term challenges:** largest build of the four; correctness burden never
  fully retires.
- **Long-term ownership:** owns the capability, but at the price of duplicating and
  perpetually re-validating GeoGebra's numeric semantics.
- **Verdict: rejected.** "If B means rebuilding GeoGebra, go with A" (owner,
  2026-09-21). B as a *from-scratch* engine is exactly that rebuild.

### Option B′ — reuse **bikar's own** engine (self-bootstrap)

The dominating variant of B, found by asking question 1. The arc *endpoints* are all
computed by statements **upstream** of the arcs — verified against the construction:
`B` (free point), `I` (Midpoint), `L`/`O` (Intersect with index), `M`/`P`
(ClosestPoint), `I'`/`M'`/`P'` (Reflect across a line) are defined before the three
`CircularArc` lines. Every one of those primitives bikar already lowers *and*
evaluates. So:

```
import geogebra <ast>  --lenient e_1,f_1,g_1   → a .bkr with the 3 arcs deferred
   → bikar evaluates it → read back the 9 endpoint coords
   → write cached_coords → re-import geogebra <ast>  (no --lenient)  → full .bkr
```

- **Dominating variant?** This *is* it — it keeps B's "own the capability" benefit
  and drops B's whole cost, because the engine already exists and has been taught
  every primitive these constructions use.
- **Pros:** no GeoGebra runtime; headless and CI-able; **self-consistent** — the
  coords come from the very engine that will render the coaster, so the arc
  major/minor decision is correct *for bikar's own geometry* by construction (see §5).
- **Cons:** needs one small new bikar output — an evaluated-points/coords dump.
  bikar has no such format today (its `--format` set is svg, stl, views, timelapse,
  parts, ldraw). The evaluator already computes point positions, so this is a thin
  CLI addition, not engine work.
- **Short-term challenges:** the coords dump must be built and land in a bikar PR
  before nmEjCTzMbDg's fixture can be produced the general way; one faithfulness
  check against a render is prudent (§5).
- **Long-term ownership:** moves *toward* owning the capability — and we are already
  most of the way there. Each migration has taught bikar another GeoGebra primitive
  (sequences, conics, inversion, point-reflection, arcs). B′ is the natural next
  increment, after which GeoGebra leaves the coords/transpile loop entirely (it stays
  only as the reconstruction-time reference that scores renders against the video —
  a different job, and one that is inherently the source's ground truth, not ours).
- **Verifies:** faithful to *bikar's* rendered geometry, which is what the coaster
  is cut from.

### Option C — compute nmEjCTzMbDg's coords once, now

Produce just this construction's arc-endpoint coords once and stage a working PR-5
draft, deferring the general producer. Implemented via **B′'s mechanism** (`--lenient`
+ a coords readback), so it doubles as the first proof of B′.

- **Pros:** cheapest path to seeing the whole chain work end to end (import → base →
  coaster → goldens → O1/O2/O3), and it validates B′ on a real construction before
  we commit the general build.
- **Cons:** not reusable on its own; the general producer still has to be built.
- **Short-term challenges:** none beyond the readback itself.
- **Long-term ownership:** neutral — a stepping stone, not a commitment.
- **Verifies:** the full pipeline, on one construction.

## 4. Decision (D-080)

- **Immediately, to unblock PR-5 (nmEjCTzMbDg):** Option **C**, implemented via B′'s
  `--lenient` mechanism — produce the coords now and stage the migration draft. This
  also serves as B′'s first proof.
- **As the general producer:** Option **B′** — add a small evaluated-coords output to
  bikar, then generate `cached_coords` by self-bootstrap. Chosen because it owns the
  capability with our existing engine, drops GeoGebra from the coords loop, and is
  self-consistent with the render target (§5).
- **Fallback:** Option **A**, documented but not built.
- **Rejected:** Option **B** (from-scratch engine).

**Reversal condition:** if bikar's evaluated endpoints prove *not* geometrically
faithful to the source — e.g. an intersect-index or conic-branch convention in bikar
picks a different root than GeoGebra, so a render fails its O2/O3 video-fidelity
check for a reason traced to a wrong endpoint — fall back to Option A for that class
of construction and record why here.

## 5. Why B′ is at least as faithful as A here

The arc major/minor choice is a **topological** decision (sweep >or< 180°), robust to
small numeric error. The failure that would matter is picking the *wrong endpoint*,
not a slightly-off one. Option A guards against that by trusting GeoGebra; B′ guards
against it differently and, for our pipeline, more directly:

- B′'s coords are the coords bikar will **render** from. So the arc direction bikar
  picks is correct *for the geometry bikar actually cuts*. A coords/render mismatch
  is impossible by construction.
- Option A's GeoGebra coords could disagree with bikar's rendered points (two
  engines), and then A picks an arc direction right for GeoGebra but wrong for
  bikar's slightly-different endpoints.
- Whether bikar's endpoints match the *video* is already gated downstream by the
  reconstruct O2/O3 render-vs-keyframe checks — the same gate that validates every
  migration. B′ adds no new unchecked surface.

## 6. Consequences and follow-up

Tracked as tasks (see the session task list):

- **Bikar: evaluated-coords output.** A `--format`/verb that dumps `{ label: [x, y] }`
  for evaluated points. Own PR off bikar main.
- **nmEjCTzMbDg PR-5 via B′/C.** Produce the coords, build fixture → base → coaster →
  goldens → O1/O2/O3, then the 3d-models vendoring PR. Gated on bikar #234 merging.
- **Option A stays documented here as the fallback**, un-built.

This decision graduated a reusable tenet — the five evaluation questions in §2 —
recorded in the design-note skill and in session memory, so the next options review
asks them by default.
