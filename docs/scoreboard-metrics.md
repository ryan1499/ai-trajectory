# Archived Scoreboard Metrics — Phase 2 Synthesis

**Status: archived Phase-2 synthesis from the July 2026 harvest. Retained for design provenance;
current metric definitions and tiering live in `data/scoreboard/metrics.json`.**

Ranking criteria: **D**iagnosticity (how much a surprise updates the takeoff picture) · **M**easurability (public, refreshable, unambiguous) · **C**overage (how many published forecasts bet on it). Scored ●●● / ●●○ / ●○○.

## Tier 1 — the headline dashboard (7)

| #   | Metric                                                                 | Stage      | D   | M   | C   | Feed                                                                                            | Who's bet on it                                                                                                                                                        |
| --- | ---------------------------------------------------------------------- | ---------- | --- | --- | --- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **METR task-time horizon** (50%-success, + doubling time)              | CAPABILITY | ●●● | ●●● | ●●● | metr.org/time-horizons, live, free                                                              | Forethought (7-mo doubling; 1-month tasks in 3-6yr), AI 2027 (SC milestone driver), Leopold (drop-in remote worker), AI Futures Model (parameter)                      |
| 2   | **Hyperscaler AI capex** (Big-4+, annualized + guidance)               | CAPITAL    | ●●● | ●●○ | ●●● | 10-Qs on EDGAR quarterly; Epoch Data Insights                                                   | Leopold ($500B/yr ~2026, $1T+/yr ~2027), Morgan Stanley ($805B '26, ~$1.1T '27), Epoch ($770B '26 trend; FCF crossover ~Q3 '26), Gartner                               |
| 3   | **Largest training run** (FLOP, confidence-tagged)                     | COMPUTE    | ●●● | ●●● | ●●● | Epoch models DB, weekly, free, CC-BY                                                            | Leopold (~5 OOMs by '27), Epoch (2e29 by 2030 central), AI 2027 (1e28 by mid-'27), Davidson (1e36 AGI median), Cotra (anchor thresholds)                               |
| 4   | **Frontier cluster power** — announced vs **energized** GW             | PHYSICAL   | ●●● | ●●○ | ●●● | SemiAnalysis (paywalled) + press + Epoch data-centers DB; manual triangulation                  | Leopold (1GW '26 / 10GW '28 / 100GW '30), Epoch (4-16GW single run '30; 30-80GW US total '30), AI 2027 (38GW global peak '26)                                          |
| 5   | **Algorithmic efficiency** (compute halving time for fixed capability) | ALGORITHMS | ●●● | ●○○ | ●●● | Epoch papers (episodic — no live series; weakest feed in Tier 1)                                | Leopold (0.5 OOM/yr), Forethought (~3x/yr; r=0.4-3.6), Davidson (10-16mo doubling), Epoch (8mo, CI 5-14)                                                               |
| 6   | **Frontier-lab revenue run-rate** (OpenAI + Anthropic)                 | VALUE      | ●●○ | ●●○ | ●●● | Self-reported, irregular (~monthly during hypergrowth); The Information paywalled               | Leopold ($100B/company milestone), AI 2027 ($140B leading co. by '27), Epoch (OpenAI 3.2x/yr). Reality: Anthropic ~$47B run-rate May '26                               |
| 7   | **AI R&D automation** (milestone ladder + eval proxies)                | AUTOMATION | ●●● | ●○○ | ●●● | Composite: METR horizons on research tasks, RE-Bench-class evals (stale), milestone resolutions | THE hinge in every model: Leopold (automated researcher '27-28), AI 2027 SC (Mar '27 → revised Dec '31 median), Davidson (20%-automation trigger), Forethought (ASARA) |

Notes on Tier 1:

- #7 is milestone-shaped, not a clean series — its "value" is the resolution state of a defined milestone ladder (below). Every takeoff model turns on it, so it stays Tier 1 despite the worst measurability. Its quantitative proxy is #1 measured on research-engineering tasks.
- #5 has no living data series — the honest treatment is "last credible estimate + vintage date" until Epoch or a successor re-measures. This gap is itself worth displaying.

## Tier 2 — supporting (9)

| #   | Metric                                                                         | Stage    | Feed                                                 | Note                                                                                                   |
| --- | ------------------------------------------------------------------------------ | -------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 8   | Inference cost per unit capability                                             | VALUE    | Artificial Analysis, live, free                      | Best capability-normalized cost series; proprietary index caveat                                       |
| 9   | Training-compute growth rate (x/yr, trend)                                     | COMPUTE  | Epoch trends                                         | The Leopold 0.5 OOM/yr vs Epoch lead-time-slowdown fight lives here                                    |
| 10  | Model count above 1e26 FLOP                                                    | COMPUTE  | Epoch, weekly                                        | Epoch's own projection: ~10 ('26) → ~200 ('30) — directly scoreable                                    |
| 11  | US/global datacenter power demand (GW)                                         | PHYSICAL | IEA/EIA annual + Gartner (bot-gated, manual refresh) | Leopold's 20%-of-US-electricity claim scores here                                                      |
| 12  | Grid interconnection queue time                                                | PHYSICAL | LBNL "Queued Up," annual                             | Proxy for the binding constraint; >5yr median now                                                      |
| 13  | AI chip supply (NVIDIA DC revenue + CoWoS/HBM capacity)                        | COMPUTE  | 10-Q quarterly (free); TrendForce bulletins          | Unit volumes paywalled; revenue proxy clean                                                            |
| 14  | Frontier training cost (per-model estimate)                                    | CAPITAL  | Epoch estimates, episodic                            | 2.4x/yr growth; estimates not disclosures                                                              |
| 15  | Export-control & frontier-AI policy events                                     | RESPONSE | Federal Register API — cleanest feed found           | Event series, not a number; pairs with EU AI Act dates                                                 |
| 16  | AGI timeline meta-forecast (Metaculus median + named-expert medians over time) | meta     | Metaculus (bot-gated but readable)                   | The "forecast drift" chart: Cotra 2050→2040, Kokotajlo 2027→Dec 2030, Lifland → ~2035, Metaculus ~2033 |

## Tier 3 — watchlist

Robot production & count doubling time (Forethought industrial-explosion trigger; AI 2027: 1M/month by 2028) · GPU rental prices (JS-scrape needed) & utilization (**undisclosed anywhere — dead until someone publishes**) · lab "% code AI-written" (self-reported tier only) · enterprise AI spend aggregates (Menlo/Gartner, incommensurable methodologies) · sovereign compute programs (no aggregator; manual) · AI share of GDP investment (**no official series exists**; BEA experimental — labeled proxy or nothing) · China compute share (AI 2027 bets 12%→10%; sourcing hard) · frontier security-level milestones (RAND SL ladder) · public salience polls.

## The milestone ladder (for #7 and milestone claims)

Canonical rungs, merged across papers so different forecasts overlay the same rung: **(a)** agent completes 1-month-human-equivalent research task (METR-measurable) → **(b)** Superhuman Coder (AI 2027 definition) → **(c)** automated AI researcher / ASARA (Leopold, Forethought) → **(d)** AI R&D speedup multipliers (2x → 10x, per lab/eval evidence) → **(e)** AGI-class (definitions differ — record each author's own). Each rung: pending/partial/resolved with evidence, counterargument, and confidence.

## Schema addenda adopted from the AI 2027 tracker study

1. **Status ≠ Confidence** — two independent fields on every resolution.
2. **Mandatory counterarguments** on every resolution, including "Confirmed."
3. **Evidence hierarchy** with explicit tiers; lab-leader statements = intention data; self-reported figures carry a confidence discount, not just a footnote.
4. **Canonical-source resolution step**: where a paper conflicts with itself (AI 2027's two multiplier tables; its Agent-0 text-vs-chart figures), record the conflict and pick a canonical reading _before_ scoring, documented.
5. **Charitable-interpretation rule** for vague claims, stated per claim.
6. **No silent changes** — per-claim changelog (we already run append-only updates.json; extend the discipline).
7. **Any composite "pace ratio" must publish its formula** — the community tracker's 0.70x headline is undisclosed; ours will be reproducible or absent.
8. **Second-reviewer mechanism** — GitHub PRs + maintainer sign-off gives us this for free; the single-maintainer tracker can't.

## Forecast-source roster (v1)

Bulls: Aschenbrenner (2024), AI 2027 original (Apr 2025). Revised bulls: AI Futures Dec 2025 update. Base rates: Epoch (vintaged), Metaculus. Models: Davidson takeoff, Cotra bio-anchors (2020 + 2022 revision), Forethought SIE (with log-uniform ranges preserved). Bears: Erdil multi-decade (wave 2 extraction). Wall Street: Morgan Stanley, Gartner (capex/power only). **Every claim carries: author, vintage, conditionality verbatim, canonical quote, metric_id, resolution {status, confidence, evidence, counterargument}.**

## Phase 3 cut — DECIDED (2026-07-13)

1. **Tier 1 = 6, one metric per core loop stage** (Ryan: "whatever you think"). The six headline metrics ARE the six load-bearing stages of the takeoff loop — a clean, defensible spine and the organizing idea for the hero:
   - COMPUTE → `largest-training-run-flop`
   - ALGORITHMS → `algorithmic-efficiency` (kept despite no live feed — it's the compute-vs-insight hinge every model bets on; displayed as "last credible estimate + vintage," and that staleness is itself shown)
   - CAPABILITY → `metr-task-horizon`
   - AUTOMATION → `ai-rd-automation` (milestone ladder)
   - CAPITAL → `hyperscaler-capex`
   - PHYSICAL → `frontier-cluster-power` (announced vs energized)
   - Demoted to lead Tier 2: frontier-lab revenue (VALUE) and export-control/policy events (RESPONSE) — both strong, but VALUE and RESPONSE are modulators of the loop, not stages of it.
2. **Milestone ladder: MERGE** across papers (5 rungs), so different forecasts overlay the same rung.
3. **Forecast-drift chart: SUPPORTING**, not headline.
4. **Cadence: EVENT-DRIVEN** — update a metric when its underlying data actually moves (an earnings call, a METR release, a policy action), not on a fixed calendar. Each metric carries its own `last_checked` and `source_cadence`; the site shows freshness per metric rather than claiming a global refresh rhythm. This is more honest than "quarterly" and matches how the data actually arrives.

Implementation contract: docs/scoreboard-build-spec.md.
