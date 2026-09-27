import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import pytest
from fuzzer.analysis.deduplication import CorrelatedFinding, build_signature
from fuzzer.analysis.final_experiment import protocol, summary

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
                "schema_sha256": protocol.digest(contract),
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


def test_cli_writes_a_compact_revalidated_review_bundle(tmp_path, capsys):
    source = tmp_path / "experiment"
    paths = make_campaign(source, "alpha")
    for run_dir in paths:
        log = run_dir / "data/target_container.log"
        log.write_text("diagnostic log", encoding="utf-8")
        manifest_path = run_dir / "run_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["artifacts"].append("data/target_container.log")
        write_json(manifest_path, manifest)
    source_hashes = {
        run_dir.name: protocol.digest(run_dir / "run_manifest.json")
        for run_dir in paths
    }
    review = tmp_path / "review"

    assert analysis.main([str(source), "expected", "--review-dir", str(review)]) == 0
    output = json.loads(capsys.readouterr().out)

    assert output["alpha"]["totals"]["executed_requests"] == 5
    assert output["alpha"]["signature_union"] == 1
    assert (review / "results.md").is_file()
    report = (review / "results.md").read_text()
    assert "| Arquivo | ID semântico (prefixo) |" in report
    assert (review / "README.md").is_file()
    assert (review / "final-analysis.json").is_file()
    index = json.loads((review / "provenance-index.json").read_text())
    assert index["collector_commit"] == "expected"
    assert index["analyzer_files_sha256"] == protocol.analyzer_source_hashes()
    assert len(index["runs"]) == 5
    assert index["source_only_invalid_attempts"] == {"alpha": []}
    assert str(tmp_path) not in json.dumps(index)
    for run_dir in paths:
        assert (run_dir / "data/target_container.log").is_file()
        bundled = review / "alpha" / run_dir.name
        manifest = json.loads((bundled / "run_manifest.json").read_text())
        assert "data/target_container.log" not in manifest["artifacts"]
        assert not (bundled / "data/target_container.log").exists()
        provenance = next(
            item for item in index["runs"] if item["run_id"] == run_dir.name
        )
        assert provenance["source_manifest_sha256"] == source_hashes[run_dir.name]
        assert provenance["package_manifest_sha256"] == protocol.digest(
            bundled / "run_manifest.json"
        )
        assert provenance["adapted_manifest_fields"] == ["artifacts", "inputs.schema"]
        assert provenance["omitted_artifacts"] == [
            {
                "path": "data/target_container.log",
                "reason": "diagnostic log kept in source",
            }
        ]
        manifest_mapping = provenance["artifact_mappings"]["run_manifest.json"]
        assert manifest_mapping["action"] == "adapted"
        assert manifest_mapping["source_sha256"] == source_hashes[run_dir.name]
        assert manifest_mapping["package_sha256"] == protocol.digest(
            bundled / "run_manifest.json"
        )
        copied_mapping = provenance["artifact_mappings"]["data/results.json"]
        assert copied_mapping["action"] == "copied"
        assert copied_mapping["source_sha256"] == copied_mapping["package_sha256"]
    readme = (review / "README.md").read_text()
    assert "## Analisar este pacote" in readme
    assert "## Exportar novamente dos runs locais" in readme
    assert "## Executar uma nova coleta" in readme
    assert "provenance-index.json" in readme
    assert "{{" not in readme
    assert '--review-dir "$REVIEW_DEST"' in readme
    validated_bundle = protocol.discover_apis(review)
    assert len(validated_bundle["alpha"]) == 5


def test_review_bundle_reports_empty_signature_union_without_division_error(
    tmp_path, capsys
):
    source = tmp_path / "experiment"
    make_campaign(source, "empty", finding=False)
    review = tmp_path / "review"

    assert analysis.main([str(source), "expected", "--review-dir", str(review)]) == 0
    output = json.loads(capsys.readouterr().out)
    report = (review / "results.md").read_text()

    assert output["empty"]["signature_union"] == 0
    assert output["empty"]["observed_once_ratio"] is None
    assert output["empty"]["reobserved_at_least_four_ratio"] is None
    assert "| empty | 5/5 | 0/0/5 | 0 | 0 | 0 | 0.0% | 0 | — | — |" in report
    assert "| empty | 0 | — | — | — | 0 | 0 | 0 |" in report


def test_shared_meilisearch_contract_keeps_source_hashes(tmp_path, capsys):
    source = tmp_path / "experiment"
    paths = make_campaign(source, "meilisearch")
    for run_dir in paths:
        contract = run_dir / "data/target_contract.json"
        contract.write_bytes((run_dir / "data/contract.json").read_bytes())
        manifest_path = run_dir / "run_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["inputs"]["schema"] = "data/target_contract.json"
        manifest["artifacts"].append("data/target_contract.json")
        write_json(manifest_path, manifest)
    review = tmp_path / "review"

    assert analysis.main([str(source), "expected", "--review-dir", str(review)]) == 0
    capsys.readouterr()
    shared_contract = review / "contracts/meilisearch-v1.45.1-openapi.json"
    assert shared_contract.is_file()
    meili_license = review / "licenses/meilisearch-LICENSE-MIT.txt"
    assert meili_license.is_file()
    assert "Copyright (c) 2019-2025 Meili SAS" in meili_license.read_text()
    license_record = (review / "LICENSES.md").read_text()
    assert "MIT-only segundo o upstream" in license_record
    assert "meilisearch/meilisearch/issues/6010" in license_record
    index = json.loads((review / "provenance-index.json").read_text())
    for run in index["runs"]:
        mapping = run["artifact_mappings"]["data/target_contract.json"]
        assert mapping["action"] == "relocated"
        assert mapping["package_path"] == "contracts/meilisearch-v1.45.1-openapi.json"
        assert mapping["source_sha256"] == mapping["package_sha256"]
        assert run["contract_input"]["distribution"] == "included"
        per_run_contract = (
            review / "meilisearch" / run["run_id"] / "data/target_contract.json"
        )
        assert not per_run_contract.exists()


def test_review_bundle_keeps_invalid_attempt_reason_only_in_source(tmp_path, capsys):
    source = tmp_path / "experiment"
    make_campaign(source, "alpha")
    make_run(source, "alpha", 6)
    review = tmp_path / "review"
    _, source_invalid = protocol.select_valid_attempts(
        "alpha", protocol.discover_apis(source)["alpha"], "expected"
    )
    assert str(tmp_path) in source_invalid[0]["reason"]

    assert analysis.main([str(source), "expected", "--review-dir", str(review)]) == 0
    capsys.readouterr()
    index = json.loads((review / "provenance-index.json").read_text())
    assert index["source_only_invalid_attempts"] == {"alpha": ["run-6"]}
    package_analysis = (review / "final-analysis.json").read_text()
    assert str(tmp_path) not in package_analysis
    invalid = json.loads(package_analysis)["alpha"]["invalid_attempts"]
    assert invalid == [{"run_id": "run-6", "reason": "retained in source only"}]


def test_cli_rejects_different_experiments_in_same_root(tmp_path, capsys):
    make_campaign(tmp_path, "alpha")
    make_campaign(tmp_path, "beta", experiment="another-experiment")

    assert analysis.main([str(tmp_path), "expected"]) == 1
    assert "experiment or fuzzer source differs across APIs" in capsys.readouterr().err


def test_missing_and_wrong_repetitions_rejected(tmp_path):
    paths = make_campaign(tmp_path, "alpha")
    with pytest.raises(protocol.InvalidCampaign, match="exactly 5 runs"):
        protocol.validate_api("alpha", paths[:4], "expected")
    manifest_path = paths[-1] / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["run_number"] = 4
    write_json(manifest_path, manifest)
    with pytest.raises(protocol.InvalidCampaign, match="numbered 1 through 5"):
        protocol.validate_api("alpha", paths, "expected")


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
    with pytest.raises(protocol.InvalidCampaign, match=expected):
        protocol.validate_api("alpha", paths, "expected")


def test_presence_frequency_and_empty_results(tmp_path):
    paths = [
        make_run(tmp_path, "alpha", number, finding=number < 5)
        for number in range(1, 6)
    ]
    summary_result = summary.summarize(
        "alpha", protocol.validate_api("alpha", paths, "expected")
    )
    assert summary_result["signature_union"] == 1
    assert summary_result["presence_frequency"]["4"] == 1
    assert summary_result["reobserved_at_least_four_ratio"] == 1

    empty_paths = [
        make_run(tmp_path, "empty", number, finding=False) for number in range(1, 6)
    ]
    empty_runs = protocol.validate_api("empty", empty_paths, "expected")
    empty = summary.summarize("alpha", empty_runs)
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

    assert summary.semantic_id(
        item("POST /multi-search", 1), "meilisearch"
    ) == summary.semantic_id(item("POST /multi-search", 2), "meilisearch")
    assert summary.semantic_id(item("GET /x", 1), "meilisearch") != summary.semantic_id(
        item("GET /x", 2), "meilisearch"
    )


def test_metrics_counts_must_match_unique_findings(tmp_path):
    paths = make_campaign(tmp_path, "alpha")
    metrics_path = paths[0] / "analysis/metrics.json"
    metrics = json.loads(metrics_path.read_text())
    metrics["counts"]["findings_unique_operational"] = 2
    write_json(metrics_path, metrics)
    with pytest.raises(protocol.InvalidCampaign, match="metrics counts"):
        protocol.validate_run(paths[0], "alpha", "expected")


@pytest.mark.parametrize(
    "part,field,value",
    [
        ("plan", "payload", {"changed": True}),
        ("result", "response_time_ms", 999),
        ("finding", "severity_score", 0.2),
    ],
)
def test_representative_must_match_complete_case_records(tmp_path, part, field, value):
    path = make_run(tmp_path, "alpha", 1)
    unique_path = path / "analysis/findings_unique.json"
    unique = json.loads(unique_path.read_text())
    unique[0]["representative"][part][field] = value
    write_json(unique_path, unique)

    with pytest.raises(protocol.InvalidCampaign, match="representative differs"):
        protocol.validate_run(path, "alpha", "expected")


@pytest.mark.parametrize(
    "change,expected",
    [
        ("candidate_endpoints", "candidate endpoint count"),
        ("http_status", "HTTP status class counts"),
    ],
)
def test_secondary_counts_are_checked_against_records(tmp_path, change, expected):
    path = make_run(tmp_path, "alpha", 1)
    metrics_path = path / "analysis/metrics.json"
    metrics = json.loads(metrics_path.read_text())
    if change == "candidate_endpoints":
        metrics["counts"]["candidate_endpoints"] = 0
    else:
        metrics["executed_by_http_status_class"] = {"4xx": 1}
    write_json(metrics_path, metrics)

    with pytest.raises(protocol.InvalidCampaign, match=expected):
        protocol.validate_run(path, "alpha", "expected")


def test_scientific_parity_excludes_only_provenance(tmp_path):
    runs = protocol.validate_api("alpha", make_campaign(tmp_path, "alpha"), "expected")
    source = summary.summarize("alpha", runs)
    assert set(source) == set(summary.SCIENTIFIC_FIELDS) | {"campaigns"}
    assert set(source["campaigns"][0]) == set(summary.CAMPAIGN_SCIENTIFIC_FIELDS) | {
        "artifact_sha256"
    }
    exported = deepcopy(source)
    exported["campaigns"][0]["artifact_sha256"] = {"adapted": "hash"}
    exported["invalid_attempts"] = [{"run_id": "invalid"}]
    summary.require_scientific_parity({"alpha": source}, {"alpha": exported})

    exported["score_distribution_unique_per_run"]["median"] = 0.1
    with pytest.raises(protocol.InvalidCampaign, match="score_distribution"):
        summary.require_scientific_parity({"alpha": source}, {"alpha": exported})
    exported = deepcopy(source)
    exported["campaigns"][0]["http_status_classes"] = {"4xx": 1}
    with pytest.raises(protocol.InvalidCampaign, match="campaign http_status_classes"):
        summary.require_scientific_parity({"alpha": source}, {"alpha": exported})


def test_illustrative_case_selection_keeps_existing_semantic_id_rule():
    signatures = {
        "z-stable": {"present_in": [1, 2, 3, 4, 5]},
        "a-stable": {"present_in": [1, 2, 3, 4, 5]},
        "z-once": {"present_in": [2]},
        "a-once": {"present_in": [3]},
        "other": {"present_in": [1, 2]},
    }
    assert [key for key, _ in summary.illustrative_signatures(signatures)] == [
        "a-stable",
        "a-once",
    ]
    fallback = {"z": signatures["other"], "a": signatures["other"]}
    assert [key for key, _ in summary.illustrative_signatures(fallback)] == ["a"]


@pytest.mark.parametrize("selected", [None, 0, True, "1"])
def test_selected_operations_requires_positive_integer(tmp_path, selected):
    path = make_run(tmp_path, "alpha", 1)
    manifest_path = path / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["counts"]["selected_endpoints"] = selected
    write_json(manifest_path, manifest)
    with pytest.raises(protocol.InvalidCampaign, match="no operations were selected"):
        protocol.validate_run(path, "alpha", "expected")


def test_missing_listed_artifact_and_case_mismatch_rejected(tmp_path):
    path = make_run(tmp_path, "alpha", 1)
    (path / "analysis/analysis_report.md").unlink()
    with pytest.raises(protocol.InvalidCampaign, match="missing or unsafe artifact"):
        protocol.validate_run(path, "alpha", "expected")

    (path / "analysis/analysis_report.md").write_text("report", encoding="utf-8")
    results_path = path / "data/results.json"
    results = json.loads(results_path.read_text())
    results[0]["case_id"] = "other-case"
    write_json(results_path, results)
    with pytest.raises(ValueError, match="plan/result case_id mismatch"):
        protocol.validate_run(path, "alpha", "expected")


def test_signature_bucket_recomputed_from_records(tmp_path):
    path = make_run(tmp_path, "alpha", 1)
    unique_path = path / "analysis/findings_unique.json"
    unique = json.loads(unique_path.read_text())
    unique[0]["signature"]["id"] = "incorrect"
    write_json(unique_path, unique)
    with pytest.raises(protocol.InvalidCampaign, match="signature/case mapping"):
        protocol.validate_run(path, "alpha", "expected")


def test_invalid_attempt_is_retained_outside_five_valid_runs(tmp_path):
    paths = make_campaign(tmp_path, "alpha")
    invalid = make_run(tmp_path, "alpha", 6)
    runs, rejected = protocol.select_valid_attempts(
        "alpha", [*paths, invalid], "expected"
    )
    assert len(runs) == 5
    assert rejected == [
        {"run_id": "run-6", "reason": f"{invalid}: run_number must be between 1 and 5"}
    ]
