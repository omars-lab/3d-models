import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import {
  parseSlicerWarnings,
  classifyWarnings,
  ruleCovers,
  studioVersionFrom,
  hashFile,
  sidecarFreshness,
  sidecarPath,
  type Manifest,
  type SlicerWarning,
  type WarningsSidecar,
} from "./warnings.js";

// The REAL Plate-1 capture (BambuStudio 2.08.02.61, --debug 2, machine card): a version banner and
// two plain [warning] boilerplate lines that are NOT slicing warnings, plus the one by-design advisory
// on the 0.4 mm wall rung. The parser must pick out exactly the slicing warning and ignore the rest.
const REAL_DEBUG2_OUTPUT = `
[2026-09-17 15:04:04.159100] [0x1] [trace]   Initializing StaticPrintConfigs
[2026-09-17 15:04:04.166049] [0x1] [warning] cli mode, Current BambuStudio Version 02.08.02.61
[2026-09-17 15:04:04.170381] [0x1] [warning] no filament colors found in projects
[2026-09-17 15:04:04.207367] [0x1] [warning] plate 1: found NON_CRITICAL slicing warnings: It seems object MC2Wall04.stl has floating regions. Please re-orient the object or enable support generation.
`;

// The by-design manifest (the one shipped in .claude/gates), inlined so the test is hermetic.
const MANIFEST: Manifest = {
  rules: [
    {
      object: "^MC2Wall04\\b",
      message: "floating regions",
      severity: "non_critical",
      reason: "sub-floor 0.4 mm rung, fails by design",
      settles: "CAL-FEA-01",
    },
  ],
};

describe("parseSlicerWarnings", () => {
  it("extracts the by-design advisory and ignores plain [warning] boilerplate", () => {
    const ws = parseSlicerWarnings(REAL_DEBUG2_OUTPUT);
    expect(ws).toHaveLength(1);
    expect(ws[0]!.severity).toBe("non_critical");
    expect(ws[0]!.plate).toBe(1);
    expect(ws[0]!.object).toBe("MC2Wall04.stl");
    expect(ws[0]!.message).toContain("floating regions");
  });

  it("treats the version banner, no-filament-colors, and preset-not-found lines as NOT warnings", () => {
    // These are the re-slice / boilerplate [warning] lines — none is a `found … slicing warnings:` line.
    const boilerplate = `
[warning] cli mode, Current BambuStudio Version 02.08.02.61
[warning] no filament colors found in projects
[warning] run:2873, can not find system preset file: /a/b/Bambu Lab X2D 0.4 nozzle.json
`;
    expect(parseSlicerWarnings(boilerplate)).toHaveLength(0);
  });

  it("classifies a warning as critical when the NON_CRITICAL marker is absent, and trims no_check", () => {
    const line = `[warning] plate 2: found slicing warnings: object Foo.stl is not printable, no_check=0`;
    const ws = parseSlicerWarnings(line);
    expect(ws).toHaveLength(1);
    expect(ws[0]!.severity).toBe("critical");
    expect(ws[0]!.plate).toBe(2);
    expect(ws[0]!.message).toBe("object Foo.stl is not printable");
    expect(ws[0]!.message).not.toContain("no_check");
  });

  it("splits a multi-object line into one warning per object", () => {
    const line = `[warning] plate 1: found NON_CRITICAL slicing warnings: object A.stl has floating regions. object B.stl has floating regions.`;
    const ws = parseSlicerWarnings(line);
    expect(ws.map((w) => w.object)).toEqual(["A.stl", "B.stl"]);
  });
});

describe("classifyWarnings", () => {
  it("clears the by-design MC2Wall04 floating-regions advisory as EXPECTED", () => {
    const ws = parseSlicerWarnings(REAL_DEBUG2_OUTPUT);
    const c = classifyWarnings(ws, MANIFEST);
    expect(c.unexpected).toHaveLength(0);
    expect(c.expected).toHaveLength(1);
    expect(c.expected[0]!.rule.settles).toBe("CAL-FEA-01");
  });

  it("BLOCKS an unexpected warning the manifest does not cover (the load-bearing case)", () => {
    // A different object floating is NOT whitelisted — a real regression the gate must catch.
    const surprise: SlicerWarning = {
      severity: "non_critical",
      plate: 1,
      object: "StarOrb.stl",
      message: "It seems object StarOrb.stl has floating regions.",
      raw: "…",
    };
    const c = classifyWarnings([surprise], MANIFEST);
    expect(c.expected).toHaveLength(0);
    expect(c.unexpected).toHaveLength(1);
    expect(c.unexpected[0]!.object).toBe("StarOrb.stl");
  });

  it("a critical warning on the whitelisted object is still UNEXPECTED (severity is constrained)", () => {
    const criticalOnWall: SlicerWarning = {
      severity: "critical",
      plate: 1,
      object: "MC2Wall04.stl",
      message: "object MC2Wall04.stl has floating regions",
      raw: "…",
    };
    // The rule only clears the NON_CRITICAL advisory; a CRITICAL error on the same object must block.
    expect(classifyWarnings([criticalOnWall], MANIFEST).unexpected).toHaveLength(1);
  });

  it("fails closed: an empty manifest classifies everything as unexpected", () => {
    const ws = parseSlicerWarnings(REAL_DEBUG2_OUTPUT);
    expect(classifyWarnings(ws, { rules: [] }).unexpected).toHaveLength(1);
  });
});

describe("ruleCovers", () => {
  it("a message-only rule (no object) covers only an object-less warning, never a by-object one", () => {
    const rule = { message: "bed adhesion", reason: "x" };
    const objectless: SlicerWarning = { severity: "non_critical", plate: null, object: null, message: "poor bed adhesion", raw: "" };
    const byObject: SlicerWarning = { severity: "non_critical", plate: 1, object: "A.stl", message: "poor bed adhesion", raw: "" };
    expect(ruleCovers(rule, objectless)).toBe(true);
    expect(ruleCovers(rule, byObject)).toBe(false);
  });

  it("a malformed regex in a rule covers nothing (fail closed, never throws)", () => {
    const bad = { object: "[", message: "floating", reason: "x" };
    const w: SlicerWarning = { severity: "non_critical", plate: 1, object: "A.stl", message: "floating regions", raw: "" };
    expect(ruleCovers(bad, w)).toBe(false);
  });
});

describe("studioVersionFrom", () => {
  it("pulls the version off the banner for the sidecar provenance", () => {
    expect(studioVersionFrom(REAL_DEBUG2_OUTPUT)).toBe("02.08.02.61");
  });
});

// Freshness: the sidecar binds its warnings to the exact .3mf bytes via source_sha256, so the dispatch
// gate can refuse a STALE sidecar (one sitting beside a .3mf it was not sliced from) — the real trap:
// a leftover capture beside a regenerated plate that would otherwise read as "clean".
describe("sidecarFreshness", () => {
  let dir: string;
  const plate = () => join(dir, "plate.3mf");
  const writeSidecar = (s: Partial<WarningsSidecar>) =>
    writeFileSync(
      sidecarPath(plate()),
      JSON.stringify({ tool: "test", sliced_at: "", studio_version: null, warnings: [], ...s }),
    );

  beforeAll(() => {
    dir = mkdtempSync(join(tmpdir(), "bambu-sidecar-"));
  });
  afterAll(() => {
    rmSync(dir, { recursive: true, force: true });
  });

  it("reports 'missing' when no sidecar is beside the plate", () => {
    writeFileSync(plate(), "MODEL-A");
    expect(sidecarFreshness(plate()).status).toBe("missing");
  });

  it("reports 'fresh' when source_sha256 matches the .3mf on disk", () => {
    writeFileSync(plate(), "MODEL-A");
    writeSidecar({ source_sha256: hashFile(plate())! });
    expect(sidecarFreshness(plate()).status).toBe("fresh");
  });

  it("reports 'stale' when the .3mf changed after the sidecar was written", () => {
    writeFileSync(plate(), "MODEL-A");
    writeSidecar({ source_sha256: hashFile(plate())! });
    writeFileSync(plate(), "MODEL-B"); // regenerated by a different pipeline; sidecar not refreshed
    expect(sidecarFreshness(plate()).status).toBe("stale");
  });

  it("reports 'unverifiable' for a legacy sidecar with no source_sha256", () => {
    writeFileSync(plate(), "MODEL-A");
    writeSidecar({}); // pre-freshness sidecar
    expect(sidecarFreshness(plate()).status).toBe("unverifiable");
  });
});
