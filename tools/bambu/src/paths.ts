// Shared path resolution. The record scaffolder and `validate record` MUST agree on where drafts
// live, so both resolve the staging dir from the repo root, not from the current cwd (the CLI is
// often run from tools/bambu). One helper, one answer.

import { existsSync } from "node:fs";
import { dirname, join } from "node:path";

/** Walk up from `start` to the repo root — the dir that holds .claude/gates/prints_gate.py. */
export function repoRoot(start = process.cwd()): string | null {
  let dir = start;
  for (let i = 0; i < 8; i++) {
    if (existsSync(join(dir, ".claude", "gates", "prints_gate.py"))) return dir;
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

/** The gitignored staging dir where `--record` scaffolds land. Repo-root/.bambu/records, else cwd. */
export function recordsDir(): string {
  const root = repoRoot();
  return join(root ?? process.cwd(), ".bambu", "records");
}
