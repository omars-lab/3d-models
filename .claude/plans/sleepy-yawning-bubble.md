# Calibrate — grounding the claims only a printer can settle

> Supersedes the Lego Lab R0 plan previously in this file; that plan is complete and
> preserved in git at `4c3b900`.

## Context

`ground-design-doc` settles what *sources* can settle. Seven design docs have now been
through it, and the residue is consistent: every audit ends with verdicts that say, in
effect, *no literature can decide this — measure it*. Today that trail just stops. The
consequences are visible in shipped code:

```
kernel3d/fit-profile.ts:71   "literature-shaped placeholders until the fit coupon
                              measures this printer"
kernel3d/fit-profile.ts:105  warpMm — "undefined until the clip coupon measures it"
kernel3d/print-gate.ts:44    MIN_BED_CONTACT_MM2 — "deliberate placeholders pending
                              the prototype catalog's P2 Q5 measurement"
```

Those comments are honest and self-aware, and they are also the whole mechanism. Nothing
makes them enumerable, nothing stops them ageing into numbers that merely *look* earned,
and nothing notices that the same physical quantity is separately unresolved in two docs
at once — `FIT_GAP_MM` is open as c2 Appendix B.3 *and* as piece-composition B.2, with no
cross-link.

There is duplicated effort in the other direction too. W-F1, LG-F1, LG-F2 and P1 each
independently plan to measure some of warp, wall floor, and bore fit. But those are not
properties of a clip, a brick, or an orb — they are properties of *(printer, material,
nozzle, slicer profile)*. One characterization plate settles the shared substrate; the
design coupons then test only what is genuinely design-specific.

**Two findings from designing the mechanism widened the scope, in the order they must be
built:**

1. **Parsing discipline is missing from the tenets, and three sites fail open.** The
   first draft of this plan proposed `@calibration CAL-…` comment markers found by grep —
   the exact mechanism `scripts/check-decision-coherence.sh` was written to replace
   (*"the discipline lived only in skill prose agents skip under pressure"*; its header
   says *"NO regex. NO markdown-body scan."*). Auditing outward from that found five
   regex sites, three of which silently skip input they can't match — including one
   inside a **commit-blocking** hook. That is ≥3 witnesses of one defect class, which is
   Tenet 28's threshold for *stop characterizing, file the fix*.
2. **A calibrated number needs structured provenance, not a naming convention.** A value
   is valid only for a specific *(machine, material, nozzle, profile)*. A comment or a
   `PROVISIONAL_` prefix can carry doubt; neither can carry that record. So provenance
   rides on the value as a type, and the registry becomes *derived from code* rather than
   maintained beside it.

**Intended outcome:** the tenets name both disciplines with their witnesses; the five
parsing sites are fixed; and a `calibrate` skill + a print-ready machine card close the
ceremony's missing half — with a gate that lets the set of unearned numbers only shrink.

### Decisions locked (Omar, 2026-07-29)

1. **New `calibrate` skill**, sibling to `ground-design-doc`. `prototype` stays the
   per-design print backlog; the three hand off to each other.
2. **Provenance rides on the value, as a type** — not a comment. A `Calibrated<T>` wrapper
   carries the bet ID and either `'provisional'` or a full measurement record.
3. **CI + pre-commit gate with an append-blocked baseline** — the set of unearned numbers
   may only shrink.
4. **Machine card only** for the first print — the shared substrate, not design coupons.
5. **Build `Machine-Card.bkr` now**, blind to the eventual machine.
6. **Fix all five regex findings first**, before calibrate.
7. **Add PyYAML and use `safe_load`** in `validate.py` — no hand-rolled reader.
8. **Two new tenets + one conventions bullet** (Phase T below).

---

## Phase T — tenets (first, so Phase R's commits cite them)

All edits in `bikar/CLAUDE.md`, the canonical tenets home. Each tenet follows the house
shape already used by 25/26/28: **rule → stop rule → companion tenets → *failure mode this
prevents* (dated, with real witnesses) → *anti-pattern this names*.**

**Tenet 29 — Parse structurally; never fail open.** Read structured formats with a
structured reader (`yaml.safe_load`, `yq --front-matter=extract`, the lexer's own tokens);
a regex is legitimate for **matching tokens inside prose** and illegitimate as the
**authoritative reader of structure**. The load-bearing half is *fail closed*: a line the
reader cannot interpret is an **error**, never a skip — most of all inside a gate, where
silently skipping input converts a blocking check into a decoration. Companion to Tenet 11
(native primitives over approximations — same rule, text instead of geometry), 15/16 (the
typing layer), and 23 (don't re-derive what the producer knows). Witnesses:
`validate.py:60-95`, `param-rewrite.ts:32`, `evaluator.ts:5777`.

**Tenet 30 — A physical constant is not earned until it records its provenance.** A number
that a printer decides is not shipped as a bare literal, however plausible its literature
value: it carries its bet ID and either an explicit `provisional` marker or a measurement
record naming machine, material, nozzle, profile, and date. Stop rule before merging a
constant with physical units: name the coupon that will settle it, or mark it provisional —
"it's the standard value" is not a measurement. Companion to Tenet 9 (no magic numbers —
the `.bkr` instance of the same rule) and Tenet 25 (no ship on a green metric alone).
Tenet 9 gains a one-line cross-reference so its reader lands here.

**Conventions bullet (not a tenet) — dependency caution scales with blast radius and
audience.** Under `## Conventions`, beside "Package manager: npm with workspaces". The
repo already practises this and it needs recording, not elevating: `packages/core` is a
published library and carries **zero** runtime dependencies (earcut vendored);
`packages/knobs` takes `lz-string` without ceremony; `scripts/` demands `yq`+`jq`;
`3d-models/Makefile:154` check-and-instructs Pillow. The anti-pattern: hand-rolling a
parser for a solved format to avoid a dependency in dev-only tooling — which is Tenet 29's
failure wearing a virtue costume.

---

## Phase R — parsing remediation (five findings)

Ordered by blast radius. #1 is the only one in a commit-blocking path.

**R1 — `3d-models/.claude/skills/maintain-use-cases/validate.py:60-95`.** Replace the
hand-rolled frontmatter scan with `yaml.safe_load`. Today `re.match(r"^\s+([\w.-]+):\s*(\S+)\s*$")`
silently skips quoted values, values containing spaces, and trailing comments, so a
**malformed `as_of` pin is indistinguishable from a missing one** — in a hook that blocks
commits. Also replace the ```` ```mermaid ```` body scan with a structured fence walk.
Leave `POINTER_RE` and `UC_RE` exactly as they are: matching tokens in prose is regex's
actual job, and they are the in-file example of Tenet 29's legitimate side.

Declare the dependency the way this repo already does — `.githooks/pre-commit.d/20-use-cases`
currently guards only for `python3`; extend that guard to `import yaml` with the
`Makefile:154` Pillow message shape (`"PyYAML required: pip install pyyaml"`). No
`requirements.txt` exists and this plan does not add one for a single dev dependency.

**R2 — `bikar/packages/knobs/src/param-rewrite.ts:32,39,48`.** A second partial
implementation of the `.bkr` `param` grammar drives the Lab's write-values-into-code, the
baked `.bkr` download, and the studio Dials tab. Three concrete defects: the tail scan
`/\s(?:range|advanced)\b/` **omits `step`**; `isExpression: !/^-?\d+(\.\d+)?$/` misjudges
`.5`, `1e3` and `+3` as expressions; and the line regex only matches a `param` whose
header form it anticipates. Fix by lexing and rewriting the **token span**, not the line:
`tokens.ts:190-195` gives `{ type, value, line, column }`, so `column + value.length`
yields an end offset. The span approach preserves the header comment's real requirement —
*"everything after the default expression is preserved byte-for-byte"* — which an
AST round-trip would violate. Update that header comment: it currently defends the line
scan, and after this it would be arguing for the code it replaced.

**R3 — `bikar/packages/core/src/dsl/evaluator.ts:5777-5792`.** `addressDepth()` counts dots
with `(prefix.match(/\./g) || []).length` to recover a depth that the code that **built**
the key already knew — Tenet 23's failure mode exactly. Carry the depth structurally
alongside the composed ID rather than re-deriving it from the string.

**R4 — `svg-renderer.ts:312-326` vs `gt-emitter.ts:1220-1234`.** The same internal-tag
predicate is copy-pasted into the renderer **and** into the ground-truth emitter that
validates the renderer, each commenting "Mirrors <the other>". They have already drifted:
svg-renderer tests `GIRIH_OUTLINE_TAG`, `GIRIH_DECORATION_TAG` and the
`GIRIH_REGION_TAG_PREFIX` constant; gt-emitter hardcodes `'_girih_region:'` and lacks both
tag equality checks. Extract one exported predicate into
`packages/core/src/kernel/girih-tiles.ts`, which already owns all three constants and is
already imported by the renderer. Resolve the drift deliberately — the emitter is the
laxer copy, so adopting the renderer's version is the behaviour change to test for.

**R5 — `bikar/packages/core/src/render/animation-compiler.ts:74`.** `[^"]*` inside a
constructed attribute-selector regex breaks on an escaped quote. Lowest severity — the
generator owns its own input — so fix narrowly and note the constraint rather than
rebuilding a CSS selector parser.

**Explicitly clean, do not touch:** `gen-decision-ledger.sh` / `check-decision-coherence.sh`
(structured `yq` throughout; one cosmetic `sed 's/\.md$//'`), and `parser.ts:111,124`
single-char `/\d/` tests, which are lexer character classes.

---

## Phase C — calibrate

### What the DSL can already express (verified, no engine work needed)

Checked against `bikar/docs/language-reference.md` §"Piece Declarations (3D)" and the
existing `patterns/Coupons/Fit-Coupon.bkr`. Every coupon below is authorable today:

| Need | Mechanism | Note |
|---|---|---|
| Bore ⌀ sweep, fit ladder | `extrude` + `hole … band d …` + `rod` | Fit-Coupon already does this at ⌀3 |
| Wall-thickness ladder | `tube inner <d> outer <d+2t> height <h>` | wall = (outer − inner)/2; the CLI already reports tube wall as the declared min feature |
| Bridge span ladder | blind bore: `band d <span> from 0 to <z1>` with `z1 < depth` | leaves a ceiling that must bridge the bore ⌀ — span is the diameter |
| Overhang fan | `revolve profile <region>` with a stepped-slope outer edge | a true cone is rejected (axis-touching, C1 ring solids only); a truncated ring with staircase slopes is legal |
| Warp | `extrude` of a large thin plate | reuse Fit-Coupon's guide-circle-quartered rectangle idiom — the blueprint has no rectangle primitive |
| Bed contact | `rod d <small> height <tall>` | one line per tower |

Two consequences, stated before anything is authored:

- **The wall ladder deliberately fails `--check`.** Sub-floor rungs (0.4–1.0 mm) sit below
  `DEFAULT_MIN_FEATURE_MM = 1.2`, so `meshGate` reports FAIL by design — the W-series
  sub-floor rule already documented in `catalog.md`. Those rungs render without `--check`.
  No `--min-feature` override flag is added.
- **Rung identity is positional, not embossed.** bikar has no text emit, so the BOSL2
  trick c2's own survey praises (the label *is* the answer) is unavailable. Mitigation:
  one piece per rung rendered via `--piece`, so identity lives in the filename, plus
  monotone size ordering that is self-evident in the hand. The protocol states this rather
  than pretending otherwise.

### C1 — the `calibrate` skill

`.claude/skills/calibrate/SKILL.md`, in the house voice of `ground-design-doc`.

**Workflows (the steps that always run):**

1. **Harvest** — sweep three surfaces: design-doc Appendix B + Open Questions,
   `catalog.md` entries, and the derived bet registry (C2). Classify every unsettled claim
   as **EMPIRICAL** (a measurement decides it) or **ARGUED** (sources or reasoning decide
   it — that belongs to `ground-design-doc`; misfiling one here is the main failure mode).
2. **Cluster** — group bets by *the single measurement that settles them*, not by the doc
   they came from. Duplicates across docs collapse to one ID. This is what lets one plate
   close entries in five documents.
3. **Design the coupon** — one variable per coupon (c2 survey §4 records BOSL2 + Bambu as
   settled prior art); a ladder bracketing the unknown generously; identity readable from
   geometry or filename; and an explicit statement of the print orientation the
   measurement assumes, because a bridge or overhang means nothing without it.
4. **Emit the print pack** — the `.bkr`, the exact CLI line per rung, the measurement
   protocol (instrument, where on the part, sample count), and a blank data sheet.
5. **Measure** — readings come only from the physical object. Inherits `prototype`'s rule:
   never from a slicer preview, never from reasoning. A failed print is a result.
6. **Propagate** — the earned number replaces the constant's value *and* its status flips
   from `provisional` to a full measurement record; the doc's Appendix B entry closes with
   the measured value; the catalog entry flips; commit hashes cited in both repos.

**Rules:** a bet with no coupon is a backlog item, not a finding. A number without a
recorded machine/material/nozzle is anecdote, not calibration (Tenet 30). Never delete a
lost bet — a measurement that refutes the design is a success outcome, as in
`ground-design-doc`.

### C2 — provenance as a type, and a registry derived from it

New in `bikar/packages/core/src/kernel3d/calibration.ts`:

```ts
export type CalBetId = 'CAL-FIT-01' | 'CAL-HOL-01' | /* … closed union … */;

export type Provenance =
  | { readonly status: 'provisional'; readonly basis: string }
  | { readonly status: 'measured'; readonly machine: string; readonly material: string;
      readonly nozzleMm: number; readonly profile: string; readonly date: string;
      readonly coupon: string };

export interface Calibrated<T> { readonly bet: CalBetId; readonly value: T;
                                 readonly provenance: Provenance }
```

A closed `CalBetId` union means a typo is a **compile error**, not a missing grep hit —
this is the whole reason the mechanism moved from comments to types, and it satisfies
Tenets 15/16 (model the variant; don't launder it through strings).

**Migration is the real cost and the plan states it plainly.** Consumer counts:
`FIT_GAP_MM` 18, `PRINTER_PROFILES` 12, `FIT_TOL_MM` 14, `DEFAULT_MIN_FEATURE_MM` 6,
`MIN_BED_CONTACT_MM2` 3 — all in-monorepo, nothing published. Approach: wrap the constant,
export a `.value` accessor beside it, and migrate call sites mechanically. One site needs
care — `dsl/parser.ts:1464` does `fitTok.value in FIT_GAP_MM`, which breaks under a wrapper
unless it reads the inner record. **No constant's numeric value changes in this phase**;
golden STLs must not move, which is the regression test.

`.claude/skills/calibrate/bets.md` is then **generated** from the source of truth by
`scripts/gen-calibration-registry.ts`, following `gen-decision-ledger.sh`'s precedent — a
derived artifact, checked in so it is reviewable, regenerated rather than edited.

| ID | Quantity | Consumers | Coupon |
|---|---|---|---|
| `CAL-FIT-01` | `FIT_GAP_MM` press/snug/sliding/free | c2 B.3, piece-comp B.2, `fit-profile.ts`, W-F1 Q1 | MC-1 |
| `CAL-HOL-01` | `holeCompMm` 0.20/0.25 | c2 B.6, `fit-profile.ts` | MC-1 |
| `CAL-FEA-01` | `DEFAULT_MIN_FEATURE_MM` 1.2 | `mesh-gate.ts`, lego B.5, P1 | MC-2 |
| `CAL-BRG-01` | bridge span ≤10 mm | w2 B.3, lego §3.6 `engage` | MC-3 |
| `CAL-OVH-01` | overhang threshold (F5) | print-val B.2, `print-gate.ts` | MC-4 |
| `CAL-WRP-01` | `warpMm` (currently `undefined`) | `fit-profile.ts`, w2 B.5, W-F1 Q2 | MC-5 |
| `CAL-BED-01` | `MIN_BED_CONTACT_MM2` 25 / ratio 0.01 | `print-gate.ts` | MC-6 |
| `CAL-RIB-01` | clutch rib `ribMm` 0.10 | lego B.8 | LG-F1 *(not on the card)* |
| `CAL-DET-01` | detent band 0.3–0.5 mm | w2 B.6 | W-C1 *(not on the card)* |
| `CAL-STR-01` | Z-layer strength ratio | c2 B.5 | none — needs a load rig, registered OPEN |

The last three are deliberately off the machine card: two are design-specific, and
`CAL-STR-01` has no coupon at all — worth recording as a known gap rather than leaving it
invisible.

### C3 — the gate

`bikar/scripts/check-calibration.ts`, modelled on `check-decision-coherence.sh`: every
`Calibrated<T>` with `status: 'provisional'` must appear in `.calibration-baseline.json`,
and the baseline is **append-blocked** — a new provisional value not in the baseline is
always an error; the file may only shrink. Wired into pre-commit and into `npm run ci`.

Note for the wiring step: `check:decisions` is **not** currently in bikar's `ci` script
(`"ci": "lint && format:check && build && test && spelling && import-graph"`). Add
`check:calibration` to `ci` — and flag the pre-existing `check:decisions` omission rather
than silently fixing it, since that is someone's earlier decision to confirm or reverse.

### C4 — the machine card

`bikar/patterns/Coupons/Machine-Card.bkr` (+ `docs/calibration-design.md` here for the
geometry rationale and the protocol).

| Coupon | Geometry | Rungs | Settles |
|---|---|---|---|
| **MC-1** bore & fit plate | extend the existing Fit-Coupon | ⌀ sweep 3/4/5/6/8/10 + the four-class fit ladder + gauge pins | `CAL-FIT-01`, `CAL-HOL-01` |
| **MC-2** wall ladder | `tube` ×7 | wall 0.4/0.6/0.8/1.0/1.2/1.6/2.0 | `CAL-FEA-01` |
| **MC-3** bridge plate | blind bores under a 2 mm ceiling | span 4/6/8/10/12/16 | `CAL-BRG-01` |
| **MC-4** overhang fan | one `revolve`, stepped outer slope | 20/30/40/45/50/60° | `CAL-OVH-01` |
| **MC-5** warp plate | thin `extrude`, large footprint | one part, 4 corners measured | `CAL-WRP-01` |
| **MC-6** bed-contact towers | `rod` ×4 | ⌀3/5/8/12 × 40 mm tall | `CAL-BED-01` |

MC-1 extends `Fit-Coupon.bkr` rather than replacing it — that file is already referenced by
catalog W-F1 and its ⌀3 ladder is correct as far as it goes; the card adds the ⌀ sweep that
`holeCompMm` actually needs.

**Authored blind, and the doc says so.** With no machine yet, the rung *ranges* are
brackets around an unknown, not predictions. `docs/calibration-design.md` records that they
are unvalidated and that the first print may show a ladder needs re-centring — itself a
result worth logging.

### C5 — the handoffs ("tasks we always do")

- **`ground-design-doc/SKILL.md`** gains a step 5: after applying an audit, every verdict
  that is UNGROUNDED-and-empirical is registered as a CAL bet, and the doc's Appendix B
  entry cites it. This closes the hole where an audit says "no evidence either way" and
  the trail ends.
- **`prototype/SKILL.md`**: catalog entries cite the CAL IDs they settle, and the existing
  **Propagate** workflow — which today stops at `.bkr` defaults, the mesh gate, and the
  design doc — gains "close the CAL bet, flip its provenance to `measured`, close its
  Appendix B entry."
- **`catalog.md`** gains an **MC series** for the six coupons, in the existing entry
  schema, ahead of W-F1/LG-F1 in the learning ladder (they consume its numbers). W-F1's Q2
  (warp) and LG-F1's tube-wall caliper question get re-pointed at `CAL-WRP-01` /
  `CAL-FEA-01` rather than re-measuring them.
- **The seven design docs** get `[CAL-…]` tags on the ten empirical Appendix B entries.
  Text otherwise untouched.
- **`calibrate/SKILL.md`** cites bikar Tenet 30 — 3d-models has no `CLAUDE.md` and this
  plan does not create one.

---

## Critical files

**New (3d-models):** `.claude/skills/calibrate/{SKILL.md,bets.md,protocol.md}`,
`docs/calibration-design.md`.

**Modified (3d-models):** `.claude/skills/maintain-use-cases/validate.py` (R1),
`.githooks/pre-commit.d/20-use-cases` (R1 guard), `.claude/skills/ground-design-doc/SKILL.md`,
`.claude/skills/prototype/{SKILL.md,catalog.md}`, and the empirical Appendix B entries in
`docs/{c2-assembly,piece-composition,w2-connector,print-validation,tile-wall,lego-lab}-design.md`.

**New (bikar):** `CLAUDE.md` tenets 29/30 + conventions bullet (Phase T),
`packages/core/src/kernel3d/calibration.ts`, `scripts/check-calibration.ts`,
`scripts/gen-calibration-registry.ts`, `.calibration-baseline.json`,
`patterns/Coupons/Machine-Card.bkr`.

**Modified (bikar):** `packages/knobs/src/param-rewrite.ts` (R2),
`packages/core/src/dsl/evaluator.ts` (R3), `packages/core/src/kernel/girih-tiles.ts` +
`render/{svg-renderer,gt-emitter}.ts` (R4), `render/animation-compiler.ts` (R5),
`packages/core/src/kernel3d/{fit-profile,mesh-gate,print-gate}.ts` + their ~53 call sites
(C2 — wrapper only, **no value changes**), `package.json` (`ci` script).

---

## Verification

**Phase T:** each new tenet names real witnesses at `file:line` that still exist.

**Phase R:**
- R1: `python3 -m yaml` reads the real frontmatter; a **deliberately malformed** `as_of`
  line now fails the hook where it previously passed silently — that inversion is the
  test. `make validate-use-cases` green on the real tree.
- R2: round-trip a `param` with `step`, with `.5` / `1e3` / `+3` defaults, and with a
  trailing comment — every non-target byte identical (the header comment's own contract).
- R3–R5: `npm run ci` green; R4 must show the emitter's behaviour change explicitly
  (adopting the renderer's stricter predicate) rather than absorbing it silently.
- Every fix gets a vitest that encodes the witness before it ships (Tenet 18).

**Phase C:**
- `npx tsc` proves the registry complete: an unregistered `CalBetId` is a compile error,
  and `gen-calibration-registry.ts` output matches the checked-in `bets.md` (regenerate
  and diff, like the decision ledger).
- `check-calibration.ts` fails on a newly-added provisional value not in the baseline, and
  passes on the same value once baselined — both directions tested.
- Golden STLs unchanged: C2 wraps values, it does not alter them.
- `Machine-Card.bkr` renders every rung; `--check` PASS on MC-1/3/4/5/6; MC-2's sub-floor
  rungs render without `--check` and are *expected* FAIL, recorded as such, not a defect.
  Watertight (`euler` consistent) on all rungs — the real regression test, since a bad
  coupon fails silently in the mesh.
- Renders eyeballed before the `.bkr` ships (Tenet 25).
- Skill-file edits trip the pointer hook on `catalog.md`; that is UC8, not a new use case,
  so `USE_CASES_OK=1` is the correct override (precedent `c7ee0e5`).
- **Not verifiable now, by construction:** every number the card produces. Nothing here
  may mark a CAL bet settled — that needs the printer, and the skill's own rules forbid
  closing one from a render.

## Out of scope

Mirroring Tenet 29 into qiyas/sacred-patterns (applies there — Python detector — but those
repos are otherwise untouched here; raise separately). Creating a 3d-models `CLAUDE.md`.
Adding `check:decisions` to bikar's `ci` (pre-existing omission — flag, don't fix).
A `requirements.txt` for one dev dependency. A `--min-feature` override flag. Text/emboss
capability. Any change to a constant's *value*. Design-specific coupons (LG-F1, W-C1 stay
as they are, re-pointed only). Printing the card — there is no machine.
