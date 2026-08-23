#!/usr/bin/env python3
"""Redacted Git identity and staged-content privacy checks for AI Trajectory.

This utility deliberately never prints an email address. It is safe to use in
local hooks and CI output. It requires GitHub user-noreply author identities,
allows only GitHub's platform-generated merge identity as a committer exception,
and rejects any non-noreply email address introduced in staged lines.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path


NOREPLY_DOMAIN = "users.noreply.github.com"
EMAIL_RE = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})(?![\w.-])")
NOREPLY_EMAIL_RE = re.compile(r"^[^@\s]+@users\.noreply\.github\.com$", re.IGNORECASE)
GITHUB_PLATFORM_COMMITTER = "@".join(("noreply", "github.com"))


def git(*args: str) -> subprocess.CompletedProcess[str]:
    """Run Git without forwarding potentially sensitive output."""
    return subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )


def is_noreply(email: str) -> bool:
    return bool(NOREPLY_EMAIL_RE.fullmatch(email))


def is_allowed_committer(email: str) -> bool:
    return is_noreply(email) or email.casefold() == GITHUB_PLATFORM_COMMITTER


def report(name: str, passed: bool, **counts: int) -> bool:
    state = "PASS" if passed else "FAIL"
    count_text = " ".join(f"{key}={value}" for key, value in counts.items())
    print(f"privacy_check: {name}={state}" + (f" {count_text}" if count_text else ""))
    return passed


def check_config() -> bool:
    # The repository-local setting prevents a later global configuration change
    # from silently changing this public repository's commit identity.
    result = git("config", "--local", "--get", "user.email")
    configured = result.returncode == 0 and bool(result.stdout.strip())
    identity_valid = configured and is_noreply(result.stdout.strip())
    config_only = git("config", "--local", "--get", "user.useConfigOnly")
    config_only_valid = config_only.returncode == 0 and config_only.stdout.strip().lower() == "true"
    valid = identity_valid and config_only_valid
    return report(
        "configured_identity",
        valid,
        configured=int(configured),
        invalid=int(configured and not identity_valid),
        config_only=int(config_only_valid),
    )


def history_identities() -> Iterable[tuple[str, str]]:
    # Only the public history reachable from the checked-out ref belongs in
    # this check. Local archive/remotes may intentionally retain old history.
    # CI fetches this public ref's complete ancestry before running the check.
    revisions = git("rev-list", "HEAD")
    if revisions.returncode != 0:
        return ()
    commit_ids = [line for line in revisions.stdout.splitlines() if line]
    if not commit_ids:
        return ()
    identities = git("log", "HEAD", "--format=%ae%x00%ce%x00")
    if identities.returncode != 0:
        return ()
    emails = [email.strip() for email in identities.stdout.split("\x00") if email.strip()]
    return zip(emails[0::2], emails[1::2], strict=True)


def check_history() -> bool:
    revisions = git("rev-list", "HEAD")
    commit_count = len([line for line in revisions.stdout.splitlines() if line]) if revisions.returncode == 0 else 0
    identities = list(history_identities())
    invalid_authors = sum(not is_noreply(author) for author, _ in identities)
    invalid_committers = sum(not is_allowed_committer(committer) for _, committer in identities)
    invalid = invalid_authors + invalid_committers
    return report(
        "history",
        invalid == 0,
        commits=commit_count,
        invalid_identities=invalid,
        invalid_authors=invalid_authors,
        invalid_committers=invalid_committers,
    )


def check_staged() -> bool:
    result = git("diff", "--cached", "--no-ext-diff", "--unified=0")
    if result.returncode != 0:
        return report("staged_content", False, added_lines=0, disallowed_emails=0)

    added_lines = 0
    disallowed = 0
    for line in result.stdout.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        added_lines += 1
        for match in EMAIL_RE.finditer(line[1:]):
            if match.group(1).lower() != NOREPLY_DOMAIN:
                disallowed += 1
    return report("staged_content", disallowed == 0, added_lines=added_lines, disallowed_emails=disallowed)


def check_tracked() -> bool:
    """Reject non-noreply addresses anywhere in the tracked text corpus.

    This closes the gap left by an additions-only pre-commit check: CI can use
    it to catch an address already present in a pushed file or introduced by a
    client that did not install the repository hook. Binary files are skipped.
    Paths and matched text are intentionally never printed.
    """
    result = git("ls-files", "-z")
    if result.returncode != 0:
        return report("tracked_content", False, text_files=0, disallowed_emails=0)

    text_files = 0
    disallowed = 0
    for path_text in result.stdout.split("\0"):
        if not path_text:
            continue
        path = Path(path_text)
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:8192]:
            continue
        text_files += 1
        content = data.decode("utf-8", errors="ignore")
        for match in EMAIL_RE.finditer(content):
            if match.group(1).lower() != NOREPLY_DOMAIN:
                disallowed += 1
    return report("tracked_content", disallowed == 0, text_files=text_files, disallowed_emails=disallowed)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Git privacy without revealing email addresses.")
    parser.add_argument("--config", action="store_true", help="Require local Git user.email to be GitHub noreply.")
    parser.add_argument("--history", action="store_true", help="Check all reachable commit author/committer identities.")
    parser.add_argument("--staged", action="store_true", help="Check added staged lines for non-noreply email addresses.")
    parser.add_argument("--tracked", action="store_true", help="Check every tracked text file for non-noreply email addresses.")
    args = parser.parse_args()

    checks = (args.config, args.history, args.staged, args.tracked)
    if not any(checks):
        parser.error("choose at least one check: --config, --history, --staged, or --tracked")

    results = []
    if args.config:
        results.append(check_config())
    if args.history:
        results.append(check_history())
    if args.staged:
        results.append(check_staged())
    if args.tracked:
        results.append(check_tracked())
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
