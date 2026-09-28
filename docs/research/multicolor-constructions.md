<!--
provenance:
  date: 2026-09-26
  produced-by: multicolour agent (Claude Opus 5.5)
  feeds: docs/multicolor-constructions-design.md (filled, coloured shapes on construction coasters)
  method: (1) in-repo reads and measurements at the bikar worktree
          ~/Workspace/git/bikar-multicolor (branch feat/multicolor-fills off bikar origin/main
          6356bb3) and this repo at origin/master 994d788; (2) a survey script run against the
          built bikar core over every plain `<id>-coaster.bkr` in bikar patterns/Constructions;
          (3) web search and fetch on 2026-09-26. Every web source below says whether the page
          itself was fetched or only a search-result summary was seen. Line numbers are as they
          read that day and are not re-pinned (research/ exemption).
-->

# Research — filled, coloured shapes on construction coasters

Omar, 2026-09-26: an alternative version of the constructions where some of the shapes the
lines enclose are filled and coloured, so a coaster prints in several colours on the X2D with
the AMS. Added the same day: **"shapes that are translations same midpoint from center should
be same color"**.

## 1. What already exists (in-repo reads)

- **Colour per face in the 2D pattern.** `fill void where <selector> color <Name>` with a
  `palette` block. Selectors include `ring`, `sides`, `area`, `shape`, `index`, `parity`,
  `neighbors`, combined with `and` (bikar `packages/core/src/theme/fill-resolver.ts`).
- **`ring` is 1D clustering of centroid distance.** `computeRingBins` in `fill-resolver.ts` sorts
  faces by the distance of their centroid from a centre and starts a new ring when the gap
  exceeds `TOLERANCE = 1e-2`, anchored on the first member of each ring. `bikar bands <file>`
  lists the rings (bikar `packages/cli/src/index.ts`, the `bands` verb near line 3517).
- **The ring centre is not the symmetry centre in general.** `findCenter(env)` in bikar
  `packages/core/src/dsl/evaluator.ts` (line 10060) returns the first circle's centre. In the
  construction files that is `(0,0)`, which is often not the rosette's centre.
- **The ring colour reaches the print** (D-078, [radial-band-colour-design.md](../radial-band-colour-design.md)).
  `--format parts` (D-073) writes one watertight STL per piece — `base`, `straps`, `border`,
  and one per palette colour name — plus a `<Coaster>.parts.json` sidecar. A ring colour
  overrides the face's region. Each piece is gated on its own under `--check`.
- **`--format parts` refuses** deboss, `outline pattern`, and the slab-reshaping clauses
  (interlock, key, tab, rim, trivet, openwork, edges). So the minimal, minimal-frame, pegs, key,
  tab, interlock and twist styles cannot be split today; plain and border can
  ([coaster-colour-design.md](../coaster-colour-design.md)).
- **Colour to slot** (D-075): palette name → logical AMS slot by first-seen order, slot 1 is the
  plate default, a shared name shares one slot. `bambu slice coaster` (D-077) writes a
  multi-part 3MF with per-part extruder metadata; headless slicing checks geometry only, colour
  is checked in the Bambu Studio window ([coaster-ams-3mf-contract.md](coaster-ams-3mf-contract.md)).
- **The plate picture is drawn from the 2D drawing**, not from the split bodies
  (`tools/bambu/src/colour-preview.ts`). It can show a colour the bodies do not have.
- **Relief targets:** `relief straps|faces|both emboss <mm>`. Under `both` every enclosed face is
  raised; a raised face with no fill colour falls into the `straps` piece.
- **The coaster is one height field** over a grid of pitch
  `COASTER_GRID_PITCH_MM = PERIMETER_WIDTH_MM` (0.4 mm, bet CAL-FEA-01). Pieces are cut from that one field, so two
  neighbouring pieces share their faces exactly: no overlap and no gap, and no boolean union is
  needed. The price is a staircase edge at the grid pitch.

## 2. Survey — do the engine's rings match Omar's colour classes?

**Method.** For each plain construction coaster, compile it with the built core, take every
bounded face, and give it a class key: vertex count + sorted edge lengths + centroid distance
from the centre, each rounded to 0.01 mm. The centre is the area-weighted centroid of all faces
(the bbox centre was tried first and is wrong for odd-fold symmetry). Sorted edge lengths do not
change under rotation or mirroring, so **a mirrored copy lands in the same class**. Then compare
the classes with the engine's `ring` numbers. Script: a scratch file, not checked in (a one-off
measurement; the proposal in the design doc is to build this into the engine instead).

| Construction | Faces | Classes | Rings | Classes split across rings |
|---|---|---|---|---|
| 7apC5Q9QS-8 | 101 | 16 | 16 | 0 |
| GimTvN9hw4U | 55 | 8 | 14 | 7 |
| lEfWSogWscs | 33 | 5 | 19 | 4 |
| n3IidKfXE1I | 58 | 58 | 35 | 0 |
| nmEjCTzMbDg | 540 | 21 | 273 | 21 |
| rDuxHF3xMOc | 116 | 17 | 107 | 17 |
| sDO9fpu76v8 | 337 | 35 | 168 | 34 |
| tA8eSdVx_EQ | 22 | 4 | 13 | 3 |

What it shows:

- Only on 7apC5Q9QS-8 are the rings exactly the classes, because its first circle sits on the
  rosette centre. On six of the other seven surveyed files, most classes are split over several
  rings, so colouring by `ring` would give matching shapes different colours — the opposite of
  Omar's rule.
- n3IidKfXE1I gives one class per face (58 of 58). It seems not to be rotation-symmetric about
  one centre; it was not inspected further, so this is a reading of the numbers, not a finding.
- **Close radii exist.** On 7apC5Q9QS-8, ring 9 sits at r = 40.48 mm and ring 10 at r = 40.70 mm,
  0.22 mm apart, and they are different classes. So a radius tolerance wider than about 0.2 mm
  would merge two real classes on this file. This is the hard case for the validator.
- The survey rounds to 0.01 mm; a tolerance sweep was not run, so how stable the class counts
  are to the rounding is not measured.

## 3. Kernel findings from the prototype (measured)

Prototype: `patterns/Constructions/7apC5Q9QS-8-fill-coaster.bkr` in the bikar worktree —
the 7apC5Q9QS-8 construction, `relief both emboss 1.2`, ring 0 and ring 3 in Ruby, every other
face in Slab (the base colour), straps in Gold.

1. **Before any fix, filling ate the straps.** A face polygon's edge *is* a strap centreline, and
   the cell colour lookup asks "which face is this cell centre in", so the inner half of each
   strap went to the face on each side. With every face filled, the straps body kept only the
   outermost line. Fix: under `relief both`, a cell within half a strap width of a strap stays
   the strap's (`faceColorAt` in bikar `packages/core/src/kernel3d/coaster.ts`). On the test
   rosette the inner edge of the straps top moved from 6.46 mm to 3.42 mm from the centre.
2. **After that fix, two bodies were not watertight.** Star tips thinner than a grid cell (once
   the strap's half-width is taken off) made diagonal-only touches between two raised pieces:
   Ruby euler 26 and straps euler −208, both failing. The existing saddle repair only fills
   cells at base level, and here every cell of the 2×2 block is raised. Fix: hand the colour
   cells of such a bowtie back to the strap (`resolveRaisedSaddles`). It only moves cells from
   a colour piece to its region piece, so it ends, and it runs only when a colour is present.
3. **After both fixes**, `render --format parts --check` passes every body: base euler 2,
   Slab euler 184, Ruby euler 18 (9 separate stars: the centre and a ring of 8), straps
   euler −200, all watertight at the 0.8 mm floor, at the file's default `size` of 90 mm.
   `--format stl --check` on the whole coaster passes too (one body, 41.7 cm³). Re-run at
   `--param size=80`: the same four bodies pass with the same euler numbers.
4. **Unfilled faces rise in the strap colour under `relief both`.** To keep them the slab colour
   they must be filled with the base palette name (the prototype does
   `ring != 0 and ring != 3 color Slab`). "Only the filled faces rise" would need a new relief target.
5. **The plate picture lied before fix 1**: the 2D drawing showed gold straps that the bodies
   did not have. A top-down picture of the actual bodies (a z-buffer of the STLs in their
   sidecar colours) showed the loss. The design doc proposes that check as a tool.

## 4. Web sources (2026-09-26)

| # | Source | Status | What it supports |
|---|---|---|---|
| W1 | [Bambu Lab AMS product page](https://us.store.bambulab.com/products/ams-multicolor-printing) | search summary only | "Each Bambu Lab AMS is composed of 4 filament slots, and up to 4 AMS can be installed in parallel and supports up to 16 colors". |
| W2 | [Bambu Lab X2D FAQ](https://bambulab.com/en-us/x2d/faq) | fetch refused (HTTP 403); search summary only | X2D "supports up to 4 AMS 2 Pro and 8 AMS HT units … and with dual hotends, enables up to 25-color printing". Not confirmed on the page. |
| W3 | [Bambu wiki — Multi-Color Printing](https://wiki.bambulab.com/en/software/bambu-studio/multi-color-printing) | fetch refused (HTTP 402); title seen in search only | Nothing cited from it. |
| W4 | [Prusa Knowledge Base — Wipe tower](https://help.prusa3d.com/article/wipe-tower_125010) | **fetched** | The tower gives "sharp color transitions"; "wipe to infill can greatly reduce the amount of wasted material"; wipe-into-object mixes colours. PrusaSlicer, not Bambu Studio. |
| W5 | [Bambu forum — "So much purge"](https://forum.bambulab.com/t/so-much-purge-tower-infill-support-poop-why-does-it-do-them-all/14369) | **fetched** | Each change purges to the chute and then prints on the prime tower; users report a tower volume default of 45 mm³ that can be lowered; no Bambu staff answer in the thread. X1C, not X2D. |
| W6 | [Printago — Bambu Studio prime line guide](https://printago.io/guides/bambu-studio-prime-line) | **fetched** | "The prime tower only appears on multi-color or multi-material prints"; removing it without flushing into the object or infill gives "color bleed where the old color contaminates the new one". |
| W7 | [Sovol — Reduce filament waste in multi-colour printing](https://www.sovol3d.com/blogs/news/reduce-filament-waste-multi-color-3d-printing-9-practical-moves) | **fetched** | "The fastest way to reduce waste is to reduce colour changes"; a height-based colour swap as the alternative; flushing too low gives "faint tinting on light filaments or 'dirty' edges on small features"; dark → light purges more. No numbers. |
| W8 | [BambuHub — Multi-colour techniques](https://bambuhub.net/guides/multi-color-techniques) | **fetched** | Height Range Modifier changes filament at a Z height; separate STLs can take different filaments; use one material type for all colours. Nothing on feature size or bleed. |
| W9 | [Kingroon — Multicolour printing tricks](https://kingroon.com/blogs/3d-print-101/multicolor-printing-tricks) | **fetched** | Flushing multiplier default 1, "you can try 0.9 or 0.85". Nothing on flat prints, first layer or feature size. |
| W10 | Nozzle-size guides ([Flashforge](https://www.flashforge.com/blogs/news/how-3d-printer-nozzle-size-affects-your-prints), [3dprintbook](https://3dprintbook.com/blog/tuning-fdm-printers-for-miniatures/)) | search summary only | Nozzle diameter sets the XY feature size; a 0.2 mm nozzle halves it. Not fetched, so not relied on for a number. |

**In-repo facts that stand in for what the web could not settle:**

- The live X2D reports its loaded trays through `bambu filament` (`print.ams.ams[].tray[]` plus an
  external spool in `print.vir_slot`); confirmed on the device 2026-09-17 (bring-up notes in this
  repo's memory, `bambu-x2d-bringup`). So the slot count is **read from the machine**, not
  assumed from W1/W2.
- The X2D slice profile reads `nozzle_diameter = 0.4,0.4` (dual nozzle), same source.
- No source fetched here gives a minimum size for a colour region or a bleed distance; nothing
  here settles them. The design doc uses existing bets (CAL-FEA-01, CAL-CST-01, CAL-PIN-01) and
  says where they may not transfer.

## 5. What was not verified

- No print. Nothing here has touched the printer; printing and filament choice are Omar's.
- The multi-part 3MF of the prototype was not sliced, and its colours were not checked in the
  Bambu Studio window.
- Colour bleed, first-layer behaviour and purge per change on the X2D are not measured; W5–W9
  are other printers or general guides, and none is an X2D measurement.
- Whether the dual nozzle on the X2D cuts purge for a two-colour print was not confirmed (W2
  was not fetched).
