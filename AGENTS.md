# AI Trajectory agent guidance

## Privacy is non-negotiable

Never use, print, save, or commit a personal email address. Commits from this
public repository must use a GitHub noreply identity ending in
`@users.noreply.github.com`.

Before making a commit in a new clone, run
`scripts/setup_privacy.sh <github-username>`. It configures the repository's
local hook path and a GitHub noreply address only. The pre-commit hook checks
the configured identity, staged additions, and the complete tracked text
corpus. CI checks the same tracked content plus every author and committer
identity in the checked-out public ref's full ancestry. Authors must always use
the repository's user-noreply form. The checker permits GitHub's
platform-generated merge committer identity as its only exception. These
checks intentionally report only pass/fail/counts—do not change them to reveal
addresses or add another bypass.

If a privacy check fails, stop and correct the identity or remove sensitive
content without exposing it in output, commits, documentation, or issues.

## Preserve the task-based site structure

The generated public site has six canonical destinations: Overview, Evidence,
Forecasts, Safety, Research map, and Methodology. Do not recombine them into one
long dashboard or restore the old global Guided/Research mode. Use page-local
`<details>` for progressive disclosure.

Evidence owns measurements and non-milestone claim cards. Forecasts owns Watch
next, source comparison, milestone claims, and revisions in that order. Safety's
eight-question chain is distinct from the ten-question Research map. Use the
link helpers in `scripts/scoreboard.py`, preserve the overview's legacy-hash
migration, and keep the build's cross-page page/fragment validation passing.
