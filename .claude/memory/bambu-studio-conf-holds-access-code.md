---
name: bambu-studio-conf-holds-access-code
description: "~/Library/Application Support/BambuStudio/BambuStudio.conf holds the printer's LAN access code — never cat/head/print it; read single keys in code (plate type is app.curr_bed_type)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-03T20:32:03.279Z
---

`~/Library/Application Support/BambuStudio/BambuStudio.conf` is plain JSON whose top level includes
`access_code` and `user_access_code` (the printer's LAN access code). Found 2026-10-03 while
looking for where Studio keeps its saved plate type.

**Why:** the access code is a secret on the same footing as BAMBU_TOKEN ([[secret-check-no-stdout-leak]]).

**How to apply:** never `cat`, `head`, `grep` lines out of, or otherwise print that file. Read one
named key in code and print only that value or a boolean. Studio's plain settings live in the
`app` section: the saved build plate is `app.curr_bed_type` (BedType enum: 1 Cool, 2 Engineering,
3 High Temp, 4 Textured PEI, 5 Supertack), read by `parseStudioSavedPlateType` in
`tools/bambu/src/plate-type.ts`. To find where a key sits, walk the JSON and print only the paths
of that key name. See [[owner-gated-and-on-hold]].
