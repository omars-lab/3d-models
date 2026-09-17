# The X2D "Filament Grouping" mode *is* headlessly settable — and a no-op for our single-material prints

*Issue slug: `x2d-filament-grouping-mode`. Written 2026-09-17, during #53. Ties to
[D-053](../decisions-log.md) (dual nozzle lives in the slicer, not the schema).*

## What surfaced it

Omar's Bambu Studio screenshot showed an X2D dual-nozzle **Filament Grouping** selector
(Filament-Saving / Convenience-Sync / Quality / Custom) that our pipeline ignored: `print-model`
never reasons which mode to pick, and `bambu slice` had no way to set it. Left alone, an operator who
opens a plate in Studio meets a control the whole tool is silent about.

## What the CLI actually exposes (measured, not assumed)

`BambuStudio --help` has **no** filament-grouping flag (57 flags surveyed; the nearest are
`--load-filament-ids`, `--load-filaments`, `--load-settings`, `--estimate-mode`). So the mode is **not**
a top-level CLI flag — it is a **process/project config key**, `filament_map_mode`, a
`ConfigOptionEnum<FilamentMapMode>` (confirmed in the binary's symbol table). The GUI selector maps to
three enum literals:

| GUI label | enum literal | meaning (from the binary's own help strings) |
|---|---|---|
| **Filament-Saving** (default) | `Auto For Flush` | *"generates filament grouping … based on the most filament-saving principles to minimise waste"* |
| **Quality** | `Auto For Match` | *"… based on the quality of prints, prioritising print quality over filament saving"* |
| **Custom** | `Manual` | a hand-assigned per-filament `filament_map` array |

(The "Convenience" label the screenshot showed is a legacy alias — the binary carries
`"Those are old settings provided for convenience."`)

## How it is set headlessly (verified live, BambuStudio 02.08.02.61, X2D presets, 2026-09-17)

- **Merge the key into the *process* config JSON.** Passing it as a second `--load-settings` process
  file fails: `duplicate process config file … run found error, exit`. Adding `filament_map_mode` to the
  one process preset JSON and slicing → **exit 0**, and the value lands in the sliced 3mf's
  `Metadata/project_settings.config` and `Metadata/model_settings.config`. So it is genuinely honoured,
  not silently dropped.
- **The default is already `Auto For Flush`.** A plain slice (no override) writes
  `filament_map_mode = "Auto For Flush"` — i.e. Studio's default *is* Filament-Saving. Nothing needs
  setting to get the default behaviour.
- **Studio does *not* validate the enum string.** A bogus value (`filament_map_mode = "Bogus"`) slices
  at **exit 0** and silently falls back to the default. So a typo would print under the *wrong* grouping
  with no error — which is why the CLI owns a closed token→literal mapping and rejects anything else,
  rather than forwarding a raw string.

## The load-bearing fact: it is a **no-op for a single filament**

With one filament loaded, the sliced 3mf reports `filament_maps = 1` — everything collapses to one
group regardless of mode. Grouping only *does* anything with **≥2 filaments** on the plate. **Every
plate in the current campaign (Plate 1 machine card, and the near-term LEGO/orb plates) is
single-material**, so for our actual prints the grouping mode is irrelevant and the Filament-Saving
default is correct. The honest behaviour is to *say that*, not to expose a knob that appears to matter
and doesn't.

## What shipped

- **`bambu slice plate --filament-map-mode <saving|quality|manual>`** (`tools/bambu/src/commands/slice.ts`):
  - `saving`→`Auto For Flush`, `quality`→`Auto For Match`; unknown tokens are rejected (Studio would
    silently default them); `manual` is recognised but refused with guidance (it needs an explicit
    `filament_map` array this command does not synthesise).
  - **Single (or zero) filament → no-op with a stated note** — the settings are left untouched and the
    operator is told grouping needs ≥2 filaments and the default is Filament-Saving.
  - **≥2 filaments → merge** the enum into the resolved process preset (written to a temp copy, swapped
    into `--load-settings`), logged so `--dry-run` shows the real merged command.
  - Pure logic (`filamentMapModeEnum`, `filamentCount`, `injectFilamentMapMode`) is unit-tested
    (`slice.test.ts`): the mapping, case-insensitivity, unknown/`manual` rejection, the ≥2 threshold, and
    the merge that touches only the process config and preserves its other keys.
- **`print-model` requirements step** (`.claude/skills/print-model/rubric.md` §Filament grouping):
  single-material → grouping is a no-op, say the Filament-Saving default is correct and move on;
  multi-material/multi-colour → reason Filament-Saving (minimise waste/flush) vs Quality (fewer
  cross-nozzle swaps, better surface) vs Custom, and recommend — never silently pick. This also
  upgrades the §Arrangement `[X2D-UNCONFIRMED]` dual-nozzle caveat: the *grouping* mechanism is now
  verified; only auto-arrange bed-zoning remains unconfirmed.

## Not done on purpose

`manual` (Custom) grouping is not synthesised — a correct per-filament `filament_map` array is a real
design decision per plate, and inventing one would be exactly the "capability nothing verifies" trap.
And the **grouping *behaviour*** (which nozzle each colour lands on, flush savings) is only verified as
*accepted and recorded*; its print-quality effect can't be measured until a real multi-material plate
exists — noted here so a future session does not re-derive the mechanism.
