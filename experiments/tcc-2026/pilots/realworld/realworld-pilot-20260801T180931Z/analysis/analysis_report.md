# Relatório de Análise

Total de resultados classificados: 98

## Por classificação
- EXPECTED_FAILURE: 85
- SERVER_ERROR: 12
- UNEXPECTED_SUCCESS: 1

## Por severidade
- HIGH: 12
- MEDIUM: 0
- LOW: 86

## Endpoints com mais achados (top 10)
- POST /articles: 16
- PUT /articles/{slug}: 15
- POST /users: 12
- PUT /user: 10
- POST /articles/{slug}/comments: 10
- POST /users/login: 10
- POST /profiles/{username}/follow: 3
- DELETE /profiles/{username}/follow: 3
- DELETE /articles/{slug}: 3
- DELETE /articles/{slug}/comments/{id}: 3

## Amostras por classificação (até 50 cada)

### EXPECTED_FAILURE
- [EXPECTED_FAILURE] GET /user → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /user → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /profiles/{username}/follow → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /profiles/{username}/follow → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /articles/feed → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /articles → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /articles/{slug} → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /articles/{slug} → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /articles/{slug}/comments → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /articles/{slug}/comments/{id} → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /articles/{slug}/favorite → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /articles/{slug}/favorite → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /users/login → 401 — score=0.32 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users/login → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.29 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.3 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.3 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.28 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.28 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.28 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /users → 422 — score=0.28 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] PUT /user → 422 — score=0.2 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] PUT /user → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] PUT /user → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] PUT /user → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] PUT /user → 422 — score=0.26 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] PUT /user → 422 — score=0.16 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] PUT /user → 422 — score=0.16 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] GET /profiles/{username} → 404 — score=0.31 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] POST /profiles/{username}/follow → 404 — score=0.31 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] DELETE /profiles/{username}/follow → 404 — score=0.31 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] POST /articles → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /articles → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /articles → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /articles → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /articles → 422 — score=0.3 severity=LOW — API correctly rejected with documented 422 error.
- [EXPECTED_FAILURE] POST /articles → 422 — score=0.31 severity=LOW — API correctly rejected with documented 422 error.

### SERVER_ERROR
- [SERVER_ERROR] GET /user → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /user → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /profiles/{username}/follow → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] DELETE /profiles/{username}/follow → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] GET /articles/feed → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /articles → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /articles/{slug} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] DELETE /articles/{slug} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /articles/{slug}/comments → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] DELETE /articles/{slug}/comments/{id} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /articles/{slug}/favorite → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] DELETE /articles/{slug}/favorite → 500 — score=0.84 severity=HIGH — Server returned a 500 error.

### UNEXPECTED_SUCCESS
- [UNEXPECTED_SUCCESS] PUT /user → 200 — score=0.16 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.