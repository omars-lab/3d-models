---
name: simulator-learns-each-setup
description: "Omar 2026-10-14 — the first-layer simulator is taught per printer setup (machine, nozzle, plate, filament) from judged prints, by its own reusable teach-simulator skill"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-14T13:50:14.190Z
---

The first-layer simulator should learn our specific machine and setup from printed pieces, photos and Omar's verdicts. The teaching is its own skill, so it can be run again on a new machine. Omar's words: "have a teach the simulator skill we cna use later if we ever change machines" and "i iamgin the simulator is learning our sepcific machine /setup". It came after the plain slicer plan ranked only 4 of 15 judged pairs the way he did (#731).

**Why:** the slicer's plan can't see what the plastic does at line ends or how far a bead spreads, and both depend on the printer, the plate and the filament.

**How to apply:**
- Fitted numbers live in one profile per setup. A setup with no profile falls back to the plain plan, labeled as such.
- Never pool two setups silently. The gold textured plate (bedface-3) is not the glacier plate.
- Agreement is reported on all pairs and on the pairs Omar didn't call the same. The held-out score is the one that counts.
- The simulation skill is separate from the ideas loop and from the teaching skill: three skills in all ([[print-pieces-not-whole-shapes]], [[slicer-plan-is-not-the-print]]).
