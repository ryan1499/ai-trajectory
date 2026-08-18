# AI Trajectory

**[ai-trajectory.vercel.app](https://ai-trajectory.vercel.app)**

Where is AI headed? This beginner-friendly evidence map follows what labs can build, what systems
can do, whether progress is compounding, and whether safeguards can keep pace. It compares like-for-like
claims with reality and maps the safety questions measurements cannot settle.

The six forces feed back into each other — more compute buys better models, better models help
build AI, which pulls in more money and megawatts, which buys more compute:

| Force          | Tier-1 metric                                   | What it answers                                      |
| -------------- | ----------------------------------------------- | ---------------------------------------------------- |
| **Compute**    | Frontier training compute (Epoch top-5 trend)   | How much raw compute is being spent at the frontier? |
| **Algorithms** | Pretraining algorithmic efficiency              | How much more capability per FLOP?                   |
| **Capability** | Autonomous task-completion horizon (METR)       | What can a model finish without a human?             |
| **Automation** | AI R&D automation ladder                        | Is AI speeding up the research that builds AI?       |
| **Capital**    | Hyperscaler capex                               | Is conviction showing up in audited accounts?        |
| **Physical**   | Frontier cluster power (announced vs energized) | Can chips, power and construction keep up?           |

Two supporting metrics sit inside the COMPUTE card — largest known single training run and global
compute stock. Two more measure stages that carry no Tier-1 headline, so they render in their own
strip after the loop: frontier lab revenue (VALUE) and binding compute-threshold rules in force
(RESPONSE).

## What makes it different

The opening translates the debate into four questions: can the frontier keep building, what can models
do on their own, is progress beginning to feed on itself, and can safeguards keep pace? Claims are **overlaid on the
measurements they predict** and scored — never averaged into a single "risk number." A doomer and a
skeptic can use the same site because reality, rather than a composite opinion, adjudicates.

The default **Guided** view keeps the four questions, next checkpoints, safety questions, and core
measurements in focus. **Research** view restores portfolio comparison, evidence health, supporting
signals, milestone ladders, and revision history.

A source-first **forecast comparison** shows each major work's coverage and status mix without
collapsing unlike claims into an accuracy score. Registered sources whose claims have not yet been
harvested remain visible as explicit gaps rather than disappearing from the interface.

Eight **frontier-safety questions** follow risk from dangerous capability through exposure, control,
governance, incidents, and recovery—without reviving a subjective composite number. The visual form
matches the evidence: defensible binaries use qualitative spectra, dangerous uplift uses a domain
matrix, deployment uses an exposure ladder, and realized harm uses an incident ledger. Every reading
shows its setting, independence, coverage, caveats, and update conditions.

Every resolution carries a **status and a confidence as independent fields**, plus a **mandatory
counterargument** — including when the verdict is favourable. Scenarios, projections, intentions,
and ordinary forecasts are labeled separately. Direct and explicitly translated claims may enter
headline totals; proxy and context claims remain visible but excluded. Every status exposes its
measurement relationship and structured assessment rule. Self-reported figures carry an explicit discount.

## How it works

Data in `data/scoreboard/*.json` is the single source of truth. A stdlib-only Python build renders
it to static HTML — no framework, no database, no build dependencies. Python 3.11 or newer is
recommended:

```
python3 scripts/build.py     # -> dashboard/index.html + dashboard/methodology.html
```

- `data/scoreboard/metrics.json` — six Tier-1 metrics (one per force) plus the Tier-2 supporting
  metrics: their measured history, current value, sources, and measurement caveats.
- `data/scoreboard/claims.json` — every tracked claim: verbatim quote, conditionality, measurement
  relationship, and append-only assessments (status, confidence, evidence, test rule, counterargument).
- `data/scoreboard/refresh.json` — review schedules, canonical source checklists, and append-only review outcomes.
- `data/research/safety-questions.json` — the public severe-risk question chain, measurement design, evidence, gaps, and current readings.
- `data/cruxes.json` — the archived worldview-crux evidence retained for provenance and research links, not the public safety framework.
- `scripts/refresh.py` — reports which evidence streams are current, due, or stale without fetching or changing data.
- `scripts/scoreboard.py` — validation and all rendering. Invalid data fails the build.
- `dashboard/` — **generated. Never edit by hand.**

A claim only plots at a height when a human has recorded `predicted.plot_value` in that metric's own
unit. Rate claims, milestones, and claims about a different quantity than the axis measures are
deliberately left off the chart and listed with the claims instead — a position on this site must
always trace to a recorded number.

## Contributing

Disagree with a resolution? That's the point. Open an issue or a PR against the data — every number
is an auditable diff. Evidence needs a real source with a date. See [`CONTRIBUTING.md`](CONTRIBUTING.md)
for the evidence and review checklist.

## Integrity and limitations

This is a working prototype maintained by one person with AI-assisted research and implementation.
An early research pass introduced five plausible but false or mismatched evidence items. A
subsequent citation-by-citation audit removed or repaired them; the incident and the controls it
produced are documented in [`docs/research-integrity.md`](docs/research-integrity.md). That audit did
not verify every raw research note in the repository, and the public data still identifies
provenance gaps where a direct point citation is unavailable.

The tracked claim data, not the raw literature-harvest notes, is the public product record. Status
calls remain human judgments, evidence collection remains manual, and a current review date does
not imply that an upstream data series is current.

## Documentation

- [`docs/decisions.md`](docs/decisions.md) — **read this first.** Every load-bearing decision, its
  reasoning, and the conditions under which it should be reconsidered. Written so a future model can
  attack the decisions rather than re-derive them blind.
- [`METHODOLOGY.md`](METHODOLOGY.md) — how claims are extracted, scored, and resolved.
- [`docs/research-integrity.md`](docs/research-integrity.md) — correction history, verification scope,
  and known gaps.
- [`docs/provenance-and-rights.md`](docs/provenance-and-rights.md) — source provenance, quotation,
  and reuse boundaries.
- `docs/harvest/` — an archived AI-assisted research corpus; useful for provenance, not verified as a
  canonical source.

## License

Code is released under the [MIT License](LICENSE). Original project data and documentation are
released under [CC BY 4.0](LICENSE-CONTENT.md). Third-party quotations and source material are
excluded from those grants and remain subject to their original rights and terms.

Built by [Ryan Combes](https://github.com/ryan1499) with frontier models. The v1 crux tracker that
preceded this is in the git history.
