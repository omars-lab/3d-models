#!/usr/bin/env python3
"""Watch one plate print on the X2D and write what the printer says onto the plate's page.

    python3 .claude/skills/send-plate/scripts/print_monitor.py <plate> [--every 30] [--lost-after 10]
    python3 .claude/skills/send-plate/scripts/print_monitor.py --self-test

`<plate>` is a plate name (`sheets-04b`) or the path of its page. Run it from the main checkout
(the vault), like every `bambu` call, so the rows land on the page Omar reads in Obsidian.

Every `--every` seconds it asks `tools/bambu/bin/bambu status show --json` for the printer's
report (each call under a timeout) and compares it with the last one. A change worth knowing
becomes one row in the page's `## Print log`, made after the Timeline when the page has none:

    | Time (UTC) | Event | Layer | Done | What the printer said |

The events are the plates gate's `PRINT_EVENTS` (P10), so the monitor and the gate share one
list: `watching` (the first look), `preparing`, `printing`, `paused` (with the error code and
what it means), `resumed`, `progress` (25, 50, 75%), `error` (a new error with no pause),
`finished`, `failed`, `stopped` (the printer went idle, or moved to another job) and `lost` (no
reply for `--lost-after` minutes). The last four end the watch; a pause does not, because a
paused print is waiting on Omar and may resume.

A `finished` row is not a print record. The record (`docs/prints/`, the Timeline's `printed`
row) is written when the pieces are judged, as before.

The run log is `.bambu/monitor/<plate>.log` (gitignored): one line per step, a UTC time, the
pid and `ev=<event> key=value`, with a line before and after each poll so a stall shows where
it froze (`grep "ev=poll" <log> | tail -1`). Each new row is also printed to stdout as
`ev=row …`, and the exit as `ev=exit …`, so a background run can be followed by grepping them.
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
TERMINAL = ("finished", "failed", "stopped", "lost")
MILESTONES = (25, 50, 75)

# What an error code means, in plain words. Only codes we have met and looked up: an unknown code
# is shown as its number, never guessed at. Source: Bambu's HMS list as mirrored in
# jmassardo/bambuddy-mobile hmsErrorCatalog.ts and hiwebsun0914 hms_errors.py (2026-10-03).
KNOWN = {
    "0500-8051": "the plate on the bed is not the one the file was sliced for",
}

INTRO = ("What the printer said while this plate printed, one row per change, written by the "
         "send-plate skill's `print_monitor.py`. A `finished` row is not a print record; that is "
         "written when the pieces are judged.")


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


def step(st: dict, frame: dict | None, now: float, plate: str, lost_after_s: float
         ) -> tuple[dict, list[tuple[str, str]]]:
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
            rows.append(("failed", said(code, state)))
        elif state == "IDLE":
            rows.append(("stopped", "the printer went idle"))
    if code and code != st.get("code") and not any(e in ("paused", "failed", "watching") for e, _ in rows):
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


def add_log_row(body: str, line: str) -> str:
    """The body with `line` at the end of its Print log, made after the Timeline if missing."""
    m = re.search(r"^## Print log\b.*?$(.*?)(?=^## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    if not m:
        section = (f"## Print log\n\n{INTRO}\n\n{pg.PRINT_LOG_HEAD}\n|---|---|---|---|---|\n{line}\n")
        t = re.search(r"^## Timeline\b.*?$(.*?)(?=^## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
        if not t or t.end() == len(body):
            return body.rstrip("\n") + "\n\n" + section
        return body[:t.end()] + section + "\n" + body[t.end():]
    lines = m.group(1).split("\n")
    last = max((i for i, ln in enumerate(lines) if ln.strip().startswith("|")), default=0)
    lines.insert(last + 1, line)
    return body[:m.start(1)] + "\n".join(lines) + body[m.end(1):]


def page_of(plate: str) -> Path:
    p = Path(plate)
    return p.resolve() if p.suffix == ".md" else pg.PLATES / f"{plate}.md"


def append_to_page(page: Path, line: str) -> None:
    text = page.read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    head, body = text[:end + 4], text[end + 4:]
    page.write_text(head + add_log_row(body, line), encoding="utf-8")


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


def watch(plate: str, every: float, lost_after_s: float) -> int:
    page = page_of(plate)
    name = page.stem
    if not page.is_file():
        print(f"print-monitor: no plate page {page}", file=sys.stderr)
        return 2
    log = Log(LOGS / f"{name}.log")
    log("start", plate=name, every_s=int(every), lost_after_s=int(lost_after_s))
    st: dict = {}
    while True:
        frame = poll(log)
        st, rows = step(st, frame, time.time(), name, lost_after_s)
        when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
        for event, text in rows:
            append_to_page(page, row_line(when, event, frame if frame and is_ours(frame, name) else None, text))
            log("row", event=event, msg=cell(text))
            print(f"ev=row plate={name} event={event} msg=\"{cell(text)}\"", flush=True)
            if event in TERMINAL:
                log("exit", reason=event)
                print(f"ev=exit plate={name} reason={event}", flush=True)
                return 0 if event == "finished" else 1
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

    st, rows = step({}, _f("PAUSE", err=0x0300400C), 0, "sheets-04b", 600)
    check(rows == [("watching", "0300-400C (not looked up yet)")],
          "an unknown code is shown as its number, never guessed at", rows)

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

    every = {e for e, _ in [("watching", 0)]} | set(TERMINAL) | {
        "preparing", "printing", "paused", "resumed", "progress", "error"}
    check(every <= set(pg.PRINT_EVENTS), "every event the monitor writes is one the gate knows",
          sorted(every - set(pg.PRINT_EVENTS)))

    # The page: the log is made after the Timeline, rows append in order, and the gate reads it.
    body = ("\n# p\n\n## Approvals\n\n| a |\n\n## Timeline\n\n| Date | What happened | Where |\n"
            "|---|---|---|\n| 2026-10-03 | sent | x |\n\n## Notes\n\nkeep me\n")
    b = add_log_row(body, row_line("2026-10-03 21:02", "watching", _f("PREPARE"), "PREPARE"))
    b = add_log_row(b, row_line("2026-10-03 21:09", "paused", _f("PAUSE"), "0500-8051: a | b"))
    rows, problem = pg.print_log(b)
    check(problem is None and [e for _, e in rows] == ["watching", "paused"],
          "the page's print log reads back through the gate", f"{problem} {rows}")
    check(b.index("## Timeline") < b.index("## Print log") < b.index("## Notes")
          and "keep me" in b, "the log sits after the Timeline and the rest of the page stays")
    check("a / b" in b, "a | in the printer's words cannot break the table")

    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "x.md"
        p.write_text("---\nplate: x\n---\n" + body, encoding="utf-8")
        append_to_page(p, row_line("2026-10-03 21:02", "watching", None, "PREPARE"))
        check(p.read_text(encoding="utf-8").startswith("---\nplate: x\n---\n"),
              "the frontmatter is left as it was")

    print(f"self-test: {'PASS' if not fails else f'FAIL ({fails})'}")
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("plate", nargs="?")
    ap.add_argument("--every", type=float, default=30, help="seconds between polls (default 30)")
    ap.add_argument("--lost-after", type=float, default=10,
                    help="minutes with no reply (or no sign of the plate) before giving up (default 10)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.plate:
        ap.error("name a plate")
    return watch(a.plate, a.every, a.lost_after * 60)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
