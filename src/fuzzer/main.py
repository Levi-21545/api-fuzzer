import asyncio

from fuzzer.utils.writer import (
    write_results,
    write_execution_plan,
    write_analysis_report,
)

from fuzzer.cli.args import parse_args
from fuzzer.cli.select import select_endpoints

from fuzzer.orchestrator.execution_plan_builder import build_execution_plan
from fuzzer.orchestrator.runner import ExecutionRunner
from fuzzer.orchestrator.auth_resolver import resolve_auth_headers

from fuzzer.parser.openapi_parser import parse_openapi
from fuzzer.mutator.engine import MutationEngine
from fuzzer.executor.executor import Executor

from fuzzer.analysis.analyzer import Analyzer
from fuzzer.utils.helpers import timestamp


async def async_main():
    args = parse_args()

    # 0. Define pasta da execução (por timestamp)
    run_id = timestamp().lstrip("_")
    run_dir = args.output_dir / run_id
    print(f"Output directory for this run: {run_dir}")

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
    write_execution_plan(execution_plan, run_dir)
    print(f"Generated {len(execution_plan)} requests to be executed.")

    print("Starting execution...")

    # Obtém headers adicionais, se houver
    headers = await resolve_auth_headers(args.auth) if args.auth else {}

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

    # 6. Análise dos Resultados
    print("Analyzing results...")
    analyzer = Analyzer(api_spec)
    analysis_results = analyzer.analyze_all(results, execution_plan)
    print(f"Found {len(analysis_results)} anomalies.")

    # 7. Relatório leve de análise
    report_md, report_json = write_analysis_report(analysis_results, run_dir)
    print(f"Analysis report saved: {report_md}")
    print(f"Findings JSON saved: {report_json}")

    write_results(results, run_dir)
    # write_results_jsonl(results, args.output_dir)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
