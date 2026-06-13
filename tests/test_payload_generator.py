from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.model.parameter import Parameter
from fuzzer.model.schema import Schema
from fuzzer.payloads.generator import generates_payloads
from fuzzer.mutator.engine import MutationEngine


def test_resolve_path_no_params():
    ep = Endpoint(
        path="/users",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={},
    )
    engine = MutationEngine(level=0, max_mutations=1)
    results = list(generates_payloads(ep, engine))
    assert len(results) == 1
    path, headers, payload = results[0]
    assert path == "/users"


def test_resolve_path_param():
    ep = Endpoint(
        path="/users/{id}",
        method=HttpMethod.GET,
        parameters=[
            Parameter(name="id", location="path", required=True, schema=Schema(type="integer")),
        ],
        request_body=None,
        responses={},
    )
    engine = MutationEngine(level=0, max_mutations=1)
    results = list(generates_payloads(ep, engine))
    assert len(results) == 1
    path, headers, payload = results[0]
    assert path.startswith("/users/")
    assert path != "/users/{id}"
    # integer path param should be numeric
    param_value = path.split("/")[-1]
    assert param_value.isdigit()


def test_resolve_path_string_param():
    ep = Endpoint(
        path="/users/{name}",
        method=HttpMethod.GET,
        parameters=[
            Parameter(name="name", location="path", required=True, schema=Schema(type="string")),
        ],
        request_body=None,
        responses={},
    )
    engine = MutationEngine(level=0, max_mutations=1)
    results = list(generates_payloads(ep, engine))
    assert len(results) == 1
    path, headers, payload = results[0]
    assert path.startswith("/users/")
    param_value = path.split("/")[-1]
    assert isinstance(param_value, str)


def test_query_params():
    ep = Endpoint(
        path="/search",
        method=HttpMethod.GET,
        parameters=[
            Parameter(name="q", location="query", required=True, schema=Schema(type="string")),
            Parameter(name="page", location="query", required=False, schema=Schema(type="integer")),
        ],
        request_body=None,
        responses={},
    )
    engine = MutationEngine(level=0, max_mutations=1)
    results = list(generates_payloads(ep, engine))
    assert len(results) == 1
    path, headers, payload = results[0]
    assert path.startswith("/search?")
    assert "q=" in path
    assert "page=" in path


def test_mixed_path_and_query_params():
    ep = Endpoint(
        path="/users/{id}/posts",
        method=HttpMethod.GET,
        parameters=[
            Parameter(name="id", location="path", required=True, schema=Schema(type="integer")),
            Parameter(name="sort", location="query", required=False, schema=Schema(type="string")),
        ],
        request_body=None,
        responses={},
    )
    engine = MutationEngine(level=0, max_mutations=1)
    results = list(generates_payloads(ep, engine))
    assert len(results) == 1
    path, headers, payload = results[0]
    assert path.startswith("/users/")
    assert "/posts?" in path or "/posts" in path
    assert "sort=" in path
