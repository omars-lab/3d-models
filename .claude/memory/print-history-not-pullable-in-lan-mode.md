---
name: print-history-not-pullable-in-lan-mode
description: "There is no viable way to pull the X2D's past-print history over the LAN — cloud history is empty in LAN mode, FTPS is partial/estimate-only; decided 2026-09-21 to stay forward-only"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9aae5724-5284-48f1-85cb-3c0496a1c2e1
  modified: 2026-09-21T16:37:15.041Z
---

Researched 2026-09-21 (Omar: "i don't want a live probe we always run … see if we can pull history").
Grounded conclusion: **no viable retroactive print-history source over the LAN.** Do not re-explore.

- **Bambu Cloud `GET api.bambulab.com/v1/user-service/my/tasks`** is the only rich source (real
  grams via task `weight` + `amsDetailMapping[]`, start/end times, device, cover, status 2=finished
  /3=aborted). But per Bambu's wiki, **in LAN Mode no print info or files are transferred to the
  cloud, and Handy/cloud print history is not supported in LAN mode** — so it is *empty* for exactly
  our prints. Also needs a separate Bambu **account** login (JWT bearer, 2FA likely; refresh
  endpoint is dead → re-auth not refresh). Only becomes useful if the machine leaves LAN-only mode,
  which reverses the deliberate #63 lockdown (owner's call) and still can't recover past LAN prints.
- **FTPS (port 990, user `bblp`, password = the LAN access code we already hold)** exposes the SD
  card only (`timelapse/`, `cache/` = recently-printed .3mf with slice metadata, `ipcam/`) — **not**
  firmware state. You can *infer* a best-effort history (mtime → timestamp, parse .3mf → **estimated**
  grams), but there is no structured log, no success/fail, no *actual* grams, and it misses prints
  with no timelapse or an evicted cache.
- **Live MQTT** = current-job snapshot only, no history, no grams (see [[bambu-x2d-bringup]]).
- The printer's on-screen task history is firmware-internal, exposed by no LAN API.

**Decision (Omar, 2026-09-21): Neither — keep it forward-only.** No `bambu print history` verb, no
cloud-mode switch. Counting GUI prints stays on the shipped `bambu print capture` verb (run after a
print, MQTT → draft record; see [[print-model-skill]] and PR #289). The counting gap #71 aimed at
is therefore only partly closed (a GUI print is counted only if capture is run afterward) — accepted.
