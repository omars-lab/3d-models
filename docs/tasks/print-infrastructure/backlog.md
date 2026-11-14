# Backlog — the print line: config in, reviewed plate out

Loop: [`print-infrastructure.md`](../../../.claude/loop-prompts/print-infrastructure.md).
Done list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal: a new plate goes from a short YAML file to a sliced, previewed plate with filament
mapped to the loaded AMS trays — no hand edits, nothing only in someone's head, a picture to
look at, and a failure that names its cause.

## Open, in ROI order

Order within the list: a check that passes wrongly first, then a step done by hand on every
plate, then anything you can't see before sending, then config ergonomics.

1. **A plate-packing skill: try layouts, measure the empty bed, keep the best.** Lay a plate's
   pieces out several ways, measure each with `python3 tools/plate_grade.py --fill`, and keep
   the fullest that still slices clean. Worth less since D-098 (2026-10-04): the fill bar is 0,
   so packing no longer decides whether a plate is production; it now saves time and filament
   per print, and nothing more. Packing by hand has come up once (sheets-04d, rows), so per
   the [skill precedent](../../design/process/dsl-extension-skill-evaluation.md) a second plate
   that wants packing comes before the skill. Session task board, 2026-10-03.
2. **Bring the live gallery's Lab pages up to date.** The gallery was last deployed on
   2026-11-12 (gh-pages from master 6a0b28e5) with the Lab pages built from bikar 702fab93.
   Four bikar Lab changes have merged since (#375, #379, #380 and #381), the side bar with its
   light and dark switch among them, so public visitors still see the old top bar. Nothing in
   3d-models' own gallery files has changed since. The public build of the side bar leaves out
   the links to pages that run only on Omar's Mac (the side bar's file in bikar's Lab, appbar.ts, under
   "The public gallery"), but look at the built pages at 1280 and 390 px before `make deploy`, since a
   deploy is published. Found 2026-11-13.

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

## Found elsewhere, maybe this loop's

- `layout report` production metrics for the tile wall (W3): plates at the declared bed size,
  spool count, calendar estimate —
  [`tile-wall-design.md`](../../design/pieces/tile-wall-design.md) §7.1. Not coaster work; take it only if a
  plate-count report for coasters needs the same code. Moved from
  [`../../working-model/backlog.md`](../../working-model/backlog.md) §6.2 on 2026-09-25.
