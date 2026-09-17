---
produced: 2026-09-17
produced-by: design task — auto-pull the print profile header from the printer (Claude, real WebSearch/WebFetch)
feeds: docs/bambu-header-autopull-design.md (the CLI/skill design that fills the bench-sheet header)
scope: for each Plate-1 bench-sheet "profile header" field, find the machine-readable source (MQTT report frame / info.get_version / AMS tray / sliced .3mf metadata / BambuStudio --version) — or establish it is genuinely manual
---

# Auto-pulling the print profile header — field→source survey

## What this grounds, and the proxy caveat

The Plate-1 bench sheet ([`../prints/plate-1-bench-sheet.md`](../prints/plate-1-bench-sheet.md))
opens with a **profile header** the operator fills **by hand at the printer**: machine / firmware /
material brand·type·colour / spool id / nozzle diameter·type / layer height / slicer profile /
ambient room temp / enclosure state / date / caliper. This survey asks, field by field: **which of
those can `tools/bambu` read programmatically**, and from where.

**Proxy caveat (repo K1/K2/K10).** No public source names the **X2D** specifically. Its sibling is
the **H2 family** (H2D / H2S / H2C), which shares firmware line `01.02.00.00`. A fact sourced from
H2/H2D/X1/P1 material and **not** yet observed on this X2D is tagged **[H2-PROXY — UNCONFIRMED]**;
a fact already observed on *this* machine in this project is tagged **[CONFIRMED-IN-REPO]** with the
memory/PR that observed it. A field the printer does not sense at all is tagged **[MANUAL]**. The
transfer sentence for every H2-proxy row is the same and must be written where it is used: *the X2D
shares the H2D's `01.02.00.00` firmware track and MQTT/AMS report shape, so an H2D field is
plausible on the X2D — but "plausible" is not "observed," and the report frame has already diverged
once here (`vir_slot` array vs the H2 `vt_tray` object, PR #192).*

## Sources consulted (2026-09-17, real fetch)

- **Doridian/OpenBambuAPI — `mqtt.md`** (fetched 2026-09-17): the canonical community MQTT
  reverse-engineering reference. Confirms the `info`/`get_version` response module shape
  (`name`, `sw_ver`, `sn`, `hw_ver`) and that the `pushing.pushall` / `push_status` report frame
  carries `nozzle_diameter` (example `"nozzle_diameter": "0.4"`), `chamber_temper`
  (example `"chamber_temper": 24.0`), and the AMS tray fields `tray_uuid` / `tray_type` /
  `tray_color` / `tray_sub_brands` / `tray_info_idx`. `nozzle_type` appears in the
  `system.set_accessories.nozzle` **request**, not clearly in the status frame.
  https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md
- **BambuTools/bambulabs_api — MQTT client docs** (fetched 2026-09-17): documents `set_nozzle_info`
  taking `nozzle_type` and `nozzle_diameter` (default `0.4`), i.e. nozzle geometry is a
  device-side accessory setting the report can echo — but read-back on H2D is untested there
  (the library README marks H2D "not tested yet"). Carry that hedge.
  https://bambutools.github.io/bambulabs_api/api/mqtt_client.html
- **greghesp/ha-bambulab + Home Assistant community MQTT thread** (fetched 2026-09-17): confirms
  the two-phase report (a full snapshot on pushall, then partial `push_status` deltas), and — the
  load-bearing hedge for "ambient" — that **`chamber_temper` is model-dependent**: X1-era firmware
  reports the flat `chamber_temper`, while a newer (P2S-generation) firmware moved the chamber
  reading under a `device.ctc` ("chamber temperature control") object. Whether the X2D exposes the
  flat field, the nested one, or a door/enclosure state is **unconfirmed** until read.
  https://github.com/greghesp/ha-bambulab ·
  https://community.home-assistant.io/t/bambu-lab-x1-x1c-mqtt/489510
- **maziggy/bambuddy #3109 + greghesp/ha-bambulab #523** (fetched 2026-09-17): the spool identity
  fields — **`tray_uuid`** is the value Bambu Studio shows as the tray **serial number (SN)**;
  **`tag_uid`** is the RFID id Bambu Handy shows. Only **official Bambu Lab RFID spools** populate
  these; third-party / refilled / re-spooled filament is skipped (no RFID → no id).
  https://github.com/maziggy/bambuddy/issues/3109 ·
  https://github.com/greghesp/ha-bambulab/issues/523
- **printago.io — "3MF File Format"** (fetched 2026-09-17): a BambuStudio/Orca `.3mf` is a ZIP; the
  slicer identity lives in `Metadata/project_settings.config` (a **flat JSON of every resolved
  slicer setting** — `printer_model`, `printer_variant`, and the preset-id keys), the slicer
  **version** is the `<metadata name="Application">` value in `3D/3dmodel.model`
  (e.g. `BambuStudio-01.10.00.89`) and/or the `X-BBL-Client-Version` header in
  `Metadata/slice_info.config`, and per-plate filament/time estimates live in
  `Metadata/slice_info.config`. https://printago.io/blog/3mf-file-format
- **bambulab/BambuStudio — Command-Line-Usage wiki** (fetched 2026-09-17): the headless binary
  supports a version query, and the standard PrusaSlicer/BambuStudio preset-id keys
  (`printer_settings_id`, `print_settings_id`, `filament_settings_id`, `layer_height`,
  `nozzle_diameter`) are the resolved keys serialized into `project_settings.config`.
  https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage
- **[CONFIRMED-IN-REPO]** — memory `bambu-x2d-bringup` + PRs #179 / #188 / #192: `setup discover`
  read **firmware `01.02.00.00`** and **serial `20P6AJ641401412`** off the device (SSDP, receive-
  only); `status show` proved the pushall frame carries the standard temp/state/layer fields;
  `filament` proved `print.ams.ams[].tray[]` carries `tray_type` / `tray_sub_brands` /
  `tray_color` (RRGGBBAA) / `tray_info_idx` (`GFA00`) / `remain`, and the external spool arrives as
  `print.vir_slot` (array), not `vt_tray`.

## Field-by-field findings

Each row: bench-sheet field → the source we would read → status for the X2D.

1. **Machine** (preset display name). Source: the sliced `.3mf` — `Metadata/project_settings.config`
   `printer_settings_id`, cross-checked against the plate G-code header `printer_model = Bambu Lab
   X2D`. Also derivable from `BAMBU_MODEL=x2d` env. **[CONFIRMED-IN-REPO]** — we slice X2D plates and
   the G-code reads `printer_model = Bambu Lab X2D` (PR #189).

2. **firmware**. Two routes. (a) `setup discover` SSDP already reports it — **[CONFIRMED-IN-REPO]**
   `01.02.00.00`. (b) MQTT `info` `{ "command": "get_version" }` → report frame `module[]` where the
   `ota` module's `sw_ver` is the printer firmware (and each module carries its own `sn`/`hw_ver`).
   The get_version *value* is confirmed for the machine (via SSDP); the **MQTT get_version round-trip
   is [H2-PROXY — UNCONFIRMED]** on the X2D (our CLI has never published it — reads today are
   pushall-only).

3. **Material — brand**. Source: AMS `tray_sub_brands` (e.g. "PLA Basic") plus the Bambu vendor
   implied by `tray_info_idx` (the `GF*` profile ids are Bambu's). **[CONFIRMED-IN-REPO]** for
   **Bambu RFID spools** (read back "PLA Basic" · `GFA00`). For a **third-party / refilled spool
   there is no RFID and no brand** — that case is **[MANUAL]** (the printer cannot know it).

4. **Material — type**. Source: AMS `tray_type` ("PLA"). **[CONFIRMED-IN-REPO]**.

5. **Material — COLOUR**. Source: AMS `tray_color`, `RRGGBBAA` hex → `#RRGGBB`.
   **[CONFIRMED-IN-REPO]** (`#F5547C` read on slot 0). Note: the frame gives the **hex, not a colour
   name** — the operator may still want to write the human name, but the load-bearing value (the hex
   that "changes flow") is machine-read.

6. **Spool id**. Source: AMS `tray_uuid` (the tray SN Bambu Studio shows; `tag_uid` is the Handy
   RFID id). **[H2-PROXY — UNCONFIRMED]**: `tray_uuid` was **not** among the fields observed on the
   X2D on 2026-09-17 (we saw `tray_type`/`tray_sub_brands`/`tray_color`/`tray_info_idx`/`remain`),
   and it only populates for **official Bambu RFID spools** — third-party spools stay **[MANUAL]**.

7. **Nozzle — diameter**. Two routes. (a) sliced `.3mf` `nozzle_diameter` / plate G-code
   `nozzle_diameter = 0.4,0.4` — **[CONFIRMED-IN-REPO]** (dual-nozzle value read from our X2D
   slice). (b) pushall frame `nozzle_diameter` (OpenBambuAPI example `"0.4"`) — **[H2-PROXY —
   UNCONFIRMED]** on the X2D: our `pick()` list does not surface it yet, so we have never observed it
   in *this* machine's frame. The `.3mf` route is the reliable one; the frame is the cross-check.

8. **Nozzle — type** (brass / hardened / CHT). Source: pushall `nozzle_type` (or the
   `set_accessories.nozzle` accessory setting the frame echoes; default `0.4`/stainless in
   `bambulabs_api`). **[H2-PROXY — UNCONFIRMED]** — not observed on the X2D frame; may require the
   operator to have set the accessory in Studio/Handy first, so treat as **best-effort machine, else
   MANUAL**.

9. **Layer height**. Source: sliced `.3mf` `layer_height` / plate G-code header. **[CONFIRMED-IN-
   REPO]** for the value chosen ("0.20mm Standard @BBL X2D" → `layer_height` 0.2). Not a printer-
   frame field (the printer only knows it mid-print); it is a **slice-file** fact.

10. **Profile** (slicer profile name verbatim). Source: sliced `.3mf` — `print_settings_id`
    (process, e.g. "0.20mm Standard @BBL X2D") + `filament_settings_id` (e.g. "Bambu PLA Basic @BBL
    X2D 0.4 nozzle"). **[CONFIRMED-IN-REPO]** — these are exactly the preset names our `slice`
    resolves and the bench-sheet pre-flight names.

11. **Slicer version**. Source: BambuStudio `--version` (**2.08.02.61** installed here), and/or the
    `.3mf` `3D/3dmodel.model` `Application` metadata (`BambuStudio-<ver>`) / `slice_info.config`
    `X-BBL-Client-Version`. **[CONFIRMED-IN-REPO]** — the installed build is known and the `.3mf`
    stamps it.

12. **settings changed from the profile**. **[MANUAL]** — the operator's narration of deliberate
    deviations (e.g. MC-4 supports OFF, MC-6 no brim). In principle a diff of the `.3mf`'s resolved
    settings against the stock preset JSON could compute this, but that is a separate, heavier tool
    and out of scope here; the header wants the operator's *intent*, not a raw setting diff.

13. **Ambient — room temp**. **[MANUAL]** — the printer does **not** sense the room. It *may* sense
    the **chamber** (`chamber_temper`, already surfaced by `status show`), but **chamber ≠ room
    ambient**, and even chamber is model-dependent (flat `chamber_temper` on X1-era vs `device.ctc`
    on newer firmware — **[H2-PROXY — UNCONFIRMED]** which the X2D uses). So the header's *room*
    field stays a blank; chamber can be offered as a **clearly-labelled proxy**, never as a
    substitute for the room reading.

14. **Ambient — enclosure open/closed**. **[MANUAL]** — no reliable door/enclosure-state field was
    found in the community field dictionaries for the H2 family; the operator records it. (If a
    door-state field surfaces on the live X2D frame, it graduates to machine-read — a validation
    observation, not an assumption.)

15. **Date**. Machine-trivial — the CLI's own system clock (UTC now). Machine-read.

16. **Caliper — make / resolution / zeroed?**. **[MANUAL]** — a property of the operator's
    instrument, nothing the printer or slicer knows.

## Summary of the verdict

Machine-readable without operator transcription (from printer frame, AMS, the sliced `.3mf`, the
installed slicer, or the clock): **Machine, firmware, material type, colour, nozzle diameter, layer
height, profile (process+filament), slicer version, date** — nine, all **[CONFIRMED-IN-REPO]** or
confirmed-value. **Conditional** (machine-read only for official Bambu RFID spools, else manual):
**material brand, spool id**. **Best-effort machine, else manual**: **nozzle type**. **Genuinely
[MANUAL]** (unsensed or operator-side): **settings-changed narration, ambient room temp, enclosure
state, and the three caliper fields**. Chamber temp is available as a labelled proxy for ambient,
not a replacement.

## What is unproven and must be validated on the live X2D (do not harden)

Three reads are H2-proxy-plausible but **not yet observed on this X2D's frame**, and the design
isolates them as a validation observation rather than baking them in:

- the **MQTT `info`/`get_version`** round-trip and its `module[].sw_ver` shape;
- **`nozzle_diameter`** and **`nozzle_type`** in *this* machine's pushall frame (only the `.3mf`
  values are confirmed today);
- **`tray_uuid`** (spool id) presence on the X2D AMS tray, and which chamber field
  (`chamber_temper` vs `device.ctc`) the X2D reports.

Each is written **unconfirmed** wherever it appears until `bambu header` is run against the live
machine and the raw frame inspected — the same honesty the transport survey applied to X2D
dual-nozzle.
