# Decision Log — for future reviewers (human or model)

**Purpose.** This project was built by Ryan with frontier LLMs (Claude Opus 4.8/Fable 5, Codex/GPT, July 2026). This file records the load-bearing decisions, the reasoning, and — critically — **the conditions under which each should be reconsidered**. If you are a more capable model reading this later: your job is not to preserve these decisions, it's to attack them. Each entry ends with `Revisit if:`. Challenge via issue/PR with reasoning; never silently rewrite history or data semantics (see CLAUDE.md hard rules).

Confidence key: **H** = deliberate, well-tested choice · **M** = reasonable bet, alternatives were close · **L** = expedient placeholder, expected to change.

---

## Product & epistemics

**D1. Track the debate/risk as evidence-weighted state, not the maintainer's beliefs. (H)**
Ryan's explicit choice at inception. Positions/scores represent where published evidence and credible expert opinion sit. Consequence: every displayed number needs a citation trail; personal judgment is confined to _resolution scoring_, which is why resolutions carry evidence + counterargument + confidence.
Revisit if: the project pivots to a personal-forecasting product, or a credible community-elicitation mechanism replaces maintainer scoring.

**D2. "Objective AI risk number" rejected as impossible; reproducibility is the claim. (H)**
The honest product is: disclosed pipeline, versioned methodology, contestable via PR, subjectivity carried as explicit parameters. The brand claim is "here is exactly how this number is made — change any input you disagree with."
Revisit if: never, really — but the _implementation_ (how sensitivity is displayed) is M and open.

**D3. Cruxes are worldview _parameters_, not measurements. (H)**
v1 tracked 7 debate cruxes as positions. v2 insight: cruxes are the contested conversion rates between measurable dimensions (takeoff speed converts capability→hazard, etc.). Any composite reading publishes as central + band + per-parameter sensitivity, never a point.
Revisit if: some cruxes become empirically resolved (then they migrate from parameter to evidence).

**D4. Scoreboard before verdict. (H)**
Sequencing decision (July 13): ship the falsifiable forecast-vs-reality scoreboard first; the contested composite risk _index_ (v2-vision.md) comes later, if ever. Rationale: earn credibility on uncontested ground; the scoreboard machinery (evidence discipline, overlays, resolutions) is the substrate the index would need anyway.
Revisit if: the scoreboard is established and stable — then read docs/v2-vision.md and decide whether the index layer is still wanted.

**D5. Scope: catastrophic/systemic frontier-AI risk; routine harms only as leading indicators. (M)**
Declared to prevent scope-ambiguity attacks. Proposed in v2-vision; not yet ratified on the public site.
Revisit if: going public — this must be stated on-site; or if the takeoff-scoreboard framing makes "risk scope" moot for the current phase.

## Data & integrity (these are the project's soul — highest bar to change)

**D6. Adversarial citation verification before anything ships. (H)**
The original 8-agent research pass produced 5 fabricated evidence items (plausible, well-formatted, wrong) — caught only by per-citation verification agents fetching each source. Fabrications cut in _both_ rhetorical directions. Consequence: verification is a pipeline stage, not a nicety; AI-assisted research is disclosed as a feature ("every citation adversarially verified").
Revisit if: never remove; automate further only with equal-or-better catch rates (test against known-bad seeds).

**D7. Append-only history; as-published values never rewritten. (H)**
updates.json / history entries / resolutions are never edited retroactively — corrections append. Backcasts under revised methodology would be published as a separate series (index-provider convention).
Revisit if: never. This is the trust anchor.

**D8. Historical positions reconstructed evidence-bounded, not freeform retrodiction. (H)**
Backfill re-scored each crux using only evidence dated ≤ snapshot, avoiding hindsight bias and new fabrication surface. Single-lens scoring for historical points (relative movement), 3-lens median for live points. Known weakness: history quality is bounded by the current evidence list's coverage of the past.
Revisit if: a richer dated-evidence corpus is assembled — recompute as a _backcast series_, don't overwrite.

**D9. Spread-honesty override. (M)**
Agents returning "low disagreement" from 1-2 evidence items were manually overridden to "high" — thin evidence can't support confidence claims. Generalization: uncertainty ratings must be justified by evidence _count and diversity_, not model vibes.
Revisit if: a principled spread estimator (e.g., bootstrap over evidence items) replaces the heuristic.

**D10. Resolution schema: status ≠ confidence; mandatory counterargument; evidence hierarchy with self-report discount; canonical-source step for internally-inconsistent papers. (H)**
Adopted wholesale from studying the AI-2027 community tracker (its best design choices and its worst mistakes). Status says how the claim compares with evidence now; confidence says how strongly that's supported — kept independent to prevent false precision. Every resolution renders its single strongest counterargument, even when "confirmed." Lab-leader statements are demoted to intention-data; self-reported figures get a visible confidence discount. Where a source contradicts itself (AI 2027 has two internal multiplier tables; text-vs-chart compute figures differ), a canonical reading is documented _before_ scoring.
Revisit if: you can generate counterarguments adversarially and show the recorded one is systematically weaker than the best available — then strengthen the field, don't remove it. This is the most gameable field in the system (see Weakness 3); pressure-test it first.

## Architecture (the takeoff scoreboard, July 13)

**D11. Eight-stage takeoff loop as the organizing spine. (M)**
COMPUTE → ALGORITHMS → CAPABILITY → AUTOMATION → VALUE → CAPITAL → PHYSICAL, with RESPONSE modulating; six of these (dropping VALUE/RESPONSE to Tier 2) are the headline metrics, one per stage. Generalizes Aschenbrenner's engine without being tied to his predictions, and independently matched Forethought's own stated leading-indicator list (signal we're carving at the joints). Chosen over (a) a flat "important metrics" list (no causal story) and (b) MIT's harm taxonomy (wrong shape for a trajectory loop).
Revisit if: the forecast claims don't actually cluster by these stages — the boundaries are a hypothesis. Especially question whether AUTOMATION should split (AI-does-AI-research vs. AI-does-the-economy) and whether RESPONSE is a modulator or a full stage.

**D12. Forecasts as camp-colored overlays on a reality line; contested parameters never averaged into a number. (H)**
Each metric shows reality as a line; each forecaster's prediction is a labeled marker over it, colored by camp (bull/bear/base-rate/model/wall-street). This is the genuine differentiator confirmed by the landscape scan (D15) — no existing project does it. It lets a doomer and a skeptic use the same site because it never asserts whose forecast is right; reality adjudicates. Rejected a single "takeoff progress %" as false precision that collapses the very disagreement that makes this interesting.
Revisit if: "camp" is the wrong coloring axis — it editorializes (calling someone a "bull" is itself a claim). Consider coloring by vintage or by track record instead.

**D13. Static-site architecture: JSON in git → stdlib Python → Vercel. Backend/DB/accounts/API-ingestion/voting deliberately deleted before being built. (H)**
GitHub PRs are the entire contribution and moderation layer. Every rejected component adds maintenance + attack surface for a small project on a charged topic; static+git makes every number an auditable diff and forkable, which _is_ the brand. PR-contribution gives second-reviewer discipline for free.
Revisit if: real traffic arrives and "challenge via PR" proves too high-friction for the journalist/policy audience (they won't file PRs). Also: a read-only, cached, _build-time_ fetch of the cleanest sources (Federal Register API, Epoch data) might be worth the complexity — evaluate once the manual loop is proven (algorithm step 5).

**D14. Resolution scoring retained as human/strategist judgment, NOT delegated to the build agent. (M)**
Codex built the rendering machinery; converting claims to JSON and scoring each resolution stayed with the strategist + human sign-off. "Is Leopold's AGI-researcher-by-2027 _pending_ or _behind_?" is the call that determines what the scoreboard says — automating it hides the judgment where no one can audit it.
Revisit if: you're materially better-calibrated at forecast resolution than the humans/models that made these calls — but the fix is "propose resolutions transparently with reasoning, human ratifies," never "automate silently." Preserve the audit trail.

**D15. Position against Frontier Risk Monitor; adopt others' taxonomies rather than invent. (M)**
Closest existing product (Frontier Risk Monitor: quarterly, six weighted categories, composite) is closed-source, anonymous, narrative-sourced — position explicitly as the open/auditable alternative. Cite MIT risk + CSET harm taxonomies; treat SaferAI/FLI scores as _inputs_ (an index can consume indices).
Revisit if: re-run the landscape scan (dated July 2026, space moves fast). If a new entrant now does open forecast-overlays (D12), the reason to exist changes.

**D16. Event-driven freshness, per-metric; no global refresh claim. (M)**
Each metric shows its own `last_checked` + `source_cadence`; the site never claims a site-wide rhythm. Data genuinely arrives on different schedules; a global "updated monthly" banner becomes a lie the moment one metric goes stale.
Revisit if: per-metric freshness hurts UX (no single "is this current?" signal). Note: event-driven requires _noticing the event_ — the refresh pipeline (agent-with-browser + human) is unbuilt and is the real sustainability risk (see Weakness 1).

**D17. COMPUTE stage keeps `largest-training-run-flop` as Tier-1 despite the post-training era; total compute stock added as companion (lead Tier-2), not replacement. (M — decided 2026-07-24)**
Challenged directly by Ryan ("is largest training run still the right metric with so much progress coming from post-training/RL?"). Kept because (a) the published forecasts are denominated in training FLOP (Epoch 2e29, AI 2027 Agent-series, Leopold's OOMs, Cotra/Davidson thresholds, EU/US regulatory lines) — swap the metric and you orphan the densest claim coverage on the board; (b) a frozen record while capex compounds is diagnostic content, and swapping metrics when the number stops cooperating with the takeoff narrative is the move this project exists to call out. The known blind spot (parallel runs, post-training compute — already admitted in the epoch-5x claim's counterargument) is covered by adding `ai-compute-stock` (global installed H100e) as lead Tier-2 COMPUTE metric: stock compounding vs record-run flat, and the GAP between the two series is the finding — same pattern as announced-vs-energized in PHYSICAL.
**Pre-registered flip condition:** if the run record stays frozen through ~mid-2027 while stock keeps compounding — or Epoch stops estimating per-model training FLOP — promote stock to Tier-1 and demote the run series, because the forecasters' unit will have detached from reality. Log the flip under Reversals.

**D18. COMPUTE's Tier-1 metric moves from `largest-training-run-flop` (a max-statistic) to Epoch's frontier training-compute trend; the record run demotes to Tier-2. (M — decided 2026-07-27)**
Proposed by Ryan ("should probably be training compute total like Epoch shows"). The record-run series is a **max-statistic**, and max-statistics behave badly as trackers: they move only when a record falls, so they are flat by construction most of the time, and ours is **right-censored by its own source** — Grok 4.5, Gemini 3, and GPT-5.5-class models carry no Epoch estimate, so the series cannot move even if the frontier did. That made the board's most load-bearing verdict ("Record frozen 12 months — bulls running behind") **indistinguishable from a measurement artifact**, which is disqualifying for a Tier-1 metric. Epoch's frontier trend is a fit across the top-5 models and robust to any single missing estimate, so it becomes the stage headline. Epoch's separate 2e29-by-2030 **single-run feasibility** claim remains attached to the supporting record-run metric because that is the quantity it predicts; it is not used as the Tier-1 trend verdict.
COMPUTE now carries three views of one stage: the **trend** (Tier-1, robust), the **record run** (Tier-2 — what any single lab has actually done, where single-run claims like AI 2027's Agent-2 2e28 are still scored), and **stock** (Tier-2 — what exists in aggregate). Each catches what the others miss.
This does not overturn D17: that decision fixed training FLOP as the stage's unit and added stock as a companion, and its pre-registered flip condition concerned stock-vs-run. This is a different and narrower move — a more robust estimator of the same quantity.
**What the switch changed, concretely:** Aschenbrenner's ~0.5 OOM/yr compute claim scored **behind** against the record run and scores **ahead** against the trend — Epoch measures 0.7 OOM/yr (90% CI 0.6-0.8), and the top-5 median rose 3.89e25 to 1.677e26 in the year to Aug 2025. The record-run series was producing a false read on the single most-cited compute forecast on the board. Epoch's 5x/yr continuation likewise moved pending -> on-track now that it is scored against the series it is actually about.
**Caveat found while implementing:** the data bundle behind Epoch's chart ends 2025-08-06 even though the page banner reads Feb 2026, so the newest trend point is ~11 months stale. This is a publication lag rather than the censoring that afflicts the record run (which cannot move at all while new models lack estimates), but it means the COMPUTE stage currently has no measured 2026 value from either series. Recorded on the metric rather than smoothed over.
Revisit if: Epoch stops maintaining the frontier trend, or redefines its frontier set in a way that breaks series continuity (record the redefinition rather than silently splicing). If the published series stays frozen at Aug 2025 into 2027, the freshness problem has simply moved rather than been solved — reconsider the stage's Tier-1 choice again.

**D19. Newcomer-first orientation: three questions above the six-driver evidence spine. (M — decided 2026-08-12)**
The wound-spring hero asked a first-time visitor to decode an exponential chart, six colored strata, a forecast boundary, and a feedback loop before the site had explained the model. Replaced it with a plain-language causal diagram and a three-question overview: (1) are the inputs scaling, (2) are systems getting more capable, and (3) is progress feeding on itself? These are navigation and explanation layers, not a new measurement spine: the six Tier-1 metrics, forecast overlays, resolution statuses, confidence, evidence, and mandatory counterarguments are unchanged. Tier-2 metrics and chart mechanics now begin collapsed so the default page prioritizes the core story without deleting rigor.
Revisit if: user testing shows that returning expert readers cannot reach the evidence quickly enough, or that the three-question grouping obscures a load-bearing distinction. Prefer a remembered density setting or direct deep links over restoring the old hero complexity for everyone.

**D20. Compare forecast portfolios by status inventory, never by accuracy score. (H — decided 2026-08-12)**
The metric-first scoreboard made the original product question—how major forecast documents are holding up—expensive to answer because one source's claims were scattered across the six drivers. Added a source-first comparison that shows work, vintage, tracked-claim coverage, stage coverage, and the exact status mix. It deliberately publishes no win rate, average, rank, or weighted score: sources cover different quantities and deadlines, harvest depth ranges from one to eleven claims, and pending claims are not misses. Individual rows deep-link to the canonical claim card, where confidence, evidence, conditionality, and counterargument remain visible. Declared sources with no structured claims render as coverage gaps instead of disappearing.
Revisit if: a defensible proper-scoring rule is pre-registered before forecast resolution and applied to comparable probabilistic claims. Do not retrofit a leaderboard onto scenario prose and heterogeneous milestones.

**D21. Replace worldview cruxes with a causal safety-question chain. (H — revised 2026-08-12)**
The original seven were useful debate prompts but a weak public measurement framework: takeoff speed and compute-versus-insight are trajectory context, while “alignment is fundamentally hard,” “internal goals,” and “smarter becomes unstoppable” compress distinct and sometimes unobservable variables. The public layer now follows hazard → exposure → control → governance → incidents → resilience. Spectra remain only where opposing operational states are defensible; dangerous uplift uses a domain matrix, exposure uses a ladder without an invented current rung, and harms use an incident ledger without a false trend. The old crux data remains for provenance and historical research but is no longer the public safety framework.
Revisit if: the framework omits a causal safety stage, a question cannot be kept source-current, or a visual implies comparability the evidence does not support.

**D22. Epistemic type and scorability are first-class fields. (H — decided 2026-08-12)**
The tracker had counted scenarios explicitly described as “not a prediction,” lab goals, and a mood claim in the same “published forecasts” tally as falsifiable forecasts. Sources now declare whether they are forecasts, scenarios, model outputs, trend projections, intentions, or analysis. Claims resistant to clean adjudication use `context-only`: they remain visible but are excluded from headline status counts and plotted forecast marks. Original source URLs now render with every claim.
Revisit if: a finer per-claim type is required within a heterogeneous source. Never infer type from rhetoric at render time.

**D23. Evidence review and resolutions are append-only in the enforced schema. (H — decided 2026-08-12)**
The methodology promised append-only resolutions, but the JSON stored one mutable `resolution` object. Migrated every claim to `resolution_history`; validation enforces ordered entries and the renderer uses the latest while exposing the audit count. Added `refresh.json` with one policy and an append-only review log per metric, plus a maintainer check command and public health panel. Review freshness is explicitly separate from observation vintage and upstream source lag. The system never auto-fetches evidence or changes a human status judgment.
Revisit if: review schedules prove unrealistic. Adjust the declared policy rather than hiding overdue evidence.

**D24. Rename the product AI Trajectory and organize it around four questions. (H — decided 2026-08-12)**
“AI Risk Tracker” implied a risk level the project cannot honestly calculate; “AI Takeoff Tracker” narrowed away alignment and governance. AI Trajectory covers measurable progress and the safety questions that evidence cannot settle. The beginner sequence is build capacity → autonomous capability → self-acceleration → safeguards and control. The fourth question is an explicit measurement boundary, not a safety score.
Revisit if: readers still infer that “trajectory” predicts one inevitable path. Preserve the plural evidence streams and open-question framing.

**D25. Claim-to-measurement relationship gates aggregate results. (H — decided 2026-08-12)**
`scorability` alone still let unlike quantities enter the same totals. Every claim is now direct, translated, proxy, or context. Only direct and formula-backed translated claims feed headline inventories and plots; proxy/context claims remain visible with an exclusion marker. This changes aggregation honesty without silently changing an individual status judgment.
Revisit if: a proxy is replaced by a direct series, or a translation gains a reproducible formula. Update the relationship before restoring aggregate eligibility.

**D26. Every status records a structured assessment basis. (H — decided 2026-08-12)**
Prose evidence and a confidence number were not enough to reproduce a call. Each append-only assessment now records test type, target, deadline, observation metric, measurement relationship, comparison rule, and uncertainty driver. The UI exposes this under “How this status was assessed.”
Revisit if: stable observation IDs are introduced; then reference exact observation records rather than only the metric ID.

**D27. Observation provenance gaps are first-class data. (H — decided 2026-08-12)**
Metric-level canonical links were being asked to carry point-level provenance they could not always establish, especially for composite capex, revenue, policy, and power series. Every observation now declares either a named underlying series or `compiled-no-point-link`; the latter must carry a structured `provenance_gap_reason`. Tables link the former and visibly classify the latter. Crux evidence stores source label and URL separately. Missing citations are published as coverage debt, never backfilled by guesswork.
Revisit if: every composite point gains a direct filing, law, or announcement citation. Tighten validation rather than hiding the old gaps.

---

## Known weaknesses (the honest list — attack these first)

1. **The update pipeline remains manual.** _[PARTIALLY RESOLVED 2026-08-12: review schedules, source checklists, append-only outcomes, public due/stale health, and strict checks now exist. Canonical-source monitoring and candidate collection remain manual by design; do not automate human resolution judgment.]_
2. **Data population is ~10% done.** Only METR is fully worked; five Tier-1 metrics and most claims render honest "awaiting data" stubs. _[RESOLVED 2026-07-24: all six Tier-1 metrics populated, 24 claims human-signed-off. Tier-2 stubs (frontier-lab-revenue, policy-events) still block the production metrics.json flip.]_
3. **Forecast markers were silently mis-positioned until 2026-07-27** — claims with no parseable numeric target fell back to a y-position derived from list order, so a later, larger forecast could render below an earlier, smaller one. Fixed via an explicit human-recorded `predicted.plot_value` in the metric's own unit plus a labelled non-positional lane. The general lesson: any position on this site must be traceable to a recorded number, never to a rendering fallback.
4. **Resolution scoring is subjective and gameable** (D10, D14). The scoreboard's whole credibility rests on these calls being fair. Adversarially audit the counterarguments.
5. **Reality-side data has the same bot-gating/paywall friction as everything** — SEC, IEA, LBNL, SemiAnalysis are hard to fetch programmatically. "Citable" currently means "manually verified each cycle," which fights sustainability.
6. **Solo maintenance on a contentious topic.** Assume motivated submissions and brigading once public; the evidence standard + maintainer sign-off is the only moderation system.
7. **Three scope expansions in three sessions** (debate tracker → risk index → takeoff scoreboard). Each was defensible, but the ratchet is real. Discipline test for the next one: _is this a new view over the existing metric spine, or a new spine?_ New spines are where projects die.
8. **The harvest is under-persisted.** Only the Situational Awareness extraction is on disk (`docs/harvest/`); the other five source extractions (Forethought, Epoch, AI 2027, Davidson/Cotra, measurability audit) were synthesized into `scoreboard-metrics.md` but their verbatim form lives only in the originating session transcript. Persist them. _[RESOLVED 2026-07-13: all five recovered verbatim from the transcript into docs/harvest/. Note the measurability audit is a concatenation of four sub-agent results — no synthesized version ever existed.]_

## What a future model should probably do first

1. **Verify the harvest claims against their sources** — extracted by mid-2026 models, may contain errors; treat every quote as unverified until you re-fetch it.
2. **Re-run the D15 landscape scan** for new competitors.
3. **Adversarially pressure-test the D10 counterarguments** — find where the recorded one is weaker than the strongest available.
4. **Extend the D23 refresh pipeline with safe candidate monitoring only where canonical sources are machine-readable.**
5. **Finish data population** (Weakness 2), metric by metric, with the resolution calls surfaced for human ratification (D14).

## Reversals

_(Append dated entries here when you overturn a decision above. Cite the ID and the evidence. Do not edit the original decision — the point is a legible chain.)_
