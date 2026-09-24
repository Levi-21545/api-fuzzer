import importlib.util
import json
from pathlib import Path

import pytest
from fuzzer.analysis.deduplication import CorrelatedFinding, build_signature


MODULE = Path(__file__).resolve().parents[1] / "scripts/experiments/analyze_final.py"
SPEC = importlib.util.spec_from_file_location("final_analysis", MODULE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {MODULE}")
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def make_run(
    root, api, number, *, finding=True, experiment="experiment", schema="schema"
):
    run_dir = root / api / f"run-{number}"
    counts = {
        "planned_requests": 1,
        "executed_requests": 1,
        "classified_observations": int(finding),
        "expected_failures": 0,
        "candidate_findings_raw": int(finding),
        "findings_unique_operational": int(finding),
        "candidate_endpoints": int(finding),
    }
    plan = {"case_id": "case-1", "endpoint_id": "GET /x", "payload": None}
    result = {
        "case_id": "case-1",
        "endpoint_id": "GET /x",
        "response_time_ms": 10,
        "status_code": 500,
        "raw_response": '{"error":"same"}',
        "error": None,
    }
    observation = {
        "case_id": "case-1",
        "endpoint_id": "GET /x",
        "classification": "SERVER_ERROR",
        "status_code": 500,
        "request_payload": None,
        "severity_score": 0.8,
        "severity": "HIGH",
    }
    unique = (
        [
            {
                "signature": build_signature(
                    api, CorrelatedFinding(plan, result, observation)
                ),
                "case_ids": ["case-1"],
                "occurrence_count": 1,
                "representative": {
                    "plan": plan,
                    "result": result,
                    "finding": observation,
                },
            }
        ]
        if finding
        else []
    )
    findings = [observation] if finding else []
    write_json(run_dir / "data/execution_plan.json", [plan])
    write_json(run_dir / "data/results.json", [result])
    write_json(run_dir / "analysis/analysis_findings.json", findings)
    write_json(run_dir / "analysis/findings_unique.json", unique)
    metrics = {
        "counts": counts,
        "candidate_by_classification": {"SERVER_ERROR": 1} if finding else {},
        "executed_by_http_status_class": {"5xx": 1},
    }
    write_json(run_dir / "analysis/metrics.json", metrics)
    contract = run_dir / "data/contract.json"
    write_json(
        contract,
        {
            "openapi": "3.0.0",
            "info": {"title": schema, "version": "1"},
            "paths": {"/x": {"get": {"responses": {"200": {"description": "ok"}}}}},
        },
    )
    for name in ("analysis/analysis_report.md", "analysis/deduplication_report.md"):
        path = run_dir / name
        path.write_text("report", encoding="utf-8")
    write_json(
        run_dir / "run_manifest.json",
        {
            "run_id": run_dir.name,
            "target_id": api,
            "run_number": number,
            "experiment_id": experiment,
            "status": "completed",
            "error": None,
            "started_at": "2026-09-23T00:00:00Z",
            "finished_at": "2026-09-23T00:01:00Z",
            "counts": {
                "planned_requests": 1,
                "completed_requests": 1,
                "findings": int(finding),
                "selected_endpoints": 1,
            },
            "inputs": {
                "schema": "data/contract.json",
                "schema_sha256": analysis.digest(contract),
                "target_image": f"image-{api}",
            },
            "fuzzer": {
                "git": {"commit": "expected", "dirty": False},
                "source_tree_sha256": "source",
                "configuration": {
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
                    "auth": api,
                },
            },
            "postprocessing": {
                "deduplication": {"status": "completed", "counts": counts}
            },
            "artifacts": [
                "run_manifest.json",
                "data/execution_plan.json",
                "data/results.json",
                "analysis/analysis_findings.json",
                "analysis/findings_unique.json",
                "analysis/metrics.json",
                "analysis/analysis_report.md",
                "analysis/deduplication_report.md",
            ],
        },
    )
    return run_dir


def make_campaign(root, api, **kwargs):
    return [make_run(root, api, number, **kwargs) for number in range(1, 6)]


def test_cli_summarizes_multiple_api_folders_and_api_configuration_can_vary(
    tmp_path, capsys
):
    make_campaign(tmp_path, "alpha")
    make_campaign(tmp_path, "beta", schema="other-schema")

    assert analysis.main([str(tmp_path), "expected"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert set(output) == {"alpha", "beta"}
    assert output["alpha"]["signature_union"] == 1
    assert output["alpha"]["presence_frequency"] == {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 1,
    }
    assert output["alpha"]["campaigns"][0]["duration_seconds"] == 60


def test_cli_rejects_different_experiments_in_same_root(tmp_path, capsys):
    make_campaign(tmp_path, "alpha")
    make_campaign(tmp_path, "beta", experiment="another-experiment")

    assert analysis.main([str(tmp_path), "expected"]) == 1
    assert "experiment or fuzzer source differs across APIs" in capsys.readouterr().err


def test_missing_and_wrong_repetitions_rejected(tmp_path):
    paths = make_campaign(tmp_path, "alpha")
    with pytest.raises(analysis.InvalidCampaign, match="exactly 5 runs"):
        analysis.validate_api("alpha", paths[:4], "expected")
    manifest_path = paths[-1] / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["run_number"] = 4
    write_json(manifest_path, manifest)
    with pytest.raises(analysis.InvalidCampaign, match="numbered 1 through 5"):
        analysis.validate_api("alpha", paths, "expected")


@pytest.mark.parametrize(
    "field,value", [("experiment_id", "changed"), ("schema_sha256", "changed")]
)
def test_incompatible_campaign_metadata_rejected(tmp_path, field, value):
    paths = make_campaign(tmp_path, "alpha")
    manifest_path = paths[-1] / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if field == "schema_sha256":
        manifest["inputs"][field] = value
    else:
        manifest[field] = value
    write_json(manifest_path, manifest)
    expected = "contract hash" if field == "schema_sha256" else "metadata differs"
    with pytest.raises(analysis.InvalidCampaign, match=expected):
        analysis.validate_api("alpha", paths, "expected")


def test_presence_frequency_and_empty_results(tmp_path):
    paths = [
        make_run(tmp_path, "alpha", number, finding=number < 5)
        for number in range(1, 6)
    ]
    summary = analysis.summarize(
        "alpha", analysis.validate_api("alpha", paths, "expected")
    )
    assert summary["signature_union"] == 1
    assert summary["presence_frequency"]["4"] == 1
    assert summary["reobserved_at_least_four_ratio"] == 1

    empty_paths = [
        make_run(tmp_path, "empty", number, finding=False) for number in range(1, 6)
    ]
    empty_runs = analysis.validate_api("empty", empty_paths, "expected")
    empty = analysis.summarize("alpha", empty_runs)
    assert empty["signature_union"] == 0
    assert empty["observed_once_ratio"] is None
    assert empty["reobserved_at_least_four_ratio"] is None


def test_meilisearch_multi_search_volatile_fields_are_normalized():
    def item(endpoint, uid):
        response = json.dumps(
            {"requestUid": uid, "processingTimeMs": uid, "message": "same"}
        )
        return {
            "signature": {
                "components": {
                    "endpoint_id": endpoint,
                    "normalized_response_sha256": f"hash-{uid}",
                },
                "normalized_response": response,
            }
        }

    assert analysis.semantic_id(
        item("POST /multi-search", 1), "meilisearch"
    ) == analysis.semantic_id(item("POST /multi-search", 2), "meilisearch")
    assert analysis.semantic_id(
        item("GET /x", 1), "meilisearch"
    ) != analysis.semantic_id(item("GET /x", 2), "meilisearch")


def test_metrics_counts_must_match_unique_findings(tmp_path):
    paths = make_campaign(tmp_path, "alpha")
    metrics_path = paths[0] / "analysis/metrics.json"
    metrics = json.loads(metrics_path.read_text())
    metrics["counts"]["findings_unique_operational"] = 2
    write_json(metrics_path, metrics)
    with pytest.raises(analysis.InvalidCampaign, match="metrics counts"):
        analysis.validate_run(paths[0], "alpha", "expected")


@pytest.mark.parametrize("selected", [None, 0, True, "1"])
def test_selected_operations_requires_positive_integer(tmp_path, selected):
    path = make_run(tmp_path, "alpha", 1)
    manifest_path = path / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["counts"]["selected_endpoints"] = selected
    write_json(manifest_path, manifest)
    with pytest.raises(analysis.InvalidCampaign, match="no operations were selected"):
        analysis.validate_run(path, "alpha", "expected")


def test_missing_listed_artifact_and_case_mismatch_rejected(tmp_path):
    path = make_run(tmp_path, "alpha", 1)
    (path / "analysis/analysis_report.md").unlink()
    with pytest.raises(analysis.InvalidCampaign, match="missing or unsafe artifact"):
        analysis.validate_run(path, "alpha", "expected")

    (path / "analysis/analysis_report.md").write_text("report", encoding="utf-8")
    results_path = path / "data/results.json"
    results = json.loads(results_path.read_text())
    results[0]["case_id"] = "other-case"
    write_json(results_path, results)
    with pytest.raises(ValueError, match="plan/result case_id mismatch"):
        analysis.validate_run(path, "alpha", "expected")


def test_signature_bucket_recomputed_from_records(tmp_path):
    path = make_run(tmp_path, "alpha", 1)
    unique_path = path / "analysis/findings_unique.json"
    unique = json.loads(unique_path.read_text())
    unique[0]["signature"]["id"] = "incorrect"
    write_json(unique_path, unique)
    with pytest.raises(analysis.InvalidCampaign, match="signature/case mapping"):
        analysis.validate_run(path, "alpha", "expected")


def test_invalid_attempt_is_retained_outside_five_valid_runs(tmp_path):
    paths = make_campaign(tmp_path, "alpha")
    invalid = make_run(tmp_path, "alpha", 6)
    runs, rejected = analysis.select_valid_attempts(
        "alpha", [*paths, invalid], "expected"
    )
    assert len(runs) == 5
    assert rejected == [
        {"run_id": "run-6", "reason": f"{invalid}: run_number must be between 1 and 5"}
    ]
