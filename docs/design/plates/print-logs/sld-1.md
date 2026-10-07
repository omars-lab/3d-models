---
plate: sld-1
---

# sld-1 — print log

What the printer said while [sld-1](../sld-1.md) printed, one row per change, written by the monitor-print skill's `print_monitor.py`. Rows are only ever added at the end: the plates gate refuses a change to a row already on master. A `finished` row is not a print record; that is written when the pieces are judged.

| Time (UTC) | Event | Layer | Done | What the printer said |
|---|---|---|---|---|
| 2026-10-07 18:31 | sent |  |  | fed #f5547c from AMS 0 · slot 0, 2.39 g by the slice |
| 2026-10-07 18:31 | watching | 0/12 | 0% | RUNNING |
| 2026-10-07 18:32 | paused | 0/12 | 0% | 0500-806E (not looked up yet) |
| 2026-10-07 18:49 | error | 0/12 | 0% | 0500-8062 (not looked up yet) |
| 2026-10-07 18:50 | resumed | 0/12 | 0% | RUNNING |
| 2026-10-07 18:55 | progress | 1/12 | 44% | 25% |
| 2026-10-07 18:56 | progress | 1/12 | 52% | 50% |
| 2026-10-07 19:00 | progress | 7/12 | 78% | 75% |
| 2026-10-07 19:03 | finished | 12/12 | 100% | FINISH |
