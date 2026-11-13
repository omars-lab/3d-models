#!/usr/bin/env python3
"""Count the broken links on the local sites Omar opens on this Mac.

Omar, 2026-11-13: "lots of the links on pressing cant be reached ... do we have a hook to go
through and see how many broken links we have at session end". None of the existing checks opened
a running page: the docs gate and hooks 35 and 40 read files. This one opens the pages.

Sites (each a host and port on 127.0.0.1):

- ``studio``  7136, the always-on Studio app (bikar ``make app-serve``). Its pages draw
  themselves in the browser, so each page is loaded in headless Chrome and read after its scripts
  ran. A print page whose data does not answer says "The print data can't be reached from here";
  that page counts as broken even though it loaded.
- ``hub``     4717, the Print Hub. Loaded in headless Chrome the same way.
- ``judging`` 8768, the comment server in front of the hub, where Omar's judging links point.
  Checked with plain GETs only, never in a browser: its comment bar writes a thread's
  found-or-lost state back to the repo when a page loads, and a crawler must not do that.

Only GETs are sent. Pages are loaded, never clicked; every write on these pages sits behind a
button (checked 2026-11-13 in 3d-model-hub ``web/src/judge.ts`` and ``web/src/main.ts``).

What counts as broken:
- ``status``: the page answered 4xx or 5xx, or the connection failed;
- ``unreachable``: the page loaded but shows the "can't be reached" sentence;
- ``down-site``: a link on a running site into one of the sites above that is not running
  (that site's own pages are not counted one by one: it is reported once as not running).

Modes:
- default: print a plain report, exit 1 when something is broken, 2 when nothing could be checked;
- ``--session-start``: the SessionStart hook. Prints nothing when every site runs and is clean,
  one quiet line when a site is only not running, and the count with an instruction to ask Omar
  only when a running site has a broken page;
- ``--stop``: the Stop hook. Reads the hook's JSON on stdin and runs only when the session edited
  a page file (bikar ``packages/web`` or ``packages/lab``, the hub's ``web/``) since the last time
  it ran; then blocks the stop once with the count when a running site has a broken page.
- ``--self-test``: checks the link and transcript readers against fixtures.

Every run logs ``ev=`` lines to ``--log`` (default ``$TMPDIR/local-links/run.log``).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html.parser
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

SITES = {
    "studio": {"port": 7136, "render": True, "start": ["/"]},
    "hub": {"port": 4717, "render": True, "start": ["/"]},
    "judging": {"port": 8768, "render": False, "start": ["/", "/judge.html"]},
}
# The sentence bikar's print pages show when /api/print does not answer
# (bikar packages/web/src/print/api.ts, UNREACHABLE_TEXT). Matched on its first words, so a
# rewording of the second half still counts.
UNREACHABLE = "can't be reached from here"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOCAL_HOSTS = {"127.0.0.1", "localhost"}
PAGE_FILES = re.compile(r"/(bikar[^/]*/packages/(web|lab)/|3d-model-hub[^/]*/web/)")


def log(path: Path, event: str, **kv: object) -> None:
    """One greppable line: UTC time, pid, ev=, then key=value (free text quoted)."""
    parts = [time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), f"pid={os.getpid()}", f"ev={event}"]
    for k, v in kv.items():
        s = str(v)
        parts.append(f'{k}="{s}"' if (" " in s or not s) else f"{k}={s}")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(" ".join(parts) + "\n")
    except OSError:
        pass


class Links(html.parser.HTMLParser):
    """Every <a href> in a page."""

    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):  # noqa: ANN001
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.hrefs.append(v)


def links_in(page_url: str, text: str) -> list[str]:
    """The local http links a page holds, resolved, with the hash kept (Studio pages route on it)."""
    p = Links()
    try:
        p.feed(text)
    except Exception:  # noqa: BLE001 - a malformed page still gives the links read so far
        pass
    out = []
    for href in p.hrefs:
        if href.startswith(("mailto:", "javascript:", "tel:")):
            continue
        url = urllib.parse.urljoin(page_url, href)
        u = urllib.parse.urlsplit(url)
        if u.scheme not in ("http", "https") or u.hostname not in LOCAL_HOSTS:
            continue
        if u.path == urllib.parse.urlsplit(page_url).path and u.query == "" and href.startswith("#") and not u.fragment.startswith("/"):
            continue  # an in-page jump such as #brim
        out.append(url)
    return out


def site_of(url: str) -> str | None:
    port = urllib.parse.urlsplit(url).port
    for name, s in SITES.items():
        if s["port"] == port:
            return name
    return None


def get(url: str, timeout: float) -> tuple[int | None, str, str]:
    """(status, content type, body) for a GET; status None when the connection failed."""
    plain = urllib.parse.urlsplit(url)._replace(fragment="").geturl()
    req = urllib.request.Request(plain, method="GET", headers={"User-Agent": "local-links-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(2_000_000).decode("utf-8", "replace")
            return r.status, r.headers.get("content-type", ""), body
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("content-type", "") if e.headers else "", ""
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        return None, "", str(getattr(e, "reason", e))


def render(url: str, timeout: float, logpath: Path) -> str | None:
    """The page's DOM after its scripts ran, from headless Chrome; None when Chrome failed."""
    profile = tempfile.mkdtemp(prefix="local-links-")
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           f"--user-data-dir={profile}", "--virtual-time-budget=5000", "--dump-dom", url]
    log(logpath, "render_start", url=url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        log(logpath, "render_end", url=url, bytes=len(r.stdout))
        return r.stdout
    except subprocess.TimeoutExpired:
        log(logpath, "render_timeout", url=url)
        return None
    finally:
        shutil.rmtree(profile, ignore_errors=True)


@dataclass
class Finding:
    kind: str  # status | unreachable | down-site
    url: str
    found_on: str
    detail: str = ""


@dataclass
class Report:
    running: dict = field(default_factory=dict)  # site -> bool
    pages: dict = field(default_factory=dict)  # site -> pages checked
    findings: list = field(default_factory=list)
    capped: bool = False
    no_chrome: bool = False

    @property
    def broken(self) -> int:
        return len(self.findings)


class Crawl:
    """One run over the sites: which are running, then every page reachable from their front pages."""

    def __init__(self, sites: list[str], max_pages: int, timeout: float, logpath: Path) -> None:
        self.sites, self.max_pages, self.timeout, self.logpath = sites, max_pages, timeout, logpath
        self.rep = Report(no_chrome=not Path(CHROME).exists())
        self.seen: set[str] = set()
        self.queue: list[tuple[str, str]] = []  # (url, found_on)
        self.down_links: set[str] = set()
        self.other_checked: set[str] = set()
        self.per_site: dict[str, int] = {}

    def broken(self, f: Finding) -> None:
        self.rep.findings.append(f)
        log(self.logpath, "broken", kind=f.kind, url=f.url, on=f.found_on, detail=f.detail)

    def probe(self) -> None:
        """Which sites answer at all; queue the front pages of those that do."""
        for name in self.sites:
            port = SITES[name]["port"]
            status, _, why = get(f"http://127.0.0.1:{port}/", self.timeout)
            self.rep.running[name] = status is not None
            log(self.logpath, "site", site=name, running=int(status is not None), status=status or "none",
                why=why if status is None else "")
            if status is not None:
                self.queue.extend((f"http://127.0.0.1:{port}{p}", "(start)") for p in SITES[name]["start"])

    def visit(self, item: tuple[str, str]) -> tuple[str, list[Finding], list[str]]:
        """Load one page: its findings and the local links it holds."""
        url, found_on = item
        name = site_of(url)
        status, ctype, body = get(url, self.timeout)
        if status is None or status >= 400:
            return url, [Finding("status", url, found_on, str(status) if status else body[:80])], []
        if "html" not in ctype:
            return url, [], []
        text = body
        if name and SITES[name]["render"] and not self.rep.no_chrome:
            text = render(url, self.timeout + 10, self.logpath) or body
        found = [Finding("unreachable", url, found_on, "the page says its data can't be reached")] \
            if UNREACHABLE in text else []
        return url, found, links_in(url, text)

    def next_batch(self) -> list[tuple[str, str]]:
        """Every queued page not yet seen, within each site's page limit."""
        batch = []
        while self.queue:
            url, on = self.queue.pop(0)
            if url in self.seen:
                continue
            name = site_of(url) or "other"
            if self.per_site.get(name, 0) >= self.max_pages:
                self.rep.capped = True  # this site hit its page limit; the others go on
                continue
            self.per_site[name] = self.per_site.get(name, 0) + 1
            self.seen.add(url)
            batch.append((url, on))
        return batch

    def other_port(self, link: str, on: str) -> None:
        """A link to some other local server: checked once, for status only."""
        key = urllib.parse.urlsplit(link)._replace(fragment="").geturl()
        if key in self.other_checked:
            return
        self.other_checked.add(key)
        st, _, why = get(link, self.timeout)
        if st is None or st >= 400:
            self.broken(Finding("status", link, on, str(st) if st else why[:80]))

    def follow(self, link: str, on: str) -> None:
        target = site_of(link)
        if target is None:
            self.other_port(link, on)
        elif target not in self.sites:
            return  # a site this run was told to leave alone
        elif not self.rep.running.get(target, True):
            if link not in self.down_links:
                self.down_links.add(link)
                self.broken(Finding("down-site", link, on, f"{target} is not running"))
        elif link not in self.seen:
            self.queue.append((link, on))

    def run(self, workers: int) -> Report:
        self.probe()
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            while batch := self.next_batch():
                for url, found, links in pool.map(self.visit, batch):
                    name = site_of(url) or "other"
                    self.rep.pages[name] = self.rep.pages.get(name, 0) + 1
                    for f in found:
                        self.broken(f)
                    for link in links:
                        self.follow(link, url)
        rep = self.rep
        log(self.logpath, "done", pages=sum(rep.pages.values()), broken=rep.broken, capped=int(rep.capped),
            not_running=",".join(n for n, r in rep.running.items() if not r) or "none")
        return rep


def check(sites: list[str], max_pages: int, timeout: float, workers: int, logpath: Path) -> Report:
    return Crawl(sites, max_pages, timeout, logpath).run(workers)


SITE_WORDS = {
    "studio": "the Studio app on 7136 (bikar `make app-serve`)",
    "hub": "the Print Hub on 4717",
    "judging": "the judging pages on 8768 (the comment server in front of the Print Hub)",
}
KIND_WORDS = {
    "status": "does not load",
    "unreachable": "loads but says its data can't be reached",
    "down-site": "points at a site that is not running",
}


def plain(rep: Report, limit: int = 15) -> str:
    lines = []
    down = [n for n, r in rep.running.items() if not r]
    for n in down:
        lines.append(f"Not running: {SITE_WORDS[n]}. Its pages were not checked.")
    checked = ", ".join(f"{n} {c}" for n, c in rep.pages.items()) or "none"
    lines.append(f"Pages checked: {checked}{' (stopped at the page limit)' if rep.capped else ''}.")
    if rep.no_chrome:
        lines.append("Chrome was not found, so pages were read without running their scripts.")
    by_kind: dict[str, list[Finding]] = {}
    for f in rep.findings:
        by_kind.setdefault(f.kind, []).append(f)
    lines.append(f"Broken links: {rep.broken}.")
    for kind, fs in by_kind.items():
        lines.append(f"- {len(fs)} {KIND_WORDS[kind]}:")
        for f in fs[:limit]:
            extra = f" ({f.detail})" if f.detail and kind == "status" else ""
            lines.append(f"    {f.url}{extra}, linked from {f.found_on}")
        if len(fs) > limit:
            lines.append(f"    … and {len(fs) - limit} more")
    return "\n".join(lines)


def edited_pages_since(transcript: Path, after_line: int) -> tuple[bool, int]:
    """Whether an Edit/Write/NotebookEdit after line ``after_line`` touched a page file; and the line count."""
    hit = False
    n = 0
    try:
        with transcript.open(encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if n <= after_line or '"tool_use"' not in line:
                    continue
                try:
                    msg = json.loads(line).get("message", {})
                except json.JSONDecodeError:
                    continue
                for part in msg.get("content", []) if isinstance(msg.get("content"), list) else []:
                    if part.get("type") != "tool_use" or part.get("name") not in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                        continue
                    path = str((part.get("input") or {}).get("file_path", ""))
                    if PAGE_FILES.search(path):
                        hit = True
    except OSError:
        return False, after_line
    return hit, n


def self_test() -> int:
    page = '<a href="/plates">x</a><a href="#brim">y</a><a href="/plate#/split-10">z</a>' \
           '<a href="https://github.com/a">g</a><a href="http://127.0.0.1:7136/judge">s</a>'
    got = links_in("http://127.0.0.1:4717/words", page)
    want = ["http://127.0.0.1:4717/plates", "http://127.0.0.1:4717/plate#/split-10", "http://127.0.0.1:7136/judge"]
    assert got == want, got
    assert site_of("http://127.0.0.1:7136/judge#a/1") == "studio"
    assert site_of("http://127.0.0.1:9999/") is None
    with tempfile.TemporaryDirectory() as d:
        t = Path(d) / "t.jsonl"
        edit = {"message": {"content": [{"type": "tool_use", "name": "Edit",
                                         "input": {"file_path": "/x/bikar-else/packages/web/src/print/api.ts"}}]}}
        other = {"message": {"content": [{"type": "tool_use", "name": "Edit",
                                          "input": {"file_path": "/x/3d-models/docs/a.md"}}]}}
        t.write_text(json.dumps(other) + "\n" + json.dumps(edit) + "\n" + json.dumps(other) + "\n")
        assert edited_pages_since(t, 0) == (True, 3)
        assert edited_pages_since(t, 2) == (False, 3)
    # A down Studio alone: one quiet line, no question.
    down = Report(running={"studio": False, "hub": True, "judging": True},
                  findings=[Finding("down-site", "http://127.0.0.1:7136/judge", "http://127.0.0.1:4717/")])
    text = session_start_text(down)
    assert text.startswith("[local-links] Not running") and "AskUserQuestion" not in text, text
    # A broken page on a running site still asks, even with the Studio down.
    bad = Report(running=dict(down.running), findings=down.findings +
                 [Finding("status", "http://127.0.0.1:4717/x", "http://127.0.0.1:4717/", "404")])
    assert "AskUserQuestion" in session_start_text(bad)
    # Every site up and clean: silent.
    assert session_start_text(Report(running={"studio": True, "hub": True, "judging": True})) == ""
    # The Stop hook: a down site alone is a note, a broken page blocks, all clean is silent.
    assert '"decision"' not in stop_text(down) and "systemMessage" in stop_text(down)
    assert '"decision": "block"' in stop_text(bad)
    assert stop_text(Report(running={"studio": True, "hub": True, "judging": True})) == ""
    print("local_links self-test: ok")
    return 0


def state_file(session: str) -> Path:
    return Path(tempfile.gettempdir()) / "local-links" / f"stop-{re.sub(r'[^A-Za-z0-9_-]', '_', session)}.json"


FULL_LIST = "python3 .claude/skills/check-local-links/scripts/local_links.py"


def stop_hook(a: argparse.Namespace, sites: list[str]) -> int:
    """The Stop hook: check only when the session edited page files since the last stop."""
    try:
        hook = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        hook = {}
    if hook.get("stop_hook_active"):
        return 0
    sf = state_file(str(hook.get("session_id") or "unknown"))
    try:
        last = json.loads(sf.read_text()).get("line", 0)
    except (OSError, json.JSONDecodeError):
        last = 0
    edited, lines = edited_pages_since(Path(str(hook.get("transcript_path") or "")), last)
    sf.parent.mkdir(parents=True, exist_ok=True)
    sf.write_text(json.dumps({"line": lines}))
    if not edited:
        return 0
    rep = check(sites, a.max_pages, a.timeout, a.workers, a.log)
    text = stop_text(rep)
    if text:
        print(text)
    return 0


def stop_text(rep: Report) -> str:
    """What the Stop hook prints after a page edit: a block only for a broken page on a running
    site, a one-line note when a site is down, nothing when every site runs and is clean."""
    if not any(rep.running.values()):
        return json.dumps({"systemMessage": "local-links: no local site was running, so the pages this "
                           "session changed were not checked."})
    if real_broken(rep):
        return json.dumps({"decision": "block", "reason":
                           "[local-links] This session changed page files, and the local pages are not "
                           f"all working:\n{plain(rep, 8)}\n"
                           "Fix the ones this session caused before handing back, or say in your closing "
                           f"message which remain and why (full list: {FULL_LIST})."})
    if down_line(rep):
        return json.dumps({"systemMessage": down_line(rep).replace("so not checked", "so the pages "
                           "this session changed there were not checked")})
    return ""


def real_broken(rep: Report) -> list[Finding]:
    """Broken pages on a running site. A site that is only not running is not one: that is a fact about
    this Mac (the always-on Studio waits on bikar #374), and asking about it every session is noise."""
    return [f for f in rep.findings if f.kind != "down-site"]


def down_line(rep: Report) -> str:
    down = [SITE_WORDS[n] for n, r in rep.running.items() if not r]
    return f"[local-links] Not running, so not checked: {'; '.join(down)}." if down else ""


def session_start_text(rep: Report) -> str:
    """What the SessionStart hook prints: nothing when clean, one quiet line per down site, and a
    question for Omar only when a running site has broken pages."""
    if not any(rep.running.values()):
        return ("[local-links] Could not check the local pages: none of the Studio (7136), the Print Hub "
                "(4717) or the judging pages (8768) is running.")
    if real_broken(rep):
        return ("[local-links] The local pages Omar opens have problems right now:\n" + plain(rep, 8) +
                "\nBefore other work, ask Omar with AskUserQuestion whether to fix these this session or "
                "not this session. Give each option what it costs and what stays broken. Full list: "
                + FULL_LIST)
    return down_line(rep)


def session_start(rep: Report) -> int:
    text = session_start_text(rep)
    if text:
        print(text)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--sites", default=",".join(SITES), help="comma list of: " + ", ".join(SITES))
    ap.add_argument("--max-pages", type=int, default=300, help="page limit for each site")
    ap.add_argument("--timeout", type=float, default=5.0, help="seconds per GET")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--log", type=Path, default=Path(tempfile.gettempdir()) / "local-links" / "run.log")
    ap.add_argument("--json", action="store_true")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--session-start", action="store_true")
    mode.add_argument("--stop", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    sites = [s.strip() for s in a.sites.split(",") if s.strip() in SITES]
    if a.self_test:
        return self_test()
    if a.stop:
        return stop_hook(a, sites)
    rep = check(sites, a.max_pages, a.timeout, a.workers, a.log)
    if a.session_start:
        return session_start(rep)
    if a.json:
        print(json.dumps({"running": rep.running, "pages": rep.pages, "capped": rep.capped,
                          "broken": rep.broken, "findings": [f.__dict__ for f in rep.findings]}, indent=1))
    else:
        print(plain(rep))
    if not any(rep.running.values()):
        return 2
    return 1 if rep.broken else 0


if __name__ == "__main__":
    sys.exit(main())
