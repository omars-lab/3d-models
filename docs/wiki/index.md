# 3D-printing wiki — index

An LLM-maintained troubleshooting reference for printing on the Bambu X2D, built on the Karpathy
LLM-wiki pattern (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and maintained by
the [`print-wiki`](../../.claude/skills/print-wiki/SKILL.md) skill. Every entry answers three questions —
*what it means, whether it is a concern for the part in front of you, and what to do* — grounded in our
own slices and prints as proof.

**How to use this:** hit a symptom (a slicer warning, a mesh flag, a print defect, a filament dialog),
find it below, read the entry. Meet a new one? The `print-wiki` skill Ingests it. Curation is human;
maintenance is the LLM's.

## Troubleshooting entries

| Symptom | Entry | Kind | Proof |
|---|---|---|---|
| "Floating regions" slicer warning | [floating-regions-warning](troubleshooting/floating-regions-warning.md) | slicer-warning | slice-only |
| Non-manifold edges on mesh import | [non-manifold-edges](troubleshooting/non-manifold-edges.md) | mesh-flag | slice-only |
| "Cannot select PLA…PLA" in the AMS dialog | [cannot-select-pla-preset](troubleshooting/cannot-select-pla-preset.md) | filament-mapping | screenshot |
| `bambu print send` refuses to dispatch | [print-send-warnings-gate](troubleshooting/print-send-warnings-gate.md) | machine | slice-only |
| Grid plate spacing / stretched instances | [even-grid-spacing](troubleshooting/even-grid-spacing.md) | tolerance | slice-only |

## Layers (Karpathy pattern)

- **Raw Sources** (immutable evidence): `docs/prints/<run>/` records, `*.sliced.3mf.warnings.json`
  sidecars, screenshots, the bikar/qiyas design docs, external slicer/printer references.
- **Wiki** (this directory): the synthesised entries above.
- **Schema** (config): the [`print-wiki`](../../.claude/skills/print-wiki/SKILL.md) skill + the repo's
  `docs_gate.py`, which lints every entry at commit.

See the maintenance [log](log.md) for what changed and why.
