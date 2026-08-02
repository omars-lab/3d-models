#!/usr/bin/env python3
"""Site-graph gate for 3d-models.

Checks `docs/site-graph.json` — the declared link graph of everything this
project publishes — against this repo and against the exposures the graph
declares for each host.

WHAT IT DOES NOT DO, and why. It never asks whether a URL resolves. This repo
measured that trade already: an 8.4% sample of 737 URLs produced ~11% false
alarms against a true dead-link rate under 1%, and `CLAUDE.md` records the
conclusion — "a gate that cries wolf gets switched off, which is worse than
having no gate."

It also would not have helped. On 2026-08-02 four crawler runs (linkinator
live, linkinator offline, linkchecker, a headless-Chrome render) were pointed at
`index.html:277`, which links the public gallery to a host behind Cloudflare
Access. All four reported it OK. They cannot do otherwise: Cloudflare answers an
unauthenticated request with a login page and HTTP 200, so a reachability check
sees success. linkchecker went further and rewrote the target to the
cloudflareaccess.com login URL, which is the address it would have recorded in
any graph it emitted.

So the checkable invariant is not "does this URL resolve." It is "does this edge
travel through a host whose declared exposure makes it a login wall" — a fact
about two checked-in declarations, offline, with no false-positive mode.

  G1 GATED    An edge leaving a page that is publicly reachable, through a host
              declared `exposure: "access"`, must carry a `gated.why`. The rule
              is not that such an edge is forbidden — a sign-in door is a real
              thing to want — it is that it must be deliberate. Same shape as
              `public-surface.json`: growing what the world can (or cannot)
              reach costs one edit to a file that says so.
  G2 HOST     Every `viaHost` names a host some surface declares. Catches a link
              to a hostname nothing serves.
  G3 ANCHOR   Every `at` anchor in THIS repo resolves to that file and line, and
              that line still contains the edge's `evidence` string. Anchors
              into bikar are counted and skipped, out loud.
  G4 VENDOR   `Makefile:LAB_PAGES` names exactly the nodes marked `vendored`,
              and `DEPLOY_PATHS` ships them. The Makefile's own comment accepts
              this seam in as many words; this pins the local half of it.
  G5 FRAGILE  The set of edges that die if a public host is put behind Access is
              recomputed and must equal the checked-in list. Counted, not
              estimated — none of them break a build or turn a test red.

Usage:
  site_graph.py                check docs/site-graph.json
  site_graph.py --self-test    mutate the real graph in memory, one defect at a
                               time, and verify each mutation is caught
  site_graph.py --mermaid      print the graph as a Mermaid flowchart
  site_graph.py --update-doc   splice that render into docs/site-graph.md

Exit: 0 clean, 1 findings, 2 usage/self-test failure.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "docs/site-graph.json"


def check(graph: dict, root: Path, quiet: bool = False) -> list[str]:
    """Return a list of findings, each prefixed with its rule id."""
    out: list[str] = []

    surfaces = {s["id"]: s for s in graph["surfaces"]}
    nodes = {n["id"]: n for n in graph["nodes"]}

    # host -> exposure, across every surface
    exposure: dict[str, str] = {}
    for s in graph["surfaces"]:
        for h in s["hosts"]:
            exposure[h["host"]] = h["exposure"]

    def publicly_reachable(node_id: str) -> bool:
        """True if some host serving this node's surface is declared public."""
        n = nodes.get(node_id)
        if not n:
            return False
        s = surfaces.get(n["surface"])
        return bool(s) and any(h["exposure"] == "public" for h in s["hosts"])

    # ---- G0: the graph refers only to things it declares ------------------
    for n in graph["nodes"]:
        if n["surface"] not in surfaces:
            out.append(f"G0: node {n['id']} names undeclared surface {n['surface']!r}")
    for e in graph["edges"]:
        for end in ("from", "to"):
            if e[end] not in nodes:
                out.append(f"G0: edge {e['from']} -> {e['to']} ({e['at']}) "
                           f"names undeclared node {e[end]!r}")

    # ---- G1 GATED ---------------------------------------------------------
    for e in graph["edges"]:
        via = e.get("viaHost")
        if not via or exposure.get(via) != "access":
            continue
        if not publicly_reachable(e["from"]):
            continue
        if not (e.get("gated") or {}).get("why"):
            out.append(
                f"G1: {e['from']} -> {e['to']} at {e['at']} travels through {via}, "
                f"declared exposure=\"access\". {e['from']} is publicly reachable, so "
                f"every visitor but the owner gets a login wall — and no link checker "
                f"will tell you, because Access answers with a login page and HTTP 200. "
                f"If the door is intended, say so with a \"gated\": {{\"why\": [...]}} on "
                f"this edge."
            )

    # ---- G2 HOST ----------------------------------------------------------
    for e in graph["edges"]:
        via = e.get("viaHost")
        if via and via not in exposure:
            out.append(
                f"G2: {e['from']} -> {e['to']} at {e['at']} travels through {via!r}, "
                f"which no surface in this file declares. Either it is a typo, or a "
                f"host we publish on is undeclared, or nothing serves it at all."
            )

    # ---- G3 ANCHOR --------------------------------------------------------
    foreign = 0
    for e in graph["edges"]:
        if e.get("repo"):
            foreign += 1
            continue
        m = re.fullmatch(r"(.+):(\d+)", e["at"])
        if not m:
            out.append(f"G3: {e['from']} -> {e['to']} has an unparseable anchor {e['at']!r} "
                       f"(want 'path/to/file:LINE')")
            continue
        path, lineno = root / m.group(1), int(m.group(2))
        if not path.is_file():
            out.append(f"G3: {e['at']} — no such file in this repo")
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if lineno > len(lines):
            out.append(f"G3: {e['at']} — file has only {len(lines)} lines")
            continue
        ev = e.get("evidence")
        if ev and ev not in lines[lineno - 1]:
            out.append(
                f"G3: {e['at']} no longer contains {ev!r} — the edge moved or changed. "
                f"Line reads: {lines[lineno - 1].strip()[:100]!r}"
            )

    # ---- G4 VENDOR --------------------------------------------------------
    mk = (root / "Makefile").read_text(encoding="utf-8")
    m = re.search(r"^LAB_PAGES\s*=\s*(.+)$", mk, re.M)
    if not m:
        out.append("G4: no LAB_PAGES assignment in Makefile")
    else:
        declared = {n["file"] for n in graph["nodes"] if n.get("vendored")}
        actual = set(m.group(1).split())
        for f in sorted(actual - declared):
            out.append(f"G4: Makefile:LAB_PAGES vendors {f} but docs/site-graph.json has no "
                       f"node for it — a page ships onto the public gallery and the graph "
                       f"does not know it exists.")
        for f in sorted(declared - actual):
            out.append(f"G4: docs/site-graph.json declares {f} as vendored but "
                       f"Makefile:LAB_PAGES does not copy it — the graph describes a page "
                       f"that never lands.")
        if not re.search(r"^DEPLOY_PATHS\s*=.*\$\(LAB_PAGES\)", mk, re.M):
            out.append("G4: DEPLOY_PATHS no longer ships $(LAB_PAGES); the vendored pages "
                       "are built and then not deployed.")

    # ---- G5 FRAGILE -------------------------------------------------------
    # A surface with both public and access hosts is one Cloudflare setting away
    # from having none public. Every edge riding one of its public hosts dies
    # that day, silently.
    at_risk = {
        h["host"]
        for s in graph["surfaces"]
        if any(x["exposure"] == "access" for x in s["hosts"])
        for h in s["hosts"]
        if h["exposure"] == "public" and not h["host"].startswith("*.")
    }
    computed = sorted(
        f"{e['from']} -> {e['to']} via {e['viaHost']}"
        for e in graph["edges"]
        if e.get("viaHost") in at_risk
    )
    listed = sorted(graph["fragileIfProtected"]["edges"])
    if computed != listed:
        out.append(
            "G5: fragileIfProtected is out of date.\n"
            + "".join(f"      + {x}\n" for x in computed if x not in listed)
            + "".join(f"      - {x}\n" for x in listed if x not in computed)
            + "      These edges break the day a public host goes behind Access. "
              "No build fails and no test turns red, which is why the list is counted."
        )

    if not quiet:
        print(f"  {len(graph['nodes'])} pages, {len(graph['edges'])} edges, "
              f"{foreign} anchor(s) in bikar not verifiable from here")
    return out


def cross_check_bikar(graph: dict) -> list[str]:
    """If a bikar clone is at hand, hold the mirrored exposures to it. Optional
    by design: bikar is private and absent from CI, and a gate that requires a
    repo it cannot have would just be switched off."""
    bikar = os.environ.get("BIKAR_DIR", str(Path.home() / "Workspace/git/bikar"))
    ps = Path(bikar) / "packages/web/public-surface.json"
    if not ps.is_file():
        print(f"  exposures: MIRRORED ONLY — no bikar clone at {ps} to check them against")
        return []
    truth = {h["host"]: h["exposure"] for h in json.loads(ps.read_text())["hosts"]}
    out = []
    for s in graph["surfaces"]:
        for h in s["hosts"]:
            if h["host"] in truth and truth[h["host"]] != h["exposure"]:
                out.append(
                    f"G6: {h['host']} is declared {h['exposure']!r} here but "
                    f"{truth[h['host']]!r} in {ps} — which is the authority. The mirror "
                    f"has drifted, and every G1 verdict above was computed from the "
                    f"stale copy."
                )
    print(f"  exposures: cross-checked against {ps}")
    return out


def mermaid(graph: dict) -> str:
    exposure = {h["host"]: h["exposure"]
                for s in graph["surfaces"] for h in s["hosts"]}
    lines = ["flowchart LR"]
    for s in graph["surfaces"]:
        lines.append(f'  subgraph {s["id"]}["{s["id"]} — {s["hosts"][0]["host"]}"]')
        for n in graph["nodes"]:
            if n["surface"] == s["id"]:
                lines.append(f'    {n["id"].replace(".", "_")}["{n["file"]}"]')
        lines.append("  end")

    # Several edges share a source and target (a static link and a JS-computed
    # one to the same page) and would draw twice. Dedupe the edge lines only —
    # deduping the whole script would eat the second `end` and leave a subgraph
    # unclosed, which Mermaid renders as one merged box.
    edges: list[str] = []
    for e in graph["edges"]:
        a, b = e["from"].replace(".", "_"), e["to"].replace(".", "_")
        via = e.get("viaHost")
        arrow = "-->" if e["visibility"] == "static" else "-.->"
        if via and exposure.get(via) == "access":
            edges.append(f'  {a} {arrow}|"sign-in wall"| {b}')
        elif via:
            edges.append(f'  {a} {arrow}|"{via}"| {b}')
        else:
            edges.append(f"  {a} {arrow} {b}")
    return "\n".join(lines + list(dict.fromkeys(edges)))


def self_test() -> int:
    """Break the real graph one way at a time and require the gate to notice.

    Deliberately not checked-in fixture files. A fixture is a copy, and a copy of
    a graph that changes every time a page is added goes stale and starts
    asserting against a shape the repo no longer has. Mutating the live graph
    cannot go stale, and it proves the gate fires on THIS graph rather than on a
    museum piece.
    """
    real = json.loads(GRAPH.read_text())

    baseline = check(copy.deepcopy(real), ROOT) + cross_check_bikar(real)
    if baseline:
        print("self-test FAIL: the real graph is not clean, so no mutation is meaningful:")
        for f in baseline:
            print(f"  {f}")
        return 2

    def mutate_ungate(g):
        for e in g["edges"]:
            if e.get("gated"):
                del e["gated"]
                return f"removed gated.why from {e['from']} -> {e['to']}"
        raise AssertionError("no gated edge to un-gate — G1 has nothing to prove")

    def mutate_bad_host(g):
        for e in g["edges"]:
            if e.get("viaHost"):
                # Not a made-up hostname: this is the one README.md:7 pointed at
                # until 2026-08-02, and it is NXDOMAIN.
                e["viaHost"] = "3d-models.bytesofpurpose.com"
                return f"repointed {e['from']} -> {e['to']} at 3d-models.bytesofpurpose.com (NXDOMAIN)"
        raise AssertionError("no cross-host edge")

    def mutate_anchor(g):
        for e in g["edges"]:
            if not e.get("repo") and e.get("evidence"):
                e["at"] = re.sub(r":(\d+)$", lambda m: f":{int(m.group(1)) + 3}", e["at"])
                return f"slid the anchor for {e['from']} -> {e['to']} by 3 lines"
        raise AssertionError("no in-repo anchor")

    def mutate_vendor(g):
        for n in g["nodes"]:
            if n.get("vendored"):
                n["vendored"] = False
                return f"stopped declaring {n['file']} as vendored"
        raise AssertionError("no vendored node")

    def mutate_fragile(g):
        g["fragileIfProtected"]["edges"] = []
        return "emptied fragileIfProtected"

    cases = [
        ("G1", mutate_ungate),
        ("G2", mutate_bad_host),
        ("G3", mutate_anchor),
        ("G4", mutate_vendor),
        ("G5", mutate_fragile),
    ]

    ok = True
    for code, mutate in cases:
        g = copy.deepcopy(real)
        what = mutate(g)
        found = [f for f in check(g, ROOT, quiet=True) if f.startswith(code + ":")]
        if found:
            print(f"self-test ok:   {code} — {what}")
            print(f"                caught: {found[0].splitlines()[0][:120]}")
        else:
            print(f"self-test FAIL: {code} — {what} — NOT CAUGHT")
            ok = False

    print("\nPASS: the real graph, unmutated, reports nothing (shown above).")
    print("FAIL: each mutation above is reported by the rule that owns it.")
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--mermaid", action="store_true")
    ap.add_argument("--update-doc", action="store_true")
    args = ap.parse_args()

    if not GRAPH.is_file():
        print(f"site-graph gate: no {GRAPH.relative_to(ROOT)} — nothing to check")
        return 0

    graph = json.loads(GRAPH.read_text())

    if args.mermaid:
        print(mermaid(graph))
        return 0
    if args.update_doc:
        doc = ROOT / "docs/site-graph.md"
        text = doc.read_text()
        new, n = re.subn(r"```mermaid\n.*?\n```",
                         "```mermaid\n" + mermaid(graph) + "\n```",
                         text, count=1, flags=re.S)
        if n != 1:
            print(f"✗ no ```mermaid block in {doc.relative_to(ROOT)}", file=sys.stderr)
            return 2
        if new == text:
            print(f"  {doc.relative_to(ROOT)} already matches the graph")
            return 0
        doc.write_text(new)
        print(f"  rewrote the mermaid block in {doc.relative_to(ROOT)}")
        return 0
    if args.self_test:
        return self_test()

    findings = check(graph, ROOT) + cross_check_bikar(graph)
    for f in findings:
        print(f"✗ {f}")
    if findings:
        print(f"\n{len(findings)} finding(s) — see docs/site-graph.json", file=sys.stderr)
        return 1
    print("✓ site graph agrees with the repo and with its declared exposures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
