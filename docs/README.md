# 3d-models docs

The home page of the `docs/` vault: design docs, the research behind them, the pivots, the
print wiki, the pattern catalog and the print records. Open `docs/` as a vault in Obsidian to see
the live tables below; on GitHub each table shows as one line naming its view file, and the
links under it are the same map in plain markdown.

How the vault is set up, and the rules it is checked against:
[vault-setup](../.claude/skills/vault-setup/SKILL.md).

## Start here

- [Plan](working-model/plan.md) — what is being built, in what order.
- [Backlog](working-model/backlog.md) and the task loops: [coaster pipeline](tasks/coaster-pipeline/backlog.md),
  [catalog expansion](tasks/catalog-expansion/backlog.md),
  [print infrastructure](tasks/print-infrastructure/backlog.md),
  [consolidation](tasks/consolidation/backlog.md), [parked](tasks/parked/backlog.md).
- [Decisions log](working-model/decisions-log.md) — every D-0xx, with the options and why.
- [FAQ](faq.md) and the [grounding defect taxonomy](guides/grounding-defect-taxonomy.md) — how docs
  here go wrong, and how to write one that does not.

## Design docs

Each design doc carries a `status`: idea, draft, decided, built or superseded.

![[bases/design-docs.base]]

Not yet built: [tower sleeve](design/printing/tower-sleeve-design.md) (an idea),
[click-to-source](design/language/click-to-source-design.md) and [Orb Lab P2](design/orb/orb-lab-p2-design.md) (drafts).
The full list is the table above, or the files at the top of this folder.

## Research

The record behind the docs, each note with the docs it `feeds`.

![[bases/research.base]]

Also: the [shipped record](research/shipped-record.md) (the orb project's ship log, July to
September 2026), [bubble lettering on coasters](research/coaster-bubble-lettering.md), and the
[studio and gallery brick render mismatch audit](research/studio-gallery-render-mismatch-audit.md).

## Issues — pivots and dead ends

![[bases/issues.base]]

- [Base-face honesty scaffold pivot](issues/base-face-honesty-scaffold-pivot.md)
- [Coaster 3MF filament shape and export hang](issues/coaster-3mf-filament-shape-and-export-hang.md)
- [Coaster outline fit pivot](issues/coaster-outline-fit-pivot.md)
- [Constructions ledger missed a new reconstruction](issues/constructions-ledger-missed-new-reconstruction.md)
- [Docs gate skipped its rules inside a `.claude/worktrees/` checkout](issues/docs-gate-worktree-under-claude.md)
- [FAQ: counted use, not re-derivation](issues/faq-counted-use-not-rederivation.md)
- [First-party dispatch](issues/first-party-dispatch.md)
- [A wrapped code span broke an Obsidian table](issues/obsidian-wrapped-code-span.md)
- [Slicer warnings: CLI visibility pivot](issues/slicer-warnings-cli-visibility-pivot.md)
- [X2D "Filament Grouping" mode](issues/x2d-filament-grouping-mode.md)

## Printing

- [Plates](plates/README.md) — what to print next and why: one review page per plate, with
  pictures, Omar's approval and how many times it printed.
- [Prints](prints.md) — what has printed; the records are in `prints/<run>/`.
- [3D-printing wiki](wiki/index.md) — what a slicer warning or print defect means, and what to do.

![[bases/plates.base]]

![[bases/prints.base]]

![[bases/troubleshooting.base]]

## Patterns and constructions

- [Pattern catalog plan](catalog/plan.md) and the [constructions ledger](constructions/ledger.md).
- [naqsh cookbook](cookbook/README.md) — recipes for the language, each with a picture of what
  one knob changes.

## Maps and runbooks

- [Orb pipeline map](guides/orb-pipeline-map.md) — the orb pipeline, source to badge.
- [Local CI runbook](guides/local-ci-runbook.md) — the checks run here, with no hosted runner.
- [Site graph](site-graph.md) — the gallery's pages and how they link.
