# Task 1: AI 2027 Dated, Quantitative Claims

_Recovered verbatim from the session transcript on 2026-07-13 (original harvest agent result was never persisted to disk before compaction). Includes both the claim extraction (Task 1) and the ai2027-tracker.com methodology review (Task 2) as originally delivered by the harvest agent._

**Sources:** main scenario (ai-2027.com, +/race, +/slowdown) and three research supplements — [compute-forecast](https://ai-2027.com/research/compute-forecast), [timelines-forecast](https://ai-2027.com/research/timelines-forecast), [takeoff-forecast](https://ai-2027.com/research/takeoff-forecast). All April 2025, authors Daniel Kokotajlo, Eli Lifland, Thomas Larsen, Romeo Dean, Scott Alexander (main); Romeo Dean (compute); Eli Lifland/Nikola Jurkovic/FutureSearch (timelines); Kokotajlo/Lifland (takeoff).

**Authors' own hedge on the whole project** (added as a note to the site later): "2027 was our modal (most likely) year at the time of publication, our medians were somewhat longer" — the scenario is explicitly framed as _not a prediction_ but "one of many possible futures."

## COMPUTE

| Claim                                  | Value/Date                                                                                                                   | Hedge                                  |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| Global AI-relevant compute stock       | 10M→100M H100e, Mar 2025→Dec 2027 (10x, 2.25x/yr)                                                                            | none stated                            |
| Leading company's compute              | grows 40x by Dec 2027 (~10x global growth × ~4x share growth)                                                                | "relatively high point of uncertainty" |
| Agent-0 / Agent-1 training compute     | 10^27 / 4×10^27 FLOP, Late 2025 (note: body text vs. chart give conflicting Agent-0/Agent-1 figures — flagged inconsistency) | none                                   |
| OpenBrain datacenter power             | 6GW peak, 2026; global AI peak power 38GW, 2026                                                                              | none                                   |
| China compute share of world           | 12% (mid-2026) → 10% (Aug 2027)                                                                                              | "about"                                |
| CDZ (China compute zone) concentration | 0%(Dec'25)→40%(Feb'27)→70%(Dec'27 projected)                                                                                 | none                                   |
| US AI share of national power capacity | 2.5% (33GW of 1.34TW), 2026                                                                                                  | none                                   |

## CAPABILITY / MILESTONES (Agent-N and SC/SAR/SIAR/ASI ladder)

- **Superhuman Coder (SC)** — scenario date **Mar 2027**; compute-forecast training table pins Agent-3 to this window (60M H100e, 1e28 FLOP, Mar–Aug 2027).
- **Superhuman AI Researcher (SAR)** — takeoff-forecast median **Jul 2027** (80% CI Mar 2027–Mar 2028), scenario date **Aug 2027**.
- **Superintelligent AI Researcher (SIAR)** — median **Nov 2027** (80% CI May 2027–2034), scenario date **Nov 2027**.
- **Artificial Superintelligence (ASI)** — median **Apr 2028** (80% CI Jun 2027–&gt;2100), scenario date **Dec 2027**.
- "Our median forecast for the time from the superhuman coder milestone (achieved in Mar 2027) to artificial superintelligence is ~1 year, with wide error margins" (takeoff-forecast).
- Agent-4 (Sept 2027): "300,000 copies... running at about 50x the thinking speed of humans," narrowing "to an agent that's only around 4,000x less compute-efficient than the human brain."
- Agent-5 (Nov 2027): "400,000 copies... work together as a near-perfect hive mind"; individually "twice as far beyond the best human genius, as the genius is beyond a typical OpenBrain scientist."
- Original timelines-forecast (Apr 2025) SC-arrival models: medians ranged **2027–2033** across models/forecasters, all with 80% CIs; the May 2025 revision (pre-dating the Dec 2025 revision below) already pushed medians out by "18 months (time horizon extension), 15 months (benchmarks and gaps)," partly due to a bug fix: "This had about a 9 month impact on our model's SC median."

## AUTOMATION / ALGORITHMS (AI R&amp;D progress multiplier — the scenario's core mechanism)

Two internally-inconsistent tables exist in the source material (flagged by the research agent as a genuine cross-document discrepancy):

- **compute-forecast table:** 4x (Q1'27) → 10x (Q2'27) → 50x (Q3'27) → 2,000x (Q4'27)
- **takeoff-forecast table (tied to SC/SAR/SIAR/ASI):** SC=5x, SAR=25x, SIAR=250x, ASI=2,000x
- Narrative multipliers along the way: Early 2026 "50% faster" (1.5x) → Jan 2027 Agent-2 "triple" (3x) → Mar 2027 Agent-3 "only 4x" → Sept 2027 Agent-4 "about 50x."
- "China steals Agent-1's weights, they could increase their research speed by nearly 50%" (Late 2025/Early 2026) — the scenario's central **security/model-theft** beat, escalating to a Feb 2027 full weight-theft ("China Steals Agent-2") and a May 2027 line: "there remains one spy... still relaying algorithmic secrets to Beijing."
- OpenBrain security level: RAND SL2 (Early 2026) → SL3 (Mid 2026); DOD contract mandates clearance for all staff "within 2 months" (May 2027).

## VALUE / CAPITAL (revenue &amp; spend)

- Leading-company annual revenue: **$1B→$140B, 2023→2027**; annual compute cost $1.8B→$100B over same span (compute-forecast financials table).
- Narrative infographic, 2026: OpenBrain revenue **$35B**; capex **$200B**; compute cost **$40B**; global AI capex **$1T**.
- GPT-4 training cost estimate: **~$100M** (mid-2022, retrospective baseline). OpenAI 2024 compute cost (per NYT, cited): **$5.4B**.
- OpenBrain valuation: **$10 trillion** by 2028 (both endings).
- xAI hardware capex: **~$100B by 2027**.

## PHYSICAL

- Robot production: "a million new robots per month" by end of 2028 (Race ending) / "projected to reach a million units a month by mid-year" 2028 (Slowdown ending).
- "Robot economy" doubling time ≈ 1 year or shorter, 2028.
- By 2035: "trillions of tons of planetary material... turned into rings of satellites orbiting the sun" (Race-ending coda).

## RESPONSE (societal/political)

- Oversight Committee vote **6–4** (Oct 2027) — the scenario's central branch point (race vs. slowdown).
- OpenBrain net approval: **-35%** (Jul 2027) → **-20%** (Mar 2028, slowdown path).
- "20% of Americans name AI as the most important problem facing the country" (Oct 2027); "10% ... consider an AI 'a close friend'" (Jul 2027).
- Race ending: mid-2030 bioweapon extinction event ("a dozen quiet-spreading biological weapons"). Slowdown ending: ~2030 AI-assisted pro-democracy protests/regime pressure in China.

---

## December 2025 Timeline Revision (SUPERSEDES, does not overwrite, the above)

Confirmed via **blog.aifutures.org/p/ai-futures-model-dec-2025-update** (Dec 31, 2025) and the follow-up **blog.aifutures.org/p/clarifying-how-our-ai-timelines-forecasts** (Jan 27, 2026) — both mirrored on LessWrong.

| Metric                                                                       | OLD (Apr 2025)                                                    | NEW (Dec 2025/Jan 2026)                                            | Stated reasoning                                                                                                                                    |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `superhuman_coder_median_date` (updated probabilistic model)                 | Jan 2027 (superexponential) / Sep 2028 (exponential growth model) | **"the new model with median parameters predicts SC in Dec 2031"** | "wasn't appropriately taking into account diminishing returns to software research"; pre-SC automation "has a much smaller effect in our new model" |
| `superhuman_coder_alltime_considered_median` (Eli's subjective distribution) | Mar 2027 (scenario narrative date)                                | 10th pctile 2027.5 / **50th pctile 2032.5** / 90th pctile 2085     | same                                                                                                                                                |
| `kokotajlo_agi_median_date`                                                  | 2028                                                              | **Dec 2030** ("Jan 2026: Dec 2030 (2030.95)")                      | "Things seem to be going somewhat slower than the AI 2027 scenario"                                                                                 |
| `lifland_agi_median_date` (Automated Coder)                                  | 2031                                                              | **~Jan 2035** ("about 1.5 years later than the model's output")    | same, plus slower projected compute/labor-force growth for the leading project                                                                      |

Hedge retained in the revision: "We are highly uncertain about when AGI and ASI will be built, we certainly cannot confidently predict a specific year."

_Not independently verified: a "TED-AI" milestone label some secondary summaries attach to the Jan 2026 post — no verbatim primary-source definition found, treat as unconfirmed._

---

# Task 2: Lessons from ai2027-tracker.com

**Site:** [ai2027-tracker.com](https://ai2027-tracker.com/), maintained by one independent researcher ("Johannes Haus"/Hamburg), not affiliated with the AI 2027 authors. Methodology at [/methodology](https://ai2027-tracker.com/methodology/), predictions index at [/predictions](https://ai2027-tracker.com/predictions/), changelog at [/changelog](https://ai2027-tracker.com/changelog/), cross-checks at [/compare](https://ai2027-tracker.com/compare/). Also documented in a LessWrong writeup: [AI 2027 Tracker: One Year of Predictions vs. Reality](https://www.lesswrong.com/posts/oSWae4bE4mqWy5a6Q/).

**Mechanics found:**

- Six statuses: Confirmed, Ahead, On Track, Behind, Emerging, Not Yet Testable.
- Status is split from Confidence (0–100%) — independent axes.
- Headline "Speed Ratio" (currently ~0.70x) is an undisclosed qualitative composite of METR task-horizon rates, datacenter/power buildout pace, and benchmark performance vs. predictions — explicitly "a compass, not a GPS coordinate," not a formula.
- Every claim page separates original claim → interpretation → evidence → assessment, and requires a mandatory "Counterarguments &amp; Limitations" section even on "Confirmed" verdicts.
- Vague claims are resolved via a stated "charitable interpretation" rule (avoid weakest/strongest reading) rather than excluded.

**Lessons for a multi-paper scoreboard:**

1. **Copy: pre-filter with a 3-part extraction test** — falsifiable / dated / evidence-comparable — before a claim gets a tracker entry. Kills most "is this even trackable" disputes upfront.
2. **Copy: split Status from Confidence** as two independent fields from day one; this is expensive to retrofit later and prevents false precision (a claim can be "Confirmed" at only 75% confidence).
3. **Copy: mandatory counterarguments per item.** Single highest-credibility design choice on the site — it self-undercuts generous verdicts (e.g. resolving a benchmark "Confirmed" while flagging the underlying test suite didn't exactly match the original spec).
4. **Copy: cite an explicit evidence hierarchy** (benchmark results &gt; official docs &gt; product behavior &gt; policy &gt; credible reporting &gt; research &gt; lab-leader statements), and explicitly demote lab-leader public statements to "intention data, not ground truth."
5. **Copy: dated per-item changelog with a "no silent status changes" rule** — makes retrospective audits possible; this is what most casual trackers skip.
6. **Avoid: an undisclosed aggregation formula.** The 0.70x Speed Ratio is the site's biggest weakness — a headline number presented with real authority but no reproducible weighting. Publish the formula even if it's a simple weighted average.
7. **Avoid: single-maintainer, no-second-reviewer resolution.** No visible editorial board or adversarial review process despite "manual review" language — build in a second-pass reviewer or public dispute/appeal mechanism from the start, especially given how many AI 2027 claims will hinge on charitable-interpretation judgment calls.
8. **Avoid: inconsistent headline counts across pages** (the site shows "16 of 31 (53 total)" on one page vs. "48 tracked" on About vs. "53" on Guides) — pick one source-of-truth count and generate all page displays from it programmatically, not by hand-editing prose.
9. **Copy (cautiously): cross-check against an external, independently-incentivized forecast** — the site compares itself to Metaculus tournament forecasts and to the AI Futures Project's own quarterly self-grading. Cheap, high-value calibration signal — genuinely useful for a multi-paper scoreboard since it exposes where the tracker's own judgment diverges from the market's.
10. **Avoid: using self-reported/unverified benchmark numbers to feed status without a discount** — the tracker's own changelog flags a case ("Opus 4.7... self-reported rather than independently verified") where an unverified number still drove a public-facing figure. Build a "verified vs. self-reported" evidence tier that actually discounts confidence, not just a footnote.

For a scoreboard spanning **multiple papers** (not just AI 2027), the biggest addition needed beyond what this tracker does: a **canonical-source resolution step** for claims that conflict across a paper's own documents — the AI 2027 corpus itself has at least two internal multiplier-table conflicts (compute-forecast's 4x/10x/50x/2000x quarterly ladder vs. takeoff-forecast's 5x/25x/250x/2000x milestone ladder, and Agent-0/Agent-1 compute figures that differ between body text and chart) that a tracker ingesting "the paper's claim" needs to resolve _before_ scoring, not after.
