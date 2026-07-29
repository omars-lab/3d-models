# Ports, Connect & Assembly (C2) — implementation design doc

Status: **v2 — grounded in a targeted implementation survey
([`research/c2-assembly-implementation-survey.md`](research/c2-assembly-implementation-survey.md),
sources in Appendix A) and revised after an adversarial grounding audit
([`research/c2-assembly-grounding-audit.md`](research/c2-assembly-grounding-audit.md);
counter-evidence and divergences recorded in Appendix B).**
Scope: the C2 rung of the composition ladder promised in
[`piece-composition-design.md`](piece-composition-design.md) §9 — explicit `port`
declarations, `connect` with contract validation, `assembly` with deterministic placement
and closure checks, per-part export, the fit coupon, and the printer-profile table. This
doc turns that doc's §4.3–§4.4 sketch into an implementable specification against the
current bikar tree, and resolves two of its open questions (Q2 spin semantics, Q3
assembly-level parameters).

Builds on: [`piece-composition-design.md`](piece-composition-design.md) (the parent design;
its fit-intent model and cycle rule are adopted verbatim, its grammar sketch is refined
here). Sibling consumer: [`tile-wall-design.md`](tile-wall-design.md) — W2's connector
library rides this machinery (profiles, fit windows, per-part export) and adds its own
layout-derived placement layer.

---

## 1. Goals

1. **Explicit ports.** C1 auto-mints ports from countersunk holes; C2 lets any piece or
   tile declare a named port — a frame (origin, z-direction, spin reference) plus a
   contract (`kind` + dimensions + fit intent) — so solids without holes (pins, collars)
   can participate in assemblies.
2. **`connect` that validates.** Anti-align the two port frames, compose the placement
   deterministically, and check the contract: kind compatibility, pin ⌀ + intent gap vs
   socket ⌀, ring/rim ⌀ and depth. A connect that would produce a part that cannot mate
   as declared is a compile error, not a surprise at the printer.
3. **`assembly` as a tree with closure checks.** First `place` is the root; each connect
   in source order grows the tree from a placed piece to an unplaced one; a connect
   between two already-placed pieces derives no transform and instead asserts the frames
   already coincide within tolerance (the parent doc's cycle rule, §4.4).
4. **Per-part export.** `export parts` + `--format parts` emits one print-oriented STL
   per piece, named `<Assembly>-<Piece>.stl`; the assembled preview stays available as a
   single mesh.
5. **The honest-fit machinery.** A printer-profile table applied to *geometry* at compile
   time, a step-gauge fit coupon whose measured results set the profile, and a physical
   deliverable — two tiles + printed pins that actually fit — that exercises all of it.

Non-goals for C2: 3MF export (deferred — §7), multiple instances of one piece
(`place … as …` aliases are C3), orb `open cap` ports (C3 per the parent doc §4.5),
motion joints of any kind.

## 2. Engine ground truth

Facts verified against the bikar tree that the design leans on:

- **C1 hole ports exist and are frameless.** `mintHolePorts` in
  `packages/core/src/dsl/evaluator.ts` derives `Owner.holeName` ports from hole stacks
  (x, y, z-band, `minD`). C2 gives every port a frame; hole ports get the deterministic
  default (origin at `(x, y, zTo)`, direction `+z`, spin 0 — pin enters from the top
  face). Authors needing bottom entry declare an explicit port.
- **`revolve` rejects axis-touching profiles** (the solidifier comment defers "the PinPeg
  example" to C2 explicitly). Rather than generalize revolve pole handling, C2 adds a
  `rod` constructor — a solid cylinder is the only pin geometry the deliverable needs,
  and it is ~40 lines of direct mesh construction (§4.2).
- **`meshGate` reports Euler characteristic without gating on it** (verified in
  `kernel3d/mesh-gate.ts`). An assembled preview mesh made of k disjoint closed
  components has Euler 2k and passes; watertightness is checked per edge-pairing, which
  each component satisfies internally.
- **Params are parse-time, file-scoped token substitutions** (`$name` → number), and the
  DSL has no cross-file import. An assembly can only place pieces declared in the same
  file — which is what makes Q3's answer cheap (§9).
- **Pattern corpus is clean for the new keyword.** `grep -rn '\bassembly\b' patterns/`
  hits comment text only; the pre-commit compile gate on staged `.bkr` is the backstop.
- **CLI multi-file precedent exists**: `--format views` requires `-o <dir>` and writes
  one file per view. `--format parts` copies that shape exactly.

## 3. What the survey established (the load-bearing facts)

From [`research/c2-assembly-implementation-survey.md`](research/c2-assembly-implementation-survey.md);
numbers restated here so the doc stands alone.

- **Slicers re-arrange independently imported objects by default.** PrusaSlicer, Bambu
  Studio, and Cura all drop such objects to the bed and/or re-arrange them; each does
  have an interactive preserve-positions workflow (PrusaSlicer's multipart-object
  import dialog, Bambu's Assembly View, Cura's merge-models), but those require a
  shared world frame, manual interaction the CLI cannot script, and give up per-part
  print orientation. Only 3MF *components-objects* carry spec-locked relative
  positions ("a 3D manufacturing device MUST respect the relative positions of the
  component objects"). Consequence: per-part STL should be exported **print-oriented
  at its own origin**, and "assembled" intent belongs to a future 3MF writer, not to
  STL coordinates (survey §1; qualified per the audit — Appendix B.4).
- **STL carries no part name — the filename is the identity.** Hence
  `<Assembly>-<Piece>.stl` (survey §1).
- **BOSL2 `attach()` is the right mating model**: anti-aligned anchors at connect time
  plus a connect-time `spin` about the shared mate axis. BOSL2 documents its
  library-wide spin convention as "counter-clockwise around the Z axis" and
  `attach()`'s `spin=` as rotating "around the axis of the parent anchor" — but never
  composes the two for the anti-aligned attach case, so whether positive spin is CCW
  about the parent's or the (opposite) child's mate axis is left to experiment, and
  its own reference concedes the child-spin interaction "may be hard to predict."
  build123d's `RigidJoint.connect_to` is the opposite convention — exactly coincident
  frames, no flip, no spin — forcing authors to hand-compose 180° flips into joint
  declarations (survey §2). C2 adopts BOSL2's model and states outright the composed
  sign BOSL2 never does, plus the residual-orientation default and the closed-form
  composition, each pinned by a unit test (§4.4; Appendix B.7).
- **No surveyed system validates a *declared* connector contract at connect/compile
  time.** The claim needs its narrow form: mainstream MCAD does validate dimensional
  clearance at assembly level — SolidWorks' Clearance Verification "checks the minimum
  distance between the components and reports clearances that fail to meet the minimum
  acceptable clearance you specify," and Onshape ships on-demand Interference
  Detection — but both are geometric analyses a user runs after assembly, computed
  from the shapes, knowing nothing about intent (a press fit *should* interfere;
  Clearance Verification can only call that a violation). Among code-CAD systems,
  build123d raises `TypeError` on joint *kind* only; NopSCADlib's fastener library
  (clearance-hole modules, BOM, exploded views) ships no fit validation; KCL's
  assertion checks are user-authored, not connect-time. FreeCAD Assembly4 is
  deliberately solver-free and cannot flag inconsistency at all, while FreeCAD 1.0's
  integrated solver can go "unstable and blow up assembled parts" when its assembly
  state is perturbed, and miscounts degrees of freedom on valid input. Comparing
  *declared* connector dimensions plus *declared* fit intent at connect time and
  failing the build remains novel within everything surveyed (survey §3; narrowed per
  the audit — Appendix B.1, B.2).
- **The coupon methodology is settled prior art.** BOSL2's `$slop` test part — the
  embossed label of the tightest fitting hole *is* the profile value — plus Bambu's
  one-variable-per-coupon discipline: separate hole and contour coupons, same
  filament/profile as production, per-side compensation = measured diametral
  undersize ÷ 2 (survey §4).
- **PrusaSlicer has no hole compensation** (single global XY compensation only; the
  hole/contour split is a years-open request chain — #1065 since 2018, #14953 opened
  Oct 2025 — current as of PrusaSlicer 2.9.x, July 2026, with 3.0 imminent; re-verify
  at implementation time). The compiler must therefore apply hole compensation to port
  geometry itself — and even if a future PrusaSlicer ships the split, compiler-side
  application remains the only mechanism that works identically across all three
  slicers and keeps the declared/compensated split visible to the contract checker
  (survey §4; Appendix B.6).
- **Pin engineering numbers.** Sources disagree on minimum ⌀ (Hydra Research ⌀1.8 mm
  engineering floor vs Hubs' "under ⌀5 mm is perimeter-only and weak"); C2 treats ⌀3 mm
  as the floor. Layer orientation costs roughly half the strength: PLA printed
  vertically failed at 55% of horizontal load, PETG at 46%, in CNC Kitchen's hook
  tests — one lab's bending-mode results; measured Z-retention across studies spans
  roughly 25–67%, so these numbers motivate the coupon rather than serve as constants
  (Appendix B.5). No citable lead-in chamfer norm for pin tips exists — it becomes a
  knob with a couponed default (survey §5, §6).
- **Assembly-level parameter precedent is "small named set or nothing."** OpenSCAD's
  dynamically-scoped `$slop` (collision hazard across libraries) and OnShape's
  enumerated configuration inputs (permutation explosion) both support assembly-level
  override of piece defaults and both deliberately keep the forwarded set small and
  named; no surveyed system forwards arbitrary piece params (survey §6, feeds §9).

## 4. Language design

Exactly **one** new keyword: `assembly`. Everything else (`port`, `place`, `export`,
`parts`, `kind`, `fit`, `rod`, `spin`, `dir`, the kind and fit words) is contextual, so no
existing pattern can break. Parser traps and their handling are recorded in the
implementation plan; the two worth naming here: `ring`/`depth`/`at`/`to` lex as keyword
tokens inside the new contextual grammar (the contract parser accepts token-type *or*
identifier), and `dir -z` lexes as a minus token followed by identifier `z`.

### 4.1 `port` — declared frames on pieces and tiles

```bkr
piece BulbCollar
  revolve collar_profile
  port mount at centroid dir +z spin 0
    kind ring d 46 depth 5

tile TileA
  face sq_face
  art tile_art
  depth 6
  port hang at -30, 40 z 6
    kind pin_socket d 3.15
```

Grammar: `port <name> at centroid | at <x> [,] <y> [z <mm>] [dir +z|-z] [spin <deg>]`,
followed by exactly one `kind` continuation line (the same statement + continuation shape
as `hole` + `band`):

| kind | continuation | mates with |
|---|---|---|
| `pin` | `kind pin d <⌀> fit press\|snug\|sliding\|free` | `pin_socket`, hole ports |
| `pin_socket` | `kind pin_socket d <⌀>` | `pin` |
| `ring` | `kind ring d <⌀> depth <mm>` | `rim` |
| `rim` | `kind rim d <⌀> depth <mm>` | `ring` |
| `axis` | `kind axis` | `axis` |

Defaults: `dir +z`; `z` defaults to the piece's top surface for `+z` ports and `0` for
`-z` ports (resolved at evaluation when depth is known); `spin 0`. `fit` is **required on
`pin` and forbidden on every other kind** — the pin side is the single source of truth
for the clearance class, so there is no both-sides-disagree case to legislate.
Validation at mint time: z within `[0, depth]`, point-ports inside the outline for
extruded pieces, no collision with an auto-minted hole port's name. Rod and tube pieces
accept only `at centroid` ports (the axis is the only meaningful frame).

A port's frame is fully determined: origin from `at`/`z`, z-axis from `dir`, x-axis =
`+X` rotated by the port's own `spin` about its z-axis, y = z × x (right-handed).

### 4.2 `rod` — the pin constructor

```bkr
piece DowelPin
  rod d 3.0 height 12
  port seat at centroid dir -z
    kind pin d 3.0 fit press
  port cap at centroid dir +z
    kind pin d 3.0 fit sliding
```

`rod d <⌀> height <mm>`: a solid cylinder, meshed directly (n-gon wall + fan caps, same
segment count as hole drilling), `minFeatureMm = min(d, height)`. This sidesteps the
revolve-pole generalization the C1 solidifier explicitly deferred; revolve keeps its
r > 0 restriction, and the restriction's error message continues to point authors at
`rod`.

### 4.3 `assembly` — place, connect, export

```bkr
assembly PinnedTiles
  place TileA
  place DowelPinA
  place DowelPinB
  place TileB
  connect DowelPinA.seat to TileA.h1        # places PinA (pressed into A)
  connect TileB.h1 to DowelPinA.cap         # places TileB (flipped, slides onto PinA)
  connect DowelPinB.seat to TileA.h2        # places PinB
  connect DowelPinB.cap to TileB.h2         # both placed → closure check
  export parts
```

Semantics (parent doc §4.4, made exact):

- **Root**: the first `place` sits at identity. Pieces are authored in their own frames;
  placement is derived, never authored.
- **Tree growth**: connects are processed in source order. A connect with exactly one
  placed endpoint mates the unplaced piece onto the placed one. A connect between two
  unplaced pieces is an *ordering error* with a message that names the root — no
  union-find, no deferred resolution, fully deterministic.
- **Closure**: a connect between two placed pieces derives no transform; the two port
  frames must already coincide — anti-aligned, spin-registered, origins within
  1e-6 mm and axes within 1e-6 rad — else compile error reporting the offset in mm
  and the twist in degrees (checked in radians, reported in degrees).
  Contract validation runs on closures too. The tolerance can be that tight because
  authored dimensions composed through quadrant-snapped rotation leave only float dust
  (~1e-13); anything larger is a real modeling error (wrong hole spacing), and the
  message says so.
- **One connection per port** — closures also consume their ports.
- **Reachability**: after the loop, any placed piece not reached by a connect is an
  error (single-piece assemblies are the trivial exception).
- **One instance per piece.** `place X` twice is a parse error whose message names the
  C3 `place … as …` alias plan. The Pinned-Tiles deliverable therefore declares two
  five-line pin pieces — accepted C2 cost, recorded as the C3 motivation.

### 4.4 Mating math — spin semantics (resolves parent doc Q2)

Adopted model: **BOSL2-style anti-alignment with a connect-time `spin`**, with the
things BOSL2 documents separately but never composes (§3) made explicit:

- **The mated frame.** Given the placed-side port's world frame `g`, the mated frame `M`
  has the same origin, `M.z = −g.z`, and `M.x = rotate(g.x, g.z, spin)`. The unplaced
  piece's transform is the rigid motion carrying its local port frame onto `M`.
- **Residual-orientation default**: at `spin 0`, the child port's x-axis coincides with
  the parent port's x-axis. (BOSL2's analog is its FRONT-points-front rule set; ours is
  one sentence because ports carry explicit x-axes.)
- **Sign convention**: positive `spin` rotates the incoming child counterclockwise as
  seen looking along the parent port's +z axis — the right-hand rule about the *parent's*
  port axis. Worked example, pinned by a unit test: parent port frame x = +X, z = +Z;
  `spin 90` lands the child port's x-axis on world +Y.
- **Closed form** (for the implementation and for anyone porting):
  `child_world = parent_world · F_p · Rx(180°) · Rz(−spin) · F_q⁻¹`, where `F_p`/`F_q`
  are the port frames as local transforms. The `Rz` sign flip relative to the convention
  above is because the mated z points opposite the parent z; the unit test pins it so
  the doc and the code cannot drift.

Rotation representation: orthonormal frames + 3×3 rotation as three vector rows (no mat4,
no quaternions) with quadrant-snapped trig — `spin 90` grids compose bit-identically and
right-angle closures have exactly zero residual. Determinism is a house tenet; this is
where it is enforced for assemblies.

## 5. Contracts, fit windows, and printer profiles

The parent doc's intent/compensation split (§5 there), operationalized:

- **Intent gaps** (diametral): press −0.10 / snug +0.05 / sliding +0.15 / free +0.35 mm
  — a calibrated-printer ladder; credible sources recommend 2–10× looser, and the
  divergence justification is recorded in Appendix B.3.
- **Fit window**: a pin↔socket connect requires
  `|(socket⌀ − pin⌀) − intentGap(fit)| ≤ 0.05 mm`. The window is symmetric — a one-sided
  "pin + clearance ≤ socket" check would silently accept a sloppy socket, and press fit
  (negative gap) needs the other side bounded too. 0.05 mm is half the *smallest*
  ladder step (snug→sliding, 0.10 mm), so adjacent windows touch at single boundary
  points but never properly overlap — a gap of exactly 0.10 mm satisfies either the
  snug or the sliding declaration, which is harmless because the check validates the
  author's declared intent; it never classifies. Hole ports mate as sockets using
  their `minD`.
- **`ring ↔ rim`**: ⌀s within the same 0.05 mm window and rim depth ≤ ring depth. Parsed
  and validated in C2; the geometry consumer is C3's collar. `axis ↔ axis` is
  dimension-free. Any other kind pairing is an error naming both kinds.
- **Printer profiles compensate geometry, never intent.** A profile is
  `{material, holeCompMm}`; at solidify time every drilled circle's ⌀ grows by
  `holeCompMm`. Contract validation always runs on the *declared* numbers, and
  provenance reports declared numbers — the mesh is the only thing that changes.
  Shipped table: `none` (0 — the default, keeping every existing pattern byte-identical),
  `pla_calibrated` (0.20 mm), `petg_calibrated` (0.25 mm — the parent doc's "PETG tack
  eats another ~0.05 mm"). Selected per render via `--fit-profile <name>`; the table's
  numbers are placeholders until the fit coupon measures them (the coupon is what makes
  the table honest — parent doc Appendix B.2). Because PrusaSlicer cannot compensate
  holes at all (§3), this compiler-side application is the only path that works across
  all three surveyed slicers.

## 6. Pins — engineering floors and the orientation question

- **⌀3 mm floor** for printed pins (between Hydra's ⌀1.8 engineering rule and Hubs'
  under-⌀5 warning); at ~0.4 mm line width that is still only a few perimeters, so fit
  *and* strength are both coupon questions, not spec questions.
- **Print orientation.** `export parts` emits authored orientation as print orientation,
  and `rod` pins are authored upright — but upright printing puts every layer boundary
  in shear (PLA 55% / PETG 46% of flat strength, §3). Resolution: the deliverable's pins
  are short (12 mm) and lightly loaded, so authored-upright is acceptable *for the
  deliverable*; whether upright pins shear in practice is a `/prototype` catalog
  question logged with the fit coupon, and re-plating a pin to lie flat is a slicer
  operation the export docs mention. C2 does not add per-part orientation overrides —
  that is a C3+ decision informed by the coupon.
- **Base fillet and lead-in chamfer** stay knobs on `rod` deferred to the first physical
  iteration: the fillet norm is documented only for plate edges, and no citable lead-in
  size norm exists (§3) — defaults get set by the coupon, not by folklore.

## 7. Export and CLI

- **`--format parts`** (requires `export parts` in the assembly and `-o <dir>`, exactly
  like `--format views`): one binary STL per placed piece, **piece-local coordinates**
  (authored = print orientation, z = 0 on the bed), named `<Assembly>-<Piece>.stl`,
  emitted in `place` order. `--check` runs the mesh gate per part and fails listing
  every failing part.
- **`--format stl`** on an assembly renders the assembled preview: world-transformed
  part meshes concatenated by **index offsetting, never vertex welding** — welding at
  mesh tolerance would fuse coincident pin/socket faces into non-manifold geometry.
  Each component stays watertight; Euler 2k for k parts is fine because the gate
  reports Euler without gating (§2). Press-fit interference in the preview is
  intentional and documented.
- **`--fit-profile <name>`** selects the printer profile (default `none`).
- **3MF is deferred**, with the survey's findings banked for whoever writes it: encode
  the assembly as a single components-object (spec-locked relative positions), 12-value
  row-major transforms, `partnumber` for toolchain identity, `<metadatagroup>` for
  port/connect provenance, and validate against the negative-determinant rule. Per-part
  STL satisfies the C2 deliverable without a new dependency.

## 8. Deliverables and coupons

- **`patterns/Assemblies/Pinned-Tiles.bkr`** — the C2 physical deliverable: two girih
  tiles + two printed dowel pins (§4.3 listing). Socket bands are authored inside the
  fit windows (⌀2.90 press-side, ⌀3.15 sliding-side against ⌀3.00 pins); the fourth
  connect *is* the closure check, so the flagship file demonstrates the cycle rule.
  Assemblies get their own `patterns/Assemblies/` directory — the 3d-models Makefile
  globs only `patterns/Orbs/`, so the gallery pipeline is untouched.
- **`patterns/Coupons/Fit-Coupon.bkr`** — the step gauge: one plate with through-holes
  ⌀2.90 / 3.00 / 3.10 / 3.20 / 3.30 plus a ⌀3.00 rod pin, printed at
  `--fit-profile none`. Procedure (in the file header, BOSL2-`$slop`-style): probe which
  hole yields press/snug/sliding; `holeCompMm = (⌀ that achieved the fit) − (designed ⌀
  for that fit)`. One variable per coupon, production filament and profile, per the
  Bambu discipline (§3). Results land in the `/prototype` catalog and update
  `PRINTER_PROFILES` — printing itself is currently on hold, so the coupon ships as a
  `planned` catalog entry.

## 9. Assembly-level parameters — resolved (parent doc Q3)

**C2 adds no assembly-level parameter namespace.** Reconciling the plan and the survey:

- File-level `param` already *is* the forwarding mechanism: params are file-scoped
  parse-time substitutions and assemblies can only place same-file pieces (§2), so one
  `$pin_d` declaration already flows into the pin's `rod d`, both tiles' hole bands, and
  the port contracts coherently, with `--param pin_d=3.2` overriding all of them at
  once. A second namespace would create two knobs that can disagree — the exact failure
  the contract check exists to prevent.
- The survey's precedent (§3) says assembly-wide knobs should be a *small named set*,
  never free-form forwarding. C2's named set has exactly one member: the printer/fit
  profile (`--fit-profile`), which is assembly-wide by construction and orthogonal to
  geometry params — the `$slop`-accessor pattern with the collision hazard removed by
  not being an ambient variable at all.
- Trigger for revisiting: a cross-file piece import or instancing mechanism (C3's
  `place … as …` at the earliest). Recorded in the bikar decision ledger with this doc.

## 10. Validator summary (all compile-time, all hard errors)

| # | Check | Error reports |
|---|---|---|
| 1 | Port kind vocabulary, fit required-on-pin/forbidden-elsewhere | offending word, allowed set |
| 2 | Port frame in-solid (z range, point in outline, centroid-only for rod/tube) | port name, limits |
| 3 | Port name collisions (declared vs declared, declared vs hole-minted) | both names |
| 4 | Connect endpoint resolution | unknown piece/port, available ports listed |
| 5 | Kind compatibility matrix | both kinds, what mates what |
| 6 | Fit window `\|gap − intent\| ≤ 0.05` | pin ⌀, fit class, required socket ⌀ ± window, actual |
| 7 | Ring/rim ⌀ window + depth containment | both ⌀s / both depths |
| 8 | One connection per port | port name, the earlier connect |
| 9 | Two-unplaced-pieces ordering | both pieces, the root |
| 10 | Closure coincidence ≤ 1e-6 mm / 1e-6 rad | offset mm, twist deg, likely cause |
| 11 | Unreachable placed piece | piece, root |
| 12 | Unknown `--fit-profile` | name, known profiles |

## 11. Phasing

Ten commit-sized steps, each leaving tests + per-workspace typecheck + lint green:
(1) frame math kernel + tests; (2) fit table + profiles; (3) `rod` end-to-end;
(4) port grammar on piece + tile; (5) evaluator port minting + frames + profile
plumbing (core minor version bump — `PiecePort` becomes a discriminated union that
keeps every C1 field); (6) `assembly` grammar; (7) assembly evaluation (tree solve,
contracts, closures, mesh concat); (8) CLI (`--format parts`, `--fit-profile`);
(9) deliverable + coupon patterns, rendered and visually verified; (10) docs (language
reference section, decision-ledger entry, roadmap tick). The detailed file-level plan
(AST shapes, parser wire-in points, exact error strings, test matrix) lives with the
implementation, not in this doc.

## 12. Open questions

- **Q1 — upright pin shear.** Do 12 mm ⌀3 authored-upright pins shear in tile service?
  Coupon question (`/prototype` catalog, blocked on printing resume); answer decides
  whether C3 needs per-part orientation overrides.
- **Q2 — lead-in geometry defaults.** Chamfer/fillet sizes for pin tips and bases have
  no citable norm (§3); first physical iteration sets them.
- **Q3 — profile table values.** 0.20/0.25 mm are literature-shaped placeholders until
  the fit coupon measures this printer; the table is honest only downstream of the
  coupon.
- **Q4 — embossed labels on the coupon.** The BOSL2 pattern embosses values into the
  part; C2's coupon documents ⌀s in comments only (text embossing is out of scope).
  Worth revisiting if the coupon confuses in practice.

## Appendix A — survey sources

Primary source file, checked in verbatim with all URLs:
[`research/c2-assembly-implementation-survey.md`](research/c2-assembly-implementation-survey.md)
(research date 2026-07-28; §1 multi-part export + slicer behavior, §2 BOSL2/build123d
mating math, §3 contract-validation precedents, §4 coupon methodology, §5 pin
engineering, §6 assembly parameters). The adversarial audit behind Appendix B is
likewise checked in verbatim:
[`research/c2-assembly-grounding-audit.md`](research/c2-assembly-grounding-audit.md)
(audit date 2026-07-28). Neither re-covers
[`research/code-cad-composition-survey.md`](research/code-cad-composition-survey.md)
(the parent doc's survey: BOSL2/build123d overviews, OnShape/Fusion mate vocabularies,
Gridfinity, the Creative3DP fit ladder).

Load-bearing numbers restated against link rot: 3MF transforms are 12 space-delimited
row-major decimals; components-objects lock relative positions by spec ("MUST respect
the relative positions"); PLA vertical-print strength 55% of horizontal, PETG 46%
(CNC Kitchen hook tests); Hydra pin floor ⌀1.8 mm, Hubs weak-pin warning < ⌀5 mm;
Bambu per-side hole compensation = diametral undersize ÷ 2; PrusaSlicer ships no hole
compensation (global XY only); BOSL2 `$slop` default 0.0 with `get_slop()` accessor;
intent-gap ladder −0.10/+0.05/+0.15/+0.35 mm inherited from the parent doc §5 with its
honesty caveats.

Key direct sources (full list in the survey): the
[3MF core spec](https://github.com/3MFConsortium/spec_core/blob/master/3MF%20Core%20Specification.md),
[BOSL2 attach tutorial](https://github.com/BelfrySCAD/BOSL2/wiki/Tutorial-Attachment-Attach)
and [attachments.scad reference](https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad),
[build123d joints.py](https://github.com/gumyr/build123d/blob/dev/src/build123d/joints.py)
and [joints docs](https://build123d.readthedocs.io/en/latest/joints.html),
[BOSL2 constants.scad ($slop)](https://github.com/BelfrySCAD/BOSL2/wiki/constants.scad),
[Bambu XY hole/contour compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation),
[Bambu Assembly View guide](https://wiki.bambulab.com/en/software/bambu-studio/assembly-view-guide),
[PrusaSlicer hole-compensation request #1065](https://github.com/prusa3d/PrusaSlicer/issues/1065),
[Hubs FDM design guide](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/),
[Hydra Research design rules](https://www.hydraresearch3d.com/design-rules),
[CNC Kitchen PLA/PETG/ASA orientation tests](https://www.cnckitchen.com/blog/comparing-pla-petg-amp-asa-feat-prusament),
[OpenSCAD special variables](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features),
[OnShape configurations help](https://cad.onshape.com/help/Content/PartStudio/part_studio_and_assembly_configurations.htm),
[FreeCAD solver-instability issue #20377](https://github.com/FreeCAD/FreeCAD/issues/20377),
[SolidWorks Clearance Verification](https://help.solidworks.com/2022/english/SolidWorks/sldworks/c_Clearance_Verification_SWassy.htm),
[Onshape Interference Detection](https://cad.onshape.com/help/Content/View/interference_detection.htm),
[NopSCADlib](https://github.com/nophead/NopSCADlib),
[KCL assertion checks](https://zoo.dev/docs/kcl-book/checking.html),
[SolveSpace reference](https://solvespace.com/ref.pl),
[Creative3DP press-fit ladder](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/),
[AON3D engineering fits for FDM](https://www.aon3d.com/applications/engineering-fits-how-to-design-for-3d-printed-assemblies/),
[MDPI Processes 2023 — ISO 286 fits on calibrated FDM](https://www.mdpi.com/2227-9717/11/10/2810).

## Appendix B — counter-evidence and divergences

From the adversarial grounding audit
([`research/c2-assembly-grounding-audit.md`](research/c2-assembly-grounding-audit.md),
audit date 2026-07-28). Each entry records the strongest counter-position found, with
its link and a fair summary, then either our justification for diverging or the change
the audit forced. Where a claim was narrowed, §3 above already carries the corrected
wording — these entries are the record of why.

Entries tagged `[CAL-…]` are **empirical** bets that no source can close — only a
measurement can. The id is the bet's entry in the registry
([`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md)), which
names the coupon that settles it; the ceremony is the `calibrate` skill (bikar
Tenet 30 — a physical constant is not earned until it records its provenance).

### B.1 "Novel contract validation" — the counter-evidence partially won; the claim was narrowed

The audit's hardest attack landed: mainstream MCAD **does** validate dimensional
clearance at assembly level. SolidWorks'
[Clearance Verification](https://help.solidworks.com/2022/english/SolidWorks/sldworks/c_Clearance_Verification_SWassy.htm)
"checks the minimum distance between the components and reports clearances that fail
to meet the minimum acceptable clearance you specify" — a genuine dimensional check
against a user-declared value. Onshape ships on-demand
[Interference Detection](https://cad.onshape.com/help/Content/View/interference_detection.htm)
(and the doc's earlier "OnShape's error is solver degrees-of-freedom" under-represented
it). The original claim — "no surveyed system validates connector dimensions at
assembly time" — was therefore **false as stated** and has been narrowed in §3: these
are geometric analyses run on demand after assembly, computed from shapes with no
notion of intent (a press fit *should* interfere, and Clearance Verification can only
report that as a violation; Onshape's clearance-threshold variant remains an unshipped
[forum request](https://forum.onshape.com/discussion/15048/add-an-offset-to-check-interference-for-quickly-checking-clearance-tolerances)).
What stays novel within everything surveyed is the composition: *declared* connector
dimensions plus *declared* fit intent, checked at connect/compile time, failing the
build. Two additional surveyed-and-negative systems strengthen the narrowed form:
[NopSCADlib](https://github.com/nophead/NopSCADlib) (fastener library with
clearance-hole modules, BOM generation, exploded views — no fit validation) and
[KCL's assertion checks](https://zoo.dev/docs/kcl-book/checking.html) (user-authored
geometry assertions, not connect-time contract checks).

### B.2 Deterministic tree vs solver — the solver steelman, and why we still decline

The steelman: mature solvers fail gracefully, not explosively. SolveSpace detects
redundant/inconsistent constraint sets, flags them visually, and "determines which
constraints could be removed to fix the problem"
([SolveSpace reference](https://solvespace.com/ref.pl)); Onshape's over-defined-mate
error is a clean refusal. The audit also found the doc's original FreeCAD evidence
mis-contextualized:
[#20377](https://github.com/FreeCAD/FreeCAD/issues/20377) ("Solver goes unstable and
blows up assembled parts") was triggered by a document corrupted by cross-workbench
Assembly3/Assembly4 experiments — not by dimensionally inconsistent joints — and was
closed not-planned; the better-fitting citation for solver misbehavior on valid input
is the DOF-miscount issue
([#27557](https://github.com/freecad/freecad/issues/27557)). §3 now states this
correctly. We keep the deterministic tree regardless: bikar's assemblies are trees
with at most closure checks, so there is nothing to solve — adopting a solver would
buy only its failure modes (initial-position sensitivity, redundancy instability;
SolveSpace's own docs note its allow-redundant mode "makes the solver less stable")
for a use case where closed-form composition already answers every placement exactly.

### B.3 The fit ladder — credible sources recommend 2–10× looser [CAL-FIT-01 — the same bet as piece-composition B.2; coupon MC-1]

The ladder transcribes Creative3DP's calibrated-printer press-fit ladder verbatim,
including its instruction to keep fit gap and printer compensation separate
([Creative3DP](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/)).
Credible sources recommend far looser numbers:
[AON3D](https://www.aon3d.com/applications/engineering-fits-how-to-design-for-3d-printed-assemblies/)
calls ISO 286 "mostly irrelevant" to FDM and recommends clearances of 1–2× extrusion
width (~0.75–1.5 mm);
[Hydra Research](https://www.hydraresearch3d.com/design-rules) quotes 0.1/0.2 mm per
side; mainstream per-side ladders (0.1 press / 0.2–0.3 sliding / 0.4–0.5 loose) run
2–4× ours diametrally. Every looser source folds uncompensated printing into one
number — the thing our profile split explicitly refuses to do — and peer-reviewed work
shows calibrated FDM can hit genuine ISO-grade fits
([MDPI Processes 2023](https://www.mdpi.com/2227-9717/11/10/2810), which measured
0.13 mm hole expansion and then compensated it away). We keep the tight ladder because
compensation is applied separately by construction, and the fit coupon — not the
literature — is the arbiter of both tables.

### B.4 Slicer position-loss — overstated as absolute, true as a default

The audit found preserve-positions workflows in all three slicers: PrusaSlicer's
"load as a single object with multiple parts"
[import dialog](https://help.prusa3d.com/article/importing-multi-material-model_121191),
Bambu Studio's Assembly View, Cura's merge-models. §3 now says "by default" rather
than absolutely. The export design is unchanged because every preserving workflow is
interactive (the CLI cannot answer the dialog), requires all parts exported in one
shared world frame, and defeats per-part print orientation — the three properties
`--format parts` exists to provide.

### B.5 CNC Kitchen strength ratios — one lab's bending numbers, wide spread across studies [CAL-STR-01 — OPEN, no coupon: needs a load rig, not a print]

The 55%/46% figures are verified verbatim in
[CNC Kitchen's hook tests](https://www.cnckitchen.com/blog/comparing-pla-petg-amp-asa-feat-prusament) —
but they are hook-load (bending) results from one configuration, while §6 reasons
about pin shear, and other measured sources span solid-PLA Z-retention of ~67%
([Snapmaker's summary](https://www.snapmaker.com/blog/how-strong-are-3d-printed-parts/))
down to ~20–25%
([RapidMade](https://rapidmade.com/isotropic-vs-anisotropic-strength-in-3d-printing/)).
§3 and §6 now label them as coupon motivation, not constants; the upright-pin question
stays a `/prototype` catalog question (Q1).

### B.6 PrusaSlicer hole compensation — a load-bearing claim with an expiry date [CAL-HOL-01 — the `holeCompMm` magnitude; coupon MC-1]

Verified current: the request chain is open
([#1065](https://github.com/prusa3d/PrusaSlicer/issues/1065) since 2018,
[#14953](https://github.com/prusa3d/PrusaSlicer/issues/14953) since Oct 2025) as of
PrusaSlicer 2.9.x, July 2026 — but 3.0 is announced as imminent, so the claim could
flip within C2's implementation window. §3 date-stamps it and records the fallback
argument that survives the flip: compiler-side compensation is the only mechanism
identical across all three slicers, and the only one that keeps declared vs
compensated numbers visible to the contract checker.

### B.7 BOSL2 spin — more documented than the survey credited

The audit found the library-wide convention **is** documented
("counter-clockwise around the Z axis") and `attach()`'s `spin=` names its axis
("the axis of the parent anchor") in
[attachments.scad](https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad); what is
genuinely absent is the *composition* of the two for the anti-aligned attach case —
exactly the ambiguity §4.4 resolves. The survey's "sign convention is undocumented"
was over-broad; §3 now carries the precise form, and the "may be hard to predict"
quote is verified verbatim.
