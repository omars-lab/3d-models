---
plate: pkt-1
---

# pkt-1 — print log

What the printer said while [pkt-1](../pkt-1.md) printed, one row per change, written by the monitor-print skill's `print_monitor.py`. Rows are only ever added at the end: the plates gate refuses a change to a row already on master. A `finished` row is not a print record; that is written when the pieces are judged.

| Time (UTC) | Event | Layer | Done | What the printer said |
|---|---|---|---|---|
| 2026-10-09 00:38 | sent |  |  | fed #f5547c from AMS 0 · slot 0, 11.6 g by the slice |
| 2026-10-09 00:38 | watching | 0/18 | 0% | RUNNING |
| 2026-10-09 00:49 | progress | 1/18 | 25% | 25% |
| 2026-10-09 00:59 | progress | 5/18 | 51% | 50% |
| 2026-10-09 01:09 | progress | 9/18 | 76% | 75% |
| 2026-10-09 01:19 | finished | 18/18 | 100% | FINISH |
