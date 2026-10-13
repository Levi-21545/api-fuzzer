# Coleta final

25 campanhas: 5 APIs × 5 repetições.

| Arquivo | Conteúdo |
|---|---|
| [`results.md`](results.md) | resultados e casos ilustrativos |
| [`assinaturas.csv`](assinaturas.csv) | um ID semântico por linha, para filtrar e ordenar |
| [`final-analysis.json`](final-analysis.json) | resultados completos, para scripts |
| `<api>/<campanha>/` | plano, respostas, achados e métricas de cada campanha |
| [`contracts/`](contracts/) e [`LICENSES.md`](LICENSES.md) | contratos usados e licenças |
| [`provenance-index.json`](provenance-index.json) | o que foi omitido ou ajustado em cada campanha |

Os logs dos contêineres não foram incluídos.

## Conferir os resultados

Da raiz do repositório:

```bash
PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  experiments/tcc-2026/final ceec101280f999e14fa95955db5bd7e5ceb05e84
```

O comando valida as 25 campanhas e imprime o conteúdo de `final-analysis.json`.

## Repetir a coleta

Exige Docker e as aplicações-alvo descritas no README do repositório. Os
números variam entre execuções. Num checkout limpo, da raiz:

```bash
set -euo pipefail
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

PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  "$EXPERIMENT_ROOT" "$COLLECTION_COMMIT"
```
