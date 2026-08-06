# Lego Lab — pattern → piece → LEGO-compatible printed part (LG) — implementation design doc

Status: **v2 — through the adversarial grounding audit
([`research/lego-lab-grounding-audit.md`](research/lego-lab-grounding-audit.md)). Four claims lost
and the design changed: the clutch is now a discrete rib rather than a nominal surface (§3.8, §7.6),
`engage` defaults to 3.2 mm rather than 1.6 (§3.6), the grid-fit measure runs on repeat-vector
*components* rather than lengths (§5.3), and the tangency tube ⌀ is recorded as a derived datum
rather than a fact about LEGO (§3.2). Remaining contested bets, each with its strongest refuting
source, are in Appendix B.**

Built: **R0, M6, M7, P0, P1 and P2 have shipped** (2026-07-29 → 2026-08-01). P1 shipped its
**sweep strip**, its design-notes page, its studio index, **multi-piece export** (§10, D-006) — a
brick mints stud/anti-stud ports from its own lattice and a two-brick assembly exports as two
printable parts — §5.3's **compatibility matrix, now filled by a real sweep**
([`research/lego-lattice-matrix-sweep.md`](research/lego-lattice-matrix-sweep.md)), and the two
**curated scripts** that make that matrix clickable rather than only readable. P2 then gave the page
custom mode — the code drawer, `code=` share links, "Open in Studio" and the localStorage draft —
by *sharing* the Orb Lab's modules rather than forking them. Only P3 has not shipped, and only
partly: its adjusted-parameter toasts have been in both Labs since P0, which §10's row went on
calling future work for two phases — what remains there is the brick page's print note and the
LDraw export. Building P1 produced the finding that a printed brick on a
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
- **LG-F2 — clutch coupon, stud side.** A 2×4 with a stud-⌀ ladder, tested against a real LEGO
  brick's underside, **and measured with calipers before testing.** *Learns:* whether `studs full`
  is viable at 0.4 mm at all; the realised-vs-authored stud diameter, which no published source
  reports. → the `studDia` entry.
- **LG-R1 — 1×N pin coupon.** A 1×4 with the three ⌀3.2 pins §3.3 predicts. *Learns:* whether the
  pin geometry survives FDM anisotropy, and whether a pin is weaker than a tube in practice — two
  Printables makers report exactly this failure (§3.3). → the `pinDia` entry.

All three ship as **three-plate bodies at `engage 3.2`**, and F2 and R1 were drafted as single
plates until the engine refused: a plate is 3.2 mm tall, so it can engage at most 1.6 mm and keep
any ceiling, and 1.6 mm is exactly what V5b flags on §3.6's grounds. A coupon that warns is a
measuring instrument with a confound — a failed clutch would then have two candidate explanations.
The ladders themselves are **not `param`s** and cannot be: no `brick` statement reads a rib
thickness or a stud ⌀, because those are `brickFit` offsets describing a printer and a spool rather
than a design. They are swept with bikar's `--brick-fit <field>=<value>`, which leaves provenance
`manual` — only a printed-and-measured result may claim `coupon` (§9, D-005). Source:
`bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr`.
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
| **P2** | both | Custom mode: code drawer, `code=` share links, Open in Studio, localStorage draft. ✅ **Complete** (bikar PR #50) — built by *sharing* the Orb Lab's `editor.ts` / `custom-state.ts` / `url-state.ts` rather than forking them; the one change any of them needed was the draft slot, and the clutch fit rides in neither the link nor the `.bkr` (§7.5). |
| **P3** | both | Polish. **Adjusted-parameter toasts ✅ already shipped** — both Labs have toasted `Adjusted N parameters to printable values` since P0 (`lego-main.ts:958`, `main.ts:618`); this row listed them as future work for two phases longer than it was true. What is *not* built is naming which parameter moved and to what, which is a refinement, not this phase. **Per-family print notes** are unbuilt on the brick page only: the Orb Lab has `updateProcessNote()` keyed on family × `PrintTarget.process` (`main.ts:538`), and the Lego Lab reads `printTarget` for the build envelope alone. **LDraw `.ldr` export** is unbuilt. This row long described it as *"a text emit, one line per piece"* on the survey's §6 framing; [`research/lego-ldraw-export.md`](research/lego-ldraw-export.md) refutes that. One line per piece requires naming a stock part, which is dimensionally false for 5 of the 7 shipped brick scripts and fails silently — so the honest shape is an MPD with inline geometry, i.e. **a mesh emit** at ~212 KiB per 2×4, larger than the same mesh's STL. **§14 now specifies all three**; the cost estimate above is the corrected one. ✅ **Complete** (bikar `a10f4f6`, PR #53) — all three built to §14, with the process note gated on a *moved* fit rather than on the margin alone (§14.1), the clamped knob named on the panel and in the toast (§14.2), and `--format ldraw` emitting an inline-block MPD (§14.3). The one thing §14.3 asked for that was **not** done is the check that needs no code: no LDraw viewer had opened the output. **Partly discharged 2026-08-02** (bikar `49aab9f`, PR #62) — the Lab grew the export button §14.3 specified but never got, and a fourth tab that reads the file back through three.js `LDrawLoader` and prints the signed volume of what it built (§14.4). One third-party reader, continuously; not the twelve-tool afternoon, and not an official LDraw implementation. |

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

**P2 — custom mode — 2026-08-01.** bikar `9cca1ae` (PR #50: `lego.html`'s drawer markup and
authoring notes, the custom-mode section of `lego-main.ts`, the draft-slot parameterization in
`custom-state.ts`, `STUDIO_EDITOR_URL`'s move into `editor.ts`,
`packages/lab/tests/lego-custom-mode.test.ts`, the custom-mode block in
`packages/e2e/tests/lego-lab.spec.ts`, and the de-paged family refusal in
`packages/lab/src/evaluate.ts`). 3d-models: this entry and the §10 P2 row.

The Lego Lab now has the Orb Lab's code drawer, `code=` share links, "Open in Studio" and the
localStorage draft — and it has them because §2's no-fork rule held a second time. `editor.ts`,
`custom-state.ts` and `url-state.ts` are used verbatim; `lego.html` mounts the same markup against
the same stylesheet. What that bought is one identity rule, one URL budget and one bake semantics
across two pages, which is the whole argument for the second Vite entry restated at the feature
level.

**The one shared module that had to change, and why it is a real defect rather than a tidy-up.** The
draft slot was a module constant in `custom-state.ts`. That was correct while exactly one Lab had a
drawer and wrong the moment the second one did: both pages are one `localStorage` origin, so a brick
draft would have booted the Orb Lab into `mode = 'custom'` holding a script that cannot be an orb —
a page that opens broken, from a write another page made. `ORB_DRAFT_SLOT` and `BRICK_DRAFT_SLOT`
are now declared beside each other and passed in, so the collision is a thing a reader sees rather
than a thing they have to reproduce. `STUDIO_EDITOR_URL` moved the other way for the mirror-image
reason: two copies of a deployment URL means a redeployed studio that one page follows and the other
does not, and a dead link is invisible from the page that still works.

Two behaviours are deliberately **not** shared, because the brick page makes different promises:

- `applyResult`'s non-brick branch carried the comment *"only reachable if a script in the registry
  stops declaring a `brick`"*. Custom mode makes typing an `orb` an ordinary thing a user does, so
  that comment became false the moment the drawer opened — a **K7** caught by reading the file
  against the change rather than by any gate. The message now names the recourse ("Add a `brick`
  block, or open it in the Orb Lab") instead of only stating the fact.
- **The clutch fit rides in neither the `code=` payload nor the downloaded `.bkr`.** §7.5 already
  separated the two panels; custom mode is where that separation earns its keep. A link that quietly
  carried the author's fit offsets would make the recipient's brick come out wrong on *their*
  machine in a way neither of them could see, because both would be looking at the same design and
  getting different parts. The drawer's authoring notes say so in the place an author is standing
  when it matters.

Beyond the spec: the sweep strip is dropped on a preset↔custom transition and kept across edits
*within* custom mode. Those are the same tolerance a knob drag already has, but the reason they
differ is worth writing down — a strip is a picture of one script's knob range, and
`refreshSweepControls`' "is this param still declared?" check is not enough to notice that the
script under it changed, because two scripts can both declare `pitch`.

Graduation rule honoured, in three places because the claims are of three different kinds.
`custom-state.test.ts` pins the two draft slots as distinct and non-interfering — the bug above,
written as a test against the module that carried it. `lego-custom-mode.test.ts` runs the identity
rule against every committed brick source *and* against a one-character edit of each, and checks
that `lego.html` declares every id `lego-main.ts` resolves with `must()`. That last one exists
because those calls throw at module load: a renamed element is a blank page, not a failing
assertion, and P0's own lesson — *a unit-tested helper is not a rendered one* — applies to a
mounted element as much as to a called function. The scan carries a guard on itself, so a refactor
that renames `must` goes red instead of quietly becoming a test that asserts nothing.

The third kind is what neither of those can reach, and it went to `packages/e2e/tests/lego-lab.spec.ts`:
that a by-hand `ribMm` stays out of the URL the page actually writes (§7.5, checked on the link
rather than on the encoder), that a comment-only edit leaves `data-tris` identical so a typed brick
is scored by the same gates on the same mesh, and that an orb pasted into this page is refused by
name. **Writing that third case found a second K7,** one level down. Its first draft pasted a
script declaring nothing at all and asserted the page's message; it got the shared worker's
instead, because a script with no declaration never reaches `applyResult`. The worker's refusal
read *"the Lab previews a 3D orb, a `wall` layout, or a `brick`"* — written when one page ran it,
false on the page this phase gave a drawer to, which previews neither an orb nor a wall. A shared
worker cannot know which page asked, so it now states only what the engine needs and the family
question stays where the answer is known. Same shape as the `applyResult` comment above: a true
sentence that the second consumer made false, invisible to every gate, found by reading a file
against the change.

**P3 — the process note, the knob that moved, and the LDraw export — 2026-08-01.** bikar `a10f4f6`
(PR #53: `updateProcessNote`/`applyMachineSelection` and the adjustment markers in `lego-main.ts`,
`markAdjustedKnobs` in `packages/knobs`, the four new e2e cases, then
`packages/core/src/render/ldraw-emitter.ts` with 22 unit cases, `--format ldraw` in the CLI, and
`docs/decisions/2026-08-01-ldraw-export-inline-mpd.md`). 3d-models: this entry, the §10 P3 row, the
§14.1 correction in `5b1534c`, and UC18 in the use-case map.

**The deliberate deviation is in §14.1, and it is the interesting one.** The spec gated the
feature-floor note on `process === 'fdm'` and a margin to `featureFloorMm`. Built exactly that way,
the note is on screen on **every brick the Lab can produce**, including the untouched default: the
thinnest feature is the anti-stud tube wall, 0.757 mm on the shipped fit against a 0.70 mm floor —
8%, inside the margin. That is not a coincidence to tune away. The wall is
`outerDia/2 − bore/2`, and both of those are fixed by §3.1's mating dimensions rather than by
anything the reader chose, so *no* setting of the margin makes the note rare while leaving it
useful. A note that never turns off is the decoration §14.1 itself refuses. The condition that does
discriminate is whether the reader has moved a clutch number — `FIT_FIELDS.some((f) =>
fitProvenance(brick.fit, f) !== 'default')` — so that is what gates it, and §14.1 now says so with
the 0.757-inside-0.805 arithmetic written out in its own PASS example. The margin still does work;
it decides whether a *moved* fit is worth reporting, which is a different job from making the note
rare.

Two smaller findings, both from building rather than reading. The e2e case that proves the note
fires first used `tubeDiaMm = −0.1` and stayed silent — because `BrickFit` fields are **diametral
deltas** and the shipped value is already −0.2, so −0.1 *raised* the wall to 0.807 mm. The passing
case dials to −0.3 (0.707 mm), and the pair of tests — silence on defaults, note on a moved fit —
is the graduation artifact for the paragraph above. Separately, nothing re-evaluated the note on a
machine change, since the mesh does not depend on the build volume; switching FDM → powder left the
pin/shear advisory on screen where §11 Q2 is not a question at all. `applyMachineSelection` now
re-asks it.

Beyond the spec: `PlacedPart` gained `bodyHeightMm` and `brickSizeLabel`, because the LDraw origin
is the brick's **top** face and the emitter cannot compute `H − z` from a placement alone.

**What is owed.** §14.3 lists four items that "are answered by opening one file in three viewers",
and the emitter shipped without that afternoon happening — the file has been read by 22 tests and
by no viewer. The PR body says so and this entry repeats it, because a claim about interoperation
that no interoperating program has seen is exactly the K1 hedge this doc is not allowed to strip.
*(Partly discharged 2026-08-02 — §14.4. One third-party reader, three.js `LDrawLoader`, now reads
the export back on every evaluation. That is not the afternoon and not an official LDraw
implementation; the hedge narrows, it does not lift.)*

**The LDraw read-back panel — 2026-08-02.** bikar `49aab9f` (PR #62), §14.4, D-009. 3d-models: this
entry, the §10 P3 row, §14.4, and UC19 in the use-case map.

**The scope was larger than D-009 wrote it.** D-009 says to wire `LDrawLoader` *"behind the LDraw
export button"*. There was no LDraw export button: `git grep -i ldraw -- packages/lab` returned one
cosmetic string. The emitter shipped in core + CLI only, reachable via `bikar render --format
ldraw`, so §14.3's export was complete in the sense the spec meant and absent from the surface a
person actually uses. Building the panel therefore meant building the export path first — one
`ldraw` request type serving both the download and the preview, so the two consumers cannot drift
onto different bytes.

**The deliberate deviation is that the cheap read-back was refused.** Parsing the MPD with a small
hand-written reader and drawing it with the existing Canvas-2D viewer would have cost no dependency
and no 550 kB chunk. It would also have been *our* parser reading *our* file, which is precisely
the self-validation gap D-009 exists to close — the panel would have proven that bikar agrees with
bikar. Independence is the entire value, so three.js went in.

**Beyond the spec:** `ldraw-readback.ts` is deliberately WebGL-free and separate from
`ldraw-preview.ts`, so the measurement runs under vitest in Node while only the picture needs a
browser. The two `LDrawLoader` traps in §14.4 were both found by running the loader against the
real emitted file; neither is visible from the API surface, and the magenta one would have shipped
as a convincing bug report about the emitter.

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
- **Q4 — the bridged cavity ceiling. RESOLVED, and the question's own premise was wrong** (bikar
  [PR #44](https://github.com/NaqshCoffee/bikar/pull/44)). Q4 as written said "span still scales
  with footprint: a 2×2 cavity bridges 12 mm, a 6×6 bridges 44 mm", and asked for a
  footprint-dependent warning. Measured on the seven shipped presets, footprint does not move the
  answer at all. The reason is in this document's own §5.2: `solveAnchors` places an anti-stud at
  **every interior cell corner**, so the stud pitch caps the widest unsupported run and a bigger
  plate simply buys more anchors. Q4 reasoned from the outline, and the outline is not what the
  ceiling spans between.

  | preset | footprint | span (mm) | anchors dropped |
  | --- | --- | --- | --- |
  | Classic-Brick | 2×4 | 4.88 | 0 |
  | Grid-Field-Tile | 5×5 | 4.88 | 0 |
  | Pin-Rail | 1×8 | 4.80 | 0 |
  | Rational-Repeat-Tile | 8×8 | 11.57 | 12 (relief) |
  | Edge-Stud-Tile | 6×6 | 12.54 | 8 (relief) |
  | Star-Brick | 4×4 (auto) | 14.25 | 8 (relief) |
  | Hex-Field-Tile | 6×6 | 25.93 | 10 (relief) |

  A 5×5 and a 1×8 land within a tenth of a millimetre of each other, and the largest plate in the
  set — the 8×8 — is not the widest span; what separates the two halves of the table is a
  **dropped** anchor, from relief art sitting on a lattice crossing. So the
  warning is keyed on the measured run, not on the plate. `supportSpanMm` (bikar
  `packages/core/src/kernel3d/grid-gate.ts`) measures it with a shrinking-grid largest-empty-circle
  search over the anchor set the build actually kept, and V12 reports it with the drop that opened
  it — a pocket drop, a body-test drop, or neither — so the recourse is stated rather than guessed.

  **Default:** the ceiling is 10 mm — `BRIDGE_SPAN_MAX_MM`, bet CAL-BRG-01. It is Bambu Studio's
  shipped `max_bridge_length`: the number a stock slicer stops trusting at, rather than the number
  filament stops spanning at. This is V12's first consumer; before it the bet had none.

  **Validator:** V12 warns, and never refuses, when the measured span exceeds that ceiling. It is a
  warning because the ceiling is transcribed from someone else's slicer preset: the same appendix
  that credits it ([`print-validation-design.md`](print-validation-design.md) B.4) records community
  bridging at 20–80 mm on tuned machines, so a refusal would be this project asserting a limit it
  has never printed against. Coupon MC-3 settles it.
  - PASS: `Classic-Brick` at its defaults — 4.88 mm, every candidate anchored, no message.
  - FAIL: a 4×4 under a 16 mm relief window — 8 of 9 candidates dropped, 14.25 mm, V12 names the
    pocket and offers "move or shrink the art that opened it, or accept the bridge".

  Brick Architect's directional result — the printed **anti-stud side** is what fails — is what
  makes the number worth reporting at all; it is not what predicts which brick is at risk. Internal
  ribbing stays unbuilt: nothing measured here calls for it, and MC-3 is the print that would say.

  The refutation is drawn rather than tabulated in the `span-and-border` design note (§12): a 1×8
  and a 5×5 as underside plans at one scale, with the same disc in both.
- **Q5 — should `auto` footprint round up or refuse? RESOLVED: round up and warn** (same PR). The
  warning is V13, and the whole of what took a second draft is **which sources it may speak about**.

  **Validator:** V13 warns when a pattern axis leaves more than half a stud pitch of dead border per
  side — i.e. when the *smaller* footprint is nearer the art than the one it got — and only when the
  source wrote `footprint auto`.
  - PASS: `Edge-Stud-Tile`, whose declared 6×6 leaves a wide margin on purpose — that margin *is*
    its perimeter stud ring, and its own header says so.
  - FAIL: `Star-Brick`, the one preset that asks the compiler to round; its source comment already
    puts the border at "~3.9 mm of margin per side", which is exactly what V13 reports.

  Run ungated, the first draft fired on five of the seven presets. Every one of those five declares
  its footprint, and in each the border is a design choice a bounding box cannot see. A typed
  `footprint 6 x 6` is a decision; `auto` is an arithmetic result — V13 judges the arithmetic, which
  is the only thing it is entitled to judge. The draft also offered "and the smaller plate already
  fits it as drawn", which contradicts its own first clause: `studsFor` picks the least *n* with
  `footprintMm(n) ≥ mm`, so under `auto` the art is always strictly wider than `footprintMm(n−1)`
  and the branch is unreachable. Deleted, with the proof kept beside the code — a K7 caught by
  reading the message against itself, and no source could have settled it.

  The gate itself is drawn in the `span-and-border` design note (§12), which draws `Star-Brick`'s
  border and — for the six presets that typed a footprint — draws nothing, because
  `borderPlanModel` returns `undefined` for them.

  Refusing was rejected for the reason the original leaning gave: the author who wants the smaller
  plate needs a number, and V13 hands them one ("scale 0.780 lands it there") instead of an error
  that says only *no*.
- **Q6 — a geometry-only gate structurally cannot score clutch. RESOLVED as far as it can be** (same
  PR). Clutch is elastic: it depends on wall and tube *flexure*, material stiffness, moisture, and
  layer adhesion (§3.5, §3.8). `gridGate` measures geometry. **`anchorability: PASS` must therefore
  not be read as "will clutch"** — and the Lab panel was rendering exactly `PASS — it will hold`,
  the paraphrase `grid-gate.ts`'s own module header forbids in so many words. Two artifacts, a rule
  and a restatement of it, and the restatement had drifted.

  The fix is structural rather than editorial: `anchorabilityVerdict()` and `CLUTCH_CAVEAT` now ship
  **from the kernel**, beside the rule, and the Lab renders what it is given. The badge reads
  `PASS — anchorable geometry`; the caveat sits directly under it, because a reader who stops at the
  green tick must have already read it. A test asserts neither verdict can say "will hold", "will
  grip" or "will clutch", so the wording cannot drift back.

  Whether a compliance proxy (rib deflection × count, or an FEA-lite bending estimate) is worth
  adding stays **open** — that part of Q6 is not resolved and is not resolvable here. LG-F1 and
  LG-D1 supply the data that would calibrate one, and the caveat names them, so the limit reads as
  a next measurement rather than a dead end.
- **Q7 — position-dependent degenerate triangles from relief pockets. RESOLVED** (bikar
  [PR #42](https://github.com/NaqshCoffee/bikar/pull/42)). Building `Hex-Field-Tile` (§10, P1)
  turned up a mesh-gate failure — 5–6 zero-area triangles — that depended on *where* a motif sat,
  not on what it was. A hexagonal motif (n=6) tiled into the field failed; the diamond (n=4) the
  preset ships with passed; `Grid-Field-Tile`, `Edge-Stud-Tile` and `Star-Brick` all baselined at
  `degenerate=0`. The narrowing that mattered was the one that *ruled out* the obvious explanation:
  disabling `voids detect` still failed, switching to `mode rectangular` still failed, a tiled
  sweep over n=3,4,5,6,7,8,12 failed **only** at n=6 — and a single-polygon repro failed at n=4 and
  passed at n=6, the exact opposite. "Hexagons are broken" was false, and the position-dependence
  was the tell.

  The cause was **two tolerances for one thing**: the mesh gate rejects a triangle under
  `DEGENERATE_AREA_MM2 = 1e-6` mm², while `absorbSlivers` — the cap repair that exists to remove
  exactly those — tested `area === 0`. Everything in between was invisible to the repair and fatal
  to the gate. The mechanism needs only two holes whose centres share a row: earcut bridges holes
  along horizontal rays, so the bridge runs down that row and ears an exactly-zero sliver *on the
  section boundary*, where `absorbSlivers` has no neighbour to split and returns `null`;
  `triangulateInFrame` then retries at 0.37 rad, where the same sliver measures `1.4e-14` rather
  than `0`, the triangulation is sound, and it is accepted with the sliver in it. Motif alignment
  is what puts hole centres on a shared row — that is the whole of the position-dependence, and the
  shape never mattered.

  The fix exports `DEGENERATE_AREA_MM2` from `mesh-gate.ts` and has `solidify-piece.ts` consume it
  as `SLIVER_AREA2_MM2 = 2 * DEGENERATE_AREA_MM2` (doubled because `signedArea2Of` returns twice
  the area), so the gate and its repair are one number rather than two that happen to agree. Note
  what defeats the weaker version of that argument: the frame retry *changes the measured area*, so
  a repair calibrated to today's exact zeros is broken by the very machinery that fixes soundness.

  The regression test drives `solidifySlabStack` directly with two hexagonal holes at
  `dy ∈ {0, 3e-15, 1e-9}` — `3e-15` mm being the y-noise the brick partition actually produced
  between two pocket rings the geometry says are on one row. It reports 2 flat triangles before the
  change and none after; the n=6 preset goes from `degenerate=6 — FAIL` to `watertight=true euler=2
  degenerate=0 — PASS`.
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
| `span-and-border` | §11 Q4 and Q5: what actually bounds the bridged span, and which sources V13 may judge | **decided** — by measurement, recorded in §11 above rather than as a `D-NNN`, because neither was a choice between designs |

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

`span-and-border` is the third mechanism, and it is the one where the kernel had to change to let
the page stay honest. `brickSection()` is handed a solid; `latticePlan()` re-runs a *pure* function
on a basis nobody built. A span is neither. It is a search over the anchor set the build kept, and
its answer — a diameter — is the one number on this site a reader cannot check by eye: a 25.93 mm
disc on a 6×6 plate looks identical whether the search found the real hole or wandered into a
corner. Drawing it left exactly two options, and one of them was a second solve.

So the kernel now returns the circle's **centre** with its diameter (`supportSpan`, with
`supportSpanMm` kept as the thin wrapper every warn-only consumer wants), and
`packages/lab/src/design/draw-cavity.ts` draws what it is handed. The same move fixed V13's figure:
by the time a `BrickSpec` exists the footprint is two integers, so the difference between a plate an
author chose and one the compiler rounded to has already been erased —
`BrickResultProvenance.art` now carries the inscribed bounding box and the `footprint auto` flag
forwarded from the exact values `validateBrick` was handed, rather than letting a drawing re-derive
a bbox from segments and hope it matches the warning printed beside it.

Two things this note had to say on the figure rather than solve:

- **It cannot draw the anchors that were dropped**, which are the cause of every over-ceiling span
  in the catalogue. `AnchorSolution` keeps their *count* and not their positions, and re-running the
  candidate search to recover them would be a second solve of precisely the step whose *rejections*
  are the subject. The counts go in the caption; the figure shows the consequence.
- **It draws no border plan at all for six of the seven presets**, and the absence is the argument.
  `borderPlanModel` returns `undefined` when the footprint was typed, so the page physically cannot
  make the claim V13's first draft made — that five authors' declared plates were wasteful — and
  had to withdraw.

`packages/lab/tests/design-cavity.test.ts` is the enforcement: the drawn diameter must `toBe` (not
`toBeCloseTo`) `BrickProvenance.supportSpanMm` on every shipped preset, the disc must fit inside the
cavity the same figure draws, and the border model must exist for exactly the `footprint auto` set —
which `lego-presets.test.ts` independently pins to `Star-Brick.bkr` alone.

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

## 14. P3 — the three items, specified

§10's P3 row names three items. Two are refinements of surfaces that already exist (§14.1, §14.2).
The third — the LDraw export — was blocked on a question about the format rather than about our
code: a generated brick is not an LDraw part and has no part number, so a type-1 line has nothing
to reference. [`research/lego-ldraw-export.md`](research/lego-ldraw-export.md) answers it, and
§14.3 is the spec that follows. **It also refutes the row's own cost estimate**, which is corrected
in §10 and explained in §14.3.

### 14.1 The brick page's process note

The Orb Lab has carried a process-dependent advisory since P1: `updateProcessNote()`
(bikar `packages/lab/src/main.ts`) sets one hidden `<p id="process-note">` when
`family === 'weave' && printTarget.process === 'fdm'`, telling the reader that interlocked ribbons
come off powder systems pre-assembled and off FDM needing support surgery. The Lego Lab has no such
element and reads `printTarget` only for `radiusCeilingMm()` and the build-volume readout — so the
one knob on the page that describes the *machine* changes nothing the page says about the *part*.

The brick's analogue is not `family` — every brick has `family: 'brick'`, so keying on it would
produce a note that is either always on or always off. It is **`LabBrick.anchorKind`**, because
that is the field §11 Q2 is a question about, and the field whose answer the FDM/powder split
actually changes. Two conditions, rendered into the same single slot as a list so the page keeps
one element:

- **Anchor anisotropy.** `anchorKind === 'pin' && process === 'fdm'`. A ⌀3.2 pin printed in layers
  loads its weakest axis in shear every time a brick is pulled off, where a moulded one does not.
  Q2 is open, LG-R1 is the coupon that closes it, and the note says exactly that — it does not say
  the pin will fail, because nothing measured here says so.
- **Margin to the feature floor.** `process === 'fdm'`, **the fit set has been moved off its
  shipped defaults**, and `minFeatureMm` is within the margin below. The panel already prints
  `minFeatureMm` / `minFeature` / `featureFloorMm`; what it does not do is say that a part clearing
  the floor by a hair clears it on paper only, since the floor is a nominal-geometry check and the
  printed wall is the one that jams. Names `minFeature` so the reader knows which dimension is
  close.

  The moved-fit clause is not decoration-avoidance bolted on afterwards — it is the same test the
  first bullet applies to `family`, applied here. On the shipped fit the thinnest feature of *every*
  brick is the anti-stud tube wall at **0.757 mm** against a **0.70 mm** floor, 8 % clear, because
  that dimension is fixed by the part this one has to mate with rather than by anything the design
  chooses. Keyed on the margin alone the note would be on screen forever. What moves the margin is
  the fit set, so that is what gates it: the note fires when the reader has dialled a clutch number
  and dialled it toward the floor. On defaults the standing fact belongs to the fit banner, which
  already says every clutch number is an unmeasured default until a coupon says otherwise.
  Implementation: `FIT_FIELDS.some((f) => fitProvenance(brick.fit, f) !== 'default')`, read off the
  fit the mesh was built from — the same source §9's provenance badges read.

  **Default:** the margin is 15 % of `featureFloorMm` — bet [CAL-FEA-01](#appendix-b--contested-bets-and-divergences),
  the same bet the 0.8 mm override rides on, because it is the same unmeasured quantity: the gap
  between the authored wall and the realised one. Appendix B records that Brick Architect reports
  the realised wall running *thicker* than authored, so the hazard is real in the direction that
  matters and its size is exactly what LG-F1's calipers settle. Note what 15 % does *not* buy here:
  at a 0.70 mm floor it admits everything up to 0.805 mm, which the shipped 0.757 mm wall is already
  inside — so the margin is what makes the note *informative once the fit moves*, not what makes it
  rare.

Neither condition fires on powder, which is the point: on SLS/MJF the anisotropy question does not
arise and the resolvable-feature floor is a different number. And a note is not a warning — nothing
here is a validator finding, so nothing here belongs in `LabBrick.warnings`, which is the channel
V5b/V7/V8/V10/V12/V13 already own.

**Validator:** the process note must not restate anything already present in `brick.warnings`. The
two channels are shown a few hundred pixels apart and a reader who sees the same sentence twice
learns to skim both.

- PASS: `Star-Brick` on FDM — 4×4, `supportSpanMm` 14.25 mm, eight anchors dropped for relief
  (§11 Q4's measured table). V12 warns about the bridge (14.25 > `BRIDGE_SPAN_MAX_MM` = 10) and
  the note stays hidden: 4×4 means §5's rule gives `anchorKind: 'tube'`, so the anisotropy
  condition does not hold, and on the shipped fit the second condition does not either — its
  thinnest feature is 0.757 mm, *inside* the 0.805 mm margin, and the moved-fit clause is the only
  reason the note is silent. One statement, one channel.
- FAIL: the same brick with a note that also said "this cavity bridges 14.25 mm unsupported". True,
  already on screen from V12, and duplicated — the reader now has to check whether the two numbers
  agree rather than read either.

Note that the example is deliberately not "a big plate": §11 Q4 measured that footprint does not
move the span at all — `Star-Brick`'s 4×4 spans wider than the 8×8 — and a PASS case that implied
otherwise would re-import the premise Q4 refuted.

### 14.2 Naming the parameter that moved

Both Labs have toasted `Adjusted N parameters to printable values` since P0
(bikar `packages/lab/src/lego-main.ts` and `packages/lab/src/main.ts`). The count is the whole
message: `applyAdjustments()` mutates `values[a.name] = a.to`, or deletes the entry when
`a.dropped`, and the knob silently shows its new position. A reader who was not watching that knob
has been told a number changed and not which one.

The data is already in hand — `KnobAdjustment` carries `name`, `to` and `dropped` — so this is a
copy and marking change, not a plumbing one. Two channels, because they have different lifetimes:

- **The toast** names every adjusted parameter when there are two or fewer
  (`Raised stud clearance to 0.12 mm`), and falls back to the existing count above that. The bound
  is the toast's own 3.6 s dwell, which is checked in beside it; it is a copy limit rather than a
  `**Default:**`, because no measurement settles it and pretending otherwise would put a number in
  Appendix B that no coupon can close.
- **The knob** carries a mark for as long as the adjustment holds, which is the channel that
  survives the toast timing out and the one a reader can act on. A dropped knob — `a.dropped`,
  where the constraint removed the override entirely — reads differently from a moved one and says
  so, since "back to the shipped value" and "clamped to 0.12" are different events.

This is deliberately not a new gate. An adjustment is the constraint solver doing its job; the
brick that comes out is printable, and the reader is being told what it cost, not warned.

### 14.3 The LDraw export

Grounding: [`research/lego-ldraw-export.md`](research/lego-ldraw-export.md), 2026-08-01, seven
LDraw specification documents plus three viewers, read against bikar at `9cca1ae`.

**The row's framing was wrong, and this is the correction.** §10 called the export *"a text emit,
one line per piece"* with no mesh work. That is true of exactly the two options the research
recommends against, and false of the one it recommends. The reason is §3.5 of the research: of the
**7 brick scripts shipped in bikar's `patterns/Lego/`**, **5** carry `relief depth` and/or
`studs none` / `studs edge`, and no stock LDraw part has a pattern relief cut into it. A type-1
line naming `3001.dat` for a `Star-Brick` produces a file that renders as a plain grey 2×4 and
warns nobody — an export that succeeds and yields the wrong thing, which is the defect class
[`c2-assembly`](c2-assembly-design.md) was audited over. Even the two scripts with a stock analogue
(`Classic-Brick`, `Pin-Rail`) differ dimensionally: 4.6 mm studs against 4.8, 6.314 mm tubes
against 6.4, a 31.8 mm 4-stud run against 32.0, and 0.1 mm clutch ribs no LEGO element carries.

So the export is an **MPD** carrying one inline `0 FILE <name>.dat` block per *distinct* brick,
geometry as type-3 triangles, referenced by a type-1 line per placement. The MPD specification's
own worked example defines a part inline with geometry inside an MPD, which is the strongest
grounding available for the shape. Placement arithmetic is unchanged from the rejected option —
that property is real and worth keeping — so the whole difference is which filename the type-1
line names.

**Default:** 1 LDU = 0.4 mm, from the
[LDraw File Format Specification 1.0.2](https://www.ldraw.org/article/218.html) as fetched and
quoted in [`research/lego-ldraw-export.md`](research/lego-ldraw-export.md) §1.3. The spec gives *two*
conversions and calls both approximations; the other, 1/64 in = 0.396875 mm, makes a stud pitch of
7.9375 mm. **K10 — why 0.4 transfers and 1/64 in does not:** 20 LDU × 0.4 reproduces §3.1's
8.0 mm pitch exactly, which is the pitch every dimension in this doc was derived under and the
conversion the survey read that table under. 1/64 in reproduces nothing here, and must not be
offered as an emitter option.

The axis map is `(x, y, z)_mm → (x/0.4, (H − z)/0.4, y/0.4)_LDU`, whose 3×3 has determinant **+1**
— a proper rotation from bikar's right-handed +z-up frame to LDraw's right-handed −y-up one, so
triangle winding survives. The near-miss `(x, y, z) → (x, −z, −y)` has determinant −1 and would
invert every face silently. The `H − z` term puts the origin on the brick's **top** face; **K10 —
that convention transfers because interoperation is the only reason to emit `.ldr` at all.** If
the file only ever held our own bricks any consistent origin would do; the moment a user drops a
library part beside ours, a different origin puts it 9.6 mm out with nothing on screen to say so.

Header lines (`0 Name:`, `0 Author:`, `0 !LDRAW_ORG`) come from specifications scoped to
*submission to an LDraw.org repository*. **K10 — they transfer as conventions, not requirements:**
a file generated for a user's own viewer is submitted nowhere, so nothing in those specs binds it;
what does transfer is a reader's expectation, and matching it costs six lines. The emitter writes
them and the doc does not claim the file is "spec-compliant" on that basis. One line is excluded
on purpose: `0 !LICENSE` asserts a CC BY 4.0 grant over the referenced geometry that nobody in
this project has made — emit this repo's actual licence or none.

`0 BFC CERTIFY CCW` was the second exclusion, on the grounds that it was *derivable* (the mesh
reports `watertight: true` and positive signed volume, and the axis map preserves winding) but had
"never been rendered in a BFC-checking viewer", so it stayed out "until someone looks". Someone
looked, within four hours of that sentence being written: [`decisions-log.md`
D-012](decisions-log.md) records the reversal and §14.4 the reader. It is written in every block
since 2026-08-02, bikar PR #63 — main model included, because S7 makes certification hierarchical
and certifying only the part would have left the file readable by way of the spec's part-file
exception rather than on its own terms. **The hedge that narrows and does not lift:** one
third-party reader has run, not the twelve-tool survey, and none of them an official LDraw
implementation.

**Validator:** an inline block's filename must fall outside all three part-number namespaces the
LDraw part-number spec defines — bare `NNNN`, `uNNNN`, `tNNNN` — all of which are
administrator-assigned, with no reserved namespace for user parts. This is not style: the MPD
extension states in its own words that there are no scoping or namespace rules for MPD files,
which is both what makes an inline block resolvable *and* what makes a badly-named one dangerous.

- PASS: `bikar-Classic-Brick-2x4-3p-a71f.dat` — begins with letters, contains hyphens, cannot be
  read as a part number under any of the three forms, and no future library part can collide with
  it. Carries a `0 //` line saying it is generated and is not an LDraw part.
- FAIL: `3001.dat` for the same block. It resolves — and, having no scoping rules to stop it,
  silently replaces the real 2×4 for *every other reference in the document*, including stock
  parts the user added themselves. The user's own model changes shape and nothing reports it.

**The cost, measured rather than estimated where it says so.** One plain `Classic-Brick` 2×4 is
3,764 triangles and **217,206 bytes (212.1 KiB)** of type-3 text — measured. `Star-Brick`
(1,300 tris), `Hex-Field-Tile` (12,148) and `Grid-Field-Tile` (12,844) are measured for triangle
count and their byte figures **extrapolated** at 57.7 B/line, so ≈ 73 / 685 / 724 KiB are
order-of-magnitude figures, not measurements. A 20-brick field-tile model lands in the 10 MB range.
The useful comparison is not "large for a text file" but that 212 KiB exceeds the **184 KiB binary
STL of the same mesh** — and anyone who wanted the mesh already has `--format stl`. De-duplicating
identical bricks into one block halves the worked two-brick example, and is the one optimisation
that is free.

**What is bounded, and stated as bounded.** Three viewers were checked — LDView, LeoCAD, BrickLink
Studio — and only **LDView** documents a resolution rule that could be quoted. LeoCAD's docs
describe a library zip/folder and an `unofficial` directory and say nothing about a model-directory
search or about an unresolvable reference; Studio's import article lists `.ldr`/`.mpd` and says
nothing about unrecognised parts. Nothing here should be read as *"LDraw viewers do X"*, only as
*"of the three checked, one documents X and two document nothing"*. Not checked: LDCad,
Bricksmith, LPub3D, `library.ldraw.org/model-viewer`, three.js `LDrawLoader`, Blender's importers.
Seven specification documents were read; roughly a dozen further language extensions were not, so
the "no units or global-scale meta command exists" finding is bounded to those seven.

Two consequences for scope, both of which the emitter must carry rather than the reader:

- **Refuse rather than mislead on a non-8 mm pitch.** `STUD_PITCH_MM = 8.0` is a module constant
  today, not a knob — §5.3 and the lattice sweep vary *pattern scale* against a fixed 8 mm pitch,
  which the export represents for free as more triangles. But if pitch ever becomes a knob, LDU is
  a unit and not a grid: a 7.5 mm pitch emits at 18.75 LDU centres, renders exactly where it was
  put, and is silently incompatible with every part in the library. The type-1 matrix does scale,
  legally — and a uniform scale shrinks the studs too, so the result mates with nothing. There is
  no way to say "this model is on a 7.5 mm pitch" in a file whose whole premise is one fixed unit,
  so the emitter refuses. That guard is written now, against a future change, not a live case.
- **The stock-part hybrid is a follow-on, not a precondition.** Emitting a real part number when
  the brick provably matches within a tolerance, and inline geometry otherwise, is the better
  answer in principle. It needs a match table (footprint × height × stud mode → part number)
  maintained against library updates, and a tolerance only a rendered comparison can set — and the
  deltas above sit in the 0.086–0.2 mm band where "close enough for a layout preview" and "wrong
  as a dimensional record" are the same number. That is the number to argue about when it is built.

Ten items could not be grounded and the research file enumerates each with the experiment that
would settle it. Four are load-bearing here: what LeoCAD does with an unresolvable reference and
whether it resolves names against same-file `0 FILE` blocks; what Studio does with an
inline-defined part on import and round-trip; what LDView does after its parts-tracker download
attempt fails for a name that never existed; and whether `0 UNOFFICIAL PART` and
`0 !LDRAW_ORG Unofficial_Part` are interchangeable — none of the seven specs reconciles them, and
the worked example's choice of the latter is an inference, not a sourced claim. **All four are
answered by opening one file in three viewers**, which is why they are listed as experiments and
not as bets: no coupon, no calipers, one afternoon.

#### 14.3.1 The afternoon, costed — and a fifth item the four did not anticipate

Grounding: [`research/ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md), 2026-08-01, twelve
named candidates. **K2 — that is a survey of twelve tools, not of the space of LDraw software;**
the session had no search budget left, so there was no exploratory search and the candidate set is
the one the brief named plus what could be reached by following links.

**How the afternoon is actually run.** Nothing LDraw is installed on this machine and there is no
Homebrew formula or cask for LDView, LeoCAD or Studio, so "opening one file" is a manual download
before it is a command. Of the twelve, **LDView** is the one to reach for: it is the only candidate
whose *macOS-specific* source shows a snapshot path that returns before `NSApplicationMain` starts
a window, and `-VerifyLDrawDir=0` lets it run with no parts library at all — which suits us exactly,
because our MPD references nothing outside itself. §1.2 of the research gives the invocation.
**K10 — LDView's documentation is written from a Windows point of view, and its Linux release ships
an off-screen build the macOS release does not have**, so the macOS off-screen path is claimed on
the strength of `MacOSX/LDView/main.m` and nothing else. It rests on CGL pbuffers, a deprecated
Apple API, and LDView's own help hedges it — *"if your video card allows this to run without
displaying a window"*. Untested here.

**The fifth item, and it is the one that matters.** §14.3's four unknowns all ask what a viewer does
with a *name*. None of them asks what a viewer does with the *triangles*, and for LeoCAD the answer
looks like: nothing. `lcModel::LoadLDraw` dispatches on line type, builds an `lcPiece` from type-1
lines, and drops types 2–5 into `else { ReadingHeader = false; mFileLines.append(OriginalLine); }`;
`mFileLines` is read back only by `SaveLDraw`. Our file is two type-1 lines and 3,764 type-3
triangles. The name resolves perfectly — `SplitMPD` → `CreatePieceInfo` → `FindPiece` consults the
same-file blocks first — so the predicted outcome is **an empty model and no error at all**, which
is the export-succeeds-and-yields-the-wrong-thing class this section was written to avoid, arriving
from a direction the section did not look. **K1 — this is a source reading, not an observation.**
It was checked against `leozide/leocad@master` a second time by hand before being written here, and
what has *not* been ruled out is some other path — a preview renderer, the POV-Ray export,
`lcSynthInfo` — reconstituting those lines. The run that settles it is the same run as ①.

So the ledger moves as follows. ③ largely **dissolves** for a well-formed export: LDView's
`subModelNamed` hits the loaded-models dictionary before any disk or tracker lookup, so the parts
tracker is never reached and the question survives only for a *malformed* file. ④ is **answered
per-implementation and stays open as a standards question**: LDView's `isPartMeta()` accepts both
forms, three.js's `isPartType()` accepts only `!LDRAW_ORG` — they are *not* interchangeable across
readers, and the emitter already writes the form both accept. ① is half-answered and now carries
the fifth item above. ② — BrickLink Studio — is **untouched**, and nothing in this survey predicts
it, because Studio maps LDraw parts onto its own catalogue. The afternoon is still owed; it is now
costed, and it has one more thing to look for than it did. **§14.4 discharges the part of it that
needed no install** — the fifth item, what a reader does with the *triangles*, is answered for
three.js `LDrawLoader` and answered well. It stays open for LeoCAD, which is where the prediction
of an empty model came from and where no run has yet been made.

### 14.4 The read-back panel — what a second reader can settle without the afternoon

Decided in [`decisions-log.md` D-009](decisions-log.md); shipped bikar `49aab9f` (PR #62).

§14.3.1 costs an afternoon of *installing* viewers. One reader needs no install: three.js
`LDrawLoader` is an npm dependency, so it can sit inside the Lego Lab and read the export back on
every evaluation. That is strictly less than the afternoon — **one third-party implementation, not
the twelve-tool survey and not an official LDraw one** — and it is the reason D-011 still authorizes
the single upload to `library.ldraw.org/model-viewer`. What it does buy is that the reading happens
continuously and without anyone remembering to do it.

The panel is the fourth tab on the Lego Lab stage. It renders the parsed result, but the render is
not the evidence: a file wound entirely inside-out draws as a convincing brick in any reader that
culls nothing. So the panel prints two numbers beside the picture, and those are the claim.

> *Qualifier corrected 2026-08-02.* This paragraph originally ended "…which is what every reader
> does with an uncertified file" — an exhaustiveness claim (**K2**) over readers, resting on a
> reading of S7's *"may not cull"* that the one reader we have does not satisfy: three builds a
> `FrontSide` mesh from the authored winding whether the file certifies or not. What NOCERTIFY
> constrains is what a consumer may *discard*; what it draws instead is unspecified. See
> [`research/ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md) §9.4.

**Validator:** the read-back passes when every type-1 line resolves against a `0 FILE` block in the
same file, the signed volume of the built geometry is positive in LDraw's right-handed −Y-up frame,
*and* every directed edge of that geometry is walked exactly once in each direction.

- PASS: `Classic-Brick.bkr` → 1 placement, 1 inline block, 1 reference resolved, 1 mesh built,
  signed volume **+62,282.24 LDU³**, and 11,292 directed edges with **0 unpaired, 0 doubled** —
  outward-facing triangles that agree with each other, and no parts library was consulted to get
  there (`setPartsLibraryPath('')` is what makes it a read-back: with nothing to fall back on, an
  unsatisfied reference fails instead of being quietly filled in from disk).
- FAIL: wrong orientation — the same bytes with the emitted certification rewritten to
  `0 BFC CERTIFY CW` → same placement and mesh counts, **same triangle count**, signed volume
  **−62,282.24**, and still 0 unpaired and 0 doubled. A culling consumer keeps the inside of the
  brick. Coherent and inside-out — which is why the two readings are separate rows and not one.
- FAIL: wrong coherence — the same bytes with one type-3 line's second and third vertices swapped —
  **one triangle of 3,764** reversed. Still `CERTIFY CCW`, still 1 reference resolved, still 3,764
  triangles, and the signed volume still **positive, at +58,095.24**. 3 unpaired edges, 3 doubled.

The first FAIL is why the orientation readout is a *sign* and not a triangle count. Certifying CW
halves the count exactly as certifying CCW does, so a count separates certified from uncertified and
says nothing about which side survived.

> *Validator strengthened 2026-08-02, and the second FAIL case is new.* As written above this line
> until today, the validator was the resolve check **and the sign alone** — and the second FAIL case
> passes it. `0 BFC CERTIFY CCW` is a claim about *every* triangle in the block; the signed volume is
> one sum over all of them, and a sum cannot see a defect that cancels inside it. Reversing one large
> triangle moved the total by 6.7% and nowhere near zero, and the panel has no per-model baseline to
> compare a magnitude against, so no threshold on this number was ever going to catch it. The panel
> said `pass`, in the word "outward faces" — plural.
>
> This is a **K7**, and an unusually plain one: [§7.3](#73-the-ring-cache-is-mandatory) has gated cap
> triangulation on exactly this directed-edge test since the corner clip, and its own FAIL line
> records the reason — the T-junction chord *"which the area check scores as exact"*. The technique
> was in the document, 1,243 lines up, and the section that needed it reached for an aggregate
> instead. §7.3 allows for a declared ring of boundary edges because a cap is open; the brick is
> closed, so here the expected count is 0.

The graduation artifact is `packages/lab/tests/ldraw-readback.test.ts` in bikar, eleven cases, run
in Node without WebGL.

The eighth case was added on 2026-08-02, when shipping D-012 turned up a claim of ours that had
never been measured. Stripping the certification entirely gives the *same* signed volume the
certified file gives — bit for bit — because the "extra" triangles three appears to build for an
uncertified file are reserved buffer slots left at `(0,0,0)`, not reversed copies. The panel's
triangle row was counting those slots; it now counts area, and reports the slots separately.

**Two `LDrawLoader` traps, found by running it rather than by reading it.**
`addDefaultMaterials()` throws unless `setConditionalLineMaterial()` ran first; and it registers
colour codes 16 and 24 only, so our type-1 lines' code 7 falls through to `missingColorMaterial`
and the brick draws magenta while the file is entirely correct — an export that reads as broken
when it is not. The panel supplies its own one-line `0 !COLOUR` table through `preloadMaterials`
via a `data:` URI, which costs no network and, load-bearingly, **leaves the model bytes untouched**:
the panel has to read what the download writes, not a repaired copy of it.

three.js is a real dependency of `@naqshcoffee/bikar-lab` now, held behind a dynamic import so it
lands in its own ~550 kB chunk while the Lego Lab entry stays at ~27 kB — a user who never opens
the tab downloads no WebGL engine. The preview rights LDraw's −Y-up with a rotation of π about X
rather than a Y scale of −1, because a mirror has determinant −1 and would flip the winding the
panel exists to show.

### 14.5 Per-placement colour — the parts read as distinct, not one grey blob

§14.3's emitter wrote every placement at the module default (7, `Light_Grey`), so a multi-part
assembly like `Brick-Stack` opened as a single grey mass in a viewer — indistinguishable parts
defeating the reason the export writes one sub-file per brick. `place` now carries an optional
colour: **`place <Piece> [color <name|code>]`** (D-026, bikar PR
[#79](https://github.com/NaqshCoffee/bikar/pull/79)). A grounded name — one of the ten in
[`research/lego-ldraw-export.md`](research/lego-ldraw-export.md) §7.4, each the lower-cased
LDConfig colour name — or a bare integer LDraw code (0–511). It rides the type-1 line's colour
field (§14.3's `1 <colour> …`), which was already the field the panel's magenta trap (§14.4) proved
the viewer honours; `--format stl`/`svg` have no colour channel and ignore it.

Three properties keep it honest:

- **A name is grounded, a code is not — and both are on purpose.** A name resolves against the
  fetched palette and an unknown one is refused with the valid list; a code is the escape hatch for
  any other of LDraw's codes and, exactly like §14.3's `4`/`7`, asserts nothing about appearance.
- **The all-grey emission is byte-identical to before.** An uncoloured `place` still emits code 7,
  so this section adds a capability without moving any existing output — the §14.4 read-back cases
  are unchanged.
- **Bounded, and stated so (K2).** Only the ten names the clause exposes are grounded, not LDraw's
  full ~380-entry palette; the mapping is fetched once (S15, header `UPDATE 2026-05-29`) and any
  other colour is reached by its integer.

This does not change the part-number discipline of §14.3 (the inline `0 FILE` blocks and their
non-part-number names are untouched) — colour is a property of the *placement*, not the part, so a
`bikar-…-.dat` block stays one block referenced by differently-coloured type-1 lines.

### 14.6 Per-brick stud colour — the pins painted apart from the body

§14.5 gives the whole part one colour: the type-1 line carries a single code and every triangle in
the block inherits it (colour 16). A real two-tone brick — blue body, yellow studs — cannot be said
that way, because the type-1 line has exactly **one** inherit slot. `place` now takes a second,
optional clause: **`place <Piece> [color <name|code>] [studs <name|code>]`** (D-027, bikar PR
[#80](https://github.com/NaqshCoffee/bikar/pull/80)). `studs` resolves through the same grounded
palette and range check as `color` (§14.5), and is independent of it — either clause may appear
alone, and `color` when present comes first.

The mechanism is forced by the one inherit slot, and it is the load-bearing design fact here:

- **The stud code is baked into the geometry, not the reference.** The body triangles stay colour 16
  and inherit the placement colour as before; the **stud** triangles are written with the explicit
  stud code, so they render that colour whatever the type-1 line says. This is the *mixed-colour
  inline part* — one watertight block, two colour regions — verified before implementation by a spike
  that placed it twice and read back a blue body and a red body sharing one yellow-studded part.
- **A stud is identified by the top-face plane, exactly and not heuristically.** A triangle is a stud
  iff a vertex stands above the brick's body height `H`. `stackBrickSlabs` builds studs as the one
  slab above `H` and puts nothing else there (§6.2's slab table), so the body's highest face sits at
  exactly `H` and never trips it. **The transfer condition (K10), stated so it cannot be assumed:**
  this holds only for meshes whose sole geometry above the top face is studs — every brick this
  emitter serves. The emitter **refuses** `studs` on a part with an empty stud set (a `studs none`
  brick, a non-brick) rather than colouring nothing silently.
- **De-duplication splits when — and only when — the stud colours differ.** The block key is the
  emitted geometry text, and the stud code now lives *in* that text, so two bricks with different
  stud colours mint two blocks while two with the same stud colour still share one. `Brick-Stack`
  (Base blue/yellow, Cap red/green) therefore emits two `0 FILE` blocks where §14.5's one-colour
  version emitted one — the split is the mechanism, not a regression.
- **The panel had to learn the palette (robustness, not ease).** §14.4's read-back preloaded only
  code 7, so a yellow stud would have rendered as the magenta the trap exists to catch — the same gap
  §14.5's coloured bodies already had. The read-back panel now preloads the full ten-colour grounded
  set with LDConfig's own RGB (§7, `UPDATE 2026-05-29`), and a read-back test asserts a
  yellow-studded brick reads back with **zero** unresolved colours and the same winding/edge
  coherence as the plain brick.

**Validator:** a stud clause is honoured when the block carries the body triangles in colour 16 and
the stud triangles in the named code, and the read-back renders both with no magenta.
PASS: `place Base color blue studs yellow` on a studded 2×4 → a block with 2244 triangles in 16
and 1520 in 14, referenced by a `1 1 …` line, read back at 0 unresolved colours.
FAIL: `place Plate color blue studs yellow` on a `studs none` plate → the emitter throws (*no
geometry stands above its top face*), because there are no pins to paint and colouring the empty set
would be a claim about nothing.

---

## Appendix A — sources

Full survey with derivations: [`research/lego-brick-system-survey.md`](research/lego-brick-system-survey.md).
Adversarial audit, preserved verbatim: [`research/lego-lab-grounding-audit.md`](research/lego-lab-grounding-audit.md).
LDraw format research behind §14.3, with its own fetch record and ten ungrounded items:
[`research/lego-ldraw-export.md`](research/lego-ldraw-export.md).

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
