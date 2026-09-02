#!/usr/bin/env python3
"""Write `status-manifest.json` — the three facts `status.html` reads — from files.

The status page (`status.html`, a sibling of `index.html`) says what the gallery
was built from and nothing more. It shows three facts and types none of them:

  1. the bikar commit the renders were built from — `build/bikar-ref.txt`, the
     stamp `make bikar-stamp` writes (a sha, a ref, and `+dirty` when the tree was);
  2. the `as_of` commits the use-case map was last checked against — the frontmatter
     of `.claude/skills/maintain-use-cases/use-cases.md`, one sha per repo;
  3. the last deploy — the tip of the `gh-pages` branch, whose commit subject
     `make deploy` writes as `Deploy gallery from master (<short>)`, so the manifest
     can name the master commit that deploy published.

This script is the only thing that writes the manifest, and it reads, never types:
each fact is present exactly when the file (or ref) that carries it is, and an
absent source writes `null` for that fact, which the page renders as the true
state ("not stamped yet", "not deployed yet") rather than an error or a guess. A
manifest someone edited by hand would be the drift this page exists to refuse, so
the file is gitignored and `make deploy` rebuilds it, with the self-test below run
before every write.

Nothing here needs PyYAML: the `as_of` block is a fixed, shallow shape and is
parsed by hand, the same discipline `build/prints_manifest.py` keeps so the check
runs under whatever `python3` a git hook happens to hand it.

Usage:
  status_manifest.py               write <repo>/status-manifest.json
  status_manifest.py --out PATH    write elsewhere (the Makefile does not)
  status_manifest.py --self-test   build a fixture repo and check the output
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "status-manifest.json"
BIKAR_REF = "build/bikar-ref.txt"
USE_CASES = ".claude/skills/maintain-use-cases/use-cases.md"
PAGES_BRANCH = "gh-pages"
SHORT = 7
SCHEMA = 1

# `<40-hex sha> <ref>` with an optional ` +dirty`, exactly what bikar-stamp writes.
_BIKAR_LINE = re.compile(r"^([0-9a-f]{40})\s+(\S+)(\s+\+dirty)?\s*$")
# `Deploy gallery from master (<short sha>)`, exactly what the deploy target writes.
_DEPLOY_SUBJECT = re.compile(r"^Deploy gallery from master \(([0-9a-f]{4,40})\)")


def parse_bikar_ref(text: str) -> dict | None:
    """`{sha, short, ref, dirty}` from `build/bikar-ref.txt`, or None if unparseable.

    A stamp that does not match the shape bikar-stamp writes is not massaged into
    a half-fact: it is None, and the page says the gallery was not stamped, which
    is the honest reading of a file it cannot trust.
    """
    m = _BIKAR_LINE.match(text.strip())
    if not m:
        return None
    sha, ref, dirty = m.group(1), m.group(2), bool(m.group(3))
    return {"sha": sha, "short": sha[:SHORT], "ref": ref, "dirty": dirty}


def parse_as_of(text: str) -> dict:
    """`{repo: sha}` from the `as_of:` block of the use-case map's frontmatter.

    Reads only the frontmatter (the first `---`-fenced block) and only the
    `as_of:` mapping inside it — one indented `<repo>: <40-hex>` line each,
    ending at the next top-level key. An empty or missing block is `{}`, which
    the page shows as "no pins recorded".
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}
    front = lines[1:end]
    pins: dict[str, str] = {}
    in_block = False
    for line in front:
        if re.match(r"^as_of\s*:\s*$", line):
            in_block = True
            continue
        if in_block:
            # A non-indented, non-blank line ends the block.
            if line.strip() and not line[0].isspace():
                break
            m = re.match(r"^\s+([\w.-]+)\s*:\s*([0-9a-f]{40})\s*$", line)
            if m:
                pins[m.group(1)] = m.group(2)
    return pins


def parse_deploy_subject(subject: str) -> str | None:
    """The master short-sha a deploy commit's subject names, or None."""
    m = _DEPLOY_SUBJECT.match(subject.strip())
    return m.group(1) if m else None


def deploy_from_git(root: Path) -> dict | None:
    """`{sha, short, date, from_master}` for the `gh-pages` tip, or None.

    Reads the branch with one `git log`. If `root` is not a repo, or has no
    `gh-pages` branch (a fresh clone that has never deployed), the read fails and
    the fact is None — "not deployed yet", not an error. `from_master` is None
    when the tip is not a deploy commit (someone committed to gh-pages by hand):
    the deploy exists, but it did not name a master commit, and the page says so.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "log", "-1", "--format=%H%n%cI%n%s", PAGES_BRANCH],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return None
    if out.returncode != 0:
        return None
    parts = out.stdout.splitlines()
    if len(parts) < 3:
        return None
    sha, iso, subject = parts[0], parts[1], parts[2]
    return {
        "sha": sha,
        "short": sha[:SHORT],
        "date": iso[:10],
        "from_master": parse_deploy_subject(subject),
    }


def build(root: Path) -> dict:
    """The manifest for the three facts held under `root`."""
    ref_path = root / BIKAR_REF
    uc_path = root / USE_CASES
    bikar = parse_bikar_ref(ref_path.read_text(encoding="utf-8")) if ref_path.is_file() else None
    as_of = parse_as_of(uc_path.read_text(encoding="utf-8")) if uc_path.is_file() else {}
    return {
        "schema": SCHEMA,
        "generated": dt.date.today().isoformat(),
        "source": f"{BIKAR_REF}, {USE_CASES} as_of, {PAGES_BRANCH} tip — via build/status_manifest.py",
        "bikar_ref": bikar,
        "as_of": as_of,
        "deploy": deploy_from_git(root),
    }


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


def self_test() -> int:
    """Build a fixture repo and assert the manifest says what the files say."""
    import os
    import tempfile

    failures = 0

    def check(label: str, ok: bool, why: str = "") -> None:
        nonlocal failures
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" — {why}"))

    # Pure parsers first — the facts the page cannot afford to get subtly wrong.
    good = "abcdef0123456789abcdef0123456789abcdef01 main\n"
    check("a clean stamp parses to sha+ref, not dirty",
          parse_bikar_ref(good) == {"sha": "abcdef0123456789abcdef0123456789abcdef01",
                                    "short": "abcdef0", "ref": "main", "dirty": False})
    check("a +dirty stamp is read as dirty",
          parse_bikar_ref(good.rstrip() + " +dirty\n") == {
              "sha": "abcdef0123456789abcdef0123456789abcdef01",
              "short": "abcdef0", "ref": "main", "dirty": True})
    # By-design failure: a stamp that is not the shape bikar-stamp writes is None,
    # never a half-parsed fact the page would show as real.
    check("a malformed stamp is None, not a half-fact",
          parse_bikar_ref("not a sha at all\n") is None)
    check("a short sha in a stamp is refused (only 40-hex is a stamp)",
          parse_bikar_ref("abcdef0 main\n") is None)

    front = (
        "---\n"
        "name: use-cases\n"
        "as_of:\n"
        "  3d-models: " + "1" * 40 + "\n"
        "  bikar: " + "2" * 40 + "\n"
        "  qiyas: " + "3" * 40 + "\n"
        "repos:\n"
        "  bikar: ../bikar\n"
        "---\n\n# body\n"
    )
    check("as_of reads exactly the three pins and stops at the next key",
          parse_as_of(front) == {"3d-models": "1" * 40, "bikar": "2" * 40, "qiyas": "3" * 40})
    check("no frontmatter is no pins, not a crash", parse_as_of("# just a doc\n") == {})

    check("a deploy subject yields the master short-sha",
          parse_deploy_subject("Deploy gallery from master (c40dbc7)") == "c40dbc7")
    check("a hand commit on gh-pages names no master sha",
          parse_deploy_subject("fix a typo") is None)

    # Now the whole thing against a real fixture on disk + in git.
    with tempfile.TemporaryDirectory(prefix="status-manifest-") as tmp:
        root = Path(tmp)
        (root / "build").mkdir()
        (root / "build" / "bikar-ref.txt").write_text(good, encoding="utf-8")
        uc = root / ".claude" / "skills" / "maintain-use-cases"
        uc.mkdir(parents=True)
        (uc / "use-cases.md").write_text(front, encoding="utf-8")
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        subprocess.run(["git", "-C", tmp, "init", "-q"], check=True, env=env)
        subprocess.run(["git", "-C", tmp, "checkout", "-q", "-b", "master"], check=True, env=env)
        subprocess.run(["git", "-C", tmp, "commit", "-q", "--allow-empty",
                        "-m", "seed"], check=True, env=env)
        subprocess.run(["git", "-C", tmp, "checkout", "-q", "-b", PAGES_BRANCH], check=True, env=env)
        subprocess.run(["git", "-C", tmp, "commit", "-q", "--allow-empty",
                        "-m", "Deploy gallery from master (c40dbc7)"], check=True, env=env)

        m = build(root)
        check("the manifest reads the bikar stamp off disk",
              m["bikar_ref"] and m["bikar_ref"]["ref"] == "main", json.dumps(m["bikar_ref"]))
        check("the manifest reads all three as_of pins",
              m["as_of"] == {"3d-models": "1" * 40, "bikar": "2" * 40, "qiyas": "3" * 40})
        check("the manifest reads the deploy off the gh-pages tip",
              m["deploy"] and m["deploy"]["from_master"] == "c40dbc7", json.dumps(m["deploy"]))

        # Zero states: each absent source is null/empty, and the page shows the
        # true state rather than a fabricated one.
        (root / "build" / "bikar-ref.txt").unlink()
        (uc / "use-cases.md").unlink()
        subprocess.run(["git", "-C", tmp, "checkout", "-q", "master"], check=True, env=env)
        subprocess.run(["git", "-C", tmp, "branch", "-q", "-D", PAGES_BRANCH], check=True, env=env)
        m0 = build(root)
        check("no stamp is a null bikar_ref", m0["bikar_ref"] is None)
        check("no map is empty pins", m0["as_of"] == {})
        check("no gh-pages is a null deploy", m0["deploy"] is None)

        # And a not-a-repo directory is a null deploy, not a traceback.
        with tempfile.TemporaryDirectory(prefix="status-not-a-repo-") as bare:
            check("a non-repo root is a null deploy", deploy_from_git(Path(bare)) is None)

    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    m = build(ROOT)
    args.out.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ref = m["bikar_ref"]["short"] if m["bikar_ref"] else "no stamp"
    dep = m["deploy"]["date"] if m["deploy"] else "not deployed"
    where = args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out
    print(f"status-manifest: bikar {ref} · deploy {dep} · {len(m['as_of'])} pins → {where}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
