from typing import Any

from fuzzer.model.schema import Schema

from fuzzer.utils.helpers import uuid4, email, datetime
from fuzzer.utils.patterns import compile_openapi_pattern


def generate_valid_value(schema: Schema | None) -> Any:
    if not schema:
        return None

    if schema.type == "string":
        return _string(schema)

    if schema.type == "integer":
        return _integer(schema)

    if schema.type == "number":
        return _number(schema)

    if schema.type == "boolean":
        return True

    if schema.type == "array":
        # Contract: at least minItems; choice: max(minItems, 1) items.
        size = schema.min_items if isinstance(schema.min_items, int) else 1
        return [_array_item(schema) for _ in range(max(size, 1))]

    if schema.type == "object":
        return _object(schema)

    return None


def _string(schema: Schema) -> str:
    if schema.constraints and "enum" in schema.constraints:
        return schema.constraints["enum"][0]

    if schema.format == "uuid":
        return uuid4()
    if schema.format == "email":
        return email()
    if schema.format == "date-time":
        return datetime()

    constraints = schema.constraints or {}
    min_len = constraints.get("minLength", 0)
    max_len = constraints.get("maxLength")
    length = max(min_len, 1)
    if isinstance(max_len, int):
        length = min(length, max_len)

    pattern = constraints.get("pattern")
    if isinstance(pattern, str):
        # Contract: pattern match; choice: first matching bounded candidate.
        try:
            compiled = compile_openapi_pattern(pattern)
            for unit in ("A", "0"):
                candidate = unit * length
                if compiled.search(candidate):
                    return candidate
            for candidate in ("0.0", "user@example.com", "A-A"):
                if len(candidate) < min_len:
                    continue
                if isinstance(max_len, int) and len(candidate) > max_len:
                    continue
                if compiled.search(candidate):
                    return candidate
        except ValueError:
            pass

    return "A" * length

def _integer(schema: Schema) -> int:
    constraints = schema.constraints or {}

    value = 0
    if "exclusiveMinimum" in constraints:
        value = int(constraints["exclusiveMinimum"]) + 1
    elif "minimum" in constraints:
        value = int(constraints["minimum"])
    elif "exclusiveMaximum" in constraints:
        value = min(value, int(constraints["exclusiveMaximum"]) - 1)
    elif "maximum" in constraints:
        value = min(value, int(constraints["maximum"]))

    multiple_of = constraints.get("multipleOf")
    if isinstance(multiple_of, int) and multiple_of > 0:
        remainder = value % multiple_of
        if remainder:
            value += multiple_of - remainder
    return value

def _number(schema: Schema) -> float:
    constraints = schema.constraints or {}
    value = 0.0
    if "exclusiveMinimum" in constraints:
        value = float(constraints["exclusiveMinimum"]) + 0.5
    elif "minimum" in constraints:
        value = float(constraints["minimum"])
    elif "exclusiveMaximum" in constraints:
        value = min(value, float(constraints["exclusiveMaximum"]) - 0.5)
    elif "maximum" in constraints:
        value = min(value, float(constraints["maximum"]))

    multiple_of = constraints.get("multipleOf")
    if isinstance(multiple_of, (int, float)) and multiple_of > 0:
        value = round(round(value / multiple_of) * multiple_of, 12)
        if "minimum" in constraints and value < constraints["minimum"]:
            value = round(value + multiple_of, 12)
    return value

def _array_item(schema: Schema):
    if not schema.items:
        return None
    return generate_valid_value(schema.items)

def _object(schema: Schema) -> dict[str, Any]:
    obj = {}
    for prop, prop_schema in (schema.properties or {}).items():
        # With required declared, omit optional properties from the baseline.
        if schema.required and prop not in schema.required:
            continue
        obj[prop] = generate_valid_value(prop_schema)
    return obj
