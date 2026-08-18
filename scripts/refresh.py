#!/usr/bin/env python3
"""Check the scoreboard's human review schedule. Never fetches or changes evidence."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
METRICS = ROOT / "data" / "scoreboard" / "metrics.json"
REFRESH = ROOT / "data" / "scoreboard" / "refresh.json"


def iso(value: str) -> date:
    return date.fromisoformat(value)


def load() -> tuple[list[dict], dict[str, dict], dict[str, dict]]:
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))["metrics"]
    refresh = json.loads(REFRESH.read_text(encoding="utf-8"))
    policies = {item["metric_id"]: item for item in refresh["policies"]}
    reviews: dict[str, dict] = {}
    for item in refresh["reviews"]:
        reviews[item["metric_id"]] = item
    return metrics, policies, reviews


def check(as_of: date, strict: bool) -> int:
    metrics, policies, reviews = load()
    due = stale = 0
    print(f"Evidence review health as of {as_of.isoformat()}")
    for metric in metrics:
        policy = policies[metric["id"]]
        review = reviews[metric["id"]]
        checked = iso(review["checked_on"])
        due_on = checked + timedelta(days=policy["review_every_days"])
        stale_on = checked + timedelta(days=policy["stale_after_days"])
        state = "stale" if as_of > stale_on else "due" if as_of > due_on else "current"
        due += state == "due"
        stale += state == "stale"
        print(f"{state.upper():7} {metric['id']}: reviewed {checked} · due {due_on} · stale {stale_on} · {review['outcome']}")
        for source in policy["sources"]:
            print(f"         - {source['label']}: {source['url']}")
    print(f"Summary: {len(metrics) - due - stale} current · {due} due · {stale} stale")
    return 1 if strict and stale else 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat(), help="YYYY-MM-DD; defaults to today")
    parser.add_argument("--strict", action="store_true", help="exit nonzero when any review is stale")
    args = parser.parse_args()
    raise SystemExit(check(iso(args.as_of), args.strict))


if __name__ == "__main__":
    main()
