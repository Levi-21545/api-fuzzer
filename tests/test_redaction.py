from fuzzer.utils.redaction import (
    REDACTED,
    redact_headers,
    redact_serialized_text,
    redact_value,
)


def test_redact_headers_preserves_non_sensitive_context():
    headers = {
        "Authorization": "Bearer secret-token",
        "X-API-Key": "api-secret",
        "Content-Type": "application/json",
    }

    assert redact_headers(headers) == {
        "Authorization": REDACTED,
        "X-API-Key": REDACTED,
        "Content-Type": "application/json",
    }


def test_redact_serialized_json_tokens_and_embedded_jwt():
    raw = (
        '{"token":"opaque-secret","message":"Bearer abc.def.ghi",'
        '"value":"kept"}'
    )

    redacted = redact_serialized_text(raw)

    assert "opaque-secret" not in redacted
    assert "abc.def.ghi" not in redacted
    assert '"value":"kept"' in redacted


def test_redact_value_handles_artifact_header_containers():
    artifact = {
        "headers": {"Authorization": "Basic credentials"},
        "request_headers": {"Cookie": "session=secret"},
        "description": "safe",
    }

    assert redact_value(artifact) == {
        "headers": {"Authorization": REDACTED},
        "request_headers": {"Cookie": REDACTED},
        "description": "safe",
    }
