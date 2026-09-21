---
title: "Floating regions" slicer warning
symptom: Bambu Studio flags "floating regions" / unsupported overhang after slicing
kind: slicer-warning
proof: slice-only
first_seen: 2026-09-21
---

# "Floating regions" slicer warning

> **Symptom (what you see):** after slicing, Bambu Studio raises a warning that the plate has
> **floating regions** — areas of the model with no material beneath them and no support enabled.

## What it means

The slicer found geometry that starts mid-air: a downward-facing region whose first layer has nothing
under it. With supports off, those layers print onto air for their first pass. On a steep decorative
overhang this **may** show as a little droop or roughness on the underside; it does not mean the print
will fail. It is the slicer telling you *"you chose not to support this"*, not *"this cannot print."*

## Is it a concern?

**It depends on what the part is for.**

- **Not a concern when** the floating region is a **decorative overhang** you deliberately left
  supportless — the underside is not a functional surface and a little sag is acceptable. Every
  egg-grid plate we sliced (2×3 through 5×5) raised **exactly two** of these warnings from the egg's
  twist geometry, and each sliced cleanly and completely. This is the by-design case.
- **A concern when** the floating region is a **functional face** — a mating surface, a bearing seat,
  anything dimensionally critical — because the droop lands on a surface that has to be accurate. There,
  enable supports (or reorient so the face is not an overhang) rather than shipping the warning.

## What to do

- Decor part, deliberate overhang → **proceed**; the warning is informational.
- Functional face → enable supports or reorient. The `print-wiki` and `print-model` skills advise this;
  they do not change the setting for you.
- Note the honesty gate: `bambu print send` **blocks** on this warning by design (it cannot tell decor
  from function), while the Studio GUI shows it without blocking. See
  [print-send-warnings-gate](print-send-warnings-gate.md).

## Proof — our own prints

- `slice-only`: the four egg-grid plates (`egg-grid-2x3` … `egg-grid-5x5.sliced.3mf`) each raised two
  floating-regions warnings, recorded in their `*.sliced.3mf.warnings.json` sidecars and classified as
  expected in `.claude/gates/expected-slicer-warnings.json`.
- Upgrade to a print-record proof link once Plate 1 comes off the machine (task #72 / #63).

## See also

- [print-send-warnings-gate](print-send-warnings-gate.md) — why the CLI refuses to send on this warning
- Bambu Studio support/overhang documentation (external reference)
