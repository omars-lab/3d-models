---
date: 2026-09-26
feeds:
  - '[[multicolor-constructions-b-design]]'
---

# Multicolour constructions — research notes (researcher B)

- **Date:** 2026-09-26
- **Produced by:** multicolour research agent B (Claude Opus 5.5), working alone as one of two
  independent researchers; a later agent merges both designs.
- **Feeds:** [`multicolor-constructions-b-design.md`](../multicolor-constructions-b-design.md)
- **Question:** a version of the pattern constructions whose closed shapes (the regions the
  traces enclose) are filled and coloured, printable in several colours on the Bambu Lab X2D
  with an AMS, under Omar's rule "shapes that are translations same midpoint from center should
  be same color".

Every web source below is marked **fetched** (the page body was read with WebFetch) or
**snippet-only** (only a search-result snippet was seen; the fetch failed or was not tried).
A snippet-only source carries no load-bearing number in the design doc on its own.

---

## 1. What already ships (read in code and docs, not the web)

bikar is read at `origin/main` = `6356bb3` (the `bikar-main` work tree, HEAD equal to
origin/main on 2026-09-26). Paths below are bikar paths, written plainly because they live in the
sibling repo.

1. **Colour regions on a coaster exist.** A `palette` block plus
   `color base|straps|border <Name>` ([D-073](../decisions-log.md), design [`coaster-colour-design.md`](../coaster-colour-design.md)).
   `bikar render --format parts` splits the coaster height field into one watertight body per
   colour, as stacked columns cut at `z = base`, and writes a `<Coaster>.parts.json` sidecar
   (fields `region`, `stl`, `triangles`, `paletteName`, `hex`) — bikar packages/cli/src/index.ts,
   the `--format parts` coaster path (`assertNoPhantomFilament`, `gateCoasterParts`,
   `writeCoasterPartBodies`).
2. **Pinches** where a relief meets the slab at an interior point are handled by
   `--pinch fillet|merge|error`, default `fillet`, floor **CAL-PIN-01** (registered, open)
   ([D-074](../decisions-log.md)).
3. **Palette name → logical AMS slot** in first-seen order, slot 1 the plate default, baked into a
   multi-part input 3MF with per-part `extruder` metadata ([D-075](../decisions-log.md);
   `tools/bambu/src/ams.ts` `buildAmsSlotMap`). The headless CLI cannot assign slots at slice time;
   the assignment must be in the input 3MF, and only when its Application tag starts with
   `BambuStudio-` ([`coaster-ams-3mf-contract.md`](coaster-ams-3mf-contract.md), whose sources
   that earlier agent fetched).
4. **`bambu slice coaster`** ([D-077](../decisions-log.md)) verifies the geometry headless on a
   copy with the Application tag stripped; colour is a GUI check because `--load-settings` clamps
   every part to slot 1.
5. **`fill where ring == N color X` carries into the print split** ([D-078](../decisions-log.md),
   [`radial-band-colour-design.md`](../radial-band-colour-design.md)): where a face carries a ring
   colour it wins over the face's coaster region; `bikar bands` lists the rings. D-078 chose to
   **warn, not cap** on colour count and to read the slot count from the device.
6. **`bambu filament`** (`tools/bambu/src/commands/filament.ts`) lists the loaded trays read-only
   over MQTT, confirmed on the live X2D 2026-09-17, and has a reconcile verb that matches a sliced
   plate's logical slots to loaded trays by colour.
7. **What the split refuses today** (bikar packages/core/src/kernel3d/coaster.ts,
   `assertSplittable` / `hasSlabReshapingClause`): `outline pattern` (the minimal style), deboss,
   interlock, rim, trivet, openwork (minimal-frame) and edge bevels. So the traces-only styles —
   minimal, minimal-frame, minimal-pegs, twist — cannot be split into colours today.
8. **Face colour applies only when the relief target is not `straps`.** `fillCellColors` gives
   each relief cell the colour of the face under its centre, and face polygons run out to the
   strap centrelines. With `relief both` the half-strap next to a filled face therefore takes the
   fill colour: under the shipped precedence a fill eats half of each bounding strap.
9. **`relief faces` raises every bounded face** (`inAnyFace`), not a selected set, and the
   relief clause has one height for both targets (bikar packages/core/src/dsl/ast.ts,
   `CoasterReliefNode`: `target: 'straps' | 'faces' | 'both'`, one `heightMm`). A fill lower than
   the straps cannot be written today.
10. **Fill selector attributes** (bikar packages/core/src/dsl/parser.ts `FILL_ATTRIBUTES`):
    sides, arcs, outward_arcs, inward_arcs, area, index, parity, ring, shape, direction, minangle,
    maxangle, source, layer, wave, neighbors, neighbor_sides, whorl. None groups by shape *and*
    radius.
11. **No boolean union** in the kernel (memory `orb-kernel-facts`). The coaster split never needs
    one: each height-field cell column belongs to exactly one body, so bodies are disjoint by
    construction.

## 2. The shipped `ring` bins do not express Omar's rule — measured

`computeRingBins` (bikar packages/core/src/theme/fill-resolver.ts) sorts faces by the distance of
their vertex-average centroid from `findCenter(env)` and starts a new bin whenever the gap exceeds
an absolute `TOLERANCE = 1e-2`. Two defects against the rule:

- **Wrong centre.** `findCenter` (bikar packages/core/src/dsl/evaluator.ts) takes the centre of
  the *first circle defined*, else (0,0). In CS-1 (GimTvN9hw4U) that is A = (0,0), while the
  rosette's rotation centre is G = (10, 17.32). The coaster art, separately, is recentred on its
  bounding-box centre (`resolveCoasterArt`), a third centre.
- **Radius only, not shape.** Two different shapes at the same radius share a ring, so "same
  ring" is weaker than "same shape, same radius".

### 2.1 Method

A throwaway script (scratchpad only, not checked in; it is measurement, not a prototype of bikar
code) read the `data-face-index` paths from `bikar render <construction>.bkr` SVGs (unit = 20),
and for each face computed the area-weighted centroid and a rotation-invariant signature: the
cyclic sequence of (edge length rounded to 0.01, turn angle rounded to 0.1°), collinear vertices
dropped, canonicalised over cyclic shifts, and optionally over the reversed walk (mirror). Faces
with equal signature were then clustered by centroid radius with tolerance 0.05 about a centre
(the area-weighted union centroid, or an override: G for CS-1, O for rDux). The script parses
`M`/`L` path commands only.

**Limits carried (K1/K2):** the grouping is *congruent and same radius*, which is weaker than
*related by a rotation (or mirror) about the centre* — a congruent shape at the same radius but
turned differently relative to the radial line would share a class here. Whether any surveyed
class splits under the stronger test was **not measured**. nmEjCTzMbDg has arc-bounded faces the
script cannot parse and was **not measured**. The 8 constructions below are the
construction roots in bikar's patterns/Constructions folder that were checked; no other pattern
was surveyed.

### 2.2 Results

| Construction | Shipped rings (`bikar bands`) | Classes, mirror separate | Classes, mirror same | Note |
|---|---|---|---|---|
| 7apC5Q9QS-8 | 16 | 18 | 16 | centre (0,0) is right; mirror-same classes match the rings one-to-one; two chiral quad pairs at r 40.38 and 45.71 |
| GimTvN9hw4U (CS-1) | 14 | 8 | 8 | about G; each class is spread over 3–6 shipped rings |
| lEfWSogWscs | 19 | 5 | 5 | |
| n3IidKfXE1I | 35 | 39 | 39 | 12-6-4 composite with several rotation centres (O, W, V): no single centre |
| rDuxHF3xMOc | 80 | 47 | 38 | about O = (10, 24.14); a partial tessellation with outer satellite pairs |
| sDO9fpu76v8 | 170 | 42 | 35 | |
| tA8eSdVx_EQ | 13 | 4 | 4 | |
| nmEjCTzMbDg | 281 | not measured | not measured | arc faces |

CS-1 in detail: `bikar bands` lists 14 rings with tile counts 1, 6, 5, 6, 10, 2, 3, 6, 2, 6, 2,
2, 2, 2 (55 faces). About G the same 55 faces form 8 classes, at r = 0, 11.55, 20, 23.09,
30.55 (12 faces), 34.64, 41.63 (12 faces), 46.19.

### 2.3 The tolerance window

- Largest radius spread inside any class: **≤ 7.9e-5** (pattern units, unit = 20).
- Smallest radius gap between two *congruent* faces in *different* classes, per construction:
  7apC 5.285, CS-1 4.555, lEf 5.734, n3Iid 1.426, sDO9 1.777, **rDux 0.20** — two congruent
  hexagons (area 136.4) at r = 51.06 and 51.26.
- So any tolerance between ~1e-4 and ~0.2 separates every measured class correctly; the shipped
  1e-2 sits inside that window with a margin over 100× above the spread and 20× below the
  tightest gap. The window is in pattern units at unit = 20, so a tolerance should scale with
  the unit rather than be an absolute number.

### 2.4 Mirror copies

Counting mirror images at the same radius as one class changes the class count in 3 of the 7
measured constructions (7apC, rDux, sDO9). In 7apC the mirror-same count reproduces the author's
ring grouping exactly; the mirror-separate count splits two quad classes into chiral pairs.

## 3. Web sources

| # | Source | Status | What it says (as read) |
|---|---|---|---|
| W1 | pctechmag, "Bambu Lab X2D: dual-nozzle 3D printing made easier" — https://pctechmag.com/2026/09/bambu-lab-x2d-dual-nozzle-3d-printing-made-easier/ | **fetched** | "At the center of the X2D is its dual-nozzle printing system." "One nozzle can print the main object while the other handles a compatible support or interface material." Build volume "256 × 256 × 260 mm". Multi-AMS support is mentioned, but **no filament-count limit is stated**, and no waste or time figures for colour changes. |
| W2 | bambureviews, Bambu AMS multicolour / flush-volume guide — https://bambureviews.com/posts/bambu-ams-multicolor-guide/ | **fetched** | "Purge cost scales with the number of color transitions, not the number of colors. A model that alternates colors every layer purges far more than one with large contiguous color regions." Defaults are high; cut similar-colour transitions, "leave dark-to-light pairs near default because that is where bleed actually shows." Flush into infill / into support. Over-trimming "shows as a faint ghost of the previous color at the start of a region". **Gives no numeric multipliers, minimum feature sizes or orientation rules.** |
| W3 | Bambu wiki, "Reduce wasting during filament change" — https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change | **snippet-only** (fetch returned HTTP 402) | Snippet: flushing-volume multiplier can be lowered (figures around 0.85, and lower for similar colours, were in snippets); flush into infill / object. A snippet (source unclear between this page and a review site) put the cost of an orientation where every layer holds several colours at roughly 22× the waste and 11× the time of one where colours sit in few layers. **Not verified; not load-bearing.** |
| W4 | Bambu Lab X2D product page — https://bambulab.com/en-us/x2d | **snippet-only** (HTTP 403) | Snippets (with swingdesign.com) claimed up to 25 colours with multiple AMS units (4 × AMS 2 Pro + 8 × AMS HT + 1 external) routed to one nozzle, the second nozzle for supports or secondary materials. **Not verified.** |
| W5 | Bambu wiki, AMS multi-model compatibility guide — https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide | **snippet-only** | URL and title only. |
| W6 | BambuStudio GitHub wiki — https://github.com/bambulab/BambuStudio/wiki/Multi-color-printing | **fetched, empty** | The fetch returned the wiki index only (the linked pages failed to load); nothing usable. The earlier agent's fetched BambuStudio sources are in [`coaster-ams-3mf-contract.md`](coaster-ams-3mf-contract.md). |
| W7 | Printables, "Multi Color Coasters" (model 972831) — https://www.printables.com/model/972831-multi-color-coasters | **snippet-only** (HTTP 403) | A multicolour flat coaster listing; construction method not read. |
| W8 | MakerWorld, 12-pointed Islamic star coaster (model 405217) — https://makerworld.com/en/models/405217 | **snippet-only** | A multicolour Islamic star coaster exists as a published model; how its colours are separated was not read. |
| W9 | YouTube tutorial on flat multicolour prints — https://www.youtube.com/watch?v=jgunDyX0Rbk | **snippet-only** | Title/snippet only. |

**What the web research did not settle (K2):** only the pages above were looked at. I did not
find, and so cannot cite, a fetched source for: the X2D's usable AMS slot count; whether the X2D's
second nozzle cuts purge for a two-colour job; a minimum colour-region width; or which way up
published multicolour coasters print. W7 and W8 show that multicolour Islamic/geometric coasters
are made and shared; they do not show how.

## 4. Scratch notes carried into the design

- Height-field cell ownership makes the colour bodies disjoint with no gaps — the reason the
  shipped split needs no union — and it holds for any number of colours.
- Colour only in the top ~1.2 mm of a plain-style coaster means few layers with colour changes
  (W2: purge scales with transitions).
- A fill lower than the straps ("cloisonné") lets the strap walls stand between neighbouring
  colours.
- Openwork/minimal styles need the split refusal lifted and make every layer multicolour if
  filled full height — the expensive shape per W2.
- A face clipped by the coaster outline is not congruent to its uncut siblings.
