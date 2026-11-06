# Deduplication report

API: `crapi`

## Summary

- Planned requests: 285
- Executed requests: 285 (100.0%)
- Classified observations: 270
- Expected failures: 31
- Raw candidate findings: 239
- Unique operational findings: 161
- Deduplication reduction: 32.6%
- Candidate endpoints: 41
- FIS rationale coverage: 161/161 unique findings
- FIS fallbacks among unique findings: 75

`EXPECTED_FAILURE` remains an execution metric and is excluded before deduplication. A unique operational finding is a strict black-box signature, not a confirmed bug, vulnerability, or root cause.

## Findings by execution level

A signature may involve more than one level, so the final column can overlap across rows.

| Level | Case mix | Planned | Executed | Classified | Raw candidates | Unique signatures involved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | `auth_probe=70, baseline=44` | 114 | 114 | 100 | 92 | 69 |
| L1 | `mutation=171` | 171 | 171 | 170 | 147 | 101 |

## Candidate classifications

| Classification | Raw | Unique |
| --- | ---: | ---: |
| `ERROR_CONTRADICTION` | 29 | 27 |
| `SERVER_ERROR` | 68 | 24 |
| `SUCCESS_CONTRADICTION` | 3 | 2 |
| `UNEXPECTED_ERROR_STATUS` | 129 | 101 |
| `UNEXPECTED_SUCCESS` | 10 | 7 |

## Endpoints with unique findings

- `POST /identity/api/auth/signup`: 11
- `POST /workshop/api/shop/orders`: 9
- `POST /workshop/api/mechanic/signup`: 8
- `POST /identity/api/v2/vehicle/add_vehicle`: 8
- `POST /workshop/api/merchant/contact_mechanic`: 8
- `POST /identity/api/v2/user/change-email`: 8
- `POST /workshop/api/shop/apply_coupon`: 8
- `POST /identity/api/auth/login`: 7
- `POST /identity/api/auth/v2.7/user/login-with-token`: 7
- `POST /identity/api/auth/v2/check-otp`: 6

## Potentially actionable findings

Showing 50 of 161 unique findings. The complete machine-readable set is available in `findings_unique.json`.

### 1. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/mechanic/receive_report`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000199`
- Signature: `79d30d2bb959`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `46.21 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 2. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/shop/orders/{order_id}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000169`
- Signature: `8b97701e8e5d`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `46.26 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 3. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /community/api/v2/community/posts/{postId}/comment`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000129`
- Signature: `bddcd8d379f4`
- Input strategy: `empty_object` on `/` (unspecified)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `{"error":"mongo: no documents in result"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `8.867 ms`, response-size signal `0.08203`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 4. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v2.7/user/login-with-token`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `5`
- Representative case: `case-000070`
- Signature: `474766f33cd9`
- Input strategy: `wrong_type` on `/email` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":123,"token":"<REDACTED>"}`
- Response excerpt: `{"message":"Invalid Credentials","mfaRequired":false,"token":"<REDACTED>","type":""}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `14.59 ms`, response-size signal `0.1484`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 5. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v2/check-otp`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `9`
- Representative case: `case-000044`
- Signature: `07ec293b0660`
- Input strategy: `remove_required_property` on `/password` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":"AAAAA","otp":"AAA"}`
- Response excerpt: `"User was not found for parameters {userEmail=AAAAA}"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `16.66 ms`, response-size signal `0.0498`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 6. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v3/check-otp`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `9`
- Representative case: `case-000029`
- Signature: `183ed38ac8a8`
- Input strategy: `remove_required_property` on `/password` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":"AAAAA","otp":"AAA"}`
- Response excerpt: `"User was not found for parameters {userEmail=AAAAA}"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `11.17 ms`, response-size signal `0.0498`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 7. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/user/pictures`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000098`
- Signature: `de62037ba8a9`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"Current request is not a multipart request"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `21.28 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 8. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/v2/user/verify-email-token`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `8`
- Representative case: `case-000090`
- Signature: `8b675c6e4976`
- Input strategy: `empty_object` on `/` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `{"message":"Sorry, Token did't match","status":500}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `32.52 ms`, response-size signal `0.09961`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 9. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/user/videos`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000099`
- Signature: `8b6f6fa85814`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"Current request is not a multipart request"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `18.13 ms`, response-size signal `0.04102`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 10. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /workshop/api/merchant/contact_mechanic`
- HTTP status: `503`
- Score: `0.84`
- Occurrences in this run: `8`
- Representative case: `case-000188`
- Signature: `01c248ce0771`
- Input strategy: `remove_required_property` on `/problem_details` (required)
- Interpretation: Server returned a 503 error.
- Request payload: `{"mechanic_api":"A","mechanic_code":"A","number_of_repeats":0.0,"repeat_request_if_failed":true,"vin":"A"}`
- Response excerpt: `{"message":" 'number_of_repeats' should be between 1 and 100."}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `49.7 ms`, response-size signal `0.06152`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 11. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /workshop/api/shop/apply_coupon`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `2`
- Representative case: `case-000172`
- Signature: `619733d8b18d`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"amount":0,"coupon_code":"A"}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `137.5 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 12. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /workshop/api/shop/orders`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000155`
- Signature: `ec34e1415a26`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"product_id":0,"quantity":0}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `69.64 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 13. HIGH · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /workshop/api/shop/orders/return_order`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `1`
- Representative case: `case-000171`
- Signature: `57d0d6cc793e`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `57.05 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

### 14. HIGH · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /workshop/api/shop/orders/{order_id}`
- HTTP status: `500`
- Score: `0.84`
- Occurrences in this run: `7`
- Representative case: `case-000164`
- Signature: `8b2e5a1f7e6f`
- Input strategy: `empty_object` on `/` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `1`, response time `53.47 ms`, response-size signal `0.2832`
- Dominant fuzzy terms: status_deviation=high (1.00); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- Strongest activated rule: `R1_HIGH_DEVIATION_OR_TIMEOUT` (strength `1.0`) — high status deviation or timeout response -> high severity

## Contract fidelity observations


### 1. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /identity/api/v2/admin/videos/{video_id}`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000021`
- Signature: `4725dbc318b6`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `17.52 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 2. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /identity/api/v2/user/videos/{video_id}`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000017`
- Signature: `b4eeb4c69c37`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `8.457 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 3. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /community/api/v2/community/posts/recent`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000037`
- Signature: `7c4f9f216eae`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `17.23 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 4. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /community/api/v2/community/posts/{postId}`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000031`
- Signature: `55d0f69f4361`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `43.03 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 5. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /community/api/v2/community/posts/{postId}`
- HTTP status: `400`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `case-000121`
- Signature: `8160209d882e`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `null`
- Response excerpt: `"{\"error\":\"mongo: no documents in result\"}\n{\"id\":\"\",\"title\":\"\",\"content\":\"\",\"author\":{\"nickname\":\"\",\"email\":\"\",\"vehicleid\":\"\",\"profile_pic_url\":\"\",\"created_at\":\"0001-01-01T00:00:00Z\"},\"comments\":null,\"authorid\":0,\"CreatedAt\":\"0001-01-01T00:00:00Z\"}\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `13.1 ms`, response-size signal `0.4844`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 6. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/user/videos/convert_video`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000019`
- Signature: `2daff72deff3`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `7.731 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 7. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /identity/api/v2/user/videos/convert_video`
- HTTP status: `403`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `case-000109`
- Signature: `6c6a202510bf`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"message":"Thi-S endpoint S-hould be accessed only inte-Rnally. -Fine? , endpoint_url http://crapi-identity:8080/identity/api/v2/user/videos/convert_video","status":403}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `31.43 ms`, response-size signal `0.332`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 8. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/user/videos/{video_id}`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000013`
- Signature: `4e6af6bfc5ba`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `13.85 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 9. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /identity/api/v2/user/videos/{video_id}`
- HTTP status: `404`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `case-000100`
- Signature: `a4de086a8fca`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `{"message":"Video not found.","status":404}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `29.5 ms`, response-size signal `0.08398`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 10. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/vehicle/vehicles`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000023`
- Signature: `919756d0f38d`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `9.251 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 11. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/vehicle/{vehicleId}/location`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000027`
- Signature: `ac05ec727f6a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `12.35 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 12. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/management/users/all`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000062`
- Signature: `5d5844ed7ae0`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `26.47 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 13. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/management/users/all`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000061`
- Signature: `e6b4bcca3d9c`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `12.05 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 14. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000064`
- Signature: `848cc5303fd5`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `26.4 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 15. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000063`
- Signature: `befbb5ed1622`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `10.63 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 16. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `400`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `case-000200`
- Signature: `03bfd9b59fe1`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `null`
- Response excerpt: `{"message":"The Report does not exist for given report_id."}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `43.45 ms`, response-size signal `0.1172`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 17. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000068`
- Signature: `27b2f9948ed9`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `25.85 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 18. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000067`
- Signature: `4eda42523a12`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `12 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 19. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/all`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000054`
- Signature: `2168443d0113`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `24.02 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 20. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/all`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000053`
- Signature: `9c02eb135aa7`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `10.77 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 21. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/{order_id}`
- HTTP status: `404`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000051`
- Signature: `dc28169b5139`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Not Found</title>\n</head>\n<body>\n  <h1>Not Found</h1><p>The requested resource was not found on this server.</p>\n</body>\n</html>\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `11.77 ms`, response-size signal `0.3496`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 22. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/products`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000043`
- Signature: `2a346a4f2f40`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `10.4 ms`, response-size signal `0.06445`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 23. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/products`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000044`
- Signature: `7c33c5fc3112`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `30.52 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 24. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/shop/return_qr_code`
- HTTP status: `406`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `case-000179`
- Signature: `9ad2c2d75064`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 406.
- Request payload: `null`
- Response excerpt: `{"detail":"Could not satisfy the request Accept header."}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `8.802 ms`, response-size signal `0.1113`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 25. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/community/posts`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000033`
- Signature: `9413a55de5cc`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"content":"A","title":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `15.41 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 26. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/community/posts/{postId}/comment`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000035`
- Signature: `75368ec5200e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"content":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `13.94 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 27. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/coupon/new-coupon`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000039`
- Signature: `ffadb067d9aa`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"amount":"A","coupon_code":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `19.38 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 28. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/coupon/validate-coupon`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000041`
- Signature: `f244e5300b9d`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"coupon_code":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `16.86 ms`, response-size signal `0.04883`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 29. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/change-email`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000003`
- Signature: `04e7d32d5cd8`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"new_email":"A","old_email":"A"}`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `12.95 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 30. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/pictures`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000009`
- Signature: `cf110626d915`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `10.49 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 31. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/reset-password`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000001`
- Signature: `4e738fc5c5e7`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"email":"A","password":"<REDACTED>"}`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `8.79 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 32. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/verify-email-token`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000005`
- Signature: `81c3eade13a5`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"new_email":"A","old_email":"A","token":"<REDACTED>"}`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `12.62 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 33. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/videos`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000011`
- Signature: `50abc3fa4a4e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `11.01 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 34. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/vehicle/add_vehicle`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000025`
- Signature: `72b2117a1ec7`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"pincode":"A","vin":"A"}`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `9.617 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 35. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/vehicle/resend_email`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000029`
- Signature: `1f317eb50e4e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `10.38 ms`, response-size signal `0.0957`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used

### 36. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /workshop/api/merchant/contact_mechanic`
- HTTP status: `401`
- Score: `0.6`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000066`
- Signature: `65b09a1fc252`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"mechanic_api":"A","mechanic_code":"A","number_of_repeats":0.0,"problem_details":"A","repeat_request_if_failed":true,"vin":"A"}`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-status-time-response-size-v1`
- FIS inputs: status deviation `0.6`, response time `26.3 ms`, response-size signal `0.0625`
- Dominant fuzzy terms: status_deviation=medium (0.67); response_time_ms=normal (1.00); response_size_signal=expected (1.00)
- FIS fallback: crisp status deviation was used
