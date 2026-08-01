from fuzzer.model.endpoint import Endpoint
from fuzzer.mutator.engine import MutationEngine
from fuzzer.payloads.generator import generates_payloads
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.utils.types import Headers, AuthContext, ExecutionPlanEntry, ExecutionPlan


def build_execution_plan(
        endpoints: list[Endpoint],
        mutation_engine: MutationEngine,
        auth_context: AuthContext | None = None,
        auth_headers: Headers | None = None,
    ) -> ExecutionPlan:
    """
    Convert endpoints into executable request cases.

    Authentication headers are merged only into endpoints that require them.
    """
    case_number = 0
    for endpoint in endpoints:
        for path, headers, payload, case in generates_payloads(
            endpoint, mutation_engine, auth_context
        ):
            merged_headers = headers
            if auth_headers and endpoint.requires_auth:
                merged_headers = {**headers, **auth_headers}
            case_number += 1
            yield ExecutionPlanEntry(
                endpoint=endpoint,
                path=path,
                payload=payload,
                headers=merged_headers,
                case_id=f"case-{case_number:06d}",
                case_kind=case["kind"],
                mutations=case["mutations"],
            )


def build_auth_probes(
    endpoints: list[Endpoint],
    auth_context: AuthContext | None = None,
    auth_headers: Headers | None = None,
) -> list[ExecutionPlanEntry]:
    """
    Generate authentication probes for secured endpoints:
    1. Request without a token
    2. Request with an invalid bearer token

    Probes are placed before slower mutations for single-threaded targets.
    """
    probe_plan: list[ExecutionPlanEntry] = []
    for endpoint in endpoints:
        if not endpoint.requires_auth:
            continue

        path = endpoint.path
        for param in endpoint.parameters:
            if param.location == "path":
                val = auth_context.get(param.name.lower()) if auth_context else None
                path = path.replace(f"{{{param.name}}}", val or "A")

        probe_headers: Headers = {}
        if endpoint.request_body:
            probe_headers["Content-Type"] = endpoint.request_body.content_type
            body = generate_valid_value(endpoint.request_body.schema)
        else:
            body = None

        probe_number = len(probe_plan) + 1
        invalid_auth_headers = {
            name: _invalid_credential(value)
            for name, value in (auth_headers or {}).items()
        } or {"Authorization": "Bearer invalid_token"}
        probe_plan.append(
            ExecutionPlanEntry(
                endpoint=endpoint,
                path=path,
                payload=body,
                headers=dict(probe_headers),
                case_id=f"auth-probe-{probe_number:06d}",
                case_kind="auth_probe",
                mutations=[],
                auth_probe_kind="missing_credential",
            )
        )
        probe_number = len(probe_plan) + 1
        probe_plan.append(
            ExecutionPlanEntry(
                endpoint=endpoint,
                path=path,
                payload=body,
                headers={**probe_headers, **invalid_auth_headers},
                case_id=f"auth-probe-{probe_number:06d}",
                case_kind="auth_probe",
                mutations=[],
                auth_probe_kind="invalid_credential",
            )
        )
    return probe_plan


def _invalid_credential(value: str) -> str:
    scheme, separator, _credential = value.partition(" ")
    return f"{scheme} invalid_token" if separator else "invalid_token"
