"""Summarize completed experiment repetitions across API targets.

Usage: ``python scripts/experiments/analyze_final.py EXPERIMENT_ROOT EXPECTED_COMMIT``

The root is expected to contain ``<api>/<run-id>/run_manifest.json`` folders.
This tool reads the finalized run artifacts; it does not modify them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from fuzzer.analysis.deduplication import (
    EXPECTED_CLASSIFICATION,
    build_signature,
)
from fuzzer.analysis.run_postprocessor import correlate_records
from fuzzer.parser.openapi_parser import parse_openapi

RUN_COUNT = 5
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
REQUIRED_ARTIFACTS = {
    "run_manifest.json",
    "data/execution_plan.json",
    "data/results.json",
    "analysis/analysis_findings.json",
    "analysis/analysis_report.md",
    "analysis/findings_unique.json",
    "analysis/metrics.json",
    "analysis/deduplication_report.md",
}
REQUIRED_CONFIGURATION = {
    "level": 2,
    "max_mutations_per_payload": 20,
    "max_pairs_per_payload": 10,
    "endpoint_limit": None,
    "path_filter": None,
    "concurrency": 1,
    "delay_ms": 250,
    "timeout_seconds": 10,
    "all_endpoints": True,
    "deduplicate": False,
}


class InvalidCampaign(ValueError):
    """A run does not satisfy the expected experiment protocol."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise InvalidCampaign(f"cannot read {path}: {error}") from error


def require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InvalidCampaign(f"{label} must be an object")
    return value


def require_records(path: Path) -> list[dict[str, Any]]:
    value = read_json(path)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise InvalidCampaign(f"{path} must contain a list of objects")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contract_path(run_dir: Path, inputs: dict[str, Any]) -> Path:
    schema = inputs.get("schema")
    if not isinstance(schema, str):
        raise InvalidCampaign(f"{run_dir}: missing contract path")
    recorded = Path(schema)
    for path in (recorded, run_dir / recorded, run_dir / "data/target_contract.json"):
        if path.is_file():
            return path
    raise InvalidCampaign(f"{run_dir}: contract unavailable for hash validation")


def artifact_hashes(run_dir: Path, manifest: dict[str, Any]) -> dict[str, str]:
    listed = manifest.get("artifacts")
    if not isinstance(listed, list) or not all(isinstance(x, str) for x in listed):
        raise InvalidCampaign(f"{run_dir}: invalid artifact list")
    if len(listed) != len(set(listed)) or not REQUIRED_ARTIFACTS <= set(listed):
        raise InvalidCampaign(f"{run_dir}: incomplete or duplicate artifact list")
    hashes = {}
    for name in listed:
        path = run_dir / name
        if run_dir.resolve() not in path.resolve().parents or not path.is_file():
            raise InvalidCampaign(f"{run_dir}: missing or unsafe artifact {name!r}")
        hashes[name] = digest(path)
    return hashes


def validate_run(run_dir: Path, api: str, commit: str) -> dict[str, Any]:
    manifest = require_dict(read_json(run_dir / "run_manifest.json"), "manifest")
    if manifest.get("target_id") != api or manifest.get("run_id") != run_dir.name:
        raise InvalidCampaign(f"{run_dir}: target or run identity mismatch")
    number = manifest.get("run_number")
    if (
        not isinstance(number, int)
        or isinstance(number, bool)
        or number not in range(1, RUN_COUNT + 1)
    ):
        raise InvalidCampaign(
            f"{run_dir}: run_number must be between 1 and {RUN_COUNT}"
        )
    if manifest.get("status") != "completed" or manifest.get("error") is not None:
        raise InvalidCampaign(f"{run_dir}: run is not completed cleanly")
    if not manifest.get("finished_at") or not manifest.get("started_at"):
        raise InvalidCampaign(f"{run_dir}: missing run timestamps")

    inputs = require_dict(manifest.get("inputs"), f"{run_dir}: inputs")
    fuzzer = require_dict(manifest.get("fuzzer"), f"{run_dir}: fuzzer")
    git_state = require_dict(fuzzer.get("git"), f"{run_dir}: fuzzer.git")
    if git_state.get("commit") != commit or git_state.get("dirty") is not False:
        raise InvalidCampaign(f"{run_dir}: expected clean commit {commit}")
    config = require_dict(fuzzer.get("configuration"), f"{run_dir}: configuration")
    if any(config.get(key) != value for key, value in REQUIRED_CONFIGURATION.items()):
        raise InvalidCampaign(f"{run_dir}: required configuration mismatch")

    postprocessing = require_dict(
        manifest.get("postprocessing"), f"{run_dir}: postprocessing"
    )
    deduplication = require_dict(
        postprocessing.get("deduplication"), f"{run_dir}: deduplication"
    )
    if deduplication.get("status") != "completed":
        raise InvalidCampaign(f"{run_dir}: deduplication is not completed")
    if not inputs.get("schema_sha256") or not inputs.get("target_image"):
        raise InvalidCampaign(f"{run_dir}: missing target provenance")
    if not fuzzer.get("source_tree_sha256"):
        raise InvalidCampaign(f"{run_dir}: missing source provenance")

    hashes = artifact_hashes(run_dir, manifest)
    schema_file = contract_path(run_dir, inputs)
    if digest(schema_file) != inputs["schema_sha256"]:
        raise InvalidCampaign(f"{run_dir}: contract hash mismatch")
    import yaml

    contract = require_dict(
        yaml.safe_load(schema_file.read_text(encoding="utf-8")), f"{run_dir}: contract"
    )
    paths = require_dict(contract.get("paths"), f"{run_dir}: contract paths")
    total_operations = sum(
        method.lower() in HTTP_METHODS
        for path_item in paths.values()
        for method in require_dict(path_item, f"{run_dir}: path item")
    )
    supported_operations = len(parse_openapi(str(schema_file)).endpoints)

    plans = require_records(run_dir / "data/execution_plan.json")
    results = require_records(run_dir / "data/results.json")
    findings = require_records(run_dir / "analysis/analysis_findings.json")
    unique = require_records(run_dir / "analysis/findings_unique.json")
    correlated = correlate_records(plans, results, findings)
    metrics = require_dict(
        read_json(run_dir / "analysis/metrics.json"), f"{run_dir}: metrics"
    )
    counts = require_dict(metrics.get("counts"), f"{run_dir}: metric counts")
    manifest_counts = require_dict(manifest.get("counts"), f"{run_dir}: counts")
    expected_count = sum(
        item.get("classification") == EXPECTED_CLASSIFICATION for item in findings
    )
    actual = (
        len(plans),
        len(results),
        len(findings),
        expected_count,
        len(findings) - expected_count,
        len(unique),
    )
    keys = (
        "planned_requests",
        "executed_requests",
        "classified_observations",
        "expected_failures",
        "candidate_findings_raw",
        "findings_unique_operational",
    )
    if tuple(counts.get(key) for key in keys) != actual:
        raise InvalidCampaign(f"{run_dir}: metrics counts do not match run artifacts")
    if (
        manifest_counts.get("planned_requests") != len(plans)
        or manifest_counts.get("completed_requests") != len(results)
        or manifest_counts.get("findings") != len(findings)
        or deduplication.get("counts") != counts
    ):
        raise InvalidCampaign(f"{run_dir}: manifest/postprocessing counts mismatch")

    selected = manifest_counts.get("selected_endpoints")
    if not isinstance(selected, int) or isinstance(selected, bool) or selected < 1:
        raise InvalidCampaign(f"{run_dir}: no operations were selected for testing")
    if selected != len({item["endpoint_id"] for item in plans}):
        raise InvalidCampaign(f"{run_dir}: selected operation count mismatch")
    if selected > supported_operations:
        raise InvalidCampaign(f"{run_dir}: selected operations exceed parser support")

    classes = Counter(
        item.get("classification")
        for item in findings
        if item.get("classification") != EXPECTED_CLASSIFICATION
    )
    if dict(classes) != metrics.get("candidate_by_classification"):
        raise InvalidCampaign(f"{run_dir}: candidate classification counts mismatch")

    buckets: dict[str, set[str]] = {}
    for item in unique:
        signature = require_dict(item.get("signature"), f"{run_dir}: signature")
        signature_id = signature.get("id")
        cases = item.get("case_ids")
        if (
            not isinstance(signature_id, str)
            or signature_id in buckets
            or not isinstance(cases, list)
            or not cases
            or len(cases) != len(set(cases))
            or item.get("occurrence_count") != len(cases)
        ):
            raise InvalidCampaign(f"{run_dir}: invalid deduplication bucket")
        buckets[signature_id] = set(cases)

    computed: dict[str, set[str]] = defaultdict(set)
    by_case = {item.case_id: item for item in correlated}
    for item in correlated:
        if item.finding["classification"] != EXPECTED_CLASSIFICATION:
            computed[build_signature(api, item)["id"]].add(item.case_id)
    if dict(computed) != buckets:
        raise InvalidCampaign(f"{run_dir}: signature/case mapping mismatch")
    for item in unique:
        representative = require_dict(
            item.get("representative"), f"{run_dir}: representative"
        )
        case_id = representative.get("plan", {}).get("case_id")
        if case_id not in buckets[item["signature"]["id"]]:
            raise InvalidCampaign(f"{run_dir}: representative outside bucket")
        if item["signature"] != build_signature(api, by_case[case_id]):
            raise InvalidCampaign(f"{run_dir}: signature differs from representative")

    return {
        "manifest": manifest,
        "metrics": metrics,
        "unique": unique,
        "configuration": config,
        "artifact_sha256": hashes,
        "contract_operations": total_operations,
        "supported_operations": supported_operations,
    }


def discover_apis(root: Path) -> dict[str, list[Path]]:
    if not root.is_dir():
        raise InvalidCampaign(f"experiment root is not a directory: {root}")
    apis = {}
    for api_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        runs = sorted(
            path
            for path in api_dir.iterdir()
            if path.is_dir() and (path / "run_manifest.json").is_file()
        )
        if runs:
            apis[api_dir.name] = runs
    if not apis:
        raise InvalidCampaign(f"no API run directories found under {root}")
    return apis


def validate_api(api: str, run_dirs: list[Path], commit: str) -> list[dict[str, Any]]:
    if len(run_dirs) != RUN_COUNT:
        raise InvalidCampaign(
            f"{api}: expected exactly {RUN_COUNT} runs, found {len(run_dirs)}"
        )
    runs = [validate_run(path, api, commit) for path in run_dirs]
    numbers = [run["manifest"]["run_number"] for run in runs]
    if sorted(numbers) != list(range(1, RUN_COUNT + 1)):
        raise InvalidCampaign(
            f"{api}: repetitions must be numbered 1 through {RUN_COUNT}"
        )
    runs.sort(key=lambda run: run["manifest"]["run_number"])
    versions = {
        (
            run["manifest"].get("experiment_id"),
            run["manifest"]["target_id"],
            run["manifest"]["inputs"].get("schema_sha256"),
            run["manifest"]["inputs"].get("target_image"),
            run["manifest"]["fuzzer"].get("source_tree_sha256"),
        )
        for run in runs
    }
    configurations = {json.dumps(run["configuration"], sort_keys=True) for run in runs}
    if len(versions) != 1:
        raise InvalidCampaign(f"{api}: campaign metadata differs across runs")
    if len(configurations) != 1:
        raise InvalidCampaign(f"{api}: configuration differs across runs")
    return runs


def select_valid_attempts(
    api: str, run_dirs: list[Path], commit: str
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Retain invalid attempts while accepting exactly five complete campaigns."""
    valid, invalid = [], []
    for path in run_dirs:
        try:
            valid.append(validate_run(path, api, commit))
        except (InvalidCampaign, ValueError, KeyError, TypeError) as error:
            invalid.append({"run_id": path.name, "reason": str(error)})
    return validate_api(
        api,
        [
            path
            for path in run_dirs
            if path.name in {run["manifest"]["run_id"] for run in valid}
        ],
        commit,
    ), invalid


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


def summarize(api: str, runs: list[dict[str, Any]]) -> dict[str, Any]:
    observations: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    origins: dict[str, list[dict[str, str]]] = defaultdict(list)
    totals, classifications = Counter(), Counter()
    strict_scores, strict_bands = [], Counter()
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

        for item in run["unique"]:
            strict_finding = item["representative"]["finding"]
            strict_score = strict_finding.get("severity_score")
            if isinstance(strict_score, (int, float)):
                strict_scores.append(float(strict_score))
            strict_bands[strict_finding.get("severity", "UNKNOWN")] += 1

            key = semantic_id(item, api)
            current = observations[key].get(number)
            if current is None or item["signature"]["id"] < current["signature"]["id"]:
                observations[key][number] = item

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
        for item in by_run.values():
            finding = item["representative"]["finding"]
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
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only summary of five finalized repetitions for every API "
            "under an experiment root."
        )
    )
    parser.add_argument(
        "experiment_root",
        type=Path,
        help="Root containing <api>/<run-id>/run_manifest.json",
    )
    parser.add_argument("expected_commit", help="Expected clean fuzzer commit")
    args = parser.parse_args(argv)
    try:
        audited = {
            api: select_valid_attempts(api, paths, args.expected_commit)
            for api, paths in discover_apis(args.experiment_root).items()
        }
        validated = {api: runs for api, (runs, _) in audited.items()}
        experiment_ids = {
            run["manifest"].get("experiment_id")
            for runs in validated.values()
            for run in runs
        }
        source_hashes = {
            run["manifest"]["fuzzer"].get("source_tree_sha256")
            for runs in validated.values()
            for run in runs
        }
        if len(experiment_ids) != 1 or len(source_hashes) != 1:
            raise InvalidCampaign("experiment or fuzzer source differs across APIs")

        summaries = {}
        for api, runs in validated.items():
            summaries[api] = summarize(api, runs)
            summaries[api]["invalid_attempts"] = audited[api][1]
        print(json.dumps(summaries, indent=2, ensure_ascii=False))
    except (InvalidCampaign, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
