---
name: review-print
description: Look at every piece before it goes on a plate or gets sliced, and decide whether it is worth printing at all — render each one top-down at the exact size and params it will print, read the picture, score it against the rubric (does it read as the pattern at that size, does the art fill its shape, is it a good object in the hand), and leave off anything that fails, with the reason written down. Use before any `bambu slice compose` / `slice plate`, when building a samples or minis plate, when adding new patterns or styles to a plate, and for "is this worth printing", "review the print", "check the plate before I send it", "look at it first". Passing the mesh gate is not this — a piece can be one clean watertight body and still be a slab with pinholes or half-empty art. Also use when a print comes back — Omar sends photos or says how the pieces came out ("too small", "loose", "looks great") — to write the print record with a verdict per piece. Runs inside print-coaster-samples and print-model; never sends.
---

# review-print — look at it before you print it

The mesh gate says a piece *can* print. It cannot say the piece is *worth* printing. On
2026-09-25 three minis passed every gate and still went onto minis-03:

- two near-solid discs (sDO9, nmEj);
- a half-filled square (n3Ii).

Two more had bare wedges between the art and the frame (lEfW, tA8e). Omar rejected all five
on sight: "mostly solid disks are not good coasters", "felt incomplete", "lots of weird empty
space".

The render showing all of it was already on disk. It was kept "so every pattern is
represented". This skill exists so that looking comes first and wins.

The rubric lives in [`rubric.md`](rubric.md). Read it every run; it grows as prints come back.

## How one run goes

1. **Render each distinct piece** at the exact params the plate will use. Use the same command
   as the mesh gate, from the bikar checkout:
   `node packages/cli/dist/index.js render <file> --format stl --check --param size=40 … -o <scratch>/<name>.stl`.
   Copies of one piece need one render.
2. **Make the sheet and the numbers**:
   `python3 tools/print_review.py sheet <scratch>/review.png <scratch>/*.stl`.
   It draws white material on black, one tile per piece, as seen from above. Per piece it
   prints four numbers:
   - `open`: the share of the outline cut through;
   - `biggest`: the share taken by the single largest hole;
   - `bare`: the share of grid cells that are almost all hole.
   - `sym` and `order`: how well the art matches itself turned, and the turn that matched.
     Below 0.9, run `python3 tools/print_review.py art <out.png> <pieces>` and look at the
     art alone.
   - When a piece sits in a frame (loose pieces in a coaster's holes), the view from above
     hides how tall each stands. `python3 tools/print_review.py side <out.png> <frame.stl>
     <label> <x0>,<y0>,<x1>,<y1> <piece.stl> …` cuts both straight down along that line and
     prints both heights. Render the pieces where their holes are, so the meshes line up.
3. **Read the PNG yourself**, every time, all of it. The numbers flag only the plain cases. On
   2026-09-25 they flagged neither tA8e's wedges nor anything that needs a sense of what the
   pattern *should* look like ([`rubric.md`](rubric.md) §What the numbers catch).
4. **Give each piece a verdict** against the rubric: **print**, or **leave off** with a reason
   in one line. When in doubt, leave it off. A missing sample costs a re-run; a bad one costs
   filament, an hour of machine time and Omar's trust in the plate.
5. **Do not fix a failure by changing size.** A pattern too dense for a mini was still a solid
   disc at 60 and 70 mm (sDO9, nmEj). Try another size once, look at it again, and if it still
   fails, leave it off and say so. Coverage of patterns never outranks a good piece: a plate of
   three patterns that read beats one of eight where five don't.
6. **Show Omar the sheet with the verdicts** before composing (`SendUserFile` the PNG), as a
   short table: piece → note → verdict → reason. The note column links each piece to its
   catalog note and style (`python3 .claude/skills/pattern-catalog/scripts/catalog.py note
   <pieces or plate.yaml> --from <the page's folder>`), so the history of that pattern is one
   click away. Omar makes the final call, and a picture is what he judges from.
7. **Write the leave-offs into the plate header** under "Left off", with the reason and Omar's
   words if he gave any, so the next session does not put them back.

## When a print comes back

Photos, or a line like "too small" or "a bit loose", mean the plate has printed. Record it the
same day, so what it taught is tied to the exact piece and size.

**Ask the page's questions first, one at a time.** Every experiment plate page has an
`## After the print` table, written before it printed (plates gate P12): the pieces, the
question, what we expected and why, and what each answer changes. Ask each row as its own
AskUserQuestion, in table order, naming the pieces to pick up **by the id cut into them** (D-109,
D-114), never by a bed name or a pair letter alone, and saying exactly what to do with them and
what to look for. A piece with no id is named by the mark it does carry ("the upper with `QT` on
its cut face"). The page's table names them the same way. Omar, 2026-10-08, on pkt-1: "i want
the questions to reference the piece ids", "be percidse in your questiosn", "update the .md to
be percise too". **Write each question as a short procedure, in the format
[`asking.md`](asking.md) sets out, with its do and don't examples**: one line on what is being
checked, the pieces by id, numbered steps of one action each, what each result looks like, then
the question. No recap, no filler (Omar, 2026-10-09: "not clear and straighformward and in
simple sop format ... easy to get a mistake"). Read it before each round. Build the options from the row's
last cell, one option per answer it names, each saying what that answer changes, plus "not
judged yet". Ask the next row only once this one is answered. Each answer goes into the record
below as those pieces' `verdict` and `notes`, in Omar's words; a row he leaves unanswered stays
`not-judged`. An answer that differs from "what we expect" is the lesson to carry forward in
step 6.

1. **Start from the draft.** `slice compose` wrote one at `.bambu/records/<date>-<plate>/`
   with every piece, its `params`, and the printer settings read off the `.3mf`. Copy it to
   `docs/prints/<date>-<plate>/`, set `status: printed`, and fill what the machine could not
   know: the filament actually loaded, and `~` for anything nobody recorded. Never guess.
2. **Give every piece its own `verdict` and `notes`.** `keep` (print it again as is),
   `adjust` (right idea, change its params), `drop` (do not print it again) or `not-judged`
   (Omar has not said yet; never fill his silence with a verdict, as sheets-04g's hexes, stars
   and outer pieces show). The notes use Omar's words about *that* piece. Then run the
   `pattern-catalog` sync, so each pattern's note lists the print and its verdict. Anything you worked out rather than saw, like a band width
   from the file's formula, says so. One note for the whole plate goes in `feedback`, and it
   does not replace the per-piece verdicts.
   Once the record is in `docs/prints/`, set each one with
   `bambu print verdict <run> <entry> keep|adjust|drop|not-judged -n "<note>"`. It changes only
   that piece's lines and refuses an unknown piece or verdict. The hub page calls the same command.
   If no draft exists, run `bambu slice compose <plate>` again to make one. It writes to
   `build/plates/`, never over `.bambu/plates/`. Then check that its meshes match the printed
   `.3mf` before you trust the hashes, as minis-04 did.
3. **Check the slice before you blame the piece.** Holes, a tight or loose fit, or weak straps
   can come from the slicer settings as easily as from the design. minis-03 and minis-04 both
   printed on Studio's built-in values instead of the X2D preset, because Studio's command line
   ignores `inherits`. Find the defect in the cause tables of
   [`print-quality-design.md`](../../../docs/design/printing/print-quality-design.md), write the suspects in
   the piece's notes, and say whether the settings actually used were the preset's. A reading
   from a slice that did not carry the preset does not move a bet. Write that in `feedback`, as
   the minis-04 record does.
   For a loose piece that is too tight or too loose, measure the fit before you guess at it.
   Render the frame and each piece group in place (the pieces file without `pack zipper`) and
   run `python3 tools/fit_gap.py <frame.stl> <piece.stl>...`: the gap per face round every piece,
   its sharpest tip, its outline per area, and where along the outline the play sits.
   `python3 tools/fit_gap.py walls <plate.3mf> <frame.stl> <piece.stl>...` reads the same off the
   slice's own wall paths, layer by layer, which shows what the slicer did to each group.
   sheets-04g found its loose middle piece this way ([the issue](../../../docs/issues/sheets-04g-fit.md)).
   For a split coaster's studs, `python3 tools/fit_gap.py studs <plate.3mf> <plate.bedmap.json>`
   gives each pair's stud and socket as sliced, and the gap between them. On spl-1 every gap came
   out as drawn, so the tight fit came from the printer, not the slice.
4. **Attach the photos.** Put them in `photos/`, list each with its sha256 and what it shows,
   and check there is no location data in them first.
5. **Check it.** Run `python3 .claude/gates/prints_gate.py`. It holds every rule, including one
   verdict per piece.
6. **Carry the lesson forward.** In the record's `feedback`, write:
   - `lesson`: what the print taught, in one line (the symptom and its cause);
   - `next`: what it changes for the next plate;
   - `decisions`: the D-ids decided from it, such as `[D-115]`, if any.

   **A fit or gap lesson names what it was measured with**: the nozzle size, the outer and inner
   wall line widths and the layer height, read off the record's profile and the `.3mf`
   (`line_width`, `outer_wall_line_width`, `inner_wall_line_width`). Write them as one clause,
   such as "(0.4 mm nozzle, 0.42 mm outer and 0.45 mm inner wall lines, 0.20 mm layers)". The
   lesson holds only for those settings. A gap that fit with a 0.4 mm nozzle says nothing yet
   about a 0.6 mm one, or about lines drawn at a different width, because the printed wall is
   built from those lines. The early minis plates were sliced with 0.4 mm lines and the outer
   wall left at the slicer's default; every plate since sheets-04 uses 0.42 and 0.45. The
   record's `nozzle_side` says which of the two nozzles printed it, and `nozzle_type` says the
   printer's code for it (such as `HS01`, standard flow, hardened steel), when the draft could
   read it from the printer. Leave either `~` when nothing recorded it.

   The Prints page lists these for every record. Then write a rule for the next plate in the
   calling skill's rules ([`sample-rules.md`](../print-coaster-samples/sample-rules.md) for
   samples). If the eye missed it before the print, add a check to [`rubric.md`](rubric.md),
   with the date and plate. If a number would have caught it, re-measure over the pieces on
   record and move the flag.
7. **Regenerate the Prints page and ship it** in the same PR as the record:
   `python3 .claude/skills/review-print/scripts/prints_page.py --write`. It rewrites the
   Lessons and Records parts of [`docs/prints.md`](../../../docs/prints.md) from every record,
   and the prints gate fails while the page is behind. The record is also what the Coaster Lab
   shows against each style.

Hand feel is not a measurement. "Loose" goes in the notes, and a bet moves only on a reading
under `readings` (the print-model skill's compare loop).

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/prints_page.py` | Writes the Lessons and Records parts of `docs/prints.md` from every record in `docs/prints/`: the run, its plate page, what happened and why, what it changed, its decisions, and its photos (or the plate page's renders, said plainly). With no flag it checks the page is current. | After writing or changing a print record, in the same PR. `make validate-prints` and hook `39-prints` run the check. | `python3 .claude/skills/review-print/scripts/prints_page.py --write` (check: no flag; tests: `--self-test`) |
