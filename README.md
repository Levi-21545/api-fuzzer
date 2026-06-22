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

**Modo estático** (token fixo, sem login):
```yaml
auth:
  inject:
    headers:
      Authorization: "Bearer eyJhbGciOi..."
```

**Modo dinâmico** (faz login e extrai token):
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

Para desabilitar autenticação sem remover o arquivo:
```yaml
auth:
  enabled: false
  inject:
    headers:
      Authorization: "Bearer ..."
```

### Auto-auth (registro + login automáticos)
Quando o schema OpenAPI declara `securitySchemes` e endpoints de registro/login,
o fuzzer pode se autenticar automaticamente sem um `auth.yaml`:

```bash
python -m fuzzer.main schema.yaml --base-url http://localhost:5002 --all --auto-auth
```

Ele descobre os endpoints de register/login pelo path, cria credenciais aleatórias,
obtém um token JWT e injeta `Authorization: Bearer` **apenas nos endpoints que
declaram `security` no schema**.
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

`fuzzer/analysis/fuzzy_engine.py`: motor de lógica fuzzy para scoring de anomalias

---

## Comandos úteis — APIs mock para testes

### VAmPI (API vulnerável com OpenAPI)

```bash
# Subir container vulnerável (porta 5002)
docker run -d --name vampi-vuln -p 5002:5000 erev0s/vampi:latest

# Inicializar banco de dados dummy
curl -s http://localhost:5002/createdb

# Executar fuzzer com auto-auth (registra + login automaticamente)
python -m fuzzer.main <caminho-para-vampi>/openapi_specs/openapi3.yml \
  --base-url http://localhost:5002 --all --auto-auth

# Remover container
docker rm -f vampi-vuln
```

### crAPI (API vulnerável completa)

```bash
# Subir (via docker-compose no diretório do projeto)
cd <caminho-para-crAPI>/deploy
docker compose up -d

# Executar fuzzer
python -m fuzzer.main <caminho-para-crAPI>/openapi_specs/openapi3.yml \
  --base-url http://localhost:8000 --all --auto-auth

# Derrubar
docker compose down
```
