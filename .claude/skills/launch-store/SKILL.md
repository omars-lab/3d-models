---
name: launch-store
description: The coaster store's pre-launch checklist — one list of everything the Shopify store still needs before it opens to buyers (the calls, the store's setup, rights records and photos, swatch card and theme prints, pricing, and the values only Omar sets), each line saying who does it and where it is tracked, with a check that keeps the calls' ticks in step with their Decided lines. Use for "what's left before the store opens", "launch the store", "pre-launch checklist", "are we ready to open", "add this to the launch list", or after a store call is decided or a store task ships. Not for building the store itself (coffee-house-storefront) or pricing one order (`bambu order price`).
---

# launch-store — what the store still needs before it opens

Omar asked for this on 2026-10-05, on call 24 of the
[open-calls page](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#24-which-pictures-the-store-opens-with)
([D-102](../../../docs/working-model/decisions-log.md#d-102--the-stores-first-setup-basic-plan-priced-by-finish-set-and-colors-etsy-later)):
"make sure we are creating a proper backlog to consolidate all the things we have to do to launch
our store - add this to the pre-launch checklist under a launchign store skill".

The store's work is spread over several designs and repos: the
[storefront design](../../../docs/design/storefront/shopify-storefront-design.md) and its phases,
the [order-driven Lab](../../../docs/design/coaster/order-driven-lab-design.md), the decisions
log, the coaster-pipeline backlog, bikar and coffee-house-storefront. The list in
[`checklist.md`](checklist.md) gathers it in one place. It does not replace those: each line
points at where its work is tracked, and the work is done there.

## Every run

1. **Read [`checklist.md`](checklist.md)** and check it:
   `python3 .claude/skills/launch-store/scripts/launch_check.py`. It prints how many items are
   done and how many are open, by who does them.
2. **Bring it up to date.**
   - A call decided on the open-calls page: tick its line. The check fails until you do, and fails
     if you tick one that has no **Decided** line.
   - A task shipped: tick its line with the PR that did it, as in "(3d-models #562)". Tick only
     what you can point at.
   - New work the store needs before it opens, found anywhere: add a line in the right section,
     in the form the file's header gives, with who does it and where it is tracked. Track it in
     its own backlog first if nothing tracks it yet, so the line has somewhere to point.
   - Work moved to after opening: take it off and name it under "Not before opening".
3. **Answer the question asked.** For "what's left", give the open lines grouped by who does
   them, Omar's first, in plain words. For "are we ready", the answer is no while any line is open.
4. **Ship a change to the list** like any doc: a branch off `origin/master`, `make validate`, a
   PR.

## What this skill never does

- **Never ticks a call for Omar.** A call with no tick on its page stays open here (the
  [request-feedback](../request-feedback/SKILL.md) rule).
- **Never ticks his lines:** prices, the lead-time range, the returns wording, the domain,
  publishing the template, opening the store, buying colors, printing, photos.
- **Never writes a price, an order or a customer into this public repo** (§9.4 of the
  order-driven design, D-101). A line says that a price is set, never what it is.
- **Never edits coffee-house-storefront** from here. Its lines are done there; this list only
  points at them.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/launch_check.py` | Checks every line has a known owner and a tracking link that resolves, each "Call N" tick matches its call's Decided line, and every D-id is in the log; prints done and open by owner | Every run, and after editing the list | `python3 .claude/skills/launch-store/scripts/launch_check.py` |
| `scripts/launch_check.py --ticks` | Only the call rule, on any doc with a tick list of calls | After deciding a storefront call; `make validate-orders` runs it on the storefront design's §16.5 | `python3 .claude/skills/launch-store/scripts/launch_check.py --ticks docs/design/storefront/shopify-storefront-design.md` |
| `scripts/launch_check.py --self-test` | Fixtures for each mistake: a call ticked before it is decided, a decided call left open, a link to the wrong call, a missing owner or link, an unknown D-id | After editing the script; `make validate-orders` runs it | `python3 .claude/skills/launch-store/scripts/launch_check.py --self-test` |

## Why this is a skill

Omar asked for it by name. It is also the place the drift it checks was found: the storefront
design's own tick list showed eight calls open a day after all of them were decided. The check
is the gate (`make validate-orders`); the skill is the routine of keeping one list honest.
