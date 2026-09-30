# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **A plate that spills onto a second bed passes every check.** `bambu slice compose`
   put minis-05's eleventh coaster on bed 2, and `bambu validate sliced` reported "objects: 11"
   without mentioning the second bed. A send of bed 1 alone would print a key coaster with no
   partner. `compose` should refuse a spill unless the recipe allows more than one bed, and
   `validate sliced` should print the bed count. Found by the prioritize-prints skill's first
   run, 2026-09-30 ([minis-05's page](../../plates/minis-05.md)).

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../design/pieces/tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../working-model/backlog.md`](../../working-model/backlog.md) §6.2 on 2026-09-25.
