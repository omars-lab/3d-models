---
name: owner-gated-and-on-hold
description: What only Omar can do and what is deliberately on hold — printing (no CAL bet settled), schema-v tag and npm publish, contract acceptance, Cloudflare/GHCR settings, studio secrets
metadata:
  type: project
---

**On hold — printing.** Decided 2026-07-27: printing is paused; when it resumes the machine is the Bambu A1/P1S/X1C class (256³ bed); catalog print targets stay "actuals only". Consequences: every `CAL-*` bet is provisional and no constant is earned; coupons (MC-1…MC-8, LG-*, W-F1/W-C1, LG-P1/P2) are `planned`; the prints tab ships an honest empty register and its gate is deferred to ship with the first real print (D-046).

**Owner-gated (never do these):**
- push the `schema-v*` tag / npm-publish `@naqshcoffee/qiyas-schema` (now 0.3.0 unpublished);
- accept contract rows in sacred-patterns (mirrors elsewhere stay PROPOSED);
- Cloudflare: the studio deploy token permission (deploy on main fails on it as of 2026-09-01), Access `self_hosted_domains`, redeploying the studio with its secrets (`setup-secrets.sh`); GHCR package access is UI-only;
- branch protection changes (applied 2026-09-02).

**Why:** these need credentials or ownership decisions the session does not hold; attempting them produces a confident failure.

**How to apply:** when a task lands on one of these, finish everything else, then hand the exact command back. Related: [[deploy-verification]], [[contract-and-schema-mirror]], [[bikar-studio-access]], [[calibration-baseline-trailer]].
