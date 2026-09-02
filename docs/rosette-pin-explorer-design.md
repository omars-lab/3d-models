# Petals to Pins — rosette → LEGO-pin explorer (design)

**Status:** grounded 2026-09-01 — adversarial audit applied
([`research/rosette-pin-explorer-grounding-audit.md`](research/rosette-pin-explorer-grounding-audit.md)),
sources in Appendix A, contested bets and divergences in Appendix B. Produced 2026-08-30 to answer a diagnostic question:
*the LEGO pins aren't landing where I expect — why?* The private artifact is a visual
instrument (a hand-ported canvas) built to make that answer visible. **Track 1 shipped
2026-08-31:** the "run bikar, don't re-port it" objective now exists as the bikar-studio
`/rosette-explorer` page, which runs the *real* kernel (`solveAnchorsOnGlobalGrid` + the real
clutch lobes) per piece on live geometry — so the seat/drop verdict is the engine's own, not a
copy. The canvas artifact remains the original diagnostic; the studio page is the kernel-backed
successor for that concern. See the shipped record in
[`d3-integration-design.md`](d3-integration-design.md) §4 and [§6 Track 1](#track-1--run-bikar-dont-re-port-it)
below. Last updated 2026-09-01 — grounded (Appendix A/B); §6.6 is the open ledger.

**Artifact this doc is tied to:**
[**Petals to Pins — rosette → LEGO-pin explorer**](https://claude.ai/code/artifact/df5788b3-8785-492b-a5f0-92533fbad4e5)
(`https://claude.ai/code/artifact/df5788b3-8785-492b-a5f0-92533fbad4e5`) — a single
self-contained HTML page (vanilla JS + canvas, no build step). This doc and that artifact
are one deliverable: the page is the instrument, this file is its design, grounding, and
roadmap. The roadmap ([§6](#6-roadmap--bringing-the-artifact-to-life)) is mirrored in a
"Bringing this to life" panel at the bottom of the artifact; **this file is the source of
record** — if the two disagree, this file wins.

**Monitoring the artifact.** It lives in the Claude Code artifact gallery, not in this repo
(the page is generative HTML, not a checked-in file), so keep track of it this way:

- **Reopen it** — click the link above, or from a Claude Code session run `/artifacts`
  (arrow-keys to it, `o` opens in the browser, `c` copies its link). The most-recent
  artifact of the current session also reopens with `ctrl+]`. On the web, the gallery is at
  [claude.ai/code/artifacts](https://claude.ai/code/artifacts).
- **It is private by default.** Only you can see it until you explicitly share it from the
  artifact view. Decide sharing there, not here.
- **Comments** — reviewers can leave comment threads on the page. Read them from a session
  with the Artifact tool (`action: "comments"`); a thread a reviewer sends to Claude can be
  replied to (`action: "reply"`) and resolved (`action: "resolve"`) from the session.
- **Republishing / versions** — editing the source and republishing to the **same URL**
  keeps this link stable and adds a version (the version picker in the artifact view lets you
  roll back). A session that published or is watching the artifact is notified when it is
  republished elsewhere, so re-read before editing to avoid clobbering a newer version.
- **Source of the page** — the working HTML for this session lived in the scratchpad
  (`petals-to-pins.html`); it is not committed. To hand the page to a fresh session, give it
  this doc plus the artifact URL — §2–§4 below specify the port precisely enough to rebuild
  or extend the page, and §6 carries the roadmap.

**Dials currently in the artifact** (all live, canvas redraws on change):
`points` (n, 5–16), `crossover angle`, `petal reach` — the rosette; `baseplate you own`
(48×48 … 8×16, drawn to scale with a fits/too-big check), `pattern span` (studs across),
`piece gap` (grout, edge-offset inset), `grid nudge X/Y` (baseplate registration); plus
show-toggles (grid, studs, seated anchors, dropped anchors, piece fill) and a per-piece
click-to-solve readout + census.

---

## 1. What it is, and the job it does

One interactive page. It dynamically generates a bikar rosette (the same geometry the
studio dial drives), lays a real 8.0 mm LEGO stud grid under it, and for **each piece** of
the pattern runs bikar's own anchor solver to decide whether that piece gets a **tube**
(≥2×2), a **pin** (1×N), or **nothing** (1×1) — and then shows, per candidate position,
which anchors *seat* and which *drop*.

The single job: expose *why* the pins land where they do. The "pins aren't what I expect"
surprise is not a bug in placement — it is the interaction of three things the tool now
draws explicitly: (a) the rosette's pieces are lobed/curved, not rectangles; (b) anchors are
placed on the interior stud lattice and **dropped, never nudged**, when their full ribbed
footprint can't fit inside the outline; (c) the diameters doing the fitting are provisional,
unmeasured knobs.

Audience: the maker (this user) debugging the decomposition, plus anyone deciding whether
the [`mural`](lego-pattern-set-design.md) pattern-set path is worth building.

Non-goals: it is **not** a mesh generator and does not claim byte-fidelity with bikar's STL.
It reimplements bikar's *placement rule* faithfully (the geometry that decides seat/drop),
not its solid modelling. It is a lens on the kernel, not a second copy of it.

---

## 2. The rosette — a faithful port of bikar's kernel

Ported from bikar's rosette kernel (`packages/core/src/kernel/rosette.ts`,
`rosetteGeometry`). One reference petal is solved on the +x axis, then rotated `n` times by
`2π/n`. All symbols in pattern units; the `.bkr` uses `circle C0 radius 100`.

```
φ = π/n
proportioningRadius = R·(1 − sin φ)
innerRadius         = petalFraction · proportioningRadius
E = (R·cos φ, 0)                              # outer tip — touches the n-gon edge midpoint
H = (proportioningRadius·cos φ, −propR·sin φ) # inner corner
X = (innerRadius, 0)                          # innermost point, on axis
th = angleDeg·π/180 ;  d = (−sin th, −cos th)
w  = H − E ;  t = (w·w)/(2·(d·w)) ;  G = E + t·d     # shoulder solve (crossover point)
base = [E, G, H, X, mirror(H), mirror(G)]           # hexagon; mirror(p) = (p.x, −p.y)
```

For `j = 0..n−1`, rotate `base` by `2φ·j` → one hexagon **petal** each. The **star** face
is built by pushing `v[3]` (X, inner) then `v[4]` (H′, outer corner) from every petal → a
`2n`-gon. A key identity that keeps the star simple: `H′_j == H_(j+1)`, so adjacent petals
*share* their outer corner — the star's outer vertices are the petal contact points.

**Result:** `n` hexagon petals + **1** star = `n + 1` pieces. n = 10 → 11 pieces.

Dials exposed (matching the studio's surface):
- **Points** `n` — 5..16.
- **Crossover angle** `angleDeg`. **Default:** `180/n` degrees, which makes the petal flanks
  parallel; sourced from bikar's `rosetteParallelAngle`
  ([`kernel/rosette.ts:101`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel/rosette.ts#L101),
  consumed at [`dsl/evaluator.ts:8006`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/dsl/evaluator.ts#L8006)).
  The tool auto-tracks this default when `n` changes unless the user has diverged from it.
  The kernel's declared range is 0–90°, but petals turn reflex above `rosetteReflexOnsetAngle`
  `= 45 + 90/n` ([`kernel/rosette.ts:115`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel/rosette.ts#L115)); the slider can
  reach past that ceiling, and the figure it then draws is legal but not a rosette anyone builds.
- **Petal reach** `petalFraction`. **Default:** `cos(2φ)/cos(φ)` with `φ = π/n`; same file
  ([`kernel/rosette.ts:132`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel/rosette.ts#L132)).
  Valid range `0 < f < cos(π/n)`.

The studio itself has **no separate JS rosette path** — it re-runs the kernel via
`compileToGeometry` + `renderSVG`. This artifact is therefore the *only* standalone JS
port; it is checked against the kernel's formula above, not against a second implementation.

---

## 3. The LEGO grid — dimensional grounding (and its hedges)

Constants are bikar's, from `packages/core/src/kernel3d/lego.ts` and `grid-gate.ts`. Every
diameter below is a **provisional, unmeasured knob** — no caliper has touched a printed part
(this is the D-005 caveat; the clutch outcome is D-006 / LG-S1). The tool surfaces this
verbatim in its footer and in every per-piece detail card, so no number reads as a promise.

| quantity | value (mm) | note |
|---|---|---|
| stud pitch | **8.0** nominal | LDraw 20 LDU; `lego.ts` calls it "the one uncontested number". Measured: **7.993 ± 0.007** across 37 pitches of a 48×48 baseplate (Cailliau) and **7.986 ± 0.002** on a 112-stud wall of Technic beams (Munafo, via the Lugnet FAQ). Over 16 studs that is 0.11–0.22 mm — Appendix B.1 |
| part relief | 0.2 | `footprintMm(studs) = 8·studs − 0.2` (0.1/side) |
| stud ⌀ | 4.8 nominal | measured 4.85–4.9 on moulded parts; the "5.0" some pages give is a rounded figure, not a measurement — see below (K1 hedge) and Appendix B.2 |
| tube (anti-stud) OD | 6.5137 nominal | derived `2·(8/√2 − 4.8/2)` |
| bore ⌀ | 4.8 | receives the mating stud |
| pin ⌀ | 3.2 nominal | solid post for 1×N |
| rib / rib-arc | 0.1 / 0.8 | the clutch lobe; "single most consequential unmeasured number" — `CAL-RIB-01`, coupon LG-F1 |
| default fit | −0.2 diametral | a knob, not a measurement (D-005): effective pin ⌀ = **3.0**, effective tube OD = **6.314**; stud entry is `CAL-STK-01` (LG-S1), plate fit `CAL-CLB-01` (LG-P2) |

**K1 hedge, carried not stripped:** the stud diameter is **not settled**, but the split is
nominal-vs-measured, not 4.8-vs-5.0. The nominal class is **⌀4.8 mm** (LDraw 12 LDU, Bartneck's
drawings, Brick Owl); the measured class is **4.85–4.9** (Cailliau 4.9; Brighton Toy Museum
4.88–4.89, "deliberately oversized"; binderclipscorpion 4.88). The **5.0** that orionrobots
reproduces is Poskanzer's rounded line on the Lugnet FAQ, and orionrobots' tube OD 6.31 and
wall 0.657 are the tangency formula run with that 5.0 — one rounded number, not an independent
source (settled in the [Lego Lab audit](research/lego-lab-grounding-audit.md)). Stud height is
split the same way: 1.6 (LDraw) vs 1.7 (Lugnet, Brick Owl) vs 1.8 (Cailliau, measured). bikar
ships **4.8**; the tool uses 4.8 and labels it — it does not launder the split into a single
"true" number. What a *printed* stud measures is empirical and lives inside `CAL-STK-01`'s
entry rungs, not in a doc edit.

Dimensional sources, with the fetched text restated in the audit's deep dive 1 so the
numbers survive link rot (Appendix A lists them):
- Lugnet FAQ "Dimensions" — Munafo's **7.986 ± 0.002 mm** pitch (Technic beams, 112 studs);
  Poskanzer's 8 / 5 / 1.7 lines; LDraw 20 LDU.
- Cailliau — **7.993 ± 0.007 mm** across 37 pitches of a 48×48 baseplate; stud 4.9, height 1.8.
- orionrobots "LEGO specifications" — a transcription of the above (its "7.985" is a slip for
  Lugnet's 7.986); the 2005 blog URL first cited here now returns 404.
- brickowl.com stud-dimensions page — HTTP 403 on both fetches; the seam survey's earlier
  fetch (1.7 stud height, "8x − 0.2" footprint) is the record.

---

## 4. The anchor solve — bikar's rule, run per piece on one baseplate

Ported from `packages/core/src/kernel3d/grid-gate.ts` (`solveAnchors`, `anchorKind`,
`signedDistToRing`) and `brick.ts` (the lobed pin/tube footprint). Every number below is pinned
at bikar `3900371`: [`SNAP_THRESHOLD_MM`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L110), [`ANCHOR_CLEARANCE_MM`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L113),
[`MIN_SHELL_WALL_MM`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L116), [`MIN_ANCHOR_WALL_MM`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L119), [`anchorKind`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L156),
[`cellReach`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L256), [`reach`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L276), [`wallMm`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L297), [`anchorability`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/grid-gate.ts#L345);
lobes at [`brick.ts:393`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/brick.ts#L393) (tube), [`:410`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/brick.ts#L410) (pin), [`ribbedCircle`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/brick.ts#L231),
[`BRICK_MIN_FEATURE_MM`](https://github.com/NaqshCoffee/bikar/blob/39003717177f5237c8cc4a59498405da616f2607/packages/core/src/kernel3d/brick.ts#L83). The shipped studio page does not call `solveAnchors`: it calls
[`solveAnchorsOnGlobalGrid`](https://github.com/NaqshCoffee/bikar/blob/74eab002fb25242bb64a8c8b3f20b8a037e5d63a/packages/core/src/kernel3d/grid-gate.ts#L342) (added after the pin, same reach and wall rules, plus
dropped-anchor positions) and passes `anchorability(sol, +∞, true)` — the shell-wall criterion
is **skipped by design**, because the page has no 3D body to measure it on
([`rosette-explorer.ts:308`](https://github.com/NaqshCoffee/bikar/blob/74eab002fb25242bb64a8c8b3f20b8a037e5d63a/packages/web/src/rosette-explorer.ts#L308)).

**One shared grid.** bikar's standalone `solveAnchors` uses a *piece-local, centered*
lattice sized to the brick's `c×r`. The tool instead lays **one global 8 mm baseplate**
under the whole rosette and solves each piece against it — the pattern-set / `mural` model,
because that is what "a toggle-able LEGO grid overlay and how each pin fits" actually asks
for: pieces on a common plate, not each on its own private grid. This is the design's one
deliberate divergence from the per-brick kernel path, and it is the honest one for a mosaic.

Per piece (petal or star), in mm on the global grid (offset by the two "grid nudge" dials):

1. **Engaged studs.** A stud at lattice point `s` engages the piece iff
   `signedDist(s, outline) ≥ cellReach`, where `cellReach = 8/2 − 0.2/2 = 3.9`. (This reads
   the cell, not the fit — bikar's exact rule: the body must cover the whole 8 mm cell.)
2. **Footprint & kind.** `c×r` = bounding box of the engaged studs.
   `anchorKind(c,r)`: `c≥2 ∧ r≥2 → tube`; `c==1 ∧ r==1 → none`; else `pin`.
3. **Candidates.** Tube → interior lattice vertices whose four surrounding studs are all
   engaged (the `(c−1)·(r−1)` interior points). Pin → midpoints between adjacent engaged
   studs along the long axis. None → no candidates.
4. **Seat vs drop.** `reach = outerDia/2 + rib + 0.4`
   (`ANCHOR_CLEARANCE_MM`). Keep a candidate iff `signedDist(candidate, outline) ≥ reach`
   → **seated**, recording `wall = clear − outerDia/2 − rib`. If it's inside the outline but
   `clear < reach` → **dropped** (drawn as a dashed ghost). Outside → skipped.
   Tube reach ≈ **3.66 mm**, pin reach ≈ **2.00 mm** (effective diameters).
5. **Anchorability verdict** — three of bikar's four criteria; shell-wall (≥ 1.2 mm) needs the
   3D body and is skipped, as above: `studsEngaged ≥ 2` (rotation lock), `seated ≥ 1`,
   `minAnchorWall ≥ 0.8 mm`. PASS/FAIL with the specific failing reason named.

The pin/tube are drawn with their real clutch geometry: tube = circle + 4 lobes at
45/135/225/315° + a ⌀4.8 bore; pin = disc + **3** lobes at 90/210/330° (odd count, so
opposing lobes can't cancel). Lobes ramp the rib bulge to 0 over ±`ribArc/2` — a port of
`ribbedCircle` from `brick.ts`.

---

## 5. What this makes visible — the "pins aren't what I expect" diagnosis

Toggling the grid and dragging the two **grid-nudge** sliders demonstrates each failure
mode directly:

- **Petals are small and lobed.** At most useful print scales a petal spans only 2–3 studs
  and its curved flanks mean the `3.9 mm` cell-coverage test rejects studs a bounding box
  would suggest are inside. Many petals resolve to **1×N pins** or, when only one stud
  engages, to **nothing** (`studsEngaged < 2` — fails rotation lock). This is the biggest
  source of surprise: *a piece can look plenty big and still get no anchor.*
- **Drops, not nudges.** bikar never moves an anchor to make it fit; it drops the candidate.
  Under a concave petal edge the full ribbed footprint (`reach`) pokes outside the outline,
  so the anchor vanishes rather than sliding inward. The dashed ghosts show exactly where.
- **Registration is everything.** The same rosette at the same size gets a different anchor
  census depending on where the baseplate sits under it. The grid-nudge dials make pins
  appear and disappear — proof that the pattern is not grid-registered by construction, one
  of the open `mural` design questions (`SNAP_THRESHOLD_MM` is a lattice-snap threshold, not
  a visual-alignment tolerance — the K10 note in
  [`lego-pattern-set-design.md`](lego-pattern-set-design.md) §3).
- **Seats, not grip.** Even a seated anchor is geometry only. Clutch is elastic and every
  diameter is unmeasured (D-005/D-006). Printed-onto-printed interference on the shipped
  defaults *computes* to 0.00 mm — the −0.2 knob cancels the +0.2 relief — and bikar reports
  that as a warning; LG-S1 is the coupon that will measure it and has not been printed
  (`CAL-STK-01`, provisional; Appendix B.3). The tool refuses to say "holds" anywhere — only
  "seats."

---

## 6. Roadmap — bringing the artifact to life

Four tracks, captured 2026-08-30 from the questions raised on the artifact's own comment
threads. Each track states its **objective** (the end state), the **question it answers**,
and its tasks. A single cross-track priority order follows in §6.5; blockers are called out
per task. Legend: **P0** = do first / unblocks the rest · **P1** = next · **P2** = later ·
🔴 blocked · 🟡 partial / in progress · 🟢 done.

### Track 1 — Run bikar, don't re-port it

- **Objective:** any bikar `.bkr` pattern (not just the rosette) is selectable in the page,
  rendered by the *real* kernel rather than a hand-port.
- **Answers:** *"How do we switch to other bikar patterns — dynamically, for any pattern?"*
- **Why it's the keystone:** bikar's studio has **no separate JS geometry path** — it
  compiles the DSL through `compileToGeometry` + `renderSVG`. This page reimplements one
  slice (`rosetteGeometry`) by hand, which does not scale to every pattern. Everything that
  makes this "a bikar → LEGO tool" instead of "a rosette toy" sits behind this track.

**Shipped 2026-08-31** as the bikar-studio `/rosette-explorer` page (bikar PRs #123 `42b22b3`,
#124 `7674683`, #125 `ac26658`). The delivery vehicle question (1.1) resolved to **in-page ESM** — the
studio already runs `compileToGeometry` in-browser, so no CLI/endpoint was needed; the page
recompiles the studio's canonical `Rosette-N.bkr` on every dial change and reads pieces through
the new d3-agnostic `faceConstructs` adapter (1.2). The seat/drop rule is the kernel's own
`solveAnchorsOnGlobalGrid` — the global-baseplate divergence lives **in the kernel**, not the
page — so the hand-port is superseded for the rosette (1.4). The **generic dial schema (Track 2)
shipped 2026-08-31** (bikar PR #126 `cff3cf1`), and the **pattern picker (1.3) shipped the same day**
(bikar PR #127 `6d17651`): a roster of flat, origin-centred `.bkr` figures (Rosette-N + Star-N to
start) with a `<select>` that swaps between them, each pattern's dials generated from its own
compiled schema — so **Track 1 is fully shipped** and the last open non-printer piece is closed.

| # | task | priority | blocker / depends | status |
|---|---|---|---|---|
| 1.1 | Decide the delivery vehicle: bundle bikar core as ESM/WASM in-page **vs.** a thin compile endpoint (`.bkr` → polygons) | P0 | needs a call on the bikar-studio public-surface question (open user decision) | 🟢 in-page ESM |
| 1.2 | Expose `compileToGeometry` (or endpoint) returning per-piece polygons in a stable shape | P0 | 1.1 | 🟢 `faceConstructs` adapter |
| 1.3 | Pattern picker UI; load `.bkr` sources (rosette, star, girih, maclado…) | P1 | 1.2 ✓; Track 2 (schema) ✓ | 🟢 roster picker shipped — bikar #127 `6d17651` (Rosette-N + Star-N; add a pattern = one roster line); **widened to six 2026-09-01** — bikar #134 `85269ac`: Girih {10/3}, Girih decagon, a hex field (6-fold tiling) and a Star-8 field (square tiling) join, one figure per §5.3 lattice row plus girih. Measured before adding: the tiler repeats one way from the origin, so tilings compile off-centre (Hex-Tiled centre (300, 259.8), Star-8-Tiled (200, 200)) — the page recentres every figure on its bbox and frames the stage from the declared span (`stageViewBox`), so "origin-centred" stopped being a roster precondition |
| 1.4 | Replace the hand-ported `rosetteGeometry` path with the engine output; keep the JS port only as an offline fallback | P1 | 1.2 | 🟢 studio page runs the kernel |

### Track 2 — Config is per-pattern: a schema, not a skill

- **Objective:** the dials for whatever pattern is loaded are **generated from data**, not
  hand-coded per pattern.
- **Answers:** *"Are these config params specific to a pattern? Do we need a Claude skill per
  pattern?"* — Yes, they're rosette-specific; and **no**, no skill is needed at runtime.

**Shipped 2026-08-31** (bikar PR #126 `cff3cf1`). 2.1 turned out to be **already delivered by the
parser**: `compileToGeometry(src).params` returns one `ParamSpec` (name / default / min / max /
step) per `param` line — the schema a knob UI needs was already on the wire, so no core change
was made. 2.2 wired the web side: `buildPatternDials` builds one dial per `ParamSpec` straight
off its bounds/step/default (a rangeless spec falls back to a number field), the three hard-coded
rosette sliders are gone, and state carries a generic `params` map fed back into
`compileToGeometry({ params })`. One deliberate trade: the old crossover→180/n auto-follow was
rosette-specific UI sugar the schema can't express, so it was dropped — the objective is one
generic surface with no per-pattern runtime knowledge, which is exactly what 2.3 concluded no
runtime skill is needed for.

| # | task | priority | blocker / depends | status |
|---|---|---|---|---|
| 2.1 | Surface each `.bkr`'s implied parameter schema from bikar's parser (a rosette declares `angle`/`reach`/`points`) | P1 | Track 1.2 (engine access) | 🟢 already on `result.params` (`ParamSpec`) |
| 2.2 | Render dials automatically from that schema (type, range, default) — one generic UI | P1 | 2.1 | 🟢 `buildPatternDials` |
| 2.3 | *(Optional, build-time only)* an authoring skill to add a NEW pattern / wire it into the picker — not a per-pattern runtime dependency | P2 | none | ⚪ not needed at runtime |

### Track 3 — A real baseplate library

- **Objective:** the user picks the plate they actually own (brand + size), sees it to scale,
  and gets a real link to buy it.
- **Answers:** *"Customize the LEGO grid — different grids with thumbnails, dimensions, and
  (possibly) affiliate links, based on what people have."*
- **Status:** 🟡 the picker ships now (48×48, 32×32, 16×32, 16×16, 8×16 — real dimensions,
  drawn to scale, fits/too-big chip). Remaining work is data, not mechanism.

| # | task | priority | blocker / depends |
|---|---|---|---|
| 3.1 | Picker with LEGO-brand plate sizes, drawn to scale + fit check | P1 | — · 🟢 **done** |
| 3.2 | Externalize plates to a data file `{name, studs, mm, brand, thumbnail, buy-link}` | P2 | none |
| 3.3 | Add verified clone plates (Mega, generic) **with measured pitch drift** | P2 | `CAL-CLB-01` bet → coupon **LG-P2**, held on a printer 🔴 |
| 3.4 | Thumbnails + real buy/affiliate URLs | P2 | data-entry / partner step — **must be real, not fabricated** 🔴 |

### Track 4 — Ground the pin count

- **Objective:** the tool can express *how many* interior tubes a printed piece actually
  needs, backed by a measurement rather than a guess.
- **Answers:** *"Do we need all these pins in the middle? Can we websearch how many are
  recommended?"* — Websearched: LEGO publishes **no minimum stud/tube count**; clutch is a
  cumulative interference fit and real plates carry a tube at every interior junction, so the
  middle tubes aren't *wrong*, but a printed anti-stud piece needn't keep them all.

| # | task | priority | blocker / depends |
|---|---|---|---|
| 4.1 | Keep bikar's honest floor visible in the readout: ≥2 engaged studs (rotation lock) + ≥1 anchor | P1 | — · 🟢 already surfaced in the verdict |
| 4.2 | Let the user cap interior tubes and watch the clutch/material trade | P2 | none (UI only) |
| 4.3 | Answer "is it enough?" with a printed coupon | P2 | **LG-F1 / LG-R1**, held on a printer 🔴 |

### 6.5 Priority order across tracks

1. **P0 — 1.1, 1.2** (engine access): the keystone; unblocks Tracks 1–2. Gated on the
   bikar-studio public-surface decision.
2. **P1 — 2.1, 2.2** (schema-driven dials, ✓ **done** 2026-08-31), **1.4** (✓ done) and
   **1.3** (pattern picker, ✓ **done** 2026-08-31 — bikar #127): every non-printer piece of
   Tracks 1–2 is now shipped.
3. **P1 — 4.1** (already done) stays; **3.1** (done) stays.
4. **P2 — 3.2, 4.2** (data-file + tube cap): cheap, no blockers, do opportunistically.
5. **Printer-gated (🔴, HELD until a Bambu-class printer):** 3.3 (`LG-P2`/`CAL-CLB-01`),
   3.4 (real links), 4.3 (`LG-F1`/`LG-R1`). These cannot close without a measured part —
   the same wall every LEGO-pin coupon hits (see [backlog.md](backlog.md) §3.2, print-gated).

---

### 6.6 The open ledger — what is left, by what gates it (2026-09-01)

Tracks 1–2 are shipped and §6.5's printer-held rows are held; this subsection is the residue read
against the Lego Lab's original five goals
([`lego-lab-design.md`](lego-lab-design.md) §1). Four of those five are code and all four are
built — the `brick` declaration, the anchorability gate, the grid-fit score with its sweep, and
the Lab page. The fifth — **true-scale interoperability verified in plastic** — is the only goal
still open, and it is open for one reason: no printer. So the ledger sorts by gate, not by
priority, because the gate is what decides whether a line can move this week.

**Unblocked — needs nothing but the work.** In the order that advances "a bikar → LEGO tool
for *any* pattern" fastest:

| # | item | why it advances the goal | size |
|---|---|---|---|
| 6.6.1 | **Widen the roster — 🟢 shipped 2026-09-01** (bikar #134 `85269ac`). Six entries: Rosette-N, Star-N, Girih {10/3}, Girih decagon, Hex field, Star-8 field — one per §5.3 lattice row plus girih. The "flat/centred check per figure" this row priced turned out to be the finding: two of the four tilings compile off-origin (the tiler repeats one way), so the page now recentres on the face bbox and frames the stage from `spanPU`; the roster test asserts each entry centres within 1e-6 and spans what it declares (0.9·spanPU < w ≤ spanPU) | Track 1's objective is *any* pattern; the picker made that a data change and then stopped at two | small — one line each, plus the flat/centred check per figure |
| 6.6.2 | **Ground this doc — 🟢 shipped 2026-09-01** (3d-models #136). Adversarial audit checked in as `research/rosette-pin-explorer-grounding-audit.md`; Appendix A (sources) and B (seven contested bets, all clustered under existing `CAL-*` ids — none minted). What the audit killed: §5's "measured 0.00 mm in LG-S1" (LG-S1 is unprinted; it *computes*), §3's "7.985 … ~0.24 mm" pitch drift (Lugnet says 7.986 ± 0.002 on beams; Cailliau 7.993 ± 0.007 on a baseplate), the 4.8-vs-5.0 stud split (5.0 is a rounded Lugnet line, not a source), §7's "none address relief across seams" (MachineBlocks ships per-brick relief), two PR shas (#124 `7674683`, #127 `6d17651`) and a link to a directory | every other design doc here went through `ground-design-doc`; the roadmap of record cannot be the one exception | medium — one audit agent, apply, appendices |
| 6.6.3 | **3.2 — plates as data.** `PLATES` is a five-entry const in `bikar:packages/web/src/rosette-explorer.ts`; move it to a data file `{id, studs, mm, brand}` so a plate is added without touching page code. **No thumbnails and no buy links** — those are 3.4, which needs real URLs and a partner, and a fabricated link is worse than none | Track 3's objective is "the plate the user owns"; a const list cannot grow past what one author typed | small |
| 6.6.4 | **4.2 — the interior-tube cap.** A dial that drops interior tubes and shows the clutch/material trade, with the kernel's floor (≥2 engaged studs + ≥1 anchor, already in the verdict) left visible and un-overridable | Track 4's question — "do we need all these pins?" — has a websearched answer and no instrument | small–medium; UI only until a coupon can price it |

**Gated on a download — a human must fetch an app.** The LDraw export has been opened by
three.js `LDrawLoader` end to end and by LDView (installed, measured, removed —
[`research/ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md) §10). Two readers are still owed
by [`backlog.md`](backlog.md) §6.1: **LeoCAD**, where the source reading *predicts* the inline
geometry is silently dropped (the export-succeeds-and-yields-nothing class), and **BrickLink
Studio**, which is untouched and which nothing in the survey predicts. Neither can be settled by
code; both need the download that the survey's §1.1 says a human must run.

**Gated on a decision.** `lego-lab-design.md` §11 Q6 leaves one question open: whether a
compliance proxy (rib deflection × count, or an FEA-lite bending estimate) is worth adding beside
the geometry gate. The decision can be made now; the *calibration* of whatever it decides cannot,
because LG-F1 and LG-D1 are the data. A proxy shipped before them is a `CAL-*` bet by
construction, which is legitimate and must be labelled as one.

**Gated on a printer — held, not blocked.** Every coupon in [`backlog.md`](backlog.md) §3.2
(LG-F1, F2, R1, S1, D1, B1, B2, P1, P2), and with them 3.3, 3.4's measured-drift half and 4.3
above. The backlog owns these; they are not re-listed in the task system, per its §3.8.

What this ledger deliberately does **not** carry: the `--format ldraw` thumbnail gate's
graduation to a hook (`lego-lab-design.md` §15.4 — waits on measured recurrence, by design), Q8's
general two-vector basis (resolved as a label, D-007), and Track 2.3's authoring skill (not needed
at runtime). Each is a closed door with its reason on it, not an open item.

## 7. Web-searched options considered (and why this shape)

Prior art surveyed for how others turn one pattern into griddable pieces, and how rosette
generators are built:

- **LEGO Art / World Map mosaic UX**, **dlvoy/base-plate-outliner**, **MachineBlocks**, and
  the systems enumerated in [`lego-baseplate-seam-survey.md`](research/lego-baseplate-seam-survey.md)
  §3 (Finke, Brickapic — snippet-only, pad-print mural vendors) — rectangle-decomposition of an
  image/region onto the stud grid. Confirms the c×r-on-8-mm decomposition is the standard
  move. MachineBlocks **does** ship per-brick relief today (`surfacePattern`, SVG emboss/deboss,
  text, base relief cuts); what none of the systems surveyed there carries is *one relief across
  piece seams on the LEGO grid*, which is the `mural` plan's hard part (Milestone A, edge-to-edge
  relief). The novelty, as the Lego Lab audit settled it, is Islamic pattern × LEGO-registered
  printed part — not "relief on a brick" (Appendix B.4).
- **Brick Mosaic / Bricklink Studio mosaic tools** — colour-per-stud, not printed relief;
  out of scope here (colour is a `mural` non-goal).
- **p5.js / Processing Islamic-geometry sketches and Girih editors** — confirm the
  compass-and-straightedge construction the kernel already encodes; nothing to port back,
  bikar's `rosetteGeometry` is the canonical source.
- **Rosette-generation literature** — Lee & Soliman, *The Geometric Rosette* (2014,
  [PDF](https://tilingsearch.mit.edu/RosetteAnalysis.pdf)) §2: the standard construction's
  proportioning circle is the circle on the centre A of radius AF where CF = CE = half the
  n-gon edge, i.e. `R − R·sin(π/n)` — the kernel's `proportioningRadius = R(1−sinφ)` exactly;
  its "angle ECF = 90° − 180°/n" is the bisector the shoulder solve uses. A. J. Lee, *Islamic
  Star Patterns*, Muqarnas 4 (1987) and Kaplan's
  [*Islamic star patterns from polygons in contact*](https://cs.uwaterloo.ca/~csk/other/phd/kaplan_diss_starpatterns_print.pdf)
  give the "hexagonal arms around a central star" anatomy §2 echoes. One qualifier the
  literature adds: Lee & Soliman's standard rosette has **one** free parameter beyond n (the
  crossover angle); bikar's `petalFraction` is a **second, independent** dial, so the kernel
  is a generalisation and only its default figure can coincide with the standard one — whether
  it does is an open question (Appendix B.5), not a claim.

**Chosen shape:** a single canvas instrument with a live kernel port + a shared-baseplate
solver, rather than an image-mosaic tool, because the question is diagnostic (*why these
pins?*) and the pieces are true polygons from the DSL, not pixels. Canvas over SVG for the
generative redraw on every dial change.

Design treatment (per the artifact-design pass): jewel-tone geometry (brass petals, deep
teal star) as the hero against a warm drafting-parchment ground, with the LEGO/engineering
layer kept quiet and technical (steel-blue studs, green seats, warn-red drops, mono caliper
readouts). Fraunces / Hanken Grotesk / Space Mono. Theme-aware (three states), responsive,
reduced-motion respected.

---

## 8. Open design questions this surfaces (for the user)

These are distinct from the roadmap ([§6](#6-roadmap--bringing-the-artifact-to-life)): the
roadmap is *how to build it*; these are *whether/what to build*, and each is a call for the
user, not a task.

1. **Does the `mural` path (the planned pattern-set feature) want per-piece bounding-box
   footprints, or footprints derived from engaged cells?** The tool shows they diverge for
   curved pieces — the census `c×r` is the engaged-stud box, which is often smaller than the
   art's bounding box.
2. **Is a rosette even a good mosaic candidate on a square grid?** The petals' radial
   symmetry fights the orthogonal lattice; the tool shows how few clean tube-anchored pieces
   result. A square/star tiling might pin far better — worth a side-by-side before committing
   build effort.
3. **Where should this live?** Right now it's a standalone artifact. Options: fold into the
   studio's `/decomp` page (already vendored), keep it as a design-time diagnostic, or drop
   it. It does not need to ship as product to have done its job.

---

## Provenance

Ports are of bikar at `3900371` (`39003717177f5237c8cc4a59498405da616f2607`: `kernel/rosette.ts`,
`kernel3d/lego.ts`, `kernel3d/grid-gate.ts`, `kernel3d/brick.ts` — every §2 and §4 link is
pinned there, and `rosette.ts` is byte-identical at `74eab002`), and the shipped page is read at
`74eab002` (`74eab002fb25242bb64a8c8b3f20b8a037e5d63a`). The 2026-08-29 web fetches
(orionrobots, Lugnet) were re-fetched and traced to their primaries on 2026-09-01 by the
grounding audit, which is the checked-in research record for this doc. The doc gates (D1–D4)
run on it at every commit.

---

## Appendix A — sources

All fetched by the 2026-09-01 audit unless marked; the fetched text is restated in
[`research/rosette-pin-explorer-grounding-audit.md`](research/rosette-pin-explorer-grounding-audit.md)
(deep dives 1–5), so each number below survives a dead link.

**Engine (primary — the thing being ported).**
- bikar `kernel/rosette.ts`, `kernel3d/lego.ts`, `kernel3d/grid-gate.ts`, `kernel3d/brick.ts` at
  `3900371` — linked line-by-line in §2 and §4.
- bikar `packages/web/src/rosette-explorer.ts` and its test at `74eab002` — the shipped page;
  `solveAnchorsOnGlobalGrid` and the roster.
- bikar PRs #123 `42b22b3`, #124 `7674683`, #125 `ac26658`, #126 `cff3cf1`, #127 `6d17651`,
  #134 `85269ac` — merge shas on bikar `main`.

**LEGO dimensions.**
- Lugnet FAQ, [Dimensions](https://www.lugnet.com/~330/FAQ/Build/dimensions) — Munafo's
  7.986 ± 0.002 mm pitch (Technic beams, 112 studs = 895 mm); Poskanzer's 8 / 5 / 1.7;
  Bliss's LDraw 20 LDU.
- Munafo, [mcg](http://mrob.com/pub/mcg.html) — the measurement behind the Lugnet line.
- Cailliau, [General considerations](https://www.cailliau.org/Alphabetical/L/Lego/Dimensions/General%20Considerations/%20General%20Considerations-en.html)
  — 7.993 ± 0.007 mm across 37 pitches of a 48×48 baseplate; stud 4.9, height 1.8, 0.1 mm play
  per side.
- Bartneck, [brick](http://www.bartneck.de/wp-content/uploads/2019/04/lego-2x4-brick-dimensions-measurements-3001.pdf)
  and [plate](http://www.bartneck.de/wp-content/uploads/2019/04/lego-2x4-plate-dimensions-measurements-3020.pdf)
  drawings — ⌀4.8 stud, ⌀6.51 tube, 0.2 mm gap between bricks.
- Brighton Toy Museum, [Lego dimensions](http://web.archive.org/web/20260109123620/https://www.brightontoymuseum.co.uk/index/Lego_dimensions)
  (archive; live page 403) — micrometer 4.88–4.89 stud, "deliberately oversized".
- binderclipscorpion, [plates between studs](https://binderclipscorpion.com/2023/02/08/should-plates-between-studs-be-an-illegal-lego-building-technique/)
  — stud 4.88 measured.
- orionrobots, [LEGO specifications](https://orionrobots.co.uk/pages/lego-specifications.html)
  — a transcription of Lugnet (7.985 is a slip for 7.986; 6.31 / 0.657 are the tangency
  formula with a 5.0 stud). Cited for what it is, not as a measurement.
- Brick Owl stud-dimensions page — 403 on this audit's fetches; recorded in
  [`lego-baseplate-seam-survey.md`](research/lego-baseplate-seam-survey.md) §1 from an earlier fetch.
- The settled verdicts on the stud-diameter and tube-OD split:
  [`lego-lab-grounding-audit.md`](research/lego-lab-grounding-audit.md);
  the LDraw-primitive reading: [`lego-brick-system-survey.md`](research/lego-brick-system-survey.md) §1.

**Rosette construction.**
- Lee & Soliman, *The Geometric Rosette: analysis of an Islamic decorative motif* (2014),
  [PDF](https://tilingsearch.mit.edu/RosetteAnalysis.pdf) — §2 standard construction,
  characteristics 3, 4, 7, 8.
- Kaplan, [*Islamic star patterns from polygons in contact*](https://cs.uwaterloo.ca/~csk/other/phd/kaplan_diss_starpatterns_print.pdf)
  — rosette anatomy, "nearly ideal in the sense given by Lee".
- A. J. Lee, *Islamic Star Patterns*, Muqarnas 4 (1987) 182 — cited through Kaplan and Lee &
  Soliman; not fetched.

**Prior art on splitting one pattern across LEGO-compatible pieces.**
- [`lego-baseplate-seam-survey.md`](research/lego-baseplate-seam-survey.md) §3 — the
  enumeration §7 relies on (LEGO Art 31203, dlvoy, MachineBlocks, Finke, Brickapic, mural vendors).
- MachineBlocks module docs (fetched by the audit): `surfacePattern`, `surfacePatternSvg`,
  `svg`/`svgDepth`, `text*`, `baseReliefCut*`.

**House decisions and bets.**
- [`decisions-log.md`](decisions-log.md) D-005 (knobs backed by `CAL-*` bets) and D-006
  (studs as ports; the computed 0.00 mm).
- [`bets.md`](../.claude/skills/calibrate/bets.md) — `CAL-RIB-01`, `CAL-STK-01`, `CAL-CLB-01`,
  `CAL-REG-01`; 20 provisional, 0 measured at this writing.
- [`catalog.md`](../.claude/skills/prototype/catalog.md) — LG-S1, LG-F1, LG-R1, LG-P2.

## Appendix B — contested bets and divergences

One entry per claim the audit contested. Each carries the counter-position fairly, then either
the justification for diverging or the change made. Bet ids are the existing registry's —
every empirical residue here clusters under a bet that already exists by *the measurement that
settles it*, so none was minted.

### B.1 Pitch drift across a piece — `CAL-CLB-01`

*Counter-position.* The doc's first draft said "7.985 on Lugnet, ~0.24 mm over 16 studs".
Lugnet says 7.986 ± 0.002, measured by Munafo on a wall of Technic **beams**; the one fetched
measurement on a **baseplate** is Cailliau's 7.993 ± 0.007 ("8 mm to within better than one
hundredth"), and bikar's own `lego.ts` calls 8.0 "the one uncontested number" while the seam
survey §1.3 reads Cailliau as showing pitch does *not* accumulate error.

*Change made.* The row now carries both measurements, the part each was taken on, and the
honest span (0.11–0.22 mm over 16 studs). The transfer sentence (K10): Cailliau's figure
transfers to the explorer's baseplate grid directly, because it was measured on that part class;
Munafo's beam figure transfers only if beam and plate moulds share a shrinkage allowance, which
no fetched source states. What a *printed* piece's pitch drifts by against a real plate is
`CAL-CLB-01`'s "pitch delta across a piece span" (coupon LG-P2, held on a printer); until it
runs, the grid-nudge dials in §5 are the instrument for the question, not an answer to it.

### B.2 The stud-diameter split — nominal vs measured, not 4.8 vs 5.0

*Counter-position.* orionrobots gives ⌀5.0 and a 6.31 tube; the first draft treated that as a
second source.

*Change made.* The audit traced 5.0 to Poskanzer's rounded line on Lugnet and 6.31 / 0.657 to the
tangency formula run with it — one rounded number, not an independent measurement (the Lego Lab
audit had already settled the tube half). The split that is real is nominal 4.8 (LDraw, Bartneck,
Brick Owl) against measured 4.85–4.9 (Cailliau, Brighton, binderclipscorpion), and the hedge now
says so. bikar keeps 4.8; a printed stud's diameter is settled inside `CAL-STK-01`'s entry rungs.

### B.3 "Measured 0.00 mm clutch" — `CAL-STK-01`

*Counter-position.* The first draft's §5 said printed-onto-printed clutch "measured 0.00 mm on
defaults in LG-S1". LG-S1's catalog entry is *planned, printing on hold, what we learned:
pending*; D-006 says the interference **computes** to 0.00 mm; the bet registry records 20
provisional and 0 measured bets. Nothing was measured — the coupon's open question had been
written as its answer, the taxonomy's K1 pattern.

*Change made.* §5 now says "computes", names D-006 and `CAL-STK-01`, and says LG-S1 has not been
printed. No conclusion in this doc rests on the number holding.

### B.4 Novelty — "none address relief continuity across seams"

*Counter-position.* MachineBlocks ships per-brick relief today (`surfacePattern`, SVG
emboss/deboss, text, base relief cuts) and the first draft's one-line dismissal omitted it — a
system inside the surveyed set under-reported, the `piece-composition` K2 pattern. Off the LEGO
grid, relief continuity across split prints is a known problem with known answers (alignment
pins, tabs); pad-print mural vendors carry an *image* across tiles at zero relief.

*Change made.* §7 credits MachineBlocks, scopes the claim to the seam survey §3 enumeration, and
narrows the novelty to the Lego Lab audit's settled form: Islamic pattern × LEGO-registered
printed part, with one relief carried across piece seams. Brickapic is named as the nearest
neighbour and marked snippet-only (403), so it is not claimed either way.

### B.5 One free parameter or two — open, argued

*Counter-position.* Lee & Soliman's standard rosette has one parameter beyond n; the inner
point's position "is determined by the size of the crossover angle". bikar exposes two dials,
and the first draft presented both as the rosette's free choices.

*Standing.* bikar's `petalFraction` is a deliberate generalisation, and the doc now says so. Open:
whether the default `cos(2φ)/cos(φ)` makes the default figure coincide with the standard
construction. That is a derivation or a numeric check against `rosette-witness.test.ts`, not a
print — it stays an argued question here rather than a bet, and is the one thing this audit
found that a later reader can close for free.

### B.6 Three criteria, not four — by design

*Counter-position.* §4 listed bikar's four anchorability criteria; the shipped page passes
`anchorability(sol, +∞, true)` and never evaluates shell-wall.

*Standing.* Intended: the page has no 3D body to measure a shell wall on, and the divergence is
now written where the rule is (§4), with the call site linked. The full four-criteria gate still
runs on every `brick` render in bikar, so a piece the page passes can still fail there.

### B.7 The lobe geometry — `CAL-RIB-01`

Every lobe the page draws inherits the 0.1 mm rib and 0.8 mm arc, both provisional (coupon LG-F1,
which also gates the pin coupon LG-R1). The page draws them as bikar's own `ribbedCircle` does, so
when the number moves the drawing moves with it; nothing here claims the lobe holds.
