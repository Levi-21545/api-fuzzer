from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class Schema:
    type: Optional[str]
    format: Optional[str] = None
    constraints: Dict[str, Any] = None
    properties: Dict[str, "Schema"] = None
    items: Optional["Schema"] = None
    required: List[str] = None

def walk_schema(schema: Schema, path=()):
    yield path, schema

    if schema.type == "object":
        for name, prop in (schema.properties or {}).items():
            yield from walk_schema(prop, path + (name,))

    if schema.type == "array" and schema.items:
        yield from walk_schema(schema.items, path + ("*",))