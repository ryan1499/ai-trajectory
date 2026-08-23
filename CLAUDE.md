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

## Public information architecture

The generated site has six canonical destinations: `index.html` (Overview), `evidence.html`,
`forecasts.html`, `safety.html`, `questions.html` (Research map), and `methodology.html`. Keep topics
grouped by reader task:

- Evidence owns AI R&D evidence, every non-milestone claim card, core measurements, supporting
  signals, and data coverage.
- Forecasts owns Watch next, source comparison, milestone claims, and forecast revisions—in that
  order.
- Safety owns the eight-question hazard-to-recovery chain; Research map owns the separate
  ten-question cross-cutting taxonomy.

Use `metric_href`, `claim_href`, and `safety_href` for cross-page links. Milestone claims are
canonical on Forecasts; all other claim cards are canonical on Evidence. Preserve the legacy-hash
migration in the overview and keep `scripts/build.py`'s cross-page link/fragment validation green.
Do not restore the global Guided/Research toggle: page boundaries provide the information hierarchy,
while `<details>` provides progressive disclosure within a page.

## Privacy is a hard release requirement

- **Never use, print, save, or commit a personal email address.** This includes Git configuration,
  commit metadata, documentation, issue templates, test fixtures, command output, and CI logs.
- Every commit made from this checkout must use a GitHub noreply identity ending in
  `@users.noreply.github.com`. Before creating a commit, run
  `scripts/setup_privacy.sh <github-username>` once per clone; it configures only local Git settings
  and the committed pre-commit hook. Do not copy a private address into that command or into any
  repository file.
- The pre-commit hook checks the configured identity, staged additions, and every tracked text file.
  CI repeats the tracked-content scan and checks every author and committer identity in the public
  checked-out ref's complete ancestry. Both tools intentionally report only pass/fail and counts;
  do not modify them to echo addresses for debugging.
- If a check fails, stop. Fix the identity or remove the sensitive staged content without exposing it
  in logs, commit messages, or issue discussion. There is no bypass for public-repository work.

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
