import asyncio
import traceback

from fuzzer.utils.writer import (
    write_results,
    write_execution_plan,
    write_analysis_report,
)

from fuzzer.cli.args import parse_args
from fuzzer.cli.select import select_endpoints

from fuzzer.orchestrator.execution_plan_builder import (
    build_execution_plan,
    build_auth_probes,
)
from fuzzer.orchestrator.runner import ExecutionRunner
from fuzzer.orchestrator.auto_auth import bootstrap_auth
from fuzzer.orchestrator.auth_resolver import resolve_auth_headers

from fuzzer.parser.openapi_parser import parse_openapi
from fuzzer.mutator.engine import MutationEngine
from fuzzer.executor.executor import Executor

from fuzzer.analysis.analyzer import Analyzer
from fuzzer.analysis.run_postprocessor import process_run
from fuzzer.utils.helpers import timestamp
from fuzzer.utils.manifest import build_run_manifest, utc_now, write_run_manifest
from fuzzer.utils.types import Headers, AuthContext


async def async_main():
    args = parse_args()

    # 0. Create an isolated output directory for this run.
    run_id = args.run_id or timestamp().lstrip("_")
    run_dir = args.output_dir / run_id
    if run_dir.exists():
        raise SystemExit(
            f"Output directory already exists; refusing to overwrite: {run_dir}"
        )
    print(f"Output directory for this run: {run_dir}")

    data_dir = run_dir / "data"
    analysis_dir = run_dir / "analysis"
    data_dir.mkdir(parents=True)
    analysis_dir.mkdir()

    manifest = build_run_manifest(args, run_id)
    write_run_manifest(manifest, run_dir)

    try:
        # 1. Parse the OpenAPI contract.
        api_spec = parse_openapi(args.schema)

        # 2. Select endpoints using the configured filters.
        selected_endpoints = select_endpoints(
            api_spec.endpoints,
            limit=args.limit,
            all=args.all,
            path_filter=args.path_filter,
            excluded_paths=args.excluded_paths,
        )
        manifest["counts"]["selected_endpoints"] = len(selected_endpoints)

        if not selected_endpoints:
            raise RuntimeError("No endpoints selected.")

        auth_context: AuthContext = {}
        headers: Headers = {}

        if args.auth:
            headers = await resolve_auth_headers(args.auth)
        elif args.auto_auth:
            base = (
                args.base_url
                or (api_spec.base_urls[0] if api_spec.base_urls else None)
            )
            if base:
                headers, auth_context = await bootstrap_auth(api_spec, base)
            else:
                raise RuntimeError(
                    "--auto-auth requires --base-url or a server in the spec."
                )

        mutation_engine = MutationEngine(level=args.level, max_mutations=args.max)

        # 3. Build the execution plan.
        execution_plan = list(
            build_execution_plan(
                selected_endpoints,
                mutation_engine,
                auth_context,
                headers,
            )
        )

        if headers and args.auth_probe:
            probes = build_auth_probes(
                selected_endpoints,
                auth_context,
                headers,
            )
            execution_plan = probes + execution_plan

        manifest["counts"]["planned_requests"] = len(execution_plan)
        write_execution_plan(execution_plan, data_dir)
        write_run_manifest(manifest, run_dir)
        print(f"Generated {len(execution_plan)} requests to be executed.")

        print("Starting execution...")

        # 4. Configure request execution and orchestration.
        executor = Executor(
            spec=api_spec,
            override_base_url=args.base_url,
            timeout=args.timeout,
        )
        runner = ExecutionRunner(
            executor=executor,
            concurrency=args.concurrency,
            delay_ms=args.delay,
        )

        # 5. Execute the planned requests.
        results = await runner.run(execution_plan)
        manifest["counts"]["completed_requests"] = len(results)
        print("Execution completed.")

        # 6. Analyze execution results.
        print("Analyzing results...")
        analyzer = Analyzer(api_spec)
        analysis_results = analyzer.analyze_all(results, execution_plan)
        manifest["counts"]["findings"] = len(analysis_results)
        print(f"Produced {len(analysis_results)} classified findings.")

        # 7. Write the lightweight analysis report.
        report_md, report_json = write_analysis_report(
            analysis_results, analysis_dir
        )
        print(f"Analysis report saved: {report_md}")
        print(f"Findings JSON saved: {report_json}")

        write_results(results, data_dir)
        manifest["status"] = "completed"
    except Exception as error:
        manifest["status"] = "failed"
        manifest["postprocessing"]["deduplication"] = {
            "status": "not_run",
            "reason": "campaign_failed",
            "error": None,
        }
        manifest["error"] = {
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
        }
        raise
    finally:
        manifest["finished_at"] = utc_now()
        write_run_manifest(manifest, run_dir)

    if not args.no_deduplicate:
        print("Deduplicating findings...")
        metrics = process_run(run_dir)
        unique_count = metrics["counts"]["findings_unique_operational"]
        print(f"Produced {unique_count} unique operational findings.")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
