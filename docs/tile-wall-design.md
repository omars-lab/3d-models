# Tile + Wall Layout DSL — design doc (pre-implementation)

Status: **DRAFT v2 — grounded in a tiling-craft + interlocking-panel field survey
(§2, sources in Appendix A) and revised after an adversarial grounding audit
([`research/tile-wall-grounding-audit.md`](research/tile-wall-grounding-audit.md);
counter-evidence and divergences in Appendix B). No implementation yet.**
v1→v2: connectors became opt-in (`connect none` default), the clip's "zero-strain" claim
became "low-preload" with prior art cited, the PLA rule's rationale moved from
creep-loosening to embrittlement-on-flex, and three unsourced numbers were fixed or
demoted to labeled placeholders (bow band, magnet interference, keyhole slot).
Scope: `tile` (flat decorative pieces with pattern relief, mounts, and connectors) and
`wall` (grid layouts over a boundary with crop, per-instance variation, movement rules,
and mounting budgets), plus the connector library and the compile-time validators that
encode what tile setters and interlocking-panel products learned the hard way.

Builds on: `piece-composition-design.md` (a `tile` is a `piece` specialization; connectors
consume its port/contract machinery and fit-by-intent model). Sibling:
`print-validation-design.md` (every tile and connector passes the print gate).

---

## 1. Goals

1. **Walls are declared, not tiled by hand.** One `wall` block: boundary, module, gap,
   layout policy — the compiler produces every full tile, every cropped edge piece, the
   connector count, and a layout report.
2. **The craft is in the validators.** Centuries of tiling doctrine and a decade of
   interlocking-plastic failures (§2) become compile-time errors and warnings, not
   forum-post surprises after twenty tiles are printed.
3. **Connectors are opt-in, and survive physics when chosen**: the default wall has no
   tile-to-tile connection at all (`connect none` — see Appendix B.1 for why); when
   enabled, connectors are face-registering (lippage), low-preload at rest (creep and
   embrittlement), compliant in the field interior (thermal movement), calibrated per
   printer (fit), printed in the right orientation (layer shear).
4. **Preview before plastic**: flat SVG wall render (pattern continuity, qiyas-checkable),
   Lab instanced 3D preview, and dry-fit artifacts (story pole, layout report).

Non-goals (v1): non-rectangular tile modules (hex/girih-shaped tiles — grammar reserves
room, v1 ships squares), floors (walking loads), exterior installs, kinematic connectors.

## 2. What the field survey established (the load-bearing facts)

- **Layout doctrine**: set out from the wall center so perimeter cuts balance; if edge
  cuts come out under **half a module**, shift the grid half a module ("quartering") —
  slivers put a joint against the wall where every waviness reads. Focal planes get full
  tiles; cuts hide at the back/bottom rows.
- **Gaps are engineering, not looks**: ANSI sizes grout ≥3× tile dimensional variation,
  never <1.6 mm; fields need movement joints; **PLA moves ~10× more than ceramic**
  (CTE ~70–80 vs 4–14 ppm/K — a rigidly linked 1 m PLA run over a 20 °C swing grows
  ~1.4 mm), which is exactly why interlocking garage floors buckle in sun and mandate
  6–13 mm perimeter gaps. PLA creeps measurably above ~40 °C ambient; Tg 55–65 °C.
- **The dominant successful practice uses no connectors at all**: commercial 3D wall
  panels (Art3d PVC/plant-fiber, sold by the millions of sq ft) and nearly every printed
  hex-panel system on Printables mount each tile independently — glue-up or command
  strips, zero tile-to-tile connection. This is the counter-position our connector
  design must answer, and it sets our default (§3.2, Appendix B.1).
- **Lippage control**: leveling-clip systems level by clamping across the joint against
  one rigid bridge — registration is face-to-face, independent of substrate and
  tile-back irregularity (mechanism inferred from leveling-system descriptions; see
  survey errata). Large flat FDM parts are reliably non-flat: reported deviations range
  from near-zero to 1–3 mm depending on geometry, bed, and material (Prusa forum
  reports; Alsoufi & Elsayed 2017). **0.2–0.5 mm over 100 mm is our working placeholder
  until the W2 clip coupon measures it per printer** — so back-registration alone risks
  visible steps in raking light.
- **Retention vs creep vs aging**: LEGO-class interference (±0.02 mm sensitivity) is
  10–20× beyond FDM tolerance — printed retention must come from compliant geometry or
  separate reprintable clips. The PLA hazard for spring parts is twofold and the
  *better-sourced* half is not creep: PLA physically ages at room temperature,
  embrittling within days (ductility collapses to a few percent), so an aged PLA arm
  tends to **fracture on engage/disengage flex**; separately, maintained deflection
  stress-relaxes faster in PLA than PETG (empirically, a PLA clip survived a week under
  tension with permanent set — the "loosens in months" timeline is unsourced; see
  Appendix B.3). Shipping print ecosystems (Multiboard) default 0.25 mm clearance and
  expose per-printer tolerance offsets; garage-tile joints are deliberately loose and
  compliant so fields survive thermal cycling.
- **Holes crack edges**: the ceramic rule is ≥12.7 mm (ideally 20–25 mm) from any edge;
  snap arms need 50% tip taper, root fillets ≥0.5× thickness, and **layer lines along the
  arm** — a vertically printed snap arm delaminates on first flex.
- **Hanging is an adhesive-budget problem, not a weight problem**: a 100 mm PLA tile is
  30–80 g and even a 3 m² field is 10–20 kg — one derated toggle carries the whole wall,
  so screw anchors essentially never fail on load. The *reported* failure path is
  adhesive strips (1–3 lb each, temperature/humidity-sensitive). Drywall anchors derate
  30–50% in tension (community/vendor-grade figure), z-clips need 19 mm top clearance,
  keyholes for a #8 screw want ⌀9.5 mm entry (the 3/8" woodworking standard),
  ~4.7 mm × 8 mm slot (shank + 0.5 mm), ≥4 mm collar.

## 3. Language design

### 3.1 `tile`

```bkr
tile StarTile
  outline square 100
  border 5                        # flat face band around the relief — mandatory (§4)
  inscribe Star-8
  depth 6
  mount keyhole screw no8 at centroid
  connector corner clipseat on corners
  connector edge pinloop on edges
```

A tile is a `piece` (extruded outline) whose 2D section = border band + clipped pattern
lattice. `border` is load-bearing: it is the clip seat, the hole keep-out donor, and the
edge that meets the neighbor. Holes/mounts/recesses obey the **margin rule**: ≥6 mm solid
material to the tile edge *and* to the nearest lattice void — the printed analog of the
ceramic drill rule, doubled up because relief makes local "edges" everywhere.

### 3.2 `wall`

```bkr
wall Hallway
  boundary rect 2400 x 1200       # any bikar 2D region (arch outlines welcome)
  module StarTile gap 1.2
  layout centered quartering      # center-out; auto half-module shift pass
  crop clip                       # drop | clip | stretch (piece-composition doc §3)
  vary rotate alternate 90        # or: checker StarTile RosetteTile
  focal edge left                 # full tiles + centered pattern face this edge
  environment interior            # interior | near_radiator | sunlit
  connect clips                   # none (default) | clips | full — see Appendix B.1
  mount keyhole grid every 600 anchors drywall-toggle
```

`connect none` is the default: each tile mounts independently (adhesive or per-tile
keyhole), matching the dominant successful practice for this product class. `connect
clips` activates the connector library, its validators, and the connector BOM — chosen
for removable installs, raking-light focal walls, and large fields where cumulative
alignment drift is visible. Clips are justified on *alignment* (rigid printed tiles do
not conform to wavy drywall the way foam PVC panels do), not retention.

The layout engine: anchor the grid at the boundary centroid; if any sightline-edge crop
fragment is narrower than **0.5 × module**, retry with half-module offsets per axis and
keep the best scoring layout; remaining sub-half fragments WARN (ERROR on the focal edge).
`crop clip` 2D-booleans boundary tiles (connectors falling in removed regions are dropped;
cut edges are connector-free mount edges); `crop drop`/`stretch` per the composition doc.

### 3.3 Connector library

First-class types, each a generated piece + matching tile feature, all fit-by-intent
through the printer profile:

| Type | Role | Design rules baked in |
|---|---|---|
| `clipseat` + `CornerClip` | corner registration + lippage control | face-registering bridge (§4); low-preload detent; PETG-only spring |
| `pinloop` | field-interior joints | deliberately compliant (garage-tile lesson): locates, permits sub-mm slide |
| `dovetail` | rigid perimeter/frame joints | 0.25 mm/side default; sliding fit |
| `magnetpocket d h` | removable tiles | +0.1–0.2 mm clearance + glue + entry chamfer (default; magnet-specific guides favor clearance-and-glue — pockets are printer-dependent and plated magnets chip under interference); `fit press` (−0.1 mm) available as explicit intent |
| `snap` | cantilever catches | macro-generated: 50% tip taper, ≥0.5×t root fillet, refuses vertical print orientation |

**Joint placement rule (validator)**: field-interior joints must use compliant types;
rigid types allowed only on perimeter/mount edges; rigid runs break every ~10 modules.

## 4. The corner clip (the one part designed in full here)

Synthesis of the leveling-clip mechanism with permanence, creep, and aging constraints.
This is a member of a century-old fastener class — quarter-turn/Dzus fasteners (cam ramp
+ end-of-travel detent) and bayonet mounts (rotate, retain in shear through lugs, small
spring only for anti-rattle; e.g. US4251134A) — cited deliberately, both for credibility
and for the design lesson that classic detents keep a small maintained preload
(Appendix B.2):

- **Two parts**: a `clipseat` — a shallow open recess crossing the joint on the tile
  *backs* at each corner — and a `CornerClip` X-bridge that drops in from behind and
  rotates ~30° to a **detent** (bayonet action), whose four arms end in jaws that wrap the
  tile edge and bear on the **front border band**. Clamping front-face-to-front-face
  across one rigid bridge is the leveling-system trick, made permanent and hidden: the jaw
  lands on the 5 mm border, flush in a 0.6 mm face rebate, invisible at the grout line.
- **Low-preload at rest** (not zero-strain — see Appendix B.2 for the honest version):
  the detent is past-center; engaged, the clip holds in shear/bearing and its *spring
  arms* carry no maintained deflection. But a bowed tile pulled flush stores elastic
  energy the jaws must react indefinitely; we accept this because the flattening force
  for a 100 mm × 3–6 mm tile is small, most of the stored strain lives in the thick
  *tile* (whose slow stress-relaxation flattens the tile rather than releasing the
  joint), and the clip prints in PETG. What we rule out is retention that depends on a
  *thin spring arm's* maintained deflection. Spring flex happens only during the engage
  twist; arms print in the XY plane.
- **Capture depth** ≥ 2× expected warp — keyed to the printer profile's *measured* warp
  from the W2 clip coupon, with 1.0 mm (2× the 0.2–0.5 mm placeholder bow band) as the
  fallback default until measured.
- **Validators**: continuous flat border ≥ 4 mm wherever a clip lands (no lattice void
  under a jaw); recess floor ≥ 3 perimeters under clamp loads (the ceramic "cracked corner
  under the clip" failure); `PLA + sustained-deflection` connector → compile ERROR.
- Cropped corners (angle ≠ 90°) get no corner clip — they are perimeter edges and mount
  instead (matching how tilers treat cut edges).

## 5. Movement and environment (compile-time physics)

- **Gap formula**: `gap ≥ 3 × profile.dimensional_tolerance + α·module·ΔT_design` —
  for ±0.1 mm FDM, PLA, 100 mm module: the tolerance term is 0.3 mm; the CTE term is
  **environment-gated** (Appendix B.4). For `environment interior`, ΔT_design = 5 K —
  0.02–0.04 mm, real physics but never dominant (commercial PVC 3D panels with similar
  CTE ship with no per-joint movement budget at all). For `sunlit`/`near_radiator`
  (ΔT 20–40 K) the term reaches 0.15–0.3 mm/tile and earns its keep. Floor ≈ **0.35 mm
  interior**; default `gap 1.2` reads as a grout line and triples the margin.
- **Perimeter clearance** ≥ 5 mm to walls/ceiling/trim (scaled-down garage-floor rule).
- **Rigid-run break at ~10 modules** — kept, but honestly labeled: with open 1.2 mm gaps
  and compliant field joints it is unreachable by design; it exists as a guard for
  `dovetail` perimeter runs and future gap-filling connectors, not as core indoor physics.
- **Environment gates**: `near_radiator`/`sunlit` with PLA → ERROR "use PETG or annealed
  PLA" (ambient ≥ 40 °C accelerates relaxation; Tg 55–65 °C is permanent sag);
  `sustained_stress` features cross-check `ambient_max`. Rationale for the PLA +
  sustained-deflection ERROR is **embrittlement-on-flex plus preload relaxation**, not a
  loosening timeline (Appendix B.3).

## 6. Mounting

- `mount keyhole screw no8` emits the parametric keyhole: entry **⌀9.5 mm** (the 3/8"
  woodworking standard), slot = shank + 0.5 mm = **4.7–5.0 mm** wide × 8 mm long for a
  #8's ≈4.2 mm thread OD, cavity = head height + 0.5 mm, ≥4 mm collar behind, margin
  rule applies. (v1 had "⌀9 mm, 4 × 8 mm" — a 4 mm slot is narrower than the #8 shank
  it claimed to fit; those numbers matched a #6.)
- **Anchor budget validator**: field weight × 2–3 safety factor vs anchor rating derated
  30–50% for pull-out (clip moments pull, not hang; the derate figure is
  community/vendor-grade, no standards-body source found); per-substrate table
  (drywall-plastic 5–20 lb … toggle 75–150 lb). Screw-anchor `demand > derated supply`
  is a **WARN** — at 10–20 kg field weights one derated toggle carries the whole wall,
  so the check can't realistically fire and ERROR would be theater. The **ERROR**-grade
  budget is the **adhesive-strip** path: at 1–3 lb per strip (temperature- and
  humidity-sensitive, the most-reported failure mode for this product class), a tile
  demanding more than its strip budget is a real, common failure.
- `mount cleat row` for panelized clusters (z-clip style) with the 19 mm top-engagement
  clearance check baked in.

## 7. Simulation and dry-fit artifacts

- **SVG wall render** (W1): every instance drawn flat by the existing 2D renderer —
  answers pattern continuity across joints; because it is an ordinary 2D composite,
  **qiyas can score the assembled wall** against a reference pattern.
- **Lab instanced preview** (W2): one tile mesh, N transforms, existing viewer.
- **`layout report`**: tile counts (full / cropped-left / cropped-right — **chirality-
  aware**: relief patterns are generally not mirror-symmetric, so a left-cut offcut cannot
  fill a right-cut slot unless the pattern's symmetry group says so), waste %, connector
  and anchor BOM, per-fragment printability (fragments also pass the print gate).
- **`story pole`**: a printable 1:1 strip of the module+gap pitch for on-wall dry layout —
  the tiler's story pole, printed.

### 7.1 Production reality: a wall's worth on one small printer

Bed size is a **non-constraint by design** — a `wall` is never printed as an object, only
as N independent tiles, each of which fits any bed ≥ module + brim. The design choices
that make small-printer production work are already in place, not accidents:

- **`connect none` default (B.1)**: tiles mount to the wall, not to each other, so there
  is no mechanical inter-fit between batches. Print order is free, a damaged tile is a
  one-tile reprint, and installation proceeds in courses while later batches are still
  printing — the `story pole` is the staged-install tool.
- **The gap formula (§5)** is what lets a tile printed in week 4 land on the grid laid in
  week 1: 1.2 mm swallows FDM scatter with 3× margin, so batch-to-batch drift never
  accumulates into a fit failure.
- **Identicality is the throughput lever**: the field is one sliced plate file re-run N
  times. `vary`/`checker` stays per-*type* (two designs = two plate files, not N unique
  ones), and the chirality-aware `layout report` states the total unique-STL count —
  typically one field tile plus two cropped edge types.

The real constraint is **print-hours**. Order-of-magnitude, *estimates until the W1 2×2
pilot measures a real tile* (≈100 mm relief tile: ~40–60 g, ~2–4 h at 0.2 mm on a modern
small printer):

| Field | Tiles (~101 mm pitch) | One machine, continuous | Filament |
|---|---|---|---|
| 0.6 × 0.6 m focal panel | ~36 | ~5 days | ~2 kg |
| 1.2 × 1.8 m accent wall | ~200 | ~4 weeks | ~10 kg |

Levers, in order of impact:

1. **Shrink the field, not the ambition** — a focal panel with a plain surround is how
   ceramic accent walls are installed in practice, and is ~5× fewer tiles for most of the
   visual impact.
2. **Match `module` to the bed** — 4-up needs `2·module + inter-part clearance + edge
   margins ≤ bed` (≈ `module 80` on a 180 mm bed, `module 100` on 220 mm). Re-moduling is
   a one-line change; `layout report` recomputes the whole BOM.
3. **Farm out the identical middle** — send the field-tile plate to a print service or
   makerspace farm and keep the local printer for edge tiles, coupons, and replacements.
   Mixed provenance is safe for the same reasons batches are: `connect none` plus the
   gap margin.
4. **Buy the filament in one batch** — across weeks of printing, spool-to-spool color
   drift is the visible failure mode (the direct analog of matching ceramic dye lots),
   and dry storage matters at multi-week timescales.

`layout report` should therefore grow **production metrics** in W3: plates required at
the declared bed size, spool count, and calendar estimate at N print-hours/day — the
numbers above, computed instead of estimated.

## 8. Validator summary (craft → compiler)

| Check | Severity | Source rule |
|---|---|---|
| crop fragment < 0.5 module | WARN (ERROR on focal edge) | sliver rule |
| hole/recess < 6 mm from edge or void | ERROR | ceramic drill rule |
| no 4 mm flat band under a clip jaw | ERROR | leveling-clip bearing |
| rigid connector in field interior / rigid run > 10 modules | ERROR | thermal buckling |
| gap below formula floor | ERROR | ANSI 3× + environment-gated CTE |
| perimeter clearance < 5 mm | WARN | floating-field rule |
| PLA + sustained deflection / hot environment | ERROR | embrittlement-on-flex + relaxation (B.3) |
| snap arm printed vertically | ERROR | layer shear |
| adhesive-strip demand > strip budget | ERROR | 1–3 lb/strip, most-reported failure path |
| screw-anchor demand > derated supply | WARN | pull-out budget (can't realistically fire at field weights) |
| clip capture < 2× expected warp | WARN | measured coupon warp; placeholder until W2 |

## 9. Phasing (rides the composition ladder)

- **W1** (with C1): `tile`, `wall` grid + centered/quartering layout, `crop clip`, SVG
  wall render, margin + sliver validators. Deliverable: printable 2×2 wall of nail-hole
  tiles + layout report.
- **W2** (with C2): connector library + coupons (fit step gauge, clip coupon: dummy
  corners in *both* rebate variants — §10 Q1 — + one CornerClip), Lab instanced preview,
  keyhole mounts. Deliverable: four
  tiles clipped into a square hanging on one screw. Prototype catalog gains fit-coupon and
  clip-coupon entries; their measurements calibrate the printer profile and warp default.
- **W3**: anchor/movement/environment validators, `vary`/`checker`, story pole, chirality
  report, `crop stretch`, production metrics in `layout report` (plates at bed size,
  spools, calendar at N h/day — §7.1). Deliverable: a real hallway wall spec compiling to
  a full BOM.

## 10. Open questions

1. **Decided 2026-07-27 — settle empirically in W2**: the clip coupon prints both corner
   variants (0.6 mm front rebate and no-rebate proud) and the in-the-flesh comparison in
   raking light picks the default. Neither variant is baked into the grammar before then.
2. `checker` with two tile types requires identical border/connector geometry — enforce by
   construction (shared `border` spec) or validate per pair?
3. Do cropped edge tiles keep their relief clipped mid-motif, or should the border band
   thicken to absorb the cut (tiler's trim strip, in-language)? Leaning: offer both,
   `crop clip | crop clip with frame`.

## Appendix A — survey sources (kept on file)

The full URL-annotated research report is checked in at
[`research/tile-craft-field-survey.md`](research/tile-craft-field-survey.md) — every rule
in §2/§5/§8 traces to a linked primary source there — and the adversarial grounding audit
behind the v1→v2 changes at
[`research/tile-wall-grounding-audit.md`](research/tile-wall-grounding-audit.md).
Headline sources:

- **Layout doctrine, sliver rule, quartering**:
  [Ceramic Tile Foundation](https://www.ceramictilefoundation.org/blog/tile-layout-centered-balanced-no-small-cuts),
  [Stone World](https://www.stoneworld.com/articles/95159-tile-layout-without-sliver-cuts),
  [DIYTileGuy quartering](https://www.diytileguy.com/quartering-tile-layout/)
- **Grout width / movement joints**:
  ANSI A108.02 3×-variation rule via [CTASC](https://ctasc.com/expert-answers/what-is-the-allowable-tolerance-for-tile-grout-head-joint-widths/)
  and [TileLetter](https://www.tileletter.com/about-grout-joint-width/);
  TCNA EJ171 via [Construction Specifier](https://www.constructionspecifier.com/specifying-movement-joints-and-sealants-for-tile-and-stone-reviewing-current-industry-standards-and-design-options/)
- **PLA vs ceramic movement**: CTE literature
  ([E3S](https://www.e3s-conferences.org/articles/e3sconf/abs/2018/07/e3sconf_eenviro2018_01007.html),
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9370745/),
  [Kyocera ceramic CTE](https://global.kyocera.com/prdct/fc/material-property/property/cte/index.html));
  garage-tile expansion failures
  ([AllGarageFloors](https://allgaragefloors.com/interlocking-garage-floor-tile/),
  [GarageFlooringLLC](https://www.garageflooringllc.com/expansion-and-contraction/))
- **Leveling-clip mechanics** (the front-face registration insight behind §4):
  [DIYTileGuy leveling systems](https://www.diytileguy.com/tile-leveling-systems/)
- **Precision + tolerance ecosystems**: LEGO ±0.01 mm vs FDM ±0.1–0.2 mm;
  [Multiboard](http://www.multiboard.io/) user tolerance sliders;
  [Printables hex wall panels](https://www.printables.com/model/206002-wallpanel-modular-hexagon-tiles)
- **Press-fit / snap-fit design**:
  [Creative3DP fit ladder](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/),
  [Hubs snap-fit guide](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/),
  [Qidi clearance guide](https://qidi3d.com/blogs/print-lab/3d-printed-snap-fit-joints-clearance-guide)
- **Hole placement + mounting**: ceramic drill-distance rule
  ([MyBuildingShop](https://mybuildingshop.com/blogs/mosaic-tile-news/can-i-drill-a-hole-in-ceramic-tile-without-cracking));
  [keyhole slot dimensions (Printables 146312)](https://www.printables.com/model/146312-keyhole-slot-for-wall-hanging)
  plus the [Rockler 3/8" keyhole standard](https://www.rockler.com/hanging-slot-router-bits-router-bits);
  anchor pull-out deratings are community/vendor-grade
  ([Austin Gallery](https://www.austingallery.org/blog/how-much-weight-can-drywall-hold),
  [EngineerFix](https://engineerfix.com/drywall-anchor-weight-chart-how-much-can-they-hold/),
  [Maden](https://maden.co/blogs/fastening-joining/how-much-can-anchors-hold-in-drywall-load-ratings-guide)
  — no standards-body source found); z-clip/acoustic mounting in the research file's §5
- **Corner-clip prior art** (added in v2):
  [Dzus fastener](https://en.wikipedia.org/wiki/Dzus_fastener),
  [Monroe Aerospace on quarter-turn fasteners](https://monroeaerospace.com/blog/what-are-quarter-turn-fasteners-and-how-do-they-work/),
  [Southco D2 Dzus catalog](https://southco.com/en_any_int/fasteners/emdzusemreg-quarter-turn-fasteners/emdzusemreg-turn-to-close-turn-to-open-quarter-turn-fasteners/d2-dzus-rapier-quarter-turn-fasteners),
  [bayonet-mount patent US4251134A](https://patents.google.com/patent/US4251134A/en)
- **PLA under sustained load — counter-evidence and aging** (added in v2):
  [Thrinter week-long clip creep test](http://thrinter.com/creep-abs-pla-petg-alloy-910/),
  [PLA scaffold long-term creep study](https://www.researchgate.net/publication/312872242_Long-Term_Creep_and_Impact_Strength_of_Biocompatible_3D-Printed_PLA-Based_Scaffolds),
  physical-aging papers ([Polymer 2019](https://www.sciencedirect.com/science/article/abs/pii/S0032386119310213),
  [Macromol. Chem. Phys. 2020](https://onlinelibrary.wiley.com/doi/abs/10.1002/macp.201900475))
- **Glue-up precedent for connector-free walls** (added in v2):
  [Art3d](https://www.art3d.com/) commercial 3D wall panels,
  [Stickgoo install guide](https://stickgoo.com/blogs/blogs/a-step-by-step-guide-on-how-to-install-3d-wall-panels)
- **Magnet pockets** (added in v2):
  [Kingroon magnet-embedding guide](https://kingroon.com/blogs/3d-printing-guides/how-to-embed-magnets-into-3d-prints),
  [Sovol magnet guide](https://www.sovol3d.com/blogs/news/how-to-use-magnets-in-3d-printed-models)
- **FDM warp magnitude** (added in v2):
  [Prusa forum on large flat parts](https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-how-do-i-print-this-printing-help/large-printed-parts-are-not-flat-even-though-they-dont-unstick-from-bed/),
  [Alsoufi & Elsayed 2017 warp study](https://www.researchgate.net/publication/318654219_Warping_Deformation_of_Desktop_3D_Printed_Parts_Manufactured_by_Open_Source_Fused_Deposition_Modeling_FDM_System)

## Appendix B — counter-evidence and divergences

Each entry records the strongest counter-position found by the grounding audit
([`research/tile-wall-grounding-audit.md`](research/tile-wall-grounding-audit.md)), with
either our justification for diverging or the design change it forced.

### B.1 Why connectors are opt-in (the counter-evidence won)

**Why clips at all?** The strongest counter-position deserves stating: the dominant
successful practice for lightweight decorative wall tiles — commercial PVC/plant-fiber 3D
panels ([Art3d](https://www.art3d.com/)) and nearly all printed hex-panel systems on
Printables — uses **no tile-to-tile connection whatsoever**; each tile is glued or
command-stripped to the wall independently, which tolerates wavy substrates, makes every
tile replaceable, and deletes the entire connector/tolerance/creep problem space. We adopt
that as the **default** (`connect none`). Clips are opt-in, and they are justified on
*alignment*, not retention: rigid printed tiles (unlike foam PVC) do not conform to
drywall waviness, so adjacent-tile coplanarity and gap uniformity in raking light are set
by the substrate unless something registers the faces — that is the one job adhesive
cannot do. `connect clips` is recommended only for removable installs, raking-light focal
walls, and field-of-many-small-tiles cases where cumulative alignment drift is visible.
This was v1's biggest reversal: connectors were the default; the audit's existence proof
(millions of sq ft of glue-up panels) flipped it.

### B.2 The clip is "low-preload", not "zero-strain" (prior art + an honest caveat)

The CornerClip is a member of a century-old fastener class — quarter-turn/Dzus fasteners
(cam ramp + end-of-travel detent) and bayonet mounts (rotate, retain in shear via lugs,
small spring only for anti-rattle). We cite them deliberately: the classic detent holds
its pin *under maintained spring preload*, and a truly zero-preload bayonet rattles. Our
claim is therefore **low-preload at rest**, not zero-strain: retention is in
shear/bearing through the detent, but any tile bowed by 0.2–0.5 mm that the jaws pull
flush stores elastic energy that the clip must react indefinitely. We accept this because
(a) the flattening force for a 100 mm × 3–6 mm tile is small, (b) it is the *tile*,
printed thick, that carries most of the stored strain, and its slow stress-relaxation
flattens the tile rather than releasing the joint, and (c) the clip prints in PETG, whose
relaxation at these stresses is modest. What we still rule out is retention that depends
on a *thin spring arm's* maintained deflection. (v1 claimed "zero-strain at rest" and
contradicted itself by also requiring bowed tiles to be pulled flush.)

### B.3 The PLA rule survives on different grounds

The categorical "PLA clips creep loose in months" overstates the sourced evidence: an
empirical week-long clip test (Thrinter) found a PLA clip under continuous tension still
functional despite permanent set, and PLA scaffold studies show no shape change under
sustained loads up to ~10 MPa — far above wall-tile clip stresses. The better-grounded
PLA hazard is **physical aging**: PLA embrittles within days at ambient (ductility
collapsing to a few percent), so an aged PLA spring arm is likely to *fracture during the
engage/disengage flex*, and PLA additionally stress-relaxes faster than PETG under
maintained deflection. The compile ERROR on `PLA + sustained-deflection` therefore
stands, but its stated rationale is "embrittlement on flex + relaxation of preload," and
the message offers PETG (preferred) or annealed PLA, citing the aging literature rather
than a loosening timeline we cannot source.

### B.4 The CTE term is real physics but negligible indoors

At PLA's ~68–80 ppm/K, a 100 mm tile in a heated living room (±5 °C) moves 0.02–0.04 mm —
under 4% of the default 1.2 mm gap and smaller than FDM dimensional scatter; commercial
PVC 3D panels (similar CTE) ship with only a 2–3 mm whole-wall edge gap and no per-joint
movement budget. We keep the formula because it is free and because it *does* bite where
the survey's failures actually happened — `sunlit` and `near_radiator` (ΔT 20–40 K),
where the term reaches 0.15–0.3 mm/tile. For `environment interior`, the CTE term is
computed with ΔT_design = 5 K (not 15 K) and can never dominate. Likewise the ~10-module
rigid-run break is kept but honestly labeled: with open 1.2 mm gaps and compliant field
joints it is unreachable by design; it exists as a guard for `dovetail` perimeter runs
and future gap-filling connectors, not as core indoor physics.
