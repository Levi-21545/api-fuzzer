from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from urllib.parse import quote
from fuzzer.utils.patterns import compile_openapi_pattern


# Bound generation and mutation traversal, not response validation. Acyclic
# nesting and separate paths sharing a schema are unaffected.
MAX_SCHEMA_VISITS = 2

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
        return self._to_jsonschema({}, "#")

    def _to_jsonschema(self, active: dict[int, str], pointer: str) -> Dict[str, Any]:
        if self.type is None:
            return {}
        if id(self) in active:
            return {"$ref": active[id(self)]}
        active[id(self)] = pointer

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
                token = quote(name.replace("~", "~0").replace("/", "~1"), safe="~")
                props[name] = subschema._to_jsonschema(
                    active, f"{pointer}/properties/{token}"
                )
            js["properties"] = props
            if self.required:
                js["required"] = list(self.required)

        if self.type == "array":
            if self.min_items is not None:
                js["minItems"] = self.min_items
            if self.max_items is not None:
                js["maxItems"] = self.max_items
            if self.items is not None:
                js["items"] = self.items._to_jsonschema(active, f"{pointer}/items")

        del active[id(self)]
        return js


def walk_schema(schema: Schema, path=(), *, _ancestors: tuple[int, ...] = ()):
    if _ancestors.count(id(schema)) >= MAX_SCHEMA_VISITS:
        return
    yield path, schema
    ancestors = (*_ancestors, id(schema))

    if schema.type == "object":
        for name, prop in (schema.properties or {}).items():
            yield from walk_schema(prop, path + (name,), _ancestors=ancestors)

    if schema.type == "array" and schema.items:
        yield from walk_schema(schema.items, path + ("*",), _ancestors=ancestors)
