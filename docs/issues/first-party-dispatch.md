# Dispatch went first-party (FTPS + MQTT) — the griches MCP never ran

*Issue slug: `first-party-dispatch`. Written 2026-09-17, during #50 (port `bambu print send`
to a transport we own).*

## What the design assumed, and why it broke

The transport survey (`D-054`) picked the **griches `@griches/bambu-mcp`** MCP server as the
control transport for everything the CLI does to the printer — status, dispatch, camera. `bambu
print send` was wired to spawn it (`npx -y @griches/bambu-mcp`), find an `upload` tool and a
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
   `uploadFrom` — never `downloadToDir`/`list` — against Omar's own LAN printer).

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
- `use_ams: false` (single filament / external spool), `bed_leveling: true`, `flow_cali: true`,
  `vibration_cali: true`, `layer_inspect: false`, `timelapse: false`.

Three fields the sources **disagree on for a dual-nozzle X2D** are exposed as overridable options
(`--bed-type`, `--ams-mapping`, `--md5`) and carry documented defaults, treated as a **CAL-shaped
bet** — a value we believe but have not yet confirmed on *this* machine:

| field | default | why unconfirmed |
|---|---|---|
| `bed_type` | `"auto"` | firmware auto-detects on most models; some builds want an explicit plate name |
| `ams_mapping` | `[0]` | dual-nozzle firmware may need a nozzle index, or the empty-string form (`--ams-mapping none`) |
| `md5` | `""` (empty) | accepted on P1/A1-class; X1-class historically validated the checksum |

**How the bet gets settled (deferred to the physical send, owner-gated):** before the first real
dispatch, diff this payload against a **BambuStudio ground-truth capture** — send one plate from the
GUI with an MQTT sniffer on `device/<serial>/request` and compare Studio's `project_file` fields to
ours, field for field. `bambu print send --dry-run` prints the exact payload we would publish for
that diff **without connecting** — it is the review surface. Any field Studio sets differently gets
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

## Files

- `tools/bambu/src/backends/ftps.ts` — the FTPS upload backend (new).
- `tools/bambu/src/backends/mqtt.ts` — `buildProjectFileCommand` / `buildPrintControlCommand` +
  `startProjectFile` / `sendPrintControl` (dispatch added to the D-055 read backend).
- `tools/bambu/src/commands/print.ts` — `runSend` / `runControl` rewired onto the two backends; the
  warnings gate (#52) and owner gate are unchanged.
- `tools/bambu/src/backends/dispatch.test.ts` — unit tests for the three pure builders.
- `tools/bambu/src/backends/router.ts` — comment updated: status/control/upload are first-party now.
