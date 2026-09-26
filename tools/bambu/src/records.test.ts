import { describe, expect, it, beforeEach, afterEach } from "vitest";
import { mkdtempSync, rmSync, readFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { scaffoldRecord } from "./records.js";

// Hermetic: scaffold into a temp dir and point BIKAR_DIR at nothing so bikarHead()/bikarBlobSha()
// return null (→ TODO pins) instead of shelling to the sibling repo. We are testing the record's
// YAML emission — the actuals block and the raw-frame sidecar — not bikar provenance (that is R1's
// job and the prints gate's).
describe("scaffoldRecord — capture writes an actuals block + raw frame", () => {
  let base: string;
  let savedBikar: string | undefined;

  beforeEach(() => {
    base = mkdtempSync(join(tmpdir(), "bambu-rec-"));
    savedBikar = process.env.BIKAR_DIR;
    process.env.BIKAR_DIR = join(base, "no-such-bikar");
  });
  afterEach(() => {
    if (savedBikar === undefined) delete process.env.BIKAR_DIR;
    else process.env.BIKAR_DIR = savedBikar;
    rmSync(base, { recursive: true, force: true });
  });

  it("emits the actuals: block with the filled fields and the provenance pointers", async () => {
    const dir = await scaffoldRecord({
      slug: "eggs-2x3",
      plateName: "eggs-2x3",
      plateFile: "eggs-2x3",
      objects: [{ entry: "obj-1", source: "bikar:TODO" }],
      date: "2026-09-21",
      baseDir: base,
      via: "bambu print capture",
      capture: {
        actuals: { state: "RUNNING", progress_pct: "42", layer: "51 / 120", chamber_c: "28" },
        capturedAt: "2026-09-21T10:15:00.000Z",
        rawFrame: { gcode_state: "RUNNING", mc_percent: 42, subtask_name: "eggs-2x3" },
      },
    });
    const md = readFileSync(join(dir, "index.md"), "utf8");
    expect(md).toContain("actuals:");
    expect(md).toContain("source: mqtt-device-report");
    expect(md).toContain("raw: device-report.json");
    expect(md).toContain('captured_at: "2026-09-21T10:15:00.000Z"');
    expect(md).toContain('state: "RUNNING"');
    expect(md).toContain('layer: "51 / 120"');
    // A field the builder left unconfirmed/absent is simply not emitted — no fabricated number.
    expect(md).not.toContain("filament_g");
    // The closing note names the capturing verb, not the dispatch one.
    expect(md).toContain("bambu print capture");
  });

  it("persists the verbatim device report beside index.md, round-tripping as JSON", async () => {
    const dir = await scaffoldRecord({
      slug: "eggs-2x3",
      plateName: "eggs-2x3",
      plateFile: "eggs-2x3",
      objects: [{ entry: "obj-1", source: "bikar:TODO" }],
      date: "2026-09-21",
      baseDir: base,
      via: "bambu print capture",
      capture: {
        actuals: { state: "FINISH" },
        capturedAt: "2026-09-21T10:15:00.000Z",
        rawFrame: { gcode_state: "FINISH", mc_percent: 100 },
      },
    });
    const raw = join(dir, "device-report.json");
    expect(existsSync(raw)).toBe(true);
    expect(JSON.parse(readFileSync(raw, "utf8"))).toEqual({ gcode_state: "FINISH", mc_percent: 100 });
  });

  it("writes no actuals block and no raw frame for a plain (non-capture) scaffold", async () => {
    const dir = await scaffoldRecord({
      slug: "plain",
      plateName: "plain",
      plateFile: "plain.3mf",
      objects: [{ entry: "obj-1", source: "bikar:TODO" }],
      date: "2026-09-21",
      baseDir: base,
    });
    const md = readFileSync(join(dir, "index.md"), "utf8");
    expect(md).not.toContain("actuals:");
    expect(existsSync(join(dir, "device-report.json"))).toBe(false);
    expect(md).toContain("bambu print send --record"); // the default verb note
  });

  it("names the plate's .3mf and leaves every object a verdict to fill (R10, R15)", async () => {
    const dir = await scaffoldRecord({
      slug: "pair",
      plateName: "pair",
      plateFile: "/x/build/plates/pair.plate.3mf",
      objects: [
        { entry: "c1", source: "bikar:a.bkr", params: { size: 40 } },
        { entry: "c2", source: "bikar:b.bkr", count: 2 },
      ],
      date: "2026-09-26",
      baseDir: base,
    });
    const md = readFileSync(join(dir, "index.md"), "utf8");
    expect(md).toContain('plate_3mf: "pair.plate.3mf"');
    expect(md.match(/ {4}verdict: "TODO"/g)).toHaveLength(2); // one per piece, not one per plate
    expect(md.match(/ {4}notes: \[\]/g)).toHaveLength(2);
  });
});
