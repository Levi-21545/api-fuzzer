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
        security_schemes = self.raw.get("components", {}).get("securitySchemes", {})
        global_security = self.raw.get("security")
        endpoints = []

        for path, methods in self.raw.get("paths", {}).items():
            path_servers = self._parse_servers(methods)
            path_parameters = methods.get("parameters", [])

            for method, data in methods.items():
                if method.lower() not in {"get", "post", "put", "patch", "delete"}:
                    continue

                operation_servers = self._parse_servers(data)
                operation_security = data.get("security")

                servers = (
                    operation_servers
                    or path_servers
                    or None
                )

                # [] means explicitly public; None inherits global security.
                resolved_security = (
                    operation_security
                    if operation_security is not None
                    else global_security
                )
                endpoints.append(
                    Endpoint(
                        path=path,
                        method=HttpMethod(method.upper()),
                        parameters=self._parse_parameters(
                            path_parameters,
                            data.get("parameters", []),
                        ),
                        request_body=self._parse_request_body(data),
                        responses=self._parse_responses(data),
                        servers=servers,
                        security=resolved_security,
                    )
                )

        return APISpec(
            base_urls=base_urls,
            endpoints=endpoints,
            security_schemes=security_schemes,
            global_security=global_security,
        )

    @staticmethod
    def _parse_servers(data: Dict[str, Any]) -> list[str]:
        servers = data.get("servers")
        if not servers:
            return []
        return [s["url"] for s in servers]

    def _parse_parameters(self, *parameter_groups: list[Dict[str, Any]]):
        parsed_by_identity: dict[tuple[str, str], Parameter] = {}
        for parameters in parameter_groups:
            for raw_parameter in parameters:
                parameter = self._resolve_local_ref(raw_parameter)
                parsed_by_identity[(parameter["name"], parameter["in"])] = (
                    Parameter(
                        name=parameter["name"],
                        location=parameter["in"],
                        required=parameter.get("required", False),
                        schema=self._parse_schema(parameter.get("schema", {})),
                    )
                )
        return list(parsed_by_identity.values())

    def _resolve_local_ref(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        reference = raw.get("$ref")
        if reference is None:
            return raw
        if not isinstance(reference, str) or not reference.startswith("#/"):
            raise ValueError(
                f"Only local OpenAPI references are supported: {reference}"
            )

        resolved: Any = self.raw
        for raw_token in reference[2:].split("/"):
            token = raw_token.replace("~1", "/").replace("~0", "~")
            if not isinstance(resolved, dict) or token not in resolved:
                raise ValueError(f"Unresolvable OpenAPI reference: {reference}")
            resolved = resolved[token]

        if not isinstance(resolved, dict):
            raise ValueError(
                f"OpenAPI reference does not point to an object: {reference}"
            )

        siblings = {key: value for key, value in raw.items() if key != "$ref"}
        return {**resolved, **siblings}

    def _parse_request_body(self, data: Dict[str, Any]):
        body = data.get("requestBody")
        if not body:
            return None
        body = self._resolve_local_ref(body)

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
            r = self._resolve_local_ref(r)
            content = r.get("content", {})
            if "application/json" not in content:
                responses[str(status)] = Schema(type=None)
                continue
            schema = content["application/json"].get("schema", {})
            responses[str(status)] = self._parse_schema(schema)
        return responses

    def _parse_schema(self, raw: Dict[str, Any]) -> Schema:
        if not raw:
            return Schema(type=None)
        raw = self._resolve_local_ref(raw)
        if "allOf" in raw:
            parts = [
                self._parse_schema(part)
                for part in raw["allOf"]
            ]
            siblings = {
                key: value
                for key, value in raw.items()
                if key != "allOf"
            }
            if any(
                key in siblings
                for key in (
                    "type",
                    "format",
                    "properties",
                    "items",
                    "required",
                    "readOnly",
                    "minItems",
                    "maxItems",
                )
            ):
                parts.append(self._parse_schema(siblings))
            return self._merge_all_of(parts)

        schema = Schema(
            type=raw.get("type"),
            format=raw.get("format"),
            read_only=raw.get("readOnly", False),
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
            "multipleOf",
            "enum",
            "pattern",
        ):
            if key in raw:
                schema.constraints[key] = raw.get(key)

        # OpenAPI 3.0 represents exclusive bounds as booleans beside
        # minimum/maximum. OpenAPI 3.1 uses the JSON Schema numeric form.
        for exclusive_key, bound_key in (
            ("exclusiveMinimum", "minimum"),
            ("exclusiveMaximum", "maximum"),
        ):
            exclusive_value = raw.get(exclusive_key)
            if exclusive_value is True and bound_key in raw:
                schema.constraints[exclusive_key] = raw[bound_key]
            elif (
                isinstance(exclusive_value, (int, float))
                and not isinstance(exclusive_value, bool)
            ):
                schema.constraints[exclusive_key] = exclusive_value

        if schema.type == "object":
            for prop, sub in raw.get("properties", {}).items():
                schema.properties[prop] = self._parse_schema(sub)

        if schema.type == "array":
            schema.items = self._parse_schema(raw.get("items", {}))

        return schema

    @staticmethod
    def _merge_all_of(parts: list[Schema]) -> Schema:
        merged = Schema(type=None)
        for part in parts:
            if part.type is not None:
                if merged.type is not None and merged.type != part.type:
                    raise ValueError(
                        "Incompatible schema types in allOf: "
                        f"{merged.type} and {part.type}"
                    )
                merged.type = part.type
            if part.format is not None:
                merged.format = part.format
            merged.read_only = merged.read_only or part.read_only
            merged.constraints.update(part.constraints)
            merged.properties.update(part.properties)
            merged.required.extend(
                name
                for name in part.required
                if name not in merged.required
            )
            if part.items is not None:
                merged.items = part.items
            if part.min_items is not None:
                merged.min_items = max(
                    value
                    for value in (merged.min_items, part.min_items)
                    if value is not None
                )
            if part.max_items is not None:
                merged.max_items = min(
                    value
                    for value in (merged.max_items, part.max_items)
                    if value is not None
                )
        return merged
