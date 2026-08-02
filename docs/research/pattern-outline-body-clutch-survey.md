<!--
Provenance: adversarial research survey, produced 2026-08-02 by a Claude
Fable 5 background research agent (raw LDraw .dat downloads, web fetches,
MachineBlocks source reads), preserved verbatim per the ground-design-doc
skill; only this header and the agent's one-line lead-in were added/removed.
Feeds: docs/pattern-outline-brick-design.md (Appendix A/B.4) and the LG-B2 coupon.
-->


# Research: non-rectangular LEGO-compatible bodies and anchor-only clutch

**Provenance:** researched 2026-08-02 for the bikar pattern-outline `brick` extension (anchor-only clutch bet, `3d-models:docs/lego-lab-design.md` §3.3/§5.2, LG-B2). LDraw geometry was fetched as **raw `.dat` text** and read directly (highest confidence); web pages marked *(fetched)* were retrieved through a summarizing fetch tool — verbatim quotes are as returned by that tool; items marked *(unverified snippet)* come from search-result snippets only and were **not** fetched.

Conventions: 1 LDU = 0.4 mm; LDraw Y is down; a brick is 24 LDU tall, a plate 8 LDU; stud centres sit at (±10, ±10) LDU with stud radius 6 LDU (⌀4.8 mm); the stud-tangent plane of a 2×2 footprint is therefore at 10 + 6 = **16 LDU = 6.4 mm** from part centre — the same plane as a square brick's inner cavity wall.

## 1. LEGO's own non-rectangular parts (geometry facts, with sources)

**Headline finding: every LEGO round/cut 2×2-class part examined keeps an interior tube *and* deliberately re-introduces wall contact at the stud-tangent plane, as local flats, facets or ridges. None is anchor-only.**

### 1.1 Brick 2×2 Round (3941 "without Reinforcement"; 6143 "Reinforced")

Raw `3941.dat` + `s/3941s01.dat`:

- Outer body: `4-4cyli` scaled 20 → cylinder radius 20 LDU (⌀16 mm ≈ 8·2 − 0.2).
- Centre: full-height axle-hole column (`axlehole` scaled 20 in Y), whose bottom is a **`stud4a` open tube** at y = 20 (bottom 4 LDU) — the anti-stud is present.
- **The wall is locally squared where studs engage.** In the bottom 4 LDU (y 20–24), the four axis-aligned sectors of the wall are flat `rect` faces at |x| or |z| = **16 LDU** (`1 16 16 22 0 … rect.dat`, half-extents 2 × 11.36), i.e. **exactly the stud-tangent plane, coplanar with a square 2×2 brick's inner wall face**; the diagonal sectors remain radius-20 arcs (`1-8cyli` at (18.47759, 7.65367): √(18.47759² + 7.65367²) = 20). Above the stud zone (y 4–20) the cavity is a radius-16 circle (`4-4cylo` scaled 16), which is fine there because studs don't reach that height (a r-16 circle would intersect a stud: centre distance 14.14, 16 − 14.14 = 1.86 < 6).
- Raw `6143s01/6143s02.dat` (the reinforced, current-mould model): same flats at ≈15.83–16 LDU spanning y 20–24 (`rect3`/`rect` at (15.826, 22, ±8.096)), a taller `stud4a` tube (scaled 1.5 → bottom 6 LDU = 2.4 mm), plus four radial reinforcement ribs (`rect3` pairs at (11.8, 11.9, ±1)).

So the round brick's answer to "no continuous tangent side wall" was **not** anchor-only clutch: LEGO flattened the wall back to the tangent plane in the 1.6 mm-tall band where studs actually engage.

### 1.2 Plate 2×2 Round (4032a, with axle hole)

Raw `4032a.dat` + `s/4032s01.dat`: centre **`stud4a` tube** occupying the bottom half (y 4–8) around the axle hole, and per quarter a flat `rect` face at x = **16 LDU** spanning y 4–8 (`1 16 16 6 0 … rect.dat`) — the same four tangent flats, plus radius-20 outer arcs/chords. Same architecture as the brick.

### 1.3 Plate 2×2 Round with 1 centre stud (18674, sharing 15535's underside)

Raw `18674.dat` + `s/15535s02.dat`: centre **`stud4` tube** (outer r 8 / inner r 6 LDU) at the bottom, and a sculpted underside ring: outer skirt r 20 (`1-8cyli`), inner faces at r 16 (`1-8cylo` at (14.78207, 6.12293): √256 = 16) and r 19, with clusters of small `rect2p`/`rect3` facets at x ≈ 14.7–16.7 LDU, z ≈ ±6–13, y 5.5–7.5 — **per-stud contact patches sculpted into the curved wall around each of the four stud positions**, again straddling the 16 LDU tangent plane.

### 1.4 Plate 2×2 without corner (26601, 45° cut) — the closest analogue to an irregular outline

Raw `26601.dat`: keeps its single interior **`stud4` tube** at the centre vertex, three studs on top, and along the diagonal cut carries dedicated wall fragments in the stud-engagement zone (`box2-5` at (15.12, 6, −2.05) and (2.05, 6, −15.12), r ≈ 15.3 LDU from centre) near the two studs adjacent to the cut — the cut wall is **positioned and faceted to keep touching those studs**.

### 1.5 Dish 2×2 (2654 → 2654a; BrickLink's "boat stud" family number)

Raw `2654a.dat` + `s/2654as01.dat`: underside has four per-stud socket rims (`stud6a` + r-4 disc at each stud position) and rim facets at r ≈ 15.8–16.7 LDU — but with engagement height only ≈0.56 LDU (**0.225 mm**, vs 4–6 LDU on bricks/plates). Community reputation of dishes/boat studs as low-clutch, rotation-prone parts is consistent with that shallow engagement but was not confirmed by a fetched source *(anecdote, unverified)*. Useful as a scaling data point: **contact at the right plane but with tiny engagement height ⇒ weak clutch.**

### 1.6 Curved outlines in current moulds

New Elementary's parts review of 11381 Jaguar E-Type *(fetched)*: "Interestingly, the anti-stud on the curved corner features the same geometry as found in the updated mould for 2x2 macaroni tiles" — i.e. LEGO's current practice for clutch along a **curved** outline is a special ridged anti-stud geometry in the mould, not a bare tube.

### 1.7 Caveat on LDraw as a specification

The repo's own audit (lego-lab-design.md §3.3) already records that the LDraw library is not uniformly faithful (`733.dat`, `6934.dat` carry no anti-stud features at all). The flats reported above are consistent across four independently-authored part families and match the algebra of tangency exactly (16 LDU), so they are very unlikely to be modelling shortcuts — but no physical part was measured for this report.

### 1.8 User reports on round parts' grip

Thin. One Eurobricks thread ("Lego Pods round plate: is it removable?", 2018) mentions a round plate that can "wiggle a bit" *(unverified snippet)*: https://www.eurobricks.com/forum/forums/topic/159963-lego-pods-round-plate-is-it-removable/ . No corpus of "round parts are loose" complaints was found — which itself is weak evidence that LEGO's flat-patch solution works.

## 2. Printed irregular-outline prior art

- **MachineBlocks** (https://github.com/pks5/machineblocks, source read raw): `lib/block.scad` line 30 — "The machineblock() module can generate … classic bricks, plates, **round bricks, wedges, slopes**, liftarms, and many more." Underside clutch: tubes with `tubeWallThickness = 0.53125` mbu (constant), and **default `tubeX/Y/ZDiameterAdjustment = −0.1 mm`** plus `tubeInnerClampThickness = 0.1 mm` — i.e. the library ships with tubes pre-shrunk 0.1 mm for FDM and adds an explicit inner clamp ridge parameter. Pins (`pinDiameterAdjustment`) for 1×N. `lib/svg3d.scad` exists (extrudes an imported SVG), and `examples/` contains `round`, `wedges`, `slopes`, `text` — but **no example was found of a free-form outline body carrying underside clutch**; whether `machineblock()` can follow an arbitrary outline is unresolved (docs page says "Documentation is still under construction") *(fetched)*.
- **base-plate-outliner** (https://github.com/dlvoy/base-plate-outliner, README fetched): generates irregular-outline **baseplates** from a PNG silhouette — but by "optimally decompos[ing] the shape into rectangular baseplates"; studs-up, no anti-stud clutch claims. Prior art for *outline ≠ grid*, not for anchor-only clutch.
- Printables/MakerWorld irregular-outline bricks exist — "lego compatible bricks love heart" (https://www.printables.com/model/391289-lego-compatible-bricks-love-heart), MakerWorld "Ultimate Brick Customizer" (Brick/Wing/Curve/Round types), "Bricks Maker Customizable" — but both Printables and MakerWorld returned HTTP 403 to fetches, so **no user fit reports on irregular-outline prints could be verified** *(unverified snippets)*.
- Maker reports on FDM tubes/pins as clutch source:
  - Brick Architect, "Enhancing your LEGO Hobby with 3D printing" *(fetched)*: printed brick tubes were "shallower and misaligned"; "an official LEGO brick was able to stack on top of my printed brick but the inverse could not as the walls were to thick and the tubes were not perfectly aligned." Some printed pieces "unable to fit on original parts all together." Bars/clips print better than stud-tube interfaces.
  - PrintPal, "Design and 3D Print Your Own LEGO-Compatible Bricks" *(fetched)*: clutch comes from "wall clutch ridges and calibrated stud diameter"; "the clutch ridges are wall features and need integrity," requiring 3–4 perimeters. Notably this printed-brick design puts tuned clutch **on the walls**, not the tubes.
  - Prusa blog, "How to make 3D printed LEGO and LEGO Duplo parts" *(fetched)*: most free models have "small or no clearances whatsoever"; Prusa's own parts use thinner walls; elephant foot compensation raised to **0.4 mm**; "every 10 micrometers are important"; printed PLA blocks "connect well, but require a larger amount of force that small children may not have."
  - LDraw forum thread 28663 *(fetched)*: FDM (Bambu, 0.2 mm nozzle) prints of a Technic connector — "Fit is going to be very tight … you may end up destroying the printed part" (Orion Pobursky); finished print: "Strong clutch power. Axles and pins are hard to remove" (Jaco van der Molen). FDM error lands on the *tight* side as often as the loose side.
  - The two Printables makers reporting "The 4x2 fits ok but the 2x1 is very loose" are already recorded in `lego-lab-design.md` §3.3 (internal; not re-fetched).

**Net for §2: nobody was found who ships an irregular-outline LEGO-compatible part with tube-only clutch and reports it holding.** The printed-brick ecosystem either keeps rectangular walls, moves clutch *onto* the walls (PrintPal ridges), or pre-compensates tube diameters (MachineBlocks −0.1 mm default).

## 3. Counter-evidence: the case that the wall is load-bearing

- **US3005282A (Christiansen, filed 1958)** *(fetched)*, https://patents.google.com/patent/US3005282A/en — Claim 3: "a pair of primary projections of one block are clamped between at least one side wall and at least one secondary projection." Description: "the geometrically projected cross-section of each primary projection is tangent to at least one secondary projection **and** the inner face of at least one of the side or end walls"; the tubes "co-operate **both** with the primary projections of the adjacent block **and** with the inner faces of the side or end walls." Per the fetch: **no embodiment describes clutch from secondary projections alone**, and all figures/claims are rectangular parallelepipeds.
- **LEGO's own explanation** *(fetched)*, https://www.lego.com/en-us/service/help-topics/article/how-do-lego-bricks-work — "The tubes on the bottom interlock with the studs on top of other bricks. The studs get neatly wedged in between the tubes **and the sides** of every brick making them stick together firmly."
- **The repo's own census** (`lego-lab-design.md` §3.3, internal): wall share of clamping contacts = 100 % (1×1), **67 % (2×2), 50 % (2×4)**, 31 % (4×4), 19 % (6×6). Consistent with the patent's per-stud tangency picture.
- **Section 1 above is itself counter-evidence:** when LEGO removed the rectangular wall, it engineered tangent-plane flats/scallops/ridges back in on every part examined, rather than trusting the tube alone. For a 2×2 round part, one centre tube touches each of the 4 studs once (4 tube contacts) and the four flats add 4 wall contacts — LEGO chose to keep the wall share at ~50 % even on a round body.
- **Force-distribution measurement between walls and tubes: none found.** What exists: LEGO clutch test implements exist but disclose no numbers (Brick Architect 2021, *fetched*, explicitly numberless); a hobby estimate of "minimum realistic clutch power of a single stud is 650 grams" (lambsandwich.net, *fetched* — informal, method unclear, treat as an estimate not a measurement); the widely-cited 4,240 N figure is *compressive* brick strength, not clutch (Smithsonian snippet, *unverified*). **The 50–67 % contact-count share has never been shown to equal a 50–67 % force share — that translation is exactly what LG-B2 must measure.** (A contact against a rigid flat wall and a contact against a compliant 0.86 mm tube wall need not carry equal force.)
- Nothing credible was found asserting tubes alone hold fine at small footprints. The nearest pro-tube datapoint is the shallow-engagement dish (§1.5) — and its reputation is *low* clutch.

## 4. FDM printability of irregular outlines and inset walls

- **Elephant's foot on the outline** *(fetched)*, https://help.prusa3d.com/article/elephant-foot-compensation_114487 — first-layer perimeter shrink, "values around 0.2 mm usually work well" (Prusa's LEGO article used 0.4 mm); crucially "PrusaSlicer automatically detects thin lines in the first layer and makes sure not to over shrink them" — directly relevant to a 1.5 mm inset wall following a rosette outline (compensation eats a two-line wall unless the slicer's thin-wall guard catches it). No corner-specific (convex vs concave) behaviour documented. Root-cause fixes (Z-offset, bed temp) per Creality/3DSourced/Tom's Hardware *(unverified snippets)*.
- **Concave corners and cusps** — Arachne perimeter generator (Prusa KB, quoted in search results, *snippet*; https://help.prusa3d.com/article/arachne-perimeter-generator_352769): Arachne produces **variable-width perimeters**, so "as long as the wall thickness is close enough to 2 perimeters, PrusaSlicer will take care of the rest" — this is what saves the self-intersecting 1.5 mm inset at lobe cusps (classic mode with "detect thin walls" off simply **trims the tips of sharp corners**). Trade-off: "Arachne … has a tendency to round concave corners; … extruded plastic tends to shrink into concave corners," so rosette re-entrant corners will print slightly rounded and locally over-filled. A lobe cusp narrower than one extrusion width (0.4–0.5 mm) will be dropped or fused by either engine.
- **Seam placement on a curved perimeter** — Prusa KB "Seam position" *(snippet; the article URL that fetched 404 is superseded by* https://help.prusa3d.com/article/seam-position_151069 *)*: the slicer "is clever enough to hide the seam in corners, but cylindrical objects have no corners, so the Z-seam will always be visible"; Random position or painted seams (Seam painting, https://help.prusa3d.com/article/seam-painting_168620, *snippet*) are the mitigations. A rosette outline is actually *better* off than a circle: its concave lobe junctions are natural seam-rest corners — but the seam must be **kept off the underside clutch band** (a seam blob on a tube or a tangent facet is a local +0.1–0.2 mm interference, the same order as the entire fit window).
- Scale sanity: 16–40 mm outlines with 1.5 mm (3 × 0.5 mm) walls are comfortably within FDM practice; the fragile features are the ⌀6.5/4.8 mm tubes (0.857 mm wall — two 0.4 mm lines, below the repo's own 1.2 mm mesh-gate floor, §3.4/§7.4) and any cusp under ~1 mm.

## 5. Rotation lock on sparse anchors

- **Kinematics:** one gripped stud is a revolute joint; two gripped studs 8 mm apart lock rotation geometrically. This is standard LEGO/Technic doctrine — Technic framing is "based around a two connection point minimum … the first point allows rotation … the second point locks that angle into place" (picklebricks.com, *unverified snippet*; the underlying fact is uncontroversial).
- **But LEGO's own floor for a small round part is much higher than two tube contacts:** the 2×2 round brick/plate engages 4 studs with 1 tube (4 tube contacts) **plus** 4 tangent flats (§1.1–1.2) = 8 contacts; the corner-cut plate keeps tube + cut-wall facets. No LEGO precedent exists for a part held by exactly two tubes and nothing else.
- **What two anchors do not resist:** (a) **rocking** about the line joining the two tubes — LEGO parts resist this with wall contacts off-axis and with the bottom rim bearing on the plate below; a rosette whose outline sweeps far from the two-anchor axis has a long pry lever against zero off-axis clamp; (b) **twist compliance** — a torque T about the part normal loads each tube laterally with F = T/8 mm; each printed tube resists via a 0.857 mm-wall ring in bending, the part's most compliant feature (and the feature FDM prints worst — §2). No measurement of stud-tube torsional resistance was found anywhere *(open)*.
- Related anecdote: single-stud connections are the canonical AFOL *swivel* (turntable/SNOT technique articles, thebrickblogger.com, *unverified snippet*) — i.e. one anchor is a bearing, by community consensus.

## 6. Source list (every URL, what it actually says, fetched vs snippet)

| # | Source | Status | What it actually says (for this question) |
|---|---|---|---|
| 1 | https://library.ldraw.org/library/official/parts/3941.dat + `s/3941s01.dat` | **raw text, downloaded** | 2×2 round brick: r-20 LDU body, centre axle column ending in `stud4a` tube, four flat `rect` wall faces at 16 LDU (stud-tangent plane) in bottom 4 LDU |
| 2 | https://library.ldraw.org/library/official/parts/6143.dat + `s/6143s01.dat`, `s/6143s02.dat` | raw, downloaded | Reinforced round brick: same tangent flats (≈15.83 LDU), taller tube (6 LDU), 4 radial ribs |
| 3 | https://library.ldraw.org/library/official/parts/4032a.dat + `s/4032s01.dat` | raw, downloaded | Round 2×2 plate: centre `stud4a` tube + four flats at 16 LDU spanning stud zone |
| 4 | https://library.ldraw.org/library/official/parts/18674.dat + `s/15535s02.dat` | raw, downloaded | Round 2×2 plate w/ centre stud: centre `stud4` tube + per-stud sculpted wall facets at r 14.7–16.7 LDU |
| 5 | https://library.ldraw.org/library/official/parts/26601.dat | raw, downloaded | 2×2 plate without corner: keeps 1 tube, diagonal cut wall carries stud-zone facets |
| 6 | https://library.ldraw.org/library/official/parts/2654a.dat + `s/2654as01.dat` | raw, downloaded | 2×2 dish: per-stud sockets + tangent-radius rim facets, engagement height only ≈0.56 LDU |
| 7 | https://library.ldraw.org/library/official/p/stud4.dat | raw, downloaded | Tube primitive: outer r 8 LDU (⌀6.4 mm), inner r 6 (⌀4.8 mm), height 4 LDU |
| 8 | https://patents.google.com/patent/US3005282A/en | fetched | Clamp = stud between ≥1 side wall AND ≥1 tube; tangent to both; no tube-only embodiment; rectangular bodies only |
| 9 | https://www.lego.com/en-us/service/help-topics/article/how-do-lego-bricks-work | fetched | "studs get neatly wedged in between the tubes and the sides of every brick" |
| 10 | https://github.com/pks5/machineblocks (`lib/block.scad`, `lib/svg3d.scad`, dir listings via raw/API) | raw source read | Round/wedge/slope bodies supported; tube diameter adjustment default −0.1 mm; `tubeInnerClampThickness` 0.1 mm; no free-form-outline clutch example found |
| 11 | https://github.com/dlvoy/base-plate-outliner | fetched (README) | Irregular outlines decomposed into rectangular baseplates; studs-up only |
| 12 | https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/ | fetched | FDM tubes shallow/misaligned; printed brick accepts official on top but not vice versa; some prints don't fit at all |
| 13 | https://blog.printpal.io/design-and-3d-print-your-own-lego-compatible-bricks/ | fetched | Printed-brick clutch from wall ridges + stud diameter; ridges "are wall features," need 3–4 perimeters |
| 14 | https://blog.prusa3d.com/how-to-make-3d-printed-lego-and-lego-duplo-parts_31741/ | fetched | Elephant foot comp 0.4 mm; "every 10 micrometers are important"; PLA connects but too stiff; most free models lack clearances |
| 15 | https://help.prusa3d.com/article/elephant-foot-compensation_114487 | fetched | Default ≈0.2 mm; auto-detects thin first-layer lines to avoid over-shrinking |
| 16 | https://help.prusa3d.com/article/arachne-perimeter-generator_352769 | snippet (quoted in search) | Variable-width perimeters handle ~2-perimeter thin walls; rounds concave corners; classic trims sharp tips |
| 17 | https://help.prusa3d.com/article/seam-position_151069 (+ seam painting 168620) | snippet | Seam hides in corners; no-corner outlines always show it; painted/random seam mitigations |
| 18 | https://www.newelementary.com/2026/07/parts-review-11381-jaguar-e-type-from.html | fetched | Anti-stud on curved corner uses updated macaroni-tile-mould geometry (ridged anti-stud for curved outlines) |
| 19 | https://forums.ldraw.org/thread-28663.html | fetched | FDM Technic print: fits err tight; "Strong clutch power. Axles and pins are hard to remove" |
| 20 | https://brickarchitect.com/2021/lego-clutch-test-implements-bricks/ | fetched | LEGO clutch test rigs exist; **no force numbers disclosed** |
| 21 | https://lambsandwich.net/welcome-to-lambsandwich-net/a-comment-on-lego-clutch-power/ | fetched | Hobby estimate "650 g per stud minimum"; informal, method unclear |
| 22 | https://www.eurobricks.com/forum/forums/topic/159963-lego-pods-round-plate-is-it-removable/ | unverified snippet | A round plate that can "wiggle a bit" |
| 23 | https://www.printables.com/model/391289-lego-compatible-bricks-love-heart ; https://makerworld.com/en/models/479021-ultimate-brick-customizer-on-makerworld | 403, unverified snippets | Irregular/curved printed bricks exist; fit comments unretrievable |
| 24 | https://www.smithsonianmag.com/smart-news/how-much-abuse-can-a-single-lego-brick-take-343398/ | unverified snippet | 4,240 N is compressive failure, **not** clutch |
| 25 | https://www.picklebricks.com/post/mastering-lego-technic-essential-building-techniques-for-beginners ; https://thebrickblogger.com/2019/11/tips-for-reversing-the-direction-of-lego-studs/ | unverified snippets | Two-connection-point minimum locks rotation; single-stud = swivel |

Dead ends recorded so nobody re-walks them: `philohome.com/3dprint/3dprint.htm` 404s (Philo's printer-compatibility test page not found at that path); `bricks.stackexchange.com` is unfetchable from this tool and site-scoped search returned nothing; Printables/MakerWorld return 403.

## 7. Verdict table

| Claim | Supports | Refutes / complicates | Open |
|---|---|---|---|
| §3.3 census: wall supplies 50–67 % of clamping **contacts** on small footprints | Patent US3005282A tangency language (#8); lego.com "tubes **and** the sides" (#9); LEGO re-adds wall flats on round parts (#1–#4) | Contact **count** ≠ force share: wall is rigid, tube wall is 0.86 mm compliant — split could skew either way | No wall-vs-tube force distribution measurement exists anywhere found; LG-B2's delta-vs-control is genuinely novel data |
| "Anchor-only clutch is viable: outline need not obey the grid so long as the interface does" | Two-tube grip is kinematically rotation-locked; FDM prints often err *tight* (#14, #19); MachineBlocks ships round bodies with tube/pin clutch (#10) | **No precedent on either side of the moulded/printed divide.** LEGO's every non-rectangular part keeps tangent-plane wall patches (#1–#6, #18); patent has no tube-only embodiment (#8); printed-brick designs put tuned clutch on walls (#13) or pre-shrink tubes 0.1 mm (#10); FDM tubes are the worst-printed feature (#12) | The strongest reframe found: LEGO's flats show wall contact can be **local 1.6–2.4 mm-tall facet pads at the tangent plane**, not a continuous rectangular wall — a rosette can add tangent pads wherever its outline passes ≥6.4 mm from a gripped stud, converting the bet from "no wall" to "wall where the outline permits" |
| Two anchors suffice for rotation lock | Two grips 8 mm apart = geometric lock; Technic two-point doctrine (#25) | LEGO's smallest round part uses 8 contacts (4 tube + 4 flat), never 2; single-stud = community-canonical swivel; twist loads each 0.857 mm tube ring in bending — weakest printed feature | Rocking about the two-anchor axis under pry (no off-axis clamp) — unmeasured; no torsional stiffness data for stud-in-tube exists |
| A rosette outline with 1.5 mm inset wall is FDM-printable at 16–40 mm | Arachne variable-width handles ~2-perimeter thin walls (#16); elephant-foot comp auto-guards thin first-layer lines (#15); concave lobe junctions give the seam a corner to hide in (#17) | Arachne rounds concave corners and plastic shrinks into them (#16); cusps < ~1 extrusion width are dropped or fused; Prusa's LEGO profile needed 0.4 mm elephant-foot comp — double the default, straight off the outline (#14, #15) | Whether comp-vs-thin-wall-guard interaction preserves a 1.5 mm inset wall *following a lobed outline* — printable answer only (a CAL-* bet / LG coupon, not a doc claim) |
| "Round LEGO parts have poor grip" (would support wall-share worry) | One "wiggle" anecdote (#22); shallow-engagement dish geometry (#6) | No corpus of complaints found — LEGO's tangent-flat solution appears to work in practice | Physical measurement of a real 3941/4032 vs square 2×2 pull-off would settle it cheaply |

**Bottom line.** The census claim's *contact arithmetic* survives adversarial checking, but its force interpretation is unmeasured in every source examined — in both directions. The anchor-only bet as stated has **zero prior art holding it up and a consistent LEGO-side pattern arguing against it**; however, the same LDraw evidence that refutes "tube-only" hands the design its escape: LEGO's own non-rectangular parts demonstrate that clutch needs only **short tangent-plane facet bands where the outline crosses the stud circles**, not a rectangular wall. If the DSL extension adds an optional "tangent pad" feature (a ≤2.4 mm-tall flat at 6.4 mm from any gripped stud centre, wherever the rosette outline reaches), the piece stops being anchor-only and starts being a faithful port of 3941's trick — with the transfer condition (K10) writable: *it transfers because the pad reproduces the moulded parts' contact plane and engagement height on the same 8 mm lattice, leaving only FDM dimensional error — which the existing CAL fit-window machinery already prices.*
