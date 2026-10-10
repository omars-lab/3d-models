#!/usr/bin/env python3
"""Watch one plate print on the X2D: write what the printer says into the plate's print log, check
the print is still moving, take a chamber picture every few minutes and make a timelapse at the end.

    python3 .claude/skills/monitor-print/scripts/print_monitor.py <plate> [--every 30] [--lost-after 10]
        [--stall-after 15] [--snapshot-every 10]
    python3 .claude/skills/monitor-print/scripts/print_monitor.py <plate> --gif
    python3 .claude/skills/monitor-print/scripts/print_monitor.py <plate> --sent <hex> <tray> <grams> [--sent …]
    python3 .claude/skills/monitor-print/scripts/print_monitor.py <plate> --next [--after N] [--wait 9]
    python3 .claude/skills/monitor-print/scripts/print_monitor.py <plate> --look <frame> "<what it shows>"
    python3 .claude/skills/monitor-print/scripts/print_monitor.py <plate> --publish
    python3 .claude/skills/monitor-print/scripts/print_monitor.py --self-test

`<plate>` is a plate name (`sheets-04b`) or the path of its page. Run it from the main checkout
(the vault), like every `bambu` call, so the rows land in the log Omar opens from the page in
Obsidian.

Every `--every` seconds it asks `tools/bambu/bin/bambu status show --json` for the printer's
report (each call under a timeout) and compares it with the last one. A change worth knowing
becomes one row in the plate's print log, its own file beside the pages,
`docs/design/plates/print-logs/<plate>.md`. The first row makes the file and links it from the
page's frontmatter (`print_log: '[[print-logs/<plate>|print log]]'`). Rows are only ever added
at the end, and the plates gate (P10) refuses a change to one already on master:

    | Time (UTC) | Event | Layer | Done | What the printer said |

The events are the plates gate's `PRINT_EVENTS` (P10), so the monitor and the gate share one
list: `watching` (the first look), `preparing`, `printing`, `paused` (with the error code and
what it means), `resumed`, `progress` (25, 50, 75%), `error` (a new error with no pause),
`finished`, `failed`, `stopped` (the printer went idle, or moved to another job) and `lost` (no
reply for `--lost-after` minutes). The last four end the watch; a pause does not, because a
paused print is waiting on Omar and may resume.

**Is it moving?** While the printer says RUNNING, the layer or the percent should change. When
neither has for `--stall-after` minutes, the monitor writes a `stalled` row; when they move
again it writes `printing` ("moving again"). A stall does not end the watch either: the printer
has not given up, so the call is Omar's.

**Pictures.** Every `--snapshot-every` minutes (0 turns it off), and at every row it writes, it
saves one chamber frame with `bambu status camera` to `.bambu/monitor/<plate>/frames/<UTC>.jpg`.
When the watch ends it joins the frames into `.bambu/monitor/<plate>/timelapse.gif`; `--gif`
rebuilds that from the frames already there. A camera that does not answer is logged and
skipped: a missing picture never stops the watch.

**The send's row.** `--sent` writes one `sent` row and exits: the trays the send fed, each with
its color and the slice's grams for it (`fed #00ae42 from AMS 0 · slot 3, 27.28 g by the slice`;
a two-tray plate separates them with `; `). The send writes it, before the watch starts. The
shelf (`bambu shelf show`) takes those grams off the matching spool when the next `finished`,
`failed` or `stopped` row closes the print (order-driven-lab-design §9.2).

**The background watcher's side** (monitor-print's `watcher.md`). `--next` blocks until the run
log has a row, a picture, a timeout or the end past line `--after`, prints those lines and
`cursor=<n>` for the next call, and gives up after `--wait` minutes with `ev=quiet`, or at once
with `ev=watch_silent` (exit 3) when the log has gone three minutes with no line, which means
the watch itself has died. `--look` adds one line to `.bambu/monitor/<plate>/looks.md`: which
picture, and what the watcher saw in it.

**Publishing.** `--publish` puts the print on its page, small (Omar, 2026-10-10): the frames as
an animated WebP, 480 px wide, and the last frame as a WebP still, both with their metadata
stripped, into `docs/design/plates/<plate>-media/`, and a `## The print` section that shows them,
after `## Pictures`. It refuses, writing nothing, when zbarimg reads a code in any frame of either
(the repo is public, and the printer wears QR stickers), or when one is over 400 KB.
`--leave-out <frame>` (repeatable, the file name with or without `.jpg`) keeps a picture off the
page, for one that shows a person: sheets-04g-fit2's last frame caught Omar's hand lifting the
plate, and his call was to drop it (2026-10-10). A name that is not a frame refuses, so a typo
cannot publish the picture it meant to leave out.

A `finished` row is not a print record. The record (`docs/prints/`, the Timeline's `printed`
row) is written when the pieces are judged, as before.

The run log is `.bambu/monitor/<plate>.log` (gitignored): one line per step, a UTC time, the
pid and `ev=<event> key=value`, with a line before and after each poll so a stall shows where
it froze (`grep "ev=poll" <log> | tail -1`). Each new row is also printed to stdout as
`ev=row …`, each picture as `ev=snapshot path=…`, and the exit as `ev=exit …`, so a background
run can be followed by grepping them.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / ".claude" / "gates"))

import plates_gate as pg  # noqa: E402

BAMBU = ROOT / "tools" / "bambu" / "bin" / "bambu"
LOGS = ROOT / ".bambu" / "monitor"
POLL_TIMEOUT_S = 60
# One frame: the camera's own ffmpeg pull gives up at 20 s, plus the TLS relay and node start-up.
SNAPSHOT_TIMEOUT_S = 45
GIF_TIMEOUT_S = 120
TERMINAL = ("finished", "failed", "stopped", "lost")
MILESTONES = (25, 50, 75)

# What an error code means, in plain words. Only codes we have met and looked up: an unknown code
# is shown as its number, never guessed at. Source: Bambu's HMS list as mirrored in
# jmassardo/bambuddy-mobile hmsErrorCatalog.ts and hiwebsun0914 hms_errors.py (2026-10-03);
# 0300-400C from bambulab/BambuStudio issue #527 ("print cancelled from front panel");
# 0500-806E and 0500-8062 from Bambu Studio's own X2D list, Resources/hms/hms_en_20P.json (2026-10-07).
CANCELLED = "0300-400C"
KNOWN = {
    "0500-8051": "the plate on the bed is not the one the file was sliced for",
    "0500-806E": "the printer saw something on the bed and wants it checked and cleared",
    "0500-8062": "the printer could not see the plate's marker: check all four corners sit square, and keep strong light off the plate",
    CANCELLED: "the print was cancelled, from the printer's screen or an app",
}

INTRO = ("What the printer said while {page} printed, one row per change, written by the "
         "monitor-print skill's `print_monitor.py`. Rows are only ever added at the end: the "
         "plates gate refuses a change to a row already on master. A `finished` row is not a "
         "print record; that is written when the pieces are judged.")


def error_code(n) -> str | None:
    """`print_error` 83918929 → `0500-8051`; 0 or nothing → None."""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return None
    if n <= 0:
        return None
    h = f"{n:08X}"
    return f"{h[:4]}-{h[4:]}"


def said(code: str | None, state: str) -> str:
    if not code:
        return state
    return f"{code}: {KNOWN[code]}" if code in KNOWN else f"{code} (not looked up yet)"


def is_ours(frame: dict, plate: str) -> bool:
    return str(frame.get("subtask_name") or "") in (f"{plate}.plate", plate)


def step(st: dict, frame: dict | None, now: float, plate: str, lost_after_s: float,
         stall_after_s: float = 900) -> tuple[dict, list[tuple[str, str]]]:
    """One poll's worth of change. `st` is the watch so far; returns it updated and the new
    (event, what-the-printer-said) pairs, in order. `frame` None means the poll got no reply."""
    st = dict(st)
    rows: list[tuple[str, str]] = []
    if frame is None:
        if now - st.get("last_reply", st.setdefault("started", now)) >= lost_after_s:
            rows.append(("lost", f"no reply for {int((now - st.get('last_reply', st['started'])) // 60)} min"))
        return st, rows
    st["last_reply"] = now
    st.setdefault("started", now)
    state = str(frame.get("gcode_state") or "UNKNOWN")
    code = error_code(frame.get("print_error"))
    st["frame"] = frame

    if not is_ours(frame, plate):
        if st.get("seen"):
            rows.append(("stopped", f"the printer moved on to {frame.get('subtask_name') or 'nothing'} ({state})"))
        elif now - st["started"] >= lost_after_s:
            rows.append(("lost", f"{plate} never showed up; the printer is on "
                                 f"{frame.get('subtask_name') or 'nothing'} ({state})"))
        return st, rows

    prev = st.get("state")
    if not st.get("seen"):
        st["seen"] = True
        rows.append(("watching", said(code, state)))
    elif state != prev:
        if state in ("PREPARE", "SLICING"):
            rows.append(("preparing", state))
        elif state == "RUNNING":
            rows.append(("resumed" if prev == "PAUSE" else "printing", state))
        elif state == "PAUSE":
            rows.append(("paused", said(code, state)))
        elif state == "FINISH":
            rows.append(("finished", state))
        elif state == "FAILED":
            # A cancel reports FAILED too (sheets-04b, 2026-10-03); it is a stop, not a failure.
            rows.append(("stopped" if code == CANCELLED else "failed", said(code, state)))
        elif state == "IDLE":
            rows.append(("stopped", "the printer went idle"))
    if code and code != st.get("code") and not any(e in ("paused", "failed", "stopped", "watching") for e, _ in rows):
        rows.append(("error", said(code, state)))
    st["code"] = code

    if state == "RUNNING" and not any(e in TERMINAL for e, _ in rows):
        try:
            pct = int(frame.get("mc_percent") or 0)
        except (TypeError, ValueError):
            pct = 0
        done = st.setdefault("milestones", [])
        for m in MILESTONES:
            if pct >= m and m not in done:
                done.append(m)
                if m == max(x for x in MILESTONES if pct >= x):
                    rows.append(("progress", f"{m}%"))

    # Is it moving? RUNNING with the same layer and percent for the whole window is a stall. The
    # clock starts again on every move and on every return to RUNNING (a resume, the first layer).
    if state == "RUNNING" and not any(e in TERMINAL for e, _ in rows):
        mark = (frame.get("layer_num"), frame.get("mc_percent"))
        if mark != st.get("mark") or prev != "RUNNING":
            if st.get("stalled") and prev == "RUNNING":
                rows.append(("printing", f"moving again: layer {mark[0]}, {mark[1]}%"))
            st["stalled"], st["mark"], st["moved_at"] = False, mark, now
        elif not st.get("stalled") and now - st["moved_at"] >= stall_after_s:
            st["stalled"] = True
            rows.append(("stalled", f"no new layer or percent for {int((now - st['moved_at']) // 60)} min "
                                    f"(layer {mark[0]}, {mark[1]}%)"))
    st["state"] = state
    return st, rows


# ---------------------------------------------------------------------------
# the page
# ---------------------------------------------------------------------------

def cell(s: str) -> str:
    return re.sub(r"\s+", " ", str(s).replace("|", "/")).strip()


def row_line(when: str, event: str, frame: dict | None, text: str) -> str:
    f = frame or {}
    layer = f"{f.get('layer_num', '?')}/{f.get('total_layer_num', '?')}" if frame else ""
    done = f"{f.get('mc_percent', '?')}%" if frame else ""
    return f"| {when} | {event} | {layer} | {done} | {cell(text)} |"


def sent_line(when: str, trays: list[tuple[str, str, float]]) -> str:
    """The send's row: each tray it fed, its color and the slice's grams for it."""
    fed = []
    for hex_, tray, grams in trays:
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", hex_):
            raise ValueError(f"{hex_!r} is not a #rrggbb color")
        if not tray.strip() or "," in tray or ";" in tray:
            raise ValueError(f"tray {tray!r} must be a name with no comma or semicolon")
        if not grams >= 0:
            raise ValueError(f"grams for {tray} must be zero or more, not {grams}")
        fed.append(f"{hex_.lower()} from {tray.strip()}, {grams:g} g by the slice")
    if not fed:
        raise ValueError("a send feeds at least one tray")
    return row_line(when, "sent", None, "fed " + "; ".join(fed))


def new_log(plate: str) -> str:
    """A print log with no rows yet: its plate, a link back to the page, the table header."""
    return (f"---\nplate: {plate}\n---\n\n# {plate} — print log\n\n"
            f"{INTRO.format(page=f'[{plate}](../{plate}.md)')}\n\n"
            f"{pg.PRINT_LOG_HEAD}\n|---|---|---|---|---|\n")


def add_log_row(text: str, line: str) -> str:
    """The log with `line` added at the end. The table is the last thing in the file, and rows
    are only ever added there (P10 checks the log is append-only)."""
    return text.rstrip("\n") + "\n" + line + "\n"


def link_page(text: str, plate: str) -> str:
    """The page with `print_log:` in its frontmatter, after `plate:`, when it has none."""
    end = text.find("\n---", 4)
    if re.search(r"^print_log:", text[:end], flags=re.MULTILINE):
        return text
    return re.sub(r"^(plate: .*)$", rf"\1\nprint_log: '{pg.log_link(plate)}'", text, count=1,
                  flags=re.MULTILINE)


def page_of(plate: str) -> Path:
    p = Path(plate)
    return p.resolve() if p.suffix == ".md" else pg.PLATES / f"{plate}.md"


def log_of(page: Path) -> Path:
    return page.parent / pg.LOGS / f"{page.stem}.md"


def append_to_log(page: Path, line: str) -> None:
    """One row onto the plate's log; the first row makes the log and links it from the page."""
    log = log_of(page)
    if not log.is_file():
        log.parent.mkdir(exist_ok=True)
        log.write_text(new_log(page.stem), encoding="utf-8")
    log.write_text(add_log_row(log.read_text(encoding="utf-8"), line), encoding="utf-8")
    text = page.read_text(encoding="utf-8")
    linked = link_page(text, page.stem)
    if linked != text:
        page.write_text(linked, encoding="utf-8")


# ---------------------------------------------------------------------------
# the loop
# ---------------------------------------------------------------------------

class Log:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path

    def __call__(self, ev: str, **kv) -> None:
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        parts = [f"{k}={v}" if k != "msg" else f'msg="{v}"' for k, v in kv.items()]
        with self.path.open("a", encoding="utf-8") as f:
            f.write(" ".join([now, f"pid={os.getpid()}", f"ev={ev}", *parts]) + "\n")


def poll(log: Log) -> dict | None:
    log("poll_start")
    try:
        r = subprocess.run([str(BAMBU), "status", "show", "--json"], capture_output=True,
                           text=True, timeout=POLL_TIMEOUT_S, cwd=ROOT)
    except subprocess.TimeoutExpired:
        log("poll_timeout", timeout_s=POLL_TIMEOUT_S)
        return None
    if r.returncode != 0:
        log("poll_failed", rc=r.returncode, msg=cell(r.stderr)[:200])
        return None
    try:
        frame = json.loads(r.stdout)
    except json.JSONDecodeError:
        log("poll_failed", rc=0, msg="the reply was not JSON")
        return None
    log("poll_done", state=frame.get("gcode_state"), layer=frame.get("layer_num"),
        pct=frame.get("mc_percent"), err=error_code(frame.get("print_error")) or 0,
        job=cell(frame.get("subtask_name") or "none").replace(" ", "_"))
    return frame


def snapshot_due(last: float | None, now: float, every_s: float) -> bool:
    return every_s > 0 and (last is None or now - last >= every_s)


def frames_dir(name: str) -> Path:
    return LOGS / name / "frames"


def snapshot(name: str, log: Log) -> Path | None:
    """One chamber frame into the plate's frames folder, or None (logged) when the camera fails."""
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = frames_dir(name) / f"{stamp}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    log("snapshot_start", path=out.name)
    try:
        r = subprocess.run([str(BAMBU), "status", "camera", "-o", str(out)], capture_output=True,
                           text=True, timeout=SNAPSHOT_TIMEOUT_S, cwd=ROOT)
    except subprocess.TimeoutExpired:
        log("snapshot_timeout", timeout_s=SNAPSHOT_TIMEOUT_S)
        return None
    if r.returncode != 0 or not out.is_file():
        log("snapshot_failed", rc=r.returncode, msg=cell(r.stderr)[:200])
        return None
    log("snapshot_done", path=out.name, bytes=out.stat().st_size)
    print(f"ev=snapshot plate={name} path={out}", flush=True)
    return out


def gif_cmd(frames: list[Path], out: Path) -> list[str]:
    """Half a second a frame, the last held two seconds so the finished plate reads."""
    return ["magick", "-loop", "0", "-delay", "50", *map(str, frames[:-1]),
            "-delay", "200", str(frames[-1]), "-resize", "640x", "-layers", "Optimize", str(out)]


def make_gif(name: str, log: Log) -> Path | None:
    frames = sorted(frames_dir(name).glob("*.jpg"))
    if len(frames) < 2:
        log("gif_skipped", frames=len(frames))
        return None
    out = LOGS / name / "timelapse.gif"
    log("gif_start", frames=len(frames))
    try:
        r = subprocess.run(gif_cmd(frames, out), capture_output=True, text=True, timeout=GIF_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        log("gif_timeout", timeout_s=GIF_TIMEOUT_S)
        return None
    except FileNotFoundError:
        log("gif_failed", msg="magick is not on PATH (brew install imagemagick)")
        return None
    if r.returncode != 0:
        log("gif_failed", rc=r.returncode, msg=cell(r.stderr)[:200])
        return None
    log("gif_done", path=out, frames=len(frames), bytes=out.stat().st_size)
    print(f"ev=gif plate={name} frames={len(frames)} path={out}", flush=True)
    return out


# ---------------------------------------------------------------------------
# publishing: the timelapse and the finished plate onto the plate's page
# ---------------------------------------------------------------------------

# Omar, 2026-10-10: publish them, but small. Measured on sheets-04g-fit2's frames: an animated WebP
# at 480 px is about 120 KB where the 640 px GIF was 1.4 MB, and a WebP still about 10 KB where a
# PNG was 250 KB. The cap stops a long print from growing the repo by megabytes unnoticed.
MEDIA_WIDTH = 480
MEDIA_QUALITY = 60
MEDIA_MAX_BYTES = 400_000
PUBLISH_TIMEOUT_S = 180
PRINT_HEADING = "## The print"


def media_of(page: Path) -> Path:
    return page.parent / f"{page.stem}-media"


def webp_cmd(frames: list[Path], out: Path) -> list[str]:
    """The GIF's timing, as an animated WebP: smaller, and with no picture metadata."""
    return ["magick", "-loop", "0", "-delay", "50", *map(str, frames[:-1]),
            "-delay", "200", str(frames[-1]), "-resize", f"{MEDIA_WIDTH}x", "-strip",
            "-quality", str(MEDIA_QUALITY), str(out)]


def still_cmd(frame: Path, out: Path) -> list[str]:
    return ["magick", str(frame), "-resize", f"{MEDIA_WIDTH}x", "-strip",
            "-quality", str(MEDIA_QUALITY), str(out)]


def codes_in(paths: list[Path]) -> int:
    """How many codes zbarimg reads in these pictures, every frame of an animated one. The repo is
    public and the printer wears QR stickers, so a picture with a readable code is never published.
    What a code says is never printed: it may be the printer's serial.

    One file per call: given several, zbarimg exits 4 ("none found") when any one of them has no
    code, so a code in the timelapse hid behind a clean still (found by the self-test)."""
    n = 0
    for p in paths:
        r = subprocess.run(["zbarimg", "--quiet", "--raw", str(p)], capture_output=True, text=True,
                           timeout=PUBLISH_TIMEOUT_S)
        if r.returncode not in (0, 4):
            raise RuntimeError(f"zbarimg exited {r.returncode} on {p.name}: {cell(r.stderr)[:200]}")
        n += len([ln for ln in r.stdout.splitlines() if ln.strip()])
    return n


def print_section(name: str, frames: list[Path], left_out: int = 0) -> str:
    def hm(f: Path) -> str:
        m = re.match(r"\d{8}T(\d\d)(\d\d)\d\dZ$", f.stem)
        return f"{m[1]}:{m[2]}" if m else f.stem
    dropped = (f" {left_out} picture{'s' if left_out > 1 else ''} with someone at the printer "
               f"left out." if left_out else "")
    return (f"{PRINT_HEADING}\n\n"
            f"The print as the chamber camera saw it: {len(frames)} pictures from {hm(frames[0])} to "
            f"{hm(frames[-1])} UTC, half a second each, the last held.{dropped} Made by the monitor-print "
            f"skill's `print_monitor.py --publish`; what the printer said is in the print log.\n\n"
            f"![{name} printing, as the chamber camera saw it]({name}-media/timelapse.webp)\n\n"
            f"![{name} finished, on the bed]({name}-media/finished.webp)\n")


def with_print_section(text: str, section: str) -> str:
    """The page with its `## The print` section replaced, or added after `## Pictures` (before
    `## Your call` when it has no Pictures, at the end when it has neither)."""
    def span(heading: str) -> tuple[int, int] | None:
        m = re.search(rf"^{re.escape(heading)}\b.*$", text, flags=re.MULTILINE)
        if not m:
            return None
        nxt = re.search(r"^## ", text[m.end():], flags=re.MULTILINE)
        return m.start(), (m.end() + nxt.start()) if nxt else len(text)
    block = section.rstrip("\n") + "\n\n"
    if s := span(PRINT_HEADING):
        out = text[:s[0]] + block + text[s[1]:]
    elif s := span("## Pictures"):
        out = text[:s[1]] + block + text[s[1]:]
    elif m := re.search(r"^## Your call\b", text, flags=re.MULTILINE):
        out = text[:m.start()] + block + text[m.start():]
    else:
        out = text.rstrip("\n") + "\n\n" + block
    return out.rstrip("\n") + "\n"


def publish(plate: str, log: Log, leave_out: list[str] = ()) -> int:
    """Make `<plate>-media/timelapse.webp` and `finished.webp` beside the page and show both in its
    `## The print` section, without the frames named in `leave_out`. Refuses, writing nothing,
    when a code reads in either, one is over the cap, or a left-out name is not a frame."""
    page = page_of(plate)
    name = page.stem
    if not page.is_file():
        print(f"print-monitor: no plate page {page}", file=sys.stderr)
        return 2
    taken = sorted(frames_dir(name).glob("*.jpg"))
    drop = {Path(x).name if x.endswith(".jpg") else f"{Path(x).name}.jpg" for x in leave_out}
    if unknown := drop - {f.name for f in taken}:
        print(f"print-monitor: not a picture of {name}: {', '.join(sorted(unknown))}; nothing "
              f"published", file=sys.stderr)
        return 2
    frames = [f for f in taken if f.name not in drop]
    if len(frames) < 2:
        print(f"print-monitor: {len(frames)} pictures of {name}; a timelapse needs two", file=sys.stderr)
        return 2
    work = LOGS / name / "publish"
    work.mkdir(parents=True, exist_ok=True)
    made = {"timelapse.webp": webp_cmd(frames, work / "timelapse.webp"),
            "finished.webp": still_cmd(frames[-1], work / "finished.webp")}
    log("publish_start", frames=len(frames), left_out=len(drop))
    try:
        for cmd in made.values():
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=PUBLISH_TIMEOUT_S)
            if r.returncode != 0:
                log("publish_failed", rc=r.returncode, msg=cell(r.stderr)[:200])
                print(f"print-monitor: magick failed: {cell(r.stderr)[:200]}", file=sys.stderr)
                return 1
        codes = codes_in([work / f for f in made])
    except subprocess.TimeoutExpired:
        log("publish_timeout", timeout_s=PUBLISH_TIMEOUT_S)
        return 1
    except (FileNotFoundError, RuntimeError) as e:
        log("publish_failed", msg=cell(str(e))[:200])
        print(f"print-monitor: {e} (brew install imagemagick zbar)", file=sys.stderr)
        return 1
    if codes:
        log("publish_refused", codes=codes)
        print(f"print-monitor: {codes} readable code(s) in the pictures; nothing published. Look at "
              f"{work}, find the frame and name it with --leave-out.", file=sys.stderr)
        return 1
    big = {f: (work / f).stat().st_size for f in made if (work / f).stat().st_size > MEDIA_MAX_BYTES}
    if big:
        log("publish_refused", too_big=",".join(big))
        print(f"print-monitor: over {MEDIA_MAX_BYTES} bytes: {big}; nothing published", file=sys.stderr)
        return 1
    media = media_of(page)
    media.mkdir(exist_ok=True)
    for f in made:
        (media / f).write_bytes((work / f).read_bytes())
    page.write_text(with_print_section(page.read_text(encoding="utf-8"), print_section(name, frames, len(drop))),
                    encoding="utf-8")
    sizes = " ".join(f"{f.split('.')[0]}_bytes={(media / f).stat().st_size}" for f in made)
    log("publish_done", frames=len(frames), left_out=len(drop), msg=sizes)
    print(f"ev=publish plate={name} frames={len(frames)} left_out={len(drop)} {sizes} dir={media}",
          flush=True)
    return 0


# ---------------------------------------------------------------------------
# the background watcher's side: wait for the next thing worth a look, note what a picture showed
# ---------------------------------------------------------------------------

# The run-log events a watcher wakes for: a row, a picture, the end, and any call that timed out.
WAKE = re.compile(r" ev=(row|snapshot_done|exit|gif_done|gif_failed|gif_skipped|\w+_timeout) ")
# The watch polls every 30 s and logs before and after each poll, so this long with no line at
# all means the watch itself has died, not the printer.
SILENT_AFTER_S = 180


def next_events(lines: list[str], after: int) -> tuple[list[str], int]:
    """The wake-worthy lines past line `after` (1-based count already seen), and the new count."""
    return [ln for ln in lines[after:] if WAKE.search(ln + " ")], len(lines)


def wait_next(name: str, after: int, wait_s: float, every: float = 5) -> int:
    """Block until the run log has a line worth a look past `after`, or `wait_s` passes.

    Prints each such line, then `cursor=<n>` to pass as `--after` next time. Prints `ev=quiet`
    when the time ran out with nothing new, and `ev=watch_silent` when the log has had no line at
    all for SILENT_AFTER_S (the watch process is gone). Fits in one 10-minute Bash call."""
    path = LOGS / f"{name}.log"
    end = time.time() + wait_s
    while True:
        lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
        hits, cursor = next_events(lines, after)
        if hits:
            print("\n".join(hits))
            print(f"cursor={cursor}")
            return 0
        if path.is_file() and time.time() - path.stat().st_mtime > SILENT_AFTER_S:
            print(f"ev=watch_silent plate={name} quiet_s={int(time.time() - path.stat().st_mtime)}")
            print(f"cursor={cursor}")
            return 3
        if time.time() >= end:
            print(f"ev=quiet plate={name}")
            print(f"cursor={cursor}")
            return 0
        time.sleep(every)


def looks_of(name: str) -> Path:
    return LOGS / name / "looks.md"


def add_look(name: str, frame: str, note: str) -> str:
    """One line in `.bambu/monitor/<plate>/looks.md`: which picture, what the watcher saw in it."""
    when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    line = f"- {when} `{Path(frame).name}`: {cell(note)}"
    p = looks_of(name)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return line


def watch(plate: str, every: float, lost_after_s: float, stall_after_s: float, snap_s: float) -> int:
    page = page_of(plate)
    name = page.stem
    if not page.is_file():
        print(f"print-monitor: no plate page {page}", file=sys.stderr)
        return 2
    log = Log(LOGS / f"{name}.log")
    log("start", plate=name, every_s=int(every), lost_after_s=int(lost_after_s),
        stall_after_s=int(stall_after_s), snapshot_every_s=int(snap_s))
    st: dict = {}
    last_shot: float | None = None
    while True:
        frame = poll(log)
        now = time.time()
        st, rows = step(st, frame, now, name, lost_after_s, stall_after_s)
        ours = bool(frame and is_ours(frame, name))
        when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
        end = None
        for event, text in rows:
            append_to_log(page, row_line(when, event, frame if ours else None, text))
            log("row", event=event, msg=cell(text))
            print(f"ev=row plate={name} event={event} msg=\"{cell(text)}\"", flush=True)
            if event in TERMINAL:
                end = event
                break
        # A picture at every row (the moment worth seeing) and on the clock while it is ours.
        if snap_s > 0 and (rows or (ours and snapshot_due(last_shot, now, snap_s))):
            snapshot(name, log)
            last_shot = now
        if end:
            if snap_s > 0:
                make_gif(name, log)
            log("exit", reason=end)
            print(f"ev=exit plate={name} reason={end}", flush=True)
            return 0 if end == "finished" else 1
        time.sleep(every)


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

def _f(state, layer=0, pct=0, err=0, job="sheets-04b.plate"):
    return {"gcode_state": state, "layer_num": layer, "total_layer_num": 20, "mc_percent": pct,
            "print_error": err, "subtask_name": job}


def _run(frames, lost=600):
    st, out, t = {}, [], 0.0
    for fr in frames:
        st, rows = step(st, fr, t, "sheets-04b", lost)
        out += [e for e, _ in rows]
        t += 30
    return out


def self_test() -> int:
    import tempfile
    fails = 0

    def check(ok: bool, label: str, why: str = "") -> None:
        nonlocal fails
        fails += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" — {why}"))

    got = error_code(83918929)
    check(got == "0500-8051", "print_error 83918929 reads 0500-8051", got)
    check(error_code(0) is None and error_code(None) is None, "no error reads as none")

    want = ["watching", "printing", "progress", "progress", "finished"]
    got = _run([_f("PREPARE"), _f("RUNNING", 1, 3), _f("RUNNING", 6, 30), _f("RUNNING", 12, 60),
                _f("RUNNING", 13, 62), _f("FINISH", 20, 100)])
    check(got == want, "a clean print: one row per change, a milestone once each", got)

    got = _run([_f("RUNNING", 1, 3), _f("RUNNING", 16, 80)])
    check(got.count("progress") == 1, "a jump past two milestones writes one progress row", got)

    got = _run([_f("PREPARE"), _f("PAUSE", err=83918929), _f("PAUSE", err=83918929),
                _f("RUNNING", 1, 2)])
    check(got == ["watching", "paused", "resumed"],
          "a pause then a resume (the sheets-04b shape); the pause does not end the watch", got)
    st, rows = step({}, _f("PREPARE"), 0, "sheets-04b", 600)
    st, rows = step(st, _f("PAUSE", err=83918929), 30, "sheets-04b", 600)
    check(rows == [("paused", "0500-8051: " + KNOWN["0500-8051"])],
          "a paused row says the code and what it means", rows)

    st, rows = step({}, _f("PAUSE", err=0x0300_4FFF), 0, "sheets-04b", 600)
    check(rows == [("watching", "0300-4FFF (not looked up yet)")],
          "an unknown code is shown as its number, never guessed at", rows)

    st, rows = step({}, _f("PAUSE", err=83918929), 0, "sheets-04b", 600)
    st, rows = step(st, _f("FAILED", err=0x0300400C), 30, "sheets-04b", 600)
    check(rows == [("stopped", "0300-400C: " + KNOWN[CANCELLED])],
          "a cancel reports FAILED but is a stop (the sheets-04b end, 2026-10-03)", rows)

    got = _run([_f("RUNNING", 3, 10), _f("RUNNING", 4, 12, err=0x0700_2000)])
    check(got == ["watching", "error"], "a new error with no pause is its own row", got)

    got = _run([_f("RUNNING", 3, 10), _f("IDLE", job="")])
    check(got == ["watching", "stopped"], "the printer moved on: stopped ends the watch", got)
    got = _run([_f("RUNNING", 3, 10), _f("FAILED", 3, 10, err=83918929)])
    check(got == ["watching", "failed"], "a failed print ends the watch", got)

    got = _run([_f("FINISH", job="sheets-04.plate")] * 3, lost=60)
    check(got == ["lost"], "a plate that never shows up is lost, with no rows before it", got)
    st, rows = step({}, _f("RUNNING", 3, 10), 0, "sheets-04b", 300)
    st, rows = step(st, None, 200, "sheets-04b", 300)
    check(rows == [], "a missed poll inside the window writes nothing", rows)
    st, rows = step(st, None, 330, "sheets-04b", 300)
    check([e for e, _ in rows] == ["lost"], "no reply for the whole window is lost", rows)

    # Is it moving: a stall after the window, once; moving again says so; a pause resets the clock.
    st, rows = step({}, _f("RUNNING", 5, 20), 0, "sheets-04b", 600, 900)
    st, rows = step(st, _f("RUNNING", 5, 20), 600, "sheets-04b", 600, 900)
    check(rows == [], "the same layer and percent inside the window writes nothing", rows)
    st, rows = step(st, _f("RUNNING", 5, 20), 900, "sheets-04b", 600, 900)
    check([e for e, _ in rows] == ["stalled"] and "15 min" in rows[0][1],
          "the same layer and percent for the whole window is a stall", rows)
    st, rows = step(st, _f("RUNNING", 5, 20), 1800, "sheets-04b", 600, 900)
    check(rows == [], "a stall is written once, not every poll", rows)
    st, rows = step(st, _f("RUNNING", 6, 21), 1830, "sheets-04b", 600, 900)
    check([e for e, _ in rows] == ["printing"] and "moving again" in rows[0][1],
          "a stalled print that moves again says so", rows)
    got = []
    st = {}
    for t, fr in [(0, _f("RUNNING", 5, 20)), (600, _f("PAUSE", 5, 20)), (1200, _f("RUNNING", 5, 20)),
                  (1800, _f("RUNNING", 5, 20))]:
        st, rows = step(st, fr, t, "sheets-04b", 600, 900)
        got += [e for e, _ in rows]
    check(got == ["watching", "paused", "resumed"],
          "time paused is not a stall: the clock starts again on the resume", got)
    st, rows = step({}, _f("PREPARE"), 0, "sheets-04b", 600, 900)
    st, rows = step(st, _f("PREPARE"), 1800, "sheets-04b", 600, 900)
    check(rows == [], "heating up is not a stall: only RUNNING is watched for movement", rows)

    # Pictures on the clock, and the timelapse command.
    check(snapshot_due(None, 0, 600) and not snapshot_due(0, 599, 600) and snapshot_due(0, 600, 600),
          "the first picture is at once, then one every window")
    check(not snapshot_due(None, 0, 0), "--snapshot-every 0 takes no pictures")
    cmd = gif_cmd([Path("a.jpg"), Path("b.jpg"), Path("c.jpg")], Path("t.gif"))
    check(cmd[:5] == ["magick", "-loop", "0", "-delay", "50"]
          and cmd[cmd.index("c.jpg") - 2:cmd.index("c.jpg")] == ["-delay", "200"] and cmd[-1] == "t.gif",
          "the GIF loops, half a second a frame, the last frame held", cmd)

    every = {e for e, _ in [("watching", 0), ("sent", 0)]} | set(TERMINAL) | {
        "preparing", "printing", "paused", "resumed", "progress", "error", "stalled"}
    check(every <= set(pg.PRINT_EVENTS), "every event the monitor writes is one the gate knows",
          sorted(every - set(pg.PRINT_EVENTS)))

    # The log: its own file beside the pages, made on the first row and linked from the page's
    # frontmatter; rows append in order, and the gate reads it back clean.
    page_text = ("---\nplate: x\nstage: sent\n---\n\n# x\n\n## Timeline\n\n"
                 "| Date | What happened | Where |\n|---|---|---|\n| 2026-10-03 | sent | x |\n")
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "x.md"
        p.write_text(page_text, encoding="utf-8")
        append_to_log(p, row_line("2026-10-03 21:02", "watching", _f("PREPARE"), "PREPARE"))
        append_to_log(p, row_line("2026-10-03 21:09", "paused", _f("PAUSE"), "0500-8051: a | b"))
        log = log_of(p).read_text(encoding="utf-8")
        rows, problem = pg.print_log(log)
        check(problem is None and [e for _, e in rows] == ["watching", "paused"],
              "the print log reads back through the gate", f"{problem} {rows}")
        check("a / b" in log, "a | in the printer's words cannot break the table")
        check("[x](../x.md)" in log, "the log links back to its page")
        linked = p.read_text(encoding="utf-8")
        check(linked == page_text.replace("plate: x\n", f"plate: x\nprint_log: '{pg.log_link('x')}'\n"),
              "the page gains its print_log link once, and nothing else changes", linked[:80])
        found = pg.check_print_logs(Path(tmp), pg.read_pages(Path(tmp)))
        check(not found, "the gate finds nothing wrong with the log and the link", found)
        log_of(p).write_text(log.replace("| watching |", "| jammed |"), encoding="utf-8")
        found = pg.check_print_logs(Path(tmp), pg.read_pages(Path(tmp)))
        check(any("event 'jammed'" in f for f in found), "and the gate does read the log", found)

    # The send's row: the trays and grams in the words the shelf reads, before the monitor's rows.
    line = sent_line("2026-10-04 18:35", [("#00AE42", "AMS 0 · slot 3", 27.28), ("#000000", "AMS 0 · slot 0", 3.0)])
    check(line == "| 2026-10-04 18:35 | sent |  |  | fed #00ae42 from AMS 0 · slot 3, 27.28 g by the slice; "
                  "#000000 from AMS 0 · slot 0, 3 g by the slice |",
          "a sent row names each tray, its color and its grams", line)
    for bad in ([("green", "AMS 0 · slot 3", 27.0)], [("#00ae42", "AMS 1, slot 4", 27.0)], []):
        try:
            sent_line("2026-10-04 18:35", bad)
            check(False, f"a sent row refuses {bad}", "it wrote one")
        except ValueError:
            check(True, f"a sent row refuses {bad}")
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "x.md"
        p.write_text(page_text, encoding="utf-8")
        append_to_log(p, line)
        append_to_log(p, row_line("2026-10-04 18:37", "watching", _f("RUNNING"), "RUNNING"))
        found = pg.check_print_logs(Path(tmp), pg.read_pages(Path(tmp)))
        check(not found, "a log that starts with the send's row reads back clean through the gate", found)

    # The background watcher wakes for rows, pictures, the end and timeouts, never for polls.
    log_lines = [
        "2026-10-10T15:23:00Z pid=1 ev=poll_start",
        "2026-10-10T15:23:01Z pid=1 ev=poll_done state=RUNNING layer=3 pct=8 err=0 job=x",
        "2026-10-10T15:23:37Z pid=1 ev=snapshot_done path=20261010T152335Z.jpg bytes=99074",
        '2026-10-10T15:32:11Z pid=1 ev=row event=progress msg="25%"',
        "2026-10-10T15:33:00Z pid=1 ev=poll_timeout timeout_s=60",
        "2026-10-10T16:20:00Z pid=1 ev=exit reason=finished",
    ]
    hits, cur = next_events(log_lines, 0)
    check([h.split(" ev=")[1].split(" ")[0] for h in hits] == ["snapshot_done", "row", "poll_timeout", "exit"]
          and cur == 6, "the watcher wakes for a picture, a row, a timeout and the end, not a poll", hits)
    hits, cur = next_events(log_lines, 3)
    check(len(hits) == 3 and hits[0].endswith('msg="25%"') and cur == 6,
          "the cursor skips what the watcher has already seen", hits)
    check(next_events(log_lines[:2], 0) == ([], 2), "polls alone wake nobody")
    with tempfile.TemporaryDirectory() as tmp:
        global LOGS
        saved, LOGS = LOGS, Path(tmp)
        try:
            line = add_look("x", "/a/b/20261010T152335Z.jpg", "first layer down | flat")
            check(line.endswith("`20261010T152335Z.jpg`: first layer down / flat")
                  and looks_of("x").read_text(encoding="utf-8") == line + "\n",
                  "a look names its picture and keeps a | from breaking the line", line)
        finally:
            LOGS = saved

    # Publishing: the section lands after Pictures once, and a second publish replaces it.
    body = ("---\nplate: x\n---\n\n# x\n\n## Pictures\n\n![bed](x-media/bed.png)\n\n"
            "## What the slice lays down\n\nwalls\n\n## Your call\n\n- [ ] Approve\n")
    shots = [Path("20261010T151500Z.jpg"), Path("20261010T162000Z.jpg")]
    once = with_print_section(body, print_section("x", shots))
    check(once.index("## Pictures") < once.index(PRINT_HEADING) < once.index("## What the slice")
          and "2 pictures from 15:15 to 16:20 UTC" in once and "](x-media/timelapse.webp)" in once,
          "the print's section goes after the pictures, with both media linked", once)
    twice = with_print_section(once, print_section("x", shots[:1] * 3))
    check(twice.count(PRINT_HEADING) == 1 and "3 pictures" in twice
          and twice.replace(print_section("x", shots[:1] * 3), "") == once.replace(print_section("x", shots), ""),
          "publishing again replaces the section and leaves the rest of the page alone", twice)
    bare = with_print_section("# x\n\n## Your call\n\n- [ ] Approve\n", print_section("x", shots))
    check(bare.index(PRINT_HEADING) < bare.index("## Your call"), "no Pictures: before Your call", bare)
    cmd = webp_cmd([Path("a.jpg"), Path("b.jpg"), Path("c.jpg")], Path("t.webp"))
    check(cmd[cmd.index("c.jpg") - 2:cmd.index("c.jpg")] == ["-delay", "200"] and "-strip" in cmd
          and f"{MEDIA_WIDTH}x" in cmd, "the WebP holds the last frame, is 480 px and drops metadata", cmd)

    # The by-design refusal, on real pictures: a frame showing a QR code (this one says
    # "print-monitor self-test", drawn by segno) in the middle of a timelapse publishes nothing.
    qr = ["#######..###.##...#######", "#.....#....####...#.....#", "#.###.#..###...##.#.###.#",
          "#.###.#.#.##.####.#.###.#", "#.###.#.#.#.##..#.#.###.#", "#.....#..##...#.#.#.....#",
          "#######.#.#.#.#.#.#######", ".........#..#.#.#........", "##...###.##.####....##...",
          ".#...#.#..#....#...##....", "##...#####.##.###...#..##", "####...#..##...#.#####...",
          "#.....##.##....#..##.#.##", "#.##......#.#..###.#.###.", "#..#####.#....##.########",
          "#.#....#..#.#...#.##.##.#", "#..####.#...#########.#.#", "........#.#...#.#...##.#.",
          "#######.#...#.#.#.#.###.#", "#.....#.#.##..#.#...#..#.", "#.###.#..################",
          "#.###.#..##.#....##..#.##", "#.###.#...#.#.##...#....#", "#.....#.##..#..###.#.#..#",
          "#######.#.#####.#....#..#"]
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        saved_logs, saved_plates = LOGS, pg.PLATES
        LOGS, pg.PLATES = t / "monitor", t / "plates"
        try:
            pg.PLATES.mkdir()
            (pg.PLATES / "x.md").write_text(body, encoding="utf-8")
            fr = frames_dir("x")
            fr.mkdir(parents=True)
            side = len(qr) + 8
            pbm = t / "qr.pbm"
            pbm.write_text(f"P1\n{side} {side}\n" + "\n".join(
                " ".join("1" if c == "#" else "0" for c in "...." + row + "....")
                for row in ["." * len(qr)] * 4 + qr + ["." * len(qr)] * 4) + "\n", encoding="ascii")
            for stamp, src in (("20261010T151500Z", None), ("20261010T152500Z", pbm),
                               ("20261010T153500Z", None)):
                art = ["xc:gray60"] if src is None else [str(src), "-scale", "400x400"]
                subprocess.run(["magick", "-size", "800x600", "xc:gray60", *art, "-gravity", "center",
                                "-composite", str(fr / f"{stamp}.jpg")], check=True, timeout=60)
            quiet = Log(t / "x.log")
            rc = publish("x", quiet)
            check(rc == 1 and not media_of(pg.PLATES / "x.md").exists()
                  and (pg.PLATES / "x.md").read_text(encoding="utf-8") == body,
                  "a QR code in a middle frame: refused, nothing written", f"rc={rc}")
            rc = publish("x", quiet, ["20261010T152600Z"])
            check(rc == 2 and not media_of(pg.PLATES / "x.md").exists()
                  and (pg.PLATES / "x.md").read_text(encoding="utf-8") == body,
                  "a left-out name that is no frame (a typo): refused, nothing written", f"rc={rc}")
            rc = publish("x", quiet, ["20261010T152500Z"])
            media = media_of(pg.PLATES / "x.md")
            sizes = [(media / f).stat().st_size for f in ("timelapse.webp", "finished.webp")
                     if (media / f).is_file()]
            text = (pg.PLATES / "x.md").read_text(encoding="utf-8")
            check(rc == 0 and len(sizes) == 2 and max(sizes) <= MEDIA_MAX_BYTES
                  and "2 pictures from 15:15 to 15:35 UTC" in text
                  and "1 picture with someone at the printer left out." in text
                  and (fr / "20261010T152500Z.jpg").is_file(),
                  "that frame left out by name: both WebPs beside the page, under the cap, the "
                  "section saying one was left out, and the frame itself kept in .bambu/",
                  f"rc={rc} sizes={sizes}")
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            check(False, "publishing needs magick and zbarimg", f"{e} (brew install imagemagick zbar)")
        finally:
            LOGS, pg.PLATES = saved_logs, saved_plates

    print(f"self-test: {'PASS' if not fails else f'FAIL ({fails})'}")
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("plate", nargs="?")
    ap.add_argument("--every", type=float, default=30, help="seconds between polls (default 30)")
    ap.add_argument("--lost-after", type=float, default=10,
                    help="minutes with no reply (or no sign of the plate) before giving up (default 10)")
    ap.add_argument("--stall-after", type=float, default=15,
                    help="minutes RUNNING with no new layer or percent before a stalled row (default 15)")
    ap.add_argument("--snapshot-every", type=float, default=10,
                    help="minutes between chamber pictures, 0 for none (default 10)")
    ap.add_argument("--gif", action="store_true",
                    help="only rebuild the plate's timelapse.gif from the frames already taken")
    ap.add_argument("--sent", nargs=3, action="append", metavar=("HEX", "TRAY", "GRAMS"),
                    help="only write the send's row: a tray it fed, its color and the slice's grams "
                         "(repeat for each tray), then exit")
    ap.add_argument("--next", action="store_true",
                    help="for the background watcher: wait until the run log has a row, a picture, "
                         "a timeout or the end past --after, print them and the new cursor, exit")
    ap.add_argument("--after", type=int, default=0,
                    help="with --next: the cursor the last --next printed (lines already seen)")
    ap.add_argument("--wait", type=float, default=9,
                    help="with --next: minutes to wait before printing ev=quiet (default 9, inside "
                         "one 10-minute Bash call)")
    ap.add_argument("--look", nargs=2, metavar=("FRAME", "NOTE"),
                    help="for the background watcher: add what one picture showed to "
                         ".bambu/monitor/<plate>/looks.md, then exit")
    ap.add_argument("--publish", action="store_true",
                    help="put the timelapse and the finished plate on the page, as small WebPs in "
                         "<plate>-media/, refusing any picture where a QR code reads")
    ap.add_argument("--leave-out", action="append", metavar="FRAME",
                    help="with --publish: a picture to keep off the page, such as one showing a "
                         "person (the frame's file name; repeat for each)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.plate:
        ap.error("name a plate")
    if a.next:
        return wait_next(page_of(a.plate).stem, a.after, a.wait * 60)
    if a.look:
        print(add_look(page_of(a.plate).stem, *a.look))
        return 0
    if a.publish:
        return publish(a.plate, Log(LOGS / f"{page_of(a.plate).stem}.log"), a.leave_out or [])
    if a.sent:
        when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
        try:
            line = sent_line(when, [(h, t, float(g)) for h, t, g in a.sent])
        except ValueError as e:
            ap.error(str(e))
        page = page_of(a.plate)
        if not page.is_file():
            ap.error(f"no plate page at {page}")
        append_to_log(page, line)
        print(f"ev=row {line}")
        return 0
    if a.gif:
        name = page_of(a.plate).stem
        return 0 if make_gif(name, Log(LOGS / f"{name}.log")) else 1
    return watch(a.plate, a.every, a.lost_after * 60, a.stall_after * 60, a.snapshot_every * 60)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
