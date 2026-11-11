#!/usr/bin/env python3
"""Open the hub's judging page, with comments on, at the first question Omar still owes.

Omar, 2026-10-29: "open the hub plate page with comments on pieces i need to answer questions
about" — then "this shoudl be part of our skills". Doing it by hand took three steps that each
fail quietly: find which plates still have unanswered rows, start the comments server (it is
not always running), and open the right row. This script does all three.

    open_questions.py              list plates with open rows, open the first one's first open row
    open_questions.py <plate>      open that plate's first open row
    open_questions.py --list       list only, open nothing
    open_questions.py --link       print the link with comments on, open nothing

The comments address is read from the hub's own settings (`.page-comments/config.json`), never
written here: this script said 8766 for a week after the hub had moved to 8768.

A row counts as answered when the plate page's `## Judged` table has it, or when the hub holds
a saved answer for it that is not sent yet.
"""

import argparse
import json
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

HUB = "http://127.0.0.1:4717"
HUB_CHECKOUT = pathlib.Path.home() / "Workspace/git/3d-model-hub"
COMMENTS_CONFIG = HUB_CHECKOUT / ".page-comments/config.json"


def comments_base(config=COMMENTS_CONFIG):
    """The comments server's address, from the port the hub's settings give it."""
    try:
        port = json.loads(config.read_text())["serve"]["port"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        sys.exit(f"cannot read the comments port from {config}: {e!r}")
    if not isinstance(port, int):
        sys.exit(f"{config}: serve.port is {port!r}, not a number")
    return f"http://127.0.0.1:{port}"


def get_json(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)


def up(url):
    try:
        with urllib.request.urlopen(url, timeout=3):
            return True
    except (urllib.error.URLError, OSError):
        return False


def answered_rows(data):
    """Row numbers with an answer, from the Judged table or the hub's saved answers."""
    rows = set()
    for a in data["sheet"].get("answers") or []:
        if isinstance(a, dict) and a.get("row") is not None:
            rows.add(int(a["row"]))
    for p in data.get("pending") or []:
        if p.get("row") is not None:
            rows.add(int(p["row"]))
    return rows


def open_rows(plate):
    data = get_json(f"{HUB}/api/judge/{plate}")
    done = answered_rows(data)
    return [r for r in data["sheet"]["rows"] if int(r["row"]) not in done]


def ensure_comments():
    """Start the hub's comments server when it is down; return the base to open."""
    comments = comments_base()
    if up(f"{comments}/judge.html"):
        return comments
    # The hub's own state folder, so the hub checkout stays untouched.
    log = pathlib.Path.home() / "Library/Application Support/3d-model-hub/comments-serve.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a") as out:
        subprocess.Popen(["make", "-s", "-C", str(HUB_CHECKOUT), "comments"],
                         stdout=out, stderr=out, start_new_session=True)
    for _ in range(15):
        time.sleep(1)
        if up(f"{comments}/judge.html"):
            return comments
    print(f"comments server did not start (log: {log}); opening the page without comments")
    return HUB


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("plate", nargs="?", help="open this plate; default the first with open rows")
    ap.add_argument("--list", action="store_true", help="list plates with open rows, open nothing")
    ap.add_argument("--link", action="store_true",
                    help="print the link with comments on (starting them if needed), open nothing")
    args = ap.parse_args()

    if not up(f"{HUB}/judge.html"):
        sys.exit(f"the hub is not running at {HUB}; start it in {HUB_CHECKOUT}")

    plates = [p["plate"] for p in get_json(f"{HUB}/api/judge")["plates"]]
    owed = {}
    for plate in plates:
        rows = open_rows(plate)
        if rows:
            owed[plate] = rows
            print(f"{plate}: {len(rows)} open — rows {', '.join(str(r['row']) for r in rows)}")
    if not owed:
        print("no plate on the hub has an open question")
        return
    if args.list:
        return

    plate = args.plate or next(iter(owed))
    if plate not in owed:
        sys.exit(f"{plate}: no open question on the hub (plates with one: {', '.join(owed)})")
    base = ensure_comments()
    url = f"{base}/judge.html#{plate}/{owed[plate][0]['row']}"
    if args.link:
        print(url)
        return
    subprocess.run(["open", url], check=True)
    print(f"opened {url}" + ("  (press C to comment on a piece)" if base != HUB else ""))


if __name__ == "__main__":
    main()
