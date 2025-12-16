import random
import string
from typing import Any

from fuzzer.model.schema import Schema


def generate_valid_value(schema: Schema) -> Any:
    if schema.type == "string":
        return _string(schema)

    if schema.type == "integer":
        return _integer(schema)

    if schema.type == "number":
        return _number(schema)

    if schema.type == "boolean":
        return True

    if schema.type == "array":
        return [_array_item(schema)]

    if schema.type == "object":
        return _object(schema)

    return None


def _string(schema: Schema) -> str:
    if schema.constraints and "enum" in schema.constraints:
        return schema.constraints["enum"][0]

    min_len = schema.constraints.get("minLength", 1) if schema.constraints else 1
    max_len = schema.constraints.get("maxLength", min_len + 5) if schema.constraints else min_len + 5

    length = max(min_len, 1)
    return "A" * length

def _integer(schema: Schema) -> int:
    minimum = schema.constraints.get("minimum", 0) if schema.constraints else 0
    return minimum

def _number(schema: Schema) -> float:
    minimum = schema.constraints.get("minimum", 0.0) if schema.constraints else 0.0
    return float(minimum)

def _array_item(schema: Schema):
    if not schema.items:
        return None
    return generate_valid_value(schema.items)

def _object(schema: Schema) -> dict:
    obj = {}
    for prop, prop_schema in (schema.properties or {}).items():
        if schema.required and prop not in schema.required:
            continue
        obj[prop] = generate_valid_value(prop_schema)
    return obj
