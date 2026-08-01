import json

from fuzzer.analysis.run_postprocessor import process_run


def _write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


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
    finding = {
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
    assert metrics["fuzzy_assessment"] == {
        "classified_with_assessment": 1,
        "classified_fallbacks": 0,
        "unique_with_assessment": 1,
        "unique_fallbacks": 0,
        "unique_by_strongest_rule": {
            "R1_HIGH_DEVIATION_OR_TIMEOUT": 1,
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
    assert "R1_HIGH_DEVIATION_OR_TIMEOUT" in report
    persisted_findings = json.loads(
        (analysis / "analysis_findings.json").read_text(encoding="utf-8")
    )
    assert persisted_findings[0]["severity_assessment"]["inputs"] == {
        "response_size_signal": 0.0,
        "response_time_ms": 0.0,
        "status_deviation": 1.0,
    }
    assert (
        persisted_findings[0]["severity_assessment"]["model_id"]
        == "mamdani-status-time-response-size-v1"
    )
