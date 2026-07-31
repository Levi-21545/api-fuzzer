import yaml

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


def test_local_schema_references_and_path_parameters_are_resolved(tmp_path):
    contract = {
        "openapi": "3.0.1",
        "servers": [{"url": "http://localhost"}],
        "paths": {
            "/orders/{orderId}": {
                "parameters": [
                    {
                        "name": "orderId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OrderRequest"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/OrderResponse"
                                    }
                                }
                            }
                        }
                    },
                },
            }
        },
        "components": {
            "schemas": {
                "OrderRequest": {
                    "type": "object",
                    "required": ["quantity"],
                    "properties": {
                        "quantity": {"type": "integer", "minimum": 1}
                    },
                },
                "OrderResponse": {
                    "type": "object",
                    "properties": {
                        "request": {
                            "$ref": "#/components/schemas/OrderRequest"
                        }
                    },
                },
            }
        },
    }
    contract_path = tmp_path / "openapi.yaml"
    contract_path.write_text(yaml.safe_dump(contract), encoding="utf-8")

    spec = OpenAPIParser(str(contract_path)).parse()
    endpoint = spec.endpoints[0]

    assert endpoint.parameters[0].name == "orderId"
    assert endpoint.parameters[0].schema.type == "integer"
    assert endpoint.request_body is not None
    assert endpoint.request_body.schema.required == ["quantity"]
    assert endpoint.request_body.schema.properties["quantity"].constraints == {
        "minimum": 1
    }
    response_request = endpoint.responses["200"].properties["request"]
    assert response_request.required == ["quantity"]
