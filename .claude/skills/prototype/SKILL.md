---
name: prototype
description: Plan and log physical orb print prototypes. Use when deciding what to print next, before sending a file to a printer or print service, and after testing a print — the catalog records every prototype we should make, what each iteration must teach us, and what we actually learned.
---

# Prototype catalog workflow

The catalog lives next to this file in `catalog.md`. It is the source of truth
for the physical-prototype backlog — harness tasks (e.g. "print a physical orb
prototype", "decide hemisphere-split export") point here for the detail.

## Entry schema

One `##` section per prototype, ordered by the learning ladder (cheapest
decisive learning first). Each entry has:

- **Status** — `planned` / `printing` / `tested` / `retired` (+ date).
- **Model** — the `.bkr` source and the exact command (or Lab steps) that
  produces the STL. Knob values that differ from defaults must be listed —
  use the Lab's "Write values into code" + Download `.bkr` so the file is
  self-describing.
- **Print target** — machine, material, nozzle, layer height. `TBD` until the
  first real print; record what was actually used, not what was planned.
- **What we want to learn** — a checklist of concrete, answerable questions.
  If a question isn't answerable by looking at or measuring the physical
  object, it doesn't belong here.
- **What we learned** — filled only after a physical print is examined.
  Answer the questions above by number; unexpected findings get their own
  bullets.
- **Iteration log** — one table row per physical print: date, what changed
  from the previous iteration, the question it targeted, result, decision.
- **Feeds** — where a learning propagates when it lands (see below).

## Workflows

**Plan the next print** — read the catalog top to bottom, pick the first
`planned` entry whose open questions are not blocked by an earlier entry's
answers. Prefer the cheapest print that settles the most downstream questions
(that ordering is why the strut coupon precedes any full orb). Before slicing,
restate the entry's questions; if none would be answered by the print, the
print is decoration, not a prototype — say so.

**Log a result** — after the user reports on a print: fill "What we learned"
(numbered answers), append the iteration row, flip Status. Never mark a
question answered from simulation, slicer preview, or reasoning — only from
the physical object. Partial answers stay unchecked with a note.

**Propagate** — a learning is not done until it lands where it changes future
output. Standing targets:

- `bikar patterns/Orbs/*.bkr` — param defaults/ranges (changing a default
  changes golden STLs: re-record goldens and re-run the qiyas sweep, and the
  Lab trust-badge composites in `packages/lab/src/scripts.ts`).
- bikar mesh gate — the FDM min-strut floor (currently 1.2 mm) if the coupon
  disproves it.
- Orb Lab process copy — machine table / weave FDM notice in bikar
  `packages/lab` (then re-run `make lab` here to vendor).
- `docs/orb-lab-design.md` — §5 print guidance, §10 status.
- The harness task list (print-prototype and split-export tasks) and the
  project memory.

Cite the commit hash in the catalog when a propagation lands.

## Rules

- Date every iteration row.
- Record settings verbatim (slicer profile names count).
- A failed print is a result — log it; "warped, retry" is a learning.
- New prototype ideas go in the catalog immediately, Status `planned`, with
  at least one question — an entry with no question gets rejected.
