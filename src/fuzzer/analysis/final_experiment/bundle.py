"""Build and revalidate a compact review package from accepted runs."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .documents import write_review_documents
from .protocol import (
    REPO_ROOT,
    InvalidCampaign,
    analyzer_git_revision,
    analyzer_source_hashes,
    digest,
    discover_apis,
    select_valid_attempts,
)
from .review_metadata import REVIEW_LICENSES, REVIEW_SCHEMA_REFERENCES
from .summary import require_scientific_parity, summarize


def write_review_bundle(
    experiment_root: Path,
    review_root: Path,
    commit: str,
    source_audit: dict[str, tuple[list[dict[str, Any]], list[dict[str, str]]]],
    source_summaries: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Write a compact, revalidatable review package from accepted runs."""
    if review_root.exists():
        raise InvalidCampaign(f"review directory already exists: {review_root}")
    if review_root.resolve() == experiment_root.resolve():
        raise InvalidCampaign("review directory cannot replace the experiment root")

    review_root.mkdir(parents=True)
    shared_contract_dir = review_root / "contracts"
    licenses_dir = review_root / "licenses"
    shared_contract_dir.mkdir()
    licenses_dir.mkdir()
    meili_contract_written = False
    provenance_runs = []

    for api, (runs, _) in source_audit.items():
        for run in runs:
            manifest = run["manifest"]
            source_dir = experiment_root / api / manifest["run_id"]
            output_dir = review_root / api / manifest["run_id"]
            output_dir.mkdir(parents=True)
            copied_artifacts = []
            omitted_artifacts = []
            package_paths = {}
            for relative in manifest["artifacts"]:
                path = Path(relative)
                if path.suffix == ".log":
                    omitted_artifacts.append(
                        {"path": relative, "reason": "diagnostic log kept in source"}
                    )
                    continue
                if api == "meilisearch" and relative == "data/target_contract.json":
                    package_paths[relative] = (
                        "contracts/meilisearch-v1.45.1-openapi.json"
                    )
                    if not meili_contract_written:
                        shutil.copyfile(
                            source_dir / relative,
                            shared_contract_dir / "meilisearch-v1.45.1-openapi.json",
                        )
                        meili_contract_written = True
                    continue
                source = source_dir / path
                target = output_dir / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                copied_artifacts.append(relative)
                package_paths[relative] = (
                    Path(api) / manifest["run_id"] / path
                ).as_posix()

            copied_manifest = json.loads(json.dumps(manifest))
            copied_manifest["artifacts"] = copied_artifacts
            if api == "meilisearch":
                copied_manifest["inputs"]["schema"] = (
                    "../../contracts/meilisearch-v1.45.1-openapi.json"
                )
            elif api in REVIEW_SCHEMA_REFERENCES:
                copied_manifest["inputs"]["schema"] = REVIEW_SCHEMA_REFERENCES[api]
            else:
                schema = Path(manifest["inputs"]["schema"])
                source_schema = schema if schema.is_file() else source_dir / schema
                if not source_schema.is_file():
                    raise InvalidCampaign(
                        f"{source_dir}: cannot package schema input {schema}"
                    )
                schema_target = output_dir / "data/target_contract.json"
                schema_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source_schema, schema_target)
                copied_manifest["inputs"]["schema"] = "data/target_contract.json"
            package_manifest_path = output_dir / "run_manifest.json"
            package_manifest_path.write_text(
                json.dumps(copied_manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            changed_fields = []
            if copied_manifest["artifacts"] != manifest["artifacts"]:
                changed_fields.append("artifacts")
            if copied_manifest["inputs"]["schema"] != manifest["inputs"]["schema"]:
                changed_fields.append("inputs.schema")
            artifact_mappings = {}
            for relative, package_path in sorted(package_paths.items()):
                action = "copied"
                if relative == "run_manifest.json":
                    action = "adapted"
                elif package_path.startswith("contracts/"):
                    action = "relocated"
                artifact_mappings[relative] = {
                    "action": action,
                    "package_path": package_path,
                    "source_sha256": digest(source_dir / relative),
                    "package_sha256": digest(review_root / package_path),
                }
            schema_distribution = (
                "external" if api in REVIEW_SCHEMA_REFERENCES else "included"
            )
            provenance_runs.append(
                {
                    "api_id": api,
                    "run_id": manifest["run_id"],
                    "run_number": manifest["run_number"],
                    "source_manifest_sha256": digest(source_dir / "run_manifest.json"),
                    "package_manifest_sha256": digest(package_manifest_path),
                    "contract_input": {
                        "schema_reference": copied_manifest["inputs"]["schema"],
                        "schema_sha256": manifest["inputs"]["schema_sha256"],
                        "distribution": schema_distribution,
                    },
                    "artifact_mappings": artifact_mappings,
                    "omitted_artifacts": omitted_artifacts,
                    "adapted_manifest_fields": changed_fields,
                }
            )

    for api, (license_name, license_path) in REVIEW_LICENSES.items():
        source_license = REPO_ROOT / license_path
        if source_license.is_file():
            shutil.copyfile(source_license, licenses_dir / f"{api}-LICENSE.txt")

    # Validate the copy itself so its hashes describe only files in the package.
    bundle_audit = {
        api: select_valid_attempts(api, paths, commit)
        for api, paths in discover_apis(review_root).items()
    }
    summaries = {}
    for api, (runs, _) in bundle_audit.items():
        summaries[api] = summarize(api, runs)
        summaries[api]["invalid_attempts"] = [
            {"run_id": item["run_id"], "reason": "retained in source only"}
            for item in source_audit[api][1]
        ]
    require_scientific_parity(source_summaries, summaries)
    (review_root / "provenance-index.json").write_text(
        json.dumps(
            {
                "format_version": 1,
                "collector_commit": commit,
                "analyzer_git_revision": analyzer_git_revision(),
                "analyzer_files_sha256": analyzer_source_hashes(),
                "runs": provenance_runs,
                "source_only_invalid_attempts": {
                    api: [item["run_id"] for item in invalid]
                    for api, (_, invalid) in source_audit.items()
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    write_review_documents(review_root, summaries, commit, experiment_root)
    (review_root / "final-analysis.json").write_text(
        json.dumps(summaries, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return summaries
