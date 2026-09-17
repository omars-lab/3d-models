import { describe, expect, it } from "vitest";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { filamentMapModeEnum, filamentCount, injectFilamentMapMode } from "./slice.js";

// These lock in the X2D filament-grouping mechanism measured 2026-09-17 (see
// docs/issues/x2d-filament-grouping-mode.md). The live-slice acceptance (Studio honours the merged
// key, single filament collapses to one group) is proven in that doc; here we pin the pure logic the
// CLI owns because Studio does NOT validate it for us.

describe("filamentMapModeEnum — token → Studio enum literal", () => {
  it("maps the two auto modes to their exact enum strings", () => {
    expect(filamentMapModeEnum("saving")).toBe("Auto For Flush");
    expect(filamentMapModeEnum("quality")).toBe("Auto For Match");
  });

  it("is case- and whitespace-insensitive on the token", () => {
    expect(filamentMapModeEnum("  SAVING ")).toBe("Auto For Flush");
    expect(filamentMapModeEnum("Quality")).toBe("Auto For Match");
  });

  it("rejects an unknown token rather than letting Studio silently default it", () => {
    // Studio slices a bogus filament_map_mode at exit 0 and falls back to the default — so a typo must
    // fail here, loudly, not slice under the wrong grouping.
    expect(() => filamentMapModeEnum("bogus")).toThrow(/unknown --filament-map-mode/);
  });

  it("recognises `manual` but refuses it (needs an explicit filament_map array)", () => {
    expect(() => filamentMapModeEnum("manual")).toThrow(/manual needs an explicit/);
  });
});

describe("filamentCount — grouping only means something with ≥2 filaments", () => {
  it("counts a ';'-joined list, ignoring blanks", () => {
    expect(filamentCount(undefined)).toBe(0);
    expect(filamentCount("")).toBe(0);
    expect(filamentCount("a.json")).toBe(1);
    expect(filamentCount("a.json;b.json")).toBe(2);
    expect(filamentCount(" a.json ; ; b.json ;")).toBe(2);
  });
});

describe("injectFilamentMapMode — merge into the ONE process config", () => {
  function fixture(): { dir: string; machine: string; process: string } {
    const dir = mkdtempSync(join(tmpdir(), "fmm-test-"));
    const machine = join(dir, "machine.json");
    const process = join(dir, "process.json");
    writeFileSync(machine, JSON.stringify({ type: "machine", name: "X2D", printer_model: "X2D" }));
    writeFileSync(process, JSON.stringify({ type: "process", name: "0.20 Std", layer_height: "0.2" }));
    return { dir, machine, process };
  }

  it("merges the enum into the process JSON and leaves the machine JSON path untouched", () => {
    const { dir, machine, process } = fixture();
    const scratch = join(dir, "scratch");
    mkdirSync(scratch);
    const res = injectFilamentMapMode(`${machine};${process}`, "Auto For Flush", scratch);

    const parts = res.settings.split(";");
    // machine path passes through verbatim; process path is swapped for a merged temp copy
    expect(parts[0]).toBe(machine);
    expect(parts[1]).not.toBe(process);
    expect(res.mergedInto).toBe(process);

    // the merged copy carries the enum AND preserves the original process keys
    const merged = JSON.parse(readFileSync(parts[1] as string, "utf8")) as Record<string, unknown>;
    expect(merged.filament_map_mode).toBe("Auto For Flush");
    expect(merged.type).toBe("process");
    expect(merged.layer_height).toBe("0.2");

    // exactly one temp file was written into scratch (only the process config)
    expect(readdirSync(scratch)).toHaveLength(1);
  });

  it("throws when no process config is present (the enum has nowhere to live)", () => {
    const { dir, machine } = fixture();
    const scratch = join(dir, "scratch");
    mkdirSync(scratch);
    expect(() => injectFilamentMapMode(machine, "Auto For Flush", scratch)).toThrow(
      /needs a process preset/,
    );
  });
});
