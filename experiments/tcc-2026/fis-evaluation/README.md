# Avaliação do FIS (Etapa 1)

Registros das duas avaliações de prioridade descritas no artigo. Nas duas,
três instâncias do mesmo modelo de linguagem classificaram cada família sem
ver a classificação do analisador nem o escore do FIS. Prevaleceu a maioria; as
famílias sem maioria foram decididas por uma quarta instância.

| Avaliação | Pasta | Famílias | Números do artigo |
|---|---|---:|---|
| Desenvolvimento (pilotos L2 de VAmPI, Petclinic, crAPI e RealWorld) | [`desenvolvimento/`](desenvolvimento/) | 161 | Seções 6.1 e 6.2: 99/59/3, acurácia 0,298, macro-F1 0,254, erro ordinal 0,702, modelo revisado 1,000 |
| Validação externa no Meilisearch v1.45.1 | [`meilisearch/`](meilisearch/) | 134 | Seção 6.3: 122 sustentadas, 120/122 contra 4/122 e a tabela de métricas |

As 25 campanhas finais não passaram por essa avaliação; estão em
[`../final/`](../final/README.md).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| [`rubric.md`](rubric.md) | Critérios entregues aos avaliadores do Meilisearch, sem alterações. O `blind_families.json` citado nela é `meilisearch/blind_families.json`. |
| `*/blind_families.json` | Fichas que os avaliadores receberam: contrato, requisição (credenciais ocultadas) e resposta. |
| `meilisearch/rater_{a,b,c}.json`, `desenvolvimento/family_rater_{a,b,c}.json` | Voto de cada instância: validade, prioridade, confiança e justificativa. |
| `meilisearch/adjudication*.json`, `desenvolvimento/family_adjudication.json` | Famílias sem maioria e a decisão da quarta instância. |
| `meilisearch/consensus.json` | Referência final e concordância entre as instâncias. |
| `meilisearch/private_family_map.json` | Liga cada ficha às assinaturas das cinco campanhas de onde ela veio. Os avaliadores não tiveram acesso a ele. |
| `meilisearch/confirmatory_analysis.json` | Escore do FIS e da regra de status por família, matrizes de confusão e métricas. |
| `desenvolvimento/analysis.json` | Consenso, previsões e métricas da avaliação de desenvolvimento. |

## Refazer as contas

```bash
# Meilisearch: refaz o consenso a partir dos votos (regrava os mesmos arquivos)
python3 experiments/tcc-2026/fis-evaluation/meilisearch/build_consensus.py

# Desenvolvimento: refaz fichas, consenso e métricas a partir dos pilotos publicados
.venv/bin/python experiments/tcc-2026/fis-evaluation/desenvolvimento/analyze_family_ratings.py
```

A saída do segundo comando deve ser idêntica a `desenvolvimento/analysis.json`.
As campanhas do Meilisearch da Etapa 1 não foram preservadas; por isso, os
escores do FIS desse conjunto estão em `confirmatory_analysis.json` como foram
gravados.
