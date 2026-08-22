# Contributing

AI Trajectory is designed to be challenged. Issues may propose evidence, identify a source problem,
or dispute an assessment. Pull requests are welcome for changes that can be represented as an
auditable diff.

## Privacy before committing

This public repository accepts only GitHub noreply commit addresses. Before your first commit in a
clone, run `scripts/setup_privacy.sh <github-username>` to enable the repository hook and configure
a local noreply identity. The hook refuses a non-noreply configured address and non-noreply email
addresses in staged additions or anywhere in tracked text. CI repeats the tracked-content scan and
checks the full public commit ancestry. These checks report only redacted pass/fail counts.

Do not put personal email addresses in commits, source files, examples, issues, or pull requests.
There is intentionally no bypass for public-repository changes. If the check fails, remove the
sensitive content and correct your local Git identity before proceeding.

## Evidence checklist

Before submitting a claim, observation, or assessment:

1. Link the accessible primary source when one exists; identify secondary or paywalled sourcing.
2. Preserve the source's wording, date, scope, units, and conditionality.
3. Classify the source's epistemic type and the claim-to-measurement relationship.
4. Do not infer a chart position from prose. Record any conversion and its formula explicitly.
5. Add rather than overwrite observations, evidence reviews, and resolution assessments.
6. Include the strongest counterargument and the main uncertainty driver.
7. Run `python3 scripts/build.py` and `python3 scripts/refresh.py`.

An issue or pull request is a proposal, not admission to the public dataset. The maintainer checks
the source and retains final responsibility for status judgments. See
[`METHODOLOGY.md`](METHODOLOGY.md) and [`docs/research-integrity.md`](docs/research-integrity.md).
