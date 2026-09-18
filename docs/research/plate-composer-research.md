<!-- provenance: date=2026-09-18; produced-by=claude-opus-4-8 subagent for Omar; feeds=docs/plate-composer-design.md -->

# Plate composer (`slice compose`) — grounded research

Research for the **`tools/bambu slice compose <plate.yaml>`** verb: a manifest of
items composed onto one X2D plate, rendered through bikar and sliced by the Bambu
Studio CLI. This file records every load-bearing fact the design doc cites, verbatim
enough that the doc survives its links rotting (`ground-design-doc` rule: restate the
number here). Facts already proven inside this repo are tagged **[PROVEN-IN-REPO]**;
X2D specifics that rest on H2-family or secondary sources rather than X2D hardware are
tagged **[X2D-UNCONFIRMED]**, matching the convention in
[`print-model-research.md`](print-model-research.md).

---

## Topic 1 — Bambu Studio headless CLI flags (the slicer the composer drives)

Fetched 2026-09-18 from the official wiki
**https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage**. Exact flags,
quoted:

- `--slice <n>` — "Slice the plates: 0-all plates, i-plate i, others-invalid".
- `--export-3mf <filename.3mf>` — export the project as a sliced `.3mf`.
- `--outputdir <dir>` — output directory for exported files.
- `--arrange <n>` — "Arrange options: 0-disable, 1-enable, others-auto". So
  `--arrange 1` is the documented spelling for *enable auto-arrange*.
- `--orient` — orient the model.
- `--scale <factor>` — "Scale the model by a float factor".
- `--load-settings "machine.json;process.json"` — load machine + process settings,
  **up to one of each**, as `;`-joined **JSON file paths** (not preset display names).
- `--load-filaments "filament1.json;filament2.json;..."` — load one or more filament
  JSONs as a `;`-joined list.
- `--debug <level>` — logging level 0–5.
- **Multiple input models** are passed as trailing positional arguments at the end of
  the command line (several `.stl`/`.3mf`/`.step`/`.obj` paths). This is what lets one
  slicer invocation take *all* the composer's rendered STLs onto one plate.
- **No `--rotate` flag** is documented on this wiki page (rotation is folded into
  `--arrange`/`--orient`); the composer must not rely on a `--rotate` it cannot see.

### [PROVEN-IN-REPO] the same flags already work here

`tools/bambu/src/commands/slice.ts` (`buildStudioArgs`, shipped) builds exactly this
vector for a *single* model today: `--debug 2` (raise log level so slicing warnings
reach stdout), then `--load-settings`, `--load-filaments`, `--arrange 1` (when the
`--arrange` flag is set), `--slice <plate>`, `--outputdir`, `--export-3mf <out>`, then
the input path last. It also proves two operational facts the composer inherits:

- **`slice.ts` resolves a preset *display name* → its bundled JSON** under
  `<app>/Contents/Resources/profiles/<Vendor>/{machine,process,filament}/<name>.json`,
  because `--load-settings`/`--load-filaments` reject a bare name with "can not find
  setting file". So the composer keeps ONE spelling of a profile (the display name) and
  reuses `slice.ts`'s resolver rather than a second one.
- **A sliced `.3mf` gets a warnings sidecar** (`bambu slice` writes
  `parseSlicerWarnings`/`classifyWarnings` output beside the `.3mf`, bound to the file's
  sha256), which the dispatch gate `bambu print send` reads. The composer produces a
  `.3mf` with the same sidecar, so no new gate seam is needed.

## Topic 2 — auto-arrange internals (why `--arrange 1` is the composer's packer)

From [`print-model-research.md`](print-model-research.md) Topic 4 (fetched 2026-09-16,
deepwiki BambuStudio 7.4 auto-arrange page):

- Placement is powered by **libnest2d** (a customized fork in BambuStudio) implementing
  **No-Fit-Polygon (NFP)** bin-packing — the same nesting library PrusaSlicer and
  OrcaSlicer use.
- Auto-arrange tries **at most 4 angles: 0 / 45 / 90 / 135°**; `spacing` sets the
  minimum gap; in **by-object** print sequence the arrange polygon is expanded by
  `max(spacing, extruder_radius)` so the toolhead clears already-printed parts.

Consequence for the composer: because NFP + the 4-angle search is the *authoritative*
packer and it runs *inside* the slicer, the composer does **not** implement its own 2D
packer. It hands every STL to `--arrange 1` and lets the slicer place them. A composer-
side check can only be a cheap *necessary* precondition (Topic 3), never a claim that a
plate tiles.

### [X2D-UNCONFIRMED] dual-nozzle bed zoning

[`print-model-research.md`](print-model-research.md) Topic 4 records a forum report that
BambuStudio auto-arrange did **not** use the H2D's L/R-nozzle-only bed areas
(https://forum.bambulab.com/t/auto-arrange-with-h2d-wont-use-l-r-nozzle-only-areas/188640,
fetched 2026-09-16). Dual-nozzle bed zoning on the X2D is unverified, so the composer
must not assume the whole 256×256 area is uniformly usable on a *multi-filament* plate
(see Topic 3's dual-nozzle footprint caveat).

## Topic 3 — X2D build area (the `--bed x2d` default)

The primary source **https://bambulab.com/en/x2d/specs** returned **HTTP 402/403 to the
fetcher** on both 2026-09-16 (recorded in
[`geogebra-construction-import-survey.md`](geogebra-construction-import-survey.md) §9)
and again 2026-09-18 (this session), so the number rests on secondary corroboration:

- **Single-nozzle build volume: 256 × 256 × 260 mm.** Corroborated 2026-09-18 by
  https://www.goodprints3d.com/blogs/3d/bambu-lab-x2d-build-plate-size-and-build-volume-what-you-actually-get
  and https://www.3djake.com/bambu-lab/x2d (search results, WebSearch 2026-09-18).
- **Dual-nozzle build volume: 235.5 × 256 × 256 mm** — the usable **X** narrows to
  **235.5 mm** when both nozzles are in play (same sources). This is the K1 qualifier on
  the 256×256 default: 256 mm across X is the *single-nozzle* footprint.

### [PROVEN-IN-REPO] how the repo already treats this

- [D-053](../decisions-log.md) decided the X2D **rides as a single-nozzle-labelled FDM
  target**; its `PrintTarget` carries a **build envelope only**, and the dual nozzle is
  a *slicer-profile* concern, not a knob. So 256 × 256 mm — the single-nozzle build area
  — is the value the repo uses for the X2D's footprint, and a `--bed x2d` default of
  256 × 256 mm is consistent with D-053, not a new claim.
- The bed value **256 × 256 mm** is already stated as a `**Default:**` for the sibling
  `--bed x2d` in [`geogebra-construction-import-design.md`](../geogebra-construction-import-design.md)
  §9, with this same 403/secondary-source caveat. The plate-composer doc restates it so
  the two docs agree (K7 across the corpus).

**Bed area = 256 × 256 = 65,536 mm².** This is the pure necessary-condition ceiling the
pre-check uses (Topic 4): a plate whose parts' *raw footprint area* alone exceeds
65,536 mm² cannot fit under any packing, no calibration constant required.

## Topic 4 — the bed-fit pre-check is a necessary condition, not a sufficiency claim

Two facts bound what a pre-slicer check can honestly assert:

1. **A per-part claim: each footprint must fit the bed rectangle.** A single part whose
   bounding box exceeds a bed dimension (X = 256 mm single-nozzle, or 235.5 mm across X
   with dual nozzles, Topic 3) can never be placed, whatever the rest of the plate looks
   like. This is a per-part test; an *aggregate* area check cannot discharge it — the
   repo's standing K6/D2 rule that "an aggregate cannot discharge a claim about every
   part" ([`CLAUDE.md`](../../CLAUDE.md)). The hard failure is exactly one oversized part
   on an otherwise near-empty plate: total area passes, the part still cannot fit.
2. **An aggregate necessary condition: Σ footprint area ≤ bed area.** If the summed raw
   footprint areas exceed 65,536 mm², no arrangement can fit them — sound with no fudge
   factor, so it needs no calibration number and stays clear of the D3/D4 bare-number
   rule.
3. **What the pre-check CANNOT prove: that the parts tile.** Parts whose areas fit can
   still fail to pack (concave shapes, no-fit polygons). Only the slicer's `--arrange 1`
   NFP result (Topic 2) is authoritative on tiling. So the pre-check is a *fail-fast
   necessary gate* that runs before the slow slicer; the slicer's arrange result is the
   sufficiency authority. Claiming the pre-check proves fit would be the silent-porting
   hazard (K10) — porting NFP's confidence onto a bounding-box aggregate.

This mirrors the plate-builder doc's advisory-vs-authoritative fit split
([`plate-builder-design.md`](../plate-builder-design.md) §5) and the geogebra doc's own
`**Validator:**` note ([`geogebra-construction-import-design.md`](../geogebra-construction-import-design.md)
§9) that "the hard case is a manifest whose area fits but whose pieces do not tile …
only the slicer's arrange result catches."

## Topic 5 — the iteration identity the manifest must NOT fork [PROVEN-IN-REPO]

From [`print-metadata-and-reprint-design.md`](../print-metadata-and-reprint-design.md),
the owner of the iteration model:

- **§2.2 — the iteration id.** `iteration.id = it-<sha12>`, where `<sha12>` is the first
  12 hex of the sha256 over the canonical JSON of the **iteration key**
  `{source, source_sha256, piece, params, slice_profile}`. Content-addressed: any param
  or preset change flips the id; the same recipe re-derives the same id, with no central
  allocator to collide on (PMR-1).
- **§3.5 — one spelling of the slice profile.** `iteration.key.slice_profile` stores the
  exact `--settings "machine;process"` and `--filament "<name>"` preset **display
  names** `slice` consumes — the same strings `slice.ts` resolves (Topic 1). The slice
  profile is *not* re-derivable from the nine-field process `profile` block; it is stored
  because the reprint/replay path needs the machine + filament preset names the profile
  does not carry (K10 transfer condition, §2.1).
- **§5 — the plate↔iteration map.** A plate record carries `objects[]`; the additive
  field `objects[].iteration` is the `it-<sha12>` that on-plate object instances, and
  `objects[].count` is its physical multiplicity on that plate. Geometry pins per object
  are `source` (`bikar:<path>`), `source_sha256`, `piece`, `params`
  ([`prints-tab-design.md`](../prints-tab-design.md) §4.1, gate rule R1/R8).
- **§4.2 / §4.4 — replay vs re-slice.** Byte-identical replay of a stored `.3mf` is valid
  **only** for the identical plate (same products, same arrangement, same quantity, sha
  intact); **any** quantity or product-selection change forces a re-slice through the
  arrangement path. Composing a *new* multi-item plate is always such a change.

The house rule these enforce: **"a migration never buys a fork"**
([`CLAUDE.md`](../../CLAUDE.md), [D-052](../decisions-log.md)). A manifest that minted a
second identity for a printable thing, parallel to `it-<sha12>`, would be that fork. The
design doc's §3 reconciliation (the manifest item's `{bkr, piece, params}` triple is the
*geometry half* of an iteration key, completed by the plate's slice profile and resolved
to `it-<sha12>`; the record's `objects[].iteration` is the single map) is grounded here.

## Topic 6 — dynamic size is a `--param` re-render, never a mesh scale [PROVEN-IN-REPO]

[D-059](../decisions-log.md): "mini and standard coasters are two values of one `param`
in one file, never two files and never a scaled mesh. The plate composer re-renders every
variant through bikar; its mesh `--scale` passthrough prints a warning naming this entry."
The reason: "scaling a mesh scales walls, straps and relief with it, and a 40 % mini of a
standard coaster puts every strap below the printable-feature floor `CAL-FEA-01` governs."
So the composer's per-item `params` drive a bikar `--param` re-render; the Bambu Studio
`--scale` flag (Topic 1) is exposed only as a flagged escape hatch that prints the D-059
warning, never the sizing mechanism.

## Topic 7 — render cache keyed by bkr-hash + params [PROVEN-IN-REPO adjacent]

The manifest re-renders each distinct `{bkr, params}` variant through bikar once and
caches the STL keyed by the bkr blob hash + the canonical params — the same content-
address discipline the geometry pin already uses (`source_sha256` over the bkr blob at a
pinned commit, [`prints-tab-design.md`](../prints-tab-design.md) §4.1 R1). Two manifest
items with the same `{bkr, params}` and different `count` render once and place N copies.
This is a cache key, not a new identity: it coincides with the *geometry half* of the
iteration key (Topic 5), which is why the cache and the iteration id never disagree.

---

## Appendix A — sources

- **Bambu Studio CLI (primary):**
  https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage (fetched 2026-09-18) —
  flags in Topic 1.
- **X2D specs (primary, unreachable):** https://bambulab.com/en/x2d/specs (402/403 to the
  fetcher, 2026-09-16 and 2026-09-18).
- **X2D build volume (secondary corroboration, fetched/searched 2026-09-18):**
  https://www.goodprints3d.com/blogs/3d/bambu-lab-x2d-build-plate-size-and-build-volume-what-you-actually-get,
  https://www.3djake.com/bambu-lab/x2d.
- **Auto-arrange / libnest2d NFP:** deepwiki BambuStudio 7.4, via
  [`print-model-research.md`](print-model-research.md) Topic 4 (fetched 2026-09-16).
- **Dual-nozzle bed zoning (unconfirmed):**
  https://forum.bambulab.com/t/auto-arrange-with-h2d-wont-use-l-r-nozzle-only-areas/188640
  (fetched 2026-09-16, via Topic 4).
- **In-repo:** [`slice.ts`](../../tools/bambu/src/commands/slice.ts);
  [`print-metadata-and-reprint-design.md`](../print-metadata-and-reprint-design.md) §§2,3,4,5;
  [`prints-tab-design.md`](../prints-tab-design.md) §4.1;
  [D-052](../decisions-log.md), [D-053](../decisions-log.md), [D-059](../decisions-log.md).
</content>
</invoke>
