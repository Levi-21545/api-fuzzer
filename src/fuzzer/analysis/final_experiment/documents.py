"""Render results.md, LICENSES.md and README.md for the review package."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .protocol import README_TEMPLATE, REPO_ROOT, analyzer_git_revision
from .review_metadata import API_METADATA, LICENSE_NOTES
from .summary import illustrative_signatures

FINDING_CLASSES = (
    "ERROR_CONTRADICTION",
    "SERVER_ERROR",
    "SUCCESS_CONTRADICTION",
    "UNEXPECTED_ERROR_STATUS",
    "UNEXPECTED_SUCCESS",
)

FIS_NOTE = (
    "Escores e faixas são descritivos; não indicam acurácia nem confirmam "
    "vulnerabilidades. Famílias e comparação FIS × status-only permanecem "
    "restritas aos conjuntos históricos com referência. N conta um "
    "representante por assinatura estrita em cada campanha."
)


def write_review_documents(
    review_root: Path,
    summaries: dict[str, dict[str, Any]],
    commit: str,
    experiment_root: Path,
) -> None:
    """Render the package documents from validated summaries."""
    apis = [api for api in API_METADATA if api in summaries]
    apis += sorted(set(summaries) - set(apis))
    results = [
        "# Resultados da coleta final",
        "",
        f"Commit congelado das campanhas: `{commit}`.",
        "",
        *overview_section(summaries, apis),
        "",
        *fis_section(summaries, apis),
        "",
        *classes_section(summaries, apis),
        "",
        FIS_NOTE,
        "",
        *cases_section(review_root, summaries, apis),
    ]
    write_lines(review_root / "results.md", results)
    write_lines(
        review_root / "LICENSES.md", licenses_document(review_root, summaries, apis)
    )
    (review_root / "README.md").write_text(
        readme_document(review_root, commit, experiment_root), encoding="utf-8"
    )


def label(api: str) -> str:
    return API_METADATA.get(api, {}).get("label", api)


def percent(value: float | None) -> str:
    return f"{value:.1%}" if value is not None else "—"


def score(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else "—"


def table(columns: list[str], align: str, rows: list[list[Any]]) -> list[str]:
    """Markdown table; `align` has one letter per column, l(eft) or r(ight)."""
    separator = "|".join("---:" if side == "r" else "---" for side in align)
    return [
        "| " + " | ".join(columns) + " |",
        f"|{separator}|",
        *("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows),
    ]


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def overview_section(
    summaries: dict[str, dict[str, Any]], apis: list[str]
) -> list[str]:
    rows, totals, total_status = [], Counter(), Counter()
    for api in apis:
        summary = summaries[api]
        counts = summary["totals"]
        status = Counter()
        for campaign in summary["campaigns"]:
            status.update(campaign["http_status_classes"])
        totals.update(counts)
        total_status.update(status)
        rows.append(
            [
                label(api),
                f"{counts['planned_requests']:,}/{counts['executed_requests']:,}",
                f"{status['2xx']:,}/{status['4xx']:,}/{status['5xx']:,}",
                f"{counts['expected_failures']:,}",
                f"{counts['candidate_findings_raw']:,}",
                f"{counts['findings_unique_operational']:,}",
                f"{summary['deduplication_reduction']:.1%}",
                summary["signature_union"],
                percent(summary["reobserved_at_least_four_ratio"]),
                percent(summary["observed_once_ratio"]),
            ]
        )
    raw = totals["candidate_findings_raw"]
    unique = totals["findings_unique_operational"]
    rows.append(
        [
            "**Total**",
            f"**{totals['planned_requests']:,}/{totals['executed_requests']:,}**",
            f"**{total_status['2xx']:,}/{total_status['4xx']:,}/"
            f"{total_status['5xx']:,}**",
            f"**{totals['expected_failures']:,}**",
            f"**{raw:,}**",
            f"**{unique:,}**",
            f"**{(raw - unique) / raw if raw else 0.0:.1%}**",
            f"**{sum(summaries[api]['signature_union'] for api in apis)}**",
            "—",
            "—",
        ]
    )
    columns = [
        "API",
        "Planejadas/executadas",
        "2xx/4xx/5xx",
        "Esperadas",
        "Brutos",
        "Únicos/run",
        "Redução",
        "União",
        "≥4/5",
        "1/5",
    ]
    return [
        *table(columns, "lrrrrrrrrr", rows),
        "",
        "Falhas esperadas são observações compatíveis com o contrato. HTTP "
        "4xx/5xx e zero achados não invalidam campanha. Assinaturas contam no "
        "máximo uma vez por run; união zero produz percentuais não aplicáveis. "
        "Meilisearch normaliza somente `requestUid` e `processingTimeMs` em "
        "`POST /multi-search`.",
        "Brutos = achados candidatos nas cinco campanhas; únicos/run = soma "
        "das assinaturas estritas de cada campanha; união = IDs semânticos "
        "distintos dentro da API. O total de união soma as cinco APIs. "
        "Classes HTTP contam resultados executados.",
    ]


def fis_section(summaries: dict[str, dict[str, Any]], apis: list[str]) -> list[str]:
    rows = []
    for api in apis:
        distribution = summaries[api]["score_distribution_unique_per_run"]
        bands = summaries[api]["band_distribution_unique_per_run"]
        rows.append(
            [
                label(api),
                distribution["count"],
                score(distribution["min"]),
                score(distribution["median"]),
                score(distribution["max"]),
                *(bands.get(band, 0) for band in ("LOW", "MEDIUM", "HIGH")),
            ]
        )
    columns = ["API", "N", "Mínimo", "Mediana", "Máximo", "LOW", "MEDIUM", "HIGH"]
    return ["## Scores e faixas do FIS", "", *table(columns, "lrrrrrrr", rows)]


def classes_section(summaries: dict[str, dict[str, Any]], apis: list[str]) -> list[str]:
    rows = [
        [label(api)]
        + [
            summaries[api]["candidate_by_classification"].get(name, 0)
            for name in FINDING_CLASSES
        ]
        for api in apis
    ]
    columns = ["API", *FINDING_CLASSES]
    return ["## Classes dos achados brutos", "", *table(columns, "lrrrrr", rows)]


def cases_section(
    review_root: Path, summaries: dict[str, dict[str, Any]], apis: list[str]
) -> list[str]:
    rows = []
    for api in apis:
        for signature_id, signature in illustrative_signatures(
            summaries[api]["signatures"]
        ):
            origin = signature["origins"][0]
            run_id, case_id = origin["run_id"], origin["case_id"]
            findings_file = f"{api}/{run_id}/analysis/analysis_findings.json"
            findings = json.loads((review_root / findings_file).read_text("utf-8"))
            finding = next(item for item in findings if item["case_id"] == case_id)
            rows.append(
                [
                    label(api),
                    f"{len(signature['present_in'])}/5",
                    f"`{run_id}` / `{case_id}`",
                    f"`{finding['endpoint_id']}`",
                    f"`{finding['classification']}`",
                    finding.get("status_code", "—"),
                    f"`{findings_file}`",
                    f"`{signature_id[:12]}…`",
                ]
            )
    columns = [
        "API",
        "Presença",
        "Run / case_id",
        "Endpoint",
        "Classe",
        "HTTP",
        "Arquivo",
        "ID semântico (prefixo)",
    ]
    return [
        "## Casos ilustrativos rastreáveis",
        "",
        "Por API, selecionar o primeiro ID semântico em ordem lexical entre "
        "os observados em 5/5 e em 1/5; se nenhum desses grupos existir, "
        "usar o primeiro ID entre todos. Mostrar a primeira origem "
        "registrada para cada ID. A escolha ilustra extremos de presença, "
        "sem representar estatisticamente a API.",
        "",
        *table(columns, "lrlllrll", rows),
    ]


def licenses_document(
    review_root: Path, summaries: dict[str, dict[str, Any]], apis: list[str]
) -> list[str]:
    rows = []
    for api in apis:
        metadata = API_METADATA.get(api, {})
        run_id = summaries[api]["run_ids"][0]
        manifest_file = review_root / api / run_id / "run_manifest.json"
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        rows.append(
            [
                metadata.get("contract_label", label(api)),
                metadata.get("source", "upstream"),
                metadata.get("license", "verificar upstream"),
                f"`{manifest['inputs']['schema_sha256']}`",
            ]
        )
    lines = [
        "# Contratos e licenças",
        "",
        "Contratos dos clones ficam referenciados por revisão e SHA-256, sem "
        "cópias extras. Os textos de licença dos quatro projetos estão em "
        "`licenses/`; o aviso MIT do asset Meilisearch também está incluído lá.",
        "",
        *table(["API", "Origem", "Licença", "SHA-256"], "llll", rows),
    ]
    for api, note in LICENSE_NOTES:
        if api in apis:
            lines += ["", note]
    return lines


def readme_document(review_root: Path, commit: str, experiment_root: Path) -> str:
    def relative(path: Path, placeholder: str) -> str:
        if path.is_relative_to(REPO_ROOT):
            return path.relative_to(REPO_ROOT).as_posix()
        return placeholder

    text = README_TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "{{COLLECTOR_COMMIT}}": commit,
        "{{ANALYZER_REVISION}}": analyzer_git_revision()
        or "pendente (checkout com alterações locais)",
        "{{EXPERIMENT_ROOT}}": relative(experiment_root, "<experiment-root>"),
        "{{REVIEW_DIR}}": relative(review_root, "<review-dir>"),
    }
    for marker, value in replacements.items():
        text = text.replace(marker, value)
    if "{{" in text or "}}" in text:
        raise ValueError("unresolved review README template marker")
    return text
