<!--
  Research produced 2026-09-26 by a research subagent (Claude Opus 5.5) under
  the 3d-models design-doc rules (K1, K2, K7, K10).
  Produced-by: research subagent, from Omar's question (quoted in §1).
  Feeds: a future coaster-lettering design doc (not yet written).
  Sources: a read of bikar at origin/main 2026-09-26 (paths and line numbers
  below are at that ref); this repo's text-emit and coaster docs; and the web
  sources in §9, fetched 2026-09-26. Web sources are shop or vendor guidance,
  never a measurement of ours.
  NOTHING WAS PRINTED, no slicer was run, and no font was baked. Every
  print-outcome claim below is either quoted guidance (hedged as the source
  hedges it) or simple arithmetic on a stated shape, labelled as such.
-->

# Bubble lettering on coasters — what it would take

## 1. Question

Omar, 2026-09-26: *"what would it take to overlay a SKIMS-like bubble 3D font or letters on the
coasters? Either on the top face or side edges. This should be doable from Coaster Lab."*

"SKIMS-like bubble" here means puffy, inflated-looking letters — soft domed strokes, like a
balloon or a pillow — not flat letters pushed straight up. The SKIMS mark itself is a custom
logotype, not a font anyone can license: one font-lookalike vendor says "The Skims font is a
custom logotype designed for the Skims brand" ([mojomox](https://mojomox.com/skims-font)). A
logo-history page describes a flat version and a "voluminous version" whose letters look "made of
silicone mass, slightly spread across the surface"
([1000logos](https://1000logos.net/skims-logo/)). So the target is the *look* — a rounded, fat
letterform with a soft dome on top — not the SKIMS letters themselves, which we should not copy.

Short answer: **the top face is a modest extension of machinery bikar already has; the side
edges are a new kind of geometry and should wait.** §4 says why.

## 2. Findings — what exists today

### 2.1 Text in bikar

bikar has one text path, built for engraving rung labels on calibration pieces
([text-emit-design.md](../text-emit-design.md)).

| Piece | Where (bikar `origin/main`) | What it does |
|---|---|---|
| One baked face | `packages/core/src/kernel3d/glyph-data.ts` line 34, `SOURCE_CODE_PRO_BOLD` | Source Code Pro Bold 2.042 outlines, flattened to closed rings at cap height 1.0. **37 glyphs only:** `0–9`, `A–Z`, `-` (space is handled as an advance, not a glyph). No lowercase, no punctuation. |
| The bake script | `scripts/bake-glyphs.py` | Reads any `.ttf`/`.otf` with fontTools and writes a TypeScript constant. Already takes a font path, `--axis TAG=VALUE` for variable fonts (line 623), `--alt` for alternate glyphs, and `--allow-crossings` (line 644) for test fixtures only. |
| Bake-time checks | `packages/core/src/kernel3d/glyph-checks.ts` line 231, `checkGlyphFace` | B1: no two contours cross. B2: nesting depth. B3: rounding. A face with overlapping contours fails B1, because the extrude path has no union. |
| Layout | `packages/core/src/kernel3d/text-layout.ts` line 186, `layoutLabel` | Places glyphs in mm, applies kerning, and throws on a character the face lacks. |
| Legibility floors | same file: `MIN_LABEL_GAP_MM` 0.4 (line 96), `MIN_COUNTER_MM` 0.4 (line 117), `LABEL_CAP_MM_CAL` 5.0 mm (line 34, bet `CAL-TXT-02`), `LABEL_RELIEF_MM_CAL` 0.6 mm (line 56, bet `CAL-TXT-01`) | The gap and counter floors are one nozzle width. The 5.0 mm cap and 0.6 mm depth are provisional bets — no label has been printed. |
| Confusables check | same file line 468, `CONFUSABLE_PAIRS` (just `0`/`O`) | Refuses a label (or label set) that could be misread. |
| Extrusion | `packages/core/src/kernel3d/solidify-piece.ts` line 664, `solidifyText` | **Engrave only**: cuts the label into the flat top of an `extrude` piece. |
| Grammar | `packages/core/src/dsl/parser.ts` line 2216, `parsePieceText`; AST `PieceTextNode` at `packages/core/src/dsl/ast.ts` line 360 | `text "<label>"` with optional `at`, `cap`, `engrave` — **only inside a `piece`**, and the parser refuses it on anything but an `extrude` piece (parser line 2097). |

### 2.2 The coaster kernel

A coaster is a **height field**: a flat bottom, and a top surface whose height at each (x, y) is
`base + relief + rim`, sampled on a grid (`packages/core/src/kernel3d/coaster.ts`, header comment
and `buildCoaster` at line 2017). The grid pitch is one perimeter width, 0.4 mm (line 185). There
is no boolean union anywhere; the solid is closed by construction.

Two things already in that kernel matter a great deal here:

- **Rounded straps already exist.** `relief … rods` gives a strap a half-round cross-section:
  height `h·√(1−(d/r)²)` at distance `d` from the strap centreline, falling to zero at the edge
  (`strapAmountAt`, line 694; `shape: 'band' | 'rod'`, line 229). Where two straps meet, the
  kernel takes the higher of the two, so crossings blend into a smooth dome with no union. That is
  the "puffy" profile, already computed, already printable as far as the kernel's gates go.
- **A grid distance calculation already exists** in the validators
  (`packages/core/src/kernel3d/coaster-validate.ts` line 359, `distanceToPockets`). A dome over a
  filled letter shape needs exactly this kind of "how far is this grid point from the edge"
  number.

### 2.3 The gaps between that and bubble letters

1. **No text on a coaster at all.** `text` is a `piece` statement; `CoasterDeclarationNode`
   (`ast.ts` line 637) has no text field.
2. **Engrave only, flat only.** The one text path cuts down into a flat face; nothing raises
   letters, and nothing domes them.
3. **Wrong face for the look.** Source Code Pro Bold is a monospaced coding face. A bubble look
   needs a fat, rounded display face, which means baking a second face.
4. **Bubble faces will likely fail B1.** Display and variable fonts commonly ship with overlapping
   contours (the check exists because the extrude path cannot handle them). *Not measured for any
   candidate below* — §8 phase 0 measures it. The height-field route in §3 does not care, because it
   fills the letter on the grid rather than building an outline polygon.
5. **Knobs are numbers only.** `ParamSpec` (`ast.ts` line 910) carries a number, and the knob
   panel's `onChange` takes `(name, value: number)` (`packages/knobs/src/knobs.ts` line 20). A
   text box and a font picker have no `param` to hang on. The Lab already has the pattern for
   this: the colour knob (`packages/lab/src/coaster-colors.ts`) and the band/rod toggle
   (`packages/lab/src/coaster-relief-shape.ts` line 56) edit the DSL source directly instead.
6. **No "text" colour region.** `CoasterRegion` is exactly `'base' | 'straps' | 'border'`
   (`ast.ts` line 573).
7. **Side edges are not a height field.** The coaster wall is built by dropping each outline loop
   straight down from the top to the bottom. Letters on the wall are bumps sideways, which
   `z = f(x, y)` cannot describe. The only existing coaster geometry that varies the outline with
   height is the twist, which lofts a ring solid instead of a height field
   (`coaster.ts` `twistDeg`; bikar `docs/design/coaster-twist-extrude.md`).

## 3. Options compared — how to get the bubble look

| Option | How | Pros | Cons | Implications |
|---|---|---|---|---|
| **A. Pillow height field over an outline font** (recommended) | Bake a rounded display face. Lay out the word. Fill the letter shapes on the coaster's 0.4 mm grid; compute each grid point's distance `d` in from the letter edge; add height `h·√(1−(1−min(d,s)/s)²)`, where `s` is a "roundness" radius. Wide strokes get a flat-ish top with rounded shoulders; narrow strokes become a full dome. | Fits the kernel's existing shape (one more height contribution, like rods). No union, no polygon offset, overlapping contours do not matter. Blends with straps by the same "take the higher" rule. Profile is one formula, so puff and roundness are two numbers — easy knobs. | New code in the kernel (letter fill + distance on the grid). The letter edge is only as sharp as the 0.4 mm grid. Needs a second baked face. Dome tops will show layer steps (§3.1). | Commits us to top-face lettering only. Adds a `text` statement to the coaster block and, later, a `text` colour region. Reuses the bake script and layout code as they are. |
| **B. Tube letters from a single-stroke font + existing `rods`** | Feed a single-stroke (Hershey-style) font's centre lines to the coaster as strap centrelines, with `relief … rods`. | Almost no new kernel code: rods already make half-round tubes and blend joins. | The look is neon tube or balloon-animal, not a fat pillowy letter. Stroke width equals strap width everywhere — no fat/thin. [text-emit-survey.md](text-emit-survey.md) found the single-stroke route needs a polygon offset *for an extruded piece*; that finding does not transfer here because the height field never builds an outline polygon — it only thresholds distance on a grid. | A quick look-alike, not the SKIMS look. Worth a render in phase 1 as the cheap comparison. |
| **C. Stacked shrinking layers** | Extrude the letter, then extrude smaller and smaller insets on top (a terraced dome). | Easy to picture; each step is flat, which FDM prints well. | Needs a reliable polygon inset of glyph shapes with holes — the survey measured that offsets of glyph shapes break. The printer terraces a smooth dome anyway, so pre-terracing adds nothing. | Rejected in favour of A, which gets the same printed result without the inset. |
| **D. OpenSCAD `minkowski` (text ⊕ sphere)** | `linear_extrude(text())` then round it with a sphere. | Known technique, true 3D rounding, any installed font. | Lives outside bikar, so Coaster Lab cannot drive it; minkowski on text is slow; bikar has no boolean union to merge the result with the coaster. | Would fork the pipeline (one coaster path in bikar, one in OpenSCAD). Out, per the repo's "no fork" rule (D-041, D-052). |
| **E. Import a ready-made puffy mesh** | Make the word in a 3D tool (inflate/cloth sim) and merge the mesh. | Best possible look for a one-off. | Not parametric, not in the DSL, not in the Lab, needs a mesh union. | A one-off gift path only; does not answer "from Coaster Lab". |
| **F. Flat raised letters with a rounded top edge** | Raise the letters flat, then round only the top edge. | Closest to what exists; flat tops iron well. | Reads as "rounded sign lettering", not puffy. | Falls out of option A for free: a small roundness `s` on a wide stroke gives exactly this. So F is a setting of A, not a separate build. |

### 3.1 How each prints on FDM (0.4 nozzle, 0.2 mm layers)

- **Layer steps on the dome.** A curved top is printed as a staircase of flat layers; guidance
  says steps show "on spheres, domes, and broad arcs" and can be reduced but "can't be completely
  eliminated" ([Chitu Systems](https://www.chitusystems.com/blogs/articles/why-your-curved-3d-prints-look-rough-and-how-to-fix-them),
  [UltiMaker community](https://community.ultimaker.com/topic/32990-reducing-stair-stepping-effect-on-round-surfaces/)).
  *Arithmetic, not a print:* a half-round dome 1.2 mm high over a 4 mm stroke is six 0.2 mm
  layers; its top layer is a flat patch about 2.2 mm wide (`2·2·√(1−(1.0/1.2)²)`), and the lower
  steps are nearly vertical. So the dome will read as a soft terrace, not a glossy balloon.
- **Variable layer height helps.** Bambu Studio has a variable-layer-height tool described as
  improving "models with spherical tops or slopes", with an adaptive mode and a smoothing mode
  (Bambu Lab wiki, [Variable Layer Height](https://wiki.bambulab.com/en/software/bambu-studio/adaptive-layer-height) —
  read via search snippet; the page itself returned HTTP 402 to our fetcher). A coaster is short,
  so finer layers only over the dome band cost little time. Untested here.
- **Ironing does not help domes.** One vendor guide: ironing "relies on flat, horizontal planar
  contact. On sloped roofs or organic dome geometry, the nozzle cannot maintain flat contact,
  resulting in severe stair-step dragging and material burning"
  ([Sovol](https://www.sovol3d.com/blogs/news/ironing-in-3d-printing-settings-for-smoother-top-surfaces)).
  The same guide lists coasters as good ironing candidates — for their flat tops. So: iron the
  slab, not the letters, if at all.
- **Stroke width at the nozzle.** Bubble faces are fat, which helps: the kernel's strap floor for
  a strap on a slab is 0.8 mm (`STRAP_WIDTH_MIN_MM_CAL`, `coaster.ts` line 76, provisional). The
  risk is the reverse — **counters and gaps closing**. Fat letters leave small holes (the eye of an
  `A`, the bowl of `B`) and tight gaps between letters. `MIN_COUNTER_MM` and `MIN_LABEL_GAP_MM`
  (both 0.4 mm) were set for Source Code Pro engraving; whether they carry to domed letters is
  open. They transfer only if a domed letter's gap is measured at the base, where the domes meet,
  since that is where two beads would fuse. With a dome falling to zero at the edge, adjacent
  letters touch at the base and a gap becomes a shallow valley — which is part of the SKIMS look,
  but also how a counter silently fills in.
- **The 5 mm cap bet does not transfer.** `CAL-TXT-02` (5.0 mm) is a floor for Source Code Pro
  Bold's thinnest stem (0.573 mm at that cap). A different face has different stems and counters;
  its floor has to be measured from its own outlines (phase 0), not ported.

## 4. Placement

### 4.1 Top face (recommended first)

A cup sits on the top face, and that constrains everything:

- **Cup wobble.** Plain coasters already raise straps 1.2 mm (`relief straps emboss 1.2` in e.g.
  bikar `patterns/Constructions/GimTvN9hw4U-coaster.bkr`). Letters taller than the straps become
  the only thing the cup rests on. Either keep puff at or below the strap relief, or keep the
  letters out of where a cup sits (a ring near the edge, or the border band). Cup base sizes were
  not measured for this file.
- **Letters vs the pattern.** Three ways to combine them, all expressible as height-field rules:
  1. **Overlay:** letters ride on top of the pattern (take the higher). Cheapest; a busy rosette
     under the letters may hurt legibility.
  2. **Knock-out pad:** flatten the relief inside a margin around the letters, then add the letters
     on the flat. Cleanest read; hides part of the pattern.
  3. **Band:** letters inside a `border` band or a blank ring. The existing `border` width is 3–15
     mm (`param border … range 3..15` in the border coasters), so a 3 mm wide band cannot hold much
     cap height; a wider blank margin would.
- **Openwork and minimal styles need a solid pad.** On `openwork` coasters the slab is cut away
  between straps (bikar `docs/design/coaster-openwork.md`); on minimal (`outline pattern`)
  coasters there is no slab at all. Letters over a hole would float. A text pad — "keep this
  region solid" — is needed: the letter footprint grown by a margin, exempt from the openwork cut.
  How wide that margin must be is open. The free-standing strap floor `CAL-CST-07` (1.6 mm,
  [coaster-minimal-design.md](../coaster-minimal-design.md)) is for a lone strap standing on its
  own; it transfers to a pad rim only if the pad rim is likewise a free-standing strip with
  nothing beside it, which depends on the pattern under it. Not assumed here.
- **Raised vs inset.** Raised domes are the SKIMS look. An inset (debossed) bubble reads as a
  mould, not a balloon — possible with the same formula and the sign flipped, but not what was
  asked.

### 4.2 Side edges (later, if at all)

- **Very little room.** The coasters are `base 4` (4 mm slab) plus relief on top. The side wall is
  about 4 mm tall, less any chamfer or fillet. Lettering there is around 3 mm cap at most — well
  under the 5 mm cap bet for the only face we have measured, and unmeasured for any other.
- **Faceted vs round.** The hexagon outlines at 90 mm across flats have ~52 mm straight sides
  (`90/√3`), enough for a short word per face. A round outline would need the text bent along the
  curve.
- **Print orientation.** Coasters print flat, face up, so the side wall is vertical. A dome on a
  vertical wall overhangs on its underside. *Arithmetic:* for a half-round bump of radius R, the
  bottom `R·(1−sin 45°) ≈ 0.29 R` of it is steeper than 45° from vertical. Guidance on embossing
  vertical walls says to minimise overhangs and, for complex text, to prefer "an embedded technique
  with no overhangs or outcroppings. Printed in two colors, the effect is essentially the same"
  ([Cubify fans blog](http://cubifyfans.blogspot.com/2015/01/considerations-for-embossing-3d-printed.html)).
  A teardrop-shaped letter profile (flat 45° underside, round top) would avoid the worst of it;
  the 45° number is itself a provisional bet in this kernel (`TWIST_MAX_LEAN_DEG`), not a measured
  one, and its source says not to port an older overhang number.
- **New geometry.** The height field cannot hold it (§2.3 item 7). It needs a wall that bulges
  sideways with height — closer to the twist loft than to the height field. That is a separate,
  larger design.

## 5. Coaster Lab surface

Coaster Lab builds its knob panel from a script's `param` block
(`packages/lab/src/coaster-scripts.ts` line 52 and the comment above it), and edits the DSL
directly for anything that is not a number (colour, band/rod). Lettering follows both patterns:

| Knob | Kind | Maps to |
|---|---|---|
| Text | text box | a source rewrite of `text "…"` inside the coaster block — the same pure string-to-string style as `coaster-colors.ts`, unit-tested apart from the page |
| Font | picker over baked faces | a rewrite of a `font <name>` word on the `text` statement; only faces that are baked and passed the checks are offered |
| Size | slider | `param text_cap = … range …` → `cap $text_cap` |
| Puff | slider | `param puff = … range …` → dome height in mm |
| Roundness | slider, advanced | `param round = …` → the `s` radius in option A |
| Placement | picker (centre / band / offset) plus x, y sliders | `at …` (already in the piece grammar) plus a `pad <mm>` margin for the knock-out |
| Colour | the existing colour control | `color text <PaletteName>`, once a `text` region exists |

A sketch of the grammar, for the design doc to settle — not a decision:

```
param text_cap = 12 range 6..30
param puff = 1.2 range 0.4..3

coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  base 4
  relief straps emboss 1.2
  strap width 2
  text "NAQSH" at 0, 0
    font bubble
    cap $text_cap
    puff $puff
    pad 2
  color text Gold
```

The Lab rule "offer only what the export can honour" (D-074, as the relief-shape module words it)
applies: hide the text control on styles where it cannot work yet (e.g. minimal coasters before a
pad exists), rather than show a knob that errors. Whether the text lives in the share URL is for
the design doc; the print target stays out of share URLs by existing convention.

## 6. Multi-colour letters

- **How colour works today.** `color <region> <PaletteName>` tags a region (D-073), and
  `bikar render --format parts` splits the height field into one body per region
  ([coaster-colour-design.md](../coaster-colour-design.md) §4–§5). The plate composer maps
  palette name to an AMS slot ([plate-composer-design.md](../plate-composer-design.md)).
- **Letters would be a fourth region**, `text`. That changes a written-down set of three
  (`CoasterRegion`, and the Lab's `REGION_ORDER`, `coaster-colors.ts` line 16).
- **Domes have a feather edge.** A dome falls to zero height at the letter edge, which is exactly
  the zero-width "pinch" the colour split already found for sharp straps (D-074;
  [coaster-colour-design.md](../coaster-colour-design.md) §5.1). The existing `--pinch fillet`
  handling may cover it; a simpler fix is to stand each dome on a short vertical skirt (say one or
  two layers), so the letter body never thins to zero at its edge. Which is better is open.
- **The split refuses several styles.** `assertSplittable` (`coaster.ts` line 2628) refuses
  openwork, rim, trivet, interlock, edge bevels, minimal coasters and deboss. So two-colour
  letters would work on the plain and border styles first; openwork/minimal/interlock need the
  split extended.
- **Compose drops colour.** `bambu slice compose` hands loose STLs to the arranger, so a plate
  built that way is single-colour; a coloured coaster has to go through `bambu slice coaster`
  (see the notes in [minis-01.yaml](../plates/minis-01.yaml)). Coloured lettering inherits that.
- **Single-colour fallback.** The layer-pause colour swap at the letter height gives two colours
  without the split, but it colours everything above that height — straps included — so it only
  suits designs where letters are the only thing that tall.

## 7. Risks and open questions

1. **Does it look puffy at coaster scale?** The dome is 6–15 layers tall. It may read as terraced
   rather than inflated. Only a print answers this (phase 2).
2. **Cup stability** vs letter height (§4.1). Unmeasured.
3. **Counters and gaps filling in** on fat letters with domed edges (§3.1). Unmeasured for any
   bubble face.
4. **Font licence.** Candidates found on Google Fonts' repository, all listed as `OFL`:
   Bagel Fat One (Kyungwon Kim, JAMO), Modak (Ek Type), Fredoka (variable, weight 300–700,
   Milena Brandão / Hafontia), Rubik Bubbles (NaN, Luke Prowse; described as a script-generated
   face based on Rubik). OFL allows embedding in products; the bake keeps the face's own licence
   text, as the Source Code Pro bake does. This is four faces found by one search, not a survey of
   rounded fonts. What each looks like as a pillow, whether it passes B1, and whether Rubik
   Bubbles' decoration adds extra contours inside letters are all unchecked.
5. **Character set.** A bubble face baked the current way would be uppercase + digits + `-`.
   Lowercase, `&`, `'` and Arabic would each widen the bake and the confusables list; Arabic
   (naqsh) lettering is a separate question — joined script changes layout entirely.
6. **Grid resolution.** Letters are sampled at 0.4 mm. Fine at a 12 mm cap; at a 6 mm cap on a
   40 mm mini, letter edges get coarse. The kernel's grid pitch is a per-spec option
   (`gridPitchMm`), so a finer grid for lettered coasters is possible at a cost in triangles.
7. **Speed in the Lab.** The fill-and-distance step runs once per render over roughly 225 × 225
   grid points for a 90 mm coaster. Expected to be fast; not measured.
8. **Side edges** need new geometry and have overhang risk; deferred (§4.2).
9. **Legal.** Do not reproduce the SKIMS wordmark; use a licensed face for the look.

## 8. Research and prototype plan

Smallest proof first. Each phase says what it checks; none prints without Omar (printing is owner-
gated).

| Phase | Work | What it checks |
|---|---|---|
| **0. Font desk check** | Download 2–4 OFL rounded faces. Run `scripts/bake-glyphs.py` on each for `A–Z 0–9 -` into a scratch output (not shipping). Measure stem widths, counter sizes and letter gaps at 8, 12 and 16 mm caps with the existing layout checks. | Licence text is present in the file; which faces pass B1–B3 (or fail on overlaps, which option A tolerates); which face keeps counters and gaps above 0.4 mm at which cap. |
| **1. Offline pillow render** | A standalone script in bikar's test tree: one word ("NAQSH") on one plain coaster (six-fold rosette, 90 mm), option A's height rule added to the field, knock-out pad on. Render STL + views. Also render option B (tube letters) beside it. | The mesh still passes the coaster mesh gate; the look on screen (Omar's call: does it read as "bubble"?); how the letters meet the pattern. |
| **2. Print coupon** | A small flat slab (e.g. 70 × 40 mm), one word, a ladder of 3 caps × 3 puff heights, one pad; slice at 0.2 mm and again with variable layer height. Review with the look-before-you-print sheet first. | Terracing on the dome; counters closing; legibility; whether variable layer height is worth it. Settles new bets for text cap and puff on this face. |
| **3. DSL** | `text` statement in the coaster block (top face, plain and border styles), `font`, `puff`, `pad`, with validators that refuse a word whose gaps or counters fall under the floor. | Parser refusals and the per-letter checks; coaster validators still pass with text. |
| **4. Coaster Lab** | Text box + font picker (source rewriters, like the colour knob), cap/puff/round sliders from `param`s, placement. | Round trip: knob → source → render; unsupported styles hide the control. |
| **5. Colour** | `text` region, `color text …`, dome skirt or pinch fillet, `--format parts`, a `bambu slice coaster` plate. | Per-region bodies stay closed; the AMS map picks up the letter colour. |
| **6. Openwork / minimal** | Solid pad exempt from the openwork cut; bridge to straps on minimal. | Letters never float; pad rim width against the strap floor. |
| **7. Side edges (separate study)** | Start with *engraved* text on one flat face of a hexagon coaster (no overhangs), then a teardrop-profile raised version. | Whether ~3 mm caps are legible on a 4 mm wall; whether the underside overhang prints clean. |

**First step:** phase 0 then phase 1 — bake two or three OFL bubble faces into scratch output and
render one word as a pillow on one plain coaster, beside the tube-letter version, for Omar to pick
from the renders before anything is printed.

## 9. Sources

All fetched 2026-09-26.

- mojomox, "Skay similar to Skims font" — https://mojomox.com/skims-font (SKIMS mark is a custom
  logotype).
- 1000logos, "SKIMS logo" — https://1000logos.net/skims-logo/ (flat and "voluminous" versions;
  read via search snippet).
- Google Fonts repository metadata (`METADATA.pb`, licence field):
  - https://raw.githubusercontent.com/google/fonts/main/ofl/rubikbubbles/METADATA.pb and
    https://raw.githubusercontent.com/google/fonts/main/ofl/rubikbubbles/DESCRIPTION.en_us.html
  - https://raw.githubusercontent.com/google/fonts/main/ofl/bagelfatone/METADATA.pb
  - https://raw.githubusercontent.com/google/fonts/main/ofl/modak/METADATA.pb
  - https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/METADATA.pb
- Sovol, "Ironing in 3D printing" —
  https://www.sovol3d.com/blogs/news/ironing-in-3d-printing-settings-for-smoother-top-surfaces
- Chitu Systems, "Why curved 3D prints look rough" —
  https://www.chitusystems.com/blogs/articles/why-your-curved-3d-prints-look-rough-and-how-to-fix-them
  (read via search snippet).
- UltiMaker community, "Reducing stair stepping effect on round surfaces" —
  https://community.ultimaker.com/topic/32990-reducing-stair-stepping-effect-on-round-surfaces/
  (read via search snippet).
- Bambu Lab wiki, "Variable Layer Height" —
  https://wiki.bambulab.com/en/software/bambu-studio/adaptive-layer-height (search snippet only;
  direct fetch returned HTTP 402).
- Cubify fans blog, "Considerations for embossing 3D printed vertical surfaces" —
  http://cubifyfans.blogspot.com/2015/01/considerations-for-embossing-3d-printed.html
- In-repo: [text-emit-design.md](../text-emit-design.md),
  [outline-font-emit.md](outline-font-emit.md), [text-emit-survey.md](text-emit-survey.md),
  [coaster-colour-design.md](../coaster-colour-design.md),
  [coaster-minimal-design.md](../coaster-minimal-design.md),
  [plate-composer-design.md](../plate-composer-design.md).
- bikar at `origin/main` (read 2026-09-26): files and line numbers as cited in §2–§6.
