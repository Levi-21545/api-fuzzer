import pytest

from fuzzer.model.schema import Schema
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.model.parameter import Parameter


@pytest.fixture
def string_schema():
    return Schema(type="string")


@pytest.fixture
def integer_schema():
    return Schema(type="integer", constraints={"minimum": 0, "maximum": 100})


@pytest.fixture
def object_schema():
    return Schema(
        type="object",
        properties={
            "name": Schema(type="string"),
            "age": Schema(type="integer"),
        },
        required=["name"],
    )


@pytest.fixture
def array_schema():
    return Schema(
        type="array",
        items=Schema(type="string"),
    )


@pytest.fixture
def nested_schema():
    return Schema(
        type="object",
        properties={
            "user": Schema(
                type="object",
                properties={
                    "email": Schema(type="string", format="email"),
                    "roles": Schema(
                        type="array", items=Schema(type="string")
                    ),
                },
                required=["email"],
            )
        },
        required=["user"],
    )


@pytest.fixture
def sample_endpoint():
    return Endpoint(
        path="/users/{id}",
        method=HttpMethod.GET,
        parameters=[
            Parameter(
                name="id",
                location="path",
                required=True,
                schema=Schema(type="string"),
            )
        ],
        request_body=None,
        responses={"200": Schema(type="object", properties={"name": Schema(type="string")})},
    )
