<!--
Provenance: adversarial grounding audit (C4), produced 2026-08-02 by a Claude
Fable 5 background audit agent (bikar source verification at main 73514f1,
9 external re-fetches, 1 raw LDraw re-download), preserved verbatim per the
ground-design-doc skill; only this header and the agent's one-line lead-in
were added/removed.
Feeds: docs/pattern-outline-brick-design.md (findings F1-F7 fixed in place).
-->


# Grounding audit: pattern-outline-brick-design.md

Audited 2026-08-02 against bikar `main` at `73514f1` (verified; `calibration.ts` uncommitted with CAL-ANC-01/CAL-INW-01 as expected), the two research files, the house docs, and 9 external fetches plus one raw LDraw primary-source download. Doc paths: `/Users/omareid/Workspace/git/3d-models/docs/pattern-outline-brick-design.md`; code at `/Users/omareid/Workspace/git/bikar-lego-lab`.

**Headline results:** all eight §2 engine-ground-truth facts verify **line-exact** — unusually clean. But the doc has one **false corpus claim** (a K2 of exactly the BOSL2 shape CLAUDE.md warns about), one **refuted §4 transfer claim** (a real cols/rows consumer that would mis-mint ports on an outline body), a **V18 tolerance rationale that is wrong on its own terms** with an unstated consequence that may refuse the flagship rosette, and a **V19 PASS example never run against the machinery it invokes** — with the evaluator's own comment suggesting it could fail.

## Claim-by-claim verdicts

| # | Claim | Verdict | Supporting evidence | Refuting/complicating evidence |
|---|---|---|---|---|
| 1 | §2: kernel already honours `bodyOutline` end-to-end; only the DSL surface is missing | **GROUNDED** | All 8 facts line-exact (see next section); `bodyOutline` set nowhere in evaluator (only read at L2423) | — |
| 2 | §3 corpus: 237 `.bkr`; `outline` "only as the tile statement and inside comments; never as a param, blueprint, pattern or declaration name" | **CONTESTED — evidence sentence false, conclusion survives** | 237 total confirmed (106+19+112+0) | `sacred-patterns/sessions/bikar-medallion-10/iterations/{20,27,28,29}/pattern.bkr` declare `boundary outline = union(...)` and reference it via `clip pattern to outline` — `outline` **is** a blueprint declaration name inside the searched set |
| 3 | §3 explicit-over-auto, Rust/`__future__`/PEP 20 precedent | **GROUNDED** (analogy slightly overstretched, but the doc writes the K10 hedge) | Rust editions quote verbatim ([edition-guide](https://doc.rust-lang.org/edition-guide/editions/index.html)); PEP 20 lines verbatim ([PEP 20](https://peps.python.org/pep-0020/)); Rails quotes verbatim ([doctrine](https://rubyonrails.org/doctrine)) | A purely *additive* mode word needs no editions-grade precedent at all; see deep dive 1 |
| 4 | §3 mode-on-`footprint` over new `body` statement; "`body` appears in no `.bkr` today" | **GROUNDED / minor overstatement** | No `body` statement or identifier exists | `body` appears in 5 `.bkr` files **in comments** (e.g. `bikar-lego-lab/patterns/Lego/Star-Brick.bkr:28`); claim needs "outside comments" |
| 5 | §4 "outline mode is `auto` plus a body substitution — every consumer of cols/rows … is a statement about the enclosing stud grid, not about the body ring" | **REFUTED as universal** | `solveAnchors`/anchorability/V2 do behave as claimed | `evaluator.ts:2409` `const bodyRing = rectangularBody(cols, rows, origin)` → passed to `mintDeclaredPorts` as `outline:` — declared `port` statements would be minted against the rectangle, not the body. Also V13's gate keys on `decl.footprint.kind === 'auto'` (`evaluator.ts:2401`, `brick-validate.ts:379`) — unstated decision |
| 6 | §5 hard-error is stricter-than-library, honestly stated | **GROUNDED** | Clipper2, OpenSCAD fetched and match; two in-kernel throw sites verified (`solidify-lattice.ts:170–174`, `solidify-piece.ts:425–428`) | OpenSCAD quote context nuance (see citations) |
| 7 | V18 spec: 0.05 mm tolerance "must merely exceed the vertex-placement error of `insetRing`'s miter clamp on legal inputs" and is `SNAP_THRESHOLD_MM` | **CONTESTED — constant verified, rationale false** | `SNAP_THRESHOLD_MM = 0.05` at `grid-gate.ts:110` ✓ | The miter clamp (`brick.ts:773–774`, `Math.max(0.2, …)`) puts any legal convex vertex sharper than ~23° interior angle at up to `d·(1−5·√cos)` short of the wall — errors of ~0.5–1 mm on *legal* inputs, 10–20× the tolerance. See deep dive 3 |
| 8 | V18 FAIL example: star tips → "the heuristic drops vertices … midpoint 0.3 mm from the body" | **CONTESTED (K7)** | V18 would still fire on this input | Contradicts the doc's own §2.6: `dropCrossingSpans` (`brick.ts:789`) only dedupes vertices <1e-6 apart and would drop nothing here; the actual mechanism is the clamp bowtie. "0.3 mm" is constructed, not computed |
| 9 | V19 PASS: "one rosette — one component, one simple outer ring" | **UNGROUNDED (ARGUED — locally checkable)** | — | Evaluator's face-grouping comment (above `groupFaces`, ~`evaluator.ts:2214`): "Faces meeting at a single *vertex* stay separate." Rosette petals meeting at point cusps would union to *multiple* edge-connected components → V19 refuses the flagship. Never run on a real rosette |
| 10 | B.4 anchor-only clutch counter-evidence and CAL-ANC-01 routing | **GROUNDED / EMPIRICAL, correctly routed** | US3005282A claim 3 verbatim ✓; lego.com quote verbatim ✓; raw `3941s01.dat` re-downloaded: `rect.dat` flats at 16 LDU, `1-8cyli` r=20, `stud4a` y=20 all confirmed; `CAL-ANC-01` at `calibration.ts:148` | "all carry flat facet bands at **exactly** the stud-tangent plane" strips the survey's own qualifiers: 18674 facets at r≈14.7–16.7 ("straddling"), 26601 at r≈15.3 — K1 |
| 11 | B.5 printed 1.5 mm inset wall / CAL-INW-01 | **EMPIRICAL, correctly routed** | `CAL-INW-01` at `calibration.ts:154`; survey's Prusa/Arachne sources | — |
| 12 | §2.7's claim that lego-lab §7.2's "fails V2" was a K7 drift | **GROUNDED** | `lego-lab-design.md:712` says it; `brick-validate.ts:148` V2 = pattern-fits-footprint; `insetRing` called only at `brick.ts:549` with no validator anywhere | — |
| 13 | V18/V19 numbering is next-free | **GROUNDED** | lego-lab V1–V13; `lego-pattern-set-design.md` §6 takes V14–V17 | — |
| 14 | §7 unblock claims (baseline entries, backlog note 10, catalog LG-B2) | **GROUNDED** | `doc-pointer-baseline.json:24,29` (two `Rosette-Brick.bkr` entries); `backlog.md:655`; catalog LG-B2 at `catalog.md:933` | — |

## Code-claim verification

Every §2 fact checked at `73514f1`. Verdicts: **8/8 line-exact** (a rarity worth noting — no drift found).

1. **Line-exact.** `readonly bodyOutline?: readonly Point[];` at `brick.ts:120`; `const body = spec.bodyOutline ?? rectangularBody(…)` at L545; `insetRing(spec.bodyOutline, effectiveWall(spec.fit))` at L549; second site `buildBrick` at L857. Quotes verbatim.
2. **Line-exact.** `export function solveAnchors(` at `grid-gate.ts:229`; `const cellReach = STUD_PITCH_MM / 2 - PART_RELIEF_MM / 2;` at L256 (= 3.9 mm exactly, as claimed); anchor drop test `const clear = signedDistToRing(p, bodyOutline);` at L279. The "rectangular c×r body engages every cell by construction" sentence is verbatim from the L243–255 comment.
3. **Line-exact.** `grid-gate.ts:351` is `if (studsEngaged < 2) {` — the doc states the gate as its contrapositive `studsEngaged >= 2`; same rule, same line.
4. **Line-exact.** `bodyOutline?: readonly Point[]` is literally line 133 of `brick-ports.ts`; `evaluator.ts:2423` passes `spec.bodyOutline` into `mintLatticePorts`. "Never non-undefined in production" confirmed: `bodyOutline` appears in the evaluator only at L1472/1474/2423 and `evaluateBrickDecl` never sets it.
5. **Verified.** L-shaped `bodyOutline` test with `studs: 'full'` spans `brick.test.ts:455–470` (the `buildBrick` call is L462–464, containing L463); `brick-top-face.test.ts` has exactly 8 `bodyOutline` occurrences (I counted occurrences, not proven-distinct fixtures — the doc's "eight fixtures" is consistent but I did not confirm they are 8 distinct fixtures).
6. **Line-exact, and the doc's "weaker than its comment" analysis is correct.** The quoted comment sits at `brick.ts:748–758` ("heuristic rather than a proof" is L752); `insetRing` at L759; `dropCrossingSpans` at L789, and its body confirms it only skips consecutive vertices `< 1e-6` apart — no self-intersection detection exists. The doc's §2.6 is the strongest paragraph in it.
7. **Verified.** `brick-validate.ts:148` is the "V2 / V9 — the pattern must fit the footprint" comment; `insetRing` has exactly one call site (`brick.ts:549`) and no validator reads its output; `lego-lab-design.md:712` contains the "fails V2" sentence the doc calls a drift.
8. **Line-exact.** `resolveBrickFootprint` at `evaluator.ts:2445` with the two-arm switch; `studsFor` (in `brick-validate.ts:126`) is least-n-such-that-`footprintMm(n) ≥ mm`; parser refusal of `footprint auto` without `inscribe` at `parser.ts:638–640`; `resolveBrickArt` at `evaluator.ts:2182` computes the bbox centre used for recentring.

Also verified: `SNAP_THRESHOLD_MM = 0.05` (`grid-gate.ts:110`); `solidify-lattice.ts:170–174` throw ("degenerates at strut half-width inset"); `solidify-piece.ts:425–428` ("the outline is likely self-intersecting"); `keywords.snapshot.txt` (`packages/core/tests/fixtures/`) contains neither `outline` nor `footprint`, consistent with "unchanged"; `CAL-ANC-01`/`CAL-INW-01` present in uncommitted `calibration.ts` at L148/L154.

**Corpus claim:** 237 `.bkr` confirmed (bikar-lego-lab 106, 3d-models 19, sacred-patterns 112, coffee-house-sites 0). The `outline` absence claim is **false** — see next section.

## Internal-consistency findings

**F1 (K2, the BOSL2 shape — the doc's §3 corpus sentence is falsified by its own searched set).** The doc: "finds `outline` only as the existing tile statement and inside comments; never as a param, blueprint, pattern or declaration name." Refutation, from the doc's own grep scope:

```
sacred-patterns/sessions/bikar-medallion-10/iterations/20/pattern.bkr:63:  boundary outline = union(C0)
sacred-patterns/sessions/bikar-medallion-10/iterations/20/pattern.bkr:98:  clip pattern to outline
```
(and iterations 27, 28, 29 likewise; `boundary` is real blueprint grammar — `parser.ts:1145` lists it among allowed blueprint statements.) `outline` **is a user-declared boundary name** — one of the exact categories the sentence denies. The design *conclusion* survives: `footprint <word>` is parsed only inside a brick declaration, a context disjoint from blueprint boundary names, so zero programs change meaning — and the finding actually *illustrates* the contextual-words argument. But the evidence sentence is wrong, and it is the same failure CLAUDE.md's K2 entry documents (`piece-composition` vs BOSL2). Similarly minor: "`body` appears in no `.bkr` today" — it appears in comments in 5 files.

**F2 (K7 — §5's V18 FAIL example contradicts §2.6).** §2.6 correctly establishes that `dropCrossingSpans` never drops crossing spans (only near-coincident duplicates). §5's FAIL narrative then says "the heuristic drops vertices, and the surviving ring has a midpoint 0.3 mm from the body." Per the code the doc itself analyzed, no vertex would be dropped at a 0.8 mm star tip; instead the miter clamp (`scale = d / Math.max(0.2, √cos)`, `brick.ts:772–774`) throws the tip vertex up to 5·d = 7.5 mm along the inward bisector, producing a self-crossing bowtie with all vertices intact. V18's *verdict* (FAIL) survives — points land at small/negative signed distance — but the narrated mechanism is the comment's fiction, not the code's behavior, and "0.3 mm" is an invented number. §6 then requires this example "verbatim from §5" as a checked-in test, which would enshrine the wrong mechanism (or fail to reproduce the narrated numbers).

**F3 (K7, flagship-risk — V18's tolerance rationale is false, and the unstated consequence may refuse the LG-B2 rosette).** The doc: 0.05 mm "must merely exceed the vertex-placement error of `insetRing`'s miter clamp on legal inputs." The clamp caps scale at `d/0.2`; for a legal simple ring with a convex vertex of interior angle θ < ~23° (where `√cos < 0.2`, `cos = cos²(θ/2)` per L773), the returned vertex sits `5d·√cos < d` from the adjacent edges — e.g. at θ = 10°, ≈0.65 mm instead of 1.5 mm, a 0.85 mm shortfall, 17× the tolerance. So V18 as specified hard-errors **every pattern with a convex vertex sharper than ~23°** — arguably the *correct* refusal (the solid genuinely lacks wall there), but: (a) the tolerance rationale is wrong as written; (b) the consequence — a hard floor on cusp sharpness in outline mode — appears nowhere in the doc; (c) five-fold rosette petals typically meet in cusps far sharper than 23°, so the flagship `Rosette-Brick.bkr` this whole extension exists to unblock may be uncompilable under v1. This is the CLAUDE.md K7 flagship pattern ("can the flagship example be built by the machinery the doc ships?"). B.3's trigger ("until a legal design is refused for wall it actually has") would also mis-fire: the refusal would be for wall the solid actually *lacks*, so B.3's escape clause never opens.

**F4 (V19 PASS example never executed).** "One rosette — one component" assumes the rosette's face union is *edge*-connected. The evaluator's own grouping comment (above `groupFaces`, ~`evaluator.ts:2210–2225`) states "Faces meeting at a single *vertex* stay separate." If the rosette's petals meet only at point cusps — common in girih/rosette constructions — the union is many components and V19 refuses the flagship. This is checkable today without printing anything: run `unionPatternFaces` on a `patterns/Rosettes/*.bkr` source. The doc asserts the PASS without having done so.

**F5 (§4's universal-consumer claim refuted — see deep dive 2).**

**F6 (K1 — B.4 strips its own survey's qualifiers).** Doc: the four LDraw parts "all carry flat facet bands at **exactly** the stud-tangent plane (16 LDU = 6.4 mm from part centre) in the 1.6–2.4 mm band." Survey: exact 16 LDU holds for 3941/4032a; 18674's facets are "at x ≈ 14.7–16.7 LDU … **straddling** the 16 LDU tangent plane"; 26601's are at "r ≈ 15.3 LDU … near the two studs." And "1.6–2.4 mm band" conflates 3941's 1.6 mm facet band with 6143's 2.4 mm *tube* height. The verbatim B.4 quote of the survey's verdict ("zero prior art holding it up and a consistent LEGO-side pattern arguing against it") does match the research file exactly (it sits in the "Bottom line" paragraph after §7's table, not in the table itself — attribution "Survey §7's verdict" is acceptable).

**F7 (cosmetic, propagated misnomer).** The kernel comment the doc quotes calls a star tip "a deeply reflex vertex." An outer ring's star tip is a *convex* vertex (the notch between tips is the reflex one), and inward-offset self-intersection at narrow tips is a convex-vertex phenomenon — which matters because F3's clamp analysis keys on convex angles. Worth one clarifying clause since two validators' engineering hinges on which vertex class misbehaves.

## Counter-evidence deep dives

**1. The Rust-editions/`__future__` analogy is doing less work than its billing (K10 attack a).** Editions are global, time-indexed, tooling-supported migration vehicles (cargo fix, cross-edition interop guarantees, "every edition compiles forever"); `footprint outline` is a per-declaration additive mode. More fundamentally: a *new mode word that no existing program contains* needs no opt-in precedent at all — languages add additive syntax constantly without edition machinery; editions exist for the case where *old* code's meaning would change. The analogy therefore only bears on the **rejected** auto rule (which genuinely would reinterpret `Star-Brick.bkr`), and there the load-bearing principle is just "don't change the meaning of existing programs," for which PEP 20's "refuse the temptation to guess" is sufficient. To the doc's credit, its K10 sentence ("they transfer not by mechanism but because the hazard is identical") already concedes most of this. Verdict: keep the citation, demote it one register — it justifies rejecting the auto rule, not choosing the mode surface.

**2. The grid-derivation reuse claim has real counterexamples (K10 attack b).** The doc claims "every consumer of `cols`/`rows` downstream of the spec … is a statement about the enclosing stud grid, not about the body ring," and that the single dangerous assumption is the one `solveAnchors` avoids. Found in code:

- **`evaluator.ts:2409`**: `const bodyRing = rectangularBody(cols, rows, origin);` handed to `mintDeclaredPorts` as `{ …, outline: bodyRing }`. This ring **is a body-ring claim** derived from cols/rows. A brick with declared `port` statements in outline mode would get ports minted on the rectangle's perimeter — floating in air off the true silhouette, or buried inside it. §6's change table does not touch this line. (The doc's §1 statement list itself includes `port` as a brick statement, so this is in-scope grammar, not a corner case.)
- **V13's predicate**: `footprintAuto: decl.footprint.kind === 'auto'` (`evaluator.ts:2401`; gate at `brick-validate.ts:379`), and the same flag stored in `brick3d` provenance at L2432 for the Lab. Under `kind === 'outline'` the dead-border advisory silently never fires and the Lab records `footprintAuto: false`. Defensible (outline mode has no rectangular border to warn about) — but it is a decision, the doc's universal claim hides that it exists, and §6 doesn't say which way to take it.
- **Late-failure ergonomics (constructed case)**: a 12 mm-wide rosette → `studsFor(12) = 2` → 2-stud grid, stud centres at ±4 mm; engagement needs `signedDistToRing ≥ 3.9 mm` at each centre, but the body reaches only 6 mm from centre → **0 cells engaged** → anchorability hard-fails with "only 0 lattice cell(s) are fully covered by the body (need 2 — one stud does not lock rotation)" — an error that never mentions outline mode, while V2 passed trivially (the grid was rounded up from the *same* bbox, so the fit check can never fire first). Not silent wrongness — the doc's §2.3 story holds — but the practical floor is unstated: **an outline body must fully cover at least two 8 mm lattice cells (roughly: contain a lattice-aligned 16×8 mm solid region)**; small or lacy patterns are structurally incompatible with outline mode and the author finds out at the last gate with no outline-specific hint.

**3. V18's miter-clamp interaction (detailed in F3).** The refuting source is the doc's own quoted code: `const scale = d / Math.max(0.2, Math.sqrt(Math.max(cos, 0)));` (`brick.ts:773–774`). The tolerance claim inverts reality: on sharp-but-legal inputs the clamp error *dwarfs* 0.05 mm by design. Either V18's threshold semantics must be restated ("V18 intentionally refuses geometry whose clamped inset thins the wall — including legal sharp cusps"), or the rosette needs pre-rounded cusps, or `insetRing` needs the real offset B.3 defers. This is the one place where counter-evidence should **change the design text**, not just its citations: v1 as specced likely cannot compile its own flagship, and the doc should either demonstrate a compiling rosette (run the union + inset numerically — an afternoon, no printer) or say explicitly that cusp-rounding is a precondition of outline mode.

**4. Anchor-only clutch (B.4) — counter-evidence verified at the primary source and correctly contained.** I re-downloaded `s/3941s01.dat` raw: `1 16 16 22 0 0 1 0 -2 0 0 0 0 11.36 rect.dat` (flat at x=16 LDU, y 20–24), `1-8cyli` at (18.47759, 7.65367) → r = 20 exactly, `stud4a` at y=20 — the survey's flagship geometric claim is real, not a fetch artifact. US3005282A claim 3 and lego.com's "between the tubes and the sides" both verified verbatim. The doc's handling is a model of the graduation rule: the physical question is routed to CAL-ANC-01/LG-B2, the design proceeds on the (correct) observation that no wall-vs-tube *force* measurement exists in either direction, and the tangent-pad contingency is a fair reading of the LDraw evidence. No change needed beyond F6's qualifier restoration.

## Citation spot-check results

| Source | Claimed | Found | Verdict |
|---|---|---|---|
| [US3005282A](https://patents.google.com/patent/US3005282A/en) | Claim 3: stud "clamped between at least one side wall and at least one secondary projection"; tangency to both; no tube-only embodiment | All three verbatim/confirmed | ✓ |
| [Rust edition guide](https://doc.rust-lang.org/edition-guide/editions/index.html) | "Since editions are opt-in, existing crates won't use the changes unless they explicitly migrate…" | Exact sentence present | ✓ |
| [PEP 20](https://peps.python.org/pep-0020/) | Three quoted lines | All three verbatim | ✓ |
| [Clipper2 ClipperOffset](https://www.angusj.com/clipper2/Docs/Units/Clipper.Offset/Classes/ClipperOffset/_Body.htm) | "should **not** be performed on **intersecting closed paths**…"; Union pre-clean; NonZero; page silent on vanish-to-nothing | All confirmed, including the silence (which the survey honestly recorded) | ✓ |
| [OpenSCAD Transformations](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations) | "walls less than 2*r thick vanish"; `resize auto` "auto-scales any 0-dimensions to match" | Both verbatim — **but** the vanish line documents the `offset(r=+3) offset(delta=-3)` *Round idiom*, not a bare single inward offset | ✓ with context nuance (see below) |
| [Rails Doctrine](https://rubyonrails.org/doctrine) | Three DHH quotes in B.1 | All three verbatim | ✓ |
| [lego.com explainer](https://www.lego.com/en-us/service/help-topics/article/how-do-lego-bricks-work) | "wedged in between the tubes and the sides" | Verbatim | ✓ |
| [brickify README](https://raw.githubusercontent.com/richfelker/brickify/master/README.md) (github.com 503'd; raw fetched) | "studs appear only in positions where they fully fit within the object"; first-quadrant/stud-cell units; "2D object" terminology | All verbatim — note the stud sentence appears in the *custom-mask* context; doc §2.2 cites it as brickify's general stud semantics | ✓ minor context nuance |
| [LDraw s/3941s01.dat](https://library.ldraw.org/library/official/parts/s/3941s01.dat) (raw) | 16 LDU flats, r-20 arcs, stud4a tube | Confirmed line-by-line | ✓ |

Not re-fetched by this audit (survey-fetched only, unchallenged): CGAL straight skeleton, Configuration Complexity Clock, Prusa/Brick Architect/PrintPal articles. The survey's own hedges on fetch-model paraphrase (CadQuery "may fail", Hadlow quote) are properly carried.

## Misgrounded or missing citations

1. **§3 corpus sentence** — misgrounded by its own grep (F1). Needs the correction below, plus "outside comments" on the `body` claim.
2. **V18 tolerance sentence** — the `SNAP_THRESHOLD_MM` citation is real but the engineering claim it decorates is false (F3). The constant survives; the rationale must be rewritten.
3. **§5/B.2 OpenSCAD** — "documents silent feature loss" is fair, but the quoted "walls … vanish" sentence is about the double-offset Round idiom; a one-clause context fix keeps the citation honest.
4. **B.4 "exactly the stud-tangent plane"** — over-claims relative to the cited survey for 18674/26601 (F6).
5. **§4** — cites no source for the "every consumer" claim because it is a code claim; the code refutes it at `evaluator.ts:2409` (F5). Missing: a citation-by-line for each consumer, which is what would have caught it.
6. **V19 PASS** — missing the one piece of evidence that is free: an actual run of `unionPatternFaces` on a rosette (F4).

## Recommended doc changes

**1. Replace the §3 corpus paragraph (fixes F1):**

> **Corpus evidence (K2 scope: exactly what was searched).** A grep over all 237 `.bkr` files under the four working trees swept by this repo's Stop hook — bikar (`bikar-lego-lab` worktree), 3d-models, sacred-patterns, coffee-house-sites, on 2026-08-02 — finds `outline` as the tile statement, inside comments, inside longer identifiers (`warp_outline`), **and as a user-declared blueprint boundary name in four sacred-patterns files** (`boundary outline = union(…)` / `clip pattern to outline`, `sessions/bikar-medallion-10/iterations/{20,27,28,29}/pattern.bkr`). None of these collides with the extension: `footprint <word>` is parsed only inside a `brick` declaration, and statement words are contextual precisely so authors may keep using them as names — which those files already do. No file contains `footprint outline`, so the extension changes the meaning of zero existing programs.

**2. Rewrite V18's tolerance paragraph and FAIL example (fixes F2, F3) — and add the consequence:**

> The 0.05 mm tolerance is `SNAP_THRESHOLD_MM` (`bikar:packages/core/src/kernel3d/grid-gate.ts`), reused so no new constant is minted. It does **not** bound `insetRing`'s error on all legal inputs: the miter clamp (`Math.max(0.2, √cos)`, `brick.ts` L773) places any convex vertex sharper than ≈23° interior angle materially closer than `wall` to the body — by design, since an unclamped miter would run away. V18 therefore refuses every outline whose cusps are sharper than ≈23°, and that refusal is correct: the shipped solid genuinely thins there. **Consequence, stated as a precondition:** outline mode requires cusp interior angles ≥ ≈23° (or pre-rounded cusps in the pattern); whether `Rosette-Brick.bkr`'s five-fold cusps clear this floor must be computed before this doc's flagship is claimed authorable.
> FAIL: a five-point star with 0.8 mm-wide tips — the clamp throws each tip vertex up to 5·wall along the bisector, the returned ring self-crosses, and V18 finds points at negative clearance and refuses, where today's kernel ships the solid. (Note the code path is the clamp, not the comment's promised crossing-span drop — §2.6.)

**3. Correct §4's transfer claim and extend §6 (fixes F5, deep dive 2):**

> **Transfer condition (K10):** this reuse is sound for the lattice consumers — origin, anchor enumeration, height rules, V2 — because each is a statement about the enclosing stud grid, and the kernel re-tests every cell and anchor against the actual ring (§2.2). Two consumers are **not** grid statements and need explicit handling: (a) `evaluateBrickDecl` mints *declared* ports against `rectangularBody(cols, rows, origin)` (`evaluator.ts` L2409) — in outline mode that ring must be the body ring, or declared `port` statements are refused in v1; (b) V13's dead-border advisory keys on `kind === 'auto'` (`evaluator.ts` L2401) and stays off in outline mode — correct, because the body follows the art and there is no rectangular border, but it is a decision, recorded here.

Add to §6's table: a `mintDeclaredPorts` row, a V13-predicate row, and a row extending the anchorability failure message with an outline-mode hint ("the body must fully cover ≥ 2 lattice cells; small or lacy outlines cannot engage the grid").

**4. Gate V19's PASS example on a real run (fixes F4):** before the doc leaves "audit pending," run `unionPatternFaces` on the actual rosette source (`patterns/Rosettes/*.bkr`) and record the component count. The evaluator's grouping rule keeps vertex-touching faces separate (`evaluator.ts` ~L2214), so a cusps-meeting-at-points rosette may be *many* components — if so, V19 as specified refuses the flagship and the doc needs either a vertex-merge rule (with its own validator) or a different flagship pattern. This is a no-printer, same-day check.

**5. Restore B.4's qualifiers (fixes F6):** "…the round brick (3941/6143) and round plate (4032a) carry flat facet bands at exactly the stud-tangent plane (16 LDU = 6.4 mm), while the centre-stud round plate (18674) and corner-cut plate (26601) carry sculpted contact patches *straddling or near* that plane (r ≈ 14.7–16.7 and ≈15.3 LDU) — all four re-introduce wall contact in the band where studs engage (1.6 mm facet bands; 6143's tube reaches 2.4 mm)."

**6. Demote the editions analogy one register (deep dive 1), e.g. append to §3:** "Strictly, no opt-in precedent is needed for the mode itself — an additive word no program contains changes nothing; editions and `__future__` bear only on the rejected auto rule, which is the case where existing programs' meaning would drift."

**7. One-clause context fixes:** OpenSCAD's "walls less than 2*r thick vanish" is documented for the `offset(r=+3) offset(delta=-3)` Round idiom (silent thin-feature loss is still the accurate takeaway); brickify's stud sentence appears in its custom-mask section; "`body` appears in no `.bkr` today **outside comments** (5 files mention it in prose)"; and the kernel comment's "deeply reflex vertex (a star tip)" should be glossed — an outer-ring star tip is a narrow *convex* vertex, which is exactly the class V18's clamp analysis governs.

**Divergence justifications that stand (no change needed):** B.2's stricter-than-library error policy — the survey's finding is quoted fairly ("Clipper2 treats self-intersecting input as a caller precondition… none of the three fetched libraries errors"), and the manufacturing-semantics + two-in-kernel-throw-sites argument is verified and sound. B.4's proceed-despite-zero-prior-art — the counter-evidence is quoted at full strength, verified here down to the raw LDraw lines, and correctly converted into a registered empirical bet (CAL-ANC-01) plus a designed contingency rather than a doc claim. B.5 likewise (CAL-INW-01). These three are exemplary; the doc's weaknesses are all in the places it reasoned *about its own code and corpus* rather than about the outside world.

---

## Post-audit addendum: the F3/F4 computations, executed (NOT part of the verbatim agent report)

<!--
Provenance: added 2026-08-02 by the session that applied the audit's findings,
after the verbatim report above. Method: a scratch tsx script driving bikar's
own `evaluate()` (packages/core/src/dsl/evaluator.ts:845) at main 73514f1,
with line-faithful local replicas of the module-private relief-path helpers
`faceComponents` (evaluator.ts:2231), `collectBoundaryEdges` (:1260) and
`chainBoundaryRings` (:1280), plus interior-angle measurement on the union's
outer ring. The clamp floor derives from brick.ts:773-774:
cos = (1 + n1.n2)/2 = sin^2(theta/2), so the clamp engages below
theta = 2*arcsin(0.2) = 23.07 deg. (Recommended-change 2's gloss
"cos = cos^2(theta/2)" in the report above is itself a misstatement; the
conclusion ~23 deg is unaffected.)
-->

All eight rosette sources in bikar at `73514f1` were evaluated — the seven
`patterns/Rosettes/*.bkr` plus `patterns/Rosette-12.bkr`:

| Source | Bounded faces | Components | Boundary rings | Outer-ring verts | Min convex interior angle |
|---|---|---|---|---|---|
| Rosettes/Rosette-10.bkr | 30 | **1** | 1 (0 holes) | 20 | **72.00°** |
| Rosettes/Flower-Rosette.bkr | 61 | **1** | 1 (0 holes) | 12 | 150.00° |
| Rosette-12.bkr | 85 | **1** | 1 (0 holes) | 12 | 150.00° |
| Rosettes/Andalusian.bkr | 109 | **1** | 1 (0 holes) | 12 | 150.00° |
| Rosettes/Rosette-12r.bkr | 48 | **1** | 1 (0 holes) | 24 | 90.00° |
| Rosettes/Ocean-Rosette.bkr | 85 | **1** | 1 (0 holes) | 12 | 150.00° |
| Rosettes/Rosette-10-Ring.bkr | 201 | **1** | 1 (0 holes) | 70 | **72.00°** |
| Rosettes/Rosette-10-Tiled.bkr | 390 | **1** | 1 (0 holes) | 70 | **72.00°** |

**F4 verdict: resolved, PASS branch.** Every source is exactly one
edge-connected component — because the relief path unions *all* bounded faces
(the fully tiled disc: kites, inter-petal triangles, spokes), not the petal
silhouette. The feared petals-touching-at-points geometry cannot arise from
these sources; if constructed deliberately, it is refused twice over
(edge-based grouping splits vertex-touching faces into components, and
`chainBoundaryRings` hard-errors on a boundary pinch — evaluator.ts:1280).

**F3 verdict: resolved, PASS branch.** Sharpest convex vertex in the corpus is
72° (the decagonal points of the three 10-fold sources) vs the 23.07° clamp
floor — 3× clearance. The flagship `Rosette-Brick.bkr` is authorable under v1
as specced, with no cusp-rounding precondition. The precondition itself is now
stated in the design doc's V18 section.
