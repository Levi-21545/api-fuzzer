import json
from pathlib import Path

from fuzzer.executor.result import ExecutionResult

def write_results(results: list[ExecutionResult], output_dir: Path) -> None:
    output_file = output_dir / "results.json"

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