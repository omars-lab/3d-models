---
plate: spl-1
---

# spl-1 — print log

What the printer said while [spl-1](../spl-1.md) printed, one row per change, written by the monitor-print skill's `print_monitor.py`. Rows are only ever added at the end: the plates gate refuses a change to a row already on master. A `finished` row is not a print record; that is written when the pieces are judged.

| Time (UTC) | Event | Layer | Done | What the printer said |
|---|---|---|---|---|
| 2026-10-09 02:23 | sent |  |  | fed #f5547c from AMS 0 · slot 0, 18.72 g by the slice |
| 2026-10-09 02:25 | watching | 0/18 | 0% | RUNNING |
| 2026-10-09 02:39 | progress | 1/18 | 25% | 25% |
| 2026-10-09 02:54 | progress | 5/18 | 50% | 50% |
| 2026-10-09 03:09 | progress | 9/18 | 75% | 75% |
| 2026-10-09 03:26 | finished | 18/18 | 100% | FINISH |
