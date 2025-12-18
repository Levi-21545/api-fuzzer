import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Contract-guided API fuzzer based on OpenAPI schemas"
    )

    parser.add_argument(
        "schema",
        help="Path to OpenAPI schema file (YAML)"
    )

    parser.add_argument(
        "--base-url",
        help="Base URL of the target API"
    )

    parser.add_argument(
        "--level",
        type=int,
        default=1,
        help="Fuzzing level (0 for no mutations, higher for more aggressive fuzzing)"
    )

    parser.add_argument(
        "--max",
        type=int,
        help="Maximum number of mutations per payload"
    )

    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of endpoints to execute"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Execute all endpoints found in the schema"
    )

    parser.add_argument(
        "--path",
        dest="path_filter",
        help="Glob pattern to filter endpoint paths (e.g. /users/*)"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Diretório onde os resultados serão salvos",
    )

    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Maximum number of concurrent requests"
    )

    return parser.parse_args()
