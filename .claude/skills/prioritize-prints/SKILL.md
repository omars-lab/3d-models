---
name: prioritize-prints
description: Rank the plates that have not printed yet by return on printer time and say why each is where it is, keeping each plate's review page in docs/plates/ current — pictures, cost, what it answers, whether Omar approved it, how many times it printed, and a dated timeline. Use for "which print next", "what should I print", "rank the prints", "prioritize prints", "what's in the print queue", "is this plate worth printing", after a new plate recipe lands, after Omar ticks a box on a plate page, and after a print record is written. Writes the pages and the queue; never ticks a box for Omar and never sends to the printer.
---

# prioritize-prints — which plate next, and why

Omar asked for this on 2026-09-30: "a skill to help us prioritize the highest roi prints and
why", with "a file per print where prints are plates", approval in the frontmatter, pictures,
a timeline and a count of times printed. The design, and the calls still open on it:
[print-review-design](../../../docs/design/printing/print-review-design.md).

Each plate has a page `docs/plates/<plate>.md` beside its recipe `<plate>.yaml`. The page's
frontmatter holds the facts; the queue in [`docs/plates/README.md`](../../../docs/plates/README.md)
is computed from them by `plates_gate.py`, never typed. The scoring rule and its weights are
in [`scoring.md`](scoring.md) — read it every run, since the weights may have changed.

## Every run

1. **Read the ticks back.** For each page with a ticked box under `## Your call`, move what it
   says into the frontmatter and add a timeline row with today's date:
   - **Approve** ticked → `stage: approved`, `approved: true`, `approved_on:` the date, a row
     `approved — <which option>`. If the option changes the recipe, make that change in the same
     PR and re-slice.
   - **Hold** → `approved: false`, a row `held — <their note>`; stay at `waiting`.
   - **It printed** (on a sent plate) → write the print record first (the review-print skill's
     record steps); the page follows it (step 4).
   - Then clear the ticks and the notes, since the timeline now holds them.
   Never tick a box, and never set `approved: true` without a ticked box or Omar's words in chat.
   `approved:` left empty means nobody asked, which is different from `false`.
2. **Give every new recipe a page.** The gate fails on a `minis-NN.yaml` with no `minis-NN.md`.
   Copy the shape of [minis-06](../../../docs/plates/minis-06.md): In short, What it is, Why
   print it, Pictures, Cost and risk, Your call, Timeline. The page starts at `proposed`.
3. **Pictures and cost, before `waiting`.** A page moves to `waiting` only with pictures.
   - The review sheet: `python3 tools/print_review.py sheet <out.png> <pieces.stl>`, from the
     review-print skill. Read it yourself and write what you saw on the page (openness, art
     fill, anything near-solid).
   - The bed: slice locally, **from a scratch directory**, because `bambu slice compose` writes
     `build/plates/` and `.bambu/records/` into whatever directory it runs in. The bed picture
     is plate_1.png in the Metadata folder inside the `.3mf`; a plate_2.png there means the plate spilled onto a
     second bed. `bambu validate sliced` does not flag that yet, so look for it.
   - `minutes`, `grams` and `bed_plates` come from that slice. Shrink every picture
     (`magick in.png -resize 1400x -strip -colors 64 PNG8:out.png`) into `<plate>-media/`.
   - Set `risk:` by the machine, not the print: `watch` for small loose parts or anything a
     nozzle could drag, with what to watch written on the page; `hold` for anything that could
     damage the printer, until it is dealt with. A piece that snaps is data, not risk.
4. **Match the count to the records.** For each record in `docs/prints/` whose `plate:` starts
   with the plate's name, the page lists its run under `runs:`, `times_printed` is how many
   there are, and the timeline has a `printed` row naming it. The gate checks all three.
5. **Write the queue.** `python3 .claude/gates/plates_gate.py --write`. It refuses while any
   page has a finding; fix the page, not the gate.
6. **Say why.** Report the top three in plain words: what each answers, what it costs, what
   pushes it up or down (a second bed, a held risk, a repeat), and what Omar has to decide on
   each page. If the order looks wrong, say so and name the weight that caused it; changing a
   weight is a line in `scoring.md`'s round log, not a quiet edit.

## Never

- Send, or pass `--yes` to anything that talks to the printer. Sending is Omar's.
- Store a rank or an ROI on a page. The queue is computed each time (D-046: priority is
  presented, never stored).
- Put a plate page under `docs/prints/`; that folder is for records of what printed.
- Use `status:` on a plate page; plates use `stage:`, because the vault's `status` means a
  design doc's state.
