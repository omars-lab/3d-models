import { describe, expect, it } from "vitest";
import { checkSliceFresh } from "./slice-fresh.js";

// The fresh-slice check a send runs (slice-fresh.ts). The hashes are plate_approve.py's; the
// end-to-end case against the real tool is in send-gate.test.ts.

describe("checkSliceFresh", () => {
  it("passes a slice made from the recipe as it is now", () => {
    expect(checkSliceFresh("0123456789ab", "0123456789ab")).toMatchObject({ ok: true, mark: "✓" });
  });

  it("refuses a slice made from an older recipe, and names both hashes", () => {
    const c = checkSliceFresh("0123456789ab", "ba9876543210");
    expect(c).toMatchObject({ ok: false, mark: "✗" });
    expect(c.line).toContain("sliced from 0123456789ab, now ba9876543210");
  });

  it("refuses a slice that recorded no recipe: it cannot be shown fresh", () => {
    expect(checkSliceFresh(undefined, "0123456789ab")).toMatchObject({ ok: false, mark: "✗" });
  });

  it("warns, not refuses, when the plate has no recipe to compare", () => {
    expect(checkSliceFresh(undefined, null)).toMatchObject({ ok: true, mark: "⚠" });
  });
});
