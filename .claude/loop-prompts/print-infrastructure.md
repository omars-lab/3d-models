# Loop prompt — the print line: config in, reviewed plate out

Paste the block below into a fresh session, or run it as `/loop` with no interval so the
session paces itself. Written 2026-09-25.

This loop builds the tooling. It does not add designs (that is
[`catalog-expansion.md`](catalog-expansion.md)), it does not get the first print through (that
is [`coaster-pipeline.md`](coaster-pipeline.md)), and it does not tidy PRs
([`consolidation.md`](consolidation.md)).

---

## The goal

**Turning any catalog design into a print-ready plate takes one short config file and one
command.** Every step checks its own output and says clearly why when it fails. The result can
be looked at before anything is sent, and the next plate costs less effort than the last one.

Met when a new plate (a mix of coasters, sizes and colours) goes from a new YAML file to a
sliced, previewed plate with filament mapped to the loaded AMS trays:
- with no hand edits,
- with no step that lives only in someone's head,
- with a picture of the plate to look at,
- with a failure that names its cause whenever an input is wrong.

The send itself stays Omar's.

## What exists (check it; don't rebuild it)

- **The `bambu` CLI** (`tools/bambu/src/commands/`): `slice plate`, `slice compose` (a plate
  from a manifest), `slice coaster` (colour regions become a multi-part AMS 3MF),
  filament-sync (maps the plate's slots to the live trays by colour), `print capture`, and
  `validate`. Hook 45 keeps its flag reference in sync.
- **Plate manifests**: [`minis-01.yaml`](../../docs/plates/minis-01.yaml), the first one.
- **Designs of record**: [`plate-composer-design.md`](../../docs/plate-composer-design.md)
  and [`coaster-colour-design.md`](../../docs/coaster-colour-design.md).
- **Skills**: `print-model` (plan a print), `guide-print` (run one at the bench), `bambu`
  (day-to-day CLI), `find-model` (outside models). Coaster Lab in bikar sets each design's
  knobs and colours.
- **Plans**: the phase map, P4.x, is in [`iterative-dazzling-finch.md`](../plans/iterative-dazzling-finch.md).
  The printer side, gates R1 to R5, is in [`binary-tickling-kay.md`](../plans/binary-tickling-kay.md).

## Each pass of the loop

0. **Read the backlog,**
   [`docs/tasks/print-infrastructure/backlog.md`](../../docs/tasks/print-infrastructure/backlog.md).
   If it holds a known friction, take the top one and go to step 3.
1. **Run the whole line on a real plate, stopping short of the send.** Take `minis-01`, or
   write a new manifest that mixes things `minis-01` doesn't cover, then compose, slice,
   preflight and filament-sync it. Use the documented commands exactly as a newcomer would.
2. **Find the first friction.** The first step that needed a hand edit, a guessed flag, a
   file read to understand an error, a slice with no preview, or a check that passes on bad
   input. Fix only that one step; write every other friction the run hit into the backlog.
3. **Fix it at the source,** where the tool, the manifest schema, or the error message lives.
   A new check needs a case that fails, not only one that passes (CLAUDE.md, "the by-design
   failure"). A picture of the plate beats a line of text saying it is fine.
4. **Ship it.** Open one PR from its own worktree, then merge it and delete that branch.
   Re-run step 1 to show the friction is gone.
5. **Record it,** in the same PR. Move the item to the
   [done list](../../docs/tasks/print-infrastructure/done.md) with the date and PR number.
   Update the plate-composer design, or add a `docs/issues/<slug>.md` if the approach changed.
   Work for another loop goes into that loop's backlog ([README](README.md)).
6. **Wait when the line runs clean.** Say so in one line, then schedule the next wakeup
   30 to 60 minutes out. A clean pass on a harder plate is the goal getting closer.

## Order

1. Anything that lets a bad plate look good: a check that passes wrongly, a silent fallback,
   a wrong filament mapping.
2. Anything done by hand on every plate.
3. Anything you cannot see before sending: previews, the contact sheet, per-region colour.
4. Config ergonomics: defaults, shorter manifests, clearer errors.

## Never

- Never dispatch a print, and never change a printer setting. Both are Omar's
  ([tenet](../memory/no-measurement-worth-the-machine.md)).
- Never reimplement bikar geometry here. This repo uses bikar.
- Never add a new tool where a flag on an existing one would do.
