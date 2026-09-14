// Backend: the bikar CLI (sibling repo) — mesh validation + blob provenance.
//
// bikar is the geometry engine and producer of record; this repo consumes it, never reimplements it
// (project CLAUDE.md). We shell to the same CLI the Makefile's `orbs` target uses —
//   node <bikar>/packages/cli/dist/index.js render <src.bkr> --format stl --check
// — so `validate mesh` runs bikar's own min-strut/FDM check, and we read blob hashes from the bikar
// checkout the same way the prints gate does, so a `--record` scaffold pins provenance the gate will
// later re-verify (the gate is the authority; this is a convenience).

import { existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { homedir } from "node:os";
import { join } from "node:path";
import { runWithTimeout } from "../log.js";

/** The bikar checkout dir: BIKAR_DIR env, else the repo convention ~/Workspace/git/bikar. */
export function bikarDir(): string {
  return process.env.BIKAR_DIR ?? join(homedir(), "Workspace", "git", "bikar");
}

/** The built bikar CLI entrypoint, or null if bikar isn't checked out / built. */
export function locateBikarCli(): string | null {
  const cli = join(bikarDir(), "packages", "cli", "dist", "index.js");
  return existsSync(cli) ? cli : null;
}

/** Is the bikar sibling a git checkout we can read blobs from? */
export function bikarIsCheckedOut(): boolean {
  return existsSync(join(bikarDir(), ".git"));
}

/**
 * sha256 of a bikar-tracked blob at a git ref (e.g. "HEAD", a commit sha), or null if unreadable.
 * bikar sources are text (.bkr), so the utf8 round-trip is lossless; the prints gate recomputes from
 * raw bytes at commit time and is the final authority on identity (R1).
 */
export async function bikarBlobSha(ref: string, path: string): Promise<string | null> {
  if (!bikarIsCheckedOut()) return null;
  const res = await runWithTimeout(
    "git",
    ["-C", bikarDir(), "cat-file", "-p", `${ref}:${path}`],
    { timeoutMs: 15_000, label: "bikar_cat" },
  );
  if (res.code !== 0 || res.timedOut) return null;
  return createHash("sha256").update(Buffer.from(res.stdout, "utf8")).digest("hex");
}

/** The bikar commit a scaffold should pin (its current HEAD), or null if unreadable. */
export async function bikarHead(): Promise<string | null> {
  if (!bikarIsCheckedOut()) return null;
  const res = await runWithTimeout(
    "git",
    ["-C", bikarDir(), "rev-parse", "HEAD"],
    { timeoutMs: 10_000, label: "bikar_head" },
  );
  if (res.code !== 0 || res.timedOut) return null;
  return res.stdout.trim() || null;
}
