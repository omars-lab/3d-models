<!--
  Grounding audit produced 2026-09-01 by an adversarial research agent
  (Agent tool, general-purpose) run under .claude/skills/ground-design-doc.
  Feeds: docs/rosette-pin-explorer-design.md (draft -> grounded; Appendix A and B).
  Preserved verbatim, exactly as returned. The agent was interrupted once by a
  usage limit and resumed; this is its single final report. It read bikar only
  at git refs 3900371 (the doc's pin) and origin/main 74eab002, never a working
  tree. The fetched dimensional quotes in deep dive 1 (Lugnet FAQ, Munafo,
  Cailliau, orionrobots) are the research record for the doc's §3 — restated
  here so the doc survives link rot.
-->

# Grounding audit: rosette-pin-explorer-design.md

Audited at 3d-models `master` (working tree, 2026-09-01), bikar read only at git refs: the doc's pinned `3900371…` (`39003717177f5237c8cc4a59498405da616f2607`) and `origin/main` = `74eab002fb25242bb64a8c8b3f20b8a037e5d63a`. Settled verdicts from `docs/research/lego-lab-grounding-audit.md`, `docs/research/lego-baseplate-seam-survey.md` and `docs/research/pattern-outline-brick-grounding-audit.md` are reused, not re-litigated. No file was edited.

## Claim-by-claim verdicts

| # | Claim (doc §) | Verdict | Supporting evidence | Refuting / qualifying evidence |
|---|---|---|---|---|
| a | §2 rosette kernel: φ=π/n, proportioning radius R(1−sinφ), shoulder solve on the perpendicular bisector of EH, base hexagon [E,G,H,X,H′,G′], star from v[3],v[4], n+1 pieces, defaults `180/n` and `cos2φ/cosφ`, ranges n≥5, 0<angle<90, 0<f<cosφ | **GROUNDED** | `bikar:packages/core/src/kernel/rosette.ts@3900371` L216 `proportioningRadius = radius * (1 - sinPhi)`; L224–226 E,H,X; L236–249 linear solve `t = (w·w)/denom`; L253 `base = [E, G, H, X, mirror(H), mirror(G)]`; L264–280 rotation by `2·φ·j`, star pushes v[3],v[4]; L100–102 `180 / n`; L130–133 `cos(2φ)/cosφ`; L163 angle range; L166–172 `> 0 && < cosPhi`. File byte-identical at `origin/main`. | One omission: `rosetteReflexOnsetAngle(n) = 45 + 90/n` (L115–117) bounds the *useful* dial range and is not mentioned; the dial's declared ceiling is 90 (L163), so a slider can reach reflex petals. |
| b | §2 pinned links `rosette.ts#L101`, `evaluator.ts#L8006`, `rosette.ts#L132` at `3900371` | **GROUNDED** | All three resolve to the quoted lines at that ref: L101 `return 180 / n;`; `evaluator.ts` L8006 `const angleDeg = node.angle ? resolveNumeric(env, node.angle) : rosetteParallelAngle(n);`; L132 `return Math.cos(2 * phi) / Math.cos(phi);` | — |
| c | §3 LEGO constants table (pitch 8.0; stud 4.8 "or 5.0"; tube 6.5137; bore 4.8; pin 3.2; rib 0.1/0.8; fit −0.2 → pin 3.0 / tube 6.314; "7.985 on Lugnet's survey, ~0.015/pitch, ~0.24 mm over 16 studs") | **CONTESTED** | Constants match `bikar:packages/core/src/kernel3d/lego.ts@3900371` L34, L43, L70, L103–109 (`2·(8/√2 − 2.4) = 6.5137`), L133–140 (RIB 0.1 provisional, CAL-RIB-01), L178 (0.8), L228–238 (`DEFAULT_BRICK_FIT` all −0.2 diametral). Arithmetic 3.2−0.2=3.0, 6.5137−0.2=6.3137 ✓. | (i) Lugnet's own page says **7.986 ± 0.002 mm** (Munafo), not 7.985 — 7.985 is orionrobots' paraphrase. (ii) Munafo measured a **wall of Technic beams** (112 studs = 895 mm); the doc applies it to a **baseplate** grid with no K10 transfer sentence. (iii) Cailliau measured **a 48×48 baseplate** across 37 units: **7.993 ± 0.007** ("8 mm to within better than one hundredth"). (iv) 16-stud drift is therefore 0.11 mm (Cailliau) to 0.22 mm (Munafo), not "~0.24". (v) The "5.0" stud and orionrobots' 6.31/0.657 are not independent measurements (see deep dive 1). (vi) `lego.ts` L34 calls pitch "the one uncontested number" and the seam survey §1.3 reads Cailliau as evidence that pitch does *not* accumulate error — the doc's row contradicts both without saying so. |
| d | §4 anchor rules: cellReach 3.9; tube reach 3.657 / pin reach 2.0; `anchorKind` (c≥2∧r≥2 tube, 1×1 none, else pin); four anchorability criteria (studs≥2, anchors≥1, wall≥0.8, shell≥1.2); SNAP 0.05 | **GROUNDED** (ARGUED) | `grid-gate.ts@3900371` L110 `SNAP_THRESHOLD_MM = 0.05`; L113 `ANCHOR_CLEARANCE_MM = 0.4`; L116 `MIN_SHELL_WALL_MM = 1.2`; L119 `MIN_ANCHOR_WALL_MM = 0.8`; L156–159 `anchorKind`; L256 `cellReach = 8/2 − 0.2/2 = 3.9`; L276–277 `reach = outerDia/2 + fit.ribMm + 0.4` → tube (6.3137/2)+0.1+0.4 = 3.657 ✓, pin 1.5+0.1+0.4 = 2.0 ✓; L297 `wallMm`; L345 `anchorability`. | §4 carries **no pinned links** and the lines have moved at `origin/main` (constants now L122/125/128/131; anchorability L523–575; new `solveAnchorsOnGlobalGrid` at L342 with `cellReach` L422, `reach` L458). The explorer actually calls the *global-grid* solver (`rosette-explorer.ts@origin/main` L308–309) with `anchorability(sol, +∞, true) // skip shell-wall` — so the shell-wall criterion the doc lists as one of four is **deliberately skipped** in the instrument. The rules are the same; the doc should say which function and which skip. |
| e | §4 clutch lobes: tube 4 lobes at 45°/135°/225°/315° + bore; pin 3 lobes at 90/210/330 "odd, so opposing lobes cannot cancel"; linear rib ramp; min feature 0.7 | **GROUNDED** | `brick.ts@3900371` L393 `anglesDeg: [45, 135, 225, 315]`; L401 bore at `ANTI_STUD_BORE_DIA_MM/2` (no fit knob); L410 `[90, 210, 330]`; L404 comment "odd count, so opposing lobes cannot cancel"; L231–254 `ribbedCircle` linear ramp to 0 at ±arc/2; L83–93 `BRICK_MIN_FEATURE_MM = 0.7` with comment that lego-lab §7.4's 0.8 was wrong (default tube wall (6.5137−0.2−4.8)/2 = 0.757). Explorer draws the real lobes via `ribbedRingPoints` (L421). | Rib depth 0.1 is provisional (`CAL-RIB-01`, LG-F1 planned) — every lobe geometry the explorer draws inherits an unmeasured number. |
| f | §5 "printed-onto-printed **measured 0.00 mm** clutch on defaults in LG-S1" | **UNGROUNDED — K1 hardening of a computed value** | The 0.00 mm figure exists: D-006 (`docs/decisions-log.md` ~L430) "Total radial interference **computes** to 0.00 mm … `CAL-STK-01` is the bet … `LG-S1` the coupon"; `catalog.md` L908–975 LG-S1 "the arithmetic says 0.00 mm interference". | LG-S1 **Status: planned (printing on hold)**, "What we learned: — pending", print target TBD. `bets.md`: "20 provisional, **0 measured**"; CAL-STK-01 provisional, "LG-S1 settles it". Nothing was measured. Same failure kind as the taxonomy's `hemisphere-split` §3.2 (own survey's open question hardened into a ruling). |
| g | §5 SNAP_THRESHOLD K10 note lives in the mural plan; §5 D-005/D-006 citations | **GROUNDED** | `.claude/plans/fuzzy-snuggling-wind.md:54,60` carries the K10 note (also `docs/lego-pattern-set-design.md:97,164`); D-005 at `docs/decisions-log.md:291` (2026-07-30, knobs backed by CAL-* bets), D-006 at L352 (studs-as-ports). | The link `[mural](../.claude/plans/)` resolves to a **directory**, not the plan file — passes D1 but points at nothing readable. |
| h | §7 prior art: LEGO Art / World Map, dlvoy, MachineBlocks — "none address relief continuity across seams"; genuinely novel | **CONTESTED — K2 (unscoped exhaustiveness) + one omission** | Seam survey §3 (checked in) reaches the same conclusion for the systems it enumerates: LEGO Art 31203 (Technic pins, colour only), dlvoy (PNG → rectangle decomposition → MachineBlocks; flat, no relief), Finke, Brickapic (snippet-only, 403), mural vendors (UV/pad-print on moulded tiles), brickmosaicdesigner "relief style" (= stacked-plate height, not printed relief). My additional searches (multi-panel 3D-printed relief, lithophane multi-panel, LEGO-compatible relief mural) found general split-model alignment-pin practice but no LEGO-grid relief-across-seams tool. | MachineBlocks **does** ship per-brick relief today — `surfacePattern`/`surfacePatternSvg`/`…Depth` ("positive emboss, negative deboss"), `svg`/`svgDepth`, `text*`, `baseReliefCut*` (module docs, fetched) — and the doc's one-line dismissal omits it. The lego-lab audit already settled: "genuinely novel = Islamic pattern × LEGO printed part", *not* "relief on a LEGO brick". The claim survives only as "none of the N systems surveyed here". |
| i | §7 "Rosette-generation literature (n-fold rosettes from a proportioning circle) — matches R(1−sinφ)" | **GROUNDED for the radius; CONTESTED for "matches" as a whole** | Lee & Soliman 2014 (PDF fetched, `tilingsearch.mit.edu/RosetteAnalysis.pdf`), §2 standard construction: "Equal circles on B and C, tangent at E, determine the radius AF of a circle on A", with CF = CE = half the N-gon edge = R·sin(π/N), so AF = R − R·sinφ = R(1−sinφ) — the same circle bikar's L216 builds; characteristic 3 "angle ECF is 90° − 180°/N" is the bisector bikar's solve uses. bikar cites it (`rosette.ts` header L28–32; `docs/research/tesselations-stars-rosettes.md@origin/main` L58, L187). Kaplan 2005 (fetched): "hexagonal arms of a rosette around a central star", "nearly ideal in the sense given by Lee [19]" (A.J. Lee, *Muqarnas* 4 (1987) 182). | (i) The doc cites **no title, author, or year** — "rosette-generation literature" is a pointer to nothing. (ii) Lee & Soliman's standard rosette has **one** free parameter beyond N (characteristic 8: "N, and one other parameter, e.g. the crossover angle"); the inner point H's position "is determined by the size of the crossover angle" (characteristic 7). bikar exposes **two** dials (angle *and* `petalFraction`, L224–226 X = f·proportioningRadius independent of angle). The doc presents both as the rosette's "two free choices"; the second is bikar's generalisation, not the literature's. (iii) Label swap: bikar's fixed point on the proportioning circle is called H (L225, on the ray toward the n-gon vertex); in Lee & Soliman that fixed point is **F** (on side AC) and H is the sliding inner point. Harmless in code, misleading in prose that claims to "match". |
| j | §6 Track 1 shipped: bikar PRs "#123 `42b22b3`, `7674683`, #125 `ac26658`", #126 `cff3cf1`, #127 `821dfe7`; §6.6.1 "picker ships with Rosette-N and Star-N; none of the girih, hex-field or rational-repeat figures … are on it yet" | **CONTESTED — two misattributions and one stale section** | `gh`/`git -C bikar`: #123 = `42b22b3` (2026-08-31) ✓; #125 = `ac26658` ✓; #126 = `cff3cf1` ✓; explorer exists at `origin/main` (`packages/web/src/rosette-explorer.ts`, `catalog.ts:196–199`, `vite.config.ts:444,598`, `rosette-explorer.html`, tests L51–258). | `7674683` is **#124** ("expose dropped anchor positions"), not #123. `821dfe7` is a branch commit; #127's merge sha on `origin/main` is **`6d17651`** (2026-08-31, "…pattern picker… (#127)"); `821dfe7` is not reachable from `origin/main` (`git log origin/main | grep -c 821dfe7` = 0). §6.6.1 is **stale**: PR **#134 `85269ac`** (merged 2026-09-02T02:01Z, "widen the rosette explorer's roster — girih, a hex field and a square-lattice field") put Girih-10, Girih-Decagon, Hex-Tiled, Star-8-Tiled on the roster (`rosette-explorer.ts@origin/main` L130–141). Note #134 merged *after* the doc's provenance date, so this is drift, not an error at authoring time — but the doc is now wrong on disk. |

## Counter-evidence deep dives

### 1. §3 LEGO dimensions — Lugnet, orionrobots, and what was actually measured

**What the doc says.** Pitch 8.0 with "7.985 on Lugnet's survey (~0.015/pitch, ~0.24 mm over 16 studs)"; stud "4.8 (or 5.0 per orionrobots)"; sources list orionrobots "fetched 2026-08-29" giving 8 / 5.0 / 1.7 / 6.31 / 0.657 / 1.5, Lugnet 7.985, brickowl 403.

**What the sources say (all fetched this audit unless marked).**

- **orionrobots** (`https://orionrobots.co.uk/pages/lego-specifications.html`, HTTP 200; the doc's 2005 blog URL returns 404): "Spacing of stud centers: 8", "Stud pitch = 7.985 on Lugnet – although 8mm is commonly used", "Diameter of studs: 5", "Height of studs: 1.7", "Outer diameter of cylinders…: 6.31", cylinder walls 0.657, walls 1.5, plate 3.2 (Lugnet 3.194). Every one of these numbers is either (a) Poskanzer's line from the Lugnet FAQ verbatim ("Spacing of stud centers: 8", "Diameter of studs: 5", "Height of studs: 1.7") or (b) the tangency formula with a 5 mm stud: 2·(8/√2 − 2.5) = 6.314 → "6.31", wall (6.314 − 5)/2 = 0.657. The lego-lab audit settled (b) already; (a) is new. **orionrobots is not a survey and not a measurement; it is Lugnet with one transcription slip (7.985 for 7.986).**
- **Lugnet FAQ** (`https://www.lugnet.com/~330/FAQ/Build/dimensions`, 200): Munafo — "the stud pitch distance is **7.986 millimeters, plus or minus 2 microns**", brick 9.582, plate 3.194; Poskanzer — 8 / 5 / 1.7; Bliss — LDraw 20 LDU.
- **Munafo** (`mrob.com/pub/mcg.html`, 200): "the LSS is 7.986±0.002 mm" (1999 posting said 7.987), measured on a wall of late-1990s **Technic beams**, 112 studs = 895 mm.
- **Cailliau** (`cailliau.org/…/General Considerations`, 200): "**7.993 mm ±0.007 mm or 8 mm to within better than one hundredth of a mm**", measured across **37 horizontal units on a 48×48 knob base plate** (295.75 ± 0.25 mm); knob diameter 4.9, knob height 1.8, play 0.1 mm per side (2×4 = 31.8).
- **Bartneck** (200): "There is a 0.2mm gap between bricks next to each other" (his drawings: Ø4.8 stud, Ø6.51 tube, wall 1.2, stud height 1.7 — settled in lego-lab audit).
- **Brighton Toy Museum**: 403 on this fetch; lego-lab audit's settled record is micrometer 4.88–4.89 "deliberately oversized". A search snippet attributes "a 2019 patent gives … studs … 4.8mm" to **WO2019106129 A1** ("Toy building bricks made of biopolymeric material") — **(unverified snippet)**; not fetched, do not cite as fetched.
- **lego.com** stud-and-tube history page (200): no numeric dimensions at all.
- **brickowl** stud-dimensions page: 403 (matches the doc; seam survey's settled record: 1.7 stud height, 8x − 0.2 footprint).

**Consequences for the doc.**

1. The pitch row cites the wrong number from the wrong page for the wrong part. The measured pitch that is *about a baseplate* — which is what the explorer's global grid represents — is Cailliau's 7.993 ± 0.007, giving 0.11 mm over 16 studs, half the doc's "~0.24". Munafo's 7.986 ± 0.002 is Technic beams; it may transfer to plates (same tool-family, same shrinkage regime) or may not — the doc must write the transfer sentence (K10) or use the baseplate number.
2. The doc's own kernel disagrees: `lego.ts@3900371` L34 calls 8.0 "the one uncontested number", and the seam survey §1.3 reads Cailliau as showing pitch does *not* accumulate error. The doc silently overrules both (K7 — read against the corpus).
3. "4.8 (or 5.0 per orionrobots)" presents Poskanzer's rounded 5 as a competing datum. The measured class is 4.85–4.9 (Cailliau 4.9, Brighton 4.88–4.89, binderclipscorpion 4.88); the nominal class is 4.8 (LDraw 12 LDU, Bartneck, BrickOwl, patent snippet). 5.0 belongs to neither and should be dropped or labelled "rounded".
4. The −0.2 diametral fit is a knob (D-005: "a knob is not a measurement"). The doc's table rows for "effective pin 3.0 / tube 6.314" are correct arithmetic on an unmeasured knob; they should carry `CAL-*` ids, not bare numbers (K4 → D3 applies if any is marked as a `**Default:**`).

### 2. §5 "measured 0.00 mm" — LG-S1 has not been printed

Traced every occurrence:

- `docs/decisions-log.md` D-006 (~L430): "Total radial interference **computes** to 0.00 mm on the shipped defaults … `CAL-STK-01` is the bet … `LG-S1` the coupon."
- `.claude/skills/prototype/catalog.md` L908–975, LG-S1: "**Status**: planned (printing on hold…)"; "On the shipped defaults that leaves total radial interference at **0.00 mm** — a stack that seats face-to-face with no clutch at all. bikar reports it as a warning on every `Brick-Stack` render"; Q2 "Does the shipped default really not clutch? **The arithmetic says** 0.00 mm interference. Print the −0.20 rung…"; "**What we learned**: — pending."; print target TBD.
- `.claude/skills/calibrate/bets.md`: "21<!--count:cal-bets--> registered bets · 21<!--count:cal-records--> `Calibrated` records — **21 provisional, 0 measured**"; CAL-STK-01 provisional (`STUD_ENTRY_MAX_MM_CAL` 0.15 at `lego.ts` L163–170), "LG-S1 settles it".

The 0.00 mm is stud ⌀ 4.8 minus stud-port entry (4.8 + 0 with −0.2 knob cancelling the +0.2 relief) — a subtraction, reported by bikar as a *warning*, whose whole purpose in LG-S1 is to be tested. The doc's sentence turns the coupon's open question into its answer. This is the exact K1 pattern the taxonomy records for `hemisphere-split` §3.2, and it is the most load-bearing single defect in the doc because §5 uses it to argue that printed-onto-printed stacking is a solved case the explorer need not model.

### 3. §7 prior art and the novelty claim

- **LEGO Art 31203 / World Map**: seam survey §3 — Technic-pin joined plates, colour mosaic, joints pop; nothing about relief. Consistent with the doc.
- **dlvoy** (README fetched): PNG → rectangle decomposition → OpenSCAD via MachineBlocks; flat top, no relief, no seam handling. Consistent.
- **MachineBlocks** (module docs fetched): `surfacePattern`, `surfacePatternSvg`, `surfacePatternDepth` ("Positive emboss, negative deboss"), `svg`/`svgSide`/`svgDepth`, `text*`, `baseReliefCut*`; multi-brick only via nested offset/align, no mosaic or seam feature. **So it does relief on a brick top today** — the lego-lab audit's settled verdict — and the doc's §7 line omits that, which is what lets "none address relief" read as "none do relief". It does not split one relief across bricks; the doc's claim is true of it only in the narrower sense.
- **Brickapic**: seam-aware panelization (snippet-only, 403 — seam survey's record). Unverified, but it is the closest neighbour and the doc does not name it.
- **brickmosaicdesigner "relief style"**: stacked plates for height — colour/height mosaic, not printed relief.
- **General 3D-print practice** (search, no primary fetch): dowel/pin alignment for split large prints, seamless repeating wall tiles with tabs/magnets — relief continuity across seams *is* a known problem with known answers off the LEGO grid; the doc's novelty is the LEGO-grid registration, not the seam problem itself.
- **Custom LEGO mural vendors**: UV/pad print on moulded tiles (seam survey) — image continuity across tiles is their whole product, at zero relief.

Net: the K2 sentence must be scoped to the enumerated set, MachineBlocks must be credited for per-brick relief, and the novelty statement narrowed to what the lego-lab audit already settled — Islamic pattern × LEGO-registered printed part, with relief carried across piece seams.

### 4. Rosette literature

Lee & Soliman 2014 §2 (fetched, extracted with pdftotext): the standard construction's proportioning circle is the circle on A of radius AF where CF = CE = half the N-gon edge; that is R − R sin(π/N) = R(1−sinφ), which is exactly `rosette.ts` L216. Characteristic 3 gives the bisector angle 90° − 180°/N that bikar's `docs/decisions/2026-08-24-rosette-primitive.md` discusses. Characteristic 4 (EG = FG) is what `rosette-witness.test.ts` freezes and what `Rosette-N.bkr`'s header quotes. So the formula is grounded — but only if the doc names the source, which it does not.

Two qualifiers the doc strips: (i) Lee & Soliman's standard rosette is a one-parameter family beyond N; bikar's `petalFraction` is a second, independent dial (L217, L226), and the default `cos2φ/cosφ` is what makes the default figure coincide with the standard construction — a claim I have not verified numerically and the doc does not state. (ii) A.J. Lee's web page ("critical proportioning circle" at the peripheral point) and Kaplan 2005 ("nearly ideal in the sense given by Lee") describe the *same* circle; Kaplan is the source for "hexagonal arms around a central star", which the doc's anatomy sentence echoes without citation.

### 5. PR shas and the roster

`gh pr list`/`git log` on bikar `origin/main`: #123 `42b22b3`, **#124 `7674683`** (doc folds it into #123), #125 `ac26658`, #126 `cff3cf1`, **#127 `6d17651`** (doc cites branch commit `821dfe7`, unreachable from `origin/main`), **#134 `85269ac`** 2026-09-02 widened the roster to six patterns. The explorer test file (`packages/web/tests/rosette-explorer.test.ts@origin/main` L182–258) already exercises the wider roster ("every roster entry is in the bundle", "Star-N brings a different schema"). §6.6.1's "none … are on it yet" is false on disk today.

## Citation spot-check results

| Citation | Result |
|---|---|
| `rosette.ts#L101` @3900371 | Resolves; line is `return 180 / n;`. Unchanged at `origin/main`. |
| `evaluator.ts#L8006` @3900371 | Resolves; line is the `angleDeg` default to `rosetteParallelAngle(n)`. |
| `rosette.ts#L132` @3900371 | Resolves; `return Math.cos(2 * phi) / Math.cos(phi);`. |
| orionrobots "fetched 2026-08-29" | Numbers match the live `/pages/lego-specifications.html` (200). The URL form in the doc (2005 blog post) returns **404**. Figures are Lugnet/Poskanzer transcriptions plus the 5 mm-stud tangency formula — not independent. Its "7.985" is a transcription of Lugnet's 7.986. |
| Lugnet 7.985 | **Lugnet says 7.986 ± 0.002** (Munafo, Technic beams). 7.985 appears nowhere on the Lugnet page. |
| brickowl stud-dimensions | 403 — as the doc says. |
| D-005, D-006 | Both present at `docs/decisions-log.md:291` and `:352` with the content the doc attributes. |
| `[mural](../.claude/plans/)` | Resolves to a directory; the K10 note is in `fuzzy-snuggling-wind.md:54,60`. |
| bikar PR shas | #123, #125, #126 correct; `7674683` → #124; `821dfe7` → not the merge sha (`6d17651`). |

## Misgrounded or missing citations

1. **§5 "measured 0.00 mm … in LG-S1"** — misgrounded: cites a planned, unprinted coupon as a measurement. Correct ground is D-006 ("computes") + CAL-STK-01 (provisional).
2. **§3 pitch row** — misgrounded: attributes orionrobots' 7.985 to Lugnet; omits Cailliau's baseplate measurement (7.993 ± 0.007), the only fetched number measured on the part class the explorer models; no K10 transfer sentence for Technic-beam → baseplate.
3. **§3 "5.0 per orionrobots"** — orionrobots' 5 is Poskanzer's Lugnet line; 6.31/0.657 derive from it. Cite Lugnet/Poskanzer, mark as rounded, or drop.
4. **§7 rosette literature** — missing citation entirely: should be Tony Lee & Ayman Soliman, *The Geometric Rosette: analysis of an Islamic decorative motif* (2014, `tilingsearch.mit.edu/RosetteAnalysis.pdf`), with A.J. Lee, *Muqarnas* 4 (1987) 182 and Kaplan 2005 (*Islamic Star Patterns from Polygons in Contact*) as the secondary anchors — all three already cited in bikar's `docs/research/tesselations-stars-rosettes.md`.
5. **§7 MachineBlocks** — missing the `surfacePattern`/`svg`/`baseReliefCut` modules; the sentence as written under-reports a system inside the surveyed set (the `piece-composition` K2 pattern).
6. **§7 Brickapic and mural vendors** — the seam survey's nearest neighbours are absent from the doc's enumeration; either list them or cite the survey's §3 as the enumeration.
7. **§4** — no pinned links at all for `grid-gate.ts`/`brick.ts`; every number in §4 is a line-number claim without an anchor, and the lines have moved at `origin/main`. Also does not say the explorer uses `solveAnchorsOnGlobalGrid` and skips the shell-wall criterion.
8. **§6** — `7674683` mis-assigned to #123; `821dfe7` is not #127's sha on main; §6.6.1 stale after #134.
9. **§2** — `rosetteReflexOnsetAngle` (`rosette.ts` L115–117) unmentioned; the dial's declared 0–90 range includes reflex petals above 45 + 90/n.
10. **Provenance** — "ports from working tree 2026-08-29" is not a ref; every bikar fact should carry `3900371` (which the §2 links already do) or `origin/main`'s sha.

## Recommended doc changes

1. **§5** — replace "printed-onto-printed measured **0.00 mm** clutch on defaults in LG-S1" with: "printed-onto-printed interference on the shipped defaults *computes* to 0.00 mm (D-006; `CAL-STK-01`, provisional); LG-S1 is the coupon that will measure it and has not been printed." Any conclusion §5 draws from "no clutch" must be re-hedged to "if the computed 0.00 mm holds".
2. **§3 pitch row** — rewrite: "8.0 nominal (LDraw 20 LDU; `lego.ts` L34). Measured: 7.993 ± 0.007 on a 48×48 baseplate across 37 pitches (Cailliau); 7.986 ± 0.002 on a 112-stud wall of Technic beams (Munafo, via Lugnet). Over 16 studs: 0.11–0.22 mm. Transfers to the explorer's baseplate grid via Cailliau directly; Munafo's beam figure transfers only if beam and plate moulds share a shrinkage allowance, which no fetched source states." Delete "7.985" and add it to nothing — it is a transcription artefact.
3. **§3 stud row** — "4.8 nominal (LDraw 12 LDU, Bartneck, BrickOwl; a 2019 patent per an unverified snippet); measured 4.85–4.9 (Cailliau 4.9, Brighton 4.88–4.89, binderclipscorpion 4.88)". Drop "or 5.0 per orionrobots" or label it "Poskanzer's rounded figure on Lugnet, reproduced by orionrobots". Mark orionrobots' 6.31/0.657 as derived (settled, lego-lab audit).
4. **§3 sources** — replace the 404 orionrobots URL with `/pages/lego-specifications.html`; add Lugnet FAQ, mrob.com, cailliau.org as the primaries orionrobots paraphrases. Put the fetched text into a `docs/research/*.md` file with a provenance header (the CLAUDE.md "research is checked in" rule) — none of §3's web sources are currently recorded there.
5. **§3 fit rows** — attach `CAL-*` ids to the −0.2 diametral knob values (D-005) rather than bare "effective 3.0 / 6.314".
6. **§4** — pin links: `grid-gate.ts#L110,#L113,#L116,#L119,#L156,#L256,#L276,#L297,#L345` and `brick.ts#L83,#L231,#L393,#L404,#L410` at `3900371`; add one sentence that the explorer calls `solveAnchorsOnGlobalGrid` (added post-pin, `origin/main` L342) with the same reach/wall rules plus `droppedAnchorPositions`, and that it passes `anchorability(sol, +∞, true)` — shell-wall skipped by design, three criteria not four.
7. **§2** — add the reflex-onset ceiling `45 + 90/n` (`rosette.ts#L115` @3900371) beside the 0–90 dial range, and note that the explorer's slider can exceed it.
8. **§7** — (a) cite Lee & Soliman 2014 for R(1−sinφ) (circle on A of radius AF), A.J. Lee 1987 and Kaplan 2005 for the star + hexagonal-petal anatomy; (b) add: "Lee & Soliman's standard rosette has one free parameter beyond N; bikar's `petalFraction` is a second, independent dial whose default recovers the standard figure" (verify that last clause against `rosette-witness.test.ts` before writing it); (c) rewrite the prior-art sentence as "of the systems enumerated in `lego-baseplate-seam-survey.md` §3 (LEGO Art, dlvoy, MachineBlocks, Finke, Brickapic [snippet-only], pad-print mural vendors), MachineBlocks ships per-brick SVG/emboss relief; none found carries one relief across piece seams on the LEGO grid"; (d) narrow the novelty line to the lego-lab audit's settled form.
9. **§6** — `7674683` → "#124"; #127 → `6d17651` (or keep `821dfe7` and label it the branch head); rewrite §6.6.1 for #134 `85269ac` (roster now Rosette-N, Star-N, Girih-10, Girih-Decagon, Hex-Tiled, Star-8-Tiled) and move "girih … not on it yet" to the shipped record.
10. **§5 link** — point `[mural]` at `../.claude/plans/fuzzy-snuggling-wind.md` (L54/60), not the directory.
11. **Provenance** — replace "working tree 2026-08-29" with the two shas used here.

## Empirical residue

Numbers the doc uses that no fetched source measures and that only a print can settle (ARGUED vs EMPIRICAL as the calibrate skill frames it):

| Quantity | Doc value | Status | Bet / coupon |
|---|---|---|---|
| Printed-onto-printed stud/port interference on defaults | 0.00 mm | EMPIRICAL — computed only | `CAL-STK-01` (provisional) / LG-S1 (planned, unprinted) |
| Rib depth and arc | 0.1 / 0.8 mm | EMPIRICAL — provisional | `CAL-RIB-01` / LG-F1 (planned, blocks M6) |
| Diametral fit knob | −0.2 on stud, tube, pin | EMPIRICAL — a knob, not a measurement (D-005) | `CAL-CLB-01` / LG-P2 (no record) |
| Pin clutch (3 lobes, pin 3.0 effective) | asserted "cannot cancel" | ARGUED (geometry) + EMPIRICAL (does it hold) | LG-R1 (planned) — **no CAL id registered** |
| Pitch drift across a 16-stud piece | "~0.24 mm" | CONTESTED — measured 0.11–0.22 depending on part class; transfer to *printed* plates unmeasured | `CAL-CLB-01` covers fit, nothing covers printed-pitch drift; needs a bet or a coupon rung |
| Anchor-only (no perimeter) clutch sufficiency | implied by four criteria | EMPIRICAL | `CAL-ANC-01`, `CAL-INW-01` / LG-B2 (no record) |
| Stud ⌀ of the printed part vs moulded 4.85–4.9 class | 4.8 nominal | EMPIRICAL — no registered bet for stud ⌀ itself | none registered; lives inside LG-P2's fit rungs by implication only |
| Minimum tube wall 0.757 vs `BRICK_MIN_FEATURE_MM` 0.7 | 0.7 | ARGUED (nozzle-width reasoning in `brick.ts` L83–93) | none — should be a `CAL-*` if any doc states it as a `**Default:**` |
| Shell-wall criterion skipped in the explorer | +∞ | ARGUED (by design) | none needed; doc must say so |

Every empirical row above is provisional today: `bets.md` records 20 provisional, 0 measured. The doc contains no sentence that is currently backed by a measured print; the audit's principal correction is to stop it from claiming one.
