from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from fuzzer.utils.patterns import compile_openapi_pattern

@dataclass
class Schema:
    type: Optional[str]
    format: Optional[str] = None
    constraints: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, "Schema"] = field(default_factory=dict)
    items: Optional["Schema"] = None
    required: List[str] = field(default_factory=list)
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    read_only: bool = False

    def to_jsonschema(self) -> Dict[str, Any]:
        """Convert this schema to a dict accepted by jsonschema.validate."""
        if self.type is None:
            return {}

        js: Dict[str, Any] = {"type": self.type}

        if self.format:
            js["format"] = self.format
        if self.read_only:
            js["readOnly"] = True

        # Copy scalar constraints directly
        for key in (
            "minLength",
            "maxLength",
            "minimum",
            "maximum",
            "exclusiveMinimum",
            "exclusiveMaximum",
            "multipleOf",
            "enum",
            "pattern",
        ):
            if key in self.constraints:
                value = self.constraints[key]
                if key == "pattern" and isinstance(value, str):
                    value = compile_openapi_pattern(value).pattern
                js[key] = value

        if self.type == "object":
            props: Dict[str, Any] = {}
            for name, subschema in (self.properties or {}).items():
                props[name] = subschema.to_jsonschema()
            js["properties"] = props
            if self.required:
                js["required"] = list(self.required)

        if self.type == "array":
            if self.min_items is not None:
                js["minItems"] = self.min_items
            if self.max_items is not None:
                js["maxItems"] = self.max_items
            if self.items is not None:
                js["items"] = self.items.to_jsonschema()

        return js

def walk_schema(schema: Schema, path=()):
    yield path, schema

    if schema.type == "object":
        for name, prop in (schema.properties or {}).items():
            yield from walk_schema(prop, path + (name,))

    if schema.type == "array" and schema.items:
        yield from walk_schema(schema.items, path + ("*",))
