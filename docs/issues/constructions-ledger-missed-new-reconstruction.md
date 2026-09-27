# The constructions ledger missed a new youtube reconstruction

Found 2026-09-27 while migrating `bknVRSMcLj0` (the Imamzadeh Isma'il 12-fold kite tile). It had
been fully reconstructed in youtube since 2026-09-17 (82/82 steps), but it had no row in
[`docs/constructions/ledger.md`](../constructions/ledger.md), and no check had pointed that out.

## Why nothing flagged it

The ledger gate is `.claude/gates/constructions_ledger.py`, run by hook `44-constructions` and
`make validate-constructions`. It did have a "youtube id with no ledger row" check, but three
things together kept it quiet:

1. **It only looked at the pin.** The ledger pins one youtube commit
   (`8c219d2c…`, 2026-09-17), and the gate listed reconstructions at that commit only.
   `bknVRSMcLj0` was committed to youtube later the same day (`3868bb0`, `593183f`), so at the
   pin it did not exist yet. Nothing compared the pin with youtube's `main`, so a pin that falls
   behind hides every newer reconstruction.
2. **Even at the pin, it was only a note.** A missing row was printed as a report with exit 0,
   the same as a reminder. `make validate` stayed green.
3. **The hook rarely runs.** Hook 44 fires only when a commit stages the ledger, a coaster file,
   or the gate itself. A youtube-side change touches none of those.

So a new reconstruction could sit without a row for as long as nobody happened to advance the pin
by hand, and even then it would have been one line among other output.

## Fix

A new blocking rule, **L3**, in the same gate:

- It lists reconstructions at the pin **and** at youtube's default branch (`refs/heads/main`,
  then `master`, then `origin/HEAD`). It reads a ref, not the working tree, so the result does not
  change with whatever branch youtube has checked out. An id at either with no ledger row fails.
- A row whose id is not a reconstruction at the pin fails too. That forces the pin forward when a
  row is added, instead of leaving the row's youtube column dated to a commit that never had it.
- `--session` (the SessionStart hook) now also prints "N youtube reconstructions have no ledger
  row: …" when a row is owed.

Blocking on a missing row is safe because the row can be written before any migration work:
youtube `attempted`/`done`, every other cell `—`. The rule asks for a record, not a finished
migration.

## Test that fails before and passes after

The gate's `--self-test` (run by `make validate-constructions`) now builds a scratch youtube repo
with the same shape as this miss: an old pin with two reconstructions, a later `main` commit that
adds a third, and a checked-out feature branch with a fourth that is not on `main` yet.

- "missing row at the pin FAILS" and "pin lags youtube main, row missing FAILS" (the
  `bknVRSMcLj0` case itself) replace the old case "missing row is reported, not failed", which
  asserted the opposite.
- "row the pin cannot see FAILS" covers a row added without moving the pin.
- "clean ledger blocks nothing" still passes with the feature-branch-only reconstruction present,
  which shows the gate reads `main` and not the working tree.

On the live tree, before the `bknVRSMcLj0` row was added, the new gate printed
`L3 youtube reconstruction bknVRSMcLj0 exists at youtube main but has no ledger row` and exited
1. After the row was added and the pin moved to youtube `main` (`6d359b11…`), it passes.
