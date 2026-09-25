# Loop prompt — GeoGebra constructions to printed coasters

Paste the block below into a fresh session, or run it as `/loop` with no interval so the
session paces itself. Written 2026-09-25, after 3d-models #306.

---

## The goal

**Every GeoGebra construction in the youtube corpus becomes a coaster that has actually been
printed on the X2D, many at a time, through a process that repeats for each new construction.**

That is the umbrella plan, [`iterative-dazzling-finch.md`](../plans/iterative-dazzling-finch.md)
(architecture, decisions, phase map). Its continuation,
[`coaster-border-continuation.md`](../plans/coaster-border-continuation.md), holds the task
detail. The printer side is [`binary-tickling-kay.md`](../plans/binary-tickling-kay.md)
(first-print campaign: nothing has ever been measured, and printing is Omar's call).

Where it stands (verified against `origin/master` and bikar `origin/main` on 2026-09-25):

- **Done: the pipeline, phases 0 to 4.2.** GeoGebra → naqsh (`.bkr`) → STL works. The
  `import-construction` skill repeats it. The
  [ledger](../../docs/constructions/ledger.md) reads 8 migrated, 1 no-piece by design,
  0 remaining. The catalog, gallery and `make coasters` are live. Border, colour regions →
  AMS slots, twist, radial bands and rods relief are all in. `bambu slice compose` builds a
  plate. [`minis-01`](../../docs/plates/minis-01.yaml) is the first mini plate (P4.2).
- **Missing: the print.** Nothing is printed. The CAL-CST bets are unmeasured
  ([`bets.md`](../skills/calibrate/bets.md)). The standard-size plate (P5.2) waits on those
  numbers.
- **The goal is met** when minis-01 has been printed, its record is in
  [`docs/prints/`](../../docs/prints), the CAL-CST bets it covers are settled (P4.3), and
  the standard-size plate (P5.2) is built from the measured numbers.

## Each pass of the loop

1. **Look before acting.** `git fetch` in 3d-models and bikar. Read `origin/master` and
   `origin/main`, never the local refs, which lag. Run `make validate`. If main is red,
   fixing it comes first. Reviewing, merging and cleaning up other PRs, branches and
   worktrees is not this loop's job; that is [`consolidation.md`](consolidation.md).
2. **Pick the top item by ROI** from the backlog,
   [`docs/tasks/coaster-pipeline/backlog.md`](../../docs/tasks/coaster-pipeline/backlog.md).
   That means what moves the goal most, for the least effort and risk. State the ranking in
   one line and do the item. Don't ask which one to take.
3. **Ship it.** One branch per item, off `origin/master` (never off another open PR), in its
   own worktree. Open a PR, merge it, and delete that item's branch and worktree. Nothing more.
4. **Record it,** in the same PR. Move the item from the backlog to the
   [done list](../../docs/tasks/coaster-pipeline/done.md) with the date and PR number. Add
   anything the pass found but didn't do to the backlog, or to another loop's backlog if it is
   that loop's job (see the [README](README.md)). If the approach changed, add a
   `docs/issues/<slug>.md`.
5. **Wait when blocked.** If every remaining item needs Omar, send one short message naming
   exactly what he has to do. Then schedule the next wakeup 20 to 30 minutes out; don't poll.

Omar's calls, never the loop's: sending a print, which filament to load, pushing bikar CI
secrets (`make setup-secrets`), and the FAQ keep/discard review. Name these; don't work
around them.

## Rules that bite here

- Get every new D- or Q- id from `python3 tools/next_id.py next D`, never from last id + 1.
- The shared checkout may be on another session's branch. Do the work in a worktree.
- Nothing outside the goal. If a pass drifts into tooling that doesn't bring the first
  printed coaster closer, stop and go back to the list.
