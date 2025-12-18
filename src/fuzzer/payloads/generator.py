from collections.abc import Generator
from typing import Any

from fuzzer.model.endpoint import Endpoint
from fuzzer.model.schema import Schema

from fuzzer.generator.valid_generator import generate_valid_value

from fuzzer.mutator.engine import MutationEngine


def generates_payloads(
    endpoint: Endpoint,
    mutation_engine: MutationEngine,
) -> Generator[tuple[str | None, dict[str, str]], None, None]:
    """
    Generate payloads and headers for a given endpoint,
    strictly guided by the OpenAPI contract.

    Yields:
        (payload, headers)
    """

    base_headers: dict[str, str] = {}

    # 1. Content-Type vindo do requestBody
    if endpoint.request_body:
        base_headers["Content-Type"] = endpoint.request_body.content_type

    # 2. Headers definidos como parameters
    for param in endpoint.parameters:
        if param.location != "header":
            continue

        base_headers[param.name] = _generate_header_value(param.schema)

    # 3. Sem request body
    if endpoint.request_body is None:
        yield None, base_headers
        return
    
    print("Generating mutated payloads...")

    # 4. Payloads mutados
    payloads = mutation_engine.generate(endpoint.request_body.schema)

    print(f"Generated {len(payloads)} payloads for endpoint {endpoint.path} [{endpoint.method}]")

    for payload in payloads:
        # copia defensiva: headers não devem ser mutados entre execuções
        headers = dict(base_headers)
        yield payload, headers
    

def _generate_header_value(schema: Schema) -> str:
    value = generate_valid_value(schema)
    return str(value)