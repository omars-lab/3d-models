---
date: 2026-10-03
produced-by: researcher A (Claude Opus 5.5) — WebSearch, WebFetch, `gh` (code search, PR diffs, file contents) and `curl` of raw source files from GitHub. Web and source research only; the printer was not contacted (no MQTT, no FTPS, no sends).
feeds:
  - '[[first-party-dispatch]]'
---

# How a print reaches an X2D with no card in — sources and options (researcher A)

The question. Our Bambu Lab X2D has nothing in its external slot. Bambu Studio still prints to
it over the LAN; our CLI (`tools/bambu`) cannot, because its FTPS `STOR` at the root came back
`553 Could not create file` and `LIST /` came back empty. The status frame says `sdcard: false`,
`tl_external_*` 0/0 and `tl_internal_free_kb` 884486 of 962560. This file answers:

1. How Studio, Handy or the cloud gets a print onto an X2D, H2D, X1 or P2S with no card: which
   transport, and where the file lands.
2. Whether a third-party LAN client can upload to the built-in storage and start the print from
   there: path, port, protocol and the `project_file` url.
3. Known firmware facts.
4. Realistic options for us, with pros, cons and implications.

It feeds [`../issues/first-party-dispatch.md`](../issues/first-party-dispatch.md), whose
2026-10-03 section records the 553. The code it is about is
[`../../tools/bambu/src/backends/ftps.ts`](../../tools/bambu/src/backends/ftps.ts) and
[`../../tools/bambu/src/storage.ts`](../../tools/bambu/src/storage.ts).

Every source below is marked **fetched** (I read the text) or **snippet** (I only saw a search
result summary; treat it as a lead, not a fact). Quotes are verbatim and short. This covers the
sources listed here and nothing else; it is not a survey of every Bambu client.

## The short answer

- **Q1.** On the H2 series, P2S and X2D, Studio's **Print** button does not use FTPS. It
  uploads the sliced `.gcode.3mf` over a separate TLS service on **TCP port 6000** (Bambu's
  "BambuTunnelLocal" file-transfer protocol, inside the closed `libbambu_networking` plugin)
  into the printer's built-in eMMC, then starts it with MQTT `project_file` and
  `url: "brtc://emmc/<name>"`. On the X2D the file lands in `/userdata/model/history/<name>`.
  FTPS on port 990 serves only external storage (card or USB stick), which is why our `STOR`
  got 553 with nothing inserted. Older models (X1 series, the "N7"-class P1/A1 boards) use FTPS
  plus `ftp://`.
- **Q2.** Yes, in principle, and one open-source project has done it: open-bamboo-networking
  (an AGPL replacement for Bambu's plugin) implements the port 6000 upload plus `brtc://emmc/`
  start and marks it working, **tested on a P2S**. Its notes include X2D-specific observations
  (chunk size, landing path, ability reply) but no claim of a full X2D print through its own
  code. One other client (bambu-printer-mcp) reached an X2D print by loading Bambu's own closed
  plugin on macOS. None of ha-bambulab, bambulabs_api, bambu-farm or OpenBambuAPI's docs ship
  an X2D eMMC upload; bambuddy tracks it as an open issue.
- **The X2D has no microSD slot.** Its external storage is a **USB stick**. The MQTT field is
  still called `sdcard` for history. So "just put in a microSD card" means "put in a USB stick".

## Raw findings

### 1. What storage the X2D has

**1.1 Retailer spec sheet (fetched)** — <https://shop3duniverse.com/products/bambu-lab-x2d>
(the bambulab.com spec page returned HTTP 403 to WebFetch, so this is the stand-in).
> "Built-in 8 GB EMMC and USB Port"

**1.2 Bambu forum, X2D thread 250906 (fetched)** —
<https://forum.bambulab.com/t/bambu-studio-cant-access-storage-on-x2d/250906> (user posts, not staff). The X2D "has a
USB stick slot (upper left)"; browsing the printer's storage from Studio was not yet supported
when the thread was written (April 2026).

**1.3 Bambu wiki, H2 USB requirements (snippet)** — the H2 manual's USB page (WebFetch returned
HTTP 402). Search snippet: USB 2.0 or above, FAT32 or exFAT, one drive at a time. Whether the
X2D page says the same was not read.

**1.4 Threads post by toddanglin (snippet)** — the H2D has 8 GB built-in plus a USB port. Lead
only.

### 2. Bambu Studio's own source (the open part)

**2.1 `bambu_networking.hpp` (fetched, via `gh search code`, file saved locally)** —
<https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/Utils/bambu_networking.hpp>.
`PrintParams` carries the switch that picks the eMMC route:
> `bool try_emmc_print;`

alongside `ftp_folder` and `dst_file`. The upload itself happens inside the closed plugin, not
in Studio's open code.

**2.2 `DeviceManager.cpp` (fetched, code search)** —
<https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/DeviceManager.cpp>.
> `is_support_print_with_emmc = get_flag_bits_no_border(fun2, 0) == 1`

so the printer advertises the eMMC print route in bit 0 of the `fun2` field of its status.

**2.3 OrcaSlicer `DeviceManager` (fetched, code search)** —
<https://github.com/OrcaSlicer/OrcaSlicer/blob/main/src/slic3r/GUI/DeviceManager.cpp>.
> `is_support_brtc = get_flag_bits(fun, 31)` with the comment "support tcp and upload protocol"

used by `SendToPrinter.cpp` to choose the port 6000 (`ft_*`) route for Send to Printer.

**2.4 BambuStudio PR #12146 (fetched, `gh pr diff`)** —
<https://github.com/bambulab/BambuStudio/pull/12146>, by maziggy (bambuddy's author),
2026-09-07, **open, not merged**. It changes
> `params.try_emmc_print = this->could_emmc_print;`

to also require a new `use_emmc_storage` setting. Its code comment describes what an eMMC print
leaves behind: a file
> "that Bambu Handy cannot list, that no FTP client on the network can read, and that the printer's own screen will not offer for a reprint"

and says firmware answers the storage-ability query with "emmc" ahead of "udisk". The PR text:
> "H2C/H2D use `brtc://emmc/` transport while X1C uses `ftp://`"

Reading of 2.1–2.4 together, with `PrintJob.cpp` (fetched, code search,
<https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/Jobs/PrintJob.cpp>): on
LAN, Studio calls `start_local_print` when the printer has a card **or** can print from eMMC,
and it sets `try_emmc_print` from the `fun2` bit. That is why
Studio still prints with `sdcard: false`.

**2.5 BambuStudio issue #10481 (fetched)** —
<https://github.com/bambulab/BambuStudio/issues/10481>, 2026-04-30, open, assigned to a Bambu
developer. Title: "By default send files to External storage instead of cache when USB flash
drive is connected". The report says the **Print** button sends to the internal cache (eMMC)
even with a USB drive in, and Bambu Handy can only see and print files on external storage. No
staff reply was visible.

### 3. The port 6000 wire and the print-start url — ClusterM/open-bamboo-networking

<https://github.com/ClusterM/open-bamboo-networking> — AGPL-3.0, an open-source drop-in for
Bambu's closed `libbambu_networking` plugin, 552 stars, last pushed 2026-09-30. All files below
were **fetched** with `curl` from the raw GitHub URLs.

**3.1 `research/06.04-port-6000.md` (fetched)** —
<https://raw.githubusercontent.com/ClusterM/open-bamboo-networking/master/research/06.04-port-6000.md>. Scope, with its own hedge:
> "reverse-engineered on **P2S**, May 2026; likely shared across models that expose `bambu:///local/...:6000`"

It is the same wire for the file browser and for the `ft_*` model upload. What it documents:

- Implicit TLS on TCP 6000; the printer's leaf certificate has `CN=<serial>`.
- Login frame: a 16-byte header (payload length, magic, sequence, reserved; little-endian),
  then 16 bytes: `bblp` NUL-padded to 8, the LAN access code NUL-padded to 8. Magic
  `0x0101013f` for login, `0x0102013f` for control frames sent to the printer, `0x0002013f`
  for the printer's replies.
- A setup message, then JSON RPCs `{"mtype":12289,"cmdtype":N,"sequence":S,"req":{..}}`.
  Commands: 1 list, 2 subscribe, 3 delete, 4 download, **5 upload**, 7 storage ability.
- Upload (cmdtype 5): an init request with `"type":"model","storage":"emmc","path":"<name>.gcode.3mf","total":<bytes>`;
  the printer answers `result:1` with `chunk_size` in KiB; the client then sends every chunk
  back to back (`{"frag_id":i,"offset":..,"size":..}`, a blank line, the bytes), the last one
  carrying a lowercase `file_md5`; one final `result:0` reply follows. Waiting for a per-chunk
  reply breaks it:
  > "Waiting for an ACK after chunk 0 on files **> 255 KiB** yields `result:-9203` on the first chunk reply"
- X2D specifics, firmware `01.02.00.00`:
  > "the **X2D** (`01.02.00.00`) returns **255** on `:6000` and **31** ... when the same job arrives over TUTK"

  > "On the X2D a `storage:"emmc"` upload lands in **`/userdata/model/history/<path>`**"

  and the X2D's ability reply lists `"storage":["emmc","udisk"]` and
  `"upload_storage":["emmc","udisk"]`.
- On the url:
  > "The label selects *where the file is written*; the print-start `url` scheme ... later selects *how firmware locates* it — typically `brtc://emmc/<name>` after a cache-resident Send-to-Printer job (firmware may still search udisk then emmc)."

**3.2 `research/08.08-print-abi.md` (fetched)** —
<https://raw.githubusercontent.com/ClusterM/open-bamboo-networking/master/research/08.08-print-abi.md>. The transport table row for Studio's LAN print:
> "`start_local_print` | none | Full `.3mf` over **TLS `:6000` (brtc)** | LAN MQTT `project_file` with `brtc://emmc/<name>` — only honest LAN path"

On FTPS, from a capture of a Send to Printer session (19 packets on 990, 220 on 6000):
> "**FTPS is a short side trip, not the upload transport** for brtc Send-to-Printer — do not `STOR` the full `.3mf` on :990 when `:6000` works."

On the url schemes:
> "`brtc://emmc/` = search both caches; `ftp://` = FTPS volume; `file://` = fixed path"

On encryption:
> "Non-Developer-Mode firmware requires `url_enc`; Developer Mode accepts plain `url`."

On `md5`: stock plugins always send the literal `"from_sd_card"`, never a real hash:
> "A real file hash never appeared in any captured LAN `project_file`."

(Our CLI sends `md5: ""`. Not shown to matter, but it differs from stock.)

On the cloud: the cloud-recorded print (`start_local_print_with_record`) has the printer
"re-download from S3", and
> "Cloud-dispatched project URLs appear limited to `https://…` and `ftp://…` (not `brtc://`)."

**3.3 `STATUS.md` (fetched)** —
<https://raw.githubusercontent.com/ClusterM/open-bamboo-networking/master/STATUS.md>.
> "`bambu_network_start_local_print` | ✅ | LAN-only: `:6000` emmc upload + `brtc://emmc/` MQTT when `try_emmc_print`; else FTPS + `ftp://` (N7)."

> "Print-start MQTT uses `brtc://emmc/<name>` after emmc cache upload (P2S), `ftp://` after FTPS (N7), or `file:///` for print-from-device."

Developer Mode is read from bit 29 of `print.fun` (clear means Developer Mode on). The repo
also ships Python tools, `bambu6000_client.py` and a REPL with `/upload <file> emmc`.

### 4. bambuddy (maziggy/bambuddy)

**4.1 Troubleshooting wiki (fetched, twice)** — <https://wiki.bambuddy.cool/reference/troubleshooting/>. The first WebFetch summary claimed Bambuddy can
print with no card. That was the summarizer's mistake; the verbatim re-fetch says the opposite:
> "Bambuddy requires an SD card in your printer for: Starting prints from Bambuddy..."

> "On H2-series, P2S and X2D, Bambu Studio puts the sliced file on the printer's internal storage instead, uploading over a separate service on port 6000."

> "On every Bambu model that port serves external storage only — the SD card or USB stick."

> "The X2D behaves like the H2 series"

and OrcaSlicer "will refuse to send with an empty slot — 'storage needs to be inserted before
printing via lan'". Bambuddy can list internal storage over port 6000, "but the firmware refuses
to serve those files back".

**4.2 `backend/app/services/print_storage.py` (fetched)** —
<https://raw.githubusercontent.com/maziggy/bambuddy/main/backend/app/services/print_storage.py>. Module docstring:
> "H2-series, P2S and X2D firmware default to keeping the sliced file on internal eMMC instead, and BambuStudio uploads there over a separate service on port 6000 (the "BambuTunnelLocal" protocol -- see #2762, which tracks implementing it)."

> "``ftp://<name>`` for external storage and ``brtc://emmc/<name>`` for internal."

It also records an H2D (firmware 01.03.00.00, card in) where `brtc://emmc/` jobs were readable
over FTPS under `/cache/<name>`, while on a P2S and H2C "the same URL really did mean nothing was
there".

**4.3 Issue #2762 (fetched)** — <https://github.com/maziggy/bambuddy/issues/2762>, open since 2026-08-04; tracks uploading over the port 6000
tunnel, which "would remove the card requirement". Not implemented.

**4.4 Issue #3126 (fetched)** — <https://github.com/maziggy/bambuddy/issues/3126>, an X2D on firmware 01.02.00.00 with Studio 2.8.2.61; it is the
report behind "the X2D behaves like the H2 series". It is about archiving, not uploading.

### 5. bambu-printer-mcp (DMontgomery40/bambu-printer-mcp)

<https://github.com/DMontgomery40/bambu-printer-mcp> — a Node MCP server that uses basic-ftp,
like our CLI. **Fetched**: `CHANGELOG.md`, `README.md`,
`SLICING.md`, the native helper source, PR #10 and PR #15.

**5.1 The FTPS session-reuse fix (CHANGELOG, fetched)** —
<https://raw.githubusercontent.com/DMontgomery40/bambu-printer-mcp/main/CHANGELOG.md>.
> "basic-ftp wraps each data socket without a host, so Node can bind its resumable session to `localhost` instead of the printer host and printers requiring TLS session reuse replied `522 SSL connection failed: session reuse required` to every LIST, STOR and RETR. The contributor verifies successful upload, size check, and deletion on physical X2D USB storage; internal eMMC still refuses FTPS writes with `553`. Printing remains a separate check."

Our `ftps.ts` passes `secureOptions: { rejectUnauthorized: false }` and no host, so it has the
same shape. It has not hit the 522 yet only because nothing got past the 553.

**5.2 PR #10 by VailElla (fetched, merged 2026-09-29)** —
<https://github.com/DMontgomery40/bambu-printer-mcp/pull/10>. "X2D rejects the legacy FTPS upload
route." The fix is a macOS-only native helper that `dlopen`s Bambu's own
`libbambu_networking.dylib` (preferring the copy inside Bambu Connect.app) and calls
`bambu_network_start_local_print` with `try_emmc_print=true` and `connection_type="lan"`,
after installing the device certificate so the plugin can encrypt `project_file`. The PR says
earlier X2D hardware testing reached `RUNNING`; the merged revision "makes no claim of a new
physical print".

**5.3 README (fetched).** "Legacy FTPS and remote G-code starts remain unsupported for X2D."
For H2/P2S it uses FTPS to `/cache/` with `url ftp:///cache/<name>`
(<https://github.com/DMontgomery40/bambu-printer-mcp/pull/15>).

### 6. ha-bambulab / pybambu (greghesp/ha-bambulab)

**6.1 `models.py` (fetched)** —
<https://raw.githubusercontent.com/greghesp/ha-bambulab/main/custom_components/bambu_lab/pybambu/models.py>. Uploads go only over FTPS (`storbinary_no_unwrap` `STOR`). It
fires `event_printer_missing_sdcard` when there is no card.

**6.2 `media_sources.py` (fetched)** —
<https://raw.githubusercontent.com/greghesp/ha-bambulab/main/custom_components/bambu_lab/pybambu/media_sources.py>. A `Tcp6000MediaSource` that logs in, asks for the storage
ability, lists and downloads over port 6000. **No upload.** Its framing is an independent
implementation and matches open-bamboo-networking's exactly: `MAGIC_LOGIN = 0x0101013F`,
`MAGIC_CTRL = 0x0102013F`, a 16-byte header (length, magic, sequence), and a login payload of
`bblp` and the access code each `ljust(8, b"\0")`.

### 7. OpenBambuAPI (Doridian/OpenBambuAPI)

**7.1 `ftp.md` (fetched)** — <https://raw.githubusercontent.com/Doridian/OpenBambuAPI/main/ftp.md>. FTPS on 990, implicit TLS, user `bblp`. Nothing on internal storage.

**7.2 `lan-file-tunnel.md` (fetched)** —
<https://raw.githubusercontent.com/Doridian/OpenBambuAPI/main/lan-file-tunnel.md>. Describes port 6000 with the same command numbers
(5 is `FILE_UPLOAD`), but its framing **disagrees** with sections 3 and 6: a 64-byte auth packet
(`bblp` in 8 bytes, the access code zero-padded to 32, 24 reserved) and a header ordered
size / sequence / cmdtype / mtype. It notes `LIST_INFO` "appears to have been retired" on H2S
firmware 01.02.00.00.

### 8. bambulabs_api and bambu-farm

**8.1 bambulabs_api (code search, fetched).** A search for "emmc" in the repo found nothing.
Our earlier survey ([`bambu-control-transport-survey.md`](bambu-control-transport-survey.md))
already records it as FTPS-only.

**8.2 TFyre/bambu-farm (fetched)** —
<https://raw.githubusercontent.com/TFyre/bambu-farm/HEAD/bambu/src/main/java/com/tfyre/bambu/printer/BambuPrinterImpl.java>. Card-only: `project_file` with
`setUrl("file:///sdcard/%s")` and `setMd5("")`, and `gcode_file` with `/sdcard/<name>`. No
eMMC route.

### 9. Bambu forum, H2D (fetched)

<https://forum.bambulab.com/t/unable-to-send-sliced-file-to-h2d-without-a-usb-drive-connected/234923> (user JonRaymond, not staff):
> "If you 'Print Plate' it will transfer the file to the internal storage and start the print"

while Send goes to external storage; later firmware offers Internal or External on Send.

### 10. Not reached

- The Bambu wiki pages on the internal cache and on USB drives returned HTTP 402 to WebFetch
  (snippets only).
- bambulab.com's X2D spec page returned HTTP 403.
- No source covered **Bambu Handy** sending a new print to a cardless printer. Issue #10481 and
  PR #12146 only say Handy cannot see eMMC files.

## Firmware facts (Q3), each with its weakest link

| Fact | Source | Strength |
|---|---|---|
| X2D storage is 8 GB eMMC plus a USB port; no microSD | 1.1, 1.2 | retailer spec (fetched) + user posts |
| FTPS on 990 serves only external storage on every model | 4.1, 4.2 | bambuddy, fetched; matches our 553 |
| X2D eMMC refuses FTPS writes with 553 | 5.1 | a contributor's X2D, fetched; matches ours |
| X2D FTPS works on a USB stick once session reuse is fixed | 5.1 | one contributor's X2D; **printing from it not checked** |
| Studio's Print uses port 6000 + `brtc://emmc/` on H2/P2S/X2D | 2.4, 3.2, 4.1 | three independent sources agree |
| X2D eMMC upload lands in `/userdata/model/history/` | 3.1 | open-bamboo-networking only, firmware 01.02.00.00 |
| X2D chunk size 255 KiB on port 6000 | 3.1 | open-bamboo-networking only |
| eMMC route advertised by `fun2` bit 0; port 6000 upload by `fun` bit 31 | 2.2, 2.3 | Studio and Orca source |
| Developer Mode accepts a plain `url`; otherwise `url_enc` is required | 3.2 | open-bamboo-networking, captured on a P2S/N7 |
| Firmware without Developer Mode raises HMS 0500-0500-0001-0007 on unsigned MQTT | bambu-printer-mcp CHANGELOG (fetched) | reported on a P1S, firmware 01.08.05+ |
| `LIST_INFO` retired on H2S firmware 01.02.00.00 | 7.2 | OpenBambuAPI only |

## Where the sources disagree, and the hedges that must travel

- **Port 6000 framing.** OpenBambuAPI (7.2) disagrees with open-bamboo-networking (3.1). Two
  independent code bases that actually talk to printers (open-bamboo-networking and ha-bambulab,
  section 6.2) use the same 16-byte header and 16-byte login. I would build on that and treat
  OpenBambuAPI's page as wrong or describing another firmware.
- **"Tested on X2D" is narrower than it looks.** open-bamboo-networking's full upload-and-start
  is marked working on a **P2S**. For the X2D it reports the chunk size, the landing path and
  the ability reply, and its camera and file-browser rows say X2D was tested; I found no line
  saying its own `start_local_print` ran a print on an X2D.
- **Where an eMMC job can be read back over FTPS varies by model.** It was readable under
  `/cache/` on one H2D with a card in, and not on a P2S or H2C (4.2). Do not assume either way on
  the X2D.
- **The bambuddy summary.** Discussed in 4.1: the first summary was wrong, the verbatim text
  says a card or stick is required. Only the verbatim text is used here.
- **No firmware version is known** for when the X2D started defaulting to eMMC (vena/bambino
  issue #381, <https://github.com/vena/bambino/issues/381>, fetched: "No firmware version is known"). Ours behaves that way now.

## Design notes

What our CLI needs is a way to put a sliced `.gcode.3mf` somewhere the X2D will print it from,
over the LAN, with no Bambu Studio. These are the options the sources support.

### Option A — put a USB stick in, keep FTPS + `ftp:///`

Insert a FAT32 or exFAT USB stick (not a microSD card; the X2D has no microSD slot). Keep the
current upload and start. Fix the basic-ftp session-reuse bug in
[`ftps.ts`](../../tools/bambu/src/backends/ftps.ts) at the same time by passing the printer host
in the TLS options, and rename "card" to "external storage" in
[`storage.ts`](../../tools/bambu/src/storage.ts) and its messages.

- **Pros.** Smallest change; the code path already exists. Another basic-ftp client has
  uploaded to X2D USB storage (5.1). FTPS is documented and stable across models. Files on the
  stick show up in Handy and on the printer's screen for a reprint, which eMMC files do not
  (2.4, 2.5).
- **Cons.** Needs a physical stick and a person to insert it. The session-reuse fix is likely
  needed before even the upload works. Nobody I found has confirmed an X2D **print start** from
  `ftp:///` on a stick; bambu-printer-mcp says "Printing remains a separate check", and
  bambuddy's "needs a card or stick" implies it but does not show it. The printer's
  `tl_external_*` will then count against a stick that wears with use.
- **Implications.** Our refusal on `sdcard: false` stays correct and just needs plain wording
  ("no USB stick in"). The next decision is whether to go on to option B; A does not close it.
  It also commits us to keeping the stick in, and anything else that writes to it (timelapses)
  shares the space.

### Option B — our own port 6000 client: upload to eMMC, start with `brtc://emmc/`

Implement the port 6000 login, ability query (cmdtype 7) and upload (cmdtype 5, `storage:"emmc"`)
in TypeScript inside `tools/bambu`, then publish `project_file` with
`url: "brtc://emmc/<name>.gcode.3mf"` (plain `url` is accepted in Developer Mode; send
`md5: "from_sd_card"` as stock does).

- **Pros.** No hardware change; matches what Studio does on this printer, so it is the route the
  firmware is built around. Removes the card requirement for good. The wire is documented in
  detail, and two independent clients agree on the framing (3.1, 6.2).
- **Cons.** Reverse-engineered, undocumented by Bambu, and can change with firmware. The upload
  is fussy (pipelined chunks, one final reply, `-9203` otherwise). Proven end-to-end only on a
  P2S. open-bamboo-networking is AGPL, so we must write it from the documented behavior, not
  copy its code. eMMC files are invisible to Handy and the printer's reprint list (2.4).
- **Implications.** A new backend and new failure modes to map into plain messages. It needs a
  first send on our X2D to verify, which falls under the one-approval-per-send rule. If it
  works, `storage.ts` should report eMMC as reachable and stop refusing on `sdcard: false`. If
  Bambu turns on signing for this path, Developer Mode becomes a hard requirement.

### Option C — call Bambu's own plugin (as bambu-printer-mcp does)

Load `libbambu_networking.dylib` from an installed Bambu Studio or Bambu Connect and call
`bambu_network_start_local_print` with `try_emmc_print=true`.

- **Pros.** Uses Bambu's own code for the upload, so wire details are not ours to get right. One
  project reports an X2D reaching `RUNNING` this way (5.2).
- **Cons.** Native helper code, macOS only, tied to a closed binary whose interface changes
  between versions; needs the device certificate step. Hard to test and to explain when it
  fails.
- **Implications.** Couples the CLI to whatever Studio or Connect version is installed on the
  machine, which our [first-party dispatch](../issues/first-party-dispatch.md) work set out to
  avoid.

### Option D — keep sending from Bambu Studio

- **Pros.** Works today; it is how minis-01 and minis-02 printed.
- **Cons.** Not a CLI path; no approval record or send checks run.
- **Implications.** The issue doc rules this out as a workaround for Omar ("Never work around it
  by sending from Bambu Studio for Omar"); Omar may still choose it himself.

### Option E — cloud print

- **Pros.** None for us.
- **Cons.** The printer is in LAN mode, and cloud-dispatched urls do not use `brtc://` (3.2).
- **Implications.** Off the table while the printer stays in LAN mode.

### Side by side

| Option | Verifies before we spend a print | Hardware | Code size | Proven on an X2D by someone |
|---|---|---|---|---|
| A. USB stick + FTPS | upload, size check, delete (as 5.1 did) | a USB stick | small | upload yes, print start no |
| B. Own port 6000 client | ability reply, upload `result:0`, read-back md5 (cmdtype 4) | none | medium | landing path yes, full print no |
| C. Bambu's plugin | little; the plugin hides the steps | none | medium, native | reached `RUNNING` |
| D. Studio by hand | nothing in our tooling | none | none | yes (our minis) |
| E. Cloud | n/a | none | n/a | n/a (LAN mode) |

**Recommendation:** do A now (insert a USB stick, fix the basic-ftp session-reuse host, rename
"card" to "external storage"), because it is the smallest change on a documented path that
another basic-ftp client has already used on X2D USB storage; then build B as the lasting fix,
verifying on our X2D that the upload and `brtc://emmc/` start work before relying on it.
