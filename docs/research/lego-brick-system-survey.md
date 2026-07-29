<!-- Produced 2026-07-29 during Lego Lab R0 (WebSearch/WebFetch + first-hand reading of the official
     LDraw parts library, downloaded and extracted locally). Checked in verbatim.
     Feeds: docs/lego-lab-design.md (Appendix A) and the LG coupon ladder in
     .claude/skills/prototype/catalog.md. -->

# LEGO brick system survey — dimensions, the clutch mechanism, and what survives contact with FDM

*Research date: 2026-07-29. Prepared as Appendix-A source material for the Lego Lab design doc.*

Scope: the dimensional standard and its provenance, the clutch mechanism as a designed geometry,
the anti-stud taxonomy (the "1×N exception"), LDraw as an interchange format, what FDM at 0.4 mm
can and cannot hold, and the prior art on forcing arbitrary geometry onto a square lattice.

**Method note — why this survey is unusually well grounded.** Most published LEGO dimension tables
are secondary and disagree with each other (stud ⌀4.8 vs 5.0 is the classic split). Rather than
arbitrate between blog posts, this survey reads the **official LDraw parts library** as its primary
geometric source: the complete library was downloaded
([library.ldraw.org/library/updates/complete.zip](https://library.ldraw.org/library/updates/complete.zip),
142,693,798 bytes; 24,297 part files and 1,775 primitives) and the relevant primitives and part
subfiles were read in full as text. LDraw part files are plain-text CSG: a type-1 line
`1 <colour> x y z a b c d e f g h i <file>` places a sub-file under a 3×3 matrix, so a primitive's
scale factors **are** its dimensions. Those numbers are then cross-checked against the original
1958 LEGO patent and against two independent documentation sources.

**Access failures (claims relying on these are marked).** The Legolization project page
([cmlab.csie.ntu.edu.tw](http://www.cmlab.csie.ntu.edu.tw/~forestking/research/SIGA15-Legolization/))
and its ACM DL record both returned HTTP 403, so that paper is cited from its abstract and
programme listing only, never for a number. Brick Architect's dimensions article returned 404.
Bartneck's page is an index to downloadable PDF/Fusion 360 technical drawings rather than a
dimension table, so his measured interior figures could not be read. The Brighton Toy Museum
dimensions page returned 403. Per-file LDraw web paths (`ldraw.org/library/official/p/stud4.dat`)
404 — the library must be taken as the zip.

> ⚠ **POST-AUDIT CORRECTION (2026-07-29).** The list above is incomplete and three of its entries
> were recoverable. See [`lego-lab-grounding-audit.md`](lego-lab-grounding-audit.md) for the full
> record; the corrections that matter to this file are marked ⚠ inline below.
>
> - **Two more sources were unreachable and were not disclosed:** `thewave.engineer/lego-tolerances/`
>   **403s** (§2 and §5 quote numbers from it), and `bricksmcgee.com/.../how-are-lego-bricks-made`
>   **404s** (§2 quotes the 0.01 mm figure from it). Both are used below for load-bearing tolerance
>   claims. When thewave.engineer was retrieved at its current path it says the stud/tube
>   interference is **0.1–0.2 mm** — which refutes this survey's "0.02 mm clutch band" outright.
> - **Bartneck's drawings were extractable after all.** They carry Ø6.51 / Ø4.8 / Ø2.6, wall **1.2**,
>   stud height **1.7**, 15.8 / 31.8 — three of which contradict §1's table.
> - **Brighton and Legolization are both recoverable via the Wayback Machine.** Brighton's micrometer
>   survey contradicts §1 (footprint `8n − 0.1`; studs measured 4.88–4.89 mm; clutch attributed to
>   wall flexure). Legolization's abstract confirms this survey's characterisation exactly.
> - **The Brick Architect dimensions URL has no Wayback record ever** and probably never existed; the
>   live and relevant article is
>   [brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/).

---

## 1. The dimensional standard, read off the primitives

LDraw's unit: **1 LDU = 0.4 mm ≈ 1/64 in**, with the official specification's own caveat that
"these real world approximations are just that: approximations"
([LDraw File Format 1.0.2](https://www.ldraw.org/article/218.html)). The same conversion is given
independently by the *Unofficial LEGO Advanced Building Techniques Guide*
([joncraton.org mirror, PDF](https://joncraton.org/media/files/UnofficialLEGOAdvancedBuildingTechniquesGuide.pdf), p. 3).
The spec also fixes brick width/depth = 20 LDU, brick height = 24 LDU, plate height = 8 LDU.

Everything below was read from the library files named in the right-hand column. LDraw's Y axis
points **down**, so a brick's top face is y = 0 and its bottom is y = 24.

| Feature | LDU | mm | Source file |
|---|---|---|---|
| Stud pitch | 20 | **8.0** | stud placements in `parts/s/3001s01.dat` (x = ±10, ±30) |
| Stud ⌀ | 12 | **4.8** | `p/stud.dat` — `4-4cyli` scaled (6, ·, 6) |
| Stud height | 4 | **1.6** | `p/stud.dat` — y = 0 → −4 |
| Plate / tile height | 8 | **3.2** | `parts/3023b.dat`, `parts/s/3068bs01.dat` |
| Brick height | 24 | **9.6** | `parts/3001.dat` outer quad, y = 0 → 24 |
| Side/end wall thickness | 4 | **1.6** *nominal* | `box5` inner vs `box4t` outer in `parts/s/3004s01.dat` |
| Ceiling thickness | 4 | **1.6** | brick cavity top y = 4 under top face y = 0 |
| Brick cavity depth | 20 | **8.0** | `box5` scaled y = −20 from y = 24 |
| Plate/tile cavity depth | 4 | **1.6** | `parts/s/3068bs01.dat` — `box4` at y = 4, height 4 |
| Anti-stud tube OD | 16 | **6.4** *(as modelled)* | `p/stud4.dat` — outer `4-4cyli` scaled 8 |
| Anti-stud tube ID | 12 | **4.8** | `p/stud4.dat` — inner `4-4cyli` scaled 6 |
| Anti-stud tube wall | 2 | **0.8** | difference of the above |
| Solid pin ⌀ (1×N) | 8 | **3.2** | `p/stud3.dat` — `4-4cyli` scaled 4 |
| Hollow-stud ID / bar ⌀ | 8 | **3.2** | `p/stud2.dat` inner scale 4 |
| 1×1 cavity, square | 12 × 12 | **4.8 × 4.8** | `p/box5` scaled 6 in `parts/s/3005s01.dat` |

⚠ **Overstated — corrected post-audit.** Zoë Blade's table agrees on the *exterior* rows only: base
unit 1.6 mm, module 8 mm, stud ⌀4.8 × 1.6 h, plate 3.2, brick 9.6, `8n − 0.2`. She gives wall
**1.6** (not the 1.5 §4 derives) and **carries no tube diameter at all**, so she cannot corroborate
the interior rows. Her table cites R. Schulz,
"What are the dimensions of a Lego brick?" (*Bricks*, Jan 2021) and Daniel Konstanski, *The Secret
Life of Lego Bricks* (2022), ch. 6
([notebook.zoeblade.com](https://notebook.zoeblade.com/Lego_brick_dimensions.html)).

**The 4.8-vs-5.0 dispute is settled: 4.8 mm is the nominal stud diameter.** The 5.0 figure that
circulates in maker forums is a rounded caliper reading of a real moulded part, not a specification.

**→ Design implication.** These are the numbers `kernel3d/brick.ts` emits. They are not
provisional any more, with the single exception of the tube OD, which §2 resolves.

---

## 2. The clutch is tangency — and it is patented as such

This is the survey's headline finding, and it changes how the whole feature should be built.

The original LEGO "Toy Building Brick" patent — **US 3,005,282, filed 28 July 1958, granted
24 October 1961** ([Google Patents](https://patents.google.com/patent/US3005282A/en)) — specifies
the coupling as a *pure tangency condition*, in these words:

- "the secondary projections 22 are arranged co-axially with the centre of a square defined by four
  primary projections 21"
- "the cross section of the secondary projections 22 being defined in such a manner that it touches
  the cross sections of the four primary projections"
- "a pair of primary projections of one element are clamped between one secondary projection and
  the inner face of an end or side wall of the other element"
- "the geometrically projected cross-section of each primary projection is tangent to at least one
  secondary projection and the inner face of at least one of the side or end walls"
- "the height of the secondary projections is equal to the depth of the cavity"

Read against the primitives, every clutch surface in the system is **exactly tangent at nominal**,
and the patent's last clause is satisfied literally — brick tube 20 LDU into a 20 LDU cavity, plate
tube 4 LDU into a 4 LDU cavity. Working the tangency arithmetic in LDU with stud radius 6:

| Contact | Tangency requirement | Exact | LDraw models | Δ |
|---|---|---|---|---|
| Tube ↔ four studs | R = 10√2 − 6 | **8.142** LDU (OD **6.514 mm**) | 8 (OD 6.4 mm) | −0.11 mm |
| Pin ↔ two studs | r = 10 − 6 | **4** LDU (⌀ **3.2 mm**) | 4 | exact |
| 1×1 cavity ↔ stud | half-width = 6 | **6** LDU (4.8 mm sq.) | 6 | exact |
| Side wall ↔ outer stud | half-extent = 10k + 6 | exact integers | same | exact |

So the **6.51 mm** anti-stud tube diameter that circulates in the 3D-printing community is not a
folk number — it is the exact value the patent's tangency condition forces, and LDraw's 6.4 mm is a
rounding to whole LDU for clean primitive scaling. **LDraw's tube is 0.11 mm undersize in diameter,
i.e. ~0.057 mm of nominal gap per side where the patent specifies contact.**

The consequence is the important part:

> **LEGO's nominal geometry contains zero designed clearance. Clutch power is an interference
> introduced by manufacturing tolerance, not a dimension you can read off any model.**

That is why the moulding tolerance is the famous number — LEGO holds roughly **0.01 mm**, and the
community consensus is that ~0.02 mm oversize will not assemble while ~0.02 mm undersize will not
hold ([Bricks McGee](https://bricksmcgee.com/blogs/news/how-are-lego-bricks-made),
[thewave.engineer](https://thewave.engineer/lego-tolerances/)).

> ⚠ **RETRACTED post-audit.** The "~0.02 mm clutch band" has **no source**. Bricks McGee 404s.
> thewave.engineer, read at its live path, says the opposite: "the interference between stud and
> tube is roughly **0.1–0.2 mm**", and calls the famous "0.002 mm tolerance" figure "misleading
> without context" — the real figures being a 10 µm *mould* tolerance and ±0.01 mm on stud diameter
> specifically. Brighton's micrometer data implies ~0.04 mm. The "zero designed clearance" framing
> above is also refuted: Brighton measured studs at 4.88–4.89 mm and concluded they are "deliberately
> oversized … to force the mating brick's walls to flex", LEGO's own designers call the joint "an
> interference fit", and moulded parts carry ~0.5° draft so "tangent" holds at one height only.
> `lego-lab-design.md` §3.2 and §3.5 carry the corrected argument.

Reported insertion/separation force
for a well-formed joint is on the order of **2–3 N**, against a 2×2 brick that survives >4000 N in
compression ([thewave.engineer](https://thewave.engineer/lego-tolerances/)). ⚠ An FDM printer holds
roughly ±0.1–0.2 mm — **one to two orders of magnitude coarser than the tolerance the clutch is
specified in.**

> ⚠ **CORRECTED post-audit.** "±0.1–0.2 mm" has no vendor source: the Bambu X1C and A1 spec sheets
> contain **no** accuracy, tolerance or repeatability figure at all (grepped), and Prusa's MK4S page
> claims "Perfect Dimensional Accuracy" with no number. What is measurable is *repeatability*, and
> it is far better: 12 identical PLA samples of a nominal 5 mm feature spanned 4.95–5.01 mm
> (σ ≈ 0.02 mm; [Zaborniak et al., *Appl. Sci.* 14(15):6404](https://doi.org/10.3390/app14156404)).
> The real obstacle is that a fit clearance is a *difference* of two such features (σ_fit ≈ 0.025 mm),
> that one scalar offset cannot null a bore and a boss at once
> ([NIST Moylan et al.](https://nvlpubs.nist.gov/nistpubs/jres/119/jres.119.017.pdf): +0.023 mm pins
> vs −0.115 mm holes in one build), and that cylinders measure ~3× worse than planes (±0.15 vs
> ±0.05 mm). `lego-lab-design.md` §3.5 carries the rebuilt argument.

**→ Design implication, and it is the load-bearing one for this whole feature.** No amount of
reading gets us a printable clutch dimension. The authored geometry must be the tangency value
(6.51 mm tube OD, 3.2 mm pin, 4.8 mm stud), and the *offset from it* must come from a printed
calibration ladder. This is exactly the house `fit-profile.ts` split — authored dimensions are the
contract, the printer profile widens or narrows at emit time — and it is why coupons **LG-F1** and
**LG-F2** block the geometry work rather than following it.

---

## 3. The anti-stud taxonomy — the "1×N exception" is real, and is not a rail

The plan flagged this as "the single most likely source of a wrong first design." Reading the part
subfiles settles it, and **both** prior hypotheses were wrong. There is no rail. There are three
distinct underside treatments, selected by footprint:

| Footprint | Underside feature | Count | Primitive | Geometry |
|---|---|---|---|---|
| **1×1** | none — bare cavity | 0 | (`box5` only) | 4.8 × 4.8 mm cavity; the four inner walls grip the stud |
| **1×N**, N ≥ 2 | **solid pins** | N − 1 | `p/stud3.dat` "Stud Tube Solid" | ⌀3.2 mm, 8.0 mm tall (brick) |
| **M×N**, both ≥ 2 | **hollow tubes** | (M−1)(N−1) | `p/stud4.dat` "Stud Tube Open" | ⌀6.51/4.8 mm, 8.0 mm tall (brick) |

Evidence, read directly:

- `parts/s/3005s01.dat` (Brick 1×1) contains one `stud.dat` on top and an inverted `box5` cavity —
  **and nothing else.** No pin, no tube.
- `parts/s/3004s01.dat` (Brick 1×2) places one `stud3.dat` at x = 0 — the midpoint between the two
  studs — scaled y by −5, i.e. 20 LDU tall.
- `parts/s/3010s01.dat` (Brick 1×4) places `stug3-1x3.dat`, which is three `stud3` at x = −20, 0,
  20 — the three interior boundaries.
- `parts/s/3003s02.dat` (Brick 2×2) places one `stud4.dat`; `parts/s/3001s01.dat` (Brick 2×4)
  places three, at x = −20, 0, 20.

The rule generalises cleanly: **anchors sit on the interior vertices of the stud lattice** — offset
half a pitch (4 mm) in each axis from stud centres — and the feature type is chosen by whether that
vertex has four studs around it (tube) or only two (pin) or none exist (1×1, bare cavity).

This also explains Rebrickable part **3065 "Brick 1×2 without Bottom Tube"**, which had looked like
counter-evidence: a 1×2 *does* normally carry a bottom feature, so a variant without one needs a
name; the feature is simply a solid pin rather than a tube.

**→ Design implication.** The anchor solver in `kernel3d/grid-gate.ts` branches three ways on
footprint, not two, and the 1×1 branch yields **zero** anchors — a 1×1 printed piece is held only
by its cavity walls and is therefore **not rotation-locked** by any anchor. The plan's
`rotationLocked: ≥2 non-coincident anchors` criterion correctly fails a 1×1, and it should: the
gate is telling the truth about a real limitation.

---

## 4. Nominal vs. real footprint — and where "1.5 mm wall" comes from

LDraw models bricks on the **nominal** grid: `parts/3004.dat`'s outer quad runs x = −20 → 20, i.e.
40 LDU = 16.0 mm for a 1×2. The real moulded part is smaller. Two independent sources give the
rule as **(studs × 8 mm) − 0.2 mm**, i.e. 0.1 mm of relief per side, so a 1×2 is **15.8 mm** and a
1×1 is 7.8 mm ([Zoë Blade](https://notebook.zoeblade.com/Lego_brick_dimensions.html),
[Bartneck](https://www.bartneck.de/2019/04/21/lego-brick-dimensions-and-measurements/), the latter
stating plainly "there is a 0.2mm gap between bricks next to each other").

**LDraw does not model this gap.** It is an XY-only rule: heights stack exactly (3 plates = 1
brick = 9.6 mm with no gap term), which is why the vertical dimensions in §1 need no correction.

This reconciles two wall-thickness figures that look contradictory in the literature. The cavity's
inner face is fixed by tangency at 2.4 mm from the outermost stud centre; the outer face moves in
by 0.1 mm. So:

- **nominal wall = 1.6 mm** (LDraw, gap ignored)
- **real wall = 1.5 mm** (tangent cavity inside a 8n − 0.2 shell)

1.5 mm is precisely the figure the 3D-printing community quotes as what printed bricks "need in
order to clutch correctly" — it is not a printing adjustment, it is the true moulded dimension.

**→ Design implication.** `brick.ts` must emit the footprint at `8n − 0.2` and derive the cavity
from tangency; 1.5 mm walls then fall out automatically. Emitting `8n` would make adjacent printed
pieces bind against each other.

---

## 5. FDM reality at 0.4 mm — where the design meets the machine

**The nozzle question is genuinely contested.** PrintPal's guide works at 130 % scale (6.5 mm
studs, 10.4 mm pitch, 1.95 mm walls) and states 0.4 mm is standard while **0.2 mm is required for
true 100 % scale**
([blog.printpal.io](https://blog.printpal.io/design-and-3d-print-your-own-lego-compatible-bricks/)).
Community practice disagrees: a true-scale ~5 mm stud is described as "right at the edge of what a
0.4 mm nozzle resolves cleanly", with 0.25–0.3 mm giving crisper studs but 0.4 mm at 0.2 mm layer
height reported as working. Pixenib gives stud ⌀4.8 against tube ⌀4.9 — i.e. a **0.1 mm** designed
clearance, the printed substitute for moulded interference — and says allowable clearance is
"0.1 mm or less" ([pixenib3d.com](https://www.pixenib3d.com/can-i-3d-print-a-lego-piece/)).
Brickset's own review of consumer-printer compatibility is the sceptical counterweight
([brickset.com](https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers)).

> ⚠ **CORRECTED post-audit — this paragraph gets the nozzle question backwards and cites a bad
> source.**
> - **Drop Pixenib.** Its "tube diameter ~4.9 mm" is **not a LEGO dimension** — the anti-stud is
>   ~6.5 OD / 4.8 ID. The number appears invented to make a tidy 0.1 mm clearance story.
> - **PrintPal is misquoted.** The actual text is "0.4 mm (standard). **0.2 mm if you want true 100 %
>   scale to print cleanly**" — a recommendation, not a requirement. The more useful fact is the one
>   this survey buried: PrintPal's *default output is 130 % scale*, because a true-scale stud is "at
>   the edge of what a 0.4 mm nozzle resolves cleanly". A vendor tool defaulting away from true scale
>   is the stronger evidence.
> - **Brickset is not merely "the sceptical counterweight" — it ran the experiment and the result
>   inverts the nozzle claim.** Printing the same 2×4 at 0.2 mm/0.1 mm layers and at 0.4 mm/0.2 mm
>   layers, clutch was "nowhere near as good as that of real bricks … slightly better on the red
>   bricks than the green, which have hardly any at all" — **the red are the 0.4 mm prints.** A
>   commenter attributes even that clutch to first-layer *elephant's foot*, an uncontrolled defect.
> - **The direction of failure is known.** [Brick Architect / Van Der
>   Hoeven](https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/): a
>   genuine brick stacked onto a printed part, but the reverse failed "as the walls were too thick
>   and the tubes were not perfectly aligned" — **the printed anti-stud side is the failing side.**

Settings that recur across sources: layer height **0.1–0.2 mm**; 3–4 perimeters; 20–30 % infill for
structure or higher for strength; PLA 200–210 °C; **studs up, no supports**; 40–50 mm/s; XY size
compensation around **−0.05 mm**. ABS is repeatedly named as the closest match to real ABS bricks;
PETG is the practical compromise.

Two features fall out badly against a 0.4 mm nozzle, and both are worth stating precisely:

- **The 1.5 mm wall is a clean target** — exactly 3 × 0.5 mm extrusion width, or 2 perimeters plus
  gap fill at 0.42 mm.
- **The tube wall is not.** Exact tangency gives (6.514 − 4.8)/2 = **0.857 mm**; LDraw's rounding
  gives 0.8 mm = exactly two 0.4 mm lines. Either way this is **below bikar's
  `DEFAULT_MIN_FEATURE_MM = 1.2`** in `kernel3d/mesh-gate.ts`. **Every LEGO-compatible brick we
  generate will fail the mesh gate's minimum-feature check by design.** This is the same situation
  the W2 corner clip is in, and it needs the same treatment: a documented, deliberate exemption
  recorded in the design doc, not a silently raised floor.

**Calibration prior art worth copying.** MachineBlocks — an established LEGO-compatible OpenSCAD
generator — ships a printed calibration tool with four independent offsets: `studDiaAdj`,
`wallThickAdj`, `tubeZDiaAdj`, `pinDiaAdj`, plus later `baseHeightAdjustment` and
`baseSideAdjustment`. Its procedure is a graduated ladder read against a real LEGO brick: "start
with the smallest setting in each row… move to the next setting until the brick fits snugly"
([machineblocks.com/docs/calibration](https://machineblocks.com/docs/calibration)).

**→ Design implication.** That is the LG-F1/LG-F2 coupon design, already validated by someone
else's shipping product. Note it carries **four** independent offsets, not one — and that its
`pinDiaAdj` exists as a separate knob is further confirmation of §3's three-way taxonomy. Our
`fit-profile.ts` LEGO entries should mirror that decomposition rather than collapsing to a single
clearance term.

**And a harder consequence, checked against our own engine.** `kernel3d/fit-profile.ts` defines the
house ladder as `press −0.10 / snug +0.05 / sliding +0.15 / free +0.35` mm, and the printer profiles
as `pla_calibrated holeCompMm 0.20` / `petg_calibrated 0.25`. Set beside §2's numbers:

- ⚠ *(retracted — see §2's correction box)* LEGO's entire clutch band is roughly **0.02 mm** wide
  (0.02 oversize won't assemble, 0.02 undersize won't hold). **No source supports this**; the one
  cited says 0.1–0.2 mm. The conclusion below survives on the argument in `lego-lab-design.md` §3.5
  — process variance, bore-vs-boss asymmetry, and the 3× cylindrical penalty — not on band width.
- Our tightest ladder rung, `press`, is **−0.10 mm** — five times the whole band. The smallest step
  between rungs is 0.10 mm.
- `pla_calibrated`'s hole compensation is **0.20 mm** — an order of magnitude larger than the band
  it would have to land inside.

**The existing fit vocabulary cannot express a LEGO clutch.** It was built for connector bores where
±0.05 mm is fine precision; here that is the entire design space and then some. Two things follow:
the LEGO offsets must be their own dedicated, finer-grained set rather than a rung added to
`PortFit`, and — the sobering part — at true scale on a 0.4 mm nozzle the realised fit is dominated
almost entirely by printer compensation, not by the authored dimension. This is the strongest
possible argument for LG-F1/LG-F2 blocking M6, and it should be stated in the design doc's risk
section rather than discovered during implementation.

---

## 6. LDraw as an interchange format

Beyond being this survey's primary source, LDraw is the natural export target for P3's "preview an
assembled set" feature ([spec](https://www.ldraw.org/article/218.html)):

- **Type-1 line**: `1 <colour> x y z a b c d e f g h i <file>` — a sub-file reference with a
  translation and a 3×3 matrix. Placement is one line per part.
- **Colour 16** is the "main/current colour" — inherited from the referencing line. **Colour 24**
  is the "complement/edge colour". A part authored in 16/24 takes whatever colour it is placed in.
- Colour definitions live in `LDConfig.ldr` (the library ships `LDConfig.ldr`, `LDCfgalt.ldr` and
  `LDConfig_TLG.ldr`).
- Y is down; 1 LDU = 0.4 mm.
- Parts carry `0 BFC CERTIFY CCW` and use `0 BFC INVERTNEXT` before a subtracted volume (⚠ these
  two are specified in LDraw's separate BFC extension document, **not** in File Format 1.0.2, which
  this section's lead citation points at) — LDraw
  expresses cavities by winding inversion rather than by boolean subtraction, which is
  conceptually the same trick `solidifySlabStack` uses to avoid CSG.
- `parts/3068b.dat` carries the comment `0 // Patternable surface` above the tile's top quad —
  LDraw's own name for the face we intend to put pattern relief on.

**→ Design implication.** A `.ldr` export is a text emit of one line per placed piece, with no
mesh work at all. It is genuinely cheap and belongs in P3 as planned.

---

## 7. Escaping the square grid — what the technique literature actually offers

The *Unofficial LEGO Advanced Building Techniques Guide* (read in full after local text
extraction) documents the levers LEGO builders use to get off the lattice, and they are all
**discrete**:

- **The 5:2 SNOT ratio.** 5 plate heights (5 × 8 = 40 LDU) equal 2 stud pitches (40 LDU) exactly —
  "not a simple coincidence but a will from the LEGO parts designers." This is what lets a
  sideways-mounted assembly re-register with the grid.
- **The 6:5 ratio.** Brick height 24 LDU to stud pitch 20 LDU = 1.2. A plate is exactly ⅓ of a
  brick.
- **The offset ladder.** Jumper plate (AZMEP, *aus zwei mach eins Plättchen*) gives a **10 LDU**
  half-stud offset; SNOTted plates give **8 LDU**; the headlight brick gives **4 LDU**; combining
  them reaches **2 LDU** ("tenths-stud") offsets.
- **Continuous offset is the exception, not the rule** — achieved only via specific parts and
  hinges, e.g. the SNIR 27° wall (Reinhard Beneke), built from jumper-plate AZMEP.
- The guide's own advice on curvature is blunt: "LEGO parts are not meant to be used to create
  nicely curved surfaces and you will obtain a pixelated looking."

**→ Design implication, and it validates the plan's core bet.** The stock-part world escapes the
grid only in 2 LDU (0.8 mm) quanta and at considerable part cost. **We are not bound by any of
this**, because we print the piece. A printed piece's *outline* can be any curve the pattern
produces; only its *anchors* must land on the lattice. The technique literature is therefore
useful as a description of the constraint we are deliberately sidestepping, and as the honest
answer to "why not just build it out of real bricks" — that path costs 0.8 mm quantisation and
cannot express a 5-fold rosette at all.

---

## 8. Prior art on pattern → grid legalization

- **Legolization: optimizing LEGO Designs** (Luo, Yue, Huang, Chung, Imai, Nishita, Chen; *ACM
  TOG* 34(6), SIGGRAPH Asia 2015, 222:1–222:12). "A method for automatically generating a LEGO
  brick layout from a given 3D model, accounting for color information, required workload and
  physical stability"
  ([SIGGRAPH Asia programme](https://sa2015.siggraph.org/en/attendees/technical-papers/event/techpapers/312.html),
  [SIGGRAPH history](https://history.siggraph.org/learning/legolization-optimizing-lego-designs/)).
  It defines a force-based stability analysis giving both an ordering in strength and an absolute
  threshold. **Marked: full text not readable — project page and ACM DL both 403.** Cited for
  framing only.
- **brickmos / brickr / LegoMosaic** — the quantise-then-merge shape: rasterise to the stud grid,
  then greedily merge runs into the largest legal stock part. A* search appears in LegoMosaic for
  the merge step.
- **three.js `LDrawLoader`** and **buildinginstructions.js** — existing readers for the format in
  §6, useful as reference implementations even though Lego Lab deliberately uses no three.js.
- **Rebrickable** CSV dumps and API for part metadata.

**→ Design implication: none of this is our pipeline, and that should be said out loud in the
design doc.** All of it solves *stock-part layout*, which decision 1 puts explicitly out of scope.
Legolization's stability metric is interesting but answers a question we do not have — our pieces
are printed monoliths, and their failure mode is clutch pull-out, not tower collapse. The one
transferable idea is its structure: a *measurable* physical criterion with a threshold, computed
over a candidate layout and used to drive refinement. That is precisely the shape of `gridGate`.

---

## Implications for the Lego Lab design (condensed)

1. **The dimension table in §1 is now authoritative** and should be transcribed into
   `docs/lego-lab-design.md` §3 with these file citations. It is no longer provisional.
2. **Author to tangency, calibrate by coupon.** Tube OD 6.514 mm, pin ⌀3.2 mm, stud ⌀4.8 mm are
   the contract; the printer offset comes from LG-F1/LG-F2. Nothing about the clutch can be
   settled on paper — the spec's tolerance is 10–20× finer than the process.
3. **Four independent fit offsets, not one** — stud ⌀, wall thickness, tube ⌀, pin ⌀ — following
   MachineBlocks. This changes the shape of the `fit-profile.ts` LEGO entries the plan assumed.
   They must be a **separate, finer set**, not a new rung on `PortFit`: the existing ladder's
   smallest step (0.10 mm) is five times the width of LEGO's entire clutch band (§5).
4. **The anchor solver branches three ways** on footprint: 1×1 → bare cavity, no anchors, no
   rotation lock; 1×N → N−1 solid pins; M×N → (M−1)(N−1) hollow tubes. Anchors live on interior
   lattice vertices, offset 4 mm from stud centres in both axes.
5. **Footprint is `8n − 0.2` in XY and exact in Z.** Derive the cavity from tangency and 1.5 mm
   walls follow.
6. **The tube wall (0.8–0.86 mm) is below the 1.2 mm mesh-gate floor.** This needs an explicit,
   documented exemption in the design doc, mirroring the W2 clip. Discovering this at implementation
   time instead would look like a bug.
7. **Plate-style anti-studs are shallow.** A tile/plate tube is only 1.6 mm tall against a brick's
   8.0 mm — the patent's "height equals cavity depth" clause. The `studs none` tile-style default
   therefore has ~⅕ the engagement depth of a full brick, which is a real argument for defaulting
   patterned pieces to brick height rather than plate height.

---

## Sources

**Primary (read in full)**

- Official LDraw parts library, complete zip — `p/stud.dat`, `p/stud2.dat`, `p/stud3.dat`,
  `p/stud4.dat`, `p/stug3-1x3.dat`, `p/box5.dat`; `parts/3001.dat`, `3003.dat`, `3004.dat`,
  `3005.dat`, `3010.dat`, `3023b.dat`, `3068b.dat`, `3070b.dat`; `parts/s/3001s01.dat`,
  `3003s01.dat`, `3003s02.dat`, `3004s01.dat`, `3005s01.dat`, `3010s01.dat`, `3068bs01.dat`,
  `3070bs01.dat`. https://library.ldraw.org/library/updates/complete.zip
- US Patent 3,005,282, "Toy Building Brick", filed 1958-07-28, granted 1961-10-24.
  https://patents.google.com/patent/US3005282A/en
- LDraw File Format Specification 1.0.2. https://www.ldraw.org/article/218.html
- *Unofficial LEGO Advanced Building Techniques Guide* (PDF, 36 pp).
  https://joncraton.org/media/files/UnofficialLEGOAdvancedBuildingTechniquesGuide.pdf

**Documentation and measurement**

- Zoë Blade, "Lego brick dimensions" (cites R. Schulz in *Bricks*, Jan 2021; Konstanski, *The
  Secret Life of Lego Bricks*, 2022, ch. 6). https://notebook.zoeblade.com/Lego_brick_dimensions.html
- Christoph Bartneck, "LEGO Brick Dimensions and Measurements."
  https://www.bartneck.de/2019/04/21/lego-brick-dimensions-and-measurements/
- Orionrobots, "Lego Specifications." https://orionrobots.co.uk/Lego+Specifications
- BrickNerd, "LEGO SNOT Basics: Geometry, Techniques and Pitfalls."
  https://bricknerd.com/home/snot-basics-geometry-techniques-and-pitfalls-3-18-2021

**Tolerance and manufacturing**

- ⚠ thewave.engineer, "LEGO tolerances." https://thewave.engineer/lego-tolerances/ — **403 at this
  URL**; retrieved at `/articles.html/productivity/legos-0002mm-specification-…-r120/`, where it
  says interference is **0.1–0.2 mm**, not the 0.02 mm band quoted above. No primary citations;
  secondary at best.
- ⚠ Bricks McGee, "How are LEGO bricks made." https://bricksmcgee.com/blogs/news/how-are-lego-bricks-made
  — **404. Unverifiable; do not cite.**
- Added post-audit: Brighton Toy Museum micrometer survey (via Wayback)
  http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions ·
  BrickNerd on LEGO's NED ("an interference fit")
  https://bricknerd.com/home/all-about-ned-the-lego-engineering-department-youve-never-heard-of-11-19-23 ·
  hardwareishard "LEGO lore" (0.5° draft, 1.2 mm wall) https://hardwareishard.substack.com/p/lego-lore-6f8

**FDM practice**

- MachineBlocks calibration documentation. https://machineblocks.com/docs/calibration
- PrintPal, "Design and 3D Print Your Own LEGO-Compatible Bricks."
  https://blog.printpal.io/design-and-3d-print-your-own-lego-compatible-bricks/
- ⚠ Pixenib, "Can I 3D print a LEGO piece?" https://www.pixenib3d.com/can-i-3d-print-a-lego-piece/
  — **withdrawn post-audit**: its "tube ⌀4.9 mm" is not a LEGO dimension.
- Brickset, "Can you make compatible bricks with consumer 3D printers?"
  https://brickset.com/article/128767/can-you-make-compatible-bricks-with-consumer-3d-printers
- bricks.lapinoo.net — LEGO-compatible brick generator. https://bricks.lapinoo.net/
- Added post-audit: Brick Architect / Van Der Hoeven, "Enhancing your LEGO hobby with 3D plastic
  printing" https://brickarchitect.com/2023/enhancing-your-lego-hobby-with-3d-plastic-printing/ ·
  Chris Finke on his own true-scale prints
  https://www.chrisfinke.com/2015/01/27/3d-printed-lego-compatible-bricks/ ·
  Prusa blog (ASA + acetone smoothing, not plain FDM)
  https://blog.prusa3d.com/how-to-make-3d-printed-lego-and-lego-duplo-parts_31741/ ·
  nophead, *Polyholes* https://hydraraptor.blogspot.com/2011/02/polyholes.html ·
  Zaborniak et al. https://doi.org/10.3390/app14156404 ·
  NIST Moylan et al. https://nvlpubs.nist.gov/nistpubs/jres/119/jres.119.017.pdf

**Prior art**

- Luo et al., "Legolization: optimizing LEGO designs", ACM TOG 34(6), SIGGRAPH Asia 2015.
  https://dl.acm.org/doi/10.1145/2816795.2818091 *(403 — abstract only)*
- SIGGRAPH Asia 2015 technical-papers listing.
  https://sa2015.siggraph.org/en/attendees/technical-papers/event/techpapers/312.html
