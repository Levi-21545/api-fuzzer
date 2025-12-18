import asyncio

from typing import Iterable, Any

from fuzzer.model.endpoint import Endpoint

from fuzzer.utils.writer import write_results, write_results_jsonl, write_execution_plan

from fuzzer.cli.args import parse_args
from fuzzer.cli.select import select_endpoints

from fuzzer.parser.openapi_parser import parse_openapi
from fuzzer.payloads.generator import generates_payloads

from fuzzer.executor.executor import Executor
from fuzzer.orchestrator.runner import ExecutionRunner
from fuzzer.mutator.engine import MutationEngine


def build_execution_plan(
        endpoints: list[Endpoint],
        mutation_engine: MutationEngine
    ) -> Iterable[tuple[Endpoint, Any | None, dict[str, str]]]:
    """
    Transforma endpoints em uma sequência de
    (endpoint, payload, headers)
    """
    for endpoint in endpoints:
        for payload, headers in generates_payloads(endpoint, mutation_engine):
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
    
    mutation_engine = MutationEngine(level=args.level, max_mutations=args.max)

    # 3. Planejamento das execuções
    execution_plan = list(build_execution_plan(selected_endpoints, mutation_engine))

    write_execution_plan(execution_plan, args.output_dir)

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

    write_results(results, args.output_dir)    
    # write_results_jsonl(results, args.output_dir)    

    # # 6. Saída bruta (análise vem depois)
    # for result in results:
    #     print(result)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
