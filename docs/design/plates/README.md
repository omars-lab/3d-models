# Plates

**In short.** A plate is one bed of pieces sent to the printer together. Each plate has a
recipe (`minis-NN.yaml`, which `bambu slice compose` turns into a slice) and, beside it, a page
(`minis-NN.md`) for Omar to review. The page says what the plate is, why to print it, what it
costs, and shows pictures of it. Its frontmatter records its stage and how many times it has
printed, its Approvals table holds every yes Omar gave it, and its timeline lists each step with a
date. What the printer said while a plate printed is in its own file, `print-logs/<plate>.md`
([sheets-04b's](print-logs/sheets-04b.md) is the first), linked from the page's `print_log`
property and only ever added to. The queue below ranks the plates that have not printed yet,
highest return first. The
[prioritize-prints skill](../../../.claude/skills/prioritize-prints/SKILL.md) keeps all of this
current; the [print review design](../printing/print-review-design.md) explains why it
is built this way.

## The queue

<!-- queue:start -->
Written by `python3 .claude/gates/plates_gate.py --write` from the plate pages and the weights in [scoring.md](../../../.claude/skills/prioritize-prints/scoring.md). Do not edit by hand; the prints hook fails when this block and the pages disagree.

| # | Plate | Stage | Value | Hours | ROI | Risk | What it answers |
|---|---|---|---|---|---|---|---|
| 1 | [sheets-01](sheets-01.md) | waiting | 6 | 2.3 | 2.65 | ok | Do the 0.4 mm steps on today's coaster edges show in the hand, and which top (round 1 or the full dome) looks right? |
| 2 | [minis-06](minis-06.md) | waiting | 8 | 3.8 | 2.11 | ok | How thin can the dovetail band go, and does the new slot fix minis-04's tight pegs? |
| 3 | [minis-05](minis-05.md) | waiting | 10 | 5.8 | 1.72 | watch | Which thin join holds a pair together best, the butterfly key or the built-in tab? |
| 4 | [sheets-04c](sheets-04c.md) | waiting | 0 | 0.8 | 0.00 | ok | A second gBV minimal coaster, the minimal construction from sheets-04, on its own: no new question, the same coaster again. |

**Waiting on a build** (no recipe or slice yet, so no hours; highest value first): [sheets-05](sheets-05.md) (value 5), [sheets-02](sheets-02.md) (value 3), [sheets-03](sheets-03.md) (value 3).

**Held for hardware risk:** none.

**Went to the printer, no record yet:** [minis-01](minis-01.md), [minis-02](minis-02.md), [sheets-04b](sheets-04b.md).

**Printed:** [minis-03](minis-03.md) ×1, [minis-04](minis-04.md) ×1, [sheets-04](sheets-04.md) ×1.
<!-- queue:end -->

## How a plate moves

| Stage | Means | Who moves it |
|---|---|---|
| `planned` | Designed, but it waits on a build before it can have a recipe or a slice; `needs:` lists what | whoever wrote the design |
| `proposed` | The recipe exists; nobody has reviewed the page yet | whoever wrote the recipe |
| `waiting` | Pictures and costs are on the page; waiting for Omar's tick | the skill, once the page is complete |
| `approved` | Omar ticked Approve, or said yes in chat, and it is a row in the Approvals table | `.claude/skills/manage-approvals/scripts/plate_approve.py`, reading the tick or his words back |
| `sent` | It went to the printer; no record yet | `bambu print send`, which spends the approval |
| `printed` | A record exists in [`docs/prints/`](../../prints.md) | the record; `times_printed` counts them |
| `retired` | Not printing it again | Omar |

Only Omar approves ([D-093](../../working-model/decisions-log.md)): he ticks the box, or says yes in
chat. Either way `python3 .claude/skills/manage-approvals/scripts/plate_approve.py <page> --approved --by "<who, and how>"` writes it
as a row in the page's `## Approvals` table and unticks the box, so the next tick is a new answer
([D-096](../../working-model/decisions-log.md)):

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|
| 2026-10-04 | approved | Omar, tick on this page | iteration 2 @ 1a2b3c4d5e | sent 2026-10-04 |

`Decision` is `approved`, `held` or `standing`; `Covers` is the recipe iteration the yes was given
on and the master commit that holds it; and `Spent by` is empty while the yes is open, then
`sent <date>`, `replaced <date>` or `reset <date>`. One approval covers one send:
`bambu print send` refuses a plate with no open row, and a send fills its `Spent by` and adds a dated `sent`
row to the timeline. The plates gate (P2) checks the table against the stage and the timeline.

**A recipe change resets the yes** ([D-097](../../working-model/decisions-log.md)). The recipe is
edited in place, and each version that differs from the last is the next iteration, kept in the
manage-approvals skill's `approvals.yaml` and named on the page as `iteration: N`. After an edit,
`python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --iterate` records it and
marks an open yes `reset <date>`; the commit hook (P9) refuses the edit until it is recorded. A
comment-only edit is not a change, so a reprint as-is keeps its iteration and its yes. A change to
a bikar file the recipe names is not caught: only the recipe file is hashed.

A plate that printed can print again, but only on a new approval, so the table keeps every approved reprint. A production plate is the exception: it has a standing approval, a `standing` row written on promotion, while its prints still show production and its recipe is the one it was promoted on ([D-095](../../working-model/decisions-log.md)). Its recipe
is frozen: a change goes on a new experiment plate with `derived_from` (grade-plate skill). Each run is its own record, and
`times_printed` is the number of records.

## How proven a plate is

Each page also says how far its prints have taken it, as `maturity`: an `experiment` (the start
for every plate: a question is still open), `repeatable` (every piece on it has printed well,
twice, on any plate), or `production` (repeatable, printed clean as laid out, and packed: as
much of the bed covered as the [rubric](../../../.claude/skills/grade-plate/rubric.md) asks). Experiments are laid out to answer a question and are not asked to
be packed; production plates must be. The prints set the level, not a feeling: the plates gate
fails a page that claims more than its records show. The
[grade-plate skill](../../../.claude/skills/grade-plate/SKILL.md) grades a plate and writes the
level; the [plate maturity design](../printing/plate-maturity-design.md) explains the
rules. Every plate is an experiment today.

## What we can print

- **Coaster sample plates** like the ones here come from the
  [print-coaster-samples skill](../../../.claude/skills/print-coaster-samples/SKILL.md), which
  keeps mating styles in pairs and has every piece looked at before it goes on.
- **Coupons and prototypes** (fit ladders, clips, test pieces) are in the
  [prototype catalog](../../../.claude/skills/prototype/catalog.md).
- **The calibration plates** — the machine card, the LEGO ladder, the wall joint, the first orb —
  are planned in the [print register](../../tasks/coaster-pipeline/backlog.md) §2. They have no
  recipe or page here yet, so they are not in the queue.

## The pages

Where each one stands is in [the queue](#the-queue), which is worked out from the pages; this
list only says what each plate is, so it cannot fall behind.

- [minis-01](minis-01.md) — the first coaster plate
- [minis-02](minis-02.md) — one mini of each style
- [minis-03](minis-03.md) — minimal-frames at 40 mm
- [minis-04](minis-04.md) — the same at 80 mm and half the height
- [minis-05](minis-05.md) — the thin joins
- [minis-06](minis-06.md) — the two dovetails
- [sheets-01](sheets-01.md) — sampler sheet: edge and top
- [sheets-02](sheets-02.md) — sampler sheet: star points
- [sheets-03](sheets-03.md) — sampler sheet: soft weld
- [sheets-04](sheets-04.md) — sampler sheet: the gBV fit
- [sheets-04b](sheets-04b.md) — the gBV fit again: pieces only, tall and flat, into a press fit
- [sheets-04c](sheets-04c.md) — the gBV minimal coaster alone, sheets-04's minimal construction
- [sheets-05](sheets-05.md) — sampler sheet: fill height

The five sampler sheets are designed in the
[sampler sheets design](../coaster/sampler-sheets-design.md).
