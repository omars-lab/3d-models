---
date: 2026-09-27
feeds:
  - '[[constructions/ledger]]'
  - '[[tasks/catalog-expansion/backlog]]'
---

<!-- Produced 2026-09-27 by Claude (local runs of the youtube O1/O2/O3 targets against a bikar branch, bikar CLI renders, qiyas mesh compare, GeoGebra coordinate dumps); checked in verbatim. Feeds: docs/constructions/ledger.md (the n3IidKfXE1I, nmEjCTzMbDg and rDuxHF3xMOc oracle cells and notes) and docs/tasks/catalog-expansion/backlog.md (item "Oracle FAILs"). -->

# Ledger oracle FAILs, 2026-09-27

Scope: the five FAILs and the one missing verdict that the
[2026-09-27 oracle runs](ledger-oracle-runs-2026-09-27.md) left in the
[constructions ledger](../constructions/ledger.md). For each one: the cause, with the
evidence, and a class.

- **(a)** The `.bkr` is wrong. Fixed in bikar.
- **(b)** The check is wrong. The fix belongs to youtube, which has no remote, so it is
  proposed here and not made.
- **(c)** The gap is deliberate. It is noted in the ledger, and the FAIL stays.

Lines in code blocks are what a tool printed, copied from its output. Lines marked
**diagnostic** were run on a scratch copy that was changed on purpose. They show a
cause and are not ledger verdicts.

## Trees and tools

| What | Ref |
|---|---|
| bikar | branch `oracle-fails-2026-09-27` at `9726578` (worktree off `origin/main`), CLI built; the `.bkr` files are its `patterns/Constructions/<id>.bkr` |
| youtube | `main` `6d359b1`, clean; `make naqsh-coords`, `make naqsh-score`, `make reference UNIT=20 DEPTH=4` |
| qiyas | `main` `abdd6fd`, `.venv/bin/qiyas mesh compare` |

The O2 hero image was rebuilt from each construction with
`scripts/ggb-build.sh --export` and then `scripts/ggb-render.sh --dpi 96`, before
anything was scored.

## Summary

| FAIL | cause | class | action | printed now |
|---|---|---|---|---|
| `n3IidKfXE1I` O1 62/2 | the fixture came from a 61-step draft (youtube `40acf3d`, 2026-09-16). The final assembly (`r_3`, `s_3`, `m1'`…`m4'`, `l1`) was added on 2026-09-17 | (a) | re-imported from the current source, 0 refused | `PASS: 64 compared, 0 failed, 84 skipped/extra` |
| `n3IidKfXE1I` O3 0.133 | same: the old `.bkr` drew one working frame, not the field | (a) | same re-import | `O3 PASS: coverage 1.000 …` |
| `n3IidKfXE1I` O2, no verdict | youtube `naqsh_score.py` treats `ggb_score.py`'s FAIL exit (2) as a crash | (b) | patch proposed below | `O2 PASS: edge-SSIM 0.9149 …` (the new `.bkr` passes, so the crash path is never reached) |
| `nmEjCTzMbDg` O1 25/15 | `R = Intersect(t, m, 2)` picks the other root in bikar. The error carries into `c_1`, `d_1`, `D`, `T`, `a`. O1 also cannot compare parabolas, hyperbolas or arcs | (b) | youtube patch proposed below | `FAIL: 25 compared, 15 failed, 35 skipped/extra` (unchanged) |
| `nmEjCTzMbDg` O2 0.9176/0.2589 | the same wrong `R`, **plus** a bikar lowering bug: a drawn full circle was two 180° half-arcs, and under `rotate` 14 of 18 rim circles traced one half twice | (b) + (a) | the half-arc bug is fixed in bikar (four 90° arcs); the `R` fix is proposed | `O2 FAIL: … recall 0.9176 precision 0.2589 …` (held by `R`) |
| `rDuxHF3xMOc` O2 0.8381/1.0 | the export keeps the tile's four full-width bounding lines visible (the video shows them); the coaster draws the tile only | (c) | ledger note "by design", FAIL kept | `O2 FAIL: … recall 0.8381 precision 1.0 …` (unchanged) |

## n3IidKfXE1I — the draft import (a)

The fixture `packages/core/tests/fixtures/geogebra/n3IidKfXE1I.json` had source sha
`b93288707e…`. That matches youtube `40acf3d` (61 steps). The current
`reconstructions/n3IidKfXE1I/construction.ggb-commands` (sha `0cf1d28b…`) has 73
statements and 69 tagged steps. youtube `2623813` and `88feb31` (2026-09-17) added the
closing reflections `r_3`, `s_3`, the four closing units and the finished tile `l1`.
Those two missing lines are O1's 2 failures. The old coaster was a mid-video working
frame: three scaffold polygons and one of each unit, one of them an empty hexagon.

Re-imported with the youtube conda env's `ggb_build.py --ast-json`, then
`bikar import geogebra … --piece Coaster`. Printed on bikar `9726578`:

```
PASS: 64 compared, 0 failed, 84 skipped/extra
O2 PASS: edge-SSIM 0.9149 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 8 (advisory); 37.8 px/unit, origin (-30, -133), stroke 1.2 px, ink box (0, 0, 500, 396)
```

O3 (`make reference` wrote 336 polygons; `bikar render --piece Coaster --format stl --check`):

```
mesh gate: watertight=true euler=2 degenerate=0 minFeature=4mm (floor 1.2mm) — PASS
linkage gate: bodies=1 pointContacts=0 errors=0 warn=0 — PASS
O3 PASS: coverage 1.000 (min 0.99), local 0.400 mm at (-121.705, 56.8788) (max 1); context: iou 0.664, hausdorff2d 102.52 mm, hausdorff3d 102.52 mm, volume 0.664, extra-fill 16802.3 mm2
```

The O2 crop was read by eye as well. The whole field matches the GeoGebra export.

**The coaster.** When the whole field is fit to a 90 mm round coaster, it renders as
near-solid gold. That fails the look check, so it was not shipped. The coaster file
is emitted with `--coaster-omit l1` (the CS-12 option). It draws the 12-fold `m1`
rosette alone: round, 3.7321 units across, with open cells at 90 mm and 40 mm.
`bikar render --coaster Coaster --format stl --check` at size 90:

```
mesh gate: watertight=true euler=2 degenerate=0 minFeature=1.2mm (floor 0.8mm) — PASS
linkage gate: bodies=1 pointContacts=0 errors=0 warn=0 — PASS
STL written to …/src/Coasters/n3IidKfXE1I-coaster-standard.stl (160860 triangles, 7855 KiB, volume 27.4 cm³)
```

This is a taste call for Omar: the coaster drops the 6-fold and 4-fold units that
`l1` adds. It also changes the n3Iid piece on the
[minis-03](../plates/minis-03.yaml) and [minis-04](../plates/minis-04.yaml) plates.

## nmEjCTzMbDg — two causes behind one FAIL

### The rim circles (a), fixed in bikar

A GeoGebra `Circle` that is drawn on its own was lowered as `divide into 2` and then
two half-arcs, the second marked `major`. bikar's `arcFromPoints` takes the minor sweep
in [−π, π], and `major` then flips it. At exactly 180° the minor sweep is ±π and
rounding picks the sign. Each copy under `rotate 18 around H` rounds differently, so
some copies traced the same half twice. The fix is `divide into 4` and four 90° arcs,
which have no tie. Details are in bikar `docs/issues/2026-09-27-full-circle-half-arc-tie.md`.

Diagnostic (a scratch copy with `R` corrected but the old half-arcs; the middle of the line was cut when it was first copied):

```
O2 FAIL: edge-SSIM 0.9748 (min 0.7), recall 0.9536 precision 1.0 (min 0.98), ... FAILED: recall
```

The crop showed only about 4 of the 18 rim circles drawn in full.

### The wrong root for R (b), proposed

bikar lowers `Intersect(t, m, 2)` to `pick 2`, ordered by line parameter. GeoGebra's
index comes from its own solver order, which depends on history. youtube's
`ggb_coords.py` dump gives the same point for both forms of the command:

| | R |
|---|---|
| bikar `pick 2` | (0.5, 2.1189) |
| GeoGebra, `Intersect(t, m, 2)` and `Intersect(t, m, S)` alike | (0.5, −0.6983357805485) |

Diagnostic (the youtube command changed to `Intersect(t, m, S)` in a scratch copy, and the
`.bkr` line changed to `pick nearest S`, on the new lowering):

```
FAIL: 31 compared, 9 failed, 35 skipped/extra
O2 PASS: edge-SSIM 0.9796 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 32 (advisory); 377.9 px/unit, origin (291, 1), stroke 3.8 px, ink box (427, 136, 3088, 2798)
```

The 9 O1 failures left all come from O1 itself, not from the geometry:

- the parabolas `d`, `q` and the hyperbola `t`, and the arcs `e_1`, `f_1`, `g_1`, each
  printed "no comparison for GeoGebra type";
- `e_1_host`, `f_1_host` and `g_1_host`, printed as "extra naqsh label with no
  reference object".

Printed on bikar `9726578` (youtube unchanged, so `R` is still wrong):

```
FAIL: 25 compared, 15 failed, 35 skipped/extra
O2 FAIL: edge-SSIM 0.8129 (min 0.7), recall 0.9176 precision 0.2589 (min 0.98), phash 40 (advisory); 377.9 px/unit, origin (-642, -940), stroke 3.8 px, ink box (0, 0, 4050, 3005); FAILED: recall, precision
```

**Do not print the nmEj coaster.** It is built on the wrong `R`. At 90 mm it renders as
near-solid gold with slivers around a centre rosette. That was true before this fix too:
the STL volume is 31.7 cm³ both before and after. A diagnostic copy of the coaster with
only `R` changed renders as a clean open rosette (27.1 cm³, not yet refit to the rim).
The coaster files are re-vendored so they match bikar, but the print verdict waits on
the youtube change.

## rDuxHF3xMOc — by design (c)

youtube `reconstructions/rDuxHF3xMOc/construction.ggb-commands` ends with
`@hide except m1* m2* m3* l1* bot rgt top lft`. The export deliberately keeps the tile's
four full-width bounding lines, as the video shows them. A coaster cannot draw an
infinite line, and the `.bkr` draws the tile. O2's recall counts those lines as missed.

Printed on bikar `9726578`:

```
PASS: 41 compared, 0 failed, 54 skipped/extra
O2 FAIL: edge-SSIM 0.9663 (min 0.7), recall 0.8381 precision 1.0 (min 0.98), phash 6 (advisory); 377.9 px/unit, origin (1164, 26), stroke 3.0 px, ink box (0, 0, 3879, 2456); FAILED: recall
```

Diagnostic (a scratch copy with `@hide bot rgt top lft` appended):

```
O2 PASS: edge-SSIM 0.9367 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 26 (advisory); 377.9 px/unit, origin (1164, 26), stroke 3.0 px, ink box (1314, 176, 3217, 2079)
```

The lines are the whole gap. The FAIL stays, noted in the ledger.

## Proposed youtube patches (not applied)

youtube has no remote, and changes there are the owner's call.

**1. `reconstructions/nmEjCTzMbDg/construction.ggb-commands` L84:** name the root by a
point on it, not by a history-dependent index.

```diff
-R = Intersect(t, m, 2)            # t=04:35  the branch point beyond S: centre of the outer cusp circle
+R = Intersect(t, m, S)            # t=04:35  the branch point beyond S: centre of the outer cusp circle
```

L61 `L = Intersect(d, p, 2)` and L74 `O = Intersect(q, p, 2)` use the same
index-picking. They agree today, but they could be hardened the same way. After the
change, bikar regenerates the fixture and goldens with the commands in bikar
`docs/issues/2026-09-22-nmej-open-lineart-migration.md`. The coaster fit changes from
11.7376 units, so its render must be looked at again before it is printed.

**2. `scripts/naqsh_score.py`, `ssim_score`:** `ggb_score.py` ends with
`sys.exit(0 if passed else 2)`. Its error paths call `sys.exit("<message>")`, which exits
1 with nothing on stdout. So 2 is a FAIL verdict and 1 is the real crash.

```diff
     r = subprocess.run(cmd, capture_output=True, text=True)
-    if r.returncode not in (0, 1) or not r.stdout.strip():
+    # ggb_score.py: 0 = PASS, 2 = FAIL (both print the JSON result); 1 = it errored
+    if r.returncode not in (0, 2) or not r.stdout.strip():
         sys.stderr.write(r.stderr)
         raise SystemExit(f"naqsh_score: ggb_score.py failed (exit {r.returncode})")
```

This was not run: youtube was not edited. The re-imported n3Iid now passes the SSIM
check, so its run never reaches this path.

**3. O1 coverage (optional):** comparing parabolas, hyperbolas and arcs, and matching
the importer's `<arc>_host` circles to their arc, would turn nmEj's last 9 O1 failures
into comparisons. Not drafted as a diff: it is new O1 work, not a one-line fix.
