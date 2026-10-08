#!/usr/bin/env python3
"""Keep the pattern catalog in docs/catalog/ in step with what we have.

    python3 .claude/skills/pattern-catalog/scripts/catalog.py sync           # write
    python3 .claude/skills/pattern-catalog/scripts/catalog.py sync --check   # exit 1 if out of date

One note per construction in the ledger (docs/constructions/ledger.md), one note
per coaster style, and the catalog page (docs/catalog/index.md). Each note's top
is written here; everything from the marker line down is written by hand and
never touched. Pictures are copied from bikar's Coaster Lab thumbnails into
docs/catalog/media/<id>/<id>-<style>.png.

Read from:
  - the ledger table, for the ids, titles, creators, checks and catalog ids;
  - bikar at a git ref (origin/main by default), never its working tree, for the
    construction files, the Coaster Lab roster and the thumbnails;
  - docs/design/plates/*.yaml, for the plates each style is on;
  - docs/prints/*/index.md frontmatter, for what was printed and how it came out;
  - the coaster styles table in the import-construction skill, for style names,
    their order and one line saying what each is.

A note is found by its `id` property, never its file name, so a note keeps its
path once made. review-md's `^id` block markers on a generated line are carried
over when the line comes out the same; a marker whose line changed stops the
sync instead of cutting a comment thread loose.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / "docs"
CATALOG = DOCS / "catalog"
PATTERNS = CATALOG / "patterns"
STYLES = CATALOG / "styles"
MEDIA = CATALOG / "media"
LEDGER = DOCS / "constructions" / "ledger.md"
PLANNED = CATALOG / "planned.yaml"
PLATES = DOCS / "design" / "plates"
PRINTS = DOCS / "prints"
STYLE_TABLE = ROOT / ".claude" / "skills" / "import-construction" / "coaster-styles.md"

MARKER = "<!-- written by hand below this line; the sync tool stops here -->"
NO_PIECE = "no piece by design"
CONSTRUCTIONS = "patterns/Constructions/"
THUMBS = "packages/lab/src/coaster-thumbs/"
ROSTER = "packages/lab/src/coaster-scripts.ts"

NEW_NOTE_HAND_PART = (
    "\n\n## Notes\n\n"
    "Nothing written by hand yet. This is the place for what makes the pattern work, what went\n"
    "wrong, and what to try next.\n"
)
NEW_STYLE_HAND_PART = "\n\n## Notes\n\nNothing written by hand yet.\n"

# ---------------------------------------------------------------- bikar, read at a ref


def bikar_dir(arg: str | None) -> Path:
    """Where bikar's git repository is: --bikar-dir, then $BIKAR_DIR, then the usual spots."""
    candidates = [arg, os.environ.get("BIKAR_DIR")]
    home = Path.home() / "Workspace" / "git"
    candidates += [str(home / "bikar-work"), str(home / "bikar-main"), str(home / "bikar")]
    for c in candidates:
        if not c:
            continue
        p = Path(c).expanduser()
        if (p / ".git").exists() or (p / "HEAD").is_file():  # a checkout, or a bare repository
            return p
    sys.exit("catalog: bikar not found; pass --bikar-dir or set BIKAR_DIR")


class Bikar:
    def __init__(self, repo: Path, ref: str | None):
        self.repo = repo
        self.ref = ref or self._default_ref()
        self.tree = set(self._git("ls-tree", "-r", "--name-only", self.ref).decode().splitlines())

    def _git(self, *args: str) -> bytes:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        return subprocess.run(
            ["git", "-C", str(self.repo), *args], capture_output=True, check=True, env=env
        ).stdout

    def _default_ref(self) -> str:
        for ref in ("origin/main", "main"):
            try:
                self._git("rev-parse", "--verify", "--quiet", ref)
                return ref
            except subprocess.CalledProcessError:
                continue
        sys.exit(f"catalog: no origin/main or main in {self.repo}")

    def read(self, path: str) -> bytes:
        return self._git("show", f"{self.ref}:{path}")

    def construction_files(self, cid: str) -> list[str]:
        """The `.bkr` files for one construction: the drawing first, then plain, then the rest."""
        names = sorted(
            p[len(CONSTRUCTIONS):]
            for p in self.tree
            if p.startswith(CONSTRUCTIONS)
            and "/" not in p[len(CONSTRUCTIONS):]
            and p.endswith(".bkr")
            and (p[len(CONSTRUCTIONS):] == f"{cid}.bkr" or p[len(CONSTRUCTIONS):].startswith(f"{cid}-"))
        )
        first = [n for n in (f"{cid}.bkr", f"{cid}-coaster.bkr") if n in names]
        return first + [n for n in names if n not in first]

    def roster(self) -> dict[str, dict[str, str]]:
        """Coaster Lab roster, keyed by `.bkr` file name: the thumbnail id and the one-line blurb."""
        text = self.read(ROSTER).decode()
        out: dict[str, dict[str, str]] = {}
        for block in re.findall(r"\{\s*id:.*?source:", text, flags=re.S):
            rid = re.search(r"id:\s*'([^']+)'", block)
            fname = re.search(r"file:\s*'([^']+)'", block)
            blurb = re.search(r"blurb:\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")", block, flags=re.S)
            if rid and fname:
                b = (blurb.group(1) or blurb.group(2) or "") if blurb else ""
                out[fname.group(1)] = {"id": rid.group(1), "blurb": " ".join(b.split())}
        return out


# ---------------------------------------------------------------- inputs in this repo


@dataclass
class Row:
    id: str
    title_md: str  # as the ledger writes it, markdown kept, creator removed
    creator: str
    naqsh: str
    checks: tuple[str, str, str]
    catalog_id: str

    @property
    def title(self) -> str:
        return self.title_md.replace("*", "")

    @property
    def no_piece(self) -> bool:
        return self.naqsh == NO_PIECE

    @property
    def migrated(self) -> bool:
        return self.naqsh.startswith("`bikar/")


def cell(s: str) -> str:
    s = s.strip()
    return "" if s in ("—", "-") else s


def read_ledger() -> list[Row]:
    rows: list[Row] = []
    in_table = False
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if line.startswith("| id | title |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        if line.startswith("|---"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        cid = cols[0].strip("`")
        title = cols[1]
        creator = ""
        m = re.match(r"^(.*?)\s*\(([^()]+)\)\s*$", title)
        if m:
            title, creator = m.group(1), m.group(2)
        rows.append(
            Row(
                id=cid,
                title_md=title,
                creator=creator,
                naqsh=cols[3],
                checks=(cell(cols[4]), cell(cols[5]), cell(cols[6])),
                catalog_id=cell(cols[8]),
            )
        )
    if not rows:
        sys.exit(f"catalog: no ledger table found in {LEDGER}")
    return rows


@dataclass
class Style:
    name: str
    what: str


def read_styles() -> list[Style]:
    """The styles table, in its order: name of record (the file suffix) and what it is."""
    out: list[Style] = []
    for line in STYLE_TABLE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| \*\*([a-z-]+)\*\*[^|]*\|[^|]*\|[^|]*\| ([^|]+) \|", line)
        if m:
            out.append(Style(m.group(1), m.group(2).strip()))
    if not out:
        sys.exit(f"catalog: no styles found in {STYLE_TABLE}")
    return out


def style_of(cid: str, fname: str) -> str | None:
    """`<id>-minimal-frame-coaster.bkr` → `minimal-frame`; `<id>-coaster.bkr` → `plain`; the drawing → None."""
    stem = fname[len(cid):-len(".bkr")]
    if not stem:
        return None
    stem = stem.lstrip("-")
    if stem == "coaster":
        return "plain"
    return stem[: -len("-coaster")] if stem.endswith("-coaster") else stem


def plates_by_file() -> dict[str, list[str]]:
    """`.bkr` file name → the plates (by name) whose recipe uses it."""
    out: dict[str, list[str]] = {}
    for p in sorted(PLATES.glob("*.yaml")):
        for fname in sorted(set(re.findall(r"Constructions/([A-Za-z0-9_-]+\.bkr)", p.read_text(encoding="utf-8")))):
            out.setdefault(fname, []).append(p.stem)
    return out


@dataclass
class PrintObject:
    run: str
    file: str
    piece: str
    params: dict
    count: int
    verdict: str
    notes: list[str] = field(default_factory=list)


def read_prints() -> list[PrintObject]:
    out: list[PrintObject] = []
    for idx in sorted(PRINTS.glob("*/index.md")):
        text = idx.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
        if not m:
            continue
        front = yaml.safe_load(m.group(1)) or {}
        for obj in front.get("objects") or []:
            src = str(obj.get("source") or "")
            fm = re.match(r"^bikar:patterns/Constructions/([A-Za-z0-9_-]+\.bkr)$", src)
            if not fm:
                continue
            out.append(
                PrintObject(
                    run=idx.parent.name,
                    file=fm.group(1),
                    piece=str(obj.get("piece") or ""),
                    params=obj.get("params") or {},
                    count=int(obj.get("count") or 1),
                    verdict=str(obj.get("verdict") or ""),
                    notes=[str(n) for n in obj.get("notes") or []],
                )
            )
    return out


@dataclass
class Planned:
    id: str
    title: str
    source: str
    creator: str
    screen: str  # the research file that queued it, from the repo root
    watch: str
    held: str  # why it is held, or "" when it is queued


def read_planned() -> list[Planned]:
    """Queued and held patterns not yet rebuilt, written by hand in docs/catalog/planned.yaml."""
    if not PLANNED.exists():
        return []
    out: list[Planned] = []
    for e in yaml.safe_load(PLANNED.read_text(encoding="utf-8")) or []:
        missing = [k for k in ("id", "title", "source", "screen", "watch") if not e.get(k)]
        if missing:
            sys.exit(f"catalog: {PLANNED.relative_to(ROOT)}: entry {e.get('id', '?')} has no {', '.join(missing)}")
        out.append(Planned(
            str(e["id"]), " ".join(str(e["title"]).split()), str(e["source"]), str(e.get("creator") or ""),
            str(e["screen"]), " ".join(str(e["watch"]).split()), " ".join(str(e.get("held") or "").split()),
        ))
    return out


def existing_notes(folder: Path, key: str) -> dict[str, Path]:
    """Notes in `folder` keyed by their frontmatter `key` property."""
    out: dict[str, Path] = {}
    for p in sorted(folder.glob("*.md")):
        m = re.match(r"^---\n(.*?)\n---\n", p.read_text(encoding="utf-8"), flags=re.S)
        if m:
            front = yaml.safe_load(m.group(1)) or {}
            if front.get(key):
                out[str(front[key])] = p
    return out


# ---------------------------------------------------------------- writing


def slug(text: str) -> str:
    text = text.replace("√", "root ").replace("*", "").replace("'", "").replace("’", "").lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def yaml_scalar(v: str) -> str:
    if re.fullmatch(r"https?://[^\s#]+", v):
        return v
    return v if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ,.()'’—–/_-]*", v) else json.dumps(v, ensure_ascii=False)


def frontmatter(props: list[tuple[str, object]]) -> str:
    lines = ["---"]
    for k, v in props:
        if isinstance(v, list):
            lines.append(f"{k}:")
            lines += [f"  - {yaml_scalar(str(x))}" for x in v]
        elif v == "" or v is None:
            lines.append(f"{k}:")
        else:
            lines.append(f"{k}: {yaml_scalar(str(v))}")
    lines.append("---")
    return "\n".join(lines) + "\n"


FOLD_WORDS = {
    "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "twelve": "12", "sixteen": "16", "fivefold": "5", "sixfold": "6", "tenfold": "10",
}


def tags_for(row: Row, has_coaster: bool) -> list[str]:
    tags = title_tags(row.title)
    if has_coaster:
        tags.append("coaster")
    if row.no_piece:
        tags.append("no-piece-by-design")
    return tags


def title_tags(title: str) -> list[str]:
    tags: list[str] = []
    for word in re.findall(r"\b([a-z0-9]+)-?fold\b", title.lower()):
        word = FOLD_WORDS.get(word, FOLD_WORDS.get(word + "fold", word))
        if word in ("m,n", "n", "m"):
            continue
        tag = f"{word}-fold"
        if tag not in tags:
            tags.append(tag)
    for word in ("star", "rosette"):
        if re.search(rf"\b{word}s?\b", title.lower()):
            tags.append(word)
    return tags


def check_lines(row: Row) -> list[str]:
    o1, o2, o3 = row.checks
    if not any(row.checks):
        return ["Not run yet: the three checks run once the pattern is written in naqsh."]
    lines: list[str] = []

    def verdict(cell_: str) -> tuple[str, str] | None:
        m = re.match(r"^(PASS|FAIL) ([0-9.]+)(?:/([0-9.]+))?$", cell_)
        return (m.group(1), m.group(2), m.group(3)) if m else None  # type: ignore[return-value]

    v = verdict(o1)
    if v and v[2] is not None:
        failed = "none failed" if v[2] == "0" else f"{v[2]} failed"
        lines.append(f"- every labelled point and line: {v[1]} compared, {failed} ({v[0]});")
    elif o1:
        lines.append(f"- every labelled point and line: {o1};")
    v = verdict(o2)
    if v and v[2] is not None:
        lines.append(f"- the drawn lines: recall {v[1]}, precision {v[2]} ({v[0]});")
    elif o2:
        lines.append(f"- the drawn lines: {o2};")
    v = verdict(o3)
    if v:
        lines.append(f"- the solid coverage: {v[1]} ({v[0]}).")
    elif o3:
        lines.append(f"- the solid coverage: {o3}.")
    else:
        lines.append("- the solid coverage: not run.")
    fails = sum(1 for c in row.checks if c.startswith("FAIL"))
    passes = sum(1 for c in row.checks if c.startswith("PASS"))
    if fails:
        head = f"{passes} of the three checks pass and {fails} fail; the ledger's notes say why."
    elif passes == 3:
        head = "All three checks against the video's GeoGebra construction pass:"
    else:
        head = f"{passes} of the three checks were run, and they pass:"
    return [head, ""] + lines


def piece_words(obj: PrintObject, style: str) -> str:
    words = style.replace("-", " ")
    if obj.piece and obj.piece != "Coaster":
        words += f", {obj.piece.lower()}"
    size = obj.params.get("size")
    if size is not None:
        words += f", {size:g} mm" if isinstance(size, (int, float)) else f", {size} mm"
    if obj.count > 1:
        words += f", {obj.count} of them"
    return words


def md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


@dataclass
class Picture:
    style: str
    rel: str  # path from a note in patterns/ or styles/: ../media/<id>/<id>-<style>.png
    data: bytes


@dataclass
class Built:
    row: Row
    path: Path
    files: list[str]
    styles: list[str]
    pictures: dict[str, Picture]
    status: str


def note_top(b: Built, style_what: dict[str, str], roster: dict, plates: dict, prints: list[PrintObject]) -> str:
    row = b.row
    video = f"https://www.youtube.com/watch?v={row.id}"
    props: list[tuple[str, object]] = [
        ("id", row.id),
        ("aliases", [row.id]),
        ("title", row.title),
        ("family", "constructions"),
        ("status", b.status),
        ("source", video),
        ("creator", row.creator),
        ("catalog id", row.catalog_id),
        ("bikar files", [CONSTRUCTIONS + f for f in b.files]),
        ("tags", tags_for(row, bool(b.styles))),
    ]
    out = [frontmatter(props).rstrip("\n"), ""]
    heading = f"# {row.title_md}" + (f" ({row.catalog_id})" if row.catalog_id else "")
    out += [heading, ""]
    who = f"[{row.creator}'s video]({video})" if row.creator else f"[the video]({video})"
    if row.no_piece:
        out.append(f"Rebuilt from {who}. The video shows a way of drawing, not a finished piece, so there is nothing")
        out.append("to make from it: the ledger marks it \"no piece by design\".")
    elif not row.migrated:
        out.append(f"Rebuilt step by step from {who} in the youtube repo. It is not written in naqsh yet, so it")
        out.append("has no bikar file, no coaster and no pictures. The ledger lists it as not yet migrated.")
    else:
        n = len(b.styles)
        made = f"in {n} coaster style{'s' if n != 1 else ''}" if n else "with no coaster yet"
        cat = f" Its catalog id is {row.catalog_id}." if row.catalog_id else ""
        out.append(f"Rebuilt step by step from {who}, written in naqsh and made {made}.{cat}")
    out.append("")

    if b.styles:
        out += ["## Pictures", ""]
        out.append("One heading per style, so each picture has its own link: the note's link plus the style")
        out.append(f"name, for example #{b.styles[0]}.")
        out.append("")
        for s in b.styles:
            out += [f"### {s}", ""]
            fname = next(f for f in b.files if style_of(row.id, f) == s)
            what = style_what.get(s) or roster.get(fname, {}).get("blurb", "")
            if what:
                out += [what[0].upper() + what[1:] + ("" if what.endswith(".") else "."), ""]
            pic = b.pictures.get(s)
            if pic:
                out += [f"![{s.replace('-', ' ')}]({pic.rel})", ""]
            else:
                out += ["No picture yet: Coaster Lab has no thumbnail for this file.", ""]

    if not row.no_piece:
        out += ["## Checks against the video", ""]
        out.append("From the [constructions ledger](../../constructions/ledger.md).")
        out.append("")
        out += check_lines(row)
        out.append("")

    if b.styles:
        out += ["## Coaster styles and plates", ""]
        on: dict[str, list[str]] = {}
        for f in b.files:
            for plate in plates.get(f, []):
                s = style_of(row.id, f)
                if s and s not in on.setdefault(plate, []):
                    on[plate].append(s)
        if on:
            out += ["| Plate | Styles of this pattern on it |", "|---|---|"]
            for plate in sorted(on):
                page = PLATES / f"{plate}.md"
                link = f"../../design/plates/{plate}.md" if page.exists() else f"../../design/plates/{plate}.yaml"
                out.append(f"| [{plate}]({link}) | {', '.join(s.replace('-', ' ') for s in on[plate])} |")
        else:
            out.append("No plate uses this pattern yet.")
        out.append("")

        out += ["## Prints", ""]
        mine = [o for o in prints if o.file in b.files]
        if mine:
            out += ["| Print | Piece | Verdict | What was seen |", "|---|---|---|---|"]
            for o in mine:
                s = style_of(row.id, o.file) or ""
                seen = "; ".join(o.notes) or "nothing written yet"
                out.append(
                    f"| [{o.run}](../../prints/{o.run}/index.md) | {md_cell(piece_words(o, s))} "
                    f"| {o.verdict or 'not judged'} | {md_cell(seen)} |"
                )
        else:
            out.append("No print record names this pattern yet.")
        out.append("")
    return "\n".join(out)


def planned_top(p: Planned, path: Path) -> str:
    tags = title_tags(p.title) + ["planned"] + (["held"] if p.held else [])
    props: list[tuple[str, object]] = [
        ("id", p.id),
        ("aliases", [p.id]),
        ("title", p.title),
        ("family", "constructions"),
        ("status", "planned"),
        ("source", p.source),
        ("creator", p.creator),
        ("catalog id", ""),
        ("bikar files", []),
        ("tags", tags),
    ]
    screen = os.path.relpath(ROOT / p.screen, path.parent)
    kind = "GeoGebra file" if "geogebra.org" in p.source else "video"
    who = f"[{p.creator}'s {kind}]({p.source})" if p.creator else f"[the {kind}]({p.source})"
    out = [frontmatter(props).rstrip("\n"), "", f"# {p.title}", ""]
    if p.held:
        out.append(f"Queued from {who} by [the candidate screen]({screen}), then held. It is not rebuilt yet,")
    else:
        out.append(f"Queued from {who} by [the candidate screen]({screen}). It is not rebuilt yet,")
    out += ["so it has no ledger row, no bikar file and no pictures.", ""]
    if p.held:
        out += ["## Why it is held", "", p.held, ""]
    out += ["## What to watch for", "", p.watch, ""]
    return "\n".join(out)


BLOCK_ID = re.compile(r"^(.*\S) (\^[A-Za-z0-9-]+)$")


def carry_block_ids(old_top: str, new_top: str, where: Path) -> str:
    """Put review-md's `^id` markers back on the regenerated lines they were on."""
    ids: dict[str, str] = {}
    for line in old_top.splitlines():
        m = BLOCK_ID.match(line)
        if m:
            ids[m.group(1)] = m.group(2)
    if not ids:
        return new_top
    lines = new_top.splitlines()
    placed: set[str] = set()
    for i, line in enumerate(lines):
        if line in ids and ids[line] not in placed:
            lines[i] = f"{line} {ids[line]}"
            placed.add(ids[line])
    lost = [f"{bid} (on: {text})" for text, bid in ids.items() if bid not in placed]
    if lost:
        sys.exit(
            f"catalog: {where.relative_to(ROOT)}: a comment thread is anchored on a generated line that "
            f"changed, so the sync would cut it loose: {'; '.join(lost)}. Move the thread or the text by hand first."
        )
    return "\n".join(lines) + ("\n" if new_top.endswith("\n") else "")


def split_note(text: str) -> tuple[str, str]:
    i = text.find(MARKER)
    return (text, "") if i < 0 else (text[:i], text[i + len(MARKER):])


def assemble(path: Path, top: str, new_hand: str) -> str:
    if path.exists():
        old_top, hand = split_note(path.read_text(encoding="utf-8"))
        if not hand and MARKER not in path.read_text(encoding="utf-8"):
            hand = new_hand
        top = carry_block_ids(old_top, top, path)
    else:
        hand = new_hand
    return top.rstrip("\n") + "\n\n" + MARKER + hand


# ---------------------------------------------------------------- the run


def build(bikar: Bikar) -> tuple[dict[Path, bytes], list[str]]:
    rows = read_ledger()
    styles = read_styles()
    style_what = {s.name: s.what for s in styles}
    style_order = {s.name: i for i, s in enumerate(styles)}
    roster = bikar.roster()
    plates = plates_by_file()
    prints = read_prints()
    by_id = existing_notes(PATTERNS, "id")
    warnings: list[str] = []
    out: dict[Path, bytes] = {}
    built: list[Built] = []

    seen_paths: set[Path] = set()
    for row in rows:
        files = [] if row.no_piece or not row.migrated else bikar.construction_files(row.id)
        if row.migrated and f"{row.id}.bkr" not in files:
            warnings.append(f"{row.id}: the ledger names a naqsh file bikar {bikar.ref} does not have")
        styles_here = sorted(
            {s for f in files if (s := style_of(row.id, f))},
            key=lambda s: (style_order.get(s, len(style_order)), s),
        )
        name = slug(row.title) + (f"-{row.catalog_id.lower()}" if row.catalog_id else "")
        path = by_id.get(row.id, PATTERNS / f"{name}.md")
        if path in seen_paths:
            sys.exit(f"catalog: two ledger rows map to {path.relative_to(ROOT)}")
        seen_paths.add(path)
        pictures: dict[str, Picture] = {}
        for s in styles_here:
            fname = next(f for f in files if style_of(row.id, f) == s)
            entry = roster.get(fname)
            thumb = f"{THUMBS}{entry['id']}.png" if entry else None
            if thumb and thumb in bikar.tree:
                media = MEDIA / row.id / f"{row.id}-{s}.png"
                pictures[s] = Picture(s, f"../media/{row.id}/{media.name}", bikar.read(thumb))
                out[media] = pictures[s].data
            else:
                warnings.append(f"{row.id}: no Coaster Lab picture for {fname}")
        if row.no_piece:
            status = "built"  # nothing to make, and nothing left to do: the status list has no better word
        elif not row.migrated:
            status = "rebuilding"
        elif any(o.file in files for o in prints):
            status = "printed"
        else:
            status = "built"
        b = Built(row, path, files, styles_here, pictures, status)
        built.append(b)
        out[path] = assemble(path, note_top(b, style_what, roster, plates, prints), NEW_NOTE_HAND_PART).encode()

    ledger_ids = {r.id for r in rows}
    planned: list[tuple[Planned, Path]] = []
    for p in read_planned():
        if p.id in ledger_ids:
            warnings.append(f"{p.id} is in the ledger now; take it out of {PLANNED.relative_to(ROOT)}")
            continue
        path = by_id.get(p.id, PATTERNS / f"{slug(p.title)}.md")
        if path in seen_paths:
            sys.exit(f"catalog: {p.id} in {PLANNED.relative_to(ROOT)} maps to {path.relative_to(ROOT)}, which is taken")
        seen_paths.add(path)
        planned.append((p, path))
        out[path] = assemble(path, planned_top(p, path), NEW_NOTE_HAND_PART).encode()

    known = ledger_ids | {p.id for p, _ in planned}
    for nid, path in by_id.items():
        if nid not in known:
            warnings.append(f"{path.relative_to(ROOT)}: id {nid} is not in the ledger or the planned list (left as it is)")

    # style notes
    by_style: dict[str, list[Built]] = {}
    for b in built:
        for s in b.styles:
            by_style.setdefault(s, []).append(b)
    all_styles = sorted(set(style_what) | set(by_style), key=lambda s: (style_order.get(s, len(style_order)), s))
    style_paths = existing_notes(STYLES, "style") if STYLES.exists() else {}
    for s in all_styles:
        path = style_paths.get(s, STYLES / f"{s}.md")
        out[path] = assemble(path, style_top(s, style_what, by_style.get(s, []), roster), NEW_STYLE_HAND_PART).encode()

    out[CATALOG / "index.md"] = index_page(built, planned, all_styles, by_style).encode()
    return out, warnings


def style_top(s: str, style_what: dict[str, str], members: list[Built], roster: dict) -> str:
    props: list[tuple[str, object]] = [
        ("style", s),
        ("aliases", [f"{s} style"]),
        ("title", f"The {s} coaster style"),
        ("family", "coaster styles"),
        ("tags", ["coaster-style"]),
    ]
    out = [frontmatter(props).rstrip("\n"), "", f"# The {s} coaster style", ""]
    what = style_what.get(s)
    if what:
        out.append(what[0].upper() + what[1:] + ("" if what.endswith(".") else "."))
        out.append("")
        out.append(
            "The name, the file it comes from and where it was decided are in the "
            "[coaster styles table](../../../.claude/skills/import-construction/coaster-styles.md)."
        )
    else:
        blurbs = [roster.get(f, {}).get("blurb", "") for b in members for f in b.files if style_of(b.row.id, f) == s]
        if blurbs and blurbs[0]:
            out.append(blurbs[0][0].upper() + blurbs[0][1:] + ".")
            out.append("")
        out.append(
            "Not in the [coaster styles table](../../../.claude/skills/import-construction/coaster-styles.md) yet: "
            "only one pattern is made this way."
        )
    out += ["", "## Patterns in this style", ""]
    if not members:
        out.append("No pattern is made in this style yet.")
    for b in members:
        label = b.row.title_md + (f" ({b.row.catalog_id})" if b.row.catalog_id else "")
        out += [f"### {b.row.id}", "", f"[{label}](../patterns/{b.path.name}#{s})", ""]
        pic = b.pictures.get(s)
        if pic:
            out += [f"![{b.row.id} {s.replace('-', ' ')}]({pic.rel})", ""]
    return "\n".join(out)


def index_page(
    built: list[Built], planned: list[tuple[Planned, Path]], all_styles: list[str], by_style: dict[str, list[Built]]
) -> str:
    def cs_key(b: Built) -> tuple[int, str]:
        m = re.match(r"CS-(\d+)$", b.row.catalog_id)
        return (int(m.group(1)) if m else 10**6, b.row.title.lower())

    made = sorted([b for b in built if b.styles], key=cs_key)
    waiting = sorted([b for b in built if not b.styles and not b.row.no_piece], key=lambda b: b.row.title.lower())
    none = [b for b in built if b.row.no_piece]
    out = [
        "---",
        "title: Pattern catalog",
        "tags:",
        "  - catalog",
        "---",
        "",
        "# Pattern catalog",
        "",
        "Every pattern we have, one note each. This page is written by the catalog tool",
        "(`python3 .claude/skills/pattern-catalog/scripts/catalog.py sync`); edit the notes, not this",
        "page. How the catalog is laid out and why: [the plan](plan.md).",
        "",
        f"## Constructions made into coasters ({len(made)})",
        "",
        "| Picture | Pattern | Catalog id | Status | Styles |",
        "|---|---|---|---|---|",
    ]
    for b in made:
        first = next((b.pictures[s] for s in b.styles if s in b.pictures), None)
        pic = f"![{b.row.id}\\|96]({first.rel.removeprefix('../')})" if first else ""
        out.append(
            f"| {pic} | [{md_cell(b.row.title_md)}](patterns/{b.path.name}) | {b.row.catalog_id} "
            f"| {b.status} | {', '.join(b.styles)} |"
        )
    out += [
        "",
        f"## Rebuilt from the video, not yet in naqsh ({len(waiting)})",
        "",
        "Rebuilt in the youtube repo. No bikar file yet, so no coaster and no picture.",
        "",
        "| Pattern | Creator |",
        "|---|---|",
    ]
    for b in waiting:
        out.append(f"| [{md_cell(b.row.title_md)}](patterns/{b.path.name}) | {b.row.creator or 'not recorded'} |")
    if planned:
        out += [
            "",
            f"## Queued, not yet rebuilt ({len(planned)})",
            "",
            "Screened and queued, or held. Add one to [the planned list](planned.yaml) and sync.",
            "",
            "| Pattern | Creator | Held |",
            "|---|---|---|",
        ]
        for p, path in sorted(planned, key=lambda x: x[0].title.lower()):
            out.append(f"| [{md_cell(p.title)}](patterns/{path.name}) | {p.creator or 'not recorded'} | {'held' if p.held else ''} |")
    if none:
        out += ["", "## Nothing to make, by design", ""]
        for b in none:
            out.append(f"- [{b.row.title_md}](patterns/{b.path.name}): the video shows a way of drawing, not a piece.")
    out += ["", "## Coaster styles", "", "| Style | Patterns made in it |", "|---|---|"]
    for s in all_styles:
        out.append(f"| [{s}](styles/{s}.md) | {len(by_style.get(s, []))} |")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("sync", help="write the catalog notes, pictures and index")
    sp.add_argument("--check", action="store_true", help="write nothing; exit 1 when anything is out of date")
    sp.add_argument("--bikar-dir", help="bikar's git repository (default: $BIKAR_DIR, then ~/Workspace/git/bikar-work)")
    sp.add_argument("--bikar-ref", help="the bikar ref to read (default: origin/main)")
    args = ap.parse_args()

    bikar = Bikar(bikar_dir(args.bikar_dir), args.bikar_ref)
    out, warnings = build(bikar)
    for w in warnings:
        print(f"catalog: note: {w}")

    stale = [p for p, data in out.items() if not p.exists() or p.read_bytes() != data]
    if args.check:
        for p in stale:
            print(f"catalog: out of date: {p.relative_to(ROOT)}")
        if stale:
            print(f"catalog: FAIL — {len(stale)} file(s) out of date; run the sync without --check")
            return 1
        print(f"catalog: OK — {len(out)} files in step with the ledger and bikar {bikar.ref}")
        return 0
    for p in stale:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(out[p])
        print(f"catalog: wrote {p.relative_to(ROOT)}")
    print(f"catalog: {len(stale)} written, {len(out) - len(stale)} already in step (bikar {bikar.ref})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
