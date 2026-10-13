# Deduplication report

API: `meilisearch`

## Summary

- Planned requests: 477
- Executed requests: 477 (100.0%)
- Classified observations: 402
- Expected failures: 84
- Raw candidate findings: 318
- Unique operational findings: 228
- Deduplication reduction: 28.3%
- Candidate endpoints: 84
- FIS rationale coverage: 228/228 unique findings
- FIS fallbacks among unique findings: 0

`EXPECTED_FAILURE` remains an execution metric and is excluded before deduplication. A unique operational finding is a strict black-box signature, not a confirmed bug, vulnerability, or root cause.

## Findings by execution level

A signature may involve more than one level, so the final column can overlap across rows.

| Level | Case mix | Planned | Executed | Classified | Raw candidates | Unique signatures involved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | `auth_probe=168, baseline=85` | 253 | 253 | 185 | 101 | 101 |
| L1 | `mutation=158` | 158 | 158 | 151 | 151 | 125 |
| L2 | `mutation=66` | 66 | 66 | 66 | 66 | 40 |

## Candidate classifications

| Classification | Raw | Unique |
| --- | ---: | ---: |
| `SUCCESS_CONTRADICTION` | 14 | 14 |
| `UNEXPECTED_ERROR_STATUS` | 304 | 214 |

## Endpoints with unique findings

- `POST /multi-search`: 24
- `PUT /indexes/{index_uid}/settings/localized-attributes`: 13
- `POST /keys`: 12
- `POST /swap-indexes`: 11
- `PUT /indexes/{index_uid}/settings/foreign-keys`: 9
- `POST /indexes/{index_uid}/documents/fetch`: 8
- `POST /indexes/{index_uid}/facet-search`: 7
- `POST /dynamic-search-rules`: 7
- `POST /indexes/{index_uid}/fields`: 6
- `POST /indexes/{index_uid}/documents/edit`: 5

## Potentially actionable findings

Showing 50 of 228 unique findings. The complete machine-readable set is available in `findings_unique.json`.

No potentially actionable findings in this run.

## Contract fidelity observations


### 1. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /indexes/{index_uid}/settings/localized-attributes`
- HTTP status: `200`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000133`
- Signature: `e7885af4bfce`
- Input strategy: baseline request
- Interpretation: Response body for 200 does not match the contract. Details: None is not of type 'array'
- Request payload: `null`
- Response excerpt: `null`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.65`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.60); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.6`) — medium behavioral contradiction -> medium priority

### 2. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PATCH /indexes/{index_uid}/settings/chat`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `case-000089`
- Signature: `9a398554bdfc`
- Input strategy: `empty_object` on `/` (unspecified)
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{}`
- Response excerpt: `{"code":"feature_not_enabled","link":"https://docs.meilisearch.com/errors#feature_not_enabled","message":"setting `chat` in the index settings requires enabling the `chat completions` experimental feature. See https://github.com/orgs/meilisearch/discussions/835","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 3. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /dynamic-search-rules`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `case-000005`
- Signature: `9facbbe6fd12`
- Input strategy: `empty_object` on `/` (unspecified)
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{}`
- Response excerpt: `{"code":"feature_not_enabled","link":"https://docs.meilisearch.com/errors#feature_not_enabled","message":"Using the `/dynamic-search-rules` routes requires enabling the `dynamic search rules` experimental feature. See https://github.com/orgs/meilisearch/discussions/884","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 4. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /export`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000016`
- Signature: `a85934777e06`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"apiKey":null,"indexes":null,"payloadSize":null,"url":null}`
- Response excerpt: `{"code":"invalid_export_url","link":"https://docs.meilisearch.com/errors#invalid_export_url","message":"Invalid value type at `.url`: expected a string, but found null","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 5. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /indexes/{index_uid}/documents/delete`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000027`
- Signature: `14da08e97765`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"filter":null}`
- Response excerpt: `{"code":"invalid_document_filter","link":"https://docs.meilisearch.com/errors#invalid_document_filter","message":"Invalid syntax for the filter parameter: `expected String, Array, found: null`.","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 6. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /indexes/{index_uid}/documents/edit`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000033`
- Signature: `5b3c750260ef`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"function":"A"}`
- Response excerpt: `{"code":"feature_not_enabled","link":"https://docs.meilisearch.com/errors#feature_not_enabled","message":"Using the documents edit route requires enabling the `edit documents by function` experimental feature. See https://github.com/orgs/meilisearch/discussions/762","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 7. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /indexes/{index_uid}/facet-search`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000058`
- Signature: `20af74cc52e4`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"facetName":"A"}`
- Response excerpt: `{"code":"invalid_facet_search_facet_name","link":"https://docs.meilisearch.com/errors#invalid_facet_search_facet_name","message":"Attribute `A` is not facet-searchable. This index does not have configured facet-searchable attributes. To make it facet-searchable add it to the `filterableAttributes` index settings.","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 8. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /keys`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000226`
- Signature: `410ebe2a9971`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"actions":["*"],"indexes":["A"]}`
- Response excerpt: `{"code":"missing_api_key_expires_at","link":"https://docs.meilisearch.com/errors#missing_api_key_expires_at","message":"Missing field `expiresAt`","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 9. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /multi-search`
- HTTP status: `200`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000251`
- Signature: `efc03edd207f`
- Input strategy: baseline request
- Interpretation: Response body for 200 does not match the contract. Details: 'hits' is a required property
- Request payload: `{"queries":[{"cropLength":0,"cropMarker":"A","highlightPostTag":"A","highlightPreTag":"A","indexUid":"A","matchingStrategy":"last","retrieveVectors":true,"showMatchesPosition":true,"showRankingScore":true,"showRankingScoreDetails":true}]}`
- Response excerpt: `{"results":[{"estimatedTotalHits":1,"hits":[{"_matchesPosition":{},"_rankingScore":1.0,"_rankingScoreDetails":{},"_vectors":{},"id":"A","title":"A"}],"indexUid":"A","limit":20,"offset":0,"processingTimeMs":2,"query":"","requestUid":"01a0d15f-e7c8-7f40-aeee-51abd1c777ad"}]}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.65`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.60); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.6`) — medium behavioral contradiction -> medium priority

### 10. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /swap-indexes`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `case-000283`
- Signature: `52b918701fad`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `[{"indexes":["A"]}]`
- Response excerpt: `{"code":"invalid_swap_indexes","link":"https://docs.meilisearch.com/errors#invalid_swap_indexes","message":"Two indexes must be given for each swap. The list `[\"A\"]` contains 1 indexes.","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 11. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `PUT /indexes/{index_uid}/settings/filterable-attributes`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000114`
- Signature: `e15055f241a9`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `[null]`
- Response excerpt: `{"code":"invalid_settings_filterable_attributes","link":"https://docs.meilisearch.com/errors#invalid_settings_filterable_attributes","message":"Invalid value type at `[0]`: expected a string, but found null","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 12. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `PUT /indexes/{index_uid}/settings/foreign-keys`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000118`
- Signature: `7cefdccabf0f`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `[{"fieldName":"A","foreignIndexUid":"A"}]`
- Response excerpt: `{"code":"feature_not_enabled","link":"https://docs.meilisearch.com/errors#feature_not_enabled","message":"setting `foreignKeys` in the index settings requires enabling the `foreign_keys` experimental feature. See https://github.com/orgs/meilisearch/discussions/873","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 13. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `PUT /indexes/{index_uid}/settings/ranking-rules`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000185`
- Signature: `13daf873b86c`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `[null]`
- Response excerpt: `{"code":"invalid_settings_ranking_rules","link":"https://docs.meilisearch.com/errors#invalid_settings_ranking_rules","message":"Invalid value type at `[0]`: expected a string, but found null","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 14. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000034`
- Signature: `0ad966f258a4`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 15. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/chat`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000040`
- Signature: `d15742db189d`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 16. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/dictionary`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000048`
- Signature: `66b8c218d352`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 17. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/displayed-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000054`
- Signature: `ad8041c981b3`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 18. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/embedders`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000058`
- Signature: `e0d2122f707e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 19. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/faceting`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000064`
- Signature: `07007dc4ccef`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 20. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/filterable-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000072`
- Signature: `d80f7609c15e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 21. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/foreign-keys`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000078`
- Signature: `a41afaff7cea`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 22. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/localized-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000084`
- Signature: `a3d8752cbe5b`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 23. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/non-separator-tokens`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000090`
- Signature: `e2635978fe29`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 24. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/pagination`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000094`
- Signature: `66905cf38541`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 25. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/prefix-search`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000102`
- Signature: `6d721ec275c1`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 26. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/proximity-precision`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000108`
- Signature: `15c027deed46`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 27. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/ranking-rules`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000114`
- Signature: `3cffb28bbd8a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 28. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/searchable-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000120`
- Signature: `04be48d19190`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 29. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/separator-tokens`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000126`
- Signature: `58b243b35417`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 30. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/sortable-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000132`
- Signature: `577916e78638`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 31. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/stop-words`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000138`
- Signature: `6b27f92ecc7a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 32. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/synonyms`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000144`
- Signature: `008b78461cd0`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 33. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /indexes/{index_uid}/settings/typo-tolerance`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000148`
- Signature: `c3be24ba5454`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 34. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /batches/{batch_id}`
- HTTP status: `400`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000001`
- Signature: `62a692522e5c`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_batch_uids","link":"https://docs.meilisearch.com/errors#invalid_batch_uids","message":"Batch uid `A` is invalid. It should only contain numeric characters.","type":"invalid_request"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 35. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /batches/{batch_id}`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000002`
- Signature: `e8dea9b21072`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 36. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /experimental-features`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000008`
- Signature: `deba82b7228a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 37. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000014`
- Signature: `a2221ff0b8e2`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 38. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000032`
- Signature: `6d91202fe609`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 39. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/chat`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000038`
- Signature: `ddbbac0e6524`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 40. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/dictionary`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000044`
- Signature: `e749b6c0a163`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 41. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/displayed-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000050`
- Signature: `54ba26539dc2`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 42. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/embedders`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000056`
- Signature: `83029d491aba`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 43. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/faceting`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000062`
- Signature: `d6adca084db0`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 44. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/filterable-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000068`
- Signature: `f493d9f82303`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 45. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/foreign-keys`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000074`
- Signature: `897ff81c2877`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 46. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/localized-attributes`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000080`
- Signature: `c71145c4e3ec`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 47. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/non-separator-tokens`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000086`
- Signature: `212cce7946c0`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 48. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/pagination`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000092`
- Signature: `49289da36b8a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 49. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/prefix-search`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000098`
- Signature: `44d2ad806b02`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 50. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /indexes/{index_uid}/settings/proximity-precision`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000104`
- Signature: `a34e8d54b8e4`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"code":"invalid_api_key","link":"https://docs.meilisearch.com/errors#invalid_api_key","message":"The provided API key is invalid.","type":"auth"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority
