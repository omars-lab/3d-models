# Piece Composition DSL — design doc (pre-implementation)

Status: **DRAFT v2 — grounded in a prior-art survey (§3, sources in Appendix A) and
revised after an adversarial grounding audit
([research/piece-composition-grounding-audit.md](research/piece-composition-grounding-audit.md);
counter-evidence and divergences in Appendix B). No implementation yet.**
v1→v2: the novelty claim was narrowed (BOSL2's screws.scad, SolidWorks Hole
Wizard/TolAnalyst, and Gridfinity all ship fit contracts — what's novel is
contract-on-the-general-port + connect-time compile failure), the no-CSG rationale was
rewritten (Manifold is now OpenSCAD's battle-tested default; our reason is the 2D layer
and semantic labels, not boolean fragility), the fit ladder is labeled as one
calibrated-printer source with mainstream guidance 2–10× looser, the §4.1 radial grub
hole was routed to §8 forcing-op territory, `connect` gained a cycle rule, and lamp
safety gained a wattage cap, air gap, and geometry-not-grip retention.
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
   ("pin ⌀3.0 + snug clearance exceeds socket ⌀3.1"), not failed prints. Dimensional fit
   contracts are not new in themselves — ISO 286 limits-and-fits is a century-old
   contract language; SolidWorks' Hole Wizard carries H7/g6-style fit classes on features
   and TolAnalyst validates stack-ups across assemblies; and BOSL2's own screws.scad
   ships thread tolerance classes ("6g"/"2A"), named clearance-hole fits
   ("close"/"normal"/"loose"), and a separate `$slop` printer-compensation knob. What no
   surveyed system does is attach the contract to the *general mating interface itself*
   and make the *connect operation* fail compilation on kind/dimension/fit mismatch:
   BOSL2's `attach()` aligns frames but knows nothing about the screw library's
   tolerances two files away; commercial mate connectors are frames without dimensions.
   The novelty is that narrower composition — contract-on-port plus connect-time
   validation for arbitrary printed interfaces (Appendix B.1).
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
  port mount rim top ring 46                # explicit port on the top rim
  port socket bore axis                     # the bore itself, as an axis port
  # (v1 sketched `hole grub radial 3.2` here — removed: a radial hole through a
  #  revolved wall is not a z-band hole; see §4.2 and Appendix B.4)

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

**Expressiveness boundary, stated up front**: radial holes through revolved walls are
*not* z-band holes — a side hole's boundary is a 3D intersection curve, which is §8
forcing-op (1) (a hole through a curved shell). They are rejected until C4, or
implemented as a dedicated θ-z wall-parameterization subtraction if C3 needs a
set-screw. This is a real limitation relative to every surveyed system — side/angled
subtraction is table stakes elsewhere (BOSL2's `diff() + attach(RIGHT, inside=true)` is
a tutorial one-liner; B-rep CADs put hole features on any face) — so it is stated here
rather than discovered in week one (Appendix B.4).

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

**Cycle rule**: the connect graph must be a tree over *pieces*: the first `connect`
reaching a piece derives its placement; any additional `connect` between two
already-placed pieces derives no transform and instead becomes a **closure check** — the
two port frames must already coincide within tolerance, else compile error. "One
connection per port" alone does not prevent cycles, because cycles use different ports of
the same piece (a 2×2 pinned tile grid is the canonical case, and the tile-wall sibling
doc guarantees users hit it in C2/C3). This is the deterministic analog of Onshape's
"mate over-defines assembly" error, which loop-closing mates trigger there
(Appendix B.3).

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
stays a knob because socket bodies vary. Tightened after the audit (Appendix B.5):

- **Wattage cap and air gap.** LED bulb heatsinks measure 60–100 °C and sealed-base
  drivers ~86 °C, while PETG's continuous service limit is ~70 °C (HDT 65–75 °C, Tg
  ~80 °C) — the margin near a compact LED's neck in an enclosed pendant can be zero or
  negative. Examples cap bulb wattage and require an explicit air gap around the bulb
  base/heatsink; the hottest zone is the base/neck, exactly where the collar sits.
- **Geometry, not grip.** The collar holds the socket by shoulder/detent geometry, never
  by sustained elastic grip — PETG creeps under constant stress well below Tg, and the
  socket zone is warm.
- **Unlisted-luminaire note.** Printed PLA/PETG carries no UL 94 flammability rating and
  the assembled fixture is an unlisted luminaire; the socket and cord set must be listed
  components.

## 5. Fit, clearance, and the 2D layer

- The fit model separates **intent gap** (press −0.10 / snug +0.05 / sliding +0.15 /
  free +0.35 mm diametral) from **printer compensation** (FDM holes print 0.1–0.3 mm
  undersize while external dims run ~0.1 mm oversize; PETG's tacky surface eats another
  ~0.05 mm of running clearance). This *generalizes a separation that today exists only
  inside thread/screw generators* — BOSL2's screws.scad separates exactly these two
  things (tolerance class vs `$slop`) — to every port kind. The `.bkr` stores intent; a
  `printer profile` (hole compensation, xy compensation, material) is applied at compile
  time — Multiboard-style user-adjustable tolerance, not baked-in numbers.
- **Where the ladder numbers come from (and their honest status).** These defaults
  transcribe one calibrated-printer source (Creative3DP's press-fit ladder) and assume
  hole compensation is applied separately by the printer profile. Mainstream guidance
  quotes much larger raw clearances — Hubs recommends 0.5 mm nominal for FDM snap-fits,
  and general tolerance guides give 0.4–0.6 mm for uncompensated FDM mating parts —
  precisely because they fold hole undersize, XY error, and material variation into one
  number. Our small intent gaps are only valid downstream of a measured printer profile;
  the C2 fit coupon is therefore not optional polish but the mechanism that makes this
  table honest (Appendix B.2). Note also the sign convention: our "press −0.10" is
  designed *interference*; several guides' "press fit 0.1 mm" is per-side *clearance*.
  Both intent and compensation are **calibration targets for the `/prototype` catalog**:
  a fit-coupon entry (pin/socket step gauge) lands with C2 and its measured results
  update the profile, propagating to every assembly at once.
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
already-3D solids (angled hole through a curved shell — including §4.2's rejected radial
holes), (2) union of overlapping extrusions from different planes, (3) chamfer/fillet
across a 3D seam, (4) shell/offset of a composed result.

**Why keep a constructive core at all?** The mainstream position is now the opposite of
ours: OpenSCAD made Manifold its default backend in August 2025 "after a long time of
battle testing" (openscad mailing list; the *stable* 2021.01 release still ships
CGAL-default), booleans there are 5–30× faster than fast-csg (openscad/openscad#4533),
and Manifold's output is guaranteed manifold by construction — so "avoid 3D CSG for
robustness/performance" is no longer a defensible reason, and we do not claim it
(Appendix B.6). We keep the constructive core for two
reasons that survive Manifold's maturity: the print-validation gate needs a robust
per-layer 2D region algebra regardless, so 2D-first geometry is paid for twice over; and
stitched meshes retain semantic labels (which face belongs to which strut, band, or
port) that a boolean result erases and our contract/gate tooling depends on. Manifold's
own docs concede sub-ε sliver triangles can survive and error compounds across chained
ops — acceptable for rendering, unhelpful for a pipeline whose value proposition is
meshes that pass gates by construction.

If a post-v1 feature needs a forcing op, adopt `manifold-3d` (~2.8 MB WASM, TS types,
lazy async init, guaranteed-manifold output) as an **opt-in backend the compiler selects
per-operation** — never as the default path. Bikar's welded watertight meshes are exactly
the input contract Manifold wants, so the adapter is small (~100 LOC MeshGL mapping). The
guardrail is cultural: "just boolean it" must stay a compiler decision, not an authoring
idiom.

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

The full URL-annotated research report is checked in at
[`research/code-cad-composition-survey.md`](research/code-cad-composition-survey.md)
(see its Errata section for two citation corrections found by the audit), and the
adversarial grounding audit behind the v1→v2 changes at
[`research/piece-composition-grounding-audit.md`](research/piece-composition-grounding-audit.md).
Headline sources:

- **BOSL2**: [attachments.scad](https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad),
  [attach tutorial](https://github.com/BelfrySCAD/BOSL2/wiki/Tutorial-Attachment-Attach),
  [distributors.scad](https://github.com/BelfrySCAD/BOSL2/wiki/distributors.scad),
  [**screws.scad**](https://github.com/BelfrySCAD/BOSL2/wiki/screws.scad) (thread
  tolerance classes + `$slop` — the strongest single counter-example to v1's novelty
  claim, from inside the surveyed ecosystem);
  anchoring pain: [OpenSCAD list thread](https://lists.openscad.org/empathy/thread/3U2AWJGYUBTRD3L2IPAH2QPDIU4IWH4E),
  [discussion #1315](https://github.com/BelfrySCAD/BOSL2/discussions/1315)
- **CadQuery / build123d**: [selectors](https://cadquery.readthedocs.io/en/latest/selectors.html),
  [assemblies](https://cadquery.readthedocs.io/en/latest/assy.html),
  [build123d joints](https://build123d.readthedocs.io/en/latest/joints.html),
  [juraph: Playing with build123d](https://juraph.com/kiwi/playing_with_build123d/)
  (the source of the assembly-pain quotes; v1 misattributed them to
  [HN 41548945](https://news.ycombinator.com/item?id=41548945), kept as secondary
  discussion)
- **Commercial mates + fit contracts**: [OnShape mates + mate connectors](https://cad.onshape.com/help/Content/mate.htm),
  [Onshape "mate over-defines" (cycle precedent)](https://forum.onshape.com/discussion/18037/mate-overdefines-the-assembly),
  [Fusion 360 joint types](https://help.autodesk.com/cloudhelp/ENU/Fusion-Assemble/files/GUID-8818AE31-958A-4A59-989B-9875A174C67A.htm),
  [SolidWorks Hole Wizard tolerances](https://www.javelin-tech.com/blog/2018/11/solidworks-hole-wizard-tolerances/),
  [SolidWorks TolAnalyst](https://help.solidworks.com/2025/english/solidworks/sldworks/c_TolAnalyst_Overview.htm),
  [Gridfinity specification](https://github.com/gridfinity-unofficial/specification/blob/main/README.md)
  (ecosystem-level connector tolerance: 0.25 mm/side)
- **Manifold**: [repo](https://github.com/elalish/manifold),
  [algorithm wiki](https://github.com/elalish/manifold/wiki/Manifold-Library),
  ["5–30x speedups" (openscad/openscad PR #4533)](https://github.com/openscad/openscad/pull/4533)
  (v1 misattributed this to discussion #387, which holds an independent
  [11× user report](https://github.com/elalish/manifold/discussions/387)),
  [OpenSCAD default-backend announcement, Aug 2025](https://lists.openscad.org/empathy/thread/TMJEJCZINIJNYJX2YF7IDNBAPQY66KIF)
  (dev snapshots; stable 2021.01 still ships CGAL-default),
  [bundling friction (#1343)](https://github.com/elalish/manifold/issues/1343),
  [three.js round-trip](https://manifoldcad.org/three)
- **2D booleans**: [Clipper2](https://github.com/AngusJohnson/Clipper2),
  [Clipper2-WASM](https://github.com/ErikSom/Clipper2-WASM)
- **Grammar / joints / export**: [CGA shape grammar](https://doc.arcgis.com/en/cityengine/latest/tutorials/tutorial-6-basic-shape-grammar.htm),
  [Tsugite, UIST 2020](https://dl.acm.org/doi/10.1145/3379337.3415899),
  [3MF core spec](https://github.com/3MFConsortium/spec_core/blob/master/3MF%20Core%20Specification.md),
  [three-mf](https://github.com/watzon/three-mf),
  [KCL patternTransform](https://zoo.dev/docs/kcl-std/functions/std-solid-patternTransform)
- **Printed-fit clearances**: the §4.3 ladder transcribes the
  [Creative3DP press-fit ladder](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/)
  (see [`research/tile-craft-field-survey.md`](research/tile-craft-field-survey.md) §7)
  plus the [Qidi guide](https://qidi3d.com/blogs/print-lab/3d-printed-snap-fit-joints-clearance-guide);
  **counter-position**: the
  [Hubs snap-fit guide](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/)
  recommends 0.5 mm nominal FDM clearance — 3–10× the ladder's snug/sliding gaps —
  because it assumes no printer compensation (v1 mis-grouped it as supporting the
  ladder; see §5 and Appendix B.2)
- **Lamp thermals** (added in v2):
  [LED bulb heatsink temperatures](https://www.electronicshub.org/led-bulbs-get-hot/),
  [PETG temperature limits](https://www.wevolver.com/article/petg-temperature-resistance-heat-limits-and-practical-insights-for-engineers),
  [PLA-vs-LED shade test](https://3dwithus.com/3d-printed-lamp-shades-ideas-led-vs-incandescent-bulbs)

## Appendix B — counter-evidence and divergences

Each entry records the strongest counter-position found by the grounding audit
([`research/piece-composition-grounding-audit.md`](research/piece-composition-grounding-audit.md)),
with either our justification for diverging or the design change it forced.

Entries tagged `[CAL-…]` are **empirical** bets that no source can close — only a
measurement can. The id is the bet's entry in the registry
([`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md)), which
names the coupon that settles it; the ceremony is the `calibrate` skill (bikar
Tenet 30 — a physical constant is not earned until it records its provenance).

### B.1 The novelty claim was overbroad — narrowed

v1 claimed "no surveyed system ships dimensional contracts on connectors." False as
written: BOSL2's screws.scad ships ISO/ASME thread tolerance classes plus named
clearance-hole fits plus a separate `$slop` printer knob — the exact intent/compensation
separation §5 claimed nobody had; SolidWorks carries H7/g6 fit classes on features and
TolAnalyst validates assembly stack-ups; Gridfinity and Multiboard publish ecosystem
connector tolerances; ISO 286 is a century-old fit-contract language. What survives, and
what §1 goal 2 now says: no surveyed system attaches the contract to the *general mating
port itself* and makes *connect* fail compilation on mismatch. The claim changed from
"nobody does fit contracts" to "nobody composes contract-on-port with connect-time
validation."

### B.2 The fit ladder is single-sourced and mainstream guidance disagrees [CAL-FIT-01 — the same bet as c2-assembly B.3; one coupon (MC-1) closes both]

The −0.10/+0.05/+0.15/+0.35 ladder transcribes one calibrated-printer source
(Creative3DP). Hubs recommends 0.5 mm FDM clearance; general guides give 0.4–0.6 mm for
uncompensated parts. Reconciliation: the ladder's numbers are *designed gaps after hole
compensation on a calibrated printer*; the looser school quotes *raw nominal clearances*.
We keep the ladder because bikar applies compensation separately (that is the
architecture), label its provenance honestly in §5, cite Hubs as the counter-position,
and make the C2 fit coupon the arbiter. Sign convention noted: our press is
interference; some guides' "press" is clearance.

### B.3 Deterministic pairwise connect does not escape over-definition

Onshape's one-mate-per-connection model still throws "mate over-defines assembly" when
mates close a loop; closed chains fundamentally cannot be expressed as a pure tree of
pairwise placements. v1's only rule (one connection per port) did not prevent this —
cycles use different ports of the same piece. The design changed: §4.4 now requires the
connect graph to be a tree over pieces, with loop-closing connects downgraded to
closure *checks* that must pass within tolerance.

### B.4 The z-band hole model cannot express v1's own flagship example

§4.1 sketched `hole grub radial 3.2` on a revolved collar, but a radial hole through a
curved wall is §8 forcing-op (1) — unbuildable before C4. Competing systems treat
side/angled subtraction as table stakes (BOSL2 tutorial one-liner; B-rep hole features
on any face). The design changed: the grub hole left the sketch, §4.2 states the
expressiveness boundary explicitly, and radial holes are rejected until C4 (or a
dedicated θ-z wall-parameterization subtraction if C3 needs a set-screw).

### B.5 "PETG near socket" can have zero thermal margin

LED-only remains well grounded (incandescent deformed a PLA shade in 2–3 h in empirical
tests; LED stayed safe). But LED heatsinks run 60–100 °C and sealed-base drivers ~86 °C
— at PETG's ~70 °C continuous ceiling, a compact high-wattage LED in an enclosed pendant
can eat the whole margin, and the hottest zone (base/neck) is where the collar sits.
The design changed: §4.5 adds a wattage cap, a required air gap around base/heatsink,
geometry-not-grip retention (PETG creeps below Tg), and the unlisted-luminaire/UL 94
note. No source argued a passive printed holder around a listed socket is per-se unsafe;
the holder-not-socket division stands.

### B.6 The no-CSG core — the *rationale* changed, the bet stands

The steelman: adopt manifold-3d everywhere from day one. OpenSCAD — the flagship
code-CAD system whose whole paradigm is 3D booleans — made Manifold its default backend
in August 2025 after "a long time of battle testing"; booleans there run 5–30× faster
than fast-csg; output is guaranteed manifold by construction. The two classic
justifications for avoiding mesh CSG (slow, fragile) are gone in 2026, and v1's framing
leaned on them. We diverge anyway, on grounds the steelman does not rebut: the
print-validation gate needs a per-layer 2D region algebra regardless (2D-first is paid
for twice over), and stitched meshes retain the semantic labels our contract/gate
tooling depends on, which boolean output erases. Full reasoning in §8; the concession is
that §8 now names manifold-3d the committed backend for all four forcing ops rather than
treating booleans as inherently suspect.
