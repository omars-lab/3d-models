---
plate: spl-2
---

# spl-2 — print log

What the printer said while [spl-2](../spl-2.md) printed, one row per change, written by the monitor-print skill's `print_monitor.py`. Rows are only ever added at the end: the plates gate refuses a change to a row already on master. A `finished` row is not a print record; that is written when the pieces are judged.

| Time (UTC) | Event | Layer | Done | What the printer said |
|---|---|---|---|---|
| 2026-10-09 17:39 | sent |  |  | fed #f5547c from AMS 0 · slot 0, 13.03 g by the slice |
| 2026-10-09 17:39 | watching | 0/18 | 0% | RUNNING |
| 2026-10-09 17:52 | progress | 1/18 | 25% | 25% |
| 2026-10-09 18:04 | progress | 4/18 | 50% | 50% |
| 2026-10-09 18:16 | progress | 9/18 | 75% | 75% |
| 2026-10-09 18:30 | finished | 18/18 | 100% | FINISH |
