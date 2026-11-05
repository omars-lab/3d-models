---
date: 2026-11-05
produced-by: research subagent (Claude Opus 5.5), one pass. GitHub API and raw source reads of Graphify-Labs/graphify on its default branch v8 (latest release v0.9.102, 2026-11-03), two pages of docs.graphify.com, a read of this repo, bikar, qiyas and the FAQ tool's own audit. Nothing was installed and no downloaded code was run.
feeds:
  - docs/design/process/code-graph.md
  - docs/faq.md (the open FAQ candidates, and Omar's question "how do we have configurable facts per repo?")
---

# Would graphify stop our sessions re-searching the same facts?

**The question.** Graphify is a tool that reads a code base and builds a graph of it: which
function calls which, which file imports which. Could it answer the questions our Claude sessions
keep looking up again with grep? If so, how would we set it up across our repos?

**Short answer.** For one of the six facts it would. For two it might help a little. For three it
would not. The facts our sessions re-search are mostly "where is this setting, this constant, this
data key, this id" across repos, and graphify is built for "who calls this function". The design
that acts on this is [../design/process/code-graph.md](../design/process/code-graph.md).

**How to read this file.** Sources are S1, S2 and so on. Each is marked **READ** (I read the page
or the source file in this run) or **SNIPPET** (I only saw a summary). Facts from our own repos are
R1 to R8 at the end. Where I could not settle something from the source, I say so rather than guess.

## 1. What graphify is (raw findings)

### 1.1 Maturity and license

- **Repo facts, from the GitHub API (S1, READ).** Created 2026-04-03, about seven months ago.
  142,799 stars and 13,657 forks. 1,641 open issues and pull requests together (the repo page
  splits this as 727 issues and 914 pull requests, S2). Last push 2026-11-03. Main language Python.
  License Apache-2.0 per the API. The repo also ships a second license file, LICENSE-MIT, and the
  repo page shows both (S2).
- **Release pace (S1, READ).** v0.9.98 to v0.9.102 came out in five days (2026-10-30 to
  2026-11-03). It is still below version 1.0. The graph file carries a schema version "so
  integrations can detect incompatible format changes" (S3), which says the format still moves.
- **A paid product sits beside it (S3, READ).** "Graphify Cloud" is offered for "monorepo and
  cross-repo support", with a 14-day trial. The free tool still has cross-repo commands of its own
  (section 1.4). The README pushes the cloud product at the exact point we care about, so read its
  claims about the free tool's cross-repo reach with that in mind.

**What this means for us.** Very popular, very active, and changing fast. Expect breaking changes
between versions; pin a version if we try it.

### 1.2 What it reads, and which of our languages it covers

- **Code is parsed on the machine, no AI model needed (S3, READ).** It uses tree-sitter, a common
  parser library, for "~40 languages", and links "calls / imports / inherits / mixes_in" across
  files. "Code is parsed locally ... no LLM, nothing leaves your machine."
- **The list of code file types it knows (S4, READ, the source's own list).** It includes `.py`,
  `.ts`, `.tsx`, `.js`, `.json`, `.yaml`, `.sh` and many more. It does **not** include `.scad`
  (OpenSCAD), `.bkr` (naqsh) or Makefiles. Those files would be left out of the graph or, if forced
  in, parsed as the wrong language. The README warns that a wrong-language file "does not fail ...
  the graph looks populated while the real symbols are missing" (S3).
- **Docs.** `.md` is on its document list (S4). A local Markdown reader (S5, READ) picks up
  headings, links, wiki links and code spans. A code span like `` `Widget` `` or
  `` `src/mod.py::Widget` `` becomes a link to that symbol, but a bare name links "only on a unique
  match". On top of that, an optional "semantic pass" sends docs to an AI model (your Claude
  session, or a configured API key) to pull out concepts (S3, S6). That pass costs model tokens.
  `--code-only` or `GRAPHIFY_BACKEND=none` turns it off (S3).
- **Data JSON is skipped (S7, READ).** The JSON reader only builds nodes for config files
  (package.json, tsconfig.json and the like) or files with config keys such as `$schema`,
  `dependencies` or `$defs`. For anything else, its own comment says, it "Returns False for data
  JSON so it is skipped by the structural pass".
- **What a node is (S6, READ).** Each node has an id, a label, a file type (code, document, paper,
  image, rationale, concept) and a source file. Code nodes are files, classes, functions and
  methods. **I could not confirm that a module-level constant becomes a node**, in Python
  (`SCHEMA_VERSION = 3`) or in TypeScript (`export const X = ...`). The docs page on inputs does not
  list node kinds and says "parser coverage varies by construct" (S8, READ). Settling it needs one
  test build.
- **Comments.** Only comments marked `# NOTE:` or `# WHY:`, and ADR or RFC citations, become nodes
  (S3). A plain comment such as bikar's "connect arc bypasses tagSegments" does not.

### 1.3 How a Claude session would use it

- **A skill plus a CLI (S3, READ).** `uv tool install graphifyy` (two y's), then `graphify install`
  registers a `/graphify` skill for Claude Code. Queries: `graphify query "<question>"`,
  `graphify explain "<name>"` (a node and everything linked to it, with file and line),
  `graphify path A B` (how two things connect).
- **A name that matches several nodes is refused, not guessed (S3).** It lists the candidates and
  exits with code 3. No match is exit code 4.
- **An MCP server is optional (S3, S9, READ).** Its tools include query_graph, get_node,
  get_neighbors, god_nodes (the most connected nodes), shortest_path and graph_stats (S9). It says
  which commit the graph was built from and warns "graph may be stale" when the repo has moved on
  (S9).
- **A hook can steer sessions toward the graph (S3).** On Claude Code it fires before Grep, Glob
  and Read calls and nudges toward a graph query. A `--strict` install goes further and *denies*
  one Read or Grep per session until a graph query has been run. That is a strong change to how
  every session in a repo behaves.
- **Output files (S3).** A folder named graphify-out holds graph.json (the whole graph),
  GRAPH_REPORT.md (a summary) and graph.html (a clickable view).

### 1.4 Several repos in one graph

- **Two commands join graphs (S3, S10, READ).**
  `graphify merge-graphs a.json b.json --out merged.json` combines graphs one time.
  `graphify global add <graph.json> --as <tag>` adds a repo's graph to a standing combined graph in the home folder, at
  ~/.graphify/global-graph.json, with a list of the repos in it (S11, READ). Every node id gets the
  repo's tag as a prefix, so the same name in two repos stays two nodes. Re-adding a repo first
  removes that repo's old nodes. A repo whose graph file has not changed is skipped.
- **What the combined graph records about each repo (S11).** Its path, its node and edge counts,
  when it was added and a hash of its graph file. It does **not** record the source commit. Each
  repo's own graph.json does record "built_at_commit" (S9, S12, READ), so the commit is known per
  repo but is not carried into the combined list.
- **Links across repos: only two narrow kinds (S13, S14, READ).**
  1. *A method call whose object's type lives in another repo* (S13). The repo-local build parks the
     call, and the merge finishes it when the type has exactly one declaration elsewhere. This works
     for C++, C#, Go, Java, Kotlin, Objective-C, Swift, PHP and TypeScript/JavaScript. **Python is
     not on the list**, so a 3d-models Python gate that calls into bikar gets no cross-repo edge.
  2. *The same type declared in two repos* (S14), matched on namespace plus name, added as a
     "same_type_as" link. It was built for .NET services sharing event classes. Whether a JSON
     Schema `$defs` entry, or a TypeScript type with no namespace, counts as "a type declaration
     carrying a namespace" I could not settle from the source.
- **Nothing links a setting to what it points at.** An environment variable read
  (`os.environ.get("BIKAR_DIR")`, `process.env.BIKAR_DIR`) is a string, not a symbol, and the
  engine source has no handling for environment variables (S15: zero matches for `process.env` or
  `os.environ`). A file copied byte for byte into another repo gets no link either; neither pass
  compares file contents.

### 1.5 How it stays current

- **Only changed files are re-read (S3).** `graphify update .` or `/graphify . --update`.
- **Git hooks (S12, READ, the source).** `graphify hook install` adds post-commit, post-checkout,
  post-merge and post-rewrite hooks, plus a merge driver for graph.json. The docs page on team use
  (S16, READ) still says there is no checkout hook; the source has one, so the page is out of date.
- **The hooks follow `core.hooksPath` (S12).** This repo sets that to `.githooks`, which is checked
  in. So `graphify hook install` here would append graphify's code to our committed hook files. That
  needs care.
- **The hooks skip linked worktrees (S12).** The source names `.claude/worktrees/` on purpose: a
  commit made inside a worktree does not rebuild the graph. Most of our session work happens in
  worktrees, so the graph in the main checkout would rebuild on `git pull` (post-merge) and branch
  switches there, not on each session's commits.
- **Sharing (S16).** The docs suggest committing only graph.json, with their union merge driver,
  and rebuilding the rest locally. With the post-commit hook, "the rebuilt graph [is left] as an
  uncommitted change", so for a committed graph they suggest a pre-commit hook instead.

### 1.6 Cost

- **Money: none for code (S3).** Code parsing makes no model calls. The docs pass uses your Claude
  session or an API key unless turned off.
- **No telemetry, but a local query log (S3).** Every query is logged to
  ~/.cache/graphify-queries.log. `GRAPHIFY_QUERY_LOG_DISABLE=1` turns it off.
- **Setup and upkeep.** Python 3.10 or newer, a uv or pipx install, hooks per repo, and a version to
  keep pinned while it releases every day or two.

### 1.7 Complexity and dependency cycles

- **Import cycles: yes (S17, S18, READ).** It finds files that import each other in a loop, up to 5
  files long, and lists them under "Import Cycles" in GRAPH_REPORT.md. Type-only imports are left
  out. I did not find an MCP tool or CLI query that returns this list on its own; it is in the
  report file.
- **Cyclomatic complexity: no.** I found no complexity measure in the source I read (analyze.py,
  report.py, cli.py, serve.py). It ranks the "most connected" nodes, which is how many things link
  to a function, not how many branches the function has.

### 1.8 Its own benchmark

- **One code result (S19, READ, graphify's own harness).** On ERPNext, a large Python repo, giving
  an agent one graphify tool raised "key-fact coverage" from 70.8% (grep and read) to 82.0%, "at
  about 140K tokens per query". It is six questions, run by the tool's makers. Treat it as a hint,
  not a measurement of our case.

## 2. The six facts, one by one

The six are the candidates in `docs/faq-proposal.md`. Five already have written answers in
`docs/faq.md` (Q-001 to Q-005, answered 2026-11-03). A graph query "answers" a fact here when
`graphify explain` or `query` would name the defining file and line, and what uses it, without a
grep.

| Fact (re-searched in N sessions) | Where it lives | Would a graph query answer it? | Why |
|---|---|---|---|
| SCHEMA_VERSION (5) | qiyas `src/qiyas/schema.py`, plus 14 other modules in qiyas that each set their own SCHEMA_VERSION (a grep, 2026-11-05); bikar's separate GT_SCHEMA_VERSION | **Partly, if constants are nodes** (not confirmed) | If they are, the "several matches" refusal lists all 15, which narrows it but leaves the pick. It cannot say which one is the contract, and nothing links it to bikar's GT_SCHEMA_VERSION (a different name). That judgment is what Q-001 holds. |
| BIKAR_DIR (4) | 3d-models Makefile, read by Python gates and the bambu tool via the environment | **No** | Makefiles are not parsed. The reads are strings (`os.environ.get("BIKAR_DIR")`), not symbols. And the fact that matters, "this points at the bikar checkout", is a cross-repo hop neither cross-repo pass makes. |
| patternSources (4) | bikar `packages/web/public-surface.json`, a key in a data file | **No** | That file has no config keys at the top (its keys are readme, hosts and so on), so the JSON reader skips it. The test that checks the count reads it as a property name in a string path. |
| tagSegments (4) | bikar `packages/core/src/dsl/environment.ts`, a method | **Yes** | A method with callers is exactly what the graph is for. `explain tagSegments` would give the file, the line and the callers. The one exception, connect arc going around it, is a plain comment, so the FAQ still says more. |
| FILL_ATTRIBUTES (3) | bikar `packages/core/src/dsl/parser.ts`, a private static set on the parser class | **Partly, if class fields are nodes** (not confirmed) | It might show the field and the class. The useful part of Q-005, that adding a word also touches two other places, is design knowledge no graph holds. |
| UCN, the use-case ids (3) | `.claude/skills/maintain-use-cases/use-cases.md` (a Mermaid block and table rows) and bikar `packages/lab/src/catalog.ts` (`uc: 'UC23'`) | **No** | "UC23" is a string in a diagram, a table cell and an object value. It is not a heading, function or type anywhere, so it is not a node. |

**Count:** one yes, two partly (both resting on something I could not confirm), three no.

## 3. How it compares with what we already have

| Tool | Better than graphify at | Worse than graphify at |
|---|---|---|
| **Plain grep** | Finds any string anywhere: settings, data keys, ids, Makefiles, OpenSCAD, naqsh. Always current. Nothing to install. Already used for all six. | Does not know callers from mentions. A grep for a common name returns noise. Each session pays the search again. |
| **The FAQ** (`docs/faq.md`) | Holds the *why*: which SCHEMA_VERSION is the contract, that FILL_ATTRIBUTES needs two more edits, that BIKAR_DIR's twin is THREED_MODELS_DIR. Its pointers are checked against the code, so drift is caught. It is measured. | Hand-written, so each answer costs a person's time. Covers only what has already been re-searched three times. |
| **CLAUDE.md and memory** | Loaded into every session without a query. Best for rules and traps. | Too small for every symbol. Memory is per repo. |
| **Graphify** | Who calls this function, what imports this file, how do these two things connect, for TypeScript and Python code. Updates itself. Can join repos. | Cannot see our settings, data keys, ids, Makefiles, OpenSCAD or naqsh. Cross-repo links are narrow and skip Python. Holds no *why*. A new tool and a new hook in every repo, still before version 1.0. |

**The case where it does not help, said plainly.** Five of the six facts are not "who calls this
function" questions. They are "where is this setting, constant, data key or id, and which one
matters". Our grep already finds them in one command; what the sessions lacked was the *answer*,
which is what the FAQ now holds. Graphify would not have prevented five of the six.

**One more measurement (R1).** The FAQ tool's audit, run today, marks all five answers "ANSWER NOT
TAKING": in the one session since 2026-11-03 that looked, each fact was searched again. One session
is far too few to judge, but it does say the FAQ alone is not reaching sessions yet. The likely
reason is delivery, not content: nothing points a session at the FAQ before it greps. That is a
cheaper fix than a new tool (see the design doc).

## 4. One graph across our five repos

**Can it build one graph from 3d-models, bikar, qiyas, youtube and sacred-patterns?** Yes, by
joining: build each repo's graph on its own, then `graphify global add` each one (S11) or run
`merge-graphs` once (S10). One query can then span all five.

**Does it link a use in one repo to the definition in another?** Not for our two examples.

| Our cross-repo link | What graphify does with it | Why |
|---|---|---|
| 3d-models gates read BIKAR_DIR to find bikar | Nothing | Environment reads are strings; no pass follows them (S15). The gates are Python, and the cross-repo call pass skips Python (S13). |
| qiyas exports a schema that bikar copies byte for byte | Nothing, as far as I can tell | Neither pass compares file contents. The "same type" pass (S14) needs a type declaration with a namespace; whether a JSON Schema `$defs` entry counts is unsettled. |
| A bikar TypeScript class used from another TypeScript repo | A cross-repo call edge, when the type has exactly one declaration (S13) | This is the case the pass was built for. Few of our cross-repo links look like this. |

**The smallest addition that would link them (an idea, not built).** A short script run after the
merge that adds edges graphify does not make:

1. *Setting edges*: for each name in a small list (BIKAR_DIR, THREED_MODELS_DIR and similar), grep
   the repos for where it is set and where it is read, and add a "reads setting" edge from each read
   to the place it is set.
2. *Copy edges*: for files that are byte-identical across repos (the schema and its copy), add a
   "copy of" edge.
3. *Or reuse what we already check*: the use-case map's anchored pointers (R7) already name
   "this use, that definition" across repos and are gated. Turning each into an edge would put
   our checked links into the graph without a second list to keep.

The merged graph is plain node-link JSON (S6), so adding edges is a small edit. The catch: a
re-merge replaces the file, so the script must run after every merge.

## 5. Where the graph could live

Every option below can span repos, because spanning comes from joining the graphs (section 4), not
from where the files sit. What differs is how the graph keeps up, and whether a session in a
worktree sees a fresh one.

| Option | How it stays in sync | One query across repos? | Cost |
|---|---|---|---|
| **(c) Nothing stored: build locally** into a folder git ignores, rebuild from a hook or by hand | graphify's own way (S3, S16). Hooks rebuild on commit, pull and branch switch, but skip worktrees (S12), so in practice it rebuilds on `git pull` in the main checkout. The combined graph in the home folder is re-added per repo. | Yes, through ~/.graphify/global-graph.json | Lowest. Nothing in git. Each machine builds its own. Our cross-repo edge script runs locally after each re-add. |
| **(b) One central repo, one folder per source repo, one branch** | Same local build, then a step copies each graph.json (which carries built_at_commit, S12) and the combined graph into the central repo and commits. | Yes, and the combined graph is versioned | Medium. A new repo to keep, a copy-and-commit step, and graph files of a few MB churning in git. Buys history ("what did the graph say last week") and sharing across machines. |
| **(a) One central repo, one branch per source repo** | As (b), but each repo's graph lands on its own branch with its source commit recorded. | Only after checking out every branch and merging them, which graphify has no support for | Highest, for nothing (b) lacks. Graphify has no notion of a branch per repo; the commit is already inside each graph.json. |

**On the cross-repo case first:** (c) and (b) both give one query across all five repos. (a) makes
it harder. The cross-repo *links* we need come from our own script in every option.

## 6. Omar's question: configurable facts per repo

Graphify has a per-repo settings file, `.graphifyrc`, but it holds tool settings (which language an
extension means, query depth, display limits; S3), not facts. Graphify has no place for "facts this
repo wants every session to know". Our own pieces already do that: the FAQ (with anchored pointers),
CLAUDE.md and memory. The design doc proposes how to make that per repo.

## 7. Recommendation

**Try it on bikar only, for a set time, without the strict hook, and measure.** Do not adopt it across
the repos yet.

| Choice | Pros | Cons | What it leads to |
|---|---|---|---|
| **Try on bikar** (recommended) | bikar is TypeScript, the one language where graphify is strong and cross-repo calls work. The one clear "yes" (tagSegments) lives there. Cheap: no model cost for code, one install. | Two weeks of a new tool. Its hooks skip our worktrees, so the graph is refreshed by hand or on pull. | A measured answer: did bikar sessions grep less for code symbols? If yes, add qiyas and the combined graph next. If no, remove it with `graphify uninstall --purge`. |
| **Adopt across all five repos now** | One graph to ask about everything. | Most of our re-searched facts are invisible to it. Hooks would write into our checked-in `.githooks`. A strict hook would change every session before we know it helps. | A lot of upkeep for one fact in six; hard to tell later whether it helped. |
| **Skip** | Nothing new to run. The FAQ keeps doing the job it was built for. | We never find out whether code-symbol lookups, a different kind than the six, get cheaper. | The FAQ's delivery problem still needs fixing either way. |

**Setup steps, if we try it** (for the trial; nothing here has been run):

1. `uv tool install graphifyy==0.9.102` (pinned).
2. In the main bikar checkout: `graphify extract . --code-only` with `GRAPHIFY_BACKEND=none`, so
   no model is called and only code goes in.
3. Add graphify-out to bikar's local exclude file (.git/info/exclude), not to any tracked file.
4. Do not run `graphify install --strict` or `graphify hook install` in the trial. Refresh with
   `graphify update .` after each pull.
5. Tell sessions about it in one line of bikar's CLAUDE.md: "for who-calls or who-imports questions,
   try `graphify explain <name>` first".
6. After two weeks, re-run `tools/session_reflect.py update-faq` and compare (the design doc's
   validator).

## Sources

- S1 GitHub API, repos/Graphify-Labs/graphify, releases and commits. READ.
- S2 https://github.com/Graphify-Labs/graphify (repo page). READ (via a page summary).
- S3 https://github.com/Graphify-Labs/graphify/blob/v8/README.md. READ, full text.
- S4 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/detect.py (the code and document extension lists). READ.
- S5 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/extractors/markdown.py (header and patterns). READ.
- S6 https://github.com/Graphify-Labs/graphify/blob/v8/docs/how-it-works.md (the graph format) and https://github.com/Graphify-Labs/graphify/blob/v8/graphify/skills/agents/references/extraction-spec.md. READ.
- S7 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/extractors/json_config.py. READ.
- S8 https://docs.graphify.com/concepts/supported-inputs. READ (via a page summary).
- S9 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/serve.py (tool list, staleness line). READ, the parts named.
- S10 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/cli.py (merge-graphs and global commands). READ, the parts named.
- S11 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/global_graph.py. READ, full.
- S12 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/hooks.py. READ, the install function, the worktree guard and the hooksPath handling.
- S13 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/cross_repo_calls.py. READ, the header and language list.
- S14 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/cross_repo_types.py. READ, the header.
- S15 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/extractors/engine.py. Searched, not read in full (11,364 lines).
- S16 https://docs.graphify.com/guides/team-workflows. READ (via a page summary).
- S17 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/analyze.py (find_import_cycles). READ, the function.
- S18 https://github.com/Graphify-Labs/graphify/blob/v8/graphify/report.py (Import Cycles section). READ, the section.
- S19 https://github.com/Graphify-Labs/graphify/blob/v8/BENCHMARKS.md. READ, the code section.

## Our repos

- R1 `python3 tools/session_reflect.py show --audit` over the 3d-models and bikar transcripts, run
  2026-11-05: all five FAQ entries "ANSWER NOT TAKING", pre 4 or 5 of 28 sessions, post 1 of 1.
- R2 `docs/faq-proposal.md`, `docs/faq.md`, `docs/faq-evidence.jsonl`,
  `docs/issues/faq-counted-use-not-rederivation.md`: the six candidates and how they are counted.
- R3 bikar `.eslintrc.cjs`: `complexity: ['error', { max: 10 }]`, no grace list; warn-only for
  scripts and Pages functions.
- R4 bikar `package.json`: `npm run ci` runs `import-graph`, which is `madge --circular` over five
  packages. bikar already fails its CI on an import cycle.
- R5 qiyas `pyproject.toml`: ruff C901 at max-complexity 10, with a per-file grace list.
- R6 3d-models has no complexity lint for its Python (`tools/`, `.claude/gates/`).
- R7 3d-models already holds cross-repo links by hand, checked: the use-case map's anchored
  pointers (`repo:path:Lnn "literal"`), `.claude/gates/schema_mirror.py` (qiyas schema vs bikar's
  copy) and `.claude/gates/contract_mirror.py` (sacred-patterns vs the two prose copies).
- R8 bikar `packages/web/public-surface.json` top-level keys start with readme and hosts; no
  `$schema`, `dependencies` or `$defs`.
