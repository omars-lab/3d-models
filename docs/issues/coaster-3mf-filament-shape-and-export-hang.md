# The coaster→AMS 3MF: the `BambuStudio-<version>` Application tag SIGSEGVs the headless slicer, and `--export-3mf` hangs it

*Pivot for #37 part 4b-ii. Written 2026-09-18 against BambuStudio 02.08.02.61 on macOS 25.6
(Darwin 25.6.0), headless (no display attached), X2D 0.4-nozzle stock presets. Every command and
its output below was run live; raw per-run logs are under the session scratchpad `proof/`.*

> **Correction (2026-09-18):** an earlier draft of this doc named `filament_id`-as-an-array as the
> crash cause. That was **wrong** and is retracted — see §2. The array is a *logged, recovered*
> parse error, not the segfault. The segfault was isolated by bisection to a single element: the
> `Application` tag in the form `BambuStudio-<version>` (§1). Both findings are kept below because
> both changed the code, but only §1 is the crash.

## What surfaced it

Part 4b-ii assembles a multi-part 3MF from the bikar `--format parts` region bodies and bakes the
palette→slot colours into it, so the X2D prints each coaster region in a different AMS filament. The
first assembled 3MF **crashed the slicer on load** (SIGSEGV, exit -11), and the multi-region
positive controls **hung for 150 s**. Neither cause was the one first assumed. This records what the
evidence actually showed, isolated to a single element in each case.

## 1. The load crash: `Application=BambuStudio-<version>` drives the headless CLI into the GL project path

The crash was bisected on the *known-good* structure (one object, three coincident part-components,
`model_settings.config` extruders 1/2/3, `project_settings.config` with three colours — this slices
`exit 0`). Adding the original crashing file's root-model header elements **one at a time**:

| fixture      | change vs the working baseline                         | result            |
|--------------|-------------------------------------------------------|-------------------|
| `t2_ex123`   | baseline — no `Application` tag                        | **exit 0**        |
| `vB_compuuid`| + `p:UUID` on each `<component>`                       | exit 0            |
| `vA2_ns`     | + `xmlns:BambuStudio` on `<model>`                     | exit 0            |
| `vA3_ver`    | + `<metadata name="BambuStudio:3mfVersion">1`         | exit 0            |
| `vA4_bare`   | + `<metadata name="Application">BambuStudio`           | exit 0            |
| `vA5_orca`   | + `<metadata name="Application">OrcaSlicer-2.1.1`      | exit 0            |
| `vA6_generic`| + `<metadata name="Application">MyTool-1.0`            | exit 0            |
| `vA1_app`    | + `<metadata name="Application">BambuStudio-02.08.02.61`| **exit -11 SIGSEGV** |
| `vA_appmeta` | + all three (ns + version + `BambuStudio-<version>`)   | **exit -11 SIGSEGV** |

Only the **dashed, versioned** form `BambuStudio-<version>` crashes. Bare `BambuStudio`, another
slicer's name, and an arbitrary name all slice fine; so do the namespace and the `3mfVersion` tag on
their own. The command for every row (only the input `.3mf` changed):

```
$ BambuStudio --debug 2 \
    --load-settings "<X2D machine>.json;0.20mm Standard @BBL X2D.json" \
    --slice 0 <fixture>.3mf --outputdir proof/<fixture>
```

The `--debug 2` log of the crashing run stops at the version-recognition line and never reaches
geometry load — the process dies in the project-restore path, not in slicing:

```
[trace]   Initializing StaticPrintConfigs
[warning] cli mode, Current BambuStudio Version 02.08.02.61
<SIGSEGV — exit -11, 0.3 s, no result.json, no gcode, no thumbnail>
```

**Mechanism.** BambuStudio parses its own version out of `Application=BambuStudio-<version>`,
concludes the file is a *native, self-authored project*, and enters the full project-restore /
preview path — which wants a GL/preview context a no-display headless run does not have, and
dereferences past it. A file that merely *mentions* BambuStudio (bare, or in the namespace/version
metadata) is treated as an imported model and loads fine.

*Transfer condition (why this is a headless artifact, not a slicer bug):* the crash is on the
project/preview restore step that needs GL. It should **not** be assumed to reproduce with a display
attached — the GUI has a GL context and loads the same file. That is exactly why the shipped artifact
keeps the tag (§4) and the *colour* check is a GUI load, while the headless *geometry* check runs on
a tag-stripped copy.

## 2. Retracted lead: `filament_id` as an array is a recovered error, not the crash

The first assembled 3MF also carried the per-slot palette under the scalar key `filament_id` as an
array. That **does** produce an error in the `--debug 2` log:

```
[error] load_from_json: parse .../_temp_3.config got a generic exception,
        reason = [json.exception.type_error.302] type must be string, but is array
[error] Error load config from json: ... type must be string, but is array
```

But this error is **caught and recovered** — BambuStudio logs it and continues. Fixing it to a
scalar did **not** stop the SIGSEGV (the same file with `filament_id` scalar still crashed via the §1
Application tag). It is still worth fixing for correctness — `filament_id` is a single filament-product
identifier; the per-slot arrays are `filament_ids`, `filament_settings_id`, `filament_colour`,
`filament_type` — but it is **not** the crash.

Web corroboration (search, 2026-09-18; sources at the end): OrcaSlicer PR #15513 ("redesign
filament_id") and BambuStudio PR #12079 treat `filament_id` as one identifier for device matching,
never per-extruder, while published preset JSON shows the plural keys as arrays. *Qualifier:* the
exact `coString` vs `coStrings` declaration line was not retrievable from the truncated upstream
source, so scalar-vs-array is established by convergent evidence (two PRs + preset JSON + our own
recovered parse error), not read off a single schema line.

## 3. `--export-3mf` hangs headless (independent of filament)

The positive controls hung at 150 s — which first looked like a filament-loading crash:

```
# A: 3 region STLs, stock PLA ×3, --load-filament-ids 1,2,3, WITH --export-3mf  → TIMEOUT (150 s)
#    but wrote a complete plate_1.gcode (5.9 MB) first
# B: one custom filament JSON (round-trip copy of the stock preset), WITH --export-3mf → TIMEOUT (150 s)
#    but wrote a complete plate_1.gcode (2.1 MB) first
# D: single STL, stock filament, NO --export-3mf → exit 0 in 0.4 s, wrote result.json + gcode
```

Both A and B **finished slicing** (complete gcode) and only failed to terminate; dropping
`--export-3mf` (D) exits cleanly. **So the hang is the 3MF export/thumbnail step on this headless
build, not the filament file** — same GL/preview family as §1. My earlier "a user-modified copy of a
stock preset crashes the loader" hypothesis is **withdrawn**: the custom-filament slice (B) produced
a full gcode exactly as the stock slice did.

## 4. `result.json` does NOT reflect the embedded colour map under `--load-settings`

The working fixtures carry three colours in `project_settings.config` and extruders 1/2/3 in
`model_settings.config`, yet every one of them reports a **single** filament slot:

```
$ # part3full / t2_ex123 / vA4_bare, each sliced with --load-settings "<X2D machine>;<0.20 process>"
result.json → return_code 0, filaments: [ {filament_id:"unknown", id:1, ...} ]   # ONE slot, not three
             project_settings.config in the file:  filament_colour=[#333333,#d4af37,#b87333]
             model_settings.config in the file:     extruder=1 / 2 / 3 per part
```

`--load-settings machine;process` loads a **single-filament** process and **overrides** the 3MF's
embedded filament arrays; the extruder=2/3 parts clamp to slot 1. `main_used_g` is `0.0` even in the
single-STL D run, so the gram field is not a signal in this fast path either. **Consequence: a
headless slice with `--load-settings` cannot verify the per-region colour assignment** — the honest
headless signals are exit code, the `objects[]`/parts structure, and geometry only. Colour
assignment has to be verified by a **GUI load** (the GUI reads the embedded `model_settings` /
`project_settings`), or by a headless slice that loads the 3MF's own filament config instead of
overriding it with a single-filament process (open follow-up).

`--load-filament-ids` does not close this either: re-running control A honestly (no `--export-3mf`)
loaded all three region STLs as distinct `objects[]` but still reported **one** filament slot. The
per-object→slot assignment the *file* carries lives in `model_settings.config` as a 1-based
`extruder` per object/part (per-triangle overrides as `paint_color` on `<triangle>`), independent of
any CLI flag.

## What this changes in the code

1. **`threemf-assemble.ts` keeps the `Application=BambuStudio-<version>` tag** in the shipped 3MF —
   it is the #9666 colour contract for the GUI/print artifact, and the GUI (with GL) loads it fine.
   The crash is a *headless* artifact, so the **headless geometry check slices a tag-stripped copy**
   and the **colour check is a GUI load + screenshot**, not a headless slice.
2. **`filament_id` is emitted as a scalar** (one product id); the per-slot palette goes under
   `filament_ids` (+ `filament_settings_id`, `filament_colour`, `filament_type`). Correctness fix
   from §2, not the crash fix. The assembler test asserting the plural key is updated to match.
3. **Per-region assignment is baked into `model_settings.config`** as an `extruder` index per part,
   not delegated to `--load-filament-ids`, which §4 shows does not surface as slots.
4. **Verification path (§4):** headless slice (no `--export-3mf`, tag stripped) verifies exit 0 +
   `objects[]`/parts; a GUI load verifies the per-region colours. `result.json` filament-slot count
   is explicitly *not* used as the colour signal.

## Sources (web, 2026-09-18)

- BambuStudio `--load-filament-ids` in source: github.com/bambulab/BambuStudio `src/BambuStudio.cpp`
  (registered `ConfigOptionInts "load_filament_ids"`, length must equal input-file count). Not in the
  official Command-Line-Usage wiki.
- `filament_id` scalar vs plural arrays: BambuStudio PR #12079; OrcaSlicer PR #15513; preset JSON in
  dgauche/BambuStudioFilamentLibrary; KuzuriAo/b2o #1 (per-extruder arrays sized to extruder count; a
  wrong-length one segfaults silently).
- CLI segfaults (context, not our exact cause): BambuStudio issues #10408, #9119, #8569, #7525, #12012.
- 3MF `model_settings.config` `extruder` per object + per-triangle `paint_color`: printago.io
  3mf-file-format writeup (third-party; no official wiki wording found).
- The `Application=BambuStudio-<version>` native-project recognition (§1 mechanism) is **our own
  bisected finding** (table above), not sourced from upstream docs.
