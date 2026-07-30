# Hemisphere-split STL export (task #11) — implementation design doc

Status: **v2 — grounded in a read-only audit of the bikar tree, a prior-art survey, and direct
measurement of the shipped engine
([`research/hemisphere-split-survey.md`](research/hemisphere-split-survey.md), sources in
Appendix A); revised after an adversarial grounding audit
([`research/hemisphere-split-grounding-audit.md`](research/hemisphere-split-grounding-audit.md)),
whose findings rewrote most of v1's numbers. Counter-evidence and divergences in Appendix B.**

Scope: the decision deferred twice by [`orb-lab-design.md`](orb-lab-design.md) — in its non-goals
(`:34`, "hemisphere-split FDM export (task #11, separate decision)") and in its print-target
section (`:344`, "would relax the Z term for tall-bed machines").

**Recommendation up front: do not build the split in the engine.** The cheapest fix for the only
benefit that survives measurement is not a split at all — it is **rotating the orb onto a face axis**
(§9.1 Option A0), which is free, is one click, and clears the print gate's bed-contact warning
outright. Where more bed contact than that is genuinely wanted, document the slicer's own cut tool
(Option C). The split is fully specified below (§4–§8) so that it *can* be built, because the
go/no-go is not this document's to close — prototype **P3** owns it
([`.claude/skills/prototype/catalog.md`](../.claude/skills/prototype/catalog.md)). But the evidence
moves the prior a long way toward "don't", and §9.2 states what P3 would have to show to flip it.

---

## 1. Goals

1. **Settle the geometry**: where the split plane goes relative to the pattern — through voids or
   through struts — and what happens to what it crosses.
2. **Settle the mesh contract**: how two halves satisfy a gate that asserts watertightness
   unconditionally, in a codebase with no exemption mechanism and an explicit statement that none
   is being added.
3. **Settle registration**: whether the halves get alignment features, and whether the C2
   `port`/`rod` layer can carry them.
4. **Settle the surface**: DSL opt-in and CLI shape, following the `--format parts` precedent.
5. **State the rationale honestly** — including the two thirds of it that do not survive contact
   with the machine table (§1.1) and the engine's own print gate (§3.3).

Non-goals: print-orientation control (V3 per `print-gate.ts:502-507`), general mesh booleans,
non-planar or multi-piece splits as a shipped feature, and cut planes anywhere other than a
symmetry plane.

### 1.1 The size rationale does not survive the machine table

The shipped ceiling is `packages/knobs/src/machines.ts:91-93`, with `BUILD_MARGIN_MM = 10` at `:84`:

```ts
export function radiusCeilingMm(target: PrintTarget): number {
  return Math.floor((Math.min(target.xMm, target.yMm, target.zMm) - BUILD_MARGIN_MM) / 2);
}
```

`orb-lab-design.md:337-347` describes this as `2R ≤ min(X, Y, Z) − 10 mm` (equivalent modulo the
integer floor) and says the split "would relax the Z term for tall-bed machines". The first clause
is true; **the second is backwards** — relaxing the Z term can only help a machine whose Z is
*binding*, which is a **short**-Z machine, not a tall-bed one.

And relaxing it buys nothing on the shipped presets, because a hemisphere printed cut-face-down
still occupies **2R in X and Y** — only its height falls to R:

```
whole:  2R ≤ min(X, Y, Z) − 10
split:  2R ≤ min(X, Y) − 10    and    R ≤ Z − 10
```

These differ only where `Z < min(X, Y)`. Against the presets dimensioned at `machines.ts:21-81`:

| Machine | Build volume | Whole-sphere R max | Split R max | Gain |
|---|---|---|---|---|
| Bambu X1C / P1S | 256³ | 123 mm | 123 mm | **0** |
| Bambu A1 | 256³ | 123 mm | 123 mm | **0** |
| Bambu A1 mini | 180³ | 85 mm | 85 mm | **0** |
| Prusa MK4S | 250×210×220 | 100 mm | 100 mm | **0** |
| Prusa Core One | 250×220×270 | 105 mm | 105 mm | **0** |
| Ender 3 | 220×220×250 | 105 mm | 105 mm | **0** |
| SLS service | 300³ | 145 mm | 145 mm | **0** |
| MJF service | 380×284×380 | 137 mm | 137 mm | **0** |

Every one of the **nine** shipped presets (the eight above plus **Custom**) has `Z ≥ min(X, Y)`, so
`min(X, Y, Z) = min(X, Y)` and the XY term binds identically either way. The `radius` parameter's
own maximum is 110 mm (⌀220), which already fits whole on a 256³ bed.

**The one real exception is the Custom entry, and it is a supported input, not a hypothetical.**
`machines.ts:80` ships `{ id: 'custom', … }` and `packages/lab/src/main.ts:710-716` accepts any
user-typed X/Y/Z ≥ 50 mm. A user entering 300 × 300 × 60 gets a whole-sphere ceiling of
`floor((60−10)/2) = 25 mm` — below the `radius` parameter's own 40 mm floor, so the orb is
unbuildable whole — against a split ceiling of `min(145, 50) = 50 mm`. So the size benefit is real,
but reachable **only** on a short-Z machine the user must type in by hand. No offered preset gets
it.

**`orb-lab-design.md:344` should be corrected** — as written it invites the reader to infer a size
benefit that no offered machine can realise, and attributes it to the wrong class of machine.
Tracked in §10 Q1.

## 2. Engine ground truth

Read from the bikar tree, not inferred; line numbers preserved in
[`research/hemisphere-split-survey.md`](research/hemisphere-split-survey.md) §0 and re-verified
against `origin/main` during the grounding audit.

**The mesh and its watertightness test.** `OrbMesh` is indexed triangles `{vertices, triangles,
stats}` (`kernel3d/solidify-lattice.ts:31-35`). `meshStats` (`:115-148`) builds a directed-edge map
and sets `watertight = bad === 0 && volume > 0`, where `bad` counts any directed edge whose
reversed twin does not occur exactly once (`:130-135`, `:146`). **This is exactly a closed
*edge*-manifold test.** An open boundary edge has no twin, so every rim edge of an uncapped half is
`bad`: an uncapped half fails by construction, not by oversight. Note the limit — it is blind to
pinch *vertices* (two shells meeting at a single point have no bad edge), the same blind spot
`print-gate.ts:141-145` documents for `countComponents`. §5.1 returns to this.

**The gate.** `meshGate` (`kernel3d/mesh-gate.ts:82`) asserts three things — watertight (`:90-92`),
zero degenerate triangles below `DEGENERATE_AREA_MM2 = 1e-6` (`:93-95`, `:52`), declared min feature
≥ 1.2 mm floor (`:96-101`, bet `CAL-FEA-01` at `:13`). **Euler is reported but deliberately not
gated** (`:76-80`): "its expected value is family-specific (2 − 2g for a pierced shell, 0 for woven
tubes)". §5.2 shows this was the right call and that a stricter gate would have been wrong.

**There is no exemption mechanism.** No pragma, no DSL statement, no CLI flag. `MeshGateOptions`
exposes only `minFeatureMm` (`:25-28`) and the CLI never passes it (`cli/src/index.ts:207`,
`:459`). The W2 sub-floor clip "exemption" is enforced socially — the pattern header tells you to
omit `--check` for that `--piece` (`patterns/Coupons/Clip-Coupon.bkr:8-20`), and
`patterns/Coupons/Machine-Card.bkr:34` states outright that no exemption flag exists **and none is
being added**. This settles §5 before any design work: a split producing open halves would need the
one mechanism the house has explicitly refused to build.

**The primitives a split needs — present, but not reachable.** `kernel3d/slice.ts` already cuts
triangles against a z-plane: `crossingPoint(a,b,z)` (`:128`), `triangleCut(tri,verts,z)` (`:139`),
`chainLoops(segments)` (`:170`), `nestLoops` (`:221`), `orient` (`:267`), with the correct tie rule
already in place — "a vertex exactly at z counts as not-below, consistently for every triangle
sharing it — that is what keeps the loops closed" (`:133-137`).
`kernel3d/earcut-vendored.ts` (`:67`) is the planar triangulator, already used for piece caps.

Two qualifications that v1 of this doc got wrong, both material to the build estimate:

- **All five slice helpers are module-private on `origin/main`.** Only `sliceAt`, `sliceMesh`,
  `signedArea`, `ringBounds` and `pointInRing` are exported. A `kernel3d/split.ts` that reuses them
  cannot simply import them; `slice.ts`'s export surface has to change first. That is a real cost
  §9.1 must price, not a free lunch.
- **`slice.ts` returns 2D `SliceRegion[]` and never re-emits a triangle.** The missing work is
  triangle re-emission and cap triangulation, not "two of three primitives".

There is no plane clip, half-space, CSG or boolean on an `OrbMesh` anywhere, and `packages/core` has
zero runtime dependencies.

**Emission and CLI.** `emitBinarySTL` (`render/mesh-emitter.ts:17`) is one mesh → one buffer.
`--format parts` (`cli/src/index.ts:303-333`) is the multi-file precedent and a good one: `-o
<directory>` required (`:317-321`), **DSL opt-in required** (`export parts`, else an error at
`:313-316`; rationale `:299-301` — "the declaration is the printable-unit contract, not a CLI
convenience"), all parts gated before any is written (`:204-220`), files named
`<Assembly>-<Piece>.stl` (`:326`). Nothing is written when a gate fails (`:475`).

**Orb facts.** All 11 shipped orbs default to `radius 60` (⌀120), `strut_width 3`, `strut_depth
2.4`; radius range `40..110`. `strut_width` and `strut_depth` are themselves parameters with ranges
`1.5..6` and `1.2..4` (`patterns/Orbs/Star-Orb.bkr:11-12`), expressed in **absolute millimetres** —
`solidifyLattice` converts strut width into pattern space via `unitMm` (`:208-209`) precisely so the
printed strut is the authored mm at any radius. Declared min feature is
`min(strutWidth, strutDepth)` = 2.4 mm (`cli/src/index.ts:457`). Thickness is applied **radially**
in both projections (`:224-235`). Symmetry axes already exist — `symmetryViewAxes(base)`
(`kernel3d/orb-views.ts:39-48`) returns three deterministic axes (`vertex-N`, `face-N`, `edge-2`),
which is where a split plane's normal should come from rather than being invented. An `orb` has no
`ports` and no `holes` field (`dsl/ast.ts:140-156`).

**Which axis is "up" in the authored mesh.** `icosahedron()` (`polyhedra.ts:122-160`) puts vertices
4 = (0,−1,t) and 5 = (0,1,t) at maximum z, and they share an edge (faces `[4,9,5]`, `[5,11,4]`).
**The authored +z axis is therefore an `edge-2` axis**, not a vertex or face axis. Every number
measured "as shipped" is a measurement of the `edge-2` plane. This is easy to miss and it invalidated
several of v1's comparisons.

## 3. What the survey and the engine established

### 3.1 The slicers already ship this, in depth

PrusaSlicer, OrcaSlicer and Bambu Studio all ship an interactive cut tool with **Planar and
Dovetail** modes and **Plug / Dowel / Snap** connectors, in Prism or Frustum style with Triangle /
Square / Hexagon / Circle cross-sections, a tolerance slider, and a post-cut placement option
literally named **"Place on cut"** — which *is* the "print the flat face down" step this feature
exists to achieve. Read from source: PrusaSlicer and OrcaSlicer carry byte-identical defaults
`m_connector_size = 2.5`, `m_connector_depth_ratio = 3.0`, `m_connector_size_tolerance = 0.0`,
`m_snap_bulge_proportion = 0.15` (`GLGizmoCut.hpp`, both projects). Bambu names support reduction
as the motivation outright.

This is the steelman for not building, and it is strong: the capability is free, interactive,
previewable, undoable, and already installed on every target machine's toolchain.

Two cracks in it, both real:

- **The connector defaults are unusable on this geometry.** A 2.5 mm connector centred in a 3 mm
  strut leaves 0.25 mm of wall per side — below one 0.4 mm extrusion.
- **The default size tolerance is 0.0 mm** — nominal-to-nominal, no designed clearance, which is
  the likely root of recurring "the dowels don't fit" reports.

A third crack claimed in v1 — that the gizmo's `is_outside_of_cut_contour` /
`is_conflict_for_connector` guards "will fight a cross-section made of dozens of ~7 mm² disjoint
islands" — **is plane-conditional and was measured on the wrong plane**. See §3.5: the cut
cross-section is 16 regions on `edge-2`, 12 on `face-3`, and **a single continuous annulus** on
`vertex-5`. On `vertex-5` there are no islands for the guards to fight.

Neither surviving crack argues for engine-side splitting. Both argue that *whichever* path is taken,
the connectors must be sized by us, not by the slicer's defaults.

### 3.2 A cell-following seam is unsettled — the design goes planar because planar is cheap

The design's most attractive idea — route the seam around the void cells so no strut is severed —
has an obvious objection: **a wandering seam does not lie in a plane, so the hemisphere cannot rest
cut-face-down**, and the flat face on the bed is the entire benefit of splitting.

**This objection is not established, and v1 of this doc overstated it.** The survey's own §8 item 4
records the honest state: "This may be a fatal objection to the design's headline idea, **or may be
resolvable with a small planar flat at the rim** — no source helps." No new evidence was found, so
the ruling is withdrawn. The steelman stands unrefuted: only one half's contact surface needs to be
planar; a raft absorbs a few millimetres of non-planarity routinely; and a hybrid "planar rim +
cell-following interior" gives up nothing.

The academic record supports the *instinct* and declines the *method*. Chopper (Luo, Baran,
Rusinkiewicz & Matusik, SIGGRAPH Asia 2012) names "**Aesthetics**: seams should be unobtrusive …
and should follow the natural symmetries of the model" as a first-class objective — the intuition
has a name. But Chopper searches a **BSP tree of planar cuts** and says why: finding assemblable
cuts is hard "since these cuts may have to be **non-planar**" and is "impractical to do every time
we evaluate a covering's quality". The canonical paper considered non-planar cuts and declined them
on tractability, not on plateability.

There is a structural sting in the tail: a void-following seam severs *zero* struts, so it has
*zero* butt-glue area and must rely entirely on interlocking geometry along a non-planar seam.

**But the aesthetic/bonding tension v1 asserted here is itself an artifact of the wrong plane.** On
`vertex-5` the planar cut already runs along a solid great-circle band of the pattern (§3.5), so
"follow the natural symmetries" and "lie in a plane" are not in conflict on this geometry at all.

**Conclusion: the split plane is planar and cuts through struts** — chosen because planar is
sufficient, cheap, and gives the largest bond area, *not* because the alternative is ruled out. The
question "voids vs struts" resolves to *struts*, and the non-planar option moves to Appendix B as an
open question.

### 3.3 Pin-in-strut registration fails at the default strut, by a factor of four

Hydra Research's design rules give minimum printable hole ⌀ **> 2 mm** and minimum structural wall
**0.9 mm** (2× extrusion width). A socket in a severed strut's butt face is bounded by the
**smaller** of the strut's two dimensions — and at the shipped defaults that is the 2.4 mm *depth*,
not the 3 mm width:

```
socket ceiling = min(strut_width, strut_depth) − 2 × 0.9 mm
               = min(3, 2.4) − 1.8 = 0.6 mm      ← a quarter of the 2 mm minimum printable hole
```

v1 of this doc computed `3 − 2(0.9) = 1.2 mm` off the non-binding dimension. The corrected figure is
**0.6 mm**, which makes the conclusion twice as strong.

**But the conclusion is not universal, and v1 asserted it as if it were.** `strut_depth` ranges
`1.2..4` mm and is absolute, not radius-scaled (§2). The socket ceiling stays below 2 mm until
`struts depth` reaches **3.8 mm** — the top ~5 % of the shipped range, where the shell is no longer
a lattice in any visual sense. So: *at the default and across almost all of the shipped parameter
space, no pin diameter fits a strut with printable walls.* That is the honest claim.

Registration, if it happens, must be carried by geometry that **spans multiple struts** — a lip or
rabbet running along the seam — not by a pin in a strut. And a lip wide enough to matter is a new
solid feature on the equator, which changes the object's appearance at exactly the place the design
was trying to keep unobtrusive.

### 3.4 A glued seam's strength depends almost entirely on which plane you cut

The best-controlled measurement found: CA-glued FFF joints at **2.46 ± 1.00 MPa** tensile and
5.16 ± 1.41 MPa flexural, versus a printed wedged mortise–tenon joint at **5.16 ± 0.66 MPa** and
8.13 ± 0.37 MPa (Shen, Zhang & Qin, *Prog. Addit. Manuf.* 11:4025–4041, 2026, open access).
Against Prusament PLA's own TDS — printed tensile yield **51 ± 3 MPa**, interlayer adhesion
**17 ± 3 MPa** — a CA seam is roughly **5 % of the printed material's strength and ~15 % of its
weakest direction**, and it fails abruptly.

Loctite's *Design Guide for Bonding Plastics* (v6) contradicts this for ABS, reporting bonds
"stronger than the ABS substrate", and supplies its own reconciliation: "Because of the large joint
overlap, the substrate will fail before the bond." **The variable is bond area, not chemistry.**
Loctite's rules: maximise shear, minimise peel and cleavage; and "as a general rule, increase the
joint **width** rather than the overlap area ('wider is better')".

**v1 concluded from this that the cut yields "a ring of butt faces of 3 × 2.4 = 7.2 mm² each — the
worst geometry in Loctite's taxonomy". That is wrong on every plane** (§3.5). Measured:

| plane | cut cross-section | regions | mean face | Loctite verdict |
|---|---|---|---|---|
| `vertex-5` | **898.2 mm²** | **1 continuous annulus** | — | one ~377 × 2.4 mm lap band — the **best** geometry in the taxonomy ("wider is better") |
| `face-3` | 175.5 mm² | 12 | 14.6 mm² | small disjoint butt faces — the worst |
| `edge-2` | 491.1 mm² | 16 | 30.7 mm² | middling |

The relative-strength framing also never computed the absolute adequacy, which is what actually
decides the question. At 898 mm² and Shen et al.'s 2.46 MPa, the `vertex-5` seam carries roughly
**2.2 kN in pure tension** against an orb that weighs ~57 g. Whatever fails first when this object
is handled, on that plane it is not the seam.

Also counter-intuitive and worth carrying forward: Loctite's bondline table shows a **thicker glue
line lowers peak stress concentration** (0.001″ → 18.40 stress ratio; 0.040″ → 3.06). A
zero-clearance butt face pressed metal-tight is the worst case, and CA's "limited gap cure" pulls
against it — epoxy suits a deliberately gapped seam better.

Note the gap in the record: the Loctite guide has sections for ABS, ASA, PMMA, acetal and nylon and
**none for PLA or PETG**. Every PLA adhesive number here is academic or community, not manufacturer.

### 3.5 The measured scorecard — what splitting actually buys

Run against the shipped engine (`npx tsx packages/cli/src/index.ts render patterns/Orbs/Star-Orb.bkr
--format stl --check print`, 2026-07-30):

```
mesh gate: watertight=true euler=-396 degenerate=0 minFeature=2.4mm (floor 1.2mm) — PASS
print gate: layers=612 @ 0.2mm bodies=1 islands=0/20 bed=7.9mm² warn=7 — PASS
  warn F7: first-layer contact is 7.86mm² (1.21% of the widest layer's 650.4mm²)
           — below 25mm² or 1%; add a brim or raft, or flatten the contact face
  warn F3: ×6 material starts in mid-air … supports required over that span
           (z = −48.3, −43.1, −21.5, +8.1, +13.1, +41.7 mm)
```

**Read `islands=0/20` correctly**: `cli/src/index.ts:281-286` prints
`islands=${orphanIslands}/${supportedIslands}`, so that is *zero orphan islands and twenty supported
islands* — **not** a first-layer region count. The report contains no first-layer region count at
all. Measured directly, the first layer (z = −61.1) is **1** region of 7.86 mm². v1 of this doc
misread this line and every "~20 severed struts / ~144 mm² of butt area" figure derived from it was
invented.

**And this run measures the `edge-2` plane**, because the authored +z axis is an edge axis (§2) —
not the `face-N` plane v1 went on to recommend. Measured on all three symmetry planes:

| | `vertex-5` | `face-3` | `edge-2` (as authored) |
|---|---|---|---|
| Cut cross-section at the plane | **898.2 mm²** | 175.5 mm² | 491.1 mm² |
| Regions (cap components *k*) | **1** | 12 | 16 |
| Cap boundary loops *b* | 2 (annulus) | 12 | 16 |
| Whole orb resting on that pole: bed contact | 3.90 mm² (0.43 %) | **30.17 mm² (5.02 %)** | 7.86 mm² (1.21 %) |
| Whole orb resting on that pole: F3 warns | 3 | **4** | 6 |
| Whole orb resting on that pole: F7 warn | yes | **none** | yes |
| Split gain in first-layer area vs. that same pole-down orientation | **230×** | 5.8× | 62.5× |

The `vertex-5` cut face is a **single continuous solid annulus** (1 region, 1 hole; outer radius
60.9–61.2 mm, inner 58.5–58.8 mm), stable under plane displacement to **|z| ≤ 1.75 mm** before it
fragments — 10 regions at 1.8 mm, 30 at 2.0 mm. Compared against a full uninterrupted shell annulus
at the same mean radii (898.9 mm²), the measured 898.2 mm² is **gapless to 0.1 %**.

| Claimed benefit | Verdict | Evidence |
|---|---|---|
| Print a **bigger** orb | **Zero gain on every preset** | §1.1 — the XY term binds identically. Non-zero only on a hand-typed short-Z Custom machine |
| Better **bed adhesion** | **Real, but not unique to splitting** | 5.8×–230× depending on plane. But simply *reorienting* the whole orb onto its face axis already gives 30.17 mm² and clears F7 with no split at all (§9.1 A0) |
| Fewer **supports** | **Exactly neutral** | Proven by symmetry, below |

**Supports: neutral, and here is why.** v1 justified this with the survey's finding that the top
29.3 % of a hemisphere's surface sits below the 45° threshold. That is an **overhang-angle**
statistic being used to explain **island** findings (F3 = regions born mid-air with no overlap below,
`print-gate.ts:347-395`), and F4 (overhang) is not implemented at all
(`PrintFindingCode = 'F1'|'F2'|'F3'|'F7'`, `print-gate.ts:24-33`). The engine cannot currently see
the quantity that argument cites.

The correct argument is measured: the Star-Orb mesh is **mirror-symmetric about the authored z = 0**
— 1034 vertices above, 1034 below, 56 exactly on the plane, with the layer-area profile symmetric to
0.1 mm² at every sampled height. So the flipped bottom half is geometrically identical to the top
half; for the top half printed cut-face-down every layer above the cut is bit-identical to the whole
orb's, and its first layer is grounded either way. Its island set is unchanged:
`{+8.1 ×4, +13.1 ×4, +41.7 ×2}` = 10 islands, 3 F3 lines. Two halves give **10 + 10 = 20 islands and
3 + 3 = 6 F3 lines**, against the whole orb's 20 islands / 6 F3 lines. Exactly neutral, measured, not
inferred.

A bonus cross-check worth recording: `euler = −396` independently confirms the survey's derivation
that a shell with *n* pierced cells has **χ = 4 − 2n**, genus *n* − 1. Solving gives n = 200 cells
(= 10 voids × 20 faces), genus 199, and 2 − 2(199) = −396 exactly.

## 4. Where the plane goes

**Decision: a plane through the origin whose normal is one of the three axes already returned by
`symmetryViewAxes(base)`** (`kernel3d/orb-views.ts:39-48`) — `vertex-N`, `face-N`, or `edge-2` —
**defaulting to `vertex-N`.**

Rationale:

- Planar is chosen by §3.2 (sufficient and cheap; the non-planar alternative is unsettled, not
  refuted) and endorsed by Chopper's own retreat to planar BSP cuts.
- Choosing from the existing symmetry axes rather than a free vector means the seam automatically
  satisfies Chopper's aesthetics objective ("follow the natural symmetries of the model"), the
  chosen plane is already named and deterministic in the codebase, and there is no new
  axis-selection concept to design, document or validate.
- **`vertex-N`, not `face-N`.** v1 defaulted to `face-N` on the reasoning that a face-centred plane
  "is most likely to pass between pattern cells rather than clipping a star's tips". That
  prediction is correct — and it is precisely what makes `face-3` the **worst** plane for both
  benefits this doc claims. Passing between cells means severing the fewest and smallest struts,
  hence the least cap area (175.5 mm², a 5.8× bed gain) and the least glue area. `vertex-5` instead
  cuts a continuous 898.2 mm² annulus: 5.1× the bond area, one region instead of twelve, and the
  best rather than the worst geometry in Loctite's taxonomy (§3.4).

**The trade, stated honestly:** `face-N` optimises seam *invisibility*; `vertex-N` optimises seam
*strength* and *bed contact*. They are opposed, and v1 chose invisibility while claiming strength and
bed contact as the benefits. Since the two surviving arguments for splitting at all are bond area and
first-layer area, the default follows them. An author who wants the least visible seam should select
`face-N` explicitly and accept a weaker joint.

The plane passes through the origin because the orb is centred there and the mid-surface sphere is
symmetric; an offset plane is not offered (it would trade equal halves for a smaller flat face,
which is backwards). On `vertex-N` the annulus tolerates ±1.75 mm of plane displacement before
fragmenting, so origin-placement is comfortably inside the stable window.

**What it crosses is struts, and that is accepted.** On the `vertex-N` default the cut is one
continuous annulus rather than a scatter of butt faces, so §3.4's bonding objection largely
dissolves; the mitigation in §6 is glue, with a seam lip only if P3 shows alignment is hard by hand.

## 5. The mesh contract: cap the cut, keep the gate

### 5.1 Cap, do not exempt

The two halves are **capped at the cut plane**, so each is a closed solid and
`mesh.stats.watertight` is true for both. `meshGate` then passes **unchanged, with no new
options, no exemption, and no CLI flag** — which is the only design compatible with
`Machine-Card.bkr:34` ("no exemption flag exists and none is being added").

This is also the industry norm rather than a local invention: Meshmixer's Plane Cut documents
"when you cut a solid, you get a solid"; Blender's Bisect has a `Fill` option for exactly this;
trimesh's `slice_mesh_plane(..., cap=True)` will "cap the result with a triangulated polygon".

Mechanically the cap is: classify each vertex against the plane; keep triangles wholly on one side;
for straddling triangles, split at `crossingPoint` (`slice.ts:128`) and re-emit the sub-triangles;
collect the cut segments, `chainLoops` them (`:170`) into closed loops; orient and nest them
(`nestLoops:221`, `orient:267`); then `earcut` each loop set into cap triangles. **Both caps are
wound outward with respect to their own solid** — what is opposite between them is the winding
*relative to the shared rim loop*. (v1 said "wound outward for one half and inward for the other";
implemented literally that produces an inverted half and fails `volume > 0`.)

**Three implementation hazards, none fatal, all under-stated in v1:**

1. **Exact vertex coincidence is guaranteed, not incidental.** A symmetry plane through the origin
   lands on mesh vertices by construction — measured, the count of vertices with |z| < 1e-9 after
   rotating each axis to +z is **60 (`vertex-5`), 12 (`face-3`), 56 (`edge-2`)**. The tie rule at
   `slice.ts:133-137` keeps *2D loops* closed, but a triangle-re-emitting split must additionally
   avoid emitting zero-area slivers when a crossing point coincides with an existing vertex, and
   earcut is well known to emit degenerate triangles on near-collinear rings. Against
   `DEGENERATE_AREA_MM2 = 1e-6` this is the likeliest way the split fails its own gate.
2. **The helpers are private** (§2) — reusing them requires widening `slice.ts`'s export surface.
3. **`meshStats` is edge-manifold only.** A cut plane tangent to a strut yields a pinch *vertex*,
   which `bad === 0` will not catch. §5.1's thesis is "the existing gate suffices"; it suffices for
   everything except this, and validator 5 in §8 is what covers it.

### 5.2 The gate was already right about Euler, and must stay that way

The survey warns that any assertion fixing χ = 2 or genus 0 would be wrong for a pierced lattice.
bikar already avoids this: `mesh-gate.ts:76-80` reports Euler without gating it, naming the reason
("2 − 2g for a pierced shell"). The measured `euler = −396` (genus 199) confirms how far from 2 a
real orb sits. **No change is needed, and no χ assertion may be added.**

### 5.3 The invariant that actually catches split bugs

Euler characteristic is additive: χ(A ∪ B) = χ(A) + χ(B) − χ(A ∩ B). **The capped halves intersect
in the cap itself, not in the rim circles** — A = S⁺ ∪ C and B = S⁻ ∪ C, so A ∩ B = C. Therefore:

```
χ(A) + χ(B) = χ(A∪B) + χ(A∩B) = [χ(S) + χ(C)] + χ(C) = χ(orig) + 2·χ(C)
χ(C) = 2k − b        (k = cap components, b = total cap boundary loops)
```

> **χ(top) + χ(bottom) − 2(2k − b) = χ(original)**

v1 stated this as the naive `χ(top) + χ(bottom) = χ(original)`, which is the *uncapped* form — it
was carried over unchanged when §5.1 introduced capping. It is wrong on two of the three symmetry
planes:

| plane | *k* | *b* | χ(cap) | correct sum | naive form predicts |
|---|---|---|---|---|---|
| `vertex-5` | 1 | 2 | 0 | **−396** | −396 — right, but by coincidence |
| `face-3` | 12 | 12 | 12 | **−372** | −396 ✗ |
| `edge-2` | 16 | 16 | 16 | **−364** | −396 ✗ |

Sanity checks: a sphere (χ = 2) cut at the equator gives two closed spheres summing to 4; the
corrected form gives 2 + 2(2·1 − 1) = 4 ✓. A torus (χ = 0) cut into two capped spheres sums to 4;
corrected, 0 + 2(2·2 − 2) = 4 ✓.

The naive form happens to hold exactly when the cap is annular (χ(C) = 0) — which is the
`vertex-N` default. **That coincidence is the trap**: an implementation tested only on the default
plane would pass a validator that silently rejects every correct `face-N` and `edge-2` split. `k`
and `b` fall straight out of `nestLoops`/`chainLoops`, so the corrected test stays cheap and exact.

## 6. Registration — what C2 can and cannot lend

The task framing asked whether "the C2 port/rod layer already exists and could carry them". The
answer is no, for two independent reasons, and the second is fatal on its own.

**Reason 1 — geometry (§3.3).** At the default strut a socket can be at most 0.6 mm ⌀ with printable
walls, against a 2 mm minimum printable hole. No pin fits, anywhere below `struts depth 3.8`.

**Reason 2 — the assembly graph does not model this.** Four blockers, each read directly:

1. **An orb is not a placeable piece.** `evaluator.ts:716` returns the orb result *without*
   registering it, unlike `piece` (`:719`), `tile` (`:725`), `clip` (`:730`);
   `resolvePlacedPieces:2420-2426` errors on any unregistered name.
2. **A port generates no geometry.** `mintDeclaredPorts` (`:1219-1240`) yields a frame plus a
   contract and zero triangles. Pins come from a separate `rod` piece, sockets from `hole` bands. A
   port could *describe* a registration interface but never *build* it.
3. **One instance per piece** (`docs/language-reference.md:840`) — two halves of one orb cannot be
   two placements of one declaration.
4. **Assembly meshes are concatenated, never welded** (`concatMeshes` at `evaluator.ts:2485`;
   rationale `:2439-2442` — welding "would fuse coincident pin/socket faces into non-manifold
   edges"). The halves are two bodies from *one* declaration, which the assembly path does not
   model.

**What C2 *can* lend, if registration is built at all:** its *numbers* — `FIT_GAP_MM`
(`kernel3d/fit-profile.ts:27-40`, bet `CAL-FIT-01`: press −0.10, snug +0.05, sliding +0.15, free
+0.35 mm, ±0.05 window) — and its *mesh generators*, `solidifyRodPiece(d, height)`
(`solidify-piece.ts:501`) and hole z-bands. Reusing the ladder means the split inherits an
already-registered calibration bet instead of minting an unearned constant (Tenet 30).

**Therefore the design's registration answer is: none by default.** Chopper's own position is the
precedent — "Supporting glue would be strictly easier, requiring no modifications to geometry" —
and Chopper additionally notes connectors "may merely serve as guides for assembly, with glue used
to permanently attach parts". On the `vertex-N` default the annular seam is self-jigging in one
axis anyway: two matching circular rims cannot be assembled far out of true. If P3 shows alignment
is genuinely hard by hand, the escalation is a **seam lip** (a rabbet spanning multiple struts,
sized from `FIT_GAP_MM`), not pins, and it is a separate decision because it visibly changes the
equator.

## 7. CLI and DSL surface

Specified for completeness; **not recommended for build** (§9).

**DSL opt-in**, mirroring `export parts` exactly — the declaration is the printable-unit contract,
not a CLI convenience (`cli/src/index.ts:299-301`). One new optional statement on `orb`:

```bkr
orb StarOrb
  base icosahedron
  radius 60
  struts width 3 depth 2.4
  export halves            # optional; default absent
```

`export halves` takes no arguments in v1. The plane normal defaults to the `vertex-N` symmetry axis
(§4); selecting `face-N` or `edge-2` is deferred (§10 Q2).

**CLI**, mirroring `--format parts`:

```
bikar render Star-Orb.bkr --format halves -o <directory> [--check]
```

- `-o <directory>` required; error string copied in shape from `:317-321`.
- Absent `export halves` → error, matching `:313-316`.
- Files named **`<Orb>-top.stl`** and **`<Orb>-bottom.stl`**, following `<Assembly>-<Piece>.stl`.
- **Gate both halves before writing either**, following `gateAssemblyParts` (`:204-220`), so a
  failing half never leaves a usable file behind (`:468-472`).
- Each half is emitted **cut-face-down** — rotated so the cap lies on z = 0 with material above.
  This is the one place the split must diverge from `print-gate.ts:502-507` ("a part meant to print
  face-down must be modeled that way for now"): here the kernel knows the orientation, so it bakes
  it in rather than asking the author to.

## 8. Validators

All compile-time, all hard errors, in house style:

1. **Split-plane sanity** — the plane must intersect the mesh in at least one closed loop; zero
   loops means a degenerate or out-of-bounds plane.
2. **Loop closure** — every chained loop must close. `chainLoops` already drops dead-ending chains
   and expects "the caller's mesh gate" to count them (`slice.ts:167-169`); the split must instead
   **fail loudly**, naming the open chain's endpoint. A silently dropped chain is a hole in the cap
   and a fail-open gate (Tenet 29).
3. **Both halves watertight** — via the unchanged `meshGate` (§5.1).
4. **Euler additivity** — `χ(top) + χ(bottom) − 2(2k − b) === χ(original)`, with `k` and `b` taken
   from the cap's own loop nesting (§5.3). Hard error, not a warning. **The naive
   `χ(top) + χ(bottom) === χ(original)` must not be used**: it holds only for an annular cap and
   would reject every correct `face-N` and `edge-2` split — a fail-*closed* gate that rejects valid
   output, which is the exact inverse of Tenet 29 and just as wrong.
5. **Rim correspondence** — the two halves' cap boundary loops must be identical as point sets and
   opposite in orientation, so a re-weld reproduces the original. This is the assertion that the
   halves actually re-close, and it is also what catches the pinch-vertex case `meshStats` is blind
   to (§5.1 hazard 3).
6. **Non-empty halves** — neither half may be empty or contain fewer triangles than its cap.

A regression test asserting the re-welded halves reproduce the original mesh's stats
(`euler`, `volumeMm3`, `watertight`) is the single highest-value test and should exist before any
other. **It must run on at least two planes** — one annular (`vertex-N`) and one multi-component
(`face-N`) — or it will not exercise the corrected invariant in validator 4.

## 9. The verdict is empirical — this doc does not close it

### 9.1 The options

| | Option | What it costs | What it buys |
|---|---|---|---|
| **A0** | **Reorient the whole orb onto its face axis** | Nothing — one click in any slicer, no split, one file, no engine work | 30.17 mm² bed contact (5.02 %), **clears F7 outright**, and drops F3 warnings 6 → 4 |
| **A** | Build the split in the engine (§4–§8) | New kernel module, cap triangulator wiring, widening `slice.ts`'s export surface, DSL keyword, CLI format, 6 validators, orientation baking | Reproducible in the Makefile; gate-assertable; 898 mm² first layer and bond area on `vertex-N` |
| **B** | Build it *with* registration features | A + a seam lip that visibly changes the equator | Easier assembly, unproven need |
| **C** | **Document the slicer recipe** | A short section in the print docs + the `orb-lab-design.md:344` correction | The same flat-face benefit via "Place on cut", zero engine surface, zero maintenance, user keeps control of cut height and connectors |
| **D** | Do nothing | — | — |

**A0 first, C as the documented fallback.** The measured scorecard (§3.5) leaves exactly one of
three claimed benefits standing — bed adhesion — and A0 delivers enough of it to clear the gate's
own threshold for free, without splitting anything. C remains the right answer for a user who wants
substantially more bed contact than A0 gives, and the slicers deliver it interactively with a
preview. **Neither justifies a new kernel module, DSL keyword and CLI format** for a
single-file-per-print workflow.

**Two honest caveats on A0's headline.** The 25 mm² floor it clears is `CAL-BED-01`, whose own basis
text reads "**no primary source at all** … That is why F7 is warn-only: the gate is deliberately
unable to fail a part on a number it has not earned" (`print-gate.ts:47-55`). And F7 is a *warn* — the
whole orb already reports `PASS` today in its authored orientation (§3.5). "Clears the F7 floor" is
therefore a benefit measured against a threshold the house has not yet earned, and A0's real claim is
narrower: it is a 3.8× improvement in bed contact for zero cost, which is worth taking regardless of
what the threshold turns out to be.

Option C is not "nothing": the recipe must carry the numbers the slicer gets wrong for this
geometry — its 2.5 mm default connector does not fit a 3 mm strut, and its 0.0 mm default size
tolerance designs in no clearance (§3.1) — plus the guidance to omit connectors entirely in favour
of glue (§6), **and the plane choice**, since cutting on the `vertex` axis rather than the model's
authored equator is what turns a scatter of butt faces into one continuous annulus (§3.4). Note that
the authored equator *is* the `edge-2` plane, so "cut at z = 0" in a slicer gets the middle option,
not the best one. Brim guidance is plane-conditional: on `vertex-N` the first layer is a continuous
outline and a standard outer brim suffices; on `face-N`/`edge-2` it is 12–16 disjoint regions and
wants an inner+outer brim (Prusa's "≥ 3 mm brim").

### 9.2 What P3 would have to show to flip this to A

Per [`catalog.md`](../.claude/skills/prototype/catalog.md), P3 owns the verdict and is blocked on
P2 (task #10, on hold). Recording the flip conditions now so P3 returns a decision rather than
observations:

- **P3-Q1 (flat-down vs whole)** flips toward building only if the slicer's own cut proves
  *unusable* on this geometry — e.g. the planar cut leaves non-manifold edges (Bambu documents this
  for its *dovetail* mode; the planar case is undocumented either way — survey §8 item 11). Note
  that the connector-guard objection is weak on the `vertex` plane, where the cross-section is a
  single region.
- **P3-Q2 (seam strength)** flips toward **B** only if the **annular** seam proves too weak to
  survive handling. The quantity to test is the `vertex-N` 898 mm² lap band, not v1's imagined
  7.2 mm² butt faces — §3.4 puts it at ~2.2 kN in tension against a 57 g object, so this is now
  *unlikely* to be the failure mode rather than the most likely one. The real question P3 answers is
  whether a hand-glued seam on a lattice cross-section achieves anything close to the coupon
  literature's per-mm² figure.
- **P3-Q3 (alignment difficulty)** flips toward **B** only if hand-alignment of the two rims proves
  impractical. Note §3.3: whatever the answer, the remedy cannot be a pin in a strut. Note also that
  a `vertex-N` annular rim is largely self-jigging.
- **P3-Q4 (where the cut lands)** should compare **`vertex-5` against `face-3` explicitly** — the
  strength/invisibility trade in §4 is the one question here that a print answers better than any
  amount of reading. **The catalog's P3 entry currently says "cut at the equator *in the slicer*",
  which is the `edge-2` plane and will therefore test neither.** Re-aiming it is tracked in §10 Q5.

If P3 returns "reorienting was enough" or "the slicer cut worked fine", A0/C stand and task #11
closes as **built-elsewhere**, not as **won't-fix**.

## 10. Open questions

- **Q1 — the `orb-lab-design.md:344` correction. ✅ Applied (owner-approved 2026-07-30).** "Would
  relax the Z term for tall-bed machines" named the wrong class of machine and implied a size
  benefit no offered preset can realise. It now states that the split raises the ceiling on no
  preset, helps only a hand-entered short-Z Custom machine, and that its real benefit is bed
  contact rather than size (§1.1).
- **Q2 — which symmetry axis is the default?** **Answered by measurement, not deferred**:
  `vertex-N` (§4). What remains open is only whether an author-facing selector is worth shipping if
  the split is ever built, since `face-N` buys seam invisibility at a real cost in strength.
- **Q3 — does the cap belong in `slice.ts` or a new module?** A `kernel3d/split.ts` importing
  `slice.ts`'s helpers is the cleaner shape, but all five helpers are currently module-private
  (§2), so either the split lives inside `slice.ts` or `slice.ts` widens its export surface.
  Deferred to build time; the cost is now priced in §9.1 Option A.
- **Q4 — do the near-pole cell spans exceed the bridging limit?** The survey could not settle
  whether the top ~30 % of a lattice hemisphere needs support, because all overhang guidance is
  written for solid surfaces, and the answer depends on near-pole *cell span*. The limit to compare
  against is already registered as **`CAL-BRG-01`** (coupon MC-3) — no new bet. The engine can
  answer this without a print, and doing so is the only way to sharpen §3.5's supports row beyond
  the symmetry argument. Worth measuring regardless of the option chosen.
- **Q5 — re-aim the P3 catalog entry. ✅ Applied (owner-approved 2026-07-30).** P3 said "cut at the
  equator in the slicer", which is the `edge-2` plane (§2) and would have tested neither the
  recommended `vertex-N` plane nor v1's `face-N`. P3 now cuts on the vertex axis and compares
  against face; P3-Q1 is benchmarked against Option A0 (reorientation) rather than the authored
  whole-sphere print; and P3-Q2 asks what the annular seam achieves per mm² rather than whether
  7.2 mm² butt faces suffice.

## Appendix A — survey sources

Full survey with per-claim URLs and verified/snippet tagging:
[`research/hemisphere-split-survey.md`](research/hemisphere-split-survey.md). Adversarial audit of
this doc against those sources and the engine:
[`research/hemisphere-split-grounding-audit.md`](research/hemisphere-split-grounding-audit.md).
Load-bearing sources:

**Slicer / CAD primary (read from source or official docs)**
- PrusaSlicer cut tool — https://help.prusa3d.com/article/cut-tool_1779 ; defaults read from
  `src/slic3r/GUI/Gizmos/GLGizmoCut.hpp` / `.cpp`
- OrcaSlicer — same files, byte-identical defaults; official wiki page is a one-line stub
- Bambu Studio cut tool — https://wiki.bambulab.com/en/software/bambu-studio/cut-tool (documents
  that dovetail cutting "may" leave non-manifold edges)
- Bambu overhang guidance — https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang
- Bambu dome-structure thread — https://forum.bambulab.com/t/3-ways-to-reduce-line-detachment-in-dome-structures/192368
- Meshmixer Plane Cut ("when you cut a solid, you get a solid") —
  https://help.autodesk.com/cloudhelp/2019/ENU/MSHMXR/files/GUID-C36CDABA-05F7-44B0-9529-C33D9E435220.htm
- Blender Bisect (Fill option) —
  https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/bisect.html
- Cura `fdmprinter.def.json` (`support_angle` default 50°) —
  https://raw.githubusercontent.com/Ultimaker/Cura/main/resources/definitions/fdmprinter.def.json

**Design rules and clearances**
- Hydra Research design rules (min hole > 2 mm, min wall 0.9 mm, bridge < 10 mm) —
  https://www.hydraresearch3d.com/design-rules
- Protolabs/Hubs FDM design (bridge < 5 mm, 45° overhang, 45° chamfer on bed edges) —
  https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
- Prusa modelling guidance (0.2 mm accuracy, 0.3 mm for movable parts) —
  https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
- Prusa skirt and brim (≥ 3 mm) — https://help.prusa3d.com/article/skirt-and-brim_133969
- Glue-moat geometry (1 mm inset, 2 mm wide, 1 mm deep, 0.2 mm fit gap) —
  https://forum.bambulab.com/t/glue-moat-for-joined-parts/75168

**Bonding and materials**
- Shen, Zhang & Qin, wedged mortise–tenon joints for FFF, *Prog. Addit. Manuf.* 11:4025–4041
  (2026), open access — https://doi.org/10.1007/s40964-026-01565-3
- Prusament PLA TDS (51 ± 3 MPa tensile, 17 ± 3 MPa interlayer) —
  https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf
- Loctite *Design Guide for Bonding Plastics* v6 (joint design rules, bondline-gap table; no PLA
  section) —
  https://www.ellsworth.com/globalassets/literature-library/manufacturer/henkel-loctite/henkel-loctite-design-guide-plastic-bonding.pdf

**Decomposition literature**
- Luo, Baran, Rusinkiewicz & Matusik, "Chopper: Partitioning Models into 3D-Printable Parts", ACM
  TOG 31(6), SIGGRAPH Asia 2012 — https://gfx.cs.princeton.edu/pubs/Luo_2012_CPM/index.php
- pychop3d (open-source Chopper; `connector_diameter 5`, `connector_tolerance 1`) —
  https://github.com/gregstarr/pychop3d
- Hu, Li, Zhang & Cohen-Or, "Approximate Pyramidal Shape Decomposition", ACM TOG 33(6), 2014 —
  https://www2.cs.sfu.ca/~haoz/pubs/hu_siga14_pym.pdf
- Alderighi et al., "Volume decomposition for two-piece rigid casting", ACM TOG 40(6), 2021 —
  https://doi.org/10.1145/3478513.3480555

**Mesh validity**
- trimesh (`is_watertight`, `slice_mesh_plane(cap=)`) — https://trimesh.org/trimesh.base.html
- libigl `is_edge_manifold` / `boundary_loop` — https://github.com/libigl/libigl
- CGAL Polygon Mesh Processing, `stitch_borders` —
  https://doc.cgal.org/latest/Polygon_mesh_processing/index.html
- MeshLab topological measures (genus reported only after 2-manifold confirmation) —
  https://github.com/cnr-isti-vclab/meshlab/blob/main/src/meshlabplugins/filter_measure/filter_measure.cpp
- Euler characteristic additivity — https://en.wikipedia.org/wiki/Euler_characteristic

## Appendix B — contested bets and divergences

### B.1 No new calibration bet is minted by this document

`CAL_BET_IDS` (`kernel3d/calibration.ts:33-56`) registers ten ids: `CAL-FIT-01`, `CAL-HOL-01`,
`CAL-FEA-01`, `CAL-BRG-01`, `CAL-OVH-01`, `CAL-WRP-01`, `CAL-BED-01`, `CAL-RIB-01`, `CAL-DET-01`,
`CAL-STR-01`. Every physical constant this doc leans on is already one of them:

| Quantity used here | Owning bet | Where |
|---|---|---|
| 25 mm² bed-contact floor / 1 % ratio | `CAL-BED-01` | `print-gate.ts:47-55` |
| 1.2 mm min printable feature | `CAL-FEA-01` | `mesh-gate.ts:13` |
| Bridge / cell-span limit (§10 Q4) | `CAL-BRG-01` | coupon MC-3 |
| 45° overhang threshold | `CAL-OVH-01` | — |
| Seam-lip clearance ladder (§6) | `CAL-FIT-01` | `fit-profile.ts:27-40` |

The one genuinely new empirical residue is **adhesive seam strength per mm² on an FFF butt/lap
face** (§3.4, §9.2 P3-Q2). No existing id covers it — `CAL-STR-01` is the *Z-layer* interlayer
strength ratio, a different failure plane; `CAL-FIT-01` is a clearance ladder.

**It is deliberately not minted here.** `catalog.md`'s P3-Q2 already owns the measurement with an
apparatus, and this document recommends *not building* the feature the bet would serve. Minting
`CAL-SEA-01` would register a bet against a declined feature and would duplicate an open question —
"the same quantity open in two docs is one bet, not two". If the owner wants it registered, the
right shape is one bet keyed to the measurement (adhesive seam strength per mm² on an FFF butt/lap
face), owned by P3, not by this doc.

### B.2 Claims that changed between v1 and v2

Every one of these was asserted in v1 and is corrected above. They are recorded because the
*direction* of the error is informative: v1 measured one plane, assumed it was the proposed plane,
and built four arguments on the mismatch.

| v1 claim | Status | Correction |
|---|---|---|
| χ(top) + χ(bottom) = χ(original) | **Wrong** | Off by 2·χ(cap). Holds only for an annular cap; as a hard error it would reject correct `face-N`/`edge-2` splits (§5.3) |
| "The widest layer *is* the equator" | **Wrong** | Widest is 650.4 mm² at z = −49.9, a polar pentagon ring. The equator is 75.5 % of it (§3.5) |
| "~83× bed contact" | **Wrong** | 5.8× / 62.5× / 230× depending on plane (§3.5) |
| "The print gate reports 20 first-layer regions" | **Wrong** | Misread `islands=0/20` (orphan/supported). First layer has **1** region; every "~20 struts / ~144 mm²" figure was invented (§3.5) |
| "A ring of 7.2 mm² butt faces — the worst geometry in Loctite's taxonomy" | **Wrong** | 898 mm² single annulus on the default plane — the *best* geometry in that taxonomy (§3.4) |
| `face-N` default | **Reversed** | Its own rationale makes it worst for both surviving benefits; default is now `vertex-N` (§4) |
| Socket ceiling `3 − 2(0.9) = 1.2 mm` | **Wrong dimension** | Binding dimension is the 2.4 mm depth → **0.6 mm**; and the claim is false above `struts depth 3.8` (§3.3) |
| "Cell-following seam is ruled out" | **Overclaimed** | The survey left it explicitly open; downgraded to unsettled (§3.2, B.3) |
| "Supports neutral" via a 29.3 % overhang statistic | **Right answer, invalid argument** | Overhang statistic explaining island findings; F4 is unimplemented. Replaced with a measured mirror-symmetry argument (§3.5) |
| "Every step but the last two already exists" | **Wrong** | All five slice helpers are module-private on `origin/main` (§2) |
| "Wound outward for one half and inward for the other" | **Wrong** | Both caps wind outward w.r.t. their own solid (§5.1) |
| "Both clauses are true" (`orb-lab-design.md:344`) | **Wrong** | Relaxing Z helps *short*-Z machines; "tall-bed" is backwards (§1.1) |
| "Gain is exactly zero on all six" | **Incomplete** | Nine presets ship; and the Custom entry admits a short-Z machine where the gain is real (§1.1) |
| `language-reference.md:838`, `evaluator.ts:2483` | **Wrong citations** | `:840` and `:2485` (§6) |

### B.3 Open counter-evidence, carried rather than resolved

1. **Non-planar / cell-following seams may be viable.** The survey's §8 item 4 leaves this open and
   no source settles it. The steelman — only one contact surface need be planar, a raft absorbs a
   few millimetres, a hybrid planar-rim design gives up nothing — is unrefuted. This doc goes planar
   because planar is sufficient and cheap, **not** because the alternative was disproved.
2. **The bed-contact threshold is unearned.** `CAL-BED-01`'s own basis says "no primary source at
   all", and F7 is warn-only by design. Every "clears the floor" claim in §9.1 inherits that
   weakness; the defensible version is the relative improvement (3.8× for A0), not the pass/fail.
3. **No manufacturer adhesive data exists for PLA or PETG.** Loctite's guide covers ABS, ASA, PMMA,
   acetal and nylon and nothing else; every PLA figure here is academic or community.
4. **`meshStats` cannot see pinch vertices.** §5.1's "the existing gate suffices" is true except for
   a plane tangent to a strut; validator 5 (rim correspondence) is what covers it, and that
   validator is specified but unbuilt.
5. **The whole scorecard is measured on one pattern.** Every number is Star-Orb at `radius 60`,
   `strut_width 3`, `strut_depth 2.4`. The three-plane comparison in particular is an icosahedral
   fact; a Goldberg or cube-based orb has different symmetry axes and may not have any plane that
   cuts a continuous annulus. Nothing here should be generalised to the other ten shipped orbs
   without re-measuring.
