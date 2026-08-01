from dataclasses import replace

from fuzzer.analysis.classification import AnomalySeverity
from fuzzer.analysis.fuzzy_engine import FuzzyEngine
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.model.request_body import RequestBody
from fuzzer.model.schema import Schema
from fuzzer.utils.types import ExecutionPlanEntry


def _engine() -> FuzzyEngine:
    return FuzzyEngine()


def _endpoint(
    responses: dict[str, Schema] | None = None,
    *,
    body: bool = False,
    requires_authentication: bool = False,
) -> Endpoint:
    request_body = None
    if body:
        request_body = RequestBody(
            content_type="application/json",
            schema=Schema(
                type="object",
                properties={"name": Schema(type="string")},
                required=["name"],
            ),
        )
    return Endpoint(
        path="/test",
        method=HttpMethod.POST,
        parameters=[],
        request_body=request_body,
        responses=responses or {},
        security=[{"bearerAuth": []}] if requires_authentication else None,
    )


def _result(
    status: int | None,
    *,
    raw_response: str | None = "{}",
    response_time_ms: float = 10,
    response_size: int | None = 100,
) -> ExecutionResult:
    return ExecutionResult(
        endpoint_id="POST /test",
        method=HttpMethod.POST,
        url="http://localhost/test",
        status_code=status,
        response_time_ms=response_time_ms,
        response_size=response_size,
        raw_response=raw_response,
        error="timeout" if status is None else None,
    )


def test_isolated_server_error_scores_medium():
    assessment = _engine().assess(_endpoint(), _result(500))

    assert assessment.score == 0.5
    assert assessment.severity == AnomalySeverity.MEDIUM
    assert assessment.inputs["behavior_contradiction"] == 1.0
    assert assessment.inputs["evidence_strength"] == 0.5
    assert [rule["id"] for rule in assessment.activated_rules] == [
        "R3_HIGH_CONTRADICTION_WEAK_EVIDENCE"
    ]


def test_repeated_server_error_scores_high_with_strong_evidence():
    assessment = _engine().assess(
        _endpoint(),
        _result(500),
        evidence_strength=1.0,
    )

    assert assessment.score == 0.84
    assert assessment.severity == AnomalySeverity.HIGH
    assert [rule["id"] for rule in assessment.activated_rules] == [
        "R4_HIGH_CONTRADICTION_STRONG_EVIDENCE"
    ]


def test_transport_failure_uses_evidence_strength():
    engine = _engine()

    isolated = engine.assess(_endpoint(), _result(None, raw_response=None))
    repeated = engine.assess(
        _endpoint(),
        _result(None, raw_response=None),
        evidence_strength=1.0,
    )

    assert isolated.severity == AnomalySeverity.MEDIUM
    assert repeated.severity == AnomalySeverity.HIGH


def test_safe_rejection_expected_scores_low_even_with_contract_drift():
    assessment = _engine().assess(
        _endpoint(),
        _result(403, raw_response='{"error":"forbidden"}'),
        expects_rejection=True,
    )

    assert assessment.inputs["behavior_contradiction"] == 0.15
    assert assessment.severity == AnomalySeverity.LOW
    assert assessment.fallback_used is False


def test_generated_resource_rejection_scores_low():
    assessment = _engine().assess(
        _endpoint(),
        _result(404, raw_response='{"error":"not found"}'),
    )

    assert assessment.inputs["behavior_contradiction"] == 0.2
    assert assessment.severity == AnomalySeverity.LOW


def test_undocumented_400_for_generated_body_scores_medium():
    assessment = _engine().assess(
        _endpoint({"200": Schema(type="object")}, body=True),
        _result(400, raw_response='{"error":"size must be at least 3"}'),
    )

    assert assessment.inputs["behavior_contradiction"] == 0.6
    assert assessment.severity == AnomalySeverity.MEDIUM


def test_expected_rejection_accepted_scores_medium():
    assessment = _engine().assess(
        _endpoint({"200": Schema(type="object")}),
        _result(200),
        expects_rejection=True,
    )

    assert assessment.inputs["behavior_contradiction"] == 0.7
    assert assessment.severity == AnomalySeverity.MEDIUM
    assert assessment.fallback_used is False


def test_missing_credential_accepted_scores_high():
    assessment = _engine().assess(
        _endpoint(
            {"200": Schema(type="object")},
            requires_authentication=True,
        ),
        _result(200),
        expects_rejection=True,
        case_kind="auth_probe",
        auth_probe_kind="missing_credential",
    )

    assert assessment.inputs["access_control_exposure"] == 1.0
    assert assessment.severity == AnomalySeverity.HIGH
    assert any(
        rule["id"] == "R6_CLEAR_ACCESS_EXPOSURE"
        for rule in assessment.activated_rules
    )


def test_invalid_credential_accepted_scores_medium():
    assessment = _engine().assess(
        _endpoint(
            {"200": Schema(type="object")},
            requires_authentication=True,
        ),
        _result(200),
        expects_rejection=True,
        case_kind="auth_probe",
        auth_probe_kind="invalid_credential",
    )

    assert assessment.inputs["access_control_exposure"] == 0.6
    assert assessment.severity == AnomalySeverity.MEDIUM


def test_success_response_schema_contradiction_scores_medium():
    assessment = _engine().assess(
        _endpoint({"200": Schema(type="object")}),
        _result(200, raw_response='["not", "an", "object"]'),
    )

    assert assessment.inputs["behavior_contradiction"] == 0.65
    assert assessment.severity == AnomalySeverity.MEDIUM


def test_undocumented_success_status_without_stronger_contradiction_scores_low():
    assessment = _engine().assess(
        _endpoint({"200": Schema(type="object")}),
        _result(201),
    )

    assert assessment.inputs["behavior_contradiction"] == 0.25
    assert assessment.severity == AnomalySeverity.LOW


def test_time_and_size_do_not_change_v3_assessment():
    engine = _engine()
    endpoint = _endpoint({"200": Schema(type="object")})
    result = _result(200, raw_response='["wrong"]')

    baseline = engine.assess(endpoint, result)
    changed = engine.assess(
        endpoint,
        replace(result, response_time_ms=5000, response_size=3_000_000),
    )

    assert baseline.score == changed.score
    assert baseline.severity == changed.severity
    assert baseline.inputs == changed.inputs


def test_rule_base_covers_representative_fact_grid():
    engine = _engine()
    endpoint = _endpoint({"200": Schema(type="object")}, body=True)
    cases = [
        (None, False, "baseline", None, 0.5),
        (500, False, "baseline", None, 1.0),
        (200, False, "baseline", None, 0.5),
        (201, False, "baseline", None, 0.5),
        (400, False, "baseline", None, 0.5),
        (403, True, "mutation", None, 0.5),
        (200, True, "mutation", None, 0.5),
        (200, True, "auth_probe", "missing_credential", 0.5),
        (200, True, "auth_probe", "invalid_credential", 0.5),
    ]

    for status, rejects, case_kind, auth_kind, evidence in cases:
        assessment = engine.assess(
            endpoint,
            _result(status, raw_response=None if status is None else "{}"),
            expects_rejection=rejects,
            case_kind=case_kind,
            auth_probe_kind=auth_kind,
            evidence_strength=evidence,
        )

        assert assessment.fallback_used is False
        assert assessment.activated_rules


def test_assessment_exposes_v3_inputs_and_memberships():
    assessment = _engine().assess(_endpoint(), _result(500))

    assert assessment.model_id == "mamdani-behavior-evidence-access-v3"
    assert assessment.inputs == {
        "behavior_contradiction": 1.0,
        "evidence_strength": 0.5,
        "access_control_exposure": 0.0,
    }
    assert assessment.memberships["behavior_contradiction"]["high"] == 1.0


def test_analyzer_integrates_fuzzy_v3_context():
    from fuzzer.analysis.analyzer import Analyzer
    from fuzzer.model.api_spec import APISpec

    endpoint = _endpoint(
        {"200": Schema(type="object")},
        requires_authentication=True,
    )
    analyzer = Analyzer(APISpec(base_urls=["http://localhost"], endpoints=[endpoint]))
    plan_entry = ExecutionPlanEntry(
        endpoint=endpoint,
        path=endpoint.path,
        payload=None,
        headers={},
        case_id="case-test",
        case_kind="auth_probe",
        auth_probe_kind="missing_credential",
    )

    analyses = analyzer.analyze_all([_result(200)], [plan_entry])

    assert len(analyses) == 1
    analysis = analyses[0]
    assert analysis.severity == AnomalySeverity.HIGH
    assert analysis.severity_assessment is not None
    assert (
        analysis.severity_assessment["model_id"]
        == "mamdani-behavior-evidence-access-v3"
    )
    assert (
        analysis.severity_assessment["inputs"]["access_control_exposure"]
        == 1.0
    )
