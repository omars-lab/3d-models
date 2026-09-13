# `tools/bambu` — Bambu X2D CLI

Contextualized CLI companion to the `setup-bambu-x2d` skill (built in a later phase — see
[`.claude/plans/binary-tickling-kay.md`](../../.claude/plans/binary-tickling-kay.md)). It encodes
*how we print* — our verbs over the community transport — so a call site stays a single,
allow-listable command instead of hand-assembled MCP pokes.

## Layers

```
tools/bambu (our verbs, --help)      ← you are here
  → griches MCP  (control/status/upload/AMS/camera transport)
  → BambuStudio CLI (headless slicing)
  → AppleScript (GUI-only actions: Bambu Connect, some Studio dialogs)
Bambu firmware (MQTT 8883 / FTPS 990 / X.509) — full control needs Developer Mode ON
```

The router (`src/backends/router.ts`) picks the cheapest capable backend, GUI last.

## Command groups

| Group | Verbs | Backend |
|---|---|---|
| `setup` | `doctor`, `mcp`, `studio` | local checks |
| `status` | `show`, `monitor`, `camera` | griches MCP |
| `slice` | `plate` (`--dry-run`, `--settings`/`--filament`, raw args after `--`) | BambuStudio CLI |
| `print` | `send --record`, `pause`, `resume`, `stop` *(phase 3, owner-gated)* | griches MCP |
| `validate` | `mesh`, `plate`, `record` *(phase 3)* | bikar / prints gate |

`bambu <group> <verb> --help` everywhere — the help *is* the documentation.

## Run

```bash
export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"   # repo-pinned Node
cd tools/bambu && npm install
npx tsx src/index.ts setup doctor        # or: ./bin/bambu setup doctor
```

## Config

Reads the SAME env block the MCP reads, so the CLI and the MCP never disagree about the printer:
`PRINTER_HOST`, `BAMBU_SERIAL`, `BAMBU_TOKEN`, `BAMBU_MODEL` — from process env, else the `bambu`
server's `env` in `.mcp.json`. The real `.mcp.json` is gitignored (it carries the token); copy
[`.mcp.json.example`](../../.mcp.json.example). `bambu setup mcp` prints the block to add.

## Logs

Structured, greppable, at `.bambu/bambu.log` (override with `BAMBU_LOG`); `BAMBU_VERBOSE=1` also
tees to stderr. Every subprocess/MCP call is timeout-bounded and bracketed with `ev=…` lines.
