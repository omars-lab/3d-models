# The CLI *does* surface Studio's slicing warnings — at `--debug 2`

*Issue slug: `slicer-warnings-cli-visibility-pivot`. Written 2026-09-17, during #52
(the pre-dispatch warnings gate).*

## What the gate needs

The whole point of #52 is: **never dispatch a plate BambuStudio would have warned about.**
The GUI shows a per-object advisory before you print — *"It seems object … has floating
regions. Please re-orient the object or enable support generation."* A dispatch gate that
can't see that advisory can only guess.

## What the prior session concluded (and it was wrong)

The earlier investigation ran the headless `BambuStudio --slice` CLI at its default log
level, saw **no** per-object slicing advisory in stdout/stderr, and concluded the advisory
was **GUI-only — invisible to the CLI**. That conclusion pushed the design toward a
*curated blind manifest*: a human-maintained list of "coupons we know warn", checked without
ever reading Studio's own words, because we believed Studio never said them on the CLI.

That is exactly the failure the repo warns against — gating on a rule *before measuring it*.
A blind manifest is a second source of truth that silently drifts from the slicer.

## What the evidence actually showed

Re-run with the log level raised — `BambuStudio --debug 2 --slice …` (2 = warning) — and the
CLI emits the **same** advisory the GUI shows, as a structured line:

```
[warning] plate 1: found NON_CRITICAL slicing warnings: It seems object MC2Wall04.stl has
          floating regions. Please re-orient the object or enable support generation.
```

So the CLI was never blind — it was *quiet*. `--debug` changes only what is reported, not
what is sliced. The gate can therefore parse **BambuStudio's own warning lines** rather than
maintain a blind list. This reverses the prior conclusion.

Severity is binary and grounded in the binary's own format strings — critical
(`plate %1%: found slicing warnings: %2%, no_check=%3%`, carrying a trailing `, no_check=`)
vs. the `NON_CRITICAL` advisory form. Nothing else in the `[warning]` stream counts: the
version banner, `no filament colors found in projects`, and (on a re-slice of an already-
sliced .3mf) `can not find system preset file` are boilerplate, not slicing warnings; the
parser matches only the `found … slicing warnings:` shape.

## The measured boundary (also corrects an assumption)

The prior notes assumed the sub-floor wall rungs 04/06/08/10 would *all* raise the floating-
regions advisory. Measured 2026-09-17 (X2D 0.4 nozzle / 0.20mm Standard @BBL X2D / PLA
Basic): of the MC-2 rungs 04/06/08/10/12/16/20, **only MC2Wall04 (0.4 mm)** raises it; 0.6 mm
and up slice clean. The full assembled Plate 1 (23 objects) emits **exactly one** slicing
warning — MC2Wall04 — and it is by design (below `DEFAULT_MIN_FEATURE_MM = 1.2`, `CAL-FEA-01`;
support/re-orient must **not** be added or the measurement is defeated). The whitelist ships
one rule, not four dead ones. (Feeds the doc correction tracked as #56.)

## What replaced the blind manifest

`tools/bambu/src/backends/warnings.ts` parses the `--debug 2` output at per-object
granularity, and classifies each warning against
`.claude/gates/expected-slicer-warnings.json` — a whitelist of *understood, by-design*
warnings (grounded, each citing what was measured and the CAL bet it belongs to). Anything
not covered is **unexpected** and blocks. The manifest is a whitelist of exceptions to
Studio's own verdict, not a replacement for it. Fail-closed throughout: an empty/absent/
malformed manifest classifies **everything** as unexpected.

Warnings live only transiently in slice stdout — they are **not** in the .3mf archive. So
`bambu slice` writes a sidecar `<3mf>.warnings.json` beside the artifact (tool, sliced_at,
studio_version, the captured warnings). Downstream gates read the sidecar; a **missing**
sidecar is fail-closed — `bambu print send` blocks (exit 2) unless `--allow-unverified`.

- **`bambu slice plate`** now slices at `--debug 2`, captures + classifies, writes the
  sidecar, and exits non-zero on any unexpected warning.
- **`bambu print send`** runs the gate *before* the owner gate: clean/expected → proceed;
  unexpected or no-sidecar → block (exit 2); `--allow-unverified` overrides with a ⚠.
- **`bambu validate sliced`** reads the sidecar and reports `warnings : N captured — X
  expected, Y unexpected`, failing on any unexpected.

## Verified (live, 2026-09-17)

Sliced `MC2Wall04.stl` at `--debug 2` with the X2D presets:

- The advisory is captured into `MC2Wall04.sliced.3mf.warnings.json` (1 warning, non_critical,
  object `MC2Wall04.stl`).
- `bambu validate sliced` → `warnings : 1 captured — 1 expected, 0 unexpected`.
- `bambu print send --dry-run` → `✓ warnings gate: 1 expected-by-design warning(s), 0
  unexpected.`
- A plate with the sidecar removed → `✗ warnings gate: no slicer-warnings capture …`,
  process exit **2** (dispatch blocked); `--allow-unverified` proceeds with a ⚠.

Unit coverage (`warnings.test.ts`, 11 tests): parses the real captured line, ignores the
boilerplate, trims `no_check`, splits multi-object lines; clears MC2Wall04 as expected,
**blocks** an unwhitelisted `StarOrb.stl` floating-regions warning (the load-bearing case),
blocks a *critical* warning even on the whitelisted object, and fails closed on an empty
manifest.
