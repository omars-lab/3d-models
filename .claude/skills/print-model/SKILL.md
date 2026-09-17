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

## What this skill resolves — it asks only what you haven't answered

A run settles a fixed set of questions. For any the operator has **not** already given, the skill
uses **AskUserQuestion** to settle it; for any they **have** given, it does not re-ask — but it does
**review and critique** the answer (see the next section), never rubber-stamp it. The questions, in
run order:

1. **What to print** — which model / piece(s), and how many of each.
2. **What filament** — which loaded AMS slot, and is it right for this part? ([`rubric.md`](rubric.md) §Filament)
3. **Which nozzle** — 0.2 / 0.4 / 0.6 / 0.8 mm. (§Nozzle)
4. **How to orient it** — which face goes down. (§Orientation)
5. **Supports / infill / brim** — any, and which. (§Supports/infill/brim)
6. **How to place on the plate** — how many fit, rotate-to-fit, fill the unused bed. (§Arrangement)
7. **What the part is for** — display vs functional / load-bearing / heat-exposed. Not a slice knob of
   its own; it **steers** 2–6 (filament choice, infill, nozzle, the scale-up guard) and is the single
   fact that most changes the answers, so ask it early if the operator hasn't said.

Global bias-to-action still holds: a **single clear answer is stated, not asked** (a lone loaded PLA
against a decor part is not a question). AskUserQuestion is reserved for the genuinely ambiguous fork —
one question at the fork, one option per real choice, the recommended option first with its reason.

## It never blindly accepts input — it reviews and critiques

The print-**master** ethos is not "do what you're told"; it is "keep the operator from getting in
their own way." So an answer the operator **provides** is an input to judge, not a command to obey:

- Say the operator asks to **print a part flat**, but that base needs a support forest a different
  face avoids — the skill **says so** and recommends the better base. It does not silently print flat,
  and it does not silently override to the better face either: it surfaces the trade and the operator
  decides (§Orientation).
- A **filament wrong for a stated functional use** (PLA on a load-bearing or heat-exposed part) is a
  footgun line in the plan, not a quiet proceed (§Filament step 6, §Proactive advisories).
- A request to **scale a dimensioned part** (a LEGO stud at 4.8 mm, an orb at spec, any mating part)
  is **refused as a footgun** — scaling breaks the fit — rather than obeyed (§Proactive advisories step 2).

Every critique is the same one-line *"what a master would do + why"* — an offer, never an auto-change
(the invariant the whole rubric enforces). The **one** place the skill overrides rather than advises is
the calibration exception: a coupon's settings are *measurements fixed by the bench sheet*, not
preferences, and are not up for a taste debate (§The calibration exception).

## It tracks the job as tasks

A print job is a multi-step process with an owner gate at the end, so the skill keeps it **visible and
resumable** by tracking it as tasks (`TaskCreate` / `TaskUpdate`), not by holding the state in its head:

- **One task per print job**, subject = model + plate (e.g. "Print: 12× Star-Orb on one X2D plate"),
  created `in_progress` when the run starts.
- **The lifecycle stages advance on the task** as each is settled: agree **what to print** →
  **filament** → **nozzle / orientation / supports·infill·brim** → **arrangement** → **slice + preview**
  → **owner-gate handoff (STOP)**. A stage flips to done only when its decision is actually made — an
  AskUserQuestion answered, or an answer stated and not contested — so a glance at the task shows exactly
  where the job is parked.
- **The job task stays `in_progress` at the owner gate — never auto-completed.** It closes only when
  Omar dispatches (`bambu print send --record`) or cancels; the skill never marks a print done it did
  not send. A failed or disappointing print re-opens the task through the recovery loop.
- **Resumable:** because the state lives in the task, a run interrupted after filament resumes at
  orientation without re-asking what it already settled — the "asks only what you haven't answered" rule
  reads the task, not just the latest message.

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
the gate and outside this skill. Open the **job task** first (§It tracks the job as tasks), then work
the decisions in this order — **each step advances that task** — consulting [`rubric.md`](rubric.md)
for each: it holds the questions to answer, the inputs to read, the grounded heuristic, and the
advisory shape per decision. Ask each question only if the operator has not already answered it, and
review — never rubber-stamp — the answers they did give (§What this skill resolves, §It never blindly
accepts input).

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
8. **Hand off at the owner gate** — plan + plate + preview, plus an offer to open the sliced plate in
   Bambu Studio for visual approval (`open -b com.bambulab.bambu-studio <plate>.3mf` — read-only, opens a
   file, dispatches nothing). **STOP.** Dispatch is Omar's recorded `print send --record`.

## When a print fails or disappoints (the recovery loop)

A second entry point — "why did this warp / string / fail?" — not the forward run. It is a
**diagnose → revise → re-slice → back to the owner gate** loop that reads against a *named* defect
catalog (Simplify3D's Print Quality Guide + Bambu's wiki) rather than inventing one, maps the symptom
to the documented cause, and emits the fix as a one-line advisory pointing at the decision that owns it
— never a silent change. The seven modeled defects, the symptom→cause→revision table, and the loop steps
are [`rubric.md`](rubric.md) §Recovery loop; the symptom lands in the record's `feedback` block
([`prints-tab-design.md`](../../../docs/prints-tab-design.md) §4.1). A physical, new finding graduates
into [`best-practices.md`](best-practices.md) (self-healing, §8).

## The calibration exception (never forget it)

For any plate that carries a `settles: CAL-…` reading — a calibration coupon — the skill gives **no
advice**. Coupon settings are *measurements fixed by the bench sheet*, not preferences
([`calibrate`](../calibrate/SKILL.md) / [`prototype`](../prototype/SKILL.md)). Steps 4–5 short-circuit:
print the fixed profile from the sheet. Stated everywhere it could be forgotten.

## Best practices + self-healing

[`best-practices.md`](best-practices.md) (read at run time) holds the grounded rules **plus our own
real examples** as we practice them. It is self-healing on **two tracks** ([`rubric.md`](rubric.md)
§Self-healing): a defect found on a real plate *and* an operational/slice-path/tooling finding surfaced
while running the skill (e.g. a profile default that silently sabotages a coupon) both graduate into a
best-practices example that fails-before / passes-after the next run — the repo's graduation rule
([`CLAUDE.md`](../../../CLAUDE.md)) applied to printing. When a fix is a repeatable command sequence,
it does not stay as prose: it becomes a `bambu` CLI flag / `make` target (preferred) or a script in this
dir's `scripts/`, named from the example and from here so the next run reaches for the tool. Neither
track is a `settles: CAL-…` coupon reading — those propagate through the bet registry, never this file.

## Status of the build

The design (PR #191) is complete; this skill is being built out task by task:

- **Done:** filament discovery (`bambu filament`, task #32); the filament-selection procedure —
  match, state-or-ask, the AskUserQuestion shape, the low-remaining footgun ([`rubric.md`](rubric.md)
  §Filament, task #35); the orientation reasoning — candidate bases, support-burden scoring, the
  Tweaker-3-or-fall-back path, and the K1 strength advisory ([`rubric.md`](rubric.md) §Orientation,
  task #33); the settings reasoning — supports (tree, threshold-gated), infill (defer-to-profile), and
  brim/raft (thin-source, attribute-never-assert) ([`rubric.md`](rubric.md) §Supports/infill/brim,
  task #34); the per-print plan artifact + slice/preview + owner-gate handoff — the compose→slice→hand-off
  procedure and the stable plan shape, composed-not-stored-twice, stopping at the gate
  ([`rubric.md`](rubric.md) §Compose → slice → hand off, task #36); the print-issue recovery loop —
  the named-catalog diagnose→revise→re-slice loop, the seven modeled defects, and the `feedback`-block
  symptom seam ([`rubric.md`](rubric.md) §Recovery loop, task #37); the plate-arrangement reasoning —
  count-and-footprint-as-given, rotate-to-fit as an in-plane Z-rotation (not a re-orientation), the
  libnest2d NFP pack at 0/45/90/135° honouring `spacing`, the strict-win rotate advisory, and the
  unverified dual-nozzle bed-zoning caveat ([`rubric.md`](rubric.md) §Arrangement, task #42); the
  nozzle-recommendation procedure — min-feature-first, default-0.4-and-state-it, the 0.2/0.6/0.8
  deviation causes (the ~30–40% speed figure attributed not measured), the layer-height/single-wall
  sanity-check, the thin-wall footgun, and the one-diameter-per-plate K2 caveat
  ([`rubric.md`](rubric.md) §Nozzle, task #43); the proactive-advisory sweep — fill-unused-bed
  (leftover ≥ one more footprint), scale-up guarded to no-fixed-dimension parts, and the four footgun
  catches *collected* from the decisions that own them (not re-derived), each a one-line offer never an
  auto-change, with the calibration short-circuit ([`rubric.md`](rubric.md) §Proactive advisories,
  task #44); the best-practices reference — the grounded rules for every decision organized by run
  order, each carrying a confidence tag (grounded / attributed / wants-CAL / measured) and its design-§
  owner, on top of our real X2D examples, `**Default:**` numbers left to the design doc (DRY)
  ([`best-practices.md`](best-practices.md), task #45); the self-healing graduation — how a physical,
  new practice finding off our machine graduates into [`best-practices.md`](best-practices.md) (flipping
  a confidence tag to `[measured]` or adding an example, fails-before / passes-after, no register), and
  the boundary that keeps it distinct from a CAL-bet settlement ([`rubric.md`](rubric.md) §Self-healing,
  task #46).
- **This scaffold (#31):** the skill dir, this front door, the rubric checklist, the seeded
  best-practices file.
- **Orchestration (#49):** the questions-intro (§What this skill resolves), the input-critique
  principle (§It never blindly accepts input), and the task-tracked, resumable lifecycle (§It tracks
  the job as tasks) — the print-master driver over the reasoning above.

**Option A is complete.** Every decision note in [`rubric.md`](rubric.md), the recovery loop, the
proactive-advisory sweep, and the self-healing graduation are written; the skill reasons a model up to
the owner gate. What remains is downstream and owner-gated: the dispatch port (§9) and the first real
plate (#9), which fills best-practices' `[measured]` tag with our own data.
