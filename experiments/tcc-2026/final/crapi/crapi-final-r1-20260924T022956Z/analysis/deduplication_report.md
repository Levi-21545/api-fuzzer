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

- `POST /identity/api/auth/signup`: 21
- `POST /workshop/api/mechanic/signup`: 15
- `POST /identity/api/v2/vehicle/add_vehicle`: 12
- `POST /workshop/api/shop/orders`: 12
- `POST /identity/api/v2/user/change-email`: 11
- `POST /identity/api/auth/login`: 11
- `POST /workshop/api/merchant/contact_mechanic`: 10
- `POST /workshop/api/shop/apply_coupon`: 9
- `POST /identity/api/auth/v2.7/user/login-with-token`: 9
- `POST /identity/api/auth/v2/check-otp`: 6

## Potentially actionable findings

Showing 50 of 198 unique findings. The complete machine-readable set is available in `findings_unique.json`.

### 1. HIGH · UNEXPECTED_SUCCESS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/return_qr_code`
- HTTP status: `200`
- Score: `0.73`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000059`
- Signature: `95b2167d7099`
- Input strategy: authentication probe with no valid credentials
- Interpretation: Authentication probe was accepted with status 200; the request used no valid credentials.
- Request payload: `null`
- Response excerpt: `"�PNG\r\n\u001a\n\u0000\u0000\u0000\rIHDR\u0000\u0000\u0004�\u0000\u0000\u0004�\b\u0002\u0000\u0000\u0000�Nc�\u0000\u0000\u0000\u0006bKGD\u0000�\u0000�\u0000�����\u0000\u0000\u001b�IDATx��ف��8\u0012\u0000����w�΁�b�͜\u0016#\u001cPI\"5�����\u0000\u0000\u0000��o=\u0000\u0000\u0000��\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000Ą\u0019\u0000\u0000@L�\u0001\u0000\u0000…`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.7`, evidence strength `0.5`, access-control exposure `1`
- Dominant fuzzy terms: behavior_contradiction=medium (0.40); evidence_strength=limited (0.67); access_control_exposure=clear (1.00)
- Strongest activated rule: `R6_CLEAR_ACCESS_EXPOSURE` (strength `1.0`) — clear access-control exposure -> high priority

### 2. MEDIUM · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/mechanic/receive_report`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000315`
- Signature: `79d30d2bb959`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 3. MEDIUM · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/shop/orders/{order_id}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000271`
- Signature: `8b97701e8e5d`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 4. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /community/api/v2/community/posts/{postId}/comment`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `case-000209`
- Signature: `bddcd8d379f4`
- Input strategy: `empty_object` on `/` (unspecified)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `{"error":"mongo: no documents in result"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 5. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v2.7/user/login-with-token`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `8`
- Representative case: `case-000114`
- Signature: `474766f33cd9`
- Input strategy: `wrong_type` on `/email` (type)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":123,"token":"<REDACTED>"}`
- Response excerpt: `{"message":"Invalid Credentials","mfaRequired":false,"token":"<REDACTED>","type":""}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 6. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v2/check-otp`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `15`
- Representative case: `case-000068`
- Signature: `07ec293b0660`
- Input strategy: `remove_required_property` on `/password` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":"AAAAA","otp":"AAA"}`
- Response excerpt: `"User was not found for parameters {userEmail=AAAAA}"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 7. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/auth/v3/check-otp`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `15`
- Representative case: `case-000043`
- Signature: `183ed38ac8a8`
- Input strategy: `remove_required_property` on `/password` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{"email":"AAAAA","otp":"AAA"}`
- Response excerpt: `"User was not found for parameters {userEmail=AAAAA}"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 8. MEDIUM · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/user/pictures`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000167`
- Signature: `de62037ba8a9`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"Current request is not a multipart request"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 9. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /identity/api/v2/user/verify-email-token`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `18`
- Representative case: `case-000149`
- Signature: `8b675c6e4976`
- Input strategy: `empty_object` on `/` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `{"message":"Sorry, Token did't match","status":500}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 10. MEDIUM · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/user/videos`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000168`
- Signature: `8b6f6fa85814`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"Current request is not a multipart request"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 11. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /workshop/api/merchant/contact_mechanic`
- HTTP status: `503`
- Score: `0.5`
- Occurrences in this run: `9`
- Representative case: `case-000307`
- Signature: `01c248ce0771`
- Input strategy: `remove_required_property` on `/problem_details` (required); `remove_required_property` on `/vin` (required)
- Interpretation: Server returned a 503 error.
- Request payload: `{"mechanic_api":"A","mechanic_code":"A","number_of_repeats":0.0,"repeat_request_if_failed":true}`
- Response excerpt: `{"message":" 'number_of_repeats' should be between 1 and 100."}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 12. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1`
- Case kind(s): `baseline, mutation`
- Endpoint: `POST /workshop/api/shop/apply_coupon`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `2`
- Representative case: `case-000274`
- Signature: `619733d8b18d`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"amount":0,"coupon_code":"A"}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 13. MEDIUM · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /workshop/api/shop/orders`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000249`
- Signature: `ec34e1415a26`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `{"product_id":0,"quantity":0}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 14. MEDIUM · SERVER_ERROR

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /workshop/api/shop/orders/return_order`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000273`
- Signature: `57d0d6cc793e`
- Input strategy: baseline request
- Interpretation: Server returned a 500 error.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

### 15. MEDIUM · SERVER_ERROR

- Execution level(s): `L0, L1, L2`
- Case kind(s): `baseline, mutation`
- Endpoint: `PUT /workshop/api/shop/orders/{order_id}`
- HTTP status: `500`
- Score: `0.5`
- Occurrences in this run: `11`
- Representative case: `case-000262`
- Signature: `8b2e5a1f7e6f`
- Input strategy: `empty_object` on `/` (required)
- Interpretation: Server returned a 500 error.
- Request payload: `{}`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Server Error (500)</title>\n</head>\n<body>\n  <h1>Server Error (500)</h1><p></p>\n</body>\n</html>\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `1`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=high (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R3_HIGH_CONTRADICTION_WEAK_EVIDENCE` (strength `0.6667`) — high contradiction with limited evidence -> medium priority

## Contract fidelity observations


### 1. MEDIUM · SUCCESS_CONTRADICTION

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /community/api/v2/community/posts/recent`
- HTTP status: `200`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000211`
- Signature: `56550db051b2`
- Input strategy: baseline request
- Interpretation: Response body for 200 does not match the contract. Details: {'posts': [{'id': 'LcJRNMr7sf34GV43pzc8uK', 'title': '', 'content': '', 'author': {'nickname': 'progrrnj', 'email': 'progrrnj@fuzzer.com', 'vehicleid': '', 'profile_pic_url': '', 'created_at': '2026-09-24T02:33:21.903Z'}, 'comments': [], 'authorid': 8, 'CreatedAt': '2026-09-24T02:33:21.903Z'}, {'id': '9dnxT4z59V8ookqsHTTyu4', 'title': 'A', 'content': 'A', 'author': {'nickname': 'progrrnj', 'email': 'progrrnj@fuzzer.com', 'vehicleid': '', 'profile_pic_url': '', 'created_at': '2026-09-24T02:33:21.307Z'}, 'comments': [], 'authorid': 8, 'CreatedAt': '2026-09-24T02:33:21.307Z'}, {'id': 'uWJBaDhAyDewvGdae8D6sk', 'title': 'Title 3', 'content': 'Hello world 3', 'author': {'nickname': 'Robot', 'email': 'robot001@example.com', 'vehicleid': '4bae9968-ec7f-4de3-a3a0-ba1b2ab5e5e5', 'profile_pic_url': '', 'created_at': '2026-09-24T02:31:26.424Z'}, 'comments': [], 'authorid': 3, 'CreatedAt': '2026-09-24T02:31:26.424Z'}, {'id': 'fwTgWbDAnEXdtNaxJroCNo', 'title': 'Title 2', 'content': 'Hello world 2', 'author': {'nickname': 'Pogba', 'email': 'pogba006@example.com', 'vehicleid': 'cd515c12-0fc1-48ae-8b61-9230b70a845b', 'profile_pic_url': '', 'created_at': '2026-09-24T02:31:26.423Z'}, 'comments': [], 'authorid': 2, 'CreatedAt': '2026-09-24T02:31:26.423Z'}, {'id': '6r3FA6Lz3Vu6XkUfbM6dHE', 'title': 'Title 1', 'content': 'Hello world 1', 'author': {'nickname': 'Adam', 'email': 'adam007@example.com', 'vehicleid': 'f89b5f21-7829-45cb-a650-299a61090378', 'profile_pic_url': '', 'created_at': '2026-09-24T02:31:26.407Z'}, 'comments': [], 'authorid': 1, 'CreatedAt': '2026-09-24T02:31:26.407Z'}], 'next_offset': 0, 'previous_offset': 0, 'total': 5} is not of type 'array'
- Request payload: `null`
- Response excerpt: `{"next_offset":0,"posts":[{"CreatedAt":"2026-09-24T02:33:21.903Z","author":{"created_at":"2026-09-24T02:33:21.903Z","email":"progrrnj@fuzzer.com","nickname":"progrrnj","profile_pic_url":"","vehicleid":""},"authorid":8,"comments":[],"content":"","id":"LcJRNMr7sf34GV43pzc8uK","title":""},{"CreatedAt":"2026-09-24T02:33:21.307Z","author":{"created_at":"2026-09-24T02:33:21.307Z","email":"progrrnj@fuzzer.com","nickname":"progrrnj","profile_pic_url":"","vehicleid":""},"authorid":8,"comments":[],"content":"A","id":"9dnxT4z59V8ookqsHTTyu4","title":"A"},{"CreatedAt":"2026-09-24T02:31:26.424Z","author":…`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.65`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.60); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.6`) — medium behavioral contradiction -> medium priority

### 2. MEDIUM · UNEXPECTED_ERROR_STATUS

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
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 3. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/auth/login`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000022`
- Signature: `3964f3d72e25`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"email":"A","password":"<REDACTED>"}`
- Response excerpt: `{"details":"org.springframework.validation.BeanPropertyBindingResult: 2 errors\nField error in object 'loginForm' on field 'email': rejected value [A]; codes [Size.loginForm.email,Size.email,Size.java.lang.String,Size]; arguments [org.springframework.context.support.DefaultMessageSourceResolvable: codes [loginForm.email,email]; arguments []; default message [email],100,3]; default message [size must be between 3 and 100]\nField error in object 'loginForm' on field 'password': rejected value [A]; codes [Size.loginForm.password,Size.password,Size.java.lang.String,Size]; arguments [org.springfra…`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 4. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/auth/signup`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000001`
- Signature: `4b0a073a7da0`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"email":"A","name":"A","number":"A","password":"<REDACTED>"}`
- Response excerpt: `{"details":"org.springframework.validation.BeanPropertyBindingResult: 3 errors\nField error in object 'signUpForm' on field 'name': rejected value [A]; codes [Size.signUpForm.name,Size.name,Size.java.lang.String,Size]; arguments [org.springframework.context.support.DefaultMessageSourceResolvable: codes [signUpForm.name,name]; arguments []; default message [name],100,3]; default message [size must be between 3 and 100]\nField error in object 'signUpForm' on field 'email': rejected value [A]; codes [Email.signUpForm.email,Email.email,Email.java.lang.String,Email]; arguments [org.springframework…`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 5. MEDIUM · UNEXPECTED_ERROR_STATUS

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
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 6. MEDIUM · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `POST /identity/api/v2/vehicle/add_vehicle`
- HTTP status: `400`
- Score: `0.5`
- Occurrences in this run: `1`
- Representative case: `case-000187`
- Signature: `28a1a9f9a4dc`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `{"pincode":"A","vin":"A"}`
- Response excerpt: `{"details":"org.springframework.validation.BeanPropertyBindingResult: 2 errors\nField error in object 'vehicleForm' on field 'pincode': rejected value [A]; codes [Size.vehicleForm.pincode,Size.pincode,Size.java.lang.String,Size]; arguments [org.springframework.context.support.DefaultMessageSourceResolvable: codes [vehicleForm.pincode,pincode]; arguments []; default message [pincode],8,4]; default message [size must be between 4 and 8]\nField error in object 'vehicleForm' on field 'vin': rejected value [A]; codes [Size.vehicleForm.vin,Size.vin,Size.java.lang.String,Size]; arguments [org.spring…`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.6`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=medium (0.80); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R2_MEDIUM_CONTRADICTION` (strength `0.8`) — medium behavioral contradiction -> medium priority

### 7. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /identity/api/v2/admin/videos/{video_id}`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000021`
- Signature: `4725dbc318b6`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 8. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `DELETE /identity/api/v2/user/videos/{video_id}`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000017`
- Signature: `b4eeb4c69c37`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 9. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /community/api/v2/community/posts/recent`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000037`
- Signature: `7c4f9f216eae`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 10. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /community/api/v2/community/posts/{postId}`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000031`
- Signature: `55d0f69f4361`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 11. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /community/api/v2/community/posts/{postId}`
- HTTP status: `400`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000200`
- Signature: `8160209d882e`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `null`
- Response excerpt: `"{\"error\":\"mongo: no documents in result\"}\n{\"id\":\"\",\"title\":\"\",\"content\":\"\",\"author\":{\"nickname\":\"\",\"email\":\"\",\"vehicleid\":\"\",\"profile_pic_url\":\"\",\"created_at\":\"0001-01-01T00:00:00Z\"},\"comments\":null,\"authorid\":0,\"CreatedAt\":\"0001-01-01T00:00:00Z\"}\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 12. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/user/videos/convert_video`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000019`
- Signature: `2daff72deff3`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 13. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /identity/api/v2/user/videos/convert_video`
- HTTP status: `403`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000184`
- Signature: `6c6a202510bf`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 403.
- Request payload: `null`
- Response excerpt: `{"message":"Thi-S endpoint S-hould be accessed only inte-Rnally. -Fine? , endpoint_url http://crapi-identity:8080/identity/api/v2/user/videos/convert_video","status":403}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 14. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/user/videos/{video_id}`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000013`
- Signature: `4e6af6bfc5ba`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 15. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /identity/api/v2/user/videos/{video_id}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000169`
- Signature: `a4de086a8fca`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `{"message":"Video not found.","status":404}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 16. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/vehicle/vehicles`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000023`
- Signature: `919756d0f38d`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 17. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /identity/api/v2/vehicle/{vehicleId}/location`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000027`
- Signature: `ac05ec727f6a`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 18. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/management/users/all`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000062`
- Signature: `5d5844ed7ae0`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 19. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/management/users/all`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000061`
- Signature: `e6b4bcca3d9c`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 20. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000064`
- Signature: `848cc5303fd5`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 21. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000063`
- Signature: `befbb5ed1622`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 22. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `400`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000316`
- Signature: `03bfd9b59fe1`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 400.
- Request payload: `null`
- Response excerpt: `{"message":"The Report does not exist for given report_id."}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 23. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000068`
- Signature: `27b2f9948ed9`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 24. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/mechanic/mechanic_report`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000067`
- Signature: `4eda42523a12`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 25. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/all`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000054`
- Signature: `2168443d0113`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 26. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/all`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000053`
- Signature: `9c02eb135aa7`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 27. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/orders/{order_id}`
- HTTP status: `404`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000051`
- Signature: `dc28169b5139`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 404.
- Request payload: `null`
- Response excerpt: `"\n<!doctype html>\n<html lang=\"en\">\n<head>\n  <title>Not Found</title>\n</head>\n<body>\n  <h1>Not Found</h1><p>The requested resource was not found on this server.</p>\n</body>\n</html>\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 28. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/products`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000043`
- Signature: `2a346a4f2f40`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"JWT Token required!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 29. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `GET /workshop/api/shop/products`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `auth-probe-000044`
- Signature: `7c33c5fc3112`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `null`
- Response excerpt: `{"message":"Invalid JWT Token!"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 30. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `baseline`
- Endpoint: `GET /workshop/api/shop/return_qr_code`
- HTTP status: `406`
- Score: `0.16`
- Occurrences in this run: `1`
- Representative case: `case-000285`
- Signature: `9ad2c2d75064`
- Input strategy: baseline request
- Interpretation: API returned an undocumented error status code: 406.
- Request payload: `null`
- Response excerpt: `{"detail":"Could not satisfy the request Accept header."}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.2`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 31. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/community/posts`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000033`
- Signature: `9413a55de5cc`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"content":"A","title":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 32. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/community/posts/{postId}/comment`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000035`
- Signature: `75368ec5200e`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"content":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 33. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/coupon/new-coupon`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000039`
- Signature: `ffadb067d9aa`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"amount":"A","coupon_code":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 34. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /community/api/v2/coupon/validate-coupon`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000041`
- Signature: `f244e5300b9d`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"coupon_code":"A"}`
- Response excerpt: `{"error":"Unauthorized"}`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority

### 35. LOW · UNEXPECTED_ERROR_STATUS

- Execution level(s): `L0`
- Case kind(s): `auth_probe`
- Endpoint: `POST /identity/api/v2/user/change-email`
- HTTP status: `401`
- Score: `0.16`
- Occurrences in this run: `2`
- Representative case: `auth-probe-000003`
- Signature: `04e7d32d5cd8`
- Input strategy: authentication probe with no valid credentials
- Interpretation: API returned an undocumented error status code: 401.
- Request payload: `{"new_email":"A","old_email":"A"}`
- Response excerpt: `"CRAPIResponse(message=Invalid Token, status=401)\n"`
- FIS model: `mamdani-behavior-evidence-access-v3`
- FIS inputs: behavior contradiction `0.15`, evidence strength `0.5`, access-control exposure `0`
- Dominant fuzzy terms: behavior_contradiction=low (1.00); evidence_strength=limited (0.67); access_control_exposure=none (1.00)
- Strongest activated rule: `R1_LOW_CONTRADICTION` (strength `1.0`) — low behavioral contradiction -> low priority
