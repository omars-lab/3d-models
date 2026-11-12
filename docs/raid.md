# Waiting on a person (RAID log)

One row per decision, action, risk, assumption or issue. A row is an index: `where` points at
the backlog line, page thread, PR or plan section that holds the detail. Edit it with
`raid.py` (task-management-manager, raid-log skill) or by hand; `raid.py check` keeps the shape.
Open rows waiting on Omar are counted on the status line.

| id | kind | status | who | asked | times | question | recommend | where | until | outcome |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | decision | decided | omar | 2026-11-12 | 1 | May a session deploy the gallery (make deploy) without asking each time? | Yes, standing | .claude/plans/monitor-print-watcher.md (rules) |  | 2026-11-12: Standing yes: deploy the gallery as needed; why: Omar, 2026-11-12: "deploy gallery as needed ... add a standing okat for deployemnts of gallery to the raid" |
| D2 | decision | open | omar | 2026-11-12 | 1 | The spinner coaster's five choices |  | spinner feedback page (#960); .claude/plans/plates-and-feedback.md section E |  |  |
| D3 | decision | open | omar | 2026-11-12 | 1 | The plate calls that decide what prints next (send cables-1, judge closeout-1 and toys-1, and the rest) |  | .claude/plans/plates-and-feedback.md, Plate decisions waiting on Omar |  |  |
| A1 | assumption | open | omar | 2026-11-12 | 1 | Importing the 16 finished youtube constructions stays parked until Omar asks (split coasters first, 2026-10-06) |  | docs/tasks/catalog-expansion/backlog.md |  |  |
| D4 | decision | decided | omar | 2026-11-12 | 1 | Move the Print Hub's pages into bikar's one app now (slices 2 to 5), without waiting for the plates session's ok? | Yes, keep the old judging link until a moved page is proven | docs/design/process/users-and-surfaces-design.md Appendix B; .claude/plans/monitor-print-watcher.md item 15 |  | 2026-11-12: Start slices 2 to 5 now; the old judging link at 127.0.0.1:8768 keeps working until a moved page is proven on a real plate; answers still save through after_print.py answer and the answers/ PR; why: Omar, 2026-11-12, picked 'Start slices 2 to 5 now' in the question box |
| D5 | decision | open | omar | 2026-11-12 | 1 | Call 2: should the Yes button in the app need Touch ID? |  | docs/design/process/users-and-surfaces-design.md section 12, call 2 (gates slice 4) |  |  |
| D6 | decision | open | omar | 2026-11-12 | 1 | Call 4: who merges a yes made with the button, and one at a time or in a batch? |  | docs/design/process/users-and-surfaces-design.md section 12, call 4 (gates slice 4) |  |  |
| D7 | decision | open | omar | 2026-11-12 | 1 | Call 7: read back the 2026-10-06 calls page before design questions move into the app |  | docs/design/process/users-and-surfaces-design.md section 12, call 7 (gates slice 5) |  |  |
