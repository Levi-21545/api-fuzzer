# Deduplication report

API: `petclinic`

## Summary

- Planned requests: 240
- Executed requests: 240 (100.0%)
- Classified observations: 233
- Expected failures: 143
- Raw candidate findings: 90
- Unique operational findings: 47
- Deduplication reduction: 47.8%
- Candidate endpoints: 29
- FIS rationale coverage: 47/47 unique findings
- FIS fallbacks among unique findings: 6

`EXPECTED_FAILURE` remains an execution metric and is excluded before deduplication. A unique operational finding is a strict black-box signature, not a confirmed bug, vulnerability, or root cause.

## Findings by execution level

A signature may involve more than one level, so the final column can overlap across rows.

| Level | Case mix | Planned | Executed | Classified | Raw candidates | Unique signatures involved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | `baseline=36` | 36 | 36 | 29 | 27 | 27 |
| L1 | `mutation=204` | 204 | 204 | 204 | 63 | 30 |

## Candidate classifications

| Classification | Raw | Unique |
| --- | ---: | ---: |
| `ERROR_CONTRADICTION` | 35 | 21 |
| `SERVER_ERROR` | 48 | 19 |
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
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:01.996525663Z","title":"ConstraintViolationException","type":"http://127.0.0.1:9966/petclinic/api/owners"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `316.7 ms`, response-size signal `0.2764`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (0.61); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 2. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `5`
- Representative case: `case-000224`
- Signature: `8553c660fece`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"username":"A"}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:06:07.234919199Z","title":"IllegalArgumentException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `73.74 ms`, response-size signal `0.2705`
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
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:02.330841711Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `43.99 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 4. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /owners/{ownerId}/pets`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `4`
- Representative case: `case-000048`
- Signature: `dd7e1dc9246f`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:16.118484383Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `35.38 ms`, response-size signal `0.293`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 5. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /owners/{ownerId}/pets/{petId}/visits`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000087`
- Signature: `043a17a33230`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets/0/visits","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:27.400311402Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets/0/visits"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `63.74 ms`, response-size signal `0.3105`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 6. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /pettypes`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000097`
- Signature: `d5e01797bfcc`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pettypes","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:30.379702054Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pettypes"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `34.54 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 7. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /specialties`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000164`
- Signature: `e5782635852c`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/specialties","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:49.898704840Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/specialties"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `33.04 ms`, response-size signal `0.2891`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 8. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000239`
- Signature: `831a9d237c63`
- Input strategy: `null_item` on `/roles` (items.type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"roles":[null],"username":"A"}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:06:11.477553732Z","title":"NullPointerException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `24.03 ms`, response-size signal `0.2666`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 9. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `4`
- Representative case: `case-000225`
- Signature: `cae28c1ebc75`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:06:07.506245802Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `21.89 ms`, response-size signal `0.2773`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 10. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000195`
- Signature: `b4e63503470f`
- Input strategy: `null_item` on `/specialties` (items.type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[null]}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:58.979143939Z","title":"NullPointerException","type":"http://127.0.0.1:9966/petclinic/api/vets"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `32.6 ms`, response-size signal `0.2646`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 11. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `4`
- Representative case: `case-000181`
- Signature: `cdb092d8e699`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:55.081318444Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/vets"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `17.32 ms`, response-size signal `0.2754`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 12. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /visits`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `3`
- Representative case: `case-000140`
- Signature: `ce37a9c98dfa`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/visits","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:42.850328773Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/visits"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `78.25 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 13. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /owners/{ownerId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000026`
- Signature: `c92e0768469d`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:09.688092281Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `43.95 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 14. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /owners/{ownerId}/pets/{petId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `4`
- Representative case: `case-000068`
- Signature: `ea69b4788f9f`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:21.876871991Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets/0"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `29.39 ms`, response-size signal `0.2969`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 15. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /pets/{petId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `4`
- Representative case: `case-000119`
- Signature: `540750d5a215`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:36.832028467Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pets/0"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `32.9 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 16. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /pettypes/{petTypeId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000105`
- Signature: `f7bf0f82a682`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pettypes/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:32.689380950Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pettypes/0"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `38.14 ms`, response-size signal `0.2871`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 17. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /specialties/{specialtyId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000172`
- Signature: `f05ef8751744`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/specialties/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:52.286370316Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/specialties/0"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `43.44 ms`, response-size signal `0.293`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 18. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /vets/{vetId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `4`
- Representative case: `case-000203`
- Signature: `524271566781`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:06:01.254477501Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/vets/0"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `28.99 ms`, response-size signal `0.2793`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 19. HIGH · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /visits/{visitId}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000153`
- Signature: `1e486bc266d0`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/visits/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-08-01T18:05:46.726236749Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/visits/0"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `21.19 ms`, response-size signal `0.2832`
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
- Representative case: `case-000022`
- Signature: `73ba1edf4fed`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `201.5 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (0.99); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION_AND_SLOW` (strength `0.0025`) — medium status deviation and slow response -> medium severity

### 2. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /pettypes`
- HTTP status: `201`
- Score: `0.4`
- Occurrences in this run: `1`
- Representative case: `case-000096`
- Signature: `2676459b4028`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":"A"}`
- Response excerpt: `{"id":7,"name":"A"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.4`, response time `66.63 ms`, response-size signal `0.03711`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 3. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /specialties`
- HTTP status: `201`
- Score: `0.4`
- Occurrences in this run: `1`
- Representative case: `case-000163`
- Signature: `5b8c5601b520`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":"A"}`
- Response excerpt: `{"id":4,"name":"A"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.4`, response time `72.55 ms`, response-size signal `0.03711`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 4. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /vets`
- HTTP status: `201`
- Score: `0.4`
- Occurrences in this run: `1`
- Representative case: `case-000180`
- Signature: `19bd3aa6c1a1`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[{"name":"A"}]}`
- Response excerpt: `{"firstName":"A","id":7,"lastName":"A","specialties":[{"id":4,"name":"A"}]}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.4`, response time `177.6 ms`, response-size signal `0.1465`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 5. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000046`
- Signature: `06f34c9f00ca`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `37.91 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 6. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000137`
- Signature: `eb676a9dfa2f`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `33.39 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 7. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000114`
- Signature: `c64a3ed3b47e`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `31.88 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 8. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000178`
- Signature: `9b36cbfe2022`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `33.34 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 9. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /vets/{vetId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000223`
- Signature: `90e5add03acb`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `30.91 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 10. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /visits/{visitId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000161`
- Signature: `4a3d849421b2`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `30.28 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 11. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000024`
- Signature: `c3c6cd08edbe`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `58.41 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 12. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners/{ownerId}/pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000066`
- Signature: `e35d26abb397`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `38.43 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 13. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000117`
- Signature: `072fdf574434`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `43.59 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 14. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000103`
- Signature: `60eda12a7031`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `45.73 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 15. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000170`
- Signature: `583767bb3841`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `43.21 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 16. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /vets/{vetId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000201`
- Signature: `762e16a59117`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `41.03 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 17. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /visits/{visitId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `1`
- Representative case: `case-000151`
- Signature: `b91af1ff1a28`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `82.65 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 18. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /owners/{ownerId}/pets`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000047`
- Signature: `3753d722c9d6`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `108.4 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 19. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000025`
- Signature: `8515e8bd0828`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"address":"A","city":"A","firstName":"A","lastName":"A","telephone":"0"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `56.67 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 20. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /owners/{ownerId}/pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000067`
- Signature: `9df5040d3f63`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `41.03 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 21. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /pets/{petId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000118`
- Signature: `c579df956569`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `87.06 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 22. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `2`
- Representative case: `case-000104`
- Signature: `f2aeaf043e5f`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"id":0,"name":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `39.08 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 23. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `2`
- Representative case: `case-000171`
- Signature: `b438e3e2aaad`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"name":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `127.2 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 24. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /vets/{vetId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000217`
- Signature: `a0cf3b2e8486`
- Input strategy: `null_item` on `/specialties` (items.type)
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"firstName":"A","lastName":"A","specialties":[null]}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `33.38 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 25. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /visits/{visitId}`
- HTTP status: `404`
- Score: `0.31`
- Occurrences in this run: `3`
- Representative case: `case-000152`
- Signature: `43dc38bb9224`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"description":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0`, response time `33.36 ms`, response-size signal `0`
- Dominant fuzzy terms: status_deviation=low (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE` (strength `1.0`) — low status deviation, normal response time, and expected response size -> low severity

### 26. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /pettypes`
- HTTP status: `201`
- Score: `0.4`
- Occurrences in this run: `1`
- Representative case: `case-000100`
- Signature: `27c5ee4a85d4`
- Input strategy: `wrong_type` on `/name` (type)
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":123}`
- Response excerpt: `{"id":8,"name":"123"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.4`, response time `36.01 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 27. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /specialties`
- HTTP status: `201`
- Score: `0.4`
- Occurrences in this run: `1`
- Representative case: `case-000167`
- Signature: `ec4711b08dd7`
- Input strategy: `wrong_type` on `/name` (type)
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":123}`
- Response excerpt: `{"id":5,"name":"123"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.4`, response time `28.13 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 28. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `201`
- Score: `0.4`
- Occurrences in this run: `1`
- Representative case: `case-000200`
- Signature: `96bb6f0391da`
- Input strategy: `wrong_type` on `/specialties/*/name` (type)
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[{"name":123}]}`
- Response excerpt: `{"firstName":"A","id":8,"lastName":"A","specialties":[{"id":5,"name":"123"}]}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.4`, response time `53.19 ms`, response-size signal `0.1504`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used
