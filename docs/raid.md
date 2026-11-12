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
