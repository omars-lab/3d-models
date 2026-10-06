# Constructions ledger

One row per GeoGebra construction on its way from a youtube reconstruction to a
naqsh (`.bkr`) file bikar renders to a printable coaster this repo vendors. The
umbrella design is the
[GeoGebra construction import design](geogebra-construction-import-design.md)
and the three oracles O1/O2/O3 are specified in
[construction equivalence](construction-equivalence.md). This file is the
record; `.claude/gates/constructions_ledger.py` keeps it honest and
`make validate-constructions` runs it over the whole tree.

Youtube pin: `e55a57797befcba7040447b38c7fc9a1475e7bdf` (2026-10-01)

The pin is a commit in the youtube repo (branch `main`, no remote). Every
"youtube" verdict below — **attempted** (a `reconstructions/<id>/` directory
with a `construction.ggb-commands` exists at the pin) or **done** (that id is
listed in the pin's docs/tasks/done.md) — is read at that commit and nowhere
else, so the column does not shift when someone checks out a different youtube
branch. The gate re-reads youtube at this pin; when youtube is not checked out
it says so and skips the cross-check rather than passing or failing it. It also
reads youtube's `main` branch (a ref, not the working tree) and fails when a
reconstruction there has no row here, or when a row's id is not at the pin — so
a new reconstruction cannot sit unledgered behind an old pin, as `bknVRSMcLj0`
did ([the write-up](../issues/constructions-ledger-missed-new-reconstruction.md)).

Scope of the set (K2): **34 <!--count:constructions-total--> constructions**,
one per reconstruction that has a `construction.ggb-commands` at the pin —
`_techniques/` holds shared snippets, not a construction, and is not a row.
**14 <!--count:constructions-migrated--> migrated** so far: a row counts as
migrated once its naqsh cell names a real `.bkr` on bikar's default branch.
`GimTvN9hw4U` landed with bikar PRs #200/#201 (importer + golden, then the
`piece Coaster` trailer), `7apC5Q9QS-8` with bikar PR #202, `tA8eSdVx_EQ`
with bikar PR #223 (its heptagon frame pinned via `--coaster-outline`,
[D-079](../working-model/decisions-log.md)), `lEfWSogWscs` with bikar PR #225 (its
octagon frame the least-area default fit, no pin), `rDuxHF3xMOc` with
bikar PR #227 (the importer now lowers a `Reflect`/`Rotate` of a brace-group
**list literal** into a conjugated orbit rather than refusing it; the video
draws three of its square's four cells, so its coaster alone adds the fourth
through `--coaster-reflect`, bikar PR #250, while the `.bkr` stays three), and
`nmEjCTzMbDg` with bikar PR-5 #243 (the first **open line-art** construction —
conic loci and circle inversion drawn as `connect arc … major` straps, resolved
by the B′ `--emit-coords` cached_coords self-bootstrap, [D-080](../working-model/decisions-log.md)),
`sDO9fpu76v8` with bikar PR #228 (the first **tessellation** rather than a
rosette — a hexagonal cell reflected into its neighbour and the layer rotated
six-fold, on the set's first hexagonal frame), and `n3IidKfXE1I` with bikar
PR #229 (three rotational orbits about three different centres, the "12-6-4",
with the walkthrough's slider angle pinned at 23.5°), and `bknVRSMcLj0` with
bikar PR #268 (the first construction that **orbits an orbit** — one tile
cell reflected across two sides of its square and the pair orbited four-fold
into a wall, lowered to `rotate` blocks nested three deep; the whole wall read
as a solid slab at coaster size, so its coaster inscribes one repeat cell, see
`CS-12`).
The three [D-087](../working-model/decisions-log.md) patterns landed 2026-09-30, each
with a **minimal** coaster (`outline pattern`, no slab) rather than a plain one, for the
90 mm comparison on the [renders page](../working-model/feedback-requests/2026-09-30-top-three-renders.md):
`gBV_JTt3Kxk` with bikar PR #287 (ten scaffold arcs through the D-080
self-bootstrap; the video's paint-over masks are left off the coaster),
`jlTmt_279M4` with bikar PR #286 (straight lines only — seven-point stars around
octagon cells, one tile reflected into a 2×2 block; it taught the importer to carry a
drawn segment list through an isometry and gave the cookbook its `Ray` recipe), and
`NtnlGMTElBk` with bikar PR #285 (six scaffold arcs, plain straps, no weave).
`0ke_GpoBa-s` landed 2026-10-06 with bikar PR #315, also as a minimal coaster: the first
construction drawn on paper with a compass and filmed, and the first whose youtube source had
to be rewritten for the importer (its petal ring, a half turn of a pair of segments, is written
as the whole ten-fold turn of one; youtube branch `coaster-0ke`).
`88q-u2eWZqg` landed 2026-10-06 with bikar PR #317, a minimal coaster too: Eman Zainab's
sixteen-petal rosette, one unbroken line of sixteen Vs and sixteen roofs, imported from youtube
main as it is, nothing refused.
All fourteen now vendor a standard (90 mm) coaster mesh under `src/Coasters/` and
carry a prototype-catalog entry (`CS-1`, `CS-2`, `CS-6`, `CS-7`, `CS-8`, `CS-9`,
`CS-10`, `CS-11`, `CS-12`, `CS-13`, `CS-14`, `CS-15`, `CS-16`, `CS-17`) — P3.3 of the umbrella plan,
which built on the `coaster` declaration (P1.6/P2.7).

The ten rows added 2026-09-29, with the pin moved to youtube `8ccacb1`, are the video loop's
newer rungs, none of them a naqsh file yet. Each is "done" in the column's sense (its id is in
the pin's done.md), though one of those rungs, `88q-u2eWZqg` (6/9), scored short of every
step and says "attempted" in its own heading. `yZN_wn0uvTY` (9/13), added 2026-09-30, is the
same case, and so is `LoCRh3SOhls` (0/2 best-effort, mean 0.691), added 2026-10-01 with the pin
moved to youtube `e55a577`. `Y6kS1MvnKoc` was the third until 2026-09-30, when its last failing step turned out
to be that slide's own `@view` 0.5% too large; it now passes 18/18 (mean 0.872).

Oracle cells read `PASS a/b` or `FAIL a/b` — O1: labels compared / failed; O2:
centreline recall / precision; O3: reference coverage — or `—` when that oracle
has not been run on the row's `.bkr`. A verdict is only ever the one the equivalence
doc's validator printed, never a re-typed summary: `GimTvN9hw4U`'s three are in
[construction equivalence §2–§4](construction-equivalence.md) and its
research file; `7apC5Q9QS-8`'s O1 and O2 were run 2026-09-17 on the youtube
`feat/ggb-coords` verdict scripts against a hero rebuilt with the loop's own
export (the earlier `export.png` was a stale 5123×5123 square that O2 scored
recall 0.01; the youtube issue note naqsh-score-stale-hero on that branch has the evidence); every
other cell was run 2026-09-27 — see [Oracle notes](#oracle-notes) under the table.
The exception is `bknVRSMcLj0`, added later that day: its three were run at its
migration, on youtube `main`
against the migrated `.bkr` and printed, verbatim:
O1 `PASS: 79 compared, 0 failed, 140 skipped/extra`; O2
`O2 PASS: edge-SSIM 0.8288 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 16 (advisory)`; O3
(`make reference` from its `export.ggb`, then `qiyas mesh compare`)
`O3 PASS: coverage 1.000 (min 0.99), local 0.400 mm at (35.541, -24.459) (max 1)`.

## Columns

- **naqsh** — the bikar source of record, `patterns/Constructions/<id>.bkr`
  written as `bikar/patterns/Constructions/<id>.bkr`; `—` until it is merged.
  The gate FAILS a row that names a `.bkr` bikar cannot resolve.
- **O1 / O2 / O3** — the three equivalence oracles: per-label geometry, drawing
  recall/precision, and solid coverage. `—` until the naqsh file exists to run
  them against.
- **coaster** — the vendored mesh, `src/Coasters/<id>-coaster-standard.stl`
  (the 90 mm standard `make coasters` writes; the 40 mm mini is validated on
  every build but not carried in git); `—` until that mesh is vendored. The
  gate FAILS a row that names an `.stl` not on disk here.
- **catalog** — the prototype-catalog id, once the coaster is catalogued.
- **printed** — the print record under `docs/prints/`, once a plate ships.
- **no piece by design** — the sentinel for a mechanism-only video with no final
  art (`M60LJNNslHU`): a complete row that asserts no `.bkr` and no coaster and
  so is neither "migrated" nor "not yet migrated".

## Ledger

| id | title | youtube | naqsh | O1 | O2 | O3 | coaster | catalog | printed |
|---|---|---|---|---|---|---|---|---|---|
| `0ke_GpoBa-s` | Ptolemy's pentagon doubled to ten | done | `bikar/patterns/Constructions/0ke_GpoBa-s.bkr` | PASS 40/0 | PASS 1.0/1.0 | — | `src/Coasters/0ke_GpoBa-s-minimal-coaster-standard.stl` | CS-16 | — |
| `1TclLO9JKAA` | Parallel 9-fold Star Rosette, "Avoiding Open Paths" (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `1h7iWJaoN80` | Folio 192 heptagonal panel, Anonymous Persian Compendium (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `7apC5Q9QS-8` | Geogebra for Beginners — 8-Fold Rosette Walkthrough (Sarah Brewer) | done | `bikar/patterns/Constructions/7apC5Q9QS-8.bkr` | PASS 144/0 | PASS 1.000/1.000 | PASS 1.000 | `src/Coasters/7apC5Q9QS-8-coaster-standard.stl` | CS-2 | — |
| `88q-u2eWZqg` | A 16-petal rosette in one unbroken line | done | `bikar/patterns/Constructions/88q-u2eWZqg.bkr` | PASS 33/0 | PASS 1.0/1.0 | — | `src/Coasters/88q-u2eWZqg-minimal-coaster-standard.stl` | CS-17 | — |
| `A9fefFurD_s` | Broug's ten-point star from one circle | done | — | — | — | — | — | — | — |
| `GimTvN9hw4U` | Simple 20-step Six-Fold Star Rosette (Sarah Brewer) | done | `bikar/patterns/Constructions/GimTvN9hw4U.bkr` | PASS 23/0 | PASS 1.000/1.000 | PASS 1.000 | `src/Coasters/GimTvN9hw4U-coaster-standard.stl` | CS-1 | — |
| `M60LJNNslHU` | Dual Slider m,n-fold Division of the Circle (Sarah Brewer) | done | no piece by design | — | — | — | no piece by design | — | — |
| `NtnlGMTElBk` | The Mustansiriya ten-fold interlaced star | done | `bikar/patterns/Constructions/NtnlGMTElBk.bkr` | FAIL 124/20 | PASS 0.9999/1.0 | — | `src/Coasters/NtnlGMTElBk-minimal-coaster-standard.stl` | CS-15 | — |
| `Y6kS1MvnKoc` | A Mamluk Qur'an page from seven ten-point stars | done | — | — | — | — | — | — | — |
| `ZXKYNvqtFKs` | Rings of Tangent Circles (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `_U6G8QSfWnk` | Sutton's fivefold rectangle and its traced quarter | done | — | — | — | — | — | — | — |
| `bknVRSMcLj0` | Imamzadeh Isma'il Shrine, Isfahan — 12-fold from a Square (Sarah Brewer) | done | `bikar/patterns/Constructions/bknVRSMcLj0.bkr` | PASS 79/0 | PASS 1.000/1.000 | PASS 1.000 | `src/Coasters/bknVRSMcLj0-coaster-standard.stl` | CS-12 | — |
| `cKYbKQvmsbs` | Sultan Barsbay 16 & 8 (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `fhGHzop7ULw` | The sixfold √3 rectangle from Baghdad | done | — | — | — | — | — | — | — |
| `gBV_JTt3Kxk` | The Itimad-ud-Daula ten-fold rosette in a rhombus tile | done | `bikar/patterns/Constructions/gBV_JTt3Kxk.bkr` | FAIL 134/20 | FAIL 0.997/0.4291 | — | `src/Coasters/gBV_JTt3Kxk-minimal-coaster-standard.stl` | CS-13 | — |
| `jlTmt_279M4` | Sevenfold stars in a tilted square | done | `bikar/patterns/Constructions/jlTmt_279M4.bkr` | PASS 86/0 | PASS 1.0/1.0 | — | `src/Coasters/jlTmt_279M4-minimal-coaster-standard.stl` | CS-14 | — |
| `kpFgs2e8YGw` | Star rosettes on a 3-uniform tiling (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `lEfWSogWscs` | Pattern from the Tomb of Itimad ad-Daula (Sarah Brewer) | done | `bikar/patterns/Constructions/lEfWSogWscs.bkr` | PASS 49/0 | PASS 1.0/1.0 | PASS 1.000 | `src/Coasters/lEfWSogWscs-coaster-standard.stl` | CS-7 | — |
| `n3IidKfXE1I` | Variable-angled 12-6-4 Star Rosette (Sarah Brewer) | done | `bikar/patterns/Constructions/n3IidKfXE1I.bkr` | PASS 64/0 | PASS 1.0/1.0 | PASS 1.000 | `src/Coasters/n3IidKfXE1I-coaster-standard.stl` | CS-10 | — |
| `n_ICgwOr6qs` | A ten-petal blossom from one compass setting | done | — | — | — | — | — | — | — |
| `nmEjCTzMbDg` | n-fold Flower in GeoGebra Classic 5 (Sarah Brewer) | done | `bikar/patterns/Constructions/nmEjCTzMbDg.bkr` | FAIL 25/15 | FAIL 0.9176/0.2589 | none by design: no solid to compare (see notes) | `src/Coasters/nmEjCTzMbDg-coaster-standard.stl` | CS-9 | — |
| `rDuxHF3xMOc` | 8-fold Star Rosette with Sequences (Sarah Brewer) | done | `bikar/patterns/Constructions/rDuxHF3xMOc.bkr` | PASS 41/0 | FAIL 0.8381/1.0 | PASS 1.000 | `src/Coasters/rDuxHF3xMOc-coaster-standard.stl` | CS-8 | — |
| `sDO9fpu76v8` | Pattern from the Royal Alcazar (Sarah Brewer) | done | `bikar/patterns/Constructions/sDO9fpu76v8.bkr` | PASS 84/0 | PASS 0.996/0.9972 | PASS 1.000 | `src/Coasters/sDO9fpu76v8-coaster-standard.stl` | CS-11 | — |
| `tA8eSdVx_EQ` | 5-minute 7-fold Star Rosette (Sarah Brewer) | done | `bikar/patterns/Constructions/tA8eSdVx_EQ.bkr` | PASS 28/0 | PASS 1.0/1.0 | PASS 1.000 | `src/Coasters/tA8eSdVx_EQ-coaster-standard.stl` | CS-6 | — |
| `tcZQLpnxGpw` | 12-fold pattern in a 6-4-3-4 tiling (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `itZftnqJ3tI` | Star rosettes on a 4-uniform tiling, in a square (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `Ln-s5FzLGms` | 8-fold rosettes turned 45°, with squares (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `awOusq0uVzc` | Ibn Tulun variable-angle pattern (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `xtox61vADMA` | Discrete variable star rosette, sliders n and k (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `ZFQt67eZ9Sg` | Alhambra Hall of the Two Sisters doors, 8-fold in a square (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `XfY1r7QKYwA` | 7-fold star rosette, the 27-minute build (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `yZN_wn0uvTY` | The Itimad-ud-Daula ten-fold rosette built by hand in GeoGebra, then tiled (Geogebra_Road to School) | done | — | — | — | — | — | — | — |
| `LoCRh3SOhls` | A tenfold rosette in a pentagon, ink on filmed paper (Samira Mian) | done | — | — | — | — | — | — | — |

## Oracle notes

The cells filled on 2026-09-27 come from the lines each tool printed that day,
kept in [the 2026-09-27 oracle runs](../research/ledger-oracle-runs-2026-09-27.md)
with the commands and the tree each ran on. One cell holds a reason instead of a
verdict: `nmEjCTzMbDg`'s O3, because an open line-art construction has no polygons to
build a reference from and its `.bkr` has no piece to extrude.

The FAILs were worked through the same day, in
[the 2026-09-27 oracle FAILs note](../research/ledger-oracle-fails-2026-09-27.md):

- **`n3IidKfXE1I`**: re-run, now PASS on all three. Its `.bkr` had been imported
  from a draft of the construction that stopped before the final assembly. The
  re-imported coaster leaves off the finished tile `l1` and draws the 12-fold
  rosette only, because the whole field was near-solid at 90 mm. The O2 cell no
  longer needs the scorer fix, but the youtube scorer bug is still open.
- **`nmEjCTzMbDg`**: the FAILs stay. Two causes:
  - one was a bikar bug, now fixed: the rim circles drew only half their outline;
  - the other is in the youtube source: `R = Intersect(t, m, 2)` picks the other
    root in bikar. The fix is proposed there.

  **Do not print this coaster.** Until the youtube fix lands, it is built on the
  wrong `R` and renders near-solid.
- **`rDuxHF3xMOc`** O2: **by design**. The GeoGebra export keeps the tile's four
  full-width bounding lines visible, because the video shows them. The coaster
  draws the tile only. The FAIL stays. With those four lines hidden, recall is 1.0.

The three D-087 rows (`gBV_JTt3Kxk`, `jlTmt_279M4`, `NtnlGMTElBk`) were scored
at their imports on 2026-09-30, on the youtube branches named in each bikar PR
(#287, #286, #285), and the cells copy the lines those runs printed:

- **`gBV_JTt3Kxk`** O1 `FAIL: 134 compared, 20 failed, 47 skipped/extra`; O2
  `O2 FAIL: edge-SSIM 0.9215 (min 0.7), recall 0.997 precision 0.4291 (min 0.98), phash 40 (advisory)`. The O1 twenty are the ten scaffold arcs ("no comparison
  for GeoGebra type 'arc'") and their ten `*_host` circles, the same O1 arc gap
  `nmEjCTzMbDg` hit; every point, line, circle, polygon and mask passes. The O2
  precision is the video's white paint-over masks: the frame shows the clipped
  rosette, the naqsh render draws the mask edges and the rosette under them. A
  re-render scores the same, so it is not a stale hero.
- **`jlTmt_279M4`** O1 `PASS: 86 compared, 0 failed, 75 skipped/extra` — on
  youtube branch `o1-polyline-ray` (9a92134), which teaches the comparator
  polyline and ray rows and is not on youtube main yet; O2
  `O2 PASS: edge-SSIM 0.9458 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 16 (advisory)`.
- **`NtnlGMTElBk`** O1 `FAIL: 124 compared, 20 failed, 12 skipped/extra` — the
  same arc gap, ten arcs and their ten host circles; O2
  `O2 PASS: edge-SSIM 0.9066 (min 0.7), recall 0.9999 precision 1.0 (min 0.98)`.
- **O3 is `—` on all three**: none of the three reconstructions has a `.ggb`
  export to build a reference from, so the oracle was not run, not skipped by
  design.

`0ke_GpoBa-s` was scored at its import on 2026-10-06, on youtube branch `coaster-0ke`
(c8d2b48), which holds the source rewrite and the hero export and is not on youtube main yet:
O1 `PASS: 40 compared, 0 failed, 21 skipped/extra`; O2
`O2 PASS: edge-SSIM 0.9146 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 20 (advisory)`.
Before the branch's `@export` line the youtube hero drew the axes, the circle and the four
diameters too, which naqsh keeps as scaffold, and recall was 0.71 against the same import. O3 is
`—`: there is no `.ggb` export to build a reference from.

`88q-u2eWZqg` was scored at its import on 2026-10-06, on youtube main (beb19b3), with no source
rewrite: O1 `PASS: 33 compared, 0 failed, 11 skipped/extra`; O2
`O2 PASS: edge-SSIM 0.9633 (min 0.7), recall 1.0 precision 1.0 (min 0.98)`. The hero export is
newer than the source's last commit, so it is not stale. O3 is `—`: there is no `.ggb` export.
