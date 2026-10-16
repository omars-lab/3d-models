---
plate: split-02
---

# split-02 — print log

What the printer said while [split-02](../split-02.md) printed, one row per change, written by the monitor-print skill's `print_monitor.py`. Rows are only ever added at the end: the plates gate refuses a change to a row already on master. A `finished` row is not a print record; that is written when the pieces are judged.

| Time (UTC) | Event | Layer | Done | What the printer said |
|---|---|---|---|---|
| 2026-10-15 20:24 | sent |  |  | fed #f5547c from AMS 0 · slot 0, 31.77 g by the slice |
| 2026-10-15 20:24 | watching | 0/22 | 0% | RUNNING |
| 2026-10-15 20:56 | progress | 2/22 | 25% | 25% |
| 2026-10-15 21:27 | progress | 5/22 | 50% | 50% |
| 2026-10-15 22:03 | lost |  |  | no reply for 10 min |
| 2026-10-15 23:49 | finished | 22/22 | 100% | FINISH, found when the watch picked up again |
