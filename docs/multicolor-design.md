# Multicolour constructions — the consolidated design

A construction coaster today is only its lines: straps standing up from a one-colour slab. This
design fills some of the **shapes** the lines enclose, gives them colours by Omar's rule, and
prints the coaster in several filaments on the X2D with the AMS.

*Status: consolidated design, the one to act on. It supersedes the two research designs it was
built from, researcher A's [multicolor-constructions-design.md](multicolor-constructions-design.md)
and researcher B's [multicolor-constructions-b-design.md](multicolor-constructions-b-design.md),
which stay as the record. The checker's raw notes, measurements and re-fetched sources are in
[research/multicolor-verification.md](research/multicolor-verification.md). No decision id is
taken: the look (§3) and the grammar change (§2) are Omar's to approve; an id is taken with
`tools/next_id.py` when he does. Nothing here has been sliced in the Bambu Studio window or
printed.*

## 0. What this doc decides, in one screen

| Question | Recommendation | One-line reason |
|---|---|---|
| How are shapes grouped into colour classes? | A new fill word **`orbit`**: faces that a rotation (or, where the pattern has a mirror line, a reflection) about the pattern's centre carries onto each other | It is Omar's rule stated as a test the engine can check face by face; `ring` breaks it on 7 of the 8 coasters measured |
| Which word? | **`orbit`**, not `class` | `class` already means `.class` tags and `classify` in the language; `orbit` is already the importer's word for exactly these copies |
| Where is the centre? | The **area-weighted centroid** of the faces, refused when the faces have no symmetry about it | Any symmetry of the face set fixes that point; B's "outermost `rotate N around`" rule refuses 7apC5Q9QS-8, which has no such block |
| Flush or lowered fills? | **Build flush first; add the fill height as one knob on the same path; the look is Omar's call** | Flush builds and passes every gate today (reproduced); lowered halves the colour-change layers but needs a parser and kernel change first |
| How do colours reach the printer? | The shipped route: `--format parts` → multi-part 3MF → `bambu slice coaster` | Both researchers agree; nothing new on the printer side |
| How many colours? | **Warn, not cap**, slots read from the machine (D-078), not A's fixed 4 | D-078 already decided it; A's cap contradicts a shipped decision |
| bikar PR #261 | The two kernel fixes are sound and should land; the prototype preset should wait for Omar's look call | §9 |

## 1. The ask and how the rule is read

Omar, 2026-09-26: "alternative version of concatructiona ... where we have multi colors shapes
(fill in some of the traces) instead of just a trace and that we can print in multiple colors", and
"shapes that are translationns same midpoint from center should be same color".

Both researchers read the rule the same way, and this doc keeps it: two filled shapes share a
colour when one is a copy of the other moved about the pattern's centre (in a rosette the move is a
rotation, so "translation" is read as "moved copy") **and** their centres sit the same distance from
the pattern's centre. Each such group is a **colour class**.

This is close to, but not the same as, the ask D-078 answered on 2026-09-19 ("polygons whose
midpoints are equidistant from midpoint of construction"), which chose the radius-only `ring`
([D-078](decisions-log.md)). The new rule adds **same shape**, and §2 shows the difference is real.

## 2. Colour classes: the `orbit` word

### 2.1 What was measured

Both researchers and the checker compiled the construction coasters with the built engine and
compared the engine's rings with the classes. The checker re-ran it on bikar main
([verification §2](research/multicolor-verification.md#2-results-on-the-plain-coaster-files-at-their-default-size-mm)):

- On **7apC5Q9QS-8** the rings are exactly the classes (16 and 16, none split) — *when a mirrored
  copy counts as the same class*. Rotation-only gives 24 classes. A and B agree; reproduced.
- On the **other 7** plain construction coasters, most classes are spread over several rings
  (GimTvN9hw4U: 7 of 8 classes split; sDO9fpu76v8: 34 of 35). The cause is the ring centre: the
  engine measures from the first circle defined, which is (0,0), not the rosette's centre, on those
  files. So colouring by `ring` gives matching shapes different colours — the opposite of the rule.
- On all 8 files, "congruent and same radius" gives the same classes as the stricter orbit test.
  B's worry that the two could differ did not occur in this set. The survey is these 8 files only.

### 2.2 The options

| Option | Pros | Cons | Implications |
|---|---|---|---|
| **`ring` as it is** | No work; D-078 carries it to the print already | Right on 1 of 8 coasters | Every other file needs hand-picked ring lists, where mistakes creep in; the rule is not what the engine checks |
| **Move the ring centre** to the symmetry centre | No new word | Changes what `ring == N` means in the **10** `.bkr` files on bikar main that select by ring (B counted 8); radius only, so two shapes at one radius still share a ring | One word with an old and a new meaning during the move — the defect this repo's CLAUDE.md says to delete, not hide |
| **`class == N`** (B) | Exactly the rule | `class` already names `classify .name`, `.class` tags and `connect arc … .CLASS` in the language | Two meanings for one word, the trap [D-078](decisions-log.md) itself rejected option (b) for |
| **`orbit == N`** (A; recommended) | Exactly the rule; leaves `ring` alone; `orbit` already means "the rotation copies of a leaf" in bikar's GeoGebra importer (lower.ts, "kept as an orbit tree") | A grammar edit: one word in the parser's attribute list plus a resolver | `ring` stays for "bands at a radius", a real and different idea; `bikar bands` lists orbits beside rings (one listing verb, not B's second `bikar classes`) |

**Recommendation: `orbit`.** A proposed it; B proposed the same idea under the name `class`. The
evidence that decides the name is in bikar's own code (verification §5), not a preference.

D-078 rejected a "second radial grammar". `orbit` is not one: it groups by shape **and** position,
and it answers a different rule from the one D-078 answered. Reusing `ring` was right for D-078's
rule and is wrong for this one.

### 2.3 How the engine finds orbits

1. **Centre.** The area-weighted centroid of all bounded faces (A). Any rotation or reflection that
   carries the face set onto itself fixes that point, so it *is* the symmetry centre whenever there
   is one. Measured: it is a true centre on 7 of the 8 coasters (whole-set rotation order 4 to 18,
   with a mirror line).
2. **Refuse when there is no symmetry.** If no rotation and no reflection about the centre carries
   the face set onto itself, `orbit` refuses with that reason rather than guessing (B's refusal,
   applied to A's centre). Measured: this refuses n3IidKfXE1I, which both researchers found has no
   single centre, and nothing else in the set.
3. **Orbit test, per pair.** Face b is in face a's orbit when a rotation about the centre carries
   every vertex of a onto a vertex of b within τ, or a reflection through a line through the centre
   does **and** the whole face set has a mirror line through the centre (B's mirror rule). On the 7
   symmetric coasters this gives the same classes as A's "mirrors always count"; the two differ
   only on a chiral pattern, where B's rule does not invent a symmetry the drawing lacks.
4. Orbits are numbered from the centre outwards, like rings.

**Why not B's centre rule.** B takes "the centre of the outermost `rotate N around X`". On
7apC5Q9QS-8 there is no such block (the rosette is built from `reflect … across` steps), so the rule
refuses the one file both researchers agree on. On the rDux coaster there are twelve such blocks
about several centres. Evidence: verification §3.

**Default:** τ = 0.02 (in the pattern's own units; millimetres on a coaster), researcher B's
1e-3 × unit at unit 20 ([3d-models PR #347](https://github.com/omars-lab/3d-models/pull/347)),
fixed rather than scaled because a coaster's size is set in millimetres. Every class on the 8
coasters passes the orbit test at 0.02, and the tightest gap between two congruent faces in
different classes, about the true centre, is 1.17 mm (n3IidKfXE1I and sDO9fpu76v8), so 0.02 sits
about 58× below it ([verification §2 and §4](research/multicolor-verification.md#4-tolerances)).
This transfers to another pattern only if its coordinates are on a similar scale (tens of units
across); the `bands` listing prints the tightest congruent gap so a closer pair is visible. The
orbit test does not need τ to separate classes: a rotation keeps radius, so two faces at different
radii can never pass it, whatever τ is. τ only absorbs floating-point noise.

A's 0.05 mm radius tolerance was justified by a 0.22 mm gap between two **different** shapes on
7apC5Q9QS-8 (rings 9 and 10); the congruence test already separates those, so that gap never
bounds the tolerance. B's hard pair (§7) is the gap that does.

### 2.4 Choosing which orbits carry colour

Both researchers agree: the author picks, nothing is merged automatically.

1. `bikar bands <file>` lists orbits (id, member count, sides, area, radius) beside rings.
2. `fill void where orbit == N color <Name>`. Several orbits may share a palette name; that is how
   a design has more classes than spools (7apC5Q9QS-8 has 16 classes).
3. Unfilled orbits keep the base colour (how depends on §3).

## 3. The look: flush or lowered fills

The coaster is one height field on a 0.4 mm grid (CAL-FEA-01) and every printed body is cut from
it by column, so neighbouring colour bodies share faces exactly, with no overlap, no gap and no
boolean union. Both researchers found this and it holds for every option below.

| Option | What it is | Pros | Cons | Implications |
|---|---|---|---|---|
| **Flush** (A) | `relief both`: filled faces rise to the strap height; unfilled faces are filled with the base colour name so they rise in the slab colour | **Builds today** with #261's two fixes; all four bodies pass `--format parts --check` at 90 and 80 mm (reproduced); a flat top, like a mosaic | Every relief layer holds every colour: at 0.2 mm layers, 6 layers × (colours) changes; the only line between two colours is the colour edge, so any bleed is on the top face | No grammar change; the unfilled-face trick is one extra `fill` line |
| **Lowered** (B, "cloisonné") | Fills rise less than the straps (B proposes 0.4–0.8 mm against 1.2 mm straps) | Fewer multicolour layers: at 0.6 mm, 3 of the 6 relief layers hold several colours and the top 3 hold only the strap colour — about half the colour changes, if purge scales with changes as the fetched guides say; a strap wall stands at every colour edge, where a ghost of the previous colour would show | **Does not build today**: the parser refuses a second `relief` clause and the kernel has one relief height; the fill depth has no source | A parser change and a kernel change (a top height per body); the depth needs a print to settle |
| Face-down mosaic (B's C) | Coaster printed upside down, colour in the first layers on the bed | Crisp flat face | Loses the raised straps; multicolour first layer with small islands; a new split mode | A second style, not a variant; not pursued now |
| Stained glass, full-height plugs, height terraces (B's D, E, F) | — | F works without an AMS | D needs the openwork split refusal lifted; E makes every layer multicolour; F cannot put two colours in one layer | Out of scope for the X2D path |

**What the evidence says.** A's case against a lowered fill ("a mug rocks if the fills stand
proud"; "grooves") does not hold for B's version: B's fills sit *below* the straps, so a mug sits
on the straps exactly as it does on today's plain coaster, and the pockets are shallower than
today's 1.2 mm unfilled pockets. B's case that lowered hides bleed is plausible and unmeasured. The
purge argument for lowered rests on two fetched guides ("purge cost scales with the number of color
transitions", bambureviews; "the fastest way to reduce waste is to reduce colour changes", Sovol)
and arithmetic on the layer count, not on an X2D measurement.

**Recommendation.** One code path, not two modes: a fill height on the relief clause, where flush
is the case fill height = strap height. Build order follows what exists: flush first (it is built
and gated), then the fill height. Which look Omar wants on the shelf is **his taste call**; the
first sample plate that has both (§10) is where he makes it.

**Default:** fills flush with the straps (fill height = strap height, 1.2 mm), as in bikar
[PR #261](https://github.com/NaqshCoffee/bikar/pull/261)'s prototype, the one version that is built
and passes the mesh gate; the 1.2 mm rise stays inside the relief aspect bet CAL-CST-04. This is a
build-order default, not a verdict on the look.

**Proposed syntax for the fill height** (one clause, so no second `relief` statement is needed):
`relief both emboss 1.2 fills 0.6` — straps to 1.2 mm, every face to 0.6 mm; omitted, faces go to
the strap height (flush). B's alternative, a second clause `relief faces emboss 0.6 filled`, needs
the parser to accept two relief clauses and gives `relief faces` a second reading; the one-clause
form avoids both. Under either form, unfilled faces take the base colour name, as in the prototype.

### 3.1 Strap wins (both researchers; built in #261)

A face outline *is* a strap centreline, so without a rule each filled face takes half of every strap
beside it. Both researchers found this and gave the same rule: a raised cell within half a strap
width of a strap centreline belongs to the strap. #261 implements it for `relief both`; a lowered
fill must use the same rule. Measured on bikar main: without it the prototype's straps body shrinks
to its outer ring (euler 0) **and every mesh gate still passes** — the case §7's second validator
exists for.

## 4. Getting the colours to the printer

Both researchers agree, and the route is shipped: `--format parts` writes one body per palette
name plus base and straps ([D-073](decisions-log.md), [D-074](decisions-log.md)); palette name →
logical AMS slot by first-seen order is baked into a multi-part input 3MF
([D-075](decisions-log.md)); `bambu slice coaster` slices it headless, verifying geometry, while
colour is checked in the Studio window ([D-077](decisions-log.md)). Since #349 the slicer flattens
each preset chain and checks the slice carries it. Separate STLs per colour were considered by both
and rejected: registration by hand every print, and D-075's contract thrown away.

### 4.1 How many colours

- **Slots are read from the machine** with `bambu filament`, which lists the loaded trays; it was
  confirmed on the live X2D on 2026-09-17. Both researchers agree.
- A proposed "at most 4 colours per coaster"; B follows D-078's **"warn, not cap"**. D-078 is a
  shipped decision, so the slice step warns when palette names exceed loaded trays and does not
  refuse. A's §7.1 "the slice step refuses" is dropped.
- The AMS slot count (4 per unit) and the X2D maximum ("up to 25 colours" with many units) are
  **snippet-only** in both researches and again on 2026-09-27: the Bambu store page returned 402,
  the X2D FAQ 403. No number here rests on them.
- The first plate stays within 4 palette names, so it fits one loaded AMS whatever the maximum is.

### 4.2 Purge, bleed and the second nozzle

- Each change purges to the chute and then primes a tower (forum user reports and the Printago
  guide, fetched; not X2D-specific).
- Dark-to-light changes show bleed most (Sovol, bambureviews, fetched). The hard test is a light
  fill next to a dark strap.
- Whether the X2D's second nozzle cuts purge for a two-colour coaster: B said no fetched source
  states it; A said "may, not confirmed". A forum thread fetched on 2026-09-27 has users saying one
  AMS can feed both nozzles through the track switch, with "lower amount of purging", at the cost of
  a full retract per nozzle change. User reports only; **unverified**.

## 5. Printability

- **Bed side.** The slab is one colour and every colour body starts at the slab top, so the first
  layer has no colour change. Both agree; true by construction of the height field.
- **Smallest fill.** Under flush, #261's second fix hands any tip thinner than one 0.4 mm cell back
  to the strap, so a fill loses sub-cell tips (A, measured). B proposed that a face narrower than the
  strap floor CAL-CST-01 is not filled at all. That floor was set for one filament; it transfers to a
  fill only if a two-colour pocket prints at least as well as a one-colour rib, which is the open
  question CAL-PIN-01 carries. Neither is measured on a print.
- **Pinches.** A fill corner meeting the slab is the two-filament interface CAL-PIN-01 names (both
  agree); the shipped `--pinch fillet` applies.
- **Edges.** Colour edges step at the 0.4 mm grid. How that looks at arm's length is unknown.
- **Styles.** `--format parts` refuses deboss, `outline pattern` and the slab-reshaping clauses, so
  only the plain and border styles can carry fills today (both agree; [coaster-colour-design.md](coaster-colour-design.md)).

## 6. What a `.bkr` says

Today, on 7apC5Q9QS-8 only (ring equals orbit there), as in #261:

```
  palette pal
    Slab = #333333
    Gold = #d4af37
    Ruby = #9b1b30
  fill void where ring == 0 color Ruby
  fill void where ring == 3 color Ruby
  fill void where ring != 0 and ring != 3 color Slab

coaster Coaster
  outline square $size
  inscribe c_7apC5Q9QS_8
  base $height
  relief both emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
```

After the grammar change, on any symmetric construction:

```
  fill void where orbit == 2 color Ruby
  fill void where orbit != 2 color Slab
...
  relief both emboss 1.2 fills 0.6
```

## 7. Validators

**Validator:** every face in an orbit carries the same colour, checked face by face. For every face
that is a member of an orbit, (a) a rotation about the centre — or, where §2.3 admits mirrors, a
reflection — carries the orbit's first member onto this face within τ, and (b) this face's palette
name equals the first member's. It reports the first failing face. A count of colours per orbit
cannot stand in for it: one odd face in a ring of twelve leaves every total looking right.

PASS: 7apC5Q9QS-8 with orbit 0 and orbit 3 in Ruby and every other orbit in Slab — every face maps
onto its orbit's first member and carries its colour (the prototype's colouring, since orbits equal
rings on this file).

FAIL: the rDux coaster measured about the wrong centre O, or grouped by radius with any tolerance of
0.18 mm or more: two congruent hexagons at r = 45.474 and 45.652 mm fall into one group, and check
(a) fails on the second, because a rotation keeps radius. This is B's hard case (51.06 vs 51.26 at
unit 20 on the root file, reproduced exactly) carried to the coaster
([verification §3](research/multicolor-verification.md#3-rduxhf3xmoc--bs-hard-case-and-why-a-and-b-disagree-on-it)).
It catches the merge whatever τ is.

FAIL: an orbit filled Gold plus a later `fill where index == 17 color Red` that hits one member —
check (b) fails on face 17 alone.

**Validator:** the straps body owns every strap cell. For every raised cell within half a strap
width of a strap centreline, the body that owns the cell is `straps` (or `border` in the band),
checked cell by cell on the split, next to the mesh gate.

PASS: the prototype on #261's build — straps body euler −200, the inner octagon strap present.

FAIL: the same file on bikar main (8e68778), before fix 1. This is the hard case because **every
mesh gate passes** (base, Slab, Ruby and straps all watertight); the straps body is one outer ring
(euler 0) and the interior straps belong to the fills. Only a per-cell check or a picture of the
actual bodies catches it; the plate picture is drawn from the 2D drawing and shows the straps that
are not there.

## 8. Where A and B agreed, disagreed, and what the sources say

Verdicts: **agree** (both found it); **A only / B only**; **disagree** (and which side the source
backs); **snippet-only** (not fetched, so not load-bearing). Evidence is the checker's re-run or
re-read unless it says otherwise.

| Claim | Who | Verdict | Evidence |
|---|---|---|---|
| The shapes are the engine's bounded faces; `fill void where … color` already colours them | both | agree | fill-resolver.ts read at main |
| `ring` is measured from the first circle's centre, not the rosette's | both | agree | evaluator.ts `findCenter` L10060 |
| Rings equal classes on 7apC5Q9QS-8 (16 and 16, none split), with mirrors counted as the same class | both | agree, reproduced | verification §2 |
| Rings split classes on the other 7 files | both | agree, reproduced | verification §2 (split counts 3 to 34) |
| Per-file class counts | both | agree on 6 files; **A's n3IidKfXE1I 58 not reproduced** (checker: 39 with mirrors, 58 without) | verification §2 |
| rDux has 17 classes (A) vs 38 (B) | both | **both right, different files**: A the coaster about its true 4-fold centre; B the root file about O | verification §3 |
| rDux hexagons at r 51.06 and 51.26, 0.20 apart | B only | reproduced exactly (0.2003) on the root file about O; 0.179 mm on the coaster about O; 3.09 mm about the coaster's true centre | verification §3 |
| Closest classes 0.22 mm apart on 7apC5Q9QS-8, so tolerance must stay below | A only | true but not load-bearing: different shapes, separated by the shape test | verification §4 |
| Centre = area-weighted centroid (A) vs centre of the outermost `rotate N around` (B) | disagree | **A backed**: B's rule refuses 7apC5Q9QS-8 (no such block) and is ambiguous on the rDux coaster (12 blocks) | verification §3 |
| Mirror copies: always the same class (A) vs only when the pattern has a mirror line (B) | disagree | no difference on the 7 symmetric coasters; B's rule is the safer one on a chiral pattern | verification §2 |
| Selector word `orbit` (A) vs `class` (B) | disagree | **A backed**: `class` is taken in the language; `orbit` already means this in the importer | verification §5 |
| Tolerance 0.05 mm on radius (A) vs 1e-3 × unit on the orbit test (B) | disagree | B's orbit test is τ-independent for merges; 0.02 passes every class | verification §4 |
| Filling eats half of each strap; the strap must win within half a strap width | both | agree; A built and tested it | #261 tests fail 2 of 6 on main |
| Corner-only touches make both bodies non-watertight once straps win | A only | reproduced via A's tests; the watertight test passes on main because the defect needs fix 1 first | verification §6 |
| Unfilled faces rise in the strap colour under `relief both` | A only (B: `relief faces` raises every face) | agree in substance | coaster.ts read |
| Flush builds and passes the mesh gate at 90 and 80 mm | A only | reproduced (euler 2, 184, 18, −200 at both sizes) | verification §6 |
| A lower fill cannot be written today | B only | confirmed: one relief height in the AST, and a second `relief` clause is refused | verification §5 |
| "A mug rocks if the fills stand proud" (against lowered) | A only | does not apply to B's fills, which sit below the straps | geometry |
| Lowered fills cut colour-change layers | B only | arithmetic holds at 0.2 mm layers; purge scaling rests on fetched guides, not an X2D measurement | bambureviews and Sovol, fetched |
| Straps as walls hide bleed | B only | plausible, **unmeasured** | — |
| Purge scales with colour transitions, not colour count | both (different sources) | agree; both sources fetched | bambureviews, Sovol |
| Dark-to-light shows bleed most | both | agree; fetched | Sovol, bambureviews |
| Each change purges to the chute then a prime tower | A only | fetched, user reports on an older printer | Bambu forum, Printago |
| 4 slots per AMS; X2D up to 25 colours | both | **snippet-only**; fetch refused again (402, 403) | verification §7 |
| At most 4 colours per coaster, the slice step refuses beyond | A only | **contradicted by D-078** ("warn, not cap") | [D-078](decisions-log.md) |
| Second nozzle may cut purge | A (hedged); B: no source | forum users say yes for one AMS feeding both nozzles; user reports, **unverified** | verification §7 |
| Only plain and border styles can be split | both | agree | coaster-colour-design |
| No boolean union; bodies share faces | both | agree | height-field split |
| First layer is one colour | both | agree; by construction | height-field split |

## 9. bikar PR #261 — verdict

**The two kernel fixes should land on their own merits.**

- Fix 1 (strap wins on `relief both`): its tests fail on main and pass on the branch; it removes a
  defect the mesh gate cannot see (§7); it changes no shipped coaster, because no `.bkr` on main uses
  `relief both`.
- Fix 2 (corner-only touches go to the strap): runs only when a colour is present, only moves cells
  from a colour body to its region body, and ends because colour cells strictly fall. Its test does
  not fail on main by itself — the defect appears only with fix 1 in — so it and fix 1 should land
  together.
- The branch merges with main (8e68778, which touched the same file in #262) without conflict, and
  the kernel test folder passes (71 files, 1149 tests).

**The prototype preset is technically safe but should not merge yet.** It passes every gate, but
merging it publishes a Coaster Lab preset, a thumbnail and a public-surface entry with a colour
choice Omar has not seen, colours by `ring` (right on this one file only), and fixes the look to
flush before §3's taste call. Recommended: split the PR — the fixes and their tests (with the
fixture moved beside the tests) first; the preset after Omar picks the look and colours. Merging is
Omar's; nothing was merged here.

## 10. Next steps, smallest first

1. **Omar looks** at #261's body picture and says whether flush is a look he wants on the shelf
   (§3). No build.
2. **Slice the prototype** through `bambu slice coaster` and open it in the Studio window: three
   palette names should land on three filaments. No print. Checks the one link in §4 nobody has run.
3. **Land #261's fixes** (split as §9 says), after Omar's go.
4. **The strap-ownership check** (§7, second validator) in the parts gate, so the lost-straps defect
   cannot come back silently.
5. **`orbit`**: the attribute word, the resolver (§2.3), orbits in `bikar bands`, and the first
   validator. One grammar edit through the main session.
6. **The fill height** (`fills <mm>`, §3), reusing the strap-wins rule.
7. **First sample plate** (owner-gated; printing is paused until a CAL bet settles): 7apC5Q9QS-8 at
   80 mm, three or four palette names — flush vs 0.6 mm lowered, and a light fill next to a dark
   strap. Look at bleed, the grid staircase, lost star tips, and the slicer's purge and time.

## 11. Still unverified

- No slice of a coloured coaster has been opened in the Studio window, and nothing has been printed.
- Bleed, purge per change and time on the X2D; whether strap walls hide bleed; whether the second
  nozzle cuts purge.
- How visible the 0.4 mm staircase is on colour edges.
- The AMS slot count and the X2D colour maximum (snippet-only).
- The fill depth for a lowered fill; the minimum fill width (CAL-PIN-01 and CAL-CST-01 do not
  transfer until a coupon shows it).
- Whether the lowered fill needs fix 2 too (likely, since its cells are raised, but not built).
- Why A's n3IidKfXE1I count (58) differs from the checker's (39).
- The survey is the 8 plain construction coasters in bikar's Constructions folder; nothing here is
  claimed about other patterns.

## 12. Read against itself (K7) and transfer conditions (K10)

- §0, §3 and §10 agree: flush is built first, the look is Omar's, lowered is a knob on the same
  path. §3's `**Default:**` is a build order, and says so.
- §2.3 says B's centre rule refuses 7apC5Q9QS-8; §7's PASS uses 7apC5Q9QS-8 with A's centre, so the
  PASS is built from the machinery this doc recommends.
- §7's hard FAIL uses the wrong centre or a radius-only grouping, not the recommended τ = 0.02: it
  exists to show the orbit test does not depend on τ, as §2.3 says.
- §4.1 drops A's cap because D-078 says warn; §10 step 7 keeps the plate to 4 names for a reason
  that does not depend on the cap (one loaded AMS).
- **K10, τ:** measured on 8 coasters in millimetres; transfers where coordinates are on a similar
  scale. The orbit test covers merges without it.
- **K10, purge:** the guides are general Bambu Studio advice; they transfer to the X2D if it flushes
  per change like other AMS printers, which no fetched source tests.
- **K10, CAL-CST-01 → fill width:** transfers only if a two-colour pocket prints at least as well
  as a one-colour rib; not shown.
