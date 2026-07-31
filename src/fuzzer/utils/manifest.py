from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_source_tree(repository_root: Path) -> str:
    """Hash the source and experiment files that define an execution."""
    patterns = (
        "src/**/*.py",
        "scripts/**/*.sh",
        "experiments/**/*.yaml",
        "experiments/**/*.yml",
    )
    files = {
        path
        for pattern in patterns
        for path in repository_root.glob(pattern)
        if path.is_file()
    }
    files.update(
        path
        for name in ("pyproject.toml", "uv.lock")
        if (path := repository_root / name).is_file()
    )

    digest = hashlib.sha256()
    for path in sorted(files):
        relative_path = path.relative_to(repository_root).as_posix()
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return Path.cwd()


def _git_state() -> dict[str, Any]:
    def git(*args: str) -> str | None:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.stdout.strip() if result.returncode == 0 else None

    status = git("status", "--porcelain")
    return {
        "commit": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "dirty": bool(status) if status is not None else None,
    }


def build_run_manifest(args: Any, run_id: str) -> dict[str, Any]:
    schema = Path(args.schema).resolve()
    repository_root = _repository_root()
    return {
        "manifest_version": 1,
        "run_id": run_id,
        "experiment_id": args.experiment_id,
        "target_id": args.target_id,
        "run_number": args.run_number,
        "status": "running",
        "started_at": utc_now(),
        "finished_at": None,
        "inputs": {
            "schema": str(schema),
            "schema_sha256": sha256_file(schema),
            "base_url": args.base_url,
            "target_image": os.environ.get("API_FUZZER_TARGET_IMAGE"),
        },
        "fuzzer": {
            "git": _git_state(),
            "source_tree_sha256": sha256_source_tree(repository_root),
            "configuration": {
                "level": args.level,
                "max_mutations_per_payload": args.max,
                "endpoint_limit": args.limit,
                "all_endpoints": args.all,
                "path_filter": args.path_filter,
                "excluded_paths": args.excluded_paths,
                "auto_auth": args.auto_auth,
                "auth_probe": args.auth_probe,
                "concurrency": args.concurrency,
                "delay_ms": args.delay,
                "timeout_seconds": args.timeout,
            },
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "counts": {
            "selected_endpoints": None,
            "planned_requests": None,
            "completed_requests": None,
            "findings": None,
        },
        "artifacts": [
            "execution_plan.json",
            "results.json",
            "analysis_findings.json",
            "analysis_report.md",
            "run_manifest.json",
        ],
        "error": None,
    }


def write_run_manifest(manifest: dict[str, Any], run_dir: Path) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "run_manifest.json"
    with path.open("w", encoding="utf-8") as destination:
        json.dump(manifest, destination, indent=2, ensure_ascii=False)
    return path
