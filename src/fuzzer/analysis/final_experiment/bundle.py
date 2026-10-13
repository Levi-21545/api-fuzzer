"""Copy accepted runs into a self-contained package and revalidate the copy."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any

from .documents import write_review_documents
from .protocol import (
    REPO_ROOT,
    InvalidCampaign,
    analyzer_git_revision,
    contract_path,
    digest,
    discover_apis,
    select_valid_attempts,
)
from .review_metadata import API_METADATA
from .summary import require_scientific_parity, summarize


def write_review_bundle(
    experiment_root: Path,
    review_root: Path,
    commit: str,
    source_audit: dict[str, tuple[list[dict[str, Any]], list[dict[str, str]]]],
    source_summaries: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Write the package, revalidate it and require the same scientific results."""
    if review_root.exists():
        raise InvalidCampaign(f"review directory already exists: {review_root}")
    if review_root.resolve() == experiment_root.resolve():
        raise InvalidCampaign("review directory cannot replace the experiment root")
    review_root.mkdir(parents=True)

    provenance_runs = []
    for api, (runs, _) in source_audit.items():
        for run in runs:
            manifest = run["manifest"]
            provenance_runs.append(
                copy_run(
                    experiment_root / api / manifest["run_id"],
                    review_root,
                    api,
                    manifest,
                )
            )
    write_licenses(review_root / "licenses", list(source_audit))

    # Validate the copy itself so the package stands on its own files.
    summaries = {}
    for api, paths in discover_apis(review_root).items():
        runs, _ = select_valid_attempts(api, paths, commit)
        summaries[api] = summarize(api, runs)
        summaries[api]["invalid_attempts"] = [
            {"run_id": item["run_id"], "reason": "retained in source only"}
            for item in source_audit[api][1]
        ]
    require_scientific_parity(source_summaries, summaries)

    provenance = {
        "campaign_commit": commit,
        "analyzer_commit": analyzer_git_revision(),
        "runs": provenance_runs,
    }
    invalid = {
        api: [item["run_id"] for item in rejected]
        for api, (_, rejected) in source_audit.items()
        if rejected
    }
    if invalid:
        provenance["invalid_attempts_not_included"] = invalid
    write_json(review_root / "provenance-index.json", provenance)
    write_review_documents(review_root, summaries, commit)
    write_json(review_root / "final-analysis.json", summaries)
    return summaries


def package_contract(api: str, manifest: dict[str, Any]) -> str:
    name = API_METADATA.get(api, {}).get("contract_file")
    if name is None:
        name = api + Path(manifest["inputs"]["schema"]).suffix
    return f"contracts/{name}"


def copy_run(
    source_dir: Path, review_root: Path, api: str, manifest: dict[str, Any]
) -> dict[str, Any]:
    """Copy one run without logs; point its manifest to the shared contract."""
    output_dir = review_root / api / manifest["run_id"]
    copied, omitted = [], []
    for relative in manifest["artifacts"]:
        if relative.endswith(".log"):
            omitted.append(relative)
            continue
        if relative == "data/target_contract.json":
            continue  # stored once under contracts/
        target = output_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_dir / relative, target)
        copied.append(relative)

    contract = package_contract(api, manifest)
    contract_copy = review_root / contract
    if not contract_copy.exists():
        contract_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contract_path(source_dir, manifest["inputs"]), contract_copy)

    adapted = deepcopy(manifest)
    adapted["artifacts"] = copied
    adapted["inputs"]["schema"] = f"../../{contract}"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "run_manifest.json", adapted)
    changed = [
        field
        for field, before, after in (
            ("artifacts", manifest["artifacts"], copied),
            (
                "inputs.schema",
                manifest["inputs"]["schema"],
                adapted["inputs"]["schema"],
            ),
        )
        if before != after
    ]
    return {
        "api": api,
        "run_id": manifest["run_id"],
        "original_manifest_sha256": digest(source_dir / "run_manifest.json"),
        "omitted_files": omitted,
        "changed_manifest_fields": changed,
    }


def write_licenses(licenses_dir: Path, apis: list[str]) -> None:
    licenses_dir.mkdir()
    for api in apis:
        metadata = API_METADATA.get(api, {})
        license_file = metadata.get("license_file")
        if "license_text" in metadata:
            (licenses_dir / metadata["license_copy"]).write_text(
                metadata["license_text"], encoding="utf-8"
            )
        elif license_file and (REPO_ROOT / license_file).is_file():
            shutil.copyfile(
                REPO_ROOT / license_file, licenses_dir / metadata["license_copy"]
            )


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
