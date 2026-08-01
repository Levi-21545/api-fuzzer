from fuzzer.utils.manifest import sha256_source_tree
from fuzzer.utils.manifest import build_run_manifest


def test_source_tree_hash_changes_with_executable_source(tmp_path):
    source = tmp_path / "src" / "fuzzer"
    source.mkdir(parents=True)
    module = source / "module.py"
    module.write_text("VALUE = 1\n", encoding="utf-8")

    first_hash = sha256_source_tree(tmp_path)
    module.write_text("VALUE = 2\n", encoding="utf-8")
    second_hash = sha256_source_tree(tmp_path)

    assert first_hash != second_hash


def test_source_tree_hash_ignores_runtime_output(tmp_path):
    source = tmp_path / "src" / "fuzzer"
    source.mkdir(parents=True)
    (source / "module.py").write_text("VALUE = 1\n", encoding="utf-8")

    first_hash = sha256_source_tree(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    (output / "results.json").write_text("[]\n", encoding="utf-8")

    assert sha256_source_tree(tmp_path) == first_hash


def test_manifest_uses_run_data_and_analysis_directories(tmp_path, monkeypatch):
    schema = tmp_path / "schema.yaml"
    schema.write_text("openapi: 3.0.0\n", encoding="utf-8")
    args = type(
        "Args",
        (),
        {
            "schema": schema,
            "experiment_id": "experiment",
            "target_id": "target",
            "run_number": 1,
            "base_url": "http://localhost",
            "level": 1,
            "max": 20,
            "limit": None,
            "all": True,
            "path_filter": None,
            "excluded_paths": [],
            "auto_auth": False,
            "auth_probe": False,
            "no_deduplicate": False,
            "concurrency": 1,
            "delay": 0,
            "timeout": 10,
        },
    )()
    monkeypatch.setattr("fuzzer.utils.manifest._repository_root", lambda: tmp_path)
    monkeypatch.setattr("fuzzer.utils.manifest._git_state", lambda: {})

    manifest = build_run_manifest(args, "run-1")

    assert manifest["artifacts"] == [
        "run_manifest.json",
        "data/execution_plan.json",
        "data/results.json",
        "analysis/analysis_findings.json",
        "analysis/analysis_report.md",
    ]
    assert manifest["fuzzer"]["configuration"]["deduplicate"] is True
    assert manifest["postprocessing"]["deduplication"]["status"] == "pending"


def test_manifest_derives_target_id_from_schema_name(tmp_path, monkeypatch):
    schema = tmp_path / "petstore.openapi.yaml"
    schema.write_text("openapi: 3.0.0\n", encoding="utf-8")
    args = type(
        "Args",
        (),
        {
            "schema": schema,
            "experiment_id": None,
            "target_id": None,
            "run_number": None,
            "base_url": "http://localhost",
            "level": 1,
            "max": 10,
            "limit": None,
            "all": False,
            "path_filter": None,
            "excluded_paths": [],
            "auto_auth": False,
            "auth_probe": False,
            "no_deduplicate": False,
            "concurrency": 1,
            "delay": 0,
            "timeout": 10,
        },
    )()
    monkeypatch.setattr("fuzzer.utils.manifest._repository_root", lambda: tmp_path)
    monkeypatch.setattr("fuzzer.utils.manifest._git_state", lambda: {})

    manifest = build_run_manifest(args, "run-1")

    assert manifest["target_id"] == "petstore.openapi"
