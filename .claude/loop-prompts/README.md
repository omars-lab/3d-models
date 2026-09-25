# Loop prompts

Each file is a self-paced `/loop` prompt for a clean session. There is one job per loop, and
each file names the other loops so no two do the same work. When the state changes, update
the matching file; don't add a new one.

Each loop has its own backlog and done list in `docs/tasks/<loop>/`. The prompt says *how* a
pass runs; the backlog says *what* is next; the done list says what shipped.

| Loop | Job | Runs in | Backlog | Done |
|---|---|---|---|---|
| [`coaster-pipeline.md`](coaster-pipeline.md) | Get the first coaster plate printed, and measure the calibration numbers from it | 3d-models | [backlog](../../docs/tasks/coaster-pipeline/backlog.md) | [done](../../docs/tasks/coaster-pipeline/done.md) |
| [`print-infrastructure.md`](print-infrastructure.md) | Turn a short config file into a reviewed, send-ready plate with one command | 3d-models | [backlog](../../docs/tasks/print-infrastructure/backlog.md) | [done](../../docs/tasks/print-infrastructure/done.md) |
| [`catalog-expansion.md`](catalog-expansion.md) | Find new patterns and turn reconstructions into catalog coasters | 3d-models, bikar, youtube | [backlog](../../docs/tasks/catalog-expansion/backlog.md) | [done](../../docs/tasks/catalog-expansion/done.md) |
| [`video-reconstruction.md`](video-reconstruction.md) | Rebuild one tutorial video as a proved GeoGebra construction | youtube | youtube: `.claude/plans/learning-from-youtube.md` | youtube: `docs/tasks/done.md` |
| [`consolidation.md`](consolidation.md) | Merge PRs, clean up branches, worktrees and stashes, and lose nothing | all six repos | [backlog](../../docs/tasks/consolidation/backlog.md) | [done](../../docs/tasks/consolidation/done.md) |
| — | Open work no loop owns | — | [parked](../../docs/tasks/parked/backlog.md) | — |

Work flows from reconstruction to catalog, then to the print infrastructure, then to the
printed plate. Consolidation runs beside all of them. The video loop keeps its lists in the
youtube repo, where it runs; they are not copied here.

## How a loop uses its backlog and done list

- **Read the backlog first.** Take the top item by ROI.
- **Feed it as you go.** Work a pass finds but does not do goes into the backlog as one line
  that says where it came from. Work that belongs to another loop goes into *that* loop's
  backlog. Work no loop owns goes into [parked](../../docs/tasks/parked/backlog.md).
- **Move finished items to the done list** in the PR that ships them: one line, newest first,
  with the date and the PR number. Delete the line from the backlog rather than marking it
  done there.

## The older records

- [`docs/backlog.md`](../../docs/backlog.md) is the full print-gated register: plates 1 to 5,
  every coupon, and every `CAL-*` bet with what it waits on. It stays where it is, because the
  count checks read it and many docs link into its sections. The first-print backlog points
  into it.
- [`docs/tasks/done.md`](../../docs/tasks/done.md) holds the session task board's snapshots 1
  to 10 and is frozen at 2026-09-25. Task ids cited elsewhere (`#37`, `#84`) resolve there.
  New finished work goes in the per-loop done lists.
