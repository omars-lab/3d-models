<!--
provenance:
  date: 2026-09-18
  produced-by: research subagent (Claude Opus 4.8), 3d-models session
  feeds: docs/coaster-colour-design.md §6 (part 4) — the headless-CLI 3MF/AMS contract
  method: web research of the Bambu Studio CLI wiki, the Bambu Lab 3MF colour-parsing and
          multi-colour wiki pages, and corroborating third-party writeups; records the settled
          answer to the §6 open question ("does headless BambuStudio need per-object filament
          baked into the 3MF, or does --load-filaments suffice"). Findings preserved verbatim.
-->

# Research — coaster AMS / 3MF headless-CLI contract

This file settles the one open, load-bearing question that
[`coaster-colour-research.md`](coaster-colour-research.md) §6 left as an "(unverified
snippet)": whether the **headless** Bambu Studio / Orca CLI can assign objects (or painted
regions) to filament slots at slice time, or whether that mapping must already be **baked
into the input 3MF**. The findings below are recorded verbatim as the settled answer.

## Settled answer

**SETTLED: per-object filament→slot assignment MUST be baked into the input 3MF; the CLI
cannot assign objects/regions to slots at slice time.**

- BambuStudio/Orca headless slicing has no CLI flag that maps objects or painted regions to
  filament slots; the mapping lives in the 3MF: Metadata/model_settings.config per-object/part
  `extruder` attributes, and per-triangle `paint_color` bitmasks in 3D/Objects/*.model.
- `--load-filaments` loads filament PROFILES/materials into existing logical slots by list
  order; its count "should not exceed the filaments used in the 3mf" — it fills slots the 3MF
  already declares, it does not create/reassign them.
- Settings precedence (CLI wiki): command-line > --load-settings/--load-filaments > values
  embedded in the 3MF.
- The slicer only honours per-object/painted assignment when the 3MF Application metadata
  starts with `BambuStudio-` (else paint_color/extruder are ignored and it imports
  single-colour — GitHub issue #9666).
- project_settings.config needs parallel arrays filament_type, filament_colour, and non-empty
  filament_id per slot; empty filament_id silently routes to the external spool.
- Emit recipe: root/model Application metadata `BambuStudio-<ver>`; per whole-object
  `<object id="N"><metadata key="extruder" value="K"/></object>` (K = 1-based slot); per
  sub-part `<part ...><metadata key="extruder" value="K"/></part>`; per painted region
  `<triangle ... paint_color="<bitmask>"/>` (slot codes 1→"4", 2→"8", 3→"0C"); slice with
  `bambu_studio --load-filaments "s1.json;s2.json" --load-settings machine.json;process.json --slice 0 --export-3mf out.3mf`.
- Caveat: logical slot ≠ physical AMS slot (physical mapping is resolved interactively / at
  print time by colour match; the CLI slice carries only logical filament index order).
  --load-filaments silently under-fills/errors if count exceeds slots used.

## Sources

1. https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage
2. https://wiki.bambulab.com/en/bambu-studio/Standard-3MF-File-Color-Parsing
3. https://wiki.bambulab.com/en/software/bambu-studio/multi-color-printing

Corroboration: https://printago.io/blog/3mf-file-format ,
https://deepwiki.com/bambulab/BambuStudio/6.3-multi-material-printing , GitHub BambuStudio#9666.
