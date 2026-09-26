#!/usr/bin/env python3
"""Analyze the final repetitions and optionally export a review package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fuzzer.analysis.final_experiment.bundle import write_review_bundle
from fuzzer.analysis.final_experiment.protocol import (
    InvalidCampaign,
    discover_apis,
    select_valid_attempts,
)
from fuzzer.analysis.final_experiment.summary import summarize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only summary of five finalized repetitions for every API "
            "under an experiment root."
        )
    )
    parser.add_argument(
        "experiment_root",
        type=Path,
        help="Root containing <api>/<run-id>/run_manifest.json",
    )
    parser.add_argument("expected_commit", help="Expected clean fuzzer commit")
    parser.add_argument(
        "--review-dir",
        type=Path,
        help=(
            "write and revalidate a compact local review package; the directory "
            "must not already exist"
        ),
    )
    args = parser.parse_args(argv)
    try:
        audited = {
            api: select_valid_attempts(api, paths, args.expected_commit)
            for api, paths in discover_apis(args.experiment_root).items()
        }
        validated = {api: runs for api, (runs, _) in audited.items()}
        experiment_ids = {
            run["manifest"].get("experiment_id")
            for runs in validated.values()
            for run in runs
        }
        source_hashes = {
            run["manifest"]["fuzzer"].get("source_tree_sha256")
            for runs in validated.values()
            for run in runs
        }
        if len(experiment_ids) != 1 or len(source_hashes) != 1:
            raise InvalidCampaign("experiment or fuzzer source differs across APIs")

        summaries = {}
        for api, runs in validated.items():
            summaries[api] = summarize(api, runs)
            summaries[api]["invalid_attempts"] = audited[api][1]
        if args.review_dir is not None:
            summaries = write_review_bundle(
                args.experiment_root.resolve(),
                args.review_dir.resolve(),
                args.expected_commit,
                audited,
                summaries,
            )
        print(json.dumps(summaries, indent=2, ensure_ascii=False))
    except (InvalidCampaign, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
