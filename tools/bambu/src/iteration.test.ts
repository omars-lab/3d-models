import { describe, expect, it } from "vitest";
import { canonicalize, canonicalJson, iterationId, type IterationKey } from "./iteration.js";

// The iteration id is the join key three views share (manifest item, reprint verb, metrics). These
// pin the ONE property that makes that safe: the same recipe hashes to the same id regardless of how
// its fields were authored, and any change to the recipe changes the id (print-metadata design §2.2).

function key(over: Partial<IterationKey> = {}): IterationKey {
  return {
    source: "bikar:patterns/Orbs/foo.bkr@abc123",
    source_sha256: "a".repeat(64),
    piece: "Orb",
    params: { size: 40, twist: 12 },
    slice_profile: { settings: "X2D;0.20 Std", filament: "PLA Basic" },
    ...over,
  };
}

describe("canonicalize — deterministic key order", () => {
  it("sorts object keys recursively while preserving array order", () => {
    const a = canonicalize({ b: 1, a: { d: 4, c: 3 }, list: [3, 1, 2] });
    expect(JSON.stringify(a)).toBe('{"a":{"c":3,"d":4},"b":1,"list":[3,1,2]}');
  });

  it("canonicalJson is order-independent for objects", () => {
    expect(canonicalJson({ x: 1, y: 2 })).toBe(canonicalJson({ y: 2, x: 1 }));
  });
});

describe("iterationId — content-addressed it-<sha12>", () => {
  it("is `it-` + exactly 12 lowercase hex", () => {
    expect(iterationId(key())).toMatch(/^it-[0-9a-f]{12}$/);
  });

  it("is stable regardless of param authoring order", () => {
    const a = iterationId(key({ params: { size: 40, twist: 12 } }));
    const b = iterationId(key({ params: { twist: 12, size: 40 } }));
    expect(a).toBe(b);
  });

  it("changes when the recipe changes", () => {
    const base = iterationId(key());
    expect(iterationId(key({ params: { size: 41, twist: 12 } }))).not.toBe(base);
    expect(iterationId(key({ piece: "Half" }))).not.toBe(base);
    expect(iterationId(key({ slice_profile: { settings: "X2D;0.28 Draft", filament: "PLA Basic" } }))).not.toBe(base);
    expect(iterationId(key({ source_sha256: "b".repeat(64) }))).not.toBe(base);
  });
});
