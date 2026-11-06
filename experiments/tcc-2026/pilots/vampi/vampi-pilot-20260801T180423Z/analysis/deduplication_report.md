# Deduplication report

API: `vampi`

## Summary

- Planned requests: 44
- Executed requests: 44 (100.0%)
- Classified observations: 34
- Expected failures: 27
- Raw candidate findings: 7
- Unique operational findings: 7
- Deduplication reduction: 0.0%
- Candidate endpoints: 6
- FIS rationale coverage: 7/7 unique findings
- FIS fallbacks among unique findings: 0

`EXPECTED_FAILURE` remains an execution metric and is excluded before deduplication. A unique operational finding is a strict black-box signature, not a confirmed bug, vulnerability, or root cause.

## Findings by execution level

A signature may involve more than one level, so the final column can overlap across rows.

| Level | Case mix | Planned | Executed | Classified | Raw candidates | Unique signatures involved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | `auth_probe=12, baseline=13` | 25 | 25 | 15 | 7 | 7 |
| L1 | `mutation=19` | 19 | 19 | 19 | 0 | 0 |

## Candidate classifications

| Classification | Raw | Unique |
| --- | ---: | ---: |
| `ERROR_CONTRADICTION` | 6 | 6 |
| `SUCCESS_CONTRADICTION` | 1 | 1 |

## Endpoints with unique findings

- `GET /books/v1/{book_title}`: 2
- `PUT /users/v1/{username}/email`: 1
- `PUT /users/v1/{username}/password`: 1
- `POST /books/v1`: 1
- `DELETE /users/v1/{username}`: 1
- `GET /me`: 1

## Potentially actionable findings

Showing 7 of 7 unique findings. The complete machine-readable set is available in `findings_unique.json`.

No potentially actionable findings in this run.

## Contract fidelity observations


### 1. LOW · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /books/v1/{book_title}`
- HTTP status: `200`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000032`
- Signature: `1c62262b7a4c`
- Input strategy: baseline request
- Interpretation: Response body for 200 does not match the contract. Details: {'book_title': 'A', 'owner': 'username_janqwnsw', 'secret': 'A'} is not of type 'array'
- Request payload: `null`
- Response excerpt: `{"book_title":"A","owner":"username_janqwnsw","secret":"A"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `15.81 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 2. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /users/v1/{username}`
- HTTP status: `401`
- Score: `0.3`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000003`
- Signature: `5debc727daa3`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- Request payload: `null`
- Response excerpt: `{"detail":"No authorization token provided","status":401,"title":"Unauthorized","type":"about:blank"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `10.21 ms`, response-size signal `0.1162`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 3. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /books/v1/{book_title}`
- HTTP status: `401`
- Score: `0.3`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000011`
- Signature: `1e2534aa692a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- Request payload: `null`
- Response excerpt: `{"detail":"No authorization token provided","status":401,"title":"Unauthorized","type":"about:blank"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `8.576 ms`, response-size signal `0.1162`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 4. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /me`
- HTTP status: `401`
- Score: `0.3`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000001`
- Signature: `87322b2e84b5`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- Request payload: `null`
- Response excerpt: `{"detail":"No authorization token provided","status":401,"title":"Unauthorized","type":"about:blank"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `4.269 ms`, response-size signal `0.1162`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 5. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /books/v1`
- HTTP status: `401`
- Score: `0.3`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000009`
- Signature: `45cea04eea84`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- Request payload: `{"book_title":"A","secret":"A"}`
- Response excerpt: `{"detail":"No authorization token provided","status":401,"title":"Unauthorized","type":"about:blank"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `10.72 ms`, response-size signal `0.1162`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 6. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `PUT /users/v1/{username}/email`
- HTTP status: `401`
- Score: `0.3`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000005`
- Signature: `040f80251096`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- Request payload: `{"email":"A"}`
- Response excerpt: `{"detail":"No authorization token provided","status":401,"title":"Unauthorized","type":"about:blank"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `9.024 ms`, response-size signal `0.1162`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 7. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `PUT /users/v1/{username}/password`
- HTTP status: `401`
- Score: `0.3`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000007`
- Signature: `115bbf07a404`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Error response body for 401 does not match contract. Details: 401 is not of type 'string'
- Request payload: `{"password":"<REDACTED>"}`
- Response excerpt: `{"detail":"No authorization token provided","status":401,"title":"Unauthorized","type":"about:blank"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `9.085 ms`, response-size signal `0.1162`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity
