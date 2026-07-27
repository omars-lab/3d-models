# Orb Lab — design doc (pre-implementation)

Status: **DRAFT v2 — revised after design review with Omar (resolved decisions in §11). No
implementation yet.**
Scope: an adjustable, knob-driven orb configurator ("Orb Lab") published in the 3d-models
catalog, with URL-query-parameter state sync, custom-orb capability, and a matching
**Dials vs Code** construction-mode tab (with visual icons) in bikar studio.

All engine facts below were verified against bikar @ `f9eab09` (file:line refs are into
`~/Workspace/git/bikar`). All knob ranges marked *measured* come from CLI render sweeps run
against the committed Rosette-Orb baseline (dodecahedron, R=60 mm, struts 3×2.4 mm).

---

## 1. Goals

1. **Knobs, not code, as the front door.** A visitor moves sliders/pickers and watches a 3D
   orb change live; every knob combination that renders is printable (STL download passes the
   mesh gate).
2. **URL = state.** Every adjustment updates the query string (debounced `replaceState`), so
   any orb design is a shareable/bookmarkable link and the six curated gallery orbs are just
   preset links into the Lab.
3. **Custom orbs.** An escape hatch from knobs to the full `.bkr` DSL — view the code the
   knobs generate, edit it, keep the URL shareable (compressed), and hand off to bikar studio.
4. **Studio parity (new requirement).** Bikar studio gets an explicit construction-mode tab
   pair — **Dials** (knob UI) vs **Code** (editor) — with visual icons, sharing one template
   engine with the Lab.
5. **Maximize reachable pattern diversity** for a given knob budget: knobs are chosen so the
   space of *valid* orbs is as visually wide as possible (§4), and invalid regions are either
   clamped away or surfaced with the engine's own actionable errors (§5).

Non-goals (v1): per-face pattern mixing (engine doesn't support it — see §2), girih-field
orbs, community sharing/galleries, in-browser qiyas validation (Python; stays in CI),
hemisphere-split FDM export (task #11, separate decision).

Motivation check (research, Appendix A): **no browser configurator for Islamic-pattern
spheres exists.** Nearest prior art is 2D pattern generators, static STL uploads, and
Kaplan's academic interwoven-sphere pipeline (not distributed). Orb Lab fills a real gap.

---

## 2. Engine reality — what knobs *can* exist

The `orb` grammar (parser `packages/core/src/dsl/parser.ts:588-772`) admits exactly seven
statements: `base`, `radius`, `inscribe`, `project`, `struts`, `pierce`, `weave`. This is the
complete dial-able surface at the orb level:

| Statement | Values | Notes |
|---|---|---|
| `base` | `tetrahedron octahedron cube dodecahedron icosahedron` | exactly 5; `goldberg`/`icosidodecahedron` are rejected future names |
| `base icosahedron subdivide N` | integer 1..4 | **icosahedron only** (parser-gated); 1 is a no-op; tris ×~4 per level |
| `radius <mm>` | positive number | mid-surface sphere circumradius |
| `inscribe <pattern>` | one bare pattern name | **no `where` filter; one pattern lifts onto every face** |
| `project` | `spherical` \| `faceted` | exactly two modes |
| `struts width <mm> depth <mm>` | two positive numbers, fixed order | **no profile option — always rectangular** |
| `pierce voids` | literal | optional; v1 always pierces |
| `weave crossing alternating amplitude <mm>` | positive amplitude | only `alternating`; switches to woven-ribbon family |

Everything else that shapes a pattern lives at the **pattern level** (rings, `divide` counts
and offsets, `connect cycle` petal shapes, `hankin angle/delta`, `rotate N`, `voids detect`…).
Two consequences drive the whole design:

- **Consequence 1 — templates, not a grammar UI.** Arbitrary pattern edits break the
  cross-face closure rules (boundary contacts must land on face corners, exact edge midpoints,
  or symmetric pairs; weaves additionally need all nodes to be degree 2/4 with solvable
  crossing parity). Sliders therefore parameterize **curated archetype templates** — code-gen
  functions that emit closure-safe `.bkr` source — never raw grammar.
- **Consequence 2 — the browser can run everything.** `compileToGeometry(source)` →
  `EvaluationResult` (with `.orbMesh` + `.orb3d` provenance) is the same public core entry the
  studio already uses (`packages/web/src/main.ts:4668`). `emitBinarySTL(mesh)` → `Uint8Array`
  (`render/mesh-emitter.ts:17`) and `meshGate(mesh, minFeature)` (`kernel3d`, floor
  `DEFAULT_MIN_FEATURE_MM = 1.2`) are **already public core exports** — the CLI uses them, the
  web just hasn't yet. Core is pure ESM TypeScript with no Node built-ins on the evaluation
  path, so it bundles into a static page. The studio's 3D preview is a dependency-free
  Canvas-2D painter (`main.ts` `drawOrbMesh`/`setupOrbCanvas`) — no three.js anywhere.

### 2.1 Required engine extension — `param` declarations (decided 2026-07-26)

The knob-binding mechanism is **DSL-native variable declarations** — the OpenSCAD-Customizer
model, chosen over a Lab-side code-gen layer during design review:

```bkr
param radius = 60 range 40..110 step 5
param inner = 38 range 16..58
param shoulder = 60 range 48..76
```

- New `param <name> = <value> [range <min>..<max> [step <s>]] [advanced]` statement.
  Range/step are **first-class DSL syntax** (decided — not OpenSCAD-style annotation
  comments, not Lab-side tables), so scripts are self-describing and studio + Lab read
  identical metadata. The optional `advanced` flag sorts the knob under the UI's collapsed
  "advanced" disclosure (decided: present from day one, §11).
- Bodies reference declared params as `$name`. The expression plumbing already exists —
  `NumericExpr` has a `var` type with const-eval bindings (`parser.ts:178-195`), today bound
  only by `for $v in a..b` loops; `param` adds the missing declaration form.
- Orb-level statements (`radius`, `struts width/depth`, `weave amplitude`) currently parse
  bare positive numbers and must learn to accept `$name`/expressions.
- Embedders need a **param-override entry point** (e.g. `compileToGeometry(source,
  { params })`) so the Lab can drive sliders without textually rewriting source on every
  drag — exact API is an engine-milestone detail (M5, §10).
- **Cross-param constraints stay out of the DSL** (v1 decision): `inner < shoulder − 8` and
  `amplitude ≥ (depth + 0.4)/2` live in the shared knob layer (§8) — constraint expressions
  in the language are a bigger feature than v1 needs.
- The committed orb scripts are refactored with param headers and become the archetype
  templates themselves (§3); geometry at declared defaults must stay byte-identical
  (golden-STL check).
- Authoring guardrails (decided): a `.claude/skills/bikar-dsl` skill (grammar, param
  conventions, cross-face closure rules) and a pre-commit/npm **mesh-gate check on changed
  `.bkr` files** so humans and agents both get edit-time validation.

---

## 3. Archetype templates

An **archetype** = a param-headed `.bkr` script (§2.1) — the committed, qiyas-validated
reference orbs themselves, refactored to declare their tunables. The knob schema *is* the
script's param block; per-base constants (divide counts/offsets, contact points) remain
literal in each script body, which is why each archetype × base cell is a separate verified
script rather than one script with a base picker. A cell ships enabled only when a verified
script exists behind it.

### v1 archetypes

| Archetype | Recipe | Distinct look | Reference orbs |
|---|---|---|---|
| **Rosette** | 2 kite petals per wedge (corner + edge-midpoint contacts), shoulder ring 2N, inner ring 2N → pierced 2N-star core | classical rosettes, petal-tip welds across edges | Rosette-Orb (dodeca, qiyas 0.954), Rosette-Cube-Orb (cube, 0.975) |
| **Rosette Weave** | midpoint-only kites, shoulders under corners, no `edges from` → all even-degree nodes + `weave` | interlaced closed ribbons (chainmail) | Rosette-Weave-Orb (dodeca, 1.000, 10 strands) |
| **Star (hexagram)** | inscribed star polygons per face (`connect every k`) | crisp geometric star field | Star-Orb (icosa), Dodeca-Orb, Star-Cube-Orb ({8/3}, 1.000), Star-Octa-Orb (0.992), Star-Tetra-Orb (1.000) |
| **Hankin star** | `hankin angle θ [delta δ]` polygons-in-contact | authentic PIC stars; θ sweeps acute→obtuse families | Hankin-Orb (dodeca, qiyas 1.000, θ knob 18–80°) |
| **Classic weave** | hexagram lattice without face edges + `weave` | great-circle chainmail | Weave-Orb (icosa, 26 strands), Weave-Dodeca-Orb ({5/2} chords, 1.000, 10 strands) |

Archetype × base compatibility matrix (✅ verified · 🔬 needs calibration sweep · ✖ rejected):

| | tetra | octa | cube | dodeca | icosa | icosa sub 2–4 |
|---|---|---|---|---|---|---|
| Rosette | 🔬 | 🔬 | ✅ | ✅ | ✖ (corner/midpoint radius ratio too extreme) | ✖ |
| Rosette Weave | 🔬 | 🔬 | 🔬 | ✅ | ✖ | ✖ |
| Star | ✅ (P1: 1008 tris, 28.1 cm³, qiyas 1.000) | ✅ (P1: 2016 tris, 34.6 cm³, qiyas 0.992¹) | ✅ (P1: {8/3} octagram, 3168 tris, 38.6 cm³, qiyas 1.000) | ✅ | ✅ | ✅ (measured: sub 2 = 20160 tris, 73.9 cm³) |
| Hankin | 🔬 | 🔬 | 🔬 | ✅ (P1: 2160 tris, 24.2 cm³, qiyas 1.000; θ envelope below) | 🔬 | 🔬 |
| Classic weave | 🔬 | 🔬 | ✖ (odd-degree risk) | ✅ (P1: {5/2} midpoint chords, 10 strands, euler 0, qiyas 1.000) | ✅ | 🔬 |

¹ Star-Octa's 0.992 is a warn-severity shape-count mismatch on the vertex-4 view (encoded 17
regions vs 16 declared) — a known qiyas encoder quirk at 4-fold tangencies, not a geometry
error; the composite still clears the 0.95 gate.

Hankin θ calibration (2026-07 sweep): at the default R=60/w=3 the gate passes θ ∈ 10..84
(θ=6 hard-errors with inset degeneracy), but the envelope narrows at the range corners —
R=40 needs θ≥14 and w=6 needs θ≥18. All four (θ=18|80) × (R=40|110) × (w=6|1.5) corner
combos pass, so the shipped declared range is **18..80 step 1, default 54** (detents:
36 / 54 ideal / 72).

Unverified cells ship **disabled** (grayed with a "not yet calibrated" tooltip), not hidden —
the matrix itself communicates the roadmap. Calibration = run the CLI sweep harness (already
scripted this session) + qiyas orb-validate, then flip the cell.

Every committed gallery orb becomes a **preset chip** in the Lab (eleven as of P1): clicking
one sets every knob (and thus the URL) to reproduce it exactly.

---

## 4. Knob taxonomy

Two tiers: **global knobs** (every archetype) and **archetype knobs** (pattern-level params
declared in each script's param block, §2.1). Knob names in the UI and URL are the param
names the scripts declare.

### 4.1 Global knobs

| Knob | UI | Range / values | Measured notes |
|---|---|---|---|
| Archetype | icon cards | §3 list | changes which archetype knobs show |
| Base solid | icon row (5 solids) | matrix-gated per archetype | drives petal count N = face sides |
| Subdivision | stepper 1–4 | icosa-only; hidden otherwise | tris ×~4/level; worker + spinner needed at 3–4 |
| Radius | slider 40 mm → print-target ceiling | default 60 | ceiling = fits-in-build-volume (§6.5); inset-degeneracy margin grows with R (§5) |
| Projection | toggle spherical/faceted | 2 values | measured: faceted works everywhere, crystalline look, ~20 % less volume |
| Strut width | slider 1.5–6 mm | measured all-PASS at R=60 | wider struts shrink the valid pattern range (inset ∝ width/R) |
| Strut depth | slider 1.2–4 mm | floor = mesh-gate min feature 1.2 | also the weave ribbon thickness |
| Weave | toggle (weave-capable archetypes only) | on/off | switches family; disables strut-lattice-only knobs |
| Weave amplitude | slider, **min = (depth + 0.4)/2** | default 1.6 at depth 2.4 | see §5 — the gate does *not* catch interpenetration |
| Print target | machine dropdown + custom X/Y/Z | Bambu X1C/P1S/A1/A1 mini, Prusa MK4/Core One, Ender 3, SLS/MJF services, Custom | **not a design knob** — localStorage, never in share URLs (§6.5); sets the radius ceiling + process guidance |

### 4.2 Rosette archetype knobs (measured envelope)

Baseline: dodeca, R=60, struts 3×2.4, inner 38, shoulder 60 (pattern units, face
circumradius = 100).

| Knob | Gate-valid | UI range | Behavior |
|---|---|---|---|
| Inner ring (star-core size) | 16–58 | **24–50**, hard-clamped `< shoulder − 8` | 20 = long dramatic petals/tiny core; 50 = chunky open center; > shoulder silently inverts petals (bowtie) — gate does not catch it |
| Shoulder ring (petal width) | 48–76 | 48–76 | ≥ 82 hard-errors with the engine's own actionable inset-degeneracy message (§5) — surface verbatim |
| Petal count | derived | read-only chip | = 2N from base (cube 8, dodeca 10) — shown, not dialed |

Two sliders alone already span six visually distinct styles (sweep contact sheet rendered
this session); adding base, projection, struts, and weave multiplies that into thousands of
distinguishable valid orbs.

Literature grounding: Kaplan & Salesin's Najm system (TOG 2004) gives the rosette exactly
**three** degrees of freedom — contact angle θ, a *multiplicative* shoulder-position factor
h (default 1 = Lee's ideal rosette), and a petal-taper angle φ (default 0), with defaults
sitting at the ideal-rosette values. Our inner/shoulder ring radii are the bikar-native
analogue of that (θ, h) space, and confirm two-to-three knobs per motif is the historically
grounded budget (a nine-parameter method exists in the literature and is the cautionary
tale — diminishing returns past ~4 knobs per motif). Slider defaults should reproduce the
committed reference orbs exactly, the way Najm defaults reproduce Lee.

### 4.3 Star / Hankin archetype knobs

- Star: point count k for `connect every k` (validity depends on face N — constants table),
  optional inner-ring scale. (Taprats precedent: star (n/d)s with *real-valued* d ∈ [1, n/2)
  and integer truncation s — real-valued d is a candidate future slider if the engine grows
  it; v1 keeps integer k.)
- Hankin: **contact angle θ as the hero slider, with detents at the "natural" angles**
  k·180°/n of the face polygon, labeled with Bonner's family names — **acute / median /
  obtuse** (4/8 system acute = 45°, 5/10 = 36°, 6/12 = 30°; Bonner's crossing angle =
  180° − 2θ). Kaplan's PIC paper sweeps exactly this knob for its worked examples (e.g.
  θ = 22.5°/45°/67.5° on one tiling), confirming θ as the single highest-leverage continuous
  knob per tiling.
- Hankin delta δ ∈ [0, shortest-edge length]: splits each contact point in two → Bonner's
  **two-point** family (θ conventionally near 45° there). Ship as an "advanced" disclosure
  knob.
- The parser enforces **no ranges** on θ/δ (`parser.ts:1985-2001`) — the valid envelope per
  base must come from a calibration sweep before the archetype ships. Done for dodeca in P1:
  the measured envelope and shipped 18..80 range are recorded under the §3 matrix. Note the
  literature warns of *aliasing*: different (tiling, θ) pairs can produce the same pattern,
  so calibration should also dedupe visually identical detents.

### 4.4 Weave archetype knobs

- Amplitude (global knob, clamped as above). Clearance readout: `2·amplitude − depth` shown
  live in mm ("ribbon gap: 0.8 mm ✓ / fused ✗").
- Ring radii (rosette-weave): same inner/shoulder sliders, same envelope until a dedicated
  weave sweep says otherwise.
- Strand count is emergent — display it (from mesh connected components or provenance) as a
  delight metric ("10 interlocked ribbons").
- Print-physics grounding: Kaplan (Bridges 2017) notes classic strand-by-strand interlacement
  "would fall apart" as a print when strands are disconnected. Our ribbons are separate
  closed loops but *topologically interlocked* (chainmail), which prints pre-assembled on
  powder processes — the Lab's print-notes panel should state the SLS/MJF-only guidance for
  weave orbs explicitly.

---

## 5. Validity model — three tiers

**Tier 1 — UI clamps (silent-invalid prevention).** The mesh gate passes some visually/
physically wrong orbs; the UI must make these unreachable:
- `inner ≥ shoulder` → petals invert (bowtie). Clamp `inner ≤ shoulder − 8`.
- Weave `amplitude < (depth + 0.4)/2` → ribbons interpenetrate/fuse (gate is per-tube and
  blind to tube-tube contact; measured: amp 1.0 at depth 2.4 = −0.4 mm clearance, passes).
  Clamp the slider minimum, recompute when depth changes.
- Strut depth < 1.2 mm → would fail the mesh-gate feature floor; clamp rather than error.
- Radius above the print-target ceiling (§6.5) → clamp the slider max, not the design: a
  *shared* design bigger than the viewer's build volume still renders, flagged "exceeds your
  print target". Weave archetypes on an FDM target get a "powder process required" notice
  rather than a hard block.
- These cross-param constraints live in the shared knob layer (§8), not the DSL (§2.1) —
  per-param ranges are the script's job, relationships between params are the UI's.

**Tier 2 — engine hard errors (surface, don't hide).** Some knob corners can't be cheaply
predicted; the engine's messages are already user-actionable — show them verbatim in an error
panel with the offending knobs highlighted:
- Inset degeneracy: `void 0 (3 sides, area 85.7 pattern-units²) degenerates at strut
  half-width inset 3.01 pattern units — reduce struts width or enlarge the orb radius`
  (measured at shoulder ≥ 82) → highlight strut-width + radius knobs.
- Manifold-gate failure (`…pattern edges must meet the face polygon's edges at points shared
  by adjacent faces`) → should be unreachable from templates; treat as a template bug, log it.
- Weave family errors (degree ≠ 2/4, odd crossing count, odd alternation cycle, collapsed
  edge at small radius) → reachable via radius/pattern-density corners; map each to the knob
  that moves it (e.g. collapsed edge → "increase radius or reduce subdivision").

**Tier 3 — mesh-gate readout (trust panel).** After every successful evaluate, run
`meshGate` in-browser and show: watertight ✓, triangle count, volume cm³, min feature vs
1.2 mm floor, strand count for weaves. The STL button stays disabled unless the gate passes —
"every downloadable orb is printable."

---

## 6. URL state sync

### 6.1 Parameter schema (knob mode)

With DSL params (§2.1), **URL keys are the param names the script declares** — no hand-
invented short-key table to maintain:

```
lab.html?v=1&f=rosette-dodeca&inner=42&shoulder=64
lab.html?v=1&f=rosette-weave-dodeca&amplitude=1.8
lab.html?v=1&f=star-icosa&subdivide=2&projection=faceted
```

- `v` — schema version, always present, bumped on any breaking change; loader migrates or
  falls back to defaults with a notice.
- `f` — archetype script id, one per verified archetype × base cell (§3).
- Every other key = a declared param name; values are the DSL literals.
- Omitted keys = the script's declared defaults, so preset links stay short and
  forward-compatible. A param *rename* in a shipped script is a breaking change → bump `v`
  and keep an alias map.

### 6.2 Sync mechanics

- Knob change → debounced (~200 ms) `history.replaceState` — no history spam while dragging.
- Archetype-script (`f=`) change → `pushState` (a real navigation-sized jump; back button
  returns).
- On load: parse → validate → **clamp into the valid envelope** (a shared/hand-edited URL may
  encode an invalid combo) → render; if clamped, show a "adjusted N parameters" toast.
- "Copy link" button (explicit affordance beats assuming users watch the address bar).

### 6.3 Custom orbs in the URL

When the source diverges from every shipped script: `f=custom&code=<lz-string
compressToEncodedURIComponent of the full .bkr source>`. Orb `.bkr` files are ~1–2 KB text and
compress well; if the resulting URL exceeds ~1,800 chars, warn and offer a `.bkr` download
instead of a link. Params declared *by the custom source* still work as URL keys next to
`code=` (overrides applied after parse) — custom orbs keep working sliders and shareable
knob tweaks.

### 6.4 Best-practice alignment (researched precedents)

- **Debounce numbers are not arbitrary**: browsers rate-limit history writes (~50 ms
  Chrome/Firefox, ~120 ms Safari). The standard pattern (nuqs): keep UI state instant in
  memory, debounce only the URL write (200–300 ms). Our 200 ms sits inside the norm.
- **Never mix push and replace inside one debounced drag** — a queued pushState turns the
  whole flush into a new history entry and corrupts the back button. Slider drags are
  replace-only; archetype-script changes push *outside* the debounce queue.
- **Default elision** (drop params at their default value) is the established convention —
  §6.1 already does this.
- **Compressed-source-in-URL precedents**: TypeScript Playground uses exactly
  `LZString.compressToEncodedURIComponent` (`#code/...`); mermaid.live prefixes the payload
  with its codec (`#pako:`/`#base64:`) — the prefix doubling as a version tag is the same
  role our `v=` plays. Compiler Explorer eventually added server-side short links when
  full-state URLs grew unwieldy — for us the `.bkr`-download fallback covers that case
  (static hosting, no server).
- **≤ ~2,000 chars** remains the practical shareability ceiling (legacy IE 2,083; modern
  proxies/QR/chat unfurlers are the real constraint) — our 1,800 warning threshold is
  consistent.

### 6.5 Print target — localStorage, not URL (decided 2026-07-26)

The radius ceiling derives from a **print target** picker: a dropdown of common machines with
known build volumes — Bambu X1C/P1S (256³), A1 (256³), A1 mini (180³), Prusa MK4/Core One,
Ender 3, … — plus SLS/MJF *service* presets and a **Custom** entry with manual X/Y/Z inputs.

- Ceiling math: whole sphere must fit → `2R ≤ min(X, Y, Z) − 10 mm` margin. (The FDM
  hemisphere-split variant, task #11, would relax the Z term for tall-bed machines.)
- The machine choice **implies the process**, driving guidance with zero extra knobs: FDM
  targets surface the weave "powder process required" notice and the split-export dependency;
  SLS/MJF service targets print everything as-is.
- The target is a fact about the *user's environment*, not the design — it persists in
  **localStorage and is never written to share URLs**. A recipient opening a design that
  exceeds *their* target sees it rendered normally with an "exceeds your print target" flag;
  the design is never silently shrunk.
- The machine table is maintained in the shared knob layer (§8) — a dozen entries, not a
  database; Custom covers the tail.

---

## 7. Custom orbs — knobs ⇄ code

DSL params (§2.1) dissolve the detach problem that a code-gen design would have had — there
is no cliff between knob-land and code-land (decided 2026-07-26, superseding the earlier
one-way-detach proposal):

- **Sliders bind to the param block by name, bidirectionally.** Dragging a slider updates the
  param's value (via the override entry point, reflected in the visible source); editing a
  param's value in code moves the slider. The knobs *teach the DSL* — the source is always
  visible.
- **Structural edits below the param header never disable the knobs** — they redefine the orb
  the knobs feed. Once the body diverges from every shipped script the design becomes
  `f=custom` (§6.3); its declared params keep working as sliders. **Users can declare their
  own knobs** — that is the custom-orb capability.
- Adding/removing/renaming a `param` line simply adds/removes/renames a slider on the next
  successful evaluate. A failed parse or eval keeps the last-good knob panel and preview,
  with the engine error shown verbatim (§5 tier 2).
- Evaluate/preview/STL/mesh-gate all work identically on custom source — same
  `compileToGeometry` path.
- **Open in Studio**: serializes current source into the studio (deep link to
  `/editor/#<name>`; exact transport — hash payload vs the dev pattern API — is P2 detail).

---

## 8. Studio "Dials vs Code" tab (new requirement)

Bikar studio gains an **input-mode toggle** — orthogonal to the existing *output* tabs
(3D / per-axis views):

```
┌──────────────────────────────────────────────┐
│ [🎛 Dials] [</> Code]        ← input mode    │
│ ┌─────────────┐  ┌─────────────────────────┐ │
│ │ knob panel  │  │ preview: [3D][axis tabs]│ │
│ │ or editor   │  │                         │ │
│ └─────────────┘  └─────────────────────────┘ │
└──────────────────────────────────────────────┘
```

- **Icons**: inline SVG glyphs in the tab labels — a three-slider "mixer" glyph for Dials, a
  `</>` chevron glyph for Code — matching studio's existing monochrome UI accents;
  `aria-label`s + keyboard focus states.
- Dials mode is available whenever the open file **declares params** (§2.1) — after the
  refactor that includes every starter orb. Files with no param block open in Code mode with
  the Dials tab visible but disabled (tooltip: "declare `param` values to get dials").
- With DSL-native params the planned code-gen template package shrinks to a thin **shared
  knob layer** used by both studio and Lab: read the evaluated param schema
  (names/defaults/ranges/steps come from core), render sliders, apply the cross-param
  constraint table (§5), and hold the print-target machine table (§6.5). Home (decided):
  **folded into `@naqshcoffee/ui`** — the existing shared UI package gains the knob
  components and tables; keep the knob exports tree-shakeable so the Lab bundle doesn't drag
  in unrelated studio UI. The schema vocabulary intentionally mirrors OpenSCAD Customizer
  conventions (range, step, labeled enums, groups) — familiar to the 3D-printing audience —
  but encoded first-class in the DSL rather than in comments.
- Studio keeps its own persistence (starter files/dev API); URL-param sync is a Lab feature,
  though the hash deep-link (`/editor/#Name`) continues to work.

---

## 9. Architecture

```
bikar (engine repo)                          3d-models (publish repo)
┌──────────────────────────────┐             ┌───────────────────────────┐
│ packages/core (+param stmt)  │             │ lab.html  (vendored dist) │
│ @naqshcoffee/ui (+knobs, §8) │──vite build→│   + assets                │
│ packages/lab   (new, vite)   │             │ index.html  "Open in Lab" │
│ packages/web   (+Dials tab)  │             │ Makefile: make lab        │
└──────────────────────────────┘             └───────────────────────────┘
```

- **Source of truth in bikar, deployment in 3d-models** — mirrors how `.bkr` files are already
  vendored by `make orbs`. `make lab` builds `packages/lab` and copies its dist into the
  gallery tree; `make deploy` (owner-gated, unchanged) publishes it with everything else.
  Fully static — fits gh-pages, no server.
- **Evaluation in a Web Worker.** `compileToGeometry` is fast for the committed orbs
  (2–7 k tris) but icosa subdivide 3–4 reaches ~80 k+ tris; a worker keeps sliders at 60 fps.
  Debounce knob → evaluate at ~200 ms; render the last-completed mesh while the next
  evaluates (stale-while-revalidate); spinner only when > ~300 ms.
- **3D preview**: port the studio's Canvas-2D painter (drag-rotate/wheel-zoom, flat-shaded
  gold with darker inner walls, no backface culling so piercings show the interior). v1 copies
  the ~100-line renderer into `packages/lab`; extracting a shared `@naqshcoffee/orb-viewer`
  is a P2 refactor once both consumers exist. Three.js remains unnecessary.
- **Axis views**: reuse public `symmetryViewAxes` + `projectOrbView` + `renderOrbViewSVG`
  exactly as the studio does — free validation-style 2D views as secondary preview tabs.
- **STL download**: `emitBinarySTL(result.orbMesh)` → `Blob` → anchor download, filename
  encoding the knob state (`rosette-dod-r60-in38-sh60.stl`). Gated on `meshGate` pass (§5).
- **No qiyas in-browser** — Python stays in CI; the Lab's trust story is the mesh-gate panel
  plus the qiyas-validated preset chips.

---

## 10. Phased plan

- **M5 — DSL params (bikar, prerequisite)**: `param` statement with first-class
  `range`/`step`, `$name` accepted in orb-level numbers, param-override entry point for
  embedders, refactor the six committed orbs with param headers (**geometry at defaults
  byte-identical — golden-STL check**), language-reference + decision-ledger docs,
  `.claude/skills/bikar-dsl` authoring skill, pre-commit/npm mesh-gate check on changed
  `.bkr` files.
- **P0 — Lab core** (first shippable): separate `lab.html` (decided) via `packages/lab`,
  knob UI auto-generated from the rosette scripts' param blocks (cube + dodeca) including
  the collapsed advanced disclosure for `advanced`-flagged params (decided: day one),
  print-target picker (§6.5), worker evaluate, 3D preview, URL sync (`v=1`, param-name
  keys), mesh-gate panel, STL download, `make lab` vendoring, gallery "Open in Lab" links on
  the two rosette plates.
- **P1 — breadth**: Star + weave archetype scripts, preset chips for all six committed orbs,
  calibration sweeps to flip 🔬 matrix cells (incl. the Hankin θ/δ envelope), axis-view tabs.
- **P2 — custom + studio**: `f=custom` code editing with lz-string URLs + declared-param
  sliders, Open-in-Studio handoff, studio Dials/Code tab with icons (consuming the shared
  knob layer), shared-viewer extraction.
- **P3 — polish**: strand-count/clearance readouts, "adjusted parameters" toasts, print-notes
  panel per family (SLS/MJF vs FDM guidance from the supports write-up).
- **Beyond (unscheduled, engine-gated)**: latitude-gradient contact angle (Kaplan's parquet
  deformation on a sphere), real-valued star d, girih tile presets — parked until the engine
  grows the corresponding statements.

Each phase ends with the standard verification: bikar `npm test` + `npm run ci` (modulo the
92 pre-existing prettier-dirty files), CLI-rendered STLs of Lab-generated sources byte-checked
against template goldens, qiyas orb-validate ≥ 0.95 on new presets.

### Implementation status

- **M5 shipped** (bikar `d1a0d43`): everything listed above, goldens byte-identical ×6.
- **P0 shipped** (bikar `03e7153` + `3269ab6`, 3d-models `dfae231`): everything listed
  above, browser-smoke-tested (clean boot, URL clamp round-trip + toast, script switch,
  machine-ceiling chip, unknown-`f` fallback). One deliberate deviation from §8: the knob
  layer lives inside `packages/lab` behind its own module boundary for now —
  `@naqshcoffee/ui` is an external GitHub-Packages dependency and installing into it needs
  `GITHUB_PACKAGES_TOKEN`, so the fold into the shared UI kit moves to the P2 studio work.
  Additions beyond the letter of the spec: cross-param guard rails in the Lab (tier-1
  rules `inner ≤ shoulder − 8`, `amplitude ≥ (strut_depth + 0.4)/2`), and the
  "adjusted parameters" toast (scheduled P3) landed early on the URL-load path.
- **P1 shipped** (bikar `0eab01f`): five calibration sweeps flipped five matrix cells (§3) —
  Hankin×dodeca (with the measured θ 18..80 envelope), Star×cube ({8/3} octagram),
  Star×octa, Star×tetra, and Classic-weave×dodeca ({5/2} midpoint chords, 10 strands,
  euler 0 — the odd-cycle parity risk did not materialize). All five ship as committed
  `patterns/Orbs/` scripts (spike-golden byte-identical) and gallery plates; all eleven
  committed orbs are now Lab preset chips with `f=` deep links. Lab additions: symmetry-axis
  view tabs (SVGs rendered lazily in the worker via the same `projectOrbView`/
  `renderOrbViewSVG` path qiyas validates, invalidated per result, stale-dropped by seq);
  weave trust rows (interlocked-ribbon count from a worker-side connected-component scan,
  ribbon-gap clearance `2·amplitude − strut_depth` with a ✓/fused readout); and the §5
  tier-3 FDM notice when a weave design targets a filament machine. The five new orbs also
  join the studio's Orbs starter folder. qiyas orb-validate composites: Hankin 1.000,
  Star-Cube 1.000, Star-Tetra 1.000, Weave-Dodeca 1.000, Star-Octa 0.992 (warn-severity
  shape-count quirk, §3 footnote).
- **P2 shipped** (bikar `52e7990` `59c1b8a` `bade84e` `5e51850` `228466b` `ba5ef85`, per
  `orb-lab-p2-design.md`): custom orbs + studio Dials. The knob layer moved into a
  `packages/knobs` workspace package (P2.1 — chosen over the `@naqshcoffee/ui` fold; the
  external-package token requirement stands, so the workspace package is the durable home).
  The Lab worker gained the L8 watchdog (60 s heavy tier via the L3 source sniff), an
  evaluation-generation protocol with respawn, the 64 KiB size guard, and SVG attribute
  escaping (P2.2). Custom mode (P2.3): a code drawer with gutter + debounced re-evaluate,
  verbatim engine errors beside a stale-while-revalidate last-good mesh, and "Write values
  into code" baking. Share links (P2.4): lz-string `code=` payloads under an 1,800-char URL
  budget that degrade to `.bkr` download beyond it, a localStorage draft mirror, and the
  damaged-payload toast. The studio (P2.5) gained a Dials mode (param scripts only) with
  write-through to the source line, plus the Lab→studio `#code/` handoff behind "Open in
  Studio". P2.6 hardening: the §4.3 trust badge (validated ✓ score / calibrated range /
  custom — not qiyas-validated) backed by a fresh full-sweep of Docker qiyas orb-validate
  composites recorded per script — Rosette 0.954, Rosette-Cube 0.975, Rosette-Weave 1.000,
  Star 1.000, Star-Dodeca 1.000, Weave 0.997 newly recorded; the five P1 scores reproduced
  exactly — plus ten Playwright specs (six Lab custom-mode, four studio Dials; the Lab
  preview binds :4613 so a stray default-port vite preview is never silently reused), L6
  guard-rail unit tests in `packages/knobs`, in-page authoring notes, and this repo's
  `make lab-smoke` vendoring check (asset refs + worker chunk), run inside `make lab`.

---

## 11. Decisions & open questions

### Resolved in design review (Omar, 2026-07-26)

1. **Lab placement → separate `lab.html`**, linked from the gallery header + per-plate "Open
   in Lab" links. Implication: index.html stays static/cacheable; engine bundle loads only in
   the Lab; the Lab owns its URL namespace.
2. **Radius ceiling → print-target picker** (machine dropdown — Bambu/Prusa/Ender/… — plus
   SLS/MJF service presets and custom X/Y/Z; §6.5). Implications: ceiling derives from build
   volume, process guidance (weave warnings, split-export note) comes free from the machine
   choice, target lives in localStorage and never in share URLs.
3. **Knobs↔code → DSL-native `param` declarations** ("sliders as variables"), superseding
   the one-way-detach/marker-comment options entirely. Implications: new bikar milestone M5
   (§2.1, §10); committed orbs refactored into self-describing templates; bidirectional
   slider↔code sync by construction; custom orbs can declare their own knobs; URL keys are
   param names (§6.1); the code-gen template package collapses into a thin shared knob layer
   (§8).
4. **Param ranges → first-class DSL syntax** (`param inner = 38 range 16..58 step 1`), not
   annotation comments, not Lab-side tables. Implication: scripts are self-describing;
   studio and Lab can never disagree about a knob's bounds.
5. **Authoring guardrails → both**: a `.claude/skills/bikar-dsl` skill (grammar + param
   conventions + closure rules) and a pre-commit/npm mesh-gate check on changed `.bkr` files.

6. **Shared knob layer home → fold into `@naqshcoffee/ui`** (chosen over a new workspace
   package). Implications: the existing shared UI package gains the knob components plus the
   cross-param constraint and machine tables; the Lab bundle takes a dependency on
   `@naqshcoffee/ui`, so its knob exports must stay tree-shakeable to keep studio-only UI
   out of the Lab page.
7. **Advanced knobs → disclosure from day one** (chosen over curated-v1). Implications: the
   `param` statement carries an `advanced` flag (§2.1); scripts may expose less-calibrated
   extras under the collapsed disclosure immediately; accepted trade-off — advanced knobs
   will hit tier-2 engine errors more often, with the verbatim error panel as the safety net,
   and calibration sweeps promote knobs out of advanced over time.

### Still open

None — all design-review questions are resolved (2026-07-26).

---

## Appendix A — prior art (researched 2026-07-26; primary sources read in full)

**Islamic-pattern parameterization**
- Kaplan, *Islamic Star Patterns from Polygons in Contact* (GI 2005): Hankin's method
  exposes tiling (discrete, biggest lever), contact angle θ (continuous — worked examples
  sweep e.g. 22.5°/45°/67.5°), two-point offset δ ∈ [0, shortest edge], plus second-pass
  inference and contact-position adjustment booleans. Also: *parquet deformations* (θ varying
  spatially — a future latitude-gradient knob for orbs) and the rosette transform (source of
  (tiling, θ) aliasing).
- Kaplan, *Computer Generated Islamic Star Patterns* (Bridges 2000, the taprats paper):
  motif family per tiling polygon — star (n/d)s with real d ∈ [1, n/2) and integer
  truncation s; rosette (Lee 1987 construction, one natural sliding DOF); extended rosette;
  render styles plain/outline/emboss/interlace/checkerboard.
- Kaplan & Salesin, *Islamic Star Patterns in Absolute Geometry* (TOG 2004, Najm): rosette =
  exactly (θ, shoulder factor h, taper φ) with defaults reproducing the ideal rosette — the
  direct ancestor of our inner/shoulder knob pair.
- Bonner & Kaplan (Bridges 2012): acute/median/obtuse/two-point families = crossing-line
  angles at polygon edge midpoints; natural angles are multiples of 180°/n (4/8: 45°,
  5/10: 36°, 6/12: 30°, 7/14: 51.43°…); crossing angle = 180° − 2θ. Basis for slider detents.
- Lu & Steinhardt (Science 2007) / girih tiles: five tiles, strapwork frozen at 54° to each
  edge (fivefold median family) — girih is combinatorial (tile arrangement), arguing for
  presets, not sliders; consistent with keeping girih out of v1.
- arXiv 1809.09270 (nine-parameter star method): the diminishing-returns cautionary tale.
  Survey: npj Heritage Science 2022 review of computational IGP methods.

**Configurator UX precedents**
- Kaplan, *Interwoven Islamic Geometric Patterns* (Bridges 2017): the closest academic
  precedent to bikar's orbs (weave folded onto polyhedra → bulged spherical → radial
  extrusion; 3D-printed truncated-icosahedron star sphere). Not distributed; **no browser
  Islamic-pattern sphere configurator exists** — nearest live tools are 2D generators and
  static STL uploads.
- OpenSCAD/Thingiverse Customizer: comment-annotation grammar for knob declaration
  (`// [10:100]`, labeled enums, `/* [Tab] */` groups, JSON presets) — adopted as our
  knob-schema vocabulary (§8).
- MakerWorld Parametric Model Maker: in-browser OpenSCAD with auto-generated UI — validates
  the tweak → live 3D preview → download loop as the winning UX.
- Nervous System *Cell Cycle* (2012–): the canonical browser mesh configurator — continuous
  sliders bound to a live 3D mesh + save/load/share of designs.

**URL-state precedents**
- nuqs / redux-query-sync patterns: instant in-memory state, debounced URL writes (browser
  history rate limits ~50–120 ms), replace-for-drag / push-for-navigation, default elision.
- TypeScript Playground (`#code/` + lz-string `compressToEncodedURIComponent`), mermaid.live
  (`#pako:` codec-prefix-as-version), Compiler Explorer (outgrew full-state URLs → server
  short links), Excalidraw (documents move server-side past a size threshold; URL holds a
  pointer). Practical shareability ceiling ≈ 2,000 chars.

## Appendix B — measured sweep data (2026-07-26, bikar f9eab09)

Baseline Rosette-Orb, dodeca, R=60 mm, struts 3×2.4 mm, inner 38 / shoulder 60.

| Sweep | Values tried | Result |
|---|---|---|
| Inner ring | 16, 20, 24, 38, 50, 58, 62 | 16–58 gate-PASS; 62 (> shoulder) passes but inverts petals — silent-invalid |
| Shoulder ring | 48, 60, 70, 76, 82 | 48–76 PASS; 82 hard EvalError (inset degeneracy, actionable message) |
| Strut width | 1.5, 3, 6 mm | all PASS; volume 25.4 → 78.4 cm³ |
| Weave amplitude | 1.0, 1.6, 2.6 | all gate-PASS incl. physically-fused 1.0 → gate blind to tube-tube contact |
| Projection | faceted | PASS; 37.6 vs 47.0 cm³ spherical |
| Subdivision | icosa sub 2 (Star archetype) | PASS; 20160 tris, 80 faces, 73.9 cm³ |

Strand count check: Rosette-Weave-Orb STL → union-find on vertex-shared triangles → 10
components = 10 closed interlaced ribbons.
