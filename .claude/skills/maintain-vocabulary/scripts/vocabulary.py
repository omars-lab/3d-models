#!/usr/bin/env python3
"""The print vocabulary: one term a card, each with a picture, written from one YAML file.

Omar, 2026-11-05: "i also want a vocabulary in out hub with visual - skirt va brim vs pin va
dovetail wtc ... as we add more generic techiques we expand the vocabulary/tehcniqur oage". He had
asked whether a plate had "stars with skirts", and nothing here said what a skirt was.

The source is `docs/vocabulary/vocabulary.yaml`. `render` writes the vault page beside it,
`docs/vocabulary/README.md`; the hub's vocabulary page reads `json`. `check` fails when the page
is behind the YAML or the YAML names something that is not there. `scan` lists every param and
object setting the plates use that no term names, which is how a new technique gets noticed.

    vocabulary.py render
    vocabulary.py check
    vocabulary.py scan [--all]
    vocabulary.py json
    vocabulary.py pictures
    vocabulary.py --self-test
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SOURCE = VOCAB_DIR / "vocabulary.yaml"
PAGE = VOCAB_DIR / "README.md"
DOCS = ROOT / "docs"
PLATES = DOCS / "design" / "plates"
RENDER_CMD = "python3 .claude/skills/maintain-vocabulary/scripts/vocabulary.py render"
FIELDS = {"id", "group", "term", "also", "what", "ours", "picture", "alt", "from", "drawn",
          "pictures", "snippet", "lang", "knobs", "plates", "related", "cookbook"}
NEEDED = ("id", "group", "term", "what", "ours", "picture", "alt", "from")


def load(path=SOURCE):
    with open(path) as f:
        return yaml.safe_load(f)


def pictures_of(term):
    """Every picture a term shows, the first one first, as (path, alt, from, drawn)."""
    out = [(term.get("picture"), term.get("alt"), term.get("from"), bool(term.get("drawn")))]
    for p in term.get("pictures") or []:
        out.append((p.get("picture"), p.get("alt"), p.get("from"), bool(p.get("drawn"))))
    return out


# --- the vault page ----------------------------------------------------------------------------

def render(data):
    groups = {g["id"]: g["title"] for g in data["groups"]}
    terms = data["terms"]
    names = {t["id"]: t["term"] for t in terms}
    out = [
        "# Print vocabulary",
        "",
        "<!-- Written by vocabulary.py from vocabulary.yaml. Edit the YAML, then run:",
        f"     {RENDER_CMD} -->",
        "",
        "The words we use for printing coasters, each with a picture of the real thing and where it",
        "shows up on our coasters. Look-alikes sit next to each other: a skirt beside a brim, a pin",
        "beside a stud, a flange beside a lip. The same page is on the hub, under Vocabulary.",
        "",
        "A picture marked *drawing* is a diagram; every other one is a slice, a render or a photo of",
        "ours. To add a term, see the [maintain-vocabulary skill]"
        "(../../.claude/skills/maintain-vocabulary/SKILL.md).",
        "",
    ]
    for gid, title in groups.items():
        members = [t for t in terms if t["group"] == gid]
        if not members:
            continue
        out.append(f"- **{title}:** " + ", ".join(f"[{t['term']}](#{anchor(t['term'])})"
                                                  for t in members))
    out.append("")
    for gid, title in groups.items():
        members = [t for t in terms if t["group"] == gid]
        if not members:
            continue
        out += [f"## {title}", ""]
        for t in members:
            out += [f"### {t['term']}", ""]
            if t.get("also"):
                out += ["*Also: " + ", ".join(t["also"]) + ".*", ""]
            out += [t["what"].strip(), ""]
            for path, alt, src, drawn in pictures_of(t):
                out += [f"![{alt}]({path})", "",
                        f"*{alt} ({'drawing, ' if drawn else ''}{src}.)*", ""]
            out += ["**On our coasters.** " + t["ours"].strip(), ""]
            if t.get("snippet"):
                out += [f"```{t.get('lang', '')}", t["snippet"].rstrip(), "```", ""]
            links = []
            if t.get("plates"):
                links.append("Plates: " + ", ".join(
                    f"[{p}](../design/plates/{p}.md)" for p in t["plates"]))
            if t.get("cookbook"):
                links.append(f"[Cookbook recipe]({t['cookbook']})")
            if t.get("related"):
                links.append("See also: " + ", ".join(
                    f"[{names[r]}](#{anchor(names[r])})" for r in t["related"] if r in names))
            if links:
                out += [" · ".join(links), ""]
    return "\n".join(out).rstrip() + "\n"


def anchor(heading):
    """The heading's link anchor, the way GitHub and the docs gate spell it."""
    keep = []
    for ch in heading.lower():
        if ch.isalnum() or ch in "-_ ":
            keep.append(ch)
    return "".join(keep).replace(" ", "-")


# --- the checks --------------------------------------------------------------------------------

def problems(data, vocab_dir=VOCAB_DIR, plates_dir=PLATES, docs=DOCS):
    """What is wrong with the YAML, as plain sentences, each naming the term."""
    out = []
    groups = {g["id"] for g in data.get("groups", [])}
    ids = [t.get("id") for t in data.get("terms", [])]
    seen = set()
    for t in data.get("terms", []):
        tid = t.get("id", "?")
        if tid in seen:
            out.append(f"{tid}: the id is used twice")
        seen.add(tid)
        for k in NEEDED:
            if not t.get(k):
                out.append(f"{tid}: has no `{k}`")
        for k in set(t) - FIELDS:
            out.append(f"{tid}: `{k}` is not a field this page knows")
        if t.get("group") and t["group"] not in groups:
            out.append(f"{tid}: group `{t['group']}` is not in `groups`")
        if t.get("snippet") and not t.get("lang"):
            out.append(f"{tid}: has a snippet but no `lang`")
        for r in t.get("related") or []:
            if r not in ids:
                out.append(f"{tid}: related `{r}` is not a term")
        for p in t.get("plates") or []:
            if not (plates_dir / f"{p}.md").exists():
                out.append(f"{tid}: plate `{p}` has no page in docs/design/plates")
        if t.get("picture"):
            for path, alt, src, _ in pictures_of(t):
                full = (vocab_dir / path).resolve()
                if not full.is_relative_to(docs.resolve()):
                    out.append(f"{tid}: picture {path} is outside docs/")
                elif not full.exists():
                    out.append(f"{tid}: picture {path} does not exist")
                if not alt or not src:
                    out.append(f"{tid}: picture {path} needs `alt` and `from`")
        if t.get("cookbook"):
            target = t["cookbook"].split("#")[0]
            if not (vocab_dir / target).exists():
                out.append(f"{tid}: cookbook link {target} does not exist")
    return out


def plate_knobs(plates_dir=PLATES):
    """Every param and object setting the plate recipes use: {name: set of plates}. Settings are
    named `setting:<key>`, as the terms' `knobs` name them."""
    used = {}

    def walk(node, plate):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "params" and isinstance(v, dict):
                    for name in v:
                        used.setdefault(name, set()).add(plate)
                elif k == "object_settings" and isinstance(v, dict):
                    for name in v:
                        used.setdefault(f"setting:{name}", set()).add(plate)
                else:
                    walk(v, plate)
        elif isinstance(node, list):
            for item in node:
                walk(item, plate)

    for f in sorted(plates_dir.glob("*.yaml")):
        try:
            walk(yaml.safe_load(f.read_text()), f.stem)
        except yaml.YAMLError:
            continue
    return used


def unnamed(data, used):
    """The knobs plates use that no term names and `not_techniques` does not excuse."""
    patterns = [k for t in data["terms"] for k in (t.get("knobs") or [])]
    excused = set(data.get("not_techniques") or {})
    return {name: plates for name, plates in sorted(used.items())
            if name not in excused and not any(fnmatch.fnmatchcase(name, p) for p in patterns)}


def cmd_check():
    data = load()
    bad = problems(data)
    if not PAGE.exists() or PAGE.read_text() != render(data):
        bad.append(f"{PAGE.relative_to(ROOT)} is behind vocabulary.yaml: run {RENDER_CMD}")
    missing = unnamed(data, plate_knobs())
    for name, plates in missing.items():
        bad.append(f"plates use `{name}` ({', '.join(sorted(plates)[:4])}) but no term names it: "
                   "add it to a term's `knobs`, give it a term, or list it under `not_techniques`")
    for line in bad:
        print("vocabulary:", line)
    if bad:
        return 1
    print(f"vocabulary: {len(data['terms'])} terms, page current, every plate knob named")
    return 0


def cmd_scan(show_all):
    data = load()
    used = plate_knobs()
    missing = unnamed(data, used)
    print(f"{len(used)} knobs across the plates; {len(missing)} named by no term")
    for name, plates in missing.items():
        print(f"  {name:28} {len(plates):3} plates  {', '.join(sorted(plates)[:5])}")
    if show_all:
        patterns = {t["id"]: t.get("knobs") or [] for t in data["terms"]}
        for name in sorted(set(used) - set(missing)):
            who = [tid for tid, ps in patterns.items()
                   if any(fnmatch.fnmatchcase(name, p) for p in ps)] or ["not a technique"]
            print(f"  {name:28} -> {', '.join(who)}")
    return 0


def cmd_json():
    """The terms for the hub, each picture as a path inside docs/."""
    data = load()
    terms = []
    for t in data["terms"]:
        card = {k: t.get(k) for k in ("id", "group", "term", "also", "what", "ours", "snippet",
                                      "lang", "plates", "related", "knobs")}
        card["pictures"] = [
            {"path": str((VOCAB_DIR / p).resolve().relative_to(DOCS.resolve())),
             "alt": alt, "from": src, "drawn": drawn}
            for p, alt, src, drawn in pictures_of(t)]
        if t.get("cookbook"):
            target, _, frag = t["cookbook"].partition("#")
            card["cookbook"] = {"path": str((VOCAB_DIR / target).resolve()
                                            .relative_to(DOCS.resolve())), "anchor": frag}
        terms.append(card)
    json.dump({"groups": data["groups"], "terms": terms}, sys.stdout, indent=1)
    print()
    return 0


# --- the pictures made for this page -----------------------------------------------------------

def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True, cwd=ROOT, **kw)


def banner(path, text):
    """A white strip on top of the picture saying what to look at."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.open(path).convert("RGB")
    font = ImageFont.load_default(size=max(22, img.width // 32))
    strip = Image.new("RGB", (img.width, font.size * 2), (255, 255, 255))
    ImageDraw.Draw(strip).text((16, font.size), text, fill=(20, 20, 20), font=font, anchor="lm")
    out = Image.new("RGB", (img.width, img.height + strip.height), (255, 255, 255))
    out.paste(strip, (0, 0))
    out.paste(img, (0, strip.height))
    out.save(path)


def cmd_pictures():
    """Slice the demo plate and draw the skirt, raft and tree-support pictures from its first
    layer; render the star at slope 0 and 0.2 and cut each through for the slope picture."""
    media = VOCAB_DIR / "media"
    review = ROOT / "tools" / "print_review.py"
    bikar = Path(os.environ.get("BIKAR_DIR", Path.home() / "Workspace/git/bikar"))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        run([ROOT / "tools/bambu/bin/bambu", "slice", "compose", media / "bases-demo.yaml",
             "--plate-type", "textured_plate", "--no-record", "-d", tmp])
        plate = tmp / "bases-demo.plate.3mf"
        spots = {o["label"]: (o["x"], o["y"]) for o in
                 json.loads((tmp / "bases-demo.plate.bedmap.json").read_text())["objects"]}
        xs = [x for x, _ in spots.values()]
        ys = [y for _, y in spots.values()]
        whole = f"{(min(xs) + max(xs)) / 2:.1f},{(min(ys) + max(ys)) / 2 + 3:.1f},90"
        shots = [
            ("skirt.png", whole, 1200,
             "Skirt: the blue loop round everything, touching nothing"),
            ("raft.png", "{:.1f},{:.1f},36".format(*spots["RAFT"]), 800,
             "Raft: the grey slab under each small star"),
            ("tree-supports.png", "{:.1f},{:.1f},44".format(*spots["TREE"]), 800,
             "Tree supports: the grey ring round each middle piece"),
        ]
        for name, region, px, words in shots:
            run(["python3", review, "paths", media / name, plate, "0.2", region, "--px", px])
            banner(media / name, words)
        cuts = []
        for slope in ("0", "0.2"):
            stl = tmp / f"star-slope-{slope}.stl"
            run(["node", bikar / "packages/cli/dist/index.js", "render",
                 bikar / "patterns/Constructions/gBV_JTt3Kxk-split-flange-coaster.bkr",
                 "--format", "stl", "--piece", "Star", "-o", stl,
                 *[a for p in ("size=112.5", "gap=0.1", "room=0.2", "halves=1", "wedge=36",
                               f"slope={slope}") for a in ("--param", p)]])
            cut = tmp / f"side-{slope}.png"
            run(["python3", review, "side", cut, stl, f"slope {slope}", "-6.5,7.27,6.5,7.27", stl])
            cuts.append(cut)
        run(["python3", review, "join", media / "slope.png", *cuts])
        shrink(media / "slope.png", 1600)
    return 0


def shrink(path, width):
    """The joined side cuts come out thousands of pixels wide; the page shows them at a few
    hundred, so keep the file small."""
    from PIL import Image
    img = Image.open(path)
    if img.width > width:
        img.resize((width, round(img.height * width / img.width)), Image.LANCZOS).save(path)


# --- self-test ---------------------------------------------------------------------------------

def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        docs = tmp / "docs"
        vocab = docs / "vocabulary"
        plates = docs / "design" / "plates"
        (vocab / "media").mkdir(parents=True)
        plates.mkdir(parents=True)
        (vocab / "media" / "a.png").write_bytes(b"png")
        (plates / "p-1.md").write_text("# p-1\n")
        (plates / "p-1.yaml").write_text(
            "items:\n  - params: { pin: 1, pins_star: 3, size: 112, band: 2 }\n"
            "    object_settings: { brim_type: outer_only }\n")
        good = {"groups": [{"id": "g", "title": "Joins"}], "not_techniques": {"size": "a size"},
                "terms": [
                    {"id": "pin", "group": "g", "term": "Pin", "what": "w", "ours": "o",
                     "picture": "media/a.png", "alt": "a", "from": "f", "knobs": ["pin", "pins_*"],
                     "plates": ["p-1"], "related": ["brim"], "snippet": "pin 1", "lang": "naqsh"},
                    {"id": "brim", "group": "g", "term": "Brim", "what": "w", "ours": "o",
                     "picture": "media/a.png", "alt": "a", "from": "f",
                     "knobs": ["setting:brim_type"]}]}
        assert problems(good, vocab, plates, docs) == [], problems(good, vocab, plates, docs)
        bad = json.loads(json.dumps(good))
        bad["terms"][0].update(plates=["p-9"], related=["nope"], picture="../../../x.png")
        bad["terms"][1].pop("alt")
        found = problems(bad, vocab, plates, docs)
        for want in ("plate `p-9`", "related `nope`", "outside docs/", "has no `alt`"):
            assert any(want in f for f in found), (want, found)
        # The by-design miss: `band` is a technique no term names, and only it is reported.
        assert list(unnamed(good, plate_knobs(plates))) == ["band"]
        page = render(good)
        assert "### Pin" in page and "[p-1](../design/plates/p-1.md)" in page
        assert "```naqsh\npin 1\n```" in page and "[Brim](#brim)" in page
        assert anchor("Supports, grid and tree") == "supports-grid-and-tree"
        assert anchor("Slope (stairs under the flange)") == "slope-stairs-under-the-flange"
    print("vocabulary self-test: ok")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("render", help="write docs/vocabulary/README.md from the YAML")
    sub.add_parser("check", help="fail when the page is behind or the YAML names something missing")
    s = sub.add_parser("scan", help="plate knobs no term names")
    s.add_argument("--all", action="store_true", help="also show which term names each knob")
    sub.add_parser("json", help="the terms for the hub")
    sub.add_parser("pictures", help="remake the pictures drawn for this page (slices, renders)")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "render":
        PAGE.write_text(render(load()))
        print("wrote", PAGE.relative_to(ROOT))
        return 0
    if a.cmd == "check":
        return cmd_check()
    if a.cmd == "scan":
        return cmd_scan(a.all)
    if a.cmd == "json":
        return cmd_json()
    if a.cmd == "pictures":
        return cmd_pictures()
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
