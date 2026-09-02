#!/usr/bin/env python3
"""Write `prints-manifest.json` — the register `prints.html` reads — from `docs/prints/`.

The prints page (bikar `packages/lab/prints.html`, vendored here by `make lab`)
shows one card per plate that came off a machine, and nothing else. It gets that
list from one file beside it, `prints-manifest.json`, and this script is the only
thing that writes that file: it walks `docs/prints/<run>/index.md`, parses each
record's YAML frontmatter with the same parser `prints_gate.py` gates it with,
and emits the frontmatter plus where the record and its photos are served from.

Nothing is typed. A record exists in the manifest exactly when its directory
exists on disk, and an empty `docs/prints/` — or no such directory at all, as on
the day this shipped — writes `{"records": []}`, which the page renders as
"nothing printed yet, and that is the true state". A manifest someone edits by
hand would be the failure the prints tab exists to prevent, so the file is
gitignored and `make deploy` rebuilds it.

Where things are served from: the site ships the manifest but not the record
directories — the photos are source binaries tracked on master, and the honest
place to read them is the repository. So each record carries `url` (the
directory on GitHub) and each photo `url` (the raw blob), and the page prefers
those to its `dir/file` fallback.

Usage:
  prints_manifest.py               write <repo>/prints-manifest.json
  prints_manifest.py --out PATH    write elsewhere (the Makefile does not)
  prints_manifest.py --self-test   build the gate's fixture and check the output
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / ".claude" / "gates" / "prints_gate.py"
OUT = ROOT / "prints-manifest.json"
REPO_BLOB = "https://github.com/omars-lab/3d-models/blob/master"
REPO_RAW = "https://raw.githubusercontent.com/omars-lab/3d-models/master"
SCHEMA = 1


def _gate():
    """The prints gate as a module — one frontmatter parser, not two."""
    spec = importlib.util.spec_from_file_location("prints_gate", GATE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def record(gate, rec_dir: Path, prints: Path) -> dict | None:
    """One manifest record from one `docs/prints/<run>/`, or None with a reason on stderr.

    A record the gate would refuse is not silently included: an unparseable
    frontmatter is skipped and named, so a broken record cannot appear on the
    page looking like a printed plate.
    """
    data, err = gate.parse_frontmatter((rec_dir / "index.md").read_text(encoding="utf-8"))
    if data is None:
        print(f"prints-manifest: skipping {rec_dir.name}: {err}", file=sys.stderr)
        return None
    rel = f"docs/prints/{rec_dir.name}"
    out = dict(data)
    out["run"] = data.get("run", rec_dir.name)
    out["dir"] = rel
    out["url"] = f"{REPO_BLOB}/{rel}"
    photos = []
    for p in data.get("photos") or []:
        if not isinstance(p, dict) or not p.get("file"):
            continue
        photos.append({**p, "url": f"{REPO_RAW}/{rel}/{p['file']}"})
    out["photos"] = photos
    return out


def build(prints: Path) -> dict:
    """The manifest for every record under `prints`, or the empty register."""
    gate = _gate()
    records: list[dict] = []
    if prints.is_dir():
        for rec_dir in gate.record_dirs(prints):
            r = record(gate, rec_dir, prints)
            if r is not None:
                records.append(r)
    return {
        "schema": SCHEMA,
        "generated": dt.date.today().isoformat(),
        "source": "docs/prints/<run>/index.md, via build/prints_manifest.py",
        "records": records,
    }


def self_test() -> int:
    """Build the gate's own fixture and assert the manifest says what the disk says."""
    import tempfile

    gate = _gate()
    failures = 0

    def check(label: str, ok: bool, why: str = "") -> None:
        nonlocal failures
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" — {why}"))

    with tempfile.TemporaryDirectory(prefix="prints-manifest-") as tmp:
        prints = gate._build_fixture(Path(tmp))
        m = build(prints)
        on_disk = sorted(d.name for d in gate.record_dirs(prints))
        in_manifest = sorted(r["run"] for r in m["records"])
        check("every record directory on disk is a record", in_manifest == on_disk,
              f"disk {on_disk}, manifest {in_manifest}")
        rec = m["records"][0]
        check("a record points at its directory on the repository",
              rec["url"] == f"{REPO_BLOB}/docs/prints/{rec['run']}", rec["url"])
        check("every photo points at its raw blob",
              all(p["url"].startswith(f"{REPO_RAW}/docs/prints/{rec['run']}/") for p in rec["photos"])
              and len(rec["photos"]) == len(gate.parse_frontmatter(
                  (prints / rec["run"] / "index.md").read_text())[0].get("photos") or []),
              json.dumps(rec["photos"]))
        # The by-design failure: a record the gate cannot parse must not
        # appear on the page as a printed plate.
        broken = prints / "2099-01-01-broken"
        broken.mkdir()
        (broken / "index.md").write_text("no frontmatter here\n")
        m2 = build(prints)
        check("a record with no frontmatter is skipped, not shown",
              "2099-01-01-broken" not in {r["run"] for r in m2["records"]}
              and len(m2["records"]) == len(m["records"]))
        # And the zero state is the honest one, not an error.
        m3 = build(Path(tmp) / "never-made")
        check("no docs/prints/ at all is an empty register", m3["records"] == [] and m3["schema"] == SCHEMA)

    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    m = build(ROOT / "docs" / "prints")
    args.out.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n = len(m["records"])
    where = "docs/prints/ is empty (nothing printed yet)" if n == 0 else f"from docs/prints/"
    print(f"prints-manifest: {n} record(s) — {where} → {args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
