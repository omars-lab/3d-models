<!-- Held edits for the ten-petal blossom (n_ICgwOr6qs), written 2026-11-03 by agent G of the authorized-decisions session. Apply after bikar PR #368 merges; delete this file in that commit. -->

# n_ICgwOr6qs — the edits owed after the bikar PR merges (held, not committed)

Not urgent after the merge: with the row still `—`, hook 51 stays green (checked against bikar branch blossom-n_I: "catalog: OK — 89 files in step"), so the ledger row and the note can follow in their own commit.

Held because the ledger's own column rule says the naqsh cell stays `—` until the
.bkr is merged, and hook 51 (pattern catalog) reads bikar at origin/main.

## docs/constructions/ledger.md — exact per-line replacements (keep line 130 where it is:
## every edit above it is in-line, the use-case map pins `ledger.md:L130`)

Replace the line
    **14 [the count marker stays as it is] migrated** so far: a row counts as
with
    **15 [the count marker stays as it is] migrated** so far: a row counts as

Replace the line (the end of the 88q sentence)
    main as it is, nothing refused.
with
    main as it is, nothing refused. `n_ICgwOr6qs` landed 2026-11-03 with bikar PR #368, a minimal coaster too: Samira Mian's Sheikh Zayed Mosque fivefold blossom, the first construction drawn in arcs only (twenty `connect arc` lines, no segment), whose four `CircularArc` needed the D-080 coordinate bootstrap and whose coaster needed the importer to measure an arc-only pattern's span (same PR).

Replace the line
    All fourteen now vendor a standard (90 mm) coaster mesh under `src/Coasters/` and
with
    All fifteen now vendor a standard (90 mm) coaster mesh under `src/Coasters/` and

Replace the line
    `CS-10`, `CS-11`, `CS-12`, `CS-13`, `CS-14`, `CS-15`, `CS-16`, `CS-17`) — P3.3 of the umbrella plan,
with
    `CS-10`, `CS-11`, `CS-12`, `CS-13`, `CS-14`, `CS-15`, `CS-16`, `CS-17`, `CS-18`) — P3.3 of the umbrella plan,

Replace the line (the n_ICgwOr6qs row)
    | `n_ICgwOr6qs` | A ten-petal blossom from one compass setting | done | — | — | — | — | — | — | — |
with
    | `n_ICgwOr6qs` | A ten-petal blossom from one compass setting | done | `bikar/patterns/Constructions/n_ICgwOr6qs.bkr` | PASS 34/0 | PASS 1.0/1.0 | none by design: no solid to compare (see notes) | `src/Coasters/n_ICgwOr6qs-minimal-coaster-standard.stl` | CS-18 | — |

After the 88q Oracle-notes paragraph (ends "O3 is `—`: there is no `.ggb` export.", about line 217), add a blank line and:
    `n_ICgwOr6qs` was scored at its import on 2026-11-03, on youtube main (1f1ec57, the ledger's pin; the source last changed at 224a346, and the `coaster-n_I` branch is that same tree), with no source rewrite but with the D-080 coordinate bootstrap: the four `CircularArc` have no coordinates in the command file, so the AST was built once with `--lenient CircularArc --emit-coords`, the seventeen point coordinates written back in with `--cached-coords`, and the import run again, which then lowered every statement (Rotate 18, Intersect 8, CircularArc 4, Circle 3, point 3, Segment 3, Line 2, Sequence 1, Translate 1, Vector 1; nothing refused or dropped). O1 `PASS: 34 compared, 0 failed, 58 skipped/extra` — the skips are the `Sequence` orbits (`radials`, `f2`..`f5`, `b2`..`b5`), which are the naqsh pattern layer, and `u180`, which the lowering tracks and never makes an object; the extras are the conjugates the lowering introduces (`i0_f2` and the like). O2 `O2 PASS: edge-SSIM 0.9818 (min 0.7), recall 1.0 precision 1.0 (min 0.98), phash 14 (advisory)` on a hero rebuilt with the loop's own export (the same timestamp as the source's last commit). O3 is `none by design`: `make reference` writes `polygons = 0`, because a construction drawn only in arcs has no polygon to extrude, so there is no solid to compare — the same reason as `nmEjCTzMbDg`.

Also, on the same visit, the gBV_JTt3Kxk row (line 137): its O1 cell `FAIL 134/20` was re-run today against bikar/patterns/Constructions/gBV_JTt3Kxk.bkr and reads `PASS: 144 compared, 0 failed, 47 skipped/extra`; the row and its Oracle-notes paragraph are the intake session's to update, not blossom's.

## docs/catalog — one command, after the merge
    git -C ~/Workspace/git/bikar fetch origin    # the tool reads origin/main; a stale ref regenerates the old note
    python3 .claude/skills/pattern-catalog/scripts/catalog.py sync
writes docs/catalog/patterns/a-ten-petal-blossom-from-one-compass-setting.md (top half) and
docs/catalog/media/n_ICgwOr6qs/n_ICgwOr6qs-minimal.png (the Coaster Lab thumbnail). Then hand-write
below the marker, modelled on the 88q note:

```markdown
    ## Pictures
    ### minimal
    ![minimal](../media/n_ICgwOr6qs/n_ICgwOr6qs-minimal.png)

    ## Notes
    Every line is an arc of one compass setting: five petals in front (fa1, fa2) and five behind
    (ba1, ba2), each pair turned five-fold. No straight line is drawn, so the coaster's straps are
    the arcs' chords (sagitta a quarter of the grid pitch) — the first arc-only coaster. The 40 mm
    mini keeps every window open (22,980 triangles, 2.8 cm³); the standard is 62,372 / 7.3 cm³.
```

## .claude/skills/prototype/catalog.md — CS-18 block, after CS-17

```markdown
## CS-18 — Ten-petal blossom, minimal (Samira Mian, n_ICgwOr6qs)

- **Status**: planned
- **Model**: `bikar/patterns/Constructions/n_ICgwOr6qs-minimal-coaster.bkr` —
  rendered as `--coaster Coaster` at `--param size=40` (mini) and `--param
  size=90` (standard) by `make coasters` (→
  `src/Coasters/n_ICgwOr6qs-minimal-coaster-mini.stl` and `-standard.stl`).
  The **minimal** style like CS-13. The art is the Sheikh Zayed Grand Mosque fivefold
  blossom: five petals in front and five behind, every line an arc of one compass
  setting (`connect arc … on <host circle>`), the two front arcs and the two back arcs
  each turned five-fold. The compass circles, the radials and the rays only locate the
  points, so the coaster leaves them out. Arcs only, no straight line — the first
  coaster whose straps are all chords of arcs. Knobs `--param strap=3` (1.6..5) and
  `--param round=1` (0..1.5) as CS-4; `unit` is `(size − strap)/3.6542`. Both sizes pass
  the mesh gate at the 1.6 mm free-standing floor (watertight, 0 degenerate) and the
  linkage gate (1 body): the mini is 22,980 triangles / 2.8 cm³ and the standard
  62,372 / 7.3 cm³ (euler −30 at both). Migrated with bikar PR #368.
- **Print target**: TBD — record machine/material/nozzle/layer on first print.
- **What we want to learn**:
  - [ ] 1. Do the ten petal tips, where two arcs meet at a shallow angle, print clean at 90 mm with 3 mm straps, or do they need a weld (`--param weld`)?
  - [ ] 2. At 40 mm, does a strap built from arc chords read as a curve or as facets?
- **What we learned**: — pending.
- **Feeds**: the gallery's coaster entry; the constructions ledger's `coaster` and
  `catalog` cells for `n_ICgwOr6qs`.
```

## .claude/gates/doc-pointer-baseline.json — entry after the 88q one
    {
      "doc": ".claude/skills/prototype/catalog.md",
      "path": "src/Coasters/n_ICgwOr6qs-minimal-coaster-mini.stl",
      "why": "Gitignored build output — same as the coaster minis above. .gitignore:57 excludes src/Coasters/*-mini.stl; `make coasters` renders it, only `-standard.stl` is vendored. Samira Mian's ten-petal blossom, minimal style (CS-18); introduced with bikar PR #368."
    }

## index.html + docs/site-graph.json — the gallery card

Already landed in #872 (commit 738948c0): the card after the 88q card, the site-graph anchors
moved, the use-case map's UC23 pin repaired. Nothing left here.

## Gates to run by path before the commit
    python3 .claude/gates/constructions_ledger.py
    python3 .claude/gates/counts_gate.py
    python3 .claude/skills/pattern-catalog/scripts/catalog.py sync --check
    python3 .claude/gates/site_graph.py
    python3 .claude/gates/doc_pointers.py
