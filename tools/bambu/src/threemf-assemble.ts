// Assemble a multi-part, multi-filament input 3MF for a coloured coaster plate (part 4b-ii; D-075,
// docs/plate-composer-design.md §12; the contract is docs/research/coaster-ams-3mf-contract.md).
//
// WHY this exists: the headless BambuStudio/Orca CLI has NO flag to map objects or regions to filament
// slots at slice time — the assignment must be baked into the INPUT 3MF (BambuStudio#9666, the settled
// research answer). So a coloured plate is not the loose-STL `--arrange` path `slice compose` uses for a
// mono-colour plate (that path treats each STL as an independent object). Instead every coaster becomes
// ONE object whose region bodies are PARTS sharing the coaster's coordinate frame, so `--arrange` packs
// whole coasters, not loose bodies (the §12 K10 note). Each part carries `<metadata key="extruder"
// value="K"/>` for its logical slot, and the root model carries `Application: BambuStudio-<ver>` — the
// gate that makes the slicer honour per-part assignment at all (else it imports single-colour, #9666).
//
// WHAT is verifiable here vs. at the owner gate: this module builds a structurally valid 3MF (a ZIP of
// OPC parts) whose XML/config members this file's tests pin against the contract, and which re-reads
// through the same `unzip` path `threemf.ts` uses. That BambuStudio ACCEPTS it and slices each region in
// its slot colour is confirmed by loading the assembled plate in BambuStudio and reading the render (the
// screenshot check) — NOT claimed by this module. Printing stays owner-gated (§11).

import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import type { IndexedMesh } from "./mesh.js";
import { filamentArrays, type AmsSlotMap, type FilamentDefaults } from "./ams.js";

/** One region body to bake into the plate: its slicer-facing name, its 1-based logical filament slot,
 *  and its indexed geometry. */
export interface AssemblyBody {
  region: string;
  name: string; // the part name shown in the slicer object tree, e.g. "coaster-1 · straps (Gold)"
  extruder: number; // 1-based logical slot (§12; the value written as <metadata key="extruder">)
  mesh: IndexedMesh;
}
/** One whole coaster: a named object whose region bodies become parts in a shared coordinate frame. */
export interface AssemblyCoaster {
  name: string; // unique per plate — the object name in the slicer tree
  bodies: AssemblyBody[];
}

/** The default filament the plate is sliced in — slot 1, and the material/id every colour slot reuses
 *  (only the colour is overridden per slot; §6 / research contract). The `ams.ts` type is the source of
 *  truth; re-exported here so the assembler's boundary reads clearly at its call site. */
export type DefaultFilamentSpec = FilamentDefaults;

// A deterministic UUID generator: the 3MF production extension wants a p:UUID on every object, component
// and build item, but the value need only be unique within the package — it is not content-addressed.
// Sequential ids keep an assembled plate byte-reproducible (so the same manifest yields the same 3MF,
// matching the composer's iteration-cache philosophy) and keep the tests free of random output.
function uuidGen(): () => string {
  let n = 0;
  return () => {
    n += 1;
    const hex = n.toString(16).padStart(12, "0");
    return `00000000-0000-0000-0000-${hex}`;
  };
}

const XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n';

/** Escape the five XML entities for an attribute/text value (part names carry palette names + spaces). */
export function xmlEscape(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

/** A serialisable number for a 3MF coordinate: finite, and never in exponent form (some importers choke
 *  on `1e-7`). Trailing zeros are trimmed. */
function coord(x: number): string {
  if (!Number.isFinite(x)) return "0";
  // toFixed(6) is well under float32 precision and avoids exponent notation for the coordinate ranges a
  // coaster occupies (tens of mm); trim trailing zeros so the file stays compact.
  return x.toFixed(6).replace(/\.?0+$/, "");
}

// ── The OPC skeleton (fixed members) ───────────────────────────────────────────────────────────────

/** `[Content_Types].xml` — declares the media types for the model parts and the rels. */
export function buildContentTypes(): string {
  return (
    XML_HEADER +
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n' +
    ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n' +
    ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n' +
    "</Types>\n"
  );
}

/** `_rels/.rels` — the package root points at the primary 3dmodel.model part. */
export function buildRootRels(): string {
  return (
    XML_HEADER +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n' +
    ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n' +
    "</Relationships>\n"
  );
}

/** `3D/_rels/3dmodel.model.rels` — the root model points at the Objects part that holds the meshes
 *  (the production extension's cross-file reference). */
export function buildModelRels(): string {
  return (
    XML_HEADER +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n' +
    ' <Relationship Target="/3D/Objects/object_1.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n' +
    "</Relationships>\n"
  );
}

// ── The mesh part (3D/Objects/object_1.model) ────────────────────────────────────────────────────────
// Every region body of every coaster becomes one `<object>` here, with a stable numeric id. The root
// model references these by (path, objectid) components. Ids are assigned in flat coaster/body order.

/** A body with its assigned mesh-object id, threaded through both the mesh part and the root model. */
interface IdBody extends AssemblyBody {
  meshId: number;
}
interface IdCoaster {
  name: string;
  objectId: number; // the assembly object's id in 3dmodel.model
  bodies: IdBody[];
}

/** Assign mesh-object ids (1..N, in coaster/body order) and assembly-object ids (after the meshes). */
function assignIds(coasters: AssemblyCoaster[]): IdCoaster[] {
  let meshId = 0;
  const withMesh = coasters.map((c) => ({
    name: c.name,
    bodies: c.bodies.map((b) => ({ ...b, meshId: (meshId += 1) })),
  }));
  let objectId = meshId; // assembly ids continue after the last mesh id
  return withMesh.map((c) => ({ ...c, objectId: (objectId += 1) }));
}

/** `3D/Objects/object_1.model` — the indexed meshes, one `<object>` per body. */
export function buildObjectsModel(coasters: IdCoaster[], uuid: () => string): string {
  const out: string[] = [
    XML_HEADER,
    '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n',
    ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n',
    " <resources>\n",
  ];
  for (const c of coasters) {
    for (const b of c.bodies) {
      out.push(`  <object id="${b.meshId}" p:UUID="${uuid()}" type="model">\n   <mesh>\n    <vertices>\n`);
      const v = b.mesh.vertices;
      for (let i = 0; i < v.length; i += 3) {
        out.push(`     <vertex x="${coord(v[i]!)}" y="${coord(v[i + 1]!)}" z="${coord(v[i + 2]!)}"/>\n`);
      }
      out.push("    </vertices>\n    <triangles>\n");
      const t = b.mesh.triangles;
      for (let i = 0; i < t.length; i += 3) {
        out.push(`     <triangle v1="${t[i]}" v2="${t[i + 1]}" v3="${t[i + 2]}"/>\n`);
      }
      out.push("    </triangles>\n   </mesh>\n  </object>\n");
    }
  }
  out.push(" </resources>\n</model>\n");
  return out.join("");
}

// ── The root model (3D/3dmodel.model) ────────────────────────────────────────────────────────────────
// One assembly `<object>` per coaster, each a set of `<component>`s pointing (cross-file) at the body
// meshes in the same shared coordinate frame (identity component transforms). One `<build><item>` per
// coaster; `--arrange 1` repacks the items, so build transforms are identity (the K10 note in §12).

/** `3D/3dmodel.model` — the assembly objects + build items + the Application gate metadata. */
export function buildRootModel(coasters: IdCoaster[], appVersion: string, uuid: () => string): string {
  const out: string[] = [
    XML_HEADER,
    '<model xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" unit="millimeter" xml:lang="en-US" requiredextensions="p" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021">\n',
    // The Application metadata MUST start with "BambuStudio-" or the slicer ignores per-part extruder
    // assignment and imports the plate single-colour (research contract; #9666).
    ` <metadata name="Application">${xmlEscape(appVersion)}</metadata>\n`,
    ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n',
    " <resources>\n",
  ];
  for (const c of coasters) {
    out.push(`  <object id="${c.objectId}" p:UUID="${uuid()}" type="model">\n   <components>\n`);
    for (const b of c.bodies) {
      out.push(
        `    <component p:path="/3D/Objects/object_1.model" objectid="${b.meshId}" p:UUID="${uuid()}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>\n`,
      );
    }
    out.push("   </components>\n  </object>\n");
  }
  out.push(" </resources>\n <build");
  out.push(` p:UUID="${uuid()}">\n`);
  for (const c of coasters) {
    out.push(`  <item objectid="${c.objectId}" p:UUID="${uuid()}" transform="1 0 0 0 1 0 0 0 1 0 0 0" printable="1"/>\n`);
  }
  out.push(" </build>\n</model>\n");
  return out.join("");
}

// ── Metadata/model_settings.config ───────────────────────────────────────────────────────────────────
// The per-object + per-part extruder assignment. Each assembly object lists its region bodies as
// `<part id=meshId subtype="normal_part">` (part id === the component objectid), each carrying the
// `extruder` metadata for its slot. The object-level extruder is the first part's (a harmless default;
// the per-part values are what colour the regions).

export function buildModelSettingsConfig(coasters: IdCoaster[]): string {
  const out: string[] = [XML_HEADER, "<config>\n"];
  for (const c of coasters) {
    const objExtruder = c.bodies[0]?.extruder ?? 1;
    out.push(`  <object id="${c.objectId}">\n`);
    out.push(`    <metadata key="name" value="${xmlEscape(c.name)}"/>\n`);
    out.push(`    <metadata key="extruder" value="${objExtruder}"/>\n`);
    for (const b of c.bodies) {
      out.push(`    <part id="${b.meshId}" subtype="normal_part">\n`);
      out.push(`      <metadata key="name" value="${xmlEscape(b.name)}"/>\n`);
      out.push('      <metadata key="matrix" value="1 0 0 0 1 0 0 0 1 0 0 0"/>\n');
      out.push(`      <metadata key="extruder" value="${b.extruder}"/>\n`);
      out.push("    </part>\n");
    }
    out.push("  </object>\n");
  }
  out.push("</config>\n");
  return out.join("");
}

// ── Metadata/project_settings.config ─────────────────────────────────────────────────────────────────
// The filament slot declaration: parallel arrays sized to the logical slot count, every colour slot
// reusing the default's material + a NON-EMPTY id (an empty id silently routes to the external spool),
// only the colour overridden per slot (research contract). This member declares how many slots there
// are and their colours; each part's `extruder` metadata (buildModelSettingsConfig) is what routes a
// region to a slot.
//
// Key shapes are NOT interchangeable: `filament_colour`, `filament_type` and the per-slot product-id
// array `filament_ids` are arrays, but `filament_id` is a SCALAR string in Bambu's config schema.
// Emitting `filament_id` as an array made the JSON config parser throw
// `type must be string, but is array` and segfault the loader (exit -11) —
// docs/issues/coaster-3mf-filament-shape-and-export-hang.md.

export function buildProjectSettingsConfig(map: AmsSlotMap, def: DefaultFilamentSpec): string {
  const arrays = filamentArrays(map, def);
  return JSON.stringify(
    {
      filament_type: arrays.filament_type,
      filament_colour: arrays.filament_colour,
      filament_ids: arrays.filament_ids,
      filament_id: def.id, // scalar — a single product id, never the per-slot array (see above)
    },
    null,
    2,
  ) + "\n";
}

// ── The assembly ─────────────────────────────────────────────────────────────────────────────────────

/** The in-memory members of an assembled 3MF, keyed by their archive path. Pure — no filesystem, so the
 *  tests assert the exact member contents; `assemble3mf` writes and zips these. */
export interface ThreeMfMembers {
  [archivePath: string]: string;
}

/** Build every 3MF member for a coloured plate, in memory. `appVersion` is the BambuStudio version tag
 *  (must start with "BambuStudio-"); `map` + `def` come from the plate's palette-name → slot mapping. */
export function buildThreeMfMembers(
  coasters: AssemblyCoaster[],
  map: AmsSlotMap,
  def: DefaultFilamentSpec,
  appVersion: string,
): ThreeMfMembers {
  if (coasters.length === 0) throw new Error("cannot assemble a 3MF with no coasters");
  if (!appVersion.startsWith("BambuStudio-")) {
    throw new Error(
      `3MF Application metadata must start with "BambuStudio-" or the slicer ignores per-part colour ` +
        `assignment (research contract; #9666) — got "${appVersion}"`,
    );
  }
  const ided = assignIds(coasters);
  const uuid = uuidGen();
  return {
    "[Content_Types].xml": buildContentTypes(),
    "_rels/.rels": buildRootRels(),
    "3D/3dmodel.model": buildRootModel(ided, appVersion, uuid),
    "3D/_rels/3dmodel.model.rels": buildModelRels(),
    "3D/Objects/object_1.model": buildObjectsModel(ided, uuid),
    "Metadata/model_settings.config": buildModelSettingsConfig(ided),
    "Metadata/project_settings.config": buildProjectSettingsConfig(map, def),
  };
}

/** Write the members under a scratch dir and zip them into `outPath` (a .3mf is a zip). Shells out to
 *  `zip` — the same no-bundled-zip-lib convention `threemf.ts` uses for reading (unzip). */
export function writeThreeMf(members: ThreeMfMembers, outPath: string, scratchDir: string): void {
  rmSync(scratchDir, { recursive: true, force: true });
  const names: string[] = [];
  for (const [rel, content] of Object.entries(members)) {
    const full = join(scratchDir, rel);
    mkdirSync(dirname(full), { recursive: true });
    writeFileSync(full, content);
    names.push(rel);
  }
  // Resolve to an absolute path FIRST: zip runs with cwd=scratchDir, so a relative outPath would land
  // inside the scratch dir (and be deleted with it), not where the caller asked.
  const outAbs = resolve(outPath);
  mkdirSync(dirname(outAbs), { recursive: true });
  rmSync(outAbs, { force: true });
  // -X drops extra file attributes for a reproducible archive; paths are relative to scratchDir (-j would
  // flatten the tree, which OPC forbids — the directory structure IS the package).
  execFileSync("zip", ["-X", "-q", outAbs, ...names], { cwd: scratchDir });
}
