---
name: x2d-does-its-own-failure-detection
description: "Omar 2026-10-02 — never ask them to turn on failure detection or watch the first layer; the Bambu X2D does both itself, so neither is a per-plate yes/no, a checklist line, or a print blocker"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-02T20:26:07.684Z
---

Do not put "failure detection on" or "watch the first layer" to Omar as a question, a tick box, a
pre-send checklist line, or a condition a plate waits on. The Bambu X2D does both itself; neither
is ours to worry about. Recorded as D-092 (3d-models #481 and the follow-up that took the
first-layer watch out of guide-print and minis-05).

Omar, 2026-10-02, on the sheets-04 plate page: "no failure detection, bambu does this" — then
"remember this". When told the answer was being taken to cover the first-layer watch too, they
confirmed: "bambu x2d automatically does this, no need for us to worry about this".

**Why:** loose-pieces §3.7 made small loose pieces wait on their yes to failure detection plus a
watched first layer, and sheets-04 sat approved but blocked on that box. They consider both the
printer's job, so the question only added a blocker.

**How to apply:** a small-piece or "watch" risk plate is not held for this, and guide-print never
asks for a watched first layer. Keep only risks the printer cannot catch (hardware damage, see
[[no-measurement-worth-the-machine]]). A first layer that is itself the measurement (MC-6 adhesion
on bare plate) is still read as data. Related: [[look-before-you-print]], [[owner-gated-and-on-hold]].
