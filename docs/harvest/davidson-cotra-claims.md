# Extraction: Davidson Takeoff Model &amp; Cotra Bio Anchors

_Recovered verbatim from the session transcript on 2026-07-13 (original harvest agent result was never persisted to disk before compaction)._

**Sources fetched.** Open Phil rebranded to Coefficient Giving (openphilanthropy.org now 301-redirects to coefficientgiving.org; the redirect target itself returned 403 to WebFetch, so quotes below are sourced from the LessWrong mirror of Davidson's report, the interactive model at takeoffspeeds.com, Cotra's original AF/LW posts, and Epoch AI's independent breakdown — flagged per claim). Where two secondary sources gave conflicting numbers, both are shown rather than false-precision-averaged.

---

## PART 1 — Tom Davidson, "What a Compute-Centric Framework Says About AI Takeoff Speeds" (2023)

Primary: https://www.lesswrong.com/posts/Gc9FGtdXhK9sCSEYu/what-a-compute-centric-framework-says-about-ai-takeoff (= AF crosspost; canonical report lives at https://coefficientgiving.org/research/what-a-compute-centric-framework-says-about-takeoff-speeds/, 403'd for me) · Interactive model: https://takeoffspeeds.com/ · Reports index: https://takeoffspeeds.com/reports.html

### Claims

1. **[trajectory]** Central takeoff-duration estimate. "~50% probability: &lt;3 year takeoff" from 20%-automation to 100%-automation (conditional on AGI arriving by 2100). Stage: **AUTOMATION**. Metric: `cognitive-automation-takeoff-duration-years`.
2. **[trajectory]** Full takeoff-duration distribution: ~10% chance &lt;3 months, ~25% chance &lt;1 year, ~50% chance &lt;3 years, ~80% chance &lt;10 years. Davidson: "My personal probabilities are still very much in flux and are not robust." Stage: **AUTOMATION**.
3. **[milestone]** Effective FLOP gap (compute needed to go from 20%-AI to AGI/100%-AI): best guess **10,000x (≈4 orders of magnitude)**, full distribution spans 1–9 OOM, densest around 4 OOM. Stage: **COMPUTE**. Metric: `effective-flop-gap-oom`.
4. **[milestone]** AGI training-compute requirement (2020-algorithm terms): median **~1e36 FLOP**, ±~3 OOM uncertainty; conservative/Bio-Anchors-"long-horizon" scenario 1e38 FLOP; aggressive scenario ~1e31 FLOP (this scenario alone implies ~40% &lt;1yr, ~70% &lt;3yr, ~90% &lt;10yr takeoff). Stage: **COMPUTE**. Metric: `agi-training-flop-requirement`.
5. **[trajectory]** Hardware progress input: Epoch-sourced estimate of FLOP/$ doubling every **~2.5 years**. Stage: **COMPUTE**. Metric: `hardware-flop-per-dollar-doubling-years`.
6. **[trajectory]** Software/algorithmic efficiency input: OpenAI's "Efficiency" analysis cited at **16-month doubling**; Epoch's own analysis at **~10-month doubling**; Davidson's assessment: "Progress is if anything faster for [language models]." Stage: **ALGORITHMS**. Metric: `algorithmic-efficiency-doubling-months`.
7. **[milestone]** Time from AGI to superintelligence: best guess **&lt;1 year "absent humanity choosing to go slower,"** driven by mass availability of AI labor for AI R&amp;D once AGI exists. Stage: **CAPABILITY**. Metric: `agi-to-superintelligence-lag-years`.
8. **[trajectory]** AI-automates-AI-R&amp;D feedback effect at the 20%-AI point: conservative case ~20% of AI-R&amp;D cognitive tasks automated → ~1.3x R&amp;D speedup; aggressive case ~40% automated → ~1.8x speedup. Net effect of the feedback loop: **shortens the 20%→100% interval by ~2.5x** versus a no-feedback baseline. Stage: **AUTOMATION**. Metric: `ai-rd-automation-speedup-multiplier`.
9. **[milestone/value]** At the 20%-AI threshold, Davidson estimates AI "could readily add ~$10 trillion/year to global GDP," against a 2023 baseline of "~$10–100 billion/year" in AI revenue. Stage: **VALUE**. Metric: `ai-attributable-gdp-addition-usd-trillion`.
10. **[milestone/value]** A **$3 trillion/year** economic-impact threshold corresponds to ~6% of cognitive tasks automated in his model; Davidson assigns **~15% probability** that GDP impact stays under $3T/yr before AI reaches a point where it "could disempower humanity." Stage: **VALUE**. Metric: `pre-disempowerment-gdp-impact-usd-trillion`.
11. **[trajectory]** Distinguishes "capabilities takeoff" (~3 years, 20%→100% automation potential) from "impact takeoff" (~10 years, i.e., when GDP actually visibly accelerates), citing historical deployment lag: "Typically takes decades for new technologies to noticeably affect GDP growth, e.g. computers and the internet." Stage: **RESPONSE** (deployment/political-economy lag). Metric: `impact-takeoff-deployment-lag-years`.
12. **[trajectory]** Relationship constraint linking takeoff speed and timeline: "Holding AGI difficulty fixed, decreasing the time from 20%-AI to 100%-AI by two years delays 100%-AI by three years." Stage: **CAPABILITY**. (This is a structural/derived claim, useful as a consistency check across the other metrics rather than a standalone metric.)
13. **[milestone]** Hardware-overgang scenario: if AGI isn't trainable by ~2035, accumulated runtime compute (enough to run "100s of millions of SOTA AIs") could shorten timelines by ~5 years once training-compute requirements are met. Stage: **COMPUTE/CAPABILITY**. Dated, scoreable by 2035.

### 2024–2026 revisions found (Davidson)

14. **[trajectory, secondary-sourced — flag]** A 2025 update to the takeoff-speeds model (incorporating Epoch AI trend data and current-AI R&amp;D-automation estimates) reportedly has hardware scaling slowing from ~4x/yr (through GPT-4) to ~2.5x/yr in the early 2030s, and algorithmic progress slowing from ~3x/yr to ~2.25x/yr over the same window; central scenario pushes AGI arrival forward 1–2 years with potential arrival by **2030**. Source: LessWrong "Takeoff Speeds Update: Crunch Time" (https://www.lesswrong.com/posts/jLEcddwp4RBTpPHHq/takeoff-speeds-update-crunch-time-1) and the May 2025 summary "When will AI automate all mental work, and how fast?" by aggliu/Writer (https://www.lesswrong.com/posts/ykJ8Ku7tKeSCe9fFo/when-will-ai-automate-all-mental-work-and-how-fast) — **not Davidson's own byline**, treat as third-party model re-run, not an author-issued revision.
15. **[milestone, secondary-sourced]** A separately-cited "updated Bio Anchors" calculation (attributed to Davidson, ~2023) reportedly added a recursive-self-improvement term and shifted median AGI date from **2053 → 2043**. I could not independently verify this against a primary Davidson document — flag as unconfirmed pending direct source access.
16. Davidson has since moved to Forethought (https://www.forethought.org/people/tom-davidson) and continues publishing timelines/takeoff work there — no single canonical "2026 update" located in this pass; recommend checking forethought.org directly for anything newer than the 2025 items above.
17. Downstream, non-Davidson work building on his "Full Takeoff Model": the **AI Futures Model, Dec 2025 update** (Eli Lifland, Daniel Kokotajlo, et al. — https://www.lesswrong.com/posts/YABG5JmztGGPwNFq2/ai-futures-timelines-and-takeoff-model-dec-2025-update, blog: https://blog.aifutures.org/p/ai-futures-model-dec-2025-update) gives Eli's all-things-considered view as 10th pct 2027.5 / 50th pct 2032.5 / 90th pct 2085 for AGI-equivalent milestones, and a Superhuman Coder milestone estimate of **December 2031** (vs. Jan 2027/Sep 2028 in their earlier AI 2027 model) — a ~3–5 year lengthening attributed to revised AI-R&amp;D-automation modeling. This is not Davidson's own claim but is the clearest available "someone re-ran his framework with 2025 data" signal.

### Input parameters (candidate metrics) — from takeoffspeeds.com model UI

Category: Training dynamics

- AGI training requirements (FLOP with 2022 algorithms) → `agi_training_flop`
- Effective FLOP gap (training) → `effective_flop_gap_oom`
- R&amp;D parallelization penalty → `rd_parallelization_penalty`
- Training requirements steepness (OOM) → `training_req_steepness_oom`

Category: Resource allocation

- Growth rate of fraction of GWP spent on compute → `gwp_compute_spend_growth_rate`
- Max fraction of compute spent on the training run → `max_fraction_compute_training`

Category: Hardware/software R&amp;D

- Hardware R&amp;D: capital input share, labour input share, compute input share
- Software R&amp;D: capital input share, labour input share, compute input share
- Maximum hardware performance (asymptotic ceiling) → `max_hardware_performance`
- Maximum software performance (asymptotic ceiling) → `max_software_performance`

Category: Initial conditions

- Initial biggest training run (FLOP) → `initial_training_run_flop`
- Initial GWP → `initial_gwp`
- Initial world labour force → `initial_world_labour_force`

These are literally the "what to measure" list — hardware FLOP/$ trend, algorithmic efficiency trend, fraction-of-GWP-on-compute trend, and AI-R&amp;D-automation fraction are the four highest-leverage ones to track against real-world data (Epoch AI publishes the first two continuously).

---

## PART 2 — Ajeya Cotra, "Forecasting TAI with Biological Anchors" (2020) + "Two-Year Update" (2022)

2020 report (LessWrong original): https://www.alignmentforum.org/posts/KrJfoZzpSDpnrv9va/draft-report-on-ai-timelines · 2022 update: https://www.alignmentforum.org/posts/AfH2oPHCApdKicM4m/two-year-update-on-my-personal-ai-timelines · Independent breakdown of the anchor table: https://epoch.ai/blog/grokking-bioanchors

### Claims

18. **[milestone]** 2020 report median TAI year: **~2050** ("A median of ~2050 for transformative AI"). 90th-percentile/near-ceiling: 78–80% by 2100. Stage: **CAPABILITY**. Metric: `median_tai_year`. Note: Epoch AI's independent read of the report's percentile table gives 10th pct 2031 / 50th pct 2052 / &gt;2100 90th — a slightly different median (2052 vs. "~2050") depending on whether you read Cotra's own rounded bottom line or Epoch's table interpolation. Flag both.
19. **[milestone]** 2020 report dated probabilities: **~10% by 2031, ~15% by 2036, ~50% by 2050/2052, ~78–80% by 2100**. Stage: **CAPABILITY**.
20. **[milestone]** 2022 update: median revised to **~2040**, a **10-year** decrease. Direct quote: "A median of ~2040 (a decrease of ~10 years from 2050)." Stage: **CAPABILITY**. Metric: `median_tai_year` (same metric, revised value — this is the single most important trajectory-vs-time data point in the whole extraction).
21. **[milestone]** 2022 update dated probabilities: **~15% by 2030, ~35% by 2036, ~60% by 2050**. Quote: "~15% probability by 2030 (a decrease of ~6 years from 2036). ~35% probability by 2036." Stage: **CAPABILITY**.
22. **[trajectory]** Probability-mass compression: "Previously, my probability increased from 10% to 60% over ~32 years (2032–2064); now this happens over ~24 years (2026–2050)." Stage: **CAPABILITY**. Metric: `p10_to_p60_window_years` — directly falsifiable/scoreable trajectory-shape claim.
23. **[trajectory]** Implied annual hazard rates from the 2022 update: &gt;3% probability/year over 2030–2036; ~4% probability/year over 2036–2040. Stage: **CAPABILITY**. Metric: `annual_tai_probability_rate`.
24. **[milestone]** One-time methodological correction: Cotra applied a **~10x upward adjustment** to her 2020 FLOP/$ hardware-cost baseline, having judged she'd underestimated hardware efficiency. Stage: **COMPUTE**. Metric: `flop_per_dollar_baseline_correction_factor`.
25. **[milestone]** Update triggers / stated reasons for the 2020→2022 revision (functions as her explicit "what would change my mind" list — use as forward-looking falsifiable checkpoints):
    a. Automating AI R&amp;D (rather than all of science) sets a lower capability bar than she'd modeled.
    b. Short-horizon training may suffice without expensive meta-learning — lowers required compute anchor weight.
    c. Explicit "GPT-N anchor" — scaling language models toward brain-equivalent size — added as a distinct path.
    d. Endogenous feedback between R&amp;D investment and progress rate (economy spends more as returns become visible).
    e. Continued deep-learning scaling without a clear counterexample emerging (2020–2022).
    f. Benchmark progress ran faster than forecasters predicted.
    g. The hardware-cost baseline correction (see #24).
    Stage: **RESPONSE** (investment/R&amp;D feedback) + **CAPABILITY** (scaling continuation) — mixed; treat each sub-item as its own scoreable checkpoint against 2026–2030 evidence (e.g., "has deep learning scaling hit a clear wall?" is directly checkable now).
26. **[milestone]** Anchor-by-anchor FLOP table (per Epoch AI's independent reconstruction — **treat as secondary-source reconstruction, not verbatim from Cotra**, since I could not pull the original spreadsheet):

| Anchor                                  | FLOP for TAI                                                           | Weight (Epoch AI reading) |
| --------------------------------------- | ---------------------------------------------------------------------- | ------------------------- |
| Evolution anchor                        | ~1e41                                                                  | 10%                       |
| Lifetime anchor                         | ~1e28 (one search source instead gave ~1e24 — discrepancy, unresolved) | 5%                        |
| Short-horizon NN anchor                 | ~1e32 (alt. source: 1e30, 20% weight)                                  | 15%                       |
| Medium-horizon NN anchor                | ~3e34                                                                  | 30%                       |
| Long-horizon NN anchor                  | ~1e37 (alt: 1e36)                                                      | 15–20%                    |
| Genome anchor                           | ~1e33                                                                  | 10%                       |
| Catch-all / "anchors all underestimate" | —                                                                      | 10%                       |

Stage: **COMPUTE**. Metric per anchor: `tai_flop_threshold_[anchor_name]`. **Flag**: the two independent secondary sources I could access disagree on exact exponents and weights for 3 of 6 rows; before using these numbers in anything load-bearing, pull the original report PDF or Colab notebook directly (referenced in the report but not independently re-fetched here).

### 2024–2026 revisions found (Cotra)

27. **No standalone Cotra-authored update post-2022 was located.** Her "Two-year update" (2022) remains the most recent primary-source revision found. Searches for 2024/2025/2026 Cotra timeline updates returned only discussion of the 2022 post and third-party literature reviews (e.g., https://epoch.ai/blog/literature-review-of-transformative-artificial-intelligence-timelines/, arXiv 2604.22766). If she has published something more recent, it wasn't surfaced by search — worth checking her Open Phil / Coefficient Giving author page and Alignment Forum profile (https://www.alignmentforum.org/users/ajeya-cotra) directly rather than trusting this gap as confirmed absence.

---

## Cross-cutting notes for your tracker

- **Model output vs. author's actual belief**: Davidson repeatedly flags his takeoff-duration probabilities as "not robust" — treat claims 1–2 as _model-conditional outputs_, not settled predictions. Cotra's numbers (18–23) are explicitly her _personal all-things-considered_ estimates, already one level past raw model output — the anchor table (26) is the model-output layer underneath them.
- **Best directly falsifiable-by-2026-2030 claims**: #19/#21 (15% by 2030, 35% by 2036), #22 (probability-mass compression window), #14 (potential AGI arrival by 2030 in the 2025 third-party re-run), #25c/e (has scaling hit a wall / GPT-N anchor holding up) are the cleanest score-by-2030 checkpoints.
- **Gap in my access**: coefficientgiving.org 403'd WebFetch outright, and takeoffspeeds.com's live parameter values/defaults didn't render through WebFetch (JS-rendered page, names only came through). If you want exact current default parameter _values_ (not just names) for the Davidson model, that needs a browser-rendered fetch of takeoffspeeds.com rather than WebFetch.
