---
name: deploy-verification
description: Verify a deploy at the published bundle, not the green run — bikar studio targets Cloudflare project bikar-studio, the deploy was silently dead for four days once, and it currently fails on a token permission the owner must fix
metadata:
  type: feedback
---

`deploy.yml` publishes `packages/web/dist` to Cloudflare Pages project **bikar-studio** → `bikar-studio.pages.dev`, custom domain `bikar.naqshcoffee.com` (302 → CF Access). The `bikar-studio-aur.pages.dev` alias is from a one-off manual `npx wrangler` deploy and is not what the workflow targets. Per-deployment `<hash>.bikar-studio.pages.dev` aliases are permanent and declared as a wildcard in `public-surface.json`.

The deploy was silently dead 2026-07-27 → 07-31 (34 failures) while `npm run build` stayed green: the workflow hand-listed workspaces and `packages/web` used an undeclared sibling. Fixed by a `--workspaces` build plus an AST manifest gate (bikar #32); one deploy then published 81 commits. As of 2026-09-01 the `Deploy to Cloudflare Pages` job on main fails on a token-permissions error — owner-only fix ([[owner-gated-and-on-hold]]).

**Why:** a green local build says nothing about a deploy that names its dependencies by hand ("an acknowledgement is not an outcome", bikar Tenet 31).

**How to apply:** after merging, `gh run list --workflow=deploy.yml`; settle "is it live" by matching content hashes of a local `npm run build --workspace packages/web` against the served bundle, grepping a string literal or CSS class ([[bikar-dev-server-and-browser-checks]]). Gallery deploy mechanics and the ~40 s 404 window: [[3d-models-deploy]]. Access model: [[bikar-studio-access]]. Merge timing: [[gh-auto-merge-footgun]].
