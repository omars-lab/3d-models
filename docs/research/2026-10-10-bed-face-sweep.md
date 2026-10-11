---
date: 2026-10-10
produced-by: Claude Opus 5.5, building the bed-face simulator Omar asked for on 2026-10-10 ("can we also build a simulator ehere we can play with nozzle size and shape size to dind ideal settings"). Every number below came from slicing with the installed Bambu Studio CLI (through `bambu slice compose`) and scoring the sliced G-code with `tools/bed_face_sweep.py`, which uses the drawing in `tools/print_review.py`. No piece was printed for this file, and no web source was read.
feeds:
  - docs/design/printing/bed-face-slicing-design.md
---

# Bed-face sweep: four nozzles, seven pieces, two presets

Kept verbatim as the record the design doc's §9 comes from. The slices, pictures and results live
in the gitignored `build/bed-face-sweep/`; the commands below make them again.

## What was sliced

Seven pieces, each a scratch recipe with `no_id: "scratch slice, not printed"`, on `bed: x2d`,
sliced `--plate-type hot_plate`:

| Name | Construction | Piece | Params |
|---|---|---|---|
| star-2 | `7apC5Q9QS-8-minimal-coaster` | the coaster | size 90, strap 2, height 4, round 1 |
| star-3 | `7apC5Q9QS-8-minimal-coaster` | the coaster | size 90, strap 3, height 4, round 1 |
| star-4 | `7apC5Q9QS-8-minimal-coaster` | the coaster | size 90, strap 4, height 4, round 1 |
| radial-3 | `GimTvN9hw4U-radial-coaster` | the coaster | size 90, strap 3, height 4, round 1 |
| kite-90 | `gBV_JTt3Kxk-minimal-pieces` | Kite (a row of ten small kites) | size 90, strap 3, height 4.4, gap 0.05 |
| kite-112 | `gBV_JTt3Kxk-minimal-pieces` | Kite | size 112.5, strap 3.75, height 4.4, gap 0.05 |
| kite-125 | `gBV_JTt3Kxk-minimal-pieces` | Kite | size 125, strap 4, height 4.4, gap 0.05 |

At each of the X2D's four nozzles, with the X2D's own presets and Bambu PLA Basic:

| Nozzle | Process | Stock first line | Line | Layer |
|---|---|---|---|---|
| 0.2 | `0.10mm Standard @BBL X2D 0.2 nozzle` | 0.25 | 0.22 | 0.1 |
| 0.4 | `0.20mm Standard @BBL X2D` | 0.5 | 0.42 | 0.2 |
| 0.6 | `0.30mm Standard @BBL X2D 0.6 nozzle` | 0.62 | 0.62 | 0.3 |
| 0.8 | `0.40mm Standard @BBL X2D 0.8 nozzle` | 0.82 | 0.82 | 0.4 |

And with two presets: **stock** (the process above, nothing changed) and **house** (concentric
bottom surface, `infill_wall_overlap` 30%, and the first line as wide as the ordinary line). At 0.4
the house preset is the checked-in `tools/bambu/presets/bed-face-0.20.json`; at the other nozzles
`house_preset` writes the same three keys over that nozzle's process.

7 pieces × 4 nozzles × 2 presets = 56 slices.

## How each slice is scored

The lowest layer is drawn from below at 30 px a millimeter, as in the design doc's §6. Bare bed
closed in by lines is split in two:

- **Slits**: bare spots no wider than a slit. These are what the check counts: it passes when they
  cover under 0.6% of the face and the largest is under 0.2 sq mm.
- **Wide bare spots**: wider ones. Most are holes the design cuts (101 in each star, 31 in the
  radial). A wide spot the same piece's 0.4 stock slice does not have is new: a middle no line
  reached, or a slit grown wide. A slice with any new one is marked **core**.

A printed patch of 1 sq mm or more counts as a piece. A slice with fewer pieces than the same
piece's 0.4 stock slice is marked **lost** (a piece dropped). No slice in this sweep lost one.

Two rules were tried first and dropped, because the pictures showed them wrong:

- *Core by wide area*: total wide area against 0.4 stock went from −40 sq mm at 0.2 to +187 at 0.8 on
  every piece alike. That is the line width moving every edge, not a middle left bare.
- *Lost by printed area*: the kites from a 90 mm coaster, at 0.2 and with the 0.4 house preset,
  printed 0.83 to 0.85 of the 0.4 stock area and would have been marked lost, but the pictures show all ten kites there. Printed area follows
  the line width too.

The piece count has a known blind spot: a strap dropped inside a one-piece coaster leaves the coaster
one piece. It would show as two holes merging (fewer wide spots), which the core mark does not catch.

The best setting for a piece is the slice that passes, is neither lost nor core, and has the least
bare share; where the house preset leaves a slice the same as stock, stock is named.

## Commands

Slice and score: `python3 tools/bed_face_sweep.py run` (a job already scored is skipped; `--force`
slices again, `--rescore` scores the kept slices again). Each slice is
`bambu slice compose <recipe.yaml> [-s "<machine>;<house preset>"] -d build/bed-face-sweep/slices -o <job>.3mf --no-record --plate-type hot_plate`,
with `BIKAR_DIR` pointing at a bikar checkout.

Page: `python3 tools/bed_face_sweep.py page` writes `build/bed-face-sweep/index.html`.

Table: `python3 tools/bed_face_sweep.py table` prints the table below.

Self-test: `python3 tools/bed_face_sweep.py --self-test` (run by `make validate-print-review`).

**Size and time.** 56 slices. The main run sliced and scored 43 of them in 8.0 minutes
(02:00:30 to 02:08:30 UTC on 2026-10-11, the evening of the 10th locally), about 11 seconds a
slice, of which the slicer took 3 to 13. The other 13 came from two smaller runs: a 2-job trial and
an 11-job run. Scoring all 56 again from the kept slices took 5.0 minutes. A full sweep from
nothing is estimated at about 10 minutes at that rate; it was not timed in one piece.

## Results

"Printed vs 0.4 stock" and the wide spot total are context only: both follow the line width.
"Slicer time" is the slicer's own estimate for the piece alone, not a measured print.

| Job | First line | Bare share % | Largest pocket mm² | Slits | Pieces | Printed vs 0.4 stock | Wide bare spots (new) | Check | Slicer time min | Grams |
|---|---|---|---|---|---|---|---|---|---|---|
| star-2-n0.2-stock | 0.25 | 0.150 | 0.054 | 465 | 1 | 1.044 | 101 (0) | PASS | 241 | 15.54 |
| star-2-n0.2-house | 0.22 | 0.123 | 0.009 | 2826 | 1 | 1.04 | 101 (0) | PASS | 244 | 15.55 |
| star-2-n0.4-stock | 0.5 | 3.097 | 0.695 | 2152 | 1 | 1.0 | 101 (0) | FAIL | 52 | 16.41 |
| star-2-n0.4-house | 0.42 | 0.139 | 0.044 | 302 | 1 | 1.037 | 101 (0) | PASS | 55 | 16.38 |
| star-2-n0.6-stock | 0.62 | 0.536 | 0.478 | 229 | 1 | 1.025 | 101 (0) | FAIL | 37 | 16.06 |
| star-2-n0.6-house | 0.62 | 0.536 | 0.478 | 223 | 1 | 1.025 | 101 (0) | FAIL | 37 | 16.07 |
| star-2-n0.8-stock | 0.82 | 1.090 | 1.155 | 142 | 1 | 0.985 | 155 (54) | FAIL core | 28 | 16.24 |
| star-2-n0.8-house | 0.82 | 1.090 | 1.155 | 142 | 1 | 0.985 | 155 (54) | FAIL core | 28 | 16.24 |
| star-3-n0.2-stock | 0.25 | 0.252 | 0.412 | 2764 | 1 | 1.013 | 101 (0) | FAIL | 283 | 17.37 |
| star-3-n0.2-house | 0.22 | 0.156 | 0.057 | 3726 | 1 | 1.012 | 101 (0) | PASS | 281 | 17.37 |
| star-3-n0.4-stock | 0.5 | 0.884 | 0.688 | 2708 | 1 | 1.0 | 101 (0) | FAIL | 69 | 18.4 |
| star-3-n0.4-house | 0.42 | 0.367 | 0.096 | 1142 | 1 | 1.01 | 101 (0) | PASS | 69 | 18.46 |
| star-3-n0.6-stock | 0.62 | 1.664 | 0.936 | 633 | 1 | 0.991 | 105 (4) | FAIL core | 47 | 22.5 |
| star-3-n0.6-house | 0.62 | 0.163 | 0.134 | 402 | 1 | 1.007 | 101 (0) | PASS | 48 | 22.58 |
| star-3-n0.8-stock | 0.82 | 0.266 | 0.492 | 162 | 1 | 0.965 | 259 (158) | FAIL core | 35 | 22.84 |
| star-3-n0.8-house | 0.82 | 0.266 | 0.492 | 162 | 1 | 0.965 | 259 (158) | FAIL core | 35 | 22.85 |
| star-4-n0.2-stock | 0.25 | 0.166 | 0.049 | 2395 | 1 | 1.007 | 101 (0) | PASS | 288 | 18.61 |
| star-4-n0.2-house | 0.22 | 0.138 | 0.032 | 3903 | 1 | 1.006 | 101 (0) | PASS | 290 | 18.63 |
| star-4-n0.4-stock | 0.5 | 0.572 | 0.389 | 2152 | 1 | 1.0 | 101 (0) | FAIL | 70 | 20.02 |
| star-4-n0.4-house | 0.42 | 0.388 | 0.109 | 1617 | 1 | 1.004 | 101 (0) | PASS | 72 | 20.08 |
| star-4-n0.6-stock | 0.62 | 0.656 | 0.710 | 1520 | 1 | 0.998 | 101 (0) | FAIL | 46 | 22.77 |
| star-4-n0.6-house | 0.62 | 0.103 | 0.089 | 615 | 1 | 1.004 | 101 (0) | PASS | 47 | 22.9 |
| star-4-n0.8-stock | 0.82 | 1.501 | 1.263 | 633 | 1 | 0.991 | 103 (2) | FAIL core | 40 | 28.03 |
| star-4-n0.8-house | 0.82 | 0.122 | 0.190 | 432 | 1 | 1.006 | 101 (0) | PASS | 40 | 28.2 |
| radial-3-n0.2-stock | 0.25 | 0.247 | 0.090 | 1811 | 1 | 1.006 | 31 (0) | PASS | 185 | 13.86 |
| radial-3-n0.2-house | 0.22 | 0.047 | 0.099 | 1076 | 1 | 1.009 | 31 (0) | PASS | 188 | 13.91 |
| radial-3-n0.4-stock | 0.5 | 0.531 | 0.384 | 1668 | 1 | 1.0 | 31 (0) | FAIL | 45 | 15.04 |
| radial-3-n0.4-house | 0.42 | 0.106 | 0.158 | 559 | 1 | 1.006 | 31 (0) | PASS | 46 | 15.19 |
| radial-3-n0.6-stock | 0.62 | 0.457 | 0.786 | 490 | 1 | 1.004 | 31 (0) | FAIL | 33 | 17.38 |
| radial-3-n0.6-house | 0.62 | 0.091 | 0.555 | 253 | 1 | 1.008 | 31 (0) | FAIL | 33 | 17.59 |
| radial-3-n0.8-stock | 0.82 | 0.755 | 0.858 | 404 | 1 | 0.997 | 35 (4) | FAIL core | 27 | 20.08 |
| radial-3-n0.8-house | 0.82 | 0.090 | 0.061 | 189 | 1 | 1.003 | 36 (5) | PASS core | 27 | 20.42 |
| kite-90-n0.2-stock | 0.25 | 2.779 | 0.047 | 436 | 10 | 0.83 | 0 (0) | FAIL | 14 | 0.36 |
| kite-90-n0.2-house | 0.22 | 0.793 | 0.034 | 77 | 10 | 0.849 | 0 (0) | FAIL | 14 | 0.36 |
| kite-90-n0.4-stock | 0.5 | 4.948 | 0.193 | 31 | 10 | 1.0 | 0 (0) | FAIL | 8 | 0.35 |
| kite-90-n0.4-house | 0.42 | 3.275 | 0.196 | 13 | 10 | 0.852 | 0 (0) | FAIL | 8 | 0.35 |
| kite-90-n0.6-stock | 0.62 | 2.723 | 0.196 | 15 | 10 | 1.021 | 0 (0) | FAIL | 7 | 0.34 |
| kite-90-n0.6-house | 0.62 | 2.723 | 0.196 | 15 | 10 | 1.021 | 0 (0) | FAIL | 7 | 0.34 |
| kite-90-n0.8-stock | 0.82 | 8.651 | 0.603 | 10 | 10 | 0.927 | 0 (0) | FAIL | 6 | 0.31 |
| kite-90-n0.8-house | 0.82 | 8.651 | 0.603 | 10 | 10 | 0.927 | 0 (0) | FAIL | 6 | 0.31 |
| kite-112-n0.2-stock | 0.25 | 2.246 | 0.044 | 662 | 10 | 1.006 | 0 (0) | FAIL | 17 | 0.58 |
| kite-112-n0.2-house | 0.22 | 0.363 | 0.021 | 74 | 10 | 1.033 | 0 (0) | PASS | 17 | 0.58 |
| kite-112-n0.4-stock | 0.5 | 5.894 | 0.575 | 23 | 10 | 1.0 | 0 (0) | FAIL | 8 | 0.55 |
| kite-112-n0.4-house | 0.42 | 0.517 | 0.056 | 13 | 10 | 1.055 | 0 (0) | PASS | 8 | 0.56 |
| kite-112-n0.6-stock | 0.62 | 0.686 | 0.067 | 19 | 10 | 1.061 | 0 (0) | FAIL | 7 | 0.54 |
| kite-112-n0.6-house | 0.62 | 0.686 | 0.067 | 19 | 10 | 1.061 | 0 (0) | FAIL | 7 | 0.54 |
| kite-112-n0.8-stock | 0.82 | 3.976 | 0.439 | 20 | 10 | 1.161 | 0 (0) | FAIL | 7 | 0.53 |
| kite-112-n0.8-house | 0.82 | 3.976 | 0.439 | 20 | 10 | 1.161 | 0 (0) | FAIL | 7 | 0.53 |
| kite-125-n0.2-stock | 0.25 | 3.177 | 0.129 | 901 | 10 | 0.957 | 0 (0) | FAIL | 20 | 0.81 |
| kite-125-n0.2-house | 0.22 | 0.763 | 0.040 | 387 | 10 | 0.986 | 0 (0) | FAIL | 20 | 0.81 |
| kite-125-n0.4-stock | 0.5 | 0.860 | 0.141 | 32 | 10 | 1.0 | 0 (0) | FAIL | 9 | 0.79 |
| kite-125-n0.4-house | 0.42 | 0.494 | 0.063 | 22 | 10 | 0.999 | 0 (0) | PASS | 9 | 0.79 |
| kite-125-n0.6-stock | 0.62 | 5.366 | 0.730 | 10 | 10 | 0.957 | 0 (0) | FAIL | 8 | 0.78 |
| kite-125-n0.6-house | 0.62 | 5.366 | 0.730 | 10 | 10 | 0.957 | 0 (0) | FAIL | 8 | 0.78 |
| kite-125-n0.8-stock | 0.82 | 3.670 | 0.425 | 30 | 10 | 1.089 | 0 (0) | FAIL | 7 | 0.74 |
| kite-125-n0.8-house | 0.82 | 3.670 | 0.425 | 30 | 10 | 1.089 | 0 (0) | FAIL | 7 | 0.74 |

| Best for | Job |
|---|---|
| star-2 | star-2-n0.2-house |
| star-2-n0.2 | star-2-n0.2-house |
| star-2-n0.4 | star-2-n0.4-house |
| star-2-n0.6 | star-2-n0.6-stock |
| star-2-n0.8 | star-2-n0.8-stock |
| star-3 | star-3-n0.2-house |
| star-3-n0.2 | star-3-n0.2-house |
| star-3-n0.4 | star-3-n0.4-house |
| star-3-n0.6 | star-3-n0.6-house |
| star-3-n0.8 | star-3-n0.8-stock |
| star-4 | star-4-n0.6-house |
| star-4-n0.2 | star-4-n0.2-house |
| star-4-n0.4 | star-4-n0.4-house |
| star-4-n0.6 | star-4-n0.6-house |
| star-4-n0.8 | star-4-n0.8-house |
| radial-3 | radial-3-n0.2-house |
| radial-3-n0.2 | radial-3-n0.2-house |
| radial-3-n0.4 | radial-3-n0.4-house |
| radial-3-n0.6 | radial-3-n0.6-house |
| radial-3-n0.8 | radial-3-n0.8-house |
| kite-90 | kite-90-n0.2-house |
| kite-90-n0.2 | kite-90-n0.2-house |
| kite-90-n0.4 | kite-90-n0.4-house |
| kite-90-n0.6 | kite-90-n0.6-stock |
| kite-90-n0.8 | kite-90-n0.8-stock |
| kite-112 | kite-112-n0.2-house |
| kite-112-n0.2 | kite-112-n0.2-house |
| kite-112-n0.4 | kite-112-n0.4-house |
| kite-112-n0.6 | kite-112-n0.6-stock |
| kite-112-n0.8 | kite-112-n0.8-stock |
| kite-125 | kite-125-n0.4-house |
| kite-125-n0.2 | kite-125-n0.2-house |
| kite-125-n0.4 | kite-125-n0.4-house |
| kite-125-n0.6 | kite-125-n0.6-stock |
| kite-125-n0.8 | kite-125-n0.8-stock |

"Best" at one nozzle is the least bad slice there; it can still fail (kite-90 at every nozzle,
star-2 at 0.6 and 0.8). kite-90 has no passing slice at all, so its overall "best" is the least
bad one.

## What the pictures showed

Looked at, not measured:

- **Where the house preset changes nothing.** At 0.6 and 0.8 the stock first line already equals the
  ordinary line (0.62, 0.82), and on the narrow straps and the kites the first layer is walls and gap
  fill with no bottom surface for the concentric pattern or the 30% overlap to change. Nine of the
  fourteen house slices at 0.6 and 0.8 score the same as stock to three decimals; the five that
  differ are star-3 at 0.6, star-4 at 0.6 and 0.8, and radial-3 at 0.6 and 0.8.
- **star-3 at 0.8.** Walls and gap fill only. The 158 new wide spots are small closed-in triangles at
  the strap crossings.
- **star-2 at 0.8.** The largest slit (1.155 sq mm) is a bare triangle where three straps meet,
  between gap-fill lines that stop short of each other.
- **radial-3 at 0.6, house.** Fails on its largest slit alone (0.555): two bare spots inside the
  bottom surface at the center.
- **radial-3 at 0.8, house.** Passes the check, but leaves 5 new wide spots; one is a small bare spot
  near the center.
- **Kites at 0.6 and 0.8.** The kite tips come out rounder in the plan as the line widens.

## Hedges carried with every number

- It is the slicer's plan, not a print. Bare in the plan is very likely bare in the print; covered in
  the plan is not proof of a covered print.
- Both bars (0.6% share, 0.2 sq mm pocket) were fitted to ten slices at the 0.4 nozzle, and may not hold at
  the others. At 0.8, for one, the 0.82 line is wider than a 0.5 mm slit, so a slit the plan shows
  may close under squash; whether it does is not known.
- Only the 0.4 nozzle is fitted on the printer. The other three nozzles are what Bambu Studio would
  plan if one were fitted.
- One filament (Bambu PLA Basic), one plate type (`hot_plate`), each nozzle's stock layer height,
  seven pieces.
