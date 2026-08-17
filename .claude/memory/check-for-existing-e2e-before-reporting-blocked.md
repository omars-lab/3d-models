---
name: check-for-existing-e2e-before-reporting-blocked
description: "Before reporting browser/UI verification as blocked, look for an existing e2e suite — bikar has one at packages/e2e"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 792c03e6-3f91-4133-a2ea-35c8bfde5227
  modified: 2026-08-03T06:38:56.954Z
---

I reported studio browser verification as "blocked" because the
chrome-devtools MCP profile was locked, and offered a corpus probe as a
substitute. The user asked "can we not set up playwright tests for
verification?" — bikar already had `packages/e2e` (8 Playwright specs,
Chromium installed, `playwright.config.ts` starting its own dev servers). I
never looked.

**Why:** an interactive browser tool being unavailable says nothing about
whether the repo can drive a browser. Treating one blocked tool as "browser
verification is impossible" skipped the check that would have answered it in
one `ls`, and unit tests were offered as a substitute for a claim they
structurally cannot make (a canvas cannot be inspected without a browser).

**How to apply:** when a UI/visual claim needs verifying, search for an e2e
harness first (`packages/e2e`, `*.spec.ts`, `playwright.config.*`,
`.github/workflows/*e2e*`) before reporting any browser tool as blocking.
Then check whether anything actually *runs* it — the suite here had no
workflow, and that is how a top-level `TypeError` crashed `editor.html` on
every load for four months while lint, typecheck and 2460 unit tests stayed
green. Related: [[islamic-orb-project]].
