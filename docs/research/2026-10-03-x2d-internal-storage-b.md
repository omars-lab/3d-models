---
date: 2026-10-03
produced-by: researcher B (Claude Opus 5.5), one of two independent researchers on the same question; web search and fetch, `gh api` and `gh search code` against public GitHub repos, and local clones of Bambu Studio (commit da8b44e, 2026-09-28) and ClusterM/open-bamboo-networking (commit 8656b66, 2026-09-30). The printer was not contacted.
feeds:
  - '[[first-party-dispatch]]'
---

# X2D built-in storage: how a print gets on with no card (research B)

Feeds [the first-party dispatch issue](../issues/first-party-dispatch.md), the record of
why our CLI's send stopped at the upload with `553 Could not create file`.

**The question.** Our X2D is in LAN mode with Developer Mode on and has no removable
storage in it (the status frame says `sdcard: false`). Bambu Studio printed minis-01 and
minis-02 to it anyway. Our CLI uploads over FTPS (port 990, user `bblp`, the access code
as password) and is refused. How does Studio do it, and can our CLI do the same?

**How to read this file.** Every source says whether I **fetched** it (read the whole
page or file) or saw only a **snippet** (a search-result line or a code-search excerpt,
which can be out of context). Source code read from a clone or with `gh api` counts as
fetched. Quotes are short and verbatim; everything else is paraphrase. Hedges are the
sources' own. Where I say "none of the clients checked here", the set is listed in
section 7.

---

## Short answer

1. **Studio does not use FTPS for the built-in storage.** When the printer reports that it
   can print from its built-in storage, Studio's print job uploads the `.3mf` over a
   second, TLS-wrapped file channel on **TCP port 6000**, writing it to storage `emmc`,
   then starts the print with the usual MQTT `project_file` command whose `url` is
   **`brtc://emmc/<name>`**. On the X2D the file lands in `/userdata/model/history/`
   (one source, X2D firmware 01.02.00.00). The FTPS server on 990 only serves the
   removable drive, which is why our upload with no drive gets 553.
2. **A third-party LAN client can do this.** At least four open-source projects implement
   the port-6000 upload plus `brtc://emmc/` start: ClusterM/open-bamboo-networking (C++),
   ProjectPandar/pandar (Rust), kainpl/bamdude (Python) and FoxForge (Python, snippet
   only). Pandar reports a real H2D with `sdcard = false` reaching `RUNNING` this way.
   I found no source that reports the full upload-and-start on an X2D specifically; the
   X2D upload half is observed by ClusterM.
3. **The X2D has no microSD slot.** It takes a USB drive (two third-party sources; the
   official spec page refused my fetch). So "just put in a microSD card" becomes "just
   put in a USB drive".

---

## 1. Raw findings: what Bambu Studio's own source does

Source: [bambulab/BambuStudio](https://github.com/bambulab/BambuStudio) at commit
da8b44e (2026-09-28), read from a local sparse clone. **Fetched.** Studio's GUI is open
source; the networking plugin (`libbambu_networking`) that does the actual transfer is
closed.

**1.1 The X2D's printer profile says it can print without a card.**
[resources/printers/N6.json](https://github.com/bambulab/BambuStudio/blob/master/resources/printers/N6.json).
Model `N6`, serial prefix `20P` (ours is 20P6AJ…), and:
`"support_print_without_sd": true`, `"support_send_to_sd": true`,
`"support_save_remote_print_file_to_storage": true`. Nine other profiles also carry
`support_print_without_sd: true` (including O1D, the H2D; N7, the P2S; BL-P001, the
X1C); N1, N2S, N9, C11 and C12 carry `false`.

**1.2 The printer announces the ability at run time.**
[src/slic3r/GUI/DeviceManager.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/DeviceManager.cpp),
lines 4483 and 4488:
`is_support_print_with_emmc = get_flag_bits_no_border(fun2, 0) == 1;` and
`is_support_model_internal_storage = (get_flag_bits_no_border(fun2, 17) == 1);`.
So bit 0 of `print.fun2` in the MQTT status is the switch. Line 4464 reads a separate
`is_support_brtc = get_flag_bits(fun, 31)`.
[SelectMachine.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/SelectMachine.cpp)
line 3359 copies it onto the job: `m_print_job->could_emmc_print = obj_->is_support_print_with_emmc;`.

**1.3 The print job probes port 6000, then prints with storage present or `could_emmc_print`.**
[src/slic3r/GUI/Jobs/PrintJob.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/Jobs/PrintJob.cpp):

- Line 228, the LAN access check: `std::string url = "bambu:///local/" + devIP + "?port=6000&user=" + "bblp" + "&passwd=" + accessCode;`, opened as a `FileTransferTunnel`.
- Lines 234 to 238: it also tries an FTPS probe upload named `verify_job`. The job fails only when both fail (`if (!emmc_ok && !ftp_ok)`).
- Line 293: `params.try_emmc_print = this->could_emmc_print;`.
- Lines 847 to 852, the LAN branch: `if (this->has_sdcard || this->could_emmc_print) { ... result = m_agent->start_local_print(params, update_fn, cancel_fn); } else { ... _L("Storage needs to be inserted before printing via LAN.") }`.

So Studio's gate for a LAN print is "a card, **or** the printer can print from eMMC". What
`start_local_print` does with `try_emmc_print` is inside the closed plugin; section 2
covers what others observed on the wire.

**1.4 Send to Printer names the storage explicitly.**
[src/slic3r/GUI/SendToPrinter.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/SendToPrinter.cpp):
line 36 `#define EMMC_STORAGE "emmc"`; line 1889 asks for the storage list with
`{"cmd_type", 7}`; lines 1962 to 1964 upload with `{"cmd_type", 5}` and
`upload_params["dest_storage"] = m_selected_storage;`.
[src/slic3r/Utils/FileTransferUtils.hpp](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/Utils/FileTransferUtils.hpp)
declares the `ft_tunnel_create` / `ft_job_create` C functions that the closed plugin
implements.

**1.5 The upload message itself is in Studio's open source.**
[src/slic3r/GUI/Printer/PrinterFileSystem.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/Printer/PrinterFileSystem.cpp)
(the Device > Files tab), lines 1275 to 1278: `req["type"] = "model"; req["storage"] = m_upload_file->select_storage; req["path"] = m_upload_file->name;` plus `req["total"] = file_size`.
Lines 1398 to 1405 build each chunk as the JSON, then `oss << "\n\n";`, then the bytes.

---

## 2. Raw findings: the port-6000 wire, from people who captured it

**2.1 ClusterM/open-bamboo-networking**, an open-source drop-in replacement for Bambu's
networking plugin. [Repo](https://github.com/ClusterM/open-bamboo-networking), commit
8656b66 (2026-09-30). **Fetched** (local clone). The README lists X2D and H2D among
supported printers. It says eMMC "browsing internal memory may still be slow or
unreliable (e.g. on P2S)".

- [research/06.04-port-6000.md](https://github.com/ClusterM/open-bamboo-networking/blob/master/research/06.04-port-6000.md), reverse-engineered on P2S, with X2D notes:
  - Implicit TLS on 6000, leaf certificate `CN=<serial>`, login as user `bblp` plus the access code, then JSON commands. Upload is `cmdtype 5` with `{"type":"model","storage":"emmc","path":"<name>.gcode.3mf","total":<bytes>}`, sent in chunks; the last chunk carries `file_md5`.
  - X2D: "the **X2D** (`01.02.00.00`) returns **255** on `:6000` and **31** ... when the same job arrives over TUTK" (chunk size in KiB).
  - X2D: "On the X2D a `storage:"emmc"` upload lands in **`/userdata/model/history/<path>`**".
  - X2D storage reply: `{"allow_internal_model_download":true,"api_version":3,"storage":["emmc","udisk"],"upload_storage":["emmc","udisk"]}`.
- [research/06.03-ftps.md](https://github.com/ClusterM/open-bamboo-networking/blob/master/research/06.03-ftps.md): FTPS is "used for file transfer to an **external / USB-style volume**"; "Observed P2S FTPS root follows the inserted USB stick; internal eMMC paths are often unreachable over FTPS". Note the hedge: "often", and on P2S.
- [research/08.08-print-abi.md](https://github.com/ClusterM/open-bamboo-networking/blob/master/research/08.08-print-abi.md):
  - Stock `start_local_print` sends the "Full `.3mf` over **TLS `:6000` (brtc)**" and then "LAN MQTT `project_file` with `brtc://emmc/<name>`" ("wire-confirmed P2S, 2026-07").
  - URL schemes: `ftp://` is the FTPS volume, and "A `:6000` cache file of the same name does **not** satisfy `ftp://`". `brtc://emmc/` is the model-cache lookup; "Despite the `emmc` token, firmware searches udisk cache then emmc". `ftp:///` with three slashes is also accepted.
  - "Non-Developer-Mode firmware requires `url_enc`; Developer Mode accepts plain `url`." Our printer has Developer Mode on.
  - Stock LAN `project_file` always sends `"md5": "from_sd_card"`.
- Source [src/print_job_naming.cpp](https://github.com/ClusterM/open-bamboo-networking/blob/master/src/print_job_naming.cpp): `use_brtc_cache_upload()` returns `p.try_emmc_print` unless the `force_ftps` setting is on; `build_brtc_emmc_url()` returns `"brtc://emmc/" + name`. The `force_ftps` comment: "this is how LAN print worked before the BRTC :6000 protocol was added."

**2.2 ProjectPandar/pandar**, a print farm hub with its own Studio plugin.
[docs/roadmap.md](https://github.com/ProjectPandar/pandar/blob/main/docs/roadmap.md),
**fetched**: "A Web-submitted print on an H2D with `sdcard = false` reached `RUNNING`
from built-in storage through a `brtc://emmc/...` upload." Its own open acceptance work
still lists proving the same from real Bambu Studio. "Printable artifacts probe the
BRTC/eMMC tunnel on port 6000 before protected FTPS fallback." It also notes the port-6000
TLS needs "the printer's static-RSA TLS 1.2 profile".
[crates/pandar-agent/src/machine/file_transfer.rs](https://github.com/ProjectPandar/pandar/blob/main/crates/pandar-agent/src/machine/file_transfer.rs),
**fetched**: `format!("brtc://emmc/{}", path.trim_start_matches('/'))`.

**2.3 kainpl/bamdude**, a print manager (Python).
[backend/app/services/bambu_tunnel/__init__.py](https://github.com/kainpl/bamdude/blob/main/backend/app/services/bambu_tunnel/__init__.py),
**fetched**: "the channel that reaches a printer's internal storage, which FTP cannot see."
[codec.py](https://github.com/kainpl/bamdude/blob/main/backend/app/services/bambu_tunnel/codec.py),
**fetched**: 16-byte frame header `<I payload_len> <I type> <I sequence> <I 0>`, and the
`\n\n` separator, citing Studio's `UploadFileTask`.
[tests/unit/test_start_print_url_by_storage.py](https://github.com/kainpl/bamdude/blob/main/backend/tests/unit/test_start_print_url_by_storage.py),
**fetched**, with the test printer model set to `"X2D"`: external gives
`ftp://job.gcode.3mf`, internal gives `brtc://emmc/job.gcode.3mf`. It warns:
"``brtc://udisk/…`` does not exist". Unlike Studio, bamdude sends a real uppercase MD5.
These are unit tests; they do not prove a real X2D accepted it.

**2.4 maziggy/bambuddy**, a print archiver. **Snippet** (code-search excerpts of a
release note and a wiki page). The X2D release note: "Bambu Studio filed the sliced file
on the printer's eMMC (`"url": "brtc://emmc/..."`), which FTPS on port 990 does not
serve, and the X2D does this like the H2 series and the P2S." Based on a user report,
[issue #3126](https://github.com/maziggy/bambuddy/issues/3126). This is independent
field evidence that Studio uses `brtc://emmc/` on an X2D.

**2.5 greghesp/ha-bambulab** (Home Assistant, pybambu).
[custom_components/bambu_lab/pybambu/media_sources.py](https://github.com/greghesp/ha-bambulab/blob/main/custom_components/bambu_lab/pybambu/media_sources.py),
**fetched**. It lists and downloads over port 6000 (`Tcp6000MediaSource`), with a 16-byte
login (8 bytes user, 8 bytes access code). I found no upload or print start in this file,
and I did not check the rest of ha-bambulab for one.

**2.6 OpenBambuAPI.** [lan-file-tunnel.md](https://github.com/Doridian/OpenBambuAPI/blob/main/lan-file-tunnel.md),
**fetched**. It documents TCP 6000 with `cmdtype` 1 LIST_INFO, 4 FILE_DOWNLOAD,
5 FILE_UPLOAD, 7 REQUEST_MEDIA_ABILITY. Its caveats: on A1/P1 port 6000 is the MJPEG
camera, and on an H2S on 01.02.00.00 LIST_INFO returned result 2. It credits the names to
"Bambu's open-source `bambu_net_oss` reference implementation". That attribution looks
doubtful to me: bambu_net_oss appears to be a community project, not Bambu's. I hedge it;
I did not settle it.
[mqtt.md](https://github.com/Doridian/OpenBambuAPI/blob/main/mqtt.md), **fetched**: the
`project_file` example gives only `file:///` and `ftp:///` URLs, with no `brtc://`.
[ftp.md](https://github.com/Doridian/OpenBambuAPI/blob/main/ftp.md), **fetched**: implicit
FTPS on 990, `bblp` plus access code.

**Disagreement to flag.** The login framing differs. OpenBambuAPI describes a 64-byte
auth packet (`bblp` NUL-padded, then the access code). ClusterM and ha-bambulab both send
a 16-byte login (8 bytes user, 8 bytes access code) under header magic `0x0101013f`. Two
implementations against one doc favor 16 bytes, but whoever builds this should capture
Studio's real handshake to settle it.

---

## 3. Raw findings: X2D hardware and forum reports

- **The X2D takes a USB drive, not a microSD card.** [printer-hub.ru X2D vs X1C](https://printer-hub.ru/en/posts/bambu-lab-x2d-vs-x1c), **fetched**: X2D "8 GB eMMC + USB", X1 Carbon "4 GB eMMC + microSD". The official [X2D spec page](https://bambulab.com/en-us/x2d/specs) returned 403, so its "built-in 8 GB eMMC and USB Port" is **snippet** only.
- **A standard thumb drive can hit the toolhead.** [forum thread 253935](https://forum.bambulab.com/t/why-you-should-not-use-a-standard-usb-thumb-drive-in-the-x2d/253935), **fetched**. user_3145750058 (May 28, 2026): "the riser bumps against the USB drive, leading me to wonder how long it would be until the USB socket ... would become damaged". Tool_Maker (June 1, 2026): "BL sells the SanDisk Ultra Fit USB 3.2 Flash Drive". One user's report, with a hedge ("leading me to wonder").
- **Bambu's wiki has a page on printing from internal storage.** [How to send and print models from Internal Storage](https://wiki.bambulab.com/en/knowledge-sharing/how-to-use-internal-model-cache-space): **snippet** only, the fetch returned 402.
- [H2D forum thread 234923](https://forum.bambulab.com/t/unable-to-send-sliced-file-to-h2d-without-a-usb-drive-connected/234923), **fetched**. JonRaymond (Feb 17, 2026): "Print Plate" puts the file in internal storage and starts it, while "The 'Send' feature has always transfered the file (but not start it) to an external storage." JvL_1 (Mar 4, 2026): after a firmware update you can "choose 'Internal' or 'External' storage when you click 'send'". Nothing about FTP or LAN mode.
- [H2 SD-slot thread 159157, page 2](https://forum.bambulab.com/t/silly-question-is-there-an-sd-card-slot/159157?page=2), **fetched**. The H2 has no SD slot and uses USB. maxim3D on the internal storage: "No way to access those as far as I know without pulling the drive". EinUrElf (Mar 5, 2026): "via FTP access, this is still possible". The context is unclear, so I do not read this as FTP reaching the eMMC.
- **Snippet:** older Studio builds showed "A microsd card needs to be inserted before printing via LAN"; the current string (section 1.3) says "Storage".

---

## 4. Raw findings: our own repo and status frame

- [tools/bambu/src/backends/ftps.ts](../../tools/bambu/src/backends/ftps.ts) uploads with a bare `STOR` to the FTP root, and maps 553 to "no card". That matches every source above: the FTPS root is the removable drive.
- The status frame we read: `sdcard: false`, `tl_external_*` 0/0, `tl_internal_free_kb` 884486 of 962560. The `tl_` fields are named for timelapse storage. They show the built-in volume exists and has about 864 MB free, but I found no source saying they measure the model cache, so I do not lean on them.
- We have not yet looked at `print.fun2` bit 0 in our captured status. That bit is exactly what Studio checks (section 1.2). Reading it from an existing capture needs no printer contact.

---

## 5. Firmware facts, with their reach

| Fact | Printer and firmware it was seen on | Sources |
|---|---|---|
| Upload over TLS port 6000, `cmdtype 5`, storage `emmc` | P2S (captured); X2D 01.02.00.00 (upload, chunk size, landing path) | ClusterM; Studio source (message shape) |
| Start with `project_file`, `url: brtc://emmc/<name>` | P2S (wire-confirmed); H2D (Pandar, `RUNNING`); X2D (bambuddy user log, Studio-sent) | ClusterM, Pandar, bambuddy (snippet) |
| FTPS 990 serves only the removable drive | P2S ("often"); X2D and H2 (bambuddy, snippet) | ClusterM, bambuddy, bamdude |
| Plain `url` accepted with Developer Mode on; `url_enc` needed with it off | X2D (signing note); P2S | ClusterM |
| X2D storage list `["emmc","udisk"]`, upload to both allowed | X2D 01.02.00.00 | ClusterM |
| Printer flags eMMC printing in `print.fun2` bit 0 | all Studio-supported models | Studio source |

What I did **not** find: any source showing a third-party client running the whole
upload-and-start on an X2D, or the X2D firmware version we run. Firmware past
01.02.00.00 could differ.

---

## 6. Design notes: the options

| Option | Pros | Cons | Implications |
|---|---|---|---|
| **A. Put a USB drive in the X2D** (it has no microSD slot) | No code. Our FTPS backend and `ftp://` start stay as they are. Studio's own LAN gate accepts a drive. Cheap: one short drive. | A standard-length drive may be hit by the toolhead (one forum report); needs a low-profile one. Whether the X2D prints our `STOR` + `ftp:///<name>` from a drive is likely (it is the older path in every source) but **not shown on an X2D** in anything I read. Studio would keep sending to eMMC while we send to the drive: two places to look for a file. | First check is one send of a known-good plate (one approval, D-093). Leaves the eMMC path unbuilt, so the CLI keeps depending on a physical drive being in. |
| **B. Build the port-6000 eMMC upload in tools/bambu** | Same path Studio uses on this exact printer, so no hardware dependency. Four open-source implementations to read. Our Developer Mode means a plain `url`, no encryption. | Reverse-engineered and undocumented by Bambu; can change with firmware. The login framing is disputed (64 vs 16 bytes). Needs TLS that accepts the printer's self-signed cert with the right TLS profile (Pandar notes static RSA, TLS 1.2). No X2D end-to-end report found. More code to keep. | A second upload backend; the storage check becomes a choice of route (drive present: FTPS; `fun2` bit 0 set: port 6000) instead of a refusal. Best built against a capture of Studio's own send to our printer (needs a Studio send, Omar's call, and a capture tool). |
| **C. Use another project's code as a bridge** (for example ClusterM's plugin or tools, or Pandar's agent) | Code that has already been run against real printers. Fastest way to a working send. | Brings in another language and runtime (C++, Rust or Python) next to our TypeScript CLI. Licenses not checked. Their bugs and update timing become ours. | Good as a reference or one-off check even if we build option B ourselves; poor as a long-term dependency. |
| **D. Keep sending from Bambu Studio** | Works today (minis-01 and minis-02). | The repo says "Never work around it by sending from Bambu Studio for Omar" (the dispatch issue). It leaves the CLI unable to print and keeps Omar in the loop for every send. | Not an option under the current rule. |
| **E. Cloud print** | Bambu's path, no LAN protocol work. | The printer is in LAN mode; cloud needs it bound to an account, and it moves the file through Bambu's servers. | Out of scope unless LAN mode is dropped. |

**Recommendation:** do A now (a low-profile USB drive, then one approved test send of a
known-good plate) to unblock the CLI on the path it already has, and build B next as a
second backend chosen by `print.fun2` bit 0, modeled on ClusterM's and bamdude's code and
checked against a capture of Studio's own send, because that is what Studio does on this
printer and it removes the drive dependency.

---

## 7. What was checked, and what was not

Clients and sources checked for eMMC upload (seven): Bambu Studio source (does it, through
the closed plugin), ClusterM/open-bamboo-networking (does it), ProjectPandar/pandar (does
it), kainpl/bamdude (does it), ha-bambulab media_sources.py (lists and downloads over 6000;
no upload found in that file), OpenBambuAPI (documents port 6000; its print example has no
`brtc://`), BambuTools/bambulabs_api (a code search for "emmc" found nothing, so I take it
to be FTPS only; I did not read its upload code).

Seen by code search only, not read: OrcaSlicer (mirrors Studio's `try_emmc_print`, with a
`disable_emmc` switch), FoxForge (refuses internal storage without a `brtc://emmc/` URL),
bambuddy (section 2.4), DMontgomery40/bambu-printer-mcp (passes a `try_emmc_print` flag),
yanshay/SpoolEase (parses `brtc://emmc` URLs).

Not checked: bambu-farm, the rest of ha-bambulab, the persano plugin fork (cloned, not
read), Bambu Handy (closed). Bambu's own wiki page on internal storage: snippet only.
