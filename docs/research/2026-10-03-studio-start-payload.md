---
date: 2026-10-03
produced-by: checker agent (Claude) consolidating researcher A (PR #504) and researcher B (PR #503); sources re-opened with curl, gh and WebFetch
feeds:
  - '[[first-party-dispatch]]'
  - send parity in tools/bambu (the start command built in tools/bambu/src/backends/mqtt.ts)
---

# What Bambu Studio sends to start a LAN print on the X2D (consolidated)

This is the one to act on. It checks two independent research passes, A (PR #504,
`docs/research/2026-10-03-studio-start-payload-a.md` on its branch) and B (PR #503,
`docs/research/2026-10-03-studio-start-payload-b.md` on its branch), against the sources
behind them and against our start command, `buildProjectFileCommand` in
`tools/bambu/src/backends/mqtt.ts`. It feeds [first-party-dispatch](../issues/first-party-dispatch.md).
The two research files stay on their branches as the record this was built from.

**What happened.** Our CLI sent sheets-04b with `bed_type: "auto"`. The printer paused at
layer 0 with HMS 0500-8051 ("Detected build plate is not the same as the Gcode file. Please
adjust slicer settings or use the correct plate.") and the job was cancelled at the printer
(0300-400C). The slice says Cool Plate (plate_1.json `"bed_type":"cool_plate"`, project
settings `curr_bed_type` "Cool Plate"). The bed photo shows a gold, grainy Textured PEI plate.
So the file was sliced for a plate that was not on the bed.

No printer was contacted for this check.

"Fetched" below means the checker downloaded the file or page on 2026-10-03 and read the
quoted text. "Carried" means the checker did not re-open it and is relying on what a research
file says about it (with that file's own fetched or snippet mark).

## The short answer

1. **The real fault is the slice, not just the send.** The file was sliced for Cool Plate, the
   bed holds Textured PEI, and the X2D's own printer profile says it does not support Cool
   Plate at all. The plate type changes the G-code itself (bed temperature and the first-layer
   Z offset), so no start-command field can make a Cool Plate file correct on a Textured PEI
   plate. The fix is to slice for the plate that is on the bed and send that plate's name.
2. **Studio never sends `bed_type: "auto"`.** It sends the plate name from the slice. `"auto"`
   came to us from community clients and docs. Both passes agree and the source confirms it.
3. **Our start command is missing several fields Studio sends on an X2D**, the most important
   being the three-way calibration modes as numbers. None of them is known to feed the plate
   check, but they are real differences and one X2D capture shows all of them.
4. **The claim that "the same kind of file, sent from Studio, printed fine on the same plate" is
   not shown by any source.** Nobody captured what Studio sent for sheets-04. Studio has code
   paths that would quietly switch an X2D job from Cool Plate to Textured PEI, which would
   explain why Studio's print ran and ours paused. That is a reading of the source, not proven.

## What to change in the send, ranked

Each row says what Studio does, the source, and whether the checker fetched it.

| # | Change | What Studio does | Source | Status |
|---|---|---|---|---|
| 1 | **Slice for the plate on the bed.** Set `curr_bed_type` when slicing (the X2D default is Textured PEI) and refuse to send when the slice's plate does not match the plate seen in the bed photo. | The X2D profile says `"default_bed_type": "Textured PEI Plate"` and `"not_support_bed_type": "Cool Plate"`. The X2D start G-code picks the Z offset by plate: `{if curr_bed_type=="Textured PEI Plate"} G29.1 Z{0.002}` else `Z{0.022}` (at bed 70 °C or below), and the bed temperature comes from the plate's own setting. The Studio command-line slicer defaults `curr_bed_type` to Cool Plate (btPC) when nothing sets it, which is how our slice got Cool Plate. | BambuStudio master: X2D machine profile JSON; X2D 0.4 nozzle start G-code template; PrintConfig.cpp L1367-1382 | Fetched |
| 2 | **Send `bed_type` as the slice's plate name, never `"auto"`.** Map the slice's `curr_bed_type` through Studio's table (Cool Plate → `cool_plate`, Engineering → `eng_plate`, High Temp → `hot_plate`, Textured PEI → `textured_plate`, and so on) and refuse to send if the result is `unknown`. | PrintJob.cpp L207-210 takes the bed type from the slice's plate; `bed_type_to_gcode_string` in PrintConfig.hpp L464-490 has no `"auto"` entry and falls back to `"unknown"`. The send dialog's `"auto"` entry is commented out (SelectMachine.cpp L177). | BambuStudio master: PrintJob.cpp, PrintConfig.hpp, SelectMachine.cpp | Fetched |
| 3 | **Send the calibration modes as numbers** `auto_bed_leveling`, `extrude_cali_flag`, `nozzle_offset_cali` (0 off, 1 on, 2 auto), and `extrude_cali_manual_mode` (0 in the X2D capture; left out when Studio holds -1). | The X2D start G-code uses `M1002 judge_flag` on `extrude_cali_flag`, `g29_before_print_flag` and `auto_cali_toolhead_offset_flag`, so the job decides whether those steps run. The X2D capture sends `auto_bed_leveling: 2`, `extrude_cali_flag: 2`, `nozzle_offset_cali: 2`, `extrude_cali_manual_mode: 0`. | bambuddy issue #1192 (X2D, firmware 01.01.00.00, Studio sends); X2D start G-code template; open-bamboo-networking print ABI L177-181 | Fetched |
| 4 | **Match the booleans to Studio.** `bed_leveling` and `flow_cali` false (the mode rides in the numbers), `vibration_cali` false, `layer_inspect` true. We send true, true, true, false. | SelectMachine.cpp L3371-3383 hard-codes vibration false and layer_inspect true; the X2D capture shows bed_leveling false and flow_cali false next to the "2" modes. | SelectMachine.cpp; bambuddy #1192 | Fetched |
| 5 | **Add `file`**, the .3mf name. | Present in both Studio sends in the X2D capture. | bambuddy #1192 | Fetched |
| 6 | **Add `ams_mapping2`** next to `ams_mapping`. | Present in the X2D capture. | bambuddy #1192 | Fetched |
| 7 | **Add `cfg`.** `"0"` in the X2D capture; `"4"` in a P2S capture where bit 2 meant the internal timelapse. | Bit meanings: bit 0 extruder-change assist, bit 2 internal timelapse. | bambuddy #1192; open-bamboo print ABI L133-157, L177-181 | Fetched |
| 8 | **Use a `sequence_id` in the 20000s**, and do not reuse one across restarts. | The X2D capture uses 20001 and 20002. open-bamboo records err_code 84033544 when an id is reused across restarts. | bambuddy #1192; open-bamboo print ABI L164 | Fetched |
| 9 | **`md5`: leave as is for now.** We send `""`. Studio sends either a real uppercase MD5 or the literal `"from_sd_card"`, depending on the source (see disagreements). The X2D accepted our `""` and started the job, so md5 is not what paused it. | | bambuddy #1192; open-bamboo print ABI L171 | Fetched, disputed |

Not changes:

- **The url scheme.** Studio's X2D sends use `brtc://emmc/<name>` (the eMMC path over port
  6000); we use `ftp:///<name>`. With Developer Mode on, the printer took our FTPS url and
  started the job, so this is not the fault. Source: bambuddy #1192 (fetched), open-bamboo print
  ABI L116-121 (fetched).
- **`nozzle_mapping`.** Disputed; see below. Do not add it until it is seen in an X2D capture.

## What the two passes agreed on

- **Studio never sends `"auto"`.** Both found it. The checker confirmed: the only `"auto"` in
  Studio is the starting value of a cloud-task record (ProjectTask.cpp L66,
  `task_bed_type = "auto";`, which is not the send path) and the commented-out dialog entry. Community clients
  send `"auto"`: the OpenBambuAPI doc ("Always auto for local prints", A fetched), ha-bambulab
  (A fetched, B snippet), bambuddy's own client (both fetched), bambu-printer-mcp (carried).
- **There is no per-job field that skips the plate check.** Both found the check is a
  printer-wide camera switch, not a start-command field. The checker confirmed: one camera key,
  `buildplate_marker_detector`, turns on both plate-type and plate-position detection
  (DevPrintOptions.cpp L110-146, fetched). Nothing in Studio's print parameters, the dialog, or
  either capture skips it.
- **The X2D start G-code does not set `build_plate_detect_flag=1`.** The brief for this work
  said it did; both passes and the checker found the line is commented out
  (`;M1002 set_flag build_plate_detect_flag=1`). The detection that does run is
  `M972 S19 P0 ;heatbed detection` and `M972 S34 P0 ;print plate deviation detection`
  (start G-code template, fetched).
- **Fixing the plate means matching it.** Both read 0500-8051 as a real mismatch, not a false
  alarm. The printer's own text says "adjust slicer settings or use the correct plate"
  (hms_en_20P.json, fetched). A forum thread (t/65448, fetched) has the same pause with Cool
  Plate chosen in Studio and Textured PEI on the bed; selecting Textured in the slicer fixed it,
  and a second person confirmed that.
- **Our calibration fields differ from Studio's** (booleans vs three-way numbers). Both found
  it; the X2D capture settles the values.
- **The printer's status differs between the paused run and the finished run in a few bits:**
  `job_attr` 2 vs 18 (bit 4, inside the nibble Studio reads as job state, most likely pause vs
  finish), the status `cfg` bit 40 and the status `fun` bit 58. Both passes found these; neither
  found what bits 40 and 58 mean. These are fields the printer reports, not fields we send.

## Where they disagreed, and whom the source backs

### md5 on a LAN send

- **A:** Studio sends the literal `"from_sd_card"`, never a real hash. Source: open-bamboo
  print ABI L171, "A real file hash never appeared in any captured LAN project_file", from
  plugin versions 02.05.00 to 02.08.02 on the SD-card and FTPS paths. **The source says what A
  says** (fetched).
- **B:** Studio sends a real uppercase MD5. Source: bambuddy #1192, two Studio sends to an X2D
  on firmware 01.01.00.00 over the eMMC path, May 2026, md5 `BCF8FEA7...` and `A3FC355A...`,
  different per file; the maintainer notes only md5 and sequence_id differ between the two.
  **The source says what B says** (fetched).
- **Checker:** both are true for their own setup. The likely split is plugin version or upload
  path (eMMC on a newer X2D vs FTPS/SD card on older plugins), but no source states that. Not
  settled. It does not matter for the pause: the X2D started our job with `md5: ""`.

### nozzle_mapping on a two-nozzle printer

- **A:** Studio sends it on multi-nozzle printers, taken from the printer's reply to
  `get_auto_nozzle_mapping`. Source: open-bamboo print ABI L176 (fetched).
- **B:** the X2D capture has no `nozzle_mapping`.
- **Checker:** Studio's code adds it only when the mapping it built is non-empty
  (SelectMachine.cpp L3346-3352, fetched), so both can be true. The one X2D capture we have
  (bambuddy #1192, fetched) has none. The X2D capture backs leaving it out for now.

### The bed_type field table in open-bamboo

- open-bamboo's own field table (print ABI L172) says `bed_type` "defaults to 'auto'" and is
  "One of the MachineBedTypeString values". A said that line is wrong; B leaned on it less.
- **Checker:** the same file's capture (L133-157) shows `textured_plate`, and its overlay note
  (L246) shows `task_bed_type="textured_plate"` turning `"auto"` into `"textured_plate"`. The
  `"auto"` default is the plugin's fallback when it is handed nothing, not what Studio hands it.
  The capture backs A.

## What only one pass found

### Only A

- **The storage difference.** Studio's sheets-04 send used the printer's eMMC with no card; our
  send went to a USB drive. A flagged this as something that differs between the run that
  printed and the run that paused. Nothing ties storage to the plate check, so it is a
  confound to keep in mind, not a cause. Single-source.
- **"The same kind of file, sent from Studio's GUI to the same printer with the same plate on
  the bed, printed to the end."** See the next section: no source shows this. Single-source,
  and B made the same assumption without stating it.

### Only B

- **The X2D capture itself** (bambuddy #1192). It is the only wire capture of Studio talking to
  an X2D in either pass, and most of the field table above rests on it. Single-source, but
  fetched and specific (firmware, date, two sends).
- **Forum evidence on Studio's "Auto plate type" setting** (t/161622, fetched): "If on, it will
  always use your current plate type or the last one used", and it can override a 3mf's plate
  type. The checker found the code behind it (below).
- **A send-time check that shows the slice's plate before sending.** B proposed printing the
  slice's plate name and the plate on the bed before every send. The checker agrees and folded
  it into change 1.
- **Notes from bambuddy:** `use_ams` must stay a boolean; -1 marks an unused AMS slot; HMS
  0500-4004 means the printer is busy; the acknowledgement can be slow on an H2D Pro. Carried,
  single-source.

## The "Studio's Cool Plate job printed fine" claim

**What the sources show.** The sheets-04 plate page records "sent — by Omar, from Bambu Studio
over LAN, the local slice of 62 minutes and 17 g", then printed. The print record for
2026-10-02 sheets-04 says it printed and was judged by hand. The status reports from that run
show the printer's plate id `P0101` at the end. None of these say what Studio put on the wire,
or which plate was on the bed, or which plate the job was sliced for at the moment of sending.

**Why that matters.** Studio has three code paths that would quietly move an X2D job off Cool
Plate before sending (all BambuStudio master, fetched):

- When the printer preset changes, the plate list is rebuilt without types the printer does
  not support, and any plate set to an unsupported type is reset to the printer's default
  (Plater.cpp L3838-3866 reset_bed_type_combox_choices; PartPlate.cpp L5431
  check_all_plate_local_bed_type).
- When the chosen type is not offered, the plate falls back to the printer default
  (Plater.cpp L3810-3822 set_bed_type_accord_combox → use_default_bed_type, L3869-3880).
- With "Auto plate type" on (Preferences.cpp L1476: "Studio will remember build plate selected
  last time for certain printer model"), loading a project uses the remembered plate for that
  printer rather than the file's (Plater.cpp L3440-3485).

The X2D's default plate is Textured PEI and Cool Plate is unsupported, so any of these would
turn the job into a Textured PEI job, re-slice it, and send `textured_plate`. That would print
cleanly on the Textured PEI plate in the photo, and explain why Studio's send ran and ours
paused. **This is the checker's reading of the source, not a proven fact.** `P0101` fits it
(ha-bambulab's recorded data shows `P0101` on the X2D, H2D and H2S, whose default plate is
Textured PEI), but nothing decodes `P0101` to a plate name.

**Verdict:** single-source, an inference from status reports, and contradicted in spirit by the
bed photo. Do not build on it.

## Options that belong to the printer's owner

These would make the pause go away without fixing the mismatch. They are listed so the owner
knows they exist, not recommended:

- Turning off the camera's plate detection (the `buildplate_marker_detector` switch, also shown
  in Studio's printer options; the forum's "Enable detection of build plate position").
- Answering the paused job with resume, or with the HMS "ignore" command
  (DeviceManager.cpp L1474, `"command":"ignore"`). The printer offers three actions for
  0500-8051 (hms_action_20P.json, fetched).

Both leave a file sliced for the wrong plate printing with the wrong bed temperature and
first-layer offset.

## Open questions

- **What Studio actually sent for sheets-04**, and whether it re-sliced for Textured PEI. The
  way to settle it is a capture at the broker or Studio's network-plugin log on the next Studio
  send.
- **What the firmware compares when `bed_type` is `"auto"`.** No source in either pass says.
  Once we send the real plate name this stops mattering, unless we want `"auto"` as a fallback.
- **What `P0101` and the other `cur_id` values mean.** Not decoded anywhere either pass looked.
- **Whether md5 matters on the X2D** (real hash vs `"from_sd_card"` vs empty). It did not stop
  our job from starting.
- **Whether `nozzle_mapping` is ever needed on the X2D.** The one capture has none.
- **The start command's `cfg` bits beyond 0 and 2**, and what bits 40 and 58 of the printer's
  status `cfg` and `fun` mean.
- **Whether to send `cfg` at all.** Studio's X2D sends carry `"cfg": "0"` (bambuddy #1192,
  fetched), but bambuddy's own client notes "No cfg: it is the printer's device-config bitmask"
  (bambuddy #3040, carried from B). Sending `"0"` matches the capture, so change 7 follows it.

## Sources the checker re-opened

All fetched on 2026-10-03.

- BambuStudio master (raw.githubusercontent.com): PrintJob.cpp and PrintJob.hpp, ProjectTask.cpp,
  PrintConfig.hpp and PrintConfig.cpp, SelectMachine.cpp, PartPlate.cpp, Plater.cpp,
  Preferences.cpp, DevPrintOptions.cpp, DeviceManager.cpp, the Bambu Lab X2D machine profile,
  the X2D 0.4 nozzle start G-code template, hms_en_20P.json and hms_action_20P.json.
- open-bamboo-networking, research/08.08-print-abi.md.
- bambuddy issue #1192 (gh issue view).
- Bambu Lab forum threads t/65448 and t/161622 (WebFetch).

Carried from the research files without re-opening, with their own marks: OpenBambuAPI mqtt.md
(A fetched), ha-bambulab (A fetched, B snippet), bambuddy's bambu_mqtt.py (both fetched), other
open-bamboo pages (12.01.01, 12.01.04, 12.12), DeviceErrorDialog and DevBed in Studio, an
OrcaSlicer snippet, forum t/206297, and the search snippets each pass marked as such.
