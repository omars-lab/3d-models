// The picture of a COLOUR plate. `slice coaster` cannot slice with pictures headless (`--export-3mf`
// hangs — docs/issues/coaster-3mf-filament-shape-and-export-hang.md), so Studio never draws one. bikar's
// top-down SVG of each coaster fills every region with its palette hex — the same hex the parts sidecar
// carries and the AMS slot map reports — so rasterising it shows the regions in their slot colours
// without opening the GUI. It is a drawing of each distinct coaster, not of the bed layout.

import { readFileSync } from "node:fs";
import { runWithTimeout } from "./log.js";
import type { CoasterPartsSidecar } from "./ams.js";

/** Every fill/stroke colour an SVG paints with, lower-cased (`none` and url() paints left out). */
export function svgColours(svg: string): Set<string> {
  const out = new Set<string>();
  for (const m of svg.matchAll(/\b(?:fill|stroke)\s*[=:]\s*"?\s*(#[0-9a-fA-F]{3,8})\b/g)) out.add(m[1]!.toLowerCase());
  return out;
}

/** The sidecar colours the drawing does NOT paint. Empty means every region appears in its slot colour;
 *  anything listed is a region the picture would hide or show in the wrong colour. */
export function missingRegionColours(svg: string, parts: CoasterPartsSidecar["parts"]): string[] {
  const painted = svgColours(svg);
  const missing: string[] = [];
  for (const p of parts) {
    if (!p.hex) continue; // a region with no palette colour prints in the plate default — nothing to match
    if (!painted.has(p.hex.toLowerCase())) missing.push(`${p.region} (${p.paletteName ?? "?"} ${p.hex})`);
  }
  return missing;
}

/** The bikar CLI args that draw the SAME recipe `--format parts` rendered (same source, piece, params). */
export function svgRenderArgs(
  bikarCli: string,
  source: string,
  piece: string | undefined,
  params: Record<string, string | number>,
  outFile: string,
): string[] {
  const args = [bikarCli, "render", source, "--format", "svg", "-o", outFile];
  if (piece) args.push("--piece", piece);
  for (const [k, v] of Object.entries(params)) args.push("--param", `${k}=${v}`);
  return args;
}

/** Rasterise each SVG (rsvg-convert) and lay them side by side (magick +append) into `out`. */
export async function composeColourPreview(svgs: string[], out: string, width = 480): Promise<void> {
  if (svgs.length === 0) throw new Error("no coaster drawings to compose");
  const pngs: string[] = [];
  for (const svg of svgs) {
    const png = svg.replace(/\.svg$/i, "") + ".png";
    const r = await runWithTimeout("rsvg-convert", ["-w", String(width), "-b", "white", "-o", png, svg], {
      timeoutMs: 60_000,
      label: "rsvg_convert",
    });
    if (r.code !== 0 || r.timedOut) throw new Error(`rsvg-convert failed on ${svg}: ${(r.stderr || "").trim()}`);
    pngs.push(png);
  }
  const r = await runWithTimeout("magick", [...pngs, "+append", out], { timeoutMs: 60_000, label: "magick_append" });
  if (r.code !== 0 || r.timedOut) throw new Error(`magick +append failed: ${(r.stderr || "").trim()}`);
}

/** Read an SVG from disk and check it against a sidecar (the IO half of `missingRegionColours`). */
export function checkDrawing(svgPath: string, parts: CoasterPartsSidecar["parts"]): string[] {
  return missingRegionColours(readFileSync(svgPath, "utf8"), parts);
}
