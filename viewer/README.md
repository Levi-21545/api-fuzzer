# Visualizador de resultados

Interface local e somente leitura para consultar os artefatos do fuzzer no
navegador: o pacote final em `experiments/tcc-2026/final/` e campanhas avulsas
geradas pelo CLI ou pelos runners.

A interface não executa o fuzzer, não recalcula métricas, não refaz a
deduplicação nem o FIS e não altera arquivos. Todo número exibido vem de um
arquivo publicado, e o arquivo de origem aparece ao lado do valor.

## Como rodar

Requer Python 3.9 ou superior e um navegador. Não há dependências para
instalar e nada precisa de rede. A partir da raiz do repositório:

```bash
python3 viewer/serve.py
```

Depois, abra `http://127.0.0.1:8765/`.

| Opção | Efeito |
|---|---|
| `--include-output` | também procura campanhas locais em `output/experiments/` |
| `--root PATH` | procura também neste diretório (repetível), por exemplo a saída de uma run do CLI |
| `--repo PATH` | usa outro checkout do api-fuzzer (padrão: o diretório acima de `viewer/`) |
| `--port N` | porta local (padrão 8765) |

Para abrir uma run feita pelo CLI:

```bash
python3 viewer/serve.py --root output/<run-id>
```

O botão "Reler arquivos" refaz a busca sem reiniciar o servidor. Para
encerrar, use Ctrl+C no terminal.

## O que é reconhecido

| Diretório com | Tratado como |
|---|---|
| `final-analysis.json` e `provenance-index.json` | pacote final, com campanhas em `<api>/<run_id>/` |
| `run_manifest.json` ou `data/execution_plan.json` | campanha avulsa |

O formato de referência é o do pacote publicado. Não há conversão de formatos
antigos: um campo ausente aparece como "não disponível" e a diferença é listada
como aviso no topo da página.

## Mapa da ferramenta

```text
Artefatos encontrados
├── Pacote final
│   ├── APIs (totais por API)
│   └── API
│       ├── Campanhas ─────────────┐
│       ├── IDs semânticos          │
│       │   └── ID semântico        │
│       │       └── origens ────────┤
│       └── Totais, medidas e configuração
│                                   ▼
└── Campanha (do pacote ou avulsa)
    ├── Configuração, proveniência e métricas
    ├── Assinaturas estritas
    │   └── Assinatura estrita ──┐
    ├── Observações classificadas ┤
    └── Plano (todas as requisições)
                                  ▼
                                Caso
                                ├── requisição e resposta lado a lado
                                ├── classificação e FIS
                                └── registros originais (JSON)
```

| Tela | O que mostra | De onde vem |
|---|---|---|
| Artefatos encontrados | pacotes e campanhas avulsas, agrupadas por pasta | busca nos diretórios configurados |
| Pacote final | proveniência e uma linha por API com os totais | `provenance-index.json`, `final-analysis.json` |
| API → Campanhas | contagens e classes HTTP de cada campanha | `final-analysis.json` → `campaigns` |
| API → IDs semânticos | um ID por achado entre campanhas, com presença, score e faixas | `final-analysis.json` → `signatures`, `assinaturas.csv` |
| API → Totais, medidas e configuração | somas, medidas entre campanhas, distribuição do FIS e configuração | `final-analysis.json` |
| ID semântico | resumo publicado e a assinatura estrita de cada campanha em que aparece | `final-analysis.json` → `origins` |
| Campanha → Configuração, proveniência e métricas | manifesto, configuração do fuzzer, hashes e distribuições | `run_manifest.json`, `analysis/metrics.json` |
| Campanha → Assinaturas estritas | achados brutos agrupados nesta campanha | `analysis/findings_unique.json` |
| Campanha → Observações classificadas | cada resposta classificada, incluindo falhas esperadas (ocultas por padrão) | `analysis/analysis_findings.json` |
| Campanha → Plano | todas as requisições planejadas, inclusive as que não geraram observação | `data/execution_plan.json` |
| Assinatura estrita | componentes da assinatura, resposta normalizada e casos do grupo | `analysis/findings_unique.json` |
| Caso | requisição, resposta, classe e FIS (entradas, pertinências e regras) | `execution_plan.json`, `results.json`, `analysis_findings.json` |

Todas as tabelas de casos, assinaturas e IDs têm busca, filtros e ordenação
pelo cabeçalho. Filtros e ordem ficam na URL, então o botão Voltar retorna à
mesma tabela e um link copiado abre a mesma visão.

## Como ler os números

Cada contagem tem uma unidade. Os exemplos são da campanha 3 da crAPI.

| Termo | É | Não confundir com | Exemplo |
|---|---|---|---|
| Requisição planejada / executada | uma entrada do plano / uma requisição enviada | — | 411 / 411 |
| Observação classificada | uma resposta que o analisador classificou | achado: inclui falhas esperadas | 396 |
| Falha esperada (`EXPECTED_FAILURE`) | um erro 4xx documentado e no formato do contrato | achado: não é achado | 52 |
| Achado bruto | uma observação que não é falha esperada | achado distinto | 344 |
| Assinatura estrita | um grupo de achados brutos da mesma campanha com mesma operação, classe, status, resposta normalizada e caminho do erro | ID semântico | 196 |
| ID semântico | o mesmo achado reconhecido entre as campanhas de uma API | assinatura estrita: só existe no pacote | — |
| Presença | em quantas campanhas um ID semântico aparece | acurácia ou taxa de acerto | 5/5 |
| Score e faixa (`LOW`, `MEDIUM`, `HIGH`) | prioridade de triagem atribuída pelo FIS | gravidade de segurança ou vulnerabilidade confirmada | 0,16 `LOW` |

Duas regras de leitura:

- Na tabela de assinaturas estritas, faixa e score são os do caso
  representante, como em `metrics.json`. Na página da API, a distribuição de
  faixas é a de `final-analysis.json`, que usa o maior score entre os casos.
  As duas só diferem quando uma assinatura tem casos em faixas diferentes; a
  interface marca esses casos como "mista".
- Os números do pacote e os de campanhas avulsas nunca são somados. As páginas
  do pacote têm o selo "agregado do pacote" e as de campanha, "dados da
  campanha".

## Roteiro: de um número publicado até o caso

1. Abra o pacote final e a API desejada.
2. Na aba "IDs semânticos", filtre por presença, classe, HTTP ou faixa, ou
   busque o ID citado em `results.md`.
3. Na página do ID, a tabela de origens leva à assinatura estrita e ao caso
   representante de cada campanha.
4. No caso, compare requisição e resposta e confira as entradas, as
   pertinências e as regras do FIS. "Registros originais" mostra o JSON
   exato e o arquivo de onde ele veio.

Exemplo: o ID `01fece02c197…` da crAPI, citado em `results.md`, leva ao
`case-000019` da campanha 3.

## Garantias

- Os registros são ligados por `case_id`, `signature.id` e `origins`, nunca
  pela posição nos arrays. Um `case_id` repetido é reportado e nenhum registro
  é escolhido.
- O servidor escuta só em `127.0.0.1`, responde só a GET e recusa `Host`
  diferente de `127.0.0.1` ou `localhost`.
- Lê apenas `.json`, `.md`, `.csv`, `.yml`, `.yaml` e `.txt` dentro dos
  diretórios configurados. Logs, arquivos ocultos e caminhos fora desses
  diretórios são recusados.
- Corpos de resposta, Markdown e CSV são exibidos como texto. URLs presentes nos
  registros não viram links nem são acessadas.
- Nada é gravado em disco. O navegador guarda só a escolha de tema, no
  `localStorage`.

## Testes

```bash
python3 -m unittest discover -s viewer/tests
node --test viewer/tests/
```

Os testes Python cobrem a busca de artefatos, o confinamento aos diretórios e
as recusas do servidor. Os testes Node (Node 20 ou superior) leem os artefatos
reais deste repositório e conferem, para as 25 campanhas do pacote, que as
contagens exibidas batem com `metrics.json`, que os totais por API batem com a
soma das campanhas e que cada vínculo entre ID semântico, assinatura, caso,
requisição e resposta resolve. As 25 campanhas originais em
`output/experiments/TCC-FINAL-001` também são conferidas quando existem na
máquina; no clone público, esses testes são pulados.

## Limitações

- Tabelas paginadas em 100 linhas; cada arquivo é lido inteiro (o maior JSON
  do pacote tem cerca de 850 KB).
- `README.md` e `results.md` aparecem como texto, sem renderizar Markdown.
- Os hashes registrados são exibidos, não recalculados.
