"""Calculate campaign and cross-run descriptive metrics."""

from __future__ import annotations

import hashlib
import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any

from fuzzer.analysis.deduplication import EXPECTED_CLASSIFICATION

from .protocol import InvalidCampaign, RUN_COUNT

SCIENTIFIC_FIELDS = (
    "api_id",
    "run_ids",
    "totals",
    "candidate_by_classification",
    "deduplication_reduction",
    "signature_union",
    "presence_frequency",
    "reobserved_at_least_four_ratio",
    "observed_once_ratio",
    "signatures_with_band_change",
    "strict_signatures_with_mixed_bands",
    "fis_inputs_with_different_scores",
    "score_distribution_unique_per_run",
    "band_distribution_unique_per_run",
    "signatures",
    "configuration",
)


CAMPAIGN_SCIENTIFIC_FIELDS = (
    "run_id",
    "run_number",
    "selected_operations",
    "contract_operations",
    "supported_operations",
    "duration_seconds",
    "counts",
    "http_status_classes",
)


def normalize_meilisearch_response(response: str) -> str | None:
    try:
        value = json.loads(response)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(value, dict):
        return None

    def normalize(node: Any) -> Any:
        if isinstance(node, dict):
            return {
                key: "<VARIABLE>"
                if key in {"requestUid", "processingTimeMs"}
                else normalize(child)
                for key, child in node.items()
            }
        if isinstance(node, list):
            return [normalize(child) for child in node]
        return node

    return json.dumps(
        normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def semantic_id(item: dict[str, Any], api: str) -> str:
    components = dict(item["signature"]["components"])
    if api == "meilisearch" and components["endpoint_id"] == "POST /multi-search":
        normalized = normalize_meilisearch_response(
            item["signature"].get("normalized_response")
        )
        if normalized is not None:
            components["normalized_response_sha256"] = hashlib.sha256(
                normalized.encode()
            ).hexdigest()
    canonical = json.dumps(components, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def timestamp(value: str, run_id: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as error:
        raise InvalidCampaign(f"{run_id}: invalid timestamp") from error


def fis_score(finding: dict[str, Any]) -> float:
    score = finding.get("severity_score")
    return float(score) if isinstance(score, (int, float)) else float("-inf")


def summarize(api: str, runs: list[dict[str, Any]]) -> dict[str, Any]:
    observations: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    # FIS finding that gives each selected strict signature its score.
    top_findings: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    origins: dict[str, list[dict[str, str]]] = defaultdict(list)
    totals, classifications = Counter(), Counter()
    strict_scores, strict_bands = [], Counter()
    # A strict signature groups by response while the FIS also scores the
    # request, so its cases may differ in band. A signature takes the highest
    # score among its cases; the FIS must give one output per input combination.
    mixed_bands, fis_outputs = 0, defaultdict(set)
    campaigns = []
    for run in runs:
        manifest, metrics = run["manifest"], run["metrics"]
        number, run_id = manifest["run_number"], manifest["run_id"]
        counts = metrics["counts"]
        campaigns.append(
            {
                "run_id": run_id,
                "run_number": number,
                "selected_operations": manifest["counts"].get("selected_endpoints"),
                "contract_operations": run["contract_operations"],
                "supported_operations": run["supported_operations"],
                "duration_seconds": (
                    timestamp(manifest["finished_at"], run_id)
                    - timestamp(manifest["started_at"], run_id)
                ).total_seconds(),
                "counts": counts,
                "http_status_classes": metrics.get("executed_by_http_status_class", {}),
                "artifact_sha256": run["artifact_sha256"],
            }
        )
        for key in (
            "planned_requests",
            "executed_requests",
            "classified_observations",
            "expected_failures",
            "candidate_findings_raw",
            "findings_unique_operational",
        ):
            totals[key] += counts[key]

        classifications.update(metrics.get("candidate_by_classification", {}))

        findings_by_case = {}
        for finding in run["findings"]:
            if finding.get("classification") == EXPECTED_CLASSIFICATION:
                continue
            findings_by_case[finding["case_id"]] = finding
            inputs = (finding.get("severity_assessment") or {}).get("inputs")
            fis_outputs[json.dumps(inputs, sort_keys=True)].add(
                (finding.get("severity_score"), finding.get("severity"))
            )

        for item in run["unique"]:
            cases = [findings_by_case[case] for case in item["case_ids"]]
            mixed_bands += len({case.get("severity") for case in cases}) > 1
            strict_finding = max(cases, key=fis_score)
            strict_score = strict_finding.get("severity_score")
            if isinstance(strict_score, (int, float)):
                strict_scores.append(float(strict_score))
            strict_bands[strict_finding.get("severity", "UNKNOWN")] += 1

            key = semantic_id(item, api)
            current = observations[key].get(number)
            if current is None or item["signature"]["id"] < current["signature"]["id"]:
                observations[key][number] = item
                top_findings[key][number] = strict_finding

            origins[key].append(
                {
                    "run_id": run_id,
                    "strict_signature": item["signature"]["id"],
                    "case_id": item["representative"]["plan"]["case_id"],
                }
            )

    scores, response_times, bands = (
        defaultdict(list),
        defaultdict(list),
        defaultdict(set),
    )
    for key, by_run in observations.items():
        for number, item in by_run.items():
            finding = top_findings[key][number]
            result = item["representative"]["result"]
            response_time, score = (
                result.get("response_time_ms"),
                finding.get("severity_score"),
            )
            if isinstance(response_time, (int, float)) and response_time >= 0:
                response_times[key].append(float(response_time))
            if isinstance(score, (int, float)):
                scores[key].append(float(score))
            band = finding.get("severity", "UNKNOWN")
            bands[key].add(band)

    frequencies = Counter(len(by_run) for by_run in observations.values())
    union, raw, unique_count = (
        len(observations),
        totals["candidate_findings_raw"],
        totals["findings_unique_operational"],
    )
    return {
        "api_id": api,
        "campaigns": campaigns,
        "run_ids": [run["manifest"]["run_id"] for run in runs],
        "totals": dict(totals),
        "candidate_by_classification": dict(sorted(classifications.items())),
        "deduplication_reduction": (raw - unique_count) / raw if raw else 0.0,
        "signature_union": union,
        "presence_frequency": {str(n): frequencies[n] for n in range(1, RUN_COUNT + 1)},
        "reobserved_at_least_four_ratio": (frequencies[4] + frequencies[5]) / union
        if union
        else None,
        "observed_once_ratio": frequencies[1] / union if union else None,
        "signatures_with_band_change": sum(len(value) > 1 for value in bands.values()),
        "strict_signatures_with_mixed_bands": mixed_bands,
        "fis_inputs_with_different_scores": sum(
            len(outputs) > 1 for outputs in fis_outputs.values()
        ),
        "score_distribution_unique_per_run": {
            "count": len(strict_scores),
            "median": statistics.median(strict_scores) if strict_scores else None,
            "min": min(strict_scores) if strict_scores else None,
            "max": max(strict_scores) if strict_scores else None,
        },
        "band_distribution_unique_per_run": dict(sorted(strict_bands.items())),
        "signatures": {
            key: {
                "present_in": sorted(observations[key]),
                "score_range": [min(scores[key]), max(scores[key])]
                if scores[key]
                else None,
                "score_stdev": statistics.pstdev(scores[key]) if scores[key] else None,
                "response_time_cv": statistics.pstdev(response_times[key])
                / statistics.mean(response_times[key])
                if response_times[key] and statistics.mean(response_times[key]) > 0
                else None,
                "bands": sorted(bands[key]),
                "origins": origins[key],
            }
            for key in sorted(observations)
        },
        # check_campaign guarantees the five runs share one configuration.
        "configuration": runs[0]["configuration"] if runs else None,
    }


def require_scientific_parity(
    source: dict[str, dict[str, Any]], exported: dict[str, dict[str, Any]]
) -> None:
    """Compare every study result; file hashes and invalid attempts are provenance."""
    if set(source) != set(exported):
        raise InvalidCampaign("review bundle API set differs from source experiment")
    for api in source:
        for field in SCIENTIFIC_FIELDS:
            if source[api][field] != exported[api][field]:
                raise InvalidCampaign(f"{api}: review bundle changed {field}")
        source_runs = source[api]["campaigns"]
        exported_runs = exported[api]["campaigns"]
        if len(source_runs) != len(exported_runs):
            raise InvalidCampaign(f"{api}: review bundle changed campaign count")
        for source_run, exported_run in zip(source_runs, exported_runs, strict=True):
            for field in CAMPAIGN_SCIENTIFIC_FIELDS:
                if source_run[field] != exported_run[field]:
                    raise InvalidCampaign(
                        f"{api}: review bundle changed campaign {field}"
                    )


def illustrative_signatures(
    signatures: dict[str, dict[str, Any]],
) -> list[tuple[str, dict[str, Any]]]:
    """Use the existing lexical semantic-ID rule for 5/5 and 1/5 examples."""
    selected = []
    for frequency in (5, 1):
        candidates = sorted(
            (signature_id, item)
            for signature_id, item in signatures.items()
            if len(item["present_in"]) == frequency
        )
        if candidates:
            selected.append(candidates[0])
    if not selected and signatures:
        selected.append(sorted(signatures.items())[0])
    return selected
