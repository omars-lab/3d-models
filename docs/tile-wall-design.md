# Tile + Wall Layout DSL — design doc (pre-implementation)

Status: **DRAFT v1 — grounded in a tiling-craft + interlocking-panel field survey
(§2, sources in Appendix A). No implementation yet.**
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
3. **Connectors that survive physics**: face-registering (lippage), zero-strain at rest
   (creep), compliant in the field interior (thermal movement), calibrated per printer
   (fit), printed in the right orientation (layer shear).
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
- **Lippage control**: leveling-clip systems work by bridging **both front faces** across
  the joint and clamping them flush against one rigid bridge — registration is
  face-to-face, independent of substrate and tile-back irregularity. FDM tiles bow
  0.2–0.5 mm over 100 mm, so back-registration alone leaves visible steps in raking light.
- **Retention vs creep**: LEGO-class interference (±0.02 mm sensitivity) is 10–20× beyond
  FDM tolerance — printed retention must come from compliant geometry or separate
  reprintable clips, and **any clip that holds by sustained spring deflection creeps loose
  in PLA within months**. Shipping print ecosystems (Multiboard) default 0.25 mm clearance
  and expose per-printer tolerance offsets; garage-tile joints are deliberately loose and
  compliant so fields survive thermal cycling.
- **Holes crack edges**: the ceramic rule is ≥12.7 mm (ideally 20–25 mm) from any edge;
  snap arms need 50% tip taper, root fillets ≥0.5× thickness, and **layer lines along the
  arm** — a vertically printed snap arm delaminates on first flex.
- **Hanging is a pull-out problem, not a weight problem**: a 100 mm PLA tile is 30–80 g;
  drywall anchors derate 30–50% in tension, z-clips need 19 mm top clearance, keyholes for
  a #8 screw want ~⌀9 mm entry, 4×8 mm slot, ≥4 mm collar.

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
  mount keyhole grid every 600 anchors drywall-toggle
```

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
| `clipseat` + `CornerClip` | corner registration + lippage control | face-registering bridge (§4); zero-strain detent; PETG-only spring |
| `pinloop` | field-interior joints | deliberately compliant (garage-tile lesson): locates, permits sub-mm slide |
| `dovetail` | rigid perimeter/frame joints | 0.25 mm/side default; sliding fit |
| `magnetpocket d h` | removable tiles | auto −0.1 mm interference + glue note |
| `snap` | cantilever catches | macro-generated: 50% tip taper, ≥0.5×t root fillet, refuses vertical print orientation |

**Joint placement rule (validator)**: field-interior joints must use compliant types;
rigid types allowed only on perimeter/mount edges; rigid runs break every ~10 modules.

## 4. The corner clip (the one part designed in full here)

Synthesis of the leveling-clip mechanism with permanence and creep constraints:

- **Two parts**: a `clipseat` — a shallow open recess crossing the joint on the tile
  *backs* at each corner — and a `CornerClip` X-bridge that drops in from behind and
  rotates ~30° to a **detent** (bayonet action), whose four arms end in jaws that wrap the
  tile edge and bear on the **front border band**. Clamping front-face-to-front-face
  across one rigid bridge is the leveling-system trick, made permanent and hidden: the jaw
  lands on the 5 mm border, flush in a 0.6 mm face rebate, invisible at the grout line.
- **Zero-strain at rest**: the detent is past-center — engaged, the clip sits unstressed
  and holds in shear/bearing. No sustained deflection → no creep loosening (the failure
  mode that kills spring clips in month 3). Spring flex happens only during the engage
  twist; the clip prints in PETG, arms in the XY plane.
- **Capture depth** ≥ 2× expected warp (default 1.0 mm for 0.2–0.5 mm FDM bow) so bowed
  tiles are pulled flush rather than un-capturable.
- **Validators**: continuous flat border ≥ 4 mm wherever a clip lands (no lattice void
  under a jaw); recess floor ≥ 3 perimeters under clamp loads (the ceramic "cracked corner
  under the clip" failure); `PLA + sustained-deflection` connector → compile ERROR.
- Cropped corners (angle ≠ 90°) get no corner clip — they are perimeter edges and mount
  instead (matching how tilers treat cut edges).

## 5. Movement and environment (compile-time physics)

- **Gap formula**: `gap ≥ 3 × profile.dimensional_tolerance + α·module·ΔT_design` —
  for ±0.1 mm FDM, PLA, 100 mm module, 15 K swing: 0.3 + 0.12 ≈ **0.5 mm floor**;
  default `gap 1.2` reads as a grout line and doubles the margin.
- **Perimeter clearance** ≥ 5 mm to walls/ceiling/trim (scaled-down garage-floor rule).
- **Environment gates**: `near_radiator`/`sunlit` with PLA → ERROR "creep: use PETG or
  annealed PLA" (ambient ≥ 40 °C accelerates creep; Tg 55–65 °C is permanent sag);
  `sustained_stress` features cross-check `ambient_max`.

## 6. Mounting

- `mount keyhole screw no8` emits the parametric keyhole: entry ⌀ = head + 1 mm (~9 mm),
  slot = shank + 0.5 mm (4 × 8 mm), cavity = head height + 0.5 mm, ≥4 mm collar behind,
  margin rule applies.
- **Anchor budget validator**: field weight × 2–3 safety factor vs anchor rating derated
  30–50% for pull-out (clip moments pull, not hang); per-substrate table
  (drywall-plastic 5–20 lb … toggle 75–150 lb). ERROR when demand exceeds supply;
  command-strip mounting WARNs above 2 strips-worth per tile.
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

## 8. Validator summary (craft → compiler)

| Check | Severity | Source rule |
|---|---|---|
| crop fragment < 0.5 module | WARN (ERROR on focal edge) | sliver rule |
| hole/recess < 6 mm from edge or void | ERROR | ceramic drill rule |
| no 4 mm flat band under a clip jaw | ERROR | leveling-clip bearing |
| rigid connector in field interior / rigid run > 10 modules | ERROR | thermal buckling |
| gap below formula floor | ERROR | ANSI 3× + CTE |
| perimeter clearance < 5 mm | WARN | floating-field rule |
| PLA + sustained deflection / hot environment | ERROR | creep |
| snap arm printed vertically | ERROR | layer shear |
| anchor demand > derated supply | ERROR | pull-out budget |
| clip capture < 2× expected warp | WARN | FDM bow |

## 9. Phasing (rides the composition ladder)

- **W1** (with C1): `tile`, `wall` grid + centered/quartering layout, `crop clip`, SVG
  wall render, margin + sliver validators. Deliverable: printable 2×2 wall of nail-hole
  tiles + layout report.
- **W2** (with C2): connector library + coupons (fit step gauge, clip coupon: two dummy
  corners + one CornerClip), Lab instanced preview, keyhole mounts. Deliverable: four
  tiles clipped into a square hanging on one screw. Prototype catalog gains fit-coupon and
  clip-coupon entries; their measurements calibrate the printer profile and warp default.
- **W3**: anchor/movement/environment validators, `vary`/`checker`, story pole, chirality
  report, `crop stretch`. Deliverable: a real hallway wall spec compiling to a full BOM.

## 10. Open questions

1. Is the 0.6 mm front rebate for the clip jaw acceptable on the art face, or should v1
   clips bear on the border band *without* a rebate (slight 1-layer proudness at corners)?
2. `checker` with two tile types requires identical border/connector geometry — enforce by
   construction (shared `border` spec) or validate per pair?
3. Do cropped edge tiles keep their relief clipped mid-motif, or should the border band
   thicken to absorb the cut (tiler's trim strip, in-language)? Leaning: offer both,
   `crop clip | crop clip with frame`.

## Appendix A — survey sources (kept on file)

The full URL-annotated research report is checked in at
[`research/tile-craft-field-survey.md`](research/tile-craft-field-survey.md) — every rule
in §2/§5/§8 traces to a linked primary source there. Headline sources:

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
  [keyhole slot dimensions (Printables 146312)](https://www.printables.com/model/146312-keyhole-slot-for-wall-hanging);
  anchor pull-out deratings and z-clip/acoustic mounting are sourced in the research
  file's §5, creep literature in its §7
