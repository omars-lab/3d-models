import { describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { previewPathFor, writePlatePreview } from "./threemf.js";

// The minis-01 run (2026-09-26) found the plate picture Bambu Studio draws stayed inside the 3MF,
// so looking before sending meant unzipping it. `slice plate` and `slice compose` now write it out.
describe("writePlatePreview", () => {
  const dir = mkdtempSync(join(tmpdir(), "bambu-preview-test-"));
  // Bytes a utf8 round-trip would mangle: the PNG signature, a NUL and bytes over 0x7f.
  const png = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0xff, 0xfe, 0x80]);

  function threemf(name: string, withPicture: boolean): string {
    const src = join(dir, `${name}-src`);
    mkdirSync(join(src, "Metadata"), { recursive: true });
    writeFileSync(join(src, "Metadata", "slice_info.config"), "<config/>\n");
    if (withPicture) writeFileSync(join(src, "Metadata", "plate_1.png"), png);
    const out = join(dir, `${name}.plate.3mf`);
    execFileSync("zip", ["-q", "-r", out, "Metadata"], { cwd: src });
    return out;
  }

  it("names the picture after the plate", () => {
    expect(previewPathFor("/b/plates/minis-01.plate.3mf")).toBe("/b/plates/minis-01.plate.preview.png");
  });

  it("copies the picture out byte for byte", async () => {
    const plate = threemf("with", true);
    const out = await writePlatePreview(plate);
    expect(out).toBe(previewPathFor(plate));
    expect(readFileSync(out!).equals(png)).toBe(true);
  });

  it("returns null and writes nothing when the 3MF has no picture", async () => {
    const plate = threemf("without", false);
    expect(await writePlatePreview(plate)).toBeNull();
    expect(existsSync(previewPathFor(plate))).toBe(false);
  });
});
