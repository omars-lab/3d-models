# Pattern-Outline Brick Bodies — `footprint outline` — design doc

Status: **v2 — drafted and adversarially audited 2026-08-02
([`research/pattern-outline-brick-grounding-audit.md`](research/pattern-outline-brick-grounding-audit.md));
findings F1–F7 applied same day, and the audit's two demanded computations (F3 cusp floor, F4
component count) were executed against the rosette corpus — results in §5.** The kernel side is
already built and tested in bikar (§2); this doc specifies the missing language surface.
**Implemented 2026-08-02** (bikar `bf6c602`, decision doc
`bikar:docs/decisions/2026-08-02-pattern-outline-footprint.md`) with `Rosette-Brick.bkr`
authored in the same commit; one §6 cell diverged in the small — see the table's grammar row.
Nothing here ships plastic: the physical questions stay with LG-B2 and its bets (Appendix B.4).

Scope: the smallest bikar DSL extension that lets a `.bkr` declare a brick whose silhouette **is**
the inscribed pattern's outline rather than a stud-grid rectangle — the body case
[`lego-lab-design.md`](lego-lab-design.md) §5.2/§7.2 specifies, the kernel honours, and no grammar
statement reaches. It exists to unblock **LG-B2** (`.claude/skills/prototype/catalog.md`), the
coupon the lego-lab doc calls the load-bearing test of the anchor-only clutch bet.

Builds on: [`lego-lab-design.md`](lego-lab-design.md) (the `brick` declaration, the two body
cases, Appendix B.7's inset caveat);
[`research/pattern-outline-dsl-surface-survey.md`](research/pattern-outline-dsl-surface-survey.md)
(the Appendix-A survey behind every prior-art and precedent claim here);
[`research/pattern-outline-body-clutch-survey.md`](research/pattern-outline-body-clutch-survey.md)
(non-rectangular LEGO prior art and the clutch counter-case);
[`backlog.md`](backlog.md) note 10 (the blocker this doc resolves);
[`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md) (the house precedent on
when a DSL extension deserves process, and what a wrong pointer costs).

---

## 1. The gap, the goal, the non-goals

**The gap.** bikar's brick kernel accepts an arbitrary body silhouette: `BrickSpec.bodyOutline`
is an optional field (`bikar:packages/core/src/kernel3d/brick.ts` L120), and when present the
kernel builds the body from it and the cavity from its inset (L545, L549). The anchor solver,
port minting and top-face partition all take the real outline (§2). Tests construct such specs
directly. But `evaluateBrickDecl` never sets the field, and the grammar's brick statement set
(`inscribe|footprint|height|studs|anchors|engage|clutch|relief|origin|port`) has no statement
that could — the evaluator's own comment records it: *"M6 ships the **rectangular** body case
only (§7.2). The pattern-outline case … is what LG-B2 depends on."*
(`bikar:packages/core/src/dsl/evaluator.ts` above `evaluateBrickDecl`).

**The goal.** One grammar production, one evaluator branch, two new validators — after which

```
brick RosetteBrick
  inscribe Rosette
  footprint outline
  height 3 plates
```

compiles to a piece whose body is the rosette's outer boundary, whose cavity is that boundary
inset by the wall, and whose studs, anchors and ports are whatever the existing solver finds
room for inside it.

**Non-goals.**

- **No auto rule.** The body mode is never inferred from the pattern's geometry (§3 argues why).
- **No multi-component bodies.** A pattern whose face union has two disjoint components is an
  error (V19), not two bodies.
- **No holes in the silhouette.** The body is the union's *outer* ring; interior rings remain
  what they are today — relief. A brick that is itself an annulus is out of scope.
- **No `footprint 4 x 4 outline` combination.** Outline mode derives its grid (§4); a declared
  grid wider than the body would only add lattice cells that can never engage. If a use case
  appears it is a separate decision, not a v1 default.
- **No change to `insetRing`.** The kernel's inset heuristic stays as-is; what changes is that
  its failure modes become a hard error at the gate instead of silent geometry (§5, B.3).
- **No tangent pads.** LEGO's own non-rectangular parts add flat wall pads at the stud-tangent
  plane rather than trusting the tube (B.4); that feature is LG-B2's designed contingency, not
  a v1 surface — building it before the coupon measures the anchor-only ratio would be paying
  for an answer the print may hand us for free.

## 2. Engine ground truth (bikar `main` at `73514f1`, read 2026-08-02)

The extension is small because the kernel is already finished. Each fact below was read from
source at the named location, not remembered:

1. **Body and cavity honour the field.** `const body = spec.bodyOutline ?? rectangularBody(…)`;
   the cavity is `insetRing(spec.bodyOutline, effectiveWall(spec.fit))` when the field is set
   (`bikar:packages/core/src/kernel3d/brick.ts` L545–L551, and again L857).
2. **The anchor solver takes the real outline.** `solveAnchors(c, r, bodyOutline, fit, …)`
   engages a lattice cell only when the body covers the whole 8 mm cell less the part relief —
   reach 3.9 mm exactly, `STUD_PITCH_MM/2 − PART_RELIEF_MM/2` — and drops any anchor whose
   ribbed footprint the outline cannot contain
   (`bikar:packages/core/src/kernel3d/grid-gate.ts` L229, L256, L279). A rectangular c×r body
   engages every cell by construction; a pattern-outline body engages the cells it actually
   covers. This is the same semantics brickify documents for studs — "only in positions where
   they fully fit within the object" (survey §1; the sentence sits in brickify's custom-mask
   section, not its general docs) — already implemented here.
3. **Rotation lock is engagement-based, not shape-based.** The gate is `studsEngaged >= 2`
   (`bikar:packages/core/src/kernel3d/grid-gate.ts` L351), so an outline body passes or fails by
   what it covers, with no rectangular assumption anywhere in the rule.
4. **Ports are already plumbed.** `brickPorts` takes an optional `bodyOutline`
   (`bikar:packages/core/src/kernel3d/brick-ports.ts` L133) and the evaluator already passes
   `spec.bodyOutline` through to lattice-port minting
   (`bikar:packages/core/src/dsl/evaluator.ts` L2423) — a dormant argument that has never been
   non-undefined in production.
5. **Tests exercise the field.** An L-shaped body with full studs in
   `bikar:packages/core/tests/kernel3d/brick.test.ts` L463; eight `bodyOutline` fixtures in
   `bikar:packages/core/tests/kernel3d/brick-top-face.test.ts`.
6. **The inset is a self-flagged heuristic.** `insetRing`'s own comment: *"a heuristic rather
   than a proof: a concave vertex whose offset self-intersects is clipped by dropping the
   crossing span. Appendix B.7 still carries this as unverified — the counterexample to look for
   is a deeply reflex vertex (a star tip) where the dropped span removes wall the anchor test
   then assumes is present"* (`bikar:packages/core/src/kernel3d/brick.ts` L752, on `insetRing`
   at L759). And the implementation is *weaker than its comment*: `dropCrossingSpans` (L789) only removes
   near-coincident consecutive vertices; no code detects an actual self-intersection span.
   (One gloss the comment needs: an outer ring's star *tip* is a narrow **convex** vertex — the
   notch between tips is the reflex one — and it is the convex class that misbehaves under
   inward offset, which is exactly what §5's clamp analysis governs.)
7. **No validator guards the inset today.** `lego-lab-design.md` §7.2 says a degenerate inset
   "fails V2" — but V2 in code is *pattern must fit the footprint*
   (`bikar:packages/core/src/kernel3d/brick-validate.ts` L148), and nothing anywhere validates
   `insetRing`'s output. That sentence in §7.2 was written against the specified design, not the
   shipped code (a K7-class drift this doc corrects: §5 assigns the check a real number, V18).
8. **Footprint resolution is a two-armed switch ready for a third.**
   `resolveBrickFootprint` returns the declared `c × r`, or for `auto`, `studsFor(bbox)` on each
   axis (`bikar:packages/core/src/dsl/evaluator.ts` L2445); the parser refuses `footprint auto`
   without `inscribe`. Art is recentred by its bbox centre onto the brick frame
   (`resolveBrickArt`, L2182), and relief pockets are built in that frame — so a body ring
   derived from the same faces shares the transform for free.

## 3. The surface: a third `footprint` mode, chosen over three alternatives

**Grammar.** `BrickFootprint = "footprint" ("auto" | "outline" | UINT "x" UINT)` — one new arm
in `parseBrickFootprint`, no new statement, no new reserved word. `outline` is already a bikar
statement word (the tile declaration's `outline square <side>`), brick statement words are
contextual rather than globally reserved, and the kernel field this reaches is literally named
`bodyOutline` (survey §5).

**Corpus evidence (K2 scope: exactly what was searched).** A grep over all 237 `.bkr` files under
the four working trees swept by this repo's Stop hook — bikar (`bikar-lego-lab` worktree,
106 files), 3d-models (19), sacred-patterns (112), coffee-house-sites (0), on 2026-08-02 — finds
`outline` as the tile statement, inside comments, inside longer identifiers (`warp_outline`),
**and as a user-declared blueprint boundary name in four sacred-patterns files**
(`boundary outline = union(…)` / `clip pattern to outline`,
`sessions/bikar-medallion-10/iterations/{20,27,28,29}/pattern.bkr`). None of these collides with
the extension: `footprint <word>` is parsed only inside a `brick` declaration, and statement
words are contextual precisely so authors may keep using them as names — which those files
already do. No file contains `footprint outline`, so the extension changes the meaning of zero
existing programs. (This paragraph originally claimed `outline` was *never* a declared name; the
grounding audit falsified that against the same corpus — the K2 failure CLAUDE.md documents —
and the finding, an existing name coexisting harmlessly with the new mode, is itself evidence
for the contextual-words argument.)

**Why explicit, not inferred.** The tempting alternative is an auto rule — "if the inscribed
art's union touches the footprint boundary, the body becomes the outline." It is rejected
because it changes what existing programs mean: `Star-Brick.bkr` inscribes art into a
rectangular body today, and a geometry-triggered rule would silently rebuild its silhouette on
the day the rule ships. The precedent for gating a semantics change behind explicit opt-in is
industrial and consistent: Rust editions ("since editions are opt-in, existing crates won't use
the changes unless they explicitly migrate"), Python `__future__` statements, and PEP 20's
"in the face of ambiguity, refuse the temptation to guess" (survey §3). **Transfer condition
(K10):** editions and `__future__` are language-*version* mechanisms, not per-feature modes;
they transfer here not by mechanism but because the hazard is identical — an existing program
whose compiled output would change under a new interpretation. Strictly, no opt-in precedent is
needed for the mode itself — an additive word no program contains changes nothing; editions and
`__future__` bear only on the rejected auto rule, which is the case where existing programs'
meaning would drift. The counter-position (convention-over-configuration) is taken up in
Appendix B.1.

**Alternatives considered and declined.**

- **A new `body outline` statement.** Costs a new contextual word (`body` appears in no `.bkr`
  today outside comments — 5 files mention it in prose — so it is *available* — but availability is not free: it is one more statement whose
  interaction with `footprint` needs a rule), and it splits body policy across two statements.
  The Configuration Complexity Clock's warning against knob accretion cuts against it
  (survey §3); `footprint` already owns the body-shape decision, so the mode belongs there.
- **A geometry-triggered auto rule.** Rejected above.
- **Shape-as-input, à la brickify.** brickify takes the 2D object as the module's *only* input,
  so passing a shape is itself the opt-in. bikar's `brick` already has `inscribe` *and* a
  rectangular default, so the same surface here would be exactly the inference this section
  rejects (survey §1).
- **Other names.** The fetched generators mostly say "shape"; `profile` is well-attested in CAD
  but already means the *revolve* input in bikar — reusing it would plant a K7 collision;
  `silhouette` appears in none of the nine surveyed vocabularies (survey §5, scoped to its
  table).

## 4. Semantics

**`footprint outline` requires `inscribe`** — same rule, same error shape as `footprint auto`
("nothing to fit"): the outline *is* the art's, so a brick without art has no outline to take.

**The grid is derived exactly as `auto` derives it**: `cols = studsFor(bbox.width)`,
`rows = studsFor(bbox.height)` on the inscribed art's bbox. **Transfer condition (K10):** this
reuse is sound for the *lattice* consumers — origin, anchor candidate enumeration, height
rules, V2's fit check — because each is a statement about the enclosing stud grid, and the
kernel separately re-tests every cell and anchor against the actual ring (§2.2). Two consumers
are **not** grid statements and need explicit handling (the audit found both after this doc
claimed the reuse universally): (a) `evaluateBrickDecl` mints *declared* ports against
`rectangularBody(cols, rows, origin)` (`bikar:packages/core/src/dsl/evaluator.ts` L2409) — in
outline mode that argument must be the body ring, or a declared `port` on an outline brick
would mint on a rectangle that is not the body, floating off or buried inside the true
silhouette; §6 carries the row. (b) V13's dead-border advisory keys on `kind === 'auto'`
(evaluator L2401, gate `bikar:packages/core/src/kernel3d/brick-validate.ts` L379) and stays off
in outline mode — correct, because the body follows the art and there is no rectangular border
to warn about, but it is a decision, recorded here, and the Lab's provenance will show
`footprintAuto: false`.

**A practical floor the error message must name.** An outline body engages only the cells it
fully covers (§2.2), so a small or lacy pattern can pass V2 trivially (its grid was rounded up
from the same bbox) and then hard-fail anchorability at the last gate with a message that never
mentions outline mode — e.g. a 12 mm-wide rosette gets a 2-stud grid whose cell centres its
body cannot reach. The floor, stated plainly: **the body must fully cover at least two 8 mm
lattice cells** (roughly, contain a lattice-aligned 16 × 8 mm solid region). §6 adds the
outline-mode hint to the anchorability failure.

**The body ring** is the outer ring of the single edge-connected component of
`unionPatternFaces` over the inscribed pattern — the same union the relief path already
computes — translated by the same art-recentring the relief pockets receive. Interior rings of
the union stay relief. Preconditions are validated, not assumed (V19).

**Everything after the spec is the kernel as-is** (§2): cavity = `insetRing(ring, wall)`, cell
engagement and stud placement filtered by the ring, anchors dropped where the ring cannot
contain them, rotation lock `studsEngaged >= 2`, ports minted against the ring, mesh and print
gates unchanged.

**Relief composes.** A `relief` statement on an outline brick means what it means today: the
art's interior faces are pocketed into the top face. The body ring and the pockets come from
one union, so a pocket can only touch the body edge where the art touches its own boundary —
the edge-to-edge relief machinery (`lego-pattern-set-design.md` §7) already handles exactly
that case.

## 5. Degeneracy is a hard error — a stricter-than-library choice, stated as one

The failure this section exists for: inset an outline with a narrow star tip — a sharp
**convex** vertex (§2.6's gloss) — by 1.5 mm, and the miter clamp
(`scale = d / Math.max(0.2, √cos)`, `bikar:packages/core/src/kernel3d/brick.ts` L773–L774)
places the tip's offset vertex materially closer to the body than the wall it claims; on
sharper tips the returned ring self-crosses into a bowtie, and nothing detects either — the
comment's promised crossing-span drop does not exist in the code (§2.6). The anchor solver's
clearance test then reads wall that is not there. Today that ships a wrong solid with no
message (§2.7).

The survey's honest finding (survey §4): **hard error is not what geometry libraries do.**
Clipper2 treats self-intersecting input as a caller precondition and repairs by winding; CGAL's
straight skeleton defines split-or-vanish as a *valid* offset result; OpenSCAD documents silent
feature loss ("walls less than 2*r thick vanish" — written for its `offset(r=+3) offset(delta=-3)`
Round idiom, but silent thin-feature loss is the accurate takeaway). None of the three fetched
libraries errors.
The justification for erroring anyway is not industry standard but manufacturing semantics plus
in-repo precedent: a `.bkr` compiles to a physical part whose clutch model *reads* the wall the
heuristic deleted; bikar's own kernel already throws on inset degeneracy in two of its three
inset sites (`bikar:packages/core/src/kernel3d/solidify-lattice.ts` L172,
`bikar:packages/core/src/kernel3d/solidify-piece.ts` L427); and PEP 20's "errors should never
pass silently" is house instinct. The divergence is argued fully in Appendix B.2.

### V18 — the inset ring keeps the wall it claims

**Validator:** after `insetRing(body, wall)`, every vertex **and every edge midpoint** of the
returned ring must lie at least `wall − 0.05 mm` inside the body ring
(`signedDistToRing ≥ wall − 0.05`), the ring must have ≥ 3 vertices, and its area must be
positive with the same winding as the body. Any violation is a hard error naming the worst
offending point and its actual clearance.
PASS: a convex decagon body inset 1.5 mm — every inset point sits 1.5 mm inside; V18 is silent.
FAIL: a five-point star with 0.8 mm-wide tips — the clamp throws each tip vertex up to 5·wall
along the inward bisector, the returned ring self-crosses, and V18 finds vertices and midpoints
at small or negative clearance and refuses, naming the worst point — where today's kernel ships
the solid. (The code path is the miter clamp, not the comment's promised crossing-span drop —
§2.6.)
The 0.05 mm tolerance is the repo's existing lattice snap epsilon (`SNAP_THRESHOLD_MM`,
`bikar:packages/core/src/kernel3d/grid-gate.ts` L110), reused so no new constant is minted. It
does **not** bound `insetRing`'s error on all legal inputs: the clamp's `cos` is
`(1 + n1·n2)/2 = sin²(θ/2)` for interior angle θ, so any convex vertex sharper than
`2·arcsin(0.2) ≈ 23.1°` is placed materially closer than `wall` to the body — by design, since
an unclamped miter would run away. At θ = 10° the achieved wall is `(wall/0.2)·sin(5°) ≈ 0.65 mm`
of 1.5 mm — a 0.85 mm shortfall, 17× the tolerance. V18 therefore refuses every outline whose
convex cusps are sharper than ≈23.1°, and that refusal is correct: the shipped solid genuinely
thins there. **Consequence, stated as a precondition:** outline mode requires every convex
interior angle on the union's outer ring to clear ≈23.1° (or the pattern must pre-round its
cusps). **Measured, 2026-08-02:** replicating the relief pipeline (`faceComponents` →
`collectBoundaryEdges` → `chainBoundaryRings`, line-faithful to
`bikar:packages/core/src/dsl/evaluator.ts` L1260/L1280/L2231) over all eight rosette sources in
bikar at `73514f1` — the seven `patterns/Rosettes/*.bkr` plus `patterns/Rosette-12.bkr` — the
sharpest convex vertex on any outer ring is **72°** (Rosette-10 and both 10-fold variants, at
the decagonal points; the 12-fold rosettes sit at 150°). The corpus clears the floor three
times over, so the flagship is authorable under v1 with no cusp-rounding — because the union is
over *all* bounded faces of the pattern (the fully tiled disc), not the star petals alone (V19's
measurement explains why).

### V19 — the body is one piece with one boundary

**Validator:** the inscribed pattern's face union must have exactly one edge-connected
component, and that component's outer ring must be simple (no self-intersections). Violations
error with the component count or the crossing coordinate.
PASS: one rosette — one component, one simple outer ring. **Executed, not assumed
(2026-08-02):** every one of the eight rosette sources in bikar at `73514f1` (the seven
`patterns/Rosettes/*.bkr` plus `patterns/Rosette-12.bkr`, 30–390 bounded faces each) evaluates
to exactly **one** edge-connected component with one boundary ring and no holes, under the
relief path's own grouping. The reason is structural, and worth keeping: the union takes *all*
bounded faces — kites, inter-petal triangles and spokes included — so a rosette's union is the
fully tiled disc, whose boundary is the outer polygon, not the petal silhouette.
FAIL: a pattern of two disjoint rosettes — two components; the error says
"2 body components (outline mode needs exactly 1)" rather than picking one silently.
A petals-only art whose lobes meet at single points cannot slip through either: vertex-touching
faces land in *different* components (the grouping is edge-based —
`bikar:packages/core/src/dsl/evaluator.ts` L2231 — so the count check fires), and a single
component whose boundary touches itself at a point is refused by the union itself with a named
pinch error ("two regions touch at a single point", `chainBoundaryRings`, evaluator L1280).

## 6. What changes where (all in bikar; this repo changes docs only)

| Piece | Change |
| --- | --- |
| `parser.ts` `parseBrickFootprint` | third arm: `outline` → `{ kind: 'outline' }`; reuse the `auto`-without-`inscribe` refusal |
| AST `BrickFootprintNode` | add `kind: 'outline'` |
| `evaluator.ts` `resolveBrickFootprint` | `outline` branch = the `auto` branch (grid from bbox) |
| `evaluator.ts` `evaluateBrickDecl` | when `kind === 'outline'`: compute the union's outer ring (helper refactored from the relief path), validate V19, set `spec.bodyOutline` |
| `evaluator.ts` L2409 declared-port minting | when `kind === 'outline'`, hand `mintDeclaredPorts` the body ring, not `rectangularBody(cols, rows, origin)` — otherwise a declared `port` mints on a rectangle that is not the body (audit F5; §4a) |
| V13's predicate (`evaluator.ts` L2401) | unchanged — stays keyed to `kind === 'auto'`; outline mode has no rectangular dead border, so the advisory staying off is the decision §4b records |
| anchorability failure message | gains an outline-mode hint: "the body must fully cover ≥ 2 lattice cells; small or lacy outlines cannot engage the grid" (§4's practical floor) |
| `kernel3d` | V18 check where `insetRing` is called; no change to `insetRing` itself |
| `docs/grammar.md` | `BrickFootprint` production; **no §12 row** — implementation found the coverage table keys on dispatched keywords only, and `outline` is a contextual identifier, not one (prose + contextual-words list + an invalid fence instead) |
| `keywords.snapshot.txt` | **unchanged** — the whole point of the naming choice |
| corpus-sweep | pre-flight `npx tsx scripts/corpus-sweep.ts` before and after; expected delta zero |
| tests | parse (`footprint outline`, refusal without `inscribe`); eval (grid derivation, frame identity with relief); V18 star-tip FAIL case verbatim from §5; V19 two-component FAIL case; an end-to-end outline brick rendered `--check` watertight |
| decision doc | `bikar:docs/decisions/2026-08-02-pattern-outline-footprint.md` — the mode-over-statement choice and the stricter-than-library error policy |

## 7. What this unblocks, and what it does not

Unblocked: **LG-B2** — `Rosette-Brick.bkr` becomes authorable, and not merely by assertion:
the audit's two flagship-risk checks were run against the rosette corpus (§5) — every candidate
source unions to one component and clears the ≈23.1° cusp floor at 72° — so the flagship
compiles under v1's validators with no cusp-rounding precondition. The two forward-reference
entries for it in `.claude/gates/doc-pointer-baseline.json` are removed when it lands
(the ratchet's designed shrink).

Not unblocked: any physical claim. Whether an outline body's anchor-only clutch retains
usefully on a real baseplate is exactly the bet LG-B2 exists to measure, and it stays
provisional until printed (Appendix B.4). Printing itself remains held on LG-F1 producing a
seated rung.

---

## Appendix A — sources

The research behind this doc is checked in, verbatim, with provenance headers:

- [`research/pattern-outline-dsl-surface-survey.md`](research/pattern-outline-dsl-surface-survey.md) —
  brick-generator prior art (brickify, LEGO.scad, MachineBlocks, base-plate-outliner — fetched;
  two more known only as unverified snippets), CAD DSL mode precedent (OpenSCAD `resize auto`,
  CadQuery, JSCAD), the explicit-vs-implicit argument both ways (Rust editions, Python
  `__future__`, PEP 20 vs Rails doctrine, Configuration Complexity Clock), offset degeneracy
  semantics (Clipper2, CGAL straight skeleton, OpenSCAD `offset`), and the naming table.
  Headline primary URLs: <https://github.com/richfelker/brickify>,
  <https://doc.rust-lang.org/edition-guide/editions/index.html>,
  <https://doc.cgal.org/latest/Straight_skeleton_2/index.html>,
  <https://www.angusj.com/clipper2/Docs/Units/Clipper.Offset/Classes/ClipperOffset/_Body.htm>.
- [`research/pattern-outline-body-clutch-survey.md`](research/pattern-outline-body-clutch-survey.md) —
  LEGO's own non-rectangular parts and their clutch strategies, printed irregular-outline prior
  art, the steelmanned case against anchor-only clutch, FDM printability of concave outlines and
  1.5 mm inset walls, rotation lock on two anchors.
- [`research/pattern-outline-brick-grounding-audit.md`](research/pattern-outline-brick-grounding-audit.md) —
  the adversarial grounding audit of this doc (C4): claim-by-claim verdicts, 8/8 §2 code facts
  verified line-exact, citation spot-checks, findings F1–F7 with the paste-ready corrections
  this v2 applied, and the two computations (§5) it demanded before the flagship could be
  claimed authorable.
- Local ground truth: every claim in §2 carries its `file:line` at bikar `main` `73514f1`.

## Appendix B — counter-evidence and divergences

### B.1 — "Convention over configuration" argues against a new explicit mode

*Counter-position:* the Rails doctrine — "there are thousands of such decisions that just need
to be made once, and if someone else can do it for you, all the better" — and DHH's broader
case that demanding declarations for inferable intent is ceremony
(<https://rubyonrails.org/doctrine>, survey §3).
*Why we diverge:* convention-over-configuration defends good **stable defaults**, and the
rectangular default stays. The auto rule this doc rejects is not a default but a *change of
meaning* for existing programs (`Star-Brick.bkr`'s body), which is the case Rails conventions
never cover and Rust/Python explicitly gate. DHH's own concession — "the hard part is knowing
when to stray from convention" — is this paragraph.

### B.2 — No fetched geometry library hard-errors on a degenerate inset

*Counter-position:* Clipper2 (precondition + winding repair), CGAL (split-or-vanish is a valid
result), OpenSCAD (documented silent vanishing, in the context of its double-offset Round
idiom — §5) — the industry treats offset degeneracy as geometry, not error (survey §4, scoped
to those three).
*Why we diverge:* those libraries return geometry to a *program*; bikar returns a part to a
*printer*, and the deleted geometry is cavity wall the clutch model reads as present (§5). Two
of bikar's three existing inset sites already throw. The divergence is deliberate and scoped:
V18 gates the *brick* path only, and general pattern offsets elsewhere keep library semantics.

### B.3 — The inset heuristic itself is still unverified (carried from lego-lab B.7)

lego-lab Appendix B.7 marks the crossing-span clip "still trusted rather than verified," with
the star-tip counterexample named. This doc does **not** discharge that bet — it contains it:
V18 converts the failure from silent wall loss into a refusal, and §6 requires the star-tip
case as a checked-in test. The heuristic's replacement (a real self-intersection-aware offset)
stays out of scope until a legal design is refused for wall it actually has — that event, not
this doc, justifies the rebuild.

### B.4 — Anchor-only clutch has zero prior art holding it up [CAL-ANC-01]

*Counter-position — the strongest in this doc, and it is consistent across every source the
survey could reach.* The original patent (US3005282A, claim 3) defines the clamp as a stud
"between at least one side wall **and** at least one secondary projection," with no tube-only
embodiment; LEGO's own explainer says studs wedge "between the tubes **and the sides**"; and —
the survey's headline, read from raw LDraw geometry — **every LEGO non-rectangular part
examined re-introduces wall contact rather than trusting the tube**: the 2×2 round brick
(3941/6143) and round plate (4032a) carry flat facet bands at exactly the stud-tangent plane
(16 LDU = 6.4 mm from part centre), while the centre-stud round plate (18674) and corner-cut
plate (26601) carry sculpted contact patches *straddling or near* that plane (≈14.7–16.7 and
≈15.3 LDU) — all four re-introduce wall contact in the band where studs engage (3941's facet
band is 1.6 mm tall; 6143's tube reaches 2.4 mm). The printed ecosystem points the same way:
PrintPal puts tuned clutch ridges *on the walls*; MachineBlocks pre-shrinks tubes 0.1 mm; and
FDM tubes are the worst-printed clutch feature on record (Brick Architect: "shallower and
misaligned"). Survey §7's verdict, quoted: the anchor-only bet "has **zero prior art holding
it up and a consistent LEGO-side pattern arguing against it**."
*What survives, and why the design proceeds:* the contact-count arithmetic
(`lego-lab-design.md` §3.3: walls are 50–67 % of contacts on small footprints) was never shown
to be a *force* share — no wall-vs-tube force distribution measurement exists anywhere the
survey reached, in either direction. That translation is exactly what the bet measures:
registered as `CAL-ANC-01`, settled by coupon **LG-B2** (rosette piece vs rectangular 2×4
control; the number is the retention *ratio*), provisional until printed.
*And the counter-evidence changed the design's fallback, not its surface.* The same LDraw
facts that refute "tube-only" show LEGO's actual solution for non-rectangular bodies: **short
tangent-plane pads** where the outline passes the stud circle, not a rectangular wall. If
LG-B2 under-retains, the answer is a pad feature — a ≤2.4 mm-tall flat at 6.4 mm from any
gripped stud centre, wherever the outline permits — which is a faithful port of 3941's
geometry with a writable K10 transfer condition (same contact plane, same engagement height,
same 8 mm lattice; only FDM dimensional error remains, which the existing fit-window
machinery already prices). That feature is deliberately **out of v1 scope** (§1): it is
LG-B2's *contingency*, and building it before the measurement would be paying for an answer
the coupon may hand us for free.

### B.5 — The 1.5 mm inset wall may not survive the slicer on a lobed outline [CAL-INW-01]

*Counter-position:* the printability survey's own caveats (survey §4): Arachne "has a tendency
to round concave corners" and plastic "tends to shrink into" them; Prusa's LEGO profile needed
0.4 mm of elephant-foot compensation — double the default, taken straight off the outline —
and the thin-wall guard that would protect a two-line wall is a slicer heuristic, not a
guarantee. V18 (§5) proves the *geometric* wall; nothing in this doc can prove the printed one.
*Status:* **empirical — no literature answers whether the compensation-vs-thin-wall-guard
interaction preserves a 1.5 mm inset wall that follows a concave lobed outline.** Registered as
`CAL-INW-01`, settled by the same LG-B2 print that settles B.4 (one coupon, two quantities —
the W-C1 precedent). Until then, every printed-wall claim here inherits the provisional
qualifier.

### B.6 — Most surveyed tools call the concept "shape," not "outline"

*Counter-position:* brickify and base-plate-outliner both say "shape"; "outline" as a noun for
the body boundary is attested mainly by our own tile statement and kernel field (survey §5).
*Why we diverge:* in-language consistency beats cross-tool consistency for a word a `.bkr`
author already knows: bikar has an `outline` statement and a `bodyOutline` field, and `shape`
would be a genuinely new word with the sweep cost the chosen surface exists to avoid.
