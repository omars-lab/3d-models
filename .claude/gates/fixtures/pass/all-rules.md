# Fixture: a doc that satisfies D1, D2 and D3

Asserted PASS fixture for `docs_gate.py`. Every rule the gate enforces is
exercised here in its satisfied form. If this file starts reporting findings,
the gate has a false positive.

## D1 — relative links resolve

The taxonomy this gate is built from:
[grounding-defect-taxonomy.md](../../../../docs/grounding-defect-taxonomy.md).
An absolute link is not checked: [Anthropic](https://www.anthropic.com).
A fragment-only link is not checked: [see below](#d3--defaults-carry-provenance).

A marker shown as code is a mention, not a use: writing `**Validator:**` or
`**Default:**` inline — as this file and `CLAUDE.md` both must, to document the
discipline — declares nothing and is not checked. Same for a link written as
code: `[dead](./no-such-file.md)`.

A dead link inside a fenced block is not checked, because it is an example,
not a reference:

```markdown
[this does not resolve](./no-such-file.md)
```

## D2 — validators ship both examples

**Validator:** `gap >= 3 * printerTolerance` for every adjacent tile pair.

- PASS: tolerance 0.2 mm, gap 1.2 mm → 1.2 ≥ 0.6, accepted.
- FAIL: tolerance 0.5 mm, gap 1.2 mm → 1.2 < 1.5, rejected with the pair id.

**Validator:** `studsEngaged >= 2` for any piece that must not rotate.

- FAIL: a 1×1 footprint engages one stud → rejected.
- PASS: a 1×2 footprint engages two → accepted.

## D3 — defaults carry provenance

**Default:** `minFeatureMm = 1.2` — [Hubs FDM design
rules](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/).

**Default:** `detentRibMm = 0.30` — no source can settle this; it is bet
CAL-DET-01 and ships from the coupon reading.
