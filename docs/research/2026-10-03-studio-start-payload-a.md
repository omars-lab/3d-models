---
date: 2026-10-03
produced-by: researcher A (Claude), WebFetch / WebSearch / gh / curl
feeds:
  - '[[first-party-dispatch]]'
---

# What Bambu Studio sends to start a LAN print, and what trips 0500-8051 (researcher A)

Research for [first-party-dispatch](../issues/first-party-dispatch.md). Our CLI send of
sheets-04b stopped in PAUSE at layer 0 with `print_error` 83918929, which is HMS
`0500-8051` ("Detected build plate is not the same as the Gcode file"). The same kind of file,
sent from Studio's GUI to the same printer with the same plate on the bed, printed to the end.
This file asks why, and what our start command should change.

No printer was contacted for this research. Everything below comes from source code, other
people's wire captures, docs and forum posts.

## The short answer

- **Studio does not send `bed_type: "auto"`.** On a normal GUI send it reads the plate's
  `curr_bed_type` from the 3mf and sends it as a plate string. For a 3mf sliced with
  `curr_bed_type = Cool Plate` that string is `"cool_plate"`. We send `"auto"`, a value that
  came from a community doc which says "Always auto for local prints".
- **That is the most likely cause of the pause, but it is not proven.** No source I found says
  what the firmware compares when `bed_type` is `"auto"`. The check itself is a printer-wide
  camera option, not a per-job field.
- **Our start command also differs from Studio's in about ten other fields** for a two-nozzle
  printer. None of them is named as a plate-check input in any source, but they are real
  differences.
- **`P0101` is not decoded anywhere I looked.** It is the same on the H2D, H2S and X2D in
  other projects' recorded data.

## Sources

"Fetched" means I downloaded the page or file and read the text quoted. "Snippet" means I saw
only a search-result excerpt or summary, not the page.

| # | Source | Kind | Status |
|---|---|---|---|
| S1 | [BambuStudio `PrintJob.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/Jobs/PrintJob.cpp) (master) | source | fetched |
| S2 | [BambuStudio `PrintJob.hpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/Jobs/PrintJob.hpp) | source | fetched |
| S3 | [BambuStudio `PrintConfig.hpp`](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.hpp) and [`PrintConfig.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp) | source | fetched |
| S4 | [BambuStudio `SelectMachine.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/SelectMachine.cpp) | source | fetched |
| S5 | [BambuStudio `PartPlate.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/PartPlate.cpp) | source | fetched |
| S6 | [BambuStudio `bambu_networking.hpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/Utils/bambu_networking.hpp) (the `PrintParams` struct) | source | fetched |
| S7 | [BambuStudio `ProjectTask.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/ProjectTask.cpp) | source | fetched |
| S8 | [BambuStudio `DevPrintOptions.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/DeviceCore/DevPrintOptions.cpp) and [`PrintOptionsDialog.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/PrintOptionsDialog.cpp) | source | fetched |
| S9 | [BambuStudio `DeviceManager.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/DeviceManager.cpp), [`DevUtil.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/DeviceCore/DevUtil.cpp) | source | fetched |
| S10 | [BambuStudio `DeviceErrorDialog.hpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/DeviceErrorDialog.hpp) and [`.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/DeviceErrorDialog.cpp) | source | fetched |
| S11 | [BambuStudio X2D machine profile](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/machine/Bambu%20Lab%20X2D.json) and the X2D 0.4 nozzle start gcode | profile | fetched |
| S12 | [BambuStudio `resources/hms/hms_en_20P.json`](https://github.com/bambulab/BambuStudio/tree/master/resources/hms) and `hms_action_20P.json` | data | fetched |
| S13 | [ClusterM/open-bamboo-networking `research/08.08-print-abi.md`](https://github.com/ClusterM/open-bamboo-networking/blob/main/research/08.08-print-abi.md) (wire captures of the stock network plugin) | captures + notes | fetched |
| S14 | open-bamboo-networking `STATUS.md`, `12.01.04-fields-device.md`, `12.12-xcam.md` | notes | fetched (STATUS.md as a code-search excerpt) |
| S15 | [Doridian/OpenBambuAPI `mqtt.md`](https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md) | community doc | fetched |
| S16 | [greghesp/ha-bambulab](https://github.com/greghesp/ha-bambulab) `pybambu/commands.py`, `coordinator.py`, test mock data | client | fetched |
| S17 | [maziggy/bambuddy `backend/app/services/bambu_mqtt.py`](https://github.com/maziggy/bambuddy/blob/main/backend/app/services/bambu_mqtt.py) and issue [#1629](https://github.com/maziggy/bambuddy/issues/1629) | client | fetched |
| S18 | [DMontgomery40/bambu-printer-mcp `src/printers/bambu.ts`](https://github.com/DMontgomery40/bambu-printer-mcp/blob/main/src/printers/bambu.ts) | client | fetched |
| S19 | ioBroker.bambulab `lib/state_attr.js` | client | fetched |
| S20 | [Bambu forum t/39104](https://forum.bambulab.com/t/the-current-build-plate-is-not-the-same-as-in-g-code-error/39104) | forum | fetched |
| S21 | [Bambu forum t/170676](https://forum.bambulab.com/t/cool-plate-selection-workaround-found/170676) | forum | fetched |
| S22 | Web search summary on disabling the build plate check | search | snippet |
| S23 | synman/bambu-printer-manager (`bed.name.lower()`), tribixbite/beambam schema comment | client | snippet (code-search line only) |
| S24 | Forum threads 36736, 33769, 65448, 161622; BambuStudio issues #9945, #7921, #8281, #7051 | forum / issues | snippet |

The set of clients I checked for how they fill `bed_type`: Studio (S1–S5), the stock network
plugin as captured by S13, OpenBambuAPI (S15), ha-bambulab (S16), bambuddy (S17),
bambu-printer-mcp (S18), ioBroker (S19), and two more seen only as snippets (S23). OrcaSlicer
shares Studio's `PrintJob` code, but I did not read its copy.

## Q1. The `project_file` field set

### How Studio fills it

Studio's GUI builds a `PrintParams` struct (S6) in `PrintJob::process()` (S1). The closed
network plugin then turns it into the MQTT message. S13 captured what the plugin puts on the
wire, so the chain is: Studio source shows the inputs, S13 shows the output.

**`bed_type` comes from the plate in the 3mf.** S1, lines ~207–210:

```cpp
PartPlate* curr_plate = m_plater->get_partplate_list().get_curr_plate();
if (curr_plate) {
    this->task_bed_type = bed_type_to_gcode_string(plate_data.is_valid ? plate_data.bed_type : curr_plate->get_bed_type(true));
}
```

`get_bed_type(true)` (S5, line 178) returns the plate's own `curr_bed_type`, else the project's
`curr_bed_type`, else `btDefault`. `bed_type_to_gcode_string` (S3, `PrintConfig.hpp` ~line 464)
maps the enum to the wire string:

| Slicer name (`curr_bed_type`) | Enum | Wire `bed_type` |
|---|---|---|
| Cool Plate | `btPC` | `cool_plate` |
| Engineering Plate | `btEP` | `eng_plate` |
| High Temp Plate | `btPEI` | `hot_plate` |
| Textured PEI Plate | `btPTE` | `textured_plate` |
| Supertack Plate | `btSuperTack` | `supertack_plate` |
| Default Plate, or anything else | `btDefault` | `unknown` |

So for sheets-04 (sliced with `curr_bed_type = Cool Plate`), Studio's GUI would send
`"bed_type": "cool_plate"`. Studio never sends `"auto"` on this path; `"auto"` is only the
struct's starting value in S7 (`task_bed_type = "auto"`), which `process()` overwrites when a
plate exists. In `SelectMachine.cpp` (S4) the dialog first passes `MachineBedTypeString[0]`
(`"pc"`) and the `"auto"` entry of that list is commented out; `process()` then replaces it.

S13's capture agrees with the source: it shows `"bed_type":"textured_plate"`, and its overlay
test shows `task_bed_type="textured_plate"` changes the wire value from `"auto"` to
`"textured_plate"` verbatim. One line in S13's field table says the value is "One of the
`MachineBedTypeString` values" (`pc`, `pei`, ...). The source (S1, S3) and S13's own capture
both show the gcode strings instead, so that table line looks wrong.

**The other flags, as Studio's dialog sets them (S4, ~lines 3371–3383):**

```cpp
m_print_job->set_print_config(MachineBedTypeString[0], (bed_leveling=="on"), (flow_cali=="on"), false,
    timelapse_option, true, m_ext_change_assist, bed_leveling getValueInt, flow_cali getValueInt,
    nozzle_offset_cali getValueInt, (m_pa_value_switch->GetValue()?0:1));
```

So `vibration_cali` is always `false` and `layer_inspect` is always `true` from this dialog.
The three-way options (off / on / auto) go out twice: a bool that is true only for "on", and an
int (0 off, 1 on, 2 auto). bambuddy (S17) documents the same encoding.

### The full field set, side by side

Studio column: what the stock plugin puts on the wire (S13 capture and field table), with values
from Studio's source for a GUI send. Ours: `buildProjectFileCommand` in
[`tools/bambu/src/backends/mqtt.ts`](../../tools/bambu/src/backends/mqtt.ts).

| Field | Studio GUI + stock plugin | Ours | Note |
|---|---|---|---|
| `sequence_id` | `"20001"` on a fresh process, then counts up | `"0"` | S13: stock uses 20000–29999; reusing one across restarts got `err_code` 84033544 |
| `command` | `project_file` | same | |
| `param` | `Metadata/plate_<n>.gcode` | same | |
| `project_id`, `profile_id`, `task_id`, `subtask_id` | `"0"` on LAN | same | bambuddy sends a unique id here (S17 cites its #1042) |
| `subtask_name` | project name | same idea | |
| `file` | basename of the `.3mf` | **missing** | S13: on an upload it matches the uploaded name |
| `url` | `brtc://emmc/<name>` after a port-6000 upload; `ftp://<name>` right after an FTPS upload; `ftp:///<name>` for a file pushed earlier | `ftp:///<name>` | S13: firmware accepts both FTP spellings |
| `url_enc` | only when the printer is not in Developer Mode | absent | fine for us in Developer Mode (S14) |
| `md5` | always the literal `"from_sd_card"` | `""` | S13, stock plugin versions 02.05.00–02.08.02 |
| `bed_type` | plate string from the 3mf, e.g. `cool_plate` | **`"auto"`** | the main suspect |
| `bed_leveling` / `auto_bed_leveling` | bool + int (0/1/2) | bool only | |
| `flow_cali` / `extrude_cali_flag` | bool + int (0/1/2) | bool only | |
| `nozzle_offset_cali` | int (0/1/2), two-nozzle printers | **missing** | |
| `extrude_cali_manual_mode` | int; omitted when -1 | **missing** | |
| `vibration_cali` | `false` from the GUI dialog | `true` | |
| `layer_inspect` | `true` from the GUI dialog | `false` | |
| `timelapse` | per dialog | `false` | |
| `cfg` | string bitmask: bit 0 external-spool change assist, bit 2 internal timelapse (S13) | absent | bambuddy (S17) omits it on purpose; S13 lists it as sent |
| `use_ams` | true when AMS is used | `true` | |
| `ams_mapping` | flat int array, one per project filament, -1 for unused | `[3]` | |
| `ams_mapping2` | `[{ams_id, slot_id}]`, `255/255` for none or the external spool | **missing** | sent as `[]` when no AMS (S14) |
| `nozzle_mapping` | int array, **only on multi-nozzle printers** | **missing** | from the printer's own auto-mapping reply (S13) |
| `slicer_uid` | LAN MQTT only, newer plugins | absent | |
| `job_type`, `skip_objects`, `plate_idx`, `bed_temp`, `job_id` | **cloud** variant only, not LAN | absent | S13: the cloud sends `bed_temp` instead of `bed_type` |

S13's capture, for reference (single-nozzle P2S in Developer Mode, so no `nozzle_mapping`):

```json
{"print":{"sequence_id":"20001","command":"project_file","param":"Metadata/plate_1.gcode","project_id":"0","profile_id":"0","task_id":"0","subtask_id":"0","subtask_name":"test","file":"test.gcode.3mf","url_enc":"…","md5":"from_sd_card","bed_type":"textured_plate","bed_leveling":false,"flow_cali":false,"vibration_cali":false,"layer_inspect":true,"timelapse":true,"use_ams":true,"ams_mapping":[3,-1,-1],"ams_mapping2":[{"ams_id":0,"slot_id":3},{"ams_id":255,"slot_id":255},{"ams_id":255,"slot_id":255}],"auto_bed_leveling":0,"cfg":"4","extrude_cali_flag":0,"extrude_cali_manual_mode":0,"nozzle_offset_cali":2}}
```

Hedge: S13's captures are from a P2S and an N7, not an H2D or X2D. For the two-nozzle fields I
rely on Studio's source and S13's notes, not on a captured X2D frame. bambu-printer-mcp (S18)
says the H2/X2D path uses "project-length `ams_mapping`, parallel `ams_mapping2`, and
H2-compatible calibration flags", which agrees, but it is another client, not a capture.

### Where `"auto"` comes from

OpenBambuAPI (S15) shows `"bed_type": "auto", // Always "auto" for local prints`. ha-bambulab
(S16), bambuddy (S17) and bambu-printer-mcp's H2 path (S18, as a default) all send `"auto"`.
Studio and the stock plugin do not. So "always auto for local prints" is true of several
community clients, and not true of Studio, among the clients I checked.

## Q2. What triggers or suppresses 0500-8051

**The message.** S12:

```json
"ecode": "05008051", "intro": "Detected build plate is not the same as the Gcode file. Please adjust slicer settings or use the correct plate."
```

83918929 in decimal is `0x05008051`, so this is the code our job stopped on.

**The check is a printer option, not a job field.** Studio shows "Build Plate Detection" in the
printer's options dialog (S8) with the caption "Identifies the type and position of the build
plate on the heatbed. Pausing printing if a mismatch is detected." and, on older layouts,
"Pauses printing when the detected build plate type does not match the selected one." It is
turned on and off with an `xcam_control_set` command (S8):

```json
{"xcam":{"command":"xcam_control_set","sequence_id":"…","module_name":"buildplate_marker_detector","control":false,"enable":false,"print_halt":true}}
```

Plate *alignment* is a separate module, `plate_offset_switch`, read from report `cfg` bit 20
(S8). Our printer reports `xcam.buildplate_marker_detector: true` for both jobs, so type
detection was on both times.

**What the job contributes.** I found no `PrintParams` field and no `project_file` key for
skipping the check per job, among the fields in S6 and S13. The only job-side input that names a
plate is `bed_type`. The firmware's own comparison is closed source, so the rest is inference:

- With `bed_type: "cool_plate"` (Studio), the job printed with plate `P0101` on the bed.
- With `bed_type: "auto"` (ours), the same plate gave 0500-8051.
- So either `"auto"` makes the firmware compare against something other than the 3mf's plate
  (a default, or "unknown"), or one of the other differences matters. No source says which.
  The forum (S20) says the gcode is "coded" for a plate type, which fits a firmware that reads
  the type from the job, but that post is about slicer settings, not MQTT.

**`curr_bed_type` in the 3mf and gcode.** The X2D start gcode (S11) uses `curr_bed_type` only
to adjust a Z offset (`{if curr_bed_type=="Textured PEI Plate"} G29.1 Z{-0.003}`). The detection
itself runs as `M972 S19 P0 ;heatbed detection` and
`M972 S34 P0 ;print plate deviation detection`. The start gcode has a commented-out `;M1002 set_flag build_plate_detect_flag=1`. So
the gcode does not visibly pass the plate type to the check; whether the firmware reads it from
the 3mf's config when `bed_type` is `"auto"` is unknown.

**A twist: the X2D profile says Cool Plate is not supported.** S11:
`"not_support_bed_type": "Cool Plate"`, `"default_bed_type": "Textured PEI Plate"`. H2D, H2D
Pro, H2S, P2S and A2L list the same. Users on S21 unlocked Cool Plate on an H2D by deleting that
line. Yet Studio's GUI sent a Cool Plate job that printed. Two readings, neither proven: the
firmware treats the physical plate `P0101` as a match for `cool_plate`; or the GUI sent a
different value than the source suggests (for example if the 3mf was re-sliced on open). A
GUI-side capture of the sheets-04 send would settle it.

**Does `"auto"` fall back to a default plate?** Unknown. No source says. The X2D's profile
default is Textured PEI Plate; if the firmware used that, a Cool Plate on the bed would
mismatch, which would fit what we saw. This is a guess built on the profile, not a source.

**Per-job skip.** None found in the job fields. Two ways out exist, both from Studio:

- The printer-wide toggle above (turns the check off for every print).
- After the pause, the error's own buttons. S12's action list for 05008051 is `[28, 27, 5]`,
  which S10 names `PROBLEM_SOLVED_RESUME`, `IGNORE_RESUME` and `STOP_PRINTING`. "Ignore"
  sends (S9, `command_hms_ignore`):

  ```json
  {"print":{"command":"ignore","err":"<error code>","param":"reserve","job_id":"<job id>","sequence_id":"…"}}
  ```

  and "resume" sends the same with `"command":"resume"`. The `err` value is the error code as
  a decimal string (`std::to_string` of an int), which I infer from the code, not a capture.

**S22 (snippet only):** a search summary says the check can be turned off in the Device tab,
and lists QR marker, lidar and caching causes. I could not confirm the details on a fetched
page, so treat it as a lead.

## Q3. What `device.plate.cur_id` values mean

No source I found decodes them.

- S14 names the fields only: `base` "Plate base type code", `mat` "Plate material code",
  `cur_id` / `tar_id` "Current / target plate id", `cali2d_id` "2D calibration id". No value
  table.
- ioBroker (S19) gives the same generic labels.
- ha-bambulab's recorded test data (S16) shows `{base:4, cur_id:"P0101", mat:1}` for an X2D,
  and `P0101` for the H2D and H2S too; an H2C shows `base:6, cur_id:"P0102"`; a P2S shows
  `"00000"`. None of those files says which physical plate that is.
- Studio's source (S9) parses neither `cur_id` nor `base` in `DeviceManager.cpp`, the file I
  read.

So `P0101` is "whatever plate this printer family usually has fitted", by pattern, and that is
all the evidence supports. `tar_id` being empty in both of our reports fits it being the
job's target plate, but no source says so.

## Q4. What else Studio does before a send

From S1 and S13, things our client does not do yet:

1. **An access-code check before the real send.** On a LAN send, Studio first tries a small
   "verify_job" send over FTPS (and a port-6000 connect when the printer supports eMMC
   printing). If both fail it stops with "access code is invalid".
2. **A storage check.** Studio refuses with "Storage needs to be inserted before printing via
   LAN." unless the printer has an SD card or supports eMMC printing (`fun2` bit 0). We added a
   card check in #497.
3. **eMMC upload when supported.** When `fun2` bit 0 is set, Studio uploads over TLS port 6000
   and starts with `brtc://emmc/<name>` (S13; also the earlier consolidated finding in the
   brief). We use FTPS to the SD card.
4. **`nozzle_mapping` from the printer.** On multi-nozzle printers Studio asks the printer for
   its automatic nozzle mapping and sends the result (S13).
5. **A `sequence_id` in the 20000–29999 range**, unique per process (S13).

**The report differences in the brief, decoded where a source allows** (bit numbers count from
the low end; S9 `get_flag_bits` confirms the order):

| Field | Studio job → ours | What it means | Source |
|---|---|---|---|
| `aux` | `2800004` → `2801004` | bit 12 changed: the SD card state. Studio's job ran with **no** card (it used eMMC); ours ran with a card | S9 |
| `job_attr` | 2 → 18 | Studio reads bits 4–7 as a job state; 0 vs 1. The low bits match. Likely job state, not an input | S9 |
| `cfg` | `5C1…` → `4C1…` | bit 40 changed. Not parsed in the Studio files I read. Bit 20 (alignment detection) is on in both | S8, S9 |
| `fun` | `4402…` → `4002…` | bit 58 changed. Not parsed in the Studio files I read | S9 |
| `2D.cond` | 15 → 14 | bit 0 changed. Not decoded by any source I found | — |
| `sdcard` | False → True | same as `aux` bit 12 | S9 |

So one difference is not a payload field at all: **the Studio job came from eMMC with no SD
card fitted, and ours came from the SD card.** That is a second confound alongside `bed_type`.

## Design

What `buildProjectFileCommand` and `print send` could change.

| Option | Pros | Cons | Implications |
|---|---|---|---|
| **A. Send `bed_type` from the 3mf.** Read `curr_bed_type` from the plate's config in the 3mf, map it with Studio's table (`Cool Plate` → `cool_plate`, ...), and refuse to send if it is missing or maps to `unknown`. | One field; matches Studio's source exactly; one send tests the main hypothesis cleanly. | Fixes only the most likely cause. If the pause was caused by something else, we learn that but still pause. | Makes the 3mf the single source of the plate type. The refusal turns a silent mismatch into a clear error before the printer moves. |
| **B. A, plus Studio parity for the rest.** Add `file`, `md5: "from_sd_card"`, `ams_mapping2`, `nozzle_mapping` on the X2D, the int modes (`auto_bed_leveling`, `extrude_cali_flag`, `nozzle_offset_cali`, `extrude_cali_manual_mode`), `cfg`, a 20000–29999 `sequence_id`, and Studio's dialog values for `vibration_cali` (false) and `layer_inspect` (true). | Removes every known difference from the stock plugin's output; fewer unknowns on the next odd error. | More code; `nozzle_mapping` needs the printer's auto-mapping reply, a new request; if sent together with A, a success does not say which change fixed it. | Commits us to tracking the stock plugin's field set as the reference. A test can pin our output against S13's capture. |
| **C. Turn off `buildplate_marker_detector`.** | Removes the pause for any `bed_type`. | Drops a safety check for every print, Studio's included; hides a real wrong-plate mistake; changes printer state that is Omar's. | A printer setting, not a code fix. Goes against fixing the cause. Only as a stated last resort with Omar's yes. |
| **D. Keep `"auto"`; add a `print ignore` verb** that sends Studio's `ignore` command for 0500-8051 after a person checks the plate. | Works whatever the cause; mirrors Studio's own button. | Every print pauses and needs a person; it routes around the cause. | Useful as a recovery tool even with A, but not as the fix. |

**Recommendation:** B, built in two steps: ship A alone first and test one send, so the result
shows whether `bed_type` was the cause, then add the parity fields in the next change.

Before trusting A, one more check would help: capture what Studio's GUI actually sends for a
Cool Plate job on the X2D (a broker-side log or the plugin's own log), since the X2D profile
says Cool Plate is not supported and the source alone cannot prove the GUI sent
`"cool_plate"`. If both A and B still pause, the next suspect is the storage difference (SD
card vs eMMC).
