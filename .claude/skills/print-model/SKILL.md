---
name: print-model
description: Plan how to 3D-print a model on the Bambu X2D like a sage master operator — discover the loaded filament, then reason out nozzle (0.2/0.4/0.6/0.8), orientation, supports/infill/brim, and plate arrangement (pack repeats, rotate-to-fit), and compose a reviewable per-print plan + sliced plate + preview up to the owner gate. Use for "how should I print this?", "print this model", "what settings/orientation for X?", "how many fit on the plate?", "why did this print warp/string/fail?". NOT the day-to-day CLI (that is the bambu skill) and NOT first-time setup (setup-bambu-x2d). It advises, never auto-changes a setting, and never dispatches — the physical send stays Omar's `bambu print send`.
---

# print-model — a sage master 3D-printer operator

You ask it to print a model and it makes sure you are not getting in your own way. It discovers the
loaded filament, reasons out nozzle / orientation / supports / infill / plate arrangement the way an
expert would, composes a per-print plan that says **what a master would do and why**, and hands you a
sliced plate + preview at the owner gate. It **advises**; it never silently changes a setting, and it
**never dispatches**.

Full rationale, the two lifecycle axes, and every grounded number with its hedge live in the
print-model design doc (docs/print-model-design.md, merged in PR #191). This file is the run-time
front door; the decision detail is in [`rubric.md`](rubric.md), read at run time so it can sharpen
without editing this body.

## The boundary — own the judgement, consume the verbs

The one design risk is re-implementing a slicer, a transport, or the record schema instead of
orchestrating the ones that already exist. So:

- **Owns (new):** the reasoning that turns "print this" into a defensible per-print plan — filament
  match, nozzle, orientation, supports/infill/brim, grid arrangement of repeats, proactive advisories.
  This is the judgement a CLI verb cannot carry.
- **Presents:** the plan artifact + the plate preview PNG pulled from the sliced `.3mf` (its
  Metadata/plate_1.png archive member), the same asset the bambu skill already extracts.
- **Consumes (read-only, owned elsewhere):** transport + slicing + records via the
  [`bambu` skill / CLI](../bambu/SKILL.md) (`status`, `filament`, `slice plate`, `print list`,
  `print send`, `validate record`); geometry via bikar; the record schema via
  [`prints-tab-design.md`](../../../docs/prints-tab-design.md) and
  [`prints_gate.py`](../../../.claude/gates/prints_gate.py); the calibration bench-sheet truth via
  [`prototype`](../prototype/SKILL.md).
- **Refuses:** dispatch. The skill stops at the owner gate — it produces the plate and the plan; it
  does not upload or start a print, and never passes `--yes` on the operator's behalf. Why dispatch is
  materially harder (FTPS + RSA-signed control commands) is the design doc §9.

## How one run flows

Read-only device discovery and local reasoning throughout; the only hardware write is downstream of
the gate and outside this skill. Work the decisions in this order, consulting [`rubric.md`](rubric.md)
for each — it holds the questions to answer, the inputs to read, the grounded heuristic, and the
advisory shape per decision.

1. **Read the model** — bounds, minimum feature, repeated pieces.
2. **Discover filament** — `bambu filament` lists the loaded AMS trays + external spool (read-only).
3. **Pick filament** — one clear match is chosen and *stated*; only when several are plausible does it
   **AskUserQuestion** (bias to action; reserve the question for the pivotal call).
4. **Decide nozzle** (0.2/0.4/0.6/0.8) → **orientation** → **supports/infill/brim** → **arrangement**
   (pack repeats, rotate-to-fit) — each a one-line "what a master would do + why", never a silent change.
5. **Proactive advisories** — leftover bed → more copies / another piece / scale up; footgun catches
   (wall thinner than the nozzle's single-wall floor, needless supports, fragile layer direction, wrong
   filament). Each is a line in the plan; the operator decides.
6. **Compose the plan** — every choice + its one-line why.
7. **Slice** — `bambu slice plate` → `.3mf` + preview PNG.
8. **Hand off at the owner gate** — plan + plate + preview. **STOP.** Dispatch is Omar's `print send`.

## The calibration exception (never forget it)

For any plate that carries a `settles: CAL-…` reading — a calibration coupon — the skill gives **no
advice**. Coupon settings are *measurements fixed by the bench sheet*, not preferences
([`calibrate`](../calibrate/SKILL.md) / [`prototype`](../prototype/SKILL.md)). Steps 4–5 short-circuit:
print the fixed profile from the sheet. Stated everywhere it could be forgotten.

## Best practices + self-healing

[`best-practices.md`](best-practices.md) (read at run time) holds the grounded rules **plus our own
real examples** as we practice them. It is self-healing: a defect found on a real plate graduates into
a best-practices example that fails-before / passes-after the next plan — the repo's graduation rule
([`CLAUDE.md`](../../../CLAUDE.md)) applied to printing.

## Status of the build

The design (PR #191) is complete; this skill is being built out task by task:

- **Done:** filament discovery (`bambu filament`, task #32); the filament-selection procedure —
  match, state-or-ask, the AskUserQuestion shape, the low-remaining footgun ([`rubric.md`](rubric.md)
  §Filament, task #35); the orientation reasoning — candidate bases, support-burden scoring, the
  Tweaker-3-or-fall-back path, and the K1 strength advisory ([`rubric.md`](rubric.md) §Orientation,
  task #33).
- **This scaffold (#31):** the skill dir, this front door, the rubric checklist, the seeded
  best-practices file.
- **Deepened by later tasks:** settings reasoning (#34), the
  per-print plan artifact + owner-gate handoff (#36),
  print-issue recovery (#37), arrangement/rotate-to-fit (#42), nozzle recommendation (#43), proactive
  advisories (#44), the best-practices reference (#45), and self-healing graduation (#46). Each fleshes
  out its row in [`rubric.md`](rubric.md) or its section in [`best-practices.md`](best-practices.md)
  rather than changing this body.
