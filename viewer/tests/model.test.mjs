// Testes da camada de dados contra os artefatos reais e contra fixtures.
//
// FUZZER_REPO aponta para o checkout do api-fuzzer (padrão: a raiz deste repositório).
// Os testes só leem arquivos.

import assert from "node:assert/strict";
import { readFile, readdir, stat } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import {
  EXPECTED_FAILURE,
  buildCampaign,
  buildPackage,
  filterRows,
  formatBody,
  indexByCaseId,
  loadCampaign,
  loadPackage,
  lookupCase,
  observationRows,
  packageApis,
  packageCampaign,
  paginate,
  sortRows,
  parseCsv,
  planRows,
  semanticIdsFor,
  semanticRows,
  signatureRows,
} from "../app/js/model.js";
import { href, parseHash } from "../app/js/router.js";

const here = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(process.env.FUZZER_REPO ?? join(here, "..", ".."));
const PACKAGE_ROOT = join(REPO, "experiments", "tcc-2026");
const PACKAGE_DIR = "final";
const OUTPUT_ROOT = join(REPO, "output", "experiments");

function fsReader(root) {
  return {
    async text(path) {
      try {
        return await readFile(join(root, path), "utf8");
      } catch (error) {
        if (error.code === "ENOENT") return null;
        throw error;
      }
    },
  };
}

async function exists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

function memoryReader(files) {
  return { async text(path) { return path in files ? files[path] : null; } };
}

function countBy(items, key) {
  const counts = {};
  for (const item of items) counts[key(item)] = (counts[key(item)] ?? 0) + 1;
  return counts;
}

function sortedObject(object) {
  return Object.fromEntries(Object.entries(object).sort(([a], [b]) => a.localeCompare(b)));
}

// Confere que tudo o que a interface mostra de uma campanha bate com metrics.json
// e que cada case_id citado resolve para um registro único nos três arquivos.
function checkCampaign(campaign, label) {
  assert.deepEqual(campaign.problems, [], `${label}: avisos de leitura`);
  const counts = campaign.metrics.counts;
  assert.equal(campaign.plan.size, counts.planned_requests, `${label}: planejadas`);
  assert.equal(campaign.results.size, counts.executed_requests, `${label}: executadas`);
  assert.equal(campaign.findings.size, counts.classified_observations, `${label}: observações`);

  const observations = observationRows(campaign);
  const expected = observations.filter((row) => row.classification === EXPECTED_FAILURE);
  assert.equal(expected.length, counts.expected_failures, `${label}: falhas esperadas`);
  assert.equal(observations.length - expected.length, counts.candidate_findings_raw, `${label}: achados brutos`);

  const signatures = signatureRows(campaign);
  assert.equal(signatures.length, counts.findings_unique_operational, `${label}: assinaturas estritas`);
  // A faixa mostrada na tabela é a do representante, o mesmo critério de metrics.json.
  assert.deepEqual(sortedObject(countBy(signatures, (row) => row.band)), sortedObject(campaign.metrics.unique_by_severity), `${label}: faixas`);
  assert.deepEqual(
    sortedObject(countBy(signatures, (row) => row.classification)),
    sortedObject(campaign.metrics.unique_by_classification),
    `${label}: classes das assinaturas`,
  );

  for (const row of signatures) {
    assert.equal(row.unresolvedCases, 0, `${label}: ${row.id} tem case_id sem achado`);
    for (const caseId of row.caseIds) {
      for (const index of [campaign.plan, campaign.results, campaign.findings]) {
        assert.equal(lookupCase(index, caseId).state, "ok", `${label}: ${caseId}`);
      }
      const finding = lookupCase(campaign.findings, caseId).record;
      assert.notEqual(finding.classification, EXPECTED_FAILURE, `${label}: falha esperada dentro de assinatura`);
      assert.equal(finding.endpoint_id, row.endpoint, `${label}: endpoint de ${caseId}`);
    }
  }
  for (const row of planRows(campaign)) {
    assert.equal(row.resultState, "ok", `${label}: plano ${row.caseId} sem resultado`);
  }
  for (const row of observations) {
    assert.equal(lookupCase(campaign.plan, row.caseId).state, "ok", `${label}: observação ${row.caseId} sem plano`);
  }
  return signatures;
}

const hasPackage = await exists(join(PACKAGE_ROOT, PACKAGE_DIR, "final-analysis.json"));

test("pacote final: campanhas, totais e vínculos batem com os arquivos", { skip: !hasPackage && "pacote ausente" }, async () => {
  const reader = fsReader(PACKAGE_ROOT);
  const pkg = await loadPackage(reader, PACKAGE_DIR);
  assert.deepEqual(pkg.problems, []);
  assert.deepEqual(packageApis(pkg), ["crapi", "meilisearch", "petclinic", "realworld", "vampi"]);

  let campaignsChecked = 0;
  let originsChecked = 0;
  for (const api of packageApis(pkg)) {
    const entry = pkg.analysis[api];
    const sums = {};
    const campaigns = new Map();
    for (const runId of entry.run_ids) {
      const info = packageCampaign(pkg, api, runId);
      assert.ok(info?.summary, `${runId}: resumo em final-analysis.json`);
      assert.ok(info.provenance, `${runId}: entrada em provenance-index.json`);
      const campaign = await loadCampaign(reader, info.dir);
      checkCampaign(campaign, runId);
      assert.deepEqual(campaign.metrics.counts, info.summary.counts, `${runId}: counts do pacote`);
      for (const [key, value] of Object.entries(campaign.metrics.counts)) sums[key] = (sums[key] ?? 0) + value;
      campaigns.set(runId, campaign);
      campaignsChecked += 1;
    }
    // Os totais publicados da API são a soma dos metrics.json das campanhas.
    for (const [key, value] of Object.entries(entry.totals)) assert.equal(value, sums[key], `${api}: totals.${key}`);

    const rows = semanticRows(pkg, api);
    assert.equal(rows.length, entry.signature_union, `${api}: IDs semânticos`);
    const frequency = countBy(rows, (row) => String(row.presence));
    for (const [presence, count] of Object.entries(entry.presence_frequency)) {
      assert.equal(frequency[presence] ?? 0, count, `${api}: presença ${presence}`);
    }
    for (const row of rows) {
      assert.ok(row.csvRow, `${api}: ${row.id} ausente de assinaturas.csv`);
      assert.equal(Number(row.csvRow.presenca), row.presence, `${api}: presença do CSV`);
      for (const origin of row.origins) {
        const campaign = campaigns.get(origin.run_id);
        const strict = campaign.unique.byId.get(origin.strict_signature);
        assert.ok(strict, `${api}: origem ${origin.strict_signature} inexistente em ${origin.run_id}`);
        assert.ok(strict.record.case_ids.includes(origin.case_id), `${api}: ${origin.case_id} fora da assinatura`);
        assert.ok(semanticIdsFor(pkg, api, origin.run_id, origin.strict_signature).includes(row.id));
        originsChecked += 1;
      }
    }
  }
  assert.equal(campaignsChecked, 25);
  assert.ok(originsChecked > 0);
});

const hasOutput = await exists(OUTPUT_ROOT);

test("campanhas originais do runner abrem sem o pacote", { skip: !hasOutput && "output/experiments ausente" }, async () => {
  const base = join(OUTPUT_ROOT, "TCC-FINAL-001");
  const reader = fsReader(base);
  let checked = 0;
  for (const api of await readdir(base)) {
    if (!["vampi", "petclinic", "crapi", "realworld", "meilisearch"].includes(api)) continue;
    for (const run of await readdir(join(base, api))) {
      if (run.startsWith(".")) continue;
      const campaign = await loadCampaign(reader, `${api}/${run}`);
      checkCampaign(campaign, run);
      assert.equal(campaign.manifest.run_id, run);
      checked += 1;
    }
  }
  assert.equal(checked, 25);
});

test("pacote fora do formato público é reportado, sem traduzir campos", { skip: !hasOutput && "output/experiments ausente" }, async () => {
  const base = join(OUTPUT_ROOT, "TCC-FINAL-001");
  const candidate = (await readdir(base)).find((name) => name.startsWith("public-review-"));
  if (!candidate) return;
  const pkg = await loadPackage(fsReader(base), candidate);
  const text = pkg.problems.join("\n");
  assert.match(text, /sem o campo campaign_commit/);
  assert.match(text, /runs sem api ou run_id/);
  assert.match(text, /assinaturas\.csv: arquivo ausente/);
  // Sem a correspondência por `api`, nenhuma campanha recebe proveniência.
  const api = packageApis(pkg)[0];
  assert.equal(packageCampaign(pkg, api, pkg.analysis[api].run_ids[0]).provenance, null);
});

test("campanha falha só com manifesto: arquivos ausentes viram 'não disponível'", async () => {
  const campaign = await loadCampaign(
    memoryReader({ "run/run_manifest.json": JSON.stringify({ run_id: "x", status: "failed", error: { type: "E" } }) }),
    "run",
  );
  assert.equal(campaign.files.manifest.state, "ok");
  for (const key of ["plan", "results", "findings", "unique", "metrics"]) assert.equal(campaign.files[key].state, "missing");
  assert.equal(signatureRows(campaign), null);
  assert.equal(observationRows(campaign), null);
  assert.equal(planRows(campaign), null);
  assert.equal(campaign.metrics, null);
  assert.equal(lookupCase(campaign.plan, "case-1").state, "unavailable");
});

test("formato incompatível e case_id repetido são reportados, não resolvidos", async () => {
  const campaign = await loadCampaign(
    memoryReader({
      "r/data/execution_plan.json": JSON.stringify([{ case_id: "a" }, { case_id: "a" }, { nope: 1 }]),
      "r/data/results.json": "{ não é json",
      "r/analysis/analysis_findings.json": JSON.stringify({ not: "a list" }),
    }),
    "r",
  );
  assert.equal(campaign.files.results.state, "invalid");
  assert.equal(campaign.files.findings.state, "invalid");
  assert.match(campaign.problems.join("\n"), /case_id repetido \(a\)/);
  assert.match(campaign.problems.join("\n"), /1 registro\(s\) sem case_id/);
  assert.match(campaign.problems.join("\n"), /esperado uma lista/);
  assert.equal(lookupCase(campaign.plan, "a").state, "duplicate");

  const empty = await loadCampaign(memoryReader({}), "vazio");
  assert.match(empty.problems[0], /nenhum arquivo de campanha/);
});

test("pacote com formato inesperado é marcado como incompatível", () => {
  const pkg = buildPackage(
    "p",
    { state: "ok", path: "p/final-analysis.json", data: { api: { run_ids: [], campaigns: {} } } },
    { state: "missing", path: "p/provenance-index.json" },
    "api,id\n",
  );
  assert.equal(pkg.fatal, true);
  const text = pkg.problems.join("\n");
  assert.match(text, /api\.campaigns: esperado array, encontrado object/);
  assert.match(text, /api\.signatures/);
  assert.match(text, /provenance-index\.json: arquivo ausente/);
  assert.match(text, /assinaturas\.csv sem as colunas/);
});

test("utilitários: CSV, filtros, paginação, corpo e rotas", () => {
  const csv = parseCsv('a,b\n1,"x, ""y"""\r\n2,z\n');
  assert.deepEqual(csv.records, [{ a: "1", b: 'x, "y"' }, { a: "2", b: "z" }]);

  const rows = [
    { id: "1", status: 500, bands: ["LOW"], endpoint: "GET /a" },
    { id: "2", status: 400, bands: ["LOW", "HIGH"], endpoint: "POST /b" },
  ];
  assert.deepEqual(filterRows(rows, { http: "400" }, { http: "status" }).map((r) => r.id), ["2"]);
  assert.deepEqual(filterRows(rows, { faixa: "HIGH" }, { faixa: "bands" }).map((r) => r.id), ["2"]);
  assert.deepEqual(filterRows(rows, { q: "get" }, {}, ["endpoint"]).map((r) => r.id), ["1"]);
  assert.deepEqual(paginate([1, 2, 3], 9, 2), { rows: [3], page: 2, pages: 2 });
  const cases = [{ id: "case-10", n: 2 }, { id: "case-2", n: null }, { id: "case-1", n: 2 }, { id: "case-3", n: 1 }];
  assert.deepEqual(sortRows(cases, (r) => r.id).map((r) => r.id), ["case-1", "case-2", "case-3", "case-10"]);
  assert.deepEqual(sortRows(cases, (r) => r.n, "desc").map((r) => r.id), ["case-10", "case-1", "case-3", "case-2"]);
  assert.deepEqual(sortRows(cases, (r) => r.n).map((r) => r.id), ["case-3", "case-10", "case-1", "case-2"]);

  assert.equal(formatBody('{"a":1}').kind, "json");
  assert.deepEqual(formatBody("<b>oi</b>"), { kind: "text", text: "<b>oi</b>" });

  const link = href(["run", 0, "a/b c", "case", "case-1"], { op: "GET /x", q: "" });
  assert.deepEqual(parseHash(link), { segments: ["run", "0", "a/b c", "case", "case-1"], params: { op: "GET /x" } });

  const index = indexByCaseId([{ case_id: "x" }]);
  assert.equal(lookupCase(index, "x").index, 0);
  assert.equal(buildCampaign("d", { manifest: { state: "missing" }, plan: { state: "missing" }, results: { state: "missing" }, findings: { state: "missing" }, unique: { state: "missing" }, metrics: { state: "missing" } }).problems.length, 1);
});
