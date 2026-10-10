---
name: monitor-print
description: Watch a print running on the X2D until it ends, in the background — the printer's state into the plate's print log (its own file, linked from the page), a check that the print is still moving (a stall when the layer and percent stop), a chamber picture every 10 minutes that a background watcher agent opens and looks at, and at the end a small WebP timelapse and finished picture published onto the plate's page. Use right after a plate is sent (send-plate hands off here), when Omar asks how a print is going, whether it is proceeding, for camera screenshots or a timelapse of a print, or to pick up watching a print already running.
---

# monitor-print — is the print going, and what does it look like

A sent plate is not a printed plate. Between the send and the judging, three things can go
wrong that nobody sees from the terminal: the printer pauses (a wrong plate, a filament runout),
the print stops moving while still saying RUNNING, or it keeps moving and makes spaghetti. The
monitor catches the first two from the printer's own report and takes the pictures for the
third, which only eyes can judge. Omar asked for it on 2026-10-03: "our skill should make sure
print is proceeding", with a chamber picture every 10 minutes and a GIF timelapse.

On 2026-10-10 he asked for the watching to happen behind the scenes, since a print runs 45
minutes or more: "a sub agent and that our main agent can continue working on important things
as our print proceeds". So a background agent, the watcher, looks at the pictures, and the main
session hears from it only when something needs Omar or the print is over. He also asked that
the watcher put the timelapse on the plate's page, small: "are they slow and efficient or are
they bloated?" An animated WebP at 480 px is about 120 KB, where the 640 px GIF was 1.4 MB.

The X2D runs its own first-layer and spaghetti detection
([D-092](../../../docs/working-model/decisions-log.md)), so never ask Omar to turn it on. The
pictures here are our look on top of that, not a substitute for it.

Run everything from the main checkout (the vault), with the node 22 PATH, like every `bambu`
call, so the rows land in the log Omar opens from the page in Obsidian.

## 1. Start the watch, then hand it to the watcher

Right after the send (send-plate step 6), or as soon as you learn a print is running with no
watch on it (`pgrep -fl print_monitor` prints nothing):

1. **Start the script** in the background yourself (Bash `run_in_background`, which tells you
   when it exits). A background shell started by a subagent can end with the subagent, so the
   main session owns it:
   `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name>`
2. **Start the watcher**: an Agent (it runs in the background), its prompt the brief in
   [`watcher.md`](watcher.md) below the line, with `<plate>` filled in and `<cursor>` as `0`.
3. **Go back to other work.** You hear from the watcher when it returns, and from the script when
   it exits.

The script asks the printer every 30 seconds and adds a row to the plate's print log,
`docs/design/plates/print-logs/<name>.md`, for each change. The first row makes the file and
links it from the page's frontmatter (`print_log: '[[print-logs/<name>|print log]]'`), so the
page keeps the design and the approvals and the log keeps the printer's words. The rows are
watching, preparing, printing, paused (with the error code and what it means), resumed, the
25/50/75% marks, stalled, error, finished, failed, stopped, and lost when the printer stops
answering. It keeps going through a pause and a stall, and stops on the last four. Every 10
minutes, and at every row, it saves a chamber picture to `.bambu/monitor/<name>/frames/`. When
it stops it makes `.bambu/monitor/<name>/timelapse.gif`, the full-size copy to send Omar.

For a short print, take pictures more often so the timelapse has enough frames:
`--snapshot-every 2` gives about 20 frames for a 40-minute plate. Ten minutes suits prints of an
hour or more.

## 2. While it prints

The watcher waits on the run log (`--next`), opens every picture and writes a line about it
(`--look`, into `.bambu/monitor/<name>/looks.md`). It comes back early when:

- **a picture shows something wrong**: a piece knocked loose, strings or a blob on the nozzle,
  filament not reaching the bed, the plate empty while the percent climbs. Tell Omar at once,
  with the picture. Send it with SendUserFile and PushNotification, since he is likely away from
  the terminal.
- **paused**: tell Omar at once, with the code and its meaning.
- **stalled**: the printer says RUNNING but no new layer or percent has come for 15 minutes. Tell
  Omar, with the newest picture. It may be a long layer, so do not call it failed.
- **lost**: the printer stopped answering. Say so; the print may still be going.
- **the watch went silent** (`ev=watch_silent`): the script has died. Check `pgrep -fl
  print_monitor`; if it is gone and the print is still running, start it again (§1 step 1).

Then start a new watcher with the cursor the last one returned, so it picks up where that one
stopped, if the print is still going.

Resuming, stopping, pausing or swapping the plate are Omar's, at the printer or on his word in
chat. Never send one of those commands yourself, and never the "ignore and resume" one. The
watcher's brief says the same.

When Omar asks how it is going, read the last lines of `looks.md` and open the newest picture
yourself; there is no need to wait for the watcher.

## 3. When it ends

The watcher comes back once the script exits. By then it has looked at the last pictures and run
`--publish`.

- **The pictures on the page.** `--publish` makes `docs/design/plates/<name>-media/timelapse.webp`
  (every frame, 480 px, half a second each, the last held) and `finished.webp` (the last frame),
  with their metadata stripped, and a `## The print` section on the page that shows both. It
  refuses, writing nothing, when a QR code can be read in any frame (the repo is public and the
  printer wears QR stickers), or when either file is over 400 KB. A refusal is Omar's call:
  show him the picture, and never get round the check. A picture with someone in it (a hand
  lifting the plate off, an arm reaching in) stays off the page: `--leave-out <frame>` drops it,
  and the section says how many were left out. Omar's call on 2026-10-10, after sheets-04g-fit2's
  last frame caught his hand. Leaving a picture out is for a person, never for a QR code. If the
  watcher could not publish, run it yourself from the vault:
  `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --publish [--leave-out <frame>]`.
- **Send Omar the timelapse**: the full-size GIF in `.bambu/monitor/<name>/timelapse.gif`
  (SendUserFile), which plays everywhere. Open it first. If the watch died before making it,
  rebuild it from the frames: `print_monitor.py <name> --gif`.
- **Finished** means the print is done, not judged. The record and the Timeline's `printed` row
  come when the pieces are judged, as before.
- **Ship it all in one PR:** the vault's `print-logs/<name>.md`, the page (its `## The print`
  section, and on a plate's first watch its new `print_log:` line), and the two WebPs. Copy them
  into a work branch off `origin/master`, run `plates_gate.py --write`, then PR and merge. The
  log is append-only: the plates gate (P10, hook 39) refuses a commit that changes or drops a
  row master already has, or deletes a log, so a wrong row is answered by a new row, never by an
  edit. Then put the vault's copies back to the merged ones: `git -C <vault> checkout --` each
  tracked file only after `git diff` shows it matches, move the untracked copies aside only
  after `cmp` shows they match, then fast-forward. The frames, the looks and the GIF stay in
  `.bambu/`, which is gitignored.

## 4. Report

In plain words: how it ended, how long it took, what the pictures showed (the last one most of
all), and the timelapse.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/print_monitor.py` | Polls the printer, adds each change and any stall to the plate's `print-logs/<name>.md` (linking it from the page the first time), saves a chamber picture on the clock and at every row, makes the GIF at the end, logs to `.bambu/monitor/<name>.log` | Right after a send, or to pick up watching a print already running; the main session starts it | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> [--snapshot-every 10] [--stall-after 15]` |
| same, `--next` | Waits until the run log has a row, a picture, a timeout or the end past line `--after`, prints them and `cursor=<n>`; `ev=quiet` after `--wait` minutes, `ev=watch_silent` (exit 3) when the script has died | The watcher's loop ([`watcher.md`](watcher.md)); give the Bash call a 10-minute timeout | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --next --after <cursor> --wait 9` |
| same, `--look` | Adds one line to `.bambu/monitor/<name>/looks.md`: the picture and what it showed | The watcher, after opening each picture | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --look <frame> "<what it shows>"` |
| same, `--publish` | Animated WebP and finished still, 480 px, metadata stripped, into `<name>-media/`, and a `## The print` section on the page; `--leave-out` keeps a picture with a person in it off; refuses on a readable QR code, a file over 400 KB, or a left-out name that is not a picture | The print has ended; the watcher runs it, or you do if it could not | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --publish [--leave-out <frame>]` |
| same, `--gif` | Rebuilds the full-size `timelapse.gif` in `.bambu/` from the frames already taken | The watch died before the end, or frames were added by hand | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --gif` |
| same, `--sent` | Writes the send's `sent` row and exits: each tray it fed, its color and the slice's grams for it, which the shelf (`bambu shelf show`) takes off the spool when the print closes | `print send` calls it itself right after the print starts; by hand only when the send said it could not name a tray | `python3 .claude/skills/monitor-print/scripts/print_monitor.py <name> --sent '#00ae42' 'AMS 0 · slot 3' 27.28` |
| same, `--self-test` | Runs the monitor on made-up printer reports and a made-up page, reads the log back through the plates gate, and publishes made-up frames, one with a real QR code that must be refused, then left out by name | After editing it; `make validate-prints` runs it | `python3 .claude/skills/monitor-print/scripts/print_monitor.py --self-test` |
