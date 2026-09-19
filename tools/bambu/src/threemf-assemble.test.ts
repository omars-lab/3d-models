import { describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import {
  buildContentTypes,
  buildProjectSettingsConfig,
  buildThreeMfMembers,
  stripApplicationTag,
  writeThreeMf,
  xmlEscape,
} from "./threemf-assemble.js";
import { buildAmsSlotMap, type CoasterPartsSidecar } from "./ams.js";
import type { IndexedMesh } from "./mesh.js";

// A unit cube-ish mesh stub — two triangles, four vertices. Geometry content is irrelevant to the
// assembly structure (that is what these tests pin); a real body's geometry is exercised end-to-end by
// the BambuStudio screenshot check, not here.
const stubMesh: IndexedMesh = {
  vertices: [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
  triangles: [0, 1, 2, 0, 2, 3],
};

/** A 3-region coaster sidecar (base=Slab, straps=Gold, border=Copper) matching the shipped presets. */
function borderSidecar(name: string): CoasterPartsSidecar {
  return {
    coaster: name,
    pinch: "fillet",
    parts: [
      { region: "base", stl: `${name}-base.stl`, triangles: 2, paletteName: "Slab", hex: "#333333" },
      { region: "straps", stl: `${name}-straps.stl`, triangles: 2, paletteName: "Gold", hex: "#d4af37" },
      { region: "border", stl: `${name}-border.stl`, triangles: 2, paletteName: "Copper", hex: "#b87333" },
    ],
  };
}

const APP = "BambuStudio-02.08.02.61";
const DEF = { type: "PLA", id: "GFA00", hex: "#ffffff" };

/** Build the AssemblyCoaster inputs + slot map the assembler takes, from sidecars. */
function assemblyFrom(sidecars: CoasterPartsSidecar[]) {
  const map = buildAmsSlotMap(sidecars, { defaultFilament: "PLA Basic" });
  const coasters = sidecars.map((sc) => ({
    name: sc.coaster,
    bodies: sc.parts.map((p) => ({
      region: p.region,
      name: `${sc.coaster} · ${p.region}${p.paletteName ? ` (${p.paletteName})` : ""}`,
      extruder: map.assignments.get(sc.coaster)!.get(p.region)!,
      mesh: stubMesh,
    })),
  }));
  return { map, coasters };
}

describe("buildModelSettingsConfig — per-part extruder assignment (§12 / research contract)", () => {
  it("writes one <part> per region with its slot's extruder, part id === mesh objectid", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("Star")]);
    // slot map: 1=default, 2=Slab(base), 3=Gold(straps), 4=Copper(border)
    expect(map.assignments.get("Star")!.get("base")).toBe(2);
    expect(map.assignments.get("Star")!.get("straps")).toBe(3);
    expect(map.assignments.get("Star")!.get("border")).toBe(4);
    const cfg = buildThreeMfMembers(coasters, map, DEF, APP)["Metadata/model_settings.config"]!;
    // Mesh ids are 1,2,3 (base,straps,border) in order; the assembly object id continues after them (4).
    expect(cfg).toContain('<object id="4">');
    expect(cfg).toContain('<metadata key="name" value="Star"/>');
    expect(cfg).toMatch(/<part id="1" subtype="normal_part">[\s\S]*?extruder" value="2"/);
    expect(cfg).toMatch(/<part id="2" subtype="normal_part">[\s\S]*?extruder" value="3"/);
    expect(cfg).toMatch(/<part id="3" subtype="normal_part">[\s\S]*?extruder" value="4"/);
  });
});

describe("buildProjectSettingsConfig — filament slot declaration", () => {
  it("emits parallel arrays sized to the slot count, colours in slot order, non-empty ids", () => {
    const { map } = assemblyFrom([borderSidecar("Star")]);
    const json = JSON.parse(buildProjectSettingsConfig(map, DEF));
    expect(json.filament_colour).toEqual(["#ffffff", "#333333", "#d4af37", "#b87333"]);
    expect(json.filament_type).toEqual(["PLA", "PLA", "PLA", "PLA"]);
    // Per-slot product ids live under the PLURAL key; the scalar `filament_id` must stay a string,
    // or the loader segfaults (docs/issues/coaster-3mf-filament-shape-and-export-hang.md).
    expect(json.filament_ids).toEqual(["GFA00", "GFA00", "GFA00", "GFA00"]);
    expect(json.filament_ids.every((id: string) => id.length > 0)).toBe(true);
    expect(typeof json.filament_id).toBe("string");
    expect(json.filament_id.length).toBeGreaterThan(0);
  });
});

describe("buildRootModel — the Application gate + assembly components", () => {
  it("carries a BambuStudio- Application tag and one build item per coaster", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("A"), borderSidecar("B")]);
    const members = buildThreeMfMembers(coasters, map, DEF, APP);
    const root = members["3D/3dmodel.model"]!;
    expect(root).toContain('<metadata name="Application">BambuStudio-02.08.02.61</metadata>');
    expect((root.match(/<item objectid=/g) ?? []).length).toBe(2);
    // Two coasters × 3 bodies = 6 components pointing at the shared Objects part.
    expect((root.match(/<component p:path="\/3D\/Objects\/object_1.model"/g) ?? []).length).toBe(6);
  });

  it("refuses an Application tag that would make the slicer drop colour (research contract / #9666)", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("Star")]);
    expect(() => buildThreeMfMembers(coasters, map, DEF, "OrcaSlicer-2.0")).toThrow(/BambuStudio-/);
  });
});

describe("buildObjectsModel — the indexed meshes", () => {
  it("writes each body's vertices and triangles as one <object>", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("Star")]);
    const objs = buildThreeMfMembers(coasters, map, DEF, APP)["3D/Objects/object_1.model"]!;
    expect((objs.match(/<object id=/g) ?? []).length).toBe(3); // three region bodies
    expect((objs.match(/<vertex /g) ?? []).length).toBe(3 * 4); // 4 verts per stub body
    expect((objs.match(/<triangle /g) ?? []).length).toBe(3 * 2); // 2 tris per stub body
  });
});

describe("xmlEscape", () => {
  it("escapes the five entities so a palette name with & or < is safe in an attribute", () => {
    expect(xmlEscape(`A & B <"'>`)).toBe("A &amp; B &lt;&quot;&apos;&gt;");
  });
});

describe("writeThreeMf — a real .3mf round-trips through unzip", () => {
  it("produces a zip whose members re-read to the exact assembled content", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("Star")]);
    const members = buildThreeMfMembers(coasters, map, DEF, APP);
    const dir = mkdtempSync(join(tmpdir(), "3mf-test-"));
    const out = join(dir, "plate.3mf");
    writeThreeMf(members, out, join(dir, "scratch"));
    const list = execFileSync("unzip", ["-Z1", out]).toString().trim().split("\n").sort();
    expect(list).toEqual(
      [
        "[Content_Types].xml",
        "3D/3dmodel.model",
        "3D/Objects/object_1.model",
        "3D/_rels/3dmodel.model.rels",
        "Metadata/model_settings.config",
        "Metadata/project_settings.config",
        "_rels/.rels",
      ].sort(),
    );
    const backModel = execFileSync("unzip", ["-p", out, "Metadata/model_settings.config"]).toString();
    expect(backModel).toBe(members["Metadata/model_settings.config"]);
    // Sanity: the primary content type is declared and readable.
    expect(readFileSync(out).length).toBeGreaterThan(0);
    expect(buildContentTypes()).toContain("3dmanufacturing-3dmodel+xml");
  });
});

describe("writeThreeMf — a relative outPath resolves against the caller's cwd, not the scratch dir", () => {
  it("writes the .3mf where the relative path resolves (regression: zip runs with cwd=scratchDir)", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("Star")]);
    const members = buildThreeMfMembers(coasters, map, DEF, APP);
    const dir = mkdtempSync(join(tmpdir(), "3mf-rel-"));
    const prev = process.cwd();
    try {
      process.chdir(dir);
      // A RELATIVE outPath, and a scratch dir beside it. Before the fix, zip's cwd=scratch put the
      // archive at scratch/out/plate.3mf and it vanished with the scratch cleanup.
      writeThreeMf(members, "out/plate.3mf", "scratch");
      expect(existsSync(resolve("out/plate.3mf"))).toBe(true);
      expect(existsSync(join(dir, "scratch", "out", "plate.3mf"))).toBe(false);
    } finally {
      process.chdir(prev);
      rmSync(dir, { recursive: true, force: true });
    }
  });
});

describe("stripApplicationTag — the headless-safe copy for the geometry slice", () => {
  it("rewrites the versioned Application tag to bare BambuStudio, touching nothing else", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("Star")]);
    const members = buildThreeMfMembers(coasters, map, DEF, APP);
    const stripped = stripApplicationTag(members);
    // The versioned tag SIGSEGVs the headless slicer; bare BambuStudio slices exit 0 (pivot doc §1).
    expect(members["3D/3dmodel.model"]).toContain(
      `<metadata name="Application">${APP}</metadata>`,
    );
    expect(stripped["3D/3dmodel.model"]).toContain(
      '<metadata name="Application">BambuStudio</metadata>',
    );
    expect(stripped["3D/3dmodel.model"]).not.toContain(APP);
    // Every other member is carried through byte-identical — only the root model is rewritten.
    for (const key of Object.keys(members)) {
      if (key === "3D/3dmodel.model") continue;
      expect(stripped[key]).toBe(members[key]);
    }
  });

  it("does not mutate the input members (returns a fresh object)", () => {
    const { map, coasters } = assemblyFrom([borderSidecar("Star")]);
    const members = buildThreeMfMembers(coasters, map, DEF, APP);
    const before = members["3D/3dmodel.model"];
    stripApplicationTag(members);
    expect(members["3D/3dmodel.model"]).toBe(before);
  });

  it("throws when there is no versioned Application tag to strip (already bare, or absent)", () => {
    // A members object whose root model has no `BambuStudio-<ver>` tag: stripping is a no-op the caller
    // must not silently accept — an unstripped tagged file would SIGSEGV the verify slice.
    const bare = { "3D/3dmodel.model": '<metadata name="Application">BambuStudio</metadata>' };
    expect(() => stripApplicationTag(bare)).toThrow(/Application/);
  });

  it("throws when the root model member is missing entirely", () => {
    expect(() => stripApplicationTag({})).toThrow(/3D\/3dmodel\.model/);
  });
});
