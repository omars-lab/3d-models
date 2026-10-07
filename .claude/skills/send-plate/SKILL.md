---
name: send-plate
description: Send one approved plate to the Bambu X2D end to end — check Omar's approval on the plate page, slice if needed, check the printer is idle, match the filament, look at the bed photo, send, and log the send on the page. Use for "send it", "print this plate", "send sheets-04b", "start the print", "reprint minis-03", and right after Omar approves a plate in chat. Not for deciding which plate to print (prioritize-prints), planning a new model's print (print-model), or a person walking a print at the machine (guide-print).
---

# send-plate — one approved plate, from page to printer

The checks that must never be skipped live in `bambu print send` itself
([`send-gate.ts`](../../../tools/bambu/src/send-gate.ts)): it refuses a plate whose page has no live
approval, and a printer that is busy or will not say its state. This skill puts the rest in order
and does the part only eyes can do: looking at the bed. The rules come from
[D-093](../../../docs/working-model/decisions-log.md).

**One approval covers one send.** The approval is a row in the page's `## Approvals` table
([D-096](../../../docs/working-model/decisions-log.md)): Omar's tick on the page, or his yes in
chat, written there by `.claude/skills/manage-approvals/scripts/plate_approve.py` with the date, his words and the recipe
iteration it covers (D-097).
Sending spends it: the row's `Spent by` gets the send's date. The table keeps every yes and the
timeline every send, so together they are the record of each approved reprint. A plate that
already went out needs a new yes, even when the last one was yesterday.

**Except a production plate** ([D-095](../../../docs/working-model/decisions-log.md)): it has a
standing approval, so it goes out again with no new yes. The CLI checks it live, through
`.claude/skills/manage-approvals/scripts/plate_approve.py --status`: the prints must still show production and the recipe must match the page's
`recipe_hash`. If either fails, the plate is back to one yes per send. Every plate today is an
experiment.

Run every `bambu` call from the main checkout (the vault), with the node 22 PATH, so it reads the
pages Omar ticks in Obsidian: `tools/bambu/bin/bambu …`.

## 1. Find the plate

The plate is `docs/design/plates/<name>.yaml`, its page is `docs/design/plates/<name>.md`, and the sliced file is
`build/plates/<name>.plate.3mf`. No page means no send: the page is where the yes lives.

## 2. The approval

Ask the tool, which reads the table the way the CLI will:
`python3 .claude/skills/manage-approvals/scripts/plate_approve.py docs/design/plates/<name>.md --status`.

- **Live:** `approved on <date> (…), for its first send` or `for send N`: an `approved` row with
  `Spent by` empty. Go on.
- **Ticked, not recorded:** the Approve box is ticked but no open row backs it. Read the tick back
  first (`plate_approve.py <page> --approved --by "Omar, tick on this page"`), ship it as below,
  then go on. A tick left over from a send made outside the CLI is the case this catches: if the
  timeline shows a send after the last row, ask him whether the tick is a new yes before you
  record it.
- **Standing (production only):** the dry run's `✓ approval: standing approval: …` line. Go on;
  the send leaves the box alone and logs a `sent` row that names the standing approval. A
  `no standing approval:` reason on a refusal means the plate slipped or its recipe changed: say
  which, and ask Omar for a yes for this send, or grade it (grade-plate).
- **Omar said yes in chat for this plate, this send:** write it down before anything else. On a
  branch off `origin/master`:
  `python3 .claude/skills/manage-approvals/scripts/plate_approve.py docs/design/plates/<name>.md --approved --by 'Omar, in chat: "<his words>"'`.
  It adds the row, sets `stage: approved` and leaves the box unticked. Ship it (PR, merge), then fast-forward the vault (`git -C <vault> merge --ff-only origin/master`)
  so the CLI reads it. His yes must name this plate. A general "go ahead" from earlier in the
  session does not cover a plate he has not seen.
- **Spent or missing:** stop. Say which, quoting the CLI's `✗ approval:` line, and ask him to tick
  the box or say yes.

Never write a yes he did not give. A plate whose last print showed the setup was wrong gets its
fix first and a new yes after.

## 3. Slice, if needed

If the `.3mf` is missing, or made from an older recipe, slice it again with the verb the recipe names in its header (`bambu slice compose docs/design/plates/<name>.yaml`, or
`slice sheet` for a sampler sheet), then
`bambu validate sliced build/plates/<name>.plate.3mf`. A slice that changes the plate's minutes,
grams or picture goes on the page as a `sliced` row. A recipe change resets the approval
([D-097](../../../docs/working-model/decisions-log.md)): record it with
`plate_approve.py <name> --iterate` (manage-approvals skill), ship it, and ask Omar again. A
comment-only edit is not a change, so a reprint as-is keeps its yes.

The slice verbs write the recipe's hash beside the `.3mf` (in its `.warnings.json`), and the send
compares it with the recipe now: `✗ slice` means the recipe changed since, or the slice predates
the check, and either way it gets sliced again. A `.bkr` edited in bikar under the same recipe is
not caught, so after a bikar change, slice again by hand.

A slice is made for one build plate, and the plate type changes the G-code itself: the bed
temperature, and on the X2D a first-layer offset only the Textured PEI Plate gets. The slice verbs
take the plate Bambu Studio is set to, or `--plate-type textured_plate` (and the like) when you
name it; the log says which (`plate type: Textured PEI Plate (…)`). When the plate on the bed
changes, slice again: a slice made for another plate is refused at the send, and a slice made
without a plate type is refused too. sheets-04b went out sliced for a Cool Plate with a Textured
PEI Plate on the bed, and the X2D paused it at layer 0 with 0500-8051
([the issue](../../../docs/issues/sliced-for-wrong-plate.md)).

## 4. The printer, the filament, the bed

1. `bambu status show`: the printer is idle (IDLE, FINISH or FAILED) and nothing is mid-job.
   `bambu storage show`: a storage card is in and has room, since the upload writes to the card.
   No card is Omar's to fix at the printer (the sheets-04b send, 2026-10-03). Old plates can come
   off with `bambu storage list` and `bambu storage rm <name>`, which deletes from his printer, so
   ask him first.
2. `bambu filament-sync --plate build/plates/<name>.plate.3mf`: the plate's colors match loaded
   trays. A mismatch is Omar's to fix at the AMS; say which tray needs which spool. A recipe with
   no `color:` is one whose color is picked at the send: pass the color Omar named with his yes,
   `--color "#RRGGBB"`, on the dry run and the send alike, and the dry run's `color:` line and
   tray match show which spool it took. With no `--color` it prints in the slice's own color,
   Studio's default green.
3. `bambu print send build/plates/<name>.plate.3mf --dry-run`. Every line must be green:
   `✓ approval`, `✓ printer`, `✓ plate`, `✓ nozzle`, `✓ slice`, `✓ storage`, the warnings sidecar, the
   filament plan. It saves a bed photo under `.bambu/bed/` and prints its path (or take one with
   `bambu bed photo <name>`). The `plate:` line compares the plate the slice is for with the one
   the printer reports. `⚠ plate` means the printer named a plate id we have not matched yet, or
   none: the photo settles it in the next step. The `nozzle:` line compares the nozzle sizes the
   slice was made for with the ones fitted; `✗ nozzle` means slice again. The `bed:` line is `✗`
   on this first dry run, because nobody has looked at the photo yet.
4. **Open the photo and look, then write down what it shows.** Say what is on the bed: empty or
   not, the build plate seated or not, and which plate it is (the Textured PEI Plate is gold and
   grainy; Omar's glacier plate, from 2026-10-07, is smooth light blue with a honeycomb strip on
   its right edge). The printer reports both as P0101, so only the photo tells them apart. For
   the glacier plate, see [a non-Bambu plate](#a-non-bambu-plate-the-glacier) below before going
   on. Then record it, since the send refuses without it:
   `bambu bed verdict <name> --plate-type <the plate you saw> --by "Claude, opened the photo" --clear --seated`,
   or `--no-clear` / `--no-seated` with a `--note` saying what is wrong. Run the dry run again
   with `--no-bed-photo` (a new photo would need a new look); the `bed:` line must now be `✓`.
   Anything left from the last print, or no plate, or no photo at all: stop and ask Omar to clear
   or check the bed in person. Never send on a photo you did not open, and never write a verdict
   for one.

### A non-Bambu plate (the glacier)

sld-1 went out on the glacier plate (2026-10-07), sliced for Textured PEI, and the X2D stopped
before the first layer twice: first "foreign objects detected on heatbed" (0500-806E) on an empty
plate, then "the print plate marker was not detected" (0500-8062). It ran as soon as Omar put the
gold plate in. What to do instead, from
[the plate research](../../../docs/research/2026-10-07-third-party-plates.md#recommendation):

1. **Slice it as Smooth PEI:** `--plate-type hot_plate` ("Smooth PEI Plate / High Temp Plate").
   Not Textured PEI: the X2D's start G-code lowers the nozzle 0.02 mm for Textured only, which
   squashes the first layer on a smooth plate. Bambu's PLA profile keeps the bed at 55 °C.
2. **Record the bed verdict for that plate:** `--plate-type hot_plate`, with a `--note` that names
   the glacier plate. The printer still reports P0101, which we also read as Textured PEI; the
   dry run's `plate:` line then shows `⚠ … the bed verdict decides: it saw a High Temp Plate`
   instead of refusing. With no verdict, or one that saw Textured, it still refuses.
3. **The printer's two checks are Omar's to switch.** Foreign Object Detection and Type
   Detection must be off on the printer, or he presses "Ignore this and Resume" on 8062 each
   print. `bambu options show` says where they stand. To switch them, ask him: he does it at the
   printer (Settings > Print Options), or says go in chat for this change and you run
   `bambu options set foreign-object off --yes` and `bambu options set plate-type off --yes`
   (Studio closed), each of which must read back `✓`. His go for one change does not cover the
   next. Both are printer-wide, so they stay off for the gold plate until switched back on the
   same way. The rest of the checks stay on; the walk-through is in the
   [printer setup skill](../setup-bambu-x2d/SKILL.md#build-plates-and-print-options).

What the send checks on its own, and why there is no git hook for it:
[the issue](../../../docs/issues/sliced-for-wrong-plate.md#checked-before-every-send).

## 5. Send

`bambu print send build/plates/<name>.plate.3mf --record --yes`. Pass `--yes` only after steps
2 to 4 are all green in this run. The CLI checks the approval, the printer, the plate, the nozzles
and the bed verdict again on its own. It takes no new photo: it reads the newest one, which must
be under 30 minutes old and carry a verdict for those exact bytes.

When it goes through, the CLI rewrites the page in the vault through `plate_approve.py --sent`:
the open row's `Spent by` becomes `sent <today>`, the box unticked, `stage: sent`, and a dated
`sent` row on the timeline naming the approval it spent. Ship that change: copy the page into a work branch
off `origin/master`, PR, merge, then put the vault's copy back to the merged one
(`git -C <vault> checkout -- docs/design/plates/<name>.md` only after `git diff` shows it matches) and
fast-forward. The `--record` draft stays in `.bambu/records/` until the pieces are judged.

It also writes the send's `sent` row into the plate's print log
(`docs/design/plates/print-logs/<name>.md`), through the monitor-print skill's
`print_monitor.py --sent`: each tray it fed, the tray's color and the slice's grams for it. The
shelf (`bambu shelf show`) takes those grams off the spool when the print ends, so ship the log
with the page. The dry run's `sent row:` line shows the row first. A `⚠ sent row:` line means
one tray could not be named and no row is written: the print will show on the shelf as not
counted. Say so in the report, and write the row by hand with
`print_monitor.py <name> --sent <hex> <tray> <grams>` if Omar wants it counted.

If the send is refused, or a permission check denies the call, report it as it came. Never retry
another way and never send from Bambu Studio for him.

## 6. Watch it

Right after the send goes through, hand the print to the
[monitor-print](../monitor-print/SKILL.md) skill. It writes the printer's state onto the page,
checks the print is still moving, takes a chamber picture every 10 minutes for you to look at,
and makes a timelapse GIF when the print ends. A send with no watch after it is not finished.

## 7. Report

In plain words: what was sent, the bed as the photo showed it, the printer state after the send,
the minutes and grams, that the monitor is watching it, and that the approval is spent, so a
reprint needs a new yes.
