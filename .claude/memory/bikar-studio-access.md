---
name: bikar-studio-access
description: "bikar studio access pattern — public URL bikar.naqshcoffee.com, gated behind org GitHub sign-in (internal audience, internet-reachable)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 792c03e6-3f91-4133-a2ea-35c8bfde5227
  modified: 2026-08-31T15:36:42.868Z
---

**bikar studio is reachable over the open internet but gated to the org.** The only
public-facing access is **`https://bikar.naqshcoffee.com/`**, and reaching it requires
**signing into our NaqshCoffee org GitHub account**. So the surface is *internal by
audience* (only org members can use it) yet *public by reachability* (a real internet
URL, not a VPN/private network) — the "internal, over the internet" shape, i.e. an
org-SSO gate in front of a public endpoint (matches qiyas's Cloudflare-Access "Shape C").

Do not describe bikar studio as either "fully public" or "private/internal-network." It
is org-gated-but-internet-accessible. An earlier note called the surface
`bikar-studio.pages.dev`; the canonical public entry is `bikar.naqshcoffee.com` behind
the GitHub org sign-in.

**This settles the "bikar-studio public-surface keystone"** that gated the d3-integration
Phase 1 and the qiyas data-model-API D-API-2 (see [[islamic-orb-project]],
`docs/d3-integration-design.md` §5, `qiyas/docs/design/data-model-http-api.md`): a shared
d3 layer / explorer and a qiyas data API can be served from this org-gated surface — behind
the same GitHub-org gate, internet-reachable but not open to the world.
