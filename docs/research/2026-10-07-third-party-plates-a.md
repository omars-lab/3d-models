---
date: 2026-10-07
feeds:
  - send-plate skill step 4
  - the X2D setup walkthrough
  - a possible bambu options CLI
---

<!-- provenance
date: 2026-10-07
produced-by: Claude (research pass A of two, independent), on Omar's ask "on using non bambu plates ... what options to disable per agreed upon best practices? websearch accordingly"
feeds: send-plate skill step 4, the X2D setup walkthrough, a possible `bambu options` CLI
-->

# Third-party plates on the X2D (research pass A)

The glacier plate is smooth and light blue, with a honeycomb marker strip. Its maker is not
confirmed. On 2026-10-07 the X2D refused to start on it twice:

- **0500-806E**: foreign objects on the bed, though the plate was empty.
- **0500-8062**: plate marker not detected.

In both cases the printer reported `device.plate.cur_id: "P0101"`, `base: 4`, the same as for the
gold Textured PEI plate, which then printed at once.

This file holds pass A's raw findings and its recommendation. A second, independent pass and a
checker come after it.

## Raw findings

### How this was gathered, and its limits

- **Bambu's own sources come first.**
  - The X2D and H2D wiki pages, fetched with curl and a browser user agent. The WebFetch tool got
    HTTP 402 from wiki.bambulab.com.
  - Bambu Studio's source and profiles at commit
    [da8b44e](https://github.com/bambulab/BambuStudio/tree/da8b44ee34dd349f2ae0df3f1cbae366df482354),
    fetched raw.
  - Bambu's HMS error tables for the X2D (serial prefix 20P), also at that commit.
- **Community sources come second.**
  - forum.bambulab.com threads, read through the forum's JSON API (each post fetched in full).
  - Two reverse-engineered MQTT references and one Home Assistant integration.
- **What could not be done:**
  - The WebSearch budget ran out partway through, so search breadth is narrower than planned.
    Reddit and BIQU's own site were not searched.
  - web.archive.org was refused or rate-limited.
  - The Bambu store's plate pages render in the browser and carry no product data in the HTML, so
    what the store sells today could not be read from the store itself.
- **Fetched vs snippet:**
  - "Fetched" means the full page or post was read.
  - "Snippet" means only a search-result excerpt was seen.
  - Every claim below was fetched unless it says snippet.
- **The printer was not touched.** No MQTT commands were sent and no `bambu` CLI commands were
  run. Its config file was not read.

### Q1. Which options to switch off or keep on, where each is set, and whether it lasts

| # | Claim | Source | Fetched? | Quote (15 words or fewer) |
|---|---|---|---|---|
| 1.1 | Bambu says third-party plates cause more false foreign-object alarms, and that you can turn the check off. | [X2D wiki, Intelligent Detection §5.2](https://wiki.bambulab.com/en/x2d/manual/intelligent-detection) | fetched | "Third-party build plates are more prone to false detections." |
| 1.2 | Where to turn foreign-object detection off on the X2D (the printer screen). | same, §5.2 | fetched | "you can turn off foreign object detection in "Settings > Print Options"." |
| 1.3 | **0500-8062 belongs to Build Plate Type Detection.** It is listed under that heading, and the type check uses the corner live view camera. | same, §6 and §6.4 | fetched | "0500-8062: Build plate marker not detected. Ensure proper placement and clear markers." |
| 1.4 | Bambu's own fix for 8062 includes blocking outside light. | same, §6.4 | fetched | "Block external light if necessary." |
| 1.5 | The type check is switched on the printer screen. | same, §6.3 | fetched | "can be enabled in Settings > Print Options on the screen." |
| 1.6 | **Alignment is a separate check** that uses the toolhead camera at two points. Its error is 0500-808C, not 8062. | same, §8, §8.2, §8.4 | fetched | "the toolhead moves to the two positions… takes two pictures" |
| 1.7 | Alignment, displacement, spaghetti, pile-up and clumping are all set in Settings > Print Options on the screen. | same, §1.2, §2.1, §3.3, §4.4, §8.3 | fetched | "Printed Part Displacement Detection can be enabled in Settings > Print Options" |
| 1.8 | The foreign-object check runs once or twice before a print, the second time with the bed raised. Its blind spot is a 6 × 6 cm triangle near the camera. | same, §5.2 and §5.5 | fetched | "Max blind spot: triangular area 6cm x 6cm near the live view camera." |
| 1.9 | Firmware 01.02.00.00 (2026-07-30) changed the camera detection and dropped the user calibration step. | [X2D firmware release history](https://wiki.bambulab.com/en/x2d/manual/x2d-firmware-release-history) | fetched | "users no longer need to perform liveview camera calibration." |
| 1.10 | Firmware 01.01.00.00 (2026-04-14) added the foreign-object switch and turned plate presence detection on by default. | same | fetched | "Build Plate Presence Detection enabled by default." / "Added toggles for foreign object detection" |
| 1.11 | Firmware 01.01.01.00 (2026-05-20) tuned plate-offset and displacement detection. | same | fetched | "Optimized build plate offset and print displacement detection" |
| 1.12 | On the H2D there is one switch covering plate type and position. The H2C splits it into type and alignment. The X2D wiki documents them as two checks. | [H2 wiki, Intelligent Detection §2.4.3](https://wiki.bambulab.com/en/h2/manual/intelligent-detection) | fetched | "H2C: Separate settings are available for build plate type detection and alignment detection" |
| 1.13 | **Bambu Studio has the same switches** (Device tab, print options). The labels are listed after this table. | [PrintOptionsDialog.cpp](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/PrintOptionsDialog.cpp) | fetched | "Pauses printing when the detected build plate type does not match the selected one." |
| 1.14 | Idle Heating Protection is in Studio's separate Safety Options dialog, not Print Options. | [SafetyOptionsDialog.cpp](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/SafetyOptionsDialog.cpp) | fetched | "Stops heating automatically after 5 mins of idle to ensure safety." |
| 1.15 | **Per print, both plate errors can be skipped.** On 05008062 and 0500808C Studio offers "Ignore this and Resume" and "Problem Solved and Resume". On 0500806E the only listed action (21) has no matching button in Studio's code. | X2D HMS action table with [DeviceErrorDialog.hpp](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/DeviceErrorDialog.hpp) | fetched | "IGNORE_RESUME = 27, PROBLEM_SOLVED_RESUME = 28," |
| 1.16 | The X2D HMS table also has these related errors: 05008051 (wrong plate type for the G-code), 05008061 (no plate), 0C008009 (marker not found) and 0500807A (foreign-object check did not run). | X2D HMS table, ver 202511162200, in BambuStudio resources/hms | fetched | "Detected build plate is not the same as the Gcode file" |
| 1.17 | X2D owner bug report: false foreign-object errors with BIQU Glacier and Frostbite plates since firmware 01.02.00.00. | [forum post 69/283](https://forum.bambulab.com/t/bambu-firmware-bug-reporting-thread/69/283), 2026-08-03 | fetched | "This issue only started occurring for me with the 1.02 firmware update" |
| 1.18 | On X2D beta firmware 1.1.3.69, a Glacier owner turned the check off. A carbon-fibre third-party plate had the same problem (#11). | [forum 256670 #8, #11](https://forum.bambulab.com/t/256670) | fetched | "Biqu Glacier. No issues in previous firmware. I had to turn off detection." |
| 1.19 | Thread 257780 (an X2D owner): false foreign-object errors on green, blue and purple third-party plates after 01.02.00.00. Going back to old firmware and running the camera calibration stopped them (#4). | [forum 257780](https://forum.bambulab.com/t/257780) | fetched | "NO MORE FALSE ERRORS" |
| 1.20 | For marker misreads, community practice is to switch plate detection off on the printer. Seen on X1C with Bambu's own SuperTack plate, and on A1 with BIQU plates. | [forum 113355 #2, #10](https://forum.bambulab.com/t/113355) | fetched | "I just went into printer settings and turned plate detection off" |
| 1.21 | **Even Bambu's own plates get misread.** H2D did not recognise Bambu's Engineering Plate, and the advice was to switch recognition off or ignore the error. | [forum 232948 #2, #5](https://forum.bambulab.com/t/232948) | fetched | "temporarily you can disable the plate recognition in the settings" |
| 1.22 | One H2D foreign-object error was real: packing foam near the camera. | [forum 172793](https://forum.bambulab.com/t/172793) | fetched | (summary; no quote kept) |

The Studio labels behind 1.13:

- "Build Plate Detection", with "Type Detection" and "Alignment Detection" under it
- "Foreign Object Detection"
- "Printed Part Displacement Detection"
- "First Layer Inspection"
- "AI Detections"
- "Filament Tangle Detect"

**Not found:**

- **Bambu Handy.** No document on where these switches sit in Handy. Searched: the two wiki pages
  above and the firmware history. Web search was not available for a broader look.
- **Whether the settings last.** No Bambu document says whether they survive a power cycle or a
  firmware update. What the code shows:
  - Studio reads each switch's state back from the printer's status report (the bits under Q4),
    not from its own settings.
  - So the setting lives on the printer and is shared by the screen, Studio and Handy.
  - This is **inferred from code, not documented**.
  - The 01.01.00.00 note shows a firmware update *can* change a default.

### Q2. Which bed type to slice as, what Textured PEI changes in the start G-code, and PLA bed temperatures

| # | Claim | Source | Fetched? | Quote (15 words or fewer) |
|---|---|---|---|---|
| 2.1 | The X2D defaults to Textured PEI and does not support the old "Cool Plate" type. | [Bambu Lab X2D.json](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/resources/profiles/BBL/machine/Bambu%20Lab%20X2D.json) | fetched | `"not_support_bed_type": "Cool Plate"` |
| 2.2 | Studio's bed types are Cool Plate, Engineering Plate, High Temp Plate, Textured PEI Plate and Supertack Plate. "High Temp Plate" is labelled "Smooth PEI Plate / High Temp Plate". | [PrintConfig.cpp](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/libslic3r/PrintConfig.cpp) | fetched | "Smooth PEI Plate / High Temp Plate" |
| 2.3 | **The start G-code sets the nozzle 0.02 mm lower when sliced as Textured PEI.** It runs `G29.1 Z-0.003` vs `Z0.017` when the first-layer bed is above 70 °C, and `Z0.002` vs `Z0.022` otherwise. So a smooth plate sliced as Textured gets its first layer squashed by about 0.02 mm. | [X2D 0.4 machine start G-code](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/resources/profiles/BBL/machine/Bambu%20Lab%20X2D%200.4%20nozzle%20template%20machine_start_gcode.json) | fetched | `{if curr_bed_type=="Textured PEI Plate"} G29.1 Z{0.002} {else} G29.1 Z{0.022}` |
| 2.4 | The reason given in a comment in the same G-code. | same | fetched | "lower the nozzle as the nozzle was touching topmost of the texture when homing" |
| 2.5 | The same start G-code runs these checks itself, whatever the bed type. The printer's switches decide whether each one acts. *That last point is inferred.* The checks are listed after this table. | same | fetched | `M1002 gcode_claim_action : 74 ; Heatbed surface foreign object detection` |
| 2.6 | Bambu's generic PLA bed temperature is 55 °C for High Temp (smooth PEI) and for Textured PEI. Cool plate is 35 °C. | fdm_filament_pla.json in BambuStudio resources/profiles/BBL/filament | fetched | `"hot_plate_temp": ["55"]` |
| 2.7 | Bambu PLA Basic on the X2D: 55 °C on the Engineering plate and 40 °C on SuperTack, first layer included. | [Bambu PLA Basic @BBL X2D 0.4 nozzle.json](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40BBL%20X2D%200.4%20nozzle.json) | fetched | `"supertack_plate_temp": ["40"]` |
| 2.8 | **Community advice for a BIQU Glacier on the H2D is to slice it as High Temp (smooth PEI).** After switching, the mismatch error went away (#9). | [forum 164540 #4, #9](https://forum.bambulab.com/t/164540) | fetched | "Texture Plate… hard-coded with an offset in the machine begin gcode" |
| 2.9 | Glacier is a high-temperature coating that wants about 5 °C more than PEI. Frostbite is BIQU's low-temperature plate. One user's claim. | same, #11 | fetched | (paraphrase; one user, not BIQU) |
| 2.10 | A Glacier owner slices it as smooth PEI and the printer reads its code. Frostbite has no code and is sliced as SuperTack. | [forum 204784](https://forum.bambulab.com/t/204784) | fetched | "With my Biqu Glacier plate I use the Smooth PEI Plate /High Temp Plate setting" |
| 2.11 | An H2D Glacier plate carries the smooth-plate code. A P2S owner said BIQU recommends "Cool Plate" for Glacier; that P2S then crashed into the plate. The thread does not put the crash down to the bed type. | [forum 205851 #2, #4](https://forum.bambulab.com/t/205851) | fetched | "I have always used smooth plate with the glacier" |

The checks behind 2.5:

- `M972 S26 P0 C0` (foreign objects)
- `M972 S19 P0` (heatbed detection)
- `M972 S34 P0` (plate deviation)
- `G3811`, the check under the bed, only when the print reaches 145 mm high or more
- `build_plate_detect_flag=1`

**Not found:**

- BIQU's own slicing advice for the X2D. BIQU's site was not searched.

### Q3. Whether Bambu sells smooth PEI or SuperTack for the X2D/H2D, which plates carry the marker, and whether copies get misread

| # | Claim | Source | Fetched? | Quote (15 words or fewer) |
|---|---|---|---|---|
| 3.1 | **An X2D owner says Bambu's smooth PEI plate is no longer sold.** A dual PEI plate is available instead, and BIQU Glacier is the usual stand-in. Community claim; not checked against the store. | [forum 258878](https://forum.bambulab.com/t/258878), 2026-08-28 | fetched | "not for sale any more" |
| 3.2 | The Bambu store sold no H2D plates as of April 2025. | [forum 163705](https://forum.bambulab.com/t/163705) | fetched | (paraphrase) |
| 3.3 | In mid-2025 the H2D offered only two plate types, Textured and smooth PEI. | [forum 172971](https://forum.bambulab.com/t/172971) | fetched | "It only shows official plates" |
| 3.4 | Bambu's Engineering Plate was not recognised on the H2D. The EU store said support would come in Q1 2026 (#1). Plate codes differ by printer family (#16). | [forum 232948](https://forum.bambulab.com/t/232948) | fetched | (paraphrase) |
| 3.5 | **A BIQU Glacier gave the marker error on a P2S but not on a P1S** (#14). Homemade stickers need high contrast and exact placement (#17–#20). | same | fetched | (paraphrase) |
| 3.6 | Bambu's own plates carry printed markers. BIQU plates ship with stickers so the printer can read them (#8). Bambu's SuperTack marker was too faint for an X1C to read (#11). | [forum 113355](https://forum.bambulab.com/t/113355) | fetched | "BIQU plates come with stickers so that the printer can scan and register them" |
| 3.7 | Another X1C could not read the SuperTack marker either. | [forum 113809 #6](https://forum.bambulab.com/t/113809) | fetched | "My X1C can't read the localization marker on this plate." |
| 3.8 | An H2D with a BIQU Glacier got both the foreign-object error and the plate-type mismatch. It printed after both were ignored. | [forum 164540](https://forum.bambulab.com/t/164540) | fetched | (paraphrase) |
| 3.9 | `cur_id: "P0101"` with `base: 4` appears in community mock data for an X2D, and P0101 appears for H2D and H2S too. Studio's source has no reader for `cur_id`, so its meaning is **undocumented**. | [ha-bambulab MOCK-X2D.json](https://github.com/greghesp/ha-bambulab) (pybambu mock_data); BambuStudio code search | fetched | `"plate": {"base": 4, "cur_id": "P0101", ...}` |

**Not found:**

- **What the Bambu store sells for the X2D today.** The store pages render in the browser and
  WebFetch got 402.
- **A Bambu statement on which plates carry which marker code.**
- **Who made Omar's glacier plate.** Nothing found ties a light-blue smooth plate with a honeycomb
  strip to one maker. "Glacier" is BIQU's product name, but other brands use "glacier/ice/cool"
  names. Treating it as BIQU is **an assumption**.
- **Why the printer shows P0101 for both plates.** Pass A's guess, *not supported by any source*: the
  printer may keep the last plate it read when it cannot read a new marker. That would explain 8062
  on the glacier plate with `cur_id` unchanged. It needs a status read with the glacier plate in and
  the type check on, which this pass did not do (no printer access by brief).

### Q4. The MQTT command shape, module names and how state is reported

| # | Claim | Source | Fetched? | Quote (15 words or fewer) |
|---|---|---|---|---|
| 4.1 | **Studio builds the camera-check command like this** (shown after this table). | [DevPrintOptions.cpp `command_xcam_control`](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/DeviceCore/DevPrintOptions.cpp) | fetched | `j["xcam"]["command"] = "xcam_control_set";` |
| 4.2 | The module name for each switch (table below). | same | fetched | — |
| 4.3 | How the printer reports state (bits listed below). | same, plus [DevUtil.cpp](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/DeviceCore/DevUtil.cpp) | fetched | — |
| 4.4 | OpenBambuAPI lists `xcam_control_set` with seven modules. It does not list `fod_check`, `plate_offset_switch` or `model_movement_check`, so it predates the X2D/H2D switches. | [OpenBambuAPI mqtt.md](https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md) | fetched | "first_layer_inspector, buildplate_marker_detector, printing_monitor, pileup_detector…" |
| 4.5 | open-bamboo-networking lists the full module set, including `plate_offset_switch`, `fod_check` and `model_movement_check`. Its example uses `"sequence_id": "20000"`. | [ClusterM/open-bamboo-networking research/12.12-xcam.md](https://github.com/ClusterM/open-bamboo-networking) | fetched | (module list; matches 4.2) |
| 4.6 | Same project: on "NP" firmware, `xcam.cfg` and `home_flag` are not sent. | open-bamboo-networking research/12.01-status.md | **snippet** (code-search excerpt) | — |
| 4.7 | A community X2D status sample decodes as all switches on, first-layer inspection on, tangle off and idle heating protection on (values below). | ha-bambulab MOCK-X2D.json | fetched (decoded by pass A) | `"halt_print_sensitivity": "medium"` |

The command Studio sends (4.1):

```json
{"xcam": {"command": "xcam_control_set", "sequence_id": "<n>",
          "module_name": "<module>", "control": true, "enable": true,
          "print_halt": true, "halt_print_sensitivity": "<low|medium|high, optional>"}}
```

- `enable` and `print_halt` are marked "old protocol" in the code.
- Studio holds off reading the state again for 3 seconds after a toggle.

The module names (4.2):

| Switch (Studio label) | Command |
|---|---|
| Build Plate Detection / Type Detection | xcam `buildplate_marker_detector` (the one module drives both) |
| Alignment Detection | xcam `plate_offset_switch` |
| Foreign Object Detection | xcam `fod_check` |
| Printed Part Displacement Detection | xcam `model_movement_check` |
| First Layer Inspection | xcam `first_layer_inspector` |
| AI monitoring / spaghetti | xcam `printing_monitor` / `spaghetti_detector` |
| Purge chute pile-up | xcam `pileup_detector` |
| Nozzle clumping | xcam `clump_detector` |
| Air printing | xcam `airprint_detector` |
| Idle Heating Protection | `{"print":{"command":"set_against_continued_heating_mode","enable":bool}}` |
| Filament tangle | `print_option` with `filament_tangle_detect` |
| Auto-recovery, sound, nozzle blob, air purification | `print_option` with `auto_recovery`, `sound_enable`, `nozzle_blob_detect`, `air_purification` |

How the printer reports state (4.3):

- `xcam.cfg` is an integer. Bit 0 is the lowest.
  - spaghetti: bit 7, sensitivity in bits 8–9
  - pile-up: bit 10
  - clumping: bit 13
  - air printing: bit 16
  - **alignment: bit 20**
  - **foreign objects: bit 21**
  - **displacement: bit 22**
- Booleans under `xcam`: `buildplate_marker_detector`, `first_layer_inspector`, `printing_monitor`,
  `spaghetti_detector`, and the string `halt_print_sensitivity`.
- `print.cfg` is a hex string.
  - first-layer inspection: bit 12
  - AI monitor: bit 15
  - tangle: bit 23
  - idle heating protection: bits 32–33
- Which switches a printer supports is read from these bits:
  - `fun` (hex): tangle 9, idle heating 62
  - `fun2` (hex, bit 0 at the rightmost digit): alignment 2, foreign objects 13, displacement 14

The X2D sample decoded (4.7):

- `xcam.cfg = 8089015`: bits 20, 21 and 22 all set (alignment, foreign objects and displacement on)
- `print.cfg = "5A1045FDA99"`: first-layer bit 12 = 1, tangle bit 23 = 0, idle bits 32–33 = 1
- `fun2 = "B7B77"`: supports alignment, foreign objects and displacement

## Recommendation (pass A)

**For the glacier plate**, in order of what to do:

| Setting | Do | Confidence | Why |
|---|---|---|---|
| Foreign Object Detection | **Off** while the glacier plate is on the bed. On again for the gold plate. | **High** that turning it off clears 806E. Medium on switching it back each time. | Bambu's X2D wiki says third-party plates cause false alarms and tells you to turn it off (1.1, 1.2). X2D owners report the same with Glacier-type plates since 01.02.00.00 (1.17–1.19). The cost: no check for a print left on the bed, and it is a printer-wide switch. |
| Build Plate Type Detection | First try once: clean the marker strip and shade the plate from outside light (1.4). If 8062 comes back, use **"Ignore this and Resume"** for that print, or switch type detection **off**. | **Medium-high** | 8062 belongs to the type check (1.3). Ignore-and-resume is offered for 8062 (1.15). Switching off is the common fix, even for Bambu's own plates (1.20, 1.21). The cost: nothing checks that the slicer bed type matches the plate, so the slice must be right (next rows). |
| Alignment Detection | **Keep on** | Medium | It is a separate check using the toolhead camera (1.6). No source shows it misfiring on third-party plates. It guards a misplaced plate. Turn it off only if 808C fires on the glacier plate. |
| Printed Part Displacement, First Layer Inspection, AI detections (spaghetti, pile-up, clumping, air printing) | **Keep on** | Medium | None reads the plate marker or the bare bed before the print. No source ties them to third-party plates. Not tested on a light-blue smooth surface. |
| Filament Tangle, Idle Heating Protection | **Keep on** | High | They have nothing to do with the plate (1.14, 4.2). |
| Slice as | **"Smooth PEI Plate / High Temp Plate"** | **Medium-high** | Slicing as Textured lowers the nozzle by 0.02 mm (2.3, 2.4), which squashes the first layer on a smooth plate. Community advice for BIQU Glacier is smooth PEI (2.8, 2.10, 2.11). The X2D cannot use "Cool Plate" (2.1). Use SuperTack only if the plate turns out to be a low-temperature, Frostbite-type plate. |
| PLA bed temperature | **55 °C**, both for the first layer and after | High that it is Bambu's default; Low that the glacier plate wants it | Bambu's own default for High Temp (2.6). One user says Glacier wants about +5 °C (2.9). Raise it only if adhesion is weak. |
| Where to set the switches | On the printer screen: **Settings > Print Options**. Or in Studio: Device tab, print options. Idle heating protection is under Studio's Safety Options. | High (screen and Studio). Handy: not found. | 1.2, 1.5, 1.7, 1.13, 1.14 |
| Do they last? | Probably yes: they live on the printer and every app reads them back. Check after any firmware update. | Medium (inferred from code, not documented) | Q1 "Not found"; 1.10 |
| For a `bambu options` CLI | Read state from `xcam.cfg` bits 20–22 plus the `xcam` booleans. Write with the `xcam_control_set` shape above, one module per command. | High that this is Studio's protocol. Not tested on Omar's printer. | 4.1–4.3, 4.7 |

**Open questions this pass could not settle:**

- Who made the glacier plate.
- Why `cur_id` stays P0101.
- Whether firmware past 01.02.00.00 changes the foreign-object false alarms.
- Where these switches sit in Bambu Handy.
