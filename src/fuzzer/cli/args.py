import argparse
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
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
        "--auth",
        type=Path,
        help="Path for authentication configuration file (YAML)"
    )

    parser.add_argument(
        "--level",
        type=int,
        default=1,
        help="Fuzzing level (0=baseline only, 1=single mutations, 2=combined mutations)"
    )

    parser.add_argument(
        "--max",
        type=int,
        default=10,
        help="Maximum number of individual mutations per payload (default: 10)"
    )

    parser.add_argument(
        "--max-pairs",
        type=int,
        default=10,
        help="Maximum number of level-2 mutation pairs per payload (default: 10)",
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
        "--exclude-path",
        dest="excluded_paths",
        action="append",
        default=[],
        help="Glob pattern to exclude; may be specified more than once",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Diretório onde os resultados serão salvos",
    )

    parser.add_argument(
        "--run-id",
        help="Identificador explícito da execução (a pasta não pode existir)",
    )

    parser.add_argument(
        "--experiment-id",
        help="Identificador do experimento ao qual esta execução pertence",
    )

    parser.add_argument(
        "--target-id",
        help="Identificador estável da aplicação alvo",
    )

    parser.add_argument(
        "--run-number",
        type=int,
        help="Número da repetição dentro do experimento",
    )

    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Maximum number of concurrent requests (default: 5)"
    )

    parser.add_argument(
        "--delay",
        type=int,
        default=0,
        help="Delay in milliseconds between requests to avoid DoS (default: 0)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )

    parser.add_argument(
        "--auto-auth",
        action="store_true",
        help="Automatically register and login to obtain auth token from the target API"
    )

    parser.add_argument(
        "--auth-probe",
        action="store_true",
        help="Probe authenticated endpoints without token and with invalid token"
    )

    parser.add_argument(
        "--no-deduplicate",
        action="store_true",
        help="Skip automatic deduplication after a successful run",
    )

    return parser.parse_args(argv)
