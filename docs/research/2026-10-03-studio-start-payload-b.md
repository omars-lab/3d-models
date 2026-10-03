---
date: 2026-10-03
produced-by: researcher B (Claude), curl of raw GitHub files / gh search code / gh api / gh issue view / WebSearch / WebFetch
feeds:
  - '[[first-party-dispatch]]'
---

# What Bambu Studio sends to start a LAN print on an X2D, and what decides the plate check

This is researcher B's raw record for one question. What does Bambu Studio publish in
`print.project_file` on an X2D or H2D? And what makes the printer stop with HMS `0500-8051`,
"Detected build plate is not the same as the Gcode file"? Researcher A is working on the same
question on their own. A third pass is meant to check the two against each other.

No printer was contacted for this. All the facts about our own printer come from the brief.

## What I checked

Every source is marked **fetched** (I read the file or page) or **snippet** (I only saw a search
result). Bambu Studio files were read from the `master` branch on 2026-10-03.

### Bambu Studio source (bambulab/BambuStudio)

1. **PrintJob.cpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/Jobs/PrintJob.cpp
   - Around line 209, the bed type comes from the slice's plate, not from the send dialog:
     `this->task_bed_type = bed_type_to_gcode_string(plate_data.is_valid ? plate_data.bed_type : curr_plate->get_bed_type(true));`
   - Lines 222 to 251 are a LAN check before the send. If the printer can print from eMMC, it opens
     a test link to `bambu:///local/<ip>?port=6000&user=bblp&passwd=<code>`. It also tries an FTPS
     upload with the project name `verify_job`. Both check that the access code works.
   - Lines 272 to 293 copy the job fields into the plugin's PrintParams: plate_index,
     task_bed_leveling, task_flow_cali, task_vibration_cali, task_layer_inspect,
     task_record_timelapse, task_timelapse_use_internal, nozzle_mapping, ams_mapping, ams_mapping2,
     ams_mapping_info, nozzles_info, connection_type, task_use_ams, task_bed_type, print_type,
     auto_bed_leveling, auto_flow_cali, auto_offset_cali, extruder_cali_manual_mode,
     task_ext_change_assist, try_emmc_print.
   - Around line 850, a LAN send calls the plugin's `start_local_print`.
2. **PrintJob.hpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/Jobs/PrintJob.hpp
   - Lines 98 to 116: `set_print_config` takes bed_type, bed_leveling, flow_cali,
     vabration_cali, record_timelapse, layer_inspect, ext_change_assist, auto_bed_leveling,
     auto_flow_cali, auto_offset_cali and extruder_calit_manual_mode. The last four are ints.
   - Lines 93 to 96: `auto_bed_leveling{0}`, `auto_flow_cali{0}`, `auto_offset_cali{0}`,
     `extruder_cali_manual_mode = -1` are the defaults.
3. **PrintConfig.hpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.hpp
   - Line 296: `enum BedType { btDefault = 0, btPC, btEP, btPEI, btPTE, btSuperTack, btCount }`.
   - Lines 464 to 490, `bed_type_to_gcode_string`: SuperTack gives `"supertack_plate"`, PC (Cool
     Plate) gives `"cool_plate"`, EP gives `"eng_plate"`, PEI gives `"hot_plate"`, PTE (Textured
     PEI) gives `"textured_plate"`, and anything else gives `"unknown"`. There is no `"auto"` in
     this map.
4. **SelectMachine.cpp** (the send dialog), fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/SelectMachine.cpp
   - Lines 165 to 180: `MachineBedTypeString = {"pc", "pe", "pei", "pte", "suprtack"}`. An
     `"auto"` entry is there but commented out.
   - Lines 3346 to 3352: ams_mapping, ams_mapping2 and ams_mapping_info are set. Then
     `task_nozzle_mapping` is set from `obj_->get_nozzle_mapping_result()->GetNozzleMappingJson()`,
     but only when that JSON is not empty.
   - Lines 3354 to 3359: `build_nozzles_info(...)` "for multi extruders printers"; `has_sdcard`;
     `could_emmc_print = obj_->is_support_print_with_emmc`.
   - Lines 3370 to 3382: `set_print_config` is called with, in order,
     `MachineBedTypeString[0]`, `bed_leveling == "on"`, `flow_cali == "on"`, `false`,
     `timelapse_option`, `true`, `m_ext_change_assist`, `bed_leveling.getValueInt()`,
     `flow_cali.getValueInt()`, `nozzle_offset_cali.getValueInt()` and
     `m_pa_value_switch ? 0 : 1`. So the dialog passes `"pc"` as the bed type here. PrintJob then
     overwrites it with the slice's plate (source 1). Vibration is always false here. Layer
     inspect is always true.
   - Lines 3385 to 3400: use_ams is true when the mapping uses the AMS only, false when it uses
     only the external spool, and true when it uses both.
   - Around lines 5490 to 5500: the dialog shows the slice plate's bed type to the user.
5. **bambu_networking.hpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/Utils/bambu_networking.hpp
   - Lines 229 to 281: the PrintParams struct. Besides the fields above, it has svc_context,
     slicer_uid and queue_plate_id. The plugin that turns PrintParams into MQTT JSON is closed
     source. So Studio's source alone does not show the wire format.
6. **DevPrintOptions.cpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceCore/DevPrintOptions.cpp
   - Lines 110 to 120: one printer key, `xcam.buildplate_marker_detector`, sets both
     `m_buildplate_mark_detection` and `m_buildplate_type_detection`. So one switch turns both the
     marker check and the plate-type check on or off.
   - Lines 138 to 146: the switch commands use `module_name` `"buildplate_marker_detector"` and
     `"plate_offset_switch"` (alignment). Line 84: the xcam `cfg` bit 20 is plate alignment.
   - Lines 184 to 225: the `print.cfg` bits Studio reads are 8 to 10 (speed), 12 (first layer),
     13 to 15 (AI), 16 (auto recovery), 22 (sound), 23 (tangle), 24 (blob), 32 and 33 (idle heat),
     36 and 37 (purify), 43 and 44 (smart blob). Studio does not decode bit 40 of `cfg` or bit 58
     of `fun`. Those are the two bits that differed between Studio's job and ours.
7. **DevBed.cpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceCore/DevBed.cpp
   - It parses bed temperatures only. Studio does not read `device.plate`.
   - A `gh search code` for `cur_id` and `cali2d_id` in BambuStudio found nothing that maps plate
     ids. (gh search, snippet-level.)
8. **DeviceErrorDialog.hpp / .cpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceErrorDialog.hpp
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceErrorDialog.cpp
   - Action 27 is `IGNORE_RESUME`, "Ignore this and Resume", and calls `command_hms_ignore`.
     Action 28 is `PROBLEM_SOLVED_RESUME` and calls `command_hms_resume`. Action 5 is
     `STOP_PRINTING` and calls `command_hms_stop`.
9. **DeviceManager.cpp**, fetched.
   https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceManager.cpp
   - Lines 1460 to 1496. The ignore command is:
     ```json
     {"print":{"command":"ignore","err":"<error_str>","param":"reserve","job_id":"<job_id>","sequence_id":"<n>"}}
     ```
     Resume and stop have the same shape with `"resume"` and `"stop"`. Ignore and resume return
     early when `check_resume_condition()` is true.
10. **hms_en_20P.json and hms_action_20P.json**, fetched. 20P is the X2D serial prefix, which
    matches our printer.
    https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/hms/hms_en_20P.json
    https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/hms/hms_action_20P.json
    - `05008051`: "Detected build plate is not the same as the Gcode file. Please adjust slicer
      settings or use the correct plate." Actions `[28, 27, 5]`: resume, ignore and resume, stop.
    - Nearby codes: `05008061` (no plate), `05008062` (marker not detected), `0500808C` (plate
      offset), `03008049` ("The current plate is invalid"), `0C00030000020019` (Vision Encoder
      Plate).
    - `gh search code` also found `05008051` in the action files for 094 (H2D), 22E, 093, 239 and
      31B. (Snippet-level for those five.)
11. **X2D machine start G-code template**, fetched.
    https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/machine/Bambu%20Lab%20X2D%200.4%20nozzle%20template%20machine_start_gcode.json
    - The first lines are comments: `;M1002 set_flag extrude_cali_flag=1`,
      `;M1002 set_flag g29_before_print_flag=1`, `;M1002 set_flag auto_cali_toolhead_offset_flag=1`,
      `;M1002 set_flag build_plate_detect_flag=1`. They are commented out, so the G-code does not
      set these flags itself. Something else sets them.
    - Lines 101 to 115, "detection start": `M972 S19 P0 ;heatbed detection`,
      `M972 S31 P0 ;toolhead camera dirt detection`,
      `M1002 gcode_claim_action : 73 ; Build plate alignment detection`,
      `M972 S34 P0 ;print plate deviation detection`.
    - The template uses `curr_bed_type` only to nudge the Z offset for the Textured PEI plate. No
      line passes the plate type to `M972`.
    - `gh search code build_plate_detect_flag` found the same flag in the A2L, H2C, H2D, H2D Pro
      and P2S templates. (Snippet-level for those.)
12. **OrcaSlicer**, snippet. `gh search code bed_type_to_gcode_string --owner OrcaSlicer` shows the
    same line in its PrintJob.cpp:
    `this->task_bed_type = bed_type_to_gcode_string(plate_data.is_valid ? plate_data.bed_type : curr_plate->get_bed_type(true));`
    Its SendMultiMachinePage.cpp also sets `params.task_bed_type = bed_type_to_gcode_string(curr_plate->get_bed_type(true))`.

### Wire captures and third-party clients

13. **open-bamboo-networking, research/08.08-print-abi.md** (ClusterM), fetched.
    https://raw.githubusercontent.com/ClusterM/open-bamboo-networking/master/research/08.08-print-abi.md
    - A P2S capture of a Studio start (single nozzle). Fields: `sequence_id "20001"`, `param`,
      `project_id`/`profile_id`/`task_id`/`subtask_id` all `"0"`, `subtask_name`,
      `file "test.gcode.3mf"`, `url`, `md5 "from_sd_card"`, `bed_type "textured_plate"`,
      `bed_leveling false`, `flow_cali false`, `vibration_cali false`, `layer_inspect true`,
      `timelapse true`, `use_ams true`, `ams_mapping [3,-1,-1]`,
      `ams_mapping2 [{"ams_id":0,"slot_id":3},{"ams_id":255,"slot_id":255},{"ams_id":255,"slot_id":255}]`,
      `auto_bed_leveling 0`, `cfg "4"`, `extrude_cali_flag 0`, `extrude_cali_manual_mode 0`,
      `nozzle_offset_cali 2`.
    - Its field table says `bed_type` "defaults to 'auto'". Its worked example shows that setting
      `task_bed_type="textured_plate"` changes the plugin's output from `"auto"` to
      `"textured_plate"`. I read this as: the plugin writes `"auto"` only when Studio hands it an
      empty bed type. Studio's own code (source 1) always hands it the slice's plate.
    - `nozzle_mapping` is a flat int array, sent only on multi-extruder printers.
    - `cfg` bit 0 is ext_change_assist; bit 2 is "timelapse to internal storage".
    - Keys go out in alphabetical order. With Developer Mode on, a plain `url` is accepted.
    - Cloud starts add `job_id` (int), `job_type: 1`, `design_id`, `model_id`, `dev_id`,
      `plate_idx`, `bed_temp` in place of `bed_type`, `skip_objects: []`, and `timestamp`. A LAN
      start does not send these.
    - URL forms: `ftp://` vs `ftp:///` depend on the case; `brtc://emmc/<name>` makes the printer
      look in the USB drive and then the eMMC cache; `file:///media/usb0/...` is also seen. A
      Studio LAN start uploads over port 6000 and sends `brtc://`.
    - Starting while a job is already running gives `0500_4004`.
14. **open-bamboo-networking, research/12.01.04-fields-device.md**, fetched.
    https://raw.githubusercontent.com/ClusterM/open-bamboo-networking/master/research/12.01.04-fields-device.md
    - `device.plate.base` is "Plate base type code"; `mat` is "Plate material code"; `cur_id` and
      `tar_id` are "Current / target plate id"; `cali2d_id` is "2D calibration id". It gives no
      table of values.
15. **open-bamboo-networking, research/12.01.01-fields-job.md**, fetched.
    https://raw.githubusercontent.com/ClusterM/open-bamboo-networking/master/research/12.01.01-fields-job.md
    - `job_attr` is a bitfield. Studio reads `get_flag_bits(jobAttr, 4, 4)` as the job state.
      Our 18 vs Studio's 2 differ in bit 4, which is inside that state nibble. So that difference
      is most likely "paused" vs "finished", not a setting.
16. **open-bamboo-networking, research/12.12-xcam.md**, fetched.
    https://raw.githubusercontent.com/ClusterM/open-bamboo-networking/master/research/12.12-xcam.md
    - `xcam.xcam_control_set` takes `module_name` (including `buildplate_marker_detector` and
      `plate_offset_switch`), `control` (bool, new protocol), `enable` (bool, old protocol),
      `print_halt`, and an optional `halt_print_sensitivity`.
17. **bambuddy issue #1192**, "X2D + FTS: Bambuddy-launched prints route to wrong nozzle", fetched
    with `gh issue view 1192 --repo maziggy/bambuddy`.
    https://github.com/maziggy/bambuddy/issues/1192
    - This is the only **X2D** Studio capture I found. The user reports firmware 01.01.00.00. Ours
      is 01.02.x. bambuddy logged it from the request topic. Test A, a two-color print with the
      filaments on different nozzles:
      ```json
      {"ams_mapping": [1, 0], "ams_mapping2": [{"ams_id": 0, "slot_id": 1}, {"ams_id": 0, "slot_id": 0}],
       "auto_bed_leveling": 2, "bed_leveling": false, "bed_type": "textured_plate", "cfg": "0",
       "command": "project_file", "extrude_cali_flag": 2, "extrude_cali_manual_mode": 0,
       "file": "Cube + Cube.gcode.3mf", "flow_cali": false, "layer_inspect": true,
       "md5": "BCF8FEA788082C764F3C8CD977481C0B", "nozzle_offset_cali": 2,
       "param": "Metadata/plate_1.gcode", "profile_id": "0", "project_id": "0",
       "sequence_id": "20001", "subtask_id": "0", "subtask_name": "Cube + Cube", "task_id": "0",
       "timelapse": true, "url": "brtc://emmc/Cube + Cube.gcode.3mf", "use_ams": true,
       "vibration_cali": false}
      ```
    - There is no `nozzle_mapping` key, even on this dual-nozzle printer. (The keys are in
      alphabetical order, and it would sit between `md5` and `nozzle_offset_cali`.)
    - `md5` is a real hash here, not `"from_sd_card"`. That disagrees with the P2S capture and with
      the brief's earlier research. It may depend on the Studio version or on the eMMC path.
    - The maintainer's reading of Test A vs Test B: "Studio doesn't carry per-filament nozzle
      routing in project_file at all. The tool-routing must be inside the 3MF gcode". They also
      list the fields where bambuddy differs from Studio: "auto_bed_leveling, extrude_cali_flag,
      bed_type, and the task-identity fields".
18. **bambuddy backend/app/services/bambu_mqtt.py** (maziggy/bambuddy, `main`), fetched.
    https://raw.githubusercontent.com/maziggy/bambuddy/main/backend/app/services/bambu_mqtt.py
    - Lines 5963 to 6240, its own start builder. It sends `sequence_id "20000"`,
      `url ftp://{filename}`, `file`, `md5 ""`, **`bed_type "auto"`**, `timelapse`, `bed_leveling`
      (true only for "on") plus `auto_bed_leveling` (int), `flow_cali` (bool) plus
      `extrude_cali_flag` (int), `extrude_cali_manual_mode 0`, `nozzle_offset_cali` (dual-nozzle
      only), and task, subtask and project ids made unique from the epoch time. It sends no `cfg`.
    - Comments in the code, kept with their own wording:
      - "BambuStudio request-topic capture from a real H2D sends plain booleans."
      - `use_ams` must stay a bool. An H2D Pro reads an int there as a nozzle index.
      - In a flat `ams_mapping`, use -1 for the 254/255 slots, or the printer raises `0700_8012`.
      - Dual-nozzle external spool: ams_id 254 is the deputy (left) nozzle, 255 the main (right).
      - Ids hard-coded to "0" made watchers think the job was a continuation. A P1S treated a
        fresh start as a continuation of the last FAILED job (bambuddy #1042, #1011).
      - Never start while busy, or `0500_4004` (#2598).
      - "No cfg: it is the printer's device-config bitmask" (#3040).
      - An H2D Pro can take 80 to 210 s to acknowledge `project_file`.
    - bambuddy also reads `curr_bed_type` from the slice's slice_info.config, but for display.
19. **ha-bambulab pybambu/commands.py**, snippet (`gh search code`). Has `"bed_type": "auto"`. Its
    tests read `Metadata/plate_N.json` with `{"bed_type":"textured_plate"}`.
20. **bambulabs_api mqtt_client.py**, snippet (`gh search code`). Has `"bed_type": "textured_plate"`
    hard-coded.

### Forum and wiki

21. forum.bambulab.com, "The current build plate is not the same as in g-code, redux", fetched.
    https://forum.bambulab.com/t/the-current-build-plate-is-not-the-same-as-in-g-code-redux/65448
    - ovityons (2024-03-16): the error came from a Cool Plate chosen in Studio while a PEI plate
      was on the bed. The fix is to match the plate type, or to uncheck "Enable detection of build
      plate position" under Device > print options. jdedwards confirmed that matching the plate
      fixed it.
22. forum.bambulab.com, "...not the same as in g-code on second print", post 2, fetched.
    https://forum.bambulab.com/t/the-current-build-plate-is-not-the-same-as-in-g-code-on-second-print/161622/2
    - JayZay (2025-04-15) mentions an "Auto Plate Type" setting. The post does not say what it does
      on the wire.
23. forum.bambulab.com, "Build plate detection" (P2S), fetched.
    https://forum.bambulab.com/t/build-plate-detection/206297
    - maxim3D (2025-11-06): "You can just turn off plate detection, so with custom plates it wont
      give you an error anymore."
24. Snippets only, all about the same error and its fixes (match the plate, or turn detection off):
    - https://forum.bambulab.com/t/the-current-build-plate-is-not-the-same-as-in-g-code-error/39104
    - https://forum.bambulab.com/t/the-current-build-plate-is-not-the-same-as-in-g-code/36736
    - https://forum.bambulab.com/t/current-build-plate-is-not-the-same-in-the-gcode/33769
    - https://forum.bambulab.com/t/changing-type-of-build-plate-does-not-change-g-code/34453
    - https://forum.bambulab.com/t/build-plate-error/103844
    - https://forum.drucktipps3d.de/forum/thread/29390-the-current-build-plate-is-not-the-same-as-in-the-g-code-was-tun/
25. WebSearch for `cur_id` with `P0101` or `P0201`: snippet results only.
    - https://forum.bambulab.com/t/h2d-build-plate/156314
    - https://forum.bambulab.com/t/where-is-the-plate-detector/234568
    - https://forum.bambulab.com/t/engineering-print-plate-not-recognized-marker-was-not-detected/232948
    - https://wiki.bambulab.com/en/x1/troubleshooting/hmscode/0C00_0300_0002_000C
    - None of them names a plate id.

**The set checked**, for any "none of them" claim below: Bambu Studio (sources 1 to 11), OrcaSlicer
(12, snippet), open-bamboo-networking (13 to 16), bambuddy (17, 18), ha-bambulab (19, snippet),
bambulabs_api (20, snippet), and the forum and wiki pages in 21 to 25. I did not check Pandar,
bamdude or OpenBambuAPI.

## Answers

### 1. The full field set Studio sends on an X2D or H2D

The best evidence is the X2D capture in bambuddy #1192 (source 17). It agrees in shape with the P2S
capture (source 13) and with Studio's code (sources 1 to 5). Here are Studio's fields next to ours.

| Field | Studio on X2D (source 17) | Ours | Note |
|---|---|---|---|
| `command` | `"project_file"` | same | |
| `sequence_id` | `"20001"` | `"0"` | Studio counts up. Probably harmless. |
| `param` | `"Metadata/plate_1.gcode"` | same | |
| `file` | `"<name>.gcode.3mf"` | missing | Sent by every Studio capture checked. |
| `url` | `"brtc://emmc/<name>"` | `"ftp:///<name>"` | Studio uploads over port 6000 to eMMC. |
| `md5` | real hash (X2D) or `"from_sd_card"` (P2S) | `""` | The two captures disagree. |
| `subtask_name` | name without extension | same | |
| `project_id`, `profile_id`, `task_id`, `subtask_id` | `"0"` | `"0"` | bambuddy makes these unique (source 18). |
| `bed_type` | **`"textured_plate"`** (the slice's plate) | **`"auto"`** | See question 2. |
| `bed_leveling` | `false` | `true` | Bool. Studio sends false and puts the mode in the int. |
| `auto_bed_leveling` | `2` | missing | Int: 0 off, 1 on, 2 auto. |
| `flow_cali` | `false` | `true` | Bool, as above. |
| `extrude_cali_flag` | `2` | missing | Int, as above. |
| `extrude_cali_manual_mode` | `0` | missing | |
| `nozzle_offset_cali` | `2` | missing | Dual-nozzle only (source 18). |
| `vibration_cali` | `false` | `true` | Studio's dialog always passes false (source 4). |
| `layer_inspect` | `true` | `false` | Studio's dialog always passes true. |
| `timelapse` | `true` (user choice) | `false` | |
| `use_ams` | `true` | `true` | Must stay a bool (source 18). |
| `ams_mapping` | `[1, 0]` | `[3]` | Flat; -1 for an unused slot. |
| `ams_mapping2` | `[{"ams_id":0,"slot_id":1}, ...]` | missing | |
| `cfg` | `"0"` (X2D), `"4"` (P2S) | missing | Bit 0 ext_change_assist, bit 2 timelapse to internal storage. |
| `nozzle_mapping` | not present | missing | Studio sets it only when the mapping JSON is non-empty. Not in the X2D capture. |
| `job_type`, `skip_objects`, `job_id`, `bed_temp`, `plate_idx` | not present | missing | Cloud starts only (source 13). |

Bed type spellings are `cool_plate`, `eng_plate`, `hot_plate`, `textured_plate`,
`supertack_plate` and `unknown` (source 3). Studio never sends `"auto"` itself. The plugin falls
back to `"auto"` only when it is handed an empty bed type (source 13).

### 2. What triggers or suppresses 0500-8051

**The likely trigger is our `bed_type: "auto"`.** This is an inference, not a proven fact. Here is
the chain:

- Studio always sends the slice plate's type (`"cool_plate"` for our sheets), taken from the slice
  (sources 1, 3, 12). The Studio GUI send of sheets-04 printed with no pause. That send would have
  carried `"cool_plate"`, by this code path. I did not see that send on the wire.
- Our send carried `"auto"` and paused with 0500-8051. The plate, the slice settings and the
  detector setting were the same.
- The X2D start G-code runs `M972 S19 P0 ;heatbed detection` and passes no plate type to it
  (source 11). So the firmware must compare what the camera sees against a value it holds from
  somewhere else. The `project_file` command is the obvious candidate. The `.3mf` metadata
  (`Metadata/plate_1.json` `bed_type`, slice_info `curr_bed_type`) is the other one. Both were the
  same in the two sends, while `bed_type` in the command was not. That points at the command.
- The commented flag lines at the top of the start G-code (source 11) list
  `build_plate_detect_flag` next to `extrude_cali_flag` and `g29_before_print_flag`. Those two
  are set by the command's calibration fields. This hints that the firmware sets the plate flags
  from the job too. It is a hint only.

**Does "auto" fall back to a default plate?** No source says. What we saw fits "auto" being
treated as some plate other than Cool Plate, or as "unknown", which then fails the check. Two
third-party clients send `"auto"` (bambuddy, ha-bambulab; sources 18, 19). bambuddy's maintainer
listed `bed_type` as one of their differences from Studio, but did not tie it to this error. I
found no report of `"auto"` working with plate detection on, and none of it failing, outside our
own printer.

**How to suppress it:**

- **Per printer:** turn off `xcam.buildplate_marker_detector`. In Studio this is "Enable detection
  of build plate position" (sources 6, 16, 21, 23). One switch covers both the marker check and the
  plate-type check (source 6).
- **Per error, after the pause:** the X2D offers "Ignore this and Resume" for 05008051 (source 10).
  It sends `{"print":{"command":"ignore","err":"<code>","param":"reserve","job_id":"<id>"}}`
  (source 9).
- **Per job:** none of the sources checked has a field that skips the plate check for one job. The
  Studio send dialog's options are bed leveling, flow calibration, nozzle offset calibration,
  timelapse and PA. None of them is a plate-check skip (source 4).

### 3. What `cur_id` values like P0101 mean

None of the sources checked maps `cur_id` values to plate names. open-bamboo-networking names the
fields only: `base` "Plate base type code", `mat` "Plate material code", `cur_id`/`tar_id`
"Current / target plate id", `cali2d_id` "2D calibration id" (source 14). Studio does not parse
`device.plate` at all (source 7).

Our own reading, not from any source: `cur_id` was `P0101` under both sends, and the Studio send
printed. So `P0101` is most likely how this printer reads our physical Cool Plate. `tar_id` ("target
plate id") was empty in both reports. But the Studio report was taken at FINISH and ours at PAUSE,
so an empty `tar_id` does not show whether the firmware fills it from the job's `bed_type`. A
`device.plate` report taken mid-print, after a `"cool_plate"` send, would settle that.

### 4. Other checks Studio does before a send

- **Access code check** (source 1): a test link on port 6000 when the printer prints from eMMC, and
  an FTPS upload named `verify_job`.
- **AMS mapping** (source 4): builds `ams_mapping`, `ams_mapping2` and `ams_mapping_info`, and
  sets `use_ams` from whether the mapping uses the AMS, the external spool or both.
- **Nozzle mapping and nozzle info** (source 4): computes an automatic nozzle mapping and
  `nozzles_info` on multi-extruder printers. The X2D capture shows no `nozzle_mapping` on the wire
  (source 17). bambuddy's maintainer concluded the routing lives in the G-code.
- **Storage** (source 4): checks for an SD card and whether the printer can print from eMMC.
- **Plate type shown to the user** (source 4): the dialog shows the slice's plate type, so the user
  can see a mismatch before sending.
- **Busy printer** (source 18): a start while a job runs gives `0500_4004`.
- **Unique ids** (source 18): bambuddy found that `"0"` ids can make a P1S treat a new job as the
  last failed one. Studio's LAN capture still sends `"0"` (source 17), so this is a bambuddy
  finding, not a Studio rule.

**The report differences we saw:**

- `job_attr` 2 vs 18 is bit 4, inside the job-state nibble. That is most likely pause vs finish
  (source 15).
- `aux` and `2D.cond` I could not decode from the sources checked.
- `cfg` 5C10057DA99 vs 4C10057DA99 is bit 40. `fun` 44029FD1930F9CB3 vs 40029FD1930F9CB3 is bit 58.
  Studio decodes neither (source 6). They may follow the job's state or the storage in use.
- `sdcard` False vs True is the USB drive we inserted.

## Design

The options for `buildProjectFileCommand` in `tools/bambu/src/backends/mqtt.ts` and for
`print send`:

| Option | Pros | Cons | Implications |
|---|---|---|---|
| **A. Send the slice's plate as `bed_type`.** Read `curr_bed_type` from the `.3mf` and map it the way Studio does (Cool Plate to `cool_plate`, and so on). Refuse to send when the type is unknown. | A one-field change. It matches every Studio and OrcaSlicer code path checked. `opts.bedType` already exists. Keeps the plate check on, so a wrong plate still stops the print. | Not yet proven on our printer. It rests on an inference (question 2). | The next send of a Cool Plate slice tests it. If it still pauses, the cause is elsewhere (B or C). Needs a test that the map covers every `BedType` value. |
| **B. A, plus Studio's other fields** over FTPS: `file`, `md5` (real hash), `ams_mapping2`, the int modes `auto_bed_leveling` / `extrude_cali_flag` / `nozzle_offset_cali`, `extrude_cali_manual_mode`, `cfg "0"`, and Studio's bool values (`vibration_cali false`, `layer_inspect true`). | Closest to the one X2D capture we have. It removes guesswork from future pauses. | More fields to get wrong. The capture is from firmware 01.01, and ours is 01.02. `md5` and `cfg` disagree between captures. | Our calibration flags change meaning: the ints become the real switch, so `print send` options must map to 0/1/2. More test cases. |
| **C. Move to Studio's transport:** upload over port 6000 to eMMC and send `brtc://emmc/<name>`. | Matches Studio byte for byte, and no USB drive is needed. | Port 6000 is a TLS file service that is not documented here. It is a large new piece of code. It is not needed to fix the plate check. | A separate project. It would make the `sdcard`/storage checks from #497 a fallback path. |
| **D. Suppress the check:** turn `buildplate_marker_detector` off, or auto-send HMS `ignore` on 05008051. | Unblocks a send at once. | It hides real wrong-plate mistakes, which is the check's job. Auto-ignore acts on a paused printer without a person. Turning the detector off changes a printer setting for every client. | Goes against the "look before you print" rule. If used at all, it should be a manual, one-off command. |
| **E. A preflight in `print send`:** compare the slice's plate type with what the printer reports, and refuse on a clear mismatch. | Catches the wrong plate before the upload, not at layer 0. | We cannot read the plate type from `device.plate` yet. No source maps `cur_id` (question 3). | Can only be built after we learn the `cur_id` map from our own sends. Until then, `print send` can at least print the slice's plate type for the person to confirm. |

**Recommendation:** do A now (send the slice's plate as Studio does), with E's "show the slice's
plate before sending" as a small add-on. Take the low-risk parts of B (`file`, the int modes,
`ams_mapping2`) once A's first send confirms the cause.
