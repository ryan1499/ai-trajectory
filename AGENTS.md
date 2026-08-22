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
identity in the checked-out public ref's full ancestry. These checks
intentionally report only pass/fail/counts—do not change them to reveal
addresses or add a bypass.

If a privacy check fails, stop and correct the identity or remove sensitive
content without exposing it in output, commits, documentation, or issues.
