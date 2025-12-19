from collections.abc import Generator

from fuzzer.model.endpoint import Endpoint
from fuzzer.model.schema import Schema

from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.engine import MutationEngine

from fuzzer.utils.helpers import uuid4


def generates_payloads(
    endpoint: Endpoint,
    mutation_engine: MutationEngine,
) -> Generator[tuple[str, dict[str, str], dict | None], None, None]:
    """
    Generate path, payloads and headers for a given endpoint,
    strictly guided by the OpenAPI contract.

    Yields:
        (resolved_path, headers, payload)
    """

    headers: dict[str, str] = {}
    path = _resolve_path(endpoint)

    # 1. Content-Type
    if endpoint.request_body:
        headers["Content-Type"] = endpoint.request_body.content_type

    # 2. Headers declarados no schema
    for param in endpoint.parameters:
        if param.location == "header":
            headers[param.name] = _generate_header_value(param.schema)

    # 3. Endpoint sem body
    if endpoint.request_body is None:
        yield path, headers, None
        return
    
    print("Generating mutated payloads...")

    # 4. Payloads mutados
    payloads = mutation_engine.generate(endpoint.request_body.schema)

    print(f"Generated {len(payloads)} payloads for endpoint {endpoint.path} [{endpoint.method}]")

    # Payloads mutados
    for payload in payloads:
        yield path, dict(headers), payload  # cópia defensiva
    

def _generate_header_value(schema: Schema) -> str:
    return str(generate_valid_value(schema))

def _resolve_path(endpoint: Endpoint) -> str:
    path = endpoint.path

    for param in endpoint.parameters:
        if param.location == "path":
            # value = generate_valid_value(param.schema)
            value = uuid4()
            path = path.replace(f"{{{param.name}}}", str(value))

    return path