---
date: 2026-09-27
feeds:
  - '[[multicolor-design]]'
---

<!--
provenance:
  date: 2026-09-27
  produced-by: checker agent (Claude Opus 5.5), the third pass of the two-researchers-then-checker pattern
  feeds: docs/multicolor-design.md (the consolidated multicolour design)
  inputs: researcher A — 3d-models PR #350 (docs/multicolor-constructions-design.md,
          docs/research/multicolor-constructions.md) and bikar PR #261 (branch feat/multicolor-fills,
          commit 5013196); researcher B — 3d-models PR #347 (docs/multicolor-constructions-b-design.md,
          docs/research/multicolor-constructions-b.md)
  method: (1) bikar built from scratch in two fresh worktrees: origin/main at 8e68778 and A's branch
          at 5013196 (npm ci, npm run build); (2) a one-off measurement script (scratchpad, not checked
          in) that compiles each construction with the built core and computes rings, congruence
          classes, per-pair orbit classes, and whole-set symmetry; (3) the prototype rendered with
          --format parts --check on both builds; (4) A's new test file run against main;
          (5) web pages re-fetched on 2026-09-27. Line numbers are as read that day (research/
          exemption).
-->

# Verification notes — multicolour constructions

Raw notes behind [`../multicolor-design.md`](../multicolor-design.md). Researcher A is
[`multicolor-constructions.md`](multicolor-constructions.md); researcher B is
[`multicolor-constructions-b.md`](multicolor-constructions-b.md).

## 1. The measurement script

For each file, compile with the built core (bikar origin/main 8e68778), drop the outer face, and
for every bounded face compute:

- the **area-weighted polygon centroid** (the engine's `Face.centroid` is used only for the ring
  bins, exactly as `computeRingBins` does);
- the engine's rings, re-derived the same way `computeRingBins` does it (distance from
  `ringCenter`, new ring when the gap from the ring's *first* member exceeds 1e-2);
- a **congruence key**: vertex count (collinear vertices dropped) + sorted edge lengths (0.01) +
  area (0.1) — A's key plus area;
- **orbit classes**, per pair: face b joins face a's class when a rotation about the centre by
  (angle of b − angle of a) carries every vertex of a onto a vertex of b within τ = 0.02, or
  (mirror variant) a reflection through the line bisecting their angles does;
- **whole-set symmetry**: the largest n ≤ 24 for which a 2π/n rotation about the centre carries
  every face centroid onto a face centroid (within 0.02), and whether any reflection through the
  centre does.

The centre defaults to the area-weighted centroid of the union of faces; a centre can be passed
by hand (B's O for rDux).

## 2. Results on the plain coaster files at their default size (mm)

| File | Faces | Rings | Congruent + radius classes | Orbit, rotation only | Orbit, mirror admitted | Orbit classes split over rings | Tightest gap, congruent faces in different classes | Whole-set rotation order / a mirror axis |
|---|---|---|---|---|---|---|---|---|
| 7apC5Q9QS-8 | 101 | 16 | 16 | 24 | 16 | 0 | 5.68 | 4 / yes |
| GimTvN9hw4U | 55 | 14 | 8 | 10 | 8 | 7 | 4.35 | 6 / yes |
| lEfWSogWscs | 33 | 19 | 5 | 5 | 5 | 4 | 10.21 | 8 / yes |
| n3IidKfXE1I | 58 | 35 | 39 | 58 | 39 | 19 | 1.17 | 1 / no |
| nmEjCTzMbDg | 540 | 273 | 21 | 30 | 21 | 21 | none | 18 / yes |
| rDuxHF3xMOc | 116 | 107 | 17 | 29 | 17 | 17 | 3.09 | 4 / yes |
| sDO9fpu76v8 | 337 | 168 | 35 | 56 | 35 | 34 | 1.17 | 6 / yes |
| tA8eSdVx_EQ | 22 | 13 | 4 | 4 | 4 | 3 | none | 7 / yes |

Centre = area-weighted union centroid in every row. The mirror-axis column is a yes/no only: the
script's axis de-duplication is approximate, so it does not count axes.

**What this settles:**

- **A's "rings match the classes on 7apC5Q9QS-8" holds**, but only with mirrors admitted: 16 rings,
  16 classes, no class split over rings and no ring holding two classes. With rotation only there
  are 24 classes (chiral pairs split). B says the same ("mirror-same classes match the rings
  one-to-one").
- **A's per-file counts reproduce exactly** on the coaster files (faces, rings, classes 16 / 8 / 5 /
  21 / 17 / 35 / 4), **except n3IidKfXE1I**: A reports 58 classes (one per face); this script finds
  39 with mirrors admitted and 58 rotation-only. A's key may have separated mirror pairs there; not
  traced further.
- **Congruent-and-same-radius equals the mirror-admitted orbit on all 8 files** (no congruence class
  splits under the orbit test). So B's R3-vs-R2 worry ("a congruent shape at the same radius but
  turned differently") did not occur in this set; the orbit test is still the right definition,
  because it is the one a validator can check per face.
- **The area-weighted centroid is a true symmetry centre on 7 of 8 coaster files** (whole-set
  rotation order ≥ 4, a mirror axis). It is not on n3IidKfXE1I (order 1, no mirror): that coaster
  has no single centre, which both A ("seems not to be rotation-symmetric") and B ("no single
  centre") said.

## 3. rDuxHF3xMOc — B's hard case, and why A and B disagree on it

B measured the **root** construction file (patterns/Constructions/rDuxHF3xMOc.bkr at unit 20; 87
faces, 80 rings) about O = (10, 24.14). Reproduced exactly:

- 38 classes with mirrors admitted (B: 38), tightest congruent gap **0.2003** between two hexagons of
  area 136.39 at **r = 51.063 and 51.263** (B: 51.06 and 51.26, area 136.4). **B's claim holds.**
- The same file about its union centroid (−22.19, 40.24) gives 87 rotation-only classes (every face
  alone): the root file is a partial tessellation that is not symmetric about its own centroid.

A measured the **coaster** file (rDuxHF3xMOc-coaster.bkr at size 90; 116 faces, 107 rings). The
coaster adds a `coaster_fill` reflection ("coaster only — not in the video"), which makes the art a
2×2 block of rosettes about O, O_l1, O_l1_l1_p and one more centre. Its union centroid
(−12.59, 43.00) is a true 4-fold centre (orbits of 4 and 8), and there A's 17 classes hold with a
tightest congruent gap of 3.09 mm. About O instead, the coaster gives 38 classes and a 0.179 mm gap
(45.474 vs 45.652) — B's pair again, scaled by the coaster's unit 17.81.

So both researchers measured correctly; they measured **different files about different centres**.
What it means for the design:

- B's centre rule ("the centre of the outermost `rotate N around X`") picks O on the coaster — the
  file has twelve top-level `rotate N around` blocks about several centres, the first about O —
  which is not the coaster's symmetry centre; by B's own rule ("rotations about several centres →
  refuse") the coaster would be refused instead.
- B's rule **refuses 7apC5Q9QS-8 outright**: that file has no `rotate N around` block at all (grep
  of `^ *rotate [0-9]` finds nothing; the rosette is built by `reflect … across` and
  `rotate … by … around` point/line statements). That is the one file both researchers agree on.
- A's centre (area-weighted union centroid) is right whenever the face set has any symmetry: any
  isometry that carries a finite set of regions onto itself fixes its area-weighted centroid. When
  the set has none (root rDux, n3Iid), no centre is right and the class rule is ill-posed.

## 4. Tolerances

- A: absolute 0.05 mm on radius, with a congruence key. B: τ = 1e-3 × unit (0.02 at unit 20), on
  the orbit test.
- A's justification ("closest two real classes are 0.22 mm apart, 7apC rings 9 and 10") is about
  two **different** shapes, which the congruence key already separates; the radius tolerance never
  sees that pair. The smallest radius gap between any two class radii on the coasters is lower
  still (sDO9fpu76v8 0.027 mm, rDux 0.082, 7apC 0.093) — also different shapes. The gap that matters
  is between **congruent** faces: ≥ 1.17 mm on the coasters about their true centres, 0.18–0.20 about
  a wrong centre (rDux about O).
- B's spread inside a class (≤ 7.9e-5 at unit 20) was not re-measured here; the orbit test passing
  at τ = 0.02 on every class is consistent with it.

## 5. The engine code, read at bikar origin/main 8e68778

- `computeRingBins` (packages/core/src/theme/fill-resolver.ts L414): distance from a centre, sorted,
  new ring when `dist - lastDist > TOLERANCE` (1e-2) where `lastDist` is reset only when a ring
  opens — so a ring is anchored on its first member (A's wording is exact; B's "whenever the gap
  exceeds" is close but not exact).
- `findCenter` (packages/core/src/dsl/evaluator.ts L10060): the first circle's centre, else (0,0).
  Both researchers agree.
- `FILL_ATTRIBUTES` (packages/core/src/dsl/parser.ts L5414): 18 words; neither `orbit` nor
  `class` is one.
- **`class` already has a meaning in the language**: `classify .name`, `connect arc … .CLASS`,
  `.class` tags on entities, `faceClasses` in the render (parser.ts L7088–7110; language-reference
  `.class` rows). A `class == N` selector would give "class" two meanings.
- **`orbit` is already the importer's word for the rotation copies of a leaf** ("kept as an orbit
  tree", "a full N-fold orbit" — packages/core/src/import/geogebra/lower.ts L23, L172, L257). Same
  meaning as the proposed selector.
- **A second `relief` clause is refused today**: the coaster statement table marks `relief` as
  taken once `a.relief` is set and throws "coaster '…' already has a 'relief' statement"
  (parser.ts L3355–3365, L3510). B's two-clause syntax needs that changed, which B flagged as
  unchecked.
- `CoasterReliefNode` has one `target` (straps | faces | both) and one height (ast.ts L575). A
  lower fill needs kernel work (a per-owner top height), not only a word.
- `faceColorAt` returns null for `relief straps` (coaster.ts): face colour applies only when faces
  are raised. Both researchers agree.
- Files that select by `ring` on main: **10** `.bkr` files (grep `ring *[=!<>]`), including
  nmEjCTzMbDg-coaster.bkr. B said 8; main has moved or B counted differently.

## 6. bikar PR #261, checked

- Builds clean at 5013196; `git merge-tree` against origin/main 8e68778 (which added #262 to the
  same coaster.ts) reports no conflict.
- `render 7apC5Q9QS-8-fill-coaster.bkr --format parts --check` on A's build: base euler 2, Slab 184,
  Ruby 18, straps −200, all watertight, all PASS. Same four numbers at `--param size=80`.
  **A's claim reproduces.**
- The same file on **main's** build: every gate PASSES too, with Slab euler −16 and **straps euler
  0** — the straps body is one ring (the outer line), the defect fix 1 removes. **The mesh gate does
  not catch the lost straps**; only a per-cell or picture check does. That is the strongest reason
  for fix 1 and for the strap-ownership validator in the design.
- A's test file run against main's kernel (with the fixture copied in): **2 of 6 fail** — "no
  raised strap cell takes a face colour…" and "the straps body reaches the inner octagon…". The
  other 4 pass on main, including the watertight test for fix 2: fix 2's failure only appears once
  fix 1 is in (A's research §3 item 2 says so: "after that fix, two bodies were not watertight").
  Fix 2 therefore has no test that fails on main by itself; its guard is the combination.
- `vitest run packages/core/tests/kernel3d/` on A's branch: 71 files, 1149 tests, all pass.
- Scope of fix 1: gated on `relief.target === 'both'`. No shipped `.bkr` on main uses `relief both`
  (grep: only packages/core/tests/dsl/coaster-parse.test.ts), so no shipped coaster changes.
- Scope of fix 2: runs only when `field.colors.length > 0`, and only moves cells from a colour piece
  to its region piece; the loop ends because colour cells strictly fall. A block where two region
  keys (straps and border) form the bowtie is left unresolved (no move), so the gate would still
  catch it — not a new failure.
- The prototype also adds a Coaster Lab preset + thumbnail, a patterns/index.json entry and a
  public-surface count bump (158 → 159): merging it publishes a preset.

## 7. Web sources, re-opened 2026-09-27

| Source | Cited by | Re-fetch | What the page says |
|---|---|---|---|
| [Bambu AMS product page](https://us.store.bambulab.com/products/ams-multicolor-printing) | A W1 | **refused (HTTP 402)** | Not readable. "4 slots per AMS" stays snippet-only. |
| [X2D FAQ](https://bambulab.com/en-us/x2d/faq) | A W2, B W4 | **refused (HTTP 403)** | Not readable. A 2026-09-27 search summary repeats "up to 4 AMS 2 Pro and 8 AMS HT … up to 25 colors" and "1 or 2 AMS 2 Pro natively": snippet-only. |
| [Bambu wiki, multi-AMS compatibility](https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide) | B W5 | **refused (HTTP 402)** | Not readable. |
| [bambureviews AMS guide](https://bambureviews.com/posts/bambu-ams-multicolor-guide/) | B W2 | **fetched** | "Purge cost scales with the number of color transitions, not the number of colors." Over-trimmed flush shows as "a faint ghost of the previous color at the start of a region." No numbers. **B's quotes hold.** |
| [Sovol waste guide](https://www.sovol3d.com/blogs/news/reduce-filament-waste-multi-color-3d-printing-9-practical-moves) | A W7 | **fetched** | "The fastest way to reduce waste is to reduce colour changes"; too-low flushing gives "faint tinting on light filaments or 'dirty' edges on small features"; dark → light is the visible case. **A's quotes hold.** |
| [Printago prime line guide](https://printago.io/guides/bambu-studio-prime-line) | A W6 | **fetched** | "The prime tower only appears on multi-color or multi-material prints"; removing it without redirecting the purge gives colour bleed. **Holds.** |
| [Bambu forum, "So much purge"](https://forum.bambulab.com/t/so-much-purge-tower-infill-support-poop-why-does-it-do-them-all/14369) | A W5 | **fetched** | A user: purge to the chute, then a layer on the tower; "Mine defaults to 45mm³. I changed it to 25mm³". User reports, X1-era, not staff. **Holds as A worded it.** |
| [pctechmag X2D article](https://pctechmag.com/2026/09/bambu-lab-x2d-dual-nozzle-3d-printing-made-easier/) | B W1 | **fetched** | "One nozzle can print the main object while the other handles a compatible support or interface material"; more than two AMS units need a 4-in-1 PTFE adapter; no colour count. **B's reading holds.** |
| [Bambu forum, "One AMS unit with two nozzles?"](https://forum.bambulab.com/t/one-ams-unit-with-two-nozzles/250717) | new (checker) | **fetched** | Users: one AMS can feed both X2D nozzles through the track switch; "the only advantage is the lower amount of purging you would need to do over a single nozzle system"; slower, because it retracts between nozzle changes. User reports, not staff, not measured. |

Not re-opened: A's W4 (Prusa wipe tower), W8 (BambuHub), W9 (Kingroon), W10; B's W3, W6–W9. None of
them carries a load-bearing number in either design.
