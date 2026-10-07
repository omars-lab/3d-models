import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { mkdirSync, mkdtempSync, rmSync, utimesSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  type BedPhoto,
  type BedVerdict,
  bedCheck,
  bedDir,
  bedPhotoName,
  isPhotoOf,
  newestBedPhoto,
  readVerdict,
  writeVerdict,
} from "./bed-check.js";

// The bed check a real send runs (bed-check.ts). The load-bearing case is sheets-04b on 2026-10-03:
// the photo showed a Textured PEI Plate and the slice was for a Cool Plate. A verdict that says what
// the photo shows must stop that send.

const NOW = Date.parse("2026-10-03T20:00:00Z");
const photo: BedPhoto = { path: "/x/.bambu/bed/sheets-04b-2026-10-03T19-50-00-000Z.jpg", mtimeMs: NOW - 10 * 60000, sha256: "aa" };
const good: BedVerdict = {
  photo: "sheets-04b-2026-10-03T19-50-00-000Z.jpg",
  sha256: "aa",
  plate: "sheets-04b",
  bed_clear: true,
  plate_seated: true,
  plate_type: "textured_plate",
  by: "Claude, opened the photo",
  at: "2026-10-03T19:51:00Z",
};

describe("bedCheck", () => {
  it("passes a recent photo whose verdict says clear, seated, and the slice's plate", () => {
    const c = bedCheck("sheets-04b", photo, good, "textured_plate", NOW);
    expect(c.ok).toBe(true);
    expect(c.line).toContain("10 min old");
    expect(c.line).toContain("Textured PEI Plate");
  });

  it("refuses the sheets-04b case: a Textured PEI Plate seen, a Cool Plate slice", () => {
    const c = bedCheck("sheets-04b", photo, good, "cool_plate", NOW);
    expect(c.ok).toBe(false);
    expect(c.line).toContain("saw a Textured PEI Plate");
    expect(c.line).toContain("the slice is for a Cool Plate");
    expect(c.line).toContain("--plate-type textured_plate");
  });

  it("refuses with no photo, and names the command that takes one", () => {
    const c = bedCheck("sheets-04b", null, null, "textured_plate", NOW);
    expect(c.ok).toBe(false);
    expect(c.line).toContain("bambu bed photo sheets-04b");
  });

  it("refuses a photo nobody wrote a verdict for", () => {
    const c = bedCheck("sheets-04b", photo, null, "textured_plate", NOW);
    expect(c.ok).toBe(false);
    expect(c.line).toContain("nobody has written down");
  });

  it("refuses a photo over the age limit, and passes one exactly at it", () => {
    const old = { ...photo, mtimeMs: NOW - 31 * 60000 };
    expect(bedCheck("sheets-04b", old, good, "textured_plate", NOW).ok).toBe(false);
    expect(bedCheck("sheets-04b", old, good, "textured_plate", NOW).line).toContain("31 min old, over 30");
    const edge = { ...photo, mtimeMs: NOW - 30 * 60000 };
    expect(bedCheck("sheets-04b", edge, good, "textured_plate", NOW).ok).toBe(true);
  });

  it("refuses a verdict written for other photo bytes", () => {
    const c = bedCheck("sheets-04b", { ...photo, sha256: "bb" }, good, "textured_plate", NOW);
    expect(c.ok).toBe(false);
    expect(c.line).toContain("other photo bytes");
  });

  it("refuses a bed that is not clear, with the note", () => {
    const c = bedCheck("sheets-04b", photo, { ...good, bed_clear: false, note: "last print's purge line" }, "textured_plate", NOW);
    expect(c.ok).toBe(false);
    expect(c.line).toContain("purge line");
  });

  it("refuses a plate that is not seated", () => {
    const c = bedCheck("sheets-04b", photo, { ...good, plate_seated: false }, "textured_plate", NOW);
    expect(c.ok).toBe(false);
    expect(c.line).toContain("not seated");
  });
});

describe("isPhotoOf", () => {
  it("matches this plate's photos and not a plate whose name starts the same", () => {
    const name = bedPhotoName("sheets-04b", new Date(NOW));
    expect(name).toBe("sheets-04b-2026-10-03T20-00-00-000Z.jpg");
    expect(isPhotoOf("sheets-04b", name)).toBe(true);
    expect(isPhotoOf("sheets-04", name)).toBe(false);
    expect(isPhotoOf("sheets-04b", `${name}.verdict.json`)).toBe(false);
  });
});

describe("newestBedPhoto, writeVerdict, readVerdict", () => {
  let root: string;
  beforeAll(() => {
    root = mkdtempSync(join(tmpdir(), "bed-check-"));
    mkdirSync(bedDir(root), { recursive: true });
  });
  afterAll(() => rmSync(root, { recursive: true, force: true }));

  it("picks the newest photo by file time, writes a verdict bound to its bytes, and reads it back", () => {
    const older = join(bedDir(root), "sheets-04b-2026-10-03T19-00-00-000Z.jpg");
    const newer = join(bedDir(root), "sheets-04b-2026-10-03T19-50-00-000Z.jpg");
    const other = join(bedDir(root), "sheets-04-2026-10-03T19-55-00-000Z.jpg");
    writeFileSync(older, "old bytes");
    writeFileSync(newer, "new bytes");
    writeFileSync(other, "another plate");
    utimesSync(older, new Date(NOW - 60 * 60000), new Date(NOW - 60 * 60000));
    utimesSync(newer, new Date(NOW - 5 * 60000), new Date(NOW - 5 * 60000));
    utimesSync(other, new Date(NOW), new Date(NOW));

    const p = newestBedPhoto(root, "sheets-04b");
    expect(p?.path).toBe(newer);
    const { photo: _p, sha256: _s, ...rest } = good;
    writeVerdict(p!, rest);
    const v = readVerdict(newer);
    expect(v?.sha256).toBe(p!.sha256);
    expect(bedCheck("sheets-04b", p, v, "textured_plate", NOW).ok).toBe(true);

    // The photo changes after the look: the verdict no longer covers it.
    writeFileSync(newer, "a retaken photo");
    utimesSync(newer, new Date(NOW - 1 * 60000), new Date(NOW - 1 * 60000));
    const again = newestBedPhoto(root, "sheets-04b");
    expect(bedCheck("sheets-04b", again, readVerdict(newer), "textured_plate", NOW).ok).toBe(false);
  });

  it("keeps non_bambu on the verdict, so `options for-bed` knows the plate (D-108)", () => {
    const glacier = join(bedDir(root), "sld-1-2026-10-07T18-00-00-000Z.jpg");
    writeFileSync(glacier, "glacier bytes");
    const p = newestBedPhoto(root, "sld-1");
    const { photo: _p, sha256: _s, ...rest } = good;
    writeVerdict(p!, { ...rest, non_bambu: true });
    expect(readVerdict(glacier)?.non_bambu).toBe(true);
    writeVerdict(p!, rest);
    expect(readVerdict(glacier)?.non_bambu).toBeUndefined();
  });

  it("finds nothing for a plate with no photos", () => {
    expect(newestBedPhoto(root, "minis-01")).toBeNull();
  });
});
