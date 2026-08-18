#!/usr/bin/env python3
"""Validate and load the question-first research registry.

This registry is deliberately separate from rendering.  It makes relationships
between questions, observations, published forecasts, and aggregate belief
signals auditable without converting unlike evidence into a single score.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = ROOT / "data" / "research"
SCOREBOARD_DIR = ROOT / "data" / "scoreboard"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
LANES = {"observed", "named-forecast", "aggregate"}
QUESTION_KINDS = {"measurement", "crux", "forecast-review"}
QUESTION_STATUSES = {"measured", "partly-measured", "forecast-only", "open", "missing-series"}
LINK_TYPES = {"metric", "crux", "claim-portfolio", "coverage-gap", "research-evidence"}
LINK_RELATIONS = {
    "direct-observation", "supporting-observation", "constraint-observation",
    "proxy-observation", "context-observation", "open-evidence", "portfolio-review", "unmeasured",
    "evidence-package",
}
SOURCE_TYPES = {
    "measurement-series", "primary-record", "forecast", "scenario", "model", "model-output",
    "analysis", "intention", "longitudinal-panel", "cross-sectional-expert-survey",
    "community-forecast-platform", "benchmark-evaluation", "field-experiment", "worker-survey",
    "company-disclosure",
}
SOURCE_FORBIDDEN_FIELDS = {"weight", "prestige", "score", "rank", "authority_weight"}
AI_RD_EVIDENCE_KINDS = {
    "benchmark-evaluation",
    "randomized-field-experiment",
    "technical-worker-survey",
    "company-operational-report",
    "company-deployment-report",
    "company-autonomous-research-demo",
}
AI_RD_DIRECTNESS = {
    "benchmark-only",
    "adjacent-causal-evidence",
    "self-report-only",
    "company-report-with-direct-relevance",
    "company-reported-autonomous-demo",
}
AI_RD_DIRECTIONS = {"capability-signal", "supports-limited", "counterevidence", "mixed", "self-report-signal"}
AI_RD_RELATIONS = {
    "ai-rd-capability-proxy",
    "adjacent-software-productivity",
    "technical-worker-productivity",
    "direct-ai-rd-contribution",
    "autonomous-ai-rd-demo",
}
AI_RD_SYNTHESIS_STATUSES = {"partly-measured", "direct-evidence-limited", "missing-series"}
SAFETY_VISUAL_TYPES = {"spectrum", "domain-matrix", "exposure-ladder", "incident-ledger"}
SAFETY_MEASUREMENT_STATES = {"measured", "partly-measured", "missing-series"}
SAFETY_STAGES = {"hazard", "exposure", "control", "governance", "outcomes", "resilience"}
SAFETY_RANGES = {"narrow", "moderate", "wide"}
SAFETY_SOURCE_TYPES = {
    "government-evaluation", "developer-evaluation", "developer-experiment", "government-taxonomy",
    "government-research", "international-synthesis", "official-legal-guidance", "statute",
    "provider-threat-intelligence", "intergovernmental-methodology", "government-synthesis",
}


class RegistryError(ValueError):
    """Raised when the registry makes an invalid or misleading relationship."""


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryError(f"Missing required registry file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RegistryError(f"{path.name} must be a JSON object")
    if not SEMVER.fullmatch(str(value.get("schema_version", ""))):
        raise RegistryError(f"{path.name} needs a semantic schema_version")
    if not DATE.fullmatch(str(value.get("registry_version", ""))):
        raise RegistryError(f"{path.name} needs a YYYY-MM-DD registry_version")
    return value


def _load_existing(path: Path) -> dict[str, Any]:
    """Load legacy tracker data without imposing the new registry envelope."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryError(f"Missing referenced tracker data: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RegistryError(f"{path.name} must be a JSON object")
    return value


def _items(data: dict[str, Any], key: str, file_name: str) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, dict) for item in value):
        raise RegistryError(f"{file_name}.{key} must be a non-empty array of objects")
    return value


def _unique_ids(items: list[dict[str, Any]], label: str) -> set[str]:
    ids: list[str] = []
    for item in items:
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            raise RegistryError(f"{label} has an item without a non-empty id")
        ids.append(item_id)
    duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
    if duplicates:
        raise RegistryError(f"Duplicate {label} IDs: {', '.join(duplicates)}")
    return set(ids)


def _require_strings(item: dict[str, Any], fields: tuple[str, ...], label: str) -> None:
    for field in fields:
        if not isinstance(item.get(field), str) or not item[field].strip():
            raise RegistryError(f"{label}.{field} must be a non-empty string")


def _validate_questions(
    questions: list[dict[str, Any]], metric_ids: set[str], crux_ids: set[str], safety_question_ids: set[str]
) -> set[str]:
    question_ids = _unique_ids(questions, "question")
    for question in questions:
        label = f"question {question['id']}"
        _require_strings(question, ("title", "short_label", "summary", "what_would_change"), label)
        if question.get("kind") not in QUESTION_KINDS:
            raise RegistryError(f"{label}.kind is invalid")
        if question.get("status") not in QUESTION_STATUSES:
            raise RegistryError(f"{label}.status is invalid")
        lanes = question.get("lanes")
        if not isinstance(lanes, list) or not lanes or not set(lanes) <= LANES:
            raise RegistryError(f"{label}.lanes must use recognized evidence lanes")
        if len(lanes) != len(set(lanes)):
            raise RegistryError(f"{label}.lanes must not contain duplicates")
        linked_metrics = question.get("metric_ids")
        if not isinstance(linked_metrics, list) or not set(linked_metrics) <= metric_ids:
            raise RegistryError(f"{label}.metric_ids references an unknown scoreboard metric")
        linked_cruxes = question.get("crux_ids")
        if not isinstance(linked_cruxes, list) or not set(linked_cruxes) <= crux_ids:
            raise RegistryError(f"{label}.crux_ids references an unknown crux")
        linked_safety_questions = question.get("safety_question_ids")
        if not isinstance(linked_safety_questions, list) or not set(linked_safety_questions) <= safety_question_ids:
            raise RegistryError(f"{label}.safety_question_ids references an unknown safety question")
        if question["status"] == "missing-series" and linked_metrics:
            raise RegistryError(f"{label} is missing-series but claims a metric series")
    return question_ids


def _validate_sources(
    clusters: list[dict[str, Any]], sources: list[dict[str, Any]], scoreboard_source_ids: set[str]
) -> set[str]:
    cluster_ids = _unique_ids(clusters, "dependency cluster")
    source_ids = _unique_ids(sources, "source")
    for cluster in clusters:
        _require_strings(cluster, ("label", "reason"), f"dependency cluster {cluster['id']}")
    mapped_scoreboard_sources: set[str] = set()
    for source in sources:
        label = f"source {source['id']}"
        _require_strings(source, ("label", "url", "lane", "source_type", "dependency_cluster", "versioning", "last_reviewed"), label)
        if not source["url"].startswith("https://"):
            raise RegistryError(f"{label}.url must be an https URL")
        if source["lane"] not in LANES or source["source_type"] not in SOURCE_TYPES:
            raise RegistryError(f"{label} has an invalid lane or source_type")
        if source["dependency_cluster"] not in cluster_ids:
            raise RegistryError(f"{label} references an unknown dependency cluster")
        if not DATE.fullmatch(source["last_reviewed"]):
            raise RegistryError(f"{label}.last_reviewed must be YYYY-MM-DD")
        forbidden = SOURCE_FORBIDDEN_FIELDS & set(source)
        if forbidden:
            raise RegistryError(
                f"{label} uses prohibited prestige-based fields: {', '.join(sorted(forbidden))}. "
                "Inclusion and provenance are not forecast weights."
            )
        scoreboard_source_id = source.get("scoreboard_source_id")
        if scoreboard_source_id is not None:
            if source["lane"] != "named-forecast" or scoreboard_source_id not in scoreboard_source_ids:
                raise RegistryError(f"{label}.scoreboard_source_id must reference a named forecast source")
            mapped_scoreboard_sources.add(scoreboard_source_id)
    missing = scoreboard_source_ids - mapped_scoreboard_sources
    if missing:
        raise RegistryError(f"Named forecast sources missing source-registry entries: {', '.join(sorted(missing))}")
    return source_ids


def _validate_evidence_links(
    links: list[dict[str, Any]], question_ids: set[str], metric_ids: set[str], crux_ids: set[str],
    research_evidence_ids: set[str],
) -> None:
    seen: set[tuple[str, str, str]] = set()
    for link in links:
        _require_strings(link, ("question_id", "record_type", "record_id", "relation"), "evidence link")
        if link["question_id"] not in question_ids:
            raise RegistryError(f"Evidence link references unknown question {link['question_id']}")
        if link["record_type"] not in LINK_TYPES or link["relation"] not in LINK_RELATIONS:
            raise RegistryError("Evidence link has an invalid record_type or relation")
        key = (link["question_id"], link["record_type"], link["record_id"])
        if key in seen:
            raise RegistryError(f"Duplicate evidence link: {' / '.join(key)}")
        seen.add(key)
        if link["record_type"] == "metric" and link["record_id"] not in metric_ids:
            raise RegistryError(f"Evidence link references unknown metric {link['record_id']}")
        if link["record_type"] == "crux" and link["record_id"] not in crux_ids:
            raise RegistryError(f"Evidence link references unknown crux {link['record_id']}")
        if link["record_type"] == "claim-portfolio" and link["record_id"] != "all-scoreboard-claims":
            raise RegistryError("The only supported claim portfolio is all-scoreboard-claims")
        if link["record_type"] == "research-evidence" and link["record_id"] not in research_evidence_ids:
            raise RegistryError(f"Evidence link references unknown research evidence {link['record_id']}")
        if link["record_type"] == "research-evidence" and link["relation"] != "evidence-package":
            raise RegistryError("Research evidence links must use the evidence-package relation")


def _validate_aggregate_signals(signals: list[dict[str, Any]], source_ids: set[str], aggregate_source_ids: set[str], question_ids: set[str]) -> None:
    _unique_ids(signals, "aggregate signal")
    for signal in signals:
        label = f"aggregate signal {signal['id']}"
        _require_strings(signal, ("source_id", "status", "why_registered", "snapshot_rule"), label)
        if signal["source_id"] not in source_ids:
            raise RegistryError(f"{label} references unknown source")
        if signal["source_id"] not in aggregate_source_ids:
            raise RegistryError(f"{label}.source_id must reference a source in the aggregate lane")
        links = signal.get("question_links")
        if not isinstance(links, list) or not links:
            raise RegistryError(f"{label}.question_links must not be empty")
        for question_link in links:
            if not isinstance(question_link, dict) or question_link.get("question_id") not in question_ids:
                raise RegistryError(f"{label} has an invalid canonical question link")
            if question_link.get("match") not in {"exact", "related"}:
                raise RegistryError(f"{label} question match must be exact or related")
        if signal["status"] == "registered-no-snapshot":
            if "snapshot" in signal or "value" in signal:
                raise RegistryError(f"{label} may not carry a value before a verified snapshot is imported")
        elif signal["status"] == "verified-snapshot":
            snapshot = signal.get("snapshot")
            if not isinstance(snapshot, dict):
                raise RegistryError(f"{label}.snapshot must be an object")
            _require_strings(
                snapshot,
                (
                    "question_text", "canonical_match_rationale", "fielded_from", "fielded_to",
                    "captured_at", "publication_url", "aggregate_method", "resolution_rule",
                    "source_url", "cohort", "sample_or_participants", "display",
                ),
                f"{label}.snapshot",
            )
            for field in ("fielded_from", "fielded_to", "captured_at"):
                if not DATE.fullmatch(snapshot[field]):
                    raise RegistryError(f"{label}.snapshot.{field} must be YYYY-MM-DD")
            if snapshot["fielded_from"] > snapshot["fielded_to"]:
                raise RegistryError(f"{label}.snapshot fielded_from must not follow fielded_to")
            if snapshot["captured_at"] < snapshot["fielded_to"]:
                raise RegistryError(f"{label}.snapshot captured_at must not precede fielding")
            if not snapshot["source_url"].startswith("https://") or not snapshot["publication_url"].startswith("https://"):
                raise RegistryError(f"{label}.snapshot source URLs must be https URLs")
            distribution = snapshot.get("distribution")
            value = snapshot.get("value")
            if distribution is None and value is None:
                raise RegistryError(f"{label}.snapshot must record a value or distribution")
            if distribution is not None:
                if not isinstance(distribution, dict) or not isinstance(distribution.get("unit"), str):
                    raise RegistryError(f"{label}.snapshot.distribution must declare a unit")
                buckets = distribution.get("buckets", distribution.get("values"))
                if not isinstance(buckets, dict) or not buckets:
                    raise RegistryError(f"{label}.snapshot.distribution must have non-empty buckets or values")
                if not all(isinstance(bucket, str) and isinstance(amount, (int, float)) and amount >= 0 for bucket, amount in buckets.items()):
                    raise RegistryError(f"{label}.snapshot.distribution values must be named, non-negative numbers")
                if distribution["unit"] == "percent" and any(amount > 100 for amount in buckets.values()):
                    raise RegistryError(f"{label}.snapshot.distribution percentages must be at most 100")
                if distribution["unit"] == "percent" and abs(sum(buckets.values()) - 100) > 0.01:
                    raise RegistryError(f"{label}.snapshot.distribution percentages must sum to 100")
            if not all(link.get("match") == "exact" for link in links):
                raise RegistryError(f"{label} verified snapshots require exact canonical-question matches")
        else:
            raise RegistryError(f"{label}.status must be registered-no-snapshot or verified-snapshot")


def _validate_ai_rd_evidence(
    evidence: dict[str, Any], source_ids: set[str], question_ids: set[str]
) -> str:
    """Validate the non-scoreable evidence package for the AI R&D feedback question.

    This file deliberately records unlike empirical material side by side.  Its
    labels make it impossible for a renderer to mistake a benchmark, survey, or
    company disclosure for independently verified AI-R&D acceleration.
    """
    _require_strings(evidence, ("id", "question_id"), "AI R&D evidence package")
    if evidence["question_id"] != "ai-rd-feedback" or evidence["question_id"] not in question_ids:
        raise RegistryError("AI R&D evidence package must belong to the ai-rd-feedback question")
    synthesis = evidence.get("current_synthesis")
    if not isinstance(synthesis, dict):
        raise RegistryError("AI R&D evidence package.current_synthesis must be an object")
    _require_strings(
        synthesis,
        ("as_of", "status", "reading", "strongest_direct_evidence", "strongest_counterevidence", "measurement_gap"),
        "AI R&D evidence package.current_synthesis",
    )
    if not DATE.fullmatch(synthesis["as_of"]):
        raise RegistryError("AI R&D evidence package.current_synthesis.as_of must be YYYY-MM-DD")
    if synthesis["status"] not in AI_RD_SYNTHESIS_STATUSES:
        raise RegistryError("AI R&D evidence package.current_synthesis.status is invalid")

    observations = _items(evidence, "observations", "ai-rd-evidence.json")
    _unique_ids(observations, "AI R&D evidence observation")
    for observation in observations:
        label = f"AI R&D evidence observation {observation['id']}"
        _require_strings(
            observation,
            ("date", "title", "evidence_kind", "directness", "direction", "finding", "source_id", "caveat"),
            label,
        )
        if not DATE.fullmatch(observation["date"]):
            raise RegistryError(f"{label}.date must be YYYY-MM-DD")
        if observation["evidence_kind"] not in AI_RD_EVIDENCE_KINDS:
            raise RegistryError(f"{label}.evidence_kind is invalid")
        if observation["directness"] not in AI_RD_DIRECTNESS:
            raise RegistryError(f"{label}.directness is invalid")
        if observation["direction"] not in AI_RD_DIRECTIONS:
            raise RegistryError(f"{label}.direction is invalid")
        if observation["source_id"] not in source_ids:
            raise RegistryError(f"{label}.source_id references an unknown source")
        source = observation.get("source")
        if not isinstance(source, dict):
            raise RegistryError(f"{label}.source must be an object")
        _require_strings(source, ("artifact", "publisher", "published_on", "url"), f"{label}.source")
        if not DATE.fullmatch(source["published_on"]):
            raise RegistryError(f"{label}.source.published_on must be YYYY-MM-DD")
        if not source["url"].startswith("https://"):
            raise RegistryError(f"{label}.source.url must be an https URL")
        question_link = observation.get("question_link")
        if not isinstance(question_link, dict):
            raise RegistryError(f"{label}.question_link must be an object")
        if question_link.get("question_id") != evidence["question_id"]:
            raise RegistryError(f"{label}.question_link must point to ai-rd-feedback")
        if question_link.get("relation") not in AI_RD_RELATIONS:
            raise RegistryError(f"{label}.question_link.relation is invalid")
        if observation["evidence_kind"] == "benchmark-evaluation" and observation["directness"] != "benchmark-only":
            raise RegistryError(f"{label} benchmark evaluations must be benchmark-only")
        if observation["directness"] == "benchmark-only" and observation["evidence_kind"] != "benchmark-evaluation":
            raise RegistryError(f"{label} is benchmark-only but is not labelled benchmark-evaluation")
        if observation["evidence_kind"] == "technical-worker-survey" and observation["directness"] != "self-report-only":
            raise RegistryError(f"{label} technical-worker surveys must be self-report-only")
        if observation["directness"] == "self-report-only" and observation["evidence_kind"] != "technical-worker-survey":
            raise RegistryError(f"{label} is self-report-only but is not labelled technical-worker-survey")
        if observation["evidence_kind"] in {"company-operational-report", "company-deployment-report"} and observation["directness"] != "company-report-with-direct-relevance":
            raise RegistryError(f"{label} company reports must be company-report-with-direct-relevance")
        if observation["evidence_kind"] == "company-autonomous-research-demo" and observation["directness"] != "company-reported-autonomous-demo":
            raise RegistryError(f"{label} autonomous-research demos must be company-reported-autonomous-demo")
    return evidence["id"]


def _validate_safety_questions(data: dict[str, Any]) -> set[str]:
    _require_strings(data, ("scope", "framework", "headline_reading"), "safety-questions.json")
    questions = _items(data, "questions", "safety-questions.json")
    question_ids = _unique_ids(questions, "safety question")
    for question in questions:
        label = f"safety question {question['id']}"
        _require_strings(
            question,
            ("stage", "title", "question", "visual_type", "measurement_state", "current_reading", "reading_as_of"),
            label,
        )
        if question["stage"] not in SAFETY_STAGES:
            raise RegistryError(f"{label}.stage is invalid")
        if question["visual_type"] not in SAFETY_VISUAL_TYPES:
            raise RegistryError(f"{label}.visual_type is invalid")
        if question["measurement_state"] not in SAFETY_MEASUREMENT_STATES:
            raise RegistryError(f"{label}.measurement_state is invalid")
        if not DATE.fullmatch(question["reading_as_of"]):
            raise RegistryError(f"{label}.reading_as_of must be YYYY-MM-DD")
        quality = question.get("evidence_quality")
        if not isinstance(quality, dict):
            raise RegistryError(f"{label}.evidence_quality must be an object")
        _require_strings(quality, ("setting", "independence", "coverage"), f"{label}.evidence_quality")
        for field in ("indicators", "gaps", "movers"):
            values = question.get(field)
            if not isinstance(values, list) or not values or not all(isinstance(value, str) and value.strip() for value in values):
                raise RegistryError(f"{label}.{field} must be a non-empty string array")
        evidence = question.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise RegistryError(f"{label}.evidence must be a non-empty array")
        for index, item in enumerate(evidence):
            evidence_label = f"{label}.evidence[{index}]"
            _require_strings(
                item,
                ("date", "observed_period", "finding", "measurement", "source_label", "source_url", "source_type", "independence", "caveat"),
                evidence_label,
            )
            if not DATE.fullmatch(item["date"]):
                raise RegistryError(f"{evidence_label}.date must be YYYY-MM-DD")
            if not item["source_url"].startswith("https://"):
                raise RegistryError(f"{evidence_label}.source_url must be https")
            if item["source_type"] not in SAFETY_SOURCE_TYPES:
                raise RegistryError(f"{evidence_label}.source_type is invalid")
        visual_type = question["visual_type"]
        if visual_type == "spectrum":
            for pole in ("pole_a", "pole_b"):
                if not isinstance(question.get(pole), dict):
                    raise RegistryError(f"{label}.{pole} must be an object")
                _require_strings(question[pole], ("label", "desc"), f"{label}.{pole}")
            lean = question.get("lean")
            if not isinstance(lean, (int, float)) or isinstance(lean, bool) or not -1 <= lean <= 1:
                raise RegistryError(f"{label}.lean must be from -1 to 1")
            if question.get("range") not in SAFETY_RANGES:
                raise RegistryError(f"{label}.range is invalid")
        elif visual_type == "domain-matrix":
            domains = question.get("domains")
            if not isinstance(domains, list) or len(domains) < 2:
                raise RegistryError(f"{label}.domains must have at least two domains")
            for domain in domains:
                _require_strings(domain, ("label", "state", "reading"), f"{label}.domain")
                if domain["state"] not in {"limited", "emerging", "material-signal"}:
                    raise RegistryError(f"{label}.domain.state is invalid")
        elif visual_type == "exposure-ladder":
            ladder = question.get("ladder")
            if not isinstance(ladder, list) or len(ladder) < 3:
                raise RegistryError(f"{label}.ladder must have at least three levels")
            levels = []
            for level in ladder:
                _require_strings(level, ("label", "desc"), f"{label}.ladder")
                if not isinstance(level.get("level"), int):
                    raise RegistryError(f"{label}.ladder levels must be integers")
                levels.append(level["level"])
            if levels != sorted(levels) or len(levels) != len(set(levels)):
                raise RegistryError(f"{label}.ladder levels must be unique and ascending")
            current_level = question.get("current_level")
            if current_level is not None and current_level not in levels:
                raise RegistryError(f"{label}.current_level must reference a ladder level or be null")
        elif visual_type == "incident-ledger":
            incidents = question.get("incidents")
            if not isinstance(incidents, list) or not incidents:
                raise RegistryError(f"{label}.incidents must be a non-empty array")
            for incident in incidents:
                _require_strings(incident, ("date", "domain", "severity", "ai_role", "reading", "attribution"), f"{label}.incident")
    return question_ids


def load_research_registry(root: Path = ROOT) -> dict[str, Any]:
    """Load and validate the registry; suitable for a future renderer or build hook."""
    research = root / "data" / "research"
    scoreboard = root / "data" / "scoreboard"
    questions_data = _load(research / "questions.json")
    sources_data = _load(research / "sources.json")
    evidence_data = _load(research / "evidence-map.json")
    aggregates_data = _load(research / "aggregate-signals.json")
    ai_rd_evidence_data = _load(research / "ai-rd-evidence.json")
    safety_questions_data = _load(research / "safety-questions.json")
    metrics = _load_existing(scoreboard / "metrics.json").get("metrics")
    claims_data = _load_existing(scoreboard / "claims.json")
    cruxes = _load_existing(root / "data" / "cruxes.json").get("cruxes")
    if not isinstance(metrics, list) or not isinstance(cruxes, list):
        raise RegistryError("Referenced tracker metric or crux collection is malformed")
    metric_ids = _unique_ids(metrics, "scoreboard metric")
    crux_ids = _unique_ids(cruxes, "crux")
    scoreboard_source_ids = _unique_ids(claims_data["forecast_sources"], "scoreboard forecast source")
    safety_question_ids = _validate_safety_questions(safety_questions_data)
    question_ids = _validate_questions(
        _items(questions_data, "questions", "questions.json"), metric_ids, crux_ids, safety_question_ids
    )
    source_ids = _validate_sources(
        _items(sources_data, "dependency_clusters", "sources.json"),
        _items(sources_data, "sources", "sources.json"),
        scoreboard_source_ids,
    )
    ai_rd_evidence_id = _validate_ai_rd_evidence(ai_rd_evidence_data, source_ids, question_ids)
    _validate_evidence_links(
        _items(evidence_data, "links", "evidence-map.json"),
        question_ids,
        metric_ids,
        crux_ids,
        {ai_rd_evidence_id},
    )
    aggregate_source_ids = {
        source["id"] for source in sources_data["sources"] if source.get("lane") == "aggregate"
    }
    _validate_aggregate_signals(
        _items(aggregates_data, "signals", "aggregate-signals.json"),
        source_ids,
        aggregate_source_ids,
        question_ids,
    )
    return {
        "questions": questions_data,
        "sources": sources_data,
        "evidence": evidence_data,
        "aggregates": aggregates_data,
        "ai_rd_evidence": ai_rd_evidence_data,
        "safety_questions": safety_questions_data,
    }


def main() -> int:
    try:
        registry = load_research_registry()
    except RegistryError as exc:
        print(f"Research registry validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "Validated research registry: "
        f"{len(registry['questions']['questions'])} questions, "
        f"{len(registry['sources']['sources'])} sources, "
        f"{len(registry['evidence']['links'])} evidence links, "
        f"{len(registry['aggregates']['signals'])} aggregate signal registrations, "
        f"{len(registry['ai_rd_evidence']['observations'])} AI R&D evidence observations, "
        f"{len(registry['safety_questions']['questions'])} safety questions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
