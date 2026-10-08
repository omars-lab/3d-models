---
name: coffee-house-storefront-repo
description: "The Shopify store is built in coffee-house-storefront, at /Users/omareid/Workspace/git-naqshcoffee/coffee-house-storefront (NaqshCoffee, private, branch main); it already has its own DESIGN.md with Omar's decisions"
metadata:
  node_type: memory
  type: reference
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-05T02:28:53.931Z
---

Omar, 2026-10-04, answering "which repo builds the store" (storefront design call 1): "it will be
in coffee-house-storefront", "under git coffeehouse", then "rmeeber fhis and find full local path".

- **Local path:** `/Users/omareid/Workspace/git-naqshcoffee/coffee-house-storefront`. Note the
  parent is `git-naqshcoffee/`, not `git/` and not `git/coffeehouse/` (neither exists). The other
  `coffee-house-*` repos sit beside it.
- **Remote:** `git@github.com:NaqshCoffee/coffee-house-storefront.git`, PRIVATE, default branch
  `main`.
- **It already has decisions.** Its `DESIGN.md` (2026-10-04, status "decided, nothing built yet")
  records Omar's calls: a native Shopify Horizon theme with the Coaster Lab in an iframe on a
  product page (Lab on its own Cloudflare Pages host, design handed over by `postMessage`, added
  with `/cart/add.js`), and the `naqshop` CLI (a fork of EarlBear's `ebshop`). Its own memory lives
  in its `.claude/memory/`. It also names a blocker 3d-models' storefront design missed: selling
  rights per design (GeoGebra-sourced designs are CC BY-NC-SA, Broug's book is under copyright).
- **How to apply:** read its `DESIGN.md` before changing 3d-models'
  `docs/design/storefront/shopify-storefront-design.md`, and where the two disagree, write the
  disagreement down as an open call rather than picking a side. Its repo has its own rules
  (CLAUDE.md, gitleaks hooks, dotenvx secrets): don't edit it from a 3d-models session unless asked.

Related: [[orb-repo-roles]], [[only-touch-our-repos]].
