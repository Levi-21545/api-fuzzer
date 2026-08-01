#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from fuzzer.analysis.run_postprocessor import CorrelationError, process_run


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deduplicate one OpenAPI Contract Fuzzer run."
    )
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    try:
        metrics = process_run(args.run_dir.resolve())
    except CorrelationError as error:
        parser.error(str(error))
    counts = metrics["counts"]
    print(
        f"{metrics['api_id']}: {counts['candidate_findings_raw']} raw candidates "
        f"-> {counts['findings_unique_operational']} unique operational findings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
