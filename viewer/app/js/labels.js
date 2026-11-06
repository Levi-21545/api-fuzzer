// Rótulos e unidades dos campos publicados. As definições seguem o
// results.md e o código que gera cada arquivo; campos sem rótulo aparecem com
// o nome original.

export const COUNT_LABELS = {
  planned_requests: ["Requisições planejadas", "requisições"],
  executed_requests: ["Requisições executadas", "requisições"],
  completed_requests: ["Requisições concluídas", "requisições"],
  classified_observations: ["Observações classificadas (inclui falhas esperadas)", "observações"],
  findings: ["Observações classificadas (inclui falhas esperadas)", "observações"],
  expected_failures: ["Falhas esperadas (não são achados)", "observações"],
  candidate_findings_raw: ["Achados brutos", "achados brutos"],
  findings_unique_operational: ["Assinaturas estritas", "assinaturas estritas"],
  candidate_endpoints: ["Operações com ao menos um achado bruto", "operações"],
  selected_endpoints: ["Operações selecionadas", "operações"],
  unique_findings_involving_level: ["Assinaturas estritas com caso neste nível", "assinaturas estritas"],
  planned_by_case_kind: ["Planejadas por tipo de caso", "requisições"],
};

// Texto de results.md, seção "Classes dos achados brutos".
export const CLASS_HELP = {
  EXPECTED_FAILURE:
    "Falha esperada: a API rejeitou a requisição com um erro 4xx documentado e no formato do contrato. Não é achado.",
  ERROR_CONTRADICTION: "Erro 4xx documentado, mas o corpo não é JSON ou não segue o contrato.",
  SERVER_ERROR: "Resposta 5xx.",
  SUCCESS_CONTRADICTION: "Resposta 2xx não documentada, ou corpo fora do contrato.",
  UNEXPECTED_ERROR_STATUS: "Erro 4xx não documentado para a operação, ou requisição sem resposta.",
  UNEXPECTED_SUCCESS:
    "Resposta 2xx a uma requisição que deveria ser rejeitada (payload mutado ou credencial ausente/inválida).",
};

export const PRIORITY_NOTE =
  "Faixa de prioridade de triagem atribuída pelo FIS (campo severity). Não é gravidade de segurança nem vulnerabilidade confirmada.";

// Campos de metrics.json → fuzzy_assessment, como o pós-processador os conta
// (src/fuzzer/analysis/run_postprocessor.py).
export const FIS_ASSESSMENT_FIELDS = {
  classified_with_assessment: [
    "Observações avaliadas pelo FIS",
    "Observações classificadas que têm avaliação do FIS registrada (severity_assessment). Inclui falhas esperadas.",
  ],
  classified_fallbacks: [
    "Observações avaliadas por fallback",
    "Dessas observações, quantas usaram o fallback: o FIS não conseguiu calcular e o score passou a ser o valor de contradição comportamental. Zero significa que o FIS calculou todas.",
  ],
  unique_with_assessment: [
    "Assinaturas com representante avaliado",
    "Assinaturas estritas cujo caso representante tem avaliação do FIS registrada.",
  ],
  unique_fallbacks: [
    "Assinaturas com representante em fallback",
    "Dessas assinaturas, quantas têm o caso representante avaliado pelo fallback em vez do FIS.",
  ],
};

// Faixa que cada regra do FIS produz (src/fuzzer/analysis/fuzzy_engine.py).
export const RULE_PRIORITY = {
  R1_LOW_CONTRADICTION: "LOW",
  R2_MEDIUM_CONTRADICTION: "MEDIUM",
  R3_HIGH_CONTRADICTION_WEAK_EVIDENCE: "MEDIUM",
  R4_HIGH_CONTRADICTION_STRONG_EVIDENCE: "HIGH",
  R5_POTENTIAL_ACCESS_EXPOSURE: "MEDIUM",
  R6_CLEAR_ACCESS_EXPOSURE: "HIGH",
};

export const PACKAGE_MEASURES = {
  deduplication_reduction: ["Redução pela deduplicação", "1 − assinaturas estritas ÷ achados brutos, somados nas campanhas", "ratio"],
  signature_union: ["IDs semânticos", "distintos entre as campanhas da API", "count"],
  reobserved_at_least_four_ratio: ["IDs semânticos em ≥ 4 campanhas", "fração dos IDs semânticos da API", "ratio"],
  observed_once_ratio: ["IDs semânticos em só 1 campanha", "fração dos IDs semânticos da API", "ratio"],
  signatures_with_band_change: ["IDs semânticos que mudam de faixa entre campanhas", "IDs semânticos", "count"],
  strict_signatures_with_mixed_bands: ["Assinaturas estritas com casos em faixas diferentes", "assinaturas estritas, somadas nas campanhas", "count"],
  fis_inputs_with_different_scores: ["Entradas idênticas do FIS com mais de um score", "vetores de entrada distintos", "count"],
};

export function countLabel(key) {
  return COUNT_LABELS[key] ?? [key, ""];
}
