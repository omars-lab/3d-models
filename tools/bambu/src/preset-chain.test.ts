// Tests for the preset-chain flattener and the check that a slice carried it.
//
// Two kinds of fixture:
//   - a synthetic three-level chain written to a temp dir per test, so each merge rule is visible;
//   - test/fixtures/minis-04/: the real X2D machine, process and filament presets as this module
//     flattens them from Bambu Studio 02.08.02.61's bundled profiles, and the project settings of two
//     real minis-04 slices, 2026-09-26: `old-slice` is the plate sliced from the top preset files
//     alone (the bug, docs/research/print-quality-verification.md §1.2), `flattened-slice` the same
//     plate re-sliced from the flattened files. The old one must fail the check; the new one pass.

import { describe, it, expect } from "vitest";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, copyFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import {
  flattenPreset,
  flattenPresetList,
  studioPresetLookup,
  compareSliceToPresets,
  formatMismatch,
  type FlattenedPreset,
  type PresetLookup,
} from "./preset-chain.js";
import { checkSliceCarriesPresets } from "./commands/slice.js";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "test", "fixtures", "minis-04");

/** Write a preset JSON into `dir` and return its path. */
function preset(dir: string, file: string, body: Record<string, unknown>): string {
  const p = join(dir, file);
  writeFileSync(p, JSON.stringify(body, null, 2));
  return p;
}

/** A lookup over a plain name → path map (the synthetic chain's "profiles"). */
function mapLookup(map: Record<string, string>): PresetLookup {
  return (name) => map[name] ?? null;
}

/** leaf → mid → root, each level overriding something the level below sets. */
function threeLevelChain(dir: string): { leaf: string; lookup: PresetLookup } {
  const root = preset(dir, "root.json", {
    type: "process",
    name: "root",
    from: "system",
    instantiation: "false",
    wall_generator: "arachne", // overridden by mid
    top_shell_layers: "4", // overridden by leaf
    elefant_foot_compensation: "0", // overridden by mid, then leaf
    seam_position: "aligned", // set only here: must survive to the leaf
    bridge_speed: ["50", "50", "50"], // overridden whole by mid's shorter list
  });
  const mid = preset(dir, "mid.json", {
    type: "process",
    name: "mid",
    inherits: "root",
    wall_generator: "classic",
    elefant_foot_compensation: "0.1",
    bridge_speed: ["30"],
    brim_width: "5", // set only here
  });
  const leaf = preset(dir, "leaf.json", {
    type: "process",
    name: "leaf",
    inherits: "mid",
    from: "system",
    instantiation: "true",
    top_shell_layers: "5",
    elefant_foot_compensation: "0.15",
  });
  return { leaf, lookup: mapLookup({ root, mid, leaf }) };
}

describe("flattenPreset", () => {
  it("merges a three-level chain child over parent, all the way down", () => {
    const dir = mkdtempSync(join(tmpdir(), "chain-"));
    const { leaf, lookup } = threeLevelChain(dir);
    const flat = flattenPreset(leaf, lookup);
    expect(flat.chain).toEqual(["leaf", "mid", "root"]);
    expect(flat.type).toBe("process");
    expect(flat.config.elefant_foot_compensation).toBe("0.15"); // leaf over mid over root
    expect(flat.config.top_shell_layers).toBe("5"); // leaf over root
    expect(flat.config.wall_generator).toBe("classic"); // mid over root
    expect(flat.config.brim_width).toBe("5"); // mid only
    expect(flat.config.seam_position).toBe("aligned"); // root only
    expect(flat.config.bridge_speed).toEqual(["30"]); // a list is replaced whole, not merged
    expect(flat.config.name).toBe("leaf");
    expect(flat.config.instantiation).toBe("true");
    expect("inherits" in flat.config).toBe(false);
  });

  it("lays each level's include templates under that level's own keys (Studio's order)", () => {
    const dir = mkdtempSync(join(tmpdir(), "chain-"));
    const base = preset(dir, "base.json", { type: "filament", name: "base", fan_min_speed: "20", nozzle_temperature: ["200"] });
    const tmpl = preset(dir, "tmpl.json", {
      type: "filament",
      name: "tmpl",
      instantiation: "false",
      nozzle_temperature: ["220", "220"], // over the parent
      fan_min_speed: "60", // under the level's own key
      filament_extruder_variant: ["Direct Drive Standard", "Bowden Standard"],
    });
    const leaf = preset(dir, "leaf.json", {
      type: "filament",
      name: "leaf",
      inherits: "base",
      include: ["tmpl"],
      fan_min_speed: "100",
    });
    const flat = flattenPreset(leaf, mapLookup({ base, tmpl, leaf }));
    expect(flat.config.fan_min_speed).toBe("100");
    expect(flat.config.nozzle_temperature).toEqual(["220", "220"]);
    expect(flat.config.filament_extruder_variant).toEqual(["Direct Drive Standard", "Bowden Standard"]);
    expect(flat.config.name).toBe("leaf"); // an include never lends its name
    expect(flat.config.instantiation).toBeUndefined(); // …nor its instantiation
    expect("include" in flat.config).toBe(false);
  });

  it("refuses a missing parent, naming it", () => {
    const dir = mkdtempSync(join(tmpdir(), "chain-"));
    const { leaf, lookup } = threeLevelChain(dir);
    const noRoot: PresetLookup = (name, type) => (name === "root" ? null : lookup(name, type));
    expect(() => flattenPreset(leaf, noRoot)).toThrow(/missing parent preset "root" \(inherited by "mid"/);
  });

  it("refuses a missing include, naming it", () => {
    const dir = mkdtempSync(join(tmpdir(), "chain-"));
    const leaf = preset(dir, "leaf.json", { type: "filament", name: "leaf", include: "gone" });
    expect(() => flattenPreset(leaf, () => null)).toThrow(/missing include "gone"/);
  });

  it("refuses a chain that loops", () => {
    const dir = mkdtempSync(join(tmpdir(), "chain-"));
    const a = preset(dir, "a.json", { type: "process", name: "a", inherits: "b" });
    const b = preset(dir, "b.json", { type: "process", name: "b", inherits: "a" });
    expect(() => flattenPreset(a, mapLookup({ a, b }))).toThrow(/loops: a → b → a/);
  });

  it("writes one flattened file per preset in a ';'-joined list", () => {
    const dir = mkdtempSync(join(tmpdir(), "chain-"));
    const { leaf, lookup } = threeLevelChain(dir);
    const out = mkdtempSync(join(tmpdir(), "flat-"));
    const r = flattenPresetList(`${leaf}`, lookup, out);
    expect(r.list).toBe(join(out, "leaf.json"));
    const written = JSON.parse(readFileSync(r.list, "utf8")) as Record<string, unknown>;
    expect(written.wall_generator).toBe("classic");
    expect(written.inherits).toBeUndefined();
  });
});

describe("studioPresetLookup", () => {
  it("finds a parent through the vendor index's sub_path, as Studio does", () => {
    const root = mkdtempSync(join(tmpdir(), "profiles-"));
    mkdirSync(join(root, "BBL", "filament", "sub"), { recursive: true });
    writeFileSync(
      join(root, "BBL.json"),
      JSON.stringify({ filament_list: [{ name: "Odd Name @base", sub_path: "filament/sub/odd.json" }] }),
    );
    writeFileSync(join(root, "BBL", "filament", "sub", "odd.json"), "{}");
    const lookup = studioPresetLookup(root);
    expect(lookup("Odd Name @base", "filament")).toBe(join(root, "BBL", "filament", "sub", "odd.json"));
    expect(lookup("nowhere", "filament")).toBeNull();
  });
});

describe("compareSliceToPresets", () => {
  const flat = (type: string, config: Record<string, unknown>): FlattenedPreset => ({
    leaf: `${type}.json`,
    type,
    chain: [String(config.name ?? type)],
    config,
  });

  it("reads Studio's spelling of the same value as the same value", () => {
    const presets = [
      flat("process", {
        name: "p",
        top_shell_thickness: "1.0", // Studio writes "1"
        top_surface_density: "100", // Studio writes "100%"
        monotonic_travel_into_wall: "45.0", // Studio writes "45%"
        best_object_pos: "0.3x0.5", // Studio writes "0.3,0.5"
        print_settings_id: "", // the slice fills in the preset's name
      }),
    ];
    const r = compareSliceToPresets(
      {
        top_shell_thickness: "1",
        top_surface_density: "100%",
        monotonic_travel_into_wall: "45%",
        best_object_pos: "0.3,0.5",
        print_settings_id: "p",
      },
      presets,
    );
    expect(r.mismatches).toEqual([]);
  });

  it("names every key whose value differs, and fails a built-in fallback", () => {
    const presets = [flat("process", { name: "p", wall_generator: "classic", elefant_foot_compensation: "0.15" })];
    const r = compareSliceToPresets({ wall_generator: "arachne", elefant_foot_compensation: "0" }, presets);
    expect(r.mismatches.map((m) => m.key)).toEqual(["wall_generator", "elefant_foot_compensation"]);
    expect(formatMismatch(r.mismatches[0]!)).toBe(
      'p: wall_generator is "arachne" in the slice, preset chain sets "classic"',
    );
  });

  it("reports a key the slice does not carry at all without failing it", () => {
    const r = compareSliceToPresets({}, [flat("process", { name: "p", wall_infill_order: "inner wall/outer wall/infill" })]);
    expect(r.mismatches).toEqual([]);
    expect(r.notInSlice).toEqual(["wall_infill_order"]);
  });

  it("reads each filament from its own slot of the project's per-filament lists", () => {
    const presets = [
      flat("filament", { name: "a", fan_min_speed: ["100"] }),
      flat("filament", { name: "b", fan_min_speed: ["60"] }),
    ];
    expect(compareSliceToPresets({ fan_min_speed: ["100", "60"] }, presets).mismatches).toEqual([]);
    const swapped = compareSliceToPresets({ fan_min_speed: ["60", "100"] }, presets).mismatches;
    expect(swapped.map((m) => m.preset)).toEqual(["a", "b"]);
  });

  it("skips nil placeholders; a scalar expanded to a list must hold in every element", () => {
    const presets = [flat("filament", { name: "f", filament_z_hop: ["nil"], filament_flush_temp_fast: "0" })];
    expect(compareSliceToPresets({ filament_flush_temp_fast: ["0", "0"] }, presets).mismatches).toEqual([]);
    expect(compareSliceToPresets({ filament_flush_temp_fast: ["0", "5"] }, presets).mismatches).toHaveLength(1);
  });

  it("allows a list collapsed to its first element only for the measured keys", () => {
    const presets = [
      flat("filament", {
        name: "f",
        filament_dev_ams_drying_temperature: ["45", "45", "45", "45"],
        filament_max_volumetric_speed: ["21", "40"],
      }),
    ];
    const r = compareSliceToPresets(
      { filament_dev_ams_drying_temperature: "45", filament_max_volumetric_speed: ["21"] },
      presets,
    );
    expect(r.mismatches.map((m) => m.key)).toEqual(["filament_max_volumetric_speed"]);
  });
});

// ── The real plate: minis-04 sliced before and after the fix ─────────────────────────────────────

function realPresets(): FlattenedPreset[] {
  return ["machine", "process", "filament"].map((type) => {
    const config = JSON.parse(readFileSync(join(FIXTURES, `${type}.flat.json`), "utf8")) as Record<string, unknown>;
    return { leaf: `${type}.flat.json`, type, chain: [String(config.name)], config };
  });
}

/** Pack a project_settings.config into a minimal .3mf (a zip), as the slicer's output carries it. */
function fixture3mf(settingsFile: string): string {
  const dir = mkdtempSync(join(tmpdir(), "fixture-3mf-"));
  mkdirSync(join(dir, "Metadata"));
  copyFileSync(join(FIXTURES, settingsFile), join(dir, "Metadata", "project_settings.config"));
  const res = spawnSync("zip", ["-q", "-r", "plate.3mf", "Metadata"], { cwd: dir });
  if (res.status !== 0) throw new Error(`zip failed: ${res.stderr}`);
  return join(dir, "plate.3mf");
}

describe("the minis-04 slice carries the flattened chain", () => {
  it("PASS: the plate re-sliced from flattened presets carries every value", async () => {
    const r = await checkSliceCarriesPresets(fixture3mf("flattened-slice.project_settings.config"), realPresets());
    expect(r).not.toBeNull();
    expect(r!.mismatches.map(formatMismatch)).toEqual([]);
  });

  it("FAIL: the old minis-04 slice, from the top preset files alone, is caught and names the keys", async () => {
    const r = await checkSliceCarriesPresets(fixture3mf("old-slice.project_settings.config"), realPresets());
    expect(r).not.toBeNull();
    const keys = new Set(r!.mismatches.map((m) => m.key));
    // The fallbacks the verification recorded (print-quality-verification.md §1.2).
    for (const k of [
      "elefant_foot_compensation",
      "top_shell_layers",
      "top_shell_thickness",
      "wall_generator",
      "top_surface_pattern",
      "bottom_surface_pattern",
      "additional_cooling_fan_speed",
      "fan_min_speed",
      "hot_plate_temp",
      "sparse_infill_density",
      "line_width",
    ]) {
      expect(keys, k).toContain(k);
    }
    const efc = r!.mismatches.find((m) => m.key === "elefant_foot_compensation")!;
    expect(efc.actual).toBe("0");
    expect(efc.expected).toBe("0.15");
  });
});
