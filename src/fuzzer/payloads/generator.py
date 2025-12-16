from collections.abc import Generator
from typing import Any

from fuzzer.model.endpoint import Endpoint
from fuzzer.model.schema import Schema
from fuzzer.model.parameter import Parameter

from fuzzer.generator.valid_generator import generate_valid_value


def generates_payloads(
    endpoint: Endpoint,
) -> Generator[tuple[str | None, dict[str, str]], None, None]:
    """
    Generate payloads and headers for a given endpoint,
    strictly guided by the OpenAPI contract.

    Yields:
        (payload, headers)
    """

    headers: dict[str, str] = {}

    # 1. Content-Type vindo do requestBody
    if endpoint.request_body:
        headers["Content-Type"] = endpoint.request_body.content_type

    # 2. Headers definidos como parameters
    for param in endpoint.parameters:
        if param.location != "header":
            continue

        headers[param.name] = _generate_header_value(param.schema)

    # 3. Payload
    if endpoint.request_body is None:
        yield None, headers
        return

    payload = _build_payload_from_schema(endpoint.request_body.schema)
    yield payload, headers


def _generate_header_value(schema: Schema) -> str:
    value = generate_valid_value(schema)
    return str(value)

def _build_payload_from_schema(schema: Schema) -> Any:
    """
    Recursively build a valid payload based on a Schema.
    """
    return generate_valid_value(schema)
