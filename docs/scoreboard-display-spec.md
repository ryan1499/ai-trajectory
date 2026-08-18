# Scoreboard Display Spec v2 — "Verdict First"

**Status: approved by Ryan 2026-07-24. Implementation contract for the rendering layer (scripts/scoreboard.py + template). Data files are NOT to be populated or re-scored by the implementer — rendering only.**

## Problem

The built page is ~6,200 words rendered at uniform volume (~5,000 in the six metric sections). The epistemics (quotes, conditionality, counterarguments) are the product's credibility, but they currently render as ambient text. Goal: **verdict first, rigor one click deep.** Visible-by-default budget: **≤ ~600 words**. Nothing is deleted — everything moves behind expanders.

## 1. Verdict layer (new, directly under the hero)

- **Global tally strip**, computed at build time from claims data: counts of `resolution.status` across ALL claims (Tier-1 and Tier-2 metrics). Render as one line of status-colored segments, e.g.:
  `27 forecasts tracked — 1 resolved true · 1 ahead · 13 on-track · 4 behind · 8 pending`
  Omit zero-count statuses. Each segment gets the status color (see §4). The strip is a summary, not a link farm — one anchor to `#loop` is enough.
- **Per-stage verdict line**: metrics may now carry an optional `verdict` field (short editorial string, ≤70 chars, human-written — already present in the seed data). Render it (a) in the six-stage strip card for that stage's Tier-1 metric, small mono, and (b) as a subtitle in the metric section header. If absent, render nothing (no placeholder).
- **One global explainer** sentence under the tally ("Markers show each claim's stated target and date; every resolution carries its counterargument — open any claim to audit it."). Delete the per-section repeats of chart-explainer prose.

## 2. Metric card slimming

Always-visible per metric section, in order:

1. Stage eyebrow (number + stage name) + metric name + `verdict` subtitle if present.
2. The current value: `current.display` big, with confidence rendered as a small tag (see §4), NOT a sentence.
3. One compressed freshness line derived from `last_checked` + `source_cadence`: format `checked 2026-07-24 · <first clause of source_cadence>` (truncate source_cadence at the first em-dash/semicolon; full text lives in the expander).
4. The chart (unchanged).
5. The claim chip row (§3).

Everything else moves into the existing per-metric `<details>` expander: `source_note`, `unit`, `what_it_measures`, measurement notes, history-inspection helper text, canonical source link (keep a small ↗ icon visible next to the metric name pointing at `source.url`).

## 3. Claim chips

Replace the single "N FORECAST CLAIMS · MEASUREMENT NOTES" accordion with a **visible chip row** under each chart:

- One chip per claim: `[camp-colored left border] Forecaster-short-name · STATUS-BADGE · NN` (NN = confidence numeral, mono).
- Forecaster short name = first word of the source author ("Leopold" → use author surname; map via forecast_sources: Aschenbrenner→"Leopold", Epoch AI→"Epoch", Kokotajlo/Lifland et al.→"AI 2027", AI Futures Project→"AI Futures", MacAskill/Davidson et al.→"Forethought", Tom Davidson→"Davidson", Morgan Stanley→"Morgan Stanley", Sam Altman (OpenAI)→"Altman", Ajeya Cotra→"Cotra", Ege Erdil→"Erdil"). Implement as a small mapping on source id, falling back to `author`.
- Each chip is a `<details>`/`<summary>` (summary = the chip): expanding reveals that claim's full card — quote (with quote_location), conditionality, predicted value/by, evidence, counterargument, as_of. Same content as today, per-claim instead of all-at-once.
- Measurement notes become their own small expander at the end of the section ("Measurement notes ⓘ").

## 4. Visual encoding (replace words with marks)

- Status badge colors (badge = small filled/outlined pill, uppercase mono ≤11px):
  - `resolved-true`: filled moss-deep `#24392d`, paper text
  - `ahead`: filled moss `#3c5c48`, paper text
  - `on-track`: moss outline, moss text
  - `pending`: neutral outline `rgba(28,43,40,.4)`, muted text
  - `behind`: filled gold `#a8863a`, ink text
  - `falsified`: filled signal `#b5432a`, paper text
- Confidence: bare mono numeral in the chip (no bar, no percent sign).
- Staleness: if `current.as_of` is older than 12 months at build time (compare to `last_checked`, not wall clock — build must stay deterministic), render a gold `VINTAGE <as_of>` tag beside the current value (this is the algorithmic-efficiency feature).
- Camp colors: keep the existing camp palette for chip borders and chart markers — unchanged.

## 5. Tier-2 supporting slots

Render Tier-2 metrics as **compact supporting cards inside their stage's Tier-1 section**, after the claim chips: metric name + `current.display` (if populated) + chip row (if claims exist) + expander with the same anatomy as Tier-1 (smaller type scale, no chart required; render a small chart only if `history` has ≥3 points). Unpopulated Tier-2 stubs render one muted line: "`<name or id>` — awaiting data." Tier-2 metrics whose stage has no Tier-1 section (`value`, `response`) render in a single compact "Supporting signals" strip between the last stage section and the milestone ladder.

This brings `ai-compute-stock` (populated, 3 claims) onto the page — its `verdict` field should render on its supporting card.

## 6. Demotions

- **Methodology** → its own generated page `dashboard/methodology.html` (same head/styles, rendered from METHODOLOGY.md exactly as the current section is). Header/footer link "Methodology" replaces the on-page section. Keep a `#methodology` anchor on the main page that is just the link block, so old links don't 404 into nothing.
- **Milestone ladder** → compact: five rungs, each ONE visible line (rung label + status dot derived from the most advanced status among claims carrying that `ladder_rung`: any resolved-true → filled; any on-track/ahead → half; else empty) + per-rung expander listing its claims as chips (§3 anatomy).
- **Forecast drift** section: unchanged (it is already compact and awaiting data).

## 7. Validation changes

- Allow optional `verdict` (string, ≤80 chars hard limit) on metric objects — both seed and production modes.
- Add a build WARNING (stderr, non-fatal) when `current.display` exceeds 60 characters — data cleanup follows separately; do not fail the build.
- No other schema changes. Anchors `#metric-{id}`, `#loop`, `#milestones`, `#forecast-drift` must survive.

## 8. Non-goals / constraints

- No JS frameworks, no external dependencies, no network fetches. Stdlib Python only. The page may use vanilla `<details>` + the existing inline JS patterns.
- Do NOT populate, re-score, or reword any data values, quotes, resolutions, or notes. Rendering only. (Decision D14.)
- Do NOT redesign the hero. Leave current hero markup as-is; add an HTML comment `<!-- hero-viz-slot -->` immediately after the hero copy block for a later visual.
- Keep seed/production mode behavior and the "Seed data preview" label logic.
- Design system unchanged: Bitter / Source Serif 4 / JetBrains Mono; paper `#eef0e9`, ink `#1c2b28`, moss `#3c5c48` / `#24392d`, signal `#b5432a`, gold `#a8863a`. Chips/badges must feel like the existing editorial-instrument aesthetic (hairline borders, mono small caps), not web-app pills.

## Acceptance checks

1. `python3 scripts/build.py` exits 0; writes `dashboard/index.html` AND `dashboard/methodology.html`.
2. Global tally counts match a manual count of `resolution.status` values in the claims file.
3. Default-visible word count of index.html (all `<details>` content stripped) ≤ ~600 words. Print this count at build time.
4. Every claim in the data appears exactly once as a chip; every chip expands to show quote + conditionality + evidence + counterargument.
5. `ai-compute-stock` renders as a supporting card under the COMPUTE section with its 3 chips.
6. Anchors listed in §7 resolve.
