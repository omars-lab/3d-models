#!/usr/bin/env python3
"""session_reflect — PROTOTYPE census miner for repeated re-derivations.

  *** PROTOTYPE — census only. Not the shipped skill/tool. ***

Design: docs/session-reflection-design.md. Census output feeds
docs/research/session-reflection-census.md. This is the `--census` first cut
referenced there; `update-faq` / `show` are specified in the design doc and NOT
implemented here.

What it does: streams every Claude Code transcript for a project (one JSON
object per line, files up to ~300 MB, so *never* read whole — line by line),
classifies assistant content blocks (thinking / text / tool_use) and measures
four candidate re-derivation signals:

  (a) same file Read > N times in one session, split by whether the session
      ever Wrote it (loop vs re-derivation) and by main-thread vs sidechain;
  (b) the same grep/find/ls/rg/cat command SHAPE repeated across sessions;
  (c) thinking/text blocks with a question shape ("where is", "which file",
      "how does", "need to check whether", "let me verify/check/find");
  (d) known recurring repo facts (literal probes) — sessions & occurrences,
      earliest/latest UTC, so a before/after-memory split can be read off.

Authorship vs read-back: a hit inside a tool_use INPUT is authorship; a hit in
a tool_result/attachment is a read-back. This mirrors bikar/scripts/transcript.py
and .claude/skills/transcript-archaeology/SKILL.md — the design doc says the
shared reader should live in one place; this prototype does not yet import it.

Pointers are emitted as `<session-uuid> <line>` with 0-based line index, the
same index bikar's transcript.py `show`/`entry` take, so a pointer is directly
openable. They are DATA (JSON/TSV), never backticked doc paths.

Usage:
  session_reflect.py --census [--project DIR] [--min-reads N] [--json OUT]
  # --project accepts a repo path OR a pre-slugged -Users-... dir name;
  # default: this repo. Repeat --also-project to fold in sibling dirs.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"

READ_TOOLS = {"Read"}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}

QUESTION_SHAPES = {
    "where is": re.compile(r"\bwhere (?:is|are|does|do|did)\b", re.I),
    "which file": re.compile(r"\bwhich file\b", re.I),
    "how does": re.compile(r"\bhow (?:does|do|is|are)\b", re.I),
    "need to check": re.compile(r"\bneed to (?:check|verify|find|confirm)\b", re.I),
    "let me check": re.compile(r"\blet me (?:check|verify|find|see|confirm|look)\b", re.I),
    "let me find": re.compile(r"\b(?:let me|i'll|i will) (?:find|locate|search|grep)\b", re.I),
    "what is the": re.compile(r"\bwhat(?:'s| is) the\b", re.I),
}

# (d) Known recurring repo facts — literal probes drawn from .claude/memory/MEMORY.md.
FACT_PROBES = {
    "THREED_MODELS_DIR on bikar commits": re.compile(r"THREED_MODELS_DIR"),
    "npm ci / install in fresh worktree": re.compile(r"npm (?:ci|install)"),
    "dotenvx version on PATH": re.compile(r"dotenvx"),
    "ci/e2e/gitleaks required on bikar main": re.compile(r"gitleaks"),
    "use-cases hook / USE_CASES_OK": re.compile(r"USE_CASES_OK|20-use-cases|use-cases hook"),
    "D-id collision (next decision id)": re.compile(r"\bD-0\d\d\b.*colli|decision.id.colli", re.I),
    "v22.22.3 node PATH prefix": re.compile(r"v22\.22\.3"),
    "gh-pages diverged branch": re.compile(r"gh-pages"),
    "make validate is the only CI": re.compile(r"make validate\b|local\.ci"),
    "worktree add sibling": re.compile(r"git worktree add"),
}


def project_dir(arg: str | None) -> Path:
    raw = arg or os.getcwd()
    if raw.startswith("-") and (PROJECTS / raw).is_dir():
        return PROJECTS / raw
    d = PROJECTS / str(Path(raw).resolve()).replace("/", "-")
    if not d.is_dir():
        sys.exit(f"no transcripts for {raw}\n  looked in: {d}")
    return d


def transcripts(d: Path) -> list[tuple[Path, str, str]]:
    """Every transcript for the project as (path, parent_session_uuid, agent).

    Two shapes, and missing the second is a real bug: the main session is
    `<slug>/<uuid>.jsonl` (agent = "main"), and each SUBAGENT is a separate file
    `<slug>/<uuid>/subagents/agent-<agentId>.jsonl` — NOT an inline
    `isSidechain:true` entry, which is the older format bikar's transcript.py and
    the task brief both assume. A top-level `*.jsonl` glob silently drops every
    subagent, and that is exactly where the read-loops live.
    """
    out = []
    for f in sorted(d.glob("*.jsonl")):
        if "orphaned" in f.name:
            continue
        out.append((f, f.stem, "main"))
    for f in sorted(d.glob("*/subagents/agent-*.jsonl")):
        parent = f.parent.parent.name
        agent = f.stem.replace("agent-", "")
        out.append((f, parent, agent))
    return out


def blocks(entry):
    content = (entry or {}).get("message", {}).get("content")
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict):
                yield b


def census(dirs: list[Path], min_reads: int):
    stats = {
        "main_sessions": 0, "subagent_files": 0, "lines": 0, "parse_errors": 0,
        "assistant_turns": 0,
        "tool_use": defaultdict(int),
        "entry_types": defaultdict(int),
    }
    # (a) reads[(session,agent,file)] = {n, line, first_ts, last_ts, kind}
    reads = defaultdict(lambda: {"n": 0, "line": None, "first_ts": None,
                                 "last_ts": None, "kind": "main"})
    wrote = set()  # (session, agent, file) — did THIS agent write it?
    # (b) cmd shape -> {sessions:set, n:int, sample:(session,line,cmd)}
    cmds = defaultdict(lambda: {"sessions": set(), "n": 0, "sample": None})
    # (c) question shape -> {sessions:set, n:int, samples:list}
    ques = {k: {"sessions": set(), "n": 0, "samples": []} for k in QUESTION_SHAPES}
    # (d) fact -> {sessions:set, n:int, first:ts, last:ts, samples:list, per_session_ts:dict}
    facts = {k: {"sessions": set(), "n": 0, "first": None, "last": None,
                 "samples": [], "authored": 0} for k in FACT_PROBES}

    for path, sid, agent in dirs:
        if agent == "main":
            stats["main_sessions"] += 1
        else:
            stats["subagent_files"] += 1
        with path.open(errors="replace") as fh:
            for i, raw in enumerate(fh):
                stats["lines"] += 1
                try:
                    e = json.loads(raw)
                except json.JSONDecodeError:
                    stats["parse_errors"] += 1
                    continue
                etype = e.get("type", "?")
                stats["entry_types"][etype] += 1
                ts = e.get("timestamp")
                if etype == "assistant":
                    stats["assistant_turns"] += 1

                # (d) literal probes over the raw line, but authorship only counts
                #     when the literal is in a tool_use input or thinking/text.
                authored_line = False
                for b in blocks(e):
                    if b.get("type") in ("tool_use", "thinking", "text"):
                        authored_line = True
                        break
                for name, pat in FACT_PROBES.items():
                    if pat.search(raw):
                        f = facts[name]
                        f["sessions"].add(sid)
                        f["n"] += 1
                        if authored_line:
                            f["authored"] += 1
                        if ts:
                            f["first"] = min(f["first"], ts) if f["first"] else ts
                            f["last"] = max(f["last"], ts) if f["last"] else ts
                        if len(f["samples"]) < 12:
                            f["samples"].append([sid, i, ts, authored_line])

                for b in blocks(e):
                    bt = b.get("type")
                    if bt == "tool_use":
                        name = b.get("name", "?")
                        stats["tool_use"][name] += 1
                        inp = b.get("input", {}) or {}
                        if name in READ_TOOLS:
                            fp = inp.get("file_path")
                            if fp:
                                r = reads[(sid, agent, fp)]
                                r["n"] += 1
                                r["kind"] = "main" if agent == "main" else "subagent"
                                if r["line"] is None:
                                    r["line"] = i
                                if ts:
                                    r["first_ts"] = r["first_ts"] or ts
                                    r["last_ts"] = ts
                        elif name in WRITE_TOOLS:
                            fp = inp.get("file_path")
                            if fp:
                                wrote.add((sid, agent, fp))
                        elif name == "Bash":
                            cmd = (inp.get("command") or "").strip()
                            shape = cmd_shape(cmd)
                            if shape:
                                c = cmds[shape]
                                c["sessions"].add(sid)
                                c["n"] += 1
                                if c["sample"] is None:
                                    c["sample"] = [sid, i, cmd[:120]]
                    elif bt in ("thinking", "text"):
                        txt = b.get("thinking") or b.get("text") or ""
                        for name, pat in QUESTION_SHAPES.items():
                            if pat.search(txt):
                                q = ques[name]
                                q["sessions"].add(sid)
                                q["n"] += 1
                                if len(q["samples"]) < 12:
                                    m = pat.search(txt)
                                    s = max(0, m.start() - 20)
                                    q["samples"].append(
                                        [sid, i, txt[s:m.end() + 60].replace("\n", " ")])

    return stats, reads, wrote, cmds, ques, facts


SHAPE_CMDS = ("grep", "rg", "find", "ls", "cat", "git", "sed", "head", "tail", "awk")


def cmd_shape(cmd: str) -> str | None:
    """Normalize a Bash command to a repeatable SHAPE.

    First real token + the first flag-less argument that looks like a path or a
    quoted pattern, so `grep -rn "orbs:" Makefile` and `grep -rn "foo" x` share
    a family only when they share the search vocabulary, not just the verb.
    """
    if not cmd:
        return None
    # ignore env-prefix
    parts = cmd.split("&&")[-1].strip()
    tok = parts.split()
    if not tok:
        return None
    # strip leading export PATH=...
    while tok and ("=" in tok[0] or tok[0] in ("export", "sudo")):
        tok = tok[1:]
    if not tok:
        return None
    verb = tok[0].split("/")[-1]
    if verb not in SHAPE_CMDS:
        return None
    # pull the first non-flag argument as the "target vocabulary"
    arg = ""
    for t in tok[1:]:
        if t.startswith("-"):
            continue
        arg = t.strip("'\"")
        break
    # normalize a path/pattern to its basename-ish tail
    arg = re.sub(r"[0-9]+", "N", arg)
    return f"{verb} {arg}"[:60]


def emit(stats, reads, wrote, cmds, ques, facts, min_reads: int, jsonpath: str | None):
    def p(*a):
        print(*a)

    p("# CENSUS")
    p(f"main_sessions={stats['main_sessions']} subagent_files={stats['subagent_files']} "
      f"lines={stats['lines']} parse_errors={stats['parse_errors']} "
      f"assistant_turns={stats['assistant_turns']}")
    p("entry_types:", dict(sorted(stats["entry_types"].items(), key=lambda x: -x[1])))
    p("tool_use:", dict(sorted(stats["tool_use"].items(), key=lambda x: -x[1])))

    p("\n## (a) same file Read >= %d times by one agent" % min_reads)
    rows = []
    for (sid, agent, fp), r in reads.items():
        if r["n"] >= min_reads:
            w = (sid, agent, fp) in wrote
            rows.append((r["n"], sid, agent, fp, w, r["kind"], r["line"],
                         (r["first_ts"] or "")[:19], (r["last_ts"] or "")[:19]))
    rows.sort(reverse=True)
    p("count session agent kind wrote? first_line span(first..last) file")
    for n, sid, agent, fp, w, kind, line, t0, t1 in rows[:45]:
        p(f"{n:4d} {sid[:8]} {agent[:12]:12s} {kind:8s} wrote={str(w):5s} "
          f"@line={line} {t0}..{t1[11:]} {fp}")
    loops = [r for r in rows if not r[4]]
    p(f"[{len(rows)} (session,agent,file) pairs at >= {min_reads} reads; "
      f"{len(loops)} never written by that agent (loop/re-derivation candidates); "
      f"{sum(1 for r in loops if r[5] == 'subagent')} of those in a subagent]")

    p("\n## (b) repeated command shapes across sessions")
    crows = sorted(((len(c["sessions"]), c["n"], shape, c["sample"])
                    for shape, c in cmds.items()), reverse=True)
    p("sessions occ shape | sample(session line cmd)")
    for nses, n, shape, samp in crows[:40]:
        p(f"{nses:3d} {n:5d}  {shape:32s} | {samp}")

    p("\n## (c) question-shaped thinking/text blocks")
    p("sessions occ shape")
    for name, q in sorted(ques.items(), key=lambda x: -x[1]["n"]):
        p(f"{len(q['sessions']):3d} {q['n']:6d}  {name}")

    p("\n## (d) known recurring repo facts (literal probes)")
    p("sessions occ authored first_utc last_utc fact")
    for name, f in sorted(facts.items(), key=lambda x: -x[1]["n"]):
        p(f"{len(f['sessions']):3d} {f['n']:6d} {f['authored']:6d}  "
          f"{(f['first'] or '-')[:10]} {(f['last'] or '-')[:10]}  {name}")

    if jsonpath:
        out = {
            "stats": {k: (dict(v) if isinstance(v, defaultdict) else v)
                      for k, v in stats.items()},
            "reads_ge_min": [
                {"session": sid, "agent": agent, "file": fp, "count": r["n"],
                 "wrote_by_agent": (sid, agent, fp) in wrote, "kind": r["kind"],
                 "first_line": r["line"], "first_ts": r["first_ts"], "last_ts": r["last_ts"]}
                for (sid, agent, fp), r in reads.items() if r["n"] >= min_reads],
            "cmd_shapes": [
                {"shape": shape, "sessions": len(c["sessions"]), "occ": c["n"],
                 "sample": c["sample"]}
                for shape, c in cmds.items() if len(c["sessions"]) >= 2],
            "question_shapes": {
                name: {"sessions": sorted(q["sessions"]), "occ": q["n"],
                       "samples": q["samples"]}
                for name, q in ques.items()},
            "facts": {
                name: {"sessions": sorted(f["sessions"]), "occ": f["n"],
                       "authored": f["authored"], "first": f["first"], "last": f["last"],
                       "samples": f["samples"]}
                for name, f in facts.items()},
        }
        Path(jsonpath).write_text(json.dumps(out, indent=1))
        p(f"\n[json written: {jsonpath}]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--census", action="store_true")
    ap.add_argument("--project", default=None)
    ap.add_argument("--also-project", action="append", default=[])
    ap.add_argument("--min-reads", type=int, default=15)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    if not a.census:
        ap.error("only --census is implemented in this prototype")
    dirs = transcripts(project_dir(a.project))
    for extra in a.also_project:
        dirs += transcripts(project_dir(extra))
    emit(*census(dirs, a.min_reads), min_reads=a.min_reads, jsonpath=a.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
