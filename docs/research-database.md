# Question-First Research Database

**Status: foundation, 2026-08-12.** The research registry adds a durable information architecture behind AI Trajectory. It does not create a risk score, overwrite historical tracker data, or add a backend. Its job is to make the project easier to extend and easier to audit.

## The reader-facing rule

The public interface should begin with only a short answer to a question: a one-line reading, its freshness, and the next useful action. Detail appears only when the reader asks for it.

The intended progression is:

1. **Overview** — a small set of plain-language questions, each with a short state such as measured, open, or missing data.
2. **Question page** — separate lanes for observed reality, named published views, and group expectations; one primary chart or evidence card at a time.
3. **Evidence detail** — exact source, vintage, methodology, counterargument, and relationship to the question.

Never show a wall of metrics, source names, numbers, or confidence labels on the overview. A coverage gap is itself useful information and may be shown as a short, calm “not yet measured” state.

## Registry files

| File | What it owns | What it does not duplicate |
| --- | --- | --- |
| `data/research/questions.json` | The canonical ten-question map, evidence lanes, state, linked metrics/cruxes, and what would change the current reading | Individual data points and claims |
| `data/research/sources.json` | Source identity, epistemic type, provenance expectations, and dependency clusters | Forecast values or source-derived observations |
| `data/research/evidence-map.json` | Links from a question to an existing metric, crux, claim portfolio, or visible coverage gap | Metric and claim content |
| `data/research/aggregate-signals.json` | Registered panel/platform sources and exact conditions for future imports | Unsourced aggregate values |
| `data/research/ai-rd-evidence.json` | Dated empirical evidence for the AI R&D feedback question, including its source artifact, directness, and caveat | A ladder resolution, a blended productivity multiplier, or a forecast |
| `data/research/safety-questions.json` | The eight-question severe-risk causal chain, question-specific visual form, current reading, evidence quality, indicators, gaps, and update conditions | A composite risk score or the archived worldview-crux positions |

Existing measurements remain in `data/scoreboard/metrics.json`; published claims remain in `data/scoreboard/claims.json`; open crux evidence remains in `data/cruxes.json`. The registry references their IDs so there is one canonical copy.

## The severe-risk causal chain

The public safety layer is narrower and more operational than the archived seven worldview cruxes. It asks eight questions across hazard, exposure, control, governance, observed outcomes, and resilience. A spectrum is allowed only where two operational poles are defensible. Domain matrices, exposure ladders, and incident ledgers are used when a single pole position would erase important differences or invent a denominator.

Each safety question must record the evidence setting, independence, coverage, observation period, caveat, measurement gaps, and what would change the current reading. Missing public telemetry stays missing; it is never replaced with a convenient proxy or a midpoint dot presented as knowledge.

## The three evidence lanes

### Observed reality

Measurements, primary records, independently verified evaluations, and documented incidents belong here. An observation needs a date, unit or event definition, methodology version where relevant, and a source locator. Announced capacity and energized capacity are different observations; a source headline is not a point-level citation.

### AI R&D feedback evidence package

`ai-rd-evidence.json` is an intentionally non-scoreable evidence package for the question “Is AI accelerating the creation of better AI?” It records the closest available public evidence without pretending that unlike measurements answer the same question.

- `benchmark-evaluation` is a capability signal only. It must never be rendered as an observed R&D speedup.
- `randomized-field-experiment` is causal evidence about the studied work setting. It remains **adjacent** unless it directly studies frontier AI R&D.
- `technical-worker-survey` is a self-report signal, not observed productivity.
- `company-operational-report`, `company-deployment-report`, and `company-autonomous-research-demo` can have direct relevance to AI R&D but remain company-reported observations, not independent direct evidence, until audited or replicated.

Each observation has one `directness` label, a direction relative to the feedback question, a source artifact with its publication date, and a concrete caveat. The compact `current_synthesis` must name both the strongest direct evidence and the strongest counterevidence, and must state the missing measurement. It is a qualitative reading, not a numeric aggregate.

### Named published views

This lane records dated claims from influential documents, models, and institutions. It must preserve whether an item is a forecast, scenario, model output, trend projection, analysis, or company intention. A source can be important to track without becoming a high-weight source of truth.

### Aggregate expectations

Panels, expert surveys, forecasting platforms, and markets are aggregate beliefs—not observations. A stored snapshot must preserve exact question wording, resolution criteria if applicable, capture date, aggregation method, participant/sample information when available, and its source URL. Aggregate values must not be imported when their target only loosely resembles a tracker question.

The registry contains one deliberately narrow historical snapshot: the October 2023 ESPAI randomized subset (299 responses) on whether AI doing nearly all R&D could create a tenfold-under-five-years feedback loop. Its complete category distribution, fielding window, source question, and publication vintage are stored together. It is not a current consensus or a probability of takeoff.

LEAP remains registered without a snapshot for AI R&D. Its Wave 4 AI-written-paper/Test-of-Time question is informative but is not a direct measure of the feedback loop: recognition has cultural lag and “written in part” has a lower threshold than autonomous research. Metaculus also remains registered without a snapshot until an authorized question with matching resolution rules is located. This prevents a plausible but mismatched number from becoming a dashboard fact. Metaculus is a community forecasting platform, not a prediction market.

## Source inclusion and weighting policy

Influential people and works are tracked because they shape the live AI trajectory conversation. Their prominence is a reason for **coverage**, not a reason for a larger numeric weight.

The project does not create a prestige-weighted master forecast. Where forecasts eventually have an identical target, horizon, unit, and resolution rule, an explicitly documented aggregation may be considered only after pre-registering the method. Otherwise, views display side by side.

When assessing a claim or choosing which evidence deserves review priority, use these qualitative checks:

1. Is the target and date/resolution rule explicit?
2. Was the statement made before the outcome was known, and is its original vintage preserved?
3. Is the source close to the relevant domain or underlying primary record?
4. Is the reasoning/method transparent and reproducible?
5. Is the item independent of other sources already represented?
6. Does it have a relevant resolved track record, without retrofitting a score across unlike claims?
7. For group forecasts, are the question definition, sample/participation, and aggregation method visible?

Company statements are recorded as intention or disclosure evidence and receive no special authority merely because of the speaker’s role. Forecast-family clustering prevents the original AI 2027 scenario, its revisions, derivative commentary, and market reactions from being counted as independent support.

## Versioning, corrections, and review

- The existing metric histories and claim assessments remain append-only.
- A new source version, model update, or method break gets a new record or explicit supersession link; it never silently replaces the original.
- A review date means the tracker checked a source. It is not an assertion that the underlying observation itself is recent.
- A missing source, indirect proxy, or unresolved disagreement is exposed as coverage debt rather than filled with an estimate.

Run `python3 scripts/research_registry.py` before integrating registry data into a page. The validator rejects broken tracker references, invalid evidence lanes, missing dependency clusters, undeclared versions, non-exact aggregate mappings, source-level prestige-weight fields, and AI R&D evidence whose category, directness, source artifact, or question link is inconsistent.

## A small UI contract for future work

An overview card should contain no more than:

- the question;
- a plain-language state;
- one featured observation or explicit gap; and
- a route to explore it.

Question detail may reveal the three evidence lanes. Source lineage, methodology, quotes, and assessment counterarguments belong in a final “inspect the evidence” layer. Do not reintroduce a global score, source leaderboard, or an unlabelled blended forecast in the name of simplicity.
