<!-- provenance: date=2026-09-16; produced-by=claude-opus-4-8 research subagent; feeds=docs/print-model-design.md -->

# print-model skill — grounded web research

Research for a **print-model** skill driving a Bambu Lab **X2D** dual-nozzle
printer (firmware 01.02.00.00) over the LAN.

**Proxy caveat (repo K2/K1 rules):** No public documentation names the **X2D**
specifically. Its sibling is the **H2 family** (H2D / H2S / H2C), which shares
firmware line 01.02.00.00. Where a fact is sourced from H2/H2D or generic
Bambu material and NOT confirmed on X2D hardware, it is tagged
**[X2D-UNCONFIRMED — H2-proxy]**. Facts already proven in *this* project
(status reads over MQMQTT/TLS 8883) are tagged **[PROVEN-IN-REPO]**.

Transport already proven here: status reads over first-party MQTT/TLS 8883
(user `bblp`, access-code password, `rejectUnauthorized:false`), topics
`device/<serial>/report` (sub) and `device/<serial>/request` (pub),
`pushing.pushall` for a full frame. **Dispatch (submitting + starting a print)
is NOT yet ported** off the defunct griches MCP — see Topic 1 signing caveat.

---

## 1. LAN print submission protocol (FTPS upload + MQTT project_file)

The LAN flow is two steps: **FTPS** (implicit TLS, port **990**) upload of the
sliced `.gcode.3mf` to the printer's storage, then an **MQTT** `project_file`
command on `device/<serial>/request` that names the plate file to start.

- https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md — (fetched
  2026-09-16) Primary reverse-engineering reference. Verbatim `project_file`
  request payload shape:
  ```json
  { "print": {
    "sequence_id": "0", "command": "project_file",
    "param": "Metadata/plate_X.gcode",
    "project_id": "0", "profile_id": "0", "task_id": "0",
    "subtask_id": "0", "subtask_name": "", "file": "",
    "url": "file:///mnt/sdcard", "md5": "",
    "timelapse": true, "bed_type": "auto", "bed_levelling": true,
    "flow_cali": true, "vibration_cali": true, "layer_inspect": true,
    "ams_mapping": "", "use_ams": false } }
  ```
  Note the field is spelled **`bed_levelling`** (double-L) in this payload.
  `param` points at the plate gcode *inside* the uploaded 3mf
  (`Metadata/plate_1.gcode`); `url` is the storage root (`file:///mnt/sdcard`
  for SD, or a cache path). [X2D-UNCONFIRMED — H2-proxy for exact field set on
  H2/X2D firmware]

- https://github.com/schwarztim/bambu-mcp — (fetched 2026-09-16) MCP server
  doing exactly LAN MQTT control + FTP upload + AMS + camera; a working
  reference implementation of the upload-then-project_file sequence and X.509
  cert auth. Good code cross-check for the FTPS(990)+MQTT(8883) handshake.

- https://forum.bambulab.com/t/printing-gcode-not-sliced-3mf-using-mqtt/172699
  — (fetched 2026-09-16) Community thread: printing a sliced **`.3mf` via
  `project_file` requires Developer Mode / LAN Mode**; plain `.gcode` files and
  all other commands (stop/pause/resume/status/speed/AMS) do not. Load-bearing
  precondition for dispatch.

- https://wiki.bambuddy.cool/features/virtual-printer/ — (fetched 2026-09-16)
  Documents the FTPS-upload-to-storage + MQTT-start model from an
  actively-maintained integration's perspective.

**H2/X2D difference — SIGNED MQTT (load-bearing for dispatch):**
- Bambu's Jan-2025+ **authorization-control firmware (X2D/H2D family, plus
  refreshed P1/X1) rejects UNSIGNED control commands** (error `84033543`).
  Control commands must be **signed RSA-SHA256**, and the signing cert's **CN
  must match the printer's serial**. Status *reads* are unaffected (hence reads
  already work here [PROVEN-IN-REPO]); **print dispatch on X2D will require the
  signing path**, not the plain publish that worked on older firmware.
  - https://github.com/bambulab/BambuStudio/issues/6145 — "MQTT Command
    verification failed, please update Studio or Handy" (fetched 2026-09-16)
  - https://github.com/bambulab/BambuStudio/issues/9344 — same class, newer
    (fetched 2026-09-16)
  [X2D-UNCONFIRMED on the exact error code/cert-CN rule for X2D specifically;
  reported for the H2D/X2D authorization-control firmware family — H2-proxy.]

---

## 2. AMS filament discovery (report-frame `ams` object + `vt_tray`)

The full report frame (from `pushing.pushall`) carries `print.ams.ams[]` (one
entry per physical AMS unit, each with a `tray[]`) and a separate
`print.vt_tray` for the external spool.

- https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md — (fetched
  2026-09-16) Verbatim AMS report shape:
  ```json
  { "ams": [ { "humidity": "4", "id": "0", "temp": "22.7",
      "tray": [ { "id": "0", "tray_type": "PLA", "tray_color": "000000FF",
                  "tray_sub_brands": "", "tray_info_idx": "GFA00",
                  "remain": 0 } ] } ],
    "vt_tray": { "id": "254", "tray_type": "", "tray_color": "00000000",
                 "tray_sub_brands": "", "tray_info_idx": "", "remain": 0 } }
  ```
  Usable per-tray fields to list loaded filament: **`tray_type`** (e.g. "PLA"),
  **`tray_color`** (hex `RRGGBBAA`, alpha typically `FF`), **`tray_sub_brands`**,
  **`tray_info_idx`** (Bambu filament-profile id, e.g. `GFA00`), **`remain`**
  (percent remaining; **`-1` = unknown / no RFID tag**). External spool is
  **`vt_tray`** with sentinel **`id":"254"`**.

- https://github.com/davglass/bambu-cli — (fetched 2026-09-16) Maintained CLI
  reading these AMS fields; cross-check for parsing `ams[].tray[]` and
  `vt_tray`.

- https://wiki.bambuddy.cool/features/ams/ — (fetched 2026-09-16) Notes a tray
  is one slot (AMS slot OR the external spool); on newer firmware the external
  spool may appear under **`print.vir_slot`** rather than / in addition to
  `vt_tray` — watch for both keys.
  [X2D-UNCONFIRMED — H2/X2D dual-nozzle may map trays per-nozzle; the H2D AMS
  had MQTT-validation churn, see below. H2-proxy.]

- https://github.com/bambulab/BambuStudio/issues/7051 — (fetched 2026-09-16)
  H2D firmware 01.01.02.08 caused AMS MQTT-validation errors (slot flips
  filament→empty→filament). Evidence the **H2-family AMS report schema/validation
  differs from X1/P1** — treat `ams` parsing defensively on the H2/X2D line.
  [X2D-UNCONFIRMED — reported on H2D; H2-proxy.]

---

## 3. Print orientation optimization

- https://github.com/ChristophSchranz/Tweaker-3 — (fetched 2026-09-16)
  Headless Python auto-rotate. Default minimizes **support VOLUME** while
  guaranteeing printability; evaluates three criteria: **overhang area, bottom
  (contact) area, contour length**. Parameters trained by an evolutionary
  algorithm. CLI: `-min sur` / `--minimize surfaces` switches the objective to
  minimal support *surface* instead of volume; `--favside` weights a preferred
  facing direction. This is the CLI/headless path.
- https://github.com/ChristophSchranz/Tweaker-3/blob/master/MeshTweaker.py —
  (fetched 2026-09-16) The actual scoring implementation
  (`target_function`, overhang/bottom weighting) — source of truth for the
  heuristic if we reimplement or shell out.
- https://www.researchgate.net/publication/311765131 — (fetched 2026-09-16)
  "Tweaker – Auto Rotation Module for FDM 3D Printing" — the paper behind the
  algorithm (objective: minimize support volume subject to printability).
- Slicer built-in **Auto-Orient**: BambuStudio/OrcaSlicer expose an "Orient"
  action (largest-flat-face-down / minimize supports). See Topic 4 DeepWiki
  link (same subsystem) and OrcaSlicer CLI `--orient` in Topic 4.
  **Note:** other axes (layer-line anisotropy / part strength) are NOT what
  Tweaker or slicer auto-orient optimize — they minimize support/overhang, not
  directional strength. Do not claim orientation tools optimize strength (K1).

---

## 4. Plate arrangement / nesting

- https://deepwiki.com/bambulab/BambuStudio/7.4-auto-arrange-and-orientation —
  (fetched 2026-09-16) Placement is powered by **libnest2d** (a customized fork
  in BambuStudio) implementing **No-Fit-Polygon (NFP)** packing. Auto-arrange
  tries at most **4 angles: 0/45/90/135°**; `spacing` = min gap; in
  **by-object** print sequence the arrange polygon is expanded by
  `max(spacing, extruder_radius)` so the toolhead clears already-printed parts
  (parts spaced much farther than by-layer). Load-bearing for max-copy packing.
- https://wiki.bambulab.com/en/software/bambu-studio/auto-arranging — (fetched
  2026-09-16) Official GUI behavior: `A` arranges all + adds plates as needed;
  `Shift-A` arranges the selected plate only.
- https://www.orcaslicer.com/wiki/cli/cli_actions — (fetched 2026-09-16)
  OrcaSlicer **headless CLI**: transform flags include **`--arrange`,
  `--orient`, `--rotate`, `--scale`**; action flags **`--slice`** (0 = all
  plates, i = plate i), **`--export-3mf`** (writes `.gcode.3mf`),
  `--export-slicedata`, `--export-stls`, `--export-settings`. This is the
  scriptable arrange→orient→slice→export-3mf pipeline that produces the file we
  then FTPS-upload in Topic 1. (Flag names confirmed present; per-flag prose
  for the transform flags was not rendered — verify args against `--help`.)
- https://printago.io/blog/orca-slicer-cli-reference — (fetched 2026-09-16)
  Third-party consolidated CLI reference (headless slicing recipes) — useful
  worked examples; secondary source, cross-check against the wiki above.

**libnest2d** is the shared nesting lib used by PrusaSlicer and Orca/BambuStudio
(NFP bin-packing). [X2D-UNCONFIRMED — H2D's L/R-nozzle-only bed zones affect
arrange; a forum report notes auto-arrange not using H2D L/R-only areas:
https://forum.bambulab.com/t/auto-arrange-with-h2d-wont-use-l-r-nozzle-only-areas/188640
(fetched 2026-09-16). Dual-nozzle bed zoning is an X2D-relevant open item.]

---

## 5. Slicer settings heuristics (infill / supports / brim vs raft)

- https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns — (fetched
  2026-09-16) Official fill-pattern catalog: **8 patterns** — Concentric,
  Rectilinear, Monotonic, Monotonic Line, Aligned Rectilinear, Hilbert Curve,
  Archimedean Chords, Octagram Spiral. (If the doc says "N patterns", enumerate
  or write "the N listed on the wiki" — K2.)
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang —
  (fetched 2026-09-16) **Overhang angle** = angle between inclined surface and
  heatbed; larger threshold angle → more support generated. Grounds the
  "support-threshold angle" knob.
- https://deepwiki.com/bambulab/BambuStudio/6.2-support-generation — (fetched
  2026-09-16) Normal vs **tree** supports: tree branches from a small base to
  contact points, minimizing material/time vs grid; **interface layers** = dense
  smooth cap between support and model. Grounds normal-vs-tree choice.
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings
  — (fetched 2026-09-16) Strength/advance params incl. infill angle guidance
  (large 45–75° angles flatten infill for better horizontal/side strength).
- **Brim vs raft:** no single authoritative Bambu wiki page found; community
  guidance only (e.g.
  https://forum.bambulab.com/t/brim-skirt-raft-settings-for-tree-supports/147071,
  fetched 2026-09-16). **THIN/CONFLICTING SOURCE — flag in doc.** General FDM
  rule (brim = adhesion for small footprints/warp-prone corners; raft = full
  base for very warpy materials / uneven beds) should be attributed to a named
  source, not asserted bare.

---

## 6. Print-defect diagnosis taxonomy

Simplify3D's Print Quality Guide is the canonical named catalog (per-defect
pages with causes + fixes).

- https://www.simplify3d.com/resources/print-quality-troubleshooting/ —
  (fetched 2026-09-16) Index of the full guide (the named defect catalog).
- https://www.simplify3d.com/resources/print-quality-troubleshooting/stringing-or-oozing/
  — (fetched 2026-09-16) Stringing/oozing → retraction. Example per-defect page.
- https://www.simplify3d.com/resources/print-quality-troubleshooting/layer-shifting/
  — (fetched 2026-09-16) Layer shift: open-loop steppers lose position →
  belts/mechanical, speed.
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang —
  (fetched 2026-09-16) Bambu's own print-quality wiki section (overhang, and
  siblings under `.../print-quality/`) — printer-specific troubleshooting to
  pair with Simplify3D's generic taxonomy.

Defects to model (from these): warping / poor bed adhesion, stringing/oozing,
layer shift, under-/over-extrusion, elephant's foot, support scarring,
overhang droop. [Elephant's foot & support-scarring pages exist in the
Simplify3D index; enumerate the exact set you cite rather than "all defects".]

---

## 7. Print-job lifecycle / status prior art

For a `draft → queued → printing → printed → measured → shipped` enum, the
mature prior art models the *machine* portion (queued/printing/done/failed);
`measured`/`shipped` are this project's post-print additions (no prior art).

- https://moonraker.readthedocs.io/en/latest/external_api/history/ — (fetched
  2026-09-16) Moonraker job-history status enum (7 values, verbatim):
  **`in_progress`, `completed`, `cancelled`, `error`, `klippy_shutdown`,
  `klippy_disconnect`, `interrupted`**. Cleanest terminal-vs-active split; note
  it distinguishes *why* a job ended (user cancel vs error vs host death).
- https://docs.octoeverywhere.com/plugin-api/printer-status/ — (fetched
  2026-09-16) Common status API spanning OctoPrint + Moonraker/Klipper: states
  like Idle / Printing / Paused / Complete / Error / Cancelled — the
  cross-system normalized vocabulary.
- https://github.com/MarcinOrlowski/octoprint-monitor/blob/master/docs/states.md
  — (fetched 2026-09-16) OctoPrint's own state set (Operational, Printing,
  Paused, Pausing, Cancelling, Error, Offline, …) — richer transient states
  (Pausing/Cancelling) worth considering if we surface in-flight transitions.
- Bambu cloud/MQTT job state: the report frame's `gcode_state`
  (`IDLE/PREPARE/RUNNING/PAUSE/FINISH/FAILED`) is the device-side enum this
  skill actually reads [PROVEN-IN-REPO transport]; map it onto our lifecycle.
  Documented in the OpenBambuAPI mqtt.md above (Topic 1 link).

---

## 8. Nozzle-diameter selection tradeoffs (0.2 / 0.4 / 0.6 / 0.8 mm)

The X2D ships all four nozzle profiles. Core tradeoff axis: **smaller = finer
detail / thinner min wall / slower; larger = more flow / faster / stronger,
coarser detail.** [X2D-UNCONFIRMED that all four ship *per-nozzle on the
dual-tool X2D specifically* — the four-diameter lineup is the standard Bambu
range (H2/X1/P1/A1); H2-proxy. Dual-nozzle X2D can also mix two diameters at
once — see Orca mixed-nozzle link below.]

- https://wiki.bambulab.com/en/filament-acc/acc/nozzles — (attempted fetch
  2026-09-17; returned **HTTP 402 / bot-blocked**, content via WebSearch
  index 2026-09-17) Official Bambu nozzle intro. Grounded use-case split:
  **0.2 mm** miniatures / jewelry / fine text; **0.4 mm** general-purpose
  standard; **0.6 mm** carbon-fiber & abrasive filaments / speed; **0.8 mm**
  rapid prototyping / large layer heights. "A nozzle can reliably reproduce
  features roughly equal to its diameter and no smaller" (min-feature floor).
  [Direct-fetch blocked — quote is from the search index, not a rendered page;
  re-verify the page before pinning a load-bearing number (K4/D3).]

- https://wiki.bambulab.com/en/software/bambu-studio/layer-height — (fetched
  via search 2026-09-17) Bambu's own layer-height page; grounds the
  **layer-height ≈ 25–75 % of nozzle diameter** rule of thumb and per-nozzle
  sweet spots (0.4 nozzle ≈ 0.10–0.28 mm; 0.8 nozzle comfortably 0.4–0.6 mm).
  [Confirm exact endpoints on the live page.]

- https://www.orcaslicer.com/wiki/guides/mixed_nozzle_sizes — (fetched
  2026-09-17) OrcaSlicer mixed-nozzle guide — directly relevant to a
  dual-nozzle X2D. **Line width should be set as a % of nozzle diameter**
  (0.4 mm line on a 0.4 mm nozzle = 100 %; 0.48 mm = 120 %) so the slicer
  auto-scales per extruder. Example multi-nozzle roles it gives: 0.4 standard,
  0.6 "big nozzle for faster surface", 0.2 "small nozzle for fine details at
  walls", 1.0 "extra-large for very fast infill". **Pressure advance changes
  per nozzle size** — each diameter needs its own calibration. Does NOT give
  per-nozzle layer-height numbers.

- https://blog.uavmodel.com/3d-printer-nozzle-size-comparison-0-2mm-vs-0-4mm-vs-0-6mm-vs-0-8mm-detail-speed-and-strength-2026-guide/
  — (fetched via search 2026-09-17) Third-party head-to-head across all four:
  a **0.6 mm cuts print time ~30–40 % vs 0.4 with negligible detail loss on
  functional parts**; 0.2 gives finest detail/smooth curves but slower and
  more clog-prone. **SECONDARY / non-official — attribute as such, don't assert
  the 30–40 % bare (K4/D3: it wants a citation or a `CAL-*` bet).**

**Decision heuristic (synthesized, attribute each half):** pick **0.2** only
when the min feature ≲ 0.4 mm or fine surface text matters (worth the time
penalty); **0.4** as default balance; **0.6** when the part is functional/large
and detail is non-critical (biggest throughput win per the sources); **0.8** for
draft/large-layer prototyping and max-flow infill. Min printable wall ≈ nozzle
diameter (single-wall) — a 0.8 nozzle cannot do a 0.5 mm wall. Layer time and
part inter-layer strength both scale with flow (larger nozzle → faster + often
stronger Z bonding). [Strength claim is from the search index/secondary sources,
not an official Bambu page — mark unconfirmed / attribute.]

---

### Source-quality flags (for the doc author)
- **Topic 1 signing** and **Topic 2 H2D AMS churn**: strongest, most
  load-bearing, but X2D-specific behavior is inferred from H2D — mark unconfirmed.
- **Topic 5 brim-vs-raft**: thin (no authoritative Bambu page) — attribute to a
  named community source or a `CAL-*` bet, don't assert bare (K4/D3).
- **Topic 4 transform-flag prose**: OrcaSlicer wiki lists `--arrange/--orient`
  but did not render per-flag descriptions in the fetch — verify against
  `orca-slicer --help` before pinning exact semantics.
- Everything else (OpenBambuAPI payloads, Tweaker CLI, Moonraker enum, Simplify3D
  catalog, Bambu fill/support wiki) is directly quoted from primary/official pages.
