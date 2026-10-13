# Relatório de Análise

Total de resultados classificados: 402

## Por classificação
- UNEXPECTED_ERROR_STATUS: 304
- EXPECTED_FAILURE: 84
- SUCCESS_CONTRADICTION: 14

## Por severidade
- HIGH: 0
- MEDIUM: 27
- LOW: 375

## Endpoints com mais achados (top 10)
- POST /multi-search: 33
- PUT /indexes/{index_uid}/settings/localized-attributes: 28
- POST /keys: 26
- POST /swap-indexes: 26
- POST /indexes/{index_uid}/documents/fetch: 19
- PUT /indexes/{index_uid}/settings/foreign-keys: 16
- POST /dynamic-search-rules: 13
- POST /indexes/{index_uid}/facet-search: 13
- POST /indexes/{index_uid}/fields: 11
- POST /indexes/{index_uid}/documents/edit: 7

## Amostras por classificação (até 50 cada)

### UNEXPECTED_ERROR_STATUS
- [UNEXPECTED_ERROR_STATUS] GET /batches/{batch_id} → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /dumps → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /dynamic-search-rules → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /experimental-features → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PATCH /experimental-features → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /export → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes/{index_uid}/compact → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes/{index_uid}/documents/delete → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes/{index_uid}/documents/delete-batch → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes/{index_uid}/documents/edit → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes/{index_uid}/documents/fetch → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes/{index_uid}/facet-search → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] POST /indexes/{index_uid}/fields → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PATCH /indexes/{index_uid}/settings → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/chat → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/chat → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PATCH /indexes/{index_uid}/settings/chat → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/dictionary → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PUT /indexes/{index_uid}/settings/dictionary → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/dictionary → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/displayed-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PUT /indexes/{index_uid}/settings/displayed-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/displayed-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/embedders → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/embedders → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PATCH /indexes/{index_uid}/settings/embedders → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/faceting → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/faceting → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PATCH /indexes/{index_uid}/settings/faceting → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/filterable-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PUT /indexes/{index_uid}/settings/filterable-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/filterable-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/foreign-keys → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PUT /indexes/{index_uid}/settings/foreign-keys → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/foreign-keys → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/localized-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PUT /indexes/{index_uid}/settings/localized-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/localized-attributes → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/non-separator-tokens → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PUT /indexes/{index_uid}/settings/non-separator-tokens → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/non-separator-tokens → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/pagination → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] DELETE /indexes/{index_uid}/settings/pagination → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PATCH /indexes/{index_uid}/settings/pagination → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] GET /indexes/{index_uid}/settings/prefix-search → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.
- [UNEXPECTED_ERROR_STATUS] PUT /indexes/{index_uid}/settings/prefix-search → 403 — score=0.16 severity=LOW — API returned an undocumented error status code: 403.

### EXPECTED_FAILURE
- [EXPECTED_FAILURE] GET /batches/{batch_id} → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /dumps → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /dynamic-search-rules → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /experimental-features → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PATCH /experimental-features → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /export → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes/{index_uid}/compact → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes/{index_uid}/documents/delete → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes/{index_uid}/documents/delete-batch → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes/{index_uid}/documents/edit → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes/{index_uid}/documents/fetch → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes/{index_uid}/facet-search → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /indexes/{index_uid}/fields → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PATCH /indexes/{index_uid}/settings → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/chat → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/chat → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PATCH /indexes/{index_uid}/settings/chat → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/dictionary → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /indexes/{index_uid}/settings/dictionary → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/dictionary → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/displayed-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /indexes/{index_uid}/settings/displayed-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/displayed-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/embedders → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/embedders → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PATCH /indexes/{index_uid}/settings/embedders → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/faceting → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/faceting → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PATCH /indexes/{index_uid}/settings/faceting → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/filterable-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /indexes/{index_uid}/settings/filterable-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/filterable-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/foreign-keys → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /indexes/{index_uid}/settings/foreign-keys → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/foreign-keys → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/localized-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /indexes/{index_uid}/settings/localized-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/localized-attributes → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/non-separator-tokens → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /indexes/{index_uid}/settings/non-separator-tokens → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/non-separator-tokens → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/pagination → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] DELETE /indexes/{index_uid}/settings/pagination → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PATCH /indexes/{index_uid}/settings/pagination → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /indexes/{index_uid}/settings/prefix-search → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] PUT /indexes/{index_uid}/settings/prefix-search → 401 — score=0.16 severity=LOW — API correctly rejected with documented 401 error.

### SUCCESS_CONTRADICTION
- [SUCCESS_CONTRADICTION] POST /export → 200 — score=0.17 severity=LOW — API returned undocumented success status code 200.
- [SUCCESS_CONTRADICTION] GET /indexes/{index_uid}/settings/localized-attributes → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: None is not of type 'array'
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property
- [SUCCESS_CONTRADICTION] POST /multi-search → 200 — score=0.5 severity=MEDIUM — Response body for 200 does not match the contract. Details: 'hits' is a required property