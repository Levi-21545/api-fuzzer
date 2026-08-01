from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any


EXPECTED_CLASSIFICATION = "EXPECTED_FAILURE"
TOKEN_KEYS = {
    "access_token",
    "auth_token",
    "authorization",
    "jwt",
    "refresh_token",
    "token",
}
ID_KEY_PATTERN = re.compile(r"(?:^id$|_id$|Id$)")
UUID_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
)
TIMESTAMP_PATTERN = re.compile(
    r"\b\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:[Zz]|[+-]\d{2}:?\d{2})\b"
)
JWT_PATTERN = re.compile(
    r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)
BEARER_PATTERN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
JAVA_IDENTITY_PATTERN = re.compile(r"@[0-9a-fA-F]{6,16}\b")


@dataclass(frozen=True)
class CorrelatedFinding:
    plan: dict[str, Any]
    result: dict[str, Any]
    finding: dict[str, Any]

    @property
    def case_id(self) -> str:
        return self.plan["case_id"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan": self.plan,
            "result": self.result,
            "finding": self.finding,
        }


def _redact_text(value: str) -> str:
    value = BEARER_PATTERN.sub("Bearer <TOKEN>", value)
    value = JWT_PATTERN.sub("<TOKEN>", value)
    value = UUID_PATTERN.sub("<UUID>", value)
    value = TIMESTAMP_PATTERN.sub("<TIMESTAMP>", value)
    return JAVA_IDENTITY_PATTERN.sub("@<ID>", value)


def _normalize_json(value: Any, key: str | None = None) -> Any:
    if key is not None and key.casefold() in TOKEN_KEYS:
        return "<TOKEN>"
    if key is not None and ID_KEY_PATTERN.search(key):
        if value is not None and not isinstance(value, (dict, list, bool)):
            return "<ID>"
    if isinstance(value, dict):
        return {
            item_key: _normalize_json(value[item_key], item_key)
            for item_key in sorted(value)
        }
    if isinstance(value, list):
        return [_normalize_json(item) for item in value]
    if isinstance(value, str):
        return _redact_text(value)
    return value


def normalize_response(raw_response: str | None, error: str | None = None) -> str:
    """Create a conservative, deterministic response representation."""
    if error is not None:
        category = error.split(":", maxsplit=1)[0].strip() or "UNKNOWN_ERROR"
        return f"network-error:{category}"
    try:
        parsed = json.loads(raw_response or "")
    except (json.JSONDecodeError, TypeError):
        return _redact_text(raw_response or "")
    return json.dumps(
        _normalize_json(parsed),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _validation_path(finding: dict[str, Any]) -> str | None:
    for key in ("validation_error_path", "validation_path", "schema_path"):
        value = finding.get(key)
        if isinstance(value, list):
            return "/" + "/".join(str(part) for part in value)
        if value is not None:
            return str(value)
    return None


def build_signature(
    api_id: str,
    correlated: CorrelatedFinding,
) -> dict[str, Any]:
    normalized = normalize_response(
        correlated.result.get("raw_response"),
        correlated.result.get("error"),
    )
    components = {
        "api_id": api_id,
        "endpoint_id": correlated.finding["endpoint_id"],
        "classification": correlated.finding["classification"],
        "status_code": correlated.result.get("status_code"),
        "normalized_response_sha256": _sha256(normalized),
        "validation_error_path": _validation_path(correlated.finding),
    }
    canonical = json.dumps(components, sort_keys=True, separators=(",", ":"))
    return {
        "id": _sha256(canonical),
        "components": components,
        "normalized_response": normalized,
    }


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _representative_key(item: CorrelatedFinding) -> tuple[int, str]:
    payload = json.dumps(
        item.plan.get("payload"),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return len(payload.encode("utf-8")), item.case_id


def deduplicate_findings(
    api_id: str,
    correlated: list[CorrelatedFinding],
) -> list[dict[str, Any]]:
    buckets: dict[str, list[CorrelatedFinding]] = {}
    signatures: dict[str, dict[str, Any]] = {}
    for item in correlated:
        if item.finding["classification"] == EXPECTED_CLASSIFICATION:
            continue
        signature = build_signature(api_id, item)
        signature_id = signature["id"]
        signatures[signature_id] = signature
        buckets.setdefault(signature_id, []).append(item)

    unique: list[dict[str, Any]] = []
    for signature_id in sorted(buckets):
        items = buckets[signature_id]
        representative = min(items, key=_representative_key)
        unique.append(
            {
                "signature": signatures[signature_id],
                "occurrence_count": len(items),
                "case_ids": sorted(item.case_id for item in items),
                "representative": representative.to_dict(),
            }
        )
    return unique
