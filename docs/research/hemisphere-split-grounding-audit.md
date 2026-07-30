# Adversarial grounding audit — `hemisphere-split-design.md`

Produced by an adversarial audit agent on 2026-07-30 against the design doc and its survey, with
every code claim re-read from bikar `origin/main` and every number re-measured against the shipped
engine. Preserved verbatim below per
[`ground-design-doc`](../../.claude/skills/ground-design-doc/SKILL.md) §2 (research is checked in,
not summarised away).

**Independent re-verification (author, 2026-07-30).** Because the audit's findings rewrote most of
the design doc's numbers, every load-bearing measurement was re-run independently in a clean
`git worktree` of `origin/main` (so the parallel session's `dsl/` changes could not perturb the
mesh). All of the following reproduced **exactly**:

- `F2` — max layer 650.4 mm² at z = −49.90 (1 region), not the equator.
- `F5` — first layer is **1** region of 7.86 mm², matching the real print-gate run's `bed=7.9mm²`,
  which validates the measurement method against the shipped gate.
- `F3`/`F4` — cut cross-sections: `vertex-5` 898.2 mm² / k=1 / b=2; `face-3` 175.5 mm² / k=12 /
  b=12; `edge-2` 491.1 mm² / k=16 / b=16.
- `F1` — the corrected Euler form `χ(orig) + 2(2k − b)` gives −396 / −372 / −364 respectively.
- `F8` — whole-orb bed contact by resting axis: `vertex-5` 3.90 mm², `face-3` **30.17 mm²
  (5.02 %, no F7)**, `edge-2` 7.86 mm².
- `F9` — 1034 vertices above / 1034 below / 56 on the authored z = 0 plane.
- `F10` — vertices lying exactly on each plane: 60 / 12 / 56.

**One refinement to the audit's own text.** Finding F4 states the `vertex-5` annulus is "stable over
z ∈ [−1.8, +1.8] before it breaks into 30 regions at z = 2.0". Measured more finely, it is
continuous (1 region, 1 hole) through **|z| ≤ 1.75 mm**, is already 10 regions at |z| = 1.8, and is
30 regions at 2.0. The usable placement tolerance is therefore **±1.75 mm**, not ±1.8. Separately,
the "99.3 % solid" figure uses the outer/inner *maximum* radii (π(61.2² − 58.8²) = 904.8 mm²); by
*mean* radii (60.9–61.2 outer, 58.5–58.8 inner) a full annulus is 898.9 mm² against 898.2 measured,
i.e. gapless to 0.1 %. Either convention supports the finding; the doc states the measured
region/hole counts, which are convention-free.

---

# Adversarial grounding audit — `docs/hemisphere-split-design.md`

Method: every code claim re-read from `bikar` `origin/main` (`git show origin/main:<path>`); every number re-measured against the shipped engine at `origin/main` (working tree verified byte-identical for `kernel3d/`, `cli/src/`, `patterns/Orbs/Star-Orb.bkr`). Temp probes were run under `/Users/omareid/Workspace/git/bikar/.tmp-audit` and deleted; nothing in bikar was modified.

---

## 1. Verdict table

| # | Claim (doc §:line) | Verdict |
|---|---|---|
| 1 | §1.1 `2R ≤ min(X,Y,Z) − 10` is the shipped ceiling formula | **GROUNDED** — but cited to prose, not to code |
| 2 | §1.1:54-61 build-volume table arithmetic | **GROUNDED** (all six rows correct) |
| 3 | §1.1:63 "Every shipped preset has Z ≥ min(X,Y)… gain exactly zero on all six" | **WEAK** — nine presets ship, not six; and the Lab's **Custom** entry breaks the universal reading |
| 4 | §1.1:44 "Both clauses are true" | **WRONG** — relaxing Z helps *short*-Z machines; "for tall-bed machines" is incoherent, not merely useless |
| 5 | §3.5:230 "the widest layer *is* the equator" | **WRONG** — widest layer is at z = ±49.9 mm; equator is 75.5 % of it |
| 6 | §3.5:230 "~83× gain", "ratio 1.21 % → 100 %" | **WRONG** — 62.5× / 75.5 % on the measured plane; **5.8× / 29.2 %** on the plane §4 actually recommends |
| 7 | §3.5:231 "supports: ~neutral" | **conclusion GROUNDED, reasoning UNGROUNDED (ARGUED)** — right answer, non-sequitur evidence |
| 8 | §3.5:236-238 `euler=−396` ⇒ χ=4−2n ⇒ n=200 | **GROUNDED** — 10 voids × 20 faces = 200, confirmed three ways |
| 9 | §3.3 "pin-in-strut is geometrically infeasible", 3 − 2(0.9) = 1.2 mm | **WRONG ARITHMETIC, RIGHT CONCLUSION** — the binding dimension is the 2.4 mm *depth*, giving **0.6 mm**; and the claim is false at the top of the shipped `strut_width`/`strut_depth` ranges |
| 10 | §3.2 "a cell-following seam is fatal because it can't rest flat" | **WEAK / OVERCLAIMED** — the survey (§8 item 4) explicitly leaves it open; §9.1 hardens it to "ruled out" |
| 11 | §5.1 "capping makes both halves watertight; gate passes unchanged" | **WEAK** — `volume > 0` fine; the degenerate-triangle risk is real and dismissed (56–60 mesh vertices sit *exactly* on the symmetry planes) |
| 12 | §5.3 χ(top)+χ(bottom) = χ(original) | **WRONG** — off by `2·χ(cap)`. Correct: **χ(top)+χ(bottom) = χ(orig) + 2(2k − b)** |
| 13 | §8 validator 4 "Euler additivity — hard error, not a warning" | **WRONG** — as written it would reject every *correct* split on two of the three symmetry planes |
| 14 | §4:263 "the print gate reports 20 first-layer regions" | **WRONG** — misreading of `islands=0/20` (orphan/supported islands). First layer has **1** region |
| 15 | §4:264 "~144 mm² of total butt area" | **WRONG** — 491 mm² (edge-2), 175 mm² (face-3), 898 mm² (vertex-5) |
| 16 | §3.4:202 / §3.1:143 "butt faces of 7.2 mm² each", "dozens of ~7 mm² disjoint islands" | **WRONG** — mean cut face is 30.7 mm² (edge-2) / 14.6 mm² (face-3); 16 or 12 islands, not "dozens" |
| 17 | §4 `face-N` default | **UNGROUNDED (ARGUED) and self-defeating** — its own rationale predicts the worst plane on every metric the doc values |
| 18 | §2 engine-ground-truth citations (mesh, gate, exemption, `--format parts`) | **GROUNDED** — spot-checked ~20 `path:line` refs, all correct except two below |
| 19 | `docs/language-reference.md:838` (one instance per piece) | **WRONG CITATION** — the text is at `:840` |
| 20 | `evaluator.ts:2483` (`concatMeshes`) | **WRONG CITATION** — `concatMeshes` is at `:2485` |
| 21 | §5.1 "Every step but the last two already exists" | **WRONG** — `crossingPoint`/`triangleCut`/`chainLoops`/`nestLoops`/`orient` are all **module-private** on origin/main |
| 22 | Status line `research/hemisphere-split-grounding-audit.md` | **WRONG** — file does not exist; and Appendix B says the audit is "pending". Direct self-contradiction + dead link |
| 23 | §9 recommendation (Option C) | **HOLDS, but under-argued** — the doc misses a cheaper option that dominates C on its own scorecard (see finding 8) |

---

## 2. Findings

### F1 — §5.3's Euler invariant is wrong, and §8 builds a hard error on it

**Evidence.** Inclusion–exclusion on the *capped* halves: A = S⁺ ∪ C, B = S⁻ ∪ C, so A ∩ B = **the cap C itself**, not the rim circles. The survey's derivation (`hemisphere-split-survey.md:708-711`) is correct *for uncapped halves* (A ∩ B = b circles, χ = 0). §5.1 changed the design to cap; §5.3 carried the uncapped invariant over unchanged.

Correct form:
```
χ(A) + χ(B) = χ(A∪B) + χ(A∩B) = [χ(S) + χ(C) − 0] + χ(C) = χ(orig) + 2·χ(C)
χ(C) = 2k − b   (k = cap components, b = total cap boundary loops)
```
Sanity check: cut a sphere (χ=2) at the equator → two closed spheres, sum 4. Doc's formula predicts 2. Corrected: 2 + 2(2·1−1) = 4 ✓. Torus (χ=0) cut into two capped spheres, sum 4; corrected: 0 + 2(2·2−2) = 4 ✓.

Measured for Star-Orb (χ = −396):

| plane | cap k | cap b | χ(cap) | correct χ(top)+χ(bot) | doc predicts |
|---|---|---|---|---|---|
| `vertex-5` | 1 | 2 | 0 | **−396** | −396 ✓ (by luck) |
| `face-3` | 12 | 12 | 12 | **−372** | −396 ✗ |
| `edge-2` (authored z) | 16 | 16 | 16 | **−364** | −396 ✗ |

**Recommended change.** Replace §5.3's blockquote with `χ(top) + χ(bottom) − 2(2k − b) = χ(original)`, note that `k` and `b` fall straight out of `nestLoops`/`chainLoops` so the test stays cheap and exact, and note the special case where the doc's naive form happens to hold (annular cap, χ = 0). Rewrite §8 validator 4 accordingly — as written it is a fail-closed gate that rejects correct output, which is the exact inverse of Tenet 29.

### F2 — §3.5's "the widest layer *is* the equator" is false; the 83× and 100 % numbers are wrong

**Evidence.** For a spherical *shell*, every horizontal slice has the same annular area π(R₀²−Rᵢ²) = 904.8 mm² for |z| < Rᵢ — the equator has no geometric privilege at all. Measured slice-area profile of the shipped Star-Orb mesh (0.2 mm layers, authored orientation):

```
MAX layer area  = 650.4 mm²  at  z = −49.9  (1 region)
layer at z≈0    = 494.3 mm²  (16 regions);  sliceAt(0) = 491.1 mm², 16 regions
```

So the widest layer sits **50 mm from the equator**, at the polar pentagon ring. The correct comparison for a split half's first layer is 491.1 mm², not 650.4:

| doc says | actually |
|---|---|
| ~83× bed contact | **62.5×** (491.1 / 7.86) — on the authored/`edge-2` plane |
| ratio 1.21 % → 100 % | **1.21 % → 75.5 %** |

**Recommended change.** Delete "(the widest layer *is* the equator, which becomes each half's first layer)" — it is a false lemma. State the measured pair per plane, and note that F7's ratio test compares against the *global* max layer, which is a polar ring, not the cut face.

### F3 — The whole §3.5 measurement is on a plane the design does not propose

**Evidence.** bikar's `icosahedron()` (`polyhedra.ts:122-160`) puts vertices 4 = (0,−1,t) and 5 = (0,1,t) at maximum z; they share an edge (faces `[4,9,5]`, `[5,11,4]`), so the **authored +z axis is an edge-2 axis**. I confirmed this numerically: rotating the mesh so `symmetryViewAxes(icosahedron())[2]` (`edge-2`) → +z reproduces the authored numbers exactly (bed 7.86, max 650.4, 16 regions, identical six F3 z-values).

§4 recommends `face-N` (= `face-3` for an icosahedron). Measured on the three symmetry planes:

| plane | cut cross-section at z=0 | regions | mean face | whole-orb bed contact (pole-down) | first-layer gain |
|---|---|---|---|---|---|
| `vertex-5` | **898.2 mm²**, **one annulus** (1 outer + 1 hole) | 1 | — | 3.90 mm² | **230×** |
| `face-3` (§4's default) | **175.5 mm²** | 12 | 14.6 mm² | 30.17 mm² | **5.8×** |
| `edge-2` (measured in §3.5) | 491.1 mm² | 16 | 30.7 mm² | 7.86 mm² | 62.5× |

**Recommended change.** §3.5 must name the plane it measured. §4's default must change or its rationale must be rewritten — see F4.

### F4 — §4's `face-N` rationale is self-defeating, and `vertex-N` is the plane the doc was looking for

**Evidence.** §4:255-256 argues `face-N` is best "because a face-centred plane is most likely to pass between pattern cells rather than clipping a star's tips". That prediction is **correct** — and it is exactly what makes `face-3` the worst plane for both surviving arguments in the doc: it severs the fewest and smallest struts, so it has the *least* cap area (175.5 mm², a 5.8× bed gain, 29.2 % of the widest layer) and the *least* glue area. The doc optimises for seam invisibility in §4 while claiming bed contact and bond area as the benefits in §3.5 and §3.4, and never notices the two point opposite ways.

Meanwhile the `vertex-5` plane cuts a **continuous solid annulus** — verified stable over z ∈ [−1.8, +1.8] before it breaks into 30 regions at z = 2.0:
```
z=0.0: 1 region, 1 hole, area 898.2  (outer r 60.9–61.2, hole r 58.5–58.8)
z=1.5: 1 region, 1 hole, area 900.3
z=2.0: 30 regions, area 350.7
full shell annulus π(61.2²−58.8²) = 904.8 → the vertex-5 equator is 99.3 % solid
```
This single fact demolishes three separate paragraphs:
- §3.4:202 "a ring of butt faces of 3 × 2.4 = 7.2 mm² each — the worst geometry in Loctite's taxonomy" → on `vertex-5` it is one continuous ~377 mm × 2.4 mm lap band of 898 mm², which is precisely Loctite's "increase the joint **width**" case, *the best* geometry in that taxonomy.
- §3.1:143 "a cross-section made of dozens of ~7 mm² disjoint islands" fighting the slicer's `is_conflict_for_connector` guard → on `vertex-5` there are no islands to fight.
- §9.1:418-419 "an inner+outer brim because the first layer is ~20 disjoint islands, not a continuous outline" → on `vertex-5` the first layer *is* a continuous outline.

At 898 mm² and Shen et al.'s 2.46 MPa CA figure, the seam carries ~2.2 kN in pure tension against an orb that weighs ~57 g. The doc's §9.2 P3-Q2 ("§3.4 predicts a seam at ~5 % of printed PLA strength, so this is the most likely failure") states a *relative* number and never computes the *absolute* adequacy, which is what decides whether it survives handling.

**Recommended change.** Flip §4's default to `vertex-N`, or state honestly that the plane choice trades seam invisibility against seam strength/adhesion and that `face-N` optimises the former at the cost of both benefits §3.5 claims. Fix §3.4, §3.1 and §9.1's island/butt-face descriptions to be plane-conditional. Also fix §9.2 P3-Q4 and the P3 catalog entry, which says "cut at the equator **in the slicer**" — the STL's equator is the `edge-2` plane, so P3 as written will not test §4's proposal.

### F5 — §4:263 misreads the CLI output; the "20 severed struts" number is invented

**Evidence.** `cli/src/index.ts:281-286` prints `islands=${report.orphanIslands}/${report.supportedIslands}`. So `islands=0/20` means *zero orphan islands and twenty supported islands*, not "20 first-layer regions". There is no first-layer region count in the report at all. Measured: the first layer (z = −61.1) has **1** region of 7.86 mm². The cut cross-section has 16 (edge-2), 12 (face-3) or 1 (vertex-5) regions. Every downstream number built on "~20" is wrong: §4:264 "~144 mm² of total butt area" (actual 491 / 175 / 898), §3.1:143 "dozens of ~7 mm² disjoint islands", §9.1:418, §9.2:429.

**Recommended change.** Replace "the print gate reports 20 first-layer regions" with the measured cross-section counts per plane, and add a footnote that `islands=a/b` is orphan/supported island counts.

### F6 — §3.3/§6's 1.2 mm is arithmetic on the wrong dimension; the conclusion is stronger than the doc says, and its generality is false

**Evidence.** The butt face of a severed strut is width × depth = 3 × 2.4 mm (the doc's own §3.4:202). A socket drilled into that face is bounded by the **smaller** dimension. Applying Hydra's 0.9 mm wall per side to the 2.4 mm shell depth gives **2.4 − 2(0.9) = 0.6 mm**, not 1.2 mm. The 0.9 mm-per-side reading is correct (a hole leaves a wall on each side); the doc just picked the non-binding dimension.

Generality is the bigger problem. `strut_width` and `strut_depth` are *parameters*, not constants (`patterns/Orbs/Star-Orb.bkr:11-12`): `range 1.5..6` and `range 1.2..4`. And they are absolute millimetres, not radius-scaled — `solidifyLattice` converts strut width into pattern space via `unitMm` (`solidify-lattice.ts:208-209`) precisely so the printed strut is the authored mm at any radius. So at the top of the shipped ranges (`width 6 depth 4`) the max socket is 4 − 1.8 = **2.2 mm**, which clears Hydra's ">2 mm" floor. §3.3's heading "Pin-in-strut registration is **geometrically infeasible**" and §6:310's "A socket in a 3 mm strut can be at most 1.2 mm ⌀" are unqualified statements that are false over part of the shipped parameter space.

**Recommended change.** Restate as: "at the default 3 × 2.4 mm strut, the socket ceiling is min(3, 2.4) − 2(0.9) = **0.6 mm**, a quarter of Hydra's 2 mm minimum printable hole. It stays sub-2 mm until `struts depth` reaches 3.8 mm, i.e. only in the top ~5 % of the shipped 1.2–4 mm range, where the shell is no longer a lattice in any visual sense." That is both correct and a much harder claim than the one currently written.

### F7 — §1.1's "zero gain" is a fact about presets, not about the Lab; and its supporting sentence is incoherent

**Evidence — the formula.** The shipped ceiling is `packages/knobs/src/machines.ts:91-93`:
```ts
export function radiusCeilingMm(target: PrintTarget): number {
  return Math.floor((Math.min(target.xMm, target.yMm, target.zMm) - BUILD_MARGIN_MM) / 2);
}
```
with `BUILD_MARGIN_MM = 10` (`:84`). Equivalent to the doc's `2R ≤ min(X,Y,Z) − 10` modulo an integer floor. **GROUNDED — but the doc cites only `orb-lab-design.md` prose.** That is the failure mode this skill exists to prevent; cite the code.

**Evidence — the table.** `machines.ts:21-81` dimensions every preset. All six rows arithmetically check out. Two nits: the shipped label is **"Prusa MK4S"**, not "Prusa MK4"; and nine presets ship, not six — `sls-service` (300³) and `mjf-service` (380×284×380) are omitted. Both also gain zero, so the conclusion survives, but "all six" / "every shipped preset" should say nine.

**Evidence — the hole.** `machines.ts:80` ships `{ id: 'custom', … }`, and `packages/lab/src/main.ts:710-716` reads user-typed X/Y/Z accepting **any value ≥ 50 mm**. A user entering 300 × 300 × 60 gets: whole-sphere ceiling floor((60−10)/2) = **25 mm** (below the `radius` param's own 40 mm floor — the orb is unbuildable), split ceiling min(145, 50) = **50 mm**. That is not a hypothetical belt printer; it is a supported input on the shipped picker, and `orb-lab-design.md:180` and `:341` — the very lines the doc cites — both name the Custom entry. The doc's §1.1:64-65 ("It turns positive only on a short-Z machine … and none is in the table") is true of the table and silent about the entry that makes the table not exhaustive.

**Evidence — the logic.** §1.1:44 says of `orb-lab-design.md:344` ("would relax the Z term for tall-bed machines"): "Both clauses are true." The second clause is not true in any reading. Relaxing the Z term can only help a machine whose Z is *binding*, i.e. a **short**-Z machine. Saying it helps tall-bed machines is not a useless truth, it is a mis-statement — which strengthens Q1's case for correcting `:344`.

**Recommended change.** Cite `machines.ts:84,91-93` for the formula and `machines.ts:21-81` for the volumes; fix "MK4" → "MK4S"; say "all nine presets"; add one sentence acknowledging the Custom entry and that the split's ceiling gain is real but reachable only there; and change "Both clauses are true" to "the first clause is true; the second is backwards — relaxing Z can only help a *short*-Z machine".

### F8 — The doc misses the option that dominates its own recommendation: just rotate the orb

**Evidence.** Running the shipped `printGate` on the same mesh in each of the three symmetry orientations, no split, no engine work:

```
resting on vertex-5 pole : bed= 3.90 mm²  max=900.6  →  3 F3 warns + F7 warn
resting on face-3  pole : bed=30.17 mm²  max=600.8  →  4 F3 warns, NO F7 AT ALL
resting on edge-2  pole : bed= 7.86 mm²  max=650.4  →  6 F3 warns + F7 warn   ← the authored/shipped orientation
```
`checkBedContact` (`print-gate.ts:429-457`) emits nothing when `bedContact ≥ 25 mm² && ratio ≥ 1 %`. On `face-3`, 30.17 ≥ 25 and 30.17/600.8 = 5.0 % ≥ 1 %. **Rotating the whole orb onto a face axis clears F7 outright and drops F3 warnings from 6 to 4 — one click in any slicer, zero engine work, zero split, one file.**

This is a strictly cheaper option than C for the doc's one surviving benefit, and it does not appear in §9.1's option table at all. It also undercuts §3.5's framing: the doc treats the 7.86 mm² first layer as a property of "the orb", when it is a property of *the authored orientation*.

Two honest caveats to state alongside it: the 25 mm² floor is `CAL-BED-01`, whose own basis text (`print-gate.ts:47-55`) reads "**no primary source at all** … That is why F7 is warn-only: the gate is deliberately unable to fail a part on a number it has not earned"; and F7 is a *warn*, so the whole orb already reports `PASS` today (the doc's own §3.5 output block says so). "Clears the F7 floor" is therefore a benefit measured against an unearned threshold, and the doc should say so.

**Recommended change.** Add a row **A0 — reorient the whole orb onto a face axis** to §9.1's table, with its measured numbers, and re-derive the recommendation from a four-option comparison. Add the CAL-BED-01 caveat wherever §3.5 and §9.1 lean on "clears F7's 25 mm² floor".

### F9 — "supports: neutral" is the right answer reached by an invalid argument

**Evidence.** §3.5:231 justifies "neutral" with the survey's derivation that "the top **29.3 %** of a hemisphere's surface … sits below the 45° threshold either way". That is an **overhang-angle** statistic. The six F3 findings it is being used to explain are **island** findings — regions born mid-air with no overlap below (`print-gate.ts:347-395`). F4 (overhang) is not implemented at all (`print-gate.ts:24-33`; `PrintFindingCode = 'F1'|'F2'|'F3'|'F7'`). The cited evidence measures a quantity the cited gate does not compute. Category error.

The correct argument, which I verified: the Star-Orb mesh is **mirror-symmetric about the authored z = 0** (1034 vertices above, 1034 below, 56 exactly on the plane; the layer-area profile is symmetric to 0.1 mm² at every sampled height — 650.4/650.4, 457.1/457.1, 372.0/372.0, 364.4/364.4, 320.3/320.3, 467.4/467.4). Therefore the flipped bottom half is *geometrically identical* to the top half. And for the top half printed cut-face-down, every layer at z > 0 is bit-identical to the whole orb's, and its first layer is grounded either way — so its island set is unchanged: `{+8.1 ×4, +13.1 ×4, +41.7 ×2}` = 10 islands, 3 F3 lines. Two halves therefore give 10 + 10 = 20 islands and 3 + 3 = 6 F3 lines, against the whole orb's 20 islands / 6 F3 lines. **Exactly neutral, measured, not guessed.**

**Recommended change.** Replace the 29.3 % justification with the symmetry argument above and its numbers. Keep the 29.3 % figure only where it belongs — as an *overhang* caveat, flagged against `CAL-OVH-01` (already registered), noting F4 is unimplemented so the engine cannot currently see it.

### F10 — §5.1's "the gate passes unchanged" understates a real implementation hazard

**Evidence.** `meshStats` (`solidify-lattice.ts:115-148`) sets `watertight = bad === 0 && volume > 0`. `volume > 0` is trivially fine for a capped half. The exposure is `meshGate`'s second assertion (`mesh-gate.ts:93-95`), degenerate triangles at `DEGENERATE_AREA_MM2 = 1e-6` (`:52`). A symmetry plane through the origin lands on mesh vertices *by construction*:

```
verts with |z| < 1e-9 after rotating each axis to +z:
  vertex-5: 60     face-3: 12     edge-2: 56
```

`slice.ts:133-137`'s tie rule ("a vertex exactly at z counts as not-below") keeps 2D loops closed, but a *triangle-re-emitting* split must additionally not emit zero-area slivers when a crossing point coincides with an existing vertex — and earcut is well known to emit degenerate triangles on near-collinear rings. Between 12 and 60 exact coincidences per plane, this is the likeliest way the split fails its own gate, and §5.1 gives it one clause.

Two smaller points in the same section:
- §5.1:284 "wound outward for one half and inward for the other" is wrong as written — **both** caps must be wound outward with respect to their own solid (else `volume > 0` fails). What is opposite is the winding *relative to the shared rim loop*. A builder implementing the sentence literally produces an inverted half.
- §5.1:285-286 "Every step but the last two already exists". On origin/main, `crossingPoint` (`:128`), `triangleCut` (`:139`), `chainLoops` (`:170`), `nestLoops` (`:221`) and `orient` (`:267`) are **all module-private**; only `sliceAt`, `sliceMesh`, `signedArea`, `ringBounds`, `pointInRing` are exported. §10 Q3's proposed "`kernel3d/split.ts` importing `slice.ts`'s helpers" is not possible without changing `slice.ts`'s export surface — which is a real cost the option table does not price.
- `meshStats` is an **edge**-manifold test only. A cut plane tangent to a strut produces a pinch *vertex*, which `bad === 0` will not catch (`print-gate.ts:141-145` documents the same blind spot for `countComponents`). Worth one sentence, since §5.1's whole thesis is "the existing gate suffices".

**Recommended change.** Add the exact-coincidence count as a measured hazard, fix the winding sentence, correct the "everything exists" claim with the five private helpers, and note the edge-vs-vertex manifold gap.

### F11 — §3.2 overclaims relative to its own survey

**Evidence.** `hemisphere-split-survey.md:788` (§8 item 4) records: "**This may be a fatal objection** to the design's headline idea, **or may be resolvable with a small planar flat at the rim** — no source helps." The design doc's §3.2 heading is "probably fatal", its body asserts "the hemisphere cannot rest cut-face-down … the part is back to point contact plus supports", and §9.1:410 escalates to "is **ruled out** by §3.2". A doc may not upgrade its own survey's explicit open question into a settled ruling without new evidence, and none is offered.

The steelman the doc never engages: a seam with bounded excursions can still plate — only one half's contact surface needs to be planar; a raft absorbs a few millimetres of non-planarity as a matter of routine; and a hybrid "planar rim + cell-following interior" gives up nothing. Note also that on the `vertex-5` plane the planar cut *already* follows a solid great-circle band of the pattern, i.e. the aesthetic goal and the planar constraint are not actually in conflict on this geometry — the doc's central §3.2 tension may be an artifact of measuring the wrong plane.

**Recommended change.** Downgrade §3.2 to "unsettled, and the design proceeds planar because planar is sufficient and cheap", and delete "ruled out" from §9.1. Move the residue to Appendix B as an open question, not a conclusion.

### F12 — Broken self-reference and internal contradiction in the status line

**Evidence.** Line 3-8 claims the doc was "revised after an adversarial grounding audit ([`research/hemisphere-split-grounding-audit.md`]…; counter-evidence and divergences in Appendix B)". `docs/research/` contains only `hemisphere-split-survey.md` — the audit file **does not exist** — and Appendix B (line 524) reads "*(pending the adversarial grounding audit)*". The status line asserts as done exactly what the appendix says is pending, and links to a file that isn't there.

**Recommended change.** Revert the status line to v1/pre-audit wording until the audit report is actually checked in, then restore it.

### F13 — Two wrong `path:line` citations

- `docs/language-reference.md:838` (§6 blocker 3, "one instance per piece") — line 838 is "Both ends unplaced → hard error (order connects outward from the root)."; the quoted text is at **`:840`**. The survey (`:216`) carries the same error; fix both.
- `evaluator.ts:2483` (§6 blocker 4, `concatMeshes`) — `:2483` is `return {`; `orbMesh: concatMeshes(...)` is at **`:2485`**. (The rationale comment at `:2439-2442` is correct.)

Everything else I spot-checked is right: `solidify-lattice.ts:31-35`, `:115-148`, `:224-235`; `mesh-gate.ts:13`, `:25-28`, `:76-80`, `:82`, `:90-92`, `:93-95`, `:96-101`; `slice.ts:128`, `:139`, `:167-170`, `:221`, `:267`; `orb-views.ts:39-48`; `earcut-vendored.ts:67`; `solidify-piece.ts:501`; `fit-profile.ts:27-40`; `ast.ts:140-156`; `print-gate.ts:502-507`; `cli/src/index.ts:204-220`, `:256-263`, `:299-301`, `:313-316`, `:317-321`, `:326`, `:457`, `:459`, `:468-472`, `:475`; `patterns/Coupons/Machine-Card.bkr:34`; `orb-lab-design.md:34`, `:340-341`, `:344`; `catalog.md` P3 ("its verdict … comes from here" — verbatim).

### F14 — Does the recommendation survive? Yes, and it gets stronger — but not for the stated reasons

Option C stands. But every load-bearing number underneath it moved:

- The bed-adhesion benefit is **not** ~83×; it is 5.8× on the plane §4 recommends, 62.5× on the plane §3.5 measured, 230× on the plane nobody proposed.
- The benefit is **not unique to splitting**: a free reorientation onto a face axis clears F7 entirely (F8).
- The glue-area objection (§3.4, §9.2 P3-Q2 "the most likely failure") rests on a 7.2 mm² butt face that does not exist; the real cut faces are 2–125× larger depending on plane, and on `vertex-5` the joint is Loctite's *best* geometry, not its worst.
- The one capability argument the doc discards (§3.2, cell-following seam) was discarded on a question its own survey left open.

So the doc reaches "don't build" through three broken premises and one over-hardened one. The conclusion is right — the engine buys automation and gate-assertability over a slicer that does the geometry interactively — but as written the argument would not survive a careful reader, and §9.2's flip conditions are aimed at the wrong quantities.

**Recommended change.** Rewrite §3.5's scorecard as a per-plane table, add option A0, and re-aim §9.2: P3-Q2 should ask whether the `vertex-N` annular seam holds, not whether 7.2 mm² butt faces do; P3-Q4 should compare `vertex-5` vs `face-3` explicitly and note that the catalog's "cut at the equator in the slicer" is the `edge-2` plane.

---

## 3. UNGROUNDED residue — ARGUED vs EMPIRICAL

`CAL_BET_IDS` on origin/main (`kernel3d/calibration.ts:33-56`) currently registers ten ids: `CAL-FIT-01`, `CAL-HOL-01`, `CAL-FEA-01`, `CAL-BRG-01`, `CAL-OVH-01`, `CAL-WRP-01`, `CAL-BED-01`, `CAL-RIB-01`, `CAL-DET-01`, `CAL-STR-01`.

**ARGUED (stays in the doc — no print needed):**
1. **"Supports: neutral"** (§3.5 row 3) — settled above by symmetry + the existing island analysis. No coupon.
2. **Which symmetry plane** (§10 Q2) — settled above by measurement, not by a print. Q2 should close, not wait on P3-Q4.
3. **Near-pole cell span** (§10 Q4) — the doc already says "the engine can answer this without a print". Correct: it is a software measurement. The *limit* it is compared against is **`CAL-BRG-01`** (already open, coupon MC-3). **Do not mint a new bet.**
4. **Non-planar seam plateability** (§3.2) — argued, unsettled; belongs in Appendix B as an open question with what was checked, not as a ruling.
5. **Degenerate-triangle risk at exact vertex coincidences** (§5.1) — decidable by writing the split and running the existing gate. Not a bet.

**EMPIRICAL (would leave this skill):**
6. **Adhesive butt/lap-seam strength on a printed lattice cross-section** (§3.4, §9.2 P3-Q2). No existing id covers it: `CAL-STR-01` is the *Z-layer* (interlayer) strength ratio, a different failure plane; `CAL-FIT-01` is a clearance ladder. This is the only genuinely new empirical residue.

  **My recommendation is to NOT mint an id for it in this doc.** Per the skill's own rule ("misfiling an ARGUED claim as a bet is the failure mode"; "fewer correct bets beat a full-looking table"), the doc recommends *not building*, and `catalog.md` P3-Q2 already owns the measurement with an apparatus ("does the lattice give enough glue area?"). Minting `CAL-SEA-01` here would register a bet for a feature the same document declines to build. If the owner disagrees, the right shape is one bet keyed to the measurement — *adhesive seam strength per mm² on an FFF butt/lap face* — not one per doc.

7. Everything else the doc leans on is already registered and must **not** be duplicated: bed contact floor → `CAL-BED-01` (`print-gate.ts:47-55`, basis "no primary source at all"); 45° overhang → `CAL-OVH-01`; bridge span → `CAL-BRG-01`; 1.2 mm feature floor → `CAL-FEA-01`; seam-lip clearance → `CAL-FIT-01` (`fit-profile.ts:27-40`, whose basis already records it as "one quantity, two documents" — a third would be the same mistake).

---

## 4. Priority order for fixing

1. **F1** (§5.3 + §8 validator 4) — a wrong invariant shipped as a hard error is the only finding here that would break a build.
2. **F12** (dead link + status/Appendix B contradiction) — the doc currently claims an audit that does not exist.
3. **F2 / F5 / F3** — the three arithmetic/measurement errors that propagate into §3.1, §3.4, §4, §9.1, §9.2.
4. **F8** — the missing option that beats the recommendation on its own scorecard.
5. **F6, F7, F9, F11** — claims that are true-but-overstated or right-for-the-wrong-reason.
6. **F13, F10** — citation and implementation-detail corrections.