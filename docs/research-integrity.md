# Research integrity

AI Trajectory is a working prototype maintained by Ryan Combes with AI-assisted research,
implementation, and adversarial review. Ryan is the final sign-off point for evidence admission and
assessment judgments.

## The early evidence failure

An early multi-agent research pass introduced five plausible but false or mismatched evidence items
into the original crux-tracker dataset. A separate citation-verification pass checked all 67 evidence
citations in that dataset against their linked sources, removed the fabricated items, repaired three
URLs, and narrowed roughly ten claims to what their sources actually supported. The removed items
cut in different rhetorical directions; the failure was in the research process, not one preferred
conclusion.

The detailed correction record is preserved in `data/updates.json`, and the design consequence is
recorded in decision D6 in `docs/decisions.md`: source verification is a required pipeline stage.

## What that audit did not establish

The 67-citation audit covered the legacy crux evidence corpus. It did **not** verify every statement
in `docs/harvest/`, every later metric observation, or every external page linked by the current
scoreboard. Raw harvest files are preserved as research provenance and may contain errors. They are
not the public source of truth.

The current product also publishes known provenance debt. Some compiled observations do not yet
have direct point-level citations, and several comparisons rely on self-reported, derived, or proxy
evidence. Those limitations remain visible rather than being silently filled.

## Current controls

- Structured data is validated before rendering.
- Original-source wording and conditionality stay attached to each claim.
- Scenarios, forecasts, projections, intentions, and analysis are labeled separately.
- Only direct and formula-backed translated relationships enter headline totals.
- Assessments require evidence, a test rule, confidence, uncertainty, and a counterargument.
- Evidence reviews and resolution histories are append-only.
- Automated research may prepare candidates but cannot change a status without human approval.

## Corrections

If a source, quotation, observation, or judgment is wrong, open an issue or pull request with the
source and the proposed correction. Material corrections add a dated record; they do not erase the
fact that the earlier version existed. See [`CONTRIBUTING.md`](../CONTRIBUTING.md).
