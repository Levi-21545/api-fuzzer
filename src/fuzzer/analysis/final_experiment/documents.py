"""Render human-readable tables and reproduction guidance."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .protocol import (
    REPO_ROOT,
    analyzer_git_revision,
)
from .review_metadata import REVIEW_LICENSES, REVIEW_PROVENANCE
from .summary import illustrative_signatures


def write_review_documents(
    review_root: Path,
    summaries: dict[str, dict[str, Any]],
    commit: str,
    experiment_root: Path,
) -> None:
    """Render compact tables, provenance, and reproduction steps from validated data."""
    known_order = ("vampi", "petclinic", "crapi", "realworld", "meilisearch")
    order = [api for api in known_order if api in summaries]
    order.extend(sorted(set(summaries) - set(order)))
    labels = {
        "vampi": "VAmPI",
        "petclinic": "Spring Petclinic REST",
        "crapi": "crAPI",
        "realworld": "RealWorld/Conduit",
        "meilisearch": "Meilisearch",
    }

    def percent(value: float | None) -> str:
        return f"{value:.1%}" if value is not None else "—"

    def score(value: float | None) -> str:
        return f"{value:.2f}" if value is not None else "—"

    totals, total_status = Counter(), Counter()
    rows = []
    for api in order:
        summary = summaries[api]
        counts = summary["totals"]
        totals.update(counts)
        status = Counter()
        for campaign in summary["campaigns"]:
            status.update(campaign["http_status_classes"])
        total_status.update(status)
        rows.append(
            f"| {labels.get(api, api)} | "
            f"{counts['planned_requests']:,}/{counts['executed_requests']:,} | "
            f"{status['2xx']:,}/{status['4xx']:,}/{status['5xx']:,} | "
            f"{counts['expected_failures']:,} | {counts['candidate_findings_raw']:,} | "
            f"{counts['findings_unique_operational']:,} | "
            f"{summary['deduplication_reduction']:.1%} "
            f"| {summary['signature_union']} | "
            f"{percent(summary['reobserved_at_least_four_ratio'])} | "
            f"{percent(summary['observed_once_ratio'])} |"
        )
    raw = totals["candidate_findings_raw"]
    dedup_rate = (raw - totals["findings_unique_operational"]) / raw if raw else 0.0
    rows.append(
        f"| **Total** "
        f"| **{totals['planned_requests']:,}/{totals['executed_requests']:,}** "
        f"| **{total_status['2xx']:,}/{total_status['4xx']:,}/"
        f"{total_status['5xx']:,}** | **{totals['expected_failures']:,}** "
        f"| **{raw:,}** | "
        f"**{totals['findings_unique_operational']:,}** | **{dedup_rate:.1%}** | "
        f"**{sum(summaries[api]['signature_union'] for api in order)}** | — | — |"
    )
    lines = [
        "# Resultados da coleta final",
        "",
        f"Commit congelado das campanhas: `{commit}`.",
        "",
        (
            "| API | Planejadas/executadas | 2xx/4xx/5xx | Esperadas | Brutos | "
            "Únicos/run | Redução | União | ≥4/5 | 1/5 |"
        ),
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        *rows,
        "",
        (
            "Falhas esperadas são observações compatíveis com o contrato. HTTP "
            "4xx/5xx e zero achados não invalidam campanha. Assinaturas contam no "
            "máximo uma vez por run; união zero produz percentuais não aplicáveis. "
            "Meilisearch normaliza somente `requestUid` e `processingTimeMs` em "
            "`POST /multi-search`."
        ),
        (
            "Brutos = achados candidatos nas cinco campanhas; únicos/run = soma "
            "das assinaturas estritas de cada campanha; união = IDs semânticos "
            "distintos dentro da API. O total de união soma as cinco APIs. "
            "Classes HTTP contam resultados executados."
        ),
        "",
        "## Scores e faixas do FIS",
        "",
        "| API | N | Mínimo | Mediana | Máximo | LOW | MEDIUM | HIGH |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for api in order:
        summary = summaries[api]
        distribution = summary["score_distribution_unique_per_run"]
        bands = summary["band_distribution_unique_per_run"]
        lines.append(
            f"| {labels.get(api, api)} | {distribution['count']} | "
            f"{score(distribution['min'])} | {score(distribution['median'])} | "
            f"{score(distribution['max'])} | {bands.get('LOW', 0)} | "
            f"{bands.get('MEDIUM', 0)} | {bands.get('HIGH', 0)} |"
        )
    classes = (
        "ERROR_CONTRADICTION",
        "SERVER_ERROR",
        "SUCCESS_CONTRADICTION",
        "UNEXPECTED_ERROR_STATUS",
        "UNEXPECTED_SUCCESS",
    )
    lines.extend(
        [
            "",
            "## Classes dos achados brutos",
            "",
            "| API | " + " | ".join(classes) + " |",
            "|---|" + "---:|" * len(classes),
        ]
    )
    for api in order:
        counts = summaries[api]["candidate_by_classification"]
        lines.append(
            f"| {labels.get(api, api)} | "
            + " | ".join(str(counts.get(name, 0)) for name in classes)
            + " |"
        )
    lines.extend(
        [
            "",
            (
                "Escores e faixas são descritivos; não indicam acurácia nem confirmam "
                "vulnerabilidades. Famílias e comparação FIS × status-only permanecem "
                "restritas aos conjuntos históricos com referência. N conta um "
                "representante por assinatura estrita em cada campanha."
            ),
            "",
            "## Casos ilustrativos rastreáveis",
            "",
            (
                "Por API, selecionar o primeiro ID semântico em ordem lexical entre "
                "os observados em 5/5 e em 1/5; se nenhum desses grupos existir, "
                "usar o primeiro ID entre todos. Mostrar a primeira origem "
                "registrada para cada ID. A escolha ilustra extremos de presença, "
                "sem representar estatisticamente a API."
            ),
            "",
            "| API | Presença | Run / case_id | Endpoint | Classe | HTTP | Arquivo |",
            "|---|---:|---|---|---|---:|---|",
        ]
    )
    for api in order:
        signatures = summaries[api]["signatures"]
        for signature_id, signature in illustrative_signatures(signatures):
            origin = signature["origins"][0]
            run_id, case_id = origin["run_id"], origin["case_id"]
            finding_path = (
                review_root / api / run_id / "analysis/analysis_findings.json"
            )
            findings = json.loads(finding_path.read_text(encoding="utf-8"))
            finding = next(item for item in findings if item["case_id"] == case_id)
            lines.append(
                f"| {labels.get(api, api)} | {len(signature['present_in'])}/5 | "
                f"`{run_id}` / `{case_id}` | `{finding['endpoint_id']}` | "
                f"`{finding['classification']}` | {finding.get('status_code', '—')} | "
                f"`{api}/{run_id}/analysis/analysis_findings.json` "
                f"({signature_id[:12]}…) |"
            )
    (review_root / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    license_rows = []
    for api in order:
        if api == "meilisearch":
            continue
        license_name, _ = REVIEW_LICENSES.get(api, ("verificar upstream", ""))
        run_id = summaries[api]["run_ids"][0]
        manifest_path = review_root / api / run_id / "run_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        license_rows.append(
            f"| {labels.get(api, api)} | {REVIEW_PROVENANCE.get(api, 'upstream')} | "
            f"{license_name} | `{manifest['inputs']['schema_sha256']}` |"
        )
    license_lines = [
        "# Contratos e licenças",
        "",
        (
            "Contratos dos clones ficam referenciados por revisão e SHA-256, sem "
            "cópias extras. Os textos de licença dos quatro projetos estão em "
            "`licenses/`."
        ),
        "",
        "| API | Origem | Licença | SHA-256 |",
        "|---|---|---|---|",
        *license_rows,
    ]
    if "meilisearch" in summaries:
        run_id = summaries["meilisearch"]["run_ids"][0]
        manifest_path = review_root / "meilisearch" / run_id / "run_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        license_lines.append(
            f"| Meilisearch v1.45.1 | Asset comunitário em `contracts/` | "
            f"Redistribuição do asset ainda a comprovar | "
            f"`{manifest['inputs']['schema_sha256']}` |"
        )
        license_lines.extend(
            [
                "",
                (
                    "O contrato VAmPI não foi copiado porque contém um exemplo "
                    "com formato de JWT. O asset comunitário Meilisearch é distinto "
                    "do Enterprise ([licença e distinção](https://github.com/"
                    "meilisearch/meilisearch/issues/6010))."
                ),
            ]
        )
    (review_root / "LICENSES.md").write_text(
        "\n".join(license_lines) + "\n", encoding="utf-8"
    )

    revision = analyzer_git_revision() or "pendente (checkout com alterações locais)"
    template = (
        REPO_ROOT / "scripts/experiments/templates/final-review-readme.md"
    ).read_text(encoding="utf-8")
    replacements = {
        "{{COLLECTOR_COMMIT}}": commit,
        "{{ANALYZER_REVISION}}": revision,
        "{{EXPERIMENT_ROOT}}": (
            experiment_root.relative_to(REPO_ROOT).as_posix()
            if experiment_root.is_relative_to(REPO_ROOT)
            else "<experiment-root>"
        ),
        "{{REVIEW_DIR}}": (
            review_root.relative_to(REPO_ROOT).as_posix()
            if review_root.is_relative_to(REPO_ROOT)
            else "<review-dir>"
        ),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    if "{{" in template or "}}" in template:
        raise ValueError("unresolved review README template marker")
    (review_root / "README.md").write_text(template, encoding="utf-8")
