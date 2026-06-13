# OpenAPI Contract Fuzzer

Ferramenta de fuzzing guiada por contrato OpenAPI para APIs REST.

## Requisitos

- Python 3.10+
- `pip`

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

### Testes

```bash
pytest -v
```

### Lint

```bash
ruff check src/ tests/
```

## Como executar
Comando base:
```bash
python -m fuzzer.main <schema.yaml>
```

### Argumentos principais
- `schema` (posicional): caminho para o arquivo OpenAPI (YAML)
- `--base-url`: sobrescreve a URL base definida no schema
- `--auth <arquivo.yaml>`: configura autenticação dinâmica
- `--level <int>`: nível de fuzzing (default: 1)
- `--max <int>`: máximo de mutações por payload
- `--limit <int>`: limita quantidade de endpoints executados
- `--all`: executa todos os endpoints
- `--path <glob>`: filtra endpoints por padrão de path (ex.: /users/*)
- `--concurrency <int>`: requisições concorrentes (default: 5)
- `--output-dir <dir>`: diretório de saída (default: output)

Observação: se você não usar `--all`, `--limit` ou `--path`, o projeto executa até 10 endpoints por padrão.

### Exemplo com autenticação
```bash
python -m fuzzer.main biometrique.openapi.yaml \
  --base-url http://localhost:3000 \
  --auth auth.yaml \
  --all
```

Formato esperado do `auth.yaml`:
```yaml
auth:
  request:
    method: POST
    url: http://localhost:3000/auth/login
    headers:
      Content-Type: application/json
    body:
      email: test@example.com
      password: secret123
  response:
    extract:
      token: ["access_token"]
  inject:
    headers:
      Authorization: "Bearer {token}"
```

## Saídas
Cada execução cria uma pasta em `output/<timestamp>/` contendo:

- `execution_plan.json`: plano de execução gerado
- `results.json`: resultados brutos de execução
- `analysis_report.md`: resumo leve dos achados (para desenvolvimento)
- `analysis_findings.json`: lista de achados com campos principais

## Estrutura (resumo)
`fuzzer/main.py`: fluxo principal da execução

`fuzzer/cli/args.py`: argumentos da linha de comando

`fuzzer/parser/openapi_parser.py`: parser do schema OpenAPI

`fuzzer/mutator/engine.py`: motor de mutações

`fuzzer/orchestrator/execution_plan_builder.py`: planejamento da execução
`fuzzer/orchestrator/runner.py`: orquestrador da execução

`fuzzer/executor/executor.py`: cliente de execução das requisições

`fuzzer/analysis/analyzer.py`: análise dos resultados (em construção)
