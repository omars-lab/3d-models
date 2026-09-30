# Scoring — how the next coaster is chosen

The [prioritize-design](SKILL.md) skill reads this every run. It is kept apart so the checks,
the weights and the facts can sharpen as Omar answers, without the skill changing. The full
argument is the prioritize-design design (3d-models PR #427, under docs/design/process once it
merges); this file is its short form plus the facts and the round log.

Three scores, never blended into one judgment: **would people like it** (judged), **is it
unusual** (judged), **how different is it from what we made** (measured by
`tools/design_difference.py`). Two checks come before any score. Readiness breaks ties. The
total is arithmetic, and the tool prints it.

## 0. Two checks before scoring

**Reads as a coaster.** The three things Omar has turned down, from the
[review-print rubric](../review-print/rubric.md) (read it, do not copy it; a new print verdict
updates both skills): a near-solid disc, a half-empty or cut-off piece, bare wedges between the
art and the frame. Once a candidate has a mesh, `tools/print_review.py` gives that rubric's
hints: `open` at 0.15 or below, `biggest` at 0.05 or above, `sym` below 0.9. Before a mesh
exists the check is made from the picture and is written **not measured**, never "passed":
pictures misled the candidate screen about openness twice (bknV, n3Ii). A candidate that fails
is **held**, not ranked, and the fix it needs is written down.

**Sell flag.** One of *clear* (public domain), *credit* (rebuilt from a video, so credit the
creator) or *check first* (it follows a copyrighted book), from the
[candidate screen's licence position](../../../docs/research/candidate-screen-2026-09-27.md#licence-position).
Printed beside the name; never changes a rank; not legal advice.

## 1. Would people like it (judged, 0 to 8)

Score unusual (section 2) **before** this one: a judge who likes a piece tends to call it novel.
Four parts, each 0, 1 or 2 from the picture, with the reason written beside the number:

| part | 2 | 1 | 0 |
|---|---|---|---|
| **whole and centred** | symmetric about its own middle, complete | complete, but the outline lowers its symmetry | a fragment: cut stars, half a motif |
| **fills its outline** | even to the edge | gaps at the rim or the corners | half-empty, or big wedges |
| **reads at 90 mm** | holes of similar size, spread evenly | a few holes far bigger than the rest, or crossings tight enough to close | near-solid, or a mesh of thin lines |
| **one clear motif** | one star or rosette the eye goes to | two layered motifs, or several competing | nothing stands out |

Dropped on purpose: "busyness in the middle" (people split into groups that want opposite
things) and a separate symmetry part ("whole and centred" already covers it; once a mesh
exists, `sym` measures it as a check, not a score).

## 2. Is it unusual (judged, 0 to 2)

Against what coaster models on Printables usually look like (970 pulled in the research, where
flower and mandala forms are common and Islamic star coasters are rare):

| score | when |
|---|---|
| 2 | nothing in that sample is named for this form: a star in a tile shape, or an interlaced star |
| 1 | a star medallion: rare as an Islamic pattern, but "star coaster" is a common search |
| 0 | a common form: flower, mandala, petals, hexagon, Voronoi |

A candidate that scores 0 on "whole and centred", or that cannot be judged, is held and is
never the "most unusual" winner: an unusual thing is liked only while it still reads as its kind.

## 3. Different from ours (measured, 0 to 1)

`python3 tools/design_difference.py table` reads the four facts below and the made set from
the [constructions ledger](../../../docs/constructions/ledger.md) (every row with a vendored
coaster). Two designs are as similar as the share of the four facts they share; a candidate's
difference is 1 minus its average similarity to every made coaster. The tool also shows the
**nearest** made coaster, and the "same source as" note for what the facts cannot see.

**Recompute after every pick.** A new made coaster changes every other candidate's difference:
until 2026-09-30 no made coaster was 5- or 10-fold; the D-087 renders added three 10-fold
pieces to the made set, and the 10-fold candidates lost most of their lead.

The tool fails, naming the ids, when a made coaster or a candidate it is asked to rank has no
row here (D-086), and when a fact value is not one of the words listed under each column.

### The four facts

- **fold family**: `4/8`, `3/6/12`, `5/10`, `7`, `9/18` (which base angles the star comes
  from; 16 petals belong to `4/8`, 18 to `9/18`);
- **layout**: `centre` (one centre star), `tile` (a repeat tile), `field cut` (cut from a field);
- **outline**: `round`, `hexagon`, `square`, `octagon`, `heptagon`, `rhombus`, `rectangle`;
- **lines**: `straight`, `arcs`, `woven` (a true over-under band).

The facts of a made coaster are the coaster **as built**. A candidate that could be built another
way gets a second row with the variant word after the id (`` `NtnlGMTElBk` woven ``); the tool
ranks it as its own candidate. Facts are one reader's reading of the pictures and the
catalog-expansion backlog's coaster notes (2026-09-29, researcher B; the three D-087 pieces and
the four newer candidates added 2026-09-30; the twelve #430 reconstructions added the same day
from their backlog entries and final renders, not measured). Change one when a render shows
otherwise.

| id | catalog | fold family | layout | outline | lines | sell | same source as |
|---|---|---|---|---|---|---|---|
| `GimTvN9hw4U` | CS-1 | 3/6/12 | centre | hexagon | straight | credit | |
| `7apC5Q9QS-8` | CS-2 | 4/8 | centre | square | straight | credit | |
| `tA8eSdVx_EQ` | CS-6 | 7 | centre | heptagon | straight | credit | |
| `lEfWSogWscs` | CS-7 | 4/8 | centre | octagon | straight | credit | the tomb of Itimad-ud-Daula, Agra (also gBV_JTt3Kxk) |
| `rDuxHF3xMOc` | CS-8 | 4/8 | tile | square | straight | credit | |
| `nmEjCTzMbDg` | CS-9 | 9/18 | centre | round | arcs | credit | |
| `n3IidKfXE1I` | CS-10 | 3/6/12 | centre | round | straight | credit | |
| `sDO9fpu76v8` | CS-11 | 3/6/12 | tile | hexagon | straight | credit | |
| `bknVRSMcLj0` | CS-12 | 3/6/12 | tile | round | straight | credit | |
| `gBV_JTt3Kxk` | CS-13 | 5/10 | centre | round | straight | credit | the tomb of Itimad-ud-Daula, Agra (also CS-7); built as the rosette alone |
| `jlTmt_279M4` | CS-14 | 7 | tile | square | straight | clear | Bourgoin 1879, plate 170 (public domain) |
| `NtnlGMTElBk` | CS-15 | 5/10 | centre | round | straight | credit | built with plain straps, no weave |
| `gBV_JTt3Kxk` rhombus | | 5/10 | tile | rhombus | straight | credit | the 72° repeat cell; no coaster style makes a rhombus yet |
| `NtnlGMTElBk` woven | | 5/10 | centre | round | woven | credit | the same star cut as an over-under band; no style weaves yet |
| `A9fefFurD_s` | | 5/10 | centre | round | straight | check first | Broug's book |
| `n_ICgwOr6qs` | | 5/10 | centre | round | arcs | credit | |
| `fhGHzop7ULw` | | 3/6/12 | tile | rectangle | straight | credit | |
| `_U6G8QSfWnk` | | 5/10 | tile | rectangle | straight | credit | held: a quarter-tile fragment until mirrored |
| `Y6kS1MvnKoc` | | 5/10 | field cut | round | straight | credit | "(c) Eric Broug 2014" on the slides; held: the pattern alone is not rendered |
| `0ke_GpoBa-s` | | 5/10 | centre | round | straight | credit | the methods of Aljanabi and Sarvdalir |
| `88q-u2eWZqg` | | 4/8 | centre | round | arcs | credit | 16 petals in one unbroken line |
| `1h7iWJaoN80` | | 7 | tile | rectangle | straight | credit | Folio 192, Anonymous Persian Compendium |
| `kpFgs2e8YGw` | | 3/6/12 | field cut | round | straight | credit | a round patch of a 3-uniform tiling, centred on a hexagon |
| `cKYbKQvmsbs` | | 4/8 | tile | square | straight | credit | Sultan Barsbay, Cairo; a 16-fold centre with quarter 8-folds in the corners |
| `1TclLO9JKAA` | | 9/18 | centre | round | straight | credit | drawn in a nonagon; the list has no nonagon, so round |
| `ZXKYNvqtFKs` | | 3/6/12 | centre | round | arcs | credit | circles only; the polygon is a slider (11, 8 and 12 shown), read at the render's 12 |
| `tcZQLpnxGpw` | | 3/6/12 | centre | round | straight | credit | drawn in a 12-gon; 8-point stars in its squares |
| `itZftnqJ3tI` | | 3/6/12 | tile | square | straight | credit | 12-point rosettes with 4-fold rosettes and octagons |
| `Ln-s5FzLGms` | | 4/8 | tile | square | straight | credit | 8-fold rosettes on a lattice turned 45° |
| `awOusq0uVzc` | | 4/8 | tile | square | straight | credit | the minbar of the Ibn Tulun mosque, Cairo; one angle bends it (22.5° to 30°) |
| `xtox61vADMA` | | 9/18 | centre | round | straight | credit | the point count is a slider (5 to 30), read at the video's end, 18 |
| `ZFQt67eZ9Sg` | | 4/8 | tile | square | straight | credit | the door of the Hall of the Two Sisters, Alhambra |
| `XfY1r7QKYwA` | | 7 | centre | heptagon | straight | credit | the same kind of rosette as CS-6; the render has no outline, so heptagon follows CS-6 |
| `yZN_wn0uvTY` | | 5/10 | tile | rhombus | straight | credit | the tomb of Itimad-ud-Daula, Agra (also CS-7, CS-13); held: print from gBV_JTt3Kxk, this one is off by up to 2°; rhombus read from its two tiling vectors, not measured |

## 4. Ready to build (a tie-break, not a score)

Three yes/no facts shown beside each candidate, never added to the total:

- **an outline we can make**: bikar's coaster outlines are round, square, regular polygon,
  lobed and `pattern` (the straps are the footprint); there is no rhombus or rectangle slab;
- **lines we can make**: straight is fine; arcs once came out near-solid (CS-9); no style
  weaves;
- **a close rebuild**: the youtube rebuild's mean edge score is 0.90 or more (a starting guess).

Readiness counts "fits its own outline" only once (it is already in appeal), and it never lets
ease outrank the three questions.

## 5. The total

**total = appeal + 5 × difference + unusual ÷ 2** (D-085). Ties break on readiness, then on
the rebuild score. `python3 tools/design_difference.py rank --scores <file>` prints it from a
small table of the judged numbers (`id | appeal | unusual | ready | rebuild`), beside the three
raw scores, so a total that hides a weak part stays visible. The 5 and the ½ are a guess; the
weights live at the top of the tool, and a round that moves them says why below, in Omar's words.

## Round log

One line per round: the date, what was ranked, what the page suggested, what Omar picked, and
whether a check or a weight moved and why. Newest first.

- **2026-09-30, round 2** — the three D-087 patterns rendered as minimal coasters at 90 mm
  (CS-13 gBV, CS-14 jlTmt, CS-15 Ntnl) on the
  [renders page](../../../docs/working-model/feedback-requests/2026-09-30-top-three-renders.md).
  Omar's pick: open (D-088). Weights unchanged. With the three now in the made set, the other
  10-fold candidates' difference drops (section 3); rerun the tool before the next page.
- **2026-09-29, round 1** — the eight D-084 rebuilds, scored in the design's own first run
  against the nine made coasters (nine, because the three D-087 pieces were not built yet).
  Suggested: jlTmt_279M4, tied with gBV_JTt3Kxk at 11.05, Ntnl 9.65 flat. Omar's answers:
  weighted total over added ranks (D-085), the facts in this file (D-086), render the top three
  before choosing (D-087), pick after the renders (D-088). Weights: the starting guess.
