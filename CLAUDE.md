# AI Trajectory

Maps AI's trajectory through six measurable forces — COMPUTE, ALGORITHMS, CAPABILITY,
AUTOMATION, CAPITAL, PHYSICAL — compares attributable claims with reality, and keeps unresolved
safety questions separate from measurement. Not a doom-o-meter and not a single risk number.

> **Improving this project? Read [`docs/decisions.md`](docs/decisions.md) first.** It records every
> load-bearing decision (D1–D27), the reasoning, and the conditions under which each should be
> reconsidered — written so a future, more capable model can _attack_ the decisions rather than
> re-derive them blind. Several things that look like bugs are deliberate honesty features and are
> documented there.

## Structure

- `data/scoreboard/metrics.json` — six Tier-1 metrics (exactly one per core stage) plus Tier-2
  supporting metrics. A Tier-2 metric on a core stage renders inside that stage's card; one on a
  non-core stage (`value`, `response`) renders in the standalone supporting strip. Those are the
  only two shapes the renderer knows, and validation rejects anything else.
- `data/scoreboard/claims.json` — every tracked claim, its source type, measurement relationship, and append-only assessment history.
- `data/scoreboard/refresh.json` — review cadence, canonical sources, and the append-only evidence-review log.
- `data/cruxes.json` — unresolved safety questions shown as a non-scored evidence layer.
- `scripts/scoreboard.py` — validation + all rendering. `scripts/template.html` — CSS and shell.
- `scripts/build.py` — the only entry point: `python3 scripts/build.py` (stdlib only, no deps).
- `dashboard/index.html`, `dashboard/methodology.html` — **generated, never edit by hand.**

The build validates before it renders: invalid data fails rather than producing a wrong page.

## Data semantics

- `metric.current` is the headline reading and `metric.history` is the measured series, oldest
  first. `current` is normally the newest history point. Where the metric tracks a frontier maximum
  (METR's horizon is a per-model eval — a weaker later model does not lower the frontier), `current`
  may stay at an earlier peak; that case **must** carry a `current.source_note` saying why, and the
  card renders its `as_of` alongside the date the series runs to, so the divergence is visible
  without opening the notes. A history value of `0` is a real observation (policy rules can be
  revoked), not a gap. History dates are `YYYY`, `YYYY-MM`, or `YYYY-Q1..Q4`; anything else fails
  the build rather than being dropped from the chart in silence.
- `metric.verdict` (≤80 chars) is the one-line editorial read shown on the status board.
- `metric.why_it_matters` explains the force's role in the loop for a first-time reader.
- `claim.predicted.plot_value` is the forecast's target **expressed in that metric's own unit**.
  Omit it when the claim is a rate, a milestone, or about a different quantity than the axis
  measures — those are listed with the claims rather than plotted. **A position on a chart must
  always trace to a recorded number, never to a rendering fallback.**
- `claim.resolution_history` is append-only. Its latest item carries `status` and `confidence` as
  independent fields, plus dated evidence links and a **mandatory** `counterargument`.
- `claim.measurement_relation` is `direct`, `translated`, `proxy`, or `context`. Only direct and
  formula-backed translated claims enter headline totals or plotted claim marks.

## Update protocol

When new evidence lands:

1. Run the evidence-health check and inspect the metric's named canonical sources.
2. Update `current` and append to `history` only when the observation changed.
3. Append a review log entry, including source-lag or access-blocked outcomes.
4. Append a new resolution assessment for affected claims; never edit an earlier assessment.
5. Rebuild and verify in the browser.

Never rewrite history: past values and past resolutions stay as written, even when later evidence
reverses them. Corrections append.

## Principles

- Every displayed number needs a source with a date. No vibes.
- Resolution scoring is human judgment and stays that way — propose resolutions with reasoning,
  never silently automate them.
- Lab-leader statements are intention data; self-reported figures carry a confidence discount.
- Deliberate honesty beats polish: show a stale estimate with its vintage, show what cannot be
  plotted, show the counterargument.
