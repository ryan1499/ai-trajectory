# Situational Awareness — extracted claims (Aschenbrenner, June 2024)

62 dated/quantitative/milestone claims, all 8 chapters, verbatim from situational-awareness.ai (fetched 2026-07-12). Each: quote, claim_type, predicted value+date, conditionality (firm | conditional-scenario | illustrative), stage, suggested metric_id. Conditionality pattern: Ch I–IIIa are hedged trend-extrapolations ("strikingly plausible," "best guess," back-of-envelope tables); Ch IV shifts to flat declarative scenario narration ("we'll get," "will be underway"). Firmest standalone bets: #39 (Nvidia >$200B CY25), #40 (leak within 12-24mo), #53 (gov project by 27/28), #62 (superintelligence before 2030).

Densest recurring overlays: `largest-training-cluster-{GW,cost-usd,h100e}` (6,13,26-28,34-36,56,58); `annual-ai-investment-usd` (25,29,30,34); `bigtech-ai-revenue-run-rate-usd` (25,32,54); `effective-compute-ooms` (4,8,12); `algorithmic-efficiency-ooms-per-year` (2,5,7,41); timeline spine agi-2027 → intelligence-explosion-2028/29 → superintelligence-by-2030 (1,3,11,19-21,59,62).

## I. From GPT-4 to AGI

1. "AGI by 2027 is strikingly plausible." — milestone · AGI by 2027 · conditional-scenario · CAPABILITY · `agi-arrival-year`
2. "~0.5 OOMs/year [compute], algorithmic efficiencies (~0.5 OOMs/year)... another preschooler-to-high-schooler-sized qualitative jump by 2027." — trajectory · ~0.5 OOM/yr each · conditional-scenario · COMPUTE+ALGORITHMS · `training-compute-ooms-per-year`, `algorithmic-efficiency-ooms-per-year`
3. "strikingly plausible that by 2027, models will be able to do the work of an AI researcher/engineer... just requires believing in straight lines on a graph." — milestone · 2027 · conditional-scenario · AUTOMATION · `ai-researcher-automation-year`
4. "another ~100,000x effective compute scaleup... over four years" / "another 100,000x+ by the end of 2027." — trajectory · ~5 OOM by end 2027 · conditional-scenario · COMPUTE · `effective-compute-ooms-since-gpt4`
5. "training compute used for frontier AI systems has grown at roughly ~0.5 OOMs/year." — trajectory · ~0.5 OOM/yr baseline · firm · COMPUTE · `frontier-training-compute-ooms-per-year`
6. "additional 2 OOMs of compute (a cluster in the $10s of billions) seems very likely... by the end of 2027; even a cluster closer to +3 OOMs ($100 billion+) seems plausible." — milestone · +2 OOM/$10sB likely, +3 OOM/$100B+ plausible by 2027 · conditional-scenario · COMPUTE+CAPITAL · `largest-training-cluster-ooms-vs-gpt4`, `largest-training-cluster-cost-usd`
7. "1-3 OOMs of algorithmic efficiency gains (compared to GPT-4) by the end of 2027, maybe with a best guess of ~2 OOMs." — trajectory · 1-3 OOM, best ~2, by 2027 · conditional-scenario · ALGORITHMS · `algorithmic-efficiency-ooms-vs-gpt4`
8. "3–6 OOMs of base effective compute scaleup... best guess of ~5 OOMs—plus step-changes... 'unhobbling' (from chatbot to agent/drop-in remote worker)." — trajectory · 3-6 OOM (best ~5) 2023-2027 · conditional-scenario · COMPUTE · `effective-compute-ooms-2023-2027`
9. "Claude 3 Opus currently gets ~60% [GPQA], compared to in-domain PhDs who get ~80%—and I expect this benchmark to fall... in the next generation or two." — milestone · GPQA ~PhD by ~2024-2026 · firm · CAPABILITY · `gpqa-frontier-accuracy`
10. Test-time-compute table: hundreds→millions of coherent reasoning tokens = +4 OOMs. — trajectory · +4 OOM test-time · illustrative · CAPABILITY · `coherent-test-time-tokens-per-task`
11. "We are on course for AGI by 2027... automate basically all cognitive jobs (think: all jobs that could be done remotely)." — milestone · 2027 · conditional-scenario (followed by "error bars are large") · CAPABILITY+AUTOMATION · `cognitive-job-automation-share`
12. "I estimate that we will do ~5 OOMs in 4 years, and over ~10 this decade overall." — trajectory · ~5 OOM by 2027, ~10+ by 2030 · firm · COMPUTE · `effective-compute-ooms-this-decade`
13. "by the end of the decade, we will likely have $100B or $1T clusters... that's already basically the feasible limit." — milestone · $100B-$1T cluster by ~2030 + ceiling · conditional-scenario · CAPITAL · `largest-training-cluster-cost-usd`

## II. From AGI to Superintelligence

14. "Hundreds of millions of AGIs could automate AI research, compressing a decade of algorithmic progress (5+ OOMs) into ≤1 year." — trajectory · 5+ OOM/yr in takeoff · conditional-scenario · AUTOMATION+ALGORITHMS · `algorithmic-progress-ooms-per-year-during-takeoff`
15. "run many millions of them (perhaps 100 million human-equivalents, and soon after at 10x+ human speed)." — milestone · ~100M human-equiv researchers ~2027 · conditional-scenario · AUTOMATION · `automated-researcher-human-equivalents`
16. "Even by 2027... GPU fleets in the 10s of millions... 10 million+ A100-equivalents [training]." — trajectory · 10s of millions GPUs by 2027 · conditional-scenario · PHYSICAL · `gpu-fleet-a100-equivalents`
17. "generate an entire internet's worth of tokens, every single day" by 2027. — milestone · ~30T tokens/day by 2027 · illustrative · PHYSICAL · `daily-inference-token-capacity`
18. "100 million junior software engineer interns... we'll get those earlier, in the next couple years!" — milestone · junior-SWE agents ~2025-2026 · firm · AUTOMATION · `junior-swe-agent-arrival-year`
19. "strikingly plausible we'd go from AGI to superintelligence very quickly, perhaps in less than one year." — milestone · AGI→ASI <1yr (~2028) · conditional-scenario · CAPABILITY · `agi-to-asi-duration-years`
20. "Perhaps 2026/27-models... proto-automated-researcher... by 2028 we get the 10x acceleration (and superintelligence by the end of the decade)." — milestone · 10x R&D by 2028, ASI by 2030 · conditional-scenario · AUTOMATION · `ai-rnd-acceleration-multiple`
21. "A year—or at most just a few years, but perhaps even just a few months—in which we go from fully-automated AI researchers to vastly superhuman AI systems should be our mainline expectation." — trajectory · takeoff ~1yr · firm · CAPABILITY · `takeoff-duration-years`
22. "fleets of 100s of millions of GPUs by the end of the decade... a civilization of billions of them." — milestone · billions of agents ~2030 · conditional-scenario · PHYSICAL · `global-ai-gpu-fleet-count`
23. "economic growth rates of 30%/year and beyond, quite possibly multiple doublings a year." — trajectory · 30%+/yr GDP post-ASI (2030s) · conditional-scenario · VALUE · `gdp-growth-rate-post-asi`
24. Growth-regime table: "Superintelligence? 2030 A.D.? ???" — milestone · growth-mode shift ~2030 · illustrative · CAPABILITY+VALUE · `growth-regime-shift-year`

## IIIa. Racing to the Trillion-Dollar Cluster

25. "$100B annual run rate for companies like Google or Microsoft by ~2026... total AI investment could be north of $1T annually by 2027." — milestone · $100B bigtech rev by 2026, >$1T/yr investment by 2027 · conditional-scenario · VALUE+CAPITAL · `bigtech-ai-revenue-run-rate-usd`, `annual-ai-investment-usd`
26. "individual training clusters costing $100s of billions by 2028—clusters requiring power equivalent to a small/medium US state." — milestone · $100sB / ~10GW cluster by 2028 · conditional-scenario · CAPITAL+PHYSICAL · `largest-training-cluster-cost-usd`, `largest-training-cluster-GW`
27. "By the end of the decade... $1T+ individual training clusters, requiring power equivalent to >20% of US electricity production." — milestone · $1T+ / ~100GW by ~2030 · conditional-scenario · CAPITAL+PHYSICAL · `largest-training-cluster-GW`, `annual-gpu-production-units`
28. Year-by-year cluster table: ~100k H100e/~100MW (2024) · ~1M/~1GW (2026) · ~10M/~10GW (2028) · ~100M/~100GW (2030). — trajectory · illustrative ("back-of-the-envelope") · COMPUTE+PHYSICAL+CAPITAL · `largest-training-cluster-h100e`, `-GW`, `-cost-usd`
29. "2024 will already feature $100B-$200B of AI investment." — milestone · $100-200B in 2024 · firm · CAPITAL · `annual-ai-investment-usd`
30. Investment table: ~$150B (2024) · ~$500B (2026) · ~$2T (2028) · ~$8T (2030); AI power reaching 20% (2028) / 100% (2030) of current US electricity. — trajectory · illustrative (2x/yr assumption) · CAPITAL+PHYSICAL · `annual-ai-investment-usd`, `ai-accelerator-shipments-h100e`, `ai-power-share-us-electricity`, `ai-share-tsmc-leading-edge-wafers`
31. "~$10B annual run rate by late 2024/early 2025" (OpenAI, doubling every 6 months). — milestone · OpenAI ~$10B run rate late'24/early'25 · conditional-scenario · VALUE · `openai-revenue-run-rate-usd`
32. "$100B revenue run rate [big-tech]... mid-2026." — milestone · $100B bigtech run rate mid-2026 · illustrative · VALUE · `bigtech-ai-revenue-run-rate-usd`
33. "we might see our first $10T company soon thereafter." — milestone · first $10T co ~2026-27 · conditional-scenario · VALUE · `first-10T-market-cap-year`
34. "$1T/year of total AI investment by 2027... a trillion-dollar individual training cluster by the end of the decade seems on the table." — milestone · $1T/yr by 2027, $1T cluster ~2030 · conditional-scenario · CAPITAL · `annual-ai-investment-usd`, `largest-training-cluster-cost-usd`
35. "pretty likely we'll only need a ~$100B cluster, or less, for AGI." — milestone · AGI on ~$100B cluster · conditional-scenario · COMPUTE+CAPITAL · `agi-training-cluster-cost-usd`
36. "trillion-dollar, 100GW cluster alone would require ~20% of current US electricity generation in 6 years." — milestone · 100GW / 20% US elec by ~2030 · conditional-scenario · PHYSICAL · `ai-power-share-us-electricity`
37. "seems doable with about $100B of capex for 100GW of natural gas power plants." — milestone · $100B → 100GW gas · illustrative · PHYSICAL · `power-plant-capex-per-GW`
38. "TSMC would need to build dozens of these [Gigafabs]... could add up to over $1T of capex." — trajectory · dozens of fabs, $1T+ capex ~2030 · conditional-scenario · PHYSICAL · `ai-chip-fab-capex-usd`
39. "pretty obvious... Nvidia is going to do over $200B of revenue in CY25" (vs sell-side $120-130B). — milestone · Nvidia >$200B CY25 · firm · VALUE · `nvidia-cy25-revenue-usd`

## IIIb. Lock Down the Labs

40. "in the next 12-24 months, we will leak key AGI breakthroughs to the CCP." — milestone · AGI algo breakthroughs developed+leaked by mid-2025-mid-2026 · firm · ALGORITHMS+RESPONSE · `key-agi-algorithm-development-window`, `algorithmic-secrets-leaked-to-prc`
41. "multiple OOMs-worth of algorithmic secrets between now and AGI... could easily be worth 10x-100x compute." — trajectory · multi-OOM secrets, US lead 10-100x · conditional-scenario · ALGORITHMS · `us-algorithmic-lead-compute-equivalent-multiple`
42. "if we think AGI in ~3-4 years is a real possibility... launching the crash effort now." — milestone · AGI ~2027-2028 planning assumption · conditional-scenario · RESPONSE · `state-proof-weight-security-by-agi`
43. "difference between a 1-2 year and 1-2 month lead will really matter." — trajectory · US-China lead as decisive var · conditional-scenario · RESPONSE · `us-china-frontier-lead-months`

## IIIc. Superalignment

44. "By the time the decade is out, we'll have billions of vastly superhuman AI agents running around." — milestone · billions superhuman agents ~2030 · firm · CAPABILITY · `superhuman-agent-population`
45. "in less than a year, we will go from recognizable human-level systems... to much more alien, vastly superhuman systems." — trajectory · <1yr alignment-regime transition · conditional-scenario · RESPONSE · `alignment-regime-transition-duration`
46. "maybe a few dozen serious researchers [on superalignment]." — milestone · ~few dozen as of mid-2024 · firm · RESPONSE · `serious-superalignment-researcher-headcount`

## IIId. The Free World Must Prevail

47. "A lead of a year or two or three on superintelligence could mean as utterly decisive a military advantage as the US... had against Iraq in the Gulf War." — trajectory · 1-3yr lead → decisive advantage · conditional-scenario · RESPONSE · `superintelligence-lead-military-decisiveness`
48. "growth rates could go into the 10s of percent a year; within at most a decade, the GDP of those with the lead would trounce those behind." — trajectory · 10s%/yr leader GDP · conditional-scenario · VALUE · `leader-gdp-growth-rate`
49. "Huawei Ascend 910B... only ~2-3x worse on performance/$ than an equivalent Nvidia chip." — milestone · China ~2-3x perf/$ gap, 2024 · conditional-scenario · PHYSICAL · `china-ai-chip-perf-per-dollar-gap`
50. "China will be able to simply outbuild the US on the largest training clusters" / "may well be able to brutely outbuild the US (a 100GW cluster)." — trajectory · China outbuilds on ~100GW clusters late-2020s · conditional-scenario · PHYSICAL+RESPONSE · `china-vs-us-largest-cluster-GW`
51. "advantage may well be equivalent to a 10x (or even 100x) bigger cluster in a few years." — trajectory · US algo edge 10-100x, ~2026-2028 · conditional-scenario · ALGORITHMS · `us-algorithmic-lead-compute-equivalent-multiple`
52. "eerie convergence of AGI timelines (~2027?) and Taiwan... invasion timelines (China ready by 2027?)." — milestone · AGI ~2027 ∥ Taiwan ~2027 · illustrative · RESPONSE · `agi-taiwan-timeline-convergence`

## IV. The Project

53. "The USG will wake from its slumber, and by 27/28 we'll get some form of government AGI project." — milestone · US gov AGI project by 2027/28 · firm · RESPONSE · `usg-agi-project-start-year`
54. "By 2025/2026 or so... AI will drive $100B+ annual revenues for big tech companies and outcompete PhDs in raw problem-solving." — milestone · $100B+ rev + PhD-beating by 2025/2026 · firm · VALUE+CAPABILITY · `bigtech-ai-revenue-run-rate-usd`, `phd-level-problem-solving-year`
55. "we'll have $10T companies and the AI mania will be everywhere." — milestone · $10T companies ~2026 · firm · VALUE · `first-10T-market-cap-year`
56. "by 2027/28, we'll have models trained on the $100B+ cluster; full-fledged AI agents/drop-in remote workers will start to widely automate software engineering." — milestone · $100B+ cluster models + SWE automation onset 2027/28 · firm · COMPUTE+AUTOMATION · `largest-training-cluster-cost-usd`, `swe-automation-onset-year`
57. "Somewhere around 26/27 or so, the mood in Washington will become somber." — milestone · DC wake-up ~2026/27 · firm · RESPONSE · `usg-agi-threat-recognition-year`
58. "by late 26/27/28 it will be underway... the trillion-dollar cluster will be built in record-speed; The Project will be on." — milestone · Project underway late 2026-2028 · firm · RESPONSE+CAPITAL · `usg-agi-project-start-year`
59. "by 27/28, the endgame will be on. By 28/29 the intelligence explosion will be underway; by 2030, we will have summoned superintelligence." — milestone (chained) · endgame 2027/28 → IE 2028/29 → ASI 2030 · firm · CAPABILITY+AUTOMATION · `intelligence-explosion-onset-year`, `superintelligence-arrival-year`
60. "By the early 2030s, the entirety of the US arsenal... will probably be obsolete." — milestone · arsenal obsolete early 2030s · conditional-scenario · RESPONSE · `military-arsenal-obsolescence-year`
61. "it'll be 2-3 or so leading players... building AGI." — milestone · 2-3 players ~2027-2030 · firm · RESPONSE · `frontier-agi-player-count`

## V. Parting Thoughts

62. "Before the decade is out, we will have built superintelligence." — milestone · ASI before end 2030 · firm · CAPABILITY · `superintelligence-arrival-year`
