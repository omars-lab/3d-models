---
name: monitor-print
description: Watch a print running on the X2D until it ends — the printer's state into the plate's print log (its own file, linked from the page), a check that the print is still moving (a stall when the layer and percent stop), a chamber picture every 10 minutes that you open and look at, and a timelapse GIF at the end. Use right after a plate is sent (send-plate hands off here), when Omar asks how a print is going, whether it is proceeding, for camera screenshots or a timelapse of a print, or to pick up watching a print already running.
---

# monitor-print — is the print going, and what does it look like

A sent plate is not a printed plate. Between the send and the judging, three things can go
wrong that nobody sees from the terminal: the printer pauses (a wrong plate, a filament runout),
the print stops moving while still saying RUNNING, or it keeps moving and makes spaghetti. The
monitor catches the first two from the printer's own report and takes the pictures for the
third, which only eyes can judge. Omar asked for it on 2026-10-03: "our skill should make sure
print is proceeding", with a chamber picture every 10 minutes and a GIF timelapse.

The X2D runs its own first-layer and spaghetti detection
([D-092](../../../docs/working-model/decisions-log.md)), so never ask Omar to turn it on. The
pictures here are our look on top of that, not a substitute for it.

Run everything from the main checkout (the vault), with the node 22 PATH, like every `bambu`
call, so the rows land in the log Omar opens from the page in Obsidian.

## 1. Start the watch

Right after the send (send-plate step 6), or as soon as you learn a print is running with no
watch on it (`pgrep -fl print_monitor` prints nothing), start it in the background (Bash
`run_in_background`, which tells you when it exits):

`python3 .claude/skills/monitor-print/scripts/print_monitor.py <name>`

It asks the printer every 30 seconds and adds a row to the plate's print log,
`docs/design/plates/print-logs/<name>.md`, for each change. The first row makes the file and
links it from the page's frontmatter (`print_log: '[[print-logs/<name>|print log]]'`), so the
page keeps the design and the approvals and the log keeps the printer's words. The rows are watching, preparing, printing, paused (with the error code and what it
means), resumed, the 25/50/75% marks, stalled, error, finished, failed, stopped, and lost when
the printer stops answering. It keeps going through a pause and a stall, and stops on the last
four. Every 10 minutes, and at every row, it saves a chamber picture to
`.bambu/monitor/<name>/frames/`. When it stops it makes `.bambu/monitor/<name>/timelapse.gif`.

For a short print, take pictures more often so the GIF has enough frames: `--snapshot-every 2`
gives about 20 frames for a 40-minute plate. Ten minutes suits prints of an hour or more.

## 2. Follow it

Follow the rows and pictures with the Monitor tool:
`tail -f .bambu/monitor/<name>.log | grep --line-buffered "ev=row\|ev=snapshot_done\|ev=exit"`.

- **Every picture: open it and look.** Say in a line what it shows: pieces laying down where the
  slice puts them, or something wrong (a piece knocked loose, strings or a blob on the nozzle,
  filament not reaching the bed, the plate empty while the percent climbs). Something wrong: tell
  Omar at once, with the picture. Send it with SendUserFile when he may be away from the terminal.
- **Paused:** tell Omar at once, with the code and its meaning.
- **Stalled:** the printer says RUNNING but no new layer or percent has come for 15 minutes. Tell
  Omar, with the newest picture. It may be a long layer, so do not call it failed.
- **Lost:** the printer stopped answering. Say so; the print may still be going.

Resuming, stopping, pausing or swapping the plate are Omar's, at the printer or on his word in
chat. Never send one of those commands yourself, and never the "ignore and resume" one.

## 3. When it ends

- **The GIF:** open `.bambu/monitor/<name>/timelapse.gif`, look at it, and send it to Omar
  (SendUserFile). If the watch died before making it, rebuild it from the frames:
  `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --gif`.
- **Finished** means the print is done, not judged. The record and the Timeline's `printed` row
  come when the pieces are judged, as before.
- **Ship the log:** the rows are in the vault's `print-logs/<name>.md` (and, on a plate's first
  watch, the page's new `print_log:` line). Copy both into a work branch off `origin/master`,
  run `plates_gate.py --write`, then PR and merge. The log is append-only: the plates gate (P10,
  hook 39) refuses a commit that changes or drops a row master already has, or deletes a log, so
  a wrong row is answered by a new row, never by an edit. Then put the vault's copies back to the
  merged ones: `git -C <vault> checkout --` each file only after `git diff` shows it matches,
  then fast-forward. The pictures and the GIF stay in `.bambu/`, which
  is gitignored.

## 4. Report

In plain words: how it ended, how long it took, what the pictures showed (the last one most of
all), and the GIF.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/print_monitor.py` | Polls the printer, adds each change and any stall to the plate's `print-logs/<name>.md` (linking it from the page the first time), saves a chamber picture on the clock and at every row, makes the GIF at the end, logs to `.bambu/monitor/<name>.log` | Right after a send, or to pick up watching a print already running | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> [--snapshot-every 10] [--stall-after 15]` |
| same, `--gif` | Rebuilds `timelapse.gif` from the frames already taken | The watch died before the end, or frames were added by hand | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --gif` |
| same, `--self-test` | Runs the monitor on made-up printer reports and a made-up page, and reads the log back through the plates gate | After editing it; `make validate-prints` runs it | `python3 .claude/skills/monitor-print/scripts/print_monitor.py --self-test` |
