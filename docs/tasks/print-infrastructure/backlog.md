# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **Piece colors phase 2: the cost table in `plates by-color`, a plate-by-plate view.**
   For each way of printing a colored coaster (one plate per color, mixed plates, AMS swaps),
   show each plate with its colors, then the net cost, the time, and the average time per
   coaster, from the slice where one exists and an estimate where not (slicer minutes plus 1.6
   minutes per color swap, from phones-01). Omar on call 1 of the
   [2026-10-05 page](../../working-model/feedback-requests/2026-10-05-open-calls.md#^qe93p4):
   "Can there be printing options where we visulzie each of the plates and their colors and the
   net cost and time and average time per coaster?" Session task board #183.
2. **A filament catalog with prices, and a command to refresh it.** The color catalog
   (`.claude/skills/color-themes/scripts/catalog.py`) already lists every Bambu color with its
   code, line, name, hex and finish, but no prices. Add the store price per spool and a refresh
   command that fetches the latest, kept open to other brands later (D-105). Every cost above
   reads its grams-to-dollars from here. Omar on the orders section of the 2026-10-05 page: "can
   we have a cli to fetch latest price - do we have a catalog of all the bambu filaments,
   colors, price, etc and a cli to referesh it".
3. **Orders phase 2: the shelf — spools, what an order holds, the buy list, closing a print.**
   Phase 2 of [the order-driven Lab design](../../design/coaster/order-driven-lab-design.md#11-the-build-in-order-of-value-for-the-work):
   `bambu order plan` (phase 1) now gives an order's plates, minutes and grams, but not what is
   short on the shelf. Phase 2 adds the spools on hand, holds grams for an open order, writes the
   buy list, and takes a print's grams off the shelf when it is closed; fixtures 04 and 05 wait
   for it in `make validate-orders` (raise `SHIPPED_PHASE` when it lands). Phases 3–4 (the price,
   the hub pages) follow; pricing writes its formula with named settings, looked-up ones
   referenced to the [consolidated pricing research](../../research/2026-10-04-coaster-pricing.md), and
   waits on all twelve settings: four looked up to confirm, five from Omar's own records and three
   his to choose. Session task board, 2026-10-04. Order files live in an iCloud folder, never in
   this repo (D-101, 2026-10-05), so phase 2 reads them from a path set outside the repo.
4. **Pricing, tried before it is set: simulated buyers, costs by quantity, a charted view.**
   Phase 3 of the order-driven Lab, reshaped by D-104 (2026-10-05). Three parts:
   - costs at 1, 5, 10 and 100 coasters, so what one piece costs us is set beside a batch;
   - simulated buyers (price-conscious and others) who say in their own words why they would
     buy at a price or walk away, and how those thoughts change as the price moves; labeled
     simulated, as review-theme's personas are;
   - a page with charts that shows where the price does best once costs are counted, built so
     real order data can replace the simulated buyers later.
   Omar on calls 13 and 15 of the 2026-10-05 page. Call 13 (the pricing method) is still his.
5. **A plate-packing skill: try layouts, measure the empty bed, keep the best.** Lay a plate's
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

- **Two of the order-driven Lab's three calls**, in
  [order-driven-lab-design.md](../../design/coaster/order-driven-lab-design.md#10-open-calls-for-omar)
  §10: where orders, the shelf and the three pages live (the hub is recommended), and how the
  price is set (cost-plus with a market band is recommended; his comment asks for the quantity
  simulations in item 4 first). Order files in this repo was decided 2026-10-05: never, an
  iCloud folder instead (D-101). Phase 1 does not wait on them. 2026-10-04.
- **How the Lab learns which colors are loaded** (call 4 of the 2026-10-05 page). Omar asked
  "cant it lookup on printer with cli": the CLI already reads the trays
  (`bambu filament --json`), but a page in the browser cannot run it, so the hub would serve the
  list. Waiting on his tick.

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../design/pieces/tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../working-model/backlog.md`](../../working-model/backlog.md) §6.2 on 2026-09-25.
