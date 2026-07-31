
from fuzzer.analysis.analyzer import Analyzer
from fuzzer.analysis.classification import Anomaly
from fuzzer.model.api_spec import APISpec
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.model.request_body import RequestBody
from fuzzer.model.schema import Schema
from fuzzer.executor.result import ExecutionResult
from fuzzer.utils.types import ExecutionPlanEntry


def _analyzer_for_endpoint(ep: Endpoint) -> Analyzer:
    spec = APISpec(base_urls=["http://localhost"], endpoints=[ep])
    return Analyzer(spec)


def _plan_entry(
    endpoint: Endpoint,
    payload=None,
    mutations: list[dict[str, object]] | None = None,
) -> ExecutionPlanEntry:
    return ExecutionPlanEntry(
        endpoint=endpoint,
        path=endpoint.path,
        payload=payload,
        headers={},
        case_id="case-test",
        case_kind="mutation" if mutations else "baseline",
        mutations=mutations or [],
    )


def test_server_error():
    ep = Endpoint(path="/test", method=HttpMethod.GET, parameters=[], request_body=None, responses={})
    result = ExecutionResult(
        endpoint_id="GET /test", method=HttpMethod.GET, url="http://localhost/test",
        status_code=500, response_time_ms=10, response_size=100,
        raw_response='{"error":"internal"}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(_plan_entry(ep), result)
    assert analysis is not None
    assert analysis.classification == Anomaly.SERVER_ERROR


def test_undocumented_4xx():
    ep = Endpoint(path="/test", method=HttpMethod.POST, parameters=[], request_body=None, responses={})
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=403, response_time_ms=10, response_size=50,
        raw_response='{"error":"forbidden"}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(_plan_entry(ep), result)
    assert analysis is not None
    assert analysis.classification == Anomaly.UNEXPECTED_ERROR_STATUS


def test_documented_4xx_expected_failure():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[], request_body=None,
        responses={"403": Schema(type="object", properties={"error": Schema(type="string")})},
    )
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=403, response_time_ms=10, response_size=50,
        raw_response='{"error":"forbidden"}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(_plan_entry(ep), result)
    assert analysis is not None
    assert analysis.classification == Anomaly.EXPECTED_FAILURE


def test_documented_4xx_error_contradiction():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[], request_body=None,
        responses={"400": Schema(type="string")},
    )
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=400, response_time_ms=10, response_size=50,
        raw_response='{"msg":"bad request"}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(_plan_entry(ep), result)
    assert analysis is not None
    assert analysis.classification == Anomaly.ERROR_CONTRADICTION


def test_unexpected_success_with_mutation():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[],
        request_body=RequestBody(
            content_type="application/json",
            schema=Schema(type="object", properties={"name": Schema(type="string")}, required=["name"]),
        ),
        responses={"200": Schema(type="object", properties={"id": Schema(type="integer")})},
    )
    # mutated payload differs from baseline
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=200, response_time_ms=10, response_size=50,
        raw_response='{"id":1}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(
        _plan_entry(ep, {"name": 123}, [{"expected_valid": False}]),
        result,
    )
    assert analysis is not None
    assert analysis.classification == Anomaly.UNEXPECTED_SUCCESS


def test_success_conformant_return_none():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[],
        request_body=RequestBody(
            content_type="application/json",
            schema=Schema(type="object", properties={"name": Schema(type="string")}, required=["name"]),
        ),
        responses={"200": Schema(type="object", properties={"id": Schema(type="integer")})},
    )
    # baseline payload matching what generate_valid_value produces
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=200, response_time_ms=10, response_size=50,
        raw_response='{"id":1}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(
        _plan_entry(ep, {"name": "A"}),
        result,
    )
    assert analysis is None


def test_valid_mutation_accepted_is_not_an_anomaly():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[],
        request_body=RequestBody(
            content_type="application/json",
            schema=Schema(type="object", properties={"enabled": Schema(type="boolean")}),
        ),
        responses={"200": Schema(type="object", properties={"id": Schema(type="integer")})},
    )
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=200, response_time_ms=10, response_size=50,
        raw_response='{"id":1}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(
        _plan_entry(ep, {"enabled": False}, [{"expected_valid": True}]),
        result,
    )
    assert analysis is None


def test_success_contradiction():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[], request_body=None,
        responses={"200": Schema(type="object", properties={"id": Schema(type="integer")})},
    )
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=200, response_time_ms=10, response_size=50,
        raw_response='{"id":"not-an-integer"}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(_plan_entry(ep), result)
    assert analysis is not None
    assert analysis.classification == Anomaly.SUCCESS_CONTRADICTION


def test_undocumented_success_status():
    ep = Endpoint(
        path="/test", method=HttpMethod.GET, parameters=[], request_body=None,
        responses={"200": Schema(type="object")},
    )
    result = ExecutionResult(
        endpoint_id="GET /test", method=HttpMethod.GET, url="http://localhost/test",
        status_code=201, response_time_ms=10, response_size=50,
        raw_response='{}', error=None,
    )
    analysis = _analyzer_for_endpoint(ep)._analyze_single(_plan_entry(ep), result)
    assert analysis is not None
    assert analysis.classification == Anomaly.SUCCESS_CONTRADICTION
