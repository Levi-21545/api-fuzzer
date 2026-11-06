# Pilotos canônicos de desenvolvimento

Oito campanhas de `TCC-PILOT-001`, executadas em 01/08/2026: quatro em L1
(mutações individuais) e quatro em L2 (mutações individuais e pares). Estes
artefatos históricos apoiaram o desenvolvimento da ferramenta; não integram
nem substituem as [25 campanhas da coleta final](../final/README.md).

## Campanhas preservadas

| Nível | API | Run | Requisições | Observações classificadas | Candidatos brutos | Assinaturas estritas |
|---|---|---|---:|---:|---:|---:|
| L1 | VAmPI | [vampi-pilot-20260801T180423Z](vampi/vampi-pilot-20260801T180423Z/) | 44 | 34 | 7 | 7 |
| L1 | Petclinic | [petclinic-pilot-20260801T180445Z](petclinic/petclinic-pilot-20260801T180445Z/) | 240 | 233 | 90 | 47 |
| L1 | crAPI | [crapi-pilot-20260801T180621Z](crapi/crapi-pilot-20260801T180621Z/) | 285 | 270 | 239 | 161 |
| L1 | RealWorld | [realworld-pilot-20260801T180931Z](realworld/realworld-pilot-20260801T180931Z/) | 105 | 98 | 13 | 13 |
| **Total L1** | | | **674** | **635** | **349** | **228** |
| L2 | VAmPI | [vampi-l2-20260801T190000Z](vampi/vampi-l2-20260801T190000Z/) | 49 | 39 | 7 | 7 |
| L2 | Petclinic | [petclinic-l2-20260801T190100Z](petclinic/petclinic-l2-20260801T190100Z/) | 356 | 349 | 118 | 47 |
| L2 | crAPI | [crapi-l2-20260801T190300Z](crapi/crapi-l2-20260801T190300Z/) | 411 | 396 | 344 | 198 |
| L2 | RealWorld | [realworld-l2-20260801T190600Z](realworld/realworld-l2-20260801T190600Z/) | 142 | 135 | 13 | 13 |
| **Total L2** | | | **958** | **919** | **482** | **265** |

“Observações classificadas” inclui rejeições esperadas; candidatos e
assinaturas não são contagens de vulnerabilidades ou causas raiz confirmadas.
Os totais de assinaturas somam as quatro campanhas de cada nível.

## Configuração e versões históricas

Todos os manifestos originais registram `dirty: false`, todas as operações
selecionadas, concorrência 1, intervalo de 250 ms, timeout de 10 s e até 20
mutações individuais por corpo. L2 acrescenta um orçamento independente de
até 10 pares por corpo. VAmPI, crAPI e RealWorld incluem sondagens de
autenticação; Petclinic não. As exclusões foram `/createdb` em VAmPI e `/oops`
em Petclinic. Cada diretório preserva sua configuração completa.

| Conjunto | Commit do fuzzer | Modelo de prioridade registrado |
|---|---|---|
| L1 | `77e3d6fa82348bdc4ec4a904033c77265f20d1f3` | `mamdani-status-time-response-size-v1` |
| L2 | `08e51240f6a850f19ebce80b7ea78c6cebdd5b7e` | `mamdani-status-time-response-size-v2` |

Os níveis foram executados em revisões diferentes, com modelos de prioridade
diferentes. Uma diferença de faixa entre eles não pode ser atribuída apenas
ao L2. Os escores e as faixas preservados não são os do FIS v3 da coleta final.
Não houve reexecução, reanálise ou recalibração para preparar este pacote.

O antigo `pilot.yaml` foi substituído por este índice dos artefatos efetivamente
publicados. Ele era apenas uma descrição documental, não uma entrada dos runners.

## Conteúdo e proveniência

Cada campanha contém seu manifesto, plano, respostas, achados, relatório,
deduplicação e métricas. Metadados das imagens e evidências de autenticação
foram mantidos quando existiam no original. Os quatro [contratos](contracts/)
são idênticos aos identificados pelos hashes nos oito manifestos; suas
[licenças e origens](LICENSES.md) acompanham o pacote.

Os arquivos vieram de `experiments-history-20261007.tar.gz`. O
[`provenance-index.json`](provenance-index.json) registra o hash do arquivo
histórico, os hashes dos manifestos originais e todas as adaptações:

- logs dos contêineres, da pilha e de inicialização omitidos;
- `inputs.schema` convertido para o contrato relativo incluído no pacote;
- lista `artifacts` dos manifestos ajustada apenas para remover os logs;
- `Config.WorkingDir` de uma imagem da crAPI substituído por `<LOCAL_PATH>`
  nos dois arquivos de metadados que expunham um caminho de máquina.

Planos, respostas, achados, assinaturas, métricas e relatórios foram preservados
byte a byte. As revisões e os hashes de fonte registrados continuam sendo os
históricos. As credenciais operacionais estão redigidas nos artefatos; entradas
sintéticas de teste e exemplos dos contratos não são credenciais de produção.

Para conferir a integridade dos arquivos, neste diretório:

```bash
shasum -a 256 -c SHA256SUMS
```

O comando confere hashes, não repete os testes HTTP. Não execute o
pós-processador atual sobre estes diretórios: ele substituiria a análise
histórica pela versão atual. Para novas execuções, use outro diretório de saída;
os runners atuais e o commit atual não reproduzem necessariamente o FIS antigo.
