/**
 * A support blocker inside a hollow piece: a sphere, marked `support_blocker` in Studio's
 * `model_settings.config`, so the slicer builds no support inside the piece while it still builds
 * support from the bed under it.
 *
 * Why: the airless ping-pong ball (ball-1) is a shell with windows. With supports on the bed only,
 * Studio still grew support up from the inside of the lower shell into the hollow, which can never
 * be taken out. "Bed only" means "not standing on the model's top faces", not "not inside the
 * model". A blocker part is Studio's own way to say "no support here", and a slice of the ball
 * with one kept the hollow empty (2026-11-08, ball-1's page has the pictures).
 *
 * The sphere is centred where the piece's own vertices say its centre is (a least-squares sphere
 * fit), so the recipe names only a radius, never a position that a re-arrange would move.
 * Every function here is PURE: XML text in, XML text out.
 */

/** A recipe's `support_blocker:` on an `stl:` item. */
export interface SupportBlocker {
  radius_mm: number;
}

/** Check a recipe's `support_blocker:`: a mapping with one key, `radius_mm`, a number above 0. */
export function checkSupportBlocker(raw: unknown, where: string): SupportBlocker {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
    throw new Error(`${where}: \`support_blocker:\` must be a mapping with \`radius_mm:\` (the sphere's radius in mm)`);
  }
  const s = raw as Record<string, unknown>;
  for (const k of Object.keys(s)) {
    if (k !== "radius_mm") throw new Error(`${where}: \`support_blocker.${k}\` is not a blocker setting; it takes radius_mm`);
  }
  if (typeof s.radius_mm !== "number" || !Number.isFinite(s.radius_mm) || s.radius_mm <= 0) {
    throw new Error(`${where}: \`support_blocker.radius_mm\` must be a number of mm above 0, got ${JSON.stringify(s.radius_mm)}`);
  }
  return { radius_mm: s.radius_mm };
}

type Vec3 = [number, number, number];

/** The least-squares sphere through the points: solves x²+y²+z² = 2ax + 2by + 2cz + d. */
export function sphereFit(points: Vec3[]): { centre: Vec3; radius: number } {
  if (points.length < 4) throw new Error(`a sphere fit needs 4 points or more, got ${points.length}`);
  // Normal equations A·[a b c d] = b for rows [2x 2y 2z 1] → x²+y²+z².
  const m = Array.from({ length: 4 }, () => [0, 0, 0, 0, 0]);
  for (const [x, y, z] of points) {
    const row = [2 * x, 2 * y, 2 * z, 1];
    const rhs = x * x + y * y + z * z;
    for (let i = 0; i < 4; i++) {
      for (let j = 0; j < 4; j++) m[i]![j]! += row[i]! * row[j]!;
      m[i]![4]! += row[i]! * rhs;
    }
  }
  for (let col = 0; col < 4; col++) {
    let pivot = col;
    for (let r = col + 1; r < 4; r++) if (Math.abs(m[r]![col]!) > Math.abs(m[pivot]![col]!)) pivot = r;
    if (Math.abs(m[pivot]![col]!) < 1e-12) throw new Error("the points do not fix a sphere (all on a plane or a line)");
    [m[col], m[pivot]] = [m[pivot]!, m[col]!];
    for (let r = 0; r < 4; r++) {
      if (r === col) continue;
      const f = m[r]![col]! / m[col]![col]!;
      for (let k = col; k < 5; k++) m[r]![k]! -= f * m[col]![k]!;
    }
  }
  const [a, b, c, d] = [0, 1, 2, 3].map((i) => m[i]![4]! / m[i]![i]!) as [number, number, number, number];
  return { centre: [a, b, c], radius: Math.sqrt(Math.max(0, d + a * a + b * b + c * c)) };
}

/** A closed UV sphere as 3MF `<vertices>` and `<triangles>`, faces outward. */
export function sphereMeshXml(centre: Vec3, radius: number, stacks = 48, slices = 96): string {
  const [cx, cy, cz] = centre;
  const v: Vec3[] = [[cx, cy, cz + radius]];
  for (let i = 1; i < stacks; i++) {
    const th = (Math.PI * i) / stacks;
    for (let j = 0; j < slices; j++) {
      const ph = (2 * Math.PI * j) / slices;
      v.push([cx + radius * Math.sin(th) * Math.cos(ph), cy + radius * Math.sin(th) * Math.sin(ph), cz + radius * Math.cos(th)]);
    }
  }
  v.push([cx, cy, cz - radius]);
  const ring = (i: number, j: number) => 1 + (i - 1) * slices + (j % slices);
  const t: Vec3[] = [];
  for (let j = 0; j < slices; j++) t.push([0, ring(1, j), ring(1, j + 1)]);
  for (let i = 1; i < stacks - 1; i++) {
    for (let j = 0; j < slices; j++) {
      const [p, q, r, s] = [ring(i, j), ring(i, j + 1), ring(i + 1, j), ring(i + 1, j + 1)];
      t.push([p, r, q], [q, r, s]);
    }
  }
  const last = v.length - 1;
  for (let j = 0; j < slices; j++) t.push([ring(stacks - 1, j), last, ring(stacks - 1, j + 1)]);
  const vx = v.map(([x, y, z]) => `     <vertex x="${x.toFixed(6)}" y="${y.toFixed(6)}" z="${z.toFixed(6)}"/>\n`).join("");
  const tx = t.map(([p, q, r]) => `     <triangle v1="${p}" v2="${q}" v3="${r}"/>\n`).join("");
  return `   <mesh>\n    <vertices>\n${vx}    </vertices>\n    <triangles>\n${tx}    </triangles>\n   </mesh>\n`;
}

/** A 3MF transform (12 numbers, row-vector order) applied to a point. */
function apply(t: number[], [x, y, z]: Vec3): Vec3 {
  return [
    x * t[0]! + y * t[3]! + z * t[6]! + t[9]!,
    x * t[1]! + y * t[4]! + z * t[7]! + t[10]!,
    x * t[2]! + y * t[5]! + z * t[8]! + t[11]!,
  ];
}

const IDENTITY = "1 0 0 0 1 0 0 0 1 0 0 0";
const BLOCKER_NAME = "no support inside";

/** What one blocker came to, for the log and the read-back. */
export interface BlockerPlaced {
  name: string; // the object's name (the staged mesh)
  objectId: string; // its id in 3D/3dmodel.model
  blockerId: string; // the blocker mesh's object id, which its part line in model_settings.config names
  centre: Vec3; // the fit centre, in the object's own frame
  fitRadius: number; // the sphere the piece's vertices fit
  inner: number; // the nearest vertex to the centre
  outer: number; // the farthest
  radius: number; // the blocker's
}

/**
 * Add a blocker sphere to every object whose name is in `byName`: a mesh object appended to the
 * object's own mesh file, a second `<component>` (identity transform) in the root model, and a
 * `<part subtype="support_blocker">` in `model_settings.config`. The sphere is centred on the fit of
 * the object's own vertices, taken through each component's transform. Refuses a radius that reaches
 * within 1 mm of the piece's outer face, since that would also block the support the bed has to give
 * the outside. Throws when a name matches no object. PURE: returns the changed texts.
 */
export function injectSupportBlockers(
  rootModel: string,
  settingsXml: string,
  meshes: Map<string, string>, // p:path → that mesh file's XML
  byName: Map<string, SupportBlocker>,
): { rootModel: string; settingsXml: string; meshes: Map<string, string>; placed: BlockerPlaced[] } {
  const names = new Map<string, string>();
  for (const block of settingsXml.match(/<object\s+id="[^"]*">[\s\S]*?<\/object>/g) ?? []) {
    const id = block.match(/<object\s+id="([^"]*)"/)?.[1];
    const name = block.match(/<metadata\s+key="name"\s+value="([^"]*)"/)?.[1];
    if (id !== undefined && name !== undefined) names.set(id, name);
  }
  // Ids are shared across the root model and its mesh files; a new one is past every id in any of them.
  let nextId = 0;
  for (const text of [rootModel, ...meshes.values()]) {
    for (const m of text.matchAll(/<object\s+id="(\d+)"/g)) nextId = Math.max(nextId, Number(m[1]));
  }
  const outMeshes = new Map(meshes);
  const placed: BlockerPlaced[] = [];
  const seen = new Set<string>();
  const root = rootModel.replace(/<object\s+id="([^"]*)"[^>]*>[\s\S]*?<\/object>/g, (obj, id: string) => {
    const name = names.get(id);
    const want = name === undefined ? undefined : byName.get(name);
    if (!want || name === undefined) return obj;
    const comps = obj.match(/<component\b[^>]*\/>/g) ?? [];
    if (comps.length === 0) throw new Error(`object ${name}: no <component> to add a blocker beside`);
    const pts: Vec3[] = [];
    let path = "";
    for (const c of comps) {
      path = c.match(/\bp:path="([^"]*)"/)?.[1] ?? "";
      const oid = c.match(/\bobjectid="([^"]*)"/)?.[1];
      const file = outMeshes.get(path);
      if (file === undefined) throw new Error(`object ${name}: no mesh file ${path || "(no path)"}`);
      const t = (c.match(/\btransform="([^"]*)"/)?.[1] ?? IDENTITY).trim().split(/\s+/).map(Number);
      const body = file.match(new RegExp(`<object\\s+id="${oid}"[^>]*>([\\s\\S]*?)</object>`))?.[1] ?? "";
      for (const v of body.matchAll(/<vertex\s+x="([^"]*)"\s+y="([^"]*)"\s+z="([^"]*)"/g)) {
        pts.push(apply(t, [Number(v[1]), Number(v[2]), Number(v[3])]));
      }
    }
    const fit = sphereFit(pts);
    const dist = pts.map((p) => Math.hypot(p[0] - fit.centre[0], p[1] - fit.centre[1], p[2] - fit.centre[2]));
    const inner = Math.min(...dist);
    const outer = Math.max(...dist);
    if (want.radius_mm > outer - 1) {
      throw new Error(
        `object ${name}: a blocker of radius ${want.radius_mm} mm reaches within 1 mm of the piece's outer face ` +
          `(${outer.toFixed(2)} mm from its centre), so it would also stop the support the bed gives the outside`,
      );
    }
    nextId += 1;
    const bid = String(nextId);
    const file = outMeshes.get(path)!;
    const uuid = (n: number) => `b10c0000-0000-4000-8000-${String(n).padStart(12, "0")}`;
    const mesh = `  <object id="${bid}" p:UUID="${uuid(Number(bid))}" type="model">\n${sphereMeshXml(fit.centre, want.radius_mm)}  </object>\n`;
    if (!/<\/resources>/.test(file)) throw new Error(`object ${name}: its mesh file ${path} has no </resources>`);
    outMeshes.set(path, file.replace(/<\/resources>/, `${mesh} </resources>`));
    seen.add(name);
    placed.push({ name, objectId: id, blockerId: bid, centre: fit.centre, fitRadius: fit.radius, inner, outer, radius: want.radius_mm });
    const comp = `    <component p:path="${path}" objectid="${bid}" p:UUID="${uuid(Number(bid) + 500000)}" transform="${IDENTITY}"/>\n`;
    return obj.replace(/([ \t]*)<\/components>/, `${comp}$1</components>`);
  });
  const missing = [...byName.keys()].filter((n) => !seen.has(n));
  if (missing.length > 0) throw new Error(`no object named ${missing.join(", ")} in the arranged plate to put a blocker in`);
  // The part line goes after the object's last part, so Studio reads it as one more volume of that object.
  const byObject = new Map(placed.map((p) => [p.objectId, p.blockerId]));
  const settings = settingsXml.replace(/(<object\s+id="([^"]*)">)([\s\S]*?)(\n[ \t]*<\/object>)/g, (whole, open: string, id: string, body: string, close: string) => {
    const bid = byObject.get(id);
    if (bid === undefined) return whole;
    const part =
      `\n    <part id="${bid}" subtype="support_blocker">\n` +
      `      <metadata key="name" value="${BLOCKER_NAME}"/>\n` +
      `      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n` +
      `    </part>`;
    return `${open}${body}${part}${close}`;
  });
  return { rootModel: root, settingsXml: settings, meshes: outMeshes, placed };
}

/** How many `support_blocker` parts each named object carries in a (sliced) `model_settings.config`. */
export function blockersByName(settingsXml: string): Map<string, number[]> {
  const out = new Map<string, number[]>();
  for (const block of settingsXml.match(/<object\s+id="[^"]*">[\s\S]*?<\/object>/g) ?? []) {
    const name = block.split(/<part\b/)[0]?.match(/<metadata\s+key="name"\s+value="([^"]*)"/)?.[1] ?? "";
    const n = (block.match(/<part\b[^>]*\bsubtype="support_blocker"/g) ?? []).length;
    out.set(name, [...(out.get(name) ?? []), n]);
  }
  return out;
}

/** The read-back: every object of each named item carries exactly one blocker, and no other object
 *  carries any. [] when the slice is as the recipe says. PURE. */
export function blockersMissing(read: Map<string, number[]>, want: { name: string; count: number }[]): string[] {
  const problems: string[] = [];
  const wanted = new Map(want.map((w) => [w.name, w.count]));
  for (const [name, counts] of read) {
    const need = wanted.get(name);
    if (need === undefined) {
      if (counts.some((n) => n > 0)) problems.push(`${name}: carries a support blocker in the slice, the recipe asks for none`);
      continue;
    }
    if (counts.length < need) problems.push(`${name}: ${counts.length} object(s) in the slice, ${need} expected`);
    if (counts.some((n) => n !== 1)) problems.push(`${name}: blockers per object in the slice are ${counts.join(", ")}, the recipe asks for 1`);
  }
  for (const [name] of wanted) if (!read.has(name)) problems.push(`${name}: not in the slice`);
  return problems;
}
