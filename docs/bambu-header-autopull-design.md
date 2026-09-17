# Auto-pulling the print profile header from the printer

**Status:** design, grounded 2026-09-17 · **Grounded in:**
[`research/bambu-header-autopull-survey.md`](research/bambu-header-autopull-survey.md)
(field→source survey, real web fetch) · **Changes (design only, not implemented here):**
`tools/bambu` verbs, [`.claude/skills/bambu/SKILL.md`](../.claude/skills/bambu/SKILL.md),
[`.claude/skills/setup-bambu-x2d/SKILL.md`](../.claude/skills/setup-bambu-x2d/SKILL.md),
[`prints/plate-1-bench-sheet.md`](prints/plate-1-bench-sheet.md).

## Why this doc exists

The Plate-1 bench sheet opens with a **profile header** — machine / firmware / material / spool /
nozzle / layer height / profile / ambient / date / caliper — that the operator today **transcribes
by hand at the printer** ([`prints/plate-1-bench-sheet.md`](prints/plate-1-bench-sheet.md), the
"Profile header" block). Hand transcription is where a calibration reading quietly loses its
provenance: a mistyped nozzle diameter or a forgotten profile name turns a measurement into
anecdote, which is exactly the failure the sheet's own rule 2 warns against ("a reading without a
profile header is anecdote, not calibration").

But we already read most of that header off the machine. `status show` parses the pushall frame and
`filament` parses the AMS
(`3d-models:tools/bambu/src/backends/mqtt.ts:L246 "pushall"`,
`3d-models:tools/bambu/src/frame.ts:L26 "tray_type"`), and `slice` produces a `.3mf`
that stamps the machine, profile, layer height and slicer version. So the header is mostly a
**join** of things the CLI can already reach — not new hardware access. This doc says which fields
that join can fill, proposes the one verb that fills them, and — mirroring how
[`bambu-cli-design.md`](bambu-cli-design.md) isolates the X2D dual-nozzle risk — names the reads
that are H2-proxy-plausible but **not yet observed on this X2D** as a validation task, not an
assumption.

It does **not** implement the CLI — it is a design to review before code.

## The header, field by field

Source column: **frame** = the live MQTT pushall report; **get_version** = an `info`/`get_version`
MQTT round-trip we do not send today; **AMS** = `print.ams.ams[].tray[]`; **.3mf** = a key in the
sliced file (`Metadata/project_settings.config` or the plate G-code header); **slicer** =
`BambuStudio --version`; **clock** = the CLI's own time; **manual** = the printer cannot know it.
Confirmed column carries the survey's hedge verbatim.

| Header field | Machine source | Confirmed for the X2D? |
|---|---|---|
| Machine (preset name) | .3mf `printer_settings_id` + G-code `printer_model` | **confirmed-in-repo** (`printer_model = Bambu Lab X2D`, PR #189) |
| firmware | `setup discover` (SSDP) today; `get_version` `module[].sw_ver` richer | **value confirmed-in-repo** (`01.02.00.00`); get_version-over-MQTT **H2-proxy — unconfirmed** |
| Material — type | AMS `tray_type` | **confirmed-in-repo** (PR #192) |
| Material — colour | AMS `tray_color` (`RRGGBBAA` → `#RRGGBB`) | **confirmed-in-repo** (`#F5547C`) — hex, not a colour name |
| Material — brand | AMS `tray_sub_brands` + Bambu vendor from `tray_info_idx` | **confirmed for Bambu RFID spools**; third-party spool = **manual** |
| Spool id | AMS `tray_uuid` (Studio tray SN) | **H2-proxy — unconfirmed** (not seen 2026-09-17); Bambu-RFID only, else **manual** |
| Nozzle — diameter | .3mf `nozzle_diameter` (G-code `0.4,0.4`); frame `nozzle_diameter` as cross-check | **.3mf confirmed-in-repo**; frame field **H2-proxy — unconfirmed** |
| Nozzle — type | frame `nozzle_type` / accessory setting | **H2-proxy — unconfirmed** → best-effort machine, else **manual** |
| Layer height | .3mf `layer_height` / G-code header | **confirmed-in-repo** (0.2) |
| Profile (process+filament) | .3mf `print_settings_id` + `filament_settings_id` | **confirmed-in-repo** (the names `slice` resolves) |
| Slicer version | `BambuStudio --version`; .3mf `Application` / `X-BBL-Client-Version` | **confirmed-in-repo** (2.08.02.61) |
| settings changed from profile | — | **manual** (operator's intent, not a raw setting diff) |
| Ambient — room temp | — (`chamber_temper` is chamber, not room) | **manual**; chamber offered as a **labelled proxy** only |
| Ambient — enclosure open/closed | — (no reliable door-state field found) | **manual** |
| Date | clock (UTC now) | machine-trivial |
| Caliper make / resolution / zeroed | — | **manual** (operator's instrument) |

**The tally the CLI acts on.** Nine fields are machine-read outright (machine, firmware value, type,
colour, nozzle diameter, layer height, profile, slicer version, date); two more (brand, spool id)
are machine-read for official Bambu RFID spools and manual otherwise; nozzle type is best-effort;
and five are genuinely manual (settings-changed narration, ambient room temp, enclosure state, and
the three caliper sub-fields). So the verb below **fills nine-to-twelve of sixteen** and leaves the
operator a short, honest set of blanks — not a whole block to copy.

**Read against itself (K7).** Chamber temp appears twice above — as a machine-read frame field
(`3d-models:tools/bambu/src/commands/status.ts:L47 "chamber_temper"`, already surfaced) and as a
field the header must **not** auto-fill into "ambient room temp." Both are true and they do not
conflict: the frame gives chamber; the header wants room; the verb prints chamber on its own labelled
line and leaves the room blank. The table's `nozzle_diameter` row is likewise consistent with the
verb: the `.3mf` value is authoritative and filled; the frame value is a cross-check and, until
observed on the X2D, is not what the header prints.

## The CLI change — a new `bambu header` verb

**Recommendation: a new top-level read-only verb, `bambu header`.** It connects over the same
first-party MQTT path `status`/`filament` already use (subscribe report, publish `pushall`, read the
cached `print` frame), optionally reads a sliced plate with `--plate <file.3mf>`, and prints the
bench-sheet header block with every machine-known field filled and each genuinely-manual field left
as a labelled blank.

```
bambu header [--plate <file.3mf>] [--json]
```

- Without `--plate`: fills the **printer-side** fields (firmware, material type/colour/brand,
  nozzle, chamber-as-proxy, date) and marks the **slice-side** fields (machine, layer height,
  profile, slicer version) `TODO — pass --plate`.
- With `--plate`: also fills machine / layer height / profile / slicer version from the `.3mf`, and
  cross-checks the frame's `nozzle_diameter` against the `.3mf`'s, flagging a mismatch (the loaded
  nozzle is not the sliced-for nozzle — a real bench error worth catching).
- `--json`: the same fields as a machine object (for `print send --record` to consume; see below).
- Manual fields are printed as the exact blanks the paper sheet uses (`Ambient room ~____°C`,
  `enclosure: open / closed`, the caliper line) so the printed output *is* the header, not a second
  format to reconcile.

**Why this shape.** A header is precisely the **join of two sources neither existing verb owns**:
`status`/`filament` see the printer but not the slice; `slice` produces the `.3mf` but never talks
to the printer. `header` is the one verb positioned to read both, it is **read-only and safe to run
now** (like `status`/`filament`, and unlike the owner-gated `print send`), and it keeps every call a
single allow-listable command that emits the operator's artifact directly.

**One code path, reused — not forked (the repo's D-052 tenet).** `header --json` is the builder;
`print send --record`
(`3d-models:tools/bambu/src/commands/print.ts:L311 "--record"`) calls **the same builder** to
pre-fill the record's profile header instead of scaffolding it as TODO. The header logic lives in
one place; the two entry points differ only in destination (stdout vs the record file), never in
what a field means.

**Runner-up: fold it into `print send --record`'s scaffold.** The record already captures the
process identity (machine / material / nozzle / layer / profile), so the builder could live only
there. Rejected as the *primary* home because the operator needs the header **at the bench, before
dispatch** — and dispatch is owner-gated and on hold until a CAL bet settles, so a header reachable
only through `print send` is a header you cannot get when you actually fill the sheet. `header` is
the front door; `--record` reuses it. **Second runner-up: `status show --header`** — rejected
because `status` is printer-only and "proves transport," and giving it a `--plate` file argument
muddies that role; the join belongs in its own verb, not bolted onto status.

## Skill and bench-sheet updates

- **[`prints/plate-1-bench-sheet.md`](prints/plate-1-bench-sheet.md)** — the "Profile header" block
  changes from *fill every line by hand* to *run `bambu header --plate <plate.3mf>`, paste its
  output, then complete only the blanks it left* (ambient room temp, enclosure, caliper, and any
  settings you changed). The pre-flight table that today lists the known-good trio becomes the
  **input** to `--plate` (you slice with that trio, then `header` reads the trio back out of the
  `.3mf`, so the sheet and the file cannot silently disagree). The rule "a reading without a profile
  header is anecdote" is unchanged — the verb makes obeying it cheaper, not optional.
- **[`.claude/skills/bambu/SKILL.md`](../.claude/skills/bambu/SKILL.md)** — add `header` to the verb
  map as **read-only, safe now** (beside `status`/`filament`/`print list`), with the one-line usage
  and the note that manual fields remain the operator's to fill.
- **[`.claude/skills/setup-bambu-x2d/SKILL.md`](../.claude/skills/setup-bambu-x2d/SKILL.md)** — in
  the read-only-before-write step, mention `header` as the second read-only proof (after
  `status show`) and the bench-sheet's filler, so a first-time setup learns it before first dispatch.

## The one unproven thing — a validation observation, not an assumption

Mirroring [`bambu-cli-design.md`](bambu-cli-design.md)'s isolation of X2D dual-nozzle: three reads
this verb wants are **H2-proxy-plausible but not yet observed on this X2D's frame**, and the design
writes them **unconfirmed** until `bambu header` is run against the live machine and the raw frame
inspected:

1. the **MQTT `info`/`get_version`** round-trip and its `module[].sw_ver` shape (firmware value is
   already confirmed via SSDP `setup discover`; only the MQTT route is unproven);
2. **`nozzle_diameter`** / **`nozzle_type`** in *this* machine's pushall frame (only the `.3mf`
   values are confirmed today — the `.3mf` is the authoritative source regardless, so this is a
   cross-check, not a blocker);
3. **`tray_uuid`** (spool id) on the X2D AMS tray, and **which chamber field** the X2D reports
   (flat `chamber_temper`
   `3d-models:tools/bambu/src/commands/status.ts:L47 "chamber_temper"` vs a nested `device.ctc`).

The transfer sentence, stated (K10): the X2D shares the H2D's `01.02.00.00` firmware track and the
AMS report shape confirmed here on 2026-09-17, so these fields are plausible — but the frame has
**already diverged once** on this machine (`vir_slot` array vs the H2 `vt_tray` object,
`3d-models:tools/bambu/src/frame.ts:L68 "vir_slot"`), so "plausible" is not
"observed." Until the observation, `header` prints these three as `unconfirmed` (or omits them and
falls back to the `.3mf`/SSDP source), never as filled machine truth.

**Validator:** `bambu header` fills a field only from a source that actually carried it, and never
prints a genuinely-manual field as machine-known.
- PASS: with a live frame that carries `tray_type`/`tray_color` and a `--plate` whose
  `printer_settings_id` is an X2D preset, the output fills material type/colour and machine/profile,
  and leaves `Ambient room ~____°C`, `enclosure: open / closed` and the caliper line as blanks.
- FAIL: the frame is missing `nozzle_diameter` (the X2D-unconfirmed case) yet the header prints a
  nozzle diameter with no `--plate` to source it from — i.e. it **fabricates** an unobserved field
  instead of marking it `unconfirmed`. This is the by-design failure the verb must not commit:
  filling a blank the machine did not answer is worse than leaving it blank, because a fabricated
  header reads as ground truth on the bench sheet.

## Cross-links

- Survey / provenance: [`research/bambu-header-autopull-survey.md`](research/bambu-header-autopull-survey.md)
- The sheet this fills: [`prints/plate-1-bench-sheet.md`](prints/plate-1-bench-sheet.md)
- Transport + slice design this extends: [`bambu-cli-design.md`](bambu-cli-design.md)
- CLI reference: [`../tools/bambu/README.md`](../tools/bambu/README.md) · status
  [`../tools/bambu/src/commands/status.ts`](../tools/bambu/src/commands/status.ts) · filament
  [`../tools/bambu/src/commands/filament.ts`](../tools/bambu/src/commands/filament.ts) · records
  [`../tools/bambu/src/commands/print.ts`](../tools/bambu/src/commands/print.ts)
- Skills: [`../.claude/skills/bambu/SKILL.md`](../.claude/skills/bambu/SKILL.md) ·
  [`../.claude/skills/setup-bambu-x2d/SKILL.md`](../.claude/skills/setup-bambu-x2d/SKILL.md)
- Live-machine facts: memory `bambu-x2d-bringup`
