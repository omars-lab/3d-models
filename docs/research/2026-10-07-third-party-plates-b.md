---
date: 2026-10-07
produced-by: researcher B (Claude Opus 5.5), one of two independent researchers on the same question; Bambu wiki pages fetched directly and through its search endpoint, Bambu forum threads read through the forum's JSON API, and a local clone of Bambu Studio (commit da8b44e, 2026-09-28). The printer was not contacted.
feeds:
  - send-plate skill step 4
  - the X2D setup walkthrough
  - a possible bambu options CLI
---
<!-- provenance
date: 2026-10-07
produced-by: Claude (research pass B of two, independent), on Omar's ask "on using non bambu plates ... what options to disable per agreed upon best practices? websearch accordingly"
feeds: send-plate skill step 4, the X2D setup walkthrough, a possible `bambu options` CLI
-->

# Third-party plates on the X2D: which checks to turn off (research B)

**The question.** Omar's smooth light-blue "glacier" plate has a honeycomb marker strip.
On 2026-10-07 the X2D twice refused to start with it, before the first layer: HMS
0500-806E (foreign objects detected, on an empty plate) and then 0500-8062 (plate marker
not detected). The printer reported the plate as `device.plate.cur_id: "P0101"`,
`base: 4`, the same as the gold Textured PEI plate, which printed fine. Four questions:
which detection options to turn off for a non-Bambu plate, which bed type to slice as,
what Bambu sells and how markers work, and the exact MQTT shape for the options.

**How to read this file.** Every source says whether I **fetched** it (read the whole
page, thread or file) or saw only a **snippet** (a search-result line, which can be out
of context). Bambu Studio source was read from a local clone at commit
`da8b44ee34dd349f2ae0df3f1cbae366df482354` (2026-09-28); links below point at that
commit. Quotes are at most 15 words. The web-search tool was not available in this pass
(its session budget was used up), so searching went through the Bambu wiki's own search,
the Bambu forum's search, and the Studio source. Third-party sites (BIQU, Panda, Reddit)
were **not** searched; nothing below says what they do or do not publish.

Studio links share this prefix, written once:
`https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/`
(shortened to `BS/` below).

## Raw findings

### Q1. Which options to turn off for a non-Bambu plate, where each is set, and whether it sticks

**What the X2D has, and which camera does each check.**

- Bambu wiki, X2D intelligent detection, https://wiki.bambulab.com/en/x2d/manual/intelligent-detection
  (**fetched**). The live view camera (chamber corner) does spaghetti, purge-chute
  pile-up, nozzle clumping, printed-part displacement, foreign object detection, and
  build plate *type* detection. The toolhead camera does build plate *alignment*
  detection. Each section says the toggle is on the printer screen:
  "can be enabled in Settings > Print Options on the screen."
- Same page, §5 Foreign Object Detection: "Third-party build plates are more prone to
  false detections." Then: "When using a third-party build plate, you can turn off foreign
  object detection". It lists 0500806E as "Foreign object detected on the plate". It
  detects objects "larger than 5cm x 3cm x 0.1cm". Note the hedge: "can turn off", not
  "must".
- Same page, §5.4: from firmware 01.01.00.00 foreign object detection "no longer relies on
  this calibration step"; machines are "factory-calibrated".
- Same page, §6 Build Plate Type Detection: the camera checks the plate against "the
  sliced heatbed type in the print file". Lists 0500-8062 "Build plate marker not
  detected" and 0500-8051 "Detected plate type doesn't match slicer G-code".
- Same page, §8 Alignment Detection: toolhead camera "takes two pictures"; error
  0500-808C. Says nothing about third-party plates.
- The page does not mention First Layer Inspection, filament tangle or idle heating.

**Bambu's own advice for a plate the printer does not recognise.**

- Bambu wiki, build plates overview, https://wiki.bambulab.com/en/filament-acc/acc/plates
  (**fetched**). On an unrecognised plate: "select 'Resolved' on the screen or disable the
  Build Plate Detection feature." Also: "First-generation build plates do not support the
  build plate recognition feature of second-generation printers." (X2D and P2S are named
  among the second-generation printers that use the updated QR code.)
- Bambu wiki, P2S troubleshooting, build plate not detected,
  https://wiki.bambulab.com/en/p2s/troubleshooting/build-plate-not-detected (**fetched**;
  P2S page, not X2D, but the same marker family per the plates page): "If you are using a
  third-party build plate, simply ignore this message."
- Bambu wiki, H2 intelligent detection, https://wiki.bambulab.com/en/h2/manual/intelligent-detection
  (**fetched**; H2D, not X2D): for build plate detection, "Disabling it skips this check."
  It also says the H2C has separate toggles for type and alignment; the X2D Studio code
  below has the same split.

**What the error dialogs offer.** Studio ships the X2D's HMS text in
`BS/resources/hms/hms_en_20P.json` (**fetched**, from the clone; 20P is the X2D serial
prefix). The action numbers map to buttons in `BS/src/slic3r/GUI/DeviceErrorDialog.hpp` (5 is stop printing, 27 "Ignore this and Resume", 28 "Problem Solved and Resume"):

| HMS | Text (shortened) | Buttons |
|---|---|---|
| 0500-8062 | build plate marker not detected | "Ignore this and Resume", "Problem Solved and Resume" |
| 0500-806E | foreign objects detected | action 21, which has no button in Studio's list; on the printer, unknown |
| 0500-8051 | detected plate not the same as the G-code | actions 28, 27, 5: both resume buttons and stop |
| 0500-808C | plate offset | "Ignore this and Resume", "Problem Solved and Resume" |

So 0500-8062 can be passed per print with "Ignore". Whether the printer screen offers an
ignore for 0500-806E is **not found** (searched the 20P HMS file and the X2D wiki page).

**Firmware history that bears on the false foreign-object alarm.**

- Bambu wiki, X2D firmware release history, https://wiki.bambulab.com/en/x2d/manual/x2d-firmware-release-history
  (**fetched**). 01.02.00.00 (2026-07-30): users "no longer need to perform liveview camera
  calibration". 01.01.00.00 (2026-04-14): "Added toggles for foreign object detection".
  01.01.01.00: offset and displacement detection improved "under abnormal lighting".
- Forum, https://forum.bambulab.com/t/69/283 (**fetched**, post #283, 2026-08-03, a user):
  on X2D firmware 01.02.00.00, a BIQU Glacier or Frostbite plate gives a false "Foreign
  objects detected on heatbed"; says it began with 1.02.
- Forum, https://forum.bambulab.com/t/257780 (**fetched**, 2026-08-08 to 09-16): false
  foreign-object errors on every print since 01.02.00.00, on a green cool plate and blue
  BIQU plates, X2D in LAN mode. Post #2: "about 50% of the time" on a purple BIQU Glacier.
  Post #4: rolled the firmware back, ran the camera calibration, no more false errors.
  Posts #5 and #6: same on an X2D with a BIQU Glacier. These are user reports, not Bambu
  statements; nobody from Bambu answers in the thread.
- Forum, https://forum.bambulab.com/t/164540 (**fetched**, 2025-04, H2D): a new BIQU
  Glacier gives both "a foreign object is detected" and the plate-mismatch error on an
  empty bed; the user turned plate detection off and pressed ignore, and it printed.
- Forum, https://forum.bambulab.com/t/172793 (**fetched**, H2D): foreign-object false
  alarms, usually leftover packing foam under the camera.
- Forum, https://forum.bambulab.com/t/172203 (**snippet**): H2D firmware 01.01.02.08
  "Optimized foreign object detection on smooth PEI buildplate". Suggests smooth plates
  were a known weak spot on the H2D; not checked for the X2D.

**Which options exist on the X2D, from the Studio source.**

- `BS/resources/printers/N6.json` (X2D, **fetched**): 
  `support_build_plate_marker_detect: true`, `support_build_plate_marker_detect_type: 2` (type and position check),
  `support_first_layer_inspect: false`, `support_ai_monitoring: true`,
  `support_safety_options: true`. `O1D.json` (H2D) has the same plate and first-layer
  values. Studio lets a live printer push override these (`DevConfig.cpp`), so "the X2D
  has no First Layer Inspection" is what the bundled file says, not a check of a live
  printer.
- `BS/src/slic3r/GUI/PrintOptionsDialog.cpp` (**fetched**). Labels and help text Studio
  shows under Device > Print Options:
  - "Build Plate Detection": "Ensures the build plate type and placement are correct."
    It has two sub-toggles:
    - "Type Detection": "Pauses printing when the detected build plate type does not
      match the selected one."
    - "Alignment Detection": "Pauses printing when build plate misalignment is detected."
  - "Foreign Object Detection": "Checks for any objects on the build plate at the start
    of a print".
  - "Printed Part Displacement Detection": alerts "if it shifts or collapses".
  - "First Layer Inspection" is shown only when the printer supports it (see N6 above).
  - AI monitoring options: spaghetti, purge-chute pile-up, nozzle clumping, air printing,
    each with a sensitivity.
  - Filament tangle detection, sound, auto-recovery, nozzle blob detection.
- `BS/src/slic3r/GUI/SafetyOptionsDialog.cpp` (**fetched**). "Idle Heating Protection":
  "Stops heating automatically after 5 mins of idle". It is greyed out when the printer
  reports the heating-maintenance function on.
- Bambu wiki, print options, https://wiki.bambulab.com/en/studio-handy/print-options
  (**fetched**; an older X1/A1-era page). Options are set "on the screen of the printer or
  in Bambu Studio". The page does not mention Bambu Handy as a place to set them.
  Whether the Handy app has these toggles for the X2D is **not found** (searched the wiki
  for Handy print options).

**Does a setting stick?** **Not found** as a written statement (searched the X2D, H2 and
print-options wiki pages and the Studio dialogs). The Studio source gives an inference:
Studio sends a toggle command and then reads the option's state back from the printer's
status report (`print.xcam.cfg` and `print.cfg` bits, see Q4). Nothing is stored on the
Studio side. So the setting lives on the printer and should survive across prints and
across which computer sends. Whether it survives a power cycle or a firmware update is not
documented. Check by looking at the screen after a restart.

**Options that have nothing to do with the plate.** Filament tangle, idle heating
protection, spaghetti, pile-up, clumping and air printing are not tied to the plate in any
source read here. Printed part displacement uses the live view camera on the print, and the
X2D page says "black filament may reduce accuracy". No source links it to plate colour.

### Q2. Which bed type to slice a smooth third-party PEI plate as

**Bed types the X2D accepts.**

- `BS/resources/profiles/BBL/machine/Bambu Lab X2D.json` (**fetched**):
  `default_bed_type: "Textured PEI Plate"`, `not_support_bed_type: "Cool Plate"`.
- `BS/src/libslic3r/PrintConfig.cpp` (**fetched**). Bed type values include Engineering
  Plate, High Temp Plate, Textured PEI Plate and Supertack Plate. The label for High Temp
  Plate is "Smooth PEI Plate / High Temp Plate". Each plate reads its own bed-temperature
  key: `hot_plate_temp` (smooth PEI / high temp), `textured_plate_temp`,
  `supertack_plate_temp`, `eng_plate_temp`.

**What the X2D start G-code does differently for Textured PEI.** Read from
`BS/resources/profiles/BBL/machine/Bambu Lab X2D 0.4 nozzle template machine_start_gcode.json`
(**fetched**, template dated 2026/06/05):

- Foreign object detection: one call, `M972 S26 P0 C0`, under the claim "Heatbed surface
  foreign object detection". It does not branch on plate type.
- Plate detection block: `M972 S19`, `S31`, then plate deviation `S34`. Not wrapped in a
  flag check in the template.
- Z offset trim near the end of the start code. The only plate-dependent line found:

  ```
  {if bed_temperature_initial_layer_single > 70}
    {if curr_bed_type=="Textured PEI Plate"} G29.1 Z{-0.003} {else} G29.1 Z{0.017} {endif}
  {else}
    {if curr_bed_type=="Textured PEI Plate"} G29.1 Z{0.002} {else} G29.1 Z{0.022} {endif}
  {endif}
  ```

  At PLA bed temperatures (70 or below), Textured gets +0.002 mm and every other plate
  gets +0.022 mm. Slicing a smooth plate as Textured puts the first layer 0.02 mm lower
  (more squish) than Bambu intends for a smooth plate.

- For contrast, the H2D template (`Bambu Lab H2D 0.4 nozzle template machine_start_gcode.json`,
  **fetched**) does branch the foreign-object check on plate:
  `{if curr_bed_type=="Textured PEI Plate"} M972 S26 P0 C0 {else} M972 S36 P0 C0 X1 {endif}`.
  It also wraps plate detection in `M1002 judge_flag build_plate_detect_flag`. What the
  M972 sub-codes do is not documented anywhere I found. That S36 is a smooth-plate mode,
  and that the X2D's missing branch makes smooth plates false-trigger, is **my inference**
  and is not checked.

**PLA bed temperature.**

- `BS/resources/profiles/BBL/filament/fdm_filament_pla.json` (**fetched**):
  `hot_plate_temp` 55, `textured_plate_temp` 55, `cool_plate_temp` 35.
- `BS/resources/profiles/BBL/filament/Bambu PLA Basic @BBL X2D 0.4 nozzle.json`
  (**fetched**): `eng_plate_temp` 55, `supertack_plate_temp` 40. The first layer and the
  other layers use the same value in each.
- So for Bambu PLA Basic on the X2D, Smooth PEI / High Temp and Textured are both 55 C.

**What owners of BIQU Glacier plates slice as.**

- Forum, https://forum.bambulab.com/t/164540 (**fetched**, post #4): "Should be High Temp."
  Texture Plate is "hard-coded with an offset in the machine begin gcode." Post #7 agrees.
  (H2D and X1C context.)
- Forum, https://forum.bambulab.com/t/219369 (**fetched**, P1S, Panda CryoGrip Glacier):
  one user uses "smooth plate and leave the temp default of 55C"; says the maker's sheet
  recommends 45/55.
- Forum, https://forum.bambulab.com/t/204784 (**snippet**): "With my Biqu Glacier plate I
  use the Smooth PEI Plate /High Temp Plate setting".
- Forum, https://forum.bambulab.com/t/146076 (**snippet**, P1S): PLA at 50 C on the glacier
  plate against 60 C on the stock textured plate.

### Q3. What Bambu sells, whether Bambu plates carry the marker, and whether third-party plates copy it

**What Bambu sells for the X2D.** Bambu wiki, build plates overview,
https://wiki.bambulab.com/en/filament-acc/acc/plates (**fetched**):

- X2D plates are 256 x 256 mm.
- Bambu plate types on that page: Textured PEI, Smooth PEI, Dual-Texture, Engineering and
  Cool Plate SuperTack.
- The 256 Textured PEI, Smooth PEI and SuperTack plates come in a first and a second
  generation. The second generation works with the P2S and X2D and has "updated QR code
  identification".
- I did not check the Bambu store for current stock or price.
- The H2D uses a different plate size; that page lists the H2D plates separately. I did
  not check the H2D plate list line by line.

**Whether Bambu plates carry the marker.** Yes, per the plates page (second generation
plates have a QR code). Forum https://forum.bambulab.com/t/113355 (**snippet**): Bambu's
newer plates "have markers on them, don't come with stickers". Codes differ by printer
model:

- Forum https://forum.bambulab.com/t/228520 (**fetched**): the "H2C textured plate has a
  different code than H2D's".
- Forum https://forum.bambulab.com/t/232948 post #16 (**fetched**): "P2S Engineering Plate
  use a different code than P1S".
- Forum https://forum.bambulab.com/t/232948 posts #2-#5 (**fetched**): a genuine Bambu
  Engineering Plate was not recognised by an H2D (firmware not yet supporting it); users
  disabled the check or pressed ignore. Post #3 says the EU store listed it as not
  recognised on the H2D "until Q1 2026". Forum https://forum.bambulab.com/t/210371 #112
  (**snippet**) quotes the same Q1 2026 note.
- Forum https://forum.bambulab.com/t/218582 (**snippet**): an H2D does not recognise a
  Bambu Engineering Plate; the user clicks "Ignore this issue, resume".

**Whether third-party plates copy the marker.** Yes for some, by user reports:

- Forum https://forum.bambulab.com/t/259088 (**fetched**, 2026-09, H2D): on the H2D a
  CryoClover plate "come[s] with the coolplate qr code"; the Glacier carries the smooth
  PEI one; "they are picked up by the printer". Post #9: "My Glacier plate came with
  stickers that identify it as a Smooth Hi-Temp (PEI) plate."
- Forum https://forum.bambulab.com/t/164540 (**fetched**, H2D): "it's the code on the
  plate", about a BIQU Glacier carrying the High Temp code.
- Forum https://forum.bambulab.com/t/232948 post #14 (**fetched**): the same BQ Glacier
  plate gives the marker error on a P2S but not on a P1S.
- Forum https://forum.bambulab.com/t/232948 posts #17-#20 (**fetched**): users make their
  own marker stickers; one says "the sticker has to be in the exact place".
- Forum https://forum.bambulab.com/t/219369 (**fetched**): a Panda CryoGrip Glacier came
  with a sticker set where the "recommended QR-code sticker is the one for 'cool plate'".
- Snippets only: https://forum.bambulab.com/t/151550 (a glacier plate likely "contains a
  copied QR code sticker"), https://forum.bambulab.com/t/185142 (stickers "that mimic the
  QR code"), https://forum.bambulab.com/t/254247 (Frostbite with the QR code printed on;
  Glacier with stickers that "don't stand up to washing"), https://forum.bambulab.com/t/204784
  (BIQU Frostbite has no plate code), https://forum.bambulab.com/t/258343 (X1C marker not
  detected with a textured PEI plate not made by Bambu), https://forum.bambulab.com/t/203799
  (a P2S smooth PEI plate without a marker).

**Whether a copied marker gets misread.** No source says a copied marker is read as the
*wrong* type. The reports are of a copied marker either read as its copied type, or not
read at all on a newer printer (P2S above). This fits a guess about Omar's plate: its
honeycomb strip may be a code for an older printer, which the X2D's second-generation
reader does not accept, giving 0500-8062. That is **my inference**, not a source claim.

**What `P0101` / `base: 4` means.** **Not found.** I searched the Studio clone for
`P0101`, `cur_id` and `base`, and the wiki search for "P0101", and found no table of plate
ids. Because the printer reported the same id for the gold Textured plate and the glacier,
it may be a stored or last-read value rather than a reading of the glacier's marker.
Unverified.

### Q4. The MQTT command shape and how state is reported

Source: `BS/src/slic3r/GUI/DeviceCore/DevPrintOptions.cpp` (**fetched**, from the clone),
plus `BS/src/slic3r/GUI/DeviceManager.cpp` for the HMS replies. I did not cross-check
ha-bambulab or OpenBambuAPI in this pass.

**The toggle command (`xcam_control_set`).** Built in `command_xcam_control`:

```json
{"xcam": {
  "command": "xcam_control_set",
  "sequence_id": "<n>",
  "module_name": "<module>",
  "control": true,
  "enable": true,
  "print_halt": true,
  "halt_print_sensitivity": "<low|medium|high, only for modules with a level>"
}}
```

`control` and `enable` carry the same on/off value; the source marks `enable` and
`print_halt` as the old protocol. `halt_print_sensitivity` is added only when a level is
passed.

**Module names used in the source:**

| `module_name` | Studio label | Level? |
|---|---|---|
| `printing_monitor` | AI monitoring (older printers) | yes |
| `spaghetti_detector` | Spaghetti detection | yes |
| `pileup_detector` | Purge chute pile-up | yes |
| `clump_detector` | Nozzle clumping | yes |
| `airprint_detector` | Air printing | yes |
| `buildplate_marker_detector` | Build plate marker / Type Detection | no |
| `plate_offset_switch` | Alignment Detection | no |
| `first_layer_inspector` | First Layer Inspection | no |
| `fod_check` | Foreign Object Detection | no |
| `model_movement_check` | Printed Part Displacement | no |

`buildplate_marker_detector` is used for both the older single marker toggle and the
newer "Type Detection" toggle.

**Options that are not `xcam` commands.**

- Idle heating protection: `{"print": {"command": "set_against_continued_heating_mode", "enable": true}}`.
- `print_option` commands (`{"print": {"command": "print_option", "<key>": <value>}}`), one
  key per call:
  - `filament_tangle_detect`
  - `sound_enable`
  - `auto_recovery` (sent with `option`)
  - `nozzle_blob_detect`
  - `nozzle_blob_detect_v2` (0 off, 1 on, 2 auto)
  - `air_purification` (0, 1, 2)
- Timelapse snapshot: `{"camera": {"command": "ipcam_cap_pic_set", "control": "enable"}}`.

**HMS replies** (`DeviceManager.cpp`). Ignore:
`{"print": {"command": "ignore", "err": "<decimal code>", "param": "reserve", "job_id": ..., "sequence_id": ...}}`.
Resume is the same with `"command": "resume"`.

**How state is reported** (the push status, parsed in `ParseDetectionV1_0`). Bits count
from the least significant bit.

- `print.xcam.cfg` (an integer):
  - bit 7: spaghetti on; bits 8-9: its level (0 low, 1 medium, 2 high)
  - bit 10: pile-up on; bits 11-12: its level
  - bit 13: clumping on; bits 14-15: its level
  - bit 16: air printing on; bits 17-18: its level
  - bit 20: plate alignment on
  - bit 21: foreign object detection on
  - bit 22: printed part displacement on
- `print.xcam.buildplate_marker_detector` (bool): plate marker and type detection.
- `print.xcam.first_layer_inspector` (bool).
- `print.xcam.printing_monitor`, `spaghetti_detector`, `halt_print_sensitivity`: older
  fields.
- `print.cfg` (a hex string):
  - bits 8-10: speed level
  - bit 12: first layer
  - bits 13-14: AI sensitivity
  - bit 15: AI monitor
  - bit 16: auto recovery
  - bit 22: sound
  - bit 23: filament tangle
  - bit 24: nozzle blob
  - bits 32-33: idle heating protection (2 means not available, heating maintenance on)
  - bits 36-37: air purification
  - bits 38-39: snapshot
  - bits 43-44: smart nozzle blob
- `fun` (hex) says which options the printer supports:
  - bit 8: sound
  - bit 9: tangle
  - bit 13: nozzle blob
  - bit 42: spaghetti
  - bit 43: pile-up
  - bit 44: clumping
  - bit 45: air printing
  - bit 62: idle heating
- `fun2` (hex), more support bits:
  - bit 2: plate alignment
  - bit 4: air purification
  - bit 13: foreign object detection
  - bit 14: displacement
  - bit 15: smart nozzle blob
- `home_flag` (older printers):
  - bit 4: auto recovery
  - bit 17: sound; bit 18: sound supported
  - bit 19: tangle supported; bit 20: tangle on
  - bit 24: blob on; bit 25: blob supported

## Recommendation (pass B)

For printing on the glacier plate (or any plate not made by Bambu) on the X2D:

| Option | Glacier plate | Confidence | Why |
|---|---|---|---|
| Foreign Object Detection | **Off** | High | Bambu's X2D page names third-party plates as a false-alarm case and says to turn it off; three forum threads report this exact error with BIQU Glacier plates on the X2D since firmware 01.02.00.00. |
| Build Plate Detection, Type Detection | **Off** (or press "Ignore this and Resume" on 0500-8062 each print) | High | Bambu's plates page says to choose "Resolved" or disable it; the P2S page says to ignore the message for third-party plates. |
| Build Plate Detection, Alignment Detection | **Keep on** | Medium | It uses the toolhead camera, and no source links it to third-party plates. Turn it off only if 0500-808C fires on a plate you can see is seated. |
| Spaghetti, pile-up, clumping, air printing | **Keep on** | Medium | Not tied to the plate in any source read; they protect the machine. |
| Printed Part Displacement | **Keep on** | Medium | Not tied to the plate in any source read; a light plate under the camera was not tested. |
| First Layer Inspection | Not on the X2D | Medium | The bundled X2D config says not supported; not checked on the live printer. |
| Filament tangle, idle heating protection | **Keep on** | High | Nothing to do with the plate. |
| Slice as | **Smooth PEI Plate / High Temp Plate** | High | A smooth PEI surface; X2D start code gives non-Textured plates +0.022 mm Z trim against Textured's +0.002 at PLA temperatures; forum owners of BIQU Glacier plates use it. |
| PLA bed temperature | **55 C** (Bambu's profile), try 50 C if parts stick too hard | Medium | 55 C is Bambu's value for this plate type; 50 C is a single user report and BIQU's 45/55 is second-hand. |
| Where to set | Printer screen, Settings > Print Options; or Bambu Studio, Device > Print Options | High | Bambu wiki and the Studio dialogs. Handy not checked. |
| Does it stick | Probably yes, until changed | Medium | Stored on the printer (Studio reads the state back from it); no written statement found; check after a restart. |
| Back on the gold Textured plate | Turn Foreign Object and Type Detection **back on** | Medium | They work there and catch a leftover print or the wrong plate. |

For a `bambu options` CLI: the toggles are `xcam_control_set` with `module_name` `fod_check`
and `buildplate_marker_detector`; read them back from `print.xcam.cfg` bit 21 and
`print.xcam.buildplate_marker_detector`. Sending any of these changes the printer, so it
needs Omar's go like a print send.

**Open, for the checker.**

- Why the glacier reported `P0101` / `base: 4`: not found.
- Whether the X2D screen offers an ignore for 0500-806E: not found.
- Whether a third-party marker sticker made for the X2D would make the type check pass:
  no X2D report found.
