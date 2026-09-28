---
status: superseded
---

# Multicolour constructions — filled shapes, one colour per matching ring (design B)

> **Superseded by [multicolor-design.md](multicolor-design.md)** (the checker's consolidated
> design, 2026-09-27). This is researcher B's design, kept as the record it was built from.

**Status:** proposal from researcher B of two independent researchers; a later agent merges both
designs. Nothing here is built, no decision id is taken, and nothing is printed. Research and
measurements: [`research/multicolor-constructions-b.md`](research/multicolor-constructions-b.md).

## 0. Summary

- **Recommendation:** the *plain* coaster style (a one-colour slab with raised straps) gains
  **filled shapes set lower than the straps** ("cloisonné": the straps stand as little walls
  between colours). Each filled shape is its own colour body in the `--format parts` split that
  already ships ([D-073](decisions-log.md)–[D-078](decisions-log.md)), so colours reach the
  printer through the existing multi-part 3MF and `bambu slice coaster` path with no new printer
  route.
- **Colour classes** are a new fill attribute, `class`: two shapes share a class when a rotation
  about the pattern's centre (or, for a pattern with mirror symmetry, a reflection through it)
  carries one onto the other. The shipped `ring` attribute cannot do this: measured on CS-1, one
  true class is scattered over 3–6 rings (research §2).
- **Grammar change: yes, small.** A new `class` word in the fill selector list, a `bikar classes`
  listing verb, and a way to give filled shapes their own height (§8). The `fill where … color …`
  statement itself keeps its shape.
- **First prototype (proposal only):** CS-1 plain coaster, two filled classes, four colours in
  total, as minis at three fill depths on one plate (§10).

## 1. The ask

Omar: "an alternative version of constructions … where we have multi colors shapes (fill in some
of the traces) instead of just a trace and that we can print in multiple colors", and "shapes
that are translations same midpoint from center should be same color".

Read literally, "translations" in a rosette are rotations about the centre; "same midpoint from
center" is the same centroid distance. The rule therefore says: **copies of one shape that the
pattern's symmetry moves around the centre get one colour.** A class is a ring of matching
shapes.

## 2. Where the shapes come from, and how classes are computed

### 2.1 The shapes

The fillable shapes are the bounded **faces** bikar already computes for a pattern: the regions
the traces enclose, the same faces `fill where …` colours in the SVG and `relief faces` raises on
a coaster. No new geometry source is needed. Two exceptions:

- **Faces clipped by the coaster outline** are not congruent to their uncut siblings. They get
  no class and stay the slab colour (a clipped copy in a class colour would read as a broken
  ring).
- **Faces too narrow to fill** stay the slab colour (§7.1).

### 2.2 The class rule

Three candidate rules, side by side:

| Rule | Pros | Cons | Implications |
|---|---|---|---|
| **R1 — reuse `ring`**, fixing its centre | No new word; `bikar bands` already lists rings; D-078 already carries ring colours to the print | Radius only: different shapes at one radius share a ring, which breaks the rule. Fixing the centre renumbers the rings in the 8 shipped patterns that select by `ring` | Every existing `ring == N` selector must be re-checked by hand; one word would keep two meanings during the move |
| **R2 — new `class` = orbit about the centre** (recommended) | Exactly the rule: related by a rotation (or reflection) about the centre. Checkable per face (§9). Leaves `ring` alone | A new attribute, a new listing verb, a symmetry test in the resolver | `ring` stays for "bands at a radius" (a real, different idea); `class` is the shape-aware word. The merge agent must decide whether `ring` should later be defined on the same centre |
| **R3 — congruent and same radius** | Simple: a shape signature plus a radius | Weaker than R2: a congruent shape at the same radius but turned differently relative to the radial line joins the class. Whether any surveyed pattern has such a pair was not measured | Would pass the Validator's colour check and could still break the visible symmetry |

The research survey measured R3, not R2 (research §2.1). R2's classes are the same or finer; how
much finer on the surveyed patterns is unmeasured.

### 2.3 The centre

`ring` measures from the first circle defined, which on CS-1 is the wrong point (A instead of the
rosette centre G, research §2).

**Default:** the class centre is the centre of the pattern's **outermost** `rotate N around X`
(the rotation that makes the rosette); when a pattern has no such rotation, or rotations about
several centres (n3IidKfXE1I, a 12-6-4 composite), `class` is **refused** with that reason
rather than guessed — per the measured CS-1 and n3Iid findings in
[research §2.2](research/multicolor-constructions-b.md), against the shipped first-circle rule in
bikar's [`findCenter`](https://github.com/NaqshCoffee/bikar/blob/6356bb3a7f3db2988860a86e7110e30e658a980f/packages/core/src/dsl/evaluator.ts#L10060). An explicit `centre` clause is deferred
until a pattern needs one.

### 2.4 Mirror copies — decided

**Default:** a mirror image counts as the same class **when the pattern has a mirror line
through the centre that carries the whole face set onto itself**, and does not otherwise. Mirror
handling changes the class count in 3 of the 7 measured constructions, and in 7apC5Q9QS-8 the
mirror-same count reproduces the author's own ring grouping exactly
([research §2.4](research/multicolor-constructions-b.md), measured on
[7apC5Q9QS-8.bkr](https://github.com/NaqshCoffee/bikar/blob/6356bb3a7f3db2988860a86e7110e30e658a980f/patterns/Constructions/7apC5Q9QS-8.bkr)).

Why: in a pattern with mirror symmetry the mirror image *is* one of the pattern's copies, and
colouring it differently makes the colouring lopsided when the drawing is not. In a pattern with
rotation only (a twist or whorl), the mirror image is a different shape in the design, and
merging it would invent a symmetry the drawing lacks. Whether each surveyed construction has a
mirror line was not tested.

### 2.5 Tolerance

**Default:** two members of a class may differ in centroid radius, and in vertex position after
the carrying rotation, by at most **τ = 1e-3 × unit** (0.02 at unit 20). Measured at unit 20, the
largest spread inside a class was ≤ 7.9e-5 and the tightest gap between two congruent faces in
different classes was 0.20 (rDux, two hexagons at r 51.06 and 51.26), so τ sits about 250× above
the spread and 10× below the tightest gap
([research §2.3](research/multicolor-constructions-b.md)). τ scales with the unit because the
measured window does; the shipped ring tolerance is an absolute `1e-2`
([`computeRingBins`](https://github.com/NaqshCoffee/bikar/blob/6356bb3a7f3db2988860a86e7110e30e658a980f/packages/core/src/theme/fill-resolver.ts#L414)).

This transfers to other patterns only while their tightest congruent gap stays above τ; the
Validator (§9) does not rely on that, because its orbit test fails on a merged pair whatever τ is.

### 2.6 Choosing which classes fill

Filling every class gives as many colours as classes — 4 to 47 in the survey — and a busy result.
The author chooses:

1. `bikar classes <pattern>` lists each class: id, member count, sides, area, radius — the
   `bands` verb's shape, so the author can pick by eye against the SVG.
2. The author writes `fill where class == N color <PaletteName>`. Unfilled classes stay the slab
   colour.
3. Several classes may share one palette name. That is how a design with more classes than
   spools is made (§6).

No automatic pick is proposed: which rings to colour is a taste call, and an automatic pick
verifies nothing about it.

## 3. Geometry options

The coaster is a height field: each cell column belongs to exactly one colour body, so bodies are
disjoint with no gaps and need no boolean union (research §1 item 11). Every option below keeps
that. Swap counts assume 0.2 mm layers and K filled colours plus one strap colour; they count
colour changes per layer, the quantity W2 says purge scales with (research §3, fetched). They are
arithmetic on the geometry, not measured prints.

| Option | What it is | Pros | Cons | Implications |
|---|---|---|---|---|
| **A — flush mosaic** | Fills raised to the strap height; the top is flat, colour-only | Smooth top; simplest height rule (one height) | Colour change on every layer of the relief: 6 layers × (K+1) colours. The only line between colours is the colour itself, so any bleed shows at the top face | Needs strap-wins precedence (§3.1) or the fill eats half of each strap |
| **B — cloisonné** (recommended) | Fills raised lower than the straps (proposed 0.4–0.8 mm vs 1.2 mm) | Straps stand between colours and hide a ghosted start of a region (W2's bleed symptom); multicolour layers only in the fill band (2–4 layers × (K+1)); keeps the plain style's feel | A second height to declare (grammar, §8); a fill depth no source settles | Reuses the D-073 split and the D-075 3MF path unchanged; the fill depth is laddered on the first plate (§10) |
| **C — face-down mosaic** | Coaster printed upside down: the coloured pattern is the first few layers on the bed, the slab above | Flat, crisp face; colour confined to the first 2–4 layers | Loses the raised straps; a multicolour first layer with small islands, whose adhesion is unmeasured; the kernel's split is cut at `z = base`, not at a bed-side layer | New split mode; a real second style, not a variant of the plain one |
| **D — stained glass** | Minimal-frame straps with thin coloured panes in the openings | Closest to "fill in the traces" of the minimal styles | The split refuses openwork today (research §1 item 7); pane-to-strap bond is a two-filament joint with no bet | Lifting the refusal is kernel work plus a new bet for the pane joint |
| **E — full-height plugs** | Each shape a full-thickness block of its colour | Colour on both faces | Every layer multicolour: 20+ layers × (K+1) changes — the shape W2 calls far more purge | Worst purge and time; offered only to be ruled down |
| **F — height terraces, no AMS** | Each chosen class at its own height, one colour change at each height | Works with pause-and-swap on one spool | Straps must be the highest step; the sides of taller steps show the lower colours; classes limited to distinct heights | A useful fallback when the AMS is absent; not the X2D path |

**Recommendation: B**, because it is the only option that stays inside the pipeline that already
ships (split → multi-part 3MF → `bambu slice coaster`), has the fewest colour-change layers of the
relief-keeping options, and puts a strap wall where bleed would show. **C** is the strongest
second: it should be the merge agent's pick if Omar wants a flat face.

### 3.1 Strap wins

Face polygons run to the strap centrelines, and today a face colour paints the relief cells under
it (research §1 item 8). Under B the rule must be: **a cell within half a strap width of a strap
centreline belongs to the strap body**, and only the cells inside that belong to a fill body.
Without it the fill eats half of each bounding strap and the strap lines thin to half width in
the print.

## 4. Getting colours to the printer

| Route | Pros | Cons | Implications |
|---|---|---|---|
| **One multi-part 3MF** (recommended; shipped by D-075/D-077) | One object, parts already registered to each other; palette name → logical slot baked into the 3MF, the only form the headless CLI honours | Headless slice cannot confirm colours (D-077: GUI check) | Each new fill colour is one more part and one more palette name; nothing new to build on the printer side |
| **Separate STLs per colour** | Any slicer can load them | Registration and slot assignment by hand every time | Throws away D-075's contract; verifies nothing |

- **Slots.** Read from the device with `bambu filament`, as D-078 decided ("warn, not cap").
  The X2D's full slot count with several AMS units is snippet-only (research W4) and is not used
  here.
- **Purge and time.** They scale with colour changes per layer (W2, fetched). Option B's changes
  sit in the 2–4 layers of the fill band; the strap band above is one colour. Dark-to-light
  transitions need the most flushing (W2), which argues for a dark slab with light fills only if
  the slicer orders the light colours first within a layer — not verified.
- **Second nozzle.** Whether the X2D's second nozzle reduces purge for a two-colour job is not
  something any fetched source states (W1 says it handles "support or interface material"). No
  claim is made.

## 5. Colour-change layers without an AMS

Option F is the only one that works with a pause-and-swap on one spool; A–E need an AMS because
each layer holds several colours. This matters for a printer without an AMS; on the X2D it is a
fallback, not the route.

## 6. More classes than slots

1. **Share palette names.** Several classes take the same colour; the count that must fit is
   palette names, not classes. Alternating two colours class by class, outward from the centre,
   keeps the rule (one class, one colour) with only two fill spools.
2. **Leave classes unfilled.** An unfilled class is the slab colour — itself a colour.
3. **Warn at slice time** when palette names exceed the loaded trays, following D-078's "warn,
   not cap".

No automatic merge by radius is proposed: it would silently give two classes one colour, which
the author may not want.

## 7. Printability

### 7.1 Smallest fill

**Default:** a face whose largest inscribed circle is narrower than the coaster's single-filament
feature floor, **CAL-CST-01**, gets no fill and stays the slab colour. That floor was set for one
filament: a solid rib between debossed regions. It carries over to a fill only if a two-colour
pocket fills at least as well as a one-colour rib. That is the same open question CAL-PIN-01
carries for pinches, so this default is a placeholder until a coupon measures it. The smallest
faces at 80 mm were **not measured** for any construction.

### 7.2 Bleed

Under B a fill meets a strap at a vertical wall inside the fill band, and the strap rises past
it. A ghost of the previous colour at the start of a region (W2) then sits beside a wall, not on
an open flat face. How much this hides is what the depth ladder (§10) looks at. Pinches where a
fill body tapers to nothing at a shape's sharp corner are the D-074 case, and the shipped
`--pinch fillet` floor applies.

**Default:** the pinch floor for fill bodies is **CAL-PIN-01**, as for strap bodies, because a
fill corner meeting the slab is the same two-filament interface that bet already names.

### 7.3 Bed side

The slab is the bed side under A, B, E and F: the first layers are one colour, so the first layer
has no colour changes and no small multicolour islands. Only C puts colour on the bed.

## 8. The DSL shape, and the grammar change

Proposed, for CS-1:

```
fill where class == 3 color Teal
fill where class == 5 color Ivory
coaster pattern
  outline polygon 6 $size rotate 30
  inscribe
  base $height
  relief straps emboss 1.2
  relief faces emboss 0.6 filled
  strap width 2
  color base Slab
  color straps Gold
```

(Class ids are illustrative until `bikar classes` numbers them.)

**Grammar change: yes, three small pieces.**

1. **`class`** joins the fill selector words (`FILL_ATTRIBUTES`). This adds a word; the
   `fill where … color …` statement keeps its shape.
2. **`bikar classes`**, a listing verb like `bikar bands`.
3. **A fill height for filled faces only.** `relief faces` today raises every face, with one
   height shared with the straps (research §1 item 9). The proposal adds `filled`:
   `relief faces emboss <mm> filled` raises only faces that carry a fill colour, next to a `relief straps`
   clause. The new word matters: changing plain `relief faces` to mean "filled only" would give
   one phrase two meanings across old and new files. Whether the parser accepts two relief
   clauses today was not checked; if not, that is part of this change.

The palette name → slot path, `--format parts`, `--pinch` and `bambu slice coaster` need no
grammar change.

## 9. Validator

**Validator:** after fills resolve, for **every face** that is a member of a class, (a) there is
a rotation about the class centre — or, where §2.4 admits mirrors, a reflection through it — that
carries the class's first member onto this face, vertex set to vertex set, within τ; and (b) this
face's palette name equals the first member's. Both checks run face by face and report the first
failing face id: a per-class count of colours, or a total, cannot stand in for them — one odd
face in a ring of twelve leaves every aggregate looking right. It also fails any class whose
colour would come from a clipped face (§2.1).

- PASS: CS-1 about G with `fill where class == k color Gold` on the 12-face class at r = 30.55 —
  all 12 faces map onto the first by a rotation about G, and all 12 carry Gold; no face outside
  the class changes.
- FAIL: the hard case — rDuxHF3xMOc's two congruent hexagons (area 136.4) at r = 51.06 and
  51.26, 0.20 apart, under a too-loose tolerance (τ ≥ 0.20, or any radius-only grouping). They
  fall into one class; check (a) fails on the second hexagon, because a rotation about O keeps
  radius, so no rotation carries a shape at 51.06 onto one at 51.26. The orbit test catches the
  merge whatever τ is set to.
- FAIL: a class filled Gold plus a later `fill where index == 17 color Red` hitting one member —
  check (b) fails on face 17 alone.

## 10. Smallest first prototype and first sample plate (proposal only)

Owner-gated: printing is paused until a CAL bet settles, and Omar reviews a render sheet before
any print ("look before you print").

- **Prototype:** CS-1 (GimTvN9hw4U) plain coaster, option B, with **two** filled classes — the
  centre face and the 12-face class at r = 30.55 about G. Four palette names in total (Slab,
  Gold, two fills), so it needs only four loaded trays. It exercises
  every new piece: `class`, the G centre, strap wins, `filled`, and the multi-part 3MF.
- **Sample plate:** four CS-1 minis, the same palette, at fill depths 0.4, 0.6 and 0.8 mm (B)
  and 1.2 mm (A, flush). It compares bleed and edge definition side by side and settles the fill
  depth, which no source here gives. Slot count from `bambu filament` on the day. A full-size
  80 mm CS-1 at the chosen depth follows.

## 11. Checked against itself (K7) and transfer conditions (K10)

- The §9 PASS example is built only from machinery §8 proposes (`class`, `filled`) plus shipped
  pieces. It fills one class, so it needs no mirror decision, and CS-1's classes are equal under
  either mirror rule (research §2.2).
- The §9 FAIL case uses τ ≥ 0.20, while §2.5's default τ = 0.02 separates it. The FAIL exists to
  show the orbit test does not depend on τ being right.
- §0, §3 and §10 all recommend B. §3's C is a second choice, not a contradiction.
- The survey measured R3, and the design adopts R2. §2.2 states that the two can differ and that
  the difference is unmeasured.
- **K10 — CAL-CST-01 → fill floor:** this transfers only if a two-colour pocket fills at least as
  well as a one-colour rib (§7.1). That is not shown, so it is a placeholder.
- **K10 — τ from 8 constructions to any pattern:** this transfers only while a pattern's tightest
  congruent gap exceeds τ. The orbit test covers the case where it does not.
- **K10 — W2's "purge scales with transitions":** a general Bambu Studio statement. It transfers
  to the X2D if the X2D flushes per change like other AMS machines, which W2 does not test.
- **K2:** the survey is the 8 constructions listed in research §2.2, one of them unmeasured. The
  web search is the 9 sources in research §3. No claim here reaches past those sets.
