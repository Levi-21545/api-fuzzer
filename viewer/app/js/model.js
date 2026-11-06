// Leitura e vínculo dos artefatos do fuzzer. Sem DOM: os testes rodam no Node.
//
// Nada aqui recalcula métricas, FIS, deduplicação ou IDs semânticos. As
// funções só leem os arquivos, conferem o formato e indexam registros pelos
// identificadores que os próprios artefatos trazem (case_id, signature.id,
// origins). A posição de um registro no array só é usada para apontar onde ele
// está no arquivo de origem.

export const EXPECTED_FAILURE = "EXPECTED_FAILURE";

export const CAMPAIGN_FILES = {
  manifest: "run_manifest.json",
  plan: "data/execution_plan.json",
  results: "data/results.json",
  findings: "analysis/analysis_findings.json",
  unique: "analysis/findings_unique.json",
  metrics: "analysis/metrics.json",
};

const CAMPAIGN_SHAPES = {
  manifest: "object",
  plan: "array",
  results: "array",
  findings: "array",
  unique: "array",
  metrics: "object",
};

export const PACKAGE_FILES = {
  analysis: "final-analysis.json",
  provenance: "provenance-index.json",
  signaturesCsv: "assinaturas.csv",
};

const PACKAGE_API_FIELDS = {
  run_ids: "array",
  campaigns: "array",
  signatures: "object",
  totals: "object",
};

const PROVENANCE_FIELDS = ["campaign_commit", "analyzer_commit"];

const CSV_COLUMNS =["api", "id_semantico", "endpoint", "classe", "http", "presenca"];

export function joinPath(...parts) {
  return parts.filter((part) => part !== "" && part != null).join("/");
}

export function kindOf(value) {
  if (Array.isArray(value)) return "array";
  if (value === null) return "null";
  return typeof value;
}

// Lê um JSON pelo `reader` e devolve o estado do arquivo, sem lançar erro
// para arquivo ausente ou malformado.
export async function readJson(reader, path, shape) {
  const text = await reader.text(path);
  if (text === null) return { state: "missing", path };
  let data;
  try {
    data = JSON.parse(text);
  } catch (error) {
    return { state: "invalid", path, message: `JSON inválido: ${error.message}` };
  }
  if (shape && kindOf(data) !== shape) {
    return {
      state: "invalid",
      path,
      message: `esperado ${shape === "array" ? "uma lista" : "um objeto"} no topo, encontrado ${kindOf(data)}`,
    };
  }
  return { state: "ok", path, data };
}

// Indexa registros por case_id. Repetições ficam em `duplicates` e não são
// resolvidas: quem consulta recebe todas e mostra o conflito.
export function indexByCaseId(records) {
  const byId = new Map();
  const duplicates = new Set();
  let withoutId = 0;
  (records ?? []).forEach((record, index) => {
    const id = record?.case_id;
    if (typeof id !== "string") {
      withoutId += 1;
      return;
    }
    const entries = byId.get(id);
    if (entries) {
      entries.push({ record, index });
      duplicates.add(id);
    } else {
      byId.set(id, [{ record, index }]);
    }
  });
  return { byId, duplicates: [...duplicates], withoutId, size: (records ?? []).length };
}

// Busca de um case_id num índice: {state: ok|missing|duplicate|unavailable}.
export function lookupCase(index, caseId) {
  if (!index) return { state: "unavailable" };
  const entries = index.byId.get(caseId);
  if (!entries) return { state: "missing" };
  if (entries.length > 1) return { state: "duplicate", entries };
  return { state: "ok", ...entries[0] };
}

function indexUnique(records) {
  const byId = new Map();
  const byCase = new Map();
  const problems = [];
  (records ?? []).forEach((record, index) => {
    const id = record?.signature?.id;
    if (typeof id !== "string") {
      problems.push(`findings_unique.json[${index}] sem signature.id`);
      return;
    }
    if (byId.has(id)) problems.push(`signature.id repetido em findings_unique.json: ${id}`);
    byId.set(id, { record, index });
    const caseIds = Array.isArray(record.case_ids) ? record.case_ids : [];
    if (!Array.isArray(record.case_ids)) {
      problems.push(`findings_unique.json[${index}] sem case_ids`);
    }
    for (const caseId of caseIds) {
      const owners = byCase.get(caseId) ?? [];
      owners.push(id);
      byCase.set(caseId, owners);
    }
  });
  return { byId, byCase, problems };
}

export async function loadCampaign(reader, dir) {
  const files = {};
  await Promise.all(
    Object.entries(CAMPAIGN_FILES).map(async ([key, name]) => {
      files[key] = await readJson(reader, joinPath(dir, name), CAMPAIGN_SHAPES[key]);
    }),
  );
  return buildCampaign(dir, files);
}

export function buildCampaign(dir, files) {
  const data = (key) => (files[key].state === "ok" ? files[key].data : null);
  const campaign = {
    dir,
    files,
    manifest: data("manifest"),
    metrics: data("metrics"),
    plan: data("plan") ? indexByCaseId(data("plan")) : null,
    results: data("results") ? indexByCaseId(data("results")) : null,
    findings: data("findings") ? indexByCaseId(data("findings")) : null,
    uniqueList: data("unique"),
    unique: data("unique") ? indexUnique(data("unique")) : null,
    problems: [],
  };
  const present = Object.values(files).filter((file) => file.state !== "missing");
  if (present.length === 0) {
    campaign.problems.push(
      `nenhum arquivo de campanha encontrado (${Object.values(CAMPAIGN_FILES).join(", ")})`,
    );
  }
  for (const [key, file] of Object.entries(files)) {
    if (file.state === "invalid") campaign.problems.push(`${file.path}: ${file.message}`);
    const index = campaign[key];
    if (index?.duplicates?.length) {
      campaign.problems.push(
        `${CAMPAIGN_FILES[key]}: case_id repetido (${index.duplicates.slice(0, 5).join(", ")}${index.duplicates.length > 5 ? ", …" : ""})`,
      );
    }
    if (index?.withoutId) {
      campaign.problems.push(`${CAMPAIGN_FILES[key]}: ${index.withoutId} registro(s) sem case_id`);
    }
  }
  if (campaign.unique) campaign.problems.push(...campaign.unique.problems);
  return campaign;
}

// ---------------------------------------------------------------------------
// Linhas das tabelas de uma campanha

// Uma linha por assinatura estrita de findings_unique.json. A faixa e o score
// são os do representante (mesmo critério de metrics.json). As faixas de cada
// caso vêm de analysis_findings.json, pelo case_id.
export function signatureRows(campaign) {
  if (!campaign.uniqueList) return null;
  return campaign.uniqueList.map((item, index) => {
    const components = item?.signature?.components ?? {};
    const representative = item?.representative?.finding ?? {};
    const caseIds = Array.isArray(item?.case_ids) ? item.case_ids : [];
    const caseBands = new Set();
    let unresolved = 0;
    for (const caseId of caseIds) {
      const hit = lookupCase(campaign.findings, caseId);
      if (hit.state === "ok") caseBands.add(hit.record.severity ?? "—");
      else unresolved += 1;
    }
    return {
      index,
      id: item?.signature?.id ?? null,
      endpoint: components.endpoint_id ?? null,
      classification: components.classification ?? null,
      status: components.status_code ?? null,
      occurrences: item?.occurrence_count ?? null,
      caseIds,
      representativeCase: item?.representative?.plan?.case_id ?? representative.case_id ?? null,
      band: representative.severity ?? null,
      score: representative.severity_score ?? null,
      caseBands: [...caseBands].sort(),
      unresolvedCases: campaign.findings ? unresolved : null,
    };
  });
}

// Uma linha por registro de analysis_findings.json (inclui falhas esperadas).
export function observationRows(campaign) {
  if (campaign.files.findings.state !== "ok") return null;
  return campaign.files.findings.data.map((finding, index) => ({
    index,
    caseId: finding?.case_id ?? null,
    endpoint: finding?.endpoint_id ?? null,
    classification: finding?.classification ?? null,
    status: finding?.status_code ?? null,
    band: finding?.severity ?? null,
    score: finding?.severity_score ?? null,
    signatures: campaign.unique?.byCase.get(finding?.case_id) ?? [],
  }));
}

// Uma linha por caso planejado, com o resultado e a classificação do mesmo
// case_id quando existirem.
export function planRows(campaign) {
  if (campaign.files.plan.state !== "ok") return null;
  return campaign.files.plan.data.map((plan, index) => {
    const result = lookupCase(campaign.results, plan?.case_id);
    const finding = lookupCase(campaign.findings, plan?.case_id);
    return {
      index,
      caseId: plan?.case_id ?? null,
      kind: plan?.case_kind ?? null,
      endpoint: plan?.endpoint_id ?? null,
      method: plan?.method ?? null,
      path: plan?.path ?? null,
      mutations: Array.isArray(plan?.mutations) ? plan.mutations.length : null,
      status: result.state === "ok" ? result.record.status_code : null,
      resultState: result.state,
      classification: finding.state === "ok" ? finding.record.classification : null,
      findingState: finding.state,
    };
  });
}

// ---------------------------------------------------------------------------
// Pacote final

export function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    if (quoted) {
      if (char === '"' && text[i + 1] === '"') {
        field += '"';
        i += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n" || char === "\r") {
      if (char === "\r" && text[i + 1] === "\n") i += 1;
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }
  if (field !== "" || row.length) {
    row.push(field);
    rows.push(row);
  }
  if (rows.length === 0) return { header: [], records: [] };
  const [header, ...body] = rows;
  return {
    header,
    records: body.map((values) => Object.fromEntries(header.map((name, i) => [name, values[i]]))),
  };
}

export function validatePackageAnalysis(analysis) {
  const problems = [];
  if (kindOf(analysis) !== "object") {
    return [`final-analysis.json: esperado um objeto por API, encontrado ${kindOf(analysis)}`];
  }
  if (Object.keys(analysis).length === 0) problems.push("final-analysis.json não tem nenhuma API");
  for (const [api, entry] of Object.entries(analysis)) {
    if (kindOf(entry) !== "object") {
      problems.push(`final-analysis.json → ${api}: esperado um objeto`);
      continue;
    }
    for (const [field, shape] of Object.entries(PACKAGE_API_FIELDS)) {
      if (kindOf(entry[field]) !== shape) {
        problems.push(`final-analysis.json → ${api}.${field}: esperado ${shape}, encontrado ${kindOf(entry[field])}`);
      }
    }
  }
  return problems;
}

// Formato do provenance-index.json do pacote publicado. Outros formatos não
// são traduzidos: os campos que faltarem aparecem como não disponíveis.
export function validateProvenance(provenance) {
  const problems = [];
  for (const field of PROVENANCE_FIELDS) {
    if (typeof provenance[field] !== "string") problems.push(`provenance-index.json sem o campo ${field}`);
  }
  if (!Array.isArray(provenance.runs)) {
    problems.push("provenance-index.json sem a lista runs");
  } else if (provenance.runs.some((run) => typeof run?.api !== "string" || typeof run?.run_id !== "string")) {
    problems.push("provenance-index.json: há entradas em runs sem api ou run_id");
  }
  return problems;
}

export async function loadPackage(reader, dir) {
  const analysisFile = await readJson(reader, joinPath(dir, PACKAGE_FILES.analysis), "object");
  const provenanceFile = await readJson(reader, joinPath(dir, PACKAGE_FILES.provenance), "object");
  const csvText = await reader.text(joinPath(dir, PACKAGE_FILES.signaturesCsv));
  return buildPackage(dir, analysisFile, provenanceFile, csvText);
}

export function buildPackage(dir, analysisFile, provenanceFile, csvText) {
  const pkg = {
    dir,
    analysisFile,
    provenanceFile,
    analysis: analysisFile.state === "ok" ? analysisFile.data : null,
    provenance: provenanceFile.state === "ok" ? provenanceFile.data : null,
    csv: null,
    csvState: csvText === null ? "missing" : "ok",
    problems: [],
    fatal: false,
  };
  for (const file of [analysisFile, provenanceFile]) {
    if (file.state === "missing") pkg.problems.push(`${file.path}: arquivo ausente`);
    if (file.state === "invalid") pkg.problems.push(`${file.path}: ${file.message}`);
  }
  if (pkg.analysis) {
    const shapeProblems = validatePackageAnalysis(pkg.analysis);
    pkg.problems.push(...shapeProblems);
    if (shapeProblems.length) pkg.fatal = true;
  } else {
    pkg.fatal = true;
  }
  if (pkg.provenance) pkg.problems.push(...validateProvenance(pkg.provenance));
  if (csvText === null) {
    pkg.problems.push(`${joinPath(dir, PACKAGE_FILES.signaturesCsv)}: arquivo ausente`);
  } else {
    const parsed = parseCsv(csvText);
    const missing = CSV_COLUMNS.filter((column) => !parsed.header.includes(column));
    if (missing.length) {
      pkg.csvState = "invalid";
      pkg.problems.push(`assinaturas.csv sem as colunas: ${missing.join(", ")}`);
    } else {
      pkg.csv = new Map(parsed.records.map((row) => [`${row.api}\u0000${row.id_semantico}`, row]));
    }
  }
  pkg.reverse = new Map();
  return pkg;
}

export function packageApis(pkg) {
  return pkg.analysis ? Object.keys(pkg.analysis).sort() : [];
}

// Campanha publicada no pacote: diretório <pacote>/<api>/<run_id>.
export function packageCampaign(pkg, api, runId) {
  const entry = pkg.analysis?.[api];
  if (!entry || !entry.run_ids.includes(runId)) return null;
  const summary = entry.campaigns.find((campaign) => campaign?.run_id === runId) ?? null;
  const provenance = (Array.isArray(pkg.provenance?.runs) ? pkg.provenance.runs : []).find(
    (run) => run?.api === api && run?.run_id === runId,
  ) ?? null;
  return { dir: joinPath(pkg.dir, api, runId), summary, provenance };
}

export function runIdByNumber(pkg, api) {
  const map = new Map();
  for (const campaign of pkg.analysis?.[api]?.campaigns ?? []) {
    if (campaign?.run_number != null) map.set(campaign.run_number, campaign.run_id);
  }
  return map;
}

// Uma linha por ID semântico de final-analysis.json[api].signatures. Endpoint,
// classe e HTTP vêm de assinaturas.csv (cruzado pelo ID); presença é o
// tamanho de `present_in` publicado.
export function semanticRows(pkg, api) {
  const signatures = pkg.analysis?.[api]?.signatures;
  if (!signatures) return null;
  return Object.entries(signatures).map(([id, entry]) => {
    const csvRow = pkg.csv?.get(`${api}\u0000${id}`) ?? null;
    const presentIn = Array.isArray(entry?.present_in) ? entry.present_in : [];
    return {
      id,
      endpoint: csvRow?.endpoint ?? null,
      classification: csvRow?.classe ?? null,
      status: csvRow?.http != null && csvRow.http !== "" ? Number(csvRow.http) : null,
      presence: presentIn.length,
      presentIn,
      runCount: pkg.analysis[api].run_ids.length,
      scoreRange: Array.isArray(entry?.score_range) ? entry.score_range : null,
      bands: Array.isArray(entry?.bands) ? entry.bands : [],
      origins: Array.isArray(entry?.origins) ? entry.origins : [],
      csvRow,
    };
  });
}

// IDs semânticos cujas origens apontam para (run_id, assinatura estrita).
export function semanticIdsFor(pkg, api, runId, strictSignature) {
  if (!pkg.reverse.has(api)) {
    const index = new Map();
    for (const [id, entry] of Object.entries(pkg.analysis?.[api]?.signatures ?? {})) {
      for (const origin of entry?.origins ?? []) {
        const key = `${origin?.run_id}\u0000${origin?.strict_signature}`;
        const ids = index.get(key) ?? [];
        if (!ids.includes(id)) ids.push(id);
        index.set(key, ids);
      }
    }
    pkg.reverse.set(api, index);
  }
  return pkg.reverse.get(api).get(`${runId}\u0000${strictSignature}`) ?? [];
}

// ---------------------------------------------------------------------------
// Filtros, ordenação e paginação

// `spec` mapeia o nome do filtro para o campo da linha. O filtro `q` busca
// texto nos campos listados em `searchFields`.
export function filterRows(rows, filters, spec, searchFields = []) {
  const query = (filters.q ?? "").trim().toLowerCase();
  return rows.filter((row) => {
    for (const [name, field] of Object.entries(spec)) {
      const wanted = filters[name];
      if (wanted == null || wanted === "") continue;
      const value = row[field];
      if (Array.isArray(value)) {
        if (!value.map(String).includes(wanted)) return false;
      } else if (String(value ?? "") !== wanted) {
        return false;
      }
    }
    if (!query) return true;
    return searchFields.some((field) => {
      const value = row[field];
      const text = Array.isArray(value) ? value.join(" ") : String(value ?? "");
      return text.toLowerCase().includes(query);
    });
  });
}

export function distinctValues(rows, field) {
  const values = new Set();
  for (const row of rows) {
    const value = row[field];
    if (Array.isArray(value)) value.forEach((item) => values.add(String(item)));
    else if (value != null) values.add(String(value));
  }
  return [...values].sort((a, b) => a.localeCompare(b, "pt-BR", { numeric: true }));
}

// Ordem das faixas do FIS para ordenar colunas (não é alfabética).
export const BAND_RANK = { LOW: 1, MEDIUM: 2, HIGH: 3 };

// Ordena uma cópia das linhas pelo valor de `get`. Ausentes ficam sempre no
// fim; texto usa ordem natural ("case-2" antes de "case-10"). A ordenação é
// estável, então empates mantêm a ordem do arquivo.
export function sortRows(rows, get, direction = "asc") {
  const sign = direction === "desc" ? -1 : 1;
  const key = (row) => {
    const value = get(row);
    if (Array.isArray(value)) return value.length ? value.join(", ") : null;
    return value === undefined || value === "" ? null : value;
  };
  return rows
    .map((row) => ({ row, value: key(row) }))
    .sort((a, b) => {
      if (a.value === null || b.value === null) return (a.value === null) - (b.value === null);
      if (typeof a.value === "number" && typeof b.value === "number") return sign * (a.value - b.value);
      return sign * String(a.value).localeCompare(String(b.value), "pt-BR", { numeric: true });
    })
    .map((item) => item.row);
}

export function paginate(rows, page, size) {
  const pages = Math.max(1, Math.ceil(rows.length / size));
  const current = Math.min(Math.max(1, page || 1), pages);
  return { rows: rows.slice((current - 1) * size, current * size), page: current, pages };
}

// Corpo de resposta: JSON indentado quando for JSON válido, texto caso contrário.
export function formatBody(text) {
  if (typeof text !== "string") return { kind: "none", text: "" };
  try {
    return { kind: "json", text: JSON.stringify(JSON.parse(text), null, 2) };
  } catch {
    return { kind: "text", text };
  }
}
