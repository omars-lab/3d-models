# Piece Composition DSL — design doc (pre-implementation)

Status: **DRAFT v1 — grounded in a prior-art survey (§3, sources in Appendix A). No
implementation yet.**
Scope: extending the bikar DSL from "one declaration → one solid" to **composable pieces**:
functional solids (`piece`), subtractive features (`hole`), contract-bearing mating
interfaces (`port`/`connect`), assemblies with multi-part export, and openings on orbs — the
capability behind an orb pendant light (printed collar holding a purchased lamp socket,
mated to a lattice orb) and interconnecting wall tiles.

Sibling docs: `print-validation-design.md` (layer-by-layer printability gate — shares the
2D-boolean dependency introduced here); `tile-wall-design.md` (planned: tiles, corner
connectors, wall layouts — builds on the primitives in this doc).

---

## 1. Goals

1. **Compose without 3D CSG.** The engine's core property — watertight meshes *by
   construction* (2D face extraction → inset → earcut → extrude → stitch) — is preserved.
   All new subtraction is 2D-before-extrusion; all new fusion is boundary stitching at
   planar interfaces. True mesh booleans stay out of the core (§8).
2. **Ports are contracts, not just frames.** A mating interface carries dimensions and fit
   (pin ⌀, clearance class, ring size), so `connect` failures are compile-time errors
   ("pin ⌀3.0 + snug clearance exceeds socket ⌀3.1"), not failed prints. No surveyed
   system ships this (§3) — it is the deliberately novel part.
3. **One verb.** A single deterministic `connect` composes two named ports. No constraint
   solver, no position/orient/align/attach zoo.
4. **Assemblies export honestly.** Per-piece STL for plating, 3MF with one object per piece
   + placement transforms for assembled preview, every part passing the mesh gate and the
   print gate in its own print orientation.

Non-goals (v1): kinematic joints beyond rigid/axis (no sliders/hinges/ball — printed static
assemblies), chamfers/fillets across 3D seams, shell/offset of composed solids, weave-family
orb openings (strand surgery is a separate problem).

## 2. Engine ground truth

What exists and is reused unchanged: 2D pattern evaluation and planar-graph face extraction;
polygon inset/offset; earcut band triangulation; radial extrude + wall stitching
(`solidify-lattice.ts`); spatial-hash welding; binary STL emitter; mesh gate (watertight,
Euler, ≥1.2 mm strut floor, degenerate scan); knobs/params + Lab plumbing.

What is genuinely new: a robust general 2D boolean/offset layer (§5 note), prism/revolve
piece construction, the port/connect model, multi-part export, and orb boundary surgery.

## 3. Prior art — what we borrow, what we avoid

Condensed from the survey (Appendix A):

| System | Borrow | Avoid |
|---|---|---|
| BOSL2 attachments | anchor = position + direction + spin; mating = anchors point at each other; `inside`/`shiftout` idea for subtractive mating | four overlapping placement modules with different ignore-rules; attachability as heavy opt-in authoring |
| build123d joints | **named joints + deterministic pairwise `connect_to`** — declare, don't solve | joints requiring hand-computed Locations |
| CadQuery | — | numeric constraint solver (under-constrained ambiguity); geometric selectors (`faces(">Z")`) as the *naming* mechanism — predicates over derived topology silently re-target |
| OnShape/Fusion | mate connector = full frame owned by the part; one mate per connection; **As-Built semantics** (connect derives placement, never "moves" parts); **hole centers are implicit connectors** | the full 7-joint kinematic vocabulary (static prints need rigid + axis) |
| Manifold | ideal *backend* for the four ops stitching can't do (§8); lazy CSG-tree evaluation as an internal IR shape | making booleans the default and eroding 2D-first discipline |
| CGA / BOSL2 / KCL arrays | crop policies + index-driven per-instance variation (→ tile-wall doc) | — |

Three mistakes the survey says to design against: (1) solving instead of declaring,
(2) attachability as a bolted-on multi-API, (3) geometric selection instead of names-from-
birth. Bikar's rules therefore: every piece's ports come free from its declaration, mating
features carry author-given names, `connect` is pure frame composition.

## 4. Language design

Sketches use the existing line-statement `.bkr` style.

### 4.1 `piece` — functional solids

```bkr
piece BulbCollar
  tube inner 40.4 outer 46 height 18        # sugar for revolve of a rect ring profile
  hole grub radial 3.2 at height 9          # radial hole through the wall
  port mount rim top ring 46                # explicit port on the top rim
  port socket bore axis                     # the bore itself, as an axis port

piece PinPeg
  revolve
    profile pin                              # a named 2D profile (existing 2D machinery)
  port a tip dir -z
    kind pin d 3.0
```

Constructors: `extrude <outline> depth <mm>` (prisms — tiles, brackets), `revolve <profile>`
(collars, pins, knobs), `tube` sugar. Outlines and profiles are ordinary bikar 2D regions,
so the whole pattern language is available as piece geometry.

### 4.2 `hole` — stacked 2D subtraction

```bkr
piece Tile
  extrude square100 depth 6
  hole nail at centroid
    band d 3.5 from 0 to 4                  # shaft
    band d 7.0 from 4 to 6                  # countersink (front face)
```

A hole is a named stack of z-bands; each band subtracts a circle (or region) from the
piece's 2D section over that z range. Countersink/counterbore are band stacks — never a 3D
boolean. **Every hole automatically mints a port on its axis** (OnShape's implicit-connector
insight): `Tile.nail` is connectable without further declaration.

### 4.3 `port` — frame + contract

A port is (a) a frame: origin, z-direction, spin reference; (b) a contract: `kind` plus
dimensions and fit. v1 kinds: `pin` / `pin_socket` (⌀ + clearance class), `ring` / `rim`
(⌀ + depth, for collar-to-opening mating), `axis` (dimension-free rigid frame). Clearance
is an *intent* class, never a raw number: `fit press | snug | sliding | free` (designed
diametral gaps −0.10 / +0.05 / +0.15 / +0.35 mm), compiled through a printer profile that
adds hole compensation separately (§5).

### 4.4 `assembly` + `connect`

```bkr
assembly OrbLight
  place LampOrb
  place BulbCollar
  connect BulbCollar.mount to LampOrb.polar   # rigid: frames anti-aligned, rims flush
  connect PinPeg.a to Tile.nail spin 0        # spin about the shared axis if it matters
  export parts                                # per-piece STLs; `export assembled` → 3MF
```

Semantics: `connect` anti-aligns the two port frames (they point at each other, BOSL2
style), composes transforms deterministically, and **validates the contracts** — kind
compatibility, pin ⌀ + clearance vs socket ⌀, ring ⌀ and depth vs rim. As-built: pieces are
authored in their own frames; placement is derived. One connection per port; a second
`connect` on a used port is an error.

### 4.5 Orb openings — boundary surgery

```bkr
orb LampOrb
  base icosahedron subdivide 2
  radius 60
  ...
  open cap 24deg at pole                      # omit lattice faces in the polar cap
  port polar rim ring 46                      # the cap's ring boundary becomes a rim port
```

`open cap` removes faces whose centroids fall inside the cap angle and generates a clean
ring boundary; the solidifier stitches the ring's inner/outer shells with a wall exactly as
it already stitches void walls, keeping the mesh watertight through the surgery. The ring's
measured ⌀ backs the declared rim port (mismatch beyond tolerance = compile error, so the
contract can't lie about the geometry). Weave-family orbs reject `open` in v1.

**Lamp safety (product rule, enforced in docs/examples, not the compiler):** the printed
part is a *holder around a purchased E26/E27 socket* — never printed threads carrying
mains. Examples specify LED-only and PETG near the socket; the collar's `inner` default
stays a knob because socket bodies vary.

## 5. Fit, clearance, and the 2D layer

- The fit model separates two things every surveyed ecosystem conflates: **intent gap**
  (press −0.10 / snug +0.05 / sliding +0.15 / free +0.35 mm diametral) and **printer
  compensation** (FDM holes print 0.1–0.3 mm undersize while external dims run ~0.1 mm
  oversize; PETG's tacky surface eats another ~0.05 mm of running clearance). The `.bkr`
  stores intent; a `printer profile` (hole compensation, xy compensation, material) is
  applied at compile time — Multiboard-style user-adjustable tolerance, not baked-in
  numbers. Both are **calibration targets for the `/prototype` catalog**: a fit-coupon
  entry (pin/socket step gauge) lands with C2 and its measured results update the profile,
  propagating to every assembly at once.
- The 2D boolean/offset layer follows the Clipper2 recipe — scaled-integer coordinates,
  explicit post-simplify, area-threshold sliver culling — implemented natively in TS
  (existing offset code grows up) with `clipper2-wasm` used only as a test oracle; the JS
  ports are single-maintainer and dormant, so they don't get to be load-bearing. This same
  layer powers the print-validation gate's per-layer region math.

## 6. Export

- `export parts`: one STL per piece (plating in the slicer), named `<Assembly>-<Piece>.stl`.
- `export assembled`: 3MF — one `<object>` per piece, `<build>` items carrying placement
  transforms, per-item metadata recording port/connect provenance. Writer:
  `@jscadui/3mf-export` (already in manifold-3d's dependency tree, so it's free either way).
- The Lab/gallery preview renders the assembled transforms with instanced meshes.

## 7. Validation

Three gates, in order: **contract check** (compile-time, §4.4) → **mesh gate** per piece
(unchanged) → **print gate** per piece *in its print orientation* (`print orientation` on
the piece; see `print-validation-design.md` §4). qiyas is unaffected in v1 — pattern
fidelity stays 2D per-view; assembly correctness is symbolic (contracts), not visual.

## 8. Manifold policy — the escape hatch and its tripwire

Constructive stitching + 2D booleans cover every v1 feature. Four operations force real
mesh booleans, and only these justify the dependency: (1) non-coplanar intersection of two
already-3D solids (angled hole through a curved shell), (2) union of overlapping extrusions
from different planes, (3) chamfer/fillet across a 3D seam, (4) shell/offset of a composed
result. If a post-v1 feature needs one, adopt `manifold-3d` (~2.8 MB WASM, TS types, lazy
async init, guaranteed-manifold output; OpenSCAD's backend since 2025) as an **opt-in
backend the compiler selects per-operation** — never as the default path. Bikar's welded
watertight meshes are exactly the input contract Manifold wants, so the adapter is small
(~100 LOC MeshGL mapping). The guardrail is cultural: "just boolean it" must stay a
compiler decision, not an authoring idiom.

## 9. Phasing

- **C1 — pieces + holes** (small; ships with print-gate V1, shared 2D layer): `piece`,
  `extrude`/`revolve`/`tube`, `hole` z-bands, auto-minted hole ports. Deliverable: girih
  art tile with countersunk nail hole, gated STL.
- **C2 — ports + assemblies** (medium): explicit `port`, `connect` + contract validation,
  `assembly`, `export parts`/3MF, fit-coupon prototype entry, material profile table.
  Deliverable: two tiles + printed pins that actually fit.
- **C3 — orb openings** (medium-hard): `open cap`, rim ports, ring stitching, LampOrb +
  BulbCollar example. Deliverable: the orb pendant light, both parts gated.
- **C4 — Manifold backend** (only when a §8 case ships as a feature).

## 10. Open questions

1. Does `open cap` generalize to non-polar placements (cap at an arbitrary axis) in C3, or
   is polar-only enough for the lamp? (Leaning polar-only; the cord hangs down anyway.)
2. Port spin reference for `ring` kinds — does rotational registration ever matter for
   round collars, or is spin only meaningful for `pin` arrays? (Leaning: spin optional,
   default free.)
3. Should `assembly` participate in the knobs system (assembly-level params forwarded to
   pieces) in C2, or is per-piece knobs + shared material profile enough?

## Appendix A — survey sources

BOSL2 attachments + tutorial + distributors (BelfrySCAD wiki); OpenSCAD mailing-list
threads on BOSL2 anchoring pain; build123d joints docs; CadQuery selectors/assembly docs +
community verdicts; OnShape mate + mate-connector docs; Fusion 360 joint types; Manifold
repo/wiki, OpenSCAD integration discussion #387, npm `manifold-3d`; Clipper2 repo +
`clipper2-wasm`; CGA shape grammar (CityEngine); Tsugite (UIST 2020); 3MF core spec +
`@jscadui/3mf-export`; KCL `patternTransform`; Qidi/Hubs printed-fit clearance guides.
