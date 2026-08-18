# Methodology

The scoreboard compares **dated, falsifiable claims** with the public measurements they predict. Sources are classified as forecasts, scenarios, model outputs, trend projections, intentions, or analysis. It is not a composite risk index, and it does not turn unlike metrics into one headline number.

## Data integrity

- Structured files in `data/scoreboard/` are the only source for observations, forecasts, resolution judgments, and dates.
- Forecast wording and conditionality stay attached to the original claim. `epistemic_type` keeps scenarios, model projections, and lab intentions from being presented as ordinary forecasts.
- `measurement_relation` distinguishes direct, translated, proxy, and context claims. Only direct and formula-backed translated claims enter headline status totals or chart overlays.
- Metric history, evidence reviews, and `resolution_history` are append-only. A later reversal adds an entry; it does not rewrite the earlier record.
- Every assessment links to at least one canonical measurement source; the original claim links to its published source. Observation tables distinguish named-series links from compiled points that still lack a direct point citation.
- Each metric has a machine-readable review policy and append-only review log. Review freshness and observation vintage are displayed separately: checking a source does not make an old observation new.

## Reading a resolution

**Status** says how the claim currently compares with the evidence. **Confidence** says how strongly that status is supported. They are deliberately separate. Every resolution also includes the strongest counterargument available in the structured record.

The six statuses on the board:

- **pending** — the claim's window is still open and no measurement yet bears on it.
- **on-track** — the measured series is running consistent with what the claim requires.
- **ahead** — reality is running faster or further than the claim required by now.
- **behind** — reality is running short of the pace the claim required by now.
- **resolved true** — the target was met; the claim is settled in the forecaster's favour.
- **falsified** — the window closed without the target being met, or the evidence moved decisively against it.

**Confidence** is an integer from 0 to 100 recording how strongly the evidence supports _that status call_. It is not a probability that the forecast comes true, and it is not a percentile.

Every status is the tracker's judgment, not the source author's. Disagreeing with one is the intended use of this site — open an issue or a PR against the data. Each assessment records its test, target, deadline, measurement relationship, and uncertainty driver. Headline inventories include only direct or explicitly translated claims.

Self-reported evidence is useful but receives a visible confidence discount. Where a source is ambiguous or internally inconsistent, the data record must document a canonical reading before the claim is scored.

## Forecast camps

Each forecast marker and claim chip is coloured by **camp** — the tracker's classification of the kind of argument the source is making. The label is assigned here, not claimed by the forecaster, and calling someone a "bull" is itself a claim; it colours the chart so a reader can see which kinds of reasoning cluster where, and nothing more.

- **bull** — argues takeoff is fast and near-term.
- **bear** — argues it is slower, later, or bounded.
- **base rate** — reasons by extrapolating an established historical trend.
- **model** — output of an explicit quantitative model or a published scenario.
- **wall street** — sell-side and financial-institution forecasts.

Camps are never averaged, weighted, or scored against each other. Reality adjudicates.

## Charts and calculations

Reality lines use the metric's recorded history. Forecast markers use each comparable claim's own target and date; date ranges remain ranges. Proxy and context claims remain in the ledger but are not plotted or aggregated. Qualitative milestones appear as diamonds rather than being assigned invented numeric values.

A claim takes a height on a chart only when a human has recorded `predicted.plot_value` in that metric's own unit. Nothing is inferred from the claim's prose — a target stated in different units (a duration on an hours axis, an annual total on a quarterly axis) is converted by hand, and the conversion is recorded as a `plot_note` that renders under the chart. Claims with no recorded value, and claims about a quantity the axis does not measure, are left off the chart; every chart says in its caption how many of its claims are plotted and where the rest are recorded.

No composite or aggregate is published unless its formula is shown inline. This version publishes none.

## Reading the safety questions

The safety layer is scoped to severe and catastrophic risks from frontier general-purpose AI; it is not a complete taxonomy of every AI harm. Its eight questions follow a causal chain: hazard, exposure, control, governance, incidents, and resilience.

The visual form follows the evidence. A spectrum is used only when two opposing operational states are defensible; its dot is an editorial, source-reviewed synthesis and its band is interpretive disagreement, not a probability or statistical confidence interval. Dangerous uplift uses a domain matrix because cyber, CBRN, manipulation, and autonomy can differ. Deployment uses an exposure ladder but shows no current rung without representative telemetry. Incidents use a ledger rather than a trend because reporting coverage and denominators are unstable.

Every reading separately records evidence setting, independence, coverage, observation period, limitations, and what would change it. No position is combined into an overall risk or safety number.

## Updating the scoreboard

Run `python3 scripts/refresh.py` to see which evidence streams are due. Check the named canonical sources, append a review outcome even when the source has not changed, append new observations or resolutions rather than replacing old ones, and rebuild with `python3 scripts/build.py`. Automated retrieval may prepare evidence candidates; it never changes a resolution status without human sign-off.
