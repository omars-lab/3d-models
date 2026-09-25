---
name: bambu
description: Drive the Bambu X2D printer from Claude Code via the tools/bambu CLI — check status, slice a bikar plate, dispatch a print, list what has been printed, and validate/log a print record. Use whenever the task is talking to the printer day-to-day (status, slice, print send/list, validate record) — not first-time setup, which is the setup-bambu-x2d skill. Reach here for "what has it printed?", "slice this", "send this to the printer", "check the printer", "log this print".
---

# Drive the Bambu X2D with the `bambu` CLI

`tools/bambu` is our one command over the printer: it turns a bikar `.bkr`/STL into a sliced plate,
a dispatched print, and a logged record — each as a single, allow-listable call. This skill is the
**day-to-day usage** front door (status → slice → dispatch → list → record). First-time bring-up
(LAN + Developer Mode, wiring the MCP, installing Bambu Studio) is a different job — see
[`setup-bambu-x2d`](../setup-bambu-x2d/SKILL.md).

**Consume, don't reimplement.** The CLI owns only our verbs and their ordering; transport is the
griches MCP, slicing is the BambuStudio CLI, geometry is bikar, and the record schema is the prints
gate. Route to those authorities — never re-implement one. The `--help` on every verb *is* the
reference: [`tools/bambu/README.md`](../../../tools/bambu/README.md).

## Run it

From anywhere in the repo: `tools/bambu/bin/bambu <group> <verb>` (or in `tools/bambu`,
`npm run bambu -- <group> <verb>`). Node is pinned to v22.22.3 —
`export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"` first, or bare `node` fails oddly.
`bambu <group> <verb> --help` everywhere.

## The verb map — reach for the verb, not the MCP

| Want to… | Verb | Safe to run now? |
|---|---|---|
| See temps / AMS / job progress | `status show` · `status monitor` · `status camera` | **read-only** — needs transport (bring-up done) |
| **Auto-pull the bench-sheet profile header** | `header` (`--plate <plate.3mf>` fills machine/layer/profile/slicer; `--json`) | **read-only** — fills the header off the machine + `.3mf`; the manual fields (ambient/enclosure/caliper) stay yours |
| Turn a `.bkr`/STL into a plate | `slice plate <model>` (`--dry-run`, `--settings`/`--filament`) | local — needs Bambu Studio installed |
| **List what was printed — and how** | `print list` (`--how` for machine/material/nozzle/profile; `--settles`/`--material`/`--machine`/`--status` filter; `--shipped`/`--drafts`/`--json`) | **always** — reads records, touches no hardware |
| Send a plate to the machine | `print send <plate.3mf>` (`--record`, `--dry-run`, `--yes`) | **OWNER-GATED** — see below |
| Pause / resume / stop a running job | `print pause` · `print resume` · `print stop` | acts on live hardware |
| Gate a mesh / plate / record | `validate mesh <bkr>` · `validate plate` · `validate record [dir]` | local, no hardware |

## Slicing an X2D plate

The known-good X2D trio (from the bench sheet) is passed by **preset display name** — `slice` resolves
each name to its bundled JSON automatically:

```
tools/bambu/bin/bambu slice plate <abs-path-to.stl> \
  --settings "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D" \
  --filament "Bambu PLA Basic @BBL X2D 0.4 nozzle"
```

A valid X2D slice writes gcode with `printer_model = Bambu Lab X2D` and `nozzle_diameter = 0.4,0.4`.
Two footguns worth knowing:

- **`--settings`/`--filament` take profile JSON *paths*, not names — at the BambuStudio layer.** A bare
  name to the raw CLI fails with `can not find setting file`. Our `slice` resolves a name → the bundled
  `…/BambuStudio.app/Contents/Resources/profiles/<vendor>/{machine,process,filament}/<name>.json`, so
  the names above work; an absolute JSON path still passes through for a hand-edited profile.
- **`npm --prefix tools/bambu run bambu -- slice …` runs with cwd = `tools/bambu`**, so a *relative*
  STL path resolves against the wrong root (`no such file`). Pass the STL as an **absolute path**, or
  invoke `tools/bambu/bin/bambu` from the repo root.

Regression guard: [`scripts/slice-smoke.sh`](scripts/slice-smoke.sh) slices a given STL with the trio
*by name* and asserts the X2D gcode header — it fails if name-resolution ever breaks again.

## The rails (do not route around them)

- **Dispatch is owner-gated and fail-closed.** `print send` moves real hardware, and **printing is on
  hold until a `CAL-*` bet justifies a plate** (memory *owner-gated-and-on-hold*). It prints the
  owner-gate notice and refuses unless you pass `--yes` or confirm at a TTY. Use `--dry-run` to show
  exactly what it *would* do without connecting. Never pass `--yes` on the user's behalf — the first
  filament is Omar's call.
- **`slice` and `print send` share one honesty contract.** `slice plate` captures Studio's own
  warnings and writes a `<plate>.warnings.json` sidecar stamped with the sliced `.3mf`'s
  `source_sha256`; `print send` refuses to dispatch unless that sidecar is **present, fresh (hash
  matches the plate on disk), and free of unexpected warnings** — fail-closed on missing, stale, or
  legacy-no-hash alike (#52/#62). The fix is always to re-slice, never `--allow-unverified` (the loud,
  high-bar override). `validate plate` prints the freshness verdict without dispatching.
- **There is an active print on the machine** — status/discovery are passive and read-only by design;
  do not `print pause/stop` or otherwise interfere with a running job unless asked.
- **A record is a plate that came off a machine**, written by `print send --record` into the gitignored
  `.bambu/records/<date>-<slug>/` draft staging, then promoted to `docs/prints/<date>-<slug>/` once it
  ships. The prints gate is **whole-tree**, so an incomplete draft under `docs/prints/` blocks every
  commit — that is why drafts stage under `.bambu/` first. Fill the TODOs + photos, then
  `bambu validate record .bambu/records` before moving the dir.
- **A reading without a profile header is anecdote, not calibration.** Logging a print is not done at
  "measure" — it walks **print → photograph → measure → compare → verdict**, and the gate refuses a
  bet-settling reading with no `expected`/`verdict`. That loop is owned by
  [`prototype`](../prototype/SKILL.md); the bench sheet you carry to the printer is
  [`docs/prints/plate-1-bench-sheet.md`](../../../docs/prints/plate-1-bench-sheet.md).

## Where this fits

- **Bring-up not done yet?** The X2D is on the LAN but still cloud-bound; `status`/`send` need the
  transport, which needs LAN Mode + Developer Mode toggled at the touchscreen. That is
  [`setup-bambu-x2d`](../setup-bambu-x2d/SKILL.md) + memory *bambu-x2d-bringup*.
- **Deciding what to print next / logging what a plate taught?** That is the calibration workflow:
  [`prototype`](../prototype/SKILL.md) (the catalog + record loop) and
  [`calibrate`](../calibrate/protocol.md) (the `CAL-*` bets, registry
  [`bets.md`](../calibrate/bets.md)). Nothing has been printed yet — **21 bets, 0 measured** — so
  `print list` is honestly empty and Plate 1 (the machine card) is the keystone.
- **The whole campaign** — what to print, in what order, and why — is
  [`.claude/plans/binary-tickling-kay.md`](../../plans/binary-tickling-kay.md); the master backlog is
  [print register](../../../docs/tasks/coaster-pipeline/backlog.md).

## One-command discipline

Keep every call a single allow-listable command: no `cd … &&`, no gratuitous pipes, no heredoc
scripts. A variation belongs in the CLI as a flag (`--settings`, `--object`, `--json`), not in the
shell around it — that is the whole reason the CLI exists.
