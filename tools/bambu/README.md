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

> **Every flag, generated:** [`FLAGS.md`](FLAGS.md) lists every subcommand, argument and option,
> emitted from the CLI itself by `bambu dump-flags` (regenerate: `make bambu-flags`). Hook
> `45-bambu-flags` blocks a commit whose CLI surface moved without it, so the reference never
> drifts. The table below is the human map; `FLAGS.md` and `bambu <group> <verb> --help` are the
> authoritative, always-current detail.

| Group | Verbs | Backend |
|---|---|---|
| `setup` | `doctor`, `mcp`, `studio` | local checks |
| `status` | `show`, `monitor`, `camera` | griches MCP |
| `header` | `header` (`--plate <plate.3mf>`, `--json`) — auto-pull the bench-sheet profile header | first-party MQTT + `.3mf` |
| `slice` | `plate` (`--dry-run`, `--settings`/`--filament`, raw args after `--`), `open`, `compose` (`<plate.yaml>` → one sliced `.3mf`: renders each bikar item, bed-fit pre-check, writes `objects[].iteration`) | BambuStudio CLI + bikar |
| `print` | `send` (`--record`, `--dry-run`, `--yes`; needs a live page approval), `list` (`--shipped`/`--drafts`/`--json`), `pause`, `resume`, `stop` | griches MCP + prints gate |
| `validate` | `mesh` (bikar `--check`), `plate` (calibration §7), `record` (prints gate) | bikar / prints gate |

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
server's `env` in `.mcp.json`, else the repo's `.env`. The real `.mcp.json` is gitignored (it
carries the token); copy [`.mcp.json.example`](../../.mcp.json.example). `bambu setup mcp` prints
the block to add. The `.env` is checked in with dotenvx-encrypted values; bambu decrypts them with
the `DOTENV_PRIVATE_KEY` from the gitignored `.env.keys` beside it (or from the environment). With
no key, the printer keys stay unset rather than being passed on encrypted.

## Dispatch needs Omar's approval

`print send` moves real hardware, so it is fail-closed. It refuses unless the plate's page in
`docs/design/plates/` carries a live approval from Omar (D-093: his tick, or his yes in chat written onto
the page; one approval per send, spent by the send; a production plate has a standing approval
while its prints and recipe still hold, D-095) and the printer is idle; no flag skips either
check (`src/send-gate.ts`). Then it asks at a TTY; `--yes` skips only that question. A send that
goes through unticks the box, sets the page's stage to `sent` and adds a dated `sent` row to its
timeline. `--dry-run` shows what it would upload/start without connecting. `stop` confirms too;
`pause`/`resume` are reversible and immediate.

## Records & validation

`print send --record` scaffolds a draft print record under **`.bambu/records/<date>-<slug>/`** (a
gitignored staging area — a finished record lives at `docs/prints/<date>-<slug>/`). The scaffold
pins what a machine can know at dispatch time: the bikar HEAD and each `--object bikar:<path>`'s blob
sha256 (R1 provenance), leaving readings/photos/`self_ref` as `TODO` for the operator.

The prints gate is **whole-tree** — an incomplete draft under `docs/prints/` would block every
commit — which is exactly why drafts stage in the gitignored `.bambu/` tree instead. Fill the TODOs,
add photos, then check with `bambu validate record .bambu/records` before moving the dir into
`docs/prints/`. Every `validate` verb shells to the existing authority (bikar's `--check`,
`build/verify_machine_card.py`, `.claude/gates/prints_gate.py`) — one code path, never a second that
can disagree.

`print list` answers "what has this machine printed?" — and, with `--how`, "how did I print it?".
It reads **both** trees (shipped `docs/prints/` + draft `.bambu/records/`), newest first, tagging
each row's source. The default table shows the *what* (plate / status / objects / readings /
settles); `--how` swaps in the **process identity** — machine / material / nozzle / layer / profile
— so a plate can be reprinted from a number, not a memory. Four filters turn the list into a query:
`--settles <CAL-id>`, `--material`, `--machine` (substring, case-insensitive) and `--status`
(exact) — combined with AND, reporting "N of M" and distinguishing "no match" from the zero-record
baseline. `--shipped` / `--drafts` narrow the trees and `--json` emits the raw records (`how` and
all). It parses nothing itself: it shells to the same `prints_gate.py` (its read-only `--list`
projection, which slices the `how` from the record's nine-field profile), so the list and the gate
can never disagree about a record, and a record that does not parse is shown as broken rather than
hidden — even under a filter, since hiding a broken record is the one failure this verb exists to
avoid.

`print verdict <run> <entry> <keep|adjust|drop> [-n <note>]…` sets one printed piece's verdict in
`docs/prints/<run>/index.md` and adds notes under it. It edits the lines in place, so the diff is the
verdict line and the new notes, nothing else. It then reads the YAML back to check the edit landed.
It refuses an unknown piece (and names the ones there are), a verdict the prints gate would reject,
and a note with a line break. A note already there is not added twice, so a repeat changes nothing.
It only edits the file; committing it is up to the caller. The 3d-model-hub page calls it for
"enter a verdict".

## Logs

Structured, greppable, at `.bambu/bambu.log` (override with `BAMBU_LOG`); `BAMBU_VERBOSE=1` also
tees to stderr. Every subprocess/MCP call is timeout-bounded and bracketed with `ev=…` lines.
