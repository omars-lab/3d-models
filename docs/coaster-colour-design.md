# Coaster colour regions — a symbolic name per region, one body per colour, a filament map at the slicer

*Status: designed (task #37, decisions D-073, D-074). The direction is D-068 (coaster-level
composition): a coaster's cells already split into named regions; this doc gives those
regions a colour vocabulary in the DSL, a per-body export so each region prints in its own
filament, and a Coaster Lab knob to set it. It builds directly on the border band of
[`coaster-border-design.md`](coaster-border-design.md) (D-071), which recorded the first
region split (band vs field), and on the emboss decision of D-066. It adds no new solid; the
region split adds one bet, **CAL-PIN-01** (the pinch floor for a two-filament interface, §5.3),
introduced when the naïve split proved a K7 contradiction (D-074). Research on file:
[`research/coaster-colour-research.md`](research/coaster-colour-research.md).*

## 1. The ask

Omar (2026-09-17): "will this be part of our coaster lab? color selection?" and "do we
have a 'border' component we compose with a pattern component and can assign colour
individually that translates to different filaments on X2D?"

Today the answer is *not yet*, and the research file (§1–§2) says why precisely: every
colour clause bikar has — `palette`/named colours, `fill … color`, `edges color`,
`strapwork … color` — is **2D SVG ink** (bikar `docs/language-reference.md` §7.4/§7.5); it
never reaches the height-field kernel. The 3D path renders one watertight body per coaster,
and STL carries no colour at all. So "assign colour individually that translates to a
filament" is four separable questions, and this doc answers them as one route:

1. **What is a region, and how is it named** — so a colour is assigned to *what is
   distinct*, not to a spool.
2. **How the DSL says it** — `coaster` gains `color <region> <PaletteName>`.
3. **How the kernel exports it** — `bikar render --format parts` splits the height field
   by region into one watertight body per region.
4. **How the filament map happens** — the plate composer maps palette name → AMS slot; the
   slicer, not bikar, binds a spool.
5. **How the author sets it** — a Coaster Lab knob that edits the `color` statements and
   tints the preview per region.

Read as a careful colleague would: the border kernel already partitions cells into **band**
and **field** and records a per-cell `band` bit "so #37 has something to export without
re-deriving the geometry" ([`coaster-border-design.md`](coaster-border-design.md) §3, §5).
This doc does not invent region-splitting; it names the regions and adds the export.

## 2. Options and the rubric

Rubric (0/1/2): **R1 the DSL stays about geometry** (a region names what is distinct, not
which hardware slot); **R2 one kernel** (reuse the height field and the region bit; no new
solid, no boolean); **R3 checkable** (a per-body validator with a constructible FAIL, not a
total); **R4 costs the grammar little** (reuse the existing colour-name vocabulary, one new
production); **R5 ports** (the region name survives into the Lab preview, the 2D render, and
the composer's manifest, and is not printer-specific).

| Option | R1 | R2 | R3 | R4 | R5 | Verdict |
|---|---|---|---|---|---|---|
| (a) **`color <region> <PaletteName>`** — a symbolic region is tagged with a palette name; `--format parts` exports one body per region; the composer maps name → AMS slot | 2 | 2 | 2 | 2 | 2 | **chosen** |
| (b) `filament <region> <slot N>` — bind a region straight to an AMS slot in the DSL | 0 | 2 | 1 | 1 | 0 | puts the X2D's hardware into a bikar file: the same `.bkr` no longer renders as 2D art and will not port to another printer or slot layout. The DSL says what is distinct; the manifest says which spool (research §2) |
| (c) Paint colour onto the one body — write vertex/face colours into a single-body 3MF, no split | 1 | 2 | 0 | 1 | 1 | there is no per-region body to `--check`, so an empty or leaked region is invisible; and the headless CLI contract for painted-colour import is **unverified** (research §6). Couples bikar to one slicer's 3MF colour convention |
| (d) Do nothing — one filament per coaster | 2 | 2 | — | 2 | — | does not answer the ask; kept as the honest baseline "robustness verifies nothing here" option |

(a) wins because it keeps the one thing the DSL should own — *which regions are distinct* —
and hands the one thing it should not own — *which spool* — to the manifest. The palette
name is a label the author already writes for the 2D render; reusing it as the region's
symbolic colour costs the grammar one production and keeps a single source of colour truth
for both the SVG and the print.

## 3. The region vocabulary

A coaster has three regions, and only three, enumerated here so the count is a claim about a
set that is written down (K2):

- **`base`** — the slab up to `z = base`: the ground every relief sits on. Its colour is the
  coaster's body colour.
- **`straps`** — the field's embossed art (the `inscribe`d pattern's straps and bounded
  faces), raised on the slab.
- **`border`** — the band's embossed motif, present only when the coaster has a `border`
  clause (D-071); absent otherwise.

These are **symbolic names, never filament ids.** The DSL says what is distinct; the print
manifest says which spool (research §2). A region maps to a body at export and to an AMS
slot at the composer — but in the `.bkr` it is only a name, so the same file renders as 2D
art, previews in the Lab, and slices on any multi-material printer.

The region a cell belongs to is already computable: the border kernel's `band` bit plus the
existing relief/ground classification give *ground → `base`*, *field relief → `straps`*,
*band relief → `border`*. No new geometry is read; the region is a re-labelling of the two
bits `classifyCell` already stores ([`coaster-border-design.md`](coaster-border-design.md)
§3).

By default — when a coaster has no `color` statement — every region keeps the coaster's one
body colour and `--format parts` still emits one body per non-empty region (a no-op for a
single-filament print), matching today's one-body behaviour ([`coaster-design.md`](coaster-design.md)).

## 4. Grammar — `color <region> <PaletteName>`

One statement is added to `CoasterStmt` in bikar `docs/grammar.md` §10.3 (the same section
the border clause landed in), G3 fences on every example:

```ebnf
CoasterStmt  = CoasterOutline | CoasterInscribe | CoasterBase | CoasterRelief
             | CoasterStrap   | CoasterRim | CoasterEdge | CoasterTrivet
             | CoasterInterlock | CoasterBorder | CoasterColor ;
CoasterColor = "color" RegionName PaletteName NL ;
RegionName   = "base" | "straps" | "border" ;
```

`color` is already a reserved word in bikar's 2D layer (`edges color`, `fill … color`,
`strapwork … color`; research §1), so the keyword snapshot (G2) is unchanged. `RegionName`
is a **contextual identifier** dispatched on token text, exactly as `border` is in the
coaster body (D-071) — no new keyword. `PaletteName` is an identifier the evaluator
resolves against the file's `palette` block; an undeclared name is an evaluation error
naming the clause, like `inscribe`'s undeclared-pattern error. `color` may appear once per
region and at most three times.

```bkr
coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  border GimTvN9hw4U_border width $border
  base 4
  relief straps emboss 1.2
  strap width 2
  color base   Slab
  color straps Gold
  color border Gold
```

Refusals split by phase in the shipped grammar ([bikar PR #213](https://github.com/NaqshCoffee/bikar/pull/213)):
two are structural and caught at **parse** time (`ParseError`), two are semantic and caught at
**evaluation** time (the `coaster:`-prefixed mechanism the border and interlock clauses use).
The split is not cosmetic — a parse error is raised before any coaster is evaluated, on the token
text alone, while an evaluation error needs the coaster's regions and the `palette` block in hand.

Parse errors (`ParseError`), from the grammar itself:

- `color <region> …` where `<region>` is **not** in the closed set `base | straps | border` —
  the `RegionName` production admits only those three, so any other token is rejected by the
  parser, not the evaluator.
- `color <region>` repeated for the same region — per-region uniqueness is enforced at parse
  time; the second statement is a `ParseError`, the first still in force.

Evaluation errors, naming the clause:

- `color border …` on a coaster with no `border` clause — the region name parses (it is in the
  closed set) but the coaster does not carry it; the message names `border` and lists the regions
  the coaster has.
- `color … <name>` where `<name>` is not in any `palette` block — the palette name is undeclared,
  resolved (and refused) by the evaluator against the file's `palette` block.

**K10 transfer condition.** The palette-name vocabulary is being carried from the 2D SVG
world (§1) into the 3D per-body world. This transfers **because a palette name is a
symbolic label, not a rendering instruction**: in 2D it resolves to a hex stroke/fill; in
3D the *same name* tags a region for the per-body split and the manifest, and the hex is
used only to tint the Lab preview (§7) and the SVG. What does **not** transfer is the ink
semantics — a region is never "painted"; it is a separate body. The sentence that must hold
is written, so the rule is allowed to cross (K10).

## 5. Kernel and CLI — `--format parts` splits the height field by region

`bikar render <coaster> --format parts` splits the one height field into one body per region
that has at least one cell:

1. **`base`** is the slab prism to `z = base` (the full top face, including under the relief).
2. **`straps`** is the field relief — emboss prisms standing on the slab's top face.
3. **`border`** is the band relief — emboss prisms on the slab's top face, present only with
   a `border` clause.

This reuses the existing kernel: `reliefAppliesAt` already reads by region (D-071); `--format
parts` changes only *how the sampled field is assembled into meshes*, not what is sampled. The
split still requires an **emboss** ([D-066](decisions-log.md)): a deboss removes material and
leaves the slab's own colour, so a debossed region has no raised body to carry a filament and
is refused (the transfer condition on the split — meaningful only while the relief embosses).

### 5.1 The naïve split has a proven limit (D-074)

The first draft of this section asked for two invariants at once — **(A)** the union of the
bodies is *exactly* the single-body `--format stl` mesh, and **(B)** each body is watertight
and **2-manifold** on its own. For any coaster whose relief descends to `z = base` at an
*interior* point of a region — every sharp strap apex and every strap crossing (octagram,
sharp hexagon) — the two **cannot both hold**, so asserting both was a K7 contradiction. While
a strap stays fused to the slab, the slab's `base` mm of thickness carries it; cutting it off
at `z = base` severs that and leaves a genuine **zero-width pinch** — one edge shared by four
oriented faces (two relief-top, two slab-top). The body is closed and volume-correct but not
2-manifold, and no re-tessellation fixes it: the two sub-wedges meet only along a zero-width
seam. It is also physically unmakeable — a second-filament sliver that is zero-width *and*
zero-height cannot be extruded. (Verified 2026-09-18: the exact split holds to ~1e-14 for
every pinch-free emboss coaster; only saddled patterns fail (B), and the `base` body is always
2-manifold.)

### 5.2 Sharp-edge (pinch) detection

Before assembling the split bodies the kernel **detects** every pinch. A pinch is exactly an
edge that, after the region cut at `z = base`, is shared by four oriented faces — the
*four-faces-at-an-edge* test — equivalently a saddle of the height field pinned to `z = base`
inside a region footprint, where the resulting body thickness falls below the printable floor.
The detector reports each pinch with its `(x, y)` and the two cells that meet, so a strategy
can act cell-locally and a refusal can name the spot. This is **not** the kernel's existing
`desaddle`, which fixes bowties in the *solid mask* only; height-field pinches are edge-adjacent
axis pinches or single anti-diagonal-raised cells, neither a mask bowtie — a new detector is
required, not a reuse.

### 5.3 Handling strategies — `--pinch <fillet|merge|error>`

How a detected pinch is resolved is a **manufacturing** choice, not a design-intent one, so it
is a CLI flag on `render --format parts`, never a DSL statement (K10 transfer note: the DSL
says *what the coaster is*; the spool count and the pinch policy say *how this copy is made* —
the same reason the palette name, not a slot id, lives in the source). `--format stl` is never
altered by any strategy.

- **`fillet` (default).** On the split bodies *only*, raise each pinch to the printable floor
  so the body becomes 2-manifold. Preserves colour intent — a gold star tip stays gold, a hair
  thicker. The per-region STL then differs from the single-body mesh **only inside cells
  thinner than the floor** — geometry no printer could reproduce anyway.
- **`merge`.** Reassign each pinching cell to the adjacent `base` region, so no thin separate
  body is created. The split stays **exactly** union == single. Cost: the very tip loses its
  colour (it prints in the `base` filament). Deterministic; changes colour, not geometry.
- **`error`.** Refuse the whole render, naming each pinch `(x, y)` and the physical reason —
  "the relief kisses the slab at a zero-width notch no printer can make in a second colour —
  thicken/separate the motif, choose `--pinch fillet|merge`, or render `--format stl`." For an
  author who would rather redesign the motif than let the tool decide.

`--pinch keep` (emit the closed but non-manifold body) is **deliberately not offered**: it
verifies nothing a slicer can trust and ships geometry the printer chokes on.

**Default:** `fillet`, and the pinch floor is **CAL-PIN-01** — `fillet` raises any pinch
thinner than the coaster's `featureFloorMm` (0.80 mm today — `STRAP_WIDTH_MIN_MM`,
[`coaster-design.md`](coaster-design.md)) up to that floor, and CAL-PIN-01 owns whether that
single-filament strap floor is the right threshold for a *two-filament interface* pinch, which
no source here settles — a bet, not a bare number.

### 5.4 The border outer wall (second defect, D-074)

Where a border motif reaches full relief height at the outer outline edge, the single mesh
emits one tall wall panel `0 → top`; the split must reconstruct it as **stacked** `base`
(`0 → base`) + `border` (`base → top`) panels sharing a `z = base` mid-edge with matching
triangulation, or the oriented faces do not cancel and union ≠ single even with no pinch. This
panel decomposition is required for the §4 bordered example to satisfy the Validator; it is
independent of the pinch obstruction (it fails even on pinch-free borders).

### 5.5 Validator

**Validator:** `bikar render <coaster> --format parts --pinch fillet` emits exactly one
2-manifold body per non-empty region, **each passing `--check` on its own** — because an
aggregate cannot discharge a per-part claim, a valid *total* triangle count does not certify
three valid bodies; one pinched body among many stays hidden in a total. The union of the
bodies equals the single-body `--format stl` mesh **everywhere outside cells thinner than
CAL-PIN-01** (exactly, under `--pinch merge`; up to the fillet floor, under `--pinch fillet`).
A region named by a `color` statement but holding no cell is refused; a debossed region (no
raised body, D-066) is refused.
- PASS: the §4 bordered hexagon, `color base Slab`, `color straps Gold`, `color border Gold`,
  under `--pinch fillet` — three bodies, each 2-manifold and `--check` clean *individually*;
  the border outer wall decomposes into stacked base+border panels (§5.4); re-merging
  reproduces the single-body STL everywhere outside the sub-floor fillet notches.
- FAIL: the hard cases, each caught **per body, not in aggregate** — (i) the octagram under
  `--pinch error` refuses, naming a pinch `(x, y)`, the by-design refusal the strategy exists
  to give; (ii) a single strap body left with one unfilleted pinch (a strategy-resolution bug)
  fails `--check` on **that body alone** — four faces at the pinch edge — while the other two
  bodies and the total triangle count read clean; (iii) a debossed coloured region → empty
  body → error; (iv) a `color straps Gold` naming a region with zero relief cells → refused
  (a zero-triangle body mapped to a spool is a phantom filament the composer cannot detect).

FAIL is exercised by constructing the pinched / empty / debossed spec — because a manifold
defect is a kernel fault, not a grammar one — and the pinch FAIL uses a *saddled* pattern
(octagram), the case the naïve split provably could not make, not a gentle one it always could.

## 6. Plate composer — palette name → AMS slot (a dependency, not owned here)

The per-body 3MF and the AMS-slot map are the **plate composer's** job (umbrella task P4.1),
which has its own design target, docs/plate-composer-design.md (not yet written — named in
prose, not linked, because a link to a missing file is a D1 failure). This doc hands the
composer a clean contract: N named bodies, each tagged with its region's palette name. The
composer maps *palette name → AMS slot* and writes the project 3MF; the slicer binds a
physical spool.

**VERIFIED / RESOLVED (was UNVERIFIED), the composer's to implement:** the headless-CLI 3MF
contract is now settled by [`coaster-ams-3mf-contract.md`](research/coaster-ams-3mf-contract.md).
The answer, scoped to headless CLI slicing: **per-object filament→slot assignment must be
baked into the *input* 3MF** — the CLI has no flag that maps objects or painted regions to
slots at slice time. The mapping lives in the 3MF as per-object/part `extruder` attributes in
`Metadata/model_settings.config` and per-triangle `paint_color` bitmasks in `3D/Objects/*.model`,
and the slicer only honours them when the 3MF's Application metadata starts with `BambuStudio-`
(else it imports single-colour, BambuStudio#9666). `--load-filaments` is **override-only**: it
loads filament profiles into the slots the 3MF *already declares*, by list order, and does not
create or reassign them (settings precedence: command line > `--load-settings`/`--load-filaments`
> values embedded in the 3MF). This confirms the earlier hedge's cautious reading was right: the
GUI-can-assign-after-import behaviour does **not** carry to the CLI. So the composer must emit the
per-body `extruder` tags (and any `paint_color`) into the 3MF itself — it cannot lean on
`--load-filaments` to do the assignment. The colour route does not depend on the answer; this
resolves the dependency for the composer, it does not move ownership here.

**Caveat carried (K1), do not overclaim:** the finding is about *headless CLI* slicing, and a
**logical filament slot ≠ a physical AMS slot** — the CLI slice carries only the logical filament
index order; the physical AMS mapping is resolved interactively / at print time by colour match.
`--load-filaments` silently under-fills or errors if its count exceeds the slots the 3MF uses.

## 7. Coaster Lab knob

The Coaster Lab lives in `bikar/packages/lab` (the Orb Lab pattern, [D-067](decisions-log.md)).
Colour per region is a knob that **edits the `color` statements** — the same way every Lab
knob edits DSL, not a hidden side-channel — with one dropdown per region (`base`, `straps`,
and `border` when the coaster has a band), each choosing a name from the file's `palette`.
The preview **tints each region** by the palette hex, so the author sees the three regions
before export.

This reuses the Lego Lab precedent that a render is classified to *the model's own palette*,
not a global set ([`lego-lab-design.md`](lego-lab-design.md) §16.1). The transfer note (K10):
the Lab borrows the **region-is-a-named-colour** idea and the per-model palette, **not** the
Lego pixel/`visibleColours` gate — a coaster's regions are checked geometrically by the §5
per-body Validator (watertightness), because the print's correctness is that each region is a
separate body, not that a render shows a given colour. The pixel gate does not transfer; its
reasoning (classify to the model's own palette so it ports where pixels do not) does.

## 8. Decisions

- **D-073**: coaster colour is `color <region> <PaletteName>` over the three symbolic regions
  `base | straps | border`; the region names what is distinct and never a filament id; the
  kernel exports one body per non-empty region via `--format parts` (each passing `--check`,
  the split requiring emboss, D-066; the pinch handling is **D-074**); the plate composer maps
  palette name → AMS slot (P4.1, dependency, not designed here); a Coaster Lab knob edits the
  `color` statements and tints the preview per region. See [`decisions-log.md`](decisions-log.md).
- **D-074**: the naïve split's two invariants — union *exactly* == the single body **and** each
  body 2-manifold — are provably incompatible for saddled patterns (a pinch at any interior
  `z = base`, §5.1), a K7 contradiction in the first draft of §5. Resolution: **detect** every
  pinch (§5.2) and resolve it by a CLI strategy `--pinch fillet|merge|error` (§5.3), `fillet`
  the default. `fillet` raises pinches to the printable floor (**CAL-PIN-01**), so union ==
  single holds everywhere outside sub-floor notches; `merge` keeps union exact by recolouring
  the pinch to `base`; `error` refuses with coordinates. The border outer wall is decomposed
  into stacked base+border panels (§5.4). `--format stl` is unchanged. Chosen over scoping the
  feature to pinch-free coasters (the earlier Option A) because Option B makes every pattern
  print. See [`decisions-log.md`](decisions-log.md).
- **D-068** is the direction this builds; **D-071** gives the first region split; **D-066**
  fixes the relief as an emboss; **D-067** places the Lab — all unchanged.

## 9. Not yet

- **Nothing has been printed**, and the route adds **no new *print* bet**: the coloured bodies
  are the same seated emboss straps on the same slab as a single-filament coaster (CAL-CST-01's
  case, [`coaster-design.md`](coaster-design.md)) — same load, same adhesion, same shells.
  The multi-material interface between two filaments on the shared slab face is a print-time
  adhesion question the plate-composer's first print (P4.3) records, not a geometry bet here.
  The one bet the split *does* add is **CAL-PIN-01** (§5.3): a *geometry* threshold — the pinch
  floor below which `fillet` thickens — not a print/adhesion bet, and settled by measuring a
  two-filament interface, not by this print.
- **The composer's 3MF contract is now settled** (§6, [`coaster-ams-3mf-contract.md`](research/coaster-ams-3mf-contract.md)):
  the headless CLI needs per-object filament baked into the input 3MF, `--load-filaments` is
  override-only. What remains open is the composer's *implementation* of that emit recipe (and
  the logical-vs-physical AMS-slot binding at print time) — it belongs to the composer doc, not
  this one.
- **Region-scoped relief.** A region embossed while another is debossed is a second relief
  statement scoped to a region; the region bit is where that scope would attach
  ([`coaster-border-design.md`](coaster-border-design.md) §10). A debossed region carries no
  colour body (§5) — so region-scoped deboss and per-body colour are mutually exclusive on
  the same region until a "recessed inlay" solid exists, which is a new form, not this one.
- **More than three regions.** Corner motifs (the border doc's option (c)) or a second band
  would add region names; the vocabulary of §3 is closed at three because the geometry is.
