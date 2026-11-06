# Deduplication report

API: `realworld`

## Summary

- Planned requests: 142
- Executed requests: 142 (100.0%)
- Classified observations: 135
- Expected failures: 122
- Raw candidate findings: 13
- Unique operational findings: 13
- Deduplication reduction: 0.0%
- Candidate endpoints: 12
- FIS rationale coverage: 13/13 unique findings
- FIS fallbacks among unique findings: 0

`EXPECTED_FAILURE` remains an execution metric and is excluded before deduplication. A unique operational finding is a strict black-box signature, not a confirmed bug, vulnerability, or root cause.

## Findings by execution level

A signature may involve more than one level, so the final column can overlap across rows.

| Level | Case mix | Planned | Executed | Classified | Raw candidates | Unique signatures involved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | `auth_probe=24, baseline=19` | 43 | 43 | 38 | 12 | 12 |
| L1 | `mutation=62` | 62 | 62 | 60 | 1 | 1 |
| L2 | `mutation=37` | 37 | 37 | 37 | 0 | 0 |

## Candidate classifications

| Classification | Raw | Unique |
| --- | ---: | ---: |
| `SERVER_ERROR` | 12 | 12 |
| `UNEXPECTED_SUCCESS` | 1 | 1 |

## Endpoints with unique findings

- `PUT /user`: 2
- `POST /articles/{slug}/favorite`: 1
- `DELETE /articles/{slug}/comments/{id}`: 1
- `DELETE /profiles/{username}/follow`: 1
- `PUT /articles/{slug}`: 1
- `POST /articles/{slug}/comments`: 1
- `DELETE /articles/{slug}/favorite`: 1
- `DELETE /articles/{slug}`: 1
- `GET /user`: 1
- `POST /profiles/{username}/follow`: 1

## Potentially actionable findings

Showing 13 of 13 unique findings. The complete machine-readable set is available in `findings_unique.json`.

### 1. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /articles/{slug}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000016`
- Signature: `7a29d9d97aee`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `8.569 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 2. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /articles/{slug}/comments/{id}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000020`
- Signature: `2595808af433`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `8.458 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 3. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /articles/{slug}/favorite`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000024`
- Signature: `6e078a9e715f`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `7.799 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 4. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /profiles/{username}/follow`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000008`
- Signature: `2c9a126a0d11`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `6.274 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 5. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /articles/feed`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000010`
- Signature: `e630ac68c338`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `5.983 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 6. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /user`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000002`
- Signature: `b52688525ebe`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `8.146 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 7. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /articles`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000012`
- Signature: `c90788352a08`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `{"article":{"body":"A","description":"A","title":"A"}}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `7.878 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 8. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /articles/{slug}/comments`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000018`
- Signature: `5a92d85641b9`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `{"comment":{"body":"A"}}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `14.02 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 9. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /articles/{slug}/favorite`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000022`
- Signature: `2024b0172ce5`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `6.084 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 10. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /profiles/{username}/follow`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000006`
- Signature: `c2da57eb27b7`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `6.079 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 11. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `PUT /articles/{slug}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000014`
- Signature: `4771fb4a8d0e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `{"article":{"body":"A","description":"A","tagList":["A"],"title":"A"}}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `8.505 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 12. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `PUT /user`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000004`
- Signature: `2194627cec61`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Server returned a 500 error.
- Request payload: `{"user":{"bio":null,"email":"A","image":null,"password":"<REDACTED>","username":"A"}}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `7.715 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 13. MEDIUM · UNEXPECTED_SUCCESS

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /user`
- HTTP status: `200`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000042`
- Signature: `b8bb74a3d862`
- Input strategy: `wrong_type` on `/user` (type)
- Interpretation: Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- Request payload: `{"user":"not-an-object"}`
- Response excerpt: `{"user":{"bio":null,"email":"fuzzer-20260801211857-63185@test.com","image":null,"token":"<REDACTED>","username":"fuzzer-20260801211857-63185"}}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `41.68 ms`, response-size signal `0.3555`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

## Contract fidelity observations

No contract fidelity observations in this run.
