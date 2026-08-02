# TCC-PUBLIC-001 — artefatos públicos

Este diretório preserva uma pilha nova, gerada integralmente pelo pipeline
atual: uma run L2 para cada uma das cinco APIs. Nenhuma run histórica foi
reaproveitada e nenhum summary JSON/YAML foi criado manualmente.

Todas as runs usam o FIS
`mamdani-behavior-evidence-access-v3`, 20 mutações L1, até 10 pares L2,
concorrência 1, delay de 250 ms e timeout de 10 s.

| Alvo | Run | Operações | Requisições | Observações | Candidatos | Únicos |
|---|---|---:|---:|---:|---:|---:|
| VAmPI | `vampi-public-20260802T022348Z` | 13 | 49 | 39 | 7 | 7 |
| Spring Petclinic REST | `petclinic-public-20260802T022348Z` | 36 | 356 | 349 | 118 | 47 |
| crAPI | `crapi-public-20260802T022348Z` | 44 | 411 | 396 | 344 | 198 |
| RealWorld/Conduit | `realworld-public-20260802T022348Z` | 19 | 142 | 135 | 13 | 13 |
| Meilisearch | `meilisearch-r1-20260802T023155Z` | 85 | 477 | 402 | 318 | 228 |
| **Total** | — | **197** | **1.435** | **1.321** | **800** | **493** |

Cada diretório foi copiado integralmente de
`output/experiments/TCC-PUBLIC-001/` depois que a execução, deduplicação e
cleanup terminaram. O `run_manifest.json` lista todos os arquivos presentes:

- `data/`: plano, resultados brutos e proveniência disponível do alvo;
- `analysis/`: achados, relatório humano, deduplicação e métricas;
- `run_manifest.json`: configuração, versão, hash, contagens e estado da run.

Para publicação, somente o campo `inputs.schema` dos cinco manifests foi
portabilizado: caminhos absolutos locais viraram `<MOCK_ROOT>/...`; no
Meilisearch ele aponta para a cópia preservada em `data/target_contract.json`.
Espaços finais emitidos pelo Docker também foram removidos dos arquivos `.log`
para satisfazer `git diff --check`. Hashes, contagens e demais campos
permanecem como gerados.

As credenciais pertenciam somente aos ambientes locais descartáveis. Headers
foram redigidos e uma auditoria da pilha publicada não encontrou JWT nem a
master key local do Meilisearch.

## Reprodução

Os runners de cada alvo aceitam `EXPERIMENT_ID` e mantêm
`TCC-PILOT-001` como padrão. Para reproduzir o conjunto público, usar
`EXPERIMENT_ID=TCC-PUBLIC-001`, `LEVEL=2`, `MAX_MUTATIONS=20` e
`MAX_PAIRS=10` com:

- `scripts/experiments/run_vampi_pilot.sh`;
- `scripts/experiments/run_petclinic_pilot.sh`;
- `scripts/experiments/run_crapi_pilot.sh`;
- `scripts/experiments/run_realworld_pilot.sh`;
- `scripts/experiments/run_meilisearch_experiment.sh` com `REPETITIONS=1`.

IDs, credenciais descartáveis, timestamps, tempos de resposta e campos
dinâmicos das aplicações podem mudar. Esta pilha é uma amostra pública do
pipeline e não substitui as cinco repetições confirmatórias do Meilisearch nem
decide se o corpus principal exigirá cinco repetições por API.
