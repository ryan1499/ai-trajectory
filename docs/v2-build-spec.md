# Archived v2 Build Spec — Implementation Handoff

**Status: archived, not adopted. Retained as design provenance for the superseded composite-index
proposal in [v2-vision.md](v2-vision.md). Do not use as current implementation guidance.**

Read `CLAUDE.md` (repo root) first — the data-integrity rules there (never rewrite history, evidence needs real dated sources, generated output is never hand-edited) are hard constraints on everything below.

## Ground rules

- Stack stays: JSON data → stdlib-only Python build (`scripts/build.py`) → static `dashboard/` output → Vercel (config in `vercel.json`, do not change build command or output dir).
- No new runtime dependencies. CI may use standard GitHub Actions.
- Existing v1 data files are the migration source, not disposable: `data/cruxes.json`, `data/indicators.json`, `data/updates.json`, `data/history.json`.
- All numeric claims rendered on the site must trace to a data file. No constants in templates.
- TODO(RYAN) markers below are open decisions — implement behind the simplest possible switch, do not resolve them yourself.

## Phase 1 — Data model

New/changed files in `data/`:

1. `data/dimensions.json` — the six dimensions:
   ```
   { "dimensions": [ {
       "id": "capability-pressure",
       "name": "...", "polarity": "risk" | "safeguard",
       "description": "...",
       "indicator_ids": ["metr-task-horizon", ...],
       "weight": 0.20,
       "score": null,            // computed, never hand-set
       "rationale": "why these indicators, why this weight (v1 declared prior)"
   } ] }
   ```
2. `data/indicators.json` — extend each indicator with:
   - `dimension_ids: [...]` (replaces prose-only `relevance`)
   - `normalization: { "anchors": [{"raw": ..., "subscore": ...}, ...], "rationale": "..." }` — piecewise-linear anchor mapping raw → 0-100; anchors and rationale are human-authored.
   - `subscore: null` (computed)
3. `data/worldview.json` — the cruxes, re-cast as parameters:
   - Each carries v1 fields (question, poles, position, spread, evidence, movers — migrate verbatim; v1 history in `history.json` stays linked by id) **plus** `parameter: { "affects": [...], "low_setting": {...}, "high_setting": {...}, "default": ... }` describing how the crux modulates aggregation.
   - v1 `cruxes.json` is superseded by this file via a migration script (`scripts/migrate_v1.py`, run once, kept in repo for provenance).
4. `data/methodology-version.json` — `{ "version": "1.0.0", "changelog": [...] }`.

## Phase 2 — Computation (`scripts/compute.py`, stdlib only)

- `compute.py` reads data/, computes: indicator subscores (from anchors) → dimension scores (weighted mean of subscores) → composite reading.
- Composite: risk dimensions aggregate with weighted arithmetic mean; safeguard dimensions enter as a divisor/soft-min. TODO(RYAN): exact functional form — implement one, isolate it in a single pure function `aggregate(dimension_scores, weights, worldview_settings) -> reading`, unit-test with worked examples, and document the formula in METHODOLOGY.md so swapping it is a one-function change.
- Band: reading computed across the worldview-parameter ranges (each parameter at low/default/high; band = min/max across the cartesian product, or across one-at-a-time perturbation — TODO(RYAN), default to one-at-a-time which is more legible).
- Sensitivity table: reading under each single-parameter setting, emitted to `data/computed.json` (gitignored? NO — commit it, so every published reading is diffable in git history; the build must fail if `computed.json` is stale relative to inputs, enforced by recomputing and comparing in CI).
- Weight-perturbation sensitivity: ±50% on each dimension weight, published.

## Phase 3 — Site

Keep the Crux Report design system (Bitter / Source Serif 4 / JetBrains Mono; paper/moss/signal palette) unless the hero direction chosen by Ryan dictates otherwise.

Page structure (single long page, as now):

1. **Hero** — from the winning candidate in `design-tournament/heroes/` (Ryan picks; port it, don't iframe it). Reading always rendered as `XX [lo–hi] · vN.N.N` with sample-data tag until methodology is ratified.
2. **The six dimensions** — cards with score, trend, contributing indicators (expandable, reusing v1's evidence-item components and hover-history modal pattern).
3. **Worldview / sensitivity** — the re-cast cruxes: parameter, current evidence lean (v1 beam component), and its effect on the reading.
4. **Indicators** (reference layer, as v1).
5. **Methodology** — rendered from METHODOLOGY.md (add a tiny md→html step to build.py; stdlib only, subset of markdown is fine).
6. **Update log** (as v1).
7. **Contribute** — links to CONTRIBUTING.md, issue templates, "challenge this number" CTA on every rendered figure (deep-link to a prefilled GitHub issue).

OG/social image: generated at build time (SVG → embedded, or static SVG) containing reading + band + version, so shares carry the caveat. TODO(RYAN): confirm.

## Phase 4 — Repo as a public project

- `METHODOLOGY.md` — full disclosure doc (drafted by strategist, refined during implementation; the compute code must match it exactly — CI asserts the worked example in the doc equals `compute.py` output).
- `CONTRIBUTING.md` — evidence standards (dated primary source, adversarial verification note), PR types, RFC process.
- Issue templates: evidence submission, weight RFC, crux challenge.
- CI (GitHub Actions): JSON schema validation, link-liveness check on changed sources, recompute-and-diff check, build check. PR preview deploys already come from Vercel.
- LICENSE: TODO(RYAN) — suggest CC BY 4.0 for data, MIT for code (dual).
- README rewrite for public audience.

## Phase order & verification

Implement in phase order; each phase lands as a separate PR with the build green. Phase 1+2 are pure data/compute (no visual changes — v1 site keeps rendering until Phase 3 swaps sections in one PR). Definition of done per phase: CI green, `python3 scripts/build.py && python3 scripts/compute.py` clean from fresh clone, worked example in METHODOLOGY.md reproduced by tests.

## Explicitly out of scope (do not build)

Backend, database, accounts, comments, voting, API ingestion, cron automation, analytics beyond Vercel defaults. If a phase seems to need one of these, stop and flag instead of building.
