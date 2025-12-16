import yaml
from typing import Dict, Any
from fuzzer.model.types import APISpec, Endpoint, Parameter, Schema


class OpenAPIParser:
    def __init__(self, spec_path: str):
        with open(spec_path, "r") as f:
            self.raw = yaml.safe_load(f)

    def parse(self) -> APISpec:
        base_url = self.raw["servers"][0]["url"]
        endpoints = []

        for path, methods in self.raw.get("paths", {}).items():
            for method, data in methods.items():
                endpoints.append(
                    Endpoint(
                        path=path,
                        method=method.upper(),
                        parameters=self._parse_parameters(data),
                        request_body=self._parse_request_body(data),
                        responses=self._parse_responses(data),
                    )
                )

        return APISpec(base_url=base_url, endpoints=endpoints)

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
        if "application/json" not in content:
            return None

        schema = content["application/json"].get("schema", {})
        return self._parse_schema(schema)

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
                schema.constraints[key] = raw[key]

        if schema.type == "object":
            for prop, sub in raw.get("properties", {}).items():
                schema.properties[prop] = self._parse_schema(sub)

        if schema.type == "array":
            schema.items = self._parse_schema(raw.get("items", {}))

        return schema
