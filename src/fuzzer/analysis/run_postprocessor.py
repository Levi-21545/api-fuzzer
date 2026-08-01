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
from fuzzer.analysis.fuzzy_engine import FUZZY_MODEL_ID, FuzzyEngine
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.http import HttpMethod
from fuzzer.parser.openapi_parser import parse_openapi
from fuzzer.utils.redaction import redact_text, redact_value


_REPORT_FINDING_LIMIT = 50
_EXCERPT_LIMIT = 600


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
            raise CorrelationError(f"{artifact_name}[{position}] has no valid case_id")
        if case_id in indexed:
            raise CorrelationError(f"duplicate case_id {case_id!r} in {artifact_name}")
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
        raise CorrelationError(f"inconsistent endpoint_id for {item.case_id}: {values}")
    if item.finding.get("status_code") != item.result.get("status_code"):
        raise CorrelationError(f"inconsistent status_code for {item.case_id}")
    if item.finding.get("request_payload") != item.plan.get("payload"):
        raise CorrelationError(f"inconsistent request payload for {item.case_id}")


def _enrich_severity_assessments(
    manifest: dict[str, Any],
    results: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> None:
    if all(
        isinstance(item.get("severity_assessment"), dict)
        and item["severity_assessment"].get("model_id") == FUZZY_MODEL_ID
        for item in findings
    ):
        return
    schema_value = manifest.get("inputs", {}).get("schema")
    if not isinstance(schema_value, str) or not Path(schema_value).is_file():
        return

    spec = parse_openapi(schema_value)
    endpoint_by_id = {endpoint.id: endpoint for endpoint in spec.endpoints}
    result_by_id = _index(results, "results.json")
    engine = FuzzyEngine()
    for finding in findings:
        existing = finding.get("severity_assessment")
        if isinstance(existing, dict) and existing.get("model_id") == FUZZY_MODEL_ID:
            continue
        endpoint = endpoint_by_id.get(finding.get("endpoint_id"))
        result_record = result_by_id.get(finding.get("case_id"))
        if endpoint is None or result_record is None:
            continue
        result = _execution_result(result_record, endpoint.method)
        assessment = engine.assess(endpoint, result)
        finding["severity_assessment"] = assessment.to_dict()


def _execution_result(record: dict[str, Any], method: HttpMethod) -> ExecutionResult:
    return ExecutionResult(
        case_id=record["case_id"],
        endpoint_id=record["endpoint_id"],
        method=method,
        url=record.get("url") or "",
        status_code=record.get("status_code"),
        response_time_ms=float(record.get("response_time_ms") or 0),
        response_size=record.get("response_size"),
        raw_response=record.get("raw_response"),
        error=record.get("error"),
    )


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
    unique_severities = Counter(
        item["representative"]["finding"].get("severity", "UNKNOWN") for item in unique
    )
    unique_scores = Counter(
        str(item["representative"]["finding"].get("severity_score")) for item in unique
    )
    findings_with_assessment = [
        item for item in findings if item.get("severity_assessment") is not None
    ]
    unique_findings = [item["representative"]["finding"] for item in unique]
    unique_with_assessment = [
        item for item in unique_findings if item.get("severity_assessment") is not None
    ]
    strongest_rules = Counter()
    for finding in unique_with_assessment:
        assessment = finding["severity_assessment"]
        activated = assessment.get("activated_rules", [])
        if assessment.get("fallback_used"):
            strongest_rules["FALLBACK_STATUS_DEVIATION"] += 1
        elif activated:
            strongest_rules[activated[0]["id"]] += 1
        else:
            strongest_rules["NO_ACTIVE_RULE"] += 1
    status_classes = Counter(
        "network_error"
        if item.get("status_code") is None
        else f"{int(item['status_code']) // 100}xx"
        for item in results
    )
    expected = raw_classes[EXPECTED_CLASSIFICATION]
    raw_candidates = len(findings) - expected
    unique_count = len(unique)
    return {
        "api_id": api_id,
        "counts": {
            "planned_requests": len(plans),
            "executed_requests": len(results),
            "classified_observations": len(findings),
            "expected_failures": expected,
            "candidate_findings_raw": raw_candidates,
            "findings_unique_operational": unique_count,
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
        "unique_by_severity": dict(sorted(unique_severities.items())),
        "unique_by_score": dict(
            sorted(unique_scores.items(), key=lambda item: float(item[0]))
        ),
        "executed_by_http_status_class": dict(sorted(status_classes.items())),
        "fuzzy_assessment": {
            "classified_with_assessment": len(findings_with_assessment),
            "classified_fallbacks": sum(
                item["severity_assessment"].get("fallback_used", False)
                for item in findings_with_assessment
            ),
            "unique_with_assessment": len(unique_with_assessment),
            "unique_fallbacks": sum(
                item["severity_assessment"].get("fallback_used", False)
                for item in unique_with_assessment
            ),
            "unique_by_strongest_rule": dict(sorted(strongest_rules.items())),
        },
        "rates": {
            "execution_completion_ratio": _ratio(len(results), len(plans)),
            "candidate_per_executed_ratio": _ratio(raw_candidates, len(results)),
            "deduplication_reduction_ratio": (
                round(1 - _ratio(unique_count, raw_candidates), 4)
                if raw_candidates
                else 0.0
            ),
        },
    }


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _percentage(value: float) -> str:
    return f"{value * 100:.1f}%"


def _mutation_summary(item: dict[str, Any]) -> str:
    mutations = item["representative"]["plan"].get("mutations") or []
    if not mutations:
        return "baseline request"
    summaries: list[str] = []
    for mutation in mutations:
        operator = mutation.get("operator", "unknown")
        constraint = mutation.get("constraint") or "unspecified"
        raw_path = mutation.get("path") or []
        path = "/" + "/".join(str(part) for part in raw_path)
        summaries.append(f"`{operator}` on `{path}` ({constraint})")
    return "; ".join(summaries)


def _excerpt(value: Any, *, serialized: bool = False) -> str:
    if serialized and isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
    rendered = json.dumps(
        redact_value(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    if len(rendered) <= _EXCERPT_LIMIT:
        return rendered
    return rendered[: _EXCERPT_LIMIT - 1] + "…"


def _severity_key(item: dict[str, Any]) -> tuple[int, float, str, str]:
    finding = item["representative"]["finding"]
    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return (
        severity_rank.get(finding.get("severity"), 3),
        -float(finding.get("severity_score") or 0),
        finding.get("endpoint_id") or "",
        item["signature"]["id"],
    )


def _dominant_terms(memberships: dict[str, Any]) -> str:
    dominant: list[str] = []
    for variable, raw_terms in memberships.items():
        if not isinstance(raw_terms, dict) or not raw_terms:
            continue
        term, degree = max(raw_terms.items(), key=lambda item: item[1])
        dominant.append(f"{variable}={term} ({float(degree):.2f})")
    return "; ".join(dominant) or "unavailable"


def _format_fis_input(value: Any, suffix: str = "") -> str:
    if not isinstance(value, (int, float)):
        return "unavailable"
    return f"{float(value):.4g}{suffix}"


def _assessment_lines(finding: dict[str, Any]) -> list[str]:
    assessment = finding.get("severity_assessment")
    if not isinstance(assessment, dict):
        return ["- FIS rationale: unavailable for this artifact"]
    inputs = assessment.get("inputs", {})
    activated = assessment.get("activated_rules", [])
    strongest = activated[0] if activated else None
    lines = [
        f"- FIS model: `{assessment.get('model_id', 'unknown')}`",
        "- FIS inputs: "
        f"status deviation "
        f"`{_format_fis_input(inputs.get('status_deviation'))}`, "
        f"response time "
        f"`{_format_fis_input(inputs.get('response_time_ms'), ' ms')}`, "
        f"response-size signal "
        f"`{_format_fis_input(inputs.get('response_size_signal'))}`",
        f"- Dominant fuzzy terms: {_dominant_terms(assessment.get('memberships', {}))}",
    ]
    if isinstance(strongest, dict):
        lines.append(
            f"- Strongest activated rule: `{strongest.get('id')}` "
            f"(strength `{strongest.get('strength')}`) — "
            f"{strongest.get('description')}"
        )
    if assessment.get("fallback_used"):
        lines.append("- FIS fallback: crisp status deviation was used")
    return lines


def _report(metrics: dict[str, Any], unique: list[dict[str, Any]]) -> str:
    counts = metrics["counts"]
    rates = metrics["rates"]
    fuzzy_assessment = metrics["fuzzy_assessment"]
    lines = [
        "# Deduplication report",
        "",
        f"API: `{metrics['api_id']}`",
        "",
        "## Summary",
        "",
        f"- Planned requests: {counts['planned_requests']}",
        f"- Executed requests: {counts['executed_requests']} "
        f"({_percentage(rates['execution_completion_ratio'])})",
        f"- Classified observations: {counts['classified_observations']}",
        f"- Expected failures: {counts['expected_failures']}",
        f"- Raw candidate findings: {counts['candidate_findings_raw']}",
        f"- Unique operational findings: {counts['findings_unique_operational']}",
        f"- Deduplication reduction: "
        f"{_percentage(rates['deduplication_reduction_ratio'])}",
        f"- Candidate endpoints: {counts['candidate_endpoints']}",
        f"- FIS rationale coverage: "
        f"{fuzzy_assessment['unique_with_assessment']}/"
        f"{counts['findings_unique_operational']} unique findings",
        f"- FIS fallbacks among unique findings: "
        f"{fuzzy_assessment['unique_fallbacks']}",
        "",
        "`EXPECTED_FAILURE` remains an execution metric and is excluded before "
        "deduplication. A unique operational finding is a strict black-box "
        "signature, not a confirmed bug, vulnerability, or root cause.",
        "",
        "## Candidate classifications",
        "",
        "| Classification | Raw | Unique |",
        "| --- | ---: | ---: |",
    ]
    candidate_classes = metrics["candidate_by_classification"]
    unique_classes = metrics["unique_by_classification"]
    for classification in sorted(candidate_classes):
        lines.append(
            f"| `{classification}` | {candidate_classes[classification]} | "
            f"{unique_classes.get(classification, 0)} |"
        )

    endpoint_counts = Counter(
        item["representative"]["finding"]["endpoint_id"] for item in unique
    )
    lines.extend(["", "## Endpoints with unique findings", ""])
    for endpoint, count in endpoint_counts.most_common(10):
        lines.append(f"- `{endpoint}`: {count}")

    ordered = sorted(unique, key=_severity_key)
    displayed = ordered[:_REPORT_FINDING_LIMIT]
    lines.extend(
        [
            "",
            "## Prioritized unique findings",
            "",
            f"Showing {len(displayed)} of {len(ordered)} unique findings. The "
            "complete machine-readable set is available in "
            "`findings_unique.json`.",
        ]
    )
    for position, item in enumerate(displayed, start=1):
        representative = item["representative"]
        finding = representative["finding"]
        result = representative["result"]
        signature_id = item["signature"]["id"][:12]
        lines.extend(
            [
                "",
                f"### {position}. {finding.get('severity', 'UNKNOWN')} · "
                f"{finding['classification']}",
                "",
                f"- Endpoint: `{finding['endpoint_id']}`",
                f"- HTTP status: `{result.get('status_code')}`",
                f"- Score: `{finding.get('severity_score')}`",
                f"- Occurrences in this run: `{item['occurrence_count']}`",
                f"- Representative case: `{representative['plan']['case_id']}`",
                f"- Signature: `{signature_id}`",
                f"- Mutation: {_mutation_summary(item)}",
                f"- Interpretation: {redact_text(finding['description'])}",
                "- Request payload: `"
                f"{_excerpt(representative['plan'].get('payload'))}`",
                "- Response excerpt: `"
                f"{_excerpt(result.get('raw_response'), serialized=True)}`",
            ]
        )
        lines.extend(_assessment_lines(finding))
    return "\n".join(lines) + "\n"


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(
            redact_value(value),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _redact_text_artifacts(run_dir: Path) -> None:
    for directory in (run_dir / "data", run_dir / "analysis"):
        for path in directory.iterdir():
            if path.is_file() and path.suffix in {".log", ".md"}:
                text = path.read_text(encoding="utf-8")
                path.write_text(redact_text(text), encoding="utf-8")


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
    _postprocessing(manifest)["deduplication"] = {
        "status": "failed",
        "error": {"type": type(error).__name__, "message": str(error)},
    }
    _write_json(manifest_path, manifest)


def _postprocessing(manifest: dict[str, Any]) -> dict[str, Any]:
    value = manifest.get("postprocessing")
    if isinstance(value, dict):
        return value
    value = {}
    manifest["postprocessing"] = value
    return value


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
        findings = _load_records(run_dir / "analysis" / "analysis_findings.json")
        plans = redact_value(plans)
        results = redact_value(results)
        findings = redact_value(findings)
        _enrich_severity_assessments(manifest, results, findings)
        correlated = correlate_records(plans, results, findings)
        unique = deduplicate_findings(api_id, correlated)
        metrics = _build_metrics(api_id, plans, results, findings, unique)
        analysis_dir = run_dir / "analysis"
        _write_json(run_dir / "data" / "execution_plan.json", plans)
        _write_json(run_dir / "data" / "results.json", results)
        _write_json(analysis_dir / "analysis_findings.json", findings)
        _write_json(analysis_dir / "findings_unique.json", unique)
        _write_json(analysis_dir / "metrics.json", metrics)
        (analysis_dir / "deduplication_report.md").write_text(
            _report(metrics, unique), encoding="utf-8"
        )
        _redact_text_artifacts(run_dir)
        manifest["artifacts"] = _artifact_paths(run_dir)
        _postprocessing(manifest)["deduplication"] = {
            "status": "completed",
            "counts": metrics["counts"],
            "error": None,
        }
        _write_json(manifest_path, manifest)
        return metrics
    except Exception as error:
        _record_failure(manifest_path, manifest, error)
        raise
