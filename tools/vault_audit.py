#!/usr/bin/env python3
"""Measure how the docs/ Obsidian vault is set up, in one command.

Prints the numbers the vault-setup skill compares against its rubric
(.claude/skills/vault-setup/vault-rules.md):

  plugins      community plugins on, and the core ones the rubric relies on
  properties   per folder: how many notes carry frontmatter, and which keys;
               any frontmatter that is not valid YAML (Obsidian drops all of it)
  bases        the .base views, and which notes embed them
  links        markdown links vs wikilinks (code is not counted), and any
               wikilink that names no file — the same rule the docs gate runs
  orphans      notes no other note links to (markdown link, wikilink or a
               property such as `feeds:`)
  names        file names that are ids, not words — Obsidian shows the file
               name in the graph, tabs and search, not the title

Usage:
  tools/vault_audit.py                 report on docs/
  tools/vault_audit.py --json          the same numbers as JSON
  tools/vault_audit.py --setup-graph   also merge the graph color groups into
                                       .obsidian/graph.json (read-merge-write:
                                       every other setting is kept)

The wikilink rule is imported from the docs gate, not copied, so the audit and
the gate cannot disagree about what resolves.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "gates"))
from docs_gate import (  # noqa: E402
    LINK, SKIP_SCHEMES, WIKILINK, check_d8_frontmatter, frontmatter_end, strip_code,
    vault_files,
)

VAULT = ROOT / "docs"

# Core plugins the rubric relies on. Obsidian keeps core-plugins.json local (the
# vault's .gitignore does not commit it), so a fresh clone may not have the file.
CORE_WANTED = ("bases", "properties", "graph", "backlink", "outgoing-link")

# Graph colors by page kind. The first query that matches a note wins, so the
# specific groups come first. Obsidian stores a color as one packed integer,
# (r << 16) | (g << 8) | b; a "#rrggbb" string is silently ignored.
GRAPH_GROUPS = [
    ("path:research/", "#8e8e8e"),          # research: grey, the record behind a doc
    ("path:issues/", "#d9534f"),            # issues: red, pivots and dead ends
    ("path:wiki/", "#5cb85c"),              # wiki: green, the how-to notebook
    ("path:catalog/", "#f0ad4e"),           # catalog: amber, patterns to build
    ("path:constructions/", "#9b59b6"),     # constructions: purple
    ("path:tasks/", "#5bc0de"),             # tasks: light blue
    ("path:prints/", "#e67e22"),            # prints: orange
    ('file:"-design"', "#337ab7"),          # design docs: blue
]

# A name that is an id: a YouTube id (11 chars, mixed case or digits), a hash,
# a bare number. Words joined by hyphens are fine.
OPAQUE = re.compile(r"^(?=.*\d)(?=.*[A-Z])[A-Za-z0-9_-]{11}$|^[0-9a-f]{7,}$|^\d+$")

ARCHIVED_BODY = "research"  # the docs gate's exemption: verbatim bodies


def notes(vault: Path) -> list[Path]:
    """Markdown notes, not review-md comment sidecars or hidden folders."""
    out = []
    for p in sorted(vault.rglob("*.md")):
        rel = p.relative_to(vault)
        if any(part.startswith(".") for part in rel.parts):
            continue
        out.append(p)
    return out


def folder(vault: Path, p: Path) -> str:
    rel = p.relative_to(vault).parts
    return "(top level)" if len(rel) == 1 else rel[0]


def frontmatter_keys(lines: list[str]) -> list[str]:
    end = frontmatter_end(lines)
    if end < 0:
        return []
    return [m.group(1) for line in lines[1:end]
            if (m := re.match(r"^([A-Za-z_][\w -]*):", line))]


def resolve_wikilink(vault: Path, target: str) -> Path | None:
    """The file a wikilink opens, by the gate's rule; the shortest path wins a tie."""
    t = target.strip().lower()
    names = (t, t + ".md")
    hits = [f for f in vault_files(vault)
            if f in names or f.endswith(tuple("/" + n for n in names))]
    return vault / min(hits, key=len) if hits else None


def audit(vault: Path) -> dict:
    obs = vault / ".obsidian"

    def read_json(name: str):
        try:
            return json.loads((obs / name).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    core = read_json("core-plugins.json")
    graph = read_json("graph.json") or {}
    report: dict = {
        "vault": str(vault),
        "plugins": {
            "community": read_json("community-plugins.json") or [],
            "core": ({k: bool(core.get(k)) for k in CORE_WANTED}
                     if isinstance(core, dict) else "core-plugins.json not in this checkout"),
            "graph_color_groups": len(graph.get("colorGroups", [])),
        },
    }

    all_notes = notes(vault)
    by_folder: dict[str, dict] = defaultdict(lambda: {"notes": 0, "with_properties": 0, "keys": Counter()})
    inbound: Counter = Counter()
    md_links = wikilinks = embeds = 0
    broken: list[str] = []
    bad_yaml: list[str] = []
    bases_embedded: dict[str, list[str]] = defaultdict(list)

    for p in all_notes:
        rel = p.relative_to(vault).as_posix()
        raw = p.read_text(encoding="utf-8").splitlines()
        keys = frontmatter_keys(raw)
        f = by_folder[folder(vault, p)]
        f["notes"] += 1
        bad_yaml += check_d8_frontmatter(p, raw)
        if keys:
            f["with_properties"] += 1
            f["keys"].update(keys)

        lines = strip_code(raw)
        fm_end = frontmatter_end(raw)
        archived = ARCHIVED_BODY in p.relative_to(vault).parts
        for n, line in enumerate(lines):
            for target in LINK.findall(line):
                if target.startswith(SKIP_SCHEMES) or target.startswith("#"):
                    continue
                bare = unquote(target.split("#")[0])
                dest = (p.parent / bare).resolve()
                if dest.suffix == ".md" and dest.is_relative_to(vault.resolve()):
                    md_links += 1
                    if dest != p.resolve():
                        inbound[dest.relative_to(vault.resolve()).as_posix()] += 1
            for m in WIKILINK.finditer(line):
                target = m.group(1)
                if not target.strip():
                    continue
                wikilinks += 1
                embeds += m.group(0).startswith("!")
                dest = resolve_wikilink(vault, target)
                if dest is None:
                    if not (archived and n > fm_end):
                        broken.append(f"{rel}:{n + 1}: [[{target}]]")
                    continue
                d = dest.relative_to(vault).as_posix()
                if d.endswith(".base"):
                    bases_embedded[d].append(rel)
                elif d != rel:
                    inbound[d] += 1

    rels = [p.relative_to(vault).as_posix() for p in all_notes]
    orphans = [r for r in rels if not inbound[r] and r != "README.md"]
    base_files = sorted(p.relative_to(vault).as_posix() for p in vault.rglob("*.base"))
    report.update({
        "notes": len(all_notes),
        "comment_sidecars": sum(1 for p in vault.rglob(".*.comments.md")),
        "properties": {
            k: {"notes": v["notes"], "with_properties": v["with_properties"],
                "keys": dict(v["keys"].most_common())}
            for k, v in sorted(by_folder.items())
        },
        "invalid_frontmatter": bad_yaml,
        "bases": {b: bases_embedded.get(b, []) for b in base_files},
        "links": {"markdown": md_links, "wikilinks": wikilinks, "embeds": embeds,
                  "broken_wikilinks": broken},
        "orphans": orphans,
        "opaque_names": [r for r in rels if OPAQUE.match(Path(r).stem)],
    })
    return report


def print_report(r: dict) -> None:
    pl = r["plugins"]
    print(f"vault: {r['vault']}  ({r['notes']} notes, {r['comment_sidecars']} review-md comment files)")
    print("\nplugins")
    print(f"  community: {', '.join(pl['community']) or 'none'}")
    core = pl["core"]
    print("  core: " + (core if isinstance(core, str)
                         else ", ".join(f"{k} {'on' if v else 'OFF'}" for k, v in core.items())))
    print(f"  graph color groups: {pl['graph_color_groups']}")

    print("\nproperties (notes with frontmatter / notes, then keys by use)")
    for name, f in r["properties"].items():
        keys = ", ".join(f"{k} {c}" for k, c in list(f["keys"].items())[:8])
        print(f"  {name:<16} {f['with_properties']:>3} / {f['notes']:<3} {keys}")
    print(f"  invalid frontmatter (Obsidian shows no properties): {len(r['invalid_frontmatter'])}")
    for b in r["invalid_frontmatter"]:
        print(f"    {b.split(': D8')[0]}")

    print(f"\nbases: {len(r['bases'])}")
    for b, where in r["bases"].items():
        print(f"  {b}  embedded in: {', '.join(where) or 'nothing'}")

    lk = r["links"]
    print(f"\nlinks: {lk['markdown']} markdown, {lk['wikilinks']} wikilinks "
          f"({lk['embeds']} embeds), {len(lk['broken_wikilinks'])} broken wikilinks "
          f"(research bodies not counted)")
    for b in lk["broken_wikilinks"][:20]:
        print(f"  {b}")

    print(f"\norphans (no note links here): {len(r['orphans'])}")
    for o in r["orphans"]:
        print(f"  {o}")

    print(f"\nopaque file names: {len(r['opaque_names'])}")
    for o in r["opaque_names"][:10]:
        print(f"  {o}")


def hex_to_int(color: str) -> int:
    return int(color.lstrip("#"), 16)


def setup_graph(vault: Path) -> str:
    """Merge GRAPH_GROUPS into graph.json. Groups with the same query are
    replaced; any group someone added by hand, and every other setting, stays.
    A graph.json that exists but does not parse is left alone and reported."""
    path = vault / ".obsidian" / "graph.json"
    data: dict = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            return f"left alone: {path} is not valid JSON — fix it by hand first"
    ours = {q for q, _ in GRAPH_GROUPS}
    kept = [g for g in data.get("colorGroups", []) if g.get("query") not in ours]
    data["colorGroups"] = [{"query": q, "color": {"a": 1, "rgb": hex_to_int(c)}}
                           for q, c in GRAPH_GROUPS] + kept
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return (f"wrote {len(GRAPH_GROUPS)} color groups to {path} (kept {len(kept)} others). "
            "Obsidian reads it when the graph view opens; reload the vault if it is open.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", type=Path, default=VAULT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--setup-graph", action="store_true")
    args = ap.parse_args()
    vault = args.vault.resolve()
    if args.setup_graph:
        print(setup_graph(vault))
    r = audit(vault)
    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print_report(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
