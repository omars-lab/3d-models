---
title: "Cannot select PLA…PLA" in the AMS dialog
symptom: The filament dialog refuses to map a PLA spool to a PLA slot ("Cannot select…")
kind: filament-mapping
proof: screenshot
first_seen: 2026-09-21
---

# "Cannot select PLA…PLA" in the AMS dialog

> **Symptom (what you see):** in the AMS / filament dialog you try to assign a PLA spool to a slot and
> the UI refuses — a message like "Cannot select PLA … PLA" — even though both sides *are* PLA.

## What it means

The refusal is about the filament **preset (profile)**, not the material **type**. A Bambu plate is
sliced against a specific filament profile (e.g. *Bambu PLA Basic @BBL X2D 0.4 nozzle*). If the spool in
the slot is set to a **different preset** — for instance *Generic PLA* on the External spool — the
slicer will not silently substitute one PLA profile for another, because temperatures, flow, and cooling
differ between profiles. Same material family, different calibrated profile → the dialog blocks the map.

The related "why is this slot the primary?" question is separate and benign: a **single-filament** plate
defaults to the **lowest AMS slot** (A1). That slot being "primary" is just the default assignment for a
one-colour job, not a special property of the spool.

## Is it a concern?

**Yes — resolve it before printing, but it is a settings fix, not a hardware fault.**

- **A concern always** in the sense that the print will not map/start until the presets agree — but it
  is trivially fixable and protects you from printing PLA at the wrong profile's temps.
- **Not a hardware or material problem** — nothing is wrong with the spool or the machine; the two sides
  just name different profiles.

## What to do

- Set the slot's filament to the **same preset the plate was sliced against** (the X2D trio uses
  *Bambu PLA Basic @BBL X2D 0.4 nozzle*), **or** re-slice the plate against the profile the spool
  actually is. Make both sides name the same profile.
- Do **not** force a generic profile onto a Bambu-calibrated plate to dodge the dialog — that is exactly
  the temp/flow mismatch the block exists to prevent.
- Entering filament profiles is a settings choice the operator makes in Studio; the skills advise which
  profile, they do not change it.

## Proof — our own prints

- `screenshot`: the AMS Pro filament dialog showing the External-spool preset mismatch on a
  single-filament egg plate (slot A1 shown as primary).
- Upgrade to a print-record proof link once a plate prints against the confirmed X2D trio (task #72).

## See also

- The confirmed X2D slice profile (machine / process / filament trio) recorded in `docs/prints/`
- [print-send-warnings-gate](print-send-warnings-gate.md) — the other pre-dispatch check
