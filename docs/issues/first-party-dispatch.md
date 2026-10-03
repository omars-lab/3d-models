---
date: 2026-09-17
---

# Dispatch went first-party (FTPS + MQTT) — the griches MCP never ran

*Issue slug: `first-party-dispatch`. Written 2026-09-17, during #50 (port `bambu print send`
to a transport we own).*

## What the design assumed, and why it broke

The transport survey (`D-054`) picked the **griches `@griches/bambu-mcp`** MCP server as the
control transport for everything the CLI does to the printer — status, dispatch, camera.
`bambu print send` was wired to spawn it (`npx -y @griches/bambu-mcp`), find an `upload` tool and a
`print`/`start` tool, base64 the `.3mf` up and call print.

That path **was never exercised end-to-end**, and it can't be: `@griches/bambu-mcp` is not on npm
(`npx -y @griches/bambu-mcp` 404s) and the GitHub repo ships no build, so the server cannot start
as wired. The status read already hit this wall and went first-party over MQTT (`D-055`, amends
`D-054`, PR #188). Dispatch is the same story, so it takes the same medicine: **own the transport
rather than depend on one we cannot install.**

## What replaced it

Dispatch is two independent halves, each now first-party:

1. **Upload — implicit FTPS on :990** (`tools/bambu/src/backends/ftps.ts`, `FtpsBackend`). The
   `.3mf` is STOR'd to the **FTP root under its bare basename** (not `/sdcard`, not `/model` — the
   reference clients upload to the login working directory and subdir uploads are rejected). User
   `bblp`, password = the LAN access code (`BAMBU_TOKEN`), self-signed cert →
   `rejectUnauthorized: false` (the trust boundary is the LAN, same as MQTT). Data-connection TLS
   **session reuse is required** by the firmware — `basic-ftp` reuses the control session on the
   data socket by default, so we simply don't break it. `basic-ftp` is pinned exact at **5.3.1**
   (the 5.0.x line carried a path-traversal + a CRLF advisory; 5.3.1 clears them, and we use only
   `uploadFrom`, plus `list` and `remove` for `bambu storage` since 2026-10-03 — never
   `downloadToDir` — against Omar's own LAN printer).

2. **Start — MQTT `print.project_file`** (`tools/bambu/src/backends/mqtt.ts`,
   `MqttBackend.startProjectFile`, built by the pure `buildProjectFileCommand`). Publishes
   `{ print: { command: "project_file", param: "Metadata/plate_<n>.gcode", url: "ftp:///<name>", … } }`
   to `device/<serial>/request`. The uploaded file is referenced as `ftp:///<name>` — **three
   slashes**: empty host + `/<name>` at the FTP root. Pause/resume/stop ride the same topic via
   `buildPrintControlCommand`.

`print.ts` now orchestrates the two backends directly; `McpBackend` is gone from the dispatch path
(it survives only as the router's aspirational fallback for capabilities with no first-party backend
yet — camera/ams — which is honest, since it isn't installable either).

## Grounded command shapes, and the three fields that are a CAL-shaped bet

The `project_file` payload was grounded against three independent working clients — **pybambu**,
**bambulabs_api**, and the **OpenBambuAPI** spec — not guessed. Where they agree, the value is a
default two clients actually send:

- all four `project_id` / `profile_id` / `task_id` / `subtask_id` are the string `"0"` ("Always 0
  for a local print"); `sequence_id` `"0"`;
- `use_ams: false` (single filament / external spool — the builder default only; since 2026-09-26
  `print send` sets it from the loaded trays, see below), `bed_leveling: true`, `flow_cali: true`,
  `vibration_cali: true`, `layer_inspect: false`, `timelapse: false`.

Three fields the sources **disagree on for a dual-nozzle X2D** are exposed as overridable options
(`--bed-type`, `--ams-mapping`, `--md5`) and carry documented defaults, treated as a **CAL-shaped
bet** — a value we believe but have not yet confirmed on *this* machine:

| field | default | why unconfirmed |
|---|---|---|
| `bed_type` | settled 2026-10-03: the slice's own plate type, never `"auto"` | `"auto"` paused sheets-04b at layer 0; see [the plate type](sliced-for-wrong-plate.md) |
| `ams_mapping` | matched from the loaded trays (the builder default `[0]` is no longer sent) | dual-nozzle firmware may need a nozzle index, or the empty-string form (`--ams-mapping none`) |
| `md5` | `""` (empty) | accepted on P1/A1-class; X1-class historically validated the checksum |

**How the bet gets settled (deferred to the physical send, owner-gated):** before the first real
dispatch, diff this payload against a **BambuStudio ground-truth capture** — send one plate from the
GUI with an MQTT sniffer on `device/<serial>/request` and compare Studio's `project_file` fields to
ours, field for field. `bambu print send --dry-run` prints the exact payload we would publish for
that diff **without uploading or publishing** (it reads the loaded trays to fill `ams_mapping`) — it is
the review surface. Any field Studio sets differently gets
corrected here (or wired to its flag) and the bet closes with a one-line note.

## Why verification stops at the gate

Printing is **owner-gated and on hold** — no `CAL` bet yet justifies spending filament (memory
*owner-gated-and-on-hold*). So this PR ships the transport **verified as far as it can be without
moving hardware**: the pure builders are unit-tested
(`tools/bambu/src/backends/dispatch.test.ts`), typecheck is clean, and `--dry-run` proves the
end-to-end payload. The FTPS handshake and the physical `print`
publish are exercised only when Omar dispatches a real plate — `send` stays fail-closed (refuses
without `--yes` or a TTY confirm), and the skill never passes `--yes` on Omar's behalf. The
ground-truth diff above is the first thing that real send does.

## The exact Plate-1 payload to diff (the review surface)

This is what `bambu print send build/…/plate-1-machine-card.sliced.3mf --plate 1 --dry-run` publishes
to `device/<serial>/request` (rendered from the pure `buildProjectFileCommand`, so it is byte-for-byte
what a real send would put on the wire — the upload lands over FTPS at `<host>:990` as
`STOR /plate-1-machine-card.sliced.3mf` first). **This block is the ground-truth diff surface:** send
one plate from the BambuStudio GUI with a sniffer on the same topic and compare field-for-field. The
three `[X2D-UNCONFIRMED]` fields are the only ones expected to possibly differ; anything else that
differs is a bug to fix here before the first real send.

```json
{
  "print": {
    "sequence_id": "0",
    "command": "project_file",
    "param": "Metadata/plate_1.gcode",
    "url": "ftp:///plate-1-machine-card.sliced.3mf",
    "subtask_name": "plate-1-machine-card.sliced",
    "project_id": "0",
    "profile_id": "0",
    "task_id": "0",
    "subtask_id": "0",
    "md5": "",
    "bed_type": "auto",
    "bed_leveling": true,
    "flow_cali": true,
    "vibration_cali": true,
    "layer_inspect": false,
    "timelapse": false,
    "use_ams": false,
    "ams_mapping": [0]
  }
}
```

`md5` / `bed_type` / `ams_mapping` are the three CAL-shaped fields from the table above — the diff
closes the bet by confirming or correcting exactly these. (This block predates 2026-09-26: a send
now puts the matched tray in `ams_mapping` and sets `use_ams` to match — next section.) The operator runbook consumes this from
[`guide-print`](../../.claude/skills/guide-print/SKILL.md) step 4's pre-send gate (line 2).

## 2026-09-26: the send picks the tray

**What went wrong.** Every send published `use_ams: false` with `ams_mapping: [0]` — feed from
the external spool — and `print send` had no way to say otherwise. The external spool on our X2D
is empty, so a CLI send would have printed nothing. The minis-01 run found it (2026-09-25), and
minis-01 and minis-02 went out from Bambu Studio instead.

**What replaced it.** Without `--ams-mapping`, `print send` now reads the plate's *used* filaments
(`Metadata/slice_info.config`, not the project's full filament list) and the loaded trays (a
read-only status request). It matches them by color with the same `filament-sync` match, and
sends one tray number per filament, with -1 for the ones the plate does not print with. `use_ams`
is true when any of those is an AMS tray. Trays are numbered `unit*4 + tray`, and the external
spool by its id `254`, the numbering OpenBambuAPI documents for Studio's sends. An AMS HT unit
(id 128 and up) has no number we are sure of, so a match to one is refused.

**It refuses rather than choose.** A missing color, a near-tie, a material mismatch or an
unnumbered tray stops the send, and it prints the loaded trays with their numbers so the operator
can pass `--ams-mapping`. That is the usual case today: our slices carry Studio's default green
`#00AE42`, not the color that is loaded, so the operator names the tray, and choosing the
filament stays Omar's.

**Still unconfirmed on the X2D.** The tray numbering, and whether dual-nozzle firmware also wants a
per-nozzle field beside `ams_mapping`, are settled only by the Studio capture above. The numbers
come from OpenBambuAPI, not from this machine.

## 2026-10-03: the first CLI send stopped at the upload

**What happened.** sheets-04b was the first plate sent through `print send` rather than Bambu
Studio. Every check before the upload passed: the approval, the printer idle (FINISH), the tray
match (`ams_mapping [3]`) and the bed photo. The FTPS login worked, then `STOR sheets-04b.plate.3mf`
at the FTP root came back `553 Could not create file`. Nothing was published over MQTT, nothing
printed, and the page's yes was left unspent, because the send only rewrites the page after it
succeeds.

**What it does and does not tell us.** A 553 is the server refusing to write that file. That
fits several causes, and this run cannot tell them apart: no storage card in the printer, a full
or read-only card, or the X2D wanting the file somewhere other than the root that the reference
clients use (the comment at the top of `ftps.ts`). The upload path is unchanged until one of those
is checked on the machine. Never work around it by sending from Bambu Studio for Omar.

**What the status report showed (later the same day).** The printer's status report carries
`sdcard`, and it read `false`, with the card's free and total space both 0. The printer had no card
in, and the FTP root the upload writes to is the card, so this is the likeliest cause. It is not
proven until a send with a card in goes through. Bambu Studio's earlier sends still printed because
they land in the printer's built-in storage, which the report shows with about 864 MB free and the
FTP upload cannot reach.

**What changed.** `print send` reads `sdcard` from the status read it already makes, and refuses
before the upload when there is no card, or when the card's free space is reported and smaller
than the plate (`tools/bambu/src/storage.ts`). A frame that does not mention the card is let
through, since other models may leave the field out and the upload's own error still stops the
send. A 553 now comes back as "the printer would not save the file", pointing at
`bambu storage show`. Reading the card's free space from the `tl_external_*` fields is our reading
of names the printer reports for timelapses; it is unconfirmed until a card is in.

New verbs, `bambu storage`: `show` (card in or not, free space, from the status report), `list`
(the files in a folder on the card) and `rm` (deletes plate files). `rm` takes only `.3mf` names at
the card's top, where `print send` puts them, refuses the file the printer is printing from, and
asks first unless given `--yes`. `list` and `rm` use basic-ftp's `list` and `remove` on the same
login as the upload; the advisories noted above were against the 5.0.x line and the pin is 5.3.1.

**Settled (the same evening).** Omar put a USB drive in; the X2D's external storage is a USB port,
though the status report still names it `sdcard`. `bambu storage show` then read 22.7 GB free of
28.7 GB from the `tl_external_*` fields, so those fields do track the external drive. The same
sheets-04b send went through unchanged: the upload to the FTP root and the `ftp:///` start both
worked, the printer went to PREPARE and then RUNNING, and the X2D took `bed_type: "auto"`,
`ams_mapping: [3]` and an empty `md5` without complaint. So the missing drive was the cause of the
553. Bambu Studio prints without a drive because it uploads to the built-in storage another way;
two research passes and a consolidation of them were still open as PRs when this was written.

**Then it paused at layer 0.** A few minutes later the printer stood in PAUSE at 0%, layer 0 of
20, heaters off, with `print_error` 83918929, which is `0500-8051` in Bambu's error list:
"Detected build plate is not the same as the Gcode file". Our slices are made for the Cool Plate
(`curr_bed_type` in the `.3mf`), and the send said `bed_type: "auto"`. The printer reports the
plate it sees as `device.plate.cur_id` `P0101`, an id with no name we can look up. So the send
itself worked, and what stopped the print is the slice's plate type against the plate on the
bed. Nothing in `print send` compares the two yet; it would need the name behind `P0101`, which
only the plate on the bed can tell us.

**What it was.** The bed photo showed a Textured PEI Plate, and Bambu Studio is set to one; the
slice was made for a Cool Plate because Studio's command line defaults to it and our slices never
named a plate. The print was cancelled at 20:12 UTC (`0300-400C`). The fix, and the evidence, are
in [sliced-for-wrong-plate.md](sliced-for-wrong-plate.md).

## Files

- `tools/bambu/src/backends/ftps.ts` — the FTPS upload backend (new).
- `tools/bambu/src/backends/mqtt.ts` — `buildProjectFileCommand` / `buildPrintControlCommand` +
  `startProjectFile` / `sendPrintControl` (dispatch added to the D-055 read backend).
- `tools/bambu/src/commands/print.ts` — `runSend` / `runControl` rewired onto the two backends; the
  warnings gate (#52) and owner gate are unchanged.
- `tools/bambu/src/backends/dispatch.test.ts` — unit tests for the three pure builders.
- `tools/bambu/src/backends/router.ts` — comment updated: status/control/upload are first-party now.
