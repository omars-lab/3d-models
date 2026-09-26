---
name: look-before-you-print
description: "Omar rejects prints that pass the gates but don't read well (near-solid discs, half-empty art, bare wedges); fewer good pieces beat full pattern coverage — run the review-print skill before any compose"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-26T04:01:14.963Z
---

Before a piece goes on a plate, look at it top-down at its print size and leave it off if it
doesn't read as a good object — even if that leaves a pattern out. On 2026-09-25 minis-03 put
five minimal-frames on the plate "so every pattern is represented" although my own render showed
two near-solid discs (sDO9, nmEj), one half-filled square (n3Ii) and two with bare wedges
(lEfW, tA8e). Omar rejected all five on sight: "mostly solid disks are not good coasters",
"felt incomplete", "lots of weird empty space".

**Why:** the mesh/linkage gates only say a piece *can* print; a wasted plate costs filament,
machine hours and Omar's trust. Upsizing a dense pattern did not fix it (60/70 mm still solid).

**How to apply:** run the `review-print` skill (3d-models PR #323, `tools/print_review.py sheet`)
for every plate; send Omar the sheet with per-piece verdicts before composing; write leave-offs
into the plate header. Related: [[no-measurement-worth-the-machine]], [[omar-working-preferences]].
