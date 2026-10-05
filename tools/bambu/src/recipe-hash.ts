// A plate recipe's hash, the same one the approvals and the send read.
//
// The send compares a slice's recipe hash with the recipe's now (slice-fresh.ts), and both come from
// iterations.py's `hash_text` (manage-approvals skill): the first 12 hex of sha256 over the recipe's
// YAML content as canonical JSON, keys sorted, no spaces, non-ASCII escaped. So a comment edit is not
// a change. The order planner keys its frozen slices by the recipes it writes, which have no page
// yet, so it cannot ask plate_approve.py; this is the same rule in TypeScript, and
// recipe-hash.test.ts runs both on the same texts so they cannot drift apart.
//
// Where the two could differ, and why it does not reach a recipe the planner writes: python keeps a
// YAML `1.0` a float and prints "1.0", JavaScript prints "1". The planner writes numbers from
// JavaScript, so it never writes `1.0`.

import { createHash } from "node:crypto";
import { parse as parseYaml } from "yaml";
import { canonicalJson } from "./iteration.js";

/** The recipe hash of a YAML text, or null when it is not YAML or is empty (as iterations.py). */
export function recipeHash(text: string): string | null {
  let doc: unknown;
  try {
    doc = parseYaml(text);
  } catch {
    return null;
  }
  if (doc === null || doc === undefined) return null;
  const canon = canonicalJson(doc).replace(/[\u0080-￿]/g, (c) => `\\u${c.charCodeAt(0).toString(16).padStart(4, "0")}`);
  return createHash("sha256").update(canon, "utf8").digest("hex").slice(0, 12);
}
