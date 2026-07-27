<!-- Research report produced 2026-07-27 by a deep-research subagent (code-CAD prior art:
     BOSL2, CadQuery/build123d, OnShape/Fusion, Manifold, Clipper2, CGA, Tsugite, 3MF, KCL).
     Feeds docs/piece-composition-design.md — its §3 borrow/avoid table, §8 Manifold policy,
     and the three design mistakes are condensed from this. Kept verbatim for provenance. -->

# Prior-Art Research: Composition for bikar

## 1. OpenSCAD + BOSL2 attachments (deepest prior art for `port`/`connect`)

**Anchor model.** A BOSL2 anchor is a triple: **position + direction + spin**. Standard anchors on box-like shapes are vectors with components in {-1,0,1} — `[0,0,1]` is `TOP`, `BOTTOM+BACK+RIGHT` is a corner. Placement is a fixed pipeline: *translate to anchor → spin (rotate about Z) → orient (rotate top toward direction)* — "an object is first translated to its anchor position, then spun, then oriented." Non-box shapes pick an anchor scheme via `atype=` (`"box"`, `"perim"`, `"intersect"`, `"hull"`), which matters for curved perimeters.

**Four composition modules**, in increasing power:
- `position(at)` — translate child to parent anchor, no rotation.
- `orient(anchor, spin)` — rotate child's top toward the anchor direction.
- `align(anchor, align, inside=, inset=, shiftout=, overlap=)` — place on a face, snap to an edge/corner; child's own `anchor=` is *ignored*.
- `attach(parent, child, align=, spin=, overlap=, inside=, inset=, shiftout=)` — the real mating primitive. It points the two anchors *at each other* (child direction inverted) and pushes the objects together.

Verbatim from the tutorial (https://github.com/BelfrySCAD/BOSL2/wiki/Tutorial-Attachment-Attach):

```scad
cube(50,anchor=BOT)
  attach(TOP,BOT) cylinder(d1=30,d2=15,h=25);

// subtraction via the same mechanism:
diff()
cube(50,anchor=BOT)
  attach(TOP,TOP,inside=true,shiftout=0.01)
    cylinder(d1=30,d2=15,h=25);

// spin about the joined anchor axis; overlap sinks the child in:
cube(30) attach(RIGHT,BOT,spin=-90) prismoid([8,8],[6,6],shift=-[1,1],h=8);
cuboid(50) attach(TOP,BOT,overlap=15) cuboid(20);
```

Key semantic rule: with two-argument `attach()`, "both `anchor=` and `orient=` given to the child are ignored" — the mate wins over the child's own frame. `inside=true` flips the mating for cavities and `shiftout` epsilon-extends to avoid z-fighting — i.e., **the same attach vocabulary drives both addition and subtraction**, which is exactly the countersink/hole pattern bikar wants.

**Custom/named anchors.** Authors wrap geometry in `attachable(anchor, spin, orient, size=..., anchors=[...]) { shape(); children(); }` and build anchors with `named_anchor(name, position, direction, spin)`. Complex parts (stepper motors, screws) expose semantic anchors like `"screw1"`. Children can read `$attach_anchor` to react to where they're attached.

**Pain points (forums/issues):**
- Jargon wall: "I sort of glossed over the parts of the manual where it just became too much of a jargon mumble for me to understand" (https://lists.openscad.org/empathy/thread/3U2AWJGYUBTRD3L2IPAH2QPDIU4IWH4E).
- Making custom parts attachable is heavy even per the maintainer: "It's not the easiest process to create well-behaved attachable modules, so I don't think it makes sense to do it for intermediate one-off parts" (Adrian Mariano, same thread).
- Inconsistency bugs: named anchors that work with `position()` but fail in `attach()` with "from and to must be specified together" (https://github.com/BelfrySCAD/BOSL2/discussions/1315, unanswered).
- Four overlapping modules (`position`/`orient`/`align`/`attach`) with different rules about which child parameters get ignored; anchor **spin** semantics confuse even the official examples.
- No contracts: `attach()` aligns frames but knows nothing about pin diameters or clearances — every fit is manual arithmetic.

Docs: https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad

**→ bikar take:** Borrow the anchor = (position, direction, spin) triple, the "anchors point at each other" mating rule, `inside=`/`shiftout` for subtractive mating, and semantic *named* anchors as the only user-facing kind. Avoid the 4-module zoo — bikar needs exactly one `connect`. Avoid making attachability opt-in/hard: every `piece` should get ports for free from its declaration. BOSL2's biggest gap — no dimensional contract on the anchor — is precisely what bikar's `port` (pin dia, clearance, ring) adds; that's the novel part, keep it.

## 2. CadQuery / build123d — selectors and joints

**Selectors** (https://cadquery.readthedocs.io/en/latest/selectors.html): string micro-grammar filters topology lists — `>Z` farthest in +Z, `|X` parallel, `+Z`/`-Z` aligned, `%Plane` by type, `#Z` perpendicular; combinable: `edges("|Z and >Y").chamfer(0.2)`; arbitrary directions `edges(">(-1,1,0)")`. Known failure mode, verbatim: "If a face is not planar, selectors are evaluated at the center of mass of the face. This can lead to results that are quite unexpected." Selectors are also **order-fragile**: they select by geometric predicate over whatever topology the kernel produced, so upstream edits silently re-target them (the classic "topological naming problem" lives on in geometric form).

**CadQuery assemblies** (https://cadquery.readthedocs.io/en/latest/assy.html): a numeric constraint *solver* — `Point`, `Axis`, `Plane`, `PointInPlane`, `PointOnLine`, `FixedPoint/Rotation/Axis` — with string paths mixing tags and selectors:

```python
door.constrain("left@faces@<Z", "con_bl?Z", "Plane")
door.constrain("panel?hole1", "handle?mate1", "Plane")
assy.solve()
```

The solver minimizes a cost function; under-constrained systems depend on initial locations; users found it painful: "a system of constraints... made placing components in assemblies far more difficult than desired" (https://news.ycombinator.com/item?id=41548945).

**build123d joints** (https://build123d.readthedocs.io/en/latest/joints.html) replaced solving with **direct kinematic pairs**: `RigidJoint`, `RevoluteJoint`, `LinearJoint`, `CylindricalJoint`, `BallJoint`, each carrying a label and a location/axis, connected pairwise and deterministically:

```python
RigidJoint(label="outlet", to_part=pipe, joint_location=path.location_at(1))
RevoluteJoint("hinge", axis=Axis.X, angle_reference=Vector(0,1,0), angular_range=(0, 90))
pipe.joints["outlet"].connect_to(flange_outlet.joints["pipe"])
latch.part.joints["latch"].connect_to(slide.part.joints["slide"], position=12)
```

User verdict: build123d joints let you "simply declare: 'This part goes right here', no fuss" vs CadQuery's solver. Complaints: joints are one-shot repositioning (not persistent constraints), and joint placement still requires computing a `Location` by hand.

**→ bikar take:** Borrow build123d's *named joints + deterministic pairwise connect* — skip constraint solvers entirely (declarative ≠ numeric solving; solvers bring under-constraint ambiguity and debugging hell). Borrow the `connect_to(other, position=, angle=)` parameterization for adjustable mates. Avoid CadQuery-style geometric selectors as the way to *name* mating features — bikar's ports should be declared by name at authoring time, never discovered by predicate over derived topology.

## 3. Commercial mate vocabularies (OnShape, Fusion 360)

**OnShape** (https://cad.onshape.com/help/Content/mate.htm) — 9 mates, but only 7 are kinematic pairs: **Fastened** (0 DOF), **Revolute** (1R), **Slider** (1T), **Cylindrical** (1R+1T), **Planar** (2T+1R), **Pin-slot** (1R+1T on different axes), **Ball** (3R); plus relation-style **Parallel** and **Tangent**. Crucially, OnShape mates are *one mate per connection* (unlike SolidWorks' stacked constraints) — each mate references exactly **two mate connectors**.

**Mate connectors** are "local coordinate systems located on or between entities" — full frames (origin + Z axis + X axis), created two ways: *implicitly* (hover: centroid of face, midpoints, vertices, **centers of circular openings, centers of negative space for cuts**) or *explicitly* placed and owned by the part. The implicit "center of a hole" connector is the workhorse — the hole you cut *is* the mating feature.

**Fusion 360** (https://help.autodesk.com/cloudhelp/ENU/Fusion-Assemble/files/GUID-8818AE31-958A-4A59-989B-9875A174C67A.htm) — exactly **7 joint types**: Rigid, Revolute, Slider, Cylindrical, Pin-slot, Planar, Ball. Same vocabulary, independently converged. Fusion adds two placement modes: **Joint** (moves parts to mate) vs **As-Built Joint** (parts already positioned; just declare the relationship) — plus standalone **Joint Origin** features (a named frame placed on geometry, reusable across joints).

**Minimal vocabulary finding:** the industry fixed point is {fastened, revolute, slider, cylindrical, planar, pin-slot, ball}, and for *printed static assemblies* the effective working set collapses to **fastened + revolute + slider** — everything else is motion simulation. For bikar (static pierced-lattice assemblies with pins/rings), **fastened with an axis + optional free spin (i.e., fastened vs cylindrical)** covers nearly everything.

**→ bikar take:** Borrow (1) mate connector = full coordinate frame owned by the part, (2) one-mate-per-connection, (3) As-Built semantics (bikar layouts are declarative; `connect` should never need to "move" anything at author time — it *derives* placement), and (4) OnShape's insight that hole centers are first-class connectors: bikar's `hole` should automatically mint a `port` at its axis. Defer the full 7-type vocabulary: ship `fastened` (rigid pin+ring) and maybe `axis` (rotationally free) and stop.

## 4. Manifold library (the boolean escape hatch)

**Guarantees & mechanism** (https://github.com/elalish/manifold, https://github.com/elalish/manifold/wiki/Manifold-Library): "guaranteed manifold output without caveats or edge cases" — the first guaranteed-manifold mesh boolean. Not exact arithmetic: floating point + **symbolic perturbation** (modified Smith), engineered so "the same question is never asked in two different ways." Union perturbs the first mesh along its surface normals (so touching cubes merge; equal-height differences make through-holes). Manifoldness is guaranteed *by construction* ("the set of manifold meshes *is* closed under Boolean operations"); geometric ε-validity is targeted but "cannot be mathematically proven." Limitations: requires manifold inputs (a `Merge` fixes slightly-broken ones); no single-mesh self-intersection repair; degenerate sliver triangles below ε may survive; error compounds across chained ops.

**Performance:** TBB-parallelized, serial fallback for small problems. OpenSCAD integration (2023, Preferences→Features→manifold; default backend since 2025): **5–30× over CGAL fast-csg**; one model went 3m36s → 3.4s (https://github.com/elalish/manifold/discussions/387). Key architectural detail for bikar: Manifold records CSG ops and **evaluates lazily**, reordering/parallelizing the tree — booleans are free until you ask for the mesh.

**JS/TS integration:** npm `manifold-3d` v3.5.1 (Jan 2026 registry data), unpacked ~**2.76 MB** (wasm is the bulk of it), ships `manifold.d.ts` TypeScript types, ESM. Setup:

```js
import Module from 'manifold-3d';
const wasm = await Module();
wasm.setup();
const { Manifold } = wasm;
const result = Manifold.difference(a, b);   // also .union, .intersection, .add
```

Powers ManifoldCAD.org (script in JS/TS) and a documented three.js round-trip (https://manifoldcad.org/three) via `Mesh`/`MeshGL` (flat Float32/Uint32 arrays — trivially adaptable to bikar's mesh struct). Adopters: OpenSCAD, Blender, Godot, Babylon.js, BRL-CAD, trimesh. Known friction: bundler setup for the .wasm asset is under-documented (open issue https://github.com/elalish/manifold/issues/1343 — Parcel/web bundling examples requested); async WASM init forces an async boundary into an otherwise-sync geometry pipeline.

**Cost of adoption:** ~2–3 MB payload + async init + a mesh↔MeshGL adapter (~100 LOC given bikar already produces indexed watertight meshes — which is precisely the input contract Manifold wants). No native build complexity: prebuilt wasm. The real cost is *semantic*: once booleans exist, the temptation is to stop maintaining constructive watertightness — resist that (see verdict below).

**→ bikar take:** Bikar's "watertight by construction" pipeline is Manifold's ideal *feeder* — adopt it later as an opt-in backend for the few ops stitching can't do, not as the core. Lazy CSG-tree evaluation is worth stealing as an internal IR shape even pre-Manifold.

## 5. Clipper2 and 2D boolean/offset robustness

**Capabilities** (https://github.com/AngusJohnson/Clipper2): intersection/union/difference/XOR on simple *and complex* polygons; EvenOdd + NonZero (and Positive/Negative) fill rules; offsetting with join types **miter, round, square, bevel** and end types including **open-path** offsetting (polylines → stroked polygons — useful for bikar strapwork). Robustness comes from **int64 coordinates** (floats scaled in/out), sidestepping FP predicate failures entirely. Degenerate output (slivers, micro-self-touches) is *expected* and handled by explicit post-pass `SimplifyPaths`/cleaning — the library documents iterative offset + simplify as the standard recipe.

**JS/WASM ports:** `clipper2-wasm` (ErikSom, https://github.com/ErikSom/Clipper2-WASM) — works, ~1.3k weekly downloads, but v0.2.1, last publish >1 yr, single-maintainer; fork `@dexus1985/clipper2-wasm` v1.4.0, similarly dormant. The old Clipper1 port (`clipper-lib`, pure JS) is ancient but battle-tested. Nothing here is as healthy as manifold-3d.

**Known 2D pitfalls** (from Clipper docs/issues + general practice): (1) sliver polygons from near-tangent boolean edges — must clean by area/width threshold; (2) offsetting can self-intersect or vanish thin features — inset by more than half the local feature width deletes geometry *silently*; (3) float→int scaling picks a global precision — too coarse loses arcs, too fine overflows on multiplied intermediate values; (4) winding/orientation conventions (holes = opposite winding) are an endless source of bugs when interoperating with earcut, which wants hole indices, not winding.

**→ bikar take:** Bikar already lives in the "2D booleans then extrude" world — adopt the Clipper2 *approach* (scaled integer grid + explicit post-simplify + area-threshold sliver culling) even if implementing natively in TS; treat `clipper2-wasm` as a reference/validation oracle rather than a load-bearing dependency given its maintenance state. `hole` as 2D subtraction per z-band is exactly the robust move — every countersink is a clean 2D boolean, never a 3D one.

## 6. Declarative assembly / grammar prior art

- **CGA shape grammar (CityEngine)** (https://doc.arcgis.com/en/cityengine/latest/tutorials/tutorial-6-basic-shape-grammar.htm): the strongest prior art for `wall`. Facades are produced by *split rules*: `split(y){ 4: Groundfloor | {~3.5: Upperfloor}* }` — repeat operator `{...}*` plus the tilde `~` for *flexible sizes that stretch to fit exactly*, guaranteeing "matching floors with no holes." Floors split into **tiles**, tiles into wall/window elements. This is a declarative grid-with-crop: the region dictates counts and the `~` absorbs the remainder — no manual modulo math.
- **Tsugite** (UIST 2020, https://dl.acm.org/doi/10.1145/3379337.3415899): joints as a **3D voxel grid** design space, enabling combinatorial search and automatic checking of *slidability, fabricability, durability*. Lesson: a constrained joint representation buys you machine-checkable validity — analogous to bikar's port contract (pin dia + clearance) being checkable at compile time.
- **Print-in-place vs assembled**: consensus clearances — PIP joints 0.3 mm start (0.2–0.6 range); FDM snap/pin fits 0.2–0.3 mm snug, 0.4–0.5 mm free-sliding; material shrinkage shifts these (PLA/PETG 0.2–0.5%, ABS/Nylon up to 1.5%); pros print *fitment gauges* first (https://qidi3d.com/blogs/print-lab/3d-printed-snap-fit-joints-clearance-guide, https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/). This is direct input to `port` contract defaults: clearance should be a named, material-profile-scoped parameter with a `fit: snug|free` enum, not a magic number.
- **3MF multi-part** (https://github.com/3MFConsortium/spec_core/blob/master/3MF%20Core%20Specification.md): `<resources>` holds `<object>`s (which may nest other objects as `<component>` with transforms — components must not be re-transformed relative to each other by the printer); `<build>` holds `<item objectid=... transform=...>` for each thing actually printed; `<item>` supports `<metadatagroup>` with vendor key/value metadata per object. So: **bikar assembly → one object per piece, build items with placement transforms, per-item metadata for port/mate provenance.** JS support: `@jscadui/3mf-export` (already a dependency of manifold-3d!) writes 3MF from JS; `three-mf` (TypeScript, https://github.com/watzon/three-mf) parses/builds 3MF without manual XML/ZIP.

**→ bikar take:** Borrow CGA's `~`-flexible repeat split as `wall`'s layout semantics (declare tile nominal size, let the wall stretch/crop to fit the boundary). Borrow Tsugite's mindset: ports constrained enough to *verify* (does the pin fit? is clearance ≥ material minimum?). Emit 3MF with one object per `piece` + build transforms — `@jscadui/3mf-export` makes this nearly free since it rides along with manifold-3d anyway.

## 7. Arrays / patterns / instancing

- **OpenSCAD core**: bare `for` loops + `children()`; no per-instance context beyond loop vars; cropping = intersect the whole array with a volume (wasteful, and cut instances become fragments, not omitted instances).
- **BOSL2 distributors** (https://github.com/BelfrySCAD/BOSL2/wiki/distributors.scad): `xcopies/ycopies/zcopies`, `line_copies`, `grid_copies(spacing, stagger=, inside=)`, `rot_copies`, `arc_copies`, `sphere_copies`. **`grid_copies` has first-class boundary crop**: "If given a list of polygon points, or a region, only creates copies whose center would be inside the polygon or region."

```scad
poly = [[-25,-25], [25,25], [-25,25], [25,-25]];
grid_copies(spacing=5, stagger=true, inside=poly)
   zrot(180/6) cylinder(d=5, h=1, $fn=6);
```

  Per-instance variation via context vars: `$idx`, `$pos`, `$row`, `$col`, `$ang`, `$dir` — so alternating rotation is `zrot($idx%2*90 ...)` and checkerboards key off `($row+$col)%2`. This is the closest existing thing to "crop an array against a boundary region" — but note it's *center-inside* culling, not clipping: partial tiles are dropped, never trimmed.
- **CadQuery**: `pushPoints([...])`/`rarray()` on workplanes, then `.each()`/`cutEach()` — Python-level iteration, no declarative crop.
- **KCL (Zoo)** (https://zoo.dev/docs/kcl-std/functions/std-solid-patternTransform): `patternLinear3d(instances=4, distance=10, axis=[1,0,0])`, `patternCircular3d`, and the general `patternTransform(instances, transform)` where transform is a **function of the 1-based instance index** returning `{translate, rotate, scale, replicate}` — the cleanest per-instance-variation design in any code-CAD language: `fn transform(@id) { return { translate = [4 * id, 0] } }`. The `replicate=false` return field even allows predicate-based *omission* (checkerboard by returning replicate for even ids). No boundary-crop primitive.
- **CGA `{~size: Tile}*`** (see §6) is the only system where the *boundary drives the count and the tiles stretch* — true crop semantics, but 2.5D-architectural only.

**→ bikar take:** Borrow BOSL2's `inside=region` culling *and* CGA's `~` stretch as two explicit crop policies on `wall`/`tile`: `crop: drop | clip | stretch` (drop = BOSL2 center-cull; clip = actually 2D-boolean each tile against the boundary — bikar's 2D pipeline can do what BOSL2 can't; stretch = CGA flexible sizing). Borrow KCL's index-function for per-instance variation but declaratively (`alternate:`, `checker:` sugar over an index expression). Nobody has all three policies — this is a genuine differentiation point.

---

## (a) Recommended minimal grammar (.bkr sketch)

Synthesis: build123d's named-joint determinism + OnShape's frame-with-contract connectors + BOSL2's inside/shiftout subtractive mating + CGA/BOSL2 crop semantics.

```bkr
profile hex_ring { ... }                      // existing 2D machinery

piece bracket {
  extrude hex_ring height 6
  hole "pin1" at (10, 0) {                    // 2D subtraction, per z-band stack
    band d 3.2 from 0 to 4                    // shaft
    band d 6.0 from 4 to 6                    // countersink
  }
  // every hole mints a port at its axis (OnShape implicit connector):
  port "pin1" from hole "pin1" {              // frame = hole axis, z = +normal
    kind pin_socket                           // contract vocabulary, not geometry
    pin d 3.0  clearance snug                 // snug=0.25, free=0.45 (material profile)
    ring d 6.0 depth 2
  }
  port "hang" at face top (0, 20) dir +z spin 0   // explicit named frame
}

piece pin { revolve pin_profile;  port "a" at tip dir -z { kind pin, d 3.0 } }

assembly frame {
  place bracket as b1
  place bracket as b2 rotate z 180
  connect b1.pin1 -> pin.a                    // fastened (default): frames anti-aligned
  connect b2.hang -> hook.mount spin 90       // BOSL2-style spin about mate axis
  // contracts checked here: pin.d + clearance vs socket.d, ring depth vs band, etc.
}

wall lattice {
  boundary arch_outline                        // any bikar 2D region
  tile star_tile size 24 stagger               // nominal tile
  crop clip                                    // drop | clip | stretch
  vary rotate z (idx % 2 * 90)                 // KCL-style index expression
  frame width 4                                // fused border, stitched not booleaned
}
```

Rules: one `connect` verb (no position/orient/align/attach zoo); ports are always declared or derived from holes, never selected by geometric predicate; `connect` is as-built/deterministic — no solver; contracts are validated at compile time with material-profile clearance tables.

## (b) Verdict: when Manifold becomes unavoidable

Constructive stitching + 2D booleans go **remarkably far** — farther than most teams assume: every prismatic piece, every hole/countersink/counterbore (stacked z-band 2D subtraction), tile walls with clip-cropping (2D boolean per tile, then extrude), revolved pins, and even piece∪piece fusion *when the union is expressible as a 2D union before extrusion or a boundary stitch at a shared planar interface*. That covers ~90% of a pierced-lattice/bracket/pin domain.

The specific operations that force the transition:

1. **Non-coplanar intersection of two already-3D solids** — a pin hole drilled at an angle through a curved orb shell; a revolved solid subtracted from an extruded one. No 2D projection exists; stitching cannot express the intersection curve.
2. **Union of overlapping extrusions from different planes** (two walls meeting at a dihedral, cross-lap joints à la Tsugite) — the seam is a general 3D curve.
3. **Chamfer/fillet across a 3D seam** — needs the seam first, which needs the boolean.
4. **Global shell/offset of a composed 3D result** (e.g., "thicken the whole assembled orb by 1 mm").

Recommendation: keep the constructive core as the *primary* backend forever — it produces cleaner, ε-free, semantically labeled meshes and is Manifold's ideal input format anyway. Add manifold-3d (~2.76 MB wasm, TS types, async init) as a **lazy opt-in backend** triggered only when the compiler detects one of the four cases above — mirroring OpenSCAD's experience, where Manifold slotted in as a swappable backend for a 5–30× win without changing the language. Cost is modest (bundle + async boundary + MeshGL adapter); the danger is cultural, not technical: don't let "just boolean it" erode the 2D-first discipline that makes bikar's output watertight and slicer-friendly.

## (c) The 3 biggest design mistakes to avoid

1. **Solving instead of declaring (CadQuery assemblies).** Numeric constraint solvers gave under-constrained ambiguity, initial-position sensitivity, and undebuggable failures; users fled to build123d's "this part goes right here" joints. Bikar's `connect` must be a deterministic frame composition, never an optimization.
2. **Attachability as a hard, opt-in, multi-API bolt-on (BOSL2).** Four overlapping placement modules with different ignore-rules, anchor spin confusion, named anchors that work in `position()` but crash `attach()`, and a maintainer conceding it's "not the easiest process" so one-off parts shouldn't bother. Ports must be free, uniform, and singular: every piece gets them from its declaration, one verb consumes them, and holes mint them automatically.
3. **Geometric selection as the naming mechanism (CadQuery `faces(">Z")`).** Predicates over derived topology are evaluated "at the center of mass" with "quite unexpected" results on non-planar faces, and silently re-target when upstream geometry changes — the topological naming problem wearing a string costume. In bikar, mating features carry author-given names from birth; geometry is derived from names, never the reverse. (Runner-up, from all three ecosystems: frames without contracts — no system ships fit/clearance semantics on its connectors, which is why every printed assembly starts with a fitment gauge. Bikar's contract-bearing `port` is the gap in the market.)

Sources: [BOSL2 attachments.scad](https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad) · [BOSL2 attach tutorial](https://github.com/BelfrySCAD/BOSL2/wiki/Tutorial-Attachment-Attach) · [BOSL2 distributors](https://github.com/BelfrySCAD/BOSL2/wiki/distributors.scad) · [OpenSCAD list: BOSL2 anchoring](https://lists.openscad.org/empathy/thread/3U2AWJGYUBTRD3L2IPAH2QPDIU4IWH4E) · [BOSL2 discussion #1315](https://github.com/BelfrySCAD/BOSL2/discussions/1315) · [CadQuery selectors](https://cadquery.readthedocs.io/en/latest/selectors.html) · [CadQuery assemblies](https://cadquery.readthedocs.io/en/latest/assy.html) · [build123d joints](https://build123d.readthedocs.io/en/latest/joints.html) · [HN on build123d vs CadQuery](https://news.ycombinator.com/item?id=41548945) · [OnShape mates](https://cad.onshape.com/help/Content/mate.htm) · [Fusion 360 joint types](https://help.autodesk.com/cloudhelp/ENU/Fusion-Assemble/files/GUID-8818AE31-958A-4A59-989B-9875A174C67A.htm) · [Manifold repo](https://github.com/elalish/manifold) · [Manifold algorithm wiki](https://github.com/elalish/manifold/wiki/Manifold-Library) · [OpenSCAD+Manifold successes](https://github.com/elalish/manifold/discussions/387) · [Manifold bundling issue #1343](https://github.com/elalish/manifold/issues/1343) · [manifold-3d three.js example](https://manifoldcad.org/three) · [Clipper2](https://github.com/AngusJohnson/Clipper2) · [Clipper2-WASM](https://github.com/ErikSom/Clipper2-WASM) · [CGA shape grammar tutorial](https://doc.arcgis.com/en/cityengine/latest/tutorials/tutorial-6-basic-shape-grammar.htm) · [Tsugite (UIST 2020)](https://dl.acm.org/doi/10.1145/3379337.3415899) · [3MF core spec](https://github.com/3MFConsortium/spec_core/blob/master/3MF%20Core%20Specification.md) · [three-mf](https://github.com/watzon/three-mf) · [KCL patternTransform](https://zoo.dev/docs/kcl-std/functions/std-solid-patternTransform) · [Qidi PIP clearance guide](https://qidi3d.com/blogs/print-lab/3d-printed-snap-fit-joints-clearance-guide) · [Hubs snap-fit guide](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/)

---

## Errata (added after the adversarial grounding audit, kept out of the verbatim text above)

The verbatim report above is preserved as delivered. The grounding audit
([`piece-composition-grounding-audit.md`](piece-composition-grounding-audit.md))
spot-checked its citations and found the following; the design doc
(`../piece-composition-design.md`) applies them:

1. **build123d quotes misattributed.** The quotes "made placing components in
   assemblies far more difficult…" and "simply declare: 'This part goes right here', no
   fuss" are verbatim from https://juraph.com/kiwi/playing_with_build123d/ — not from
   HN item 41548945 as cited. The additional complaint about joints being "one-shot
   repositioning" appears in neither source (unverified snippet).
2. **Manifold "5–30×" misattributed; one benchmark garbled.** The "5-30x speedups over
   fast-csg" phrase is verbatim from https://github.com/openscad/openscad/pull/4533
   (merged March 2023), not from manifold discussion #387 — #387 contains only an
   independent 11× user report (62.2 s → 5.4 s). The "3m36s → 3.4s" figure matches no
   fetched source and appears garbled; PR #4533's example is a BOSL2 minkowski going
   4m31s → ~4 s.
3. **"OpenSCAD's backend since 2025" needs a nuance.** Manifold became the *default* in
   OpenSCAD dev snapshots in August 2025 (mailing-list announcement, "after a long time
   of battle testing"); the stable 2021.01 release still ships CGAL-default.
4. **Hubs guide mis-grouped.** The Hubs snap-fit guide recommends 0.5 mm nominal FDM
   clearance — it does not support the −0.10/+0.05/+0.15/+0.35 fit ladder it was cited
   alongside; it is the counter-position (raw uncompensated clearance vs
   calibrated-printer designed gaps).
5. **The survey never audited BOSL2's screws.scad**, which ships thread tolerance
   classes ("6g"/"2A"), named clearance-hole fits ("close"/"normal"/"loose"), and a
   separate `$slop` printer-compensation knob — the strongest counter-example to the
   survey's runner-up claim that no surveyed system ships fit contracts.
6. **Flagged unverified (not re-fetched by the audit):** the CadQuery "center of
   mass… quite unexpected" selector quote; the Manifold adopters list
   (Blender/Godot/BRL-CAD/trimesh); clipper2-wasm version/dormancy details; Qidi PIP
   clearance numbers.
