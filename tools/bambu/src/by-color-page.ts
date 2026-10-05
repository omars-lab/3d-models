// The cost view as one page: the three routes side by side, then each route's plates, each drawn
// from its slice's top view (piece colors phase 2, infill-color-ux-design §6). Self-contained HTML
// (pictures inline), so it opens from build/ with no server. Nothing here reads a file.

import type { Costs, Route, RoutePlate } from "./by-color-costs.js";

/** Pictures by recipe name: the slice's top view as a data URI, one per bed. */
export type Pictures = Record<string, string[]>;

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const num = (n: number | null, unit: string, digits = 0) => (n === null ? "—" : `${n.toFixed(digits)}${unit}`);
const usd = (n: number | null) => (n === null ? "—" : `$${n.toFixed(2)}`);
const hm = (min: number | null) => {
  if (min === null) return "—";
  const h = Math.floor(min / 60);
  const m = Math.round(min - h * 60);
  return h ? `${h} h ${String(m).padStart(2, "0")} min` : `${m} min`;
};

function swatch(hex: string): string {
  return `<span class="sw" style="background:${esc(hex)}"></span>`;
}

function picture(p: RoutePlate, route: Route, pictures: Pictures, bed: number): string {
  const src = pictures[p.name]?.[bed];
  if (!src) return `<div class="bed empty">no slice picture</div>`;
  // One-color plates show the slice's own picture, drawn in its color. The whole set prints once
  // per color from one slice, so its picture is tinted with that print's color; the swapping plate
  // is drawn grey, since its picture has one color only.
  if (route.key === "per-color") return `<div class="bed"><img src="${src}" alt="${esc(p.name)} bed ${bed + 1}"></div>`;
  const tint = route.key === "whole-set" ? p.colors[0]!.hex : "#8a8f98";
  return `<div class="bed"><div class="mask" style="background:${esc(tint)};-webkit-mask-image:url(${src});mask-image:url(${src})"></div></div>`;
}

function plateCard(p: RoutePlate, route: Route, pictures: Pictures): string {
  const beds = p.bed_minutes ?? [null];
  const label = { slice: "from the slice", estimate: "estimate", none: "not sliced" }[p.source];
  const bedRows =
    p.bed_minutes && p.bed_minutes.length > 1
      ? `<ul class="beds">${p.bed_minutes.map((m, i) => `<li>bed ${i + 1}: ${hm(m)}</li>`).join("")}</ul>`
      : "";
  return `<article class="plate${p.sendable ? "" : " warn"}">
  <div class="pics">${beds.map((_, i) => picture(p, route, pictures, i)).join("")}</div>
  <h4>${p.colors.map((c) => swatch(c.hex)).join("")} ${esc(p.colors.map((c) => [c.name ?? c.hex, c.line].join(" · ")).join(" + "))}</h4>
  <p class="what">${esc(p.what.join(", "))}</p>
  <dl>
    <dt>time</dt><dd>${hm(p.minutes)}${p.swaps ? ` <small>(${hm(p.sliced_minutes)} sliced + ${p.swaps} swaps × 1.6 min)</small>` : ""}</dd>
    <dt>watched</dt><dd>${hm(p.watched_minutes)}</dd>
    <dt>filament</dt><dd>${num(p.grams, " g", 1)}</dd>
    <dt>cost</dt><dd>${usd(p.usd)}</dd>
  </dl>
  ${bedRows}
  <p class="src ${p.source}">${label}</p>
  ${p.notes.map((n) => `<p class="note">${esc(n)}</p>`).join("")}
</article>`;
}

function routeSection(r: Route, costs: Costs, pictures: Pictures): string {
  return `<section class="route${r.fits_rule ? "" : " dropped"}" id="${r.key}">
  <header><h3>${esc(r.title)}</h3><p class="status">${esc(r.status)}</p></header>
  <div class="totals">
    <div><b>${r.total.sends ?? "—"}</b><span>sends</span></div>
    <div><b>${hm(r.total.minutes)}</b><span>time</span></div>
    <div><b>${num(r.total.grams, " g", 1)}</b><span>filament</span></div>
    <div><b>${usd(r.total.usd)}</b><span>filament cost</span></div>
    <div><b>${hm(r.per_coaster.minutes)}</b><span>per coaster${costs.coasters > 1 ? ` (of ${costs.coasters})` : ""}</span></div>
    <div><b>${usd(r.per_coaster.usd)}</b><span>cost per coaster</span></div>
  </div>
  <p class="left">Left over: ${esc(r.left_over)}</p>
  <div class="plates">${r.plates.map((p) => plateCard(p, r, pictures)).join("")}</div>
  ${r.notes.map((n) => `<p class="note">${esc(n)}</p>`).join("")}
</section>`;
}

function compareTable(costs: Costs): string {
  const rows = costs.routes
    .map(
      (r) => `<tr${r.fits_rule ? "" : ` class="dropped"`}>
  <th><a href="#${r.key}">${esc(r.title)}</a><small>${esc(r.status)}</small></th>
  <td>${r.total.sends ?? "—"}</td><td>${r.total.swaps}</td><td>${hm(r.total.minutes)}</td><td>${hm(r.total.watched_minutes)}</td>
  <td>${num(r.total.grams, " g", 1)}</td><td>${usd(r.total.usd)}</td><td>${hm(r.per_coaster.minutes)}</td><td>${usd(r.per_coaster.usd)}</td>
  <td>${esc(r.left_over)}</td></tr>`,
    )
    .join("");
  return `<div class="scroll"><table>
<thead><tr><th>Way to print</th><th>Sends</th><th>Swaps</th><th>Time</th><th>Watched</th><th>Filament</th><th>Cost</th><th>Time per coaster</th><th>Cost per coaster</th><th>Left over</th></tr></thead>
<tbody>${rows}</tbody></table></div>`;
}

/** The whole page. `title` names the coloring, e.g. "gBV, pink and green on black". */
export function costsPage(costs: Costs, pictures: Pictures, title: string): string {
  const tierWords = { refill: "a refill bought on its own", spool: "a roll with spool", ten_refill: "a refill at the 10-roll tier", ten_spool: "a roll at the 10-roll tier" }[
    costs.prices.tier
  ];
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Coaster print costs</title>
<style>
:root{--bg:#faf8f4;--fg:#1d1c1a;--muted:#6b675f;--card:#fff;--line:#e4dfd5;--bed:#d8d2c4;--warn:#b5651d;--ok:#2f7d4f}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161514;--fg:#ece8e1;--muted:#a19b90;--card:#201f1d;--line:#34312d;--bed:#cfc8b8;--warn:#e0a060;--ok:#6cc08b}}
:root[data-theme="dark"]{--bg:#161514;--fg:#ece8e1;--muted:#a19b90;--card:#201f1d;--line:#34312d;--bed:#cfc8b8;--warn:#e0a060;--ok:#6cc08b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:24px;margin:0 0 4px}h2{font-size:18px;margin:28px 0 8px}h3{margin:0;font-size:17px}h4{margin:8px 0 2px;font-size:14px;font-weight:600}
.sub{color:var(--muted);margin:0 0 12px}.sw{display:inline-block;width:14px;height:14px;border-radius:3px;border:1px solid var(--line);vertical-align:-2px;margin-right:3px}
.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card)}
th,td{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left;white-space:nowrap}thead th{color:var(--muted);font-weight:600}
td:last-child{white-space:normal;min-width:140px}tbody th{white-space:normal;min-width:200px}tbody th small{display:block;color:var(--muted);font-weight:400;font-size:12px}tr.dropped{opacity:.6}a{color:inherit}
.route{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:16px 0}.route.dropped{opacity:.75}
.route header{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}.status{color:var(--muted);margin:0}
.totals{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin:12px 0}
.totals div{border:1px solid var(--line);border-radius:8px;padding:8px}.totals b{display:block;font-size:17px}.totals span{color:var(--muted);font-size:12px}
.left{margin:0 0 10px;color:var(--muted)}
.plates{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.plate{border:1px solid var(--line);border-radius:8px;padding:10px}.plate.warn{border-color:var(--warn)}
.pics{display:flex;gap:6px}.bed{flex:1;aspect-ratio:1;background:var(--bed);border-radius:6px;overflow:hidden;display:flex;align-items:center;justify-content:center}
.bed img{width:100%;height:100%;object-fit:contain}.bed .mask{width:100%;height:100%;-webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-position:center;mask-position:center}
.bed.empty{color:#555;font-size:12px}
.what{margin:0 0 6px;color:var(--muted);font-size:13px}
dl{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;margin:0;font-size:14px}dt{color:var(--muted)}dd{margin:0}
.beds{margin:6px 0 0;padding-left:18px;font-size:13px}
.src{font-size:12px;margin:6px 0 0;font-weight:600}.src.slice{color:var(--ok)}.src.estimate,.src.none{color:var(--warn)}
.note{font-size:12px;color:var(--muted);margin:4px 0 0}
</style></head><body><main>
<h1>${esc(title)}</h1>
<p class="sub">${costs.colors.map((c) => `${swatch(c.hex)}${esc(c.name ?? c.hex)}`).join(" &nbsp; ")} · ${costs.coasters} coaster${costs.coasters === 1 ? "" : "s"} · filament priced as ${esc(tierWords)}, store prices read ${esc(costs.prices.read)}</p>
<h2>Three ways to print it</h2>
${compareTable(costs)}
<p class="note">Time is the slicer's, which includes each plate's warm-up. Watched is that time corrected by past prints of the same filament, where there are any. Cost is filament only: no power, wear or failed prints.</p>
${costs.routes.map((r) => routeSection(r, costs, pictures)).join("")}
${costs.notes.length ? `<h2>Notes</h2>${costs.notes.map((n) => `<p class="note">${esc(n)}</p>`).join("")}` : ""}
</main></body></html>
`;
}
