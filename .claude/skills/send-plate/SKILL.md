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

**One approval covers one send.** The approval is Omar's tick on the plate's page, or his yes in
chat that this skill writes onto the page. Sending spends it. The page's timeline logs every
approval and every send, so it is the record of each approved reprint. A plate that already went
out needs a new yes, even when the last one was yesterday.

Run every `bambu` call from the main checkout (the vault), with the node 22 PATH, so it reads the
pages Omar ticks in Obsidian: `tools/bambu/bin/bambu …`.

## 1. Find the plate

The plate is `docs/plates/<name>.yaml`, its page is `docs/plates/<name>.md`, and the sliced file is
`build/plates/<name>.plate.3mf`. No page means no send: the page is where the yes lives.

## 2. The approval

Read the page's `## Your call` boxes and its `## Timeline`.

- **Live:** an `approved` row after the last `sent` or `printed` row, or a ticked Approve box on a
  plate that has never gone out. Go on.
- **Omar said yes in chat for this plate, this send:** write it down before anything else. On a
  branch off `origin/master`: frontmatter `approved: true`, `approved_on: <today>`,
  `stage: approved`; tick the Approve box; add
  `| <today> | approved — by Omar in chat: "<his words>" | this page |` as the last timeline row.
  Ship it (PR, merge), then fast-forward the vault (`git -C <vault> merge --ff-only origin/master`)
  so the CLI reads it. His yes must name this plate. A general "go ahead" from earlier in the
  session does not cover a plate he has not seen.
- **Spent or missing:** stop. Say which, quoting the CLI's `✗ approval:` line, and ask him to tick
  the box or say yes.

Never write a yes he did not give. A plate whose last print showed the setup was wrong gets its
fix first and a new yes after.

## 3. Slice, if needed

If the `.3mf` is missing, or older than the `.yaml` or the bikar files it uses, slice it again
with the verb the recipe names in its header (`bambu slice compose docs/plates/<name>.yaml`, or
`slice sheet` for a sampler sheet), then
`bambu validate sliced build/plates/<name>.plate.3mf`. A slice that changes the plate's minutes,
grams or picture goes on the page as a `sliced` row. Whether a recipe change voids the approval is
still Omar's open call (print-review design call 6): say it changed and ask.

## 4. The printer, the filament, the bed

1. `bambu status show`: the printer is idle (IDLE, FINISH or FAILED) and nothing is mid-job.
2. `bambu filament-sync --plate build/plates/<name>.plate.3mf`: the plate's colors match loaded
   trays. A mismatch is Omar's to fix at the AMS; say which tray needs which spool.
3. `bambu print send build/plates/<name>.plate.3mf --dry-run`. Every line must be green:
   `✓ approval`, `✓ printer`, the warnings sidecar, the filament plan. It saves a bed photo under
   `.bambu/bed/` and prints its path.
4. **Open the photo and look.** Say what is on the bed: empty or not, the build plate seated or
   not. Anything left from the last print, or no plate, or no photo at all: stop and ask Omar to
   clear or check the bed in person. Never send on a photo you did not open.

## 5. Send

`bambu print send build/plates/<name>.plate.3mf --record --yes`. Pass `--yes` only after steps
2 to 4 are all green in this run. The CLI checks the approval and the printer again on its own.

When it goes through, the CLI rewrites the page in the vault: the box unticked, `stage: sent`, a
dated `sent` row naming the approval it spent. Ship that change: copy the page into a work branch
off `origin/master`, PR, merge, then put the vault's copy back to the merged one
(`git -C <vault> checkout -- docs/plates/<name>.md` only after `git diff` shows it matches) and
fast-forward. The `--record` draft stays in `.bambu/records/` until the pieces are judged.

If the send is refused, or a permission check denies the call, report it as it came. Never retry
another way and never send from Bambu Studio for him.

## 6. Report

In plain words: what was sent, the bed as the photo showed it, the printer state after the send,
the minutes and grams, and that the approval is spent, so a reprint needs a new yes.
