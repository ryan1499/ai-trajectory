# Archived v2 Vision: From Debate Tracker to Open Risk Index

**Status: archived proposal — not adopted. Owner: Ryan. Drafted 2026-07-12. Superseded by the
non-composite AI Trajectory design recorded in `README.md`, `METHODOLOGY.md`, and decisions D21–D27.**

## The reframe

v1 answers "where does the AI safety _debate_ stand?" — it measures positions in an argument. v2 answers a different question: **"how much risk are we actually carrying, and which way is it moving?"** — it measures the risk itself, to the extent that's honestly possible.

The first-principles question — _if we wanted to objectively quantify AI risk across all its dimensions, what would that look like?_ — has a trap in it. A fully objective AI risk number does not exist; any project claiming one gets correctly dismissed by both camps within a week. What **can** exist, and doesn't yet (pending prior-art scan), is a **reproducible** risk index: one where every step from raw evidence to headline reading is disclosed, versioned, and attackable via pull request, and where the irreducibly subjective parts are carried as _explicit, adjustable parameters_ instead of being smuggled into the weights.

The product claim is not "this number is true." It is: **"here is exactly how this number is made — change any input you disagree with and see what happens."** Reproducibility is the moat; radical transparency is the brand.

## Scope declaration (required, currently a proposal)

The index measures **catastrophic and systemic risk from frontier AI**: loss-of-control scenarios, catastrophic misuse (cyber, bio), and systemic erosion (governance failure, uncontrolled proliferation, deep integration without safeguards). Routine product harms (bias incidents, deepfakes, job displacement) enter only as _leading indicators_ where they evidence a tracked dimension — they are not scored as risk in themselves. This must be stated on the site; most criticism of composite indices comes from scope ambiguity.

## Architecture: three layers

```
Layer 1 — INDICATORS   observable, dated, source-verified measurements
        │              (METR horizons, scheming eval rates, interp coverage,
        │               open-weight diffusion %, incident counts, ...)
        ▼  disclosed transform: raw value → normalized 0-100 subscore
Layer 2 — DIMENSIONS   six composite subscores with disclosed weights
        │
        ▼  disclosed aggregation + worldview parameters
Layer 3 — OUTLOOK      the headline reading: a RANGE, not a point,
                       with visible sensitivity to worldview settings
```

### Layer 2: the six dimensions

Risk = hazard × exposure ÷ safeguards — the classic decomposition from catastrophe modeling, adapted:

| #   | Dimension                               | What it measures                                                           | Example indicators (mostly already tracked in v1)                                                                         |
| --- | --------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Capability pressure**                 | How fast dangerous capability frontiers advance                            | METR time horizon + doubling rate, cyber benchmark saturation, bio-uplift eval results, compute growth                    |
| 2   | **Misalignment propensity**             | Evidence that systems develop goals conflicting with operators             | Scheming/deception rates in cross-lab evals, reward-hacking generalization, eval-awareness prevalence                     |
| 3   | **Containment & verification capacity** | Can we detect, verify, and correct — counts _against_ risk                 | Interp coverage (J-lens et al.), CoT monitorability, deception-probe robustness, control-eval results                     |
| 4   | **Governance capacity**                 | Enforceable institutional grip — counts _against_ risk                     | Binding-rule coverage, RSP integrity (pause triggers intact?), verification-tech readiness, treaty progress               |
| 5   | **Exposure & integration**              | How much surface area we've handed over — **new; v1's biggest blind spot** | Agent deployment in critical systems, autonomy levels granted, open-weight frontier diffusion, tool/actuator access norms |
| 6   | **Realized harm signal**                | Trailing ground truth that keeps the model honest                          | AI Incident Database counts/severity, documented autonomous-harm events (e.g., the Claude Code espionage campaign)        |

Note what happened to v1: the **indicators become Layer 1** (largely as-is), the **evidence discipline** (dated, source-verified, adversarially checked) becomes the Layer 1 admission standard, the **update log and history** carry forward as the integrity spine — and the **cruxes move to Layer 3**.

### Layer 3: cruxes become worldview parameters

The cruxes were never measurements — they're the _contested conversion rates_ between dimensions. "Takeoff speed" determines how fast capability pressure converts to hazard. "Does smarter cash out as unstoppable" determines how much capability pressure matters at all versus exposure. "Compute-bound vs insight-bound" determines whether hardware bottlenecks discount capability trajectory.

So the headline reading is published as: **central reading (under declared default parameters) + band (across defensible parameter ranges) + a sensitivity view** — "under fast-takeoff settings this reads X, under slow-takeoff Y." This is the intellectually honest way to get one shareable number: a number that discloses how much of itself is evidence and how much is worldview. No other index does this (to be confirmed by landscape scan). It is also the feature that lets both a doomer and a skeptic use the same site without either dismissing it.

## Methodology principles (to become METHODOLOGY.md v1.0)

1. **Every transform is written down.** Indicator → subscore normalizations (with anchor points and rationale), subscore → dimension weights, dimension → composite aggregation. If it isn't in METHODOLOGY.md, it doesn't affect the number.
2. **Weights v1 are declared priors, and say so.** No fake elicitation. Label: "v1 weights are the maintainers' declared priors; sensitivity to ±50% weight perturbation is published alongside. Weight RFCs welcome."
3. **Aggregation punishes false comfort.** Weighted geometric mean (HDI-style) or soft-min for the safeguard dimensions, so one collapsed safeguard can't be averaged away by good news elsewhere. Exact function: an open decision, documented with worked examples.
4. **The number never travels alone.** The shareable artifact is always `reading + band + methodology version` (e.g., "**58 [44–71] · v1.0**"). Rendered into the OG/social image itself so screenshots carry the caveat.
5. **Versioned like an index provider.** METHODOLOGY.md is semver'd. Methodology changes recompute a _backcast series_ published separately from the as-published series; as-published values are never rewritten (the v1 rule, kept).
6. **Provenance disclosure.** Research passes are AI-assisted with human sign-off; every citation is adversarially verified against its source before admission. This is already true of v1 — in v2 it's a published pipeline stage, not a private discipline. It preempts the "an AI wrote this" attack by making it a feature.

## Contribution model (GitHub-native, no new infrastructure)

- **Evidence PRs** — add/challenge an indicator reading or evidence item; CI validates schema + link liveness; maintainer verifies source before merge.
- **Weight/methodology RFCs** — issues using a template; accepted RFCs bump the methodology version.
- **Crux challenges** — dispute a worldview-parameter range with evidence.
- Repo governance from day one: CONTRIBUTING.md, evidence standards, CODEOWNERS (Ryan as maintainer-of-record), a decision log. Politically charged topic ⇒ assume motivated submissions and brigading; the evidence standard and maintainer sign-off are the moderation system.

## What v2 explicitly does NOT include (deleted before it exists)

Backend, database, user accounts, comments, community weight-voting, live API ingestion, a separate contribution UI. The stack remains: JSON in git → stdlib Python build → static hosting. GitHub is the community layer. Each of these earns its way back only when a manual process it would automate is already proven (algorithm step 5).

## Open decisions (Ryan)

1. **Scope** — catastrophic/systemic focus as declared above, or broaden to all harms? (Recommend: catastrophic/systemic. Broadening dilutes the differentiator and triples maintenance.)
2. **The headline number** — publish composite reading + band from launch, or launch dimensions-only and add the composite after the methodology survives public contact? (Recommend: composite from launch, _because_ the band/sensitivity design is the differentiator — but it's the highest-stakes call.)
3. **Naming/brand** — pending landscape scan collision check. "The Crux Report" name fits v1's framing more than v2's.
4. **Attribution** — your name on it, or pseudonymous/organizational? Affects shareability, credibility, and your personal exposure to a contentious discourse.
5. **Cadence commitment** — monthly full pass is the honest floor for an index that claims to be alive. A visibly stale index is worse than none.

## Prior art & differentiation (landscape scan, July 2026)

| Project                                                                      | What it is                                                                                         | Composite?                 | Weights disclosed                              | Versioned         | Open contribution                     | Worldview sensitivity |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------- | ---------------------------------------------- | ----------------- | ------------------------------------- | --------------------- |
| [Frontier Risk Monitor](https://www.frontierriskmonitor.org/)                | Quarterly "Global AI Risk Index" (72/100 "ELEVATED," Q1 2026), 6 weighted categories, NIST-aligned | **Yes**                    | Yes (in report)                                | No                | **No** (closed, anonymous authorship) | No                    |
| [FLI AI Safety Index](https://futureoflife.org/ai-safety-index-summer-2026/) | Biannual letter grades for 9 companies, ~37 indicators, expert panel                               | Per-company                | Partially ("discretionary" reviewer weighting) | No changelog      | No (survey + panel)                   | No                    |
| [SaferAI Tracker](https://tracker.safer-ai.org/)                             | Lab risk-management practice scores, 65 criteria                                                   | Per-company %              | **Yes, fully**                                 | **Yes (v1→v2)**   | No                                    | No                    |
| [MIT AI Risk Repository](https://airisk.mit.edu/)                            | Taxonomy DB: 1,700+ risks from 65+ frameworks; incident tracker                                    | No (explicitly)            | n/a                                            | Dataset versions  | Submission form                       | n/a                   |
| [Epoch ECI](https://epoch.ai/eci)                                            | Composite _capability_ index (IRT over 50+ benchmarks)                                             | Yes (capability, not risk) | Statistical (IRT)                              | Not yet           | Partial                               | No                    |
| Metaculus                                                                    | Per-question open forecasting; AI Safety tournament                                                | No                         | n/a                                            | n/a               | **Yes** (forecasts)                   | No                    |
| AIID / OECD AIM                                                              | Incident logs                                                                                      | No                         | n/a                                            | Taxonomy versions | AIID yes / AIM not yet                | n/a                   |
| Int'l AI Safety Report                                                       | Annual expert narrative (Bengio, 100+ experts)                                                     | No                         | n/a                                            | Editions          | No                                    | No                    |
| Doomsday Clock / IMD AI Safety Clock                                         | Symbolic single readings                                                                           | Symbolic                   | No                                             | No                | No                                    | No                    |
| [airiskindex.com](https://airiskindex.com)                                   | Small BlueDot course project, 4 indicators, 0-100 score                                            | Yes                        | Partial                                        | No                | Nominally (stale since Oct 2024)      | No                    |

**Differentiators that survived the scan** (each verified absent from everything above):

1. **Worldview-parameter sensitivity** — no project separates contested assumptions (takeoff speed etc.) from evidence and publishes the reading's sensitivity to them. FLI buries judgment in discretionary weights; MIT avoids composites entirely; Metaculus disagreement is per-question. This is the genuine gap and should be the headline differentiator.
2. **Fully open, PR-driven evidence pipeline with per-citation adversarial verification** — AIID accepts incident submissions, MIT has a form, but no risk _index_ is open-source and contribution-governed.
3. **Versioned methodology with backcast series** — only SaferAI versions its methodology at all; nobody backcasts.

**The closest threat** is Frontier Risk Monitor (launched ~March 2026): quarterly, six weighted categories, composite number. It is closed-source, anonymously authored, narrative-sourced, and has none of the three differentiators — position against it explicitly ("the open, auditable alternative") rather than pretending it doesn't exist.

**Adopt, don't invent:** cite the MIT AI Risk Repository taxonomy for categorizing Layer 1 evidence (legitimacy + interop), CSET's harm taxonomy for the realized-harm dimension, and SaferAI/FLI scores themselves as candidate _indicators_ inside the governance dimension (an index can consume other indices).

**Naming (now a forced decision):** "AI Risk Tracker" collides with a live trademarked consultancy (airisktracker.com, AI Risk Tracker™ LLC); "AI Risk Index" collides with airiskindex.com (small but live, same concept). Both hyphenated domains, and both names on npm/PyPI, are free — but launching public under either invites confusion or friction. Recommendation: rebrand before public launch, keeping "crux" equity (it's distinctive, already ours, and names the differentiator — e.g., "Crux Index" or similar; run a fresh collision check on the shortlist before committing). The private GitHub repo name can stay `ai-risk-tracker` until then.
