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
   prints three numbers:
   - `open`: the share of the outline cut through;
   - `biggest`: the share taken by the single largest hole;
   - `bare`: the share of grid cells that are almost all hole.
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
   short table: piece → verdict → reason. Omar makes the final call, and a picture is what he
   judges from.
7. **Write the leave-offs into the plate header** under "Left off", with the reason and Omar's
   words if he gave any, so the next session does not put them back.

## When a print comes back

Photos, or a line like "too small" or "a bit loose", mean the plate has printed. Record it the
same day, so what it taught is tied to the exact piece and size.

1. **Start from the draft.** `slice compose` wrote one at `.bambu/records/<date>-<plate>/`
   with every piece, its `params`, and the printer settings read off the `.3mf`. Copy it to
   `docs/prints/<date>-<plate>/`, set `status: printed`, and fill what the machine could not
   know: the filament actually loaded, and `~` for anything nobody recorded. Never guess.
2. **Give every piece its own `verdict` and `notes`.** `keep` (print it again as is),
   `adjust` (right idea, change its params) or `drop` (do not print it again). The notes use
   Omar's words about *that* piece. Anything you worked out rather than saw, like a band width
   from the file's formula, says so. One note for the whole plate goes in `feedback`, and it
   does not replace the per-piece verdicts.
3. **Attach the photos.** Put them in `photos/`, list each with its sha256 and what it shows,
   and check there is no location data in them first.
4. **Check it.** Run `python3 .claude/gates/prints_gate.py`. It holds every rule, including one
   verdict per piece.
5. **Carry the lesson forward.** Write a rule for the next plate in the calling skill's rules
   ([`sample-rules.md`](../print-coaster-samples/sample-rules.md) for samples). If the eye
   missed it before the print, add a check to [`rubric.md`](rubric.md), with the date and
   plate. If a number would have caught it, re-measure over the pieces on record and move the
   flag.
6. **Ship it** as a PR. The record is what the Prints page and the Coaster Lab show against
   each style.

Hand feel is not a measurement. "Loose" goes in the notes, and a bet moves only on a reading
under `readings` (the print-model skill's compare loop).
