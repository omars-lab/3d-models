# Coaster colour regions — a symbolic name per region, one body per colour, a filament map at the slicer

*Status: designed (task #37, decision D-073). The direction is D-068 (coaster-level
composition): a coaster's cells already split into named regions; this doc gives those
regions a colour vocabulary in the DSL, a per-body export so each region prints in its own
filament, and a Coaster Lab knob to set it. It builds directly on the border band of
[`coaster-border-design.md`](coaster-border-design.md) (D-071), which recorded the first
region split (band vs field), and on the emboss decision of D-066. It adds no new solid and
no new bet. Research on file: [`research/coaster-colour-research.md`](research/coaster-colour-research.md).*

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

`bikar render <coaster> --format parts` splits the one height field into one watertight
body per region that has at least one cell:

1. **`base`** is the slab prism to `z = base`.
2. **`straps`** is the field relief — emboss prisms standing on the slab's top face.
3. **`border`** is the band relief — emboss prisms on the slab's top face, present only with
   a `border` clause.

The bodies **share coincident faces** at the slab top where a relief prism meets the slab,
so their union is exactly the single-body `--format stl` mesh with no gap and no overlapping
volume. Each body is closed on its own and passes `--check` (the mesh gate every coaster
render already runs, [`coaster-design.md`](coaster-design.md)) independently. This reuses
the existing kernel: `reliefAppliesAt` already reads by region (D-071); `--format parts`
changes only *how the sampled field is assembled into meshes*, not what is sampled.

The split requires an **emboss**, which is already the decided relief mode — a deboss
removes material and leaves the slab's own colour, so a debossed region has no raised body
to carry a filament ([D-066](decisions-log.md)). This is the transfer condition on the
split: it is meaningful only while the relief embosses; a future debossed region exports an
empty body, which the Validator below refuses rather than silently emitting.

**Validator:** `bikar render <coaster> --format parts` emits exactly one watertight body per
non-empty region, each passing `--check` on its own, and the union of the bodies is
face-coincident with the single-body `--format stl` mesh (no gap, no overlap). Every named
region either carries ≥ 1 cell and a body, or is absent from the file; a region named by a
`color` statement but holding no cell is refused. Because an aggregate cannot discharge a
per-part claim, each body is checked on its own — a valid *total* triangle count does not
certify three valid bodies.
- PASS: the §4 bordered hexagon with `color base Slab`, `color straps Gold`, `color border
  Gold` — three regions, three watertight bodies, each `--check` clean; re-merging the three
  reproduces the one-body STL exactly.
- FAIL: (the hard case) a coaster whose `border` run holds no whole motif — CV11's `N = 0` case
  ([`coaster-border-design.md`](coaster-border-design.md) §6.2) — so the `border` body would
  be **empty**: `--format parts` errors (a zero-triangle body mapped to a spool is a phantom
  filament the composer cannot detect), and separately, a split whose strap prisms meet the
  slab on a **non-coincident seam** leaves a non-manifold edge that fails `--check` on the
  merged mesh though each body reads closed alone. Both are by-design failures this Validator
  exists to catch; neither is visible in a total triangle count.

FAIL is exercised the way the border's CV11(ii) is — by building a spec whose region split is
forced to an empty body or a seam offset — because a manifold defect is a kernel fault, not a
grammar one.

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
  kernel exports one watertight body per non-empty region via `--format parts` (each passing
  `--check`, the split requiring emboss, D-066); the plate composer maps palette name → AMS
  slot (P4.1, dependency, not designed here); a Coaster Lab knob edits the `color` statements
  and tints the preview per region. See [`decisions-log.md`](decisions-log.md).
- **D-068** is the direction this builds; **D-071** gives the first region split; **D-066**
  fixes the relief as an emboss; **D-067** places the Lab — all unchanged.

## 9. Not yet

- **Nothing has been printed**, and the route adds **no new bet**: the coloured bodies are
  the same seated emboss straps on the same slab as a single-filament coaster (CAL-CST-01's
  case, [`coaster-design.md`](coaster-design.md)) — same load, same adhesion, same shells.
  The multi-material interface between two filaments on the shared slab face is a print-time
  adhesion question the plate-composer's first print (P4.3) records, not a geometry bet here.
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
