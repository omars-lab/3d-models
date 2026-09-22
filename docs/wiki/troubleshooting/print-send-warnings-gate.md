---
title: "bambu print send" refuses to dispatch
symptom: bambu print send blocks with a warnings-gate error instead of sending the plate
kind: machine
proof: slice-only
first_seen: 2026-09-21
---

# `bambu print send` refuses to dispatch

> **Symptom (what you see):** `bambu print send <plate>` stops with a warnings-gate error — no sidecar,
> a stale sidecar, an unverifiable one, or an UNEXPECTED slicer warning — instead of dispatching.

## What it means

This is the **warnings honesty gate** (#52 / #62) working as designed, not a bug. `slice plate` writes a
`<output>.sliced.3mf.warnings.json` sidecar stamped with the source's `source_sha256`. Before any send,
`bambu print send` is **fail-closed**: it blocks if the sidecar is missing, stale (its stamp no longer
matches the plate), unverifiable, or lists any warning not present in
`.claude/gates/expected-slicer-warnings.json`. The gate runs **before** the owner gate, so a plate can
never be dispatched with unreviewed slicer warnings. The Studio GUI, by contrast, shows warnings without
blocking — so a plate the GUI will happily print, the CLI may refuse.

## Is it a concern?

**It is the gate doing its job — the question is which case you are in.**

- **Not a concern (expected)** when the block is on a **known by-design warning** already listed as
  expected — e.g. [floating-regions](floating-regions-warning.md) on a decor overhang. The fix is to
  confirm the warning is expected, not to bypass the gate.
- **A concern** when the block is on a **stale sidecar** (you edited the model after slicing — re-slice)
  or an **UNEXPECTED warning** (a real new slicer complaint you have not reviewed — read it, decide, and
  only then add it to the expected list with justification).

## What to do

- **Stale / missing sidecar** → re-run `bambu slice plate` so a fresh, stamped sidecar exists.
- **Expected by-design warning** → verify it is genuinely by-design, then ensure it is in
  `.claude/gates/expected-slicer-warnings.json`. Do not blanket-bypass.
- **New unexpected warning** → treat it as a real finding; understand it before allow-listing it.
- Never route around the gate to force a send. Robustness over ease: the gate exists so a warning is
  reviewed once, not re-met at the machine.

## Proof — our own prints

- `slice-only`: the egg-grid plates each carry a stamped sidecar with two expected floating-regions
  warnings; a plate sliced but not re-stamped after an edit is blocked as stale. Gate shipped in #52/#62.
- Upgrade to a print-record proof link once a plate is dispatched and recorded (task #72 / #63).

## See also

- [floating-regions-warning](floating-regions-warning.md) — the most common expected warning
- The `bambu` skill — day-to-day CLI usage of `slice plate` / `print send`
