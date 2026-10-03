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

If the `.3mf` is missing, or older than the `.yaml` or the bikar files it uses, slice it again
with the verb the recipe names in its header (`bambu slice compose docs/design/plates/<name>.yaml`, or
`slice sheet` for a sampler sheet), then
`bambu validate sliced build/plates/<name>.plate.3mf`. A slice that changes the plate's minutes,
grams or picture goes on the page as a `sliced` row. A recipe change resets the approval
([D-097](../../../docs/working-model/decisions-log.md)): record it with
`plate_approve.py <name> --iterate` (manage-approvals skill), ship it, and ask Omar again. A
comment-only edit is not a change, so a reprint as-is keeps its yes.

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
   trays. A mismatch is Omar's to fix at the AMS; say which tray needs which spool.
3. `bambu print send build/plates/<name>.plate.3mf --dry-run`. Every line must be green:
   `✓ approval`, `✓ printer`, `✓ plate`, `✓ storage`, the warnings sidecar, the filament plan. It
   saves a bed photo under `.bambu/bed/` and prints its path. The `plate:` line compares the plate
   the slice is for with the one the printer reports. `⚠ plate` means the printer named a plate id
   we have not matched yet, or none: the photo settles it in the next step.
4. **Open the photo and look.** Say what is on the bed: empty or not, the build plate seated or
   not, and which plate it is (the Textured PEI Plate is gold and grainy) and that it is the one
   the `plate:` line names. Anything left from the last print, or no plate, or no photo at all: stop and ask Omar to
   clear or check the bed in person. Never send on a photo you did not open.

## 5. Send

`bambu print send build/plates/<name>.plate.3mf --record --yes`. Pass `--yes` only after steps
2 to 4 are all green in this run. The CLI checks the approval and the printer again on its own.

When it goes through, the CLI rewrites the page in the vault through `plate_approve.py --sent`:
the open row's `Spent by` becomes `sent <today>`, the box unticked, `stage: sent`, and a dated
`sent` row on the timeline naming the approval it spent. Ship that change: copy the page into a work branch
off `origin/master`, PR, merge, then put the vault's copy back to the merged one
(`git -C <vault> checkout -- docs/design/plates/<name>.md` only after `git diff` shows it matches) and
fast-forward. The `--record` draft stays in `.bambu/records/` until the pieces are judged.

If the send is refused, or a permission check denies the call, report it as it came. Never retry
another way and never send from Bambu Studio for him.

## 6. Watch it

Right after the send goes through, start the monitor from the vault, in the background (Bash
`run_in_background`, which tells you when it exits):

`python3 .claude/skills/send-plate/scripts/print_monitor.py <name>`

It asks the printer for its state every 30 seconds and adds a row to the page's `## Print log`
for each change: preparing, printing, paused (with the error code and what it means), resumed,
25/50/75%, finished, failed, stopped, or lost when the printer stops answering. It keeps going
through a pause and stops on the last four. To hear about a pause while it runs, follow the rows
with the Monitor tool: `tail -f .bambu/monitor/<name>.log | grep --line-buffered "ev=row\|ev=exit"`.

- **Paused:** tell Omar at once, with the code and its meaning. Resuming, stopping or swapping
  the plate are his, at the printer or on his word in chat; never resume or stop it yourself.
- **Finished:** the print is done, not judged. The record and the Timeline's `printed` row come
  when the pieces are judged, as before.
- **Ship the log:** the rows are on the vault's page. When the watch ends, ship the page the
  same way as the send's change in step 5.

## 7. Report

In plain words: what was sent, the bed as the photo showed it, the printer state after the send,
the minutes and grams, that the monitor is watching it, and that the approval is spent, so a
reprint needs a new yes.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/print_monitor.py` | Polls the printer, writes each change onto the plate page's `## Print log`, logs to `.bambu/monitor/<name>.log` | Right after a send (step 6), or to pick up watching a print already running | `python3 .claude/skills/send-plate/scripts/print_monitor.py <name>` |
| same, `--self-test` | Runs the monitor on made-up printer reports and a made-up page | After editing it; `make validate-prints` runs it | `python3 .claude/skills/send-plate/scripts/print_monitor.py --self-test` |
