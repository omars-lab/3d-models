# Fixture: a doc that satisfies D1, D2 and D3

Asserted PASS fixture for `docs_gate.py`. Every rule the gate enforces is
exercised here in its satisfied form. If this file starts reporting findings,
the gate has a false positive.

## D1 — relative links resolve

The taxonomy this gate is built from:
[grounding-defect-taxonomy.md](../../../../docs/guides/grounding-defect-taxonomy.md).
An absolute link is not checked: [Anthropic](https://www.anthropic.com).
A heading link resolves by GitHub's slug, where the dash in a heading leaves two
hyphens: [see below](#d3--defaults-carry-provenance). It also resolves by the
heading text, the form Obsidian writes: [D2](#D2%20—%20validators%20ship%20both%20examples).
Into another file too: [the taxonomy's K9](../../../../docs/guides/grounding-defect-taxonomy.md#k9--misdirected-pointer).
And onto a block id review-md wrote: [this line](#^fixture-block). ^fixture-block
An obsidian link lands through the vault mapping:
[CS-1, minimal](obsidian://open?vault=docs&file=catalog%2Fpatterns%2Fsimple-20-step-six-fold-star-rosette-cs-1.md%23minimal),
and a review-md one too: <obsidian://review-md-open?vault=docs&file=catalog%2Fpatterns%2Fsimple-20-step-six-fold-star-rosette-cs-1.md>.

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

## D4 — a withdrawn number is named, not asserted

A doc may still discuss a number an audit withdrew; it may not restate it as
fact. Saying so in the same block is what makes it a discussion:

- **Retention**: v1 argued from an FDM tolerance of ±0.1–0.2 mm. That figure is
  withdrawn — no printer vendor publishes an accuracy number at all.

And in a plain paragraph, the same way: the ±0.1–0.2 mm figure is uncited by
construction, so the argument was rebuilt from measured repeatability instead.
