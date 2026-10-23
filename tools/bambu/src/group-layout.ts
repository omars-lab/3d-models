// Lay a plate out by group: each group's pieces in a block of their own, the blocks side by side.
//
// `--arrange` packs pieces wherever they fit, so on split-03 the three sets' kites and stars sat
// mixed together and nobody could tell which piece belonged to which set (Omar, 2026-10-22: "unclear
// in split 3 which pieces is for what, can we group related pieces into a rectangle and organize the
// rectangles"). A plate whose items name a `group:` is placed here instead: the groups left to right
// in the order the plate first names them, each group's pieces packed in rows inside its column,
// nothing turned. Studio still arranges first (its first slice gives the plate a nozzle list); the
// placements here then overwrite where each object sits, and the second slice prints it as it lies.

export interface LayoutPiece {
  name: string; // the object's name in the plate (`stagedName`), shared by an item's `count` copies
  group: string;
  w: number; // footprint width (mm), as rendered: nothing is turned
  h: number; // footprint depth (mm)
}

export interface PlacedPiece extends LayoutPiece {
  x: number; // centre, bed millimetres from the front-left corner
  y: number;
}

export interface GroupBlock {
  group: string;
  x0: number;
  y0: number;
  x1: number;
  y1: number;
}

export interface GroupLayout {
  pieces: PlacedPiece[];
  blocks: GroupBlock[];
}

/** 6 mm between pieces inside a block: a guess, room for a label on the bed picture. Not measured. */
export const GROUP_GAP_MM = 6;
/** 14 mm between blocks, more than between pieces, so the eye splits the sets on the bed and the
 *  boxes on the bed picture (drawn 3 mm out) do not touch: at 6 mm, split-04's three boxes met. */
export const BLOCK_GAP_MM = 14;

/**
 * Place every piece: one column per group, `blockGap` apart, as wide as the bed allows; inside a
 * column, pieces in rows, tallest first, left to right, a new row when the next would not fit. The
 * columns are centred on the bed together. PURE. Throws naming the group when a piece is wider than
 * its column or a column is deeper than the bed, since a plate that does not fit must not be sliced.
 */
export function layoutGroups(
  pieces: LayoutPiece[],
  bed: { x: number; y: number },
  gap = GROUP_GAP_MM,
  blockGap = BLOCK_GAP_MM,
): GroupLayout {
  const groups: string[] = [];
  for (const p of pieces) if (!groups.includes(p.group)) groups.push(p.group);
  const colW = (bed.x - 2 * gap - blockGap * (groups.length - 1)) / groups.length;
  const columns = groups.map((g) => packColumn(pieces.filter((p) => p.group === g), colW, gap, g));
  const tallest = Math.max(...columns.map((c) => c.h));
  if (tallest > bed.y - 2 * gap) {
    const g = groups[columns.findIndex((c) => c.h === tallest)];
    throw new Error(`group "${g}" needs ${tallest.toFixed(1)} mm of depth; the bed has ${(bed.y - 2 * gap).toFixed(1)} inside its margins`);
  }
  const usedW = columns.reduce((s, c) => s + c.w, 0) + blockGap * (groups.length - 1);
  let left = (bed.x - usedW) / 2;
  const top = (bed.y - tallest) / 2;
  const placed: PlacedPiece[] = [];
  const blocks: GroupBlock[] = [];
  columns.forEach((c, i) => {
    for (const p of c.pieces) placed.push({ ...p, x: p.x + left, y: p.y + top });
    blocks.push({ group: groups[i]!, x0: left, y0: top, x1: left + c.w, y1: top + c.h });
    left += c.w + blockGap;
  });
  const clash = overlaps(placed, gap / 2);
  if (clash) throw new Error(`the group layout puts ${clash[0]} and ${clash[1]} on top of each other`);
  return { pieces: placed, blocks };
}

/** One group's pieces in rows inside a column `maxW` wide, from (0, 0). */
function packColumn(pieces: LayoutPiece[], maxW: number, gap: number, group: string): { pieces: PlacedPiece[]; w: number; h: number } {
  const order = [...pieces].sort((a, b) => b.h - a.h || b.w - a.w);
  const out: PlacedPiece[] = [];
  let x = 0;
  let y = 0;
  let rowH = 0;
  let w = 0;
  for (const p of order) {
    if (p.w > maxW) throw new Error(`group "${group}": ${p.name} is ${p.w.toFixed(1)} mm wide; a column holds ${maxW.toFixed(1)} mm`);
    if (x > 0 && x + p.w > maxW) {
      y += rowH + gap;
      x = 0;
      rowH = 0;
    }
    out.push({ ...p, x: x + p.w / 2, y: y + p.h / 2 });
    x += p.w + gap;
    rowH = Math.max(rowH, p.h);
    w = Math.max(w, x - gap);
  }
  return { pieces: out, w, h: y + rowH };
}

/** The first two pieces whose footprints come closer than `clear`, or null. */
export function overlaps(pieces: PlacedPiece[], clear: number): [string, string] | null {
  for (let i = 0; i < pieces.length; i++) {
    for (let j = i + 1; j < pieces.length; j++) {
      const a = pieces[i]!;
      const b = pieces[j]!;
      if (Math.abs(a.x - b.x) < (a.w + b.w) / 2 + clear && Math.abs(a.y - b.y) < (a.h + b.h) / 2 + clear) return [a.name, b.name];
    }
  }
  return null;
}

/**
 * Where each build object's footprint centre sits in its own frame, from its mesh. Studio wraps each
 * piece in an object whose `<component>` points at a mesh file and offsets it, and the offset is not
 * the mesh's centre: on split-04 the upper halves sat 31 mm from the lower ones under the same item
 * translation, and the first slice refused the plate for the two overlapping. So the centre is
 * measured: every vertex through its component's transform, the middle of the x and y range.
 * `meshes` maps a component's `p:path` (as written, leading slash and all) to that file's XML. PURE.
 */
export function footprintCentres(modelXml: string, meshes: Map<string, string>): Map<string, { cx: number; cy: number }> {
  const out = new Map<string, { cx: number; cy: number }>();
  for (const obj of modelXml.match(/<object\s+id="[^"]*"[^>]*>[\s\S]*?<\/object>/g) ?? []) {
    const id = obj.match(/<object\s+id="([^"]*)"/)?.[1];
    const comps = obj.match(/<component\b[^>]*>/g) ?? [];
    if (id === undefined || comps.length === 0) continue;
    let [x0, x1, y0, y1] = [Infinity, -Infinity, Infinity, -Infinity];
    for (const c of comps) {
      const path = c.match(/\bp:path="([^"]*)"/)?.[1];
      const mesh = path === undefined ? undefined : meshes.get(path);
      if (mesh === undefined) throw new Error(`object ${id}: no mesh file for its component ${path ?? "(no path)"}`);
      const t = (c.match(/\btransform="([^"]*)"/)?.[1] ?? "1 0 0 0 1 0 0 0 1 0 0 0").trim().split(/\s+/).map(Number);
      for (const v of mesh.matchAll(/<vertex\s+x="([^"]*)"\s+y="([^"]*)"\s+z="([^"]*)"/g)) {
        const [x, y, z] = [Number(v[1]), Number(v[2]), Number(v[3])];
        // 3MF row-vector order: x' = x·m00 + y·m10 + z·m20 + tx
        const px = x * t[0]! + y * t[3]! + z * t[6]! + t[9]!;
        const py = x * t[1]! + y * t[4]! + z * t[7]! + t[10]!;
        [x0, x1, y0, y1] = [Math.min(x0, px), Math.max(x1, px), Math.min(y0, py), Math.max(y1, py)];
      }
    }
    if (x0 === Infinity) throw new Error(`object ${id}: its mesh has no vertices`);
    out.set(id, { cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 });
  }
  return out;
}

/**
 * Move each object of a plate's `3D/3dmodel.model` to its place: the `<build>` items, matched to
 * objects by name through `Metadata/model_settings.config`, take the layout's centre in order (an
 * item's `count` copies share a name and take its places in turn), unturned, at the height Studio
 * gave them. `centres` (from `footprintCentres`) says where each object's footprint centre sits in
 * its own frame, so the item is shifted by that much; absent, the object's origin is taken as its
 * centre. PURE. Throws when an object has no place or a place has no object, so a plate is never
 * sliced half laid out.
 */
export function writePlacements(
  modelXml: string,
  settingsXml: string,
  placed: PlacedPiece[],
  centres: Map<string, { cx: number; cy: number }> = new Map(),
): string {
  const names = new Map<string, string>();
  for (const block of settingsXml.match(/<object\s+id="[^"]*">[\s\S]*?<\/object>/g) ?? []) {
    const id = block.match(/<object\s+id="([^"]*)"/)?.[1];
    const name = block.match(/<metadata\s+key="name"\s+value="([^"]*)"/)?.[1];
    if (id !== undefined && name !== undefined) names.set(id, name);
  }
  const waiting = new Map<string, PlacedPiece[]>();
  for (const p of placed) waiting.set(p.name, [...(waiting.get(p.name) ?? []), p]);
  const unplaced: string[] = [];
  const build = modelXml.match(/<build\b[\s\S]*?<\/build>/)?.[0];
  if (!build) throw new Error("the arranged plate has no <build>");
  const moved = build.replace(/<item\b[^>]*>/g, (tag) => {
    const id = tag.match(/\bobjectid="([^"]*)"/)?.[1];
    const name = id === undefined ? undefined : names.get(id);
    const p = name === undefined ? undefined : waiting.get(name)?.shift();
    if (!p) {
      unplaced.push(name ?? `object ${id}`);
      return tag;
    }
    const t = (tag.match(/\btransform="([^"]*)"/)?.[1] ?? "1 0 0 0 1 0 0 0 1 0 0 0").trim().split(/\s+/);
    const c = (id === undefined ? undefined : centres.get(id)) ?? { cx: 0, cy: 0 };
    const transform = `1 0 0 0 1 0 0 0 1 ${(p.x - c.cx).toFixed(4)} ${(p.y - c.cy).toFixed(4)} ${t[11] ?? "0"}`;
    return /\btransform="/.test(tag) ? tag.replace(/\btransform="[^"]*"/, `transform="${transform}"`) : tag.replace(/<item\b/, `<item transform="${transform}"`);
  });
  const left = [...waiting.values()].flat().map((p) => p.name);
  if (unplaced.length > 0) throw new Error(`no place in the group layout for ${unplaced.join(", ")}`);
  if (left.length > 0) throw new Error(`no object in the arranged plate for ${left.join(", ")}`);
  return modelXml.replace(build, moved);
}
