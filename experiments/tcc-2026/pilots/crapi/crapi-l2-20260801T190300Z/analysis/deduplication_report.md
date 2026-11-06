# Deduplication report

API: `crapi`

## Summary

- Planned requests: 411
- Executed requests: 411 (100.0%)
- Classified observations: 396
- Expected failures: 52
- Raw candidate findings: 344
- Unique operational findings: 198
- Deduplication reduction: 42.4%
- Candidate endpoints: 41
- FIS rationale coverage: 198/198 unique findings
- FIS fallbacks among unique findings: 0

`EXPECTED_FAILURE` remains an execution metric and is excluded before deduplication. A unique operational finding is a strict black-box signature, not a confirmed bug, vulnerability, or root cause.

## Findings by execution level

A signature may involve more than one level, so the final column can overlap across rows.

| Level | Case mix | Planned | Executed | Classified | Raw candidates | Unique signatures involved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | `auth_probe=70, baseline=44` | 114 | 114 | 100 | 92 | 69 |
| L1 | `mutation=171` | 171 | 171 | 170 | 147 | 101 |
| L2 | `mutation=126` | 126 | 126 | 126 | 105 | 66 |

## Candidate classifications

| Classification | Raw | Unique |
| --- | ---: | ---: |
| `ERROR_CONTRADICTION` | 57 | 40 |
| `SERVER_ERROR` | 106 | 24 |
| `SUCCESS_CONTRADICTION` | 4 | 2 |
| `UNEXPECTED_ERROR_STATUS` | 165 | 124 |
| `UNEXPECTED_SUCCESS` | 12 | 8 |

## Endpoints with unique findings

- `POST /identity/api/auth/signup`: 20
- `POST /workshop/api/mechanic/signup`: 15
- `POST /identity/api/v2/user/change-email`: 12
- `POST /workshop/api/shop/orders`: 12
- `POST /identity/api/auth/login`: 11
- `POST /identity/api/v2/vehicle/add_vehicle`: 11
- `POST /workshop/api/merchant/contact_mechanic`: 10
- `POST /identity/api/auth/v2.7/user/login-with-token`: 10
- `POST /workshop/api/shop/apply_coupon`: 9
- `POST /identity/api/auth/v2/check-otp`: 6

## Potentially actionable findings

Showing 50 of 198 unique findings. The complete machine-readable set is available in `findings_unique.json`.

### 1. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/mechanic/receive_report`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000315`
- Signature: `79d30d2bb959`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `40.99 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 2. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/shop/orders/{order_id}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000271`
- Signature: `8b97701e8e5d`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `42.24 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 3. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /community/api/v2/community/posts/{postId}/comment`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000209`
- Signature: `bddcd8d379f4`
- Input strategy: `empty_object` on `/` (unspecified)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `{"error":"mongo: no documents in result"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `16.53 ms`, response-size signal `0.08203`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 4. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v2.7/user/login-with-token`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `8`
- Representative case: `case-000114`
- Signature: `474766f33cd9`
- Input strategy: `wrong_type` on `/email` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":123,"token":"<REDACTED>"}`
- Response excerpt: `{"message":"Invalid Credentials","mfaRequired":false,"token":"<REDACTED>","type":""}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `25.53 ms`, response-size signal `0.1484`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 5. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v2/check-otp`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `15`
- Representative case: `case-000068`
- Signature: `07ec293b0660`
- Input strategy: `remove_required_property` on `/password` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":"AAAAA","otp":"AAA"}`
- Response excerpt: `"User was not found for parameters {userEmail=AAAAA}"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `23.12 ms`, response-size signal `0.0498`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 6. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v3/check-otp`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `15`
- Representative case: `case-000043`
- Signature: `183ed38ac8a8`
- Input strategy: `remove_required_property` on `/password` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":"AAAAA","otp":"AAA"}`
- Response excerpt: `"User was not found for parameters {userEmail=AAAAA}"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `21.24 ms`, response-size signal `0.0498`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 7. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/user/pictures`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000167`
- Signature: `de62037ba8a9`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"Current request is not a multipart request"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `15.68 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 8. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/v2/user/verify-email-token`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `18`
- Representative case: `case-000149`
- Signature: `8b675c6e4976`
- Input strategy: `empty_object` on `/` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `{"message":"Sorry, Token did't match","status":500}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `18.73 ms`, response-size signal `0.09961`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 9. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/user/videos`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000168`
- Signature: `8b6f6fa85814`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"Current request is not a multipart request"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `19.36 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 10. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /workshop/api/merchant/contact_mechanic`
- HTTP status: `503`
- Score: `0.84`
- Occurrences in this run: `9`
- Representative case: `case-000307`
- Signature: `01c248ce0771`
- Input strategy: `remove_required_property` on `/problem_details` (required); `remove_required_property` on `/vin` (required)
- Interpretation: Server returned a 503 error.
- Request payload: `{"mechanic_api":"A","mechanic_code":"A","number_of_repeats":0.0,"repeat_request_if_failed":true}`
- Response excerpt: `{"message":" 'number_of_repeats' should be between 1 and 100."}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `39.32 ms`, response-size signal `0.06152`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 11. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /workshop/api/shop/apply_coupon`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000274`
- Signature: `619733d8b18d`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"amount":0,"coupon_code":"A"}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `158.7 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 12. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /workshop/api/shop/orders`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000249`
- Signature: `ec34e1415a26`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"product_id":0,"quantity":0}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `75.85 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 13. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /workshop/api/shop/orders/return_order`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000273`
- Signature: `57d0d6cc793e`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `39.29 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 14. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /workshop/api/shop/orders/{order_id}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `11`
- Representative case: `case-000262`
- Signature: `8b2e5a1f7e6f`
- Input strategy: `empty_object` on `/` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `1`, response time `48.92 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 15. MEDIUM · UNEXPECTED_SUCCESS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/return_qr_code`
- HTTP status: `200`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000059`
- Signature: `95b2167d7099`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Authentication probe was accepted with status 200; the request used no valid credentials.
- Request payload: `null`
- Response excerpt: `"�PNG\r\n\u001a\n\u0000\u0000\u0000\rIHDR\u0000\u0000\u0004�\u0000\u0000\u0004�\b\u0002\u0000\u0000\u0000�Nc�\u0000\u0000\u0000\u0006bKGD\u0000�\u0000�\u0000�����\u0000\u0000\u001b�IDATx��ف��8\u0012\u0000����w�΁�b�͜\u0016#\u001cPI\"5�����\u0000\u0000\u0000��o=\u0000\u0000\u0000��\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000…`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `14.17 ms`, response-size signal `3`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (0.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

## Contract fidelity observations


### 1. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /identity/api/v2/admin/videos/{video_id}`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000021`
- Signature: `4725dbc318b6`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `11.52 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 2. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /identity/api/v2/user/videos/{video_id}`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000017`
- Signature: `b4eeb4c69c37`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `4.948 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 3. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /community/api/v2/community/posts/recent`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000037`
- Signature: `7c4f9f216eae`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `19.22 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 4. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /community/api/v2/community/posts/{postId}`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000031`
- Signature: `55d0f69f4361`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `53.12 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 5. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /community/api/v2/community/posts/{postId}`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000200`
- Signature: `8160209d882e`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `null`
- Response excerpt: `"{\"error\":\"mongo: no documents in result\"}\n{\"id\":\"\",\"title\":\"\",\"content\":\"\",\"author\":{\"nickname\":\"\",\"email\":\"\",\"vehicleid\":\"\",\"profile_pic_url\":\"\",\"created_at\":\"0001-01-01T00:00:00Z\"},\"comments\":null,\"authorid\":0,\"CreatedAt\":\"0001-01-01T00:00:00Z\"}\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `42.76 ms`, response-size signal `0.4844`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 6. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/user/videos/convert_video`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000019`
- Signature: `2daff72deff3`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `12 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 7. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /identity/api/v2/user/videos/convert_video`
- HTTP status: `403`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000184`
- Signature: `6c6a202510bf`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"message":"Thi-S endpoint S-hould be accessed only inte-Rnally. -Fine? , endpoint_url http://crapi-identity:8080/identity/api/v2/user/videos/convert_video","status":403}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `22.74 ms`, response-size signal `0.332`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 8. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/user/videos/{video_id}`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000013`
- Signature: `4e6af6bfc5ba`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `16.52 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 9. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /identity/api/v2/user/videos/{video_id}`
- HTTP status: `404`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000169`
- Signature: `a4de086a8fca`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `{"message":"Video not found.","status":404}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `31.62 ms`, response-size signal `0.08398`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 10. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/vehicle/vehicles`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000023`
- Signature: `919756d0f38d`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `11.97 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 11. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/vehicle/{vehicleId}/location`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000027`
- Signature: `ac05ec727f6a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `15.48 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 12. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/management/users/all`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000062`
- Signature: `5d5844ed7ae0`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `30.54 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 13. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/management/users/all`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000061`
- Signature: `e6b4bcca3d9c`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `12.84 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 14. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000064`
- Signature: `848cc5303fd5`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `30.22 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 15. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000063`
- Signature: `befbb5ed1622`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `7.251 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 16. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000316`
- Signature: `03bfd9b59fe1`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `null`
- Response excerpt: `{"message":"The Report does not exist for given report_id."}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `37.59 ms`, response-size signal `0.1172`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 17. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000068`
- Signature: `27b2f9948ed9`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `17.22 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 18. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000067`
- Signature: `4eda42523a12`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `8.076 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 19. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/all`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000054`
- Signature: `2168443d0113`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `21.84 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 20. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/all`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000053`
- Signature: `9c02eb135aa7`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `14.02 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 21. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/{order_id}`
- HTTP status: `404`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000051`
- Signature: `dc28169b5139`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Not Found</title>\n</head>\n<body>\n  <h1>Not Found</h1><p>The requested resource was not found on this server.</p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `13.12 ms`, response-size signal `0.3496`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 22. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/products`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000043`
- Signature: `2a346a4f2f40`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `4.75 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 23. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/products`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000044`
- Signature: `7c33c5fc3112`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `45.59 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 24. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/shop/return_qr_code`
- HTTP status: `406`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000285`
- Signature: `9ad2c2d75064`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 406.
- Request payload: `null`
- Response excerpt: `{"detail":"Could not satisfy the request Accept header."}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `3.184 ms`, response-size signal `0.1113`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 25. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/community/posts`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000033`
- Signature: `9413a55de5cc`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"content":"A","title":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `18.83 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 26. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/community/posts/{postId}/comment`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000035`
- Signature: `75368ec5200e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"content":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `18.25 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 27. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/coupon/new-coupon`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000039`
- Signature: `ffadb067d9aa`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"amount":"A","coupon_code":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `17.22 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 28. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/coupon/validate-coupon`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000041`
- Signature: `f244e5300b9d`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"coupon_code":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `16.65 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 29. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/auth/forget-password`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000033`
- Signature: `da59aaa7f96f`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"email":"A"}`
- Response excerpt: `{"details":"org.springframework.validation.BeanPropertyBindingResult: 2 errors\nField error in object 'forgetPassword' on field 'email': rejected value [A]; codes [Size.forgetPassword.email,Size.email,Size.java.lang.String,Size]; arguments [org.springframework.context.support.DefaultMessageSourceResolvable: codes [forgetPassword.email,email]; arguments []; default message [email],100,3]; default message [size must be between 3 and 100]\nField error in object 'forgetPassword' on field 'email': rejected value [A]; codes [Email.forgetPassword.email,Email.email,Email.java.lang.String,Email]; argu…`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `22.96 ms`, response-size signal `1.746`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=large (0.75)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 30. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/auth/login`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000022`
- Signature: `8ec0bbc8fa25`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"email":"A","password":"<REDACTED>"}`
- Response excerpt: `{"details":"org.springframework.validation.BeanPropertyBindingResult: 2 errors\nField error in object 'loginForm' on field 'password': rejected value [A]; codes [Size.loginForm.password,Size.password,Size.java.lang.String,Size]; arguments [org.springframework.context.support.DefaultMessageSourceResolvable: codes [loginForm.password,password]; arguments []; default message [password],100,4]; default message [size must be between 4 and 100]\nField error in object 'loginForm' on field 'email': rejected value [A]; codes [Size.loginForm.email,Size.email,Size.java.lang.String,Size]; arguments [org.…`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `20.51 ms`, response-size signal `1.602`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=large (0.60)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 31. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/signup`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `case-000001`
- Signature: `4b0a073a7da0`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"email":"A","name":"A","number":"A","password":"<REDACTED>"}`
- Response excerpt: `{"details":"org.springframework.validation.BeanPropertyBindingResult: 3 errors\nField error in object 'signUpForm' on field 'name': rejected value [A]; codes [Size.signUpForm.name,Size.name,Size.java.lang.String,Size]; arguments [org.springframework.context.support.DefaultMessageSourceResolvable: codes [signUpForm.name,name]; arguments []; default message [name],100,3]; default message [size must be between 3 and 100]\nField error in object 'signUpForm' on field 'email': rejected value [A]; codes [Email.signUpForm.email,Email.email,Email.java.lang.String,Email]; arguments [org.springframework…`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `26.44 ms`, response-size signal `2.404`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=large (0.60)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 32. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/change-email`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000003`
- Signature: `04e7d32d5cd8`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"new_email":"A","old_email":"A"}`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `12.73 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 33. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/user/change-email`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000136`
- Signature: `dd512b73e989`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"new_email":"A","old_email":"A"}`
- Response excerpt: `{"details":"org.springframework.validation.BeanPropertyBindingResult: 2 errors\nField error in object 'changeEmailForm' on field 'new_email': rejected value [A]; codes [Size.changeEmailForm.new_email,Size.new_email,Size.java.lang.String,Size]; arguments [org.springframework.context.support.DefaultMessageSourceResolvable: codes [changeEmailForm.new_email,new_email]; arguments []; default message [new_email],40,3]; default message [size must be between 3 and 40]\nField error in object 'changeEmailForm' on field 'old_email': rejected value [A]; codes [Size.changeEmailForm.old_email,Size.old_emai…`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `28.95 ms`, response-size signal `1.723`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=large (0.72)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 34. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/pictures`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000009`
- Signature: `cf110626d915`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `11.93 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity

### 35. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/reset-password`
- HTTP status: `401`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000001`
- Signature: `4e738fc5c5e7`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"email":"A","password":"<REDACTED>"}`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v2`
- FIS inputs: status deviation `0.6`, response time `9.276 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R2_MEDIUM_DEVIATION` (strength `0.6667`) — medium status deviation -> medium severity
