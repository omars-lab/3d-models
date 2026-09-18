<!--
provenance:
  date: 2026-09-18
  produced-by: subagent (Claude Opus 4.8) for Omar, in worktree 3d-models-colour on feat/design-colour
  feeds: docs/coaster-colour-design.md (the coaster colour-region / per-body export / filament-map route, D-073)
  method: in-repo reads at the sibling checkouts present on this machine
          (~/Workspace/git/bikar on feat/bambu-x2d-print-target, ~/Workspace/git/3d-models on feat/x2d-slice-preflight)
          plus one WebSearch pass for Bambu AMS / 3MF facts. External snippets that could not be
          fetched are marked "(unverified snippet)" per the ground-design-doc rule and are hedged
          (K1/K2) in the doc.
-->

# Research — coaster colour regions, per-body export, filament map

This file records what the colour design doc's load-bearing claims trace to. In-repo
facts are cited to the file that states them; external facts carry a URL and, where the
page could not be fetched, an explicit "(unverified snippet)" tag so nothing unfetched
is promoted into the design doc as settled.

## 1. What bikar colour is *today* — 2D SVG only (in-repo, primary)

The producer of record is bikar; its language reference and grammar are the primary
source. Every colour clause bikar has is a **2D rendering** concern that reaches the
SVG output and nothing else:

- `palette <name>` opens a palette block; `<color> = <hex>` names a colour in it; and
  `fill void where <condition> color <color>` fills matching faces. Source: bikar
  `docs/language-reference.md`, "Fill & Palette" table, which points at grammar
  §7.4 "Faces, fills, and classes".
- `edges color <color> [width <N>]`, `circles color …`, `lines color …`, and
  `scale <N>` ("Scale **SVG** output") sit under bikar `docs/language-reference.md`
  "Visual Properties", pointing at grammar §7.5 "Colour and presentation". This is the
  §7.5 the task and the umbrella plan name.
- `strapwork … color <color>` sets an optional band **fill** colour and "defaults to
  the edge color"; the same table says outright "Strapwork is a rendering concern …
  SVG output contains `<g class="strapwork-under">` …". Source: same file, "Strapwork".

**Load-bearing conclusion:** every colour bikar understands is SVG ink. There is no
colour clause that reaches the 3D height-field kernel or the STL. Grounded: the three
tables above are the complete set of colour statements in bikar's language reference as
read on 2026-09-18.

## 2. STL carries no colour; a coaster STL is one body (in-repo, primary)

- A coaster renders through the height-field kernel to a mesh that is "manifold by
  construction with one kernel"; `--check` "runs the mesh gate on every render". Source:
  3d-models `docs/coaster-design.md` (the shape-and-check prose and its `--check`
  sentence). The mesh is one watertight solid — the doc speaks throughout of "the mesh"
  and "the disc/slab", singular, and of the worst point being "named" by one gate over
  one body.
- The direction for colour is already named in the same doc's roadmap bullet: colour
  regions (#37) are "named regions exported as separate bodies (`--format parts`) for a
  filament map in the 3MF; the X2D's AMS assignment happens in the slicer, not in
  bikar." Source: 3d-models `docs/coaster-design.md`, "Colour regions (#37)" bullet.
  This is in-repo confirmation that (a) `--format parts` is the intended mechanism,
  (b) the filament map lives in the 3MF, and (c) AMS-slot assignment is the slicer's job,
  not the kernel's.

**Note (K2):** `--format parts` for a coaster is **not implemented today** — it is named
as the direction, not as a shipped flag. The design doc states this as future work, not
as a current capability.

## 3. The relief is an emboss (in-repo, primary) — the transfer condition for colour

Colour needs a raised region to carry a distinct filament; a debossed pocket removes
material and leaves the slab's own colour, so it cannot be a separately-coloured body on
an FDM multi-material print. The relief mode is already decided:

- **D-066** decided "the relief is an **emboss**" (Omar, AskUserQuestion "A: pattern
  outline + emboss"). Source: 3d-models `docs/decisions-log.md` D-066.
- The importer "emits exactly one: `relief straps emboss 1.2`" and the slab is the
  ground. Source: 3d-models `docs/coaster-design.md` (the emit-exactly-one prose).

So the "Option A → emboss" the umbrella plan cites is D-066, verified. The transfer
condition to write in the doc (K10): the per-body colour split is only meaningful while
the relief is an emboss; if a future coaster debosses a region, that region has no raised
body to assign a filament to, and the split for it is empty by construction — which the
Validator must catch, not silently pass.

## 4. The first region split already exists — the border band (in-repo, primary)

The border kernel already partitions a coaster's cells into **band** and **field**:
`reliefAppliesAt` splits on `outlineInset(p) < W`, and the field records a per-cell
`band` bit "beside `relief`/`deboss`/`cut`", explicitly "so #37 has something to export
without re-deriving the geometry." Source: 3d-models `docs/coaster-border-design.md`
§3 ("Regions") and §5 ("`reliefAppliesAt` reads by region"), decision D-071.

**Load-bearing conclusion:** the colour route does not invent region-splitting; it
generalises the existing two-way band/field split into a named region vocabulary and adds
the per-body *export*. The border doc's own §10 "Not yet" says the per-body export and
filament map "are #37's, unchanged in direction (D-068)."

## 5. The Coaster Lab and the visibleColours precedent (in-repo, primary)

- **D-067** placed the coaster design UI as a **Coaster Lab in bikar's `packages/lab`**
  (the Orb Lab pattern), not a page in the 3d-model hub. Source: 3d-models
  `docs/decisions-log.md` D-067. Directory `bikar/packages/lab` is present in the sibling
  checkout.
- The Lego Lab already ships a **per-model palette** discipline the colour doc reuses as
  precedent: a render's pixels are classified to "the model's **own palette** plus the
  scene background", the observed set is `visibleColours`, and a `--check` compares the
  observed visible set against a committed `visibleColours` "by set identity". Source:
  3d-models `docs/lego-lab-design.md` §16.1–§16.2. The transfer note the doc must carry
  (K10): the Lego gate proves *palette classification ports where golden pixels do not*;
  the coaster colour Validator borrows the **region-is-a-symbolic-name** idea, not the
  pixel gate — coaster bodies are checked geometrically (watertightness), not by render.

## 6. Bambu AMS / multi-material / 3MF (external — hedged)

One WebSearch pass, 2026-09-18. The Bambu Lab wiki pages returned HTTP 402 to the
fetcher, so the wiki claims below are **(unverified snippet)** — taken from the search
result summaries, not from a fetched page — and are hedged in the doc. They bear only on
the *plate-composer* dependency, which is a different doc's to settle (see §7).

- A multi-body 3MF opens in Bambu Studio with "each body … a separate object in the
  Objects panel", and a filament can be assigned per body from a dropdown; filament can
  be bound to an object/part via the sidebar, right-click, or number keys 1–9.
  (unverified snippet) — search summary of the Bambu Lab wiki "multi color printing" and
  forum threads.
- One source states the slicer "matches color groups to slots by **order, not by hex
  value**", group 0 → AMS slot 1, group 1 → slot 2, etc. (unverified snippet) — a
  community/blog summary, not the primary wiki; treat as *a* reported behaviour, not a
  guaranteed contract.
- Bambu Studio supports vertex and face colouring on 3MF import but "does not yet
  support texture mapping". (unverified snippet)

Primary URLs to fetch when the plate-composer doc is written (recorded so the trail does
not stop):

- Bambu Studio CLI reference: https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage
- Standard 3MF colour parsing: https://wiki.bambulab.com/en/bambu-studio/Standard-3MF-File-Color-Parsing
- Multi-colour printing: https://wiki.bambulab.com/en/software/bambu-studio/multi-color-printing

**UNVERIFIED, load-bearing for the composer (not this doc):** whether per-object
filament/`extruder` assignment must already be present in the *input* 3MF the CLI is
handed, or whether the CLI's `--load-filaments` plus slot-by-order mapping is enough. The
search shows the *GUI* can assign per object after import; it does **not** establish the
*CLI/headless* contract. The plate-composer design owns this question; the colour doc
references it as a dependency and does not resolve it.

## 7. What this doc does not own (scope boundary)

The plate composer (umbrella task P4.1) owns the manifest → AMS-slot mapping and the 3MF
writing; it has its own design doc target (docs/plate-composer-design.md, not yet
written — referenced in prose in the design doc, not as a link, because a link to a
missing file is a D1 gate failure). The colour doc's job is the DSL region vocabulary,
the `color <region> <PaletteName>` clause, the `--format parts` per-body split, and the
Coaster Lab knob — and to hand the composer a clean, named-region contract.

## 8. Load-bearing numbers and their sources (quick index)

| Claim in the doc | Value | Source |
|---|---|---|
| bikar colour is 2D/SVG only | — | bikar `docs/language-reference.md` §7.4/§7.5 tables (§1) |
| STL carries no colour; coaster mesh is one body | — | 3d-models `docs/coaster-design.md` (§2) |
| export mechanism is `--format parts`, filament map in 3MF, AMS in slicer | — | 3d-models `docs/coaster-design.md` #37 bullet (§2) |
| relief is emboss (colour needs a raised body) | emboss | D-066 (§3) |
| first region split (band/field, `band` bit) already exists | — | 3d-models `docs/coaster-border-design.md` §3/§5, D-071 (§4) |
| Coaster Lab is in `bikar/packages/lab` | — | D-067 (§5) |
| per-model palette / visibleColours precedent | — | 3d-models `docs/lego-lab-design.md` §16.1–§16.2 (§5) |
| Bambu per-object filament assignment / slot-by-order | — | (unverified snippet), §6; UNVERIFIED CLI contract |
