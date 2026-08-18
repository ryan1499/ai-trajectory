# Scoreboard Build Spec — Codex Implementation Contract

**Audience: the executing engineer/model (Codex). This is settled; do not re-open strategy. Strategy lives in [scoreboard-metrics.md](scoreboard-metrics.md) (decisions) and [scoreboard-schema.md](scoreboard-schema.md) (object shapes).**

Read the repo root `CLAUDE.md` first — its data-integrity rules are hard constraints (never rewrite history; generated output never hand-edited; every rendered number traces to a data file).

## What exists

- v1 site: `data/*.json` → `scripts/build.py` (stdlib only) → `dashboard/index.html` → Vercel (`vercel.json`, do not touch build command/output dir). Keep it working.
- Design system: Bitter (display) / Source Serif 4 (body) / JetBrains Mono (data); paper `#eef0e9`, moss `#3c5c48`/`#24392d`, signal `#b5432a`, gold `#a8863a`, ink `#1c2b28`.
- Chosen hero: **"The Argument"** direction (essay-led question decomposing into measurable pieces). Reference mockup: `design-tournament/heroes/candidate-d/index.html` — port its spirit; the organizing idea is **six stages of one feedback loop**.
- Seed data (your worked pattern): `data/scoreboard/metrics.seed.json`, `data/scoreboard/claims.seed.json`.

## Your task (settled engineering only — NOT data population)

Build the machinery that renders the scoreboard from `data/scoreboard/metrics.json` + `claims.json`, driven by the seed files as the shape. Data population (converting `docs/harvest/*.md` into full JSON, and scoring each claim's resolution status/confidence) is a **judgment task retained by the strategist — do not do it**. Build so that when those files are filled in, everything renders.

### Deliverables

1. **`scripts/scoreboard.py`** (stdlib only) — reads `data/scoreboard/*.json`, renders a new scoreboard section. Pure functions; no network.
2. **Rendering**, integrated into the existing single-page flow (extend `build.py` to call it, or a sibling invoked by it — keep one `python3 scripts/build.py` entry point):
   - **Hero** (candidate-d spirit): the question "How fast is AI actually taking off?" decomposing into the six loop stages.
   - **The six-stage loop**: one Tier-1 metric card per stage (Compute/Algorithms/Capability/Automation/Capital/Physical), each showing current value + freshness (`last_checked`, `source_cadence`), sparkline of `history` (reuse v1's hover-modal history component), and the forecast overlays for that metric.
   - **Forecast overlay** (the core visual): on a metric's history, plot each forecast claim's predicted value/date as a labeled marker colored by camp (bull/bear/base-rate/model/wall-street), so "here's reality, here's Leopold, here's Epoch, here's Metaculus" reads at a glance. This is the product — invest here.
   - **Milestone ladder**: the 5 merged rungs, each with the forecasts that bet on it and its resolution state.
   - **Forecast-drift chart** (supporting, not headline): median-estimate-over-time for AGI across sources (Cotra 2050→2040, Kokotajlo 2027→2030, etc.).
   - **Methodology** section rendered from `METHODOLOGY.md` (add a tiny stdlib md-subset → html step).
3. **Freshness model** = event-driven (Ryan decision #4): render each metric's own `last_checked` + `source_cadence`; NO global "updated quarterly" claim anywhere.
4. **Resolution rendering rules** (from AI-2027-tracker study): status and confidence are SEPARATE fields; every claim renders its `counterargument`; self-reported evidence renders with a visible discount marker. Any composite/aggregate number must render its formula inline or not exist.
5. **CI-ready**: JSON schema validation for the two data files; build must run clean from a fresh clone (`build.py` already `mkdir`s output).

### Explicitly out of scope (do not build)

Backend, DB, accounts, live API ingestion, cron, the composite risk _index_ (that's the separate v2-vision layer, later). No new runtime deps. Do not populate data. Do not touch `vercel.json`.

### Definition of done

`python3 scripts/build.py` renders the scoreboard from the SEED files with zero errors from a fresh clone; hero + six-stage loop + one fully-worked metric (metr-task-horizon) with its forecast overlays display correctly; responsive to 375px; `prefers-reduced-motion` respected. Hand back for data population + review.
