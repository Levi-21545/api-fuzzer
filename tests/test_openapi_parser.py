from fuzzer.parser.openapi_parser import OpenAPIParser


def test_documented_response_without_json_body_is_preserved():
    parser = OpenAPIParser.__new__(OpenAPIParser)

    responses = parser._parse_responses(
        {
            "responses": {
                "204": {"description": "Updated without response body"},
                "400": {"description": "Invalid request", "content": {}},
            }
        }
    )

    assert set(responses) == {"204", "400"}
    assert responses["204"].type is None
    assert responses["400"].type is None
