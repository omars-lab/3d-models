# Petals to Pins — rosette → LEGO-pin explorer (design)

**Status:** draft / working design capture (not yet gate-audited, not yet committed via the
house `ground-design-doc` process). Produced 2026-08-30 to answer a diagnostic question:
*the LEGO pins aren't landing where I expect — why?* The artifact is a visual instrument
built to make that answer visible, not a shipped feature. Last updated 2026-08-30.

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
the [`mural`](../.claude/plans/) pattern-set path is worth building.

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
| stud pitch | **8.0** | LEGO-brand measures **7.985** on Lugnet's survey — a systematic ~0.015/pitch shortfall, ~0.24 mm over a 16-stud span |
| part relief | 0.2 | `footprintMm(studs) = 8·studs − 0.2` (0.1/side) |
| stud ⌀ | 4.8 *or* 5.0 | **sources split** — see below (K1 hedge) |
| tube (anti-stud) OD | 6.5137 nominal | derived `2·(8/√2 − 4.8/2)` |
| bore ⌀ | 4.8 | receives the mating stud |
| pin ⌀ | 3.2 nominal | solid post for 1×N |
| rib / rib-arc | 0.1 / 0.8 | the clutch lobe; "single most consequential unmeasured number" |
| default fit | −0.2 diametral | so effective pin ⌀ = **3.0**, effective tube OD = **6.314** |

**K1 hedge, carried not stripped:** the stud diameter is **not settled**. LEGO's own
technical drawings and multiple maker references give **⌀4.8 mm**; a widely-cited secondary
survey (orionrobots) gives **⌀5.0 mm** (and stud height 1.7 vs bikar's 1.6). bikar ships
**4.8**. The tool uses 4.8 and labels it — it does not launder the split into a single
"true" number. Resolving it is empirical (a measured plate), i.e. a `CAL-*` bet, not a doc
edit.

Web-searched dimensional sources (for the grounding file, if this graduates):
- orionrobots.co.uk — "The Dimensions of LEGO Bricks" (pitch 8, stud ⌀5.0, height 1.7,
  underside cylinder OD 6.31 / wall 0.657, brick wall 1.5). Fetched 2026-08-29.
- Lugnet / LEGO fan measurements — pitch **7.985 mm** (the systematic-error figure).
- brickowl.com dimension pages — returned HTTP 403; not usable as a citable source.

---

## 4. The anchor solve — bikar's rule, run per piece on one baseplate

Ported from `packages/core/src/kernel3d/grid-gate.ts` (`solveAnchors`, `anchorKind`,
`signedDistToRing`) and `brick.ts` (the lobed pin/tube footprint).

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
5. **Anchorability verdict** (bikar's four criteria, minus shell-wall which needs the 3D
   body): `studsEngaged ≥ 2` (rotation lock), `seated ≥ 1`,
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
  a visual-alignment tolerance — the K10 note in the mural plan).
- **Seats, not grip.** Even a seated anchor is geometry only. Clutch is elastic and every
  diameter is unmeasured (D-005/D-006; printed-onto-printed measured **0.00 mm** clutch on
  defaults in LG-S1). The tool refuses to say "holds" anywhere — only "seats."

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

| # | task | priority | blocker / depends |
|---|---|---|---|
| 1.1 | Decide the delivery vehicle: bundle bikar core as ESM/WASM in-page **vs.** a thin compile endpoint (`.bkr` → polygons) | P0 | needs a call on the bikar-studio public-surface question (open user decision) |
| 1.2 | Expose `compileToGeometry` (or endpoint) returning per-piece polygons in a stable shape | P0 | 1.1 |
| 1.3 | Pattern picker UI; load `.bkr` sources (rosette, star, girih, maclado…) | P1 | 1.2; Track 2 (schema) for the dials |
| 1.4 | Replace the hand-ported `rosetteGeometry` path with the engine output; keep the JS port only as an offline fallback | P1 | 1.2 |

### Track 2 — Config is per-pattern: a schema, not a skill

- **Objective:** the dials for whatever pattern is loaded are **generated from data**, not
  hand-coded per pattern.
- **Answers:** *"Are these config params specific to a pattern? Do we need a Claude skill per
  pattern?"* — Yes, they're rosette-specific; and **no**, no skill is needed at runtime.

| # | task | priority | blocker / depends |
|---|---|---|---|
| 2.1 | Surface each `.bkr`'s implied parameter schema from bikar's parser (a rosette declares `angle`/`reach`/`points`) | P1 | Track 1.2 (engine access) |
| 2.2 | Render dials automatically from that schema (type, range, default) — one generic UI | P1 | 2.1 |
| 2.3 | *(Optional, build-time only)* an authoring skill to add a NEW pattern / wire it into the picker — not a per-pattern runtime dependency | P2 | none |

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
2. **P1 — 2.1, 2.2** (schema-driven dials) → **1.3, 1.4** (pattern picker + swap the port).
3. **P1 — 4.1** (already done) stays; **3.1** (done) stays.
4. **P2 — 3.2, 4.2** (data-file + tube cap): cheap, no blockers, do opportunistically.
5. **Printer-gated (🔴, HELD until a Bambu-class printer):** 3.3 (`LG-P2`/`CAL-CLB-01`),
   3.4 (real links), 4.3 (`LG-F1`/`LG-R1`). These cannot close without a measured part —
   the same wall every LEGO-pin coupon hits (see [backlog.md](backlog.md) §3.2, print-gated).

---

## 7. Web-searched options considered (and why this shape)

Prior art surveyed for how others turn one pattern into griddable pieces, and how rosette
generators are built:

- **LEGO Art / World Map mosaic UX**, and **dlvoy/base-plate-outliner**, **MachineBlocks** —
  rectangle-decomposition of an image/region onto the stud grid. Confirms the c×r-on-8-mm
  decomposition is the standard move; none address *relief continuity across seams*, which
  is the `mural` plan's hard part (Milestone A, edge-to-edge relief).
- **Brick Mosaic / Bricklink Studio mosaic tools** — colour-per-stud, not printed relief;
  out of scope here (colour is a `mural` non-goal).
- **p5.js / Processing Islamic-geometry sketches and Girih editors** — confirm the
  compass-and-straightedge construction the kernel already encodes; nothing to port back,
  bikar's `rosetteGeometry` is the canonical source.
- **Rosette-generation literature** (n-fold rosettes from a proportioning circle) — matches
  the kernel's `proportioningRadius = R(1−sinφ)` construction; reassuring, not novel.

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

Ports are of bikar at the working tree checked out 2026-08-29 (`kernel/rosette.ts`,
`kernel3d/lego.ts`, `kernel3d/grid-gate.ts`, `kernel3d/brick.ts`). LEGO dimensional sources
fetched 2026-08-29 (orionrobots.co.uk; Lugnet pitch survey). If this graduates to a
committed design doc, the bikar references must be pinned to a git ref and the web sources
moved into `docs/research/` under a provenance header per the `ground-design-doc` process,
and the whole thing run through the doc gates (D1–D4) and an adversarial grounding audit.
