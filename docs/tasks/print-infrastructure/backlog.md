# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **See the plate without unzipping it.** `slice compose` slices the plate and Bambu Studio
   draws a picture of it, but the picture stays inside the 3MF (as plate_1.png in its Metadata folder), and
   compose never says where. You have to unzip the file to look before sending. Compose
   should write the picture next to the 3MF and print its path. Found by the minis-01 run,
   2026-09-26.
2. **Finish the minis-01 run at filament-sync.** Compose, slice and `validate sliced` ran
   clean on 2026-09-26 (4 pieces, 1 h 7 m, about 20 g). filament-sync stopped at
   "Not configured": this machine has no printer config (host, serial and token). Setting it
   is Omar's; after that, run `bambu filament-sync --plate build/plates/minis-01.plate.3mf` and
   log what it shows.
3. **A second manifest that mixes what minis-01 doesn't** — sizes, a bordered coaster, a
   multi-colour one — to find the frictions a single-kind plate hides.

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../backlog.md`](../../backlog.md) §6.2 on 2026-09-25.
