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


def test_local_request_body_and_response_references_are_resolved(tmp_path):
    contract = {
        "openapi": "3.1.0",
        "paths": {
            "/users": {
                "post": {
                    "requestBody": {
                        "$ref": "#/components/requestBodies/NewUserRequest"
                    },
                    "responses": {
                        "201": {"$ref": "#/components/responses/UserResponse"}
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "NewUser": {
                    "type": "object",
                    "required": ["username"],
                    "properties": {"username": {"type": "string"}},
                },
                "User": {
                    "type": "object",
                    "required": ["username"],
                    "properties": {"username": {"type": "string"}},
                },
            },
            "requestBodies": {
                "NewUserRequest": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/NewUser"}
                        }
                    },
                }
            },
            "responses": {
                "UserResponse": {
                    "description": "Created user",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    },
                }
            },
        },
    }
    contract_path = tmp_path / "openapi.yaml"
    contract_path.write_text(yaml.safe_dump(contract), encoding="utf-8")

    endpoint = OpenAPIParser(str(contract_path)).parse().endpoints[0]

    assert endpoint.request_body is not None
    assert endpoint.request_body.schema.required == ["username"]
    assert endpoint.responses["201"].required == ["username"]


def test_all_of_object_schemas_are_merged(tmp_path):
    contract = {
        "openapi": "3.0.1",
        "paths": {
            "/pets": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Pet"
                                }
                            }
                        }
                    },
                    "responses": {"204": {"description": "Updated"}},
                }
            }
        },
        "components": {
            "schemas": {
                "PetFields": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "minLength": 1,
                        }
                    },
                },
                "Pet": {
                    "allOf": [
                        {"$ref": "#/components/schemas/PetFields"},
                        {
                            "type": "object",
                            "required": ["id"],
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "readOnly": True,
                                }
                            },
                        },
                    ]
                },
            }
        },
    }
    contract_path = tmp_path / "openapi.yaml"
    contract_path.write_text(yaml.safe_dump(contract), encoding="utf-8")

    endpoint = OpenAPIParser(str(contract_path)).parse().endpoints[0]
    assert endpoint.request_body is not None
    schema = endpoint.request_body.schema

    assert schema.type == "object"
    assert schema.required == ["name", "id"]
    assert set(schema.properties) == {"name", "id"}
    assert schema.properties["name"].constraints == {"minLength": 1}
    assert schema.properties["id"].constraints == {"minimum": 0}
    assert schema.properties["id"].read_only is True
