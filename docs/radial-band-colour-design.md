# Radial-band colour — the ring a polygon sits in is a print region, reusing one binning

*Status: designed (task #25, decision D-078 pending — the id is minted at merge, see the
decisions log). Omar asked to colour different polygons differently within one construction,
and for tooling to colour the polygons whose centroids are equidistant from the construction's
centre. The finding that shapes this doc: bikar **already** groups a construction's faces into
concentric rings by centroid distance and **already** lets an author colour a ring — as 2D SVG
ink. This doc does not invent radial binning; it carries the ring a polygon already sits in
into the 3D per-region export, so a ring prints in its own filament. It builds directly on
[`coaster-colour-design.md`](coaster-colour-design.md) (D-073, D-074), whose region→body→slot
route it reuses wholesale, and adds one read-only enumeration verb. It adds no new solid and no
new binning. Research on file: [`research/radial-band-colour-research.md`](research/radial-band-colour-research.md).*

## 1. The ask

Omar (2026-09-19): *"in the color mapping process, in the same constructions, i want to be able
to color different polygons differently"* and *"have tooling to make it easier to apply colors
on polygons that have midpoints that are equidistant from midpoint of construction."*

The second sentence names a specific grouping: polygons whose centroid is the same distance from
the construction's centre — concentric **radial bands**. The ask is two things: (1) a way to say
"this band is that colour" that reaches a print, and (2) tooling to see which bands a construction
has before colouring them.

Read as a careful colleague would, against the code: bikar already answers most of (1) for the
**2D** render and none of it for the **3D** print, and answers none of (2). The precise state:

- **Binning already exists.** bikar buckets faces into concentric rings by centroid distance from
  the construction centre (the centre of the first circle, else the origin), innermost = ring 0.
  This is the `ring` fill selector, shipped in the pattern grammar.
- **2D colouring already exists.** `fill where ring == N color <Name>` tints ring `N` in the SVG,
  and each face carries a `data-ring` attribute in the output.
- **It is 2D ink only.** Exactly as [`coaster-colour-design.md`](coaster-colour-design.md) §1
  records for every colour clause bikar has, `fill … color` "never reaches the height-field
  kernel"; the 3D path exports one body per coaster with no colour.
- **The 3D split knows nothing of rings.** `bikar render --format parts` ([bikar PR #275](https://github.com/NaqshCoffee/bikar/pull/275))
  splits the height field into one body per **coaster region** — a fixed three-name set
  `base`, `straps`, `border` — by a relief/inset test, not by which ring a face sits in.
- **No enumeration.** There is no verb that lists a construction's rings, so an author writing
  `fill where ring == N` is guessing `N`.

So the feature is a bridge and a verb, not a grammar: carry the ring index the kernel already
computes into the region-split the exporter already runs, and add a way to list the rings.

## 2. Options and the rubric

Rubric (0/1/2), the same five axes as [`coaster-colour-design.md`](coaster-colour-design.md) §2 so
the two colour routes are judged alike: **R1 the DSL stays about geometry** (a band names a
geometric fact — equal centroid radius — not a hardware slot); **R2 one radial system** (reuse the
shipped ring binning and the shipped colour clause; add no second way to say "a band"); **R3
checkable** (a per-body validator with a constructible FAIL, not a total); **R4 costs the grammar
little** (ideally zero new productions); **R5 ports** (the band survives into the 2D render, the
parts manifest, and the Lab, and is not printer-specific).

| Option | R1 | R2 | R3 | R4 | R5 | Verdict |
|---|---|---|---|---|---|---|
| (a) **Reuse `fill where ring … color`** — the ring an author already colours in 2D becomes a print region; `--format parts` emits one body per coloured ring; the composer maps palette name → AMS slot exactly as for coaster regions | 2 | 2 | 2 | 2 | 2 | **chosen** |
| (b) `color band <i> <Name>` — a new coaster-block statement naming a band by index | 2 | 0 | 2 | 1 | 1 | adds a **second** radial system beside the shipped `fill where ring`; two clauses that mean "the i-th ring" is one name with two spellings — the divergence the [robustness tenet](../CLAUDE.md) calls the defect itself |
| (c) `color ring <r0>..<r1> <Name>` — explicit radius bounds in mm | 1 | 0 | 1 | 1 | 1 | most control over where a band starts, but the author must know the radii, and it still adds a second radial system; the shipped binning already opens a band at each radial gap |
| (d) Do nothing — the ring stays 2D ink | 2 | 2 | — | 2 | — | does not answer the ask (no colour reaches the print); kept as the honest baseline that verifies nothing |

(a) wins because the one thing the DSL should own — *which faces are one band* — is already
owned by the shipped ring binning, and the one thing it should not own — *which spool* — is
already handed to the manifest by [`coaster-colour-design.md`](coaster-colour-design.md). The
feature adds no way to name a band because bikar already has one. Decision **D-078** (2026-09-19,
Omar chose (a) from a rendered comparison of (a)/(b)/(c)).

## 3. What already exists, and what this adds

The honest split, so the review knows what is new versus reused:

**Reused, unchanged (shipped in bikar):**
- The ring binning — faces bucketed by centroid distance from the centre, ring 0 innermost, a new
  ring opened at each radial gap.
- The colour clause — `fill where ring == N color <Name>` and the `palette` block it names.
- The 2D carry — each face emits a `data-ring` index; per-ring animation already keys off it.
- The region→body→slot route — `--format parts` writes one watertight body per region plus a
  `.parts.json` manifest carrying `paletteName`/`hex`, which the plate composer maps to an AMS slot
  ([`coaster-colour-design.md`](coaster-colour-design.md) §4, [bikar PR #275](https://github.com/NaqshCoffee/bikar/pull/275)).

**Added by this doc (proposed, task #25):**
- **§4 — the bridge:** a face's ring index becomes a region key the `--format parts` split honours,
  so a coloured ring exports as its own body.
- **§5 — the `bands` verb:** a read-only CLI verb that lists a construction's rings (index, centroid
  radius, face count) so the author knows which `N` to colour.
- **§6 — the region × ring rule:** how a radial band coexists with a coaster's `base/straps/border`
  without multiplying bodies (the design decision that needs stating, not the easy part).

## 4. The bridge — a ring is a region source

`--format parts` today keys each output body on a coaster region computed from the **height field**
on a grid: a cell is `straps` or `border` by a relief/inset test, `base` otherwise
([`coaster-colour-design.md`](coaster-colour-design.md) §3). Ring membership lives on the **2D
faces**, not the grid — the recon's one real awkwardness. The bridge is a lookup, not a new split:

1. Each grid cell that carries relief samples the 2D face it falls inside (the exporter already
   walks the faces to raise the field; the face index is in hand at sample time).
2. That face's ring index is read from the binning the kernel already computed.
3. The body key becomes the **palette name the author assigned to that ring**, not the ring index —
   so two rings the author gave the same colour merge into one body (one filament, one slot), and a
   ring the author left uncoloured falls to the coaster's own region key (§6). Keying on the colour,
   not the index, is what keeps the body count at the number of filaments rather than the number of
   rings.

A construction that is not a coaster (a bare pattern) has no height field to split; for it, "reach
the 3D print" is out of scope here — this doc bridges rings into the **coaster** export, the only
3D solid bikar ships. A bare pattern keeps its 2D ring colour unchanged. (Stated so §6 and the
status line do not over-claim: this is a coaster-print feature, not a general-solid one.)

## 5. The `bands` verb — enumerate before you colour

A read-only verb modelled on the existing `points` verb (which enumerates a construction's named
points without rendering): `bikar bands <construction.bkr>` prints one line per ring —

```
ring  radius   faces  colour
0     0.00     3      —
1     8.24     6      Gold
2     14.10    6      —
```

`radius` is the mean centroid distance of the ring's faces from the centre; `colour` is the palette
name if a `fill where ring == N` assigns one, `—` otherwise. The data is already in the evaluation
result (the per-face ring indices and colours); the verb is a formatter over it, no kernel change.
It answers "which `N` do I write" and "did my `fill` clause hit the ring I meant" in one place.

**Validator:** `bikar bands <c.bkr>` lists every distinct ring index the binning produced, exactly
once each, in ascending index order, and the count of listed rings equals the number of distinct
`data-ring` values in the same construction's 2D render.

PASS: a rosette whose faces fall in three radial gaps lists rings 0, 1, 2 — three lines — and its
SVG carries `data-ring` values {0, 1, 2}.

FAIL: a construction whose faces all sit at one radius lists two or more rings, or lists ring 0
twice, or lists a ring absent from the SVG's `data-ring` set — any of these means the verb and the
renderer disagree about the binning, which is the bug the validator exists to catch.

## 6. Region × ring — the rule that stops bodies multiplying

A coaster already partitions its cells into `base`, `straps`, `border` (a relief distinction). A
ring partitions faces radially (a planar distinction). The two are **orthogonal**: naïvely, a body
per (region × ring) pair could be many bodies, most empty, and would blow past the AMS slot count
(§7). The rule that prevents this, and the one design choice a reader must check:

**A ring colour, when present on a face, overrides that face's coaster-region key for the split.**
So the body set is: one body per palette name assigned to any ring, plus the coaster's own
`base/straps/border` bodies for the faces no ring colour claimed. The author gets exactly as many
bodies as they gave colours — never the Cartesian product.

This is the K7 check against [`coaster-colour-design.md`](coaster-colour-design.md): that doc's
`color <region> <Name>` and this doc's `fill where ring … color` can both be written in one file,
and the precedence above is the single rule that resolves them — ring colour wins on the faces it
covers, region colour holds elsewhere. Without this sentence the two features would each claim the
same face and the split would be ambiguous; with it, there is one owner per face.

**Default:** when a face is claimed by neither a ring colour nor an explicit `color <region>`, its
body is the coaster region `base` — the same default [`coaster-colour-design.md`](coaster-colour-design.md)
§3 already ships (**CAL-PIN-01** governs the two-filament pinch floor at any resulting interface,
unchanged by this doc).

## 7. The AMS bound — bands are cheap, slots are not

Each printed body binds to one AMS slot at the slicer ([`coaster-colour-design.md`](coaster-colour-design.md)
§4). The useful number of coloured bands is therefore bounded by the number of filament slots the
printer offers, not by the number of rings the geometry has. This is why radial *bands* (a handful)
are the right granularity and per-*polygon* colour (potentially hundreds) is not — the ask's own
"equidistant" grouping is what keeps the colour count inside the slot budget.

The exact slot count is **not grounded in either repo** (the recon found no in-repo constant; the
X2D is dual-nozzle with per-unit AMS trays plus one external spool). So this doc states the bound
qualitatively and defers the number: the `bands` verb and the composer should **warn, not cap**,
when the distinct-colour count exceeds the slots the live printer reports via `bambu filament`,
and the number is confirmed against that output before any print — not hard-coded here. (Writing a
slot cap as a `**Default:**` with a guessed number would be a K4 violation; the honest record is
"verify against the device," and the print itself is owner-gated regardless.)

## 8. Status and scope

- **Grammar:** no new production. Reuse `fill where ring == N color <Name>` (shipped).
- **Kernel:** the §4 bridge (face ring index → region key in `--format parts`) and the §6
  precedence rule. One bikar PR.
- **CLI:** the §5 `bands` verb. May be the same PR or a follow-up; it is read-only and independent.
- **Composer/AMS:** no change to the palette-name → slot mapping; it already keys on palette name.
- **Out of scope:** ring colour into a bare (non-coaster) 3D solid (bikar ships none); an explicit
  radius grammar (option (c), rejected); any slot-count constant (§7).
- **Bets:** none new. §7's slot bound is a device fact to read, not a calibration to earn.
