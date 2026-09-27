# Pacote de revisão da coleta final

O pacote omite logs volumosos e guarda uma cópia
do contrato Meilisearch. Os originais completos continuam no diretório-fonte.

Coletor congelado: `{{COLLECTOR_COMMIT}}`. Os SHA-256 do entrypoint e dos módulos do
analisador estão em `provenance-index.json`. Revisão Git recuperável:
`{{ANALYZER_REVISION}}`. Conferir a revisão antes da publicação.

## Analisar este pacote

Rode da raiz do checkout que contém a revisão do analisador indicada acima.
Enquanto essa revisão estiver pendente, este é apenas um pacote local candidato.
Os contratos dos quatro clones externos devem estar em `../mock-projects` nas
revisões e com os hashes indicados em `LICENSES.md`. Este pacote depende desses
contratos para a validação completa.

```bash
PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  {{REVIEW_DIR}} \
  {{COLLECTOR_COMMIT}}
```

## Exportar novamente dos runs locais

O destino deve ser novo. A exportação confere a paridade dos resultados
científicos com a fonte e gera `provenance-index.json`, que registra hashes da
fonte e do pacote, omissões e adaptações por run. Os manifestos dentro do pacote
são adaptados; os originais permanecem no diretório-fonte.

```bash
REVIEW_DEST="{{EXPERIMENT_ROOT}}/public-review-$(date -u +%Y%m%dT%H%M%SZ)"
PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  {{EXPERIMENT_ROOT}} {{COLLECTOR_COMMIT}} --review-dir "$REVIEW_DEST"
```

O pacote preserva metadados completos de inspeção das imagens Docker; revisar
seu conteúdo antes da publicação. O contrato Community Meilisearch v1.45.1 está
identificado como MIT-only pelo upstream; sua atribuição acompanha o pacote em
`licenses/meilisearch-LICENSE-MIT.txt` e `LICENSES.md`.

## Executar uma nova coleta

Esta etapa é separada da análise acima e exige Docker. Para repetir o protocolo
congelado, use um checkout limpo do commit do coletor `{{COLLECTOR_COMMIT}}` e um
identificador novo. O analisador/exportador deste pacote pertence a uma revisão
posterior; use-o somente depois da coleta. Todas as 25 campanhas precisam
registrar o mesmo commit do coletor.

Os quatro runners usam `LEVEL=2`, `MAX_MUTATIONS=20`, `MAX_PAIRS=10`,
`CONCURRENCY=1`, `DELAY_MS=250`, `TIMEOUT_SECONDS=10` e `RUN_NUMBER=1..5`.
Meilisearch usa `REPETITIONS=5`. Rode da raiz do checkout:

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

Depois, no checkout da revisão recuperável do analisador, rode:

```bash
PYTHONPATH=src .venv/bin/python scripts/experiments/analyze_final.py \
  "$EXPERIMENT_ROOT" "$COLLECTION_COMMIT"
```

Campanhas são probabilísticas: IDs, tempos e respostas dinâmicas podem variar.
Logs e eventuais tentativas inválidas permanecem no diretório original.
