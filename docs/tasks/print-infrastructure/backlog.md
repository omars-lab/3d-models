# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **Check the printer's certificate on MQTT and FTPS too.** Both skip the check today
   (`rejectUnauthorized: false`), and both carry the access code. The camera now checks against
   a certificate saved once per printer ([camera-tls-pin](../../issues/camera-tls-pin.md)). Fetch
   what ports 8883 and 990 present. If it is the same certificate, use the same pinned options,
   with a test that a different certificate is refused. Found by the camera work, 2026-10-02.
2. **Confirm `md5` and `bed_type` against a Studio send.** The `print send` dry run for
   sheets-04b matched the printer's report of Studio's sheets-04 send on `ams_mapping` (both
   `[3]`), on the project, profile and subtask ids (all `"0"`) and on `print_type` local. The
   report shows neither Studio's `md5` nor its `bed_type`; it gives the plate as
   `cur_id "P0101"`. Read Studio's request itself: try subscribing to `device/<serial>/request`
   while Omar sends from Studio (untested; the printer may not let a client read that topic). Then fix any field that differs before the first CLI send
   ([first-party-dispatch](../../issues/first-party-dispatch.md)). Found 2026-10-02.

## Waiting on Omar

- **Three of the print review's six calls**, in
  [print-review-design.md](../../design/printing/print-review-design.md) §9: one queue for every
  plate (call 1), the scoring weights (call 4), and whether an approval lapses when its recipe
  changes (call 6). Calls 2, 3 and 5 are tick boxes on the plate pages and sit in the
  [coaster-pipeline backlog](../coaster-pipeline/backlog.md)'s owner-gated list.
- **A send button on the hub's plate queue.** The queue is on the page and read-only (3d-model-hub
  #9). The send still happens by hand with `bambu print send`, which asks before it sends. A send
  button needs its own confirmation step, and it waits for two things: prints resuming (on hold,
  Omar 2026-09-30) and Omar saying how that confirmation should work. Found by hub step 3,
  2026-09-30.

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../design/pieces/tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../working-model/backlog.md`](../../working-model/backlog.md) §6.2 on 2026-09-25.
