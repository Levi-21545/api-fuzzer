# Coleta final: dados e resultados

Este diretório reúne a coleta final do TCC: 5 APIs, 5 campanhas por API, 25
campanhas no total, todas com a mesma configuração do fuzzer.

## Por onde começar

- [`results.md`](results.md): tabelas e casos ilustrativos, com um glossário
  no topo.
- [`final-analysis.json`](final-analysis.json): os mesmos resultados, completos,
  por API e por ID semântico.
- `<api>/<campanha>/`: os arquivos de cada campanha (plano, respostas, achados
  e métricas).
- [`LICENSES.md`](LICENSES.md): origem, revisão, licença e SHA-256 de cada
  contrato.
- [`provenance-index.json`](provenance-index.json): hashes dos arquivos
  originais e das cópias deste diretório, campanha por campanha.

## Versões

- Fuzzer usado nas campanhas: `{{COLLECTOR_COMMIT}}`.
- Analisador que gerou este diretório: `{{ANALYZER_REVISION}}`.

## Diferenças em relação aos arquivos originais

- Os logs dos contêineres não foram incluídos.
- Em cada `run_manifest.json`, a lista de artefatos e o caminho do contrato
  foram ajustados para não expor caminhos da máquina da coleta. Os hashes dos
  manifestos originais estão em `provenance-index.json`.
- O contrato do Meilisearch está em `contracts/`. Os contratos das outras
  quatro APIs não estão incluídos: são identificados em `LICENSES.md` e
  precisam ser obtidos nos repositórios de origem.

## Conferir os resultados

Use um clone deste repositório no commit do analisador indicado acima, com os
quatro contratos externos em `../mock-projects`, nas revisões de
`LICENSES.md`. Da raiz do repositório:

```bash
PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  {{REVIEW_DIR}} \
  {{COLLECTOR_COMMIT}}
```

O comando valida as 25 campanhas e imprime os resultados de
`final-analysis.json`.

## Como este diretório foi gerado

A partir das 25 campanhas originais, que não estão no repositório:

```bash
PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  {{EXPERIMENT_ROOT}} {{COLLECTOR_COMMIT}} --review-dir {{REVIEW_DIR}}
```

## Repetir a coleta

Exige Docker e as cinco aplicações. Os números não serão idênticos: as
respostas das APIs variam entre execuções.

Use um checkout limpo no commit do fuzzer indicado acima e, da raiz:

```bash
set -euo pipefail
test "$(git rev-parse HEAD)" = "{{COLLECTOR_COMMIT}}"
test -z "$(git status --porcelain)"
export EXPERIMENT_ID="TCC-FINAL-REPRO-$(date -u +%Y%m%dT%H%M%SZ)"
export EXPERIMENT_ROOT="output/experiments/$EXPERIMENT_ID"
export COLLECTION_COMMIT="$(git rev-parse HEAD)"
export LEVEL=2 MAX_MUTATIONS=20 MAX_PAIRS=10
export CONCURRENCY=1 DELAY_MS=250 TIMEOUT_SECONDS=10

for api in vampi petclinic crapi realworld; do
  case "$api" in
    vampi) runner=scripts/experiments/run_vampi_pilot.sh ;;
    petclinic) runner=scripts/experiments/run_petclinic_pilot.sh ;;
    crapi) runner=scripts/experiments/run_crapi_pilot.sh ;;
    realworld) runner=scripts/experiments/run_realworld_pilot.sh ;;
  esac
  for run_number in 1 2 3 4 5; do
    export RUN_NUMBER="$run_number"
    export RUN_ID="${api}-final-r${run_number}-$(date -u +%Y%m%dT%H%M%SZ)"
    bash "$runner"
  done
done
unset RUN_ID RUN_NUMBER
EXPERIMENT_ID="$EXPERIMENT_ID" REPETITIONS=5 \
  bash scripts/experiments/run_meilisearch_experiment.sh
```

Depois, num checkout com o analisador indicado acima:

```bash
PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  "$EXPERIMENT_ROOT" "$COLLECTION_COMMIT"
```
