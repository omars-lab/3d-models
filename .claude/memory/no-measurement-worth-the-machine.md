---
name: no-measurement-worth-the-machine
description: "Print-campaign safety tenet — never dispatch a coupon/validation that could physically damage the printer, no matter what bet it settles"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9aae5724-5284-48f1-85cb-3c0496a1c2e1
  modified: 2026-09-18T03:29:04.947Z
---

Tenet (Omar, 2026-09-18, prepping Plate 1): **no measurement is worth the machine.** A coupon or
validation plate that could *physically damage* the printer is never sliced-for-dispatch or sent,
regardless of what `CAL-*` bet it would settle. The value of any reading is capped by the cost of
the hardware.

**Why:** during Plate 1 prep the MC2Wall04 0.4 mm rung raised BambuStudio's "floating regions"
warning (the expected, whitelisted by-design one). Omar's response was to make the safety line a
standing rule, not a one-off judgement.

**How to apply:** draw the line where FDM does.
- **Cosmetic / geometry failures are NOT damage → fair game, they are the data.** Floating regions,
  a dropped thin wall, a sagging bridge, a curling overhang — several coupons are *built to fail*
  (K10); a refuting/failing rung is a success.
- **Hardware-risk failures cross the line:** a part that detaches and is dragged into a blob the
  nozzle plows through, a toolpath into the bed/gantry, anything that could crash the nozzle or scar
  the plate. Such a coupon is acceptable ONLY with active mitigation — on-device failure/spaghetti
  detection **and** a watched first layer **and** small part mass — else **drop or redesign it**.
- The firmware owns collision/thermal/runout; this tenet owns the geometry we *choose* to send.

Lives in the runbook as **gate 3** ("before you touch the slicer") + a Rules bullet in
[[print-model-skill]]'s sibling `guide-print` SKILL.md (PR to master 2026-09-18). Related:
[[owner-gated-and-on-hold]] (dispatch owner-gated), [[bambu-x2d-bringup]].
