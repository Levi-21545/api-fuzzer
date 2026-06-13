from fuzzer.model.http import HttpMethod
from fuzzer.model.schema import Schema


def test_endpoint_id(sample_endpoint):
    assert sample_endpoint.id == "GET /users/{id}"


def test_endpoint_method(sample_endpoint):
    assert sample_endpoint.method == HttpMethod.GET


def test_endpoint_parameters(sample_endpoint):
    assert len(sample_endpoint.parameters) == 1
    param = sample_endpoint.parameters[0]
    assert param.name == "id"
    assert param.location == "path"
    assert param.required is True


def test_endpoint_no_request_body(sample_endpoint):
    assert sample_endpoint.request_body is None


def test_endpoint_with_body():
    from fuzzer.model.endpoint import Endpoint
    from fuzzer.model.request_body import RequestBody

    ep = Endpoint(
        path="/users",
        method=HttpMethod.POST,
        parameters=[],
        request_body=RequestBody(
            content_type="application/json",
            schema=Schema(type="object", properties={"name": Schema(type="string")}),
        ),
        responses={"201": Schema(type="object")},
    )
    assert ep.request_body is not None
    assert ep.request_body.content_type == "application/json"
    assert ep.request_body.schema.type == "object"
