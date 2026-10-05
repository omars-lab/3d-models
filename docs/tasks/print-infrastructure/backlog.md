# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **`bambu order plan <order.yaml>`: an order in, plates, minutes, grams and a shortfall out.**
   Phase 1 of [the order-driven Lab design](../../design/coaster/order-driven-lab-design.md#11-the-build-in-order-of-value-for-the-work):
   count an order's pieces by color, write one recipe per color through the `plates by-color`
   writer (piece colors phase 1, built together so recipes keep one writer), slice each, and
   correct the minutes by the measured ratio of real to sliced time. Today every one of those
   numbers is worked out by hand for each order. Phases 2–4 (the shelf, the price, the hub
   pages) follow it; pricing writes its formula with named settings, looked-up ones referenced to
   the [consolidated pricing research](../../research/2026-10-04-coaster-pricing.md), and waits on all
   twelve settings: four looked up to confirm, five from Omar's own records and three his to
   choose. Session task board, 2026-10-04.
2. **A plate-packing skill: try layouts, measure the empty bed, keep the best.** Lay a plate's
   pieces out several ways, measure each with `python3 tools/plate_grade.py --fill`, and keep
   the fullest that still slices clean. Worth less since D-098 (2026-10-04): the fill bar is 0,
   so packing no longer decides whether a plate is production; it now saves time and filament
   per print, and nothing more. Packing by hand has come up once (sheets-04d, rows), so per
   the [skill precedent](../../design/process/dsl-extension-skill-evaluation.md) a second plate
   that wants packing comes before the skill. Session task board, 2026-10-03.

## Waiting on Omar

- **Two of the print review's six calls**, in
  [print-review-design.md](../../design/printing/print-review-design.md) §9: one queue for every
  plate (call 1) and the scoring weights (call 4). Call 6 (does a recipe change void a yes) was
  decided 2026-10-03 as D-097. Calls 2, 3 and 5 are tick boxes on the plate pages and sit in the
  [coaster-pipeline backlog](../coaster-pipeline/backlog.md)'s owner-gated list.
- **A send button on the hub's plate queue.** The queue is on the page and read-only (3d-model-hub
  #9). The send still happens by hand with `bambu print send`, which asks before it sends. A send
  button needs its own confirmation step, and it waits for two things: prints resuming (on hold,
  Omar 2026-09-30) and Omar saying how that confirmation should work. Found by hub step 3,
  2026-09-30.

- **The order-driven Lab's three calls**, in
  [order-driven-lab-design.md](../../design/coaster/order-driven-lab-design.md#10-open-calls-for-omar)
  §10: where orders, the shelf and the three pages live (the hub is recommended); how the price
  is set (cost-plus with a market band is recommended); and whether order files may ever sit in
  this public repo (never is recommended). Phase 1 does not wait on them. 2026-10-04.

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../design/pieces/tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../working-model/backlog.md`](../../working-model/backlog.md) §6.2 on 2026-09-25.
