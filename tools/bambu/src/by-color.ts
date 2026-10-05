// One plate recipe per color: the writer `bambu plates by-color` and `bambu order plan` share.
//
// A loose coaster prints as a frame plus groups of pieces, and each group prints under its palette
// name (`--piece Kite`). The piece-color design (infill-color-ux-design §4.5) puts every group of one
// color on one plate, so a color is one spool and one send; the order design (order-driven-lab-design
// §8, "one recipe writer") feeds the same writer with the pieces of a whole order. This file is that
// writer, and nothing in it reads a file or runs a program: the commands pass in the .bkr text and
// what `bikar bands` says about it.
//
// What it refuses, until piece colors phase 5 (#188) proves picking one piece at a time: a `fill` or
// `loose` rule chosen by anything but `orbit == <n>`, and any `index` in one. Per group is what the
// piece-color design's call 2 leans to and what `--piece` can render today.

import { canonicalJson } from "./iteration.js";
import { recipeHash } from "./recipe-hash.js";

/** What a pieces .bkr says about its colors: palette hexes and which orbits print loose. */
export interface PiecesBkr {
  hexes: Record<string, string>; // palette name → #rrggbb (lowercase)
  fills: Record<number, string>; // orbit → palette name, from `fill … where orbit == n color Name`
  looseOrbits: number[];
}

/** One orbit as `bikar bands --json` reports it. */
export interface BandsOrbit {
  orbit: number;
  members: number;
  color?: string | null; // the palette name its faces fill with
}

/** A group of pieces: what one `--piece <name>` item renders, and how many pieces that is. */
export interface PieceGroup {
  piece: string;
  orbits: number[];
  members: number;
  hex: string | null; // the .bkr palette's own color for the group
}

const ORBIT_RULE = /\bwhere\s+orbit\s*==\s*(\d+)(?=\s|$)/;

/** Read a pieces .bkr's palette and loose rules. Throws on a rule this phase cannot plan. */
export function readPiecesBkr(text: string): PiecesBkr {
  const hexes: Record<string, string> = {};
  const fills: Record<number, string> = {};
  const looseOrbits: number[] = [];
  text.split("\n").forEach((raw, i) => {
    const line = raw.replace(/#(?![0-9a-fA-F]{6}\b).*$/, "").trim(); // drop a comment, keep a #hex
    const where = `line ${i + 1}`;
    const pal = /^([A-Za-z_]\w*)\s*=\s*(#[0-9a-fA-F]{6})$/.exec(line);
    if (pal) {
      hexes[pal[1]!] = pal[2]!.toLowerCase();
      return;
    }
    const verb = /^(fill|loose)\b/.exec(line)?.[1];
    if (!verb) return;
    if (/\bindex\b/.test(line)) {
      throw new Error(`${where}: \`${verb}\` picks by \`index\`; one piece at a time is piece colors phase 5, not yet planned: ${line}`);
    }
    const m = ORBIT_RULE.exec(line);
    if (!m) {
      throw new Error(`${where}: \`${verb}\` is chosen by something other than \`orbit == <n>\`; only whole orbits are planned: ${line}`);
    }
    const orbit = Number(m[1]);
    if (verb === "loose") {
      looseOrbits.push(orbit);
    } else {
      const color = /\bcolor\s+([A-Za-z_]\w*)\b/.exec(line);
      if (color) fills[orbit] = color[1]!;
    }
  });
  return { hexes, fills, looseOrbits };
}

/** The groups of loose pieces, in orbit order: palette name, orbits and piece count, from the .bkr and
 *  what bands reports. Throws when the two disagree about an orbit's name, or bands lacks a loose orbit. */
export function pieceGroups(bkr: PiecesBkr, bands: BandsOrbit[]): PieceGroup[] {
  const byName = new Map<string, PieceGroup>();
  for (const orbit of [...bkr.looseOrbits].sort((a, b) => a - b)) {
    const band = bands.find((b) => b.orbit === orbit);
    if (!band) throw new Error(`loose orbit ${orbit}: bands reports no such orbit`);
    const name = band.color ?? bkr.fills[orbit];
    if (!name) throw new Error(`loose orbit ${orbit}: no palette name fills it, so no \`--piece\` renders it`);
    if (bkr.fills[orbit] && bkr.fills[orbit] !== name) {
      throw new Error(`loose orbit ${orbit}: the .bkr fills it as ${bkr.fills[orbit]}, bands says ${name}`);
    }
    const g = byName.get(name) ?? { piece: name, orbits: [], members: 0, hex: bkr.hexes[name] ?? null };
    g.orbits.push(orbit);
    g.members += band.members;
    byName.set(name, g);
  }
  return [...byName.values()];
}

/** A color as a plate is keyed by: a catalog spool (line and code) for an order, a hex for by-color. */
export interface PlateColor {
  key: string; // what makes two plates one: `<line>|<code>`, or the lowercase hex
  hex: string; // #RRGGBB, the recipe's profile.color
  line: string; // the filament line, which picks the filament preset
  code: string | null;
  name: string | null;
  note: string | null; // the palette's store note (e.g. "not on the US store")
}

/** What one construction asks for in one color. `piece` null is the frame, the coaster itself. */
export interface Demand {
  construction: string; // "bikar:<path>"
  params: Record<string, number>;
  piece: string | null;
  count: number;
  rank: number; // the order items sit in on a plate: frame -1, then the group's first orbit
  color: PlateColor;
}

export interface PlateItem {
  construction: string;
  params: Record<string, number>;
  piece: string | null;
  count: number;
  rank: number;
}

export interface ColorPlate {
  color: PlateColor;
  items: PlateItem[];
}

/** Group demands by color, one plate per color in the order colors first appear, merging items that
 *  render the same thing (construction, params, piece) by adding their counts. Items sit by
 *  construction (first seen first), then frame before pieces, then orbit. */
export function groupByColor(demands: Demand[]): ColorPlate[] {
  const plates = new Map<string, ColorPlate>();
  const firstSeen = new Map<string, number>();
  for (const d of demands) {
    if (!firstSeen.has(d.construction)) firstSeen.set(d.construction, firstSeen.size);
    const plate = plates.get(d.color.key) ?? { color: d.color, items: [] };
    plates.set(d.color.key, plate);
    const same = plate.items.find(
      (it) => it.construction === d.construction && it.piece === d.piece && canonicalJson(it.params) === canonicalJson(d.params),
    );
    if (same) same.count += d.count;
    else plate.items.push({ construction: d.construction, params: d.params, piece: d.piece, count: d.count, rank: d.rank });
  }
  for (const p of plates.values()) {
    p.items.sort(
      (a, b) =>
        firstSeen.get(a.construction)! - firstSeen.get(b.construction)! ||
        a.rank - b.rank ||
        canonicalJson(a.params).localeCompare(canonicalJson(b.params)),
    );
  }
  return [...plates.values()];
}

/** A construction's short name for a label: the file stem up to its first `-` or `_` (gBV, GimTvN9hw4U). */
export function constructionStem(construction: string): string {
  const base = construction.replace(/^bikar:/, "").split("/").pop()!.replace(/\.bkr$/, "");
  return base.split(/[-_]/)[0]!;
}

/** One label per item, unique on the plate: the piece's name in capitals, COASTER for a frame, the
 *  construction's stem in front when two constructions share the plate, and a number when two items
 *  would still read the same. */
export function itemLabels(items: PlateItem[]): string[] {
  const many = new Set(items.map((i) => i.construction)).size > 1;
  const seen = new Map<string, number>();
  return items.map((it) => {
    const base = it.piece ? it.piece.toUpperCase() : "COASTER";
    const label = many ? `${constructionStem(it.construction).toUpperCase()} ${base}` : base;
    const n = (seen.get(label) ?? 0) + 1;
    seen.set(label, n);
    return n === 1 ? label : `${label} ${n}`;
  });
}

/** The profile every plate this writer makes slices with: the X2D's 0.4 nozzle at 0.20 mm. */
export const PLATE_SETTINGS = "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D";

/** The filament preset for a line: `Bambu PLA Matte @BBL X2D 0.4 nozzle`. */
export function filamentPreset(line: string): string {
  return `Bambu ${line} @BBL X2D 0.4 nozzle`;
}

export interface RecipeOpts {
  name: string;
  about: string[]; // header lines under the title, each without the leading "# "
  pieceCount: (it: PlateItem) => number | null; // how many pieces one item renders, for the header
}

/** The recipe YAML for one color plate, in the format compose.ts reads (sheets-04g's shape). */
export function recipeText(plate: ColorPlate, opts: RecipeOpts): string {
  const c = plate.color;
  const what = [c.line, c.name, c.code ? `(${c.code})` : null, c.hex].filter(Boolean).join(" ");
  const labels = itemLabels(plate.items);
  const width = Math.max(...labels.map((l) => l.length));
  const lines = [`# ${opts.name} — every piece in ${what}`, "#", ...opts.about.map((l) => (l ? `# ${l}` : "#")), "#"];
  plate.items.forEach((it, i) => {
    const n = opts.pieceCount(it);
    const each = it.piece ? `${it.piece} pieces of ${constructionStem(it.construction)}` : `the ${constructionStem(it.construction)} coaster`;
    const total = n === null ? `${it.count}×` : `${it.count * n}`;
    lines.push(`#   ${labels[i]!.padEnd(width)}  ${each} (${total})`);
  });
  if (c.note) lines.push("#", `# ${c.code ?? c.hex}: ${c.note}`);
  lines.push(
    "",
    "bed: x2d",
    "profile:",
    `  settings: ${JSON.stringify(PLATE_SETTINGS)}`,
    `  filament: ${JSON.stringify(filamentPreset(c.line))}`,
    `  color:    ${JSON.stringify(c.hex.toUpperCase())}`,
    "",
    "items:",
  );
  plate.items.forEach((it, i) => {
    lines.push(`  - bkr:    ${it.construction}`);
    if (it.piece) lines.push(`    piece:  ${it.piece}`);
    const params = Object.entries(it.params).map(([k, v]) => `${k}: ${v}`);
    if (params.length > 0) lines.push(`    params: { ${params.join(", ")} }`);
    if (it.count !== 1) lines.push(`    count:  ${it.count}`);
    lines.push(`    label:  ${labels[i]}`);
  });
  return lines.join("\n") + "\n";
}

export interface WrittenRecipe {
  name: string;
  plate: ColorPlate;
  text: string;
  hash: string;
}

/** Write each plate's recipe text and hash it, naming each `<prefix>-<code or hex>`. */
export function writeRecipes(plates: ColorPlate[], prefix: string, about: string[], pieceCount: RecipeOpts["pieceCount"]): WrittenRecipe[] {
  const names = new Set<string>();
  return plates.map((plate) => {
    const tag = (plate.color.code ?? plate.color.hex.replace(/^#/, "")).toLowerCase();
    let name = `${prefix}-${tag}`;
    if (names.has(name)) name = `${prefix}-${slug(plate.color.line)}-${tag}`;
    names.add(name);
    const text = recipeText(plate, { name, about, pieceCount });
    const hash = recipeHash(text);
    if (!hash) throw new Error(`${name}: the recipe written is not YAML`); // cannot happen; a bug if it does
    return { name, plate, text, hash };
  });
}

export function slug(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

/** A hex as a plate's color: #rrggbb, alpha dropped, lowercase. Null when it is not one. */
export function normalHex(hex: string): string | null {
  const m = /^#?([0-9a-fA-F]{6})(?:[0-9a-fA-F]{2})?$/.exec(hex.trim());
  return m ? `#${m[1]!.toLowerCase()}` : null;
}
