// Telas de uma campanha: visão geral, assinatura estrita e caso. Funciona com
// a campanha dentro do pacote (com os vínculos para IDs semânticos) ou avulsa.

import { getCampaign, getPackage } from "../data.js";
import { badge, bandBadge, code, countTable, fmt, fmtText, h, kvTable, na, notice, pre, rawJson, section, shortId, stats } from "../dom.js";
import { CLASS_HELP, COUNT_LABELS, PRIORITY_NOTE, RATE_LABELS, countLabel } from "../labels.js";
import {
  BAND_RANK,
  CAMPAIGN_FILES,
  EXPECTED_FAILURE,
  formatBody,
  joinPath,
  lookupCase,
  observationRows,
  packageCampaign,
  planRows,
  semanticIdsFor,
  signatureRows,
} from "../model.js";
import { href } from "../router.js";
import { filterableTable } from "../table.js";
import { configTable, scopeBanner } from "./package.js";

const BODY_PREVIEW_CHARS = 200_000;

// Monta o contexto da campanha a partir da rota.
export async function campaignContext(route) {
  if (route.kind === "run") {
    const campaign = await getCampaign(route.source, route.dir);
    return { ...route, base: ["run", route.source, route.dir], campaign, inPackage: null };
  }
  const pkg = await getPackage(route.source, route.pkgDir);
  const info = pkg.fatal ? null : packageCampaign(pkg, route.api, route.runId);
  if (!info) {
    return {
      ...route,
      error: `A campanha ${route.runId} não está listada em final-analysis.json → ${route.api}.run_ids.`,
      base: ["pkg", route.source, route.pkgDir, "api", route.api, "run", route.runId],
    };
  }
  const campaign = await getCampaign(route.source, info.dir);
  return {
    ...route,
    dir: info.dir,
    base: ["pkg", route.source, route.pkgDir, "api", route.api, "run", route.runId],
    campaign,
    inPackage: { pkg, api: route.api, runId: route.runId, ...info },
  };
}

function runLabel(ctx) {
  return ctx.campaign?.manifest?.run_id ?? ctx.runId ?? ctx.dir.split("/").pop() ?? ctx.dir;
}

function crumbs(ctx, ...tail) {
  const parts = [h("a", { href: "#/" }, "Artefatos")];
  if (ctx.kind === "pkg") {
    parts.push(" / ", h("a", { href: href(["pkg", ctx.source, ctx.pkgDir]) }, "pacote"));
    parts.push(" / ", h("a", { href: href(["pkg", ctx.source, ctx.pkgDir, "api", ctx.api]) }, ctx.api));
  }
  parts.push(" / ", tail.length ? h("a", { href: href(ctx.base) }, runLabel(ctx)) : runLabel(ctx));
  for (const item of tail) parts.push(" / ", item);
  return h("p", { class: "crumbs" }, parts);
}

function campaignBanner(ctx) {
  if (ctx.inPackage) {
    return notice(
      "scope run",
      badge("dados desta campanha", "run"),
      ` Campanha ${ctx.runId} do pacote `,
      code(ctx.pkgDir || "(raiz)"),
      `, API ${ctx.api}. Os números abaixo são só desta campanha; os agregados estão na página da API.`,
    );
  }
  return notice(
    "scope run",
    badge("campanha avulsa", "run"),
    " Aberta direto do diretório ",
    code(ctx.dir || "(raiz da fonte)"),
    ". Não pertence a nenhum pacote aberto aqui e não entra em agregados.",
  );
}

function fileLink(ctx, relative) {
  return h("a", { href: href(["file", ctx.source, joinPath(ctx.dir, relative)]) }, relative);
}

function origin(ctx, file, index) {
  return `${joinPath(ctx.dir, CAMPAIGN_FILES[file])}${index != null ? ` [${index}]` : ""}`;
}

function errorPage(ctx) {
  return h("div", {}, h("p", { class: "crumbs" }, h("a", { href: "#/" }, "Artefatos")), notice("error", ctx.error));
}

function problemsBlock(campaign) {
  if (!campaign.problems.length) return null;
  return notice("warn", "Avisos ao ler a campanha:", h("ul", {}, campaign.problems.map((problem) => h("li", {}, problem))));
}

// ---------------------------------------------------------------------------
// Visão geral

export async function renderCampaign(route, params) {
  const ctx = await campaignContext(route);
  if (ctx.error) return errorPage(ctx);
  const { campaign } = ctx;
  const tab = ["resumo", "assinaturas", "observacoes", "plano"].includes(params.tab) ? params.tab : "resumo";
  const tabLink = (name, label) =>
    h("a", { href: href(ctx.base, { tab: name }), class: tab === name ? "tab active" : "tab" }, label);
  const tabContent = {
    resumo: () => summaryTab(ctx),
    assinaturas: () => signaturesTab(ctx, params),
    observacoes: () => observationsTab(ctx, params),
    plano: () => planTab(ctx, params),
  }[tab]();
  const manifest = campaign.manifest;

  return h(
    "div",
    {},
    crumbs(ctx),
    h("h1", {}, "Campanha ", code(runLabel(ctx))),
    campaignBanner(ctx),
    problemsBlock(campaign),
    h(
      "p",
      { class: "facts" },
      "Alvo: ",
      fmt(manifest?.target_id),
      " · Status: ",
      manifest?.status ? badge(manifest.status, manifest.status === "completed" ? "ok" : "warn") : na(),
      " · Fuzzer: ",
      manifest?.fuzzer?.git?.commit ? code(manifest.fuzzer.git.commit.slice(0, 12)) : na(),
      " · Início: ",
      fmt(manifest?.started_at),
    ),
    h(
      "nav",
      { class: "tabs" },
      tabLink("resumo", "Configuração, proveniência e métricas"),
      tabLink("assinaturas", "Assinaturas estritas"),
      tabLink("observacoes", "Observações classificadas"),
      tabLink("plano", "Plano (todas as requisições)"),
    ),
    tabContent,
  );
}

// Resumo: contagens no topo, depois identificação, configuração, proveniência,
// distribuições e, por último, os arquivos e registros originais.
function summaryTab(ctx) {
  const manifest = ctx.campaign.manifest;
  return [
    manifest?.error ? notice("error", "A campanha registrou um erro: ", code(manifest.error.type ?? "?"), ` ${manifest.error.message ?? ""}`) : null,
    countsCard(ctx),
    manifest ? manifestCards(ctx, manifest) : section("Manifesto", na("run_manifest.json")),
    ctx.inPackage ? packageProvenance(ctx) : null,
    metricsCards(ctx),
    sourcesCard(ctx),
  ];
}

function countsCard(ctx) {
  const counts = ctx.campaign.metrics?.counts;
  const order = [
    "planned_requests",
    "executed_requests",
    "classified_observations",
    "expected_failures",
    "candidate_findings_raw",
    "findings_unique_operational",
    "candidate_endpoints",
  ];
  if (!counts) return section("Contagens", na("analysis/metrics.json"));
  const keys = [...order.filter((key) => key in counts), ...Object.keys(counts).filter((key) => !order.includes(key))];
  return section(
    "Contagens da campanha",
    stats(keys.map((key) => [countLabel(key)[0], counts[key], countLabel(key)[1]])),
    h("p", { class: "muted note" }, "Fonte: analysis/metrics.json → counts. Falhas esperadas não são achados; assinaturas estritas agrupam achados brutos desta campanha."),
  );
}

function hash(value) {
  return typeof value === "string" ? shortId(value, 16) : na();
}

function fullHash(value) {
  return typeof value === "string" ? code(value) : na();
}

function manifestCards(ctx, manifest) {
  const inputs = manifest.inputs ?? {};
  const fuzzer = manifest.fuzzer ?? {};
  const git = fuzzer.git ?? {};
  const dedup = manifest.postprocessing?.deduplication;
  return [
    h(
      "div",
      { class: "stack" },
      section(
        "Execução",
        kvTable([
          ["Run ID", manifest.run_id],
          ["Experimento", manifest.experiment_id],
          ["Alvo (target_id)", manifest.target_id],
          ["Número da run", manifest.run_number],
          ["Status", manifest.status ? badge(manifest.status, manifest.status === "completed" ? "ok" : "warn") : na()],
          ["Início", manifest.started_at],
          ["Fim", manifest.finished_at],
        ], { layout: "wide" }),
      ),
      section(
        "Alvo e contrato",
        kvTable([
          ["URL base (não acessada)", inputs.base_url],
          ["Contrato", inputs.schema],
          ["SHA-256 do contrato", fullHash(inputs.schema_sha256)],
          ["Imagem do alvo", inputs.target_image],
        ], { layout: "wide" }),
      ),
      section(
        "Revisão do fuzzer",
        kvTable([
          ["Commit", fullHash(git.commit)],
          ["Branch", git.branch],
          ["Árvore com alterações", git.dirty],
          ["SHA-256 da árvore-fonte", fullHash(fuzzer.source_tree_sha256)],
          ["Plataforma", manifest.environment?.platform],
          ["Python", manifest.environment?.python],
          ["Versão do manifesto", manifest.manifest_version],
        ], { layout: "wide" }),
      ),
    ),
    h(
      "div",
      { class: "grid cols-2" },
      section("Configuração do fuzzer", fuzzer.configuration ? configTable(fuzzer.configuration, "end") : na("fuzzer.configuration")),
      section(
        "Registro do manifesto",
        h("h3", {}, "Contagens"),
        manifest.counts ? kvTable(Object.entries(manifest.counts).map(([key, value]) => [countLabel(key)[0], value]), { layout: "end" }) : na("counts"),
        h("h3", {}, "Pós-processamento (deduplicação)"),
        dedup
          ? kvTable([
              ["Status", dedup.status],
              ["Motivo", dedup.reason],
              ["Erro", dedup.error],
            ], { layout: "end" })
          : na("postprocessing.deduplication"),
      ),
    ),
  ];
}

function packageProvenance(ctx) {
  const { provenance, summary } = ctx.inPackage;
  return h(
    "div",
    { class: "grid cols-2" },
    section(
      "Proveniência no pacote",
      h("p", { class: "muted note" }, "O manifesto foi adaptado na exportação do pacote; provenance-index.json registra o que mudou e o hash do original."),
      provenance
        ? kvTable([
            ["SHA-256 do manifesto original", hash(provenance.original_manifest_sha256)],
            ["Arquivos omitidos", Array.isArray(provenance.omitted_files) ? provenance.omitted_files.join(", ") || "nenhum" : na()],
            ["Campos do manifesto alterados", Array.isArray(provenance.changed_manifest_fields) ? provenance.changed_manifest_fields.join(", ") || "nenhum" : na()],
          ], { layout: "end" })
        : na("entrada em provenance-index.json"),
    ),
    section(
      "SHA-256 dos arquivos",
      h("p", { class: "muted note" }, "Registrados em final-analysis.json → campaigns. Exibidos, não recalculados."),
      summary?.artifact_sha256
        ? kvTable(Object.entries(summary.artifact_sha256).map(([file, value]) => [file, hash(value)]), { layout: "end" })
        : na("artifact_sha256"),
    ),
  );
}

function metricsCards(ctx) {
  const metrics = ctx.campaign.metrics;
  if (!metrics) {
    return section("Distribuições", na(ctx.campaign.files.metrics.state === "missing" ? "analysis/metrics.json ausente" : "analysis/metrics.json inválido"));
  }
  const distribution = (title, object, unit, keyHeader, note) =>
    section(title, note ? h("p", { class: "muted note" }, note) : null, countTable(object, { unit, keyHeader }));
  return [
    h("h3", { class: "band" }, "Distribuições — analysis/metrics.json"),
    h(
      "div",
      { class: "grid cols-3" },
      distribution("Requisições executadas por classe HTTP", metrics.executed_by_http_status_class, "requisições", "Classe HTTP"),
      distribution("Observações classificadas por classe", metrics.raw_by_classification, "observações", "Classe", "Inclui EXPECTED_FAILURE, que não é achado."),
      distribution("Achados brutos por classe", metrics.candidate_by_classification, "achados brutos", "Classe"),
      distribution("Assinaturas estritas por classe", metrics.unique_by_classification, "assinaturas", "Classe"),
      distribution("Assinaturas estritas por faixa", metrics.unique_by_severity, "assinaturas", "Faixa", "Faixa do caso representante. Prioridade de triagem, não gravidade."),
      distribution("Assinaturas estritas por score", metrics.unique_by_score, "assinaturas", "Score", "Score do caso representante."),
    ),
    metrics.by_execution_level ? executionLevels(metrics.by_execution_level) : null,
    h(
      "div",
      { class: "grid cols-2" },
      metrics.fuzzy_assessment ? fuzzyAssessment(metrics.fuzzy_assessment) : section("Avaliação do FIS", na("fuzzy_assessment")),
      section(
        "Razões",
        metrics.rates
          ? kvTable(Object.entries(metrics.rates).map(([key, value]) => [h("span", {}, RATE_LABELS[key] ?? key, h("br"), h("small", {}, code(key))), value]), { layout: "end" })
          : na("rates"),
      ),
    ),
  ];
}

function executionLevels(levels) {
  const order = [
    "planned_requests",
    "planned_by_case_kind",
    "executed_requests",
    "classified_observations",
    "candidate_findings_raw",
    "unique_findings_involving_level",
  ];
  const present = new Set(Object.values(levels).flatMap((level) => Object.keys(level ?? {})));
  const fields = [...order.filter((field) => present.has(field)), ...[...present].filter((field) => !order.includes(field))];
  return section(
    "Por nível de execução",
    h(
      "div",
      { class: "scroll" },
      h(
        "table",
        { class: "data" },
        h("thead", {}, h("tr", {}, h("th", {}, "Nível"), fields.map((field) => h("th", { class: field === "planned_by_case_kind" ? "" : "num", title: field }, COUNT_LABELS[field]?.[0] ?? field)))),
        h(
          "tbody",
          {},
          Object.entries(levels).map(([level, values]) =>
            h(
              "tr",
              {},
              h("td", {}, code(level)),
              fields.map((field) => {
                const value = values?.[field];
                if (value && typeof value === "object") {
                  return h("td", {}, Object.entries(value).map(([key, count]) => `${key}: ${fmtText(count)}`).join(", "));
                }
                return h("td", { class: "num" }, fmt(value));
              }),
            ),
          ),
        ),
      ),
    ),
  );
}

function fuzzyAssessment(assessment) {
  const scalars = Object.entries(assessment).filter(([, value]) => typeof value !== "object" || value === null);
  return section(
    "Avaliação do FIS",
    kvTable(scalars.map(([key, value]) => [code(key), value]), { layout: "end" }),
    assessment.unique_by_strongest_rule
      ? [
          h("h3", {}, "Regra mais forte do representante"),
          countTable(assessment.unique_by_strongest_rule, { unit: "assinaturas", keyHeader: "Regra" }),
        ]
      : null,
  );
}

function sourcesCard(ctx) {
  // Um selo novo por linha: um mesmo nó DOM só pode estar em um lugar.
  const stateBadge = (state) => ({ ok: () => badge("lido", "ok"), missing: () => badge("ausente", "warn"), invalid: () => badge("inválido", "error") })[state]();
  const { manifest, metrics } = ctx.campaign;
  const knownMetrics = new Set([
    "api_id",
    "counts",
    "raw_by_classification",
    "candidate_by_classification",
    "unique_by_classification",
    "unique_by_severity",
    "unique_by_score",
    "executed_by_http_status_class",
    "by_execution_level",
    "fuzzy_assessment",
    "rates",
  ]);
  const otherMetrics = metrics ? Object.fromEntries(Object.entries(metrics).filter(([key]) => !knownMetrics.has(key))) : {};
  return section(
    "Arquivos e registros originais",
    h(
      "table",
      { class: "data" },
      h("thead", {}, h("tr", {}, h("th", {}, "Arquivo"), h("th", {}, "Estado"))),
      h(
        "tbody",
        {},
        Object.entries(CAMPAIGN_FILES).map(([key, name]) =>
          h("tr", {}, h("td", {}, ctx.campaign.files[key].state === "missing" ? name : fileLink(ctx, name)), h("td", {}, stateBadge(ctx.campaign.files[key].state))),
        ),
      ),
    ),
    manifest ? rawJson("run_manifest.json completo", manifest, origin(ctx, "manifest")) : null,
    ctx.inPackage?.provenance ? rawJson("entrada em provenance-index.json", ctx.inPackage.provenance, joinPath(ctx.pkgDir, "provenance-index.json")) : null,
    Object.keys(otherMetrics).length ? rawJson("outros campos de metrics.json", otherMetrics, origin(ctx, "metrics")) : null,
  );
}

// ---------------------------------------------------------------------------
// Abas

function signaturesTab(ctx, params) {
  const rows = signatureRows(ctx.campaign);
  if (!rows) return section("Assinaturas estritas", na(`${CAMPAIGN_FILES.unique} ${ctx.campaign.files.unique.state === "missing" ? "ausente" : "inválido"}`));
  return section(
    "Assinaturas estritas",
    h(
      "p",
      { class: "muted" },
      "Cada linha agrupa, nesta campanha, achados brutos com a mesma operação, classe, status HTTP, resposta normalizada e caminho do erro de validação. ",
      "Faixa e score são os do caso representante (o mesmo critério de metrics.json); a coluna seguinte mostra as faixas de todos os casos.",
    ),
    filterableTable({
      segments: ctx.base,
      params,
      rows,
      unit: "assinaturas estritas",
      searchFields: ["id", "endpoint", "caseIds"],
      searchPlaceholder: "buscar assinatura, operação ou case_id",
      filters: [
        { name: "op", label: "Operação", field: "endpoint" },
        { name: "classe", label: "Classe", field: "classification" },
        { name: "http", label: "HTTP", field: "status" },
        { name: "faixa", label: "Faixa (representante)", field: "band" },
      ],
      columns: [
        { header: "Assinatura", key: "id", sort: (row) => row.id, cell: (row) => (row.id ? h("a", { href: href([...ctx.base, "sig", row.id]) }, shortId(row.id)) : na()) },
        { header: "Operação", key: "op", sort: (row) => row.endpoint, cell: (row) => fmt(row.endpoint) },
        { header: "Classe", key: "classe", sort: (row) => row.classification, cell: (row) => fmt(row.classification) },
        { header: "HTTP", key: "http", sort: (row) => row.status, class: "num", cell: (row) => fmt(row.status) },
        { header: "Casos", key: "casos", sort: (row) => row.occurrences, class: "num", cell: (row) => fmt(row.occurrences) },
        { header: "Faixa (repr.)", key: "faixa", sort: (row) => BAND_RANK[row.band] ?? null, cell: (row) => bandBadge(row.band) },
        { header: "Score (repr.)", key: "score", sort: (row) => row.score, class: "num", cell: (row) => fmt(row.score) },
        {
          header: "Faixas dos casos",
          class: "nowrap",
          cell: (row) =>
            row.unresolvedCases == null
              ? na("analysis_findings.json")
              : [h("span", { class: "bands" }, row.caseBands.map(bandBadge)), row.caseBands.length > 1 ? [" ", badge("mista", "warn")] : null, row.unresolvedCases ? [" ", badge(`${row.unresolvedCases} sem registro`, "error")] : null],
        },
      ],
    }),
  );
}

function observationsTab(ctx, params) {
  const rows = observationRows(ctx.campaign);
  if (!rows) return section("Observações classificadas", na(`${CAMPAIGN_FILES.findings} ${ctx.campaign.files.findings.state === "missing" ? "ausente" : "inválido"}`));
  return section(
    "Observações classificadas",
    notice(
      "info",
      "Registros de analysis_findings.json. Incluem falhas esperadas (EXPECTED_FAILURE), que não são achados; elas ficam ocultas a menos que a opção abaixo esteja marcada.",
    ),
    filterableTable({
      segments: ctx.base,
      params,
      rows,
      unit: "observações classificadas",
      searchFields: ["caseId", "endpoint"],
      searchPlaceholder: "buscar case_id ou operação",
      toggles: [{ name: "esperadas", label: "incluir falhas esperadas" }],
      prefilter: (all, state) => (state.esperadas === "1" ? all : all.filter((row) => row.classification !== EXPECTED_FAILURE)),
      filters: [
        { name: "op", label: "Operação", field: "endpoint" },
        { name: "classe", label: "Classe", field: "classification" },
        { name: "http", label: "HTTP", field: "status" },
        { name: "faixa", label: "Faixa", field: "band" },
      ],
      columns: [
        { header: "case_id", key: "caso", sort: (row) => row.caseId, cell: (row) => (row.caseId ? h("a", { href: href([...ctx.base, "case", row.caseId]) }, row.caseId) : na()) },
        { header: "Operação", key: "op", sort: (row) => row.endpoint, cell: (row) => fmt(row.endpoint) },
        { header: "Classe", key: "classe", sort: (row) => row.classification, cell: (row) => (row.classification === EXPECTED_FAILURE ? [row.classification, " ", badge("não é achado", "muted")] : fmt(row.classification)) },
        { header: "HTTP", key: "http", sort: (row) => row.status, class: "num", cell: (row) => fmt(row.status) },
        { header: "Faixa", key: "faixa", sort: (row) => BAND_RANK[row.band] ?? null, cell: (row) => bandBadge(row.band) },
        { header: "Score", key: "score", sort: (row) => row.score, class: "num", cell: (row) => fmt(row.score) },
        { header: "Assinatura estrita", key: "assinatura", sort: (row) => row.signatures, cell: (row) => (row.signatures.length ? row.signatures.map((id) => h("a", { href: href([...ctx.base, "sig", id]) }, shortId(id))) : "—") },
      ],
    }),
  );
}

function planTab(ctx, params) {
  const rows = planRows(ctx.campaign);
  if (!rows) return section("Plano (todas as requisições)", na(`${CAMPAIGN_FILES.plan} ${ctx.campaign.files.plan.state === "missing" ? "ausente" : "inválido"}`));
  const lookupText = { missing: "sem registro", duplicate: "case_id repetido", unavailable: "arquivo indisponível" };
  return section(
    "Plano (todas as requisições)",
    h("p", { class: "muted" }, "Um caso por registro de data/execution_plan.json. Status e classe vêm de results.json e analysis_findings.json pelo case_id."),
    filterableTable({
      segments: ctx.base,
      params,
      rows,
      unit: "casos planejados",
      searchFields: ["caseId", "endpoint", "path"],
      searchPlaceholder: "buscar case_id, operação ou path",
      filters: [
        { name: "tipo", label: "Tipo", field: "kind" },
        { name: "op", label: "Operação", field: "endpoint" },
        { name: "http", label: "HTTP", field: "status" },
        { name: "classe", label: "Classe", field: "classification" },
      ],
      columns: [
        { header: "case_id", key: "caso", sort: (row) => row.caseId, cell: (row) => (row.caseId ? h("a", { href: href([...ctx.base, "case", row.caseId]) }, row.caseId) : na()) },
        { header: "Tipo", key: "tipo", sort: (row) => row.kind, cell: (row) => fmt(row.kind) },
        { header: "Operação", key: "op", sort: (row) => row.endpoint, cell: (row) => fmt(row.endpoint) },
        { header: "Path enviado", key: "path", sort: (row) => row.path, cell: (row) => fmt(row.path) },
        { header: "Mutações", key: "mutacoes", sort: (row) => row.mutations, class: "num", cell: (row) => fmt(row.mutations) },
        { header: "HTTP", key: "http", sort: (row) => row.status, class: "num", cell: (row) => (row.resultState === "ok" ? fmt(row.status) : h("span", { class: "na" }, lookupText[row.resultState])) },
        { header: "Classe", key: "classe", sort: (row) => row.classification, cell: (row) => (row.findingState === "ok" ? fmt(row.classification) : h("span", { class: "na" }, lookupText[row.findingState])) },
      ],
    }),
  );
}

// ---------------------------------------------------------------------------
// Assinatura estrita

export async function renderSignature(route, signatureId, params = {}) {
  const ctx = await campaignContext(route);
  if (ctx.error) return errorPage(ctx);
  const { campaign } = ctx;
  const head = [crumbs(ctx, "assinatura estrita"), h("h1", {}, "Assinatura estrita ", code(signatureId)), campaignBanner(ctx)];
  if (!campaign.unique) return h("div", {}, head, notice("error", `${CAMPAIGN_FILES.unique} indisponível nesta campanha.`));
  const hit = campaign.unique.byId.get(signatureId);
  if (!hit) return h("div", {}, head, notice("error", `Nenhum registro com signature.id = ${signatureId} em ${CAMPAIGN_FILES.unique}.`));
  const item = hit.record;
  const components = item.signature?.components ?? {};
  const representativeCase = item.representative?.plan?.case_id ?? item.representative?.finding?.case_id;
  const semanticIds = ctx.inPackage ? semanticIdsFor(ctx.inPackage.pkg, ctx.api, ctx.runId, signatureId) : null;

  return h(
    "div",
    {},
    head,
    h(
      "div",
      { class: "columns" },
      section(
        "Componentes da assinatura",
        kvTable([
          ["api_id", components.api_id],
          ["Operação (endpoint_id)", components.endpoint_id],
          ["Classe", components.classification],
          ["HTTP", components.status_code],
          ["SHA-256 da resposta normalizada", components.normalized_response_sha256 ? code(components.normalized_response_sha256) : na()],
          ["Caminho do erro de validação", components.validation_error_path === null ? code("null") : components.validation_error_path],
          ["Ocorrências (occurrence_count)", item.occurrence_count],
          ["Tipos de caso", (item.case_kinds ?? []).join(", ")],
          ["Níveis de execução", (item.execution_levels ?? []).join(", ")],
        ]),
        components.classification ? h("p", { class: "muted" }, CLASS_HELP[components.classification] ?? "") : null,
      ),
      section(
        "Entre campanhas",
        ctx.inPackage
          ? semanticIds.length
            ? h(
                "ul",
                { class: "plain" },
                semanticIds.map((id) => {
                  const entry = ctx.inPackage.pkg.analysis[ctx.api].signatures[id];
                  return h(
                    "li",
                    {},
                    "ID semântico ",
                    h("a", { href: href(["pkg", ctx.source, ctx.pkgDir, "api", ctx.api, "id", id]) }, shortId(id)),
                    ` — presente em ${entry.present_in.length} de ${ctx.inPackage.pkg.analysis[ctx.api].run_ids.length} campanhas`,
                  );
                }),
              )
            : notice("warn", "Nenhuma origem de final-analysis.json aponta para esta assinatura.")
          : h("p", { class: "muted" }, "ID semântico não disponível: só existe para campanhas abertas pelo pacote final."),
      ),
    ),
    section("Resposta normalizada", pre(formatBody(item.signature?.normalized_response).text || "", "body")),
    section(
      "Casos desta assinatura",
      h("p", { class: "muted" }, "Cada case_id foi seguido até analysis_findings.json, execution_plan.json e results.json. O representante é o registro copiado em findings_unique.json → representative."),
      filterableTable({
        segments: [...ctx.base, "sig", signatureId],
        params,
        rows: (item.case_ids ?? []).map((caseId) => {
          const plan = lookupCase(campaign.plan, caseId);
          const finding = lookupCase(campaign.findings, caseId);
          const f = finding.state === "ok" ? finding.record : null;
          return {
            caseId,
            planState: plan.state,
            kind: plan.state === "ok" ? plan.record.case_kind ?? null : null,
            findingState: finding.state,
            classification: f?.classification ?? null,
            status: f?.status_code ?? null,
            band: f?.severity ?? null,
            score: f?.severity_score ?? null,
            representative: caseId === representativeCase,
          };
        }),
        unit: "casos",
        searchFields: ["caseId"],
        searchPlaceholder: "buscar case_id",
        filters: [
          { name: "tipo", label: "Tipo", field: "kind" },
          { name: "faixa", label: "Faixa", field: "band" },
        ],
        columns: [
          { header: "case_id", key: "caso", sort: (row) => row.caseId, cell: (row) => h("a", { href: href([...ctx.base, "case", row.caseId]) }, row.caseId) },
          { header: "Tipo", key: "tipo", sort: (row) => row.kind, cell: (row) => (row.planState === "ok" ? fmt(row.kind) : na(row.planState)) },
          { header: "Classe", key: "classe", sort: (row) => row.classification, cell: (row) => (row.findingState === "ok" ? fmt(row.classification) : na(row.findingState)) },
          { header: "HTTP", key: "http", sort: (row) => row.status, class: "num", cell: (row) => fmt(row.status) },
          { header: "Faixa", key: "faixa", sort: (row) => BAND_RANK[row.band] ?? null, cell: (row) => (row.findingState === "ok" ? bandBadge(row.band) : na()) },
          { header: "Score", key: "score", sort: (row) => row.score, class: "num", cell: (row) => fmt(row.score) },
          { header: "Representante", key: "repr", sort: (row) => (row.representative ? 0 : 1), title: "Representante primeiro", cell: (row) => (row.representative ? badge("representante", "pkg") : "") },
        ],
      }),
    ),
    section("Registro original", rawJson("findings_unique.json", item, origin(ctx, "unique", hit.index))),
  );
}

// ---------------------------------------------------------------------------
// Caso

function lookupNotice(state, file) {
  const text = {
    missing: `Nenhum registro com este case_id em ${file}.`,
    duplicate: `case_id repetido em ${file}; nenhum registro foi escolhido.`,
    unavailable: `${file} indisponível nesta campanha.`,
  };
  return notice(state === "missing" ? "info" : "warn", text[state]);
}

function headersTable(headers) {
  if (!headers || typeof headers !== "object") return na();
  const entries = Object.entries(headers);
  if (!entries.length) return h("p", { class: "muted" }, "Nenhum header.");
  return kvTable(entries.map(([key, value]) => [code(key), String(value)]));
}

function bodyBlock(text) {
  const formatted = formatBody(text);
  if (formatted.kind === "none") return na();
  const label = h("p", { class: "muted" }, formatted.kind === "json" ? "Corpo JSON, indentado para leitura." : "Corpo em texto puro (não interpretado).");
  if (formatted.text.length <= BODY_PREVIEW_CHARS) return [label, pre(formatted.text, "body")];
  const block = pre(formatted.text.slice(0, BODY_PREVIEW_CHARS), "body");
  const button = h(
    "button",
    {
      type: "button",
      onclick: () => {
        block.textContent = formatted.text;
        button.remove();
      },
    },
    `mostrar completo (${fmtText(formatted.text.length)} caracteres)`,
  );
  return [label, block, button];
}

function payloadBlock(payload) {
  if (payload === undefined) return na();
  if (payload === null) return h("p", { class: "muted" }, "Sem payload (null).");
  return pre(JSON.stringify(payload, null, 2), "body");
}

function mutationsTable(mutations) {
  if (!Array.isArray(mutations)) return na();
  if (!mutations.length) return h("p", { class: "muted" }, "Nenhuma mutação (caso sem payload mutado).");
  const fields = [...new Set(mutations.flatMap((mutation) => Object.keys(mutation ?? {})))];
  return h(
    "div",
    { class: "scroll" },
    h(
      "table",
      { class: "data compact" },
      h("thead", {}, h("tr", {}, fields.map((field) => h("th", {}, field)))),
      h(
        "tbody",
        {},
        mutations.map((mutation) =>
          h("tr", {}, fields.map((field) => h("td", {}, typeof mutation?.[field] === "object" && mutation[field] !== null ? JSON.stringify(mutation[field]) : fmt(mutation?.[field])))),
        ),
      ),
    ),
  );
}

// Pertinências como fichas "termo grau"; o termo com grau > 0 fica em destaque.
function membershipChips(terms) {
  const entries = Object.entries(terms ?? {});
  if (!entries.length) return na();
  return h(
    "span",
    { class: "chips" },
    entries.map(([term, degree]) => h("span", { class: degree > 0 ? "chip on" : "chip" }, term, " ", h("b", {}, fmtText(degree)))),
  );
}

function fisBlock(finding) {
  const assessment = finding.severity_assessment;
  if (!assessment) return na("severity_assessment");
  const inputs = assessment.inputs ?? {};
  const memberships = assessment.memberships ?? {};
  const variables = [...new Set([...Object.keys(inputs), ...Object.keys(memberships)])];
  const rules = Array.isArray(assessment.activated_rules) ? assessment.activated_rules : [];
  return h(
    "div",
    { class: "grid cols-2 fis" },
    h(
      "div",
      {},
      h("h3", {}, "Entradas e pertinências"),
      h(
        "table",
        { class: "data compact" },
        h("thead", {}, h("tr", {}, h("th", {}, "Variável"), h("th", { class: "num" }, "Entrada"), h("th", {}, "Pertinência por termo"))),
        h(
          "tbody",
          {},
          variables.map((variable) =>
            h("tr", {}, h("td", {}, code(variable)), h("td", { class: "num" }, fmt(inputs[variable])), h("td", {}, membershipChips(memberships[variable]))),
          ),
        ),
      ),
    ),
    h(
      "div",
      {},
      h("h3", {}, "Regras ativadas"),
      rules.length
        ? h(
            "table",
            { class: "data compact" },
            h("thead", {}, h("tr", {}, h("th", {}, "Regra"), h("th", { class: "num" }, "Força"))),
            h(
              "tbody",
              {},
              rules.map((rule) =>
                h("tr", {}, h("td", {}, code(rule?.id ?? "?"), h("div", { class: "muted" }, fmt(rule?.description))), h("td", { class: "num" }, fmt(rule?.strength))),
              ),
            ),
          )
        : h("p", { class: "muted" }, "Nenhuma regra registrada."),
    ),
  );
}

// Faixa de resumo do achado: classe, faixa, score, modelo e fallback.
function findingFacts(f) {
  const assessment = f.severity_assessment;
  const item = (label, value, wide) => h("div", { class: wide ? "fact wide" : "fact" }, h("div", { class: "label" }, label), h("div", { class: "value" }, value));
  return h(
    "div",
    { class: "facts-row" },
    item("Classe", f.classification === EXPECTED_FAILURE ? [f.classification, " ", badge("não é achado", "muted")] : fmt(f.classification), true),
    item("Faixa de prioridade", bandBadge(f.severity)),
    item("Score", fmt(f.severity_score)),
    item("Fallback", assessment ? fmt(assessment.fallback_used) : na()),
    item("Modelo do FIS", assessment ? code(assessment.model_id ?? "?") : na("severity_assessment"), true),
  );
}

export async function renderCase(route, caseId) {
  const ctx = await campaignContext(route);
  if (ctx.error) return errorPage(ctx);
  const { campaign } = ctx;
  const plan = lookupCase(campaign.plan, caseId);
  const result = lookupCase(campaign.results, caseId);
  const finding = lookupCase(campaign.findings, caseId);
  const p = plan.state === "ok" ? plan.record : null;
  const r = result.state === "ok" ? result.record : null;
  const f = finding.state === "ok" ? finding.record : null;
  const signatures = campaign.unique?.byCase.get(caseId) ?? [];

  return h(
    "div",
    {},
    crumbs(ctx, `caso ${caseId}`),
    h("h1", {}, "Caso ", code(caseId), " ", h("span", { class: "muted" }, p?.endpoint_id ?? f?.endpoint_id ?? r?.endpoint_id ?? "")),
    campaignBanner(ctx),
    section(
      "Vínculos",
      kvTable([
        ["Tipo de caso", p ? fmt(p.case_kind) : na()],
        ["Teste de acesso (auth_probe_kind)", p ? (p.auth_probe_kind === null ? code("null") : fmt(p.auth_probe_kind)) : na()],
        [
          "Assinatura estrita",
          !campaign.unique
            ? na(CAMPAIGN_FILES.unique)
            : signatures.length
              ? h("span", {}, signatures.map((id) => h("a", { href: href([...ctx.base, "sig", id]) }, shortId(id))))
              : "nenhuma (o caso não é achado bruto)",
        ],
        [
          "ID semântico",
          ctx.inPackage
            ? h(
                "span",
                {},
                signatures
                  .flatMap((id) => semanticIdsFor(ctx.inPackage.pkg, ctx.api, ctx.runId, id))
                  .map((id) => h("a", { href: href(["pkg", ctx.source, ctx.pkgDir, "api", ctx.api, "id", id]) }, shortId(id))),
              )
            : na("só no pacote final"),
        ],
      ]),
    ),
    h(
      "div",
      { class: "compare" },
      section(
        "Requisição",
        plan.state !== "ok" ? lookupNotice(plan.state, CAMPAIGN_FILES.plan) : null,
        p
          ? [
              kvTable([
                ["Método", p.method],
                ["Path enviado", p.path],
                ["URL registrada no resultado", r ? r.url : na()],
              ]),
              h("h3", {}, "Headers do plano"),
              headersTable(p.headers),
              h("h3", {}, "Payload"),
              payloadBlock(p.payload),
              h("h3", {}, "Mutações"),
              mutationsTable(p.mutations),
            ]
          : null,
      ),
      section(
        "Resposta",
        result.state !== "ok" ? lookupNotice(result.state, CAMPAIGN_FILES.results) : null,
        r
          ? [
              kvTable([
                ["Status HTTP", r.status_code],
                ["Tempo de resposta (ms)", r.response_time_ms],
                ["Tamanho (bytes)", r.response_size],
                ["Erro de execução", r.error === null ? code("null") : r.error],
              ]),
              h("h3", {}, "Corpo (raw_response)"),
              bodyBlock(r.raw_response),
            ]
          : null,
      ),
    ),
    section(
      "Classificação e FIS",
      finding.state !== "ok" ? lookupNotice(finding.state, CAMPAIGN_FILES.findings) : null,
      f
        ? [
            findingFacts(f),
            h(
              "div",
              { class: "finding-text" },
              h("p", {}, h("span", { class: "muted" }, "Descrição do analisador: "), fmt(f.description)),
              CLASS_HELP[f.classification] ? h("p", { class: "muted note" }, CLASS_HELP[f.classification]) : null,
              h("p", { class: "muted note" }, PRIORITY_NOTE),
            ),
            fisBlock(f),
          ]
        : null,
    ),
    section(
      "Registros originais",
      p ? rawJson("execution_plan.json", p, origin(ctx, "plan", plan.index)) : null,
      r ? rawJson("results.json", r, origin(ctx, "results", result.index)) : null,
      f ? rawJson("analysis_findings.json", f, origin(ctx, "findings", finding.index)) : null,
      [plan, result, finding]
        .filter((hit) => hit.state === "duplicate")
        .map((hit) => hit.entries.map((entry) => rawJson(`registro duplicado [${entry.index}]`, entry.record, null))),
    ),
  );
}
