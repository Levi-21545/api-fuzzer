import json

import pytest

from fuzzer.analysis.deduplication import (
    CorrelatedFinding,
    build_signature,
    deduplicate_findings,
    normalize_response,
)
from fuzzer.analysis.run_postprocessor import CorrelationError, correlate_records


def _records(case_id="case-000001", classification="SERVER_ERROR", payload=None):
    endpoint = "POST /owners"
    plan = {
        "case_id": case_id,
        "endpoint_id": endpoint,
        "payload": payload,
    }
    result = {
        "case_id": case_id,
        "endpoint_id": endpoint,
        "status_code": 500,
        "raw_response": '{"title":"Failure","timestamp":"2026-07-31T01:00:00Z"}',
        "error": None,
    }
    finding = {
        "case_id": case_id,
        "endpoint_id": endpoint,
        "status_code": 500,
        "classification": classification,
        "request_payload": payload,
    }
    return plan, result, finding


def test_normalize_response_is_conservative_and_deterministic():
    first = json.dumps(
        {
            "timestamp": "2026-07-31T01:02:03.123Z",
            "detail": "field count must be 3",
            "request_id": 42,
            "token": "secret-value",
            "uuid": "123e4567-e89b-42d3-a456-426614174000",
            "path": "/owners/42",
        }
    )
    second = json.dumps(
        {
            "path": "/owners/42",
            "uuid": "123e4567-e89b-42d3-a456-426614174999",
            "token": "another-secret",
            "request_id": 99,
            "detail": "field count must be 3",
            "timestamp": "2026-08-01T09:08:07Z",
        }
    )

    assert normalize_response(first) == normalize_response(second)
    assert '"detail":"field count must be 3"' in normalize_response(first)
    assert '"path":"/owners/42"' in normalize_response(first)


def test_signature_includes_validation_path_and_changes_by_endpoint():
    _, result, finding = _records()
    finding["validation_error_path"] = ["body", "name"]
    plan = {"case_id": "case-000001", "payload": None}
    correlated = CorrelatedFinding(plan, result, finding)
    first = build_signature("petclinic", correlated)
    finding["endpoint_id"] = "POST /pets"
    second = build_signature("petclinic", correlated)

    assert first["components"]["validation_error_path"] == "/body/name"
    assert first["id"] != second["id"]


def test_correlation_rejects_duplicates_missing_records_and_inconsistency():
    plan, result, finding = _records()
    with pytest.raises(CorrelationError, match="duplicate case_id"):
        correlate_records([plan, plan], [result], [finding])
    with pytest.raises(CorrelationError, match="plan/result case_id mismatch"):
        correlate_records([plan], [], [finding])
    bad_finding = {**finding, "status_code": 400}
    with pytest.raises(CorrelationError, match="inconsistent status_code"):
        correlate_records([plan], [result], [bad_finding])


def test_expected_failures_are_excluded_before_deduplication():
    plan, result, finding = _records(classification="EXPECTED_FAILURE")
    correlated = correlate_records([plan], [result], [finding])

    assert deduplicate_findings("petclinic", correlated) == []


def test_shortest_serialized_payload_is_representative_then_case_id():
    first = _records("case-000002", payload={"name": "longer"})
    second = _records("case-000003", payload=None)
    third = _records("case-000001", payload=None)
    correlated = correlate_records(
        [first[0], second[0], third[0]],
        [first[1], second[1], third[1]],
        [first[2], second[2], third[2]],
    )

    unique = deduplicate_findings("petclinic", correlated)

    assert len(unique) == 1
    assert unique[0]["occurrence_count"] == 3
    assert unique[0]["representative"]["plan"]["case_id"] == "case-000001"
    assert unique[0]["execution_levels"] == ["level_0"]
    assert unique[0]["case_kinds"] == ["baseline"]


def test_deduplication_preserves_all_levels_for_one_signature():
    baseline = _records("case-000001", payload=None)
    baseline[0]["case_kind"] = "baseline"
    baseline[0]["mutations"] = []
    mutation = _records("case-000002", payload=None)
    mutation[0]["case_kind"] = "mutation"
    mutation[0]["mutations"] = [{"operator": "wrong_type"}]
    correlated = correlate_records(
        [baseline[0], mutation[0]],
        [baseline[1], mutation[1]],
        [baseline[2], mutation[2]],
    )

    unique = deduplicate_findings("petclinic", correlated)

    assert len(unique) == 1
    assert unique[0]["execution_levels"] == ["level_0", "level_1"]
    assert unique[0]["case_kinds"] == ["baseline", "mutation"]
