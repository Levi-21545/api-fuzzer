import json
from typing import Any

from fuzzer.analysis.run_postprocessor import (
    _apply_repetition_evidence,
    _auth_probe_kind,
    _case_kind,
    process_run,
)


def _write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def test_plan_context_normalizes_untyped_json_values():
    assert _case_kind({"case_kind": "mutation"}) == "mutation"
    assert _case_kind({"case_kind": "unknown"}) == "baseline"
    assert (
        _auth_probe_kind(
            {
                "case_kind": "auth_probe",
                "auth_probe_kind": "missing_credential",
            }
        )
        == "missing_credential"
    )
    assert (
        _auth_probe_kind(
            {
                "case_kind": "auth_probe",
                "headers": {"Authorization": "<REDACTED>"},
            }
        )
        == "invalid_credential"
    )


def test_process_run_writes_analysis_and_updates_manifest(tmp_path):
    data = tmp_path / "data"
    analysis = tmp_path / "analysis"
    data.mkdir()
    analysis.mkdir()
    schema = tmp_path / "schema.yaml"
    schema.write_text(
        """
openapi: 3.0.0
paths:
  /items:
    get:
      responses:
        '200':
          description: ok
""".strip(),
        encoding="utf-8",
    )
    manifest = {
        "target_id": "sample-api",
        "status": "completed",
        "artifacts": [],
        "inputs": {"schema": str(schema)},
    }
    plan = {
        "case_id": "case-000001",
        "case_kind": "mutation",
        "endpoint_id": "GET /items",
        "payload": None,
        "headers": {
            "Authorization": "Bearer secret-token",
            "Content-Type": "application/json",
        },
        "mutations": [
            {
                "operator": "wrong_type",
                "constraint": "type",
                "path": ["name"],
            }
        ],
    }
    result = {
        "case_id": "case-000001",
        "endpoint_id": "GET /items",
        "status_code": 500,
        "raw_response": '{"error":"failure","token":"response-secret"}',
        "error": None,
    }
    finding: dict[str, Any] = {
        "case_id": "case-000001",
        "endpoint_id": "GET /items",
        "status_code": 500,
        "classification": "SERVER_ERROR",
        "request_payload": None,
        "request_headers": {
            "Authorization": "Bearer secret-token",
            "Content-Type": "application/json",
        },
        "description": "Server returned a 500 error.",
        "severity": "HIGH",
        "severity_score": 0.84,
    }
    _write_json(tmp_path / "run_manifest.json", manifest)
    _write_json(data / "execution_plan.json", [plan])
    _write_json(data / "results.json", [result])
    _write_json(analysis / "analysis_findings.json", [finding])
    (analysis / "analysis_report.md").write_text("report", encoding="utf-8")

    metrics = process_run(tmp_path)

    updated = json.loads((tmp_path / "run_manifest.json").read_text(encoding="utf-8"))
    assert metrics["counts"]["findings_unique_operational"] == 1
    assert metrics["rates"]["execution_completion_ratio"] == 1.0
    assert metrics["rates"]["deduplication_reduction_ratio"] == 0.0
    assert metrics["by_execution_level"] == {
        "level_1": {
            "planned_by_case_kind": {"mutation": 1},
            "planned_requests": 1,
            "executed_requests": 1,
            "classified_observations": 1,
            "candidate_findings_raw": 1,
            "unique_findings_involving_level": 1,
        }
    }
    assert metrics["fuzzy_assessment"] == {
        "classified_with_assessment": 1,
        "classified_fallbacks": 0,
        "unique_with_assessment": 1,
        "unique_fallbacks": 0,
        "unique_by_strongest_rule": {
            "R3_HIGH_CONTRADICTION_WEAK_EVIDENCE": 1
        },
    }
    assert updated["status"] == "completed"
    assert updated["postprocessing"]["deduplication"]["status"] == "completed"
    assert (analysis / "findings_unique.json").is_file()
    assert (analysis / "metrics.json").is_file()
    assert (analysis / "deduplication_report.md").is_file()
    persisted_plan = (data / "execution_plan.json").read_text(encoding="utf-8")
    persisted_results = (data / "results.json").read_text(encoding="utf-8")
    persisted_unique = (analysis / "findings_unique.json").read_text(encoding="utf-8")
    report = (analysis / "deduplication_report.md").read_text(encoding="utf-8")
    for artifact in (persisted_plan, persisted_results, persisted_unique, report):
        assert "secret-token" not in artifact
        assert "response-secret" not in artifact
    assert "<REDACTED>" in persisted_plan
    assert "Deduplication reduction: 0.0%" in report
    assert "wrong_type" in report
    assert "Server returned a 500 error." in report
    assert 'Response excerpt: `{"error":"failure","token":"<REDACTED>"}`' in report
    assert "R3_HIGH_CONTRADICTION_WEAK_EVIDENCE" in report
    assert "## Findings by execution level" in report
    assert "| L1 | `mutation=1` | 1 | 1 | 1 | 1 | 1 |" in report
    assert "## Potentially actionable findings" in report
    assert "## Contract fidelity observations" in report
    persisted_findings = json.loads(
        (analysis / "analysis_findings.json").read_text(encoding="utf-8")
    )
    assert persisted_findings[0]["severity_assessment"]["inputs"] == {
        "access_control_exposure": 0.0,
        "behavior_contradiction": 1.0,
        "evidence_strength": 0.5,
    }
    assert (
        persisted_findings[0]["severity_assessment"]["model_id"]
        == "mamdani-behavior-evidence-access-v3"
    )


def test_repetition_evidence_promotes_repeated_valid_server_failure(tmp_path):
    schema = tmp_path / "schema.yaml"
    schema.write_text(
        """
openapi: 3.0.0
paths:
  /items:
    get:
      responses:
        '200':
          description: ok
""".strip(),
        encoding="utf-8",
    )
    finding: dict[str, Any] = {
        "classification": "SERVER_ERROR",
        "endpoint_id": "GET /items",
    }
    unique = [
        {
            "occurrence_count": 3,
            "representative": {
                "plan": {
                    "case_id": "case-000001",
                    "case_kind": "baseline",
                    "endpoint_id": "GET /items",
                    "mutations": [],
                },
                "result": {
                    "case_id": "case-000001",
                    "endpoint_id": "GET /items",
                    "status_code": 500,
                    "raw_response": '{"error":"failure"}',
                    "error": None,
                },
                "finding": finding,
            },
        }
    ]

    _apply_repetition_evidence({"inputs": {"schema": str(schema)}}, unique)

    assert finding["severity"] == "HIGH"
    assert finding["severity_score"] == 0.84
    assert finding["severity_assessment"]["inputs"]["evidence_strength"] == 1.0
