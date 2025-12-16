import asyncio

from typing import Iterable

from fuzzer.model.endpoint import Endpoint

from fuzzer.cli.args import parse_args
from fuzzer.cli.select import select_endpoints

from fuzzer.parser.openapi_parser import parse_openapi
from fuzzer.payloads.generator import generates_payloads
from fuzzer.executor.executor import Executor
from fuzzer.orchestrator.runner import ExecutionRunner


def build_execution_plan(endpoints: list[Endpoint]) -> Iterable[tuple[Endpoint, str | None, dict[str, str]]]:
    """
    Transforma endpoints em uma sequência de
    (endpoint, payload, headers)
    """
    for endpoint in endpoints:
        for payload, headers in generates_payloads(endpoint):
            yield endpoint, payload, headers


async def async_main():
    args = parse_args()

    # 1. Parse do contrato OpenAPI
    api_spec = parse_openapi(args.schema)

    # 2. Seleção controlada de endpoints
    selected_endpoints = select_endpoints(
        api_spec.endpoints,
        limit=args.limit,
        all=args.all,
        path_filter=args.path_filter,
    )

    if not selected_endpoints:
        print("No endpoints selected. Exiting.")
        return

    # 3. Planejamento das execuções
    execution_plan = list(build_execution_plan(selected_endpoints))

    print(f"Generated {len(execution_plan)} requests to be executed.")
    print("Starting execution...")

    # 4. Executor + Orquestrador
    executor = Executor(
        spec=api_spec,
        override_base_url=args.base_url,
    )
    
    runner = ExecutionRunner(
        executor=executor,
        concurrency=args.concurrency,
    )

    # 5. Execução
    results = await runner.run(execution_plan)

    print("Execution completed.")

    # Garantir que o diretório de saída existe
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.output_dir:
        with open(args.output_dir / "results.txt", "w") as f:
            # write as json
            f.write(f"{results}\n")

    # # 6. Saída bruta (análise vem depois)
    # for result in results:
    #     print(result)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
