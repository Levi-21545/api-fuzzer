"""Render results.md, LICENSES.md and README.md for the review package."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .protocol import REPO_ROOT, RUN_COUNT, analyzer_git_revision
from .review_metadata import API_METADATA, LICENSE_NOTES
from .summary import illustrative_signatures

README_TEMPLATE = Path(__file__).with_name("readme_template.md")

FINDING_CLASSES = {
    "ERROR_CONTRADICTION": (
        "erro 4xx documentado, mas o corpo não é JSON ou não segue o contrato."
    ),
    "SERVER_ERROR": "resposta 5xx.",
    "SUCCESS_CONTRADICTION": (
        "resposta 2xx não documentada, ou corpo fora do contrato."
    ),
    "UNEXPECTED_ERROR_STATUS": (
        "erro 4xx não documentado para a operação, ou requisição sem resposta."
    ),
    "UNEXPECTED_SUCCESS": (
        "resposta 2xx a uma requisição que deveria ser rejeitada (payload "
        "mutado ou credencial ausente/inválida)."
    ),
}

GLOSSARY = (
    (
        "Falha esperada",
        "a API rejeitou a requisição com um erro 4xx documentado e no formato "
        "do contrato. Não é achado.",
    ),
    (
        "Achado bruto",
        "uma requisição cuja resposta foi classificada como divergência "
        "(classes abaixo). Conta cada requisição.",
    ),
    (
        "Assinatura estrita",
        "reúne, dentro de uma campanha, achados com a mesma operação, classe, "
        "status HTTP, resposta normalizada e caminho do erro de validação.",
    ),
    (
        "ID semântico",
        "identifica o mesmo achado entre campanhas. No Meilisearch, ignora "
        "`requestUid` e `processingTimeMs` em `POST /multi-search`.",
    ),
    (
        "Presença",
        f"em quantas das {RUN_COUNT} campanhas um ID semântico apareceu. Cada ID "
        "conta no máximo uma vez por campanha.",
    ),
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
        f"{len(apis) * RUN_COUNT} campanhas: {len(apis)} APIs × {RUN_COUNT} "
        f"repetições, todas com o fuzzer no commit `{commit}` e a mesma "
        "configuração.",
        "",
        "## Como ler",
        "",
        *(f"- **{term}:** {meaning}" for term, meaning in GLOSSARY),
        "",
        *execution_section(summaries, apis),
        "",
        *findings_section(summaries, apis),
        "",
        *classes_section(summaries, apis),
        "",
        *stability_section(summaries, apis),
        "",
        *fis_section(summaries, apis),
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


def number(value: int) -> str:
    """Brazilian thousands separator: 1.780."""
    return f"{value:,}".replace(",", ".")


def percent(value: float | None) -> str:
    return "—" if value is None else f"{value:.1%}".replace(".", ",")


def score(value: float | None) -> str:
    return "—" if value is None else f"{value:.2f}".replace(".", ",")


def bold(value: Any) -> str:
    return f"**{value}**"


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


def execution_section(
    summaries: dict[str, dict[str, Any]], apis: list[str]
) -> list[str]:
    keys = ("planned_requests", "executed_requests")
    statuses = ("2xx", "4xx", "5xx")
    rows, total = [], Counter()
    for api in apis:
        status = Counter()
        for campaign in summaries[api]["campaigns"]:
            status.update(campaign["http_status_classes"])
        values = [summaries[api]["totals"][key] for key in keys]
        values += [status[name] for name in statuses]
        total.update(dict(enumerate(values)))
        rows.append([label(api), *map(number, values)])
    rows.append([bold("Total"), *(bold(number(total[i])) for i in range(5))])
    return [
        "## Execução",
        "",
        *table(["API", "Planejadas", "Executadas", *statuses], "lrrrrr", rows),
        "",
        "Respostas 4xx e 5xx são resultados normais do teste e não invalidam uma "
        "campanha.",
    ]


def findings_section(
    summaries: dict[str, dict[str, Any]], apis: list[str]
) -> list[str]:
    keys = (
        "expected_failures",
        "candidate_findings_raw",
        "findings_unique_operational",
    )
    rows, total = [], Counter()
    for api in apis:
        counts = summaries[api]["totals"]
        total.update({key: counts[key] for key in keys})
        rows.append(
            [
                label(api),
                *(number(counts[key]) for key in keys),
                percent(summaries[api]["deduplication_reduction"]),
            ]
        )
    raw, unique = total["candidate_findings_raw"], total["findings_unique_operational"]
    rows.append(
        [
            bold("Total"),
            *(bold(number(total[key])) for key in keys),
            bold(percent((raw - unique) / raw if raw else 0.0)),
        ]
    )
    columns = [
        "API",
        "Falhas esperadas",
        "Achados brutos",
        "Assinaturas estritas",
        "Redução",
    ]
    return [
        "## Achados e deduplicação",
        "",
        *table(columns, "lrrrr", rows),
        "",
        f"Assinaturas estritas somam as {RUN_COUNT} campanhas. Redução = 1 − "
        "assinaturas ÷ achados brutos.",
    ]


def classes_section(summaries: dict[str, dict[str, Any]], apis: list[str]) -> list[str]:
    rows = [
        [label(api)]
        + [
            number(summaries[api]["candidate_by_classification"].get(name, 0))
            for name in FINDING_CLASSES
        ]
        for api in apis
    ]
    return [
        "## Classes dos achados brutos",
        "",
        *table(["API", *FINDING_CLASSES], "lrrrrr", rows),
        "",
        *(f"- `{name}`: {meaning}" for name, meaning in FINDING_CLASSES.items()),
    ]


def stability_section(
    summaries: dict[str, dict[str, Any]], apis: list[str]
) -> list[str]:
    presences = [str(count) for count in range(RUN_COUNT, 0, -1)]
    rows, total = [], Counter()
    for api in apis:
        summary = summaries[api]
        frequency = summary["presence_frequency"]
        total.update({"union": summary["signature_union"]})
        total.update({key: frequency[key] for key in presences})
        rows.append(
            [
                label(api),
                summary["signature_union"],
                *(frequency[key] for key in presences),
                percent(summary["reobserved_at_least_four_ratio"]),
                percent(summary["observed_once_ratio"]),
            ]
        )
    rows.append(
        [
            bold("Total"),
            bold(total["union"]),
            *(bold(total[key]) for key in presences),
            "—",
            "—",
        ]
    )
    columns = [
        "API",
        "IDs semânticos",
        *(f"em {key}/{RUN_COUNT}" for key in presences),
        f"≥ 4/{RUN_COUNT}",
        f"só 1/{RUN_COUNT}",
    ]
    return [
        "## Estabilidade entre as campanhas",
        "",
        *table(columns, "l" + "r" * (len(columns) - 1), rows),
        "",
        f'As colunas "em k/{RUN_COUNT}" contam IDs presentes em exatamente k '
        "campanhas. As duas últimas são percentuais sobre os IDs semânticos da "
        "API; não há percentual no total porque ele mistura APIs.",
    ]


def fis_section(summaries: dict[str, dict[str, Any]], apis: list[str]) -> list[str]:
    rows = []
    for api in apis:
        distribution = summaries[api]["score_distribution_unique_per_run"]
        bands = summaries[api]["band_distribution_unique_per_run"]
        rows.append(
            [
                label(api),
                number(distribution["count"]),
                score(distribution["min"]),
                score(distribution["median"]),
                score(distribution["max"]),
                *(number(bands.get(band, 0)) for band in ("LOW", "MEDIUM", "HIGH")),
            ]
        )
    columns = [
        "API",
        "Assinaturas",
        "Mínimo",
        "Mediana",
        "Máximo",
        "LOW",
        "MEDIUM",
        "HIGH",
    ]
    return [
        "## Prioridade atribuída pelo FIS",
        "",
        *table(columns, "lrrrrrrr", rows),
        "",
        "Um score por assinatura estrita em cada campanha (mesmo total da tabela "
        "de deduplicação). Os scores descrevem a prioridade de triagem "
        "atribuída; não medem acerto nem confirmam vulnerabilidades. A "
        "comparação com rótulos de referência existe só nos conjuntos "
        "históricos.",
    ]


def cases_section(
    review_root: Path, summaries: dict[str, dict[str, Any]], apis: list[str]
) -> list[str]:
    rows = []
    for api in apis:
        run_numbers = {
            campaign["run_id"]: campaign["run_number"]
            for campaign in summaries[api]["campaigns"]
        }
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
                    f"{len(signature['present_in'])}/{RUN_COUNT}",
                    f"`{finding['endpoint_id']}`",
                    f"`{finding['classification']}`",
                    finding.get("status_code", "—"),
                    f"[`{case_id}`, campanha {run_numbers[run_id]}]({findings_file})",
                    f"`{signature_id[:12]}…`",
                ]
            )
    columns = ["API", "Presença", "Endpoint", "Classe", "HTTP", "Caso", "ID semântico"]
    return [
        "## Casos ilustrativos",
        "",
        f"Para cada API, um ID presente nas {RUN_COUNT} campanhas e um presente em "
        "só 1: o primeiro de cada grupo em ordem alfabética do ID. APIs sem ID "
        f"em 1/{RUN_COUNT} têm só um caso. Os casos servem para seguir um exemplo "
        "até os dados brutos; não representam a API.",
        "",
        *table(columns, "lrllrll", rows),
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
