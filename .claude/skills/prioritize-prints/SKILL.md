---
name: prioritize-prints
description: Rank the plates that have not printed yet by return on printer time and say why each is where it is, keeping each plate's review page in docs/design/plates/ current — pictures, cost, what it answers, its Approvals table (every yes or hold Omar gave it), how many times it printed, and a dated timeline. Use for "which print next", "what should I print", "rank the prints", "prioritize prints", "what's in the print queue", "is this plate worth printing", after a new plate recipe lands, after Omar ticks a box on a plate page, and after a print record is written. Writes the pages and the queue, and reads a tick or a yes in chat into the Approvals table with .claude/skills/manage-approvals/scripts/plate_approve.py (D-093, D-096); never writes a yes he did not give and never sends to the printer.
---

# prioritize-prints — which plate next, and why

Omar asked for this on 2026-09-30: "a skill to help us prioritize the highest roi prints and
why", with "a file per print where prints are plates", approval on the page, pictures,
a timeline and a count of times printed. The design, and the calls still open on it:
[print-review-design](../../../docs/design/printing/print-review-design.md).

Each plate has a page `docs/design/plates/<plate>.md` beside its recipe `<plate>.yaml`. The page's
frontmatter holds the facts; the queue in [`docs/design/plates/README.md`](../../../docs/design/plates/README.md)
is computed from them by `plates_gate.py`, never typed. The scoring rule and its weights are
in [`scoring.md`](scoring.md) — read it every run, since the weights may have changed.

## Every run

1. **Read the ticks back.** For each page with a ticked box under `## Your call`, write it into
   the page's `## Approvals` table with `.claude/skills/manage-approvals/scripts/plate_approve.py` (D-096). The tool writes the dated
   row, the recipe iteration it covers (D-097) and the stage, and unticks the box, so the next tick is a new answer:
   - **Approve** ticked →
     `python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --approved --by "Omar, tick on this page"`. If the
     option he picked changes the recipe, make that change first, record it with `--iterate`,
     merge it, then record the yes, so the row covers the iteration he approved (manage-approvals
     skill).
   - **Hold** → `python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --held --by "Omar, tick: <his note>"`.
   - **It printed** (on a sent plate) → write the print record first (the review-print skill's
     record steps); the page follows it (step 4).
   - Then clear the notes, since the table now holds them.
   Never tick a box, and never record a yes with no ticked box or his words in chat; for a yes in
   chat, `--by "Omar, in chat: \"<his words>\""`. One approval covers one send: the send fills the
   row's `Spent by`, so a plate that went out needs a new row before it goes out again, and a
   design approved many times keeps every row. A production plate has a standing approval instead
   (D-095); leave its box alone. The plates gate (P2) checks the table; there is no approval in
   the frontmatter.
2. **Give every new recipe a page.** The gate fails on a `minis-NN.yaml` with no `minis-NN.md`.
   Copy the shape of [minis-06](../../../docs/design/plates/minis-06.md): In short, What it is, Why
   print it, Pictures, Cost and risk, Your call, Timeline. The page starts at `proposed`, with
   `maturity: experiment`; only the [grade-plate](../grade-plate/SKILL.md) skill raises it.
   A plate that is designed but waits on a build before it can have a recipe (the sampler
   sheets, [sheets-01](../../../docs/design/plates/sheets-01.md)) gets its page now, at `planned`,
   with `recipe:` and the costs empty and `needs:` listing the builds it waits on; the queue
   shows it by value on its "waiting on a build" line. When its recipe lands, drop `needs:` and
   move it to `proposed`.
   Before the page goes to Omar, check every prototype on it carries its id (an `id`, a `pair`
   letter or dots, whichever its `.bkr` declares), set by the plate, since the file's default is
   no mark. Omar, 2026-10-06: "every proptoty should have an id". The rule, and what to do with a
   piece too small to mark, is in print-coaster-samples'
   [sample-rules](../print-coaster-samples/sample-rules.md#checks-every-plate-passes-before-the-owner-gate).
3. **Pictures and cost, before `waiting`.** A page moves to `waiting` only with pictures.
   - The review sheet: `python3 tools/print_review.py sheet <out.png> <pieces.stl>`, from the
     review-print skill. Read it yourself and write what you saw on the page (openness, art
     fill, anything near-solid).
   - The bed: slice locally, **from a scratch directory**, because `bambu slice compose` writes
     `build/plates/` and `.bambu/records/` into whatever directory it runs in. The bed picture
     is plate_1.png in the Metadata folder inside the `.3mf`. A plate that spills onto a second
     bed is refused by `bambu slice compose`, naming what spilled, unless the recipe sets
     `beds: <n>`; `bambu validate sliced` prints the bed count and fails past `--beds`.
   - `minutes`, `grams` and `bed_plates` come from that slice. Shrink every picture
     (`magick in.png -resize 1400x -strip -colors 64 PNG8:out.png`) into `<plate>-media/`.
   - Set `risk:` by the machine, not the print: `watch` for small loose parts or anything a
     nozzle could drag, with what to watch written on the page; `hold` for anything that could
     damage the printer, until it is dealt with. A piece that snaps is data, not risk.
4. **Match the count to the records.** For each record in `docs/prints/` whose `plate:` starts
   with the plate's name, the page lists its run under `runs:`, `times_printed` is how many
   there are, and the timeline has a `printed` row naming it. The gate checks all three. A new
   record's verdicts can move the plate's maturity (and the maturity of every plate sharing a
   piece with it): run the grade-plate skill after it.
5. **Write the queue.** `python3 .claude/gates/plates_gate.py --write`. It refuses while any
   page has a finding; fix the page, not the gate.
6. **Say why.** Report the top three in plain words: what each answers, what it costs, what
   pushes it up or down (a second bed, a held risk, a repeat), and what Omar has to decide on
   each page. If the order looks wrong, say so and name the weight that caused it; changing a
   weight is a line in `scoring.md`'s round log, not a quiet edit.

## Never

- Send, or pass `--yes` to anything that talks to the printer. Sending is the
  [`send-plate`](../send-plate/SKILL.md) skill's, on Omar's live approval (D-093).
- Store a rank or an ROI on a page. The queue is computed each time (D-046: priority is
  presented, never stored).
- Put a plate page under `docs/prints/`; that folder is for records of what printed.
- Use `status:` on a plate page; plates use `stage:`, because the vault's `status` means a
  design doc's state.
