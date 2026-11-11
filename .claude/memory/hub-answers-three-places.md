---
name: hub-answers-three-places
description: "Where Omar's hub judging answers wait before they reach a plate page; check all three before saying \"nothing judged\""
metadata:
  node_type: memory
  type: reference
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-11-08T02:18:13.548Z
---

Omar's answers on the hub's judging page pass through three places, and `after_print.py waiting`
sees only the last one (and only as of the checkout it reads, not origin/master):

1. **Saved, not sent:** `~/Library/Application Support/3d-model-hub/answers/<plate>.jsonl`
   (the `HUB_STATE_DIR` default), plus `answers/events.log`. They are sent when every question is
   answered or he presses "Send now".
2. **Sent, PR open:** a 3d-models PR on branch `answers/<plate>-<time>`
   (`gh pr list --search "head:answers/"`).
3. **Merged:** the plate page's `## Judged` table on origin/master.

When reporting a commit, quote `origin/master`'s own SHA (`git log -1 origin/master`), not the main
checkout's HEAD. On 2026-11-07 I reported HEAD (b537f73) as master's tip while master was at
7c805c07, and the manager session caught it.

Related: [[print-feedback-on-hub-page]], [[open-hub-at-owed-questions]].
