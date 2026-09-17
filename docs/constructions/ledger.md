# Constructions ledger

One row per GeoGebra construction on its way from a youtube reconstruction to a
naqsh (`.bkr`) file bikar renders to a printable coaster this repo vendors. The
umbrella design is geogebra-construction-import-design.md and the three oracles
O1/O2/O3 are construction-equivalence.md (both on PR #187, not yet on master —
so they are named here in prose, not linked, until they land). This file is the
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
**0 <!--count:constructions-migrated--> migrated** so far: a row counts as
migrated once its naqsh cell names a real `.bkr`. `GimTvN9hw4U`'s lowering has
been measured against all three oracles (equivalence doc, 2026-09-17) but its
`.bkr` lives on bikar branch `feat/naqsh-import` and is not merged, so its
naqsh cell — like every other — is still `—`.

## Columns

- **naqsh** — the bikar source of record, `patterns/Constructions/<id>.bkr`
  written as `bikar/patterns/Constructions/<id>.bkr`; `—` until it is merged.
  The gate FAILS a row that names a `.bkr` bikar cannot resolve.
- **O1 / O2 / O3** — the three equivalence oracles: per-label geometry, drawing
  recall/precision, and solid coverage. `—` until the naqsh file exists to run
  them against.
- **coaster** — the vendored mesh, `src/Coasters/<id>.stl`; `—` until printed
  art exists. The gate FAILS a row that names an `.stl` not on disk here.
- **catalog** — the prototype-catalog id, once the coaster is catalogued.
- **printed** — the print record under `docs/prints/`, once a plate ships.
- **no piece by design** — the sentinel for a mechanism-only video with no final
  art (`M60LJNNslHU`): a complete row that asserts no `.bkr` and no coaster and
  so is neither "migrated" nor "not yet migrated".

## Ledger

| id | title | youtube | naqsh | O1 | O2 | O3 | coaster | catalog | printed |
|---|---|---|---|---|---|---|---|---|---|
| `7apC5Q9QS-8` | Geogebra for Beginners — 8-Fold Rosette Walkthrough (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `GimTvN9hw4U` | Simple 20-step Six-Fold Star Rosette (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `M60LJNNslHU` | Dual Slider m,n-fold Division of the Circle (Sarah Brewer) | done | no piece by design | — | — | — | no piece by design | — | — |
| `lEfWSogWscs` | Pattern from the Tomb of Itimad ad-Daula (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `n3IidKfXE1I` | Variable-angled 12-6-4 Star Rosette (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `nmEjCTzMbDg` | n-fold Flower in GeoGebra Classic 5 (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `rDuxHF3xMOc` | 8-fold Star Rosette with Sequences (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `sDO9fpu76v8` | Pattern from the Royal Alcazar (Sarah Brewer) | done | — | — | — | — | — | — | — |
| `tA8eSdVx_EQ` | 5-minute 7-fold Star Rosette (Sarah Brewer) | done | — | — | — | — | — | — | — |
