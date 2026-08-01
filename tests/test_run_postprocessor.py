import json

from fuzzer.analysis.run_postprocessor import process_run


def _write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def test_process_run_writes_analysis_and_updates_manifest(tmp_path):
    data = tmp_path / "data"
    analysis = tmp_path / "analysis"
    data.mkdir()
    analysis.mkdir()
    manifest = {
        "target_id": "sample-api",
        "status": "completed",
        "artifacts": [],
        "postprocessing": {
            "deduplication": {"status": "pending", "error": None}
        },
    }
    plan = {
        "case_id": "case-000001",
        "endpoint_id": "GET /items",
        "payload": None,
    }
    result = {
        "case_id": "case-000001",
        "endpoint_id": "GET /items",
        "status_code": 500,
        "raw_response": '{"error":"failure"}',
        "error": None,
    }
    finding = {
        "case_id": "case-000001",
        "endpoint_id": "GET /items",
        "status_code": 500,
        "classification": "SERVER_ERROR",
        "request_payload": None,
    }
    _write_json(tmp_path / "run_manifest.json", manifest)
    _write_json(data / "execution_plan.json", [plan])
    _write_json(data / "results.json", [result])
    _write_json(analysis / "analysis_findings.json", [finding])
    (analysis / "analysis_report.md").write_text("report", encoding="utf-8")

    metrics = process_run(tmp_path)

    updated = json.loads(
        (tmp_path / "run_manifest.json").read_text(encoding="utf-8")
    )
    assert metrics["counts"]["findings_unique_operational"] == 1
    assert updated["status"] == "completed"
    assert updated["postprocessing"]["deduplication"]["status"] == "completed"
    assert (analysis / "findings_unique.json").is_file()
    assert (analysis / "metrics.json").is_file()
    assert (analysis / "deduplication_report.md").is_file()
