---
title: Non-manifold edges on mesh import
symptom: Slicer / mesh-repair dialog reports "N non-manifold edges"
kind: mesh-flag
proof: screenshot
first_seen: 2026-09-21
---

# Non-manifold edges on mesh import

> **Symptom (what you see):** on import, the slicer's mesh-repair dialog reports some number of
> **non-manifold edges** (e.g. "79 non-manifold edges") alongside the triangle count.

## What it means

A manifold ("watertight") mesh is one where every edge is shared by exactly two faces — a clean solid
with a well-defined inside and outside. A **non-manifold edge** is shared by the wrong number of faces
(one, or three-plus): a crack, a duplicated face, or a T-junction in the mesh. The slicer flags them
because in the worst case they confuse the inside/outside test. In practice the slicer's auto-repair
closes small ones before slicing, and a **tiny fraction** of non-manifold edges on an otherwise sound
mesh is cosmetic — it does not mean the STL is unprintable.

## Is it a concern?

**It depends on the fraction and on what the part is for.**

- **Not a concern when** the count is a **negligible fraction** of the mesh and the part is decorative.
  The Mini Twisted Dragon Egg imported with **79 non-manifold edges out of 238,496 triangles (~0.03%)**;
  it auto-repaired and sliced cleanly and completely. For a decor print this is noise.
- **A concern when** the fraction is large, the errors cluster on a **functional or dimensionally
  critical** feature, or the slice/preview shows an actual hole, spike, or missing region after repair —
  then the mesh needs fixing at the source (re-export, or a repair pass in the modeller) before printing.

## What to do

- Small fraction, decor part, clean preview → **proceed**; let the slicer auto-repair.
- Large fraction or visible defect after repair → fix the mesh at the source; do not print a mesh whose
  inside/outside is genuinely ambiguous on a feature that matters.
- Always eyeball the sliced preview of the affected region — a repair that "succeeded" can still have
  bridged a hole in the wrong place.

## Proof — our own prints

- `screenshot`: the Bambu Studio mesh-repair dialog for the Mini Twisted Dragon Egg — 79 non-manifold
  edges / 238,496 triangles / 29.79 × 29.73 × 35.79 mm / 13,944 mm³ — sliced without incident.
- Upgrade to a print-record proof link once the egg plate prints (task #72 / #63).

## See also

- bikar's mesh gate (`--check` watertight/euler checks) — the upstream guard that keeps our *authored*
  geometry manifold before it ever reaches the slicer
