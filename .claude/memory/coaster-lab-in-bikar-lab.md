---
name: coaster-lab-in-bikar-lab
description: "Decided 2026-09-17 — a coaster design UI is a Coaster Lab in bikar's lab (Orb Lab pattern), not a page in 3d-model-hub; starts after coaster shape v2 fixes the param set"
metadata: 
  node_type: memory
  type: project
  originSessionId: 82a84811-d601-4caf-aeb6-288a0d47b1e9
  modified: 2026-09-17T19:37:09.729Z
---

On 2026-09-17 Omar asked (comment on the Coaster Shape Study artifact,
https://claude.ai/artifact/22EcRMQzqCvLYcbn6mqHez) whether 3d-model-hub needs its own
coaster builder UI. Recommendation given and confirmed ("coaster lab in bikars lab sounds
good"): a **Coaster Lab** in bikar `packages/lab`, following [[orb-lab-conventions]] (knobs
are DSL params, touched-set overrides, print target never in share URLs). 3d-model-hub stays
the plate builder (Option D) and only lists coaster iterations with their params.

**Why:** a coaster is a `.bkr` with three or four params (size, margin, relief height, rim);
a design form is a thin layer over the same declaration re-rendered through bikar, which is
exactly what the Orb Lab already does. The hub holds the printer secret and should stay about
plates.

**How to apply:** start the lab only after coaster shape v2 (task #33, [[print-model-skill]]
era backlog) defines the knob set; write the decision line in `docs/decisions-log.md` with
the shape v2 PR. Related open idea: interlocking dovetail edges (task #34).
