# Lego Pattern Set — one pattern → c×r pinned pieces (`mural`) — design doc

Status: **v1 — drafted 2026-08-02, through the adversarial grounding audit (C4) the same day
([research/lego-pattern-set-grounding-audit.md](research/lego-pattern-set-grounding-audit.md):
two internal-consistency defects and one misattributed citation found and fixed in place; all four
Appendix-B bets survived counter-evidence search). Every clutch or registration claim below
remains provisional until the LG-P coupons print.** The kernel prerequisite (§7, bikar
Milestone A) is built and tested; the `mural` language surface (§4–5) is specified here and built
in Milestone B.

Scope: a new `mural` declaration in bikar that takes one holistic 2D pattern (the primary use case
is Islamic geometry) and decomposes it along the **nominal 8.0 mm LEGO stud grid** into a c×r array
of rectangular printed pieces. Each piece carries its clipped pattern fragment as top-face relief
and a LEGO-baseplate-compatible underside from the existing anchor solver, so pieces placed
adjacently on a store-bought baseplate reconstitute the pattern in top view — interrupted only by
the 0.2 mm designed seam.

Builds on: [`lego-lab-design.md`](lego-lab-design.md) (the `brick` declaration, anchor solver, both
gates — a mural piece **is** a brick); [`research/lego-baseplate-seam-survey.md`](research/lego-baseplate-seam-survey.md)
(the Appendix-A survey behind every dimensional claim here);
[`tile-wall-design.md`](tile-wall-design.md) (what does *not* transfer — §3);
[`decisions-log.md`](decisions-log.md) (D-013 will record the cut rule and the L78 ruling — C5; D-008 through D-012 are already
assigned, a numbering collision the C4 audit caught).

**Decisions locked by Omar, 2026-08-01, before this doc was written.** (1) Rectangular grid tiles
on the stock 8 mm pitch — the plates one buys at Target, not a custom pinboard. (2) Mount is
LEGO-baseplate clutch. (3) Full house process: design doc + bikar implementation. (4) **Seamless
first** — the kernel rebuild that lets relief run edge-to-edge (§7) is a prerequisite, not a
follow-up, so art is interrupted by nothing but the physical 0.2 mm gap.

---

## 1. Goals and non-goals

1. **A `mural` declaration** that compiles one pattern into c×r watertight printable pieces, each a
   `brick` (§4), with the pattern cut at nominal grid lines (§5) and per-piece relief running to
   the piece's physical edge (§7).
2. **Reconstitution on a real baseplate.** The pieces, studded down on one store-bought plate,
   read as the original pattern from the top. The seam is designed, not accidental: exactly 0.2 mm
   of art per cut line is sacrificed to the inter-piece gap (§3).
3. **Per-piece printability and clutch** via the machinery `lego-lab-design.md` already ships —
   anchor solvability as a hard gate per piece, grid fit as a score, the mesh and print gates
   unchanged.
4. **An honest layout report**: which pieces exist, which are blank, what sliver area was dropped,
   and an area ledger that closes (§6).

**The apparent conflict with lego-lab, defused.** `lego-lab-design.md` §1 lists "stock-part mosaic
generation and BrickLink/Rebrickable BOMs" as an LG non-goal. That non-goal excludes composing
murals out of *purchased LEGO parts* (1×1 plate mosaics, LEGO Art-style stud paintings). This
document is the other branch: **printed** pieces, each carrying continuous engraved relief that no
stock part can carry, mounted on a purchased baseplate. The one stock part in the system is the
baseplate itself. Nothing here emits a parts list.

**Non-goals for this family**: irregular (pattern-outline) piece shapes — every piece is a
rectangle on the stud grid; spans across more than one baseplate (the LEGO Art World Map's
Technic-pin panel joining, and its reported flex problems, are exactly the territory we are
staying out of — survey §3); colour; scaling the pattern to fit (real-scale rule: the pattern is
recentred, never scaled, and a pattern too big for the declared piece array is an error naming the
smallest array that fits); curved or clipped baseplate outlines.

**Prior art, and the gap this fills.** Of the systems surveyed in
[`research/lego-baseplate-seam-survey.md`](research/lego-baseplate-seam-survey.md) §3 —
LEGO Art 31203, Mosaic Maker, dlvoy/base-plate-outliner, MachineBlocks, Finke's printed bricks,
and the Printables/Thingiverse results the survey's searches returned — **none was found that
splits one continuous relief pattern across multiple LEGO-compatible printed pieces and validates
seam registration**. dlvoy splits blank plates and its README says nothing about seams;
mosaic services tile 1×1 studs where the grid *is* the image. The claim is scoped to that surveyed
set, not to the world; but within it, LG-P1 has no published predecessor.

Two near-misses found by the C4 audit
([research/lego-pattern-set-grounding-audit.md](research/lego-pattern-set-grounding-audit.md))
sharpen rather than defeat the gap claim. Brickapic
([bricksly.net/tools/brickapic](https://bricksly.net/tools/brickapic), unfetched — 403, snippet
only) splits one mosaic image across multiple 32×32/48×48 baseplates and re-renders "a grid
overlay showing you exactly where the seams will sit" — seam-aware panelization, but of stock 1×1
parts, with no printed pieces, no relief, and nothing validated. Custom-print vendors
(EclipseBricks, BrickBuildersPro, PriBri — via
[thebrickblogger.com](https://thebrickblogger.com/2025/04/add-mosaics-and-murals-to-your-lego-city/),
fetched) sell continuous mural images spanning multiple stock tiles — pattern continuity across
seams, but by 2D printing on moulded parts. Both do half of LG-P1's job; neither does the half
this doc exists for: engraved relief on printed bodies whose seam registration is checked, not
hoped.

## 2. Engine ground truth

Verified against bikar at **`834dfc2`** (branch `feat/edge-to-edge-relief`; the two commits above
`main` are Milestone A — §7 — and the CAL-REG-01/CAL-CLB-01 registration). Not yet merged to
`main` at the time of writing; §7 records what those commits contain.

- **A mural piece is a `brick`.** `BrickSpec`, `solveAnchors`, `partitionBrick`, `buildBrick`
  (`bikar:packages/core/src/kernel3d/brick.ts`) are reused per piece, unmodified. Tubes for ≥2×2
  footprints, pins for 1×N, the rib clutch, the fit profile — all inherited, none respecified here.
- **The physical footprint rule is `8n − 0.2` mm.** `footprintMm`
  (`bikar:packages/core/src/kernel3d/lego.ts:112`) already emits `studs × 8.0 − PART_RELIEF_MM`,
  with `PART_RELIEF_MM = 0.2` (`lego.ts:67`). Two adjacent pieces registered on the same plate
  therefore leave a 0.2 mm gap — the same gap real LEGO leaves (§3).
- **The lattice-snap threshold is not a seam tolerance.** `SNAP_THRESHOLD_MM = 0.05`
  (`bikar:packages/core/src/kernel3d/grid-gate.ts:110`) decides when a pattern repeat-vector
  residual counts as "on the lattice" for the grid-fit score. §3 states why it must not be read as
  a visual-alignment budget.
- **Multi-piece export exists.** D-006 shipped `--format parts` and per-part STL naming; a mural
  exports as c×r parts through the same path, plus LDraw MPD via the 2026-08-01 inline-block
  export. No new exporter is needed.
- **Edge-to-edge relief is in the kernel** as of `54615ff` (§7): a relief pocket that crosses the
  cavity wall no longer refuses; it is partitioned by a scoped planar arrangement, and pockets
  reaching past the body outline are clipped with a reported area note — the exact behaviour the
  cut rule (§5) relies on.
- **`BRICK_MIN_FEATURE_MM = 0.7`** (`bikar:packages/core/src/kernel3d/brick.ts:91`) floors every
  named brick dimension, including relief depth. A worked example in this doc must therefore use
  `relief depth 0.8`, not the 0.6 an earlier draft of the plan sketched — 0.6 is refused by the
  machinery this doc ships, and shipping the refused number would be this doc's own K7.

## 3. Seam arithmetic, and what transfers

### 3.1 The numbers

A `mural` of `c × r` pieces of `f × g` studs spans `8·c·f × 8·r·g` mm nominal. Each piece's body is
`8f−0.2 × 8g−0.2` mm centred in its cell, so every interior boundary is a **0.2 mm gap** (0.1 mm
per side), and the art cut at the nominal line loses exactly 0.2 mm of continuity per seam — no
more, because the kernel clips relief at the physical outline, not at an inset (§5, §7).

**Default:** inter-piece seam = `PART_RELIEF_MM` = 0.2 mm, i.e. 0.1 mm relief per side. This is
LEGO's own convention, measured independently four ways: Cailliau's caliper pages
([cailliau.org](https://www.cailliau.org/Alphabetical/L/Lego/Dimensions/General%20Considerations/%20General%20Considerations-en.html),
"0.1 mm play on each side", a 2×4 measuring 31.8 × 15.8 mm), Brick Owl's "8x − 0.2 mm" brick
length ([brickowl.com](https://www.brickowl.com/help/stud-dimensions)), the latericius guide's
7.8 × 7.8 mm unit footprint, and Bartneck's dimensioned CAD drawings
([bartneck.de](https://www.bartneck.de/2019/04/21/lego-brick-dimensions-and-measurements/),
"there is a 0.2mm gap between bricks next to each other" — the fourth leg, added by the C4 audit).
A printed piece inherits a proven inter-part gap, not an invented one — though printed-brick
practice sometimes *widens* the clearance to ~0.2 mm per side for FDM (unverified snippet, audit
claim 2), which is LG-F1/LG-P1 territory, not a number this doc adopts.

The seam **will be visible where it crosses lit relief** — a 0.2 mm slot between raised edges
self-shadows into exactly the high-contrast dark line the acuity literature measures. At a 45 cm
viewing distance 0.2 mm subtends ≈1.5 arcmin — at the 20/20 resolution limit as a feature, and
far above dark-line *detection* thresholds (survey §4; the sub-arcsecond Hecht & Mintz figure is
a corroborated secondary — *J Gen Physiol* 1939;22:593–612, primary unfetched — and even the
conservatively-sourced 1 arcmin makes a high-contrast groove detectable). In flat matte
blank-field regions the sourced thresholds do not directly apply (the fetched vernier review
requires Michelson contrast ≥ 0.22 for optimal performance), so there the seam may read fainter —
which costs the design nothing, since those are the regions with no art to interrupt. The design
stance
follows: do not chase invisibility; align cuts with the pattern's own construction lines so the
grid reads as intentional. That stance is our inference, marked as such in the survey (§4.2), not
a sourced fact.

### 3.2 The three transfer statements (K10)

1. **`PART_RELIEF_MM` transfers as a physical-gap prediction and as nothing else.** It transfers
   because it is the same constant serving the same purpose it serves in moulded LEGO — an
   inter-part clearance on a stud-registered grid, corroborated by three independent measurements
   (§3.1). It does **not** transfer as a pattern-registration tolerance: whether two relief lines
   *align* across the gap is governed by FDM XY error (±0.1–0.3 mm per the survey's fetched
   JLC figure — up to 1.5× the whole seam), stud/socket play, and baseplate pitch accuracy — none
   of which the 0.2 constant measures. Reusing a moulding relief as a registration tolerance is
   this repo's named K10 defect (`grounding-defect-taxonomy.md`, lego-lab instance), and it is the
   bet CAL-REG-01 exists to measure instead of assume. [CAL-REG-01]
2. **The tile-wall gap formula does not port.** `tile-wall-design.md`'s inter-tile gap reasoning
   assumes operator-positioned tiles whose placement error the gap must absorb. Mural pieces are
   **stud-registered**: the baseplate lattice sets position, and the gap's job is only to prevent
   interference. The transfer condition — "placement is operator-controlled" — fails, so the rule
   stays home.
3. **`SNAP_THRESHOLD_MM` is a lattice-membership test, not an alignment budget.** 0.05 mm decides
   whether a repeat vector counts as commensurate for the grid-fit *score*. It transfers to the
   mural's per-piece grid-fit scoring because that is the same computation on the same lattice. It
   does not transfer to "misalignment under 0.05 mm is fine": vernier acuity detects ideal-edge
   offsets of 4–11 µm at viewing distance (survey §4), and real seams are bounded by print error,
   not by this constant. Seam visibility is empirical → LG-P1.

### 3.3 What the baseplate itself contributes

LEGO-brand plates hold 8.0 mm pitch to better than enthusiast-caliper resolution across a 32-stud
span (Cailliau derived the pitch *from* long-span measurements — survey §1.3, §2.2). For clone
plates, **no source surveyed publishes pitch-consistency data across a multi-stud span** — an
absence finding, not a pass. A c×r array bridges seams, so accumulated pitch error lands directly
in seam width and registration. Compatibility claims in this family are therefore scoped:
**"LEGO-brand verified (paper only, pending LG-P1); clone plates unmeasured — CAL-CLB-01."**
Never "any store-bought baseplate". [CAL-CLB-01]

Stud engagement numbers carry the survey's hedges with them: stud diameter 4.8 nominal vs
4.88–4.9 measured, height 1.6 (LDraw) vs 1.7–1.8 (measured) — disagreements recorded in survey
§1.3, resolved only by coupon. All clutch claims stay **provisional**; the bets registry currently
holds no measured entry.

## 4. Language surface — the `mural` declaration

Specified here; built in Milestone B. One new reserved word (`mural`), gated before implementation
by the corpus sweep (`bikar:scripts/corpus-sweep.ts`; 345 `.bkr` files across four repos at the
2026-08-02 sweep, all parsed, none using the word) so an existing script cannot be broken by the
reservation; fallback name `panelwork`. `mosaic` is
rejected because lego-lab reserved it *as an error* pointing at the LG2 non-goal, and `panel`
collides with Lab vocabulary.

```
mural StarMural
  inscribe Star
  pieces 4 x 4 of 4 x 4      # c x r pieces, each f x g studs
  height 3 plates
  relief depth 0.8
  # optional: blanks emit|skip     (default emit)
  # optional: slivers drop|keep|error   (default drop)
```

- `pieces c x r of f x g` — required; `x`/`of` are bare identifiers per the `footprint` precedent.
  The worked default `4 x 4 of 4 x 4` spans 16×16 studs = 128 mm — one quadrant of a 32×32
  baseplate (survey §1.1: 640 LDU = 256 mm full plate), each piece 31.8 × 31.8 mm. A full 32×32
  plate is `4 x 4 of 8 x 8` (16 pieces of 63.8 mm) or `8 x 8 of 4 x 4` (64 pieces, the §6 cap).
  The C4 audit caught the first draft claiming this default spans a full plate — false by §3.1's
  own formula (8·4·4 = 128, not 256): the taxonomy's K7 class, fixed here.
- `height` and `relief depth` — per-piece, passed through to every `BrickSpec` unchanged. All
  brick validators (V1–V13) run per piece. `relief depth` is required and must clear
  `BRICK_MIN_FEATURE_MM` (§2).
- `studs none` is the default (studs over relief is refused by the kernel's stud-overlap guard,
  §7); `anchors auto` and `clutch auto` as in `brick`.
- No `footprint`, no `origin`: both derive from `pieces`. The pattern is recentred on the panel
  centre and never scaled; a pattern bbox exceeding `8·c·f × 8·r·g` is an error naming the
  smallest `pieces` that fits (V15's sibling, defined with the Milestone B validator set).
- `blanks` — a cell whose fragment is empty still prints as a blank brick by default (`emit`),
  because a hole in the wall of pieces is worse than a blank; `skip` omits it and the layout
  report says so. `slivers` — fragments thinner than the printable floor are dropped by default
  with their area reported (§6 V15 makes the ledger close), `keep` passes them to the kernel
  (which may refuse), `error` refuses the mural. These two are policy choices recorded in D-013
  (C5), not empirical constants — hence no `**Default:**` provenance marker: there is no
  measurement they could cite.

## 5. The cut rule — nominal lines cut art, physics clips bodies

The single load-bearing convention of the family:

1. **Art is cut at nominal grid lines** — pure multiples of 8.0 mm. The decomposition injects the
   c−1 + r−1 interior cut lines into the pattern's planar graph as extra edges (the same
   `extractPlanarGraph` route `clip pattern to boundary` uses), so both sides of every cut share
   **bit-identical vertices** by construction. Seam continuity is not a tolerance to manage; it is
   an identity the graph guarantees. Faces are bucketed to cells by centroid (they cannot straddle
   — they were split at the lines) and reassembled per piece in piece-local frame.
2. **The physical body clips each fragment 0.1 mm per side.** A fragment reaches its cell's
   nominal edge; the piece's body stops at `8f−0.2`. The kernel (§7) clips the relief pocket at
   the body outline and reports the clipped area. Exactly 0.2 mm of art is interrupted per seam —
   the arithmetic in §3.1 — and **no art offset is ever applied**: the 0.1 mm inset is physical
   truth, and pre-shrinking the art to "fit" the body would double-count it (the K10 mistake in
   miniature).

Nothing in the decomposition performs polygon clipping; there is still no 2D boolean in
bikar-core. The pattern is one planar graph before the cut and a partition of faces after it.

## 6. Validators — the mural set (V14+, continuing lego-lab's V1–V13)

Per-piece rules V1–V13 run unchanged on every emitted piece, prefixed `P_c<i>r<j>:`. The mural
adds panel-level validators. Numbering continues the lego-lab table; the D2 discipline (a
hand-constructed failing example per validator) applies to each.

### V14 — every emitted piece is anchorable, or the mural says which are not

**Validator:** V14 collects, per piece, the anchor solver's result; a piece with zero surviving
anchors is an ERROR unless `anchors none` was declared, in which case the layout report must list
it under "unclutched pieces". A 1×1-stud piece can never host a tube (tubes need a 2×2 lattice
cell) and hosts a pin only if the pattern leaves the centre solid.
PASS: the worked 4×4-of-4×4 mural — every piece is 4×4 studs, hosting up to nine tube candidates;
even `Star-Brick`-class relief that drops 8 of 9 keeps one.
FAIL: `pieces 32 x 32 of 1 x 1` — every piece is 1×1; the solver returns no tubes anywhere, V14
refuses the mural and names the smallest piece size (`2 x 2`) that admits tubes, instead of
emitting 1,024 decorative tiles that fall off the plate.

### V15 — the area ledger closes

**Validator:** Σ (fragment areas assigned to pieces) + Σ (dropped sliver areas) must equal the
pattern's total bounded-face area within rel 1e-6. Anything else means the decomposition lost or
double-counted art silently — the same invariant the kernel enforces for its own top-face
partition (§7), lifted to panel scale.
PASS: the worked mural with `slivers drop` — the report prints e.g. "art 4 811.20 mm² = kept
4 809.86 + dropped 1.34", and the sum is exact to the tolerance.
FAIL: a bucketing bug that assigns a face crossing x = 96.0 mm to *both* neighbouring cells
(possible only if the cut-line injection missed that face's edge) — the ledger over-counts by that
face's area, V15 refuses, and the error names the face's centroid rather than shipping a mural
with one motif printed twice.

### V16 — seam continuity is checked, not assumed

**Validator:** for every interior cut line, the set of relief-boundary vertices each adjacent
piece places **on** that line (in panel frame, before recentring) must be equal as exact
coordinate sets. The graph guarantees this by construction (§5); V16 exists because "guaranteed by
construction" is a claim about code that a refactor can silently break, and a seam mismatch is
invisible until two pieces are printed and butted.
PASS: any mural produced by the §5 injection path — both sides inherited the same split vertices,
sets identical.
FAIL: a hand-built counterexample that recentres one piece with a rounded (float32) offset before
comparing — vertex x = 12.800000190734863 vs 12.8 on the neighbour; the sets differ, V16 names the
cut line and the first mismatched vertex, and the doc's own guarantee is demoted from prose to a
tested invariant.

### V17 — the layout report and the export agree

**Validator:** the layout report's piece table (name, cell, studs, anchors kept, blank/sliver
notes) must enumerate exactly the parts the export emits: same names, same count, blanks included
under `blanks emit` and listed-as-omitted under `blanks skip`.
PASS: the worked mural under `blanks emit` — 16 rows, 16 STLs, zero omissions.
FAIL: `blanks skip` with two empty corner cells and a report that still prints 16 rows (or an
export that emits 14 files while the report claims 16) — V17 refuses; a mural whose paperwork
disagrees with its parts is the assembly-instructions bug class, caught at compile time.

## 7. Kernel — edge-to-edge relief (bikar Milestone A, shipped)

The seamless-first decision required retiring a real kernel refusal: `requirePocketsInsideCavity`
rejected any relief pocket crossing the ~1.5 mm cavity wall, which would have imposed a blank
stripe ≈3.4 mm wide at every seam (1.5 wall + 0.1 relief, twice, plus the 0.2 gap). This shipped
2026-08-02 as bikar `54615ff` on `feat/edge-to-edge-relief`, decision doc
`bikar:docs/decisions/2026-08-02-edge-to-edge-relief-top-face-arrangement.md`. Summary of record:

- **Dispatch, not rewrite.** A brick whose pockets all stay strictly inside the cavity takes the
  legacy nested partition, byte-identical to before — verified by sha256 over all seven shipped
  `patterns/Lego/*.bkr` presets. A pocket that touches or leaves the cavity ring
  (`pocketLeavesRing` — vertex *and* edge-intersection test) routes to a scoped planar arrangement
  (`bikar:packages/core/src/kernel3d/brick-top-face.ts`).
- **Four face classes** (band / band-under-pocket / ceiling / ceiling-under-pocket), each with its
  own z-life in the slab stack; every cell comes from one planar subdivision, so shared boundaries
  reuse bit-identical coordinates and the solidifier's twin cancellation holds — the reason a
  vendored polygon-boolean was rejected a second time.
- **Body-outline clipping is a feature.** Pockets past the physical outline are clipped and the
  dropped area is reported — this is precisely §5's cut rule meeting §3.1's arithmetic.
- **Guards**: a stud circle meeting a crossing pocket throws (studs and edge-crossing relief
  cannot share a top face — hence `studs none` as the mural default); islands and anchors
  straddling a region boundary throw; a weld-clearance check throws when two top-face features
  come within the 1e-3 mm mesh weld tolerance; an area invariant (kept cells tile the body,
  rel 1e-6) turns any partition bug into a loud failure instead of a leaky mesh.
- **Known limit, carried forward**: a crossing pocket can leave a top-view band strip thinner than
  0.7 mm that `brickMinFeature` does not measure (it measures named dimensions, not arrangement
  slivers). The mural's `slivers` policy (§4) is the mitigation at the layer that knows the art;
  this is why sliver handling is a required policy rather than an afterthought.

**This section amends `lego-lab-design.md` §7.2 to historical in one respect.** Its correction 3
states that geometry crossing a partition boundary "needs the 2D boolean this partition exists to
avoid" and can only be dropped. For **anchors straddling a pocket edge** that remains true and
`droppedForRelief` remains the behaviour. For **pockets crossing the cavity ring** it is no longer
true: the arrangement partitions them without any boolean. The lego-lab statement was correct
about its construction at its commit (`6b38342`); it is not a statement about the kernel after
`54615ff`.

## 8. What Milestone B builds (forward pointer, not spec)

The decomposition internals (§5's graph injection), per-piece `BrickSpec` minting, the
assembly-shaped result with `mural3d` provenance, the report printer, and validators V14–V17 land
in bikar Milestone B with their own tests and decision doc (`mural-panelization`). This document
is the product-side contract those changes are held to; where building them proves a section wrong,
the section gets corrected in place and the deviation recorded, per house convention.

---

## Appendix A — sources

The research behind every dimensional, prior-art, and acuity claim in this document is checked in
verbatim at [`research/lego-baseplate-seam-survey.md`](research/lego-baseplate-seam-survey.md)
(produced 2026-08-02; provenance header names this doc as its consumer). Per-claim fetch status —
including which numbers are **snippet-only** and which fetches failed — is recorded there, not
duplicated here. Load-bearing items used above: LDraw 3811/4186 part files (8.0 mm pitch, 1.6 mm
baseplate slab), Cailliau + Brick Owl + latericius (the 0.2 mm inter-part gap, three ways), the
absence finding on clone-plate pitch consistency (§2.2), the split-pattern prior-art gap (§3), and
the acuity/FDM-error numbers (§4).

The C4 adversarial grounding audit of this document is preserved verbatim at
[`research/lego-pattern-set-grounding-audit.md`](research/lego-pattern-set-grounding-audit.md)
(2026-08-02): claim-by-claim verdicts, the counter-evidence deep dives behind §1's near-miss
paragraph and B.1's tuned-printer divergence, citation spot-checks (five fetched, all confirmed
except B.4's bulge attribution, fixed), and the two K7 defects this revision corrects.

## Appendix B — contested bets and divergences

Entries tagged `[CAL-…]` are empirical bets no source can close; ids live in the registry
([`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md)), which names the
settling coupon. The status line at the top of this document claims no audit and no measurement;
these entries are why.

**B.1 — Seam registration on a real plate.** [CAL-REG-01 — coupon LG-P1] The doc's central visual
claim — pieces on a baseplate reconstitute the pattern — assumes the lateral jog of a relief line
crossing a seam stays below annoyance threshold. *Strongest counter:* FDM XY error (±0.1–0.3 mm,
fetched JLC figure) exceeds vernier-acuity detection (4–11 µm ideal-edge equivalent at 45 cm) by
one to two orders of magnitude, so a detectable jog is the *expected* outcome, not the tail risk;
and no tuning of the 0.2 mm gap corrects a lateral jog. *Tuned-printer counter to the counter
(C4 audit):* Bambu-forum calibration threads report holding ±0.05 mm XY after per-filament flow
calibration (unverified snippets) — the JLC band is a service-bureau envelope, not a floor. This
narrows but does not overturn the bet: even ±0.05 mm per piece yields relative seam jogs of
50–100 µm, five to ten times the vernier bound, so a detectable jog remains the expected outcome
on the best available printer; "one to two orders of magnitude" is the uncalibrated worst case.
LG-P1 (two 2×2 pieces, one motif crossing the seam, on one genuine and one clone plate) measures
apparent seam width and jog. Until it prints, "reconstitutes the pattern" is a bet. LG-P1 is
print-gated and **held** pending a printer; its catalog entry in
[`.claude/skills/prototype/catalog.md`](../.claude/skills/prototype/catalog.md) is authored in C8
and did not exist when this doc first shipped (audit finding 10).

**B.2 — Clone-plate behaviour.** [CAL-CLB-01 — coupon LG-P2] §3.3's scoping ("LEGO-brand verified;
clone unmeasured") rests on an absence: no surveyed source measures clone pitch consistency over a
multi-stud span. *Strongest counter:* the same absence cuts both ways — clones may be fine
(Brickyard's qualitative "near perfect match" suggests some are), and the scoping may be
needlessly conservative. Either way the datum does not exist until LG-P2 produces it. Held with
B.1.

**B.3 — "Align cuts with construction lines" as the visibility answer.** No CAL id — this is a
design inference, not a measurable constant. The survey's acuity chain (§4) establishes the seam
will be *detectable*; the leap from "detectable" to "acceptable if intentional-looking" is
aesthetic judgment with no source. If LG-P1's printed coupon reads as broken rather than gridded,
this stance — and §3.1's design posture with it — is wrong, and the fallback (wider deliberate
grout, or engraved seam channels) becomes a v2 question.

**B.4 — Elephant's foot vs the 0.2 mm gap.**
**Default:** first-layer elephant-foot compensation ≈0.2 mm at a 0.4 mm nozzle, per
[help.prusa3d.com](https://help.prusa3d.com/article/elephant-foot-compensation_114487) — vendor
guidance, not a measurement on our printer. *The bet:* uncompensated first-layer bulge can close
the entire designed gap and mechanically prevent flush seating — a failure mode the top-view
arithmetic in §3.1 never sees. The Prusa page does **not** quantify the bulge (the C4 audit caught
this doc attributing "0.1–0.2 mm per side" to it); we infer its order from the 0.2 mm compensation
default that removes it, and community caliper examples (unfetched blog measurements:
~0.25–0.3 mm per side on uncompensated prints) suggest it can run *larger* than our whole designed
gap — the bet's failure mode is more credible, not less. LG-P1's coupon prints with compensation
on; if seating still binds, the piece footprint may need a bottom-chamfer, which would be a kernel
change (a fifth slab) and is deliberately **not** designed until measured.
