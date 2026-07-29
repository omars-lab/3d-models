<!--
  Grounding audit produced 2026-07-29 by an adversarial research agent
  (Agent tool, general-purpose) run under .claude/skills/ground-design-doc.
  Feeds: docs/lego-lab-design.md (v1 -> v2).
  Preserved verbatim, exactly as returned; the addendum below was a second
  message from the same agent after its last background researcher reported.
-->

Agent 2 (FDM printability) is still running; I have enough primary evidence to deliver. Writing up now.

# Grounding audit: docs/lego-lab-design.md

**Method note.** Everything marked *(LDraw)* was settled first-hand from the local library at `…/scratchpad/ldraw/ldraw/` with file+line quoted. Everything marked *(bikar)* was verified against `/Users/omareid/Workspace/git/bikar` at `6b38342`. Web sources were fetched, not searched-and-assumed; anything I could not open is marked. One background researcher (FDM printability / MachineBlocks source) had not returned when this was written — §(d)/(h) below rest on sources I fetched myself and are marked where thinner than the rest.

---

## Claim-by-claim verdicts

| # | Claim | Verdict | Supporting | Refuting / complicating |
|---|---|---|---|---|
| 1 | §3.1 core dims: pitch 8.0, stud ⌀4.8×1.6h, plate 3.2, brick 9.6, ceiling 1.6 | **GROUNDED** | *(LDraw)* `p/stud.dat` L18-21; `parts/3001.dat`; [ldraw.org/article/218.html](https://www.ldraw.org/article/218.html) ("1 brick height = 24 LDU", "1 plate height = 8 LDU"); [zoeblade](https://notebook.zoeblade.com/Lego_brick_dimensions.html) | Stud **height** contested: Bartneck's drawing calls **1.7**, [Brick Owl](https://www.brickowl.com/help/stud-dimensions) **1.7**, doc says 1.6 |
| 2 | §3.1/3.4 side wall (real) = **1.5 mm** | **CONTESTED** | Derivation is arithmetically correct *(LDraw)*: `parts/s/3004s01.dat` cavity `box5` at ±16 LDU vs outer `box4t` ±20 → 4 LDU = 1.6 nominal | Bartneck's measured drawing of 3001 calls wall **1.2**; [hardwareishard](https://hardwareishard.substack.com/p/lego-lore-6f8) "wall thickness of a LEGO brick is 1.2mm"; [Sather](https://medium.com/@bsather/breaking-down-the-perfect-design-of-a-lego-brick-a95000bb0a7e) "sides are 1.5mm thick" |
| 3 | §3.1 footprint = **8n − 0.2** | **CONTESTED** | [Bartneck](https://www.bartneck.de/2019/04/21/lego-brick-dimensions-and-measurements/) "There is a 0.2mm gap between bricks next to each other"; his drawing: 15.8 / 31.8 | [Brighton Toy Museum](http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions) micrometer: "consistent ~15.9mm and ~31.9mm … minus a tenth of a millimetre" → **8n − 0.1** |
| 4 | §3.2 tube OD = **6.514**, derived by tangency | **CONTESTED (arithmetic correct, grounding circular)** | Arithmetic verified by me: 10√2−6 = 8.1421 LDU → ⌀6.5137 mm. Bartneck drawing prints **Ø6.51** | Number spread 6.31 / 6.4 / 6.4537 / 6.4637 / 6.5 / 6.51 — and the two "measured-looking" endpoints are the *same formula* with different stud constants (see deep dive a) |
| 5 | §3.2 "**LEGO's nominal geometry has zero designed clearance**" | **CONTESTED — the strongest refutation in this audit** | Patent language is unhedged (verified) | [Brighton](http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions) micrometer 4.88–4.89 mm studs, "deliberately oversized … to force the mating brick's walls to flex"; [BrickNerd/NED](https://bricknerd.com/home/all-about-ned-the-lego-engineering-department-youve-never-heard-of-11-19-23) LEGO's own designers: "an **interference fit**"; [LEGO.scad](https://github.com/cfinke/LEGO.scad) subtracts explicit `stud_play = 0.03` |
| 6 | §3.2 LDraw's 6.4 is "a rounding … for clean whole-LDU primitive scaling" | **CONTESTED** | — | *(LDraw)* LDraw uses non-integer scales freely (`p/stud4s.dat` uses `0.75`, `-0.25`; `4-4ring3.dat` vertices are non-integer), so whole-LDU is not a constraint it observes; and `stud4` is placed at unit XZ scale in **3336** parts, never rescaled — it is a hard library-wide convention, i.e. the de-facto interoperable value |
| 7 | §3.2 patent quotes | **GROUNDED with three defects** | 4 of 5 quotes verbatim in [US3005282A](https://patents.google.com/patent/US3005282A/en) | Quote 5 strips "**In the preferred embodiments**"; quotes 1–2 drop "…when said cross sections are **geometrically projected normal to the bottom wall**"; **claims 1, 2 and 3 were formally disclaimed by Interlego AG, 31 Mar 1978** |
| 8 | §3.3 three-way anti-stud taxonomy (1×1 none / 1×N pins ⌀3.2 / M×N tubes) | **GROUNDED** | *(LDraw)* my sweep of all 67 plain `Brick/Plate/Tile n x m` parts: **65 conform**. `p/stud3.dat` r=4 LDU, `p/stud4.dat` r=8/6 LDU | 2 exceptions: `parts/6934.dat` (Tile 3×6, Scala) and `parts/733.dat` (Brick 10×10) have **no** anti-stud features at all |
| 9 | §3.4 tube wall 0.857 mm, below the 1.2 mm floor → §7.4 exemption | **GROUNDED** | *(LDraw + bikar)* `p/stud4.dat` wall = 2 LDU = 0.8; `kernel3d/mesh-gate.ts:10` `DEFAULT_MIN_FEATURE_MM = 1.2` | — |
| 10 | §3.5 "LEGO's clutch band is ~0.02 mm" → existing fit ladder unusable | **CONTESTED — the doc's own cited source says otherwise** | — | thewave.engineer, actually read: "The **interference between stud and tube is roughly 0.1–0.2 mm**", "designed for 2-3 Newton insertion force" — i.e. the same size as `press −0.10` and `holeCompMm 0.20`. Also 404/403: see citation table |
| 11 | §3.6 the deep cavity is a moulding artifact; FDM free to use `engage 1.6` | **CONTESTED — should change the design** | Physics half-right: a host stud is only 1.6 mm tall, so cavity depth beyond 1.6 adds **zero** stud contact *(LDraw: `3001s01.dat` tube spans y=4→24, stud occupies y=20→24)* | [Brickset](https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers): unsupported bridging strands "will not get in the way of the studs … **but it would if it was a plate or tile**". Plus tube-compliance and wall-share arguments (deep dive e) |
| 12 | §5.3 rotation lock = `studsEngaged ≥ 2`; a 1×1 "**spins freely**" | **CONTESTED on the prose, criterion sound** | [Eurobricks](https://www.eurobricks.com/forum/forums/topic/30171-1x1-brick-alignment/): "1x1 pieces are connected to other parts by only one stud and **can freely rotate around it**" | Same thread: "The bricks had a much stronger grip back then and **you sometimes couldn't rotate a 1x1 piece without taking it off**" — resistance is real, material- and tolerance-dependent |
| 13 | §5.3 grid-fit formula `1 − max(residual)/4` | **REFUTED (mechanically, by counterexample)** | — | The formula reads only `\|L₁\|,\|L₂\|` and never the angle between them. A hexagonal lattice `a₁=(8,0), a₂=(4,4√3)` has `\|a₁\|=\|a₂\|=8` → **gridFit = 1.0**, contradicting the doc's own 6-fold row |
| 14 | §5.3 table: 4/8-fold → 1.0; 6/12-fold "carries √3"; 5/10-fold "never … carries φ" | **CONTESTED (conclusions ~right for canonical cases, reasons wrong)** | √3 for hexagonal is correct | [Cromwell, *Math. Intelligencer* 31 (2009) 36–56](https://link.springer.com/article/10.1007/s00283-008-9018-6): "the rotation centres in a **periodic** pattern can only be 2-, 3-, 4- or 6-fold" — **8-fold and 12-fold are as forbidden as 5-fold**. And 5-fold Islamic designs are periodic with rectangular repeat units (deep dive f). The rhombic-lattice ratio is cot 36° = 1.3764, **not φ** |
| 15 | Novelty: nothing does pattern → LEGO-compatible printed part with a gate | **CONTESTED** | No OpenSCAD LEGO library ships a compatibility *score* | [MachineBlocks `machineblock` module](https://machineblocks.com/docs/modules/machineblock) exposes `svg` / `surfacePattern` / `text` / `baseReliefCut` — literally 2D vector pattern → LEGO-compatible printable part, today |
| 16 | §2 engine ground truth (all 8 bullets) | **GROUNDED** | *(bikar @ 6b38342)* every line/number verified — see Citation spot-check | — |
| 17 | §3.7 stock-part offset ladder (10/8/4/2 LDU), 5:2 SNOT ratio, curvature quote | **GROUNDED — verbatim** | Guide PDF L112-124, L338-340, L512 (see spot-check) | — |
| 18 | §7.5 "mirroring MachineBlocks" four offsets `studDia/wall/tubeDia/pinDia` | **CONTESTED (names wrong, count wrong)** | Four-way decomposition is a fair reading | [pks5/machineblocks `lib/block.scad`](https://github.com/pks5/machineblocks) actual names: `tubeXDiameterAdjustment`, `tubeYDiameterAdjustment`, `tubeZDiameterAdjustment` (all default **−0.1**), `studDiameterAdjustment` (**+0.2**), `baseSideAdjustment`, `baseWallThicknessAdjustment`, `tubeInnerClampThickness`. There is no `pinDiaAdj` |

---

## Counter-evidence deep dives

### (a) The tangency / 6.514 bet

**Arithmetic: I verified it and it is correct.** From `p/stud.dat` L20 — `1 16 0 0 0 6 0 0 0 -4 0 0 0 6 4-4cyli.dat` — stud radius 6 LDU. From `p/stud4.dat` L17-18, outer `4-4cyli` scaled 8, inner scaled 6 → OD 16 LDU / ID 12 LDU. Studs at the corners of a 20 LDU square are 10√2 = 14.1421 LDU from the tube axis; tangency gives 14.1421 − 6 = **8.1421 LDU = ⌀6.5137 mm**. LDraw models 8 → a **0.0569 mm gap per contact**, exactly as the survey says.

Three other tangency values in the system land on *exact* integers, which is the doc's best argument: pin r = 10 − 6 = 4 LDU (`p/stud3.dat` L18, scale 4 — exact); 1×1 cavity half-width 6 LDU (`parts/s/3070bs01.dat`: `box5` scaled `6 · −4 · 6` — exact); side wall tangent to outermost stud, `parts/s/3004s01.dat` cavity at ±16 LDU vs stud centre ±10 → 6 LDU (exact).

**But the grounding is circular, and this is the finding that most needs to land in the doc.**

- [Bartneck 2×4 brick drawing (PDF)](http://www.bartneck.de/wp-content/uploads/2019/04/lego-2x4-brick-dimensions-measurements-3001.pdf) — I downloaded and text-extracted it. Its three diameter callouts are **Ø2.6, Ø4.8, Ø6.51**, and the identical triple appears on [the 2×4 plate drawing](http://www.bartneck.de/wp-content/uploads/2019/04/lego-2x4-plate-dimensions-measurements-3020.pdf). **Ø6.51 is 6.5137 rounded to 2 dp.** Bartneck's page makes no measurement claim for 3001 and states no tolerance. This is very likely the same derivation, not independent confirmation.
- [orionrobots "Lego Specifications"](https://orionrobots.co.uk/Lego+Specifications) presents **6.31** and wall **0.657** as *verified measurements*. But 8√2 − 5 = 6.3137 and (8√2 − 5)/2 = 0.6569. **It is the identical tangency formula run with a 5 mm stud.** The 0.2 mm spread between 6.31 and 6.514 is entirely an artifact of the stud constant you choose.
- [cfinke/LEGO.scad](https://github.com/cfinke/LEGO.scad) derives the same √2 geometry and then subtracts `stud_play = 0.03` → **6.4537**. [richfelker/brickify](https://github.com/richfelker/brickify): `large_post_diameter = sqrt(2)*spacing - stud_diameter` with stud 4.85 → **6.4637**.
- Zoë Blade, Brick Owl, BrickLink, Brighton Toy Museum and Brick Architect **give no tube diameter at all**. There is no metrologically-obtained tube OD anywhere I could reach.

**Steelman of the opposing view — three independent lines, all pointing at designed interference:**

1. [Brighton Toy Museum](http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions) (403 live; recovered via Wayback): *"Almost every brick stud we measured, from 1960s sets to modern sets, was reported by the micrometer as being 4.88mm or 4.89mm… the stud size appears to be **deliberately oversized 'pragmatically' away from the official dimensions in order to force the mating brick's walls to flex to accommodate the stud, which then provides grip**."* Feed 4.88 into the doc's own algebra against Bartneck's 6.51: sum of radii 5.695 vs centre distance 5.657 → **≈0.038 mm interference per contact**, not tangency.
2. The patent itself designs elasticity in *geometrically*: *"The secondary projections may be provided with **longitudinal slits 18** … **to increase the clamping effect**."* A slit only helps if the tube must flex against an interfering stud; exact tangency between rigid parts produces zero clamping force.
3. **Draft angle.** Two sources put LEGO's draft at 0.5° ([hardwareishard](https://hardwareishard.substack.com/p/lego-lore-6f8): *"All walls of the part in the tooling direction are drafted by 0.5 degrees"*; corroborated by [Adiraj C K, LinkedIn](https://www.linkedin.com/pulse/clever-design-lego-bricks-adiraj-c-k-lssbb)). Over a 1.7 mm stud that is ~0.03 mm of diameter variation — the same order as the whole clutch effect. **A moulded stud is a truncated cone; "exactly tangent" can hold at only one height.**
4. Wall contact is not tangency either. Bartneck's drawing puts the outer wall at 1.2 and the stud centre 3.9 from the outer face → inner wall face 2.7 mm from a 2.4 mm-radius stud = **0.3 mm gap**. Real bricks bridge it with moulded splines, which is why both `LEGO.scad` (`spline_thickness`, `wall_thickness_with_splines`) and `brickify.scad` (`make_splines()`) model wall contact as a *separate rib feature*. The patent's "tangent to the inner face of a side wall" is not literally true of the part.

### (b) The anti-stud taxonomy — I tried hard to break it and mostly could not

I resolved subfile references transitively across the whole library and classified every part whose description matches exactly `Brick|Plate|Tile n x m` (67 parts, vs the 8 the doc read). **65 of 67 conform to the doc's rule.** Representative rows:

- 1×N → `stud3` only: `3004` (1×2), `3622`, `3010`, `3009`, `3008`, `6111`, `6112`, `2465` (1×16); plates `3023b`, `3623`, `3710`, `78329`, `3666`, `3460`, `4477`, `60479`; tiles `63864`, `6636`, `4162`.
- M×N → `stud4` only: `3003`, `3002`, `3001`, `2456`, `3007`, `3006`, `4201`, `4202`, `4204`, `30072`; plates `3022`…`92438`; tiles `26603`, `87079`, `69729`, `8165`, `1751`, `6320`, `48288`.
- 1×1 → nothing: `parts/3005.dat`, `parts/3024.dat`, and `parts/s/3070bs01.dat` is a bare `box5` scaled `6 · −4 · 6`.

**The two counterexamples, both real:**
- `parts/733.dat` (Brick 10×10) — a single `BFC INVERTNEXT` + `box5` cavity and 100 studs, **zero tubes**.
- `parts/6934.dat` (Tile 3×6, keyword `Scala`) — `box5` shell + `box5` cavity, **zero tubes**.

Both are old/peripheral parts and may be LDraw modelling simplifications rather than真 counterexamples — which is itself the point: **the library is not uniformly faithful, so it cannot be treated as a specification without spot-checks.** No 1×N part anywhere uses `stud4`, and no M×N part uses `stud3` — that half of the rule is airtight.

Corroborating detail the doc should add: `stud3`/`stud4` are placed at **unit XZ scale in every one of ~6,000 placements** — authors never rescale them.

**A gap the taxonomy exposes that the doc does not address.** The patent's clamping clause is *"a pair of primary projections … clamped between one secondary projection **and the inner face of an end or side wall**."* Counting contacts on the lattice:

| footprint | tube-contacts | wall-contacts | share from the **wall** |
|---|---|---|---|
| 1×1 | 0 | 2 | 100% |
| 2×2 | 4 | 8 | **67%** |
| 2×4 | 12 | 12 | **50%** |
| 4×4 | 36 | 16 | 31% |
| 6×6 | 100 | 24 | 19% |

For any small footprint the side wall does *most* of the clamping. The doc's anchor-only bet (§5.2 "candidates that fail are dropped", LG-B2 "a five-fold rosette piece anchored by two tubes") deliberately discards the half of the clamp the patent names first. Two tubes give the engaged studs 1–2 tangent point-contacts and no wall — strictly weaker than any real LEGO element.

### (c) Rotation lock

Verdict: **directionally correct, prose overstated.** [Eurobricks "1x1 brick alignment"](https://www.eurobricks.com/forum/forums/topic/30171-1x1-brick-alignment/) supplies the doc's phrasing almost exactly — *"1x1 pieces are connected to other parts by only one stud and can freely rotate around it"* — and no participant disputes it. The **same thread** supplies the refutation: *"The bricks had a much stronger grip back then and you sometimes couldn't rotate a 1x1 piece without taking it off."* So rotational resistance is a real friction quantity that varies with tolerance and material; "spins freely" implies zero.

The round-1×1-as-pivot counter-argument **does not hold**. [New Elementary on building at angles](https://www.newelementary.com/2025/03/lego-building-at-angles-escaping-grid.html) and [BrickNerd on SNOT hinges](https://bricknerd.com/home/lego-snot-hinge-techniques-and-element-design-11-28-22) discuss round plates for off-grid work but nowhere claim square 1×1s cannot rotate. Round 1×1s are chosen for **swept-volume clearance** (a square corner collides with neighbours when turned), not for lower friction. That is a geometry argument, not a friction one, so it says nothing against the doc.

No engineering measurement of single-stud torque resistance exists that I could find. Treat the quantitative side as **UNGROUNDED**.

### (d) 0.4 mm nozzle / true-scale printability

The best evidence is a **primary experiment by the doc's own cited source**, and the doc has characterised it only as "the sceptical counterweight" without reporting what it found.

[Brickset, "Can you make compatible bricks with consumer 3D printers?"](https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers) (403 to WebFetch; retrieved by curl) printed 2×4 bricks at true scale two ways — 0.2 mm nozzle / 0.1 mm layers and 0.4 mm nozzle / 0.2 mm layers:

> "Both are perfectly functional, connecting to each other, and the genuine yellow bricks. The all-important property of bricks — **clutch power — is nowhere near as good as that of real bricks**, though and, for some reason, **it was slightly better on the red bricks than the green**, which have hardly any at all."

The red bricks are the **0.4 mm** ones. **The finer nozzle produced the worse clutch.** That refutes PrintPal's "0.2 mm required for true 100 % scale" *and* undercuts the doc's Q1 fallback ("needs a 0.2 mm nozzle — which would make `studs none` the only shippable interface"). His conclusion: *"it's certainly possible to print functioning bricks but, frankly, it is not worth the time and effort."*

[Brick Architect, hosting Koen Van Der Hoeven](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/) is blunter: *"Due to the inaccuracy, even when on the best settings the **3D printed parts fail to reach the clutch power of LEGO bricks**"*, and reports an asymmetry — *"an official LEGO brick was able to stack on top of my printed brick but the inverse could not as the walls were too thick."* (Note: brickarchitect.com is live and has a real 3D-printing article — the doc's specific *2018 dimensions* URL is what 404s.)

Counter-side: [Pixenib](https://www.pixenib3d.com/can-i-3d-print-a-lego-piece/) verified verbatim — "Stud diameter: ~4.8 mm", "Tube diameter: ~4.9 mm", "Allowable clearance: 0.1 mm or less", and "With proper design, accurate tolerances, and high-resolution printing, 3D printed LEGO bricks can fit with original LEGO bricks." Note that this source, cited approvingly by the doc, **designs in 0.1 mm of clearance** — a direct contradiction of §3.2's zero-clearance premise, which the doc does not reconcile.

*(FDM repeatability-vs-accuracy numbers were delegated to a researcher that had not returned; the "calibrated repeatability may be far better than raw accuracy" line of argument is therefore **unresolved** and should be treated as an open question rather than settled either way.)*

### (e) The moulding-constraint bet — this one should change the design

The doc's physics is **half right and the half it gets right is not the half that matters.** Cavity depth genuinely adds no stud contact: from `parts/s/3001s01.dat`, `1 16 20 4 0 1 0 0 0 -5 0 0 0 1 stud4.dat` puts the tube across y = 4→24 LDU (8 mm), while the host stud occupies only y = 20→24 (1.6 mm). **6.4 mm of the tube's height touches nothing.** So "the 8 mm depth is not an engagement requirement" survives, and the uniform-wall explanation is well supported ([Protolabs](https://www.protolabs.com/resources/design-tips/improving-part-design-with-uniform-wall-thickness/), [Xometry](https://www.xometry.com/resources/injection-molding/managing-sink-in-injection-molding-designs/), [hardwareishard](https://hardwareishard.substack.com/p/lego-lore-6f8)).

**Three functional consequences the doc has mistaken for nothing:**

1. **FDM-specific, and decisive.** [Brickset](https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers), printing studs-up without supports: *"the straggly strands of filament **will not get in the way of the studs of pieces connected below it, but it would if it was a plate or tile**."* A real brick's 8 mm cavity parks the sagging bridged ceiling **6.4 mm clear** of the contact zone. `engage 1.6` puts that surface **exactly where the host studs land**. The doc's §3.6 headline — "a 9.6 mm printed piece can have a 1.6 mm cavity and an 8 mm solid ceiling" — is the *worst* case for FDM, not the free lunch it is presented as. Q4 spots the bridging but draws the opposite conclusion (that a deep cavity is the problem).
2. **Compliance.** Clutch is elastic interference, not tangency (deep dive a). A thin-walled tube is a cantilever: `k ∝ 1/L³`. Dropping the free height from 8.0 mm to 1.6 mm makes the tube **125× stiffer** (3.2 mm → 15.6×). A rigid joint at FDM's ±0.1 mm either will not assemble or will not hold — there is no elastic reserve. This is precisely Brighton's point that clutch depends on *wall flexure*, a compliance property a geometry-only gate cannot see.
3. **Wall share.** Per the census in (b), for the small footprints the doc actually targets, the side wall supplies 50–100 % of the clamping contacts — and a 1.6 mm cavity leaves 1.6 mm of wall.

The doc's own Appendix B.3 already suspects this ("A more conservative default is 3.2 mm"). The evidence says B.3 should be promoted from a contested bet to a **decision**.

### (f) Commensurability

Two separate problems.

**The formula is broken, independent of any source.** `residual(L) = 8·minₙ|L/8 − n|` consumes only the two repeat *lengths*. I ran it: a hexagonal lattice `a₁=(8,0), a₂=(4,4√3)` has `|a₁| = |a₂| = 8.0000` → **gridFit = 1.0000**, flatly contradicting the doc's own "6-, 12-fold: the repeat carries √3" row. A square lattice rotated 30° also scores 1.0. The measure must run on the repeat vectors' **components in the lattice basis** (each of `L₁ₓ, L₁ᵧ, L₂ₓ, L₂ᵧ` mod 8), not on their lengths.

**The taxonomy's reasons are wrong.** [Cromwell, "The Search for Quasi-Periodicity in Islamic 5-fold Ornament", *The Mathematical Intelligencer* 31 (2009) 36–56](https://link.springer.com/article/10.1007/s00283-008-9018-6) (full text read from the [free NWD copy](http://www.fi.uu.nl/nwd/nwd2009/handouts/tom/Islamic%205%20fold.pdf)):

> "in patterns generated by translation of a template, this symmetry must break down and cannot hold for the design as a whole. **This is a consequence of the crystallographic restriction: the rotation centres in a periodic pattern can only be 2-, 3-, 4- or 6-fold.**"

So **8-fold and 12-fold are exactly as forbidden as 5-fold**. The doc's grouping (8 with 4, 12 with 6) is not a symmetry fact; it is a fact about which *lattice* the canonical construction happens to use. Cromwell again:

> "Many of the early Islamic designs are created by arranging **6-, 8- or 12-point stars at the vertices of the standard grids of squares or equilateral triangles**. The more general rhombic lattice allows other stars to be used. An example based on {10/3} is shown… The angles in the rhombus are 72 and 108"

and, on a decagonal design:

> "The centres of the rose motifs … are diagonally opposite corners of **a rectangle that is a repeat unit for the design**."

**5-/10-fold Islamic patterns are periodic and have finite repeat units.** "Never reaches 1 at any scale" is therefore not a theorem about 5-foldness — a rectangular repeat unit with a rational aspect ratio *can* be scaled onto the grid; it is only the 72° rhombic family that cannot, and the obstruction there is cot 36° = 1.3764, **not φ = 1.618**. (Where a pattern is genuinely quasiperiodic there are no repeat vectors at all, so `gridFit` has no input and should return *undefined*, not 0.) See also [Cromwell & Beltrami, "Cognitive Bias and Claims of Quasiperiodicity in Traditional Islamic Patterns", *Math. Intelligencer* 2015](https://link.springer.com/article/10.1007/s00283-015-9538-9) *(paywalled — abstract only, unverified)*.

Also worth noting: `repeatUnitStuds` snaps at `residual < 0.2 mm` and the doc says "0.2 mm is the system's own tolerance (§3.1), so the threshold is not arbitrary." The 0.2 mm in §3.1 is an **inter-part moulding relief**, not a pattern-registration tolerance. Reusing it is a category error, and one of the two sources on it says 0.1 (claim 3).

### (g) Novelty

**The claim as implied is refuted; the conjunction survives.**

- [MachineBlocks `machineblock` module docs](https://machineblocks.com/docs/modules/machineblock) — parameters `svg`, `surfacePattern`, `text`, `studIcon`, `baseReliefCut`. **This is 2D vector pattern → LEGO-compatible printable part, shipping today.** Any auditor finds this in one search; not citing it reads as an unexamined claim.
- [dlvoy/base-plate-outliner](https://github.com/dlvoy/base-plate-outliner) — PNG → thresholded shape → rectangle decomposition → OpenSCAD → printable LEGO-compatible baseplate. No validation step.
- [bricks.lapinoo.net](https://bricks.lapinoo.net/) — draw a 2D outline, get an STL, with four fit sliders; explicitly **no** validation ("first try to print a small test brick… then adjust as needed").
- Automated *gates* exist adjacently: [Stud.io collision detection](https://studiohelp.bricklink.com/hc/en-us/articles/5412820155927-Collision) ("allows you to know whether or not parts will fit together"), [Brick-by-Brick, NeurIPS 2021](https://arxiv.org/abs/2110.15481) ("action validity prediction network that efficiently filters invalid actions"), and Legolization's stability threshold.
- [Computational Design of LEGO® Sketch Art, ACM 2023](https://dl.acm.org/doi/10.1145/3618306) and [Image2Lego](https://arxiv.org/pdf/2108.08477) are 2D-image → LEGO-layout precedents.
- Genuinely unoccupied: **Islamic geometric pattern × LEGO-compatible printed part.** Existing girih work ([Printables 780631](https://www.printables.com/model/780631-girih-tiles-for-islamic-geometric-patterns), [mathgrrl](https://mathgrrl.com/hacktastic/2016/03/girih-tiles-for-interactive-islamic-designs/)) is standalone tiles with no stud system. Lead with this.

### (h) The fit-ladder-too-coarse claim

**The doc's own cited source refutes its central number.** thewave.engineer (403 direct; retrieved via reader):

> "The frequently cited **'0.002mm tolerance' is misleading without context**. LEGO's actual **mold precision is 10 microns** … The cylindrical studs on top are 4.8mm in diameter with a tolerance of ±0.01mm."
> "**The interference between stud and tube is roughly 0.1-0.2mm.**"
> "The 0.1-0.2mm interference fit is designed for **2-3 Newton insertion force**."

The doc reads "~0.01 mm moulding tolerance" and infers a "**~0.02 mm clutch band**", then concludes the ladder (`press −0.10`, step 0.10, `holeCompMm 0.20`) is "five times the whole band" and "an order of magnitude larger". Read properly, the cited interference is **0.1–0.2 mm** — the ladder's `press` rung sits in the middle of it. §3.5's conclusion may still be right for other reasons (FDM variance, four-way decomposition), but **the arithmetic supporting it does not survive contact with its own source.** Caveat: thewave.engineer reads as SEO/AI-assisted content with no primary citations, and its 0.1–0.2 mm is an order of magnitude above the ~0.04 mm implied by Brighton's micrometer data. **Neither number supports 0.02 mm.**

Corroborating that clutch *is* achievable by calibration rather than by resolution: [MachineBlocks](https://github.com/pks5/machineblocks) ships `tubeXYZDiameterAdjustment = −0.1` and `studDiameterAdjustment = +0.2` as **defaults** — i.e. a shipping generator's baseline offsets are the same magnitude as bikar's existing ladder steps, not 5× finer.

---

## Citation spot-check results

| Cited as | Live? | Says what the doc claims? |
|---|---|---|
| [ldraw.org/article/218.html](https://www.ldraw.org/article/218.html) | 200 | **Yes.** "1 LDU = 0.4 mm", "1 brick width/depth = 20 LDU", "1 brick height = 24 LDU", "1 plate height = 8 LDU", type-1 line format, colour 16/24 — all verbatim. Caveat verbatim: *"These real world approximations are just that: approximations."* **But BFC CERTIFY CCW / INVERTNEXT are not in this document** (they live in the separate BFC spec) — survey §6 attributes them here. |
| [patents.google.com/patent/US3005282A](https://patents.google.com/patent/US3005282A/en) | 200 | **4 of 5 quotes verbatim.** Quote 3 is a paraphrase splicing claim 3's grammar onto the description's wording. **Quote 5 strips "In the preferred embodiments".** Quotes 1–2 omit the qualifier "when said cross sections are geometrically projected normal to the bottom wall". Priority 1958-01-28 (DK), filed 1958-07-28, granted 1961-10-24 — doc correct. Tube explicitly hollow. **Claims 1, 2 and 3 disclaimed by Interlego AG, 31 Mar 1978** — undisclosed by the doc. Zero hits for *clearance / slightly / approximately / resilient / elastic / friction*; 2 hits for *substantially*, neither about tangency. |
| [notebook.zoeblade.com](https://notebook.zoeblade.com/Lego_brick_dimensions.html) | 200 | **Partly.** Stud ⌀4.8, module 8, plate 3.2, brick 9.6, `(studs × 8) − 0.2` — all present. But it gives wall **1.6**, not 1.5, and **no tube diameter at all**. Survey §1's "Every one of these agrees with Zoë Blade" overstates: she does not carry the tube row. |
| [bartneck.de](https://www.bartneck.de/2019/04/21/lego-brick-dimensions-and-measurements/) | 200 | **Yes** for "There is a 0.2mm gap between bricks next to each other" (verbatim). Survey's admission that his page is an index and his figures "could not be read" is **honest but was fixable** — I extracted the drawings and they carry **Ø6.51 / Ø4.8 / Ø2.6, wall 1.2, stud height 1.7, 15.8, 31.8**. The 1.2 wall and 1.7 stud height *contradict* the doc's table. |
| [machineblocks.com/docs/calibration](https://machineblocks.com/docs/calibration) | 200 | **Procedure quote is right; the knob names are wrong.** Actual source constants are `tubeX/Y/ZDiameterAdjustment`, `studDiameterAdjustment`, `baseSideAdjustment`, `baseWallThicknessAdjustment`, `tubeInnerClampThickness` — seven, not four, and **no `pinDiaAdj`**. |
| [thewave.engineer/lego-tolerances/](https://thewave.engineer/lego-tolerances/) | **403** | **Not as claimed.** Current URL is `/articles.html/productivity/legos-0002mm-specification-…-r120/`. Content says interference is **0.1–0.2 mm**, not a 0.02 mm band; and calls the famous tolerance figure "misleading". Neither the doc nor the survey flags this source as unreachable, yet both quote numbers from it. |
| [bricksmcgee.com/…/how-are-lego-bricks-made](https://bricksmcgee.com/blogs/news/how-are-lego-bricks-made) | **404** | **Unverifiable.** Cited for "LEGO holds roughly 0.01 mm" and the ±0.02 mm consensus. Not in the survey's access-failure list. |
| Legolization — [cmlab page](http://www.cmlab.csie.ntu.edu.tw/~forestking/research/SIGA15-Legolization/) / [ACM DL](https://dl.acm.org/doi/10.1145/2816795.2818091) | **403 / 403** — I confirmed both | **Honest, and now recoverable.** The [Wayback capture](http://web.archive.org/web/20191016021839/http://www.cmlab.csie.ntu.edu.tw/~forestking/research/SIGA15-Legolization/) yields the abstract: *"our force-based metric gives 1) an ordering in the strength … and 2) a threshold for stability."* The doc's characterisation is **exactly right**. |
| Brick Architect dimensions (`/2018/the-dimensions-of-lego-bricks/`) | **404** | **Worse than link rot: zero Wayback snapshots, ever, and absent from the CDX index for `brickarchitect.com/2018*`.** The URL very likely never existed. Brick Architect *does* have a live, relevant [2023 3D-printing article](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/) the doc missed. |
| Brighton Toy Museum | **403** | **Honest, and recoverable via Wayback** — and it contains material that contradicts the doc (8n−0.1; studs measured 4.88–4.89; clutch depends on wall flexure). |
| [Unofficial LEGO Advanced Building Techniques Guide](https://joncraton.org/media/files/UnofficialLEGOAdvancedBuildingTechniquesGuide.pdf) | 200 | **Every quote verbatim.** L120 "not a simple coincidence but a will from the LEGO parts designers"; L112-118 the 5:2 ratio; L297 "aus zwei mach eins Plättchen"; L338 "jumper plate provides a 10 LDU offset, SNOTted plates provide an 8 LDU offset and the headlight brick provide a 4 LDU offset"; L512 "LEGO parts are not meant to be used to create nicely curved surfaces and you will obtain a pixelated". Best-grounded section in the doc. |
| §2 engine claims *(bikar @ 6b38342)* | n/a | **All verified.** `fit-profile.ts` L20-23 `press:-0.1, snug:0.05, sliding:0.15, free:0.35`; L77-78 `pla_calibrated 0.2 / petg_calibrated 0.25`; `mesh-gate.ts:10` `DEFAULT_MIN_FEATURE_MM = 1.2`; `protocol.ts:116` `family: 'lattice' \| 'weave' \| 'wall'`; `solidify-slabs.ts` L38-39 "a CCW outline with optional CCW hole rings", L57 "outline CCW, holes CCW"; `evaluator.ts:956` `unionPatternFaces`; every named export in `solidify-piece.ts` present with the stated constants. `docs/language-reference.md:580` "Art fills the face" verbatim. |
| Survey §6 "`parts/3068b.dat` carries the comment `0 // Patternable surface`" | n/a | **Verbatim, line 20.** |

---

## Misgrounded or missing citations

1. **`bricksmcgee.com` (404) and `thewave.engineer` (403) are quoted for load-bearing tolerance numbers but are not in the survey's access-failure list.** The survey's four declared failures all check out honestly; these two omissions are the honesty gap. §3.2's "~0.01 mm moulding tolerance" and §3.5's "~0.02 mm clutch band" currently rest on one dead link and one blocked link that says something different.
2. **The 0.02 mm clutch band has no source.** Neither cited source states it. thewave says **0.1–0.2 mm interference**; Brighton's micrometer data implies **~0.04 mm**. §3.5 must be rewritten around one of those.
3. **6.514 mm has no independent confirmation.** Bartneck's Ø6.51 is the same derivation to 2 dp; orionrobots' 6.31 is provably the same formula with a 5 mm stud. Present it as *derived*, not as a fact about LEGO.
4. **The Brick Architect 2018 URL should be deleted, not marked 404** — no Wayback record exists, so it was probably never a page. Replace with [brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/), which is live and directly relevant.
5. **Replace two dead URLs with Wayback permalinks** (Legolization, Brighton) — both are recoverable and both change the doc: Legolization *confirms* the doc's characterisation; Brighton *contradicts* §3.1/§3.2.
6. **§7.5's MachineBlocks knob names are fabricated-by-paraphrase.** Cite the real ones from `pks5/machineblocks/lib/block.scad`, and note there is no pin knob — which weakens the survey's "its `pinDiaAdj` exists as a separate knob is further confirmation of §3's three-way taxonomy."
7. **Missing prior art that an auditor will find immediately:** [MachineBlocks `svg`/`surfacePattern`](https://machineblocks.com/docs/modules/machineblock), [base-plate-outliner](https://github.com/dlvoy/base-plate-outliner), [Brick-by-Brick's action-validity network](https://arxiv.org/abs/2110.15481), [Stud.io collision detection](https://studiohelp.bricklink.com/hc/en-us/articles/5412820155927-Collision), [Computational Design of LEGO Sketch Art](https://dl.acm.org/doi/10.1145/3618306).
8. **Missing counter-sources on printability:** the Brickset article's *actual result*, and [Brick Architect / Van Der Hoeven](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/).
9. **Missing on the clutch mechanism:** [Brighton micrometer data](http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions), [BrickNerd/NED "interference fit"](https://bricknerd.com/home/all-about-ned-the-lego-engineering-department-youve-never-heard-of-11-19-23), [LEGO.scad's `stud_play`](https://github.com/cfinke/LEGO.scad), [brickify's tangency identity](https://github.com/richfelker/brickify), the 0.5° draft angle, and the 1978 disclaimer of claims 1–3.
10. **Missing on commensurability:** [Cromwell 2009](https://link.springer.com/article/10.1007/s00283-008-9018-6) and the crystallographic restriction theorem.
11. **Internal contradiction, not a citation issue but it interacts with LG-B2.** §5.2 says "a printed piece's outline is the pattern's, not a rectangle", but §7.2's partition is "one **shell ring** cell: outer outline `8c−0.2 × 8r−0.2` with the cavity rectangle as its hole". §7 describes only the rectangular case; the non-rectangular case — the one LG-B2 calls "the load-bearing bet of the whole anchor-only approach" — has no kernel description. Relatedly, `studsEngaged` is never defined for a non-rectangular outline, and §5.2 tests *anchors* against the body but never tests *studs*.

---

## Recommended doc changes

### Ready-to-paste divergence justifications

**For §3.2 — replace "zero designed clearance" (the approach survives; the framing must not).**

> **Divergence — tangency is our authoring contract, not a claim about the moulded part.** The strongest measurement-grade source disagrees with a literal tangency reading: the Brighton Toy Museum's micrometer survey reports that "almost every brick stud we measured, from 1960s sets to modern sets, was reported by the micrometer as being 4.88mm or 4.89mm", and concludes that "the stud size appears to be deliberately oversized 'pragmatically' away from the official dimensions in order to force the mating brick's walls to flex to accommodate the stud, which then provides grip." LEGO's own element designers describe the joint as "an interference fit" (BrickNerd/NED), the patent reaches for "longitudinal slits … to increase the clamping effect" — which only makes sense against an interfering stud — and moulded parts carry ~0.5° of draft, so a stud is a truncated cone for which "tangent" is undefined except at one height. **We nevertheless author to tangency, because it is the only value derivable without a metrology programme and because §8's coupon ladder sweeps ±0.15 mm around it.** What changes is the claim: tangency is our *datum*, and the printed clutch is an interference we will find empirically — not a property we inherit from the nominal geometry.

**For §3.2 / Appendix B.1 — the 6.514 number.**

> **Divergence — 6.514 is derived, not measured, and no source measures it.** The published spread is 6.31 / 6.4 / 6.4537 / 6.4637 / 6.5 / 6.51 / 6.5137 — a 0.20 mm range. Two of the values that look like independent confirmation are not: orionrobots presents 6.31 and a 0.657 wall as "verified measurements", but 8√2 − 5 = 6.3137 and (8√2 − 5)/2 = 0.6569 — the identical tangency formula run with a 5 mm stud; and Bartneck's Ø6.51 is 6.5137 to two decimals with no stated instrument or tolerance. **Our 6.514 is therefore a fact about our chosen stud diameter, not about LEGO.** We keep it as the authoring datum because 4.8 mm is the best-attested stud figure and because §3.5 shows the whole 0.20 mm spread sits inside the printer-compensation term — but the doc must stop describing it as "the exact value the patent's tangency condition forces" and start describing it as "the value our stud constant forces."

**For §3.2 — LDraw's 6.4.**

> **Divergence — 6.4 is a convention, not a rounding.** LDraw uses non-integer scale factors freely (`p/stud4s.dat` carries 0.75 and −0.25; `4-4ring3.dat`'s vertices are irrational), so "clean whole-LDU scaling" is not a constraint the library observes. `stud4.dat` is placed at unit XZ scale in **3,336** part files and never rescaled — 6.4 mm is a library-wide fixed convention encoding a 0.057 mm clearance per contact, and it is what every existing LEGO-compatible generator interoperates against. LG-F1 sweeps across both values, as B.1 already provides.

**For §3.6 / §4 `engage` — this one should change the design, not just the prose.**

> **Correction — the deep cavity is not purely a moulding artifact under FDM.** The doc is right that cavity depth adds no stud engagement (`parts/s/3001s01.dat` places the tube across 8 mm while the host stud occupies only its bottom 1.6 mm). But three functional consequences follow that the doc treated as absent. First and decisively, Brickset's true-scale print test records that unsupported bridging strands "will not get in the way of the studs of pieces connected below it, **but it would if it was a plate or tile**" — a real brick's 8 mm cavity parks the sagging bridged ceiling 6.4 mm clear of the contact zone, and `engage 1.6` puts it exactly where the host studs land. Second, clutch is an elastic interference, and a tube's cantilever stiffness goes as 1/L³: shortening it from 8.0 mm to 1.6 mm makes it 125× stiffer, removing the compliance FDM's ±0.1 mm needs. Third, on the small footprints we target, the tangent side wall supplies 50–100 % of the clamping contacts (2×2: 67 %; 2×4: 50 %), and a 1.6 mm cavity leaves 1.6 mm of wall. **Recommended: promote Appendix B.3 to a decision — default `engage` to 3.2 mm, cap the relief budget accordingly in V3, and make `engage 1.6` an opt-in that emits a WARN naming the bridging risk.** LG-F1 should carry 1.6 / 3.2 / 8.0.

**For §5.3 rotation lock — soften the prose, keep the criterion.**

> A 1×1 piece contacts a single cylindrical stud and is **not rotationally constrained by geometry** — it turns under modest applied torque, resisted only by clutch friction, which is tolerance- and material-dependent and cannot be relied upon. (Eurobricks builders report both that "1x1 pieces … can freely rotate around it" *and* that on older, tighter-tolerance bricks "you sometimes couldn't rotate a 1x1 piece without taking it off".) Because a printed part's clutch friction is *less* predictable than moulded ABS, geometric constraint is the right criterion: `studsEngaged ≥ 2`.

**For §5.3 grid fit — this is a bug, not a bet.**

> **Correction — the grid-fit residual must be computed on repeat-vector components, not lengths.** As specified, `residual(L) = 8·minₙ|L/8 − n|` never sees the angle between L₁ and L₂. A hexagonal lattice with a₁ = (8,0) and a₂ = (4, 4√3) has |a₁| = |a₂| = 8 and therefore scores **gridFit = 1.0**, directly contradicting §5.3's own "6-, 12-fold: the repeat carries √3" row; a square lattice rotated 30° also scores 1.0. The measure must run over the four components (L₁ₓ, L₁ᵧ, L₂ₓ, L₂ᵧ) reduced mod 8 — that is, over the repeat vectors expressed in the lattice basis — with the max taken over all four.

**For §5.3's expectation table — restate it as a fact about lattices.**

> **Correction — commensurability is a property of the pattern's lattice, not of its fold number.** By the crystallographic restriction, "the rotation centres in a periodic pattern can only be 2-, 3-, 4- or 6-fold" (Cromwell, *Math. Intelligencer* 31 (2009) 36–56) — so 8-fold and 12-fold are exactly as forbidden globally as 5-fold, and grouping 8 with 4 and 12 with 6 is not a symmetry argument. What actually decides the score is the aspect ratio of the pattern's translation lattice: square (ratio 1) → 1.0; hexagonal (√3) → unreachable; 72° rhombic → unreachable, and the irrational involved is cot 36° = 1.3764, **not φ**. And 5-/10-fold Islamic designs are periodic and do have repeat units — Cromwell describes a decagonal design whose rose-motif centres "are diagonally opposite corners of a rectangle that is a repeat unit for the design" — so "5-fold never reaches 1 at any scale" is false as a general statement. Where a pattern is genuinely quasiperiodic there are no repeat vectors at all and `gridFit` should return **undefined**, not 0.

**For §3.5 — rebuild the argument on a number that has a source.**

> **Correction — the "~0.02 mm clutch band" is unsourced and both cited sources say otherwise.** thewave.engineer, read in full, states that "the interference between stud and tube is roughly 0.1–0.2 mm", "designed for 2–3 Newton insertion force", and that the famous "0.002 mm tolerance" figure "is misleading without context" — the real figure being a 10 µm *mould* tolerance and ±0.01 mm on stud diameter specifically. Brighton's micrometer data implies ~0.04 mm of interference. On either figure, `press −0.10` and `holeCompMm 0.20` are the *same order* as the clutch interference, not 5–10× larger. §3.5's conclusion — that LEGO offsets need their own four-way set rather than a `PortFit` rung — still stands, but it must be argued from the **four-way decomposition** and from FDM process variance, not from a band width that no source supports.

**For §1 / novelty framing.**

> **Prior art.** MachineBlocks already generates LEGO-compatible printable parts carrying arbitrary 2D vector artwork on their surfaces (`svg`, `surfacePattern`, `text`, `baseReliefCut`), and base-plate-outliner already goes raster-image → decomposed shape → printable baseplate. Automated legality gates already exist adjacently: Stud.io's collision detection, Brick-by-Brick's action-validity network (NeurIPS 2021), and Legolization's force-based stability threshold. **What is new here is the conjunction** — a compatibility/anchorability score computed *from generated printable geometry* and used as a compile-time gate, driven by a pattern language — **and the application: no existing tool produces LEGO-compatible printed parts from Islamic geometric patterns.** Existing girih work is standalone tiles with no stud system.

### Non-prose actions

- **Add a "contested dimensions" row-note to §3.1.** Wall: 1.5 (doc, derived) vs 1.2 (Bartneck drawing, hardwareishard) vs 1.6 (LDraw/Zoë Blade). Stud height: 1.6 (doc/LDraw) vs 1.7 (Bartneck, Brick Owl). Footprint: 8n−0.2 (Bartneck text, Zoë Blade) vs 8n−0.1 (Brighton micrometer). None of these is settled; the table currently reads as if all are.
- **Add the two LDraw counterexamples to §3.3** (`parts/733.dat`, `parts/6934.dat`) with a one-line note that the library is not uniformly faithful — this is the honest version of "read the primitives as the primary source."
- **Add the wall-vs-tube contact census to §5.2/§5.3** and make it a stated risk for the anchor-only bet: the patent's clamp is "between one secondary projection **and the inner face of an end or side wall**", and dropping anchors that fail the body test drops half the clamp. On 2×2 and 2×4 footprints the wall supplies 67 % and 50 % of contacts. LG-B2's brief should say so explicitly.
- **Resolve §5.2 vs §7.2.** §7 describes only a rectangular shell; §5.2 and LG-B2 assume an arbitrary pattern outline. Either §7 gains the non-rectangular partition or LG-B2 is re-scoped.
- **Define `studsEngaged` for a non-rectangular outline**, and test stud positions against the body the way §5.2 tests anchors.
- **Add to Q1**: Brickset's result that the **0.2 mm nozzle produced *worse* clutch than the 0.4 mm nozzle** removes the "just use a finer nozzle" escape hatch. Q1's fallback needs a different answer.
- **Add a new open question Q6** — clutch depends on wall/tube **flexure**, a material-and-compliance property. A geometry-only gate structurally cannot score it. Say so, rather than letting `anchorability: PASS` imply "will clutch."
- **Note the 1978 disclaimer** wherever US3005282's claims 1–3 are leaned on, and restore "In the preferred embodiments" to the height-equals-depth quote, since §4's `engage` semantics are justified by it.

---

# Grounding audit addendum: FDM printability (bets d, h) — and two corrections to the verdicts above

The delayed printability researcher has returned. It supplies the repeatability data bet (h) was missing, hardens bet (d), and **contradicts two things I stated above.** Corrections first, since they matter more than the new material.

---

## Corrections to the verdicts I already issued

**Correction 1 — verdict #18 was wrong; the doc is right about MachineBlocks' knob names.**
I wrote that the doc's four offsets (`studDiaAdj`, `wallThickAdj`, `tubeZDiaAdj`, `pinDiaAdj`) were "fabricated-by-paraphrase" and that "there is no `pinDiaAdj`". [machineblocks.com/docs/calibration](https://machineblocks.com/docs/calibration) publishes exactly those **short forms**, and `config/config-default.scad` does define `pinDiameterAdjustment = 0.0`. **The doc quoted the calibration page correctly and I audited it against the wrong file.** The residual, much weaker, criticism stands: the calibration page lists **six** (adding `baseHeightAdjustment`, `baseSideAdjustment`), and the source defines ~a dozen (tube X/Y/Z and hole X/Y/Z are each three independent offsets). So §7.5's "four" undercounts — it does not misname. **Recommended doc change #6 above should be replaced with: "note that MachineBlocks exposes six calibration knobs and ~a dozen source-level offsets, with tube and hole diameters split per-axis."**

**Correction 2 — the researcher's headline claim ("the doc builds to LDraw's 6.4 mm tube; this is independently fatal") does not apply.** It misread the doc. §3.1 specifies **6.514** and §3.4's 0.857 mm tube wall is `(6.514 − 4.8)/2`, i.e. the doc already builds to tangency. The 0.8 mm figure is LDraw's, which the doc correctly labels as such. **I am not passing that finding through as a defect.** What survives from it, and is worth adding to the doc, is the corroboration in §D3 below: every independent generator also uses ~6.5, and one derives it from the same formula.

---

## (h) The clutch-band premise — now resolvable, and it moves from "unsourced" to "wrong quantity"

Three findings, in ascending order of importance:

1. **No printer vendor publishes the accuracy figure the argument leans on.** The researcher grepped the actual [Bambu X1C spec PDF](https://public-cdn.bambulab.com/store/bambulab-X1-carbon-tech-specs.pdf) and the [A1 spec sheet](https://cdn.shopify.com/s/files/1/0635/8247/0318/files/A1_Spec_EN_1.pdf) for `accur|precis|toler|repeat|deviat` — **zero matches in both**. [Prusa MK4S](https://www.prusa3d.com/product/original-prusa-mk4s-3d-printer/) claims "Perfect Dimensional Accuracy" with no number. Any ±0.1–0.2 mm attributed to vendor specs is uncited by construction.

2. **Measured part-to-part repeatability at ~5 mm is ~5–10× better than "accuracy" implies.** [Zaborniak et al., *Appl. Sci.* 14(15):6404](https://doi.org/10.3390/app14156404), Prusa i3 MK3 / PLA / 12 nominally identical 3D-scanned samples: *"the difference between the extreme measurement values of 4.95 and 5.01 mm is 0.06 mm. However, the average value of the measurement results is 4.99 mm."* Systematic bias −0.01 mm, spread 0.06 mm over 12 parts. **σ ≈ 0.018 mm is the researcher's own derivation** (range ÷ d₂, n=12) — the paper publishes distribution plots, not a numeric σ, and its headline "accuracy and repeatability of all patterns were 0.1 mm" is a pass/fail against an assumed band, not a measurement. Treat 0.018 as an order-of-magnitude figure.

3. **Bambu itself treats 0.02 mm as an actionable calibration increment** — [Auto Circle Contour Compensation](https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation): *"we recommend using a step value of 0.02mm for fine-tuning"*, and [XY Hole/Contour Compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation) documents one iteration taking a 0.24 mm error to a 0.04 mm residual. **The big number is systematic and removable; the doc's §3.5 argument spends it as if it were random.**

**Net effect on §3.5: the conclusion survives, on a completely different argument.** Against a σ ≈ 0.02 mm and a fit clearance that is a *difference* of two features (σ_fit ≈ √2·σ ≈ 0.025 mm), a 0.02 mm band is roughly ±0.4σ wide → **~30 % of mating pairs land inside it**. That is a real reason the ladder is unusable, and it is defensible. Two supporting facts the doc should carry with it:
- [NIST, Moylan et al., *J. Res. NIST* 119](https://nvlpubs.nist.gov/nistpubs/jres/119/jres.119.017.pdf) — 4 mm pins came out **+0.023 mm** and 4 mm holes **−0.115 mm in the same build**, a 0.138 mm split; after one beam-offset calibration the residual split was still 0.048 mm, because a single scalar offset cannot null both directions. *(Caveat: metal LPBF, not FDM — mechanism transfers, magnitudes do not, and FDM is better placed because slicers expose hole and contour compensation separately.)* This is the real justification for §3.5's four-way decomposition.
- Bambu documents calibration as **per-filament and moisture-dependent** — *"dry filament results in a looser fit, and moist filament results in a tighter fit."* A 0.02 mm band requires requalification per spool. Corroborated independently by Joseph Larson on [3D Printing Tips & Tricks](https://groups.google.com/g/3d-printing-tips--tricks/c/NaorfFlY5ao): *"it's repeatability that matters. You might dial in your 3D printer for one set, but then switch to silk PLA and tell me how it goes."*

**One thing the doc must stop charging to the printer.** [nophead, *Polyholes*](https://hydraraptor.blogspot.com/2011/02/polyholes.html) decomposes hole undersize into four causes, one of which is pure **CAD faceting** — fully removable by `$fn` plus a `1/cos(π/n)` scale, with the empirical rule *"the maximum number of vertices you can have before the hole shrinks is twice the hole size in mm"* (so a 4.8 mm bore wants ~10 facets, not 64). bikar's `HOLE_SEGMENTS = 64` in `solidify-piece.ts:28` **over**-facets, which is the safe side, but the compensation term should be stated explicitly rather than folded into `holeCompMm`. Measured FDM undersize with the faceting removed: [Popescu et al., *Appl. Sci.* 13(1):41](https://doi.org/10.3390/app13010041) — 6 mm holes **−0.124 mm** at best settings, **−0.370 mm** at worst.

**And one finding that is directly adverse to stud/tube geometry specifically:** [*Measurement Science Review* 26(1):33–39](https://journals.savba.sk/index.php/msr/article/download/5835/1760), building an ISO/ASTM 52902 artifact, measured **±0.05 mm on planar surfaces vs ±0.15 mm on cylindrical features in the same part**. Curved features are ~3× worse — which is exactly the stud and the tube. See also [Grgić et al., *Processes* 11(10):2810](https://doi.org/10.3390/pr11102810): *"the quality of FDM 3D printing starts at IT9 grade and goes up to IT14."* *(ISO/ASTM 52902 itself: iso.org 403s; snippets suggest it prescribes test geometries but no accuracy values, so it cannot be cited for a tolerance — **unverified snippet**.)*

---

## (d) Printability — the sceptical case is now much stronger than the doc states

**The Brickset result has a mechanism, and it is worse for the doc than I reported.** A commenter on the article: *"Looks like the red material has a lot of first layer elephant foot… **Ironically that may also be why the red has better clutch power.**"* So the only clutch Huw observed came from an **uncontrolled first-layer printing defect**, not from designed geometry — and the 0.2 mm-nozzle bricks, printed to the doc's own preferred fallback, had *"hardly any at all."*

**[Brick Architect / Van Der Hoeven](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/) isolates the direction of failure, which the doc needs.** A genuine brick stacked *onto* the printed part; the reverse failed, because *"the walls were too thick and the tubes were not perfectly aligned."* **The anti-stud side is the failing side.** That is precisely the side §3.6's `engage 1.6` and §7.4's mesh-floor exemption touch, and it compounds deep dive (e) above. The printed 2×4 also weighed 2.97 g vs 2.32 g genuine (+28 %).

**Other named failure modes**, none currently in the doc: over-tight parts destroyed on removal ([LDraw forums](https://forums.ldraw.org/thread-28663.html): *"you may end up destroying the printed part to remove it"*, and admin Orion Pobursky: *"Printing a part that small in actual size on a FDM printer is going to be tricky with the standard 0.4mm nozzle"*); **size-dependent failure** — two independent Printables makers report 1×N too loose while 2×N works (*"The 4x2 fits ok but the 2x1 is very loose"*), which is the wall-share census in deep dive (b) showing up empirically; stud shear; and cumulative error across tiled cells ([HN](https://news.ycombinator.com/item?id=30243269): *"When you add up tolerancing errors over 10 or 50 bricks in a row the differences can add up"*). Chris Finke, author of `LEGO.scad`, on his own true-scale prints: [*"The fit with real LEGO bricks is acceptable to my six-year-old son, but not satisfying to me."*](https://www.chrisfinke.com/2015/01/27/3d-printed-lego-compatible-bricks/)

**Counter-evidence (people who succeeded) is real but thin and heavily conditioned.** The best datapoint is [Printables 348098](https://www.printables.com/model/348098-perfect-parametric-bricks-and-more) (39 makes, 4.95/5): *"Your parts saved 3 separate builds due to missing pieces. All parts fit perfectly and matched the set really well"* — but with no printer, nozzle, or measurement stated. [Printables 98071](https://www.printables.com/model/98071-lego-custom-bricks-calibration): *"it snapped nicely together with Lego bricks!"* at 0.2 mm layers. The [Prusa blog success](https://blog.prusa3d.com/how-to-make-3d-printed-lego-and-lego-duplo-parts_31741/) is **not a plain-FDM success** — it requires ASA/ABS **plus acetone vapour smoothing**, elephant-foot compensation at 0.4 mm, and deliberately thinned walls. **Zero sources anywhere report caliper measurements on a printed stud, and zero report a clutch durability cycle count** — so any claim about clutch retention over repeated assembly is unsupported in either direction, and §8's coupon ladder is the only way to get that number.

**Two source-quality demotions.**
- **Stop citing pixenib.** Its numbers are verbatim as I reported, but *"tube diameter ~4.9 mm"* **is not a LEGO dimension** — the anti-stud is ~6.5 OD / 4.8 ID. The 4.9 appears invented to make a tidy 0.1 mm clearance story. Its verdict is also positive, so it doesn't support the doc's position anyway.
- **PrintPal is misquoted, and the true text is more useful.** Actual: *"Nozzle: 0.4 mm (standard). **0.2 mm if you want true 100% scale to print cleanly.**"* — a recommendation, not a requirement. But the damaging fact is that **PrintPal's default output is 130 % scale**, because *"True LEGO-size studs are about 5 mm in diameter. On most FDM printers that is right at the edge of what a 0.4 mm nozzle resolves cleanly."* A vendor tool defaulting away from true scale is stronger evidence than the misquote was. (It also says "5 mm stud" — wrong — so treat its dimensional claims as sloppy.)

---

## (d/D3) Generator survey — new, and it points at a concrete design change

Every independent generator lands on ~6.5, and one **derives** it, which is the best available corroboration of §3.2's tangency reasoning:

| Generator | Stud | Tube OD | Wall | Clearance handling |
|---|---|---|---|---|
| [MachineBlocks](https://github.com/pks5/machineblocks) | 4.8 (+0.2 adj) | **6.5** | 1.6 → 1.5 | −0.1/side body **+ 0.1 mm clamp ribs** |
| [MCAD `lego_compatibility.scad`](https://github.com/openscad/MCAD/blob/master/lego_compatibility.scad) | 4.8 | **6.5** | **1.45** | undersized wall, `block_height = 9.5` |
| [brickify](https://github.com/richfelker/brickify) | 4.85 | `sqrt(2)*spacing - stud_diameter` = **6.4637** | **1.2** | `stud_fudge = .2`, `wall_clearance = .1` |
| [anandamous/OpenSCADLEGO](https://github.com/anandamous/OpenSCADLEGO) | **4.85** ("slightly increased from the official 4.8 mm to improve PLA fit") | **6.5** | 1.45 | `fit_tolerance = 0.1`, `stud_rescale = 1.05` |
| [cfinke/LEGO.scad](https://github.com/cfinke/LEGO.scad) | 4.8 × `stud_rescale` (~1.05) | — | — | `stud_play = 0.03` |
| [bricks.lapinoo.net](https://bricks.lapinoo.net/) | — | — | — | 11-step stud scale T5…T1·N·L1…L5 + independent cavity/body/height; **no mm values published** |

**Three of five use walls thinner than the doc's 1.5 mm** (1.45, 1.45, 1.2) — converging on Bartneck's measured 1.2 rather than on the derived 1.5, which strengthens the contested-wall note in verdict #2.

**The architectural finding, and the most actionable item in this addendum:** MachineBlocks does not get clutch from nominal surfaces. It **shrinks the body 0.1 mm per side** (`baseSideAdjustment = -0.1`, `baseWallThicknessAdjustment = -0.1`, `tubeX/Y/ZDiameterAdjustment = -0.1`) and then **adds back a local compliant band** (`baseClampThickness = 0.1`, `tubeInnerClampThickness = 0.1`, `studHoleClampThickness = 0.1`, `tongueClampThickness = 0.1`). Clearance is global; grip is a discrete feature. That is the same architecture as this repo's W2 detent rib, arrived at independently.

### Paste-ready addition for §3.6 / §7

> **Clutch is a feature, not a surface.** The leading LEGO-compatible generator does not obtain clutch from nominal geometry: MachineBlocks shrinks every mating surface by 0.1 mm per side (`baseSideAdjustment`, `baseWallThicknessAdjustment`, `tubeX/Y/ZDiameterAdjustment` all default to −0.1) and then reintroduces grip as discrete compliant bands (`baseClampThickness`, `tubeInnerClampThickness`, `studHoleClampThickness` = 0.1). Clearance is global; interference is local and elastic. This is the same architecture as the W2 detent rib, reached independently, and it is the right answer to §3.5's objection that the fit ladder is too coarse: **we do not need to hit a 0.02 mm band on a 6.5 mm cylinder — we need a loose global fit plus a rib whose deflection absorbs the process spread.** Two facts make this the only workable route. Measured part-to-part repeatability on a 5 mm FDM feature is σ ≈ 0.02 mm (Zaborniak et al., *Appl. Sci.* 14(15):6404 — 12 samples, extremes 4.95/5.01 mm), and clearance is a *difference* of two such features, so σ_fit ≈ 0.025 mm and a 0.02 mm band captures roughly 30 % of pairs. And cylindrical features are the worst case: an ISO/ASTM 52902 artifact study measured ±0.05 mm on planar surfaces against ±0.15 mm on cylinders in the same part. **Recommended: §7 should specify the clutch rib as a first-class feature with its own mesh-floor exemption, and §8 should add a coupon that sweeps rib thickness rather than bore diameter.**

### Further doc changes from this addendum

- **§3.5** — replace the "±0.1–0.2 mm printer accuracy" framing entirely. No vendor publishes it (verified by grep on the Bambu X1C and A1 spec sheets). Argue from σ ≈ 0.02 mm repeatability + variance addition + per-spool recalibration, and cite NIST Moylan for why one scalar offset cannot null both bore and boss.
- **§3.6 / Q4** — add Brick Architect's directional result: the printed **anti-stud** side is what fails, not the stud side. This is the third independent line converging on the same conclusion as deep dive (e).
- **Q1** — record that Brickset's 0.2 mm-nozzle bricks had *worse* clutch than the 0.4 mm ones, and that the only clutch observed was attributed by a commenter to **elephant's foot**, an uncontrolled defect. The "finer nozzle" fallback has no supporting evidence and one direct counterexample.
- **Delete the pixenib citation** (fabricated tube dimension) and **fix the PrintPal quote** to "0.2 mm if you want true 100 % scale to print cleanly", noting its 130 % default scale — which is the stronger fact.
- **New §8 coupon** — the survey found **zero** public sources reporting caliper measurements on a printed stud and **zero** reporting a clutch durability cycle count. Both are cheap to produce here and would be the first public data of their kind; state that as a deliverable rather than leaving clutch retention as an untested assumption.
- **`solidify-piece.ts:28`** — note that `HOLE_SEGMENTS = 64` over-facets small bores relative to nophead's rule (≈2× diameter in mm), which is harmless but means faceting error must not be double-counted inside `holeCompMm`.

**Gaps that remain open after all three researchers.** Reddit and YouTube were unfetchable throughout, so no video comparisons or subreddit failure reports are represented. iso.org 403s. No clutch-durability data exists publicly. And no metrologically-obtained anti-stud tube diameter exists anywhere I could reach — 6.514 remains derived, corroborated only by generators that derive it the same way.
