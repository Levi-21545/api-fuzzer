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
    Transforma endpoints em uma sequência de
    (endpoint, path, payload, headers)

    Se auth_headers for fornecido e o endpoint exigir autenticação,
    os headers de auth são mesclados nos headers da requisição.
    """
    for endpoint in endpoints:
        for path, headers, payload in generates_payloads(endpoint, mutation_engine, auth_context):
            merged_headers = headers
            if auth_headers and endpoint.requires_auth:
                merged_headers = {**headers, **auth_headers}
            yield endpoint, path, payload, merged_headers


def build_auth_probes(
    endpoints: list[Endpoint],
    auth_context: AuthContext | None = None,
) -> list[ExecutionPlanEntry]:
    """
    Gera probes de autenticação para endpoints que exigem security:
    1. Sem token (apenas headers básicos)
    2. Token inválido (Authorization: Bearer invalid_token)

    Os probes são inseridos no início do plano para executar
    antes das mutações lentas em servidores single-thread.
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

        probe_plan.append((endpoint, path, body, dict(probe_headers)))
        probe_plan.append(
            (endpoint, path, body, {**probe_headers, "Authorization": "Bearer invalid_token"})
        )
    return probe_plan
