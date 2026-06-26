import urllib.parse

from fuzzer.model.endpoint import Endpoint
from fuzzer.model.schema import Schema

from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.engine import MutationEngine
from fuzzer.utils.types import Headers, AuthContext, PayloadGenerator

_KNOWN_USER_PARAMS = {"username", "user", "email", "userid", "user_id"}

def generates_payloads(
    endpoint: Endpoint,
    mutation_engine: MutationEngine,
    auth_context: AuthContext | None = None,
) -> PayloadGenerator:
    headers: Headers = {}
    path = _resolve_path(endpoint, auth_context)

    if endpoint.request_body:
        headers["Content-Type"] = endpoint.request_body.content_type

    for param in endpoint.parameters:
        if param.location == "header":
            headers[param.name] = _generate_header_value(param.schema)

    if endpoint.request_body is None:
        yield path, headers, None
        return

    print("Generating mutated payloads...")

    payloads = mutation_engine.generate(endpoint.request_body.schema)

    print(f"Generated {len(payloads)} payloads for endpoint {endpoint.path} [{endpoint.method}]")

    for payload in payloads:
        yield path, dict(headers), payload


def _generate_header_value(schema: Schema) -> str:
    return str(generate_valid_value(schema))

def _resolve_path(endpoint: Endpoint, auth_context: AuthContext | None = None) -> str:
    path = endpoint.path
    query_parts: list[str] = []

    for param in endpoint.parameters:
        if param.location == "path":
            key = param.name.lower()
            if auth_context and key in _KNOWN_USER_PARAMS and key in auth_context:
                value = auth_context[key]
            else:
                value = generate_valid_value(param.schema)
            path = path.replace(f"{{{param.name}}}", str(value))
        elif param.location == "query":
            value = str(generate_valid_value(param.schema))
            encoded = urllib.parse.quote(param.name) + "=" + urllib.parse.quote(value)
            query_parts.append(encoded)

    if query_parts:
        path += "?" + "&".join(query_parts)

    return path
