---
name: print-watching-in-background
description: "Omar 2026-10-10 — a running print is watched by a background watcher agent, not the main session; at the end it publishes a small QR-checked WebP timelapse and still on the plate page"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-10T16:54:11.613Z
---

A sent print is watched in the background so the main session keeps working. The main session starts
`print_monitor.py` itself, in the background. A shell that a subagent starts can die when that
subagent ends. It then hands `.claude/skills/monitor-print/watcher.md` to an Agent. The watcher
loops on `--next`, opens each picture, notes it with `--look`, and comes back early on trouble. At
the end it runs `--publish` (3d-models #679).

**Why:** Omar, 2026-10-10: prints "typically take more than 45 minutes", so the picture watching
should happen "behind the scenes and a sub agent and that our main agent can continue working on
important things". He also asked: "that agent should also worry about … re-updating the design
documents with the GIF of the print construction."

**Publishing is approved, if small.** He said "I don't mind publishing the gifts, but are they …
bloated?" So:
- What goes in the repo is an animated WebP (about 120 KB) and a WebP still (about 10 KB). A 640 px
  GIF was 1.4 MB.
- Both go in `docs/design/plates/<plate>-media/`, under a `## The print` section on the page.
- `--publish` refuses any file over 400 KB, and any frame where zbarimg decodes a code (the printer
  has QR stickers and the repo is public).
- Every other chamber picture, and the full-size GIF sent to Omar, stays in the gitignored `.bambu/`.

**How to apply:**
- Run the watcher with the vault's absolute script path. The script finds `.bambu/` from its own
  location (`ROOT = parents[4]`), so a copy in a worktree sees an empty folder.
- Never send a printer command from the watcher.
- Don't give the watcher a Monitor. Tested 2026-10-10: a subagent started a Monitor and ended its
  turn to wait. It was forced to hand back at once, before any event arrived. The blocking
  `--next --wait 9` loop is what keeps it alive. Any Monitor belongs to the main session.
- **A picture with a person in it stays off the page.** This was Omar's call on 2026-10-10, after
  sheets-04g-fit2's last frame caught his hand lifting the plate. The watcher starts that
  picture's `--look` with "person:" and passes the frame to `--publish --leave-out <frame>`. A
  name that is not a frame refuses and nothing is written. Leaving a picture out never gets round
  the QR check (#681).
- **Proven end to end on 2026-10-10.** The watcher replayed sheets-04g-fit2 with 41 tool calls in
  about 98 s. It opened all 17 pictures, marked the hand frame on its own and published 16 frames:
  84 KB of timelapse and a 5 KB still (#682). Trust the brief as written. The main session still
  opens `finished.webp` before shipping.
- Related: [[look-before-you-print]], [[x2d-does-its-own-failure-detection]],
  [[third-party-stls-stay-out-of-git]].
