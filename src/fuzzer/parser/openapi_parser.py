import yaml
from typing import Dict, Any

from fuzzer.model.api_spec import APISpec
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.parameter import Parameter
from fuzzer.model.request_body import RequestBody
from fuzzer.model.schema import Schema

from fuzzer.model.http import HttpMethod


def parse_openapi(spec_path: str) -> APISpec:
    """
    Facade function to parse an OpenAPI specification file.

    This function exists to decouple the CLI/orchestrator layer
    from the concrete OpenAPIParser implementation.
    """
    parser = OpenAPIParser(spec_path)
    return parser.parse()


class OpenAPIParser:
    def __init__(self, spec_path: str):
        with open(spec_path, "r") as f:
            self.raw = yaml.safe_load(f)

    def parse(self) -> APISpec:
        base_urls = self._parse_servers(self.raw)
        endpoints = []

        for path, methods in self.raw.get("paths", {}).items():
            path_servers = self._parse_servers(methods)

            for method, data in methods.items():
                if method.lower() not in {"get", "post", "put", "patch", "delete"}:
                    continue

                operation_servers = self._parse_servers(data)

                servers = (
                    operation_servers
                    or path_servers
                    or None
                )

                endpoints.append(
                    Endpoint(
                        path=path,
                        method=HttpMethod(method.upper()),
                        parameters=self._parse_parameters(data),
                        request_body=self._parse_request_body(data),
                        responses=self._parse_responses(data),
                        servers=servers,
                    )
                )

        return APISpec(base_urls=base_urls, endpoints=endpoints)

    @staticmethod
    def _parse_servers(data: Dict[str, Any]) -> list[str]:
        servers = data.get("servers")
        if not servers:
            return []
        return [s["url"] for s in servers]

    def _parse_parameters(self, data: Dict[str, Any]):
        params = []
        for p in data.get("parameters", []):
            params.append(
                Parameter(
                    name=p["name"],
                    location=p["in"],
                    required=p.get("required", False),
                    schema=self._parse_schema(p.get("schema", {})),
                )
            )
        return params

    def _parse_request_body(self, data: Dict[str, Any]):
        body = data.get("requestBody")
        if not body:
            return None

        content = body.get("content", {})

        if "application/json" in content:
            request_body = RequestBody(
                content_type="application/json",
                schema=self._parse_schema(content["application/json"]["schema"]),
            )
        else:
            request_body = None

        return request_body

    def _parse_responses(self, data: Dict[str, Any]):
        responses = {}
        for status, r in data.get("responses", {}).items():
            content = r.get("content", {})
            if "application/json" not in content:
                continue
            schema = content["application/json"].get("schema", {})
            responses[status] = self._parse_schema(schema)
        return responses

    def _parse_schema(self, raw: Dict[str, Any]) -> Schema:
        if not raw:
            return Schema(type=None)

        schema = Schema(
            type=raw.get("type"),
            format=raw.get("format"),
            constraints={},
            properties={},
            required=raw.get("required", []),
            min_items=raw.get("minItems"),
            max_items=raw.get("maxItems"),
        )

        for key in (
            "minLength",
            "maxLength",
            "minimum",
            "maximum",
            "enum",
            "pattern",
        ):
            if key in raw:
                schema.constraints[key] = raw.get(key)

        if schema.type == "object":
            for prop, sub in raw.get("properties", {}).items():
                schema.properties[prop] = self._parse_schema(sub)

        if schema.type == "array":
            schema.items = self._parse_schema(raw.get("items", {}))

        return schema
