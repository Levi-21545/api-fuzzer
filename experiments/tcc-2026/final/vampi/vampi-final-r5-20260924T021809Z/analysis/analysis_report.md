# Relatório de Análise

Total de resultados classificados: 39

## Por classificação
- EXPECTED_FAILURE: 32
- ERROR_CONTRADICTION: 6
- SUCCESS_CONTRADICTION: 1

## Por severidade
- HIGH: 0
- MEDIUM: 1
- LOW: 38

## Endpoints com mais achados (top 10)
- POST /users/v1/register: 8
- POST /books/v1: 7
- PUT /users/v1/{username}/email: 6
- PUT /users/v1/{username}/password: 5
- POST /users/v1/login: 5
- DELETE /users/v1/{username}: 3
- GET /books/v1/{book_title}: 3
- GET /me: 2

## Amostras por classificação (até 50 cada)

### EXPECTED_FAILURE
- [EXPECTED_FAILURE] GET /me → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /users/v1/{username} → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/email → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/password → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /books/v1 → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /books/v1/{book_title} → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/register → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/login → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/login → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/login → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/login → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /users/v1/login → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] DELETE /users/v1/{username} → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/email → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/email → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/email → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/email → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/password → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/password → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /users/v1/{username}/password → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /books/v1 → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /books/v1 → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /books/v1 → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /books/v1 → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /books/v1 → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.

### ERROR_CONTRADICTION
- [ERROR_CONTRADICTION] GET /me → 401 — score=0.16 severity=LOW — Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- [ERROR_CONTRADICTION] DELETE /users/v1/{username} → 401 — score=0.16 severity=LOW — Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- [ERROR_CONTRADICTION] PUT /users/v1/{username}/email → 401 — score=0.16 severity=LOW — Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- [ERROR_CONTRADICTION] PUT /users/v1/{username}/password → 401 — score=0.16 severity=LOW — Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- [ERROR_CONTRADICTION] POST /books/v1 → 401 — score=0.16 severity=LOW — Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- [ERROR_CONTRADICTION] GET /books/v1/{book_title} → 401 — score=0.16 severity=LOW — Error response body for 401 does not match contract. Details: 401 is not of type 'string'

### SUCCESS_CONTRADICTION
- [SUCCESS_CONTRADICTION] GET /books/v1/{book_title} → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: {'book_title': 'A', 'owner': 'username_sqcjzhvr', 'secret': 'A'} is not of type 'array'