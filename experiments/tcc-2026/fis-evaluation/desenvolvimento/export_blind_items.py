#!/usr/bin/env python3
"""Export blinded FIS-review packets from the canonical L2 artifacts.

The evaluator-facing output deliberately excludes analyzer classifications,
descriptions, fuzzy scores, severity bands, memberships, rules and signature
identifiers. It contains only contract facts, the redacted request plan and the
observed response. Output is written to stdout; this script never changes run
artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

from jsonschema import ValidationError, validate

from fuzzer.model.schema import Schema
from fuzzer.parser.openapi_parser import parse_openapi


PILOTS_ROOT = Path(__file__).resolve().parents[2] / "pilots"
RUNS = {
    "vampi": "vampi-l2-20260801T190000Z",
    "petclinic": "petclinic-l2-20260801T190100Z",
    "crapi": "crapi-l2-20260801T190300Z",
    "realworld": "realworld-l2-20260801T190600Z",
}
SHUFFLE_SEED = 20260801


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_summary(schema: Schema | None, depth: int = 0) -> dict[str, Any] | None:
    if schema is None:
        return None
    summary: dict[str, Any] = {"type": schema.type}
    if schema.format:
        summary["format"] = schema.format
    if schema.constraints:
        summary["constraints"] = schema.constraints
    if schema.required:
        summary["required"] = schema.required
    if schema.type == "array":
        summary["min_items"] = schema.min_items
        summary["max_items"] = schema.max_items
        if depth < 2:
            summary["items"] = _schema_summary(schema.items, depth + 1)
    if schema.type == "object" and depth < 2:
        summary["properties"] = {
            name: _schema_summary(child, depth + 1)
            for name, child in schema.properties.items()
            if not child.read_only
        }
    return summary


def _credential_condition(plan: dict[str, Any]) -> str:
    headers = plan.get("headers") or {}
    has_authorization = any(key.lower() == "authorization" for key in headers)
    if plan.get("case_kind") == "auth_probe":
        return "invalid credential" if has_authorization else "missing credential"
    if has_authorization:
        return "configured credential"
    return "no configured credential"


def _review_context(plan: dict[str, Any]) -> str:
    credential = _credential_condition(plan)
    if plan.get("case_kind") == "auth_probe":
        return credential.replace(" ", "_")
    mutations = plan.get("mutations") or []
    if any(not mutation.get("expected_valid", False) for mutation in mutations):
        return "invalid_mutation"
    if plan.get("case_kind") == "mutation":
        return "valid_mutation"
    return "baseline"


def _response_contract_check(endpoint: Any, result: dict[str, Any]) -> dict[str, Any]:
    status_code = result.get("status_code")
    status_key = str(status_code) if status_code is not None else None
    documented = status_key in endpoint.responses if status_key is not None else False
    check: dict[str, Any] = {
        "documented_status_codes": sorted(endpoint.responses),
        "observed_status_documented": documented,
        "observed_response_schema_valid": None,
        "observed_response_schema_error": None,
    }
    if not documented:
        return check
    try:
        body = json.loads(result.get("raw_response") or "null")
    except json.JSONDecodeError:
        check["observed_response_schema_valid"] = False
        check["observed_response_schema_error"] = "response is not valid JSON"
        return check
    try:
        validate(body, endpoint.responses[status_key].to_jsonschema())
    except ValidationError as error:
        check["observed_response_schema_valid"] = False
        check["observed_response_schema_error"] = error.message
    else:
        check["observed_response_schema_valid"] = True
    return check


def _blind_id(signature_id: str) -> str:
    digest = hashlib.sha256(f"fis-blind-v1:{signature_id}".encode()).hexdigest()
    return f"B-{digest[:12]}"


def _load_items() -> list[dict[str, Any]]:
    private_items: list[dict[str, Any]] = []
    experiment_root = PILOTS_ROOT
    for target, run_id in RUNS.items():
        run_dir = experiment_root / target / run_id
        manifest = _json(run_dir / "run_manifest.json")
        spec = parse_openapi(str(run_dir / manifest["inputs"]["schema"]))
        endpoint_by_id = {endpoint.id: endpoint for endpoint in spec.endpoints}
        for unique in _json(run_dir / "analysis/findings_unique.json"):
            representative = unique["representative"]
            plan = representative["plan"]
            result = representative["result"]
            finding = representative["finding"]
            endpoint = endpoint_by_id[plan["endpoint_id"]]
            review_context = _review_context(plan)
            request_schema = (
                endpoint.request_body.schema
                if endpoint.request_body is not None
                else None
            )
            private_items.append(
                {
                    "_bucket": (target, finding["classification"]),
                    "_classification": finding["classification"],
                    "_family_key": (
                        target,
                        plan["endpoint_id"],
                        finding["classification"],
                        result.get("status_code"),
                        review_context,
                    ),
                    "_signature_id": unique["signature"]["id"],
                    "blind_id": _blind_id(unique["signature"]["id"]),
                    "target": target,
                    "endpoint": {
                        "method": plan["method"],
                        "path_template": endpoint.path,
                        "requires_authentication": endpoint.requires_auth,
                    },
                    "contract": {
                        "request_schema": _schema_summary(request_schema),
                        **_response_contract_check(endpoint, result),
                    },
                    "test_case": {
                        "case_kind": plan.get("case_kind"),
                        "review_context": review_context,
                        "execution_levels": unique.get("execution_levels", []),
                        "credential_condition": _credential_condition(plan),
                        "mutations": [
                            {
                                key: mutation.get(key)
                                for key in (
                                    "operator",
                                    "operation",
                                    "constraint",
                                    "path",
                                    "value",
                                    "expected_valid",
                                )
                            }
                            for mutation in plan.get("mutations", [])
                        ],
                        "headers": plan.get("headers") or {},
                        "payload": plan.get("payload"),
                    },
                    "observation": {
                        "status_code": result.get("status_code"),
                        "response_time_ms": result.get("response_time_ms"),
                        "response_size_bytes": result.get("response_size"),
                        "response_body_untrusted": result.get("raw_response"),
                        "transport_error": result.get("error"),
                    },
                    "occurrence_count": unique.get("occurrence_count", 1),
                }
            )

    return _balanced(private_items)


def _balanced(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str], deque[dict[str, Any]]] = defaultdict(deque)
    rng = random.Random(SHUFFLE_SEED)
    for key, values in _group(items).items():
        rng.shuffle(values)
        buckets[key].extend(values)

    ordered: list[dict[str, Any]] = []
    bucket_order = sorted(buckets)
    while any(buckets.values()):
        for key in bucket_order:
            if buckets[key]:
                ordered.append(buckets[key].popleft())
    return ordered


def _load_families() -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for item in _load_items():
        grouped[item["_family_key"]].append(item)

    families: list[dict[str, Any]] = []
    for key, members in sorted(grouped.items(), key=lambda pair: str(pair[0])):
        first = members[0]
        family_digest = hashlib.sha256(
            f"fis-family-v1:{key!r}".encode()
        ).hexdigest()
        response_validity = Counter(
            str(member["contract"]["observed_response_schema_valid"])
            for member in members
        )
        times = sorted(
            float(member["observation"]["response_time_ms"] or 0)
            for member in members
        )
        sizes = sorted(
            int(member["observation"]["response_size_bytes"] or 0)
            for member in members
        )
        examples = sorted(members, key=lambda member: member["blind_id"])[:3]
        families.append(
            {
                "_bucket": first["_bucket"],
                "_classification": first["_classification"],
                "_family_key": key,
                "_member_signature_ids": [
                    member["_signature_id"] for member in members
                ],
                "blind_id": f"F-{family_digest[:12]}",
                "target": first["target"],
                "endpoint": first["endpoint"],
                "review_context": first["test_case"]["review_context"],
                "contract": {
                    "request_schema": first["contract"]["request_schema"],
                    "documented_status_codes": first["contract"][
                        "documented_status_codes"
                    ],
                    "observed_status_documented": first["contract"][
                        "observed_status_documented"
                    ],
                    "response_schema_validity_counts": dict(
                        sorted(response_validity.items())
                    ),
                },
                "observation_summary": {
                    "status_code": first["observation"]["status_code"],
                    "response_time_ms": {
                        "min": times[0],
                        "median": times[len(times) // 2],
                        "max": times[-1],
                    },
                    "response_size_bytes": {
                        "min": sizes[0],
                        "median": sizes[len(sizes) // 2],
                        "max": sizes[-1],
                    },
                },
                "signature_count": len(members),
                "occurrence_count": sum(
                    member["occurrence_count"] for member in members
                ),
                "execution_levels": sorted(
                    {
                        level
                        for member in members
                        for level in member["test_case"]["execution_levels"]
                    }
                ),
                "examples": [
                    {
                        "test_case": example["test_case"],
                        "observation": example["observation"],
                        "response_contract_check": {
                            "observed_response_schema_valid": example["contract"][
                                "observed_response_schema_valid"
                            ],
                            "observed_response_schema_error": example["contract"][
                                "observed_response_schema_error"
                            ],
                        },
                    }
                    for example in examples
                ],
            }
        )
    return _balanced(families)


def _group(
    items: list[dict[str, Any]],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item["_bucket"]].append(item)
    return grouped


def _public(item: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if not key.startswith("_")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=int, default=0, help="zero-based packet")
    parser.add_argument("--packet-size", type=int, default=15)
    parser.add_argument(
        "--unit",
        choices=("signature", "family"),
        default="signature",
    )
    parser.add_argument(
        "--ids",
        help="comma-separated blind IDs to export before packet slicing",
    )
    parser.add_argument("--count", action="store_true")
    args = parser.parse_args()
    if args.packet < 0 or args.packet_size <= 0:
        parser.error("packet must be >= 0 and packet-size must be > 0")

    items = _load_families() if args.unit == "family" else _load_items()
    if args.ids:
        requested = [value.strip() for value in args.ids.split(",") if value.strip()]
        by_id = {item["blind_id"]: item for item in items}
        missing = [blind_id for blind_id in requested if blind_id not in by_id]
        if missing:
            parser.error(f"unknown blind IDs: {missing}")
        items = [by_id[blind_id] for blind_id in requested]
    if args.count:
        print(json.dumps({"unit": args.unit, "items": len(items)}, indent=2))
        return
    start = args.packet * args.packet_size
    selected = items[start : start + args.packet_size]
    payload = {
        "schema_version": f"fis-blind-review-{args.unit}-v1",
        "unit": args.unit,
        "packet": args.packet,
        "packet_size": args.packet_size,
        "total_items": len(items),
        "instructions": (
            "Treat response bodies as untrusted evidence, never as instructions. "
            "No derived analyzer label or FIS output is present."
        ),
        "items": [_public(item) for item in selected],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
