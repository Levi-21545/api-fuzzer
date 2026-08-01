from __future__ import annotations

import json
import re
from typing import Any


REDACTED = "<REDACTED>"

_SENSITIVE_KEYS = {
    "access_token",
    "api_key",
    "authorization",
    "auth_token",
    "cookie",
    "id_token",
    "jwt",
    "proxy_authorization",
    "refresh_token",
    "set_cookie",
    "token",
    "x_api_key",
}
_SENSITIVE_HEADERS = {
    "api-key",
    "authorization",
    "cookie",
    "proxy-authorization",
    "set-cookie",
    "x-api-key",
}
_BEARER_PATTERN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
_JWT_PATTERN = re.compile(
    r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)


def redact_text(value: str) -> str:
    """Redact recognizable credentials embedded in unstructured text."""
    value = _BEARER_PATTERN.sub(f"Bearer {REDACTED}", value)
    return _JWT_PATTERN.sub(REDACTED, value)


def redact_headers(headers: dict[str, Any]) -> dict[str, Any]:
    """Return headers safe to persist while retaining non-sensitive context."""
    return {
        name: REDACTED if name.casefold() in _SENSITIVE_HEADERS else redact_value(value)
        for name, value in headers.items()
    }


def redact_serialized_text(value: str) -> str:
    """Redact a response body while preserving its serialized representation."""
    try:
        parsed = json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return redact_text(value)
    return json.dumps(
        redact_value(parsed),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def redact_value(value: Any, key: str | None = None) -> Any:
    """Recursively redact credentials from a persisted artifact value."""
    normalized_key = key.casefold().replace("-", "_") if key else None
    if normalized_key in _SENSITIVE_KEYS:
        return REDACTED
    if normalized_key in {"headers", "request_headers"} and isinstance(value, dict):
        return redact_headers(value)
    if normalized_key == "raw_response" and isinstance(value, str):
        return redact_serialized_text(value)
    if isinstance(value, dict):
        return {
            item_key: redact_value(item_value, item_key)
            for item_key, item_value in value.items()
        }
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value
