#!/usr/bin/env python3
"""The price page: what a coaster costs at each size, what each price earns, who would buy at it,
and in their own (made-up) words why; plus real orders on top once there are any.

The cost and margin come from the pricer (`bambu order price --json --sweep`), so the page and the
CLI can never disagree. The buyers come from a sweep in buyers.yaml (`buyers.py`). The best price is
the one where the simulated buy share times the margin is highest: what one shopper is worth at
that price, on average. It is a picture of made-up buyers, not a forecast.

Real orders, once there are any, go in a gitignored file (default `.bambu/pricing/sales.yaml`):

    sales:
      - { date: 2026-11-02, price_each: 10, coasters: 4, outcome: bought }    # or declined

and the page draws, at each price tried, the share of real offers that sold, beside the simulated
share. The output carries the private settings' numbers, so it goes to the gitignored
`.bambu/pricing/` by default.

Usage:
    price_page.py --plan <plan.json> --buyers <construction>/<theme> [--settings <f>] [--sales <f>] [--out <html>]
    price_page.py --self-test
"""
from __future__ import annotations

import argparse
import html
import json
import math
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import buyers as by  # noqa: E402

ROOT = by.ROOT
BAMBU = ROOT / "tools" / "bambu" / "bin" / "bambu"
SALES = ROOT / ".bambu" / "pricing" / "sales.yaml"
OUT = ROOT / ".bambu" / "pricing"
QUANTITIES = [1, 5, 10, 100]  # D-104, call 13: "1 peice, 5 pieces, 10, 100"


# ---- the sums -------------------------------------------------------------------------------

def expected(curve: dict, sweep_rows: list[dict]) -> list[dict]:
    """Per price tried: the simulated share, the margin each, and what one shopper is worth there
    (share × margin), or None where the margin is empty."""
    margin = {float(r["price_each"]): r["margin_each"] for r in sweep_rows}
    out = []
    for r in curve["by_price"]:
        p = float(r["price_each"])
        m = margin.get(p)
        out.append({"price_each": p, "share": r["share"], "margin_each": m,
                    "per_shopper": None if m is None else round(r["share"] * m, 4)})
    return out


def best(rows: list[dict]) -> dict | None:
    """The price where one shopper is worth the most; on a tie, the lower price (more buyers).
    None when no margin is known, or none is above zero: there is no best price to mark."""
    known = [r for r in rows if r["per_shopper"] is not None and r["per_shopper"] > 0]
    if not known:
        return None
    return max(known, key=lambda r: (r["per_shopper"], -r["price_each"]))


def real_share(sales: list[dict], prices: list[float]) -> dict[float, dict]:
    """At each price tried, the real offers seen at that price and the share that sold."""
    out = {}
    for p in prices:
        at = [s for s in sales if float(s["price_each"]) == float(p)]
        if at:
            sold = sum(1 for s in at if s["outcome"] == "bought")
            out[float(p)] = {"offers": len(at), "bought": sold, "share": round(sold / len(at), 4)}
    return out


def read_sales(path: Path) -> tuple[list[dict], bool]:
    """The offers, and whether the file says they are a made-up example (`example: true`)."""
    if not path.exists():
        return [], False
    data = yaml.safe_load(path.read_text()) or {}
    rows = data.get("sales") or []
    for i, r in enumerate(rows):
        if r.get("outcome") not in ("bought", "declined"):
            raise SystemExit(f"{path}: sale {i + 1}: outcome must be bought or declined, not {r.get('outcome')!r}")
        if not isinstance(r.get("price_each"), (int, float)):
            raise SystemExit(f"{path}: sale {i + 1}: price_each must be a number")
    return rows, data.get("example") is True


def price(plan: Path, settings: Path | None, prices: list[float]) -> dict:
    cmd = [str(BAMBU), "order", "price", str(plan), "--json",
           "--quantities", ",".join(str(q) for q in QUANTITIES),
           "--sweep", ",".join(f"{p:g}" for p in prices)]
    if settings:
        cmd += ["--settings", str(settings)]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if done.returncode != 0:
        raise SystemExit(f"bambu order price failed:\n{done.stderr or done.stdout}")
    return json.loads(done.stdout)


# ---- drawing --------------------------------------------------------------------------------

W, H, PAD_L, PAD_R, PAD_T, PAD_B = 640, 250, 56, 16, 16, 40


def esc(s) -> str:
    return html.escape(str(s))


def money(v) -> str:
    return "—" if v is None else (f"-${-v:,.2f}" if v < 0 else f"${v:,.2f}")


class Axes:
    """A plot box: x by position (0..n-1, labeled) or by value, y by value."""

    def __init__(self, xs: list[float], ys: list[float], xlabels: list[str], ylabel: str, by_index=False):
        self.by_index = by_index
        self.xs = xs
        self.xlabels = xlabels
        lo, hi = min(ys + [0]), max(ys + [0])
        if hi == lo:
            hi = lo + 1
        # Ticks on a round step (1, 2 or 5 times a power of ten), the range widened to whole steps.
        raw = (hi - lo) / 4
        mag = 10 ** math.floor(math.log10(raw))
        self.step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
        self.ylo = math.floor(lo / self.step) * self.step
        self.yhi = math.ceil(hi / self.step) * self.step
        self.ylabel = ylabel
        # By index, each label gets a slot and sits in its middle, so a bar never covers the y labels.
        self.xmin, self.xmax = (-0.5, len(xs) - 0.5) if by_index else (min(xs), max(xs))

    def x(self, i_or_v: float) -> float:
        span = (self.xmax - self.xmin) or 1
        return PAD_L + (i_or_v - self.xmin) / span * (W - PAD_L - PAD_R)

    def y(self, v: float) -> float:
        return PAD_T + (self.yhi - v) / (self.yhi - self.ylo) * (H - PAD_T - PAD_B)

    def frame(self, yfmt=lambda v: f"-${-v:g}" if v < 0 else f"${v:g}") -> str:
        parts = []
        k = 0
        while self.ylo + k * self.step <= self.yhi + 1e-9:
            v = self.ylo + k * self.step
            k += 1
            yy = self.y(v)
            parts.append(f'<line class="grid" x1="{PAD_L}" x2="{W - PAD_R}" y1="{yy:.1f}" y2="{yy:.1f}"/>'
                         f'<text class="tick" x="{PAD_L - 6}" y="{yy + 4:.1f}" text-anchor="end">{esc(yfmt(round(v, 2)))}</text>')
        for i, (xv, lab) in enumerate(zip(self.xs, self.xlabels)):
            xx = self.x(i if self.by_index else xv)
            parts.append(f'<text class="tick" x="{xx:.1f}" y="{H - PAD_B + 16}" text-anchor="middle">{esc(lab)}</text>')
        if self.ylo < 0 < self.yhi:
            parts.append(f'<line class="zero" x1="{PAD_L}" x2="{W - PAD_R}" y1="{self.y(0):.1f}" y2="{self.y(0):.1f}"/>')
        return "".join(parts)


def svg(body: str, title: str) -> str:
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}" '
            f'preserveAspectRatio="xMidYMid meet">{body}</svg>')


def polyline(points: list[tuple[float, float]], cls: str) -> str:
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    dots = "".join(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="3.5"/>' for x, y in points)
    return f'<polyline class="{cls}" fill="none" points="{pts}"/>{dots}'


def chart_cost(report: dict) -> str:
    rows = [r for r in report["by_quantity"] if r["coasters"] in QUANTITIES]
    labels = [f"{r['coasters']}" for r in rows]
    series = {k: [r["each"][k]["value"] for r in rows] for k in ("cost", "break_even", "suggested")}
    band = [b for b in report["market_band"]["each"]]
    band_vals = [v for b in band for v in (b.get("median"), b.get("low"), b.get("high")) if v is not None]
    ys = [v for vs in series.values() for v in vs if v is not None] + band_vals
    if not ys:
        return '<p class="empty">No cost yet: the settings leave every amount empty.</p>'
    ax = Axes(list(range(len(rows))), ys, labels, "each", by_index=True)
    body = ax.frame()
    lo = min(band_vals) if band_vals else None
    hi = max(band_vals) if band_vals else None
    if lo is not None:
        body += (f'<rect class="band" x="{PAD_L}" width="{W - PAD_L - PAD_R}" y="{ax.y(hi):.1f}" '
                 f'height="{max(ax.y(lo) - ax.y(hi), 2):.1f}"/>')
    band_text = (f'market band: others ask {money(lo)} to {money(hi)} each' if lo is not None
                 else 'market band: none read')
    for k, cls in (("cost", "s1"), ("break_even", "s2"), ("suggested", "s3")):
        pts = [(ax.x(i), ax.y(v)) for i, v in enumerate(series[k]) if v is not None]
        body += polyline(pts, cls)
    body += f'<text class="tick" x="{W / 2}" y="{H - 6}" text-anchor="middle">coasters in the order</text>'
    legend = ('<p class="legend"><span class="k s1"></span>cost each <span class="k s2"></span>break-even each '
              '<span class="k s3"></span>cost-plus price each <span class="k band"></span>'
              f'{band_text}</p>')
    return svg(body, "cost each by order size") + legend


def chart_margin(rows: list[dict]) -> str:
    known = [r for r in rows if r["margin_each"] is not None]
    if not known:
        return '<p class="empty">No margin yet: the settings leave the cost empty.</p>'
    xs = [r["price_each"] for r in rows]
    ax = Axes(xs, [r["margin_each"] for r in known], [f"${p:g}" for p in xs], "margin")
    body = ax.frame() + polyline([(ax.x(r["price_each"]), ax.y(r["margin_each"])) for r in known], "s2")
    body += f'<text class="tick" x="{W / 2}" y="{H - 6}" text-anchor="middle">price a coaster</text>'
    return svg(body, "margin each by price") + '<p class="legend"><span class="k s2"></span>margin each, after fees and cost</p>'


def chart_verdicts(curve: dict, real: dict, example: bool = False) -> str:
    rows = curve["by_price"]
    n = curve["buyers"]
    xs = [r["price_each"] for r in rows]
    ax = Axes(list(range(len(rows))), [0, n], [f"${p:g}" for p in xs], "buyers", by_index=True)
    body = ax.frame(yfmt=lambda v: f"{v:g}")
    bw = (W - PAD_L - PAD_R) / len(rows) * 0.62
    for i, r in enumerate(rows):
        base = 0
        for v in ("buy", "maybe", "too-cheap", "walk"):
            c = r["counts"][v]
            if c:
                y0, y1 = ax.y(base + c), ax.y(base)
                body += (f'<rect class="v-{v}" x="{ax.x(i) - bw / 2:.1f}" y="{y0:.1f}" width="{bw:.1f}" '
                         f'height="{y1 - y0:.1f}"><title>{c} {v} at ${r["price_each"]:g}</title></rect>')
                base += c
        rs = real.get(float(r["price_each"]))
        if rs:
            yy = ax.y(rs["share"] * n)
            body += (f'<circle class="real" cx="{ax.x(i):.1f}" cy="{yy:.1f}" r="6">'
                     f'<title>real: {rs["bought"]} of {rs["offers"]} bought</title></circle>')
    body += f'<text class="tick" x="{W / 2}" y="{H - 6}" text-anchor="middle">price a coaster</text>'
    legend = ('<p class="legend"><span class="k v-buy"></span>buy <span class="k v-maybe"></span>maybe '
              '<span class="k v-too-cheap"></span>too cheap <span class="k v-walk"></span>walk'
              + (f' <span class="k real"></span>{"example offers (made up)" if example else "real orders"}: '
                 'share that bought, scaled to the buyers' if real else '')
              + '</p>')
    return svg(body, "simulated verdicts by price") + legend


def chart_expected(rows: list[dict], top: dict | None, n: int) -> str:
    known = [r for r in rows if r["per_shopper"] is not None]
    if not known:
        return '<p class="empty">No best price: the margin is empty, so what a shopper is worth cannot be worked.</p>'
    xs = [r["price_each"] for r in rows]
    ax = Axes(xs, [r["per_shopper"] * n for r in known], [f"${p:g}" for p in xs], "per shoppers")
    body = ax.frame() + polyline([(ax.x(r["price_each"]), ax.y(r["per_shopper"] * n)) for r in known], "s3")
    if top:
        xx, yy = ax.x(top["price_each"]), ax.y(top["per_shopper"] * n)
        body += (f'<line class="best" x1="{xx:.1f}" x2="{xx:.1f}" y1="{PAD_T}" y2="{H - PAD_B}"/>'
                 f'<text class="bestlabel" x="{xx + 6:.1f}" y="{yy - 8:.1f}">best: ${top["price_each"]:g}</text>')
    body += f'<text class="tick" x="{W / 2}" y="{H - 6}" text-anchor="middle">price a coaster</text>'
    return svg(body, "expected margin per shoppers") + (
        f'<p class="legend"><span class="k s3"></span>margin earned from {n} shoppers, one coaster each '
        f'(buy share × margin × {n})</p>')


def thoughts_grid(sweep: dict) -> str:
    prices = sweep["prices"]
    head = "".join(f"<th>${p:g}</th>" for p in prices)
    body = []
    for bid, cells in sweep["buyers"].items():
        tds = []
        for p in prices:
            c = cells[by.price_key(cells, p)]
            tds.append(f'<td class="v-{c["verdict"]}-cell"><b>{esc(c["verdict"])}</b> {esc(c["thought"])}</td>')
        body.append(f"<tr><th class='who'>{esc(bid)}</th>{''.join(tds)}</tr>")
    return (f'<div class="gridwrap"><table class="thoughts"><thead><tr><th></th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


CSS = """
:root{--bg:#fbfaf7;--fg:#1d2330;--muted:#5f6878;--line:#d9dde4;--s1:#4a6fa5;--s2:#1f8a70;--s3:#c0703a;
--band:rgba(120,140,170,.18);--buy:#2f8f5b;--maybe:#d8a93b;--walk:#b9bfc9;--cheap:#8b6bb8;--real:#c2364b;
--buy-bg:#e3f2e8;--maybe-bg:#fbf1d6;--walk-bg:#eef0f3;--cheap-bg:#ece5f6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14171d;--fg:#e6e9ef;--muted:#9aa3b2;
--line:#2c323d;--band:rgba(150,170,200,.16);--walk:#5b6270;--buy-bg:#1d3326;--maybe-bg:#3a3220;--walk-bg:#22262e;--cheap-bg:#2c2440}}
:root[data-theme="dark"]{--bg:#14171d;--fg:#e6e9ef;--muted:#9aa3b2;--line:#2c323d;--band:rgba(150,170,200,.16);
--walk:#5b6270;--buy-bg:#1d3326;--maybe-bg:#3a3220;--walk-bg:#22262e;--cheap-bg:#2c2440}
body{background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,system-ui,sans-serif;margin:0;padding:24px 16px}
main{max-width:980px;margin:0 auto}h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 6px}
.sub,.legend,.note{color:var(--muted);font-size:13px}.banner{border:1px solid var(--line);border-left:4px solid var(--real);
padding:8px 12px;margin:12px 0;font-size:14px}.cards{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0}
.card{border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:150px}.card b{display:block;font-size:20px}
svg{width:100%;height:auto;display:block}.grid{stroke:var(--line)}.zero{stroke:var(--fg);stroke-width:1.2}
.tick{fill:var(--muted);font-size:11px}polyline{stroke-width:2.2}polyline.s1,circle.s1{stroke:var(--s1);fill:var(--s1)}
polyline.s2,circle.s2{stroke:var(--s2);fill:var(--s2)}polyline.s3,circle.s3{stroke:var(--s3);fill:var(--s3)}
polyline{fill:none!important}rect.band{fill:var(--band)}.bandlabel{fill:var(--muted);font-size:11px}
.v-buy{fill:var(--buy);background:var(--buy)}.v-maybe{fill:var(--maybe);background:var(--maybe)}
.v-walk{fill:var(--walk);background:var(--walk)}.v-too-cheap{fill:var(--cheap);background:var(--cheap)}
circle.real{fill:none;stroke:var(--real);stroke-width:2.5}.k.real{border:2px solid var(--real);border-radius:50%;background:none}
.best{stroke:var(--s3);stroke-dasharray:4 3}.bestlabel{fill:var(--s3);font-size:12px;font-weight:600}
.k{display:inline-block;width:12px;height:12px;border-radius:2px;margin:0 4px 0 10px;vertical-align:-1px}
.k.s1{background:var(--s1)}.k.s2{background:var(--s2)}.k.s3{background:var(--s3)}.k.band{background:var(--band)}
.gridwrap{overflow-x:auto}table.thoughts{border-collapse:collapse;font-size:12px;min-width:900px}
.thoughts th,.thoughts td{border:1px solid var(--line);padding:6px;vertical-align:top;text-align:left}
.thoughts td{width:10%}.who{white-space:nowrap}.v-buy-cell{background:var(--buy-bg)}.v-maybe-cell{background:var(--maybe-bg)}
.v-walk-cell{background:var(--walk-bg);color:var(--muted)}.v-too-cheap-cell{background:var(--cheap-bg)}
.empty{color:var(--muted);font-style:italic}
"""


def page(report: dict, sweep: dict, curve: dict, rows: list[dict], top: dict | None, sales: list[dict],
         real: dict, cid: str, example_sales: bool = False) -> str:
    n = curve["buyers"]
    plan_each = report["price"]["each"]
    cards = [("cost each, this order", money(plan_each["cost"]["value"])),
             ("break-even each", money(plan_each["break_even"]["value"])),
             ("best simulated price", f"${top['price_each']:g}" if top else "—"),
             ("buy share there", f"{top['share']:.0%}" if top else "—")]
    floor = " The amounts are floors: no timed print corrects some plate's minutes yet." if report["price"]["floor"] else ""
    real_line = (f"The {len(sales)} offers drawn as circles are a MADE-UP EXAMPLE, to show where real orders "
                 f"will go; they are not sales." if sales and example_sales else
                 f"{len(sales)} real offers read, at {len(real)} of the prices tried. Where they disagree with "
                 f"the made-up buyers, believe the orders." if sales else
                 "No real orders yet. When there are, add them to the sales file and the circles appear on the "
                 "verdict chart; the made-up buyers are the guess until then.")
    turns = "".join(
        f"<li><b>{esc(b)}</b>: buys up to {money(t['buys_up_to'])}, hesitates up to {money(t['warm_up_to'])}, "
        f"walks from {money(t['walks_from'])}" + (f", too cheap below {money(t['too_cheap_below'])}" if t['too_cheap_below'] else "")
        + "</li>" for b, t in curve["turns"].items())
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Price check</title><style>{CSS}</style></head>
<body><main>
<h1>Price check: {esc(cid)} {esc(sweep['theme'])}</h1>
<p class="sub">Order {esc(report['order'])}, {report['price']['coasters']} coasters. Settings: {esc(Path(report['settings']).name)}.{esc(floor)}</p>
<p class="banner"><b>Simulated buyers, not customer research.</b> The verdicts and thoughts are Claude imagining six
made-up buyers looking at the picture; nobody was asked. A maybe counts as half a buyer, a made-up weight. {esc(real_line)}</p>
<p class="sub">Shown: {esc(sweep['shown'])}</p>
<div class="cards">{''.join(f'<div class="card"><span class="sub">{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in cards)}</div>

<h2>What one coaster costs, by order size</h2>
{chart_cost(report)}
<h2>What each price earns</h2>
{chart_margin(rows)}
<h2>Who would buy at each price</h2>
{chart_verdicts(curve, real, example_sales)}
<ul class="note">{turns}</ul>
<h2>Where the price earns the most</h2>
{chart_expected(rows, top, n)}
<p class="note">{esc(sweep['overall'])}</p>
<h2>What they thought</h2>
{thoughts_grid(sweep)}
</main></body></html>
"""


# ---- self-test ------------------------------------------------------------------------------

def self_test() -> int:
    fails = []

    def expect(cond, what):
        if not cond:
            fails.append(what)

    curve = {"buyers": 2, "by_price": [{"price_each": 5, "share": 1.0}, {"price_each": 10, "share": 0.5},
                                       {"price_each": 20, "share": 0.25}]}
    sweep_rows = [{"price_each": 5, "margin_each": 1}, {"price_each": 10, "margin_each": 6},
                  {"price_each": 20, "margin_each": 12}]
    rows = expected(curve, sweep_rows)
    expect([r["per_shopper"] for r in rows] == [1.0, 3.0, 3.0], f"per shopper: {[r['per_shopper'] for r in rows]}")
    top = best(rows)
    expect(top is not None and top["price_each"] == 10, f"a tie goes to the lower price: {top}")
    # The by-design case: no margin known, so no best price, rather than a best price of $0.
    empty = expected(curve, [{**r, "margin_each": None} for r in sweep_rows])
    expect(best(empty) is None, "an empty margin still gave a best price")
    expect(best(expected(curve, [{**r, "margin_each": -1} for r in sweep_rows])) is None,
           "every price losing money still gave a best price")
    sales = [{"price_each": 10, "outcome": "bought"}, {"price_each": 10, "outcome": "declined"},
             {"price_each": 20, "outcome": "declined"}, {"price_each": 7, "outcome": "bought"}]
    rs = real_share(sales, [5, 10, 20])
    expect(rs == {10.0: {"offers": 2, "bought": 1, "share": 0.5}, 20.0: {"offers": 1, "bought": 0, "share": 0.0}},
           f"real share: {rs}")
    # The shipped example file must say it is an example, so its circles are never read as sales.
    ex, is_example = read_sales(HERE.parent / "example-sales.yaml")
    expect(ex and is_example, "example-sales.yaml is not marked example: true")
    expect(read_sales(HERE / "no-such-sales.yaml") == ([], False), "a missing sales file is not empty")
    for f in fails:
        print(f"self-test FAIL: {f}")
    print("self-test: ok" if not fails else f"self-test: {len(fails)} failed")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--plan", type=Path, help="a plan.json from `bambu order plan`")
    ap.add_argument("--buyers", help="<construction>/<theme>, a sweep in that construction's buyers.yaml")
    ap.add_argument("--settings", type=Path, help="pricing settings (default: the pricer's own default)")
    ap.add_argument("--sales", type=Path, default=SALES, help=f"real offers and orders (default: {SALES.relative_to(ROOT)})")
    ap.add_argument("--out", type=Path, help="the HTML to write (default: .bambu/pricing/<construction>-<theme>.html)")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.plan or not a.buyers or "/" not in a.buyers:
        ap.error("--plan and --buyers <construction>/<theme> are needed")
    cid, tid = a.buyers.split("/", 1)
    sweep = by.find_sweep(cid, tid)
    curve = by.curve(sweep)
    report = price(a.plan, a.settings, [float(p) for p in sweep["prices"]])
    rows = expected(curve, report["sweep"])
    top = best(rows)
    sales, example_sales = read_sales(a.sales)
    real = real_share(sales, [float(p) for p in sweep["prices"]])
    out = a.out or OUT / f"{cid}-{tid}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(report, sweep, curve, rows, top, sales, real, cid, example_sales))
    print(f"wrote {out}")
    print(f"best simulated price: {'$%g' % top['price_each'] if top else 'none (no margin above zero)'}"
          f"; {len(sales)} {'example' if example_sales else 'real'} offers read")
    return 0


if __name__ == "__main__":
    sys.exit(main())
