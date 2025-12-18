import json
from pathlib import Path
from typing import Any
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.endpoint import Endpoint

from fuzzer.utils.helpers import timestamp

def write_results(results: list[ExecutionResult], output_dir: Path) -> None:
    output_file = output_dir / ("results" + timestamp() + ".json")

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(
            [r.to_dict() for r in results],
            f,
            indent=2,
            ensure_ascii=False,
        )

def write_results_jsonl(results, output_dir: Path):
    output_file = output_dir / "results.jsonl"

    with output_file.open("w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result.to_dict(), ensure_ascii=False) + "\n")

def write_execution_plan(
    execution_plan: list[tuple[Endpoint, Any | None, dict[str, str]]],
    output_dir: Path,
) -> None:
    output_file = output_dir / ("execution_plan" + timestamp() + ".json")

    serialized = []

    for endpoint, payload, headers in execution_plan:
        serialized.append(
            {
                "endpoint_id": f"{endpoint.method.value} {endpoint.path}",
                "method": endpoint.method.value,
                "path": endpoint.path,
                "payload": payload,
                "headers": headers,
            }
        )

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(serialized, f, indent=2, ensure_ascii=False)