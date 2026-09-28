<!-- Produced 2026-09-27 by Claude (local runs of the youtube O1/O2/O3 targets, bikar CLI, qiyas mesh compare); checked in verbatim. Feeds: docs/constructions/ledger.md (the oracle cells). -->

# Ledger oracle runs, 2026-09-27

Scope: the oracle cells that were blank in the [constructions ledger](../constructions/ledger.md)
on 2026-09-25 (catalog-expansion backlog item 2). Each line below is what the tool
printed, copied from its output; the ledger cells are taken from these lines and
nothing else. What the oracles are and what their thresholds mean lives in
[construction equivalence](../construction-equivalence.md).

## Trees and tools

| What | Ref |
|---|---|
| bikar | a fresh detached worktree at `origin/main` `8639c76`, `npm ci`, core + CLI built; the `.bkr` files are its `patterns/Constructions/<id>.bkr` |
| youtube | `main` `6d359b1`, clean; `make naqsh-coords`, `make naqsh-score`, `make reference` |
| qiyas | `main` `abdd6fd`, `.venv/bin/qiyas mesh compare` |

Sanity runs before the blank cells, to check the setup reproduces a recorded verdict:
`7apC5Q9QS-8` O1 printed `PASS: 144 compared, 0 failed, 803 skipped/extra` and O2
`O2 PASS … recall 1.0 precision 1.0` (the ledger has PASS 144/0 and 1.000/1.000);
`GimTvN9hw4U` O3 printed `O3 PASS: coverage 1.000 (min 0.99), local 0.000 mm` from
the same 119 830-byte, 42-polygon reference the equivalence doc measured.

## Commands

- **O1:** `make naqsh-coords ID=<id> NAQSH=<bikar>/patterns/Constructions/<id>.bkr OUT=<scratch> BIKAR_DIR=<bikar>` in youtube.
- **O2:** `make naqsh-score ID=<id> NAQSH=… OUT=<scratch> BIKAR_DIR=<bikar>` in youtube. For
  `n3IidKfXE1I`, `nmEjCTzMbDg` and `rDuxHF3xMOc` the hero was first rebuilt with the loop's
  own two commands
  (`scripts/ggb-build.sh --in reconstructions/<id>/construction.ggb-commands --out render/export.ggb --export`, then
  `scripts/ggb-render.sh --dpi 96 --out render/export.png render/export.ggb`) into a scratch data dir passed as `YT_OUTPUT_DIR`;
  each printed `ev=export_size … verdict=ok`. The shared data dir was not touched.
- **O3:** `make reference IN=reconstructions/<id>/construction.ggb-commands OUT=<dir>/coords.json UNIT=20 DEPTH=4`
  in youtube, then `bikar render <id>.bkr --piece Coaster --format stl --check -o <dir>/print.stl`,
  then `qiyas mesh compare <dir>/reference.stl <dir>/print.stl`. `DEPTH=4` matches the
  `.bkr` files' `param depth = 4`; the footprint is sliced at mid-height either way.

## What each tool printed

### O1

| id | printed |
|---|---|
| `lEfWSogWscs` | `PASS: 49 compared, 0 failed, 22 skipped/extra` |
| `n3IidKfXE1I` | `FAIL: 62 compared, 2 failed, 73 skipped/extra` — the two rows: `r_3 line FAIL missing in naqsh`, `s_3 line FAIL missing in naqsh` |
| `nmEjCTzMbDg` | `FAIL: 25 compared, 15 failed, 35 skipped/extra` — six rows are `no comparison for GeoGebra type` parabola (`d`, `q`), hyperbola (`t`) and arc (`e_1`, `f_1`, `g_1`); three are `extra naqsh label with no reference object` (`e_1_host`, `f_1_host`, `g_1_host`); the rest are real misses: points `R`, `D`, `T` off by 2.817, 4.482 and 8.965, circles `c_1`, `d_1`, segment `a` |
| `sDO9fpu76v8` | `PASS: 84 compared, 0 failed, 62 skipped/extra` |
| `tA8eSdVx_EQ` | `PASS: 28 compared, 0 failed, 24 skipped/extra` |

### O2

| id | printed |
|---|---|
| `lEfWSogWscs` | `O2 PASS: edge-SSIM 0.9305 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 22 (advisory); 377.8 px/unit, origin (-103, -159), stroke 1.5 px, ink box (177, 11, 1129, 962)` |
| `n3IidKfXE1I` | `naqsh_score: ggb_score.py failed (exit 2)` — no verdict; see below |
| `nmEjCTzMbDg` | on the data-dir hero: `… export.png is 865x865 px but … export.ggb has a 800x585 view … a stale or foreign hero` (refused). On the rebuilt hero: `O2 FAIL: edge-SSIM 0.8129 (min 0.7), recall 0.9176 precision 0.2589 (min 0.98), phash 40 (advisory); 377.9 px/unit, origin (-642, -940), stroke 3.8 px, ink box (0, 0, 4050, 3005); FAILED: recall, precision` |
| `rDuxHF3xMOc` | `O2 FAIL: edge-SSIM 0.9663 (min 0.7), recall 0.8381 precision 1.0 (min 0.98), phash 6 (advisory); 377.9 px/unit, origin (1164, 26), stroke 3.0 px, ink box (0, 0, 3879, 2456); FAILED: recall` — the same on the data-dir hero and the rebuilt one |
| `sDO9fpu76v8` | `O2 PASS: edge-SSIM 0.8579 (min 0.7), recall 0.996 precision 0.9972 (min 0.98), phash 22 (advisory); 37.7 px/unit, origin (19, -8), stroke 1.2 px, ink box (32, 5, 303, 264)` |
| `tA8eSdVx_EQ` | `O2 PASS: edge-SSIM 0.9747 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 24 (advisory); 377.9 px/unit, origin (149, 1), stroke 1.5 px, ink box (341, 167, 1469, 1267)` |

**Why `n3IidKfXE1I` has no O2 verdict.** youtube's `scripts/ggb_score.py` exits 2 when its
edge-SSIM check fails (`sys.exit(0 if passed else 2)`), and exits 1 on a usage error;
`scripts/naqsh_score.py` accepts only exit 0 or 1 from it and treats 2 as a crash. So an
SSIM failure stops the scorer before it prints the O2 line. The fix belongs in youtube
(accept 2 as a scored result) and is reported there, not made here. A scratch copy with
only that line changed printed
`O2 FAIL: edge-SSIM 0.3312 (min 0.7), recall 0.1473 precision 0.8153 …` — a diagnostic, not the tool's verdict, so it is not in the ledger.

What the crops show (looked at, not inferred): `rDuxHF3xMOc`'s export draws two
full-width construction lines that the `.bkr` does not — the only difference visible in
the crop, so most likely the recall gap;
`nmEjCTzMbDg`'s naqsh drawing carries many construction circles and rays the export
hides, and misses the export's small outer circles; `n3IidKfXE1I`'s export is a tiled
field of the rosette while the `.bkr` draws one cell.

### O3

| id | printed |
|---|---|
| `7apC5Q9QS-8` | `O3 PASS: coverage 1.000 (min 0.99), local 0.000 mm (max 1); context: iou 0.666, hausdorff2d 34.89 mm, hausdorff3d 35.26 mm, volume 0.666, extra-fill 2138.04 mm2` |
| `lEfWSogWscs` | `O3 PASS: coverage 1.000 (min 0.99), local 0.000 mm (max 1); context: iou 1.000, hausdorff2d 0.00 mm, hausdorff3d 10.00 mm, volume 1.000, extra-fill 0.0022 mm2` |
| `n3IidKfXE1I` | `O3 FAIL: coverage 0.133 (min 0.99), local 15.331 mm at (-49.505, 71.659) (max 1); context: iou 0.123, hausdorff2d 95.90 mm, hausdorff3d 95.90 mm, volume 0.207, extra-fill 2473.92 mm2; FAILED: coverage, local` |
| `nmEjCTzMbDg` | no verdict: `make reference` wrote `polygons = 0` and OpenSCAD refused the empty extrusion (exit 1), and `bikar render --piece Coaster` printed `--piece 'Coaster' is not a piece in this file (the file declares no piece, tile, or clip)` — an open line-art construction has no solid region on either side |
| `rDuxHF3xMOc` | `O3 PASS: coverage 1.000 (min 0.99), local 0.000 mm (max 1); context: iou 0.923, hausdorff2d 27.48 mm, hausdorff3d 27.40 mm, volume 0.923, extra-fill 535.76 mm2` |
| `sDO9fpu76v8` | `O3 PASS: coverage 1.000 (min 0.99), local 0.000 mm (max 1); context: iou 0.463, hausdorff2d 43.49 mm, hausdorff3d 43.49 mm, volume 0.463, extra-fill 5992.62 mm2` |
| `tA8eSdVx_EQ` | `O3 PASS: coverage 1.000 (min 0.99), local 0.000 mm (max 1); context: iou 0.496, hausdorff2d 16.00 mm, hausdorff3d 16.00 mm, volume 0.498, extra-fill 931.67 mm2` |

`n3IidKfXE1I`'s O3 agrees with its O2 crop: the GeoGebra construction's polygons cover a
tiled field and the `.bkr` extrudes one cell, so 13 % of the reference is covered.
