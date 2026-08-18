#!/usr/bin/env python3
"""Pure, stdlib-only rendering and validation for the forecast scoreboard."""

from __future__ import annotations

import html
import json
import math
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable


CORE_STAGES = ("compute", "algorithms", "capability", "automation", "capital", "physical")
STATUS_VALUES = {"pending", "on-track", "ahead", "behind", "falsified", "resolved-true"}
STATUS_ORDER = ("resolved-true", "ahead", "on-track", "behind", "pending", "falsified")
CAMP_VALUES = {"bull", "bear", "base-rate", "model", "wall-street"}
EPISTEMIC_TYPES = {"forecast", "scenario", "model", "trend-projection", "intention", "analysis"}
SCORABILITY_VALUES = {"scored", "context-only"}
MEASUREMENT_RELATIONS = {"direct", "translated", "proxy", "context"}
PROVENANCE_VALUES = {"named-series", "compiled-no-point-link"}
NON_DATABLE_PREFIXES = ("undated", "ongoing", "conditional")
SOURCE_SHORT_NAMES = {
    "aschenbrenner-2024": "Leopold",
    "epoch": "Epoch",
    "ai2027-apr2025": "AI 2027",
    "ai2027-dec2025": "AI Futures",
    "forethought-2025": "Forethought",
    "davidson-2023": "Davidson",
    "morgan-stanley": "Morgan Stanley",
    "altman-2025": "Altman",
    "cotra-2022": "Cotra",
    "erdil-2025": "Erdil",
}
STAGE_COPY = {
    "compute": ("Compute", "How much raw compute exists—and what is actually being trained?"),
    "algorithms": ("Algorithms", "How much more capability are researchers extracting from each FLOP?"),
    "capability": ("Capability", "What can frontier systems actually complete without a human?"),
    "automation": ("Automation", "Is AI beginning to automate the research that improves AI?"),
    "capital": ("Capital", "Is spending converting expectations into new capacity?"),
    "physical": ("Physical", "Can chips, power, and construction keep up with the plans?"),
}

CHART_W = 840
CHART_H = 372
PAD_L = 76
PAD_R = 30
PAD_T = 58
PAD_B = 56


class SchemaError(ValueError):
    """Raised when a scoreboard JSON file violates the supported schema."""


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def slug(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")


def require(condition: bool, path: str, message: str) -> None:
    if not condition:
        raise SchemaError(f"{path}: {message}")


def require_keys(obj: dict[str, Any], keys: Iterable[str], path: str) -> None:
    missing = [key for key in keys if key not in obj]
    require(not missing, path, f"missing required field(s): {', '.join(missing)}")


def validate_observation_provenance(point: dict[str, Any], path: str, *, production: bool) -> None:
    """Each production observation is either directly cited or explicitly classified as debt.

    A metric-wide canonical link is not a substitute for evidence for a plotted point.
    """
    if not production:
        return
    require(point.get("provenance") in PROVENANCE_VALUES, f"{path}.provenance", f"must be one of {sorted(PROVENANCE_VALUES)}")
    has_label = bool(point.get("source_label"))
    has_url = bool(point.get("source_url"))
    require(has_label == has_url, path, "source_label and source_url must appear together")
    if has_url:
        require(
            isinstance(point["source_url"], str) and re.match(r"^https?://", point["source_url"]) is not None,
            f"{path}.source_url",
            "must be an http(s) URL",
        )
        require(point.get("provenance") == "named-series", f"{path}.provenance", "must be named-series when a direct point link is supplied")
        return
    require(point.get("provenance") == "compiled-no-point-link", f"{path}.provenance", "must be compiled-no-point-link without a direct point link")
    require(
        isinstance(point.get("provenance_gap_reason"), str) and point["provenance_gap_reason"].strip(),
        f"{path}.provenance_gap_reason",
        "is required when no direct point link is available",
    )


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SchemaError(f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    require(isinstance(value, dict), str(path), "top level must be an object")
    return value


def choose_data_file(data_dir: Path, stem: str) -> tuple[Path, bool]:
    production = data_dir / f"{stem}.json"
    if production.exists():
        return production, True
    seed = data_dir / f"{stem}.seed.json"
    require(seed.exists(), str(seed), f"missing both {stem}.json and {stem}.seed.json")
    return seed, False


def validate_metrics(data: dict[str, Any], *, production: bool) -> None:
    require_keys(data, ("schema_version", "stages", "metrics"), "metrics")
    require(isinstance(data["schema_version"], str), "metrics.schema_version", "must be a string")
    require(isinstance(data["stages"], list), "metrics.stages", "must be an array")
    require(isinstance(data["metrics"], list), "metrics.metrics", "must be an array")

    stage_ids: set[str] = set()
    for index, stage in enumerate(data["stages"]):
        path = f"metrics.stages[{index}]"
        require(isinstance(stage, dict), path, "must be an object")
        require_keys(stage, ("id", "label", "order"), path)
        require(isinstance(stage["id"], str) and stage["id"], f"{path}.id", "must be a non-empty string")
        require(stage["id"] not in stage_ids, f"{path}.id", "must be unique")
        require(isinstance(stage["order"], int), f"{path}.order", "must be an integer")
        stage_ids.add(stage["id"])

    metric_ids: set[str] = set()
    for index, metric in enumerate(data["metrics"]):
        path = f"metrics.metrics[{index}]"
        require(isinstance(metric, dict), path, "must be an object")
        require_keys(metric, ("id", "stage", "tier"), path)
        require(isinstance(metric["id"], str) and metric["id"], f"{path}.id", "must be a non-empty string")
        require(metric["id"] not in metric_ids, f"{path}.id", "must be unique")
        require(metric["stage"] in stage_ids, f"{path}.stage", "must reference metrics.stages")
        # Only two shapes render: Tier-1 on a core stage (headline card) and Tier-2
        # (supporting card). Anything else would be dropped from the page while its
        # claims still counted in the tally, so it fails the build instead.
        require(metric["tier"] in (1, 2), f"{path}.tier", "must be 1 or 2 — no renderer exists for tier 3")
        if metric["tier"] == 1:
            require(
                metric["stage"] in CORE_STAGES,
                f"{path}.stage",
                f"a Tier-1 metric must sit on a core stage {CORE_STAGES} or it would render nowhere",
            )
        metric_ids.add(metric["id"])

        if production:
            require_keys(
                metric,
                ("name", "what_it_measures", "source", "source_cadence", "measurement_notes", "last_checked"),
                path,
            )
        if "source" in metric:
            require(isinstance(metric["source"], dict), f"{path}.source", "must be an object")
            require_keys(metric["source"], ("name", "url"), f"{path}.source")
            require(
                isinstance(metric["source"]["url"], str)
                and re.match(r"^https?://", metric["source"]["url"]) is not None,
                f"{path}.source.url",
                "must be an http(s) URL",
            )
        if "verdict" in metric:
            require(isinstance(metric["verdict"], str), f"{path}.verdict", "must be a string")
            require(len(metric["verdict"]) <= 80, f"{path}.verdict", "must be 80 characters or fewer")
        if "why_it_matters" in metric:
            require(isinstance(metric["why_it_matters"], str), f"{path}.why_it_matters", "must be a string")
            require(len(metric["why_it_matters"]) <= 500, f"{path}.why_it_matters", "must be 500 characters or fewer")
        if "current" in metric:
            require(isinstance(metric["current"], dict), f"{path}.current", "must be an object")
            require_keys(metric["current"], ("value", "display", "as_of", "confidence"), f"{path}.current")
            validate_observation_provenance(metric["current"], f"{path}.current", production=production)
            if len(str(metric["current"]["display"])) > 60:
                print(
                    f"WARNING: {path}.current.display exceeds 60 characters",
                    file=sys.stderr,
                )
        if "axis_unit" in metric:
            require(isinstance(metric["axis_unit"], str), f"{path}.axis_unit", "must be a string")
        if "series" in metric:
            require(isinstance(metric["series"], list), f"{path}.series", "must be an array")
            for s_i, extra in enumerate(metric["series"]):
                s_path = f"{path}.series[{s_i}]"
                require(isinstance(extra, dict), s_path, "must be an object")
                require_keys(extra, ("key", "label", "points"), s_path)
                require(isinstance(extra["points"], list) and extra["points"], f"{s_path}.points", "must be a non-empty array")
                for p_i, pt in enumerate(extra["points"]):
                    p_path = f"{s_path}.points[{p_i}]"
                    require(isinstance(pt, dict), p_path, "must be an object")
                    require_keys(pt, ("date", "value"), p_path)
                    validate_observation_provenance(pt, p_path, production=production)
                    require(decimal_date(pt.get("date")) is not None, f"{p_path}.date", "must be a parseable date")
                    require(
                        isinstance(pt["value"], (int, float)) and not isinstance(pt["value"], bool),
                        f"{p_path}.value", "must be numeric, in the metric's own unit",
                    )
                    if "promised" in pt:
                        require(decimal_date(pt.get("promised")) is not None, f"{p_path}.promised", "must be a parseable date")
        if "history" in metric:
            require(isinstance(metric["history"], list), f"{path}.history", "must be an array")
            previous: float | None = None
            for h_index, point in enumerate(metric["history"]):
                h_path = f"{path}.history[{h_index}]"
                require(isinstance(point, dict), h_path, "must be an object")
                require_keys(point, ("date", "value"), h_path)
                validate_observation_provenance(point, h_path, production=production)
                require(isinstance(point["value"], (int, float)) and not isinstance(point["value"], bool), f"{h_path}.value", "must be numeric")
                # An unreadable date used to be dropped from the chart in silence while
                # the caption still counted it. Fail the build instead.
                when = decimal_date(point["date"])
                require(
                    when is not None,
                    f"{h_path}.date",
                    "must be YYYY, YYYY-MM, or YYYY-Q1..Q4 so the point can be plotted",
                )
                require(previous is None or when >= previous, f"{h_path}.date", "history must be oldest first")
                previous = when

    for stage in CORE_STAGES:
        candidates = [m for m in data["metrics"] if m.get("stage") == stage and m.get("tier") == 1]
        require(len(candidates) == 1, "metrics.metrics", f"must contain exactly one Tier-1 metric for core stage '{stage}'")


def camp_key(value: Any) -> str:
    normalized = slug(value)
    if normalized.startswith("bull"):
        return "bull"
    for camp in CAMP_VALUES:
        if normalized == camp:
            return camp
    return normalized


def validate_claims(data: dict[str, Any], metric_ids: set[str], *, production: bool) -> None:
    require_keys(data, ("schema_version", "milestone_ladder", "forecast_sources", "claims"), "claims")
    require(isinstance(data["forecast_sources"], list), "claims.forecast_sources", "must be an array")
    require(isinstance(data["claims"], list), "claims.claims", "must be an array")
    ladder = data["milestone_ladder"]
    require(isinstance(ladder, dict), "claims.milestone_ladder", "must be an object")
    require(isinstance(ladder.get("rungs"), list), "claims.milestone_ladder.rungs", "must be an array")

    rung_ids: set[str] = set()
    for index, rung in enumerate(ladder["rungs"]):
        path = f"claims.milestone_ladder.rungs[{index}]"
        require(isinstance(rung, dict), path, "must be an object")
        require_keys(rung, ("id", "label", "measurable_via"), path)
        require(rung["id"] not in rung_ids, f"{path}.id", "must be unique")
        rung_ids.add(rung["id"])

    source_ids: set[str] = set()
    for index, source in enumerate(data["forecast_sources"]):
        path = f"claims.forecast_sources[{index}]"
        require(isinstance(source, dict), path, "must be an object")
        require_keys(source, ("id", "author", "work", "published", "camp", "url", "epistemic_type"), path)
        require(source["id"] not in source_ids, f"{path}.id", "must be unique")
        require(camp_key(source["camp"]) in CAMP_VALUES, f"{path}.camp", f"must map to one of {sorted(CAMP_VALUES)}")
        require(source["epistemic_type"] in EPISTEMIC_TYPES, f"{path}.epistemic_type", f"must be one of {sorted(EPISTEMIC_TYPES)}")
        require(isinstance(source["url"], str) and re.match(r"^https?://", source["url"]) is not None, f"{path}.url", "must be an http(s) URL")
        source_ids.add(source["id"])

    claim_ids: set[str] = set()
    for index, claim in enumerate(data["claims"]):
        path = f"claims.claims[{index}]"
        require(isinstance(claim, dict), path, "must be an object")
        require_keys(
            claim,
            ("id", "source", "metric_id", "claim_type", "scorability", "measurement_relation", "quote", "quote_location", "conditionality", "predicted", "resolution_history"),
            path,
        )
        require(claim["id"] not in claim_ids, f"{path}.id", "must be unique")
        require(claim["source"] in source_ids, f"{path}.source", "must reference forecast_sources")
        require(claim["metric_id"] in metric_ids, f"{path}.metric_id", "must reference metrics")
        require(claim["claim_type"] in ("trajectory", "milestone"), f"{path}.claim_type", "must be trajectory or milestone")
        require(claim["scorability"] in SCORABILITY_VALUES, f"{path}.scorability", f"must be one of {sorted(SCORABILITY_VALUES)}")
        relation = claim["measurement_relation"]
        require(isinstance(relation, dict), f"{path}.measurement_relation", "must be an object")
        require_keys(relation, ("type", "note"), f"{path}.measurement_relation")
        require(relation["type"] in MEASUREMENT_RELATIONS, f"{path}.measurement_relation.type", f"must be one of {sorted(MEASUREMENT_RELATIONS)}")
        require(isinstance(relation["note"], str) and relation["note"].strip(), f"{path}.measurement_relation.note", "must be non-empty")
        require((claim["scorability"] == "context-only") == (relation["type"] == "context"), f"{path}.measurement_relation.type", "context relation must match context-only scorability")
        if relation["type"] == "translated":
            require(isinstance(relation.get("formula"), str) and relation["formula"].strip(), f"{path}.measurement_relation.formula", "translated claims require a conversion formula")
        require(isinstance(claim["quote"], str) and claim["quote"].strip(), f"{path}.quote", "must be non-empty")
        require(isinstance(claim["conditionality"], str) and claim["conditionality"].strip(), f"{path}.conditionality", "must be non-empty")
        require(isinstance(claim["predicted"], dict), f"{path}.predicted", "must be an object")
        require_keys(claim["predicted"], ("value", "by"), f"{path}.predicted")
        # A date the parser cannot read used to degrade silently: the claim was
        # reported to the reader as having "no fixed date" while its own chip printed
        # the date. Either the parser reads it, or the claim says plainly it has none.
        by_text = str(claim["predicted"]["by"]).strip()
        require(
            date_range(by_text) is not None or by_text.lower().startswith(NON_DATABLE_PREFIXES),
            f"{path}.predicted.by",
            "must parse as a date/range (YYYY, YYYY-MM, YYYY-Q1..Q4, or a range of those) "
            f"or start with one of {NON_DATABLE_PREFIXES} to declare itself undated",
        )
        if "plot_value" in claim["predicted"]:
            require(
                isinstance(claim["predicted"]["plot_value"], (int, float))
                and not isinstance(claim["predicted"]["plot_value"], bool),
                f"{path}.predicted.plot_value",
                "must be numeric, expressed in the metric's own unit",
            )
        if "plot_note" in claim["predicted"]:
            require(isinstance(claim["predicted"]["plot_note"], str), f"{path}.predicted.plot_note", "must be a string")
        if "ladder_rung" in claim:
            require(claim["ladder_rung"] in rung_ids, f"{path}.ladder_rung", "must reference milestone_ladder.rungs")

        history = claim["resolution_history"]
        require(isinstance(history, list) and history, f"{path}.resolution_history", "must be a non-empty array")
        previous_resolution_date: float | None = None
        for r_index, resolution in enumerate(history):
            r_path = f"{path}.resolution_history[{r_index}]"
            require(isinstance(resolution, dict), r_path, "must be an object")
            require_keys(resolution, ("status", "confidence", "as_of", "evidence", "evidence_urls", "provenance_scope", "assessment_basis", "counterargument"), r_path)
            require(resolution["status"] in STATUS_VALUES, f"{r_path}.status", f"must be one of {sorted(STATUS_VALUES)}")
            resolution_date = decimal_date(resolution["as_of"])
            require(resolution_date is not None, f"{r_path}.as_of", "must be YYYY, YYYY-MM, or YYYY-Q1..Q4")
            require(previous_resolution_date is None or resolution_date >= previous_resolution_date, f"{r_path}.as_of", "resolution history must be oldest first")
            previous_resolution_date = resolution_date
            confidence = resolution["confidence"]
            require(isinstance(confidence, (int, float)) and not isinstance(confidence, bool), f"{r_path}.confidence", "must be numeric")
            require(0 <= confidence <= 100, f"{r_path}.confidence", "must be between 0 and 100")
            require(isinstance(resolution["counterargument"], str) and resolution["counterargument"].strip(), f"{r_path}.counterargument", "must be non-empty")
            evidence_urls = resolution["evidence_urls"]
            require(isinstance(evidence_urls, list) and evidence_urls, f"{r_path}.evidence_urls", "must be a non-empty array")
            for url_index, url in enumerate(evidence_urls):
                require(isinstance(url, str) and re.match(r"^https?://", url) is not None, f"{r_path}.evidence_urls[{url_index}]", "must be an http(s) URL")
            basis = resolution["assessment_basis"]
            require(isinstance(basis, dict), f"{r_path}.assessment_basis", "must be an object")
            require_keys(basis, ("test_type", "target", "deadline", "observation_metric_id", "measurement_relation", "comparison_rule", "uncertainty_drivers"), f"{r_path}.assessment_basis")
            require(basis["observation_metric_id"] == claim["metric_id"], f"{r_path}.assessment_basis.observation_metric_id", "must match the claim metric")
            require(basis["measurement_relation"] == relation["type"], f"{r_path}.assessment_basis.measurement_relation", "must match the claim relation")
            require(isinstance(basis["uncertainty_drivers"], list) and basis["uncertainty_drivers"], f"{r_path}.assessment_basis.uncertainty_drivers", "must be a non-empty array")
            if production:
                require(isinstance(resolution["evidence"], str) and resolution["evidence"].strip(), f"{r_path}.evidence", "must be non-empty")
        claim_ids.add(claim["id"])

    if "forecast_drift" in data:
        drift = data["forecast_drift"]
        require(isinstance(drift, list), "claims.forecast_drift", "must be an array")
        for s_index, series in enumerate(drift):
            s_path = f"claims.forecast_drift[{s_index}]"
            require(isinstance(series, dict), s_path, "must be an object")
            require_keys(series, ("source", "observations"), s_path)
            require(isinstance(series["observations"], list), f"{s_path}.observations", "must be an array")
            milestones: set[str] = set()
            for o_index, observation in enumerate(series["observations"]):
                o_path = f"{s_path}.observations[{o_index}]"
                require(isinstance(observation, dict), o_path, "must be an object")
                require_keys(observation, ("as_of", "median_year"), o_path)
                require(isinstance(observation["median_year"], (int, float)), f"{o_path}.median_year", "must be numeric")
                if "milestone" in observation:
                    require(isinstance(observation["milestone"], str), f"{o_path}.milestone", "must be a string")
                    milestones.add(observation["milestone"])
            # A drift line is only drift if every point measures the same milestone;
            # otherwise a change of definition renders as a change of belief.
            require(
                len(milestones) <= 1,
                f"{s_path}.observations",
                f"all observations in one series must name the same milestone, found {sorted(milestones)} — "
                "split the series instead",
            )


def validate_refresh(data: dict[str, Any], metrics: dict[str, Any]) -> None:
    require_keys(data, ("schema_version", "policies", "reviews"), "refresh")
    metric_ids = {metric["id"] for metric in metrics["metrics"]}
    policies: dict[str, dict[str, Any]] = {}
    for index, policy in enumerate(data["policies"]):
        path = f"refresh.policies[{index}]"
        require_keys(policy, ("metric_id", "review_every_days", "stale_after_days", "sources"), path)
        require(policy["metric_id"] in metric_ids, f"{path}.metric_id", "must reference a metric")
        require(policy["metric_id"] not in policies, f"{path}.metric_id", "must be unique")
        require(isinstance(policy["review_every_days"], int) and policy["review_every_days"] > 0, f"{path}.review_every_days", "must be a positive integer")
        require(isinstance(policy["stale_after_days"], int) and policy["stale_after_days"] >= policy["review_every_days"], f"{path}.stale_after_days", "must be at least review_every_days")
        require(isinstance(policy["sources"], list) and policy["sources"], f"{path}.sources", "must be a non-empty array")
        for s_index, source in enumerate(policy["sources"]):
            s_path = f"{path}.sources[{s_index}]"
            require_keys(source, ("label", "url"), s_path)
            require(re.match(r"^https?://", source["url"]) is not None, f"{s_path}.url", "must be an http(s) URL")
        policies[policy["metric_id"]] = policy
    require(set(policies) == metric_ids, "refresh.policies", "must contain exactly one policy for every metric")

    latest: dict[str, str] = {}
    previous: dict[str, float] = {}
    for index, review in enumerate(data["reviews"]):
        path = f"refresh.reviews[{index}]"
        require_keys(review, ("metric_id", "checked_on", "outcome", "note"), path)
        require(review["metric_id"] in metric_ids, f"{path}.metric_id", "must reference a metric")
        try:
            parsed_date = date.fromisoformat(review["checked_on"])
        except (TypeError, ValueError):
            parsed_date = None
        require(parsed_date is not None, f"{path}.checked_on", "must be an ISO date")
        when = float(parsed_date.toordinal()) if parsed_date else 0.0
        require(review["outcome"] in {"baseline", "no-change", "updated", "source-lag", "access-blocked"}, f"{path}.outcome", "has an unsupported outcome")
        require(review["metric_id"] not in previous or when >= previous[review["metric_id"]], path, "reviews for each metric must be oldest first")
        previous[review["metric_id"]] = when
        latest[review["metric_id"]] = review["checked_on"]
    require(set(latest) == metric_ids, "refresh.reviews", "must contain at least one review for every metric")
    for metric in metrics["metrics"]:
        require(latest[metric["id"]] == metric.get("last_checked"), f"metrics.{metric['id']}.last_checked", "must equal the latest append-only review date")


def validate_cruxes(data: dict[str, Any], metric_ids: set[str]) -> None:
    require_keys(data, ("cruxes",), "cruxes")
    require(isinstance(data["cruxes"], list), "cruxes.cruxes", "must be an array")
    ids: set[str] = set()
    for index, crux in enumerate(data["cruxes"]):
        path = f"cruxes.cruxes[{index}]"
        require_keys(crux, ("id", "title", "question", "pole_a", "pole_b", "position", "summary", "spread", "evidence", "movers", "related_metric_ids", "last_updated"), path)
        require(crux["id"] not in ids, f"{path}.id", "must be unique")
        ids.add(crux["id"])
        for pole in ("pole_a", "pole_b"):
            require_keys(crux[pole], ("label", "desc"), f"{path}.{pole}")
        require(
            isinstance(crux["position"], (int, float)) and not isinstance(crux["position"], bool) and -1 <= crux["position"] <= 1,
            f"{path}.position",
            "must be a number from -1 (Pole A) to 1 (Pole B)",
        )
        require(crux["spread"] in {"low", "medium", "high"}, f"{path}.spread", "must be low, medium, or high")
        require(isinstance(crux["related_metric_ids"], list), f"{path}.related_metric_ids", "must be an array")
        for metric_id in crux["related_metric_ids"]:
            require(metric_id in metric_ids, f"{path}.related_metric_ids", "must reference known metrics")
        for e_index, item in enumerate(crux["evidence"]):
            e_path = f"{path}.evidence[{e_index}]"
            require_keys(item, ("finding", "direction", "date", "source_label", "source_url"), e_path)
            require(isinstance(item["source_url"], str) and re.match(r"^https?://", item["source_url"]) is not None, f"{e_path}.source_url", "must be an http(s) URL")
        try:
            date.fromisoformat(crux["last_updated"])
            valid_updated = True
        except (TypeError, ValueError):
            valid_updated = False
        require(valid_updated, f"{path}.last_updated", "must be an ISO date")
        require(isinstance(crux["evidence"], list) and crux["evidence"], f"{path}.evidence", "must be non-empty")
        require(isinstance(crux["movers"], list) and crux["movers"], f"{path}.movers", "must be non-empty")


def load_scoreboard(data_dir: Path, root_data_dir: Path | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, str]]:
    metrics_path, metrics_production = choose_data_file(data_dir, "metrics")
    claims_path, claims_production = choose_data_file(data_dir, "claims")
    metrics = read_json(metrics_path)
    claims = read_json(claims_path)
    validate_metrics(metrics, production=metrics_production)
    metric_ids = {metric["id"] for metric in metrics["metrics"]}
    validate_claims(claims, metric_ids, production=claims_production)
    root_data_dir = root_data_dir or data_dir.parent
    refresh_path = data_dir / "refresh.json"
    cruxes_path = root_data_dir / "cruxes.json"
    refresh = read_json(refresh_path)
    cruxes = read_json(cruxes_path)
    validate_refresh(refresh, metrics)
    validate_cruxes(cruxes, metric_ids)
    return metrics, claims, refresh, cruxes, {"metrics": metrics_path.name, "claims": claims_path.name, "refresh": refresh_path.name, "cruxes": cruxes_path.name}


def source_link(source: Any) -> str:
    if not isinstance(source, dict):
        return '<span class="muted">Source not yet populated</span>'
    name = esc(source.get("name", "Source"))
    url = source.get("url")
    if not url:
        return name
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{name}<span aria-hidden="true"> ↗</span></a>'


def source_map(claims_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {source["id"]: source for source in claims_data["forecast_sources"]}


def source_short(source: dict[str, Any]) -> str:
    return SOURCE_SHORT_NAMES.get(str(source.get("id")), str(source.get("author", "Forecast")))


def source_icon(source: Any) -> str:
    if not isinstance(source, dict) or not source.get("url"):
        return ""
    return (
        f'<a class="source-icon" href="{esc(source["url"])}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="Open canonical source for {esc(source.get("name", "this metric"))}">↗</a>'
    )


def confidence_number(value: Any) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def status_badge(status: Any) -> str:
    value = str(status)
    return f'<span class="status-badge status-{slug(value)}">{esc(value)}</span>'


def current_resolution(claim: dict[str, Any]) -> dict[str, Any]:
    """The latest append-only resolution is the only one used for current status."""
    history = claim.get("resolution_history", [])
    if not history:
        raise SchemaError(f"claim {claim.get('id', '<unknown>')} has no resolution history")
    return history[-1]


def is_headline_claim(claim: dict[str, Any]) -> bool:
    """Only like-for-like or explicitly translated claims belong in aggregate status reads."""
    relation = (claim.get("measurement_relation") or {}).get("type")
    return claim.get("scorability") == "scored" and relation in {"direct", "translated"}


def cadence_clause(value: Any) -> str:
    clause = re.split(r"\s*(?:—|;)\s*", str(value or "not yet populated"), maxsplit=1)[0]
    if clause.count("(") > clause.count(")"):   # never cut inside a parenthetical
        clause = str(value or "").split("(")[0].strip() or clause
    return clause


QUARTER_MONTHS = {"1": (1, 3), "2": (4, 6), "3": (7, 9), "4": (10, 12)}
DATE_PATTERN = re.compile(r"\d{4}(?:-(?:\d{2}|Q[1-4]))?")


def date_month(value: Any) -> int | None:
    text = str(value).strip()
    quarter = re.match(r"^(\d{4})-Q([1-4])", text)
    if quarter:
        # A quarter's observation is as recent as the quarter's last month.
        return int(quarter.group(1)) * 12 + QUARTER_MONTHS[quarter.group(2)][1]
    match = re.match(r"^(\d{4})-(\d{2})", text)
    if not match:
        return None
    year, month = int(match.group(1)), int(match.group(2))
    if not 1 <= month <= 12:
        return None
    return year * 12 + month


def vintage_tag(metric: dict[str, Any]) -> str:
    """The headline reading's own date, always visible. Two cases get a highlighted
    tag: an estimate more than a year old, and a headline that is not the newest
    point on its own chart (a frontier maximum). Both used to be legible only by
    opening the collapsed source note."""
    current = metric.get("current")
    if not isinstance(current, dict) or not current.get("as_of"):
        return ""
    as_of = str(current["as_of"])
    observed = date_month(as_of)
    checked = date_month(metric.get("last_checked"))
    if observed is not None and checked is not None and checked - observed > 12:
        return f'<span class="vintage-tag">Vintage {esc(as_of)}</span>'
    newest = ""
    for point in metric.get("history", []) or []:
        candidate = str(point.get("date", ""))
        if date_month(candidate) is not None and (not newest or date_month(candidate) > date_month(newest)):
            newest = candidate
    if observed is not None and newest and date_month(newest) > observed:
        return f'<span class="vintage-tag">as of {esc(as_of)} · series runs to {esc(newest)}</span>'
    return f'<span class="confidence-tag">as of {esc(as_of)}</span>'


def decimal_date(value: Any, *, end: bool = False) -> float | None:
    """Accepts YYYY, YYYY-MM and YYYY-Q1..Q4. Quarters are a format the dataset
    genuinely uses (capex reporting), so the parser must read them rather than
    silently bucketing a dated claim as undated."""
    text = str(value).strip()
    quarter = re.fullmatch(r"(\d{4})-Q([1-4])", text)
    if quarter:
        first, last = QUARTER_MONTHS[quarter.group(2)]
        return int(quarter.group(1)) + ((last if end else first) - 1) / 12
    match = re.fullmatch(r"(\d{4})(?:-(\d{2}))?", text)
    if not match:
        return None
    year = int(match.group(1))
    month = int(match.group(2) or (12 if end else 1))
    if not 1 <= month <= 12:
        return None
    return year + (month - 1) / 12


def date_range(value: Any) -> tuple[float, float] | None:
    text = str(value).strip()
    year_range = re.fullmatch(r"(\d{4})\s*[-–—/]\s*(\d{4})", text)
    if year_range:
        start = decimal_date(year_range.group(1))
        finish = decimal_date(year_range.group(2), end=True)
        if start is not None and finish is not None:
            return start, finish
    single = decimal_date(text)
    if single is not None:
        end = decimal_date(text, end=True)
        return single, end if end is not None else single
    match = re.fullmatch(rf"({DATE_PATTERN.pattern})\s*(?:–|—|to|/)\s*({DATE_PATTERN.pattern})", text)
    if match:
        start = decimal_date(match.group(1))
        finish = decimal_date(match.group(2), end=True)
        if start is not None and finish is not None:
            return start, finish
    return None


def claim_plot_number(claim: dict[str, Any], unit: str) -> tuple[float | None, str | None]:
    """A claim plots at a y-position ONLY when a human has recorded plot_value in the
    metric's own unit. Rate claims, milestone claims, and claims about a different
    quantity than the axis measures deliberately have none — they render in the
    non-positional lane rather than at a meaningless height."""
    predicted = claim.get("predicted", {})
    raw = predicted.get("plot_value")
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return float(raw), predicted.get("plot_note")
    # No text-parsing fallback: a height inferred from prose is exactly the
    # rendering fallback docs/decisions.md Weakness 3 forbids.
    return None, None


def format_value(value: float) -> str:
    if value >= 1_000_000_000_000_000:
        exponent = math.floor(math.log10(value))
        return f"{value / 10 ** exponent:g}e{exponent}"
    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:g}T"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:g}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:g}M"
    if value >= 1_000:
        return f"{value / 1_000:g}k"
    return f"{value:g}"


def is_integral(values: Iterable[float]) -> bool:
    """A count metric ('binding regimes in force') cannot take a half value, so its
    axis must not be labelled at half-unit resolution."""
    materialised = list(values)
    return bool(materialised) and all(float(value).is_integer() for value in materialised)


def value_ticks(values: list[float], *, logarithmic: bool, integral: bool = False) -> list[float]:
    low = min(values)
    high = max(values)
    if logarithmic:
        lower_power = math.floor(math.log10(low))
        upper_power = math.ceil(math.log10(high))
        ticks = [10.0**power for power in range(lower_power, upper_power + 1)]
        if low < 1 and low not in ticks:
            ticks.insert(0, low)
        return sorted(set(ticks))
    if math.isclose(low, high):
        return [low]
    raw_step = (high - low) / 4
    magnitude = 10.0 ** math.floor(math.log10(raw_step)) if raw_step > 0 else 1.0
    step = next((magnitude * m for m in (1, 2, 2.5, 5, 10) if magnitude * m >= raw_step), magnitude * 10)
    if integral:
        step = float(max(1, math.ceil(step - 1e-9)))
    start = math.ceil(low / step) * step
    ticks = []
    value = start
    while value <= high + step * 0.01:
        ticks.append(round(value, 10))
        value += step
    return ticks or [low, high]


def time_ticks(x_min: float, x_max: float) -> list[tuple[float, str]]:
    """Year ticks where the span crosses at least two Januaries; month ticks where it
    does not. A series living inside one calendar year used to render with no x axis
    at all, leaving every point unlocatable in time."""
    first_year = math.ceil(x_min)
    last_year = math.floor(x_max)
    step = max(1, math.ceil(max(1, last_year - first_year) / 6))
    years = list(range(first_year, last_year + 1, step))
    if len(years) >= 2:
        return [(float(year), str(year)) for year in years]

    def month_label(months: int) -> str:
        year, month = divmod(months, 12)
        return f"{year}-{month + 1:02d}"

    start = math.ceil(x_min * 12 - 1e-9)
    finish = math.floor(x_max * 12 + 1e-9)
    if finish > start:
        month_step = max(1, math.ceil((finish - start + 1) / 6))
        ticks = [(months / 12, month_label(months)) for months in range(start, finish + 1, month_step)]
        if len(ticks) >= 2:
            return ticks
    return [
        (x_min, month_label(round(x_min * 12))),
        (x_max, month_label(round(x_max * 12))),
    ]


def observation_evidence(point: dict[str, Any], *, announcement: bool = False) -> str:
    """Never turn a metric-wide source into a point citation by implication."""
    if point.get("source_url") and point.get("source_label"):
        label = "Announcement source" if announcement else point["source_label"]
        return f'<a href="{esc(point["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(label)} ↗</a>'
    reason = point.get("provenance_gap_reason")
    if reason:
        category = str(reason).split(":", 1)[0].replace("-", " ")
        return f'<span class="provenance-gap" title="{esc(reason)}">Provenance gap: {esc(category)}</span>'
    return '<span class="provenance-gap">Compiled; no direct point link</span>'


def latest_observation(metric: dict[str, Any]) -> str:
    history = metric.get("history", []) or []
    if not history:
        return ""
    dated = [(decimal_date(point.get("date")), index, point) for index, point in enumerate(history)]
    available = [item for item in dated if item[0] is not None]
    if not available:
        return ""
    _when, _index, point = max(available, key=lambda item: (item[0], item[1]))
    note = point.get("note") or f'value {point.get("value")}'
    return f'<p class="latest-observation"><span>Latest recorded observation</span><strong>{esc(point.get("date"))} · {esc(note)}</strong>{observation_evidence(point)}</p>'


def chart_data_table(
    metric: dict[str, Any],
    claims: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
) -> str:
    """Keyboard-accessible counterpart to the plotted marks and hover titles."""
    rows = []
    for point in metric.get("history", []):
        note = f' · {esc(point["note"])}' if point.get("note") else ""
        rows.append(
            f'<tr><td>Reality</td><td>{esc(point.get("date"))}</td><td>{esc(point.get("value"))}{note}</td><td>Measured</td><td>{observation_evidence(point)}</td></tr>'
        )
    for series in metric.get("series", []):
        for point in series.get("points", []):
            promised = f' · promised {esc(point["promised"])}' if point.get("promised") else ""
            note = f' · {esc(point["note"])}' if point.get("note") else ""
            rows.append(
                f'<tr><td>{esc(series.get("label", "Additional series"))}</td><td>{esc(point.get("date"))}</td>'
                f'<td>{esc(point.get("value"))}{promised}{note}</td><td>{"Cancelled" if point.get("cancelled") else "Announced"}</td><td>{observation_evidence(point, announcement=True)}</td></tr>'
            )
    for claim in claims:
        source = sources[claim["source"]]
        resolution = current_resolution(claim)
        rows.append(
            f'<tr><td>{esc(source_short(source))}</td><td>{esc(claim["predicted"].get("by"))}</td>'
            f'<td>{esc(claim["predicted"].get("value"))}</td><td>{esc(resolution["status"])} · confidence {esc(confidence_number(resolution["confidence"]))}</td><td><a href="{esc(source["url"])}" target="_blank" rel="noopener noreferrer">Published claim ↗</a></td></tr>'
        )
    if not rows:
        return ""
    return f"""
      <details class="chart-data">
        <summary>View chart as data</summary>
        <div><table><thead><tr><th>Series</th><th>Date / deadline</th><th>Observation / target</th><th>State</th><th>Evidence</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
      </details>
    """


def milestone_timeline(
    metric: dict[str, Any],
    dated: list[tuple[dict[str, Any], tuple[float, float]]],
    sources: dict[str, dict[str, Any]],
    stats: dict[str, Any] | None = None,
) -> str:
    """Some forces (AI R&D automation) have no numeric series at all — only dated
    milestones. Rendering them on an empty numeric grid produced an axis-less chart
    with no plot points; this renders what actually exists: dates and resolution states."""
    width, height = CHART_W, 96 + 34 * len(dated)
    pad_l, pad_r, top = 150, 40, 54
    x_values = [value for _claim, pair in dated for value in pair]
    x_min, x_max = min(x_values), max(x_values)
    if math.isclose(x_min, x_max):
        x_min -= 0.5
        x_max += 0.5
    margin = max((x_max - x_min) * 0.06, 0.1)
    x_min -= margin
    x_max += margin

    def x_pos(value: float) -> float:
        return pad_l + (value - x_min) / (x_max - x_min) * (width - pad_l - pad_r)

    parts = [f'<text x="{pad_l}" y="24" class="chart-overline">DATED MILESTONES &middot; NO NUMERIC SERIES</text>']
    baseline = height - 30
    for position, label in time_ticks(x_min, x_max):
        x = x_pos(position)
        parts.append(f'<line x1="{x:.1f}" y1="{top - 14:.1f}" x2="{x:.1f}" y2="{baseline}" class="chart-grid vertical"/>')
        parts.append(f'<text x="{x:.1f}" y="{baseline + 22}" text-anchor="middle" class="axis-label">{esc(label)}</text>')
    parts.append(f'<line x1="{pad_l}" y1="{baseline}" x2="{width - pad_r}" y2="{baseline}" class="chart-axis"/>')

    for index, (claim, (start, finish)) in enumerate(sorted(dated, key=lambda item: item[1][0])):
        source = sources[claim["source"]]
        camp = camp_key(source["camp"])
        status = current_resolution(claim)["status"]
        y = top + index * 34
        sx, fx = x_pos(start), x_pos(finish)
        tooltip = f'{source_short(source)}: {claim["predicted"].get("value")} by {claim["predicted"].get("by")} — {status}'
        parts.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width - pad_r}" y2="{y:.1f}" class="chart-grid"/>')
        if not math.isclose(sx, fx):
            parts.append(f'<line x1="{sx:.1f}" y1="{y:.1f}" x2="{fx:.1f}" y2="{y:.1f}" class="forecast-range camp-{camp}"/>')
        parts.append(
            f'<polygon points="{sx:.1f},{y - 7:.1f} {sx + 7:.1f},{y:.1f} {sx:.1f},{y + 7:.1f} {sx - 7:.1f},{y:.1f}" '
            f'class="forecast-dot camp-{camp}" role="img" aria-label="{esc(tooltip)}"><title>{esc(tooltip)}</title></polygon>'
        )
        parts.append(f'<text x="{pad_l - 14}" y="{y + 4:.1f}" text-anchor="end" class="timeline-source">{esc(source_short(source))}</text>')
        parts.append(f'<text x="{fx + 14:.1f}" y="{y + 4:.1f}" class="timeline-status status-text-{slug(status)}">{esc(status)}</text>')

    drawn = len(dated)
    if stats is not None:
        stats.update(
            mode="milestones",
            reality_recorded=len(metric.get("history", [])),
            reality_drawn=0,
            marks_drawn=drawn,
        )
    aria = (
        f"{drawn} dated milestone marker{'s' if drawn != 1 else ''} for "
        f"{metric.get('name', metric['id'])}; no numeric series exists for this force."
    )
    return f"""
      <div class="chart-scroll" tabindex="0" role="group" aria-label="{esc('Milestone timeline for ' + str(metric.get('name', metric['id'])) + ' (scrollable)')}">
        <svg class="forecast-chart" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(aria)}">
          {''.join(parts)}
        </svg>
      </div>
      <details class="chart-explanation"><summary>How to read this chart</summary><p class="chart-note">{drawn} dated milestone{'s' if drawn != 1 else ''} drawn. This force has no numeric series — vertical position is ordering, not a value.</p></details>
      {chart_data_table(metric, [claim for claim, _dates in dated], sources)}
    """


def forecast_chart(
    metric: dict[str, Any],
    metric_claims: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    stats: dict[str, Any] | None = None,
) -> str:
    history = [point for point in metric.get("history", []) if isinstance(point.get("value"), (int, float))]
    if not history and not metric_claims:
        return '<div class="chart-empty"><strong>No series yet.</strong><span>History and forecast markers will appear when this metric is populated.</span></div>'

    historical = []
    for point in history:
        date = decimal_date(point.get("date"))
        if date is not None:
            historical.append((date, float(point["value"]), point))

    # A metric may carry additional named series — e.g. what was ANNOUNCED alongside
    # what was actually measured. Each point may name a promised delivery date, which
    # renders as a whisker: the horizontal distance to reality is the delivery lag.
    extra_series = []
    for extra in metric.get("series", []):
        pts = []
        for pt in extra["points"]:
            date = decimal_date(pt.get("date"))
            if date is None:
                continue
            pts.append((date, float(pt["value"]), decimal_date(pt.get("promised")), pt))
        if pts:
            extra_series.append({"key": extra["key"], "label": extra["label"], "points": sorted(pts), "connect": extra.get("connect", True)})

    plotted_claims = []
    conversion_notes: set[str] = set()
    unit = str(metric.get("unit", ""))
    level_claims: list[tuple[dict[str, Any], float]] = []
    for claim in metric_claims:
        number, note = claim_plot_number(claim, unit)
        if note:
            conversion_notes.add(note)
        dates = date_range(claim["predicted"].get("by"))
        if dates is None:
            # "ongoing" rate claims assert a level that holds across time rather than
            # at a target date — draw them as a reference line, don't silently drop them.
            if number is not None and number > 0:
                level_claims.append((claim, number))
            continue
        plotted_claims.append((claim, dates, number))

    positioned = [item for item in plotted_claims if item[2] is not None and item[2] > 0]
    unpositioned = [item for item in plotted_claims if not (item[2] is not None and item[2] > 0)]
    if not historical and not positioned and not level_claims and plotted_claims:
        return milestone_timeline(metric, [(claim, dates) for claim, dates, _n in plotted_claims], sources, stats)

    x_values = [date for date, _value, _point in historical]
    for extra in extra_series:
        for date, _v, promised, _pt in extra["points"]:
            x_values.append(date)
            if promised is not None:
                x_values.append(promised)
    for _claim, (start, finish), _number in plotted_claims:
        x_values.extend((start, finish))
    if not x_values:
        return '<div class="chart-empty"><strong>No plottable dates yet.</strong><span>Claims still appear in the ledger below.</span></div>'
    x_min = min(x_values)
    x_max = max(x_values)
    if math.isclose(x_min, x_max):
        x_min -= 0.5
        x_max += 0.5
    else:
        x_margin = max((x_max - x_min) * 0.05, 0.08)
        x_min -= x_margin
        x_max += x_margin

    positive = [value for _date, value, _point in historical if value > 0]
    positive.extend(v for extra in extra_series for _d, v, _p, _pt in extra["points"] if v > 0)
    positive.extend(number for _claim, _dates, number in positioned)
    positive.extend(number for _claim, number in level_claims)
    logarithmic = bool(positive) and min(positive) > 0 and max(positive) / min(positive) >= 20
    if logarithmic:
        numeric_values = positive
    else:
        # A zero is a real observation — policy-events drops to 0 when a rule is
        # revoked, which is that metric's whole point. Only a log axis must drop it.
        numeric_values = [value for _date, value, _point in historical]
        numeric_values.extend(v for extra in extra_series for _d, v, _p, _pt in extra["points"])
        numeric_values.extend(number for _claim, _dates, number in positioned)
        numeric_values.extend(number for _claim, number in level_claims)
    if numeric_values:
        y_min = min(numeric_values)
        y_max = max(numeric_values)
        if math.isclose(y_min, y_max):
            y_min *= 0.8
            y_max *= 1.2
        elif logarithmic:
            y_max *= 1.6
            y_min /= 1.3
        else:
            span = y_max - y_min
            y_max += span * 0.14
            # Clamp the floor to zero only when the data itself is non-negative;
            # clamping a negative series pushes those points outside the viewBox.
            padded_min = y_min - span * 0.1
            y_min = padded_min if y_min < 0 else max(0.0, padded_min)
    else:
        y_min, y_max = 0.0, 1.0

    pad_t = PAD_T

    def x_pos(value: float) -> float:
        return PAD_L + (value - x_min) / (x_max - x_min) * (CHART_W - PAD_L - PAD_R)

    def y_pos(value: float) -> float:
        drawable = CHART_H - pad_t - PAD_B
        if logarithmic:
            lo = math.log10(y_min)
            hi = math.log10(y_max)
            if math.isclose(lo, hi):
                return pad_t + drawable / 2
            return pad_t + (hi - math.log10(value)) / (hi - lo) * drawable
        if math.isclose(y_min, y_max):
            return pad_t + drawable / 2
        return pad_t + (y_max - value) / (y_max - y_min) * drawable

    grid = []
    if numeric_values:
        for tick in value_ticks(numeric_values, logarithmic=logarithmic, integral=is_integral(numeric_values)):
            if tick < y_min or tick > y_max:
                continue
            y = y_pos(tick)
            grid.append(f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{CHART_W - PAD_R}" y2="{y:.1f}" class="chart-grid"/>')
            grid.append(f'<text x="{PAD_L - 12}" y="{y + 4:.1f}" text-anchor="end" class="axis-label">{esc(format_value(tick))}</text>')

    for position, label in time_ticks(x_min, x_max):
        x = x_pos(position)
        grid.append(f'<line x1="{x:.1f}" y1="{pad_t}" x2="{x:.1f}" y2="{CHART_H - PAD_B}" class="chart-grid vertical"/>')
        grid.append(f'<text x="{x:.1f}" y="{CHART_H - PAD_B + 25}" text-anchor="middle" class="axis-label">{esc(label)}</text>')

    reality = ""
    reality_drawn = 0
    if historical:
        # A zero cannot sit on a log axis. Break the line at the gap rather than
        # bridging it, and count what was actually drawn so the caption can say so.
        segments: list[list[tuple[float, float, dict[str, Any]]]] = []
        for date, value, point in historical:
            if value > 0 or not logarithmic:
                if not segments or segments[-1] is None:
                    segments.append([])
                segments[-1].append((date, value, point))
            elif segments:
                segments.append(None)  # type: ignore[arg-type]
        runs = [run for run in segments if run]
        drawable = [item for run in runs for item in run]
        reality_drawn = len(drawable)
        lines = "".join(
            f'<polyline points="{" ".join(f"{x_pos(d):.1f},{y_pos(v):.1f}" for d, v, _p in run)}" class="reality-line"/>'
            for run in runs
            if len(run) >= 2
        )
        dots = []
        for date, value, point in drawable:
            dots.append(
                f'<circle cx="{x_pos(date):.1f}" cy="{y_pos(value):.1f}" r="5" class="reality-dot" role="img" '
                f'aria-label="Reality, {esc(point.get("date"))}: {esc(value)}">'
                f'<title>{esc(point.get("date"))}: {esc(value)}{(" — " + esc(point.get("note"))) if point.get("note") else ""}</title></circle>'
            )
        reality = f'{lines}{"".join(dots)}'

    claimed = []
    for s_index, extra in enumerate(extra_series):
        pts = [(d, v, pr, pt) for d, v, pr, pt in extra["points"] if v > 0 or not logarithmic]
        if not pts:
            continue
        cls = f"claimed-series claimed-{s_index % 3}"
        if len(pts) >= 2 and extra.get("connect", True):
            spine = " ".join(f"{x_pos(d):.1f},{y_pos(v):.1f}" for d, v, _pr, _pt in pts)
            claimed.append(f'<polyline points="{spine}" class="{cls} claimed-line"/>')
        for date, value, promised, pt in pts:
            x, y = x_pos(date), y_pos(value)
            label = pt.get("note") or extra["label"]          # raw: tip is escaped once, at insertion
            promised_text = f' — promised by {pt.get("promised")}' if promised is not None else " — no delivery date given"
            unit_suffix = f' {metric.get("axis_unit")}' if metric.get("axis_unit") else ""
            tip = f'{extra["label"]} — {format_value(value)}{unit_suffix}, announced {pt.get("date")}{promised_text}. {label}'
            if promised is not None and promised > date:
                px = x_pos(promised)
                claimed.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{px:.1f}" y2="{y:.1f}" class="{cls} claimed-whisker"/>')
                claimed.append(f'<line x1="{px:.1f}" y1="{y - 5:.1f}" x2="{px:.1f}" y2="{y + 5:.1f}" class="{cls} claimed-cap"/>')
            if pt.get("cancelled"):
                claimed.append(
                    f'<g class="{cls} claimed-cancelled" role="img" aria-label="{esc(tip)}">'
                    f'<title>{esc(tip)}</title>'
                    f'<line x1="{x - 5:.1f}" y1="{y - 5:.1f}" x2="{x + 5:.1f}" y2="{y + 5:.1f}"/>'
                    f'<line x1="{x - 5:.1f}" y1="{y + 5:.1f}" x2="{x + 5:.1f}" y2="{y - 5:.1f}"/></g>'
                )
            else:
                claimed.append(
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" class="{cls} claimed-dot" role="img" '
                    f'aria-label="{esc(tip)}"><title>{esc(tip)}</title></circle>'
                )
    reality += "".join(claimed)
    if extra_series:
        conversion_notes.add(
            "Open markers are ANNOUNCED targets, plotted at the date each was claimed; the bar runs to the "
            "delivery date promised for it. The vertical distance is an announced-to-energized scale gap, but "
            "capacity bases are not always like-for-like; the horizontal gap is the delivery lag."
        )
    dropped_history = len(historical) - reality_drawn
    if dropped_history:
        conversion_notes.add(
            f"{dropped_history} zero observation{'s' if dropped_history != 1 else ''} cannot be shown on a log axis — "
            "the reality line breaks there rather than bridging the gap."
        )

    forecast_marks = []
    drawn_camps: list[str] = []

    def note_camp(camp: str) -> None:
        if camp not in drawn_camps:
            drawn_camps.append(camp)

    for claim, number in sorted(level_claims, key=lambda item: -item[1]):
        source = sources[claim["source"]]
        camp = camp_key(source["camp"])
        note_camp(camp)
        y = y_pos(number)
        label = source_short(source)
        tooltip = f'{label}: {claim["predicted"].get("value")} — a standing rate, not a dated target'
        forecast_marks.append(
            f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{CHART_W - PAD_R}" y2="{y:.1f}" class="forecast-level camp-{camp}" '
            f'role="img" aria-label="{esc(tooltip)}"><title>{esc(tooltip)}</title></line>'
        )
        forecast_marks.append(
            f'<text x="{CHART_W - PAD_R - 6:.1f}" y="{y - 6:.1f}" text-anchor="end" class="level-label">{esc(label)}</text>'
        )
    # Pass 1: every marker. Pass 2: every label. Labels used to be emitted inside the
    # marker loop and collision-tested only against other labels, so an opaque pill
    # could paint over a dot drawn earlier — including another forecaster's.
    markers: list[tuple[float, float]] = []
    pending_labels: list[tuple[float, float, str, str]] = []
    for claim, (start, finish), number in sorted(positioned, key=lambda item: item[1][0]):
        source = sources[claim["source"]]
        camp = camp_key(source["camp"])
        note_camp(camp)
        midpoint = (start + finish) / 2
        x = x_pos(midpoint)
        start_x = x_pos(start)
        finish_x = x_pos(finish)
        label = source_short(source)
        target = str(claim["predicted"].get("value", "milestone"))
        tooltip = f'{label}: {target} by {claim["predicted"].get("by")}'
        y = y_pos(number)
        markers.append((x, y))
        pending_labels.append((x, y, label, camp))
        forecast_marks.append(f'<line x1="{start_x:.1f}" y1="{y:.1f}" x2="{finish_x:.1f}" y2="{y:.1f}" class="forecast-range camp-{camp}"/>')
        forecast_marks.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{CHART_H - PAD_B}" class="forecast-stem camp-{camp}"/>')
        forecast_marks.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="forecast-dot camp-{camp}" role="img" aria-label="{esc(tooltip)}"><title>{esc(tooltip)}</title></circle>')

    placed_labels: list[tuple[float, float, float]] = []
    top_limit = pad_t + 14
    bottom_limit = CHART_H - PAD_B - 8

    def label_collides(lx: float, ly: float, lw: float) -> bool:
        for px, py, pw in placed_labels:
            if abs(ly - py) < 19 and lx < px + pw and px < lx + lw:
                return True
        for mx, my in markers:  # r=7 plus a 3px stroke, rounded up for clearance
            if lx - 10 < mx < lx + lw + 10 and ly - 24 < my < ly + 16:
                return True
        return False

    for x, y, label, camp in pending_labels:
        label_width = min(132, max(66, len(label) * 7 + 18))
        base_x = min(max(x - label_width / 2, PAD_L), CHART_W - PAD_R - label_width)
        chosen: tuple[float, float] | None = None
        for dy in (-20, -39, 26, 45, -58, 64, -77, 83):
            label_y = y + dy
            if label_y < top_limit or label_y > bottom_limit:
                continue
            for dx in (0.0, -(label_width / 2 + 16), label_width / 2 + 16):
                label_x = min(max(base_x + dx, PAD_L), CHART_W - PAD_R - label_width)
                if not label_collides(label_x, label_y, label_width):
                    chosen = (label_x, label_y)
                    break
            if chosen:
                break
        if chosen is None:
            chosen = (base_x, min(bottom_limit, max(top_limit, y - 20)))
        label_x, label_y = chosen
        placed_labels.append((label_x, label_y, label_width))
        forecast_marks.append(f'<rect x="{label_x:.1f}" y="{label_y - 14:.1f}" width="{label_width:.1f}" height="20" rx="4" class="forecast-label camp-{camp}"/>')
        forecast_marks.append(f'<text x="{label_x + label_width / 2:.1f}" y="{label_y:.1f}" text-anchor="middle" class="forecast-label-text">{esc(label)}</text>')

    # The legend keys the marks that exist, not the claims that were considered — a
    # camp swatch for a claim this axis never plotted advertises a mark that is not there.
    camps = [
        f'<span><i class="legend-dot camp-{camp}"></i>{esc(camp.replace("-", " "))}</span>'
        for camp in drawn_camps
    ]
    marks_drawn = len(positioned) + len(level_claims)
    _plotted_n, unplottable_n, undated_n = claim_counts(metric, metric_claims)
    off_chart = unplottable_n + undated_n
    if off_chart:
        conversion_notes.add(
            f"{marks_drawn} of {len(metric_claims)} claims are plotted here. The other {off_chart} set no numeric target "
            f"on this axis (dated milestones, or a quantity this axis does not measure) — they are recorded "
            f"{off_chart_where(metric_claims)}."
        )
    if level_claims:
        conversion_notes.add("Horizontal lines are standing rate claims — they assert a level that holds over time rather than by a target date.")
    notes = " ".join(sorted(conversion_notes))
    scale_note = " Log scale." if logarithmic else ""
    axis_unit = str(metric.get("axis_unit") or metric.get("unit") or "").strip()
    unit_label = (
        f'<text x="{PAD_L}" y="42" class="axis-label">{esc(axis_unit)}</text>' if axis_unit else ""
    )
    overline = "REALITY + PUBLISHED FORECASTS" if marks_drawn else "REALITY &middot; NO FORECAST PLOTS ON THIS AXIS"
    name = str(metric.get("name", metric["id"]))
    aria = (
        f"Reality history and {marks_drawn} plotted forecast marker{'s' if marks_drawn != 1 else ''} "
        f"({len(metric_claims)} claim{'s' if len(metric_claims) != 1 else ''} recorded) for {name}"
        + (f", measured in {axis_unit}." if axis_unit else ".")
    )
    if stats is not None:
        stats.update(
            mode="numeric",
            reality_recorded=len(metric.get("history", [])),
            reality_drawn=reality_drawn,
            marks_drawn=marks_drawn,
            unplottable=unplottable_n,
            undated=undated_n,
        )
    return f"""
      <div class="chart-scroll" tabindex="0" role="group" aria-label="{esc(name + ' chart (scrollable)')}">
        <svg class="forecast-chart" viewBox="0 0 {CHART_W} {CHART_H}" role="img" aria-label="{esc(aria)}">
          <text x="{PAD_L}" y="24" class="chart-overline">{overline}</text>
          {unit_label}
          {''.join(grid)}
          <line x1="{PAD_L}" y1="{CHART_H - PAD_B}" x2="{CHART_W - PAD_R}" y2="{CHART_H - PAD_B}" class="chart-axis"/>
          {reality}
          {''.join(forecast_marks)}
        </svg>
      </div>
      <div class="chart-legend"><span><i class="legend-line"></i>reality</span>{''.join(camps)}</div>
      {f'<details class="chart-explanation"><summary>How to read this chart</summary><p class="chart-note">{esc((scale_note + " " + notes).strip())}</p></details>' if scale_note or notes else ''}
      {chart_data_table(metric, metric_claims, sources)}
    """


def self_reported_marker(claim: dict[str, Any]) -> str:
    resolution = current_resolution(claim)
    evidence_kind = " ".join(
        str(value).lower()
        for value in (resolution.get("evidence_kind"), resolution.get("evidence_tier"), claim.get("evidence_kind"))
        if value
    )
    evidence = str(resolution.get("evidence", "")).lower()
    if "self-report" in evidence_kind or "self-report" in evidence:
        return '<span class="discount-marker" title="Self-reported evidence receives a confidence discount">Self-reported · discounted</span>'
    return ""


def claim_chip(claim: dict[str, Any], sources: dict[str, dict[str, Any]]) -> str:
    source = sources[claim["source"]]
    resolution = current_resolution(claim)
    camp = camp_key(source["camp"])
    status = str(resolution["status"])
    supersedes = ""
    if claim.get("supersedes"):
        supersedes = f'<p class="supersedes"><strong>Revision trail:</strong> {esc(claim["supersedes"])}</p>'
    relation = claim["measurement_relation"]
    relation_label = relation["type"].replace("-", " ")
    excluded = relation["type"] in {"proxy", "context"}
    relation_marker = f'<span class="relation-marker relation-{esc(relation["type"])}">{esc(relation_label)}{" · excluded from totals" if excluded else ""}</span>'
    history_items = "".join(
        f'<li><span>{esc(item["as_of"])}</span>{status_badge(item["status"])}<b>confidence {esc(confidence_number(item["confidence"]))}</b></li>'
        for item in claim["resolution_history"]
    )
    history_html = f'<details class="resolution-history"><summary>{len(claim["resolution_history"])} recorded assessment{"s" if len(claim["resolution_history"]) != 1 else ""}</summary><ol>{history_items}</ol></details>'
    evidence_links = "".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">Canonical measurement source {index + 1} ↗</a>'
        for index, url in enumerate(resolution["evidence_urls"])
    )
    basis = resolution["assessment_basis"]
    basis_html = f"""
      <details class="assessment-basis">
        <summary>How this status was assessed</summary>
        <dl>
          <div><dt>Relationship to measurement</dt><dd>{esc(relation['note'])}</dd></div>
          <div><dt>Test</dt><dd>{esc(basis['comparison_rule'])}</dd></div>
          <div><dt>Target / deadline</dt><dd>{esc(basis['target'])} · {esc(basis['deadline'])}</dd></div>
          {f'<div><dt>Conversion</dt><dd>{esc(relation["formula"])}</dd></div>' if relation.get('formula') else ''}
        </dl>
      </details>
    """
    return f"""
      <details class="claim-chip camp-border-{camp}" id="claim-{esc(claim['id'])}" data-claim-id="{esc(claim['id'])}">
        <summary><span>{esc(source_short(source))}</span><span aria-hidden="true">·</span>{status_badge(status)}<span aria-hidden="true">·</span><b>{esc(confidence_number(resolution['confidence']))}</b></summary>
        <div class="claim-card">
          <div class="claim-topline">
            <span class="camp-chip camp-{camp}">{esc(camp.replace('-', ' '))}</span>
            <span class="epistemic-chip">{esc(source['epistemic_type'].replace('-', ' '))}</span>
            {relation_marker}
            <span><a href="{esc(source['url'])}" target="_blank" rel="noopener noreferrer">{esc(source['author'])} · {esc(source['published'])} ↗</a></span>
          </div>
          <blockquote>“{esc(claim['quote'])}”<cite>{esc(claim['quote_location'])}</cite></blockquote>
          <dl class="claim-prediction">
            <div><dt>Prediction</dt><dd>{esc(claim['predicted']['value'])}</dd></div>
            <div><dt>By</dt><dd>{esc(claim['predicted']['by'])}</dd></div>
          </dl>
          <p class="conditionality"><strong>Conditionality:</strong> {esc(claim['conditionality'])}</p>
          {supersedes}
          <div class="resolution-pair" aria-label="Resolution status and confidence">
            <div><span>Status</span>{status_badge(status)}</div>
            <div><span>Confidence</span><strong>{esc(confidence_number(resolution['confidence']))}</strong></div>
            {self_reported_marker(claim)}
          </div>
          <div class="resolution-copy">
            <p><strong>Evidence · {esc(resolution['as_of'])}</strong>{esc(resolution['evidence'])}<span class="evidence-links">{evidence_links}</span></p>
            <p class="counterargument"><strong>Counterargument</strong>{esc(resolution['counterargument'])}</p>
          </div>
          {basis_html}
          {history_html}
        </div>
      </details>
    """


def off_chart_where(claims: list[dict[str, Any]]) -> str:
    """Ladder claims render once, in section 03 — pointing a reader "below" for them
    sends them to a card that does not contain them."""
    return (
        "in the milestone ladder and the claims below"
        if any(claim.get("ladder_rung") for claim in claims)
        else "in the claims below"
    )


def history_inspection(
    metric: dict[str, Any],
    claims: list[dict[str, Any]],
    stats: dict[str, Any] | None = None,
) -> str:
    history = metric.get("history", [])
    if not history and not claims:
        return "Exact history and forecast labels will appear when structured points are added."
    stats = stats or {}
    plotted, unplottable, undated = claim_counts(metric, claims)
    recorded = len(history)
    drawn = stats.get("reality_drawn", recorded)
    marks = stats.get("marks_drawn", plotted)
    reality_part = f"{recorded} reality point{'s' if recorded != 1 else ''}"
    if drawn < recorded:
        reality_part += f" ({drawn} drawn)"
    if stats.get("mode") == "milestones":
        parts = [reality_part, f"{marks} dated milestone{'s' if marks != 1 else ''} drawn"]
        unplottable = 0  # on this renderer the dated claims ARE the drawn milestones
    else:
        parts = [reality_part, f"{marks} forecast marker{'s' if marks != 1 else ''} drawn"]
    tail = []
    if unplottable:
        tail.append(f"{unplottable} dated claim{'s' if unplottable != 1 else ''} with no numeric target")
    if undated:
        tail.append(f"{undated} claim{'s' if undated != 1 else ''} with no fixed date")
    suffix = f" ({', '.join(tail)} — recorded {off_chart_where(claims)})" if tail else ""
    return " · ".join(parts) + suffix + ". Focus a marker for its exact label."


def metric_notes(metric: dict[str, Any], inspection: str) -> str:
    rows = []
    current = metric.get("current") or {}
    observation_points = ([current] if current else []) + list(metric.get("history", []) or []) + [point for series in metric.get("series", []) or [] for point in series.get("points", [])]
    linked_points = sum(bool(point.get("source_url")) for point in observation_points)
    for label, value in (
        ("Why it matters", metric.get("why_it_matters")),
        ("Source note", (metric.get("current") or {}).get("source_note")),
        ("Unit", metric.get("unit")),
        ("What it measures", metric.get("what_it_measures")),
        ("Source cadence", metric.get("source_cadence")),
        ("History inspection", inspection),
    ):
        if value:
            rows.append(f"<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>")
    if current:
        rows.append(f"<div><dt>Current observation provenance</dt><dd>{observation_evidence(current)}</dd></div>")
    rows.append(f"<div><dt>Point-level provenance</dt><dd>{linked_points} of {len(observation_points)} current and historical observations have direct point links; every remaining gap is classified explicitly.</dd></div>")
    rows.append(f"<div><dt>Canonical source</dt><dd>{source_link(metric.get('source'))}</dd></div>")
    return f"""
      <details class="metric-details">
        <summary>Metric notes ⓘ</summary>
        <dl class="metric-meta">{''.join(rows)}</dl>
      </details>
    """


def measurement_notes(metric: dict[str, Any]) -> str:
    notes = metric.get("measurement_notes") or "Measurement notes not yet populated."
    return f"""
      <details class="measurement-details">
        <summary>Measurement notes ⓘ</summary>
        <p class="measurement-notes">{esc(notes)}</p>
      </details>
    """


def claim_counts(metric: dict[str, Any], claims: list[dict[str, Any]]) -> tuple[int, int, int]:
    """(plotted, dated-but-unplottable, undated). The chart's note and the history
    caption must both describe what is actually drawn, not how many claims exist."""
    unit = str(metric.get("unit", ""))
    plotted = unplottable = undated = 0
    for claim in claims:
        number, _note = claim_plot_number(claim, unit)
        has_level = number is not None and number > 0
        if has_level:
            plotted += 1          # a dated point, or an undated reference line
        elif date_range(claim["predicted"].get("by")) is not None:
            unplottable += 1
        else:
            undated += 1
    return plotted, unplottable, undated


def visible_claims(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Give ladder claims one canonical chip location so every claim renders once."""
    return [claim for claim in claims if not claim.get("ladder_rung")]


def claim_row(claims: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> str:
    chips = "".join(claim_chip(claim, sources) for claim in visible_claims(claims))
    return f'<div class="claim-chip-row">{chips}</div>'


def supporting_card(metric: dict[str, Any], claims: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> str:
    name = metric.get("name") or metric["id"].replace("-", " ").title()
    current = metric.get("current")
    if not current:
        return (
            f'<article class="supporting-card unpopulated" id="metric-{esc(metric["id"])}">'
            f'<p>{esc(name)} — awaiting data.</p></article>'
        )
    verdict = f'<p class="metric-verdict">{esc(metric["verdict"])}</p>' if metric.get("verdict") else ""
    chart = ""
    stats: dict[str, Any] = {}
    scored_claims = [claim for claim in claims if is_headline_claim(claim)]
    if len(metric.get("history", [])) >= 3:
        chart = f'<div class="history-shell supporting-chart">{forecast_chart(metric, scored_claims, sources, stats)}</div>'
    inspection = history_inspection(metric, scored_claims, stats)
    return f"""
      <article class="supporting-card" id="metric-{esc(metric['id'])}">
        <header>
          <span class="stage-label">{esc(metric['stage'])} · supporting metric</span>
          <h4>{esc(name)} {source_icon(metric.get('source'))}</h4>
          {verdict}
        </header>
        {chart}
        <div class="supporting-current">
          <strong>{esc(current.get('display', current.get('value')))}</strong>
          <span class="confidence-tag">{esc(current.get('confidence', 'not recorded'))}</span>
          {vintage_tag(metric)}
        </div>
        {latest_observation(metric)}
        <p class="freshness-line">checked {esc(metric.get('last_checked', 'not yet populated'))} · {esc(cadence_clause(metric.get('source_cadence')))}</p>
        {claim_row(claims, sources)}
        {metric_notes(metric, inspection)}
        {measurement_notes(metric)}
      </article>
    """


def metric_card(
    metric: dict[str, Any],
    claims: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    order: int,
    supporting: list[tuple[dict[str, Any], list[dict[str, Any]]]],
) -> str:
    stage = metric["stage"]
    stage_label, _stage_question = STAGE_COPY[stage]
    name = metric.get("name") or metric["id"].replace("-", " ").title()
    current = metric.get("current")
    verdict = f'<p class="metric-verdict">{esc(metric["verdict"])}</p>' if metric.get("verdict") else ""
    if current:
        display = str(current.get("display", current.get("value")))
        # A sentence-length reading set at display size out-shouts the metric title;
        # the validator already flags these at 60 characters, so give that a rendering
        # consequence instead of leaving it advisory.
        size_class = ' class="long"' if len(display) > 60 else ""
        current_html = f"""
          <div class="metric-current">
            <span class="data-label">Current observation</span>
            <strong{size_class}>{esc(display)}</strong>
            <span class="current-tags"><span class="confidence-tag">{esc(current.get('confidence', 'not recorded'))}</span>{vintage_tag(metric)}</span>
          </div>
        """
    else:
        current_html = """
          <div class="metric-current unpopulated">
            <span class="data-label">Current observation</span>
            <strong>Awaiting structured data</strong>
          </div>
        """

    freshness = f"""
      <p class="freshness-line">checked {esc(metric.get('last_checked', 'not yet populated'))} · {esc(cadence_clause(metric.get('source_cadence')))}</p>
    """
    stats: dict[str, Any] = {}
    scored_claims = [claim for claim in claims if is_headline_claim(claim)]
    chart = forecast_chart(metric, scored_claims, sources, stats)
    inspection = history_inspection(metric, scored_claims, stats)
    supporting_html = ""
    if supporting:
        supporting_html = (
            f'<details class="supporting-details"><summary>{len(supporting)} supporting signal{"s" if len(supporting) != 1 else ""}</summary><div class="supporting-group">'
            + "".join(supporting_card(item, item_claims, sources) for item, item_claims in supporting)
            + "</div></details>"
        )
    return f"""
      <article class="metric-card" id="metric-{esc(metric['id'])}">
        <header class="metric-header">
          <div class="stage-number" aria-hidden="true">0{order}</div>
          <div>
            <span class="stage-label">{esc(stage_label)}</span>
            <h3>{esc(name)} {source_icon(metric.get('source'))}</h3>
            {verdict}
          </div>
        </header>
        <div class="metric-summary">{current_html}</div>
        {latest_observation(metric)}
        {freshness}
        <details class="metric-evidence">
          <summary><span>Explore chart and {len(claims)} forecast{'s' if len(claims) != 1 else ''}</span><i>Open evidence</i></summary>
          <div class="metric-evidence-body">
            <div class="history-shell">
              {chart}
            </div>
            {claim_row(claims, sources)}
            {supporting_html}
            {metric_notes(metric, inspection)}
            {measurement_notes(metric)}
          </div>
        </details>
      </article>
    """


WOUND_SPRING_JS = """
(function(){
var NS='http://www.w3.org/2000/svg';
var svg=document.getElementById('tk');
if(!svg)return;
var INK='#1c2b28';
var STAGES=__STAGES__;
var LABELFILL=['#eef0e9','#eef0e9','#eef0e9','#1c2b28','#1c2b28','#eef0e9'];
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var firstDraw=true;

function draw(){
  while(svg.firstChild)svg.removeChild(svg.firstChild);
  /* responsive geometry: viewBox width follows the container's aspect so the
     drawing fills wide screens instead of letterboxing left (fixed 1440 was
     the bug). Doubling counts are preserved so the curve shape is identical. */
  var box=svg.getBoundingClientRect();
  var Hv=828;
  var aspect=Math.max(1.15,Math.min(3.4,(box.width||1440)/(box.height||828)));
  var W=Math.round(Hv*aspect);
  svg.setAttribute('viewBox','0 0 '+W+' '+Hv);
  var BASE=740, H0=6;
  var X0=Math.round(0.048*W);      /* span the full container width */
  var XMAX=Math.round(0.935*W);
  var NOWX=Math.round(X0+0.6961*(XMAX-X0));  /* NOW keeps its horizontal position */
  /* The curve tops out LEVEL WITH THE EYEBROW rather than escaping the frame.
     Measured from the eyebrow's real position so it holds at any viewport:
     preserveAspectRatio xMinYMax anchors the bottom, so screen y maps back to
     viewBox y as (y - offsetY) / scale. */
  var scale=Math.min((box.width||W)/W,(box.height||Hv)/Hv);
  var offsetY=(box.height||Hv)-Hv*scale;
  var eyebrow=document.querySelector('.hero-headline .eyebrow');
  var topY=Hv*0.17;
  if(eyebrow&&scale>0){
    var er=eyebrow.getBoundingClientRect();
    topY=Math.max(28,Math.min(BASE-60,(er.top-box.top-offsetY)/scale));
  }
  var T=(XMAX-X0)/(Math.log((BASE-topY)/H0)/Math.LN2);
  function h(x){return H0*Math.pow(2,(x-X0)/T)}
  function el(name,attrs,parent){
    var e=document.createElementNS(NS,name);
    for(var k in attrs)e.setAttribute(k,attrs[k]);
    (parent||svg).appendChild(e);return e;
  }
  function pts(x1,x2,f){
    var a=[],x;
    for(x=x1;x<x2;x+=3)a.push([x,BASE-h(x)*f]);
    a.push([x2,BASE-h(x2)*f]);
    return a;
  }
  function poly(a){
    return a.map(function(p,i){return (i?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)}).join('');
  }
  /* strata: six stacked bands; solid through measured time, ghost past NOW */
  var segs=[[X0,NOWX,false],[NOWX,XMAX,true]];
  for(var i=0;i<6;i++){
    for(var sg=0;sg<2;sg++){
      var x1=segs[sg][0],x2=segs[sg][1],ghost=segs[sg][2];
      var top=pts(x1,x2,(i+1)/6), bot=pts(x1,x2,i/6).reverse();
      var d=poly(top.concat(bot))+'Z';
      var b=el('path',{d:d,fill:STAGES[i].color,'class':'band'+(ghost?' ghost':'')});
      b.style.transitionDelay=(firstDraw&&!reduce)?((0.35+i*0.09)+'s'):'0s';
    }
  }
  /* baseline + 2023 tick */
  el('line',{x1:Math.max(10,X0-58),y1:BASE,x2:Math.min(W-8,XMAX+52),y2:BASE,stroke:INK,'stroke-width':1,opacity:.45});
  var tick=X0+0.688*T;
  el('line',{x1:tick,y1:BASE,x2:tick,y2:BASE+8,stroke:INK,'stroke-width':1,opacity:.6});
  el('text',{x:tick,y:BASE+26,'text-anchor':'middle','class':'tmark'}).textContent='2023';
  /* the wound spring: coil + measured curve, one continuous stroke */
  var R=30, C=[X0,BASE-H0-R];
  var curvePts=[],k,N=110;
  for(k=0;k<=N;k++){
    var t=k/N, th=Math.PI/2+4.5*Math.PI*(1-t), r=9+(R-9)*t;
    curvePts.push([C[0]+r*Math.cos(th),C[1]+r*Math.sin(th)]);
  }
  var x;
  for(x=X0;x<NOWX;x+=3)curvePts.push([x,BASE-h(x)]);
  curvePts.push([NOWX,BASE-h(NOWX)]);
  var solid=el('path',{d:poly(curvePts),fill:'none',stroke:INK,'stroke-width':2.25,
    'stroke-linecap':'round','stroke-linejoin':'round'});
  /* forecast continuation: dashed, punches through the top of the frame */
  var late=el('g',{'class':'late'});
  var dashPts=[];
  for(x=NOWX;x<XMAX;x+=3)dashPts.push([x,BASE-h(x)]);
  dashPts.push([XMAX,BASE-h(XMAX)]);
  el('path',{d:poly(dashPts),fill:'none',stroke:INK,'stroke-width':2,
    'stroke-dasharray':'7 8','stroke-linecap':'round'},late);
  /* NOW rule + marker */
  el('line',{x1:NOWX,y1:BASE-h(NOWX)-14,x2:NOWX,y2:BASE,stroke:INK,'stroke-width':1.25,opacity:.8},late);
  el('text',{x:NOWX-12,y:BASE-h(NOWX)-22,'text-anchor':'end','class':'tmark'},late)
    .textContent='NOW (mid-2026)';
  /* open future */
  el('text',{x:Math.min(W-14,XMAX+20),y:topY+11,'class':'qmark'},late).textContent='?';
  /* force labels ride the slope of their own stratum; each links to its section */
  var defs=el('defs',{});
  var lx1=X0+3.05*T, lx2=NOWX-0.03*T;
  for(i=0;i<6;i++){
    el('path',{id:'mid'+i,d:poly(pts(lx1,lx2,(i+0.5)/6)),fill:'none'},defs);
    var a=el('a',{href:'#'+STAGES[i].anchor,'class':'bandlink'});
    var tx=el('text',{'class':'bandlabel late',fill:LABELFILL[i]},a);
    var tp=el('textPath',{href:'#mid'+i,startOffset:'100%','text-anchor':'end'},tx);
    tp.textContent=STAGES[i].name;
  }
  /* draw-in: coil unwinds into the curve; strata deposit; forecast fades up */
  if(firstDraw&&!reduce){
    var L=solid.getTotalLength();
    solid.style.strokeDasharray=L;
    solid.style.strokeDashoffset=L;
    solid.style.transition='stroke-dashoffset 1.7s cubic-bezier(.6,0,.3,1) .15s';
    requestAnimationFrame(function(){requestAnimationFrame(function(){
      solid.style.strokeDashoffset='0';
    })});
  }
  firstDraw=false;
}

function go(){
  draw();
  document.getElementById('scoreboard-top').classList.add('in');
}
requestAnimationFrame(function(){requestAnimationFrame(go)});
setTimeout(function(){
  if(!document.getElementById('scoreboard-top').classList.contains('in'))go();
},900); /* backstop: rAF suspends in background tabs */
var rT;
window.addEventListener('resize',function(){clearTimeout(rT);rT=setTimeout(draw,150);});
})();
"""


def render_hero_strata(stage_anchors: dict[str, str]) -> str:
    """Explain the causal model without asking a newcomer to decode a chart first."""
    anchors = {stage: f"metric-{esc(metric_id)}" for stage, metric_id in stage_anchors.items()}
    return f"""
      <aside class="takeoff-model" aria-labelledby="takeoff-model-title">
        <div class="model-heading">
          <span>Trajectory, in plain English</span>
          <strong id="takeoff-model-title">A feedback loop with a real-world speed limit.</strong>
        </div>
        <ol class="model-flow">
          <li>
            <span class="model-step">01</span>
            <div><strong>Supply grows</strong><p><a href="#{anchors['compute']}">Compute</a>, <a href="#{anchors['capital']}">capital</a>, and <a href="#{anchors['physical']}">power</a> expand what labs can build.</p></div>
          </li>
          <li>
            <span class="model-step">02</span>
            <div><strong>Systems improve</strong><p>Better <a href="#{anchors['algorithms']}">algorithms</a> turn those inputs into greater <a href="#{anchors['capability']}">capability</a>.</p></div>
          </li>
          <li>
            <span class="model-step">03</span>
            <div><strong>Progress may compound</strong><p>If AI can <a href="#{anchors['automation']}">automate AI research</a>, each cycle can help accelerate the next.</p></div>
          </li>
        </ol>
        <p class="model-question"><span>The central uncertainty</span> Does the software feedback loop accelerate faster than chips, power, and institutions can keep up?</p>
      </aside>
    """


def render_hero(
    stage_anchors: dict[str, str],
    tier_one: dict[str, dict[str, Any]],
    claims: list[dict[str, Any]],
    data_files: dict[str, str],
) -> str:
    data_label = "Seed data preview" if any(name.endswith(".seed.json") for name in data_files.values()) else "Production data build"
    strata_visual = render_hero_strata(stage_anchors)
    counts = {status: 0 for status in STATUS_ORDER}
    scored_claims = [claim for claim in claims if is_headline_claim(claim)]
    excluded_claims = [claim for claim in claims if not is_headline_claim(claim)]
    for claim in scored_claims:
        counts[current_resolution(claim)["status"]] += 1
    segments = "".join(
        f'<span class="hero-status status-text-{slug(status)}"><b>{counts[status]}</b> {esc("confirmed" if status == "resolved-true" else status)}</span>'
        for status in STATUS_ORDER
        if counts[status]
    )
    return f"""
      <header class="scoreboard-hero" id="scoreboard-top">
        <div class="hero-mast">
          <a href="#scoreboard-top" class="wordmark">AI Trajectory</a>
          <span>Evidence dashboard · {esc(data_label)}</span>
        </div>
        <div class="hero-stage">
          <div class="hero-headline">
            <p class="eyebrow">Progress, constraints, forecasts, and safety</p>
            <h1>Where is AI headed?</h1>
            <p class="hero-lede">Follow what labs can build, what systems can do, whether progress is compounding, and whether safeguards can keep pace.</p>
            <div class="hero-actions">
              <a class="primary-link" href="#overview">Start with the 2-minute overview <span aria-hidden="true">↓</span></a>
              <a class="secondary-link" href="methodology.html">How the evidence is assessed</a>
            </div>
            <p class="hero-scope">Measurement first, interpretation second. No composite risk score.</p>
          </div>
          {strata_visual}
        </div>
        <div class="hero-pulse" aria-label="Comparable claim status summary">
          <strong>{len(claims)} claims tracked · {len(scored_claims)} comparable · {len(excluded_claims)} proxy or context</strong>
          <div>{segments}</div>
        </div>
      </header>
    """


def render_status(
    claims: list[dict[str, Any]],
    tier_one: dict[str, dict[str, Any]],
    stage_anchors: dict[str, str],
    policy_metric: dict[str, Any] | None,
) -> str:
    def signal(stage: str) -> str:
        metric = tier_one[stage]
        return (
            f'<a class="overview-signal" href="#metric-{esc(stage_anchors[stage])}">'
            f'<span>{esc(STAGE_COPY[stage][0])}</span>'
            f'<strong>{esc(metric.get("verdict", "Open the evidence"))}</strong>'
            '<i aria-hidden="true">→</i></a>'
        )

    groups = [
        (
            "01",
            "Can the frontier keep building?",
            "Compute, money, and power set the pace the physical world can support.",
            ("compute", "capital", "physical"),
        ),
        (
            "02",
            "What can models do on their own?",
            "Algorithms translate resources into useful autonomy—but the cleanest measurements are still young and imperfect.",
            ("algorithms", "capability"),
        ),
        (
            "03",
            "Are systems accelerating their own progress?",
            "AI automating AI research is the hinge in fast-takeoff forecasts, and the least settled part of the story.",
            ("automation",),
        ),
    ]
    cards = "".join(
        f"""
          <article class="overview-card">
            <span class="overview-number">{number}</span>
            <h3>{esc(title)}</h3>
            <p>{esc(description)}</p>
            <div class="overview-signals">{''.join(signal(stage) for stage in stages)}</div>
          </article>
        """
        for number, title, description, stages in groups
    )
    policy_signal = ""
    if policy_metric:
        policy_signal = (
            f'<a class="overview-signal" href="#metric-{esc(policy_metric["id"])}">'
            f'<span>Policy</span><strong>{esc(policy_metric.get("verdict", "Open the evidence"))}</strong>'
            '<i aria-hidden="true">→</i></a>'
        )
    cards += f"""
      <article class="overview-card overview-boundary">
        <span class="overview-number">04</span>
        <h3>Can safeguards and institutions keep up?</h3>
        <p>Policy is observable. Alignment, verification, and real-world control remain open questions—not inputs to a pretend safety score.</p>
        <div class="overview-signals">
          {policy_signal}
          <a class="overview-signal" href="#open-questions"><span>Safety</span><strong>Follow risk from hazard through recovery</strong><i aria-hidden="true">→</i></a>
        </div>
      </article>
    """
    return f"""
      <section class="scoreboard-section status-section" id="overview" aria-labelledby="status-title">
        <div class="section-heading">
          <span>Start here</span>
          <h2 id="status-title">The AI trajectory in four questions.</h2>
          <p>Each question opens into measurements below. Start with the verdict; open the evidence only when you want to audit it.</p>
        </div>
        <div class="overview-grid">{cards}</div>
        <div class="reading-guide">
          <strong>How to read the tracker</strong>
          <p><span>Black line</span> = measured reality</p>
          <p><span>Colored marker</span> = a scoreable published claim</p>
          <p><span>Open any claim</span> = source, evidence, confidence, and the strongest counterargument</p>
        </div>
      </section>
    """


def render_next_checkpoints(claims_data: dict[str, Any], metrics_data: dict[str, Any]) -> str:
    """A repeat-visit surface: the next heterogeneous claims that reality can adjudicate."""
    sources = source_map(claims_data)
    metrics = {metric["id"]: metric for metric in metrics_data["metrics"]}
    today = date.today()
    today_value = today.year + (today.month - 1) / 12 + (today.day - 1) / 365
    candidates = []
    for claim in claims_data["claims"]:
        resolution = current_resolution(claim)
        window = date_range(claim["predicted"].get("by"))
        if not is_headline_claim(claim) or window is None or resolution["status"] in {"resolved-true", "falsified"}:
            continue
        if window[1] + 0.001 < today_value:
            continue
        candidates.append((window[1], claim))
    candidates.sort(key=lambda item: (item[0], str(item[1]["predicted"].get("by")), item[1]["id"]))
    cards = []
    for _deadline, claim in candidates[:6]:
        source = sources[claim["source"]]
        metric = metrics[claim["metric_id"]]
        resolution = current_resolution(claim)
        cards.append(f"""
          <article class="checkpoint-card">
            <div><span>{esc(claim['predicted']['by'])}</span>{status_badge(resolution['status'])}</div>
            <h3>{esc(claim['predicted']['value'])}</h3>
            <p>{esc(source['work'])}</p>
            <a href="#claim-{esc(claim['id'])}">{esc(metric.get('name', metric['id']))} →</a>
          </article>
        """)
    return f"""
      <section class="scoreboard-section checkpoint-section" id="checkpoints" aria-labelledby="checkpoint-title">
        <div class="section-heading">
          <span>Watch next</span>
          <h2 id="checkpoint-title">The next claims reality can test.</h2>
          <p>These are the nearest comparable deadlines still in play. They are checkpoints to revisit—not probabilities that an event will happen.</p>
        </div>
        <div class="checkpoint-grid">{''.join(cards)}</div>
      </section>
    """


def render_evidence_health(metrics_data: dict[str, Any], refresh_data: dict[str, Any]) -> str:
    policies = {item["metric_id"]: item for item in refresh_data["policies"]}
    reviews: dict[str, dict[str, Any]] = {}
    for review in refresh_data["reviews"]:
        reviews[review["metric_id"]] = review
    today = date.today()
    states = {"current": 0, "due": 0, "stale": 0}
    source_lag = 0
    point_total = 0
    point_linked = 0
    rows = []
    for metric in metrics_data["metrics"]:
        points = list(metric.get("history", []) or []) + [point for series in metric.get("series", []) or [] for point in series.get("points", [])]
        point_total += len(points)
        point_linked += sum(bool(point.get("source_url")) for point in points)
        policy = policies[metric["id"]]
        review = reviews[metric["id"]]
        checked = date.fromisoformat(review["checked_on"])
        due_on = checked + timedelta(days=policy["review_every_days"])
        stale_on = checked + timedelta(days=policy["stale_after_days"])
        state = "stale" if today > stale_on else "due" if today > due_on else "current"
        states[state] += 1
        source_lag += review["outcome"] == "source-lag"
        sources = "".join(
            f'<a href="{esc(source["url"])}" target="_blank" rel="noopener noreferrer">{esc(source["label"])} ↗</a>'
            for source in policy["sources"]
        )
        observed = (metric.get("current") or {}).get("as_of", "not recorded")
        rows.append(f"""
          <li class="health-row" data-review-health data-due="{due_on.isoformat()}" data-stale="{stale_on.isoformat()}">
            <span class="health-state health-{state}" data-health-label>{state}</span>
            <div><strong>{esc(metric.get('name', metric['id']))}</strong><span>reviewed {esc(review['checked_on'])} · observation {esc(observed)} · {esc(review['outcome'].replace('-', ' '))}</span></div>
            <details><summary>Sources</summary><div>{sources}<p>{esc(review['note'])}</p></div></details>
          </li>
        """)
    return f"""
      <section class="scoreboard-section health-section research-layer" id="evidence-health" aria-labelledby="health-title">
        <div class="health-summary">
          <div class="section-heading">
            <span>Evidence health</span>
            <h2 id="health-title">Fresh review and fresh data are not the same thing.</h2>
            <p>A source can be checked recently while its newest published observation remains old. This separates maintenance health from source lag.</p>
          </div>
          <div class="health-totals" aria-label="Evidence review summary"><strong data-health-summary>{states['current']} current · {states['due']} due · {states['stale']} stale</strong><span>{source_lag} source-lagged streams · {point_linked}/{point_total} observation points link to a named series</span></div>
        </div>
        <details class="health-details"><summary>Review all {len(rows)} evidence streams</summary><ol>{''.join(rows)}</ol></details>
      </section>
    """


def render_question_map(
    research: dict[str, Any],
    metrics_data: dict[str, Any],
    claims_data: dict[str, Any],
    cruxes_data: dict[str, Any],
) -> str:
    """Render the question-first registry without flattening its evidence lanes.

    The card face is deliberately qualitative. Numbers, source lineages, and
    unresolved assumptions only appear after the reader opens a question.
    """
    metrics = {metric["id"]: metric for metric in metrics_data["metrics"]}
    sources = source_map(claims_data)
    safety_questions = {
        question["id"]: question for question in research["safety_questions"]["questions"]
    }
    source_registry = {source["id"]: source for source in research["sources"]["sources"]}
    evidence_by_question: dict[str, list[dict[str, Any]]] = {}
    for link in research["evidence"]["links"]:
        evidence_by_question.setdefault(link["question_id"], []).append(link)
    aggregate_by_question: dict[str, list[dict[str, Any]]] = {}
    for signal in research["aggregates"]["signals"]:
        for link in signal["question_links"]:
            aggregate_by_question.setdefault(link["question_id"], []).append(signal)

    # Put the four load-bearing entry points first. The remaining six are one
    # explicit reveal away in Guided view and all visible in Research view.
    priority = {
        item: index
        for index, item in enumerate(
            ("build-capacity", "real-task-capability", "ai-rd-feedback", "control-and-evaluation")
        )
    }
    questions = sorted(
        research["questions"]["questions"],
        key=lambda question: (priority.get(question["id"], 99), research["questions"]["questions"].index(question)),
    )
    cards = []
    state_labels = {
        "measured": ("Measured", "is-measured"),
        "partly-measured": ("Partly measured", "is-partial"),
        "forecast-only": ("Forecasts, no stable series", "is-review"),
        "open": ("Open question", "is-open"),
        "missing-series": ("Missing a defensible series", "is-gap"),
    }

    for index, question in enumerate(questions, start=1):
        question_links = evidence_by_question.get(question["id"], [])
        observed_links = [
            link for link in question_links
            if link["record_type"] == "metric" and link["relation"] in {
                "direct-observation", "supporting-observation", "constraint-observation"
            }
        ]
        proxy_links = [
            link for link in question_links
            if link["record_type"] == "metric" and link["relation"] in {"proxy-observation", "context-observation"}
        ]
        linked_metrics = [metrics[link["record_id"]] for link in observed_links if link["record_id"] in metrics]
        proxy_metrics = [metrics[link["record_id"]] for link in proxy_links if link["record_id"] in metrics]
        linked_claims = [
            claim for claim in claims_data["claims"] if claim["metric_id"] in question["metric_ids"]
        ]
        linked_safety_questions = [
            safety_questions[question_id]
            for question_id in question["safety_question_ids"]
            if question_id in safety_questions
        ]
        aggregate_signals = aggregate_by_question.get(question["id"], [])

        if linked_metrics:
            metric_links = "".join(
                f'<li><a href="#metric-{esc(metric["id"])}">{esc(metric.get("name", metric["id"]))}</a>'
                f'<span>{esc((metric.get("current") or {}).get("as_of", "observation not dated"))}</span></li>'
                for metric in linked_metrics
            )
            observed_copy = f'{len(linked_metrics)} measurement stream{"s" if len(linked_metrics) != 1 else ""} directly or supportingly inform this question. Open one to see its reality line and point-level evidence.'
            observed_list = f"<ul>{metric_links}</ul>"
            if proxy_metrics:
                observed_copy += f' {len(proxy_metrics)} additional stream{"s are" if len(proxy_metrics) != 1 else " is"} shown only as proxy or context.'
        else:
            observed_copy = "No direct or supporting recurring measurement series is registered yet. The gap is being shown rather than filled with a proxy."
            if proxy_metrics:
                observed_copy += f' {len(proxy_metrics)} related stream{"s are" if len(proxy_metrics) != 1 else " is"} registered only as proxy or context.'
            observed_list = ""

        work_ids: list[str] = []
        for claim in linked_claims:
            if claim["source"] not in work_ids:
                work_ids.append(claim["source"])
        if work_ids:
            works = "".join(
                f'<li><a href="#forecast-comparison">{esc(sources[source_id]["work"])}</a>'
                f'<span>{esc(sources[source_id]["epistemic_type"].replace("-", " "))}</span></li>'
                for source_id in work_ids
            )
            forecast_copy = (
                f'{len(linked_claims)} attributed claim{"s" if len(linked_claims) != 1 else ""} from '
                f'{len(work_ids)} registered work{"s" if len(work_ids) != 1 else ""}. '
                "They remain separate from observed reality and from one another."
            )
            forecast_list = f"<ul>{works}</ul>"
        else:
            forecast_copy = "No structured, resolvable named forecast has been mapped to this question yet."
            forecast_list = ""

        verified_aggregates = [signal for signal in aggregate_signals if signal["status"] == "verified-snapshot"]
        if verified_aggregates:
            registered = "".join(
                f'<li><a href="{esc(signal["snapshot"]["source_url"])}" target="_blank" rel="noopener noreferrer">'
                f'{esc(source_registry[signal["source_id"]]["label"])} ↗</a><span>{esc(signal["snapshot"]["display"])} · {esc(signal["snapshot"]["captured_at"])}</span></li>'
                for signal in verified_aggregates
            )
            aggregate_copy = "Verified, exactly matched aggregate snapshots are displayed separately from observed reality and named views."
            aggregate_list = f"<ul>{registered}</ul>"
        elif aggregate_signals:
            registered = "".join(
                f'<li><a href="{esc(source_registry[signal["source_id"]]["url"])}" target="_blank" rel="noopener noreferrer">'
                f'{esc(source_registry[signal["source_id"]]["label"])} ↗</a><span>registered; no matched snapshot</span></li>'
                for signal in aggregate_signals
            )
            aggregate_copy = (
                "Relevant panels or forecasting platforms are registered, but no number is shown until the exact wording, "
                "sample, date, and aggregation method match."
            )
            aggregate_list = f"<ul>{registered}</ul>"
        else:
            aggregate_copy = "No like-for-like panel, survey, or forecasting-platform snapshot is registered for this question."
            aggregate_list = ""

        safety_links = "".join(
            f'<a href="#safety-{esc(item["id"])}">{esc(item["title"])} →</a>' for item in linked_safety_questions
        )
        status_label, status_class = state_labels[question["status"]]
        lanes = [
            f'<section class="lane lane-observed"><header><h4>Observed reality</h4><span class="lane-label">facts</span></header><p>{esc(observed_copy)}</p>{observed_list}</section>',
        ]
        if "named-forecast" in question["lanes"]:
            lanes.append(
                f'<section class="lane lane-forecasts"><header><h4>Named published views</h4><span class="lane-label">attributed</span></header><p>{esc(forecast_copy)}</p>{forecast_list}</section>'
            )
        if "aggregate" in question["lanes"]:
            lanes.append(
                f'<section class="lane lane-aggregate"><header><h4>Aggregate expectations</h4><span class="lane-label">group belief</span></header><p>{esc(aggregate_copy)}</p>{aggregate_list}</section>'
            )
        actions = (
            f'<div class="question-actions">{safety_links}'
            + (f'<a href="#metric-{esc(linked_metrics[0]["id"])}">Open the lead measurement →</a>' if linked_metrics else "")
            + "</div>"
            if linked_safety_questions or linked_metrics
            else ""
        )
        cards.append(f"""
          <article class="question-card" data-question-card id="research-question-{esc(question['id'])}">
            <span class="question-number">Question {index:02d}</span>
            <h3>{esc(question['title'])}</h3>
            <p class="question-takeaway">{esc(question['summary'])}</p>
            <span class="coverage-state {status_class}">{esc(status_label)}</span>
            <details class="question-drawer">
              <summary><span>Explore this question</span><span class="question-drawer-count">{len(lanes)} evidence lane{"s" if len(lanes) != 1 else ""}</span></summary>
              <div class="question-lanes">{''.join(lanes)}</div>
              <p class="disclosure-hint"><strong>What would change the picture:</strong> {esc(question['what_would_change'])}</p>
              {actions}
            </details>
          </article>
        """)

    return f"""
      <section class="scoreboard-section question-section" id="questions" aria-labelledby="questions-title">
        <div class="section-heading">
          <span>The research map</span>
          <h2 id="questions-title">Ten questions. Three kinds of evidence.</h2>
          <p>Start with the question, not the database. Each one keeps measured reality, named forecasts, and group expectations in separate lanes so unlike evidence never becomes a fake consensus.</p>
        </div>
        <details class="section-drawer question-index">
          <summary><span>Browse the ten-question research map</span><i>Choose a question</i></summary>
          <div class="question-map" data-progressive-questions data-guided-limit="4">
            <div class="question-map-header">
              <div><h3>Explore what matters to you.</h3><p>The four load-bearing questions appear first. Reveal the rest only when you want the full research map.</p></div>
              <div class="question-map-key" aria-label="Question evidence states"><span><i></i> measured</span><span><i></i> partial</span><span><i></i> open or missing</span></div>
            </div>
            <div class="question-map-grid" id="question-map-list">{''.join(cards)}</div>
          </div>
        </details>
      </section>
    """


def render_ai_rd_focus(research: dict[str, Any], claims_data: dict[str, Any]) -> str:
    """Flagship question page: synthesis first, unlike evidence kept separate."""
    package = research["ai_rd_evidence"]
    synthesis = package["current_synthesis"]
    sources = source_map(claims_data)
    kind_labels = {
        "benchmark-evaluation": "Benchmark", "randomized-field-experiment": "Causal study",
        "technical-worker-survey": "Self-report survey", "company-operational-report": "Company operations",
        "company-deployment-report": "Company deployment", "company-autonomous-research-demo": "Company demonstration",
    }
    directness_labels = {
        "benchmark-only": "Capability proxy", "adjacent-causal-evidence": "Adjacent causal evidence",
        "self-report-only": "Self-report only", "company-report-with-direct-relevance": "Company report; direct relevance",
        "company-reported-autonomous-demo": "Company demo; direct relevance",
    }
    direction_labels = {
        "supports-limited": "Supports limited contribution", "counterevidence": "Counterevidence",
        "mixed": "Mixed", "capability-signal": "Capability signal", "self-report-signal": "Self-report signal",
    }
    evidence_cards = []
    for observation in sorted(package["observations"], key=lambda item: item["date"], reverse=True):
        evidence_cards.append(f"""
          <details class="rd-evidence-card direction-{esc(observation['direction'])}">
            <summary><span>{esc(observation['date'])}</span><strong>{esc(observation['title'])}</strong><i>{esc(direction_labels[observation['direction']])}</i></summary>
            <div class="rd-evidence-body">
              <div class="rd-tags"><span>{esc(kind_labels[observation['evidence_kind']])}</span><span>{esc(directness_labels[observation['directness']])}</span></div>
              <p>{esc(observation['finding'])}</p>
              <aside><strong>Why this does not settle the question</strong><p>{esc(observation['caveat'])}</p></aside>
              <a href="{esc(observation['source']['url'])}" target="_blank" rel="noopener noreferrer">{esc(observation['source']['artifact'])} · {esc(observation['source']['publisher'])} ↗</a>
            </div>
          </details>
        """)
    rd_claims = [claim for claim in claims_data["claims"] if claim["metric_id"] == "ai-rd-automation"]
    claim_items = "".join(
        f'<li><a href="#claim-{esc(claim["id"])}"><span>{esc(sources[claim["source"]]["work"])} · {esc(sources[claim["source"]]["epistemic_type"].replace("-", " "))} · {esc(claim["measurement_relation"]["type"])}</span><strong>{esc(claim["predicted"]["value"])}</strong><i>{esc(claim["predicted"]["by"])}</i></a></li>'
        for claim in rd_claims
    )
    aggregate_signals = [signal for signal in research["aggregates"]["signals"] if signal["status"] == "verified-snapshot" and any(link["question_id"] == "ai-rd-feedback" for link in signal["question_links"])]
    aggregate_cards = []
    for signal in aggregate_signals:
        snapshot = signal["snapshot"]
        distribution = snapshot.get("distribution", {}).get("buckets", {})
        bucket_labels = {"quite_likely_81_100": "Quite likely", "likely_61_80": "Likely", "about_even_41_60": "About even", "unlikely_21_40": "Unlikely", "quite_unlikely_0_20": "Quite unlikely"}
        bars = "".join(f'<li><span>{esc(bucket_labels.get(key, key.replace("_", " ")))}</span><b style="--amount:{float(value):.1f}%"></b><strong>{esc(value)}%</strong></li>' for key, value in distribution.items())
        aggregate_cards.append(f"""
          <article class="rd-aggregate-card">
            <span>Historical expert view · fielded {esc(snapshot['fielded_from'])}–{esc(snapshot['fielded_to'])}</span>
            <h3>Could near-total AI R&amp;D produce a 10× feedback loop within five years?</h3>
            <ul class="belief-bars">{bars}</ul>
            <p>{esc(snapshot['sample_or_participants'])} This is a dated judgment about a stronger scenario—not a current consensus or a measured probability of takeoff.</p>
            <details><summary>Exact wording and method</summary><div><p>{esc(snapshot['question_text'])}</p><p>{esc(snapshot['aggregate_method'])}</p><a href="{esc(snapshot['source_url'])}" target="_blank" rel="noopener noreferrer">Original survey results ↗</a></div></details>
          </article>
        """)
    return f"""
      <section class="scoreboard-section rd-focus" id="ai-rd-question" aria-labelledby="rd-focus-title">
        <div class="rd-focus-heading">
          <div class="section-heading"><span>Flagship question · AI R&amp;D feedback</span><h2 id="rd-focus-title">Is AI accelerating the creation of better AI?</h2><p>{esc(synthesis['reading'])}</p></div>
          <div class="rd-reading"><span>Current reading · {esc(synthesis['as_of'])}</span><strong>Contribution visible. Multiplier unknown.</strong><p>No single score is shown because the evidence measures different things.</p></div>
        </div>
        <div class="rd-summary-grid">
          <article><span>Closest direct-relevance evidence</span><p>{esc(synthesis['strongest_direct_evidence'])}</p></article>
          <article><span>Best counterevidence</span><p>{esc(synthesis['strongest_counterevidence'])}</p></article>
          <article><span>The missing measurement</span><p>{esc(synthesis['measurement_gap'])}</p></article>
        </div>
        <div class="rd-path" aria-label="AI R&D evidence path"><span><b>1</b> AI performs research tasks</span><i>→</i><span><b>2</b> Researchers produce more</span><i>→</i><span><b>3</b> Better models arrive faster</span><i>→</i><span><b>4</b> The loop compounds</span></div>
        <p class="rd-path-note">Public evidence reaches parts of steps 1–2. It does not yet establish steps 3–4.</p>
        <details class="rd-explorer">
          <summary><span>Explore observations, forecasts, and expert beliefs</span><i>Three separate evidence lanes</i></summary>
          <div class="rd-columns">
            <div><div class="rd-column-heading"><span>Observed evidence</span><strong>Seven typed observations</strong></div><div class="rd-evidence-list">{''.join(evidence_cards)}</div></div>
            <div>
              <div class="rd-column-heading"><span>Named published views</span><strong>Forecasts stay attributed</strong></div><ol class="rd-claim-list">{claim_items}</ol>
              <details class="section-drawer rd-forecast-drawer"><summary><span>Open the shared milestone ladder</span><i>Compare dates</i></summary><p>The detailed metric section keeps each author’s original definition, relation, status, evidence, and counterargument.</p><a href="#metric-ai-rd-automation">Explore the AI R&amp;D milestone evidence →</a></details>
              <div class="rd-column-heading rd-belief-heading"><span>Aggregate expectation</span><strong>A cohort, not a consensus</strong></div>{''.join(aggregate_cards) if aggregate_cards else '<p class="rd-empty">No exact aggregate snapshot has passed the inclusion rule.</p>'}
            </div>
          </div>
        </details>
      </section>
    """


def render_open_questions(safety_data: dict[str, Any]) -> str:
    cards = []
    state_labels = {
        "measured": "Measured",
        "partly-measured": "Partly measured",
        "missing-series": "Missing a stable series",
    }

    def spectrum_visual(question: dict[str, Any], compact: bool = False) -> tuple[str, str]:
        lean = float(question["lean"])
        lean_pct = (lean + 1) * 50
        range_width = {"narrow": 16.0, "moderate": 30.0, "wide": 50.0}[question["range"]]
        range_start = max(0.0, lean_pct - range_width / 2)
        range_end = min(100.0, lean_pct + range_width / 2)
        beam_style = f"--lean:{lean_pct:.1f}%;--range-start:{range_start:.1f}%;--range-width:{range_end - range_start:.1f}%"
        if question["measurement_state"] == "missing-series" and abs(lean) <= 0.05:
            lean_class, lean_short, lean_long, leaning_pole = "leans-center", "No stable lean", "No stable evidence lean", "neither pole"
        elif lean < -0.05:
            lean_class, lean_short, lean_long, leaning_pole = "leans-a", "Leans Pole A", "Leans toward Pole A", question["pole_a"]["label"]
        elif lean > 0.05:
            lean_class, lean_short, lean_long, leaning_pole = "leans-b", "Leans Pole B", "Leans toward Pole B", question["pole_b"]["label"]
        else:
            lean_class, lean_short, lean_long, leaning_pole = "leans-center", "Near midpoint", "Evidence is near the midpoint", "neither pole"
        if compact:
            visual = f'<div class="crux-summary-lean {lean_class}"><div class="crux-mini-beam" style="{beam_style}" aria-hidden="true"><span class="crux-range"></span><span class="crux-midpoint"></span><span class="crux-marker"></span></div></div>'
        else:
            aria = f'{lean_long}: {leaning_pole}, with a {question["range"]} interpretive range. This is not a statistical confidence interval.'
            visual = f"""
              <div class="crux-poles">
                <div><span>Pole A</span><strong>{esc(question['pole_a']['label'])}</strong><p>{esc(question['pole_a']['desc'])}</p></div>
                <div><span>Pole B</span><strong>{esc(question['pole_b']['label'])}</strong><p>{esc(question['pole_b']['desc'])}</p></div>
              </div>
              <div class="crux-lean-panel {lean_class}">
                <div class="crux-lean-heading"><span>Current evidence lean</span><strong>{esc(lean_long)}</strong><i>{esc(question['range'])} interpretive range</i></div>
                <div class="crux-beam" style="{beam_style}" role="img" aria-label="{esc(aria)}"><span class="crux-range"></span><span class="crux-midpoint"></span><span class="crux-marker"></span></div>
                <div class="crux-beam-labels"><span><b>Pole A</b>{esc(question['pole_a']['label'])}</span><span><b>Pole B</b>{esc(question['pole_b']['label'])}</span></div>
                <p>The dot is the current qualitative synthesis. The band is interpretive disagreement—not a probability or statistical confidence interval.</p>
              </div>
            """
        return visual, f'{lean_short} · {question["range"]} range'

    def special_visual(question: dict[str, Any], compact: bool = False) -> tuple[str, str]:
        if question["visual_type"] == "domain-matrix":
            if compact:
                cells = "".join(f'<span class="domain-state is-{esc(item["state"])}">{esc(item["label"])}</span>' for item in question["domains"])
                return f'<div class="safety-mini-matrix">{cells}</div>', "Domain-specific"
            cells = "".join(f'<article class="safety-domain is-{esc(item["state"])}"><span>{esc(item["state"].replace("-", " "))}</span><strong>{esc(item["label"])}</strong><p>{esc(item["reading"])}</p></article>' for item in question["domains"])
            return f'<div class="safety-domain-matrix">{cells}</div><p class="safety-viz-note">Domains remain separate because evidence in one does not establish danger in another.</p>', "Domain-specific"
        if question["visual_type"] == "exposure-ladder":
            if compact:
                steps = "".join('<span></span>' for _ in question["ladder"])
                return f'<div class="safety-mini-ladder">{steps}</div>', "No coverage baseline"
            steps = "".join(f'<li><span>{item["level"]}</span><div><strong>{esc(item["label"])}</strong><p>{esc(item["desc"])}</p></div></li>' for item in question["ladder"])
            return f'<ol class="safety-exposure-ladder">{steps}</ol><p class="safety-viz-note">No single current rung is shown: public telemetry is insufficient to estimate the distribution of real deployments.</p>', "No coverage baseline"
        if compact:
            return f'<div class="safety-mini-ledger"><strong>{len(question["incidents"])}</strong><span>provider cases</span></div>', "Ledger, not a trend"
        incidents = "".join(f'<li><span>{esc(item["date"])} · {esc(item["domain"])} · {esc(item["severity"])}</span><strong>{esc(item["ai_role"])}</strong><p>{esc(item["reading"])}</p><small>{esc(item["attribution"])}</small></li>' for item in question["incidents"])
        return f'<ol class="safety-incident-ledger">{incidents}</ol><p class="safety-viz-note">These are documented provider cases, not independently verified examples or an incidence rate. Reporting coverage and denominators are missing.</p>', "Ledger, not a trend"

    for index, question in enumerate(safety_data["questions"], start=1):
        if question["visual_type"] == "spectrum":
            compact_visual, visual_label = spectrum_visual(question, compact=True)
            full_visual, _ = spectrum_visual(question)
        else:
            compact_visual, visual_label = special_visual(question, compact=True)
            full_visual, _ = special_visual(question)
        evidence = "".join(
            f'<li><span>{esc(item["observed_period"])} · {esc(item["measurement"])}</span><p>{esc(item["finding"])}</p><small>{esc(item["independence"])} · {esc(item["caveat"])}</small><a href="{esc(item["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(item["source_label"])} ↗</a></li>'
            for item in question["evidence"]
        )
        indicators = "".join(f'<li>{esc(item)}</li>' for item in question["indicators"])
        gaps = "".join(f'<li>{esc(item)}</li>' for item in question["gaps"])
        movers = "".join(f'<li>{esc(item)}</li>' for item in question["movers"])
        quality = question["evidence_quality"]
        cards.append(f"""
          <details class="crux-card safety-card" id="safety-{esc(question['id'])}">
            <summary>
              <span>{index:02d}</span>
              <div class="safety-summary-title"><i>{esc(question['stage'])}</i><strong>{esc(question['title'])}</strong></div>
              <div class="safety-summary-viz">{compact_visual}<i>{esc(visual_label)} · {esc(state_labels[question['measurement_state']])}</i></div>
            </summary>
            <div class="crux-body safety-body">
              <p class="crux-full-question">{esc(question['question'])}</p>
              <div class="safety-reading"><span>Current reading · {esc(question['reading_as_of'])}</span><strong>{esc(question['current_reading'])}</strong></div>
              {full_visual}
              <dl class="safety-quality"><div><dt>Evidence setting</dt><dd>{esc(quality['setting'])}</dd></div><div><dt>Independence</dt><dd>{esc(quality['independence'])}</dd></div><div><dt>Coverage</dt><dd>{esc(quality['coverage'])}</dd></div></dl>
              <div class="safety-method-grid">
                <div><h4>What is measured</h4><ul>{indicators}</ul></div>
                <div><h4>What is still missing</h4><ul>{gaps}</ul></div>
                <div><h4>What would change the reading</h4><ul>{movers}</ul></div>
              </div>
              <details class="crux-evidence safety-evidence"><summary>Audit {len(question['evidence'])} source-backed evidence items</summary><ol>{evidence}</ol></details>
              <p class="crux-review">No cross-question safety score is calculated. Each reading keeps its measurement setting, independence, coverage, and gaps visible.</p>
            </div>
          </details>
        """)
    return f"""
      <section class="scoreboard-section crux-section" id="open-questions" aria-labelledby="crux-title">
        <div class="section-heading">
          <span>Frontier AI safety · causal chain</span>
          <h2 id="crux-title">Eight questions from hazard to recovery.</h2>
          <p>{esc(safety_data['headline_reading'])}</p>
        </div>
        <div class="safety-chain" aria-label="Safety question framework"><span>Hazard</span><i>→</i><span>Exposure</span><i>→</i><span>Control</span><i>→</i><span>Governance</span><i>→</i><span>Outcomes</span><i>→</i><span>Resilience</span></div>
        <p class="safety-scope">Scope: {esc(safety_data['scope'])}</p>
        <details class="section-drawer">
          <summary><span>Explore the eight safety questions</span><i>Open</i></summary>
          <div class="crux-list">{''.join(cards)}</div>
        </details>
      </section>
    """


def render_forecast_comparison(
    claims_data: dict[str, Any],
    metrics_data: dict[str, Any],
) -> str:
    """Compare bodies of work without turning unlike claims into a leaderboard."""
    metric_map = {metric["id"]: metric for metric in metrics_data["metrics"]}
    rows = []
    for source in claims_data["forecast_sources"]:
        source_claims = [claim for claim in claims_data["claims"] if claim["source"] == source["id"]]
        if not source_claims:
            rows.append(f"""
              <tr class="comparison-unpopulated">
                <th scope="row"><strong>{esc(source['work'])}</strong><span>{esc(source['author'])} · {esc(source.get('published', 'undated'))}</span></th>
                <td class="comparison-coverage"><strong>Source registered</strong><span>No structured claim harvest yet</span></td>
                <td class="comparison-reading"><p>Not scored. An empty row describes tracker coverage, not the forecaster’s position.</p></td>
              </tr>
            """)
            continue
        scored_claims = [claim for claim in source_claims if is_headline_claim(claim)]
        context_claims = [claim for claim in source_claims if not is_headline_claim(claim)]
        counts = {status: 0 for status in STATUS_ORDER}
        for claim in scored_claims:
            counts[current_resolution(claim)["status"]] += 1
        coverage = []
        for claim in source_claims:
            metric = metric_map.get(claim["metric_id"], {})
            stage = str(metric.get("stage", claim["metric_id"]))
            if stage not in coverage:
                coverage.append(stage)
        bars = "".join(
            f'<span class="comparison-segment comparison-{slug(status)}" style="--share:{counts[status] / max(1, len(scored_claims)):.5f}" '
            f'title="{counts[status]} {esc("resolved true" if status == "resolved-true" else status)}"></span>'
            for status in STATUS_ORDER
            if counts[status]
        )
        count_labels = "".join(
            f'<span class="comparison-count status-text-{slug(status)}"><b>{counts[status]}</b> {esc("confirmed" if status == "resolved-true" else status)}</span>'
            for status in STATUS_ORDER
            if counts[status]
        )
        claim_links = "".join(
            f'<li><a href="#claim-{esc(claim["id"])}"><span>{esc(STAGE_COPY.get(metric_map.get(claim["metric_id"], {}).get("stage", ""), (claim["metric_id"], ""))[0])}</span>'
            f'<strong>{esc(claim["predicted"]["value"])}</strong>{status_badge(current_resolution(claim)["status"])}</a></li>'
            for claim in source_claims
        )
        year = str(source.get("published", "undated"))
        rows.append(f"""
          <tr>
            <th scope="row">
              <strong>{esc(source['work'])}</strong>
              <span>{esc(source['author'])} · {esc(year)}</span>
            </th>
            <td class="comparison-coverage">
              <strong>{len(scored_claims)} comparable · {len(context_claims)} proxy/context</strong>
              <span>{len(coverage)} area{'s' if len(coverage) != 1 else ''}: {esc(', '.join(coverage))}</span>
            </td>
            <td class="comparison-reading">
              <div class="comparison-bar" aria-hidden="true">{bars}</div>
              <div class="comparison-counts">{count_labels}</div>
              <details class="comparison-claims">
                <summary>Jump to individual claims</summary>
                <ul>{claim_links}</ul>
              </details>
            </td>
          </tr>
        """)
    return f"""
      <section class="scoreboard-section comparison-section research-layer" id="forecast-comparison" aria-labelledby="comparison-title">
        <div class="section-heading">
          <span>Compare the claims</span>
          <h2 id="comparison-title">Which bodies of work are holding up?</h2>
          <p>This is a status map, not a ranking. Forecasts, scenarios, models, and intentions answer different questions, so claim counts should never be read as grades.</p>
        </div>
        <div class="status-key" aria-label="Status definitions">
          <span><i class="key-confirmed"></i><b>Confirmed</b> target met</span>
          <span><i class="key-ahead"></i><b>Ahead</b> reality faster</span>
          <span><i class="key-on-track"></i><b>On-track</b> consistent so far</span>
          <span><i class="key-behind"></i><b>Behind</b> reality lagging</span>
          <span><i class="key-pending"></i><b>Pending</b> not yet testable</span>
          <span><i class="key-falsified"></i><b>Falsified</b> target missed</span>
        </div>
        <div class="comparison-table-shell">
          <table class="comparison-table">
            <thead><tr><th>Body of work</th><th>Coverage</th><th>Current evidence</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>
        <p class="comparison-note">Portfolio bars include only direct and formula-backed translated claims. Proxy and context claims remain linked but excluded. Status and confidence remain separate.</p>
      </section>
    """


def render_ladder(claims_data: dict[str, Any], sources: dict[str, dict[str, Any]]) -> str:
    claims = claims_data["claims"]
    rungs_html = []
    for index, rung in enumerate(claims_data["milestone_ladder"]["rungs"], start=1):
        rung_claims = [claim for claim in claims if claim.get("ladder_rung") == rung["id"]]
        if rung_claims:
            statuses = {current_resolution(claim)["status"] for claim in rung_claims}
            if "resolved-true" in statuses:
                state = "filled"
            elif statuses & {"on-track", "ahead"}:
                state = "half"
            else:
                state = "empty"
            body = "".join(claim_chip(claim, sources) for claim in rung_claims)
        else:
            state = "empty"
            body = '<p class="ladder-empty">No structured forecast is attached to this rung yet.</p>'
        rungs_html.append(f"""
          <li class="ladder-rung">
            <details class="rung-details">
              <summary><span class="rung-dot rung-{state}" aria-label="{state}"></span><span>Rung {index}</span><strong>{esc(rung['label'])}</strong></summary>
              <div class="rung-claims">{body}</div>
            </details>
          </li>
        """)
    return f"""
      <section class="scoreboard-section ladder-section research-layer" id="milestones" aria-labelledby="milestone-title">
        <div class="section-heading">
          <span>Forecasts versus reality</span>
          <h2 id="milestone-title">Different predictions, translated into the same milestones.</h2>
          <p>Authors use different definitions and dates. This ladder keeps their original wording, then shows where their claims overlap.</p>
        </div>
        <ol class="milestone-ladder">{''.join(rungs_html)}</ol>
      </section>
    """


def render_drift(claims_data: dict[str, Any]) -> str:
    series = claims_data.get("forecast_drift", [])
    observations = [
        (str(item.get("source", "Source")), obs)
        for item in series
        for obs in item.get("observations", [])
        if isinstance(obs.get("median_year"), (int, float)) and decimal_date(obs.get("as_of")) is not None
    ]
    if not observations:
        chart = """
          <div class="drift-empty" role="img" aria-label="Forecast drift chart awaiting structured observations">
            <div class="empty-axis"><span>Published estimate</span><i></i><i></i><i></i><i></i></div>
            <div><strong>No comparable revision series has been verified yet.</strong><p>This view will appear when at least two like-for-like estimates from the same forecaster have been recorded.</p></div>
          </div>
        """
    else:
        x_values = [decimal_date(obs["as_of"]) for _source, obs in observations]
        y_values = [float(obs["median_year"]) for _source, obs in observations]
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        if math.isclose(x_min, x_max):
            x_min, x_max = x_min - 0.5, x_max + 0.5
        if math.isclose(y_min, y_max):
            y_min, y_max = y_min - 1, y_max + 1
        y_pad = max((y_max - y_min) * 0.12, 0.6)
        y_min -= y_pad
        y_max += y_pad
        x_pad = max((x_max - x_min) * 0.08, 0.25)
        x_min -= x_pad
        x_max += x_pad
        label_gutter = 132

        def px(value: float) -> float:
            return PAD_L + (value - x_min) / (x_max - x_min) * (CHART_W - PAD_L - PAD_R - label_gutter)

        def py(value: float) -> float:
            return PAD_T + (y_max - value) / (y_max - y_min) * (CHART_H - PAD_T - PAD_B)

        marks = [f'<text x="{PAD_L}" y="24" class="chart-overline">PUBLISHED MEDIAN, BY VINTAGE</text>']
        # y axis: the forecast median year being predicted
        for tick in value_ticks([y_min + y_pad, y_max - y_pad], logarithmic=False):
            y = py(tick)
            marks.append(f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{CHART_W - PAD_R - label_gutter}" y2="{y:.1f}" class="chart-grid"/>')
            marks.append(f'<text x="{PAD_L - 12}" y="{y + 4:.1f}" text-anchor="end" class="axis-label">{int(round(tick))}</text>')
        marks.append(f'<text x="{PAD_L - 12}" y="{PAD_T - 14:.1f}" text-anchor="end" class="axis-label">predicts</text>')
        # x axis: when the forecast was published
        first_year, last_year = math.ceil(x_min), math.floor(x_max)
        step = max(1, math.ceil(max(1, last_year - first_year) / 6))
        for year in range(first_year, last_year + 1, step):
            x = px(float(year))
            marks.append(f'<line x1="{x:.1f}" y1="{PAD_T}" x2="{x:.1f}" y2="{CHART_H - PAD_B}" class="chart-grid vertical"/>')
            marks.append(f'<text x="{x:.1f}" y="{CHART_H - PAD_B + 25}" text-anchor="middle" class="axis-label">{year}</text>')
        marks.append(f'<line x1="{PAD_L}" y1="{CHART_H - PAD_B}" x2="{CHART_W - PAD_R - label_gutter}" y2="{CHART_H - PAD_B}" class="chart-axis"/>')
        marks.append(f'<text x="{(PAD_L + CHART_W - PAD_R - label_gutter) / 2:.1f}" y="{CHART_H - 10}" text-anchor="middle" class="axis-label">published</text>')

        groups: dict[str, list[dict[str, Any]]] = {}
        for source, obs in observations:
            groups.setdefault(source, []).append(obs)
        for index, (source, points) in enumerate(groups.items()):
            points.sort(key=lambda point: decimal_date(point["as_of"]) or 0)
            coordinates = " ".join(
                f"{px(decimal_date(point['as_of']) or 0):.1f},{py(float(point['median_year'])):.1f}" for point in points
            )
            marks.append(f'<polyline points="{coordinates}" class="drift-line drift-{index % 5}"/>')
            for point in points:
                x = px(decimal_date(point["as_of"]) or 0)
                y = py(float(point["median_year"]))
                note = point.get("note")
                milestone = point.get("milestone")
                tip = (
                    f'{source}: median {point["median_year"]} as of {point["as_of"]}'
                    + (f" for {milestone}" if milestone else "")
                    + (f" — {note}" if note else "")
                )
                marks.append(
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" class="drift-dot drift-{index % 5}" role="img" '
                    f'aria-label="{esc(tip)}"><title>{esc(tip)}</title></circle>'
                )
            last = points[-1]
            marks.append(
                f'<text x="{px(decimal_date(last["as_of"]) or 0) + 12:.1f}" y="{py(float(last["median_year"])) + 4:.1f}" '
                f'class="drift-label drift-{index % 5}">{esc(source)}</text>'
            )

        data_rows = "".join(
            f'<tr><td>{esc(source)}</td><td>{esc(obs["as_of"])}</td><td>{esc(obs["median_year"])}</td><td>{esc(obs.get("milestone", "Not recorded"))}</td></tr>'
            for source, obs in observations
        )
        chart = (
            f'<div class="chart-scroll" tabindex="0" role="group" aria-label="Forecast drift chart (scrollable)"><svg class="forecast-chart drift-chart" viewBox="0 0 {CHART_W} {CHART_H}" role="img" aria-label="Median AGI forecast over publication time">{"".join(marks)}</svg></div>'
            f'<details class="chart-data"><summary>View chart as data</summary><div><table><thead><tr><th>Forecaster</th><th>Published</th><th>Median year</th><th>Milestone</th></tr></thead><tbody>{data_rows}</tbody></table></div></details>'
        )
    return f"""
      <section class="scoreboard-section drift-section research-layer" id="forecast-drift" aria-labelledby="drift-title">
        <div class="section-heading">
          <span>How expectations change</span>
          <h2 id="drift-title">Are forecasters moving their timelines?</h2>
          <p>Each line follows one person’s published median over time. It shows revision, not consensus: these estimates are never averaged together.</p>
        </div>
        {chart}
      </section>
    """


def inline_markdown(text: str) -> str:
    safe = esc(text)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    safe = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", safe)
    return safe


def markdown_subset(text: str) -> str:
    """Render headings, paragraphs, lists, links, emphasis, and inline code."""
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            flush_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1)) + 1
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue
        item = re.match(r"^[-*]\s+(.+)$", line)
        numbered = re.match(r"^\d+\.\s+(.+)$", line)
        if item or numbered:
            flush_paragraph()
            wanted = "ul" if item else "ol"
            if list_type != wanted:
                close_list()
                output.append(f"<{wanted}>")
                list_type = wanted
            output.append(f"<li>{inline_markdown((item or numbered).group(1))}</li>")
            continue
        close_list()
        paragraph.append(line)
    flush_paragraph()
    close_list()
    return "\n".join(output)


def render_methodology(methodology_text: str, data_files: dict[str, str]) -> str:
    return f"""
      <section class="scoreboard-section methodology-section" id="methodology" aria-labelledby="methodology-title">
        <div class="section-heading">
          <span>05 · Methodology</span>
          <h2 id="methodology-title">How to read—and challenge—the scoreboard</h2>
        </div>
        <div class="methodology-prose">{markdown_subset(methodology_text)}</div>
        <p class="build-provenance">This build rendered <code>{esc(data_files['metrics'])}</code> and <code>{esc(data_files['claims'])}</code>. The generated page contains no hand-entered observations.</p>
      </section>
    """


def render_methodology_link() -> str:
    return """
      <section class="scoreboard-section methodology-link" id="methodology" aria-labelledby="methodology-link-title">
        <span class="data-label">Methodology</span>
        <h2 id="methodology-link-title"><a href="methodology.html">How to read—and challenge—the scoreboard <span aria-hidden="true">↗</span></a></h2>
      </section>
    """


def render_unmatched_supporting(
    metrics: list[dict[str, Any]],
    claims_by_metric: dict[str, list[dict[str, Any]]],
    sources: dict[str, dict[str, Any]],
) -> str:
    if not metrics:
        return ""
    cards = "".join(
        supporting_card(metric, claims_by_metric.get(metric["id"], []), sources)
        for metric in metrics
    )
    return f"""
      <section class="scoreboard-section supporting-signals research-layer" aria-labelledby="supporting-title">
        <details class="supporting-drawer">
          <summary><span>Supporting signals</span><strong id="supporting-title">Value and policy response</strong><i>Open</i></summary>
          <div class="supporting-strip">{cards}</div>
        </details>
      </section>
    """


def render_scoreboard(metrics_data: dict[str, Any], claims_data: dict[str, Any], refresh_data: dict[str, Any], cruxes_data: dict[str, Any], research: dict[str, Any], methodology_text: str, data_files: dict[str, str]) -> str:
    sources = source_map(claims_data)
    claims_by_metric: dict[str, list[dict[str, Any]]] = {}
    for claim in claims_data["claims"]:
        claims_by_metric.setdefault(claim["metric_id"], []).append(claim)
    tier_one = {metric["stage"]: metric for metric in metrics_data["metrics"] if metric.get("tier") == 1 and metric.get("stage") in CORE_STAGES}
    tier_two_by_stage: dict[str, list[dict[str, Any]]] = {}
    unmatched_tier_two = []
    for metric in metrics_data["metrics"]:
        if metric.get("tier") != 2:
            continue
        if metric.get("stage") in CORE_STAGES:
            tier_two_by_stage.setdefault(metric["stage"], []).append(metric)
        else:
            unmatched_tier_two.append(metric)
    stage_anchors = {stage: tier_one[stage]["id"] for stage in CORE_STAGES}
    policy_metric = next((metric for metric in metrics_data["metrics"] if metric["id"] == "policy-events"), None)
    cards = "".join(
        metric_card(
            tier_one[stage],
            claims_by_metric.get(tier_one[stage]["id"], []),
            sources,
            index,
            [
                (metric, claims_by_metric.get(metric["id"], []))
                for metric in tier_two_by_stage.get(stage, [])
            ],
        )
        for index, stage in enumerate(CORE_STAGES, start=1)
    )
    hero = render_hero(stage_anchors, tier_one, claims_data["claims"], data_files)
    return f"""
      <script>(function(){{try{{document.documentElement.dataset.view=localStorage.getItem('ai-trajectory-view')||'guided';}}catch(e){{document.documentElement.dataset.view='guided';}}}})();</script>
      {hero}
      <nav class="scoreboard-nav" aria-label="Scoreboard sections">
        <a href="#overview">Overview</a><a href="#ai-rd-question">AI R&amp;D</a><a href="#questions">Questions</a><a href="#checkpoints">Watch next</a><a class="research-nav" href="#forecast-comparison">Claims</a><a href="#loop">Evidence</a><a href="methodology.html">Methodology</a>
        <span class="view-switch" role="group" aria-label="Page detail level"><button type="button" data-view-button="guided">Guided</button><button type="button" data-view-button="research">Research</button></span>
      </nav>
      <main>
        {render_status(claims_data['claims'], tier_one, stage_anchors, policy_metric)}
        {render_ai_rd_focus(research, claims_data)}
        {render_question_map(research, metrics_data, claims_data, cruxes_data)}
        {render_next_checkpoints(claims_data, metrics_data)}
        {render_evidence_health(metrics_data, refresh_data)}
        {render_open_questions(research["safety_questions"])}
        {render_forecast_comparison(claims_data, metrics_data)}
        <section class="scoreboard-section loop-section" id="loop" aria-labelledby="loop-title">
          <div class="section-heading">
            <span>Explore the evidence</span>
            <h2 id="loop-title">Six drivers. One reality line for each.</h2>
            <p>Every section begins with the plain-language takeaway and current observation. The charts put published predictions on the same axis as what actually happened.</p>
          </div>
          <details class="section-drawer evidence-drawer">
            <summary><span>Browse the six core measurements</span><i>Open evidence</i></summary>
            <div class="metric-stack">{cards}</div>
          </details>
        </section>
        {render_unmatched_supporting(unmatched_tier_two, claims_by_metric, sources)}
        {render_ladder(claims_data, sources)}
        {render_drift(claims_data)}
        {render_methodology_link()}
      </main>
      <script>
      (function(){{
        var viewButtons=document.querySelectorAll('[data-view-button]');
        function setView(view){{
          document.documentElement.dataset.view=view;
          try{{localStorage.setItem('ai-trajectory-view',view);}}catch(e){{}}
          viewButtons.forEach(function(button){{button.setAttribute('aria-pressed',String(button.dataset.viewButton===view));}});
        }}
        function revealTarget(){{
          if(!location.hash)return;
          var target=document.getElementById(location.hash.slice(1));
          if(!target)return;
          if(target.closest && target.closest('.research-layer'))setView('research');
          if(target.tagName==='DETAILS')target.open=true;
          var parent=target.parentElement;
          while(parent){{if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}}
        }}
        window.addEventListener('hashchange',revealTarget);
        revealTarget();
        viewButtons.forEach(function(button){{button.addEventListener('click',function(){{setView(button.dataset.viewButton);}});}});
        setView(document.documentElement.dataset.view==='research'?'research':'guided');
        var now=new Date();
        var counts={{current:0,due:0,stale:0}};
        document.querySelectorAll('[data-review-health]').forEach(function(row){{
          var due=new Date(row.dataset.due+'T23:59:59');
          var stale=new Date(row.dataset.stale+'T23:59:59');
          var state=now>stale?'stale':now>due?'due':'current';
          counts[state]++;
          var label=row.querySelector('[data-health-label]');
          label.textContent=state;label.className='health-state health-'+state;
        }});
        var summary=document.querySelector('[data-health-summary]');
        if(summary)summary.textContent=counts.current+' current · '+counts.due+' due · '+counts.stale+' stale';
      }})();
      </script>
    """
