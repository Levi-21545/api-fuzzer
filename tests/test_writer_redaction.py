import json
from types import SimpleNamespace

from fuzzer.executor.result import ExecutionResult
from fuzzer.model.http import HttpMethod
from fuzzer.utils.writer import write_execution_plan, write_results


def test_execution_plan_redacts_authorization_header(tmp_path):
    entry = SimpleNamespace(
        case_id="case-000001",
        case_kind="baseline",
        endpoint=SimpleNamespace(id="GET /items", method=HttpMethod.GET),
        path="/items",
        payload=None,
        headers={
            "Authorization": "Bearer secret-token",
            "Accept": "application/json",
        },
        mutations=[],
    )

    write_execution_plan([entry], tmp_path)

    plan = json.loads((tmp_path / "execution_plan.json").read_text())[0]
    assert plan["headers"] == {
        "Authorization": "<REDACTED>",
        "Accept": "application/json",
    }


def test_results_redact_token_fields_in_response_body(tmp_path):
    result = ExecutionResult(
        endpoint_id="POST /login",
        method=HttpMethod.POST,
        url="http://localhost/login",
        status_code=200,
        response_time_ms=1.0,
        response_size=42,
        raw_response='{"access_token":"secret-token","status":"ok"}',
        error=None,
        case_id="case-000001",
    )

    write_results([result], tmp_path)

    persisted = json.loads((tmp_path / "results.json").read_text())[0]
    assert "secret-token" not in persisted["raw_response"]
    assert "<REDACTED>" in persisted["raw_response"]
    assert "ok" in persisted["raw_response"]
