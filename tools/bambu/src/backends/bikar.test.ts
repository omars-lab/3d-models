import { afterAll, describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { bikarRefOnMain } from "./bikar.js";

// minis-03's draft pinned bikar db68768a, a branch commit that bikar #251's squash merge replaced.
// It still read fine while the object sat in the local store, so nothing flagged it (2026-09-26).
// `slice compose` now warns when bikar HEAD is not on origin/main; the prints gate refuses (R16).
describe("bikarRefOnMain", () => {
  const repo = mkdtempSync(join(tmpdir(), "bikar-on-main-"));
  const git = (...args: string[]) =>
    execFileSync("git", ["-C", repo, ...args], {
      encoding: "utf8",
      env: { ...process.env, GIT_AUTHOR_NAME: "t", GIT_AUTHOR_EMAIL: "t@t", GIT_COMMITTER_NAME: "t", GIT_COMMITTER_EMAIL: "t@t" },
    }).trim();
  git("init", "-q");
  writeFileSync(join(repo, "a.bkr"), "a\n");
  git("add", "a.bkr");
  git("commit", "-q", "-m", "on main");
  const onMain = git("rev-parse", "HEAD");
  writeFileSync(join(repo, "a.bkr"), "b\n");
  git("commit", "-q", "-am", "branch only");
  const branchOnly = git("rev-parse", "HEAD");

  const saved = process.env.BIKAR_DIR;
  process.env.BIKAR_DIR = repo;
  afterAll(() => {
    if (saved === undefined) delete process.env.BIKAR_DIR;
    else process.env.BIKAR_DIR = saved;
  });

  it("is unknown when there is no origin/main to ask", async () => {
    expect(await bikarRefOnMain(onMain)).toBe("unknown");
  });

  it("is yes for a commit on origin/main and no for a branch commit past it", async () => {
    git("update-ref", "refs/remotes/origin/main", onMain);
    expect(await bikarRefOnMain(onMain)).toBe("yes");
    expect(await bikarRefOnMain(branchOnly)).toBe("no");
  });
});
