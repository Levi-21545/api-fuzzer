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
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:23:32.384351472Z","title":"ConstraintViolationException","type":"http://127.0.0.1:9966/petclinic/api/owners"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `1`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=strong (1.00); access_control_exposure=none (1.00)
- Strongest activated rule: `R4_HIGH_CONTRADICTION_STRONG_EVIDENCE` (strength `1.0`) — high contradiction with strong evidence -> high priority

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
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:25:09.196459269Z","title":"IllegalArgumentException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `1`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=strong (1.00); access_control_exposure=none (1.00)
- Strongest activated rule: `R4_HIGH_CONTRADICTION_STRONG_EVIDENCE` (strength `1.0`) — high contradiction with strong evidence -> high priority

### 3. MEDIUM · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /owners`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000002`
- Signature: `9981fef4dff8`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:23:32.757412566Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 4. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /owners/{ownerId}/pets`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000068`
- Signature: `dd7e1dc9246f`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:23:52.999910059Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 5. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /owners/{ownerId}/pets/{petId}/visits`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000127`
- Signature: `043a17a33230`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets/0/visits","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:10.070282173Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets/0/visits"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 6. MEDIUM · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /pettypes`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000145`
- Signature: `d5e01797bfcc`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pettypes","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:15.364800995Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pettypes"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 7. MEDIUM · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /specialties`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000250`
- Signature: `e5782635852c`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/specialties","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:46.259586888Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/specialties"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 8. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `case-000345`
- Signature: `831a9d237c63`
- Input strategy: `null_item` on `/roles` (items.type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"roles":[null],"username":"A"}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:25:13.485849831Z","title":"NullPointerException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 9. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /users`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `5`
- Representative case: `case-000331`
- Signature: `cae28c1ebc75`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/users","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:25:09.465110371Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/users"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 10. MEDIUM · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000281`
- Signature: `b4e63503470f`
- Input strategy: `null_item` on `/specialties` (items.type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[null]}`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:55.345941568Z","title":"NullPointerException","type":"http://127.0.0.1:9966/petclinic/api/vets"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 11. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /vets`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000267`
- Signature: `cdb092d8e699`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:51.354997796Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/vets"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 12. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `POST /visits`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `5`
- Representative case: `case-000208`
- Signature: `ce37a9c98dfa`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/visits","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:33.682344217Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/visits"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 13. MEDIUM · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /owners/{ownerId}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000036`
- Signature: `c92e0768469d`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:23:43.639792698Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 14. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /owners/{ownerId}/pets/{petId}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000098`
- Signature: `ea69b4788f9f`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/owners/0/pets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:01.639432114Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/owners/0/pets/0"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 15. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /pets/{petId}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000177`
- Signature: `540750d5a215`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:24.630897464Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pets/0"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 16. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /pettypes/{petTypeId}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000153`
- Signature: `f7bf0f82a682`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/pettypes/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:17.628902858Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/pettypes/0"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 17. MEDIUM · SERVER_ERROR

- Execution level(s): `L1`
- Case kind(s): `mutation`
- Endpoint: `PUT /specialties/{specialtyId}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000258`
- Signature: `f05ef8751744`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/specialties/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:48.554905810Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/specialties/0"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 18. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /vets/{vetId}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000299`
- Signature: `524271566781`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/vets/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:25:00.473413992Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/vets/0"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 19. MEDIUM · SERVER_ERROR

- Execution level(s): `L1, L2`
- Case kind(s): `mutation`
- Endpoint: `PUT /visits/{visitId}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `6`
- Representative case: `case-000231`
- Signature: `1e486bc266d0`
- Input strategy: `wrong_type` on `/` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `"not-an-object"`
- Response excerpt: `{"detail":"An unexpected error occurred while processing your request","instance":"/petclinic/api/visits/0","schemaValidationErrors":[],"status":500,"timestamp":"2026-09-24T02:24:40.588371608Z","title":"HttpMessageNotReadableException","type":"http://127.0.0.1:9966/petclinic/api/visits/0"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

## Contract fidelity observations


### 1. LOW · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /pettypes`
- HTTP status: `201`
- Score: `0.17`
- Occurrences in this run: `1`
- Representative case: `case-000144`
- Signature: `2676459b4028`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":"A"}`
- Response excerpt: `{"id":7,"name":"A"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.25`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (0.75); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `0.75`) — low behavioral contradiction -> low priority

### 2. LOW · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /specialties`
- HTTP status: `201`
- Score: `0.17`
- Occurrences in this run: `1`
- Representative case: `case-000249`
- Signature: `5b8c5601b520`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"name":"A"}`
- Response excerpt: `{"id":4,"name":"A"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.25`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (0.75); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `0.75`) — low behavioral contradiction -> low priority

### 3. LOW · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /vets`
- HTTP status: `201`
- Score: `0.17`
- Occurrences in this run: `1`
- Representative case: `case-000266`
- Signature: `19bd3aa6c1a1`
- Input strategy: baseline request
- Interpretation: API returned undocumented success status code 201.
- Request payload: `{"firstName":"A","lastName":"A","specialties":[{"name":"A"}]}`
- Response excerpt: `{"firstName":"A","id":7,"lastName":"A","specialties":[{"id":4,"name":"A"}]}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.25`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (0.75); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `0.75`) — low behavioral contradiction -> low priority

### 4. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000066`
- Signature: `06f34c9f00ca`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 5. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /pets/{petId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000205`
- Signature: `eb676a9dfa2f`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 6. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000172`
- Signature: `c64a3ed3b47e`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 7. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000264`
- Signature: `9b36cbfe2022`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 8. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /vets/{vetId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000329`
- Signature: `90e5add03acb`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 9. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `DELETE /visits/{visitId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000247`
- Signature: `4a3d849421b2`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 10. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000032`
- Signature: `73ba1edf4fed`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 11. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000034`
- Signature: `c3c6cd08edbe`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 12. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /owners/{ownerId}/pets/{petId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000096`
- Signature: `e35d26abb397`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 13. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /pets/{petId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000175`
- Signature: `072fdf574434`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 14. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000151`
- Signature: `60eda12a7031`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 15. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000256`
- Signature: `583767bb3841`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 16. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /vets/{vetId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000297`
- Signature: `762e16a59117`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 17. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /visits/{visitId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000229`
- Signature: `b91af1ff1a28`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `null`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 18. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /owners/{ownerId}/pets`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `3`
- Representative case: `case-000067`
- Signature: `3753d722c9d6`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 19. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /owners/{ownerId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `3`
- Representative case: `case-000035`
- Signature: `8515e8bd0828`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"address":"A","city":"A","firstName":"A","lastName":"A","telephone":"0"}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 20. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /owners/{ownerId}/pets/{petId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `3`
- Representative case: `case-000097`
- Signature: `9df5040d3f63`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 21. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /pets/{petId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `3`
- Representative case: `case-000176`
- Signature: `c579df956569`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"birthDate":"2000-01-01","name":"A","type":{"id":0,"name":"A"}}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 22. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /pettypes/{petTypeId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `case-000152`
- Signature: `f2aeaf043e5f`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"id":0,"name":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 23. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /specialties/{specialtyId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `case-000257`
- Signature: `b438e3e2aaad`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"name":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 24. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /vets/{vetId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `3`
- Representative case: `case-000313`
- Signature: `a0cf3b2e8486`
- Input strategy: `null_item` on `/specialties` (items.type)
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"firstName":"A","lastName":"A","specialties":[null]}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 25. LOW · ERROR_CONTRADICTION

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /visits/{visitId}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `4`
- Representative case: `case-000230`
- Signature: `43dc38bb9224`
- Input strategy: baseline request
- Interpretation: Error response body for 404 does not match contract. Details: None is not of type 'object'
- Request payload: `{"description":"A"}`
- Response excerpt: `""`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

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
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.7`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.40); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.4`) — medium behavioral contradiction -> medium priority

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
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.7`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.40); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.4`) — medium behavioral contradiction -> medium priority

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
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.7`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.40); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.4`) — medium behavioral contradiction -> medium priority
