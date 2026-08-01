from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from fuzzer.analysis.deduplication import (
    EXPECTED_CLASSIFICATION,
    CorrelatedFinding,
    deduplicate_findings,
)


class CorrelationError(ValueError):
    """Raised when raw run artifacts cannot be joined safely."""


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CorrelationError(f"cannot read {path}: {error}") from error


def _load_records(path: Path) -> list[dict[str, Any]]:
    value = _load_json(path)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise CorrelationError(f"{path} must contain a JSON list of objects")
    return value


def _index(
    records: list[dict[str, Any]], artifact_name: str
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(records):
        case_id = record.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise CorrelationError(
                f"{artifact_name}[{position}] has no valid case_id"
            )
        if case_id in indexed:
            raise CorrelationError(
                f"duplicate case_id {case_id!r} in {artifact_name}"
            )
        indexed[case_id] = record
    return indexed


def correlate_records(
    plans: list[dict[str, Any]],
    results: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> list[CorrelatedFinding]:
    plan_by_id = _index(plans, "execution_plan.json")
    result_by_id = _index(results, "results.json")
    finding_by_id = _index(findings, "analysis_findings.json")
    if plan_by_id.keys() != result_by_id.keys():
        raise CorrelationError(
            "plan/result case_id mismatch: "
            f"missing results={sorted(plan_by_id.keys() - result_by_id.keys())}; "
            f"missing plans={sorted(result_by_id.keys() - plan_by_id.keys())}"
        )
    unknown = sorted(finding_by_id.keys() - plan_by_id.keys())
    if unknown:
        raise CorrelationError(f"findings without plan/result records: {unknown}")

    correlated: list[CorrelatedFinding] = []
    for case_id in sorted(finding_by_id):
        item = CorrelatedFinding(
            plan=plan_by_id[case_id],
            result=result_by_id[case_id],
            finding=finding_by_id[case_id],
        )
        _validate_consistency(item)
        correlated.append(item)
    return correlated


def _validate_consistency(item: CorrelatedFinding) -> None:
    endpoints = {
        item.plan.get("endpoint_id"),
        item.result.get("endpoint_id"),
        item.finding.get("endpoint_id"),
    }
    if len(endpoints) != 1:
        values = sorted(str(value) for value in endpoints)
        raise CorrelationError(
            f"inconsistent endpoint_id for {item.case_id}: {values}"
        )
    if item.finding.get("status_code") != item.result.get("status_code"):
        raise CorrelationError(f"inconsistent status_code for {item.case_id}")
    if item.finding.get("request_payload") != item.plan.get("payload"):
        raise CorrelationError(f"inconsistent request payload for {item.case_id}")


def _build_metrics(
    api_id: str,
    plans: list[dict[str, Any]],
    results: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    unique: list[dict[str, Any]],
) -> dict[str, Any]:
    raw_classes = Counter(item["classification"] for item in findings)
    candidate_classes = Counter(
        item["classification"]
        for item in findings
        if item["classification"] != EXPECTED_CLASSIFICATION
    )
    unique_classes = Counter(
        item["signature"]["components"]["classification"] for item in unique
    )
    status_classes = Counter(
        "network_error"
        if item.get("status_code") is None
        else f"{int(item['status_code']) // 100}xx"
        for item in results
    )
    expected = raw_classes[EXPECTED_CLASSIFICATION]
    return {
        "api_id": api_id,
        "counts": {
            "planned_requests": len(plans),
            "executed_requests": len(results),
            "classified_observations": len(findings),
            "expected_failures": expected,
            "candidate_findings_raw": len(findings) - expected,
            "findings_unique_operational": len(unique),
            "candidate_endpoints": len(
                {
                    item["endpoint_id"]
                    for item in findings
                    if item["classification"] != EXPECTED_CLASSIFICATION
                }
            ),
        },
        "raw_by_classification": dict(sorted(raw_classes.items())),
        "candidate_by_classification": dict(sorted(candidate_classes.items())),
        "unique_by_classification": dict(sorted(unique_classes.items())),
        "executed_by_http_status_class": dict(sorted(status_classes.items())),
    }


def _report(metrics: dict[str, Any]) -> str:
    counts = metrics["counts"]
    return "\n".join(
        [
            "# Deduplication report",
            "",
            f"API: `{metrics['api_id']}`",
            "",
            "## Counts",
            "",
            f"- Planned requests: {counts['planned_requests']}",
            f"- Executed requests: {counts['executed_requests']}",
            f"- Classified observations: {counts['classified_observations']}",
            f"- Expected failures: {counts['expected_failures']}",
            f"- Raw candidate findings: {counts['candidate_findings_raw']}",
            f"- Unique operational findings: "
            f"{counts['findings_unique_operational']}",
            "",
            "## Interpretation",
            "",
            "`EXPECTED_FAILURE` remains an execution metric and is excluded "
            "before deduplication.",
            "",
            "The strict signature represents a black-box operational finding, "
            "not a confirmed bug, vulnerability, or root cause.",
            "",
        ]
    )


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _artifact_paths(run_dir: Path) -> list[str]:
    artifacts = ["run_manifest.json"]
    artifacts.extend(
        path.relative_to(run_dir).as_posix()
        for directory in (run_dir / "data", run_dir / "analysis")
        for path in sorted(directory.iterdir())
        if path.is_file()
    )
    return artifacts


def _record_failure(
    manifest_path: Path,
    manifest: dict[str, Any],
    error: Exception,
) -> None:
    manifest["postprocessing"]["deduplication"] = {
        "status": "failed",
        "error": {"type": type(error).__name__, "message": str(error)},
    }
    _write_json(manifest_path, manifest)


def process_run(run_dir: Path) -> dict[str, Any]:
    manifest_path = run_dir / "run_manifest.json"
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise CorrelationError(f"{manifest_path} must contain a JSON object")
    try:
        api_id = manifest.get("target_id")
        if not isinstance(api_id, str) or not api_id:
            raise CorrelationError("run_manifest.json has no valid target_id")
        plans = _load_records(run_dir / "data" / "execution_plan.json")
        results = _load_records(run_dir / "data" / "results.json")
        findings = _load_records(
            run_dir / "analysis" / "analysis_findings.json"
        )
        correlated = correlate_records(plans, results, findings)
        unique = deduplicate_findings(api_id, correlated)
        metrics = _build_metrics(api_id, plans, results, findings, unique)
        analysis_dir = run_dir / "analysis"
        _write_json(analysis_dir / "findings_unique.json", unique)
        _write_json(analysis_dir / "metrics.json", metrics)
        (analysis_dir / "deduplication_report.md").write_text(
            _report(metrics), encoding="utf-8"
        )
        manifest["artifacts"] = _artifact_paths(run_dir)
        manifest["postprocessing"]["deduplication"] = {
            "status": "completed",
            "counts": metrics["counts"],
            "error": None,
        }
        _write_json(manifest_path, manifest)
        return metrics
    except Exception as error:
        _record_failure(manifest_path, manifest, error)
        raise
