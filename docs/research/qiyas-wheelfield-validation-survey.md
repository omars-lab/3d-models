<!--
  Research produced 2026-08-15 by Claude Fable 5 (two parallel Explore
  sub-agents) under the 3d-models design-doc rules, for extending qiyas 3D
  validation to the wheelfield/maclado orb family so its three presets can
  become Orb Lab preset chips.
  Sources: DIRECT SOURCE-TREE READING of two local checkouts —
  `~/Workspace/git/qiyas` (working tree, master) and
  `~/Workspace/git/bikar-lego-lab` (bikar worktree, detached at merged main
  f3cb04ccd39e352896644df597594bd762f523db). No web sources; no external
  documentation was consulted. Every claim carries a file:line anchor into
  one of those two trees, valid at those revisions.
  Feeds: docs/qiyas-wheelfield-validation-design.md.
  WHAT WAS RUN: the bikar agent executed the built `packages/core/dist/index.js`
  IN MEMORY to measure view output (polygon counts, overlapping-pair counts,
  SVG SHA-256 equality across the three presets). Nothing was written to disk,
  no files were modified, no rasterizer was invoked, no mesh was generated, and
  no print was made. The qiyas agent read source and ran the parser on a
  synthetic in-memory SVG snippet to verify the `data-sides` coupling; it wrote
  nothing. Both reports are preserved verbatim below; the numbers they state as
  "measured" were measured by the run described here, and everything else is
  read from source.
-->

# Extending qiyas 3D validation to the wheelfield family — what exists, what is missing, and what breaks

*Research date: 2026-08-15. Scope: the facts a design doc needs in order to
specify validation for the maclado/wheelfield orb family (`base wheelfield`) —
how `qiyas orb-validate` works today, what bikar emits for orb views today, what
the wheelfield path actually emits, and which defects stand between a woven
ribbon lattice and a trustworthy composite score.*

---

## 0. Standing disclaimers, and the limits of this survey

- **This is a source survey of two checkouts at two specific revisions**, not a
  survey of published literature and not a survey of how other projects validate
  3D renders. Where a claim below says "no CI job does X" or "no consumer
  exists", it is a claim about **these two trees at these two revisions** and
  nowhere else. It was established by grep over the trees named in the
  provenance header, and it is stated with that scope rather than as a claim
  about the ecosystem.
- **qiyas was read at its local working-tree state on master**, which is one
  commit ahead of the `as_of` pin the use-case map carries for it. No revision
  hash is quoted for the qiyas half; a design doc that needs a stable qiyas
  anchor must pin one.
- **The two agents worked independently and did not cross-check each other.**
  Where their reports touch the same seam — the `data-*` attribute contract —
  they agree, and that agreement is the only cross-validation performed. Two
  numbers each side states about the other side (qiyas `SCHEMA_VERSION` 1.22 as
  recorded in bikar's contract mirror vs. 1.22 read from qiyas source; bikar
  `GT_SCHEMA_VERSION` 1.25 vs. the 1.24 recorded in a committed qiyas fixture)
  are consistent with a fixture baked before the 1.25 bump, but that
  reconciliation is inference, not something either agent verified.
- **Nothing here establishes that a wheelfield view SHOULD be validated the way
  a classic orb view is.** The survey records what the existing instrument
  measures and what it cannot see. Whether a centroid-and-area score over a cell
  decomposition is an adequate claim about a woven object is a design judgment
  the design doc must make and defend, not a finding of this survey.
- **The "measured" numbers are single-run measurements** of deterministic
  geometry code executed in memory. They were not re-run independently, and no
  tolerance sweep was performed on any of them.

---

## 1. Report A — qiyas: how orb validation works today

*Produced by the qiyas Explore agent against `~/Workspace/git/qiyas` (working
tree, master). Preserved verbatim.*

### Orb Validation in qiyas — Current-State Map

Repo: `/Users/omareid/Workspace/git/qiyas`. All anchors are `absolute-path:line`. Nothing was modified.

---

#### 1. The `orb-validate` CLI command

**Definition:** `/Users/omareid/Workspace/git/qiyas/src/qiyas/cli.py:3000-3087` (`@main.command(name="orb-validate")`, function `orb_validate` at :3034). It is the **last** command in `cli.py`.

**Arguments / options** (`cli.py:3001-3033`):

| Surface | Anchor | Notes |
|---|---|---|
| `VIEWS_DIR` (positional, required, must exist, dir-only) | `cli.py:3001-3004` | bikar `--format views` output dir |
| `--recon-dir` (dir, default `None`) | `cli.py:3005-3015` | optional external recon images |
| `--output-dir` / `-d` (default `./out-orb`) | `cli.py:3016-3022` | |
| `--threshold` (FloatRange 0..1, **default 0.95**) | `cli.py:3023-3028` | |
| `--verbose` (flag) | `cli.py:3029-3033` | includes `primitives` in written encodings |

**What it consumes.** Per view it needs **both** an SVG render and a bikar `gt.json`, paired by filename stem:
- Discovery: `/Users/omareid/Workspace/git/qiyas/src/qiyas/orb_validate.py:95-165` — globs `*.gt.json`, requires a sibling `<stem>.svg`.
- Stem regex: `orb_validate.py:63` — `^(?P<orb>.+)\.(?P<view>[a-z]+-\d+)$`. **View kind must be lowercase-alpha + `-` + digits** (`vertex-5`, `face-3`, `edge-2`). A new orb family that wants a different view naming (e.g. `ribbon_axis-3`, `Weave-3`) will trip `unrecognized-view-stem` (error severity, `orb_validate.py:112-122`).
- SVG is encoded through the **standard 2D pipeline**: `orb_validate.py:394` (`from .pipeline import encode_image`) and `:403` (`encode_image(view.svg_path, verbose=verbose)`).
- **gt.json is read raw via `json.load`, never as a qiyas `Encoding`** — deliberate, documented at `orb_validate.py:13-17` and executed at `:402`.

**Per-view → composite aggregation** (`orb_validate.py:466-478`):
```
composites      = [r.scores.composite for r in results]
composite       = mean(composites)            # unweighted arithmetic mean
min_view_composite = min(composites)
passed          = bool(composites) and composite >= threshold and not has_errors
```
`min_view_composite` is **reported but NOT gated** (`orb_validate.py:468, 475`) — a single catastrophic view can be masked by good siblings.

**Per-view composite formula** (`orb_validate.py:240`):
```
composite = W_STRUCTURAL*structural + W_GEOMETRIC*geometric + W_SYMMETRY*symmetry
```
Weights are imported from the 2D scorer (`orb_validate.py:199`) and defined at `/Users/omareid/Workspace/git/qiyas/src/qiyas/diff/scorer.py:94-96`: `W_STRUCTURAL = 0.4`, `W_GEOMETRIC = 0.35`, `W_SYMMETRY = 0.25`. Same line as the 2D composite at `scorer.py:789`. Values are rounded to 4 dp (`orb_validate.py:241-246`).

**Where ≥0.95 lives — it IS in qiyas, and only in qiyas.**
- Function default: `orb_validate.py:384` (`threshold: float = 0.95`).
- CLI default: `cli.py:3026`.
- Test gate asserting the plan target: `/Users/omareid/Workspace/git/qiyas/tests/test_orb_validate.py:281, 293` (`report["composite"] >= 0.95`).
- Docs: `/Users/omareid/Workspace/git/qiyas/docs/cli-reference.md:452`.
- **No qiyas CI workflow runs `orb-validate` at all.** `.github/workflows/*.yml` has zero `orb` hits; the only contract-adjacent CI step is `make local.validate-dsl-contract` at `.github/workflows/ci.yml:124`. There is also **no Makefile target** invoking `orb-validate` (the only `orb` hits in the Makefile are the DSL-contract exemptions, lines 559-588). So the threshold is enforced by (a) the CLI's own exit-1 (`cli.py:3086-3087`) and (b) `tests/test_orb_validate.py`.

**Exit code:** `SystemExit(1)` when `passed` is false (`cli.py:3086-3087`).

**Stale help text (real defect worth knowing):** `--recon-dir`'s help says "Default: self-validation — each view SVG is rasterized and the raster-path encoding is diffed against the SVG-fast-path encoding" (`cli.py:3010-3014`, mirrored into `docs/cli-reference.md:450`). The implementation does **no such diff** when `recon_dir is None` (`orb_validate.py:416` — the whole diff block is inside `if recon_dir is not None`). The default path scores only against gt.

---

#### 2. Schema (`src/qiyas/schema.py`)

- **`SCHEMA_VERSION = "1.22"`** — `/Users/omareid/Workspace/git/qiyas/src/qiyas/schema.py:25`. The 1.22 bump note (`:14-18`) is exactly the orb slice: `Contour` gains `orb_view` / `orb_projection` / `orb_base_face`, plus `OrbValidateWarning` joining `WarningUnion`.

**Orb-specific fields on `Contour`** (`schema.py:332-345`):
- `orb_view: str | None` (`:343`) ← `data-orb-view`, format `"<kind>-<fold>"`.
- `orb_projection: Literal["spherical","faceted"] | None` (`:344`) ← `data-projection`. **Closed vocabulary of exactly two values** — anything else is silently coerced to `None`.
- `orb_base_face: int | None` (`:345`) ← `data-orb-base-face`.
- Docstring at `:332-342` states "Presence of `orb_view` is the discriminator `qiyas orb-validate` uses to treat an SVG as an orb view."

**Orb-specific models:**
- `OrbValidateWarning` — `schema.py:613-622`, `source: Literal["orb-validate"]`; joins `WarningUnion` at `:625-628`.
- `OrbViewResult` — `schema.py:652-680`. Fields: `view, fold, projection, svg, gt, gt_declared_shapes, encoded_shapes, fold_in_encoding, scores, recon, recon_scores`.
- `OrbValidateReport` — `schema.py:683-699`. Fields: `schema_version, orb, views, composite, min_view_composite, threshold, passed, warnings`. Docstring at `:686-690` states the pass rule.

**Shared fields the orb path reuses:** `Scores` (`schema.py:563-569`, all four floats bounded `[0,1]`), `Symmetry` (`:485-491`), `ImageMetadata` (`:235-241`), `Encoding.shapes` / `.symmetry` / `.image`.

**Note:** `orb_base_face` is **parsed but has zero consumers** anywhere in `src/` — grep for it outside `schema.py` and `svg_primitives.py` returns nothing. The contract doc claims it "regroups faces per base tile" (`dsl-metadata-contract.md:46`); that consumer does not exist yet.

**`ShapeType`** (`schema.py:34-56`) has no orb-specific member; there is a `band_crossing` and a `lens` member (relevant to ribbon lattices — see §8).

---

#### 3. SVG parsing / encoding (`src/qiyas/stages/svg_primitives.py`)

Entry point: `extract_primitives_svg(svg_text, *, params=None, target_dims=None)` — `/Users/omareid/Workspace/git/qiyas/src/qiyas/stages/svg_primitives.py:275-363`.

**Elements consumed** (`svg_primitives.py:481-497`, docstring `:18-19`): `<line>`, `<polyline>`, `<polygon>`, `<rect>`, `<circle>`, `<ellipse>`, `<path>`, plus containers `<g>`, `<svg>`, `<defs>`, `<symbol>`, `<use>`.
- Path commands `M/L/H/V/Z/C/S/Q/T/A` flattened by `svgpathtools` to segments at `MAX_CHORD_ERROR_PX = 0.5` (`:218`, `:938-996`).
- Transforms `matrix/translate/scale/rotate/skewX/skewY` composed via CTM walk; **fails closed** on anything unparseable (`:818-911`) → `SvgParseError` → pipeline falls back to raster.
- `<rect pointer-events="none">` is skipped (`:582-583`) — that's how the WeaveOrb background rect is excluded.

**`data-*` attributes consumed** — all in `_read_bikar_metadata` (`svg_primitives.py:97-187`):
`data-sides`, `data-face-index`, `data-layer`, `data-face-class`, `data-symmetry-fold`, `data-partial`, `data-clipped-boundary`, `data-orb-view`, `data-projection`, `data-orb-base-face`.

##### ⚠️ The single most important finding for your extension

**`data-sides` is a hard gate on ALL other metadata, including the orb attrs.** `svg_primitives.py:104-106`:
```python
sides_raw = elem.get("data-sides")
if sides_raw is None:
    return _BikarMetadata(None, None, None, None)   # everything else discarded
```
Same early-return on a malformed int (`:109-112`). I verified this empirically: a `<path data-orb-view="weave-3" data-projection="spherical" data-orb-base-face="0">` **without** `data-sides` produces a `Contour` with `orb_view=None, orb_projection=None, orb_base_face=None, source_tag=None`.

Every witness test co-emits `data-sides` with the orb attrs (`tests/test_svg_primitives_bikar_metadata.py:307-309`, `:333-340`; `tests/test_orb_validate.py:198-202`), so the coupling is **untested and unnoticed**. A ribbon/stroke geometry that has no meaningful "sides" count will silently lose all three orb attrs → `gt_consistency_gate` fires `orb-view-attr-mismatch` at error severity (`orb_validate.py:302-315`) → guaranteed FAIL regardless of score.

**Contour handling / assumptions:**
- Closed detection is purely geometric: first vertex == last vertex within `1e-6` (`svg_primitives.py:675-679`); the duplicate closing vertex is dropped (`:682-685`).
- A `<path>` may split into multiple subpaths, each becoming its own `Contour`, all sharing the parent element's metadata (`:670-672`, `:924-935`).
- **Open** subpaths with exactly 2 verts become `Line`s (`:699-700`); open subpaths with ≥3 verts become **open `Contour`s** (`:701-718`) — i.e. an open polyline lands in the same `contours` list as a closed face, with no `is_closed` flag on `Contour`.
- **Strokes are second-class:** elements with `fill="none"` get their contour ids recorded in `_stroke_contour_ids` (`:433-434`, `:460-462`), and those contours are **exempted from Douglas-Peucker simplification** specifically to preserve their "classify-as-unknown" behavior (`:342-344` — comment: `# stroke outline: keep raw (classifies unknown)`).
- Producer-authored contours (`source_tag is not None`, i.e. those with `data-sides`) are **exempt from both the min-area floor and DP simplification** (`:336-340`).
- Untagged contours below `params.contour_min_area` are **dropped** (`:341-342`).
- Stroke **width is never read** — a ribbon is treated as its outline path only, with no notion of band width or over/under.

**Assumptions about the SVG:** it is a flat 2D canvas; `viewBox` → canvas via `meet` (uniform min-scale + centering) at `:774-791`; default canvas 512px (`:224`). Nothing in this module knows about hemispheres, occlusion, or 3D — the front-hemisphere guarantee is asserted only in prose (`orb_validate.py:6-9`).

---

#### 4. The dsl-metadata-contract

**Doc location (qiyas mirror, ships inside the wheel):** `/Users/omareid/Workspace/git/qiyas/src/qiyas/docs/dsl-metadata-contract.md`. Path constant: `src/qiyas/validate_dsl_contract.py:55` (with the rationale — resolving against repo root broke installed-mode). Canonical upstream is `sacred-patterns/docs/dsl-metadata-contract.md` (`dsl-metadata-contract.md:3`); mirrored canonical version **v1.4** (`:7`).

**Orb rows in "Currently covered"** (`dsl-metadata-contract.md:22-24`):
| Attribute | Field | Witness |
|---|---|---|
| `data-orb-view` | `Contour.orb_view` | `tests/test_svg_primitives_bikar_metadata.py::test_data_orb_view_carries_through_to_contour` |
| `data-projection` | `Contour.orb_projection` | `...::test_data_projection_carries_through_to_contour` |
| `data-orb-base-face` | `Contour.orb_base_face` | `...::test_data_orb_base_face_carries_through_to_contour` |

Narrative section: `dsl-metadata-contract.md:40-48` — ACCEPTED in v1.4 (2026-08-02), notes that the witnesses cover only the SVG→`Contour` half and **do not** satisfy the round-trip clause (`:44`), and that orb attrs are **conditional** so 2D fixtures must exempt them via `--allow-absent` (`:48`).

**Witness-test convention** (`/Users/omareid/Workspace/git/qiyas/tests/test_dsl_metadata_contract.py`):
- Row regex `_ROW_RE` at `:48-53` — **exactly three columns**, each backticked: `` | `data-<attr>` | `Contour.<field>` | `tests/<path>::<name>` | ``. Attr must match `data-[a-z0-9-]+`; field must match `Contour\.[a-z0-9_]+` (so a non-`Contour` consumer field **cannot** be expressed).
- Table body located structurally off the GFM delimiter row (`:59-87`), same logic duplicated at `validate_dsl_contract.py:133-159` (the duplication is deliberate — `:57-63`).
- **Fails closed:** an unparseable body row raises at collection time (`:110-116`).
- Two gates: `test_contract_mirror_has_covered_rows` (`:133`) and parametrized `test_contract_row_witness_test_exists` (`:146-161`) which only checks that `def <test_name>(` textually exists in the cited file.

**What a new contract row would require:**
1. A `Contour.<field>` addition in `schema.py` + `SCHEMA_VERSION` bump (schema docstring `:1-6` says the plan doc must be updated and the version bumped).
2. Parsing in `_read_bikar_metadata` (`svg_primitives.py:97-187`) **and** propagation into every one of the 5 `Contour(...)` construction sites (`svg_primitives.py:556-570`, `:597-611`, `:621-637`, `:641-657`, `:682-698`, `:702-718`) — note `_emit_ellipse_as_contour` and `_emit_rect` already **omit** `partial`/`clipped_at_boundary`, an existing inconsistency.
3. A witness test function named in the row, in a file under `tests/`.
4. A row added to the "Currently covered" table in the exact 3-column backticked format.
5. If the attr is conditional (as orb attrs are), add it to the Makefile exemptions: `ORB_ATTR_EXEMPTIONS` at `Makefile:564` and the inline `ORB_CONDITIONAL` set at `Makefile:588`.
6. Per `dsl-metadata-contract.md:34`, a producer-side-ACCEPTED row with **no qiyas consumer must not** be added to the table.

---

#### 5. What the per-view diff actually compares

**Not pixels.** There is no import of `pixel_diff`, `raster_diff`, or `hier_diff` anywhere in `orb_validate.py`. The comparison is **shape-centroid + area matching against declared gt**.

`score_encoding_against_gt(gt, encoding) -> Scores` — `orb_validate.py:180-246`:
- Both sides normalized to the **unit square** — gt centers by `gt.image.width_px/height_px`, encoding centers by `encoding.image.width_px/height_px` (`:168-177`, `:210-211`). Rationale at `:34-39`.
- Cost matrix = Euclidean unit-square centroid distance, `scipy.optimize.linear_sum_assignment` (`:213-214`).
- Acceptance radius: `CENTER_MATCH_MAX_DIAG_FRAC = 0.02` (`:70`) × `sqrt(2)` (`:212`). Pairs beyond it are discarded (`:218-219`).
- `structural = len(drifts) / max(len(ref), len(rec))` (`:224`).
- `geometric = max(0, 1 - mean(drift))` where `drift = 0.5*(dist/max_dist) + 0.5*relative_area_diff` (`:222-225`).
- `symmetry`: 1.0 if gt's `dominant_fold` ∈ encoding's `rotational_orders` or == `dominant_fold`; 0.5 if `gcd > 1`; else 0.0 (`:227-238`).
- **Deliberately type-agnostic** — rationale at `:18-28` and `schema.py:661-667`: projection makes faces irregular so bikar declares `unknown` where qiyas types `regular_polygon`; typed matching measured 0.67 composite with all 55 centers coincident.

**Important asymmetry:** this scorer iterates `encoding.shapes` **raw** (`orb_validate.py:204`) — it does **not** apply `_split_scoreable` (`src/qiyas/diff/__init__.py:297-308`), so `unknown`-typed shapes and `scoreable_exclusion`-flagged shapes **do** count in the structural denominator. The recon path (`compute_diff`) does filter them (`diff/__init__.py:118-119`). Consequence: extra unknown contours directly depress `structural`.

**The typed diff exists only in `--recon-dir` mode:** `orb_validate.py:429-441` — `compute_diff(enc, recon_enc, ...)` writes `<stem>.diff.json` and yields `recon_scores`. Explicitly **informational, not gated** (`:30-33`, and `passed` at `:476` reads only gt composites).

**Per-view results → composite:** results appended at `orb_validate.py:443-453`, mean taken at `:466-467`, report written to `output_dir/orb-validate.json` at `:479-483`.

**Separate gate, not part of the score:** `gt_consistency_gate` (`orb_validate.py:249-369`) emits:
- `gt-missing-orb-view` — **error** (`:268-275`)
- `orb-view-attr-mismatch` — **error**, three sites: gt/filename view disagreement (`:281-291`), SVG contour `data-orb-view` set ≠ `{declared}` (`:303-315`), contour projections ≠ `{declared}` (`:316-326`)
- `shape-count-mismatch` — **warn** (`:330-340`)
- `fold-not-detected` — **warn** (`:347-360`)

Discovery-level errors: `unrecognized-view-stem` (`:112-122`), `unpaired-gt` (`:124-134`), `unpaired-svg` (`:143-152`), `multiple-orbs` (`:154-164`), `no-views` (`:455-464`), `recon-missing` (`:419-428`).

---

#### 6. Orb fixtures

**Two distinct fixture locations. `fixtures-canonicals/` is NOT the orb-validate fixture.**

**A. `tests/fixtures/orb-views/` — the real orb-validate fixture (2 files, committed):**
- `/Users/omareid/Workspace/git/qiyas/tests/fixtures/orb-views/WeaveOrb.face-3.svg` (10,400 B)
- `/Users/omareid/Workspace/git/qiyas/tests/fixtures/orb-views/WeaveOrb.face-3.gt.json` (82,740 B)

gt.json contents: schema `1.24`; `image` 900×900 with `sha256: ""`; 40 shapes (36 `triangle`, 4 `unknown`); `symmetry.dominant_fold = 3`; `orb_view = {view: "face-3", kind: "face", fold: 3, axis: [-0.577,0.577,0.577], projection: "spherical", radius_mm: 60, front_cap_min_dot: 0.3}`. Shape evidence carries `outline`, `outline_arcs`, `fill_region`, `source_primitives`, `shape_id`, `face_class`.

SVG contents: root `<svg viewBox="-70 -70 140 140" width="140" height="140" data-orb-view="face-3" data-projection="spherical">`, a `pointer-events="none"` background rect, then **filled closed `<path>` faces** each with `fill="#8a8a8a" stroke="#333333" stroke-width="0.4" data-face-index=N data-sides=3|6 data-orb-view="face-3" data-projection="spherical" data-orb-base-face=N`.

**Critical for your scoping:** despite the name "WeaveOrb", this fixture is **per-face closed filled polygons** (triangles + hexagons grouped by `data-orb-base-face`), *not* stroked ribbons. There is **no existing fixture** exercising a stroke/ribbon orb.

Referenced by `tests/test_orb_validate.py:42` (`FIXTURES`), used e2e at `:280-296`.

**B. `fixtures-canonicals/` — showcase artifacts, gitignored:**
- `git check-ignore` confirms `.gitignore:47` excludes the whole directory; it's a local build artifact of `/Users/omareid/Workspace/git/qiyas/scripts/build_canonical_showcase.py`.
- Each fixture = **exactly two files**: `<slug>.png` + `<slug>.json`. The JSON is a metadata sidecar only — keys `{title, category, demonstrates, expected_dominant_fold, pair_with}` (written at `build_canonical_showcase.py:75-84`). **No SVG, no gt.json, no encoding.**
- Orb entry present locally: `fixtures-canonicals/orb-star-vertex5.json` + `.png` (900×900 RGB, dated 2026-07-25). Sidecar: `category: "orb-view"`, `expected_dominant_fold: 5`, title "Star Orb — vertex-5 view".
- **This one is not reproducible from the script:** `orb-star-vertex5` is absent from `CANONICAL_NAMES` (`tests/fixtures/render.py:14-58`) and from `EXPECTED_DOMINANT_FOLD` (`tests/test_canonical_validation.py:392-435`), and the script only iterates `CANONICAL_NAMES` (`build_canonical_showcase.py:68`). It was dropped in out-of-band alongside the M3 work. Its `category: "orb-view"` is also outside `_CATEGORY_HINTS` (`build_canonical_showcase.py:46-59`).
- Consumed only by `qiyas showcase --fixtures-dir fixtures-canonicals` (`Makefile:678, 683, 685`).

---

#### 7. `validate-dsl-contract`

**CLI:** `/Users/omareid/Workspace/git/qiyas/src/qiyas/cli.py:2205-2283`. Args: `SVG_PATH` (required, file); `--strict/--no-strict` (default strict); `--output/-o`; `--allow-absent ATTR` (repeatable). Exit codes documented at `cli.py:2249-2252`: 0 ok, 1 contract violation, 2 usage error (unknown exemption → `click.UsageError` at `:2260-2262`).

**Logic:** `/Users/omareid/Workspace/git/qiyas/src/qiyas/validate_dsl_contract.py:203-304` (`validate_svg`). For each row parsed from the mirror (`load_contract_rows`, `:162-200`):
1. Counts raw SVG occurrences by regex `\bdata-foo\s*=` on the file text (`:248`) — **textual, does not check which element carries it**.
2. Counts `Contour`s where `getattr(c, row.field_name) is not None` after `extract_primitives_svg` (`:251-253`).
3. Verdict matrix (`:255-289`):
   - carried == 0 & exempted → `absent_allowed=True`, passes.
   - carried == 0 & strict & not exempted → **FAIL** ("absent").
   - carried > 0 & exempted → **FAIL** ("stale exemption").
   - carried > 0 & contours_populated == 0 → **FAIL** ("parser drop or schema mismatch") — this one fails **regardless of `--strict`**.

**Note the gap:** because step 1 is a text regex and step 2 only requires ≥1 populated contour, a file where `data-orb-view` appears only on the root `<svg>` (as WeaveOrb's does) and on faces that also carry `data-sides` will pass; a file where the attr appears on 200 stroke paths lacking `data-sides` will report `svg_elements_carrying=200, contours_with_field_populated=0` → **FAIL with "parser drop"**, and `--no-strict` will not rescue it.

**CI wiring:** `Makefile:568-593` (`local.validate-dsl-contract`), invoked at `.github/workflows/ci.yml:124`. `STRICT_FIXTURES` ratchet at `Makefile:563`; orb attrs blanket-exempted for all 2D fixtures via `ORB_ATTR_EXEMPTIONS` (`Makefile:564`) and filtered out of the no-strict survey via the inline `ORB_CONDITIONAL` set (`Makefile:588`).

---

#### 8. What would break on a woven-ribbon-lattice orb

Ordered by severity. These are hard blockers, not tuning issues.

**8.1 — `data-sides` gate silently voids all orb attrs. (Blocker.)** `svg_primitives.py:104-106`. If ribbon paths carry `data-orb-view`/`data-projection` but no `data-sides` (a ribbon has no canonical side count), the `Contour` fields are `None`. Then `gt_consistency_gate` computes `contour_views = set()` (`orb_validate.py:299`) and `set() != {declared_view}` fires an **error-severity** `orb-view-attr-mismatch` (`:303-315`) → `passed=False` unconditionally (`:469, 476`). Verified empirically. Also causes `source_tag` to be `None`, which cascades into 8.2.

**8.2 — Untagged contours get area-floored and DP-simplified.** `svg_primitives.py:336-357`. Without `source_tag` (i.e. without `data-sides`), each ribbon contour is subject to `contour_min_area` dropping (`:341-342`) and Douglas-Peucker simplification with `eps = max(1, perimeter * contour_simplify_eps_frac)` (`:376-396`). For a long thin ribbon, perimeter is huge relative to width, so eps will be large enough to collapse the ribbon's width — the two long sides get merged. This is exactly the failure mode the code warns about for merged multi-lobe regions (`schema.py:320-331`).

**8.3 — Stroke ribbons (`fill="none"`) are routed to "classify as unknown".** `svg_primitives.py:342-344` and `:433-434, 460-462`. The comment is explicit: `# stroke outline: keep raw (classifies unknown)`. Combined with `orb_validate.py:204` scoring raw `encoding.shapes`, a lattice of N unknown stroke contours inflates `len(rec)` in `structural = len(drifts) / max(len(ref), len(rec))` (`:224`) — every unmatched ribbon directly divides the structural score. There is **no** stroke-width awareness anywhere in `svg_primitives.py`; a ribbon is its centerline/outline path only.

**8.4 — Crossings produce shared regions with no over/under model.** Where ribbons cross, either (a) the producer emits one closed region per crossing cell (then gt and encoding must agree on that decomposition), or (b) the SVG has genuinely self-intersecting paths. `_polygon_area` is a shoelace (`svg_primitives.py:366-373`) — **wrong for self-intersecting polygons** (signed lobes cancel), so a crossing ribbon can read as near-zero area and be dropped by the min-area floor. The schema's `Polygon`/`ArcShape` invariants (`schema.py:147-198`) assume a simple closed chain; there is no non-simple-polygon type. `band_crossing` exists in `ShapeType` (`schema.py:53`) but is a 2D-strapwork detector output, not something the orb scorer or the gt-consistency gate knows about.

**8.5 — Area-based geometric drift punishes thin geometry.** `orb_validate.py:222` — `area_drift = abs(ra-ea)/max(ra,ea)`. For thin ribbons, a 1-pixel rasterization/flattening difference in width is a large *relative* area change, so `geometric` degrades far faster than it does for chunky faces. The `CENTER_MATCH_MAX_DIAG_FRAC = 0.02` acceptance radius (`:70`) was justified specifically on face spacing: "Faces on a radius-60 orb view are ~0.05 diagonals apart" (`:67-70`). A woven lattice's crossing cells are much closer together than that; 0.02 diagonals may exceed the inter-cell spacing, letting Hungarian pair the *wrong* cells at low cost and producing a vacuously high score.

**8.6 — Centroid+area is a weak identity for a lattice.** The whole scorer is positional/area only (`:180-246`, rationale `:18-28`). A woven lattice's cells are near-identical in center spacing and area; over/under weave parity — the thing that actually distinguishes a correct weave from an incorrect one — is invisible to this metric. Two different weave topologies with the same cell grid would score identically.

**8.7 — Per-face assumptions in prose and contract.** `orb_validate.py:7-9` ("The whole-face front cap guarantees every view is a valid 2D pattern image"); `:293-295` ("the SVG's **face paths** must carry the same view id"); `schema.py:335-341`; `dsl-metadata-contract.md:46` ("Every projected **face** `<path>`... `data-orb-base-face` (index of the base-polyhedron face the pattern face was lifted through)"). A ribbon that spans multiple base-polyhedron faces has **no single** `data-orb-base-face` value — the contract's semantics don't have a representation for it. (Fortunately `orb_base_face` has no consumer, so this is a contract/semantics problem rather than a runtime one — today.)

**8.8 — Pattern-id / per-face-pattern structure:** worth noting what is **not** a problem. There is no "pattern id" concept and no per-face-pattern grouping requirement in the orb path. `face_class`, `shape_id`, and `authoritative_sides` are all optional and default `None` (`schema.py:290-345`). The DSL-contract `data-face-class` row is satisfied by any single populated contour. So "no per-face star pattern" is not itself fatal — **the fatal coupling is `data-sides`** (8.1).

**8.9 — View-stem naming.** `_VIEW_STEM_RE` at `orb_validate.py:63` requires `[a-z]+-\d+`. Any new view-kind vocabulary must stay lowercase-alpha; `fold` is parsed from gt (`:277-278`) not the stem, but the stem must still match or the view is dropped with an error.

**8.10 — Symmetry stage is raster/binary-based.** `src/qiyas/stages/symmetry.py:107-126` — rotational fold is detected by MSE over a rotated binary image, with a `fallback_dilation_radius` pass specifically for thin strokes when `dominant_fold == 1` (`:117-125`). This is the one part of the pipeline that will likely behave *acceptably* on a ribbon lattice, and it drives 25% of the composite via `W_SYMMETRY`.

---

#### Suggested reading order for the extension

1. `src/qiyas/stages/svg_primitives.py:97-187` — decouple orb attrs from `data-sides`; this is the load-bearing change.
2. `src/qiyas/orb_validate.py:180-246` — the scorer you'd need to extend or branch for non-face geometry.
3. `src/qiyas/orb_validate.py:249-369` — the gate whose `contour_views` check will fire first.
4. `src/qiyas/docs/dsl-metadata-contract.md:15-24, 40-48` + `tests/test_dsl_metadata_contract.py:48-53` — the row format any new attr must satisfy.
5. `tests/fixtures/orb-views/WeaveOrb.face-3.*` — the shape of fixture you'd need to add a ribbon sibling to.

---

## 2. Report B — bikar: what is emitted for orb views today

*Produced by the bikar Explore agent against `~/Workspace/git/bikar-lego-lab`
(worktree, detached at merged main `f3cb04c`). Preserved verbatim.*

### Orb view / gt emission map — bikar @ `f3cb04c` (worktree `/Users/omareid/Workspace/git/bikar-lego-lab`)

All paths absolute. Empirical checks were run in-memory against `packages/core/dist/index.js` (no files written).

---

#### 1. Classic orbs (Family 1/2, per-face inscription) — how views are emitted

**Two modules, one shared scene.**

- Projection: `/Users/omareid/Workspace/git/bikar-lego-lab/packages/core/src/kernel3d/orb-views.ts:156` `projectOrbView(base, patternFaces, params) → OrbViewScene`
- SVG: `/Users/omareid/Workspace/git/bikar-lego-lab/packages/core/src/render/orb-view-renderer.ts:71` `renderOrbViewSVG(input)`
- gt: `/Users/omareid/Workspace/git/bikar-lego-lab/packages/core/src/render/gt-emitter.ts:2053` `emitOrbViewGroundTruth(scene, styling, options)`
- Scene type (the shared contract so SVG and gt cannot disagree): `orb-views.ts:78-84`

**Symmetry axes per base solid** — `orb-views.ts:39-54` `symmetryViewAxes(base)`. No per-solid catalog; everything derives from *element 0*:
- `vertex-<fold>`: fold = count of faces containing vertex 0 (`orb-views.ts:40`), axis = `normalize3(base.vertices[0])`
- `face-<n>`: n = `base.faces[0].length`, axis = normalized centroid of face 0 (`orb-views.ts:42,51`)
- `edge-2`: fold fixed at 2, axis = normalized midpoint of face 0's first edge (`orb-views.ts:43,52`)

Verified: icosa → `vertex-5 / face-3 / edge-2`; dodeca → `vertex-3 / face-5 / edge-2` (matches `docs/decisions/2026-07-25-orb-view-orthographic-validation.md:70-75`).

**data-\* attributes actually written** (nothing else — there is no `data-face` and no `data-pattern` anywhere in the repo; grep over `packages/*/src` returns empty):

Root `<svg>` (`orb-view-renderer.ts:78`): `viewBox`, `width`, `height`, `data-orb-view="<scene.view.id>"`, `data-projection="<spherical|faceted>"`.

Per-face `<path>` (`orb-view-renderer.ts:88` + `buildViewFaceAttrs` at `orb-view-renderer.ts:38-58`), in emit order:
1. `class="..."` and `data-face-class="..."` — only when the pattern face has classes; sorted, space-joined, XML-escaped (`:42-49`)
2. `data-face-index="<scene index>"` (`:51`) — note this is the *scene* ordinal, not the pattern face ordinal
3. `data-sides="<polygon.source.edgeCount>"` (`:52`) — raw edge count, same as 2D
4. `data-orb-view="<view.id>"` (`:53`)
5. `data-projection="<spherical|faceted>"` (`:54`)
6. `data-orb-base-face="<baseFaceIndex>"` (`:55`)

Fill = `faceColors.get(patternFaceIndex)` else `DEFAULT_ORB_VIEW_FILL = '#8a8a8a'` (`orb-view-renderer.ts:11,84-86`); stroke fixed `#333333`/0.4; opaque `<rect>` background first (`:79`).

**Not carried into views** (the 2D renderer emits these in `packages/core/src/render/svg-renderer.ts`, orb views drop them all): `data-layer` (`:663`), `data-symmetry-fold` (`:607`), `data-wave` (`:612`), `data-shape-id` (`:616`), `data-authored-region` (`:621`), `data-whorl` (`:628`), `data-partial` (`:634`), `data-clipped-boundary` (`:636`), `data-ring`/`data-angle-index`/`data-sweep-index` (`:666-670`).

---

#### 2. The gt emitter

- `GT_SCHEMA_VERSION = '1.25'` — `/Users/omareid/Workspace/git/bikar-lego-lab/packages/core/src/render/gt-emitter.ts:409` (1.24 added `orb_view`, docstring `:383-393`; 1.25 added the `'spiral'` outline arm, `:394-407`).
- `GtOrbView` envelope type: `gt-emitter.ts:276-284` → `{view, kind, fold, axis[3], projection, radius_mm, front_cap_min_dot}`; optional field on the envelope at `gt-emitter.ts:318`.
- Per-view gt content (`emitOrbViewGroundTruth`, `gt-emitter.ts:2053-2112`):
  - `shapes`: one per projected polygon, **no colour-union merge** (`:2063`), built by `buildOrbViewShape` (`:1974-2039`): `id: shape_NNN`, `type`/`params` from `classifyFace(polygon.source)`, `params.sides = countGeometricCorners(projected points)` (`:2007`), `params.orb_base_face = polygon.baseFaceIndex` (`:2008`), `evidence.outline_arcs` all `type:'line'` (`:2022-2028`), `evidence.face_class` from the pattern face's class set via `orbViewFaceClass` (`:1948-1952`, `:2033`), `shape_id: null`, `authored_region: null` (`:2034-2035`), `mask_rle: null`.
  - `symmetry`: `rotational_orders:[view.fold]`, `dominant_fold: view.fold`, `confidence: 1.0`, `reflection_axes_deg: []` (`:2084-2089`).
  - `stats`, `centroid` computed over the view's shapes (`:2064-2073`, `:2090-2097`).
  - `orb_view` block (`:2098-2110`), axis rounded to 6 dp.
  - Pixel transform: fixed sphere disc + padding (default 10) → `imageWidth`, uniform scale, height derived (schema-1.18 semantics) (`:2058-2062`).
- **Not type-locked**: `/Users/omareid/Workspace/git/bikar-lego-lab/packages/core/src/contract-conformance.ts` locks only `image`/`stats`/`symmetry`/`centroid` leaves (`:59-65`) and required top-level keys `centroid|image|shapes|stats|symmetry` (`:72-74`). `orb_view` is deliberately outside the lock (additive optional field); the shape-level union is an explicit non-assertion (`:76-83`).

**CLI wiring** — `/Users/omareid/Workspace/git/bikar-lego-lab/packages/cli/src/index.ts`:
- Flag: `bikar render <file> --format views -o <dir> [--width <px>]` — dispatch at `:839-842`, implementation `renderOrbViews` at `:754-820`, usage text `:225-238`.
- Requires `result.orb3d` (`:756-763`) and `-o` (`:764-768`); `--width` default 900 (`:769`).
- Per axis it writes three files named `<orb.name>.<view.id>.{svg,png,gt.json}` (`:786-790`, `:814`): SVG first, then a **probe** gt to learn pixel dims (`:796-800`), rasterize via `rasterizeOrDie` (`:801-807`, needs `rsvg-convert`/`magick`), then the real gt with the PNG's sha256 (`:809-813`). No rasterizer ⇒ hard fail, no gt (pinned at `packages/cli/tests/render-image.test.ts:252-276`).
- The 2D path is separate: `--emit-truth <path.gt.json> --image --width` → `emitGroundTruth` (`packages/cli/src/index.ts:1011-1051`).
- Same renderer is reused live by the Lab worker (`/Users/omareid/Workspace/git/bikar-lego-lab/packages/lab/src/evaluate.ts:486-503`, `scale: 4`, SVG only — **no gt**) and by the web studio (`/Users/omareid/Workspace/git/bikar-lego-lab/packages/web/src/main.ts:1907-2001`).

---

#### 3. The wheelfield / maclado path — what it emits today

**It goes through exactly the same renderer, because the evaluator hands it an `orb3d`.**

- Evaluator branch: `/Users/omareid/Workspace/git/bikar-lego-lab/packages/core/src/dsl/evaluator.ts:1335-1365` `evaluateWheelfieldOrbDecl`. It sets `orb3d = {name, base: dodecahedron(), radiusMm, projection:'spherical', strut dims, family: weave?'weave':'lattice'}` (`:1355-1363`).
- The `EvaluationResult.faces` it returns are **not** an inscribed pattern: they are a synthesized 2D preview of *one flat wheel* — boundary ring + void rings pushed through `buildIntersectionGraph`/`extractFaces` (`evaluator.ts:1373-1392`, `wheelfieldPreview`). Base result is `emptyPiece2DResult()` (`evaluator.ts:1671-1683`) ⇒ `faceColors` empty `Map`, `faceClasses` **undefined**, segments carry no source tags.
- Mesh comes from a completely different construction: `solidWheelfieldMesh` (`evaluator.ts:1395-1413` → `solidifyMacladoField`) or `wovenWheelfieldMesh` (`evaluator.ts:1425-1453` → `macladoSeamGraph`/`buildWovenOverlapGraph` → `weaveSphereGraph`).

**Consequence — the views are computed from the preview, not from the field.** `renderOrbViews` (`cli/src/index.ts:775-780`) calls `projectOrbView(dodecahedron(), previewWheelFaces, …)`, which lifts the one wheel onto **each of the 12 dodecahedron faces** via `makeFaceLift` (`orb-views.ts:165-166`; `packages/core/src/kernel3d/face-frame.ts:93-98`, pentagon → `regularLift`, `:74-84`). The real object is **20 wheels at dodecahedron vertices** (`packages/core/src/kernel3d/maclado-field.ts:30-50`, `:92-96`, `:194`). The wheel is authored at `PATTERN_CIRCUMRADIUS = 100` with tips every 360/9° (`packages/core/src/kernel3d/maclado-wheel.ts:101-107`, `:116-140`), so lifting it onto a pentagon (corners every 72°) pushes tips past the face edges.

**Measured, in-memory, at `f3cb04c`:**

| preset | orb name | family | axes | polys per view (v/f/e) | crossing polygon pairs (different base faces) |
|---|---|---|---|---|---|
| Maclado-9 | `Maclado9` | lattice | `vertex-3, face-5, edge-2` | 66 / 68 / 63 | 8 / 9 / 8 |
| Maclado-9-Weave | `Maclado9Weave` | weave | same | 68 (face-5) | same |
| Maclado-9-Overlap | `Maclado9Overlap` | weave | same | 68 (face-5) | same |
| Star-Orb (classic) | `StarOrb` | lattice | `vertex-5, face-3, edge-2` | 55 / 55 / 60 | **0 / 0 / 0** |
| Weave-Orb (classic) | — | weave | — | 40 / 40 / 44 | **0 / 0 / 0** |

So: **yes, gt is emitted for wheelfield orbs** (the CLI path is family-blind), schema 1.25 with a full `orb_view` block — I produced `orb_view = {"view":"face-5","kind":"face","fold":5,"axis":[-0.525731,0.850651,0],"projection":"spherical","radius_mm":60,"front_cap_min_dot":0.3}` and 68 shapes (`{"square":31,"triangle":36,"unknown":1}`). But its content is the face-lifted preview wheel, and:

- Every face gets `fill="#8a8a8a"` (no `faceColors`), **no `class`/`data-face-class`** (no `faceClasses`), `evidence.face_class = null`, `evidence.shape_id = null`, `source_primitives = []` (the preview segments are untagged).
- **The three Maclado presets emit byte-identical view SVGs** — same SHA-256 over the rendered face-5 SVG for `Maclado-9`, `Maclado-9-Weave`, `Maclado-9-Overlap`. Views are blind to `weave`, `overlap` ratio, `amplitude`, and ribbon width/depth; the only view-visible knobs are `radius` and `wheel points/contact`.
- **Nothing in a view represents a ribbon.** There is no strand element or attribute in the orb-view renderer at all — the only element kinds are the background `<rect>` and face `<path>`s (`orb-view-renderer.ts:79,88`). The repo *does* have an over/under ribbon representation, but it lives only in the 2D strapwork path: `packages/core/src/render/svg-renderer.ts:1059-1078` emits `<g class="strapwork-under">` / `<g class="strapwork-over">` with `data-strand="<strandId>"`, under-strands trimmed at crossings (`:1020-1057`). None of that is reachable from `--format views`.
- Views never touch `orbMesh`, so the woven-overlap weld nodes, strand count, and over/under parity are unrepresented in both SVG and gt.

Also note the classic-weave orbs have the same blind spot (a `Weave-Orb` view shows the *pattern faces*, gray, not the ribbons) — see the rationale docstring at `orb-view-renderer.ts:4-11`.

---

#### 4. qiyas composite recording and gating

- `qiyasComposite` lives on `ArchetypeScript` — `/Users/omareid/Workspace/git/bikar-lego-lab/packages/lab/src/scripts.ts:23-29` (doc comment `:13-22` says it is "the recorded CI `qiyas orb-validate` mean composite at declared defaults", re-record on geometry change).
- Values, `scripts.ts:38-116`: rosette-dodeca 0.954 (`:44`), rosette-cube 0.975 (`:51`), rosette-weave 1.0 (`:58`), hankin-dodeca 1.0 (`:65`), star-icosa 1.0 (`:72`), star-dodeca 1.0 (`:79`), star-cube 1.0 (`:86`), star-octa 0.992 (`:93`), star-tetra 1.0 (`:100`), weave-icosa 0.997 (`:107`), weave-dodeca 1.0 (`:114`). **No Maclado entry exists** — the registry has 11 classic orbs only, so the wheelfield family has no preset chip, no badge, and no recorded composite.
- Gate/consumer: `/Users/omareid/Workspace/git/bikar-lego-lab/packages/lab/src/main.ts:380-410` — badge `qiyas-validated ✓ <score>` only when every touched knob equals its declared default (`:397-405`, tooltip says "composite gate ≥ 0.95"); otherwise "calibrated range" (`:406-410`); custom mode says "custom design — not qiyas-validated" and points at the offline path `bikar render <file.bkr> --format views, then qiyas orb-validate` (`:388-392`). Brick presets deliberately carry no composite (`packages/lab/src/lego-scripts.ts:13-20`).
- **There is no CI job that runs qiyas, regenerates views, or enforces ≥ 0.95.** `.github/workflows/` contains `bump-peer-deps, calibration, ci, decision-coherence, deploy, e2e, publish-core, publish-qiyas-schema, secret-scan, sync-patterns`; `ci.yml` steps are install/build/typecheck/lint/format/test/test:scripts/codespell/import-graph/doc-pointers (`.github/workflows/ci.yml:71-132`) — the only `qiyas` hits in workflows are the `@naqshcoffee/qiyas-schema` publish job. `scripts/` has no qiyas or orb-validate runner (`grep -rn "orb-validate" Makefile package.json scripts/` → no hits). The root `npm run ci` script (`package.json`) likewise has no qiyas step.
- Where the numbers actually came from: commit `ba5ef85` "P2.6: trust badge, Lab+studio e2e suites, L6 constraint tests" — *"Scores come from a fresh Docker qiyas orb-validate sweep of all 11 committed orbs (all PASS >= 0.95; the five P1-recorded composites reproduced exactly), recorded per script in scripts.ts."* i.e. a **manual local Docker sweep**, hand-transcribed. The "≥ 0.95 gate re-run makes stale values a tripwire" claim in `scripts.ts:19-21` has no automation behind it in this repo.
- Cross-repo status is acknowledged as unbuilt: `/Users/omareid/Workspace/git/bikar-lego-lab/docs/dsl-metadata-contract.md:162-166` — the round-trip CI gate "needs cross-repo CI wiring, and it is unbuilt for these rows exactly as it is unbuilt for every other row in this mirror."
- The qiyas side of the seam is typed in `/Users/omareid/Workspace/git/bikar-lego-lab/packages/qiyas-schema/src/diff.ts:47` (`Source3 = 'orb-validate'`) and `:146-152` (`OrbValidateWarning`), plus `packages/qiyas-schema/schemas/diff.json:151,341`.

---

#### 5. Occlusion / front-hemisphere story

- Implementation is a **whole-face front cap**, not back-face culling and not a z-buffer: `projectFacePolygon` returns `null` the moment any lifted vertex has `dot(v̂, axis) < cap` (`packages/core/src/kernel3d/orb-views.ts:139-140`), with `DEFAULT_FRONT_CAP_MIN_DOT = 0.3` (`:93`, rationale `:86-92`). A face is either wholly kept or wholly dropped — never clipped at the rim. The cut is recorded in `scene.frontCapMinDot` (`:83`, `:185`) and republished as `orb_view.front_cap_min_dot`.
- **No depth ordering anywhere.** `polygons` are pushed in `baseFaceIndex` × `patternFaceIndex` order (`orb-views.ts:164-179`) and both emitters iterate that order verbatim (`orb-view-renderer.ts:81-89`; `gt-emitter.ts:2063`). `OrbViewPolygon.minDot` is computed (`orb-views.ts:141,176`) and **never read by any consumer** — grep across `packages/{core,cli,lab,web}/src` shows `minDot` only inside `orb-views.ts`. So there is no painter's sort, no per-strand over/under, no occlusion resolution of any kind.
- For classic orbs that is sound: the pattern tiles each base face, and I measured **zero** overlapping projected polygon pairs on Star-Orb and Weave-Orb across all three axes.
- For wheelfield it is **not** sound: 8–9 interpenetrating polygon pairs per view (table in §3), all cross-base-face, drawn in arbitrary order with opaque fills. That directly violates the premise the whole design rests on — "no see-through occlusion... whole pattern faces only" (`docs/decisions/2026-07-25-orb-view-orthographic-validation.md:29-33`) and "one shape per path" (`docs/dsl-metadata-contract.md:176-179`).
- A woven ribbon's radial over/under offset (`weaveSphereGraph` amplitude) never enters a view; the view pipeline consumes only `orb3d.base`, `radiusMm`, `projection` and `result.faces`.

---

#### 6. The three Maclado presets — param blocks

`/Users/omareid/Workspace/git/bikar-lego-lab/patterns/Orbs/Maclado-9.bkr`
- `param radius = 60 range 40..110 step 5`
- `param strut_width = 2 range 1.5..2.5 step 0.25 advanced`
- `param strut_depth = 2.4 range 1.2..4 step 0.2 advanced`
- body: `orb Maclado9 / base wheelfield / radius $radius / wheel points 9 contact 0.5 / place rule dodecahedral / struts width $strut_width depth $strut_depth`. Header comment records the `strut_width 3 @ radius 60` degeneracy that bounds the range.

`/Users/omareid/Workspace/git/bikar-lego-lab/patterns/Orbs/Maclado-9-Weave.bkr`
- `param radius = 60 range 40..110 step 5`
- `param amplitude = 0.8 range 0.8..1.6 step 0.1`
- `param ribbon_width = 1.2 range 0.8..2 step 0.1 advanced`
- `param ribbon_depth = 1.2 range 0.8..2 step 0.1 advanced`
- body: `orb Maclado9Weave`, `wheel points 9` (no `contact` ⇒ default 0.5), `weave crossing alternating amplitude $amplitude`.

`/Users/omareid/Workspace/git/bikar-lego-lab/patterns/Orbs/Maclado-9-Overlap.bkr`
- `param radius = 60 range 40..110 step 5`
- `param overlap = 1.2 range 1.15..1.25 step 0.01`
- `param amplitude = 0.8 range 0.8..1.6 step 0.1`
- `param ribbon_width = 1.2 range 0.8..2 step 0.1 advanced`
- `param ribbon_depth = 1.2 range 0.8..2 step 0.1 advanced`
- body: `orb Maclado9Overlap`, `weave crossing alternating amplitude $amplitude`, `overlap $overlap`.

All three are param-headed, so they satisfy the registry's structural precondition (`packages/lab/src/main.ts:139`, `:250`, `:687`) — they are simply not registered in `SCRIPTS`. Two gaps if they are added:
- The knob guard rail that keeps weave amplitude clear of ribbon depth reads the param **named `strut_depth`** (`/Users/omareid/Workspace/git/bikar-lego-lab/packages/knobs/src/constraints.ts:104-116`); the Maclado weave presets name theirs `ribbon_depth`, so the rule silently no-ops for them.
- There is no orb analogue of the Lego "ships exactly the presets this file has swept" corner-sweep test (`/Users/omareid/Workspace/git/bikar-lego-lab/packages/lab/tests/lego-presets.test.ts:50-72`) — orbs have no such registry↔patterns-dir gate at all.

---

#### 7. Contract doc mirror + type lock

`/Users/omareid/Workspace/git/bikar-lego-lab/docs/dsl-metadata-contract.md` — rows covering orb view attrs (all **ACCEPTED v1.4, 2026-08-02, sacred-patterns#24**):
- `:37` `data-orb-view` — root `<svg>` + every face `<path>`, `<kind>-<fold>`, named as "the discriminator qiyas uses to enter orb-view mode", mirrored as `orb_view.view`.
- `:38` `data-projection` — root + per-face, `spherical|faceted`, mirrored as `orb_view.projection`.
- `:39` `data-orb-base-face` — face `<path>` only; gt mirror `params.orb_base_face` via `buildOrbViewShape`.
- `:43` gt.json `orb_view` — the envelope block, "one shape per projected face (no colour-union), straight-chord outlines, `shape_id`/`authored_region` null, declared symmetry = axis fold at confidence 1.0".
- Long-form section `:154-191`: witness status (qiyas `SCHEMA_VERSION` 1.22, `qiyas/src/qiyas/orb_validate.py`), the explicit caveat that only the SVG→`Contour` half is witnessed and the round-trip CI gate is unbuilt (`:162-166`), the definition of a view as *the inscribed pattern* (`:172-179`) — a definition the wheelfield path does not satisfy — and the cascade line (`:187-191`).
- Related rows sharing the table: `data-sides` `:26`, gt `params.sides` `:27`, `data-face-index` `:28`, `data-face-class` `:30`.

`/Users/omareid/Workspace/git/bikar-lego-lab/packages/core/src/contract-conformance.ts` type-locks (compile-time only; `tsc -p packages/core`, never bundled — `:13-15`):
- `ImageConforms` `:59`, `StatsConforms` `:61`, `SymmetryConforms` `:63`, `CentroidConforms` `:65` — each gt leaf assignable to `EncodingLike`'s counterpart, after a deep `readonly`-strip `Mutable<>` (`:40`, rationale `:25-39`).
- `EnvelopeKeysPresent` `:74` — required top-level keys `'centroid'|'image'|'shapes'|'stats'|'symmetry'`.
- Explicitly **not** locked: the shape-level discriminated union (`:76-83`, "a widening the qiyas detector performs; it is NOT a subtype bikar must satisfy"), and by omission `orb_view`, `boundaries`, `uncovered_shapes`.

---

#### Summary of the gap for qiyas 3D validation of the maclado/wheelfield family

1. Wheelfield views **do** emit — same renderer, same three axis files, same `data-*` trio, same schema-1.25 gt with a populated `orb_view` — so nothing errors and nothing is missing structurally.
2. But the content describes a **different object than the one printed**: 12 face-lifted copies of the flat preview wheel (`evaluator.ts:1373-1392` + `orb-views.ts:165-166`) versus 20 vertex-placed wheels (`maclado-field.ts:92-96`), with the ribbons/weld/overlap entirely absent.
3. The views violate the honest-2D premise: 8–9 overlapping projected polygons per view, drawn in construction order with no depth resolution (`minDot` computed and unread).
4. Every semantic channel is empty: `faceColors` size 0, `faceClasses` undefined, `source_primitives` `[]`, `face_class`/`shape_id`/`authored_region` null.
5. The three presets produce **identical** view SVGs, so a composite score over them could not distinguish shell from weave from woven-overlap.
6. Nothing gates any of it: no Maclado entry in `packages/lab/src/scripts.ts`, no CI qiyas run anywhere, and the recorded 0.95 gate is a hand-transcribed local Docker sweep from `ba5ef85`.

---

## 3. Fetch / read record

Everything below was read directly from a local checkout on 2026-08-15. There
are no URLs: no web source was consulted for this survey, and no external
documentation was fetched. "Read" means the file was opened and the cited lines
examined; "executed" means the built bundle was imported and run in memory.

| # | Tree | Revision | What | How |
|---|---|---|---|---|
| S1 | qiyas | working tree, master (1 commit ahead of the map's `as_of` pin) | `src/qiyas/cli.py`, `src/qiyas/orb_validate.py`, `src/qiyas/schema.py`, `src/qiyas/stages/svg_primitives.py`, `src/qiyas/stages/symmetry.py`, `src/qiyas/diff/{__init__,scorer}.py`, `src/qiyas/validate_dsl_contract.py`, `src/qiyas/docs/dsl-metadata-contract.md`, `docs/cli-reference.md`, `Makefile`, `.github/workflows/ci.yml`, `tests/test_orb_validate.py`, `tests/test_dsl_metadata_contract.py`, `tests/test_svg_primitives_bikar_metadata.py`, `tests/fixtures/orb-views/WeaveOrb.face-3.{svg,gt.json}`, `scripts/build_canonical_showcase.py` | read |
| S2 | qiyas | same | `extract_primitives_svg` on a synthetic in-memory SVG carrying the orb attrs **without** `data-sides` — the empirical check behind §8.1 | executed, nothing written |
| S3 | bikar | worktree detached at `f3cb04c` | `packages/core/src/kernel3d/{orb-views,face-frame,maclado-field,maclado-wheel}.ts`, `packages/core/src/render/{orb-view-renderer,gt-emitter,svg-renderer}.ts`, `packages/core/src/dsl/evaluator.ts`, `packages/core/src/contract-conformance.ts`, `packages/cli/src/index.ts`, `packages/lab/src/{scripts,lego-scripts,main,evaluate}.ts`, `packages/knobs/src/constraints.ts`, `packages/web/src/main.ts`, `packages/qiyas-schema/src/diff.ts`, `docs/dsl-metadata-contract.md`, `docs/decisions/2026-07-25-orb-view-orthographic-validation.md`, `.github/workflows/*.yml`, `patterns/Orbs/Maclado-9*.bkr` | read |
| S4 | bikar | same | `packages/core/dist/index.js` imported in memory; the three Maclado presets and two classic orbs evaluated and their views projected/rendered — the polygon counts, overlapping-pair counts, SVG SHA-256 equality, and the sample `orb_view` gt block in §3 | executed, nothing written |
| S5 | bikar | commit `ba5ef85` | the commit message recording where the eleven `qiyasComposite` values came from (a manual local Docker sweep) | read via git log |
