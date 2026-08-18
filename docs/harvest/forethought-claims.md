# Forethought Intelligence-Explosion Claims — Extraction

_Recovered verbatim from the session transcript on 2026-07-13 (original harvest agent result was never persisted to disk before compaction)._

**Sources fetched (all forethought.org unless noted):**

- **[A]** "Preparing for the Intelligence Explosion" — MacAskill &amp; Moorhouse, March 2025 (arXiv 2506.14863) — https://www.forethought.org/research/preparing-for-the-intelligence-explosion
- **[B]** "How Quick and Big Would a Software Intelligence Explosion Be?" — Tom Davidson, August 2025 — https://www.forethought.org/research/how-quick-and-big-would-a-software-intelligence-explosion-be
- **[C]** "Three Types of Intelligence Explosion" — Rose Hadshar, Tom Davidson, Will MacAskill, March 17, 2025 — https://www.forethought.org/research/three-types-of-intelligence-explosion
- **[D]** "Will AI R&amp;D Automation Cause a Software Intelligence Explosion?" — Daniel Eth &amp; Tom Davidson, March 2025 — https://www.forethought.org/research/will-ai-r-and-d-automation-cause-a-software-intelligence-explosion
- **[E]** "The Industrial Explosion" — Tom Davidson &amp; Rose Hadshar — https://newsletter.forethought.org/p/the-industrial-explosion

Note on conditionality: **every** number in B, C, D and most in A/E is conditional on some combination of (i) full/near-full automation of AI R&amp;D ("ASARA" = "Automated System for AI R&amp;D Automation"), (ii) hardware/compute held constant post-automation, (iii) no human-imposed bottlenecks (safety pauses, legal review, regulation), and (iv) continuation of current scaling-law trends without a paradigm shift. I've reproduced each claim's specific condition verbatim where the source states one distinct from this general frame.

---

## Claim list

### [A] Preparing for the Intelligence Explosion

1. **"the estimated amount of raw computation used in notable frontier training runs has been scaling up by around 4.5x per year since 2010"** — §Current trends. Condition: historical baseline, not forward-looking. Tag: trajectory · 4.5x/yr · COMPUTE · metric: `training_compute_growth_yoy`

2. **"physical computation required to train a model at the same level of performance is falling by roughly 3x per year"** — §Current trends. Tag: trajectory · 3x/yr · ALGORITHMS · metric: `algorithmic_efficiency_gain_yoy`

3. **"Effective training compute from pretraining is increasing by over 10x per year"** — §Current trends. Tag: trajectory · &gt;10x/yr · COMPUTE · metric: `effective_training_compute_growth_yoy`

4. **"post-training enhancements currently provide a further 3x efficiency improvement per year"** — §Current trends (attributed as an Anthropic informal estimate). Tag: trajectory · 3x/yr · ALGORITHMS · metric: `post_training_efficiency_gain_yoy`

5. **"as if physical training compute is scaling more than 30x per year"** — §Current trends (compute+algo+post-training combined). Tag: trajectory · &gt;30x/yr equivalent · CAPABILITY · metric: `combined_effective_capability_growth_yoy`

6. **"GPT-4 was trained using roughly 100,000 to 1 million times as much effective training compute as GPT-2" ... "If we also factor in post-training enhancements, effective compute likely grew by closer to ten million-fold"** — §Current trends. Timeframe: "four years." Tag: milestone (historical) · 10^5–10^6x (pretraining) / ~10^7x (incl. post-training) over 4 yrs · CAPABILITY · metric: `gpt2_to_gpt4_effective_compute_multiple`

7. **"GPT-3.5 was released at initial cost of $20 per million tokens... today... around $0.04 per million tokens; a 500x drop over less than 3 years"** — §Current trends, ~10x/yr. Tag: trajectory · 500x in &lt;3yr (~10x/yr) · VALUE · metric: `inference_cost_per_token_decline`

8. **"amount of physical compute available for inference is increasing at a rate of very roughly 2.5x per year"** — §Current trends. Tag: trajectory · 2.5x/yr · COMPUTE · metric: `inference_compute_available_growth_yoy`

9. **"could support growing the 'AI population' by about 25x per year"** — §Current trends. Condition: "at near-frontier capability levels." Tag: trajectory · 25x/yr · AUTOMATION · metric: `ai_population_growth_yoy`

10. **"total AI cognitive labour is growing more than 500x faster than total human cognitive labour"** (human research effort growing "less than 5% per year") — §Progress in AI capabilities intro. Tag: trajectory (comparative) · &gt;500x faster · AUTOMATION · metric: `ai_vs_human_cognitive_labor_growth_ratio`

11. **"biggest training runs can continue to scale for roughly another 10,000x increase before running into power and other limits"** — §How far could AI keep improving? Timeframe: "likely well within a decade." Tag: milestone (ceiling) · 10,000x, &lt;10yr · COMPUTE · metric: `training_compute_headroom_to_power_limit`

12. **"we'll see a further 1,000x increase in algorithmic efficiency in training" ... "over a decade"** — same section. Tag: milestone · 1,000x/decade · ALGORITHMS · metric: `algorithmic_efficiency_headroom_decade`

13. **Moderate/no-feedback-loop 10-yr scenario: "product of training compute, algorithmic efficiency, and inference compute... increased one hundred billion-fold" ("just over 10x per year")** — §How far could AI keep improving? Condition: "No feedback loop." Tag: trajectory · 10^11x/decade, ~10x/yr avg · CAPABILITY · metric: `decade_capability_growth_no_feedback`

14. **With software feedback loop: "AI capabilities could cover another factor of one million-fold in effective training compute within the same decade" → "trillion-fold (10^12)" in effective training compute; overall "ten quadrillion-fold (10^16) increase... roughly 40x per year"** — same section. Condition: "if" software feedback loop occurs. Tag: milestone/trajectory · 10^12–10^16x/decade, ~40x/yr · CAPABILITY · metric: `decade_capability_growth_with_feedback_loop`

15. **"product of inference compute and effective training compute is growing at least 600 times faster than all human cognitive labour"** — same section. Tag: trajectory (comparative) · ≥600x faster · AUTOMATION · metric: `ai_vs_human_growth_ratio_compute_adjusted`

16. **Moderate scenario table: training compute 2.5x/yr→10,000x; algorithmic efficiency 2x/yr→1,000x; inference compute 2.5x/yr→10,000x; "AI research effort ⩾12x/yr→⩾10^11x"; "AI vs human research effort ⩾300x faster"** — §Estimates of AI progress over the coming decade. Condition: "Moderate Scenario (No feedback loop)." Tag: milestone · ≥12x/yr, ≥10^11x/decade · AUTOMATION · metric: `moderate_scenario_ai_research_effort_growth`

17. **Rapid scenario table: algorithmic efficiency 8x/yr→10^9x; "AI research effort ⩾50x/yr→⩾10^17x"; "AI vs human research effort ⩾1000x faster"** — same section. Condition: "Rapid Scenario (Software feedback loop)." Tag: milestone · ≥50x/yr, ≥10^17x/decade · AUTOMATION · metric: `rapid_scenario_ai_research_effort_growth`

18. **"AI research effort will reach parity with human research labour within the next two decades" ... "AI could even approach human parity well within the coming decade"** — §AI-human cognitive parity. Tag: milestone · parity within 10–20yr · AUTOMATION · metric: `ai_human_research_parity_date`

19. **"maximum duration of ML-related tasks [AI models can complete]... has been doubling roughly every seven months"** — §AI-human cognitive parity (METR trend). Tag: trajectory · 7-month doubling · CAPABILITY · metric: `metr_task_horizon_doubling_time`

20. **"within three to six years, AI models will become capable of automating many cognitive tasks which take human experts up to a month"** — §AI-human cognitive parity. Condition: "Naively extrapolating this trend" [the METR doubling trend above]. Tag: milestone · 3–6yr · CAPABILITY · metric: `1_month_task_automation_date`

21. **Conservative post-parity scenario: "AI research effort would continue scaling, on average, at 5x per year for the decade following human parity" → "~10^7x (5x/yr)"** — §How much more AI research effort after AI-human parity? Condition: "Conservative" scenario, post-parity. Tag: trajectory · 5x/yr, 10^7x/decade · AUTOMATION · metric: `post_parity_conservative_growth`

22. **Aggressive post-parity scenario: "25x (~10^14x total)"** — same section. Condition: "Aggressive" scenario, post-parity. Tag: trajectory · 25x/yr, 10^14x/decade · AUTOMATION · metric: `post_parity_aggressive_growth`

23. **"To drive a century in a decade, total research effort would need to increase by a factor of 600 or more"** growth rate "around 100% (one doubling) per year" — §The technology explosion. Tag: milestone · factor ≥600, 1 doubling/yr · VALUE · metric: `research_effort_multiple_needed_for_century_in_decade`

24. **"on a default path where we keep scaling AI without collectively agreeing to slow down, a century's worth of technological progress in a decade seems likely"** — §The technology explosion. Condition: "default path," no explicit % given (qualitative "likely"). Tag: milestone · timeframe: within a decade · VALUE · metric: `century_of_progress_in_decade_likelihood`

25. **"we could increase global primary energy consumption by 100x by capturing the solar energy incident on less than 2% of oceans or deserts"** (current baseline: "Humans produce the equivalent of roughly 0.01% of the energy from sunlight that reaches Earth") — §The industrial explosion. Tag: milestone (technical ceiling) · 100x · PHYSICAL · metric: `global_energy_capacity_ceiling_solar`

26. **"[Robot manufacturing] output could double every few years or even months"** — §The industrial explosion, based on "current rates of manufacturing factories and robots." Tag: trajectory · doubling every months–years · PHYSICAL · metric: `robot_output_doubling_time`

### [B] How Quick and Big Would a Software Intelligence Explosion Be?

27. **"~60%"** probability of **"&gt;3 years of AI progress into &lt;1 year"** — §Results/Summary. Condition: "conditional on ASARA being deployed internally... hardware held constant post-ASARA... no human bottlenecks." Tag: milestone · 60% probability, compress 3yr→1yr · ALGORITHMS · metric: `p_3yr_progress_in_1yr`

28. **"~20%"** probability of **"&gt;10 years into &lt;1 year"** — same section/condition. Tag: milestone · 20% probability, compress 10yr→1yr · ALGORITHMS · metric: `p_10yr_progress_in_1yr`

29. **"~40%"** probability of **"&gt;3 years into ≤4 months"** — same section/condition. Tag: milestone · 40% probability · ALGORITHMS · metric: `p_3yr_progress_in_4mo`

30. **"~10%"** probability of **"&gt;10 years into ≤4 months"** — same section/condition. Tag: milestone · 10% probability · ALGORITHMS · metric: `p_10yr_progress_in_4mo`

31. **Initial speed-up on ASARA deployment: "Median of 8"**, range **"2–32"** (log-uniform) — §Parameter estimates. Condition: "at the point ASARA is first developed." Tag: milestone · median 8x, range 2–32x · AUTOMATION · metric: `initial_asara_speedup_multiplier`

32. **"Median estimate of r_cog is 1.2"**, log-uniform bounds **"0.4 to 3.6"** — §Returns to software R&amp;D. Tag: trajectory (parameter) · r_cog=1.2 (0.4–3.6) · ALGORITHMS · metric: `r_cog_returns_parameter`

33. **"6 – 16 OOMs of efficiency gains"** before hitting effective limits, "≈6–16 years worth of AI progress" at recent rates — §Distance to effective limits. Tag: milestone (ceiling) · 6–16 OOM · ALGORITHMS · metric: `software_efficiency_headroom_ooms`

34. **"Software has recently been doubling every 3 months"** (effective compute "~10X/year") — §Historical baselines. Tag: trajectory · 3-month doubling / ~10x/yr · ALGORITHMS · metric: `recent_software_doubling_time`

35. **"Half of recent AI progress comes from using more compute" and "the other half comes from improved software"** — §Historical baselines. Tag: trajectory (split) · 50/50 · COMPUTE/ALGORITHMS · metric: `compute_vs_software_progress_share`

36. **"Median estimate is p = 0.3"**, log-uniform **"0.15 to 0.6"** (diminishing returns to parallel labour) — §Parameter estimates. Tag: trajectory (parameter) · p=0.3 (0.15–0.6) · AUTOMATION · metric: `p_parallel_labor_diminishing_returns`

37. **"Three years to go from GPT-2 to ChatGPT (GPT-3.5)" ... "Three years to go from GPT-3.5 to o3"** — §Historical reference points. Tag: milestone (historical) · 3yr per step · CAPABILITY · metric: `gpt_generation_interval_years`

### [C] Three Types of Intelligence Explosion

38. **Software IE "~50% likely"** to accelerate independently — §Will AI progress accelerate over time? Tag: milestone · 50% probability · ALGORITHMS · metric: `p_software_ie_accelerates`

39. **AI-technology IE: "~65%"** (chip-technology loop alone) → **"~75%"** combined probability — same section. Tag: milestone · 65%/75% probability · COMPUTE · metric: `p_ai_tech_ie_accelerates`

40. **Full-stack IE: "~80%"** (chip-production loop alone) → **"~90%"** combined probability — same section. Tag: milestone · 80%/90% probability · PHYSICAL · metric: `p_full_stack_ie_accelerates`

41. **Effective-compute ceilings: software feedback loop "~12 OOMs"; AI-technology IE "~18 OOMs or more"; full-stack IE "~23 OOMs using earth-based energy, or ~32 OOMs using all solar energy"** — §How far could AI progress before hitting effective physical limits. Tag: milestone (ceiling) · 12/18/23–32 OOM · CAPABILITY · metric: `effective_compute_ceiling_ooms_by_ie_type`

42. **"It takes ~3 months to train new SOTA AI"** [software loop cycle time] vs. **"years to build new fabs"** [chip-production loop cycle time] — §Time lags in each feedback loop. Tag: trajectory (cycle time) · 3mo vs. multi-year · COMPUTE/PHYSICAL · metric: `feedback_loop_cycle_time`

43. **"Epoch estimates 0.8 to 3.5 doublings of output per doubling of input across several domains"**; refined to **"1.2 doublings... range of 0.4 to 3.6"** (Davidson &amp; Houlden 2025) — §Will AI progress accelerate over time? Tag: trajectory (parameter) · r=0.8–3.5, refined 1.2 (0.4–3.6) · ALGORITHMS · metric: `software_r_returns_parameter` (same underlying parameter as claim 32)

### [D] Will AI R&amp;D Automation Cause a Software Intelligence Explosion?

44. **Image recognition: efficiency "doubling time" of "15 months"** (runtime, 2012–2017) and **"16 months"** (training, 44x drop 2012–2019); Epoch estimate **"9 months"** (training, 2012–2022) — §Improvements in AI software are already driving fast AI progress. Tag: trajectory (historical) · 9–16 mo doubling · ALGORITHMS · metric: `image_recognition_efficiency_doubling_time`

45. **LLM training efficiency "doubled approximately every 8 months"**, 95% CI **"5 months to 14 months"** (Epoch, 2012–2023) — same section. Tag: trajectory (historical) · 8mo (5–14mo CI) · ALGORITHMS · metric: `llm_training_efficiency_doubling_time`

46. **LLM runtime "cost efficiency... has doubled around every 3.6 months since November 2021"** — same section. Condition: includes hardware-cost and margin effects, not software alone. Tag: trajectory · 3.6-month doubling · VALUE · metric: `llm_inference_cost_efficiency_doubling_time`

47. **r estimates by domain (Epoch): computer vision median "1.4"** (90% CI **"0.8 to 2.4"**); computer chess **"0.8"**; reinforcement learning **"1.6"**; SAT solvers **"3.5"**; linear programming **"1.1"** — §In the real world, are returns to software R&amp;D greater or less than one? Tag: trajectory (parameter) · r=0.8–3.5 by domain · ALGORITHMS · metric: `domain_specific_r_returns`

48. **Synthesized software-R&amp;D r "best guess ~1–4"**, adjusted down to **"~0.5–2"** for hardware constraints — same section. Tag: trajectory (parameter) · r=0.5–4 · ALGORITHMS · metric: `synthesized_r_software_rd`

49. **Fizzle scenario (r=0.7): "~30x improvement in AI software capacity in a bit under a year"**, starting from a 1-month doubling time — §Being more mathematically concrete. Condition: "r=0.7," post-ASARA, starting doubling time 1 month. Tag: milestone · 30x/~1yr · ALGORITHMS · metric: `fizzle_scenario_software_capacity_growth`

50. **SIE scenario (r=3): doublings compress to "19 days, 12 days, 7.6 days, 4.8 days"** — same section. Condition: "r=3," post-ASARA. Tag: trajectory · doubling time falling to &lt;5 days · ALGORITHMS · metric: `sie_scenario_doubling_time_compression`

51. **Proposed policy threshold: "5x the recent pace of software progress"** as a trigger companies should commit not to exceed without precautions — §What can we do if an SIE is possible? Tag: milestone (policy trigger, not a prediction) · 5x recent pace · RESPONSE · metric: `software_acceleration_precaution_threshold`

### [E] The Industrial Explosion

52. **"AI chips double in FLOP/$ every ~2 years"** (current) — §The industrial explosion will start after the intelligence explosion. Tag: trajectory · 2-yr doubling · COMPUTE · metric: `chip_flop_per_dollar_doubling_time`

53. **"AI algorithms double in efficiency every year or less"** (current) — same section. Tag: trajectory · ≤1-yr doubling · ALGORITHMS · metric: `algorithm_efficiency_doubling_time_current`

54. **"robot technology doubles in efficiency more slowly than this, perhaps every 1-4 years"** — same section. Tag: trajectory · 1–4-yr doubling · PHYSICAL · metric: `robot_tech_efficiency_doubling_time`

55. **"The most recent doubling in the number of robots in the world took 6 years"** — §heading of same name. Tag: trajectory (historical) · 6-yr doubling · PHYSICAL · metric: `robot_count_doubling_time_historical`

56. **Initial post-AGI robot doubling time: "on the order of a year or less"**, revised to **"1–2 years"** accounting for factory-construction costs — §How fast could robot doubling times be initially? Condition: "with current physical technology" + abundant AI automation. Tag: milestone · 1–2 yr · PHYSICAL · metric: `initial_robot_doubling_time_post_agi`

57. **Earth's "robot carrying capacity... 1e14 humanoid robots"** vs. **"fewer than 100,000 humanoid robots have been produced"** to date (9-OOM gap) — §How quick might robot doublings become by the time we reach the earth's carrying capacity? Tag: milestone (ceiling) · 1e14 robots, 9 OOM scale-up needed · PHYSICAL · metric: `robot_carrying_capacity_earth`

58. **Doubling time at carrying capacity: "Conservative: few days," "Median: few hours," "Aggressive: less than a second"** — same section. Tag: milestone (scenario range) · seconds–days · PHYSICAL · metric: `robot_doubling_time_at_capacity`

59. **"overall increase in physical output here might be about 10X"** from AI-directed human labour productivity gains — §AI-directed human labour. Tag: trajectory · ~10x · VALUE · metric: `ai_directed_labor_productivity_multiple`

---

## Authors' own watch-list (leading indicators they say to track)

Explicitly named across the papers:

1. **METR task-horizon trend** — the length of tasks (measured in human-time-to-complete) that AI systems can autonomously execute at a fixed success rate, tracked because it has been "doubling roughly every seven months" [A]. This is their single most-cited empirical trend line.
2. **Benchmark-vs-expert gap closing speed** — GPQA (PhD-level science Q&amp;A), SWE-bench (real-world software issue resolution), RE-Bench (time-capped ML optimization vs. domain experts) — watched for how fast AI closes the gap to top human performance [A].
3. **Effective training compute growth rate** — decomposed into (a) raw training compute, (b) pretraining algorithmic efficiency, (c) post-training enhancement efficiency, (d) inference compute available — each tracked as a separate multiplier because they compound [A].
4. **Inference cost per token** — as a proxy for both algorithmic efficiency and the economic feasibility of running larger "AI populations" [A].
5. **Ongoing measurement of software progress, disclosed to trusted third parties** — explicitly proposed as an early-warning mechanism for a software intelligence explosion [D].
6. **AI R&amp;D task-automation evaluations** — testing whether AI systems can autonomously complete a defined battery of AI-R&amp;D tasks (per METR's AI R&amp;D suite) as a direct readout of proximity to ASARA [D].
7. **Real-world AI-driven productivity gains inside AI labs** — measuring how much existing AI coding/research tools boost employee productivity and extrapolating the trend forward [D].
8. **A pre-committed acceleration threshold** (e.g., "5x the recent pace of software progress") that labs commit not to cross without added safety precautions — a governance-oriented indicator, not just observational [D].
9. **Feedback-loop cycle times** — how long it takes to (a) train a new SOTA model (~3 months currently), (b) design a new chip generation, (c) build a new fab (years) — tracked because whichever loop has the shortest cycle time dominates near-term dynamics, and shortening cycle times signal an approaching explosion [C].
10. **Empirical "r" (returns to R&amp;D) estimates by domain** — how many doublings of output a doubling of R&amp;D input buys, tracked per domain (software, chips, robots) as the core parameter determining whether any given feedback loop is self-reinforcing (r&gt;1) or fizzles (r&lt;1) [B, C, D].
11. **Remaining OOMs of headroom before hitting physical/algorithmic ceilings** — efficiency headroom versus the human-brain-efficiency benchmark and versus Landauer's-limit-style hard physical bounds, tracked as a "runway" indicator for how long acceleration can continue [B, C].
12. **Chip FLOP/$ doubling time (~2 yr) and robot-count doubling time (currently ~6 yr)** — tracked as the physical-world analogs to software doubling time, indicating how close the "industrial explosion" is to decoupling from human-paced manufacturing [E].

---

A few notes for whatever tracker/schema this feeds: nearly all headline probabilities (claims 27–30, 38–40) come from Monte Carlo models built on stacked, wide-uncertainty-range parameters (r_cog, p, initial speedup) — the authors flag these explicitly as "back-of-the-envelope" and "necessarily speculative," so if your tracker records confidence intervals, preserve the log-uniform ranges (e.g., r_cog 0.4–3.6) rather than just the point estimate. Also worth flagging: claims 14–17 and 21–22 in [A] are _scenario outputs_ (moderate/rapid, conservative/aggressive) rather than single forecasts — record the scenario label as part of the claim, not just the number.
