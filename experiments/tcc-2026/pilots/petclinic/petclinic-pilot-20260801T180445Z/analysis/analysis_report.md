# Relatório de Análise

Total de resultados classificados: 233

## Por classificação
- EXPECTED_FAILURE: 143
- SERVER_ERROR: 48
- ERROR_CONTRADICTION: 35
- SUCCESS_CONTRADICTION: 6
- UNEXPECTED_ERROR_STATUS: 1

## Por severidade
- HIGH: 48
- MEDIUM: 7
- LOW: 178

## Endpoints com mais achados (top 10)
- POST /owners: 21
- PUT /owners/{ownerId}: 21
- POST /vets: 21
- PUT /vets/{vetId}: 21
- POST /owners/{ownerId}/pets: 19
- PUT /owners/{ownerId}/pets/{petId}: 19
- PUT /pets/{petId}: 19
- POST /users: 17
- POST /visits: 12
- PUT /pettypes/{petTypeId}: 10

## Amostras por classificação (até 50 cada)

### EXPECTED_FAILURE
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.18 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.17 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.18 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.17 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /owners/{ownerId}/pets → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId}/pets/{petId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId}/pets/{petId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId}/pets/{petId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] PUT /owners/{ownerId}/pets/{petId} → 400 — score=0.16 severity=LOW — API correctly rejected with documented 400 error.

### SERVER_ERROR
- [SERVER_ERROR] POST /owners → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /owners/{ownerId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners/{ownerId}/pets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners/{ownerId}/pets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners/{ownerId}/pets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners/{ownerId}/pets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /owners/{ownerId}/pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /owners/{ownerId}/pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /owners/{ownerId}/pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /owners/{ownerId}/pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners/{ownerId}/pets/{petId}/visits → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /owners/{ownerId}/pets/{petId}/visits → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /pettypes → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /pettypes/{petTypeId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /pettypes/{petTypeId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /pets/{petId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /visits → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /visits → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /visits → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /visits/{visitId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /visits/{visitId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /specialties → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /specialties/{specialtyId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /vets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /vets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /vets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /vets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /vets → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /vets/{vetId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /vets/{vetId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /vets/{vetId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /vets/{vetId} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /users → 500 — score=0.84 severity=HIGH — Server returned a 500 error.

### ERROR_CONTRADICTION
- [ERROR_CONTRADICTION] GET /owners/{ownerId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /owners/{ownerId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /owners/{ownerId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /owners/{ownerId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] DELETE /owners/{ownerId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] POST /owners/{ownerId}/pets → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] POST /owners/{ownerId}/pets → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] POST /owners/{ownerId}/pets → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] GET /owners/{ownerId}/pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /owners/{ownerId}/pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /owners/{ownerId}/pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /owners/{ownerId}/pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] GET /pettypes/{petTypeId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /pettypes/{petTypeId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /pettypes/{petTypeId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] DELETE /pettypes/{petTypeId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] GET /pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] DELETE /pets/{petId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] GET /visits/{visitId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /visits/{visitId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /visits/{visitId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /visits/{visitId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] DELETE /visits/{visitId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] GET /specialties/{specialtyId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /specialties/{specialtyId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /specialties/{specialtyId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] DELETE /specialties/{specialtyId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] GET /vets/{vetId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /vets/{vetId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /vets/{vetId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] PUT /vets/{vetId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'
- [ERROR_CONTRADICTION] DELETE /vets/{vetId} → 404 — score=0.31 severity=LOW — Error response body for 404 does not match contract. Details: None is not of type 'object'

### SUCCESS_CONTRADICTION
- [SUCCESS_CONTRADICTION] POST /pettypes → 201 — score=0.4 severity=MEDIUM — API returned undocumented success status code 201.
- [SUCCESS_CONTRADICTION] POST /pettypes → 201 — score=0.4 severity=MEDIUM — API returned undocumented success status code 201.
- [SUCCESS_CONTRADICTION] POST /specialties → 201 — score=0.4 severity=MEDIUM — API returned undocumented success status code 201.
- [SUCCESS_CONTRADICTION] POST /specialties → 201 — score=0.4 severity=MEDIUM — API returned undocumented success status code 201.
- [SUCCESS_CONTRADICTION] POST /vets → 201 — score=0.4 severity=MEDIUM — API returned undocumented success status code 201.
- [SUCCESS_CONTRADICTION] POST /vets → 201 — score=0.4 severity=MEDIUM — API returned undocumented success status code 201.

### UNEXPECTED_ERROR_STATUS
- [UNEXPECTED_ERROR_STATUS] GET /owners → 404 — score=0.5 severity=MEDIUM — API returned an undocumented error status code: 404.