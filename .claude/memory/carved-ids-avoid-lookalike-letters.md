---
name: carved-ids-avoid-lookalike-letters
description: carved piece ids must not use letters that look alike when cut small — B/D and M/N confused Omar on spl-2 (2026-10-09); O already skipped for zero
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-09T19:57:28.992Z
---

Carved ids (D-109) are read off a 15 mm piece at about 2.5 mm letter height. On spl-2 Omar found
B and D hard to tell apart, and M and N too ("but node b and d are confusing", "m and n oto",
"we shuld remeber this", 2026-10-09). spl-2 already skipped O so it never reads as a zero.

**Why:** a misread id swaps two pieces' answers in the print record. On spl-2, 1B (0.15 mm) and
1D (0.20 mm) were different gaps, so a mix-up moves a fit reading by a whole rung.

**How to apply:** when a plate hands out pair letters or ids, skip B, D, M, N and O (and think
twice about I/1, S/5, Z/2). Two pieces at different rungs must never carry a look-alike pair.
Where letters come from a number (bikar's `pair` 1–26), the fix belongs in the generator, not
in each plate. Related: [[questions-name-carved-ids]], [[after-print-questions-as-sop]].
