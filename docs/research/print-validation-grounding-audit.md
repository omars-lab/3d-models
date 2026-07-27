<!-- Adversarial grounding audit produced 2026-07-27 by a research subagent.
     Audits docs/print-validation-design.md: verifies its thresholds/defaults against
     slicer source and docs (CuraEngine, PrusaSlicer, Bambu Studio), hunts
     counter-evidence on the no-slicer bet, and drafts divergence justifications.
     Kept verbatim; its recommendations are applied in the design doc (Appendix B). -->

# Grounding audit: print-validation-design.md

Doc audited: `/Users/omareid/Workspace/git/3d-models/docs/print-validation-design.md` (DRAFT v1). Cited research verified on file: `/Users/omareid/Workspace/git/3d-models/docs/research/code-cad-composition-survey.md` §5, `/Users/omareid/Workspace/git/3d-models/docs/research/tile-craft-field-survey.md` §7.

## Claim-by-claim verdicts

| # | Claim / design bet | Verdict | Supporting URL(s) | Refuting / complicating URL(s) |
|---|---|---|---|---|
| 1 | "None of this needs a slicer" — build own slice simulation | CONTESTED (defensible for the browser Lab; needs a divergence note + CI oracle) | https://github.com/Cloud-CNC/cura-wasm (archived Aug 2021 — the only CuraEngine-in-browser option is dead) | https://github.com/prusa3d/PrusaSlicer/wiki/Command-Line-Interface (headless slicing exists); https://grid.space/kiri/ (actively maintained pure-JS browser slicer); https://trimesh.org/trimesh.base.html (`section_multiplane` — multiplane slicing is commodity) |
| 2 | 45° overhang default (F4) | CONTESTED — every flagship slicer defaults less conservative, and the literature says the threshold is not a fixed angle | — | PrusaSlicer `PrintConfig.cpp` (default 0 = auto, "recommended"); Cura `fdmprinter.def.json` (`support_angle` default 50°); BambuStudio `PrintConfig.cpp` (`support_threshold_angle` default 30° from horizontal = tolerates 60° from vertical); https://www.padtinc.com/2017/07/12/towards-self-supporting-design-for-additive-manufacturing-part-1-standard-guidelines/; https://www.tandfonline.com/doi/full/10.1080/0951192X.2018.1466398 |
| 3 | Support-map algorithm `region_i − dilate(region_{i−1}, h·tanθ)` | GROUNDED — this is literally CuraEngine's overhang formula | https://github.com/Ultimaker/CuraEngine/wiki/Generating-Areas ; https://github.com/Ultimaker/CuraEngine/blob/main/src/support.cpp ; https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/Support/SupportMaterial.cpp | Doc omits the angle convention (θ from vertical); PrusaSlicer measures from horizontal and uses `h / tan(θ)` — silent porting hazard |
| 4 | Island lifetime tracking, F2/F3, main body = largest bed-contact region | GROUNDED (primitive) / UNGROUNDED (main-body heuristic is the doc's own) | https://github.com/Ultimaker/CuraEngine/wiki/Generating-Areas (consecutive-layer diff + downward propagation is standard) | — |
| 5 | F5: erode by 0.21 mm, vanish = **error** | CONTESTED — Arachne prints features down to 0.1 mm; <2× half-width is not unprintable in modern slicers | — | PrusaSlicer `PrintConfig.cpp` (`min_feature_size` default 25% of nozzle = 0.1 mm; `min_bead_width` 85% = 0.34 mm); https://help.prusa3d.com/article/arachne-perimeter-generator_352769 ; Cura `fdmprinter.def.json` (`min_feature_size` 0.1 mm); https://toms3d.org/2022/07/28/arachne-in-prusaslicer-0-4mm-nozzles-just-became-obsolete/ (unverified snippet) |
| 6 | F6: 10 mm bridge default | GROUNDED (it is Bambu Studio's shipped default) but conservative vs measured capability | BambuStudio `PrintConfig.cpp`: `max_bridge_length` default **10.0 mm** | https://www.thingiverse.com/thing:4833153 (10–100 mm test); https://www.printables.com/model/193838-extreme-bridging-test-pieces-50-mm-350-mm ; https://www.3dmag.com/3d-wikipedia/3d-printing-bridging-settings-materials-and-limits/ (unverified snippet: well-tuned printers 50–80 mm) |
| 7 | F6 formulation: "max span between anchored ends" | CONTESTED (simplified vs established practice) | — | https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/BridgeDetector.hpp (bridge printability is direction-dependent; PrusaSlicer brute-force searches the angle minimizing/optimizing spanned line length) |
| 8 | F7 bed-contact area check | GROUNDED as prior art (no sourced floor value — doc admits) | https://github.com/ChristophSchranz/Tweaker-3 ; https://zenodo.org/records/5569145 (Tweaker scores orientation by bottom area + overhang + contour) | — |
| 9 | F1 union-find "near-free" | GROUNDED (standard; trivially true) | — | Nuance: two bodies sharing a single welded vertex pass F1 but still fall apart; F5 only partially covers this |
| 10 | Slicing 5,040 tris × 600 layers "trivial"; 45k tris "well under a second" | GROUNDED | https://www.inf.ufpr.br/murilo/public/CAD-slicing.pdf (Minetto et al., CAD 92, 2017 — fetched: even the *trivial* algorithm processes 200–250 M triangle–plane pairs/s; their optimal one 8–11 M items/s; Slic3r 6–8 M items/s). StarOrb = ~3 M pairs | Caveat: per-layer Clipper boolean/offset cost, not slicing, will dominate — unaddressed in doc |
| 11 | "One new 2D-boolean dependency (Clipper2-class) serves both" | CONTESTED — the sibling doc's recommended dependency already bundles it | https://manifoldcad.org/docs/html/classmanifold_1_1_cross_section.html ; manifold WASM bindings d.ts (verified: `Manifold.slice(height): CrossSection`, `project()`, `CrossSection.offset(delta, joinType, …)` — Clipper2-backed) | — |
| 12 | 0.2 mm layer height default; 0.21 mm = "extrusion half-width for 0.4 mm nozzle" | UNGROUNDED (uncontroversial) / minor error | — | 0.21 assumes 0.42 mm line width — Cura's default width is 0.40 (half = 0.20), PrusaSlicer's is 0.45 (half = 0.225); the assumed width should be stated |
| 13 | Appendix A links say what the doc claims | GROUNDED (verified on file) | composition-survey §5 (Clipper2 int64/simplify/offset pitfalls — matches); tile-survey §7 (holes 0.1–0.3 mm undersize, external ~0.1 mm oversize) | Minor: "±0.1–0.2 mm printed accuracy" is a paraphrase, not what §7 literally says |

## Counter-evidence deep dives

### Bet 1: "No slicer needed" / own the computational geometry

- https://github.com/prusa3d/PrusaSlicer/wiki/Command-Line-Interface — PrusaSlicer slices fully headless (`--export-gcode`, `--loglevel`); a CI dry-run against the real engine is cheap and catches actual toolpath behavior. This is the strongest "just use the slicer" option for the CI leg (not the browser Lab leg).
- https://grid.space/kiri/ and https://github.com/GridSpace/grid-apps/wiki/Kiri:Moto — Kiri:Moto is an actively maintained, open-source slicer written in JS that runs entirely in browser workers. It directly refutes any claim that in-browser slicing is infeasible; it does not refute the error-vocabulary argument (it reports nothing like "strut from void 12 starts unsupported at z=41.2 mm").
- https://github.com/Cloud-CNC/cura-wasm — verified via GitHub API: **archived**, last push 2021-08-13. The obvious "CuraEngine in the Lab worker" path is unmaintained — this *supports* the doc's ownership bet for the browser context.
- https://trimesh.org/trimesh.base.html — `section_multiplane(plane_origin, plane_normal, heights)` returns closed 2D sections per plane; multiplane mesh slicing is a commodity primitive (Python, so not directly usable by bikar, but it shows step 1 is not novel IP).
- Key asymmetry found in primary sources: slicers **silently drop** sub-threshold features rather than erroring. PrusaSlicer's `min_feature_size` tooltip (PrintConfig.cpp, fetched): "Model features that are thinner than this value will **not be printed**" — no warning, no report. A slicer dry-run therefore does NOT surface F5-class defects without G-code diffing; this is the doc's best concrete justification for owning geometric checks, and it currently doesn't make this argument.

### Bet 2: 45° overhang threshold

- PrusaSlicer source (fetched, `src/libslic3r/PrintConfig.cpp`): `support_material_threshold` default = **0**, tooltip: "Set to zero for automatic detection (recommended)." And `src/libslic3r/Support/SupportMaterial.cpp` (fetched): when auto, the per-layer offset is **`0.5f * fw`** — "Overhang defined by half the extrusion width" — i.e., the flagship slicer's recommended detection is *not an angle at all*; it is a per-layer horizontal step of w/2, which makes the effective self-supporting angle a function of layer height (atan((w/2)/h): ~48° at h=0.2/w=0.45, ~66° at h=0.1).
- Cura `resources/definitions/fdmprinter.def.json` (fetched): `support_angle` default **50°** measured from vertical ("At a value of 0° all overhangs are supported, 90° will not provide any support") — tolerates more than 45°.
- BambuStudio source (fetched, `src/libslic3r/PrintConfig.cpp`): `support_threshold_angle` default **30°**, "Support will be generated for overhangs whose slope angle is *below* the threshold" — measured from horizontal, i.e., Bambu by default tolerates overhangs up to 60° from vertical.
- https://www.padtinc.com/2017/07/12/towards-self-supporting-design-for-additive-manufacturing-part-1-standard-guidelines/ — (unverified snippet, but explicit) stair-step model gives overhang step l = t/tan(θ); Stratasys/ULTEM data shows the max self-supported angle "is indeed a function of layer thickness, but also a function of the contour width."
- https://www.tandfonline.com/doi/full/10.1080/0951192X.2018.1466398 — Jiang, Xu, Stringer (Int. J. Computer Integrated Manufacturing 31(10), 2018): printable threshold overhang angle in extrusion AM varies with cooling fan speed, print speed, and temperature (snippet-verified; paywalled).
- Community capability sources (snippet-level, consistent): https://www.3dsourced.com/rigid-ink/how-to-print-overhangs-bridges-exeeding-the-45-degree-rule/ , https://www.wevolver.com/article/3d-print-overhang — tuned printers do 60–70° clean.
- Also: PrusaSlicer measures the angle from *horizontal* and offsets by `h / tan(θ)`; the doc's `h·tanθ` matches Cura's from-vertical convention. At 45° they coincide — which will hide a convention bug until someone changes the default. The doc never states its convention.

### Bet 3: F5 sub-extrusion neck erode (0.21 mm, error severity)

- PrusaSlicer `PrintConfig.cpp` (fetched): Arachne `min_feature_size` default = **25% of nozzle** (0.1 mm on 0.4), features above it are widened to `min_bead_width` default **85% of nozzle** (0.34 mm). Cura `fdmprinter.def.json` (fetched): `min_feature_size` 0.1 mm, `min_wall_line_width` = 0.85 × nozzle. Arachne has been the *default* engine since PrusaSlicer 2.5 and Cura 5.0 (https://help.prusa3d.com/article/arachne-perimeter-generator_352769, fetched).
- Consequence: erode-by-0.21-vanishes flags every region with min width < 0.42 mm as an **error**, but both mainstream engines will actually print features from ~0.1 mm up (thinned/widened beads). The doc's floor is 4× the modern printable floor. As an error it will reject printable geometry; the correct error floor is the "feature will not be printed at all" line (~0.1 mm, i.e., erode radius ~0.05 mm), with 0.1–0.42 mm a warning band.
- Counter-counter: sub-width single beads are weak, and bikar's mesh gate already imposes a 1.2 mm strut floor, so a 0.42 mm layer-level *warning* is coherent with bikar's intent — but the severity label "error (layer-resolved strut floor)" is the contested part.

### Bet 4: F6 bridge threshold 10 mm

- BambuStudio `PrintConfig.cpp` (fetched): `max_bridge_length` default **10.0 mm** ("Max length of bridges that don't need support") — the doc's exact number is a shipped slicer default, so it is grounded, just uncredited.
- Capability counter-evidence: https://www.thingiverse.com/thing:4833153 (standard test spans 10–100 mm), https://www.printables.com/model/193838-extreme-bridging-test-pieces-50-mm-350-mm , https://all3dp.com/2/bridging-3d-printing-tips-tricks-for-perfect-bridges/ (unverified snippets) — well-tuned FDM commonly bridges 20–80 mm. Since F6 is warn-only, conservative is acceptable but will be noisy on lattice orbs.
- Formulation gap: https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/BridgeDetector.hpp (fetched) — real bridge feasibility depends on *direction*; PrusaSlicer searches the bridging angle over the region against `lower_slices` and extracts `unsupported_edges`. "Max span between anchored ends" without a direction search can both over-estimate (region anchored on all sides: shortest-direction lines are what print) and under-estimate.

### Bet 5: Support-map algorithm choice

- https://github.com/Ultimaker/CuraEngine/wiki/Generating-Areas (fetched): CuraEngine computes overhang as the layer minus the lower layer offset by **`tan(a) × layer_height`**, then propagates support areas downward — the doc's formula is the industry-standard formulation, not an invention. GROUNDED; cite it.
- Divergence from the standard worth noting: CuraEngine works **top-down** (propagating support volumes to the bed); the doc tracks islands **bottom-up** with forward overlap. Equivalent for detection, but the doc's "main body = component containing the largest bed-contact region" is a bespoke heuristic with edge cases (multiple bed patches; island merging into another island before either joins the main body).

### Bet 6: One new 2D dependency / performance

- Manifold WASM bindings (`bindings/wasm/manifold-encapsulated-types.d.ts`, fetched): `Manifold.slice(height): CrossSection`, `Manifold.project()`, `CrossSection.offset(delta, joinType, miterLimit, circularSegments)` — manifold-3d bundles Clipper2-backed 2D booleans/offsets AND mesh slicing. The composition survey (§4) already calls manifold-3d the healthiest dependency; the "one new Clipper2-class dependency decision" may actually be a zero-new-dependency decision, and step 1's hand-rolled segment chaining has an off-the-shelf alternative inside the same package. https://manifoldcad.org/docs/html/classmanifold_1_1_cross_section.html
- https://www.inf.ufpr.br/murilo/public/CAD-slicing.pdf (fetched, experiments section): trivial slicing ≈ 200–250 M triangle–plane pairs/s; their optimal incremental algorithm 8–11 M items/s; Slic3r's slicing step 6–8 M items/s (C++). StarOrb = 5,040 × 600 ≈ 3 M pairs → milliseconds; 45k × 600 = 27 M pairs → sub-second even naively, with headroom for JS overhead. The doc's "trivial cost" claim is sound — but note the unexamined cost is the ~600 × (dilate + diff + erode) Clipper passes, not slicing.

## Misgrounded or missing citations

1. **"Deliberately uncited" thresholds are actually citable from primary sources, and two of them disagree with the doc.** Appendix A frames 45°/10 mm/0.21 mm as folklore awaiting print calibration. The 10 mm bridge is Bambu Studio's shipped `max_bridge_length` default; the 45° default contradicts all three flagship slicers' shipped defaults (Prusa auto/half-width, Cura 50°, Bambu 30°-from-horizontal); the 0.21 mm erode contradicts shipped Arachne `min_feature_size` = 0.1 mm as an *error* floor. "Uncited" reads as neutral but here it conceals that the chosen defaults sit off-distribution.
2. **Angle convention unstated** in §3 step 2 (`h·tanθ` implies θ from vertical; Prusa measures from horizontal and divides). One line fixes a latent porting bug.
3. **§3 "trivial cost" has no benchmark citation** — Minetto et al. 2017 (CAD 92) supports it directly and should be in Appendix A.
4. **"0.21 mm for a 0.4 mm nozzle"** assumes a 0.42 mm extrusion width that is neither Cura's default (0.40) nor PrusaSlicer's (0.45); state the assumed width or derive from a `--nozzle`/width flag.
5. **Appendix A's "±0.1–0.2 mm printed accuracy"** is a paraphrase of tile-survey §7, which actually says holes print 0.1–0.3 mm undersize and external dims ~0.1 mm oversize — directionally consistent, but quote it as stated (the asymmetry hole-vs-external matters for neck widths).
6. **The Clipper2 §5 citation checks out** (int64 coordinates, post-simplify, offset-deletes-thin-features pitfall) — and §5's pitfall (2) ("inset by more than half the local feature width deletes geometry silently") is exactly the mechanism F5 exploits; the doc could cite its own research file for that trick.

## Recommended doc changes

### 1. §1/§6 — divergence justification for the "no slicer" bet (paste-ready)

> **Why not just run a slicer?** PrusaSlicer slices headless (`prusa-slicer --export-gcode`, [CLI wiki](https://github.com/prusa3d/PrusaSlicer/wiki/Command-Line-Interface)) and Kiri:Moto ([grid.space/kiri](https://grid.space/kiri/)) proves full slicing runs in browser workers; the geometry here is commodity (trimesh ships `section_multiplane`). We still own the gate for three reasons: (a) the only CuraEngine-in-WASM port ([cura-wasm](https://github.com/Cloud-CNC/cura-wasm)) is archived since 2021, and embedding Kiri:Moto means adopting a whole slicer app to extract warnings it doesn't emit; (b) slicers *silently drop* features below `min_feature_size` — PrusaSlicer's own tooltip says thin features "will not be printed" — so a dry-run reports nothing for exactly the defects F2/F5 must catch; (c) our errors must speak bikar's vocabulary ("strut from void 12 starts unsupported at z=41.2 mm"). **Mitigation:** CI additionally runs a PrusaSlicer CLI dry-run on gallery presets as an oracle, so gate false-negatives/positives surface as disagreement diffs.

### 2. §3 step 2 — replace the fixed 45° default with the slicer-standard auto rule; state the convention

> θ_max is measured **from vertical** (Cura convention; the per-layer dilation is `h·tan θ`). Default is **auto**: dilation = half the extrusion width per layer — the detection PrusaSlicer ships and recommends (`support_material_threshold = 0` → "Overhang defined by half the extrusion width", [SupportMaterial.cpp](https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/Support/SupportMaterial.cpp)) — which correctly makes the effective angle a function of layer height (≈48° at 0.2 mm/0.45 mm, ≈66° at 0.1 mm). `--overhang <deg>` pins an explicit angle instead. Note the shipped-default spread we diverge from if a fixed angle is used: Cura 50° from vertical, Bambu Studio 30° from horizontal (= tolerates 60°), and the literature (Jiang et al. 2018, [IJCIM 31(10)](https://www.tandfonline.com/doi/full/10.1080/0951192X.2018.1466398)) finds the threshold moves with cooling, speed, and temperature — a fixed 45° over-warns relative to every mainstream default, acceptable only because F4 is warn-severity.

### 3. §3 step 4 — split F5 into error + warn tiers (design change, flagged)

The current F5 (erode 0.21 mm, vanish → **error**) will reject geometry that shipping slicers print. Recommended replacement:

> **Neck scan (two tiers).** Erode by `min_feature_floor` (default 0.05 mm ≈ half of Arachne's `min_feature_size`, 25% of nozzle — features below this are *silently not printed* by PrusaSlicer/Cura): vanish → **error**. Erode by extrusion half-width (0.20–0.225 mm depending on line width): vanish → **warn** "single-bead feature — printable via Arachne variable-width beads but far below the 1.2 mm strut floor". Rationale: since PrusaSlicer 2.5 / Cura 5.0, Arachne prints features from 0.1 mm up by thinning beads to `min_bead_width` (85% of nozzle), so sub-extrusion-width is degraded, not unprintable ([Arachne KB](https://help.prusa3d.com/article/arachne-perimeter-generator_352769)).

### 4. §3 step 5 — credit the 10 mm source; note direction-dependence

> `bridge_max` default 10 mm — Bambu Studio's shipped `max_bridge_length` default ([PrintConfig.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)); deliberately conservative versus community capability (tuned printers routinely bridge 20–80 mm; standard test pieces run 10–100 mm+), acceptable because F6 is warn-only. Span is measured along the *best* bridging direction (shortest anchored lines), not the patch's max chord — bridge feasibility is direction-dependent, per PrusaSlicer's `BridgeDetector`, which brute-force searches the bridging angle.

### 5. §3 / Appendix A — dependency framing correction

> Note: manifold-3d already bundles Clipper2-backed 2D ops (`CrossSection`: booleans, `offset`, simplify) plus `Manifold.slice(height)` and `project()` ([docs](https://manifoldcad.org/docs/html/classmanifold_1_1_cross_section.html)). If composition C1 adopts manifold-3d, this gate's 2D engine and even the slicing core may be zero *new* dependencies; the hand-rolled slicer (Open Question 1) should be spiked against `Manifold.slice` per layer before we commit to owning segment chaining.

### 6. Appendix A — new sources to add

- CuraEngine support-area algorithm (grounds §3 step 2): https://github.com/Ultimaker/CuraEngine/wiki/Generating-Areas
- PrusaSlicer defaults + auto-overhang + Arachne floors (grounds/moves F4, F5): https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/PrintConfig.cpp , https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/Support/SupportMaterial.cpp , https://help.prusa3d.com/article/arachne-perimeter-generator_352769
- Bambu Studio defaults (grounds F6's 10 mm; contests 45°): https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp
- Cura defaults: https://github.com/Ultimaker/Cura/blob/main/resources/definitions/fdmprinter.def.json
- Slicing performance (grounds §3 "trivial cost"): Minetto et al., "An optimal algorithm for 3D triangle mesh slicing", Computer-Aided Design 92 (2017) — https://www.inf.ufpr.br/murilo/public/CAD-slicing.pdf
- Orientation/bed-contact prior art (grounds F7): Tweaker — https://github.com/ChristophSchranz/Tweaker-3 , https://zenodo.org/records/5569145
- Overhang threshold is parameter-dependent (contests fixed 45°): Jiang et al. 2018 — https://www.tandfonline.com/doi/full/10.1080/0951192X.2018.1466398 ; PADT self-supporting guidelines — https://www.padtinc.com/2017/07/12/towards-self-supporting-design-for-additive-manufacturing-part-1-standard-guidelines/

### 7. Minor fixes

- §2 F1: add "two components sharing a single welded vertex pass union-find but are not structurally joined; the neck scan (F5) is the backstop — a point contact erodes to nothing on its shared layer."
- §3 step 1: cite Minetto for "trivial cost", and add one sentence acknowledging the per-layer Clipper passes (600 × dilate/diff/erode), not slicing, as the actual cost center to benchmark in the V1 spike.
- Appendix A: change "±0.1–0.2 mm printed accuracy" to match §7's actual finding ("holes print 0.1–0.3 mm undersize, external dims ~0.1 mm oversize") — the asymmetry is relevant to necks bounded by holes.
