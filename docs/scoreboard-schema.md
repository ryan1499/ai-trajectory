# Scoreboard Schema — Metrics & Forecast Claims

**Status: archived Phase-0 draft. Retained for design provenance; the enforced schema in
`scripts/scoreboard.py` and the current structures in `data/scoreboard/` are authoritative.**

## The spine: eight stages of the takeoff loop

Every metric attaches to exactly one stage. The stages generalize the capability-to-capital feedback loop (Aschenbrenner's engine, without being tied to his predictions):

| Stage         | What it covers                                                     | The question it answers                     |
| ------------- | ------------------------------------------------------------------ | ------------------------------------------- |
| 1. COMPUTE    | Training + inference capacity, largest runs, cluster scale         | How much raw compute exists and is coming?  |
| 2. ALGORITHMS | Algorithmic efficiency, unhobbling (agency, memory, tools)         | How much more capability per FLOP?          |
| 3. CAPABILITY | Task horizons, benchmark frontiers, domain evals                   | What can systems actually do?               |
| 4. AUTOMATION | AI performing AI R&D — the hinge of every takeoff model            | Is the loop closing?                        |
| 5. VALUE      | Revenue, adoption, margins after inference cost                    | Is capability converting to economic value? |
| 6. CAPITAL    | Capex, financing, valuations                                       | Is value unlocking investment?              |
| 7. PHYSICAL   | Power (announced vs energized), chips, packaging, land, lead times | Is the physical world keeping up?           |
| 8. RESPONSE   | Policy, export controls, security mandates, national programs      | Are institutions mobilizing or braking?     |

Loop: 1→2→3→4 (feeds back into 2)→5→6→7 (feeds back into 1); 8 modulates everything.

## Object 1: Metric

```
{
  "id": "hyperscaler-capex",
  "name": "Combined Big-4 hyperscaler capex (annualized)",
  "stage": "capital",
  "unit": "USD billions / year",
  "cadence": "quarterly (earnings)",
  "sources": ["MSFT/GOOGL/AMZN/META earnings calls", "..."],
  "measurement_notes": "Guidance vs actuals; not all capex is AI; note each company's disclosure basis.",
  "current": { "value": ..., "as_of": "YYYY-MM", "source": "..." },
  "history": [ { "date": "...", "value": ..., "source": "..." } ],
  "tier": 1 | 2 | 3
}
```

**Ranking criteria for tiering** (scored in Phase 2, cut by Ryan in Phase 3):

1. **Diagnosticity** — how much a surprise in this metric should update the overall takeoff picture.
2. **Measurability** — public, frequent, unambiguous, likely to keep existing. "Announced megawatts" and "energized megawatts" are different metrics; prefer the one closer to ground truth.
3. **Forecast coverage** — how many published forecasts make claims about it. The scoreboard is only as interesting as the bets laid on each metric.

Tier 1 (~6): the headline dashboard. Tier 2 (~10): supporting. Tier 3: watchlist, tracked but not featured.

## Object 2: Forecast claim (overlays a metric)

```
{
  "id": "sa-capex-1t-2027",
  "source_work": "Situational Awareness: The Decade Ahead",
  "author": "Leopold Aschenbrenner",
  "published": "2024-06",
  "claim_type": "trajectory" | "milestone",
  "scorability": "scored" | "context-only",
  "measurement_relation": {
    "type": "direct" | "translated" | "proxy" | "context",
    "note": "why the metric is or is not a like-for-like test",
    "formula": "required only for translated claims"
  },
  "metric_id": "hyperscaler-capex",
  "quote": "verbatim sentence(s), with section/page cite",
  "predicted": { "value": ..., "by": "YYYY[-MM]" },
  "conditionality": "How the author framed it: unconditional forecast, conditional scenario, illustrative projection. Quote their own hedge verbatim. Misrepresenting a scenario as a prediction is the cardinal sin here.",
  "resolution_history": [{
    "status": "pending | on-track | ahead | behind | falsified | resolved-true",
    "confidence": 0,
    "as_of": "YYYY-MM",
    "evidence": "1-3 sentences against the metric's current value",
    "evidence_urls": ["https://canonical-measurement-source.example"],
    "provenance_scope": "metric-series",
    "assessment_basis": {
      "test_type": "target-and-deadline",
      "target": "copied structured target",
      "deadline": "copied structured deadline",
      "observation_metric_id": "hyperscaler-capex",
      "measurement_relation": "direct",
      "comparison_rule": "reproducible test statement",
      "uncertainty_drivers": ["strongest source of uncertainty"]
    },
    "counterargument": "strongest recorded objection"
  }]
}
```

Milestone claims (e.g., "automated AI researcher by 2028") attach to the AUTOMATION or CAPABILITY stage's milestone metrics rather than a numeric series.

## Extraction rules (for harvest agents and future contributors)

1. Quote verbatim; cite section. No paraphrase-as-quote.
2. Record the prediction's own date — a 2024 claim about 2026 is scored against what was knowable in 2024.
3. Capture the author's hedging exactly. Conditional scenarios are labeled as such.
4. Dated + quantifiable (or crisply milestone-shaped) claims may be scored. Historically influential but non-resolvable statements can enter only as `context-only`; they never affect totals or charts.
5. Every resolution judgment carries a source and date; resolutions are append-only (re-resolve later with a new entry, never overwrite).
