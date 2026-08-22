#!/usr/bin/env sh
# Configure this checkout to use the committed privacy hook and a GitHub
# noreply identity. This script never accepts or writes a personal email.
set -eu

if [ "$#" -ne 1 ] || ! printf '%s' "$1" | grep -Eq '^[A-Za-z0-9-]+$'; then
  echo "Usage: scripts/setup_privacy.sh <github-username>" >&2
  exit 2
fi

git config --local core.hooksPath .githooks
git config --local user.email "$1@users.noreply.github.com"
git config --local user.useConfigOnly true

echo "Privacy hook enabled and GitHub noreply identity configured."
