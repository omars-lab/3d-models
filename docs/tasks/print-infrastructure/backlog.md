# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **First full run, stopping short of the send.** Take
   [minis-01](../../plates/minis-01.yaml) through compose, slice, preflight and filament-sync
   exactly as the docs say, and write each friction found here as its own item. This list
   stays short until that run has been done.
2. **A second manifest that mixes what minis-01 doesn't** — sizes, a bordered coaster, a
   multi-colour one — to find the frictions a single-kind plate hides.

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../backlog.md`](../../backlog.md) §6.2 on 2026-09-25.
