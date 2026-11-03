# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **The hub's plates page runs wider than a phone screen.** On a phone it scrolls sideways;
   fix the layout in 3d-model-hub so it fits at phone width, and look at it in a browser at that
   width before calling it done. The fix is in the 3d-model-hub repo; the hub runs locally at
   http://127.0.0.1:4717. Found 2026-10-29, after the "Waiting on you" box landed
   (3d-model-hub #21); still too wide on 2026-11-02.
2. **A plate-packing skill: try layouts, measure the empty bed, keep the best.** Lay a plate's
   pieces out several ways, measure each with `python3 tools/plate_grade.py --fill`, and keep
   the fullest that still slices clean. Worth less since D-098 (2026-10-04): the fill bar is 0,
   so packing no longer decides whether a plate is production; it now saves time and filament
   per print, and nothing more. Packing by hand has come up once (sheets-04d, rows), so per
   the [skill precedent](../../design/process/dsl-extension-skill-evaluation.md) a second plate
   that wants packing comes before the skill. Session task board, 2026-10-03.
3. **Orders phase 4 is the storefront repo's; what stays here is two Decided lines.** The
   hub's Orders tab (Plan, Price with its Scenarios view, Inventory) and the Lab's "Add to
   order" button, the last phase of the
   [order-driven Lab design](../../design/coaster/order-driven-lab-design.md#11-the-build-in-order-of-value-for-the-work)
   §11, are built from the storefront repo, tracked in its open list
   (`~/Workspace/git-naqshcoffee/coffee-house-storefront/docs/tasks/open.md`), by the session that owns every storefront item (handed over 2026-11-03,
   after the end-of-work hook had this session pick it; Omar: it is the store side's). Phases
   1 to 3 already work from the terminal (`bambu order plan`, `bambu shelf show`,
   `bambu order price`). What stays here: when Omar confirms the two calls the design's §10
   still lists open, record them as Decided lines, the pages live in the hub (D-112) and the
   price is cost plus a markup checked against a market band (D-113); the decisions log has
   both since 2026-10-08 but §10 does not. The third, no order files in this repo, is D-101.
   Do not fill in an answer for him.

## Waiting on Omar

- **The bed-face slits: bedface-5's pieces wait to be judged.** bedface-1's preset was no cleaner
  in print than stock, bedface-2's rings moved the slits without closing them, and bedface-3's gold
  plate left fewer slits but the plate is out. [bedface-4](../../design/plates/bedface-4.md) found
  the fill pushed 55% into the wall leaves fewer slits than 30%, and 10% more first-layer plastic
  helps a little, with every piece still slit. [bedface-5](../../design/plates/bedface-5.md)
  printed in green on 2026-10-14: 75% and 100% into the wall, and 55% and 75% with the extra
  plastic. Its "After the print" rows need Omar's hands on the twelve pieces. Also still
  unanswered: bedface-2's rows 2 and 3 (`R` beside `F`, `FC1 1E` in `S` and `R`),
  and from bedface-1: round the carved letters (FC1 vs 4GH), how FC1 1A and 1C felt, and whether
  the kites stay in upside down. Found by the bedface-1 judging, 2026-10-11.
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

- **Hub step 1: run the live printer reading on the hub page.** The read is built; running it is
  Omar's step, listed under "Things only you can do" on the
  [2026-09-29 open-calls page](../../working-model/feedback-requests/2026-09-29-open-calls.md).
  The hub's printer reading is read-only, trays and status with no send (D-111). The tray list
  for the Lab and the print-time color match both reuse this read, so they have nothing to serve
  until it runs. On macOS the background `node` may also need allowing under Local Network
  settings. From the session task board, 2026-11-02.
- **The piece-colors screen's four calls** (#538), in the
  [piece colors design](../../design/coaster/infill-color-ux-design.md#8-open-calls-for-omar) §8:
  which way of printing the screen offers first, a color per group or per piece too, whether a
  plate's color goes in its recipe or only at the send, and how the Lab learns which colors are
  loaded. Phases 1 to 5 are built; the "match the loaded trays" helper waits on call 4, and phase
  5 was built under the recommended pick for call 2. On call 4 (also call 4 of the 2026-10-05
  page), Omar asked "cant it lookup on printer with cli": the CLI already reads the trays
  (`bambu filament --json`), but a page in the browser cannot run it, so the hub would serve the
  list. D-103, D-110 and D-111 touch the same questions as calls 1, 3 and 4, but the design has
  no Decided line for any of the four. Waiting on his ticks.

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../design/pieces/tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../working-model/backlog.md`](../../working-model/backlog.md) §6.2 on 2026-09-25.
