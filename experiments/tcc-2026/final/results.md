# Resultados da coleta final

25 campanhas: 5 APIs × 5 repetições, todas com o fuzzer no commit `ceec101280f999e14fa95955db5bd7e5ceb05e84` e a mesma configuração.

## Como ler

- **Falha esperada:** a API rejeitou a requisição com um erro 4xx documentado e no formato do contrato. Não é achado.
- **Achado bruto:** uma requisição cuja resposta foi classificada como divergência (classes abaixo). Conta cada requisição.
- **Assinatura estrita:** reúne, dentro de uma campanha, achados com a mesma operação, classe, status HTTP, resposta normalizada e caminho do erro de validação.
- **ID semântico:** identifica o mesmo achado entre campanhas. No Meilisearch, ignora `requestUid` e `processingTimeMs` em `POST /multi-search`.
- **Presença:** em quantas das 5 campanhas um ID semântico apareceu. Cada ID conta no máximo uma vez por campanha.

## Execução

| API | Planejadas | Executadas | 2xx | 4xx | 5xx |
|---|---:|---:|---:|---:|---:|
| VAmPI | 245 | 245 | 55 | 190 | 0 |
| Spring Petclinic REST | 1.780 | 1.780 | 65 | 1.340 | 375 |
| crAPI | 2.055 | 2.055 | 155 | 1.370 | 530 |
| RealWorld/Conduit | 710 | 710 | 40 | 610 | 60 |
| Meilisearch | 2.385 | 2.385 | 445 | 1.940 | 0 |
| **Total** | **7.175** | **7.175** | **760** | **5.450** | **965** |

Respostas 4xx e 5xx são resultados normais do teste e não invalidam uma campanha.

## Achados e deduplicação

| API | Falhas esperadas | Achados brutos | Assinaturas estritas | Redução |
|---|---:|---:|---:|---:|
| VAmPI | 160 | 35 | 35 | 0,0% |
| Spring Petclinic REST | 1.155 | 590 | 235 | 60,2% |
| crAPI | 260 | 1.720 | 985 | 42,7% |
| RealWorld/Conduit | 610 | 65 | 65 | 0,0% |
| Meilisearch | 420 | 1.590 | 1.140 | 28,3% |
| **Total** | **2.605** | **4.000** | **2.460** | **38,5%** |

Assinaturas estritas somam as 5 campanhas. Redução = 1 − assinaturas ÷ achados brutos.

## Classes dos achados brutos

| API | ERROR_CONTRADICTION | SERVER_ERROR | SUCCESS_CONTRADICTION | UNEXPECTED_ERROR_STATUS | UNEXPECTED_SUCCESS |
|---|---:|---:|---:|---:|---:|
| VAmPI | 30 | 0 | 5 | 0 | 0 |
| Spring Petclinic REST | 180 | 375 | 30 | 5 | 0 |
| crAPI | 285 | 530 | 20 | 825 | 60 |
| RealWorld/Conduit | 0 | 60 | 0 | 0 | 5 |
| Meilisearch | 0 | 0 | 70 | 1.520 | 0 |

- `ERROR_CONTRADICTION`: erro 4xx documentado, mas o corpo não é JSON ou não segue o contrato.
- `SERVER_ERROR`: resposta 5xx.
- `SUCCESS_CONTRADICTION`: resposta 2xx não documentada, ou corpo fora do contrato.
- `UNEXPECTED_ERROR_STATUS`: erro 4xx não documentado para a operação, ou requisição sem resposta.
- `UNEXPECTED_SUCCESS`: resposta 2xx a uma requisição que deveria ser rejeitada (payload mutado ou credencial ausente/inválida).

## Estabilidade entre as campanhas

| API | IDs semânticos | em 5/5 | em 4/5 | em 3/5 | em 2/5 | em 1/5 | ≥ 4/5 | só 1/5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| VAmPI | 11 | 6 | 0 | 0 | 0 | 5 | 54,5% | 45,5% |
| Spring Petclinic REST | 47 | 47 | 0 | 0 | 0 | 0 | 100,0% | 0,0% |
| crAPI | 273 | 154 | 12 | 18 | 24 | 65 | 60,8% | 23,8% |
| RealWorld/Conduit | 17 | 12 | 0 | 0 | 0 | 5 | 70,6% | 29,4% |
| Meilisearch | 222 | 222 | 0 | 0 | 0 | 0 | 100,0% | 0,0% |
| **Total** | **570** | **441** | **12** | **18** | **24** | **75** | — | — |

As colunas "em k/5" contam IDs presentes em exatamente k campanhas. As duas últimas são percentuais sobre os IDs semânticos da API; não há percentual no total porque ele mistura APIs.

## Prioridade atribuída pelo FIS

| API | Assinaturas | Mínimo | Mediana | Máximo | LOW | MEDIUM | HIGH |
|---|---:|---:|---:|---:|---:|---:|---:|
| VAmPI | 35 | 0,16 | 0,16 | 0,50 | 30 | 5 | 0 |
| Spring Petclinic REST | 235 | 0,16 | 0,17 | 0,84 | 125 | 100 | 10 |
| crAPI | 985 | 0,16 | 0,16 | 0,73 | 790 | 190 | 5 |
| RealWorld/Conduit | 65 | 0,50 | 0,50 | 0,50 | 0 | 65 | 0 |
| Meilisearch | 1.140 | 0,16 | 0,16 | 0,50 | 1.020 | 120 | 0 |

Um score por assinatura estrita em cada campanha (mesmo total da tabela de deduplicação). Os scores descrevem a prioridade de triagem atribuída; não medem acerto nem confirmam vulnerabilidades. A comparação com rótulos de referência existe só nos conjuntos históricos.

## Casos ilustrativos

Para cada API, um ID presente nas 5 campanhas e um presente em só 1: o primeiro de cada grupo em ordem alfabética do ID. APIs sem ID em 1/5 têm só um caso. Os casos servem para seguir um exemplo até os dados brutos; não representam a API.

| API | Presença | Endpoint | Classe | HTTP | Caso | ID semântico |
|---|---:|---|---|---:|---|---|
| VAmPI | 5/5 | `PUT /users/v1/{username}/email` | `ERROR_CONTRADICTION` | 401 | [`auth-probe-000005`, campanha 1](vampi/vampi-final-r1-20260924T021658Z/analysis/analysis_findings.json) | `040f80251096…` |
| VAmPI | 1/5 | `GET /books/v1/{book_title}` | `SUCCESS_CONTRADICTION` | 200 | [`case-000037`, campanha 3](vampi/vampi-final-r3-20260924T021734Z/analysis/analysis_findings.json) | `22390c865de6…` |
| Spring Petclinic REST | 5/5 | `POST /owners/{ownerId}/pets/{petId}/visits` | `SERVER_ERROR` | 500 | [`case-000127`, campanha 1](petclinic/petclinic-final-r1-20260924T021826Z/analysis/analysis_findings.json) | `043a17a33230…` |
| crAPI | 5/5 | `POST /workshop/api/mechanic/signup` | `ERROR_CONTRADICTION` | 400 | [`case-000325`, campanha 1](crapi/crapi-final-r1-20260924T022956Z/analysis/analysis_findings.json) | `001fec228b21…` |
| crAPI | 1/5 | `POST /identity/api/auth/signup` | `UNEXPECTED_ERROR_STATUS` | 400 | [`case-000019`, campanha 3](crapi/crapi-final-r3-20260924T023820Z/analysis/analysis_findings.json) | `01fece02c197…` |
| RealWorld/Conduit | 5/5 | `POST /articles/{slug}/favorite` | `SERVER_ERROR` | 500 | [`auth-probe-000022`, campanha 1](realworld/realworld-final-r1-20260924T024911Z/analysis/analysis_findings.json) | `2024b0172ce5…` |
| RealWorld/Conduit | 1/5 | `PUT /user` | `UNEXPECTED_SUCCESS` | 200 | [`case-000042`, campanha 2](realworld/realworld-final-r2-20260924T025013Z/analysis/analysis_findings.json) | `10121daced30…` |
| Meilisearch | 5/5 | `PUT /indexes/{index_uid}/settings/localized-attributes` | `UNEXPECTED_ERROR_STATUS` | 400 | [`case-000151`, campanha 1](meilisearch/meilisearch-r1-20260924T025900Z/analysis/analysis_findings.json) | `0013241dfc27…` |
