# Harvest archive — raw extraction results (July 12, 2026)

These files preserve raw AI-assisted outputs from the Phase 1 literature harvest. They are a
research archive, **not a verified source of record** and not an independent substitute for the
linked publications. Some were recovered from session transcripts, and some contain secondary or
paywalled-source reconstructions. Treat every quotation and numerical claim here as unverified until
it has been checked against an accessible primary source.

The structured files in `data/scoreboard/` are the public product record. Corrections happen there
with notes and append-only assessments. Third-party quotations in this archive are not covered by
the repository's content license; see [`../provenance-and-rights.md`](../provenance-and-rights.md).

- `situational-awareness-claims.md` — 62 claims, all chapters (Aschenbrenner, June 2024)
- `epoch-claims.md` — 23 vintage-dated projections + Epoch's maintained data-series inventory
- `forethought-claims.md` — 59 claims + the authors' own 12-item leading-indicator watch-list
- `davidson-cotra-claims.md` — takeoff-model and bio-anchors claims + model input parameters
- `ai2027-claims.md` — scenario claims, Dec 2025 revision arc, and 10 methodology lessons from the community tracker
- `measurability-audit.md` — 18 candidate metrics: source / cadence / cost / caveats / verdict

`reading-map.md` (the 80k list + quantitative canon) was planned but its harvest agent's output was never persisted and could not be located in the session transcript during the 2026-07-13 recovery pass — treat as lost pending a re-run, not as present.

All six files above except `situational-awareness-claims.md` were recovered verbatim from the session transcript on 2026-07-13 after the original harvest run ended without writing them to disk (only the Situational Awareness capstone was saved before context compaction). `measurability-audit.md` in particular is a straight concatenation of four parallel sub-agent results (metrics 1-5, 6/7/8/13/18, 9/10/14/15, 11/12/16/17) — the coordinator agent that was supposed to synthesize them into one table never did, so the four verbatim chunks are presented back-to-back instead.

Extraction rules these were produced under: docs/scoreboard-schema.md. Synthesis: docs/scoreboard-metrics.md.
