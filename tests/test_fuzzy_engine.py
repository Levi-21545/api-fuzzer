from fuzzer.analysis.classification import AnomalySeverity
from fuzzer.analysis.fuzzy_engine import FuzzyEngine
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.executor.result import ExecutionResult


def _engine() -> FuzzyEngine:
    return FuzzyEngine()


def test_server_error_scores_high():
    ep = Endpoint(path="/test", method=HttpMethod.GET, parameters=[], request_body=None, responses={})
    result = ExecutionResult(
        endpoint_id="GET /test", method=HttpMethod.GET, url="http://localhost/test",
        status_code=500, response_time_ms=10, response_size=100,
        raw_response='{"error":"internal"}', error=None,
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.HIGH
    assert score >= 0.5


def test_no_response_scores_high():
    ep = Endpoint(path="/test", method=HttpMethod.GET, parameters=[], request_body=None, responses={})
    result = ExecutionResult(
        endpoint_id="GET /test", method=HttpMethod.GET, url="http://localhost/test",
        status_code=None, response_time_ms=5000, response_size=None,
        raw_response=None, error="timeout",
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.HIGH
    assert score >= 0.5


def test_documented_4xx_fast_scores_low():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[], request_body=None,
        responses={"403": None},
    )
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=403, response_time_ms=30, response_size=50,
        raw_response='{"error":"forbidden"}', error=None,
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.LOW
    assert score < 0.4


def test_undocumented_4xx_scores_medium():
    ep = Endpoint(path="/test", method=HttpMethod.POST, parameters=[], request_body=None, responses={})
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=403, response_time_ms=30, response_size=50,
        raw_response='{"error":"forbidden"}', error=None,
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.MEDIUM
    assert 0.3 <= score <= 0.7


def test_slow_response_escalates_severity():
    ep = Endpoint(
        path="/test", method=HttpMethod.POST, parameters=[], request_body=None,
        responses={"403": None},
    )
    result = ExecutionResult(
        endpoint_id="POST /test", method=HttpMethod.POST, url="http://localhost/test",
        status_code=403, response_time_ms=3000, response_size=50,
        raw_response='{"error":"forbidden"}', error=None,
    )
    _, severity = _engine().score(ep, result)
    assert severity in (AnomalySeverity.MEDIUM, AnomalySeverity.HIGH)


def test_analyzer_integrates_fuzzy():
    from fuzzer.analysis.analyzer import Analyzer
    from fuzzer.model.api_spec import APISpec

    ep = Endpoint(path="/test", method=HttpMethod.GET, parameters=[], request_body=None, responses={})
    spec = APISpec(base_urls=["http://localhost"], endpoints=[ep])
    analyzer = Analyzer(spec)
    result = ExecutionResult(
        endpoint_id="GET /test", method=HttpMethod.GET, url="http://localhost/test",
        status_code=500, response_time_ms=100, response_size=100,
        raw_response='{"error":"internal"}', error=None,
    )
    analysis = analyzer._analyze_single(ep, None, {}, result)
    assert analysis is not None
    score, severity = analyzer.fuzzy_engine.score(ep, result)
    assert 0.0 <= score <= 1.0
    assert severity in AnomalySeverity
