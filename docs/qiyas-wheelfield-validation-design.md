# qiyas 3D validation for the wheelfield family — design doc

Status: **v2 — Q0–Q6 all done, and the two follow-ons Q4 spawned with them.**
Q1 (cell views) merged as bikar `fe6a86c`; Q2 (ribbon views) as bikar PR #96;
Q3 (the qiyas audit fixes) as qiyas PR #11; Q6 as bikar PRs #97 and #98, with
#99 clearing the e2e flake that blocked them ([D-034](decisions-log.md)). Q4's
measurement is §7.1 and it changed the plan — it fired §7's validator and made
the composite threshold this doc was going to record unrecordable, adding Q4a
and Q4b in its place. **Q4a** shipped as qiyas PR #15, exposing `drop` and
`max_drift`. **Q4b** shipped as bikar PR #102 (`6157792`) and *inverted its own
premise*: measured against real renders the acceptance radius needed no scaling
at all, so no constant changed and the gate became a count instead (§7.1).
**Q5** shipped as bikar PR #100 (`5349a80`) — see §8 for what its first sweep
found. Q6's composites, which this line recorded as staying `null` "until Q5's
job records one", are recorded: `maclado-9` cells **1.000**, `maclado-9-weave`
**1.000** on both drawings, `maclado-9-overlap` ribbons **1.000** with
`cells: null` left standing as the geometry answering rather than a missing run.
Read those 1.000s with the hedge bikar's own registry comment carries: the
composite matches shapes by centre and scores position and area, it does not
read `type`, and the claim that these views are *typed* correctly is carried by
the histogram in `bikar:packages/lab/tests/orb-composites.test.ts`, not by these
numbers. §6's non-goal is unchanged and load-bearing — none of this verifies
weave parity. Direction taken by the user
on 2026-08-15, after a scoping pass presented four open questions: build **both**
representations (cell decomposition *and* stroked ribbons), cover **all three**
Maclado presets, **fix** the qiyas defects that make the ribbon representation
hard rather than route around them, and **build the CI wiring** that the
currently hand-transcribed composite scores only claim to have.

Scope: make the three shipped wheelfield orbs — `bikar:patterns/Orbs/Maclado-9.bkr`,
`bikar:patterns/Orbs/Maclado-9-Weave.bkr` and `bikar:patterns/Orbs/Maclado-9-Overlap.bkr`
— validatable by `qiyas orb-validate` in a way that measures *the object that gets
printed*, so that the three gallery cards can carry `lab:` links and a trust badge
on the same footing as the eleven classic orbs already in the Lab registry.

All engine facts below were read at two pinned revisions: bikar at
[`f3cb04c`](https://github.com/NaqshCoffee/bikar/commit/f3cb04c) (the merged M4e
commit) and qiyas at
[`3e547da`](https://github.com/NaqshCoffee/qiyas/commit/3e547da) (`main`). The
survey that produced them, with every `file:line` anchor and the in-memory
measurement run behind the numbers in §2 and §3, is checked in at
[`docs/research/qiyas-wheelfield-validation-survey.md`](research/qiyas-wheelfield-validation-survey.md).
Where this doc states a number as *measured*, it was measured once, by that run,
on deterministic geometry code; no tolerance sweep was performed on any of them.

---

## 1. Goals and non-goals

**Goals.**

1. Emit orb views for the wheelfield family that depict **the field bikar
   actually meshes** — 20 vertex-placed wheels — rather than a preview artifact.
2. Emit them in **two representations**, because they verify different things:
   **A**, a cell decomposition (closed filled polygons, the classic-orb shape of
   evidence); **B**, stroked ribbons with over/under grouping, which is the only
   representation in which a weave is visibly a weave.
3. Make qiyas score both honestly: audit the parser and scorer defects that a
   stroke-heavy SVG walks into, fix them with a failing-first test each, and add
   fixtures for both representations.
4. Measure the scorer's transfer conditions **before** porting the classic-orb
   pass threshold to a dense lattice (§7).
5. Replace the hand-transcribed composite sweep with a job something runs.
6. Surface the three presets in the Orb Lab registry and link them from the
   gallery cards.

**Non-goals, and one of them is load-bearing.**

- **This will not verify weave parity.** No representation proposed here lets
  the qiyas scorer distinguish a correct over/under assignment from an incorrect
  one; §6 says why, and names what does hold the parity claim instead. A reader
  who takes a passing composite as evidence that the weave is right has read it
  wrong, and that sentence belongs in the badge tooltip as much as in this doc.
- Not a rewrite of the qiyas scorer into a topology-aware instrument. The
  defects in §5 are parser and bookkeeping defects with a defined correct
  behaviour; "score a lattice the way a topologist would" is not one of them.
- Not a physical print milestone. No `CAL-*` bet is opened by this work, and no
  number here is a print tolerance.
- Not a change to the classic-orb path. Every classic orb must score exactly
  what it scores today; §8 makes that a milestone exit condition rather than an
  assumption.

---

## 2. The load-bearing result: the qiyas half is mostly a bikar half

The scoping question was "what does qiyas need in order to validate the maclado
orbs". The answer measured at the two pinned revisions is that qiyas already
runs on them, end to end, and produces a number — and the number is about the
wrong object.

The wheelfield evaluator branch does set an `orb3d` on the result, so the CLI's
`--format views` path is family-blind and emits the same three axis files with
the same attribute trio and the same ground-truth envelope it emits for a
classic orb. What it projects, though, is `result.faces`, and for a wheelfield
declaration `result.faces` is a synthesized 2D preview of **one flat wheel**
(`bikar:packages/core/src/dsl/evaluator.ts:1373-1392`), which the view path then
lifts onto **each of the 12 dodecahedron faces**
(`bikar:packages/core/src/kernel3d/orb-views.ts:165-166`). The meshed object is
**20 wheels placed at dodecahedron vertices**
(`bikar:packages/core/src/kernel3d/maclado-field.ts:92-96`). Twelve copies of a
preview of one wheel is not a picture of twenty wheels, and the wheel is
authored on a 9-fold circumradius that a pentagon's 72° corners cannot contain,
so the lifted copies overrun their faces.

Three measurements make the consequence concrete, all from the single in-memory
run recorded in the research file:

| | Maclado-9 | Maclado-9-Weave | Maclado-9-Overlap | Star-Orb (classic) | Weave-Orb (classic) |
|---|---|---|---|---|---|
| polygons per view (vertex/face/edge) | 66 / 68 / 63 | — (face-5: 68) | — (face-5: 68) | 55 / 55 / 60 | 40 / 40 / 44 |
| interpenetrating projected polygon pairs | 8 / 9 / 8 | same | same | 0 / 0 / 0 | 0 / 0 / 0 |
| face-5 SVG SHA-256 | \-\-\- identical across all three presets \-\-\- | | | n/a | n/a |

- **The three presets are byte-identical in view.** Same SHA-256 over the
  rendered face-5 SVG. The views are blind to `weave`, to `overlap`, to
  `amplitude` and to ribbon width and depth; the only view-visible knobs are
  radius and the wheel's point count and contact. A composite recorded against
  these could not tell a rigid shell from a weave from a woven overlap.
- **The views are not honest 2D.** Eight to nine projected polygon pairs
  interpenetrate per view, all spanning different base faces, drawn in
  construction order with opaque fills and no depth resolution of any kind.
  `OrbViewPolygon.minDot` is computed and never read by any consumer. The
  classic orbs measured zero such pairs on every axis, which is why the
  whole-face front cap has been sufficient for them and is not sufficient here.
- **Every semantic channel is empty**: no face colours, no face classes, no
  source primitives, `face_class` / `shape_id` / `authored_region` all null.

So the work in front of us is roughly: one large bikar milestone to make the
views true (Q1), one more to make a ribbon representation exist at all (Q2), one
qiyas milestone to make the ribbon representation scoreable (Q3), and then
measurement, wiring and surfacing (Q4–Q6). The qiyas defects are real and are
fixed here, but they are the *second* obstacle, not the first.

---

## 3. What the two engines do today

### 3.1 bikar's orb view path

Projection is `projectOrbView` in `bikar:packages/core/src/kernel3d/orb-views.ts`,
SVG is `renderOrbViewSVG` in `bikar:packages/core/src/render/orb-view-renderer.ts`,
and ground truth is `emitOrbViewGroundTruth` in
`bikar:packages/core/src/render/gt-emitter.ts`, all sharing one `OrbViewScene`
so the two emitters cannot disagree. View axes are derived from element 0 of the
base solid rather than from a per-solid catalog, giving a dodecahedron
`vertex-3`, `face-5` and `edge-2`.

Each projected face becomes one `<path>` carrying, in emit order: `class` and
`data-face-class` when the pattern face has classes, `data-face-index` (a scene
ordinal, not a pattern-face ordinal), `data-sides`, `data-orb-view`,
`data-projection` and `data-orb-base-face`. The root `<svg>` carries
`data-orb-view` and `data-projection`. Nothing else from the 2D renderer travels
— no `data-layer`, no `data-symmetry-fold`, no `data-partial`, and in
particular none of the strapwork machinery.

Occlusion is a **whole-face front cap**: a face is dropped entirely the moment
any lifted vertex falls below the cap, and never clipped at the rim.

**Default:** the front-cap cut is `front_cap_min_dot = 0.3`, and this design
carries it unchanged into the wheelfield representations rather than retuning
it, because the quantity it bounds — how far around the limb a whole element may
sit before it is dropped — is the same quantity for a cell as for a pattern
face. Source and rationale:
[`orb-views.ts` at the pinned bikar revision](https://github.com/NaqshCoffee/bikar/blob/f3cb04c/packages/core/src/kernel3d/orb-views.ts).
Ribbons are the case where the transfer is *not* obvious, and §4.2 states the
condition it needs.

### 3.2 qiyas `orb-validate`

The command consumes a directory of paired `<stem>.svg` and `<stem>.gt.json`,
stems matching `<orb>.<kind>-<fold>` with a lowercase-alpha kind. Ground truth
is read as raw JSON, deliberately not as a qiyas `Encoding`. Each SVG goes
through the ordinary 2D encode pipeline, and the per-view score is

```
composite = 0.40 * structural + 0.35 * geometric + 0.25 * symmetry
```

against ground truth, where the match is **centroid-and-area Hungarian
assignment in the unit square** with an acceptance radius, `structural` is the
matched fraction over the larger side, `geometric` is one minus the mean of a
half-distance half-relative-area drift, and `symmetry` is a three-valued check
on the declared fold. The report's composite is the unweighted mean over views;
`min_view_composite` is computed and reported but **not** gated.

**Default:** the pass threshold is `0.95`, both as the function default and as
the CLI's, and it is enforced only by the command's own exit status and by
qiyas's own test suite — no CI job in either repo runs `orb-validate` at either
pinned revision. Source:
[`orb_validate.py` at the pinned qiyas revision](https://github.com/NaqshCoffee/qiyas/blob/3e547da/src/qiyas/orb_validate.py).
Whether this number transfers to a cell decomposition is the question §7 refuses
to answer by assumption.

**Default:** the centroid acceptance radius is
`CENTER_MATCH_MAX_DIAG_FRAC = 0.02`, scaled by the unit square's diagonal, and
the comment justifying it reasons from classic-orb *face* spacing of about 0.05
diagonals — i.e. the radius was chosen with roughly a 2.5× margin against the
element spacing of the only geometry it had. Source:
[`orb_validate.py` at the pinned qiyas revision](https://github.com/NaqshCoffee/qiyas/blob/3e547da/src/qiyas/orb_validate.py).
The wheelfield's cells are denser than that geometry, which is precisely the
K10 transfer condition §7 measures.

The scorer is deliberately type-agnostic: projection makes faces irregular, so
bikar declares `unknown` where qiyas's 2D classifier types a regular polygon,
and typed matching was measured to score 0.67 with every centre coincident. The
typed diff exists only in `--recon-dir` mode and is explicitly informational.

### 3.3 What the wheelfield path emits today

Everything in §3.1, applied to the preview described in §2. Ground truth is
schema 1.25 with a fully populated `orb_view` block; the shapes are the
face-lifted preview polygons; the semantic fields are null. Nothing errors.
That is the danger: the failure is silent and the output looks well-formed.

---

## 4. The two representations, and what each verifies

### 4.1 A — cell decomposition

The field's cells (wheel arms, the polygonal gaps between wheels, and the
crossing cells where ribbons overlap) become closed filled polygons, one
`<path>` each, carrying exactly the attribute set classic orbs carry. This is
the representation the existing scorer was built for: closed simple polygons
with meaningful centroids and areas, one shape per path, no strokes.

What A verifies: that the **planar structure** of the field — how many cells,
where they sit, how large they are, and what rotational symmetry the whole view
has — matches what bikar declared it would be. That is a real claim, and it is
the claim that catches the failure in §2: a preview-derived view and a
field-derived view do not have the same cells in the same places.

What A does not verify: anything about ribbons, depth, or over/under. A cell
decomposition of a weave and of a rigid shell with the same cell boundaries are
the same picture.

**Validator:** the three Maclado presets, rendered on the same axis at the same
width, must not produce identical view SVGs, and each preset's view must differ
from the others in a way traceable to the knob that distinguishes them.
- PASS: `Maclado-9`, `Maclado-9-Weave` and `Maclado-9-Overlap` produce three
  distinct face-5 SVG digests, and re-rendering `Maclado-9-Overlap` at
  `overlap = 1.15` versus `1.25` also produces two distinct digests — the view
  responds to the knob whose whole purpose is to change the crossing geometry.
- FAIL: today's output — one digest shared by all three presets. This is the
  by-design failure case and it must be *asserted as failing* against the
  current code path, not merely absent from the new one.

### 4.2 B — stroked ribbons

Each strand becomes a stroked path, grouped over/under, so that a crossing
renders the way a crossing looks. bikar already solves this in 2D: the strapwork
renderer emits `strapwork-over` and `strapwork-under` groups with a `data-strand`
attribute and trims the under-strand at each crossing. None of that is reachable
from the orb view path today; there is no strand element or attribute in the orb
view renderer at all.

What B verifies: that the **ribbon layout** — how many strands cross the visible
hemisphere, where they cross, and how the crossings are ordered in depth — is
what bikar declared. It is the only representation in which the woven-overlap
orb looks like a different object from the rigid shell.

What B does not verify: parity (§6). A view can render an over/under assignment
faithfully and be scored by an instrument that cannot see it.

**Validator:** a wheelfield view must contain no unresolved overlap — every pair
of drawn elements that overlap in projection must have a declared depth order,
and the drawing order must agree with it.
- PASS: for representation A, zero interpenetrating polygon pairs per view
  (matching the classic orbs' measured zero); for representation B, every
  overlapping pair of strand elements is separated into an over-group and an
  under-group, and the under-element is trimmed at the crossing, so no opaque
  element is painted over a nearer one.
- FAIL: today's wheelfield output — eight to nine interpenetrating pairs per
  view, painted in construction order, with `minDot` computed and unread. A
  representation that merely *reduces* the count without making the remaining
  overlaps ordered fails this validator too, and the test must assert the count
  is zero rather than smaller.

The front-cap transfer condition for ribbons, stated because §3.1 said it would
be: the whole-element cap works for a face because a face is small relative to
the sphere, so dropping it whole loses little and never leaves a partial. **A
strand is not small** — a closed strand can ring the sphere — so a whole-element
cap either drops every strand or keeps every strand. Representation B therefore
needs either per-strand clipping at the cap or a per-segment cap, and Q2 must
pick one and say which; carrying the 0.3 constant across without that change
would be exactly the K10 failure this repo's rules name.

---

## 5. The qiyas defects, and the fix each takes

The audit found seven, catalogued below with the severity of what they do to a
stroke-heavy SVG. Every one of them was found by reading source at the pinned
qiyas revision, and the first was additionally reproduced by running the parser
on a synthetic in-memory SVG. This list is what one audit pass over the orb
validation path found; it is not a claim that the path contains no eighth
defect.

**D-a — `data-sides` silently voids every other metadata attribute. (Blocker.)**
`_read_bikar_metadata` in `qiyas:src/qiyas/stages/svg_primitives.py:104-112`
early-returns an empty metadata record when `data-sides` is absent or malformed,
discarding `data-orb-view`, `data-projection` and `data-orb-base-face` with it.
Verified empirically: a path carrying all three orb attributes and no
`data-sides` yields a contour with all three fields `None`. A ribbon has no
canonical side count, so every stroke element loses its orb identity; the
consistency gate then compares an empty set of contour views against the
declared view and raises an **error-severity** mismatch, which forces a fail
regardless of score. Every existing witness test co-emits `data-sides`, so the
coupling is untested and has never been noticed. *Fix:* decouple — parse the orb
attributes independently of `data-sides`, with a test that pins the decoupling
directly.

**D-b — untagged thin contours are area-floored and simplified. (Blocker for B.)**
Producer-tagged contours are exempt from both the minimum-area floor and
Douglas-Peucker simplification; untagged ones are not, and the simplification
epsilon scales with the contour's *perimeter*. A long thin ribbon has an
enormous perimeter relative to its width, so the epsilon can exceed the width
and merge the two long sides. Note that D-a *causes* D-b: an element that loses
its tag becomes an untagged contour. *Fix:* the tag must survive (D-a), and the
epsilon's perimeter scaling needs a width-aware bound or an explicit opt-out for
producer-authored geometry.

**D-c — `fill="none"` strokes are routed to classify-as-unknown, and unknowns
inflate the structural denominator.** The parser deliberately keeps stroke
outlines raw so they classify as unknown; the gt scorer then iterates
`encoding.shapes` **raw** at `qiyas:src/qiyas/orb_validate.py:204`, without the
`_split_scoreable` filter the recon path applies. Unknown and
excluded-from-scoring shapes therefore divide the structural score. The
asymmetry between the two paths is the defect; which side is right is a decision
Q3 must make and record, not assume. *Fix:* one filtering rule, applied in both
paths, with a test that fails if they diverge again.

**D-d — the shoelace area is wrong for self-intersecting paths.** `_polygon_area`
is a plain shoelace sum, so a self-intersecting crossing path's signed lobes
cancel and the area reads near zero — which then trips the minimum-area floor
and drops the contour entirely. The schema has no non-simple-polygon type.
*Fix:* either the producer never emits self-intersecting paths (a constraint Q2
can honour by construction, and should state), or the area routine must not be a
bare shoelace. The design's preference is the former, with the parser hardened
anyway so the failure is loud rather than a silent drop.

**D-e — the `--recon-dir` help text describes a diff the code does not perform.**
It promises that the default is self-validation by rasterizing each view and
diffing the raster-path encoding against the SVG-fast-path encoding. The
implementation runs no such diff when `recon_dir` is `None`; the whole diff block
is inside the conditional. The text is mirrored into the CLI reference, so the
correction is two files. *Fix:* correct the text. If the described
self-validation is wanted, that is a separate feature with its own milestone,
not a docstring.

**D-f — `min_view_composite` is reported and never gated.** One catastrophic view
can be masked by good siblings, and the mean is the only thing `passed` reads.
For a family whose three axes see genuinely different amounts of the field, this
matters more than it does for the classic orbs. *Fix:* Q4 decides the floor from
the measured distribution and Q3 wires the gate; the doc deliberately does not
name the number here (§7).

**D-g — `orb_base_face` is parsed with no consumer, while the contract claims
one.** The contract mirror describes it as regrouping faces per base tile; no
code reads the field. This is a contract-accuracy defect today and a semantics
problem tomorrow: a ribbon that spans several base faces has no single value to
put there. *Fix:* either give it the consumer the contract claims, or correct
the contract; and Q2 must say what a ribbon writes into it, including "nothing,
and here is why that is legal".

**Validator:** the orb attributes must survive on an element that carries no
`data-sides`.
- PASS: a `<path fill="none" stroke="#333" data-orb-view="face-5"
  data-projection="spherical">` with no `data-sides` parses to a contour whose
  `orb_view` is `"face-5"` and whose `orb_projection` is `"spherical"`, and an
  `orb-validate` run over a views directory whose elements are all such paths
  raises no `orb-view-attr-mismatch`.
- FAIL: the same input at the pinned qiyas revision, which yields
  `orb_view=None`, `orb_projection=None`, `orb_base_face=None` and an
  error-severity mismatch. The test must be written against this input first,
  observed to fail, and only then fixed — the failing case is the whole point,
  and a test added after the fix proves nothing about the coupling.

Contract obligations for anything new: a row in the mirror needs a `Contour`
field, a `SCHEMA_VERSION` bump, parsing plus propagation into every contour
construction site, a named witness test that exists, and the exact three-column
backticked row format; a conditional attribute additionally needs its Makefile
exemption entries. A producer-side row with no qiyas consumer must not be added
— which is exactly the trap D-g is already in.

---

## 6. What this will not verify, stated plainly

**Weave parity is invisible to this instrument.** The score is positional and
areal: centroids, areas, and a fold check. Two weave topologies with the same
cell grid score identically, and a view that renders the over/under assignment
correctly is scored by an instrument that never looks at which strand is on top.
Representation B makes parity *visible to a human* and does not make it
*measurable by the composite*.

What holds the parity claim instead is bikar's own kernel tests, which assert
that the alternating-crossing assignment solves over the welded spherical graph
and count the crossings and strands it solves over. That is where the claim
lives, that is where it must keep living, and this doc does not move it.
Concretely: a passing qiyas composite for `Maclado-9-Overlap` means *the field's
planar structure and ribbon layout match what bikar declared*. It does not mean
the weave is correctly alternating. The badge text and the doc must both say so,
because a trust badge that overstates what it checked is worse than no badge.

Two further limits worth writing down rather than discovering:

- A composite over three axis views is a claim about the **front hemisphere on
  three axes**, not about the sphere. The classic orbs live with this; a field
  with 20 wheels has more places for a defect to hide than a pattern that tiles
  every face identically.
- The scorer's type-agnosticism means a shape that is the right size in the
  right place scores well even if it is the wrong *kind* of shape. That was a
  deliberate, measured decision for projected faces; it is inherited here
  unchanged, and inheriting it means a cell decomposition cannot detect a cell
  that has the right footprint and the wrong boundary.

---

## 7. Measure before gating

The repo's K10 rule says a constant established under one process does not
automatically carry to another, and that the transfer sentence must be
writable. Two constants are in that position here, and neither gets a number in
this doc.

**The acceptance radius.** 0.02 diagonals was chosen against classic-orb face
spacing of roughly 0.05 diagonals. The wheelfield's cells are denser. If the
inter-cell centroid spacing in a rendered view falls near or below the radius,
Hungarian assignment can pair the *wrong* cells at low cost and return a high
score for a wrong picture — a vacuous pass, which is worse than a false fail
because nothing announces it.

**Validator:** the acceptance radius must be smaller than the field's
inter-element spacing by a stated margin before any wheelfield threshold is
recorded.
- PASS: over all three presets, all three axes, and both representations, the
  minimum nearest-neighbour centroid separation among scoreable elements is at
  least 2.5× the acceptance radius — the margin implied by qiyas's own
  justification for the constant, *not* a margin the classic orb was ever
  measured to have; see §7.1, which measured it at 1.85× on one classic view
  and corrects this sentence — and a deliberately perturbed ground truth (one
  element displaced by slightly more than the radius) scores measurably worse
  than the unperturbed one.
- FAIL: any view whose minimum separation is below that margin, **or** a
  perturbation test in which displacing an element leaves the composite
  unchanged. The second is the hard case: it is how a vacuous pass announces
  itself, and a validator that only checks the spacing statistic would miss a
  mis-pairing that the statistic permits.

**The pass threshold.** 0.95 was set against per-face inscribed patterns. Q4
measures the composite distribution across the three presets, three axes and
both representations, and only then records a threshold — with the distribution
written into the doc beside it, so the next reader can see whether the number is
a real bar or a rubber stamp. If the measured distribution puts every view above
0.99, the honest response is a *higher* family threshold, not a comfortable
inherited one. The floor for `min_view_composite` (D-f) is decided in the same
pass and from the same data.

Deliberately absent: this doc states no default for either the wheelfield pass
threshold or the `min_view_composite` floor. A number invented here and cited by
Q6 would be a bare number wearing a citation, which is the K4 failure the
repo's D3 rule exists to stop.

### 7.1 Q4 result (measured 2026-08-15) — the validator fires on both arms

Q4 ran, on all fifteen view/representation combinations the three presets and
the classic control produce. The full method, tables and the three programs are
checked in at
[`docs/research/qiyas-scorer-acceptance-measurement.md`](research/qiyas-scorer-acceptance-measurement.md).
The validator above **fails**, on both arms, and one of its own premises was
wrong.

**The spacing arm fails.** Nearest-neighbour centroid separation, in image
diagonals, against a 0.0200 radius:

| representation | views | min | median | share under the radius |
|---|---|---|---|---|
| classic orb cells (`Weave-Orb`) | 3 | 0.0370–0.0521 | 0.0512–0.0586 | 0% |
| wheelfield cells (`Maclado-9`, `-Weave`) | 6 | 0.0121–0.0191 | 0.0197–0.0236 | 20–52% |
| wheelfield ribbons (`-Weave`, `-Overlap`) | 6 | 0.0002–0.0025 | 0.0089–0.0105 | 86–95% |

**And the premise was wrong.** The 2.5× margin above was written as the one
"the classic-orb geometry had". Measured, `Weave-Orb`'s three view minima are
1.85×, 2.61× and 2.42× the radius — two of three are under it. The 0.05 figure
in qiyas's source describes inter-**face** spacing on the sphere; this doc
ported it to nearest-neighbour **cell centroid** spacing in a projected view,
where the rim foreshortens, and did not write the transfer sentence. That is a
K10 defect in the section that sets the K10 test, and §7's PASS line has been
corrected in place rather than quietly rewritten.

**The perturbation arm fails.** Displacing one element by five times the
acceptance radius — the hard case the FAIL line named — costs, in composite:
0.0091–0.0200 on a 40–44-cell classic view, 0.0031–0.0058 on a 101–130-cell
wheelfield view, and **0.0008–0.0011 on a 370–516-band ribbon view**. The
composite dilutes as 1/n, and past the radius it saturates: 2× and 5× score
identically on ten of twelve views, so the number is blind to *how* wrong the
picture is once an element is out.

Two further findings the arms did not ask for, both independent of wheelfields:

- **Mis-pairing is real and starts at half the radius.** Displacing an element
  toward its nearest neighbour swaps the assignment on every ribbon view at
  0.5r, on the two densest wheelfield cell views at 0.9r, and on no classic
  view inside the radius at all. The spacing statistic predicted the ordering
  and the behaviour matched it on all fifteen views.
- **`geometric` is not monotone in the defect.** On `WeaveOrb.face-3` and
  `WeaveOrb.edge-2`, pushing an element to 2r *raises* the geometric score to a
  perfect 1.0000, from 0.9888 and 0.9898 at 0.9r: past the radius the pair is
  discarded and the mean is taken over the exact pairs that remain. Making the
  defect worse improves one of the three numbers the report prints. This is a
  property of the scorer, visible on the classic orb, and it is why a report
  that shows `geometric` alone can point the wrong way.

**So no composite threshold is recordable for these views, at any value.** Not
0.95, not 0.99: every defect measured scored above 0.9942, most above 0.998.
`--min-view-threshold` (D-f) keeps its report-only default, and the reason is
now a measurement instead of a deferral. What replaces it is a count.

**Validator:** a wheelfield view's gate must be a statistic that does not
dilute with element count — an integer count of unmatched ground-truth
elements, or a per-pair extreme — and never the composite alone.
- PASS: the gate's statistic moves by at least one reporting unit when a single
  element of the largest view (`Maclado-9-Overlap.vertex-3`, 516 bands) is
  displaced past the acceptance radius. The unmatched count does: 0 → 1.
- FAIL: a gate whose statistic is any of `composite`, `structural` or
  `geometric` on their own. Measured on that same view, the composite moves
  0.0008 for that displacement and `structural` moves 0.0019 — both smaller
  than the fourth decimal place either is reported to, and `geometric` can move
  the wrong way entirely.

Still deliberately absent when this section was written, and now measured: **the
bound on `max_drift`.** Every number above compares ground truth against a
perturbed copy of itself, so the clean per-pair drift is exactly 0.0000 by
construction — not the floor a real gate must clear. What qiyas's encoder drifts
by when it recovers bands from an actual rendered PNG was unmeasured, because
the local `qiyas encode` CLI could not run here (cairo is missing).

**The floor, measured in Q4b (bikar PR #102, 54 views over 14 orbs, local qiyas
at the v0.3.0 commit):** every one of the 54 views reports `max_drift`, and the
distribution is min 0.0001 / median 0.0002 / max **0.0003**, with **zero views
at exactly 0.0000** — which is what makes it an encoder measurement rather than
the by-construction zero above. `max_dist` (`0.02 · √2`) is 0.028284, about
**100× the worst drift observed**. It did not need a sibling CI run to get
there: `resolveQiyas` takes `QIYAS_DIR` as well as `QIYAS_IMAGE`, so the local
checkout measured the floor without waiting for a tag.

Two build items followed, both new, and **both are done — the second one
disproved its own premise, which is the more useful outcome:**

- **Q4a (qiyas). ✅ Done** — qiyas PR #15 (`a98a657`), SCHEMA 1.25/1.26. Exposes
  the per-part statistics `Scores` does not carry: `drop`, the count of
  ground-truth elements with no partner inside the radius, and `max_drift`.
  Neither could be gated on until it was reported.
- **Q4b. ✅ Done, and it is not what this bullet asked for** — bikar PR #102
  (`6157792`), and note it landed as *bikar* work, not the qiyas work predicted
  here. The premise was that the acceptance radius must scale with the
  representation, 0.02 being 5–8× the ribbon field's own p05 spacing. Measured,
  that is not where the loss was: replicating the Hungarian assignment on the
  four affected views gives `unmatched-by-distance = 0` on all four and
  `drop == len(gt) − len(encoded)` exactly. **Every drop was a shape the encoder
  never produced** — widening the radius recovers nothing, narrowing costs
  nothing. So no constant changed; what shipped instead carries `drop` and
  `max_drift` into the gate (`RECORDED_DROP` per preset, `MAX_DRIFT_CEILING`
  0.005, ~17× the worst observed). The 30 drops that motivated all this turned
  out to be a qiyas validator defect and are now zero —
  [D-035](decisions-log.md).

---

## 8. Milestones — each states what it verifies

**Q0 — this doc and its research.** Verifies nothing about the engines; it
records what was measured and fixes the scope. Exit: the doc and the research
file are checked in, `make validate-docs` is green, and the pointer, counts and
site-graph gates pass.

**Q1 — bikar: true cell views (representation A).** Project the field's own cells
through the existing scene rather than the preview wheel; feed the wheelfield
evaluator branch's real geometry into the view path; keep the attribute contract
byte-for-byte identical to the classic orbs. Verifies §4.1's distinguishability
validator (three distinct digests, knob-responsive) and §4.2's overlap validator
for A (zero interpenetrating pairs). Exit additionally requires that every
classic orb's view output is unchanged — a snapshot over the eleven registry
orbs, so that "we fixed the wheelfield" cannot quietly mean "we moved the
classic orbs".

**Q2 — bikar: ribbon views (representation B).** Per-strand stroked paths with
over/under grouping lifted from the 2D strapwork precedent; a real depth
resolution using the `minDot` that is already computed and unread; a decision,
written down, on the front-cap transfer for strands (§4.2) and on what a
multi-face ribbon writes into `data-orb-base-face` (D-g). Verifies §4.2's
overlap validator for B. Depends on Q3's D-a fix to be scoreable at all, but not
to be *rendered* — Q2 can land and be looked at before Q3 lands.

**Q3 — qiyas: audit fixes.** D-a through D-g, each with a test that fails at the
pinned revision and passes after; contract rows, witness tests and a
`SCHEMA_VERSION` bump for anything new; fixtures for both representations, since
the only orb fixture today is per-face closed filled polygons and there is no
stroke fixture anywhere. Verifies §5's attribute-survival validator, plus one
regression test per defect.

**Q4 — measure before gating. ✅ done 2026-08-15; §7's validator fired.** The
spacing and perturbation measurements ran on all fifteen view/representation
combinations. §7.1 records the result: the acceptance radius does not transfer,
the composite dilutes as 1/n, and **no threshold was recorded, because none is
recordable** — the outcome this milestone was written to allow rather than the
one it expected. `min_view_composite` therefore keeps its report-only default
and the gate becomes a count. Two follow-ons fall out: **Q4a** (qiyas must
expose the per-part statistics it does not carry) and **Q4b** (the radius must
scale with the representation). Verified §7's acceptance-radius validator by
failing it, which is the only way a validator with a hard FAIL case gets
exercised at all.

**Q5 — CI wiring. ✅ Done** (bikar PR #100, `5349a80`). No CI job in either repo
ran `orb-validate` at either pinned revision; the eleven recorded composites came
from a manual local Docker sweep, hand-transcribed at bikar `ba5ef85`, and the
registry's comment about a CI gate making stale values a tripwire had no
automation behind it. **bikar owns the job** — three pieces:
`bikar:scripts/sweep-orb-validate.ts` measures (renders all 14 orbs, scores every
view set), `bikar:packages/lab/tests/orb-composites.test.ts` compares recorded
against measured, and `bikar:.github/workflows/orb-validate.yml` runs both. qiyas
arrives as a pinned container (`QIYAS_IMAGE`) or a sibling checkout
(`QIYAS_DIR`), **exactly one** — both set is an error rather than a precedence
rule, because a green sweep against a pinned image and a green sweep against a
working tree are different claims, and the resolved command is recorded in the
output JSON so a reader can tell which one they hold.

*Exit condition met by construction, not by a green run:* the comparing test was
mutated four ways and each was caught — a moved composite, a retyped ribbon
histogram, a `ribbon_pass` in cells, and a cells score where the sweep drew none.
Q4b added three more by-design failures on the same file (§7.1).

*What the first sweep found, which is the argument for sweeping the directory
rather than a list:* **three of the five orbs declaring a `weave` drew no ribbon
views at all** — `Rosette-Weave-Orb`, `Weave-Orb`, `Weave-Dodeca-Orb`.
`evaluateWovenOrb` never forwarded the `topology` that `weaveLattice` had been
returning the whole time; only the wheelfield branch did, so the CLI took its
early return and wrote cells only. Silently, for two weeks. No single-file test
could have surfaced it. The witness is codified twice, per bikar's tenet 18: a
directory sweep that automatically covers any woven orb added later, and a
Lab-side case comparing the presets that declare a weave against the presets that
have a ribbon score.

*One design change came out of measuring:* `qiyasComposite` is a **pair**, not a
number. An orb draws cell views, ribbon views, or both, and one number cannot
speak for two drawings — a mean lets healthy cells hide collapsed ribbons. It is
now `{cells, ribbons}`, each independently nullable, and the badge shows the
**minimum** of the drawings actually scored.

**Q6 — surface the presets.** *(Done — bikar PRs #97 and #98, [D-034](decisions-log.md).)*
Record a composite per preset; add the three registry entries; add `lab:` links
to the three gallery cards; write the badge text that carries §6's limitation
rather than eliding it. Two potholes found during scoping and fixed here: the
knob guard that keeps weave amplitude clear of ribbon depth reads a parameter
named `strut_depth`, so it silently no-ops on the weave presets, which name
theirs `ribbon_depth`; and orbs have no registry-versus-patterns-directory sweep
test, though the Lego presets do. Verifies: the guard fires on a Maclado preset
(a case that must be shown failing before the fix), and the sweep test fails
when a preset exists on disk and not in the registry.

Both verifications were satisfied before the fixes shipped — the guard test
failed on exactly the two `ribbon_depth` presets, the sweep test failed against
the pre-fix registry — and the fixes went further than the plan in one respect:
the Lab's own "ribbon gap" readout had gone blind by the same name, so the two
readers now share one `weaveDepthValue` rather than two lists that can drift
apart. The composite half is **not** done and is not Q6's to finish: the three
entries carry `qiyasComposite: null` and a badge reading *not yet
qiyas-validated*, and the sweep test pins that trio by id so recording the first
real score requires editing the assertion that says none exists.

---

## 9. Open questions and risks

1. **Does a cell decomposition of the field even exist cleanly?** The field is
   built by placement and welding, not by planar face extraction on the sphere.
   Q1 may find that "the cells" require a construction that does not exist yet,
   which would make Q1 substantially larger than a plumbing change. This is the
   largest schedule risk in the plan and it is not yet measured.
2. ~~**Which repo owns the CI job (Q5)?**~~ **Answered — bikar owns it**, with
   the seam a published container pinned by tag (`QIYAS_IMAGE`, today
   `ghcr.io/naqshcoffee/qiyas:v0.4.0`) or a sibling checkout (`QIYAS_DIR`),
   exactly one of the two. The option this question named as the one that must
   not be chosen silently — "keep doing it by hand and write down the number" —
   is the one that ended. See §8 Q5.
3. **Does fixing D-c change any classic-orb score?** Unifying the filtering rule
   between the gt path and the recon path could move the eleven recorded
   composites. If it does, that is a finding about the recorded numbers, not a
   reason to leave the asymmetry in place — but it must be measured and reported
   before it is merged, not discovered afterwards.
4. **Three axes may not be enough coverage** for a 20-wheel field (§6). Whether
   to add axes is deferred until Q4's distribution shows whether the existing
   three already disagree with each other.
5. ~~**The qiyas revision is now pinned; the classic-orb composites are not.**~~
   **Answered, and by re-measurement rather than by stamping.** The worry was
   that the eleven recorded numbers had no producing revision beyond a commit
   message, so the first disagreement would be unattributable. Q5's sweep
   re-derives all fourteen on every relevant push against the pinned image and
   records the resolved qiyas command in the output JSON, so a recorded number is
   now checked rather than merely attributed — a stale one fails the job. The
   attribution question survives only for a number read **outside** that run,
   which is the case D-035's cascade rule addresses: the image pin and the
   numbers it produced move in one commit, because a commit that moved either
   half alone would be a red run with a misleading cause.

---

## Appendix A — attribute sketch for the two representations

Representation A reuses the classic contract exactly:

```
<path class="…" data-face-class="…" data-face-index="N" data-sides="K"
      data-orb-view="face-5" data-projection="spherical" data-orb-base-face="M"
      fill="…" stroke="#333333" stroke-width="0.4"/>
```

Representation B is the open question Q2 and Q3 settle together. The sketch
below is a proposal, not a decision, and each line names the obligation it
incurs:

```
<g class="strapwork-under" data-orb-view="face-5" data-projection="spherical">
  <path data-strand="S" … fill="none" stroke-width="W"/>   ← needs D-a fixed
</g>                                                        ← and D-b's epsilon
<g class="strapwork-over" …>                                ← ordering is the
  <path data-strand="S'" … fill="none" stroke-width="W"/>      §4.2 validator
</g>
```

Open, and to be decided in Q2/Q3 rather than here: whether `data-strand` earns a
contract row (it needs a qiyas consumer first, or it must not be added); what
`data-orb-base-face` carries on a multi-face strand; and whether a stroked
ribbon is scored as its outline or as a widened centreline, which is the choice
that decides whether D-b's epsilon bound is needed at all.

## Appendix B — pinned revisions and what was read at them

| Tree | Revision | Status at read |
|---|---|---|
| bikar | `f3cb04c` (merged M4e) | read via the `bikar-lego-lab` worktree, detached; built bundle executed in memory for the §2 measurements |
| qiyas | `3e547da` on `main`, pushed | working tree clean apart from two untracked skill directories; parser run in memory for D-a |
| 3d-models | this branch | — |

§7.1's measurement was taken later and at different revisions, because it had to
run against the code Q1–Q3 shipped rather than the code they replaced:

| Tree | Revision | Status at read |
|---|---|---|
| bikar | `cc66cd3` on `feat/orb-ribbon-views` | the PR #96 head — ribbon views must exist before their spacing can be measured |
| qiyas | `17552cc` on `fix/orb-view-scoreable-split` | the PR #11 head — the scorer is the fixed one, so the numbers describe what will be on `main` |

The full per-file read record, including which files were read versus executed,
is the closing table of
[the research file](research/qiyas-wheelfield-validation-survey.md); §7.1's is
the header and appendix of
[its own research file](research/qiyas-scorer-acceptance-measurement.md).
