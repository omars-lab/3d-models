# The 9-spike "maclado" orb — design doc (pre-implementation)

Status: **DRAFT v1 — pre-implementation. Chosen direction (via AskUserQuestion, 2026-08-08):
the *faithful* 9-fold maclado, i.e. a new placement-based construction family, NOT a symmetric
star-ball substitute. No engine code written yet; this doc is written to be audited by
`ground-design-doc` before any milestone starts.**

Scope: generate, in the bikar engine, a 3D-printable spherical strapwork orb tiled with
**9-pointed star rosettes** ("wheels") joined by **filler/spacer tiles**, in the deliberately
non-symmetric manner of Ángel María Martín López's "9-SPIKE 'MACLADO' RIBBON" sphere — the maker
gives up global radial symmetry so the ribbons run continuously across seams and the fillers stay
whole.

Grounding. Every mathematical and prior-art claim traces to the checked-in research survey,
[`research/maclado-orb-survey.md`](research/maclado-orb-survey.md), and its fetch record (§7 there).
Every engine claim was verified first-hand against bikar at `origin/main` (`e8b07d5`); the files it
names all exist at that ref, so the pointers below resolve regardless of which branch the sibling
checkout sits on. Where a fact could not be sourced, this doc says so rather than inventing it — the
most important such gap (§6) is load-bearing, not a footnote.

---

## 1. Goals and non-goals

**Goals.**

1. **Carry a field of faithful 9-fold wheels over a whole sphere** — each wheel a real
   9-pointed star rosette, not a 8/10/12 substitute — and export a single watertight manifold STL.
2. **Keep the fillers whole.** The object's fillers read as whole in the source image, and the name
   *maclado* together with the §2 theorem explain why symmetry must be given up to keep them so — an
   inference, since the maker's own rationale is not sourced (§6.1). That whole-filler property, not
   a picture, is the thing this design verifies (§5.3).
3. **Run the ribbon unbroken.** Over/under strapwork parity must be globally consistent across
   wheel–filler seams (§5.4).
4. **Reuse the orb pipeline's tail** — the vertex weld, the manifold gate, and the mesh emitter are
   family-independent and are reused unchanged (§3, §5.5).

**Non-goals (v1).**

- **Reproducing Martín López's exact object.** His placement rule is not retrievable (§6). We build
  a faithful 9-fold maclado *in the same spirit*, verified against the property he prizes, and the
  doc never claims fidelity to a construction it could not read.
- **A symmetric star-ball.** That is a different object with a different star order (§2); it is
  documented here only to show it is *not* the target.
- **The browser configurator.** Orb Lab (`orb-lab-design.md`) is knob-driven per-face inscription;
  the maclado family is a distinct engine path and joins the Lab, if ever, only after it ships.
- **qiyas 3D validation** of the maclado family — the front-hemisphere view-set work stays scoped to
  the existing families until this one has a mesh at all.

---

## 2. The load-bearing result: on a sphere, 9-fold *forces* broken symmetry

This is the fact the whole design turns on, and it is a theorem, not an aesthetic preference.

The finite rotation groups of the sphere are exactly five families — cyclic Cₙ, dihedral Dₙ, and
the three polyhedral groups T (order 12), O (order 24), I (order 60) — and the rotation-axis orders
inside the polyhedral groups are **only 2, 3, 4, and 5, never 9**
([survey §1](research/maclado-orb-survey.md)). Two consequences follow, and the doc states each with
its condition (survey's K10 note carried through):

- A polyhedral group is the only way to place *many* equivalent high-symmetry sites on a sphere, and
  those sites cap at order 5. So a 9-fold rosette centre **cannot** sit on a symmetry axis of any
  polyhedral group.
- The only finite sphere group with a 9-fold axis is C₉/D₉ — a *single* distinguished axis (the
  "beach-ball": one 9-fold rosette per pole, a band repeated nine times). It cannot distribute a
  second, inequivalent 9-fold centre over the sphere and still map one onto another by a symmetry.

**Therefore, conditionally:** *if* the design wants ≥2 nine-fold centres spread over the sphere —
which this one does — *then* no global rotation relates them all, and the tiling must break global
symmetry. This is why the maker "gives up radial symmetry": it is forced. (The condition matters:
a single-axis 9-fold pendant would **not** need to break symmetry, and this doc's conclusion does
not port to that easier object — survey §1, K10.)

The escape hatch the symmetric world uses is to **change the star order**, and confirming this is
what tells us our object is genuinely new. Kaplan's 3D-printed spherical star balls use **10- or
12-point stars on a truncated icosahedron / dodecahedron** — never 9 — because those solids' sites
admit 5/3/2 ([survey §4](research/maclado-orb-survey.md)). Choosing symmetry means abandoning 9;
keeping 9 means abandoning symmetry. Of the sources surveyed, none offered both (survey §1, and the
group theory says why). Historically the reconciliation has always been *one dimension down*:
Bonner classes 9-pointed stars as strictly **non-systematic**, closed by irregular filler regions
(the "9-and-12" lazo composites) — the same fix the maclado sphere uses (survey §4/§5).

**"Maclado" names this precisely.** It is the Spanish for crystal *twinning*: local order in each
domain composed into an aggregate whose symmetry is only that of the joining, and whose twin law
"is not a symmetry operation of the untwinned crystal" ([survey §2](research/maclado-orb-survey.md)).
Each wheel is a domain with local C₉; the sphere is the aggregate; the ribbons and fillers are the
join. That is the whole design in one word. (The twin-law wording quoted here is from Wikipedia's
*Crystal twinning*; the canonical IUCr dictionary entry was unreachable in the survey — HTTP 403 —
and has not been checked, so the exact phrasing is provisional and should be re-verified against
IUCr before being quoted as canonical — [survey §2](research/maclado-orb-survey.md).)

---

## 3. What the engine does today, and exactly where it refuses 9-fold

The current `orb` construction is **per-face inscription of one shared 2D pattern** on a Platonic
solid, and three facts about it — each verified first-hand — explain why it cannot be bent into a
maclado sphere and why a new family is needed rather than a new parameter.

1. **The base is a closed set of five Platonic solids.** `bikar:packages/core/src/dsl/parser.ts`
   admits `tetrahedron, octahedron, cube, dodecahedron, icosahedron` and *recognises*
   `goldberg`/`icosidodecahedron` only to reject them with "not yet supported"; `subdivide` is
   icosahedron-only, integer 1..4. Every base thus has face valence 3, 4, or 5 — the very orders §2
   says cannot host a 9-fold centre on a symmetry axis.
2. **Every face carries the *same* pattern, lifted by a shared corner map.**
   `bikar:packages/core/src/kernel3d/face-frame.ts` maps pattern-space corner *k* to face-vertex *k*
   (`patternCorner(n, k)`) precisely so adjacent faces present matching edge points and the seams
   weld. A single shared pattern with symmetry matching the face is the design's core assumption —
   the opposite of a field of individually-placed, symmetry-breaking wheels.
3. **The manifold gate is a hard throw, not a warning.**
   `bikar:packages/core/src/dsl/evaluator.ts` rejects any orb whose mesh is not watertight
   ("mesh failed the manifold gate"; the woven path additionally requires Euler characteristic 0),
   with the watertight test itself — every directed edge paired, signed volume positive — computed
   in `bikar:packages/core/src/kernel3d/solidify-lattice.ts`. A 9-rosette inscribed on a pentagon
   does not render *wrong*; it fails to close and the build **refuses**.

So the engine's refusal of 9-fold is not a missing feature switch — it is three coupled design
commitments (Platonic base, one-shared-pattern-per-face, manifold-or-nothing). The maclado family
keeps the third and replaces the first two.

**What is reusable — and the honest limits of "reuse", because the family's affordability rests on
it.** Three parts of the orb pipeline's tail are genuinely family-independent and reused unchanged:
the global vertex weld (`bikar:packages/core/src/kernel3d/weld.ts`), the combinatorial
watertight/Euler statistics and mesh gate (`bikar:packages/core/src/kernel3d/solidify-lattice.ts`),
and the binary-STL emitter (`bikar:packages/core/src/render/mesh-emitter.ts`). Two more are reused
only *with new work*, and the doc states the condition rather than implying a free ride:

- **The over/under parity solver is not family-independent as it stands.** The only exported entry in
  `bikar:packages/core/src/kernel3d/weave.ts` is `weaveLattice`, which is *face-coupled* — it lifts
  one shared 2D pattern per base face. Its graph-level core (crossing detection, strand tracing,
  parity solve) is module-private, and its crossing detector **throws unless every node has degree
  exactly 2 (corner) or 4 (crossing)** — a welded wheel-rim/filler seam where three ribbons meet
  (degree 6) is rejected before parity is attempted. So reusing it means *exporting* the graph core
  and *guaranteeing* the welded seam graph is 2-/4-valent. That is real work and an open risk (§9.3),
  not a reused part.
- **The bounded-face extractor is 2D-planar.** `bikar:packages/core/src/graph/face-extractor.ts`
  operates on a planar edge graph; the maclado field is a spherical welded graph with no single
  shared 2D subdivision, so it transfers only per-region (extract each closed region's boundary in
  its own local frame), not over the whole sphere at once.

The new work is thus the whole *head* — placing wheels, closing fillers, threading ribbons across
seams that no longer come from a shared pattern — **plus** exporting and valence-guarding the parity
core, **plus** (see §5.5) a self-intersection check the combinatorial gate does not perform.

---

## 4. Why neither existing family reaches it — and the shape of Family 3

- **Family 2 (pierced polyhedral lattice)** and **Family 1 (woven strapwork)** both inscribe one
  symmetric pattern per face (§3). A maclado field has *no* single per-face pattern and *no* global
  symmetry to inscribe against — so neither family can express it, at any parameter setting.
- **Family 3 (this doc): a placed-wheel field with a filler-closure solver.** Wheels are placed on
  the sphere by an explicit rule; overlapping wheel rims are welded; the leftover regions are closed
  by filler tiles chosen to stay whole; ribbons are threaded with globally-consistent parity; the
  result is welded and mesh-gated. It reuses §3's tail and nothing of §3's head.

The honest crux, stated up front and expanded in §6: **the placement rule is ours, not the maker's.**
His exact rule is unretrievable, so Family 3 cannot be validated by *matching his object*. It is
validated instead by the *property* his object has — every filler whole, every ribbon closed, one
watertight manifold — which is why §5's validators are the real specification.

---

## 5. The construction family

The pipeline is five stages. Each names what it produces and, where it makes a claim that can be
false, ships a `**Validator:**` with an asserted PASS and the *hard* FAIL that would otherwise slip
through.

### 5.1 Wheel generation — the numeric nonagon and its rosette

A wheel is a 9-pointed star rosette inscribed in a bounding cell by the polygons-in-contact (PIC)
rule: a contact point on each cell edge, two rays grown at a **contact angle** θ, star motifs where
rays meet ([survey §4/§5](research/maclado-orb-survey.md)). The nonagon is **not**
compass-straightedge constructible (9 = 3², Gauss–Wantzel; survey §5), so its 20°/40° geometry is
produced numerically — θ = 2πk/9 by direct trig — and there is no exact construction to check
against.

**Default:** the rosette contact angle is a per-star knob; the sketch's starting mid-value is
`contact 0.5` — the median-line case of Hankin's PIC construction as formalised by [Kaplan's PIC
paper](https://cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2005.pdf), i.e. the contact point at
the edge midpoint. The engine exposes θ per wheel rather than baking one value, and the calibration
of a *preferred* θ for the 9-star is deferred to a render sweep, not asserted here — 0.5 is the
neutral starting point, not a claimed optimum.

**Validator:** a generated wheel is accepted only when its nine outer points return to the start
under nine successive 2π/9 rotations, each vertex closing on its predecessor within the weld
tolerance — angular closure, since there is no constructible reference.
PASS: a θ = median 9-star built from `patternCorner`-style numeric angles — nine points, closure
residual below the weld tolerance.
FAIL: a wheel whose ray count is set to 9 but whose angular step is mistakenly 2π/8 — it closes
into an 8-star with a ninth point landing off the rim, caught because vertex 9 misses vertex 0 by
one step-width even though the *point count* is nine. (A count of points cannot discharge closure —
the hard case is right-count, wrong-step.)

### 5.2 Placement and overlap — the maclado move

Wheel centres are placed on the sphere by an explicit, documented rule (§6: ours, a heuristic, not
the maker's). Adjacent wheels **overlap at the rim**: a shared rim arc is welded so a ribbon entering
one wheel continues into its neighbour. Because the field is not symmetric, placement is a search,
not a formula — the rule proposes centres and the closure/parity validators (5.3, 5.4) reject
placements that cannot be closed with whole fillers.

**Validator:** two wheels are accepted as *joined* only when the contact points of their overlapping
rim arcs coincide pairwise within the weld tolerance, so the welded seam carries the ribbon through.
PASS: two 9-wheels placed with a shared edge whose per-side contact points match — the seam welds to
a single ribbon crossing.
FAIL: two wheels whose *centres* are the correct geodesic distance apart but whose rims are rotated
out of phase, so total overlap area is right while **no** contact point pairs — an area/distance
check passes, the pairwise-coincidence check catches the phase error. (Aggregate overlap cannot
discharge a per-contact-point claim.)

### 5.3 Filler closure — the invariant the whole object exists to protect

The regions left between placed wheels are closed by filler tiles. The maclado thesis is that these
stay **whole** — congruent to a small set of canonical filler polygons up to rigid motion — because
symmetry was sacrificed to keep them so. This is *the* property to verify, and it must be checked
**per filler**, because an aggregate cannot see one stretched tile.

**Validator:** a placement's fillers are accepted only when **each** filler region is congruent to a
canonical filler polygon within tolerance — every edge length and interior angle of that filler
matching the canonical template, checked tile by tile.
PASS: a placement whose every filler, individually, matches one of the canonical templates (edge and
angle residuals below tolerance for all of them).
FAIL: a placement where one filler is stretched — its edges deviate — while the **total filler area
and the filler count are both unchanged**, so an area sum or a tile count passes and only the
per-tile congruence check fires. (This is the repo's standing lesson made concrete: an aggregate
cannot discharge a claim about every part — `lego-lab-design.md` §14's one-reversed-triangle case.)

### 5.4 Ribbon parity — the over/under must close

The strapwork ribbon alternates over/under at each crossing; on a closed surface every closed ribbon
must return to its starting over/under state, which holds iff the crossing graph is consistently
2-colourable ([survey §5](research/maclado-orb-survey.md), flagged there as an engine invariant to
verify, not a sourced theorem). The existing woven family solves 2D crossing parity
(`bikar:packages/core/src/kernel3d/weave.ts`), but its solver carries a **valence contract that is
the real transfer condition** (§3): its crossing detector accepts only degree-2 and degree-4 nodes
and throws on anything else. The maclado crossing graph spans wheel–filler seams and can produce
degree-6 nodes where three ribbons meet, so parity transfers to the *welded* graph only if the
placement/closure stages guarantee every welded node is 2- or 4-valent — otherwise the solver must
be generalised past its degree-4 assumption. This condition, not just "solve it on the welded graph",
is what M4 must establish (§9.3).

**Validator:** a woven maclado orb is accepted only when its crossing graph 2-colours consistently;
an odd cycle is surfaced as an error naming the offending ribbon, never silently flipped.
PASS: a placement whose welded crossing graph is bipartite — every closed ribbon returns to its
start state.
FAIL: a placement producing one odd cycle across a wheel–filler seam — the build errors with the
strand identified, rather than emitting a ribbon that reverses over/under mid-run. (The woven
family's existing "surface, don't hide" rule for parity cycles, extended to the seam graph.)

### 5.5 Weld and manifold gate — reused unchanged

The placed rims, fillers, and ribbons are extruded to a shell and welded with the existing global
vertex pool (`bikar:packages/core/src/kernel3d/weld.ts`, tolerance 1e-3), then held to the existing
manifold gate (`bikar:packages/core/src/kernel3d/solidify-lattice.ts`): every directed edge paired,
signed volume positive, and — for the woven variant — Euler characteristic 0.

**But the existing gate is purely combinatorial, and that is a real gap this family must close.**
The woven family already exploits it: its strand sweep builds each ribbon as a *separate* closed
torus with no welding, and its own docstring notes that "interpenetrating over/under tubes can never
fuse" — the tubes are left overlapping and the *slicer* fuses them at print time, choosing
2·amplitude < depth so they touch. Two interpenetrating closed tori each have every edge paired,
Euler 0, and positive volume, so the combinatorial gate **passes them** — it never computes a
geometric union or tests self-intersection (verified: no such test exists in the orb path). For the
woven orb that is acceptable-by-design; for a maclado field, whether overlapping-and-slicer-fused is
acceptable or whether the ribbons must be *geometrically* fused into one solid is an open decision
(§9), and if the latter, a **new** self-intersection / boolean-union check is required — it is not
reused.

**Validator:** the emitted maclado mesh is accepted only when it is a single closed, consistently
wound 2-manifold — every directed edge paired, signed volume positive, Euler 0 for the woven variant.
PASS: a two-wheel-plus-filler patch whose extruded shells weld into one closed surface — all edges
paired, one shell.
FAIL: the same patch emitted with a filler band left as an *open* strip — its free boundary leaves
unpaired directed edges, which the edge-pairing check reports even though the rest of the patch is
closed. (This is the case the combinatorial gate *does* catch; the case it does **not** catch —
two interpenetrating *closed* bands — is exactly why the paragraph above calls for a new
self-intersection check rather than claiming this gate already rejects band-soup.)

---

## 6. What is NOT retrievable — and why that shapes the whole design

This section is not a caveat; it is a design constraint, carried verbatim from the survey's K1
qualifiers ([survey §3](research/maclado-orb-survey.md)).

1. **Martín López's exact 9-SPIKE placement rule is not retrievable.** The specific object was found
   on no web-indexed page; his active channel is Facebook, which is not indexed and was not
   fetchable. His wheel count, filler scheme, and parity rule for *this* sphere could not be
   obtained. **Consequence:** Family 3's placement rule (§5.2) is **ours** — a documented heuristic —
   and the doc must never claim to reproduce his method. It builds a faithful 9-fold object *in the
   same spirit*.
2. **The indexed record is ten-fold and "regular."** The reachable sources describe Martín López's
   *lazo diez* (ten-fold) and *regular* cupolas; the target is nine-fold and explicitly *non-regular*.
   The 9-fold maclado is thus later or parallel work on the evidence reachable here — the doc asserts
   no continuity it cannot source.
3. **The UPM strapwork-dome co-author "Ángel María Martín" is probably, not certainly, the same
   person** (the surname is dropped in the byline). Treated as probable.

Because of (1), **validation-against-his-object is impossible**, and that is exactly why §5's
validators check the *property* his object has (whole fillers, closed ribbons, one manifold) rather
than a resemblance. The invariants are the specification. This is the robustness-over-ease call made
explicit: the cheap path — eyeball it against a photo — verifies nothing we can gate, so it is not
offered.

---

## 7. Print constraints

Kept light; the repo's print-validation research covers overhang and tolerance. Two constraints are
specific to a thin ribbon sphere.

**Default:** the ribbon cross-section targets the upper end of the FDM thin-wall range — a wall of
about 2.0 mm, within a [1.2–2.5 mm band for a ~0.4 mm
nozzle](https://www.raise3d.com/blog/3d-printing-wall-thickness/) — because a strapwork ribbon is an
*unsupported* thin wall over most of its length, so it sits above the 0.8 mm supported-wall floor.
K10 condition (carried from [survey §6](research/maclado-orb-survey.md)): this is nozzle-relative and
transfers only for ~0.4 mm-class nozzles; a 0.2 mm or 0.8 mm nozzle shifts the floor and the print
sheet must state the assumed nozzle. This number is a starting geometry, not a measured result —
there is no printer in the loop yet (task #10 is on hold), so it will graduate to a calibrated bet
only after a physical coupon, not before.

The mesh must be a single watertight manifold to slice reliably (survey §6); §5.5's gate is that
check, and it is the first thing to run on any emitted maclado orb.

---

## 8. Milestones — each states what it verifies

Every milestone lands in bikar first (branch → PR → merge), then surfaces in 3d-models (`.bkr` +
gallery + use-case map) once it produces a mesh. The ordering front-loads the parts that can *fail
the concept*, so a dead end is found cheap.

- **M1 — one wheel, numeric.** The rosette generator (§5.1) on a sphere: one 9-star, extruded,
  welded, mesh-gated. *Verifies:* the numeric nonagon closes (5.1's validator) and a single 9-wheel
  is a watertight shell. Proves the star before the field.
- **M2 — two wheels, overlapped and welded.** Placement + rim overlap for a pair (§5.2). *Verifies:*
  the join validator — contact points pair, the seam carries one ribbon. Proves the maclado weld
  before the closure solver.
- **M3 — the filler-closure solver (the hard part).** Close the region between placed wheels with
  whole fillers (§5.3). *Verifies:* the per-filler congruence validator on a real patch. This is the
  milestone most likely to be hard or to need the placement rule reconsidered; it is scheduled early
  for that reason.
- **M4 — the full field + ribbon parity.** Place the whole sphere and thread the woven ribbon (§5.4).
  *Verifies:* global 2-colourability, and one watertight manifold over the whole sphere (5.5).
- **M5 — print + gallery.** A `.bkr` source, an STL through the mesh gate, a gallery entry, a
  use-case row, and a print sheet stating the nozzle (§7). *Verifies:* the end-to-end path a visitor
  and a printer actually use.

The gate on advancing past M3 is a decision point, not a formality: if no placement rule the survey
permits yields whole fillers with a closable ribbon, the honest outcome is to record that in the
decisions log and stop at a documented partial, not to ship a distorted-filler orb that fails its own
§5.3 validator.

---

## 9. Open questions and risks

1. **The placement rule itself (highest risk).** We are inventing what §6 says we could not read.
   The search may not converge to whole fillers on a full sphere; M3 is where that is discovered. The
   fallback is a documented partial (a patch, not a sphere), not a relaxed validator.
2. **Filler congruence tolerance.** §5.3 checks "congruent within tolerance"; the tolerance is a
   knob that trades printability against strictness and must be set from a render sweep, then
   recorded — it is not asserted here.
3. **Parity on an asymmetric field.** The woven family's parity solver assumed per-face structure;
   whether it extends cleanly to an arbitrary welded seam graph (5.4) is unproven until M4.
4. **The θ preference for a 9-star** (5.1) is deferred to a sweep; the doc exposes θ but does not
   claim a best value.

---

## Appendix A — DSL sketch (illustrative, not final)

Family 3 needs new grammar: the current `orb` block is closed at seven statements with a Platonic
base (§3), so a maclado orb is expressed by a new base mode plus placement/closure statements, while
reusing `radius`, `project`, `struts`, and `weave` from the existing block.

```bkr
orb Maclado-9
  base wheelfield                 # NOT a Platonic solid — a placement seed
  radius 60                       # mm
  wheel Star-9 contact 0.5        # the 9-star rosette + its PIC contact angle θ
  place rule spiral seeds 32      # OUR documented heuristic (§6), not the maker's rule
  fill auto                       # the filler-closure solver (§5.3); errors if no whole-filler close
  weave crossing alternating amplitude 1.0   # Family-1 ribbon (amplitude is required by the parser); omit → pierced lattice
  struts width 2.0 depth 2.4      # unsupported thin-wall target (§7)
  project spherical
```

`wheelfield`, `wheel`, `place`, and `fill` are new; `radius`, `weave`, `struts`, and `project` are
the existing orb statements. The `place rule` names the heuristic explicitly in the source, so the
one thing we invented is the one thing the reader sees first.
