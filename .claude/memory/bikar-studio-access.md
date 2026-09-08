---
name: bikar-studio-access
description: "bikar studio access pattern — public URL bikar.naqshcoffee.com, gated behind org GitHub sign-in (internal audience, internet-reachable)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 792c03e6-3f91-4133-a2ea-35c8bfde5227
  modified: 2026-09-02T19:04:01.663Z
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

**Update 2026-09-02 — `bikar-studio.pages.dev` is now Access-gated too (verified live).**
The plan's security finding (that pages.dev served the private studio with HTTP 200 and no
auth) is closed: an anonymous GET to both `bikar-studio.pages.dev/` and `/editor` now
**302s to `naqshcoffee.cloudflareaccess.com`**, exposure-equivalent to the apex. There is
**no anonymous public host** any more. The code side shipped under **#83**: `public-surface.json`
classifies pages.dev as `"exposure": "access"`, `check-deploy.sh` presents a
`CF-Access-Client-Id/Secret` service-token pair when set (and reports content NOT VERIFIED
when absent), and `setup-secrets.sh` step 2 pipes `CF_ACCESS_CLIENT_ID/SECRET` from the
dotenvx `.env` to GitHub Actions.

**Update 2026-09-02 — the CI service token is minted, admitted, and verified working.**
The one step no script performs is *admitting* the token: `cf-setup.sh` writes only the
org-member policy (`github-organization` include), so a minted token reaches nothing until a
**Service Auth policy** is added on the *Bikar Studio* Access app **by hand** (Zero Trust →
Access → Applications → Bikar Studio → Policies). Omar did that dashboard edit; verified live
via a leak-free `dotenvx run` curl (headers into a mode-600 temp config, only the status code
prints): **200** on `/` and `/editor` **with** the token, **302** to
`naqshcoffee.cloudflareaccess.com` **without** it (anonymous shows `service_token_status:
false` in the login-redirect meta). The full mint → admit → push → verify → rotate runbook now
lives in bikar's `manage-secrets` skill (PR #157). #63 is fully closed — lockdown live *and*
CI can read content through the gate. See [[owner-gated-and-on-hold]].

**This settles the "bikar-studio public-surface keystone"** that gated the d3-integration
Phase 1 and the qiyas data-model-API D-API-2 (see [[islamic-orb-project]],
`docs/d3-integration-design.md` §5, `qiyas/docs/design/data-model-http-api.md`): a shared
d3 layer / explorer and a qiyas data API can be served from this org-gated surface — behind
the same GitHub-org gate, internet-reachable but not open to the world.
