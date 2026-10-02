# Plates

**In short.** A plate is one bed of pieces sent to the printer together. Each plate has a
recipe (`minis-NN.yaml`, which `bambu slice compose` turns into a slice) and, beside it, a page
(`minis-NN.md`) for Omar to review. The page says what the plate is, why to print it, what it
costs, and shows pictures of it. Its frontmatter records whether Omar approved it and how many
times it has printed, and its timeline lists each step with a date. The queue below ranks the
plates that have not printed yet, highest return first. The
[prioritize-prints skill](../../.claude/skills/prioritize-prints/SKILL.md) keeps all of this
current; the [print review design](../design/printing/print-review-design.md) explains why it
is built this way.

## The queue

<!-- queue:start -->
Written by `python3 .claude/gates/plates_gate.py --write` from the plate pages and the weights in [scoring.md](../../.claude/skills/prioritize-prints/scoring.md). Do not edit by hand; the prints hook fails when this block and the pages disagree.

| # | Plate | Stage | Value | Hours | ROI | Risk | What it answers |
|---|---|---|---|---|---|---|---|
| 1 | [sheets-04](sheets-04.md) | approved | 10 | 1.2 | 8.31 | watch | Which gap per face lets a loose gBV piece drop into its pocket and stay, do the small five-point stars catch at 0.15, and does a 2 mm peak read as the look in the hand? |
| 2 | [sheets-01](sheets-01.md) | waiting | 6 | 2.3 | 2.65 | ok | Do the 0.4 mm steps on today's coaster edges show in the hand, and which top (round 1 or the full dome) looks right? |
| 3 | [minis-06](minis-06.md) | waiting | 8 | 3.8 | 2.11 | ok | How thin can the dovetail band go, and does the new slot fix minis-04's tight pegs? |
| 4 | [minis-05](minis-05.md) | waiting | 10 | 5.8 | 1.72 | watch | Which thin join holds a pair together best, the butterfly key or the built-in tab? |

**Waiting on a build** (no recipe or slice yet, so no hours; highest value first): [sheets-05](sheets-05.md) (value 5), [sheets-02](sheets-02.md) (value 3), [sheets-03](sheets-03.md) (value 3).

**Held for hardware risk:** none.

**Went to the printer, no record yet:** [minis-01](minis-01.md), [minis-02](minis-02.md).

**Printed:** [minis-03](minis-03.md) ×1, [minis-04](minis-04.md) ×1.
<!-- queue:end -->

## How a plate moves

| Stage | Means | Who moves it |
|---|---|---|
| `planned` | Designed, but it waits on a build before it can have a recipe or a slice; `needs:` lists what | whoever wrote the design |
| `proposed` | The recipe exists; nobody has reviewed the page yet | whoever wrote the recipe |
| `waiting` | Pictures and costs are on the page; waiting for Omar's tick | the skill, once the page is complete |
| `approved` | Omar ticked Approve; `approved_on` is the date they ticked it | the skill, reading the tick back |
| `sent` | It went to the printer; no record yet | whoever sent it, after Omar said send |
| `printed` | A record exists in [`docs/prints/`](../prints.md) | the record; `times_printed` counts them |
| `retired` | Not printing it again | Omar |

Only Omar approves and only Omar sends. The skill writes the queue and the pages; it never
ticks a box and never talks to the printer. A plate that printed can print again: each run is
its own record, and `times_printed` is the number of records.

## What we can print

- **Coaster sample plates** like the ones here come from the
  [print-coaster-samples skill](../../.claude/skills/print-coaster-samples/SKILL.md), which
  keeps mating styles in pairs and has every piece looked at before it goes on.
- **Coupons and prototypes** (fit ladders, clips, test pieces) are in the
  [prototype catalog](../../.claude/skills/prototype/catalog.md).
- **The calibration plates** — the machine card, the LEGO ladder, the wall joint, the first orb —
  are planned in the [print register](../tasks/coaster-pipeline/backlog.md) §2. They have no
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
- [sheets-05](sheets-05.md) — sampler sheet: fill height

The five sampler sheets are designed in the
[sampler sheets design](../design/coaster/sampler-sheets-design.md).
