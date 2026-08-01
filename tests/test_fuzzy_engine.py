from fuzzer.analysis.classification import AnomalySeverity
from fuzzer.analysis.fuzzy_engine import FuzzyEngine
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.model.schema import Schema
from fuzzer.executor.result import ExecutionResult
from fuzzer.utils.types import ExecutionPlanEntry


def _engine() -> FuzzyEngine:
    return FuzzyEngine()


def test_server_error_scores_high():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={},
    )
    result = ExecutionResult(
        endpoint_id="GET /test",
        method=HttpMethod.GET,
        url="http://localhost/test",
        status_code=500,
        response_time_ms=10,
        response_size=100,
        raw_response='{"error":"internal"}',
        error=None,
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.HIGH
    assert score >= 0.5


def test_assessment_exposes_inputs_memberships_and_activated_rules():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={},
    )
    result = ExecutionResult(
        endpoint_id="GET /test",
        method=HttpMethod.GET,
        url="http://localhost/test",
        status_code=500,
        response_time_ms=10,
        response_size=100,
        raw_response='{"error":"internal"}',
        error=None,
    )

    assessment = _engine().assess(ep, result)

    assert assessment.score == 0.84
    assert assessment.model_id == "mamdani-status-time-response-size-v1"
    assert assessment.severity == AnomalySeverity.HIGH
    assert assessment.inputs == {
        "status_deviation": 1.0,
        "response_time_ms": 10.0,
        "response_size_signal": 100 / 1024 * 2,
    }
    assert assessment.memberships["status_deviation"]["high"] == 1.0
    assert [rule["id"] for rule in assessment.activated_rules] == [
        "R1_HIGH_DEVIATION_OR_TIMEOUT",
        "R6_HIGH_DEVIATION",
    ]
    assert assessment.fallback_used is False


def test_no_response_scores_high():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={},
    )
    result = ExecutionResult(
        endpoint_id="GET /test",
        method=HttpMethod.GET,
        url="http://localhost/test",
        status_code=None,
        response_time_ms=5000,
        response_size=None,
        raw_response=None,
        error="timeout",
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.HIGH
    assert score >= 0.5


def test_documented_4xx_fast_scores_low():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.POST,
        parameters=[],
        request_body=None,
        responses={"403": Schema(type=None)},
    )
    result = ExecutionResult(
        endpoint_id="POST /test",
        method=HttpMethod.POST,
        url="http://localhost/test",
        status_code=403,
        response_time_ms=30,
        response_size=50,
        raw_response='{"error":"forbidden"}',
        error=None,
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.LOW
    assert score < 0.4


def test_undocumented_4xx_scores_medium():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.POST,
        parameters=[],
        request_body=None,
        responses={},
    )
    result = ExecutionResult(
        endpoint_id="POST /test",
        method=HttpMethod.POST,
        url="http://localhost/test",
        status_code=403,
        response_time_ms=30,
        response_size=50,
        raw_response='{"error":"forbidden"}',
        error=None,
    )
    score, severity = _engine().score(ep, result)
    assert severity == AnomalySeverity.MEDIUM
    assert 0.3 <= score <= 0.7


def test_slow_response_escalates_severity():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.POST,
        parameters=[],
        request_body=None,
        responses={"403": Schema(type=None)},
    )
    result = ExecutionResult(
        endpoint_id="POST /test",
        method=HttpMethod.POST,
        url="http://localhost/test",
        status_code=403,
        response_time_ms=3000,
        response_size=50,
        raw_response='{"error":"forbidden"}',
        error=None,
    )
    _, severity = _engine().score(ep, result)
    assert severity in (AnomalySeverity.MEDIUM, AnomalySeverity.HIGH)


def test_analyzer_integrates_fuzzy():
    from fuzzer.analysis.analyzer import Analyzer
    from fuzzer.model.api_spec import APISpec

    ep = Endpoint(
        path="/test",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={},
    )
    spec = APISpec(base_urls=["http://localhost"], endpoints=[ep])
    analyzer = Analyzer(spec)
    result = ExecutionResult(
        endpoint_id="GET /test",
        method=HttpMethod.GET,
        url="http://localhost/test",
        status_code=500,
        response_time_ms=100,
        response_size=100,
        raw_response='{"error":"internal"}',
        error=None,
    )
    plan_entry = ExecutionPlanEntry(
        endpoint=ep,
        path=ep.path,
        payload=None,
        headers={},
        case_id="case-test",
        case_kind="baseline",
    )
    analyses = analyzer.analyze_all([result], [plan_entry])

    assert len(analyses) == 1
    analysis = analyses[0]
    assert 0.0 <= analysis.severity_score <= 1.0
    assert analysis.severity in AnomalySeverity
    assert analysis.severity_assessment is not None
    assert (
        analysis.severity_assessment["model_id"]
        == "mamdani-status-time-response-size-v1"
    )
    assert analysis.severity_assessment["inputs"]["status_deviation"] == 1.0
