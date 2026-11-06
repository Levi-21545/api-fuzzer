# Relatório de Análise

Total de resultados classificados: 270

## Por classificação
- UNEXPECTED_ERROR_STATUS: 129
- SERVER_ERROR: 68
- EXPECTED_FAILURE: 31
- ERROR_CONTRADICTION: 29
- UNEXPECTED_SUCCESS: 10
- SUCCESS_CONTRADICTION: 3

## Por severidade
- HIGH: 68
- MEDIUM: 130
- LOW: 72

## Endpoints com mais achados (top 10)
- POST /workshop/api/merchant/contact_mechanic: 19
- POST /identity/api/auth/v3/check-otp: 15
- POST /identity/api/auth/v2/check-otp: 15
- POST /workshop/api/mechanic/signup: 13
- POST /identity/api/v2/user/verify-email-token: 11
- POST /workshop/api/shop/products: 11
- POST /identity/api/auth/signup: 11
- POST /identity/api/auth/v4.0/user/login-with-token: 11
- POST /identity/api/auth/v2.7/user/login-with-token: 11
- POST /identity/api/v2/user/change-email: 9

## Amostras por classificação (até 50 cada)

### UNEXPECTED_ERROR_STATUS
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/reset-password → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/reset-password → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/change-email → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/change-email → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/verify-email-token → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/verify-email-token → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/pictures → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/pictures → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/videos → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/user/videos → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/user/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/user/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] PUT /identity/api/v2/user/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] PUT /identity/api/v2/user/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] DELETE /identity/api/v2/user/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] DELETE /identity/api/v2/user/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/user/videos/convert_video → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/user/videos/convert_video → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] DELETE /identity/api/v2/admin/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] DELETE /identity/api/v2/admin/videos/{video_id} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/vehicle/vehicles → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/vehicle/vehicles → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/vehicle/add_vehicle → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/vehicle/add_vehicle → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/vehicle/{vehicleId}/location → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /identity/api/v2/vehicle/{vehicleId}/location → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/vehicle/resend_email → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /identity/api/v2/vehicle/resend_email → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /community/api/v2/community/posts/{postId} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /community/api/v2/community/posts/{postId} → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/community/posts → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/community/posts → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/community/posts/{postId}/comment → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/community/posts/{postId}/comment → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /community/api/v2/community/posts/recent → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /community/api/v2/community/posts/recent → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/coupon/new-coupon → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/coupon/new-coupon → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/coupon/validate-coupon → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /community/api/v2/coupon/validate-coupon → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /workshop/api/shop/products → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] GET /workshop/api/shop/products → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /workshop/api/shop/products → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /workshop/api/shop/products → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /workshop/api/shop/orders → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] POST /workshop/api/shop/orders → 401 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 401.
- [UNEXPECTED_ERROR_STATUS] PUT /workshop/api/shop/orders/{order_id} → 404 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 404.
- [UNEXPECTED_ERROR_STATUS] PUT /workshop/api/shop/orders/{order_id} → 404 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 404.
- [UNEXPECTED_ERROR_STATUS] GET /workshop/api/shop/orders/{order_id} → 404 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 404.
- [UNEXPECTED_ERROR_STATUS] GET /workshop/api/shop/orders/{order_id} → 404 — score=0.6 severity=MEDIUM — API returned an undocumented error status code: 404.

### SERVER_ERROR
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v3/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2/check-otp → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2.7/user/login-with-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2.7/user/login-with-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2.7/user/login-with-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2.7/user/login-with-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/auth/v2.7/user/login-with-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/reset-password → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/verify-email-token → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/pictures → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /identity/api/v2/user/videos → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /community/api/v2/community/posts/{postId}/comment → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /community/api/v2/community/posts/{postId}/comment → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /community/api/v2/coupon/validate-coupon → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] POST /workshop/api/shop/orders → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /workshop/api/shop/orders/{order_id} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.
- [SERVER_ERROR] PUT /workshop/api/shop/orders/{order_id} → 500 — score=0.84 severity=HIGH — Server returned a 500 error.

### EXPECTED_FAILURE
- [EXPECTED_FAILURE] GET /identity/api/v2/user/dashboard → 404 — score=0.31 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] GET /identity/api/v2/user/dashboard → 404 — score=0.31 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] GET /workshop/api/mechanic/service_requests → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] GET /workshop/api/mechanic/service_requests → 401 — score=0.31 severity=LOW — API correctly rejected with documented 401 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 403 — score=0.28 severity=LOW — API correctly rejected with documented 403 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 400 — score=0.29 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 403 — score=0.28 severity=LOW — API correctly rejected with documented 403 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 403 — score=0.28 severity=LOW — API correctly rejected with documented 403 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 403 — score=0.28 severity=LOW — API correctly rejected with documented 403 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 403 — score=0.28 severity=LOW — API correctly rejected with documented 403 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 403 — score=0.28 severity=LOW — API correctly rejected with documented 403 error.
- [EXPECTED_FAILURE] POST /identity/api/auth/v4.0/user/login-with-token → 403 — score=0.28 severity=LOW — API correctly rejected with documented 403 error.
- [EXPECTED_FAILURE] DELETE /identity/api/v2/user/videos/{video_id} → 404 — score=0.3 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] DELETE /identity/api/v2/admin/videos/{video_id} → 404 — score=0.3 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] GET /identity/api/v2/vehicle/{vehicleId}/location → 404 — score=0.31 severity=LOW — API correctly rejected with documented 404 error.
- [EXPECTED_FAILURE] POST /workshop/api/shop/products → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/shop/products → 400 — score=0.3 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/shop/products → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/shop/products → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/shop/products → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/shop/products → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.
- [EXPECTED_FAILURE] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — API correctly rejected with documented 400 error.

### ERROR_CONTRADICTION
- [ERROR_CONTRADICTION] POST /community/api/v2/coupon/new-coupon → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: {'error': 'json: cannot unmarshal string into Go value of type models.Coupon'} is not of type 'string'
- [ERROR_CONTRADICTION] POST /community/api/v2/coupon/new-coupon → 400 — score=0.3 severity=LOW — Error response body for 400 does not match contract. Details: {'error': 'json: cannot unmarshal number into Go struct field Coupon.coupon_code of type string'} is not of type 'string'
- [ERROR_CONTRADICTION] POST /community/api/v2/coupon/new-coupon → 400 — score=0.3 severity=LOW — Error response body for 400 does not match contract. Details: {'error': 'json: cannot unmarshal number into Go struct field Coupon.amount of type string'} is not of type 'string'
- [ERROR_CONTRADICTION] POST /workshop/api/shop/orders → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/orders → 400 — score=0.3 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/orders → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/orders → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/orders → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/orders → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/apply_coupon → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/apply_coupon → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/apply_coupon → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/apply_coupon → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/shop/apply_coupon → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/merchant/contact_mechanic → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.27 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property
- [ERROR_CONTRADICTION] POST /workshop/api/mechanic/signup → 400 — score=0.31 severity=LOW — Error response body for 400 does not match contract. Details: 'message' is a required property

### UNEXPECTED_SUCCESS
- [UNEXPECTED_SUCCESS] GET /workshop/api/shop/return_qr_code → 200 — score=0.0 severity=LOW — Authentication probe was accepted with status 200; the request used no valid credentials.
- [UNEXPECTED_SUCCESS] GET /workshop/api/shop/return_qr_code → 200 — score=0.0 severity=LOW — Authentication probe was accepted with status 200; the request used no valid credentials.
- [UNEXPECTED_SUCCESS] POST /identity/api/v2/user/reset-password → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- [UNEXPECTED_SUCCESS] POST /identity/api/v2/user/reset-password → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- [UNEXPECTED_SUCCESS] POST /community/api/v2/coupon/new-coupon → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- [UNEXPECTED_SUCCESS] POST /community/api/v2/coupon/validate-coupon → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- [UNEXPECTED_SUCCESS] POST /community/api/v2/coupon/validate-coupon → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- [UNEXPECTED_SUCCESS] POST /workshop/api/shop/products → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- [UNEXPECTED_SUCCESS] POST /workshop/api/shop/products → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.
- [UNEXPECTED_SUCCESS] POST /workshop/api/shop/products → 200 — score=0.31 severity=LOW — Server accepted a mutated payload and returned 200. The API should have rejected the invalid input.

### SUCCESS_CONTRADICTION
- [SUCCESS_CONTRADICTION] GET /community/api/v2/community/posts/recent → 200 — score=0.49 severity=MEDIUM — Response body for 200 does not match the contract. Details: {'posts': [{'id': '2RUPhHy24xSyXNxJACwoJa', 'title': '', 'content': '', 'author': {'nickname': 'tqxifajc', 'email': 'tqxifajc@fuzzer.com', 'vehicleid': '', 'profile_pic_url': '', 'created_at': '2026-08-01T18:08:25.596Z'}, 'comments': [], 'authorid': 8, 'CreatedAt': '2026-08-01T18:08:25.596Z'}, {'id': 'aVuzTokrfM9FJ2KyBNU5aW', 'title': 'A', 'content': 'A', 'author': {'nickname': 'tqxifajc', 'email': 'tqxifajc@fuzzer.com', 'vehicleid': '', 'profile_pic_url': '', 'created_at': '2026-08-01T18:08:25.049Z'}, 'comments': [], 'authorid': 8, 'CreatedAt': '2026-08-01T18:08:25.049Z'}, {'id': 'KjTtSEP2ndd6Zv6vDaGtCe', 'title': 'Title 3', 'content': 'Hello world 3', 'author': {'nickname': 'Robot', 'email': 'robot001@example.com', 'vehicleid': '4bae9968-ec7f-4de3-a3a0-ba1b2ab5e5e5', 'profile_pic_url': '', 'created_at': '2026-08-01T18:06:56.651Z'}, 'comments': [], 'authorid': 3, 'CreatedAt': '2026-08-01T18:06:56.651Z'}, {'id': 'ZgifX6wp6ikxUjZSHDDz95', 'title': 'Title 2', 'content': 'Hello world 2', 'author': {'nickname': 'Pogba', 'email': 'pogba006@example.com', 'vehicleid': 'cd515c12-0fc1-48ae-8b61-9230b70a845b', 'profile_pic_url': '', 'created_at': '2026-08-01T18:06:56.65Z'}, 'comments': [], 'authorid': 2, 'CreatedAt': '2026-08-01T18:06:56.65Z'}, {'id': 'peNgqu649dsYyb4ZBixRyj', 'title': 'Title 1', 'content': 'Hello world 1', 'author': {'nickname': 'Adam', 'email': 'adam007@example.com', 'vehicleid': 'f89b5f21-7829-45cb-a650-299a61090378', 'profile_pic_url': '', 'created_at': '2026-08-01T18:06:56.623Z'}, 'comments': [], 'authorid': 1, 'CreatedAt': '2026-08-01T18:06:56.623Z'}], 'next_offset': 0, 'previous_offset': 0, 'total': 5} is not of type 'array'
- [SUCCESS_CONTRADICTION] POST /community/api/v2/coupon/new-coupon → 200 — score=0.31 severity=LOW — Response body for 200 does not match the contract. Details: None is not of type 'string'
- [SUCCESS_CONTRADICTION] POST /community/api/v2/coupon/new-coupon → 200 — score=0.31 severity=LOW — Response body for 200 does not match the contract. Details: None is not of type 'string'