---
date: 2026-10-03
---

# sheets-04b was sliced for the wrong build plate

2026-10-03. Found by the first send that reached the printer. Fixed in the CLI and the send-plate
skill the same day.

## What happened

sheets-04b went out through `bambu print send`. The upload and the start both worked, and the
printer went to PREPARE, then RUNNING. A few minutes later it stood paused at layer 0 with
`0500-8051`, "the detected build plate is not the same as the G-code file". At 20:12 UTC it
reported FAILED with `0300-400C`, which is a cancel (BambuStudio issue #527); the print was most
likely stopped at the printer. Nothing printed.

## What the evidence showed

Three sources, read separately, agree.

- **The bed photo** the dry run took before the send shows a gold, grainy Textured PEI Plate.
- **Bambu Studio's settings** on this Mac have `app.curr_bed_type` set to `4`. In Studio's
  `BedType` list (Default 0, Cool 1, Engineering 2, High Temp 3, Textured PEI 4, Supertack 5) that is
  the Textured PEI Plate. Only that one key was read; the same file holds the printer's access code.
- **The slice** said `"bed_type":"cool_plate"` in the `.3mf`'s plate file (`Metadata/plate_<n>.json`, n = 1), and
  `curr_bed_type = Cool Plate` in its settings.

Why the slice said Cool Plate: Studio's command line takes the plate type from the process
settings (`curr_bed_type`), its built-in default there is the Cool Plate (PrintConfig.cpp), and our
slice code never set it. Studio's app sets it from the plate picker, which is why plates sliced in
Studio were fine.

The plate type is not a label. It changes the G-code. The sent file and a re-slice for the
Textured PEI Plate, compared line by line:

| | sent (Cool Plate) | re-sliced (Textured PEI Plate) |
|---|---|---|
| bed temperature, start and wait | `M140 S35`, `M190 S35` | `M140 S55`, `M190 S55` |
| first-layer offset | `G29.1 Z0.022` | `G29.1 Z0.002 ; for Textured PEI Plate` |

The printer's camera reads the plate's marker before it starts and pauses on a mismatch. That check
is a printer setting (`buildplate_marker_detector`), not something the job turns on: the start
G-code's own `build_plate_detect_flag=1` line is commented out. The pause protected the print, and
no field in the start command skips it, so the only real fix is a slice made for the plate on the
bed.

The send then said `bed_type: "auto"`. Studio never sends `"auto"`: its send carries the slice's
own plate type (`plate_data.bed_type`, PrintJob.cpp), from a fixed list of tokens (`cool_plate`,
`eng_plate`, `hot_plate`, `textured_plate`, `supertack_plate`). The earlier dispatch doc had
listed `"auto"` as an unconfirmed default; this send settled it the wrong way round.

## What changed

- **Slicing names its plate.** `slice plate` and `slice compose` take `--plate-type`, and without it
  use the plate Studio is set to, so a slice here matches a slice made in Studio. With neither,
  they refuse rather than fall back to the Cool Plate. The type is written into the flattened
  process settings, the same way the filament map mode is, and the existing preset check then
  proves the slice carries it. The log line
  `plate type: Textured PEI Plate (Bambu Studio's saved plate type)` says which was used.
- **The send carries the slice's plate type.** `print send` reads it off the `.3mf` (the per-plate
  value first, then the project's) and puts that token in `bed_type`. `--bed-type` is gone:
  sending a plate name other than the one the G-code was made for is the bug itself. A file that
  names no plate type is refused, dry run or not.
- **The send compares the plate.** The printer reports a plate id (`device.plate.cur_id`). No
  source decodes these ids, so the CLI knows only the one we have seen next to a plate we could
  name: `P0101`, the Textured PEI Plate, on this day. A known id that does not match the slice
  refuses the send (`✗ plate`). An unknown id, or none, warns (`⚠ plate`) and leaves it to the bed
  photo, which the send-plate skill now says to check for the plate type as well as for a clear
  bed.
- **The monitor reads a cancel as a stop.** `print_monitor.py` writes `stopped`, with the cancel's
  meaning, for `0300-400C`, instead of `failed` and "not looked up yet".

The code is `tools/bambu/src/plate-type.ts`, with its tests beside it.

## Checked before every send

After the re-slice, Omar asked whether a hook should make sure a plate was sliced right, and
whether the send should look at the printer first. A git hook does not fit: the `.3mf` is build
output and never committed, and slicing is not a commit, so a hook would never see the file it is
meant to check. The checks went into `print send` itself, which every send runs, dry run or not,
and which no flag skips. Each refuses a real send and only reports on a dry run:

- **The plate** (above): the slice's plate type against the plate id the printer reports.
- **The nozzles:** the nozzle sizes in the slice's project settings against the ones the printer
  reports (`device.nozzle.info`, 0.4 and 0.4 on the X2D). They are compared as sizes, not per
  nozzle, because no source we hold says which slice entry belongs to which nozzle. A printer that
  reports none warns. The code is `tools/bambu/src/nozzle-check.ts`.
- **The bed, as someone saw it:** Omar asked for "recently pulled screenshots, screenshot
  verdicts". The send now needs the plate's newest bed photo to be under 30 minutes old and to
  carry a written verdict, made with `bambu bed verdict`, that says the bed is clear, the plate is
  seated, and which plate it is. The verdict holds the photo's checksum, so a retaken photo needs a
  new look, and the plate it names must be the one the slice is for, which is the sheets-04b case
  caught by eye. The real send takes no new photo; it uses the one that was looked at. The code is
  `tools/bambu/src/bed-check.ts`, with `bambu bed photo`, `bed show` and `bed verdict` in
  `tools/bambu/src/commands/bed.ts`.

Still to come: a check that the slice is newer than its recipe, so an edited plate cannot go out
on an old slice.

## What it means for sheets-04b

The file on disk was made for the Cool Plate and cannot go out again. It needs a re-slice (the one
above passed the preset check and names `textured_plate`) and a new yes from Omar before any
resend. Its approval was spent by the cancelled send.

## The other start fields

Studio's start command carried more fields than ours (the integer calibration modes, a second
tray map, the file name and others). The checked research,
[what Studio sends to start an X2D print](../research/2026-10-03-studio-start-payload.md), ranks
them; none is known to feed the plate check. They followed as their own change, described in
[first-party dispatch](first-party-dispatch.md#2026-10-03-the-start-command-matches-studios).
