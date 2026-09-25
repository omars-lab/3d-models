#!/usr/bin/env python3
"""session_reflect — mine transcripts for re-derived facts; keep a measured FAQ.

Design: docs/session-reflection-design.md (§4 verbs, §6 formats, §7 loop
detector, §8 verification). Census findings behind every choice here:
docs/research/session-reflection-census.md.

Three verbs:

  census      stream every transcript (main sessions AND the subagents/
              subtree), print the four signals: (a) same-file re-reads, with
              the loop detector; (b) repeated command shapes; (c) question-
              shaped thinking/text; (d) known-fact probes. Read-only.
              `census --self-test` runs the two built-in fixtures (§8).
  update-faq  cluster census hits into candidate questions and write a
              PROPOSAL beside the FAQ. Never writes the FAQ and never writes
              an answer: the human merges, discards and writes the prose (§5).
  show        print FAQ entries with live recurrence: the share of sessions
              that authored the fact before the answer date vs after it.
              `show --audit` exits 1 on any "answer not taking" (§8 FAIL).

Authored vs read-back: a probe hit counts as AUTHORED only when it is in
content the assistant generated — a tool_use input, a thinking block, a text
block. A hit in a tool_result or attachment is a read-back, and the census
showed read-backs inflate raw occurrence 3-10x. Recurrence is always measured
in distinct sessions, the census's robust unit.

Transcript layout: the main session is `<slug>/<uuid>.jsonl`; each subagent is
a separate file `<slug>/<uuid>/subagents/agent-<id>.jsonl`, attributed to its
parent session. A top-level glob alone drops every subagent — which is where
the one measured read-loop lived.

Pointers are `<session-uuid> <line>` with a 0-based line index, the index
bikar's transcript.py `show`/`entry` take. Files reach ~300 MB, so every
transcript is streamed line by line, never read whole.

Usage:
  session_reflect.py census [--project P] [--also-project P] [--transcripts DIR]
                            [--min-reads N] [--json OUT] [--self-test]
  session_reflect.py update-faq [...census inputs] [--min-sessions N]
                            [--faq FILE] [--evidence FILE] [--out FILE]
  session_reflect.py show [Q-NNN] [...census inputs] [--faq FILE]
                            [--evidence FILE] [--audit]
  # --project takes a repo path or a pre-slugged -Users-... name (default:
  # this checkout). --transcripts takes a directory laid out like a project
  # dir, which is how the self-test feeds its fixtures.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"
REPO = Path(__file__).resolve().parent.parent
FAQ = REPO / "docs" / "faq.md"
EVIDENCE = REPO / "docs" / "faq-evidence.jsonl"
PROPOSAL = REPO / "docs" / "faq-proposal.md"

READ_TOOLS = {"Read"}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}

# §7: a (session, agent, file) triple read this many times with ZERO writes by
# that agent is flagged as a loop. Provisional placeholder pending the
# calibration bet CAL-LOOP-01, which is proposed and not yet minted: the census
# holds one positive (129 reads) and every no-write non-loop sits near 13, so
# 40 is ~3x clear of both and is NOT a grounded value.
LOOP_READS_PROVISIONAL = 40

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
# A new fact to track is a new line here; its cluster key is `fact:<name>`.
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

SHAPE_CMDS = ("grep", "rg", "find", "ls", "cat", "git", "sed", "head", "tail", "awk")
# Signal (b) precision: git plumbing re-reads at ~0/10, a search verb carrying
# a code identifier at ~7/10 — so only search verbs become FAQ candidates.
SEARCH_VERBS = ("grep", "rg", "find")

SAMPLES = 12


# ---------------------------------------------------------------- transcripts


def project_dir(arg: str | None) -> Path:
    raw = arg or os.getcwd()
    if raw.startswith("-") and (PROJECTS / raw).is_dir():
        return PROJECTS / raw
    d = PROJECTS / str(Path(raw).resolve()).replace("/", "-")
    if not d.is_dir():
        sys.exit(f"no transcripts for {raw}\n  looked in: {d}")
    return d


def transcripts(d: Path) -> list[tuple[Path, str, str]]:
    """Every transcript under a project dir as (path, parent_session_uuid, agent)."""
    out = []
    for f in sorted(d.glob("*.jsonl")):
        if "orphaned" in f.name:
            continue
        out.append((f, f.stem, "main"))
    for f in sorted(d.glob("*/subagents/agent-*.jsonl")):
        out.append((f, f.parent.parent.name, f.stem.replace("agent-", "")))
    return out


def inputs(a) -> list[tuple[Path, str, str]]:
    if a.transcripts:
        files = transcripts(Path(a.transcripts))
    else:
        files = transcripts(project_dir(a.project))
    for extra in a.also_project:
        files += transcripts(project_dir(extra))
    return files


def blocks(entry):
    content = (entry or {}).get("message", {}).get("content")
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict):
                yield b


def authored_text(entry) -> str:
    """The content the assistant generated on this line, or '' for anything else."""
    if entry.get("type") != "assistant":
        return ""
    parts = []
    for b in blocks(entry):
        bt = b.get("type")
        if bt == "tool_use":
            parts.append(json.dumps(b.get("input", {}), ensure_ascii=False))
        elif bt in ("thinking", "text"):
            parts.append(b.get("thinking") or b.get("text") or "")
    return "\n".join(parts)


def cmd_shape(cmd: str) -> str | None:
    """Normalize a Bash command to a repeatable SHAPE.

    First real token + the first flag-less argument, digits folded, so
    `grep -rn "orbs:" Makefile` and `grep -rn "foo" x` share a family only when
    they share the search vocabulary, not just the verb.
    """
    if not cmd:
        return None
    tok = cmd.split("&&")[-1].strip().split()
    while tok and ("=" in tok[0] or tok[0] in ("export", "sudo")):
        tok = tok[1:]
    if not tok:
        return None
    verb = tok[0].split("/")[-1]
    if verb not in SHAPE_CMDS:
        return None
    arg = next((t.strip("'\"") for t in tok[1:] if not t.startswith("-")), "")
    return f"{verb} {re.sub(r'[0-9]+', 'N', arg)}"[:60]


# --------------------------------------------------------------------- census


def new_cluster():
    return {"sessions": set(), "authored": defaultdict(int), "occ": 0,
            "authored_occ": 0, "first": None, "last": None, "samples": []}


def hit(c, sid, line, ts, authored):
    c["sessions"].add(sid)
    c["occ"] += 1
    if authored:
        c["authored"][sid] += 1
        c["authored_occ"] += 1
    if ts:
        c["first"] = min(c["first"], ts) if c["first"] else ts
        c["last"] = max(c["last"], ts) if c["last"] else ts
    if len(c["samples"]) < SAMPLES and authored:
        c["samples"].append([sid, line, ts])


def census(files: list[tuple[Path, str, str]]) -> dict:
    stats = {"main_sessions": 0, "subagent_files": 0, "lines": 0, "parse_errors": 0,
             "assistant_turns": 0, "tool_use": defaultdict(int),
             "entry_types": defaultdict(int)}
    reads = defaultdict(lambda: {"n": 0, "line": None, "first_ts": None, "last_ts": None})
    wrote = set()
    clusters = defaultdict(new_cluster)       # "fact:<name>" | "cmd:<shape>"
    ques = defaultdict(new_cluster)           # display only; never an FAQ candidate
    start = {}                                # session -> earliest timestamp

    for path, sid, agent in files:
        stats["main_sessions" if agent == "main" else "subagent_files"] += 1
        with path.open(errors="replace") as fh:
            for i, raw in enumerate(fh):
                stats["lines"] += 1
                try:
                    e = json.loads(raw)
                except json.JSONDecodeError:
                    stats["parse_errors"] += 1
                    continue
                if not isinstance(e, dict):
                    stats["parse_errors"] += 1
                    continue
                etype = e.get("type", "?")
                stats["entry_types"][etype] += 1
                ts = e.get("timestamp")
                if ts and (sid not in start or ts < start[sid]):
                    start[sid] = ts
                if etype == "assistant":
                    stats["assistant_turns"] += 1
                mine = authored_text(e)

                for name, pat in FACT_PROBES.items():
                    if pat.search(raw):
                        hit(clusters[f"fact:{name}"], sid, i, ts, bool(pat.search(mine)))

                if etype != "assistant":
                    continue
                for b in blocks(e):
                    bt = b.get("type")
                    if bt == "tool_use":
                        name = b.get("name", "?")
                        stats["tool_use"][name] += 1
                        inp = b.get("input", {}) or {}
                        fp = inp.get("file_path")
                        if name in READ_TOOLS and fp:
                            r = reads[(sid, agent, fp)]
                            r["n"] += 1
                            if r["line"] is None:
                                r["line"] = i
                            if ts:
                                r["first_ts"] = r["first_ts"] or ts
                                r["last_ts"] = ts
                        elif name in WRITE_TOOLS and fp:
                            wrote.add((sid, agent, fp))
                        elif name == "Bash":
                            shape = cmd_shape((inp.get("command") or "").strip())
                            if shape:
                                hit(clusters[f"cmd:{shape}"], sid, i, ts, True)
                    elif bt in ("thinking", "text"):
                        txt = b.get("thinking") or b.get("text") or ""
                        for name, pat in QUESTION_SHAPES.items():
                            if pat.search(txt):
                                hit(ques[name], sid, i, ts, True)

    return {"stats": stats, "reads": reads, "wrote": wrote, "clusters": clusters,
            "ques": ques, "start": start}


def loops(C: dict, threshold: int = LOOP_READS_PROVISIONAL) -> list[tuple]:
    """§7 loop detector: triples at >= threshold reads and no write by that agent."""
    return sorted(((r["n"], sid, agent, fp) for (sid, agent, fp), r in C["reads"].items()
                   if r["n"] >= threshold and (sid, agent, fp) not in C["wrote"]),
                  reverse=True)


def candidate(key: str) -> bool:
    if key.startswith("fact:"):
        return True
    verb = key[4:].split(" ", 1)[0]
    return verb in SEARCH_VERBS


def metrics_line(c: dict) -> str:
    return (f"metrics: sessions {len(c['authored'])} · occ {c['occ']} "
            f"(authored {c['authored_occ']}) · first {(c['first'] or '-')[:10]} "
            f"· last {(c['last'] or '-')[:10]}")


def emit_census(C: dict, min_reads: int, jsonpath: str | None) -> None:
    s = C["stats"]
    print("# CENSUS")
    print(f"main_sessions={s['main_sessions']} subagent_files={s['subagent_files']} "
          f"lines={s['lines']} parse_errors={s['parse_errors']} "
          f"assistant_turns={s['assistant_turns']}")
    print("tool_use:", dict(sorted(s["tool_use"].items(), key=lambda x: -x[1])))

    print(f"\n## (a) same file Read >= {min_reads} times by one agent")
    rows = sorted(((r["n"], sid, agent, fp, (sid, agent, fp) in C["wrote"], r["line"])
                   for (sid, agent, fp), r in C["reads"].items() if r["n"] >= min_reads),
                  reverse=True)
    for n, sid, agent, fp, w, line in rows[:45]:
        print(f"{n:4d} {sid} {agent[:12]:12s} wrote={str(w):5s} @line={line} {fp}")
    flagged = loops(C)
    print(f"[loop detector, provisional threshold {LOOP_READS_PROVISIONAL} no-write reads "
          f"pending CAL-LOOP-01: {len(flagged)} flagged]")
    for n, sid, agent, fp in flagged:
        print(f"  LOOP {n} reads, 0 writes  {sid} agent={agent}  {fp}")

    print("\n## (b) repeated command shapes across sessions")
    cmds = sorted(((len(c["sessions"]), c["occ"], k[4:], c["samples"][:1])
                   for k, c in C["clusters"].items() if k.startswith("cmd:")), reverse=True)
    for nses, n, shape, samp in cmds[:40]:
        print(f"{nses:3d} {n:5d}  {shape:32s} | {samp}")

    print("\n## (c) question-shaped thinking/text blocks")
    for name, q in sorted(C["ques"].items(), key=lambda x: -x[1]["occ"]):
        print(f"{len(q['sessions']):3d} {q['occ']:6d}  {name}")

    print("\n## (d) known recurring repo facts (literal probes)")
    print("authored-sessions occ authored first_utc last_utc fact")
    facts = [(k[5:], c) for k, c in C["clusters"].items() if k.startswith("fact:")]
    for name, c in sorted(facts, key=lambda x: -len(x[1]["authored"])):
        print(f"{len(c['authored']):3d} {c['occ']:6d} {c['authored_occ']:6d}  "
              f"{(c['first'] or '-')[:10]} {(c['last'] or '-')[:10]}  {name}")

    if jsonpath:
        out = {
            "stats": {k: (dict(v) if isinstance(v, defaultdict) else v) for k, v in s.items()},
            "loops": [{"session": sid, "agent": agent, "file": fp, "reads": n}
                      for n, sid, agent, fp in flagged],
            "clusters": {k: {"sessions": sorted(c["authored"]), "occ": c["occ"],
                             "authored": c["authored_occ"], "first": c["first"],
                             "last": c["last"], "samples": c["samples"]}
                         for k, c in C["clusters"].items() if len(c["sessions"]) >= 2},
        }
        Path(jsonpath).write_text(json.dumps(out, indent=1))
        print(f"\n[json written: {jsonpath}]")


# ------------------------------------------------------------------------ FAQ

ENTRY = re.compile(r"^## (Q-\d{3}) — (.+)$", re.M)


def read_faq(faq: Path, evidence: Path) -> list[dict]:
    """FAQ entries joined to their sidecar record. Missing files mean no entries."""
    if not faq.exists():
        return []
    side = {}
    if evidence.exists():
        for ln in evidence.read_text().splitlines():
            if ln.strip():
                rec = json.loads(ln)
                side[rec["id"].upper()] = rec
    text = faq.read_text()
    heads = list(ENTRY.finditer(text))
    out = []
    for n, m in enumerate(heads):
        body = text[m.end(): heads[n + 1].start() if n + 1 < len(heads) else len(text)]
        out.append({"id": m.group(1), "title": m.group(2).strip(),
                    "answered": "**Answer.**" in body, "record": side.get(m.group(1))})
    return out


def recurrence(C: dict, key: str, answered: str) -> dict:
    """Share of sessions that authored the cluster, before vs on/after `answered`."""
    c = C["clusters"].get(key)
    authored = set(c["authored"]) if c else set()
    pre = [s for s, ts in C["start"].items() if ts[:10] < answered]
    post = [s for s, ts in C["start"].items() if ts[:10] >= answered]

    def rate(ss):
        hits = sum(1 for s in ss if s in authored)
        return {"sessions": len(ss), "authored": hits,
                "rate": round(hits / len(ss), 3) if ss else None}

    return {"pre": rate(pre), "post": rate(post)}


def verdict(rec: dict) -> str:
    pre, post = rec["pre"], rec["post"]
    if not post["sessions"]:
        return "pending (no sessions since the answer)"
    if not pre["rate"]:
        return "no baseline (nothing authored before the answer)"
    if post["rate"] < pre["rate"]:
        return "taking"
    return "ANSWER NOT TAKING"


def show(C: dict, entries: list[dict], only: str | None) -> tuple[list[str], int]:
    lines, failing = [], 0
    for e in entries:
        if only and e["id"] != only.upper():
            continue
        lines.append(f"{e['id']} — {e['title']}")
        if not e["answered"]:
            lines.append("  open (no answer yet)")
            continue
        rec = e["record"]
        if not rec or "cluster" not in rec or "answered" not in rec:
            lines.append("  BROKEN: answered, but no evidence record with cluster + answered date")
            failing += 1
            continue
        r = recurrence(C, rec["cluster"], rec["answered"])
        v = verdict(r)
        lines.append(f"  cluster {rec['cluster']}  answered {rec['answered']}")
        for side in ("pre", "post"):
            x = r[side]
            lines.append(f"  {side:4s}: {x['authored']}/{x['sessions']} sessions authored "
                         f"({x['rate'] if x['rate'] is not None else '-'})")
        lines.append(f"  verdict: {v}" + (" — re-open the entry" if v.startswith("ANSWER") else ""))
        failing += v.startswith("ANSWER")
    return lines, failing


def proposal(C: dict, entries: list[dict], min_sessions: int) -> str:
    taken = {e["record"]["cluster"] for e in entries if e["record"] and "cluster" in e["record"]}
    out = ["# FAQ proposal — generated by tools/session_reflect.py update-faq",
           "",
           "Merge, split or discard each candidate. The tool never writes an answer:",
           "an accepted candidate becomes a `## Q-NNN` entry in the FAQ with prose you",
           "write and an anchored pointer to where the fact lives; its evidence line",
           "goes in the sidecar with `answered` set to the day the answer ships.",
           ""]
    cands = sorted(((len(c["authored"]), k, c) for k, c in C["clusters"].items()
                    if candidate(k) and k not in taken and len(c["authored"]) >= min_sessions),
                   key=lambda x: (-x[0], x[1]))
    out.append(f"## Candidates ({len(cands)} at >= {min_sessions} authoring sessions)")
    for n, (_, key, c) in enumerate(cands, 1):
        rec = {"id": f"cand-{n:03d}", "cluster": key,
               "sessions": sorted(c["authored"]), "samples": c["samples"],
               "occ": c["occ"], "authored": c["authored_occ"],
               "first": c["first"], "last": c["last"]}
        out += ["", f"### cand-{n:03d} — {key}", "", metrics_line(c), "",
                "evidence-line:", "```json", json.dumps(rec), "```"]
    answered = [e for e in entries if e["answered"] and e["record"] and "cluster" in e["record"]]
    out += ["", f"## Answered entries re-measured ({len(answered)})"]
    for e in answered:
        c = C["clusters"].get(e["record"]["cluster"], new_cluster())
        r = recurrence(C, e["record"]["cluster"], e["record"].get("answered", "9999"))
        out += ["", f"### {e['id']} — {e['title']}", "", metrics_line(c),
                f"verdict: {verdict(r)}"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ self-test


def _entry(ts, kind, payload):
    if kind == "bash":
        content = [{"type": "tool_use", "name": "Bash", "input": {"command": payload}}]
    elif kind == "think":
        content = [{"type": "thinking", "thinking": payload}]
    elif kind in ("read", "edit"):
        name = "Read" if kind == "read" else "Edit"
        content = [{"type": "tool_use", "name": name, "input": {"file_path": payload}}]
    else:  # a tool_result echoing text back: a read-back, never authored
        return {"type": "user", "timestamp": ts,
                "message": {"content": [{"type": "tool_result", "content": payload}]}}
    return {"type": "assistant", "timestamp": ts, "message": {"content": content}}


def _write(path: Path, rows: list[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(_entry(*r)) + "\n" for r in rows))


def fixture_rederivation(d: Path) -> None:
    """PASS fixture: a planted re-derivation census must surface, plus one loop.

    s1-s3 each author `v22.22.3` (s3 only inside a subagent, so the subtree walk
    is load-bearing); s4 only reads it back and must NOT count; s1's subagent
    reads parser.ts 45 times and writes nothing (the loop); s2 reads model.ts
    45 times but edits it (normal work, must not flag).
    """
    node = "export PATH=$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"
    _write(d / "s1.jsonl", [("2026-09-01T10:00:00Z", "bash", f"{node}; git status"),
                            ("2026-09-01T10:01:00Z", "bash", "grep -rn parseSeam src")])
    _write(d / "s1/subagents/agent-a1.jsonl",
           [("2026-09-01T10:02:00Z", "read", "/r/src/parser.ts")] * 45)
    _write(d / "s2.jsonl", [("2026-09-02T10:00:00Z", "think", "need v22.22.3 here"),
                            ("2026-09-02T10:01:00Z", "bash", "grep -rn parseSeam src")]
           + [("2026-09-02T10:02:00Z", "read", "/r/src/model.ts")] * 45
           + [("2026-09-02T10:03:00Z", "edit", "/r/src/model.ts")])
    _write(d / "s3.jsonl", [("2026-09-03T10:00:00Z", "bash", "grep -rn parseSeam src")])
    _write(d / "s3/subagents/agent-b1.jsonl", [("2026-09-03T10:01:00Z", "bash", node)])
    _write(d / "s4.jsonl", [("2026-09-04T10:00:00Z", "result", "PATH has v22.22.3 on it")])


def fixture_not_taking(d: Path) -> tuple[Path, Path]:
    """FAIL fixture: Q-001's answer shipped 2026-09-10 yet recurrence continued.

    Before: 1 of 2 sessions authored `gh-pages` (0.5). After: 2 of 2 (1.0) —
    `show` must flag it. Q-002 (`gitleaks`) fell from 2/2 to 0/2 and must pass,
    and Q-003 has no answer, so both other verdicts are exercised too.
    """
    rows = {"p1": ("2026-09-01", "git log gh-pages", "gitleaks git"),
            "p2": ("2026-09-02", "git status", "gitleaks detect"),
            "q1": ("2026-09-11", "git log gh-pages", "git status"),
            "q2": ("2026-09-12", "git diff gh-pages", "git status")}
    for sid, (day, a, b) in rows.items():
        _write(d / f"{sid}.jsonl", [(f"{day}T10:00:00Z", "bash", a),
                                    (f"{day}T10:01:00Z", "bash", b)])
    faq, ev = d / "faq.md", d / "faq-evidence.jsonl"
    faq.write_text("# FAQ\n\n## Q-001 — Which branch is the deploy?\n\n**Answer.** gh-pages.\n\n"
                   "## Q-002 — Is gitleaks wired?\n\n**Answer.** Yes.\n\n"
                   "## Q-003 — Still open?\n\nNo answer yet.\n")
    ev.write_text(json.dumps({"id": "q-001", "cluster": "fact:gh-pages diverged branch",
                              "answered": "2026-09-10"}) + "\n"
                  + json.dumps({"id": "q-002",
                                "cluster": "fact:ci/e2e/gitleaks required on bikar main",
                                "answered": "2026-09-10"}) + "\n")
    return faq, ev


def self_test() -> int:
    """Fixed fixtures and fixed expectations, so this cannot pass by reading nothing."""
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"self-test {'ok  ' if good else 'FAIL'}: {label} → {got!r}"
              + ("" if good else f" (wanted {want!r})"))

    with tempfile.TemporaryDirectory() as tmp:
        a = Path(tmp) / "rederivation"
        fixture_rederivation(a)
        C = census(transcripts(a))
        node = C["clusters"]["fact:v22.22.3 node PATH prefix"]
        check("PASS fixture: walks main + subagent files",
              (C["stats"]["main_sessions"], C["stats"]["subagent_files"]), (4, 2))
        check("planted fact surfaces in the authoring sessions only",
              sorted(node["authored"]), ["s1", "s2", "s3"])
        check("read-back session is seen but not authored",
              "s4" in node["sessions"] and "s4" not in node["authored"], True)
        check("planted search re-derivation surfaces",
              sorted(C["clusters"]["cmd:grep parseSeam"]["authored"]), ["s1", "s2", "s3"])
        props = proposal(C, [], 3)
        check("update-faq proposes both planted clusters",
              ("fact:v22.22.3 node PATH prefix" in props, "cmd:grep parseSeam" in props),
              (True, True))
        check("git plumbing is never a candidate", "cmd:git status" in props, False)
        check("loop detector flags the no-write subagent only",
              [(sid, agent, fp) for _, sid, agent, fp in loops(C)],
              [("s1", "a1", "/r/src/parser.ts")])

        b = Path(tmp) / "not-taking"
        faq, ev = fixture_not_taking(b)
        C = census(transcripts(b))
        entries = read_faq(faq, ev)
        verdicts = {e["id"]: (verdict(recurrence(C, e["record"]["cluster"],
                                                 e["record"]["answered"]))
                              if e["record"] else "open") for e in entries}
        check("FAIL fixture: continued recurrence is flagged, a falling one passes",
              verdicts, {"Q-001": "ANSWER NOT TAKING", "Q-002": "taking", "Q-003": "open"})
        _, failing = show(C, entries, None)
        check("show --audit would exit nonzero", failing, 1)
        cands, remeasured = proposal(C, entries, 1).split("## Answered")
        check("an answered cluster is re-measured, not re-proposed",
              ("fact:gh-pages" in cands, "### Q-001" in remeasured,
               "verdict: ANSWER NOT TAKING" in remeasured),
              (False, True, True))

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# ----------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)

    def inputs_args(p):
        p.add_argument("--project", default=None)
        p.add_argument("--also-project", action="append", default=[])
        p.add_argument("--transcripts", default=None)

    def faq_args(p):
        p.add_argument("--faq", default=str(FAQ))
        p.add_argument("--evidence", default=str(EVIDENCE))

    c = sub.add_parser("census")
    inputs_args(c)
    c.add_argument("--min-reads", type=int, default=15)
    c.add_argument("--json", default=None)
    c.add_argument("--self-test", action="store_true")

    u = sub.add_parser("update-faq")
    inputs_args(u)
    faq_args(u)
    u.add_argument("--min-sessions", type=int, default=3)
    u.add_argument("--out", default=str(PROPOSAL))

    s = sub.add_parser("show")
    s.add_argument("id", nargs="?")
    inputs_args(s)
    faq_args(s)
    s.add_argument("--audit", action="store_true")

    a = ap.parse_args()
    if a.verb == "census":
        if a.self_test:
            return self_test()
        emit_census(census(inputs(a)), a.min_reads, a.json)
        return 0

    entries = read_faq(Path(a.faq), Path(a.evidence))
    if a.verb == "show" and not any(e["answered"] for e in entries):
        print(f"{a.faq}: no answered entries — nothing to audit")
        for e in entries:
            print(f"{e['id']} — {e['title']}\n  open (no answer yet)")
        return 0
    C = census(inputs(a))
    if a.verb == "update-faq":
        Path(a.out).write_text(proposal(C, entries, a.min_sessions))
        print(f"proposal written: {a.out} — review it; the FAQ itself is unchanged")
        return 0
    lines, failing = show(C, entries, a.id)
    print("\n".join(lines) if lines else f"no entry {a.id}")
    return 1 if (a.audit and failing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
