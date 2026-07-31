# Lego Lab — pattern → piece → LEGO-compatible printed part (LG) — implementation design doc

Status: **v2 — through the adversarial grounding audit
([`research/lego-lab-grounding-audit.md`](research/lego-lab-grounding-audit.md)). Four claims lost
and the design changed: the clutch is now a discrete rib rather than a nominal surface (§3.8, §7.6),
`engage` defaults to 3.2 mm rather than 1.6 (§3.6), the grid-fit measure runs on repeat-vector
*components* rather than lengths (§5.3), and the tangency tube ⌀ is recorded as a derived datum
rather than a fact about LEGO (§3.2). Remaining contested bets, each with its strongest refuting
source, are in Appendix B.**

Built: **R0, M6, M7, P0 and P1 have shipped** (2026-07-29 → 2026-07-31). P1 shipped its
**sweep strip**, its design-notes page, its studio index, **multi-piece export** (§10, D-006) — a
brick mints stud/anti-stud ports from its own lattice and a two-brick assembly exports as two
printable parts — §5.3's **compatibility matrix, now filled by a real sweep**
([`research/lego-lattice-matrix-sweep.md`](research/lego-lattice-matrix-sweep.md)), and the two
**curated scripts** that make that matrix clickable rather than only readable. Only P2–P3 have
not. Building it produced the finding that a printed brick on a
printed brick has **no clutch at all** on the shipped defaults, and the coupon (`LG-S1`) that would
settle where the real ceiling sits; see §10's implementation status. The Lego Lab
page is live and every clutch dimension in it is adjustable and provenance-tagged. Where building a
section proved its spec wrong, the section above is corrected in place and the deviation is listed
in §10's implementation status — so this document describes what exists, and §10 records what it
cost to find out.

Scope: a new `brick` solid declaration that turns a bikar pattern into a **3D-printable
LEGO-compatible part** — a body carrying pattern relief, with studs and/or anti-stud anchors on the
LEGO 8 mm lattice so it clutches into real LEGO — plus the two gates that make "is this pattern
LEGO-compatible?" a measurable question, and the Lego Lab page that puts both in front of a user.

Builds on: [`orb-lab-design.md`](orb-lab-design.md) (the Lab is a copy of its architecture, §9);
[`tile-wall-design.md`](tile-wall-design.md) (`brick` is a `tile`-class specialization);
[`w2-connector-design.md`](w2-connector-design.md) §7 (the slab-stack solidifier this rides, the
precedent for a documented mesh-gate exemption, and — §3.8 — the detent-rib architecture this doc
now adopts for the clutch);
[`c2-assembly-design.md`](c2-assembly-design.md) (printer profile and fit ladder — which §3.5 shows
cannot be reused as-is).

**Decisions locked by Omar, 2026-07-29, before this doc was written.** (1) Output is printed parts,
not a stock-part shopping list. (2) Both gates: anchorability hard, grid fit scored. (3) Interface
is a per-piece DSL option. (4) True LEGO scale, 8 mm pitch. (5) Full grounding ceremony.

---

## 1. Goals

1. **A `brick` declaration** that expresses footprint-in-studs, height-in-plates, and an interface
   choice, and compiles to a watertight printable solid carrying pattern relief.
2. **Anchorability as a hard gate.** For any pattern, answer pass/fail: does this piece have enough
   body, in the right places, to host legal clutch features and hold onto real LEGO?
3. **Grid fit as a score with a tuning path.** Answer 0..1 — and when the answer is low, show which
   parameter value would raise it. This is the concrete response to "can we play with settings to
   make a pattern compatible?"
4. **True-scale interoperability**, verified in plastic against LEGO the user owns, not asserted
   from a dimension table.
5. **Lego Lab** — the page: presets, knobs, viewer with a lattice overlay, both gate panels, a
   sweep strip, STL download.

**Prior art, and what is actually new here.** None of the three ingredients is novel on its own.
[MachineBlocks](https://machineblocks.com/docs/modules/machineblock) already generates
LEGO-compatible printable parts carrying arbitrary 2D vector artwork on their surfaces (`svg`,
`surfacePattern`, `text`, `baseReliefCut`), and
[base-plate-outliner](https://github.com/dlvoy/base-plate-outliner) already goes raster image →
decomposed shape → printable baseplate. Automated legality *gates* exist adjacently:
[Stud.io's collision detection](https://studiohelp.bricklink.com/hc/en-us/articles/5412820155927-Collision),
[Brick-by-Brick's action-validity network (NeurIPS 2021)](https://arxiv.org/abs/2110.15481), and
Legolization's force-based stability threshold. **What is new is the conjunction** — a
compatibility/anchorability score computed *from generated printable geometry* and used as a
compile-time gate, driven by a pattern language — **and the application:** none of the systems
surveyed in Appendix A produces LEGO-compatible printed parts from Islamic geometric patterns.
Existing girih work ([Printables 780631](https://www.printables.com/model/780631-girih-tiles-for-islamic-geometric-patterns),
[mathgrrl](https://mathgrrl.com/hacktastic/2016/03/girih-tiles-for-interactive-islamic-designs/)) is
standalone tiles with no stud system.

**Non-goals for LG** (reserved words error with an LG2 pointer): stock-part mosaic generation and
BrickLink/Rebrickable BOMs; Technic geometry (axle holes, pin holes, ⌀4.8 bars); SNOT/sideways
mounting; hinges and any continuously-rotating joint; minifig-scale anything; multi-piece
*structural* stability analysis; colour.

## 2. Engine ground truth

Verified against bikar at **`6b38342`** (`Merge pull request #4 from NaqshCoffee/w2-connectors-mounts`).
⚠ marks a fact that contradicts or constrains the original plan. The audit re-verified every bullet
in this section against the same commit and found no defects.

- **`solidifySlabStack` is the right solidifier and needs no extension.**
  `packages/core/src/kernel3d/solidify-slabs.ts` builds watertight z-varying solids from a *shared
  2D cell partition* with zero boolean operations — walls where a cell edge has no twin in the
  slab, interface faces where membership flips between slabs, caps at the ends. A brick is exactly
  this shape.
- ⚠ **Its two invariants fail silently.** From the file's own spec header (L26-31): "Cell identity
  is by object reference: reusing one `SectionCell` across slabs is what makes interface XOR and
  wall stacking line up, and shared boundaries between neighbouring cells must reuse the *same*
  discretized polyline coordinates (the C1 ring-cache pattern)". Violate either and the mesh is
  non-watertight with no error thrown. **`meshGate` assertions in tests are the only real guard.**
- ⚠ **Hole rings are CCW, not CW.** `SectionCell` is documented as "a CCW outline with optional CCW
  hole rings strictly inside it", and `NormCell` normalizes "outline CCW, holes CCW". This is the
  opposite of the usual convention and is the single most likely silent authoring bug in
  `brick.ts`.
- **Reusable helpers already exported** from `kernel3d/solidify-piece.ts`: `circlePoints`,
  `normalizeRing`, `pointInPolygon`, `minDistToRing`, `pushQuad`, `emitCap`, `WELD_TOLERANCE`
  (1e-3), `HOLE_SEGMENTS` (64), `REVOLVE_SEGMENTS` (96). `solidifyTubePiece(innerD, outerD, height)`
  exists but emits a standalone piece, not partition cells — reference only.
- ⚠ **`HOLE_SEGMENTS = 64` over-facets the bores we care about** (`solidify-piece.ts:28`). By
  nophead's empirical rule — *"the maximum number of vertices you can have before the hole shrinks
  is twice the hole size in mm"* ([*Polyholes*](https://hydraraptor.blogspot.com/2011/02/polyholes.html))
  — a 4.8 mm bore wants ~10 facets. 64 is the safe side, but it means **faceting undersize is
  already negligible and must not be double-counted inside `holeCompMm`** (§3.5, §7.5).
- **Pattern → extrudable outline exists.** `unionPatternFaces` (`dsl/evaluator.ts:956`) turns a
  pattern's bounded faces into one simply-connected ring by exact directed-edge cancellation. There
  is no general 2D polygon-clipping operation in bikar-core, and none is needed here.
- ⚠ **`DEFAULT_MIN_FEATURE_MM = 1.2`** (`kernel3d/mesh-gate.ts:10`). §3.4 shows the anti-stud tube
  wall is 0.86 mm and §3.8's clutch rib is 0.1 mm of radial protrusion. **Every brick we generate
  fails the min-feature check by design.** Handled in §7.4, the same way W2 handles the clip.
- ⚠ **The fit ladder is too coarse for this job.** `kernel3d/fit-profile.ts` defines
  `press −0.10 / snug +0.05 / sliding +0.15 / free +0.35` mm with `pla_calibrated holeCompMm 0.20`.
  See §3.5 — LEGO fit must be its own set, not a new `PortFit` rung.
- ⚠ **The Lab protocol has no brick variant.** `packages/lab/src/protocol.ts:116` types
  `family: 'lattice' | 'weave' | 'wall'`, and `packages/lab/src/evaluate.ts` `previewResponse`
  returns `null` for "a bare piece, tile, or clip". Lego Lab must **extend that union**, not fork
  the protocol.
- **`tile` is the sibling to copy.** `docs/language-reference.md` §"Tile & Wall Declarations"
  establishes the shape: `outline` / `border` / `inscribe` / `depth` / `hole` / `port` / `mount` /
  `clipseat`, with `tile3d` provenance and reuse of the piece extrude solidifier, manifold gate,
  and port mint. `brick` follows this pattern with `brick3d` provenance.
- **The tile validator precedent** — "Art fills the face: the inscribed pattern's bbox must span
  each axis within `[side − 2·border − 0.5, side + 0.5]` mm" — is the direct model for §6's
  footprint-vs-pattern rule.

## 3. What the survey established (the load-bearing facts)

Full derivations and citations in [`research/lego-brick-system-survey.md`](research/lego-brick-system-survey.md);
every claim below was re-attacked in
[`research/lego-lab-grounding-audit.md`](research/lego-lab-grounding-audit.md) and this section
records the post-audit position, including where the audit won.

### 3.1 The dimensional standard

| Feature | mm | Feature | mm |
|---|---|---|---|
| Stud pitch | **8.0** | Brick height | **9.6** |
| Stud ⌀ | **4.8** | Plate / tile height | **3.2** |
| Stud height | **1.6** ⚠ | Ceiling thickness | **1.6** |
| Side wall (derived) | **1.5** ⚠ | Footprint, n studs | **8n − 0.2** ⚠ |
| Anti-stud tube ⌀ | **6.514** ⚠ / 4.8 | Solid pin ⌀ (1×N) | **3.2** |

Heights are exact and carry **no** gap term — three plates equal one brick exactly. The 0.2 mm
relief is **XY-only**, 0.1 mm per side.

**⚠ Four of these rows are contested and the table should not be read as settled.** The audit found
credible sources disagreeing on each:

| Row | Our value | Disagreeing source | Their value |
|---|---|---|---|
| Stud height | 1.6 (LDraw `p/stud.dat`) | [Bartneck's 3001 drawing](http://www.bartneck.de/wp-content/uploads/2019/04/lego-2x4-brick-dimensions-measurements-3001.pdf), [Brick Owl](https://www.brickowl.com/help/stud-dimensions) | **1.7** |
| Side wall | 1.5 (derived, §3.4) | Bartneck's drawing; [hardwareishard](https://hardwareishard.substack.com/p/lego-lore-6f8) "wall thickness of a LEGO brick is 1.2mm"; and three of five independent generators use 1.45 / 1.45 / 1.2 (§3.8) | **1.2** |
| Footprint | 8n − 0.2 ([Bartneck](https://www.bartneck.de/2019/04/21/lego-brick-dimensions-and-measurements/): "There is a 0.2mm gap between bricks next to each other") | [Brighton Toy Museum micrometer survey](http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions): "consistent ~15.9mm and ~31.9mm … minus a tenth of a millimetre" | **8n − 0.1** |
| Tube ⌀ | 6.514 (derived, §3.2) | LDraw `p/stud4.dat`, and every existing generator | **6.4 – 6.5** |

None of the four changes the design: each disagreement is ≤ 0.3 mm, which §3.5 shows is inside the
printer-compensation term, and §8's coupons measure the realised values directly. They are recorded
because the table reads as authoritative and is not.

### 3.2 Tangency is our authoring datum, not a claim about the moulded part

US 3,005,282 (filed 1958-07-28, granted 1961-10-24) specifies the coupling as a geometric tangency
condition: secondary projections sit "co-axially with the centre of a square defined by four primary
projections", their cross-section "touches the cross sections of the four primary projections"
*(when said cross sections are geometrically projected normal to the bottom wall)*, and a stud is
"clamped between one secondary projection **and the inner face of an end or side wall**".
**In the preferred embodiments** the height of the secondary projections equals the depth of the
cavity. Working that arithmetic against stud radius 2.4 mm gives tube radius `4√2 − 2.4 = 3.257` mm,
i.e. **⌀6.514**.

Two qualifications the v1 draft omitted, both material:

- **Claims 1, 2 and 3 of US 3,005,282 were formally disclaimed by Interlego AG on 31 March 1978.**
  The disclaimer does not affect the geometry the description records, but the patent should not be
  cited as a live specification.
- **6.514 is derived, and no source measures it.** The published spread is 6.31 / 6.4 / 6.4537 /
  6.4637 / 6.5 / 6.51 / 6.5137 — a 0.20 mm range. Two values that look like independent confirmation
  are not: [orionrobots](https://orionrobots.co.uk/Lego+Specifications) presents 6.31 and a 0.657
  wall as "verified measurements", but `8√2 − 5 = 6.3137` and `(8√2 − 5)/2 = 0.6569` — *the same
  formula run with a 5 mm stud*; and Bartneck's Ø6.51 is 6.5137 to two decimals with no stated
  instrument or tolerance. **Our 6.514 is a fact about our chosen stud diameter, not about LEGO.**

**Divergence — we author to tangency anyway, and we drop the zero-clearance claim.** The strongest
measurement-grade source disagrees with a literal tangency reading: the
[Brighton Toy Museum](http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions)
micrometer survey reports that "almost every brick stud we measured, from 1960s sets to modern sets,
was reported by the micrometer as being 4.88mm or 4.89mm", and concludes the stud "appears to be
deliberately oversized 'pragmatically' away from the official dimensions in order to force the
mating brick's walls to flex to accommodate the stud, which then provides grip". LEGO's own element
designers describe the joint as
["an interference fit"](https://bricknerd.com/home/all-about-ned-the-lego-engineering-department-youve-never-heard-of-11-19-23);
the patent reaches for "longitudinal slits 18 … to increase the clamping effect", which only makes
sense against an interfering stud; and moulded parts carry ~0.5° of draft
([hardwareishard](https://hardwareishard.substack.com/p/lego-lore-6f8): "All walls of the part in
the tooling direction are drafted by 0.5 degrees"), so a stud is a truncated cone for which
"tangent" holds at exactly one height. Feed Brighton's 4.88 into our own algebra against 6.51: sum
of radii 5.695 vs centre distance 5.657 → **≈0.038 mm of interference per contact, not tangency.**

So: tangency is our *datum*, because it is the only value derivable without a metrology programme.
The clutch is an interference we add deliberately as a discrete feature (§3.8) and measure in
plastic (§8) — **not** a property we inherit from nominal geometry.

**LDraw's 6.4 is a convention, not a rounding.** The v1 draft called it "a rounding for clean
whole-LDU primitive scaling"; that is wrong. LDraw uses non-integer scale factors freely
(`p/stud4s.dat` carries 0.75 and −0.25; `4-4ring3.dat`'s vertices are irrational). `stud4.dat` is
placed at unit XZ scale in **3,336** part files and never rescaled — 6.4 mm is a library-wide fixed
convention encoding 0.057 mm of clearance per contact, and it is what every existing
LEGO-compatible generator interoperates against. LG-F1 sweeps across both values (Appendix B.1).

### 3.3 The anti-stud taxonomy branches three ways, not two

The plan's "1×N rail exception" is real but is **not a rail**:

| Footprint | Feature | Count | Geometry |
|---|---|---|---|
| 1×1 | none — bare cavity | 0 | 4.8 mm square cavity; four walls grip one stud |
| 1×N, N ≥ 2 | **solid pins** | N − 1 | ⌀3.2 mm |
| M×N, both ≥ 2 | **hollow tubes** | (M−1)(N−1) | ⌀6.514 / 4.8 mm |

Anchors sit on **interior vertices of the stud lattice** — offset 4 mm in each axis from stud
centres. Anchor height equals cavity depth (the patent's "preferred embodiments" clause).

**The audit's census strengthens this and finds its limits.** Resolving subfile references
transitively across the whole library and classifying every part described exactly as
`Brick|Plate|Tile n x m` gives 67 parts, of which **65 conform**. No 1×N part anywhere uses
`stud4`, and no M×N part uses `stud3` — that half of the rule is airtight, and `stud3`/`stud4` are
placed at unit XZ scale in every one of ~6,000 placements. The two exceptions are real:
`parts/733.dat` (Brick 10×10) and `parts/6934.dat` (Tile 3×6, Scala) carry a bare `box5` cavity and
**no anti-stud features at all**. Both are old or peripheral parts and are plausibly LDraw modelling
simplifications — which is the honest caveat on "read the primitives as the primary source": **the
library is not uniformly faithful and cannot be treated as a specification without spot-checks.**

**What the taxonomy exposes, and §5.2 must carry.** The patent's clamp is "between one secondary
projection **and the inner face of an end or side wall**". Counting contacts on the lattice:

| Footprint | tube contacts | wall contacts | share from the **wall** |
|---|---|---|---|
| 1×1 | 0 | 2 | 100 % |
| 2×2 | 4 | 8 | **67 %** |
| 2×4 | 12 | 12 | **50 %** |
| 4×4 | 36 | 16 | 31 % |
| 6×6 | 100 | 24 | 19 % |

For the small footprints this doc actually targets, **the side wall supplies most of the clamping**.
An anchor-only piece (§5.2, LG-B2) deliberately discards the half of the clamp the patent names
first, and is strictly weaker than any real LEGO element of the same size. This shows up empirically
too: two independent Printables makers report 1×N prints too loose while 2×N works
(*"The 4x2 fits ok but the 2x1 is very loose"*). §5.3 and §8 carry it as a stated risk.

### 3.4 Wall thicknesses, and the one that is too thin

Cavity faces are fixed by tangency at 2.4 mm from the outermost stud centre; the shell is
`8n − 0.2` wide. Side wall is therefore `(4n − 0.1) − (4n − 1.6) = **1.5 mm**`, independent of n.
Clean at 3 × 0.5 mm extrusion width. See §3.1 — three of five independent generators use a thinner
wall than this and Bartneck's drawing measures 1.2, so 1.5 is our derived figure, not a consensus.

The tube wall is `(6.514 − 4.8)/2 = **0.857 mm**` — two 0.4 mm lines, and **below the 1.2 mm
mesh-gate floor**. §7.4 handles the exemption.

### 3.5 Our existing fit vocabulary cannot express a LEGO clutch — but not for the reason v1 gave

**Correction — the v1 claim of a "~0.02 mm clutch band" was unsourced, and both sources cited for it
say otherwise.** thewave.engineer, read in full, states that "the interference between stud and tube
is roughly **0.1–0.2 mm**", that it is "designed for 2-3 Newton insertion force", and that the famous
"0.002 mm tolerance" figure "is misleading without context" — the real figures being a 10 µm *mould*
tolerance and ±0.01 mm on stud diameter specifically. Brighton's micrometer data implies ~0.04 mm.
On either number, `press −0.10` and `holeCompMm 0.20` are the *same order* as the clutch
interference, not five times it. The v1 arithmetic does not survive contact with its own source.

**The conclusion stands, on a different argument.** Three facts, each with a primary source:

1. **No printer vendor publishes an accuracy figure at all.** The audit grepped the
   [Bambu X1C](https://public-cdn.bambulab.com/store/bambulab-X1-carbon-tech-specs.pdf) and
   [A1](https://cdn.shopify.com/s/files/1/0635/8247/0318/files/A1_Spec_EN_1.pdf) spec sheets for
   `accur|precis|toler|repeat|deviat` — **zero matches in both**;
   [Prusa MK4S](https://www.prusa3d.com/product/original-prusa-mk4s-3d-printer/) claims "Perfect
   Dimensional Accuracy" with no number. Any "±0.1–0.2 mm printer accuracy" is uncited by
   construction, and v1's use of it is withdrawn.
2. **What is measurable is repeatability, and it is ~σ 0.02 mm.**
   [Zaborniak et al., *Appl. Sci.* 14(15):6404](https://doi.org/10.3390/app14156404) — Prusa i3 MK3,
   PLA, 12 nominally identical scanned samples: "the difference between the extreme measurement
   values of 4.95 and 5.01 mm is 0.06 mm. However, the average value of the measurement results is
   4.99 mm." Systematic bias −0.01 mm; spread 0.06 mm over 12 parts; σ ≈ 0.02 mm by range ÷ d₂
   (an order-of-magnitude figure — the paper publishes distributions, not a numeric σ). **A fit
   clearance is a *difference* of two such features, so σ_fit ≈ √2·σ ≈ 0.025 mm.** A 0.02 mm target
   band is then ±0.4σ wide and captures roughly **30 % of mating pairs** — which is the real reason
   a single authored dimension cannot deliver clutch, and the reason §3.8 exists.
3. **One scalar offset cannot null both a bore and a boss.**
   [NIST, Moylan et al., *J. Res. NIST* 119](https://nvlpubs.nist.gov/nistpubs/jres/119/jres.119.017.pdf)
   measured 4 mm pins at **+0.023 mm** and 4 mm holes at **−0.115 mm in the same build** — a
   0.138 mm split — and after one beam-offset calibration the residual split was still 0.048 mm.
   *(Caveat: metal LPBF, not FDM. The mechanism transfers; the magnitudes do not, and FDM is better
   placed because slicers expose hole and contour compensation separately.)* This is the actual
   justification for a multi-way decomposition rather than one `PortFit` rung.

**And cylindrical features are the worst case.** An ISO/ASTM 52902 artifact study
([*Measurement Science Review* 26(1):33–39](https://journals.savba.sk/index.php/msr/article/download/5835/1760))
measured **±0.05 mm on planar surfaces against ±0.15 mm on cylinders in the same part** — a 3×
penalty on exactly the stud and the tube. Compare
[Popescu et al., *Appl. Sci.* 13(1):41](https://doi.org/10.3390/app13010041): 6 mm holes came out
**−0.124 mm** at best settings and **−0.370 mm** at worst.

**Two operational consequences.** LEGO offsets are their own set, not a `PortFit` rung, following
[MachineBlocks' shipped calibration procedure](https://machineblocks.com/docs/calibration) — which
exposes **six** calibration knobs (`studDiaAdj`, `wallThickAdj`, `tubeZDiaAdj`, `pinDiaAdj`,
`baseHeightAdj`, `baseSideAdj`) and roughly a dozen source-level offsets, with tube and hole
diameters split per-axis. And calibration is **per filament and moisture-dependent** — Bambu's own
docs note "dry filament results in a looser fit, and moist filament results in a tighter fit", and
recommend "a step value of 0.02mm for fine-tuning"
([Auto Circle Contour Compensation](https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation)).
A profile is valid for a spool, not for a printer.

### 3.6 The deep cavity is a moulding artifact — but shortening it is not free

LEGO's cavity is 8 mm deep in a 9.6 mm brick because injection moulding demands uniform wall
thickness; thick sections sink ([Protolabs](https://www.protolabs.com/resources/design-tips/improving-part-design-with-uniform-wall-thickness/),
[Xometry](https://www.xometry.com/resources/injection-molding/managing-sink-in-injection-molding-designs/)).
FDM has no such constraint, and the depth genuinely buys no engagement: `parts/s/3001s01.dat` places
the tube across y = 4→24 LDU (8 mm) while the host stud occupies only its bottom 1.6 mm — **6.4 mm
of the tube's height touches nothing.**

**Correction — v1 read that as a free ~7 mm relief budget. Three consequences say otherwise, and the
default changes.**

1. **Bridging, and it is decisive for FDM.** Printing studs-up leaves the cavity ceiling as an
   unsupported bridge. [Brickset's true-scale print test](https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers)
   records that the sagging strands "will not get in the way of the studs of pieces connected below
   it, **but it would if it was a plate or tile**". A real brick's 8 mm cavity parks the sagging
   surface 6.4 mm clear of the contact zone; `engage 1.6` puts it **exactly where the host studs
   land**. v1's headline case is the *worst* case for FDM, not the free lunch it was presented as.
2. **Compliance.** Clutch is elastic interference (§3.2), and a thin-walled tube is a cantilever
   with `k ∝ 1/L³`. Dropping the free height from 8.0 mm to 1.6 mm makes the tube **125× stiffer**
   (3.2 mm → 15.6×). A rigid joint at FDM's process spread either will not assemble or will not
   hold — there is no elastic reserve.
3. **Wall share.** Per §3.3's census, on 2×2 and 2×4 footprints the tangent side wall supplies 67 %
   and 50 % of the clamping contacts, and a 1.6 mm cavity leaves only 1.6 mm of engaged wall.

Independent corroboration of the direction of failure:
[Brick Architect, hosting Koen Van Der Hoeven](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/)
reports that a genuine brick stacked *onto* a printed part but the reverse failed, "as the walls
were too thick and the tubes were not perfectly aligned" — **the printed anti-stud side is the
failing side**, which is exactly the side `engage` governs.

**Decision (was Appendix B.3, now settled): `engage` defaults to 3.2 mm.** `engage 1.6` remains
available and emits a WARN naming the bridging risk (V5b). `engage` still trades relief budget for
clutch, and the trade is now stated honestly rather than as a windfall. LG-F1 carries 1.6 / 3.2 /
8.0 mm.

### 3.7 Stock-part building escapes the grid only in 0.8 mm quanta

The technique literature's levers are all discrete: the 5:2 SNOT ratio (5 plate heights = 2 stud
pitches, exactly), jumper-plate half-stud offsets (4 mm), SNOTted plates (3.2 mm), headlight bricks
(1.6 mm), combining down to 0.8 mm. Continuous offset needs hinges. **We are not bound by any of
it** — we print the outline. This is the honest answer to "why not build it from real bricks":
that path costs 0.8 mm quantisation and cannot express a 5-fold rosette at all. (Verbatim-verified
against the *Unofficial LEGO Advanced Building Techniques Guide*; the audit found this the
best-grounded section of the survey.)

### 3.8 Clutch is a feature, not a surface — the architectural finding

**The leading LEGO-compatible generator does not obtain clutch from nominal geometry.**
[MachineBlocks](https://github.com/pks5/machineblocks) shrinks every mating surface by 0.1 mm per
side (`baseSideAdjustment`, `baseWallThicknessAdjustment`, `tubeX/Y/ZDiameterAdjustment` all default
to −0.1) and then reintroduces grip as **discrete compliant bands** (`baseClampThickness`,
`tubeInnerClampThickness`, `studHoleClampThickness`, `tongueClampThickness` = 0.1).
**Clearance is global; interference is local and elastic.** This is the same architecture as this
repo's W2 detent rib ([`w2-connector-design.md`](w2-connector-design.md) §12), reached independently.

It is the right answer to §3.5's objection. **We do not need to hit a 0.02 mm band on a 6.5 mm
cylinder — we need a loose global fit plus a rib whose deflection absorbs the process spread.** A
rib deflecting 0.1 mm swallows ±4σ of part-to-part variation where a nominal-surface interference
of the same size swallows none.

The audit's generator survey shows the wider convergence:

| Generator | Stud ⌀ | Tube OD | Wall | Clearance handling |
|---|---|---|---|---|
| [MachineBlocks](https://github.com/pks5/machineblocks) | 4.8 (+0.2 adj) | 6.5 | 1.6 → 1.5 | −0.1/side body **+ 0.1 mm clamp ribs** |
| [MCAD `lego_compatibility.scad`](https://github.com/openscad/MCAD/blob/master/lego_compatibility.scad) | 4.8 | 6.5 | 1.45 | undersized wall, `block_height = 9.5` |
| [brickify](https://github.com/richfelker/brickify) | 4.85 | `sqrt(2)*spacing − stud_diameter` = 6.4637 | 1.2 | `stud_fudge = .2`, `wall_clearance = .1` |
| [anandamous/OpenSCADLEGO](https://github.com/anandamous/OpenSCADLEGO) | 4.85 | 6.5 | 1.45 | `fit_tolerance = 0.1`, `stud_rescale = 1.05` |
| [cfinke/LEGO.scad](https://github.com/cfinke/LEGO.scad) | 4.8 × ~1.05 | — | — | `stud_play = 0.03` |

Every one lands at ~6.5 and one **derives** it from the same tangency identity — the best available
corroboration of §3.2's reasoning, and a reminder that all of them derive rather than measure.

§7.6 specifies the rib as a first-class kernel feature. §8's LG-F1 sweeps **rib thickness** rather
than bore diameter, because rib thickness is the parameter this architecture actually tunes.

## 4. Language design — the `brick` declaration

A new solid declaration, sibling to `tile` and `clip`. It earns its own keyword because
footprint-in-studs and interface-choice are semantics `tile … outline square 100` cannot express,
and because the lattice registration in §5 has no analogue in the tile grammar.

```
brick <Name>
  inscribe <pattern>                    # optional — the 2D art, as `tile`
  footprint <c> x <r> | auto            # in studs; `auto` fits the pattern bbox
  height 1 plate | 1 brick | <n> plates # integer plate multiples only
  studs none | full | edge              # the interface option (decision 3)
  anchors auto | none                   # `auto` = solver picks tubes/pins per §3.3
  engage <mm>                           # optional — cavity depth, default 3.2 (§3.6)
  clutch auto | none                    # optional — the §3.8 rib set, default auto
  relief depth <mm>                     # optional — pattern cut into the top face
  origin centered | at <col>[,] <row>   # lattice registration
  port <name> at ...                    # piece port grammar, unchanged (C2)
```

**`origin at` is unparenthesized, and the comma is not always optional.** This sketch originally
wrote `at (<col>,<row>)`; the shipped grammar does not, because every other `at` clause in the
language is unparenthesized and one convention across the grammar beats matching a sketch. The
sketch's spelling is not quietly accepted either — `at (1, -2)` is read as a parenthesized
expression and the comma inside it is a parse error.

The comma between the two offsets is optional only when the row is non-negative. Both offsets go
through the ordinary numeric-expression parser, so `at 1 -2` is the single expression `1 − 2` and
the row never arrives; `at 1, -2` is the spelling to use. This is a wart of reusing the expression
parser, not a design choice, and `brick-parse.test.ts` pins both spellings so it cannot regress
into silently reading the wrong lattice offset.

**The three interfaces.**

| `studs` | Top face | Bottom | Stacks under? | Analogue |
|---|---|---|---|---|
| `none` | flat, carries relief | anchors | no | tile (3070b/3068b) |
| `full` | one stud per cell | anchors | yes | brick (3005/3001) |
| `edge` | studs on the perimeter cells only | anchors | partly | jumper-ish; relief gets the interior |

`studs none` + `anchors auto` is the default and the one that matters: a patterned tile that
clutches onto a LEGO baseplate. `studs full` makes it stackable at the cost of burying the art
under studs, which §6 refuses to do silently.

**Why `engage` exists.** Cavity depth and body height are independent for a printed part (§3.6).
`engage` is the cavity depth (and therefore the anchor height); `ceiling = height − engage` is what
relief has to work with. Default **3.2 mm**: deep enough that the bridged ceiling clears the host
studs by 1.6 mm and the tube keeps usable cantilever compliance, shallow enough to leave 6.4 mm of
relief budget in a `1 brick` body. `engage 1.6` is legal and warns.

**The default does not fit a `1 plate` body, and that is a real restriction, not a rounding.** A
plate is 3.2 mm tall and V3/V5 require 1.2 mm of ceiling, so a one-plate brick admits `engage` only
in **[1.6, 2.0]** — every value of which trips V5b, because the whole band sits below the 3.2 mm
bridging threshold §3.6 settled on. `height 1 plate` therefore cannot be built at the shipped
default and cannot be built without a warning at any legal value. This is §3.6's finding arriving
where it bites rather than a defect: a printed one-plate tile has a bridged ceiling parked in the
host studs' zone, and the warning is the honest report of that. The two plausible fixes — lowering
the default, or refusing `1 plate` outright — both trade a measured concern for an unmeasured one,
so neither ships before LG-F2. M6 states the constraint instead.

**Why `clutch` exists.** Per §3.8, geometry is authored *loose* and grip is a discrete rib. `clutch
auto` emits the rib set §7.6 specifies, sized by the active fit profile. `clutch none` emits nominal
surfaces with global clearance only — useful for a decorative piece that must not resist removal,
and for LG-F1's rung 0.

**Height is in plates because the system is.** `1 brick` is sugar for `3 plates`. Non-integer
multiples are an error (§6) — a piece 5.0 mm tall cannot stack into a LEGO model.

## 5. Grid registration and the anchor solver

### 5.1 Lattice registration

For a `c × r` footprint centred on the origin, stud centres are at

```
x_i = (i − (c−1)/2) · 8     i = 0 … c−1
y_j = (j − (r−1)/2) · 8     j = 0 … r−1
```

and anchor candidates sit on the interior vertices — the midpoints between adjacent stud
columns/rows:

```
ax_i = (i + ½ − (c−1)/2) · 8   i = 0 … c−2
ay_j = (j + ½ − (r−1)/2) · 8   j = 0 … r−2
```

`origin at (col,row)` shifts the whole lattice by whole studs, for pieces meant to register at a
known place in a larger build. For a rectangular piece the shell outline is `8c − 0.2` by
`8r − 0.2`, per §3.1; for a pattern-outline piece see §5.2 and §7.2.

### 5.2 The solver, and what "the body" means

```
anchorKind(c, r) = c ≥ 2 ∧ r ≥ 2 → tube   at each of the (c−1)(r−1) interior vertices
                   c = 1 ∧ r ≥ 2 → pin    at each of the (r−1) mid-edges
                   c ≥ 2 ∧ r = 1 → pin    at each of the (c−1) mid-edges
                   c = r = 1     → none
```

**The body is one of two things, and the doc must say which.** A `brick` has a
`bodyOutline: Ring` that is either the rectangle `8c−0.2 × 8r−0.2` (when there is no `inscribe`, or
when the pattern fills the footprint) or the `unionPatternFaces` ring inset by the wall thickness
(when the pattern's outline is the piece's outline). §7.2 partitions both cases; the rectangular
case is the simpler specialization, not the only one.

Each candidate anchor is **tested against the body**. A candidate survives when its full footprint —
the anchor circle plus its wall plus its ribs — lies inside `bodyOutline` with ≥ 0.4 mm to spare
(`minDistToRing`). Candidates that fail are dropped, not moved: moving an anchor off the lattice
would defeat its only purpose.

**Studs are tested the same way, and `studsEngaged` is defined from that test.** For each lattice
cell `(i,j)`, the cell is *engaged* when the full 4.8 mm stud disc at `(x_i, y_j)`, plus the 1.5 mm
of cavity wall around it, lies inside `bodyOutline`. `studsEngaged` is the count of engaged cells.
For a rectangular footprint this is simply `c·r`; for a pattern outline it is strictly smaller, and
it is the number that §5.3's rotation-lock criterion reads.

**Stated risk — the anchor-only bet discards half the clamp.** Per §3.3's census the tangent side
wall supplies 50–100 % of the clamping contacts on the footprints we target. A piece whose outline
is the pattern's has no continuous tangent wall, so its clutch comes from anchors and ribs alone and
is strictly weaker than a rectangular piece of the same size. LG-B2 exists to measure how much
weaker; until it does, this is a bet, not a fact (Appendix B.2).

### 5.3 The two gates

**Anchorability (hard, pass/fail).** A piece is anchorable when *all* of:

- `studsEngaged ≥ 2` — at least two lattice cells are fully covered by body (§5.2).
- `anchors.count ≥ 1` — at least one candidate survived the body test.
- `minAnchorWallMm ≥ 0.8` — no anchor is thinner than the tangency wall.
- the shell wall is ≥ 1.2 mm everywhere the cavity runs.

**Rotation lock is `studsEngaged ≥ 2`, not `anchors.count ≥ 2`.** A 1×1 piece contacts a single
cylindrical stud and is **not rotationally constrained by geometry** — it turns under modest applied
torque, resisted only by clutch friction, which is tolerance- and material-dependent and cannot be
relied upon. ([Eurobricks](https://www.eurobricks.com/forum/forums/topic/30171-1x1-brick-alignment/)
builders report both that "1x1 pieces … can freely rotate around it" *and* that on older,
tighter-tolerance bricks "you sometimes couldn't rotate a 1x1 piece without taking it off".) Because
a printed part's clutch friction is *less* predictable than moulded ABS, geometric constraint is the
right criterion. Two engaged studs lock rotation regardless of anchor count; that is why a 1×2 with
a single pin is rigid.

**Grid fit (scored, 0..1).** The v1 formula was mechanically wrong: it consumed only the two repeat
*lengths* and never the angle between them, so a hexagonal lattice `a₁=(8,0), a₂=(4,4√3)` — for
which `|a₁| = |a₂| = 8` — scored **1.0**, contradicting the doc's own 6-fold row. The measure runs
on **components in the lattice basis**:

```
res(u)      = 8 · min over integer n of |u/8 − n|                 # mm, in [0, 4]
r(v, θ)     = max( res(vₓ cos θ − v_y sin θ), res(vₓ sin θ + v_y cos θ) )
gridFit(θ)  = 1 − max( r(L₁, θ), r(L₂, θ) ) / 4
gridFit     = max over θ ∈ [0, 90°) of gridFit(θ)                 # reported with argmax θ*
repeatUnitStuds = (round(L₁/8), round(L₂/8)) when both vectors are axis-aligned at θ*
                  and every residual < 0.05 mm; else null
```

Maximizing over θ is not a technicality — rotation offset is one of the three tuning knobs the user
was promised (scale, rotation, division count), so the score must be the best achievable
registration and the Lab must report the θ that achieves it.

**The snap threshold is 0.05 mm and it is not the 0.2 mm from §3.1.** v1 reused the inter-part
moulding relief as a pattern-registration tolerance; that is a category error, and one of the two
sources for it says 0.1 anyway. 0.05 mm is ~2σ of measured FDM part-to-part repeatability (§3.5) —
i.e. the tightest registration a printed piece can actually hold.

**What the score says — as a fact about lattices, not about fold numbers.** By the crystallographic
restriction, "the rotation centres in a **periodic** pattern can only be 2-, 3-, 4- or 6-fold"
([Cromwell, *Math. Intelligencer* 31 (2009) 36–56](https://link.springer.com/article/10.1007/s00283-008-9018-6)),
so 8-fold and 12-fold are exactly as forbidden *globally* as 5-fold and the v1 grouping (8 with 4,
12 with 6) was not a symmetry argument. What decides the score is the **aspect ratio of the
pattern's translation lattice**:

The **Measured** column is a sweep, not a prediction: five bases across one
shared interval, 2–20 mm at a 0.005 mm step (finer than the snap threshold, so
a snapping scale cannot fall between samples), pitch 8 mm, θ maximized by
`gridFit`. Run and full commentary:
[`research/lego-lattice-matrix-sweep.md`](research/lego-lattice-matrix-sweep.md).

| Lattice | Ratio | Measured (max fit · at scale · repeat unit) | Authorable | Typical families |
|---|---|---|---|---|
| square | 1 | **1.0000** at 8 mm, θ = 0, repeat unit **1 × 1** — and at 2, 4 and 16 mm too | yes — `tile … mode rectangular` | 4-, 8-fold canonical constructions |
| hexagonal | √3 = 1.7321 | max **0.8037**; never ≥ 0.999 in range. One axis snaps, the other plateaus: at 8 mm, θ = 0 the residuals are **0.000 / 4.000 mm** | yes — `tile … mode hex` | 6-, 12-fold canonical constructions |
| 72° rhombic | cot 36° = **1.3764** | max **0.7264** (at 6.995 mm, θ = 9°) over the swept interval; never ≥ 0.999 | **no — kernel only** | many 5-, 10-fold constructions |
| rectangular, rational ratio | p/q | p/q = 3/2 reaches **1.0000** at 16 mm, θ = 0, repeat unit **3 × 2** | yes — `tile … mode rectangular` | 5-/10-fold designs with a rectangular repeat |
| genuinely quasiperiodic | — | `gridFit` **undefined**, at every scale and in the fixed-scale probe | yes, trivially — any `brick` with no `tile` block | rare; no repeat vectors exist |

Three things in that table are worth reading twice.

**The rhombic row is bounded by the sweep.** 0.7264 is the maximum *over
2–20 mm*, not over every scale. The unbounded claim — that a cot 36° lattice
never registers — rests on that ratio being irrational, which is an argument and
not this measurement; the sweep is consistent with it and does not establish it.
That row is also the one row **no `.bkr` can produce**, which is what the
**Authorable** column is for. `env.repeatVectors` is assigned in exactly one
place — `packages/core/src/dsl/evaluator.ts` — and it admits exactly two basis
shapes: `[(dx,0), (0,dy)]` for `mode rectangular` and `[(dx,0), (dx/2,dy)]` for
`mode hex`. A 72° rhombus is neither, so the sweep reaches it by constructing
the basis directly. The column says which rows are facts about a script and
which are facts about the gate; without it the table silently mixes the two.

The alternative — adding a general two-vector `basis` statement so every score
in the table becomes reachable — was argued with the geometry compiled beside
it and was **not** taken: [`decisions-log.md`](decisions-log.md) D-007, and the
`lattice-basis` design note (§12) it was decided from.

**"At the right scale" is plural.** `square` scores 1.0 at every divisor of the
pitch in range: 2, 4, 8 and 16 mm. The sweet spots are periodic, so a sweep
window that straddles none of them draws a flat curve for a lattice that
registers perfectly — which is a thing the sweep strip (§10) has to not mislead
the user about.

**A good score and a withheld repeat unit are consistent.** `hexagonal` scores
0.8037 and still reports no repeat unit in studs. The score is about
registration; the repeat unit is about axis alignment. A sheared basis can do
well at the first and have no answer to the second.

**Why the hexagonal row needed a second measurement.** *One axis snaps, the
other plateaus* is a claim about the two axes separately, and `gridFit` scores
the **worst** axis — so its best scale is necessarily where the two residuals
balance (0.785 / 0.785), the one place the asymmetry cannot show. Reading each
axis at the scale that makes the first basis vector exactly one pitch shows it
exactly: 0.000 mm against 4.000 mm, a half pitch, which is the worst offset
there is. No rotation of the basis fixes one axis without moving the other.

The last two rows correct v1's "5-fold never reaches 1 at any scale", which is false as a general
statement: 5-/10-fold Islamic designs are periodic and do have repeat units — Cromwell describes a
decagonal design whose rose-motif centres "are diagonally opposite corners of **a rectangle that is
a repeat unit for the design**". The irrational that blocks the rhombic family is cot 36° = 1.3764,
**not φ**. And where a pattern is genuinely quasiperiodic there are no repeat vectors at all, so
`gridFit` returns `undefined` — not 0, which would read as "measured and bad".

`sweepGridFit(source, param, range)` returns fit-vs-value so the Lab can surface the sweet spots.
For an unreachable lattice the honest output is a flat curve — and the piece still **passes
anchorability**, which is the whole point of splitting the two.

## 6. Validators (compile-time; house error style)

| # | Rule | Level |
|---|---|---|
| V1 | `height` is an integer multiple of 3.2 mm | ERROR |
| V2 | `footprint` is large enough for the pattern bbox (tile's rule, in stud units) | ERROR |
| V3 | `relief depth ≤ ceiling − 1.2` where `ceiling = height − engage` | ERROR |
| V4 | `studs full` with any `relief depth > 0` — studs bury the art | ERROR, name `studs none` |
| V5 | `engage ≥ 1.6` and `engage ≤ height − 1.2` | ERROR |
| V5b | `engage < 3.2` — bridged ceiling lands in the host studs' zone (§3.6) | WARN |
| V6 | `anchors none` on a piece the §5.3 gate then fails | ERROR, quote the gate |
| V7 | `footprint 1 x 1` — not rotation-locked, cannot carry oriented art | WARN |
| V8 | `gridFit < 0.8` | WARN, name the swept param and its nearest sweet spot |
| V9 | pattern bbox exceeds footprint in one axis only | ERROR, suggest the `c × r` that fits |
| V10 | `clutch none` on a piece whose only clamp is anchors (§3.3 census: no tangent wall) | WARN |
| V11 | a `port` on a `brick` whose contract states a dimension — `pin`, `pin_socket`, `ring`, `rim` | ERROR, name the port |

V8 is a warning by design: an incommensurable piece is still a *correct* piece, just not a
seamlessly-tiling one. Refusing it would delete the 5-fold families, which is the opposite of the
goal. V10 likewise: a clutchless decorative piece is legitimate, but it must not be produced
silently on a footprint that has nothing else holding it.

V11 is a different shape from the other ten. They all say a dimension is wrong; V11 says a
declaration describes geometry that was never built. A `brick` has no `hole` statement and
`buildBrick` reads no ports, so only `hole` cuts material and a dimensioned port on a brick names a
feature the exported mesh does not contain — the mesh is identical with and without it, while a
`connect` against it still passes the C2 fit check. `kind axis` is exempt: it states no dimension,
so there is nothing the kernel can have failed to cut. Found while scoping multi-piece export
([`decisions-log.md`](decisions-log.md) D-006) and pinned by
`bikar:packages/core/tests/kernel3d/brick-phantom-port.test.ts`.

## 7. Kernel — the brick cell partition over `solidifySlabStack`

### 7.1 The stack

Three slabs, bottom (bed) to top. z = 0 is the printed bed face, which is the brick's **underside**
— the cavity opening. Printing studs-up is universal practice (survey §5).

| # | Slab | z range | Cells solid |
|---|---|---|---|
| 1 | cavity | `0 → engage` | outer wall ring + anchor cells (tube annuli or pin discs), both rib-lobed |
| 2 | ceiling | `engage → height` | full footprint, minus relief pockets |
| 3 | studs | `height → height + 1.6` | one disc cell per stud position (`studs` ≠ `none`) |

The `studs` slab is omitted entirely for `studs none` — a two-slab stack, which the solidifier
handles without special-casing.

**Corrected in M6 — relief splits the ceiling into two slabs, so the stack is three or four.** A
pocket is not "the ceiling minus a region": a recess has a floor, and a floor is a slab boundary.
With `relief depth d` the ceiling becomes `engage → height − d` (the pockets solid, so the recess
has a bottom) and `height − d → height` (the pockets absent, which *is* the recess). The row above
reads correctly only for `relief depth 0`.

The art's connected components each become **one pocket bounded by that component's outer
perimeter**. An enclosed void inside a component is an error, not an island left standing in the
recess — the same finding as Q3 (§11) and for the same reason: a nested void arrives from the face
extractor as material, so nothing downstream can tell "the author meant a hole" from "the author
drew an overlay". `hole` remains the supported way to ask for a void.

### 7.2 The partition — both body cases

Cells are built **once** and listed by reference in each slab they are solid in, per §2's
invariant. The partition is:

- one **shell ring** cell: `bodyOutline` (§5.2) with the cavity ring as its (CCW — §2) hole;
- one **cavity interior** cell: the cavity ring, solid only in slab 2;
- one cell per **anchor**: a tube annulus (outer ⌀6.514 rib-lobed ring with a CCW ⌀4.8 hole) or a
  solid pin disc (⌀3.2);
- one cell per **stud** disc;
- one cell per **relief pocket**, from the pattern.

The two body cases differ only in how `bodyOutline` and the cavity ring are computed:

| Case | `bodyOutline` | Cavity ring |
|---|---|---|
| **rectangular** (no `inscribe`, or pattern fills the footprint) | the rectangle `8c−0.2 × 8r−0.2` | the rectangle inset by 1.5 mm, rib-lobed at each stud-facing position |
| **pattern outline** (the piece *is* the pattern's shape) | the `unionPatternFaces` ring | the same ring inset by 1.5 mm (`normalizeRing` + offset), rib-lobed only where the inset survives |

The inset is the one operation the rectangular case does not need. It is a straight polyline offset
of a simply-connected ring, not a general boolean — a concave vertex whose offset self-intersects is
clipped by dropping the crossing span, and if that leaves the ring degenerate the piece fails V2
before the kernel runs. This is the non-rectangular partition LG-B2 depends on; it is specified
here rather than discovered in M6.

The shell's cavity hole and the cavity-interior cell share a boundary; the tube's outer ring is a
boundary of nothing else. Both must satisfy the coordinate-identity invariant.

**Corrected in M6 — four things this section got wrong about its own construction.**

1. **The interface between two slabs is the symmetric difference of their solid regions, not a cap
   per cell.** Capping every cell that is solid on exactly one side is wrong whenever the two sides
   are partitioned differently: a cell below and a cell above covering the same ground each get a
   cap, so the mesh grows a coincident double wall and the material on one side becomes a
   **separate body**. It is watertight, the Euler characteristic is fine, and a slicer prints loose
   parts rattling inside a shell — which is exactly how the first `studs full` brick came out, as
   four free discs sitting on a closed ceiling. `emitInterfaces` now accumulates directed edges with
   a signed net count per segment and chains what survives into rings, so a cell present on both
   sides cancels against itself. `brick.test.ts` counts connected shells, not just watertightness,
   because watertightness cannot see this.

2. **The anchors must be carried through the ceiling slabs, with a plug closing each bore.** A tube
   listed only in the cavity slab is solid on one side of the cavity/ceiling interface and gets its
   own cap plus a coincident counter-cap from the ceiling that holes it — the same loose-body
   failure as (1). The tube cell and its bore plug are therefore listed in every slab from the bed
   to the top of the ceiling.

3. **Anchors and relief pockets are resolved by nesting, and by dropping — never by cutting.** An
   anchor wholly inside a pocket becomes a **hole of that pocket**, so the tube stays solid through
   the recess: the relief decorates the ceiling and does not cut the structure, and a nested tube's
   top sits flush with the un-relieved top face. An anchor **straddling** a pocket edge has no such
   reading — part of it would be cut and part not, which needs the 2D boolean this partition exists
   to avoid — so `solveAnchors` drops it and reports `droppedForRelief`. This is not a corner case:
   `Star-Brick` at the default numbers keeps **1 of 9** anchor candidates, and the report says so
   rather than the piece silently losing its grip.

4. **Studs can never be cut as holes in a ribbed `cavityInterior`.** At the default fit the rib lobe
   apex reaches |x| = 6.30 mm and the stud circle reaches 4.0 + 2.3 = 6.30 mm — exactly tangent —
   and a hole ring touching its outline pinches the polygon into non-manifold edges. Studs live on
   the far side of the ceiling and need no fusion cell, so they are simply not holes here. This is
   a standing constraint rather than a one-off: `CAL-RIB-01` sweeps `ribMm` up to 0.20, which moves
   the lobe apex outward, so any future attempt to hole the studs has to re-derive the tangency at
   the top of the sweep, not at the default.

### 7.3 The ring cache is mandatory

Every circle discretized here — stud discs, tube outer rings, tube bores, pin discs, relief arcs —
must come from a **single memoized `circlePoints(cx, cy, r, HOLE_SEGMENTS)` cache keyed on
`(cx, cy, r)`**. The tube's bore ring and the stud disc that mates with it are *different* rings at
different places and need no sharing; but the cavity ring appears in two cells and **must be the
identical array**. This is the C1 pattern and it is not optional — §2 records that violating it
produces a silently non-watertight mesh. Rib lobes (§7.6) are generated *into* the cached ring, not
added afterwards, so both cells that reference it see the same coordinates.

**Corrected in M6 — coordinate identity is necessary but not sufficient; the cap triangulator now
checks its own output.** Sharing the identical array guarantees the two cells agree on where the
boundary is. It does not guarantee that earcut *triangulates* that boundary manifoldly, and M6
measured a case where it does not. Earcut bridges each hole into the outline along a horizontal
ray; when a hole edge, an outline vertex and the next hole share a row, that ray runs through the
next hole's vertices, and the result is area-exact but meets along a **T-junction** — one triangle
spanning an edge that two others split at an interior vertex. Every triangle is non-degenerate, the
area check passes, and the solid is not closed.

So `emitCap` validates the triangulation against the ring edges it was handed, and on failure
retries in rotated frames: earcut's degeneracies are axis-aligned, rotation is affine, and a
triangulation valid in the turned frame is valid in the original. Rotation alone is not enough —
collinearity is rotation-invariant, so the turned frames produce zero-area slivers instead, which
have no winding to orient and which the mesh gate rejects outright. Each sliver is therefore
**absorbed**: the triangle across its long edge is split at the sliver's middle vertex, reproducing
the sliver's short edges in the same direction and leaving the region boundary untouched. Dropping
it would be wrong — the sliver is the only thing bridging the T-junction.

**Validator:** a cap is accepted only when every directed edge of its triangulation appears exactly
once and its unpaired edges are precisely the ring edges the section declared.
PASS: the corner clip's ceiling section, 24-vertex outline and four riser holes, after retry —
40 unpaired edges, one per ring edge.
FAIL: the same section in the unrotated frame — 41 unpaired edges, the extra one being the T-junction
chord, which the area check scores as exact.

The measurement is on the corner clip rather than a brick because that is where it was found: its
four riser holes all sit on `y = ±1.2`, collinear with the outline's own necks.

### 7.4 The mesh-gate exemption

Per §3.4 the tube wall is 0.857 mm and per §7.6 the clutch rib protrudes 0.1 mm, both against a
1.2 mm floor. The rib is *additive* — it never thins anything — so it does not need its own numeric
floor; what it needs is the tangential-width rule in §7.6. Watertightness and Euler consistency are
**not** relaxed — they are the actual regression guard for §7.2's invariants and every generated
brick must pass them.

**Corrected in M6 — `minFeatureMm` is a declaration, not an override, and the number is 0.70.**
This section originally specified "an explicit `minFeatureMm` override of 0.8". Neither half
survived contact with the API it names.

`solidifySlabStack`'s `minFeatureMm` is a **declaration of the smallest feature actually present**,
which the print gate then compares against the FDM floor. It is not a floor the caller lowers.
Passing a flat 0.8 would be an unmeasured claim about the mesh, and would go on reading 0.8 after a
fit knob thinned a wall to 0.3 — the exemption would stop being bounded and become asserted. So
`brickMinFeature` computes the real minimum, `buildBrick` declares it, and the exemption becomes an
invariant instead: a brick whose thinnest dimension falls below `BRICK_MIN_FEATURE_MM` is refused,
naming the dimension.

**Default:** `BRICK_MIN_FEATURE_MM` = 0.70 mm (`bikar/packages/core/src/kernel3d/brick.ts`), with the
derivation below; the *measured* clutch numbers it has to leave room for are bet CAL-RIB-01.
0.8 was derived from the bare tangency datum's 0.857 mm tube wall, but the shipped fit
shrinks the tube's outer surface by 0.2 diametral while the bore stays nominal, so the wall a
**default** brick actually has is `(6.5137 − 0.2 − 4.8) / 2 = 0.757` mm. A floor of 0.8 refuses the
default brick — the doc's number does not survive the machinery the doc ships. 0.70 clears 0.757
with margin for the fit knobs and still sits above one 0.4 mm extrusion.

**Validator:** a brick is refused when `brickMinFeature(spec).mm < BRICK_MIN_FEATURE_MM`, and the
error names the dimension that failed rather than the aggregate.
PASS: the default 2×4, whose thinnest dimension is the 0.757 mm tube wall — 0.757 ≥ 0.70.
FAIL: the same brick with a fit profile widening the bore to 5.2 mm, whose tube wall becomes
`(6.5137 − 0.2 − 5.2) / 2 = 0.557` mm — refused, naming `anchor wall`, where a flat 0.8 declaration
would have reported 0.8 and shipped a mesh with a 0.557 mm wall in it.

This mirrors W2, where the corner clip is exempt from the mesh floor by design. The precedent is
deliberate: the floor is a default for pattern art, not a law about connectors.

### 7.5 Fit application — clearance is global

Authored geometry is the tangency datum (§3.2). A LEGO fit profile applies independent offsets at
emit time — `studDia`, `wall`, `tubeDia`, `pinDia`, and (following MachineBlocks' per-axis split)
`tubeDiaX`/`tubeDiaY` where a printer's XY error is anisotropic. These are **not** `PortFit` rungs
(§3.5). Defaults follow the shipping convention of −0.1 mm per side on every mating surface; the
values that ship come from §8's coupons, not from this document.

**Faceting is not part of the compensation.** `HOLE_SEGMENTS = 64` already over-facets a 4.8 mm bore
by ~6× against nophead's rule (§2), so the faceting undersize term is negligible here and must not
be folded into `holeCompMm` a second time.

### 7.6 The clutch rib — a first-class feature

Per §3.8, grip is a discrete elastic feature, not a nominal surface. The kernel emits:

- **Tube ribs** — four lobes on each tube's *outer* ring, at 45°/135°/225°/315°, i.e. facing the
  four studs the tube clamps. Each lobe is a radial protrusion of `ribMm` (default **0.10 mm**)
  spanning an arc of `ribArcMm` (default **0.8 mm**) with a linear ramp on each side.
- **Wall ribs** — one lobe on the cavity ring at each stud-facing position, same dimensions, giving
  back the wall contact §3.3 shows is 50–67 % of the clamp on small footprints.
- **Pin ribs** — three lobes on a solid pin's disc, at 90°/210°/330°.

Two rules make the rib survive the toolchain rather than being an authoring fiction:

1. **`ribArcMm ≥ 2 × nozzle`** (0.8 mm at 0.4). A lobe narrower than one extrusion width is
   absorbed into the perimeter path and does not exist in the printed part. This is the rib's real
   floor, not the mesh gate's.
2. **The rib is generated into the cached ring** (§7.3), so it is the same coordinates in every cell
   that references that ring — a rib added as a separate cell would violate the boundary invariant.

`ribMm` is a fit-profile value, swept by LG-F1. `clutch none` sets it to 0, which degenerates the
lobes away cleanly and leaves nominal surfaces with global clearance only.

## 8. Coupons and the prototype catalog — the LG ladder

Entered in `.claude/skills/prototype/catalog.md` in the skill's schema. Ordered
cheapest-decisive-learning-first. §3.2, §3.5 and §3.8 together mean **no clutch number in this
document is trustworthy until something is printed and pushed onto a real brick** — LG-F1 is what
makes one trustworthy.

That premise is unchanged; what changed is what follows from it. This section first read *"LG-F1
blocks M6"*, on the W-F1/W-C1 analogy. It no longer does — see §10. An untrustworthy number must not
be **baked**, which is what the analogy correctly forbids; it may perfectly well be a **knob**, and
LG-F1's own design is a `ribMm` × `engage` sweep, which is what a knob is for. The coupons keep
their full decisive role and lose only their position in the ordering.

The audit establishes an unusual fact about this ladder: **no public source reports caliper
measurements on a printed stud, and none reports a clutch durability cycle count.** LG-F2 and LG-D1
would be the first public data of their kind. That is a deliverable, not a footnote.

- **LG-F1 — clutch coupon, anchor side.** A 2×4 tile-style piece, printed as a matrix: a five-rung
  **rib-thickness** ladder (`ribMm` 0 / 0.05 / 0.10 / 0.15 / 0.20) at a fixed −0.1 mm/side global
  clearance, crossed with `engage` 1.6 / 3.2 / 8.0. Mated against a real LEGO plate. *Learns:* does
  it clutch, does it hold, which rib thickness this printer/filament needs, and whether the shallow
  cavity's bridging actually lands in the stud zone (§3.6). → `ribMm` and the `engage` default.
  **Sweeping the rib rather than the bore is the §3.8 change: the bore is set loose on purpose.**
- **LG-F2 — clutch coupon, stud side.** A plate with a stud-⌀ ladder, tested against a real LEGO
  brick's underside, **and measured with calipers before testing.** *Learns:* whether `studs full`
  is viable at 0.4 mm at all; the realised-vs-authored stud diameter, which no published source
  reports. → the `studDia` entry.
- **LG-R1 — 1×N pin coupon.** A 1×4 with the three ⌀3.2 pins §3.3 predicts. *Learns:* whether the
  pin geometry survives FDM anisotropy, and whether a pin is weaker than a tube in practice — two
  Printables makers report exactly this failure (§3.3). → the `pinDia` entry.
- **LG-D1 — clutch durability.** One passing LG-F1 rung, cycled 100 times against the same LEGO
  plate, with insertion/retention checked at 1 / 10 / 50 / 100. *Learns:* whether PLA's clutch
  survives repeated assembly, or creeps away. No public data exists on this in either direction.
- **LG-B1 — first patterned brick.** A 4×4 eight-fold piece at defaults. *Learns:* whether relief
  and clutch coexist; the first object that is both a real LEGO part and a real Islamic pattern.
- **LG-B2 — off-grid anchor.** A five-fold rosette piece anchored by two tubes, with wall ribs where
  the inset outline permits. *Learns:* whether rotation lock holds when the outline is
  incommensurable with the lattice, and **how much clutch is lost by giving up the tangent side
  wall** (§3.3's census says 50–67 % of contacts on this footprint class) — **the load-bearing bet
  of the whole anchor-only approach.**

Catalog rules apply: every entry needs ≥1 question answerable by measuring the object; nothing is
marked answered from a slicer preview; a failed print is a logged result.

## 9. Lego Lab — the page

A copy of `packages/lab`'s structure — a template, not a framework: hand-written HTML, plain DOM,
module-scope state, one `style.css`, zero UI dependencies, same 12-file layout. Reused verbatim
from `@naqshcoffee/bikar-knobs`: `renderKnobPanel`, `syncKnobPanel`, `applyConstraints`,
`clampToSpecs`, `MACHINES`/`loadPrintTarget`, `encodeBkr`/`decodeBkr`. New cross-param rules (relief
depth vs ceiling; `engage` vs bridging) go in `knobs/src/constraints.ts` beside the two orb rules,
per the ADR that put the knob layer in its own workspace package.

`viewer.ts` is reused unchanged — the Canvas-2D painter takes a mesh and a brick is a mesh. **No
three.js.** One addition: a **lattice overlay** in the top-down view drawing the 8 mm grid under the
piece with stud centres, engaged-vs-unengaged cells, and surviving/rejected anchor positions marked,
so §5.2's solve is visible rather than asserted.

New surface unique to this Lab:

- a **grid-gate panel** beside the mesh-gate panel — PASS/FAIL, anchor count and kind, min anchor
  wall, `studsEngaged`, rotation-lock ✓, then grid fit, its argmax rotation θ*, snap residual,
  repeat unit;
- a **sweep strip** — `sweepGridFit` plotted against the swept param, sweet spots clickable to set
  the knob;
- **multi-part export** when a pattern decomposes into several pieces (the CLI already has
  `--format parts`).

Because clutch depends on filament and moisture as much as on printer (§3.5), the fit-profile
selector must name the *spool*, not just the machine, and the panel must say when the active profile
came from a coupon and when it is a default.

Protocol: `LabResponse.family` gains `'brick'` in `packages/lab/src/protocol.ts` and
`previewResponse` learns `result.brick3d` — an extension of the existing union, not a fork (§2).
URL schema, debounce, stale-while-revalidate, worker watchdog, size guard, and the preset↔custom
byte comparison carry over unchanged.

Two things the wiring settled that this section had left to the reader.

**The mesh gate runs against the brick's own floor.** A brick's thinnest feature is its anti-stud
tube wall, and on the default fit that is 0.757 mm — a dimension the LEGO system fixes, not one the
design chose. The shipped 1.2 mm FDM floor would therefore fail every dimensionally-correct brick,
so the Lab passes `brick3d.featureFloorMm` (§7.4's 0.70 mm invariant) exactly as the CLI's `--check`
does.

**Validator:** a brick's mesh-gate verdict counts only if the floor it was judged against is the
brick floor, and the panel shows both numbers.

PASS: default `StarBrick` — `gate.minFeatureMm = 0.70` (the brick floor) with
`gate.declaredMinFeatureMm = 0.757` (the tube wall), verdict PASS. Printable, and visibly exempt.

FAIL: the same brick judged at `gate.minFeatureMm = 1.2` — verdict FAIL on a dimensionally-correct
part. A panel showing the verdict without the floor reads that as a geometry bug, and the recourse
it implies — widen the wall — breaks LEGO compatibility.

**The fit set travels with the result, not just a measured/unmeasured flag.** §9's honesty condition
is per value — *this* number came from a coupon, *that* one is still a default — so `LabBrick.fit`
carries the whole `BrickFit` including its per-field provenance, and the panel answers each row with
`fitProvenance(fit, field)`. `isWhollyUnmeasured(fit)` remains the banner. Carrying a boolean
instead would have made the banner the only thing the UI could honestly say.

## 10. Phasing

| Phase | Where | Contents |
|---|---|---|
| **R0** | 3d-models | Survey → this doc → grounding audit → v2. ✅ **Complete.** |
| **Q3** | bikar | Holed-pattern check against the union ring (§11 Q3). ✅ **Complete — M7 unblocked.** |
| **LG-F1/F2/R1** | physical | Clutch coupons. **No longer block M6** — see the note below. |
| **M6** | bikar | `brick` declaration (parser, AST, evaluator, `brick3d`), `kernel3d/brick.ts` incl. §7.6 ribs, LEGO fit entries, language-reference + ADR. ✅ **Complete.** |
| **M7** | bikar | Anchor solver, `kernel3d/grid-gate.ts`, `sweepGridFit`, `family: 'brick'`. Kernel and gate shipped early with M6; the protocol wiring followed. ✅ **Complete.** |
| **P0** | both | Lego Lab core: page, presets, knobs, viewer + lattice overlay, both gate panels, STL download, `make lego-lab`, gallery §03. First shippable. ✅ **Complete.** |
| **P1** | both | Compatibility matrix filled by sweeps, sweep-strip UI, multi-piece export, more curated scripts. Sweep strip ✅ **shipped** (bikar `617bee1`, PR #34), design-notes page (§12) and studio index (§13) ✅ **shipped**; multi-piece export ✅ **shipped** as studs-as-ports ([`decisions-log.md`](decisions-log.md) D-006) — V11, port minting, the entry contract and `patterns/Assemblies/Brick-Stack.bkr`; the compatibility matrix ✅ **measured** (bikar `3ad9158`, PR #37) and §5.3 rewritten from it ([`research/lego-lattice-matrix-sweep.md`](research/lego-lattice-matrix-sweep.md)); the curated scripts ✅ **shipped** (bikar `954b5c8`, PR #38) — `Hex-Field-Tile` at fit 0.48 and `Rational-Repeat-Tile` at 1.00 on a 3 : 2 lattice, one click each from the matrix rows they illustrate. ✅ **Complete.** |
| **P2** | both | Custom mode: code drawer, `code=` share links, Open in Studio, localStorage draft. |
| **P3** | both | Polish: per-family print notes, adjusted-parameter toasts, LDraw `.ldr` placement export (survey §6 — a text emit, one line per piece). |

**Why the coupons stopped being a gate.** This table originally put LG-F1/F2/R1 before M6 because
the coupons settle the dimensions M6 would otherwise have to guess. That ordering is right for a
**baked constant** and wrong for a **knob**: LG-F1 is itself a parameter sweep — §8 specifies it as
a five-rung `ribMm` ladder crossed with three `engage` values — and the Lab runs the same sweep
without a new plate. So the dependency inverts. M6 and M7 ship with every disputed value adjustable
and provenance-tagged, the coupons become the Lab's first *input*, and each print narrows a knob
rather than unblocking a phase. Recorded as
[`decisions-log.md`](decisions-log.md) D-005, which supersedes D-003.

The condition that keeps this honest is already in §9: the panel must say, per value, whether the
active number came from a coupon or is still an unmeasured default. A `CAL-*` id with no measurement
behind it has to read as *unmeasured* in the UI. Without that, "adjustable" silently becomes
"asserted", which is the thing deferring M6 was meant to prevent.

### Implementation status

**R0 — research and grounding — 2026-07-29.** `docs/research/lego-brick-system-survey.md` (field
survey, LDraw library read first-hand), `docs/lego-lab-design.md` v1 → v2,
`docs/research/lego-lab-grounding-audit.md` (audit preserved verbatim),
`.claude/skills/prototype/catalog.md` (LG ladder). Design changes forced by the audit: clutch rib
promoted to a first-class kernel feature (§3.8, §7.6); `engage` default 1.6 → 3.2 (§3.6); grid-fit
measure rebuilt on repeat-vector components with a rotation search (§5.3); `studsEngaged` and the
non-rectangular body partition specified rather than assumed (§5.2, §7.2); V5b and V10 added; LG-F1
re-scoped to sweep rib thickness; LG-D1 added. Commits: 3d-models `4c3b900`; bikar *(none —
R0 ships no code)*.

**M6 — the `brick` declaration and the brick kernel — 2026-07-31.** bikar `61c371f` (PR #27), which
squash-merged the branch this landed on: Q3's answer as a test; self-checking caps and
symmetric-difference slab interfaces; `lego.ts`, `grid-gate.ts`, `brick.ts` and `brick-validate.ts`
with V1–V10 and `RIB_MM_CAL` under `CAL-RIB-01`; then the grammar, evaluator, CLI report and
`patterns/Lego/Star-Brick.bkr`. 3d-models: this revision.

*(An earlier revision of this section cited the five branch commits by hash. The squash collapsed
them, so none resolve on `main` any more and all five have been replaced by the merge commit. The
lesson is general and worth stating once: **cite the commit that will exist on the default branch,
not the one you are standing on** — under a squash-merge policy those are never the same object.)*

Deliberate deviations from this spec, each corrected in place above and each found by building the
thing the spec described: §4's `origin at (<col>,<row>)` → `at <col>[,] <row>`, with the comma
mandatory for a negative row; §4's default `engage` shown not to fit a `1 plate` body; §7.1's
three-slab table shown to be a four-slab stack under relief; §7.2's per-cell interface replaced by
the symmetric difference, plus the anchor carry-through, the pocket nesting/drop rule, and the
stud-tangency constraint; §7.3's coordinate identity shown to be necessary but not sufficient;
§7.4's "`minFeatureMm` override of 0.8" replaced by a declared minimum against a 0.70 invariant.

Beyond the spec: `M7`'s anchor solver and grid gate shipped here rather than after M6, because V5b,
V7 and V8 cannot be written without them — a validator that cannot be run is not a validator. The
graduation rule was honoured throughout: every correction above has a test that fails before the
fix and passes after, and the two triangulation fixes were each verified by neutering the fix and
confirming the test goes red.

**M7 — the Lab protocol wiring — 2026-07-31.** bikar `61c371f` (PR #27, the same squash): `family:
'brick'`, `LabBrick`, `brickResponse`, and the `kernel3d/index.ts` brick surface. 3d-models: this
revision. The anchor solver, `grid-gate.ts` and `sweepGridFit` had already shipped with M6 for the
reason above, so what landed here is the boundary: the response payload, the barrel, and the two
facts §9 had left implicit.

Deliberate deviations, both corrected in §9 above and both found by building the thing: the Lab must
gate a brick at `brick3d.featureFloorMm` rather than the shipped 1.2 mm floor, or every
dimensionally-correct brick reports FAIL — the test asserts the substituted floor, not just the
verdict, so a regression to the generic floor goes red rather than silently passing on a thicker
part; and `BrickProvenance` now carries the `BrickFit` the mesh was emitted against, because §9's
per-value coupon-vs-default question cannot be answered from a boolean, and re-fetching the module
default is the drift the provenance record exists to prevent.

Beyond the spec: `kernel3d/index.ts` exported nothing from `brick.ts`, `brick-validate.ts`,
`grid-gate.ts`, `lego.ts` or `solidify-slabs.ts`, so the Lab could only have reached the kernel
through a deep path. The barrel now carries the whole brick surface — the lattice constants the
overlay draws, both gate reports, the anchor solve, and `sweepGridFit` for P0's sweep strip.

**P0 — the Lego Lab page — 2026-07-31.** bikar `61c371f` (PR #27: `lego.html` as `packages/lab`'s
second Vite entry, `lego-main.ts`, `lego-scripts.ts`, `lattice-overlay.ts`, `fit-profile.ts`,
`lego.css`, the four new `patterns/Lego/*.bkr`, the two brick constraint rules, and the
`fit-profile` / `lego-presets` / `anchor-candidates` / `lego-lab.spec.ts` suites) and `ae8deb1`
(PR #28 — the two fit-row defects below). 3d-models: this revision — `make bricks`, `make lego-lab`,
`build/brick_previews.py`, `src/Lego/*.bkr`, and gallery §03.

Deliberate deviations from this spec:

- **§9's page is a second Vite entry, not a workspace package.** §2 forbids forking the worker, the
  protocol or `evaluate.ts`; a second package would have had to either fork them or invent a shared
  one. A second `input` in `vite.config.ts` reuses all three as source files. The cost is that both
  Labs share one hashed `assets/` dir, which is why `lab` and `lego-lab` are two names on **one**
  Makefile recipe — two recipes would mean two `rm -rf assets`, and the second would delete the
  chunks the first page was linked against.
- **P0 needed a `make bricks` target §10 does not name.** §10 lists `make lego-lab` and "gallery
  §03" as one line, which reads as though the page carries the section. It does not: a gallery card
  needs an STL to download, a preview to show and a `.bkr` to link, and none of those exist until
  something renders them. `make bricks` drives the bikar CLI over `patterns/Lego/*.bkr` with
  `--check`, vendors each source into `src/Lego/` (matching the tracked `src/Orbs/` convention), and
  records the stems in `build/.brick-names` so the preview step previews bricks and not the orbs and
  cutters sharing `build/stls/`. Shipping §03 with dead links would have been worse than not
  shipping it.
- **Brick previews are a mesh render, not a validation view.** The orbs get axis views because
  qiyas composites them; there is no brick view set and no brick composite, and a brick's claim is
  made by its two grid gates and the mesh gate, not by a picture. So `brick_previews.py` renders the
  STL through OpenSCAD's `import()` at the Cornfield preview colours the existing
  `process_images.py` already keys to transparency — the gallery's image chain, reused whole, with
  no second pipeline.

Two defects, both shipped in #27, both invisible to `fit-profile.test.ts`, and both found by opening
the page rather than by reading the suite:

1. **Every fit row was titled `studDiaMm`.** `renderKnobPanel` derives a title from
   `spec.name.replace(/_/g, ' ')` — correct for a DSL param, inert on camelCase. `fitLabel()`
   existed and was unit-tested, but nothing called it on the path to the DOM.
2. **The "measured" toggle sat beside the field name instead of under its value.** The toggle is a
   `<label>`, so `style.css`'s `.knob-row label { grid-area: label }` (0-1-1) outranked
   `.fit-measured` (0-1-0) and put the control in the row's title cell — attaching a provenance
   control to the wrong thing, which is precisely what §9's per-value honesty condition forbids.

Both are now pinned by a seventh case in `lego-lab.spec.ts`, asserting rendered title text and the
toggle's computed `grid-area`. It is an e2e test because neither defect is reachable without a
browser: one needs the shared panel to have rendered, the other needs the cascade resolved. Each fix
was neutered in turn and the test confirmed red, then restored and confirmed green.

The general lesson, and the reason this is written down rather than just fixed: **a unit-tested
helper is not a rendered one.** Both defects live in the gap between a function that is correct and
a DOM that never calls it, and no amount of data-layer testing closes that gap. The Lab's honesty
claims are claims about what a reader *sees*, so at least one test per claim has to look.

**P1 (part) — the multi-piece decision and V11 — 2026-07-31.** bikar `617bee1` (PR #34: the
design-notes page §12, the studio index §13, and the `multi-piece-export` note as `preview`) and
`3b31fab` (PR #35: V11, and the same note closed to `decided`). 3d-models: this revision, plus
[`decisions-log.md`](decisions-log.md) D-006 and the
[`design-note`](../.claude/skills/design-note/SKILL.md) skill.

Multi-piece export is **decided, not built**: `export parts` on a `brick` assembly is studs-as-ports
— a stud mints an outward port and the tube beneath the ceiling mints its mate, so the joint names
geometry the kernel already emits. What that costs, and is accepted rather than discovered: two new
port kinds, a stud-index naming scheme that survives a footprint change, a pose solver for the
assembled preview, and a printed-onto-printed rung on the clutch ladder. It reverses on a
measurement — if no rung of that ladder holds, a stud is a shape and not a joint.

The defect that forced the decision is the reason V11 exists. Scoping the export found that a
`brick` accepted a dimensioned `port`, an `assembly` would `connect` a rod into it, and the C2 fit
ladder **passed** — while `buildBrick` reads no ports at all. The mesh was identical with and
without the port (3764 triangles either way), so nothing in the repo could see it except a print.
Graduation rule honoured: `brick-phantom-port.test.ts` fails before the fix and passes after, and
its last case asserts the plain brick is watertight *and* that the ported one no longer compiles —
so there is no pair of meshes left to be identical.

Beyond the spec: the three options were argued as a **design note whose figures are compiles**, not
drawings — each section is `compileToGeometry(...).brick3d` run through `brickSection()` at page
load, with hand-authored marks confined to a dashed overlay list. That the *real hole* option's bore
crosses load-bearing material between two solver-placed tubes is visible on the drawing because the
drawing is the part. The practice is now a skill, and its parity rule — a note's `<figure>` count
equals its `Compiled from` count — is enforced by `tests/design-notes.test.ts` rather than
remembered.

**P1 (part) — studs-as-ports built — 2026-07-31.** bikar `c60faf2` (PR #36). 3d-models: this
revision, plus the `LG-S1` coupon in
[`prototype/catalog.md`](../.claude/skills/prototype/catalog.md).

D-006 is now geometry that renders. A `brick` mints its own ports from the lattice it already
built — `stud_c<col>r<row>` on the top face, `anti_c<col>r<row>` on the bed — and
`patterns/Assemblies/Brick-Stack.bkr` decomposes into two piece-local STLs at 3764 triangles each,
both mesh-gate PASS. Three of the four costs the decision accepted turned out not to be costs: the
pose solver and `export parts` were already generic over the piece registry, so the only real work
was the minting. The naming scheme is the one cost that was real, and it is a **lattice coordinate,
not an ordinal** — under `stud0…stud7` a 2×4 widened to a 2×6 renumbers every stud past the first
row and an assembly written against the narrow brick silently re-points; under `stud_c1r3` it does
not.

Two things beyond the spec. The receptacle is **measured, not assumed**: `clearRadiusMm` is the
minimum over the placed anchors and the shell wall, so a corner cell reports tighter than an
interior one and a brick the solver gave no anchors (a 1×1) mints no anti-stud ports at all — there
is nothing bounding the cell to offer. And the evaluator grew a **warning channel**
(`assembly3d.warnings`, printed on stderr by both CLI paths), because the contract found something
that is neither fatal nor silent.

**What it found, which is the reason the build was worth doing.** On the shipped fit defaults a
printed brick stacked on a printed brick has **zero** interference: `stud.d/2 − clearRadius + rib`
comes to 0.00 mm at a wall-bound corner cell. The −0.2 mm diametral offsets are calibrated for a
printed part meeting a **moulded** one, where only one side shrank; brick-onto-brick applies them
to both sides and the clutch cancels. `brickFit { studDiaMm 0 }` applies them once and the joint
clutches again. This is a **K10** in the shipped code rather than in a doc — a constant carried
across processes with no sentence saying what must hold for it to transfer — and it is now written
in four places that a reader of any one of them will hit: the port module, the test, bikar's
`docs/language-reference.md`, and the pattern header. `CAL-STK-01` is the bet on where the real
ceiling sits and **LG-S1** is the coupon that settles it; `STUD_ENTRY_MAX_MM = 0.15 mm` is a guess
until it prints.

The error/warning split follows the line §7.4 already draws: a part that cannot be pushed together
is not a part (error above the ceiling), a part that assembles without grip still prints and still
stacks (warning at or below zero interference).

Graduation rule honoured twice. `brick-ports.test.ts` (12 cases) pins the naming invariant, the
measured receptacle, the no-anchors case, and both sides of the entry contract. Separately,
`--format parts --check` was found to refuse **every dimensionally-correct brick** on its 0.757 mm
tube wall: the 1.2 mm floor is a bet about struts, the single-STL path already exempted a brick, and
the parts path had no way to say so. `PlacedPart.featureFloorMm` carries the exemption per part —
per part, not per assembly, so a tile sharing an assembly with a brick cannot borrow it — with a
test that asserts the brick parts carry a floor and `Pinned-Tiles.bkr`'s parts carry none.

**P1 (part) — the compatibility matrix measured — 2026-07-31.** bikar `3ad9158` (PR #37:
`scripts/sweep-lattice-matrix.ts`, `packages/core/tests/kernel3d/lattice-matrix.test.ts`).
3d-models: this revision's §5.3, plus
[`research/lego-lattice-matrix-sweep.md`](research/lego-lattice-matrix-sweep.md).

§5.3's table shipped an **Expected** column and a prediction in a table reads exactly like a
measurement in one. It is now a **Measured** column: five bases over one shared interval, 2–20 mm
at 0.005 mm, θ maximized by `gridFit`. Four of the five predictions hold as written.

The fifth was not testable as the table was built. The hexagonal row predicts *one axis snaps, the
other plateaus* — a claim about the two axes separately — and `gridFit` scores the **worst** axis,
so its argmax necessarily lands where the two residuals balance: 0.785 / 0.785, the one place the
asymmetry cannot appear. The measurement had to be shaped to the claim rather than the claim read
off the nearest available number, so the script also probes at the scale that makes the first basis
vector exactly one pitch. There the prediction is exact: **0.000 mm against 4.000 mm.**

Two corrections to the surrounding prose fell out of the run. "At the right scale" is **plural** —
`square` scores 1.0 at every divisor of the pitch in range, so a sweep window straddling none of
them draws a flat curve for a lattice that registers perfectly, which is a thing the sweep strip
must not let a user misread. And a **good score with a withheld repeat unit is consistent**, not a
bug: `hexagonal` scores 0.8037 and still reports no repeat unit, because the score is about
registration and the repeat unit is about axis alignment.

One claim was deliberately *not* strengthened. §5.3's rhombic row says "never reaches 1 at any
scale"; the sweep searched 2–20 mm and can only say **max 0.7264 over that interval**. The
unbounded version still stands on cot 36° being irrational — an argument, not this table — and the
doc now attributes it there. Writing the measured number as though it settled every scale would be
a K2 wearing a measurement's clothes.

The graduation artifact is `lattice-matrix.test.ts` (7 cases), which pins every number §5.3
publishes and **imports the script rather than re-deriving the bases** — a test that rebuilt them
would pass while the table and the kernel disagreed, which is the drift it exists to catch.

**P1 (complete) — the curated scripts — 2026-07-31.** bikar `954b5c8` (PR #38:
`patterns/Lego/Hex-Field-Tile.bkr`, `patterns/Lego/Rational-Repeat-Tile.bkr`, two cases in
`packages/lab/tests/lego-presets.test.ts`). 3d-models: this entry, the §10 P1 row, and two gallery
cards in `index.html` §03. **This closes P1.**

The matrix above is a table of numbers no visitor can reach. P0's five presets could show a fit of
1.00 and a fit of `n/a`; they could not show the middle, where a piece **scores badly and is still
correct** — which is the whole reason V8 is a warning and not an error. The two new presets are
each one matrix row made clickable.

`Hex-Field-Tile` is `Grid-Field-Tile` with `mode hex` substituted and *nothing else changed*, so
the pair isolates the lattice as the only variable. It lands on the sweep's fixed-scale hexagonal
probe: **fit 0.48**, 15 tube anchors, anchor gate PASS. `Rational-Repeat-Tile` answers the
conclusion that pair invites — that registering means being square — with **fit 1.00 on a 3 : 2
lattice** and a repeat unit of 3 × 2 studs.

Two findings from building them, both deliberately left where they are. The hexagonal preset first
scored **0 of 16** tube anchors, and the cause was field size against footprint margin, not the
lattice: `repeat_x/y 4` in a 5 × 5 covered every crossing, and `3` in a 6 × 6 passes. The
motif-radius sweep that looked like the obvious knob changed nothing. Separately, with a **hexagon**
motif it emitted 5–6 degenerate triangles and with the **diamond** it ships with, zero — the three
existing tiled presets all baseline at `degenerate=0`, so this was introduced. Isolating it,
`voids detect` off still fails, `mode rectangular` still fails, a tiled sweep over n=3..12 fails
only at n=6, and a *single-polygon* repro fails at n=4 and passes at n=6, the opposite. That makes
it position-dependent sliver behaviour in the solidifier rather than a rule about hexagons, and it
is carried to §11 as an open question instead of being half-diagnosed here.

The graduation artifact is the two preset cases, which pin each preset to the row it illustrates —
including `repeatUnitStuds` as **null rather than absent**, because withholding an answer is not
the same as scoring zero and the field has to say which it is.

*(Each later phase appends an entry here carrying commit hashes in **both** repos, deliberate
deviations from this spec, and additions beyond it.)*

## 11. Open questions

- **Q1 — is true scale printable on this machine at all?** If LG-F2 says studs will not resolve at
  0.4 mm, `studs full` and `studs edge` ship disabled with a documented nozzle requirement, and
  `studs none` carries the feature. **The "just use a finer nozzle" fallback has one direct
  counterexample and no supporting evidence:** Brickset printed the same brick at 0.2 mm/0.1 mm
  layers and 0.4 mm/0.2 mm layers and reported clutch "slightly better on the red bricks than the
  green, which have hardly any at all" — the red are the **0.4 mm** ones. A commenter attributes
  that clutch to first-layer **elephant's foot**, i.e. an uncontrolled defect rather than geometry.
  So Q1's answer may be "neither nozzle, without a rib" — which is §3.8. Decided by coupon.
- **Q2 — pin vs tube strength under FDM anisotropy.** A ⌀3.2 solid pin printed in layers may shear
  where a moulded one does not, and two independent makers report 1×N prints too loose (§3.3).
  LG-R1 decides whether 1×N footprints are supported in M6 or deferred.
- **Q3 — does `unionPatternFaces` always return a ring the anchor test can use? — RESOLVED, yes.**
  Measured against a deliberately-holed pattern (a 50 mm square with a nested 15 mm square, no
  edge joining them) in `bikar:packages/core/tests/kernel3d/piece-e2e.test.ts`. The question as
  written named the wrong mechanism and drew the wrong conclusion from it, so both are corrected
  here.

  *Mechanism.* The void is not "cancelled away". `getBoundedFaces` returns **every non-outer
  face**, and in a planar subdivision an enclosed void *is* a bounded face — so it arrives as
  material, tiles edge-to-edge with its neighbours, and the union never sees a hole at all. The
  `holeCount > 0` guard cannot fire on a nested void; it fires only on a gap the faces genuinely
  fail to cover, which one subdivision does not produce.

  *Conclusion.* The ring and the mesh **agree** — the extrusion really is solid across the void
  (measured volume 25000 mm³, the full solid; a preserved void would give 22750). So an anchor
  placed by that ring sits in real material, and the failure Q3 feared does not occur. **M7 is
  unblocked, and so is §7.2's inset**, which had the same supposed exposure.

  *What is actually lost is fidelity, not soundness:* art drawn as a void prints filled, silently.
  That is unfixable at this layer rather than merely unfixed — a nested subgraph component is the
  same input whether the author meant a void or a decorative overlay, `Nail-Tile.bkr` depends on
  the overlay reading, and the DSL has no word separating them. `hole` is the supported way to ask
  for a void, which is what the sibling `uncovered hole` error already advises.
- **Q4 — the bridged cavity ceiling.** `engage 3.2` (§3.6) puts the sagging surface 1.6 mm clear of
  the host studs, which is the minimum that works. But span still scales with footprint: a 2×2
  cavity bridges 12 mm, a 6×6 bridges 44 mm. Brick Architect's directional result — the printed
  **anti-stud side** is what fails — says this is where large pieces will break. May need a
  footprint-dependent warning or internal ribbing.
- **Q5 — should `auto` footprint round up or refuse?** Rounding a 33 mm pattern up to 5 studs
  (39.8 mm) leaves a 3.4 mm dead border. Refusing forces the author to rescale. Leaning: round up,
  warn, and let the sweep strip show the scale that lands on 4 studs.
- **Q6 — a geometry-only gate structurally cannot score clutch.** Clutch is elastic: it depends on
  wall and tube *flexure*, material stiffness, moisture, and layer adhesion (§3.5, §3.8). `gridGate`
  measures geometry. **`anchorability: PASS` must therefore not be read as "will clutch"**, and the
  Lab panel must say so in words rather than implying it with a green tick. Whether a compliance
  proxy (rib deflection × count, or an FEA-lite bending estimate) is worth adding is open; LG-F1 and
  LG-D1 supply the data that would calibrate one.
- **Q7 — position-dependent degenerate triangles from relief pockets.** Building `Hex-Field-Tile`
  (§10, P1) turned up a mesh-gate failure — 5–6 zero-area triangles — that depends on *where* a
  motif sits, not on what it is. A hexagonal motif (n=6) tiled into the field fails; the diamond
  (n=4) the preset ships with passes; `Grid-Field-Tile`, `Edge-Stud-Tile` and `Star-Brick` all
  baseline at `degenerate=0`, so it is introduced rather than latent. The narrowing that matters is
  the one that *rules out* the obvious explanation: disabling `voids detect` still fails, switching
  to `mode rectangular` still fails, a tiled sweep over n=3,4,5,6,7,8,12 fails **only** at n=6 —
  and a single-polygon repro fails at n=4 and passes at n=6, the exact opposite. So "hexagons are
  broken" is false, and the real shape is slivers produced when a pocket boundary lands near
  another edge. Needs a minimal repro driven from the solidifier rather than from a preset.
- **Q8 — §5.3's rhombic row is not expressible in the `tile` grammar.** `env.repeatVectors` is
  assigned in exactly one place, `packages/core/src/dsl/evaluator.ts`, and it admits exactly two
  basis shapes: `[(dx,0), (0,dy)]` for `mode rectangular` and `[(dx,0), (dx/2,dy)]` for `mode hex`.
  A 72° rhombic basis is neither. The measured matrix therefore reports a lattice **`gridFit` can
  score but no `.bkr` can produce** — the sweep reaches it by constructing the basis directly. That
  is not wrong, but it is a gap between a table and the machinery the same document ships, which is
  what K7 is about, so it is written down here rather than left for a reader to discover. Three ways
  out: widen the grammar with a general two-vector basis, or mark the row in §5.3 as
  kernel-reachable-only, or drop the row. **Resolved: label the row** —
  [`decisions-log.md`](decisions-log.md) D-007. §5.3 gains an **Authorable** column and the
  sentence saying why; the grammar is unchanged; the row stays, because it is the 5-fold case an
  Islamic-pattern reader will look for. The three options were drawn side by side, with the
  geometry compiled, in the `lattice-basis` design note (§12).

---

## 12. Design notes — the argument, with the geometry compiled beside it

P1 had to settle multi-piece export (§10), and the way that decision got made is the same way §3.8
and §5.3 got made: write the options down, draw them, cost them, choose. What was missing was
anywhere to *put* that once it was written. A transcript is not a place; a design doc section is
the right place for the conclusion and the wrong place for three side-by-side figures.

`design.html` is that place — a fourth page in `packages/lab`, built by the same Vite config as
`lab.html` and `lego.html`, carrying one `DesignNote` per decision from
`packages/lab/src/design/notes/`.

**The figures are compiled, not drawn.** A hand-authored SVG of a brick section is a *claim* about
the brick that nothing checks, and it stays on the page long after the geometry it depicts has
moved. So `brickSection()` in `packages/lab/src/design/draw.ts` takes the `BrickProvenance` that
`compileToGeometry(source).brick3d` returns — the same record the Lab's gate panels read — and cuts
a section from it: cavity, ceiling and stud bands come out of `stackBrickSlabs`, the anchor spans
out of the solver's placements, the dimension leaders off the numbers the kernel computed. Nothing
in `draw.ts` knows a brick's dimensions; it only knows how to draw one it is handed.

This buys the property the notes exist for: **a note whose argument has expired breaks loudly.**
Change the anchor solver and the figure changes with it, or the note stops compiling. It does not
quietly keep showing last month's brick.

It also costs something, and the cost is worth naming rather than discovering. A compiled figure
can only show geometry the kernel builds **today**. A note arguing for a capability we do not have
yet — which is most of what a decision note argues about — has exactly one option it can draw from
life, and the alternatives have to be drawn schematically. The rule that keeps that honest is that
the caption says which it is: every `<figure>` carries a provenance line naming the pattern and the
cut plane it came from, or saying plainly that it is a sketch of something not yet buildable.

**Validator:** a note's figure count and its provenance-line count are equal, and
`tests/design-notes.test.ts` fails when they are not.

PASS: the multi-piece-export note as it ships — three figures, three provenance lines, the
buildable option's line naming the compiled source and the other two marked as sketches.

FAIL: a fourth figure added to argue a fourth option, with no fourth provenance line. The suite goes
red on the commit that adds it — which is the only moment anyone still knows whether that figure was
compiled or drawn. Without this check the note degrades in the one direction that matters: a sketch
gradually reads as a measurement.

A note carries `status: 'open' | 'decided' | 'superseded'` and, when the status is not `open`, the
decision it records. That pairing is asserted rather than remembered, because a note that argues
three ways and never says which way it went is the failure mode this page would otherwise
institutionalise. Notes are ordered newest-first by an ISO date, and the ordering is asserted too —
a hand-ordered list of documents is a list that will eventually be wrong about which decision is
current.

**Where the decision itself lives is unchanged.** A note is the *argument*; the outcome still goes
to [`decisions-log.md`](decisions-log.md) as a `D-NNN` entry and, when it changes the design, into
the relevant section here. The note is not a third register — it is the worked page a `D-NNN` line
compresses.

### 12.1 Published so far

| Note | Argues | Status |
|---|---|---|
| `multi-piece-export` | How an assembly leaves the Lab as separate solids | **decided** — studs as ports ([`decisions-log.md`](decisions-log.md) D-006) |
| `lattice-basis` | §11 Q8: the matrix row the `tile` grammar cannot build | **decided** — label the row ([`decisions-log.md`](decisions-log.md) D-007) |

`lattice-basis` extends the page's "compiled, not drawn" rule to a second kind of figure, and the
extension is worth recording because it is not the same mechanism. `brickSection()` is handed a
`BrickProvenance` and draws what the kernel already built. A lattice plan has no solid to be handed:
`packages/lab/src/design/draw-lattice.ts` calls `gridFit` **itself**, rotates the basis to the
argmax angle the report returns, and draws, per repeat vector, the dashed **L** to the nearest stud
centre — where the two legs *are* the two component residuals and the labelled one is the leg the
score used. The figure is not illustrating the measurement; it is the measurement, rendered.

Two things that discipline forced, both of which were defects first:

- **A figure must name its scale.** §5.3's headline column is a *maximum over a 2–20 mm sweep*, so
  captioning an 8 mm drawing with 0.8037 would have been exactly the K1 the page is about. The
  families are functions of scale, and each is drawn twice — at the size an author reaches for
  first, and at the size the sweep found best. That pair turned out to carry the argument: the same
  3 : 2 rectangular lattice scores **0.41 at 8 mm and 1.00 at 16 mm**, while hexagonal tops out at
  **0.8037** at any size, because no scale repairs an irrational ratio.
- **A comparison must not vary its frame.** The two figure-vs-figure rows use a new `.pair` class
  rather than `.split`, whose `380px 1fr` columns are deliberately asymmetric for figure-plus-prose
  and would have made the right-hand drawing bigger than the thing it is being compared to.

The drift risk this note carries is its own: the four lattice families are written out again in
`draw-lattice.ts` because the note is bundled for a browser while `scripts/sweep-lattice-matrix.ts`
is a node entry point. `packages/lab/tests/design-lattice.test.ts` is the whole mitigation — it
imports the script and compares the two at four scales per family, rather than restating the bases
a third time and passing while the published table disagrees.

## 13. The studio index and the page catalogue

Four pages is the point at which "which page do I want?" becomes a real question, and the honest
answer is not a list of filenames — it is *who each page is for and what they walk away with*. That
is the actor/use-case map's question, already answered, in
[`../.claude/skills/maintain-use-cases/use-cases.md`](../.claude/skills/maintain-use-cases/use-cases.md).
So the index does not invent an answer; it points into that one.

`studio.html` is rendered entirely from `packages/lab/src/catalog.ts`, which holds every page, the
actors it serves, and one `does` sentence per actor per use case. There is no second list of pages
in the renderer to drift from it.

**An index maintained by hand goes stale on the day someone adds a page and does not notice, and a
stale index is worse than none** — it is confidently wrong about what the site can do. Two checks
remove the hand:

1. `packages/lab/tests/catalog.test.ts` reads the directory. Every `*.html` beside `vite.config.ts`
   must be a `PAGES` entry *and* a Rollup input, and every entry must name a file and an entry
   module that exist and reference each other.
2. `.claude/skills/maintain-use-cases/validate.py` reads the `uc:` ids out of that catalogue at the
   pinned `as_of` commit and fails when one of them is not a use case the map carries. The map is
   the register of what this system does for whom; a page may point into it and may not invent
   entries in it.

Check 1 lives in bikar because that is where the pages are; check 2 lives here because that is where
the map is. Neither is a new gate — check 2 is a rule inside the `maintain-use-cases` validator the
repo already runs on every commit, per this repo's standing precedent that a measured recurrence
earns [a gate rather than a skill](dsl-extension-skill-evaluation.md).

**Validator:** the index is complete exactly when the catalogue and the package agree, in both
directions.

PASS: `design.html` added as a fourth page — catalogued, listed as a Rollup input, entry module
present and referenced. Suite green, and the card appears on the index without anyone editing the
index.

FAIL: a `sweep.html` dropped into `packages/lab` with no `PAGES` entry. `catalogues every html page
in the package, and no page that is not there` goes red — verified by construction, not by
inspection. The converse also fails: a `PAGES` entry for a page that was deleted fails the same
assertion from the other side, which is what stops the index advertising a dead link.

The `does` sentences carry a length floor of 60 characters, and the number is chosen to sit just
under an ordinary use-case title: UC7's — *"Validate bikar renders against ground truth per symmetry
axis"* — is 61. A `does` short enough to fail the floor is therefore shorter than the title the
reader already has from the id chip beside it, which means it restates the id instead of saying what
the person leaves with. This is a lint threshold, not a measured constant, and it is written down
here so that it stays a decision rather than becoming a habit.

**Unserved actors stay on the page.** The catalogue carries all seven actors the map names, and the
four with no page in this package — Gallery visitor, Studio author, Baker, qiyas validator — carry
an `elsewhere` string saying where they *are* served. The test pins `elsewhere` present exactly when
the actor is unserved, in both directions, so an actor cannot silently become unserved when a page
is deleted. An index that lists only the actors it has pages for quietly implies the rest of the
system does not exist; "nobody has built this" and "this is served elsewhere" are different answers
and a reader deserves to be told which.

The index page itself carries no use case. Navigation is not something a person accomplishes, and
minting a UC for it would put an entry in the map that no code delivers.

---

## Appendix A — sources

Full survey with derivations: [`research/lego-brick-system-survey.md`](research/lego-brick-system-survey.md).
Adversarial audit, preserved verbatim: [`research/lego-lab-grounding-audit.md`](research/lego-lab-grounding-audit.md).

**Primary, read in full**

- Official LDraw parts library (complete zip, 24,297 parts / 1,775 primitives) — `p/stud.dat`,
  `stud2`, `stud3`, `stud4`, `stug3-1x3`, `box5`; `parts/3001`, `3003`, `3004`, `3005`, `3010`,
  `3023b`, `3068b`, `3070b`, `733`, `6934` and their `parts/s/*` subfiles.
  https://library.ldraw.org/library/updates/complete.zip
- US Patent 3,005,282 "Toy Building Brick", filed 1958-07-28, granted 1961-10-24. **Claims 1–3
  disclaimed by Interlego AG, 1978-03-31.** https://patents.google.com/patent/US3005282A/en
- LDraw File Format Specification 1.0.2. https://www.ldraw.org/article/218.html
  (BFC `CERTIFY`/`INVERTNEXT` are specified separately, not in this document.)
- *Unofficial LEGO Advanced Building Techniques Guide* (36 pp).
  https://joncraton.org/media/files/UnofficialLEGOAdvancedBuildingTechniquesGuide.pdf

**Dimensions and measurement**

- Zoë Blade, "Lego brick dimensions" — carries stud ⌀, module, plate/brick height, `8n − 0.2`; wall
  1.6; **no tube diameter**. https://notebook.zoeblade.com/Lego_brick_dimensions.html
- Christoph Bartneck, "LEGO Brick Dimensions and Measurements" (index page + the 3001/3020
  drawings, text-extracted: Ø6.51 / Ø4.8 / Ø2.6, wall 1.2, stud height 1.7, 15.8 / 31.8).
  https://www.bartneck.de/2019/04/21/lego-brick-dimensions-and-measurements/
- Brighton Toy Museum, micrometer survey — studs 4.88–4.89 mm, footprint `8n − 0.1`, clutch from
  wall flexure. Live site 403s; cited via Wayback.
  http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions
- Brick Owl, stud dimensions (1.7 mm stud height). https://www.brickowl.com/help/stud-dimensions
- orionrobots, "Lego Specifications" — 6.31 / 0.657, **shown by the audit to be the tangency formula
  run with a 5 mm stud**, not measurements. https://orionrobots.co.uk/Lego+Specifications

**Clutch mechanism and moulding**

- BrickNerd on LEGO's NED — LEGO designers describing the joint as "an interference fit".
  https://bricknerd.com/home/all-about-ned-the-lego-engineering-department-youve-never-heard-of-11-19-23
- hardwareishard, "LEGO lore" — 0.5° draft on all tooling-direction walls; 1.2 mm wall.
  https://hardwareishard.substack.com/p/lego-lore-6f8
- Protolabs, uniform wall thickness. https://www.protolabs.com/resources/design-tips/improving-part-design-with-uniform-wall-thickness/
- Xometry, sink marks in injection moulding. https://www.xometry.com/resources/injection-molding/managing-sink-in-injection-molding-designs/
- thewave.engineer, "LEGO tolerances" — **original URL 403s**; current path
  `/articles.html/productivity/legos-0002mm-specification-…-r120/`. States interference of
  **0.1–0.2 mm** and 2–3 N insertion force, and calls the "0.002 mm" figure misleading. No primary
  citations; treat as secondary.

**FDM process capability**

- Zaborniak et al., *Appl. Sci.* 14(15):6404 — 12 identical PLA samples, extremes 4.95/5.01 mm.
  https://doi.org/10.3390/app14156404
- Moylan et al., *J. Res. NIST* 119 — 4 mm pins +0.023 mm vs 4 mm holes −0.115 mm in one build.
  https://nvlpubs.nist.gov/nistpubs/jres/119/jres.119.017.pdf
- *Measurement Science Review* 26(1):33–39 — ISO/ASTM 52902 artifact, ±0.05 mm planar vs ±0.15 mm
  cylindrical. https://journals.savba.sk/index.php/msr/article/download/5835/1760
- Popescu et al., *Appl. Sci.* 13(1):41 — 6 mm holes −0.124 mm best, −0.370 mm worst.
  https://doi.org/10.3390/app13010041
- Grgić et al., *Processes* 11(10):2810 — FDM lands IT9–IT14. https://doi.org/10.3390/pr11102810
- nophead, *Polyholes* — faceting undersize and the "twice the hole size in mm" facet rule.
  https://hydraraptor.blogspot.com/2011/02/polyholes.html
- Bambu Lab, XY hole/contour compensation and auto circle contour compensation — 0.02 mm tuning
  step, per-filament and moisture-dependent.
  https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation ·
  https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation
- Bambu X1C and A1 spec sheets — **contain no accuracy/tolerance/repeatability figure** (grepped).
  https://public-cdn.bambulab.com/store/bambulab-X1-carbon-tech-specs.pdf ·
  https://cdn.shopify.com/s/files/1/0635/8247/0318/files/A1_Spec_EN_1.pdf

**Printed-LEGO practice, including the sceptics**

- Brickset, "Can you make compatible bricks with consumer 3D printers?" — the 0.2 mm nozzle produced
  *worse* clutch; bridging strands "would" foul a plate or tile.
  https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers
- Brick Architect / Koen Van Der Hoeven — printed parts "fail to reach the clutch power of LEGO
  bricks"; the **anti-stud side** is the failing side; +28 % mass.
  https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/
- Chris Finke on his own true-scale prints — "acceptable to my six-year-old son, but not satisfying
  to me". https://www.chrisfinke.com/2015/01/27/3d-printed-lego-compatible-bricks/
- LDraw forums thread on printing parts at true size. https://forums.ldraw.org/thread-28663.html
- Prusa blog, printed LEGO-compatible parts — **not a plain-FDM success**: ASA/ABS plus acetone
  vapour smoothing, elephant-foot compensation, thinned walls.
  https://blog.prusa3d.com/how-to-make-3d-printed-lego-and-lego-duplo-parts_31741/
- PrintPal — "Nozzle: 0.4 mm (standard). 0.2 mm if you want true 100 % scale to print cleanly", a
  recommendation not a requirement; **its own default output is 130 % scale**.
  https://blog.printpal.io/design-and-3d-print-your-own-lego-compatible-bricks/

**Generators and prior art**

- MachineBlocks — calibration docs and source (`lib/block.scad`, `config/config-default.scad`);
  the global-clearance-plus-clamp-band architecture of §3.8, and the `svg`/`surfacePattern`/`text`
  pattern surface of §1. https://machineblocks.com/docs/calibration ·
  https://machineblocks.com/docs/modules/machineblock · https://github.com/pks5/machineblocks
- MCAD `lego_compatibility.scad`. https://github.com/openscad/MCAD/blob/master/lego_compatibility.scad
- richfelker/brickify — derives the tube OD from the same tangency identity.
  https://github.com/richfelker/brickify
- anandamous/OpenSCADLEGO. https://github.com/anandamous/OpenSCADLEGO
- cfinke/LEGO.scad — `stud_play = 0.03`. https://github.com/cfinke/LEGO.scad
- dlvoy/base-plate-outliner. https://github.com/dlvoy/base-plate-outliner
- bricks.lapinoo.net — 2D outline → STL with fit sliders and no validation. https://bricks.lapinoo.net/
- Stud.io collision detection. https://studiohelp.bricklink.com/hc/en-us/articles/5412820155927-Collision
- Brick-by-Brick, NeurIPS 2021 — "action validity prediction network". https://arxiv.org/abs/2110.15481
- Luo et al., "Legolization", ACM TOG 34(6), SIGGRAPH Asia 2015 — force-based stability metric.
  Live pages 403; abstract via Wayback.
  http://web.archive.org/web/20191016021839/http://www.cmlab.csie.ntu.edu.tw/~forestking/research/SIGA15-Legolization/
- "Computational Design of LEGO® Sketch Art", ACM 2023. https://dl.acm.org/doi/10.1145/3618306

**Pattern geometry**

- Cromwell, "The Search for Quasi-Periodicity in Islamic 5-fold Ornament", *The Mathematical
  Intelligencer* 31 (2009) 36–56 — the crystallographic restriction, rhombic lattices, and 5-fold
  designs with rectangular repeat units. https://link.springer.com/article/10.1007/s00283-008-9018-6
  (free copy: http://www.fi.uu.nl/nwd/nwd2009/handouts/tom/Islamic%205%20fold.pdf)

**Withdrawn between v1 and v2**

- ~~Bricks McGee, "How are LEGO bricks made"~~ — **404**, and it was carrying the "~0.01 mm
  tolerance" claim. Removed; §3.5 no longer depends on it.
- ~~Pixenib, "Can I 3D print a LEGO piece?"~~ — its "tube diameter ~4.9 mm" is **not a LEGO
  dimension** (the anti-stud is ~6.5 OD / 4.8 ID); the figure appears invented to make a tidy
  0.1 mm clearance story. Removed as unreliable.
- ~~`brickarchitect.com/2018/the-dimensions-of-lego-bricks/`~~ — **no Wayback record has ever
  existed** for this URL; it probably never was a page. Replaced with Brick Architect's live 2023
  3D-printing article above.

## Appendix B — contested bets and divergences

Each entry: the bet, the strongest source against it, and either why we diverge or what changed.

Entries tagged `[CAL-…]` are **empirical** bets that no source can close — only a measurement
can. The id is the bet's entry in the registry
([`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md)), which names the
coupon that settles it; the ceremony is the `calibrate` skill (bikar Tenet 30 — a physical
constant is not earned until it records its provenance).

**B.1 — The tangency value over LDraw's convention.** We author the tube at ⌀6.514.
*Counter-position:* LDraw models 6.4 and does so as a **library-wide convention, not a rounding** —
`stud4.dat` is placed at unit XZ scale in 3,336 parts and never rescaled, and LDraw uses non-integer
scales freely elsewhere, so "clean whole-LDU scaling" is not a constraint it observes. 6.4 is what
every existing generator interoperates against. *Why we diverge:* the difference is 0.11 mm, which
§3.5 shows is smaller than the printer-compensation term and far smaller than the −0.1 mm/side
global clearance §7.5 applies on top; and §3.8 means the realised fit is set by the rib, not the
bore. **The bet is cheap either way and LG-F1's rung 0 (`ribMm = 0`) measures both.** What changed
in v2: the doc no longer claims 6.514 is a fact about LEGO — it is a fact about our stud constant.

**B.2 — `studsEngaged ≥ 2` as the rotation-lock criterion, and anchor-only pieces generally.**
*Counter-position:* the patent's clamp is "between one secondary projection **and the inner face of
an end or side wall**", and §3.3's contact census shows the wall supplies 67 % of contacts on a 2×2
and 50 % on a 2×4. An anchor-only piece discards that. Empirically, two Printables makers report
1×N prints "very loose" while 2×N works — the census showing up in plastic. *Why we proceed:*
geometric rotation constraint is still the right *gate* criterion precisely because friction is
unreliable; and §7.6's wall ribs restore wall contact wherever the inset outline permits. **But the
strength claim is unmeasured** — LG-B2 exists to quantify how much clutch the anchor-only case
loses, and V10 warns when a piece has nothing but anchors.

**B.3 — `engage` default. RESOLVED AGAINST v1.** v1 defaulted to 1.6 mm to maximise relief budget.
The counter-evidence won on three independent lines (bridging, cantilever compliance, wall share —
§3.6), so **the default is now 3.2 mm** and `engage 1.6` warns. Recorded here rather than deleted
because the reasoning that produced 1.6 (FDM has no uniform-wall constraint) is still correct — it
just was not the whole picture.

**B.4 — The grid-fit formula. RESOLVED AGAINST v1.** The v1 measure was refuted by counterexample
(a hexagonal lattice scores 1.0 because the formula never sees the angle between the repeat
vectors). §5.3 now runs residuals on **components in the lattice basis**, maximized over the
registration rotation θ, with the snap threshold moved off §3.1's moulding relief and onto 2σ of
measured FDM repeatability. The remaining judgement call is `max` over the four components rather
than a mean: it makes a pattern that snaps in one axis and misses in the other score the same as one
that misses in both. That is deliberate — butted pieces fail on the worse axis — but it flattens the
12-fold case in a way the P1 matrix may want to distinguish.

**B.5 — The 0.8 mm mesh-gate override.** [CAL-FEA-01 — coupon MC-2, not LG-F1: the minimum
printable wall is a printer property] Set to the tangency tube wall exactly, so any *thinner*
feature still errors. *Counter-position:* Brick Architect reports printed parts whose "walls were
too thick", i.e. the realised wall exceeds the authored one, and a 0.857 mm authored wall may print
as ~1.0 and jam. The risk runs both ways and neither direction is settled on paper. LG-F1 measures
the printed tube wall with calipers.

**B.6 — Three slabs.** Assumes relief never breaches the cavity (V3 enforces a 1.2 mm floor) and
studs never overlap relief (V4 forbids the combination). Both hold by validator, so the stack is
genuinely three slabs — but V4 is a real capability loss (no studded piece may carry relief), and
a four-slab variant that recesses relief *between* studs is the obvious LG2 extension.

**B.7 — `unionPatternFaces` as the body outline, and the §7.2 inset.** The first half of this bet is
**settled and was wrong** — see §11 Q3. A nested void is not cancelled away; it is classified as a
bounded face and tiles the region, so the ring and the extruded mesh agree and the "inside the body"
predicate is sound. Measured, not argued.

The second half stands: §7.2's polyline inset clips a self-intersecting offset at a concave vertex by
dropping the crossing span, which is a heuristic, not a proof. Nothing in the Q3 measurement touches
it — a convex test pattern never exercises the clip. **Still trusted rather than verified**, and the
counterexample to look for is a deeply reflex vertex (a star tip) where the dropped span removes wall
the anchor test then assumes is present.

**B.8 — The rib as the clutch mechanism.** [CAL-RIB-01 — coupon LG-F1, design-specific: off
the machine card by design] New in v2. *Counter-position:* nobody has published
caliper data on a printed LEGO stud, a clutch force measurement, or a durability cycle count, so
"a 0.1 mm rib absorbs the process spread" is an argument from MachineBlocks' shipped defaults and
from W2's detent precedent — not from measurement. A rib that is too stiff jams; one too compliant
creeps away under repeated cycling, and PLA is known in this repo to embrittle with age
([`w2-connector-design.md`](w2-connector-design.md)). **LG-F1 and LG-D1 are the only evidence that
will exist**, and until they run this is the single largest unverified bet in the document.
