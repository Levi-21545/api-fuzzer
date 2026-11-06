// Telas do pacote final: visão geral, API e ID semântico. Todos os números
// vêm de final-analysis.json, provenance-index.json e assinaturas.csv.

import { getPackage } from "../data.js";
import { badge, bandBadge, code, countTable, fmt, fmtText, h, kvTable, linkRow, na, notice, pct, rawJson, scoreRange, section, shortId } from "../dom.js";
import { COUNT_LABELS, PACKAGE_MEASURES, PRIORITY_NOTE, countLabel } from "../labels.js";
import { BAND_RANK, PACKAGE_FILES, bandKey, joinPath, packageApis, priorityEntries, runIdByNumber, semanticRows } from "../model.js";
import { href } from "../router.js";
import { filterableTable } from "../table.js";

const TOTAL_KEYS = [
  "planned_requests",
  "executed_requests",
  "classified_observations",
  "expected_failures",
  "candidate_findings_raw",
  "findings_unique_operational",
];

export function scopeBanner(pkg) {
  return notice(
    "scope pkg",
    badge("agregado do pacote", "pkg"),
    " Números publicados pela análise final do pacote ",
    code(pkg.dir || "(raiz)"),
    ". Não incluem campanhas abertas fora dele.",
  );
}

function problemsBlock(pkg) {
  if (!pkg.problems.length) return null;
  return notice(
    pkg.fatal ? "error" : "warn",
    pkg.fatal ? "Formato incompatível com um pacote final:" : "Avisos ao ler o pacote:",
    h("ul", {}, pkg.problems.map((problem) => h("li", {}, problem))),
  );
}

export async function renderPackage(source, dir) {
  const pkg = await getPackage(source, dir);
  const base = ["pkg", source, dir];
  const header = [
    h("p", { class: "crumbs" }, h("a", { href: "#/" }, "Artefatos"), " / pacote"),
    h("h1", {}, "Pacote final ", code(dir || "(raiz)")),
    problemsBlock(pkg),
  ];
  if (pkg.fatal) return h("div", {}, header);
  const provenance = pkg.provenance ?? {};
  return h(
    "div",
    {},
    header,
    scopeBanner(pkg),
    section(
      "Proveniência",
      kvTable([
        ["Commit do fuzzer na coleta (campaign_commit)", typeof provenance.campaign_commit === "string" ? code(provenance.campaign_commit) : na("provenance-index.json")],
        ["Commit do analisador (analyzer_commit)", typeof provenance.analyzer_commit === "string" ? code(provenance.analyzer_commit) : na("provenance-index.json")],
        ["Campanhas listadas (runs)", Array.isArray(provenance.runs) ? provenance.runs.length : na("provenance-index.json")],
      ]),
      rawJson("provenance-index.json completo", provenance, joinPath(dir, PACKAGE_FILES.provenance)),
    ),
    section(
      "APIs",
      h("p", { class: "muted" }, "Cada linha soma as campanhas da API (campo totals). IDs semânticos são distintos entre as campanhas da API."),
      h(
        "div",
        { class: "scroll" },
        h(
          "table",
          { class: "data" },
          h(
            "thead",
            {},
            h(
              "tr",
              {},
              h("th", {}, "API"),
              h("th", { class: "num" }, "Campanhas"),
              TOTAL_KEYS.map((key) => h("th", { class: "num" }, COUNT_LABELS[key][0])),
              h("th", { class: "num" }, "IDs semânticos"),
            ),
          ),
          h(
            "tbody",
            {},
            packageApis(pkg).map((api) => {
              const entry = pkg.analysis[api];
              const target = href([...base, "api", api]);
              return linkRow(
                target,
                h("td", {}, h("a", { href: target }, api)),
                h("td", { class: "num" }, fmt(entry.run_ids.length)),
                TOTAL_KEYS.map((key) => h("td", { class: "num" }, fmt(entry.totals[key]))),
                h("td", { class: "num" }, fmt(entry.signature_union)),
              );
            }),
          ),
        ),
      ),
    ),
    section(
      "Arquivos do pacote",
      h(
        "ul",
        { class: "plain" },
        ["README.md", "results.md", PACKAGE_FILES.signaturesCsv, "LICENSES.md", PACKAGE_FILES.provenance, PACKAGE_FILES.analysis].map((name) =>
          h("li", {}, h("a", { href: href(["file", source, joinPath(dir, name)]) }, name)),
        ),
      ),
    ),
  );
}

export async function renderPackageApi(source, dir, api, params) {
  const pkg = await getPackage(source, dir);
  const entry = pkg.analysis?.[api];
  const base = ["pkg", source, dir];
  const crumbs = h(
    "p",
    { class: "crumbs" },
    h("a", { href: "#/" }, "Artefatos"),
    " / ",
    h("a", { href: href(base) }, "pacote"),
    ` / ${api}`,
  );
  if (!entry) return h("div", {}, crumbs, problemsBlock(pkg), notice("error", `API "${api}" não existe em final-analysis.json.`));
  const tab = ["campanhas", "ids", "resumo"].includes(params.tab) ? params.tab : "campanhas";
  const segments = [...base, "api", api];
  const tabLink = (name, label) =>
    h("a", { href: href(segments, { tab: name }), class: tab === name ? "tab active" : "tab" }, label);
  const content = {
    campanhas: () => campaignsTable(source, dir, api, pkg, entry),
    ids: () => semanticTable(source, dir, api, pkg, segments, params),
    resumo: () => apiSummary(entry, semanticRows(pkg, api)),
  }[tab]();

  return h(
    "div",
    {},
    crumbs,
    h("h1", {}, api, " ", h("span", { class: "muted" }, `— ${entry.run_ids.length} campanhas no pacote`)),
    problemsBlock(pkg),
    scopeBanner(pkg),
    h("nav", { class: "tabs" }, tabLink("campanhas", "Campanhas"), tabLink("ids", "IDs semânticos"), tabLink("resumo", "Totais, medidas e configuração")),
    content,
  );
}

// Maior score por classe entre os IDs semânticos da API (assinaturas.csv +
// final-analysis.json), para ordenar as tabelas por classe.
function classRanking(rows) {
  const ranking = new Map();
  for (const row of rows ?? []) {
    const score = row.scoreRange?.[1];
    if (!row.classification || typeof score !== "number") continue;
    if (!ranking.has(row.classification) || score > ranking.get(row.classification)) ranking.set(row.classification, score);
  }
  return ranking;
}

function apiSummary(entry, rows) {
  const ranking = classRanking(rows);
  return [
    h(
      "div",
      { class: "columns" },
      section(
        "Totais (soma das campanhas)",
        kvTable(Object.entries(entry.totals).map(([key, value]) => [countLabel(key)[0], value]), { layout: "end" }),
        h("h3", {}, "Achados brutos por classe"),
        countTable(entry.candidate_by_classification, {
          unit: "achados brutos",
          keyHeader: "Classe",
          entries: entry.candidate_by_classification ? priorityEntries(entry.candidate_by_classification, "class", ranking) : undefined,
        }),
        h("p", { class: "muted note" }, "Ordem: classe com maior score entre os IDs semânticos da API primeiro, não a maior contagem."),
      ),
      section(
        "Medidas entre campanhas",
        kvTable(
          Object.entries(PACKAGE_MEASURES)
            .filter(([key]) => key in entry)
            .map(([key, [label, scope, kind]]) => [
              h("span", {}, label, h("br"), h("small", { class: "muted" }, scope)),
              kind === "ratio" ? pct(entry[key]) : fmt(entry[key]),
            ]),
          { layout: "end" },
        ),
        h("p", { class: "muted" }, "Presença é contagem de campanhas em que o ID semântico aparece; não é medida de acerto."),
        h("h3", {}, "IDs semânticos por número de campanhas em que aparecem"),
        countTable(entry.presence_frequency, { unit: "IDs semânticos", keyHeader: "Campanhas" }),
      ),
    ),
    section(
      "Prioridade atribuída pelo FIS",
      h(
        "p",
        { class: "muted" },
        PRIORITY_NOTE,
        " Escopo: um score por assinatura estrita em cada campanha, o maior entre os seus casos (results.md).",
      ),
      h(
        "div",
        { class: "columns" },
        kvTable(
          Object.entries(entry.score_distribution_unique_per_run ?? {}).map(([key, value]) => [
            { count: "Assinaturas estritas", min: "Mínimo", median: "Mediana", max: "Máximo" }[key] ?? key,
            value,
          ]),
          { layout: "end" },
        ),
        countTable(entry.band_distribution_unique_per_run, {
          unit: "assinaturas estritas",
          keyHeader: "Faixa",
          entries: entry.band_distribution_unique_per_run ? priorityEntries(entry.band_distribution_unique_per_run, "band") : undefined,
          keyCell: (key) => bandBadge(key),
        }),
      ),
    ),
    section("Configuração (idêntica nas campanhas da API)", entry.configuration ? configTable(entry.configuration, "wide") : na("configuration")),
    Array.isArray(entry.invalid_attempts) && entry.invalid_attempts.length
      ? section("Tentativas inválidas registradas", rawJson("invalid_attempts", entry.invalid_attempts, PACKAGE_FILES.analysis))
      : null,
  ];
}

export function configTable(configuration, layout = "end") {
  return kvTable(
    Object.entries(configuration).map(([key, value]) => [
      code(key),
      // null aqui é um valor registrado (opção não usada), não um dado ausente.
      value === null ? code("null") : Array.isArray(value) ? (value.length ? value.join(", ") : "(lista vazia)") : value,
    ]),
    { layout },
  );
}

function campaignsTable(source, dir, api, pkg, entry) {
  const columns = [
    ["Requisições planejadas", (c) => c.counts?.planned_requests],
    ["Executadas", (c) => c.counts?.executed_requests],
    ["Falhas esperadas", (c) => c.counts?.expected_failures],
    ["Achados brutos", (c) => c.counts?.candidate_findings_raw],
    ["Assinaturas estritas", (c) => c.counts?.findings_unique_operational],
    ["2xx", (c) => c.http_status_classes?.["2xx"]],
    ["4xx", (c) => c.http_status_classes?.["4xx"]],
    ["5xx", (c) => c.http_status_classes?.["5xx"]],
  ];
  return section(
    "Campanhas",
    h("p", { class: "muted" }, "Valores de final-analysis.json → campaigns. Classes HTTP contam requisições executadas."),
    h(
      "div",
      { class: "scroll" },
      h(
        "table",
        { class: "data" },
        h(
          "thead",
          {},
          h(
            "tr",
            {},
            h("th", {}, "Nº"),
            h("th", {}, "Run ID"),
            h("th", { class: "num" }, "Operações selecionadas / do contrato"),
            h("th", { class: "num" }, "Duração (s)"),
            columns.map(([title]) => h("th", { class: "num" }, title)),
          ),
        ),
        h(
          "tbody",
          {},
          entry.campaigns.map((campaign) =>
            linkRow(
              href(["pkg", source, dir, "api", api, "run", campaign.run_id]),
              h("td", {}, fmt(campaign.run_number)),
              h("td", {}, h("a", { href: href(["pkg", source, dir, "api", api, "run", campaign.run_id]) }, campaign.run_id)),
              h("td", { class: "num" }, `${fmtText(campaign.selected_operations)} / ${fmtText(campaign.contract_operations)}`),
              h("td", { class: "num" }, typeof campaign.duration_seconds === "number" ? campaign.duration_seconds.toFixed(1).replace(".", ",") : na()),
              columns.map(([, get]) => h("td", { class: "num" }, fmt(get(campaign)))),
            ),
          ),
        ),
      ),
    ),
  );
}

function semanticTable(source, dir, api, pkg, segments, params) {
  const rows = semanticRows(pkg, api);
  const runCount = entryRunCount(pkg, api);
  return section(
    "IDs semânticos",
    h(
      "p",
      { class: "muted" },
      "Um ID semântico identifica o mesmo achado entre campanhas. Endpoint, classe e HTTP vêm de assinaturas.csv; presença, scores e faixas, de final-analysis.json.",
    ),
    pkg.csvState !== "ok" ? notice("warn", "assinaturas.csv ausente ou incompatível: endpoint, classe e HTTP ficam como não disponíveis.") : null,
    filterableTable({
      segments,
      params,
      rows,
      unit: "IDs semânticos",
      searchFields: ["id", "endpoint"],
      searchPlaceholder: "buscar ID ou endpoint",
      filters: [
        { name: "presenca", label: "Presença", field: "presence", options: Array.from({ length: runCount }, (_, i) => String(runCount - i)) },
        { name: "op", label: "Operação", field: "endpoint" },
        { name: "classe", label: "Classe", field: "classification" },
        { name: "http", label: "HTTP", field: "status" },
        { name: "faixa", label: "Faixa", field: "bands" },
      ],
      defaultSort: { key: "faixa", dir: "desc", label: "faixa mais alta primeiro" },
      columns: [
        { header: "ID semântico", key: "id", sort: (row) => row.id, cell: (row) => h("a", { href: href([...segments, "id", row.id]) }, shortId(row.id)) },
        { header: "Operação", key: "op", sort: (row) => row.endpoint, cell: (row) => row.endpoint ?? na() },
        { header: "Classe", key: "classe", sort: (row) => row.classification, cell: (row) => row.classification ?? na() },
        { header: "HTTP", key: "http", sort: (row) => row.status, class: "num narrow", cell: (row) => fmt(row.status) },
        { header: "Presença", key: "presenca", sort: (row) => row.presence, title: "Campanhas em que o ID aparece (contagem, não acurácia)", class: "num narrow", cell: (row) => `${row.presence}/${row.runCount}` },
        { header: "Score", key: "score", sort: (row) => row.scoreRange?.[1], title: "Mínimo–máximo entre campanhas; um valor quando são iguais. Ordena pelo máximo.", class: "num nowrap", cell: (row) => scoreRange(row.scoreRange) },
        { header: "Faixas", key: "faixa", sort: (row) => bandKey(row.bands.reduce((top, band) => ((BAND_RANK[band] ?? 0) > (BAND_RANK[top] ?? 0) ? band : top), null), row.scoreRange?.[1]), class: "nowrap", cell: (row) => (row.bands.length ? h("span", { class: "bands" }, row.bands.map(bandBadge)) : na()) },
      ],
    }),
  );
}

function entryRunCount(pkg, api) {
  return pkg.analysis[api].run_ids.length;
}

export async function renderSemanticId(source, dir, api, id) {
  const pkg = await getPackage(source, dir);
  const base = ["pkg", source, dir];
  const row = (semanticRows(pkg, api) ?? []).find((item) => item.id === id);
  const crumbs = h(
    "p",
    { class: "crumbs" },
    h("a", { href: "#/" }, "Artefatos"),
    " / ",
    h("a", { href: href(base) }, "pacote"),
    " / ",
    h("a", { href: href([...base, "api", api], { tab: "ids" }) }, api),
    " / ID semântico",
  );
  if (!row) return h("div", {}, crumbs, notice("error", `ID semântico ${id} não existe em final-analysis.json → ${api}.signatures.`));
  const numbers = runIdByNumber(pkg, api);
  const entry = pkg.analysis[api].signatures[id];
  return h(
    "div",
    {},
    crumbs,
    h("h1", {}, "ID semântico ", code(id)),
    scopeBanner(pkg),
    section(
      "Resumo publicado",
      kvTable([
        ["Operação", row.endpoint ?? na("assinaturas.csv")],
        ["Classe", row.classification ?? na("assinaturas.csv")],
        ["HTTP", row.status ?? na("assinaturas.csv")],
        ["Presença", `${row.presence} de ${row.runCount} campanhas (contagem, não acurácia)`],
        ["Campanhas (run_number)", row.presentIn.join(", ")],
        ["Score (mín–máx entre campanhas)", scoreRange(row.scoreRange)],
        ["Desvio-padrão do score (score_stdev)", entry.score_stdev],
        ["CV do tempo de resposta (response_time_cv)", entry.response_time_cv],
        ["Faixas", row.bands.length ? h("span", { class: "bands" }, row.bands.map(bandBadge)) : na()],
      ]),
      h("p", { class: "muted" }, PRIORITY_NOTE),
    ),
    section(
      "Origens nas campanhas",
      h("p", { class: "muted" }, "Cada origem liga o ID a uma assinatura estrita de uma campanha e ao caso representante dela (final-analysis.json → origins)."),
      h(
        "table",
        { class: "data" },
        h("thead", {}, h("tr", {}, ["Nº", "Campanha", "Assinatura estrita", "Caso representante"].map((title) => h("th", {}, title)))),
        h(
          "tbody",
          {},
          row.origins.map((origin) => {
            const runBase = [...base, "api", api, "run", origin.run_id];
            const number = [...numbers].find(([, runId]) => runId === origin.run_id)?.[0];
            return h(
              "tr",
              {},
              h("td", {}, fmt(number)),
              h("td", {}, h("a", { href: href(runBase) }, origin.run_id)),
              h("td", {}, h("a", { href: href([...runBase, "sig", origin.strict_signature]) }, shortId(origin.strict_signature))),
              h("td", {}, h("a", { href: href([...runBase, "case", origin.case_id]) }, origin.case_id)),
            );
          }),
        ),
      ),
    ),
    section(
      "Registros originais",
      rawJson("final-analysis.json", entry, `${joinPath(dir, PACKAGE_FILES.analysis)} → ${api}.signatures["${id}"]`),
      row.csvRow ? rawJson("assinaturas.csv", row.csvRow, joinPath(dir, PACKAGE_FILES.signaturesCsv)) : null,
    ),
  );
}
