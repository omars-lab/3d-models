---
date: 2026-10-04
produced-by: Claude (Opus 5.5), reading the filament color list that ships inside Bambu Studio 02.08.02.61 on this machine. One pass, no web search. The file is Bambu's own, so there was nothing to cross-check it against.
feeds:
  - '[[gbv-themes]]'
---

# Bambu PLA Basic and PLA Matte: the hex Bambu Studio uses for each color

This is where the `color-themes` skill gets the colors it is allowed to suggest buying
(`.claude/skills/color-themes/palette.yaml`). That skill's self-test checks that every hex on its
buy list matches a row in this file. So no buy color can carry a hex we made up.

## The source

- **File:** `/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/filament/filaments_color_codes.json`
- **App version:** Bambu Studio 02.08.02.61, read from the app's `Info.plist`
- **sha256:** `b600b1da4b275d93f06cfdd5cc715b5459691a47fade432998355cd908217a1d`
- **Size:** 314 entries in 40 filament types. Only the single-color PLA Basic (30) and PLA Matte (25)
  entries are copied below. Those are the plain filaments a coaster would use.
- **Fetched:** yes. The file was read whole with Python's `json` module on 2026-10-04. Nothing in
  the table below comes from a search snippet.

Each entry carries a product code (`fila_color_code`, the number on the spool's label), a short slot
code (`color_code`), names in twelve languages, and one hex color with an alpha byte (`#RRGGBBFF`).
The table drops the alpha byte, which is `FF` (fully opaque) on every row copied here.

## What the hex is, and what it is not

Bambu Studio uses this hex to tint the filament in the slicer and in the AMS view. It is the
maker's own label for the color, **not a measurement of a printed part**. Three cautions carry over
to every picture the skill draws:

- **The finish is not in the hex.** Matte and Basic print with different sheen, and a flat picture
  shows neither. Ivory White (Matte) and Jade White (Basic) share `#FFFFFF`, and so do Charcoal
  (Matte) and Black (Basic) with `#000000`, yet they will not look the same on the bed.
- **A screen is not a spool.** How close the hex looks to the plastic depends on the screen. This
  file gives no tolerance.
- **Two products can share a hex.** A hex alone does not tell you which spool is loaded (see the blue
  tray below).

## The loaded trays, against this list

The four trays the printer reported on 2026-10-04 (`bambu filament --json`, read in the session that
asked for this work):

| Tray hex | Matches here | So |
|---|---|---|
| `#F5547C` | PLA Basic **Hot Pink** (10204, R3) | same hex as Hot Pink |
| `#00AE42` | PLA Basic **Bambu Green** (10501, G6) | same hex as Bambu Green |
| `#000000` | PLA Basic **Black** (10101, K0), and PLA Matte **Charcoal** (11101, K1) | black; which product it is, the hex cannot say |
| `#0047BB` | no PLA Basic or PLA Matte row. In the whole file it appears only on PLA Translucent Blue (13611, as `#0047BB80`, half transparent) and as one of the two colors of PLA Silk "Midnight Blaze" and "Neon City" | the hex does not name the product; the tray is blue |

## PLA Basic (30 single colors)

| Code | Slot | Name | Hex |
|---|---|---|---|
| 10300 | A0 | Orange | `#FF6A13` |
| 10301 | A1 | Pumpkin Orange | `#FF9016` |
| 10602 | B1 | Blue Gray | `#5B6579` |
| 10604 | B3 | Cobalt Blue | `#0056B8` |
| 10605 | B5 | Turquoise | `#00B1B7` |
| 10603 | B8 | Cyan | `#0086D6` |
| 10601 | B9 | Blue | `#0A2989` |
| 10103 | D0 | Gray | `#8E9089` |
| 10102 | D1 | Silver | `#A6A9AA` |
| 10104 | D2 | Light Gray | `#D1D3D5` |
| 10105 | D3 | Dark Gray | `#545454` |
| 10502 | G2 | Mistletoe Green | `#3F8E43` |
| 10503 | G3 | Bright Green | `#BECF00` |
| 10501 | G6 | Bambu Green | `#00AE42` |
| 10101 | K0 | Black | `#000000` |
| 10800 | N0 | Brown | `#9D432C` |
| 10802 | N1 | Cocoa Brown | `#6F5034` |
| 10201 | P0 | Beige | `#F7E6DE` |
| 10203 | P1 | Pink | `#F55A74` |
| 10701 | P2 | Indigo Purple | `#482960` |
| 10700 | P5 | Purple | `#5E43B7` |
| 10202 | P6 | Magenta | `#EC008C` |
| 10200 | R0 | Red | `#C12E1F` |
| 10205 | R2 | Maroon Red | `#9D2235` |
| 10204 | R3 | Hot Pink | `#F5547C` |
| 10100 | W1 | Jade White | `#FFFFFF` |
| 10400 | Y0 | Yellow | `#F4EE2A` |
| 10402 | Y2 | Sunflower Yellow | `#FEC600` |
| 10801 | Y3 | Bronze | `#847D48` |
| 10401 | Y4 | Gold | `#E4BD68` |

The file lists 38 PLA Basic entries in all. The other 8 have more than one hex (gradients and
dual colors) and are left out here.

## PLA Matte (25 single colors)

| Code | Slot | Name | Hex |
|---|---|---|---|
| 11300 | A2 | Mandarin Orange | `#F99963` |
| 11603 | B0 | Sky Blue | `#56B7E6` |
| 11600 | B3 | Marine Blue | `#0078BF` |
| 11601 | B4 | Ice Blue | `#A3D8E1` |
| 11602 | B6 | Dark Blue | `#042F56` |
| 11104 | D0 | Nardo Gray | `#757575` |
| 11102 | D3 | Ash Gray | `#9B9EA0` |
| 11502 | G0 | Apple Green | `#C2E189` |
| 11500 | G1 | Grass Green | `#61C680` |
| 11501 | G7 | Dark Green | `#68724D` |
| 11101 | K1 | Charcoal | `#000000` |
| 11802 | N0 | Dark Chocolate | `#4D3324` |
| 11800 | N1 | Latte Brown | `#D3B7A7` |
| 11801 | N2 | Dark Brown | `#7D6556` |
| 11803 | N3 | Caramel | `#AE835B` |
| 11201 | P3 | Sakura Pink | `#E8AFCF` |
| 11700 | P4 | Lilac Purple | `#AE96D4` |
| 11200 | R1 | Scarlet Red | `#DE4343` |
| 11203 | R2 | Terracotta | `#B15533` |
| 11204 | R3 | Plum | `#950051` |
| 11202 | R4 | Dark Red | `#BB3D43` |
| 11100 | W2 | Ivory White | `#FFFFFF` |
| 11103 | W3 | Bone White | `#CBC6B8` |
| 11400 | Y2 | Lemon Yellow | `#F7D959` |
| 11401 | Y3 | Desert Tan | `#E8DBB7` |

## Not checked

- Whether every color here is on sale today, and at what price. The file is what this version of
  the slicer knows. The store is not checked, so a buy list is a list of colors that exist, not a
  basket.
- Whether this X2D's profile prints all of them with the same settings. They are all PLA, the type
  sheets-04g was sliced for. Whether one tray-profile fits every color is the slicer's call.
