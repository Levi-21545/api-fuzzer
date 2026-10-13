"""Validate the frozen experiment protocol and its run artifacts."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from fuzzer.analysis.deduplication import EXPECTED_CLASSIFICATION, build_signature
from fuzzer.analysis.run_postprocessor import correlate_records
from fuzzer.parser.openapi_parser import parse_openapi

REPO_ROOT = Path(__file__).resolve().parents[4]
PACKAGE_DIR = Path(__file__).resolve().parent
ENTRYPOINT = REPO_ROOT / "scripts/experiments/analyze_final.py"
README_TEMPLATE = REPO_ROOT / "scripts/experiments/templates/final-review-readme.md"

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


def analyzer_source_hashes() -> dict[str, str]:
    """Hash the entrypoint, every module of this package, and the README template."""
    files = [ENTRYPOINT, *sorted(PACKAGE_DIR.glob("*.py")), README_TEMPLATE]
    return {path.relative_to(REPO_ROOT).as_posix(): digest(path) for path in files}


def analyzer_git_revision() -> str | None:
    """Identify a recoverable analyzer revision only from a clean checkout."""
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if status.returncode or status.stdout:
        return None
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return revision.stdout.strip() if revision.returncode == 0 else None


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


def check_manifest(
    run_dir: Path, manifest: dict[str, Any], api: str, commit: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Check identity, completion, frozen commit, configuration, and provenance."""
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
    return inputs, config, deduplication


def count_operations(run_dir: Path, inputs: dict[str, Any]) -> tuple[int, int]:
    """Verify the contract hash; count documented and parser-supported operations."""
    schema_file = contract_path(run_dir, inputs)
    if digest(schema_file) != inputs["schema_sha256"]:
        raise InvalidCampaign(f"{run_dir}: contract hash mismatch")
    contract = require_dict(
        yaml.safe_load(schema_file.read_text(encoding="utf-8")), f"{run_dir}: contract"
    )
    paths = require_dict(contract.get("paths"), f"{run_dir}: contract paths")
    total_operations = sum(
        method.lower() in HTTP_METHODS
        for path_item in paths.values()
        for method in require_dict(path_item, f"{run_dir}: path item")
    )
    return total_operations, len(parse_openapi(str(schema_file)).endpoints)


def check_counts(
    run_dir: Path,
    manifest: dict[str, Any],
    metrics: dict[str, Any],
    deduplication: dict[str, Any],
    records: dict[str, list[dict[str, Any]]],
    supported_operations: int,
) -> None:
    """Recount metrics.json and manifest counts from the raw run records."""
    plans, results = records["plans"], records["results"]
    findings, unique = records["findings"], records["unique"]
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
    candidate_endpoints = len(
        {
            item["endpoint_id"]
            for item in findings
            if item["classification"] != EXPECTED_CLASSIFICATION
        }
    )
    if counts.get("candidate_endpoints") != candidate_endpoints:
        raise InvalidCampaign(f"{run_dir}: candidate endpoint count mismatch")
    status_classes = Counter(
        "network_error"
        if item.get("status_code") is None
        else f"{int(item['status_code']) // 100}xx"
        for item in results
    )
    if dict(status_classes) != metrics.get("executed_by_http_status_class"):
        raise InvalidCampaign(f"{run_dir}: HTTP status class counts mismatch")
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


def check_signatures(
    run_dir: Path, api: str, unique: list[dict[str, Any]], correlated: list[Any]
) -> None:
    """Recompute every deduplication bucket and representative from case records."""
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
        plan = require_dict(
            representative.get("plan"), f"{run_dir}: representative plan"
        )
        case_id = plan.get("case_id")
        if case_id not in buckets[item["signature"]["id"]]:
            raise InvalidCampaign(f"{run_dir}: representative outside bucket")
        if representative != by_case[case_id].to_dict():
            raise InvalidCampaign(
                f"{run_dir}: representative differs from case records"
            )
        if item["signature"] != build_signature(api, by_case[case_id]):
            raise InvalidCampaign(f"{run_dir}: signature differs from representative")


def validate_run(run_dir: Path, api: str, commit: str) -> dict[str, Any]:
    manifest = require_dict(read_json(run_dir / "run_manifest.json"), "manifest")
    inputs, config, deduplication = check_manifest(run_dir, manifest, api, commit)
    hashes = artifact_hashes(run_dir, manifest)
    total_operations, supported_operations = count_operations(run_dir, inputs)

    records = {
        "plans": require_records(run_dir / "data/execution_plan.json"),
        "results": require_records(run_dir / "data/results.json"),
        "findings": require_records(run_dir / "analysis/analysis_findings.json"),
        "unique": require_records(run_dir / "analysis/findings_unique.json"),
    }
    correlated = correlate_records(
        records["plans"], records["results"], records["findings"]
    )
    metrics = require_dict(
        read_json(run_dir / "analysis/metrics.json"), f"{run_dir}: metrics"
    )
    check_counts(
        run_dir, manifest, metrics, deduplication, records, supported_operations
    )
    check_signatures(run_dir, api, records["unique"], correlated)

    return {
        "manifest": manifest,
        "metrics": metrics,
        "unique": records["unique"],
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
    return check_campaign(api, [validate_run(path, api, commit) for path in run_dirs])


def check_campaign(api: str, runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Check numbering and shared metadata across already validated runs."""
    if len(runs) != RUN_COUNT:
        raise InvalidCampaign(
            f"{api}: expected exactly {RUN_COUNT} runs, found {len(runs)}"
        )
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
    return check_campaign(api, valid), invalid
