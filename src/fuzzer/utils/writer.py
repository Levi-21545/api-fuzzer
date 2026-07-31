import json
from pathlib import Path
from typing import Any

from collections import Counter, defaultdict
from fuzzer.executor.result import ExecutionResult
from fuzzer.analysis.result import AnalysisResult
from fuzzer.utils.types import ExecutionPlanEntry

def write_results(results: list[ExecutionResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "results.json"

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(
            [r.to_dict() for r in results],
            f,
            indent=2,
            ensure_ascii=False,
        )

def write_results_jsonl(results: list[ExecutionResult], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "results.jsonl"

    with output_file.open("w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result.to_dict(), ensure_ascii=False) + "\n")

def write_execution_plan(
    execution_plan: list[ExecutionPlanEntry],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "execution_plan.json"

    serialized = []

    for entry in execution_plan:
        serialized.append(
            {
                "case_id": entry.case_id,
                "case_kind": entry.case_kind,
                "endpoint_id": entry.endpoint.id,
                "method": entry.endpoint.method.value,
                "path": entry.path,
                "payload": entry.payload,
                "headers": entry.headers,
                "mutations": entry.mutations,
            }
        )

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(serialized, f, indent=2, ensure_ascii=False)

def write_analysis_report(
    analysis_results: list[AnalysisResult],
    output_dir: Path,
) -> tuple[Path, Path]:
    """Writes a lightweight development-time report.

    Produces:
    - Markdown summary with counts and a small sample of findings.
    - JSON list with full findings for quick inspection.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Aggregate summary
    by_class = Counter(ar.classification.name for ar in analysis_results)
    by_severity = Counter(ar.severity.name for ar in analysis_results)
    by_endpoint = defaultdict(int)
    for ar in analysis_results:
        by_endpoint[ar.endpoint_id] += 1

    total = len(analysis_results)

    # Build Markdown content
    lines: list[str] = []
    lines.append("# Relatório de Análise")
    lines.append("")
    lines.append(f"Total de resultados classificados: {total}")
    lines.append("")
    lines.append("## Por classificação")
    for name, count in sorted(by_class.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"- {name}: {count}")

    lines.append("")
    lines.append("## Por severidade")
    for name in ("HIGH", "MEDIUM", "LOW"):
        count = by_severity.get(name, 0)
        lines.append(f"- {name}: {count}")

    lines.append("")
    lines.append("## Endpoints com mais achados (top 10)")
    for ep, count in sorted(by_endpoint.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"- {ep}: {count}")

    # Sample findings per classification (up to 50 each)
    lines.append("")
    lines.append("## Amostras por classificação (até 50 cada)")

    # Bucket findings by classification preserving original order
    findings_by_class: dict[str, list[AnalysisResult]] = defaultdict(list)
    for ar in analysis_results:
        findings_by_class[ar.classification.name].append(ar)

    for name, _count in sorted(by_class.items(), key=lambda x: (-x[1], x[0])):
        lines.append("")
        lines.append(f"### {name}")
        for ar in findings_by_class.get(name, [])[:50]:
            status = ar.execution_result.status_code
            lines.append(
                f"- [{ar.classification.name}] {ar.endpoint_id} → {status} "
                f"— score={ar.severity_score} severity={ar.severity.name} — {ar.description}"
            )

    md_path = output_dir / "analysis_report.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # JSON findings (lightweight fields)
    json_path = output_dir / "analysis_findings.json"
    serializable: list[dict[str, Any]] = []
    for ar in analysis_results:
        serializable.append(
            {
                "case_id": ar.case_id,
                "classification": ar.classification.name,
                "endpoint_id": ar.endpoint_id,
                "status_code": ar.execution_result.status_code,
                "description": ar.description,
                "request_payload": ar.request_payload,
                "request_headers": ar.request_headers,
                "url": ar.execution_result.url,
                "severity_score": ar.severity_score,
                "severity": ar.severity.name,
            }
        )

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)

    return md_path, json_path
