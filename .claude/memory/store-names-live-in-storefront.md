---
name: store-names-live-in-storefront
description: "Before naming or renaming a pattern or color theme for shoppers, read the storefront's docs/naming/names.yaml — Omar may already have picked the store name there"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e778ebdd-03d8-4cb5-9096-0e141345d0f5
  modified: 2026-11-10T20:12:55.079Z
---

The shop's names for patterns and colorways live in the storefront repo
(`~/Workspace/git-naqshcoffee/coffee-house-storefront/docs/naming/names.yaml`), not in 3d-models.
Its `colorways:` map overrides 3d-models' theme names when the store syncs. On 2026-11-10 I drafted
"Leaf green" for the gBV all-green theme (catalog-expansion item 8) without looking there. Omar had
already picked "Emerald green" on 2026-10-11 (call 8). Shown both, he kept "Emerald green" everywhere,
and #999 shipped that.

**Why:** a fresh draft beside an existing pick gives one theme two names and asks Omar a question he
already answered.

**How to apply:** before any shopper-facing name in 3d-models (themes.yaml `name`, a pattern name),
grep names.yaml for the handle (`gbv-<theme id>`) and use what is there. Draft only when it has no
entry. Pink heart → Bougainvillea, All four trays → Bazaar and Pink and green rings → Watermelon are
already picked there too. See [[omar-working-preferences]].
