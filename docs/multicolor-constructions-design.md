---
status: superseded
---

# Multicolor constructions — filled, colored shapes on a coaster

> **Superseded by [multicolor-design.md](multicolor-design.md)** (the checker's consolidated
> design, 2026-09-27). This is researcher A's design, kept as the record it was built from.

Today a construction coaster is only its lines: the pattern's straps stand up from a slab.
This design fills some of the **shapes** the lines enclose (stars, petals, polygons) and gives
them colors, so one coaster prints in several filaments on the X2D with the AMS.

*Status: proposed, with a working prototype. The research, the survey and every web source
(fetched or search-summary only) are in
[`research/multicolor-constructions.md`](research/multicolor-constructions.md). The prototype
is bikar [PR #261](https://github.com/NaqshCoffee/bikar/pull/261) (branch `feat/multicolor-fills`), not merged. No decision id is taken
here; one is taken with `tools/next_id.py` when Omar picks.*

![The prototype's split bodies seen from above, each in its own color](https://github.com/NaqshCoffee/bikar/blob/feat/multicolor-fills/docs/images/7apC5Q9QS-8-fill-coaster-bodies.png?raw=true)

**In the picture:** a top-down view of the four printed bodies of the prototype — not the 2D
drawing. Gold straps, ruby stars (the centre and a ring of eight: the two classes Omar's rule
groups together here), dark slab faces flush with the straps.

## 1. The ask, and Omar's coloring rule

Omar, 2026-09-26: "an alternative version of constructions … where we have multi colors shapes
(fill in some of the traces) instead of just a trace and that we can print in multiple colors",
and the same day: **"shapes that are translations same midpoint from center should be same
color"**.

**How this doc reads the rule.** Two filled shapes get the same color when they are the same
shape moved (in a rosette the move is a rotation about the centre, so "translation" is read as
"moved copy", rotation included) **and** their centroids sit the same distance from the
pattern's centre. Each such group is a **color class**. On a rosette a class is one ring of
matching shapes.

**A mirrored copy at the same distance counts as the same class.** Reasons: in the dihedral
rosettes surveyed here the mirror copy of a shape is usually also a rotated copy, so the two
readings agree there; and to the eye a mirrored petal is the same petal. The class test in §3
compares sorted edge lengths, which do not change under a mirror, so it does this by
construction. If Omar wants mirrors apart, the test adds the sign of the shape's winding; that
is one line and is listed in §9.

## 2. Where the shapes come from, and how one is picked (Q1)

The shapes are the bounded **faces** the pattern already finds (`voids detect`). The design
language already colors a face: `fill void where <selector> color <Name>`, with a `palette`
block, and D-078 already carries that color into its own printed body
([radial-band-color-design.md](radial-band-color-design.md)). So picking a shape needs no new
statement; the open question is only **which selector names a color class**.

| Option | What it is | Pros | Cons | Implications |
|---|---|---|---|---|
| **A. `ring` as it is** | Color by `ring == N` | Works today, no code | The ring centre is the first circle's centre, not the rosette's. On 6 of the 8 surveyed coasters, matching shapes fall in different rings, so `ring` breaks Omar's rule | Right on 7apC5Q9QS-8 only (0 split classes); every other file needs hand-picked ring lists, which is where mistakes creep in |
| **B. Move the ring centre** to the pattern's symmetry centre | Same `ring` word, better centre | No new word | Changes what `ring == N` means on screen for every existing pattern; may move goldens; ring is radius only, so two different shapes at one radius still share a ring | A cascade across every file that uses `ring`; still not Omar's rule where two shape kinds share a radius |
| **C. New selector `orbit`** (recommended) | `fill void where orbit == N color X`: classes by congruence + centroid radius about the symmetry centre | Is exactly Omar's rule; leaves `ring` alone; `bikar bands` can list orbits next to rings | Grammar change (a new attribute word in the parser's fixed list); a tolerance to choose | One grammar edit through the main session; the old ring coloring keeps working |
| **D. Classes from the construction's symmetry group** | Read the n-fold rotation from the construction steps | Exact, no tolerance | Constructions do not declare their symmetry; would need a new statement or guessing from the steps | Bigger grammar change; the imported GeoGebra steps carry no such fact |

**Recommendation: C.** It is the only option that matches the rule on every surveyed file
without touching what `ring` already means. The prototype uses A because on its one
construction A and C agree (16 rings, 16 classes, none split), which needs no grammar change.

## 3. How the engine finds the classes

1. **Centre.** The area-weighted centroid of all bounded faces. The bounding-box centre is wrong
   for odd-fold symmetry (it was tried first in the survey); the first circle's centre is wrong
   on GimTvN9hw4U and six other files (§2).
2. **Shape key.** Vertex count + edge lengths sorted, each compared within the tolerance. Sorted
   edge lengths do not change under rotation or mirroring. They can in principle match two
   different polygons with the same edge set in another order; the survey saw no such case, but
   it did not look for one, so the implementation should also compare sorted interior angles.
3. **Radius.** The distance from the centre to the face's centroid.
4. Two faces are in one class when the shape keys match and the radii differ by no more than the
   tolerance. Classes are numbered by radius from the centre outwards, like rings.

**Default:** radius tolerance 0.05 mm. The closest two real classes found are 0.22 mm apart
(7apC5Q9QS-8, r = 40.48 and 40.70 mm), so the tolerance must stay well below that; 0.05 mm is
still about five times the 0.01 mm gap the engine's `ring` binning uses today
([`fill-resolver.ts` `TOLERANCE = 1e-2`](https://github.com/NaqshCoffee/bikar/blob/main/packages/core/src/theme/fill-resolver.ts#L429)).
Both measured radii are from [research §2](research/multicolor-constructions.md#2-survey--do-the-engines-rings-match-omars-colour-classes).
This transfers to another construction only if its closest two real classes are more than
about four tolerances apart; the class lister should print the smallest gap so that is visible.

Scale matters. The construction files draw the art in millimetres from the `size` knob, and the
survey ran each file at its default size (90 mm for 7apC5Q9QS-8). The radii shrink with `size`:
at 80 mm the 0.22 mm gap becomes about 0.20 mm, still four times the tolerance. The class test
runs at the size being printed.

## 4. Geometry of the filled version (Q2)

The coaster is one height field on a 0.4 mm grid (`COASTER_GRID_PITCH_MM`, bet CAL-FEA-01), and
every printed body is cut from it. Two neighbouring bodies therefore share their faces exactly:
**no overlap and no gap, and no boolean union**. That answers the shared-edge-or-clearance
question: **shared edge**, because the bodies are printed together as one object with several
filaments, not assembled. A clearance would print as a groove and trap dirt on a coaster.

| Option | What it is | Pros | Cons | Implications |
|---|---|---|---|---|
| **Flush** (recommended) | `relief both`: filled faces rise to the strap height, straps stay their own color | A mug sits flat; works today after the two kernel fixes; one top surface | Every top layer holds several colors, so more color changes per layer | Unfilled faces must be filled with the base color name or they rise in the strap color (§4.1) |
| **Inlay** | Filled faces stay at slab height but take a color; straps raised | Only the straps rise; the colored faces are the slab top | The color is only on the top few slab layers, so each of those layers needs changes too; needs the color body to be a thin skin, which the kernel does not cut | A new cut in the kernel; no grammar change |
| **Relief** | Filled faces rise less than the straps | Reads as layered | Grooves between strap and fill; a mug rocks if the fills stand proud | Needs a second relief height per color: a grammar change |
| **Layer swap** | One body; the slicer changes filament at a height | Cheapest; one color change per swap | Cannot put two colors in one layer: straps and fills at the same height cannot differ | Useful only for a two-tone look (slab one color, all raised art another) |

**Recommendation: flush.** It is the only option that gives several colors in one top surface
with no new grammar, and it keeps the coaster flat.

### 4.1 What the two kernel fixes do

Found while building the prototype, both in bikar's coaster kernel, both with tests that fail
before and pass after (research §3):

1. **A strap stays the strap's.** A face's outline *is* a strap centreline, so the old lookup
   gave the inner half of each strap to the face beside it; with every face filled the straps
   body kept only its outer line. Now, under `relief both`, a cell within half a strap width of
   a strap is never a fill.
2. **Sliver tips go to the strap.** A star tip narrower than one grid cell (after the strap's
   half-width is off it) touched the strap only at a corner, and both bodies failed the
   watertight check. Now such a corner-only touch hands the color cells back to the strap. So a
   fill loses any tip thinner than one cell (0.4 mm) to the strap color; the strap widens there
   by at most that cell.

**Unfilled faces.** Under `relief both` every enclosed face rises, and a face with no fill goes
to the straps body. The prototype fills them with the base color name (Slab), so they rise
flush in the slab color and share its AMS slot (D-075: one name, one slot). The alternative, a
new relief target where only filled faces rise, is in §7.

### 4.2 What does not work yet

`--format parts` refuses deboss, `outline pattern` and the slab-reshaping clauses, so only the
plain and border styles can carry fills ([coaster-color-design.md](coaster-color-design.md)).
The minimal, minimal-frame, pegs, key, tab, interlock and twist styles are out until the split
learns them.

## 5. How the colors reach the printer (Q3)

| Option | Pros | Cons | Implications |
|---|---|---|---|
| **One 3MF with one part per color** (recommended) | Already built: `bambu slice coaster` writes per-part filament numbers (D-077); the sidecar carries each body's color | Color is checked only in the Bambu Studio window; headless slicing checks geometry | Omar sees the parts in the window before any print |
| **Separate STLs** | Nothing to build | Parts must be lined up by hand in the slicer; easy to shift one by a fraction | Every print needs a manual step |
| **One STL + layer swap** | One color change per swap | Only one color per layer (§4) | A two-tone style only |

**Color limits.** Each AMS holds 4 filaments and several units can be connected (W1, a search
summary; the X2D count W2 was not fetched). The design does **not** assume a number: the
slots are read from the machine with `bambu filament`, which reads the live tray list (confirmed
on the X2D 2026-09-17). **Default:** at most 4 colors per coaster, one AMS, the count W1
states for one unit ([Bambu Lab AMS page](https://us.store.bambulab.com/products/ams-multicolor-printing),
search summary only; [research §4](research/multicolor-constructions.md#4-web-sources-2026-09-26)).
This transfers to Omar's machine only if one AMS is what is loaded; `bambu filament` says.

**Purge and time.** Each color change purges the old filament to the chute and then onto a prime
tower (W5, W6, fetched), and dark-to-light changes purge more (W7, fetched). No fetched source
gives an X2D number. The design keeps changes low in two ways: every color sits only in the
**raised layers** (1.2 mm, about 6 layers at 0.2 mm), so the slab prints in one color with no
changes; and the base color is reused for the unfilled faces, so it needs no extra slot. The X2D
has two nozzles, which may cut purge for a two-color print; not confirmed (W2 not fetched).

## 6. Printability (Q4)

- **Smallest fill.** A fill narrower than one grid cell (0.4 mm) is handed to the strap (§4.1).
  The printed floor the gate enforces is 0.8 mm (CAL-FEA-01, three perimeters' worth). No fetched
  source gives a color-region minimum; the nozzle guides (W10) were seen only as summaries.
- **Bleed between colors.** A color boundary between two raised bodies is the case CAL-PIN-01
  names (the pinch floor for a two-filament interface), and that bet is open. Too little purge
  gives "faint tinting on light filaments or 'dirty' edges on small features" (W7, fetched), so
  a light fill next to a dark strap is the worst case to test first.
- **First layer.** The base body is the whole footprint, one color, so the first layer is one
  filament and no color touches the bed. This holds because every color body starts at the slab
  top (z = 4 mm on the prototype), which the height field guarantees.
- **Edges.** Color boundaries are staircased at the 0.4 mm grid. Whether that shows at arm's
  length is not known; it is the first thing to look at on a print.

## 7. What a `.bkr` says (Q5)

**Fits today** (the prototype, no grammar change):

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

**Grammar proposal** (for the main session, one edit at a time; nothing here is built):

1. **`orbit` selector attribute.** `fill void where orbit == 2 color Ruby`. Same comparison
   operators as `ring`. Needs a new word in the parser's attribute list and a resolver function
   that runs §3. `bikar bands` prints orbits beside rings, with the smallest radius gap.
2. **Default coloring by orbit** (optional). `fill orbits cycle Ruby, Gold, Slab`: give each
   class a color from the list in turn. Makes Omar's rule the default with one line.
3. **`relief fills`** (optional). A relief target where only filled faces rise and unfilled
   faces stay at the slab. Removes the need to fill the rest with the base color, but leaves
   pits between the straps that a mug does not sit on flat.

**Default:** straps 2 mm wide and fills raised 1.2 mm, the prototype's values; the strap width
is the one [`coaster-design.md`](coaster-design.md) ships and is floored by CAL-CST-01, and the
1.2 mm rise stays inside the relief aspect bet CAL-CST-04.

### 7.1 More classes than slots

7apC5Q9QS-8 has 16 classes and one AMS has 4 slots, so this is the normal case, not the edge.

| Policy | Pros | Cons | Implications |
|---|---|---|---|
| **Leave classes unfilled** (recommended default) | The rule still holds: each filled class is one color; the rest are base color | Fewer colored shapes | Designer picks which classes carry color; nothing is merged silently |
| **Share a color name across classes** | Allowed by the rule (it only says one class gets one color, not one color per class) | Two classes look alike | A designer choice, written in the file as the same palette name |
| **Merge by radius band** | Automatic | Can put two different shapes in one color against intent; hides which were merged | Needs a band width, another number to justify |

The engine never merges on its own. When more palette names are used than the machine has slots,
the slice step refuses and names the classes, the same way D-075 already maps names to slots.

## 8. Validators

**Validator:** color classes are colored consistently. For every class found by §3 (about the
area-weighted centre, radius tolerance 0.05 mm), every face in it has the same fill color or
none of them has one. Checked on the 2D faces and on the printed bodies: each face's centre point
is looked up in the body that owns that cell.

PASS: the prototype — the centre star (class 0) and the ring of eight stars (class 3) are all
Ruby, and every other class is all Slab; the Ruby body is 9 separate stars.

FAIL: two congruent stars whose centroids sit 40.48 mm and 40.49 mm from the centre (0.01 mm
apart, inside the 0.05 mm tolerance, so one class) with one Ruby and one Slab. This is the hard
case: a ring-based coloring can produce it whenever the ring clustering and the class test
disagree about a close pair, and nothing else catches it.

FAIL: GimTvN9hw4U colored by `ring == N`. Its rings are counted from the first circle's centre,
not the rosette's, so 7 of its 8 classes span several rings, and coloring one ring colors part
of a class.

**Validator:** the printed bodies show what the drawing shows. A top-down picture of the actual
bodies (each STL in its sidecar color) is compared with the 2D drawing's color per face.

PASS: the prototype after both fixes — gold straps run through the pattern's interior in both.

FAIL: the prototype before fix 1 — the drawing showed gold straps inside the pattern; the bodies
had none, because the fills had taken them. The plate picture is drawn from the 2D drawing
(`tools/bambu/src/color-preview.ts`), so it passed this case; only the body picture caught it.

## 9. Proposal — the smallest prototype and a first sample plate

**Built (bikar [PR #261](https://github.com/NaqshCoffee/bikar/pull/261)):** one coaster, 7apC5Q9QS-8 plain, flush fills, three colors (Slab,
Gold, Ruby). The two kernel fixes and their tests. All four bodies pass `--format parts --check`;
the whole coaster passes `--format stl --check`. Checked at the file's default 90 mm and again at
`size=80`: all four bodies pass at both, with the same body shapes (same euler numbers). Not
sliced, not printed.

**First sample plate (a proposal; not added under `docs/plates/`):** two coasters of 7apC5Q9QS-8
at 80 mm, both plain, both three colors.

1. The prototype as built (dark slab, gold straps, ruby classes 0 and 3).
2. The same with a light fill next to the dark strap, to show bleed at its worst (W7).

What to look at: color bleed on the light fill, the staircase at the color edges, whether any
star tip lost to the strap shows, purge and time as the slicer reports them. Printing and
filament choice are Omar's.

**Smallest next step:** the `orbit` attribute (§7 item 1), so the fill works on GimTvN9hw4U and
the other six surveyed files where rings split the classes. Then the slice through
`bambu slice coaster` and a look in the Bambu Studio window.

**Open choices for Omar:** mirrored copies in one class (this doc: yes, §1); flush vs
`relief fills` (§4, §7); which classes carry color on the sample plate.

## 10. Read against itself (K7)

- §2 recommends C, but the prototype uses A. Consistent: on the prototype's construction A and C
  give the same 16 classes (research §2), and C needs a grammar change the prototype may not make.
- §3's 0.05 mm tolerance and §8's hard FAIL (0.01 mm apart) agree: 0.01 is inside 0.05. The real
  0.22 mm gap on 7apC5Q9QS-8 is outside it, so the PASS case keeps rings 9 and 10 apart.
- §4 says no color touches the bed; §6 says the same, for the same reason (color bodies start at
  the slab top).
- §5's 4-color default and §7.1's 16 classes agree: 16 classes do not need 16 slots, because
  unfilled classes take the base color.
- The survey covers the 8 plain construction coasters in bikar's Constructions folder only
  (research §2); nothing here is claimed about other patterns.
