import asyncio

from fuzzer.utils.writer import write_results, write_results_jsonl, write_execution_plan

from fuzzer.cli.args import parse_args
from fuzzer.cli.select import select_endpoints

from fuzzer.orchestrator.execution_plan_builder import build_execution_plan
from fuzzer.orchestrator.runner import ExecutionRunner
from fuzzer.orchestrator.auth_resolver import resolve_auth_headers

from fuzzer.parser.openapi_parser import parse_openapi
from fuzzer.mutator.engine import MutationEngine
from fuzzer.executor.executor import Executor


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

    # Obtém headers adicionais, se houver
    headers = {}
    if args.auth:
        headers = await resolve_auth_headers(args.auth)

    # 4. Executor + Orquestrador
    executor = Executor(
        spec=api_spec,
        override_base_url=args.base_url,
        override_headers=headers,
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
