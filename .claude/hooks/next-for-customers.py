#!/usr/bin/env python3
"""Stop hook: when a stretch of work ends, have Claude ask the advisor what the
next most important thing is for our customers and users.

Claude Code has no "session is ending" event the model can act on (SessionEnd
runs after the model is gone and drops its output), so this hangs off Stop,
which fires each time Claude finishes a turn. To make that mean "a stretch of
work just finished" rather than "any reply", it fires only when:

- this is not already a continuation from a Stop hook (``stop_hook_active``);
- no background agents or tasks are still running (``background_tasks``), since
  then the work is not done yet;
- at least MIN_TOOL_CALLS tool calls have run in this session's transcript since
  the last time it fired (so a short question-and-answer never triggers it).

When it fires it blocks the stop once, with a reason that tells Claude to call
the advisor, put the answer in its closing message, and not start the work.

Tune or turn off with ``.claude/hooks/next-for-customers.conf`` in the repo, or
once for the whole machine with ``~/.claude/hooks/next-for-customers.conf``:

    ENABLED=1
    MIN_TOOL_CALLS=40      # work since the last ask before it asks again

The tool-call count at the last firing is kept in a marker file in $TMPDIR keyed
by session id. Exits 0 always; a crash or a missing transcript stays silent. Run
``next-for-customers.py --self-test`` to check the rules against fixtures.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CONF_NAME = "next-for-customers.conf"
DEFAULT_MIN_TOOL_CALLS = 40

MESSAGE = (
    "[next-for-customers] A stretch of work just finished. Before you hand back, "
    "call the advisor and ask it: what is the next most important thing to do for "
    "our customers and users (the people who buy and use the coasters, the store, "
    "the gallery and the Lab)? If no advisor tool is attached, answer it yourself "
    "from the backlogs in docs/tasks/. End your closing message with a short "
    "\"Next for customers\" section: the one pick, why it matters to them, and "
    "whether it is already on a backlog. Name it; do not start it in this turn."
)


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


def count_tool_calls(transcript_path: str) -> int:
    """Tool calls the main thread made, counted from the session transcript."""
    total = 0
    try:
        handle = open(transcript_path, encoding="utf-8")
    except OSError:
        return 0
    with handle:
        for line in handle:
            if '"tool_use"' not in line:
                continue
            try:
                rec = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            message = rec.get("message")
            if not isinstance(message, dict):
                continue
            for block in message.get("content", []) or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    total += 1
    return total


def _marker(session_id: str) -> Path:
    base = Path(os.environ.get("TMPDIR") or "/tmp")
    return base / f"next-for-customers-{session_id or 'unknown'}"


def _last_count(marker: Path) -> int:
    try:
        return int(marker.read_text().strip() or "0")
    except (OSError, ValueError):
        return 0


def should_fire(payload: dict, calls: int, last: int, min_calls: int) -> bool:
    if payload.get("stop_hook_active"):
        return False
    if payload.get("background_tasks"):
        return False
    return calls - last >= min_calls


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
        min_calls = int(conf.get("MIN_TOOL_CALLS") or DEFAULT_MIN_TOOL_CALLS)
    except ValueError:
        min_calls = DEFAULT_MIN_TOOL_CALLS

    session_id = payload.get("session_id") or Path(transcript_path).stem
    marker = _marker(session_id)
    calls = count_tool_calls(transcript_path)
    if not should_fire(payload, calls, _last_count(marker), min_calls):
        return 0
    try:
        marker.write_text(str(calls))
    except OSError:
        return 0  # without the marker it would ask on every stop; stay quiet
    print(json.dumps({"decision": "block", "reason": MESSAGE}))
    return 0


def _self_test() -> int:
    """Check the firing rules and the tool-call count against fixtures."""
    import tempfile

    ok = True

    def check(label, got, want):
        nonlocal ok
        flag = "ok" if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"self-test {flag}: {label} → {got} (want {want})")

    lines = [
        {"message": {"content": [{"type": "text", "text": "hi"}]}},
        {"message": {"content": [{"type": "tool_use", "name": "Bash"},
                                 {"type": "tool_use", "name": "Read"}]}},
        {"message": {"content": [{"type": "tool_result", "content": "\"tool_use\" in text"}]}},
        {"message": {"content": [{"type": "tool_use", "name": "Edit"}]}},
    ]
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
        for rec in lines:
            fh.write(json.dumps(rec) + "\n")
        path = fh.name
    try:
        check("counts tool_use blocks, not the word in a result", count_tool_calls(path), 3)
    finally:
        os.unlink(path)
    check("missing transcript counts zero", count_tool_calls("/nonexistent.jsonl"), 0)

    idle = {"stop_hook_active": False, "background_tasks": []}
    check("enough work, nothing running: fires", should_fire(idle, 40, 0, 40), True)
    check("too little work: quiet", should_fire(idle, 39, 0, 40), False)
    check("counts only work since the last ask", should_fire(idle, 70, 40, 40), False)
    check("already continuing from a stop hook: quiet",
          should_fire({"stop_hook_active": True}, 100, 0, 40), False)
    check("agents still running: quiet",
          should_fire({"background_tasks": [{"id": "a1"}]}, 100, 0, 40), False)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
