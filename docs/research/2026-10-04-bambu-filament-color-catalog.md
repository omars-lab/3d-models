---
date: 2026-10-04
produced-by: Claude (Opus 5.5), reading the filament color list that ships inside Bambu Studio 02.08.02.61 on this machine, whole, with Python's json module (`catalog.py build`), then fetching the same file from Bambu's public GitHub repo once (`catalog.py refresh`). No web search.
feeds:
  - '[[bambu-color-catalog]]'
  - '[[gbv-themes]]'
---

# Every Bambu filament color: where the catalog comes from

The `color-themes` skill now reads its colors from a catalog of every color Bambu Studio knows,
not only the 55 plain PLA Basic and Matte colors copied by hand into
[the first hex file](2026-10-04-bambu-pla-color-hexes.md). That file stays as it was; this one
records the wider read. The catalog is
`docs/design/coaster/themes/catalog/catalog.yaml`, written by
`.claude/skills/color-themes/scripts/catalog.py build`, and drawn as swatch sheets on
[the catalog page](../design/coaster/themes/bambu-color-catalog.md).

## The source

- **File:** `/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/filament/filaments_color_codes.json`
- **App version:** Bambu Studio 02.08.02.61, read from the app's `Info.plist`
- **sha256:** `b600b1da4b275d93f06cfdd5cc715b5459691a47fade432998355cd908217a1d` (the same file
  the first hex file read)
- **Size:** 314 colors in **46** filament lines (`fila_type`). The first hex file says "40
  filament types"; counting the distinct `fila_type` values in the same file gives 46. That
  file is kept word for word, so the difference is noted here instead.
- **Fetched:** yes, read whole. Nothing here comes from a search snippet.

Each color carries its product code (`fila_color_code`, the number on the spool's label), a
short slot code (`color_code`), its line (`fila_type`, such as `PLA Silk+`), names in twelve
languages (the catalog keeps the English one), a kind (`fila_color_type`: 单色 one color, 渐变色
gradient, 多拼色 multi-color), and one or more hexes with an alpha byte (`#RRGGBBAA`).

## The same file on GitHub, for `catalog.py refresh`

- **Path checked:** `bambulab/BambuStudio`, default branch `master`,
  `resources/profiles/BBL/filament/filaments_color_codes.json`. It exists (`gh api` returned the
  file, 231,442 bytes). `refresh` fetches it from
  `https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/filaments_color_codes.json`.
- **What it found on 2026-10-04:** 318 colors (sha256 `5af6c01befa0…`), so 4 added since the
  app's copy, none removed, none changed. All four are PETG Basic: 30404 Sunflower Yellow
  `#FFB81C`, 30504 Bright Green `#97D700`, 30701 Purple `#8A75D1`, 30702 Hot Pink `#F277C6`.
- `refresh` only reports. It writes nothing; the catalog is rebuilt from the installed app with
  `build`, so the catalog always matches a slicer someone can print with.

## Colors by line

| Line | Colors | | Line | Colors |
|---|---|---|---|---|
| PLA Basic | 38 | | PLA-CF | 7 |
| PLA Matte | 25 | | TPU for AMS | 7 |
| PLA Silk | 18 | | ASA | 6 |
| ABS | 16 | | PETG-CF | 6 |
| PETG HF | 14 | | PLA Sparkle | 6 |
| PETG Basic | 13 | | PLA Wood | 6 |
| PLA Lite | 13 | | TPU 95A HF | 6 |
| PLA Silk+ | 13 | | PLA Glow | 5 |
| PLA Tough | 10 | | PLA Metal | 5 |
| PLA Translucent | 10 | | PLA Pure | 5 |
| PETG Translucent | 9 | | TPU 85A | 5 |
| ABS-GF | 8 | | PLA Galaxy | 4 |
| PA6-GF | 8 | | PC | 4 |
| PETG Matte | 8 | | PLA Aero | 3 |
| TPU 90A | 8 | | PC FR | 3 |
| PLA Tough+ | 7 | | PLA Marble | 2 |
| Support for PLA/PETG | 2 | | TPU 95A | 2 |

One color each: PLA Dynamic, ASA Aero, ASA-CF, PAHT-CF, PA6-CF, PPA-CF, Support for PA/PET, PVA,
Support for ABS, PET-CF, PPS-CF, Support for PLA. Together: 314.

## Which lines a coaster may use

The catalog's `coaster_lines` list is every PLA line (Basic, Matte, Silk, Silk+, Sparkle,
Galaxy, Marble, Metal, Translucent, Glow, Wood, Lite, Pure, Tough, Tough+, Aero, PLA-CF,
Dynamic) and the four PETG lines (Basic, Matte, HF, Translucent): 22 lines. This is a choice,
not a fact from the file. PLA is what sheets-04g was sliced for, and PETG prints on the same
textured plate with a different profile. ABS, ASA, PC, nylon and TPU need other settings or an
enclosure, and support filaments are not for show, so the buy list may not use them.

## The finish label is read from the line's name

The file has no finish field. `catalog.py` takes the word in the line's name: Silk+ (checked
before Silk), Silk, Matte, Sparkle, Galaxy, Marble, Metal, Translucent, Glow, Wood, Aero,
Tough, Lite, Pure; Dynamic as "uv color change"; `-CF` and `-GF` as carbon and glass fiber;
anything else "plain". So "PLA Basic" is plain and "PETG HF" is plain. The label says what the
product is called, not how it looks on the bed.

## What a hex is, and what it is not

The cautions in [the first hex file](2026-10-04-bambu-pla-color-hexes.md#what-the-hex-is-and-what-it-is-not)
carry over, and the wider catalog adds three:

- **A multi-hex spool is not a pattern.** A gradient or multi-color spool lists two to four
  hexes, but the file does not say how long each color runs along the filament. Which piece
  gets which color depends on where the spool is when that piece prints, so it cannot be
  predicted. The theme pictures draw such a spool as its hexes in stripes and print a warning.
- **The alpha byte is the slicer's tint.** Translucent colors carry alpha `80` (half
  transparent). It is how Bambu Studio shows the color, not a measured light transmission.
- **Sheen and flecks are not in the hex.** The pictures draw silk with a light band and sparkle
  with dots so the finish is visible at all; neither is a measurement of a printed part.

## Not checked

- Whether every color is on sale today, and at what price. The file is what this version of the
  slicer knows; Bambu's store was not opened.
- Whether the X2D's PLA profile prints Silk, Sparkle or PETG colors well with sheets-04g's
  settings. Each line has its own filament profile in the slicer; nothing here was printed.
- Whether the four PETG Basic colors on GitHub are in a released app yet. They are on the
  repo's `master` branch; the installed 02.08.02.61 does not have them.
