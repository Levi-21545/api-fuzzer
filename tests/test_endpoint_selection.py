from fuzzer.cli.select import select_endpoints
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod


def _endpoint(path: str) -> Endpoint:
    return Endpoint(
        path=path,
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={},
    )


def test_multiple_excluded_path_patterns():
    endpoints = [
        _endpoint("/createdb"),
        _endpoint("/internal/health"),
        _endpoint("/users"),
    ]

    selected = select_endpoints(
        endpoints,
        all=True,
        excluded_paths=["/createdb", "/internal/*"],
    )

    assert [endpoint.path for endpoint in selected] == ["/users"]
