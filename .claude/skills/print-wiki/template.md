---
title: <Phenomenon in plain words, e.g. "Floating regions" slicer warning>
symptom: <the exact words the operator sees — the warning text, error dialog, or visible defect>
kind: slicer-warning | mesh-flag | print-defect | filament-mapping | tolerance | machine
proof: print-record | slice-only | screenshot
first_seen: <YYYY-MM-DD>
---

# <Phenomenon in plain words>

> **Symptom (what you see):** <verbatim warning / error / defect the operator meets>

## What it means

<The mechanism, in plain terms. Carry the source's hedge — if the source says "may", write "may".
Do not harden a possibility into a certainty (K1).>

## Is it a concern?

**It depends on what the part is for.** State both sides explicitly:

- **Not a concern when …** <the case where you proceed — e.g. a decorative overhang; cite the proof>.
- **A concern when …** <the case where you must act — e.g. a functional/load-bearing feature>.

<Never a context-free verdict. If we have only observed one case, say so and label the other side an
unverified expectation, not a ruling (K2).>

## What to do

<The action, or the explicit "nothing — proceed." If the fix is a slicer setting, name it and say the
skill advises but does not change it.>

## Proof — our own prints

<Link the evidence this entry is grounded in:>

- <`docs/prints/<run>/…` record — the load-bearing proof once a real print exists (task #72)>, or
- <`<plate>.sliced.3mf.warnings.json` sidecar / screenshot — the honest `slice-only` proof until then>.

## See also

- <cross-links to related wiki entries, `[[…]]`-style by slug or relative link>
- <external reference (Bambu wiki, slicer docs) if one grounds a claim above>
