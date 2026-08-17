---
name: supabase-paused-project-timeout
description: "A paused free-tier Supabase project reports as a connection TIMEOUT, not as paused — check /v1/projects/{ref} status before debugging the query"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 416aa36c-c7af-4cf1-91db-d2cdc9668841
  modified: 2026-07-31T22:14:34.740Z
---

The naqshcoffee Supabase project `gmwmrcmfywsdescglijg` (org `hbvptlahxcrlmhvtnbtk`,
**free** plan, us-west-2) auto-pauses after inactivity. While paused, every
Management API query returns:

    {"message":"Failed to run sql query: Connection terminated due to connection timeout"}

That message reads like a pooler blip or a bad query and invites debugging the
SQL. It is not. Check the control plane first — it answers instantly even when
the database is unreachable:

    curl -s "https://api.supabase.com/v1/projects/$REF" -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN"

`status` is `INACTIVE` when paused, `RESTORING` → `COMING_UP` → `ACTIVE_HEALTHY`
after a restore (~1 min observed 2026-07-31).

**Why:** the free tier pauses on inactivity, and a paused project's studio saves
and API calls all fail with the same misleading timeout — so a real outage looks
identical to a transient network error.

**How to apply:** before touching a query that times out against Supabase, read
the project status. To un-pause, `POST /v1/projects/{ref}/restore` — but note
that call was **blocked by the auto-mode classifier** on 2026-07-31, so it is
Omar's to run (dashboard **Restore**, or `! <curl>` in the session). Restoring is
free on this plan and re-pausable, but it is an outward-facing infra state change
and is not covered by authorization to apply a migration.

Token lives in `coffee-house-sites/.env` as `SUPABASE_ACCESS_TOKEN` — see
[[islamic-orb-project]] for the studio's own secrets, which are Omar's to set.
