#!/usr/bin/env python3
"""UserPromptSubmit hook: nudge toward the delegate-parallel-work skill when the
task list is holding several open, unblocked tasks that could be fanned out.

Signal: the harness TaskList, reconstructed from the session transcript (the
JSONL at ``transcript_path``, handed to the hook on stdin). A task is
*fan-out-ready* when its status is ``pending`` (not started, not in progress)
and none of its ``blockedBy`` ids is still open. When that count reaches
MIN_READY the hook prints a short nudge; Claude Code adds stdout to the
conversation as context. Work that is already delegated moves to ``in_progress``
and drops out of the count, so the nudge quiets itself once you act on it.

Opt in / tune with ``.claude/hooks/delegate-nudge.conf`` in the repo, or once for
the whole machine with ``~/.claude/hooks/delegate-nudge.conf``:

    ENABLED=1
    MIN_READY=3            # nudge when this many pending+unblocked tasks exist
    REMIND_EVERY_MIN=30    # repeat at most this often unless the count grows

Rate-limited through a marker file in $TMPDIR keyed by session id, so it does not
fire on every prompt. Exit 0 always — a nudge is advisory, never a block. Run
``delegate-nudge.py --self-test`` to check the counter against a fixture.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

CONF_NAME = "delegate-nudge.conf"
DEFAULT_MIN_READY = 3
DEFAULT_REMIND_EVERY_MIN = 30.0
OPEN = ("pending", "in_progress")


def _truthy(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def _load_conf() -> dict:
    """Repo conf wins over the machine conf; missing files mean defaults."""
    conf: dict = {}
    candidates = [
        Path.home() / ".claude" / "hooks" / CONF_NAME,
        Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".") / ".claude" / "hooks" / CONF_NAME,
    ]
    for path in candidates:
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.split("#", 1)[0].strip()
                if "=" in line:
                    key, val = line.split("=", 1)
                    conf[key.strip()] = val.strip()
        except OSError:
            continue
    return conf


def _read_stdin_json() -> dict:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except (json.JSONDecodeError, ValueError):
        return {}


def _iter_records(transcript_path: str):
    """Yield parsed JSONL records, skipping lines with no task signal cheaply."""
    try:
        handle = open(transcript_path, encoding="utf-8")
    except OSError:
        return
    with handle:
        for line in handle:
            if '"tasks"' not in line and '"task"' not in line and "Task" not in line:
                continue
            try:
                yield json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue


def _apply_record(state: dict, rec: dict) -> None:
    """Fold one transcript record into the reconstructed task state.

    A TaskList result (``toolUseResult.tasks``) is authoritative and replaces the
    whole snapshot; a single-task result adds a pending task; a TaskUpdate
    tool call refines status / blockers on top.
    """
    result = rec.get("toolUseResult")
    if isinstance(result, dict) and isinstance(result.get("tasks"), list):
        state.clear()
        for task in result["tasks"]:
            tid = str(task.get("id"))
            state[tid] = {
                "status": task.get("status", "pending"),
                "blockedBy": [str(b) for b in task.get("blockedBy", [])],
            }
        return
    if isinstance(result, dict) and isinstance(result.get("task"), dict):
        task = result["task"]
        tid = str(task.get("id"))
        if tid and tid != "None":
            entry = state.setdefault(tid, {"status": "pending", "blockedBy": []})
            if "status" in task:
                entry["status"] = task["status"]
            if "blockedBy" in task:
                entry["blockedBy"] = [str(b) for b in task["blockedBy"]]

    message = rec.get("message")
    if not isinstance(message, dict):
        return
    for block in message.get("content", []) or []:
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        if block.get("name") != "TaskUpdate":
            continue
        inp = block.get("input") or {}
        tid = str(inp.get("taskId"))
        if not tid or tid == "None":
            continue
        entry = state.setdefault(tid, {"status": "pending", "blockedBy": []})
        if inp.get("status"):
            entry["status"] = inp["status"]
        for dep in inp.get("addBlockedBy", []) or []:
            dep = str(dep)
            if dep not in entry["blockedBy"]:
                entry["blockedBy"].append(dep)


def count_ready(state: dict) -> int:
    """Pending tasks whose every blocker is gone or completed."""
    ready = 0
    for entry in state.values():
        if entry.get("status") != "pending":
            continue
        blockers = entry.get("blockedBy", [])
        if all(state.get(dep, {}).get("status", "completed") == "completed" for dep in blockers):
            ready += 1
    return ready


def ready_from_transcript(transcript_path: str) -> int:
    state: dict = {}
    for rec in _iter_records(transcript_path):
        _apply_record(state, rec)
    return count_ready(state)


def _marker(session_id: str) -> Path:
    base = Path(os.environ.get("TMPDIR") or "/tmp")
    return base / f"delegate-nudge-{session_id or 'unknown'}"


def _should_fire(marker: Path, count: int, remind_every_min: float, now: float) -> bool:
    try:
        last_count = int(marker.read_text().strip() or "0")
        age_min = (now - marker.stat().st_mtime) / 60.0
    except (OSError, ValueError):
        return True
    return count > last_count or age_min >= remind_every_min


def _record_fire(marker: Path, count: int) -> None:
    try:
        marker.write_text(str(count))
    except OSError:
        pass


def _message(count: int) -> str:
    return (
        f"[delegate-nudge] {count} task(s) are pending and unblocked — fan-out-ready. "
        "If their files are disjoint, consider the delegate-parallel-work skill "
        "(/delegate-parallel-work): one isolated worktree + Opus subagent per piece, "
        "then integrate serially by cherry-pick. One reviewable piece is fine too."
    )


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()

    payload = _read_stdin_json()
    conf = _load_conf()
    if not _truthy(conf.get("ENABLED", "1"), default=True):
        return 0
    transcript_path = payload.get("transcript_path") or ""
    if not transcript_path or not Path(transcript_path).exists():
        return 0

    try:
        min_ready = int(conf.get("MIN_READY") or DEFAULT_MIN_READY)
    except ValueError:
        min_ready = DEFAULT_MIN_READY
    try:
        remind_every = float(conf.get("REMIND_EVERY_MIN") or DEFAULT_REMIND_EVERY_MIN)
    except ValueError:
        remind_every = DEFAULT_REMIND_EVERY_MIN

    count = ready_from_transcript(transcript_path)
    if count < min_ready:
        return 0

    session_id = payload.get("session_id") or Path(transcript_path).stem
    marker = _marker(session_id)
    now = time.time()
    if not _should_fire(marker, count, remind_every, now):
        return 0
    _record_fire(marker, count)
    print(_message(count))
    return 0


def _self_test() -> int:
    """Reconstruct a fixture transcript and assert the ready-count."""
    import tempfile

    lines = [
        # TaskList snapshot: 4 tasks — 2 pending-unblocked, 1 blocked, 1 done.
        {"toolUseResult": {"tasks": [
            {"id": "1", "subject": "a", "status": "pending", "blockedBy": []},
            {"id": "2", "subject": "b", "status": "pending", "blockedBy": []},
            {"id": "3", "subject": "c", "status": "pending", "blockedBy": ["4"]},
            {"id": "4", "subject": "d", "status": "in_progress", "blockedBy": []},
        ]}},
        # task 4 completes → task 3 becomes unblocked (ready rises 2 → 3).
        {"message": {"content": [{"type": "tool_use", "name": "TaskUpdate",
                                  "input": {"taskId": "4", "status": "completed"}}]}},
        # start task 1 → drops out of the pending count (ready falls 3 → 2).
        {"message": {"content": [{"type": "tool_use", "name": "TaskUpdate",
                                  "input": {"taskId": "1", "status": "in_progress"}}]}},
    ]
    ok = True

    def check(label, got, want):
        nonlocal ok
        flag = "ok" if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"self-test {flag}: {label} → {got} (want {want})")

    # Fold the whole fixture: 2 (base pending-unblocked) + 3 unblocked − 1 started = 2.
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
        for rec in lines:
            fh.write(json.dumps(rec) + "\n")
        path = fh.name
    try:
        check("full fold ready-count", ready_from_transcript(path), 2)
    finally:
        os.unlink(path)

    # Just the base snapshot: 2 pending-unblocked (3 is blocked by open 4).
    base = {"1": {"status": "pending", "blockedBy": []},
            "2": {"status": "pending", "blockedBy": []},
            "3": {"status": "pending", "blockedBy": ["4"]},
            "4": {"status": "in_progress", "blockedBy": []}}
    check("blocked task excluded", count_ready(base), 2)

    # An empty list nudges nothing.
    check("empty state", count_ready({}), 0)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
