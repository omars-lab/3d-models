---
date: 2026-10-07
produced-by: checker (Claude Opus 5.5), the third agent after two independent researchers; read both pass docs, re-opened the sources behind every load-bearing claim (Bambu wiki pages fetched directly, Bambu forum threads read through the forum's JSON API, a local clone of Bambu Studio at commit da8b44e, the HMS tables of the installed Studio 02.08.02.61, ha-bambulab's mock data through the GitHub API). The printer was not contacted and its config file was not read.
feeds:
  - send-plate skill (step 4, the plate and its options)
  - setup-bambu-x2d skill (the print options to set once)
  - a possible read-only bambu options show command
checks:
  - "pass A: PR #605, docs/research/2026-10-07-third-party-plates-a.md on branch research/third-party-plates-a"
  - "pass B: PR #604, docs/research/2026-10-07-third-party-plates-b.md on branch research/third-party-plates-b"
---

<!-- provenance
date: 2026-10-07
produced-by: Claude (checker, the third agent), consolidating research passes A (#605) and B (#604) on Omar's ask "on using non bambu plates ... what options to disable per agreed upon best practices? websearch accordingly"
feeds: send-plate skill, setup-bambu-x2d skill, a possible read-only `bambu options show`
-->

# Non-Bambu plates on the X2D: what to switch off, what to slice as (checked)

**The question.** Omar's "glacier" plate is smooth, light blue, and has a honeycomb marker strip
on its right edge. Who makes it is not known. On 2026-10-07 the X2D stopped print sld-1 twice
before the first layer:

- **0500-806E**: foreign objects on the bed, though the plate was empty.
- **0500-8062**: the plate marker was not detected.

The same print then ran at once on the gold Bambu Textured PEI plate. The printer reported both
plates as `plate.cur_id: P0101`, `base: 4`.

Omar asked three things: which printer options to switch off or keep on for a non-Bambu plate,
what to slice the plate as, and whether our CLI can change plate settings.

**How this file was made.** Two researchers answered the question on their own (pass A, PR #605;
pass B, PR #604). This file checks one against the other. For every claim that changes what we
do, I re-opened the source myself. Each source in the table at the end says whether I read it in
full ("fetched") or only saw a search excerpt ("snippet"), and whether I re-opened it or am
relying on a pass. A claim only one pass found, or one that rests on a snippet, is flagged rather
than dropped or trusted. The two pass docs stay as the record; this is the one to act on.

## The short answer

For the glacier plate, switch **Foreign Object Detection** and **Type Detection** off, keep the
rest on, and slice as **"Smooth PEI Plate / High Temp Plate"** at **55 °C** for PLA. Switch the
two back on when the gold plate goes back in. Our CLI can already set the slice's plate type
(`--plate-type hot_plate`). It cannot change the printer's options today. A read-only
`bambu options show` is a small step; changing an option from the CLI changes the printer and
needs Omar's go each time.

## Recommendation

| Option | On the glacier plate | Confidence | Source | A and B |
|---|---|---|---|---|
| Foreign Object Detection | **Off.** On again for Bambu plates. | High | Bambu's X2D page, §5.2: "Third-party build plates are more prone to false detections ... you can turn off foreign object detection". Three X2D forum threads report false 806E alarms on BIQU Glacier-type plates since firmware 01.02.00.00. | Agree |
| Type Detection (Studio: Build Plate Detection > Type Detection) | **Off**, or press **"Ignore this and Resume"** on 8062 each print | High | Bambu's X2D intro page: "If the device indicates unrecognized plate type, manually select "Ignore" or disable plate detection on the screen." The plates page says the same for older-generation plates. 8062 offers Ignore in the X2D error table. | Agree on off-or-ignore. A adds "clean the strip and shade it first", from Bambu's own 8062 advice; worth one try, not required. |
| Alignment Detection | **Keep on** | Medium | It is a separate check, run by the toolhead camera; its error is 808C, not 8062. No source ties it to third-party plates. Turn it off only if 808C fires on a plate that is plainly seated. | Agree |
| Printed Part Displacement | **Keep on** | Medium | No source ties it to the plate. Not tested on a light-blue smooth plate. | Agree |
| AI checks: spaghetti, pile-up, clumping, air printing | **Keep on** | Medium | No source ties them to the plate. They protect the machine. | Agree |
| First Layer Inspection | **Not offered on the X2D**; nothing to set | Medium | Studio's X2D printer file says `support_first_layer_inspect: false`, and Studio hides the switch when that is false. Bambu's X2D detection page has no first-layer section. Not checked on the live printer. | **Disagree.** A said keep on; B said not on the X2D. B is right by the sources. |
| Filament Tangle, Idle Heating Protection | **Keep on** | High | Nothing to do with the plate. | Agree |
| Slice as | **"Smooth PEI Plate / High Temp Plate"** (`--plate-type hot_plate`) | High that it should not be Textured PEI; medium-high that smooth PEI is the right one | The X2D start G-code lowers the nozzle by 0.02 mm for Textured PEI only, which squashes the first layer on a smooth plate. Forum owners of BIQU Glacier plates slice it as smooth PEI, and report the plate's marker is the smooth PEI one. If the plate turns out to be a low-temperature plate, SuperTack would fit instead. | Agree (A medium-high, B high) |
| PLA bed temperature | **55 °C**, first layer and after | Medium | Bambu's PLA profile: 55 °C for smooth PEI. One user runs a Glacier at 55 °C; another at 50 °C (snippet); one says Glacier wants about 5 °C more; BIQU's 45/55 is second-hand. Change it only if adhesion is wrong. | Agree on 55 |

**What switching off costs.** With Foreign Object Detection off, nothing checks for a print left
on the bed. With Type Detection off, nothing checks that the slice's plate type matches the plate,
so the slice has to be right. Both are printer-wide switches, not per plate: they stay off for the
gold plate too until switched back.

## What to slice as, and the bed temperature

**The 0.02 mm.** The X2D start G-code ends with a small nozzle height trim that depends on the
plate type in the slice:

```
;===== for Textured PEI Plate , lower the nozzle as the nozzle was touching topmost of the texture when homing ==
  {if bed_temperature_initial_layer_single > 70}
    {if curr_bed_type=="Textured PEI Plate"} G29.1 Z{-0.003} {else} G29.1 Z{0.017} {endif}
  {else}
    {if curr_bed_type=="Textured PEI Plate"} G29.1 Z{0.002} {else} G29.1 Z{0.022} {endif}
  {endif}
```

At PLA temperatures (bed 70 °C or below), Textured PEI gets +0.002 mm and every other plate type
gets +0.022 mm. A smooth plate sliced as Textured therefore prints its first layer 0.02 mm lower
than Bambu intends for a smooth plate. I read this in the Studio clone and in the installed app;
both files are the same. It is the only plate-dependent line in the X2D start G-code.

**Which non-Textured type.** The X2D does not accept "Cool Plate" (its printer file lists it under
`not_support_bed_type`). That leaves Smooth PEI / High Temp, Engineering and SuperTack. Forum
owners of the BIQU Glacier, on several printers, slice it as Smooth PEI / High Temp, and two say the
plate's own marker sticker is the smooth PEI one (forum 259088 #7 and #9, 204784 #1, 205851 #2,
164540 #4 and #12). These are user reports, mostly H2D, not BIQU or Bambu statements. A Panda
"CryoGrip Glacier" came with a sticker set that recommends the cool-plate code (219369 #1), so
"glacier" plates are not all alike. Omar's plate is assumed, not known, to be the BIQU kind.

**The temperature.** Bambu's generic PLA profile (Bambu PLA Basic on the X2D inherits it) sets
55 °C for Smooth PEI / High Temp and 55 °C for Textured PEI. So switching from Textured to Smooth PEI
does not change the bed temperature. Community numbers for Glacier plates:

- 55 °C, "leave the temp default" (219369 #2, Panda CryoGrip Glacier on a P1S; fetched).
- "BIQU recommends 45/55" (219369 #4; second-hand, from a photo of BIQU's sheet).
- "Glacier requires about 5C hotter than the PEI sheet" (164540 #11; one user).
- 50 °C on a glacier plate against 60 °C on textured (146076; **snippet only**, from pass B).

The four disagree. Keep Bambu's 55 °C and change it only if a print lifts or sticks too hard.

**A separate thing, not a switch.** Firmware 01.01.00.00 added "First Layer Quality Calibration",
a nozzle height fine-tune under the printer's calibration menu. Bambu's X2D first-layer guide
suggests steps of about 0.02 to 0.05 mm. If the first layer on the glacier plate still looks wrong
after slicing as Smooth PEI, this is the knob, not First Layer Inspection.

## Where the switches live, and whether they stay set

- **On the printer screen:** Settings > Print Options. Bambu's X2D detection page says so for each
  check (§5.2, §6.3, §8.3). The 01.01.00.00 release note puts the displacement switch under
  "Settings -> Print Options -> AI Detection", so the AI ones may sit in a submenu.
- **In Bambu Studio:** Device tab > Print Options. The labels are "Build Plate Detection" with
  "Type Detection" and "Alignment Detection" under it, "Foreign Object Detection", "Printed Part
  Displacement Detection", the AI detections, and filament tangle. Idle Heating Protection is in a
  separate Safety Options dialog.
- **In Bambu Handy:** not found. Neither pass nor I found a Bambu page that names Handy as a place
  for these switches.

**Do they stay set?** Probably yes, but no Bambu page says so. What the code shows: Studio sends a
switch command, then reads the switch's state back from the printer's status report, and keeps
nothing on its own side. So the setting lives on the printer and the screen, Studio and Handy all
see the same value. That is an inference from code. Whether it survives a restart or a firmware
update is not written anywhere found; firmware 01.01.00.00 did turn one check on by default
("Build Plate Presence Detection enabled by default"), so an update can change a setting. Check the
screen after a restart or update.

## Can our CLI change plate settings

- **The slice's plate type: yes, today.** `bambu slice plate` and `bambu slice compose` take
  `--plate-type hot_plate` (Smooth PEI / High Temp), and the send passes the slice's plate type to
  the printer. See [the CLI flags](../../tools/bambu/FLAGS.md).
- **The printer's options: no command today.** Studio's protocol for them is below. A read-only
  `bambu options show` would only read the status report, which `bambu status show` already
  receives, so it adds no new risk. Writing an option changes the printer and, like a print send,
  needs Omar's go.

### The command and state bits, for a future `bambu options show`

**Untested on Omar's printer.** Everything here is read from Bambu Studio's source at commit
[da8b44e](https://github.com/bambulab/BambuStudio/tree/da8b44ee34dd349f2ae0df3f1cbae366df482354)
(`DevPrintOptions.cpp`, `DevUtil.h`) and checked against a community X2D status sample. It has not
been seen on Omar's X2D.

**Switch command** (what Studio sends; for a later write command, not for `show`):

```json
{"xcam": {"command": "xcam_control_set", "sequence_id": "<n>",
          "module_name": "<module>", "control": true, "enable": true,
          "print_halt": true, "halt_print_sensitivity": "<low|medium|high, only for checks with a level>"}}
```

- `enable` and `print_halt` are marked "old protocol" in the source; `control` carries the same
  on/off value as `enable`.
- After a toggle, Studio keeps its own value for 3 seconds and ignores the read-back.

**Module names**, as sent on the wire:

| Switch | `module_name` |
|---|---|
| Type Detection (and the older single "build plate marker" switch) | `buildplate_marker_detector` |
| Alignment Detection | `plate_offset_switch` |
| Foreign Object Detection | `fod_check` |
| Printed Part Displacement | `model_movement_check` |
| First Layer Inspection (not shown for the X2D) | `first_layer_inspector` |
| Spaghetti / pile-up / clumping / air printing | `spaghetti_detector` / `pileup_detector` / `clump_detector` / `airprint_detector` |

The names `build_plate_type_detector` and `build_plate_align_detector` are only names of functions
inside Studio (they show up in the app as compiled symbols). They are never sent to the printer.

Idle Heating Protection is a different command:
`{"print":{"command":"set_against_continued_heating_mode","enable":true}}`.

**State bits** (bit 0 is the lowest):

- `print.xcam.cfg`, an integer:
  - bit 7 spaghetti on, bits 8–9 its level (0 low, 1 medium, 2 high)
  - bit 10 pile-up on, bits 11–12 its level
  - bit 13 clumping on, bits 14–15 its level
  - bit 16 air printing on, bits 17–18 its level
  - **bit 20 alignment on**
  - **bit 21 foreign objects on**
  - **bit 22 displacement on**
- `print.xcam.buildplate_marker_detector`, a true/false: **Type Detection on**.
- `fun2`, a hex string, says which checks the printer supports: bit 2 alignment, bit 13 foreign
  objects, bit 14 displacement.

The community X2D sample (ha-bambulab's `MOCK-X2D.json`) has `xcam.cfg = 8089015`. Decoded, that is
every AI check on at level 1 (medium), and bits 20, 21 and 22 all on. Its `fun2 = "B7B77"` has bits 2,
13 and 14 set. It also has `buildplate_marker_detector: true` and `first_layer_inspector: true`, so
the first-layer field is present in the status even though Studio does not offer the switch for the
X2D.

**Answering an error from the CLI** (pass B, from Studio's `DeviceManager.cpp`; I did not re-check
this one): `{"print":{"command":"ignore","err":"<code in decimal>","param":"reserve",...}}`, and the
same with `"resume"`.

## Open questions

- **Why both plates read P0101.** No Bambu source explains `cur_id` or `base`. Studio's code never
  reads the plate's `cur_id`, and "P0101" is not in the Studio app. The same `cur_id: P0101`,
  `base: 4` block appears in the community status samples for the X2D, the H2D and the H2S, which
  suggests a common or default value rather than a reading of the glacier's marker. Both passes
  guessed it may be the last plate read; nobody has checked. A status read with the glacier plate in
  and Type Detection on would settle it.
- **Whether the screen offers an ignore for 806E.** The X2D error table gives 806E only action 21,
  and Studio has no button for action 21. Bambu's H2 detection page says to clear the bed and press
  "Continue". What the X2D screen shows is not found. Switching the check off avoids the question.
- **Who makes the glacier plate.** "Glacier" is a BIQU product name, but Panda and others sell
  "Glacier" plates too, with different marker stickers. Treating it as BIQU is an assumption.
- **Why the marker fails.** Bambu's plates page says the X2D cannot read first-generation plate
  codes. Pass B guessed the glacier's strip is an older code the X2D does not accept. That fits the
  plates page and a P2S report (the same Glacier plate fails on a P2S and reads on a P1S, 232948 #14),
  but it is an inference.
- **Whether newer firmware fixes the false 806E.** The reports start with 01.02.00.00. One user went
  back to older firmware and ran the camera calibration, and the false alarms stopped (257780 #4).
  No later release note was found that addresses it.
- **Whether Bambu sells a smooth plate for the X2D now.** See the last disagreement below.

## Agreement and disagreement

**Where the two passes agree** (and the source supports both):

- Foreign Object Detection off for a third-party plate (X2D page §5.2; three X2D forum threads).
- Type Detection off or ignored per print.
- Alignment, displacement, AI checks, tangle and idle heating stay on.
- Slice as Smooth PEI / High Temp; the 0.02 mm Textured trim. I re-read the trim: +0.002 vs +0.022 at
  70 °C or below, -0.003 vs +0.017 above. Both passes quoted it correctly.
- PLA at 55 °C.
- The module names `buildplate_marker_detector`, `plate_offset_switch`, `fod_check`,
  `model_movement_check`, and the state bits 20, 21, 22.
- Switches set on the screen (Settings > Print Options) or in Studio; Handy not found; persistence
  inferred from code, not documented.

**Where they disagree, or a point needed settling:**

1. **First Layer Inspection on the X2D.** A listed it among the checks to keep on. B said the X2D
   does not offer it. **The source supports B.** The X2D printer file in Studio (the clone and the
   installed 02.08.02.61) says `support_first_layer_inspect: false`, and Studio shows the switch
   only when that is true. Bambu's X2D detection page has no first-layer section, and the same printer file says
   `support_lidar_calibration: false` (the X1's first-layer inspection uses its lidar). Hedge: a live printer can override the bundled file,
   and the community X2D sample does carry a `first_layer_inspector` field, so this is medium
   confidence until the screen is looked at.
2. **Which check raises 0500-8062.** A said the type check; B listed it under type detection too,
   and called the switch the "marker detector". **These are the same switch.** Bambu's X2D page lists
   8062 under §6 Build Plate Type Detection (the corner camera), next to 8051. In Studio, the "Type
   Detection" switch sends `buildplate_marker_detector`. Alignment is a different check (§8, toolhead
   camera, error 808C). So 8062 is the type check, which on the wire is the marker detector, and not
   alignment.
3. **The module names given to the checker** (`build_plate_type_detector`,
   `build_plate_align_detector`). Neither pass used them, and **the source shows they are function
   names inside Studio**, not what is sent. The wire names are `buildplate_marker_detector` and
   `plate_offset_switch`.
4. **Whether the X2D start G-code switches plate detection on.** A listed
   `build_plate_detect_flag=1` among the checks the start G-code runs. **The source supports B:** that
   line is commented out (`;M1002 set_flag build_plate_detect_flag=1`), and the X2D template has no
   `judge_flag` around the plate checks. A's point that the printer's switches decide whether each
   check acts is still an inference.
5. **What to do first on 8062.** A: clean the marker and block outside light once, then ignore or
   switch off. B: switch off or ignore. **Both are sourced.** Bambu's 8062 advice includes blocking
   outside light (X2D page §6.4, and the error text itself). Bambu's X2D intro page tells you to press
   Ignore or disable plate detection for a plate it cannot recognise. For a plate whose marker the X2D
   may never read, the intro page is the closer fit, so the table says off or ignore, with cleaning as
   an optional first try.
6. **Slice-as confidence.** A said medium-high, B high. **The source supports high for "not
   Textured"** (the G-code is read directly). Which non-Textured type is right rests on user reports
   about BIQU plates, and the maker is not known, so the table keeps medium-high for Smooth PEI
   specifically.
7. **What Bambu sells as a smooth plate for the X2D.** A, from forum 258878 (2026-08-28, one X2D
   owner): Bambu's smooth PEI plate is "not for sale any more", and a dual PEI plate is available. B,
   from the Bambu plates page: Smooth PEI comes in a second generation that works with the P2S and X2D.
   **Not settled.** I re-read both: the wiki implies a second-generation Smooth PEI plate exists; the
   forum owner could not buy one, in an unknown region. Neither pass, nor I, could read the Bambu
   store (its pages carry no product data in the HTML). Check the store before buying.
8. **The P2S "plate not detected" page.** B called it a P2S page, not an X2D one. Its title is
   "0500-4095： P2S/X2D", so it covers the X2D too. But it is about error 0500-4095 ("No print plate
   detected" in the X2D table), not 8062. Its advice, "If you are using a third-party build plate,
   simply ignore this message", fits the same pattern but is not about our error.

**What only one pass found** (flagged, not dropped):

- *Only A:* the 01.01.00.00 note that plate presence detection is on by default (I re-read it:
  confirmed). The X2D error table also has 0C008009 "marker not found" (not re-checked). Forum 172793
  (a real 806E caused by packing foam; not re-opened). OpenBambuAPI's module list predates the
  X2D switches (not re-opened). The ha-bambulab X2D sample (re-read: confirmed).
- *Only B:* the H2D start G-code branches its foreign-object check on plate type, `M972 S26` for
  Textured and `M972 S36 ... X1` otherwise, and wraps plate detection in `judge_flag` (I re-read it:
  confirmed). B's further guess, that S36 is a smooth-plate mode and the X2D's missing branch is why
  smooth plates false-trigger, is **an inference with no source**. Also only B: the H2 page's "Disabling
  it skips this check" (confirmed), and the HMS ignore and resume command shape (not re-checked).
- *Neither:* Bambu's X2D intro page, which I found while checking. It is the most direct Bambu
  statement for this case: "X2D printers come with a Bambu Textured PEI Plate and support all current
  Bambu 256*256mm build plates, but cannot recognize first-generation plates. If the device indicates
  unrecognized plate type, manually select "Ignore" or disable plate detection on the screen."
- *Neither:* firmware 01.01.00.00's "First Layer Quality Calibration", the nozzle height fine-tune.

**Snippets that I fetched in full, and what they said:**

- Forum 204784 (B had a snippet; A fetched it): confirmed. "With my Biqu Glacier plate I use the
  Smooth PEI Plate /High Temp Plate setting", and the printer reads the plate code.
- Forum 113355 (B had a snippet; A fetched it): confirmed. #8: Bambu's new plates have printed
  markers, BIQU plates come with stickers.
- Forum 172203 (B had a snippet): the first post is a user's copy of the H2D 01.01.02.08 release
  notes, including "Optimized foreign object detection on smooth PEI buildplate". Second-hand, and H2D
  only.

## Sources

"Re-opened" means I read it again for this file. "Relied on" means I am taking a pass's word.

| Source | What it supports | Read as | Re-opened? |
|---|---|---|---|
| [Bambu wiki, X2D intelligent detection](https://wiki.bambulab.com/en/x2d/manual/intelligent-detection) | 806E and third-party plates (§5.2), 8062 under type detection (§6), alignment and 808C (§8), switch locations | fetched | yes |
| [Bambu wiki, X2D intro](https://wiki.bambulab.com/en/x2d/manual/x2d-intro) | X2D cannot read first-generation plates; press Ignore or disable plate detection | fetched | found by the checker |
| [Bambu wiki, build plates](https://wiki.bambulab.com/en/filament-acc/acc/plates) | plate types; second-generation codes for P2S/X2D; "select 'Resolved' ... or disable" | fetched | yes |
| [Bambu wiki, X2D firmware history](https://wiki.bambulab.com/en/x2d/manual/x2d-firmware-release-history) | 01.01.00.00 toggles and defaults; 01.02.00.00 camera calibration dropped | fetched | yes |
| [Bambu wiki, X2D first-layer guide](https://wiki.bambulab.com/en/x2d/troubleshooting/first-layer-printing-optimization-guide) | the 0.02–0.05 mm fine-tune steps | fetched | found by the checker |
| [Bambu wiki, H2 intelligent detection](https://wiki.bambulab.com/en/h2/manual/intelligent-detection) | H2D single switch, H2C split; "Disabling it skips this check" | fetched | yes |
| [Bambu wiki, P2S/X2D plate not detected](https://wiki.bambulab.com/en/p2s/troubleshooting/build-plate-not-detected) | 0500-4095; ignore for third-party plates | fetched | yes |
| [Bambu wiki, print options](https://wiki.bambulab.com/en/studio-handy/print-options) | set on the screen or in Studio (X1/A1-era page) | fetched | yes |
| Studio X2D printer file `N6.json` ([clone](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/resources/printers/N6.json), and the installed 02.08.02.61) | no first-layer inspection; marker detection type 2; no lidar | fetched | yes |
| [Studio `PrintOptionsDialog.cpp`](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/PrintOptionsDialog.cpp) | switch labels; first-layer switch hidden when unsupported | fetched | yes |
| [Studio `DevPrintOptions.cpp`](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/DeviceCore/DevPrintOptions.cpp) | command shape, module names, state bits | fetched | yes |
| [Studio `DeviceErrorDialog.hpp`](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/DeviceErrorDialog.hpp) | action 27 Ignore and Resume, 28 Problem Solved and Resume; no action 21 | fetched | yes |
| Studio X2D error tables (`hms_en_20P.json`, `hms_action_20P.json`, ver 202511162200, in the installed app) | 806E action 21; 8062 actions 27, 28; 4095 text | fetched | yes |
| Studio app binary (02.08.02.61) | wire names present as strings; the `build_plate_*_detector` names only inside compiled symbols; no "P0101" | fetched | found by the checker |
| [X2D 0.4 start G-code](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/resources/profiles/BBL/machine/Bambu%20Lab%20X2D%200.4%20nozzle%20template%20machine_start_gcode.json) | the 0.02 mm trim; plate checks; commented-out detect flag | fetched (clone and installed app match) | yes |
| H2D 0.4 start G-code (same folder) | S26/S36 branch; `judge_flag` | fetched | yes |
| [Studio `fdm_filament_pla.json`](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/resources/profiles/BBL/filament/fdm_filament_pla.json) | PLA 55 °C smooth PEI and textured, 35 °C cool | fetched | yes |
| Studio `SafetyOptionsDialog.cpp`, `PrintConfig.cpp` labels, `DeviceManager.cpp` ignore/resume | Idle Heating in Safety Options; "Smooth PEI Plate / High Temp Plate" label; ignore command | fetched by the passes | relied on |
| [ha-bambulab](https://github.com/greghesp/ha-bambulab) `MOCK-X2D.json` (and the H2D, H2S mocks) | the X2D status sample; P0101 in all three | fetched | yes |
| [OpenBambuAPI](https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md), [open-bamboo-networking](https://github.com/ClusterM/open-bamboo-networking) | module lists (A; the "NP firmware" note is a snippet) | fetched by A, one snippet | relied on |
| [Forum 69/283](https://forum.bambulab.com/t/69/283) | X2D, 01.02.00.00, false 806E on Glacier and Frostbite | fetched | yes |
| [Forum 257780](https://forum.bambulab.com/t/257780) | X2D false 806E on third-party plates; rollback and calibration stopped it (#4) | fetched | yes |
| [Forum 256670](https://forum.bambulab.com/t/256670) | X2D beta: Glacier owner "had to turn off detection" (#8); carbon-fibre plate same (#11) | fetched | yes |
| [Forum 164540](https://forum.bambulab.com/t/164540) | H2D Glacier: "Should be High Temp" (#4); +5 °C (#11); the code on the plate (#12) | fetched | yes |
| [Forum 259088](https://forum.bambulab.com/t/259088) | Glacier stickers mark it as smooth PEI (#7, #9) | fetched | yes |
| [Forum 204784](https://forum.bambulab.com/t/204784) | Glacier sliced as Smooth PEI, code read | fetched | yes (B had a snippet) |
| [Forum 205851](https://forum.bambulab.com/t/205851) | Glacier sliced as smooth on an H2D (#2); a P2S Cool Plate crash, cause unsettled (#4) | fetched | yes |
| [Forum 219369](https://forum.bambulab.com/t/219369) | Panda CryoGrip Glacier: cool-plate code recommended; 55 °C; "BIQU recommends 45/55" second-hand | fetched | yes |
| [Forum 232948](https://forum.bambulab.com/t/232948) | Bambu's own Engineering plate unread on H2D; Glacier fails on P2S, reads on P1S (#14) | fetched | yes |
| [Forum 113355](https://forum.bambulab.com/t/113355) | turning plate detection off; printed markers vs stickers (#8) | fetched | yes (B had a snippet) |
| [Forum 172203](https://forum.bambulab.com/t/172203) | user's copy of H2D 01.01.02.08 notes | fetched | yes (B had a snippet) |
| [Forum 258878](https://forum.bambulab.com/t/258878) | Bambu smooth PEI "not for sale any more" (one owner, region unknown) | fetched | yes |
| Forum 172793, 113809, 163705, 172971, 228520 | real 806E from foam; SuperTack marker unread; early H2D plate stock; marker codes differ by printer | fetched by the passes | relied on |
| Forum 146076, 151550, 185142, 254247, 258343, 203799, 210371, 218582 | 50 °C on glacier; copied QR stickers; plates without markers; Engineering plate Q1 2026 | **snippet** (pass B) | no, flagged |

Not searched by anyone: BIQU's and Panda's own sites, Reddit, the Bambu store's live stock.
Nothing here says what they publish.
