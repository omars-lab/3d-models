# Constructions ledger

One row per GeoGebra construction on its way from a youtube reconstruction to a
naqsh (`.bkr`) file bikar renders to a printable coaster this repo vendors. The
umbrella design is the
[GeoGebra construction import design](../geogebra-construction-import-design.md)
and the three oracles O1/O2/O3 are specified in
[construction equivalence](../construction-equivalence.md). This file is the
record; `.claude/gates/constructions_ledger.py` keeps it honest and
`make validate-constructions` runs it over the whole tree.

Youtube pin: `8c219d2c44ec72abf586523266f5e9976f7ef416` (2026-09-17)

The pin is a commit in the youtube repo (branch `main`, no remote). Every
"youtube" verdict below — **attempted** (a `reconstructions/<id>/` directory
with a `construction.ggb-commands` exists at the pin) or **done** (that id is
listed in the pin's docs/tasks/done.md) — is read at that commit and nowhere
else, so the column does not shift when someone checks out a different youtube
branch. The gate re-reads youtube at this pin; when youtube is not checked out
it says so and skips the cross-check rather than passing or failing it.

Scope of the set (K2): **9 <!--count:constructions-total--> constructions**,
one per reconstruction that has a `construction.ggb-commands` at the pin —
`_techniques/` holds shared snippets, not a construction, and is not a row.
**8 <!--count:constructions-migrated--> migrated** so far: a row counts as
migrated once its naqsh cell names a real `.bkr` on bikar's default branch.
`GimTvN9hw4U` landed with bikar PRs #200/#201 (importer + golden, then the
`piece Coaster` trailer), `7apC5Q9QS-8` with bikar PR #202, `tA8eSdVx_EQ`
with bikar PR #223 (its heptagon frame pinned via `--coaster-outline`,
[D-079](../decisions-log.md)), `lEfWSogWscs` with bikar PR #225 (its
octagon frame the least-area default fit, no pin), `rDuxHF3xMOc` with
bikar PR #227 (the importer now lowers a `Reflect`/`Rotate` of a brace-group
**list literal** into a conjugated orbit rather than refusing it), and
`nmEjCTzMbDg` with bikar PR-5 #243 (the first **open line-art** construction —
conic loci and circle inversion drawn as `connect arc … major` straps, resolved
by the B′ `--emit-coords` cached_coords self-bootstrap, [D-080](../decisions-log.md)),
`sDO9fpu76v8` with bikar PR #228 (the first **tessellation** rather than a
rosette — a hexagonal cell reflected into its neighbour and the layer rotated
six-fold, on the set's first hexagonal frame), and `n3IidKfXE1I` with bikar
PR #229 (three rotational orbits about three different centres, the "12-6-4",
with the walkthrough's slider angle pinned at 23.5°).
All eight now vendor a standard (90 mm) coaster mesh under `src/Coasters/` and
carry a prototype-catalog entry (`CS-1`, `CS-2`, `CS-6`, `CS-7`, `CS-8`, `CS-9`,
`CS-10`, `CS-11`) — P3.3 of the umbrella plan, which built on the `coaster`
declaration (P1.6/P2.7).

Oracle cells read `PASS a/b` — O1: labels compared / failed; O2: centreline
recall / precision; O3: reference coverage — or `—` when that oracle has not
been run on the row's `.bkr`. A verdict is only ever the one the equivalence
doc's validator printed, never a re-typed summary: `GimTvN9hw4U`'s three are in
[construction equivalence §2–§4](../construction-equivalence.md) and its
research file; `7apC5Q9QS-8`'s O1 and O2 were run 2026-09-17 on the youtube
`feat/ggb-coords` verdict scripts against a hero rebuilt with the loop's own
export (the earlier `export.png` was a stale 5123×5123 square that O2 scored
recall 0.01; the youtube issue note naqsh-score-stale-hero on that branch has the evidence), and its O3 has
not been run: no `make reference` for it yet.

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
| `7apC5Q9QS-8` | Geogebra for Beginners — 8-Fold Rosette Walkthrough (Sarah Brewer) | done | `bikar/patterns/Constructions/7apC5Q9QS-8.bkr` | PASS 144/0 | PASS 1.000/1.000 | — | `src/Coasters/7apC5Q9QS-8-coaster-standard.stl` | CS-2 | — |
| `GimTvN9hw4U` | Simple 20-step Six-Fold Star Rosette (Sarah Brewer) | done | `bikar/patterns/Constructions/GimTvN9hw4U.bkr` | PASS 23/0 | PASS 1.000/1.000 | PASS 1.000 | `src/Coasters/GimTvN9hw4U-coaster-standard.stl` | CS-1 | — |
| `M60LJNNslHU` | Dual Slider m,n-fold Division of the Circle (Sarah Brewer) | done | no piece by design | — | — | — | no piece by design | — | — |
| `lEfWSogWscs` | Pattern from the Tomb of Itimad ad-Daula (Sarah Brewer) | done | `bikar/patterns/Constructions/lEfWSogWscs.bkr` | — | — | — | `src/Coasters/lEfWSogWscs-coaster-standard.stl` | CS-7 | — |
| `n3IidKfXE1I` | Variable-angled 12-6-4 Star Rosette (Sarah Brewer) | done | `bikar/patterns/Constructions/n3IidKfXE1I.bkr` | — | — | — | `src/Coasters/n3IidKfXE1I-coaster-standard.stl` | CS-10 | — |
| `nmEjCTzMbDg` | n-fold Flower in GeoGebra Classic 5 (Sarah Brewer) | done | `bikar/patterns/Constructions/nmEjCTzMbDg.bkr` | — | — | — | `src/Coasters/nmEjCTzMbDg-coaster-standard.stl` | CS-9 | — |
| `rDuxHF3xMOc` | 8-fold Star Rosette with Sequences (Sarah Brewer) | done | `bikar/patterns/Constructions/rDuxHF3xMOc.bkr` | PASS 41/0 | — | — | `src/Coasters/rDuxHF3xMOc-coaster-standard.stl` | CS-8 | — |
| `sDO9fpu76v8` | Pattern from the Royal Alcazar (Sarah Brewer) | done | `bikar/patterns/Constructions/sDO9fpu76v8.bkr` | — | — | — | `src/Coasters/sDO9fpu76v8-coaster-standard.stl` | CS-11 | — |
| `tA8eSdVx_EQ` | 5-minute 7-fold Star Rosette (Sarah Brewer) | done | `bikar/patterns/Constructions/tA8eSdVx_EQ.bkr` | — | — | — | `src/Coasters/tA8eSdVx_EQ-coaster-standard.stl` | CS-6 | — |
