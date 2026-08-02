<!--
Provenance: adversarial research survey, produced 2026-08-02 by a Claude
Fable 5 background research agent (web fetches + direct bikar source reads),
preserved verbatim per the ground-design-doc skill; only this header and the
agent's one-line lead-in were added/removed.
Feeds: docs/pattern-outline-brick-design.md (Appendix A/B).
-->


# Research: DSL surface for pattern-outline bodies

Date: 2026-08-02. Produced by adversarial research agent (web + local source reads). Feeds the brick body-outline language-surface design. All "fetched" sources were retrieved 2026-08-02 via WebFetch (content summarized by a fetch-side model; quotes below are as returned by that fetch and marked where verbatim status is uncertain). Local `bikar` claims were read directly from source at the working tree current on 2026-08-02.

## 1. Brick-generator prior art (what knobs exist, with sources)

Four generators were fetched and read; two more are known only from search snippets. This is not an exhaustive survey of LEGO generators — it covers the six named below and no others.

**brickify (richfelker) — the closest prior art, and it chose implicit-by-construction.**
The module takes an arbitrary OpenSCAD 2D object as a *child* and produces a brick of matching shape: `brickify() square([2,4]);`. The README (per fetch) "expects the 2D object it operates on to be in the first quadrant, with units in stud cells," calls the input just "the 2D object" (no term like outline/profile/footprint), and derives walls, posts, splines, and studs from it — "studs appear only in positions where they fully fit within the object." No discussion of concave/degenerate handling was found in the README. Note the structural difference from bikar: in brickify the shape-to-body mapping is the module's *only* behavior, so passing a shape *is* the explicit trigger; there is no rectangular default to silently displace. https://github.com/richfelker/brickify (fetched)

**LEGO.scad (cfinke) — named mode enum, no custom outline.**
Non-rectangular bodies are selected by a `type` parameter with an enumerated set: `"brick"`, `"tile"`, `"wing"`, `"slope"`, `"curve"`, `"baseplate"`, `"round"`, `"round-tile"`, each refined by dedicated parameters (`wing_type`, `round_radius`, `curve_type`, …). A mode word chooses the body family; there is no arbitrary-outline input. https://github.com/cfinke/LEGO.scad (fetched)

**MachineBlocks (pks5) — rectangle only.**
`lib/block.scad` was fetched raw: the body is controlled by `size` ("vector3 x grid ([x, y, z]) - Size of the brick as multiple of the grid unit"), `baseHeight` (`mm | 'auto'`), `baseSideAdjustment`, `scale`. Per the fetch, "the base is always rectangular… No parameters named `outline`, `shape`, `contour`, or `profile` exist in this module"; the only shape variations are `bevel`, `slope`, `crop`. Two `auto` precedents inside a brick generator: `baseHeight: 'auto'` derives height from size. https://github.com/pks5/machineblocks, https://raw.githubusercontent.com/pks5/machineblocks/master/lib/block.scad (both fetched)

**base-plate-outliner (dlvoy) — outline from raster, called a "shape."**
"The script analyzes a reference PNG image to identify a shape (dark pixels = inside, light pixels = outside)… then optimally decomposes the shape into rectangular baseplates." The boundary choice is expressed by `-t, --threshold` (grayscale cut), with `--edge [THICKNESS]` and `--frame` as alternative body modes. Terminology is consistently "shape," not outline/contour/silhouette — despite "outliner" in the project name. Complexity is handled by decomposition into rectangles, not by hard error. https://github.com/dlvoy/base-plate-outliner (fetched)

**BRICK.scad (mlkood), OpenSCADLEGO (anandamous)** — (unverified snippets from search results only): BRICK.scad appears to be a LEGO.scad derivative with the same type-enum approach; OpenSCADLEGO exposes block type/length/width/height. Not fetched; do not cite beyond existence.

Summary: among the four generators actually read, none has bikar's exact situation — a rectangular default *and* an arbitrary-outline option in the same declaration. The two poles are LEGO.scad (explicit mode enum, closed shape set) and brickify (arbitrary shape, but as the module's sole input, so no silent-change hazard existed to design around).

## 2. CAD DSL mode-choice precedent (derived vs explicit dimensions)

**OpenSCAD `resize(..., auto=true)` is the cleanest precedent for a named derive-instead-of-specify mode.** Per the wikibooks manual, `auto=true` "auto-scales any 0-dimensions to match" — the author explicitly writes a mode word to say "derive this dimension," and can even do it per-axis (`auto=[true,true,false]`). A `0` without `auto` means "leave as-is": the same literal input means two different things depending on an explicit flag, which is precisely the `footprint auto` / `footprint outline` shape. https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations (fetched)

**MachineBlocks `baseHeight: 'auto'`** (§1) is the same pattern inside a brick generator: a keyword value selecting derived-from-context over explicit millimetres — directly analogous to bikar's existing `footprint auto`.

**CadQuery** builds solids from "profiles"/"pending wires" (`extrude` operates on pending wires; the 2D shape being extruded is the "profile"). `Workplane.offset2D(d, kind='arc')` exposes corner treatment as a named `kind` enum (`'arc'`, `'intersection'`, `'tangent'`) — precedent for spelling geometric-policy choices as small named enums rather than booleans. The fetch's statement that degenerate offsets "may fail to produce valid output" is the fetch model's paraphrase, not a verbatim doc quote — treat as low-confidence. https://cadquery.readthedocs.io/en/latest/classreference.html (fetched)

**JSCAD** `expand`/`offset` take `delta` (negative = contract; "delta of offset (+ to exterior, - from interior)") and `corners: 'edge'|'chamfer'|'round'` — again a named-enum policy knob. "No specific warnings about degenerate results appear" in the fetched docs. https://openjscad.xyz/docs/module-modeling_expansions.html (fetched)

**KittyCAD KCL**: https://zoo.dev/docs/kcl-lang/foundations returned 404; not fetched, no claims made. ImplicitCAD was not fetched.

Summary: a named mode value choosing derived-vs-explicit is well-precedented (OpenSCAD `resize auto`, MachineBlocks `baseHeight auto`, bikar's own `footprint auto` / `anchors auto` / `clutch auto`). No fetched CAD DSL was found that *silently* switches body derivation based on geometry properties; but only the five systems above were checked.

## 3. Explicit-vs-implicit: the language-design argument, both sides

**For explicit opt-in when semantics of existing programs would change:**

- **Rust editions** are the strongest industrial precedent. "When there are backwards-incompatible changes, they are pushed into the next edition. Since editions are opt-in, existing crates won't use the changes unless they explicitly migrate into the new edition." Each crate declares its edition in `Cargo.toml`; the change of meaning is never ambient. https://doc.rust-lang.org/edition-guide/editions/index.html (fetched)
- **Python `__future__` statements**: "The future statement is intended to ease migration to future versions of Python that introduce incompatible changes to the language" — an explicit per-module directive, required because "changes to the semantics of core constructs are often implemented by generating different code… Such decisions cannot be pushed off until runtime." The parallel to a compiler-visible `footprint outline` statement (vs. inferring from pattern geometry at evaluation time) is direct. https://docs.python.org/3/reference/simple_stmts.html#future-statements (fetched)
- **PEP 20**: "Explicit is better than implicit." / "In the face of ambiguity, refuse the temptation to guess." / "Errors should never pass silently. Unless explicitly silenced." The second line bears on the rejected auto rule (pattern-touches-bbox is a guess about intent); the third bears on §4's degeneracy question. https://peps.python.org/pep-0020/ (fetched)

Applicability note (K10): editions and `__future__` govern *language-version* migration, not per-feature modes. They transfer here because the hazard is identical — an existing program whose output would change under a new interpretation — not because the mechanism (a version declaration) is the right surface.

**The steelman — smart defaults, and the cost of mode proliferation:**

- **Rails Doctrine, "Convention over Configuration" (DHH)**: "There are thousands of such decisions that just need to be made once, and if someone else can do it for you, all the better"; "by giving up vain individuality, you can leapfrog the toils of mundane decisions." But DHH concedes the limit himself: "most applications worth building have some elements that are unique in some way… The hard part is knowing when to stray from convention." https://rubyonrails.org/doctrine (fetched)
- **The Configuration Complexity Clock (Mike Hadlow, 2012)**: each move from hard-coded value → config flag → rules engine → ad-hoc DSL adds complexity and bugs, ending in "hard coding everything, except now in a much crappier language"; "at a certain level of complexity, hard-coding a solution may be the least evil option" (quote as returned by fetch). This is the live warning against growing `brick` a new knob per body policy. https://mikehadlow.blogspot.com/2012/05/configuration-complexity-clock.html (fetched)

How the steelman cuts here: Convention-over-configuration argues for good *defaults*, not for *changing* an established default out from under existing programs — Rails conventions are stable precisely so programs keep meaning the same thing. Hadlow's warning argues against a proliferation of knobs, which favors extending the existing `footprint` mode set over adding a second orthogonal statement. Neither fetched source defends silently reinterpreting existing inputs.

## 4. Inset/offset degeneracy semantics in established geometry tools

The question: when the pattern-derived body outline is inset 1.5 mm for the cavity wall and the inset self-intersects or vanishes, is "hard error" standard practice? Finding: **no single standard exists; the three fetched libraries choose three different semantics, and none of them is "hard error" — but none of them is a manufacturing DSL either.**

- **Clipper2** (Angus Johnson): "Offsetting should **not** be performed on **intersecting closed paths**, as doing so will almost always produce undesirable results" — self-intersections must be removed by a Union operation *before* offsetting; solution winding matches input, and hole-bearing polygons "should comply with **NonZero filling**." I.e., Clipper's contract is *precondition on the caller + winding-rule cleanup*, not an error. The fetched page does not state what happens when an inset shrinks a path to nothing. https://www.angusj.com/clipper2/Docs/Units/Clipper.Offset/Classes/ClipperOffset/_Body.htm (fetched)
- **CGAL 2D Straight Skeleton**: inward offsets are *well-defined* even when topology changes — "An offset polygon can have fewer, equal, or more sides as its source polygon. It can even be composed of multiple polygons," and at large distances offsets vanish. Preconditions are strict (weakly simple polygon, CCW outer/CW holes); behavior outside them is simply out of documented scope. Semantics: *split-or-vanish is a valid answer, not an error*. https://doc.cgal.org/latest/Straight_skeleton_2/index.html (fetched)
- **OpenSCAD `offset`**: features silently disappear — "holes less than 2*r in diameter vanish," "walls less than 2*r thick vanish." Silent geometry loss is the documented behavior. https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations (fetched)
- **JSCAD**: no degeneracy discussion found in fetched docs. **CadQuery/OCCT**: fetch paraphrase only ("may fail"), low confidence.

**bikar's own kernel already holds both positions** (read directly from source):
- `packages/core/src/kernel3d/brick.ts:759` `insetRing` is a straight polyline inset whose doc comment admits it "is a heuristic rather than a proof: a concave vertex whose offset self-intersects is clipped by dropping the crossing span. Appendix B.7 still carries this as unverified — the counterexample to look for is a deeply reflex vertex (a star tip) where the dropped span removes wall the anchor test then assumes is present." Silent-repair, self-flagged as the risk case for *exactly* the star-shaped bodies this feature targets.
- `packages/core/src/kernel3d/solidify-lattice.ts:172` throws when a void "degenerates at strut half-width inset" — hard error on inset degeneracy, in the same kernel.
- `packages/core/src/kernel3d/solidify-piece.ts:427` errors with "the outline is likely self-intersecting."

So "inset degenerates → hard error" is **not** what general-purpose geometry libraries do (they repair, redefine, or silently drop), but it **is** what two of bikar's three existing inset sites do, and PEP 20's "Errors should never pass silently" plus the physical stake (a dropped span deletes cavity wall the anchor/clutch model assumes exists) argue the DSL layer should error even though libraries don't. The honest statement for the design doc: hard error is a *stricter-than-library* choice justified by manufacturing semantics and in-repo precedent, not by industry standard.

## 5. Naming survey (what the concept is called across tools)

| Tool | Term for the body-defining 2D boundary |
|---|---|
| brickify | "2D object" / "shape" (child geometry, unnamed) |
| base-plate-outliner | "shape" (project *name* says outliner; docs say shape) |
| LEGO.scad | `type` (enum of body families) |
| MachineBlocks | none (rectangle from `size`) |
| OpenSCAD | `offset`, `projection`; no body-outline noun |
| CadQuery | "profile" (2D shape being extruded), "pending wires" |
| CGAL | "offset contour" / "offset polygon" |
| Clipper2 | "paths" / "contours" |
| **bikar today** (read from source) | tile: `outline square <side>` statement (`parser.ts:1850`); piece: `profile` contextual word (`parser.ts:1485`); evaluator error vocabulary `'outline' | 'profile'` (`evaluator.ts:1156`); kernel field `bodyOutline` (`kernel3d/brick.ts:120`) |

Load-bearing local facts for the naming decision:

1. **`outline` is already a bikar statement word** — the tile declaration accepts `outline square <side>` — and the kernel field is literally `bodyOutline`. Choosing `outline` reserves nothing new.
2. **Statement words are contextual, not globally reserved.** The parser dispatches brick statements from a `brickStatements` map of contextual identifiers (parser.ts ~1990), and comments state orb statement words "are contextual" (parser.ts:1229). The 328-file-sweep cost applies to genuinely new words; `outline` has already paid it.
3. **`footprint` already has a mode grammar**: `parseBrickFootprint` (parser.ts:2123) accepts `auto` | `N x M`. Adding a third mode value — `footprint outline` — is a one-armed extension of an existing parse function, keeps one-statement-per-line style, and mirrors LEGO.scad's mode-enum and OpenSCAD's `resize auto` shape. Caveat to resolve in the design doc: `footprint` today determines *both* the stud grid and the body rectangle; under `outline` mode the stud grid must still come from somewhere (presumably the auto rule), so the doc must say whether `footprint outline` means "body from pattern, grid auto" and whether `footprint outline 2 x 4`-style combination is rejected.
4. Cross-tool support for the alternatives is weak: "silhouette" appears in none of the fetched tools' vocabularies; "contour" only in CGAL/Clipper (library-level, not DSL-level); "profile" in bikar already means the *revolve* input (evaluator.ts:1633), so reusing it for the body would collide with an established in-language meaning — a K7-style self-contradiction waiting to happen.

## 6. Source list (every URL, what it actually says, fetched vs snippet)

1. https://github.com/richfelker/brickify — fetched. Arbitrary 2D child object → matching brick; "2D object" terminology; studs only where fully inside; no degeneracy discussion.
2. https://github.com/cfinke/LEGO.scad — fetched. `type` enum (`brick|tile|wing|slope|curve|baseplate|round|round-tile`) + per-type params; no arbitrary outline.
3. https://github.com/pks5/machineblocks — fetched. Repo layout only; parameters not on landing page.
4. https://raw.githubusercontent.com/pks5/machineblocks/master/lib/block.scad — fetched. `size`, `baseHeight: mm|'auto'`, `baseSideAdjustment`; base always rectangular; no outline/shape/contour/profile params.
5. https://github.com/dlvoy/base-plate-outliner — fetched. Raster → "shape" via `--threshold`; `--edge`, `--frame` modes; decomposes into rectangular baseplates.
6. https://github.com/mlkood/BRICK.scad — (unverified snippet) LEGO.scad-style generator; not fetched.
7. https://github.com/anandamous/OpenSCADLEGO — (unverified snippet) type/length/width/height params; not fetched.
8. https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations — fetched. `offset(r|delta, chamfer)`; "holes less than 2*r in diameter vanish"; `resize(..., auto=true)` "auto-scales any 0-dimensions to match."
9. https://www.angusj.com/clipper2/Docs/Units/Clipper.Offset/Classes/ClipperOffset/_Body.htm — fetched. Do not offset intersecting closed paths; pre-clean via Union; NonZero filling; winding preserved.
10. https://doc.cgal.org/latest/Straight_skeleton_2/index.html — fetched. Inward offsets may split into multiple polygons or vanish; weakly-simple-polygon precondition; non-simple input out of scope.
11. https://cadquery.readthedocs.io/en/latest/classreference.html — fetched. `offset2D(d, kind='arc'|'intersection'|'tangent')`; "profile"/"pending wires" terminology; degeneracy statement is fetch-model paraphrase (low confidence).
12. https://openjscad.xyz/docs/module-modeling_expansions.html — fetched. `expand`/`offset` with `delta` (negative contracts), `corners: 'edge'|'chamfer'|'round'`; no degeneracy warnings found.
13. https://doc.rust-lang.org/edition-guide/editions/index.html — fetched. Editions opt-in; incompatible changes gated behind explicit `Cargo.toml` declaration; cross-edition interop rule.
14. https://docs.python.org/3/reference/simple_stmts.html#future-statements — fetched. Explicit per-module opt-in to semantics-changing features; compile-time necessity rationale.
15. https://peps.python.org/pep-0020/ — fetched. "Explicit is better than implicit"; "refuse the temptation to guess"; "Errors should never pass silently."
16. https://rubyonrails.org/doctrine — fetched. Convention-over-configuration case for smart defaults; concession that unique elements exist and "the hard part is knowing when to stray."
17. https://mikehadlow.blogspot.com/2012/05/configuration-complexity-clock.html — fetched. Config/flag escalation ends in an ad-hoc DSL; sometimes hard-coding is the least evil; quotes as returned by fetch.
18. https://zoo.dev/docs/kcl-lang/foundations — **404, not fetched**; no KCL claims made.
19. Local: `bikar` source at `~/Workspace/git/bikar` — `packages/core/src/dsl/parser.ts` (brickStatements map ~L1990; `parseBrickFootprint` L2123; tile `outline` L1850; piece `profile` L1485), `packages/core/src/kernel3d/brick.ts` (`bodyOutline` L120, `insetRing` L759 with drop-crossing-spans heuristic and Appendix B.7 caveat), `packages/core/src/kernel3d/solidify-lattice.ts:172` (throws on degenerate inset), `packages/core/src/kernel3d/solidify-piece.ts:427` (self-intersection error). Read directly, not via fetch.

## 7. Verdict table

| Claim | Supports | Refutes / complicates | Open |
|---|---|---|---|
| An explicit trigger (not a geometry-sniffing auto rule) is the right call when existing programs' bodies would change | Rust editions (opt-in incompatible changes); Python `__future__` (explicit per-module semantics opt-in); PEP 20 ("refuse the temptation to guess"); no fetched CAD tool silently switches body derivation | Rails CoC argues defaults over declarations — but for *stable* conventions, not changed ones; brickify is "implicit" only because shape-as-input is its sole behavior | K10: editions/`__future__` are version-migration mechanisms; the transfer rests on the shared hazard (changed meaning of existing programs), argued in §3 |
| A named mode value on an existing statement (à la `footprint outline`) beats a new statement or new reserved word | OpenSCAD `resize auto`; MachineBlocks `baseHeight 'auto'`; LEGO.scad `type` enum; bikar's own `footprint auto` grammar already forks on a mode word; Hadlow warns against knob proliferation (favors extending one statement) | brickify shows shape-as-first-class-input as an alternative surface; `outline` as a *value* of footprint slightly overloads a statement whose other modes set the stud grid | What sets the stud grid under `footprint outline`; whether `outline` may combine with explicit `N x M`; whether `body outline` (new contextual word `body`) reads better despite costing a sweep |
| "Inset degenerates → hard error" is standard practice in geometry tools | bikar's own `solidify-lattice` throws; `solidify-piece` errors on self-intersection; PEP 20 "errors should never pass silently"; Clipper documents self-intersecting offsets as invalid *input* | **Not standard in libraries**: Clipper repairs via union/winding; CGAL defines split-or-vanish as a valid result; OpenSCAD silently vanishes thin features; none of the three fetched libraries hard-errors | Whether kernel `insetRing`'s drop-crossing-spans heuristic (self-flagged unverified vs. star tips, Appendix B.7) must be replaced or gated before star-shaped bodies ship — the DSL-level error decision is separate from fixing the kernel heuristic |
| "Outline" is the best-attested name for the concept | bikar tile `outline` statement + kernel `bodyOutline` field already exist (zero new reserved words); CGAL "offset contour" adjacent; base-plate-outliner's *name* | Fetched brick tools mostly say "shape" or use a `type` enum; "profile" is well-attested in CAD (CadQuery) but already means revolve-input in bikar — reusing it would collide | None material; "silhouette" found in no fetched tool's vocabulary (checked the 9 tools/libraries in §5's table only) |
| No surveyed generator both keeps a rectangular default and offers arbitrary-outline bodies in one declaration | Holds across the 4 generators fetched (brickify, LEGO.scad, MachineBlocks, base-plate-outliner) | — | Only 4 generators were actually read; BRICK.scad, OpenSCADLEGO, Printables customizers, brick.js, LDraw tools were not fetched — the claim is scoped to the fetched set |
