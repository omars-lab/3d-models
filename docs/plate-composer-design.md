# Plate composer — many rendered pieces onto one X2D plate

*Status: DRAFT, DESIGN ONLY — NOT BUILT. Every path this doc gives for a new subverb,
flag, or file is a **target**, not a shipped file. This is task #12 P4.1 of
[`.claude/plans/coaster-border-continuation.md`](../.claude/plans/coaster-border-continuation.md)
§4. It specifies the composer that
[`geogebra-construction-import-design.md`](geogebra-construction-import-design.md) §9
summarizes and defers to "the plate doc" — this one. Its key decision is
[D-072](decisions-log.md); the decisions-log entry is written at integration, not here.
Research on file: [`research/plate-composer-research.md`](research/plate-composer-research.md).*

The composer is a **new `slice compose` subverb of the existing `slice` command group**
in [`tools/bambu`](../tools/bambu/README.md) — a sibling to the shipped `slice plate`
and `slice open` ([`slice.ts`](../tools/bambu/src/commands/slice.ts)). It takes a
manifest of items, renders each through bikar, and hands *all* the STLs to the Bambu
Studio CLI in one `--arrange 1 --export-3mf` invocation, producing one composed plate
`.3mf`. It is not a new CLI and not a new top-level command; it extends `slice.ts`.

---

## 1. The ask

Plan §4 P4.1: `tools/bambu slice compose <plate.yaml>` — a manifest of items
`{bkr, piece, params, count}`; render each variant via bikar (cache keyed by bkr-hash +
params); collect STLs; call the Bambu Studio CLI with all inputs `--arrange 1
--export-3mf`; `--dry-run` prints the argv; `--bed x2d` = 256 × 256 mm with an
area/count pre-check that fails *before* the slicer; per-object provenance
`bikar:<path>@<ref>` in the plate record; a mesh `--scale` passthrough that prints the
dynamic-STL warning. The first consumer is the mini plate
`docs/plates/<name>.yaml` (plan §4 P4.2); the plate-builder frontend
([`plate-builder-design.md`](plate-builder-design.md)) sits on top of this verb and
does not reimplement it.

Read as a careful colleague would: the composer is **plumbing over three things this
repo already owns** — bikar's renderer, `slice plate`'s Bambu Studio invocation, and the
print record's iteration model. Its whole job is to compose them without inventing a
fourth source of truth. The one genuinely new idea it must get right is stated in §3.

## 2. What exists today, and what the composer reuses

`slice compose` is deliberately thin because `slice plate` already does the hard part for
one model. The reuse boundary, read end-to-end from
[`slice.ts`](../tools/bambu/src/commands/slice.ts):

| Concern | Reused verbatim from `slice.ts` | Genuinely new in `compose` |
|---|---|---|
| Preset name → bundled JSON | `resolvePresetList` (one spelling of a profile across CLI + docs) | — |
| Studio CLI argv | `buildStudioArgs` (`--debug 2`, `--load-settings`, `--load-filaments`, `--arrange 1`, `--slice`, `--outputdir`, `--export-3mf`, input last) | extend to append **N** trailing input paths, not one |
| Dual-nozzle filament grouping | `filamentMapModeEnum`, `filamentCount`, `injectFilamentMapMode` (X2D `filament_map_mode`) | — |
| Warnings sidecar | `parseSlicerWarnings`/`classifyWarnings`/`sidecarPath`/`hashFile` (the sidecar `bambu print send` reads) | — (composed `.3mf` gets the same sidecar) |
| Backend router, Studio locate, timeout, `ev` logging | `surveyBackends`/`preferenceFor`, `locateStudio`, `runWithTimeout`, `ev` | — |
| Sliceable-extension guard | `SLICEABLE` set | applied to each rendered STL |
| bikar render of a variant | — (`slice plate` takes an already-rendered mesh) | **new**: shell to bikar per item, cache keyed by bkr-hash + params (§4) |
| Manifest parse | — | **new**: read `plate.yaml` (§4) |
| Bed footprint + fit pre-check | — (no `--bed` flag today) | **new**: `--bed` + the pre-check (§6) |
| Iteration id + record provenance | — | **new**: resolve each item to `it-<sha12>`, write the plate record (§3, §7) |

So the composer adds a *manifest → render loop → multi-input slice → record* wrapper and
reuses everything `slice plate` proved. It keeps the flag surface consistent with its
sibling: `-o/--out`, `-d/--outputdir`, `-s/--settings`, `-f/--filament`, `--arrange`,
`--dry-run`, `-t/--timeout`, `--strict` carry the same meaning as on `slice plate`; the
only additions are the `<plate.yaml>` argument and `--bed` (§6). (There is no `slice
mesh` or `--bed` in the repo today — both are named here as targets, not as shipped
surface, to keep the claim honest.)

## 3. The pivotal question: the manifest does not fork the iteration model (D-072)

A `plate.yaml` item is `{bkr, piece, params, count}`. The print record already has an
identity for "a printable thing":
[`print-metadata-and-reprint-design.md`](print-metadata-and-reprint-design.md) §2.2
defines the **iteration id** `it-<sha12>` = the first 12 hex of sha256 over the canonical
JSON of the **iteration key** `{source, source_sha256, piece, params, slice_profile}`,
and §5 defines the plate↔iteration map `objects[].iteration`. The house rule is **"a
migration never buys a fork"** ([`CLAUDE.md`](../CLAUDE.md), [D-052](decisions-log.md)):
a manifest that minted a *second* identity for a printable thing, parallel to
`it-<sha12>`, would be exactly that fork, and is wrong.

**The reconciliation (D-072): a manifest item is not an identity — it is the *geometry
half* of an iteration key, completed by the plate's slice profile and resolved to
`it-<sha12>`.** Concretely:

- `bkr` resolves to `source: bikar:<path>@<ref>` and `source_sha256` (the bkr blob hash
  at the pinned ref — the same pin gate rule R1 already computes,
  [`prints-tab-design.md`](prints-tab-design.md) §4.1). With `piece` and canonicalized
  `params`, that is four of the five iteration-key fields.
- The fifth field, `slice_profile` (the `--settings "machine;process"` and `--filament`
  preset display names), is **not per item** — it is the plate's, taken from the
  `profile:` block of `plate.yaml` or the `-s/-f` flags. One plate is sliced under one
  profile.
- The composer computes `it-<sha12>` for each item from (its geometry triple) + (the
  plate profile), and **writes the resolved id into the plate record's
  `objects[].iteration`**, with `count` → `objects[].count`. The record — the single
  source of truth — carries the ids; the manifest is an *authoring surface* that resolves
  to them and stores no parallel id of its own.

> **K10 — the transfer condition, written.** The manifest's `{bkr, piece, params}` triple
> transfers to the iteration key **because** it *is* the key's geometry half by
> construction, and the missing fifth field is supplied by the one profile the plate is
> sliced under — so a `{bkr, piece, params}` triple and an `it-<sha12>` coexist without
> two sources of truth: the triple never names an identity on its own, and the id is
> derived, written to the record, and never stored back into the manifest. If a future
> manifest wanted per-item slice profiles (mixed profiles on one plate), this transfer
> would break — an item would need its own profile to complete its key — and that is the
> condition under which the reconciliation would have to be revisited, not assumed.

**An item may also be written directly as an iteration id** — `{iteration: it-<sha12>,
count}` — for "put this exact known recipe on the plate." The composer resolves that
through the record store the way
[`print-metadata-and-reprint-design.md`](print-metadata-and-reprint-design.md) §4's
`reprint` does (newest record with that id → its `key`), then re-renders and re-slices,
because composing a fresh multi-item plate is an arrangement change and §4.4 makes any
arrangement change a re-slice, never a byte-identical replay. Both spellings resolve to
the same `it-<sha12>`; the record stores one map.

This also disposes of a would-be second identity from the render cache (§4): the cache
key (bkr-hash + params) *coincides with* the geometry half of the iteration key, so the
cache and the id are the same content-address seen twice, and cannot disagree.

## 4. The manifest

`plate.yaml` is a small, hand-authorable file:

```yaml
bed: x2d                       # bed footprint name (§6); default x2d
profile:                       # the ONE slice profile the plate is sliced under (§3)
  settings: "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D"   # -s (machine;process)
  filament: "Bambu PLA Basic @BBL X2D 0.4 nozzle"                 # -f
items:
  - bkr:    bikar:patterns/Constructions/<id>-coaster.bkr
    piece:  Coaster
    params: { size: 40, border: 4 }     # bikar --param overrides — dynamic size is a re-render (§8)
    count:  2
  - bkr:    bikar:patterns/Constructions/<other>-coaster.bkr
    piece:  Coaster
    params: { size: 40 }
    count:  2
  - iteration: it-9f3c1a2b4d5e           # OR: an already-known iteration id (§3)
    count:  1
```

- **`bkr`** is a `bikar:<path>` source; the composer pins it to the bikar HEAD ref at
  compose time (`bikar:<path>@<ref>`) and records its blob `source_sha256`, exactly the
  provenance `print send --record` already scaffolds
  ([`tools/bambu/README.md`](../tools/bambu/README.md), R1).
- **`params`** are bikar `--param` overrides; they and the bkr hash form the render-cache
  key (§7) and the iteration key's geometry half (§3).
- **`count`** is the physical multiplicity on this plate → `objects[].count` (R8).
- **`piece`** names the bikar piece to render (as `slice plate` and the record schema
  already use `piece`).

The composer renders each **distinct** `{bkr, params}` once (cache), then places `count`
copies of the resulting STL, letting `--arrange 1` position them (§6).

## 5. The verb and its argv

```
bambu slice compose <plate.yaml> [-o out.3mf] [-d dir] [-s ...] [-f ...] [--bed x2d]
                                 [--arrange] [--dry-run] [-t secs] [--strict]
```

Flow: parse `plate.yaml` → resolve the plate profile once via `resolvePresetList` →
for each distinct `{bkr, params}` render an STL through bikar (cache, §7) → run the bed
pre-check on the footprints × counts (§6) → build the Studio argv with **all** STL paths
as trailing inputs and `--arrange 1` → slice → write the warnings sidecar → scaffold the
plate record with resolved `objects[].iteration` provenance (§7). `-s/-f` on the command
line override the manifest `profile:` (one spelling either way).

**`--dry-run` prints the exact argv and touches no hardware and no slicer** — the same
contract `slice plate --dry-run` honors, extended to first print the render plan (which
variants would render, cache hits/misses) and the resolved iteration ids, then the
Studio command line with every input. A dry run is a single allow-listable command that
lets a reader inspect the whole plan before a byte is sliced.

The Studio invocation is `buildStudioArgs` extended to take an array of inputs: `--debug
2 --load-settings <machine;process> --load-filaments <filament> --arrange 1 --slice 0
--outputdir <dir> --export-3mf <out> <stl1> <stl2> …`. `--slice 0` slices all plates;
multiple trailing model paths are how the Bambu Studio CLI composes several objects onto
one plate ([`research/plate-composer-research.md`](research/plate-composer-research.md)
Topic 1).

## 6. The bed and the fit pre-check

**Default:** the `--bed x2d` footprint is **256 × 256 mm**, the X2D single-nozzle build
area ([bambulab X2D specs](https://bambulab.com/en/x2d/specs) returned 402/403 to the
fetcher, so the number rests on secondary corroboration —
[goodprints3d](https://www.goodprints3d.com/blogs/3d/bambu-lab-x2d-build-plate-size-and-build-volume-what-you-actually-get)
and [3DJake](https://www.3djake.com/bambu-lab/x2d), recorded in
[`research/plate-composer-research.md`](research/plate-composer-research.md) Topic 3),
consistent with [D-053](decisions-log.md) treating the X2D as a single-nozzle-labelled
FDM target whose `PrintTarget` is a build envelope only.

> **K1 — the qualifier carried, not stripped.** 256 mm across X is the *single-nozzle*
> footprint. On a *dual-nozzle / multi-filament* plate the usable X **narrows to
> 235.5 mm** ([`research/plate-composer-research.md`](research/plate-composer-research.md)
> Topic 3), and dual-nozzle bed zoning on the X2D is an unverified open item (Topic 2,
> `[X2D-UNCONFIRMED]`). So the 256×256 default is the single-nozzle build area D-053
> names; a multi-filament plate's true usable area is the slicer's `--arrange` authority,
> and the pre-check does not assume the whole 256×256 is uniformly usable there.

**Default:** the compose arrange mode is **`--arrange 1`** (the Bambu Studio CLI's
documented "enable auto-arrange"; libnest2d No-Fit-Polygon packing over the inputs,
trying at most the 4 angles 0/45/90/135°) — see the CLI wiki
([github.com/bambulab/BambuStudio](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage))
and [`research/plate-composer-research.md`](research/plate-composer-research.md) Topics 1–2.
The composer does **not** ship its own 2D packer; it owns one only as a fallback (plan
P2) *if* `--arrange` proves unreliable on real X2D plates, and only then, recorded in
`docs/issues/`. It is not designed now.

**Validator:** the composer runs a bed-fit pre-check **before** invoking the slicer, and
it is a *necessary* condition only, in two parts — (i) **per-part**: every single item's
footprint bounding box fits the bed rectangle (`x ≤ 256`, `y ≤ 256` for `x2d`; the
narrower dual-nozzle X of the K1 note when applicable); (ii) **aggregate**: the summed
footprint area × count is ≤ the bed area (65,536 mm² for `x2d`). It never reports "fits"
as a guarantee — tiling is the slicer's `--arrange` result, not the pre-check's
([`research/plate-composer-research.md`](research/plate-composer-research.md) Topic 4).
- PASS: a manifest of 9 minis at 40 mm (each ≈ 40×40) plus 2 standards at 90 mm — every
  part is well within 256 mm and the summed area (`9·1,600 + 2·8,100 ≈ 30,600 mm²`) is
  under 65,536, so the pre-check passes and the composed `.3mf` is handed to `--arrange`.
- FAIL: the hard case is **one oversized part on an otherwise near-empty plate** — a
  single 300 mm-wide piece (`count 1`) beside two 20 mm minis. The *aggregate* area
  (`300·h + 2·400`) can sit far under 65,536 mm², so an area-only check passes it, yet the
  300 mm part cannot fit a 256 mm bed under any arrangement. The per-part check (i) catches
  it; the aggregate (ii) cannot, because an aggregate cannot discharge a per-part claim
  (K6/D2, [`CLAUDE.md`](../CLAUDE.md)). The pre-check refuses it before the slow slicer
  runs, naming the offending item and its dimension.

The complement — a plate whose parts' areas fit but that does **not tile** (concave/no-fit
shapes) — is deliberately **not** the pre-check's claim to make: the pre-check passes it,
and `--arrange` is the authority that catches a genuine no-fit, exactly as
[`geogebra-construction-import-design.md`](geogebra-construction-import-design.md) §9 and
[`plate-builder-design.md`](plate-builder-design.md) §5 draw the advisory-vs-authoritative
line.

## 7. Render cache and record provenance

**Render cache.** Each distinct `{bkr, params}` renders through bikar once and the STL is
cached keyed by the bkr blob hash + canonical params
([`research/plate-composer-research.md`](research/plate-composer-research.md) Topic 7).
Two items sharing a `{bkr, params}` and differing only in `count` render once and place N
copies. The key is a cache key, not an identity; it coincides with the geometry half of
the iteration key (§3), so cache and id never disagree.

**Record provenance.** On a real (non-dry) compose, the verb scaffolds a plate record via
the existing `records.ts` scaffolder (the one `print send --record` uses,
[`tools/bambu/README.md`](../tools/bambu/README.md)), writing per on-plate object:
`source: bikar:<path>@<ref>`, `source_sha256`, `piece`, `params`, `count`, and the
resolved `iteration: it-<sha12>` (§3). The composed `.3mf` and its sha go into
`plate_3mf`/`produced` exactly as
[`print-metadata-and-reprint-design.md`](print-metadata-and-reprint-design.md) §3.2
specifies. The composer stops at a `status: sliced` draft under
`.bambu/records/<date>-<slug>/` and the **owner gate** — it never dispatches (dispatch is
`print send`, owner-gated, [`print-model-design.md`](print-model-design.md) §9). No new
record store, no forked schema: the composer *fills* the schema those docs own.

## 8. Dynamic size is a `--param` re-render; mesh `--scale` is a flagged escape hatch

Per [D-059](decisions-log.md): sizing is always a bikar `--param` re-render (a mini is
`params: { size: 40 }`, a standard `size: 90`), never a scaled mesh, because scaling a
mesh scales walls, straps and relief below the printable-feature floor `CAL-FEA-01`
governs ([`research/plate-composer-research.md`](research/plate-composer-research.md)
Topic 6). The composer therefore drives size through `params` in the manifest. The Bambu
Studio `--scale` flag is exposed only as a flagged passthrough (after `--`, like
`slice plate`'s raw-arg escape hatch), and **using it prints the D-059 warning** naming
this entry — the same "say the hazard out loud" discipline `slice plate` uses for its
dual-nozzle no-op. `--scale` is never the sizing mechanism.

## 9. Decisions

- **D-072** (this doc's key decision): the `plate.yaml` manifest is an **authoring
  surface**, not an identity. A manifest item's `{bkr, piece, params}` triple is the
  geometry half of the iteration key
  ([`print-metadata-and-reprint-design.md`](print-metadata-and-reprint-design.md) §2.2),
  completed by the plate's one slice profile and resolved to `it-<sha12>`; the composed
  plate record's `objects[].iteration` is the single plate↔iteration map. The manifest
  mints no parallel id, and the render cache key coincides with the iteration key's
  geometry half, so nothing forks (the K10 transfer condition in §3). See
  [D-072](decisions-log.md). *(The bed-fit pre-check design, the `--bed x2d`/`--arrange 1`
  defaults, and the `slice.ts` reuse boundary are design details of this same decision; if
  the integrator judges any needs its own id, a second decision is pending id — this doc
  does not take D-073.)*
- Local ids scoped to this doc (`PC-*`), **not** entries in
  [`decisions-log.md`](decisions-log.md):

| # | Decision | Options | Recommendation & why |
|---|---|---|---|
| PC-1 | Where the composer lives | (a) a new `slice compose` subverb extending `slice.ts`; (b) a new top-level command; (c) a new CLI | **(a).** Reuses `slice plate`'s render/slice path, argv builder, preset resolver and warnings sidecar (§2); a second command or CLI would fork the Studio invocation — the fork [D-052](decisions-log.md) forbids. |
| PC-2 | Manifest ↔ iteration identity | (a) items resolve to `it-<sha12>` (the record is the one map); (b) the manifest carries its own item ids | **(a) = D-072.** (b) is a second source of truth for a printable thing — the exact fork the house rule bans. |
| PC-3 | Composer-side packer | (a) hand every STL to `--arrange 1` (NFP, in the slicer); (b) ship a 2D packer now | **(a).** The authoritative packer is libnest2d inside the slicer (Topic 2); a self-owned packer is a P2 fallback only if `--arrange` proves unreliable, recorded in `docs/issues/` — not built now. |
| PC-4 | Bed-fit pre-check strength | (a) a necessary condition (per-part + aggregate area) that fails fast; (b) claim it proves the plate fits | **(a).** Only `--arrange` proves tiling (§6, Topic 4); an aggregate area check cannot discharge the per-part fit claim (K6/D2). Over-claiming would be the K10 silent-porting hazard. |
| PC-5 | Sizing | (a) `--param` re-render per item; mesh `--scale` a warned escape hatch | **(a) = D-059.** Mesh scaling drives features below the printable floor; the passthrough prints the D-059 warning. |

## 10. Read against itself (K7)

- **The flagship flow is buildable by the machinery cited.** Compose = parse manifest →
  bikar render (cache) → `buildStudioArgs` with N inputs + `--arrange 1` → warnings
  sidecar → `records.ts` scaffold. Every step but the render loop, the manifest parse, the
  `--bed` pre-check and the id resolution is reused verbatim from `slice.ts` (§2) — no new
  slicer path, no forked record store.
- **No new concept where one exists.** §3 binds a manifest item to the *existing*
  `it-<sha12>` iteration key rather than inventing a parallel unit — consistent with
  PMR-2 and the D-052 no-fork rule; the render cache key is shown to *coincide* with the
  key's geometry half, not to be a second id.
- **The defaults and the validator agree.** `--bed x2d` = 256×256 (single-nozzle) and the
  pre-check's `x ≤ 256 / area ≤ 65,536` use the same number; the K1 note that dual-nozzle
  X narrows to 235.5 mm is carried in the same section, not stripped, and the pre-check
  explicitly defers tiling to `--arrange` rather than claiming sufficiency.
- **Every claim carries its hedge (K1/K2).** The bed number rests on secondary sources
  because the primary 403'd (said so, §6 + research Topic 3); the arrange internals and
  dual-nozzle zoning are `[X2D-UNCONFIRMED]` where unproven; the `slice.ts` reuse table
  says plainly there is no `slice mesh` or `--bed` today. The four bed-fit outcomes name a
  set (per-part, aggregate, tiles, does-not-tile), not "no plate can fail otherwise."
- **The validator's FAIL is the hard case.** Not a trivially-too-big plate but one
  oversized part hiding under an aggregate area that fits — the per-part check must fire
  where the aggregate cannot (K6/D2), which is the substitution the gate discipline warns
  a passing aggregate can smuggle through.
- **Every relative link resolves on disk or is a placeholder.** Sibling docs, the research
  file, `slice.ts` and `CLAUDE.md` exist; new artifacts appear only as placeholders
  (`plate.yaml`, `docs/plates/<name>.yaml`, `bikar:<path>@<ref>`, `it-<sha12>`,
  `.bambu/records/<date>-<slug>/`), so no pointer is stale.

## 11. Not yet

- **Nothing is built and nothing prints.** Printing stays owner-gated ([D-060](decisions-log.md); no
  `CAL-CST-*` bet settled); the composer stops at the owner gate (§7).
- **The mini plate manifest** `docs/plates/<name>.yaml` (plan P4.2) is the composer's
  first real input and is authored after the verb ships; `bambu validate plate` must
  accept the composed `.3mf`.
- **A self-owned 2D packer** (plan P2) is a fallback only if `--arrange` proves
  unreliable on hardware — a `docs/issues/` entry with the evidence, then a design, not a
  speculative build (PC-3).
- **Per-item slice profiles** (a mixed-profile plate) would break the §3 transfer
  condition and are out of scope; the manifest carries one plate profile until a real need
  names the shape.
</content>
