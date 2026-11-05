#!/usr/bin/env python3
"""PreToolUse hook: when a session searches for a term the FAQ already answers,
put that answer in front of it before the search runs.

Why: the FAQ audit marked every written answer "not taking" (2026-11-05). The
answers existed, but sessions searched before they read them. A pointer in
CLAUDE.md is read once at the start and forgotten; this lands at the moment the
search happens (D-129, docs/design/process/code-graph.md section 1).

Which terms: each answered entry's evidence line in docs/faq-evidence.jsonl has
a cluster such as "cmd:grep BIKAR_DIR". The term after "cmd:grep " is the
trigger, so a new FAQ entry is picked up with no list to keep here.

When it fires: a Grep tool call whose pattern contains the term, or a Bash
command that runs a search tool (grep, rg, git grep, ag, ack) and contains the
term. Matched on word edges, so "BIKAR_DIR_X" does not fire for BIKAR_DIR.

Once per session per entry, through a marker file in $TMPDIR. It never blocks:
the search still runs, and the answer arrives as added context. Each time it
fires it writes one line to ~/.claude/state/faq-at-grep.log, so the audit can
tell a search the hook answered from one it did not.

    faq_at_grep.py              # hook mode, reads the event JSON on stdin
    faq_at_grep.py --self-test  # checks matching and extraction on fixtures
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

SEARCH_TOOL = re.compile(r"(^|[\s|;&(])(grep|rg|ag|ack|egrep|fgrep)(\s|$)|git\s+grep")
LOG = Path.home() / ".claude" / "state" / "faq-at-grep.log"
MAX_ANSWER_CHARS = 1500


def repo_root() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[4]


def load_terms(evidence: Path) -> dict[str, str]:
    """term -> Q id, from the answered entries' clusters."""
    terms: dict[str, str] = {}
    if not evidence.exists():
        return terms
    for line in evidence.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        cluster = str(row.get("cluster", ""))
        qid = str(row.get("id", ""))
        if cluster.startswith("cmd:grep ") and qid.startswith("Q-"):
            term = cluster[len("cmd:grep "):].strip()
            if term:
                terms[term] = qid
    return terms


def load_answers(faq: Path) -> dict[str, tuple[str, str]]:
    """Q id -> (question, answer paragraph)."""
    answers: dict[str, tuple[str, str]] = {}
    if not faq.exists():
        return answers
    text = faq.read_text(encoding="utf-8")
    for m in re.finditer(r"^## (Q-\d{3}) — (.+?)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        qid, question, body = m.group(1), m.group(2).strip(), m.group(3)
        a = re.search(r"\*\*Answer\.\*\*\s*(.+?)(?:\n\s*\n|\Z)", body, re.S)
        if a:
            answers[qid] = (question, " ".join(a.group(1).split()))
    return answers


def search_text(event: dict) -> str | None:
    """The text a search call searches for, or None when it is not a search."""
    tool = event.get("tool_name")
    inp = event.get("tool_input") or {}
    if tool == "Grep":
        return str(inp.get("pattern", ""))
    if tool == "Bash":
        cmd = str(inp.get("command", ""))
        return cmd if SEARCH_TOOL.search(cmd) else None
    return None


def matches(text: str, terms: dict[str, str]) -> list[str]:
    hits = []
    for term, qid in terms.items():
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(term)}(?![A-Za-z0-9_])", text):
            hits.append(qid)
    return sorted(set(hits))


def first_time(session: str, qid: str) -> bool:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", session or "nosession")
    marker = Path(tempfile.gettempdir()) / f"faq-at-grep-{safe}-{qid}"
    if marker.exists():
        return False
    try:
        marker.touch()
    except OSError:
        pass
    return True


def log(session: str, qid: str, tool: str) -> None:
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        repo = repo_root().name
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(f"{stamp} pid={os.getpid()} ev=faq_shown repo={repo} q={qid} tool={tool} session={session}\n")
    except OSError:
        pass


def context_for(qids: list[str], answers: dict[str, tuple[str, str]]) -> str:
    parts = []
    for qid in qids:
        if qid not in answers:
            continue
        question, answer = answers[qid]
        if len(answer) > MAX_ANSWER_CHARS:
            answer = answer[:MAX_ANSWER_CHARS].rsplit(" ", 1)[0] + " …"
        parts.append(f"{qid} — {question}\n{answer}")
    if not parts:
        return ""
    head = "[faq] The FAQ (docs/faq.md) already answers what this search looks for. Read it before searching further:\n\n"
    return head + "\n\n".join(parts)


def run_hook() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    text = search_text(event)
    if not text:
        return 0
    root = repo_root()
    terms = load_terms(root / "docs" / "faq-evidence.jsonl")
    qids = matches(text, terms)
    session = str(event.get("session_id", ""))
    fresh = [q for q in qids if first_time(session, q)]
    if not fresh:
        return 0
    ctx = context_for(fresh, load_answers(root / "docs" / "faq.md"))
    if not ctx:
        return 0
    for q in fresh:
        log(session, q, str(event.get("tool_name")))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": ctx}}))
    return 0


def self_test() -> int:
    terms = {"BIKAR_DIR": "Q-002", "tagSegments": "Q-004"}
    cases = [
        ({"tool_name": "Grep", "tool_input": {"pattern": "BIKAR_DIR"}}, ["Q-002"]),
        ({"tool_name": "Bash", "tool_input": {"command": "git grep -n tagSegments packages"}}, ["Q-004"]),
        ({"tool_name": "Bash", "tool_input": {"command": "rg 'BIKAR_DIR ?='"}}, ["Q-002"]),
        ({"tool_name": "Bash", "tool_input": {"command": "echo $BIKAR_DIR"}}, None),
        ({"tool_name": "Grep", "tool_input": {"pattern": "BIKAR_DIR_EXTRA"}}, []),
        ({"tool_name": "Read", "tool_input": {"file_path": "BIKAR_DIR"}}, None),
    ]
    failed = 0
    for event, want in cases:
        text = search_text(event)
        got = None if text is None else matches(text, terms)
        if got != want:
            failed += 1
            print(f"FAIL {event} -> {got}, want {want}")
    root = repo_root()
    real_terms = load_terms(root / "docs" / "faq-evidence.jsonl")
    real_answers = load_answers(root / "docs" / "faq.md")
    missing = [q for q in real_terms.values() if q not in real_answers]
    if not real_terms:
        failed += 1
        print("FAIL no terms read from docs/faq-evidence.jsonl")
    if missing:
        failed += 1
        print(f"FAIL evidence ids with no answer in docs/faq.md: {missing}")
    print(f"faq_at_grep self-test: {len(cases)} cases, {len(real_terms)} FAQ terms, "
          f"{len(real_answers)} answers, {'OK' if not failed else f'{failed} failed'}")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(run_hook())
