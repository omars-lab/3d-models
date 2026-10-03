---
date: 2026-10-03
produced-by: checker (Claude Opus 5.5), consolidating researchers A and B. Re-opened the sources behind each load-bearing claim with WebFetch, `curl` of raw GitHub files, and the installed basic-ftp 5.3.1 and Node.js TLS source. The printer was not contacted by the checker; the first-hand facts below were gathered by the coordinating session and passed in.
feeds:
  - '[[first-party-dispatch]]'
---

# X2D built-in storage: how a print gets on with no drive in (consolidated)

This is the doc to act on. It is built from two independent passes, kept as the record:
researcher A's 2026-10-03-x2d-internal-storage-a.md (branch `research-x2d-storage-a`, PR #499)
and researcher B's 2026-10-03-x2d-internal-storage-b.md (branch `research-x2d-storage-b`,
PR #498). It feeds [the first-party dispatch issue](../issues/first-party-dispatch.md), whose
2026-10-03 section records the `553` our CLI got when nothing was in the external slot.

**How to read it.** Each claim says whether A, B or both made it, whether I re-opened the
source, and whether that source was **fetched** (I read the page or file) or only a
**snippet** (a search result or code-search excerpt). A claim only one researcher found is
kept and flagged, not dropped. Hedges are the sources' own. Where a row says "none of the
clients checked", the set is the one listed in section 7.

## The short answer

**Why Studio can print with nothing in the slot.** On the X2D (and the H2 series and P2S),
Studio's Print button does not use FTPS. Studio checks bit 0 of the `fun2` field in the
printer's status; when it is set, Studio lets a LAN print go ahead with no external storage
and has Bambu's closed networking plugin upload the `.3mf` over a second TLS file service on
TCP port 6000 into built-in storage, then start it with MQTT `project_file` and
`url: "brtc://emmc/<name>"`. FTPS on port 990 serves only external storage, which is why our
`STOR` got `553` with the slot empty. Our printer reports `fun2: "B7B77"`, so bit 0 is set.

**What we can do.** Two routes work for a third-party LAN client:

1. **A USB drive plus FTPS plus `ftp:///` (what our CLI already does).** Proven on our own X2D
   on 2026-10-03: with a USB drive in, our unchanged CLI uploaded over FTPS and the print
   started (section 3). The X2D has a USB port, not a microSD slot.
2. **Our own port-6000 client plus `brtc://emmc/`.** Documented by people who captured it and
   built by at least three open-source projects, proven end to end on a P2S and an H2D. No
   source shows a third-party client running the full upload and start on an X2D.

**Recommendation in one line:** keep the USB-drive route as the way we send, and in one small
PR pass the printer host to basic-ftp's TLS options and rename "card" to "external storage";
build the port-6000 client later, only if the drive becomes a cost (section 6).

## 1. Claims, side by side

"A" and "B" say what each researcher claimed; a dash means that one did not raise it.

| # | Claim | A | B | Source re-checked | Fetched or snippet | Verdict |
|---|---|---|---|---|---|---|
| 1 | FTPS on 990 serves only external storage; `553` with nothing in | yes | yes | bambuddy wiki (troubleshooting); open-bamboo-networking `research/06.03-ftps.md` ("often unreachable", P2S); bambu-printer-mcp changelog ("internal eMMC still refuses FTPS writes with `553`") | fetched | **Agree, confirmed.** Our own `553` with no drive and success with a drive (section 3) fit it. The open-bamboo-networking line is hedged "often" and is about a P2S. |
| 2 | Studio's LAN gate is "has external storage **or** can print from eMMC" | yes | yes | Bambu Studio `src/slic3r/GUI/Jobs/PrintJob.cpp` line 847; else the message "Storage needs to be inserted before printing via LAN." | fetched | **Agree, confirmed.** Line 293 sets `params.try_emmc_print = this->could_emmc_print`. |
| 3 | Studio's access check probes port 6000 and an FTPS `verify_job`, and fails only if both fail | – | yes | `PrintJob.cpp` lines 223–242 | fetched | **B only, confirmed.** |
| 4 | Studio uploads to built-in storage over port 6000 and starts with `brtc://emmc/<name>` | yes | yes | open-bamboo-networking `research/08.08-print-abi.md` ("wire-confirmed P2S, 2026-07"); bambuddy `print_storage.py` and wiki; BambuStudio PR #12146 | fetched | **Agree, confirmed for P2S on the wire.** For the X2D the evidence is a bambuddy user report (issue #3126) of a Studio-sent `brtc://emmc/` url, and the "X2D behaves like the H2 series" wiki line. The upload code itself is in the closed plugin. |
| 5 | `fun2` bit 0 is `is_support_print_with_emmc` | yes | yes | Bambu Studio `DeviceManager.cpp` (`get_flag_bits_no_border(fun2, 0)`) | fetched | **Agree, confirmed.** Ours is `B7B77`: the last hex digit 7 has bit 0 set. |
| 6 | `fun2` bit 17 is `is_support_model_internal_storage` | – | yes | same file | fetched | **B only, confirmed.** Ours has it set (hex digit B at bits 16–19). |
| 7 | `fun` bit 31 is `is_support_brtc` | yes | yes | Bambu Studio and OrcaSlicer `DeviceManager.cpp` | fetched | **Agree, confirmed.** |
| 8 | OrcaSlicer uses the port-6000 route for Send | yes | partly ("mirrors Studio, with a `disable_emmc` switch", code search only) | OrcaSlicer `DeviceManager.cpp` lines 621–622; bambuddy wiki | fetched | **A is too broad.** Orca reads `is_support_brtc`, but its print path uses eMMC only when `disable_emmc_print` is "0" or "false", and the default is "true", so it prints over FTPS by default. That matches the bambuddy wiki: Orca "will refuse to send with an empty slot". I did not re-check Orca's `SendToPrinter.cpp` path. |
| 9 | Port-6000 login is a 16-byte header plus a 16-byte login, not a 64-byte packet | yes, confident | flags it, wants a Studio capture | open-bamboo-networking `06.04-port-6000.md`; ha-bambulab `media_sources.py`; bamdude `codec.py`; OpenBambuAPI `lan-file-tunnel.md` | fetched | **16 bytes, with a hedge.** See section 2. |
| 10 | Upload chunks are sent back to back; waiting for a reply per chunk gives `-9203` | yes | partly (chunks, `file_md5` on the last) | `06.04-port-6000.md` | fetched | **Confirmed**, P2S-based. |
| 11 | On the X2D an eMMC upload lands in `/userdata/model/history/<path>`; chunk size 255 KiB; ability reply lists `emmc` and `udisk` for storage and upload | yes | yes | `06.04-port-6000.md`, X2D on firmware 01.02.00.00 | fetched | **Agree; one source.** All three facts come from open-bamboo-networking alone, on one firmware. |
| 12 | `ftp://` names the FTPS volume and a port-6000 file of the same name does not satisfy it; `brtc://emmc/` makes the firmware search the udisk cache, then eMMC | yes | yes | `08.08-print-abi.md` | fetched | **Agree, confirmed** (P2S captures). |
| 13 | `brtc://udisk/` does not exist; Studio uses `file:///media/usb0/…` for the drive | – | yes (first half) | bamdude `tests/unit/test_start_print_url_by_storage.py` and its notes | fetched | **B only, confirmed as bamdude's statement.** Unit tests with the model set to "X2D"; not a real printer. |
| 14 | Developer Mode accepts a plain `url`; without it `url_enc` is required | yes | yes | `08.08-print-abi.md` | fetched | **Agree, confirmed**, captured on P2S/N7 boards. Our send in section 3 used a plain url with Developer Mode on and started. |
| 15 | Stock clients send `md5: "from_sd_card"`; ours sends `""` | yes | yes | `08.08-print-abi.md` ("A real file hash never appeared in any captured LAN `project_file`") | fetched | **Agree, confirmed.** Our `""` did not stop the print in section 3 (assuming the send used the CLI's current fields). |
| 16 | The X2D has 8 GB eMMC and a USB port, no microSD slot | yes | yes | shop3duniverse product page ("Built-in 8 GB EMMC and USB Port"); printer-hub.ru X2D vs X1C ("8 GB eMMC + USB" vs "4 GB eMMC + microSD"); bambulab.com spec page returned 403 | fetched (two retailers or reviewers); snippet (Bambu's own page) | **Agree, confirmed.** First-hand: our drive is in and read (section 3). |
| 17 | A standard-length USB drive can be hit by the toolhead | – | yes | forum thread 253935 (user_3145750058, May 28, 2026: "the riser bumps against the USB drive"; Tool_Maker, June 1: Bambu sells the SanDisk Ultra Fit) | fetched | **B only, confirmed as one user's report**, hedged by the user ("leading me to wonder"). |
| 18 | Which third-party clients implement the eMMC upload | open-bamboo-networking only (plus bambu-printer-mcp through Bambu's own plugin) | open-bamboo-networking, Pandar, bamdude, FoxForge (snippet) | Pandar `docs/roadmap.md` and `file_transfer.rs`; bamdude `bambu_tunnel/`; open-bamboo-networking `STATUS.md` | fetched (FoxForge: snippet) | **Disagree on reach; B searched wider and its sources hold.** Both are right that none of the clients checked shows a full third-party upload and start on an X2D. Proven end to end: P2S (open-bamboo-networking `STATUS.md`) and H2D (Pandar: "reached `RUNNING` from built-in storage through a `brtc://emmc/...` upload"). Pandar also notes it needs "the printer's static-RSA TLS 1.2 profile". |
| 19 | bambu-printer-mcp reached an X2D print by loading Bambu's closed plugin on macOS | yes | – (code search only) | bambu-printer-mcp PR #10 | fetched | **A only, confirmed with its hedge:** earlier X2D testing "reached `RUNNING`"; the merged revision "makes no claim of a new physical print". PR #10 also says it ran on "Linux/Node 24", which matters for row 20. |
| 20 | basic-ftp drops the host on the data connection, so an X2D with a USB drive answers `522 session reuse required` | yes | – | bambu-printer-mcp `CHANGELOG.md` 1.1.14; basic-ftp 5.3.1 `transfer.js` and `Client.js`; Node.js TLS source | fetched | **A only; the source says it, but it did not happen to us.** The mechanism is real and depends on the Node.js version: it hits LIST and STOR alike on newer Node, and neither on the Node we pin. Our LIST and STOR both worked (section 3). See section 4. |
| 21 | "N7" is the P1/A1 class | yes | – (B calls N7 the P2S) | Bambu Studio `resources/printers/N7.json` (serial prefix `22E`) | fetched | **A is wrong; N7 is the P2S.** |
| 22 | PR #12146 quote: "H2C/H2D use `brtc://emmc/` transport while X1C uses `ftp://`" | yes | – | BambuStudio PR #12146 body | fetched | **Not verbatim; same meaning.** The text reads "H2C/H2D route sliced sends to `brtc://emmc/`, while X1C uses `ftp://`". The PR is open, by bambuddy's author, not Bambu staff. |
| 23 | Files Studio puts in eMMC cannot be listed by Handy, read over FTP, or reprinted from the screen | yes | – | PR #12146 code comment; BambuStudio issue #10481 (open, assigned to a Bambu developer) | fetched | **A only, confirmed as a contributor's statement and a user report**, not Bambu documentation. |
| 24 | Bambuddy can list built-in storage over 6000 "but the firmware refuses to serve those files back" | yes | – | bambuddy wiki | fetched | **Conflicts with another source.** open-bamboo-networking reports the X2D ability reply `"allow_internal_model_download":true` and documents download (cmdtype 4). Unsettled; it may depend on model, firmware or file kind. |
| 25 | An eMMC job can be read back over FTPS under `/cache/<name>` | yes | – | bambuddy `print_storage.py` | fetched | **A only, confirmed, and model-dependent:** yes on one H2D (firmware 01.03.00.00, card in), no on a P2S and an H2C. Unknown on the X2D. |
| 26 | Bambuddy lists the USB drive plus "Store Sent Files on External Storage" as a working workaround | – | – | bambuddy issue #2762 (H2D, LAN only, Developer Mode) | fetched | **Found by the checker.** It is H2-series evidence for the USB route; our X2D send worked without our touching that setting. |
| 27 | Bambuddy evidence | wiki and `print_storage.py` fetched | release note and wiki as snippet | both re-opened | fetched | **A's fetch stands;** B's snippets match what the full pages say. |
| 28 | LAN-only mode turns off the cloud, so cloud print is out; cloud-dispatched urls are `https://` or `ftp://`, never `brtc://` | yes | yes | SimplyPrint help page ("LAN-only Mode disconnects the printer from Bambu Lab's cloud"); `08.08-print-abi.md` ("Cloud-dispatched project URLs appear limited to …") | fetched (a third-party help page, not Bambu's) | **Agree.** The LAN-mode line rests on a third-party page; the url line carries its source's "appear". |
| 29 | OpenBambuAPI credits names to "Bambu's open-source `bambu_net_oss`"; the attribution looks doubtful | – | yes | `lan-file-tunnel.md` | fetched | **B only; not settled.** |
| 30 | `LIST_INFO` (cmdtype 1) returns result 2 on an H2S on firmware 01.02.00.00 | yes | yes | `lan-file-tunnel.md` | fetched | **Agree; one source, one model.** |
| 31 | The H2D forum: "Print Plate" goes to built-in storage and starts; "Send" goes to external storage | yes | yes | forum thread 234923 (JonRaymond, Feb 17, 2026; JvL_1, Mar 4, 2026) | fetched | **Agree, confirmed**, user posts. |

## 2. Port-6000 login framing: 16 bytes, with a hedge

Three independent code bases that talk to real printers use the same framing:
open-bamboo-networking (`research/06.04-port-6000.md`), ha-bambulab (`media_sources.py`:
`MAGIC_LOGIN = 0x0101013F`, `MAGIC_CTRL = 0x0102013F`, login of `bblp` and the access code
each `ljust(8, b"\0")`) and bamdude (`codec.py`: header `<I payload_len> <I type> <I sequence> <I 0>`).
The frame is a 16-byte little-endian header (payload length, magic, sequence, zero) followed
by a 16-byte login (`bblp` padded to 8 bytes, the access code padded to 8). Control frames to
the printer use magic `0x0102013f`; replies come back with `0x00xx013f`.

OpenBambuAPI's `lan-file-tunnel.md` stands alone with a 64-byte login (`bblp` in 8 bytes, the
code in 32, 24 reserved) and a header ordered size, sequence, cmdtype, mtype. The same page
says port 6000 is the MJPEG camera on A1 and P1 printers and that `LIST_INFO` was retired on
one H2S firmware, so it may describe a different service or firmware. open-bamboo-networking's
X2D notes (ability reply, landing path) imply a login that worked on an X2D, most likely its
own 16-byte client, though the notes do not say so in those words.

**What is still open:** Bambu documents none of this, and nobody has checked our X2D's
handshake. Whoever builds the port-6000 client should check the login against a capture of
Studio's own send to our printer before trusting it.

## 3. Our first-hand facts (2026-10-03)

These were gathered by the coordinating session, read-only until the send, after both
research passes. The checker did not contact the printer.

- **With nothing in the slot:** status `sdcard: false`, `tl_external_*` 0/0,
  `tl_internal_free_kb` 884486 of 962560; FTPS `LIST /` came back empty and `STOR` at the
  root came back `553`.
- **Capability flags:** `fun2: "B7B77"`. Bit 0 (print from eMMC) and bit 17 (built-in model
  storage) are both set.
- **With a USB drive in:** `bambu storage show` reads 22.7 GB free of 28.7 GB from
  `ipcam.tl_external_free_kb` and `tl_external_total_kb`, so those fields track the drive. The
  comment in [`storage.ts`](../../tools/bambu/src/storage.ts) that calls this reading
  unconfirmed can now say confirmed.
- **LIST with the drive in:** `bambu storage list /` worked over basic-ftp 5.3.1, implicit TLS
  on 990, with no host in `secureOptions`. It returned a `timelapse/` folder, so the data
  connection succeeded.
- **STOR and print start with the drive in (about 19:43 UTC):** our unchanged
  [`ftps.ts`](../../tools/bambu/src/backends/ftps.ts) stored `/sheets-04b.plate.3mf`
  (558 KB) over the same setup, with no host in `secureOptions`, and it succeeded with no
  `522`. MQTT `project_file` with `url: "ftp:///sheets-04b.plate.3mf"` started the print: the
  state went PREPARE, then RUNNING (layer 0 of 20, 41 minutes).

So on our X2D, with our pinned Node.js, the `522` that bambu-printer-mcp saw did not happen
for LIST or STOR, and a `ftp:///` start from a USB drive works. That is the first report of a
third-party X2D print start from a USB drive among the sources here; bambu-printer-mcp had
said "Printing remains a separate check".

## 4. The 522 risk: why it did not hit us, and when it would

bambu-printer-mcp's changelog (1.1.14, 2026-09-28) says basic-ftp "wraps each data socket
without a host, so Node can bind its resumable session to `localhost` instead of the printer
host", and printers that require TLS session reuse (vsftpd's `require_ssl_reuse`; the X2D
runs vsFTPd 3.0.5 per an open-bamboo-networking transcript) replied `522` "to every LIST,
STOR and RETR". Reading the code:

- **basic-ftp 5.3.1 treats LIST and STOR the same.** Both open their data connection through
  `connectForPassiveTransfer` in `transfer.js`, which calls `tls.connect` with the stored
  `tlsOptions`, the data socket and `session: ftp.socket.getSession()`, and no host or
  servername. In implicit mode, `connectImplicitTLS` stores our `secureOptions` as they are
  (`{ rejectUnauthorized: false }`, no host); only explicit TLS copies the host in. The one
  difference for upload is that it waits for `secureConnect` before writing.
- **Whether the session is offered depends on Node.js.** Node commit fd890ba01d ("tls: bind
  reusable sessions to authenticated host", the fix for CVE-2026-48934) makes Node drop a
  saved session whose stored host does not match the new connection's. A data socket
  connected by IP has no host name, so Node treats it as `localhost`; the control session is
  stored under the printer's IP; they differ, Node does a fresh handshake, and vsftpd answers
  `522`. That commit is in Node v22.23.0 (released 2026-06-18) and v24.19.0. It is not in
  v22.22.3, which [`bin/bambu`](../../tools/bambu/bin/bambu) pins, so our sessions are reused.
  bambu-printer-mcp ran on Node 24.
- **A second, smaller trap:** under TLS 1.3 the session ticket arrives after the handshake.
  bambu-printer-mcp waits for it (`waitForTlsSession`). Our `access()` makes several round
  trips before any LIST or STOR, so the ticket is there in time, and our LIST and STOR both
  worked.

**Verdict.** A's claim is right about the mechanism and wrong as stated for us: it needs a
newer Node.js, and it hits LIST as well as STOR. Today the risk is nil on our setup, shown by
both commands working. It comes back the day `bin/bambu` moves to Node v22.23.0 or later, or
to v24.19.0 or later. Passing `host: this.config.host` in `secureOptions` makes basic-ftp
bind the session to the printer's IP on both sockets and closes it for good; that is one line
in [`ftps.ts`](../../tools/bambu/src/backends/ftps.ts), and the header comment there ("we
simply don't touch it") should say why the host is passed. This reading of Node's source was
not tested by running a newer Node against the printer.

## 5. What was re-checked and what rests on less

- **Fetched by me:** every source named in the table, except as below.
- **Snippet only:** Bambu's own X2D spec page (403), Bambu's wiki pages on internal storage
  and USB drives (402), FoxForge (code search), and the "LAN mode turns off Handy" claims
  beyond the SimplyPrint page.
- **Not re-checked:** OrcaSlicer's `SendToPrinter.cpp` route, bambulabs_api's upload code
  (both researchers relied on a search for "emmc" finding nothing), and the persano plugin
  fork.

## 6. Options

The USB route is no longer a bet; it ran on our printer. The open choices are what to tidy on
it and whether to build the port-6000 route at all.

| Option | Pros | Cons | Implications |
|---|---|---|---|
| **A. Keep the USB drive, FTPS and `ftp:///`; pass the host and fix the wording** | Proven end to end on our X2D (section 3). The code path exists; the change is one line plus wording. Files on the drive show up in Handy and on the printer's screen, which eMMC files do not (row 23). Upload can be verified by LIST, size and delete before any print. | Needs a drive in the printer at all times. A standard-length drive may be hit by the toolhead (row 17, one report); a low-profile drive avoids it. Studio still sends to eMMC, so files live in two places. Timelapses share the drive's space. | `storage.ts` keeps refusing when no external storage is in, reworded from "card" to "external storage" / "USB drive". The host line removes the Node upgrade trap (section 4). Leaves the port-6000 route unbuilt, so a pulled drive stops CLI sends. |
| **B. Our own port-6000 client: upload to eMMC, start with `brtc://emmc/`, chosen by `fun2` bit 0** | No drive needed; the route Studio uses on this printer. Three open-source implementations to learn from and agreement on the framing (section 2). Developer Mode lets us send a plain url. | Reverse-engineered, undocumented by Bambu, can change with firmware. A fussy upload (pipelined chunks, `-9203` otherwise). Not proven end to end on an X2D by anyone. open-bamboo-networking is AGPL, so we write from the documented behavior, not its code. eMMC files are invisible to Handy and the reprint list. | A second upload backend and new failure messages. Should be built against a capture of Studio's send to our printer (Omar's call, and a capture tool). Its first send is one approval under D-093. If Bambu adds signing to this path, Developer Mode becomes a hard requirement. |
| **C. Load Bambu's closed plugin, or run another project's client** | Someone else's code has run against real printers; one report of an X2D reaching RUNNING through Bambu's plugin (row 19). | macOS-only native code tied to a closed binary whose interface changes, or another language and runtime next to our TypeScript CLI; licenses not checked; failures are hard to explain. | Couples the CLI to an installed Studio or Connect version, which the first-party dispatch work set out to avoid. Useful as a one-off reference, poor as a dependency. |
| **D. Send from Bambu Studio by hand** | Works. | No approval record or send checks. | Ruled out for Omar by the dispatch issue: "Never work around it by sending from Bambu Studio for Omar." |
| **E. Cloud print** | Bambu's own path. | LAN-only mode turns off the cloud (row 28); cloud urls do not use `brtc://`; the file goes through Bambu's servers. | Out unless LAN mode is dropped. |

**Recommendation:** take A now, because it already printed on our X2D: one PR that passes the
printer host in `secureOptions`, renames "card" to "external storage", and marks the
`tl_external_*` reading confirmed; leave B parked with its first step written down (capture
Studio's send to our printer), to build only when needing the drive costs us something.
