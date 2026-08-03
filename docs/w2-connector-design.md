# Wall Connectors, Coupons & Mounts (W2) — implementation design doc

Status: **v2 — grounded in a targeted snap-fit/detent/keyhole/warp survey
([`research/w2-connector-coupon-survey.md`](research/w2-connector-coupon-survey.md),
sources in Appendix A) and revised per the adversarial grounding audit
([`research/w2-connector-grounding-audit.md`](research/w2-connector-grounding-audit.md);
contested bets recorded in Appendix B).**
Scope: the W2 rung of [`tile-wall-design.md`](tile-wall-design.md) §9 — the connector
library's first shipping member (clipseat + CornerClip), the fit and clip coupons, the
keyhole mount, wall `connect clips` with a connector BOM, and the Lab's instanced wall
preview. Deliverable: four tiles clipped into a square, hanging on **four** screws —
`mount keyhole` is declared on the *tile*, so every placement mints its own.

Builds on: [`tile-wall-design.md`](tile-wall-design.md) (the parent design; its §4 corner
clip and §6 keyhole are adopted and given engineering numbers here; its §10 Q1
rebate-vs-proud question stays decided-empirically by the coupon). Rides:
[`c2-assembly-design.md`](c2-assembly-design.md) — W2 consumes C2's printer profile, fit
ladder, material declarations, and `export parts`, and mints ports C2-style; it does
**not** route wall clips through `connect` (§8).

---

## 1. Goals

1. **The corner clip, buildable.** Turn the parent doc's §4 clip concept (bayonet X-bridge,
   ~30° past-center twist, jaws bearing on front border bands) into parameterized
   geometry with defensible numbers: strain budget, arm taper, detent size, fillets.
2. **The clipseat**, cut into tiles: corner well + seat recess + the §10-Q1 face rebate
   in **both** variants, since the coupon — not this doc — picks the default.
3. **Keyhole mounts** sized for a real #8 screw, with the stack-up validated against
   tile depth and the face-down-print bridging handled by design.
4. **Coupons as the fit-adjustment path.** A fit step gauge and a clip coupon (both
   rebate variants + one CornerClip), entered in the `/prototype` catalog — the printed
   analog of Multiboard's 0.25 mm tolerance note and openGrid's "rescale to 99.5%"
   advice.
5. **Wall integration**: `connect clips` on `wall`, interior-corner enumeration, a
   connector BOM line in the layout report, and an instanced Lab preview of the wall.

Non-goals for W2 (reserved words error with a W3 pointer): `pinloop`, `dovetail`,
`magnetpocket`, `snap`; wall-level mount grids; joint-placement rules (meaningless with
one connector type); fragment meshes and per-instance rotation in the Lab preview;
whole-wall STL.

## 2. Engine ground truth

Facts verified against the bikar tree that shape the design:

- **The Lab is a Canvas-2D painter's-algorithm renderer** (`packages/lab/src/viewer.ts`)
  — not three.js. "Instanced preview" therefore means: project the module tile's mesh
  once per frame, stamp per-instance screen offsets (wall instances are pure XY
  translations in W2), draw instances back-to-front. The Lab worker currently rejects
  non-orb sources, so the wall preview needs a worker/protocol extension, not just a
  viewer change. (See §9 for how this diverges from the survey's three.js findings.)
- **`solidifyExtrudedPiece` supports circular, outline-interior z-band holes only**;
  outline-breaching cuts throw. The clipseat's corner cuts breach the outline and the
  keyhole is non-circular — both are outside the current solidifier's model. The one
  new geometric primitive W2 needs is a **slab-stack solidifier** (§7).
- **W1 tiles are unpierced slabs** — `inscribe` art is 2D-only. The "no lattice void
  under a jaw" check is therefore a 2D query of art segments against jaw footprints,
  not a 3D one.
- **z-convention**: z = 0 is the back/bed face, z = depth the front face. Clipseat
  recess and keyhole cut from the back; the 0.6 mm jaw rebate cuts from the front.
- **Byte-identity**: tiles without W2 features never enter the new solidifier —
  existing STLs stay byte-identical, backed by a regression test on `Nail-Wall.bkr`.
- **C2 boundary**: W2 consumes C2's profile/fit/material/`export parts` through one
  seam — `PrinterProfileFacts {holeCompMm, warpMm?, perimeterWidthMm}` read at a single
  function (`resolveClipDims`) — so C2 slippage or type drift costs one adapter, and
  the coupons can fall back to one-`.bkr`-per-part if `export parts` slips.

## 3. What the survey established (the load-bearing facts)

From [`research/w2-connector-coupon-survey.md`](research/w2-connector-coupon-survey.md);
numbers restated so the doc stands alone.

- **Snap-arm sizing comes from the Bayer/Covestro guide** (the primary source, fetched
  in full): permissible deflection y = 0.67·ε·l²/h for a constant arm and **1.09·ε·l²/h
  for an arm tapered to h/2 at the tip** — the taper buys more than 60% extra
  deflection at the same root strain. Deflection force uses the secant modulus at
  actual strain. After joining, a snap feature must return to an essentially
  **stress-free condition** — retention must never depend on sustained strain
  (survey §1).
- **The working strain budget for printed PETG is ~2% effective.** Three independent
  chains land there (Appendix B.1 — the survey's original derivation cited a "7–10%
  PETG vendor design band" that could not be re-verified at its source and is
  withdrawn): (1) Covestro's amorphous-resin rule — up to ~70% of yield strain, PETG
  yield ~5–6% — times the 0.6 factor for repeatedly-separated joints gives ~2.1–2.5%;
  (2) the community heuristic of designing to 10–15% of elongation-at-break (Hackaday)
  gives 2.4–3.6% of PETG's ~24%; (3) Core77/Fictiv's FDM anisotropy rule — elongation
  at break drops ~50% across layer planes, so derate Z-flexing members by half — which
  W2 sidesteps entirely by keeping every flexing member in the XY print plane (also
  the Hubs orientation rule), holding the halving in reserve as margin (survey §1,
  audit deep-dive 2).
- **Root fillet ≥ 0.5× arm thickness** (Hubs' FDM restatement of Covestro's
  stress-concentration knee at R/h ≈ 0.6; absolute minimum ~0.4 mm) (survey §1).
- **The detent number converges from two independent sources**: 0.3–0.5 mm of proud,
  rounded, filleted bump gives a clear tactile click (Firgelli's bayonet guide;
  SnapLock's printed twist-lock uses the same range — both verified verbatim by the
  audit; one popular parametric coupling ships at ~0.2 mm, so the low end is soft —
  Appendix B.6). Supporting geometry: ~5° entry clearance on engaging faces,
  0.1–0.2 mm radial clearance, slot corner radii ≥ 0.5 mm, ~1 mm fillets at lug roots
  (Sherlock's printed lens mounts — to strengthen the lugs and stop them warping
  upward during printing), 0.3 mm chamfers under overhung lugs (survey §2).
- **A ~30° twist is below the 60–120° hardware norm** (Firgelli's 90° default;
  Seetronic's 60–120° range) **but inside printed practice** (SnapLock locks in 20°
  with four tabs; 60° is normal for small fittings). No surveyed source quantifies
  retention as a function of twist angle below 60° — the 30°/four-arm geometry rests
  on the SnapLock existence proof and is confirmed or rejected by coupon W-C1, not by
  literature (survey §2, Appendix B.4).
- **The keyhole dimensions check out against primary screw tables**: #8 *slotted* pan
  head ⌀8.18 mm × 2.44 mm high (ASME B18.6.3), major ⌀4.17 mm — so ⌀9.5 entry
  (~1.3 mm head clearance, matching the 3/8-in hardware norm), 4.7 mm slot (0.5 mm
  shank clearance), and a ~3–3.6 mm head cavity all have sensible margins. The more
  common cross-recessed (Phillips) pan head runs taller — #8 max 2.92 mm (B18.6.3
  Type 2) — which the 3.6 mm cavity still clears (§4.3; audit deep-dive 5)
  (survey §3).
- **Face-down keyhole cavities are bridges.** The conservative bridge rule is ~10 mm
  (Hydra; UltiMaker allows more, community practice reaches 20–30 mm on tuned
  machines — Appendix B.3); the proven roof treatment is a **flat or stepped roof
  ~0.4 mm above the theoretical ceiling** to absorb first-bridge droop, with
  sequential bridging for wider spans (survey §3).
- **No *surveyed* published warp number exists for our exact case** (100×100×4 mm
  PETG on textured PEI; nearest miss: a 2025 Int. Polymer Processing study tests PETG
  adhesion on PEI and textured plates without reporting plate-warp magnitudes, and
  quantitative warp studies exist for ABS/PLA+ — Appendix B.5). Community reports put
  badly-printed large flat parts at 1–3 mm of bow (WhyItFailed); the parent doc's
  0.2–0.5 mm band is a labeled placeholder until the clip coupon measures it
  (straightedge + feeler gauges at corners, center, diagonals — the published
  per-corner protocol at shop-tool cost). PETG flat-plate practice varies by source:
  bed 80–90 °C, brim 5–8 mm (contested), reduced or disabled part/aux cooling —
  while Prusa's official line is that PETG barely warps at all. The coupon exists
  precisely because vendor statements conflict (survey §4, Appendix B.5).
- **Every surveyed printed wall system separates alignment from retention** (Multiboard
  snaps, openGrid pegs + wall screws, HSW fasteners, Gridfinity's screwed-down
  baseplates — its magnet/M3 features join blocks *to* baseplates, and no native
  plate-to-plate joint exists), keeps tile-to-tile joints compliant, sources stiffness
  from the wall,
  and ships a per-printer fit adjustment path. openGrid states the division outright:
  connectors are "primarily for alignment rather than structural support" (survey §5).
- **The tile-leveling clip's transferable principle**: coplanarity comes from clamping
  both front faces to one shared reference spanning the joint — never from butting
  edges (survey §5). This is why the clip jaws bear on the front border bands.

## 4. Language design

All new statement words are contextual identifiers; `clip` is already a keyword
(`crop clip`), and a top-level `clip <Name>` dispatch is unambiguous.

### 4.1 `clipseat` — the tile-side cuts

```bkr
tile ClipTile
  face sq_face
  art tile_art
  border 5
  depth 10
  clipseat corners rebate 0.6      # or:  clipseat corners proud
  mount keyhole screw no8 at centroid
```

The variant word is **required** — per the parent doc's §10 Q1, neither rebate nor
proud is a default until the coupon decides; the error message says exactly that.
Optional dimension overrides (`seat d <mm> depth <mm>`, `well d <mm>`, `jaw <mm>`) keep
coupon iteration in `.bkr` params, never in TypeScript.

Per-corner geometry (all cuts open to both edges, centered on the corner):

1. **Corner well** — quarter-disc r 3.5 mm, full depth. Four wells plus the gap cross
   form the central opening that gives the clip's risers rotation clearance during the
   ~30° twist — a rigid riser cannot swing inside a 1.2 mm gap channel; the well is
   what makes the bayonet kinematically possible.
2. **Seat recess** — quarter-disc r 9 mm, 1.8 mm deep from the **back**: the arm sweep
   envelope and detent plane.
3. **Face rebate** (variant `rebate`) — quarter-annulus r 3.5..8 mm, 0.6 mm deep from
   the **front**, so the jaw sits flush; variant `proud` cuts nothing.

### 4.2 `clip` — a generated piece, not an authored one

```bkr
clip StarClip for ClipTile gap 1.2
  material petg                    # default petg; pla → compile ERROR
```

The CornerClip is a **parametric built-in generator** (like `orb`/`tile`/`wall`), not a
`.bkr`-authored piece and not a macro: the piece grammar cannot express multi-level XY
sections with hooked jaws, and hand-copied dimensions that must co-vary with tile
border/depth/gap/profile are exactly the mismatch class the parent doc's §3.3
"generated piece + matching tile feature" rule exists to prevent. Every dimension
derives from the tile declaration, the wall gap, the fit ladder, and the printer
profile in one resolver — seat and clip cannot drift apart because one module owns
both sides.

The clip solid is a three-slab X-bridge, printed as modeled with all flexing members
in the XY plane (§3's orientation rule): four jaw pads (the bearing feet, landing on
the border band), four risers (through the wells), and a hub-plus-arms plate with the
past-center detent as a **full-width transverse rib** stepping down from the arm
underside (a point bump under the tapered tip is neither printable nor watertight — see
§12). Applied survey numbers: arms
**taper toward h/2** at the tip (the 1.09 formula's >60% deflection dividend); root
fillets **≥ 0.5× arm thickness**; detent **0.3–0.5 mm** proud, rounded, mating into a
slightly larger pocket; ~5° entry clearance on blade faces; 0.1–0.2 mm radial
clearance in the seat; ~1 mm fillets at blade roots; seated state near **stress-free**
with only a small residual bias for anti-rattle (the printed substitute for a metal
bayonet's preload spring). That bias, and the matching setback that keeps the arm
plate sub-flush, are the one pair of numbers here with no survey behind them at all:
they ship as `CLIP_Z_BIAS_MM_CAL` under **`CAL-CLP-01`**, settled by W-C1, and the
absence of a source is why the bet exists rather than a footnote. Working strain
budgeted at **≤ ~2%** effective for PETG.
Capture depth = `max(1.0 mm, 2 × measured warp)` from the profile's `warpMm`
(`CLIP_CAPTURE_FLOOR_MM_CAL`, **`CAL-WRP-01`**) — the 1.0 mm fallback holds until
MC-5 measures real warp (§11 Q3).

`material pla` is a compile **error** (aged PLA fractures on the engage flex and
relaxes preload — the parent doc's §5/B.3 embrittlement rule), not a warning. The
counter-position is real — design-allowables sources treat PLA snaps as designable
and toughened PLA is marketed for exactly this — but none of them address ambient
aging, which is precisely a wall clip's load case; the full argument and the
tough-PLA escape hatch are in Appendix B.2.

### 4.3 `mount keyhole`

```bkr
  mount keyhole screw no8 at centroid      # or: at <x>, <y>
```

Cut from the back (z = 0), slot extending +y so the tile slides down onto the screw:
a 4 mm **collar** slab whose surface region is the ⌀9.5 entry circle ∪ 4.7 × 8 mm
shank slot, then a head cavity slab (⌀10.5 ∪ 9.0 × 8 mm, 3.6 mm deep) strictly
containing the surface region — the shoulder the screw head hooks behind is a proper
nested ring for the slab solidifier. Screw table: `no6` and `no8` (#8: shank 4.2 →
slot 4.7; head ⌀8.4 × 3.1 → cavity ⌀10.5 × 3.6 — clearing the ASME slotted pan head
⌀8.18 × 2.44 from §3 with margin, and still clearing the taller cross-recessed
(Phillips) pan head at its B18.6.3 Type-2 max of 2.92 mm, which is what a user will
actually buy). Flat-head (countersunk) screws are out of scope for the keyhole
cavity.

**Stack-up validator**: a #8 keyhole needs 4 (collar) + 3.6 (cavity) + 1.2 (front
floor) = **8.8 mm of depth** — a 6 mm tile cannot hold one, which is why the W2
deliverable tile declares `depth 10` and `Nail-Wall.bkr` is untouched. The tile-edge
margin rule extends from circle-radius to **footprint bbox**: the keyhole's widest
extent must clear every tile edge and every clipseat corner footprint by ≥ 6 mm.

**Bridging**: printed back-down, the head cavity's roof is a ~⌀10.5 bridge — at the
edge of the conservative 10 mm rule, though nowhere near modern printer limits
(Multiboard's own snaps demand 30 mm bridging; Appendix B.3 records why the
conservative rule is kept anyway). The cavity roof is generated as a **flat roof
with a 0.4 mm droop allowance** rather than a circular ceiling (§3's proven
treatment); roof quality is inspected on the first deliverable print and logged in
the catalog.

### 4.4 `wall connect`

```bkr
wall StarWall
  boundary 201.2 x 201.2
  module ClipTile gap 1.2
  connect clips                    # default: connect none (parent doc B.1)
```

`connect clips` requires the module tile to declare a clipseat and, if a `clip … for
<moduleTile>` is declared in-file, cross-checks its gap against the wall's — a clip
generated for a different gap is a compile error.

## 5. Clip placement is layout-derived — not `connect`-derived

A 2×2 clipped grid is the canonical connect-graph **cycle** (the parent composition
doc's §4.4/B.3 example): routing wall clips through C2's `connect` tree would trip
closure checks *by design*, on every wall. So the wall emits clip placements and the
connector BOM directly from the layout kernel: a grid vertex receives a clip iff all
four adjacent placements exist and are full (cropped or missing corners get none —
the conservative all-full rule; per-fragment corner refinement is W3). C2's machinery
is still honored at the edges: clipseat corners and keyholes **mint ports**
(`Tile.clipseat.ne`, `Tile.keyhole`) exactly like hole ports, so future assemblies
can reference them; the placement math just never goes through `connect`.

The layout report gains the BOM line the parent doc's §7 promised:

```
connectors: 4 × CornerClip (StarClip, petg) — 1 interior corner, 8 perimeter corners unclipped; screws: 4 × no8 keyhole
```

## 6. Validators (compile-time; house error style)

| # | Check | Severity |
|---|---|---|
| 1 | Clipseat variant word present (`rebate <mm>` or `proud`) | error, cites §10 Q1 |
| 2 | Jaw bearing: border ≥ 4 mm continuous flat band under the jaw annulus | error |
| 3 | Art occupancy: no inscribed segment crosses a jaw footprint (2D distance test — the bbox-only art check misses diagonal incursions) | error |
| 4 | Recess floor: depth − 1.8 ≥ 3 perimeter widths under clamp loads | error |
| 5 | `material pla` on a clip | error |
| 6 | Keyhole stack-up: depth ≥ 8.8 mm for #8 | error |
| 7 | Keyhole/clipseat footprint-bbox margins ≥ 6 mm (edges and cross-feature) | error |
| 8 | `connect clips` needs a clipseat on the module tile | error |
| 9 | Clip/wall gap coherence | error |
| 10 | W3 connector words (`pinloop`, `dovetail`, `magnetpocket`, `snap`) | error, "W3 connector type" |

Deferred to W3 with in-code comments: joint-placement rules, the gap-formula floor and
environment gates, anchor budgets, and the `capture < 2× measured warp` WARN (which
can only fire once the coupon has produced a measured `warpMm`).

## 7. Kernel: the slab-stack solidifier

The tile's new cuts and the clip solid are the same shape class — **a stack of
z-slabs, each with its own planar section** (disjoint outline islands + interior hole
rings), sections changing only at slab boundaries. One new module generalizes the
extrude solidifier in exactly two ways: per-slab outlines (corner cuts breach the
square) and multiple disjoint islands (the clip's four jaw pads). Interface faces
between adjacent slabs are computed under a **strict nesting contract** — every ring
pair across an interface must be identical, strictly nested, or disjoint; partial
overlap throws. That keeps the module honest without growing a general 2D boolean
layer (which stays C-track work, per the parent composition doc's Clipper2 recipe).
`solidifyExtrudedPiece` itself is untouched; shared helpers get exported, and W1
outputs stay byte-identical.

> **⚠️ Superseded in implementation (2026-07-29).** The nesting contract in the
> paragraph above did not survive contact with the shapes. A corner-rebated square
> and its seat-recessed sibling **share long boundary stretches** rather than
> nesting one inside the other — partial overlap under this contract, so it would
> have thrown on the primary deliverable. What shipped is a **shared cell
> partition**: the caller decomposes the union of all sections into non-overlapping
> 2D cells, each slab is the subset of cells solid in its z range, walls come from
> boundary edges with no twin in the slab, and interface faces from cells whose
> membership flips between adjacent slabs (cell identity by object reference).
> The non-overlap invariant replaces the nesting invariant. Everything else in this
> section held: no boolean layer, `solidifyExtrudedPiece` untouched, W1 byte-identical.
> See `bikar/packages/core/src/kernel3d/solidify-slabs.ts` (module header) and
> `bikar/docs/decisions/2026-07-29-w2-wall-connectors-mounts.md` §A. This paragraph
> is left standing as the proposal it was.

## 8. Coupons and the prototype catalog

Coupon files in a new `patterns/Coupons/` directory (invisible to the 3d-models
gallery Makefile, which globs only `patterns/Orbs/`; the bikar pre-commit still
compiles them):

- **`Clipseat-Fit-Coupon.bkr`** — the clip joint's clearance ladder: one 40 mm
  clipseat dummy tile plus five `CornerClip`s whose declared `gap` walks the blade
  clearance from 0.40 mm down to 0.00 mm, every dimension a `param`. Catalog entry
  **W-F1**; its measured result sets `CLIP_CLEARANCE_MM.insert` and the `gap` to
  declare.

  > **Corrected 2026-08-02.** This bullet originally named a file called
  > `Fit-Step-Gauge.bkr` and described a *bore-and-pin* ladder — a plate of holes
  > at the press/snug/sliding/free intents around a nominal pin ⌀, plus matching
  > pins — assigning it catalog entry **W-F1** and saying its results set the
  > profile's `holeCompMm` "shared with C2's fit coupon procedure". Two things were
  > wrong. The filename never existed: what shipped is `Fit-Coupon.bkr`, and as a
  > *machine* measurement it was in turn superseded by MC-1's `MC1FitLadder`
  > (catalog: [`.claude/skills/prototype/catalog.md`](../.claude/skills/prototype/catalog.md)).
  > And the joint
  > was the wrong one — a bore-and-pin number does not transfer to a bayonet blade
  > that drops down a channel and then sweeps sideways under load, because a blade
  > can pass the drop and still bind on the twist. The transfer condition could not
  > be written, so the rule did not transfer (**K10**); the fix was a second file
  > for the second joint. See `docs/decisions-log.md` **D-008**.
- **`Clip-Coupon.bkr`** — two 40 mm dummy tiles (`CouponTileRebate` with
  `clipseat corners rebate 0.6`, `CouponTileProud` with `clipseat corners proud`)
  plus one `CouponClip`. Print four of each dummy → two real four-corner joints in
  both jaw variants. Catalog entry **W-C1**; its questions: (1) whether the
  capture default holds at the warp **MC-5** measured (`CAL-WRP-01`) — W-C1
  checks the clip against that number, it does not measure warp itself (§11 Q3);
  (2) **§10 Q1** — rebate vs proud in
  raking light, the decided-empirical verdict that sets the grammar default;
  (3) detent past-center feel and engage force; (4) PETG jaw survival over repeated
  engagement; (5) front-face lippage across the joint vs back registration.

This is the per-printer fit-adjustment path every surveyed ecosystem ships in some
form (Multiboard's 0.25 mm design tolerance, openGrid's 99.5% rescale advice, HSW's
"print one test insert first") — ours closes the loop into the compiler profile
instead of a README. Printing is currently on hold, so both entries land as `planned`.

Deliverable pattern: **`patterns/Walls/Clip-Wall.bkr`** — 100 mm tile (`border 5`,
`depth 10`, clipseat rebate, centroid #8 keyhole), a `clip` declaration, and a
201.2 × 201.2 wall with `gap 1.2 connect clips` → four full tiles, one interior clip,
four screws. Catalog entry **W2**.

> **Corrected 2026-08-03.** This paragraph and §2's scope line both said the
> deliverable hangs "on one screw". It hangs on four. `mount keyhole` is declared on
> the **tile**, at its centroid, so a wall mints one keyhole per placement — and the
> compiler has been saying so all along. Rendering the shipped model prints
> `screws: 4 × no8 keyhole` on the BOM line beside `1 × CornerClip`. §5's illustrative
> BOM in this same doc also reads `screws: 4 × no8 keyhole`, for a larger wall; two
> sections of one doc disagreed and neither needed a source to settle (**K7**).
> Whether a wall *should* be able to declare a single shared mount is a real design
> question, and a different one — it is **§11 Q6**, not something this line decided.

## 9. Lab instanced wall preview — and a survey divergence

The survey's §6 documents three.js `InstancedMesh` (per-instance matrices, the
bounding-sphere/frustum-culling pitfall, `instanceId` picking) — useful, but **the
Lab is not three.js** (§2): it is a Canvas-2D painter's-algorithm viewer, and W2 keeps
it that way. What transfers is the structural lesson — share one geometry, apply
per-instance transforms — implemented natively: project the module tile's mesh once
per frame; each wall instance is a pure XY translation, which projects to a constant
per-instance screen offset; draw instances back-to-front by projected center depth
with triangles pre-sorted once within the tile (a two-level painter — correct for
disjoint coplanar slabs except razor-edge-on views, which is accepted and commented).
The three.js findings stay on file for any future viewer migration; adopting
`InstancedMesh` now would mean adopting three.js itself, which no W2 requirement
justifies at N = 4 instances. (The survey's "either approach performs fine below
~50 instances" is an internal estimate, not a published threshold — no source gives
one; three.js issue #30352 documents instancing being *slower* than plain meshes at
few instances, which supports staying put — Appendix B.7.)

Plumbing: the worker protocol gains an optional `wall` payload (name, pitch,
boundary, placements, fragment/clip counts) and a `'wall'` family; the worker stops
requiring an orb declaration when a wall result is present; the viewer gains
`setMesh(mesh, instances?)`; wall results render a caption line and suppress
orb-only UI. Explicitly out (scope-guard comment in code): fragment meshes, the clip
mesh, per-instance rotation, preset chips, whole-wall STL.

## 10. Phasing

Eight commit-sized steps, each leaving tests + typecheck + lint green: (1) slab-stack
solidifier + shared-helper refactor; (2) `mount keyhole` end-to-end; (3) `clipseat`
grammar + cuts + validators; (4) `clip` declaration + CornerClip generator + profile
seam; (5) wall `connect clips` + interior-corner enumeration + BOM; (6) Lab wall
preview; (7) deliverable + coupon patterns (rendered and eyeballed before commit);
(8) 3d-models catalog entries W-F1/W-C1. W2 rides C2's release train but is
insulated: with C2 slipped, the profile seam falls back to placeholder constants and
the coupons split into one file per part.

## 11. Open questions

- **Q1 — rebate vs proud** (inherited from the parent doc §10 Q1, unchanged): decided
  empirically by W-C1 in raking light; until then the variant word is mandatory.
- **Q2 — detent dimensions and feel.** 0.3–0.5 mm is the surveyed range; where in
  that range our PETG + this seat geometry lands (click vs shear vs mush) is W-C1
  question 3. Every detent dimension is a `param`.
- **Q3 — measured warp.** The 1.0 mm capture fallback stands in for
  `2 × measured warp` until the real number is measured on this printer. That
  measurement is **`CAL-WRP-01`, settled by machine-card coupon MC-5** (warp
  plate) — not by W-C1, as this line previously said. Warp is a property of
  *(printer, material, nozzle, profile)*, not of a clip: MC-5 measures it once
  on a large thin plate, and W-C1 consumes the number rather than re-deriving
  it from a 40 mm dummy tile whose footprint barely warps. The constant lives in
  `bikar/packages/core/src/kernel3d/corner-clip.ts` as `CLIP_CAPTURE_FLOOR_MM_CAL`
  and carries that bet in code.
- **Q4 — keyhole cavity roof quality.** The ~⌀10.5 flat-roof bridge is at the edge of
  *our conservative 10 mm rule* — not the edge of printability (Appendix B.3);
  verified by inspection on the first Clip-Wall print.
- **Q5 — fragment-corner clips.** W2's all-four-full rule leaves some structurally
  fine corners unclipped on cropped walls; per-fragment corner analysis is W3.
- **Q6 — one mount per tile, or one per wall?** `mount keyhole` is declared on the
  tile, so an N-tile wall needs N screws. That is the honest reading of the grammar
  and it is what ships; whether a clipped grid *wants* a wall-level mount — one or
  two screws carrying a rigid clipped panel, the tiles below hanging off their
  neighbours — is undecided and partly empirical: it depends on whether the engaged
  clip carries shear, which **W-C1** measures (its detent/engage questions are about
  capture, not load). Not a defect in the grammar, and not something the deliverable
  paragraph should have settled in passing. Raised 2026-08-03 by the correction
  recorded in §8.

## 12. Detent geometry — resolved during implementation (commit W2 4/8)

The §4.2 phrase "detent as a ramp bump on the arm underside" is under-specified in a
way that only surfaced when the CornerClip generator tried to build it. Two independent
failures showed the *small interior bump* reading is not buildable **or** printable, and
the fix changes the detent's shape (not its size or the survey numbers behind it).

### 12.1 Why the small interior bump fails

The arm tapers from `wArmRoot` at the root to `wArmTip = wArmRoot / 2` at the tip, and
the detent's default plan footprint (`CLIP_DETENT_LEN_MM` square, at
`rDetentIn = rPadOut + 0.15`) lands **under the narrow tip**. At the default rebate
fixture (tile depth 10, gap 1.2) this leaves the bump surrounded by **0.05–0.32 mm** of
arm material on three sides. Two consequences:

1. **Un-printable.** Those surrounding walls are below the 0.4 mm perimeter width, so an
   FDM printer cannot render them as solid — the very rule the generator enforces
   everywhere else (`validateClipDims` rejects sub-two-perimeter jaw blades).
2. **Un-meshable in the flat-prism slab model.** A proud bump *inside* the arm is an
   interior island: the plate slab must punch it as a hole and refill it, and the fill's
   top face must weld to the plate bottom. But the wedge cap and the bump cap are
   triangulated by **independent earcut calls that do not agree**, so their shared
   boundary never pairs and the mesh is non-watertight (euler 3, one unpaired sliver
   triangle per limb). Every slab-membership permutation was tried — detent continuous
   (6 open edges), detent as two refs (a zero-thickness membrane, euler 14+), detent
   only below the plate (a doubled surface, 37 edges) — and each fails topologically.
   This is a genuine limitation of flat-prism slabs for a sub-plate boss that is an
   interior island, **not** a solidifier bug: `detent 0` produces a fully watertight,
   euler-2 clip, and the jaw pads (also holes-refilled-fresh) weld correctly because
   they *reappear* in the plate slab with a sealing bottom cap, which a bump directly
   under the plate cannot do.

### 12.2 Options considered

| Option | Shape | Printable | Weldable | Keeps click | Cost |
|---|---|---|---|---|---|
| **A. Full-width rib** ✅ chosen | Detent spans the **entire arm width** over `[rDetentIn, rDetentOut]` — a downward step of the whole arm cross-section, not an interior island | Yes (edge-to-edge, no thin walls) | Yes (rib side edges coincide with arm edges → walls pair as twins; the band is a first-class cell split out of the arm, continuous bump→plate) | Yes — same proud height, same survey 0.3–0.5 mm range | generator rework + volume-test rework |
| B. Ship `detent 0` default | No bump | Yes | Yes (already euler 2) | No — deferred to the physical coupon | ~none |
| C. Relocate to hub | Bump moved to the wide hub/arm-root region | Yes | Yes | Yes, but the click engages near the assembly centre, not at the seat rim | new dims + tests |

### 12.3 Chosen fix — full-width transverse rib

The detent becomes a **full-width rib**: over the radial band `[rDetentIn, rDetentOut]`
the *entire arm cross-section* steps down by `detentMm`. Because the rib's ±y edges lie
exactly on the arm's tapered ±y edges, the rib is not an interior hole — it is the arm
band split into its own cell, present in both the detent slab and the plate slab as one
continuous reference (the C1 shared-ref rule), with the inner-arm and tip segments
butting against it at `rDetentIn` / `rDetentOut` along shared transverse edges that pair
as twins. No sub-perimeter walls, no independent-earcut weld seam.

This preserves everything the survey fixed (§B.6): the proud height stays `detentMm`
(default 0.4 mm, still a `param`, still in the 0.3–0.5 mm band), the rib still mates as
an anti-rattle preload against the flat seat floor, and `detent 0` still disables it.
What changes is only the **plan shape** — a transverse rib instead of a point bump —
which is if anything closer to a bayonet's full-width detent ramp than the original
point reading. The W-C1 coupon (Q2) still settles the exact proud height and feel;
this section only records that the *geometry class* is a rib, decided by buildability,
not the number.

## Appendix A — survey sources

Primary source file, checked in verbatim with all URLs and access-failure notes:
[`research/w2-connector-coupon-survey.md`](research/w2-connector-coupon-survey.md)
(research date 2026-07-28; §1 cantilever snap-fit engineering, §2 bayonet/detent
geometry, §3 keyhole dimensions + face-down bridging, §4 warp measurement, §5 printed
wall-system joints + tile-leveling clips, §6 three.js instancing). It deliberately
does not re-cover [`research/tile-craft-field-survey.md`](research/tile-craft-field-survey.md)
(the parent doc's survey) or
[`research/tile-wall-grounding-audit.md`](research/tile-wall-grounding-audit.md).

The adversarial grounding audit of this doc is checked in verbatim at
[`research/w2-connector-grounding-audit.md`](research/w2-connector-grounding-audit.md)
(audit date 2026-07-28). The survey file itself is checked in verbatim and is not
edited retroactively — the attribution errors the audit found in it (the Unionfab
strain band, the Prusa-forum 1–3 mm figure, the Bambu-forum practice bundle, the
Gridfinity baseplate wording, the Sherlock fillet rationale) are corrected here and
recorded in Appendix B, with the audit as the source of the corrections.

Load-bearing numbers restated against link rot: tapered-arm deflection y = 1.09·ε·l²/h
(>60% over constant section — verified against the Covestro PDF's Table 1 by the
audit); PETG effective design strain ~2% (three-chain derivation in §3; the 0.6
rejoining factor is Covestro verbatim); root fillet ≥ 0.5× arm thickness (min
~0.4 mm); detent 0.3–0.5 mm (Firgelli + SnapLock, both verbatim); #8 slotted pan head
⌀8.18 × 2.44 mm (Phillips pan max 2.92 mm), major ⌀4.17 mm; keyhole entry ⌀9.5 =
3/8-in hardware norm; conservative bridge span ~10 mm with 0.4 mm flat-roof droop
allowance (counter-spread 20–30 mm, B.3); community flat-plate bow reports 1–3 mm
worst case (WhyItFailed) with no surveyed published number for 100×100×4 PETG on
textured PEI; Multiboard 0.25 mm design tolerance (unverified snippet — the Thangs
listings carrying it return 403); openGrid 99.5% rescale advice (board guide only).

Key direct sources (full list in the survey; attributions corrected per the audit): the
[Bayer/Covestro snap-fit design guide](https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1556891135.pdf),
[Machine Design on the AlliedSignal/McMaster–Lee Q-factor equations](https://www.machinedesign.com/archive/article/21818595/new-equations-make-fastening-plastic-components-a-snap)
(previously mislabeled "BASF" — the article credits McMaster & Lee of AlliedSignal),
[Hubs snap-fit guide](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/),
[Core77/Fictiv on snap-fit design and the 50% Z-axis derating](https://www.core77.com/posts/65318/how-to-design-snap-fit-components),
[Hackaday's snap-fit strain heuristic](https://hackaday.com/2022/11/11/oh-snap-3d-printing-snapping-parts-without-breakage/),
[Firgelli bayonet-joint guide](https://www.firgelliauto.com/blogs/mechanisms/bayonet-joint),
[SnapLock parametric twist-lock](https://github.com/flight505/SnapLock),
[Seetronic on bayonet connector norms](https://seetronic.com/blog/what-is-a-bayonet-connector-a-guide-to-quick-disconnect-solutions/),
[Nick Sherlock's printed lens mounts](https://www.nicksherlock.com/2024/01/reverse-engineering-lens-mounts-for-3d-printing/),
[ASME B18.6.3 head dimensions (mirror)](https://www.globalfastener.com/standards/detail_4972.html),
[Torqbolt B18.6.3 slotted-pan table](https://torqbolt.com/asme-b18-6-3-slotted-pan-head-machine-screws-dimensions-standards-specifications)
(mirror for the [Engineers Edge pan-head table](https://www.engineersedge.com/pan_head1.htm), which now returns 403),
[Boltingspecialist B18.6.3 Type-2 cross-recessed pan heads](https://boltingspecialist.com/dimensions/asme-b18-6-3-type-2-cross-recessed-pan-head-machine-screws/index.html),
[rahix's design-for-3d-printing notes (roof treatments)](https://blog.rahix.de/design-for-3d-printing/),
[WhyItFailed on PETG warping](https://whyitfailed.fyi/blog/petg-warping-causes-and-how-to-fix-it),
[Prusa's PETG material guide](https://help.prusa3d.com/article/petg_2059),
[De Gruyter Int. Polymer Processing 2025 print-surface adhesion study](https://www.degruyterbrill.com/document/doi/10.1515/ipp-2025-0113/html)
(unverified snippet; nearest-miss prior art for the warp non-number),
[openGrid board guide](https://www.opengrid.world/guides/board/),
[Multibuild core-parts docs](https://docs.multibuild.io/beginner-section/core-parts-documentation),
[Gridfinity specification](https://gridfinity.xyz/specification/),
[DIYTileGuy on tile-leveling systems](https://www.diytileguy.com/tile-leveling-systems/),
[three.js InstancedMesh docs](https://threejs.org/docs/pages/InstancedMesh.html),
[three.js issue #30352 (instancing slower at few instances)](https://github.com/mrdoob/three.js/issues/30352).

## Appendix B — contested bets and why they stand

One entry per claim the grounding audit contested; the audit report
([`research/w2-connector-grounding-audit.md`](research/w2-connector-grounding-audit.md))
is the evidence trail for each.

Entries tagged `[CAL-…]` are **empirical** bets that no source can close — only a
measurement can. The id is the bet's entry in the registry
([`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md)), which
names the coupon that settles it; the ceremony is the `calibrate` skill (bikar
Tenet 30 — a physical constant is not earned until it records its provenance).

### B.1 The ~2% PETG strain budget — derivation replaced, endpoint kept

The audit broke the survey's original chain: the "7–10% PETG vendor design band"
attributed to Unionfab is not on that page (verified with two differently-framed
fetches), and no other source for that band was found — it is withdrawn as
apparently synthesized. The ½ cross-layer factor is real but belongs to
Core77/Fictiv, not Unionfab. The ~2% endpoint survives on three independent chains
(§3): Covestro's amorphous-resin rule × the 0.6 rejoin factor (~2.1–2.5%),
Hackaday's 10–15%-of-elongation heuristic (2.4–3.6%), and the Fictiv Z-derating held
in reserve because every flexing member prints in XY. Cross-lineage caveat: the
AlliedSignal/Ticona treatments allow only 50% of yield strain for amorphous resins
where Covestro allows 70% — Covestro is the liberal end of the doctrine; the other
safety factors absorb the spread.

### B.2 `material pla` on a clip is an error — a materials-policy call, not settled doctrine

The steelman is real: Fictiv's allowables table designs PLA snaps to 4–8% strain,
hobbyist reports of long-lived PLA clips exist (including the parent doc's own B.3
week-long test), and toughened PLA is marketed specifically for snap fits and living
hinges. The error is kept because the clip is a *generated* part where PETG costs the
user one spool swap, and the parent doc's aging hazard — ambient physical aging
collapsing PLA ductility so an aged arm fractures on the engage/disengage flex — is
exactly the load case a wall clip sees years after printing, and none of the pro-PLA
sources address aging. A tough/annealed-PLA story would be a new material word with
its own datasheet, not a bypass of this error.

### B.3 The ≤10 mm bridge rule — deliberately conservative, not a capability claim [CAL-BRG-01 — the same bet as print-validation B.4; one coupon (MC-3) closes both]

Credible counter-evidence says a ⌀10.5 mm bridge is nowhere near modern limits:
Multiboard's official snaps require printers to bridge up to 30 mm, community
guidance puts clean unsupported bridges at 20–25 mm on well-tuned machines, and
UltiMaker documents 25 mm with Tough PLA. The Hydra ≤10 mm rule is kept anyway
because the cavity roof is a cosmetic-and-functional seat printed at production
settings without per-part tuning, and the flat-roof + 0.4 mm droop allowance costs
nothing. Q4's "at the edge of the rule" means the edge of *our conservative rule*,
not the edge of printability.

### B.4 The ~30° twist — an existence proof, not a studied design point

No surveyed source quantifies retention as a function of twist angle below 60°
(Firgelli offers nothing below 60°; Seetronic puts the hardware norm at 60–120°;
SnapLock's 20°/four-tab lock is an enclosure lid — a lower-stakes retention job than
holding four wall tiles coplanar). Equally, no source argues 30° is inadequate. This
is a genuinely coupon-decided bet: W-C1 confirms or rejects it; the literature
cannot.

### B.5 The warp non-number — claim narrowed, practice bundle downgraded [CAL-WRP-01 — coupon MC-5, not W-F1: warp is a printer property]

The novelty claim survives as qualified in §3: "no *surveyed* published measurement
for this exact case." Nearest misses found by the audit: a 2025 Int. Polymer
Processing study (PLA/PETG/ASA adhesion on six surfaces including PEI and textured
plates — no plate-warp magnitudes) and quantitative warp studies for ABS (3.7 →
0.8 mm after tuning) and PLA+ (per-corner percent-error protocol). The 1–3 mm bow
figure re-homes to WhyItFailed — the originally-cited Prusa forum thread is purely
qualitative. The bed/brim/fan practice bundle is mixed community practice, not a
sourced spec: WhyItFailed says a 5 mm brim is plenty and part fan 30–40% rather than
off; Prusa's official guide flatly states PETG "does not shrink or warp" — directly
opposing WhyItFailed's 0.5–0.7% contraction figure. The coupon exists precisely
because these sources conflict; only the straightedge-and-feeler-gauge measurement
settles it.

### B.6 The detent 0.3–0.5 mm — verified verbatim, low end soft [CAL-DET-01 — coupon W-C1, design-specific: off the machine card by design]

Both attributions survived verbatim (Firgelli's "0.3-0.5 mm of axial relief gives a
clear tactile click"; SnapLock's "Minimal column protrusion (0.3–0.5 mm)"). A
popular parametric twist-lock coupling ships at ~0.2 mm of lock depth (unverified
snippet), so the range's floor is softer than "converges" implies. The doc already
handles this correctly: every detent dimension is a `param`, and W-C1 Q2 picks the
value by feel. One drift fixed: Firgelli's slot corner radius is "at least 0.5 mm",
not 0.3–0.5 mm.

### B.7 Canvas-2D over three.js — bet grounded, threshold de-numbered

The engine fact (the Lab is Canvas-2D) is repo ground truth, and the audit verified
three.js issue #30352 (InstancedMesh slower than plain meshes at few instances) —
which *supports* not adopting instancing at N = 4. The survey's "~50 instances"
threshold traces to nothing and is now labeled an internal estimate (§9); its one
cited performance article is 403 and was never verified. The steelman for adopting
three.js now (pre-investing in a 3D wall future) is weakened by the repo fact that
orbs already render in the Canvas-2D Lab — there is no separate three.js future the
wall preview would be buying into.

### B.8 The keyhole head cavity — sized for the worst pan head, not the nominal one

The audit found the survey's #8 pan head (⌀8.18 × 2.44 mm) is the *slotted* B18.6.3
value; the cross-recessed (Phillips) pan a user will actually buy runs to 2.92 mm
max (B18.6.3 Type 2). The design's 3.1 mm head allowance and 3.6 mm cavity clear
both; §4.3 now states the Phillips number explicitly and scopes flat-head screws
out. Also verified: keyhole plate norms (23/64-in ≈ 9.1 mm entry, #6 flathead,
30 lb rating) and the #8 major ⌀ 4.17 mm.
