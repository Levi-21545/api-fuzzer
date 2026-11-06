# Deduplication report

API: `petclinic`

## Summary

- Planned requests: 356
- Executed requests: 356 (100.0%)
- Classified observations: 349
- Expected failures: 231
- Raw candidate findings: 118
- Unique operational findings: 47
- Deduplication reduction: 60.2%
- Candidate endpoints: 29
- FIS rationale coverage: 47/47 unique findings
- FIS fallbacks among unique findings: 0

`EXPECTED_FAILURE` remains an execution metric and is excluded before deduplication. A unique operational finding is a strict black-box signature, not a confirmed bug, vulnerability, or root cause.

## Findings by execution level

A signature may involve more than one level, so the final column can overlap across rows.

| Level | Case mix | Planned | Executed | Classified | Raw candidates | Unique signatures involved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | `baseline=36` | 36 | 36 | 29 | 27 | 27 |
| L1 | `mutation=204` | 204 | 204 | 204 | 63 | 30 |
| L2 | `mutation=116` | 116 | 116 | 116 | 28 | 13 |

## Candidate classifications

| Classification | Raw | Unique |
| --- | ---: | ---: |
| `ERROR_CONTRADICTION` | 36 | 21 |
| `SERVER_ERROR` | 75 | 19 |
| `SUCCESS_CONTRADICTION` | 6 | 6 |
| `UNEXPECTED_ERROR_STATUS` | 1 | 1 |

## Endpoints with unique findings

- `POST /vets`: 4
- `POST /pettypes`: 3
- `POST /specialties`: 3
- `POST /users`: 3
- `PUT /visits/{visitId}`: 2
- `POST /owners/{ownerId}/pets`: 2
- `PUT /vets/{vetId}`: 2
- `PUT /pets/{petId}`: 2
- `PUT /owners/{ownerId}`: 2
- `POST /owners`: 2

## Potentially actionable findings

Showing 47 of 47 unique findings. The complete machine-readable set is available in `findings_unique.json`.

### 1. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /owners`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `3`
- Representative case: `case-000001`
- Signature: `8bd992e08c48`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"address":"A","city":"A","firstName":"A","lastName":"A","telephone":"0"}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:12:51.892829400Z","title":"ConstraintViolationException","type":"http://127.0.0.1:9966/petclinic/api/owners"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `322.5 ms`, response-size signal `0.2764`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (0.59); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 2. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000330`
- Signature: `8553c660fece`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"username":"A"}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:27.035466194Z","title":"IllegalArgumentException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `82.08 ms`, response-size signal `0.2705`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 3. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /owners`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000002`
- Signature: `9981fef4dff8`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:12:52.228188803Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `43.29 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 4. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /owners/{ownerId}/pets`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000068`
- Signature: `dd7e1dc9246f`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:11.845786731Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `36.71 ms`, response-size signal `0.293`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 5. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /owners/{ownerId}/pets/{petId}/visits`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000127`
- Signature: `043a17a33230`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets/0/visits","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:29.150818104Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets/0/visits"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `31.72 ms`, response-size signal `0.3105`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 6. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /pettypes`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000145`
- Signature: `d5e01797bfcc`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pettypes","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:34.399932345Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pettypes"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `29.97 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 7. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /specialties`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000250`
- Signature: `e5782635852c`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/specialties","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:04.311539704Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/specialties"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `25.13 ms`, response-size signal `0.2891`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 8. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000345`
- Signature: `831a9d237c63`
- Input strategy: `null_item` on `/roles` (items.type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"roles":[null],"username":"A"}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:31.298967169Z","title":"NullPointerException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `28.35 ms`, response-size signal `0.2666`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 9. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `5`
- Representative case: `case-000331`
- Signature: `cae28c1ebc75`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:27.312364644Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `26.16 ms`, response-size signal `0.2773`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 10. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000281`
- Signature: `b4e63503470f`
- Input strategy: `null_item` on `/specialties` (items.type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[null]}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:13.192965498Z","title":"NullPointerException","type":"http://127.0.0.1:9966/petclinic/api/vets"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `34.6 ms`, response-size signal `0.2646`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 11. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000267`
- Signature: `cdb092d8e699`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:09.252578279Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/vets"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `8.862 ms`, response-size signal `0.2754`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 12. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /visits`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `5`
- Representative case: `case-000208`
- Signature: `ce37a9c98dfa`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/visits","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:52.344842935Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/visits"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `13.99 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 13. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /owners/{ownerId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000036`
- Signature: `c92e0768469d`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:02.404009867Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `30.54 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 14. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /owners/{ownerId}/pets/{petId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000098`
- Signature: `ea69b4788f9f`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:20.507235530Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets/0"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `31.42 ms`, response-size signal `0.2969`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 15. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /pets/{petId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000177`
- Signature: `540750d5a215`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:43.556973959Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pets/0"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `23.31 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 16. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /pettypes/{petTypeId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000153`
- Signature: `f7bf0f82a682`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pettypes/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:36.664788304Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pettypes/0"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `37.96 ms`, response-size signal `0.2871`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 17. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /specialties/{specialtyId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000258`
- Signature: `f05ef8751744`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/specialties/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:06.578834739Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/specialties/0"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `31.12 ms`, response-size signal `0.293`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 18. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /vets/{vetId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000299`
- Signature: `524271566781`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:14:18.316788547Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/vets/0"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `26.04 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 19. HIGH · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /visits/{visitId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `6`
- Representative case: `case-000231`
- Signature: `1e486bc266d0`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/visits/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T21:13:58.901684774Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/visits/0"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `25.45 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

## Contract fidelity observations


### 1. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners`
- HTTP status: `404`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000032`
- Signature: `73ba1edf4fed`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `209.3 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (0.97); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 2. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /pettypes`
- HTTP status: `201`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000144`
- Signature: `2676459b4028`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":"A"}`
- Response excerpt: `{"id":7,"name":"A"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.4`, response time `66.88 ms`, response-size signal `0.03711`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 3. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /specialties`
- HTTP status: `201`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000249`
- Signature: `5b8c5601b520`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":"A"}`
- Response excerpt: `{"id":4,"name":"A"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.4`, response time `53.93 ms`, response-size signal `0.03711`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 4. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /vets`
- HTTP status: `201`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000266`
- Signature: `19bd3aa6c1a1`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[{"name":"A"}]}`
- Response excerpt: `{"firstName":"A","id":7,"lastName":"A","specialties":[{"id":4,"name":"A"}]}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.4`, response time `180.8 ms`, response-size signal `0.1465`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 5. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000066`
- Signature: `06f34c9f00ca`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `74.8 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 6. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000205`
- Signature: `eb676a9dfa2f`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `42.93 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 7. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000172`
- Signature: `c64a3ed3b47e`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `29.14 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 8. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000264`
- Signature: `9b36cbfe2022`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `30.25 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 9. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /vets/{vetId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000329`
- Signature: `90e5add03acb`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `35.33 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 10. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /visits/{visitId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000247`
- Signature: `4a3d849421b2`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `32.84 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 11. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000034`
- Signature: `c3c6cd08edbe`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `62.74 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 12. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners/{ownerId}/pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000096`
- Signature: `e35d26abb397`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `53.12 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 13. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000175`
- Signature: `072fdf574434`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `41.91 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 14. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000151`
- Signature: `60eda12a7031`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `46.9 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 15. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000256`
- Signature: `583767bb3841`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `46.6 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 16. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /vets/{vetId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000297`
- Signature: `762e16a59117`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `39.18 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 17. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /visits/{visitId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000229`
- Signature: `b91af1ff1a28`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `39.83 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 18. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /owners/{ownerId}/pets`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000067`
- Signature: `3753d722c9d6`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `173 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 19. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000035`
- Signature: `8515e8bd0828`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"address":"A","city":"A","firstName":"A","lastName":"A","telephone":"0"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `40.71 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 20. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /owners/{ownerId}/pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000097`
- Signature: `9df5040d3f63`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `46.14 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 21. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000176`
- Signature: `c579df956569`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `67.77 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 22. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `2`
- Representative case: `case-000152`
- Signature: `f2aeaf043e5f`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"id":0,"name":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `32.57 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 23. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `2`
- Representative case: `case-000257`
- Signature: `b438e3e2aaad`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"name":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `32.56 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 24. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /vets/{vetId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000313`
- Signature: `a0cf3b2e8486`
- Input strategy: `null_item` on `/specialties` (items.type)
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"firstName":"A","lastName":"A","specialties":[null]}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `30.85 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 25. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /visits/{visitId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `4`
- Representative case: `case-000230`
- Signature: `43dc38bb9224`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"description":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0`, response time `28.69 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION` (strength `1.0`) — low status deviation -> low severity

### 26. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /pettypes`
- HTTP status: `201`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000148`
- Signature: `27c5ee4a85d4`
- Input strategy: `wrong_type` on `/name` (type)
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":123}`
- Response excerpt: `{"id":8,"name":"123"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `41.37 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 27. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /specialties`
- HTTP status: `201`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000253`
- Signature: `ec4711b08dd7`
- Input strategy: `wrong_type` on `/name` (type)
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":123}`
- Response excerpt: `{"id":5,"name":"123"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `31.29 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 28. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `201`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000286`
- Signature: `96bb6f0391da`
- Input strategy: `wrong_type` on `/specialties/*/name` (type)
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[{"name":123}]}`
- Response excerpt: `{"firstName":"A","id":8,"lastName":"A","specialties":[{"id":5,"name":"123"}]}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `51.49 ms`, response-size signal `0.1504`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity
