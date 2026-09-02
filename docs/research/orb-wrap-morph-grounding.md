<!-- Produced 2026-09-02 by a Claude session (WebSearch/WebFetch + local bikar and 3d-models tree reads); checked in verbatim. Feeds: docs/orb-wrap-morph-design.md (every code fact and every source it cites is recorded here). -->

# Grounding: the flat→sphere wrap morph

Date: 2026-09-02. Method: the engine facts were read from the bikar tree; the two
checkouts consulted were `~/Workspace/git/bikar` (a peer's branch checkout) and
`~/Workspace/git/bikar-sweep` at `origin/main` = `52eab35`; where the two could differ
the fact is a function name and a behaviour, not a line number. Web sources were fetched
where reachable and are marked **fetched**; anything seen only in a search snippet is
marked **(unverified snippet)** and is not cited by the design doc. Sources that could
not be fetched are listed with the failure so nobody re-tries them blind.

## A. Engine facts, read from code

| # | Fact | Where | What it settles |
|---|---|---|---|
| A1 | `projectFacePolygon` lifts each pattern vertex with `lift(vertex)` into `flat` (a point on the face's chord plane of the unit solid), sets `dir = normalize3(flat)`, then draws `world = scale3(dir, R)` when `params.projection === 'spherical'` and `scale3(flat, R)` when `'faceted'`. The cull reads `d = dot3(dir, view.axis)` in both modes. | `bikar:packages/core/src/kernel3d/orb-views.ts`, `projectFacePolygon` | Both ends of the bend already exist per vertex, they are collinear with the sphere's centre, and the set of drawn polygons does not depend on which end is drawn. |
| A2 | `makeFaceLift` is barycentric for triangles and a similarity map for regular n-gons; both send pattern corner k to face corner k. The lift lands on the face plane; nothing in `face-frame.ts` normalises. | `bikar:packages/core/src/kernel3d/face-frame.ts`, `triangleLift`, `regularLift` | The "flat" end of the bend is the pattern lying on the polyhedron face, not the 2D drawing in the picture plane. |
| A3 | Every stage frame, the base frame and the shipped views pass `projection: orb.projection` — the orb's own declaration. | `bikar:packages/cli/src/index.ts`, the `projection: orb.projection` call sites | A morph frame is the first frame that would draw an orb at a projection it did not declare; that has to be a named parameter, not a flag flip. |
| A4 | All eleven inscribed orbs declare `project spherical`. The language reference: `project spherical \| faceted  # optional; default spherical`, and for wheelfields "`project faceted` (the field is born on the sphere, there is no flat …". | `bikar:patterns/Orbs/*.bkr`; `bikar:docs/language-reference.md` | Every orb that has a face lift is bent; the three wheelfield orbs have no flat end to bend from. |
| A5 | `slerp` exists in bikar for two jobs only: the camera tilt (`writeTransition`, between two view axes) and the scaffold's great-circle arcs (`orb-views.ts`). Neither interpolates a vertex between two radii. | `bikar:packages/cli/src/index.ts` `writeTransition`; `bikar:packages/core/src/kernel3d/orb-views.ts` | The word "slerp" in the task text names the camera's tool, not the vertex's. |
| A6 | `STAGE_STYLE = { silhouette: true }` and `COMPLETE_STYLE = { silhouette: true }`; stage frames also draw the scaffold, `complete` does not; the highlight fill is `#c9782e`, the placed fill `#8a8a8a`. | `bikar:packages/cli/src/index.ts`; `3d-models:.claude/gates/timelapse_gate.py` `STAGE_FILLS` | The two junction identities the design proposes are one string substitution and one element strip away from frames that already exist. |
| A7 | `timelapse_gate.py`: `STAGE_KINDS = {base, element, repeat, strand, complete}`; T2 one viewBox; T3 last frame is `complete` and equals the shipped view repainted + limb; T4 transition junctions are byte identities; T6 scaffold only on unfinished frames; T7 containment for `CONTAINED_KINDS` against the base outline with `CONTAINMENT_SLACK_MM`. | `3d-models:.claude/gates/timelapse_gate.py` | Which rules a morph frame must join, and which two it adds. |
| A8 | The page footer says, verbatim: "What this is not yet: there is no frame that shows the flat drawing bending onto the sphere." The standfirst for the cell family says "copied onto every face of … and bent onto the sphere." | `bikar:packages/lab/src/breakdown-main.ts` `provenance`; `bikar:packages/lab/src/breakdown-copy.ts` `standfirst` | The page already promises the order *copy, then bend*; the frames draw *bend, then copy*. |

## B. Manifest measurement, 2026-09-02

Read from `build/orb-breakdown/*/manifest.json` in this repo (built from the bikar ref in
`build/bikar-ref.txt`): frame-kind order per orb, `flat.relation`, and turntable
representation.

| Orb | `flat.relation` | spin | frame kinds, in order |
|---|---|---|---|
| DodecaOrb, HankinOrb, RosetteCubeOrb, RosetteOrb, StarCubeOrb, StarOctaOrb, StarOrb, StarTetraOrb | lifted | cells | base → element → repeat → complete |
| RosetteWeaveOrb, WeaveDodecaOrb, WeaveOrb | lifted | ribbons | base → element → repeat → complete → strand → complete |
| Maclado9 | preview | cells | base → element → repeat → complete |
| Maclado9Weave | preview | ribbons | base → element → repeat → complete → strand → complete |
| Maclado9Overlap | preview | ribbons | base → strand → complete |

Eleven orbs are `lifted`; three are `preview`. Transition frame counts across the
fourteen: 3, 6 or 7 (RosetteCubeOrb and StarCubeOrb 7; StarOrb and WeaveOrb 6; the rest 3).

## C. Web sources

| # | Source | Status | What it says (short) | Used for |
|---|---|---|---|---|
| C1 | https://en.wikipedia.org/wiki/Slerp | **fetched** | slerp(p₀,p₁;t) = sin((1−t)Ω)/sinΩ·p₀ + sin(tΩ)/sinΩ·p₁; Shoemake 1985; constant-speed motion along a great-circle arc. Degenerate case: "When endpoints become collinear (Ω → 0), the formula simplifies to standard linear interpolation." | Why the vertex travel is a lerp along the radius, and why calling it a slerp is not wrong so much as empty. |
| C2 | https://antitile.readthedocs.io/en/latest/gco-spherical.html | **fetched** | "Projection from Euclidean space to the sphere is literally just normalizing the vector." Downside: "shapes near the corners … bunched up; this is particularly bad for larger faces e.g. on the tetrahedron." Slerp-based alternatives "require equilateral faces and lack an analytic reverse transformation"; "no method always comes out the winner." | Names bikar's `spherical` projection (gnomonic) and its known distortion; explains why the morph does not change the projection, only draws its two ends. |
| C3 | Yang, Jenny, Dwyer, Marriott, Chen, Cordeil, *Maps and Globes in Virtual Reality*, EuroVis 2018, https://arxiv.org/pdf/1908.02088v1 | **fetched** (PDF, text extracted) | §"future work": "a prototype implementation that allows the viewer to interactively transition between exocentric globe and flat map. Due to the complexity of the transition, we allow the user to control the progress of the morphing. … We used linear interpolation to transition between the 3D position of points in the rendered textures of the source visualisation and the target visualisation. … Evaluation of this hybrid visualisation remains future work." | Precedent for interpolating 3D positions between two renderings of the same points, with user-controlled progress; **no** comprehension claim transfers, the paper makes none. |
| C4 | Heer & Robertson, *Animated Transitions in Statistical Data Graphics*, InfoVis 2007 | **not fetched** — idl.cs.washington.edu redirected to idl.uw.edu (404), the stanford.edu PDF failed on a certificate mismatch, dl.acm.org answered 403 | — | Not cited. |
| C5 | Praun & Hoppe, *Spherical Parametrization and Remeshing*, https://hhoppe.com/sphereparam.pdf | **not fetched** — over the fetch size limit | — | Not cited. |
| C6 | "Understanding Slerp, Then Not Using It", number-none.com | **not fetched** — TLS failure on both http and https | — | Not cited. |
| C7 | emergentmind.com slerp topic page; splines.readthedocs.io slerp page; Motion/Flubber SVG path-morph tutorials | (unverified snippet) | Search snippets only. The path-morph tutorials describe interpolating between two 2D shapes with a library guessing point correspondence. | Only as the description of the picture-space option the design rejects; no number or claim is taken from them. |

## D. How far each vertex travels, computed 2026-09-02

The bend moves a lifted vertex from `flat` (on the face's chord plane) to `dir` (on the
sphere), along the radius (A1). A vertex at a face corner is already on the sphere and
does not move; the face centre moves furthest, by `1 − r` where `r` is the base solid's
inradius over its circumradius. The camera is orthographic (`x = world·u`, `y = world·v`
in `projectFacePolygon`, `viewBasis` in `orb-views.ts`), so a radial move of `Δ` at angle
`θ` off the view axis shows in the picture as `Δ·sinθ` — nothing at the axis, most near
the limb. Computed from the unit-circumradius vertex sets of the five regular solids
(one face found by edge count; script in the session, values reproducible from the
standard coordinates):

| base | face | inradius/circumradius r | face-centre travel 1−r | in-picture shift at 30° off axis | at 60° |
|---|---|---|---|---|---|
| tetrahedron | 3-gon | 0.3333 | 0.6667 | 0.333·R | 0.577·R |
| cube | 4-gon | 0.5774 | 0.4226 | 0.211·R | 0.366·R |
| octahedron | 3-gon | 0.5774 | 0.4226 | 0.211·R | 0.366·R |
| dodecahedron | 5-gon | 0.7947 | 0.2053 | 0.103·R | 0.178·R |
| icosahedron | 3-gon | 0.7947 | 0.2053 | 0.103·R | 0.178·R |

Which base each lifted orb uses, read from `manifest.base` in the same build as §B:
dodecahedron — DodecaOrb, HankinOrb, RosetteOrb, RosetteWeaveOrb, WeaveDodecaOrb;
icosahedron — StarOrb, WeaveOrb; cube — RosetteCubeOrb, StarCubeOrb; octahedron —
StarOctaOrb; tetrahedron — StarTetraOrb. The same manifests show the last `repeat`
frame and the cells `complete` frame carry the same polygon count on every lifted orb
(alphabetically: 42, 21, 21, 84, 18, 36, 16, 55, 6, 18, 40), which is the count the
morph must hold constant.
