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
              that re-derived the fact before the answer date vs after it.
              `show --audit` exits 1 on any "answer not taking" (§8 FAIL).

Authored vs read-back: a probe hit counts as AUTHORED only when it is in
content the assistant generated — a tool_use input, a thinking block, a text
block. A hit in a tool_result or attachment is a read-back, and the census
showed read-backs inflate raw occurrence 3-10x. Recurrence is always measured
in distinct sessions, the census's robust unit.

Used vs re-derived: authoring a fact only shows a session USED it, and the
first real run found that nearly every use was a session that already knew it
(docs/issues/faq-counted-use-not-rederivation.md). A session RE-DERIVES a fact
when, at that file's first authored use, a failed tool result in the WINDOW
lines before it names the fact, or it grepped for the fact's own term. For a
search-command cluster, a grep/rg for one specific name is the re-derivation.
Candidates, `show` and the verdicts count re-derivation only.

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
from collections import defaultdict, deque
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
# a code identifier at ~7/10 — so only a grep/rg for a specific name
# (`specific_name`) counts as a lookup. `find`'s first argument is a
# directory, not what is being looked for, so it is left out.
SEARCH_VERBS = ("grep", "rg")

SAMPLES = 12

# A failure counts as leading to a fact when it sits at most this many
# transcript lines before the line that uses the fact.
WINDOW = 12


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


def error_text(entry) -> str:
    """The text of every failed tool_result on this line, or ''."""
    if entry.get("type") != "user":
        return ""
    out = []
    for b in blocks(entry):
        if b.get("type") == "tool_result" and b.get("is_error"):
            c = b.get("content")
            if isinstance(c, list):
                c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
            out.append(str(c or ""))
    return "\n".join(out)


def verb_and_arg(cmd: str) -> tuple[str, str] | None:
    """The first real token of a command's last `&&` step and its first
    flag-less argument: `grep -rn "orbs:" Makefile` -> ("grep", "orbs:")."""
    if not cmd:
        return None
    tok = cmd.split("&&")[-1].strip().split()
    while tok and ("=" in tok[0] or tok[0] in ("export", "sudo")):
        tok = tok[1:]
    if not tok:
        return None
    arg = next((t.strip("'\"") for t in tok[1:] if not t.startswith("-")), "")
    return tok[0].split("/")[-1], arg


def cmd_shape(cmd: str) -> str | None:
    """Normalize a Bash command to a repeatable SHAPE.

    First real token + the first flag-less argument, digits folded, so
    `grep -rn "orbs:" Makefile` and `grep -rn "foo" x` share a family only when
    they share the search vocabulary, not just the verb.
    """
    va = verb_and_arg(cmd)
    if not va or va[0] not in SHAPE_CMDS:
        return None
    return f"{va[0]} {re.sub(r'[0-9]+', 'N', va[1])}"[:60]


def search_term(cmd: str) -> str | None:
    """What a grep/rg command searches for, or None when it is not a search."""
    va = verb_and_arg(cmd)
    return va[1] if va and va[0] in SEARCH_VERBS else None


def specific_name(term: str) -> bool:
    """A search term that names one thing in the code: `BIKAR_DIR`,
    `SCHEMA_VERSION`, `parseSeam`. Keywords (`def`, `export`), headings (`^##`)
    and short all-caps words are routine outline scans, not a fact being
    looked up — the first real run proposed 69 of those and almost nothing else."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", term):
        return False
    return "_" in term or bool(re.search(r"[a-z][A-Z]", term)) or \
        (term.isupper() and len(term) >= 4)


# --------------------------------------------------------------------- census


def new_cluster():
    return {"sessions": set(), "authored": defaultdict(int), "occ": 0,
            "authored_occ": 0, "first": None, "last": None, "samples": [],
            "contexts": [], "rederived": defaultdict(int), "how": defaultdict(int)}


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
        recent = deque()                       # (line, kind, text): recent failures, reads, commands
        mentioned = set()                      # facts this file has already authored
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
                while recent and i - recent[0][0] > WINDOW:
                    recent.popleft()
                now = []                       # this line's own reads and commands
                for b in blocks(e) if etype == "assistant" else ():
                    if b.get("type") == "tool_use":
                        inp = b.get("input", {}) or {}
                        if b.get("name") in READ_TOOLS and inp.get("file_path"):
                            now.append((i, "read", inp["file_path"]))
                        elif b.get("name") == "Bash" and inp.get("command"):
                            now.append((i, "bash", inp["command"]))

                for name, pat in FACT_PROBES.items():
                    if pat.search(raw):
                        c = clusters[f"fact:{name}"]
                        authored = bool(pat.search(mine))
                        hit(c, sid, i, ts, authored)
                        if authored and name not in mentioned:
                            mentioned.add(name)
                            ev = list(recent) + now
                            c["contexts"].append([sid, i, [(k, t[:160]) for _, k, t in ev]])
                            how = learned(pat, ev)
                            c["how"][how] += 1
                            if how != "knew":
                                c["rederived"][sid] += 1

                err = error_text(e)
                if err:
                    recent.append((i, "fail", err))
                recent.extend(now)

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
                            cmd = (inp.get("command") or "").strip()
                            shape = cmd_shape(cmd)
                            if shape:
                                c = clusters[f"cmd:{shape}"]
                                hit(c, sid, i, ts, True)
                                if specific_name(search_term(cmd) or ""):
                                    c["rederived"][sid] += 1   # the search is the lookup
                                    c["how"]["search"] += 1
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


def learned(pat: re.Pattern, ev: list[tuple]) -> str:
    """How a session came to a fact at its first use: 'failure' when a failed
    tool result just before it names the fact (the use-cases hook's block
    message names USE_CASES_OK), 'search' when it grepped for the fact's own
    term, 'knew' otherwise. Only the first two are re-derivation: a fact used
    correctly with no failure and no search is an answer that is working."""
    if any(k == "fail" and pat.search(t) for _, k, t in ev):
        return "failure"
    if any(k == "bash" and pat.search(search_term(t) or "") for _, k, t in ev):
        return "search"
    return "knew"


def candidate(key: str) -> bool:
    return key.startswith("fact:") or key.startswith("cmd:")


def metrics_line(c: dict) -> str:
    how = c["how"]
    return (f"metrics: re-derived in {len(c['rederived'])} sessions "
            f"(after a failure {how['failure']}, by searching {how['search']}, "
            f"already knew it {how['knew']}) · used in {len(c['authored'])} · "
            f"occ {c['occ']} (authored {c['authored_occ']}) · "
            f"first {(c['first'] or '-')[:10]} · last {(c['last'] or '-')[:10]}")


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
    print("re-derived (failure/search/knew at first use per file) used-in occ first_utc last_utc fact")
    facts = [(k[5:], c) for k, c in C["clusters"].items() if k.startswith("fact:")]
    for name, c in sorted(facts, key=lambda x: (-len(x[1]["rederived"]), -len(x[1]["authored"]))):
        h = c["how"]
        print(f"{len(c['rederived']):3d} ({h['failure']}/{h['search']}/{h['knew']}) "
              f"{len(c['authored']):4d} {c['occ']:6d}  "
              f"{(c['first'] or '-')[:10]} {(c['last'] or '-')[:10]}  {name}")

    if jsonpath:
        out = {
            "stats": {k: (dict(v) if isinstance(v, defaultdict) else v) for k, v in s.items()},
            "loops": [{"session": sid, "agent": agent, "file": fp, "reads": n}
                      for n, sid, agent, fp in flagged],
            "clusters": {k: {"sessions": sorted(c["authored"]),
                             "rederived": sorted(c["rederived"]), "how": dict(c["how"]),
                             "occ": c["occ"],
                             "authored": c["authored_occ"], "first": c["first"],
                             "last": c["last"], "samples": c["samples"]}
                         for k, c in C["clusters"].items() if len(c["sessions"]) >= 2},
        }
        Path(jsonpath).write_text(json.dumps(out, indent=1))
        print(f"\n[json written: {jsonpath}]")


def emit_contexts(C: dict, want: str) -> None:
    """What came just before each file's first use of a fact: the failed tool
    results in the WINDOW lines before it. This is how a fact's failure
    signature is found from real transcripts rather than guessed."""
    for key, c in sorted(C["clusters"].items()):
        if not key.startswith("fact:") or (want != "all" and want not in key):
            continue
        ctx = c["contexts"]
        kinds = {k: sum(1 for _, _, ev in ctx if any(x == k for x, _ in ev))
                 for k in ("fail", "read", "bash")}
        print(f"## {key[5:]}: {len(ctx)} first use(s); within {WINDOW} lines before: "
              f"a failure {kinds['fail']}, a Read {kinds['read']}, a command {kinds['bash']}")
        for sid, line, ev in ctx:
            shown =[(k, t) for k, t in ev if k in ("fail", "read") or kinds_search(t)]
            if shown:
                print(f"  {sid} {line}")
                for k, t in shown:
                    print(f"    {k:4s} | " + " ".join(t.split())[:140])


def kinds_search(cmd: str) -> bool:
    """True when a command is a search (grep, rg) rather than an action."""
    return search_term(cmd) is not None


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
    """Share of sessions that re-derived the cluster, before vs on/after `answered`.
    Re-derived, not used: a fact every session is meant to type (the Node prefix)
    would otherwise read as an answer that never takes."""
    c = C["clusters"].get(key)
    rederived = set(c["rederived"]) if c else set()
    pre = [s for s, ts in C["start"].items() if ts[:10] < answered]
    post = [s for s, ts in C["start"].items() if ts[:10] >= answered]

    def rate(ss):
        hits = sum(1 for s in ss if s in rederived)
        return {"sessions": len(ss), "rederived": hits,
                "rate": round(hits / len(ss), 3) if ss else None}

    return {"pre": rate(pre), "post": rate(post)}


def verdict(rec: dict) -> str:
    pre, post = rec["pre"], rec["post"]
    if not post["sessions"]:
        return "pending (no sessions since the answer)"
    if not pre["rate"]:
        return "no baseline (nothing re-derived it before the answer)"
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
            lines.append(f"  {side:4s}: {x['rederived']}/{x['sessions']} sessions re-derived it "
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
    cands = sorted(((len(c["rederived"]), k, c) for k, c in C["clusters"].items()
                    if candidate(k) and k not in taken and len(c["rederived"]) >= min_sessions),
                   key=lambda x: (-x[0], x[1]))
    out.append(f"## Candidates ({len(cands)} re-derived in >= {min_sessions} sessions)")
    for n, (_, key, c) in enumerate(cands, 1):
        rec = {"id": f"cand-{n:03d}", "cluster": key,
               "sessions": sorted(c["rederived"]), "samples": c["samples"],
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
        res = {"type": "tool_result", "content": payload}
        if kind == "fail":
            res["is_error"] = True
        return {"type": "user", "timestamp": ts, "message": {"content": [res]}}
    return {"type": "assistant", "timestamp": ts, "message": {"content": content}}


def _write(path: Path, rows: list[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(_entry(*r)) + "\n" for r in rows))


BLOCKED = "pre-commit 20-use-cases: staged file is pinned; re-run with USE_CASES_OK=1"
COMMIT = "USE_CASES_OK=1 git commit -m wip"


def fixture_rederivation(d: Path) -> None:
    """PASS fixture: planted re-derivations must surface, plain use must not.

    USE_CASES_OK is re-derived three ways: s1 after the hook's block message
    names it, s2 by grepping for it, s3 after a failure inside a subagent (so
    the subtree walk is load-bearing). s5 types it with no failure and no
    search — it already knew — and a failure *after* its first use must not
    turn that into a re-derivation. Every session types the Node prefix and
    none re-derives it, so it must not be proposed. s4 only reads both facts
    back. `grep parseSeam` (a specific name) in 3 sessions is a candidate;
    `grep ^##` (an outline scan) in the same 3 is not. s1's subagent reads
    parser.ts 45 times and writes nothing (the loop); s2 reads model.ts 45
    times but edits it (normal work, must not flag).
    """
    node = "export PATH=$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"
    _write(d / "s1.jsonl", [("2026-09-01T10:00:00Z", "bash", f"{node}; git status"),
                            ("2026-09-01T10:00:30Z", "fail", BLOCKED),
                            ("2026-09-01T10:00:40Z", "bash", COMMIT),
                            ("2026-09-01T10:01:00Z", "bash", "grep -rn parseSeam src"),
                            ("2026-09-01T10:01:10Z", "bash", "grep -n '^##' docs/a.md")])
    _write(d / "s1/subagents/agent-a1.jsonl",
           [("2026-09-01T10:02:00Z", "read", "/r/src/parser.ts")] * 45)
    _write(d / "s2.jsonl", [("2026-09-02T10:00:00Z", "think", "need v22.22.3 here"),
                            ("2026-09-02T10:00:30Z", "bash", "grep -rn USE_CASES_OK .githooks"),
                            ("2026-09-02T10:01:00Z", "bash", "grep -rn parseSeam src"),
                            ("2026-09-02T10:01:10Z", "bash", "grep -n '^##' docs/b.md")]
           + [("2026-09-02T10:02:00Z", "read", "/r/src/model.ts")] * 45
           + [("2026-09-02T10:03:00Z", "edit", "/r/src/model.ts")])
    _write(d / "s3.jsonl", [("2026-09-03T10:00:00Z", "bash", "grep -rn parseSeam src"),
                            ("2026-09-03T10:00:10Z", "bash", "grep -n '^##' docs/c.md")])
    _write(d / "s3/subagents/agent-b1.jsonl", [("2026-09-03T10:01:00Z", "bash", node),
                                               ("2026-09-03T10:01:30Z", "fail", BLOCKED),
                                               ("2026-09-03T10:01:40Z", "bash", COMMIT)])
    _write(d / "s4.jsonl", [("2026-09-04T10:00:00Z", "result",
                             "PATH has v22.22.3 on it; USE_CASES_OK is set")])
    _write(d / "s5.jsonl", [("2026-09-05T10:00:00Z", "bash", f"{node}; {COMMIT}"),
                            ("2026-09-05T10:00:30Z", "fail", BLOCKED),
                            ("2026-09-05T10:00:40Z", "bash", COMMIT)])


def fixture_not_taking(d: Path) -> tuple[Path, Path]:
    """FAIL fixture: Q-001's answer shipped 2026-09-10 yet re-derivation continued.

    Before: 1 of 2 sessions grepped for `deployBranch` (0.5). After: 2 of 2
    (1.0) — `show` must flag it. Q-002 (`GITLEAKS_CONFIG`) fell from 2/2 to 0/2
    and must pass, and Q-003 has no answer, so both other verdicts are
    exercised too.
    """
    rows = {"p1": ("2026-09-01", "grep -rn deployBranch .", "grep -rn GITLEAKS_CONFIG ."),
            "p2": ("2026-09-02", "git status", "grep -rn GITLEAKS_CONFIG ."),
            "q1": ("2026-09-11", "grep -rn deployBranch .", "git status"),
            "q2": ("2026-09-12", "grep -rn deployBranch src", "git status")}
    for sid, (day, a, b) in rows.items():
        _write(d / f"{sid}.jsonl", [(f"{day}T10:00:00Z", "bash", a),
                                    (f"{day}T10:01:00Z", "bash", b)])
    faq, ev = d / "faq.md", d / "faq-evidence.jsonl"
    faq.write_text("# FAQ\n\n## Q-001 — Which branch is the deploy?\n\n**Answer.** gh-pages.\n\n"
                   "## Q-002 — Where is the gitleaks config?\n\n**Answer.** Here.\n\n"
                   "## Q-003 — Still open?\n\nNo answer yet.\n")
    ev.write_text(json.dumps({"id": "q-001", "cluster": "cmd:grep deployBranch",
                              "answered": "2026-09-10"}) + "\n"
                  + json.dumps({"id": "q-002", "cluster": "cmd:grep GITLEAKS_CONFIG",
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
        hook = C["clusters"]["fact:use-cases hook / USE_CASES_OK"]
        node = C["clusters"]["fact:v22.22.3 node PATH prefix"]
        check("PASS fixture: walks main + subagent files",
              (C["stats"]["main_sessions"], C["stats"]["subagent_files"]), (5, 2))
        check("re-derived after a failure, by a search, and inside a subagent",
              sorted(hook["rederived"]), ["s1", "s2", "s3"])
        check("how each file first came to it (a later failure does not count)",
              dict(hook["how"]), {"failure": 2, "search": 1, "knew": 1})
        check("read-back session is seen but not authored",
              "s4" in hook["sessions"] and "s4" not in hook["authored"], True)
        check("a fact every session types but none re-derives",
              (len(node["authored"]), len(node["rederived"])), (4, 0))
        check("planted search re-derivation surfaces",
              sorted(C["clusters"]["cmd:grep parseSeam"]["rederived"]), ["s1", "s2", "s3"])
        props = proposal(C, [], 3)
        check("update-faq proposes the re-derived clusters only",
              ("fact:use-cases hook" in props, "cmd:grep parseSeam" in props,
               "fact:v22.22.3" in props, "cmd:grep ^##" in props),
              (True, True, False, False))
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
        check("FAIL fixture: continued re-derivation is flagged, a falling one passes",
              verdicts, {"Q-001": "ANSWER NOT TAKING", "Q-002": "taking", "Q-003": "open"})
        _, failing = show(C, entries, None)
        check("show --audit would exit nonzero", failing, 1)
        cands, remeasured = proposal(C, entries, 1).split("## Answered")
        check("an answered cluster is re-measured, not re-proposed",
              ("cmd:grep deployBranch" in cands, "### Q-001" in remeasured,
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
    c.add_argument("--context", default=None, metavar="FACT",
                   help="print the failures just before each file's first use of the "
                        "facts whose name contains FACT ('all' for every fact)")

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
        C = census(inputs(a))
        if a.context:
            emit_contexts(C, a.context)
        else:
            emit_census(C, a.min_reads, a.json)
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
