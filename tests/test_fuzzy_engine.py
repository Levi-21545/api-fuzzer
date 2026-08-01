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
    assert assessment.model_id == "mamdani-status-time-response-size-v2"
    assert assessment.severity == AnomalySeverity.HIGH
    assert assessment.inputs == {
        "status_deviation": 1.0,
        "response_time_ms": 10.0,
        "response_size_signal": 100 / 1024 * 2,
    }
    assert assessment.memberships["status_deviation"]["high"] == 1.0
    assert [rule["id"] for rule in assessment.activated_rules] == [
        "R1_HIGH_DEVIATION_OR_TIMEOUT",
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


def test_expected_rejection_accepted_scores_medium():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.POST,
        parameters=[],
        request_body=None,
        responses={"200": Schema(type="object")},
    )
    result = ExecutionResult(
        endpoint_id="POST /test",
        method=HttpMethod.POST,
        url="http://localhost/test",
        status_code=200,
        response_time_ms=30,
        response_size=50,
        raw_response="{}",
        error=None,
    )

    assessment = _engine().assess(ep, result, expects_rejection=True)

    assert assessment.inputs["status_deviation"] == 0.6
    assert assessment.severity == AnomalySeverity.MEDIUM
    assert assessment.fallback_used is False


def test_rule_base_covers_representative_input_grid():
    ep = Endpoint(
        path="/test",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={"200": Schema(type="object")},
    )

    for status in (200, 403, 500):
        for response_time in (10, 800, 3000):
            for response_size in (0, 512, 2048):
                result = ExecutionResult(
                    endpoint_id="GET /test",
                    method=HttpMethod.GET,
                    url="http://localhost/test",
                    status_code=status,
                    response_time_ms=response_time,
                    response_size=response_size,
                    raw_response="{}",
                    error=None,
                )

                assessment = _engine().assess(ep, result)

                assert assessment.fallback_used is False


def test_rule_base_covers_every_status_deviation_category():
    documented = Endpoint(
        path="/test",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={"200": Schema(type="object")},
    )
    no_reference = Endpoint(
        path="/test",
        method=HttpMethod.GET,
        parameters=[],
        request_body=None,
        responses={},
    )
    cases = [
        (documented, None, False, 1.0),
        (documented, 500, False, 1.0),
        (documented, 200, False, 0.0),
        (no_reference, 200, False, 0.5),
        (documented, 403, False, 0.6),
        (documented, 302, False, 0.4),
        (documented, 200, True, 0.6),
    ]

    for endpoint, status, expects_rejection, expected_deviation in cases:
        result = ExecutionResult(
            endpoint_id="GET /test",
            method=HttpMethod.GET,
            url="http://localhost/test",
            status_code=status,
            response_time_ms=10,
            response_size=100,
            raw_response="{}" if status is not None else None,
            error="timeout" if status is None else None,
        )

        assessment = _engine().assess(
            endpoint,
            result,
            expects_rejection=expects_rejection,
        )

        assert assessment.inputs["status_deviation"] == expected_deviation
        assert assessment.fallback_used is False


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
        == "mamdani-status-time-response-size-v2"
    )
    assert analysis.severity_assessment["inputs"]["status_deviation"] == 1.0
