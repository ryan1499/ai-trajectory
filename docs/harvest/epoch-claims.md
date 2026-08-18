# Epoch AI: Extracted Dated Projections + Data Series Inventory

_Recovered verbatim from the session transcript on 2026-07-13 (original harvest agent result was never persisted to disk before compaction)._

## PART 1: Numbered Claims

### From "Can AI Scaling Continue Through 2030?" — published August 20, 2024

URL: https://epoch.ai/blog/can-ai-scaling-continue-through-2030

**1.** Power — central projection, single-campus training
&gt; "Data center campuses between 1 to 5 gigawatt (GW)" enabling "training runs ranging from 1e28 to 3e29 FLOP"
Tag: trajectory | value: 1–5 GW / 1e28–3e29 FLOP | date: 2030 | stage: POWER (PHYSICAL) | metric: `frontier-training-campus-power-gw`

**2.** Power — geographically distributed training (upper bound scenario)
&gt; "2 to 45 GW" enabling "training runs of 2e28 to 2e30 FLOP"
Tag: trajectory | value: 2–45 GW / 2e28–2e30 FLOP | date: 2030 | stage: PHYSICAL | metric: `frontier-training-distributed-power-gw`

**3.** Chips — central estimate for training-dedicated fleet
&gt; "100M H100-equivalents could...be dedicated to training to power an 9e29 FLOP training run" (range: "20 million to 400 million H100-equivalents, corresponding to 1e29 to 5e30 FLOP")
Tag: trajectory | value: 100M H100e central / 20M–400M range | date: 2030 | stage: COMPUTE | metric: `training-fleet-h100e-count`

**4.** Data — text token availability
&gt; "Indexed web contains around 500 trillion tokens" (range 100T–3,000T); with multimodal data, "400 trillion to 20 quadrillion effective tokens available for training" by 2030
Tag: trajectory | value: 400T–20Q effective tokens | date: 2030 | stage: COMPUTE (data) | metric: `effective-training-tokens-available`

**5.** Latency — assessed as non-binding
&gt; "Latency is...unlikely to be the binding constraint" — intranode latency of "110 microseconds" per transformer layer (60M token batch) allows "training runs between 2e30 to 2e32 FLOP"
Tag: milestone (bound, not projection) | value: 2e30–2e32 FLOP ceiling | date: 2030 | stage: PHYSICAL | metric: `latency-implied-flop-ceiling`

**6.** Headline central projection — largest training run by 2030
&gt; "Training runs of around 2e29 FLOP are likely possible by 2030" — comparative framing: "2e29 FLOP...exceeds GPT-4 in scale to the same degree that GPT-4 exceeds GPT-2 in scale"
&gt; Constraint hierarchy: "The constraint likely to bind first is power, followed by the capacity to manufacture enough chips"
Tag: milestone | value: 2e29 FLOP central (2e28–2e30 range) | date: 2030 | stage: COMPUTE | metric: `largest-training-run-flop-2030`

---

### Algorithmic efficiency — "Algorithmic Progress in Language Models," published March 12, 2024

URL: https://epoch.ai/blog/algorithmic-progress-in-language-models

**7.** Central algorithmic efficiency doubling estimate
&gt; "The level of compute needed to achieve a given level of performance has halved roughly every 8 months, with a 95% confidence interval of 5 to 14 months."
&gt; Decomposition: "60-95% of performance gains resulted from increased compute and training data, while algorithms accounted for only 5-40% of progress."
Tag: trajectory | value: 8-month halving (5–14mo CI) | date: as of March 2024 (backward-looking fit, treated as ongoing rate) | stage: ALGORITHMS | metric: `algorithmic-compute-efficiency-halving-months`

**8.** Revision/debate note (2025-2026 vintage) — not an official Epoch retraction but relevant methodological pushback surfaced in later literature discussing Epoch's dataset: subsequent analysis (e.g., "On the Origin of Algorithmic Progress in AI," Nov 2025, not an Epoch paper) argues most 2017–2025 gains trace to two scale-dependent innovations (LSTM→Transformer), i.e., a caution flag on the 8-month figure's decomposition rather than a revised headline number. Flag as **uncertain provenance — attribute to third-party critique, not Epoch's own site**, when building the scoreboard.

---

### GATE model — "GATE: Modeling the trajectory of AI and automation," published March 21, 2025

URL: https://epoch.ai/blog/announcing-gate | Sandbox: https://epoch.ai/gate | Paper: https://arxiv.org/abs/2503.04941

**9.** Compute investment share of GDP
&gt; "GATE predicts that the investment in global compute supply may exceed 10% of world GDP, an approximately 50-fold increase over current levels."
Tag: trajectory | value: &gt;10% of world GDP | date: unspecified time horizon (model output, not single-year forecast) | stage: CAPITAL | metric: `global-compute-investment-pct-gdp`

**10.** Growth-rate acceleration under automation
&gt; "AI automation leads to significantly accelerated economic growth, with rates elevated by 2-20 times compared to the recent historical average of ~3% per year." (Epoch's own summary elsewhere phrases the upper end as "30-100% per year" GDP growth in high-automation scenarios.)
Tag: trajectory | value: 6%–60%+ annual GDP growth (2–20x historical) | date: model-scenario-dependent | stage: VALUE | metric: `gdp-growth-rate-under-ai-automation`

**11.** Automation timeline
&gt; "Global economy can marshal enough effective compute to automate most tasks within two decades" (conservative-assumptions scenario)
Tag: milestone | value: most economic tasks automatable | date: ~2045 (within 2 decades of 2025) | stage: AUTOMATION | metric: `task-automation-compute-sufficiency-year`

**12.** Explicit caveat on rigor
&gt; Epoch caveats these are "early results" and "best treated as a qualitative description" rather than precise predictions — this is the load-bearing distinction between GATE's outputs and Epoch's more empirically-anchored compute/power projections.

---

### "Compute scaling will slow down due to increasing lead times" — published September 5, 2025 (authors: Yafah Edelman, Anson Ho)

URL: https://epoch.ai/gradient-updates/compute-scaling-will-slow-down-due-to-increasing-lead-times

**13.** Trillion-dollar cluster — naive vs. lead-time-adjusted
&gt; "At that pace, current trends would predict a trillion dollar cluster around 2030 — but longer lead times would delay this to around 2035."
Basis: OpenAI's compute stock "over $15 billion," growing "around 2.2× each year"; "every additional 10× increase in compute scale lengthens lead times by around a year."
Tag: milestone | value: $1T compute cluster | date: ~2030 (naive) vs ~2035 (lead-time-adjusted, Epoch's revised central case) | stage: CAPITAL/PHYSICAL | metric: `trillion-dollar-cluster-year`

**14.** Near-term scaling continuation despite slowdown
&gt; "Frontier AI labs may still scale training compute at 5× per year for another 1-2 years by allocating a larger fraction of compute to training."
Tag: trajectory | value: 5x/year | date: 2025–2027 | stage: COMPUTE | metric: `training-compute-growth-rate-near-term`

**15.** Lead-time-by-investment-scale table (bounds, not point projections)
GPU rental (&lt;$30M): ~0yr; GPU purchase ($30M–$1B): ~0.5yr; data center ($3B): 1–2yr; very large data center ($10B–$30B): 2–3yr; cutting-edge fab ($300B): 4–5yr.
Tag: trajectory | stage: CAPITAL | metric: `procurement-lead-time-by-investment-scale`

---

### Power demand — "How much power will frontier AI training demand in 2030?" — published August 11, 2025

URL: https://epoch.ai/blog/power-demands-of-frontier-ai-training

**16.** Largest single training run power draw by 2030
&gt; "largest individual frontier training runs in 2030 will likely draw 4-16 gigawatts (GW) of power" — growth rate "2.2x to 2.9x per year" off a 2025 baseline of "largest runs now exceeding 100 MW"
Tag: trajectory | value: 4–16 GW central range | date: 2030 | stage: PHYSICAL | metric: `largest-single-run-power-draw-gw-2030`

**17.** Total AI power capacity, US and worldwide
&gt; "&gt;100 GW of total AI capacity worldwide" and "&gt;50 GW in the US" by 2030, "approximately 5% of total US power generation capacity"
&gt; Explicit uncertainty flag: "It is not certain that this much power growth is actually feasible by 2030, especially at the upper end of the uncertainty range."
Tag: trajectory | value: &gt;100 GW global / &gt;50 GW US | date: 2030 | stage: PHYSICAL | metric: `total-ai-power-capacity-gw-2030`

---

### "Is almost everyone wrong about America's AI power problem?" — published December 17, 2025

URL: https://epoch.ai/gradient-updates/is-almost-everyone-wrong-about-americas-ai-power-problem

**18.** Revised (more recent-vintage) power demand range
&gt; AI data centers will require "30 to 80 GW of power by 2030" under Epoch's central research, though the piece stress-tests an aggressive "100 GW by 2030" scenario against supply-side capacity (gas turbines "well beyond 200 GW" manufacturing capacity through 2030 combined GE Vernova + Siemens; solar ~40 GW/5yr; demand response 76–126 GW; next-gen geothermal 40 GW by 2035).
Tag: trajectory | value: 30–80 GW central (100 GW stress case) | date: 2030 | stage: PHYSICAL | metric: `ai-data-center-power-demand-gw-2030`
Note: this **supersedes/refines** claim #16–17's numbers — later vintage (Dec 2025 vs Aug 2025), narrower band. Flag both with vintage dates on the scoreboard rather than picking one.

---

### "How big could an 'AI Manhattan Project' get?" — published July 2, 2025

URL: https://epoch.ai/gradient-updates/how-big-could-an-ai-manhattan-project-get

**19.** Accelerated-scenario compute milestone
&gt; Under a state-mobilized "Manhattan Project"-style effort (compute investment matching ~0.4–0.8% of GDP, i.e., ~$122B–$244B/year), "a 2e29 FLOP training run by the end of 2027" — "500 times larger than the most compute-intensive model to date," "10,000-fold scale-up over GPT-4," roughly two years ahead of the organic-scaling baseline.
Tag: milestone (explicitly a policy/stress scenario, NOT Epoch's base-rate forecast) | value: 2e29 FLOP | date: end of 2027 | stage: CAPITAL/COMPUTE | metric: `manhattan-project-scenario-flop-2027`

---

### Model-count projections — "How many AI models will exceed compute thresholds?" — published May 30, 2025

URL: https://epoch.ai/blog/model-counts-compute-thresholds

**20.** Models above 1e26 FLOP, median scenario
&gt; "Model counts rapidly increase from 10 above 1e26 FLOP by 2026, to over 200 by 2030" (median scenario). Conservative scenario: ~10–80 by 2027, 61 by 2030. Aggressive scenario: ~80 by 2027, 528 by 2030.
Tag: trajectory | value: 10 (2026) → ~200 (2030) median, with 61–528 range at 2030 | date: 2026–2030 | stage: COMPUTE | metric: `model-count-above-1e26-flop`

**21.** Models above 1e27 FLOP by 2030
&gt; "over 100 models" above 1e27 FLOP by 2030 in the median scenario
Tag: trajectory | value: &gt;100 models | date: 2030 | stage: COMPUTE | metric: `model-count-above-1e27-flop`

---

### Hyperscaler capex vs. cash flow — "Data Insight," snapshot dated June 16, 2026 (live-updating series)

URL: https://epoch.ai/data-insights/hyperscaler-capex-vs-cash-flow

**22.** Capex/cash-flow crossover
&gt; Cash capex growing "about 70% per year" vs. operating cash flow "about 23% per year"; aggregate crossover "around the third quarter of 2026, when aggregate free cash flow reaches zero." Company-level: Oracle already crossed; Amazon crossing "around now" (June 2026); Alphabet ~Q1 2027; Meta ~Q3 2027; Microsoft ~Q3 2028.
&gt; Sensitivity caveat: "starting the operating-cash-flow fit anywhere from Q2 2023 to Q1 2022 moves the aggregate crossover between roughly Q2 and Q4 2026."
Tag: milestone | value: aggregate FCF = 0 | date: Q3 2026 (central, sensitive to fit window) | stage: CAPITAL | metric: `hyperscaler-capex-cashflow-crossover-quarter`
Note: this is a **live Data Insight**, not a static blog post — the underlying chart updates as new quarterly filings land, so the "June 16, 2026" date is a snapshot vintage, not a fixed publication date.

**23.** Related — hyperscaler capex trend growth rate (companion Data Insight, "Hyperscaler capex has quadrupled since GPT-4's release")
URL: https://epoch.ai/data-insights/hyperscaler-capex-trend
&gt; Hyperscaler capex "grown 70% per year since GPT-4 shipped in March 2023"; extrapolated: "If that trend held through 2026, Alphabet, Amazon, Meta, Microsoft, and Oracle would collectively spend $770 billion on capex this year."
Tag: trajectory | value: $770B collective 2026 capex (trend-extrapolated) | date: 2026 | stage: CAPITAL | metric: `hyperscaler-collective-capex-usd`

---

## PART 2: Data Series Epoch AI Actually Maintains (live candidate feeds)

Central hub: **https://epoch.ai/data** — Trends dashboard: **https://epoch.ai/trends** — Data Insights stream: **https://epoch.ai/data-insights**

| Series                               | URL                                             | What it tracks                                                                                                                                                                                                                                                                                                                                      | Cadence (as stated/observed)                                                              |
| ------------------------------------ | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| AI Models database                   | https://epoch.ai/data/ai-models                 | 3,500+ ML models since 1950 — compute, params, data, org, benchmark scores                                                                                                                                                                                                                                                                          | Rolling/continuous; documented at https://epoch.ai/data/ai-models-documentation           |
| AI Benchmarking Hub                  | https://epoch.ai/benchmarks                     | Frontier model performance on hard benchmarks, incl. Epoch-run internal evals                                                                                                                                                                                                                                                                       | Continuous, new model runs added as released                                              |
| AI Data Centers                      | https://epoch.ai/data/ai-data-centers           | Compute/power/construction timelines for large facilities, via satellite + permit data                                                                                                                                                                                                                                                              | Periodic updates as new facilities identified                                             |
| AI Chip Sales                        | https://epoch.ai/data/ai-chip-sales             | Open database of AI chip sales/spending by vendor                                                                                                                                                                                                                                                                                                   | Periodic                                                                                  |
| AI Companies                         | https://epoch.ai/data/ai-companies              | Revenue, funding, staff, compute for frontier labs                                                                                                                                                                                                                                                                                                  | Periodic, tied to earnings/funding events                                                 |
| AI Chip Owners                       | https://epoch.ai/data/ai-chip-owners            | Distribution of leading AI chips/compute capacity across owners                                                                                                                                                                                                                                                                                     | Periodic                                                                                  |
| AI Chip Components                   | https://epoch.ai/data/ai-chip-components        | Advanced logic wafer capacity, CoWoS packaging, HBM memory supply chain                                                                                                                                                                                                                                                                             | Periodic                                                                                  |
| GPU Clusters                         | https://epoch.ai/data/gpu-clusters              | 500+ GPU clusters/supercomputers                                                                                                                                                                                                                                                                                                                    | Periodic                                                                                  |
| Machine Learning Hardware            | https://epoch.ai/data/machine-learning-hardware | 170+ AI accelerators (GPUs/TPUs) specs and performance                                                                                                                                                                                                                                                                                              | Periodic                                                                                  |
| Cyber Vulnerabilities (CVE)          | https://epoch.ai/data/cve                       | Software/hardware vulnerability trends since 2020                                                                                                                                                                                                                                                                                                   | Periodic                                                                                  |
| Polling on AI Usage                  | https://epoch.ai/data/polling                   | AI adoption/usage patterns by demographic                                                                                                                                                                                                                                                                                                           | Periodic, tied to survey waves                                                            |
| Trends Dashboard (aggregated charts) | https://epoch.ai/trends                         | Training compute (5x/yr since 2020, 5.2mo doubling), training cost (3.5x/yr), inference cost (halving ~2mo), compute stock (3.4x/yr), FLOP/s per dollar (1.37x/yr), model capability index "ECI" (15.5 ECI/yr), context windows (30x/yr), memory bandwidth (1.28x/yr), GPU energy efficiency (1.34x/yr), OpenAI revenue growth (3.2x/yr since 2024) | Dashboard snapshot observed updated Feb 5, 2026; no fixed refresh schedule stated on-page |
| Data Insights stream                 | https://epoch.ai/data-insights                  | Short, frequently-updated single-chart analyses (e.g., hyperscaler capex vs. cash flow) — closest thing Epoch has to a "live blog" of metric snapshots                                                                                                                                                                                              | Frequent (roughly weekly-to-monthly cadence based on observed post density)               |
| Gradient Updates newsletter          | https://epoch.ai/gradient-updates               | Longer-form analysis pieces with embedded projections (the source for claims #6, #13-15, #16-19 above)                                                                                                                                                                                                                                              | Roughly weekly; cross-posted to Substack (https://epochai.substack.com)                   |
| GATE model sandbox                   | https://epoch.ai/gate                           | Interactive integrated-assessment model — not a passive data feed, but user-adjustable scenario outputs                                                                                                                                                                                                                                             | Static model version, not a live feed                                                     |

---

## Notes for scoreboard construction

1. **Vintage conflicts are real, not noise.** The single-run power-draw figure moved from "4–16 GW by 2030" (Aug 2025 piece, claim #16) to "30–80 GW total data-center demand by 2030" (Dec 2025 piece, claim #18) — these aren't strictly comparable (single run vs. total capacity) but both should carry their publication date so the scoreboard doesn't silently average across vintages.
2. **GATE outputs are explicitly scenario-dependent**, not point forecasts — Epoch's own language ("early results," "qualitative description") means GATE numbers should be tagged with lower confidence than the compute/power empirical pieces.
3. **The Manhattan Project piece (#19) is a stress-test scenario, not Epoch's base case** — don't let it get pulled into the scoreboard as if it were Epoch's central 2027 projection.
4. **Data Insights (capex/cash-flow, capex-trend) are the closest thing to genuinely live feeds** among the analysis pieces — everything else in the "data hub" proper (models, chips, clusters, hardware) is closer to a maintained database than a narrative projection, and is the stronger candidate set for automated metric ingestion.
